# 03 — WORLD, ROOM GRAPH, PUZZLES AND STATE RULES

## 1. Geography: seven authored locations

World locations are discrete connected maps, not an uncontrolled seamless megamap. The main hub is Entrance Hall. Each location has authored obstacles and a Here/Almost interaction layer. Exits show an entry silhouette and are not hidden behind indistinguishable walls.

```text
                         [Attic Clockroom]
                                ^
                          [Mirror Hallway]
                                ^
 [Forgotten Street] -> [Entrance Hall] -> [Crooked Kitchen]
                                |                  |
                                v                  | (tea clue)
                      [Unwritten Library] <-------+
                                |
                                v
                      [Moonlight Greenhouse]
```

This is a dependency drawing rather than literal floor adjacency. Prefer a readable hub with distinct doors: Kitchen and Library open after Guestbook; Greenhouse route from Library after tea; Mirror Hallway from Entrance Hall after evidence; Clockroom from Mirror Hallway after reflection sequence. Backtracking must be short, rewarding and explained by NPC movement/updated props.

### Proposed room dimensions (refine after scale mockup)
- Forgotten Street: 48 × 24 tiles (768 × 384 world pixels) with camera pan.
- Entrance Hall: 32 × 22 tiles (512 × 352 px), visual hub.
- Kitchen: 28 × 20 tiles (448 × 320 px).
- Library: 40 × 24 tiles (640 × 384 px), shelves form navigable mini-aisles.
- Greenhouse: 32 × 24 tiles (512 × 384 px).
- Mirror Hallway: 30 × 18 tiles (480 × 288 px), symmetrical illusion.
- Attic Clockroom: 34 × 22 tiles (544 × 352 px).

All these are *targets*, not technical measurements taken from the old repo. Adapt if a user-tested 384×216 viewport cannot clearly show puzzle objects.

## 2. Global progression state names

Use stable, namespaced IDs; trigger transitions atomically after animation/dialogue completion; save flag changes before room transition.

| Flag | Initial | Set when | Unlocks |
|---|---|---|---|
| `intro_letter_read` | false | Inspect opening letter | Arrival objective |
| `fig_met` | false | Finish intro conversation | Basic controls hint |
| `almost_unlocked` | false | Receive Fig's pocket mirror | Mode toggle |
| `guestbook_solved` | false | Sign valid guest title | Hall, Kitchen, Library |
| `erasure_notice_read` | false | Read red notice after foyer puzzle | Major stakes journal |
| `tea_brewed` | false | Complete tea recipe | Hidden ink note |
| `thimble_helped` | false | Restore unwritten book order | Library evidence |
| `crumb_helped` | false | Bloom moonflower, talk to Crumb | Greenhouse evidence |
| `mabel_confessed` | false | Greenhouse/Library confrontation | Mirror Hall access |
| `mirror_solved` | false | Complete hallway sequence | Attic access |
| `evidence_complete` | false | Library + greenhouse + erasure notice | Auditor challenge |
| `clock_restarted` | false | Finish final assembly | Ending choice |
| `final_choice` | `unset` | Choose `open` or `secret` | Ending + epilogue |
| `keepsake_01..05` | false | Optional discoveries | Epilogue flavor |

Make flags explicit, versioned and idempotent. Reopening a solved puzzle displays changed room state and optional line; it must not respawn already collected items.

## 3. Puzzle design contract

Every puzzle page below specifies: visible problem; learnable clue; Almost interaction; solution; feedback; post-solve state; recovery; hints. Codex must implement **those conditions**, not use arbitrary locks or 'press interact to complete'. Allow inspection in any order where reasonable. No one-time missed clue, strict timer or punishment. If key item is not in inventory, corresponding hotspot remains discoverable. Repeated actions should be safe.

### P1 — The Guestbook (Entrance Hall, tutorial; 4–6 min)

**Problem:** A thick book politely refuses to record the Visitor's ordinary name. The entry door locks behind the Visitor, but leaving the map is never essential to solve the puzzle.

**Clues:** Fig explains the house only admits “someone who might have arrived”; a painting shows a blank nameplate; inspecting guestbook states “The expected guest has no written name.” In The Almost, ink appears reading **THE VISITOR** on an otherwise empty nameplate.

**Action path:** Talk to Fig -> obtain a small pocket mirror / `almost_unlocked` -> toggle -> inspect glowing nameplate -> add notebook entry `clue_guest_title` -> return to Here -> interact guestbook -> choose `The Visitor` from 3 reasonable names (other two can be funny wrong options with feedback). Selection remains possible in either mode if clear.

