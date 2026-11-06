#!/usr/bin/env python3
"""
Complete Production Suite for OC-A01 Aether Striker (ms_colony_aether_01)
Outer Colony League Flagship Superiority Striker (Faction B)
Canvas: 160x160, Origin: (80, 145)
Facing: 3/4 FRONT-RIGHT (xscale = 1)
Primary Ranged: Type-6A High-Output Thermal Beam Rifle
Melee: High-Energy Thermal Plasma Saber
Defense: Aerosteel Deflector Shield

Strict adherence to Lead Art Asset Analyst rules:
- Zero occluded weapons behind shield.
- Weapon clearly drawn and held in hand in the foreground.
- Zero weapon duplication (lowered gun cleanly erased during saber strike).
- Cherenkov cyan energy (#45E5E0, #72F5F0) with pure white core (#FFFFFF).
- Precise mathematical beam alignment along the rifle barrel bore.
- Fully connected limbs (shoulder -> bicep -> elbow -> forearm -> hand).
"""
import os
import sys
import math
import json
import uuid
from PIL import Image, ImageDraw

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ARTIFACT_DIR = "/home/tom/.gemini/antigravity/brain/e8ad7f5f-e9da-49e2-b06a-c225ea63e0a7"

# Color Palette Constants for Outer Colony League
AEROSTEEL_WHITE = (228, 247, 235, 255)
AEROSTEEL_LIGHT = (202, 226, 213, 255)
AEROSTEEL_MID   = (154, 186, 175, 255)
AEROSTEEL_DARK  = (108, 142, 133, 255)
CHASSIS_DARK    = (34, 46, 48, 255)
CHASSIS_BLACK   = (14, 20, 22, 255)
AMBER_VISOR     = (240, 180, 50, 255)
AMBER_CORE      = (255, 230, 130, 255)

BEAM_CORE_WHITE = (255, 255, 255, 255)
BEAM_CYAN_HOT   = (180, 255, 252, 255)
BEAM_CYAN_MAIN  = (69, 229, 224, 255)
BEAM_CYAN_DEEP  = (28, 168, 175, 255)
BEAM_CYAN_FAINT = (18, 92, 105, 180)

# =========================================================================
# 1. LOAD MASTER BASE SPRITE & DISSECT COMPONENTS
# =========================================================================
idle_path = os.path.join(PROJECT_ROOT, "sprites", "spr_ms_aether_idle")
with open(os.path.join(idle_path, "spr_ms_aether_idle.yy")) as f:
    idle_yy = json.load(f)

f0_id = idle_yy["frames"][0]["name"]
master_base = Image.open(os.path.join(idle_path, f"{f0_id}.png")).convert("RGBA")
m_pix = master_base.load()

# Clean Shield Layer
shield_layer = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
s_pix = shield_layer.load()
for y in range(48, 105):
    for x in range(92, 126):
        r, g, b, a = m_pix[x, y]
        if a > 100 and (r > 130 and g > 160 and b > 150):
            s_pix[x, y] = (r, g, b, a)

# Clean Body without lowered weapon
gun_mask = Image.new("L", (160, 160), 0)
dmask = ImageDraw.Draw(gun_mask)
dmask.polygon([(104, 60), (128, 60), (128, 94), (104, 94)], fill=255)

body_clean = master_base.copy()
b_pix = body_clean.load()

for y in range(160):
    for x in range(160):
        if gun_mask.getpixel((x, y)) > 128:
            b_pix[x, y] = (0, 0, 0, 0)

# Seamlessly restore right thigh/leg and hip armor under erased gun
for y in range(65, 96):
    prog = (y - 65) / 31.0
    lx = int(88 - 2 * prog)
    rx = int(106 - 4 * prog)
    for x in range(lx, rx + 1):
        if x == lx:
            b_pix[x, y] = AEROSTEEL_WHITE
        elif x == rx:
            b_pix[x, y] = CHASSIS_BLACK
        elif x > rx - 3:
            b_pix[x, y] = CHASSIS_DARK
        elif x == lx + 1:
            b_pix[x, y] = AEROSTEEL_LIGHT
        else:
            b_pix[x, y] = AEROSTEEL_MID

