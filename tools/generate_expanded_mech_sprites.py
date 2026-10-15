import os
import json
import uuid
from PIL import Image, ImageDraw

SPRITES_DIR = "sprites"
YYP_PATH = "MechMakerConcept.yyp"

def create_mech_sprite(sprite_name, base_color, accent_color, glow_color, mech_type):
    spr_path = os.path.join(SPRITES_DIR, sprite_name)
    layers_path = os.path.join(spr_path, "layers")
    os.makedirs(spr_path, exist_ok=True)
    os.makedirs(layers_path, exist_ok=True)

    layer_id = str(uuid.uuid4())
    frame_uuids = [str(uuid.uuid4()) for _ in range(4)]
    
    # Generate 4 distinct animation frames (160x160)
    for i, f_uuid in enumerate(frame_uuids):
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        
        # Ground shadow
        draw.ellipse([35, 142, 125, 154], fill=(0, 0, 0, 90))
        
        # Stride offset based on frame
        y_bob = -2 if (i == 1 or i == 3) else 0
        x_shift = 1 if i == 2 else (-1 if i == 3 else 0)
        
        if mech_type == "ballista":
            # Quadruped Heavy Artillery
            # Rear legs
            draw.polygon([(40 + x_shift, 142 + y_bob), (32 + x_shift, 120 + y_bob), (50 + x_shift, 115 + y_bob), (58 + x_shift, 142 + y_bob)], fill=(45, 52, 42, 255))
            draw.polygon([(102 - x_shift, 142 + y_bob), (110 - x_shift, 120 + y_bob), (128 - x_shift, 115 + y_bob), (120 - x_shift, 142 + y_bob)], fill=(45, 52, 42, 255))
            # Front hydraulic anchors
            draw.polygon([(52 + x_shift, 146 + y_bob), (46 + x_shift, 110 + y_bob), (64 + x_shift, 105 + y_bob), (72 + x_shift, 146 + y_bob)], fill=base_color)
            draw.polygon([(88 - x_shift, 146 + y_bob), (96 - x_shift, 105 + y_bob), (114 - x_shift, 110 + y_bob), (108 - x_shift, 146 + y_bob)], fill=base_color)
            # Low-slung chassis torso
            draw.rounded_rectangle([48, 75 + y_bob, 112, 112 + y_bob], radius=6, fill=base_color, outline=accent_color, width=2)
            # Head sensor turret
            draw.rectangle([68, 62 + y_bob, 92, 75 + y_bob], fill=(35, 40, 32, 255), outline=accent_color)
            draw.line([72, 68 + y_bob, 88, 68 + y_bob], fill=glow_color, width=2)
            # Dual massive howitzer barrels
            barrel_recoil = 4 if i == 3 else 0
            draw.rectangle([42, 28 + y_bob + barrel_recoil, 54, 82 + y_bob], fill=(60, 68, 55, 255), outline=(20, 25, 20, 255), width=2)
            draw.rectangle([106, 28 + y_bob + barrel_recoil, 118, 82 + y_bob], fill=(60, 68, 55, 255), outline=(20, 25, 20, 255), width=2)
            # Muzzle flash on frame 3
            if i == 3:
                draw.polygon([(40, 26), (48, 10), (56, 26)], fill=(255, 200, 50, 240))
                draw.polygon([(104, 26), (112, 10), (120, 26)], fill=(255, 200, 50, 240))
            # Exhaust vents glow
            if i == 1 or i == 3:
                draw.rectangle([64, 105 + y_bob, 72, 110 + y_bob], fill=glow_color)
                draw.rectangle([88, 105 + y_bob, 96, 110 + y_bob], fill=glow_color)

        elif mech_type == "zephyr":
            # High-Speed EW Interceptor (Swept wings, hovering posture)
            # Hover thruster plumes
            plume_len = 16 if (i == 1 or i == 3) else 10
            draw.polygon([(62, 138), (68, 138 + plume_len), (74, 138)], fill=glow_color)
            draw.polygon([(86, 138), (92, 138 + plume_len), (98, 138)], fill=glow_color)
            # Sleek legs tucked in flight
            draw.polygon([(58 + x_shift, 136 + y_bob), (50, 105 + y_bob), (66, 105 + y_bob), (72 + x_shift, 136 + y_bob)], fill=(30, 45, 65, 255))
            draw.polygon([(88 - x_shift, 136 + y_bob), (94, 105 + y_bob), (110, 105 + y_bob), (102 - x_shift, 136 + y_bob)], fill=(30, 45, 65, 255))
            # Aerodynamic swept wings
            draw.polygon([(24, 75 + y_bob), (52, 60 + y_bob), (52, 95 + y_bob)], fill=accent_color, outline=(20, 30, 45, 255))
            draw.polygon([(136, 75 + y_bob), (108, 60 + y_bob), (108, 95 + y_bob)], fill=accent_color, outline=(20, 30, 45, 255))
            # Sleek fuselage torso
            draw.polygon([(80, 42 + y_bob), (104, 70 + y_bob), (96, 108 + y_bob), (64, 108 + y_bob), (56, 70 + y_bob)], fill=base_color, outline=accent_color)
            # Visor & EW sensor pod
            draw.ellipse([70, 52 + y_bob, 90, 62 + y_bob], fill=glow_color)
            # Twin pulse carbines under wings
            draw.rectangle([38, 88 + y_bob, 46, 118 + y_bob], fill=(40, 55, 75, 255))
            draw.rectangle([114, 88 + y_bob, 122, 118 + y_bob], fill=(40, 55, 75, 255))

        elif mech_type == "gorgon":
            # Spiked Boarding Breaker (Massive claw, heavy ram)
            # Heavy stomping legs
            draw.polygon([(46 + x_shift, 146 + y_bob), (40, 108 + y_bob), (62, 108 + y_bob), (68 + x_shift, 146 + y_bob)], fill=(55, 38, 30, 255))
            draw.polygon([(92 - x_shift, 146 + y_bob), (98, 108 + y_bob), (120, 108 + y_bob), (114 - x_shift, 146 + y_bob)], fill=(55, 38, 30, 255))
            # Chunky reinforced torso with hazard stripes
            draw.rectangle([52, 65 + y_bob, 108, 112 + y_bob], fill=base_color, outline=accent_color, width=2)
            # Hazard stripes across breastplate
            draw.line([56, 75 + y_bob, 70, 89 + y_bob], fill=(230, 190, 30, 255), width=3)
            draw.line([72, 75 + y_bob, 86, 89 + y_bob], fill=(230, 190, 30, 255), width=3)
            draw.line([88, 75 + y_bob, 102, 89 + y_bob], fill=(230, 190, 30, 255), width=3)
            # Armored faceplate slit
            draw.rectangle([70, 52 + y_bob, 90, 65 + y_bob], fill=(40, 28, 22, 255))
            draw.line([72, 58 + y_bob, 88, 58 + y_bob], fill=glow_color, width=2)
            # Giant thermal claw on right arm
            claw_open = 4 if i == 3 else 0
            draw.polygon([(26 - claw_open, 65 + y_bob), (48, 70 + y_bob), (44, 98 + y_bob), (22 - claw_open, 105 + y_bob)], fill=(180, 45, 35, 255), outline=glow_color)
            draw.polygon([(22 - claw_open, 105 + y_bob), (36, 125 + y_bob), (18 - claw_open, 128 + y_bob)], fill=(240, 110, 40, 255))
            # Pneumatic pile driver ram on left arm
            ram_ext = 8 if i == 3 else 0
            draw.rectangle([112, 70 + y_bob, 134, 115 + y_bob + ram_ext], fill=(65, 50, 45, 255), outline=accent_color)
            draw.polygon([(116, 115 + y_bob + ram_ext), (123, 135 + y_bob + ram_ext), (130, 115 + y_bob + ram_ext)], fill=(200, 180, 160, 255))

        elif mech_type == "kage":
            # Cyber Stealth Infiltrator (Matte obsidian, needle railgun)
            # Slender articulated digitigrade legs
            draw.polygon([(52 + x_shift, 144 + y_bob), (44, 112 + y_bob), (58, 112 + y_bob), (64 + x_shift, 144 + y_bob)], fill=(28, 22, 38, 255))
            draw.polygon([(96 - x_shift, 144 + y_bob), (102, 112 + y_bob), (116, 112 + y_bob), (108 - x_shift, 144 + y_bob)], fill=(28, 22, 38, 255))
            # Faceted stealth diamond torso
            draw.polygon([(80, 50 + y_bob), (106, 75 + y_bob), (96, 112 + y_bob), (64, 112 + y_bob), (54, 75 + y_bob)], fill=base_color, outline=accent_color, width=2)
            # Optical sensor cowl
            draw.polygon([(70, 42 + y_bob), (90, 42 + y_bob), (88, 56 + y_bob), (72, 56 + y_bob)], fill=(20, 15, 25, 255))
            draw.ellipse([75, 46 + y_bob, 85, 52 + y_bob], fill=glow_color)
            # Needle beam rail sniper
            draw.rectangle([110, 35 + y_bob, 118, 115 + y_bob], fill=(45, 35, 60, 255), outline=glow_color)
            draw.line([114, 20 + y_bob, 114, 35 + y_bob], fill=glow_color, width=2)
            # Optical shimmer cloak lines on frame 1
            if i == 1:
                draw.line([48, 60, 112, 60], fill=(0, 255, 230, 100), width=1)
                draw.line([54, 85, 106, 85], fill=(0, 255, 230, 100), width=1)

        # Save main frame PNG
        main_png = os.path.join(spr_path, f"{f_uuid}.png")
        im.save(main_png, "PNG")
        
        # Save layer PNG
        layer_dir = os.path.join(layers_path, f_uuid)
        os.makedirs(layer_dir, exist_ok=True)
        layer_png = os.path.join(layer_dir, f"{layer_id}.png")
        im.save(layer_png, "PNG")

    # Build .yy file
    yy_data = {
        "$GMSprite": "v2",
        "%Name": sprite_name,
        "bboxMode": 0,
        "bbox_bottom": 154,
        "bbox_left": 18,
        "bbox_right": 142,
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
            }
            for f_uuid in frame_uuids
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
            "length": 4.0,
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
                                "Key": float(k_idx),
                                "Length": 1.0,
                                "resourceType": "Keyframe<SpriteFrameKeyframe>",
                                "resourceVersion": "2.0",
                                "Stretch": False
                            }
                            for k_idx, f_uuid in enumerate(frame_uuids)
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
            "xorigin": 0,
            "yorigin": 0
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

