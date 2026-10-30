#!/usr/bin/env python3
import os
import json
import glob
from collections import deque
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITES_DIR = os.path.join(PROJECT_DIR, 'sprites')
ARTIFACTS_DIR = '/home/tom/.gemini/antigravity-ide/brain/725a9c2e-86b9-467f-a6bb-ea567d402c22'

TARGET_W = 160
TARGET_H = 160
ORIGIN_X = 80
ORIGIN_Y = 145
TARGET_MECH_HEIGHT = 126
MAX_WIDTH = 144

# Master list of 13 canonical chassis with explicit facing standardization.
# Standard: ALL base idle sprites MUST face RIGHT (towards +x).
# In combat / proving ground:
# - Attacker on left (facing = 1) faces RIGHT -> towards Defender
# - Defender on right (facing = -1) is flipped to face LEFT <- towards Attacker
# Centurion was originally drawn facing RIGHT (keep as-is).
# Ballista and others were originally drawn facing LEFT (flip_to_face_right = True).
MECHA_CONFIGS = [
    {
        'id': 'centurion',
        'art_file': 'centurion_mech_art_1793356839164.jpg',
        'is_white': False,
        'bg_thresh': 40,
        'flip_to_face_right': False, # Already faces right with Spartan shield on left
        'front_spr': 'spr_ms_centurion_idle',
        'back_spr': 'spr_ms_centurion_back_idle',
        'flame_color': (255, 140, 40)
    },
    {
        'id': 'ballista',
        'art_file': 'ballista_mech_art_1793356855516.jpg',
        'is_white': True,
        'bg_thresh': 40,
        'flip_to_face_right': True, # Flipped so twin howitzers & cockpit face RIGHT towards enemy!
        'front_spr': 'spr_ms_ballista_idle',
        'back_spr': 'spr_ms_ballista_back_idle',
        'flame_color': (255, 180, 50)
    },
    {
        'id': 'trenchcoat',
        'art_file': 'trenchcoat_mech_art_1793356875899.jpg',
        'is_white': False,
        'bg_thresh': 40,
        'flip_to_face_right': True, # Flipped so slugger autoshotgun aims RIGHT
        'front_spr': 'spr_ms_trenchcoat_idle',
        'back_spr': 'spr_ms_trenchcoat_back_idle',
        'flame_color': (255, 120, 30)
    },
    {
        'id': 'zephyr',
        'art_file': 'zephyr_mech_art_1793356892311.jpg',
        'is_white': True,
        'bg_thresh': 40,
        'flip_to_face_right': True, # Flipped so pulse carbine aims RIGHT
        'front_spr': 'spr_ms_zephyr_idle',
        'back_spr': 'spr_ms_zephyr_back_idle',
        'flame_color': (80, 220, 255)
    },
    {
        'id': 'titan',
        'art_file': 'titan_dreadnought_art_1793356908249.jpg',
        'is_white': False,
        'bg_thresh': 40,
        'flip_to_face_right': True, # Flipped so siege cannon aims RIGHT
        'front_spr': 'spr_ms_titan_proto',
        'back_spr': 'spr_ms_titan_proto_back_idle',
        'flame_color': (255, 160, 40)
    },
    {
        'id': 'gorgon',
        'art_file': 'gorgon_mech_art_1793356925688.jpg',
        'is_white': True,
        'bg_thresh': 40,
        'flip_to_face_right': True, # Flipped so pile-driver spike aims RIGHT
        'front_spr': 'spr_ms_gorgon_idle',
        'back_spr': 'spr_ms_gorgon_back_idle',
        'flame_color': (255, 100, 20)
    },
    {
        'id': 'kage',
        'art_file': 'kage_mech_art_1793356941009.jpg',
        'is_white': True,
        'bg_thresh': 40,
        'flip_to_face_right': True, # Flipped so needle rifle aims RIGHT
        'front_spr': 'spr_ms_kage_idle',
        'back_spr': 'spr_ms_kage_back_idle',
        'flame_color': (0, 255, 230)
    },
    {
        'id': 'bloodhound',
        'art_file': 'bloodhound_mech_art_1793356959893.jpg',
        'is_white': False,
        'bg_thresh': 40,
        'flip_to_face_right': True, # Flipped so snout & quad-missiles face RIGHT
        'front_spr': 'spr_ms_bloodhound_idle',
        'back_spr': 'spr_ms_bloodhound_back_idle',
        'flame_color': (255, 140, 30)
    },
    {
        'id': 'ronin',
        'art_file': 'ronin_mech_art_1793356977950.jpg',
        'is_white': False,
        'bg_thresh': 40,
        'flip_to_face_right': True, # Flipped so pulse cannons aim RIGHT
        'front_spr': 'spr_ms_ronin_idle',
        'back_spr': 'spr_ms_ronin_back_idle',
        'flame_color': (255, 210, 50)
    },
    {
        'id': 'tessen',
        'art_file': 'tessen_mech_art_1793356995169.jpg',
        'is_white': False,
        'bg_thresh': 40,
        'flip_to_face_right': True, # Flipped so war-fans face RIGHT
        'front_spr': 'spr_ms_tessen_idle',
        'back_spr': 'spr_ms_tessen_back_idle',
        'flame_color': (220, 100, 255)
    },
    {
        'id': 'vandal',
        'art_file': 'vandal_mech_art_1793357012481.jpg',
        'is_white': False,
        'bg_thresh': 40,
        'flip_to_face_right': True, # Flipped so flechette autogun aims RIGHT
        'front_spr': 'spr_ms_vandal_idle',
        'back_spr': 'spr_ms_vandal_back_idle',
        'flame_color': (255, 120, 40)
    },
    {
        'id': 'kepler',
        'art_file': 'kepler_mech_art_1793357032252.jpg',
        'is_white': False,
        'bg_thresh': 40,
        'flip_to_face_right': True, # Flipped so long rail-rifle aims RIGHT
        'front_spr': 'spr_ms_kepler_idle',
        'back_spr': 'spr_ms_kepler_back_idle',
        'flame_color': (60, 200, 255)
    },
    {
        'id': 'oberon',
        'art_file': 'oberon_mech_art_1793357050039.jpg',
        'is_white': False,
        'bg_thresh': 40,
        'flip_to_face_right': True, # Flipped so beam lance aims RIGHT
        'front_spr': 'spr_ms_oberon_idle',
        'back_spr': 'spr_ms_oberon_back_idle',
        'flame_color': (100, 240, 255)
    }
]

