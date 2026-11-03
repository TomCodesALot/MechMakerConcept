import math
from PIL import Image, ImageDraw, ImageFont

gw = 1280
gh = 720
im = Image.new("RGBA", (gw, gh), (10, 14, 20, 255))
draw = ImageDraw.Draw(im)

# Load fonts
try:
    font_lg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
    font_md = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)
    font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
except:
    font_lg = ImageFont.load_default()
    font_md = ImageFont.load_default()
    font_sm = ImageFont.load_default()

# 1. Background Grid & Outer Bezel
draw.rectangle([0, 0, gw, gh], fill=(8, 12, 18, 255))

# Top App Header
draw.rectangle([16, 12, gw - 16, 52], fill=(14, 20, 30, 255), outline=(40, 75, 120, 255), width=2)
draw.text((28, 20), "MECH-COMMAND-OS // STRATEGIC THEATER RADAR // SHIN GIHREN'S GREED TACTICAL HEX ENGINE", fill=(255, 215, 60, 255), font=font_lg)
draw.text((gw - 280, 22), "YEAR 214 // TAC-CYCLE: 01 // READY", fill=(0, 240, 255, 255), font=font_md)

# Theater Tabs
tab_x = 16
for tab_name, active in [("EARTH THEATER (GLOBAL / STRONGHOLD)", True), ("MARS CRATER BASIN", False), ("ORBITAL COLONIES (L4/L5)", False)]:
    tw = 260 if active else 180
    bg_c = (24, 40, 65, 255) if active else (12, 18, 26, 255)
    border_c = (0, 240, 255, 255) if active else (30, 50, 75, 255)
    text_c = (255, 255, 255, 255) if active else (140, 170, 200, 255)
    draw.rectangle([tab_x, 60, tab_x + tw, 88], fill=bg_c, outline=border_c, width=2)
    draw.text((tab_x + 12, 68), tab_name, fill=text_c, font=font_md)
    tab_x += tw + 10

rad_x = 16
rad_y = 98
rad_w = 954
rad_h = 596

# Radar Panel Frame
draw.rectangle([rad_x, rad_y, rad_x + rad_w, rad_y + rad_h], fill=(12, 16, 24, 255), outline=(60, 180, 240, 255), width=2)
# Panel Title Header
draw.rectangle([rad_x + 2, rad_y + 2, rad_x + rad_w - 2, rad_y + 24], fill=(20, 36, 56, 255))
draw.text((rad_x + 12, rad_y + 6), "STRATEGIC STRONGHOLD // GRANITE DEEP REDOUNT (AMAZON BASIN TACTICAL MAP)", fill=(0, 240, 255, 255), font=font_md)

# Map background inside radar panel
map_bg_path = "sprites/spr_map_earth_theater/spr_map_earth_theater.png"
try:
    map_bg = Image.open(map_bg_path).convert("RGBA")
    map_bg = map_bg.resize((rad_w - 24, rad_h - 38))
    # Dim background slightly for hex grid readability
    overlay = Image.new("RGBA", map_bg.size, (10, 16, 26, 85))
    map_bg = Image.alpha_composite(map_bg, overlay)
    im.paste(map_bg, (rad_x + 12, rad_y + 26), map_bg)
except Exception as e:
    print("Error loading map bg:", e)

# Navigation Top Bar inside Radar
ret_x = rad_x + 18
ret_y = rad_y + 32
draw.rectangle([ret_x, ret_y, ret_x + 175, ret_y + 26], fill=(20, 32, 48, 255), outline=(0, 240, 255, 255), width=2)
draw.text((ret_x + 10, ret_y + 6), "<< WORLD MAP [ESC]", fill=(0, 240, 255, 255), font=font_md)

sb_x = ret_x + 175 + 8
draw.rectangle([sb_x, ret_y, sb_x + 270, ret_y + 26], fill=(10, 16, 26, 255), outline=(255, 215, 60, 255), width=2)
draw.text((sb_x + 10, ret_y + 6), "★ GRANITE DEEP COMMAND REDOUBT", fill=(255, 230, 100, 255), font=font_md)

grid_btn_x = sb_x + 270 + 8
draw.rectangle([grid_btn_x, ret_y, grid_btn_x + 125, ret_y + 26], fill=(24, 52, 45, 255), outline=(80, 220, 180, 255), width=2)
draw.text((grid_btn_x + 10, ret_y + 6), "HEX GRID: [ON]", fill=(120, 255, 200, 255), font=font_md)