# =========================================================================
# 2. ARTICULATED ARM DRAWING ROUTINE
# =========================================================================
def draw_aether_arm(draw, shoulder_x, shoulder_y, hand_x, hand_y, holding_weapon=True):
    mid_x = (shoulder_x + hand_x) // 2 + 3
    mid_y = (shoulder_y + hand_y) // 2 + 5
    
    # Bicep & Armature
    draw.line([shoulder_x, shoulder_y, mid_x, mid_y], fill=CHASSIS_DARK, width=5)
    draw.line([shoulder_x, shoulder_y - 1, mid_x, mid_y - 1], fill=AEROSTEEL_MID, width=2)
    
    # Elbow joint
    draw.ellipse([mid_x - 3, mid_y - 3, mid_x + 3, mid_y + 3], fill=CHASSIS_BLACK, outline=AEROSTEEL_DARK)
    
    # Forearm gauntlet
    draw.line([mid_x, mid_y, hand_x, hand_y], fill=AEROSTEEL_MID, width=4)
    draw.line([mid_x, mid_y - 1, hand_x, hand_y - 1], fill=AEROSTEEL_WHITE, width=2)
    draw.line([mid_x, mid_y + 2, hand_x, hand_y + 2], fill=CHASSIS_BLACK, width=1)
    
    # Hand manipulator
    draw.ellipse([hand_x - 3, hand_y - 3, hand_x + 3, hand_y + 3], fill=CHASSIS_DARK, outline=AEROSTEEL_LIGHT)

# =========================================================================
# 3. TYPE-6A HIGH-OUTPUT THERMAL BEAM RIFLE ROUTINE
# =========================================================================
def draw_type6a_beam_rifle(draw, hx, hy, recoil_x=0):
    """
    Draws the Type-6A High-Output Thermal Beam Rifle.
    Manipulator hand holds the grip at (hx, hy).
    Rifle barrel extends forward to (hx + 42 + recoil_x, hy - 4).
    Returns muzzle bore coordinates (bx, by).
    """
    rx = hx - 12 + recoil_x
    ry = hy - 6
    
    # 1. Rear Stock & E-Cap Power Cell
    draw.polygon([(rx - 10, ry + 2), (rx, ry), (rx, ry + 8), (rx - 8, ry + 10)],
                 fill=CHASSIS_DARK, outline=CHASSIS_BLACK)
    draw.rectangle([rx - 6, ry + 4, rx - 1, ry + 9], fill=AEROSTEEL_DARK)
    
    # 2. Main Receiver Body
    draw.rectangle([rx, ry - 3, rx + 18, ry + 7], fill=CHASSIS_DARK, outline=CHASSIS_BLACK)
    draw.line([rx + 2, ry - 2, rx + 16, ry - 2], fill=AEROSTEEL_WHITE) # top aerosteel plate
    draw.line([rx + 2, ry + 5, rx + 16, ry + 5], fill=CHASSIS_BLACK) # under-receiver bevel
    
    # 3. Optical Targeting Sensor (Amber/Cyan reticle)
    draw.rectangle([rx + 6, ry - 7, rx + 14, ry - 4], fill=CHASSIS_BLACK, outline=AEROSTEEL_MID)
    draw.point((rx + 13, ry - 6), fill=AMBER_VISOR)
    draw.point((rx + 13, ry - 5), fill=BEAM_CYAN_MAIN)
    
    # 4. Twin Magnetic Accelerator Rails & Barrel Shroud
    draw.rectangle([rx + 18, ry - 2, rx + 38, ry + 3], fill=AEROSTEEL_MID, outline=CHASSIS_DARK)
    draw.line([rx + 18, ry - 1, rx + 38, ry - 1], fill=AEROSTEEL_WHITE) # upper rail highlight
    draw.line([rx + 18, ry + 1, rx + 38, ry + 1], fill=BEAM_CYAN_MAIN)  # internal accelerator guide glow
    draw.line([rx + 18, ry + 2, rx + 38, ry + 2], fill=CHASSIS_BLACK)   # lower rail shadow
    
    # Under-barrel Thermal Radiator Vanes
    for vx in range(rx + 20, rx + 36, 4):
        draw.line([vx, ry + 4, vx, ry + 6], fill=CHASSIS_BLACK)
        draw.point((vx + 1, ry + 5), fill=AEROSTEEL_DARK)
    
    # 5. Muzzle Emitter Ring & Bore
    bx = rx + 40
    by = ry
    draw.rectangle([bx - 2, by - 3, bx, by + 4], fill=CHASSIS_BLACK, outline=AEROSTEEL_WHITE)
    draw.point((bx, by), fill=BEAM_CORE_WHITE)
    
    return bx, by

