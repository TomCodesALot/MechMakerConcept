from PIL import Image, ImageDraw, ImageFont
import os

brain_dir = "/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e"
units_dir = os.path.join(brain_dir, "tactical_units")
gw, gh = 1366, 768

try:
    f_modal_h = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 14)
    f_modal_body = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 12)
    f_modal_bold = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 12)
    f_hud = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf", 11)
except:
    f_modal_h = f_modal_body = f_modal_bold = f_hud = ImageFont.load_default()

# 1. Render Directive Modal with Dual Choices (Auto vs Manual Sortie)
base_p = os.path.join(brain_dir, "live_order_dispatch_mode.png")
im = Image.open(base_p).convert("RGBA")
draw = ImageDraw.Draw(im)

overlay = Image.new("RGBA", (gw, gh), (0, 0, 0, 185))
im.paste(overlay, (0, 0), overlay)

omw, omh = 660, 430
omx = (gw - omw) // 2
omy = (gh - omh) // 2

# Modal panel
draw.rectangle([omx, omy, omx + omw, omy + omh], fill=(12, 18, 28), outline=(0, 240, 255), width=2)
draw.rectangle([omx, omy, omx + omw, omy + 28], fill=(20, 48, 76))
draw.text((omx + 16, omy + 6), "TACTICAL OPERATION DIRECTIVE // VANGUARD ORDERS", font=f_modal_h, fill=(0, 240, 255))

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

# TRIPLE ACTION BUTTONS: Auto-Dispatch, Manual Sortie, Abort
by = omy + 346

# 1. Auto-Dispatch Button
draw.rectangle([omx + 20, by, omx + 208, by + 44], fill=(20, 54, 88), outline=(0, 240, 255))
draw.text((omx + 32, by + 12), "⚡ AUTO-DISPATCH", font=f_modal_bold, fill=(0, 240, 255))

# 2. Manual Tactical Sortie Button
draw.rectangle([omx + 224, by, omx + 440, by + 44], fill=(70, 48, 14), outline=(255, 215, 60), width=2)
draw.text((omx + 240, by + 12), "⚔️ MANUAL SORTIE (rm_combat)", font=f_modal_bold, fill=(255, 225, 100))

# 3. Abort Button
draw.rectangle([omx + 456, by, omx + omw - 20, by + 44], fill=(45, 18, 18), outline=(255, 90, 80))
draw.text((omx + 490, by + 12), "✖ ABORT [ESC]", font=f_modal_bold, fill=(255, 110, 110))

out_modal_p = os.path.join(brain_dir, "live_directive_modal_dual_choice.png")
im.save(out_modal_p)
print("Saved:", out_modal_p)

# 2. Render Tactical Battle Arena with Sector Biome & Defending OPFOR
im2 = Image.new("RGBA", (gw, gh), (8, 12, 18, 255))
draw2 = ImageDraw.Draw(im2)

# Isometric Grid
grid_ox, grid_oy = gw // 2, 160
for r in range(16):
    for c in range(16):
        px = grid_ox + (c - r) * 28
        py = grid_oy + (c + r) * 14
        pts = [(px, py), (px + 28, py + 14), (px, py + 28), (px - 28, py + 14)]
        draw2.polygon(pts, fill=(18, 32, 48) if (c + r) % 2 == 0 else (14, 26, 40), outline=(28, 54, 76))

# Top Battle Banner with Sector Context
draw2.rectangle([16, 12, gw - 16, 68], fill=(12, 18, 28), outline=(0, 240, 255), width=2)
draw2.rectangle([16, 12, 22, 68], fill=(40, 220, 180)) # Colonial Teal
draw2.text((32, 20), "SECTOR BATTLEGROUND // AETHELGARD PRIME CLUSTER (L4) FRONT", font=f_modal_h, fill=(0, 240, 255))
draw2.text((32, 42), "[SPACE THEATER // DEFENSE ENVELOPE: 82 DEF // GARRISON: AETHELGARD 1ST AEROSPACE PLATOON // BIOME: COLONY CYLINDER SHELL]", font=f_hud, fill=(40, 220, 180))

# Allied Squad on West Edge
ms_p_iron = Image.open(os.path.join(units_dir, "spr_mini_ms_ironclad.png")).convert("RGBA")
for i in range(3):
    ax = grid_ox - 180 + i * 40
    ay = grid_oy + 120 + i * 30
    draw2.ellipse([ax - 20, ay + 6, ax + 20, ay + 24], fill=(0, 200, 255, 60), outline=(0, 240, 255))
    im2.paste(ms_p_iron, (ax - 24, ay - 24), ms_p_iron)
    draw2.text((ax - 28, ay - 36), f"Alpha-0{i+1}", font=f_hud, fill=(0, 240, 255))

# Hostile Colonial Cohort on East Edge
ms_p_aero = Image.open(os.path.join(units_dir, "spr_mini_ms_aerostriker.png")).convert("RGBA")
for i in range(3):
    ex = grid_ox + 160 - i * 40
    ey = grid_oy + 80 + i * 34
    draw2.ellipse([ex - 20, ey + 6, ex + 20, ey + 24], fill=(40, 220, 180, 60), outline=(40, 220, 180))
    im2.paste(ms_p_aero, (ex - 24, ey - 24), ms_p_aero)
    draw2.text((ex - 36, ey - 36), f"Colony Aero-0{i+1}", font=f_hud, fill=(40, 220, 180))

# Bottom Combat Console HUD
draw2.rectangle([16, gh - 96, gw - 16, gh - 16], fill=(10, 16, 26), outline=(35, 65, 100))
draw2.rectangle([24, gh - 88, 380, gh - 24], fill=(14, 22, 34), outline=(0, 240, 255))
draw2.text((36, gh - 80), "SELECTED: Alpha-01 'WARHAMMER' [AP: 6/6]", font=f_modal_bold, fill=(255, 255, 255))
draw2.text((36, gh - 60), "120mm Kinetic Cannon [AP: 3]  |  Ares Missiles [AP: 4]", font=f_hud, fill=(160, 200, 240))
draw2.text((36, gh - 42), "HEAT: 0.0%  |  ARMOR: 680/680 Titanium-Carbide", font=f_hud, fill=(80, 255, 140))

draw2.rectangle([gw - 280, gh - 88, gw - 24, gh - 24], fill=(20, 60, 40), outline=(80, 255, 150))
draw2.text((gw - 264, gh - 62), ">> END PLAYER TURN [SPACE] >>", font=f_modal_bold, fill=(255, 255, 255))

out_arena_p = os.path.join(brain_dir, "live_tactical_arena_sector_integration.png")
im2.save(out_arena_p)
print("Saved:", out_arena_p)
