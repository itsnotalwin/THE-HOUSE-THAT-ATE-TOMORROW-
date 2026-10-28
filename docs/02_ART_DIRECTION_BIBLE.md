# 02 — ART DIRECTION BIBLE

## 1. Identity: The House That Ate Tomorrow

**Selected display title:** `The House That Ate Tomorrow`  
**Tagline:** `Tomorrow is missing. The cat denies everything.`  
**Brand rule:** Key art is a text-free scenic layer; title lettering and tagline are independently editable foreground/UI assets. Keep source repo `itsnotalwin/Innate` unchanged. The title is not a promise of commercial/trademark availability.


**Visual signature:** richly observed pixel-art rooms with warm candlelight, witchy Victorian silhouettes, pink/burgundy floral details, a welcoming lived-in feel, and sudden ghostly blues when The Almost is active. Characters are lovable and slightly strange; no photoreal textures, generic stock UI or muddy AI-pixel paintings.

**Golden test:** A screenshot with no text should communicate “cozy, a little haunted, and funny.” A room must read at actual playable zoom, not just in a huge illustration.

## 2. Reference images INCLUDED in the kit

- `art_references/01_TITLE_WORLD_CAST_REFERENCE.png`: retitled gothic house, character, UI and reality-shift overview.
- `art_references/02_TITLE_KEY_ART_CONCEPT.png`: key art with approved selected title and tagline.
- `art_references/03_CHARACTER_LINEUP_CONCEPT.png`: character lineup and proportions (concept only).
- `art_references/04_palette_and_scale.png`: exact working palette tokens, native grid and sprite sizes.
- `art_references/05_environment_comparison.png`: Here/Almost same-layout mood comparison.
- `art_references/06_ROOM_EXAMPLES_CONCEPT.png`: exploratory room looks from the updated board.

**IMPORTANT:** Large boards are generated CONCEPT imagery and may contain distorted or incorrect miniaturized words and inconsistent pixel sizes. Do **not** crop characters from the boards and ship them as final gameplay sprites; these are layout/lighting/mood inspiration. Final production art must be rebuilt and checked frame by frame. Reference art is not evidence of working Godot scenes or screenshots.

### Optional outside visual research (look only, do not copy)
- `https://www.gamesradar.com/haunted-chocolatier-guide/` for warm dark pixel interiors and readable silhouettes.
- `https://www.moonlightpeaks.com/press/sheet.php?p=moonlightpeaks` for cozy supernatural material language, not necessarily the same render perspective.
- `https://steamcommunity.com/app/1899060/` for dramatic Gothic interior staging and bold lighting.
- `https://glintapps.itch.io/cozy-interiors` for a concrete example of modular 16px interior asset inventories, not for automatic borrowing; obey licenses.

Originality is mandatory. No traced assets, copied characters/logos, or unlicensed Sprout Lands reuse. If the existing repository contains third-party art, document origin and licensing first.

## 3. Technical pixel art grammar

| Element | Target | Validation |
|---|---|---|
| World tile | **16×16 px** logical square | All walls/floors align without seam |
| Walkable corridor | ≥ 3 tiles at usual pinch points | Pathing clear, room reading uncluttered |
| Player animation cell | **24×32 px** (feet centered on 16px grid) | 4 directions, idle/walk, consistent baseline |
| Common NPC | 24×32 px for humanoids, variable for cat/mouse | Consistent pixel density and scale |
| Large decor | Multiples of 16px where modular | Collision footprint separate from drawn overhang |
| UI item icon | 16×16 or 24×24 px | Legible against dark UI |
| Effects | 16/32/64 pixel authored frames as needed | No anti-alias blur, nearest-neighbor imports |
| Playfield reference | **384×216** internal pixel canvas (16:9) | Test 2x/3x/4x integer presentation |
| UI type | Prefer separate resolution-independent UI | Test readability at browser 100% and small laptop |
| Asset format | Transparent PNG, straight alpha | No baked checkerboards or magic-color backgrounds |
| Animation | 4–8 frames per directional walk, 4–8 fps initial target | Gentle personality, no excessive motion |

