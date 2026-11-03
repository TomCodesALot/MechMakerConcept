import os
import shutil
import json
import uuid
import math
from PIL import Image, ImageDraw

SPRITES_DIR = "sprites"
YYP_PATH = "MechMakerConcept.yyp"

def create_suit_sprite(sprite_name, draw_func, is_back=False, num_frames=4):
    spr_path = os.path.join(SPRITES_DIR, sprite_name)
    layers_path = os.path.join(spr_path, "layers")
    os.makedirs(spr_path, exist_ok=True)
    os.makedirs(layers_path, exist_ok=True)

    layer_id = str(uuid.uuid4())
    frame_uuids = [str(uuid.uuid4()) for _ in range(num_frames)]
    frames = []

    for i, f_uuid in enumerate(frame_uuids):
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw_func(draw, i, is_back)
        
        main_png = os.path.join(spr_path, f"{f_uuid}.png")
        im.save(main_png, "PNG")
        
        layer_dir = os.path.join(layers_path, f_uuid)
        os.makedirs(layer_dir, exist_ok=True)
        layer_png = os.path.join(layer_dir, f"{layer_id}.png")
        im.save(layer_png, "PNG")
        frames.append(im)

    frames[0].save(os.path.join(spr_path, f"{sprite_name}.png"), "PNG")

    strip_im = Image.new("RGBA", (160 * num_frames, 160), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        strip_im.paste(fr, (i * 160, 0))
    strip_im.save(os.path.join(spr_path, f"{sprite_name}_strip{num_frames}.png"), "PNG")

    yy_data = {
        "$GMSprite": "v2",
        "%Name": sprite_name,
        "bboxMode": 0,
        "bbox_bottom": 141,
        "bbox_left": 15,
        "bbox_right": 145,
        "bbox_top": 12,
        "collisionKind": 1,
        "collisionTolerance": 0,
        "DynamicTexturePage": False,
        "edgeFiltering": False,
        "For3D": False,
        "frames": [
            {
                "$GMSpriteFrame": "v1",
                "%Name": f_uuid,
                "name": f_uuid,
                "resourceType": "GMSpriteFrame",
                "resourceVersion": "2.0"
            } for f_uuid in frame_uuids
        ],
        "gridX": 0,
        "gridY": 0,
        "height": 160,
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
        "name": sprite_name,
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
            "length": float(num_frames),
            "lockOrigin": False,
            "moments": {
                "$KeyframeStore<MomentsEventKeyframe>": "",
                "Keyframes": [],
                "resourceType": "KeyframeStore<MomentsEventKeyframe>",
                "resourceVersion": "2.0"
            },
            "name": sprite_name,
            "playback": 1,
            "playbackSpeed": 6.0,
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
                        "Keyframes": [
                            {
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
                                "Key": float(i),
                                "Length": 1.0,
                                "resourceType": "Keyframe<SpriteFrameKeyframe>",
                                "resourceVersion": "2.0",
                                "Stretch": False
                            } for i, f_uuid in enumerate(frame_uuids)
                        ],
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
            "xorigin": 80,
            "yorigin": 145
        },
        "swatchColours": None,
        "swfPrecision": 2.525,
        "textureGroupId": {
            "name": "Default",
            "path": "texturegroups/Default"
        },
        "type": 0,
        "VTile": False,
        "width": 160
    }

    with open(os.path.join(spr_path, f"{sprite_name}.yy"), "w") as f:
        json.dump(yy_data, f, indent=2)

