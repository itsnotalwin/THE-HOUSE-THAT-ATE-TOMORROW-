#!/usr/bin/env python3
"""Original UI art authoring/export only. No gameplay or UI runtime implementation.

Run with Python3 and Pillow from any working directory. Native pixels use the
shared exact palette; typography is deliberately rendered at display resolution.
"""
from pathlib import Path
import json
import hashlib
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'ui'
REVIEW = ROOT / 'review'
COLORS = json.loads((ROOT / 'palette.json').read_text())
C = {k: tuple(bytes.fromhex(v[1:])) + (255,) for k, v in COLORS.items()}
FONT = ROOT / 'branding/fonts/DejaVuSans.ttf'
SERIF = ROOT / 'branding/fonts/DejaVuSerif-Bold.ttf'
CLEAR = (0, 0, 0, 0)
ICON_NAMES = ['mirror', 'book', 'key', 'tea', 'moon', 'letter', 'notebook', 'home', 'sun', 'gear']


def canvas(w, h):
    im = Image.new('RGBA', (w, h), CLEAR)
    return im, ImageDraw.Draw(im)


def font(size, serif=False):
    return ImageFont.truetype(str(SERIF if serif else FONT), size)


def text(d, xy, value, size=20, color='paper', serif=False):
    d.text(xy, value, font=font(size, serif), fill=C[color])


def icon(name):
    im, d = canvas(24, 24)
    def r(box, c): d.rectangle(box, fill=C[c])
    def l(p, c, width=1): d.line(p, fill=C[c], width=width)
    def p(points, c): d.polygon(points, fill=C[c])
    def e(box, c, border=None): d.ellipse(box, fill=C[c], outline=C[border] if border else None)
    if name == 'mirror':
        e((5, 2, 18, 16), 'outline'); e((6, 3, 17, 15), 'candle_amber')
        e((8, 5, 15, 13), 'slate_violet'); l([(9, 8), (12, 5)], 'moon_cream')
        l([(11, 12), (14, 9)], 'spectral_blue'); r((10, 16, 13, 21), 'outline')
        r((11, 16, 12, 20), 'timber'); r((9, 20, 14, 21), 'candle_amber')
    elif name == 'book':
        p([(2, 4), (9, 3), (12, 5), (15, 3), (21, 4), (21, 19), (15, 18), (12, 20), (9, 18), (2, 19)], 'outline')
        p([(3, 5), (9, 4), (11, 6), (11, 17), (8, 16), (3, 17)], 'paper')
        p([(13, 6), (15, 4), (20, 5), (20, 17), (15, 16), (13, 17)], 'candle_amber')
        l([(12, 6), (12, 18)], 'timber')
        for y in (8, 11, 14): l([(5, y), (9, y)], 'timber'); l([(15, y), (18, y)], 'wine')
    elif name == 'key':
        e((3, 3, 12, 12), 'outline'); e((4, 4, 11, 11), 'candle_amber')
        e((6, 6, 9, 9), 'deep_plum'); l([(10, 11), (19, 20)], 'outline', 4)
        l([(10, 11), (19, 20)], 'candle_amber', 2)
        l([(15, 16), (18, 13)], 'candle_amber', 2); l([(18, 19), (21, 16)], 'candle_amber', 2)
        l([(5, 5), (8, 4)], 'paper')
    elif name == 'tea':
        r((4, 8, 16, 17), 'outline'); r((5, 9, 15, 16), 'paper'); r((6, 9, 14, 10), 'timber')
        p([(5, 15), (7, 18), (13, 18), (15, 15)], 'paper')
        d.arc((13, 9, 21, 16), 260, 100, fill=C['paper'], width=2)
        l([(3, 20), (18, 20)], 'candle_amber'); l([(7, 6), (6, 4), (8, 2)], 'moon_cream')
        l([(12, 6), (11, 4), (13, 2)], 'moon_cream')
    elif name == 'moon':
        p([(15, 2), (9, 3), (5, 7), (3, 12), (5, 18), (10, 21), (16, 20), (20, 16), (14, 17), (10, 14), (9, 9), (11, 5)], 'moon_cream')
        l([(5, 9), (5, 14), (7, 17)], 'spectral_blue')
        p([(18, 4), (19, 6), (21, 7), (19, 8), (18, 10), (17, 8), (15, 7), (17, 6)], 'ghost_mint')
    elif name == 'letter':
        r((2, 5, 21, 18), 'outline'); r((3, 6, 20, 17), 'paper')
        l([(3, 7), (11, 13), (20, 7)], 'timber'); l([(3, 17), (9, 12)], 'candle_amber'); l([(20, 17), (14, 12)], 'candle_amber')
        e((10, 11, 14, 15), 'raspberry'); d.point((12, 12), fill=C['blush'])
    elif name == 'notebook':
        r((4, 2, 19, 21), 'outline'); r((5, 3, 18, 20), 'wine'); r((7, 3, 8, 20), 'timber')
        r((10, 6, 16, 12), 'paper'); l([(11, 8), (15, 8)], 'timber'); l([(11, 10), (14, 10)], 'timber')
        r((13, 16, 15, 21), 'blush')
        for y in (5, 10, 15, 19): l([(3, y), (6, y)], 'candle_amber')
    elif name == 'home':
        p([(2, 11), (11, 2), (21, 11), (19, 13), (18, 12), (18, 21), (5, 21), (5, 12), (3, 13)], 'outline')
        p([(4, 10), (11, 4), (19, 10)], 'wine'); r((6, 11, 17, 20), 'timber')
        r((10, 14, 13, 20), 'deep_plum'); r((7, 12, 8, 14), 'candle_amber'); r((15, 12, 16, 14), 'candle_amber')
        r((16, 3, 18, 7), 'wine'); d.point((12, 17), fill=C['paper'])
    elif name == 'sun':
        e((6, 6, 17, 17), 'candle_amber'); e((8, 8, 15, 15), 'paper')
        for a, b in [((11, 2), (11, 4)), ((11, 19), (11, 21)), ((2, 11), (4, 11)), ((19, 11), (21, 11)), ((4, 4), (5, 5)), ((18, 18), (19, 19)), ((4, 19), (5, 18)), ((18, 5), (19, 4))]: l([a, b], 'candle_amber')
    elif name == 'gear':
        p([(9, 2), (14, 2), (14, 5), (17, 6), (20, 5), (22, 9), (19, 11), (19, 14), (21, 16), (18, 20), (15, 18), (13, 19), (13, 22), (8, 21), (8, 18), (5, 17), (3, 19), (1, 14), (4, 12), (4, 9), (2, 7), (6, 4), (8, 6)], 'candle_amber')
        e((7, 7, 16, 16), 'timber'); e((9, 9, 14, 14), 'deep_plum'); l([(9, 3), (12, 3)], 'paper')
    elif name == 'focus_arrow':
        p([(6, 4), (17, 11), (6, 19), (8, 11)], 'blush')
        l([(8, 6), (14, 11)], 'paper')
    return im


