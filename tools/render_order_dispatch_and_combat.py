from PIL import Image, ImageDraw, ImageFont
import os, re, math

brain_dir = "/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e"
units_dir = os.path.join(brain_dir, "tactical_units")
gw, gh = 1366, 768

try:
    f_title = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 13)
    f_sub = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 10)
    f_bold = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 11)
    f_badge = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 10)
    f_hud = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf", 11)
    f_modal_h = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 14)
    f_modal_body = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 12)
    f_modal_bold = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 12)
except:
    f_title = f_sub = f_bold = f_badge = f_hud = f_modal_h = f_modal_body = f_modal_bold = ImageFont.load_default()

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

def get_faction_colors(fac):
    colors = {
        "pmc": (255, 215, 60),
        "faction_a": (60, 140, 255),
        "faction_b": (40, 220, 180),
        "faction_c": (255, 160, 40),
        "faction_d": (180, 90, 240),
        "faction_e": (120, 130, 240),
        "faction_f": (240, 60, 60)
    }
    return colors.get(fac, (180, 180, 180))

def get_unit_spec(fac, def_r):
    if fac == "pmc": return "spr_mini_ms_ironclad", 4, "GHA-07 Ironclad MS"
    if fac == "faction_a":
        if def_r >= 85: return "spr_mini_ms_commander", 3, "Apex Commander MS"
        return "spr_mini_veh_heavy_tank", 6, "MB-88 Goliath Armor"
    if fac == "faction_b":
        if def_r >= 80: return "spr_mini_ms_aerostriker", 4, "Aero-Striker MS"
        return "spr_mini_veh_gunship", 6, "Wyvern Gunship Wing"
    if fac == "faction_c":
        return "spr_mini_veh_technical", 8, "ATV-4 Strike Techs"
    if fac == "faction_d":
        return "spr_mini_ms_hoversniper", 4, "Kurogane Hover-Sniper"
    if fac == "faction_e":
        return "spr_mini_ms_artillery", 4, "Heavy Artillery MS"
    return "spr_mini_ms_grunt", 5, "Standard Combat Unit"

def draw_hex(draw, cx, cy, r, fill, outline=None):
    pts = []
    for i in range(6):
        angle = math.radians(60 * i)
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        pts.append((px, py))
    draw.polygon(pts, fill=fill, outline=outline)

