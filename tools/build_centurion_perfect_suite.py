#!/usr/bin/env python3
"""
Complete Production Suite for TH-C02 Centurion (ms_terran_centurion_02)
Standard Allied Attacker: Facing FRONT-RIGHT by default.
Zero double guns. Zero occluded muzzle flashes.
Rotating Barrel 35mm Chain Vulcan with smooth spin-down.
Bespoke Spartan Shield Slam & High-Frequency Thermal Gladius.
"""
import os
import sys
import math
import json
import uuid
from PIL import Image, ImageOps, ImageDraw

def clamp(v, low, high):
    return max(low, min(high, v))

# =========================================================================
# 1. LOAD MASTER CENTURION BASE SPRITE & CLEAN SHIELD
# =========================================================================
raw_base = Image.open("/tmp/git_centurion/f0.png").convert("RGBA")
m = ImageOps.mirror(raw_base)
pix = m.load()

# Clean Spartan tower shield: replace decals/reversed text with clean olive armor
for y in range(55, 95):
    for x in range(112, 136):
        r, g, b, a = pix[x, y]
        if a > 0 and r > 125 and g > 125 and b > 105:
            y_prog = (y - 55) / 40.0
            col = (int(102 - 12 * y_prog), int(98 - 14 * y_prog), int(72 - 12 * y_prog), 255)
            pix[x, y] = col

# Clean shoulder decal
for y in range(44, 54):
    for x in range(50, 58):
        p = pix[x, y]
        if p[3] > 100 and p[0] > 125:
            pix[x, y] = (92, 102, 75, 255)

master_clean = m.copy()

# =========================================================================
# 2. DISSECT BODY COMPONENTS (Shield, Clean Right Leg, Body-No-Gun)
# =========================================================================
# A. Extract Shield Layer
shield_layer = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
s_pix = shield_layer.load()
for y in range(25, 130):
    for x in range(95, 138):
        s_pix[x, y] = pix[x, y]

# B. Erase lowered gun from body
gun_mask = Image.new("L", (160, 160), 0)
dmask = ImageDraw.Draw(gun_mask)
dmask.polygon([(19, 52), (32, 52), (34, 64), (19, 64)], fill=255) # top counterweight
dmask.polygon([(19, 65), (38, 65), (40, 92), (19, 92)], fill=255) # drum magazine
dmask.polygon([(36, 70), (54, 70), (54, 86), (36, 86)], fill=255) # receiver & feed
dmask.polygon([(46, 82), (58, 80), (76, 110), (62, 118)], fill=255) # barrel cluster
dmask.ellipse([58, 104, 76, 118], fill=255) # barrel muzzle

body_clean = master_clean.copy()
bpix = body_clean.load()
for y in range(160):
    for x in range(160):
        if gun_mask.getpixel((x, y)) > 128:
            bpix[x, y] = (0, 0, 0, 0)

# C. Seamlessly paint the authentic right leg connecting hip to foot
for y in range(68, 96):
    prog = (y - 68) / 28.0
    lx = int(48 - 4 * prog)
    rx = int(60 - 2 * prog)
    for x in range(lx, rx + 1):
        if x == lx:
            bpix[x, y] = (220, 225, 230, 255) # white highlight rim
        elif x == rx:
            bpix[x, y] = (40, 45, 35, 255) # shadow border
        elif x == lx + 1:
            bpix[x, y] = (135, 145, 110, 255)
        elif x > rx - 3:
            bpix[x, y] = (65, 72, 52, 255)
        else:
            bpix[x, y] = (95, 105, 78, 255)

d_body = ImageDraw.Draw(body_clean)
d_body.ellipse([46, 94, 56, 104], fill=(42, 46, 50, 255), outline=(220, 225, 230, 255))
d_body.ellipse([49, 97, 53, 101], fill=(70, 75, 82, 255))

for y in range(104, 124):
    prog = (y - 104) / 20.0
    lx = int(45 + 2 * prog)
    rx = int(58 + 2 * prog)
    for x in range(lx, rx + 1):
        if x == lx:
            bpix[x, y] = (220, 225, 230, 255)
        elif x == rx:
            bpix[x, y] = (40, 45, 35, 255)
        elif x == lx + 1:
            bpix[x, y] = (135, 145, 110, 255)
        elif x > rx - 3:
            bpix[x, y] = (65, 72, 52, 255)
        else:
            bpix[x, y] = (92, 102, 75, 255)

