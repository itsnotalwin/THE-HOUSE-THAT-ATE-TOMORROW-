# Runtime scripts

The Street + Entrance Hall slice was authorized after explicit art approval on 27 October 2026. The current scope and acceptance status are recorded in `../PROJECT.md`, `../ART_APPROVAL_RECORD.md`, and `../SLICE_REVIEW.md`.

- `main.gd` coordinates scenes, input, conversations, notebook contents, rewards, saving, and chapter completion.
- `state.gd` is the `GameState` autoload. It owns progress, validates prerequisites and save payloads, and persists progress and independent preferences.
- `world.gd` renders the two authored rooms from `../data/`, builds collision, moves the Visitor, and selects reachable interaction targets. It reports targets without owning puzzle rewards.
- `ui.gd` renders title, HUD, dialogues, choices, notebook, settings, pause, credits, and chapter completion. It emits actions without owning progress.
- `audio.gd` manages original music/ambience loops and cues, including crossfades and volume settings.

Narrative and room data are external JSON. The four checks under `../tests/` cover persistent state, coordinator regressions, world geometry, and the complete chapter flow. The full-game handoff is reference material; it does not expand the current two-room scope.
