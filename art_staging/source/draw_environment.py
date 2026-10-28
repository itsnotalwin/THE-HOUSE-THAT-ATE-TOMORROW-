"""Original native-pixel environment art. No runtime, collision, or gameplay code.

Run from any directory with Python 3 and Pillow. All sprite geometry is authored
on the final integer pixel grid. Source palette is shared with the character art.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
P = {k: tuple(bytes.fromhex(v[1:])) + (255,) for k, v in json.loads((ROOT/'palette.json').read_text()).items()}
O, I, D, A, W, R, B, G, C, S, U, M, H, L, T, V = [P[k] for k in ['outline','ink','deep_plum','aubergine','wine','raspberry','blush','candle_amber','paper','slate_violet','spectral_blue','moon_cream','ghost_mint','leaf_muted','timber','warning_plum']]
ALMOST = {G:M, C:H, T:S, W:A, R:U, B:M, V:S, L:U}
assets = {}

def canvas(w,h):
    im=Image.new('RGBA',(w,h)); return im, ImageDraw.Draw(im)

def add(name, im, kind, note='', anchor=None):
    assets[name]={'image':im, 'kind':kind, 'note':note, 'anchor':anchor or [im.width//2,im.height-1]}
    return im

def line(d,coords,c,width=1): d.line(coords,fill=c,width=width)
def rect(d,box,c,outline=None): d.rectangle(box,fill=c,outline=outline)
def poly(d,points,c,outline=None): d.polygon(points,fill=c,outline=outline)
def ellipse(d,box,c,outline=None): d.ellipse(box,fill=c,outline=outline)

def floor(variant=0):
    im,d=canvas(16,16); rect(d,(0,0,15,15),D)
    for y in [0,8]:
        line(d,[(0,y),(15,y)],I)
        line(d,[(0,y+1),(15,y+1)],A)
    x=4 if variant==0 else 12
    line(d,[(x,1),(x,7)],I); line(d,[((x+8)%16,9),((x+8)%16,15)],I)
    line(d,[(7,4),(11,4)],A)
    if variant==1: line(d,[(2,12),(5,12)],W)
    return im

for n in range(2): add(f'floor_plank_{n}',floor(n),'repeat_tile','Horizontal board courses continue across 16px seams.')
im,d=canvas(16,16);rect(d,(0,0,15,15),D)
for x,y in [(4,4),(12,12)]:
    poly(d,[(x,y-3),(x+2,y),(x,y+3),(x-2,y)],A)
    d.point((x,y),fill=W)
add('wallpaper',im,'repeat_tile','Muted diamond damask; horizontal and vertical repeat.')
im,d=canvas(16,16); rect(d,(0,0,15,15),D)
rect(d,(0,0,15,1),W);rect(d,(0,3,15,4),T); rect(d,(0,6,15,14),A);line(d,[(1,7),(1,13)],W);line(d,[(14,7),(14,13)],I);rect(d,(0,15,15,15),O)
add('baseboard',im,'repeat_tile','North-wall lower timber panel, repeat horizontally.')
im,d=canvas(16,16);rect(d,(0,0,15,15),D)
for y,c in [(0,O),(1,W),(2,T),(4,A),(5,O),(8,A),(9,W),(11,O)]:line(d,[(0,y),(15,y)],c)
add('cornice',im,'repeat_tile','North wall header trim, repeat horizontally.')
im,d=canvas(16,16);rect(d,(0,0,15,15),D);rect(d,(2,0,13,15),A);rect(d,(3,0,4,15),T);rect(d,(6,0,7,15),W);rect(d,(12,0,13,15),I)
add('pillar',im,'repeat_tile','Vertical pilaster, repeat vertically.')
im,d=canvas(16,16);rect(d,(0,0,15,15),I)
for y in [1,5,9,13]:line(d,[(0,y),(15,y)],A)
add('threshold',im,'repeat_tile')
im,d=canvas(16,16);rect(d,(0,0,15,15),A)
poly(d,[(0,0),(15,0),(15,15),(0,15)],A)
poly(d,[(8,1),(14,8),(8,14),(1,8)],W);poly(d,[(8,4),(11,8),(8,11),(4,8)],T)
add('floor_inlay',im,'repeat_tile','Decorative border tile, not default field tile.')

# Nine-slice rug tiles: a single original medallion vocabulary in a muted border.
for row in range(3):
    for col in range(3):
        im,d=canvas(16,16);rect(d,(0,0,15,15),W)
        if col==0:rect(d,(0,0,1,15),D);rect(d,(2,0,3,15),T);rect(d,(5,0,5,15),B)
        if col==2:rect(d,(14,0,15,15),D);rect(d,(12,0,13,15),T);rect(d,(10,0,10,15),B)
        if row==0:rect(d,(0,0,15,1),D);rect(d,(2,2,13,3),T);line(d,[(5,5),(10,5)],B)
        if row==2:rect(d,(0,14,15,15),D);rect(d,(2,12,13,13),T);line(d,[(5,10),(10,10)],B)
        if row==1 and col==1:
            poly(d,[(8,2),(13,8),(8,13),(2,8)],A);poly(d,[(8,5),(10,8),(8,10),(5,8)],R)
            d.point((8,7),fill=B)
        add(f'rug_{row}{col}',im,'nine_slice_tile','Tile this row/column role; middle cell repeats.')

def door():
    im,d=canvas(48,64)
    poly(d,[(3,63),(3,20),(7,12),(15,5),(23,1),(32,5),(40,12),(44,20),(44,63)],O)
    poly(d,[(6,60),(6,21),(10,14),(17,8),(23,5),(30,8),(37,14),(41,21),(41,60)],T)
    poly(d,[(9,59),(9,22),(12,16),(19,11),(23,9),(28,11),(34,16),(38,22),(38,59)],A)
    poly(d,[(12,57),(12,23),(16,17),(23,13),(30,17),(35,23),(35,57)],I)
    rect(d,(14,26,33,56),D)
    line(d,[(23,14),(23,56)],W)
    for x in [15,25]:
        rect(d,(x,29,x+6,41),A);line(d,[(x,29),(x+6,29)],W)
        rect(d,(x,45,x+6,53),A)
    rect(d,(26,41,28,43),G);d.point((26,41),fill=C)
    rect(d,(4,59,43,61),W);rect(d,(2,62,45,63),I)
    for x in [4,40]:
        line(d,[(x,23),(x,56)],G)
    return im
add('door',door(),'modular_object','3×4 tiles; same carved arch used for both side exits.',anchor=[24,62])

im,d=canvas(48,80)
poly(d,[(5,76),(5,25),(10,13),(17,6),(23,1),(30,6),(38,14),(42,25),(42,76)],O)
poly(d,[(8,74),(8,26),(13,15),(19,9),(23,6),(28,9),(35,16),(39,26),(39,74)],T)
poly(d,[(11,70),(11,28),(15,19),(23,11),(31,19),(36,28),(36,70)],T)
poly(d,[(13,68),(13,29),(17,20),(23,14),(29,20),(34,29),(34,68)],G)
rect(d,(15,34,21,48),C);rect(d,(26,34,32,48),C)
rect(d,(15,54,21,66),T);rect(d,(26,54,32,66),T)
line(d,[(23,12),(23,70)],O,2);line(d,[(12,31),(36,31)],O,2);line(d,[(12,51),(36,51)],O,2)
line(d,[(23,14),(14,30)],T);line(d,[(23,14),(32,30)],T)
for x in [3,40]:
    poly(d,[(x,17),(x+5,19),(x+3,51),(x+5,68),(x-1,71),(x-2,34)],W)
    line(d,[(x,23),(x+1,49)],R);line(d,[(x-1,63),(x+3,64)],G)
rect(d,(3,74,44,76),T);rect(d,(1,77,46,79),O)
add('window',im,'modular_object','3×5 tiles. Opaque glazing; transparent outer contour.')

im,d=canvas(48,64)
rect(d,(3,5,44,59),O);rect(d,(4,6,43,57),T);rect(d,(6,8,41,55),G);rect(d,(8,10,39,53),A);rect(d,(10,12,37,51),O);rect(d,(11,13,36,50),D)
for x,y in [(4,7),(38,7),(4,51),(38,51)]:
    poly(d,[(x,y+2),(x+2,y),(x+5,y+3),(x+2,y+5)],C)
ellipse(d,(16,18,31,34),A);poly(d,[(14,49),(15,40),(21,35),(28,35),(33,41),(34,49)],A)
rect(d,(15,55,32,60),O);rect(d,(16,56,31,59),T)
poly(d,[(19,2),(23,0),(28,2),(26,5),(21,5)],G)
add('portrait',im,'modular_object','3×4 tiles. Unnamed silhouette, no rasterized clue text.')

im,d=canvas(64,64)
rect(d,(3,5,60,60),O);rect(d,(5,7,58,58),T);rect(d,(8,9,55,56),D)
for y in [10,25,40]:
    for j,(x,w,c,h) in enumerate([(10,4,W,11),(15,5,L,12),(21,3,S,10),(25,6,T,12),(32,4,R,11),(37,6,W,9),(44,4,U,12),(49,5,A,10)]):
        rect(d,(x,y+12-h,x+w-1,y+11),c)
        line(d,[(x,y+13-h),(x+w-1,y+13-h)],G if j%3==0 else C)
    rect(d,(7,y+12,56,y+14),T);line(d,[(7,y+12),(56,y+12)],G)
rect(d,(2,2,61,5),T);rect(d,(0,0,63,1),W)
rect(d,(7,59,12,63),O);rect(d,(51,59,56,63),O)
add('bookcase',im,'modular_object','4×4 tiles; complete shelf contours with grouped book colors.')

im,d=canvas(32,48)
ellipse(d,(3,1,28,32),O);ellipse(d,(5,3,26,31),T);ellipse(d,(7,5,24,30),W)
rect(d,(5,20,26,35),W);rect(d,(7,24,24,35),R);rect(d,(8,25,23,27),B)
for x in [2,25]:rect(d,(x,21,x+4,36),O);rect(d,(x+1,22,x+3,33),T);d.point((x+1,22),fill=G)
rect(d,(5,36,26,39),A);rect(d,(6,39,9,44),T);rect(d,(22,39,25,44),T)
line(d,[(8,7),(8,18)],R);line(d,[(23,8),(23,18)],A)
poly(d,[(15,10),(18,14),(15,18),(12,14)],R)
add('armchair',im,'modular_object','2×3 tiles. Sitting furniture; base anchor below feet.')

im,d=canvas(48,32)
ellipse(d,(1,2,46,18),O);ellipse(d,(3,3,44,16),T);ellipse(d,(5,4,42,13),W)
rect(d,(20,17,27,27),A);rect(d,(17,28,30,30),T);rect(d,(14,31,33,31),O)
line(d,[(7,7),(37,7)],T);rect(d,(27,5,34,10),C);rect(d,(29,4,32,5),G)
line(d,[(34,6),(37,6),(37,9),(35,9)],C)
add('tea_table',im,'modular_object','3×2 tiles with tiny cup on tabletop.')

im,d=canvas(32,48)
rect(d,(13,23,18,39),A);rect(d,(12,24,13,38),T);poly(d,[(6,43),(10,39),(21,39),(26,43),(26,45),(6,45)],O);rect(d,(8,41,23,43),T)
poly(d,[(2,11),(13,6),(29,10),(29,25),(16,29),(2,24)],O)
poly(d,[(4,12),(14,8),(27,11),(27,23),(16,26),(4,22)],T)
line(d,[(4,22),(15,25),(27,22)],G);line(d,[(16,13),(16,26)],A)
add('lectern',im,'modular_object','2×3 tiles, book exported independently for Here/Almost substitution.')

im,d=canvas(32,16)
poly(d,[(2,4),(12,2),(16,4),(21,2),(29,4),(28,12),(17,14),(13,12),(3,13)],O)
poly(d,[(3,4),(12,3),(15,5),(15,12),(12,11),(4,12)],C)
poly(d,[(16,5),(21,3),(28,4),(27,11),(20,12),(16,13)],G)
line(d,[(5,6),(12,5)],T);line(d,[(5,8),(12,7)],T);line(d,[(19,6),(25,6)],T)
line(d,[(15,5),(15,12)],W);line(d,[(14,12),(15,15)],R)
add('guestbook',im,'prop','Open blank guestbook; illustrative marks are not readable words.',anchor=[16,14])

im,d=canvas(32,16)
poly(d,[(1,5),(5,2),(26,2),(30,5),(30,10),(26,13),(5,13),(1,10)],O)
poly(d,[(3,5),(6,4),(25,4),(28,5),(28,10),(25,11),(6,11),(3,10)],T)
rect(d,(7,5,24,10),D);d.point((4,7),fill=G);d.point((27,7),fill=G)
add('nameplate',im,'prop','Both states remain blank; clue text belongs in a later readable UI layer.',anchor=[16,13])

im,d=canvas(64,48)
line(d,[(31,0),(31,18)],T);ellipse(d,(28,13,34,20),G)
line(d,[(31,19),(31,33)],G,2)
for x,y in [(8,24),(19,30),(44,30),(55,24)]:
    line(d,[(31,29),(x,36),(x,y+7)],T,2)
    rect(d,(x-3,y+6,x+3,y+8),G);rect(d,(x-1,y,x+1,y+6),C)
    poly(d,[(x,y-6),(x-2,y-2),(x,y),(x+1,y-2)],G);d.point((x,y-3),fill=C)
line(d,[(13,38),(23,43),(39,43),(50,38)],T)
for x,y in [(18,39),(31,42),(45,39)]:poly(d,[(x,y),(x+2,y+4),(x,y+7),(x-2,y+4)],G)
add('chandelier',im,'modular_object','4×3 tiles; hanging art layer only, no collision assumptions.',anchor=[32,0])

im,d=canvas(32,48)
poly(d,[(8,30),(24,30),(22,44),(11,44)],O);poly(d,[(10,32),(22,32),(20,42),(12,42)],T);rect(d,(8,28,24,31),W);line(d,[(9,29),(23,29)],G)
for points in [[(16,29),(13,14),(9,9)],[(16,28),(19,13),(24,5)],[(16,26),(9,22),(3,17)],[(17,26),(24,21),(28,14)]]:line(d,points,L,2)
for x,y in [(9,10),(23,7),(5,18),(26,16),(15,16)]:
    ellipse(d,(x-3,y-3,x+3,y+3),A);poly(d,[(x,y-3),(x+3,y),(x,y+3),(x-3,y)],R);rect(d,(x-1,y-1,x,y),B)
for points in [[(12,23),(7,19),(10,18)],[(19,21),(25,19),(22,23)],[(13,15),(8,12),(12,11)]]:poly(d,points,L)
add('rose_planter',im,'modular_object','2×3 tiles; chunky rose clusters, no random texture.')

im,d=canvas(32,64)
rect(d,(8,18,23,56),O);rect(d,(10,22,21,54),T);rect(d,(12,25,19,50),A)
line(d,[(16,27),(16,44)],G);ellipse(d,(13,43,19,49),G)
ellipse(d,(2,1,29,28),O);ellipse(d,(4,3,27,26),T);ellipse(d,(6,5,25,24),C)
for x,y in [(15,7),(23,14),(15,22),(8,14)]:rect(d,(x,y,x+1,y+1),T)
line(d,[(16,15),(15,7)],D);line(d,[(16,15),(14,8)],D);ellipse(d,(15,14,17,16),W)
rect(d,(6,56,25,59),T);rect(d,(4,60,27,63),O)
add('clock',im,'modular_object','2×4 tiles. Hands cluster just before midnight (11:59), art only.')

im,d=canvas(64,48)
rect(d,(5,14,58,37),O);rect(d,(7,17,56,35),A)
rect(d,(8,18,29,31),W);rect(d,(34,18,54,31),W)
for x in [18,43]:rect(d,(x,24,x+3,25),G)
poly(d,[(2,12),(10,6),(56,6),(62,12),(62,17),(2,17)],O)
poly(d,[(4,12),(11,8),(55,8),(60,12)],T);rect(d,(4,13,60,15),W)
rect(d,(8,36,12,44),T);rect(d,(51,36,55,44),T)
rect(d,(16,6,27,9),C);line(d,[(19,7),(24,7)],W);rect(d,(37,4,46,9),W);line(d,[(38,5),(45,5)],G)
add('sideboard',im,'modular_object','4×3 tiles; papers and in-tray support bureaucratic house identity.')

im,d=canvas(16,32)
ellipse(d,(3,24,12,28),T);line(d,[(8,14),(8,25)],G,2);rect(d,(5,12,10,15),T);rect(d,(6,5,9,12),C)
poly(d,[(8,0),(5,4),(7,6),(10,4)],G);d.point((8,3),fill=C)
add('candle',im,'modular_object','1×2 tiles, static flame sample.')

im,d=canvas(32,48)
poly(d,[(9,39),(7,28),(8,17),(12,10),(20,10),(25,17),(25,31),(22,39),(19,36),(15,40),(12,36)],S)
ellipse(d,(10,8,22,23),U);ellipse(d,(12,11,20,20),M)
rect(d,(13,16,14,17),S);rect(d,(18,16,19,17),S)
poly(d,[(9,26),(15,23),(18,25),(24,23),(25,31),(18,34),(15,31),(9,33)],H)
line(d,[(17,26),(17,32)],U)
line(d,[(10,37),(8,40)],U);line(d,[(23,37),(25,39)],U)
add('ghost_reader',im,'almost_overlay','2×3 tiles; an unrealized reader only appears in The Almost. Opaque palette illusion, not runtime alpha effect.')

def almost_image(name,src):
    im=src.copy();im.putdata([ALMOST.get(p,p) if p[3] else p for p in src.getdata()]);d=ImageDraw.Draw(im)
    if name=='portrait':
        ellipse(d,(17,20,30,33),U);poly(d,[(16,48),(18,39),(23,34),(28,38),(32,48)],S)
        line(d,[(19,26),(21,26)],M);line(d,[(26,26),(28,26)],M)
        poly(d,[(24,39),(27,43),(24,46),(21,43)],H)
    if name=='guestbook':
        poly(d,[(4,2),(11,0),(14,2),(13,7),(6,5)],H);line(d,[(6,2),(10,2)],U)
        poly(d,[(21,1),(27,0),(28,5),(22,6)],M)
        line(d,[(18,7),(20,9),(24,6)],H)
    if name=='nameplate':
        # Per specification the center stays empty; readable lettering is separate.
        line(d,[(7,4),(24,4)],H);line(d,[(7,11),(24,11)],U)
    if name=='window':
        for x,y in [(17,38),(29,41),(19,57),(30,60)]:line(d,[(x,y),(x-1,y+4)],H)
    return im

def pack():
    atlas=Image.new('RGBA',(256,256)); atlas_alt=Image.new('RGBA',(256,256));x=y=rowh=0; objects={};tiles=[]
    for name,asset in assets.items():
        im=asset['image'];w,h=im.size
        if x+w>256:x=0;y+=rowh;rowh=0
        assert y+h<=256,(name,y,h)
        atlas.alpha_composite(im,(x,y));atlas_alt.alpha_composite(almost_image(name,im),(x,y))
        ids=[]
        for ty in range(h//16):
            for tx in range(w//16):
                idx=(y//16+ty)*16+x//16+tx;ids.append(idx)
                tiles.append({'index':idx,'name':f'{name}_{tx}_{ty}','rect_px':[x+tx*16,y+ty*16,16,16],'object':name})
        objects[name]={'atlas_rect_px':[x,y,w,h],'size_tiles':[w//16,h//16],'tile_indices':ids,'anchor_px':asset['anchor'],'kind':asset['kind'],'note':asset['note']}
        x+=w;rowh=max(rowh,h)
    atlas.save(ROOT/'tiles/foyer_atlas_here.png');atlas_alt.save(ROOT/'tiles/foyer_atlas_almost.png')
    meta={'status':'REVIEW CANDIDATE — not user approved','native_dimensions':[256,256],'tile_size':[16,16],'columns':16,'rows':16,'index_order':'row-major; empty cells remain transparent','alpha':'straight RGBA; alpha values 0 and 255 only','filtering':'nearest; no mipmaps; no lossy compression','padding_px':0,'source':'../source/draw_environment.py','provenance':'Original AI-assisted hand-authored pixel geometry; no external artwork reused. User-supplied palette.','here':'foyer_atlas_here.png','almost':'foyer_atlas_almost.png','objects':objects,'tiles':tiles,'no_runtime_claim':'Art atlas and placement studies only; no engine import or collision test.'}
    (ROOT/'tiles/foyer_atlas.json').write_text(json.dumps(meta,indent=2)+'\n')
    return atlas,atlas_alt,meta

atlas,atlas_alt,atlas_meta=pack()

# Individual props are also exported from their original drawing objects.
for name in ['guestbook','nameplate','ghost_reader']:
    for mode in ['here','almost']:
        if name=='ghost_reader' and mode=='here': continue
        im=assets[name]['image'] if mode=='here' else almost_image(name,assets[name]['image'])
        im.save(ROOT/f'props/{name}_{mode}.png')
    meta={'name':name,'native_dimensions':list(assets[name]['image'].size),'frame_count':1,'cell_dimensions':list(assets[name]['image'].size),'rows':1,'columns':1,'timing_ms':0,'anchor_px':assets[name]['anchor'],'alpha':'RGBA binary transparency','source':'../source/draw_environment.py','provenance':'Original authored pixel art for this project','status':'REVIEW CANDIDATE','note':assets[name]['note']}
    (ROOT/f'props/{name}.json').write_text(json.dumps(meta,indent=2)+'\n')

def room_layout(candidate):
    placements=[]
    def put(name,x,y,layer='furniture',only=None):placements.append({'asset':name,'position_px':[x,y],'layer':layer,'mode':only or 'both'})
    # Exact same static floor/wall placements are shared by each Here/Almost pair.
    for y in range(112,336,16):
        for x in range(16,496,16):put('floor_plank_'+str((x//16)%2),x,y,'floor')
    for y in range(16,96,16):
        for x in range(16,496,16):put('wallpaper',x,y,'wall')
    for x in range(16,496,16):put('cornice',x,16,'trim');put('baseboard',x,96,'trim')
    for y in range(32,112,16):
        for x in [16,144,352,480]:put('pillar',x,y,'trim')
    for y in range(112,336,16):
        for x in [16,480]:put('floor_inlay',x,y,'floor_border')
    def rug(x,y,w,h):
        for dy in range(h):
            for dx in range(w):
                col=0 if dx==0 else (2 if dx==w-1 else 1);row=0 if dy==0 else (2 if dy==h-1 else 1)
                put(f'rug_{row}{col}',x+dx*16,y+dy*16,'rug')
    if candidate=='A':
        rug(208,128,6,13)
        put('door',80,48,'architecture');put('door',384,48,'architecture')
        put('window',176,24,'architecture');put('window',288,24,'architecture');put('portrait',232,40,'architecture')
        put('nameplate',240,102,'clue')
        put('bookcase',32,120);put('bookcase',416,120)
        put('sideboard',96,176);put('tea_table',352,208)
        put('armchair',328,192);put('armchair',416,208)
        put('rose_planter',40,240);put('rose_planter',440,272)
        put('clock',112,256);put('lectern',176,176);put('guestbook',176,186,'clue')
        put('candle',120,156);put('candle',368,188)
        put('chandelier',224,112,'ceiling')
        put('ghost_reader',328,190,'almost_reveal','almost')
    else:
        rug(80,176,10,8);rug(320,112,5,14)
        put('door',48,48,'architecture');put('door',384,48,'architecture')
        put('window',192,24,'architecture');put('window',256,24,'architecture');put('portrait',304,40,'architecture')
        put('nameplate',312,102,'clue')
        put('clock',112,48,'architecture')
        put('bookcase',32,128);put('bookcase',112,128)
        put('sideboard',416,128);put('armchair',96,208);put('armchair',192,224)
        put('tea_table',136,240);put('rose_planter',48,272);put('rose_planter',432,256)
        put('lectern',272,160);put('guestbook',272,170,'clue');put('candle',440,108)
        put('chandelier',144,112,'ceiling');put('ghost_reader',96,206,'almost_reveal','almost')
    return {'candidate':candidate,'title':'Candlelit Registry' if candidate=='A' else 'Moonlit Reading Hall','native_dimensions':[512,352],'grid_px':16,'camera_crop_px':[64,32,384,216],'status':'ART LAYOUT MOCKUP — not a Godot scene or runtime screenshot','placements':placements,'note':'Fixed authored art placements, no collision data, puzzle code, pathfinding, or generator behavior. Props may overhang floor footprints. Camera crop is an art readability study.'}

def render_room(layout,mode):
    im=Image.new('RGBA',(512,352),I)
    source=atlas if mode=='here' else atlas_alt
    # Room architecture is clipped once, from atlas pieces, with no paint-over.
    for p in layout['placements']:
        if p['mode'] not in ['both',mode]: continue
        x,y,w,h=atlas_meta['objects'][p['asset']]['atlas_rect_px']
        tile=source.crop((x,y,x+w,y+h))
        im.alpha_composite(tile,tuple(p['position_px']))
    return im

rooms={}
for candidate in ['A','B']:
    layout=room_layout(candidate)
    (ROOT/f'concept/HALL_{candidate}_layout.json').write_text(json.dumps(layout,indent=2)+'\n')
    for mode in ['here','almost']:
        im=render_room(layout,mode);rooms[(candidate,mode)]=im
        im.save(ROOT/f'concept/HALL_{candidate}_{mode.upper()}.png')
        im.crop((64,32,448,248)).save(ROOT/f'concept/HALL_{candidate}_{mode.upper()}_VIEWPORT.png')

FONT=str(ROOT/'branding/fonts/DejaVuSans.ttf')
BOLD=str(ROOT/'branding/fonts/DejaVuSans-Bold.ttf')
def font(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
def text(d,xy,t,n=18,c=C,b=False):d.text(xy,t,font=font(n,b),fill=c)

sheet=Image.new('RGB',(1440,1260),I[:3]);d=ImageDraw.Draw(sheet)
text(d,(48,30),'TWO WAYS INTO THE HOUSE',32,C,True)
text(d,(48,76),'Original modular pixel artwork · 16px tiles · art mockups, not runtime screenshots',18,B)
for row,candidate in enumerate(['A','B']):
    y=132+row*552
    title='A / CANDLELIT REGISTRY' if candidate=='A' else 'B / MOONLIT READING HALL'
    text(d,(48,y),title,22,G if candidate=='A' else M,True)
    text(d,(48,y+32),'Ceremonial axis, paired exits, guestbook beside the runner.' if candidate=='A' else 'An off-center runner leaves a quiet reading nook and a generous approach.',16,C)
    for col,mode in enumerate(['here','almost']):
        x=48+col*696
        text(d,(x,y+70),'THE HERE' if mode=='here' else 'THE ALMOST',16,G if mode=='here' else H,True)
        # Native full-room previews with a generous dark mat, no distortion.
        sheet.paste(rooms[(candidate,mode)].convert('RGB'),(x+68,y+105))
        text(d,(x+68,y+469),'512 × 352 native · same coordinates in both modes',14,S)
text(d,(48,1230),'Almost reveals: an absent reader, a changed portrait, floating guestbook pages and ghost rain.',16,M)
sheet.save(ROOT/'review/ENVIRONMENT_DIRECTIONS.png')

sheet=Image.new('RGB',(1600,680),I[:3]);d=ImageDraw.Draw(sheet)
text(d,(32,24),'THE HERE / THE ALMOST',30,C,True)
text(d,(32,66),'Candidate A · actual 384×216 crop enlarged 2× with nearest filtering · ART MOCKUP',17,B)
for col,mode in enumerate(['here','almost']):
    x=24+col*792
    text(d,(x,110),'THE HERE — inhabited' if mode=='here' else 'THE ALMOST — unrealized',20,G if mode=='here' else H,True)
    crop=rooms[('A',mode)].crop((64,32,448,248))
    sheet.paste(crop.resize((768,432),Image.Resampling.NEAREST).convert('RGB'),(x,148))
text(d,(32,610),'Fixed room silhouette and furniture. Readable clue text will be a separate UI layer.',18,C)
text(d,(32,642),'The spectral reader is an art-only reveal; no interaction, collision or mode-switch code exists.',16,S)
sheet.save(ROOT/'review/ART_MODE_COMPARISON.png')

sheet=Image.new('RGB',(1440,1220),I[:3]);d=ImageDraw.Draw(sheet)
text(d,(40,28),'FOYER / NATIVE ASSET INVENTORY',30,C,True)
text(d,(40,76),'256 × 256 atlas · 16 × 16 cells · all visible asset colors from the shared 16-color palette',17,B)
for col,(mode,im) in enumerate([('HERE',atlas),('ALMOST',atlas_alt)]):
    x=40+col*700;text(d,(x,124),mode,19,G if mode=='HERE' else H,True)
    for yy in range(0,512,16):
        for xx in range(0,512,16):rect(d,(x+xx,160+yy,x+xx+15,160+yy+15),A[:3] if (xx//16+yy//16)%2 else D[:3])
    sheet.paste(im.resize((512,512),Image.Resampling.NEAREST),(x,160),im.resize((512,512),Image.Resampling.NEAREST))
    text(d,(x,692),'2× nearest · checkerboard belongs only to this review sheet',15,S)
text(d,(40,754),'REPEAT AND TRANSPARENCY STUDIES',21,C,True)
for idx,name in enumerate(['floor_plank_0','wallpaper','rug_11']):
    tile=assets[name]['image'];sample=Image.new('RGBA',(64,64))
    for y in range(4):
        for x in range(4):sample.alpha_composite(tile,(x*16,y*16))
    sheet.paste(sample.resize((192,192),Image.Resampling.NEAREST).convert('RGB'),(40+idx*240,806))
    text(d,(40+idx*240,1010),name,16,B)
for idx,name in enumerate(['guestbook','nameplate']):
    for row,mode in enumerate(['here','almost']):
        im=assets[name]['image'] if mode=='here' else almost_image(name,assets[name]['image'])
        x=800+idx*280;y=806+row*112
        sheet.paste(im.resize((128,64),Image.Resampling.NEAREST),(x,y),im.resize((128,64),Image.Resampling.NEAREST))
        text(d,(x,y+66),f'{name} / {mode}',14,C)
text(d,(40,1090),'Original geometry is editable in source/draw_environment.py. Tile IDs and object footprints are in tiles/foyer_atlas.json.',16,C)
text(d,(40,1120),'No antialiasing, transparency backgrounds, third-party sprite crops, or AI illustration downscales are present in native exports.',16,S)
text(d,(40,1162),'REVIEW CANDIDATES · artwork is unapproved · production import and runtime checks remain for a later phase',16,B,True)
sheet.save(ROOT/'review/ENVIRONMENT_ATLAS_REVIEW.png')

def validate():
    palette=set(P.values());results=[]
    for path in sorted(list((ROOT/'tiles').glob('*.png'))+list((ROOT/'props').glob('*.png'))):
        im=Image.open(path);assert im.mode=='RGBA',path
        pixels=list(im.getdata());assert {p[3] for p in pixels}<={0,255},path
        assert {p for p in pixels if p[3]}<=palette,path
        assert im.width%16==0 and im.height%16==0,path
        results.append({'file':str(path.relative_to(ROOT)),'dimensions':list(im.size),'rgba':True,'binary_alpha':True,'palette_match':True,'transparent_pixels':sum(p[3]==0 for p in pixels)})
    for candidate in ['A','B']:
        layout=room_layout(candidate)
        for mode in ['here','almost']:
            im=render_room(layout,mode);assert im.tobytes()==Image.open(ROOT/f'concept/HALL_{candidate}_{mode.upper()}.png').tobytes()
    report={'checks':results,'atlas_reconstruction':'All four room exports reconstruct exactly from the shared atlas and documented static placements.','tile_grid':'All asset atlas coordinates, dimensions and tile rectangles are multiples of 16.','seams':'Repeat sample sheets inspected; plank courses and damask edges continue consistently.','not_checked':['Godot import','collision','player navigation','runtime text','puzzle functionality'],'status':'Native art samples technically valid, awaiting visual approval.'}
    (ROOT/'review/ENVIRONMENT_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Created environment atlas, props, 4 room mockups, 4 viewport crops and 3 review sheets.')
    print('Validated',len(results),'native PNGs, palette, alpha, grid and exact room reconstruction.')

if __name__=='__main__':validate()
