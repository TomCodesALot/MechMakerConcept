#!/usr/bin/env python3
"""
tools/generate_commander_and_location_assets.py
Generates engine-ready 200x200 animated portraits for the Player Commander:
- spr_portrait_commander_male (12 frames animated)
- spr_portrait_commander_female (12 frames animated)
- spr_portrait_commander_silhouette (4 frames animated with tactical scanlines and encryption HUD)
And 1024x576 location environment backdrops:
- spr_loc_hangar_bay (Prototyping & Factory floor)
- spr_loc_war_room (War Map & Flagship Bridge)
Outputs full GameMaker Studio 2 sprite structures and registers in MechMakerConcept.yyp.
"""

import os
import json
import uuid
import math
from PIL import Image, ImageDraw

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITES_DIR = os.path.join(PROJECT_DIR, "sprites")
YYP_PATH = os.path.join(PROJECT_DIR, "MechMakerConcept.yyp")
BRAIN_DIR = "/home/tom/.gemini/antigravity-ide/brain/b8b31d33-92aa-4d09-a376-999bd161799d"

MALE_SRC = os.path.join(BRAIN_DIR, "commander_male_portrait_1792102582190.jpg")
FEMALE_SRC = os.path.join(BRAIN_DIR, "commander_female_portrait_1792102595554.jpg")
HANGAR_SRC = os.path.join(BRAIN_DIR, "loc_hangar_bay_1792102610132.jpg")
WAR_ROOM_SRC = os.path.join(BRAIN_DIR, "loc_war_room_1792102623402.jpg")

def register_in_yyp(spr_name):
    with open(YYP_PATH, "r") as f:
        content = f.read()
    
    target_path = f"sprites/{spr_name}/{spr_name}.yy"
    if target_path in content:
        return
    
    idx = content.find('"resources":')
    if idx != -1:
        bracket_idx = content.find('],', idx)
        if bracket_idx != -1:
            new_entry = '    {"id":{"name":"' + spr_name + '","path":"' + target_path + '",},},\n'
            content = content[:bracket_idx] + new_entry + content[bracket_idx:]
            with open(YYP_PATH, "w") as f:
                f.write(content)
            print(f"  ✓ Registered {spr_name} in MechMakerConcept.yyp")

def create_gmsprite_yy(spr_name, w, h, frames, layer_id):
    frame_objs = []
    keyframe_objs = []
    
    for idx, f_id in enumerate(frames):
        frame_objs.append({
            "$GMSpriteFrame": "v1",
            "%Name": f_id,
            "name": f_id,
            "resourceType": "GMSpriteFrame",
            "resourceVersion": "2.0"
        })
        keyframe_objs.append({
            "$Keyframe<SpriteFrameKeyframe>": "",
            "Channels": {
                "0": {
                    "$SpriteFrameKeyframe": "",
                    "Id": {
                        "name": f_id,
                        "path": f"sprites/{spr_name}/{spr_name}.yy"
                    },
                    "resourceType": "SpriteFrameKeyframe",
                    "resourceVersion": "2.0"
                }
            },
            "Disabled": False,
            "id": str(uuid.uuid4()),
            "IsCreationKey": False,
            "Key": float(idx),
            "Length": 1.0,
            "resourceType": "Keyframe<SpriteFrameKeyframe>",
            "resourceVersion": "2.0",
            "Stretch": False
        })
        
    yy = {
        "$GMSprite": "v2",
        "%Name": spr_name,
        "bboxMode": 0,
        "bbox_bottom": h - 1,
        "bbox_left": 0,
        "bbox_right": w - 1,
        "bbox_top": 0,
        "collisionKind": 1,
        "collisionTolerance": 0,
        "DynamicTexturePage": False,
        "edgeFiltering": False,
        "For3D": False,
        "frames": frame_objs,
        "gridX": 0,
        "gridY": 0,
        "height": h,
        "HTile": False,
        "layers": [
            {
                "$GMImageLayer": "",
                "%Name": layer_id,
                "blendMode": 0,
                "displayName": "default",
                "isLocked": False,
                "name": layer_id,
                "opacity": 100.0,
                "resourceType": "GMImageLayer",
                "resourceVersion": "2.0",
                "visible": True
            }
        ],
        "name": spr_name,
        "nineSlice": None,
        "origin": 0,
        "parent": {
            "name": "MechMakerConcept",
            "path": "MechMakerConcept.yyp"
        },
        "preMultiplyAlpha": False,
        "resourceType": "GMSprite",
        "resourceVersion": "2.0",
        "sequence": {
            "$GMSequence": "v1",
            "%Name": spr_name,
            "autoRecord": True,
            "backdropHeight": 768,
            "backdropImageOpacity": 0.5,
            "backdropImagePath": "",
            "backdropWidth": 1366,
            "backdropXOffset": 0.0,
            "backdropYOffset": 0.0,
            "events": {
                "$KeyframeStore<MessageEventKeyframe>": "",
                "Keyframes": [],
                "resourceType": "KeyframeStore<MessageEventKeyframe>",
                "resourceVersion": "2.0"
            },
            "eventStubScript": None,
            "eventToFunction": {},
            "length": float(len(frames)),
            "lockOrigin": False,
            "moments": {
                "$KeyframeStore<MomentsEventKeyframe>": "",
                "Keyframes": [],
                "resourceType": "KeyframeStore<MomentsEventKeyframe>",
                "resourceVersion": "2.0"
            },
            "name": spr_name,
            "playback": 1,
            "playbackSpeed": 12.0,
            "playbackSpeedType": 0,
            "showBackdrop": True,
            "showBackdropImage": False,
            "timeUnits": 1,
            "tracks": [
                {
                    "$GMSpriteFramesTrack": "",
                    "builtinName": 0,
                    "events": [],
                    "inheritsTrackColour": True,
                    "interpolation": 1,
                    "isCreationTrack": False,
                    "keyframes": {
                        "$KeyframeStore<SpriteFrameKeyframe>": "",
                        "Keyframes": keyframe_objs,
                        "resourceType": "KeyframeStore<SpriteFrameKeyframe>",
                        "resourceVersion": "2.0"
                    },
                    "modifiers": [],
                    "name": "frames",
                    "resourceType": "GMSpriteFramesTrack",
                    "resourceVersion": "2.0",
                    "spriteId": None,
                    "trackColour": 0,
                    "tracks": [],
                    "traits": 0
                }
            ],
            "visibleRange": None,
            "volume": 1.0,
            "xorigin": 0,
            "yorigin": 0
        },
        "swatchColours": None,
        "textureGroupId": {
            "name": "Default",
            "path": "texturegroups/Default"
        },
        "type": 0,
        "VTile": False,
        "width": w
    }
    return yy