# -------------------------------------------------------------------------
# RENDER SCREEN 1: ORDER DISPATCH MODE ACTIVE ON SPACE THEATER
# -------------------------------------------------------------------------
def render_order_dispatch_screen():
    im = Image.new("RGBA", (gw, gh), (8, 12, 18, 255))
    draw = ImageDraw.Draw(im)

    # Master Space Background Map
    bg_p = "sprites/spr_map_space_theater/spr_map_space_theater.png"
    if os.path.exists(bg_p):
        bg = Image.open(bg_p).convert("RGBA").resize((930, 558))
        im.paste(bg, (28, 124), bg)

    # Coordinate grid
    for x in range(0, gw, 48): draw.line([(x, 0), (x, gh)], fill=(16, 24, 36, 120))
    for y in range(0, gh, 48): draw.line([(y, 0), (y, gh)], fill=(16, 24, 36, 120))

    # Top Header
    draw.rectangle([16, 6, gw - 16, 54], fill=(12, 18, 28), outline=(35, 60, 95))
    draw.rectangle([16, 6, 20, 54], fill=(0, 220, 255))
    draw.text((26, 14), "IRON RIDGE PMC // COMMAND DECK", font=f_bold, fill=(0, 240, 255))
    draw.text((26, 32), "TACTICAL HEADQUARTERS // WAR ROOM CENTERPIECE", font=f_sub, fill=(140, 175, 215))

    # Funds & Cycle
    draw.rectangle([216, 12, 350, 48], fill=(14, 28, 20), outline=(30, 90, 50))
    draw.text((224, 22), "100,000 Cr", font=f_bold, fill=(80, 240, 140))
    draw.rectangle([356, 12, 476, 48], fill=(20, 26, 38), outline=(45, 70, 105))
    draw.text((364, 22), "Y214 · D1 [T-1]", font=f_bold, fill=(255, 215, 80))

    # HQ Deck Tabs
    decks = [("WAR MAP", True), ("R&D BAY", False), ("FACTORY", False), ("CONTRACTS", False), ("FLEET", False)]
    dx0 = 486
    for i, (dname, dact) in enumerate(decks):
        bx = dx0 + i * 96
        draw.rectangle([bx, 12, bx + 92, 48], fill=(24, 60, 96) if dact else (12, 18, 28), outline=(0, 240, 255) if dact else (35, 65, 95))
        if dact: draw.rectangle([bx, 12, bx + 92, 15], fill=(0, 240, 255))
        draw.text((bx + 12, 22), dname, font=f_bold, fill=(255, 255, 255) if dact else (150, 180, 210))

    # Action buttons
    draw.rectangle([980, 12, 1120, 48], fill=(20, 70, 40), outline=(80, 255, 150))
    draw.text((990, 22), ">> ADVANCE DAY", font=f_bold, fill=(255, 255, 255))
    draw.rectangle([1126, 12, 1216, 48], fill=(80, 50, 10), outline=(255, 210, 60))
    draw.text((1136, 22), "⚔️ SORTIE", font=f_bold, fill=(255, 225, 100))
    draw.rectangle([1222, 12, 1276, 48], fill=(12, 32, 22), outline=(50, 190, 100))
    draw.text((1234, 22), "[🔊]", font=f_bold, fill=(130, 255, 170))
    draw.rectangle([1282, 12, 1348, 48], fill=(12, 22, 34), outline=(55, 130, 190))
    draw.text((1294, 22), "[⚙ CFG]", font=f_bold, fill=(120, 220, 255))

    # Theater Tabs
    th_tabs = [("[1. SPACE & COLONIES // 15 SECTORS]", True), ("[2. EARTH SPHERE // 10 CITADELS]", False), ("[3. MARS & ASTEROIDS // 8 REDOUBTS]", False)]
    for ti, (tname, tact) in enumerate(th_tabs):
        bx = 16 + ti * 314
        draw.rectangle([bx, 60, bx + 304, 92], fill=(28, 62, 98) if tact else (10, 16, 26), outline=(0, 240, 255) if tact else (35, 60, 95))
        draw.text((bx + 18, 68), tname, font=f_bold, fill=(255, 255, 255) if tact else (140, 175, 210))

    # ORDER DISPATCH STATUS RIBBON
    draw.rectangle([16, 96, 970, 118], fill=(160, 120, 10), outline=(255, 220, 60))
    draw.text((26, 100), "⚡ TACTICAL DISPATCH MODE ACTIVE: SELECT AN ADJACENT CONNECTED DESTINATION NODE TO ISSUE SQUADRON DIRECTIVE   [ESC TO CANCEL]", font=f_bold, fill=(255, 255, 255))

    # Radar Panel
    rad_x, rad_y, rad_w, rad_h = 16, 122, 954, 572
    draw.rectangle([rad_x, rad_y, rad_x + rad_w, rad_y + rad_h], outline=(60, 180, 240))

    origin_id = "space_kepler_haven"
    orig_node = all_nodes[origin_id]

    # Hyperlanes
    for nid, node in all_nodes.items():
        if node["reg"] != "SPACE": continue
        for cid in node["conns"]:
            if cid in all_nodes and all_nodes[cid]["reg"] == "SPACE":
                cnode = all_nodes[cid]
                # If connected to origin, highlight!
                if nid == origin_id or cid == origin_id:
                    draw.line([(node["sx"], node["sy"]), (cnode["sx"], cnode["sy"])], fill=(255, 220, 60), width=3)
                    # Chevron marker
                    cx = (node["sx"] + cnode["sx"]) // 2
                    cy = (node["sy"] + cnode["sy"]) // 2
                    draw.polygon([(cx - 6, cy - 6), (cx + 6, cy), (cx - 6, cy + 6)], fill=(255, 240, 120))
                else:
                    draw.line([(node["sx"], node["sy"]), (cnode["sx"], cnode["sy"])], fill=(0, 160, 210), width=1)

    # Nodes
    for nid, node in all_nodes.items():
        if node["reg"] != "SPACE": continue
        nx, ny = node["sx"], node["sy"]
        fcol = get_faction_colors(node["fac"])

        # Hex cluster
        draw_hex(draw, nx, ny - 4, 22, fill=(fcol[0], fcol[1], fcol[2], 60))
        draw_hex(draw, nx - 26, ny - 18, 16, fill=(fcol[0], fcol[1], fcol[2], 40))
        draw_hex(draw, nx + 26, ny - 18, 16, fill=(fcol[0], fcol[1], fcol[2], 40))

        # Check order origin vs target
        is_origin = (nid == origin_id)
        is_target = (nid in orig_node["conns"])

        if is_origin:
            draw.ellipse([nx - 32, ny - 36, nx + 32, ny + 28], outline=(255, 215, 60), width=3)
            draw.rectangle([nx - 52, ny - 50, nx + 52, ny - 34], fill=(20, 14, 8), outline=(255, 215, 60))
            draw.text((nx - 46, ny - 48), "[ORDER ORIGIN]", font=f_badge, fill=(255, 225, 100))
        elif is_target:
            tcol = (80, 255, 140) if node["fac"] == "pmc" else (255, 90, 80)
            draw.ellipse([nx - 30, ny - 34, nx + 30, ny + 26], outline=tcol, width=2)
            draw.rectangle([nx - 56, ny - 48, nx + 56, ny - 32], fill=(12, 18, 28), outline=tcol)
            draw.text((nx - 50, ny - 46), ">> TARGET ASSAULT >>", font=f_badge, fill=tcol)

        # Tactical chit
        plinth_name = f"spr_hex_base_{node['fac'] if node['fac'] != 'faction_a' else 'terran'}.png"
        plinth_p = os.path.join(units_dir, plinth_name)
        if os.path.exists(plinth_p):
            pl = Image.open(plinth_p).convert("RGBA")
            im.paste(pl, (nx - pl.width // 2, ny - pl.height // 2 + 6), pl)

        spr_name, stack, ulabel = get_unit_spec(node["fac"], node["def"])
        ms_p = os.path.join(units_dir, spr_name + ".png")
        if os.path.exists(ms_p):
            ms = Image.open(ms_p).convert("RGBA")
            im.paste(ms, (nx - ms.width // 2, ny - ms.height // 2 - 8), ms)

        # Badge
        draw.rectangle([nx + 10, ny - 2, nx + 24, ny + 12], fill=(10, 16, 26), outline=(255, 215, 60))
        draw.text((nx + 14, ny), str(stack), font=f_badge, fill=(255, 215, 60))

        # Nameplate
        draw.rectangle([nx - 46, ny + 18, nx + 46, ny + 34], fill=(10, 16, 26), outline=(0, 240, 255) if is_origin else (45, 80, 120))
        draw.text((nx - 40, ny + 20), node["name"][:14], font=f_badge, fill=(255, 255, 255))

    # ACTIVE TRANSIT CHIT (Striking across Hyperlane from Selene Zenith to Daedalus)
    tr_ox, tr_oy = all_nodes["space_selene_zenith"]["sx"], all_nodes["space_selene_zenith"]["sy"]
    tr_tx, tr_ty = all_nodes["space_daedalus_foundry"]["sx"], all_nodes["space_daedalus_foundry"]["sy"]
    tr_cx = int(tr_ox + (tr_tx - tr_ox) * 0.45)
    tr_cy = int(tr_oy + (tr_ty - tr_oy) * 0.45)

    draw.line([(tr_ox, tr_oy), (tr_tx, tr_ty)], fill=(0, 240, 255), width=3)
    ms_iron = Image.open(os.path.join(units_dir, "spr_mini_ms_ironclad.png")).convert("RGBA")
    im.paste(ms_iron, (tr_cx - 24, tr_cy - 30), ms_iron)
    draw.rectangle([tr_cx - 44, tr_cy - 44, tr_cx + 44, tr_cy - 30], fill=(10, 16, 26), outline=(0, 240, 255))
    draw.text((tr_cx - 40, tr_cy - 42), "TRANSIT WING [4]", font=f_badge, fill=(0, 240, 255))

    # Minimap in Top Right of radar
    mm_x, mm_y, mm_w, mm_h = rad_x + rad_w - 188, rad_y + 12, 176, 102
    draw.rectangle([mm_x, mm_y, mm_x + mm_w, mm_y + mm_h], fill=(10, 16, 24), outline=(45, 80, 120))
    draw.text((mm_x + 8, mm_y + 6), "SOL ORBITAL TELEMETRY", font=f_badge, fill=(0, 240, 255))
    draw.ellipse([mm_x + mm_w//2 - 24, mm_y + mm_h//2 - 24, mm_x + mm_w//2 + 24, mm_y + mm_h//2 + 24], outline=(0, 180, 220))
    draw.ellipse([mm_x + mm_w//2 - 40, mm_y + mm_h//2 - 40, mm_x + mm_w//2 + 40, mm_y + mm_h//2 + 40], outline=(40, 80, 120))
    draw.rectangle([mm_x + 48, mm_y + 40, mm_x + 92, mm_y + 74], outline=(0, 255, 255), width=2)

    # Telemetry HUD
    hud_x, hud_y = rad_x + rad_w - 210, rad_y + rad_h - 84
    draw.rectangle([hud_x, hud_y, hud_x + 196, hud_y + 72], fill=(10, 16, 26), outline=(35, 60, 90))
    draw.rectangle([hud_x, hud_y, hud_x + 196, hud_y + 20], fill=(20, 36, 56))
    draw.text((hud_x + 8, hud_y + 4), "ORBITAL VACUUM", font=f_hud, fill=(255, 255, 255))
    draw.text((hud_x + 8, hud_y + 26), "DEFENSE BONUS:  +20%", font=f_hud, fill=(200, 225, 250))
    draw.text((hud_x + 8, hud_y + 44), "SENSOR DENSITY:  00%", font=f_hud, fill=(200, 225, 250))

    # Dossier Panel on Right
    dos_x, dos_y, dos_w, dos_h = 982, 122, 368, 572
    draw.rectangle([dos_x, dos_y, dos_x + dos_w, dos_y + dos_h], outline=(100, 200, 255))
    draw.rectangle([dos_x, dos_y, dos_x + dos_w, dos_y + 24], fill=(20, 44, 70))
    draw.text((dos_x + 12, dos_y + 4), "TACTICAL SECTOR DOSSIER", font=f_bold, fill=(0, 240, 255))

    # Spot art
    cyl_p = "sprites/spr_loc_colony_cylinder/spr_loc_colony_cylinder.png"
    if os.path.exists(cyl_p):
        cyl = Image.open(cyl_p).convert("RGBA").resize((dos_w - 32, 120))
        im.paste(cyl, (dos_x + 16, dos_y + 32), cyl)

    draw.text((dos_x + 16, dos_y + 160), "KEPLER ORBITAL HAVEN (L5)", font=f_title, fill=(255, 215, 60))
    draw.text((dos_x + 16, dos_y + 180), "SPACE // Earth-Moon L5 Trojan Cluster", font=f_sub, fill=(140, 175, 210))

    # Battlegroup Card
    draw.rectangle([dos_x + 16, dos_y + 200, dos_x + dos_w - 16, dos_y + 264], fill=(12, 18, 28), outline=(40, 75, 115))
    im.paste(ms_iron, (dos_x + 28, dos_y + 208), ms_iron)
    draw.text((dos_x + 82, dos_y + 208), "GHA-07 IRONCLAD HEAVY MS", font=f_bold, fill=(255, 255, 255))
    draw.text((dos_x + 82, dos_y + 226), "SQUADRON STRENGTH: [4] UNITS", font=f_bold, fill=(0, 240, 255))
    draw.text((dos_x + 82, dos_y + 244), "Iron Ridge Veteran Garrison Wing", font=f_sub, fill=(160, 190, 220))

    # Controller Banner
    draw.rectangle([dos_x + 16, dos_y + 276, dos_x + dos_w - 16, dos_y + 320], fill=(14, 22, 32), outline=(255, 215, 60))
    draw.rectangle([dos_x + 16, dos_y + 276, dos_x + 20, dos_y + 320], fill=(255, 215, 60))
    draw.text((dos_x + 26, dos_y + 282), "CONTROLLER: PMC Sovereign Dominion (Player)", font=f_bold, fill=(255, 215, 60))
    draw.text((dos_x + 26, dos_y + 300), "DAILY YIELD: +48,000 Cr / +22kg COMPOSITE", font=f_sub, fill=(80, 255, 140))

    # Defense Bar
    draw.text((dos_x + 16, dos_y + 332), "DEFENSE FORTIFICATION: 80 / 100", font=f_bold, fill=(200, 220, 245))
    draw.rectangle([dos_x + 16, dos_y + 350, dos_x + dos_w - 16, dos_y + 360], fill=(20, 28, 40), outline=(50, 80, 120))
    draw.rectangle([dos_x + 16, dos_y + 350, dos_x + 16 + int((dos_w - 32) * 0.8), dos_y + 360], fill=(0, 220, 255))

    # Dossier Buttons
    draw.rectangle([dos_x + 16, dos_y + dos_h - 130, dos_x + dos_w - 16, dos_y + dos_h - 96], fill=(20, 54, 88), outline=(0, 240, 255))
    draw.text((dos_x + 36, dos_y + dos_h - 122), "⚡ ISSUE TACTICAL ORDER / DISPATCH", font=f_bold, fill=(255, 255, 255))

    draw.rectangle([dos_x + 16, dos_y + dos_h - 90, dos_x + dos_w - 16, dos_y + dos_h - 56], fill=(14, 38, 22), outline=(80, 240, 140))
    draw.text((dos_x + 36, dos_y + dos_h - 82), ">> FORTIFY SECTOR (+10 DEF: $25K) >>", font=f_bold, fill=(80, 240, 140))

    draw.rectangle([dos_x + 16, dos_y + dos_h - 50, dos_x + dos_w - 16, dos_y + dos_h - 16], fill=(60, 20, 20), outline=(255, 100, 100))
    draw.text((dos_x + 56, dos_y + dos_h - 42), "⚔️ SORTIE COMBAT SQUAD HERE", font=f_bold, fill=(255, 150, 150))

    # Hegemony strip
    draw.rectangle([16, 704, gw - 16, 756], fill=(10, 16, 24), outline=(35, 60, 90))
    draw.rectangle([30, 712, gw - 30, 726], fill=(20, 25, 35))
    # Segments
    draw.rectangle([30, 712, 30 + 160, 726], fill=(60, 140, 255))
    draw.rectangle([190, 712, 190 + 160, 726], fill=(40, 220, 180))
    draw.rectangle([350, 712, 350 + 140, 726], fill=(255, 160, 40))
    draw.rectangle([490, 712, 490 + 140, 726], fill=(180, 90, 240))
    draw.rectangle([630, 712, 630 + 140, 726], fill=(120, 130, 240))
    draw.rectangle([770, 712, 770 + 200, 726], fill=(240, 60, 60))
    draw.rectangle([970, 712, 970 + 336, 726], fill=(255, 215, 60))
    draw.text((34, 732), "HEGEMONY PARITY: Terran: 18%  |  Colony: 18%  |  Syndicate: 15%  |  Zaibatsu: 15%  |  Sidereal: 15%  |  Mars: 12%  |  PMC: 7%", font=f_sub, fill=(180, 210, 240))

    out_p = os.path.join(brain_dir, "live_order_dispatch_mode.png")
    im.save(out_p)
    print("Saved:", out_p)
    return im

# -------------------------------------------------------------------------
# RENDER SCREEN 2: TACTICAL ORDER DISPATCH CONFIRMATION MODAL
# -------------------------------------------------------------------------
def render_tactical_order_modal(base_im):
    im = base_im.copy()
    draw = ImageDraw.Draw(im)

    # Dark overlay
    overlay = Image.new("RGBA", (gw, gh), (0, 0, 0, 180))
    im.paste(overlay, (0, 0), overlay)

    omw, omh = 660, 430
    omx = (gw - omw) // 2
    omy = (gh - omh) // 2

    # Modal panel
    draw.rectangle([omx, omy, omx + omw, omy + omh], fill=(12, 18, 28), outline=(0, 240, 255), width=2)
    draw.rectangle([omx, omy, omx + omw, omy + 28], fill=(20, 48, 76))
    draw.text((omx + 16, omy + 6), "TACTICAL OPERATION DIRECTIVE // VANGUARD DISPATCH", font=f_modal_h, fill=(0, 240, 255))

    # Routing
    draw.rectangle([omx + 20, omy + 40, omx + omw - 20, omy + 96], fill=(14, 22, 34), outline=(45, 80, 120))
    draw.text((omx + 32, omy + 48), "STAGING BASE: KEPLER ORBITAL HAVEN (L5) [PMC SOVEREIGN DOMINION]", font=f_modal_bold, fill=(255, 215, 60))
    draw.text((omx + 32, omy + 70), "===[ HYPERLANE TRANSIT VECTOR ]===> TARGET: AETHELGARD PRIME CLUSTER (L4)", font=f_modal_bold, fill=(0, 240, 255))

    # Squadron Card
    draw.rectangle([omx + 20, omy + 110, omx + omw - 20, omy + 184], fill=(12, 18, 28), outline=(35, 65, 100))
    ms_iron = Image.open(os.path.join(units_dir, "spr_mini_ms_ironclad.png")).convert("RGBA")
    im.paste(ms_iron, (omx + 32, omy + 118), ms_iron)
    draw.text((omx + 90, omy + 118), "ASSIGNED SQUADRON: GHA-07 IRONCLAD HEAVY MS [4 UNITS]", font=f_modal_bold, fill=(255, 255, 255))
    draw.text((omx + 90, omy + 138), "ARMOR: 480 Titanium-Carbide  |  FIREPOWER: 120mm Rotary Vulcan + Dual Cannon", font=f_modal_body, fill=(160, 195, 225))
    draw.text((omx + 90, omy + 158), "OPERATION CLASSIFICATION: INTERDICTION ASSAULT & SECTOR SEIZURE", font=f_modal_bold, fill=(255, 120, 120))

    # Combat Simulation Forecast
    draw.rectangle([omx + 20, omy + 198, omx + omw - 20, omy + 320], fill=(14, 20, 30), outline=(45, 75, 110))
    draw.text((omx + 32, omy + 208), "COMBAT SIMULATION FORECAST (SHIN GIHREN'S GREED ALGORITHM):", font=f_modal_bold, fill=(255, 215, 80))
    draw.text((omx + 32, omy + 232), "• Projectile & Kinetic Attack Power: ~96 pts (Iron Ridge Strike Squadron)", font=f_modal_body, fill=(140, 220, 255))
    draw.text((omx + 32, omy + 254), "• Target Fortification Envelope: 82 / 100 DEF (Colony League Automated Emplacements)", font=f_modal_body, fill=(255, 120, 120))
    draw.text((omx + 32, omy + 276), "• Projected Breakthrough Probability: 65%  |  Estimated Hostile Losses: High", font=f_modal_bold, fill=(80, 255, 150))
    draw.text((omx + 32, omy + 296), "• Operation Fuel & Ammunition Logistics Cost: $15,000 Cr", font=f_modal_body, fill=(200, 220, 245))

    # Action Buttons
    btn_w, btn_h, by = 290, 44, omy + 346
    draw.rectangle([omx + 24, by, omx + 24 + btn_w, by + btn_h], fill=(20, 70, 95), outline=(0, 240, 255), width=2)
    draw.text((omx + 50, by + 12), "⚡ EXECUTE DISPATCH [ENTER]", font=f_modal_bold, fill=(0, 240, 255))

    draw.rectangle([omx + omw - 24 - btn_w, by, omx + omw - 24, by + btn_h], fill=(45, 18, 18), outline=(255, 90, 80))
    draw.text((omx + omw - 24 - btn_w + 50, by + 12), "✖ ABORT DIRECTIVE [ESC]", font=f_modal_bold, fill=(255, 110, 110))

    out_p = os.path.join(brain_dir, "live_tactical_order_modal.png")
    im.save(out_p)
    print("Saved:", out_p)

# -------------------------------------------------------------------------
# RENDER SCREEN 3: COMBAT ACTION REPORT MODAL
# -------------------------------------------------------------------------
def render_combat_action_report(base_im):
    im = base_im.copy()
    draw = ImageDraw.Draw(im)

    # Dark overlay
    overlay = Image.new("RGBA", (gw, gh), (0, 0, 0, 195))
    im.paste(overlay, (0, 0), overlay)

    cmw, cmh = 660, 410
    cmx = (gw - cmw) // 2
    cmy = (gh - cmh) // 2

    # Modal panel
    draw.rectangle([cmx, cmy, cmx + cmw, cmy + cmh], fill=(12, 18, 28), outline=(255, 215, 60), width=2)
    draw.rectangle([cmx, cmy, cmx + cmw, cmy + 28], fill=(50, 40, 14))
    draw.text((cmx + 16, cmy + 6), "OPERATION SUCCESS // SECTOR SECURED", font=f_modal_h, fill=(255, 215, 60))

    # Status Banner
    draw.rectangle([cmx + 20, cmy + 40, cmx + cmw - 20, cmy + 92], fill=(14, 20, 30), outline=(255, 215, 60))
    draw.rectangle([cmx + 20, cmy + 40, cmx + 26, cmy + 92], fill=(255, 215, 60))
    draw.text((cmx + 36, cmy + 48), "★ TACTICAL VICTORY: SECTOR SECURED & SOVEREIGNTY CLAIMED ★", font=f_modal_bold, fill=(255, 215, 60))
    draw.text((cmx + 36, cmy + 68), "STAGING: Kepler Haven ===> TARGET: Aethelgard Prime Cluster (L4)", font=f_modal_body, fill=(180, 210, 240))

    # Round Ledger
    led_y = cmy + 106
    draw.rectangle([cmx + 20, led_y, cmx + cmw - 20, led_y + 200], fill=(10, 16, 24), outline=(40, 65, 95))
    draw.text((cmx + 32, led_y + 14), "BATTLE ACTION LOG // COMBAT RESOLUTION LEDGER (SHIN GIHREN'S GREED ENGINE):", font=f_modal_bold, fill=(0, 220, 255))

    rounds = [
        "PHASE 1 (INGRESS): Iron Ridge strike wing engages target outer sensors along L4 transfer vector.",
        "PHASE 2 (FIRE EXCHANGE): Attack rating [98 pts] vs Garrison defense envelope [78 pts].",
        "PHASE 3 (BREACH): 120mm kinetic rounds shatter outer hangar airlock. Enemy defense collapses!",
        "PHASE 4 (SOVEREIGNTY): Faction flags replaced. Iron Ridge PMC administrative hub established."
    ]
    for ri, rline in enumerate(rounds):
        draw.text((cmx + 32, led_y + 40 + ri * 28), "• " + rline, font=f_modal_body, fill=(200, 225, 250))

    draw.text((cmx + 32, led_y + 165), "RESULT: Sector liberated and integrated into Iron Ridge PMC sovereign zone (+44,000 Cr/Day).", font=f_modal_bold, fill=(80, 240, 140))

    # Dismiss Button
    dbtn_w, dbtn_h, dby = 320, 42, cmy + cmh - 56
    dbx = cmx + (cmw - dbtn_w) // 2
    draw.rectangle([dbx, dby, dbx + dbtn_w, dby + dbtn_h], fill=(30, 60, 40), outline=(80, 255, 150), width=2)
    draw.text((dbx + 36, dby + 12), ">> ACKNOWLEDGE REPORT [ESC/ENTER] >>", font=f_modal_bold, fill=(80, 255, 150))

    out_p = os.path.join(brain_dir, "live_combat_action_report.png")
    im.save(out_p)
    print("Saved:", out_p)

base_im = render_order_dispatch_screen()
render_tactical_order_modal(base_im)
render_combat_action_report(base_im)
print("All 3 interactive order & combat screens generated and verified!")
