import os, sys, math, re
from PIL import Image, ImageDraw, ImageFont

brain_dir = "/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e"
units_dir = os.path.join(brain_dir, "tactical_units")
gw, gh = 1366, 768

try:
    f_large = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 15)
    f_title = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 13)
    f_sub = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 10)
    f_bold = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 11)
    f_badge = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 9)
    f_hud = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf", 11)
except:
    f_large = f_title = f_sub = f_bold = f_badge = f_hud = ImageFont.load_default()

def draw_snes_panel(draw, x, y, w, h, title, title_col=(60, 180, 240)):
    draw.rectangle([x, y, x + w, y + h], fill=(12, 18, 28))
    draw.rectangle([x, y, x + w, y + h], outline=(45, 80, 120), width=2)
    draw.rectangle([x + 2, y + 2, x + w - 2, y + 24], fill=(18, 30, 48))
    draw.line([x + 2, y + 24, x + w - 2, y + 24], fill=(60, 120, 180), width=1)
    draw.text((x + 10, y + 6), title, font=f_bold, fill=title_col)

def draw_snes_button(draw, x, y, w, h, text, is_hov=False, is_sel=False, col=(0, 240, 255)):
    bg = (24, 48, 76) if is_hov else ((20, 40, 60) if is_sel else (14, 24, 38))
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    draw.rectangle([x, y, x + w, y + h], outline=col if (is_hov or is_sel) else (40, 75, 115), width=2 if (is_hov or is_sel) else 1)
    draw.rectangle([x, y, x + 4, y + h], fill=col)
    tw = draw.textlength(text, font=f_bold)
    draw.text((x + (w - tw) // 2, y + (h - 14) // 2), text, font=f_bold, fill=(255, 255, 255) if is_hov else col)

def draw_hex(draw, cx, cy, r, outline, fill=None):
    pts = []
    for i in range(6):
        ang = math.radians(60 * i - 30)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    if fill:
        draw.polygon(pts, fill=fill)
    draw.polygon(pts, outline=outline)

fac_colors = {
    "faction_a": (60, 140, 255),
    "faction_b": (40, 220, 180),
    "faction_c": (255, 160, 40),
    "faction_d": (180, 90, 240),
    "faction_e": (120, 130, 240),
    "faction_f": (240, 60, 60),
    "pmc": (255, 215, 60)
}

fac_hex_keys = {
    "faction_a": "spr_hex_base_terran",
    "faction_b": "spr_hex_base_colony",
    "faction_c": "spr_hex_base_syndicate",
    "faction_d": "spr_hex_base_zaibatsu",
    "faction_e": "spr_hex_base_sidereal",
    "faction_f": "spr_hex_base_mars",
    "pmc": "spr_hex_base_pmc"
}

def draw_tactical_counter(im, draw, cx, cy, fac, unit_sprite_name, stack_cnt, is_sel=False, is_hov=False, scale=1.0):
    hex_k = fac_hex_keys.get(fac, "spr_hex_base_terran")
    hex_path = os.path.join(units_dir, f"{hex_k}.png")
    if os.path.exists(hex_path):
        h_im = Image.open(hex_path).convert("RGBA")
        if scale != 1.0:
            h_im = h_im.resize((int(h_im.width * scale), int(h_im.height * scale)), Image.Resampling.LANCZOS)
        im.paste(h_im, (cx - h_im.width // 2, cy - h_im.height // 2), h_im)

    u_path = os.path.join(units_dir, f"{unit_sprite_name}.png")
    if os.path.exists(u_path):
        u_im = Image.open(u_path).convert("RGBA")
        if scale != 1.0:
            u_im = u_im.resize((int(u_im.width * scale), int(u_im.height * scale)), Image.Resampling.LANCZOS)
        im.paste(u_im, (cx - u_im.width // 2, cy - u_im.height // 2 - 4), u_im)

    bw, bh = 18, 13
    bx, by = cx + 8, cy + 4
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(12, 18, 28), outline=(0, 240, 255) if is_sel else (200, 200, 200))
    draw.text((bx + 3, by + 1), f"x{stack_cnt}", font=f_badge, fill=(255, 255, 255))

    if is_sel:
        draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=(0, 240, 255), width=2)
        draw.line([cx - 28, cy, cx - 22, cy], fill=(0, 240, 255), width=2)
        draw.line([cx + 22, cy, cx + 28, cy], fill=(0, 240, 255), width=2)
        draw.line([cx, cy - 28, cx, cy - 22], fill=(0, 240, 255), width=2)
        draw.line([cx, cy + 22, cx, cy + 28], fill=(0, 240, 255), width=2)

def draw_top_deck(draw, active_tab_name="WAR MAP", active_subtheater="EARTH THEATER"):
    draw.rectangle([0, 0, gw, 52], fill=(8, 14, 22))
    draw.line([0, 52, gw, 52], fill=(45, 80, 120), width=2)
    draw.text((20, 14), "⚡ FRONT MISSION: MECH MAKER CONCEPT // UNIFIED TACTICAL DECK", font=f_large, fill=(255, 215, 60))
    draw.text((gw - 360, 16), "FUNDS: $2,450,000  |  ALLOY: 14,200kg  |  YEAR 214", font=f_bold, fill=(0, 240, 255))

    draw.rectangle([16, 58, gw - 16, 92], fill=(12, 18, 26))
    tabs = ["PMC HANGAR", "FACTORY FORGE", "ALLOY CRUCIBLE", "WAR MAP", "FACTION NETWORK", "SYSTEM SETTINGS"]
    tx = 24
    for t in tabs:
        is_a = (t == active_tab_name)
        tw = int(draw.textlength(t, font=f_bold)) + 24
        draw.rectangle([tx, 62, tx + tw, 88], fill=(20, 44, 70) if is_a else (14, 22, 32), outline=(0, 240, 255) if is_a else (30, 50, 75))
        draw.text((tx + 12, 68), t, font=f_bold, fill=(255, 255, 255) if is_a else (140, 175, 210))
        tx += tw + 10

    th_x = 982
    draw.rectangle([th_x, 62, gw - 20, 88], fill=(14, 22, 34), outline=(45, 80, 120))
    theaters = ["SPACE", "EARTH", "MARS"]
    for i, th in enumerate(theaters):
        bx = th_x + 6 + i * 115
        is_th_a = (th in active_subtheater)
        draw.rectangle([bx, 64, bx + 110, 86], fill=(24, 50, 80) if is_th_a else (16, 26, 40), outline=(0, 240, 255) if is_th_a else (35, 60, 90))
        draw.text((bx + 16, 68), f"🌍 {th}" if th=="EARTH" else (f"🛰️ {th}" if th=="SPACE" else f"🔴 {th}"), font=f_bold, fill=(255, 215, 60) if is_th_a else (160, 190, 220))

def draw_bottom_hegemony(draw):
    bx, by, bw, bh = 16, 704, gw - 32, 52
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(10, 16, 24), outline=(35, 60, 90))
    bar_x, bar_y, bar_w, bar_h = bx + 14, by + 8, bw - 28, 14
    draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], fill=(20, 25, 35))

    f_defs = [
        ("TERRAN", 28, (60, 140, 255)),
        ("COLONY", 22, (40, 220, 180)),
        ("SYNDICATE", 16, (255, 160, 40)),
        ("ZAIBATSU", 14, (180, 90, 240)),
        ("SIDEREAL", 10, (120, 130, 240)),
        ("MARS", 6, (240, 60, 60)),
        ("PMC", 4, (255, 215, 60))
    ]
    cx = bar_x
    for name, pct, col in f_defs:
        w = int(bar_w * (pct / 100.0))
        draw.rectangle([cx, bar_y, cx + w, bar_y + bar_h], fill=col)
        cx += w
    draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], outline=(50, 80, 120))
    draw.text((bar_x + 4, bar_y + 20), "HEGEMONY PARITY: Terran: 28%  |  Colony: 22%  |  Syndicate: 16%  |  Zaibatsu: 14%  |  Sidereal: 10%  |  Mars: 6%  |  PMC: 4%", font=f_sub, fill=(180, 210, 240))

