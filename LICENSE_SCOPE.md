# License scope and attribution

This repository uses **different licenses for independent documentation/tools and Ardour-derived material**. The root [`LICENSE`](LICENSE) file does **not** relicense Ardour or any third-party component.

| Files | License | Notes |
| --- | --- | --- |
| Original English documentation in the repository root (except upstream reference texts) | **MIT** | Copyright (c) 2026 Contributors to the Ardour 7.5 Catalina Build Notes |
| `scripts/`, `tests/`, and independently prepared inventory metadata in `inventory/` | **MIT** | Applies only to original contributions, not to any incorporated third-party material |
| `patches/0001-catalina-gtk-quartz-canvas-fallback.patch` | **GPL-2.0-or-later** | Derived from the Ardour 7.5 source file. Preserve upstream copyright and source license notices; this patch is **not MIT-licensed** |
| `UPSTREAM_LICENSES/GPL-2.0.txt` | GNU GPL version 2 legal text (verbatim) | License text supplied for upstream compliance/reference; not a MIT-licensed creative work |
| `Ardour7.app`, original Ardour source, GTK stack, other third-party artifacts | **Not included in this repository** | Each component retains its own applicable upstream rights and obligations |

## Ardour-specific license

Ardour's source notices generally grant reuse under **GNU GPL version 2 or (at the licensee's option) any later version**. The identifier `GPL-2.0-or-later` is used for the patch derived from that code. This repository contains the GNU GPL version 2 license text at [`UPSTREAM_LICENSES/GPL-2.0.txt`](UPSTREAM_LICENSES/GPL-2.0.txt). Source-file-specific notices and any exceptions in the recorded Ardour 7.5 checkout remain authoritative. See [`PATCHES.md`](PATCHES.md) and [`SOURCE_IDENTITY.md`](SOURCE_IDENTITY.md).

## Copyright-holder attribution

The publisher **formally adopted** the collective notice **“Contributors to the Ardour 7.5 Catalina Build Notes”** on 2026-10-14 (Step 160-E). The same wording appears in the root `LICENSE`. This records the publisher's chosen attribution, **not independently verified evidence** of the identity or authorization of every rights holder. In Step 163 on 2026-10-15, the publisher explicitly stated that they own and may distribute the **independently prepared** content under MIT, and retained the selected collective public credit. This is a publisher **self-attestation, not independently verified ownership**. If any other contributor or employer holds relevant rights, obtain their
authorization or promptly amend/remove affected published materials. The
publisher approved the exact 24-file initial public package in Step 166
(2026-10-16); Step 169 published it, and Step 170 verified public visibility
and content correspondence. **That publication approval is complete, but it
is not an independent audit of underlying ownership, employment assignments,
or other applicable rights.** MIT selection does not relicense third-party
content. See [`COPYRIGHT_REVIEW.md`](COPYRIGHT_REVIEW.md).

## Policy for reuse and contributions

- Retain the MIT copyright/license notice in copies of MIT-covered material.
- Keep the Ardour-derived patch under the applicable GPL terms; do not change its text merely to insert a copyright header, because the exact patch has been byte-for-byte verified against the local build.
- This repository documents an **unofficial local workaround**. It does not represent upstream approval or an invitation to submit generated code to Ardour upstream; check the [Ardour contributor policy](https://ardour.org/development) separately.
- **No permission to redistribute the compiled `.app` or bundled dependencies is represented by the MIT license for this repository.** The binary release compliance audit is incomplete.

## References

- [MIT license reference](https://choosealicense.com/licenses/mit/)
- [Ardour GPL v2 text](https://ardour.org/copying.html)
- [SPDX: GPL-2.0-or-later](https://spdx.org/licenses/GPL-2.0-or-later)
- [GitHub repository licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
