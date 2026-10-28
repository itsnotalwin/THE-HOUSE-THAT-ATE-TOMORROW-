# Foyer visual grammar

Dark damask sits above timber wainscoting; long floorboard courses keep the walking area visually quiet. Carved arches, striped rose runners, plump reading chairs and brass chandeliers use chunky, deliberate clusters. Native assets contain only the shared sixteen palette colors and transparent pixels; there is no antialiasing or baked lighting blur.

The Almost retains atlas coordinates and furniture silhouettes. Cold materials accompany a changed portrait, ghost rain and floating pages. Its absent reader is a separate overlay. Nameplates stay blank so clue typography can later render at a readable UI resolution.

The atlas includes multi-cell objects as contiguous rectangles. Reconstruct those using metadata rather than treating every object fragment as a standalone repeating tile. Zero padding requires nearest sampling without mipmaps; engine import validation is deferred. Review examples are in `../review/ENVIRONMENT_ATLAS_REVIEW.png` and `../review/ART_MODE_COMPARISON.png`; they are static art layouts, not runtime screenshots.
