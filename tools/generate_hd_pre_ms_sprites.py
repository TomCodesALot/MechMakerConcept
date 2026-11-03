import shutil
import os
import json
import uuid
import math
from PIL import Image, ImageDraw

SPRITES_DIR = "sprites"
YYP_PATH = "MechMakerConcept.yyp"

def build_sprite(sprite_name, draw_func, num_frames=4, speed=6.0):
    spr_path = os.path.join(SPRITES_DIR, sprite_name)
    layers_path = os.path.join(spr_path, "layers")
    if os.path.exists(spr_path):
        for f in os.listdir(spr_path):
            if f.endswith(".png"):
                os.remove(os.path.join(spr_path, f))
        if os.path.exists(layers_path):
            shutil.rmtree(layers_path)
    os.makedirs(spr_path, exist_ok=True)
    os.makedirs(layers_path, exist_ok=True)

    layer_id = str(uuid.uuid4())
    frame_uuids = [str(uuid.uuid4()) for _ in range(num_frames)]

    for i, f_uuid in enumerate(frame_uuids):
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw_func(draw, i)

        main_png = os.path.join(spr_path, f"{f_uuid}.png")
        im.save(main_png, "PNG")
        layer_dir = os.path.join(layers_path, f_uuid)
        os.makedirs(layer_dir, exist_ok=True)
        layer_png = os.path.join(layer_dir, f"{layer_id}.png")
        im.save(layer_png, "PNG")
        if i == 0:
            preview_png = os.path.join(spr_path, f"{sprite_name}.png")
            im.save(preview_png, "PNG")

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

# =============================================================================
# DETAILED PIXEL-ART INFANTRY DRAWING PRIMITIVES
# =============================================================================

