# Publishing the documentation repository on GitHub

This is a **documentation-and-patch** repository. It contains **no app binary or third-party libraries**.

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
displays. No GitHub account or destination has been supplied and no repository
has been created by this project.

## Repository classification

This is **ready for owner review**. The local source SHA and file-level patch provenance are recorded, but upstream tag matching is verified from builder-supplied Git output, while original clone provenance, independent rights-holder verification and complete build reproducibility have **not** all been established. The MIT license, collective attribution, and the publisher's Step 163 **self-attestation** are documented, but third-party rights if applicable and the final human staged-content approval have not been independently established; see [`COPYRIGHT_REVIEW.md`](COPYRIGHT_REVIEW.md). Do not label it as a verified reproducible binary build. Complete the open documentation-only checks in `RELEASE_CHECKLIST.md` before publishing.

## Upstream contribution policy

This package documents an independent local workaround, not an upstream Ardour contribution. Before submitting code or generated patches to the Ardour project, consult its current contributor rules: https://ardour.org/development (which currently restricts LLM-generated code contributions). Do not present independently generated material as an upstream-approved fix.

## Keep binary distribution separate

- Do not add `Ardour7.app`, unsigned or ad-hoc-signed DMGs, source trees, dependency binaries, private logs or cached archives to this documentation repository.
- Complete `RELEASE_CHECKLIST.md` before any GitHub Release containing binaries.
- If a binary is eventually cleared, include exact corresponding source, licenses, a release archive SHA-256 and an explicit unofficial build notice.