# ==============================================================================
# SUIT 1: CASSIAN CUSTOM (Colony Gen 2 Ace Interceptor)
# ==============================================================================
def draw_cassian_custom(draw, frame_idx, is_back):
    bob = int(math.sin(frame_idx * math.pi / 2.0) * 1.5)
    cy = 82 + bob
    cx = 80

    # Colors
    c_white = (225, 235, 245, 255)
    c_navy = (22, 38, 65, 255)
    c_azure = (42, 110, 185, 255)
    c_cyan_glow = (0, 240, 255, 255)
    c_gold = (235, 185, 50, 255)
    c_dark = (15, 20, 30, 255)

    # 1. Back Thruster / Aero Wings
    wing_spread = 38
    # Left Wing
    draw.polygon([(cx - 15, cy - 10), (cx - wing_spread - 8, cy - 35), (cx - wing_spread + 2, cy - 5), (cx - 18, cy + 8)], fill=c_navy, outline=c_azure)
    draw.line([(cx - wing_spread - 4, cy - 30), (cx - 20, cy - 2)], fill=c_cyan_glow, width=2)
    # Right Wing
    draw.polygon([(cx + 15, cy - 10), (cx + wing_spread + 8, cy - 35), (cx + wing_spread - 2, cy - 5), (cx + 18, cy + 8)], fill=c_navy, outline=c_azure)
    draw.line([(cx + wing_spread + 4, cy - 30), (cx + 20, cy - 2)], fill=c_cyan_glow, width=2)

    # 2. Legs & Feet
    # Left Leg
    draw.polygon([(cx - 16, cy + 20), (cx - 24, cy + 42), (cx - 18, cy + 56), (cx - 10, cy + 20)], fill=c_navy, outline=c_azure)
    draw.polygon([(cx - 28, cy + 54), (cx - 14, cy + 54), (cx - 12, cy + 59), (cx - 30, cy + 59)], fill=c_azure, outline=c_white)
    # Right Leg (Forward)
    draw.polygon([(cx + 8, cy + 20), (cx + 18, cy + 40), (cx + 14, cy + 56), (cx + 2, cy + 20)], fill=c_navy, outline=c_azure)
    draw.polygon([(cx + 6, cy + 54), (cx + 22, cy + 54), (cx + 26, cy + 59), (cx + 8, cy + 59)], fill=c_white, outline=c_azure)
    # Knee Armor
    draw.polygon([(cx - 24, cy + 34), (cx - 16, cy + 32), (cx - 18, cy + 40)], fill=c_gold)
    draw.polygon([(cx + 14, cy + 32), (cx + 22, cy + 34), (cx + 18, cy + 40)], fill=c_gold)

    # 3. Torso / Pelvis
    draw.polygon([(cx - 14, cy + 12), (cx + 14, cy + 12), (cx + 10, cy + 22), (cx - 10, cy + 22)], fill=c_navy, outline=c_azure)
    draw.polygon([(cx - 16, cy - 12), (cx + 16, cy - 12), (cx + 12, cy + 14), (cx - 12, cy + 14)], fill=c_white, outline=c_azure)
    if not is_back:
        # Chest Cockpit / Sensor
        draw.polygon([(cx - 6, cy - 6), (cx + 6, cy - 6), (cx + 4, cy + 6), (cx - 4, cy + 6)], fill=c_azure, outline=c_gold)
        draw.rectangle([(cx - 2, cy - 2), (cx + 2, cy + 2)], fill=c_cyan_glow)
    else:
        # Backpack Vernier Twin Bells
        draw.rectangle([(cx - 8, cy - 8), (cx + 8, cy + 6)], fill=c_dark, outline=c_azure)
        draw.ellipse([(cx - 6, cy + 6), (cx - 2, cy + 14)], fill=c_azure, outline=c_cyan_glow)
        draw.ellipse([(cx + 2, cy + 6), (cx + 6, cy + 14)], fill=c_azure, outline=c_cyan_glow)

    # 4. Shoulders & Arms
    # Left Arm (Holding Beam Lance / Carbine)
    draw.polygon([(cx - 26, cy - 10), (cx - 16, cy - 14), (cx - 14, cy - 2), (cx - 24, cy + 2)], fill=c_white, outline=c_gold)
    draw.line([(cx - 20, cy), (cx - 28, cy + 18)], fill=c_navy, width=4)
    # Right Arm (Forward holding high-precision beam spray)
    draw.polygon([(cx + 16, cy - 14), (cx + 28, cy - 10), (cx + 26, cy + 2), (cx + 14, cy - 2)], fill=c_white, outline=c_gold)
    draw.line([(cx + 20, cy), (cx + 32, cy + 16)], fill=c_navy, width=4)
    # Beam Carbine Weapon in hand
    if not is_back:
        draw.rectangle([(cx + 30, cy + 8), (cx + 56, cy + 14)], fill=c_dark, outline=c_azure)
        draw.line([(cx + 56, cy + 11), (cx + 64, cy + 11)], fill=c_cyan_glow, width=2)
        draw.rectangle([(cx + 34, cy + 14), (cx + 40, cy + 20)], fill=c_azure)

    # 5. Head & Ace Commander Fin
    draw.ellipse([(cx - 7, cy - 22), (cx + 7, cy - 10)], fill=c_white, outline=c_azure)
    if not is_back:
        draw.line([(cx - 5, cy - 15), (cx + 5, cy - 15)], fill=c_cyan_glow, width=2) # Visor
        # V-Fin Crest
        draw.polygon([(cx - 1, cy - 20), (cx - 14, cy - 34), (cx - 2, cy - 23)], fill=c_gold)
        draw.polygon([(cx + 1, cy - 20), (cx + 14, cy - 34), (cx + 2, cy - 23)], fill=c_gold)
    else:
        draw.rectangle([(cx - 3, cy - 18), (cx + 3, cy - 12)], fill=c_azure)

