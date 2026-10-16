# Reproducing the Intel macOS Catalina build

**Evidence level:** commands below reflect the successful local build and successful subsequent fixes on one Intel Mac. They are **not yet a fully automated, clean-room recipe**. Build the dependency stack independently before running Ardour's Waf configure step. Do not overwrite a working build tree.

## 1. Platform

| Item | Recorded value |
| --- | --- |
| macOS | Catalina 10.15.x, Intel x86_64 |
| Apple Clang | 12.0.0 (`clang-1200.0.32.29`) |
| Python | 3.10.2 |
| Waf | Included with the Ardour 7.5 source |
| Meson / Ninja | 0.62.2 / 1.10.2 |
| CMake | 3.20.0 |
| pkg-config | 0.29.2 |
| Build threads | 2 |

The original terminal reported the SDK directory at `/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk`. Do not hard-code that path: use `xcrun --sdk macosx --show-sdk-path`.

## 2. Project directories

The local build used the following **paths under the build user's home directory**. Adjust these variables for your machine:

```bash
export ROOT="$HOME/DTM/build-env/gtk-osx-2022"
export GTK_PREFIX="$HOME/gtk/inst"
export GETTEXT_PREFIX="$ROOT/tools/gettext-0.21"
export ARDOUR_SRC="$HOME/DTM/ardour-src/ardour-7.5"
export INSTALL_PREFIX="$HOME/DTM/ardour-7.5-install"
export BOOST_SRC="$ROOT/work/boost_1_76_0"
```

The original app was packaged separately at `~/DTM/ardour-7.5-app/Ardour7.app`.

## 3. Observed direct dependencies

Versions confirmed using `pkg-config` during the successful process:

| Library | Version |
| --- | --- |
| TagLib | 1.12 |
| Vamp SDK and Host SDK | 2.10 |
| Rubber Band | 3.3.0 |
| FFTW (single precision) | 3.3.10 |
| aubio | 0.4.9 |
| libsamplerate | 0.2.2 |
| LV2 | 1.18.10 |
| Serd | 0.30.16 |
| Sord | 0.16.14 |
| Sratom | 0.6.14 |
| Lilv | 0.24.20 |
| Ogg | 1.3.5 |
| FLAC | 1.4.3 |
| libsndfile | 1.2.2 |

Other required libraries included GTK2/Quartz, gtkmm, GLib, Cairo, Pango, fontconfig, libxml2 and more. **Their exact versions and complete source/provenance inventory were not captured.** This is why a release-grade rebuild from scratch cannot yet be claimed.

### FFTW threads

Ardour linked against `libfftw3f_threads`, not just `libfftw3f`. The first build omitted the thread variant, then it was successfully rebuilt from the original FFTW 3.3.10 source with:

```bash
# Example configure options; use a separate, clean FFTW build directory.
/path/to/fftw-3.3.10/configure \
  --prefix="$GTK_PREFIX" \
  --enable-float --enable-threads \
  --enable-shared --disable-static --disable-fortran
```

**Do not blindly run `make install` if that would replace your existing `libfftw3f`**. The recorded repair staged the result and installed only `libfftw3f_threads*.dylib` after reviewing its dependency IDs. The thread-enabled FFTW library resolved the missing `libfftw3f_threads` link dependency, and the Ardour build and GUI launch subsequently succeeded. **A dedicated runtime test of the FFTW thread API was not recorded; thread behavior remains unverified.**

### GNU gettext

GNU gettext 0.21 was already available under `$GETTEXT_PREFIX`, but its `libintl.h` and `libintl.dylib` were outside `$GTK_PREFIX`. Ardour needs both the header include path and library search path.

## 4. Configure Ardour

Set the compiler and SDK environment before Waf configure:

```bash
export PATH="$ROOT/runtime/python-3.10.2/bin:$ROOT/tools/bin:$GETTEXT_PREFIX/bin:$GTK_PREFIX/bin:$PATH"
export PKG_CONFIG="$ROOT/tools/bin/pkg-config"
export PKG_CONFIG_PATH="$GTK_PREFIX/lib/pkgconfig:$GTK_PREFIX/share/pkgconfig"
export PKG_CONFIG_LIBDIR="$PKG_CONFIG_PATH"
export CC="$(xcrun --find clang)"
export CXX="$(xcrun --find clang++)"
export SDKROOT="$(xcrun --sdk macosx --show-sdk-path)"
export CFLAGS="-isysroot $SDKROOT -I$GETTEXT_PREFIX/include"
export CXXFLAGS="-isysroot $SDKROOT -I$GETTEXT_PREFIX/include"
export LDFLAGS="-isysroot $SDKROOT -L$GETTEXT_PREFIX/lib -Wl,-rpath,$GETTEXT_PREFIX/lib"

cd "$ARDOUR_SRC"
./waf configure \
  --keepflags \
  --prefix="$INSTALL_PREFIX" \
  --boost-include="$BOOST_SRC" \
  --also-include="$GETTEXT_PREFIX/include" \
  --also-libdir="$GETTEXT_PREFIX/lib"
```

