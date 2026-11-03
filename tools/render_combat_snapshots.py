import os
import json
import math
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = "/home/tom/.gemini/antigravity-ide/brain/a9197ef4-c206-4eb1-b4b4-83dfffe898d6"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

FONT_REG = ImageFont.truetype("/usr/share/fonts/google-noto/NotoSansMono-Regular.ttf", 13)
FONT_BOLD = ImageFont.truetype("/usr/share/fonts/google-noto/NotoSansMono-CondensedBold.ttf", 15)
FONT_TITLE = ImageFont.truetype("/usr/share/fonts/google-noto/NotoSansMono-CondensedBold.ttf", 17)
FONT_SMALL = ImageFont.truetype("/usr/share/fonts/google-noto/NotoSansMono-Regular.ttf", 11)
FONT_LARGE = ImageFont.truetype("/usr/share/fonts/google-noto/NotoSansMono-CondensedBold.ttf", 20)

def load_first_sprite_frame(sprite_name):
    spr_path = os.path.join("sprites", sprite_name)
    if not os.path.exists(spr_path):
        return None
    pngs = [f for f in os.listdir(spr_path) if f.endswith(".png")]
    if not pngs:
        return None
    # Pick first frame
    return Image.open(os.path.join(spr_path, pngs[0])).convert("RGBA")

def load_sprite_frame(sprite_name, frame_idx=0):
    spr_path = os.path.join("sprites", sprite_name)
    if not os.path.exists(spr_path):
        return None
    pngs = sorted([f for f in os.listdir(spr_path) if f.endswith(".png")])
    if not pngs:
        return None
    f_name = pngs[frame_idx % len(pngs)]
    return Image.open(os.path.join(spr_path, f_name)).convert("RGBA")

def iso_x(col, row, elev, cam_x=420, zoom=1.0):
    return int(((col - row) * 32.0) * zoom + cam_x)

def iso_y(col, row, elev, cam_y=230, zoom=1.0):
    return int((((col + row) * 16.0) - (elev * 16.0)) * zoom + cam_y)

def draw_snes_panel(draw, x1, y1, x2, y2, bg_col=(18, 24, 32, 235), border_col=(60, 110, 160, 255)):
    draw.rectangle([x1, y1, x2, y2], fill=bg_col, outline=border_col, width=2)
    # Corner rivets / bevel
    draw.line([(x1 + 2, y1 + 2), (x2 - 2, y1 + 2)], fill=(90, 150, 210, 255), width=1)
    draw.line([(x1 + 2, y1 + 2), (x1 + 2, y2 - 2)], fill=(90, 150, 210, 255), width=1)
    draw.line([(x2 - 2, y1 + 2), (x2 - 2, y2 - 2)], fill=(25, 45, 70, 255), width=1)
    draw.line([(x1 + 2, y2 - 2), (x2 - 2, y2 - 2)], fill=(25, 45, 70, 255), width=1)