def draw_single_soldier(draw, sx, sy, faction="terran", role="rifle", pose="idle", frame=0, is_back=False):
    """
    Renders an individual high-detail retro pixel-art soldier.
    sx, sy: foot ground anchor
    role: 'rifle', 'bazooka', 'lmg', 'officer'
    pose: 'idle', 'fire', 'recoil', 'blown_away', 'retreat'
    """
    # Palette lookup per faction
    if faction == "terran":
        c_armor = (65, 80, 55, 255)
        c_armor_dark = (35, 45, 30, 255)
        c_cloth = (85, 95, 75, 255)
        c_cloth_dark = (48, 55, 42, 255)
        c_skin = (225, 175, 135, 255)
        c_visor = (245, 195, 40, 255)
        c_boots = (30, 30, 28, 255)
        c_gun = (40, 42, 45, 255)
        c_gun_metal = (85, 90, 95, 255)
    elif faction == "colony":
        c_armor = (220, 235, 248, 255)
        c_armor_dark = (45, 75, 115, 255)
        c_cloth = (70, 110, 160, 255)
        c_cloth_dark = (25, 45, 75, 255)
        c_skin = (235, 185, 145, 255)
        c_visor = (245, 210, 60, 255)
        c_boots = (45, 60, 80, 255)
        c_gun = (50, 60, 75, 255)
        c_gun_metal = (120, 160, 210, 255)
    elif faction == "syndicate":
        c_armor = (95, 60, 45, 255)
        c_armor_dark = (45, 25, 18, 255)
        c_cloth = (110, 85, 65, 255)
        c_cloth_dark = (55, 40, 30, 255)
        c_skin = (210, 160, 125, 255)
        c_visor = (220, 90, 40, 255)
        c_boots = (38, 30, 25, 255)
        c_gun = (35, 30, 30, 255)
        c_gun_metal = (140, 110, 90, 255)
    else: # zaibatsu
        c_armor = (28, 22, 35, 255)
        c_armor_dark = (15, 10, 20, 255)
        c_cloth = (45, 38, 55, 255)
        c_cloth_dark = (22, 18, 28, 255)
        c_skin = (170, 175, 190, 255)
        c_visor = (220, 40, 240, 255)
        c_boots = (20, 18, 24, 255)
        c_gun = (25, 25, 30, 255)
        c_gun_metal = (160, 120, 200, 255)

    y_bob = -1 if (frame % 2 == 1 and pose == "idle") else 0
    bx = sx
    by = sy + y_bob

    # ADVANCE WARS STYLE DEFEAT POSE (BLOWN AWAY / TUMBLING)
    if pose == "blown_away":
        # Tumbling in the air / flying backward
        air_y = by - 14 - (frame * 5)
        rot_x = bx + (frame * 6)
        # Small ground blast ring
        draw.ellipse([sx - 10, sy - 2, sx + 10, sy + 6], fill=(0, 0, 0, 50))
        # Puffed smoke
        draw.ellipse([sx - 8, sy - 8, sx + 8, sy + 4], fill=(200, 195, 190, 160))

        # Body tilted back in mid air (45 to 90 degrees)
        # Legs flailing upward
        draw.line([(rot_x - 4, air_y + 4), (rot_x - 10, air_y - 4)], fill=c_cloth, width=3)
        draw.line([(rot_x + 2, air_y + 4), (rot_x + 8, air_y - 2)], fill=c_cloth, width=3)
        draw.rectangle([rot_x - 12, air_y - 6, rot_x - 8, air_y - 2], fill=c_boots)
        draw.rectangle([rot_x + 6, air_y - 4, rot_x + 10, air_y], fill=c_boots)

        # Torso
        draw.rectangle([rot_x - 5, air_y + 2, rot_x + 5, air_y + 12], fill=c_armor, outline=c_armor_dark)

        # Head / Face
        draw.ellipse([rot_x - 4, air_y + 12, rot_x + 4, air_y + 20], fill=c_skin)
        draw.ellipse([rot_x - 2, air_y + 14, rot_x + 2, air_y + 17], fill=(255, 255, 255, 255)) # wide scared eyes

        # Arms flailing outward
        draw.line([(rot_x - 4, air_y + 6), (rot_x - 12, air_y + 12)], fill=c_cloth, width=2)
        draw.line([(rot_x + 4, air_y + 6), (rot_x + 12, air_y + 4)], fill=c_cloth, width=2)

        # Helmet flying off into the air!
        helm_x = rot_x - 6 - (frame * 4)
        helm_y = air_y - 8 - (frame * 4)
        draw.ellipse([helm_x - 5, helm_y - 5, helm_x + 5, helm_y + 5], fill=c_armor, outline=c_armor_dark)
        draw.line([helm_x - 3, helm_y, helm_x + 3, helm_y], fill=c_visor, width=2)

        # Dropped weapon spinning downward
        gun_x = bx - 10 + (frame * 2)
        gun_y = sy - 4 + (frame * 2)
        draw.line([(gun_x - 6, gun_y + 2), (gun_x + 6, gun_y - 4)], fill=c_gun, width=2)
        return

    # ADVANCE WARS STYLE SCRAMBLING RETREAT
    if pose == "retreat":
        run_off = frame * 7
        rx = bx - run_off
        ry = by
        # Shadow
        # draw.ellipse([rx - 8, ry - 2, rx + 8, ry + 4], fill=(0, 0, 0, 70)) # Scrubbed for transparent ground
        # Running legs
        leg_stride = 6 if (frame % 2 == 1) else -6
        draw.line([(rx - 2, ry - 8), (rx - 6 + leg_stride, ry)], fill=c_cloth, width=3)
        draw.line([(rx + 2, ry - 8), (rx + 6 - leg_stride, ry)], fill=c_cloth, width=3)
        draw.rectangle([rx - 8 + leg_stride, ry - 2, rx - 4 + leg_stride, ry + 2], fill=c_boots)
        draw.rectangle([rx + 4 - leg_stride, ry - 2, rx + 8 - leg_stride, ry + 2], fill=c_boots)
        # Hunched sprinting torso
        draw.polygon([(rx - 5, ry - 8), (rx + 4, ry - 8), (rx + 2, ry - 17), (rx - 7, ry - 17)], fill=c_armor, outline=c_armor_dark)
        # Head ducked low
        draw.ellipse([rx - 8, ry - 23, rx, ry - 15], fill=c_armor, outline=c_armor_dark)
        # Surrender white flag or hands waving back
        if frame % 2 == 0:
            draw.line([(rx + 2, ry - 14), (rx + 10, ry - 22)], fill=(240, 240, 240, 255), width=2)
            draw.polygon([(rx + 10, ry - 26), (rx + 18, ry - 24), (rx + 10, ry - 20)], fill=(255, 255, 255, 255))
        return

    # NORMAL / COMBAT POSE (IDLE, FIRE, RECOIL)
    # Ground shadow
    # draw.ellipse([bx - 9, by - 3, bx + 9, by + 4], fill=(0, 0, 0, 75)) # Scrubbed for transparent ground

    recoil_off = 0
    if pose == "fire" and frame == 1:
        recoil_off = -2

    # Legs & Boots
    # Staggered tactical firing stance
    draw.polygon([(bx - 4 + recoil_off, by - 12), (bx - 7 + recoil_off, by), (bx - 3 + recoil_off, by), (bx - 1 + recoil_off, by - 12)], fill=c_cloth, outline=c_cloth_dark)
    draw.polygon([(bx + 1 + recoil_off, by - 12), (bx + 4 + recoil_off, by - 2), (bx + 8 + recoil_off, by - 2), (bx + 5 + recoil_off, by - 12)], fill=c_cloth, outline=c_cloth_dark)
    # Knee pads
    draw.rectangle([bx - 6 + recoil_off, by - 7, bx - 3 + recoil_off, by - 4], fill=c_armor_dark)
    draw.rectangle([bx + 4 + recoil_off, by - 8, bx + 7 + recoil_off, by - 5], fill=c_armor_dark)
    # Combat boots
    draw.rectangle([bx - 8 + recoil_off, by - 3, bx - 2 + recoil_off, by + 1], fill=c_boots)
    draw.rectangle([bx + 4 + recoil_off, by - 4, bx + 9 + recoil_off, by], fill=c_boots)

    # Torso (Tactical Plate Carrier & Pouches)
    draw.rectangle([bx - 5 + recoil_off, by - 22, bx + 5 + recoil_off, by - 12], fill=c_armor, outline=c_armor_dark)
    # Magazine pouches
    draw.rectangle([bx - 4 + recoil_off, by - 15, bx - 1 + recoil_off, by - 12], fill=c_cloth_dark)
    draw.rectangle([bx + 1 + recoil_off, by - 15, bx + 4 + recoil_off, by - 12], fill=c_cloth_dark)
    # Tactical chest webbing
    draw.line([(bx - 4 + recoil_off, by - 19), (bx + 4 + recoil_off, by - 19)], fill=c_cloth_dark, width=1)

    # Head (Ballistic Helmet & Visor / Goggles)
    if not is_back:
        # Ballistic helmet dome
        draw.ellipse([bx - 5 + recoil_off, by - 30, bx + 5 + recoil_off, by - 21], fill=c_armor, outline=c_armor_dark)
        # Face / Chin
        draw.rectangle([bx - 3 + recoil_off, by - 24, bx + 3 + recoil_off, by - 21], fill=c_skin)
        # Visor / Goggles with bright glint
        draw.rectangle([bx - 4 + recoil_off, by - 26, bx + 4 + recoil_off, by - 23], fill=c_visor)
        draw.point((bx - 2 + recoil_off, by - 25), fill=(255, 255, 255, 255))
    else:
        # Back of helmet and radio harness
        draw.ellipse([bx - 5 + recoil_off, by - 30, bx + 5 + recoil_off, by - 21], fill=c_armor, outline=c_armor_dark)
        draw.rectangle([bx - 4 + recoil_off, by - 20, bx + 4 + recoil_off, by - 14], fill=c_cloth_dark)
        # Radio backpack whip antenna
        draw.line([(bx + 3 + recoil_off, by - 20), (bx + 5 + recoil_off, by - 35)], fill=(30, 30, 30, 255), width=1)

    # WEAPONS & ARMS HANDLING
    if role == "bazooka":
        # Heavy Shoulder-Mounted Anti-Tank Rocket Launcher (Bazooka / ATGM)
        bz_x = bx + recoil_off
        bz_y = by - 24

        # Massive green/steel launch tube resting over right shoulder
        # Front tube
        draw.polygon([(bz_x - 8, bz_y - 2), (bz_x + 18, bz_y - 2), (bz_x + 18, bz_y + 4), (bz_x - 8, bz_y + 4)], fill=c_armor_dark, outline=c_gun)
        # Wide front muzzle lip
        draw.rectangle([bz_x + 17, bz_y - 3, bz_x + 20, bz_y + 5], fill=c_gun_metal)
        # Conical rear exhaust bell
        draw.polygon([(bz_x - 8, bz_y), (bz_x - 14, bz_y - 4), (bz_x - 14, bz_y + 6), (bz_x - 8, bz_y + 4)], fill=c_gun)
        # Optical viewfinder scope on top
        draw.rectangle([bz_x + 2, bz_y - 6, bz_x + 8, bz_y - 2], fill=c_gun, outline=c_visor)

        # Arms holding bazooka front grip and shoulder rest
        draw.line([(bx - 2 + recoil_off, by - 19), (bz_x + 6, bz_y + 4)], fill=c_cloth, width=2)
        draw.line([(bx + 2 + recoil_off, by - 19), (bz_x + 12, bz_y + 4)], fill=c_cloth, width=2)

        # FIRING FX: MASSIVE BACKBLAST & ROCKET LAUNCH!
        if pose == "fire" and frame == 1:
            # Fiery rear backblast exhaust plume!
            draw.polygon([(bz_x - 14, bz_y + 1), (bz_x - 28, bz_y - 7), (bz_x - 34, bz_y + 1), (bz_x - 28, bz_y + 9)], fill=(255, 120, 20, 240))
            draw.polygon([(bz_x - 14, bz_y + 1), (bz_x - 22, bz_y - 4), (bz_x - 26, bz_y + 1), (bz_x - 22, bz_y + 6)], fill=(255, 230, 80, 255))
            # Smoke ring behind launcher
            draw.ellipse([bz_x - 36, bz_y - 5, bz_x - 24, bz_y + 7], outline=(200, 200, 200, 200), width=2)

            # High-velocity anti-tank rocket shooting forward!
            rkt_x = bz_x + 26
            rkt_y = bz_y + 1
            draw.polygon([(rkt_x + 12, rkt_y), (rkt_x, rkt_y - 3), (rkt_x, rkt_y + 3)], fill=(220, 60, 40, 255))
            draw.rectangle([rkt_x - 4, rkt_y - 2, rkt_x, rkt_y + 2], fill=c_gun_metal)
            # Rocket motor flame
            draw.polygon([(rkt_x - 4, rkt_y), (rkt_x - 12, rkt_y - 3), (rkt_x - 12, rkt_y + 3)], fill=(255, 200, 50, 255))
        elif pose == "fire" and frame == 2:
            # Lingering white/grey smoke plume
            draw.ellipse([bz_x - 30, bz_y - 6, bz_x - 14, bz_y + 8], fill=(210, 210, 210, 160))
            draw.ellipse([bz_x + 20, bz_y - 4, bz_x + 36, bz_y + 6], fill=(230, 230, 230, 140))

    elif role == "lmg":
        # Emplaced / Shoulder Heavy Machine Gun
        lmg_x = bx + recoil_off
        lmg_y = by - 19
        # Heavy receiver & long barrel
        draw.line([(lmg_x - 4, lmg_y), (lmg_x + 18, lmg_y)], fill=c_gun, width=3)
        draw.rectangle([lmg_x + 16, lmg_y - 2, lmg_x + 20, lmg_y + 2], fill=c_gun_metal)
        # Circular drum magazine
        draw.ellipse([lmg_x + 2, lmg_y + 1, lmg_x + 8, lmg_y + 7], fill=c_gun_metal)
        # Arms holding LMG
        draw.line([(bx - 3 + recoil_off, by - 18), (lmg_x + 4, lmg_y + 2)], fill=c_cloth, width=2)
        draw.line([(bx + 3 + recoil_off, by - 18), (lmg_x + 12, lmg_y + 2)], fill=c_cloth, width=2)

        if pose == "fire" and (frame == 1 or frame == 2):
            # Rapid fire muzzle flash starburst
            fx_x = lmg_x + 22
            fx_y = lmg_y
            draw.polygon([(fx_x, fx_y), (fx_x + 8, fx_y - 4), (fx_x + 6, fx_y), (fx_x + 12, fx_y), (fx_x + 6, fx_y + 2), (fx_x + 8, fx_y + 6)], fill=(255, 220, 60, 255))
            # Flying brass casings
            draw.rectangle([lmg_x + 6, lmg_y - 6, lmg_x + 8, lmg_y - 4], fill=(245, 200, 30, 255))
            draw.rectangle([lmg_x + 10, lmg_y - 9, lmg_x + 12, lmg_y - 7], fill=(245, 200, 30, 255))

    else: # rifle / officer
        # Tactical Assault Carbine with Banana Mag & Stock
        rf_x = bx + recoil_off
        rf_y = by - 18
        # Stock resting against shoulder
        draw.polygon([(rf_x - 6, rf_y + 1), (rf_x - 1, rf_y), (rf_x - 1, rf_y + 3), (rf_x - 6, rf_y + 4)], fill=c_cloth_dark)
        # Receiver & barrel
        draw.line([(rf_x - 1, rf_y + 1), (rf_x + 15, rf_y + 1)], fill=c_gun, width=2)
        draw.point((rf_x + 14, rf_y), fill=c_gun_metal) # front sight
        # Curved banana magazine
        draw.polygon([(rf_x + 4, rf_y + 2), (rf_x + 6, rf_y + 8), (rf_x + 4, rf_y + 9), (rf_x + 2, rf_y + 2)], fill=c_gun_metal)
        # Arms
        draw.line([(bx - 3 + recoil_off, by - 18), (rf_x + 2, rf_y + 3)], fill=c_cloth, width=2)
        draw.line([(bx + 2 + recoil_off, by - 18), (rf_x + 10, rf_y + 2)], fill=c_cloth, width=2)

        if pose == "fire" and frame == 1:
            # Muzzle flash cone
            fx_x = rf_x + 16
            draw.polygon([(fx_x, rf_y + 1), (fx_x + 7, rf_y - 3), (fx_x + 5, rf_y + 1), (fx_x + 9, rf_y + 1), (fx_x + 5, rf_y + 2), (fx_x + 7, rf_y + 5)], fill=(255, 220, 50, 255))
            # Ejected casing
            draw.rectangle([rf_x + 4, rf_y - 5, rf_x + 6, rf_y - 3], fill=(245, 200, 30, 255))

