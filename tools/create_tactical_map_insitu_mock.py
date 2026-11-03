from PIL import Image, ImageDraw, ImageFont
import os

units_dir = "/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_units"
out_path = "/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_map_shin_gihren_style.png"

# Load space theater backdrop
map_bg_path = "sprites/spr_map_space_theater/spr_map_space_theater.png"
if os.path.exists(map_bg_path):
    map_bg = Image.open(map_bg_path).convert("RGBA")
    map_im = map_bg.resize((1280, 720), Image.Resampling.LANCZOS)
else:
    map_im = Image.new("RGBA", (1280, 720), (6, 10, 16, 255))

draw = ImageDraw.Draw(map_im)

# Dim background slightly for high contrast
dim = Image.new("RGBA", (1280, 720), (0, 0, 0, 120))
map_im = Image.alpha_composite(map_im, dim)
draw = ImageDraw.Draw(map_im)

# Font setup
try:
    font_bold = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 11)
    font_badge = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 13)
    font_stat = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf", 13)
except:
    font_bold = font_sub = font_badge = font_stat = ImageFont.load_default()

# 1. Hyperlane Transit Lines (Deep Red / Crimson glow like Shin Gihren's Greed)
lines = [
    ((0, 360), (1280, 360)),         # Main Trans-Lagrange Axis
    ((640, 360), (480, 720)),        # Slingshot south corridor 1
    ((640, 360), (740, 720)),        # Slingshot south corridor 2
    ((1120, 360), (1220, 560)),      # Asteroid belt feeder
]

for (p1, p2) in lines:
    draw.line([p1, p2], fill=(180, 30, 40, 255), width=5)
    draw.line([p1, p2], fill=(255, 90, 100, 255), width=2)

# Function to render counter
def get_counter(unit_name, base_name, stack_str="4"):
    im_u = Image.open(os.path.join(units_dir, f"{unit_name}.png")).convert("RGBA")
    im_b = Image.open(os.path.join(units_dir, f"{base_name}.png")).convert("RGBA")
    
    tile = Image.new("RGBA", (84, 84), (0, 0, 0, 0))
    bw, bh = 64, 44
    b_resized = im_b.resize((bw, bh), Image.Resampling.LANCZOS)
    bx = 10
    by = 84 - bh - 2
    tile.paste(b_resized, (bx, by), b_resized)
    
    uw, uh = 58, 58
    u_resized = im_u.resize((uw, uh), Image.Resampling.LANCZOS)
    ux = 13
    uy = by - uh + 28
    tile.paste(u_resized, (ux, uy), u_resized)
    
    t_draw = ImageDraw.Draw(tile)
    badge_x = bx + bw - 18
    badge_y = by + 10
    t_draw.rectangle([(badge_x, badge_y), (badge_x + 16, badge_y + 18)], fill=(6, 12, 18, 240), outline=(0, 240, 255, 255), width=1)
    t_draw.text((badge_x + 4, badge_y + 2), stack_str, fill=(0, 255, 220, 255), font=font_badge)
    return tile

# 2. Sector Nodes
# Node A (Center): Kepler Orbital Haven (L5)
node_x, node_y = 640, 360
# Hex Base Node
draw.polygon([
    (node_x - 36, node_y - 20), (node_x, node_y - 42), (node_x + 36, node_y - 20),
    (node_x + 36, node_y + 20), (node_x, node_y + 42), (node_x - 36, node_y + 20)
], fill=(20, 30, 45, 255), outline=(0, 240, 255, 255))
draw.polygon([
    (node_x - 28, node_y - 15), (node_x, node_y - 32), (node_x + 28, node_y - 15),
    (node_x + 28, node_y + 15), (node_x, node_y + 32), (node_x - 28, node_y + 15)
], fill=(210, 40, 60, 255), outline=(255, 220, 100, 255))

# Node B (Right): Ironspire Asteroid Bastion (L2)
ast_x, ast_y = 1120, 360
draw.ellipse([(ast_x - 32, ast_y - 32), (ast_x + 32, ast_y + 32)], fill=(45, 50, 60, 255), outline=(160, 175, 195, 255), width=2)
# Ring around asteroid
draw.arc([(ast_x - 48, ast_y - 18), (ast_x + 48, ast_y + 18)], 0, 360, fill=(0, 240, 255, 255), width=2)

# 3. Deploy Units along nodes & supply lines (Matching Reference layout)
# Garrison at Center Node:
# Counter 1: Main Battle Bipedal MS (Stack [4])
c1 = get_counter("spr_mini_ms_ironclad", "spr_hex_base_mars", "4")
map_im.paste(c1, (node_x - 65, node_y - 95), c1)

# Counter 2: Hover Sniper MS (Stack [4])
c2 = get_counter("spr_mini_ms_hoversniper", "spr_hex_base_mars", "4")
map_im.paste(c2, (node_x + 10, node_y - 95), c2)

