# 09 — ORIGINAL ART CREATION BRIEFS AND PROMPTS

Use these as inspiration for image-generation, commissioned, hand-authored, or coded-pixel art workflows. They are not a substitute for actual final pixel-grid production assets. Artwork must be **original**, and every art output must be inspected for coherence, transparency, silhouettes and grid adherence.

## Universal creative constraints

Mood: cozy Gothic mystery, absurd warmth, slightly haunted, lovingly cluttered; burgundy/ink/pink/moonlight palette, amber light pools, mysterious spectral lavender. 2D top-down 3/4 view with readable walkable architecture, consistent 16×16 pixel tiles; whimsical character expressions. No photorealism, no smooth illustration masquerading as pixel sprites, no fantasy battle UI, no indistinct background clutter, no grid-breaking perspective, no stolen existing game character, no illegible text baked into playable art. For production sprites: transparent RGBA, correct sheet layout and frame boundaries.

### Brief A — Mansion title key art

> Original pixel-art title background for an intimate spooky-cozy narrative adventure: an impossible old Victorian mansion between two mundane town buildings at midnight, windows softly glowing amber, rain on dark cobblestones, burgundy roses, moon in muted magenta behind ornate roof silhouettes; tiny Visitor and judgmental black cat with red tie at the front gate; atmosphere mysterious, playful and inviting, not threatening. 16:9, foreground breathing room for separate UI title, no embedded text or fake UI, sharp deliberate pixel clusters, 2D game-art composition, subdued vignette, independent original design.

**Deliver:** 1536×864 or appropriate high-res concept reference; separately make game-ready pixel-consistent title layers. Do not force a photo-derived image through nearest scaling and call it pixel art.

### Brief A2 — Exact-name title lettering and tagline (separate from background)

> Create a uniquely lettered, readable gothic-storybook game title on transparent layers. The exact user-selected text is **"The House That Ate Tomorrow"**, with capitalization and word order verified. Gothic, elegant and lightly crooked, in cream/blush against deep plum; subtle bespoke flourishes referencing the mansion, moon and cat without obscuring letters. A separate smaller text lockup reads exactly **"Tomorrow is missing. The cat denies everything."**. Avoid generated gibberish and do not bake this lettering into title-background art. Supply an editable source/vector/font-based layer where possible, a transparent export, and a legibility check at real menu scale.

**Deliver:** `title_wordmark` editable source and transparent export; `title_tagline_lockup` editable source and transparent export; clear-area screenshot/mockup labelled CONCEPT, not verified runtime.

### Brief B — Entrance Hall Here state

> Precisely laid out top-down 3/4 pixel-art game room, a 32×22 logical 16px-tile Gothic foyer: walkable central runner, two clearly readable branching doors, one large Guestbook lectern, a painting on the north wall with an empty nameplate, a warm chandelier, candlelit wooden stairs suggested at back but not required gameplay route; decorative pink flowers, plum wallpaper, deep polished wood, amber pools of light; composition must prioritize actual walkable paths and game readability over decorative density, no characters or UI baked into tile art, original consistent modular assets, no text.

**Deliver:** concept + **actual modular tile atlas** + prop sprites + matching collision/placement plan. Keep same layout in B2.

### Brief B2 — Entrance Hall Almost state

> Exact same camera, wall/floor and prop coordinates as Entrance Hall Here state, but reimagined as The Almost: moon-blue spectral light, the painting's formerly blank nameplate now glowing with a shape suggesting hidden writing, a ghost silhouette briefly inhabits one armchair, translucent book dust and slight ethereal curtains; still cozy and navigable, no changing physical wall geometry, strong legible before/after contrast, original consistent pixel-art grid and sprites, no text rasterized into tile background.

**Deliver:** pair B/B2 anchored identically and with individual state-change sprites.

### Brief C — Visitor spritesheet

> Original small pixel-art game protagonist, curious young adult adventurer in deep plum coat with burgundy scarf and shoulder satchel, gender-neutral approachable silhouette, clear hair shape, consistent 24x32 pixels per frame on true transparent background; 4-direction idle and 4-frame walk for each direction, exact consistent feet origin and limb proportions across all frames, identical 1px shading clusters, no giant cinematic proportions or antialiasing, organized sheet grid with labelled metadata in separate JSON not baked text.

