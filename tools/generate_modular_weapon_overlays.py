import os
import json
import uuid
from PIL import Image, ImageDraw

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITES_DIR = os.path.join(ROOT_DIR, "sprites")
YYP_PATH = os.path.join(ROOT_DIR, "MechMakerConcept.yyp")

WEAPONS = [
    # 1. Terran Coalition (TC)
    {
        "id": "spr_wpn_tc_carbine_90mm",
        "name": "Type-45 90mm Kinetic Carbine",
        "faction": "faction_a",
        "slot": "primary",
        "draw_func": "tc_carbine"
    },
    {
        "id": "spr_wpn_tc_cannon_150mm",
        "name": "150mm Recoil Howitzer / Autocannon",
        "faction": "faction_a",
        "slot": "support",
        "draw_func": "tc_cannon"
    },
    {
        "id": "spr_wpn_tc_tower_shield",
        "name": "Cast-Alloy Riot Tower Shield",
        "faction": "faction_a",
        "slot": "secondary",
        "draw_func": "tc_shield"
    },
    # 2. Outer Colony League (OCL)
    {
        "id": "spr_wpn_ocl_beam_spray",
        "name": "Focused Pulse Beam Spray Gun",
        "faction": "faction_b",
        "slot": "primary",
        "draw_func": "ocl_spray"
    },
    {
        "id": "spr_wpn_ocl_beam_lance",
        "name": "Continuous-Wave Beam Lance",
        "faction": "faction_b",
        "slot": "support",
        "draw_func": "ocl_lance"
    },
    {
        "id": "spr_wpn_ocl_deflector_wing",
        "name": "Ceramic Vernier Deflector Wing",
        "faction": "faction_b",
        "slot": "secondary",
        "draw_func": "ocl_wing"
    },
    # 3. Rust Syndicate Cartel (RSC)
    {
        "id": "spr_wpn_rsc_scrap_flechette",
        "name": "60mm Shrapnel Flechette Gun",
        "faction": "faction_c",
        "slot": "primary",
        "draw_func": "rsc_flechette"
    },
    {
        "id": "spr_wpn_rsc_harpoon_winch",
        "name": "Pneumatic Harpoon Winch",
        "faction": "faction_c",
        "slot": "support",
        "draw_func": "rsc_harpoon"
    },
    {
        "id": "spr_wpn_rsc_rock_saw",
        "name": "Thermite Rock-Saw & Buckler",
        "faction": "faction_c",
        "slot": "secondary",
        "draw_func": "rsc_saw"
    },
    # 4. Apex Bio-Cybernetics Zaibatsu (ABC)
    {
        "id": "spr_wpn_abc_needle_pistol",
        "name": "Subsonic Kinetic Needle Pistol",
        "faction": "faction_d",
        "slot": "primary",
        "draw_func": "abc_needle"
    },
    {
        "id": "spr_wpn_abc_tachyon_katana",
        "name": "High-Frequency Tachyon Katana",
        "faction": "faction_d",
        "slot": "secondary",
        "draw_func": "abc_katana"
    },
    {
        "id": "spr_wpn_abc_tessen_fan",
        "name": "Armored Tessen EMP Fan",
        "faction": "faction_d",
        "slot": "secondary",
        "draw_func": "abc_tessen"
    }
]