for cy in [108, 114, 120]:
    d_body.line([48, cy, 54, cy + 2], fill=(225, 120, 20, 255), width=1)
    d_body.line([49, cy + 1, 55, cy + 3], fill=(30, 32, 35, 255), width=1)

d_body.line([44, 98, 44, 118], fill=(210, 215, 220, 255), width=1)

for y in range(45, 76):
    for x in range(95, 112):
        col = (92, 102, 75, 255) if x < 105 else (60, 68, 50, 255)
        bpix[x, y] = col

# =========================================================================
# 3. BUILD spr_ms_centurion_idle (4 FRAMES)
# =========================================================================
idle_frames = []
for i in range(4):
    fr = master_clean.copy()
    if i == 1 or i == 2:
        fr_dip = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        shadow_crop = master_clean.crop((0, 140, 160, 160))
        fr_dip.paste(shadow_crop, (0, 140), shadow_crop)
        mech_upper = master_clean.crop((0, 0, 160, 145))
        fr_dip.paste(mech_upper, (0, 1), mech_upper)
        idle_frames.append(fr_dip)
    else:
        idle_frames.append(fr)

# =========================================================================
# 4. BUILD spr_ms_centurion_fire_chaingun (7 FRAMES)
# ROTATING BARRELS & SMOOTH SPIN-DOWN (ZERO ABRUPT EXPLOSIONS!)
# =========================================================================
def draw_rotary_chain_vulcan(draw, rx, ry, rot_angle_deg=0, recoil_x=0):
    ox = rx + recoil_x
    oy = ry
    
    # 1. Stock
    draw.polygon([(ox - 14, oy - 2), (ox, oy - 4), (ox, oy + 8), (ox - 10, oy + 10)],
                 fill=(40, 44, 50, 255), outline=(22, 25, 28, 255))
    draw.line([ox - 12, oy, ox - 2, oy - 2], fill=(85, 95, 105, 255))
    
    # 2. Main Receiver Box
    draw.rectangle([ox, oy - 6, ox + 22, oy + 8], fill=(52, 58, 66, 255), outline=(28, 32, 36, 255))
    draw.line([ox + 2, oy - 5, ox + 20, oy - 5], fill=(130, 140, 155, 255))
    
    # Drum Magazine (heavy 35mm chain feed)
    draw.ellipse([ox + 4, oy + 5, ox + 18, oy + 17], fill=(42, 46, 52, 255), outline=(25, 28, 32, 255))
    draw.line([ox + 6, oy + 11, ox + 16, oy + 11], fill=(85, 92, 102, 255))
    
    # Receiver Armor Plate
    draw.rectangle([ox + 2, oy + 1, ox + 8, oy + 7], fill=(92, 102, 75, 255), outline=(42, 48, 36, 255))
    
    # Targeting Scope
    draw.rectangle([ox + 8, oy - 9, ox + 18, oy - 6], fill=(30, 32, 36, 255), outline=(20, 22, 25, 255))
    draw.point((ox + 17, oy - 8), fill=(0, 240, 255, 255))
    draw.point((ox + 17, oy - 7), fill=(0, 240, 255, 255))
    
    # 3. Rotary Motor Housing
    draw.rectangle([ox + 22, oy - 6, ox + 32, oy + 7], fill=(44, 48, 55, 255), outline=(26, 28, 32, 255))
    for vx in [ox + 24, ox + 27, ox + 30]:
        draw.line([vx, oy - 4, vx, oy + 5], fill=(22, 24, 28, 255))
        
    # 4. ROTATING BARRELS (4 heavy fluted rotary barrels around cylinder axis)
    cy = oy + 1
    r_hub = 5.0
    num_barrels = 4
    
    barrel_info = []
    for b_i in range(num_barrels):
        ang_deg = rot_angle_deg + b_i * (360.0 / num_barrels)
        rad = math.radians(ang_deg)
        by = cy + r_hub * math.sin(rad)
        depth = math.cos(rad)
        barrel_info.append((depth, b_i, by, ang_deg))
    barrel_info.sort(key=lambda item: item[0])
    
    draw.line([ox + 32, cy, ox + 60, cy], fill=(35, 38, 44, 255), width=3)
    
    active_bore_pos = None
    all_muzzle_pos = []
    
    for depth, b_i, by_f, ang_deg in barrel_info:
        by_int = int(round(by_f))
        all_muzzle_pos.append((ox + 60, by_int))
        
        if depth > 0.4:
            col_body = (75, 84, 96, 255)
            col_rim = (175, 188, 205, 255)
            col_dark = (36, 40, 46, 255)
        elif depth > -0.2:
            col_body = (60, 68, 78, 255)
            col_rim = (130, 140, 155, 255)
            col_dark = (30, 34, 40, 255)
        else:
            col_body = (45, 50, 58, 255)
            col_rim = (85, 95, 105, 255)
            col_dark = (24, 26, 30, 255)
            
        draw.line([ox + 32, by_int, ox + 60, by_int], fill=col_body, width=2)
        draw.line([ox + 32, by_int - 1, ox + 60, by_int - 1], fill=col_rim, width=1)
        draw.point((ox + 60, by_int), fill=col_dark)
        
        if active_bore_pos is None or (depth > 0 and by_int < active_bore_pos[1]):
            active_bore_pos = (ox + 61, by_int)
            
    # 5. Rotor Alignment Clamp Rings
    for cx in [ox + 44, ox + 59]:
        draw.line([cx, cy - 6, cx, cy + 7], fill=(32, 36, 42, 255), width=2)
        notch_y = int(round(cy + 6.0 * math.sin(math.radians(rot_angle_deg))))
        draw.point((cx, notch_y), fill=(220, 230, 245, 255))
        
    ejection_port = (ox + 15, oy - 6)
    return active_bore_pos, ejection_port, all_muzzle_pos