def render_isometric_grid(draw, cam_x=420, cam_y=230, zoom=1.0, highlight_tiles=None):
    if highlight_tiles is None:
        highlight_tiles = {}

    # 14x14 grid
    for r in range(14):
        for c in range(14):
            elev = 0
            # Elevation stepped plateau in back
            if 8 <= c <= 12 and 1 <= r <= 4:
                elev = 1

            p0 = (iso_x(c, r, elev, cam_x, zoom), iso_y(c, r, elev, cam_y, zoom))
            p1 = (iso_x(c + 1, r, elev, cam_x, zoom), iso_y(c + 1, r, elev, cam_y, zoom))
            p2 = (iso_x(c + 1, r + 1, elev, cam_x, zoom), iso_y(c + 1, r + 1, elev, cam_y, zoom))
            p3 = (iso_x(c, r + 1, elev, cam_x, zoom), iso_y(c, r + 1, elev, cam_y, zoom))

            # Base tile color
            t_col = (42, 48, 44, 255) if (c + r) % 2 == 0 else (36, 42, 38, 255)
            b_col = (26, 32, 28, 255)

            if elev == 1:
                t_col = (54, 62, 56, 255) if (c + r) % 2 == 0 else (48, 56, 50, 255)
                b_col = (38, 46, 40, 255)

            # Highlight check
            if (c, r) in highlight_tiles:
                t_col = highlight_tiles[(c, r)]

            # Draw diamond
            draw.polygon([p0, p1, p2, p3], fill=t_col, outline=b_col)

            # Elevation wall sides if elev > 0
            if elev > 0:
                p0_b = (iso_x(c, r, 0, cam_x, zoom), iso_y(c, r, 0, cam_y, zoom))
                p1_b = (iso_x(c + 1, r, 0, cam_x, zoom), iso_y(c + 1, r, 0, cam_y, zoom))
                p2_b = (iso_x(c + 1, r + 1, 0, cam_x, zoom), iso_y(c + 1, r + 1, 0, cam_y, zoom))
                p3_b = (iso_x(c, r + 1, 0, cam_x, zoom), iso_y(c, r + 1, 0, cam_y, zoom))
                # Right cliff wall
                draw.polygon([p1, p2, p2_b, p1_b], fill=(28, 34, 30, 255), outline=(15, 18, 16, 255))
                # Left cliff wall
                draw.polygon([p3, p2, p2_b, p3_b], fill=(22, 28, 24, 255), outline=(15, 18, 16, 255))

def paste_unit(canvas, spr, col, row, elev, cam_x=420, cam_y=230, zoom=1.0, y_offset=0):
    if spr is None:
        return
    # Tile center: (col + 0.5, row + 0.5)
    gx = iso_x(col + 0.5, row + 0.5, elev, cam_x, zoom)
    gy = iso_y(col + 0.5, row + 0.5, elev, cam_y, zoom)
    # Origin is at (80, 145)
    draw_x = gx - 80
    draw_y = gy - 145 + y_offset
    canvas.alpha_composite(spr, (draw_x, draw_y))

def render_top_hud(draw):
    draw_snes_panel(draw, 0, 0, 1366, 82, bg_col=(14, 20, 28, 245), border_col=(50, 95, 140, 255))
    draw.text((18, 8), "TACTICAL COMBAT // SECTOR 4 MINING CLAIM", fill=(100, 215, 255), font=FONT_TITLE)
    draw.text((18, 28), "OBJECTIVE: Repel Syndicate Strike Battlegroup | Era: ERA 0 [DAWN OF THE MOBILE SUIT]", fill=(170, 195, 220), font=FONT_REG)
    draw.text((18, 48), "STATUS: [PLAYER PHASE] | TURN: 1 | ALLIED COMBINED-ARMS (1 MOBILE SUIT PROTOTYPE, 3 CONVENTIONAL ESCORTS)", fill=(80, 240, 130), font=FONT_REG)
    draw.text((18, 64), "[WASD/Drag] Pan | [Wheel] Zoom: 100% | [TAB] Cycle Units | [F] Rotate Perspective | [Z] Aimed Shot Precision", fill=(130, 160, 190), font=FONT_SMALL)

    # Mini Unit Timeline Roster on top right
    units_info = [
        ("Alpha-01", True), ("Mammoth-1", True), ("Skyhammer-2", True), ("Terran 88th", True),
        ("Mammoth-3", False), ("Guerrilla-1", False), ("Valkyrie-2", False), ("Kurogane-4", False)
    ]
    rx = 760
    for name, is_ally in units_info:
        bg = (30, 70, 110, 255) if is_ally else (110, 40, 40, 255)
        border = (60, 140, 220, 255) if is_ally else (220, 70, 70, 255)
        draw.rectangle([rx, 14, rx + 68, 48], fill=bg, outline=border, width=2)
        draw.text((rx + 4, 18), name[:8], fill=(255, 255, 255), font=FONT_SMALL)
        draw.text((rx + 4, 32), "ALLIED" if is_ally else "HOSTILE", fill=(120, 220, 255) if is_ally else (255, 140, 140), font=FONT_SMALL)
        rx += 74

