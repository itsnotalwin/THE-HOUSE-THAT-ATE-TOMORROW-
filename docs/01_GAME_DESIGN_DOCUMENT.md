# 01 — GAME DESIGN DOCUMENT (GDD)

**Selected display title:** The House That Ate Tomorrow  
**Tagline:** Tomorrow is missing. The cat denies everything.  
**Revision:** 1.1 / 2026-10-26 / name aligned; story and mechanics still proposed  
**Audience:** A personal game for Paige that should also be enjoyable on its own merits.  
**Genre:** Cozy-gothic narrative puzzle adventure, light exploration, whimsical mystery.  
**Platform priority:** Windows desktop and browser; keyboard and controller; mouse optionally; mobile only after verified usability and feasible export.  
**Engine target:** Existing Godot 4.6.3 project; verify actual repository and export configuration first.  
**Target runtime:** 40–50 minutes main path; optional 10–20 minutes of secrets (planning budget, not promise).  
**Perspective:** 2D top-down/three-quarter readable pixel-art environments; no perspective inconsistency between rooms.

## A. The player promise

A peculiar mansion has lost tomorrow. Explore its warm, unsettling rooms, shift between what is and what almost was, meet lovable eccentrics, solve fair environmental puzzles, and decide whether the house should remain hidden or welcome the world. Every five minutes should deliver one of: a genuine discovery, strong character moment, satisfying puzzle, striking room reveal, or a joke with real personality.

### Creative pillars, in priority order

1. **Curiosity is rewarded.** Inspectable props react; optional details reinforce setting, never bury the main objective.
2. **One memorable mechanic.** `The Almost` has clear before/after consequences, predictable controls, and no unexplained softlocks.
3. **Cozy is the baseline, spooky is the seasoning.** Mystery, tension and the uncanny without gore, unavoidable jump scares, or punishing chase sequences.
4. **Humor comes from earnest characters.** The game never winks at the player constantly; the cat takes bureaucracy seriously, the mouse takes vegetables seriously.
5. **Short but complete.** Strong opening, escalating clues, earned twist, satisfying conclusion; avoid open-world feature creep.
6. **Artistically cohesive.** Final in-game sprites must match a deliberate 16px pixel-grid system; reference boards do not excuse inconsistent scaling.

## B. Fiction and scenario

The impossible house collects unfinished possibilities: books that were never written, conversations never spoken, paths never chosen. It exists beside ordinary life, just out of notice. Tomorrow has been deliberately sealed in the attic clock. Without it, time outside is unable to pass normally near the mansion, and inhabitants inside begin to fade. Mabel did this to delay a scheduled shutdown by the Department of Unfinished Things, not out of malice. The Auditor believes anomalies must be closed for everyone else's safety. The player can investigate and present evidence that the house is a lived-in home, not only a containment error.

**Opening letter, tentative copy:**
> Dear Occupant, We regret to inform you that tomorrow has gone missing. As you are the only available person, locating it has become your responsibility. Please refrain from dying during the investigation. The paperwork is tremendous. Sincerely, The Department of Unfinished Things.

### The player character

Known only as **the Visitor**. Expressive silhouette, independent personality through thoughtful examination comments but little rigid backstory. No requirement to use Paige's real name or likeness. The visitor does not need combat, health, hunger, crafting, romance, jump physics or extensive inventory complexity. Optional user-approved personalization can be added late, separately from narrative-critical systems.

## C. Game boundaries and non-goals

**In scope:** seven authored areas, five main puzzle sequences, five major NPCs, one central mode-shift mechanic, small inventory, notebook and hint system, meaningful environmental transformations, two choices of ending, autosaves, simple settings and credits.

**Out of scope for V1:** procedural generation, combat, AI NPC simulation, branching campaigns, multiplayer, farming, crafting trees, large seamless 128×88 map reuse as a mandatory requirement, achievements service integrations, weather systems beyond authored ambiance, procedural dialogue, multiple playable protagonists, complex character customization, timed puzzle deaths, live services, licensed media references and publishing private memories as source art.

No feature may be added because a framework makes it easy. Anything new requires demonstrating how it improves the core player promise.

## D. Player experience and controls

**Primary controls (rebindable where feasible):**