def make_rotary_fire_frame(rot_deg=0, recoil_x=0, mode="lock", casing_count=0):
    f = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    f.paste(body_clean, (recoil_x, 0), body_clean)
    
    shield_braced = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    shield_braced.paste(shield_layer, (0, 12), shield_layer)
    f.paste(shield_braced, (recoil_x, 0), shield_braced)
    
    d = ImageDraw.Draw(f)
    for y in range(48, 60):
        for x in range(42 + recoil_x, 68 + recoil_x):
            col = (220, 225, 230, 255) if y == 48 else ((40, 45, 35, 255) if y == 59 else (95, 105, 78, 255))
            d.point((x, y), fill=col)
    d.ellipse([52 + recoil_x, 52, 62 + recoil_x, 62], fill=(42, 46, 50, 255), outline=(220, 225, 230, 255))
    
    active_bore, ej_port, all_muzzles = draw_rotary_chain_vulcan(d, rx=64, ry=54, rot_angle_deg=rot_deg, recoil_x=recoil_x)
    mx, my = active_bore[0], active_bore[1]
    
    if mode == "lock":
        # Frame 0: Spin-up lock (targeting diode beam, zero fire)
        d.line([mx, my, mx + 26, my], fill=(0, 240, 255, 220), width=1)
        d.point((mx + 27, my), fill=(255, 255, 255, 255))
        
    elif mode == "fire":
        # Focused forward muzzle star & supersonic tungsten tracer
        d.polygon([(mx, my - 2), (mx + 26, my), (mx, my + 2)], fill=(255, 255, 240, 255))
        d.polygon([(mx + 1, my - 6), (mx + 20, my), (mx + 1, my + 6)], fill=(255, 210, 60, 220))
        d.line([mx, my, mx + 32, my], fill=(255, 255, 255, 255), width=2)
        d.line([mx + 1, my - 10, mx + 14, my], fill=(255, 140, 30, 200), width=1)
        d.line([mx + 1, my + 10, mx + 14, my], fill=(255, 140, 30, 200), width=1)
        for sp in [(mx + 28, my - 3), (mx + 34, my + 2), (mx + 38, my)]:
            d.point(sp, fill=(255, 240, 120, 255))
            
        bx, by = ej_port[0], ej_port[1] - 2
        d.rectangle([bx, by, bx + 5, by + 4], fill=(255, 215, 60, 255), outline=(180, 130, 20, 255))
        d.line([bx + 1, by + 1, bx + 4, by + 3], fill=(255, 255, 200, 255))
        if casing_count > 1:
            d.rectangle([bx - 6, by - 5, bx - 2, by - 2], fill=(240, 195, 50, 230), outline=(160, 110, 15, 255))
        if casing_count > 2:
            d.rectangle([bx - 12, by - 3, bx - 8, by], fill=(220, 175, 40, 200), outline=(140, 95, 10, 255))
        d.ellipse([mx + 12, my - 6, mx + 18, my - 2], fill=(215, 220, 225, 120))
        
    elif mode == "spindown_1":
        # Frame 5: Spin-down 1 - NO EXPLOSION! Glowing cherry-red muzzles & forward smoke
        for bx_m, by_m in all_muzzles:
            d.point((bx_m, by_m), fill=(255, 120, 20, 255))
            d.point((bx_m - 1, by_m), fill=(200, 60, 10, 255))
        for sx, sy in [(mx + 4, my - 3), (mx + 12, my - 5), (mx + 20, my - 7),
                       (mx + 6, my + 3), (mx + 14, my + 5)]:
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(205, 210, 215, 120))
            
    elif mode == "spindown_2":
        # Frame 6: Spin-down 2 - NO EXPLOSION! Residual heat dissipating & smoke dissipation
        for bx_m, by_m in all_muzzles:
            d.point((bx_m, by_m), fill=(160, 50, 15, 255))
        for sx, sy in [(mx + 10, my - 4), (mx + 18, my - 5), (mx + 26, my - 6),
                       (mx + 14, my + 3), (mx + 22, my + 4)]:
            d.ellipse([sx - 3, sy - 2, sx + 3, sy + 2], fill=(195, 200, 205, 80))
            
    return f

