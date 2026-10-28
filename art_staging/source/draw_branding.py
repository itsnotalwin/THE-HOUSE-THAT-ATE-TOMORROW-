"""Author/export exact-title vector branding. Art only; no gameplay dependencies.

Run: python art_staging/source/draw_branding.py
Dependencies: Pillow, fontTools. Bundled unchanged DejaVu fonts are used.
"""
from pathlib import Path
import json, html, shutil, math
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'art_staging/branding'
OUT.mkdir(exist_ok=True)
FONTS=OUT/'fonts'
FONTS.mkdir(exist_ok=True)
for name in ['DejaVuSerif-Bold.ttf','DejaVuSans.ttf','DejaVuSans-Bold.ttf']:
    target=FONTS/name
    if not target.exists():
        shutil.copyfile(Path('/usr/share/fonts/truetype/dejavu')/name,target)
license_file=FONTS/'LICENSE-DejaVu.txt'
if not license_file.exists():
    license_file.write_text(Path('/usr/share/doc/fonts-dejavu-core/copyright').read_text())
P=json.loads((ROOT/'art_staging/palette.json').read_text())
S=4
TITLE='The House That Ate Tomorrow'
TAGLINE='Tomorrow is missing. The cat denies everything.'

class Art:
    def __init__(self,w,h,title):
        self.w,self.h=w,h
        self.im=Image.new('RGBA',(w*S,h*S),(0,0,0,0))
        self.d=ImageDraw.Draw(self.im)
        self.base=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title)}">',f'<title>{html.escape(title)}</title>', '<style>@font-face {font-family: "House Serif"; src: url("fonts/DejaVuSerif-Bold.ttf");} @font-face {font-family: "House Sans"; src: url("fonts/DejaVuSans.ttf");}</style>']
        self.edit=[]; self.outline=[]
    def both(self,v):
        self.edit.append(v);self.outline.append(v)
    def line(self,pts,color,width=2):
        self.d.line([(round(x*S),round(y*S)) for x,y in pts],fill=color,width=round(width*S),joint='curve')
        p=' '.join(f'{x},{y}' for x,y in pts)
        self.both(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')
    def polygon(self,pts,color):
        self.d.polygon([(round(x*S),round(y*S)) for x,y in pts],fill=color)
        p=' '.join(f'{x},{y}' for x,y in pts)
        self.both(f'<polygon points="{p}" fill="{color}"/>')
    def ellipse(self,box,fill=None,stroke=None,width=2):
        self.d.ellipse(tuple(round(x*S) for x in box),fill=fill,outline=stroke,width=round(width*S))
        x0,y0,x1,y1=box
        self.both(f'<ellipse cx="{(x0+x1)/2}" cy="{(y0+y1)/2}" rx="{(x1-x0)/2}" ry="{(y1-y0)/2}" fill="{fill or "none"}" stroke="{stroke or "none"}" stroke-width="{width}"/>')
    def cubic(self,pts,color,width=2):
        p0,p1,p2,p3=pts
        curve=[]
        for i in range(61):
            t=i/60;u=1-t
            curve.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
        self.d.line([(round(x*S),round(y*S)) for x,y in curve],fill=color,width=round(width*S))
        self.both(f'<path d="M{p0[0]},{p0[1]} C{p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>')
    def text(self,text,size,baseline,color,font_name='DejaVuSerif-Bold.ttf',maxwidth=None):
        font_path=FONTS/font_name
        ft=TTFont(font_path)
        glyphs=ft.getGlyphSet(); cmap=ft.getBestCmap(); upem=ft['head'].unitsPerEm
        advances=[ft['hmtx'][cmap[ord(c)]][0] for c in text]
        width=sum(advances)*size/upem
        if maxwidth and width>maxwidth:
            size=size*maxwidth/width; width=maxwidth
        x=(self.w-width)/2
        font=ImageFont.truetype(str(font_path),round(size*S))
        self.d.text((round(x*S),round(baseline*S)),text,font=font,anchor='ls',fill=color,stroke_width=2*S,stroke_fill=P['deep_plum'],features=['-kern'])
        family='House Serif' if 'Serif' in font_name else 'House Sans'
        self.edit.append(f'<text x="{x:.4f}" y="{baseline}" font-family="{family}" font-size="{size:.4f}" font-kerning="none" fill="{color}" stroke="{P["deep_plum"]}" stroke-width="4" stroke-linejoin="round" paint-order="stroke" textLength="{width:.4f}" lengthAdjust="spacingAndGlyphs">{html.escape(text)}</text>')
        self.outline.append(f'<g aria-label="{html.escape(text)}" fill="{color}" stroke="{P["deep_plum"]}" stroke-width="{4*upem/size:.4f}" stroke-linejoin="round" paint-order="stroke">')
        offset=0
        for c,advance in zip(text,advances):
            pen=SVGPathPen(glyphs)
            glyphs[cmap[ord(c)]].draw(pen)
            if pen.getCommands():
                self.outline.append(f'<path transform="translate({x+offset*size/upem:.6f},{baseline}) scale({size/upem:.8f},{-size/upem:.8f})" d="{pen.getCommands()}"/>')
            offset+=advance
        self.outline.append('</g>')
        return {'text':text,'font':str(font_path.relative_to(OUT)),'font_size':round(size,4),'baseline_y':baseline,'width':round(width,4),'x':round(x,4)}
    def save(self,name,lines):
        # Antialiased display typography, intentionally separate from native pixel art.
        im=self.im.resize((self.w,self.h),Image.Resampling.LANCZOS)
        im.save(OUT/(name+'.png'))
        (OUT/(name+'.svg')).write_text('\n'.join(self.base+self.edit+['</svg>'])+'\n')
        (OUT/(name+'_outlined.svg')).write_text('\n'.join(self.base[:2]+self.outline+['</svg>'])+'\n')
        data={'asset':name,'status':'ART_REVIEW_UNAPPROVED','classification':'high-resolution editable branding, not a native pixel sprite','native_dimensions':[self.w,self.h], 'format':'RGBA PNG + editable text SVG + portable outlined SVG','alpha':'straight alpha, antialiased edges; transparent canvas','source':'../source/draw_branding.py','filter':'smooth downsampling for typography; not nearest-neighbor pixel art','layers':['original vector ornaments','editable font-backed text'], 'text_lines':lines, 'fonts':'fonts/; unchanged DejaVu files with LICENSE-DejaVu.txt','provenance':'Original layout and ornaments authored for this project; lettering uses licensed DejaVu typefaces. No generative text or cropped reference art.','approval':'Human approval not recorded'}
        (OUT/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
        assert im.mode=='RGBA' and im.getextrema()[3][0]==0 and im.getextrema()[3][1]==255
        return im

# Three-line lockup; clock, roofline, leaf flourishes, and unobtrusive Fig cameo.
a=Art(1000,420,TITLE)
rose=P['blush']; gold=P['candle_amber']; paper=P['paper']
# Near-midnight clock centered above the title.
a.ellipse((484,14,516,46),fill=P['deep_plum'],stroke=gold,width=2)
a.ellipse((488,18,512,42),stroke=rose,width=.9)
a.line([(500,30),(499,19)],paper,2)
a.line([(500,30),(499,22)],paper,3)
a.ellipse((498,28,502,32),fill=gold)
for ang in range(0,360,90):
    r=math.radians(ang)
    a.line([(500+11*math.sin(r),30-11*math.cos(r)),(500+13*math.sin(r),30-13*math.cos(r))],gold,1)
# Asymmetrical spires make the frame original without deforming the lettering.
a.line([(441,43),(441,33),(447,24),(455,34),(455,42),(470,42)],rose,1.7)
a.line([(530,42),(548,42),(548,28),(554,17),(561,30),(561,43)],rose,1.7)
a.cubic([(475,35),(421,35),(403,62),(322,48)],rose,1.8)
a.cubic([(525,35),(579,35),(597,62),(678,48)],rose,1.8)
for x,y,sgn in [(364,48,-1),(400,47,-1),(636,48,1),(600,47,1)]:
    a.polygon([(x,y),(x+sgn*10,y-10),(x+sgn*14,y-8),(x+sgn*7,y)],rose)
lines=[]
lines.append(a.text('The House',103,148,paper,maxwidth=840))
lines.append(a.text('That Ate',88,243,paper,maxwidth=720))
lines.append(a.text('Tomorrow',119,354,rose,maxwidth=900))
# Quiet side hairlines around the middle line.
for sgn in [-1,1]:
    a.cubic([(500+sgn*270,207),(500+sgn*328,197),(500+sgn*352,231),(500+sgn*393,212)],rose,2)
    a.ellipse((500+sgn*393-3,209,500+sgn*393+3,215),fill=gold)
# Footer ribbon curves, little cat in the gap.
a.cubic([(110,365),(173,412),(354,377),(461,390)],rose,2.2)
a.cubic([(539,390),(646,377),(827,412),(890,365)],rose,2.2)
a.cubic([(156,385),(112,392),(117,367),(132,370)],rose,1.7)
a.cubic([(844,385),(888,392),(883,367),(868,370)],rose,1.7)
a.ellipse((489,378,511,403),fill=paper)
a.polygon([(490,382),(490,369),(497,375),(504,375),(511,369),(511,383)],paper)
a.cubic([(507,399),(531,406),(533,379),(521,383)],paper,4)
a.line([(498,386),(501,391),(504,386)],P['wine'],2)
a.ellipse((494,380,496,382),fill=P['deep_plum'])
a.ellipse((504,380,506,382),fill=P['deep_plum'])
wordmark=a.save('title_wordmark',lines)

b=Art(1000,90,TAGLINE)
# An open two-sentence lockup has readable text even when rendered at half width.
lines=[b.text('Tomorrow is missing.',31,34,paper,'DejaVuSans.ttf',900),b.text('The cat denies everything.',31,75,paper,'DejaVuSans.ttf',900)]
tagline=b.save('title_tagline_lockup',lines)

# Presentation is kept separate from transparent assets and clearly labelled.
review=Image.new('RGB',(1160,680),P['ink'])
d=ImageDraw.Draw(review)
label=ImageFont.truetype(str(FONTS/'DejaVuSans.ttf'),20)
small=ImageFont.truetype(str(FONTS/'DejaVuSans.ttf'),15)
d.text((40,25),'BRANDING / 01',font=label,fill=P['blush'])
d.text((40,56),'Original font-backed lockup · ART SAMPLE · unapproved',font=small,fill=P['paper'])
review.paste(wordmark,(80,95),wordmark)
review.paste(tagline,(80,532),tagline)
d.text((40,647),'Separate transparent layers · editable SVG + portable outlines · title casing verified',font=small,fill=P['moon_cream'])
review.save(OUT/'branding_review.png')

(OUT/'CONTEXT.md').write_text('''# Branding art samples\n\nExact-title original layout and vector ornaments. Files are staged for human review, not approved production artwork. The text-free mansion background lives separately under `../concept/`.\n\n- `title_wordmark.svg`: editable title text and vector ornaments.\n- `title_wordmark_outlined.svg`: portable glyph outlines; does not require a font installation.\n- `title_wordmark.png`: 1000×420 transparent antialiased export.\n- `title_tagline_lockup.svg`, `_outlined.svg`, `.png`: separate 1000×90 tagline layer.\n- `branding_review.png`: labelled display sample on an ink background.\n- Matching JSON files record content, dimensions, sources, and alpha/filter rules.\n\nRebuild with `python art_staging/source/draw_branding.py` from the repo root. Requires Pillow and fontTools. Text SVGs reference bundled fonts; install the provided fonts if an editor does not support relative font-face URLs, or use the outlined version.\n''')
(OUT/'DESIGN.md').write_text('''# Wordmark design\n\nCream title lines and blush “Tomorrow” use a restrained storybook serif with a near-midnight clock, crooked roof fragments, leaf flourishes, and a small cat cameo. Ornaments leave the letterforms clear. The exact title reads **The House That Ate Tomorrow**. The separate two-line tagline reads **Tomorrow is missing. The cat denies everything.**\n\nThis is an original font-backed lockup, not a claim of custom-drawn type design. DejaVu Serif Bold supplies title letterforms; DejaVu Sans supplies the tagline. Both unmodified fonts are redistributed with their license in `fonts/`. Original ornament/layout work was authored as vectors for this project; no reference game assets or supplied concept crops were used.\n\nBranding uses antialiasing and smooth display resampling for high-resolution typography, unlike the strict native pixel sprites. At 50% export size, tagline text is approximately 15.5px; render at 52% or larger to meet a 16px text target. Display below that size requires a separately rendered larger tagline. Keep the scene background, title, tagline, and menu choices independently editable.\n\nAll exports remain unapproved art samples. The title has not been legally or commercially cleared.\n''')
(FONTS/'CONTEXT.md').write_text('''# Bundled font dependencies\n\nUnchanged DejaVuSerif-Bold.ttf, DejaVuSans.ttf and DejaVuSans-Bold.ttf from the environment's Debian fonts-dejavu-core package. LICENSE-DejaVu.txt preserves the supplied copyright and permission notices. The fonts are dependencies for editable text and deterministic exports, not original character artwork. No blanket license is assigned to other project files.\n''')
(FONTS/'DESIGN.md').write_text('''# Typography roles\n\nDejaVu Serif Bold: decorative title letterforms only. DejaVu Sans: separate readable tagline; the bold face is used for art-review labels. Keep each font unchanged; exported SVG outlines are available for font-independent display. The font license permits redistribution subject to its included notices.\n''')
print('Branding exports created in',OUT)
print('Exact title:',TITLE)
print('Exact tagline:',TAGLINE)