def render_bottom_action_bar(draw, selected_unit="Alpha-01 'WARHAMMER' [PROTOTYPE]"):
    # Bottom Left Command Action Bar
    draw_snes_panel(draw, 16, 595, 915, 755, bg_col=(14, 20, 28, 245), border_col=(50, 95, 140, 255))
    draw.text((26, 602), f"ACTIVE UNIT: {selected_unit} // PILOT: COMMANDER VANCE", fill=(100, 220, 255), font=FONT_BOLD)
    draw.text((26, 620), "AP: [■■■■■■] 6/6 | HEAT: [0.0 / 100.0] DISSIPATION: 35.0/TURN | CHASSIS INTEGRITY: 100%", fill=(220, 220, 220), font=FONT_REG)

    # Action Buttons
    btns = [
        ("[M] MANEUVER", "Cost: 1-4 AP\nRange: 5 Tiles"),
        ("[1] 120MM CANNON", "AP: 3 | Heat: +15\nDmg: 165 (Kinetic)"),
        ("[2] GAU-88 VULCAN", "AP: 2 | Heat: +10\nDmg: 85 (Rotary)"),
        ("[3] SWARM-16", "AP: 4 | Heat: +22\nDmg: 195 (Missile)"),
        ("[4] MELEE STOMP", "AP: 3 | Heat: +8\nDmg: 210 (Hydraulic)"),
        ("[E] END TURN", "Yield Initiative\nDissipate Heat")
    ]
    bx = 26
    for title, desc in btns:
        draw.rectangle([bx, 642, bx + 138, 744], fill=(24, 36, 48, 255), outline=(70, 120, 180, 255), width=2)
        draw.text((bx + 8, 648), title, fill=(255, 230, 80), font=FONT_BOLD)
        lines = desc.split("\n")
        draw.text((bx + 8, 672), lines[0], fill=(180, 210, 240), font=FONT_SMALL)
        draw.text((bx + 8, 688), lines[1], fill=(140, 180, 210), font=FONT_SMALL)
        bx += 146

def render_combat_terminal(draw, lines):
    # Bottom Right Live Terminal Feed
    draw_snes_panel(draw, 930, 595, 1350, 755, bg_col=(10, 14, 18, 250), border_col=(40, 75, 105, 255))
    draw.text((942, 602), "TACTICAL TELEMETRY // COMBAT FEED", fill=(80, 220, 120), font=FONT_BOLD)
    ty = 624
    for line in lines[-7:]:
        col = (200, 225, 210)
        if "PROMETHEUS" in line or "MOBILE SUIT" in line:
            col = (100, 230, 255)
        elif "HIT" in line or "SALVO" in line or "FIRING" in line:
            col = (255, 220, 80)
        elif "BREACH" in line or "DETONATION" in line or "CASUALTY" in line or "OVERRUN" in line:
            col = (255, 100, 80)
        elif "WARNING" in line:
            col = (255, 180, 40)
        draw.text((942, ty), line[:52], fill=col, font=FONT_SMALL)
        ty += 18

print("Helper definitions complete.")