# 7-frame rotating chain vulcan sequence
fire_frames = [
    make_rotary_fire_frame(rot_deg=0,   recoil_x=0,  mode="lock",        casing_count=0),
    make_rotary_fire_frame(rot_deg=45,  recoil_x=-3, mode="fire",        casing_count=1),
    make_rotary_fire_frame(rot_deg=90,  recoil_x=-2, mode="fire",        casing_count=2),
    make_rotary_fire_frame(rot_deg=135, recoil_x=-3, mode="fire",        casing_count=3),
    make_rotary_fire_frame(rot_deg=180, recoil_x=-2, mode="fire",        casing_count=3),
    make_rotary_fire_frame(rot_deg=225, recoil_x=-1, mode="spindown_1",  casing_count=0),
    make_rotary_fire_frame(rot_deg=270, recoil_x=0,  mode="spindown_2",  casing_count=0)
]

# =========================================================================
# 5. BUILD spr_ms_centurion_attack_melee (7 FRAMES)
# SPARTAN TOWER SHIELD SLAM -> HIGH-FREQUENCY THERMAL GLADIUS THRUST!
# =========================================================================
def draw_gladius_clean(draw, hx, hy, angle_deg, blade_len=36, thermal=True):
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    perp = rad + math.pi / 2
    cos_p = math.cos(perp)
    sin_p = math.sin(perp)
    
    bx = hx - int(cos_a * 8)
    by = hy - int(sin_a * 8)
    draw.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(35, 38, 44, 255), outline=(180, 190, 205, 255))
    draw.line([bx, by, hx, hy], fill=(55, 60, 68, 255), width=3)
    
    gx1 = hx + int(cos_p * 7)
    gy1 = hy + int(sin_p * 7)
    gx2 = hx - int(cos_p * 7)
    gy2 = hy - int(sin_p * 7)
    draw.line([gx1, gy1, gx2, gy2], fill=(42, 46, 52, 255), width=4)
    draw.line([gx1, gy1, gx2, gy2], fill=(210, 215, 225, 255), width=1)
    
    tx = hx + int(cos_a * blade_len)
    ty = hy + int(sin_a * blade_len)
    
    b1_x = hx + int(cos_p * 4) + int(cos_a * 3)
    b1_y = hy + int(sin_p * 4) + int(sin_a * 3)
    b2_x = hx - int(cos_p * 4) + int(cos_a * 3)
    b2_y = hy - int(sin_p * 4) + int(sin_a * 3)
    
    tp1_x = tx - int(cos_a * 8) + int(cos_p * 4)
    tp1_y = ty - int(sin_a * 8) + int(sin_p * 4)
    tp2_x = tx - int(cos_a * 8) - int(cos_p * 4)
    tp2_y = ty - int(sin_a * 8) - int(sin_p * 4)
    
    blade_poly = [(b1_x, b1_y), (tp1_x, tp1_y), (tx, ty), (tp2_x, tp2_y), (b2_x, b2_y)]
    draw.polygon(blade_poly, fill=(225, 232, 245, 255), outline=(50, 56, 65, 255))
    
    fuller_c = (255, 130, 20, 255) if thermal else (120, 130, 145, 255)
    draw.line([hx + int(cos_a * 4), hy + int(sin_a * 4), tx - int(cos_a * 6), ty - int(sin_a * 6)],
              fill=fuller_c, width=2)
              
    if thermal:
        draw.line([b1_x, b1_y, tx, ty], fill=(255, 220, 80, 220), width=1)
        draw.line([b2_x, b2_y, tx, ty], fill=(255, 170, 30, 220), width=1)
        draw.point((tx, ty), fill=(255, 255, 255, 255))
        
    return (tx, ty)

