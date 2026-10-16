#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Prepare the documentation-and-patch repository locally.
# Does not commit, create GitHub repositories, push, or modify the Ardour source.
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
# This script can run in any directory name; the exact 24-file allowlist
# and the Git preflight (no existing commits or remotes) protect its scope.
PYTHON="python3"

if [ -x "$HOME/DTM/build-env/gtk-osx-2022/runtime/python-3.10.2/bin/python3" ]; then
  PYTHON="$HOME/DTM/build-env/gtk-osx-2022/runtime/python-3.10.2/bin/python3"
elif [ -x "$HOME/DTM/build-env/gtk-osx-2022/runtime/python-3.10.2/bin/python" ]; then
  PYTHON="$HOME/DTM/build-env/gtk-osx-2022/runtime/python-3.10.2/bin/python"
fi

exit_report() {
  rc=$?
  echo
  printf '========== Step 161: result end (exit code: %s) ==========\n' "$rc"
}
trap exit_report EXIT

abort() { printf 'NG: %s\n' "$*" >&2; exit 1; }

printf '\n========== Step 161: result start ==========\n'
printf '\n[1. Validate the target directory]\n'

[ -f "$ROOT/README.md" ] && [ -f "$ROOT/LICENSE" ] && [ -f "$ROOT/GITHUB_SETUP.md" ] || abort "Not the expected publication package"
[ ! -e "$ROOT/waf" ] && [ ! -d "$ROOT/gtk2_ardour" ] && [ ! -d "$ROOT/libs/ardour" ] || abort "Ardour source tree detected; aborting"
command -v git >/dev/null 2>&1 || abort "Git command not installed"
command -v "$PYTHON" >/dev/null 2>&1 || abort "Python 3 not found"

printf 'Package: %s\n' "$ROOT"
printf 'Git: %s\n' "$(git --version)"
printf 'Python: %s\n' "$("$PYTHON" --version 2>&1)"

printf '\n[2. Review exact file list and basic secret/binary indicators]\n'
"$PYTHON" - "$ROOT" <<'PYCODE'
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
expected = {
    '.gitignore', 'BUILD.md', 'BUILD_RECORD.md', 'COPYRIGHT_REVIEW.md',
    'GITHUB_SETUP.md', 'LICENSE', 'LICENSE_SCOPE.md', 'PATCHES.md',
    'PUBLISHING.md', 'README.md', 'RELEASE_CHECKLIST.md', 'REVIEW_REPORT.md',
    'SOURCES.md', 'SOURCE_IDENTITY.md', 'THIRD_PARTY_LICENSES.md',
    'UPSTREAM_LICENSES/GPL-2.0.txt', 'UPSTREAM_LICENSES/README.md',
    'inventory/known-components.csv', 'inventory/verified-source-checksums.csv',
    'patches/0001-catalina-gtk-quartz-canvas-fallback.patch',
    'scripts/audit_bundle.py', 'scripts/record_source_identity.sh',
    'scripts/prepare_git_repository.sh', 'tests/test_audit_bundle.py',
}
actual = set()
issues = []
patterns = {
    'absolute macOS home path': re.compile(r'/' + r'Users/[^\s/]+/'),
    'personal token pattern': re.compile(r'(?i)(?:ghp_|gho_|ghu_|ghs_|github_pat_)[A-Za-z0-9_]{12,}'),
    'AWS access key candidate': re.compile(r'(?<![A-Z0-9])(?:AKIA|ASIA)[A-Z0-9]{16}(?![A-Z0-9])'),
    'private key block': re.compile(r'-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----'),
    'password assignment': re.compile(r'(?im)^\s*(?:password|passwd|secret|api_key|access_token)\s*[:=]\s*\S+'),
}
for f in root.rglob('*'):
    if '.git' in f.relative_to(root).parts:
        continue
    rel = f.relative_to(root).as_posix()
    if f.is_symlink():
        issues.append(f'{rel}: symbolic links are not permitted in this publication package')
        continue
    if not f.is_file():
        continue
    actual.add(rel)
    if f.stat().st_size > 1024 * 1024:
        issues.append(f'{rel}: exceeds 1 MiB documentation-only size limit')
        continue
    data = f.read_bytes()
    if b'\x00' in data:
        issues.append(f'{rel}: contains binary NUL bytes')
        continue
    try:
        content = data.decode('utf-8')
    except UnicodeDecodeError:
        issues.append(f'{rel}: not UTF-8 text')
        continue
    for name, pattern in patterns.items():
        if pattern.search(content):
            issues.append(f'{rel}: {name} - manual review required')
