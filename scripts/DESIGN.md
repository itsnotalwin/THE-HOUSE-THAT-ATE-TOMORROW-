# Runtime presentation

Render the world in a 384×216 SubViewport with nearest texture filtering. Preserve 16×16 tiles, 24×32 Visitor cells, 24×24 Fig cells, and the approved plum/amber/spectral palette. Here and Almost share collision geometry; changing modes must not move the player or create a trap. Furniture uses depth sorting around the Visitor's feet.

The UI uses a separate high-resolution 1152×648 reference canvas so dialogue remains readable over the native pixel world. Use the approved nine-slice panels and buttons, licensed DejaVu fonts, cream text, plum surfaces, and visible focus outlines. Standard and large reading sizes are 22 and 26. Keep text and icons as the source of gameplay information; color and sound supplement them.

Modal panels disable movement. One input advances one dialogue line; E must not select a choice accidentally. Deferred focus must check that the control still belongs to the visible tree. Reduced motion suppresses optional ambient movement; it must preserve clues and navigation.

`SCREENSHOT.png` is reserved for an actual capture from the running game. Concept art and interface studies under `../art_staging/` do not satisfy that requirement. See `../qa/` for capture provenance and review evidence.