# =============================================================================
# SQUAD DRAWING PROCEDURES (IDLE, BACK, FIRE, DEFEAT)
# =============================================================================

def draw_infantry_squad(draw, frame, faction="terran", mode="idle"):
    # Ground shadow for the squad
    # draw.ellipse([30, 138, 130, 154], fill=(0, 0, 0, 80)) # Scrubbed for transparent ground

    if mode == "defeat":
        # ADVANCE WARS STYLE DEFEAT SEQUENCE
        # Frame 0: Blast shock! Dropping guns, flying back
        # Frame 1: Airborne tumbling, helmets popping off, comic arcs
        # Frame 2: Mid-air tumbling and crawling retreat
        # Frame 3: Dust cloud puff, abandoned gear, running off screen!
        if frame == 0:
            draw_single_soldier(draw, 55, 126, faction, "bazooka", "blown_away", 0)
            draw_single_soldier(draw, 78, 130, faction, "officer", "blown_away", 0)
            draw_single_soldier(draw, 102, 124, faction, "rifle", "blown_away", 0)
        elif frame == 1:
            draw_single_soldier(draw, 55, 126, faction, "bazooka", "blown_away", 1)
            draw_single_soldier(draw, 78, 130, faction, "officer", "blown_away", 1)
            draw_single_soldier(draw, 102, 124, faction, "rifle", "blown_away", 1)
        elif frame == 2:
            draw_single_soldier(draw, 55, 126, faction, "bazooka", "blown_away", 2)
            draw_single_soldier(draw, 80, 134, faction, "officer", "retreat", 1)
            draw_single_soldier(draw, 105, 128, faction, "rifle", "retreat", 1)
        else: # frame 3
            # Comic Advance Wars Dust Puffs ("*POOF*")
            for dx, dy in [(50, 125), (75, 132), (100, 122)]:
                draw.ellipse([dx - 12, dy - 10, dx + 12, dy + 6], fill=(225, 220, 210, 180))
                draw.ellipse([dx - 8, dy - 16, dx + 8, dy - 2], fill=(240, 235, 225, 210))
            # Abandoned helmet and bazooka in dirt
            draw.ellipse([58, 132, 68, 140], fill=(60, 75, 55, 255), outline=(30, 40, 25, 255))
            draw.line([(70, 136), (92, 132)], fill=(40, 42, 45, 255), width=3)
            # Surrendering retreat soldier diving away
            draw_single_soldier(draw, 40, 138, faction, "officer", "retreat", 3)
        return

    # FORTIFICATIONS ON TILE (Sandbags / Scrap Barricades)
    if faction == "syndicate":
        # Rusted corrugated sheet barricade with hazard stripes
        draw.polygon([(42, 144), (118, 144), (112, 133), (48, 133)], fill=(90, 55, 40, 255), outline=(40, 25, 18, 255))
        for hx in [52, 68, 84, 100]:
            draw.line([(hx, 142), (hx + 6, 134)], fill=(230, 140, 30, 255), width=2)
    elif faction == "zaibatsu":
        # Carbon hex deployable barricade with glowing magenta trim
        draw.polygon([(44, 143), (116, 143), (110, 134), (50, 134)], fill=(25, 22, 32, 255), outline=(80, 40, 100, 255))
        draw.line([(52, 138), (108, 138)], fill=(220, 40, 240, 255), width=2)
    else:
        # Terran / Colony Sandbag revetment
        draw.polygon([(44, 144), (116, 144), (110, 135), (50, 135)], fill=(130, 120, 90, 255), outline=(65, 60, 45, 255))
        draw.polygon([(48, 135), (112, 135), (106, 127), (54, 127)], fill=(145, 135, 100, 255), outline=(65, 60, 45, 255))

    is_back = (mode == "back_idle")
    p_state = "fire" if mode == "fire" else "idle"

    # 4 SOLDIERS IN TACTICAL FORMATION
    # 1. Left: Heavy Bazooka Gunner
    draw_single_soldier(draw, 58, 127, faction, "bazooka", p_state, frame, is_back)
    # 2. Center: Squad Leader / Officer
    draw_single_soldier(draw, 78, 130, faction, "officer", p_state, frame, is_back)
    # 3. Right: Support Machine Gunner
    draw_single_soldier(draw, 98, 125, faction, "lmg", p_state, frame, is_back)
    # 4. Rear: Radio Operator / Marksman
    draw_single_soldier(draw, 76, 114, faction, "rifle", p_state, frame, is_back)

print("Infantry procedures drafted.")

# =============================================================================
# DETAILED VEHICLE DRAWING PROCEDURES (TANKS, SKIFFS, ROVERS)
# =============================================================================

def draw_terran_tank(draw, frame, mode="idle"):
    is_back = (mode == "back_idle")
    is_fire = (mode == "fire")

    # Suspension idle rumble & recoil squat
    y_bob = -1 if (frame % 2 == 1 and not is_fire) else 0
    recoil_x = -5 if (is_fire and frame == 1) else 0
    recoil_pitch = 2 if (is_fire and frame == 1) else 0

    # Ground shadow
    # draw.ellipse([20, 140, 140, 154], fill=(0, 0, 0, 95)) # Scrubbed for transparent ground

    # Colors
    c_hull = (56, 68, 52, 255)
    c_hull_dark = (32, 40, 30, 255)
    c_hull_light = (85, 102, 78, 255)
    c_tread = (35, 38, 32, 255)
    c_tread_metal = (60, 65, 55, 255)
    c_steel = (45, 48, 50, 255)

    # 1. CATERPILLAR TRACKS WITH ANIMATED CONVEYOR TREAD LINKS
    t_shift = (frame * 3) % 12
    # Left and Right Tread Pods
    for tx1, tx2, ty in [(24 + recoil_x, 62 + recoil_x, 122 + y_bob + recoil_pitch), (98 + recoil_x, 136 + recoil_x, 122 + y_bob + recoil_pitch)]:
        # Tread outer casing
        draw.polygon([(tx1, ty + 24), (tx2, ty + 24), (tx2 + 4, ty), (tx1 - 4, ty)], fill=c_tread, outline=(20, 22, 18, 255), width=2)
        # Road wheels (3 spinning wheels with cross spokes)
        for wx in range(tx1 + 6, tx2 - 4, 12):
            draw.ellipse([wx, ty + 10, wx + 10, ty + 20], fill=(48, 52, 45, 255), outline=(22, 25, 20, 255))
            # Wheel axle / spoke rotation
            ang = (frame * 45) * math.pi / 180.0
            spk_x = int(5 * math.cos(ang))
            spk_y = int(5 * math.sin(ang))
            draw.line([(wx + 5 - spk_x, ty + 15 - spk_y), (wx + 5 + spk_x, ty + 15 + spk_y)], fill=c_tread_metal, width=1)
        # Moving Tread Links (horizontal teeth shifting every frame!)
        for lx in range(tx1 - 2, tx2 + 4, 6):
            mov_lx = lx + t_shift
            if tx1 <= mov_lx <= tx2:
                draw.line([(mov_lx, ty + 23), (mov_lx + 2, ty + 25)], fill=c_tread_metal, width=2)
                draw.line([(mov_lx, ty), (mov_lx + 2, ty - 2)], fill=c_tread_metal, width=1)

    # 2. MAIN ARMORED HULL & SKIRTING
    draw.polygon([(46 + recoil_x, 142 + y_bob + recoil_pitch), (114 + recoil_x, 142 + y_bob + recoil_pitch),
                  (122 + recoil_x, 108 + y_bob + recoil_pitch), (38 + recoil_x, 108 + y_bob + recoil_pitch)],
                 fill=c_hull, outline=c_hull_dark, width=2)
    # Armor skirting side plate highlights
    draw.line([(48 + recoil_x, 126 + y_bob + recoil_pitch), (112 + recoil_x, 126 + y_bob + recoil_pitch)], fill=c_hull_light, width=2)
    # Bolt rivets on armor skirts
    for rx in range(54 + recoil_x, 108 + recoil_x, 10):
        draw.point((rx, 128 + y_bob + recoil_pitch), fill=(20, 22, 18, 255))

    # 3. TURRET & WEAPONS
    turret_x = 80 + recoil_x
    turret_y = 104 + y_bob + recoil_pitch

    if not is_back:
        # Cast steel heavy turret
        draw.polygon([(turret_x - 26, turret_y + 8), (turret_x + 26, turret_y + 8),
                      (turret_x + 20, turret_y - 18), (turret_x - 20, turret_y - 18)],
                     fill=c_hull, outline=c_hull_dark, width=2)
        # Commander cupola & vision periscopes
        draw.ellipse([turret_x - 8, turret_y - 24, turret_x + 8, turret_y - 14], fill=c_hull_dark)
        draw.rectangle([turret_x - 6, turret_y - 20, turret_x + 6, turret_y - 18], fill=(120, 220, 255, 255)) # periscope glass

        # Twin 120mm rifled cannon barrels
        b_kick = -6 if (is_fire and frame == 1) else 0
        b_len = 34 + b_kick
        # Left barrel
        draw.rectangle([turret_x - 12, turret_y - 6, turret_x - 6, turret_y + b_len], fill=c_steel, outline=(20, 22, 25, 255))
        draw.rectangle([turret_x - 14, turret_y + b_len - 2, turret_x - 4, turret_y + b_len + 4], fill=c_hull_light) # muzzle brake
        # Right barrel
        draw.rectangle([turret_x + 6, turret_y - 6, turret_x + 12, turret_y + b_len], fill=c_steel, outline=(20, 22, 25, 255))
        draw.rectangle([turret_x + 4, turret_y + b_len - 2, turret_x + 14, turret_y + b_len + 4], fill=c_hull_light) # muzzle brake

        # CANNON BLAST ANIMATION!
        if is_fire and frame == 1:
            # Massive dual muzzle blast cones!
            for mx in [turret_x - 9, turret_y + 9]:
                my = turret_y + b_len + 4
                draw.polygon([(mx - 14, my + 6), (mx + 14, my + 6), (mx + 22, my + 30), (mx, my + 38), (mx - 22, my + 30)], fill=(255, 140, 20, 240))
                draw.polygon([(mx - 8, my + 4), (mx + 8, my + 4), (mx + 12, my + 20), (mx, my + 26), (mx - 12, my + 20)], fill=(255, 240, 80, 255))
                draw.ellipse([mx - 18, my + 14, mx + 18, my + 32], outline=(255, 255, 255, 220), width=2)
            # Ejected 120mm brass artillery casing
            draw.rectangle([turret_x - 30, turret_y - 10, turret_x - 22, turret_y - 4], fill=(245, 205, 40, 255))
        elif is_fire and frame == 2:
            # Dissipating white gunsmoke
            for mx in [turret_x - 9, turret_y + 9]:
                my = turret_y + b_len + 15
                draw.ellipse([mx - 16, my - 10, mx + 16, my + 10], fill=(220, 220, 220, 160))
        elif not is_fire:
            # Twin rear exhaust smoke puffs chugging!
            smk_y = turret_y - 28 - (frame * 4)
            smk_r = 4 + (frame * 2)
            draw.ellipse([turret_x - 18 - smk_r, smk_y - smk_r, turret_x - 18 + smk_r, smk_y + smk_r], fill=(160, 155, 150, 140 - frame*30))
            draw.ellipse([turret_x + 18 - smk_r, smk_y - smk_r, turret_x + 18 + smk_r, smk_y + smk_r], fill=(160, 155, 150, 140 - frame*30))
    else:
        # Turret from behind with stowage basket & engine deck
        draw.polygon([(turret_x - 24, turret_y + 6), (turret_x + 24, turret_y + 6),
                      (turret_x + 20, turret_y - 16), (turret_x - 20, turret_y - 16)],
                     fill=c_hull, outline=c_hull_dark, width=2)
        # Stowage rack mesh
        draw.rectangle([turret_x - 16, turret_y - 12, turret_x + 16, turret_y - 2], outline=(30, 32, 28, 255))
        draw.rectangle([turret_x - 20, turret_y + 12, turret_x - 10, turret_y + 24], fill=(120, 90, 40, 255)) # fuel drum
        draw.rectangle([turret_x + 10, turret_y + 12, turret_x + 20, turret_y + 24], fill=(120, 90, 40, 255)) # fuel drum
        # Rear radio antenna swaying
        ant_sway = 2 if (frame % 2 == 1) else -2
        draw.line([(turret_x + 14, turret_y - 12), (turret_x + 16 + ant_sway, turret_y - 36)], fill=(30, 30, 30, 255), width=1)

