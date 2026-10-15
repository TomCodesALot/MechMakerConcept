import os
import json
import uuid
from PIL import Image, ImageDraw

ART_DIR = "/home/tom/.gemini/antigravity-ide/brain/9e7b4250-94ad-4463-8c59-22968ebafcd3"
SPRITES_DIR = "sprites"

LANDMARKS = {
    "vance": {
        "m": (100, 142, 26, 12),
        "le": (80, 75, 16, 10),
        "re": (118, 75, 16, 10),
        "skin_dy": -8,
        "teeth_color": (220, 212, 205, 255),
        "cavity_color": (28, 12, 16, 255),
        "tongue_color": (95, 42, 48, 255),
        "lash_color": (28, 20, 24, 255)
    },
    "cole": {
        "m": (98, 122, 26, 12),
        "le": (78, 72, 16, 10),
        "re": (116, 72, 16, 10),
        "skin_dy": -7,
        "teeth_color": (215, 208, 200, 255),
        "cavity_color": (26, 10, 14, 255),
        "tongue_color": (90, 38, 44, 255),
        "lash_color": (24, 18, 20, 255)
    },
    "cassian": {
        "m": (98, 140, 26, 12),
        "le": (78, 74, 16, 10),
        "re": (116, 74, 16, 10),
        "skin_dy": -8,
        "teeth_color": (225, 218, 210, 255),
        "cavity_color": (25, 10, 15, 255),
        "tongue_color": (92, 40, 46, 255),
        "lash_color": (26, 18, 22, 255)
    },
    "sorren": {
        "m": (100, 124, 26, 12),
        "le": (80, 75, 16, 10),
        "re": (118, 75, 16, 10),
        "skin_dy": -7,
        "teeth_color": (220, 215, 210, 255),
        "cavity_color": (28, 14, 18, 255),
        "tongue_color": (96, 44, 50, 255),
        "lash_color": (25, 20, 24, 255)
    },
    "cruz": {
        "m": (100, 132, 26, 12),
        "le": (78, 76, 16, 10),
        "re": (118, 76, 16, 10),
        "skin_dy": -8,
        "teeth_color": (218, 210, 202, 255),
        "cavity_color": (26, 12, 16, 255),
        "tongue_color": (92, 40, 45, 255),
        "lash_color": (24, 18, 22, 255)
    },
    "nadia": {
        "m": (98, 128, 26, 12),
        "le": (78, 86, 16, 10),
        "re": (116, 86, 16, 10),
        "skin_dy": -7,
        "teeth_color": (224, 216, 208, 255),
        "cavity_color": (28, 14, 18, 255),
        "tongue_color": (98, 45, 52, 255),
        "lash_color": (26, 20, 24, 255)
    },
    "renzo": {
        "m": (100, 142, 26, 12),
        "le": (82, 78, 16, 10),
        "re": (118, 78, 16, 10),
        "skin_dy": -8,
        "teeth_color": (222, 215, 208, 255),
        "cavity_color": (24, 10, 14, 255),
        "tongue_color": (88, 38, 44, 255),
        "lash_color": (25, 18, 22, 255)
    },
    "null07": {
        "m": (98, 120, 26, 12),
        "le": (78, 72, 16, 10),
        "re": (116, 72, 16, 10),
        "skin_dy": -7,
        "teeth_color": (218, 210, 205, 255),
        "cavity_color": (24, 12, 16, 255),
        "tongue_color": (90, 40, 46, 255),
        "lash_color": (22, 18, 20, 255)
    }
}

