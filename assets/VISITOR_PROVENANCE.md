# Visitor character revision

The player requested a dark-haired girl for the playable character. This revision gives the Visitor long dark hair and a pink-and-gold hair clip; the same visual features appear in her companion portraits. Her four movement directions, idle plus four walking frames, 24 × 32 cells, 120 × 128 sheet, foot anchor, and approved palette are retained.

- `visitor_sheet.png`: SHA-256 `70b2ac4e47899edeb7c7a7c951bad6fb63071ce8081bd0bfe1baa610806a2b2d`.
- `visitor_portraits.png`: SHA-256 `66ba3c6db4a247e92a81035a8c5a1128aa03877a45e35c9eb0812ec446da47d9`; three 64 × 64 frames: neutral, happy, concerned.
- Source: `tools/draw_visitor.py` (Python 3, Pillow), drawing original pixels over the project's original approved sprite cells. No external character art was sampled.

The original approved character sheet remains unchanged at `art_staging/sprites/visitor_sheet.png` (SHA-256 `93aea858ae17f71320728196a7fe434a300ce62083d61a1531475598e40384a5`). It remains the historical art-review baseline; the revised runtime files are new work and are no longer represented as exact copies of that approved sheet in `approved_manifest.csv`.