# ==============================================================================
# SUIT 2: CHRONOS (Colony Gen 4 Sovereign Flagship)
# ==============================================================================
def draw_chronos(draw, frame_idx, is_back):
    bob = int(math.sin(frame_idx * math.pi / 2.0) * 1.0)
    cy = 80 + bob
    cx = 80

    c_white = (240, 245, 255, 255)
    c_cobalt = (25, 40, 80, 255)
    c_violet = (138, 79, 255, 255)
    c_cyan = (56, 232, 255, 255)
    c_gold = (245, 210, 80, 255)
    c_metal = (40, 50, 70, 255)

    # 1. Sovereign Tachyon Halo Ring (Floating behind torso)
    halo_r = 34
    draw.arc([cx - halo_r, cy - halo_r - 10, cx + halo_r, cy + halo_r - 10], 0, 360, fill=c_cyan, width=2)
    # Radiating emitter crystals
    for angle in [45, 90, 135, 225, 270, 315]:
        rad = math.radians(angle)
        px = cx + int(math.cos(rad) * halo_r)
        py = cy - 10 + int(math.sin(rad) * halo_r)
        draw.rectangle([px - 2, py - 2, px + 2, py + 2], fill=c_violet)

    # 2. Imposing Legs
    draw.polygon([(cx - 18, cy + 18), (cx - 28, cy + 44), (cx - 20, cy + 58), (cx - 12, cy + 18)], fill=c_white, outline=c_cobalt)
    draw.polygon([(cx - 32, cy + 54), (cx - 16, cy + 54), (cx - 14, cy + 59), (cx - 34, cy + 59)], fill=c_cobalt, outline=c_gold)
    draw.polygon([(cx + 12, cy + 18), (cx + 24, cy + 42), (cx + 18, cy + 58), (cx + 4, cy + 18)], fill=c_white, outline=c_cobalt)
    draw.polygon([(cx + 12, cy + 54), (cx + 28, cy + 54), (cx + 32, cy + 59), (cx + 14, cy + 59)], fill=c_cobalt, outline=c_gold)
    # Tachyon knee conductors
    draw.rectangle([(cx - 26, cy + 34), (cx - 20, cy + 38)], fill=c_cyan)
    draw.rectangle([(cx + 18, cy + 32), (cx + 24, cy + 36)], fill=c_cyan)

    # 3. Torso
    draw.polygon([(cx - 18, cy - 14), (cx + 18, cy - 14), (cx + 14, cy + 16), (cx - 14, cy + 16)], fill=c_white, outline=c_cobalt)
    draw.polygon([(cx - 8, cy - 8), (cx + 8, cy - 8), (cx + 5, cy + 10), (cx - 5, cy + 10)], fill=c_cobalt, outline=c_gold)
    draw.rectangle([(cx - 2, cy - 2), (cx + 2, cy + 4)], fill=c_violet) # Core

    # 4. Shoulder Radiators & Sovereign Wings
    draw.polygon([(cx - 34, cy - 16), (cx - 18, cy - 18), (cx - 16, cy + 2), (cx - 30, cy + 6)], fill=c_cobalt, outline=c_white)
    draw.polygon([(cx + 18, cy - 18), (cx + 34, cy - 16), (cx + 30, cy + 6), (cx + 16, cy + 2)], fill=c_cobalt, outline=c_white)
    # Crystal emitters on shoulders
    draw.line([(cx - 32, cy - 12), (cx - 22, cy - 12)], fill=c_cyan, width=2)
    draw.line([(cx + 22, cy - 12), (cx + 32, cy - 12)], fill=c_cyan, width=2)

    # 5. Massive Heavy Tachyon Cannon (Right Arm)
    draw.line([(cx + 24, cy), (cx + 32, cy + 18)], fill=c_metal, width=5)
    draw.rectangle([(cx + 28, cy + 6), (cx + 62, cy + 18)], fill=c_metal, outline=c_cobalt)
    draw.polygon([(cx + 62, cy + 8), (cx + 70, cy + 12), (cx + 62, cy + 16)], fill=c_cyan)
    # Left Arm (Tower Shield)
    draw.polygon([(cx - 34, cy - 4), (cx - 24, cy - 8), (cx - 26, cy + 28), (cx - 38, cy + 22)], fill=c_white, outline=c_gold)
    draw.line([(cx - 34, cy + 4), (cx - 28, cy + 18)], fill=c_violet, width=2)

    # 6. Crown Head
    draw.ellipse([(cx - 8, cy - 24), (cx + 8, cy - 12)], fill=c_white, outline=c_cobalt)
    draw.line([(cx - 5, cy - 17), (cx + 5, cy - 17)], fill=c_cyan, width=2)
    # Radiating triple-spike crown
    draw.polygon([(cx - 10, cy - 24), (cx - 14, cy - 36), (cx - 6, cy - 25)], fill=c_gold)
    draw.polygon([(cx - 2, cy - 24), (cx, cy - 38), (cx + 2, cy - 24)], fill=c_cyan)
    draw.polygon([(cx + 6, cy - 25), (cx + 14, cy - 36), (cx + 10, cy - 24)], fill=c_gold)

