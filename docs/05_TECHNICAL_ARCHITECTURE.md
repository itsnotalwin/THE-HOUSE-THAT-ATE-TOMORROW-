# 05 — PROPOSED TECHNICAL ARCHITECTURE (ONLY AFTER ART APPROVAL)

## Ground rules

The source game lives in `itsnotalwin/Innate`. The vault note currently records an experimental Godot 4.6.3 game with unresolved default branch / Pages deployment questions; inspect actual repo status before modifications. Never overwrite existing work on a guess. The user wants **asset production before game implementation**; the technical architecture here is a future blueprint, not permission to start coding now.

### Repository preflight (read-only)

- Inspect existing `AGENTS.md`, `PROJECT.md`, root structure, `project.godot`, main scenes, art licenses, build/export workflow, GitHub Pages config and current default branch.
- Read the authoritative vault build standard at `itsnotalwin/obsidian-vault` `99_System/BUILD-STANDARDS.md` and project-local instructions if accessible.
- Report what is reusable, what would be replaced, and any contradictory older project architecture. Don't change code, scenes, CI or assets without an explicit approved implementation stage.
- Work on an appropriately isolated branch when changes are approved, with a named baseline commit and no force pushes.

## Godot architecture proposal

```text
AGENTS.md                         (portable build rules)
PROJECT.md                        (entry point and how to run)
project.godot
art_staging/                       (ART PHASE ONLY, not imported as finalized game assets)
    CONTEXT.md
    concept/                       (+ CONTEXT.md, DESIGN.md; concept images are NOT SCREENSHOT.png)
    review/                        (+ CONTEXT.md, DESIGN.md; contact sheets)
assets/                            (after approved production work)
    CONTEXT.md
    characters/                    (+ CONTEXT.md, DESIGN.md, actual runtime SCREENSHOT.png once implemented)
    environment/                   (+ CONTEXT.md, DESIGN.md, actual runtime SCREENSHOT.png once implemented)
    ui/                            (+ CONTEXT.md, DESIGN.md, actual runtime SCREENSHOT.png once implemented)
    audio/                         (+ CONTEXT.md)
scenes/
    CONTEXT.md
    menus/                         (+ CONTEXT.md, DESIGN.md, runtime SCREENSHOT.png)
    gameplay/                      (+ CONTEXT.md, DESIGN.md, runtime SCREENSHOT.png)
    rooms/                         (+ CONTEXT.md, DESIGN.md, runtime SCREENSHOT.png)
scripts/
    CONTEXT.md
    core/                          (+ CONTEXT.md)
    puzzles/                       (+ CONTEXT.md)
    ui/                            (+ CONTEXT.md, DESIGN.md, runtime SCREENSHOT.png where visual)
data/
    CONTEXT.md
    dialogue/                      (+ CONTEXT.md)
    puzzles/                       (+ CONTEXT.md)
tests/                             (+ CONTEXT.md)
```

The exact tree must adapt to the current repository. New authored folders must receive `CONTEXT.md` immediately. UI/visual source folders additionally need `DESIGN.md` and a genuine current running `SCREENSHOT.png` **only after runtime exists**. A concept board never counts as actual in-engine evidence. If runtime evidence is impossible, leave the gate failed and document the blocker honestly, not a fake screenshot. Root must have `PROJECT.md` and `AGENTS.md`.

## Responsibilities and APIs (design, not code)

