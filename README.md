# Ardour 7.5 on Intel macOS Catalina — Unofficial Build Notes

> **Independent, unofficial community build documentation.** This repository is not affiliated with, endorsed by, or supported by the Ardour project.
>
> **Documentation and patch only. No Ardour executable, `.app`, `.dmg`, third-party binary, or bundled third-party source is published here.**

## What was built

Ardour **7.5.0** was built from source on an **Intel x86_64 MacBook Pro running macOS Catalina 10.15.x**, using **Apple Clang 12.0.0** and a locally built GTK2/Quartz dependency stack. The machine-specific build was finished on **2026-10-14**.

| Check | Result |
| --- | --- |
| Waf configure and full build | Passed |
| CLI version check (`ardev --version`) | Passed |
| Local `Ardour7.app` packaging | Passed |
| Bundle library collection | 63 added dependencies, as reported by the packaging script |
| Rewritten library references | 906, as reported by the packaging script |
| Mach-O validation and ad-hoc signing | 96 Mach-O files checked; signing verified |
| Finder launch and basic GUI input | Passed on the build Mac |
| CoreAudio playback / recording | **Not tested** |
| Running on a different, clean Mac | **Not tested** |
| Third-party license audit for binary redistribution | **Incomplete** |
| Developer ID signing / notarization | **Not done** |

The local app was installed at `~/DTM/ardour-7.5-app/Ardour7.app` **on the build machine only**. That local file is not part of this repository.

## Repository contents

| File or directory | Purpose |
| --- | --- |
| [`BUILD.md`](BUILD.md) | Build environment, dependencies, configure/build commands and limitations |
| [`PATCHES.md`](PATCHES.md) | Explanation and application instructions for the GTK Quartz workaround |
| [`patches/0001-catalina-gtk-quartz-canvas-fallback.patch`](patches/0001-catalina-gtk-quartz-canvas-fallback.patch) | Minimal, machine-tested change to `nsglview.mm` |
| [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md) | Known components and **unverified** license-review items |
| [`inventory/known-components.csv`](inventory/known-components.csv) | Recorded versions, with license review status |
| [`inventory/verified-source-checksums.csv`](inventory/verified-source-checksums.csv) | Checksums checked during the build for four archives |
| [`scripts/audit_bundle.py`](scripts/audit_bundle.py) | Inventories the real `.app` contents on macOS; does **not** make legal determinations |
| [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) | Prerequisites before distributing a binary |
| [`BUILD_RECORD.md`](BUILD_RECORD.md) | Evidence summary and open checks |
| [`SOURCES.md`](SOURCES.md) | Official technical and licensing references |
| [`PUBLISHING.md`](PUBLISHING.md) | Initial publication steps and binary release safeguards |
| [`GITHUB_SETUP.md`](GITHUB_SETUP.md) | Step 161: local staging, authorization gates and optional private GitHub repository setup |
| [`scripts/prepare_git_repository.sh`](scripts/prepare_git_repository.sh) | Text-only Git staging and validation; never commits or pushes |
| [`UPSTREAM_LICENSES/`](UPSTREAM_LICENSES/) | GPL v2 reference copy for Ardour-derived code; **not** the repository documentation license |
| [`LICENSE`](LICENSE) | MIT license for original repository documentation, scripts and tests |
| [`LICENSE_SCOPE.md`](LICENSE_SCOPE.md) | Exact license boundaries and GPL patch exception |
| [`COPYRIGHT_REVIEW.md`](COPYRIGHT_REVIEW.md) | Publisher sign-off checklist for the adopted collective MIT attribution |
| [`SOURCE_IDENTITY.md`](SOURCE_IDENTITY.md) | Verified source commit, patch equivalence, local tag and official mirror comparison |
| [`REVIEW_REPORT.md`](REVIEW_REPORT.md) | Final documentation review, verified checks and remaining blockers |
| [`scripts/record_source_identity.sh`](scripts/record_source_identity.sh) | Read-only source identifier and pristine-patch applicability check |
| [`tests/test_audit_bundle.py`](tests/test_audit_bundle.py) | Unit tests for dependency and symlink classifications |

## Build at a glance

This build used:

