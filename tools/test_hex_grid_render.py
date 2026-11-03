import math
from PIL import Image, ImageDraw, ImageFont

# Screen canvas 1280x720
im = Image.new("RGBA", (1280, 720), (12, 14, 20, 255))
draw = ImageDraw.Draw(im)

rad_x = 16
rad_y = 98
rad_w = 954
rad_h = 596

start_x = rad_x + 36
start_y = rad_y + 42
col_dist = 42
row_dist = 48
odd_offset = 24

def hex_center(c, r):
    x = start_x + c * col_dist
    y = start_y + r * row_dist + (odd_offset if (c % 2 == 1) else 0)
    return x, y

def draw_hex(draw, cx, cy, r, fill, outline, width=1):
    pts = []
    for i in range(6):
        ang = math.radians(i * 60)
        px = cx + r * math.cos(ang)
        py = cy + r * math.sin(ang)
        pts.append((px, py))
    if fill:
        draw.polygon(pts, fill=fill)
    if outline:
        draw.polygon(pts, outline=outline, width=width)

# Draw radar panel box
draw.rectangle([rad_x, rad_y, rad_x + rad_w, rad_y + rad_h], fill=(8, 12, 18, 255), outline=(60, 180, 240, 255), width=2)

# Sample terrain
# Draw 16x10 grid
for c in range(16):
    for r in range(10):
        hx, hy = hex_center(c, r)
        # Terrain coloring
        if (c == 7 and 1 <= r <= 8) or (c == 6 and 3 <= r <= 5) or (c == 8 and 6 <= r <= 9):
            fill = (15, 45, 90, 120)
            outline = (30, 90, 170, 140)
        elif (3 <= c <= 5 and r <= 3) or (11 <= c <= 13 and r >= 7):
            fill = (15, 60, 35, 120)
            outline = (35, 120, 70, 140)
        elif (c <= 2 and r <= 2) or (c >= 13 and r <= 2):
            fill = (55, 50, 65, 130)
            outline = (100, 95, 120, 150)
        elif (c, r) in [(10, 4), (6, 2), (12, 6)]:
            fill = (120, 90, 20, 140)
            outline = (255, 215, 60, 220)
        else:
            fill = (20, 32, 48, 80)
            outline = (35, 65, 95, 100)
        draw_hex(draw, hx, hy, 26, fill, outline, width=1)

# Reachable hexes around (2, 4) with 4 MP
selected_c, selected_r = 2, 4
import heapq
def get_nbrs(c, r):
    if c % 2 == 0:
        raw = [(c, r-1), (c+1, r-1), (c+1, r), (c, r+1), (c-1, r), (c-1, r-1)]
    else:
        raw = [(c, r-1), (c+1, r), (c+1, r+1), (c, r+1), (c-1, r+1), (c-1, r)]
    return [(nc, nr) for nc, nr in raw if 0 <= nc < 16 and 0 <= nr < 10]

dist = {(selected_c, selected_r): 0}
pq = [(0, selected_c, selected_r)]
while pq:
    d, c, r = heapq.heappop(pq)
    for nc, nr in get_nbrs(c, r):
        cost = 3 if ((nc == 7 and 1 <= nr <= 8) or (nc <= 2 and nr <= 2)) else (2 if (3 <= nc <= 5 and nr <= 3) else 1)
        nd = d + cost
        if nd <= 4 and ( (nc, nr) not in dist or nd < dist[(nc, nr)] ):
            dist[(nc, nr)] = nd
            heapq.heappush(pq, (nd, nc, nr))

for (rc, rr), cost in dist.items():
    if (rc, rr) == (selected_c, selected_r): continue
    hx, hy = hex_center(rc, rr)
    draw_hex(draw, hx, hy, 25, (0, 240, 200, 45), (0, 240, 220, 180), width=2)