def extract_alpha_subject(img_path, is_white, bg_thresh=40):
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    pixels = img.load()
    visited = bytearray(w * h)
    queue = deque()
    
    def is_bg(r, g, b):
        if is_white:
            return (r > 255 - bg_thresh and g > 255 - bg_thresh and b > 255 - bg_thresh)
        else:
            return (r < bg_thresh and g < bg_thresh and b < bg_thresh)
            
    for x in range(w):
        if is_bg(*pixels[x, 0]):
            queue.append((x, 0))
            visited[0 * w + x] = 1
        if is_bg(*pixels[x, h - 1]):
            queue.append((x, h - 1))
            visited[(h - 1) * w + x] = 1
            
    for y in range(h):
        if is_bg(*pixels[0, y]) and not visited[y * w + 0]:
            queue.append((0, y))
            visited[y * w + 0] = 1
        if is_bg(*pixels[w - 1, y]) and not visited[y * w + (w - 1)]:
            queue.append((w - 1, y))
            visited[y * w + (w - 1)] = 1
            
    while queue:
        cx, cy = queue.popleft()
        for nx, ny in ((cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)):
            if 0 <= nx < w and 0 <= ny < h:
                idx = ny * w + nx
                if not visited[idx]:
                    if is_bg(*pixels[nx, ny]):
                        visited[idx] = 1
                        queue.append((nx, ny))
                        
    rgba = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    rgba_pixels = rgba.load()
    for y in range(h):
        for x in range(w):
            if not visited[y * w + x]:
                r, g, b = pixels[x, y]
                rgba_pixels[x, y] = (r, g, b, 255)
                
    return rgba

