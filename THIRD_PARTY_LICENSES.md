# Third-party licenses and provenance — initial inventory

## Do not treat this document as license clearance

This document distinguishes **observed installed versions** from **actual third-party components redistributed in a particular `.app`**. The successful local bundling run reported 63 additional library entries (not 63 separately identified projects), but the file-by-file list and each exact license notice have **not** been collected in this environment. It would be misleading to claim that all 63 have been reviewed.

A GitHub **documentation-only** repository may be published separately from a binary release. **Do not publish the packaged `.app`, a DMG, or copied third-party binaries until this audit is complete.**

## Software and known licensing leads

| Component | Observed version | Public license information | Evidence status | Required action |
| --- | --- | --- | --- | --- |
| Ardour | 7.5.0 | GNU GPL, official site supplies GPL v2 text | Official source and exact 7.5 notices still require confirmation | Include applicable COPYING, original source, local patch and build scripts |
| Vamp Plugin SDK / Host SDK | 2.10 | BSD-style SDK terms as described by the project | Upstream project description | Review exact distribution's COPYING and copyright notices |
| TagLib | 1.12 | LGPL/MPL choice as described by the project | Upstream project description; **exact 1.12 terms still to check** | Select compliant option and retain required notice/source material |
| Rubber Band | 3.3.0 | **Unverified for this exact build** | Version observed only | Check exact source tree and any commercial/GPL terms |
| FFTW | 3.3.10 | **Unverified for this exact build** | Version observed only | Check exact source tree, especially `libfftw3f_threads` |
| gettext / libintl | 0.21 | **Unverified for this exact build** | Files in separate prefix were observed | Read gettext 0.21 licenses and copyright notices |
| aubio | 0.4.9 | **Unverified** | Version observed only | Check original source COPYING |
| libsamplerate | 0.2.2 | **Unverified** | Version observed only | Check original source COPYING |
| LV2 | 1.18.10 | **Unverified** | Version observed only | Check LV2 source and distribution notice |
| Serd | 0.30.16 | **Unverified** | Version observed only | Check exact Serd source |
| Sord | 0.16.14 | **Unverified** | Version observed only | Check exact Sord source |
| Sratom | 0.6.14 | **Unverified** | Version observed; SHA-512 verified | Check exact Sratom source |
| Lilv | 0.24.20 | **Unverified** | Version observed; SHA-512 verified | Check exact Lilv source |
| Ogg | 1.3.5 | **Unverified** | Version observed; SHA-256 verified | Check exact libogg source |
| FLAC | 1.4.3 | **Unverified** | Version observed; SHA-256 verified | Check exact FLAC source |
| libsndfile | 1.2.2 | **Unverified** | Version observed only | Check exact libsndfile source |
| GTK2 / GDK Quartz / gtkmm / glibmm / GLib / Pango / Cairo / fontconfig / Freetype / other transitive libraries | Not completely captured | **Unverified individually** | Libraries were observed in link output | Inventory all actual packaged files and license notices |
| Ardour fonts, icons, themes, scripts, LV2/Vamp plugins and optional assets | Mixed / not fully captured | **Unverified individually** | Assets were copied to local bundle | Inspect actual contents and upstream copyright/license notices |

The above names **do not mean every library was included as an independent shared object**. They are a provisional build/dependency list. Some components may be statically included, dynamically linked, or used only at build time.

## How to perform the actual bundle audit

On the original Intel Mac, from this repository:

```bash
python3 scripts/audit_bundle.py \
  --app "$HOME/DTM/ardour-7.5-app/Ardour7.app" \
  --output "$HOME/DTM/ardour-7.5-license-audit"
```

The script generates:

- `macho_inventory.csv` — each Mach-O image, a SHA-256, install ID and signing status if available;
- `dependencies.csv` — dependency install names and a classification (system / app-relative / unresolved);
- `assets.csv` — packaged non-Mach-O files including fonts and bundled assets;
- `symlinks.csv` — every packaged symlink, its target and whether it resolves inside the bundle, is broken or points outside;
- `audit_summary.txt` — counts and unresolved reference warnings.

**Review the resulting CSV data manually**. The symlink report must be inspected independently because dyld can follow library aliases, and the audit tool treats unresolved `@rpath`/bare-name references conservatively as pending review. The report intentionally does not claim that 96 Mach-O images or 63 third-party packages are uniquely redistributable components. The script cannot infer definitive software package ownership or license terms from a binary filename. Save each exact source COPYING/LICENSE/NOTICE text, match it to the actual copied file/version and retain the appropriate attributions and corresponding sources.

## GPL source obligations and additional assets

GPL v2 section 3 describes several ways to comply when distributing a binary, including making complete corresponding source (with scripts controlling compilation and installation) available. Providing **only** an upstream repository URL may not cover local patches, exact source revisions or external components.

Full obligations depend on the actual licenses, linking arrangement and distribution method; this matrix is technical due diligence, not legal advice. For general source obligations see https://www.gnu.org/licenses/gpl-faq.en.html and https://ardour.org/copying.html .

## Scope of the documentation repository license

The root [`LICENSE`](LICENSE) (MIT) covers independent repository notes, helpers and original inventories, **not** Ardour source or the third-party components listed here. The Ardour-derived patch remains GPL-2.0-or-later; see [`LICENSE_SCOPE.md`](LICENSE_SCOPE.md). The dependency licenses and related binary redistribution obligations remain unverified and unchanged by the repository license decision.
