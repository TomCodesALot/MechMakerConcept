from PIL import Image, ImageDraw, ImageFont
import os, re

brain_dir = "/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e"
units_dir = os.path.join(brain_dir, "tactical_units")
gw, gh = 1366, 768

try:
    f_title = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 13)
    f_sub = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 10)
    f_bold = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 11)
    f_badge = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 10)
    f_hud = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf", 11)
except:
    f_title = f_sub = f_bold = f_badge = f_hud = ImageFont.load_default()

with open("scripts/scr_territory_war_system/scr_territory_war_system.gml") as f:
    gml_text = f.read()

entries = re.findall(r"_db\.(\w+)\s*=\s*\{([^}]+)\};", gml_text, re.DOTALL)
all_nodes = {}
for tid, body in entries:
    reg = re.search(r"region:\s*\"([^\"]+)\"", body).group(1)
    name = re.search(r"name:\s*\"([^\"]+)\"", body).group(1)
    subreg = re.search(r"subregion:\s*\"([^\"]+)\"", body).group(1)
    fac = re.search(r"controlling_faction:\s*\"([^\"]+)\"", body).group(1)
    mx = int(re.search(r"map_x:\s*(\d+)", body).group(1))
    my = int(re.search(r"map_y:\s*(\d+)", body).group(1))
    conns = [c.strip().replace("\"", "") for c in re.search(r"connected_ids:\s*\[([^\]]+)\]", body).group(1).split(",") if c.strip()]
    def_r = int(re.search(r"defense_rating:\s*(\d+)", body).group(1))
    loc_spr = re.search(r"loc_sprite_name:\s*\"([^\"]+)\"", body).group(1)
    garr_title = re.search(r"garrison_unit:\s*\"([^\"]+)\"", body).group(1)
    
    rad_x, rad_y = 16, 98
    sx = rad_x + 40 + int(mx * 1.34)
    sy = rad_y + 48 + int(my * 1.48)
    all_nodes[tid] = {
        "id": tid, "name": name, "subregion": subreg, "reg": reg, "fac": fac,
        "sx": sx, "sy": sy, "conns": conns, "def": def_r, "loc_spr": loc_spr, "garr": garr_title
    }

