#!/usr/bin/env python3
"""Draw the dark-haired Visitor revision using the project's approved 16-color palette.

The original approved 24x32 walk cells remain in art_staging. This revision
retains their body poses and anchors, and adds authored hair and a companion
64x64 portrait sheet. Requires Pillow; no external art is sampled.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib

ROOT = Path(__file__).resolve().parents[1]
P = json.loads((ROOT / 'art_staging/palette.json').read_text())
C = {k: tuple(bytes.fromhex(v[1:])) + (255,) for k, v in P.items()}

def hair(im, direction):
    d = ImageDraw.Draw(im)
    def poly(points, color): d.polygon(points, fill=C[color])
    def line(points, color, width=1): d.line(points, fill=C[color], width=width)
    def rect(box, color): d.rectangle(box, fill=C[color])
    if direction == 'south':
        # Flowing side locks frame the face and fall onto her shoulders.
        poly([(6,5),(8,4),(9,8),(8,13),(9,16),(7,18),(5,16),(6,12)], 'outline')
        poly([(7,6),(8,6),(8,12),(8,15),(7,16),(6,15),(7,12)], 'deep_plum')
        poly([(15,5),(17,5),(18,9),(17,12),(18,16),(16,18),(15,15),(15,11)], 'outline')
        poly([(15,6),(16,6),(17,9),(16,12),(17,15),(16,16),(15,14)], 'deep_plum')
        poly([(7,4),(9,2),(14,2),(17,5),(16,7),(14,7),(12,5),(10,7),(8,7),(7,8),(6,7)], 'ink')
        line([(8,4),(10,3),(13,3),(15,4)], 'slate_violet')
        rect((15,5,16,5),'blush'); rect((16,6,16,6),'candle_amber')
        line([(6,10),(6,14)],'aubergine'); line([(17,11),(17,14)],'aubergine')
        # Restore a clear, expressive face after layering the long front locks.
        rect((9,7,14,10),'paper')
        rect((10,8,10,9),'outline'); rect((13,8,13,9),'outline')
        rect((9,10,9,10),'blush'); rect((14,10,14,10),'blush')
        rect((12,11,12,11),'timber')
    elif direction == 'north':
        poly([(6,6),(8,3),(14,3),(17,5),(18,10),(18,17),(16,20),(13,18),(11,20),(8,18),(6,19),(5,16),(6,11)], 'outline')
        poly([(7,5),(9,3),(14,3),(16,5),(17,9),(17,16),(16,18),(13,17),(11,18),(9,17),(7,18),(6,16),(7,11)], 'ink')
        poly([(9,4),(12,3),(15,4),(16,6),(15,7),(13,5),(11,5),(9,7),(8,7)], 'deep_plum')
        line([(8,6),(8,12),(9,15),(9,16)],'slate_violet')
        line([(14,6),(15,9),(15,14),(14,16)],'aubergine')
        line([(10,12),(10,16),(11,17)],'aubergine')
        rect((15,6,16,6),'blush'); rect((15,7,15,7),'candle_amber')
    else:
        # Both profiles share the same long lock; mirror the authored silhouette.
        mirrored = direction == 'west'
        if mirrored:
            im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            d = ImageDraw.Draw(im)
        poly([(6,6),(8,3),(12,3),(14,5),(12,7),(11,10),(11,13),(12,16),(10,18),(7,17),(5,15),(6,11)], 'outline')
        poly([(7,6),(8,4),(11,4),(13,5),(11,6),(10,9),(10,13),(11,15),(10,16),(8,16),(6,15),(7,11)], 'ink')
        line([(8,5),(10,4),(12,4)],'slate_violet')
        line([(7,9),(7,13),(8,15)],'aubergine')
        rect((8,6,9,6),'blush'); rect((9,7,9,7),'candle_amber')
        if mirrored:
            im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    return im


def portrait(expression):
    im = Image.new('RGBA',(64,64),(0,0,0,0)); d = ImageDraw.Draw(im)
    def poly(points, color): d.polygon(points, fill=C[color])
    def line(points, color, width=1): d.line(points, fill=C[color], width=width)
    def rect(box, color): d.rectangle(box, fill=C[color])
    # Silhouette and long dark waves, on a transparent background.
    poly([(16,15),(20,7),(27,4),(38,4),(46,9),(49,17),(49,32),(53,43),(49,51),(43,53),(21,53),(14,48),(11,42),(14,31),(13,22)],'outline')
    poly([(17,15),(21,9),(27,6),(38,6),(44,10),(47,17),(47,32),(51,42),(47,49),(43,51),(21,51),(16,47),(13,42),(16,31),(15,22)],'ink')
    poly([(16,36),(22,35),(25,43),(24,51),(18,50),(14,45)],'deep_plum')
    poly([(43,34),(48,35),(51,42),(47,49),(42,51),(40,44)],'deep_plum')
    # Coat, scarf and a neat collar echo the world sprite.
    poly([(23,43),(41,43),(49,49),(53,60),(51,62),(13,62),(11,60),(15,49)],'outline')
    poly([(23,44),(40,44),(47,49),(51,59),(49,60),(15,60),(13,59),(17,49)],'aubergine')
    poly([(18,49),(24,45),(29,51),(26,60),(17,60),(15,57)],'wine')
    poly([(42,46),(47,49),(50,58),(47,60),(37,60),(36,51)],'deep_plum')
    poly([(26,36),(38,36),(39,45),(35,49),(28,49),(25,45)],'outline')
    rect((28,37,36,45),'candle_amber')
    poly([(25,43),(29,45),(35,45),(39,42),(41,46),(36,50),(27,50),(23,46)],'wine')
    line([(26,44),(30,46),(35,46),(38,44)],'blush')
    poly([(29,48),(34,48),(34,56),(31,59),(29,56)],'raspberry')
    line([(30,49),(30,54)],'blush')
    # Face: soft features, warm highlights, readable at portrait scale.
    poly([(20,18),(23,13),(30,11),(39,13),(44,18),(43,30),(40,37),(36,41),(28,41),(23,37),(20,30)],'outline')
    poly([(21,18),(24,14),(30,12),(39,14),(43,18),(42,29),(39,36),(36,39),(28,39),(24,36),(21,29)],'candle_amber')
    poly([(23,18),(25,15),(31,14),(38,15),(41,19),(40,28),(38,34),(35,37),(29,37),(25,34),(23,28)],'paper')
    # Dark fringe and soft side locks sit above the face.
    poly([(17,19),(19,12),(25,7),(36,6),(43,9),(47,15),(46,22),(43,23),(41,18),(39,16),(36,16),(33,14),(29,18),(25,19),(23,23),(20,26),(18,24)],'ink')
    poly([(19,16),(22,11),(27,8),(36,8),(41,10),(44,13),(45,17),(41,16),(37,13),(33,12),(28,16),(24,17),(21,21),(19,21)],'deep_plum')
    line([(22,13),(26,10),(31,9),(36,9)],'slate_violet')
    line([(18,23),(19,29),(18,35),(16,40)],'aubergine')
    line([(45,23),(45,31),(48,38),(47,44)],'slate_violet')
    # Little hair clip, pink and gold.
    poly([(42,13),(44,11),(46,13),(44,15)],'blush'); rect((43,13,44,14),'candle_amber')
    if expression == 1:
        line([(25,25),(28,24),(30,25)],'outline'); line([(35,25),(38,24),(40,25)],'outline')
    else:
        rect((26,24,28,27),'outline'); rect((36,24,38,27),'outline')
        rect((26,24,26,24),'moon_cream'); rect((36,24,36,24),'moon_cream')
    line([(24,22),(28,21),(30,22)],'timber'); line([(35,22),(38,21),(40,22)],'timber')
    rect((24,30,26,31),'blush'); rect((38,30,40,31),'blush')
    rect((32,29,32,30),'candle_amber')
    if expression == 2:
        line([(30,34),(33,33),(35,34)],'timber')
    else:
        line([(30,33),(32,34),(34,33)],'timber')
    return im


def main():
    source = Image.open(ROOT/'art_staging/sprites/visitor_sheet.png').convert('RGBA')
    out = Image.new('RGBA',source.size,(0,0,0,0))
    for row, direction in enumerate(('south','west','east','north')):
        for column in range(5):
            box = (column*24,row*32,(column+1)*24,(row+1)*32)
            out.alpha_composite(hair(source.crop(box), direction), (column*24,row*32))
    sheet = Image.new('RGBA',(192,64),(0,0,0,0))
    for i in range(3): sheet.alpha_composite(portrait(i), (i*64,0))
    allowed=set(C.values())|{(0,0,0,0)}
    for im in (out,sheet):
        assert set(im.getdata()).issubset(allowed)
        assert set(im.getchannel('A').getdata()).issubset({0,255})
    for row in range(4):
        frames=[]
        for col in range(5):
            frame=out.crop((col*24,row*32,(col+1)*24,(row+1)*32))
            bounds=frame.getbbox()
            assert bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<24 and bounds[3]<32
            if col: frames.append(frame.tobytes())
        assert len(set(frames))==4
    out.save(ROOT/'assets/visitor_sheet.png')
    sheet.save(ROOT/'assets/visitor_portraits.png')
    for name in ('visitor_sheet.png','visitor_portraits.png'):
        data=(ROOT/'assets'/name).read_bytes()
        print(name, hashlib.sha256(data).hexdigest())

if __name__=='__main__': main()
