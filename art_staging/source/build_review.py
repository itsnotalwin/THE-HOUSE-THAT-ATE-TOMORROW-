"""Compose art-review exports from unchanged source layers. No game runtime.

Pillow handles exact typography and static layer assembly. Native sprites are
only enlarged with nearest filtering. Illustration/type layers use Lanczos.
Run from any working directory after drawing the native assets and branding.
"""
from pathlib import Path
import csv
import hashlib
import html
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'review'
P = json.loads((ROOT / 'palette.json').read_text())
FONT = ROOT / 'branding/fonts/DejaVuSans.ttf'
SERIF = ROOT / 'branding/fonts/DejaVuSerif-Bold.ttf'
TITLE = 'The House That Ate Tomorrow'
TAGLINE = 'Tomorrow is missing. The cat denies everything.'


def font(size, serif=False):
    return ImageFont.truetype(str(SERIF if serif else FONT), size)


def label(im, xy, text, size=20, color='paper', serif=False):
    ImageDraw.Draw(im).text(xy, text, font=font(size, serif), fill=P[color])


def layer(im, path, xy, size=None, native=False):
    item = Image.open(ROOT / path).convert('RGBA')
    if size:
        item = item.resize(size, Image.Resampling.NEAREST if native else Image.Resampling.LANCZOS)
    im.alpha_composite(item, xy)


def title_composition():
    im = Image.open(ROOT / 'concept/MANSION_TITLE_BACKGROUND.png').convert('RGBA')
    # Native concept is retained as a separate file; only this new composition has text.
    layer(im, 'branding/title_wordmark.png', (38, 200), (650, 273))
    layer(im, 'branding/title_tagline_lockup.png', (38, 490), (650, 59))
    label(im, (44, 38), 'TITLE COMPOSITION / ART MOCKUP', 16, 'moon_cream')
    d = ImageDraw.Draw(im)
    # High-resolution menu lettering remains separate from the illustration.
    for i, (text, enabled) in enumerate([('New Game', True), ('Continue', False), ('Settings', True), ('Credits', True)]):
        y = 610 + i * 57
        if i == 0:
            d.rounded_rectangle((199, y - 5, 525, y + 41), radius=3, fill=P['deep_plum'], outline=P['blush'], width=2)
            d.polygon([(216, y + 11), (223, y + 17), (216, y + 23)], fill=P['paper'])
        f = font(22)
        box = d.textbbox((0, 0), text, font=f)
        d.text((362 - (box[2] - box[0]) / 2, y), text, font=f, fill=P['paper' if enabled else 'slate_violet'])
    label(im, (44, im.height - 38), 'Static art composition • layered sources retained • unapproved', 16, 'moon_cream')
    im.convert('RGB').save(REVIEW / 'TITLE_MENU_COMPOSITION.png')
    # Editable composition references files without baking text into the scene.
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{im.width}" height="{im.height}" viewBox="0 0 {im.width} {im.height}">',
           '<title>The House That Ate Tomorrow — static title composition</title>',
           f'<image href="../concept/MANSION_TITLE_BACKGROUND.png" width="{im.width}" height="{im.height}"/>',
           '<image href="../branding/title_wordmark_outlined.svg" x="38" y="200" width="650" height="273"/>',
           '<image href="../branding/title_tagline_lockup_outlined.svg" x="38" y="490" width="650" height="59"/>',
           '<g font-family="DejaVu Sans" fill="' + P['paper'] + '">',
           '<text x="44" y="54" font-size="16">TITLE COMPOSITION / ART MOCKUP</text>']
    for i, text in enumerate(['New Game', 'Continue', 'Settings', 'Credits']):
        y = 610 + i * 57
        if i == 0:
            svg.append(f'<rect x="199" y="{y-5}" width="326" height="46" rx="3" fill="{P["deep_plum"]}" stroke="{P["blush"]}" stroke-width="2"/>')
            svg.append(f'<path d="M216 {y+11} l7 6 l-7 6Z"/>')
        color = P['slate_violet'] if i == 1 else P['paper']
        svg.append(f'<text x="362" y="{y+21}" text-anchor="middle" font-size="22" fill="{color}">{html.escape(text)}</text>')
    svg.extend(['</g>', '</svg>'])
    (REVIEW / 'TITLE_MENU_COMPOSITION.svg').write_text('\n'.join(svg) + '\n')
    (REVIEW / 'TITLE_MENU_COMPOSITION.json').write_text(json.dumps({
        'classification': 'Static layered art mockup, not runtime UI', 'dimensions': list(im.size),
        'layers': ['../concept/MANSION_TITLE_BACKGROUND.png', '../branding/title_wordmark_outlined.svg', '../branding/title_tagline_lockup_outlined.svg', 'editable menu labels'],
        'source': '../source/build_review.py', 'title': TITLE, 'tagline': TAGLINE,
        'tagline_effective_font_px': 20.15, 'body_font_px': 22, 'status': 'REVIEW_REQUIRED',
        'svg_note': 'SVG preserves editable composition; small font-rasterization differences from PNG are expected.'
    }, indent=2) + '\n')