# Draw selected unit at (2, 4)
sx, sy = hex_center(selected_c, selected_r)
draw_hex(draw, sx, sy, 27, (0, 180, 255, 60), (0, 255, 255, 255), width=3)
draw.ellipse([sx - 18, sy - 18, sx + 18, sy + 18], fill=(255, 215, 60, 220), outline=(255, 255, 255, 255))
draw.text((sx - 12, sy - 6), "PMC", fill=(0, 0, 0, 255))

# Draw enemy units
for ec, er, label in [(12, 4, "CMD"), (13, 2, "ART"), (9, 3, "GRN"), (11, 6, "TNK"), (8, 7, "REC")]:
    ex, ey = hex_center(ec, er)
    draw.ellipse([ex - 16, ey - 16, ex + 16, ey + 16], fill=(220, 50, 60, 220), outline=(255, 200, 200, 255))
    draw.text((ex - 10, ey - 6), label, fill=(255, 255, 255, 255))

# Draw Target engagement range around Grunt at (9, 3) if within range
# (9, 3) is enemy

# Sidebar
sb_x = rad_x + rad_w - 235
draw.rectangle([sb_x, rad_y + 36, rad_x + rad_w - 18, rad_y + 154], fill=(15, 22, 32, 255), outline=(45, 80, 125, 255), width=2)
draw.text((sb_x + 10, rad_y + 42), "SATELLITE TELEMETRY", fill=(255, 215, 80, 255))

# Unit inspector
insp_y = rad_y + 162
draw.rectangle([sb_x, insp_y, rad_x + rad_w - 18, insp_y + 230], fill=(20, 28, 42, 255), outline=(60, 140, 210, 255), width=2)
draw.text((sb_x + 10, insp_y + 8), "TACTICAL UNIT INSPECTOR", fill=(0, 240, 255, 255))
draw.text((sb_x + 10, insp_y + 28), "Ironclad Vanguard Alpha", fill=(255, 255, 255, 255))
draw.text((sb_x + 10, insp_y + 48), "FACTION: PMC VANGUARD", fill=(255, 215, 60, 255))
draw.text((sb_x + 10, insp_y + 70), "HP: [========] 100/100", fill=(80, 240, 120, 255))
draw.text((sb_x + 10, insp_y + 90), "MP: [====....] 4 / 4", fill=(60, 180, 255, 255))
draw.text((sb_x + 10, insp_y + 115), "ATK: 45 | DEF: 30 | RNG: 1", fill=(220, 220, 240, 255))
draw.text((sb_x + 10, insp_y + 135), "STATUS: READY FOR ACTION", fill=(0, 255, 180, 255))
draw.text((sb_x + 10, insp_y + 165), "HEX: [COL: 02, ROW: 04]", fill=(180, 200, 220, 255))
draw.text((sb_x + 10, insp_y + 185), "TERRAIN: BASALT CRATON", fill=(255, 200, 80, 255))
draw.text((sb_x + 10, insp_y + 205), "DEFENSE BONUS: +10% | 1 MP", fill=(160, 180, 210, 255))

# End Turn Button
btn_y = insp_y + 240
draw.rectangle([sb_x, btn_y, rad_x + rad_w - 18, btn_y + 36], fill=(180, 130, 20, 255), outline=(255, 215, 60, 255), width=2)
draw.text((sb_x + 16, btn_y + 10), ">> END TURN / CYCLE [SPACE]", fill=(0, 0, 0, 255))

btn2_y = btn_y + 44
draw.rectangle([sb_x, btn2_y, rad_x + rad_w - 18, btn2_y + 36], fill=(30, 80, 160, 255), outline=(0, 220, 255, 255), width=2)
draw.text((sb_x + 18, btn2_y + 10), "⚡ ENTER COMBAT SIM (rm_combat)", fill=(255, 255, 255, 255))

im.save("tools/hex_grid_test_layout.png")
print("Saved tools/hex_grid_test_layout.png")
