#!/usr/bin/env python3
"""
tools/generate_snes_portraits.py
Generates authentic Front Mission (SNES, 1995) style 16-bit retro character portraits:
- 64x64 native pixel resolution (with 128x128 integer scale exports)
- 16-color indexed militaristic palettes
- Classic retro details: boom microphones, flak collars, cybernetic optics, scars, dithering
- Exports reference visual assets to docs/assets/ and sprites/
"""

import os
from PIL import Image, ImageDraw

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# 16-Color Faction Palettes (Classic 90s Mecha Anime & Front Mission 1)
PALETTES = {
    "terran": {
        "bg": (28, 34, 38),
        "frame": (75, 88, 96),
        "frame_dark": (14, 18, 22),
        "skin_base": (214, 178, 142),
        "skin_shadow": (158, 118, 88),
        "skin_dark": (102, 72, 54),
        "uniform_base": (78, 92, 54),
        "uniform_shadow": (46, 58, 32),
        "uniform_highlight": (118, 138, 86),
        "hair_base": (70, 72, 78),
        "hair_shadow": (40, 42, 46),
        "metal_base": (142, 150, 160),
        "metal_dark": (70, 76, 84),
        "eye_col": (40, 90, 140),
        "scar_red": (160, 68, 68),
        "accent": (210, 180, 70) # Brass medals/insignia
    },
    "colony": {
        "bg": (20, 26, 42),
        "frame": (60, 85, 120),
        "frame_dark": (10, 14, 24),
        "skin_base": (230, 195, 165),
        "skin_shadow": (175, 135, 105),
        "skin_dark": (115, 85, 65),
        "uniform_base": (220, 228, 240),
        "uniform_shadow": (140, 155, 175),
        "uniform_highlight": (255, 255, 255),
        "hair_base": (210, 185, 120),
        "hair_shadow": (145, 120, 70),
        "metal_base": (80, 180, 215),
        "metal_dark": (35, 95, 125),
        "eye_col": (140, 90, 210), # Violet/amber
        "scar_red": (140, 70, 90),
        "accent": (60, 220, 255) # Cyan HUD optics
    },
    "syndicate": {
        "bg": (32, 22, 18),
        "frame": (110, 65, 40),
        "frame_dark": (18, 10, 8),
        "skin_base": (195, 145, 110),
        "skin_shadow": (135, 95, 70),
        "skin_dark": (85, 55, 40),
        "uniform_base": (155, 80, 40), # Rust orange
        "uniform_shadow": (90, 42, 20),
        "uniform_highlight": (215, 120, 60),
        "hair_base": (45, 40, 38),
        "hair_shadow": (25, 20, 18),
        "metal_base": (175, 140, 90), # Worn copper
        "metal_dark": (75, 55, 35),
        "eye_col": (190, 150, 40), # Yellow reaver eye
        "scar_red": (180, 50, 40), # Fresh slag burn
        "accent": (255, 140, 30) # Molten flare
    },
    "zaibatsu": {
        "bg": (16, 16, 24),
        "frame": (65, 50, 95),
        "frame_dark": (8, 6, 14),
        "skin_base": (220, 205, 195), # Pale cybernetic complexion
        "skin_shadow": (155, 140, 140),
        "skin_dark": (95, 80, 85),
        "uniform_base": (35, 35, 48), # Carbon-fiber black
        "uniform_shadow": (18, 18, 25),
        "uniform_highlight": (75, 75, 100),
        "hair_base": (25, 25, 35),
        "hair_shadow": (10, 10, 15),
        "metal_base": (190, 195, 210), # Chrome prosthetics
        "metal_dark": (85, 90, 105),
        "eye_col": (230, 40, 70), # Crimson cyber-optic
        "scar_red": (190, 50, 90), # Subdermal stitch
        "accent": (180, 60, 255) # Neon violet telemetry
    }
}