def draw_thrust_arm_natural(draw, shoulder_x, shoulder_y, hand_x, hand_y):
    mid_x = (shoulder_x + hand_x) // 2
    mid_y = max(shoulder_y, hand_y) + 8
    draw.line([shoulder_x, shoulder_y, mid_x, mid_y], fill=(92, 102, 75, 255), width=7)
    draw.line([shoulder_x, shoulder_y, mid_x, mid_y], fill=(160, 175, 130, 255), width=2)
    draw.ellipse([mid_x - 4, mid_y - 4, mid_x + 4, mid_y + 4], fill=(42, 46, 52, 255), outline=(220, 225, 230, 255))
    draw.point((mid_x, mid_y), fill=(100, 105, 115, 255))
    draw.line([mid_x, mid_y, hand_x, hand_y], fill=(88, 98, 72, 255), width=6)
    draw.line([mid_x, mid_y, hand_x, hand_y], fill=(145, 160, 115, 255), width=2)
    draw.ellipse([hand_x - 4, hand_y - 4, hand_x + 4, hand_y + 4], fill=(48, 52, 60, 255), outline=(220, 225, 230, 255))

melee_frames = []

# Frame 0: Linebreaker Stance & Sheathed Blade
f0 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
f0.paste(body_clean, (2, 2), body_clean)
f0.paste(shield_layer, (2, 2), shield_layer)
d0 = ImageDraw.Draw(f0)
for vx in range(10, 32):
    prog = (32 - vx) / 22.0
    d0.line([vx, 40, vx, 46], fill=(0, 220, 255, int(220 * (1.0 - prog))), width=1)
draw_gladius_clean(d0, hx=42, hy=68, angle_deg=120, blade_len=26, thermal=True)
melee_frames.append(f0)

# Frame 1: Rocket Lunge (+14px) - Drawing Blade Upward
f1 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
f1.paste(body_clean, (14, 2), body_clean)
f1.paste(shield_layer, (14, 2), shield_layer)
d1 = ImageDraw.Draw(f1)
draw_thrust_arm_natural(d1, shoulder_x=58, shoulder_y=50, hand_x=66, hand_y=46)
draw_gladius_clean(d1, hx=66, hy=46, angle_deg=65, blade_len=30, thermal=True)
melee_frames.append(f1)

# Frame 2: Spartan Shield Slam (+22px) - Massive Kinetic Shockwave!
f2 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
f2.paste(body_clean, (22, 2), body_clean)
f2.paste(shield_layer, (22, 2), shield_layer)
d2 = ImageDraw.Draw(f2)
for sy in range(35, 120, 4):
    d2.line([150, sy, 157, sy + ((sy % 8) - 4)], fill=(255, 245, 150, 240), width=2)
for sp in [(154, 45), (156, 60), (158, 75), (155, 95), (157, 110), (153, 52), (155, 85)]:
    d2.point(sp, fill=(255, 255, 255, 255))
draw_gladius_clean(d2, hx=68, hy=42, angle_deg=35, blade_len=32, thermal=True)
melee_frames.append(f2)

# Frame 3: Target Pinned & Gladius Thrust Windup (+20px)
f3 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
f3.paste(body_clean, (20, 2), body_clean)
shield_low = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
shield_low.paste(shield_layer, (20, 10), shield_layer)
f3.paste(shield_low, (0, 0), shield_low)
d3 = ImageDraw.Draw(f3)
draw_thrust_arm_natural(d3, shoulder_x=64, shoulder_y=50, hand_x=62, hand_y=52)
draw_gladius_clean(d3, hx=62, hy=52, angle_deg=0, blade_len=34, thermal=True)
d3.ellipse([58, 48, 66, 56], fill=(255, 220, 50, 255))
melee_frames.append(f3)