def draw_colony_stiletto(draw, frame, mode="idle"):
    is_back = (mode == "back_idle")
    is_fire = (mode == "fire")
    y_bob = -2 if (frame % 2 == 1) else 1

    # Concentric ground dust ripples from ion repulsors
    dust_r = 14 + (frame * 4)
    draw.ellipse([80 - dust_r, 146 - int(dust_r*0.35), 80 + dust_r, 146 + int(dust_r*0.35)], outline=(0, 220, 255, 120 - frame*25), width=2)
    # draw.ellipse([26, 140, 134, 152], fill=(0, 0, 0, 80)) # Scrubbed for transparent ground

    # Catamaran hover hull
    c_white = (225, 238, 248, 255)
    c_blue = (45, 85, 135, 255)
    c_cyan = (0, 230, 255, 255)

    # Hover skirt
    draw.polygon([(36, 134 + y_bob), (124, 134 + y_bob), (116, 116 + y_bob), (44, 116 + y_bob)], fill=c_blue, outline=(25, 50, 80, 255), width=2)
    # Sleek aerodynamic upper deck
    draw.polygon([(46, 120 + y_bob), (114, 120 + y_bob), (96, 92 + y_bob), (64, 92 + y_bob)], fill=c_white, outline=c_blue, width=2)
    # Cyan repulsor glow strip underneath
    draw.line([(40, 133 + y_bob), (120, 133 + y_bob)], fill=c_cyan, width=2)

    # Twin linear railgun barrels
    draw.line([(58, 112 + y_bob), (58, 146 + y_bob)], fill=(50, 60, 75, 255), width=3)
    draw.line([(102, 112 + y_bob), (102, 146 + y_bob)], fill=(50, 60, 75, 255), width=3)

    if is_fire and frame == 1:
        # Electric cyan railgun discharge!
        for rx in [58, 102]:
            draw.line([(rx, 146 + y_bob), (rx, 170 + y_bob)], fill=c_cyan, width=3)
            draw.polygon([(rx - 6, 148), (rx + 6, 148), (rx, 162)], fill=(255, 255, 255, 255))
    if is_back:
        # Rear ion thruster ports
        draw.ellipse([64, 98 + y_bob, 74, 106 + y_bob], fill=c_cyan)
        draw.ellipse([86, 98 + y_bob, 96, 106 + y_bob], fill=c_cyan)

def draw_syndicate_technical(draw, frame, mode="idle"):
    is_back = (mode == "back_idle")
    is_fire = (mode == "fire")
    y_bob = -1 if (frame % 2 == 1) else 0

    # draw.ellipse([24, 140, 136, 154], fill=(0, 0, 0, 85)) # Scrubbed for transparent ground

    c_rust = (110, 65, 45, 255)
    c_metal = (55, 50, 48, 255)
    c_rubber = (28, 25, 24, 255)

    # 6 Rotating Mud-Tread Tires
    w_rot = (frame * 45) * math.pi / 180.0
    for wx, wy in [(34, 140), (52, 142), (108, 142), (126, 140)]:
        draw.ellipse([wx - 7, wy - 7 + y_bob, wx + 7, wy + 7 + y_bob], fill=c_rubber, outline=(15, 12, 10, 255), width=2)
        # Spokes
        spk_x = int(5 * math.cos(w_rot))
        spk_y = int(5 * math.sin(w_rot))
        draw.line([(wx - spk_x, wy - spk_y + y_bob), (wx + spk_x, wy + spk_y + y_bob)], fill=(180, 175, 165, 255), width=1)

    # Rugged truck chassis & flatbed
    draw.polygon([(36, 136 + y_bob), (124, 136 + y_bob), (118, 116 + y_bob), (42, 116 + y_bob)], fill=c_rust, outline=(40, 22, 15, 255), width=2)
    # Hazard stripes on bumper
    for hx in range(46, 114, 12):
        draw.line([(hx, 135 + y_bob), (hx + 6, 126 + y_bob)], fill=(240, 150, 30, 255), width=2)

    # Welded tubular roll cage & pintle gunner
    draw.line([(48, 116 + y_bob), (54, 96 + y_bob), (106, 96 + y_bob), (112, 116 + y_bob)], fill=c_metal, width=3)
    # Pintle 50mm flak gun & gunner silhouette
    draw.rectangle([76, 92 + y_bob, 84, 104 + y_bob], fill=(45, 35, 28, 255))
    # Gun barrel
    draw.line([(80, 96 + y_bob), (80, 126 + y_bob)], fill=(30, 30, 30, 255), width=4)

    if is_fire and (frame == 1 or frame == 2):
        # Muzzle blast starburst from 50mm flak gun
        draw.polygon([(72, 126 + y_bob), (88, 126 + y_bob), (80, 144 + y_bob)], fill=(255, 160, 30, 255))
        draw.polygon([(76, 126 + y_bob), (84, 126 + y_bob), (80, 136 + y_bob)], fill=(255, 240, 90, 255))

def draw_zaibatsu_kurogane(draw, frame, mode="idle"):
    is_back = (mode == "back_idle")
    is_fire = (mode == "fire")
    y_bob = -1 if (frame % 2 == 1) else 0

    # draw.ellipse([26, 140, 134, 154], fill=(0, 0, 0, 90)) # Scrubbed for transparent ground

    c_carbon = (24, 20, 30, 255)
    c_edge = (60, 50, 75, 255)
    c_mag = (220, 40, 240, 255)

    # Low-profile faceted stealth hull
    draw.polygon([(34, 142 + y_bob), (126, 142 + y_bob), (112, 112 + y_bob), (48, 112 + y_bob)], fill=c_carbon, outline=c_edge, width=2)
    draw.polygon([(52, 114 + y_bob), (108, 114 + y_bob), (94, 96 + y_bob), (66, 96 + y_bob)], fill=c_carbon, outline=c_edge, width=2)

    # Pulsing purple optical eye scanner (sweeps horizontally!)
    eye_x = 72 + (frame * 4)
    draw.rectangle([68, 102 + y_bob, 92, 105 + y_bob], fill=(40, 15, 45, 255))
    draw.rectangle([eye_x - 3, 102 + y_bob, eye_x + 3, 105 + y_bob], fill=c_mag)

    # 75mm Hypersonic Railgun
    draw.line([(80, 98 + y_bob), (80, 138 + y_bob)], fill=(40, 35, 45, 255), width=4)
    # Accelerator coils
    for cy in [106, 116, 126]:
        draw.line([(77, cy + y_bob), (83, cy + y_bob)], fill=c_mag if is_fire else c_edge, width=2)

    if is_fire and frame == 1:
        draw.polygon([(74, 138 + y_bob), (86, 138 + y_bob), (80, 160 + y_bob)], fill=c_mag)
        draw.line([(80, 138 + y_bob), (80, 170 + y_bob)], fill=(255, 255, 255, 255), width=2)