# ==============================================================================
# SUIT 3: MARAUDER (Syndicate Gen 2 Scrap Brawler)
# ==============================================================================
def draw_marauder(draw, frame_idx, is_back):
    bob = int(math.sin(frame_idx * math.pi / 2.0) * 1.5)
    cy = 82 + bob
    cx = 80

    c_rust = (185, 85, 30, 255)
    c_iron = (55, 60, 68, 255)
    c_hazard_y = (220, 175, 20, 255)
    c_hazard_b = (25, 25, 28, 255)
    c_red_optic = (255, 45, 45, 255)
    c_dark = (30, 32, 36, 255)
    c_steel = (130, 140, 150, 255)

    # 1. Heavy Spiked Legs
    draw.polygon([(cx - 20, cy + 20), (cx - 30, cy + 42), (cx - 22, cy + 58), (cx - 12, cy + 20)], fill=c_iron, outline=c_rust)
    draw.polygon([(cx - 34, cy + 52), (cx - 16, cy + 52), (cx - 14, cy + 59), (cx - 36, cy + 59)], fill=c_rust, outline=c_iron)
    draw.polygon([(cx + 10, cy + 20), (cx + 22, cy + 40), (cx + 18, cy + 58), (cx + 2, cy + 20)], fill=c_iron, outline=c_rust)
    draw.polygon([(cx + 8, cy + 52), (cx + 26, cy + 52), (cx + 28, cy + 59), (cx + 10, cy + 59)], fill=c_rust, outline=c_iron)
    # Leg spikes
    draw.polygon([(cx - 30, cy + 40), (cx - 36, cy + 38), (cx - 28, cy + 46)], fill=c_steel)
    draw.polygon([(cx + 22, cy + 38), (cx + 28, cy + 36), (cx + 20, cy + 44)], fill=c_steel)

    # 2. Asymmetric Scrap Torso & Roll Cage
    draw.polygon([(cx - 20, cy - 14), (cx + 18, cy - 12), (cx + 14, cy + 18), (cx - 16, cy + 18)], fill=c_rust, outline=c_iron)
    # Welded armor plates with rivets
    draw.polygon([(cx - 14, cy - 8), (cx + 4, cy - 8), (cx + 2, cy + 8), (cx - 12, cy + 8)], fill=c_iron, outline=c_steel)
    draw.point([(cx - 10, cy - 5), (cx + 1, cy - 5), (cx - 10, cy + 5), (cx + 1, cy + 5)], fill=c_hazard_y)
    # Slag burner furnace vent
    draw.rectangle([(cx + 6, cy - 4), (cx + 14, cy + 6)], fill=c_dark, outline=c_rust)
    draw.line([(cx + 8, cy + 1), (cx + 12, cy + 1)], fill=(255, 120, 20, 255), width=2)

    # 3. Shoulder Mounts
    # Left Shoulder: Massive Scrap Pauldron with hazard stripes
    draw.polygon([(cx - 36, cy - 18), (cx - 18, cy - 20), (cx - 16, cy), (cx - 32, cy + 6)], fill=c_hazard_y, outline=c_iron)
    draw.line([(cx - 32, cy - 14), (cx - 22, cy - 4)], fill=c_hazard_b, width=3)
    # Right Shoulder: Slag Mortar Tube
    draw.polygon([(cx + 16, cy - 18), (cx + 32, cy - 14), (cx + 28, cy + 2), (cx + 14, cy)], fill=c_iron, outline=c_rust)
    draw.rectangle([(cx + 22, cy - 26), (cx + 28, cy - 14)], fill=c_steel, outline=c_dark) # Mortar barrel

    # 4. Arms
    # Left Arm: Giant Hydraulic Demolition Claw
    draw.line([(cx - 26, cy), (cx - 36, cy + 18)], fill=c_iron, width=6)
    # Twin claw pincers
    draw.polygon([(cx - 44, cy + 14), (cx - 36, cy + 18), (cx - 46, cy + 28)], fill=c_steel, outline=c_dark)
    draw.polygon([(cx - 38, cy + 24), (cx - 32, cy + 20), (cx - 40, cy + 34)], fill=c_steel, outline=c_dark)
    # Right Arm: Flak gun / Scrap Ripper
    draw.line([(cx + 22, cy), (cx + 32, cy + 16)], fill=c_iron, width=5)
    draw.rectangle([(cx + 30, cy + 10), (cx + 54, cy + 20)], fill=c_rust, outline=c_iron)
    draw.rectangle([(cx + 54, cy + 13), (cx + 62, cy + 17)], fill=c_dark)

    # 5. Asymmetric Head / Slit Sensor
    draw.rectangle([(cx - 9, cy - 22), (cx + 7, cy - 12)], fill=c_iron, outline=c_rust)
    draw.line([(cx - 6, cy - 17), (cx + 4, cy - 17)], fill=c_red_optic, width=2)
    # Welded antenna
    draw.line([(cx + 5, cy - 22), (cx + 10, cy - 32)], fill=c_steel, width=2)