def panel(kind='dialogue'):
    w, h = (48, 48) if kind == 'dialogue' else (48, 32)
    im, d = canvas(w, h)
    fill = 'wine' if kind == 'focused' else 'deep_plum'
    edge = 'blush' if kind == 'focused' else ('slate_violet' if kind == 'disabled' else 'timber')
    shape = [(6, 1), (w-7, 1), (w-2, 6), (w-2, h-7), (w-7, h-2), (6, h-2), (1, h-7), (1, 6)]
    d.polygon(shape, fill=C['outline'])
    shape2 = [(6, 3), (w-7, 3), (w-4, 6), (w-4, h-7), (w-7, h-4), (6, h-4), (3, h-7), (3, 6)]
    d.polygon(shape2, fill=C[fill], outline=C[edge])
    d.line([(8, 5), (w-9, 5)], fill=C[edge])
    if kind == 'dialogue':
        for x, y in [(6, 6), (w-7, 6), (6, h-7), (w-7, h-7)]:
            d.polygon([(x, y-2), (x+2, y), (x, y+2), (x-2, y)], fill=C['candle_amber'])
    elif kind == 'focused':
        d.line([(8, h-6), (w-9, h-6)], fill=C['blush'])
    return im


def portrait_frame():
    im, d = canvas(80, 80)
    d.rectangle((2, 2, 77, 77), outline=C['outline'], width=3)
    d.rectangle((4, 4, 75, 75), outline=C['timber'], width=2)
    d.rectangle((7, 7, 72, 72), outline=C['candle_amber'])
    for x, y in [(5, 5), (74, 5), (5, 74), (74, 74)]:
        d.polygon([(x, y-3), (x+3, y), (x, y+3), (x-3, y)], fill=C['blush'])
    return im