def get_spec(fac, def_r, reg):
    if fac == "faction_a":
        if reg == "EARTH": return "spr_mini_veh_heavy_tank", max(4, def_r // 11), "MB-88 Goliath Tanks"
        return "spr_mini_ms_ironclad", max(3, def_r // 14), "GHA-07 Ironclad MS"
    if fac == "faction_b":
        if reg == "EARTH": return "spr_mini_veh_gunship", max(3, def_r // 13), "SV-13 Wyvern Gunships"
        return "spr_mini_ms_aerostriker", max(3, def_r // 14), "Aero-Striker Wings"
    if fac == "faction_c":
        if reg == "EARTH": return "spr_mini_veh_technical", max(4, def_r // 10), "ATV-4 Recon Technicals"
        return "spr_mini_ms_artillery", max(2, def_r // 16), "Mammoth-Tread MS"
    if fac == "faction_d":
        return "spr_mini_ms_hoversniper", max(3, def_r // 15), "Specter Hover Railguns"
    if fac == "faction_e":
        if reg == "EARTH": return "spr_mini_inf_exo_squad", max(4, def_r // 10), "Exo-Shock Troopers"
        return "spr_mini_veh_dropship", max(2, def_r // 18), "Skyhook Fleet Escorts"
    if fac == "faction_f":
        return "spr_mini_ms_commander", max(3, def_r // 12), "Autonomous Hegemon MS"
    return "spr_mini_ms_grunt", max(4, def_r // 12), "Iron Ridge Custom Lance"

def paste_tac_counter(canvas, cx, cy, fac, unit_spr_name, stack_val, is_sel=False, scale=0.9):
    b_map = {
        "faction_a": "spr_hex_base_terran", "faction_b": "spr_hex_base_colony",
        "faction_c": "spr_hex_base_syndicate", "faction_d": "spr_hex_base_zaibatsu",
        "faction_e": "spr_hex_base_sidereal", "faction_f": "spr_hex_base_mars",
        "pmc": "spr_hex_base_pmc"
    }
    b_file = b_map.get(fac, "spr_hex_base_pmc") + ".png"
    u_file = unit_spr_name + ".png"
    
    im_b = Image.open(os.path.join(units_dir, b_file)).convert("RGBA")
    im_u = Image.open(os.path.join(units_dir, u_file)).convert("RGBA")
    
    bw, bh = int(46 * scale), int(34 * scale)
    im_b_sc = im_b.resize((bw, bh), Image.Resampling.LANCZOS)
    canvas.paste(im_b_sc, (cx - bw//2, cy - bh//2 + int(4 * scale)), im_b_sc)
    
    uw, uh = int(44 * scale), int(44 * scale)
    im_u_sc = im_u.resize((uw, uh), Image.Resampling.LANCZOS)
    canvas.paste(im_u_sc, (cx - uw//2, cy - uh + int(8 * scale)), im_u_sc)
    
    bx, by = cx + int(8 * scale), cy + int(2 * scale)
    bw_bg, bh_bg = int(14 * scale), int(16 * scale)
    cdraw = ImageDraw.Draw(canvas)
    cdraw.rectangle([(bx, by), (bx + bw_bg, by + bh_bg)], fill=(8, 14, 22, 255), outline=(0, 240, 255, 255))
    cdraw.text((bx + 3, by + 1), str(stack_val), fill=(0, 255, 220, 255), font=f_badge)
    
    if is_sel:
        im_br = Image.open(os.path.join(units_dir, "spr_tactical_bracket.png")).convert("RGBA")
        brw, brh = int(56 * scale), int(42 * scale)
        im_br_sc = im_br.resize((brw, brh), Image.Resampling.LANCZOS)
        canvas.paste(im_br_sc, (cx - brw//2, cy - brh//2 - int(4 * scale)), im_br_sc)

theaters = [
    ("SPACE", "space_kepler_haven", "sprites/spr_map_space_theater/spr_map_space_theater.png", "live_space_colony_theater_verified.png", 0),
    ("EARTH", "earth_granite_redoubt", "sprites/spr_map_earth_theater/spr_map_earth_theater.png", "live_earth_theater_verified.png", 1),
    ("MARS", "mars_olympus_caldera", "sprites/spr_map_mars_theater/spr_map_mars_theater.png", "live_mars_theater_verified.png", 2)
]

for reg_name, sel_id, bg_path, out_file, tab_idx in theaters:
    im = Image.new("RGBA", (gw, gh), (8, 12, 18, 255))
    draw = ImageDraw.Draw(im)
    
    # Grid
    for gx in range(0, gw, 48): draw.line([(gx, 0), (gx, gh)], fill=(16, 24, 36, 255))
    for gy in range(0, gh, 48): draw.line([(0, gy), (gw, gy)], fill=(16, 24, 36, 255))
    
    # Top Bar
    draw.rectangle([(16, 6), (gw - 16, 54)], fill=(12, 18, 28, 255), outline=(35, 60, 95, 255))
    draw.rectangle([(16, 6), (20, 54)], fill=(0, 220, 255, 255))
    draw.text((28, 14), "IRON RIDGE PMC // GALACTIC THEATER WAR MAP", fill=(0, 240, 255, 255), font=f_title)
    draw.text((28, 32), "TACTICAL COMMAND & FACTION CONQUEST SYSTEM", fill=(140, 175, 215, 255), font=f_sub)
    
    # Buttons
    draw.rectangle([(832, 12), (1008, 48)], fill=(12, 38, 22, 255), outline=(45, 190, 100, 255))
    draw.text((844, 22), ">> ADVANCE DAY [SPACE]", fill=(255, 255, 255, 255), font=f_bold)
    draw.rectangle([(1016, 12), (1170, 48)], fill=(38, 24, 8, 255), outline=(210, 150, 40, 255))
    draw.text((1026, 22), "⚔️ SORTIE [S]", fill=(255, 225, 100, 255), font=f_bold)
    draw.rectangle([(1178, 12), (1256, 48)], fill=(12, 32, 22, 255), outline=(50, 190, 100, 255))
    draw.text((1186, 22), "[🔊 100%]", fill=(130, 255, 170, 255), font=f_bold)
    draw.rectangle([(1262, 12), (1350, 48)], fill=(12, 22, 34, 255), outline=(55, 130, 190, 255))
    draw.text((1270, 22), "[⚙ CONFIG]", fill=(120, 220, 255, 255), font=f_bold)
    
    # Theater Tabs
    tab_defs = [
        ("[1. SPACE & COLONIES // 15 SECTORS]", 16),
        ("[2. EARTH SPHERE // 10 CITADELS]", 326),
        ("[3. MARS & ASTEROIDS // 8 REDOUBTS]", 636)
    ]
    for idx, (lbl, bx) in enumerate(tab_defs):
        is_act = (idx == tab_idx)
        fill_col = (28, 62, 98, 255) if is_act else (12, 18, 28, 255)
        border_col = (0, 240, 255, 255) if is_act else (40, 70, 105, 255)
        draw.rectangle([(bx, 60), (bx + 300, 92)], fill=fill_col, outline=border_col)
        draw.text((bx + 14, 68), lbl, fill=(255, 255, 255, 255) if is_act else (160, 190, 220, 255), font=f_bold)
    
    # Radar Canvas
    rad_x, rad_y, rad_w, rad_h = 16, 98, 954, 596
    draw.rectangle([(rad_x, rad_y), (rad_x + rad_w, rad_y + rad_h)], fill=(10, 16, 24, 255), outline=(60, 180, 240, 255), width=2)
    
    if os.path.exists(bg_path):
        bg_im = Image.open(bg_path).convert("RGBA").resize((rad_w - 24, rad_h - 38), Image.Resampling.LANCZOS)
        # Moderate tint so the gorgeous topography shines through
        bg_dim = Image.new("RGBA", bg_im.size, (0, 0, 0, 60))
        bg_im = Image.alpha_composite(bg_im, bg_dim)
        im.paste(bg_im, (rad_x + 12, rad_y + 26), bg_im)
    
    # Filter nodes for this region
    reg_nodes = {tid: n for tid, n in all_nodes.items() if n["reg"] == reg_name}
    
    # 1. Hyperlanes & Assault Arrows
    drawn_edges = set()
    for tid, n in reg_nodes.items():
        for cid in n["conns"]:
            if cid in reg_nodes:
                edge = tuple(sorted([tid, cid]))
                if edge in drawn_edges: continue
                drawn_edges.add(edge)
                n2 = reg_nodes[cid]
                is_cont = (n["fac"] != n2["fac"])
                col = (255, 60, 70, 255) if is_cont else (0, 160, 210, 140)
                w = 3 if is_cont else 1
                draw.line([(n["sx"], n["sy"]), (n2["sx"], n2["sy"])], fill=col, width=w)
                
                # If contested: Draw attack engagement arrow and patrol unit
                if is_cont:
                    mid_x = (n["sx"] + n2["sx"]) // 2
                    mid_y = (n["sy"] + n2["sy"]) // 2
                    draw.line([(mid_x - 12, mid_y), (mid_x + 12, mid_y)], fill=(255, 130, 190, 255), width=3)
                    draw.polygon([(mid_x + 12, mid_y - 6), (mid_x + 22, mid_y), (mid_x + 12, mid_y + 6)], fill=(255, 130, 190, 255))
    
    # 2. Draw Nodes with Hex Influence Zones
    for tid, n in reg_nodes.items():
        is_sel = (tid == sel_id)
        uspr, stk, ulabel = get_spec(n["fac"], n["def"], reg_name)
        
        # Draw translucent hex influence
        f_colors = {
            "faction_a": (60, 140, 255, 60), "faction_b": (40, 220, 180, 60),
            "faction_c": (255, 160, 40, 60), "faction_d": (180, 90, 240, 60),
            "faction_e": (120, 130, 240, 60), "faction_f": (240, 60, 60, 60),
            "pmc": (255, 215, 60, 70)
        }
        hcol = f_colors.get(n["fac"], (0, 240, 255, 50))
        for ox, oy in [(0, 0), (-26, -16), (26, -16), (-26, 14), (26, 14)]:
            draw.ellipse([(n["sx"] + ox - 20, n["sy"] + oy - 14), (n["sx"] + ox + 20, n["sy"] + oy + 14)], fill=hcol, outline=hcol)
        
        # Paste Tactical Counter
        paste_tac_counter(im, n["sx"], n["sy"] - 4, n["fac"], uspr, stk, is_sel, 1.05)
        
        # Nameplate
        nb_w, nb_h = 98, 18
        nb_y = n["sy"] + 16
        draw.rectangle([(n["sx"] - nb_w//2, nb_y), (n["sx"] + nb_w//2, nb_y + nb_h)], fill=(12, 22, 34, 255), outline=(0, 240, 255, 255) if is_sel else (45, 80, 120, 255))
        disp = n["name"][:13]
        draw.text((n["sx"] - nb_w//2 + 8, nb_y + 2), disp, fill=(255, 255, 255, 255) if is_sel else (190, 215, 240, 255), font=f_sub)
    
    # 3. Minimap in Top-Right
    mm_w, mm_h = 210, 118
    mm_x = rad_x + rad_w - mm_w - 18
    mm_y = rad_y + 36
    draw.rectangle([(mm_x, mm_y), (mm_x + mm_w, mm_y + mm_h)], fill=(8, 14, 22, 230), outline=(45, 80, 125, 255), width=2)
    
    if reg_name == "EARTH":
        amb_path = os.path.join(brain_dir, "radar_earth_amber_screen.png")
        if os.path.exists(amb_path):
            amb_im = Image.open(amb_path).convert("RGBA").resize((mm_w - 4, mm_h - 4), Image.Resampling.LANCZOS)
            im.paste(amb_im, (mm_x + 2, mm_y + 2), amb_im)
        draw.text((mm_x + 8, mm_y + 6), "TERRESTRIAL SATELLITE RADAR", fill=(255, 215, 80, 255), font=f_sub)
        draw.rectangle([(mm_x + 48, mm_y + 54), (mm_x + 88, mm_y + 92)], outline=(0, 240, 255, 255), width=2)
    elif reg_name == "MARS":
        mars_m_im = Image.open("sprites/spr_map_mars_theater/spr_map_mars_theater.png").convert("RGBA").resize((mm_w - 4, mm_h - 4), Image.Resampling.LANCZOS)
        im.paste(mars_m_im, (mm_x + 2, mm_y + 2), mars_m_im)
        draw.text((mm_x + 8, mm_y + 6), "THARSIS SATELLITE TELEMETRY", fill=(255, 90, 80, 255), font=f_sub)
        draw.rectangle([(mm_x + 38, mm_y + 28), (mm_x + 92, mm_y + 76)], outline=(0, 240, 255, 255), width=2)
    else:
        draw.text((mm_x + 8, mm_y + 6), "SOL ORBITAL TELEMETRY", fill=(0, 240, 255, 255), font=f_sub)
        mcx, mcy = mm_x + 105, mm_y + 68
        draw.ellipse([(mcx - 78, mcy - 38), (mcx + 78, mcy + 38)], outline=(25, 45, 75, 255))
        draw.ellipse([(mcx - 50, mcy - 24), (mcx + 50, mcy + 24)], outline=(25, 45, 75, 255))
        draw.ellipse([(mcx - 4, mcy - 4), (mcx + 4, mcy + 4)], fill=(255, 215, 80, 255))
        draw.ellipse([(mcx + 44, mcy - 14), (mcx + 50, mcy - 8)], fill=(60, 150, 255, 255))
        draw.rectangle([(mcx + 30, mcy - 24), (mcx + 68, mcy + 2)], outline=(0, 240, 255, 255), width=2)
    
    # 4. Terrain HUD Box in Bottom-Right
    thud_w, thud_h = 236, 92
    thud_x = rad_x + rad_w - thud_w - 18
    thud_y = rad_y + rad_h - thud_h - 18
    draw.rectangle([(thud_x, thud_y), (thud_x + thud_w, thud_y + thud_h)], fill=(222, 226, 236, 255), outline=(28, 40, 56, 255), width=2)
    draw.rectangle([(thud_x + 3, thud_y + 3), (thud_x + thud_w - 3, thud_y + 24)], fill=(240, 244, 252, 255))
    terr_label = "TERRESTRIAL CRATON" if reg_name == "EARTH" else ("MARTIAN BASALT" if reg_name == "MARS" else "ORBITAL VACUUM")
    draw.text((thud_x + 10, thud_y + 6), terr_label, fill=(12, 22, 36, 255), font=f_hud)
    draw.text((thud_x + 10, thud_y + 30), "DEFENSE BONUS", fill=(25, 35, 50, 255), font=f_hud)
    draw.text((thud_x + thud_w - 55, thud_y + 30), "+20 %", fill=(0, 110, 180, 255), font=f_hud)
    draw.text((thud_x + 10, thud_y + 48), "SENSOR DENSITY", fill=(25, 35, 50, 255), font=f_hud)
    draw.text((thud_x + thud_w - 55, thud_y + 48), "00 %", fill=(25, 35, 50, 255), font=f_hud)
    draw.text((thud_x + 10, thud_y + 68), "GARRISON SQUAD", fill=(25, 35, 50, 255), font=f_hud)
    draw.text((thud_x + thud_w - 55, thud_y + 68), "06 MS", fill=(190, 40, 25, 255), font=f_hud)
    
    # 5. Sector Dossier on Right Panel
    dos_x, dos_y, dos_w, dos_h = 982, 98, gw - 982 - 16, rad_h
    draw.rectangle([(dos_x, dos_y), (dos_x + dos_w, dos_y + dos_h)], fill=(12, 18, 28, 255), outline=(100, 200, 255, 255), width=2)
    draw.text((dos_x + 16, dos_y + 8), "TACTICAL SECTOR DOSSIER", fill=(100, 200, 255, 255), font=f_bold)
    
    sel_node = all_nodes[sel_id]
    thumb_y = dos_y + 26
    thumb_w = dos_w - 32
    thumb_h = 130
    loc_file = f"sprites/{sel_node['loc_spr']}/{sel_node['loc_spr']}.png"
    if os.path.exists(loc_file):
        loc_im = Image.open(loc_file).convert("RGBA").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        im.paste(loc_im, (dos_x + 16, thumb_y), loc_im)
    draw.rectangle([(dos_x + 16, thumb_y), (dos_x + 16 + thumb_w, thumb_y + thumb_h)], outline=(0, 220, 255, 255), width=1)
    
    content_y = thumb_y + thumb_h + 8
    draw.text((dos_x + 16, content_y), sel_node["name"].upper(), fill=(255, 220, 90, 255), font=f_bold)
    draw.text((dos_x + 16, content_y + 18), f"{reg_name} // {sel_node['subregion']}", fill=(140, 175, 210, 255), font=f_sub)
    
    # Tac-Card
    gcard_y = content_y + 36
    gcard_h = 64
    draw.rectangle([(dos_x + 16, gcard_y), (dos_x + dos_w - 16, gcard_y + gcard_h)], fill=(12, 18, 28, 255), outline=(40, 75, 115, 255))
    uspr_sel, stk_sel, ulabel_sel = get_spec(sel_node["fac"], sel_node["def"], reg_name)
    paste_tac_counter(im, dos_x + 46, gcard_y + 42, sel_node["fac"], uspr_sel, stk_sel, is_sel=True, scale=1.15)
    draw.text((dos_x + 78, gcard_y + 8), ulabel_sel.upper(), fill=(255, 255, 255, 255), font=f_bold)
    draw.text((dos_x + 78, gcard_y + 24), f"SQUADRON STRENGTH: [{stk_sel}] UNITS", fill=(0, 240, 255, 255), font=f_sub)
    draw.text((dos_x + 78, gcard_y + 42), sel_node["garr"], fill=(160, 190, 220, 255), font=f_sub)
    
    # Bottom Hegemony bar
    bot_y = 704
    bot_w = gw - 32
    draw.rectangle([(16, bot_y), (16 + bot_w, bot_y + 52)], fill=(10, 16, 24, 255), outline=(35, 60, 90, 255))
    bar_w = bot_w - 28
    bar_y = bot_y + 8
    draw.rectangle([(30, bar_y), (30 + bar_w, bar_y + 14)], fill=(20, 25, 35, 255))
    segs = [(int(bar_w * 0.20), (60, 140, 255)), (int(bar_w * 0.20), (40, 220, 180)), (int(bar_w * 0.20), (255, 160, 40)), (int(bar_w * 0.20), (180, 90, 240)), (int(bar_w * 0.20), (120, 130, 240))]
    cx = 30
    for sw, sc in segs:
        draw.rectangle([(cx, bar_y), (cx + sw, bar_y + 14)], fill=sc)
        cx += sw
    draw.text((34, bar_y + 20), "HEGEMONY PARITY: Terran: 20%  |  Colony: 20%  |  Syndicate: 20%  |  Zaibatsu: 20%  |  Sidereal: 20%  |  Mars: 0%  |  PMC: 0%", fill=(180, 210, 240, 255), font=f_sub)
    
    full_out = os.path.join(brain_dir, out_file)
    im.save(full_out)
    print(f"✓ Rendered verified live view for {reg_name} -> {full_out}")

print("All 3 theaters rendered successfully!")