def draw_weapon_frame(draw, func_name, frame_idx):
    y_bob = -2 if (frame_idx == 1 or frame_idx == 3) else 0
    is_attack = (frame_idx == 3)

    # 1. Terran 90mm Carbine (Foreground Right Hand: x ~ 102-144, y ~ 80-106)
    if func_name == "tc_carbine":
        draw.rectangle([102, 80 + y_bob, 126, 92 + y_bob], fill=(55, 60, 62, 255), outline=(30, 32, 34, 255), width=1)
        draw.rectangle([126, 83 + y_bob, 142, 88 + y_bob], fill=(42, 45, 48, 255), outline=(20, 22, 24, 255))
        draw.rectangle([138, 81 + y_bob, 144, 90 + y_bob], fill=(60, 64, 68, 255))
        draw.polygon([(110, 92 + y_bob), (118, 92 + y_bob), (116, 106 + y_bob), (108, 106 + y_bob)], fill=(40, 42, 44, 255), outline=(25, 26, 28, 255))
        draw.line([104, 79 + y_bob, 124, 79 + y_bob], fill=(85, 90, 95, 255), width=2)
        if is_attack:
            draw.polygon([(144, 85 + y_bob), (158, 80 + y_bob), (153, 85 + y_bob), (159, 91 + y_bob)], fill=(255, 220, 70, 255))
            draw.ellipse([143, 82 + y_bob, 150, 89 + y_bob], fill=(255, 255, 230, 255))

    # 2. Terran 150mm Cannon (Shoulder/Arm: x ~ 98-152, y ~ 46-70)
    elif func_name == "tc_cannon":
        draw.rectangle([98, 54 + y_bob, 148, 68 + y_bob], fill=(45, 50, 45, 255), outline=(25, 30, 25, 255), width=2)
        draw.rectangle([102, 46 + y_bob, 124, 54 + y_bob], fill=(70, 75, 68, 255), outline=(35, 40, 35, 255))
        draw.rectangle([144, 52 + y_bob, 152, 70 + y_bob], fill=(65, 70, 62, 255))
        draw.line([100, 61 + y_bob, 146, 61 + y_bob], fill=(85, 95, 80, 255), width=1)
        if is_attack:
            draw.polygon([(152, 61 + y_bob), (160, 50 + y_bob), (156, 61 + y_bob), (160, 72 + y_bob)], fill=(255, 180, 40, 255))
            draw.ellipse([150, 56 + y_bob, 158, 66 + y_bob], fill=(255, 240, 180, 255))

    # 3. Terran Tower Shield (Background Left Arm: x ~ 20-50, y ~ 54-140)
    elif func_name == "tc_shield":
        draw.polygon([(20, 60 + y_bob), (46, 54 + y_bob), (50, 134 + y_bob), (24, 140 + y_bob)], fill=(62, 72, 60, 255), outline=(28, 34, 28, 255), width=2)
        draw.line([33, 62 + y_bob, 37, 132 + y_bob], fill=(95, 110, 92, 255), width=3)
        draw.rectangle([28, 74 + y_bob, 42, 78 + y_bob], fill=(20, 24, 20, 255))
        draw.line([30, 76 + y_bob, 40, 76 + y_bob], fill=(255, 160, 40, 255), width=1)
        draw.line([25, 120 + y_bob, 35, 112 + y_bob], fill=(220, 180, 40, 255), width=2)
        draw.line([35, 112 + y_bob, 45, 120 + y_bob], fill=(220, 180, 40, 255), width=2)

    # 4. Colony Pulse Spray Gun (Right Hand: x ~ 104-136, y ~ 80-96)
    elif func_name == "ocl_spray":
        draw.polygon([(104, 82 + y_bob), (130, 80 + y_bob), (128, 94 + y_bob), (106, 96 + y_bob)], fill=(235, 242, 250, 255), outline=(160, 175, 195, 255), width=1)
        draw.rectangle([130, 83 + y_bob, 136, 91 + y_bob], fill=(0, 210, 255, 255), outline=(0, 140, 200, 255))
        draw.line([110, 88 + y_bob, 126, 88 + y_bob], fill=(0, 240, 255, 255), width=2)
        if is_attack:
            draw.ellipse([136, 81 + y_bob, 150, 93 + y_bob], fill=(0, 240, 255, 220))
            draw.ellipse([138, 84 + y_bob, 145, 90 + y_bob], fill=(255, 255, 255, 255))

    # 5. Colony Beam Lance (Arm/Pylon: x ~ 96-156, y ~ 70-86)
    elif func_name == "ocl_lance":
        draw.polygon([(96, 75 + y_bob), (138, 70 + y_bob), (136, 84 + y_bob), (98, 86 + y_bob)], fill=(225, 235, 248, 255), outline=(150, 170, 195, 255))
        draw.line([138, 77 + y_bob, 156, 77 + y_bob], fill=(0, 240, 255, 255), width=3)
        draw.line([140, 77 + y_bob, 156, 77 + y_bob], fill=(255, 255, 255, 255), width=1)
        if is_attack:
            draw.line([156, 77 + y_bob, 160, 77 + y_bob], fill=(120, 250, 255, 255), width=5)
            draw.polygon([(148, 73 + y_bob), (158, 77 + y_bob), (148, 81 + y_bob)], fill=(0, 240, 255, 200))

    # 6. Colony Deflector Wing (Left Arm: x ~ 18-44, y ~ 45-120)
    elif func_name == "ocl_wing":
        draw.polygon([(24, 45 + y_bob), (44, 60 + y_bob), (40, 120 + y_bob), (18, 95 + y_bob)], fill=(240, 245, 255, 255), outline=(140, 165, 195, 255), width=2)
        draw.polygon([(18, 85 + y_bob), (26, 82 + y_bob), (26, 92 + y_bob)], fill=(40, 50, 65, 255))
        draw.line([28, 58 + y_bob, 34, 110 + y_bob], fill=(0, 220, 255, 255), width=2)

    # 7. Syndicate 60mm Flechette Gun (Right Hand: x ~ 102-138, y ~ 82-104)
    elif func_name == "rsc_flechette":
        draw.rectangle([102, 82 + y_bob, 124, 94 + y_bob], fill=(95, 65, 48, 255), outline=(48, 32, 24, 255), width=1)
        draw.rectangle([124, 83 + y_bob, 138, 87 + y_bob], fill=(68, 48, 38, 255))
        draw.rectangle([124, 89 + y_bob, 138, 93 + y_bob], fill=(68, 48, 38, 255))
        draw.ellipse([108, 94 + y_bob, 120, 104 + y_bob], fill=(130, 80, 50, 255))
        if is_attack:
            draw.polygon([(138, 88 + y_bob), (152, 81 + y_bob), (148, 88 + y_bob), (154, 95 + y_bob)], fill=(255, 130, 30, 255))
            draw.ellipse([136, 84 + y_bob, 144, 92 + y_bob], fill=(255, 220, 100, 255))

    # 8. Syndicate Harpoon Winch (Arm/Shoulder: x ~ 98-146, y ~ 66-90)
    elif func_name == "rsc_harpoon":
        draw.rectangle([100, 68 + y_bob, 132, 78 + y_bob], fill=(80, 55, 42, 255), outline=(40, 26, 20, 255), width=1)
        draw.polygon([(132, 66 + y_bob), (146, 73 + y_bob), (132, 80 + y_bob), (135, 73 + y_bob)], fill=(180, 190, 195, 255), outline=(50, 55, 60, 255))
        draw.ellipse([104, 76 + y_bob, 118, 90 + y_bob], fill=(120, 75, 40, 255), outline=(45, 30, 18, 255))
        if is_attack:
            draw.line([144, 73 + y_bob, 158, 73 + y_bob], fill=(240, 240, 250, 255), width=2)
            draw.polygon([(118, 76 + y_bob), (124, 73 + y_bob), (118, 84 + y_bob)], fill=(255, 120, 40, 200))

    # 9. Syndicate Rock-Saw & Buckler (Left Hand: x ~ 22-54, y ~ 72-124)
    elif func_name == "rsc_saw":
        draw.polygon([(26, 72 + y_bob), (48, 76 + y_bob), (44, 124 + y_bob), (22, 120 + y_bob)], fill=(90, 60, 45, 255), outline=(45, 30, 22, 255))
        draw.ellipse([30, 88 + y_bob, 54, 112 + y_bob], fill=(140, 110, 80, 255), outline=(50, 40, 30, 255))
        draw.line([42, 88 + y_bob, 42, 112 + y_bob], fill=(255, 100, 20, 255), width=2)
        draw.line([30, 100 + y_bob, 54, 100 + y_bob], fill=(255, 100, 20, 255), width=2)

    # 10. Zaibatsu Needle Pistol (Right Hand: x ~ 104-138, y ~ 80-90)
    elif func_name == "abc_needle":
        draw.rectangle([104, 82 + y_bob, 126, 90 + y_bob], fill=(25, 28, 35, 255), outline=(10, 12, 16, 255), width=1)
        draw.rectangle([126, 84 + y_bob, 138, 88 + y_bob], fill=(18, 20, 26, 255))
        draw.line([110, 80 + y_bob, 118, 80 + y_bob], fill=(0, 255, 180, 255), width=1)
        if is_attack:
            draw.line([138, 86 + y_bob, 154, 86 + y_bob], fill=(0, 255, 200, 255), width=2)
            draw.ellipse([136, 84 + y_bob, 142, 88 + y_bob], fill=(200, 255, 240, 255))

    # 11. Zaibatsu Tachyon Katana (Foreground Right Hand: x ~ 100-140, y ~ 52-96)
    elif func_name == "abc_katana":
        draw.line([106, 92 + y_bob, 140, 52 + y_bob], fill=(0, 255, 200, 255), width=3)
        draw.line([107, 91 + y_bob, 139, 53 + y_bob], fill=(240, 255, 250, 255), width=1)
        draw.ellipse([102, 89 + y_bob, 109, 96 + y_bob], fill=(220, 180, 50, 255))
        draw.line([98, 98 + y_bob, 104, 91 + y_bob], fill=(20, 22, 28, 255), width=3)
        if is_attack:
            draw.arc([90, 35 + y_bob, 155, 105 + y_bob], start=240, end=350, fill=(0, 255, 200, 220), width=4)

    # 12. Zaibatsu Tessen Fan & Deflector (Left Hand: x ~ 26-54, y ~ 68-105)
    elif func_name == "abc_tessen":
        draw.polygon([(26, 95 + y_bob), (36, 68 + y_bob), (54, 80 + y_bob), (48, 105 + y_bob)], fill=(32, 38, 48, 255), outline=(15, 18, 24, 255))
        draw.line([26, 95 + y_bob, 36, 68 + y_bob], fill=(0, 255, 200, 255), width=1)
        draw.line([26, 95 + y_bob, 46, 73 + y_bob], fill=(220, 180, 50, 255), width=1)
        draw.line([26, 95 + y_bob, 54, 80 + y_bob], fill=(0, 255, 200, 255), width=1)