- `GameState`: versioned global flags, inventory and visited/solved room states. Serializable to JSON/binary save with explicit migration strategy.
- `RoomController`: loads scene, entrance marker, room-specific lighting and ambient sound, loads flags without duplicate rewards.
- `ModeController`: toggles Here/Almost, emits mode-changed signal, swaps authored visible/interactable state; preserves base collision.
- `InteractionResolver`: nearest visible eligible interactive, consistent prompt and action; no blind clicking.
- `PuzzleManager`: data-driven requirements, conditional clues, state transition and output. Puzzle IDs stable, actions idempotent.
- `DialogueRunner`: branching small conversation trees with conditional topics and hint tiers; keyboard/controller focus safe.
- `NotebookManager`: discovered clues, tasks, room summaries and hint log from source of truth GameState.
- `InventoryManager`: quest item acquisition/use, non-drop rules, unique item IDs.
- `SaveManager`: auto on scene transition / major solution / before ending, one or more recoverable slots, version stamp, checksum/error fallback as feasible; do not write temp file then overwrite valid without durability checks.
- `AudioDirector`: ambient room transitions, music cues, mode filtering, bus volume settings.
- `UIRouter`: pause, notebook, inventory, dialogue and settings priorities; no overlay collisions.

### Example state schema

```json
{
  "schema_version": 1,
  "current_room": "entrance_hall",
  "spawn_marker": "hall_from_street",
  "mode": "HERE",
  "player": {"x": 120, "y": 176, "facing": "north"},
  "flags": {"intro_letter_read": true, "fig_met": true, "almost_unlocked": false},
  "inventory": [],
  "clues": [],
  "hint_tiers_seen": {},
  "tokens": [],
  "ending": null,
  "play_seconds": 95
}
```

This is illustrative JSON schema only. Actual save code must validate load and migrate older versions safely. If older repository format exists, provide adapter/backups rather than wiping saves.

## Data ownership and behavior

- Dialogue and puzzle data separate from scene scripts where reasonable for writers/testers.
- Content paths relative to project; no remote internet requirements at runtime.
- Every prop has `object_id`, `room_id`, modes present, inspect text, optional flag condition, collision metadata, animation state.
- The Almost palette/lighting should be per-room layered state, with mode-specific interactable IDs. Every puzzle interaction logs ID and flag in dev builds to diagnose blocked routes.
- Player movement frame independent; collisions generous; transitions asynchronous without input-spam. NPC positions cannot block doors.
- Runtime may support local browser storage, but test actual restrictions of Godot Web export and origin changes. No false claims that browser saves are permanent across devices.

## Asset pipeline (after art approval)

- Convert only signed-off art sheets from `art_staging/` into `assets/` for runtime use. Keep provenance + license + import settings in manifest.
- PNG with RGBA and pixel-grid nearest filtering; fixed spritesheet cells; trim/padding metadata and anchors; no automatic lossy rescaling.
- Automatically validate dimensions, 4 directions, transparency, palette compliance tolerances, duplicate filenames and existence before importing.
- Stage art review with output PNG files first. A standalone Python Pillow or Aseprite conversion helper is permitted during ART phase; runtime gameplay/scene coding is not.

## Editor/export and CI

- Godot headless editor parse/import smoke, script check, asset missing refs, startup smoke.
- Unit/data tests for puzzle transitions, solvability and save/load flags; static dialog reference validation.
- Export Windows if supported in environment; export Web to an isolated build path; run in browser for true keyboard/audio/local persistence/performance testing.
- GitHub Actions status is not equal to live Pages verification. Repo note says the prior artifact checks passed while deploy jobs failed; confirm any future repair explicitly before claiming deployment.
- Aim for typical laptop playable 60fps when feasible, zero game-breaking warnings/errors, no major load spikes between small rooms; test actual target, don't claim from static lint.

## Security, privacy and attribution

No telemetry, account system or analytics needed. No secrets in repository. No private chats, intimate details or third-party personally identifying records inside public assets. Avoid direct use of copyrighted game art and soundtrack. Maintain credits and license metadata for any approved third-party dependencies. Don't assume removal of credit on a title screen solves license obligations.

## Ready to implement when...

Only when the user has approved art package AND its technical resolution: approved palette, environment reference, Visitor/fig sprite cells and playable UI size; art manifest status `APPROVED`, source branch baseline selected, architectural differences reviewed, and vertical slice tasks explicitly authorized. No ambiguous auto-continue.