ph_x = grid_btn_x + 125 + 8
draw.rectangle([ph_x, ret_y, ph_x + 130, ret_y + 26], fill=(14, 22, 34, 255), outline=(0, 220, 255, 255), width=2)
draw.text((ph_x + 10, ret_y + 6), "CYCLE 01 // ALLIES", fill=(255, 255, 255, 255), font=font_md)

# Hex Grid Geometry
start_x = rad_x + 36
start_y = rad_y + 42
col_dist = 42
row_dist = 48
odd_offset = 24

def hex_center(c, r):
    x = start_x + c * col_dist
    y = start_y + r * row_dist + (odd_offset if (c % 2 == 1) else 0)
    return x, y

def get_hex_polygon(cx, cy, r):
    pts = []
    for i in range(6):
        ang = math.radians(i * 60)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts

# Terrain definition
terrain = {}
for c in range(16):
    for r in range(10):
        t = "CRATON"
        if (c == 7 and 1 <= r <= 8) or (c == 6 and 3 <= r <= 5) or (c == 8 and 6 <= r <= 9):
            t = "WATER"
        elif (3 <= c <= 5 and r <= 3) or (11 <= c <= 13 and r >= 7):
            t = "FOREST"
        elif (c <= 2 and r <= 3) or (c >= 13 and r <= 3):
            t = "MOUNTAIN"
        terrain[(c, r)] = t

terrain[(10, 4)] = "BASE_FACILITY"
terrain[(6, 2)] = "BASE_FACILITY"
terrain[(12, 6)] = "BASE_FACILITY"

# Draw Hex Grid Layer
hex_overlay = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
hdraw = ImageDraw.Draw(hex_overlay)

for c in range(16):
    for r in range(10):
        hx, hy = hex_center(c, r)
        pts = get_hex_polygon(hx, hy, 26)
        t = terrain[(c, r)]
        if t == "WATER":
            fill = (12, 42, 85, 120)
            outline = (25, 80, 150, 140)
        elif t == "FOREST":
            fill = (16, 55, 30, 110)
            outline = (35, 110, 60, 130)
        elif t == "MOUNTAIN":
            fill = (52, 48, 62, 130)
            outline = (90, 85, 110, 140)
        elif t == "BASE_FACILITY":
            fill = (110, 85, 20, 120)
            outline = (255, 215, 60, 200)
        else:
            fill = (18, 30, 48, 60)
            outline = (32, 60, 90, 80)
        hdraw.polygon(pts, fill=fill, outline=outline)

        if t == "BASE_FACILITY":
            hdraw.ellipse([hx - 4, hy - 14, hx + 4, hy - 6], fill=(255, 220, 80, 255))
            hdraw.text((hx - 12, hy - 24), "BASE", fill=(255, 235, 140, 255), font=font_sm)

# Reachable Hexes for selected unit at (2, 4) with 4 MP
def get_nbrs(c, r):
    if c % 2 == 0:
        raw = [(c, r-1), (c+1, r-1), (c+1, r), (c, r+1), (c-1, r), (c-1, r-1)]
    else:
        raw = [(c, r-1), (c+1, r), (c+1, r+1), (c, r+1), (c-1, r+1), (c-1, r)]
    return [(nc, nr) for nc, nr in raw if 0 <= nc < 16 and 0 <= nr < 10]

import heapq
dist = {(2, 4): 0}
pq = [(0, 2, 4)]
while pq:
    d, c, r = heapq.heappop(pq)
    for nc, nr in get_nbrs(c, r):
        step_cost = 3 if terrain.get((nc, nr)) in ["WATER", "MOUNTAIN"] else (2 if terrain.get((nc, nr)) == "FOREST" else 1)
        nd = d + step_cost
        if nd <= 4 and ( (nc, nr) not in dist or nd < dist[(nc, nr)] ):
            dist[(nc, nr)] = nd
            heapq.heappush(pq, (nd, nc, nr))

for (rc, rr), cost in dist.items():
    if (rc, rr) == (2, 4): continue
    hx, hy = hex_center(rc, rr)
    pts = get_hex_polygon(hx, hy, 25)
    hdraw.polygon(pts, fill=(0, 240, 200, 55), outline=(0, 255, 220, 210))

