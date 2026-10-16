# Documentation review report — 2026-10-14

## Scope

The previously assembled 13-file documentation ZIP was unpacked and reviewed for consistency across the README, Waf build instructions, local patch, recorded source checksums, license matrix, publication process and Python inventory tool. The underlying MacBook Pro application and dependency files were **not available** for direct inspection here.

## Corrections implemented

| Issue | Corrective action | Verification |
| --- | --- | --- |
| Exact source revision unspecified | Added `SOURCE_IDENTITY.md` and a read-only Git source/provenance helper | Shell syntax and fixture tested; no access to original Mac |
| Patch not yet verified against original 7.5 checkout | Made this limitation prominent; helper checks the `HEAD` copy of the affected source file | Patch format and synthetic fixture `git apply --check` passed |
| Bundle audit missed symlinks | Added symlink inventory with outside-app and broken-target checks | Unit tests cover link classification; actual `.app` not audited here |
| Ambiguity of 63 dependencies | Clarified as added library **entries**, not necessarily 63 unique projects | Cross-checked with supplied terminal result |
| Source and license gate ambiguity | Added a GPL v2 upstream reference, and tightened publication checklist and publishing instructions; documentation license remains for owner to choose | Cross-document consistency review |
| Real-world limitations | Explicitly separated GUI success from audio I/O, clean-machine tests and public binary release | Checked against supplied build history |

## Confirmed from supplied local logs

- Waf configure and build completed successfully for Ardour 7.5.0.
- Intel x86_64 `.app` was packaged locally; 63 dependency entries added, 906 install-name references rewritten, 96 Mach-O objects validated and ad-hoc-signed.
- `Ardour7.app` launched through Finder and responded to GUI input on the build machine.
- CoreAudio playback/recording, external plugin GUI behavior and clean-system installs remain untested.

## Step 160-A source verification addendum — 2026-10-14

The builder subsequently executed an isolated, read-only source verification on the original MacBook Pro. The results supersede the earlier **pending** source-identity and patch-applicability items noted above.

- Exact checked-out Git HEAD: `e1950ec49e601864f06e316ba8cee730a3964989`.
- Local Git description: `7.5-dirty`; one tracked-file change reported (`libs/gtkmm2ext/nsglview.mm`).
- Pristine `HEAD` file SHA-256: `ef8e8a7dcf50ae74377a5ffba6d57ef7a6df7e54250498bff9c924ebbcd7898a`.
- Modified local file SHA-256: `188905e362f0a720847a12e94145b975328dd01d6315be441979a9ab7d695cfc`.
- Patch applicability on pristine `HEAD` copy: **PASS**.
- Patched pristine copy compared to actual modified local file: **PASS (byte-for-byte identical)**.
- The temporary patch used in the builder's verification script matches the repository's `.patch` file exactly.
- No build-machine source or build artifacts were modified by the check.

The original 13-file review predates this new evidence; its description of missing source provenance above is historical. The source SHA and patch match are now verified **from builder-supplied output**, not by independently inspecting the Mac or upstream remote.

## Open publication gates

1. Review untracked files and submodules; Step 160-B verified the configured `origin` and official mirror `7.5` tag but did not establish the original clone URL or cryptographic tag authenticity.
2. Select an appropriate license for the **original** documentation and helper scripts; preserve the upstream licensing of modified Ardour source.
3. Review personal/private information, authorship and all material claims before making the repository public.
4. A *binary release* additionally requires a full per-file bundled component/license audit, corresponding source arrangements, clean-machine tests and appropriate macOS signing/notarization decisions.

## Validation performed on the revised package

- Python source compiles successfully.
- Unit tests cover path classification, symlink validation and dependency parsing.
- Bash syntax check passes for the read-only provenance helper.
- A synthetic representation of the four-line guard accepts the provided patch via `git apply --check`.
- ZIP integrity and archive-file consistency are checked after creation.