# =========================================================================
# 4. BEAM RIFLE FIRING SEQUENCE (4 FRAMES)
# =========================================================================
fire_beam_frames = []

# FRAME 0: Pre-charge & Aim
# Stable firing posture, Cherenkov magnetic energy condensing at muzzle bore
f0 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
f0.paste(body_clean, (0, 0), body_clean)
# Shield braced low/back on left flank
s0 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
s0.paste(shield_layer, (-4, 4), shield_layer)
f0.paste(s0, (0, 0), s0)

d0 = ImageDraw.Draw(f0)
draw_aether_arm(d0, shoulder_x=76, shoulder_y=48, hand_x=102, hand_y=64)
bx0, by0 = draw_type6a_beam_rifle(d0, hx=102, hy=64, recoil_x=0)

# Pre-charge energy glow at muzzle
d0.ellipse([bx0 - 3, by0 - 3, bx0 + 3, by0 + 3], fill=BEAM_CYAN_MAIN)
d0.ellipse([bx0 - 1, by0 - 1, bx0 + 1, by0 + 1], fill=BEAM_CORE_WHITE)
for dx, dy in [(-4, 0), (4, 0), (0, -4), (0, 4), (-3, -3), (3, -3), (-3, 3), (3, 3)]:
    d0.point((bx0 + dx, by0 + dy), fill=BEAM_CYAN_HOT)
fire_beam_frames.append(f0)

# FRAME 1: Coherent Beam Pulse Discharge!
# High-output particle beam fires forward, chassis recoils -3px, brilliant white/cyan lance
f1 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
f1.paste(body_clean, (-2, 0), body_clean)
s1 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
s1.paste(shield_layer, (-6, 4), shield_layer)
f1.paste(s1, (0, 0), s1)

d1 = ImageDraw.Draw(f1)
draw_aether_arm(d1, shoulder_x=74, shoulder_y=48, hand_x=99, hand_y=64)
bx1, by1 = draw_type6a_beam_rifle(d1, hx=99, hy=64, recoil_x=-3)

# Massive Coherent Beam Lance penetrating forward to x=160
# Outer Cherenkov Cyan Corona
d1.rectangle([bx1 + 2, by1 - 6, 160, by1 + 6], fill=BEAM_CYAN_FAINT)
d1.rectangle([bx1 + 1, by1 - 4, 160, by1 + 4], fill=BEAM_CYAN_DEEP)
d1.rectangle([bx1, by1 - 3, 160, by1 + 3], fill=BEAM_CYAN_MAIN)
d1.rectangle([bx1, by1 - 2, 160, by1 + 2], fill=BEAM_CYAN_HOT)
# White-hot razor-sharp core
d1.rectangle([bx1, by1 - 1, 160, by1 + 1], fill=BEAM_CORE_WHITE)

# Radial Muzzle Blast Rings & Ionization Flares
d1.ellipse([bx1 - 6, by1 - 8, bx1 + 6, by1 + 8], outline=BEAM_CYAN_MAIN, width=1)
d1.ellipse([bx1 - 4, by1 - 5, bx1 + 4, by1 + 5], fill=BEAM_CYAN_HOT)
d1.ellipse([bx1 - 2, by1 - 3, bx1 + 2, by1 + 3], fill=BEAM_CORE_WHITE)

# Dynamic light reflection on front armor
for ly in range(48, 80):
    for lx in range(70, 95):
        p = f1.getpixel((lx, ly))
        if p[3] > 100:
            f1.putpixel((lx, ly), (min(255, p[0] + 25), min(255, p[1] + 45), min(255, p[2] + 45), p[3]))
fire_beam_frames.append(f1)

# FRAME 2: Sustained Penetration & Dissipation
# Beam body sustaining with expanding ionization rings, recoil stabilizing (-1px)
f2 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
f2.paste(body_clean, (-1, 0), body_clean)
s2 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
s2.paste(shield_layer, (-5, 4), shield_layer)
f2.paste(s2, (0, 0), s2)

