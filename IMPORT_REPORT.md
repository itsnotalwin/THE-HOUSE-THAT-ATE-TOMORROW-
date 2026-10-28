# Handoff import verification

**Import date:** 26 October 2026  
**Source archive:** `The_House_That_Ate_Tomorrow_Codex_Handoff.zip`  
**Archive SHA-256:** `1ccf939b941607e1f8c8e45ed202d187e537a78a5510bd8254f4f8cfa0b76f36`

## Import layout

The archive's enclosing `The_House_That_Ate_Tomorrow_Codex_Kit/` directory was removed, placing its contents at the repository root while preserving all internal paths and file bytes. The archive itself remains an upload outside the repository.

The separate `CODEX_MASTER_PROMPT.md` upload is byte-identical to the archive copy. One unchanged copy was imported.

## Validation results

| Check | Result |
| --- | --- |
| ZIP integrity / CRC | Passed for every member |
| Unsafe archive paths, symlinks, duplicate destinations | None found |
| Existing files overwritten | None; repository was empty |
| Imported handoff files | 22: 13 Markdown, 7 PNG, 1 CSV, 1 checksum manifest |
| Original SHA-256 entries | All 21 matched before import and after writing |
| Checksum coverage | Every supplied file except the checksum manifest itself |
| Standalone / archived master prompt | Byte-identical |
| PNG integrity | All 7 decoded and passed Pillow verification |
| PNG classification | RGB concept images; no transparent production sheets supplied |
| CSV asset backlog | 82 entries; all `NOT STARTED` |
| Art review signoff | Unsigned, preserved unchanged |

## Supplied image inventory

| File | Dimensions |
| --- | --- |
| `art_references/00_OVERVIEW.png` | 1500×740 |
| `art_references/01_TITLE_WORLD_CAST_REFERENCE.png` | 1536×1024 |
| `art_references/02_TITLE_KEY_ART_CONCEPT.png` | 628×484 |
| `art_references/03_CHARACTER_LINEUP_CONCEPT.png` | 644×307 |
| `art_references/04_palette_and_scale.png` | 1400×850 |
| `art_references/05_environment_comparison.png` | 1320×420 |
| `art_references/06_ROOM_EXAMPLES_CONCEPT.png` | 531×298 |

File integrity checks establish that the import matches the upload. They do not establish production art quality, rights clearance, or a working game.

## Repository additions

The initial import added `README.md`, `PROJECT.md`, `AGENTS.md`, `.gitignore`, and this report to explain the checkout and how to use the supplied material. These five files are outside the original checksum manifest. After the user separately requested original artwork, the repository gained `art_staging/` and art reports, and the setup documents were updated. The original 22 supplied files remain unchanged.

The supplied documents' references to `itsnotalwin/Innate`, a private vault, Godot 4.6.3, earlier maps, deployment blockers, and third-party art licensing were preserved without treating them as verified current facts. No external repository or private vault was accessed as part of this import.
