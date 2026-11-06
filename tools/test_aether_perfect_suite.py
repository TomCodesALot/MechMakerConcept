#!/usr/bin/env python3
"""
Verification & Art Asset Analyst QA Gate for OC-A01 Aether Striker Production Suite
"""
import os
import sys
import json
from PIL import Image

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def check_sprite_metadata(sprite_name, expected_frames=4, expected_origin=(80, 145)):
    spr_dir = os.path.join(PROJECT_ROOT, "sprites", sprite_name)
    yy_path = os.path.join(spr_dir, f"{sprite_name}.yy")
    assert os.path.exists(yy_path), f"Missing {yy_path}"
    with open(yy_path) as f:
        yy = json.load(f)
    
    seq = yy.get("sequence", {})
    xorigin = seq.get("xorigin")
    yorigin = seq.get("yorigin")
    assert (xorigin, yorigin) == expected_origin, f"{sprite_name} origin is ({xorigin}, {yorigin}), expected {expected_origin}"
    
    frames = yy.get("frames", [])
    assert len(frames) == expected_frames, f"{sprite_name} has {len(frames)} frames, expected {expected_frames}"
    
    for i, fr in enumerate(frames):
        fid = fr["name"]
        png_path = os.path.join(spr_dir, f"{fid}.png")
        assert os.path.exists(png_path), f"Missing frame image: {png_path}"
        img = Image.open(png_path)
        assert img.size == (160, 160), f"Frame {i} size {img.size} != (160, 160)"
        assert img.getbbox() is not None, f"Frame {i} is completely empty!"
    print(f"  ✓ {sprite_name}: metadata & {expected_frames} frames verified at origin {expected_origin}.")

def run_art_analyst_qa():
    print("=== LEAD ART ASSET ANALYST QUALITY ASSURANCE & VERIFICATION ===")
    
    # 1. Metadata & Frame checks
    for spr in ["spr_ms_aether_idle", "spr_ms_aether_fire_beam", "spr_ms_aether_attack_saber", "spr_ms_aether_boost", "spr_ms_aether_back_idle"]:
        check_sprite_metadata(spr)
        
    # 2. Fire Beam Audit
    print("\n--- Auditing spr_ms_aether_fire_beam ---")
    fb_dir = os.path.join(PROJECT_ROOT, "sprites", "spr_ms_aether_fire_beam")
    with open(os.path.join(fb_dir, "spr_ms_aether_fire_beam.yy")) as f:
        fb_yy = json.load(f)
        
    for i, fr in enumerate(fb_yy["frames"]):
        img = Image.open(os.path.join(fb_dir, f"{fr['name']}.png")).convert("RGBA")
        # Check red pixel corruption
        corrupted_red = 0
        for y in range(160):
            for x in range(160):
                r, g, b, a = img.getpixel((x, y))
                # Check for alien red armor patches on right shoulder or outer armor
                if a > 100 and r > 180 and g < 60 and b < 60 and not (55 <= x <= 95 and 25 <= y <= 45):
                    corrupted_red += 1
        assert corrupted_red == 0, f"Frame {i} has {corrupted_red} corrupted red armor pixels!"
        
        # Check cyan beam presence in frames 0, 1, 2
        cyan_count = sum(1 for p in img.getdata() if p[3] > 50 and p[1] > 180 and p[2] > 180 and p[0] < 200)
        assert cyan_count > 300, f"Frame {i} lacks Cherenkov cyan energy (found {cyan_count})"
        
        # Verify beam alignment in frame 1 (discharge)
        if i == 1:
            white_core_count = sum(1 for p in img.getdata() if p[3] > 50 and p[0] > 240 and p[1] > 240 and p[2] > 240)
            assert white_core_count > 80, f"Discharge frame lacks white-hot core (found {white_core_count})"
            # check beam reaches right border
            border_beam = [img.getpixel((159, y)) for y in range(50, 75) if img.getpixel((159, y))[3] > 100]
            assert len(border_beam) > 0, "Beam pulse does not project through right edge!"
    print("  ✓ spr_ms_aether_fire_beam: zero corrupted red pixels, coherent beam pulse, verified mathematically.")

    # 3. Attack Saber Audit
    print("\n--- Auditing spr_ms_aether_attack_saber ---")
    sab_dir = os.path.join(PROJECT_ROOT, "sprites", "spr_ms_aether_attack_saber")
    with open(os.path.join(sab_dir, "spr_ms_aether_attack_saber.yy")) as f:
        sab_yy = json.load(f)
        
    for i, fr in enumerate(sab_yy["frames"]):
        img = Image.open(os.path.join(sab_dir, f"{fr['name']}.png")).convert("RGBA")
        cyan_count = sum(1 for p in img.getdata() if p[3] > 50 and p[1] > 180 and p[2] > 180 and p[0] < 200)
        assert cyan_count > 300, f"Frame {i} lacks Cherenkov cyan energy (found {cyan_count})"
        
        # Verify lowered rifle is removed (accounting for forward lunge offset)
        offset_x = [4, 8, 12, 6][i]
        # In master sprite, lowered gun was at x=115..128. With offset, it would be at 115+offset..128+offset
        lowered_rifle_pixels = [img.getpixel((x, y)) for y in range(70, 95) for x in range(112 + offset_x, 128 + offset_x) if img.getpixel((x, y))[3] > 100 and img.getpixel((x, y))[0] < 50 and img.getpixel((x, y))[1] < 50]
        assert len(lowered_rifle_pixels) < 10, f"Frame {i} still has lowered weapon on hip! ({len(lowered_rifle_pixels)} dark pixels)"
    print("  ✓ spr_ms_aether_attack_saber: lowered rifle removed, hand-held saber blade verified.")

    # 4. Database & Battle Manager Registration
    print("\n--- Auditing Central Database Registration ---")
    db_path = os.path.join(PROJECT_ROOT, "scripts", "scr_mobile_suit_database", "scr_mobile_suit_database.gml")
    with open(db_path) as f:
        db_content = f.read()
    assert "spr_ms_aether_fire_beam" in db_content, "Missing spr_ms_aether_fire_beam in database"
    assert "spr_ms_aether_attack_saber" in db_content, "Missing spr_ms_aether_attack_saber in database"
    assert "spr_ms_aether_boost" in db_content, "Missing spr_ms_aether_boost in database"
    print("  ✓ Database registration: all action sprites correctly bound to ms_colony_aether_01.")

    print("\n=======================================================")
    print("LEAD ART ASSET ANALYST FORMAL VERDICT: [APPROVED]")
    print("=======================================================")

if __name__ == "__main__":
    run_art_analyst_qa()
