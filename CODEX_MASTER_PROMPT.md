# CODEX MASTER PROMPT — THE HOUSE THAT ATE TOMORROW

You are the lead art director, pixel artist, narrative game designer, UX designer and Godot engineer responsible for eventually delivering a **complete, polished** 2D cozy-gothic narrative puzzle adventure called **The House That Ate Tomorrow** for Paige.

## LOCKED CREATIVE NAME FOR THIS HANDOFF

- **DISPLAY TITLE (selected by the user):** **The House That Ate Tomorrow**.
- **OFFICIAL TAGLINE FOR CONCEPT ART:** **Tomorrow is missing. The cat denies everything.**
- Use the exact spelling and capitalization in title concepts, logo/wordmark proposals, art-review sheets, future Godot window/title menu, future docs and packaging. Do not resurrect a previous creative title. The name is **selected for this personal project** but has **not been legally/storefront cleared for commercial launch**.
- **Legacy technical identifiers remain unchanged:** GitHub repository `itsnotalwin/Innate`, existing directory names in source, and BRAIN canonical file `20_Projects/INNATE-Paige-Game.md`. Do **not** rename, archive, delete or migrate them as part of the art phase. Public branding and repository paths are different concerns.
- The new title describes the same approved story premise, cast, seven planned locations and The Almost gameplay system. Rename must NOT trigger a story or scope rewrite.
- Title key art should visually suggest an impossible crooked mansion, a clock at **11:59**, a pink moon, warm windows and Fig appearing suspiciously innocent; prepare the lettering and tagline as **separate editable/transparent assets**, not text baked into game-background layers. Match the title treatment in the included updated concept board but redraw for production.

## NON-NEGOTIABLE WORK MODE: ARTWORK FIRST. DO NOT CODE THE GAME YET.

**This execution is PHASE ART ONLY.** Do **not** build, edit or replace gameplay code, Godot scenes, collision maps, generator logic, CI workflows or deployment settings before separate explicit user approval of the ART package. The user was dissatisfied with a previous attempt; don't begin with a large map or placeholders. Create professional, consistent, ORIGINAL game artwork first, then stop for review. You may use image-generation/graphics/drawing tools and limited scripts to **author/export/validate ART files** in a staging workspace. Art tooling scripts are not permission to implement game mechanics.

If art-generation capabilities are absent, report the blocker, generate the best faithful original pixel art you legitimately can using available drawing/image tools, and STOP rather than falling back to gameplay coding. Never claim a generative illustration is a production spritesheet without verifying its pixels, alpha, frame layout and usable source assets.

## Authoritative supplied materials

Read in this order:
1. `README_START_HERE.md` and this prompt.
2. `docs/01_GAME_DESIGN_DOCUMENT.md` (game scope and rules).
3. `docs/02_ART_DIRECTION_BIBLE.md` (pixel-art grammar and palettes).
4. `docs/03_WORLD_AND_PUZZLES.md` (seven rooms, five main puzzles, flags and hints).
5. `docs/04_STORY_AND_DIALOGUE.md` (cast/three acts/sample lines).
6. `docs/06_ART_FIRST_PRODUCTION_PLAN.md` (hard stop).
7. `docs/09_VISUAL_CREATION_PROMPTS.md` (asset briefs).
8. `docs/05_TECHNICAL_ARCHITECTURE.md`, `docs/07_AUDIO_AND_ACCESSIBILITY.md`, `docs/08_MILESTONES_AND_TEST_MATRIX.md` for future handoff.
9. `manifests/asset_manifest.csv`, `checklists/ART_APPROVAL.md`.
10. View ALL `art_references/*.png` concept files. They are ORIGINAL mood references, not final assets; their small text can be wrong. Written specification prevails. Never use concept composites as production sprite sheets.

Do not skip reading by trusting an earlier chat recap. If spec files are missing, request access before making assumptions. Keep documentation and art separate from actual Godot project source until approval.