# =============================================================================
# HELICOPTER / VTOL TILT-ROTOR & COMBAT AIRCRAFT DRAWING PROCEDURES
# =============================================================================

def draw_colony_gunship(draw, frame, mode="idle"):
    is_back = (mode == "back_idle")
    is_fire = (mode == "fire")
    # Aerodynamic hovering bob
    hover_bobs = [-2, 0, 1, -1]
    y_bob = hover_bobs[frame % 4]

    # Ground Shadow with expanding downwash rotor wind rings!
    # draw.ellipse([28, 140, 132, 154], fill=(0, 0, 0, 75)) # Scrubbed for transparent ground
    d_ring = 18 + (frame * 6)
    draw.ellipse([80 - d_ring, 147 - int(d_ring * 0.35), 80 + d_ring, 147 + int(d_ring * 0.35)], outline=(0, 220, 255, 110 - frame*25), width=2)

    # Elevated body
    by = 100 + y_bob

    c_fuselage = (220, 235, 248, 255)
    c_blue = (40, 80, 130, 255)
    c_glass = (100, 220, 255, 220)
    c_blade = (40, 45, 50, 240)
    c_blur = (180, 225, 255, 90)

    # Fuselage
    draw.polygon([(62, by + 28), (98, by + 28), (106, by - 6), (54, by - 6)], fill=c_fuselage, outline=c_blue, width=2)
    # Cockpit bubble canopy
    draw.ellipse([68, by - 2, 92, by + 18], fill=c_glass, outline=c_blue)
    draw.point((76, by + 4), fill=(255, 255, 255, 255)) # HUD glare

    # Stub wings extending to dual tilt-rotors
    draw.line([(24, by + 6), (136, by + 6)], fill=c_blue, width=4)
    # Rocket pods under wings
    draw.rectangle([34, by + 8, 44, by + 18], fill=(50, 55, 60, 255))
    draw.rectangle([116, by + 8, 126, by + 18], fill=(50, 55, 60, 255))

    # DYNAMIC SPINNING 4-BLADE ROTOR DISCS (Dual Tandem Rotors!)
    # Frame 0: 0 deg | Frame 1: 22.5 deg | Frame 2: 45 deg | Frame 3: 67.5 deg
    rotor_ang = (frame * 22.5) * math.pi / 180.0
    for rx, ry in [(24, by + 4), (136, by + 4)]:
        # Rotor hub
        draw.ellipse([rx - 4, ry - 3, rx + 4, ry + 3], fill=(30, 30, 30, 255))
        # Rotor motion blur disc
        draw.ellipse([rx - 22, ry - 9, rx + 22, ry + 9], fill=c_blur, outline=(140, 200, 245, 120))
        # 4 Spinning Blades at current rotation
        for a_off in [0, math.pi * 0.5, math.pi, math.pi * 1.5]:
            bx1 = rx + int(20 * math.cos(rotor_ang + a_off))
            by1 = ry + int(8 * math.sin(rotor_ang + a_off))
            draw.line([(rx, ry), (bx1, by1)], fill=c_blade, width=2)

    # Chin 25mm Gatling Turret
    draw.ellipse([76, by + 24, 84, by + 32], fill=(35, 38, 42, 255))
    draw.line([(80, by + 28), (80, by + 38)], fill=(20, 20, 20, 255), width=3)

    if is_fire and (frame == 1 or frame == 2):
        # Gatling tracer stream & rocket launch!
        draw.polygon([(76, by + 38), (84, by + 38), (80, by + 56)], fill=(255, 230, 60, 255))
        draw.line([(80, by + 40), (80, by + 68)], fill=(255, 255, 255, 255), width=2)
        # Rocket leaving left pod!
        rkt_x = 39
        rkt_y = by + 26
        draw.polygon([(rkt_x - 3, rkt_y), (rkt_x + 3, rkt_y), (rkt_x, rkt_y + 12)], fill=(220, 50, 30, 255))
        # Rocket exhaust smoke
        draw.ellipse([rkt_x - 6, rkt_y - 12, rkt_x + 6, rkt_y - 2], fill=(220, 220, 220, 180))

def draw_terran_skyhammer(draw, frame, mode="idle"):
    is_fire = (mode == "fire")
    y_bob = -1 if (frame % 2 == 1) else 0

    # draw.ellipse([26, 142, 134, 154], fill=(0, 0, 0, 70)) # Scrubbed for transparent ground
    by = 92 + y_bob

    c_olive = (60, 72, 54, 255)
    c_dark = (35, 42, 32, 255)
    c_glass = (120, 180, 220, 220)

    # Swept CAS Jet Wings
    draw.polygon([(80, by + 34), (20, by), (30, by - 12), (80, by + 4), (130, by - 12), (140, by)], fill=c_olive, outline=c_dark, width=2)
    # Fuselage & Titanium nose
    draw.polygon([(74, by + 42), (86, by + 42), (88, by - 22), (72, by - 22)], fill=c_olive, outline=c_dark, width=2)
    # Cockpit
    draw.ellipse([75, by, 85, by + 16], fill=c_glass, outline=c_dark)

    # Animated Pulsing Afterburner Jet Flames
    flame_lens = [10, 16, 22, 14]
    fl_len = flame_lens[frame % 4]
    draw.polygon([(75, by - 22), (85, by - 22), (80, by - 22 - fl_len)], fill=(255, 140, 20, 240))
    draw.polygon([(77, by - 22), (83, by - 22), (80, by - 22 - int(fl_len*0.6))], fill=(255, 240, 80, 255))

    # 30mm Rotary Nose Cannon
    draw.line([(80, by + 42), (80, by + 52)], fill=(30, 30, 30, 255), width=3)
    if is_fire and frame == 1:
        draw.polygon([(74, by + 52), (86, by + 52), (80, by + 72)], fill=(255, 220, 50, 255))

def draw_colony_dart(draw, frame, mode="idle"):
    is_fire = (mode == "fire")
    y_bob = -1 if (frame % 2 == 1) else 0

    # draw.ellipse([26, 142, 134, 154], fill=(0, 0, 0, 65)) # Scrubbed for transparent ground
    by = 92 + y_bob

    # Delta-wing interceptor
    draw.polygon([(80, by + 44), (18, by - 8), (34, by - 18), (80, by - 4), (126, by - 18), (142, by - 8)], fill=(225, 238, 248, 255), outline=(40, 80, 130, 255), width=2)
    draw.polygon([(75, by + 44), (85, by + 44), (87, by - 24), (73, by - 24)], fill=(225, 238, 248, 255), outline=(40, 80, 130, 255), width=2)

    # Twin Ion Afterburners
    fl_len = 8 + (frame * 4)
    for ix in [72, 88]:
        draw.polygon([(ix - 4, by - 24), (ix + 4, by - 24), (ix, by - 24 - fl_len)], fill=(0, 220, 255, 255))
        draw.polygon([(ix - 2, by - 24), (ix + 2, by - 24), (ix, by - 24 - int(fl_len*0.6))], fill=(255, 255, 255, 255))

def draw_syndicate_bomber(draw, frame, mode="idle"):
    is_fire = (mode == "fire")
    y_bob = -1 if (frame % 2 == 1) else 0

    # draw.ellipse([20, 142, 140, 154], fill=(0, 0, 0, 80)) # Scrubbed for transparent ground
    by = 90 + y_bob

    # Asymmetrical heavy bomber
    draw.polygon([(78, by + 36), (16, by + 4), (24, by - 14), (80, by - 4), (136, by - 14), (144, by + 4)], fill=(100, 65, 45, 255), outline=(45, 25, 18, 255), width=2)
    draw.polygon([(72, by + 42), (88, by + 42), (90, by - 20), (70, by - 20)], fill=(115, 75, 52, 255), outline=(45, 25, 18, 255), width=2)

    # Smoky turbofans venting soot
    for tx in [46, 114]:
        draw.rectangle([tx - 6, by - 10, tx + 6, by + 10], fill=(45, 40, 38, 255))
        # Flame & soot
        draw.ellipse([tx - 4, by - 18 - frame*4, tx + 4, by - 10 - frame*4], fill=(80, 75, 70, 180 - frame*35))
        draw.polygon([(tx - 4, by - 10), (tx + 4, by - 10), (tx, by - 18)], fill=(255, 120, 30, 240))

    if is_fire and frame == 1:
        # Bomb bay dropping slag canister
        draw.ellipse([76, by + 38, 84, by + 50], fill=(220, 70, 20, 255), outline=(255, 200, 40, 255))

