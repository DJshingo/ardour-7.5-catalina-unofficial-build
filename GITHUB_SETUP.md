# GitHub repository preparation — first-time setup and subsequent checks

This guide prepares a **documentation-and-patch-only** local Git repository for an
unofficial Ardour 7.5 Intel macOS Catalina build. It does not distribute the
application, its GTK build, bundled dependencies, DMG, or private machine logs.

**Historical setup guide — publication completed 2026-10-16.** Steps 166 and
169-172 document the publisher's approval, public GitHub push,
post-publication README update, and metadata confirmation. The existing
repository is Public at
[`DJshingo/ardour-7.5-catalina-unofficial-build`](https://github.com/DJshingo/ardour-7.5-catalina-unofficial-build).
The initial *Private* repository option below was only a recommendation; do
not infer that this was the actual creation method, and do **not** rerun
initialization/creation commands in the existing repository.

**Suggested repository:** `ardour-7.5-catalina-unofficial-build`
**Initial branch:** `main`
**Historical first-time recommendation (not the current setting):** **Private**

## Prerequisites

- Use a reviewed documentation-only package (Step 164-A or later), or an existing checkout of this repository. The directory name may differ from the historical build-machine staging folder. **Never** run the preparer in the original Ardour source checkout.
- Use `git` and Python 3 on the target Mac; do not assume `gh` (GitHub CLI) is installed.
- Read [`COPYRIGHT_REVIEW.md`](COPYRIGHT_REVIEW.md). The publisher selected the
  collective MIT notice and **self-attested to ownership and MIT authority in
  Step 163**. This has not been independently verified. The exact initial
  staged text/patch package was subsequently approved in Step 166 and published
  in Steps 169-170; **publication approval is not pending**. Any applicable
  third-party, employer or co-author rights remain subject to review.
- This is a record of the successful local build, **not** a reproducible one-command build or a binary release.

## Catalina path handling — Step 161-A

The bundle-audit helper now normalizes both sides of internal/external path
comparisons; on macOS, the temporary-file directory may appear as both `/var`
and `/private/var`. Two symlinked-parent regression tests accompany the fix.
The Step 161 failure and Step 161-B successful original-Mac rerun are
preserved in [`REVIEW_REPORT.md`](REVIEW_REPORT.md). Current packages include
the corrected path comparisons, plus four Step 165-A source verification tests (**15 tests total**).

## 1. First-time local staging (uncommitted package only)

In a **fresh, reviewed text-only package**, or an existing **uncommitted**
`main` repository with **no Git remotes**, run:

```bash
bash scripts/prepare_git_repository.sh
```

The preparer accepts different directory names, but requires the exact
24-file allowlist, no Ardour source-tree markers, no prior Git commits, and
no Git remotes. It checks for common secret/binary indicators, runs 15 unit
tests, initializes branch `main` only when needed, and stages the files.
**It refuses an already-committed clone or a repository with remotes.** It
never commits, contacts GitHub, or pushes. Automated checks are not a legal
or confidentiality review.

If the **original build Mac** already has an uncommitted `main` repository
with the 24 files staged (Step 163-B), do **not** repeat `git init` or replace
that checkout. Verify and stage only the specific reviewed updates, then
inspect the complete staged contents.

```bash
git status --short
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
git diff --cached -- README.md LICENSE LICENSE_SCOPE.md
```

For an **existing clone with commits or a remote**, do not run the preparer.
To check the included auditor tests without changing Git history:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v
bash -n scripts/prepare_git_repository.sh scripts/record_source_identity.sh
```

Review all staged content, especially licensing, copyright notices, third-party
rights, and the exclusion of upstream code from the root MIT grant.

## 2. Publication gates — do not bypass

Before sharing this repository, the owner/publisher must personally confirm:

1. The Step 163 publisher ownership/MIT-authorization declaration still holds;
   correct the collective attribution or seek further permission if another
   person, employer, or organization has any relevant rights.
2. All staged files are suitable for public view, with no credentials, private logs,
   personal information, unintended binaries, or third-party content lacking rights.
3. The modified Ardour source patch is kept separately under the original GPL terms.
4. Third-party binary distribution is **not** cleared and `Ardour7.app` is not included.

See [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) and
[`COPYRIGHT_REVIEW.md`](COPYRIGHT_REVIEW.md). **Do not mark these checked purely
because an automated script passed.**

## 3. Create the initial Git commit — only after the gates are satisfied

Once the owner has explicitly signed off on the staged contents and attribution:

```bash
git commit -m "Document unofficial Ardour 7.5 Catalina build"
```

If Git requires author configuration, set the identity you **actually wish to
publish** using normal Git settings; do not commit credentials.

## 4. Historical option: create a private GitHub repository (first setup only)

If GitHub CLI is already installed and authenticated:

```bash
gh repo create ardour-7.5-catalina-unofficial-build --private --source=. --remote=origin
```

This does **not** include `--push`. After confirming repository ownership,
privacy and the intended initial commit, you can push separately:

```bash
git push -u origin main
```

If `gh` is not available, use the GitHub web UI to create an empty **private**
repository without auto-adding a README, `.gitignore` or license, and then use
the remote URL displayed by GitHub (`git remote add origin <URL>` followed by
`git push -u origin main`). Do not claim any remote repository exists until
GitHub has confirmed its creation.

## 5. Historical option: switch to Public after approval

Review the GitHub Settings → General → Danger Zone visibility controls; do not
change to Public until all documentation/publication checks are signed off.
Publishing source documentation does **not** clear a downloadable `.app` release.

## Reference

- [GitHub: Add locally hosted code](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)
- [GitHub CLI: gh repo create](https://cli.github.com/manual/gh_repo_create)