d2 = ImageDraw.Draw(f2)
draw_aether_arm(d2, shoulder_x=75, shoulder_y=48, hand_x=101, hand_y=64)
bx2, by2 = draw_type6a_beam_rifle(d2, hx=101, hy=64, recoil_x=-1)

# Sustained beam dissipation envelope
d2.rectangle([bx2 + 6, by2 - 5, 160, by2 + 5], fill=BEAM_CYAN_FAINT)
d2.rectangle([bx2 + 4, by2 - 3, 160, by2 + 3], fill=BEAM_CYAN_MAIN)
d2.rectangle([bx2 + 2, by2 - 1, 160, by2 + 1], fill=BEAM_CYAN_HOT)
d2.line([bx2 + 10, by2, 160, by2], fill=BEAM_CORE_WHITE, width=1)

# Expanding Ionization Rings along beam path
for rx_ring in [bx2 + 12, bx2 + 28, bx2 + 44]:
    if rx_ring < 156:
        d2.ellipse([rx_ring - 2, by2 - 6, rx_ring + 2, by2 + 6], outline=BEAM_CYAN_MAIN, width=1)
        d2.point((rx_ring, by2 - 7), fill=BEAM_CYAN_HOT)
        d2.point((rx_ring, by2 + 7), fill=BEAM_CYAN_HOT)

# Muzzle flare dissipating
d2.ellipse([bx2 - 3, by2 - 4, bx2 + 3, by2 + 4], fill=BEAM_CYAN_MAIN)
d2.ellipse([bx2 - 1, by2 - 2, bx2 + 1, by2 + 2], fill=BEAM_CORE_WHITE)
fire_beam_frames.append(f2)

# FRAME 3: Beam Cutoff & Radiator Venting
# Primary beam severed, cooling thermal gradient on barrel, radiator vapor
f3 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
f3.paste(body_clean, (0, 0), body_clean)
s3 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
s3.paste(shield_layer, (-4, 4), shield_layer)
f3.paste(s3, (0, 0), s3)

d3 = ImageDraw.Draw(f3)
draw_aether_arm(d3, shoulder_x=76, shoulder_y=48, hand_x=102, hand_y=64)
bx3, by3 = draw_type6a_beam_rifle(d3, hx=102, hy=64, recoil_x=0)

# Residual glowing gas exiting bore
d3.ellipse([bx3 - 1, by3 - 2, bx3 + 2, by3 + 2], fill=BEAM_CYAN_DEEP)
d3.point((bx3 + 1, by3), fill=BEAM_CYAN_HOT)
# Thermal radiator vapor venting downward
for vx in range(bx3 - 20, bx3 - 4, 4):
    d3.point((vx, by3 + 7), fill=(100, 220, 230, 200))
    d3.point((vx + 1, by3 + 9), fill=(60, 180, 200, 150))
    d3.point((vx, by3 + 11), fill=(40, 140, 160, 100))
fire_beam_frames.append(f3)

print("spr_ms_aether_fire_beam 4-frame suite rendered successfully.")

# =========================================================================
# 5. HIGH-ENERGY THERMAL PLASMA SABER ROUTINE & SEQUENCE (4 FRAMES)
# =========================================================================
def draw_plasma_saber(draw, hx, hy, angle_deg, blade_len=36, intensity=1.0):
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    # 1. Cylindrical Emitter Hilt (length 10px in opposite direction)
    hilt_len = 10
    back_x = hx - int(hilt_len * cos_a)
    back_y = hy - int(hilt_len * sin_a)
    draw.line([back_x, back_y, hx, hy], fill=CHASSIS_DARK, width=3)
    draw.line([back_x, back_y, hx, hy], fill=AEROSTEEL_LIGHT, width=1)
    
    # Emitter nozzle ring
    draw.ellipse([hx - 2, hy - 2, hx + 2, hy + 2], fill=CHASSIS_BLACK, outline=BEAM_CYAN_MAIN)
    
    # 2. Thermal Plasma Blade
    tip_x = hx + int(blade_len * cos_a)
    tip_y = hy + int(blade_len * sin_a)
    
    # Outer Cyan Plasma Sheath
    draw.line([hx, hy, tip_x, tip_y], fill=BEAM_CYAN_DEEP, width=5)
    draw.line([hx, hy, tip_x, tip_y], fill=BEAM_CYAN_MAIN, width=3)
    draw.line([hx, hy, tip_x, tip_y], fill=BEAM_CYAN_HOT, width=2)
    # Brilliant White-Hot Razor Core
    draw.line([hx, hy, tip_x, tip_y], fill=BEAM_CORE_WHITE, width=1)
    
    # Plasma Blade Tip (tapered needle)
    draw.point((tip_x, tip_y), fill=BEAM_CORE_WHITE)
    draw.point((tip_x + int(cos_a), tip_y + int(sin_a)), fill=BEAM_CYAN_HOT)
    
    return tip_x, tip_y