def save_sprite_resource(spr_name, w, h, frame_images):
    spr_dir = os.path.join(SPRITES_DIR, spr_name)
    os.makedirs(spr_dir, exist_ok=True)
    
    layer_id = str(uuid.uuid4())
    frame_ids = [str(uuid.uuid4()) for _ in frame_images]
    
    # Save composite preview png
    frame_images[0].save(os.path.join(spr_dir, f"{spr_name}.png"))
    
    for f_idx, f_img in enumerate(frame_images):
        f_id = frame_ids[f_idx]
        frame_png_path = os.path.join(spr_dir, f"{f_id}.png")
        f_img.save(frame_png_path)
        
        layer_dir = os.path.join(spr_dir, "layers", f_id)
        os.makedirs(layer_dir, exist_ok=True)
        layer_png_path = os.path.join(layer_dir, f"{layer_id}.png")
        f_img.save(layer_png_path)
        
    yy_data = create_gmsprite_yy(spr_name, w, h, frame_ids, layer_id)
    with open(os.path.join(spr_dir, f"{spr_name}.yy"), "w") as f:
        json.dump(yy_data, f, indent=2)
        
    register_in_yyp(spr_name)
    print(f"✓ Saved {spr_name}: {len(frame_images)} frames ({w}x{h})")

# =============================================================================
# 1. COMMANDER MALE 12-FRAME ANIMATION (200x200)
# =============================================================================
def build_male_commander_frames():
    im = Image.open(MALE_SRC)
    # Crop inner portrait
    base = im.crop((80, 80, 944, 944)).resize((200, 200), Image.Resampling.LANCZOS).convert("RGBA")
    
    # Landmarks
    mx, my, mw = 100, 114, 26
    lex, ley = 80, 72
    rex, rey = 120, 72
    skin_tone = (239, 188, 149, 255)
    crease_tone = (180, 130, 100, 255)
    lash_color = (25, 20, 22, 255)
    cavity_color = (26, 12, 16, 255)
    teeth_color = (220, 215, 210, 255)
    tongue_color = (95, 42, 48, 255)
    
    p0 = base.copy()
    
    # Pose 1: Mouth slight open
    p1 = base.copy()
    d1 = ImageDraw.Draw(p1)
    d1.rectangle([mx - 7, my - 1, mx + 7, my + 1], fill=cavity_color)
    d1.line([mx - 5, my - 1, mx + 5, my - 1], fill=teeth_color, width=1)
    
    # Pose 2: Mouth open
    p2 = base.copy()
    d2 = ImageDraw.Draw(p2)
    d2.rectangle([mx - 9, my - 2, mx + 9, my + 3], fill=cavity_color)
    d2.ellipse([mx - 4, my + 1, mx + 4, my + 3], fill=tongue_color)
    d2.line([mx - 7, my - 2, mx + 7, my - 2], fill=teeth_color, width=1)
    
    # Pose 3: Half Blink
    p3 = base.copy()
    d3 = ImageDraw.Draw(p3)
    for (ex, ey) in [(lex, ley), (rex, rey)]:
        d3.rectangle([ex - 7, ey - 4, ex + 7, ey], fill=skin_tone)
        d3.line([ex - 7, ey - 4, ex + 7, ey - 4], fill=crease_tone, width=1)
        d3.line([ex - 7, ey, ex + 7, ey], fill=lash_color, width=1)
        
    # Pose 4: Full Blink
    p4 = base.copy()
    d4 = ImageDraw.Draw(p4)
    for (ex, ey) in [(lex, ley), (rex, rey)]:
        d4.rectangle([ex - 7, ey - 4, ex + 7, ey + 4], fill=skin_tone)
        d4.line([ex - 7, ey - 2, ex + 7, ey - 2], fill=crease_tone, width=1)
        d4.line([ex - 7, ey + 3, ex + 7, ey + 3], fill=lash_color, width=1)
        
    return [p0, p1, p2, p1, p0, p0, p3, p4, p3, p0, p0, p0]

