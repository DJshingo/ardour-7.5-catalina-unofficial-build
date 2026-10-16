# Release gates

**Current status: DOCUMENTATION/PATCH PACKAGE ONLY. Binary release is NOT cleared.**

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
- [ ] **Remaining rights/content gate:** resolve any actual third-party, employer or co-author rights where applicable; manually review and explicitly approve all staged text before public publication.
- [x] Record exact local Ardour Git `HEAD` and both pristine and patched source-file SHA-256 values (see `SOURCE_IDENTITY.md`).
- [x] Verify patch applicability to the exact pristine `HEAD` file and byte-for-byte equivalence of the patched copy to the local modified file.
- [x] Record configured `origin` and compare the local `7.5` tag with the official GitHub mirror tag (Step 160-B: matching commit).
- [ ] Review untracked files/submodules and avoid claiming the original clone URL or signed-tag authenticity is verified.
- [ ] Remove repository secrets and machine-specific identifiers; review `git diff --cached` before committing. See `GITHUB_SETUP.md`; the Step 161 preparer only performs heuristic text checks and local staging.

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