**Solution:** Correct selection writes guest title, book slams contentedly; `guestbook_solved = true`; the hall lamp ignites, doors unlock, Fig says “You'll do. Probably.” A red departmental warning appears on the noticeboard (`erasure_notice_read` obtained by inspecting). Keep the hall accessible and save at solve.

**Hints:** (1) “The book expects a kind of guest, not a name.” (2) “Look at the portrait in The Almost.” (3) “Use the title THE VISITOR.”

**Recovery:** No consumable items. Wrong option creates short line, no reset. If player shifts mid-dialogue, disallow shift until dialogue finishes and show a cue. A return path always exists.

### P2 — The Impossible Tea (Crooked Kitchen; 5–7 min)

**Problem:** A handwritten recipe has missing ingredients; Mabel needs tea to make an invisible message visible on a letter. The kettle doesn't want tap water.

**Clues:** Cup says “hot water and a memory of rain”; pantry tin is labeled for ingredients but its label is blank in Here. In Almost, label reveals `moonleaf`, and the old window contains animated ghost rain; inspecting ghost rain notes it can be captured in a cup. Mabel mentions “No sugar. Our accountant is already sweet enough.”

**Action path:** Read recipe (`tea_recipe_seen`) -> find plain cup on shelf (reusable key item) -> toggle and catch ghost rain at window (`ghost_rain_captured`) -> discover `moonleaf` in The Almost pantry cupboard -> return Here and place leaf + ghost rain at kettle -> choose brew (with feedback for incomplete combination) -> offer cup to Mabel or apply to sealed letter.

**Solution:** Tea makes hidden ink on the letter legible; receive `clue_department_seal`, set `tea_brewed = true`; next Library clue indicated. Mabel moves to the central hall when the stage ends.

**Hints:** (1) “The recipe is not telling the whole truth.” (2) “Try the pantry and window in The Almost.” (3) “Collect ghost rain and moonleaf, then use the kettle.”

**Recovery:** Cup never lost. If tea is offered to wrong item, gently refuse, return cup. No failed-brew resource drain. Clear item names remain in inventory.

### P3 — The Unwritten Library (Library; 7–8 min)

**Problem:** Miss Thimble guards a locked archive because her shelves contain stories in the wrong order. Three spectral book spines show fragmentary descriptions of impossible events.

**Clues:** Desk card reads “Before the cause, there was the consequence; before the promise, a wish.” This is intentionally abstract, so illustrations and dialogue must clarify the sequence, not demand poetic guessing. The books have distinct motifs: seed, sprout, blossom. In Here, covers seem blank. In The Almost, revealed titles are `A Wish Planted`, `A Promise Remembered`, `A Future Offered` and corresponding symbols. A framed timeline illustrates seed -> sprout -> blossom.

**Action path:** Inspect frame -> shift -> read titles/symbols -> use shelf UI to arrange three books in seed/sprout/blossom order. Player can reset/undo arrangement. Use spatial feedback on each successful placement. Thimble responds to progress.

**Solution:** Shelf rotates to reveal archive drawer holding `evidence_resident_registry`, set `thimble_helped = true`, unlock the greenhouse path. The registry shows names/roles of residents and why they belong.

**Hints:** (1) “Think growth, not dates.” (2) “Check the book symbols in The Almost and the frame in Here.” (3) “Order: wish/seed, promise/sprout, future/blossom.”

**Recovery:** Books never vanish. Wrong order triggers humorous Thimble comment, no hard failure. Reset returns books to clearly documented starting positions.

### P4 — The Moonflower (Greenhouse; 6–8 min)

**Problem:** A moonflower that documents the house's past won't bloom. Sir Crumb claims the flower is held hostage by a dangerous carrot.

**Clues:** In Here, a wilted moonflower has a reflective silver vein. In Almost, moonlit droplets appear in a raincatcher; a gardener's label says it needs `a promise` (spoken or written) as well as spectral moisture. A note from a former visitor uses the wording “I'll come back.” Sir Crumb can provide the note after resolving his carrot confrontation with a short harmless dialogue puzzle.

**Action path:** Talk to Crumb -> choose reassurance rather than threaten the vegetable (no irreversible wrong choice) -> receive `old_promise_note` -> shift -> collect phantom dew in vessel -> return Here -> place note beside flower and add dew -> bloom animation -> examine revealed memory imprint.

**Solution:** Register `evidence_caretaking`; learn Mabel tended the refuge for decades, and she recently hid tomorrow; set `crumb_helped = true` then stage Mabel's confession (`mabel_confessed = true` after dialogue). Hall Mirror access becomes available.

