from PIL import Image
import os

out_dir = "/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_units"
os.makedirs(out_dir, exist_ok=True)

img_ms = Image.open("/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/ms_tactical_sheet_1792504765608.jpg").convert("RGBA")
img_veh = Image.open("/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/veh_inf_sheet_1792504787023.jpg").convert("RGBA")
img_hex = Image.open("/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_hex_chits_1792504806606.jpg").convert("RGBA")

def remove_black_bg(im, threshold=30):
    datas = im.getdata()
    newData = []
    for item in datas:
        # Check if near black
        if item[0] < threshold and item[1] < threshold and item[2] < threshold:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)
    im.putdata(newData)
    return im

def auto_crop_and_fit(im, target_size=(64, 64), padding=4):
    bbox = im.getbbox()
    if not bbox:
        return im.resize(target_size)
    cropped = im.crop(bbox)
    
    avail_w = target_size[0] - padding * 2
    avail_h = target_size[1] - padding * 2
    cw, ch = cropped.size
    ratio = min(avail_w / cw, avail_h / ch)
    new_w = max(1, int(cw * ratio))
    new_h = max(1, int(ch * ratio))
    
    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", target_size, (0, 0, 0, 0))
    offset_x = (target_size[0] - new_w) // 2
    offset_y = target_size[1] - padding - new_h
    canvas.paste(resized, (offset_x, offset_y), resized)
    return canvas

# 1. Slice Mobile Suits
ms_boxes = {
    "spr_mini_ms_ironclad": (5, 50, 320, 440),         # Main Battle Bipedal
    "spr_mini_ms_aerostriker": (340, 70, 670, 440),     # Aero Flight
    "spr_mini_ms_artillery": (660, 50, 995, 440),       # Tread Artillery
    "spr_mini_ms_grunt": (5, 540, 310, 950),            # Frontline Recon Grunt
    "spr_mini_ms_hoversniper": (240, 530, 670, 910),    # Hover Sniper
    "spr_mini_ms_commander": (650, 560, 1000, 930)     # Ace Custom
}

print("Slicing Mobile Suits...")
for name, box in ms_boxes.items():
    crop = img_ms.crop(box)
    clean = remove_black_bg(crop, threshold=32)
    fit_64 = auto_crop_and_fit(clean, (64, 64), padding=3)
    fit_64.save(os.path.join(out_dir, f"{name}.png"))
    print(f"  Saved {name}.png (64x64 transparent)")

# 2. Slice Vehicles and Infantry
veh_boxes = {
    "spr_mini_veh_heavy_tank": (15, 48, 195, 175),       # Goliath Heavy Tank
    "spr_mini_veh_gunship": (15, 240, 195, 375),         # Wyvern Gunship
    "spr_mini_veh_technical": (15, 445, 195, 575),       # ATV-4 Technical
    "spr_mini_veh_dropship": (15, 625, 210, 775),        # LC-9 Dropship Carrier
    "spr_mini_inf_exo_squad": (8, 840, 240, 960)         # Mechanized Exo-Squad (trio)
}

print("Slicing Conventional Vehicles & Infantry...")
for name, box in veh_boxes.items():
    crop = img_veh.crop(box)
    clean = remove_black_bg(crop, threshold=36)
    fit_64 = auto_crop_and_fit(clean, (64, 64), padding=3)
    fit_64.save(os.path.join(out_dir, f"{name}.png"))
    print(f"  Saved {name}.png (64x64 transparent)")

# 3. Slice Hex Bases & Tactical UI
hex_boxes = {
    "spr_hex_base_terran": (15, 15, 320, 240),
    "spr_hex_base_colony": (350, 15, 650, 240),
    "spr_hex_base_syndicate": (15, 260, 320, 480),
    "spr_hex_base_zaibatsu": (350, 260, 650, 480),
    "spr_hex_base_sidereal": (15, 510, 320, 730),
    "spr_hex_base_mars": (350, 510, 650, 730),
    "spr_hex_base_pmc": (15, 760, 320, 980),
    "spr_tactical_bracket": (840, 20, 980, 150)
}

print("Slicing Hex Plinths & Reticle...")
for name, box in hex_boxes.items():
    crop = img_hex.crop(box)
    clean = remove_black_bg(crop, threshold=25)
    fit = auto_crop_and_fit(clean, (64, 48), padding=1)
    fit.save(os.path.join(out_dir, f"{name}.png"))
    print(f"  Saved {name}.png (64x48 transparent)")

print("✓ All tactical unit sprites and hex plinths extracted successfully!")