| Action | Keyboard | Controller proposal | Behavior |
|---|---|---|---|
| Move | WASD / arrows | Left stick / D-pad | 8-way animated movement; normalized diagonals |
| Interact / confirm | E / Enter | South face button | Interact in range; show short verb + name prompt |
| The Almost | Space / Tab | Right shoulder | Instant toggle when unlocked, no arbitrary cooldown |
| Notebook / objectives | N | View/Back | Pauses exploration, shows discovered clues only |
| Inventory | I | West face button | Inspect, select or use an item, no large backpack |
| Back / pause | Esc | Start/Options | Close dialogs and panels; pause gameplay |
| Dialogue advance | E / Enter / click | South face button | One action per line, hold doesn't skip instantly |

**Mouse:** supported for UI selection and clicking inspectable objects if practical, but never required. Keyboard-only path required. Rebind controls when feasible; otherwise ensure clear alternatives. No mandatory fast reaction or precision movement. Single-pixel positioning should never be needed to interact.

**Camera:** orthographic PixelArt 2D, room-bounded, never reveal void beyond the map. Smooth optional camera-follow only if it doesn't blur pixel content. Walk speed proposal 60–75 world px/sec at 16px tile scale, tuned to traversals, not assumed final. Interact detection: nearest visible eligible object in a short directional cone with unobstructed line of sight, plus generous buffer; no accidental multi-trigger. Every interactable visually hints through silhouette/detail and an interaction prompt.

## E. The Almost — gameplay system

The world has **The Here** (present) and **The Almost** (unrealized possibility). Early puzzle teaches shift using the Guestbook. All rooms have clearly authored differences, but only clues, interactables and explicit special passages change; physical base walls remain stable for simplicity and safety. Later special thresholds may be traversed only when destination collision is known valid.

Rules:
- Shift is toggled by one input; reversible; audible chime and readable 0.2–0.35s transition, optionally reducible in settings.
- Shift does not freeze the player for long or impose battery/mana/timer constraints.
- A transition may change palette, ambience, highlight previously unseen props, swap permitted interactions, or expose text/characters.
- Interactables have stable IDs and mode masks (`HERE`, `ALMOST`, `BOTH`); puzzle flags persist across mode changes and saves.
- No vital clue may be revealed *only* by low-contrast color. Provide shape/outline/audio/interaction changes.
- If a switch would produce an invalid position or blocked route, preserve a stable safe space or veto with an unobtrusive cue and explanation. Never teleport through walls.
- Keep a subtle mode label/icon in the HUD, not permanent intrusive effects. If reduced motion is enabled, use a quick fade instead of screen distortion.
- Every puzzle has at least one discoverable use of The Almost; don't turn it into a universal 'press to highlight the answer' cheat button.

**Not** a separate fully simulated world with duplicate maps, alternate NPC AI or physics. It is an authored state layer that can scale.

## F. Core gameplay loop

1. Enter a compact, detailed room with a clear immediate curiosity.
2. Inspect objects and meet a resident who has a specific problem.
3. Toggle The Almost to reveal contradictory evidence or missing parts.
4. Combine a clue, conversation, or inventory item in an understandable way.
5. Resolve an environmental puzzle and earn a story change (door, character, journal evidence or animated world reaction).
6. Return to the hub or move forward. Optionally explore for flavor; no meaningless fetch chains.

**Pacing guardrail:** First playable control in under 45 seconds after launch; first interaction in under 90 seconds; first use of The Almost within 3 minutes; first aha puzzle solved around 5–7 minutes for an uncoached first-time player. These are test targets, not skip-cutscene mandates.

## G. Systems

### Investigation notebook
- Auto-captures **confirmed clues**, character notes and active objective, never presumes a fact unseen by the player.
- Shows compact page tabs: `Clues`, `Residents`, `Rooms`, `Tasks`; accessibility-friendly text sizes.
- Clue IDs ensure known / unknown / resolved states; no fake pages filled with filler.
- May pin one objective in HUD as plain language, e.g. “Find a name the Guestbook will accept.”