def create_weapon_sprite(wpn):
    spr_name = wpn["id"]
    spr_path = os.path.join(SPRITES_DIR, spr_name)
    layers_path = os.path.join(spr_path, "layers")
    os.makedirs(spr_path, exist_ok=True)
    os.makedirs(layers_path, exist_ok=True)

    layer_id = str(uuid.uuid4())
    frame_uuids = [str(uuid.uuid4()) for _ in range(4)]
    
    # 4 frames (160x160)
    for i, f_uuid in enumerate(frame_uuids):
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw_weapon_frame(draw, wpn["draw_func"], i)
        
        # Save frame png
        frame_file = os.path.join(spr_path, f"{f_uuid}.png")
        im.save(frame_file)

        # Save single master preview png if first frame
        if i == 0:
            im.save(os.path.join(spr_path, f"{spr_name}.png"))

        # Save layer structure
        layer_dir = os.path.join(layers_path, f_uuid)
        os.makedirs(layer_dir, exist_ok=True)
        im.save(os.path.join(layer_dir, f"{layer_id}.png"))

    # GameMaker 2.0 .yy file
    frames_json = []
    keyframes_json = []
    for i, f_uuid in enumerate(frame_uuids):
        frames_json.append({
            "$GMSpriteFrame": "v1",
            "%Name": f_uuid,
            "name": f_uuid,
            "resourceType": "GMSpriteFrame",
            "resourceVersion": "2.0"
        })
        keyframes_json.append({
            "$Keyframe<SpriteFrameKeyframe>": "",
            "Channels": {
                "0": {
                    "$SpriteFrameKeyframe": "",
                    "Id": {
                        "name": f_uuid,
                        "path": f"sprites/{spr_name}/{spr_name}.yy"
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
        })

    yy_data = {
        "$GMSprite": "v2",
        "%Name": spr_name,
        "bboxMode": 0,
        "bbox_bottom": 159,
        "bbox_left": 0,
        "bbox_right": 159,
        "bbox_top": 0,
        "collisionKind": 1,
        "collisionTolerance": 0,
        "DynamicTexturePage": False,
        "edgeFiltering": False,
        "For3D": False,
        "frames": frames_json,
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
        "name": spr_name,
        "nineSlice": None,
        "origin": 9,
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
            "length": 4.0,
            "lockOrigin": False,
            "moments": {
                "$KeyframeStore<MomentsEventKeyframe>": "",
                "Keyframes": [],
                "resourceType": "KeyframeStore<MomentsEventKeyframe>",
                "resourceVersion": "2.0"
            },
            "name": spr_name,
            "playback": 1,
            "playbackSpeed": 8.0,
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
                        "Keyframes": keyframes_json,
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

    with open(os.path.join(spr_path, f"{spr_name}.yy"), "w") as f:
        json.dump(yy_data, f, indent=2)

    print(f"Generated weapon overlay: {spr_name}")

def register_in_yyp(wpn_list):
    with open(YYP_PATH, "r") as f:
        content = f.read()

    new_entries = []
    for w in wpn_list:
        spr_name = w["id"]
        if spr_name not in content:
            spr_path = f"sprites/{spr_name}/{spr_name}.yy"
            entry = f'{{"id":{{"name":"{spr_name}","path":"{spr_path}",}},}},'
            new_entries.append(entry)

    if new_entries:
        marker = '"resources":['
        idx = content.find(marker)
        if idx != -1:
            insert_pos = idx + len(marker)
            joined = "".join(new_entries)
            content = content[:insert_pos] + joined + content[insert_pos:]
            with open(YYP_PATH, "w") as f:
                f.write(content)
            print(f"Registered {len(new_entries)} new weapon sprites in {YYP_PATH}")
        else:
            print("ERROR: Could not locate '\"resources\":[' in YYP")
    else:
        print("All weapon overlay sprites already registered in YYP.")

if __name__ == "__main__":
    for wpn in WEAPONS:
        create_weapon_sprite(wpn)
    register_in_yyp(WEAPONS)
    print("Weapon overlay sprite generation complete!")
