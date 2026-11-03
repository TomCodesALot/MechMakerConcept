from PIL import Image, ImageDraw, ImageFont
import os

units_dir = "/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_units"
out_path = "/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_counters_showcase.png"

# Canvas: 1100 x 680
canvas_w = 1140
canvas_h = 720
showcase = Image.new("RGBA", (canvas_w, canvas_h), (8, 12, 18, 255))
draw = ImageDraw.Draw(showcase)

# Draw dark grid
for x in range(0, canvas_w, 40):
    draw.line([(x, 0), (x, canvas_h)], fill=(16, 24, 34, 255))
for y in range(0, canvas_h, 40):
    draw.line([(0, y), (canvas_w, y)], fill=(16, 24, 34, 255))

# Header Panel
draw.rectangle([(16, 14), (canvas_w - 16, 68)], fill=(12, 20, 32, 255), outline=(0, 200, 240, 255), width=2)
# Left cyan strip
draw.rectangle([(16, 14), (22, 68)], fill=(0, 240, 255, 255))

# Try default or truetype font
try:
    font_title = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 18)
    font_sub = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 12)
    font_badge = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 14)
    font_label = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 11)
    font_desc = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 10)
except:
    font_title = font_sub = font_badge = font_label = font_desc = ImageFont.load_default()

draw.text((32, 22), "SOL THEATER WAR MAP // TACTICAL UNIT COUNTERS & PLINTH SYSTEM", fill=(0, 240, 255, 255), font=font_title)
draw.text((32, 44), "Inspired by Shin Gihren's Greed & Front Mission: Micro-Scale Miniatures with Faction Bases & Stack Numbers", fill=(160, 195, 230, 255), font=font_sub)

# Function to render a single composite counter (Hex Base + Unit Sprite + Stack Badge)
def make_counter(unit_name, base_name, stack_str="4", scale=1.5):
    u_path = os.path.join(units_dir, f"{unit_name}.png")
    b_path = os.path.join(units_dir, f"{base_name}.png")
    
    im_u = Image.open(u_path).convert("RGBA")
    im_b = Image.open(b_path).convert("RGBA")
    
    # Target size: 96x96
    cw, ch = 96, 96
    tile = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    
    # 1. Paste Base at bottom
    base_w, base_h = 76, 52
    b_resized = im_b.resize((base_w, base_h), Image.Resampling.LANCZOS)
    bx = (cw - base_w) // 2
    by = ch - base_h - 4
    tile.paste(b_resized, (bx, by), b_resized)
    
    # 2. Paste Unit standing on base
    uw, uh = 68, 68
    u_resized = im_u.resize((uw, uh), Image.Resampling.LANCZOS)
    ux = (cw - uw) // 2
    uy = by - uh + 32  # anchor onto plinth
    tile.paste(u_resized, (ux, uy), u_resized)
    
    # 3. Stack Number Badge (cyan digit on dark pill)
    t_draw = ImageDraw.Draw(tile)
    badge_x = bx + base_w - 22
    badge_y = by + 12
    t_draw.rectangle([(badge_x, badge_y), (badge_x + 18, badge_y + 20)], fill=(8, 16, 24, 230), outline=(0, 240, 255, 255), width=1)
    t_draw.text((badge_x + 5, badge_y + 3), stack_str, fill=(0, 255, 220, 255), font=font_badge)
    
    return tile

# --- SECTION 1: MOBILE SUIT COMBAT UNITS (Top Half) ---
sec1_y = 80
draw.rectangle([(16, sec1_y), (canvas_w - 16, sec1_y + 280)], fill=(12, 18, 26, 200), outline=(35, 60, 95, 255), width=1)
draw.text((28, sec1_y + 8), "1. MOBILE SUIT CHASSIS MINIATURES (64x64 Tactical Counters)", fill=(255, 215, 80, 255), font=font_label)

ms_showcase_list = [
    ("spr_mini_ms_ironclad", "spr_hex_base_terran", "6", "GHA-07 Ironclad", "Terran Main Battle MS", "Solid ballistic armor, rifle & shield"),
    ("spr_mini_ms_aerostriker", "spr_hex_base_colony", "4", "Aero-Striker V2", "Colony Flight Skirmisher", "Swept-wing thrusters, beam carbine"),
    ("spr_mini_ms_artillery", "spr_hex_base_syndicate", "3", "Mammoth-Tread MS", "Syndicate Siege Frame", "Dual 203mm cannons, tank treads"),
    ("spr_mini_ms_hoversniper", "spr_hex_base_zaibatsu", "4", "Kurogane Specter", "Zaibatsu Hover Sniper", "Flared thruster skirt, long railgun"),
    ("spr_mini_ms_commander", "spr_hex_base_mars", "1", "Tharsis Redoubt Ace", "Mars Command Consensus", "Sensor crest, high-output binders"),
    ("spr_mini_ms_grunt", "spr_hex_base_pmc", "6", "Iron Ridge Custom", "Player PMC Vanguard", "High-spec tuned frontline custom")
]

