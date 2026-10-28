# Original art production plan — revision 1

**Date:** 26 October 2026  
**Authorized work:** The user requested original artwork after importing the handoff, with gameplay kept for later.  
**Status:** First art sample pass delivered on 27 October 2026; see `ART_REVIEW_REPORT.md`. No art approval recorded.

## Baseline and boundaries

This checkout began empty, on `work`, with origin `itsnotalwin/THE-HOUSE-THAT-ATE-TOMORROW-`. The supplied handoff is intact and its checksums pass. Seven RGB concept references and an 82-item unstarted backlog were supplied; there are no existing sprites, third-party art packs, or Godot sources here to reuse. The older `Innate` repository and private vault have not been inspected, migrated, or modified. Their historical engine, export, and licensing claims do not establish this checkout's state.

All new work stays under `art_staging/`, with this plan and the review report at the root. This stage authors graphics and export/validation helpers only. Gameplay, scenes, collision data, CI, releases, and deployment remain later work.

## Tools and source pipeline

- Built-in ImageGen: original text-free mansion illustration, explicitly classified as concept art. Its returned image is preserved without claiming native pixel-grid suitability.
- Python 3 and Pillow: original coordinate-authored pixel drawings, native PNG exports, deterministic static room compositions, contact sheets, and art validation. These are art tools, not gameplay generators.
- SVG and installed freely licensed fonts: exact editable wordmark and tagline, transparent exports, and readable UI typography. Record font provenance and redistribution terms alongside the assets.
- The Creative Production board tool is unavailable in this session. Review is delivered through saved images and repository links.

Sources live in `art_staging/source/` and editable branding files in `art_staging/branding/`. Output filenames describe subject, mode, and variant. Metadata shares each sheet's stem as a JSON file wherever practical.

## Shared art specification

| Element | Specification |
| --- | --- |
| World tile | 16×16 native pixels; no gaps or atlas padding |
| Hall layout mockup | 512×352 native pixels, two compositions; fixed coordinates within each Here/Almost pair |
| Camera reading sample | 384×216 native pixels; nearest integer enlargement |
| Visitor | 24×32 cells, rows south/west/east/north, idle + four walk frames |
| Fig | 24×24 cells, idle/blink/tail/talk poses; 64×64 expression portraits |
| Other cast | Individual native static concept sprites, coherent relative scale |
| Native tile/sprite alpha | RGBA, hard 0/255 alpha; transparent margin where appropriate |
| Native palette | Exact 16 colors from `art_staging/palette.json`, copied from the written art bible |
| Branding/UI text | Separate high-resolution text layer; antialiasing permitted for readability |
| UI samples | 1366×768 and a compact presentation; effective body text at least 16px |
| Runtime import proposal | Nearest filtering, lossless textures, no mipmaps for native pixel art; unimplemented |

The Here uses warm timber, plum, and candlelight. The Almost keeps the room geometry and furniture positions, adds cool spectral colors and visibly different clue/ghost shapes. Color alone must not carry the change.

## Deliverables for this pass

1. Two tile-built hall composition candidates and a matched Here/Almost pair for each.
2. Original text-free mansion illustration; separate editable title and tagline; static menu composition.
3. Native Visitor and Fig sheets with animation metadata and a six-character scale lineup.
4. Modular tile atlas, props, guestbook/nameplate pairs, and placement metadata for static art review.
5. Dialogue frame, focus states, notebook/inventory samples, and useful native icons.
6. Palette, native-scale contact sheets, comparison previews, manifest, validation report, and disclosed remaining limitations.

## Provenance and rights

No supplied concept crop will be promoted into a production sprite. New native art is coordinate-authored for this project; the mansion concept is AI-generated. Preserve that distinction in metadata. No third-party game artwork or Sprout Lands files are used. Keep any redistributed font's license with its file. Do not invent a blanket repository license or assert trademark clearance.

## Validation and review

Check image decoding, dimensions, exact cell grids, frame counts, occupied bounds, transparent margins, hard alpha, native palette membership, distinct walk poses, tile footprints, and static room placement parity. Inspect actual exports visually at native size and nearest 2×/4×. Check typography strings and high-resolution UI contrast/readability. Assemble a report from observed checks, not the desired specification.

Technical validity does not establish artistic approval or runtime usability. The final report will distinguish usable native art samples, static concepts, and unfinished refinements. The user's next art review determines changes or approval; this pass does not implement the game.