# =============================================================================
# 2. COMMANDER FEMALE 12-FRAME ANIMATION (200x200)
# =============================================================================
def build_female_commander_frames():
    im = Image.open(FEMALE_SRC)
    base = im.crop((80, 80, 944, 944)).resize((200, 200), Image.Resampling.LANCZOS).convert("RGBA")
    
    mx, my, mw = 100, 98, 24
    lex, ley = 84, 74
    rex, rey = 116, 74
    skin_tone = (238, 189, 151, 255)
    crease_tone = (185, 135, 105, 255)
    lash_color = (28, 18, 22, 255)
    cavity_color = (28, 12, 16, 255)
    teeth_color = (225, 218, 212, 255)
    tongue_color = (98, 45, 52, 255)
    
    p0 = base.copy()
    
    p1 = base.copy()
    d1 = ImageDraw.Draw(p1)
    d1.rectangle([mx - 6, my - 1, mx + 6, my + 1], fill=cavity_color)
    d1.line([mx - 4, my - 1, mx + 4, my - 1], fill=teeth_color, width=1)
    
    p2 = base.copy()
    d2 = ImageDraw.Draw(p2)
    d2.rectangle([mx - 8, my - 2, mx + 8, my + 3], fill=cavity_color)
    d2.ellipse([mx - 3, my + 1, mx + 3, my + 3], fill=tongue_color)
    d2.line([mx - 6, my - 2, mx + 6, my - 2], fill=teeth_color, width=1)
    
    p3 = base.copy()
    d3 = ImageDraw.Draw(p3)
    for (ex, ey) in [(lex, ley), (rex, rey)]:
        d3.rectangle([ex - 7, ey - 4, ex + 7, ey], fill=skin_tone)
        d3.line([ex - 7, ey - 4, ex + 7, ey - 4], fill=crease_tone, width=1)
        d3.line([ex - 7, ey, ex + 7, ey], fill=lash_color, width=1)
        
    p4 = base.copy()
    d4 = ImageDraw.Draw(p4)
    for (ex, ey) in [(lex, ley), (rex, rey)]:
        d4.rectangle([ex - 7, ey - 4, ex + 7, ey + 4], fill=skin_tone)
        d4.line([ex - 7, ey - 2, ex + 7, ey - 2], fill=crease_tone, width=1)
        d4.line([ex - 7, ey + 3, ex + 7, ey + 3], fill=lash_color, width=1)
        
    return [p0, p1, p2, p1, p0, p0, p3, p4, p3, p0, p0, p0]

