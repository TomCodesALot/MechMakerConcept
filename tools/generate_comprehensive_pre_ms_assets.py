import os
import json
import uuid
from PIL import Image, ImageDraw

SPRITES_DIR = "sprites"
YYP_PATH = "MechMakerConcept.yyp"

def build_sprite(sprite_name, draw_func, num_frames=4):
    spr_path = os.path.join(SPRITES_DIR, sprite_name)
    layers_path = os.path.join(spr_path, "layers")
    os.makedirs(spr_path, exist_ok=True)
    os.makedirs(layers_path, exist_ok=True)

    layer_id = str(uuid.uuid4())
    frame_uuids = [str(uuid.uuid4()) for _ in range(num_frames)]

    for i, f_uuid in enumerate(frame_uuids):
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw_func(draw, i)

        # Save main frame and layer png
        main_png = os.path.join(spr_path, f"{f_uuid}.png")
        im.save(main_png, "PNG")
        layer_dir = os.path.join(layers_path, f_uuid)
        os.makedirs(layer_dir, exist_ok=True)
        layer_png = os.path.join(layer_dir, f"{layer_id}.png")
        im.save(layer_png, "PNG")

    # Generate .yy file
    yy_data = {
        "$GMSprite": "v2",
        "%Name": sprite_name,
        "bboxMode": 0,
        "bbox_bottom": 156,
        "bbox_left": 10,
        "bbox_right": 150,
        "bbox_top": 10,
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
                "$GMImageLayer": "v1",
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
        "origin": 9,
        "parent": {
            "name": "sprites",
            "path": "folders/Sprites.yy"
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
                                "Key": float(idx),
                                "Length": 1.0,
                                "resourceType": "Keyframe<SpriteFrameKeyframe>",
                                "resourceVersion": "2.0",
                                "Stretch": False
                            } for idx, f_uuid in enumerate(frame_uuids)
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

    print(f"Created sprite: {sprite_name}")

# =============================================================================
# DRAWING PROCEDURES
# =============================================================================

# --- 1. TERRAN INFANTRY SQUAD ---
def draw_terran_infantry(draw, frame, is_back=False):
    # Ground shadow across tile
    draw.ellipse([30, 138, 130, 152], fill=(0, 0, 0, 85))

    y_bob = -1 if (frame % 2 == 1) else 0

    # Sandbag fortification on tile
    draw.polygon([(45, 142), (115, 142), (110, 134), (40, 134)], fill=(120, 110, 85, 255), outline=(60, 55, 40, 255))
    draw.polygon([(48, 134), (108, 134), (104, 126), (52, 126)], fill=(135, 125, 95, 255), outline=(60, 55, 40, 255))

    # 4 Soldiers positioned in fireteam formation
    # Soldier positions: (x, y) relative to ground
    soldiers = [
        (60, 122),  # Left Heavy Gunner
        (80, 126),  # Center Squad Leader
        (100, 120), # Right AT Missileer
        (78, 112)   # Rear Comms / Marksman
    ]

    for idx, (sx, sy) in enumerate(soldiers):
        b_y = sy + y_bob if (idx % 2 == frame % 2) else sy
        # Small soldier shadow
        draw.ellipse([sx - 8, b_y + 12, sx + 8, b_y + 18], fill=(0, 0, 0, 70))

        if not is_back:
            # Body / Legs (Khaki / Olive)
            draw.rectangle([sx - 4, b_y + 4, sx + 4, b_y + 14], fill=(55, 65, 50, 255), outline=(25, 30, 22, 255))
            # Torso Armor (Dark Steel Plate)
            draw.rectangle([sx - 5, b_y - 2, sx + 5, b_y + 6], fill=(40, 48, 38, 255), outline=(20, 25, 18, 255))
            # Helmet (Olive Ballistic Dome)
            draw.ellipse([sx - 5, b_y - 12, sx + 5, b_y - 3], fill=(65, 78, 60, 255), outline=(30, 36, 28, 255))
            # Goggles / Visor
            draw.rectangle([sx - 3, b_y - 7, sx + 3, b_y - 5], fill=(240, 180, 50, 255))

            # Specialized Weapons
            if idx == 0:
                # Heavy Machine Gun on bipod resting on sandbag
                draw.line([(sx + 2, b_y + 2), (sx + 16, b_y + 4)], fill=(20, 20, 20, 255), width=2)
                draw.rectangle([sx + 8, b_y + 2, sx + 12, b_y + 6], fill=(50, 50, 50, 255))
                if frame == 3:
                    # Muzzle spark
                    draw.ellipse([sx + 16, b_y + 2, sx + 22, b_y + 6], fill=(255, 220, 80, 255))
            elif idx == 2:
                # Shoulder Anti-Tank Missile Tube (Bazooka)
                draw.rectangle([sx - 8, b_y - 8, sx + 14, b_y - 2], fill=(45, 55, 45, 255), outline=(20, 25, 20, 255))
                draw.ellipse([sx + 12, b_y - 8, sx + 16, b_y - 2], fill=(80, 40, 30, 255))
            elif idx == 1:
                # Assault Carbine
                draw.line([(sx + 2, b_y + 2), (sx + 10, b_y + 4)], fill=(25, 25, 25, 255), width=2)
            elif idx == 3:
                # Radio Antenna
                draw.line([(sx + 3, b_y - 6), (sx + 3, b_y - 22)], fill=(180, 180, 180, 255), width=1)
        else:
            # BACK PERSPECTIVE
            draw.rectangle([sx - 4, b_y + 4, sx + 4, b_y + 14], fill=(55, 65, 50, 255), outline=(25, 30, 22, 255))
            # Combat Rucksack
            draw.rectangle([sx - 5, b_y - 3, sx + 5, b_y + 7], fill=(80, 70, 55, 255), outline=(35, 30, 22, 255))
            draw.line([(sx - 4, b_y), (sx + 4, b_y)], fill=(120, 105, 80, 255), width=1)
            # Helmet Back
            draw.ellipse([sx - 5, b_y - 12, sx + 5, b_y - 3], fill=(65, 78, 60, 255), outline=(30, 36, 28, 255))
            if idx == 3:
                draw.line([(sx + 3, b_y - 6), (sx + 3, b_y - 22)], fill=(180, 180, 180, 255), width=1)
            elif idx == 2:
                # Rear of missile tube
                draw.ellipse([sx - 10, b_y - 8, sx - 6, b_y - 2], fill=(20, 20, 20, 255))

# --- 2. COLONY VOID / ZERO-G INFANTRY SQUAD ---
def draw_colony_infantry(draw, frame, is_back=False):
    draw.ellipse([32, 138, 128, 152], fill=(0, 0, 0, 80))
    # Hover jump thruster bob
    j_bob = -2 if (frame % 2 == 1) else 1

    soldiers = [
        (58, 120 + j_bob),
        (78, 124 + j_bob),
        (102, 118 + j_bob),
        (82, 110 + j_bob)
    ]

    for idx, (sx, sy) in enumerate(soldiers):
        draw.ellipse([sx - 6, sy + 14, sx + 6, sy + 19], fill=(0, 220, 255, 45))

        if not is_back:
            # Sleek White/Cyan Void Suit
            draw.rectangle([sx - 4, sy + 4, sx + 4, sy + 14], fill=(210, 225, 240, 255), outline=(30, 60, 100, 255))
            draw.rectangle([sx - 5, sy - 2, sx + 5, sy + 6], fill=(40, 75, 125, 255), outline=(15, 35, 65, 255))
            # Curved Gold Visor Helmet
            draw.ellipse([sx - 5, sy - 12, sx + 5, sy - 3], fill=(225, 235, 245, 255), outline=(30, 60, 100, 255))
            draw.ellipse([sx - 3, sy - 9, sx + 3, sy - 5], fill=(0, 235, 255, 255))

            # Pulse Carbines & Linear Launchers
            draw.line([(sx + 2, sy + 2), (sx + 12, sy + 4)], fill=(0, 180, 240, 255), width=2)
            if idx == 2:
                # Shoulder Micro-Missile Tube
                draw.rectangle([sx - 6, sy - 9, sx + 12, sy - 4], fill=(25, 55, 95, 255), outline=(0, 220, 255, 255))
        else:
            # BACK VIEW: Twin Vernier Thruster Jump Packs
            draw.rectangle([sx - 4, sy + 4, sx + 4, sy + 14], fill=(210, 225, 240, 255), outline=(30, 60, 100, 255))
            # Vernier Jump Pack
            draw.rectangle([sx - 5, sy - 3, sx + 5, sy + 7], fill=(30, 50, 85, 255), outline=(0, 220, 255, 255))
            draw.ellipse([sx - 4, sy + 5, sx - 1, sy + 9], fill=(0, 240, 255, 255))
            draw.ellipse([sx + 1, sy + 5, sx + 4, sy + 9], fill=(0, 240, 255, 255))
            draw.ellipse([sx - 5, sy - 12, sx + 5, sy - 3], fill=(225, 235, 245, 255), outline=(30, 60, 100, 255))

# --- 3. SYNDICATE GUERRILLA MILITIA SQUAD ---
def draw_syndicate_infantry(draw, frame, is_back=False):
    draw.ellipse([30, 138, 130, 152], fill=(0, 0, 0, 90))
    y_bob = -1 if (frame % 2 == 1) else 0

    # Improvised scrap metal barricade
    draw.polygon([(46, 142), (114, 142), (108, 132), (52, 132)], fill=(75, 45, 35, 255), outline=(35, 20, 15, 255))
    draw.line([(55, 134), (105, 140)], fill=(220, 120, 30, 255), width=2)

    soldiers = [
        (62, 123),
        (82, 126),
        (102, 121),
        (76, 114)
    ]

    for idx, (sx, sy) in enumerate(soldiers):
        b_y = sy + y_bob if (idx % 2 == frame % 2) else sy
        draw.ellipse([sx - 7, b_y + 12, sx + 7, b_y + 17], fill=(0, 0, 0, 75))

        if not is_back:
            # Trench coat & scrap iron vest
            draw.rectangle([sx - 4, b_y + 4, sx + 4, b_y + 14], fill=(45, 38, 35, 255), outline=(20, 18, 16, 255))
            draw.rectangle([sx - 5, b_y - 2, sx + 5, b_y + 6], fill=(110, 55, 38, 255), outline=(50, 25, 18, 255))
            # Gas Mask / Scrap Helmet
            draw.ellipse([sx - 5, b_y - 12, sx + 5, b_y - 3], fill=(70, 60, 55, 255), outline=(30, 25, 22, 255))
            draw.ellipse([sx - 3, b_y - 8, sx - 1, b_y - 6], fill=(255, 120, 30, 255))
            draw.ellipse([sx + 1, b_y - 8, sx + 3, b_y - 6], fill=(255, 120, 30, 255))

            # RPG / Sawn-off Autocannon
            if idx == 2:
                # Improvised RPG with oversized warhead
                draw.line([(sx - 6, b_y - 4), (sx + 14, b_y - 4)], fill=(30, 30, 30, 255), width=3)
                draw.polygon([(sx + 14, b_y - 7), (sx + 20, b_y - 4), (sx + 14, b_y - 1)], fill=(220, 80, 40, 255))
            else:
                draw.line([(sx + 2, b_y + 2), (sx + 12, b_y + 3)], fill=(25, 25, 25, 255), width=2)
        else:
            # Back view
            draw.rectangle([sx - 4, b_y + 4, sx + 4, b_y + 14], fill=(45, 38, 35, 255), outline=(20, 18, 16, 255))
            draw.rectangle([sx - 5, b_y - 2, sx + 5, b_y + 6], fill=(85, 45, 32, 255), outline=(35, 20, 15, 255))
            draw.ellipse([sx - 5, b_y - 12, sx + 5, b_y - 3], fill=(70, 60, 55, 255), outline=(30, 25, 22, 255))

# --- 4. ZAIBATSU CYBER-ANDROID SHOCK TROOPS ---
def draw_zaibatsu_infantry(draw, frame, is_back=False):
    draw.ellipse([30, 138, 130, 152], fill=(0, 0, 0, 85))
    y_bob = -1 if (frame % 2 == 1) else 0

    soldiers = [
        (60, 122),
        (80, 125),
        (100, 121),
        (78, 113)
    ]

    for idx, (sx, sy) in enumerate(soldiers):
        b_y = sy + y_bob if (idx % 2 == frame % 2) else sy
        draw.ellipse([sx - 6, b_y + 12, sx + 6, b_y + 17], fill=(0, 0, 0, 70))

        if not is_back:
            # Sleek Black/Carbon Monocoque Android Chassis
            draw.rectangle([sx - 4, b_y + 4, sx + 4, b_y + 14], fill=(22, 18, 28, 255), outline=(70, 55, 90, 255))
            draw.rectangle([sx - 5, b_y - 2, sx + 5, b_y + 6], fill=(35, 28, 48, 255), outline=(90, 70, 120, 255))
            # Angular Cylindrical Head with Horizontal Red/Green Lens
            draw.rectangle([sx - 4, b_y - 12, sx + 4, b_y - 3], fill=(18, 15, 24, 255), outline=(90, 70, 120, 255))
            draw.line([(sx - 3, b_y - 7), (sx + 3, b_y - 7)], fill=(0, 255, 180, 255), width=2)
            # Forearm Integrated Rail-Needles
            draw.line([(sx + 2, b_y + 2), (sx + 14, b_y + 2)], fill=(0, 255, 180, 255), width=2)
        else:
            # Back view: Power Conduit & Heat Sinks
            draw.rectangle([sx - 4, b_y + 4, sx + 4, b_y + 14], fill=(22, 18, 28, 255), outline=(70, 55, 90, 255))
            draw.rectangle([sx - 5, b_y - 2, sx + 5, b_y + 6], fill=(35, 28, 48, 255), outline=(90, 70, 120, 255))
            draw.line([(sx, b_y - 2), (sx, b_y + 6)], fill=(0, 255, 180, 255), width=1)
            draw.rectangle([sx - 4, b_y - 12, sx + 4, b_y - 3], fill=(18, 15, 24, 255), outline=(90, 70, 120, 255))

# --- 5. COLONY VALKYRIE TILT-ROTOR GUNSHIP ---
def draw_colony_gunship(draw, frame, is_back=False):
    # High altitude ground shadow
    draw.ellipse([35, 142, 125, 152], fill=(0, 0, 0, 70))
    f_bob = -2 if (frame % 2 == 1) else 1

    hull_blue = (35, 65, 110, 255)
    cyan_glow = (0, 235, 255, 255)

    if not is_back:
        # Front Cockpit & Fuselage
        draw.polygon([(70, 80 + f_bob), (90, 80 + f_bob), (86, 125 + f_bob), (74, 125 + f_bob)], fill=hull_blue, outline=(15, 35, 65, 255), width=2)
        draw.ellipse([74, 98 + f_bob, 86, 115 + f_bob], fill=(10, 25, 50, 255), outline=cyan_glow)
        # Outrigger Tilt-Wings
        draw.rectangle([25, 88 + f_bob, 70, 98 + f_bob], fill=hull_blue, outline=(15, 35, 65, 255))
        draw.rectangle([90, 88 + f_bob, 135, 98 + f_bob], fill=hull_blue, outline=(15, 35, 65, 255))
        # Twin Tilt-Rotors (with spinning motion blur)
        for rx in [22, 138]:
            draw.ellipse([rx - 6, 75 + f_bob, rx + 6, 110 + f_bob], fill=(20, 40, 70, 255), outline=cyan_glow)
            # Rotor disc blur
            r_rad = 22
            draw.ellipse([rx - r_rad, 85 + f_bob, rx + r_rad, 95 + f_bob], fill=(0, 220, 255, 60), outline=cyan_glow)
        # Chin Mounted Gatling Turret
        draw.line([(80, 125 + f_bob), (80, 138 + f_bob)], fill=(20, 20, 20, 255), width=2)
    else:
        # Back View: Twin Turbines & Rear Cargo Ramp
        draw.polygon([(70, 75 + f_bob), (90, 75 + f_bob), (85, 120 + f_bob), (75, 120 + f_bob)], fill=hull_blue, outline=(15, 35, 65, 255), width=2)
        draw.rectangle([25, 85 + f_bob, 135, 95 + f_bob], fill=hull_blue, outline=(15, 35, 65, 255))
        # Twin Tail Stabilizers
        draw.polygon([(68, 60 + f_bob), (74, 60 + f_bob), (74, 85 + f_bob), (66, 85 + f_bob)], fill=(25, 50, 90, 255))
        draw.polygon([(86, 60 + f_bob), (92, 60 + f_bob), (94, 85 + f_bob), (86, 85 + f_bob)], fill=(25, 50, 90, 255))
        for rx in [22, 138]:
            draw.ellipse([rx - 6, 75 + f_bob, rx + 6, 110 + f_bob], fill=(20, 40, 70, 255), outline=cyan_glow)
            draw.ellipse([rx - 20, 85 + f_bob, rx + 20, 95 + f_bob], fill=(0, 220, 255, 60), outline=cyan_glow)

# --- 6. SYNDICATE BUZZARD LIGHT BOMBER ---
def draw_syndicate_bomber(draw, frame, is_back=False):
    draw.ellipse([30, 142, 130, 152], fill=(0, 0, 0, 75))
    f_bob = -1 if (frame % 2 == 1) else 0

    scrap_rust = (115, 55, 38, 255)
    dark_iron = (45, 35, 30, 255)

    if not is_back:
        # Nose Radial Engine & Spinning Propeller
        draw.ellipse([74, 122 + f_bob, 86, 134 + f_bob], fill=dark_iron, outline=(220, 120, 30, 255))
        # Propeller Blur
        p_angle = (frame * 45)
        draw.line([(80 - 18, 128 + f_bob), (80 + 18, 128 + f_bob)], fill=(240, 200, 100, 120), width=3)
        # Asymmetrical Welded Wings
        draw.polygon([(15, 102 + f_bob), (74, 88 + f_bob), (74, 118 + f_bob), (20, 122 + f_bob)], fill=scrap_rust, outline=dark_iron, width=2)
        draw.polygon([(145, 102 + f_bob), (86, 88 + f_bob), (86, 118 + f_bob), (140, 122 + f_bob)], fill=scrap_rust, outline=dark_iron, width=2)
        # Fuselage & Cockpit Glass
        draw.polygon([(72, 65 + f_bob), (88, 65 + f_bob), (86, 125 + f_bob), (74, 125 + f_bob)], fill=scrap_rust, outline=dark_iron, width=2)
        draw.rectangle([76, 88 + f_bob, 84, 102 + f_bob], fill=(30, 25, 20, 255), outline=(220, 120, 30, 255))
        # Underwing Incendiary Drums
        draw.rectangle([35, 112 + f_bob, 48, 126 + f_bob], fill=(160, 40, 30, 255), outline=dark_iron)
        draw.rectangle([112, 112 + f_bob, 125, 126 + f_bob], fill=(160, 40, 30, 255), outline=dark_iron)
    else:
        # Back: Twin Booms & Exhaust soot
        draw.polygon([(15, 102 + f_bob), (74, 88 + f_bob), (74, 118 + f_bob), (20, 122 + f_bob)], fill=scrap_rust, outline=dark_iron, width=2)
        draw.polygon([(145, 102 + f_bob), (86, 88 + f_bob), (86, 118 + f_bob), (140, 122 + f_bob)], fill=scrap_rust, outline=dark_iron, width=2)
        # Twin tail rudders
        draw.rectangle([45, 60 + f_bob, 52, 95 + f_bob], fill=scrap_rust, outline=dark_iron)
        draw.rectangle([108, 60 + f_bob, 115, 95 + f_bob], fill=scrap_rust, outline=dark_iron)
        draw.line([(48, 62 + f_bob), (112, 62 + f_bob)], fill=dark_iron, width=2)

# --- 7. ZAIBATSU KAMAITACHI STEALTH DRONE JET ---
def draw_zaibatsu_drone_jet(draw, frame, is_back=False):
    draw.ellipse([35, 142, 125, 152], fill=(0, 0, 0, 75))
    f_bob = -1 if (frame % 2 == 1) else 1

    stealth_black = (20, 16, 26, 255)
    carbon_trim = (55, 45, 75, 255)
    green_lens = (0, 255, 180, 255)

    if not is_back:
        # Diamond Flying Wing (No Cockpit)
        draw.polygon([(80, 145 + f_bob), (145, 95 + f_bob), (80, 65 + f_bob), (15, 95 + f_bob)], fill=stealth_black, outline=carbon_trim, width=2)
        draw.line([(80, 65 + f_bob), (80, 145 + f_bob)], fill=green_lens, width=1)
        # Optical Sensor Slits
        draw.polygon([(74, 115 + f_bob), (86, 115 + f_bob), (80, 128 + f_bob)], fill=(10, 8, 14, 255), outline=green_lens)
    else:
        # Back: Vectoring Exhaust
        draw.polygon([(80, 145 + f_bob), (145, 95 + f_bob), (80, 65 + f_bob), (15, 95 + f_bob)], fill=stealth_black, outline=carbon_trim, width=2)
        # Blue Ion Exhaust Slot
        draw.polygon([(72, 110 + f_bob), (88, 110 + f_bob), (80, 122 + f_bob)], fill=(0, 255, 180, 255))
        draw.polygon([(76, 122 + f_bob), (80, 142 + f_bob), (84, 122 + f_bob)], fill=(0, 255, 200, 200))

# --- 8. WRECKAGE & DESTRUCTION STATES ---
def draw_tank_wreckage(draw, frame):
    draw.ellipse([20, 138, 140, 154], fill=(0, 0, 0, 110))
    # Cratered earth
    draw.ellipse([26, 130, 134, 150], fill=(30, 25, 20, 255), outline=(15, 12, 10, 255))
    # Burned out hull
    draw.polygon([(36, 136), (124, 136), (116, 110), (44, 110)], fill=(25, 25, 25, 255), outline=(15, 15, 15, 255), width=2)
    # Detached turret blown off to the side
    draw.polygon([(18, 134), (54, 134), (48, 116), (24, 116)], fill=(35, 32, 30, 255), outline=(15, 15, 15, 255))
    draw.line([(20, 125), (6, 115)], fill=(15, 15, 15, 255), width=3)
    # Smoking embers
    draw.ellipse([70, 105, 80, 115], fill=(240, 90, 20, 220))
    if frame % 2 == 1:
        draw.ellipse([72, 90, 84, 102], fill=(60, 60, 60, 150))
        draw.ellipse([76, 75, 90, 88], fill=(40, 40, 40, 100))

def draw_plane_wreckage(draw, frame):
    draw.ellipse([25, 138, 135, 154], fill=(0, 0, 0, 100))
    # Crash scar
    draw.polygon([(10, 140), (150, 140), (130, 120), (30, 120)], fill=(25, 20, 18, 255))
    # Embedded nose & snapped wings
    draw.polygon([(70, 142), (90, 142), (85, 115), (75, 115)], fill=(30, 30, 35, 255))
    # Broken port wing
    draw.polygon([(25, 132), (65, 122), (68, 136), (28, 142)], fill=(40, 42, 48, 255))
    # Fire & smoke
    draw.ellipse([78, 110, 88, 120], fill=(255, 140, 30, 240))
    if frame % 2 == 1:
        draw.ellipse([75, 95, 89, 107], fill=(50, 50, 50, 160))

def draw_infantry_suppressed(draw, frame):
    draw.ellipse([30, 138, 130, 152], fill=(0, 0, 0, 85))
    # Cratered dirt mound / ruined sandbags
    draw.polygon([(40, 144), (120, 144), (110, 130), (50, 130)], fill=(80, 70, 55, 255), outline=(40, 35, 25, 255))
    # Prone soldiers taking cover / heads down
    draw.rectangle([55, 134, 75, 142], fill=(50, 58, 48, 255), outline=(25, 30, 22, 255))
    draw.ellipse([52, 133, 60, 141], fill=(60, 72, 55, 255))
    draw.rectangle([85, 132, 105, 140], fill=(50, 58, 48, 255), outline=(25, 30, 22, 255))
    draw.ellipse([100, 131, 108, 139], fill=(60, 72, 55, 255))

# =============================================================================
# BATCH GENERATION
# =============================================================================

sprites_to_build = [
    # Terran Infantry
    ("spr_inf_terran_squad_idle", lambda d, f: draw_terran_infantry(d, f, False)),
    ("spr_inf_terran_squad_back_idle", lambda d, f: draw_terran_infantry(d, f, True)),
    # Colony Void Infantry
    ("spr_inf_colony_squad_idle", lambda d, f: draw_colony_infantry(d, f, False)),
    ("spr_inf_colony_squad_back_idle", lambda d, f: draw_colony_infantry(d, f, True)),
    # Syndicate Guerrilla Militia
    ("spr_inf_syndicate_squad_idle", lambda d, f: draw_syndicate_infantry(d, f, False)),
    ("spr_inf_syndicate_squad_back_idle", lambda d, f: draw_syndicate_infantry(d, f, True)),
    # Zaibatsu Android Shock Troops
    ("spr_inf_zaibatsu_squad_idle", lambda d, f: draw_zaibatsu_infantry(d, f, False)),
    ("spr_inf_zaibatsu_squad_back_idle", lambda d, f: draw_zaibatsu_infantry(d, f, True)),
    # Additional Conventional Aircraft
    ("spr_veh_colony_gunship_idle", lambda d, f: draw_colony_gunship(d, f, False)),
    ("spr_veh_colony_gunship_back_idle", lambda d, f: draw_colony_gunship(d, f, True)),
    ("spr_veh_syndicate_bomber_idle", lambda d, f: draw_syndicate_bomber(d, f, False)),
    ("spr_veh_syndicate_bomber_back_idle", lambda d, f: draw_syndicate_bomber(d, f, True)),
    ("spr_veh_zaibatsu_drone_jet_idle", lambda d, f: draw_zaibatsu_drone_jet(d, f, False)),
    ("spr_veh_zaibatsu_drone_jet_back_idle", lambda d, f: draw_zaibatsu_drone_jet(d, f, True)),
    # Battlefield Wreckages
    ("spr_veh_wreckage_tank", draw_tank_wreckage),
    ("spr_veh_wreckage_plane", draw_plane_wreckage),
    ("spr_inf_suppressed", draw_infantry_suppressed)
]

for spr_name, draw_fn in sprites_to_build:
    build_sprite(spr_name, draw_fn)

# Register all in MechMakerConcept.yyp
with open(YYP_PATH, "r") as f:
    yyp_content = f.read()

registered_count = 0
for spr_name, _ in sprites_to_build:
    spr_path = f"sprites/{spr_name}/{spr_name}.yy"
    res_entry = f"{{\"id\":{{\"name\":\"{spr_name}\",\"path\":\"{spr_path}\",}},}},"
    if spr_name not in yyp_content:
        marker = '"resources": ['
        idx = yyp_content.find(marker)
        if idx != -1:
            insert_pos = idx + len(marker)
            yyp_content = yyp_content[:insert_pos] + f"\n    {res_entry}" + yyp_content[insert_pos:]
            registered_count += 1

with open(YYP_PATH, "w") as f:
    f.write(yyp_content)

print(f"All {len(sprites_to_build)} assets successfully generated! Registered {registered_count} new entries in {YYP_PATH}.")