def draw_zaibatsu_drone_jet(draw, frame, mode="idle"):
    is_fire = (mode == "fire")
    y_bob = -1 if (frame % 2 == 1) else 0

    # draw.ellipse([26, 142, 134, 154], fill=(0, 0, 0, 70)) # Scrubbed for transparent ground
    by = 92 + y_bob

    # Forward-swept wings
    draw.polygon([(80, by + 38), (14, by + 22), (24, by + 8), (80, by - 18), (136, by + 8), (146, by + 22)], fill=(26, 22, 32, 255), outline=(80, 50, 110, 255), width=2)
    # Red glowing sensor intake
    draw.polygon([(74, by + 38), (86, by + 38), (80, by + 44)], fill=(240, 30, 60, 255))
    # Magenta anti-grav thruster
    draw.polygon([(76, by - 18), (84, by - 18), (80, by - 32 - frame*3)], fill=(220, 40, 240, 240))

# =============================================================================
# WRECKAGES & SUPPRESSION WITH ANIMATED FIRE & SMOKE
# =============================================================================

def draw_tank_wreckage(draw, frame):
    # Burned out crumpled tank hull
    # draw.ellipse([20, 140, 140, 154], fill=(0, 0, 0, 100)) # Scrubbed for transparent ground
    draw.polygon([(30, 144), (130, 144), (122, 120), (38, 120)], fill=(32, 28, 26, 255), outline=(15, 12, 10, 255), width=2)
    # Shattered track links
    draw.line([(24, 146), (36, 136)], fill=(65, 55, 45, 255), width=3)
    draw.line([(124, 146), (134, 138)], fill=(65, 55, 45, 255), width=3)
    # Sheared off turret leaning in crater
    draw.polygon([(62, 126), (102, 126), (94, 108), (70, 114)], fill=(25, 22, 20, 255), outline=(15, 12, 10, 255), width=2)
    # Bent smoking cannon barrel
    draw.line([(90, 112), (116, 126)], fill=(20, 18, 16, 255), width=3)

    # ANIMATED FLICKERING FIRE FLAMES
    f_shift = (frame * 5) % 8
    draw.polygon([(74, 116), (82 + f_shift, 96), (88, 116)], fill=(255, 100, 20, 240))
    draw.polygon([(78, 116), (82, 104), (86, 116)], fill=(255, 220, 50, 255))

    # Billowing black & gray smoke puffs
    for s_idx, (sx, sy) in enumerate([(76, 92), (84, 76), (78, 60), (86, 44)]):
        sr = 8 + s_idx * 3 + (frame * 2)
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(45, 42, 40, 160 - s_idx*30))

def draw_plane_wreckage(draw, frame):
    # Burned aircraft crash crater
    # draw.ellipse([18, 138, 142, 154], fill=(0, 0, 0, 110)) # Scrubbed for transparent ground
    # Snapped delta wing
    draw.polygon([(24, 142), (76, 130), (62, 118)], fill=(45, 50, 55, 255), outline=(20, 22, 24, 255), width=2)
    # Crumpled smoking fuselage
    draw.polygon([(68, 138), (114, 138), (126, 124), (82, 122)], fill=(35, 38, 42, 255), outline=(15, 16, 18, 255), width=2)

    # Flickering flame & embers
    f_shift = (frame * 4) % 6
    draw.polygon([(88, 124), (94 + f_shift, 106), (102, 124)], fill=(255, 90, 20, 240))
    draw.polygon([(92, 124), (95, 112), (98, 124)], fill=(255, 210, 40, 255))
    # Rising smoke
    for s_idx, (sx, sy) in enumerate([(94, 98), (90, 80), (98, 62)]):
        sr = 7 + s_idx * 4 + frame
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(50, 48, 45, 150 - s_idx*35))

def draw_infantry_suppressed_state(draw, frame):
    # Pinned down soldiers behind blown sandbags with orange distress flare
    # draw.ellipse([30, 138, 130, 154], fill=(0, 0, 0, 85)) # Scrubbed for transparent ground
    # Broken sandbags
    draw.polygon([(46, 144), (114, 144), (108, 136), (52, 136)], fill=(110, 100, 75, 255), outline=(55, 50, 35, 255))
    # Scattered helmets and rifles in dirt
    draw.ellipse([54, 136, 62, 142], fill=(60, 75, 55, 255))
    draw.line([(96, 140), (112, 138)], fill=(30, 30, 30, 255), width=2)

    # 3 Soldiers huddling prone / ducking
    y_duck = 1 if (frame % 2 == 1) else 0
    for sx in [68, 82, 96]:
        draw.ellipse([sx - 6, 134 + y_duck, sx + 6, 140 + y_duck], fill=(50, 60, 45, 255), outline=(25, 30, 20, 255))
        draw.ellipse([sx - 4, 130 + y_duck, sx + 4, 136 + y_duck], fill=(60, 75, 55, 255)) # helmet

    # Orange Distress Signal Flare burning on ground with rising smoke
    fl_x = 74
    fl_y = 136
    draw.ellipse([fl_x - 3, fl_y - 2, fl_x + 3, fl_y + 2], fill=(255, 100, 20, 255))
    draw.polygon([(fl_x - 3, fl_y), (fl_x + 3, fl_y), (fl_x, fl_y - 8 - frame*2)], fill=(255, 180, 50, 255))
    # Expanding smoke puff
    smk_y = fl_y - 12 - frame * 4
    draw.ellipse([fl_x - 6 - frame*2, smk_y - 5, fl_x + 6 + frame*2, smk_y + 5], fill=(240, 160, 80, 140 - frame*25))

# =============================================================================
# BATCH EXECUTION & SPRITE CATALOG
# =============================================================================


# =============================================================================
# NEW 4x4 CONVENTIONAL MATRIX ASSETS
# =============================================================================

