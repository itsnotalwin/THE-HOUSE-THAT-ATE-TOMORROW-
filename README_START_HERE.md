# The House That Ate Tomorrow — Codex preproduction handoff

**Package version:** 1.0 | **Prepared:** 26 October 2026 | **Stage:** concept approved in principle; artwork NOT approved; gameplay implementation NOT authorized by this handoff.

A 40–50 minute, 2D top-down narrative puzzle adventure for Paige, built in Godot, with spooky mystery, cozy exploration and bizarre humor. The experience must be a complete, tightly scoped authored adventure rather than an expansive generic map.

## Your first move

1. Read `CODEX_MASTER_PROMPT.md` completely. Paste it into Codex together with this kit or place this folder in its workspace.
2. Codex must read `docs/01_GAME_DESIGN_DOCUMENT.md`, `docs/02_ART_DIRECTION_BIBLE.md`, `docs/03_WORLD_AND_PUZZLES.md`, and `docs/04_STORY_AND_DIALOGUE.md` before proposing assets.
3. Codex must inspect the existing `itsnotalwin/Innate` repository **read-only** and obey existing root/parent context and vault build standards. The project's recorded default-branch and Pages issues must be checked, not assumed fixed.
4. **PHASE ART-0 and ART-1 ONLY:** Create original production-scale visual assets and compelling previews before any new gameplay source is written. Save them in a dedicated staging location or separate branch. Include contact sheets and an asset review manifest.
5. **STOP FOR HUMAN ART APPROVAL.** Do not proceed to implementation merely because previews were generated, and do not treat concept boards as shipped sprite art.
6. After explicit approval, implement the playable vertical slice first, and stop for review before full production.

## Canonical project naming (updated 26 October 2026)

**Selected player-facing title:** **The House That Ate Tomorrow**  
**Selected tagline:** **Tomorrow is missing. The cat denies everything.**

This replaces the provisional player-facing name in all active specs, prompts, and concept references. The GitHub source repo `itsnotalwin/Innate` and private BRAIN path `20_Projects/INNATE-Paige-Game.md` are **legacy technical identifiers**, not approved public branding and not instructions to rename repositories. Their names should remain unchanged until separately authorized.

Artwork must be delivered **first**, including an independently editable title/wordmark and tagline. The images are concept references, not native game art. Formal name/trademark availability for a potential public commercial release has not been cleared.

## File map

| File | Purpose |
| --- | --- |
| `NAME_UPDATE.md` | Selected-title rename record, immutable source ID distinction |
| `CODEX_MASTER_PROMPT.md` | Copy/paste controlling Codex instruction with explicit stop points |
| `docs/01_GAME_DESIGN_DOCUMENT.md` | Complete vision, gameplay, story, controls, UX, non-goals and scope |
| `docs/02_ART_DIRECTION_BIBLE.md` | Aesthetic rules, pixel sizes, palette, animation specs and reference imagery |
| `docs/03_WORLD_AND_PUZZLES.md` | All seven locations, puzzle solutions, progression flags and anti-softlock rules |
| `docs/04_STORY_AND_DIALOGUE.md` | Three-act plot, character arcs, samples and writing/ending rules |
| `docs/05_TECHNICAL_ARCHITECTURE.md` | Proposed Godot structure, state/save model, testing and platform targets |
| `docs/06_ART_FIRST_PRODUCTION_PLAN.md` | The mandatory artwork-first workflow, asset approval gate and QA |
| `docs/07_AUDIO_AND_ACCESSIBILITY.md` | Sound plan, settings, readability and inclusive interaction rules |
| `docs/08_MILESTONES_AND_TEST_MATRIX.md` | Gates, schedules, pass/fail checks and Definition of Done |
| `docs/09_VISUAL_CREATION_PROMPTS.md` | Specific prompts and specs for creating original assets, not web copying |
| `manifests/asset_manifest.csv` | Trackable asset batches and acceptance criteria |
| `checklists/ART_APPROVAL.md` | Signoff checklist: deliberately **not signed** |
| `art_references/*.png` | Original generated concept examples: **visual direction only** |

## Critical distinctions

- The art boards are original concept references, **not** tested runtime captures, production sprite sheets, collision maps, UI truth or licensed third-party art.
- Any tiny typography/labels inside generated boards may be inaccurate. The text specifications are authoritative.
- The art references show an illustrative rich pixel-art look; finished game art must have true pixel-grid consistency and verified transparent PNG sprites where necessary.
- All game design content in this package is a **proposed specification** subject to creative approval; confirmed direction is the tonal blend and request for art-first planning.
- Existing source/license obligations remain: inspect reused assets, including any Sprout Lands materials, before reuse; don't silently strip credits or redistribute restricted art.
- This kit contains **no game code**, does not modify the existing Godot project, and does not resolve deployment blockers.

## License and privacy

Original generated imagery is supplied as concept material for this private project. Don't paste private conversations, personal identifiers, private relationship material or copyrighted movie/game imagery into public source. Use entirely original final art or documented properly licensed assets. Third-party reference links (if consulted) are inspiration only, not permission to copy.
