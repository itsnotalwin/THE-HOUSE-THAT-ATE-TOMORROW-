# 08 — MILESTONES, ACCEPTANCE TESTS AND QUALITY CONTROL

## Decision gates — explicit approval required

| Stage | Deliverable | Pass condition | Authorization |
|---|---|---|---|
| M0 | Read-only repo inventory, risk, licensing and art plan | Correct current status, safe branch plan, no code changes | Planning request permits read-only investigation |
| M1 | Art boards, room pair, real sample sprites/tiles/UI, asset manifest | Original usable assets pass grid, alpha, scale and cohesion tests | **User must explicitly approve art** |
| M2 | Playable 8–10 minute street + foyer slice | All slice tests below pass in editor + actual exported browser | **User must explicitly accept slice** |
| M3 | Rooms Kitchen/Library/Greenhouse/Mirror | Main P2–P4 and hallway sequence solvable, content consistency | Approved DEV scope |
| M4 | Attic, ending variants, sound, save/UX | All progress/ending branches and settings tested | Approved DEV scope |
| M5 | Candidate release + visual/credits/accessibility QA | Real environment/browser verifications, no blockers | **User approves release/deploy** |

**Indicative work ordering**, not calendar promises: M0 -> M1 -> review -> M2 -> review -> M3 -> M4 -> M5. Avoid time estimates that create false deadlines. Keep progress as explicit commits/PRs with verified file lists.

## M1 art test matrix

- [ ] Art package contains concept and **production-suitable** original PNGs, not only AI composites.
- [ ] Exactly documented world tile size, character cell size, frame counts, direction order and anchor coordinates.
- [ ] Transparent assets really have alpha; no checkerboard baked in, no bright halo, no cropped limbs or frame bleed.
- [ ] Atlas tiles align perfectly to 16px without gaps, using nearest-neighbor upscaling and correct padding.
- [ ] Sprite readability tested 1×, 2×, 4× and in a simulated 384×216 gameplay crop.
- [ ] Here vs Almost room comparison retains spatial objects while changing clues, atmosphere and meaning.
- [ ] At least two visual variants and justified selected direction, with honest weak points.
- [ ] UI dialogue text comfortably readable at 1366×768 browser viewport.
- [ ] Source/licensing log for every non-self-created asset. No unauthorized asset pack copying.
- [ ] User explicitly said `ART APPROVED`; signoff checklist contains decision date and revision ID.

## M2 vertical slice test matrix

- [ ] Launch -> title -> new game -> player walking within 45s, coherent transition and no dead blank screen.
- [ ] Movement normalized diagonally; collisions match objects; no camera void or blurry pixel scroll.
- [ ] Fig interactable, correct portraits and quest dialogue; all input methods advertised work.
- [ ] `The Almost` toggle reveals invisible nameplate and clearly changes room/audio without making clues illegible.
- [ ] Guestbook cannot finish without correct clue logic, but can be solved after clue and responds to mistakes.
- [ ] Fig's 3 hint tiers give progressively useful non-spoiler prompts.
- [ ] Puzzle resolves, red erasure warning appears, doors unlock, and a satisfying world response occurs.
- [ ] Save/load preserves solved puzzle, inventory, clue log, room and mode; reopening does not duplicate rewards.
- [ ] No crash/softlock after repeated toggles, interacting during doors/dialogue, pause/resume and repeated puzzle activation.
- [ ] Real gameplay screenshots captured at desktop viewport and browser; no concept mockup labeled runtime evidence.
- [ ] Editor headless parse has no relevant errors, exports create expected files; browser verified by actual launching, not only CI.
- [ ] At least three first-time testers can explain goal, discover toggle and solve or intentionally request hints; list observed confusion.
- [ ] Art style consistently applied; no leftover rough placeholders without clear disclosed status.

## Full game functional matrix

| Test | Setup | Expected result |
|---|---|---|
| New game | No save | Intro begins with playable controls; Fig appears |
| Early save | Before Guestbook solved | Reload remains before puzzle, clue state preserved |
| Solved puzzle reload | After P1/P2/P3/P4/P5 each | Completion persists, no duplicate item or NPC |
| Shift spam | Any room, repeated rapid input | Stable mode, no invisible collision traps |
| Wrong combination | Any puzzle | Helpful feedback, retry allowed, no item lost |
| Cross-room inventory | Obtain then change rooms | Inventory retains correct item and use prompts |
| Missing evidence | Enter final route early | Auditor indicates what's missing, route home exists |
| Completion A | Solve final, Open Doors | Appropriate epilogue and credits, choice saved |
| Completion B | Solve final, Secret | Different full epilogue and credits, choice saved |
| NPC state updates | Revisit after plot changes | Dialogue and placement reflect current flags |
| Hint recovery | 3rd hint selected | Direct actionable guidance, no spoilers after solve |
| Notebook | Each clue obtained | Correct current task, no premature future clues |
| Focus loss | Switch tabs during movement | No stuck keys, sane pause/resume behavior |
| Resize | Common desktop resolutions | Letterbox/scale legibly, no cutoff controls |
| Audio mute | Master/music/SFX set zero | Silence in appropriate channels, retained setting |
| Reduced motion | Enabled | No excessive blur, wobble or flashing during shift |
| Keyboard only | Menu through ending | Full operation without mouse |
| Controller | If supported | Correct focus and prompts, no double activation |
| Broken save | Load corrupt slot | Safe recover/fail message; no unhandled crash |
| Licensing | Build assets scan | Every third-party asset properly attributed/licensed |
| GitHub Pages | CI passes and website opened | Actual exported game functional at published URL |

## Narrative/puzzle audit

- Every clue used by a puzzle is either observable, discussed or recorded earlier; no hidden dependency on a discarded object.
- Important choices and ending conditions are correctly previewed, explained and acknowledged.
- Mabel's confession reconciles earlier dialogue; Auditor's exception is explicitly foreshadowed.
- Every line of comic dialog fits the character voice and leaves appropriate serious beats intact.
- The Visitor and all NPCs remain visually consistent; no accidentally copied copyrighted characters.
- No unexpected external URL or tracking needed to finish the game.

## Definition of Done

Art fully approved; 7 rooms built and coherently decorated; 5 main puzzles pass tested logic; all 5 major NPCs have distinct arcs and readable dialogue; both complete endings; correct settings, UI, audio, notebook, hints, inventory, save/reload; PC+Web runs verified; licensed content recorded; folder documentation and real UI screenshots updated; remaining bugs tracked openly; final user signs off the release. Until then label `WIP` and report what remains.
