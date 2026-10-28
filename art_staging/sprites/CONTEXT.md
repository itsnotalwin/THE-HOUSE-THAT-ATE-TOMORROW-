# Native character art

Original pixel drawings for art review. `visitor_sheet.png` contains 20 frames in 24×32 cells; rows face south, west, east, north and columns are idle followed by four walk frames. `fig_sheet.png` contains four 24×24 poses. `fig_portraits.png` contains three 64×64 expressions. Six individual cast PNGs are static silhouette/scale studies, not complete NPC animation sets.

JSON beside each PNG records dimensions, frame rectangles, anchors, timing, source and status. `validation.json` records actual alpha, palette, clear-border and frame checks. Rebuild with `python art_staging/source/draw_characters.py`. These are unapproved production-scale samples; runtime imports and animation feel remain untested.
