#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Read-only Ardour source identity and patch-state verification.
# Exit 0: exact patched file; 3: pristine/not yet applied;
# 1: incompatible patch or unexpected local change; 2: invalid prerequisites.
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: bash scripts/record_source_identity.sh /path/to/ardour-7.5" >&2
  exit 2
fi
if ! command -v git >/dev/null 2>&1 || ! command -v shasum >/dev/null 2>&1; then
  echo "NG: git and shasum must be available" >&2
  exit 2
fi
if [ ! -d "$1" ]; then
  echo "NG: source directory does not exist" >&2
  exit 2
fi
SRC="$(cd "$1" && pwd -P)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PATCH="$SCRIPT_DIR/../patches/0001-catalina-gtk-quartz-canvas-fallback.patch"
F='libs/gtkmm2ext/nsglview.mm'

if [ ! -f "$PATCH" ] || [ ! -f "$SRC/$F" ]; then
  echo "NG: patch or source file is missing" >&2
  exit 2
fi
if ! git -C "$SRC" rev-parse --is-inside-work-tree 2>/dev/null | grep -qx true; then
  echo "NG: source is not a Git working tree; record the archive URL and SHA-256 instead" >&2
  exit 2
fi
TOP="$(git -C "$SRC" rev-parse --show-toplevel)"
if [ "$(cd "$TOP" && pwd -P)" != "$SRC" ]; then
  echo "NG: supplied source directory is not the Git repository root" >&2
  exit 2
fi
HEAD="$(git -C "$SRC" rev-parse --verify 'HEAD^{commit}')"

printf '\n========== Source identity: start ==========\n'
printf 'HEAD: %s\n' "$HEAD"
printf 'Description: '
git -C "$SRC" describe --tags --always --dirty 2>/dev/null || printf '(unavailable)\n'
printf 'Affected-file working-tree status:\n'
git -C "$SRC" status --short -- "$F"
printf 'Local file SHA-256: '
shasum -a 256 "$SRC/$F" | awk '{print $1}'

TMP="$(mktemp -d "${TMPDIR:-/tmp/}ardour-source-identity.XXXXXX")"
trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/libs/gtkmm2ext"
if ! git -C "$SRC" show "$HEAD:$F" > "$TMP/$F"; then
  echo "NG: cannot read the pristine file from HEAD" >&2
  exit 2
fi
printf 'Pristine HEAD file SHA-256: '
shasum -a 256 "$TMP/$F" | awk '{print $1}'
printf 'Patch check against pristine Git HEAD: '

if ! (cd "$TMP" && git apply --check "$PATCH" >/dev/null 2>&1); then
  printf 'FAIL (patch does not apply to this source revision)\n'
  printf 'Result: FAIL (patch context mismatch; no local file changed)\n'
  printf '========== Source identity: end ==========\n'
  exit 1
fi
printf 'PASS\n'
if ! (cd "$TMP" && git apply "$PATCH"); then
  printf 'Result: FAIL (isolated patch application failed; no local file changed)\n'
  printf '========== Source identity: end ==========\n'
  exit 1
fi
printf 'Patched HEAD file SHA-256: '
shasum -a 256 "$TMP/$F" | awk '{print $1}'
printf 'Local file state: '

status=1
if cmp -s "$TMP/$F" "$SRC/$F"; then
  printf 'PASS (exactly matches the patched HEAD file)\n'
  status=0
else
  # Recreate pristine HEAD independently; the copied file was patched above.
  if git -C "$SRC" show "$HEAD:$F" | cmp -s - "$SRC/$F"; then
    printf 'NOT YET APPLIED (local file exactly matches pristine HEAD)\n'
    status=3
  else
    printf 'FAIL (local file contains unexpected differences)\n'
    status=1
  fi
fi

printf 'Tracked-file changes (review before publication):\n'
git -C "$SRC" status --short --untracked-files=no
printf 'NOTE: Untracked files are excluded from this status output.\n'
if [ "$status" -eq 0 ]; then
  printf 'Result: PASS (verified patch applied exactly)\n'
elif [ "$status" -eq 3 ]; then
  printf 'Result: NOT YET APPLIED (verification not complete; exit 3)\n'
else
  printf 'Result: FAIL (source differs from expected patch; exit 1)\n'
fi
printf '========== Source identity: end ==========\n'
exit "$status"