# ==============================================================================
# SUIT 4: IRON REAVER (Syndicate Gen 4 Dreadnought Rig)
# ==============================================================================
def draw_iron_reaver(draw, frame_idx, is_back):
    bob = int(math.sin(frame_idx * math.pi / 2.0) * 1.0)
    cy = 78 + bob
    cx = 80

    c_charcoal = (35, 38, 44, 255)
    c_rust_red = (160, 50, 40, 255)
    c_copper = (50, 110, 95, 255)
    c_ember = (255, 90, 20, 255)
    c_iron = (65, 70, 80, 255)
    c_dark = (20, 22, 26, 255)

    # 1. Quad Exhaust Stacks (Emitting embers)
    draw.rectangle([(cx - 26, cy - 36), (cx - 20, cy - 14)], fill=c_dark, outline=c_iron)
    draw.rectangle([(cx - 18, cy - 32), (cx - 14, cy - 14)], fill=c_dark, outline=c_iron)
    draw.rectangle([(cx + 14, cy - 32), (cx + 18, cy - 14)], fill=c_dark, outline=c_iron)
    draw.rectangle([(cx + 20, cy - 36), (cx + 26, cy - 14)], fill=c_dark, outline=c_iron)
    # Sparks / Smoke
    ember_shift = (frame_idx * 3) % 8
    draw.point([(cx - 23, cy - 38 - ember_shift), (cx + 23, cy - 40 - ember_shift)], fill=c_ember)

    # 2. Colossal Biped Tread Feet
    draw.polygon([(cx - 24, cy + 22), (cx - 36, cy + 46), (cx - 26, cy + 62), (cx - 14, cy + 22)], fill=c_charcoal, outline=c_rust_red)
    draw.polygon([(cx - 42, cy + 54), (cx - 18, cy + 54), (cx - 16, cy + 62), (cx - 44, cy + 62)], fill=c_iron, outline=c_charcoal)
    draw.polygon([(cx + 14, cy + 22), (cx + 28, cy + 44), (cx + 22, cy + 62), (cx + 4, cy + 22)], fill=c_charcoal, outline=c_rust_red)
    draw.polygon([(cx + 12, cy + 54), (cx + 36, cy + 54), (cx + 38, cy + 62), (cx + 14, cy + 62)], fill=c_iron, outline=c_charcoal)

    # 3. Massive Torso Fortress
    draw.polygon([(cx - 26, cy - 14), (cx + 26, cy - 14), (cx + 20, cy + 22), (cx - 20, cy + 22)], fill=c_charcoal, outline=c_copper)
    draw.polygon([(cx - 16, cy - 6), (cx + 16, cy - 6), (cx + 12, cy + 16), (cx - 12, cy + 16)], fill=c_rust_red, outline=c_charcoal)
    # Glowing furnace grates
    draw.rectangle([(cx - 8, cy + 2), (cx + 8, cy + 12)], fill=c_dark)
    draw.line([(cx - 6, cy + 5), (cx + 6, cy + 5)], fill=c_ember, width=2)
    draw.line([(cx - 6, cy + 9), (cx + 6, cy + 9)], fill=c_ember, width=2)

    # 4. Oversized Warship Broadside Arm (Right)
    draw.line([(cx + 26, cy - 2), (cx + 36, cy + 16)], fill=c_iron, width=8)
    draw.polygon([(cx + 32, cy + 6), (cx + 68, cy + 8), (cx + 66, cy + 24), (cx + 30, cy + 22)], fill=c_charcoal, outline=c_rust_red)
    draw.rectangle([(cx + 68, cy + 10), (cx + 74, cy + 20)], fill=c_dark) # 200mm Muzzle
    # Left Arm: Spiked Battering Ram Shield
    draw.polygon([(cx - 44, cy - 8), (cx - 26, cy - 12), (cx - 28, cy + 28), (cx - 46, cy + 24)], fill=c_iron, outline=c_copper)
    draw.polygon([(cx - 52, cy + 6), (cx - 44, cy + 4), (cx - 44, cy + 16)], fill=c_rust_red)

    # 5. Pirate Commander Head & Optics
    draw.polygon([(cx - 10, cy - 22), (cx + 10, cy - 22), (cx + 7, cy - 12), (cx - 7, cy - 12)], fill=c_charcoal, outline=c_iron)
    draw.ellipse([(cx - 5, cy - 18), (cx - 1, cy - 14)], fill=c_ember)
    draw.ellipse([(cx + 2, cy - 18), (cx + 6, cy - 14)], fill=c_ember)