### Inventory
- 6–8 fixed slots or a compact list, supports acquisition, inspection and contextual use; avoid sprawling RPG menus.
- Only tangible objects belong here (blank guest pass, brass key, tea tin, folded note). Information belongs in notebook.
- The player can never permanently discard a key item. Inventory items cannot be consumed unless puzzle explicitly expects it, and save state records consumption atomically.
- Items used on objects yield specific responses; one amusing generic failure line is fine but don't rely only on “Doesn't work.”

### NPC conversations
- Short, expressive, two lines per beat where possible; 3–4 optional topic choices max.
- Dialog tracks story flags and location, so characters acknowledge what happened.
- A joke can conceal a clue but cannot be the **only** clear clue without a follow-up notebook record.
- Allow text speed controls, instant reveal and skip previously read lines. No involuntary autoplay in essential dialog.

### Hint ladder
- Fig can provide 3 hints per active puzzle. Tier 1: point toward relevant room; Tier 2: name the relevant mechanic; Tier 3: give explicit combination/use.
- Never punish hint use. Hints unlocked via dialog and notebook, no wait timer required. Never reveal future spoilers.

### Cozy exploration rewards
- Inspect descriptions contain small jokes and stories; every room includes at least 3 optional inspectables.
- Optional **Keepsake Tokens** (five in total) reward attentive exploration. They reveal humorous epilogue lines, not gate main endings.
- Environmental feedback when a room is solved: lights become warmer, residents relocate, a plant flowers, or background music gains a layer.
- There is no failure state where the house disappears because the player pauses or reads slowly.

## H. Narrative structure and endings

**Act 1 (0–15 min):** Forgotten Street -> Entrance Hall -> first puzzle; unlock Crooked Kitchen and learn of erasure warning. Stakes: tomorrow is missing.

**Act 2 (15–35 min):** Kitchen, Library, Greenhouse, Mirror Hallway (routing described in file 03). Stakes: residents fade, Mabel admits sealing tomorrow, evidence needed to stop closure.

**Act 3 (35–50 min):** Attic Clockroom; player combines documentation of a household (relationships, caretaking, shared history) with the clock mechanism and debates the Auditor; restoring time unavoidable; choice shapes how house survives.

**Ending A — Open Doors:** The mansion is recognized as a home that may be visited. It appears on rare rainy nights. The cast begins connecting to the world.
**Ending B — Secret Sanctuary:** The mansion stays hidden but protected by an exemption; it shelters unfinished possibilities and welcomes select visitors. Everyone keeps their eccentric rhythms.

Both endings must feel complete and coherent. Optional collectibles add final character vignettes but not a 'true ending' lock. No ending says the player saved everyone through vague magic: evidence assembled, house bonds documented, and the Auditor uses a loophole supported by prior clues.

## I. Art, audio and UI requirements (overview)

- 16×16 environment tile grammar; 24×32 player/NPC sprite cells or deliberate per-character exceptions; original art only unless license is documented. Full rules in file 02.
- Target reference internal playfield of 384×216, crisp integer-scaled pixels; UI may render separately at higher resolution for text clarity. Validate on real target screens.
- Warm burgundy, dusk plum, candle amber in The Here; spectral indigo / dusty blue / pale violet in The Almost. Color cannot be the sole semantic cue.
- Layered ambient audio, comfortable music, understated but legible interaction feedback; no abrupt ear-splitting horror stingers.
- UI: title, New/Continue, one autosave + optional 3 manual slots if simple, settings, pause, credits; scene objective; dialogue box; compact notebook/inventory; ending cards.

## J. Scope control and approval contract

**Artwork before game implementation.** First inspect the repository read-only, then create concept art AND usable production-scale assets in art staging. Present contact sheets, color palette and technical inspection (frame count, transparency, dimensions, coherent scale). Stop for **explicit human art approval** before altering gameplay code, Godot scenes or existing maps. See files 06 and 08.

**Quality gates:** Art approved -> 8–10 minute vertical slice passed in editor and exported browser build -> full map/content build -> all puzzle flags/endings tested -> desktop/browser signoff -> mobile only if feasible.

**Change control:** If story or scope change is proposed, edit documentation and ask for approval; do not claim agreed scope based on assistant brainstorm alone. Codex must report what is implemented, what is conceptual and what remains unverified.
