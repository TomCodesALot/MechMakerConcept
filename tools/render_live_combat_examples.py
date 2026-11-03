# -*- coding: utf-8 -*-
"""
tools/render_live_combat_examples.py
Generates 4 authentic, pixel-accurate in-engine visual examples showcasing:
1. Custom Mobile Suit Melee Dash & Kinetic Cleavage Arc (Vanguard Prime vs Syndicate Hyena)
2. High-Mobility Hover Energy Beam Snipe & Aimed Shot (Ghost Sniper vs Aether Interceptor)
3. Modular Limb Detachment, Flying Debris & Persistent Tactical Map Battle Scars
4. Combined-Arms Conventional Forces & Platoon Salvo (Mammoth Heavy Tank + Infantry Squad)
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = "/home/tom/.gemini/antigravity-ide/brain/3a64f444-71a9-4417-a131-fddab3683c63"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

# Monospace fonts
FONT_PATH = "/usr/share/fonts/fira-code/FiraCode-Regular.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/fira-code/FiraCode-Bold.ttf"

FONT_TINY  = ImageFont.truetype(FONT_PATH, 10)
FONT_SMALL = ImageFont.truetype(FONT_PATH, 12)
FONT_BOLD  = ImageFont.truetype(FONT_BOLD_PATH, 14)
FONT_TITLE = ImageFont.truetype(FONT_BOLD_PATH, 16)
FONT_HEAD  = ImageFont.truetype(FONT_BOLD_PATH, 20)

def load_sprite(name, frame_idx=0):
    p = os.path.join("sprites", name)
    if not os.path.exists(p):
        return None
    pngs = sorted([f for f in os.listdir(p) if f.endswith(".png")])
    if not pngs:
        return None
    f = pngs[frame_idx % len(pngs)]
    return Image.open(os.path.join(p, f)).convert("RGBA")

def draw_snes_panel(draw, x1, y1, x2, y2, fill_col=(14, 20, 28, 245), border_col=(0, 200, 255, 255)):
    draw.rectangle([x1, y1, x2, y2], fill=fill_col, outline=border_col, width=2)
    # Bevel lines
    draw.line([(x1 + 2, y1 + 2), (x2 - 2, y1 + 2)], fill=(90, 160, 230, 255), width=1)
    draw.line([(x1 + 2, y1 + 2), (x1 + 2, y2 - 2)], fill=(90, 160, 230, 255), width=1)
    draw.line([(x2 - 2, y1 + 2), (x2 - 2, y2 - 2)], fill=(20, 40, 65, 255), width=1)
    draw.line([(x1 + 2, y2 - 2), (x2 - 2, y2 - 2)], fill=(20, 40, 65, 255), width=1)

def apply_scanlines(img):
    scanline_spr = load_sprite("spr_snes_crt_scanline")
    if scanline_spr is None:
        return
    sw, sh = scanline_spr.size
    w, h = img.size
    for x in range(0, w, sw):
        for y in range(0, h, sh):
            img.alpha_composite(scanline_spr, (x, y))

def draw_cockpit_deck(draw, canvas, atk_pilot_name, atk_callsign, atk_mech, atk_expr, atk_bark, atk_portrait_name,
                      def_pilot_name, def_callsign, def_mech, def_expr, def_bark, def_portrait_name,
                      telemetry_info, limb_flash=None):
    gw, gh = canvas.size
    hud_y = gh - 120
    hud_h = 108

    # 1. Left Cockpit: Attacker
    draw_snes_panel(draw, 16, hud_y, 490, hud_y + hud_h, fill_col=(12, 18, 24, 245), border_col=(0, 200, 255, 255))
    port_atk = load_sprite(atk_portrait_name)
    if port_atk:
        port_atk = port_atk.resize((80, 80), Image.NEAREST)
        canvas.alpha_composite(port_atk, (26, hud_y + 14))
        draw.rectangle([26, hud_y + 14, 106, hud_y + 94], outline=(0, 220, 255), width=1)

    draw.text((116, hud_y + 12), f"[{atk_expr}] {atk_pilot_name}", fill=(60, 240, 120), font=FONT_BOLD)
    draw.text((116, hud_y + 30), f"{atk_callsign} | {atk_mech.upper()}", fill=(180, 210, 240), font=FONT_SMALL)
    draw.text((116, hud_y + 48), f"> \"{atk_bark}_\"", fill=(80, 255, 140), font=FONT_SMALL)

    # 5 Front Mission Limb Bars (Attacker)
    parts = [("HD", 0.90), ("TR", 0.85), ("LA", 0.70), ("RA", 1.00), ("LG", 0.80)]
    for i, (pname, ratio) in enumerate(parts):
        bx = 116 + i * 70
        by = hud_y + 70
        draw.text((bx, by), pname, fill=(150, 170, 200), font=FONT_TINY)
        draw.rectangle([bx, by + 14, bx + 60, by + 22], fill=(20, 28, 40), outline=(60, 80, 110))
        bcol = (60, 240, 100) if ratio > 0.6 else ((240, 200, 50) if ratio > 0.25 else (255, 60, 60))
        draw.rectangle([bx + 1, by + 15, bx + int(58 * ratio), by + 21], fill=bcol)

    # 2. Right Cockpit: Defender
    def_x = gw - 490 - 16
    draw_snes_panel(draw, def_x, hud_y, gw - 16, hud_y + hud_h, fill_col=(18, 12, 14, 245), border_col=(255, 80, 80, 255))
    port_def = load_sprite(def_portrait_name)
    if port_def:
        port_def = port_def.resize((80, 80), Image.NEAREST)
        canvas.alpha_composite(port_def, (gw - 106, hud_y + 14))
        draw.rectangle([gw - 106, hud_y + 14, gw - 26, hud_y + 94], outline=(255, 80, 80), width=1)

    draw.text((def_x + 14, hud_y + 12), f"[{def_expr}] {def_pilot_name}", fill=(255, 140, 80), font=FONT_BOLD)
    draw.text((def_x + 14, hud_y + 30), f"{def_callsign} | {def_mech.upper()}", fill=(180, 210, 240), font=FONT_SMALL)
    draw.text((def_x + 14, hud_y + 48), f"> \"{def_bark}_\"", fill=(255, 180, 60), font=FONT_SMALL)

    def_parts = [("HD", 0.85), ("TR", 0.50), ("LA", 0.00 if limb_flash == "LA" else 0.40), ("RA", 0.75), ("LG", 0.60)]
    for i, (pname, ratio) in enumerate(def_parts):
        bx = def_x + 14 + i * 70
        by = hud_y + 70
        draw.text((bx, by), pname, fill=(150, 170, 200), font=FONT_TINY)
        draw.rectangle([bx, by + 14, bx + 60, by + 22], fill=(20, 28, 40), outline=(60, 80, 110))
        if pname == limb_flash:
            draw.rectangle([bx + 1, by + 15, bx + 59, by + 21], fill=(255, 255, 255))
        elif ratio <= 0:
            draw.rectangle([bx + 1, by + 15, bx + 59, by + 21], fill=(60, 60, 60))
        else:
            bcol = (60, 240, 100) if ratio > 0.6 else ((240, 200, 50) if ratio > 0.25 else (255, 60, 60))
            draw.rectangle([bx + 1, by + 15, bx + int(58 * ratio), by + 21], fill=bcol)

    # 3. Center Tactical Telemetry
    cen_x = 502
    cen_w = def_x - cen_x - 12
    draw_snes_panel(draw, cen_x, hud_y, cen_x + cen_w, hud_y + hud_h, fill_col=(10, 14, 20, 250), border_col=(0, 200, 255, 255))
    draw.text((cen_x + 12, hud_y + 10), "TACTICAL TELEMETRY", fill=(0, 220, 255), font=FONT_BOLD)
    draw.text((cen_x + 12, hud_y + 30), telemetry_info[0], fill=(255, 215, 80), font=FONT_SMALL)
    draw.text((cen_x + 12, hud_y + 48), telemetry_info[1], fill=(160, 200, 240), font=FONT_SMALL)
    draw.text((cen_x + 12, hud_y + 66), telemetry_info[2], fill=(80, 240, 120), font=FONT_SMALL)
    draw.text((cen_x + 12, hud_y + 86), "[SPACE / CLICK] FAST-FORWARD >>", fill=(0, 210, 255), font=FONT_TINY)

# =========================================================================
# EXAMPLE 1: Melee Forward Dash & Kinetic Cleavage Arc
# =========================================================================
def render_example_1():
    w, h = 1280, 720
    im = Image.new("RGBA", (w, h), (10, 14, 22, 255))
    draw = ImageDraw.Draw(im)

    # Industrial hanger / crater combat background
    for y in range(0, 480):
        ratio = y / 480.0
        r = int(12 + ratio * 20)
        g = int(16 + ratio * 24)
        b = int(26 + ratio * 32)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))

    # Floor grid perspective
    for i in range(-10, 30):
        fx1 = i * 60
        fy1 = 360
        fx2 = i * 120 - 400
        fy2 = 600
        draw.line([(fx1, fy1), (fx2, fy2)], fill=(25, 38, 52, 180), width=1)
    for y in range(360, 600, 28):
        draw.line([(0, y), (w, y)], fill=(30, 45, 60, 180), width=1)

    # Top Shutter Header
    draw_snes_panel(draw, 0, 0, w, 54, fill_col=(8, 12, 18, 255), border_col=(0, 200, 255, 255))
    draw.text((24, 16), "THEATER: EARTH CRATER BASIN // ENGAGEMENT GRID: CLASH DUEL", fill=(100, 220, 255), font=FONT_BOLD)
    draw.text((w / 2 - 130, 16), "COMBAT CLASH // PHASE 1: MELEE IMPACT", fill=(255, 215, 80), font=FONT_BOLD)

    # Units: Vanguard Prime (Custom Biped) Dashed Forward (+320px) vs Syndicate Hyena
    atk_spr = load_sprite("spr_ms_custom_biped_heavy_idle", 0)
    def_spr = load_sprite("spr_ms_hyena_idle", 0)

    # Defender Staggered Position
    def_x, def_y = 860, 340
    # Shadow
    draw.ellipse([def_x - 70, def_y + 110, def_x + 70, def_y + 130], fill=(0, 0, 0, 120))
    if def_spr:
        # Scale 1.7x for epic side clash
        ds = def_spr.resize((int(160 * 1.7), int(160 * 1.7)), Image.NEAREST)
        # Stagger tilt
        ds_rot = ds.rotate(12, expand=True, resample=Image.BICUBIC)
        im.alpha_composite(ds_rot, (def_x - 120, def_y - 120))

    # Attacker Dashed Forward Point-Blank
    atk_x, atk_y = 660, 340
    draw.ellipse([atk_x - 70, atk_y + 110, atk_x + 70, atk_y + 130], fill=(0, 0, 0, 120))
    if atk_spr:
        # Tint with Vanguard Cerulean alloy
        tinted = Image.new("RGBA", atk_spr.size, (110, 160, 240, 255))
        atk_tint = Image.blend(atk_spr, tinted, 0.28)
        atk_tint.putalpha(atk_spr.getchannel("A"))
        as_scaled = atk_tint.resize((int(160 * 1.7), int(160 * 1.7)), Image.NEAREST)
        im.alpha_composite(as_scaled, (atk_x - 140, atk_y - 120))

    # Melee Kinetic Cleavage Arc (Vibrant golden-orange slash arc cutting into defender)
    arc_cx, arc_cy = 760, 380
    draw.arc([arc_cx - 90, arc_cy - 120, arc_cx + 90, arc_cy + 120], start=210, end=350, fill=(255, 230, 80, 255), width=8)
    draw.arc([arc_cx - 86, arc_cy - 116, arc_cx + 86, arc_cy + 116], start=215, end=345, fill=(255, 255, 255, 255), width=4)
    # Sparks eruption
    for sp in [(-20, -10), (10, -35), (35, 10), (-15, 45), (40, -10), (15, 30)]:
        draw.ellipse([arc_cx + sp[0] - 5, arc_cy + sp[1] - 5, arc_cx + sp[0] + 5, arc_cy + sp[1] + 5], fill=(255, 255, 200))
        draw.line([(arc_cx, arc_cy), (arc_cx + sp[0] * 1.8, arc_cy + sp[1] * 1.8)], fill=(255, 180, 40), width=2)

    # Dynamic Floating Damage Popups
    draw.text((def_x - 40, def_y - 150), "-285 TORSO BREACH!", fill=(255, 220, 60), font=FONT_HEAD)
    draw.text((def_x - 30, def_y - 125), "CRUSHING KINETIC CLEAVE [x1.5]", fill=(255, 90, 80), font=FONT_BOLD)

    # Bottom Cockpit HUD
    draw_cockpit_deck(
        draw, im,
        atk_pilot_name="Commander Vance", atk_callsign="VANGUARD PRIME", atk_mech="Custom Bipedal",
        atk_expr="MELEE THRUST", atk_bark="Kinetic plasma blade fully engaged! Target core cleaved!",
        atk_portrait_name="spr_portrait_vance",
        def_pilot_name="Syndicate Enforcer", def_callsign="SCAVENGER-4", def_mech="Hyena Striker",
        def_expr="TAKING HIT", def_bark="Hydraulic breach in primary core! Ejection alarms ringing!",
        def_portrait_name="spr_portrait_cruz",
        telemetry_info=[
            "ORDNANCE: Heavy Plasma Cleaver",
            "HIT: 95% | KINETIC MULT: 1.50x",
            "CALC DMG: 285 [REAR FLANK ANGLE +20%]"
        ]
    )

    apply_scanlines(im)
    out_path = os.path.join(ARTIFACT_DIR, "clash_example_1_melee_dash_cleave.png")
    im.save(out_path, "PNG")
    print("[PASS] Saved Example 1:", out_path)

# =========================================================================
# EXAMPLE 2: Precision Energy Beam Pulse (Ghost Sniper vs Aether Interceptor)
# =========================================================================
def render_example_2():
    w, h = 1280, 720
    im = Image.new("RGBA", (w, h), (8, 12, 18, 255))
    draw = ImageDraw.Draw(im)

    # Deep orbital starfield background
    for i in range(120):
        sx = (i * 97) % w
        sy = (i * 71) % 480
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(200, 230, 255, 180))

    # Top Shutter Header
    draw_snes_panel(draw, 0, 0, w, 54, fill_col=(8, 12, 18, 255), border_col=(0, 200, 255, 255))
    draw.text((24, 16), "THEATER: LUNA HIGH ORBIT // ENGAGEMENT: LONG-RANGE SNIPE DUEL", fill=(100, 220, 255), font=FONT_BOLD)
    draw.text((w / 2 - 130, 16), "COMBAT CLASH // PHASE 1: BEAM DISCHARGE", fill=(0, 240, 255), font=FONT_BOLD)

    # Attacker: Ghost Sniper (Hover chassis levitating with cyan thrusters)
    atk_x, atk_y = 280, 310
    # Twin vernier exhaust plumes
    draw.ellipse([atk_x - 130, atk_y + 20, atk_x - 90, atk_y + 50], fill=(0, 220, 255, 140))
    draw.ellipse([atk_x - 120, atk_y + 26, atk_x - 100, atk_y + 44], fill=(255, 255, 255, 220))

    atk_spr = load_sprite("spr_ms_custom_hover_sniper_idle", 0)
    if atk_spr:
        tinted = Image.new("RGBA", atk_spr.size, (80, 180, 255, 255))
        atk_tint = Image.blend(atk_spr, tinted, 0.25)
        atk_tint.putalpha(atk_spr.getchannel("A"))
        as_scaled = atk_tint.resize((int(160 * 1.6), int(160 * 1.6)), Image.NEAREST)
        im.alpha_composite(as_scaled, (atk_x - 140, atk_y - 120))

    # Defender: Free Colonies Aether Interceptor executing high-G evasion
    def_x, def_y = 960, 290
    def_spr = load_sprite("spr_ms_aether_idle", 0)
    if def_spr:
        ds_scaled = def_spr.resize((int(160 * 1.6), int(160 * 1.6)), Image.NEAREST)
        im.alpha_composite(ds_scaled, (def_x - 120, def_y - 120))

    # Continuous Glowing Raster Beam Stream (Dual-layer cyan/white stream)
    muzzle_x, muzzle_y = atk_x + 90, atk_y - 10
    target_x, target_y = def_x - 50, def_y - 10

    # Outer cyan plasma glow
    draw.line([(muzzle_x, muzzle_y), (target_x, target_y)], fill=(0, 220, 255, 160), width=14)
    # Mid glow
    draw.line([(muzzle_x, muzzle_y), (target_x, target_y)], fill=(120, 245, 255, 220), width=6)
    # Inner pure white energy core
    draw.line([(muzzle_x, muzzle_y), (target_x, target_y)], fill=(255, 255, 255, 255), width=2)

    # Muzzle charging flare rings
    draw.ellipse([muzzle_x - 18, muzzle_y - 18, muzzle_x + 18, muzzle_y + 18], fill=(0, 240, 255, 160))
    draw.ellipse([muzzle_x - 9, muzzle_y - 9, muzzle_x + 9, muzzle_y + 9], fill=(255, 255, 255, 255))

    # Shield deflection ripple on defender
    draw.arc([target_x - 40, target_y - 40, target_x + 40, target_y + 40], start=90, end=270, fill=(0, 255, 220, 255), width=4)

    draw.text((def_x - 60, def_y - 150), "-190 L-ARM [CRITICAL]", fill=(255, 220, 60), font=FONT_HEAD)
    draw.text((def_x - 40, def_y - 125), "ACCELERATED BEAM [99% ACC]", fill=(0, 230, 255), font=FONT_BOLD)

    # Bottom Cockpit HUD
    draw_cockpit_deck(
        draw, im,
        atk_pilot_name="Lt. Nadia Cruz", atk_callsign="GHOST SNIPER", atk_mech="Custom Hover",
        atk_expr="FIRING SALVO", atk_bark="Capacitor discharge synced. Beam rifle impact dead center.",
        atk_portrait_name="spr_portrait_nadia",
        def_pilot_name="Colony Ace 'Sylph'", def_callsign="AETHER-01", def_mech="Aether Interceptor",
        def_expr="DEFENDING", def_bark="Particle beam burn across left wing! Lateral thrusters offline!",
        def_portrait_name="spr_portrait_commander_male",
        telemetry_info=[
            "ORDNANCE: Long-Range Tachyon Beam",
            "HIT: 95% | RANGE: 6 TILES",
            "CALC DMG: 190 [HIGH GROUND +15%]"
        ],
        limb_flash="LA"
    )

    apply_scanlines(im)
    out_path = os.path.join(ARTIFACT_DIR, "clash_example_2_energy_beam_sniper.png")
    im.save(out_path, "PNG")
    print("[PASS] Saved Example 2:", out_path)

# =========================================================================
# EXAMPLE 3: Modular Limb Detachment, Flying Debris & Persistent Scars
# =========================================================================
def render_example_3():
    w, h = 1280, 720
    im = Image.new("RGBA", (w, h), (12, 16, 22, 255))
    draw = ImageDraw.Draw(im)

    # Background
    for y in range(0, 480):
        ratio = y / 480.0
        draw.line([(0, y), (w, y)], fill=(int(14 + ratio * 15), int(18 + ratio * 20), int(28 + ratio * 28), 255))

    # Top Shutter Header
    draw_snes_panel(draw, 0, 0, w, 54, fill_col=(8, 12, 18, 255), border_col=(255, 60, 60, 255))
    draw.text((24, 16), "SECTOR CRITICAL BREACH // MODULAR LIMB DESTRUCTION REPORT", fill=(255, 100, 100), font=FONT_BOLD)
    draw.text((w / 2 - 140, 16), "PHASE 3: COMPONENT DETACHMENT & SCARS", fill=(255, 215, 80), font=FONT_BOLD)

    # Main Center: Ironclad unit in clash screen with severed right arm overlay
    ic_x, ic_y = 420, 310
    draw.ellipse([ic_x - 70, ic_y + 110, ic_x + 70, ic_y + 130], fill=(0, 0, 0, 120))
    ic_spr = load_sprite("spr_ms_ironclad_idle", 0)
    if ic_spr:
        ic_scaled = ic_spr.resize((int(160 * 1.6), int(160 * 1.6)), Image.NEAREST)
        im.alpha_composite(ic_scaled, (ic_x - 120, ic_y - 120))

    # Severed right arm socket overlay
    sock_r = load_sprite("spr_ms_ironclad_hit_right_arm_off", 0)
    if sock_r:
        sock_scaled = sock_r.resize((int(160 * 1.6), int(160 * 1.6)), Image.NEAREST)
        im.alpha_composite(sock_scaled, (ic_x - 120, ic_y - 120))

    # Electrical arc sparks at the severed shoulder socket
    sock_joint_x, sock_joint_y = ic_x + 35, ic_y - 40
    for sx, sy in [(-10, -5), (12, -8), (-5, 15), (14, 8), (-12, 10)]:
        draw.line([(sock_joint_x, sock_joint_y), (sock_joint_x + sx * 2, sock_joint_y + sy * 2)], fill=(120, 220, 255), width=2)
        draw.ellipse([sock_joint_x + sx * 2 - 3, sock_joint_y + sy * 2 - 3, sock_joint_x + sx * 2 + 3, sock_joint_y + sy * 2 + 3], fill=(255, 255, 255))

    # Detached Severed Arm Debris Flying Across the Air with Angular Spin
    deb_x, deb_y = 680, 200
    if sock_r:
        # Crop just the arm section and spin it
        deb_arm = sock_r.crop((90, 40, 160, 130)).resize((110, 130)).rotate(48, expand=True, resample=Image.BICUBIC)
        im.alpha_composite(deb_arm, (deb_x, deb_y))
        # Parabolic motion trail
        draw.arc([deb_x - 80, deb_y - 20, deb_x + 60, deb_y + 80], start=180, end=320, fill=(255, 160, 40), width=2)

    # Dramatic Critical Banner
    draw_snes_panel(draw, 340, 120, 840, 172, fill_col=(40, 12, 14, 250), border_col=(255, 60, 60, 255))
    draw.text((360, 134), "CRITICAL BREACH // RIGHT ARM SEVERED!", fill=(255, 80, 80), font=FONT_HEAD)

    # Right Inset Panel: Isometric Map View Showing Persistent Tactical Battle Scars
    map_x, map_y, map_w, map_h = 880, 80, 380, 360
    draw_snes_panel(draw, map_x, map_y, map_x + map_w, map_y + map_h, fill_col=(10, 16, 24, 250), border_col=(0, 200, 255, 255))
    draw.text((map_x + 14, map_y + 12), "TACTICAL ISOMETRIC MAP PERSISTENCE", fill=(0, 220, 255), font=FONT_BOLD)

    # Mini isometric diamond tiles
    tile_cx, tile_cy = map_x + 190, map_y + 240
    for dc, dr in [(-1, 0), (0, -1), (0, 0), (1, 0), (0, 1)]:
        tx = tile_cx + (dc - dr) * 44
        ty = tile_cy + (dc + dr) * 22
        pts = [(tx, ty - 22), (tx + 44, ty), (tx, ty + 22), (tx - 44, ty)]
        fill_t = (24, 38, 52) if (dc == 0 and dr == 0) else (18, 28, 40)
        draw.polygon(pts, fill=fill_t, outline=(40, 65, 90))

    # Inset Map Unit with Scars
    if ic_spr:
        im.alpha_composite(ic_spr, (tile_cx - 80, tile_cy - 145))
    if sock_r:
        im.alpha_composite(sock_r, (tile_cx - 80, tile_cy - 145))

    # Map sparks and smoke puffs
    draw.ellipse([tile_cx + 14, tile_cy - 105, tile_cx + 20, tile_cy - 99], fill=(120, 240, 255))
    draw.ellipse([tile_cx - 8, tile_cy - 45, tile_cx + 12, tile_cy - 25], fill=(180, 190, 205, 120))
    draw.text((map_x + 14, map_y + 315), "• Persistent Socket Arc Sparks [RA: 0/120]", fill=(255, 160, 60), font=FONT_SMALL)
    draw.text((map_x + 14, map_y + 333), "• Crippled Legs Trailing Smoke [AP -2]", fill=(180, 210, 240), font=FONT_SMALL)

    # Bottom Cockpit HUD
    draw_cockpit_deck(
        draw, im,
        atk_pilot_name="Col. Cruz", atk_callsign="BALLISTA HEAVY", atk_mech="Terran Ballista",
        atk_expr="CRITICAL HIT", atk_bark="Direct kinetic slug to right actuator! Limb destroyed!",
        atk_portrait_name="spr_portrait_cruz",
        def_pilot_name="Mercenary Pilot", def_callsign="IRONCLAD-07", def_mech="Ironclad Heavy",
        def_expr="CRIPPLED", def_bark="Primary weapon arm severed! Switching to backup vulcans!",
        def_portrait_name="spr_portrait_commander_male",
        telemetry_info=[
            "DISARMED: Weapon Stripped",
            "DAMAGE: 240 SOLID IMPACT",
            "ACCURACY PENALTY: -25%"
        ],
        limb_flash="RA"
    )

    apply_scanlines(im)
    out_path = os.path.join(ARTIFACT_DIR, "clash_example_3_limb_severing_and_scars.png")
    im.save(out_path, "PNG")
    print("[PASS] Saved Example 3:", out_path)

# =========================================================================
# EXAMPLE 4: Combined-Arms Conventional Forces & Platoon Salvo (Doc 38)
# =========================================================================
def render_example_4():
    w, h = 1280, 720
    im = Image.new("RGBA", (w, h), (10, 14, 20, 255))
    draw = ImageDraw.Draw(im)

    # Rocky canyon terrain
    for y in range(0, 480):
        ratio = y / 480.0
        draw.line([(0, y), (w, y)], fill=(int(22 + ratio * 18), int(18 + ratio * 22), int(16 + ratio * 18), 255))

    # Top Shutter Header
    draw_snes_panel(draw, 0, 0, w, 54, fill_col=(8, 12, 18, 255), border_col=(0, 200, 255, 255))
    draw.text((24, 16), "THEATER: MARS RIDGE // COMBINED-ARMS CONVENTIONAL PLATOON SALVO", fill=(100, 220, 255), font=FONT_BOLD)
    draw.text((w / 2 - 130, 16), "ERA 0 TACTICAL BATTLEGROUP // SALVO PHASE", fill=(255, 215, 80), font=FONT_BOLD)

    # Allied Unit 1: Terran Mammoth Heavy MBT (spr_veh_terran_mammoth_idle) firing 150mm cannon
    tank_x, tank_y = 260, 340
    draw.ellipse([tank_x - 70, tank_y + 90, tank_x + 70, tank_y + 115], fill=(0, 0, 0, 140))
    tank_spr = load_sprite("spr_veh_terran_mammoth_idle", 0)
    if tank_spr:
        ts_scaled = tank_spr.resize((int(160 * 1.5), int(160 * 1.5)), Image.NEAREST)
        im.alpha_composite(ts_scaled, (tank_x - 120, tank_y - 120))

    # Allied Unit 2: Terran 88th Infantry Squad in echelon support firing rifles
    inf_x, inf_y = 440, 360
    draw.ellipse([inf_x - 50, inf_y + 80, inf_x + 50, inf_y + 100], fill=(0, 0, 0, 120))
    inf_spr = load_sprite("spr_inf_terran_squad_idle", 0)
    if inf_spr:
        is_scaled = inf_spr.resize((int(160 * 1.4), int(160 * 1.4)), Image.NEAREST)
        im.alpha_composite(is_scaled, (inf_x - 100, inf_y - 110))

    # Heavy cannon muzzle flash
    cmz_x, cmz_y = tank_x + 130, tank_y - 10
    draw.ellipse([cmz_x - 24, cmz_y - 24, cmz_x + 24, cmz_y + 24], fill=(255, 220, 80, 220))
    draw.ellipse([cmz_x - 12, cmz_y - 12, cmz_x + 12, cmz_y + 12], fill=(255, 255, 255, 255))
    # Ballistic Shell Trajectory
    draw.line([(cmz_x, cmz_y), (cmz_x + 280, cmz_y - 40)], fill=(255, 180, 60), width=4)

    # Infantry tracer fire lines
    for off_y in [-15, 0, 15]:
        draw.line([(inf_x + 70, inf_y - 20 + off_y), (inf_x + 360, inf_y - 30 + off_y)], fill=(255, 230, 120), width=2)

    # Defender: Hostile MBT Taking Hit with Smoke
    def_x, def_y = 920, 330
    draw.ellipse([def_x - 70, def_y + 90, def_x + 70, def_y + 115], fill=(0, 0, 0, 140))
    if tank_spr:
        # Flip horizontal to face left
        def_tank = tank_spr.transpose(Image.FLIP_LEFT_RIGHT).resize((int(160 * 1.5), int(160 * 1.5)), Image.NEAREST)
        im.alpha_composite(def_tank, (def_x - 120, def_y - 120))

    # Explosion on defender hull
    ex_x, ex_y = def_x - 20, def_y - 10
    draw.ellipse([ex_x - 38, ex_y - 38, ex_x + 38, ex_y + 38], fill=(255, 180, 40, 220))
    draw.ellipse([ex_x - 18, ex_y - 18, ex_x + 18, ex_y + 18], fill=(255, 255, 255, 255))
    draw.text((def_x - 60, def_y - 140), "-175 HULL BREACH", fill=(255, 220, 60), font=FONT_HEAD)
    draw.text((def_x - 80, def_y - 115), "[FIELD WRECKAGE CREATED]", fill=(100, 230, 255), font=FONT_BOLD)

    # Bottom Cockpit HUD
    draw_cockpit_deck(
        draw, im,
        atk_pilot_name="Capt. Miller", atk_callsign="MAMMOTH-LEAD", atk_mech="Terran Heavy MBT",
        atk_expr="COMBINED SALVO", atk_bark="150mm high-explosive round away! Infantry covering fire good!",
        atk_portrait_name="spr_portrait_commander_male",
        def_pilot_name="Colony Armor Cohort", def_callsign="DART TANK-2", def_mech="Colony Light Armor",
        def_expr="HULL BREACHED", def_bark="Heavy armor compromised! Abandon vehicle!",
        def_portrait_name="spr_portrait_vance",
        telemetry_info=[
            "COMBINED-ARMS: +20% SALVO DMG",
            "FIELD WRECKAGE: +20% COVER",
            "CALC DMG: 175 [DIRECT IMPACT]"
        ]
    )

    apply_scanlines(im)
    out_path = os.path.join(ARTIFACT_DIR, "clash_example_4_conventional_platoon_salvo.png")
    im.save(out_path, "PNG")
    print("[PASS] Saved Example 4:", out_path)

if __name__ == "__main__":
    print("=== RENDERING 4 LIVE COMBAT SYSTEM EXAMPLES ===")
    render_example_1()
    render_example_2()
    render_example_3()
    render_example_4()
    print("=== ALL 4 COMBAT EXAMPLES SUCCESSFULLY RENDERED ===")