Render using nearest-neighbor texture filtering and correct import settings. No subpixel crawl from camera or scaled parent nodes. Camera follow should snap to pixel bounds if needed. Use authored fixed light pools/color layers instead of expensive full-screen shaders for visual fundamentals. The Almost effect may add a mild palette shift and ghostly overlays, but **preserve pixel legibility**.

**IMPORTANT**: Reference character art may suggest a 32x48 style or more detail than a 24x32 game sprite allows. Codex must resolve this visually through comparison sheets; if 24x32 fails readability, recommend one cohesive alternate sprite scale BEFORE implementing. Never mix scales room by room.

## 4. Palette (starting token library, adjust through art review)

| Token | Hex | Role |
|---|---|---|
| Void / ink | `#11101C` | Deep backgrounds, silhouettes |
| Deep plum | `#25152E` | Night atmosphere, shadows |
| Aubergine | `#432047` | Walls/fabric, contour richness |
| Wine | `#752C58` | Drapery / midtone, character accents |
| Raspberry | `#B63A75` | Pink accent, glints |
| Blush | `#EF93B4` | Lightest pink, highlight / UI accent |
| Candle amber | `#F6B56B` | Active lamps, tactile warmth |
| Paper | `#F4DBB9` | Readable UI, letters |
| Slate violet | `#59508A` | Shadow in The Almost |
| Spectral blue | `#7393C5` | Uncanny glow, clues |
| Moon cream | `#C7D8E9` | Highlight in The Almost |
| Ghost mint | `#9ADBC7` | Spectral accents, sparse |
| Leaf muted | `#496B5D` | Plants, tonal variance |
| Timber | `#8E584F` | Wood / shelves |
| Warning plum | `#A74758` | Moderate danger / bureaucracy |
| Outline | `#0B0C16` | Sprite outlines and typography edges |

Limit an individual sprite's shading to 3–5 values per material plus outline, unless readability requires more. Avoid neon pink everywhere. Distinguish important interactables with a **unique shape + restrained glint**, not blanket glowing outlines. Warm/cold contrast does storytelling.

## 5. World art examples / required art samples FIRST

Art stage **must produce**:

1. **Exterior hero illustration** of Forgotten Street with gothic mansion between mundane neighbors, wet cobbles, absurd cat receptionist, pink moon. 16:9 composition for title illustration (illustrative, not tiled gameplay).
2. **Entrance Hall master mockup** at actual proposed playable viewport with clearly readable pathing and 16px environment grammar, plus matching Almost variant with same object placements.
3. **True tileset atlas**: floors, baseboards, Victorian wallpaper, columns, door frames, windows, furniture, rugs, signage, glass, plants and chandeliers; a grid, not an uncut illustrated room.
4. **Player spritesheet**: idle and walk 4-direction, facing consistent, transparent grid; layout metadata.
5. **Fig and Miss Thimble**: full small sprites, expressive 64×64 portraits, 2 expression states each.
6. **Guestbook + clue props**: normal/Almost sprites with transparencies and proper anchor points.
7. **UI and branding sample**: exact-title wordmark and separate tagline lockup, title/menu composition, dialogue with character portrait, notebook page and inventory. At least one mockup at playable screen width to prove readability.
8. **One contact sheet**: show all art side-by-side at native 1×, 2×, and 4× nearest scale with checkerboard for transparency testing.

Art samples must be hand-authored or newly generated ORIGINAL artwork. If generative concept images are used, refine or redraw them into valid tile/sprite assets. Automated pixel downscaling alone is NOT enough; reject inconsistent pixel clusters, blurry anti-aliased edges and unreadable silhouettes.

## 6. Environmental location identity

