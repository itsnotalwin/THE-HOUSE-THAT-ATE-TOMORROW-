# The House That Ate Tomorrow

*Tomorrow is missing. The cat denies everything.*

A cozy-gothic narrative puzzle adventure about a house that collects things that almost happened. The first playable Godot chapter covers the **Forgotten Street and Entrance Hall**: meet Fig, acquire the pocket mirror, explore The Almost, solve the Guestbook puzzle, and discover the first warning notice.

The user approved the original artwork on 27 October 2026. [Art approval](ART_APPROVAL_RECORD.md) records that decision and the authorized slice scope. The selected Candlelit Registry hall now runs in-game; the remaining rooms await separate slice acceptance.

## Play the chapter

Open [`project.godot`](project.godot) in **Godot 4.6.3** and press **F6** with `scenes/main.tscn` open, or press **F5** to run the project. From a terminal:

```sh
godot --path .
```

The local Web export lives in `builds/web/`. Serve it over HTTP, then open `http://localhost:8000/` in a browser with WebGL 2:

```sh
python -m http.server 8000 --directory builds/web
```

Do not open `index.html` directly with `file://`. Builds are local review artifacts, ignored by Git. Export commands, test coverage, known limits, and review guidance are in [SLICE_REVIEW.md](SLICE_REVIEW.md).

| Action | Control |
| --- | --- |
| Move | WASD or arrow keys |
| Inspect / speak | E or Enter |
| Advance dialogue | E or Enter; click Continue |
| Reveal The Almost | Space or Tab, after obtaining the mirror |
| Notebook and inventory | N or I |
| Pause / close a panel | Escape |
| Choose a dialogue option | Arrow keys / Tab, then Enter; or click |

Dialogue waits for you. Settings include standard/large reading text, reduced ambient motion, and separate master, music, and effects levels. Progress autosaves at milestones and during exploration; Continue restores the room, position, clues, and puzzle state. Preferences are stored separately from progress.

## Review evidence and source

Start with the [slice review](SLICE_REVIEW.md), [actual title screenshot](qa/runtime/01-title.png), and [actual street screenshot](qa/runtime/02-street.png). Runtime evidence lives under `qa/`; the earlier illustrations and UI studies remain under `art_staging/review/`.

| Path | Contents |
| --- | --- |
| `scenes/`, `scripts/`, `data/` | Godot scene, gameplay/UI/audio code, room geometry, and dialogue |
| `assets/` | Approved production copies, original street art and audio, bundled font license |
| `tests/` | State, coordinator, world, and chapter integration checks |
| `tools/` | Reproducible street-art and audio generators |
| `qa/` | Actual runtime captures and verification context |
| `art_staging/` | Original art sources, exports, metadata, studies, and validation |
| `docs/`, `art_references/`, `manifests/`, `checklists/` | Preserved supplied preproduction handoff |

The [art manifest](art_staging/manifest.csv) records original art deliverables. The [approved production manifest](assets/approved_manifest.csv) records the selected copies. The original 82-row backlog and unsigned supplied checklist remain unchanged historical inputs; they do not describe current approval or implementation status.

## Verify

```sh
sha256sum -c PACKAGE_FILES_SHA256.txt
python art_staging/source/validate_art.py
godot --headless --path . --script tests/test_state.gd
godot --headless --path . --script tests/test_coordinator_regressions.gd
godot --headless --path . --script tests/test_world.gd
godot --headless --path . --script tests/test_slice.gd
```

Art validation requires Python 3 and Pillow. See the [art report](ART_REVIEW_REPORT.md#reproduce-the-exports) for reproduction details, and [project status](PROJECT.md) for the current milestone.

## Supplied design and repository identity

The [handoff overview](README_START_HERE.md), [game design](docs/01_GAME_DESIGN_DOCUMENT.md), [art bible](docs/02_ART_DIRECTION_BIBLE.md), [puzzles](docs/03_WORLD_AND_PUZZLES.md), and [story](docs/04_STORY_AND_DIALOGUE.md) describe the proposed full game. Instructions inside those documents are project references; the user's live requests determine authorized work.

This checkout's configured remote is [`itsnotalwin/THE-HOUSE-THAT-ATE-TOMORROW-`](https://github.com/itsnotalwin/THE-HOUSE-THAT-ATE-TOMORROW-). Historical references to `itsnotalwin/Innate` and a private knowledge vault have been preserved. Those repositories have not been inspected or modified. This chapter has not been published or deployed.