def draw_terran_sabre(draw, frame, mode="idle"):
    c_hull = (56, 64, 52, 255)
    c_hull_dark = (32, 36, 30, 255)
    c_hull_light = (95, 110, 88, 255)
    c_hazard = (235, 185, 45, 255)
    c_canopy = (215, 175, 75, 230)
    c_engine = (30, 30, 32, 255)

    y_bob = -1 if (frame % 2 == 1) else 0

    if mode == "back_idle":
        draw.polygon([(80, 72 + y_bob), (138, 102 + y_bob), (126, 112 + y_bob), (80, 88 + y_bob)], fill=c_hull, outline=c_hull_dark)
        draw.polygon([(80, 72 + y_bob), (22, 102 + y_bob), (34, 112 + y_bob), (80, 88 + y_bob)], fill=c_hull, outline=c_hull_dark)
        draw.polygon([(130, 98 + y_bob), (138, 102 + y_bob), (126, 112 + y_bob)], fill=c_hazard)
        draw.polygon([(30, 98 + y_bob), (22, 102 + y_bob), (34, 112 + y_bob)], fill=c_hazard)
        draw.polygon([(72, 54 + y_bob), (88, 54 + y_bob), (92, 106 + y_bob), (68, 106 + y_bob)], fill=c_hull, outline=c_hull_dark)
        draw.polygon([(68, 58 + y_bob), (64, 38 + y_bob), (72, 38 + y_bob), (74, 68 + y_bob)], fill=c_hull_light, outline=c_hull_dark)
        draw.polygon([(92, 58 + y_bob), (96, 38 + y_bob), (88, 38 + y_bob), (86, 68 + y_bob)], fill=c_hull_light, outline=c_hull_dark)
        draw.ellipse([70, 100 + y_bob, 78, 110 + y_bob], fill=(255, 140, 40, 255), outline=c_engine)
        draw.ellipse([82, 100 + y_bob, 90, 110 + y_bob], fill=(255, 140, 40, 255), outline=c_engine)
        draw.ellipse([72, 102 + y_bob, 76, 108 + y_bob], fill=(255, 240, 180, 255))
        draw.ellipse([84, 102 + y_bob, 88, 108 + y_bob], fill=(255, 240, 180, 255))
        return

    # FRONT ISOMETRIC PERSPECTIVE
    draw.polygon([(80, 80 + y_bob), (142, 98 + y_bob), (130, 108 + y_bob), (80, 96 + y_bob)], fill=c_hull, outline=c_hull_dark)
    draw.polygon([(80, 80 + y_bob), (18, 98 + y_bob), (30, 108 + y_bob), (80, 96 + y_bob)], fill=c_hull, outline=c_hull_dark)
    draw.line([(82, 84 + y_bob), (132, 100 + y_bob)], fill=c_hull_light, width=1)
    draw.line([(78, 84 + y_bob), (28, 100 + y_bob)], fill=c_hull_light, width=1)
    draw.polygon([(134, 95 + y_bob), (142, 98 + y_bob), (130, 108 + y_bob)], fill=c_hazard)
    draw.polygon([(26, 95 + y_bob), (18, 98 + y_bob), (30, 108 + y_bob)], fill=c_hazard)
    for mx in [42, 58, 102, 118]:
        draw.rectangle([mx - 2, 102 + y_bob, mx + 2, 116 + y_bob], fill=(220, 220, 225, 255), outline=(60, 60, 65, 255))
        draw.polygon([(mx - 2, 116 + y_bob), (mx + 2, 116 + y_bob), (mx, 120 + y_bob)], fill=(220, 40, 40, 255))
    draw.polygon([(80, 42 + y_bob), (94, 76 + y_bob), (92, 112 + y_bob), (68, 112 + y_bob), (66, 76 + y_bob)], fill=c_hull, outline=c_hull_dark)
    draw.line([(80, 46 + y_bob), (80, 108 + y_bob)], fill=c_hull_light, width=2)
    draw.ellipse([74, 56 + y_bob, 86, 76 + y_bob], fill=c_canopy, outline=c_hull_dark)
    draw.line([(77, 59 + y_bob), (83, 73 + y_bob)], fill=(255, 255, 255, 180))
    draw.rectangle([78, 110 + y_bob, 82, 124 + y_bob], fill=c_engine, outline=(15, 15, 15, 255))

    if mode == "fire":
        fl_r = 8 if (frame % 2 == 1) else 14
        draw.ellipse([80 - fl_r, 124 + y_bob, 80 + fl_r, 124 + y_bob + fl_r * 2], fill=(255, 240, 100, 240))
        draw.ellipse([80 - fl_r // 2, 126 + y_bob, 80 + fl_r // 2, 126 + y_bob + fl_r * 2 - 4], fill=(255, 255, 240, 255))
        if frame >= 1:
            draw.ellipse([100, 124 + y_bob, 104, 134 + y_bob], fill=(255, 160, 40, 255), outline=(255, 240, 120, 255))
            draw.ellipse([98, 114 + y_bob, 106, 122 + y_bob], fill=(200, 200, 200, 160))

def draw_syndicate_chopper(draw, frame, mode="idle"):
    c_rust = (120, 68, 48, 255)
    c_dark = (42, 42, 45, 255)
    c_weld = (185, 190, 195, 255)
    c_hazard = (235, 175, 35, 255)
    c_engine = (55, 58, 62, 255)

    y_bob = -1 if (frame % 2 == 1) else 0

    draw.line([(44, 134 + y_bob), (116, 134 + y_bob)], fill=(50, 50, 55, 255), width=3)
    draw.line([(58, 122 + y_bob), (54, 134 + y_bob)], fill=c_dark, width=2)
    draw.line([(102, 122 + y_bob), (106, 134 + y_bob)], fill=c_dark, width=2)

    if mode == "back_idle":
        draw.polygon([(72, 70 + y_bob), (88, 70 + y_bob), (84, 114 + y_bob), (76, 114 + y_bob)], fill=c_rust, outline=c_dark)
        draw.polygon([(74, 82 + y_bob), (78, 82 + y_bob), (28, 52 + y_bob), (26, 58 + y_bob)], fill=c_dark)
        for tx in [36, 48, 60]:
            draw.line([(tx, 58 + y_bob), (tx + 6, 68 + y_bob)], fill=c_hazard, width=3)
        draw.line([(24, 40 + y_bob), (28, 68 + y_bob)], fill=(200, 205, 210, 200), width=2)
        draw.rectangle([72, 60 + y_bob, 88, 72 + y_bob], fill=c_engine, outline=c_dark)
        for ey in range(62, 72, 3):
            draw.line([(74, ey + y_bob), (86, ey + y_bob)], fill=c_weld)
        draw.rectangle([76, 44 + y_bob, 84, 60 + y_bob], fill=c_dark, outline=c_weld)
        draw.ellipse([16, 38 + y_bob, 144, 48 + y_bob], fill=(180, 185, 190, 80), outline=(140, 145, 150, 120))
        return

    # FRONT ISOMETRIC VIEW
    draw.polygon([(52, 72 + y_bob), (96, 68 + y_bob), (112, 92 + y_bob), (106, 120 + y_bob), (58, 122 + y_bob), (48, 98 + y_bob)], fill=c_rust, outline=c_dark)
    draw.line([(52, 92 + y_bob), (110, 90 + y_bob)], fill=c_weld, width=2)
    draw.line([(78, 70 + y_bob), (82, 121 + y_bob)], fill=c_weld, width=2)
    draw.polygon([(68, 74 + y_bob), (94, 72 + y_bob), (98, 90 + y_bob), (72, 92 + y_bob)], fill=(20, 22, 25, 255), outline=c_hazard)
    for wx in range(72, 96, 4):
        draw.line([(wx, 74 + y_bob), (wx, 90 + y_bob)], fill=(90, 95, 100, 200))
    draw.rectangle([60, 54 + y_bob, 74, 70 + y_bob], fill=c_engine, outline=c_dark)
    draw.line([(58, 56 + y_bob), (50, 46 + y_bob)], fill=(70, 70, 75, 255), width=3)
    if frame % 2 == 1:
        draw.ellipse([44, 38 + y_bob, 52, 46 + y_bob], fill=(50, 50, 50, 160))
    draw.rectangle([94, 114 + y_bob, 124, 122 + y_bob], fill=c_dark, outline=c_weld)
    draw.line([(96, 116 + y_bob), (128, 116 + y_bob)], fill=(80, 80, 85), width=2)
    draw.line([(96, 120 + y_bob), (128, 120 + y_bob)], fill=(80, 80, 85), width=2)
    draw.ellipse([86, 112 + y_bob, 96, 124 + y_bob], fill=(160, 130, 40, 255))
    draw.rectangle([76, 42 + y_bob, 84, 68 + y_bob], fill=c_dark, outline=c_weld)
    draw.ellipse([14, 36 + y_bob, 146, 48 + y_bob], fill=(190, 195, 200, 90), outline=(150, 155, 160, 140))
    b_len = 54
    ang = (frame * 60) * (3.14159 / 180.0)
    bx = 80 + int(b_len * math.cos(ang))
    by = 42 + y_bob + int(b_len * 0.25 * math.sin(ang))
    draw.line([(80, 42 + y_bob), (bx, by)], fill=(220, 225, 230, 240), width=3)

    if mode == "fire":
        m_r = 10 if (frame % 2 == 1) else 16
        draw.ellipse([128, 112 + y_bob, 128 + m_r * 2, 124 + y_bob], fill=(255, 220, 60, 255))
        draw.ellipse([130, 115 + y_bob, 130 + m_r, 121 + y_bob], fill=(255, 255, 240, 255))
        draw.rectangle([100 - frame * 4, 124 + frame * 5, 104 - frame * 4, 128 + frame * 5], fill=(240, 200, 50, 255))

def draw_zaibatsu_rotor(draw, frame, mode="idle"):
    c_carbon = (26, 28, 34, 255)
    c_facet = (48, 52, 62, 255)
    c_optic = (235, 35, 65, 255)
    c_plasma = (35, 220, 210, 255)
    c_fan = (60, 65, 75, 255)

    y_bob = -1 if (frame % 2 == 1) else 0

    if mode == "back_idle":
        draw.polygon([(80, 80 + y_bob), (142, 88 + y_bob), (130, 98 + y_bob), (80, 92 + y_bob)], fill=c_carbon, outline=c_facet)
        draw.polygon([(80, 80 + y_bob), (18, 88 + y_bob), (30, 98 + y_bob), (80, 92 + y_bob)], fill=c_carbon, outline=c_facet)
        for dx in [36, 124]:
            draw.ellipse([dx - 20, 76 + y_bob, dx + 20, 104 + y_bob], fill=c_carbon, outline=c_facet, width=3)
            draw.ellipse([dx - 14, 80 + y_bob, dx + 14, 100 + y_bob], fill=(15, 16, 20, 255), outline=c_plasma)
            f_ang = (frame * 45) * (3.14159 / 180.0)
            for k in range(4):
                a = f_ang + k * (3.14159 / 2.0)
                bx = dx + int(12 * math.cos(a))
                by = 90 + y_bob + int(8 * math.sin(a))
                draw.line([(dx, 90 + y_bob), (bx, by)], fill=c_fan, width=2)
        draw.polygon([(72, 60 + y_bob), (88, 60 + y_bob), (92, 114 + y_bob), (68, 114 + y_bob)], fill=c_carbon, outline=c_facet)
        draw.rectangle([74, 102 + y_bob, 86, 110 + y_bob], fill=(20, 22, 28, 255), outline=c_facet)
        for ey in range(104, 110, 3):
            draw.line([(76, ey + y_bob), (84, ey + y_bob)], fill=c_plasma)
        return

    # FRONT ISOMETRIC PERSPECTIVE
    draw.polygon([(80, 84 + y_bob), (144, 90 + y_bob), (132, 102 + y_bob), (80, 98 + y_bob)], fill=c_carbon, outline=c_facet)
    draw.polygon([(80, 84 + y_bob), (16, 90 + y_bob), (28, 102 + y_bob), (80, 98 + y_bob)], fill=c_carbon, outline=c_facet)
    for dx in [36, 124]:
        draw.ellipse([dx - 22, 78 + y_bob, dx + 22, 106 + y_bob], fill=c_carbon, outline=c_facet, width=3)
        draw.ellipse([dx - 15, 82 + y_bob, dx + 15, 102 + y_bob], fill=(18, 20, 24, 255), outline=c_plasma)
        f_ang = (frame * 45) * (3.14159 / 180.0)
        for k in range(4):
            a = f_ang + k * (3.14159 / 2.0)
            bx = dx + int(13 * math.cos(a))
            by = 92 + y_bob + int(9 * math.sin(a))
            draw.line([(dx, 92 + y_bob), (bx, by)], fill=(120, 130, 145, 220), width=2)
    draw.polygon([(80, 52 + y_bob), (96, 78 + y_bob), (94, 118 + y_bob), (66, 118 + y_bob), (64, 78 + y_bob)], fill=c_carbon, outline=c_facet)
    draw.line([(80, 54 + y_bob), (80, 116 + y_bob)], fill=c_facet, width=2)
    draw.polygon([(72, 74 + y_bob), (88, 74 + y_bob), (84, 82 + y_bob), (76, 82 + y_bob)], fill=c_optic)
    draw.line([(74, 76 + y_bob), (86, 76 + y_bob)], fill=(255, 180, 190, 240))
    draw.ellipse([74, 114 + y_bob, 86, 126 + y_bob], fill=(18, 20, 25, 255), outline=c_facet)
    draw.rectangle([78, 122 + y_bob, 82, 128 + y_bob], fill=c_plasma)

    if mode == "fire":
        draw.line([(80, 126 + y_bob), (80, 156 + y_bob)], fill=(180, 255, 250, 255), width=4)
        draw.line([(80, 126 + y_bob), (80, 156 + y_bob)], fill=c_plasma, width=2)
        draw.ellipse([72, 120 + y_bob, 88, 132 + y_bob], fill=(120, 255, 245, 200))

sprites_to_build = [
    # 1. INFANTRY SQUADS (ALL 4 FACTIONS x 4 ANIMATION STATES = 16 SPRITES)
    ("spr_inf_terran_squad_idle", lambda d, f: draw_infantry_squad(d, f, "terran", "idle")),
    ("spr_inf_terran_squad_back_idle", lambda d, f: draw_infantry_squad(d, f, "terran", "back_idle")),
    ("spr_inf_terran_squad_fire", lambda d, f: draw_infantry_squad(d, f, "terran", "fire")),
    ("spr_inf_terran_squad_defeat", lambda d, f: draw_infantry_squad(d, f, "terran", "defeat")),

    ("spr_inf_colony_squad_idle", lambda d, f: draw_infantry_squad(d, f, "colony", "idle")),
    ("spr_inf_colony_squad_back_idle", lambda d, f: draw_infantry_squad(d, f, "colony", "back_idle")),
    ("spr_inf_colony_squad_fire", lambda d, f: draw_infantry_squad(d, f, "colony", "fire")),
    ("spr_inf_colony_squad_defeat", lambda d, f: draw_infantry_squad(d, f, "colony", "defeat")),

    ("spr_inf_syndicate_squad_idle", lambda d, f: draw_infantry_squad(d, f, "syndicate", "idle")),
    ("spr_inf_syndicate_squad_back_idle", lambda d, f: draw_infantry_squad(d, f, "syndicate", "back_idle")),
    ("spr_inf_syndicate_squad_fire", lambda d, f: draw_infantry_squad(d, f, "syndicate", "fire")),
    ("spr_inf_syndicate_squad_defeat", lambda d, f: draw_infantry_squad(d, f, "syndicate", "defeat")),

    ("spr_inf_zaibatsu_squad_idle", lambda d, f: draw_infantry_squad(d, f, "zaibatsu", "idle")),
    ("spr_inf_zaibatsu_squad_back_idle", lambda d, f: draw_infantry_squad(d, f, "zaibatsu", "back_idle")),
    ("spr_inf_zaibatsu_squad_fire", lambda d, f: draw_infantry_squad(d, f, "zaibatsu", "fire")),
    ("spr_inf_zaibatsu_squad_defeat", lambda d, f: draw_infantry_squad(d, f, "zaibatsu", "defeat")),

    # Universal Suppression
    ("spr_inf_suppressed", draw_infantry_suppressed_state),

    # 2. TANKS & GROUND VEHICLES (4 VEHICLES x 3 STATES = 12 SPRITES)
    ("spr_veh_terran_mammoth_idle", lambda d, f: draw_terran_tank(d, f, "idle")),
    ("spr_veh_terran_mammoth_back_idle", lambda d, f: draw_terran_tank(d, f, "back_idle")),
    ("spr_veh_terran_mammoth_fire", lambda d, f: draw_terran_tank(d, f, "fire")),

    ("spr_veh_colony_stiletto_idle", lambda d, f: draw_colony_stiletto(d, f, "idle")),
    ("spr_veh_colony_stiletto_back_idle", lambda d, f: draw_colony_stiletto(d, f, "back_idle")),
    ("spr_veh_colony_stiletto_fire", lambda d, f: draw_colony_stiletto(d, f, "fire")),

    ("spr_veh_syndicate_technical_idle", lambda d, f: draw_syndicate_technical(d, f, "idle")),
    ("spr_veh_syndicate_technical_back_idle", lambda d, f: draw_syndicate_technical(d, f, "back_idle")),
    ("spr_veh_syndicate_technical_fire", lambda d, f: draw_syndicate_technical(d, f, "fire")),

    ("spr_veh_zaibatsu_kurogane_idle", lambda d, f: draw_zaibatsu_kurogane(d, f, "idle")),
    ("spr_veh_zaibatsu_kurogane_back_idle", lambda d, f: draw_zaibatsu_kurogane(d, f, "back_idle")),
    ("spr_veh_zaibatsu_kurogane_fire", lambda d, f: draw_zaibatsu_kurogane(d, f, "fire")),

    # 3. HELICOPTERS / TILT-ROTORS & AIRCRAFT (5 VEHICLES x 3 STATES = 15 SPRITES)
    ("spr_veh_colony_gunship_idle", lambda d, f: draw_colony_gunship(d, f, "idle")),
    ("spr_veh_colony_gunship_back_idle", lambda d, f: draw_colony_gunship(d, f, "back_idle")),
    ("spr_veh_colony_gunship_fire", lambda d, f: draw_colony_gunship(d, f, "fire")),

    ("spr_veh_terran_skyhammer_idle", lambda d, f: draw_terran_skyhammer(d, f, "idle")),
    ("spr_veh_terran_skyhammer_back_idle", lambda d, f: draw_terran_skyhammer(d, f, "back_idle")),
    ("spr_veh_terran_skyhammer_fire", lambda d, f: draw_terran_skyhammer(d, f, "fire")),

    ("spr_veh_colony_dart_idle", lambda d, f: draw_colony_dart(d, f, "idle")),
    ("spr_veh_colony_dart_back_idle", lambda d, f: draw_colony_dart(d, f, "back_idle")),
    ("spr_veh_colony_dart_fire", lambda d, f: draw_colony_dart(d, f, "fire")),

    ("spr_veh_syndicate_bomber_idle", lambda d, f: draw_syndicate_bomber(d, f, "idle")),
    ("spr_veh_syndicate_bomber_back_idle", lambda d, f: draw_syndicate_bomber(d, f, "back_idle")),
    ("spr_veh_syndicate_bomber_fire", lambda d, f: draw_syndicate_bomber(d, f, "fire")),

    ("spr_veh_zaibatsu_drone_jet_idle", lambda d, f: draw_zaibatsu_drone_jet(d, f, "idle")),
    ("spr_veh_zaibatsu_drone_jet_back_idle", lambda d, f: draw_zaibatsu_drone_jet(d, f, "back_idle")),
    ("spr_veh_zaibatsu_drone_jet_fire", lambda d, f: draw_zaibatsu_drone_jet(d, f, "fire")),

    ("spr_veh_terran_sabre_idle", lambda d, f: draw_terran_sabre(d, f, "idle")),
    ("spr_veh_terran_sabre_back_idle", lambda d, f: draw_terran_sabre(d, f, "back_idle")),
    ("spr_veh_terran_sabre_fire", lambda d, f: draw_terran_sabre(d, f, "fire")),

    ("spr_veh_syndicate_chopper_idle", lambda d, f: draw_syndicate_chopper(d, f, "idle")),
    ("spr_veh_syndicate_chopper_back_idle", lambda d, f: draw_syndicate_chopper(d, f, "back_idle")),
    ("spr_veh_syndicate_chopper_fire", lambda d, f: draw_syndicate_chopper(d, f, "fire")),

    ("spr_veh_zaibatsu_rotor_idle", lambda d, f: draw_zaibatsu_rotor(d, f, "idle")),
    ("spr_veh_zaibatsu_rotor_back_idle", lambda d, f: draw_zaibatsu_rotor(d, f, "back_idle")),
    ("spr_veh_zaibatsu_rotor_fire", lambda d, f: draw_zaibatsu_rotor(d, f, "fire")),

    # 4. WRECKAGES (2 SPRITES)
    ("spr_veh_wreckage_tank", draw_tank_wreckage),
    ("spr_veh_wreckage_plane", draw_plane_wreckage)
]

print(f"Generating all {len(sprites_to_build)} high-detail sprites...")
for spr_name, draw_fn in sprites_to_build:
    build_sprite(spr_name, draw_fn)

# Register newly added sprites in MechMakerConcept.yyp
with open(YYP_PATH, "r") as f:
    yyp_content = f.read()

reg_count = 0
for spr_name, _ in sprites_to_build:
    spr_path = f"sprites/{spr_name}/{spr_name}.yy"
    res_entry = f"{{\"id\":{{\"name\":\"{spr_name}\",\"path\":\"{spr_path}\",}},}},"
    if spr_name not in yyp_content:
        marker = '"resources": ['
        idx = yyp_content.find(marker)
        if idx != -1:
            insert_pos = idx + len(marker)
            yyp_content = yyp_content[:insert_pos] + f"\n    {res_entry}" + yyp_content[insert_pos:]
            reg_count += 1

with open(YYP_PATH, "w") as f:
    f.write(yyp_content)

print(f"Generated {len(sprites_to_build)} high-detail retro assets! Registered {reg_count} new entries in {YYP_PATH}.")