# ==============================================================================
# SUIT 5: TAKAHASHI CUSTOM (Zaibatsu Gen 2 Samurai Commander)
# ==============================================================================
def draw_takahashi_custom(draw, frame_idx, is_back):
    bob = int(math.sin(frame_idx * math.pi / 2.0) * 1.5)
    cy = 82 + bob
    cx = 80

    c_obsidian = (20, 22, 28, 255)
    c_gold = (215, 175, 55, 255)
    c_crimson = (195, 30, 45, 255)
    c_jade = (20, 215, 145, 255)
    c_silver = (165, 175, 190, 255)
    c_dark = (12, 14, 18, 255)

    # 1. Twin Sashimono Blade Antennas (Backpack)
    draw.polygon([(cx - 14, cy - 10), (cx - 22, cy - 42), (cx - 18, cy - 42), (cx - 12, cy - 10)], fill=c_crimson, outline=c_gold)
    draw.polygon([(cx + 12, cy - 10), (cx + 18, cy - 42), (cx + 22, cy - 42), (cx + 14, cy - 10)], fill=c_crimson, outline=c_gold)

    # 2. Sleek Samurai Sode Armor Legs
    draw.polygon([(cx - 16, cy + 20), (cx - 24, cy + 42), (cx - 18, cy + 58), (cx - 10, cy + 20)], fill=c_obsidian, outline=c_gold)
    draw.polygon([(cx - 26, cy + 54), (cx - 14, cy + 54), (cx - 12, cy + 59), (cx - 28, cy + 59)], fill=c_crimson, outline=c_silver)
    draw.polygon([(cx + 8, cy + 20), (cx + 18, cy + 40), (cx + 14, cy + 58), (cx + 2, cy + 20)], fill=c_obsidian, outline=c_gold)
    draw.polygon([(cx + 6, cy + 54), (cx + 20, cy + 54), (cx + 24, cy + 59), (cx + 8, cy + 59)], fill=c_crimson, outline=c_silver)

    # 3. Torso Armor / Crest
    draw.polygon([(cx - 16, cy - 12), (cx + 16, cy - 12), (cx + 12, cy + 18), (cx - 12, cy + 18)], fill=c_obsidian, outline=c_gold)
    draw.polygon([(cx - 8, cy - 6), (cx + 8, cy - 6), (cx + 5, cy + 10), (cx - 5, cy + 10)], fill=c_crimson, outline=c_gold)
    # Mon Crest (Zaibatsu Clan Diamond)
    draw.polygon([(cx, cy - 2), (cx + 4, cy + 2), (cx, cy + 6), (cx - 4, cy + 2)], fill=c_gold)

    # 4. Tiered Sode Shoulder Armor & Arms
    # Left Shoulder
    draw.polygon([(cx - 32, cy - 16), (cx - 16, cy - 18), (cx - 14, cy - 2), (cx - 28, cy + 4)], fill=c_obsidian, outline=c_gold)
    draw.polygon([(cx - 34, cy - 2), (cx - 22, cy - 4), (cx - 20, cy + 8), (cx - 30, cy + 12)], fill=c_crimson, outline=c_gold)
    # Right Shoulder
    draw.polygon([(cx + 16, cy - 18), (cx + 32, cy - 16), (cx + 28, cy + 4), (cx + 14, cy - 2)], fill=c_obsidian, outline=c_gold)
    draw.polygon([(cx + 22, cy - 4), (cx + 34, cy - 2), (cx + 30, cy + 12), (cx + 20, cy + 8)], fill=c_crimson, outline=c_gold)

    # 5. Sheathed Tachyon Wakizashi (Hip) & Needle Rifle (Right Arm)
    draw.line([(cx - 14, cy + 8), (cx - 28, cy + 28)], fill=c_crimson, width=4) # Scabbard
    draw.line([(cx - 14, cy + 8), (cx - 10, cy + 2)], fill=c_gold, width=3) # Hilt
    # Right Arm Rifle
    draw.line([(cx + 22, cy), (cx + 32, cy + 16)], fill=c_silver, width=4)
    draw.rectangle([(cx + 30, cy + 8), (cx + 56, cy + 15)], fill=c_obsidian, outline=c_gold)
    draw.line([(cx + 56, cy + 11), (cx + 64, cy + 11)], fill=c_jade, width=2) # Needle barrel

    # 6. Kabuto Crest Head
    draw.ellipse([(cx - 7, cy - 22), (cx + 7, cy - 10)], fill=c_obsidian, outline=c_gold)
    draw.line([(cx - 5, cy - 15), (cx + 5, cy - 15)], fill=c_jade, width=2) # Optic Visor
    # Golden Crescent Moon Crest (Kabuto Maedate)
    draw.arc([cx - 12, cy - 34, cx + 12, cy - 18], 180, 360, fill=c_gold, width=3)