def fit_to_160(rgba_img, flip_lr=False):
    bbox = rgba_img.getbbox()
    if not bbox:
        return Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
        
    cropped = rgba_img.crop(bbox)
    if flip_lr:
        cropped = cropped.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        
    cw, ch = cropped.size
    scale = TARGET_MECH_HEIGHT / ch
    if cw * scale > MAX_WIDTH:
        scale = MAX_WIDTH / cw
        
    nw = max(1, int(cw * scale))
    nh = max(1, int(ch * scale))
    
    resized = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
    
    canvas = Image.new('RGBA', (TARGET_W, TARGET_H), (0, 0, 0, 0))
    # Ground contact shadow
    draw = ImageDraw.Draw(canvas)
    shadow_w = int(nw * 0.75)
    sx0 = ORIGIN_X - shadow_w // 2
    sx1 = ORIGIN_X + shadow_w // 2
    sy0 = ORIGIN_Y - 4
    sy1 = ORIGIN_Y + 7
    draw.ellipse([sx0, sy0, sx1, sy1], fill=(0, 0, 0, 85))
    
    paste_x = ORIGIN_X - nw // 2
    paste_y = ORIGIN_Y - nh
    canvas.paste(resized, (paste_x, paste_y), resized)
    return canvas

def generate_animation_frames(base_img):
    frames = []
    
    # Frame 0: Base
    frames.append(base_img.copy())
    
    # Frame 1: Hydraulic Compression (legs stay grounded, upper torso compresses down 2px)
    f1 = base_img.copy()
    upper = f1.crop((0, 0, TARGET_W, 115))
    f1.paste(Image.new('RGBA', (TARGET_W, 117), (0, 0, 0, 0)), (0, 0))
    f1.paste(upper, (0, 2), upper)
    frames.append(f1)
    
    # Frame 2: Core Reactor Glow / Radiator Venting
    f2 = base_img.copy()
    enhancer = ImageEnhance.Brightness(f2)
    bright = enhancer.enhance(1.15)
    f2 = Image.blend(f2, bright, 0.4)
    frames.append(f2)
    
    # Frame 3: Hydraulic Recovery / Stride Dampening
    f3 = base_img.copy()
    upper3 = f3.crop((0, 0, TARGET_W, 115))
    f3.paste(Image.new('RGBA', (TARGET_W, 115), (0, 0, 0, 0)), (0, 0))
    f3.paste(upper3, (0, -1), upper3)
    frames.append(f3)
    
    return frames

def generate_back_animation_frames(base_front, flame_color):
    # Flip horizontally for rear 3/4 perspective
    back_base = base_front.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    
    # Apply rear tactical shading
    enhancer = ImageEnhance.Color(back_base)
    back_base = enhancer.enhance(0.9)
    enhancer_b = ImageEnhance.Brightness(back_base)
    back_base = enhancer_b.enhance(0.92)
    
    frames = []
    for i in range(4):
        f = back_base.copy()
        
        # Apply vertical hydraulic bob
        y_bob = 2 if i == 1 else (-1 if i == 3 else 0)
        if y_bob != 0:
            upper = f.crop((0, 0, TARGET_W, 115))
            f.paste(Image.new('RGBA', (TARGET_W, 117), (0, 0, 0, 0)), (0, 0))
            f.paste(upper, (0, max(0, y_bob)), upper)
            
        # Draw backpack vernier thruster flares
        draw = ImageDraw.Draw(f)
        flame_len = 8 + (4 if i == 2 else (2 if i == 0 else 0))
        r, g, b = flame_color
        lx, rx = ORIGIN_X - 16, ORIGIN_X + 16
        ny = ORIGIN_Y - 78 + y_bob
        
        # Outer flame cone
        draw.polygon([(lx - 3, ny), (lx + 3, ny), (lx, ny + flame_len)], fill=(r, g, b, 200))
        draw.polygon([(rx - 3, ny), (rx + 3, ny), (rx, ny + flame_len)], fill=(r, g, b, 200))
        # Inner white core
        draw.polygon([(lx - 1, ny), (lx + 1, ny), (lx, ny + flame_len - 3)], fill=(255, 255, 255, 240))
        draw.polygon([(rx - 1, ny), (rx + 1, ny), (rx, ny + flame_len - 3)], fill=(255, 255, 255, 240))
        
        frames.append(f)
        
    return frames