attack_saber_frames = []

# FRAME 0: High-Speed Dash & Saber Ignition
# Suit surges forward +4px, draws hilt forward, ignition sparks
f_sab0 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
f_sab0.paste(body_clean, (4, 0), body_clean)
s_sab0 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
s_sab0.paste(shield_layer, (0, 2), shield_layer)
f_sab0.paste(s_sab0, (0, 0), s_sab0)

d_sab0 = ImageDraw.Draw(f_sab0)
draw_aether_arm(d_sab0, shoulder_x=80, shoulder_y=48, hand_x=98, hand_y=68)
draw_plasma_saber(d_sab0, hx=98, hy=68, angle_deg=25, blade_len=24)
# Ignition flare at hilt nozzle
d_sab0.ellipse([96, 66, 100, 70], fill=BEAM_CORE_WHITE)
d_sab0.ellipse([94, 64, 102, 72], outline=BEAM_CYAN_MAIN, width=1)
# Vernier boost pulse at rear
for vy in range(65, 85, 3):
    d_sab0.line([28, vy, 36, vy], fill=BEAM_CYAN_MAIN, width=1)
attack_saber_frames.append(f_sab0)

# FRAME 1: High Overhead Wind-up
# Blade raised high overhead ready to cleave downward
f_sab1 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
f_sab1.paste(body_clean, (8, 0), body_clean)
s_sab1 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
s_sab1.paste(shield_layer, (4, 4), shield_layer)
f_sab1.paste(s_sab1, (0, 0), s_sab1)

d_sab1 = ImageDraw.Draw(f_sab1)
draw_aether_arm(d_sab1, shoulder_x=84, shoulder_y=48, hand_x=92, hand_y=38)
draw_plasma_saber(d_sab1, hx=92, hy=38, angle_deg=-45, blade_len=36)
# Plasma crackle along overhead blade
for sp_x, sp_y in [(105, 26), (115, 18), (122, 12)]:
    d_sab1.point((sp_x, sp_y - 1), fill=BEAM_CYAN_HOT)
    d_sab1.point((sp_x + 1, sp_y), fill=BEAM_CORE_WHITE)
attack_saber_frames.append(f_sab1)

# FRAME 2: Dynamic Cleave / Sweeping Crescent Slash Arc!
# Massive forward strike cutting diagonally across target space
f_sab2 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
f_sab2.paste(body_clean, (12, 0), body_clean)
s_sab2 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
s_sab2.paste(shield_layer, (6, 6), shield_layer)
f_sab2.paste(s_sab2, (0, 0), s_sab2)

d_sab2 = ImageDraw.Draw(f_sab2)
draw_aether_arm(d_sab2, shoulder_x=88, shoulder_y=48, hand_x=112, hand_y=68)
draw_plasma_saber(d_sab2, hx=112, hy=68, angle_deg=35, blade_len=38)

# Giant Sweeping Energy Arc
# Arc sweeps from (105, 20) down through (145, 60) to (154, 98)
d_sab2.arc([85, 15, 156, 110], start=290, end=420, fill=BEAM_CYAN_DEEP, width=5)
d_sab2.arc([87, 17, 154, 108], start=295, end=415, fill=BEAM_CYAN_MAIN, width=3)
d_sab2.arc([88, 18, 153, 107], start=300, end=410, fill=BEAM_CYAN_HOT, width=2)
d_sab2.arc([89, 19, 152, 106], start=305, end=405, fill=BEAM_CORE_WHITE, width=1)

