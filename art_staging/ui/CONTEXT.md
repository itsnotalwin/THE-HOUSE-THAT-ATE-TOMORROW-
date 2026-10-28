# UI art samples

Original native UI components and static high-resolution interface studies. This folder contains artwork and metadata only, with no runtime implementation. Export with `python art_staging/source/draw_ui.py` from the repository root. Requires Pillow and the bundled DejaVu fonts in `../branding/fonts/`.

`icons_sheet.png` has ten 24×24 cells. Individual icon exports include a separate focus arrow. `dialogue_panel.png` and the three button backgrounds use 8px nine-slice margins. `portrait_frame.png` has a 64×64 transparent content area. All native PNGs are RGBA, exact shared palette, binary alpha.

Static dialogue and notebook/inventory samples are saved in `../review/UI_*`. They demonstrate typography and layout at 1366×768 and 960×540, not functioning interaction. No human art approval is recorded.