These are **local documentation package tests**. Step 160-A additionally tested the included patch against the exact Git `HEAD` file from the builder's Mac. The later Step 160-B check separately compared the build-machine remote and official GitHub mirror `7.5` tag. None of these checks establishes a clean-room rebuild or cryptographic tag authenticity.

## Step 160-B Git remote and tag provenance addendum — 2026-10-14

The builder ran a read-only Git provenance check against the original MacBook Pro checkout and supplied the terminal results:

| Observation | Result |
| --- | --- |
| Git HEAD | `e1950ec49e601864f06e316ba8cee730a3964989` |
| Local tag `7.5` | Same commit as HEAD (**PASS**) |
| Configured remote `origin` | `https://github.com/Ardour/ardour.git` |
| Public GitHub mirror tag `7.5` (`git ls-remote`) | Same commit as HEAD (**PASS**) |
| Tracked-file modification | `libs/gtkmm2ext/nsglview.mm` only |
| Script exit code | `0` |
| Local repository mutations | None |

**Result:** The previously open *configured remote URL / official tag comparison* check is closed. We rely on builder-supplied terminal output rather than independent access to the original Mac. Original clone URL, cryptographic tag signature, untracked files and submodules were not verified. This does not change the incomplete third-party redistribution audit or clean-machine build status.

## Step 160-C license selection addendum — 2026-10-14

The publication package now contains a root `LICENSE` (MIT) and `LICENSE_SCOPE.md`, documenting the boundaries between independently prepared materials and Ardour-derived content. The original notes, helper scripts, tests and independently prepared inventory records use **MIT**. The verified `nsglview.mm` patch retains **GPL-2.0-or-later**. The GPL v2 reference text is unchanged, and the patch bytes and successful SHA-256 evidence remain unchanged.

**Still required before a public commit:** the publisher must confirm rights-holder authorization for the original content, and the accuracy of the collective MIT copyright attribution, as well as review the staged files for privacy and secrets. The previous review sections above are retained as historical notes from before a license was selected. This license selection **does not clear any binary release** or establish the rights in included third-party source material.

## Step 160-D attribution review — 2026-10-14

The source package was inspected to determine whether the collective notice in the root MIT `LICENSE` identifies verified copyright holders. The available build and Git evidence proves source commit/tag identity and patch correspondence, **not who owns the newly prepared documentation, helper scripts, tests or inventory**. The collective notice was therefore **retained provisionally**, without claiming that its factual accuracy or rights-holder permission was independently confirmed.

- Added [`COPYRIGHT_REVIEW.md`](COPYRIGHT_REVIEW.md) with alternative ownership scenarios and a human sign-off checklist.
- Clarified the provisional attribution and publication blocker in the README, `LICENSE_SCOPE.md`, publishing instructions and release checklist.
- Kept Ardour's GPL-2.0-or-later-derived patch byte-for-byte unchanged; root MIT applies only to independent original work.
- Verified that the release archive excludes Python bytecode/caches and binary/application artifacts.
- **Status:** documentation and tooling are prepared for publisher sign-off; public GitHub publication and binary distribution are **not yet authorized/complete**.


## Step 160-E collective attribution adoption — 2026-10-14

The publisher selected option 1 to **formally adopt** the existing collective copyright notice: `Copyright (c) 2026 Contributors to the Ardour 7.5 Catalina Build Notes`. The unchanged notice is present in the root MIT `LICENSE`. Accordingly, documentation referring to this wording as *provisional* has been updated to describe it as **publisher-selected**. The division between MIT for original repository materials and GPL-2.0-or-later for the Ardour-derived patch is unchanged.

**Important scope:** Selecting the collective name is a publication/attribution decision, not independent verification that every original contributor is identified and has authorized the MIT grant. A separate rights-holder sign-off and final staged-file/privacy review remain required before making the repository public. This update does not authorize redistribution of the compiled app. All prior review findings remain as dated historical observations.


