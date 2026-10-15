import os, sys, json, uuid
from PIL import Image, ImageDraw, ImageFont

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITES_DIR = os.path.join(PROJECT_DIR, "sprites")
YYP_PATH = os.path.join(PROJECT_DIR, "MechMakerConcept.yyp")

def create_gm_sprite_resource(sprite_name, frames, speed=0.0):
    w, h = frames[0].size
    sprite_dir = os.path.join(SPRITES_DIR, sprite_name)
    layers_dir = os.path.join(sprite_dir, "layers")
    os.makedirs(sprite_dir, exist_ok=True)
    os.makedirs(layers_dir, exist_ok=True)

    layer_uuid = str(uuid.uuid4())
    frame_uuids = [str(uuid.uuid4()) for _ in frames]

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
                "$GMImageLayer": "v1",
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
        "origin": 0,
        "parent": {
            "name": "sprites",
            "path": "folders/sprites.yy"
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
        "width": w
    }

    yy_path = os.path.join(sprite_dir, f"{sprite_name}.yy")
    with open(yy_path, "w") as f:
        json.dump(yy_data, f, indent=2)

    register_in_yyp(sprite_name, f"sprites/{sprite_name}/{sprite_name}.yy")
    print(f"✓ Generated Sprite: {sprite_name} ({w}x{h}, {len(frames)} frames)")

def register_in_yyp(name, path):
    with open(YYP_PATH, "r") as f:
        content = f.read()

    target_entry = f'"path":"{path}"'
    if target_entry in content:
        return

    idx = content.find('"resources":[\n')
    if idx == -1:
        idx = content.find('"resources": [')
    
    bracket_idx = content.find('],', idx)
    if bracket_idx != -1:
        new_entry = f'    {{"id":{{"name":"{name}","path":"{path}",}},}},\n'
        content = content[:bracket_idx] + new_entry + content[bracket_idx:]
        with open(YYP_PATH, "w") as f:
            f.write(content)
        print(f"  -> Registered {name} in MechMakerConcept.yyp")

def generate_stamps():
    W, H = 84, 26
    frames = []

    # Palette definitions
    c_dark = (10, 14, 20, 255)
    c_black = (0, 0, 0, 255)

    # Frame 0: GRADE S (Emerald / Laurel Glint)
    f0 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d0 = ImageDraw.Draw(f0)
    d0.rectangle([0, 0, W-1, H-1], fill=(12, 38, 24, 240), outline=(40, 220, 120, 255))
    d0.rectangle([2, 2, W-3, H-3], outline=(80, 255, 160, 200))
    # Bevel highlights
    d0.line([(1, 1), (W-2, 1)], fill=(140, 255, 200, 255))
    d0.line([(1, 1), (1, H-2)], fill=(140, 255, 200, 255))
    # Laurel tick brackets
    d0.line([(6, 6), (6, H-7), (12, H-7)], fill=(255, 220, 80, 255), width=2)
    d0.line([(W-7, 6), (W-7, H-7), (W-13, H-7)], fill=(255, 220, 80, 255), width=2)
    d0.text((18, 6), "★ GRADE S ★", fill=(255, 235, 120, 255))
    frames.append(f0)

    # Frame 1: GRADE A (Cyan / Navy Military)
    f1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(f1)
    d1.rectangle([0, 0, W-1, H-1], fill=(14, 30, 48, 240), outline=(60, 180, 240, 255))
    d1.rectangle([2, 2, W-3, H-3], outline=(100, 220, 255, 180))
    d1.line([(1, 1), (W-2, 1)], fill=(180, 240, 255, 255))
    d1.line([(1, 1), (1, H-2)], fill=(180, 240, 255, 255))
    d1.text((16, 6), "APPROVED [A]", fill=(120, 230, 255, 255))
    frames.append(f1)

    # Frame 2: GRADE B (Amber / Caution)
    f2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(f2)
    d2.rectangle([0, 0, W-1, H-1], fill=(42, 26, 10, 240), outline=(240, 160, 40, 255))
    d2.rectangle([2, 2, W-3, H-3], outline=(255, 190, 80, 180))
    d2.line([(1, 1), (W-2, 1)], fill=(255, 220, 140, 255))
    d2.line([(1, 1), (1, H-2)], fill=(255, 220, 140, 255))
    d2.text((15, 6), "CONDITIONAL", fill=(255, 190, 80, 255))
    frames.append(f2)

    # Frame 3: GRADE F (Crimson / Rejection)
    f3 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d3 = ImageDraw.Draw(f3)
    d3.rectangle([0, 0, W-1, H-1], fill=(40, 12, 12, 240), outline=(240, 50, 50, 255))
    d3.rectangle([2, 2, W-3, H-3], outline=(255, 90, 90, 180))
    d3.line([(1, 1), (W-2, 1)], fill=(255, 140, 140, 255))
    d3.line([(1, 1), (1, H-2)], fill=(255, 140, 140, 255))
    d3.text((18, 6), "REJECTED [F]", fill=(255, 110, 110, 255))
    frames.append(f3)

    # Frame 4: BLOCK II (Gold Modernized Crest)
    f4 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d4 = ImageDraw.Draw(f4)
    d4.rectangle([0, 0, W-1, H-1], fill=(36, 28, 8, 240), outline=(230, 190, 60, 255))
    d4.rectangle([2, 2, W-3, H-3], outline=(255, 220, 100, 200))
    d4.line([(1, 1), (W-2, 1)], fill=(255, 240, 160, 255))
    d4.line([(1, 1), (1, H-2)], fill=(255, 240, 160, 255))
    d4.text((14, 6), "MODERNIZED II", fill=(255, 225, 100, 255))
    frames.append(f4)

    # Frame 5: TOOLING (Hazard Yellow / Black)
    f5 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d5 = ImageDraw.Draw(f5)
    d5.rectangle([0, 0, W-1, H-1], fill=(24, 20, 8, 240), outline=(220, 180, 20, 255))
    # Diagonal hazard stripes
    for x in range(-H, W, 8):
        d5.line([(x, 0), (x + H, H)], fill=(240, 200, 30, 100), width=3)
    d5.rectangle([2, 2, W-3, H-3], outline=(255, 230, 60, 180))
    d5.text((15, 6), "TOOLING LINE", fill=(255, 235, 90, 255))
    frames.append(f5)

    create_gm_sprite_resource("spr_snes_trial_stamps", frames)

if __name__ == "__main__":
    generate_stamps()
