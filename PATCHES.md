# Local source modification: GTK Quartz canvas guard

**Status:** Applied on the original build machine; compiled successfully; app launched; basic GUI operations worked. **This is a local compatibility workaround, not an upstream patch or general-purpose fix.**

## Affected file

`libs/gtkmm2ext/nsglview.mm` in the Ardour 7.5 source tree.

The original guard aborts compilation when Ardour's GTK Quartz extension does not provide `ARDOUR_CANVAS_NSVIEW_TAG`:

```cpp
#ifndef ARDOUR_CANVAS_NSVIEW_TAG
#error NO TAG
#define ARDOUR_CANVAS_NSVIEW_TAG 0x0
#endif
```

The machine-tested modification replaced the `#error` with an explanatory comment while leaving the fallback `0x0` definition unchanged:

```cpp
#ifndef ARDOUR_CANVAS_NSVIEW_TAG
/* No patched GTK Quartz tag: normal Cairo canvas is used. */
#define ARDOUR_CANVAS_NSVIEW_TAG 0x0
#endif
```

File: [`patches/0001-catalina-gtk-quartz-canvas-fallback.patch`](patches/0001-catalina-gtk-quartz-canvas-fallback.patch)

**Exact local build source:** Git HEAD `e1950ec49e601864f06e316ba8cee730a3964989` (local description `7.5-dirty`).

- Pristine `HEAD` file SHA-256: `ef8e8a7dcf50ae74377a5ffba6d57ef7a6df7e54250498bff9c924ebbcd7898a`
- Patched local file SHA-256: `188905e362f0a720847a12e94145b975328dd01d6315be441979a9ab7d695cfc`
- Step 160-A (2026-10-14): `git apply --check` against an isolated pristine `HEAD` copy **passed**; applying the patch to that copy and comparing it to the modified local file **passed, byte for byte**.
- The patch text tested in Step 160-A is identical to the `.patch` file linked above.

These hashes and results identify **this particular checked-out file**, not every Ardour 7.5 checkout. See [`SOURCE_IDENTITY.md`](SOURCE_IDENTITY.md).

## Applying it

1. Obtain a clean copy of the exact recorded Git HEAD `e1950ec49e601864f06e316ba8cee730a3964989` (official GitHub mirror tag `7.5` matches this commit in Step 160-B; verify on your own machine before use).
2. Check that the GTK Quartz macro is genuinely missing, and consider using Ardour's patched GTK stack instead.
3. Back up or commit the original source before applying the patch. The provided patch has been checked and applied to a pristine copy of the **actual recorded Git HEAD file**, without modifying the original build checkout.
4. Run `bash scripts/record_source_identity.sh <source-directory>` from this documentation repository to inspect the source and perform the isolated patch comparison. On a **separate, pristine checkout**, run `git apply --check <patch-file>` followed by `git apply <patch-file>` **once**, only if the GTK situation calls for this workaround.
5. Rebuild, launch and test rendering, cursor movement, selection and plugin window behavior.

Do **not** apply the patch to a checkout already containing this modification. Do not use `#define ARDOUR_CANVAS_NSVIEW_TAG` as an unconditional compiler flag without understanding GTK's event routing.

## Risks

The macro is related to a custom NSView/GTK Quartz event-routing contract. Suppressing the compile-time guard does not make the unpatched GTK implementation semantically equivalent to the required patched version. It may affect OpenGL canvas input routing, plugin GUIs or other events even when the application launches. The original builder confirmed basic GUI interaction, not the entire feature matrix.

### Provenance

- Applied in the local project on 2026-10-14, after the `NO TAG` compile failure.
- Similar Ardour 7.3 problem discussed publicly: https://discourse.ardour.org/t/libgtkmm2-fails-when-attempting-a-build/108367
- There is no claim that Ardour upstream accepted this workaround.

## License

**SPDX: `GPL-2.0-or-later`.** This file is a patch to GPL-covered Ardour source, not material subject to the repository root MIT license. Keep original copyright and licensing notices intact and comply with the actual Ardour 7.5 source-file terms when distributing modified versions. The patch file was not edited during the licensing decision, preserving the successful file-level reproducibility check. See [`LICENSE_SCOPE.md`](LICENSE_SCOPE.md) and [`UPSTREAM_LICENSES/GPL-2.0.txt`](UPSTREAM_LICENSES/GPL-2.0.txt).
