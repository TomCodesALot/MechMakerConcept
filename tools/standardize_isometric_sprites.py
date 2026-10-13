#!/usr/bin/env python3
import os
import glob
import json
from PIL import Image

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITES_DIR = os.path.join(PROJECT_DIR, 'sprites')

TARGET_W = 160
TARGET_H = 160
ORIGIN_X = 80
ORIGIN_Y = 145
TARGET_MECH_HEIGHT = 130

def standardize_sprite(spr_dir):
    spr_name = os.path.basename(spr_dir)
    yy_path = os.path.join(spr_dir, f'{spr_name}.yy')
    if not os.path.exists(yy_path):
        return None

    with open(yy_path, 'r', encoding='utf-8') as f:
        yy_data = json.load(f)

    cur_w = yy_data.get('width', 256)
    cur_h = yy_data.get('height', 256)

    if cur_w == TARGET_W and cur_h == TARGET_H:
        # Already 160x160, check origin
        seq = yy_data.get('sequence', {})
        if seq.get('xorigin') == ORIGIN_X and seq.get('yorigin') == ORIGIN_Y:
            return 'ALREADY_COMPLIANT'
        else:
            seq['xorigin'] = ORIGIN_X
            seq['yorigin'] = ORIGIN_Y
            with open(yy_path, 'w', encoding='utf-8') as f:
                json.dump(yy_data, f, indent=2)
            return 'ORIGIN_FIXED'

    # Gather all frame PNGs in root
    frames_info = yy_data.get('frames', [])
    frame_ids = [f.get('name') for f in frames_info if f.get('name')]
    
    # Also preview png if exists
    preview_png = os.path.join(spr_dir, f'{spr_name}.png')

    # Find sequence global bbox across all frames to keep animation stable
    global_bbox = None
    frame_imgs = {}
    for fid in frame_ids:
        fpath = os.path.join(spr_dir, f'{fid}.png')
        if os.path.exists(fpath):
            img = Image.open(fpath).convert('RGBA')
            frame_imgs[fid] = img
            bb = img.getbbox()
            if bb:
                if global_bbox is None:
                    global_bbox = bb
                else:
                    global_bbox = (
                        min(global_bbox[0], bb[0]),
                        min(global_bbox[1], bb[1]),
                        max(global_bbox[2], bb[2]),
                        max(global_bbox[3], bb[3])
                    )

    if global_bbox is None:
        # Fallback if empty image
        global_bbox = (0, 0, cur_w, cur_h)

    gb_x0, gb_y0, gb_x1, gb_y1 = global_bbox
    gb_w = max(1, gb_x1 - gb_x0)
    gb_h = max(1, gb_y1 - gb_y0)

    # Determine uniform scale factor
    scale = min(1.0, TARGET_MECH_HEIGHT / gb_h)

    # Process and save each frame
    for fid, img in frame_imgs.items():
        # Crop to global bbox for consistent framing
        crop = img.crop(global_bbox)
        nw = max(1, int(crop.width * scale))
        nh = max(1, int(crop.height * scale))
        resized = crop.resize((nw, nh), Image.Resampling.LANCZOS)

        canvas = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
        paste_x = ORIGIN_X - (nw // 2)
        paste_y = ORIGIN_Y - nh
        canvas.paste(resized, (paste_x, paste_y), resized)

        # Save root frame
        out_fpath = os.path.join(spr_dir, f'{fid}.png')
        canvas.save(out_fpath, 'PNG')

        # Also update any copies in layers/
        layer_matches = glob.glob(os.path.join(spr_dir, 'layers', fid, '*.png'))
        for lp in layer_matches:
            canvas.save(lp, 'PNG')

    # Update preview png
    if os.path.exists(preview_png) and frame_ids:
        first_fpath = os.path.join(spr_dir, f'{frame_ids[0]}.png')
        if os.path.exists(first_fpath):
            p_img = Image.open(first_fpath)
            p_img.save(preview_png, 'PNG')

    # Update .yy metadata
    yy_data['width'] = TARGET_W
    yy_data['height'] = TARGET_H
    yy_data['bbox_bottom'] = TARGET_H - 1
    yy_data['bbox_right'] = TARGET_W - 1
    if 'sequence' in yy_data:
        yy_data['sequence']['xorigin'] = ORIGIN_X
        yy_data['sequence']['yorigin'] = ORIGIN_Y

    with open(yy_path, 'w', encoding='utf-8') as f:
        json.dump(yy_data, f, indent=2)

    return 'STANDARDIZED'

def main():
    spr_list = sorted(glob.glob(os.path.join(SPRITES_DIR, 'spr_ms_*')))
    print(f'Standardizing {len(spr_list)} mobile suit combat sprites to 160x160 (origin 80, 145)...')
    std_count = 0
    orig_fixed = 0
    comp_count = 0

    for s_path in spr_list:
        name = os.path.basename(s_path)
        res = standardize_sprite(s_path)
        if res == 'STANDARDIZED':
            std_count += 1
            print(f'  ✓ Standardized: {name} -> 160x160 (origin 80, 145)')
        elif res == 'ORIGIN_FIXED':
            orig_fixed += 1
            print(f'  ✓ Fixed Origin: {name} -> (80, 145)')
        elif res == 'ALREADY_COMPLIANT':
            comp_count += 1
            print(f'  - Compliant: {name}')

    print(f"Summary: {std_count} standardized, {orig_fixed} origin-fixed, {comp_count} already compliant.")

if __name__ == '__main__':
    main()