card_w = 176
card_h = 230
for i, (u_id, b_id, stk, title, role, desc) in enumerate(ms_showcase_list):
    cx = 28 + i * (card_w + 8)
    cy = sec1_y + 34
    
    # Card Background
    draw.rectangle([(cx, cy), (cx + card_w, cy + card_h)], fill=(15, 24, 36, 240), outline=(40, 75, 115, 255), width=1)
    
    # Counter Sprite
    counter_im = make_counter(u_id, b_id, stk)
    showcase.paste(counter_im, (cx + (card_w - 96)//2, cy + 8), counter_im)
    
    # Text info
    draw.text((cx + 10, cy + 116), title, fill=(255, 255, 255, 255), font=font_label)
    draw.text((cx + 10, cy + 134), role, fill=(0, 220, 255, 255), font=font_desc)
    draw.text((cx + 10, cy + 154), desc, fill=(160, 190, 220, 255), font=font_desc)
    
    # Hex Badge Pill
    draw.rectangle([(cx + 10, cy + 196), (cx + card_w - 10, cy + 218)], fill=(10, 16, 24, 255), outline=(0, 180, 220, 255), width=1)
    draw.text((cx + 16, cy + 201), f"STACK: [{stk}] UNITS", fill=(255, 220, 100, 255), font=font_desc)

# --- SECTION 2: CONVENTIONAL SUPPORT & INFANTRY (Bottom Half) ---
sec2_y = 376
draw.rectangle([(16, sec2_y), (canvas_w - 16, sec2_y + 328)], fill=(12, 18, 26, 200), outline=(35, 60, 95, 255), width=1)
draw.text((28, sec2_y + 8), "2. CONVENTIONAL FORCES, LOGISTICS & FACTION TACTICAL PLINTHS", fill=(255, 215, 80, 255), font=font_label)

veh_showcase_list = [
    ("spr_mini_veh_heavy_tank", "spr_hex_base_terran", "8", "MB-88 Goliath", "Terran Heavy Tank", "Dual 150mm heavy turret"),
    ("spr_mini_veh_gunship", "spr_hex_base_colony", "6", "SV-13 Wyvern", "Colony Strike Gunship", "VTOL twin-engine missile craft"),
    ("spr_mini_veh_technical", "spr_hex_base_syndicate", "8", "ATV-4 Scout", "Syndicate Recon Technical", "6-wheel armored buggy & cannon"),
    ("spr_mini_veh_dropship", "spr_hex_base_sidereal", "2", "LC-9 Skyhook", "Sidereal Drop Carrier", "Orbital troop/MS transport"),
    ("spr_mini_inf_exo_squad", "spr_hex_base_pmc", "9", "Exo-Shock Squad", "PMC Mechanized Infantry", "Armored trio with anti-MS rocket")
]

for i, (u_id, b_id, stk, title, role, desc) in enumerate(veh_showcase_list):
    cx = 28 + i * (card_w + 8)
    cy = sec2_y + 34
    
    draw.rectangle([(cx, cy), (cx + card_w, cy + card_h)], fill=(15, 24, 36, 240), outline=(40, 75, 115, 255), width=1)
    
    counter_im = make_counter(u_id, b_id, stk)
    showcase.paste(counter_im, (cx + (card_w - 96)//2, cy + 8), counter_im)
    
    draw.text((cx + 10, cy + 116), title, fill=(255, 255, 255, 255), font=font_label)
    draw.text((cx + 10, cy + 134), role, fill=(0, 220, 255, 255), font=font_desc)
    draw.text((cx + 10, cy + 154), desc, fill=(160, 190, 220, 255), font=font_desc)
    
    draw.rectangle([(cx + 10, cy + 196), (cx + card_w - 10, cy + 218)], fill=(10, 16, 24, 255), outline=(0, 180, 220, 255), width=1)
    draw.text((cx + 16, cy + 201), f"STACK: [{stk}] UNITS", fill=(255, 220, 100, 255), font=font_desc)

# 6th Column on bottom row: Faction Plinth Legend & Reticle
leg_x = 28 + 5 * (card_w + 8)
leg_y = sec2_y + 34
draw.rectangle([(leg_x, leg_y), (leg_x + card_w, leg_y + card_h + 38)], fill=(14, 22, 34, 255), outline=(0, 220, 255, 255), width=1)
draw.text((leg_x + 10, leg_y + 10), "FACTION PLINTHS", fill=(0, 240, 255, 255), font=font_label)

plinths = [
    ("TERRAN BLUE", (60, 140, 255)),
    ("COLONY TEAL", (40, 220, 180)),
    ("SYNDICATE GOLD", (255, 160, 40)),
    ("ZAIBATSU VIOLET", (180, 90, 240)),
    ("SIDEREAL INDIGO", (120, 130, 240)),
    ("MARS CRIMSON", (240, 60, 60)),
    ("PMC SOVEREIGN", (255, 215, 60))
]

for pi, (pname, pcol) in enumerate(plinths):
    py = leg_y + 36 + pi * 24
    draw.rectangle([(leg_x + 12, py), (leg_x + 24, py + 14)], fill=pcol, outline=(255, 255, 255, 200), width=1)
    draw.text((leg_x + 32, py), pname, fill=(220, 235, 250, 255), font=font_desc)

# Paste reticle bracket preview
im_br = Image.open(os.path.join(units_dir, "spr_tactical_bracket.png")).convert("RGBA")
br_w, br_h = 56, 42
im_br_scaled = im_br.resize((br_w, br_h), Image.Resampling.LANCZOS)
showcase.paste(im_br_scaled, (leg_x + 60, leg_y + 215), im_br_scaled)
draw.text((leg_x + 22, leg_y + 258), "SELECTION RETICLE ( )", fill=(0, 240, 255, 255), font=font_desc)

showcase.save(out_path)
print(f"✓ Showcase image generated successfully at {out_path}!")
