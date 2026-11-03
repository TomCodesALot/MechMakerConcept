import os
import shutil
import json
from PIL import Image

PROJECT_DIR = "/home/tom/GameMakerProjects/MechMakerConcept"
SPRITES_DIR = os.path.join(PROJECT_DIR, "sprites")
BRAIN_DIR = "/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e"

maps = {
    "spr_map_earth_theater": os.path.join(BRAIN_DIR, "earth_theater_map_1792505877305.jpg"),
    "spr_map_mars_theater": os.path.join(BRAIN_DIR, "mars_theater_map_1792505898931.jpg"),
    "spr_map_space_theater": os.path.join(BRAIN_DIR, "colony_space_map_1792505921644.jpg")
}

for spr_name, src_path in maps.items():
    spr_dir = os.path.join(SPRITES_DIR, spr_name)
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size
    
    # Save spr_name.png
    im.save(os.path.join(spr_dir, f"{spr_name}.png"))
    
    # Update frame PNGs in spr_dir and layers
    for fname in os.listdir(spr_dir):
        if fname.endswith(".png") and fname != f"{spr_name}.png":
            im.save(os.path.join(spr_dir, fname))
    
    layers_dir = os.path.join(spr_dir, "layers")
    if os.path.exists(layers_dir):
        for sub in os.listdir(layers_dir):
            sub_p = os.path.join(layers_dir, sub)
            if os.path.isdir(sub_p):
                for l_file in os.listdir(sub_p):
                    if l_file.endswith(".png"):
                        im.save(os.path.join(sub_p, l_file))
                        
    # Update .yy width, height, bbox
    yy_path = os.path.join(spr_dir, f"{spr_name}.yy")
    with open(yy_path, "r", encoding="utf-8") as f:
        yy = json.load(f)
    
    yy["width"] = w
    yy["height"] = h
    yy["bbox_right"] = w - 1
    yy["bbox_bottom"] = h - 1
    
    with open(yy_path, "w", encoding="utf-8") as f:
        json.dump(yy, f, indent=2)
        
    print(f"✓ Upgraded {spr_name} to massive HD map ({w}x{h})")

# Also crop amber world radar screen for minimap texture
amber_src = os.path.join(BRAIN_DIR, "earth_global_radar_1792505945860.jpg")
im_amb = Image.open(amber_src).convert("RGBA")
# Crop CRT inner screen: ~x: 120 to 1250, y: 70 to 920
screen_crop = im_amb.crop((120, 70, 1250, 920))
amber_out = os.path.join(BRAIN_DIR, "radar_earth_amber_screen.png")
screen_crop.save(amber_out)
print(f"✓ Cropped amber radar screen: {screen_crop.size} -> {amber_out}")

# Register spr_radar_earth_amber
import uuid
spr_name = "spr_radar_earth_amber"
from tools.import_tactical_counter_sprites import create_sprite
create_sprite(spr_name, amber_out)
print(f"✓ Created and registered {spr_name} in project!")
