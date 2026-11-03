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

    # Stack Badge
    bw, bh = 18, 13
    bx = cx + 8
    by = cy + 4
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(12, 18, 28), outline=(0, 240, 255) if is_sel else (200, 200, 200))
    draw.text((bx + 3, by + 1), f"x{stack_cnt}", font=f_badge, fill=(255, 255, 255))

    # Selection Ring
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

    # Sub-tabs
    draw.rectangle([16, 58, gw - 16, 92], fill=(12, 18, 26))
    tabs = ["PMC HANGAR", "FACTORY FORGE", "ALLOY CRUCIBLE", "WAR MAP", "FACTION NETWORK", "SYSTEM SETTINGS"]
    tx = 24
    for t in tabs:
        is_a = (t == active_tab_name)
        tw = int(draw.textlength(t, font=f_bold)) + 24
        draw.rectangle([tx, 62, tx + tw, 88], fill=(20, 44, 70) if is_a else (14, 22, 32), outline=(0, 240, 255) if is_a else (30, 50, 75))
        draw.text((tx + 12, 68), t, font=f_bold, fill=(255, 255, 255) if is_a else (140, 175, 210))
        tx += tw + 10

    # Theater Selector
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

# =========================================================================
# 1. RENDER TIER 1: GLOBAL WORLD OVERVIEW
# =========================================================================
def render_tier1_global():
    im = Image.new("RGBA", (gw, gh), (6, 10, 16, 255))
    draw = ImageDraw.Draw(im)

    draw_top_deck(draw, "WAR MAP", "EARTH THEATER")

    rad_x, rad_y, rad_w, rad_h = 16, 98, 954, 596
    draw_snes_panel(draw, rad_x, rad_y, rad_w, rad_h, "EARTH THEATER // GLOBAL STRATEGIC OVERVIEW (10 CONTINENTAL CITADELS)", (60, 180, 240))

    # Stretched global satellite map
    glob_path = "sprites/spr_map_earth_global/spr_map_earth_global.png"
    if os.path.exists(glob_path):
        g_bg = Image.open(glob_path).convert("RGBA")
        g_bg = g_bg.resize((rad_w - 24, rad_h - 38), Image.Resampling.LANCZOS)
        # Apply dark tactical overlay tint
        tint = Image.new("RGBA", g_bg.size, (10, 20, 36, 60))
        g_bg = Image.alpha_composite(g_bg, tint)
        im.paste(g_bg, (rad_x + 12, rad_y + 26))

    # Grid lines
    for gx in range(rad_x + 40, rad_x + rad_w - 20, 64):
        draw.line([gx, rad_y + 26, gx, rad_y + rad_h - 12], fill=(18, 30, 46, 150))
    for gy in range(rad_y + 40, rad_y + rad_h - 12, 48):
        draw.line([rad_x + 12, gy, rad_x + rad_w - 12, gy], fill=(18, 30, 46, 150))

    # Equator Line
    eq_y = rad_y + 26 + int(390 * ((rad_h - 38) / 768.0))
    draw.line([rad_x + 12, eq_y, rad_x + rad_w - 12, eq_y], fill=(0, 220, 255, 90), width=1)
    draw.text((rad_x + 20, eq_y - 12), "EQUATORIAL TRANSIT VECTOR // LAT 00°00'00\"", font=f_badge, fill=(0, 200, 240, 140))

    # Header Banner
    draw.rectangle([rad_x + 20, rad_y + 32, rad_x + 500, rad_y + 60], fill=(10, 16, 26), outline=(0, 240, 255))
    draw.text((rad_x + 28, rad_y + 38), "GLOBAL CITADEL NETWORK: 10 STRATEGIC CONTINENTAL BASES", font=f_bold, fill=(255, 220, 80))

    gx_scale = (rad_w - 24) / 1376.0
    gy_scale = (rad_h - 38) / 768.0

    bases = [
        {"id": "earth_granite_redoubt", "name": "Granite Deep", "full": "Granite Deep Command Redoubt", "gx": 440, "gy": 470, "fac": "faction_a", "unit": "spr_mini_ms_commander", "cnt": 5, "stronghold": True, "conns": ["earth_cascadia_driver", "earth_andes_battery", "earth_gibraltar_redoubt"]},
        {"id": "earth_cascadia_driver", "name": "Cascadia", "full": "Cascadia Mass-Driver Complex", "gx": 270, "gy": 250, "fac": "faction_a", "unit": "spr_mini_veh_heavy_tank", "cnt": 6, "stronghold": False, "conns": ["earth_granite_redoubt", "earth_shanghai_arcology", "earth_nordic_vault"]},
        {"id": "earth_sahara_array", "name": "Al-Kufra", "full": "Al-Kufra Solar Gantry Array", "gx": 730, "gy": 360, "fac": "faction_c", "unit": "spr_mini_veh_technical", "cnt": 4, "stronghold": False, "conns": ["earth_gibraltar_redoubt", "earth_ural_arsenal", "earth_andes_battery"]},
        {"id": "earth_andes_battery", "name": "Chimborazo", "full": "Chimborazo Orbital Bastion", "gx": 390, "gy": 430, "fac": "faction_b", "unit": "spr_mini_ms_artillery", "cnt": 4, "stronghold": False, "conns": ["earth_granite_redoubt", "earth_sahara_array", "earth_cascadia_driver"]},
        {"id": "earth_gibraltar_redoubt", "name": "Gibraltar", "full": "Gibraltar Sea-Gate Bastion", "gx": 660, "gy": 290, "fac": "faction_a", "unit": "spr_mini_veh_gunship", "cnt": 6, "stronghold": False, "conns": ["earth_granite_redoubt", "earth_sahara_array", "earth_nordic_vault"]},
        {"id": "earth_outback_proving", "name": "Woomera", "full": "Woomera Proving Grounds", "gx": 1180, "gy": 520, "fac": "faction_c", "unit": "spr_mini_ms_grunt", "cnt": 4, "stronghold": False, "conns": ["earth_shanghai_arcology", "earth_antarctic_facility", "earth_andes_battery"]},
        {"id": "earth_shanghai_arcology", "name": "Neo-Shanghai", "full": "Neo-Shanghai Arcology Spire", "gx": 1060, "gy": 310, "fac": "faction_d", "unit": "spr_mini_ms_aerostriker", "cnt": 5, "stronghold": False, "conns": ["earth_cascadia_driver", "earth_outback_proving", "earth_ural_arsenal"]},
        {"id": "earth_nordic_vault", "name": "Skagerrak", "full": "Skagerrak Sub-Sea Hangar", "gx": 680, "gy": 210, "fac": "faction_b", "unit": "spr_mini_veh_heavy_tank", "cnt": 6, "stronghold": False, "conns": ["earth_cascadia_driver", "earth_gibraltar_redoubt", "earth_ural_arsenal"]},
        {"id": "earth_ural_arsenal", "name": "Ural Munitions", "full": "Ural Mountain Munitions Vault", "gx": 870, "gy": 210, "fac": "faction_a", "unit": "spr_mini_ms_artillery", "cnt": 4, "stronghold": False, "conns": ["earth_sahara_array", "earth_nordic_vault", "earth_shanghai_arcology"]},
        {"id": "earth_antarctic_facility", "name": "Vostok", "full": "Vostok Sub-Glacial Vault", "gx": 750, "gy": 690, "fac": "faction_b", "unit": "spr_mini_inf_exo_squad", "cnt": 8, "stronghold": False, "conns": ["earth_granite_redoubt", "earth_outback_proving", "earth_andes_battery"]},
    ]

    base_map = {b["id"]: b for b in bases}

    # Pass 1: Global Intercontinental Hyperlanes
    for b1 in bases:
        x1 = rad_x + 12 + int(b1["gx"] * gx_scale)
        y1 = rad_y + 26 + int(b1["gy"] * gy_scale)
        for cid in b1["conns"]:
            b2 = base_map.get(cid)
            if b2:
                x2 = rad_x + 12 + int(b2["gx"] * gx_scale)
                y2 = rad_y + 26 + int(b2["gy"] * gy_scale)
                is_cont = (b1["fac"] != b2["fac"])
                if is_cont:
                    draw.line([x1, y1, x2, y2], fill=(255, 60, 70), width=2)
                    mid_x = (x1 + x2) // 2
                    mid_y = (y1 + y2) // 2
                    ang = math.atan2(y2 - y1, x2 - x1)
                    draw.polygon([
                        (mid_x + 8 * math.cos(ang), mid_y + 8 * math.sin(ang)),
                        (mid_x - 8 * math.cos(ang - 0.5), mid_y - 8 * math.sin(ang - 0.5)),
                        (mid_x - 8 * math.cos(ang + 0.5), mid_y - 8 * math.sin(ang + 0.5))
                    ], fill=(255, 120, 160))
                else:
                    draw.line([x1, y1, x2, y2], fill=(0, 160, 210, 130), width=1)

    # Pass 2: Base nodes
    for b in bases:
        nx = rad_x + 12 + int(b["gx"] * gx_scale)
        ny = rad_y + 26 + int(b["gy"] * gy_scale)
        is_sel = (b["id"] == "earth_granite_redoubt")

        # Hex influence
        f_col = fac_colors[b["fac"]]
        draw_hex(draw, nx, ny - 4, 22, outline=f_col, fill=(f_col[0]//5, f_col[1]//5, f_col[2]//5))

        # Major Stronghold Bracket Ring
        if b["stronghold"]:
            draw.ellipse([nx - 28, ny - 32, nx + 28, ny + 24], outline=(255, 215, 60), width=2)
            draw.text((nx - 48, ny - 42), "★ STRONGHOLD ★", font=f_badge, fill=(255, 240, 120))

        # Tactical Counter
        draw_tactical_counter(im, draw, nx, ny - 4, b["fac"], b["unit"], b["cnt"], is_sel=is_sel, is_hov=False, scale=1.0)

        # Nameplate Banner
        nb_w = 94
        nb_h = 16
        nb_y = ny + 16
        draw.rectangle([nx - nb_w//2, nb_y, nx + nb_w//2, nb_y + nb_h], fill=(24, 48, 76) if is_sel else (10, 16, 26), outline=(0, 240, 255) if is_sel else (45, 80, 120))
        draw.rectangle([nx - nb_w//2 + 2, nb_y + 2, nx - nb_w//2 + 5, nb_y + nb_h - 2], fill=f_col)
        draw.text((nx - nb_w//2 + 8, nb_y + 1), b["name"], font=f_sub, fill=(255, 255, 255) if is_sel else (190, 215, 240))

    # Top-Right Sol Alignment Minimap
    mm_w, mm_h = 210, 118
    mm_x = rad_x + rad_w - mm_w - 18
    mm_y = rad_y + 36
    draw.rectangle([mm_x, mm_y, mm_x + mm_w, mm_y + mm_h], fill=(8, 14, 22, 220), outline=(45, 80, 125))
    draw.text((mm_x + 8, mm_y + 6), "SOL ORBITAL ALIGNMENT", font=f_badge, fill=(0, 240, 255))
    mcx, mcy = mm_x + 105, mm_y + 68
    draw.ellipse([mcx - 78, mcy - 38, mcx + 78, mcy + 38], outline=(25, 45, 75))
    draw.ellipse([mcx - 50, mcy - 24, mcx + 50, mcy + 24], outline=(25, 45, 75))
    draw.ellipse([mcx - 26, mcy - 12, mcx + 26, mcy + 12], outline=(25, 45, 75))
    draw.ellipse([mcx - 4, mcy - 4, mcx + 4, mcy + 4], fill=(255, 215, 80)) # Sol
    draw.ellipse([mcx + 44, mcy - 14, mcx + 48, mcy - 10], fill=(60, 150, 255)) # Earth
    draw.ellipse([mcx - 72, mcy + 14, mcx - 68, mcy + 18], fill=(240, 80, 60)) # Mars

    # Bottom-Right Tactical Terrain HUD Box
    thud_w, thud_h = 236, 92
    thud_x = rad_x + rad_w - thud_w - 18
    thud_y = rad_y + rad_h - thud_h - 18
    draw.rectangle([thud_x, thud_y, thud_x + thud_w, thud_y + thud_h], fill=(222, 226, 236), outline=(28, 40, 56), width=2)
    draw.rectangle([thud_x + 3, thud_y + 3, thud_x + thud_w - 3, thud_y + 24], fill=(240, 244, 252))
    draw.text((thud_x + 10, thud_y + 6), "TERRESTRIAL CRATON", font=f_bold, fill=(12, 22, 36))
    draw.text((thud_x + 10, thud_y + 30), "DEFENSE BONUS", font=f_sub, fill=(25, 35, 50))
    draw.text((thud_x + thud_w - 55, thud_y + 30), "+20 %", font=f_bold, fill=(0, 110, 180))
    draw.text((thud_x + 10, thud_y + 48), "SENSOR DENSITY", font=f_sub, fill=(25, 35, 50))
    draw.text((thud_x + thud_w - 55, thud_y + 48), "00 %", font=f_sub, fill=(25, 35, 50))
    draw.text((thud_x + 10, thud_y + 68), "GARRISON SQUAD", font=f_sub, fill=(25, 35, 50))
    draw.text((thud_x + thud_w - 55, thud_y + 68), "05 MS", font=f_bold, fill=(190, 40, 25))

    # --- DOSSIER FOR GRANITE DEEP COMMAND ---
    dos_x = 982
    dos_y = 98
    dos_w = gw - dos_x - 16
    dos_h = rad_h
    draw_snes_panel(draw, dos_x, dos_y, dos_w, dos_h, "TACTICAL SECTOR DOSSIER", (100, 200, 255))

    # Location thumbnail
    thumb_x = dos_x + 16
    thumb_y = dos_y + 26
    thumb_w = dos_w - 32
    thumb_h = 130
    loc_path = "sprites/spr_loc_earth_granite/spr_loc_earth_granite.png"
    if os.path.exists(loc_path):
        l_im = Image.open(loc_path).convert("RGBA").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        im.paste(l_im, (thumb_x, thumb_y), l_im)
    draw.rectangle([thumb_x, thumb_y, thumb_x + thumb_w, thumb_y + thumb_h], outline=(0, 220, 255))
    draw.rectangle([thumb_x + 8, thumb_y + thumb_h - 22, thumb_x + 185, thumb_y + thumb_h - 4], fill=(12, 18, 28), outline=(0, 240, 255))
    draw.text((thumb_x + 12, thumb_y + thumb_h - 19), "RECON TELEMETRY // SEC-01", font=f_badge, fill=(0, 240, 255))

    cy = thumb_y + thumb_h + 8
    draw.text((dos_x + 16, cy), "GRANITE DEEP COMMAND REDOUBT", font=f_bold, fill=(255, 220, 90))
    draw.text((dos_x + 16, cy + 18), "EARTH // South America Craton", font=f_sub, fill=(140, 175, 210))

    # Garrison tac-card
    g_y = cy + 36
    draw.rectangle([dos_x + 16, g_y, dos_x + dos_w - 16, g_y + 64], fill=(12, 18, 28), outline=(40, 75, 115))
    draw_tactical_counter(im, draw, dos_x + 46, g_y + 36, "faction_a", "spr_mini_ms_commander", 5, scale=1.1)
    draw.text((dos_x + 78, g_y + 8), "TERRAN DEFENSE COMMAND DIVISION", font=f_bold, fill=(255, 255, 255))
    draw.text((dos_x + 78, g_y + 24), "SQUADRON STRENGTH: [5] HEAVY UNITS", font=f_sub, fill=(0, 240, 255))
    draw.text((dos_x + 78, g_y + 42), "GHA-07 Ironclad MS Squad", font=f_sub, fill=(160, 190, 220))

    # Controller Box
    cbox_y = cy + 108
    draw.rectangle([dos_x + 16, cbox_y, dos_x + dos_w - 16, cbox_y + 44], fill=(14, 22, 32), outline=(60, 140, 255))
    draw.rectangle([dos_x + 16, cbox_y, dos_x + 20, cbox_y + 44], fill=(60, 140, 255))
    draw.text((dos_x + 26, cbox_y + 6), "CONTROLLER: Terran Defense Coalition (TDC)", font=f_bold, fill=(60, 140, 255))
    draw.text((dos_x + 26, cbox_y + 24), "DAILY YIELD: +8,500 Cr / +120kg TITANIUM", font=f_sub, fill=(80, 255, 140))

    # Defense Rating
    def_y = cbox_y + 52
    draw.text((dos_x + 16, def_y), "DEFENSE FORTIFICATION: 95 / 100", font=f_bold, fill=(200, 220, 245))
    draw.rectangle([dos_x + 16, def_y + 18, dos_x + dos_w - 16, def_y + 28], fill=(20, 28, 40), outline=(50, 80, 120))
    d_fill = int((dos_w - 32) * 0.95)
    draw.rectangle([dos_x + 16, def_y + 18, dos_x + 16 + d_fill, def_y + 28], fill=(0, 220, 255))

    # Lore
    draw.text((dos_x + 16, def_y + 36), "★ CONTESTED FRONTLINE BATTLEGROUND", font=f_bold, fill=(255, 80, 80))
    draw.text((dos_x + 16, def_y + 54), "Massive subterranean fortress carved three kilometers beneath ancient\ngranite strata. Features deep river docking bays and heavy vulcan turrets.", font=f_sub, fill=(160, 190, 220))

    # Direct Action Buttons
    act_y = dos_y + dos_h - 120
    act_w = dos_w - 32

    # Prominent Major Stronghold Map Button
    draw_snes_button(draw, dos_x + 16, act_y - 38, act_w, 32, "🔍 ENTER BASE THEATER (SEPARATE MAP) >>", is_hov=True, is_sel=False, col=(255, 215, 60))
    draw_snes_button(draw, dos_x + 16, act_y, act_w, 32, "⚔️ LAUNCH INVASION ASSAULT ($15K)", is_hov=False, is_sel=False, col=(255, 180, 60))
    draw_snes_button(draw, dos_x + 16, act_y + 38, act_w, 34, "⚔️ SORTIE COMBAT SQUAD HERE", is_hov=False, is_sel=False, col=(255, 100, 100))

    draw_bottom_hegemony(draw)

    out_p = os.path.join(brain_dir, "live_earth_tier1_global_overview.png")
    im.save(out_p)
    print("Saved Tier 1 Global Overview to:", out_p)

# =========================================================================
# 2. RENDER TIER 2: DEDICATED MAJOR STRONGHOLD BASE MAP (GRANITE DEEP)
# =========================================================================
def render_tier2_stronghold():
    im = Image.new("RGBA", (gw, gh), (6, 10, 16, 255))
    draw = ImageDraw.Draw(im)

    draw_top_deck(draw, "WAR MAP", "EARTH THEATER")

    rad_x, rad_y, rad_w, rad_h = 16, 98, 954, 596
    draw_snes_panel(draw, rad_x, rad_y, rad_w, rad_h, "STRATEGIC STRONGHOLD // GRANITE DEEP COMMAND [REGIONAL THEATER]", (255, 215, 60))

    # Stretched regional theater map
    reg_path = "sprites/spr_map_earth_theater/spr_map_earth_theater.png"
    if os.path.exists(reg_path):
        r_bg = Image.open(reg_path).convert("RGBA")
        r_bg = r_bg.resize((rad_w - 24, rad_h - 38), Image.Resampling.LANCZOS)
        tint = Image.new("RGBA", r_bg.size, (10, 20, 36, 40))
        r_bg = Image.alpha_composite(r_bg, tint)
        im.paste(r_bg, (rad_x + 12, rad_y + 26))

    # Tactical Grid Lines
    for gx in range(rad_x + 40, rad_x + rad_w - 20, 64):
        draw.line([gx, rad_y + 26, gx, rad_y + rad_h - 12], fill=(20, 36, 52, 160))
    for gy in range(rad_y + 40, rad_y + rad_h - 12, 48):
        draw.line([rad_x + 12, gy, rad_x + rad_w - 12, gy], fill=(20, 36, 52, 160))

    # Range Circles
    draw.ellipse([rad_x + rad_w//2 - 140, rad_y + rad_h//2 - 140, rad_x + rad_w//2 + 140, rad_y + rad_h//2 + 140], outline=(25, 60, 85))
    draw.ellipse([rad_x + rad_w//2 - 250, rad_y + rad_h//2 - 250, rad_x + rad_w//2 + 250, rad_y + rad_h//2 + 250], outline=(25, 60, 85))

    # Navigation Return Button
    ret_x, ret_y, ret_w, ret_h = rad_x + 20, rad_y + 34, 230, 28
    draw_snes_button(draw, ret_x, ret_y, ret_w, ret_h, "<< WORLD OVERVIEW [ESC]", is_hov=True, is_sel=False, col=(0, 240, 255))

    # Stronghold Title Banner
    sb_x = ret_x + ret_w + 12
    sb_w = rad_w - 24 - (ret_w + 24) - 235
    draw.rectangle([sb_x, ret_y, sb_x + sb_w, ret_y + ret_h], fill=(10, 16, 26), outline=(255, 215, 60))
    draw.text((sb_x + 12, ret_y + 6), "★ MAJOR STRONGHOLD: GRANITE DEEP COMMAND (SOUTH AMERICA)", font=f_bold, fill=(255, 230, 100))

    # 6 Local Defense Subnodes
    subnodes = [
        {"id": "granite_core", "name": "Command Redoubt", "type": "CORE_BUNKER", "mx": 390, "my": 280, "fac": "faction_a", "unit": "spr_mini_ms_commander", "cnt": 4, "core": True, "label": "Command Division", "conns": ["granite_north_gate", "granite_andes_battery", "granite_missile_silos"]},
        {"id": "granite_north_gate", "name": "Amazon Flank Sentry", "type": "RIVER_GATE", "mx": 320, "my": 180, "fac": "faction_a", "unit": "spr_mini_veh_heavy_tank", "cnt": 6, "core": False, "label": "Amazon Armor Cohort", "conns": ["granite_core", "granite_caribbean_dock"]},
        {"id": "granite_andes_battery", "name": "Chimborazo Rail Battery", "type": "MOUNTAIN_BATTERY", "mx": 210, "my": 220, "fac": "faction_b", "unit": "spr_mini_ms_artillery", "cnt": 4, "core": False, "label": "Andes Artillery MS", "conns": ["granite_core", "granite_pacific_coast"]},
        {"id": "granite_caribbean_dock", "name": "Caribbean Anchorage", "type": "AIR_NAVAL_GATE", "mx": 170, "my": 90, "fac": "faction_b", "unit": "spr_mini_veh_gunship", "cnt": 6, "core": False, "label": "Caribbean Drop Wing", "conns": ["granite_north_gate"]},
        {"id": "granite_missile_silos", "name": "Mato Grosso Silos", "type": "MISSILE_SILO", "mx": 480, "my": 350, "fac": "faction_a", "unit": "spr_mini_inf_exo_squad", "cnt": 8, "core": False, "label": "Rainforest Exo-Troopers", "conns": ["granite_core"]},
        {"id": "granite_pacific_coast", "name": "Pacific Shoreline Depot", "type": "PERIMETER_DEPOT", "mx": 150, "my": 340, "fac": "faction_c", "unit": "spr_mini_veh_technical", "cnt": 6, "core": False, "label": "Pacific Shore Techs", "conns": ["granite_andes_battery"]},
    ]

    sub_map = {s["id"]: s for s in subnodes}

    # Pass 1: Local Perimeter Supply & Defense Lines
    for s1 in subnodes:
        sx1 = rad_x + 40 + int(s1["mx"] * 1.34)
        sy1 = rad_y + 48 + int(s1["my"] * 1.48)
        for cid in s1["conns"]:
            s2 = sub_map.get(cid)
            if s2:
                sx2 = rad_x + 40 + int(s2["mx"] * 1.34)
                sy2 = rad_y + 48 + int(s2["my"] * 1.48)
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

    # Pass 2: Local Subnodes
    for s in subnodes:
        snx = rad_x + 40 + int(s["mx"] * 1.34)
        sny = rad_y + 48 + int(s["my"] * 1.48)
        is_sel = (s["id"] == "granite_core")

        f_col = fac_colors[s["fac"]]
        draw_hex(draw, snx, sny - 4, 24, outline=f_col, fill=(f_col[0]//5, f_col[1]//5, f_col[2]//5))

        if s["core"]:
            draw.ellipse([snx - 30, sny - 34, snx + 30, sny + 26], outline=(255, 215, 60), width=2)
            draw.text((snx - 42, sny - 46), "[CENTRAL CORE]", font=f_badge, fill=(255, 240, 120))

        draw_tactical_counter(im, draw, snx, sny - 4, s["fac"], s["unit"], s["cnt"], is_sel=is_sel, is_hov=False, scale=1.05)

        snb_w = 110
        snb_h = 18
        snb_y = sny + 16
        draw.rectangle([snx - snb_w//2, snb_y, snx + snb_w//2, snb_y + snb_h], fill=(24, 48, 76) if is_sel else (10, 16, 26), outline=(0, 240, 255) if is_sel else (50, 90, 130))
        draw.rectangle([snx - snb_w//2 + 2, snb_y + 2, snx - snb_w//2 + 5, snb_y + snb_h - 2], fill=f_col)
        draw.text((snx - snb_w//2 + 8, snb_y + 2), s["name"], font=f_sub, fill=(255, 255, 255) if is_sel else (190, 215, 240))

    # Top-Right Amber Satellite Radar (matching user reference media_1792505836970.png)
    mm_w, mm_h = 210, 118
    mm_x = rad_x + rad_w - mm_w - 18
    mm_y = rad_y + 36
    draw.rectangle([mm_x, mm_y, mm_x + mm_w, mm_y + mm_h], fill=(8, 14, 22), outline=(45, 80, 125))
    amb_path = "sprites/spr_radar_earth_amber/spr_radar_earth_amber.png"
    if os.path.exists(amb_path):
        amb_im = Image.open(amb_path).convert("RGBA").resize((mm_w - 4, mm_h - 4), Image.Resampling.LANCZOS)
        im.paste(amb_im, (mm_x + 2, mm_y + 2), amb_im)
    draw.text((mm_x + 8, mm_y + 6), "TERRESTRIAL SATELLITE RADAR", font=f_badge, fill=(255, 215, 80))
    # Active camera box over South America
    draw.rectangle([mm_x + 48, mm_y + 54, mm_x + 88, mm_y + 92], outline=(0, 240, 255), width=2)

    # Bottom-Right Terrain HUD Box
    thud_w, thud_h = 236, 92
    thud_x = rad_x + rad_w - thud_w - 18
    thud_y = rad_y + rad_h - thud_h - 18
    draw.rectangle([thud_x, thud_y, thud_x + thud_w, thud_y + thud_h], fill=(222, 226, 236), outline=(28, 40, 56), width=2)
    draw.rectangle([thud_x + 3, thud_y + 3, thud_x + thud_w - 3, thud_y + 24], fill=(240, 244, 252))
    draw.text((thud_x + 10, thud_y + 6), "SUBTERRANEAN GRANITE CRATON", font=f_bold, fill=(12, 22, 36))
    draw.text((thud_x + 10, thud_y + 30), "DEFENSE BONUS", font=f_sub, fill=(25, 35, 50))
    draw.text((thud_x + thud_w - 55, thud_y + 30), "+40 %", font=f_bold, fill=(0, 110, 180))
    draw.text((thud_x + 10, thud_y + 48), "RADAR MASKING", font=f_sub, fill=(25, 35, 50))
    draw.text((thud_x + thud_w - 55, thud_y + 48), "85 %", font=f_sub, fill=(25, 35, 50))
    draw.text((thud_x + 10, thud_y + 68), "ACTIVE SUBNODE", font=f_sub, fill=(25, 35, 50))
    draw.text((thud_x + thud_w - 55, thud_y + 68), "04 UNITS", font=f_bold, fill=(190, 40, 25))

    # --- DOSSIER FOR SELECTED SUBNODE (GRANITE CORE) ---
    dos_x = 982
    dos_y = 98
    dos_w = gw - dos_x - 16
    dos_h = rad_h
    draw_snes_panel(draw, dos_x, dos_y, dos_w, dos_h, "STRONGHOLD SECTOR DOSSIER", (255, 215, 60))

    thumb_x = dos_x + 16
    thumb_y = dos_y + 26
    thumb_w = dos_w - 32
    thumb_h = 130
    loc_path = "sprites/spr_loc_earth_granite/spr_loc_earth_granite.png"
    if os.path.exists(loc_path):
        l_im = Image.open(loc_path).convert("RGBA").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        im.paste(l_im, (thumb_x, thumb_y), l_im)
    draw.rectangle([thumb_x, thumb_y, thumb_x + thumb_w, thumb_y + thumb_h], outline=(255, 215, 60))
    draw.rectangle([thumb_x + 8, thumb_y + thumb_h - 22, thumb_x + 195, thumb_y + thumb_h - 4], fill=(12, 18, 28), outline=(255, 215, 60))
    draw.text((thumb_x + 12, thumb_y + thumb_h - 19), "SUBNODE TELEMETRY // SEC-01", font=f_badge, fill=(255, 215, 60))

    cy = thumb_y + thumb_h + 8
    draw.text((dos_x + 16, cy), "SUBTERRANEAN COMMAND REDOUBT", font=f_bold, fill=(255, 220, 90))
    draw.text((dos_x + 16, cy + 18), "GRANITE COMMAND // CORE_BUNKER", font=f_sub, fill=(140, 175, 210))

    # Garrison tac-card
    g_y = cy + 36
    draw.rectangle([dos_x + 16, g_y, dos_x + dos_w - 16, g_y + 64], fill=(12, 18, 28), outline=(40, 75, 115))
    draw_tactical_counter(im, draw, dos_x + 46, g_y + 36, "faction_a", "spr_mini_ms_commander", 4, scale=1.1)
    draw.text((dos_x + 78, g_y + 8), "COMMAND DIVISION MS CADRE", font=f_bold, fill=(255, 255, 255))
    draw.text((dos_x + 78, g_y + 24), "GARRISON STRENGTH: [4] UNITS", font=f_sub, fill=(0, 240, 255))
    draw.text((dos_x + 78, g_y + 42), "★ PRIMARY HQ REACTOR CORE", font=f_sub, fill=(160, 190, 220))

    # Controller box
    cbox_y = cy + 108
    draw.rectangle([dos_x + 16, cbox_y, dos_x + dos_w - 16, cbox_y + 44], fill=(14, 22, 32), outline=(60, 140, 255))
    draw.rectangle([dos_x + 16, cbox_y, dos_x + 20, cbox_y + 44], fill=(60, 140, 255))
    draw.text((dos_x + 26, cbox_y + 6), "CONTROLLER: Federal Terran Garrison", font=f_bold, fill=(60, 140, 255))
    draw.text((dos_x + 26, cbox_y + 24), "BASE SECTOR FORTIFICATION BONUS: +95 DEF", font=f_sub, fill=(80, 255, 140))

    # Fortification rating
    def_y = cbox_y + 52
    draw.text((dos_x + 16, def_y), "PERIMETER FORTIFICATION: 95 / 100", font=f_bold, fill=(200, 220, 245))
    draw.rectangle([dos_x + 16, def_y + 18, dos_x + dos_w - 16, def_y + 28], fill=(20, 28, 40), outline=(50, 80, 120))
    d_fill = int((dos_w - 32) * 0.95)
    draw.rectangle([dos_x + 16, def_y + 18, dos_x + 16 + d_fill, def_y + 28], fill=(255, 215, 60))

    # Lore
    draw.text((dos_x + 16, def_y + 36), "Excavated three thousand meters beneath ancient granite. Central HQ\nand heavy fusion reactor core. Interdicted by perimeter river sentries.", font=f_sub, fill=(160, 190, 220))

    # Actions
    act_y = dos_y + dos_h - 100
    act_w = dos_w - 32
    draw_snes_button(draw, dos_x + 16, act_y, act_w, 32, ">> FORTIFY PERIMETER (+10 DEF: $20K) >>", is_hov=False, is_sel=False, col=(80, 240, 140))
    draw_snes_button(draw, dos_x + 16, act_y + 40, act_w, 34, "⚔️ SORTIE COMBAT SQUAD HERE", is_hov=True, is_sel=False, col=(255, 100, 100))

    draw_bottom_hegemony(draw)

    out_p = os.path.join(brain_dir, "live_earth_tier2_stronghold_granite_deep.png")
    im.save(out_p)
    print("Saved Tier 2 Stronghold Base Map to:", out_p)

if __name__ == "__main__":
    render_tier1_global()
    render_tier2_stronghold()