**Deliver:** direction-labelled raw frames or atlas, metadata, alpha and animation review.

### Brief D — Fig sprites and portraits

> Original black cat receptionist for cozy gothic pixel game, tiny burgundy necktie, clear golden eyes, rigid self-important posture, expressive tail and ears, not humanized or wearing a full suit; 24x24 or 24x32 logical native sprite as consistent with main cast, idle/blink/tail animation, separate expressive close-up 64x64 portrait grid, fully transparent RGBA, crisp chunky controlled pixel clusters.

**Deliver:** sprite atlas + two portrait expressions + facing rules and anchor.

### Brief E — Cast lineup

> Consistent original pixel-art NPC model sheet at same native pixel density: Miss Thimble friendly floating lavender ghost librarian with round glasses and book; Sir Crumb small armored mouse with sewing-needle sword; Mabel warm old-fashioned caretaker with purple hat and teacup; The Auditor tall ominous coat-and-hat silhouette with neat papers; Fig black cat in tiny tie; all scale relationships clear, silhouette and eye lines readable at native game view, neutral and expressive poses; transparent backgrounds in individual exports. No copied recognizable characters, no text.

**Deliver:** individual PNG sheets, not just one composited board; do not add every NPC to actual game in art approval stage if only first-room assets needed, but create concept lineup.

### Brief F — UI system

> Minimal, refined Gothic pixel-art game UI components: dialogue box deep plum and paper text, tiny portrait frame, raspberry focus outline, button hover/active/disabled examples, small mode icon for The Here / The Almost, 16px inventory icons, notebook page with clear readable modern body text, no ornate unreadable paragraphs; intended high-resolution UI overlay aligned above a 384x216 pixel playfield, coherent with warm candlelight and ghostly violet; original screens deliberately labelled as concept outside image.

**Deliver:** sliced 9-patch panel images, button states, empty portrait frame, icons, typography license, component measurements, keyboard focus indication, separate mockup showing full legible UI.

### Brief G — Other location keys

- **Kitchen:** cozy crooked copper and mahogany, kettle on stove, cups and sealed envelope, ghost rain at window in Almost state; clear hotpot interaction.
- **Library:** Victorian wine shelves and book-spine symbols seed/sprout/blossom, gentle spectral paper wisps, Thimble floating behind librarian desk, unobstructed aisles.
- **Greenhouse:** midnight flowers, pink glasshouse, glimmering moonflower, one ridiculous dangerous-looking carrot to a mouse's perspective, fantasy humidity.
- **Mirror Hall:** dim lavender mirrors with differing icons, sparse arrangement to increase unease, no jump scares.
- **Clockroom:** giant ornate three-station clock, papers and spectral gear, moody window and enough free space for Auditorium confrontation.

## Suggested staged art-tool procedure

1. Use images for composition and mood; pick strongest palette and character shape.
2. Create literal 16px tiles, 24px sprites and 64px portraits from original drawings; where an image model cannot output exact pixels, redraw using a suitable pixel-art tool.
3. Use native-size sheets, not bloated 1024px screenshots masquerading as sprites.
4. Check background alpha, tile seams, bounds/anchors, repeated frames and one coherent palette.
5. Make real contact sheets with no embedded UI text; annotate separately in Markdown.
6. Present selected art to human. Stop for signoff.

## Art evaluation checklist (apply per sample)

- **Distinctive:** memorable silhouette and world, not generic fantasy pixel pack.
- **Cohesive:** same tile and sprite pixel density, lighting direction and outline rules.
- **Useful:** atlas tiles and transparent sprites genuinely reconstruct the reference room.
- **Readable:** clue hotspots and exits obvious at actual playing resolution.
- **Expressive:** animations give personality without noisy effects.
- **Legal:** original or properly licensed, and source/credit documented.
- **Accessible:** text and mode labels legible without color-only distinctions.

## Explicit originality note

Reference screenshots from existing indie games, if used, are style studies only; do NOT reproduce another game's layouts, exact tile artwork, trademarked characters, UI or story. The generated images included in this kit are original mood illustrations but may contain text errors, and are NOT preapproved source sprites.