def palette():
    im = Image.new('RGBA', (1280, 620), P['ink'])
    label(im, (40, 26), 'THE HOUSE / NATIVE PALETTE', 30, serif=True)
    label(im, (40, 74), '16 exact colors • warm Here / spectral Almost • original pixel-art samples', 18, 'blush')
    d = ImageDraw.Draw(im)
    for i, (name, value) in enumerate(P.items()):
        x, y = 40 + (i % 8) * 151, 134 + (i // 8) * 183
        d.rectangle((x, y, x+130, y+88), fill=value, outline=P['moon_cream'])
        label(im, (x, y+101), name.replace('_', ' '), 15)
        label(im, (x, y+127), value, 16, 'moon_cream')
    label(im, (40, 520), 'Native assets: binary alpha, integer pixels, nearest scaling. Illustration and typography use separate rules.', 17)
    label(im, (40, 554), 'World tiles 16×16  /  Visitor 24×32  /  Fig 24×24  /  portraits 64×64', 18, 'blush')
    im.convert('RGB').save(REVIEW / 'ART_PALETTE.png')


def contact_sheet():
    im = Image.new('RGBA', (1720, 1920), P['ink'])
    label(im, (40, 28), TITLE, 38, serif=True)
    label(im, (40, 84), 'ART REVIEW 01 • original concepts + native pixel samples • 27 October 2026 • unapproved', 20, 'blush')
    label(im, (40, 135), '01 / SEPARATE SCENERY, TITLE AND TAGLINE', 18, 'moon_cream')
    layer(im, 'review/TITLE_MENU_COMPOSITION.png', (40, 173), (1003, 565))
    label(im, (1100, 174), 'NATIVE PALETTE', 23, serif=True)
    d = ImageDraw.Draw(im)
    for i, (name, value) in enumerate(P.items()):
        x, y = 1100 + (i % 4)*140, 222 + (i//4)*62
        d.rectangle((x, y, x+120, y+36), fill=value, outline=P['moon_cream'])
    label(im, (1100, 490), 'Fig / receptionist', 24, serif=True)
    portrait = Image.open(ROOT/'sprites/fig_portraits.png').crop((0, 0, 64, 64)).resize((192,192), Image.Resampling.NEAREST)
    im.alpha_composite(portrait, (1100, 538))
    label(im, (1310, 553), '64×64 portrait', 18)
    label(im, (1310, 587), '3 expressions', 18)
    label(im, (1310, 621), '3× nearest', 18, 'blush')
    label(im, (1310, 669), 'Source PNGs', 18)
    label(im, (1310, 699), 'have real alpha.', 18)
    label(im, (40, 776), '02 / THE HERE', 22, 'candle_amber', True)
    label(im, (888, 776), 'THE ALMOST / SAME COORDINATES', 22, 'ghost_mint', True)
    layer(im, 'concept/HALL_A_HERE_VIEWPORT.png', (40, 818), (768, 432), True)
    layer(im, 'concept/HALL_A_ALMOST_VIEWPORT.png', (888, 818), (768, 432), True)
    label(im, (40, 1270), '384×216 native crop at 2× • built from the modular atlas • static layout, not a game screenshot', 19, 'moon_cream')
    label(im, (40, 1323), '03 / SIX RESIDENTS, ONE PIXEL SCALE', 23, serif=True)
    cast = [('visitor','Visitor'),('fig','Fig'),('miss_thimble','Miss Thimble'),('sir_crumb','Sir Crumb'),('mabel','Mabel'),('auditor','Auditor')]
    for i, (stem, name) in enumerate(cast):
        asset=Image.open(ROOT/f'sprites/{stem}_concept.png').convert('RGBA')
        x=60+i*275
        im.alpha_composite(asset.resize((asset.width*4,asset.height*4),Image.Resampling.NEAREST),(x,1550-asset.height*4))
        label(im,(x,1568),name,20)
        label(im,(x,1600),f'{asset.width}×{asset.height} • 4×',16,'moon_cream')
    label(im, (40, 1672), 'REVIEW NOTES', 21, 'blush', True)
    notes = ['Native sheets, tiles and props are technically checked; all artwork still needs your review.',
             'The mansion is an illustration. Room layouts and UI screens are static art mockups.',
             'Refine lighting, character contrast and NPC anatomy before treating this as final production art.',
             'See ART_REVIEW_REPORT.md for dimensions, tests, sources, fonts, and remaining work.']
    for i, note in enumerate(notes):
        label(im, (40, 1712+i*36), note, 19, 'moon_cream')
    im.convert('RGB').save(REVIEW/'ART_REVIEW_CONTACT_SHEET.png')


def manifest():
    rows=[]
    for path in sorted(ROOT.rglob('*')):
        if path.suffix.lower() not in {'.png','.svg','.gif','.ttf'}:
            continue
        relative=path.relative_to(ROOT).as_posix()
        width=height=frames=''
        if path.suffix.lower() in {'.png','.gif'}:
            with Image.open(path) as asset:
                width,height=asset.size
                frames=getattr(asset,'n_frames',1)
        classification='review presentation'
        source='source/build_review.py'
        status='REVIEW_REQUIRED'
        license_note='Original project art; no blanket distribution license assigned'
        if relative.startswith('sprites/'):
            classification='native pixel sprite sample'
            source='source/draw_characters.py'
            meta=json.loads(path.with_suffix('.json').read_text())
            frames=meta['frame_count']
            if '_concept' in path.stem:
                classification='native static character concept'
        elif relative.startswith(('tiles/','props/')):
            classification='native modular pixel art sample'
            source='source/draw_environment.py'
        elif relative.startswith('ui/'):
            classification='native UI component or icon sample'
            source='source/draw_ui.py'
        elif relative.startswith('branding/fonts/'):
            classification='third-party font dependency'
            source='branding/fonts/LICENSE-DejaVu.txt'
            license_note='DejaVu/Bitstream Vera licenses; bundled unchanged with notices'
            status='LICENSE_INCLUDED'
        elif relative.startswith('branding/'):
            classification='editable branding' if path.suffix=='.svg' else 'high-resolution branding export'
            source='source/draw_branding.py'
            license_note='Original layout and ornaments; DejaVu font license included'
        elif relative.startswith('concept/MANSION'):
            classification='AI-generated illustration concept'
            source='concept/MANSION_TITLE_BACKGROUND.json'
            license_note='OpenAI ImageGen output; not copied game artwork; no rights-clearance claim'
            status='NEEDS_REFINEMENT'
        elif relative.startswith('concept/HALL'):
            classification='static tile-built room art mockup'
            source='source/draw_environment.py'
        elif path.name.startswith(('ENVIRONMENT_','ART_MODE_')):
            source='source/draw_environment.py'
        elif path.name.startswith('CHARACTER_'):
            source='source/draw_characters.py'
        elif path.name.startswith('UI_'):
            source='source/draw_ui.py'
        rows.append({'path':relative,'classification':classification,'status':status,'width_px':width,'height_px':height,'frames':frames,'source':source,'provenance_license':license_note,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    with (ROOT/'manifest.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    print(f'Wrote manifest for {len(rows)} visual/font files.')


if __name__=='__main__':
    title_composition()
    palette()
    contact_sheet()
    manifest()
    print('Built layered menu, palette, contact sheet, and manifest.')