def generate_character_poses(name):
    cfg = LANDMARKS[name]
    base_path = os.path.join(ART_DIR, f"base_{name}.png")
    base = Image.open(base_path).convert("RGBA")
    
    mx, my, mw, mh = cfg["m"]
    lex, ley, lew, leh = cfg["le"]
    rex, rey, rew, reh = cfg["re"]
    
    # Sample skin tone
    skin_tone = base.getpixel((lex, ley + cfg["skin_dy"]))
    crease_tone = (max(0, skin_tone[0] - 38), max(0, skin_tone[1] - 32), max(0, skin_tone[2] - 28), 255)
    
    # --- Pose 0: Idle ---
    p0 = base.copy()
    
    # --- Pose 1: Mouth Slight Open (Talk 1) ---
    p1 = base.copy()
    draw1 = ImageDraw.Draw(p1)
    slit_w = int(mw * 0.62)
    # Oral cavity
    draw1.rectangle([mx - slit_w//2, my - 1, mx + slit_w//2, my + 1], fill=cfg["cavity_color"])
    # Upper teeth highlight
    teeth_w = int(slit_w * 0.75)
    draw1.line([mx - teeth_w//2, my - 1, mx + teeth_w//2, my - 1], fill=cfg["teeth_color"], width=1)
    # Lower lip slight drop
    lower_lip = base.crop((mx - mw//2, my + 1, mx + mw//2, my + 6))
    p1.paste(lower_lip, (mx - mw//2, my + 2), lower_lip)
    
    # --- Pose 2: Mouth Open (Talk 2) ---
    p2 = base.copy()
    draw2 = ImageDraw.Draw(p2)
    open_w = int(mw * 0.76)
    # Oral cavity
    draw2.rectangle([mx - open_w//2, my - 2, mx + open_w//2, my + 3], fill=cfg["cavity_color"])
    # Tongue highlight
    draw2.ellipse([mx - open_w//4, my + 1, mx + open_w//4, my + 3], fill=cfg["tongue_color"])
    # Upper teeth row
    draw2.line([mx - open_w//2 + 2, my - 2, mx + open_w//2 - 2, my - 2], fill=cfg["teeth_color"], width=1)
    # Lower lip shifted downward
    lower_lip2 = base.crop((mx - mw//2, my + 1, mx + mw//2, my + 8))
    p2.paste(lower_lip2, (mx - mw//2, my + 4), lower_lip2)
    
    # --- Pose 3: Half Blink ---
    p3 = base.copy()
    draw3 = ImageDraw.Draw(p3)
    for (ex, ey, ew, eh) in [(lex, ley, lew, leh), (rex, rey, rew, reh)]:
        top_y = ey - eh//2
        mid_y = ey
        # Draw eyelid over upper half
        draw3.rectangle([ex - ew//2, top_y, ex + ew//2, mid_y], fill=skin_tone)
        # Upper crease line
        draw3.line([ex - ew//2, top_y + 1, ex + ew//2, top_y + 1], fill=crease_tone, width=1)
        # Descending lash line
        draw3.line([ex - ew//2, mid_y, ex + ew//2, mid_y], fill=cfg["lash_color"], width=1)
        
    # --- Pose 4: Full Blink ---
    p4 = base.copy()
    draw4 = ImageDraw.Draw(p4)
    for (ex, ey, ew, eh) in [(lex, ley, lew, leh), (rex, rey, rew, reh)]:
        top_y = ey - eh//2
        bot_y = ey + eh//2
        # Draw full eyelid
        draw4.rectangle([ex - ew//2, top_y, ex + ew//2, bot_y], fill=skin_tone)
        # Upper crease line
        draw4.line([ex - ew//2, top_y + 2, ex + ew//2, top_y + 2], fill=crease_tone, width=1)
        # Closed lash line at bottom
        draw4.line([ex - ew//2, bot_y - 1, ex + ew//2, bot_y - 1], fill=cfg["lash_color"], width=1)
        
    # Construct 12-frame loop:
    # 0: Idle, 1: Talk 1, 2: Talk 2, 3: Talk 1, 4: Idle, 5: Idle,
    # 6: Blink Half, 7: Blink Full, 8: Blink Half, 9: Idle, 10: Idle, 11: Idle
    frames = [
        p0, # 0: Idle
        p1, # 1: Talk 1
        p2, # 2: Talk 2
        p1, # 3: Talk 1
        p0, # 4: Idle
        p0, # 5: Idle
        p3, # 6: Blink Half
        p4, # 7: Blink Full
        p3, # 8: Blink Half
        p0, # 9: Idle
        p0, # 10: Idle
        p0  # 11: Idle
    ]
    return frames

def update_gamemaker_sprite(name, frames):
    spr_dir = os.path.join(SPRITES_DIR, f"spr_portrait_{name}")
    yy_path = os.path.join(spr_dir, f"spr_portrait_{name}.yy")
    
    with open(yy_path, "r") as f:
        yy_data = json.load(f)
        
    layer_id = yy_data["layers"][0]["name"]
    orig_frame_id = yy_data["frames"][0]["name"]
    
    # Generate UUIDs for 12 frames, keeping original frame 0 UUID
    frame_uuids = [orig_frame_id] + [str(uuid.uuid4()) for _ in range(11)]
    
    # Write frames into sprite directory and layers
    layers_root = os.path.join(spr_dir, "layers")
    os.makedirs(layers_root, exist_ok=True)
    
    for idx, (frame_img, f_uuid) in enumerate(zip(frames, frame_uuids)):
        # Main frame PNG
        frame_png_path = os.path.join(spr_dir, f"{f_uuid}.png")
        frame_img.save(frame_png_path, "PNG")
        
        # Layer folder & PNG
        layer_frame_dir = os.path.join(layers_root, f_uuid)
        os.makedirs(layer_frame_dir, exist_ok=True)
        layer_png_path = os.path.join(layer_frame_dir, f"{layer_id}.png")
        frame_img.save(layer_png_path, "PNG")
        
    # Update yy_data structure
    yy_data["frames"] = [
        {
            "$GMSpriteFrame": "v1",
            "%Name": f_uuid,
            "name": f_uuid,
            "resourceType": "GMSpriteFrame",
            "resourceVersion": "2.0"
        }
        for f_uuid in frame_uuids
    ]
    
    # Sequence settings
    seq = yy_data["sequence"]
    seq["length"] = 12.0
    seq["playbackSpeed"] = 8.0
    seq["playbackSpeedType"] = 0
    
    # Track keyframes
    keyframes = []
    for idx, f_uuid in enumerate(frame_uuids):
        kf_uuid = str(uuid.uuid4())
        keyframes.append({
            "$Keyframe<SpriteFrameKeyframe>": "",
            "Channels": {
                "0": {
                    "$SpriteFrameKeyframe": "",
                    "Id": {
                        "name": f_uuid,
                        "path": f"sprites/spr_portrait_{name}/spr_portrait_{name}.yy"
                    },
                    "resourceType": "SpriteFrameKeyframe",
                    "resourceVersion": "2.0"
                }
            },
            "Disabled": False,
            "id": kf_uuid,
            "IsCreationKey": False,
            "Key": float(idx),
            "Length": 1.0,
            "resourceType": "Keyframe<SpriteFrameKeyframe>",
            "resourceVersion": "2.0",
            "Stretch": False
        })
        
    seq["tracks"][0]["keyframes"]["Keyframes"] = keyframes
    
    with open(yy_path, "w") as f:
        json.dump(yy_data, f, indent=2)
        
    print(f"[{name.upper()}] Successfully updated sprite with 12 frames at 8.0 FPS.")
    
    # Also save an animated GIF preview
    gif_path = os.path.join(ART_DIR, f"anim_{name}.gif")
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=125,
        loop=0
    )
    print(f"[{name.upper()}] Saved animated preview GIF: {gif_path}")

def main():
    print("=== GENERATING ANIMATED FRONT MISSION PORTRAITS ===")
    for name in ["vance", "cole", "cassian", "sorren", "cruz", "nadia", "renzo", "null07"]:
        frames = generate_character_poses(name)
        update_gamemaker_sprite(name, frames)
    print("=== ALL 8 PORTRAITS SUCCESSFULLY GENERATED & INTEGRATED ===")

if __name__ == "__main__":
    main()
