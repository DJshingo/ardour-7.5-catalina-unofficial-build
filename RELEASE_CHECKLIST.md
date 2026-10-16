# Release gates

**Current status (2026-10-16): The 24-file documentation/patch repository is
PUBLIC (Steps 169-172). Binary release is NOT cleared.**

The checkboxes in section A originated as **pre-publication gates**. Subsequent
publisher approval and public verification are recorded below; a remaining
conditional rights check must not be mistaken for an assertion that the
repository is still unpublished.

## A. Documentation-only repository

- [x] Write English README, build notes and technical limitations.
- [x] Describe the machine-tested source modification and supply a patch.
- [x] Include a GPL-2.0 reference text for the Ardour-derived source patch; retain original source notices separately.
- [x] Record observed library versions and known checksums.
- [x] Explain that bundled libraries, fonts, themes, icons and plugins require separate review.
- [x] Exclude `.app`, `.dmg`, `.zip` binaries, build trees and private logs from the repository package.
- [x] Select **MIT** for original documentation, scripts, tests and original inventory records; add root `LICENSE` and `LICENSE_SCOPE.md`.
- [x] Explicitly exclude the GPL-2.0-or-later Ardour-derived patch from the MIT scope.
- [x] Adopt the collective MIT copyright notice `Copyright (c) 2026 Contributors to the Ardour 7.5 Catalina Build Notes` and match it in `LICENSE_SCOPE.md` (publisher selection, Step 160-E).
- [x] **Publisher declaration recorded (Step 163, 2026-10-15):** publisher states they own and may MIT-license their independently prepared content; collective attribution retained. This is self-attestation, not independent legal verification; see [`COPYRIGHT_REVIEW.md`](COPYRIGHT_REVIEW.md).
- [x] **Publisher approval of public text:** the exact initial 24-file staged package was explicitly approved in Step 166; first publication completed in Step 169 and public tree/content was verified in Step 170. This approval is not independent legal proof.
- [ ] **Conditional third-party rights:** independent verification of any applicable employer, co-author, client or third-party restrictions has not been established. If relevant rights issues arise, correct/remove affected public material and obtain permissions as required.
- [x] Record exact local Ardour Git `HEAD` and both pristine and patched source-file SHA-256 values (see `SOURCE_IDENTITY.md`).
- [x] Verify patch applicability to the exact pristine `HEAD` file and byte-for-byte equivalence of the patched copy to the local modified file.
- [x] Record configured `origin` and compare the local `7.5` tag with the official GitHub mirror tag (Step 160-B: matching commit).
- [ ] Review untracked files/submodules and avoid claiming the original clone URL or signed-tag authenticity is verified.
- [x] **Initial-package content/privacy review:** publisher-approved 24-file
  staged text (Step 166), technical file/secret-indicator checks, and publicly
  retrievable content verification (Step 170). The checks are limited; they do
  not establish absence of every possible sensitive item.
- [ ] **Independent or ongoing privacy/rights assurance:** if new information
  reveals a secret, personal identifier, or material without publication
  authority, investigate and remediate the public Git history as appropriate.
  See `GITHUB_SETUP.md`; the Step 161 preparer performed heuristic checks only.

## B. Prerequisites to distribute compiled `.app`, ZIP or DMG

- [ ] Generate and review the **actual** file inventory from the completed `.app`, including symlinks and alias target validation.
- [ ] Trace all 63 **added library entries** to actual filenames, unique component owners, versions and source origins; identify other embedded resources and modules.
- [ ] Audit exact third-party licenses, notices, copyright, patents or redistribution restrictions as applicable.
- [ ] Add complete and corresponding source for Ardour and applicable redistributed dependencies, including patches and scripts.
- [ ] Include copyright notices and license texts with the release in an appropriate form.
- [ ] Ensure no dependency or resource points into the original builder's home directory.
- [ ] Reproduce the app build from a clean documented source snapshot.
- [ ] Test clean Intel Mac install, application start and permissions.
- [ ] Test GUI events, session creation, CoreAudio playback and recording.
- [ ] Test relevant AU/VST3/LV2 plugin UI operation and audio processing.
- [ ] Assess graphics workaround behavior (prefer supported patched GTK when possible).
- [ ] Complete Developer ID signature and Apple notarization for standard consumer distribution, if proceeding with that distribution route.
- [ ] Produce release asset archive, SHA-256 digest, provenance and full changelog.
- [ ] State clearly **unofficial build**, x86_64, target OS, limitations and absence of upstream support.

## C. GitHub repository and binary placement

- Put text, patches and scripts in Git, **not** compiled app trees or captured GTK SDKs.
- GitHub generally blocks Git-tracked files above 100 MiB.
- For any future approved binary, GitHub Releases has a per-asset limit of under 2 GiB.
- GitHub Releases can host binaries, but the hosting platform does not remove license and security obligations.

Official references: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github , https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases , https://developer.apple.com/developer-id/ .

## D. Published documentation status (2026-10-16)

| Verification | Evidence | Status |
| --- | --- | --- |
| Publisher-approved initial package | Step 166; 24 files | Complete (publisher decision) |
| Public `main` and 24-file tree | Steps 169-170, remote and anonymous API checks | Verified from builder logs |
| Updated README | Step 171-A, commit `8dd0d74285e2beadd6879665ca177daa82110ab8` | Published and checked |
| Description, website and eight Topics | Step 172 public API checks | Complete |
| Third-party and employer rights | No independent confirmation represented | Conditional / not independently cleared |
| Compiled `.app`, ZIP or DMG distribution | Section B | **Not cleared** |

This table is a **later status update**, not a retroactive claim that every
pre-publication checkbox had been proven by automated tests. The original
source-checkout provenance and all binary-distribution gates remain limited
as described above.
