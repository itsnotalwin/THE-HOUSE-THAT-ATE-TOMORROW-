"""Read and validate exported artwork without rewriting source assets.

Checks image integrity, native palette/alpha, sprite geometry, atlas indices,
room reconstruction, exact branding text, and manifest provenance/hashes.
This is an art-package validator, not a gameplay test suite.
"""
from pathlib import Path
import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'review/ART_VALIDATION.json'
PALETTE = {tuple(bytes.fromhex(v[1:])) for v in json.loads((ROOT/'palette.json').read_text()).values()}
checks = []


def check(condition, message):
    if not condition:
        raise ValueError(message)


def image_integrity():
    count = 0
    for path in sorted(ROOT.rglob('*')):
        if path.suffix.lower() not in {'.png', '.gif'}:
            continue
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            im.load()
        count += 1
    checks.append({'check':'image_decode','passed':True,'files':count})


def native_assets():
    results=[]
    for folder in ['sprites','tiles','props','ui']:
        for path in sorted((ROOT/folder).glob('*.png')):
            with Image.open(path) as im:
                check(im.mode=='RGBA', f'{path}: not RGBA')
                colors=im.getcolors(im.width*im.height)
                alpha={color[3] for _,color in colors}
                check(alpha<={0,255}, f'{path}: interpolated alpha')
                check({color[:3] for _,color in colors if color[3]} <= PALETTE, f'{path}: outside palette')
                check(0 in alpha and 255 in alpha, f'{path}: missing transparency or visible art')
                results.append({'path':path.relative_to(ROOT).as_posix(),'size':list(im.size),'palette_colors':sum(color[3]>0 for _,color in colors),'binary_alpha':True})
    checks.append({'check':'native_rgba_palette_alpha','passed':True,'files':results})


def character_geometry():
    total=0
    for path in sorted((ROOT/'sprites').glob('*.png')):
        meta=json.loads(path.with_suffix('.json').read_text())
        im=Image.open(path)
        check(list(im.size)==meta['native_dimensions'], f'{path}: dimension mismatch')
        cw,ch=meta['cell_px']
        check((cw*meta['columns'],ch*meta['rows'])==im.size, f'{path}: cell layout mismatch')
        check(meta['frame_count']==len(meta['frames'])==meta['columns']*meta['rows'], f'{path}: frame count')
        for frame in meta['frames']:
            x,y,w,h=frame['rect_px']
            check(x>=0 and y>=0 and x+w<=im.width and y+h<=im.height, f'{path}: frame outside sheet')
            bbox=im.crop((x,y,x+w,y+h)).getbbox()
            check(bbox and bbox[0]>0 and bbox[1]>0 and bbox[2]<w and bbox[3]<h, f'{path}: frame border occupied')
            total+=1
    im=Image.open(ROOT/'sprites/visitor_sheet.png')
    for row in range(4):
        frames=[im.crop((col*24,row*32,(col+1)*24,(row+1)*32)).tobytes() for col in range(1,5)]
        check(len(set(frames))==4, f'Visitor row{row}: duplicate walk pose')
    checks.append({'check':'character_cell_bounds_and_walk_uniqueness','passed':True,'frames_checked':total,'visitor_walk_frames':16})