# Movement Path Preview to (4, 4)
src_x, src_y = hex_center(2, 4)
dst_x, dst_y = hex_center(4, 4)
hdraw.line([(src_x, src_y), (dst_x, dst_y)], fill=(0, 240, 255, 240), width=3)
hdraw.ellipse([dst_x - 5, dst_y - 5, dst_x + 5, dst_y + 5], fill=(0, 240, 255, 255))
# MP badge
hdraw.rectangle([dst_x - 22, dst_y - 28, dst_x + 22, dst_y - 12], fill=(10, 16, 26, 240), outline=(0, 240, 255, 255))
hdraw.text((dst_x - 17, dst_y - 27), "-2 MP", fill=(255, 255, 255, 255), font=font_sm)

# Targeting reticle on enemy Grunt at (9, 3) and Rover at (8, 7)
for ec, er in [(9, 3), (8, 7)]:
    ex, ey = hex_center(ec, er)
    hdraw.ellipse([ex - 22, ey - 22, ex + 22, ey + 22], outline=(255, 60, 70, 220), width=2)
    hdraw.text((ex - 18, ey - 30), "[TARGET]", fill=(255, 90, 100, 255), font=font_sm)

im = Image.alpha_composite(im, hex_overlay)
draw = ImageDraw.Draw(im)

