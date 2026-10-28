"""Author the native first-slice street using original geometry and approved tiles.

The background is 512x352, uses the approved 16-colour palette, and contains no
characters. The mailbox and sign footprints are documented in the room data.
Run with Python 3 + Pillow from any directory. No downloaded artwork is used.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
P = json.loads((ROOT/'art_staging/palette.json').read_text())
C = {k: tuple(bytes.fromhex(v[1:]))+(255,) for k,v in P.items()}
im = Image.new('RGBA',(512,352),C['ink'])
d = ImageDraw.Draw(im)

def rect(box,c): d.rectangle(box,fill=C[c])
def line(points,c,w=1): d.line(points,fill=C[c],width=w)
def poly(points,c): d.polygon(points,fill=C[c])
def ellipse(box,c): d.ellipse(box,fill=C[c])

# A few broad clouds frame the small rose moon; no random grain or bright noise.
poly([(0,10),(72,10),(110,24),(185,24),(205,35),(0,35)],'deep_plum')
poly([(274,10),(323,10),(344,24),(442,24),(478,40),(512,40),(512,52),(300,52)],'deep_plum')
ellipse((365,16,407,58),'wine')
ellipse((370,18,405,53),'blush')
ellipse((373,22,385,32),'raspberry')
ellipse((394,36,402,44),'raspberry')
ellipse((382,40,391,49),'raspberry')

# Quiet ordinary neighbours, cropped at the street edges.
for x,w,h in [(0,96,92),(430,82,115)]:
 rect((x,176-h,x+w,175),'deep_plum')
 rect((x,176-h,x+w,181-h),'slate_violet')
 rect((x+4,184-h,x+w-4,175),'ink')
 for yy in [176-h+26,176-h+65]:
  for xx in range(x+17,x+w-12,31):
   rect((xx,yy,xx+14,yy+23),'deep_plum')
   rect((xx+2,yy+2,xx+12,yy+20),'slate_violet')
   rect((xx+3,yy+3,xx+7,yy+11),'spectral_blue')
   line([(xx+7,yy+2),(xx+7,yy+21)],'ink')
   line([(xx+2,yy+12),(xx+12,yy+12)],'ink')
 for yy in range(176-h+15,175,16):
  line([(x+4,yy),(x+w-4,yy)],'deep_plum')

# Crooked mansion: mansard silhouette, asymmetric turrets, carved warm entrance.
poly([(94,83),(117,74),(141,31),(166,75),(208,57),(247,27),(287,64),(321,66),(354,18),(384,69),(418,84),(414,176),(98,176)],'outline')
poly([(105,87),(141,46),(167,86),(210,68),(247,39),(287,75),(325,78),(353,33),(382,80),(405,91),(402,171),(109,171)],'aubergine')
poly([(102,85),(141,31),(171,85)],'ink')
poly([(325,78),(354,18),(388,83)],'ink')
poly([(207,66),(247,27),(290,70)],'deep_plum')
for x,y in [(140,23),(354,9),(247,18)]:
 line([(x,y-5),(x,y+11)],'outline',2)
 line([(x-3,y),(x+3,y)],'outline')
 poly([(x-2,y+5),(x,y+2),(x+2,y+5),(x,y+8)],'timber')
for y,x1,x2 in [(59,126,153),(68,119,159),(75,115,165),(51,339,369),(60,334,376),(69,329,381)]:
 line([(x1,y),(x2,y)],'aubergine')
line([(105,88),(163,88),(163,83),(207,69)],'timber')
line([(291,72),(327,81),(382,84),(406,91)],'timber')
rect((110,92,404,174),'deep_plum')
rect((110,94,404,98),'wine')
rect((110,99,404,101),'timber')
rect((112,106,402,169),'aubergine')
for x in [114,168,218,290,340,396]:
 rect((x,100,x+5,171),'deep_plum')
 rect((x+1,102,x+2,168),'timber')
 rect((x-2,170,x+7,175),'wine')
for yy in [116,132,148,164]:
 for xx in range(120,397,32):
  line([(xx,yy),(xx+18,yy)],'deep_plum')

# Reuse only approved modular pixel assets, preserving their native density.
atlas = Image.open(ROOT/'art_staging/tiles/foyer_atlas_here.png').convert('RGBA')
meta=json.loads((ROOT/'art_staging/tiles/foyer_atlas.json').read_text())
def asset(name,x,y):
 xx,yy,w,h=meta['objects'][name]['atlas_rect_px']
 im.alpha_composite(atlas.crop((xx,yy,xx+w,yy+h)),(x,y))

asset('door',232,112)
asset('window',120,91)
asset('window',176,91)
asset('window',288,91)
asset('window',344,91)
# Narrow upper attic lights and a minute-to-midnight clock.
for x,y in [(135,65),(349,54)]:
 poly([(x,y+20),(x,y+6),(x+5,y),(x+10,y+6),(x+10,y+20)],'outline')
 poly([(x+2,y+17),(x+2,y+7),(x+5,y+3),(x+8,y+7),(x+8,y+17)],'candle_amber')
 line([(x+5,y+3),(x+5,y+17)],'timber')
ellipse((231,59,263,91),'outline')
ellipse((233,61,261,89),'timber')
ellipse((236,64,258,86),'paper')
for point in [(247,66),(256,75),(247,84),(238,75)]:
 d.point(point,fill=C['timber'])
line([(247,75),(246,66)],'deep_plum')
line([(247,75),(247,69)],'outline')
d.point((247,75),fill=C['wine'])

# Stone doorstep and curb are broad horizontal forms, readable below the camera.
rect((224,175,287,183),'outline')
rect((226,175,285,178),'timber')
rect((220,180,291,185),'deep_plum')
line([(222,180),(289,180)],'slate_violet')
rect((0,176,219,181),'slate_violet')
rect((292,176,511,181),'slate_violet')
rect((0,182,511,351),'deep_plum')
line([(0,182),(511,182)],'outline')

# Restrained staggered cobbles; both horizontal repeat and row offset use16px.
for row,y in enumerate(range(184,352,8)):
 for x in range(-16+(row%2)*8,512,16):
  rect((x+1,y,x+14,y+5),'ink')
  line([(x+2,y),(x+12,y)],'aubergine')
  if (x//16+row)%5==0:
   line([(x+3,y+1),(x+7,y+1)],'slate_violet')
# A warmer invitation on the central approach; these are ground markings, not obstacles.
for y,w in [(187,40),(195,45),(203,47),(211,43),(219,39)]:
 line([(256-w//2,y),(256+w//2,y)],'aubergine')
 if y<204: line([(244,y),(268,y)],'timber')

# Rain puddles use bounded, deliberately sparse clusters with clean shapes.
for x,y,w in [(43,294,48),(331,278,56),(192,324,42),(427,224,41)]:
 poly([(x,y+3),(x+8,y),(x+w-6,y),(x+w,y+3),(x+w-12,y+6),(x+5,y+6)],'ink')
 line([(x+7,y+2),(x+w-9,y+2)],'slate_violet')
 line([(x+13,y+4),(x+w-17,y+4)],'aubergine')

# Low iron fences frame the open paving without cutting across the main route.
for start,end in [(7,108),(404,505)]:
 line([(start,168),(end,168)],'outline',2)
 line([(start,181),(end,181)],'outline',2)
 for x in range(start,end+1,10):
  line([(x,151),(x,188)],'outline',2)
  poly([(x,145),(x-3,152),(x+3,152)],'outline')
  d.point((x,151),fill=C['slate_violet'])

# Rose urns stay near the façade, leaving the central walkway and all targets clear.
asset('rose_planter',86,160)
asset('rose_planter',402,160)

# The entry letter waits in a burgundy municipal mailbox. No words baked into art.
rect((158,213,163,237),'outline')
rect((159,213,160,235),'timber')
rect((153,236,168,239),'outline')
poly([(148,213),(148,195),(152,190),(170,190),(174,195),(174,213)],'outline')
poly([(150,211),(150,196),(153,192),(169,192),(172,196),(172,211)],'wine')
line([(152,194),(169,194)],'blush')
rect((152,201,170,204),'outline')
rect((155,201,167,207),'paper')
line([(155,201),(161,205),(167,201)],'timber')
d.point((161,204),fill=C['raspberry'])
line([(171,196),(171,208)],'warning_plum')

# The street sign has a house emblem and blank plate, rendered text appears in UI.
rect((62,229,65,257),'outline')
rect((63,230,63,256),'timber')
poly([(48,218),(52,214),(76,214),(80,218),(80,234),(48,234)],'outline')
rect((50,217,78,231),'timber')
rect((52,219,76,229),'deep_plum')
poly([(60,225),(60,222),(64,219),(68,222),(68,225)],'paper')
rect((63,223,64,225),'deep_plum')

# Two lanterns provide a restrained warm/cold contrast.
for x in [82,426]:
 line([(x,158),(x,218)],'outline',3)
 line([(x,158),(x+7,154)],'timber')
 poly([(x+2,145),(x+7,140),(x+12,145)],'outline')
 rect((x+3,146,x+11,157),'outline')
 rect((x+5,147,x+9,154),'candle_amber')
 rect((x+6,148,x+8,151),'paper')
 line([(x-5,219),(x+5,219)],'outline',2)

OUT=ROOT/'assets/street_background.png'
OUT.parent.mkdir(exist_ok=True)
im.save(OUT)
assert im.size==(512,352)
assert {p for _,p in im.getcolors(im.width*im.height)}<=set(C.values())
print('Exported512x352 native street; exact16-colour palette, original geometry and approved atlas crops, no baked characters.')