- Ardour 7.5.0 source and Waf
- macOS Command Line Tools / Apple Clang 12.0.0 with an explicit `-isysroot`
- Python 3.10.2, Meson 0.62.2, Ninja 1.10.2, CMake 3.20.0, pkg-config 0.29.2
- Boost 1.76.0 headers, GNU gettext 0.21, FFTW 3.3.10 with `--enable-float --enable-threads`
- GTK2/Quartz and the other libraries listed in `BUILD.md`

Read [`BUILD.md`](BUILD.md) before attempting to reproduce the build. **This repository is a record and starting point, not a one-command setup for a clean machine.** The original build checkout was identified as Git HEAD [`e1950ec49e601864f06e316ba8cee730a3964989`](SOURCE_IDENTITY.md), and the published patch was verified against its pristine `nsglview.mm`. The full GTK-stack dependency versions and a clean-machine rebuild are still outstanding.

## The local GTK Quartz workaround

The stock Ardour source contained `#error NO TAG` when `ARDOUR_CANVAS_NSVIEW_TAG` was not supplied by Ardour's patched GTK Quartz stack. On this particular local build, the error was replaced by a comment, while the `0x0` fallback remained. The resulting app launched and responded to basic GUI interactions.

**This is a workaround, not an upstream fix.** OpenGL canvas behavior, AU/VST windows, event delivery and audio work still require further testing. See [`PATCHES.md`](PATCHES.md). Do not assume it is correct for every macOS/GTK combination.

## Source verification and reproducibility limits

**Source verification completed on the build Mac (2026-10-14):** Git HEAD `e1950ec49e601864f06e316ba8cee730a3964989`; local description `7.5-dirty`; the package patch applied to the pristine `HEAD` copy and the result matched the modified local file byte-for-byte. See [`SOURCE_IDENTITY.md`](SOURCE_IDENTITY.md) and [`REVIEW_REPORT.md`](REVIEW_REPORT.md). The build machine verified its configured `origin` URL and compared the `7.5` tag with the official GitHub mirror (all matched). The original clone URL, signed-tag authenticity and a clean-machine rebuild remain **unverified**. **Do not present this package as a turnkey reproducible build.**

The included helper script [`scripts/record_source_identity.sh`](scripts/record_source_identity.sh) can safely inspect the local Git checkout and test the supplied patch against the original file from `HEAD` without altering the working tree.

## Licensing and publication status

Ardour is GPL-covered software. The exact license text and any file-specific exceptions must be verified against the **actual Ardour 7.5 source tree** prior to redistributing its modified executable. Packaging additional libraries, icons, fonts, themes or plugins can introduce additional obligations.

**This documentation-and-patch repository has been public on GitHub since 2026-10-16.** The publisher approved the 24-file contents in Step 166; Step 169 pushed the initial `main` commit; Step 170 verified public anonymous access, the commit, the tracked file list, and the published README, license and patch against the local copies. **No Ardour app or other binary is distributed here.** The publisher adopted the collective MIT attribution in `LICENSE` and self-attested in Step 163 to ownership and MIT licensing authority for the independently prepared materials. This is **not independent proof of legal ownership**, and any applicable third-party, employer or co-author rights must still be respected. [`COPYRIGHT_REVIEW.md`](COPYRIGHT_REVIEW.md), [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) and [`PUBLISHING.md`](PUBLISHING.md) retain *historical pre-publication checks*; their older pending items do not mean this documentation repository is unpublished.

**Binary redistribution remains on hold.** Read [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md) and [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md).

Source patches derived from Ardour must be distributed consistently with Ardour's applicable source license (**GPL-2.0-or-later** for this patch). The attached patch was verified on the build Mac against the exact pristine file extracted from the recorded Git HEAD, and the patched output was identical to the local modified file. This confirms **file-level patch reproducibility**, not a full reproducible build. Original repository documentation, helper scripts, tests and independently prepared inventory data are offered under the **MIT License**, based on the publisher's documented self-attestation (see [`COPYRIGHT_REVIEW.md`](COPYRIGHT_REVIEW.md)). That record does not independently establish third-party or employer rights. The Ardour-derived patch remains **GPL-2.0-or-later** and is excluded from the MIT grant. No rights in upstream code are asserted here.

## Upstream

- Ardour: https://ardour.org/
- macOS build documentation: https://ardour.org/building_osx_native.html
- Source mirror: https://github.com/Ardour/ardour

For issues with this **unofficial** build, do not assume the upstream team supports the local modifications. Reproduce any issue against an official or unmodified Ardour build first.
