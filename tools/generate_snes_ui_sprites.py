#!/usr/bin/env python3
"""
tools/generate_snes_ui_sprites.py
Generates engine-ready 16-bit Super Nintendo UI sprite resources:
- spr_snes_faction_crests (64x64, 4 frames: Terran, Colony, Syndicate, Zaibatsu)
- spr_snes_panel_corner (32x32, 4 frames: TL, TR, BL, BR)
- spr_snes_hazard_stripe (64x16, 2 frames: Yellow/Black, Orange/Black)
- spr_snes_led_indicators (16x16, 5 frames: Green, Amber, Red, Cyan, Offline)
- spr_snes_tactical_cursor (32x32, 4 frames: Animated crosshair brackets)
- spr_snes_crt_scanline (128x128, 1 frame: CRT scanline raster)

Strictly outputs GameMaker Studio 2 sprite resources ($GMSprite v2) and registers them in MechMakerConcept.yyp.
"""

import os, sys, json, uuid
from PIL import Image, ImageDraw

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITES_DIR = os.path.join(PROJECT_DIR, "sprites")
YYP_PATH = os.path.join(PROJECT_DIR, "MechMakerConcept.yyp")

def create_gm_sprite_resource(sprite_name, frames, speed=0.0, origin_mode=0, origin_x=0, origin_y=0):
    """
    Creates a full GameMaker Studio 2 sprite resource directory and .yy file.
    frames: list of PIL Images (must all be same size and RGBA)
    """
    w, h = frames[0].size
    sprite_dir = os.path.join(SPRITES_DIR, sprite_name)
    layers_dir = os.path.join(sprite_dir, "layers")
    os.makedirs(sprite_dir, exist_ok=True)
    os.makedirs(layers_dir, exist_ok=True)

    layer_uuid = str(uuid.uuid4())
    frame_uuids = [str(uuid.uuid4()) for _ in frames]

    # Save representative sprite png (frame 0)
    frames[0].save(os.path.join(sprite_dir, f"{sprite_name}.png"))

    frames_meta = []
    keyframes_meta = []

    for idx, (frame_im, f_uuid) in enumerate(zip(frames, frame_uuids)):
        frame_path = os.path.join(sprite_dir, f"{f_uuid}.png")
        frame_im.save(frame_path)

        f_layer_dir = os.path.join(layers_dir, f_uuid)
        os.makedirs(f_layer_dir, exist_ok=True)
        frame_im.save(os.path.join(f_layer_dir, f"{layer_uuid}.png"))

        frames_meta.append({
            "$GMSpriteFrame": "v1",
            "%Name": f_uuid,
            "name": f_uuid,
            "resourceType": "GMSpriteFrame",
            "resourceVersion": "2.0"
        })

        keyframes_meta.append({
            "$Keyframe<SpriteFrameKeyframe>": "",
            "Channels": {
                "0": {
                    "$SpriteFrameKeyframe": "",
                    "Id": {
                        "name": f_uuid,
                        "path": f"sprites/{sprite_name}/{sprite_name}.yy"
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

    yy_data = {
        "$GMSprite": "v2",
        "%Name": sprite_name,
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
        "frames": frames_meta,
        "gridX": 0,
        "gridY": 0,
        "height": h,
        "HTile": False,
        "layers": [
            {
                "$GMImageLayer": "",
                "%Name": layer_uuid,
                "blendMode": 0,
                "displayName": "default",
                "isLocked": False,
                "name": layer_uuid,
                "opacity": 100.0,
                "resourceType": "GMImageLayer",
                "resourceVersion": "2.0",
                "visible": True
            }
        ],
        "name": sprite_name,
        "nineSlice": None,
        "origin": origin_mode,
        "parent": {
            "name": "MechMakerConcept",
            "path": "MechMakerConcept.yyp"
        },
        "preMultiplyAlpha": False,
        "resourceType": "GMSprite",
        "resourceVersion": "2.0",
        "sequence": {
            "$GMSequence": "v1",
            "%Name": sprite_name,
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
            "name": sprite_name,
            "playback": 1,
            "playbackSpeed": speed,
            "playbackSpeedType": 0,
            "resourceType": "GMSequence",
            "resourceVersion": "2.0",
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
                        "Keyframes": keyframes_meta,
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
            "xorigin": origin_x,
            "yorigin": origin_y
        },
        "swatchColours": None,
        "swfPrecision": 2.525,
        "textureGroupId": {
            "name": "Default",
            "path": "texturegroups/Default"
        },
        "type": 0,
        "VTile": False,
        "width": w
    }

    yy_path = os.path.join(sprite_dir, f"{sprite_name}.yy")
    with open(yy_path, "w") as f:
        json.dump(yy_data, f, indent=2)

    # Register in YYP if needed
    register_in_yyp(sprite_name, f"sprites/{sprite_name}/{sprite_name}.yy")
    print(f"✓ Generated Sprite: {sprite_name} ({w}x{h}, {len(frames)} frames)")

def register_in_yyp(name, path):
    with open(YYP_PATH, "r") as f:
        content = f.read()

    target_entry = f'"path":"{path}"'
    if target_entry in content:
        return # Already registered

    # Find the end of resources: [] block
    # Insert right before the closing ],
    idx = content.find('"resources":[\n')
    if idx == -1:
        idx = content.find('"resources": [')
    
    # Find the closing bracket of the resources array
    bracket_idx = content.find('],', idx)
    if bracket_idx != -1:
        new_entry = f'    {{"id":{{"name":"{name}","path":"{path}",}},}},\n'
        content = content[:bracket_idx] + new_entry + content[bracket_idx:]
        with open(YYP_PATH, "w") as f:
            f.write(content)
        print(f"  -> Registered {name} in MechMakerConcept.yyp")

# =============================================================================
# SPRITE ART GENERATORS
# =============================================================================

def generate_faction_crests():
    """Generates 4 distinct 16-bit military crests (64x64, 4 frames)."""
    frames = []

    # -------------------------------------------------------------------------
    # Frame 0: Terran Hegemony (Imperial Eagle Shield)
    # -------------------------------------------------------------------------
    f0 = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d0 = ImageDraw.Draw(f0)
    # Beveled shield base
    shield_pts = [(32, 4), (56, 12), (56, 40), (32, 60), (8, 40), (8, 12)]
    d0.polygon(shield_pts, fill=(28, 38, 48, 255))
    # Bevel highlight & shadow
    d0.line([(32, 4), (8, 12), (8, 40), (32, 60)], fill=(120, 145, 170, 255), width=2)
    d0.line([(32, 4), (56, 12), (56, 40), (32, 60)], fill=(14, 20, 26, 255), width=2)
    # Inner shield rim
    inner_pts = [(32, 8), (52, 15), (52, 38), (32, 55), (12, 38), (12, 15)]
    d0.polygon(inner_pts, fill=(36, 48, 62, 255), outline=(50, 70, 95, 255))
    # Brass Imperial Eagle / Starburst Emblem
    gold_dark = (130, 95, 25, 255)
    gold_mid = (195, 150, 45, 255)
    gold_hi = (250, 220, 90, 255)
    gold_spec = (255, 245, 180, 255)
    # Wings
    for side in [-1, 1]:
        cx = 32
        d0.polygon([(cx, 28), (cx + side*18, 18), (cx + side*22, 26), (cx + side*14, 34), (cx, 32)], fill=gold_mid, outline=gold_dark)
        d0.line([(cx, 28), (cx + side*18, 18)], fill=gold_hi, width=1)
        d0.line([(cx + side*2, 24), (cx + side*16, 22)], fill=gold_spec, width=1)
        # Feathers
        d0.polygon([(cx + side*6, 32), (cx + side*20, 36), (cx + side*12, 42), (cx, 38)], fill=gold_mid, outline=gold_dark)
    # Center Eagle Head / Star
    d0.polygon([(32, 16), (36, 24), (32, 32), (28, 24)], fill=gold_hi, outline=gold_dark)
    d0.point([(32, 18), (32, 19), (31, 20)], fill=gold_spec)
    # Crimson Military Ribbon banner at base
    d0.polygon([(16, 44), (48, 44), (52, 50), (48, 56), (16, 56), (12, 50)], fill=(170, 35, 35, 255), outline=(90, 15, 15, 255))
    d0.line([(16, 44), (48, 44)], fill=(235, 75, 75, 255), width=1)
    # Banner text stipple: TH
    d0.point([(26, 48), (26, 49), (26, 50), (26, 51), (27, 48), (28, 48), (30, 48), (30, 49), (30, 50), (30, 51)], fill=(255, 240, 150, 255))
    d0.point([(34, 48), (34, 49), (34, 50), (34, 51), (37, 48), (37, 49), (37, 50), (37, 51), (35, 50), (36, 50)], fill=(255, 240, 150, 255))
    frames.append(f0)

    # -------------------------------------------------------------------------
    # Frame 1: Colony League / Aetherian Ascendancy (Orbital Solar Prism)
    # -------------------------------------------------------------------------
    f1 = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(f1)
    # Deep cobalt circular roundel
    d1.ellipse([6, 6, 58, 58], fill=(16, 26, 48, 255), outline=(10, 16, 30, 255))
    d1.arc([6, 6, 58, 58], start=135, end=315, fill=(90, 140, 210, 255), width=2)
    d1.arc([6, 6, 58, 58], start=315, end=495, fill=(8, 12, 22, 255), width=2)
    # Inner ring
    d1.ellipse([12, 12, 52, 52], fill=(22, 36, 64, 255), outline=(40, 70, 120, 255))
    # Orbital Cyan Ring angled
    d1.arc([10, 22, 54, 42], start=0, end=360, fill=(70, 210, 255, 255), width=2)
    # Ascendant Cyber Wings
    wing_col = (180, 215, 245, 255)
    wing_hi = (240, 250, 255, 255)
    wing_sh = (60, 90, 130, 255)
    for side in [-1, 1]:
        cx = 32
        d1.polygon([(cx, 44), (cx + side*16, 18), (cx + side*20, 22), (cx + side*8, 40), (cx, 46)], fill=wing_col, outline=wing_sh)
        d1.line([(cx, 44), (cx + side*16, 18)], fill=wing_hi, width=1)
        d1.polygon([(cx + side*4, 38), (cx + side*22, 28), (cx + side*12, 46)], fill=wing_col, outline=wing_sh)
    # Core Radiant Prism
    d1.polygon([(32, 14), (40, 28), (32, 42), (24, 28)], fill=(220, 245, 255, 255), outline=(50, 180, 240, 255))
    d1.polygon([(32, 18), (37, 28), (32, 38), (27, 28)], fill=(255, 255, 255, 255))
    # Ambient lens flare pips
    d1.point([(32, 10), (32, 12), (32, 44), (32, 46), (18, 28), (46, 28)], fill=(120, 230, 255, 255))
    frames.append(f1)

    # -------------------------------------------------------------------------
    # Frame 2: Hyena Syndicate (Scorched Iron Wolf Skull)
    # -------------------------------------------------------------------------
    f2 = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(f2)
    # Heavy industrial diamond plate
    diamond_pts = [(32, 4), (58, 32), (32, 60), (6, 32)]
    d2.polygon(diamond_pts, fill=(36, 24, 18, 255), outline=(14, 10, 8, 255))
    d2.line([(32, 4), (6, 32), (32, 60)], fill=(150, 75, 40, 255), width=2)
    d2.line([(32, 4), (58, 32), (32, 60)], fill=(18, 12, 10, 255), width=2)
    # Hazard notched inner diamond
    d2.polygon([(32, 10), (52, 32), (32, 54), (12, 32)], fill=(50, 32, 24, 255), outline=(210, 130, 40, 255))
    # Wolf Skull / Lupine Jaws
    bone_hi = (210, 195, 175, 255)
    bone_sh = (85, 70, 60, 255)
    # Cranium
    d2.polygon([(32, 16), (44, 24), (40, 36), (32, 34), (24, 36), (20, 24)], fill=bone_hi, outline=bone_sh)
    # Snout
    d2.polygon([(26, 34), (38, 34), (36, 44), (32, 46), (28, 44)], fill=bone_hi, outline=bone_sh)
    # Fangs / Teeth
    d2.polygon([(28, 44), (30, 48), (32, 45), (34, 48), (36, 44)], fill=(245, 240, 230, 255), outline=bone_sh)
    # Glowing Cybernetic Red Eye Sockets
    d2.rectangle([25, 26, 28, 29], fill=(255, 30, 30, 255))
    d2.rectangle([36, 26, 39, 29], fill=(255, 30, 30, 255))
    d2.point([(26, 27), (37, 27)], fill=(255, 200, 200, 255))
    # Crossed industrial cleavers behind skull
    cleaver_col = (110, 115, 125, 255)
    d2.line([(14, 16), (50, 52)], fill=cleaver_col, width=3)
    d2.line([(50, 16), (14, 52)], fill=cleaver_col, width=3)
    d2.line([(13, 15), (22, 24)], fill=(220, 110, 30, 255), width=2) # Rust serration
    frames.append(f2)

    # -------------------------------------------------------------------------
    # Frame 3: Muramasa Zaibatsu (Hexagonal Cyber-Mon & Crossed Katanas)
    # -------------------------------------------------------------------------
    f3 = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d3 = ImageDraw.Draw(f3)
    # Hexagonal lacquer black backing
    hex_pts = [(32, 4), (56, 18), (56, 46), (32, 60), (8, 46), (8, 18)]
    d3.polygon(hex_pts, fill=(12, 16, 24, 255), outline=(6, 8, 14, 255))
    d3.line([(32, 4), (8, 18), (8, 46), (32, 60)], fill=(0, 210, 190, 255), width=2)
    d3.line([(32, 4), (56, 18), (56, 46), (32, 60)], fill=(0, 70, 70, 255), width=2)
    # Circuit traces inside
    d3.line([(16, 24), (24, 24), (28, 28)], fill=(0, 160, 150, 255), width=1)
    d3.line([(48, 24), (40, 24), (36, 28)], fill=(0, 160, 150, 255), width=1)
    # Crossed High-Frequency Katanas
    blade_core = (0, 240, 220, 255)
    blade_hi = (255, 255, 255, 255)
    blade_dark = (0, 100, 110, 255)
    # Blade 1: Top-Left to Bottom-Right
    d3.line([(14, 14), (50, 50)], fill=blade_core, width=2)
    d3.line([(15, 13), (49, 47)], fill=blade_hi, width=1)
    # Blade 2: Top-Right to Bottom-Left
    d3.line([(50, 14), (14, 50)], fill=blade_core, width=2)
    d3.line([(49, 13), (15, 47)], fill=blade_hi, width=1)
    # Hilt handles (Tsuka)
    d3.line([(12, 12), (18, 18)], fill=(180, 20, 40, 255), width=3)
    d3.line([(52, 12), (46, 18)], fill=(180, 20, 40, 255), width=3)
    # Center Corporate Mon Seal (Three Petals / Tri-force crest)
    mon_pts1 = [(32, 22), (37, 30), (27, 30)]
    mon_pts2 = [(27, 32), (32, 40), (22, 40)]
    mon_pts3 = [(37, 32), (42, 40), (32, 40)]
    d3.polygon(mon_pts1, fill=(240, 250, 255, 255), outline=(0, 180, 180, 255))
    d3.polygon(mon_pts2, fill=(240, 250, 255, 255), outline=(0, 180, 180, 255))
    d3.polygon(mon_pts3, fill=(240, 250, 255, 255), outline=(0, 180, 180, 255))
    # Vermilion corporate seal stamp in corner
    d3.rectangle([42, 42, 50, 50], fill=(220, 30, 50, 255), outline=(140, 15, 25, 255))
    d3.point([(45, 44), (46, 44), (47, 44), (46, 45), (46, 46), (46, 47), (44, 48), (48, 48)], fill=(255, 255, 255, 255))
    frames.append(f3)

    return frames

def generate_panel_corners():
    """Generates 4 frames of 32x32 metallic beveled corner brackets with hex rivets."""
    # Frame 0: Top-Left Corner Bracket
    f0 = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d0 = ImageDraw.Draw(f0)
    # Outer dark edge
    d0.line([(0, 0), (31, 0)], fill=(10, 14, 20, 255), width=1)
    d0.line([(0, 0), (0, 31)], fill=(10, 14, 20, 255), width=1)
    # Bright specular highlight ridge
    d0.line([(1, 1), (31, 1)], fill=(140, 165, 190, 255), width=2)
    d0.line([(1, 1), (1, 31)], fill=(140, 165, 190, 255), width=2)
    d0.point([(2, 2)], fill=(240, 250, 255, 255)) # Specular corner glint
    # Bracket plate fill
    d0.polygon([(2, 2), (18, 2), (18, 8), (8, 8), (8, 18), (2, 18)], fill=(40, 52, 68, 255))
    # Inner chamfer bevel
    d0.line([(18, 8), (8, 18)], fill=(75, 95, 120, 255), width=2)
    d0.line([(18, 2), (18, 8)], fill=(18, 24, 32, 255), width=1)
    d0.line([(2, 18), (8, 18)], fill=(18, 24, 32, 255), width=1)
    # Hex Rivet Bolt at (6, 6)
    d0.polygon([(5, 4), (7, 4), (8, 5), (8, 7), (7, 8), (5, 8), (4, 7), (4, 5)], fill=(110, 130, 155, 255), outline=(15, 20, 28, 255))
    d0.point([(5, 5), (6, 5)], fill=(225, 240, 255, 255)) # Bolt specular
    d0.point([(6, 7), (7, 7)], fill=(20, 26, 36, 255)) # Bolt shadow

    # Frames 1, 2, 3 are transformations of Frame 0
    f1 = f0.transpose(Image.FLIP_LEFT_RIGHT)
    f2 = f0.transpose(Image.FLIP_TOP_BOTTOM)
    f3 = f0.transpose(Image.ROTATE_180)

    return [f0, f1, f2, f3]

def generate_hazard_stripes():
    """Generates 64x16 diagonal hazard warning tape strips."""
    frames = []

    # Frame 0: Tactical Yellow / Black (Caution)
    f0 = Image.new("RGBA", (64, 16), (0, 0, 0, 0))
    d0 = ImageDraw.Draw(f0)
    for x in range(-16, 80, 8):
        pts = [(x, 0), (x+5, 0), (x-3, 16), (x-8, 16)]
        d0.polygon(pts, fill=(240, 185, 30, 255))
        # Top specular highlight
        d0.line([(max(0, x), 0), (min(63, x+5), 0)], fill=(255, 235, 120, 255), width=1)
        # Black stripes
        b_pts = [(x+5, 0), (x+8, 0), (x, 16), (x-3, 16)]
        d0.polygon(b_pts, fill=(20, 24, 30, 255))
    # Border rims
    d0.line([(0, 0), (63, 0)], fill=(90, 70, 15, 255), width=1)
    d0.line([(0, 15), (63, 15)], fill=(10, 14, 18, 255), width=1)
    frames.append(f0)

    # Frame 1: Emergency Orange / Black (Warning)
    f1 = Image.new("RGBA", (64, 16), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(f1)
    for x in range(-16, 80, 8):
        pts = [(x, 0), (x+5, 0), (x-3, 16), (x-8, 16)]
        d1.polygon(pts, fill=(230, 80, 25, 255))
        d1.line([(max(0, x), 0), (min(63, x+5), 0)], fill=(255, 160, 90, 255), width=1)
        b_pts = [(x+5, 0), (x+8, 0), (x, 16), (x-3, 16)]
        d1.polygon(b_pts, fill=(24, 18, 18, 255))
    d1.line([(0, 0), (63, 0)], fill=(120, 35, 10, 255), width=1)
    d1.line([(0, 15), (63, 15)], fill=(12, 10, 10, 255), width=1)
    frames.append(f1)

    return frames

def generate_led_indicators():
    """Generates 16x16 status indicator LED pips (Green, Amber, Red, Cyan, Offline)."""
    frames = []
    schemes = [
        # (core, mid, bloom, spec)
        ((80, 255, 120), (35, 180, 65), (10, 60, 25), (220, 255, 230)), # 0: Green
        ((255, 195, 50), (210, 130, 20), (70, 40, 8), (255, 245, 180)), # 1: Amber
        ((255, 60, 60), (195, 25, 25), (65, 10, 10), (255, 190, 190)),  # 2: Red
        ((80, 220, 255), (25, 140, 210), (8, 45, 70), (220, 250, 255)), # 3: Cyan
        ((65, 75, 90), (38, 45, 55), (14, 18, 24), (110, 125, 145))    # 4: Offline
    ]

    for (core, mid, bloom, spec) in schemes:
        f = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        d = ImageDraw.Draw(f)
        # Outer dark metal housing
        d.ellipse([1, 1, 14, 14], fill=(12, 16, 22, 255), outline=(6, 8, 12, 255))
        d.arc([1, 1, 14, 14], start=135, end=315, fill=(75, 95, 115, 255), width=1)
        # Outer bloom ring
        d.ellipse([3, 3, 12, 12], fill=(*bloom, 255))
        # Illuminated LED core
        d.ellipse([4, 4, 11, 11], fill=(*mid, 255))
        d.ellipse([5, 5, 10, 10], fill=(*core, 255))
        # Specular glint
        d.point([(6, 6), (7, 6)], fill=(*spec, 255))
        frames.append(f)

    return frames

def generate_tactical_cursor():
    """Generates 32x32 Front Mission style bracket crosshairs (4 frames)."""
    frames = []
    for step in range(4):
        f = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        d = ImageDraw.Draw(f)
        # Distance from center pulses 12 -> 11 -> 10 -> 11
        radii = [12, 11, 10, 11]
        r = radii[step]
        cx, cy = 16, 16
        col = (60, 230, 255, 255) if step != 2 else (255, 210, 60, 255) # Locks gold on frame 2
        col_hi = (220, 255, 255, 255) if step != 2 else (255, 250, 200, 255)
        # 4 Corner brackets
        # Top-Left
        d.line([(cx - r, cy - r), (cx - r + 4, cy - r)], fill=col, width=2)
        d.line([(cx - r, cy - r), (cx - r, cy - r + 4)], fill=col, width=2)
        d.point([(cx - r, cy - r)], fill=col_hi)
        # Top-Right
        d.line([(cx + r, cy - r), (cx + r - 4, cy - r)], fill=col, width=2)
        d.line([(cx + r, cy - r), (cx + r, cy - r + 4)], fill=col, width=2)
        d.point([(cx + r, cy - r)], fill=col_hi)
        # Bottom-Left
        d.line([(cx - r, cy + r), (cx - r + 4, cy + r)], fill=col, width=2)
        d.line([(cx - r, cy + r), (cx - r, cy + r - 4)], fill=col, width=2)
        d.point([(cx - r, cy + r)], fill=col_hi)
        # Bottom-Right
        d.line([(cx + r, cy + r), (cx + r - 4, cy + r)], fill=col, width=2)
        d.line([(cx + r, cy + r), (cx + r, cy + r - 4)], fill=col, width=2)
        d.point([(cx + r, cy + r)], fill=col_hi)
        # Center pip
        d.point([(cx, cy)], fill=col_hi)
        if step == 2: # Reticle tick marks
            d.line([(cx - 2, cy), (cx + 2, cy)], fill=col, width=1)
            d.line([(cx, cy - 2), (cx, cy + 2)], fill=col, width=1)
        frames.append(f)
    return frames

def generate_crt_scanlines():
    """Generates 128x128 repeating scanline raster tile."""
    f = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(f)
    for y in range(0, 128, 2):
        # Semi-transparent dark phosphor raster line
        d.line([(0, y), (127, y)], fill=(0, 0, 0, 48), width=1)
    return [f]

def main():
    print("=== EXPORTING 16-BIT SNES UI SPRITE ASSETS ===")
    
    # 1. Faction Crests
    crests = generate_faction_crests()
    create_gm_sprite_resource("spr_snes_faction_crests", crests, speed=0.0, origin_mode=0)

    # 2. Panel Corners
    corners = generate_panel_corners()
    create_gm_sprite_resource("spr_snes_panel_corner", corners, speed=0.0, origin_mode=0)

    # 3. Hazard Stripes
    hazards = generate_hazard_stripes()
    create_gm_sprite_resource("spr_snes_hazard_stripe", hazards, speed=0.0, origin_mode=0)

    # 4. LED Status Indicators
    leds = generate_led_indicators()
    create_gm_sprite_resource("spr_snes_led_indicators", leds, speed=0.0, origin_mode=0)

    # 5. Tactical Crosshair Cursor
    cursor = generate_tactical_cursor()
    create_gm_sprite_resource("spr_snes_tactical_cursor", cursor, speed=6.0, origin_mode=4, origin_x=16, origin_y=16)

    # 6. CRT Scanline Raster Tile
    scanlines = generate_crt_scanlines()
    create_gm_sprite_resource("spr_snes_crt_scanline", scanlines, speed=0.0, origin_mode=0)

    print("\n✓ ALL 16-BIT SNES UI SPRITES CREATED & REGISTERED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