# =============================================================================
# SNAPSHOT 1: ISOMETRIC THEATER OVERVIEW (ERA 0 CONVENTIONAL FORCES DEPLOYMENT)
# =============================================================================
def generate_snapshot_1():
    print("Generating Snapshot 1: Tactical Isometric Battlefield Overview...")
    im = Image.new("RGBA", (1366, 768), (14, 18, 24, 255))
    draw = ImageDraw.Draw(im)

    # Distant space stars & atmospheric haze
    for sx, sy in [(120, 110), (340, 140), (580, 120), (840, 105), (1120, 130), (220, 95), (960, 115)]:
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(220, 240, 255, 180))

    # Render 14x14 isometric grid
    render_isometric_grid(draw, cam_x=440, cam_y=210, zoom=1.0)

    # Load actual engine sprites
    spr_ironclad = load_sprite_frame("spr_ms_ironclad_idle", 0)
    spr_mammoth_ally = load_sprite_frame("spr_veh_terran_mammoth_idle", 0)
    spr_skyhammer = load_sprite_frame("spr_veh_terran_skyhammer_idle", 1)
    spr_terran_inf = load_sprite_frame("spr_inf_terran_squad_idle", 0)

    spr_mammoth_hostile = load_sprite_frame("spr_veh_terran_mammoth_idle", 0)
    spr_syndicate_inf = load_sprite_frame("spr_inf_syndicate_squad_idle", 0)
    spr_valkyrie = load_sprite_frame("spr_veh_colony_gunship_idle", 2)
    spr_kurogane = load_sprite_frame("spr_veh_zaibatsu_kurogane_idle", 0)

    # Unit positions (col, row, elev, y_offset)
    # Allied units
    paste_unit(im, spr_ironclad, 3, 5, 0, cam_x=440, cam_y=210)
    paste_unit(im, spr_mammoth_ally, 2, 7, 0, cam_x=440, cam_y=210)
    paste_unit(im, spr_skyhammer, 1, 4, 0, cam_x=440, cam_y=210, y_offset=-20) # elevated flight!
    paste_unit(im, spr_terran_inf, 4, 4, 0, cam_x=440, cam_y=210)

    # Hostile units
    paste_unit(im, spr_mammoth_hostile, 7, 6, 0, cam_x=440, cam_y=210)
    paste_unit(im, spr_syndicate_inf, 8, 4, 0, cam_x=440, cam_y=210)
    paste_unit(im, spr_valkyrie, 9, 7, 0, cam_x=440, cam_y=210, y_offset=-22) # elevated helicopter flight!
    paste_unit(im, spr_kurogane, 6, 8, 0, cam_x=440, cam_y=210)

    # Tactical callout badges over key units
    # Ironclad badge
    ic_gx = iso_x(3.5, 5.5, 0, 440)
    ic_gy = iso_y(3.5, 5.5, 0, 210) - 150
    draw.rectangle([ic_gx - 75, ic_gy - 16, ic_gx + 75, ic_gy + 4], fill=(15, 30, 45, 230), outline=(80, 220, 255), width=2)
    draw.text((ic_gx - 70, ic_gy - 14), "★ Alpha-01 'WARHAMMER'", fill=(100, 230, 255), font=FONT_SMALL)

    # Terran Infantry badge
    inf_gx = iso_x(4.5, 4.5, 0, 440)
    inf_gy = iso_y(4.5, 4.5, 0, 210) - 95
    draw.rectangle([inf_gx - 55, inf_gy - 16, inf_gx + 55, inf_gy + 4], fill=(15, 35, 25, 230), outline=(90, 200, 110), width=1)
    draw.text((inf_gx - 50, inf_gy - 14), "Terran 88th Squad", fill=(130, 240, 150), font=FONT_SMALL)

    # Hostile Mammoth badge
    hm_gx = iso_x(7.5, 6.5, 0, 440)
    hm_gy = iso_y(7.5, 6.5, 0, 210) - 110
    draw.rectangle([hm_gx - 60, hm_gy - 16, hm_gx + 60, hm_gy + 4], fill=(45, 20, 20, 230), outline=(240, 80, 80), width=1)
    draw.text((hm_gx - 55, hm_gy - 14), "Hostile MBT Mammoth-3", fill=(255, 140, 140), font=FONT_SMALL)

    # Render HUD
    render_top_hud(draw)
    render_bottom_action_bar(draw, "Alpha-01 'WARHAMMER' [PROTOTYPE]")
    render_combat_terminal(draw, [
        "ERA 0 COMBINED-ARMS THEATER // SECTOR 4 MINING DEPOSIT",
        "Project Prometheus Sortie: 1 Walking Mobile Suit Prototype deployed.",
        "Escort Elements: 1 Heavy MBT, 1 CAS Strike Jet, 1 Mechanized Infantry Squad.",
        "Hostile Intelligence: Conventional armor platoons, atmospheric air wings, and entrenched infantry detected.",
        ">> THEATER ESCALATION: Dawn of the Mobile Suit (Era 0)",
        ">> TACTICAL COMMAND: WASD/Drag to Pan, Wheel to Zoom, TAB to cycle units, [F] to rotate perspective!"
    ])

    out_path = os.path.join(ARTIFACT_DIR, "snapshot_01_isometric_theater_overview.png")
    im.save(out_path, "PNG")
    print(f"Saved: {out_path}")