# Dynamic light reflection on front torso armor
for ly in range(45, 80):
    for lx in range(75, 105):
        p = f_sab2.getpixel((lx, ly))
        if p[3] > 100:
            f_sab2.putpixel((lx, ly), (min(255, p[0] + 30), min(255, p[1] + 50), min(255, p[2] + 50), p[3]))
attack_saber_frames.append(f_sab2)

# FRAME 3: Follow-through & Residual Vapor Reset
# Blade low forward, dissipating ionization sparks, posture resetting
f_sab3 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
f_sab3.paste(body_clean, (6, 0), body_clean)
s_sab3 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
s_sab3.paste(shield_layer, (2, 4), shield_layer)
f_sab3.paste(s_sab3, (0, 0), s_sab3)

d_sab3 = ImageDraw.Draw(f_sab3)
draw_aether_arm(d_sab3, shoulder_x=82, shoulder_y=48, hand_x=108, hand_y=78)
draw_plasma_saber(d_sab3, hx=108, hy=78, angle_deg=55, blade_len=32)

# Dissipating thermal vapor and sparks along slash trajectory
for arc_pt in [(148, 52), (152, 70), (146, 88), (135, 102)]:
    d_sab3.ellipse([arc_pt[0] - 2, arc_pt[1] - 2, arc_pt[0] + 2, arc_pt[1] + 2], fill=BEAM_CYAN_MAIN)
    d_sab3.point(arc_pt, fill=BEAM_CORE_WHITE)
    d_sab3.point((arc_pt[0] + 2, arc_pt[1] - 1), fill=BEAM_CYAN_FAINT)
attack_saber_frames.append(f_sab3)

print("spr_ms_aether_attack_saber 4-frame suite rendered successfully.")

# =========================================================================
# 6. SAVE ARTIFACT AUDIT SHEETS & INDIVIDUAL FRAMES
# =========================================================================
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def save_contact_sheet(frames, name):
    w, h = 160, 160
    n = len(frames)
    scale = 2
    sheet = Image.new("RGBA", (n * w * scale, h * scale + 30), (20, 24, 30, 255))
    draw = ImageDraw.Draw(sheet)
    for i, fr in enumerate(frames):
        scaled = fr.resize((w * scale, h * scale), Image.NEAREST)
        sheet.paste(scaled, (i * w * scale, 30), scaled)
        draw.text((i * w * scale + 10, 8), f"{name} Frame {i}", fill=(220, 220, 220, 255))
    sheet.save(os.path.join(ARTIFACT_DIR, f"audit_perfect_{name}.png"))
    print(f"Saved {ARTIFACT_DIR}/audit_perfect_{name}.png")

save_contact_sheet(fire_beam_frames, "spr_ms_aether_fire_beam")
save_contact_sheet(attack_saber_frames, "spr_ms_aether_attack_saber")

# =========================================================================
# 7. COMMIT NEW ASSETS TO GAMEMAKER SPRITE DIRECTORIES
# =========================================================================
def update_gamemaker_sprite(sprite_name, frames):
    spr_dir = os.path.join(PROJECT_ROOT, "sprites", sprite_name)
    yy_path = os.path.join(spr_dir, f"{sprite_name}.yy")
    with open(yy_path) as f:
        yy = json.load(f)
    
    # Save individual frame PNGs matching yy frame UUIDs
    for i, fr_info in enumerate(yy["frames"]):
        fid = fr_info["name"]
        frame_img = frames[i]
        png_path = os.path.join(spr_dir, f"{fid}.png")
        frame_img.save(png_path)
    
    # Save default sprite png (frame 0)
    frames[0].save(os.path.join(spr_dir, f"{sprite_name}.png"))
    
    # Save horizontal sprite strip
    strip_w = 160 * len(frames)
    strip = Image.new("RGBA", (strip_w, 160), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        strip.paste(fr, (i * 160, 0), fr)
    strip.save(os.path.join(spr_dir, f"{sprite_name}_strip{len(frames)}.png"))
    print(f"Successfully updated {sprite_name} in engine directory.")

update_gamemaker_sprite("spr_ms_aether_fire_beam", fire_beam_frames)
update_gamemaker_sprite("spr_ms_aether_attack_saber", attack_saber_frames)

print("\n=== AETHER STRIKER PRODUCTION SUITE BUILD COMPLETE ===")