# ==============================================================================
# SUIT 6: KAMAITACHI (Zaibatsu Gen 3 Plasma Skirmisher)
# ==============================================================================
def draw_kamaitachi(draw, frame_idx, is_back):
    bob = int(math.sin(frame_idx * math.pi / 2.0) * 1.5)
    cy = 82 + bob
    cx = 80

    c_graphite = (40, 44, 52, 255)
    c_cyan = (25, 230, 255, 255)
    c_silver = (190, 200, 215, 255)
    c_plasma = (0, 255, 200, 255)
    c_dark = (18, 20, 24, 255)

    # 1. Dual Curved Scythe Vernier Binders (Sweeping behind)
    draw.polygon([(cx - 16, cy - 8), (cx - 38, cy - 34), (cx - 30, cy - 4), (cx - 14, cy + 6)], fill=c_graphite, outline=c_cyan)
    draw.line([(cx - 36, cy - 28), (cx - 24, cy - 2)], fill=c_plasma, width=2)
    draw.polygon([(cx + 16, cy - 8), (cx + 38, cy - 34), (cx + 30, cy - 4), (cx + 14, cy + 6)], fill=c_graphite, outline=c_cyan)
    draw.line([(cx + 36, cy - 28), (cx + 24, cy - 2)], fill=c_plasma, width=2)

    # 2. Reverse-Joint Agility Legs
    draw.polygon([(cx - 14, cy + 18), (cx - 28, cy + 32), (cx - 20, cy + 46), (cx - 24, cy + 58), (cx - 12, cy + 58), (cx - 10, cy + 18)], fill=c_graphite, outline=c_silver)
    draw.polygon([(cx + 10, cy + 18), (cx + 22, cy + 32), (cx + 16, cy + 46), (cx + 18, cy + 58), (cx + 8, cy + 58), (cx + 4, cy + 18)], fill=c_graphite, outline=c_silver)
    # Ankle plasma thrusters
    draw.rectangle([(cx - 22, cy + 50), (cx - 16, cy + 54)], fill=c_cyan)
    draw.rectangle([(cx + 14, cy + 50), (cx + 18, cy + 54)], fill=c_cyan)

    # 3. Aerodynamic Needle Cockpit Torso
    draw.polygon([(cx - 14, cy - 14), (cx + 14, cy - 14), (cx + 8, cy + 16), (cx - 8, cy + 16)], fill=c_silver, outline=c_graphite)
    draw.polygon([(cx - 6, cy - 8), (cx + 6, cy - 8), (cx, cy + 12)], fill=c_cyan, outline=c_dark)

    # 4. High-Speed Plasma Lance Arms
    draw.line([(cx - 18, cy - 2), (cx - 30, cy + 14)], fill=c_graphite, width=4)
    draw.line([(cx + 18, cy - 2), (cx + 30, cy + 14)], fill=c_graphite, width=4)
    # Twin plasma forearm blade emitters
    draw.polygon([(cx - 34, cy + 6), (cx - 48, cy + 22), (cx - 30, cy + 20)], fill=c_plasma, outline=c_cyan)
    draw.polygon([(cx + 30, cy + 6), (cx + 46, cy + 22), (cx + 28, cy + 20)], fill=c_plasma, outline=c_cyan)

    # 5. Streamlined Aerodynamic Head
    draw.polygon([(cx - 6, cy - 24), (cx + 6, cy - 24), (cx + 3, cy - 12), (cx - 3, cy - 12)], fill=c_silver, outline=c_graphite)
    draw.line([(cx - 4, cy - 17), (cx + 4, cy - 17)], fill=c_cyan, width=2)
    # Needle blade crest
    draw.line([(cx, cy - 24), (cx, cy - 36)], fill=c_plasma, width=2)


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
print("Generating 6 bespoke canonical mobile suit sprites (front & back)...")