# =============================================================================
# SNAPSHOT 2: TARGETED AIMING & FRONT MISSION COMPONENT DUEL LOCK
# =============================================================================
def generate_snapshot_2():
    print("Generating Snapshot 2: Front Mission Targeted Aiming & Component Duel Lock...")
    im = Image.new("RGBA", (1366, 768), (14, 18, 24, 255))
    draw = ImageDraw.Draw(im)

    # Highlight attack range tiles in subtle translucent red
    atk_tiles = {}
    for c in range(2, 9):
        for r in range(3, 9):
            if 1 <= abs(c - 3) + abs(r - 5) <= 6:
                atk_tiles[(c, r)] = (55, 38, 42, 255) if (c + r) % 2 == 0 else (48, 32, 36, 255)

    render_isometric_grid(draw, cam_x=440, cam_y=210, zoom=1.0, highlight_tiles=atk_tiles)

    spr_ironclad = load_sprite_frame("spr_ms_ironclad_idle", 0)
    spr_mammoth_ally = load_sprite_frame("spr_veh_terran_mammoth_idle", 0)
    spr_skyhammer = load_sprite_frame("spr_veh_terran_skyhammer_idle", 1)
    spr_terran_inf = load_sprite_frame("spr_inf_terran_squad_idle", 0)

    spr_mammoth_hostile = load_sprite_frame("spr_veh_terran_mammoth_idle", 0)
    spr_syndicate_inf = load_sprite_frame("spr_inf_syndicate_squad_idle", 0)
    spr_valkyrie = load_sprite_frame("spr_veh_colony_gunship_idle", 2)
    spr_kurogane = load_sprite_frame("spr_veh_zaibatsu_kurogane_idle", 0)

    # Paste Units
    paste_unit(im, spr_ironclad, 3, 5, 0, cam_x=440, cam_y=210)
    paste_unit(im, spr_mammoth_ally, 2, 7, 0, cam_x=440, cam_y=210)
    paste_unit(im, spr_skyhammer, 1, 4, 0, cam_x=440, cam_y=210, y_offset=-20)
    paste_unit(im, spr_terran_inf, 4, 4, 0, cam_x=440, cam_y=210)

    paste_unit(im, spr_mammoth_hostile, 7, 6, 0, cam_x=440, cam_y=210)
    paste_unit(im, spr_syndicate_inf, 8, 4, 0, cam_x=440, cam_y=210)
    paste_unit(im, spr_valkyrie, 9, 7, 0, cam_x=440, cam_y=210, y_offset=-22)
    paste_unit(im, spr_kurogane, 6, 8, 0, cam_x=440, cam_y=210)

    # DOTTED BALLISTIC TRAJECTORY LINE from Ironclad to Hostile Mammoth
    p_from_x = iso_x(3.5, 5.5, 0, 440)
    p_from_y = iso_y(3.5, 5.5, 0, 210) - 70
    p_to_x = iso_x(7.5, 6.5, 0, 440)
    p_to_y = iso_y(7.5, 6.5, 0, 210) - 40

    # Draw arc trajectory
    steps = 20
    for s in range(steps):
        t = s / float(steps)
        arc_x = int(p_from_x + t * (p_to_x - p_from_x))
        arc_y = int(p_from_y + t * (p_to_y - p_from_y) - (35 * math.sin(math.pi * t)))
        if s % 2 == 0:
            draw.ellipse([arc_x - 3, arc_y - 3, arc_x + 3, arc_y + 3], fill=(255, 230, 80, 240))

    # Pulsing Isometric Targeting Reticle on Hostile Mammoth tile
    tg_x = iso_x(7.5, 6.5, 0, 440)
    tg_y = iso_y(7.5, 6.5, 0, 210)
    draw.ellipse([tg_x - 36, tg_y - 18, tg_x + 36, tg_y + 18], outline=(255, 60, 40, 240), width=2)
    draw.ellipse([tg_x - 18, tg_y - 9, tg_x + 18, tg_y + 9], outline=(255, 220, 60, 240), width=1)
    # Crosshair tick marks
    draw.line([(tg_x - 44, tg_y), (tg_x - 36, tg_y)], fill=(255, 60, 40), width=2)
    draw.line([(tg_x + 36, tg_y), (tg_x + 44, tg_y)], fill=(255, 60, 40), width=2)
    draw.line([(tg_x, tg_y - 24), (tg_x, tg_y - 18)], fill=(255, 60, 40), width=2)
    draw.line([(tg_x, tg_y + 18), (tg_x, tg_y + 24)], fill=(255, 60, 40), width=2)

    # RIGHT PANEL: FRONT MISSION TARGET DUEL & DIAGNOSTICS (x: 930 to 1350, y: 92 to 585)
    draw_snes_panel(draw, 930, 92, 1350, 585, bg_col=(14, 20, 28, 248), border_col=(220, 70, 70, 255))
    draw.text((945, 102), "TARGET DUEL // COMPONENT LOCK", fill=(255, 90, 80), font=FONT_TITLE)
    draw.text((945, 124), "TARGET: Hostile MBT 'MAMMOTH-3' [T-720]", fill=(240, 240, 240), font=FONT_BOLD)
    draw.text((945, 142), "CHASSIS: Conventional Heavy Armor | Distance: 5 Tiles", fill=(170, 190, 210), font=FONT_SMALL)

    # Aimed Shot Precision Lock Banner
    draw.rectangle([945, 164, 1335, 192], fill=(45, 25, 20, 255), outline=(255, 160, 40, 255), width=2)
    draw.text((955, 170), "★ AIMED SHOT LOCK: ARMORED HULL (-15% ACCURACY)", fill=(255, 210, 60), font=FONT_BOLD)

    # Front Mission Component Diagnostic Table
    parts = [
        ("TORSO", "Armored Hull", 520, 520, 36, 68, True),
        ("HEAD", "Turret / Optics", 240, 240, 28, 44, False),
        ("ARM_L", "Port Mount", 182, 182, 21, 55, False),
        ("ARM_R", "Starboard Mount", 182, 182, 21, 55, False),
        ("LEGS", "Caterpillar Treads", 480, 480, 21, 76, False)
    ]
    py = 205
    for p_id, p_name, hp, max_hp, arm, hit, is_locked in parts:
        bg_p = (45, 40, 25, 255) if is_locked else (20, 26, 34, 255)
        brd_p = (255, 200, 50, 255) if is_locked else (45, 65, 90, 255)
        draw.rectangle([945, py, 1335, py + 52], fill=bg_p, outline=brd_p, width=2 if is_locked else 1)

        lock_tag = "[DESIGNATED LOCK]" if is_locked else ""
        draw.text((955, py + 6), f"[{p_id}] {p_name} {lock_tag}", fill=(255, 230, 80) if is_locked else (210, 230, 250), font=FONT_BOLD)
        draw.text((955, py + 24), f"HP: {hp}/{max_hp} | Armor: {arm} | Hit Chance: {hit}%", fill=(170, 200, 220), font=FONT_SMALL)

        # Health bar
        draw.rectangle([1180, py + 26, 1320, py + 38], fill=(30, 30, 30, 255), outline=(60, 60, 60, 255))
        pct = hp / float(max_hp)
        draw.rectangle([1182, py + 28, 1182 + int(136 * pct), py + 36], fill=(80, 220, 120, 255))
        py += 60

    # Weapon in use box
    draw.rectangle([945, 515, 1335, 575], fill=(22, 32, 44, 255), outline=(80, 140, 210, 255), width=2)
    draw.text((955, 522), "SELECTED WEAPON: Type-77 120mm Cannon", fill=(100, 220, 255), font=FONT_BOLD)
    draw.text((955, 540), "AP Cost: 3 | Heat: +15 | Damage: 165 (Kinetic Solid-Slug)", fill=(240, 240, 240), font=FONT_SMALL)
    draw.text((955, 555), "CLICK TARGET TILE OR ENEMY TO EXECUTE FIRING SALVO!", fill=(255, 220, 60), font=FONT_SMALL)

    render_top_hud(draw)
    render_bottom_action_bar(draw, "Alpha-01 'WARHAMMER' [PROTOTYPE] -> TARGETING")
    render_combat_terminal(draw, [
        "ERA 0 COMBINED-ARMS THEATER // SECTOR 4 MINING DEPOSIT",
        "Project Prometheus Sortie: 1 Walking Mobile Suit Prototype deployed.",
        "[TARGET ACQUIRED] Hostile MBT 'MAMMOTH-3' in weapon envelope.",
        "[AIMED SHOT LOCK] Designated component -> ARMORED HULL.",
        "[BALLISTIC CALC] Hit probability: 68% (Distance: 5 tiles, Elevation: 0)."
    ])

    out_path = os.path.join(ARTIFACT_DIR, "snapshot_02_targeted_aiming_and_duel_lock.png")
    im.save(out_path, "PNG")
    print(f"Saved: {out_path}")