# Helper function to draw tactical counter using real sprites
def draw_counter(cx, cy, base_spr_name, unit_spr_name, stack_count, is_sel=False, hp=100, max_hp=100, mp=4, max_mp=4, is_pmc=True):
    # Plinth
    try:
        base_im = Image.open(f"sprites/{base_spr_name}/{base_spr_name}.png").convert("RGBA")
        base_im = base_im.resize((44, 32))
        im.paste(base_im, (cx - 22, cy - 12), base_im)
    except:
        draw.ellipse([cx - 20, cy - 6, cx + 20, cy + 10], fill=(40, 60, 90, 255), outline=(0, 240, 255, 255))

    # Unit sprite
    try:
        unit_im = Image.open(f"sprites/{unit_spr_name}/{unit_spr_name}.png").convert("RGBA")
        unit_im = unit_im.resize((36, 36))
        im.paste(unit_im, (cx - 18, cy - 28), unit_im)
    except:
        draw.ellipse([cx - 12, cy - 24, cx + 12, cy], fill=(255, 200, 40, 255))

    # Selection Ring
    if is_sel:
        draw.ellipse([cx - 24, cy - 20, cx + 24, cy + 18], outline=(0, 240, 255, 255), width=2)

    # Stack Badge
    sb_w, sb_h = 16, 12
    draw.rectangle([cx + 10, cy + 2, cx + 10 + sb_w, cy + 2 + sb_h], fill=(12, 18, 28, 255), outline=(255, 215, 60, 255))
    draw.text((cx + 12, cy + 3), f"x{stack_count}", fill=(255, 255, 255, 255), font=font_sm)

    # HP Bar Underneath
    bar_w = 32
    draw.rectangle([cx - bar_w//2, cy + 18, cx + bar_w//2, cy + 22], fill=(10, 16, 24, 255))
    pct = hp / max_hp
    fill_col = (60, 220, 100, 255) if pct > 0.6 else ((255, 200, 40, 255) if pct > 0.3 else (255, 60, 60, 255))
    draw.rectangle([cx - bar_w//2, cy + 18, cx - bar_w//2 + int(bar_w * pct), cy + 22], fill=fill_col)
    draw.rectangle([cx - bar_w//2, cy + 18, cx + bar_w//2, cy + 22], outline=(40, 60, 80, 255))

    # MP Pips Above (for PMC)
    if is_pmc:
        pip_start = cx - (max_mp * 6) // 2
        for pi in range(max_mp):
            pcol = (0, 240, 255, 255) if pi < mp else (40, 60, 80, 255)
            draw.rectangle([pip_start + pi * 6, cy - 34, pip_start + pi * 6 + 4, cy - 31], fill=pcol)

# Draw Friendly PMC Units
u1_x, u1_y = hex_center(2, 4)
draw_counter(u1_x, u1_y, "spr_hex_base_pmc", "spr_mini_ms_ironclad", 3, is_sel=True, hp=100, max_hp=100, mp=4, max_mp=4, is_pmc=True)

u2_x, u2_y = hex_center(2, 6)
draw_counter(u2_x, u2_y, "spr_hex_base_pmc", "spr_mini_ms_aerostriker", 3, is_sel=False, hp=80, max_hp=80, mp=5, max_mp=5, is_pmc=True)

u3_x, u3_y = hex_center(3, 3)
draw_counter(u3_x, u3_y, "spr_hex_base_pmc", "spr_mini_veh_heavy_tank", 5, is_sel=False, hp=120, max_hp=120, mp=3, max_mp=3, is_pmc=True)

u4_x, u4_y = hex_center(3, 7)
draw_counter(u4_x, u4_y, "spr_hex_base_pmc", "spr_mini_inf_exo_squad", 8, is_sel=False, hp=65, max_hp=65, mp=2, max_mp=2, is_pmc=True)

# Draw OPFOR Garrison Units
e1_x, e1_y = hex_center(12, 4)
draw_counter(e1_x, e1_y, "spr_hex_base_colony", "spr_mini_ms_commander", 4, is_sel=False, hp=110, max_hp=110, mp=4, max_mp=4, is_pmc=False)

e2_x, e2_y = hex_center(13, 2)
draw_counter(e2_x, e2_y, "spr_hex_base_colony", "spr_mini_ms_artillery", 4, is_sel=False, hp=85, max_hp=85, mp=3, max_mp=3, is_pmc=False)

e3_x, e3_y = hex_center(9, 3)
draw_counter(e3_x, e3_y, "spr_hex_base_colony", "spr_mini_ms_grunt", 4, is_sel=False, hp=90, max_hp=90, mp=4, max_mp=4, is_pmc=False)

e4_x, e4_y = hex_center(11, 6)
draw_counter(e4_x, e4_y, "spr_hex_base_colony", "spr_mini_veh_heavy_tank", 5, is_sel=False, hp=110, max_hp=110, mp=3, max_mp=3, is_pmc=False)

e5_x, e5_y = hex_center(8, 7)
draw_counter(e5_x, e5_y, "spr_hex_base_colony", "spr_mini_veh_technical", 6, is_sel=False, hp=70, max_hp=70, mp=4, max_mp=4, is_pmc=False)

# Right Radar HUD ($x: 738..954$)
hud_w = 216
hud_x = rad_x + rad_w - hud_w - 16

# Minimap
mm_h = 112
mm_y = rad_y + 32
draw.rectangle([hud_x, mm_y, hud_x + hud_w, mm_y + mm_h], fill=(8, 14, 22, 255), outline=(45, 80, 125, 255), width=2)
try:
    amber_mm = Image.open("sprites/spr_radar_earth_amber/spr_radar_earth_amber.png").convert("RGBA")
    amber_mm = amber_mm.resize((hud_w - 4, mm_h - 4))
    im.paste(amber_mm, (hud_x + 2, mm_y + 2), amber_mm)
except:
    pass
draw.text((hud_x + 8, mm_y + 6), "TERRESTRIAL SATELLITE", fill=(255, 215, 80, 255), font=font_sm)
draw.rectangle([hud_x + 44, mm_y + 40, hud_x + 44 + 50, mm_y + 40 + 44], outline=(0, 240, 255, 255), width=2)

# Middle Inspector
insp_y = mm_y + mm_h + 8
insp_h = 230
draw.rectangle([hud_x, insp_y, hud_x + hud_w, insp_y + insp_h], fill=(12, 18, 28, 255), outline=(45, 85, 130, 255), width=2)
draw.rectangle([hud_x + 2, insp_y + 2, hud_x + hud_w - 2, insp_y + 22], fill=(20, 32, 50, 255))
draw.text((hud_x + 8, insp_y + 6), "TACTICAL SQUADRON INSPECTOR", fill=(0, 240, 255, 255), font=font_sm)

draw.text((hud_x + 8, insp_y + 28), "Ironclad Vanguard Alpha", fill=(255, 255, 255, 255), font=font_md)
draw.text((hud_x + 8, insp_y + 44), "GHA-07 Ironclad", fill=(255, 215, 60, 255), font=font_sm)
draw.text((hud_x + 8, insp_y + 60), "PMC VANGUARD [ALLIED]", fill=(0, 220, 255, 255), font=font_sm)

draw.text((hud_x + 8, insp_y + 78), "HULL INTEGRITY:", fill=(180, 210, 240, 255), font=font_sm)
draw.text((hud_x + hud_w - 65, insp_y + 78), "100/100 HP", fill=(60, 220, 100, 255), font=font_sm)
draw.rectangle([hud_x + 8, insp_y + 94, hud_x + hud_w - 8, insp_y + 101], fill=(20, 30, 42, 255))
draw.rectangle([hud_x + 8, insp_y + 94, hud_x + hud_w - 8, insp_y + 101], fill=(60, 220, 100, 255))

draw.text((hud_x + 8, insp_y + 106), "MOBILITY POINTS:", fill=(180, 210, 240, 255), font=font_sm)
draw.text((hud_x + hud_w - 65, insp_y + 106), "4 / 4 MP", fill=(0, 220, 255, 255), font=font_sm)
draw.rectangle([hud_x + 8, insp_y + 122, hud_x + hud_w - 8, insp_y + 129], fill=(20, 30, 42, 255))
draw.rectangle([hud_x + 8, insp_y + 122, hud_x + hud_w - 8, insp_y + 129], fill=(0, 220, 255, 255))

draw.text((hud_x + 8, insp_y + 138), "ATK: 45  DEF: 30  RNG: 1 HEX", fill=(220, 230, 245, 255), font=font_sm)
draw.text((hud_x + 8, insp_y + 154), "STATUS: [READY FOR ACTION]", fill=(80, 255, 140, 255), font=font_sm)
draw.text((hud_x + 8, insp_y + 174), "SECTOR [02,04]: Basalt Craton", fill=(160, 190, 220, 255), font=font_sm)
draw.text((hud_x + 8, insp_y + 192), "TERRAIN DEFENSE BONUS: +10 %", fill=(255, 215, 60, 255), font=font_sm)
draw.text((hud_x + 8, insp_y + 210), "CLICK GREEN HEX TO MOVE / FIRE", fill=(140, 180, 220, 255), font=font_sm)

# Combat Log Box
log_y = insp_y + insp_h + 8
log_h = 70
draw.rectangle([hud_x, log_y, hud_x + hud_w, log_y + log_h], fill=(8, 12, 18, 255), outline=(35, 60, 95, 255), width=2)
draw.text((hud_x + 6, log_y + 4), "COMBAT TELEMETRY LOG:", fill=(255, 215, 60, 255), font=font_sm)
draw.text((hud_x + 6, log_y + 20), "CYCLE 01 INITIALIZED.", fill=(170, 205, 240, 255), font=font_sm)
draw.text((hud_x + 6, log_y + 35), "VANGUARD DEPLOYED AT L-PERIMETER.", fill=(170, 205, 240, 255), font=font_sm)
draw.text((hud_x + 6, log_y + 50), "TARGET ACQUIRED: HOSTILE RECON [8,7]", fill=(255, 140, 100, 255), font=font_sm)

# End Turn Button
et_y = log_y + log_h + 8
draw.rectangle([hud_x, et_y, hud_x + hud_w, et_y + 32], fill=(180, 130, 20, 255), outline=(255, 215, 60, 255), width=2)
draw.text((hud_x + 18, et_y + 8), "⏩ ADVANCE CYCLE [SPACE]", fill=(0, 0, 0, 255), font=font_md)

# Sortie Button
sort_y = et_y + 32 + 6
draw.rectangle([hud_x, sort_y, hud_x + hud_w, sort_y + 28], fill=(140, 35, 45, 255), outline=(255, 90, 90, 255), width=2)
draw.text((hud_x + 28, sort_y + 6), "⚡ ENTER COMBAT SIM", fill=(255, 255, 255, 255), font=font_sm)

# Right Dossier Panel ($x: 982..1264$)
dos_x = 982
dos_y = 98
dos_w = gw - dos_x - 16
dos_h = rad_h

draw.rectangle([dos_x, dos_y, dos_x + dos_w, dos_y + dos_h], fill=(12, 18, 28, 255), outline=(255, 215, 60, 255), width=2)
draw.rectangle([dos_x + 2, dos_y + 2, dos_x + dos_w - 2, dos_y + 24], fill=(28, 40, 60, 255))
draw.text((dos_x + 12, dos_y + 6), "STRONGHOLD SECTOR DOSSIER", fill=(255, 215, 60, 255), font=font_md)

# Spot Artwork Thumbnail
thumb_x = dos_x + 16
thumb_y = dos_y + 28
thumb_w = dos_w - 32
thumb_h = 130
draw.rectangle([thumb_x, thumb_y, thumb_x + thumb_w, thumb_y + thumb_h], fill=(10, 16, 24, 255), outline=(255, 215, 60, 255), width=2)
try:
    loc_im = Image.open("sprites/spr_loc_earth_granite/spr_loc_earth_granite.png").convert("RGBA")
    loc_im = loc_im.resize((thumb_w - 4, thumb_h - 4))
    im.paste(loc_im, (thumb_x + 2, thumb_y + 2), loc_im)
except Exception as e:
    print("Error loading loc im:", e)

draw.rectangle([thumb_x + 8, thumb_y + thumb_h - 22, thumb_x + 185, thumb_y + thumb_h - 4], fill=(12, 18, 28, 240), outline=(255, 215, 60, 255))
draw.text((thumb_x + 12, thumb_y + thumb_h - 19), "TELEMETRY // CORE BUNKER", fill=(255, 230, 120, 255), font=font_sm)

# Subnode Details
cy = thumb_y + thumb_h + 10
draw.text((dos_x + 16, cy), "GRANITE COMMAND REDOUBT", fill=(255, 220, 90, 255), font=font_lg)
draw.text((dos_x + 16, cy + 18), "SOUTH AMERICA // CORE BUNKER", fill=(140, 175, 210, 255), font=font_sm)

# Garrison Tac-Card
gcard_y = cy + 36
draw.rectangle([dos_x + 16, gcard_y, dos_x + dos_w - 16, gcard_y + 64], fill=(12, 18, 28, 255), outline=(40, 75, 115, 255), width=2)
draw_counter(dos_x + 46, gcard_y + 40, "spr_hex_base_colony", "spr_mini_ms_commander", 5, is_sel=False, hp=120, max_hp=120, is_pmc=False)
draw.text((dos_x + 76, gcard_y + 8), "REDOUBT GARRISON COMMAND", fill=(255, 255, 255, 255), font=font_md)
draw.text((dos_x + 76, gcard_y + 24), "SQUADRON STRENGTH: [05] UNITS", fill=(0, 240, 255, 255), font=font_sm)
draw.text((dos_x + 76, gcard_y + 40), "★ PRIMARY HQ REACTOR", fill=(255, 215, 60, 255), font=font_sm)

# Controller
box_y = gcard_y + 74
draw.rectangle([dos_x + 16, box_y, dos_x + dos_w - 16, box_y + 44], fill=(14, 22, 32, 255), outline=(60, 140, 255, 255), width=2)
draw.text((dos_x + 24, box_y + 6), "CONTROLLER: Federal Terran Garrison", fill=(60, 140, 255, 255), font=font_sm)
draw.text((dos_x + 24, box_y + 24), "BASE FORTIFICATION BONUS: +95 DEF", fill=(80, 255, 140, 255), font=font_sm)

# Fortify rating
def_y = box_y + 54
draw.text((dos_x + 16, def_y), "PERIMETER FORTIFICATION: 95 / 100", fill=(200, 220, 245, 255), font=font_sm)
draw.rectangle([dos_x + 16, def_y + 18, dos_x + dos_w - 16, def_y + 28], fill=(20, 28, 40, 255), outline=(50, 80, 120, 255))
draw.rectangle([dos_x + 16, def_y + 18, dos_x + 16 + int((dos_w - 32) * 0.95), def_y + 28], fill=(255, 215, 60, 255))

# Lore description
draw.text((dos_x + 16, def_y + 36), "Buried two kilometers beneath granite craton.\nHeavy geothermal reactors power local rail\ngun batteries and deep MS maintenance bays.", fill=(160, 190, 220, 255), font=font_sm)

# Actions
act_y = dos_y + dos_h - 85
draw.rectangle([dos_x + 16, act_y, dos_x + dos_w - 16, act_y + 32], fill=(20, 60, 45, 255), outline=(80, 240, 140, 255), width=2)
draw.text((dos_x + 32, act_y + 8), ">> FORTIFY PERIMETER (+10 DEF) >>", fill=(80, 240, 140, 255), font=font_md)

act2_y = act_y + 38
draw.rectangle([dos_x + 16, act2_y, dos_x + dos_w - 16, act2_y + 34], fill=(160, 40, 40, 255), outline=(255, 100, 100, 255), width=2)
draw.text((dos_x + 44, act2_y + 8), "⚔️ SORTIE COMBAT SQUAD HERE", fill=(255, 255, 255, 255), font=font_md)

out_path = "/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/live_stronghold_hex_grid_movement.png"
im.save(out_path)
print("Saved live screenshot to:", out_path)