missing = sorted(expected - actual)
extra = sorted(actual - expected)
if missing:
    issues.append('missing files: ' + ', '.join(missing))
if extra:
    issues.append('unexpected files: ' + ', '.join(extra))
if issues:
    print('NG: file-review issues:')
    for issue in issues:
        print(' -', issue)
    raise SystemExit(1)
print(f'OK: {len(expected)} approved text files; no candidate secret/binary/absolute-user-path indicators')
print('NOTE: Automated checks cannot prove absence of sensitive information or copyright issues.')
PYCODE

printf '\n[3. Run bundled Python tests]\n'
(cd "$ROOT" && PYTHONDONTWRITEBYTECODE=1 "$PYTHON" -B -m unittest discover -s tests -v)

printf '\n[4. Initialize only this local Git repository]\n'
if [ ! -e "$ROOT/.git" ]; then
  git -C "$ROOT" init >/dev/null
  git -C "$ROOT" symbolic-ref HEAD refs/heads/main
  printf 'OK: initialized main branch\n'
else
  [ -d "$ROOT/.git" ] || abort "Unexpected .git entry type"
  [ "$(git -C "$ROOT" rev-parse --show-toplevel)" = "$ROOT" ] || abort "Git root mismatch"
  [ "$(git -C "$ROOT" symbolic-ref --short HEAD)" = main ] || abort "Existing Git branch is not main"
  if git -C "$ROOT" rev-parse --verify HEAD >/dev/null 2>&1; then
    abort "Local repository already has commits; refusing to touch history"
  fi
  printf 'OK: existing uncommitted main branch reused\n'
fi

# Do not stage anything in an existing repository connected to a remote.
# This script is not for already-published clones or updating history.
if git -C "$ROOT" remote | grep -q .; then
  abort "Existing Git remote detected; do not use this first-time preparer"
fi

printf '\n[5. Stage and validate the initial changes]\n'
git -C "$ROOT" add -A
git -C "$ROOT" diff --cached --check || abort "Git whitespace/content check failed"

"$PYTHON" - "$ROOT" <<'PYCODE'
from pathlib import Path
import subprocess
import sys
root=Path(sys.argv[1])
files=subprocess.check_output(['git','-C',str(root),'diff','--cached','--name-only','--diff-filter=ACMR','-z']).split(b'\x00')
files=[f.decode('utf-8') for f in files if f]
for f in files:
    if f.endswith(('.app','.dmg','.pkg','.zip','.tar','.tar.gz','.tar.xz','.dylib','.so','.a','.o','.log')):
        raise SystemExit('NG: disallowed staged path: '+f)
print(f'OK: {len(files)} text files staged; binary/app/archive extensions absent')
PYCODE

echo '========== Staged files: start =========='
git -C "$ROOT" diff --cached --stat
echo '========== Staged files: end =========='

printf '\n[6. Publication safeguards]\n'
if git -C "$ROOT" remote | grep -q .; then
  abort "Unexpected existing Git remote; manually review"
fi
if git -C "$ROOT" rev-parse --verify HEAD >/dev/null 2>&1; then
  abort "Unexpected committed history"
fi
printf 'OK: no Git remote and no commit; nothing has been uploaded\n'
printf 'RECORDED: publisher ownership and MIT licensing self-attestation (Step 163)\n'
printf 'PENDING: final human staged-content/privacy approval and any applicable third-party/employer permissions\n'
printf 'PENDING: public repository approval, creation and first push\n'
printf 'NEXT: read GITHUB_SETUP.md; do not publish until all gates are cleared\n'
printf 'OK: Step 161 local preparation completed\n'
