# Branding art samples

Exact-title original layout and vector ornaments. Files are staged for human review, not approved production artwork. The text-free mansion background lives separately under `../concept/`.

- `title_wordmark.svg`: editable title text and vector ornaments.
- `title_wordmark_outlined.svg`: portable glyph outlines; does not require a font installation.
- `title_wordmark.png`: 1000×420 transparent antialiased export.
- `title_tagline_lockup.svg`, `_outlined.svg`, `.png`: separate 1000×90 tagline layer.
- `branding_review.png`: labelled display sample on an ink background.
- Matching JSON files record content, dimensions, sources, and alpha/filter rules.

Rebuild with `python art_staging/source/draw_branding.py` from the repo root. Requires Pillow and fontTools. Text SVGs reference bundled fonts; install the provided fonts if an editor does not support relative font-face URLs, or use the outlined version.