# Frame 4: Lethal Thermal Gladius Thrust (+16px body, shield at flank, blade in open air)
f4 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
f4.paste(body_clean, (16, 2), body_clean)
shield_flank = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
shield_flank.paste(shield_layer, (6, 10), shield_layer)
f4.paste(shield_flank, (0, 0), shield_flank)
d4 = ImageDraw.Draw(f4)
draw_thrust_arm_natural(d4, shoulder_x=62, shoulder_y=50, hand_x=118, hand_y=52)
tx, ty = draw_gladius_clean(d4, hx=118, hy=52, angle_deg=0, blade_len=38, thermal=True)
for off_y in [-3, 0, 3]:
    d4.line([95, 52 + off_y, 145, 52 + off_y], fill=(255, 200, 60, 200), width=1)
melee_frames.append(f4)

# Frame 5: Molten Armor Detonation (+16px, impact at 156, 52)
f5 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
f5.paste(body_clean, (16, 2), body_clean)
f5.paste(shield_flank, (0, 0), shield_flank)
d5 = ImageDraw.Draw(f5)
draw_thrust_arm_natural(d5, shoulder_x=62, shoulder_y=50, hand_x=118, hand_y=52)
tx, ty = draw_gladius_clean(d5, hx=118, hy=52, angle_deg=0, blade_len=38, thermal=True)
d5.ellipse([tx - 16, ty - 16, tx + 16, ty + 16], outline=(255, 255, 240, 255), width=2)
d5.ellipse([tx - 24, ty - 14, tx + 24, ty + 14], outline=(255, 140, 20, 200), width=2)
for ang in range(-90, 95, 15):
    rad = math.radians(ang)
    sx = tx + int(math.cos(rad) * 22)
    sy = ty + int(math.sin(rad) * 22)
    d5.line([tx, ty, sx, sy], fill=(255, 230, 80, 255), width=2)
melee_frames.append(f5)

# Frame 6: Steam Relief & Recovery (+10px)
f6 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
f6.paste(body_clean, (10, 1), body_clean)
f6.paste(shield_layer, (10, 1), shield_layer)
d6 = ImageDraw.Draw(f6)
draw_gladius_clean(d6, hx=48, hy=68, angle_deg=115, blade_len=28, thermal=False)
for sx in range(74, 102):
    for sy in range(64, 86):
        dist = math.hypot(sx - 86, sy - 74)
        if dist <= 8:
            d6.point((sx, sy), fill=(215, 220, 225, int(150 * (1.0 - dist / 8.0))))
melee_frames.append(f6)

# =========================================================================
# 6. BUILD spr_ms_centurion_boost (4 FRAMES)
# =========================================================================
boost_frames = []
for b_idx in range(4):
    b_im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    b_im.paste(master_clean, (6 + (b_idx % 2), 2), master_clean)
    d_b = ImageDraw.Draw(b_im)
    fl_len = 24 + (b_idx * 4)
    for x in range(32 - fl_len, 32):
        prog = (32 - x) / float(fl_len)
        half_w = 4.0 * (1.0 - prog * 0.5)
        for dy in range(-int(math.ceil(half_w)), int(math.ceil(half_w)) + 1):
            if abs(dy) <= half_w:
                if prog < 0.3:
                    col = (255, 255, 255, 240)
                elif prog < 0.7:
                    col = (0, 220, 255, int(220 * (1.0 - prog)))
                else:
                    col = (255, 140, 20, int(180 * (1.0 - prog)))
                d_b.point((x, 38 + dy), fill=col)
                d_b.point((x, 46 + dy), fill=col)
    dust_x = 44 - (b_idx * 5)
    dust_y = 132
    for dx in range(dust_x - 12, dust_x + 6):
        for dy in range(dust_y - 4, dust_y + 4):
            dist = math.hypot(dx - dust_x, dy - dust_y)
            if dist <= 5:
                d_b.point((dx, dy), fill=(180, 175, 160, int(140 * (1.0 - dist / 5.0))))
    boost_frames.append(b_im)

# =========================================================================
# 7. BUILD spr_ms_centurion_idle_damaged (4 FRAMES)
# =========================================================================
dmg_frames = []
for d_idx in range(4):
    dmg = idle_frames[d_idx].copy()
    d_draw = ImageDraw.Draw(dmg)
    d_draw.ellipse([80, 53, 86, 59], fill=(25, 25, 28, 240))
    d_draw.line([78, 56, 88, 56], fill=(15, 15, 18, 255), width=1)
    d_draw.ellipse([112, 70, 118, 76], fill=(30, 32, 35, 240))
    d_draw.line([115, 76, 115, 86 + (d_idx * 2)], fill=(40, 25, 15, 220), width=1)
    if d_idx % 2 == 1:
        d_draw.point((84, 52), fill=(255, 240, 100, 255))
        d_draw.point((85, 51), fill=(255, 255, 255, 255))
        d_draw.point((116, 71), fill=(255, 200, 50, 255))
    dmg_frames.append(dmg)