**Hints:** (1) “The flower seems to recognize something it was promised.” (2) “Ask Crumb about the note; inspect greenhouse in The Almost.” (3) “Place the old promise and phantom dew at the moonflower.”

**Recovery:** Dew capture always repeatable until used; note is marked quest-critical. Dialogue choices never permanently antagonize Crumb; player can continue conversation.

### P5 — The Last Minute (Mirror Hallway -> Attic Clockroom; 8–12 min total)

**Phase A / hallway:** Hallway has three mirrors reflecting room details inconsistently. In Almost, each reveals a single clear icon: `home`, `witness`, `tomorrow`; an earlier Auditor form in Here shows their reading order. Interact with the mirrors in that order, with progress tracked and mistake resetting only the sequence. No arbitrary physics tricks.

**Phase A result:** Door to Clockroom opens; `mirror_solved = true`. Existing evidence notebook entries clarify that the house qualifies for a special bureaucratic exemption only if it can prove residency, mutual care and free passage of time.

**Phase B / clockroom:** The clock has three empty stations: REGISTRY, CARE, and TIME. Put registry evidence in Registry station, moonflower/caretaking evidence in Care station, then interact with clock in The Almost to retrieve the sealed `tomorrow_gear` and return to Here to place it in TIME. Gear is not lost on mistakes.

**Precondition:** `evidence_complete` checks `erasure_notice_read && thimble_helped && crumb_helped` (and `tea_brewed` in intended route); if not, Auditor points to the missing evidence in an in-world way, with route back unlocked. No unexplained lockout.

**Outcome:** Clock restores movement. The Auditor agrees that tomorrow may resume if the home is properly registered. Set `clock_restarted = true` and choose either `open` or `secret`, generating two equal-quality epilogues. The reason the exception works must have been foreshadowed in the Library registry and Auditor paperwork before the final scene.

**Hints:** (1) “The mirrors are arguing about the order.” (2) “The form names the sequence; The Almost reveals the symbols.” (3) “Mirror order HOME > WITNESS > TOMORROW. Then assign resident registry, proof of care, and tomorrow gear to matching stations.”

**Recovery:** Can enter/exit Clockroom until final choice; no missing single-use key. Keep a checkpoint before choice and allow replaying the ending from title after game completed.

## 4. Traversal and locked-door design

Main plot order: Start -> P1 -> (Kitchen P2 and optional Library inspect) -> P3 -> P4 -> Mabel confession -> P5A -> P5B -> choice. The player may revisit open areas for optional details; no forced repeated 10-minute walks. Hall shortcuts or short door transitions are favored over long empty corridors.

**Door messaging:** Show `Locked: someone seems to be reading in there` plus notebook objective, rather than generic “Locked.” Doors unlock visibly with unique short animation and audio. No door should vanish silently.

**Map states:** A room may have `UNVISITED`, `VISITED`, `ACTIVE`, `RESOLVED`; map entry always stable; solved-state interaction changes authored visual pieces, not underlying logical map structure. Every doorway has spawn markers in both directions.

## 5. Optional finds (not blocking)

1. Paperclip wearing a tiny crown in foyer; Fig claims it's a prince.
2. An apology note to a kettle in Kitchen.
3. Book titled “How to Win Arguments With Dust” in Library.
4. A ceremonial carrot medal in Greenhouse.
5. Mirror that briefly reflects Fig as a human civil servant (visual gag only).

Keep safe for a personal gift: secrets should be original world-building and not unapproved private messages. Finding all tokens unlocks a short cast reunion vignette, not a major ending.

## 6. Room content contract

For each location, Codex must produce a room data sheet containing: map bounds, spawn/exits, tile layers, collision layer, audio zone, light pools, inspectable list with lines, NPC spawns/conditional routes, puzzle hotspots, Here/Almost differences, scene state conditions, optional token, performance budget and test cases. Each mode needs a labelled mockup before level construction and a real running screenshot afterward.

## 7. Softlock / consistency invariants

- Key quest items persist through save/load; can't be discarded.
- A required puzzle always has all its clue sources accessible in its current progression state.
- Switching reality never strands or damages the player.
- Doors cannot permanently lock behind a player without another route to solve current objective.
- Exiting mid-dialogue or saving mid-room cannot duplicate rewards or lose flags.
- NPC movement changes do not block doorways; unique NPCs have safe fallback spawn paths.
- Repeated activation of any solved puzzle is harmless and does not re-award unique items.
- Hints reflect the exact unsolved puzzle state; never point at a completed challenge.
- The final ending choice has a save checkpoint, replay, and a way back to title/credits.
