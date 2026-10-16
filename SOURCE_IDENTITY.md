# Verified Ardour 7.5 source identity — local build

**Status: LOCAL SOURCE AND OFFICIAL GITHUB MIRROR TAG VERIFIED FROM BUILD-MACHINE GIT OUTPUT (2026-10-14).** Step 160-A verified the local source file and patch. Step 160-B verified the local tag, configured remote URL, and the public GitHub mirror's `7.5` tag with read-only Git commands. The results below are **builder-supplied terminal evidence**, not a separate inspection of the Mac or a verification of cryptographic tag signatures.

## Recorded evidence

| Field | Verified observation |
| --- | --- |
| Source type | Git checkout; source directory was the Git repository root |
| Git `HEAD` commit | `e1950ec49e601864f06e316ba8cee730a3964989` |
| Local `git describe --tags --always --dirty` | `7.5-dirty` |
| Tracked-file changes (`git status --short --untracked-files=no`) | ` M libs/gtkmm2ext/nsglview.mm` |
| Pristine `HEAD:libs/gtkmm2ext/nsglview.mm` SHA-256 | `ef8e8a7dcf50ae74377a5ffba6d57ef7a6df7e54250498bff9c924ebbcd7898a` |
| Modified local `nsglview.mm` SHA-256 | `188905e362f0a720847a12e94145b975328dd01d6315be441979a9ab7d695cfc` |
| Patch `git apply --check` on isolated pristine `HEAD` copy | **PASS** |
| Patched pristine copy vs. local modified file (`cmp -s`) | **PASS: byte-for-byte identical** |
| Patched copy SHA-256 matches build record | **PASS** |
| Verification script exit code | `0` |
| Direct source/build modification by verification | None |
| Local `7.5` tag dereferenced to commit | `e1950ec49e601864f06e316ba8cee730a3964989` (**PASS: same as HEAD**) |
| Tags pointing at `HEAD` | `7.5` |
| Configured `origin` URL (credentials redacted) | `https://github.com/Ardour/ardour.git` |
| Remote type | Official Ardour GitHub mirror |
| Public mirror `refs/tags/7.5` resolved to commit | `e1950ec49e601864f06e316ba8cee730a3964989` (**PASS: same as HEAD**) |
| Step 160-B exit code | `0` |
| Git fetch / checkout / pull / push by verification | None |

The file patch used in the Step 160-A verification was byte-for-byte identical to [`patches/0001-catalina-gtk-quartz-canvas-fallback.patch`](patches/0001-catalina-gtk-quartz-canvas-fallback.patch) in this package. The working tree is intentionally **dirty** because the build uses the local GTK Quartz workaround. A dirty description does **not** change the underlying immutable Git `HEAD` commit.

**Scope of the tracked change audit:** both checks reported one tracked-file modification. Untracked files were **not included**, and neither check established submodule provenance. `7.5-dirty` describes the working-tree modification and does not change the `HEAD` commit.

## Step 160-B: official mirror tag comparison

The following observations were captured by the builder on **2026-10-14**:

```text
HEAD:                    e1950ec49e601864f06e316ba8cee730a3964989
Local tag 7.5 commit:    e1950ec49e601864f06e316ba8cee730a3964989
Configured origin:       https://github.com/Ardour/ardour.git
GitHub mirror tag 7.5:  e1950ec49e601864f06e316ba8cee730a3964989
All comparisons:         PASS
```

The online comparison used Git `ls-remote` against the public mirror; it did **not** fetch or change the local checkout. The configured remote and matching tag strongly substantiate the source's association with the official Ardour 7.5 mirror, but a configured remote does **not** prove which URL was originally used to clone the checkout. A matching Git tag object/reference is not proof of a cryptographically authenticated signed tag.

Recheck against the public mirror from a machine with Git/network access:

```bash
ARDOUR_SRC="$HOME/DTM/ardour-src/ardour-7.5"
git -C "$ARDOUR_SRC" rev-parse HEAD
git -C "$ARDOUR_SRC" rev-parse 'refs/tags/7.5^{commit}'
git ls-remote --tags https://github.com/Ardour/ardour.git \
  'refs/tags/7.5' 'refs/tags/7.5^{}'
```

## Local verification and repeat checks

From a copy of this documentation repository on the original Mac:

```bash
bash scripts/record_source_identity.sh "$HOME/DTM/ardour-src/ardour-7.5"
```

The helper does not edit the checkout. It extracts the pristine file from Git `HEAD` into an isolated temporary directory, checks and applies this repository's patch **to that temporary copy only**, compares the result with the local file, and prints source fingerprints and tracked-file status. The exit status is meaningful: **0** means the local file matches the patched HEAD exactly; **3** means the patch is **NOT YET APPLIED** (local file is pristine); **1** means the patch context is incompatible or the local file differs unexpectedly; **2** means prerequisites or inputs are invalid. Only exit **0** establishes the expected local patch state. Refer to [`PATCHES.md`](PATCHES.md) before applying the patch to any other checkout.

## Still unverified / incomplete

- **Original clone source:** the configured `origin` and upstream mirror tag match were verified from builder-supplied Step 160-B output. The originally used `git clone` URL was not independently established; a remote may be changed after cloning.
- **Cryptographic tag authenticity:** local and remote `7.5` references matched the exact commit; no signed-tag/GPG authenticity check was performed.
- **Untracked source files, submodule changes and dependency sources:** the reported tracked-file audit does not comprehensively cover these.
- **Reproducible complete build:** this patch was reproduced at **file level**; Ardour and its GTK/toolchain dependencies were **not** rebuilt on a clean independent Mac from these documents.
- **Binary redistribution audit:** licenses, copyright notices, corresponding sources, clean-target testing, and signing/notarization remain open.

Do not publish the raw Step 160-A or 160-B logs: it contains a macOS account name and private filesystem paths. The factual SHA values and tracked source path shown here are the sanitized evidence record.

## Patch license identity (Step 160-C)

The byte-for-byte verified patch at [`patches/0001-catalina-gtk-quartz-canvas-fallback.patch`](patches/0001-catalina-gtk-quartz-canvas-fallback.patch) remains subject to upstream Ardour source license terms (**GPL-2.0-or-later**) and is expressly excluded from the independent-documentation MIT license. The source commit, pristine/modified SHA-256 values and patch bytes were not changed. See [`LICENSE_SCOPE.md`](LICENSE_SCOPE.md).