suits = [
    ("spr_ms_cassian_custom_idle", draw_cassian_custom, False),
    ("spr_ms_cassian_custom_back_idle", draw_cassian_custom, True),
    ("spr_ms_chronos_idle", draw_chronos, False),
    ("spr_ms_chronos_back_idle", draw_chronos, True),
    ("spr_ms_marauder_idle", draw_marauder, False),
    ("spr_ms_marauder_back_idle", draw_marauder, True),
    ("spr_ms_iron_reaver_idle", draw_iron_reaver, False),
    ("spr_ms_iron_reaver_back_idle", draw_iron_reaver, True),
    ("spr_ms_takahashi_custom_idle", draw_takahashi_custom, False),
    ("spr_ms_takahashi_custom_back_idle", draw_takahashi_custom, True),
    ("spr_ms_kamaitachi_idle", draw_kamaitachi, False),
    ("spr_ms_kamaitachi_back_idle", draw_kamaitachi, True),
]

for name, func, is_back in suits:
    create_suit_sprite(name, func, is_back=is_back, num_frames=4)
    print(f"  Created: {name}")

# Now register new sprites in MechMakerConcept.yyp if not already present
with open(YYP_PATH, "r") as f:
    yyp = json.load(f)

existing_res = {r["id"]["name"] for r in yyp.get("resources", [])}
added = 0
for name, _, _ in suits:
    if name not in existing_res:
        yyp["resources"].append({
            "id": {
                "name": name,
                "path": f"sprites/{name}/{name}.yy"
            }
        })
        added += 1

with open(YYP_PATH, "w") as f:
    json.dump(yyp, f, indent=2)

print(f"Registered {added} new sprites into {YYP_PATH}!")
