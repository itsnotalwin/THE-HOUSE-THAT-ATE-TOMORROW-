#!/usr/bin/env python3
"""Original coordinate-authored native pixel character studies. Art export only.
Run from any directory; requires Pillow. No reference image is sampled or traced.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'sprites'
REVIEW = ROOT / 'review'
P = json.loads((ROOT / 'palette.json').read_text())
C = {k: tuple(bytes.fromhex(v[1:])) + (255,) for k,v in P.items()}
CLEAR=(0,0,0,0)

class Pixel:
    def __init__(self,w,h):
        self.im=Image.new('RGBA',(w,h),CLEAR); self.d=ImageDraw.Draw(self.im)
    def r(self,box,c): self.d.rectangle(box,fill=C[c])
    def p(self,points,c): self.d.polygon(points,fill=C[c])
    def l(self,points,c,w=1): self.d.line(points,fill=C[c],width=w)
    def e(self,box,c): self.d.ellipse(box,fill=C[c])
    def dot(self,x,y,c): self.d.point((x,y),fill=C[c])


def visitor(direction='south',phase=-1):
    a=Pixel(24,32)
    # One planted foot every frame; stride changes are authored, not translated crops.
    offsets=[(0,0),(-1,1),(0,-1),(1,0),(0,1)]
    q=phase+1
    if direction in ('south','north'):
        ls,rs=offsets[q]
        a.r((8+ls,23,10+ls,28),'outline'); a.r((13+rs,23,15+rs,28),'outline')
        a.r((8+ls,24,10+ls,26),'ink'); a.r((13+rs,24,15+rs,26),'ink')
        a.r((7+ls,28-(q==2),10+ls,29-(q==2)),'outline')
        a.r((13+rs,28-(q==4),16+rs,29-(q==4)),'outline')
        a.l([(8+ls,28-(q==2)),(10+ls,28-(q==2))],'timber')
        a.l([(13+rs,28-(q==4)),(15+rs,28-(q==4))],'timber')
        # Coat silhouette has deliberately asymmetrical hem and shoulder bag.
        a.p([(7,13),(15,13),(17,16),(17,24),(13,25),(11,23),(7,25),(6,22),(6,16)],'outline')
        a.p([(8,14),(14,14),(16,17),(16,23),(13,24),(11,22),(8,24),(7,22),(7,17)],'aubergine')
        a.p([(8,15),(10,15),(10,22),(8,24),(7,22)],'wine')
        a.l([(12,16),(12,22),(13,24)],'deep_plum')
        # Arms alternate opposite the leading foot.
        ly=16 + (1 if q in (1,4) else 0)
        ry=16 + (1 if q in (2,3) else 0)
        a.r((5,ly,7,ly+5),'outline'); a.r((5,ly,6,ly+3),'aubergine')
        a.r((5,ly+4,6,ly+5),'candle_amber'); a.dot(5,ly+4,'paper')
        a.r((16,ry,18,ry+5),'outline'); a.r((17,ry,18,ry+3),'deep_plum')
        a.r((17,ry+4,18,ry+5),'candle_amber')
        if direction=='south':
            a.l([(8,14),(15,20)],'timber')
            a.r((15,19,19,24),'outline'); a.r((16,19,18,23),'timber')
            a.l([(16,20),(18,20)],'candle_amber'); a.dot(17,22,'paper')
            a.dot(12,18,'candle_amber'); a.dot(12,21,'candle_amber')
        else:
            a.l([(15,14),(8,21)],'timber'); a.r((5,20,9,24),'outline'); a.r((6,20,8,23),'timber')
            a.dot(7,21,'candle_amber'); a.l([(10,16),(13,16)],'wine')
        # Neck + scarf, anchored independently of the stepping limbs.
        a.r((9,11,14,14),'outline'); a.r((10,11,13,13),'candle_amber')
        a.r((7,13,15,15),'wine'); a.l([(8,13),(14,13)],'blush')
        a.r((8 if direction=='south' else 13,15,9 if direction=='south' else 14,18+(q%2)),'raspberry')
        a.dot(8 if direction=='south' else 13,15,'blush')
        # Hair/head silhouette, 11 pixels wide, no edge bleed.
        a.p([(8,2),(14,2),(17,5),(17,9),(16,11),(14,13),(9,13),(6,10),(6,5)],'outline')
        if direction=='south':
            a.p([(8,5),(15,5),(16,7),(15,11),(13,12),(10,12),(8,10)],'candle_amber')
            a.r((9,6,14,10),'paper'); a.dot(14,10,'candle_amber')
            a.r((7,6,8,9),'timber'); a.r((15,6,16,9),'timber')
            a.p([(8,3),(14,3),(16,5),(15,7),(13,6),(12,5),(10,7),(8,6),(7,7),(7,5)],'timber')
            a.l([(9,3),(13,3),(15,4)],'candle_amber')
            a.r((10,8,10,9),'outline'); a.r((14,8,14,9),'outline')
            a.dot(12,11,'timber'); a.dot(8,10,'blush')
        else:
            a.p([(8,3),(14,3),(16,5),(16,9),(14,12),(9,12),(7,9),(7,5)],'timber')
            a.p([(8,4),(10,3),(14,3),(15,4),(12,4),(10,6),(8,6)],'candle_amber')
            a.l([(8,8),(9,10),(12,11),(14,9),(15,7)],'deep_plum')
            a.l([(8,7),(8,9)],'wine')
    else:
        # Side body is drawn once, mirrored for facing only; near satchel added below.
        front=[0,2,0,-2,0][q]; back=[0,-1,1,2,-1][q]
        a.p([(10,23),(13,23),(13+front,27),(14+front,28),(14+front,29),(10+front,29),(10+front,27)],'outline')
        a.p([(9,23),(11,23),(10+back,27),(10+back,29),(7+back,29),(7+back,28),(9+back,27)],'outline')
        a.r((10+front,28,13+front,28),'timber'); a.dot(8+back,28,'timber')
        a.p([(8,13),(14,13),(16,17),(15,24),(10,25),(7,23),(7,17)],'outline')
        a.p([(9,14),(13,14),(15,17),(14,23),(11,24),(8,23),(8,17)],'aubergine')
        a.l([(13,16),(14,21),(13,23)],'wine'); a.l([(9,18),(9,22)],'deep_plum')
        ay=16+(q in (1,4))
        ax=[0,-1,0,1,0][q]
        a.p([(10+ax,ay),(12+ax,ay),(13+ax,ay+5),(11+ax,ay+7),(9+ax,ay+6)],'outline')
        a.r((10+ax,ay+1,11+ax,ay+4),'wine'); a.r((10+ax,ay+5,11+ax,ay+6),'candle_amber')
        a.r((10,11,13,14),'candle_amber'); a.r((8,13,14,15),'wine'); a.l([(9,13),(13,13)],'blush')
        a.r((7,15,8,18+(q%2)),'raspberry')
        a.p([(8,2),(13,2),(16,5),(16,7),(18,8),(18,9),(16,10),(15,12),(10,13),(7,10),(6,6)],'outline')
        a.p([(11,5),(15,5),(15,8),(17,8),(17,9),(15,9),(14,11),(12,12),(10,10)],'candle_amber')
        a.r((12,6,15,9),'paper'); a.dot(14,8,'outline'); a.dot(14,11,'timber')
        a.p([(8,3),(13,3),(15,5),(12,5),(11,7),(10,9),(10,11),(8,10),(7,7),(7,5)],'timber')
        a.l([(8,4),(10,3),(12,3)],'candle_amber'); a.r((10,8,11,9),'candle_amber')
        a.dot(11,8,'paper')
        if direction=='east':
            a.l([(11,14),(8,20)],'timber'); a.r((6,20,10,24),'outline');a.r((7,20,9,23),'timber');a.dot(8,21,'candle_amber')
        else:
            a.im=a.im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            a.d=ImageDraw.Draw(a.im)
            # Far-side bag is mostly occluded, rather than reversing its body ownership.
            a.r((15,20,17,24),'outline'); a.r((16,21,16,23),'timber')
    return a.im


def fig(pose=0):
    a=Pixel(24,24)
    # Tail carries the animation, while the seated body remains steady.
    tails=[[(17,20),(20,19),(21,16),(20,13)],[(17,20),(20,19),(21,16),(20,13)],[(17,20),(20,20),(21,18),(20,16)],[(17,20),(20,19),(20,16),(19,14)]]
    a.l(tails[pose],'outline',3);a.l(tails[pose],'slate_violet',1)
    a.p([(8,11),(15,11),(17,15),(18,19),(17,21),(6,21),(5,19),(6,15)],'outline')
    a.p([(8,12),(14,12),(16,15),(16,20),(7,20),(7,15)],'ink')
    a.l([(7,16),(7,19),(9,20)],'aubergine');a.l([(15,15),(16,18)],'slate_violet')
    a.r((8,17,9,21),'outline');a.r((13,17,14,21),'outline');a.dot(8,20,'slate_violet');a.dot(13,20,'slate_violet')
    a.p([(5,3),(9,5),(14,5),(18,3),(18,10),(16,13),(7,13),(5,10)],'outline')
    a.p([(6,5),(9,6),(14,6),(17,5),(17,10),(15,12),(8,12),(6,10)],'ink')
    a.p([(6,4),(8,6),(6,7)],'wine');a.p([(17,4),(15,6),(17,7)],'wine')
    a.l([(7,7),(8,6),(10,6)],'slate_violet');a.l([(16,8),(16,10),(15,11)],'aubergine')
    if pose==1:
        a.l([(7,9),(9,9)],'candle_amber');a.l([(13,9),(15,9)],'candle_amber')
    else:
        a.r((7,8,9,9),'candle_amber');a.r((13,8,15,9),'candle_amber')
        a.dot(8,8,'outline');a.dot(14,8,'outline');a.dot(7,8,'paper');a.dot(13,8,'paper')
    a.dot(11,10,'blush')
    if pose==3: a.r((11,11,12,12),'raspberry')
    else: a.l([(10,11),(11,12),(12,11)],'timber')
    a.l([(4,10),(7,11)],'slate_violet');a.l([(16,11),(19,10)],'slate_violet')
    a.r((9,13,13,13),'wine');a.dot(11,13,'blush')
    a.p([(10,14),(12,14),(13,17),(11,19),(9,17)],'raspberry');a.l([(11,14),(11,17)],'blush')
    return a.im


def fig_portrait(expression=0):
    a=Pixel(64,64)
    a.p([(19,38),(44,38),(50,45),(53,57),(49,61),(13,61),(10,57),(14,46)],'outline')
    a.p([(20,39),(43,39),(48,46),(50,57),(47,59),(16,59),(13,56),(17,46)],'ink')
    a.p([(17,46),(19,43),(21,43),(18,50),(18,58),(15,58),(14,55)],'aubergine')
    a.p([(45,45),(47,47),(48,54),(46,58),(44,58),(45,51)],'slate_violet')
    a.l([(22,49),(22,57),(24,59)],'outline',2);a.l([(39,49),(39,57),(37,59)],'outline',2)
    a.l([(21,58),(26,58)],'aubergine');a.l([(36,58),(40,58)],'aubergine')
    ears = expression !=2
    outer=[(9,6),(20,14),(42,14),(54,6),(53,32),(48,40),(38,45),(24,45),(15,41),(10,34)] if ears else [(5,17),(19,14),(42,14),(58,17),(53,32),(48,40),(38,45),(24,45),(15,41),(10,34)]
    a.p(outer,'outline')
    inner=[(11,10),(21,16),(41,16),(52,10),(51,31),(46,38),(37,42),(25,42),(17,38),(12,32)]
    a.p(inner,'ink')
    if ears:
        a.p([(12,12),(18,17),(13,23)],'wine');a.p([(51,12),(44,17),(50,23)],'wine')
        a.l([(13,14),(15,18)],'blush');a.l([(50,14),(48,18)],'blush')
    a.p([(19,16),(25,14),(38,14),(44,17),(40,17),(36,16),(25,16),(20,19)],'aubergine')
    a.p([(15,25),(17,21),(21,20),(19,23),(18,27)],'slate_violet')
    a.l([(48,25),(49,30),(46,35),(42,38)],'aubergine',2)
    a.p([(18,26),(22,24),(26,25),(27,29),(24,31),(20,31),(17,29)],'candle_amber')
    a.p([(36,25),(40,24),(45,26),(46,29),(43,31),(38,31),(35,29)],'candle_amber')
    if expression==1:
        a.l([(17,25),(26,26)],'outline',2);a.l([(36,26),(45,24)],'outline',2)
        a.r((23,27,24,30),'outline');a.r((42,27,43,30),'outline')
    elif expression==2:
        a.r((22,25,23,30),'outline');a.r((40,25,41,30),'outline')
        a.dot(19,26,'paper');a.dot(37,26,'paper')
    else:
        a.r((22,25,23,30),'outline');a.r((40,25,41,30),'outline')
        a.l([(18,26),(20,25)],'paper');a.l([(36,26),(38,25)],'paper')
    a.p([(29,33),(33,33),(31,35)],'blush');a.l([(31,35),(31,37),(28,39),(26,38)],'timber')
    a.l([(31,37),(34,39),(36,38)],'timber')
    a.l([(8,33),(22,35)],'slate_violet');a.l([(7,37),(21,37)],'aubergine')
    a.l([(42,35),(57,33)],'slate_violet');a.l([(43,37),(58,37)],'aubergine')
    a.p([(24,43),(38,43),(36,47),(26,47)],'wine');a.l([(27,44),(35,44)],'blush')
    a.p([(29,46),(34,46),(37,55),(32,60),(27,55)],'raspberry');a.p([(30,48),(32,48),(33,55),(31,57)],'blush')
    return a.im


def thimble():
    a=Pixel(24,32)
    a.p([(7,13),(16,13),(19,18),(17,24),(19,28),(14,27),(13,30),(10,28),(6,29),(7,25),(5,20)],'slate_violet')
    a.p([(8,14),(15,14),(17,18),(15,24),(17,26),(13,25),(12,28),(10,26),(8,27),(9,23),(7,20)],'spectral_blue')
    a.p([(10,15),(13,15),(13,21),(11,24),(10,24)],'moon_cream')
    a.p([(8,3),(14,3),(17,6),(17,11),(15,14),(9,14),(6,11),(6,7)],'slate_violet')
    a.p([(9,5),(14,5),(15,8),(14,12),(10,12),(8,10)],'moon_cream')
    a.p([(7,6),(9,3),(14,3),(16,5),(15,7),(13,6),(11,5),(9,7),(7,9)],'spectral_blue')
    a.dot(9,4,'moon_cream');a.dot(13,4,'moon_cream')
    a.r((7,8,10,10),'deep_plum');a.r((12,8,15,10),'deep_plum');a.r((8,8,9,9),'moon_cream');a.r((13,8,14,9),'moon_cream');a.dot(11,9,'deep_plum');a.dot(11,12,'slate_violet')
    a.p([(5,17),(11,18),(17,16),(18,23),(12,25),(5,23)],'outline')
    a.p([(6,18),(11,19),(16,17),(17,22),(12,23),(6,22)],'paper');a.l([(11,19),(12,23)],'timber');a.l([(7,20),(9,20)],'timber');a.l([(13,19),(15,18)],'timber')
    a.dot(5,20,'moon_cream');a.dot(18,20,'moon_cream')
    return a.im

def crumb():
    a=Pixel(16,24)
    a.l([(5,20),(3,21),(2,19),(2,17)],'timber')
    a.e((2,3,6,7),'outline');a.e((3,4,5,6),'blush');a.e((8,2,12,6),'outline');a.e((9,3,11,5),'blush')
    a.p([(5,5),(10,4),(12,6),(11,10),(7,11),(4,9)],'outline');a.p([(5,6),(9,5),(11,7),(10,9),(7,10),(5,9)],'timber')
    a.p([(4,8),(7,7),(8,10),(4,10),(3,9)],'paper');a.dot(3,9,'outline');a.dot(8,7,'outline')
    a.p([(5,5),(7,3),(11,4),(12,6),(7,6)],'slate_violet');a.l([(7,4),(10,4)],'moon_cream')
    a.p([(6,10),(10,10),(12,15),(11,19),(5,19),(4,15)],'outline');a.r((6,11,10,17),'slate_violet');a.l([(6,12),(7,11),(9,11)],'moon_cream');a.l([(6,15),(10,15)],'spectral_blue')
    a.r((5,19,7,21),'outline');a.r((9,19,11,21),'outline');a.dot(6,20,'timber');a.dot(10,20,'timber')
    a.l([(13,5),(13,18)],'moon_cream');a.dot(13,4,'paper');a.l([(11,16),(14,16)],'candle_amber');a.dot(12,16,'timber')
    a.p([(3,12),(6,12),(6,17),(4,19),(2,16)],'wine');a.l([(3,13),(5,13)],'candle_amber')
    return a.im

def mabel():
    a=Pixel(24,32)
    a.r((7,27,10,29),'outline');a.r((14,27,17,29),'outline');a.dot(8,28,'timber');a.dot(15,28,'timber')
    a.p([(7,14),(16,14),(18,18),(20,26),(17,28),(6,28),(4,26),(5,19)],'outline')
    a.p([(8,15),(15,15),(17,18),(18,26),(16,27),(7,27),(5,25),(6,19)],'wine')
    a.p([(9,15),(14,15),(14,19),(16,25),(8,25),(9,19)],'paper');a.l([(10,19),(13,19)],'candle_amber');a.r((10,21,13,23),'candle_amber')
    a.p([(6,7),(8,5),(16,5),(18,8),(17,12),(14,15),(10,15),(7,12)],'outline')
    a.p([(8,7),(15,7),(16,9),(15,12),(13,14),(10,13),(8,11)],'candle_amber');a.r((9,8,14,11),'paper')
    a.r((6,8,7,11),'moon_cream');a.r((16,8,17,11),'moon_cream');a.dot(9,10,'outline');a.dot(14,10,'outline');a.dot(9,12,'blush');a.l([(11,13),(13,13)],'timber')
    a.p([(5,6),(8,3),(15,3),(18,6),(19,8),(5,8)],'outline');a.p([(7,6),(9,4),(14,4),(16,6)],'aubergine');a.r((6,7,18,7),'slate_violet');a.dot(15,5,'blush');a.dot(16,6,'raspberry')
    a.r((4,18,7,22),'outline');a.r((5,19,7,21),'candle_amber');a.r((16,18,19,22),'outline');a.r((16,19,18,21),'candle_amber')
    a.r((14,17,18,20),'paper');a.r((18,17,20,19),'paper');a.dot(19,18,'wine');a.l([(14,21),(19,21)],'candle_amber');a.l([(15,15),(16,14)],'moon_cream')
    return a.im

def auditor():
    a=Pixel(24,40)
    a.r((8,32,10,37),'outline');a.r((14,32,16,37),'outline');a.r((7,37,10,38),'outline');a.r((14,37,18,38),'outline');a.l([(8,37),(10,37)],'slate_violet');a.l([(15,37),(17,37)],'slate_violet')
    a.p([(8,14),(15,14),(18,17),(19,32),(16,34),(13,32),(12,34),(7,34),(6,18)],'outline')
    a.p([(9,15),(14,15),(16,18),(17,31),(15,32),(13,30),(11,32),(8,32),(8,18)],'ink')
    a.l([(8,18),(7,29),(8,32)],'slate_violet');a.l([(16,19),(17,29)],'aubergine')
    a.p([(10,15),(14,15),(12,23)],'moon_cream');a.l([(12,16),(12,21)],'wine');a.dot(12,17,'raspberry');a.l([(10,15),(8,19),(10,20)],'slate_violet');a.l([(14,15),(16,19),(14,20)],'slate_violet')
    a.dot(12,25,'candle_amber');a.dot(12,28,'candle_amber')
    a.r((5,18,7,27),'outline');a.r((6,19,6,25),'aubergine');a.r((6,27,7,28),'moon_cream')
    a.r((17,19,19,27),'outline');a.r((18,20,18,25),'slate_violet')
    a.p([(16,24),(21,23),(21,31),(17,32)],'paper');a.l([(18,26),(20,26)],'timber');a.l([(18,28),(20,28)],'timber');a.dot(17,25,'moon_cream')
    a.p([(8,7),(15,7),(16,11),(14,14),(10,14),(8,12)],'outline');a.r((9,8,14,12),'slate_violet');a.r((10,9,14,10),'ink');a.dot(10,10,'moon_cream');a.dot(14,10,'moon_cream');a.l([(11,12),(13,12)],'spectral_blue')
    a.p([(8,2),(15,2),(16,7),(19,7),(19,9),(5,9),(5,7),(7,7)],'outline');a.r((9,3,14,6),'ink');a.l([(9,3),(13,3)],'slate_violet');a.r((8,7,16,7),'wine');a.dot(9,7,'raspberry')
    return a.im


def save(im,name):
    OUT.mkdir(parents=True,exist_ok=True)
    im.save(OUT/name)

def meta(name,cell,columns,rows,frames,anchor,status='REVIEW_REQUIRED',extra=None):
    content={'asset':name+'.png','native_dimensions':[cell[0]*columns,cell[1]*rows], 'mode':'RGBA','alpha':'binary 0 or 255; transparent pixels are (0,0,0,0)', 'cell_px':list(cell),'columns':columns,'rows':rows,'frame_count':len(frames),'frames':frames,'foot_anchor_px':list(anchor),'coordinate_convention':'top-left; x right, y down; anchor is pixel boundary below feet','filter':'nearest','palette':'../palette.json','status':status,'provenance':{'creator':'Codex, original coordinate-authored pixel drawings for this project','source':'../source/draw_characters.py','external_art':'none; no reference pixels sampled','rights':'New original project artwork; no third-party sprite assets used; no blanket public license assigned.'}}
    if extra: content.update(extra)
    (OUT/(name+'.json')).write_text(json.dumps(content,indent=2)+'\n')


def font(size,bold=False):
    return ImageFont.truetype(str(ROOT / 'branding/fonts' / ('DejaVuSans'+('-Bold' if bold else '')+'.ttf')),size)

def label(draw,xy,s,size=16,color='paper',bold=False): draw.text(xy,s,font=font(size,bold),fill=C[color])

def checker(im,box,cell=8):
    d=ImageDraw.Draw(im)
    x,y,w,h=box
    for yy in range(y,y+h,cell):
        for xx in range(x,x+w,cell):
            d.rectangle((xx,yy,min(xx+cell-1,x+w-1),min(yy+cell-1,y+h-1)),fill=C['deep_plum' if ((xx-x)//cell+(yy-y)//cell)%2 else 'aubergine'])

def paste_scale(bg,im,xy,s): bg.alpha_composite(im.resize((im.width*s,im.height*s),Image.Resampling.NEAREST),xy)

def build_reviews(vis,fs,portraits,cast):
    REVIEW.mkdir(exist_ok=True)
    im=Image.new('RGBA',(1320,850),C['ink']); d=ImageDraw.Draw(im)
    label(d,(40,26),'THE HOUSE THAT ATE TOMORROW',26,'paper',True)
    label(d,(40,66),'CHARACTER STUDIES  /  native pixels, original drawings  /  ART REVIEW',15,'blush')
    # Lineup keeps one native pixel density and common floor line.
    for i,(name,asset) in enumerate(cast):
        x=40+i*210; baseline=286; s=4
        d.line((x,baseline,x+176,baseline),fill=C['wine'])
        checker(im,(x,108,176,176),8)
        paste_scale(im,asset,(x+(176-asset.width*s)//2,baseline-asset.height*s-8),s)
        label(d,(x,300),name,18,'paper',True)
        label(d,(x,327),f'{asset.width} × {asset.height} px',14,'moon_cream')
    label(d,(40,378),'VISITOR  /  S · W · E · N  /  idle + four-frame walk',17,'paper',True)
    checker(im,(40,414,480,256),8)
    paste_scale(im,vis,(40,414),2)
    label(d,(40,686),'2× sheet • 20 cells • foot anchor (12, 30)',14,'moon_cream')
    label(d,(570,378),'FIG  /  idle · blink · tail · talk',17,'paper',True)
    checker(im,(570,414,384,96),8);paste_scale(im,fs,(570,414),4)
    label(d,(570,534),'Portrait expressions  /  neutral · denial · concerned',16,'paper',True)
    checker(im,(570,568,576,192),8);paste_scale(im,portraits,(570,568),3)
    label(d,(40,792),'Transparent originals are in sprites/. NPC studies are static concepts; no runtime is implied.',15,'moon_cream')
    im.convert('RGB').save(REVIEW/'CHARACTER_LINEUP.png')
    # Literal 1x/2x/4x atlas samples; labels stay in high-resolution review layer.
    im=Image.new('RGBA',(1180,1030),C['ink']);d=ImageDraw.Draw(im)
    label(d,(32,24),'NATIVE PIXEL / SCALE INSPECTION',24,'paper',True)
    label(d,(32,62),'Same source pixels. Checkerboard is review-only, never baked into sprites.',15,'moon_cream')
    for i,s in enumerate((1,2,4)):
        x=[32,220,550][i];y=130
        label(d,(x,100),f'{s}×',18,'blush',True)
        checker(im,(x,y,vis.width*s,vis.height*s),8);paste_scale(im,vis,(x,y),s)
        y+=vis.height*s+32
        checker(im,(x,y,fs.width*s,fs.height*s),8);paste_scale(im,fs,(x,y),s)
    label(d,(32,800),'Animation review',19,'paper',True)
    label(d,(32,838),'Visitor: each row faces S/W/E/N; columns are idle, contact A, pass A, contact B, pass B.',15,'moon_cream')
    label(d,(32,868),'Fig: body stays seated; eyelids, tail and mouth change in separate review poses.',15,'moon_cream')
    label(d,(32,898),'All native colors come from the 16-token art palette. Alpha is strictly 0 or 255.',15,'moon_cream')
    label(d,(32,948),'Review required: walking feel and visual contrast in a running room remain untested.',15,'blush')
    im.convert('RGB').save(REVIEW/'CHARACTER_PIXEL_SCALES.png')
    gif=[]
    for phase in range(4):
        frame=Image.new('RGBA',(480,240),C['paper']);dd=ImageDraw.Draw(frame)
        label(dd,(20,10),'VISITOR • 6 FPS WALK STUDY',18,'deep_plum',True)
        for i,di in enumerate(('south','west','east','north')):
            paste_scale(frame,visitor(di,phase),(20+i*115,58),4)
            label(dd,(30+i*115,202),di.upper(),13,'deep_plum')
        gif.append(frame.convert('RGB'))
    gif[0].save(REVIEW/'CHARACTER_WALK_PREVIEW.gif',save_all=True,append_images=gif[1:],duration=167,loop=0,disposal=2)


def main():
    vis=Image.new('RGBA',(120,128),CLEAR); frames=[]
    for row,di in enumerate(('south','west','east','north')):
        for col in range(5):
            im=visitor(di,col-1);vis.alpha_composite(im,(col*24,row*32))
            frames.append({'name':di+('_idle' if col==0 else f'_walk_{col-1}'),'cell':[col,row],'rect_px':[col*24,row*32,24,32],'duration_ms':800 if col==0 else 167})
    save(vis,'visitor_sheet.png');meta('visitor_sheet',(24,32),5,4,frames,(12,30),extra={'direction_order':['south','west','east','north'],'column_order':['idle','walk_contact_a','walk_pass_a','walk_contact_b','walk_pass_b'],'loop_walk_columns':[1,2,3,4],'animation_rate_fps':6,'facing_rule':'West/east silhouettes mirror; near/far satchel rendering is authored separately.'})
    fs=Image.new('RGBA',(96,24),CLEAR)
    for col in range(4):fs.alpha_composite(fig(col),(col*24,0))
    save(fs,'fig_sheet.png');meta('fig_sheet',(24,24),4,1,[{'name':n,'cell':[i,0],'rect_px':[i*24,0,24,24],'duration_ms':[1600,120,250,180][i]} for i,n in enumerate(('idle','blink','tail','talk'))],(12,22),extra={'facing':'south only; no unverified directional animation advertised','suggested_idle_sequence':[0,0,2,0,1,0]})
    portraits=Image.new('RGBA',(192,64),CLEAR)
    for col in range(3):portraits.alpha_composite(fig_portrait(col),(col*64,0))
    save(portraits,'fig_portraits.png');meta('fig_portraits',(64,64),3,1,[{'name':n,'cell':[i,0],'rect_px':[i*64,0,64,64]} for i,n in enumerate(('neutral','denial','concerned'))],(32,62),extra={'anchor_role':'portrait bottom center; not a world foot position'})
    cast=[('Visitor',visitor()),('Fig',fig()),('Miss Thimble',thimble()),('Sir Crumb',crumb()),('Mabel',mabel()),('Auditor',auditor())]
    for name,asset in cast:
        stem=name.lower().replace(' ','_')+'_concept';save(asset,stem+'.png')
        meta(stem,asset.size,1,1,[{'name':'neutral_front','cell':[0,0],'rect_px':[0,0,*asset.size]}],(asset.width//2,asset.height-2),status='STATIC_CONCEPT_REVIEW_REQUIRED',extra={'notes':'Single original neutral pose for scale and silhouette review. Not a complete animation/directional set.'})
    build_reviews(vis,fs,portraits,cast)
    allowed={c[:3] for c in C.values()}
    results=[]
    for path in sorted(OUT.glob('*.png')):
        with Image.open(path) as im:
            assert im.mode=='RGBA'
            colors=im.getcolors(im.width*im.height)
            assert all(v[3] in (0,255) for _,v in colors)
            assert all(v[:3] in allowed for _,v in colors if v[3])
            assert any(v[3]==0 for _,v in colors)
            info=json.loads(path.with_suffix('.json').read_text())
            assert list(im.size)==info['native_dimensions']
            for frame in info['frames']:
                x,y,w,h=frame['rect_px'];sub=im.crop((x,y,x+w,y+h));bounds=sub.getbbox()
                assert bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<w and bounds[3]<h,(path,frame,bounds)
            results.append({'path':path.name,'size':list(im.size),'opaque_palette_colors':len([v for _,v in colors if v[3]]),'alpha_values':sorted(set(v[3] for _,v in colors)),'frame_edges_clear':True,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    # Walk states must be genuinely unique in each facing.
    for row in range(4):
        cells=[vis.crop((col*24,row*32,(col+1)*24,(row+1)*32)).tobytes() for col in range(1,5)]
        assert len(set(cells))==4
    (OUT/'validation.json').write_text(json.dumps({'checks':'RGBA; binary alpha; exact palette; native sheet geometry; empty frame borders; four distinct walk states per direction','results':results},indent=2)+'\n')
    print(f'Exported and validated {len(results)} character PNGs; review sheets and animation GIF created.')

if __name__=='__main__':main()
