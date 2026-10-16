# Sources and verification boundaries

Source URLs reviewed when assembling this documentation on 2026-10-14:

| Area | Reference |
| --- | --- |
| Ardour macOS source build and packaging flow | https://ardour.org/building_osx_native.html |
| Ardour license text | https://ardour.org/copying.html |
| Ardour official GitHub mirror (local `origin` and independently queried remote reference by build-machine Git) | https://github.com/Ardour/ardour |
| Exact Ardour 7.5 commit on GitHub mirror | https://github.com/Ardour/ardour/commit/e1950ec49e601864f06e316ba8cee730a3964989 |
| Ardour contribution policy (LLM-generated code) | https://ardour.org/development |
| GTK Quartz `NO TAG` discussion | https://discourse.ardour.org/t/libgtkmm2-fails-when-attempting-a-build/108367 |
| GNU GPL FAQ on matching sources and scripts | https://www.gnu.org/licenses/gpl-faq.en.html |
| Vamp SDK license statement | https://vamp-plugins.org/code-doc/main.html |
| TagLib license statement | https://taglib.org/ |
| GitHub releases | https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases |
| GitHub large files | https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github |
| Apple Developer ID signing | https://developer.apple.com/developer-id/ |

**Build-machine evidence:** The builder supplied Waf, packaging, GUI-verification, Step 160-A and Step 160-B terminal output. These outputs are not a direct inspection of the Mac by this documentation author.

- **Step 160-A:** Verified local Git `HEAD` `e1950ec49e601864f06e316ba8cee730a3964989`, pristine/patched file SHA-256 values and byte-for-byte patch equivalence.
- **Step 160-B:** Read the configured `origin` (`https://github.com/Ardour/ardour.git`), resolved local `7.5` tag to `HEAD`, and queried the official public GitHub mirror using `git ls-remote --tags`. The remote `7.5` reference resolved to the **same commit**. All reported comparisons passed; return code was zero.

**Limits:** A configured remote does not establish the original `git clone` URL, nor does tag equality prove cryptographic tag authenticity. Neither check establishes clean-machine reproducibility, provenance for untracked files/submodules, or a third-party binary redistribution license audit. Upstream documents and policies may evolve after the recorded build.

## License references (Step 160-C)

- MIT license: https://choosealicense.com/licenses/mit/
- Ardour GPL v2 text: https://ardour.org/copying.html
- SPDX `GPL-2.0-or-later`: https://spdx.org/licenses/GPL-2.0-or-later
- GitHub repository license guidance: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository

The repository's selected MIT license covers only original materials and does not supersede the upstream license for the Ardour-derived patch or any dependency. See [`LICENSE_SCOPE.md`](LICENSE_SCOPE.md).