# Generate all 4 mass production archetype sprites
create_mech_sprite("spr_ms_ballista_idle", (68, 78, 62, 255), (105, 120, 95, 255), (255, 120, 40, 255), "ballista")
create_mech_sprite("spr_ms_zephyr_idle", (38, 70, 115, 255), (85, 145, 220, 255), (0, 240, 255, 255), "zephyr")
create_mech_sprite("spr_ms_gorgon_idle", (135, 55, 40, 255), (185, 80, 50, 255), (255, 160, 40, 255), "gorgon")
create_mech_sprite("spr_ms_kage_idle", (24, 18, 32, 255), (65, 45, 85, 255), (0, 255, 200, 255), "kage")

# Register in MechMakerConcept.yyp
with open(YYP_PATH, "r") as f:
    yyp_content = f.read()

new_sprites = [
    ("spr_ms_ballista_idle", "sprites/spr_ms_ballista_idle/spr_ms_ballista_idle.yy"),
    ("spr_ms_zephyr_idle", "sprites/spr_ms_zephyr_idle/spr_ms_zephyr_idle.yy"),
    ("spr_ms_gorgon_idle", "sprites/spr_ms_gorgon_idle/spr_ms_gorgon_idle.yy"),
    ("spr_ms_kage_idle", "sprites/spr_ms_kage_idle/spr_ms_kage_idle.yy"),
]

for spr_id, spr_path in new_sprites:
    entry = f'{{"id":{{"name":"{spr_id}","path":"{spr_path}",}},}},'
    if spr_id not in yyp_content:
        # Insert into resources list
        marker = '"resources": ['
        idx = yyp_content.find(marker)
        if idx != -1:
            insert_pos = idx + len(marker)
            yyp_content = yyp_content[:insert_pos] + f"\n    {entry}" + yyp_content[insert_pos:]
            print(f"Registered {spr_id} in MechMakerConcept.yyp")

with open(YYP_PATH, "w") as f:
    f.write(yyp_content)

print("All sprites successfully created and registered!")
