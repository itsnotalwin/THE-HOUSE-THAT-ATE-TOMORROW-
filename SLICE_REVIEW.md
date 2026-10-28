# First playable chapter review

**28 October 2026 · Godot 4.6.3 · Street + Entrance Hall**

The approved Candlelit Registry direction is now a playable chapter. Read the Department letter outside the house, meet Fig, and register as a guest. The mirror reveals The Almost; the portrait supplies the title the Guestbook needs. Solving the puzzle produces a warning notice and opens the first doors. Entering an opened door reaches the chapter-end panel.

This is the scope authorized after [art approval](ART_APPROVAL_RECORD.md). The Kitchen, Library, later rooms, remaining puzzles, and endings are future work. The 8–10 minute duration is a design target, not a measured human playtest result.

## Run locally

Use **Godot 4.6.3** to open `project.godot` and run the project, or:

```sh
godot --path .
```

With the matching export templates installed, regenerate the local review builds:

```sh
mkdir -p builds/web builds/linux
godot --headless --path . --export-release Web builds/web/index.html
godot --headless --path . --export-release Linux builds/linux/the-house-that-ate-tomorrow.x86_64
```

The Web preset uses WebGL 2 and a single-threaded engine. Serve its folder over HTTP:

```sh
python -m http.server 8000 --directory builds/web
```

Open `http://localhost:8000/`. The Linux build runs with:

```sh
./builds/linux/the-house-that-ate-tomorrow.x86_64
```

In the managed workspace, writable engine state is available by prefixing Godot commands with `XDG_DATA_HOME=/workspace/.runtime XDG_CONFIG_HOME=/workspace/.runtime/config XDG_CACHE_HOME=/workspace/.cache`. Local users can use their normal writable user-data directories. Builds are ignored by Git and must be regenerated in a fresh checkout. No site has been deployed.

## Controls and assistance

| Action | Control |
| --- | --- |
| Move | WASD / arrows |
| Inspect nearby object or talk | E / Enter |
| Continue a dialogue line | E / Enter, or the Continue button |
| Switch Here / Almost | Space / Tab, after Fig gives the mirror |
| Notebook, inventory, and hint button | N / I |
| Pause or leave an ordinary panel | Escape |
| Navigate choices | Arrows / Tab, then Enter; or mouse |

Movement pauses while a dialogue or menu is open. Required conversations must be completed so their rewards are recorded. Dialogue never disappears on a timer. Wrong Guestbook choices can be retried. Hints progress from a general suggestion to the exact answer, and do not solve the puzzle automatically.

Settings provide standard/large reading text, reduced ambient motion, and master/music/effects controls. All clues and actions have visible text; sound is supportive. The Here and Almost loops crossfade; rain is mixed with the music/ambience level. [Audio provenance and measurements](assets/AUDIO_PROVENANCE.md) describe the original synthesis.

## Saving

One chapter slot stores room, position, mode, learned clues, completed conversations, puzzle state, hint tier, and settings. It saves after milestones, every 15 seconds during exploration, on focus loss, and before returning to the title. New Game asks before replacing existing progress. Continue restores the saved chapter.

Progress uses `user://house_slice_save.json`, with a validated `.bak` recovery copy. A new snapshot is written and verified before replacing the primary file; malformed saves are rejected before updating live state. Preferences additionally use `user://house_slice_settings.cfg`, so changing title-screen settings does not create a false Continue slot. In browsers, Godot's user data is stored for that browser origin; use the same browser profile and local URL to resume.

## Verification evidence

| Check | Recorded result |
| --- | --- |
| State and save tests | 52 assertions passed: prerequisites, wrong answers, mode gates, save validation, backup recovery |
| Coordinator regressions | 12 assertions passed: preferences without progress, Continue audio context, restart cancellation, malformed preferences |
| Chapter integration | 92 assertions passed: actual scene/input/dialogue callbacks, notebook and pause blocking, clue/puzzle/notice flow, disk save and Continue |
| World checks | Target approaches, collision overlap, mode position stability, and disabled movement are covered by `test_world.gd` |
| Browser evidence | Chromium/WebGL 2: title, street-to-hall route, mirror, portrait, Almost, Guestbook rejection and acceptance, saved progress and a 960 × 540 notebook and choices; no game console errors in the final capture |
| Independent human playtest | Not performed; pacing and first-time puzzle clarity remain review items |

Run the automated checks from the repository root:

```sh
godot --headless --path . --script tests/test_state.gd
godot --headless --path . --script tests/test_coordinator_regressions.gd
godot --headless --path . --script tests/test_world.gd
godot --headless --path . --script tests/test_slice.gd
sha256sum -c PACKAGE_FILES_SHA256.txt
python art_staging/source/validate_art.py
```

The chapter integration test moves between declared safe interaction approaches to exercise progression. It does not prove that a first-time player can navigate every route unaided. Browser walkthroughs and runtime screenshots provide separate visual/input evidence; headless tests do not certify rendering or audible output.

Actual screenshots available for review include the [title](qa/runtime/01-title.png), [street](qa/runtime/02-street.png), [hall in the Here](qa/runtime/08-portrait-here.png), [hall in the Almost](qa/runtime/09-hall-almost.png), and [Guestbook choices](qa/runtime/22-interaction.png). Earlier studies under `art_staging/review/` are artwork, not runtime evidence. Files named `SCREENSHOT.png` in maintained implementation folders must be copies of a verified runtime capture.

The Linux export starts successfully in a headless smoke run. Forced headless shutdown emitted Godot audio-backend ObjectDB cleanup warnings; a minimal looping-audio scene reproduced them, and the orderly test teardown is clean. Native display and listening have not been tested here.

## Review limits and acceptance

This chapter targets desktop keyboard and mouse. Controller, touch/mobile, Windows/macOS exports, assistive-technology compatibility, and independent usability testing are not certified. Automated audio checks establish file validity and runtime state; they do not substitute for a human listening pass on speakers or headphones.

Review the movement and interaction reach, Here/Almost readability, dialogue and notebook text, hint usefulness, and Continue behavior. After reviewing the playable chapter, `SLICE APPROVED` records acceptance to proceed with the next room. That acceptance does not authorize deployment; publication requires a separate instruction.