# =============================================================================
# SNAPSHOT 3: COMBAT SALVO RESOLUTION & ADVANCE WARS STYLE DEFEAT
# =============================================================================
def generate_snapshot_3():
    print("Generating Snapshot 3: Combat Salvo Resolution & Advance Wars Defeat...")
    # Slight screen shake offset!
    im = Image.new("RGBA", (1366, 768), (16, 20, 26, 255))
    draw = ImageDraw.Draw(im)

    render_isometric_grid(draw, cam_x=443, cam_y=208, zoom=1.0)

    # Load active combat frames
    spr_ironclad = load_sprite_frame("spr_ms_ironclad_idle", 0)
    spr_mammoth_ally_fire = load_sprite_frame("spr_veh_terran_mammoth_fire", 1) # firing dual cannon blast!
    spr_skyhammer = load_sprite_frame("spr_veh_terran_skyhammer_idle", 2)
    spr_terran_inf = load_sprite_frame("spr_inf_terran_squad_fire", 1) # bazooka backblast!

    spr_mammoth_hostile = load_sprite_frame("spr_veh_wreckage_tank", 1) # burning wreckage!
    spr_syndicate_inf_defeat = load_sprite_frame("spr_inf_syndicate_squad_defeat", 1) # Advance Wars tumbling in air!
    spr_valkyrie = load_sprite_frame("spr_veh_colony_gunship_idle", 3)
    spr_kurogane = load_sprite_frame("spr_veh_zaibatsu_kurogane_idle", 1)

    # Paste Units
    paste_unit(im, spr_ironclad, 3, 5, 0, cam_x=443, cam_y=208)
    paste_unit(im, spr_mammoth_ally_fire, 2, 7, 0, cam_x=443, cam_y=208)
    paste_unit(im, spr_skyhammer, 1, 4, 0, cam_x=443, cam_y=208, y_offset=-20)
    paste_unit(im, spr_terran_inf, 4, 4, 0, cam_x=443, cam_y=208)

    paste_unit(im, spr_mammoth_hostile, 7, 6, 0, cam_x=443, cam_y=208)
    paste_unit(im, spr_syndicate_inf_defeat, 8, 4, 0, cam_x=443, cam_y=208)
    paste_unit(im, spr_valkyrie, 9, 7, 0, cam_x=443, cam_y=208, y_offset=-22)
    paste_unit(im, spr_kurogane, 6, 8, 0, cam_x=443, cam_y=208)

    # IN-FLIGHT PHYSICAL PROJECTILE TRACERS (from Allied line to Hostile line)
    p_sx = iso_x(3.5, 5.5, 0, 443)
    p_sy = iso_y(3.5, 5.5, 0, 208) - 70
    p_tx = iso_x(7.5, 6.5, 0, 443)
    p_ty = iso_y(7.5, 6.5, 0, 208) - 40

    # Draw streak tracer
    mid_x = int(p_sx * 0.3 + p_tx * 0.7)
    mid_y = int(p_sy * 0.3 + p_ty * 0.7)
    draw.line([(mid_x - 18, mid_y - 6), (mid_x + 18, mid_y + 6)], fill=(255, 230, 80, 255), width=3)
    draw.line([(mid_x - 30, mid_y - 10), (mid_x - 18, mid_y - 6)], fill=(255, 120, 30, 200), width=2)

    # EXPLOSION FX ON HOSTILE TANK
    ex_x = iso_x(7.5, 6.5, 0, 443)
    ex_y = iso_y(7.5, 6.5, 0, 208) - 50
    # Blast core
    draw.ellipse([ex_x - 32, ex_y - 32, ex_x + 32, ex_y + 32], fill=(255, 180, 40, 220))
    draw.ellipse([ex_x - 18, ex_y - 18, ex_x + 18, ex_y + 18], fill=(255, 255, 220, 255))
    # Shockwave ring
    draw.ellipse([ex_x - 48, ex_y - 38, ex_x + 48, ex_y + 38], outline=(255, 255, 255, 200), width=2)

    # FLOATING COMBAT DAMAGE TEXTS
    # 1. Tank Kill Callouts
    draw.text((ex_x - 40, ex_y - 70), "-165 TORSO", fill=(255, 240, 80), font=FONT_LARGE)
    draw.text((ex_x - 85, ex_y - 95), "AMMO DETONATION // HULL BREACHED", fill=(255, 80, 60), font=FONT_BOLD)

    # 2. Advance Wars Infantry Defeat Callouts
    inf_x = iso_x(8.5, 4.5, 0, 443)
    inf_y = iso_y(8.5, 4.5, 0, 208) - 80
    draw.text((inf_x - 65, inf_y - 30), "CRUSHING BLOW! x1.5", fill=(255, 180, 40), font=FONT_BOLD)
    draw.text((inf_x - 90, inf_y - 50), "SQUAD OVERRUN // COMBAT INEFFECTIVE", fill=(255, 90, 80), font=FONT_BOLD)

    render_top_hud(draw)
    render_bottom_action_bar(draw, "Alpha-01 'WARHAMMER' [SALVO RESOLVED]")
    render_combat_terminal(draw, [
        "ERA 0 COMBINED-ARMS THEATER // SECTOR 4 MINING DEPOSIT",
        "[FIRING SALVO] Alpha-01 'WARHAMMER' engaged Hostile MBT with 120mm Cannon!",
        "[HIT] Direct kinetic breach on Armored Hull for 165 damage!",
        "[ARMOR BREACH] Hostile MBT 'MAMMOTH-3' magazine detonated! Hull breached.",
        "[SUPPRESSION] Allied Mammoth tank high-explosive round struck Scrap Militia!",
        "[SQUAD CASUALTY] Scrap Militia 'GUERRILLA-1' suffered catastrophic casualties! Unit overrun.",
        ">> VICTORY MOMENTUM: Allied combined-arms breach confirmed!"
    ])

    out_path = os.path.join(ARTIFACT_DIR, "snapshot_03_combat_salvo_and_advance_wars_defeat.png")
    im.save(out_path, "PNG")
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    generate_snapshot_1()
    generate_snapshot_2()
    generate_snapshot_3()
    print("All 3 high-detail combat snapshots successfully rendered!")