## Step 161 GitHub publication preparation — 2026-10-14

A text-only repository preparation script and GitHub setup guide were added.
The preparer validates an explicit allowlist, checks typical binary and secret
indicators, runs the bundled unit tests, initializes local branch `main` and
stages files without committing or uploading. **It does not establish permission
to publish**, nor does it claim GitHub repository creation. The publisher's rights
and staged-content sign-off remain mandatory before a first public commit.


## Step 161-A macOS canonical-path regression correction — 2026-10-14

The builder reported two test failures while running the Step 161 repository
preparation script on an Intel MacBook Pro running macOS Catalina:
`test_executable_relative` was misclassified as `EXTERNAL-REFERENCE`, and
`test_symlink_aliased_library` as `ESCAPES-APP`. The preparation stopped before
Git initialization and did not touch the Ardour build.

**Cause:** `inside()` resolved the dependency or symlink target but compared it
with a potentially non-canonical `app` directory. On macOS, an alias such as
`/var` pointing to `/private/var` can make paths to the same bundle appear
lexically different.

**Correction:** Canonicalize both operands using `Path.resolve(strict=False)`
before testing whether a path is equal to, or nested inside, the app directory.
Added two regression tests that reproduce both faulty classifications with a
symlinked parent directory. The original tests plus both regression tests pass
(11/11) in the packaging environment. A fresh run on the original Mac is still
required to confirm the Catalina result. The fix does not change the Ardour
source, the published patch, or the app binary. No license clearance or public
release is implied by the test result.


## Step 161-B original-Mac regression verification and package synchronization — 2026-10-15

The earlier Step 161-A statement that the corrected path-classification tests
still required an original-Mac rerun is **superseded by the subsequent
builder-supplied terminal output**. The failed original Catalina test run
remains documented above as historical evidence; it was not erased.

After applying the canonical-path correction, the builder reran Step 161
on the original Intel MacBook Pro. All **11 of 11 Python unit tests passed**,
including both symlinked-parent regression tests, and Git successfully
staged the 24 documentation-only files. Step 161-B then synchronized four
changed files with the reviewed 161-A package and reran the checks.

| Original-Mac observation | Reported result |
| --- | --- |
| Step 161-A regression suite after correction | **11/11 PASS** |
| Step 161-B package synchronization | **PASS** |
| Full 24-file SHA-256 manifest comparison to 161-A | **PASS** |
| Step 161-B regression suite | **11/11 PASS** |
| Local initial Git branch and staged text files | `main`, 24 files |
| Git commit, remote, or upload | None |
| Step 161-B exit code | `0` |

The manifest SHA-256 validated on the builder's Mac was:
`4d80809eada07480652a613ce3008e2827bc4d1a99f8e62593857c422b072d8b`.
That manifest identifies the **161-A version before this documentation addendum**.
This updated review report requires a new staged manifest and must not
be represented as identical to the original 161-A package.

These results confirm the targeted unit tests and exact file synchronization
reported by the builder. They do **not** establish CoreAudio functionality,
a clean-system rebuild, a complete binary-license audit, or publication
authorization. The original Mac's Git state was independently preserved
without any commit, remote, or upload.

## Step 162 publication audit follow-up — 2026-10-15

A separate documentation-package audit inspected the reviewed 24-file ZIP
and the publisher's Step 161-B evidence. Targeted binary and sensitive-data
scans, license-scope consistency checks, Markdown link validation, Bash
syntax checks, and 11 unit tests passed in the audit environment. These
automated findings are **limited in scope** and cannot prove the absence of
all sensitive material or third-party rights issues.

**Public publication remains on hold.** The actual copyright owner(s)'
authority to grant MIT rights for independently prepared materials and the
publisher's final human review of all staged contents still require explicit
confirmation. The Ardour-derived patch continues to be treated separately
under the upstream GPL-2.0-or-later terms. The compiled `.app` is not
authorized or included for redistribution.