Why these parameters matter:

- `-isysroot`: without it, `<cmath>` failed because C system headers were not found in the SDK search path.
- `--keepflags`: preserves the SDK and gettext environment flags in Ardour 7.5's Waf configuration.
- `--boost-include`: locates Boost 1.76.0 headers outside the normal installation prefix.
- `--also-include` / `--also-libdir`: includes the separate gettext 0.21 installation.

Confirm `-isysroot` and the gettext include path in the printed C/C++ compiler flags. `configure` success by itself does not guarantee that all dynamically linked libraries required by the subsequent build exist.

## 5. Apply the source workaround (only when necessary)

The local build source has been identified as Git `HEAD` `e1950ec49e601864f06e316ba8cee730a3964989` (local `git describe` output: `7.5-dirty`). The affected file and the included patch were matched against that exact `HEAD` file on the original Mac. Step 160-B verified the configured `origin` as `https://github.com/Ardour/ardour.git` and resolved both the local `7.5` tag and the official GitHub mirror `7.5` tag to the same commit. The originally used clone URL and signed-tag authenticity remain unverified. `Git version: 7.5` alone is not a commit identifier. On the build Mac, repeat the read-only check with `bash scripts/record_source_identity.sh "$ARDOUR_SRC"`; see [`SOURCE_IDENTITY.md`](SOURCE_IDENTITY.md).

If the checkout has the **unmodified** `#error NO TAG` block and the GTK stack lacks `ARDOUR_CANVAS_NSVIEW_TAG`:

```bash
cd "$ARDOUR_SRC"
git apply --check /path/to/this-repo/patches/0001-catalina-gtk-quartz-canvas-fallback.patch
git apply /path/to/this-repo/patches/0001-catalina-gtk-quartz-canvas-fallback.patch
```

The original Mac's source **has already been edited**: do not apply the patch a second time. See `PATCHES.md` for risks and verification steps. The patch is **not a substitute** for a fully compatible Ardour-patched GTK Quartz stack.

## 6. Build and run from the build tree

```bash
cd "$ARDOUR_SRC"
./waf build -j2

# From a macOS desktop GUI session (not necessarily plain SSH):
cd "$ARDOUR_SRC/gtk2_ardour"
./ardev
```

The successful build produced `build/gtk2_ardour/ardour-7.5.0`. A separate check using `./ardev --version` printed Ardour 7.5.0 and returned status 0.

## 7. Making the local `.app`

The upstream macOS bundling mechanism is documented at https://ardour.org/building_osx_native.html and uses `tools/osx_packaging/osx_build --public`. The local build did **not** use that upstream script end-to-end because it included operations unsuitable for this environment.

The local packaging work instead (historical description; the full custom local packaging scripts are not included as a reproducible turnkey tool):

1. Staged `Ardour7.app` under a **new** directory, leaving the build tree intact.
2. Copied UI resources, fonts, icons, modules and plugins found in the build tree.
3. Resolved symbolic links and recursively gathered Mach-O dependencies from the local GTK/gettext/build prefixes, excluding Apple's system libraries.
4. Rewrote non-system install names to `@executable_path/../lib/<filename>` using `install_name_tool`.
5. Verified dependency references for all 96 scanned Mach-O files; performed ad-hoc signing with `codesign -s -`.
6. Checked `--version` in normal and bundled launch modes. **Bundled Ardour redirects stdout/stderr to its user Preferences logs**, so bundled `--version` may exit 0 while writing nothing to the terminal.
7. Renamed the staging bundle to `~/DTM/ardour-7.5-app/Ardour7.app`, then checked Finder GUI launch and basic input.

The local package reported **63** additional dependency libraries and **906** rewritten references. These are the machine's logged results, **not verified universal counts**. The original ad-hoc packaging scripts were custom and machine-specific; a clean-room, publicly redistributable packaging implementation and audit remain outstanding.

Use `scripts/audit_bundle.py` to generate a dependency inventory of your local `.app` before evaluating binary distribution. This inventory includes symlink aliases and flags unresolved links, external absolute paths, bare install names and `@rpath` entries for manual investigation; it is not a full dynamic-loader simulation.

## 8. Unresolved validation

- No confirmed playback/recording test using CoreAudio.
- OpenGL canvas, AudioUnit and VST3 plugin window behavior is not fully validated.
- Other Intel Macs, newer macOS versions and ARM64 Macs are not validated.
- Source Git HEAD and single-file patch reproducibility are now verified; the original clone URL, signed-tag authenticity, complete dependency lockfile, clean-machine reproducibility and full packaged-component license audit remain outstanding.
- Local ad-hoc signing is not a substitute for Apple Developer ID signing/notarization when preparing broadly downloadable macOS software.

Do not claim a ready-to-distribute `.app` based on the local success described here.

## License distinction

The commands and original notes in this repository are licensed under MIT; the patch to upstream Ardour is GPL-2.0-or-later and is excluded from the root MIT grant. See [`LICENSE_SCOPE.md`](LICENSE_SCOPE.md). The compiled Ardour app and its dependencies are not included and are not cleared for redistribution.
