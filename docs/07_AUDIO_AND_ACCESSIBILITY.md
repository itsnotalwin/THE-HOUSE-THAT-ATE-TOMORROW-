# 07 — AUDIO, ACCESSIBILITY, UX AND SETTINGS

## Sound direction

The Here: soft lo-fi chamber/piano and plucked/string motifs, kettle hiss, candle crackle, rain, floorboards, warm room tone. The Almost: softened spectral bells, airy doubled notes, occasional low reversals and echo; retain soothing sound bed. Comedy: quiet percussive blips tailored to characters, never cartoon soundtrack spam. Auditor: precise paper clicks, subtle clock clicks and restrained dissonance.

**Cue inventory:** `title_theme`, `street_rain_loop`, `foyer_loop`, `kitchen_loop`, `library_loop`, `greenhouse_loop`, `mirror_loop`, `attic_loop`, `ending_open`, `ending_secret`, `almost_toggle`, `object_inspect`, `item_collect`, `door_unlocked`, `puzzle_success`, `puzzle_try_again`, `dialogue_confirm`, `menu_focus`, `page_flip`, `clock_tick`, `cat_meow_quiet`, `kettle_steam`, `plant_bloom`, `auditor_papers`.

- Loop seams must be tested. Music fades rather than hard cuts; never reset the loop with every mode toggle.
- Mix levels: dialogue reading sound under effects, effects below music where appropriate, ambient layers soft. User-adjustable sliders for master/music/SFX/ambience.
- All game information must be visible in text or graphic form, never exclusively through sound.
- **Audio sourcing:** use original audio or licensed tracks with license and file credit record. Don't rip music from existing games. Prefer restrained original generated/recorded samples over generic loud packs.

## Accessibility and comfort baseline

- Text speed: slow/standard/instant. Optional reveal-all/skip previously read dialogue. Never require speed-reading.
- Font size: dialogue UI scaling slider or at least 2 readable choices, test at 1366×768 and 1920×1080 at browser 100%; minimum effective ~16px common text.
- Color-vision: icons and labels for Here/Almost, patterns in puzzles, contrast-aware text/focus, no pure-color-only clue.
- Reduced motion: turn off screen wobble/chromatic shift/vignette pulse; use clean crossfade for Almost. Avoid flash/strobe.
- Photosensitivity: avoid abrupt full-screen flashing, especially during clock scene.
- Motor: no reaction timers, rapid repetitive clicking, fine cursor precision or hold-to-activate requirements.
- Keyboard: all menus, notebooks, choices and inventory accessible without mouse; clear focus indicators.
- Controller: map inputs consistently and show device prompts; controller testing gate if controller advertised.
- Pause/focus: pause correctly on menu; browser losing focus should not trigger movement or input repeat, and gameplay must resume cleanly.
- Sound: independent volume controls, mute allowed, subtitles/text for all crucial cues.
- Interface responsiveness: avoid essential UI beyond safe viewport; scale from 16:9 while keeping readability on narrower windows.
- Save: autosave progress on puzzle completion, doors/hubs and pre-ending; show save acknowledgment; do not lose progress on close.

## Product-facing presentation

Main menu: `Continue` (disabled if absent), `New Game`, `Settings`, `Credits`, `Quit` (desktop only; browser can hide), with an original title illustration. `Start New` confirmation if save overwrite. Logo needs vector or pixel-consistent rendered original type; avoid title screen plagiarism.

During play: one current objective, clear interaction prompts, optional notebook marker, understated mode indicator. Pause: Resume, Notebook, Settings, Return to Title with save caution. Error messages plain and actionable (missing asset, save invalid fallback). Credits identify contributors/asset licenses honestly.

## Usability check

5 uncoached testers ideal, 3 minimum before calling vertical slice accepted. Observe: first 2 minutes objective comprehension; independent mode discovery; interaction affordances; first puzzle solve time; ability to open notebook/hints; contrast and text. Ask participants separately: “What are you trying to do?”, “What did switching worlds change?”, “What was confusing?”, “Would you play another room?” No prompts until they are clearly stuck and voluntarily use a hint.