# =============================================================================
# 3. COMMANDER SILHOUETTE 4-FRAME ANIMATION (200x200)
# =============================================================================
def build_silhouette_frames():
    frames = []
    w, h = 200, 200
    
    for f_idx in range(4):
        img = Image.new("RGBA", (w, h), (12, 16, 22, 255))
        d = ImageDraw.Draw(img)
        
        # 1. Dark cyan recessed background scanlines
        for y in range(0, h, 4):
            scan_alpha = 18 + int(math.sin((y + f_idx * 4) * 0.15) * 8)
            d.line([(0, y), (w, y)], fill=(20, 35, 48, scan_alpha))
            
        # 2. Tactical Head & Broad Shoulder Silhouette Bust
        # Shoulder mantle
        d.polygon([(18, 198), (45, 142), (155, 142), (182, 198)], fill=(28, 36, 46, 255))
        # Torso collar
        d.polygon([(65, 142), (80, 115), (120, 115), (135, 142)], fill=(24, 30, 40, 255))
        # Neck
        d.rectangle([88, 92, 112, 118], fill=(22, 28, 38, 255))
        # Head / Helmet
        d.ellipse([70, 42, 130, 102], fill=(26, 34, 44, 255))
        # Tactical Comm Headset Antenna
        d.line([(68, 55), (62, 30)], fill=(60, 90, 115, 255), width=2)
        d.rectangle([60, 28, 64, 32], fill=(100, 220, 255, 255)) # Glowing cyan tip
        
        # Silhouette Rim Highlight (Cold Cyan Glow)
        d.arc([70, 42, 130, 102], start=160, end=270, fill=(70, 140, 185, 255), width=2)
        d.line([(45, 142), (18, 198)], fill=(60, 120, 160, 255), width=2)
        d.line([(155, 142), (182, 198)], fill=(40, 80, 110, 255), width=1)
        
        # 3. Telemetry Reticle Brackets
        bracket_col = (80, 180, 240, 255)
        # Top-left
        d.line([(8, 8), (28, 8)], fill=bracket_col, width=2)
        d.line([(8, 8), (8, 28)], fill=bracket_col, width=2)
        # Top-right
        d.line([(w - 28, 8), (w - 8, 8)], fill=bracket_col, width=2)
        d.line([(w - 8, 8), (w - 8, 28)], fill=bracket_col, width=2)
        # Bottom-left
        d.line([(8, h - 8), (28, h - 8)], fill=bracket_col, width=2)
        d.line([(8, h - 28), (8, h - 8)], fill=bracket_col, width=2)
        # Bottom-right
        d.line([(w - 28, h - 8), (w - 8, h - 8)], fill=bracket_col, width=2)
        d.line([(w - 8, h - 28), (w - 8, h - 8)], fill=bracket_col, width=2)
        
        # 4. Central Encrypted Badge / Crosshair
        cx, cy = w // 2, 72
        # Crosshair ticks
        d.line([(cx - 16, cy), (cx - 6, cy)], fill=bracket_col, width=1)
        d.line([(cx + 6, cy), (cx + 16, cy)], fill=bracket_col, width=1)
        d.line([(cx, cy - 16), (cx, cy - 6)], fill=bracket_col, width=1)
        d.line([(cx, cy + 6), (cx, cy + 16)], fill=bracket_col, width=1)
        
        # 5. Pulsating Classified Banner (Bottom Center)
        banner_pulse = 200 + int(math.sin(f_idx * 1.57) * 45)
        b_col = (255, 180, 40, banner_pulse) # Amber warning
        d.rectangle([32, 160, 168, 182], fill=(14, 18, 24, 220), outline=b_col)
        
        # Question mark glyph in center
        d.arc([cx - 5, cy - 8, cx + 5, cy - 2], start=180, end=360, fill=b_col, width=2)
        d.line([(cx + 5, cy - 5), (cx, cy)], fill=b_col, width=2)
        d.point([(cx, cy + 4)], fill=b_col)
        
        frames.append(img)
    return frames

# =============================================================================
# 4. LOCATION ENVIRONMENT BACKDROPS (1024x576)
# =============================================================================
def build_location_frames(src_path, w=1024, h=576):
    im = Image.open(src_path)
    res = im.resize((w, h), Image.Resampling.LANCZOS).convert("RGBA")
    
    # 2 Frames for subtle CRT / ambient flicker
    f0 = res.copy()
    f1 = res.copy()
    d1 = ImageDraw.Draw(f1)
    # Very subtle atmospheric lighting modulation
    for y in range(0, h, 6):
        d1.line([(0, y), (w, y)], fill=(0, 0, 0, 8))
    return [f0, f1]

# =============================================================================
# MASTER EXECUTION
# =============================================================================
def main():
    print("=====================================================================")
    print("=== GENERATING COMMANDER PORTRAITS & LOCATION ASSETS ===")
    print("=====================================================================")
    
    # 1. Male Commander Portrait
    m_frames = build_male_commander_frames()
    save_sprite_resource("spr_portrait_commander_male", 200, 200, m_frames)
    
    # 2. Female Commander Portrait
    f_frames = build_female_commander_frames()
    save_sprite_resource("spr_portrait_commander_female", 200, 200, f_frames)
    
    # 3. Classified Silhouette Portrait
    s_frames = build_silhouette_frames()
    save_sprite_resource("spr_portrait_commander_silhouette", 200, 200, s_frames)
    
    # 4. Location Hangar Bay Backdrop
    h_frames = build_location_frames(HANGAR_SRC)
    save_sprite_resource("spr_loc_hangar_bay", 1024, 576, h_frames)
    
    # 5. Location War Room Backdrop
    w_frames = build_location_frames(WAR_ROOM_SRC)
    save_sprite_resource("spr_loc_war_room", 1024, 576, w_frames)
    
    print("\n>>> All 5 Visual Assets Generated and Registered Successfully! <<<")

if __name__ == "__main__":
    main()