# Moving Strike Wing on the Right Hyperlane (Towards Asteroid):
# Counter 3: Strike Gunship (Stack [3])
c3 = get_counter("spr_mini_veh_gunship", "spr_hex_base_mars", "3")
map_im.paste(c3, (890, 360 - 85), c3)

# Counter 4: Bipedal Grunt MS (Stack [6])
c4 = get_counter("spr_mini_ms_grunt", "spr_hex_base_mars", "6")
map_im.paste(c4, (970, 360 - 85), c4)

# Counter 5: Commander Custom MS (Stack [6])
c5 = get_counter("spr_mini_ms_commander", "spr_hex_base_mars", "6")
map_im.paste(c5, (1045, 360 - 85), c5)

# Selection Brackets ( ) around central node
br_im = Image.open(os.path.join(units_dir, "spr_tactical_bracket.png")).convert("RGBA")
br_w, br_h = 72, 54
br_scaled = br_im.resize((br_w, br_h), Image.Resampling.LANCZOS)
map_im.paste(br_scaled, (node_x - 120, node_y - 27), br_scaled)

# 4. Top-Right Orbital Mini-Map Radar (Exact Shin Gihren's Greed Style)
mm_x, mm_y, mm_w, mm_h = 880, 24, 376, 200
draw.rectangle([(mm_x, mm_y), (mm_x + mm_w, mm_y + mm_h)], fill=(10, 16, 26, 230), outline=(120, 150, 190, 255), width=2)

# Celestial orbits inside minimap
cx, cy = mm_x + 190, mm_y + 110
draw.ellipse([(cx - 140, cy - 70), (cx + 140, cy + 70)], outline=(60, 90, 120, 255), width=1)
draw.ellipse([(cx - 95, cy - 50), (cx + 95, cy + 50)], outline=(80, 120, 160, 255), width=1)
draw.ellipse([(cx - 50, cy - 28), (cx + 50, cy + 28)], outline=(100, 140, 180, 255), width=1)

# Earth and Moon in minimap
draw.ellipse([(cx - 24, cy - 24), (cx + 24, cy + 24)], fill=(40, 110, 180, 255), outline=(100, 200, 255, 255), width=1) # Earth
draw.ellipse([(cx + 80, cy - 28), (cx + 96, cy - 12)], fill=(190, 190, 170, 255)) # Moon
draw.ellipse([(cx - 110, cy + 30), (cx - 98, cy + 42)], fill=(210, 90, 50, 255)) # Mars

# Camera viewport rectangle on minimap
draw.rectangle([(cx - 40, cy - 65), (cx + 50, cy - 20)], outline=(180, 220, 255, 255), width=2)
draw.text((mm_x + 12, mm_y + 10), "SOL ORBITAL TELEMETRY", fill=(0, 240, 255, 255), font=font_sub)

# 5. Bottom-Right Tactical Terrain & Sector Info HUD (Shin Gihren's Greed Box)
hud_w, hud_h = 320, 130
hud_x = 1280 - hud_w - 24
hud_y = 720 - hud_h - 24
draw.rectangle([(hud_x, hud_y), (hud_x + hud_w, hud_y + hud_h)], fill=(225, 228, 235, 255), outline=(30, 40, 50, 255), width=3)

# Title Header
draw.rectangle([(hud_x + 6, hud_y + 6), (hud_x + hud_w - 6, hud_y + 36)], fill=(240, 242, 248, 255))
draw.text((hud_x + 16, hud_y + 10), "DEEP SPACE // L5 SECTOR", fill=(10, 20, 35, 255), font=font_bold)

# Stats Rows
draw.text((hud_x + 16, hud_y + 48), "DEFENSE RATING", fill=(20, 30, 45, 255), font=font_stat)
draw.text((hud_x + hud_w - 70, hud_y + 48), "80 %", fill=(0, 120, 180, 255), font=font_stat)

draw.text((hud_x + 16, hud_y + 72), "PARTICLE DENSITY", fill=(20, 30, 45, 255), font=font_stat)
draw.text((hud_x + hud_w - 70, hud_y + 72), "00 %", fill=(20, 30, 45, 255), font=font_stat)

draw.text((hud_x + 16, hud_y + 96), "GARRISON SQUADRONS", fill=(20, 30, 45, 255), font=font_stat)
draw.text((hud_x + hud_w - 70, hud_y + 96), "08 MS", fill=(180, 40, 20, 255), font=font_stat)

# Top Bar Title
draw.rectangle([(24, 18), (560, 56)], fill=(12, 18, 28, 230), outline=(0, 200, 240, 255), width=1)
draw.text((36, 26), "★ SHIN GIHREN'S GREED TACTICAL MAP BENCHMARK", fill=(0, 240, 255, 255), font=font_bold)

map_im.save(out_path)
print(f"✓ In-situ map mockup created successfully at {out_path}!")