This Step 162-A report amendment closes the obsolete *Mac unit-test
rerun pending* note only; it does **not** close the copyright, privacy, or
binary-distribution gates.

## Step 163 publisher copyright self-attestation — 2026-10-15

The publisher selected Step 163 option 1, affirming ownership of and authority
to apply MIT to the **independently prepared** README, build documentation,
helper scripts, tests, and original inventory records. The selected collective
attribution from Step 160-E is retained as the publisher-approved public credit.

This is a **publisher statement, not independently verified legal ownership**.
It does not relicense the Ardour-derived GPL patch or any third-party content
and cannot substitute for actual collaborator, employer or contractual
permissions if those apply. Prior dated sections above record the state at
the time of those reviews and remain part of the audit trail.

**Remaining:** Manually review all exact staged text for confidentiality,
misleading statements, and third-party material; resolve applicable third-party
rights; explicitly approve intended public visibility. The compiled `.app`
remains out of scope. No commit, Git remote or push was made in this step.

## Step 164-A targeted final-content corrections — 2026-10-16

The Step 164 review identified five issues in the proposed initial GitHub
content. The following corrections were made without altering Ardour's
upstream-derived patch, license texts, component inventories, or build source:

| Finding | Resolution | Affected file |
| --- | --- | --- |
| F164-01: hard-coded unpacked directory name | The first-time preparer now relies on the exact 24-file allowlist and Git/source guards rather than a historical folder basename. | `scripts/prepare_git_repository.sh` |
| F164-02: outdated ZIP instructions | Fresh package, original staged Mac repository, and already-committed clone instructions are now explicitly separate. | `GITHUB_SETUP.md` |
| F164-03: nested Markdown emphasis | Rewrote the licensing paragraph with separate emphasis and preserved the self-attestation caveat. | `README.md` |
| F164-04: stale pending-authorization message | The preparer now reports the Step 163 publisher self-attestation while retaining third-party/organization-rights and human review gates. | `scripts/prepare_git_repository.sh` |
| F164-05: unnecessary `git init` instruction | Publishing instructions now use the first-time preparer only for fresh packages and skip reinitialization on the already staged original Mac. | `PUBLISHING.md` |

The prior Step 161/163 failure/success records above remain historical evidence.
This addendum does not independently establish all rights, a complete secret
scan, permission for public GitHub visibility, or binary redistribution.
**Publisher approval of the exact final staged contents is still required.**

## Step 165-A final approval review corrections — 2026-10-16

The Step 165 content review found three defects. They were corrected in this
independent documentation package, without changing the original Ardour 7.5
source checkout, original GTK fallback patch, or compiled application:

| Finding | Correction | Evidence |
| --- | --- | --- |
| R165-01: FFTW thread API overclaim | `BUILD.md` now describes the successful link/build and explicitly states dedicated thread-API runtime behavior was **not** tested. | Build history and scope review |
| R165-02: outdated ownership prerequisite | `BUILD_RECORD.md` preserves the Step 160-C historical position, records the Step 163 self-attestation, and retains actual third-party and human-approval gates. | Copyright decision sequence |
| R165-03: source helper printed FAIL but exited 0 | `scripts/record_source_identity.sh` now uses distinct exit statuses for exact-patch PASS (0), pristine/NOT YET APPLIED (3), unexpected differences or patch mismatch (1), and invalid prerequisites (2). | Four isolated Git regression tests added to `tests/test_audit_bundle.py` |

The helper's isolated source comparison remains **read-only** with respect to
the original Ardour checkout; the patch is applied to a temporary HEAD copy.
Passing these regression tests does **not** amount to a full Ardour rebuild,
CoreAudio verification, binary redistribution clearance, or final public
publication approval. The exact staged package must still be examined and
approved by the publisher before a public commit.
