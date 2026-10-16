# Publishing the documentation repository on GitHub

This is a **documentation-and-patch** repository. It contains **no app binary or third-party libraries**.

**Publication status (2026-10-16):** The publisher approved the initial 24-file
text/patch package in Step 166 and published it to the public GitHub repository
[`DJshingo/ardour-7.5-catalina-unofficial-build`](https://github.com/DJshingo/ardour-7.5-catalina-unofficial-build)
in Step 169. Step 170 verified anonymous access, the `main` commit and
24-file tree; Step 171-A updated the README; and Step 172 verified the About
metadata and eight topics. **The first-publication procedure below is retained
as a historical guide, not as an outstanding task or a reason to recreate the
repository.** Binary release clearance remains separate and incomplete.

## Before the first public commit

1. Review `README.md`, `BUILD.md`, `PATCHES.md`, `THIRD_PARTY_LICENSES.md` and `RELEASE_CHECKLIST.md`.
2. Review the verified local source record in `SOURCE_IDENTITY.md` (HEAD `e1950ec49e601864f06e316ba8cee730a3964989`; pristine-file patch match passed). Step 160-B recorded configured `origin` and verified the official mirror `7.5` tag; these checks agree with local `HEAD`. Check for untracked files/submodules and do not claim the original clone URL or cryptographic tag authenticity has been established. Do not publish raw machine logs.
3. Review [`LICENSE`](LICENSE) (MIT) and [`LICENSE_SCOPE.md`](LICENSE_SCOPE.md). **The publisher adopted the collective MIT notice in Step 160-E and self-attested in Step 163 to owning and being able to MIT-license the independently prepared work; see [`COPYRIGHT_REVIEW.md`](COPYRIGHT_REVIEW.md). This is a publisher declaration rather than independent legal proof. Confirm and address any applicable third-party/employer rights and manually approve staged content before publication. If actual ownership differs, correct the notice prior to the public commit.** The Ardour-derived patch uses GPL-2.0-or-later, not MIT; `UPSTREAM_LICENSES/GPL-2.0.txt` remains a separate upstream reference. A repository marked public is not an automatic grant to relicense upstream code.
4. Review the staged file list for secrets and personal paths. Run `python3 -m unittest discover -s tests -v` to check audit helpers and confirm all included ZIP members are expected. Read `REVIEW_REPORT.md` for open items.

For the verified Step 161 local staging process, see [`GITHUB_SETUP.md`](GITHUB_SETUP.md). The helper script stages files only; it does not create a commit or remote.

## Suggested repository name

`ardour-7.5-catalina-unofficial-build` (check name availability before selecting it).

## Initial local Git preparation and first commit

**Fresh reviewed package, no Git history or remote:** run the validated
one-time preparer in the documentation directory, **not** in the Ardour source
checkout:

```bash
bash scripts/prepare_git_repository.sh
```

**Original build Mac (Step 163-B or later):** a local `main` repository and
24 staged files already exist. **Do not run `git init` again.** Bring the
staged files into exact agreement with the latest reviewed package before
checking them. For either uncommitted case, inspect the actual staged files:

```bash
git status --short
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
git diff --cached -- README.md LICENSE LICENSE_SCOPE.md
```

**Existing GitHub clone with commits or remotes:** do not run the one-time
preparer; run the test command in [`GITHUB_SETUP.md`](GITHUB_SETUP.md) instead.

After **personal review and explicit approval** of the entire staged content,
confirmation of rights and privacy, and clearance of all applicable gates in
[`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md), the publisher may create the
first commit in the **uncommitted** local repository:

```bash
git commit -m "Document unofficial Ardour 7.5 Intel Catalina build"
```

Create a GitHub repository with a matching name, choose **not** to auto-add
another README or license, and follow the remote-setup commands GitHub
displays. At the time this first-publication guide was written, no GitHub account or
repository had been supplied. The actual repository was subsequently created
before Step 169 and first pushed in Step 169 (2026-10-16); these initial-setup commands are
**not** instructions to reinitialize or recreate the existing public repository.

## Repository classification

The **documentation-and-patch repository is public** (Step 169), with its
contents reviewed and approved by the publisher in Step 166 and publicly
verified in Steps 170-172. This completed human approval is distinct from an
**independent legal determination** of ownership or applicable third-party,
employer or co-author rights. See [`COPYRIGHT_REVIEW.md`](COPYRIGHT_REVIEW.md)
and [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) for the historical gates and
remaining conditional checks. The local source SHA and file-level patch match
are recorded, but original clone provenance, cryptographic tag authenticity,
independent rights verification and a clean-machine rebuild are **not** all
established. **Do not describe this as a verified reproducible binary build or
as a cleared binary release.**

## Upstream contribution policy

This package documents an independent local workaround, not an upstream Ardour contribution. Before submitting code or generated patches to the Ardour project, consult its current contributor rules: https://ardour.org/development (which currently restricts LLM-generated code contributions). Do not present independently generated material as an upstream-approved fix.

## Keep binary distribution separate

- Do not add `Ardour7.app`, unsigned or ad-hoc-signed DMGs, source trees, dependency binaries, private logs or cached archives to this documentation repository.
- Complete `RELEASE_CHECKLIST.md` before any GitHub Release containing binaries.
- If a binary is eventually cleared, include exact corresponding source, licenses, a release archive SHA-256 and an explicit unofficial build notice.