## Source and governance

The existing game repository is `itsnotalwin/Innate`. The private canonical knowledge vault is `itsnotalwin/obsidian-vault`, main branch, where project status lives in `20_Projects/INNATE-Paige-Game.md`. Read relevant vault governance: `AGENTS.md`, `CHATGPT.md`, `99_System/BOOTSTRAP.md`, `99_System/KNOWLEDGE-QUALITY.md`, `99_System/BUILD-STANDARDS.md`. Read project root `AGENTS.md` and `PROJECT.md` and nearest CONTEXT/DESIGN files, if they exist.

**Existing-state caution:** Previous notes record Godot 4.6.3, an experimental 128×88 map, some successful Web exports, but unresolved default-branch/Pages deployment blockers and third-party Sprout Lands art license concerns. These are HISTORICAL and may be stale. Verify actual repository READ-ONLY. Do not assume main is the default branch, builds deploy successfully, or old art is cleared for reuse. Do not delete branches, replace the old map or publish anything without a separately approved scope.

For later authorized build work: Every maintained source subfolder gets `CONTEXT.md` immediately; CSS/UI/visual source folders also get `DESIGN.md` and an ACTUAL updated screenshot from the running implementation `SCREENSHOT.png`. The top level needs `AGENTS.md` and `PROJECT.md`. Do not fabricate runtime screenshots or use concept mockups to satisfy the evidence requirement. Any changes to the existing canonical vault note require current SHA and verified remote commit; do not edit BRAIN unless making a meaningful confirmed update in an authorized workflow.

## Confirmed creative goal

**Blend spooky mystery + cozy exploration + bizarre humor.** Build a short, immersive, emotionally satisfying experience, not a vast empty map or visually disconnected templates. Proposed plot: a strange house gathers things that almost happened; Mabel has hidden tomorrow to delay the Auditor's scheduled closure; the Visitor uses **The Almost** to reveal hidden possibilities, solve fair puzzles, prove the inhabitants form a household, restore time and choose whether the house remains hidden or opens to visitors. The cast is Fig the bureaucratic cat, Miss Thimble the ghost librarian, Sir Crumb the mouse knight, Mabel the caretaker, and the Auditor. Target future playtime 40–50 minutes with 7 authored locations, 5 puzzles and 2 good endings. Treat numbers as design targets; note any needed scope change rather than silently diverging.

## ART TASKS: execute this stage now

### Step 0: Inspect, then plan

Read existing source files without changing them; inventory old art/licensing; report actual baseline. Create `ART_PRODUCTION_PLAN.md` that states art tools available and concrete source/export path, tile/sprite sizes, palette, output naming, rights and validation plan.

### Step 1: Original concept explorations

Make TWO differentiated entrance hall composition/style candidates (both matching cozy Gothic pixel art) and the **same Here/Almost composition**. Produce a beautiful illustrated mansion title key art with empty space for title overlay, and create **separate** crisp, original logo/wordmark and tagline lockups using the exact title **The House That Ate Tomorrow** and tagline **Tomorrow is missing. The cat denies everything.** (no text baked into background). Create a character lineup for Visitor, Fig, Miss Thimble, Sir Crumb, Mabel and Auditor. Show a coherent palette and restrained effects, not a collage of incompatible styles.

### Step 2: Produce **usable original pixel-game artwork**, not merely presentation graphics