def render_stronghold_view(sh_data, out_filename):
    im = Image.new("RGBA", (gw, gh), (6, 10, 16, 255))
    draw = ImageDraw.Draw(im)

    draw_top_deck(draw, "WAR MAP", f"{sh_data['region']} THEATER")

    rad_x, rad_y, rad_w, rad_h = 16, 98, 954, 596
    draw_snes_panel(draw, rad_x, rad_y, rad_w, rad_h, f"STRATEGIC STRONGHOLD // {sh_data['name'].upper()}", (255, 215, 60))

    # Regional Background Map
    bg_p = f"sprites/{sh_data['sprite']}/{sh_data['sprite']}.png"
    if os.path.exists(bg_p):
        r_bg = Image.open(bg_p).convert("RGBA").resize((rad_w - 24, rad_h - 38), Image.Resampling.LANCZOS)
        tint = Image.new("RGBA", r_bg.size, (10, 20, 36, 40))
        r_bg = Image.alpha_composite(r_bg, tint)
        im.paste(r_bg, (rad_x + 12, rad_y + 26))

    # Grid
    for gx in range(rad_x + 40, rad_x + rad_w - 20, 64):
        draw.line([gx, rad_y + 26, gx, rad_y + rad_h - 12], fill=(20, 36, 52, 160))
    for gy in range(rad_y + 40, rad_y + rad_h - 12, 48):
        draw.line([rad_x + 12, gy, rad_x + rad_w - 12, gy], fill=(20, 36, 52, 160))

    # Range circles
    draw.ellipse([rad_x + rad_w//2 - 140, rad_y + rad_h//2 - 140, rad_x + rad_w//2 + 140, rad_y + rad_h//2 + 140], outline=(25, 60, 85))

    # Return Button
    ret_x, ret_y, ret_w, ret_h = rad_x + 20, rad_y + 34, 230, 28
    draw_snes_button(draw, ret_x, ret_y, ret_w, ret_h, "<< WORLD OVERVIEW [ESC]", is_hov=True, is_sel=False, col=(0, 240, 255))

    # Stronghold Banner
    sb_x = ret_x + ret_w + 12
    sb_w = rad_w - 24 - (ret_w + 24) - 235
    draw.rectangle([sb_x, ret_y, sb_x + sb_w, ret_y + ret_h], fill=(10, 16, 26), outline=(255, 215, 60))
    draw.text((sb_x + 12, ret_y + 6), f"★ MAJOR STRONGHOLD: {sh_data['name'].upper()}", font=f_bold, fill=(255, 230, 100))

    subnodes = sh_data["subnodes"]
    sub_map = {s["id"]: s for s in subnodes}

    # Pass 1: Defense vectors
    for s1 in subnodes:
        sx1 = rad_x + 40 + int(s1["x"] * 1.34)
        sy1 = rad_y + 48 + int(s1["y"] * 1.48)
        for cid in s1["conns"]:
            s2 = sub_map.get(cid)
            if s2:
                sx2 = rad_x + 40 + int(s2["x"] * 1.34)
                sy2 = rad_y + 48 + int(s2["y"] * 1.48)
                is_cont = (s1["fac"] != s2["fac"])
                if is_cont:
                    draw.line([sx1, sy1, sx2, sy2], fill=(255, 60, 70), width=3)
                    ang = math.atan2(sy2 - sy1, sx2 - sx1)
                    mid_x = (sx1 + sx2) // 2
                    mid_y = (sy1 + sy2) // 2
                    draw.polygon([
                        (mid_x + 8 * math.cos(ang), mid_y + 8 * math.sin(ang)),
                        (mid_x - 8 * math.cos(ang - 0.5), mid_y - 8 * math.sin(ang - 0.5)),
                        (mid_x - 8 * math.cos(ang + 0.5), mid_y - 8 * math.sin(ang + 0.5))
                    ], fill=(255, 130, 180))
                else:
                    draw.line([sx1, sy1, sx2, sy2], fill=(0, 200, 240, 180), width=2)
                    mid_x = (sx1 + sx2) // 2
                    mid_y = (sy1 + sy2) // 2
                    draw.ellipse([mid_x - 3, mid_y - 3, mid_x + 3, mid_y + 3], fill=(180, 240, 255))

    # Pass 2: Interactive Subnodes
    sel_sub = subnodes[0]
    for s in subnodes:
        snx = rad_x + 40 + int(s["x"] * 1.34)
        sny = rad_y + 48 + int(s["y"] * 1.48)
        is_sel = (s["id"] == sel_sub["id"])

        f_col = fac_colors[s["fac"]]
        draw_hex(draw, snx, sny - 4, 24, outline=f_col, fill=(f_col[0]//5, f_col[1]//5, f_col[2]//5))

        if s["core"]:
            draw.ellipse([snx - 30, sny - 34, snx + 30, sny + 26], outline=(255, 215, 60), width=2)
            draw.text((snx - 42, sny - 46), "[CENTRAL CORE]", font=f_badge, fill=(255, 240, 120))

        draw_tactical_counter(im, draw, snx, sny - 4, s["fac"], s["u"], s["cnt"], is_sel=is_sel, is_hov=False, scale=1.05)

        snb_w = 110
        snb_h = 18
        snb_y = sny + 16
        draw.rectangle([snx - snb_w//2, snb_y, snx + snb_w//2, snb_y + snb_h], fill=(24, 48, 76) if is_sel else (10, 16, 26), outline=(0, 240, 255) if is_sel else (50, 90, 130))
        draw.rectangle([snx - snb_w//2 + 2, snb_y + 2, snx - snb_w//2 + 5, snb_y + snb_h - 2], fill=f_col)
        draw.text((snx - snb_w//2 + 8, snb_y + 2), s["name"][:14], font=f_sub, fill=(255, 255, 255) if is_sel else (190, 215, 240))

    # Minimap
    mm_w, mm_h = 210, 118
    mm_x = rad_x + rad_w - mm_w - 18
    mm_y = rad_y + 36
    draw.rectangle([mm_x, mm_y, mm_x + mm_w, mm_y + mm_h], fill=(8, 14, 22), outline=(45, 80, 125))
    if sh_data["region"] == "MARS":
        mm_p = "sprites/spr_map_mars_theater/spr_map_mars_theater.png"
        title_tag = "THARSIS SATELLITE TELEMETRY"
        tag_col = (255, 90, 80)
    else:
        mm_p = "sprites/spr_radar_earth_amber/spr_radar_earth_amber.png"
        title_tag = "TERRESTRIAL SATELLITE RADAR"
        tag_col = (255, 215, 80)
    if os.path.exists(mm_p):
        mm_im = Image.open(mm_p).convert("RGBA").resize((mm_w - 4, mm_h - 4), Image.Resampling.LANCZOS)
        im.paste(mm_im, (mm_x + 2, mm_y + 2), mm_im)
    draw.text((mm_x + 8, mm_y + 6), title_tag, font=f_badge, fill=tag_col)

    # Tracking Box
    mb = sh_data["box"]
    draw.rectangle([mm_x + mb["x"], mm_y + mb["y"], mm_x + mb["x"] + mb["w"], mm_y + mb["y"] + mb["h"]], outline=(0, 240, 255), width=2)

    # Bottom-Right Terrain HUD
    thud_w, thud_h = 236, 92
    thud_x = rad_x + rad_w - thud_w - 18
    thud_y = rad_y + rad_h - thud_h - 18
    draw.rectangle([thud_x, thud_y, thud_x + thud_w, thud_y + thud_h], fill=(222, 226, 236), outline=(28, 40, 56), width=2)
    draw.rectangle([thud_x + 3, thud_y + 3, thud_x + thud_w - 3, thud_y + 24], fill=(240, 244, 252))
    draw.text((thud_x + 10, thud_y + 6), sh_data["hud"], font=f_bold, fill=(12, 22, 36))
    draw.text((thud_x + 10, thud_y + 30), "DEFENSE BONUS", font=f_sub, fill=(25, 35, 50))
    draw.text((thud_x + thud_w - 55, thud_y + 30), "+40 %", font=f_bold, fill=(0, 110, 180))
    draw.text((thud_x + 10, thud_y + 48), "RADAR MASKING", font=f_sub, fill=(25, 35, 50))
    draw.text((thud_x + thud_w - 55, thud_y + 48), "85 %", font=f_sub, fill=(25, 35, 50))
    draw.text((thud_x + 10, thud_y + 68), "ACTIVE SUBNODE", font=f_sub, fill=(25, 35, 50))
    draw.text((thud_x + thud_w - 55, thud_y + 68), f"0{sel_sub['cnt']} UNITS", font=f_bold, fill=(190, 40, 25))

    # --- DOSSIER ---
    dos_x = 982
    dos_y = 98
    dos_w = gw - dos_x - 16
    dos_h = rad_h
    draw_snes_panel(draw, dos_x, dos_y, dos_w, dos_h, "STRONGHOLD SECTOR DOSSIER", (255, 215, 60))

    thumb_x = dos_x + 16
    thumb_y = dos_y + 26
    thumb_w = dos_w - 32
    thumb_h = 130
    loc_path = f"sprites/{sh_data['loc_thumb']}/{sh_data['loc_thumb']}.png"
    if os.path.exists(loc_path):
        l_im = Image.open(loc_path).convert("RGBA").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        im.paste(l_im, (thumb_x, thumb_y), l_im)
    draw.rectangle([thumb_x, thumb_y, thumb_x + thumb_w, thumb_y + thumb_h], outline=(255, 215, 60))
    draw.rectangle([thumb_x + 8, thumb_y + thumb_h - 22, thumb_x + 195, thumb_y + thumb_h - 4], fill=(12, 18, 28), outline=(255, 215, 60))
    draw.text((thumb_x + 12, thumb_y + thumb_h - 19), f"SUBNODE TELEMETRY // {sel_sub['type']}", font=f_badge, fill=(255, 215, 60))

    cy = thumb_y + thumb_h + 8
    draw.text((dos_x + 16, cy), sel_sub["name"].upper(), font=f_bold, fill=(255, 220, 90))
    draw.text((dos_x + 16, cy + 18), f"{sh_data['name'][:22]} // {sel_sub['type']}", font=f_sub, fill=(140, 175, 210))

    # Garrison card
    g_y = cy + 36
    draw.rectangle([dos_x + 16, g_y, dos_x + dos_w - 16, g_y + 64], fill=(12, 18, 28), outline=(40, 75, 115))
    draw_tactical_counter(im, draw, dos_x + 46, g_y + 36, sel_sub["fac"], sel_sub["u"], sel_sub["cnt"], scale=1.1)
    draw.text((dos_x + 78, g_y + 8), sel_sub["label"].upper(), font=f_bold, fill=(255, 255, 255))
    draw.text((dos_x + 78, g_y + 24), f"GARRISON STRENGTH: [{sel_sub['cnt']}] UNITS", font=f_sub, fill=(0, 240, 255))
    draw.text((dos_x + 78, g_y + 42), "★ PRIMARY REGIONAL HQ", font=f_sub, fill=(160, 190, 220))

    # Controller box
    cbox_y = cy + 108
    draw.rectangle([dos_x + 16, cbox_y, dos_x + dos_w - 16, cbox_y + 44], fill=(14, 22, 32), outline=(60, 140, 255))
    draw.rectangle([dos_x + 16, cbox_y, dos_x + 20, cbox_y + 44], fill=(60, 140, 255))
    draw.text((dos_x + 26, cbox_y + 6), f"CONTROLLER: {sel_sub['fac'].upper()} GARRISON", font=f_bold, fill=(60, 140, 255))
    draw.text((dos_x + 26, cbox_y + 24), f"BASE SECTOR FORTIFICATION BONUS: +{sel_sub['def']} DEF", font=f_sub, fill=(80, 255, 140))

    # Defense bar
    def_y = cbox_y + 52
    draw.text((dos_x + 16, def_y), f"PERIMETER FORTIFICATION: {sel_sub['def']} / 100", font=f_bold, fill=(200, 220, 245))
    draw.rectangle([dos_x + 16, def_y + 18, dos_x + dos_w - 16, def_y + 28], fill=(20, 28, 40), outline=(50, 80, 120))
    d_fill = int((dos_w - 32) * (sel_sub['def'] / 100.0))
    draw.rectangle([dos_x + 16, def_y + 18, dos_x + 16 + d_fill, def_y + 28], fill=(255, 215, 60))

    # Lore
    draw.text((dos_x + 16, def_y + 36), "Primary strategic stronghold complex equipped with heavy fusion generators\nand interlocking perimeter defensive turrets.", font=f_sub, fill=(160, 190, 220))

    # Actions
    act_y = dos_y + dos_h - 100
    act_w = dos_w - 32
    draw_snes_button(draw, dos_x + 16, act_y, act_w, 32, ">> FORTIFY PERIMETER (+10 DEF: $20K) >>", is_hov=False, is_sel=False, col=(80, 240, 140))
    draw_snes_button(draw, dos_x + 16, act_y + 40, act_w, 34, "⚔️ SORTIE COMBAT SQUAD HERE", is_hov=True, is_sel=False, col=(255, 100, 100))

    draw_bottom_hegemony(draw)

    out_p = os.path.join(brain_dir, out_filename)
    im.save(out_p)
    print(f"Saved stronghold view to: {out_p}")

# Render Cascadia, Gibraltar, and Olympus
cascadia_data = {
    'name': 'Cascadia Mass-Driver Citadel',
    'region': 'EARTH',
    'sprite': 'spr_map_earth_theater',
    'loc_thumb': 'spr_loc_earth_granite',
    'box': {'x': 28, 'y': 24, 'w': 40, 'h': 30},
    'hud': 'PACIFIC MASS-DRIVER CRATON',
    'subnodes': [
        {'id': 'cascadia_apex_driver', 'name': 'Launch Rail Apex', 'type': 'MASS_DRIVER', 'x': 340, 'y': 220, 'fac': 'faction_a', 'def': 92, 'u': 'spr_mini_ms_commander', 'cnt': 4, 'label': 'Mass-Driver Command', 'conns': ['cascadia_san_joaquin_hangar', 'cascadia_sierra_redoubt', 'cascadia_pacific_dock'], 'core': True},
        {'id': 'cascadia_san_joaquin_hangar', 'name': 'Assembly Bay', 'type': 'ASSEMBLY_BAY', 'x': 280, 'y': 310, 'fac': 'faction_a', 'def': 78, 'u': 'spr_mini_veh_heavy_tank', 'cnt': 6, 'label': 'Valley Heavy Armor', 'conns': ['cascadia_apex_driver', 'cascadia_mojave_silo'], 'core': False},
        {'id': 'cascadia_pacific_dock', 'name': 'Puget Slipway', 'type': 'AIR_NAVAL_GATE', 'x': 190, 'y': 140, 'fac': 'faction_b', 'def': 72, 'u': 'spr_mini_veh_gunship', 'cnt': 6, 'label': 'Puget Coastal Wing', 'conns': ['cascadia_apex_driver', 'cascadia_sierra_redoubt'], 'core': False},
        {'id': 'cascadia_sierra_redoubt', 'name': 'Sierra Flak Spire', 'type': 'MOUNTAIN_BATTERY', 'x': 420, 'y': 180, 'fac': 'faction_a', 'def': 85, 'u': 'spr_mini_ms_artillery', 'cnt': 4, 'label': 'Sierra Flak Battery', 'conns': ['cascadia_apex_driver', 'cascadia_pacific_dock'], 'core': False},
        {'id': 'cascadia_mojave_silo', 'name': 'Mojave Silos', 'type': 'MISSILE_SILO', 'x': 460, 'y': 330, 'fac': 'faction_c', 'def': 76, 'u': 'spr_mini_inf_exo_squad', 'cnt': 8, 'label': 'Mojave Exo-Troopers', 'conns': ['cascadia_san_joaquin_hangar'], 'core': False},
        {'id': 'cascadia_perimeter_gate', 'name': 'Great Basin Gate', 'type': 'PERIMETER_DEPOT', 'x': 180, 'y': 260, 'fac': 'faction_b', 'def': 70, 'u': 'spr_mini_veh_technical', 'cnt': 6, 'label': 'Basin Technical Vanguard', 'conns': ['cascadia_san_joaquin_hangar'], 'core': False}
    ]
}

gibraltar_data = {
    'name': 'Gibraltar Sea-Gate Fortress',
    'region': 'EARTH',
    'sprite': 'spr_map_earth_theater',
    'loc_thumb': 'spr_loc_earth_granite',
    'box': {'x': 94, 'y': 28, 'w': 34, 'h': 28},
    'hud': 'MEDITERRANEAN SEA-GATE',
    'subnodes': [
        {'id': 'gibraltar_rock_citadel', 'name': 'Rock of Gibraltar', 'type': 'CORE_BUNKER', 'x': 320, 'y': 230, 'fac': 'faction_a', 'def': 96, 'u': 'spr_mini_ms_commander', 'cnt': 4, 'label': 'Gibraltar High Command', 'conns': ['gibraltar_strait_lock', 'gibraltar_andalusian_battery', 'gibraltar_alboran_acoustic'], 'core': True},
        {'id': 'gibraltar_strait_lock', 'name': 'Strait Sea Lock', 'type': 'SEA_GATE', 'x': 220, 'y': 260, 'fac': 'faction_a', 'def': 84, 'u': 'spr_mini_veh_heavy_tank', 'cnt': 6, 'label': 'Strait Marine Armor', 'conns': ['gibraltar_rock_citadel', 'gibraltar_ceuta_bridgehead'], 'core': False},
        {'id': 'gibraltar_alboran_acoustic', 'name': 'Hydrophone Array', 'type': 'SONAR_PERIMETER', 'x': 440, 'y': 280, 'fac': 'faction_b', 'def': 75, 'u': 'spr_mini_veh_gunship', 'cnt': 6, 'label': 'Alboran Sub-Hunter Wing', 'conns': ['gibraltar_rock_citadel'], 'core': False},
        {'id': 'gibraltar_andalusian_battery', 'name': 'Andalusian Battery', 'type': 'MOUNTAIN_BATTERY', 'x': 340, 'y': 130, 'fac': 'faction_a', 'def': 80, 'u': 'spr_mini_ms_artillery', 'cnt': 4, 'label': 'Andalusian Rail Artillery', 'conns': ['gibraltar_rock_citadel'], 'core': False},
        {'id': 'gibraltar_ceuta_bridgehead', 'name': 'Ceuta Shore Bastion', 'type': 'PERIMETER_DEPOT', 'x': 180, 'y': 340, 'fac': 'faction_c', 'def': 72, 'u': 'spr_mini_veh_technical', 'cnt': 6, 'label': 'Ceuta Coastal Recon', 'conns': ['gibraltar_strait_lock'], 'core': False}
    ]
}

olympus_data = {
    'name': 'Mount Olympus Zenith Redoubt',
    'region': 'MARS',
    'sprite': 'spr_map_mars_theater',
    'loc_thumb': 'spr_loc_mars_redoubt',
    'box': {'x': 38, 'y': 28, 'w': 54, 'h': 48},
    'hud': 'MARTIAN VOLCANIC CALDERA',
    'subnodes': [
        {'id': 'olympus_caldera_core', 'name': 'Caldera Rim Redoubt', 'type': 'CORE_BUNKER', 'x': 340, 'y': 220, 'fac': 'faction_f', 'def': 98, 'u': 'spr_mini_ms_commander', 'cnt': 5, 'label': 'Red Guard High Command', 'conns': ['olympus_scarp_battery', 'olympus_lava_tube_dock', 'olympus_zenith_silos'], 'core': True},
        {'id': 'olympus_scarp_battery', 'name': 'Basalt Scarp Battery', 'type': 'MOUNTAIN_BATTERY', 'x': 220, 'y': 150, 'fac': 'faction_f', 'def': 88, 'u': 'spr_mini_ms_artillery', 'cnt': 4, 'label': 'Scarp Kinetic Battery', 'conns': ['olympus_caldera_core', 'olympus_aureole_sentry'], 'core': False},
        {'id': 'olympus_lava_tube_dock', 'name': 'Lava Tube MS Bay', 'type': 'SUB_HANGAR', 'x': 450, 'y': 270, 'fac': 'faction_f', 'def': 82, 'u': 'spr_mini_veh_heavy_tank', 'cnt': 6, 'label': 'Caldera Heavy Armor', 'conns': ['olympus_caldera_core'], 'core': False},
        {'id': 'olympus_aureole_sentry', 'name': 'Aureole Plain Gate', 'type': 'PERIMETER_DEPOT', 'x': 160, 'y': 280, 'fac': 'faction_f', 'def': 76, 'u': 'spr_mini_veh_technical', 'cnt': 6, 'label': 'Aureole Technical Rovers', 'conns': ['olympus_scarp_battery'], 'core': False},
        {'id': 'olympus_zenith_silos', 'name': 'Zenith Torpedo Silos', 'type': 'MISSILE_SILO', 'x': 420, 'y': 130, 'fac': 'faction_f', 'def': 85, 'u': 'spr_mini_inf_exo_squad', 'cnt': 8, 'label': 'Olympus Shock Troops', 'conns': ['olympus_caldera_core'], 'core': False}
    ]
}

if __name__ == "__main__":
    render_stronghold_view(cascadia_data, "live_stronghold_cascadia_mass_driver.png")
    render_stronghold_view(gibraltar_data, "live_stronghold_gibraltar_sea_gate.png")
    render_stronghold_view(olympus_data, "live_stronghold_olympus_caldera_mars.png")
