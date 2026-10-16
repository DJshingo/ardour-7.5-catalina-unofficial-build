# Local build record (2026-10-14)

## Completed

- **Target:** Intel x86_64 MacBook Pro, macOS Catalina 10.15.x.
- **Ardour:** built from 7.5 source, executable reports `Ardour7.5.0`.
- **Compiler:** Apple Clang 12.0.0 (`clang-1200.0.32.29`).
- **Source-level modification:** `libs/gtkmm2ext/nsglview.mm` compile guard; see `PATCHES.md`.
- **Build:** Waf `build` finished successfully, code 0.
- **Local app:** `Ardour7.app` bundle completed; executable x86_64; ad-hoc codesign verification passed.
- **Packaging output recorded:** 63 additional dependency library entries (not 63 confirmed unique third-party projects) added, 906 dependency references adjusted, 96 Mach-O files checked/signed.
- **GUI:** Finder launch and basic operation confirmed by the builder.

## Important limitations

- CoreAudio playback and recording **not tested**.
- No full track/session/plugin test matrix.
- Not tested on a second clean Mac.
- Not Developer ID signed and not notarized.
- Exact Ardour source Git HEAD **recorded**: `e1950ec49e601864f06e316ba8cee730a3964989` (`7.5-dirty`); file-level patch application and comparison verified. Configured `origin` and official GitHub mirror tag `7.5` both verified by the builder in Step 160-B; original clone URL and tag-signature authenticity not verified.
- Full dependency list, source provenance and license review for the 63 bundled libraries **not completed**.
- Repository does **not** include the user’s original private build logs or compiled software.

## Source and patch evidence collected on 2026-10-14

- Original Git HEAD: `e1950ec49e601864f06e316ba8cee730a3964989`.
- `git describe`: `7.5-dirty`; recorded tracked-file modification: `libs/gtkmm2ext/nsglview.mm`.
- Original file SHA-256: `ef8e8a7dcf50ae74377a5ffba6d57ef7a6df7e54250498bff9c924ebbcd7898a`.
- Patched file SHA-256: `188905e362f0a720847a12e94145b975328dd01d6315be441979a9ab7d695cfc`.
- An isolated pristine file reconstructed using `git show HEAD:libs/gtkmm2ext/nsglview.mm` accepted the repository patch, and the result matched the locally modified file byte-for-byte.
- These checks identify the local checkout and single source edit; Step 160-B subsequently confirmed the configured remote and mirror `7.5` reference. Neither step establishes end-to-end clean-machine reproducibility, original clone provenance or signed-tag authenticity.

## Step 160-B remote provenance evidence (2026-10-14)

- Build-machine `origin`: `https://github.com/Ardour/ardour.git` (official GitHub mirror).
- Local `HEAD`: `e1950ec49e601864f06e316ba8cee730a3964989`.
- Local `refs/tags/7.5^{commit}`: same commit (**PASS**).
- Public mirror `refs/tags/7.5` / dereferenced tag: same commit (**PASS**).
- Git operation scope: read-only; no fetch, checkout, pull or push.
- Caveat: the check does not certify the clone URL originally used or any tag signature.

See [`SOURCE_IDENTITY.md`](SOURCE_IDENTITY.md).

## Key problem/solution history

| Failure | Confirmed corrective action |
| --- | --- |
| `<cmath>` / C system header errors | Explicit macOS SDK with `-isysroot`; preserve flags via Waf `--keepflags` |
| Missing `libintl.h` | Use prebuilt GNU gettext 0.21 include/lib paths from independent prefix |
| Link error for `-lfftw3f_threads` | Build thread-enabled FFTW 3.3.10 single precision; stage and add thread library only |
| `nsglview.mm: error: NO TAG` | Locally comment out compile guard; retain fallback; basic GUI testing passed |
| `.app` dependency collector called valid symlinked dylibs “not Mach-O” | Resolve symlink target for inspection, preserve requested alias during copy |
| Bundled `--version` falsely marked failed | Use exit status and account for Ardour's stdout/stderr redirection to user logs |

## Recorded checksums

The local builder reported successful verification of archive digests for Sratom, Lilv, Ogg and FLAC. Values are in `inventory/verified-source-checksums.csv`. These do **not** attest to the remainder of the dependency stack.

## Privacy

The original logs contained a local macOS username and absolute home-directory paths. Public files generalize these paths to `$HOME` and do not include the original log contents.

## Step 160-C documentation repository license decision

- Original English documentation, helper scripts, tests and independently prepared inventory metadata: **MIT**; see `LICENSE` and `LICENSE_SCOPE.md`.
- Ardour-derived and byte-for-byte verified GTK Quartz patch: **GPL-2.0-or-later**, retaining upstream terms; the patch itself has not been modified.
- **Historical context:** At Step 160-C, ownership and MIT authority had not
yet been affirmed; Step 160-E adopted the collective attribution, and Step 163
recorded the publisher's **self-attestation** for independently prepared
material (see `COPYRIGHT_REVIEW.md`). Step 166 subsequently approved the exact
24-file public text/patch package, and Steps 169-172 confirmed its publication
and metadata. **Staged-file approval is no longer pending.** The declaration
is not independent legal verification; applicable third-party, employer or
client rights (if any) still require proper treatment.
- The license selection does not authorize public redistribution of the Mac `.app` or any compiled third-party dependencies.

## Documentation repository publication addendum — 2026-10-16

- **Step 166:** publisher authorized the reviewed 24 text/patch files for public
  GitHub publication (not distribution of the compiled application).
- **Step 169:** initial `main` commit
  `e0f7b2e8e740a62153b3e8a48a039c530f05728a` pushed to the public
  repository.
- **Step 170:** anonymous HTTP 200, Public repository setting, `main` SHA,
  24-file paths, and README/license/patch contents were verified.
- **Step 171-A:** README publication-status wording corrected and pushed;
  `main` advanced to `8dd0d74285e2beadd6879665ca177daa82110ab8`.
- **Step 172:** Description, blank Website, eight Topics, and unchanged
  `main` SHA checked through the public GitHub API.

These observations are based on the builder's successful terminal logs.
They do not extend to CoreAudio playback/recording, a clean-machine rebuild,
independent rights-holder verification, or permission to distribute binaries.