- **Forgotten Street:** ink blue rain, wet cobblestones, quiet shop windows, vivid mansion only in the right light, one soft lamppost, inviting threshold.
- **Entrance Hall:** mahogany, dusty plum wallpaper, brass fixtures, hanging portraits, central rug, almost-too-many doors. Has to teach navigation and look superb.
- **Crooked Kitchen:** warm terracotta, copper pans, odd cups, slightly skewed pantry labels, kettle with personality; comic warmth.
- **Library:** wine-dark bookshelves, brass reading lamps, ghost parchment, huge volumes that emit quiet blue light in Almost mode.
- **Greenhouse:** rose pink and leaf green, dew, botanical silhouettes, glass dome, midnight blooms, mysterious water source.
- **Mirror Hallway:** violet shadows, ornate frames, reflection inconsistencies, more negative space for suspense; not horror gore.
- **Attic Clockroom:** huge brass timepiece, moonlit dust, paper forms, deliberate symmetrical climactic architecture, warm vs cold light at finale.

A room's Here/Almost pair must retain identity and overall floorplan. Difference categories: color treatment, ghost props, secret lettering, spectral rain, missing/extra objects, one changed point of interaction. Never just duplicate a map with a screen tint.

## 7. Character model sheets

**Visitor:** neutral adventurer, dark plum/burgundy clothing, distinctive scarf or coat shape, readable hair silhouette, small shoulder satchel. Body language cautious but curious. Avoid real-person likeness unless user specifically authorizes.

**Fig:** small black cat, pale amber eyes, absurd tiny red tie; straight-backed, judgmental, personality conveyed with ear/tail pose. Sprite idle/blink/tail swish, one expressive portrait eyebrow/ears variant; no literal suit/body like a human.

**Miss Thimble:** spectral lavender librarian, rounded glasses, drifting scarf, book-hugging pose. Preserve gentle face features at sprite scale.

**Sir Crumb:** small mouse with oversized protective armor, sewing-needle sword, proud stance; playful but readable silhouette. Size may be 16×24, use equivalent native pixel density.

**Mabel:** caretaker wearing vintage violet hat/apron, teacup, kind eyes, old-fashioned relaxed posture. Warm palette, hint of secrecy.

**Auditor:** tall flat dark silhouette, polished hat, paper forms and thin spectral outline; imposing through stillness and negative space, not a monster face.

Give each character: front/back/left/right or proven horizontal flip rule, profile icon, two facial expressions, neutral and reactive poses, consistent feet origins, collision bounds, import settings, and credit provenance.

## 8. UI and typography

**Typography:** pixel-friendly text if legible; allow high-resolution clean sans-serif alternative for dialogue and accessibility. Do not rely on novelty Gothic fonts for body content. Decorative headings only. UI must support at least 15–16px effective screen text at common desktop resolutions, with scaling options.

**Language:** restrained linework, paper textures, deep ink backgrounds, burgundy selection states and informative icons. Text overlays must meet contrast goals and have focus states; show arrows beside choices, not color only.

**HUD:** transient interaction hint, one-line objective optionally pinned, small Here/Almost state icon; do not turn the game into a busy RPG dashboard.

**Dialogue:** portrait left, text block, speaker name, continue indicator, optional 2–3 response buttons. At 384×216 playfield, consider a distinct higher-resolution UI layer with accurate hit regions and scaling.

## 9. Animation inventory and art review standards

- Visitor 4-direction idle (minimum 1–2 frames each), 4-direction walk (minimum 4 frames each), enter/inspect optional.
- Fig idle, blink, tail sway, talk portrait expressions.
- Thimble hover (4–6 frame seamless), Sir Crumb salute, Mabel kettle action, Auditor briefcase/paper motion (subtle, not expensive).
- Candle loops (4 frames), window rain (seamless), chimney/wisp (4 frames), page flutter (3–5), mode shift (few frames), clue sparkle (4).
- Deliver sprite atlas documentation: filename, sheet cell dimensions, frame count, direction order, frame time, origin, collisions, animation names, color set.
- View at native zoom: no visually critical sprite should resemble visual noise. Edges must be truly pixel-crisp.
- Full screenshot acceptance needs a REAL in-engine screenshot later; art stage mockups must be explicitly labeled mockups and cannot satisfy that requirement.

**Art approval question:** Would a first-time player recognize the Visitor, Fig, the nearest interactable, floor exits, and current mode at actual play size within 3 seconds?