def update_sprite_directory(spr_name, frames):
    spr_dir = os.path.join(SPRITES_DIR, spr_name)
    yy_path = os.path.join(spr_dir, f'{spr_name}.yy')
    
    if not os.path.exists(yy_path):
        print(f'Error: {yy_path} does not exist!')
        return False
        
    with open(yy_path, 'r', encoding='utf-8') as fp:
        yy_data = json.load(fp)
        
    yy_data['width'] = TARGET_W
    yy_data['height'] = TARGET_H
    seq = yy_data.setdefault('sequence', {})
    seq['xorigin'] = ORIGIN_X
    seq['yorigin'] = ORIGIN_Y
    
    frame_objs = yy_data.get('frames', [])
    layers = yy_data.get('layers', [])
    layer_id = layers[0]['name'] if layers else None
    
    for idx, f_obj in enumerate(frame_objs[:4]):
        fid = f_obj['name']
        frame_img = frames[idx]
        
        # 1. Main frame PNG
        frame_img.save(os.path.join(spr_dir, f'{fid}.png'))
        
        # 2. Layer PNG
        if layer_id:
            layer_frame_dir = os.path.join(spr_dir, 'layers', fid)
            os.makedirs(layer_frame_dir, exist_ok=True)
            frame_img.save(os.path.join(layer_frame_dir, f'{layer_id}.png'))
            
    # 3. Composite preview (frame 0)
    frames[0].save(os.path.join(spr_dir, f'{spr_name}.png'))
    
    # 4. Horizontal strip (640x160)
    strip = Image.new('RGBA', (TARGET_W * 4, TARGET_H), (0, 0, 0, 0))
    for i in range(4):
        strip.paste(frames[i], (i * TARGET_W, 0))
    strip.save(os.path.join(spr_dir, f'{spr_name}_strip4.png'))
    
    with open(yy_path, 'w', encoding='utf-8') as fp:
        json.dump(yy_data, fp, indent=2)
        
    return True

print("=== Standardizing All Mobile Suit Sprite Facing & Regenerating Animations ===")

processed_mechs = {}

for cfg in MECHA_CONFIGS:
    m_id = cfg['id']
    art_path = os.path.join(ARTIFACTS_DIR, cfg['art_file'])
    flip_flag = cfg['flip_to_face_right']
    facing_str = "FLIPPED TO FACE RIGHT" if flip_flag else "PRESERVED RIGHT FACING"
    print(f"Processing [{m_id}] ({facing_str})...")
    
    subj_rgba = extract_alpha_subject(art_path, cfg['is_white'], cfg['bg_thresh'])
    base_160 = fit_to_160(subj_rgba, flip_lr=flip_flag)
    processed_mechs[m_id] = base_160
    
    front_frames = generate_animation_frames(base_160)
    update_sprite_directory(cfg['front_spr'], front_frames)
    
    back_frames = generate_back_animation_frames(base_160, cfg['flame_color'])
    update_sprite_directory(cfg['back_spr'], back_frames)

custom_mappings = [
    ('spr_ms_custom_biped_heavy_idle', 'spr_ms_custom_biped_heavy_back_idle', 'centurion', (255, 140, 40)),
    ('spr_ms_custom_hover_sniper_idle', 'spr_ms_custom_hover_sniper_back_idle', 'kepler', (60, 200, 255)),
    ('spr_ms_custom_tread_artillery_idle', 'spr_ms_custom_tread_artillery_back_idle', 'ballista', (255, 180, 50)),
    ('spr_ms_custom_aero_striker_idle', 'spr_ms_custom_aero_striker_back_idle', 'zephyr', (80, 220, 255)),
    ('spr_ms_hephaestus_avatar', 'spr_ms_hephaestus_avatar_back_idle', 'titan', (255, 160, 40)),
]

print("\n=== Updating Custom Modular Chassis & Pre-War Avatar Sprites ===")
for front_spr, back_spr, base_id, flame_col in custom_mappings:
    base = processed_mechs[base_id]
    front_f = generate_animation_frames(base)
    back_f = generate_back_animation_frames(base, flame_col)
    update_sprite_directory(front_spr, front_f)
    update_sprite_directory(back_spr, back_f)

print("\n=== All Sprites Facing Standardized & Multi-Frame Sequences Rebuilt! ===")