def nine_slice(src, size, margin=8, scale=2):
    """Art-only export of a nine-slice source with integer nearest borders."""
    out = Image.new('RGBA', size)
    destmargin = margin * scale
    xs, ys = [0, margin, src.width-margin, src.width], [0, margin, src.height-margin, src.height]
    xd, yd = [0, destmargin, size[0]-destmargin, size[0]], [0, destmargin, size[1]-destmargin, size[1]]
    for row in range(3):
        for col in range(3):
            crop = src.crop((xs[col], ys[row], xs[col+1], ys[row+1]))
            crop = crop.resize((xd[col+1]-xd[col], yd[row+1]-yd[row]), Image.Resampling.NEAREST)
            out.alpha_composite(crop, (xd[col], yd[row]))
    return out


def paste_icon(target, name, xy, scale=2):
    target.alpha_composite(ICONS[name].resize((24*scale, 24*scale), Image.Resampling.NEAREST), xy)


def plate(target, box, kind='dialogue', scale=2):
    x, y, w, h = box
    target.alpha_composite(nine_slice(PANELS[kind], (w, h), 8, scale), (x, y))


def button(target, box, caption, focused=False, body=20):
    plate(target, box, 'focused' if focused else 'normal', scale=1)
    x, y, w, h = box
    if focused: paste_icon(target, 'focus_arrow', (x+12, y+(h-24)//2), 1)
    d = ImageDraw.Draw(target)
    text(d, (x+(45 if focused else 20), y+(h-body)//2-3), caption, body)


def room_preview(mode='HERE'):
    im = Image.open(ROOT / f'concept/HALL_A_{mode}_VIEWPORT.png').convert('RGBA')
    visitor = Image.open(ROOT / 'sprites/visitor_sheet.png').crop((0, 0, 24, 32))
    fig = Image.open(ROOT / 'sprites/fig_sheet.png').crop((0, 0, 24, 24))
    im.alpha_composite(visitor, (181, 141))
    im.alpha_composite(fig, (130, 145))
    return im


def dialogue_sample(w, h):
    compact = w < 1000
    im = Image.new('RGBA', (w, h), C['ink']); d = ImageDraw.Draw(im)
    scale = 2 if compact else 3
    stage = room_preview().resize((384*scale, 216*scale), Image.Resampling.NEAREST)
    sx = (w-stage.width)//2; sy = 52 if compact else 60
    im.alpha_composite(stage, (sx, sy))
    text(d, (32, 15), 'DIALOGUE & FOCUS / ART MOCKUP', 16 if compact else 20, 'blush')
    plate(im, (sx+16, sy+18, 530 if compact else 750, 58 if compact else 68), scale=1)
    paste_icon(im, 'notebook', (sx+30, sy+33), 1)
    d = ImageDraw.Draw(im)
    text(d, (sx+68, sy+30), 'Find a name the Guestbook will accept.', 18 if compact else 24)
    mx = sx+stage.width-(190 if compact else 220)
    plate(im, (mx, sy+18, 174 if compact else 204, 58 if compact else 68), scale=1)
    paste_icon(im, 'sun', (mx+17, sy+33), 1)
    text(d, (mx+55, sy+30), 'The Here', 18 if compact else 22)
    px, py, pw, ph = (32, 318, w-64, 188) if compact else (64, 510, w-128, 206)
    plate(im, (px, py, pw, ph))
    portrait = Image.open(ROOT / 'sprites/fig_portraits.png').crop((0, 0, 64, 64))
    portraitscale = 1 if compact else 2
    fx, fy = (px+24, py+32)
    if compact:
        im.alpha_composite(portrait, (fx+8, fy+8))
        im.alpha_composite(FRAME, (fx, fy))
    else:
        im.alpha_composite(portrait.resize((128, 128), Image.Resampling.NEAREST), (fx+16, fy+16))
        im.alpha_composite(FRAME.resize((160, 160), Image.Resampling.NEAREST), (fx, fy))
    tx = px+(124 if compact else 212)
    body = 18 if compact else 24
    d = ImageDraw.Draw(im)
    text(d, (tx, py+20), 'Fig', 20 if compact else 24, 'candle_amber', True)
    text(d, (tx+56, py+25), 'RECEPTIONIST', 16, 'blush')
    lines = ['The book expects a kind of guest, not a name.', 'Have you tried being someone who might have arrived?']
    for row, value in enumerate(lines): text(d, (tx, py+55+row*(26 if compact else 32)), value, body)
    by = py+(132 if compact else 140)
    button(im, (tx, by, 310 if compact else 390, 40 if compact else 48), 'What should I look for?', True, 17 if compact else 20)
    button(im, (tx+(322 if compact else 408), by, 260 if compact else 350, 40 if compact else 48), "I'll take another look.", False, 17 if compact else 20)
    d = ImageDraw.Draw(im)
    text(d, (32, h-25), 'Static art study · keyboard focus is shown by an arrow and border · no runtime UI', 14 if compact else 16, 'moon_cream')
    return im.convert('RGB')


def notebook_sample(w, h):
    compact = w < 1000
    im = Image.new('RGBA', (w, h), C['ink']); d = ImageDraw.Draw(im)
    text(d, (32, 18), 'NOTEBOOK & INVENTORY / ART MOCKUP', 16 if compact else 20, 'blush')
    left, top = 32 if compact else 64, 68 if compact else 94
    paperw = 560 if compact else 816
    paperh = h-top-(50 if compact else 68)
    d.rectangle((left+5, top+6, left+paperw+5, top+paperh+6), fill=C['deep_plum'])
    d.rectangle((left, top, left+paperw, top+paperh), fill=C['timber'])
    d.rectangle((left+5, top+5, left+paperw-5, top+paperh-5), fill=C['paper'])
    d.line((left+28, top+6, left+28, top+paperh-6), fill=C['candle_amber'], width=2)
    tx = left+48
    text(d, (tx, top+26), 'The Visitor’s notebook', 26 if compact else 36, 'deep_plum', True)
    for i, label in enumerate(['Clues', 'Residents', 'Rooms']):
        xx = tx+i*(138 if compact else 170)
        if i == 0: d.rectangle((xx-9, top+76, xx+(110 if compact else 142), top+112), fill=C['deep_plum'])
        text(d, (xx, top+82), label, 18 if compact else 20, 'paper' if i == 0 else 'deep_plum')
    d.line((tx, top+128, left+paperw-36, top+128), fill=C['timber'])
    text(d, (tx, top+152), '01 / ENTRANCE HALL', 16 if compact else 18, 'wine')
    text(d, (tx, top+184), 'A guest without a name', 24 if compact else 32, 'deep_plum', True)
    body = 18 if compact else 22
    lines = ['The portrait has no name in The Here.', 'In The Almost, it names me THE VISITOR.', 'Fig says the book expects a kind of guest.']
    for i, value in enumerate(lines): text(d, (tx, top+232+i*(30 if compact else 36)), value, body, 'deep_plum')
    by = top+(334 if compact else 382)
    d.rectangle((tx-10, by, left+paperw-34, by+66), fill=C['candle_amber'])
    text(d, (tx+7, by+9), 'NEXT / Return to the Guestbook.', 18 if compact else 22, 'deep_plum')
    text(d, (tx+7, by+35), 'Try the title the portrait revealed.', 16 if compact else 20, 'deep_plum')
    ix = left+paperw+(24 if compact else 38)
    iw = w-ix-(32 if compact else 64)
    plate(im, (ix, top, iw, paperh), scale=1)
    d = ImageDraw.Draw(im)
    text(d, (ix+24, top+26), 'Inventory', 24 if compact else 30, 'paper', True)
    text(d, (ix+24, top+64), '2 items · 6 spaces', 16 if compact else 18, 'moon_cream')
    gap = 12 if compact else 18
    cell = min((iw-48-gap)//2, (paperh-204-gap*2)//3)
    gridx = ix+(iw-(2*cell+gap))//2
    selected = [('mirror', 'Mirror'), ('letter', 'Letter')]
    for row in range(3):
        for col in range(2):
            x = gridx+col*(cell+gap); y = top+104+row*(cell+gap)
            plate(im, (x, y, cell, cell), 'focused' if row==0 and col==0 else 'normal', scale=1)
            if row == 0:
                name, label = selected[col]
                s = 2 if cell >= 90 else 1
                paste_icon(im, name, (x+(cell-24*s)//2, y+12), s)
                d = ImageDraw.Draw(im)
                text(d, (x+(cell-int(d.textlength(label,font=font(16))))//2, y+cell-28), label, 16)
                if col == 0:
                    paste_icon(im, 'focus_arrow', (x+2, y+2), 1)
            else:
                d = ImageDraw.Draw(im)
                d.line((x+cell//2-7,y+cell//2,x+cell//2+7,y+cell//2), fill=C['slate_violet'])
    d = ImageDraw.Draw(im)
    text(d, (ix+24, top+paperh-63), 'Pocket mirror', 18 if compact else 22, 'candle_amber')
    text(d, (ix+24, top+paperh-34), 'Shows what nearly was.', 16 if compact else 18)
    text(d, (32, h-27), 'Static art study · clue text follows the supplied Guestbook puzzle · no inventory code', 14 if compact else 16, 'moon_cream')
    return im.convert('RGB')


def component_review():
    im = Image.new('RGBA', (1366, 880), C['ink']); d = ImageDraw.Draw(im)
    text(d, (40, 24), 'UI / NATIVE COMPONENTS', 28, 'paper', True)
    text(d, (40, 70), '24px icon cells · exact palette · binary alpha · high-resolution typography stays separate', 18, 'blush')
    for i, name in enumerate(ICON_NAMES):
        x = 52+(i%5)*260; y = 124+(i//5)*158
        for yy in range(0, 96, 8):
            for xx in range(0, 96, 8):
                d.rectangle((x+xx,y+yy,x+xx+7,y+yy+7),fill=C['deep_plum' if (xx//8+yy//8)%2 else 'aubergine'])
        paste_icon(im, name, (x, y), 4)
        text(d, (x, y+108), name.replace('_', ' ').title(), 18)
    text(d, (40, 458), 'Nine-slice panel', 22, 'paper', True)
    im.alpha_composite(PANELS['dialogue'].resize((192,192),Image.Resampling.NEAREST),(40,502))
    text(d, (40, 710), '48×48 source · 8px margins', 17, 'moon_cream')
    text(d, (294, 458), 'States / focus uses two cues', 22, 'paper', True)
    button(im, (294, 506, 374, 58), 'Inspect the portrait', True, 21)
    button(im, (294, 584, 374, 58), 'Return to the hall', False, 21)
    plate(im, (294, 662, 374, 58), 'disabled', scale=1)
    text(ImageDraw.Draw(im), (316, 679), 'Continue — no saved game', 20, 'moon_cream')
    text(d, (760, 458), 'Portrait frame', 22, 'paper', True)
    portrait = Image.open(ROOT/'sprites/fig_portraits.png').crop((0,0,64,64))
    im.alpha_composite(portrait.resize((128,128),Image.Resampling.NEAREST),(776,526))
    im.alpha_composite(FRAME.resize((160,160),Image.Resampling.NEAREST),(760,510))
    text(d, (760, 710), '80×80 source · center transparent', 17, 'moon_cream')
    text(d, (40, 795), 'The source PNGs have real alpha. Checkerboards appear only in this review presentation.', 18)
    text(d, (40, 827), 'Review samples, not a running interface. Body text uses bundled, licensed DejaVu Sans.', 17, 'blush')
    return im.convert('RGB')


def contrast(a, b):
    def lum(v):
        rgb = [c/255 for c in C[v][:3]]
        rgb = [c/12.92 if c <= .04045 else ((c+.055)/1.055)**2.4 for c in rgb]
        return .2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2]
    la, lb = sorted([lum(a), lum(b)])
    return round((lb+.05)/(la+.05), 2)


def main():
    OUT.mkdir(exist_ok=True); REVIEW.mkdir(exist_ok=True)
    metadata = []
    assets = {f'icon_{k}':v for k,v in ICONS.items()}
    assets.update({'dialogue_panel':PANELS['dialogue'], 'button_normal':PANELS['normal'], 'button_focused':PANELS['focused'], 'button_disabled':PANELS['disabled'], 'portrait_frame':FRAME})
    atlas = Image.new('RGBA', (24*len(ICON_NAMES),24), CLEAR)
    for col,name in enumerate(ICON_NAMES): atlas.alpha_composite(ICONS[name],(24*col,0))
    assets['icons_sheet'] = atlas
    for name, im in assets.items():
        path = OUT / (name+'.png'); im.save(path)
        info = {'asset':path.name,'native_dimensions':list(im.size),'mode':'RGBA','palette':'../palette.json','alpha':'0 or255, straight alpha','filter':'nearest','status':'ART_REVIEW_REQUIRED','source':'../source/draw_ui.py','provenance':'Original coordinate-authored UI graphics for this project; no third-party artwork sampled.'}
        if name in ['dialogue_panel','button_normal','button_focused','button_disabled']:
            info.update({'nine_slice_margins_px':{'left':8,'top':8,'right':8,'bottom':8},'minimum_output_px':[32,32],'interior':'opaque; clipped outer corners transparent','text':'Separate display-resolution text, never baked in.'})
        elif name=='portrait_frame':info.update({'portrait_content_rect_px':[8,8,64,64],'center':'transparent'})
        elif name=='icons_sheet':info.update({'cell_px':[24,24],'rows':1,'columns':len(ICON_NAMES),'frame_count':len(ICON_NAMES),'frame_order':ICON_NAMES,'frames':[{'name':n,'rect_px':[i*24,0,24,24]} for i,n in enumerate(ICON_NAMES)]})
        else:info.update({'cell_px':[24,24],'frame_count':1,'anchor_px':[12,12]})
        path.with_suffix('.json').write_text(json.dumps(info,indent=2)+'\n')
        metadata.append(info)
    for w,h in [(1366,768),(960,540)]:
        dialogue_sample(w,h).save(REVIEW/f'UI_DIALOGUE_{w}.png')
        notebook_sample(w,h).save(REVIEW/f'UI_NOTEBOOK_{w}.png')
    component_review().save(REVIEW/'UI_COMPONENTS.png')
    valid = []
    for path in sorted(OUT.glob('*.png')):
        im = Image.open(path); pixels = list(im.getdata())
        assert im.mode=='RGBA'
        assert {p[3] for p in pixels} == {0,255}
        assert {p for p in pixels if p[3]} <= set(C.values())
        assert im.getbbox(),path
        valid.append({'file':path.name,'dimensions':list(im.size),'rgba':True,'alpha':[0,255],'exact_palette':True,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    ratios = {'paper_on_deep_plum':contrast('paper','deep_plum'),'paper_on_wine':contrast('paper','wine'),'blush_on_wine':contrast('blush','wine'),'deep_plum_on_paper':contrast('deep_plum','paper'),'moon_cream_on_deep_plum':contrast('moon_cream','deep_plum')}
    assert ratios['paper_on_deep_plum']>=4.5 and ratios['paper_on_wine']>=4.5 and ratios['deep_plum_on_paper']>=4.5
    report={'native_assets':valid,'contrast_ratios':ratios,'dialogue_body_px':{'1366x768':24,'960x540':18},'notebook_body_px':{'1366x768':22,'960x540':18},'control_caption_min_px':16,'presentation_footer_px':14,'typography':'../branding/fonts/DejaVuSans.ttf and DejaVuSerif-Bold.ttf; license at../branding/fonts/LICENSE-DejaVu.txt','status':'Static art samples only; no runtime, keyboard interaction, scaling behavior or accessibility implementation tested.'}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Created17 native UI assets, individual metadata and5 static review images.')
    print('Validated exact palette, RGBA/binary alpha and text contrasts:',ratios)


ICONS = {n:icon(n) for n in ICON_NAMES+['focus_arrow']}
PANELS = {n:panel(n) for n in ['dialogue','normal','focused','disabled']}
FRAME = portrait_frame()
if __name__=='__main__':main()
