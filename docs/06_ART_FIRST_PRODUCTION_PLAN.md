# 06 — ART-FIRST PRODUCTION PLAN AND SIGNOFF GATE

## Why this is the critical path

The previous game attempt dissatisfied the user. This rebuild must not fall into a code-first pattern with placeholders, incompatible sprite packs or a decorative map that fails to deliver actual gameplay. **No gameplay source changes until a representative art pack has been created, inspected and approved.** The phase is not complete when an AI image generator outputs a nice cover: we need actual valid pixel-game assets.

## Phase ART-0 — discovery, constraints and inventory (read-only)

- Inspect `itsnotalwin/Innate` read-only: current default and active branches, Godot version/project settings, existing sprites/licenses/imports, workflow, live/demo claims and project-specific `AGENTS.md`/`PROJECT.md`/CONTEXT.
- Read this kit and vault build standards. Do not erase, modify or deploy the existing project.
- Output `ART_PRODUCTION_PLAN.md` documenting target base resolution, sprite grid choice, art pipeline (hand-authored original, art tool, Aseprite/LibreSprite, Pillow patterns, etc.), expected PNG outputs and provenance requirements.
- List potential reuse only if it fits the new concept AND rights are verified. Unknown licenses = do not reuse.
- If no tool is capable of producing real visual PNG assets, STOP and clearly report the limitation; do not substitute generated text, CSS gradients or a colored rectangle as an approved sprite.

**ART-0 output:** inventory report + art production plan. Not gameplay code.

## Phase ART-1 — art direction and original samples

1. Develop two distinct **visual interpretations** of the same entrance hall and one cast lineup. One can be detailed Gothic cozy; another can be more minimal and readable. Keep both consistent with the 16px world tile scale.
2. Generate or draw original 16:9 title key art and 3 visual treatments (street, hall Here, hall Almost). Label as **CONCEPT**, not runtime. Create **separate editable title lettering** "The House That Ate Tomorrow" and tagline "Tomorrow is missing. The cat denies everything."; do not flatten words into background art.
3. Create actual transparent PNG assets: one Visitor 4-dir idle/walk sheet, Fig idle/talk/portrait, 16px environment sample atlas, one Guestbook prop normal/Almost, and basic polished dialogue UI / inventory icons. Do not assemble a fake playable screenshot.
4. Provide clear sprite/atlas metadata (bounds, anchors, frames, pixel ratio), original image sources/provenance, palette and cross-file consistency checks.
5. Produce `ART_REVIEW_CONTACT_SHEET.png` at native 1×, 2× and 4× for sprite grids; and `MOODBOARD.png` for conceptual lighting only.
6. Provide a proposed 10–15 second **art-only** flipbook/video preview of The Here -> The Almost if supported; no need to implement Godot mode toggling for this stage.
7. Compare every asset against the art bible. Replace weak samples before asking for signoff.

**ART-1 minimum required artifacts:**

| Deliverable | Hard requirement |
|---|---|
| 2 entrance hall concept layouts | Both legible at intended playfield, different strengths, file paths |
| 1 paired Here/Almost scene | Same coordinates and furniture silhouettes; visible story changes |
| 1 exterior illustration | Original rainy mansion, Fig silhouette, compelling title framing |
| 1 player sprite sheet | Native individual RGBA frames for 4 dirs, at least 4-frame walk per direction |
| 1 Fig sprite+portrait sheet | Sprite reads as black cat with tie, good contrast and expressions |
| 1 sample atlas | Modular tiles aligned to logical 16px; identifiable floors, wall, door, props |
| 1 UI kit | Dialogue box, buttons/focus states, mode indicator, item icon style at usable sizes |
| 1 art contact sheet + provenance | Filenames, frame dims, consistency stats, import/filter notes |

## Phase ART-2 — structured review (HARD STOP)

Codex must end its answer with:
- Art deliverables table (`READY`, `BLOCKED`, `NEEDS REFINEMENT`) and exact artifact paths.
- Side-by-side room comparison and 3 strengths/risks.
- Native resolution sprite inspection: crisp clusters, full alpha, anchor placement and animation loops.
- Recommended visual direction, clearly distinguished from user approval.
- **Explicit prompt:** “Please approve the ART direction and production sprite samples before I create or modify Godot gameplay source. Reply `ART APPROVED` or list changes.”

**Absolute stop:** No commit/edit to gameplay scripts, scenes, collision maps, procedural generator, export workflow, or deployments. No unapproved art promotion into production `assets/`. Art staging can be version-controlled in a non-production branch only if repository policy permits and no unrelated files are changed. Do not auto-proceed after generating moodboards. User's approval must be explicit in a later interaction.

## Phase DEV-0 — only after approval

- Establish baseline branch and review migration/legacy code. Do not mass-delete existing work.
- Define scene and data architecture in source, ensuring project folder context, design notes, and actual runtime screenshots where appropriate.
- Add approved sprite imports, interactions and toggle skeleton; don't generate rest of world.
- Implement a single 8–10-minute playable vertical slice: street, foyer, Fig, Guestbook, mode swap, notice and first unlock.
- Test export in editor and browser; collect actual screenshots, test UI, no missing textures/audio, parse errors or softlocks. Stop for vertical-slice signoff.

## Phase DEV-1 — full production after slice accepted

- Produce remaining room art in art-first batches (full art review ahead of each room code), then implement P2–P5, dialogue, cues and save/versioning.
- Test branch choice endings, game state recovery, accessibility, Windows/Web export and credits.
- Full release only after separate final QA acceptance.

## Red flags that stop work

- Codex produces a lovely cover illustration but no production-suitable spritesheets.
- Unlicensed sprite pack is copied without proof or attribution terms.
- Assets look inconsistent across rooms or suffer interpolation blur.
- Artwork is “approved” solely because Codex thinks it looks good.
- Placeholder programmer art becomes permanent without review.
- Code or new game scenes appear in ART-only phase.
- Screenshot named `SCREENSHOT.png` was created from concept rather than real running game.
- A green CI build is presented as evidence the browser game is live.
- Changes overwrite the prior project without a reviewed migration plan.