def draw_dither_rect(draw, x0, y0, x1, y1, col_a, col_b):
    """Draws classic 16-bit checkerboard dither pattern between two colors."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if (x + y) % 2 == 0:
                draw.point((x, y), fill=col_a)
            else:
                draw.point((x, y), fill=col_b)

def generate_snes_bust(palette_key, char_type="officer"):
    pal = PALETTES[palette_key]
    w, h = 64, 64
    img = Image.new("RGB", (w, h), pal["bg"])
    draw = ImageDraw.Draw(img)

    # 1. Beveled SNES Outer Frame
    draw.rectangle([0, 0, 63, 63], outline=pal["frame"])
    draw.rectangle([1, 1, 62, 62], outline=pal["frame_dark"])
    
    # 2. Background Shading / Vignette
    draw_dither_rect(draw, 2, 2, 61, 14, pal["bg"], pal["frame_dark"])

    # 3. Uniform / Flak Jacket Torso Bust (Y: 42 to 61)
    # High collar flight jacket
    draw.polygon([(10, 61), (18, 44), (45, 44), (53, 61)], fill=pal["uniform_base"])
    # Collar folds and shadows
    draw.polygon([(18, 44), (26, 44), (22, 54)], fill=pal["uniform_highlight"])
    draw.polygon([(37, 44), (45, 44), (41, 54)], fill=pal["uniform_highlight"])
    draw.polygon([(26, 48), (37, 48), (32, 61)], fill=pal["uniform_shadow"])
    # Front zipper / ballistic flak seam
    draw.line([(31, 48), (31, 61)], fill=pal["metal_dark"])
    draw.line([(32, 48), (32, 61)], fill=pal["metal_base"])

    # Faction Accents on Collar
    if palette_key == "terran":
        # Brass eagle insignia pin
        draw.rectangle([20, 52, 23, 55], fill=pal["accent"])
    elif palette_key == "colony":
        # Aristocratic cravat pin
        draw.polygon([(30, 50), (33, 50), (32, 54)], fill=pal["accent"])
    elif palette_key == "syndicate":
        # Spiked reaver chain on collar
        for cx in [16, 20, 43, 47]:
            draw.point((cx, 50), fill=pal["metal_base"])
            draw.point((cx, 51), fill=pal["metal_dark"])
    elif palette_key == "zaibatsu":
        # Neon data collar seam
        draw.line([(18, 44), (18, 56)], fill=pal["accent"])
        draw.line([(45, 44), (45, 56)], fill=pal["accent"])

    # 4. Neck & Chin (Y: 36 to 46)
    draw.rectangle([26, 38, 37, 46], fill=pal["skin_shadow"])
    draw_dither_rect(draw, 26, 42, 37, 45, pal["skin_shadow"], pal["skin_dark"])

    # 5. Head & Facial Structure (Y: 16 to 40)
    # Jawline and cheeks
    draw.polygon([(20, 24), (43, 24), (40, 39), (32, 43), (23, 39)], fill=pal["skin_base"])
    # Jaw shadow (right side)
    draw.polygon([(34, 30), (43, 24), (40, 39), (32, 43)], fill=pal["skin_shadow"])
    # Dithered cheek shadow
    draw_dither_rect(draw, 33, 32, 38, 38, pal["skin_base"], pal["skin_shadow"])

    # 6. Facial Features (Eyes, Eyebrows, Nose, Mouth)
    # Severe Eyebrows
    draw.line([(22, 23), (28, 24)], fill=pal["hair_shadow"], width=1)
    draw.line([(35, 24), (41, 23)], fill=pal["hair_shadow"], width=1)

    # Eyes (Left & Right)
    # Sclera
    draw.rectangle([23, 26, 27, 28], fill=(230, 230, 230))
    draw.point((26, 27), fill=pal["eye_col"]) # Left Iris
    draw.point((25, 26), fill=(10, 10, 10)) # Left Pupil

    if palette_key == "zaibatsu" or char_type == "cyborg":
        # CYBERNETIC RIGHT EYE (Tachyon Glowing Optic Lens)
        draw.rectangle([36, 25, 41, 29], fill=pal["metal_dark"])
        draw.rectangle([37, 26, 40, 28], fill=pal["accent"])
        draw.point((38, 27), fill=(255, 255, 255)) # Glowing center pupil
        # Connecting cyber-bracket wire
        draw.line([(41, 27), (45, 26)], fill=pal["metal_base"])
    elif palette_key == "syndicate" and char_type == "reaver":
        # REAVER EYE-PATCH
        draw.polygon([(35, 25), (41, 25), (40, 30), (36, 30)], fill=(20, 18, 16))
        draw.line([(34, 23), (43, 32)], fill=(40, 35, 30)) # Strap
    else:
        # Standard Right Eye
        draw.rectangle([36, 26, 40, 28], fill=(230, 230, 230))
        draw.point((38, 27), fill=pal["eye_col"])
        draw.point((37, 26), fill=(10, 10, 10))

    # Nose (Classic angular Front Mission bridge)
    draw.line([(31, 25), (32, 32)], fill=pal["skin_shadow"])
    draw.line([(30, 33), (33, 33)], fill=pal["skin_dark"])

    # Mouth (Determined, grim or smirking line)
    if char_type == "reaver":
        draw.line([(27, 38), (36, 36)], fill=pal["skin_dark"]) # Snarl
    else:
        draw.line([(28, 38), (35, 38)], fill=pal["skin_dark"]) # Stoic straight line
        draw.point((32, 39), fill=pal["skin_shadow"]) # Lower lip shadow

    # Battle Scars
    if palette_key in ["terran", "syndicate"]:
        # Shrapnel scar across cheek
        draw.line([(21, 28), (26, 35)], fill=pal["scar_red"])
        draw.point((23, 31), fill=(240, 180, 180)) # Highlight stitch

    # 7. Hair & Headgear (Y: 10 to 24)
    if char_type == "officer":
        # Officer Cap (Terran / Colony)
        draw.polygon([(16, 17), (47, 17), (45, 11), (18, 11)], fill=pal["uniform_base"])
        # Cap Peak / Visor shadow
        draw.polygon([(15, 17), (48, 17), (44, 20), (19, 20)], fill=pal["metal_dark"])
        draw.line([(20, 18), (43, 18)], fill=pal["accent"]) # Gold cap strap
    else:
        # Spiky / Rugged Pilot Hair
        draw.polygon([(18, 22), (23, 12), (32, 10), (41, 13), (45, 22)], fill=pal["hair_base"])
        # Hair shadow and strands
        draw.polygon([(30, 12), (38, 13), (43, 20)], fill=pal["hair_shadow"])
        draw.line([(23, 18), (25, 23)], fill=pal["hair_shadow"])
        draw.line([(31, 16), (33, 21)], fill=pal["hair_shadow"])

    # 8. Retro Front Mission Communications Headset (Left Ear & Boom Mic)
    # Headset Earcup (Left)
    draw.rectangle([16, 24, 20, 32], fill=pal["metal_dark"])
    draw.rectangle([17, 25, 19, 31], fill=pal["metal_base"])
    # Headband arc over top
    draw.arc([16, 8, 47, 24], start=180, end=360, fill=pal["metal_dark"])
    # Boom Microphone extending to mouth corner
    draw.line([(18, 32), (22, 37)], fill=pal["metal_dark"])
    draw.line([(22, 37), (26, 38)], fill=pal["metal_base"])
    draw.rectangle([25, 37, 27, 39], fill=pal["metal_dark"]) # Mic capsule
    # Coiled Wire dropping down into collar
    draw.line([(19, 33), (17, 39)], fill=(40, 40, 45))
    draw.line([(17, 39), (20, 44)], fill=(40, 40, 45))

    return img

def export_all():
    print("=== GENERATING FRONT MISSION SNES RETRO CHARACTER PORTRAITS ===")
    
    # 1. Terran Coalition - General Vance / Marcus Cole
    im_terran = generate_snes_bust("terran", "officer")
    p_terran = os.path.join(ASSETS_DIR, "snes_portrait_terran_vance.png")
    im_terran.save(p_terran)
    # Integer 2x scale (128x128)
    im_terran.resize((128, 128), Image.Resampling.NEAREST).save(os.path.join(ASSETS_DIR, "snes_portrait_terran_vance_2x.png"))
    print(f"✓ Exported: {p_terran} (64x64 & 128x128)")

    # 2. Colony League - Fleet Commander Cassian Vane
    im_colony = generate_snes_bust("colony", "officer")
    p_colony = os.path.join(ASSETS_DIR, "snes_portrait_colony_cassian.png")
    im_colony.save(p_colony)
    im_colony.resize((128, 128), Image.Resampling.NEAREST).save(os.path.join(ASSETS_DIR, "snes_portrait_colony_cassian_2x.png"))
    print(f"✓ Exported: {p_colony} (64x64 & 128x128)")

    # 3. Syndicate Cartel - Jax 'Jackal' Vance
    im_synd = generate_snes_bust("syndicate", "reaver")
    p_synd = os.path.join(ASSETS_DIR, "snes_portrait_syndicate_jackal.png")
    im_synd.save(p_synd)
    im_synd.resize((128, 128), Image.Resampling.NEAREST).save(os.path.join(ASSETS_DIR, "snes_portrait_syndicate_jackal_2x.png"))
    print(f"✓ Exported: {p_synd} (64x64 & 128x128)")

    # 4. Zaibatsu Corp - Null-07 (Ren)
    im_zaib = generate_snes_bust("zaibatsu", "cyborg")
    p_zaib = os.path.join(ASSETS_DIR, "snes_portrait_zaibatsu_null07.png")
    im_zaib.save(p_zaib)
    im_zaib.resize((128, 128), Image.Resampling.NEAREST).save(os.path.join(ASSETS_DIR, "snes_portrait_zaibatsu_null07_2x.png"))
    print(f"✓ Exported: {p_zaib} (64x64 & 128x128)")

    # 5. Composite 4-Portrait SNES Strip (256x64)
    strip = Image.new("RGB", (256, 64), (0, 0, 0))
    strip.paste(im_terran, (0, 0))
    strip.paste(im_colony, (64, 0))
    strip.paste(im_synd, (128, 0))
    strip.paste(im_zaib, (192, 0))
    p_strip = os.path.join(ASSETS_DIR, "snes_faction_portraits_strip4.png")
    strip.save(p_strip)
    strip.resize((512, 128), Image.Resampling.NEAREST).save(os.path.join(ASSETS_DIR, "snes_faction_portraits_strip4_2x.png"))
    print(f"✓ Exported: {p_strip} (256x64 & 512x128 Strip)")

if __name__ == "__main__":
    export_all()