def environment_geometry():
    meta=json.loads((ROOT/'tiles/foyer_atlas.json').read_text())
    check(meta['tile_size']==[16,16], 'Unexpected tile grid')
    indices=[]
    for name,obj in meta['objects'].items():
        x,y,w,h=obj['atlas_rect_px']
        check(all(v%16==0 for v in [x,y,w,h]), f'{name}: off-grid atlas rect')
        check(x>=0 and y>=0 and x+w<=256 and y+h<=256, f'{name}: atlas bounds')
        expected=[(yy//16)*16+(xx//16) for yy in range(y,y+h,16) for xx in range(x,x+w,16)]
        check(expected==obj['tile_indices'], f'{name}: wrong cell indices')
        indices.extend(expected)
    check(len(indices)==len(set(indices)), 'Atlas objects overlap')
    for candidate in ['A','B']:
        layout=json.loads((ROOT/f'concept/HALL_{candidate}_layout.json').read_text())
        for mode in ['here','almost']:
            atlas=Image.open(ROOT/'tiles'/meta[mode]).convert('RGBA')
            rebuilt=Image.new('RGBA',tuple(layout['native_dimensions']),'#11101C')
            for placement in layout['placements']:
                if placement['mode'] not in ['both',mode]:
                    continue
                x,y,w,h=meta['objects'][placement['asset']]['atlas_rect_px']
                rebuilt.alpha_composite(atlas.crop((x,y,x+w,y+h)),tuple(placement['position_px']))
            exported=Image.open(ROOT/f'concept/HALL_{candidate}_{mode.upper()}.png').convert('RGBA')
            check(rebuilt.tobytes()==exported.tobytes(), f'Hall{candidate}/{mode}: not reconstructible')
            x,y,w,h=layout['camera_crop_px']
            view=Image.open(ROOT/f'concept/HALL_{candidate}_{mode.upper()}_VIEWPORT.png').convert('RGBA')
            check(exported.crop((x,y,x+w,y+h)).tobytes()==view.tobytes(), f'Hall{candidate}/{mode}: crop mismatch')
        reveals=[p['asset'] for p in layout['placements'] if p['mode']!='both']
        check(reveals==['ghost_reader'], f'Hall{candidate}: unexpected mode-only geometry')
    checks.append({'check':'atlas_indices_and_room_reconstruction','passed':True,'objects':len(meta['objects']),'indexed_cells':len(indices),'rooms':4,'camera_crops':4,'mode_geometry':'one shared placement list per candidate; only spectral reader is mode-specific'})


def branding_content():
    namespace={'svg':'http://www.w3.org/2000/svg'}
    expectations={'title_wordmark':'The House That Ate Tomorrow','title_tagline_lockup':'Tomorrow is missing. The cat denies everything.'}
    for stem,expected in expectations.items():
        tree=ET.parse(ROOT/f'branding/{stem}.svg')
        actual=' '.join(node.text or '' for node in tree.findall('.//svg:text',namespace))
        check(actual==expected, f'{stem}: wording differs: {actual}')
        portable=ET.parse(ROOT/f'branding/{stem}_outlined.svg')
        check(not portable.findall('.//svg:text',namespace), f'{stem}: outlined source depends on text')
        im=Image.open(ROOT/f'branding/{stem}.png')
        check(im.mode=='RGBA' and im.getextrema()[3][0]==0, f'{stem}: transparency')
    checks.append({'check':'exact_title_tagline_and_portable_outlines','passed':True})


def package_manifest():
    with (ROOT/'manifest.csv').open(newline='') as f:
        rows=list(csv.DictReader(f))
    names=[row['path'] for row in rows]
    check(len(names)==len(set(names)), 'Manifest duplicate paths')
    for row in rows:
        path=ROOT/row['path']
        check(path.is_file(), f'Missing manifest asset:{path}')
        check(hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'], f'Stale manifest checksum:{path}')
        check((ROOT/row['source']).is_file(), f'Missing art source:{row["source"]}')
    expected={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.suffix.lower() in {'.png','.svg','.gif','.ttf'}}
    check(set(names)==expected,'Manifest coverage differs from visual/font files')
    checks.append({'check':'manifest_paths_sources_hashes','passed':True,'rows':len(rows)})


def original_handoff():
    repo=ROOT.parent
    n=0
    for line in (repo/'PACKAGE_FILES_SHA256.txt').read_text().splitlines():
        if not line.strip():
            continue
        expected,name=line.split('  ',1)
        check(hashlib.sha256((repo/name).read_bytes()).hexdigest()==expected, f'Supplied handoff changed:{name}')
        n+=1
    checks.append({'check':'original_handoff_unchanged','passed':True,'checksums':n})


def main():
    errors=[]
    for fn in [image_integrity,native_assets,character_geometry,environment_geometry,branding_content,package_manifest,original_handoff]:
        try:
            fn()
        except Exception as exc:
            errors.append({'check':fn.__name__,'error':str(exc)})
    report={'status':'PASS' if not errors else 'FAIL','checks':checks,'errors':errors,
            'not_established':['human art approval','runtime import or gameplay','controller/browser usability','final art quality','commercial name clearance'],
            'source':'../source/validate_art.py'}
    REPORT.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'check_groups':len(checks),'errors':errors},indent=2))
    if errors:
        raise SystemExit(1)


if __name__=='__main__':
    main()