# =========================================================================
# 8. BUILD spr_ms_centurion_destroyed (1 FRAME)
# =========================================================================
dest_im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
dest_im.paste(master_clean, (0, 10), master_clean)
d_dest = ImageDraw.Draw(dest_im)

dest_pixels = dest_im.load()
for y in range(dest_im.height):
    for x in range(dest_im.width):
        r, g, b, a = dest_pixels[x, y]
        if a > 0:
            gray = int(r * 0.3 + g * 0.5 + b * 0.2) * 0.55
            dest_pixels[x, y] = (int(gray * 0.8), int(gray * 0.8), int(gray * 0.75), a)

d_dest.ellipse([78, 62, 88, 70], fill=(20, 20, 22, 255))
d_dest.point((82, 65), fill=(255, 140, 20, 255))
d_dest.point((83, 66), fill=(255, 220, 40, 255))

for sm_idx, (sx, sy) in enumerate([(82, 54), (80, 44), (76, 32), (72, 20), (84, 40), (86, 28)]):
    rad = 4 + sm_idx
    d_dest.ellipse([sx - rad, sy - rad, sx + rad, sy + rad], fill=(50, 52, 56, 170 - (sm_idx * 20)))

# =========================================================================
# 9. PACKAGING HELPER FUNCTION (PRESERVES EXACT GAMEMAKER .YY INTEGRITY)
# =========================================================================
def save_gmsprite_suite(sprite_name, frames, fps=12.0):
    sdir = f"sprites/{sprite_name}"
    os.makedirs(sdir, exist_ok=True)
    num_f = len(frames)
    
    strip = Image.new("RGBA", (160 * num_f, 160), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        strip.paste(fr, (i * 160, 0))
    strip.save(os.path.join(sdir, f"{sprite_name}_strip{num_f}.png"))
    frames[0].save(os.path.join(sdir, f"{sprite_name}.png"))
    
    yy_path = os.path.join(sdir, f"{sprite_name}.yy")
    existing_f_ids = []
    if os.path.exists(yy_path):
        try:
            with open(yy_path, "r") as f:
                old_yy = json.load(f)
                frames_arr = old_yy.get("frames", [])
                for fr in frames_arr:
                    fid = fr.get("%Name") or fr.get("name")
                    if fid:
                        existing_f_ids.append(fid)
        except Exception as e:
            print(f"Warning reading {yy_path}: {e}")
            
    frame_ids = []
    for i in range(num_f):
        if i < len(existing_f_ids):
            frame_ids.append(existing_f_ids[i])
        else:
            frame_ids.append(str(uuid.uuid4()))
            
    for i, fid in enumerate(frame_ids):
        f_png = os.path.join(sdir, f"{fid}.png")
        frames[i].save(f_png)
        ldir = os.path.join(sdir, "layers", fid)
        os.makedirs(ldir, exist_ok=True)
        layer_files = [f for f in os.listdir(ldir) if f.endswith(".png")] if os.path.exists(ldir) else []
        layer_uuid = layer_files[0][:-4] if layer_files else str(uuid.uuid4())
        frames[i].save(os.path.join(ldir, f"{layer_uuid}.png"))
        
    keyframes = []
    for i, fid in enumerate(frame_ids):
        keyframes.append({
            "$Keyframe<SpriteFrameKeyframe>": "",
            "Channels": {
                "0": {
                    "$SpriteFrameKeyframe": "",
                    "Id": {
                        "name": fid,
                        "path": f"sprites/{sprite_name}/{sprite_name}.yy"
                    },
                    "resourceType": "SpriteFrameKeyframe",
                    "resourceVersion": "2.0"
                }
            },
            "Disabled": False,
            "id": str(uuid.uuid4()),
            "IsCreationKey": False,
            "Key": float(i),
            "Length": 1.0,
            "resourceType": "Keyframe<SpriteFrameKeyframe>",
            "resourceVersion": "2.0",
            "Stretch": False
        })
        
    frames_list = []
    for fid in frame_ids:
        frames_list.append({
            "$GMSpriteFrame": "v1",
            "%Name": fid,
            "name": fid,
            "resourceType": "GMSpriteFrame",
            "resourceVersion": "2.0"
        })
        
    layer_id = str(uuid.uuid4())
    yy_data = {
        "$GMSprite": "v2",
        "%Name": sprite_name,
        "bboxMode": 0,
        "bbox_bottom": 155,
        "bbox_left": 0,
        "bbox_right": 159,
        "bbox_top": 0,
        "collisionKind": 1,
        "collisionTolerance": 0,
        "DynamicTexturePage": False,
        "edgeFiltering": False,
        "For3D": False,
        "frames": frames_list,
        "gridX": 0,
        "gridY": 0,
        "height": 160,
        "HTile": False,
        "layers": [
            {
                "$GMImageLayer": "",
                "%Name": layer_id,
                "blendMode": 0,
                "displayName": "default",
                "isLocked": False,
                "name": layer_id,
                "opacity": 100.0,
                "resourceType": "GMImageLayer",
                "resourceVersion": "2.0",
                "visible": True
            }
        ],
        "name": sprite_name,
        "nineSlice": None,
        "origin": 9,
        "parent": {
            "name": "MechMakerConcept",
            "path": "MechMakerConcept.yyp"
        },
        "preMultiplyAlpha": False,
        "resourceType": "GMSprite",
        "resourceVersion": "2.0",
        "sequence": {
            "$GMSequence": "v1",
            "%Name": sprite_name,
            "resourceType": "GMSequence",
            "resourceVersion": "2.0",
            "autoRecord": True,
            "backdropHeight": 768,
            "backdropImageOpacity": 0.5,
            "backdropImagePath": "",
            "backdropWidth": 1366,
            "backdropXOffset": 0.0,
            "backdropYOffset": 0.0,
            "events": {
                "$KeyframeStore<MessageEventKeyframe>": "",
                "Keyframes": [],
                "resourceType": "KeyframeStore<MessageEventKeyframe>",
                "resourceVersion": "2.0"
            },
            "eventStubScript": None,
            "eventToFunction": {},
            "length": float(num_f),
            "lockOrigin": False,
            "moments": {
                "$KeyframeStore<MomentsEventKeyframe>": "",
                "Keyframes": [],
                "resourceType": "KeyframeStore<MomentsEventKeyframe>",
                "resourceVersion": "2.0"
            },
            "name": sprite_name,
            "playback": 1,
            "playbackSpeed": fps,
            "playbackSpeedType": 0,
            "showBackdrop": True,
            "showBackdropImage": False,
            "timeUnits": 1,
            "tracks": [
                {
                    "$GMSpriteFramesTrack": "",
                    "builtinName": 0,
                    "events": [],
                    "inheritsTrackColour": True,
                    "interpolation": 1,
                    "isCreationTrack": False,
                    "keyframes": {
                        "$KeyframeStore<SpriteFrameKeyframe>": "",
                        "Keyframes": keyframes,
                        "resourceType": "KeyframeStore<SpriteFrameKeyframe>",
                        "resourceVersion": "2.0"
                    },
                    "modifiers": [],
                    "name": "frames",
                    "resourceType": "GMSpriteFramesTrack",
                    "resourceVersion": "2.0",
                    "spriteId": None,
                    "trackColour": 0,
                    "tracks": [],
                    "traits": 0
                }
            ],
            "visibleRange": None,
            "volume": 1.0,
            "xorigin": 80,
            "yorigin": 145
        },
        "swatchColours": None,
        "swfPrecision": 2.525,
        "textureGroupId": {
            "name": "Default",
            "path": "texturegroups/Default"
        },
        "type": 0,
        "VTile": False,
        "width": 160
    }
    
    with open(yy_path, "w") as f:
        json.dump(yy_data, f, indent=2)
    print(f"Successfully packaged {sprite_name} ({num_f} frames, fps={fps})")

# Execute packaging for all 6 core animations:
save_gmsprite_suite("spr_ms_centurion_idle", idle_frames, fps=8.0)
save_gmsprite_suite("spr_ms_centurion_fire_chaingun", fire_frames, fps=12.0)
save_gmsprite_suite("spr_ms_centurion_attack_melee", melee_frames, fps=8.0)
save_gmsprite_suite("spr_ms_centurion_boost", boost_frames, fps=10.0)
save_gmsprite_suite("spr_ms_centurion_idle_damaged", dmg_frames, fps=6.0)
save_gmsprite_suite("spr_ms_centurion_destroyed", [dest_im], fps=1.0)

print("\n=== ALL CENTURION ASSETS PACKAGED WITH ROTATING BARRELS & SPIN-DOWN! ===")