At minimum create:
- A **true modular 16×16 pixel tile atlas** covering foyer floors, walls/baseboards, doors, windows, carpet/runner, lectern, painting frame and a few furniture pieces, with seamless edges and documented tile indices/footprints.
- A **transparent RGBA Visitor spritesheet** at proposed 24×32 per frame, 4-direction idle + 4-frame directional walking (or present a visibly superior consistent scale and seek approval for size change).
- A **transparent Fig sprite sheet** with idle/blink/tail pose and 64×64 or consistent portrait expressions.
- A guestbook sprite Here/Almost pair, blank portrait nameplate pair, at least 6 useful UI icons.
- A cohesive, polished dialogue frame, focus state, notebook and inventory UI sample; text must be genuinely readable at ordinary browser/window sizes.
- A **separate layered/transparent title wordmark**, a **separate readable tagline lockup**, and sample menu composition with the exact selected title and tagline. Supply clean fonts or vector/source design layers as permitted, but never hand over a flattened banner as the only title artwork.
- A paired Hall Here vs Hall Almost **actual room layout mockup** built from the original modular sprites if feasible; separate conceptual painting explicitly labelled otherwise.
- Metadata file per atlas/sheet: native dimensions, frame rows/columns, direction order, timing, foot anchor, tile indices, transparency/provenance.

Create sprites with a purposeful limited palette, nearest filtering, no interpolation, no watermark, no fake transparency. If image-generation produces a high-res illustration instead of exact native pixels, **redraw/refine as true pixel assets**. Never rip reference game art or unlicensed assets. If you use one of your art tools to render static sprites, inspect its output visually rather than trusting the prompt alone.

### Step 3: Reviewable output package

Produce these files in a distinct art staging folder or a separately approved art branch:

```text
ART_PRODUCTION_PLAN.md
ART_REVIEW_REPORT.md
art_staging/
  [CONTEXT.md and any required DESIGN.md docs for maintained art folders]
  concept/                      # labeled concept renders + paired room alternatives
  branding/                     # editable exact-title wordmark + tagline, separate from backgrounds
  sprites/                      # native transparent Visitor/Fig sheets and exports
  tiles/                        # modular 16px atlas + tile metadata
  props/                        # guestbook/nameplate/clue examples
  ui/                           # button/dialogue/notebook/focus samples
  review/ART_REVIEW_CONTACT_SHEET.png
  review/ART_MODE_COMPARISON.png
  review/ART_PALETTE.png
  manifest.csv                  # status, size, frame count, source/license
```

Note: Documentation and concept files do not satisfy the source-project `SCREENSHOT.png` requirement; an accurate running-screen screenshot becomes possible only after actual authorized implementation.

In `ART_REVIEW_REPORT.md`, list actual generated files and validation outcomes: frame dimensions, RGBA test, pixel alignment, palette match, visual cohesion, small viewport readability, remaining weak spots, risks and next steps. Distinguish conceptual imagery from usable sprite art. Display side-by-side image previews/contact sheets to the user. Document where native assets live and any licensing caveats.

## HARD STOP — human approval

**At the end of this execution, STOP.** Finish with an approval request, **exactly about art**:

“Please review the ART directions, native sprites, tiles and UI samples. Reply `ART APPROVED` to authorize creating the first playable Godot vertical slice, or tell me what artwork to change.”

Do not treat this prompt or a previous “yeah” as art approval. The user's current request approves making the SPEC and getting ART produced first, not gameplay code. Do not continue into any game implementation, repo reset, release or deployment without explicit later approval.

## FUTURE PLAN ONLY, FOR AFTER ART APPROVAL

**Do not run the following yet.** After `ART APPROVED`, implement the 8–10 min Street + Hall slice with Fig, The Almost, Guestbook puzzle, first warning notice, saving, hints, polished controls/audio and real in-game screenshot evidence. Stop again for user acceptance. After `SLICE APPROVED`, author remaining rooms one at a time, with asset approval preceding each room code; implement stateful puzzle logic, endings, accessibility and actual browser/desktop export QA. Deploy only with separate explicit user instruction and verified live result.

## Definition of excellent

An original, cohesive pixel-art aesthetic with expressive tiny characters; a beautiful room that is actually traversable; exact transparent native sprites and modular tiles; readable UI; believable atmospheric contrast between Here and Almost; honest state reporting and hard stops. Never prioritize a flashy image over usable assets or a growing codebase over fun.

**Proceed with ART-0 / ART-1 now, and nothing beyond the art approval gate.**
