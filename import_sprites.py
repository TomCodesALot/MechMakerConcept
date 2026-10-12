import os
import json
import uuid
from PIL import Image
from collections import deque

CANVAS_W = 160
CANVAS_H = 160
ORIGIN_X = 80
ORIGIN_Y = 145

PROJECT_DIR = "/home/tom/GameMakerProjects/MechMakerConcept"
BRAIN_DIR = "/home/tom/.gemini/antigravity-ide/brain/51ad915f-cc60-4133-9e60-afcc1d5a4bc8"

HERO_IMG = os.path.join(BRAIN_DIR, "ironclad_hero_sprite_1791663986581.jpg")
FX_IMG = os.path.join(BRAIN_DIR, "ironclad_combat_fx_1791664172543.jpg")
DMG_IMG = os.path.join(BRAIN_DIR, "ironclad_damage_states_1791664187722.jpg")

def extract_bfs(im, tolerance=24):
    im = im.convert("RGBA")
    w, h = im.size
    pixels = im.load()
    bg_r, bg_g, bg_b, _ = pixels[0, 0]
    visited = set()
    queue = deque()
    
    tol_sq = tolerance * tolerance
    for x in range(w):
        for y in [0, h-1]:
            r, g, b, _ = pixels[x, y]
            if (r-bg_r)**2 + (g-bg_g)**2 + (b-bg_b)**2 < tol_sq:
                queue.append((x, y))
                visited.add((x, y))
    for y in range(h):
        for x in [0, w-1]:
            if (x, y) not in visited:
                r, g, b, _ = pixels[x, y]
                if (r-bg_r)**2 + (g-bg_g)**2 + (b-bg_b)**2 < tol_sq:
                    queue.append((x, y))
                    visited.add((x, y))
                    
    while queue:
        cx, cy = queue.popleft()
        pixels[cx, cy] = (0, 0, 0, 0)
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                r, g, b, a = pixels[nx, ny]
                if (r-bg_r)**2 + (g-bg_g)**2 + (b-bg_b)**2 < tol_sq:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    return im

def fit_on_canvas(cropped_im, max_h=130):
    bbox = cropped_im.getbbox()
    if bbox:
        cropped_im = cropped_im.crop(bbox)
    
    # Scale proportionally
    cw, ch = cropped_im.size
    scale = min(140.0 / max(1, cw), float(max_h) / max(1, ch))
    nw = max(1, int(cw * scale))
    nh = max(1, int(ch * scale))
    
    resized = cropped_im.resize((nw, nh), Image.Resampling.LANCZOS)
    
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    # Place bottom anchored near ORIGIN_Y
    paste_x = (CANVAS_W - nw) // 2
    paste_y = ORIGIN_Y - nh
    if paste_y < 5:
        paste_y = 5
    canvas.paste(resized, (paste_x, paste_y), resized)
    return canvas

def create_sprite_resource(sprite_name, frames_images, speed=10.0):
    sprite_dir = os.path.join(PROJECT_DIR, "sprites", sprite_name)
    layers_dir = os.path.join(sprite_dir, "layers")
    os.makedirs(sprite_dir, exist_ok=True)
    os.makedirs(layers_dir, exist_ok=True)
    
    layer_uuid = str(uuid.uuid4())
    frame_uuids = [str(uuid.uuid4()) for _ in frames_images]
    
    # Save composite preview
    frames_images[0].save(os.path.join(sprite_dir, f"{sprite_name}.png"))
    
    frames_meta = []
    keyframes_meta = []
    
    for idx, (frame_im, f_uuid) in enumerate(zip(frames_images, frame_uuids)):
        # Save frame png
        frame_im.save(os.path.join(sprite_dir, f"{f_uuid}.png"))
        
        # Save layer frame png
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
        "bbox_bottom": CANVAS_H - 1,
        "bbox_left": 0,
        "bbox_right": CANVAS_W - 1,
        "bbox_top": 0,
        "collisionKind": 1,
        "collisionTolerance": 0,
        "DynamicTexturePage": False,
        "edgeFiltering": False,
        "For3D": False,
        "frames": frames_meta,
        "gridX": 0,
        "gridY": 0,
        "height": CANVAS_H,
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
            "length": float(len(frames_images)),
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
            "xorigin": ORIGIN_X,
            "yorigin": ORIGIN_Y
        },
        "swatchColours": None,
        "swfPrecision": 2.525,
        "textureGroupId": {
            "name": "Default",
            "path": "texturegroups/Default"
        },
        "type": 0,
        "VTile": False,
        "width": CANVAS_W
    }
    
    yy_path = os.path.join(sprite_dir, f"{sprite_name}.yy")
    with open(yy_path, "w") as f:
        json.dump(yy_data, f, indent=2)
    print(f"Created sprite: {sprite_name} ({len(frames_images)} frames)")
    return sprite_name

print("Processing images...")
hero_raw = Image.open(HERO_IMG)
fx_raw = Image.open(FX_IMG)
dmg_raw = Image.open(DMG_IMG)

# 1. Idle
hero_trans = extract_bfs(hero_raw, tolerance=25)
spr_idle = [fit_on_canvas(hero_trans, max_h=130)]
create_sprite_resource("spr_ms_ironclad_idle", spr_idle, speed=1.0)

# 2. Combat animations (6 frames each)
# Row 0: Rifle
cw, ch = fx_raw.width / 6.0, fx_raw.height / 6.0
rifle_frames = []
for c in range(6):
    box = (int(c*cw), int(0*ch), int((c+1)*cw), int(1*ch))
    crop = fx_raw.crop(box)
    trans = extract_bfs(crop, tolerance=24)
    rifle_frames.append(fit_on_canvas(trans, max_h=130))
create_sprite_resource("spr_ms_ironclad_fire_rifle", rifle_frames, speed=12.0)

# Row 2: Chaingun
chaingun_frames = []
for c in range(6):
    box = (int(c*cw), int(2*ch), int((c+1)*cw), int(3*ch))
    crop = fx_raw.crop(box)
    trans = extract_bfs(crop, tolerance=24)
    chaingun_frames.append(fit_on_canvas(trans, max_h=130))
create_sprite_resource("spr_ms_ironclad_fire_chaingun", chaingun_frames, speed=16.0)

# Row 4: Missiles
missile_frames = []
for c in range(6):
    box = (int(c*cw), int(4*ch), int((c+1)*cw), int(5*ch))
    crop = fx_raw.crop(box)
    trans = extract_bfs(crop, tolerance=24)
    missile_frames.append(fit_on_canvas(trans, max_h=130))
create_sprite_resource("spr_ms_ironclad_fire_missiles", missile_frames, speed=10.0)

# 3. Damage states
# Left arm destroyed
crop_la = dmg_raw.crop((0, 0, 340, 480))
trans_la = extract_bfs(crop_la, tolerance=24)
create_sprite_resource("spr_ms_ironclad_damage_left_arm", [fit_on_canvas(trans_la, max_h=130)], speed=1.0)

# Right arm destroyed
crop_ra = dmg_raw.crop((340, 0, 680, 480))
trans_ra = extract_bfs(crop_ra, tolerance=24)
create_sprite_resource("spr_ms_ironclad_damage_right_arm", [fit_on_canvas(trans_ra, max_h=130)], speed=1.0)

# Legs crippled
crop_legs = dmg_raw.crop((0, 520, 512, 1024))
trans_legs = extract_bfs(crop_legs, tolerance=24)
create_sprite_resource("spr_ms_ironclad_crippled", [fit_on_canvas(trans_legs, max_h=110)], speed=1.0)

# Destroyed
crop_dest = dmg_raw.crop((512, 520, 1024, 1024))
trans_dest = extract_bfs(crop_dest, tolerance=24)
create_sprite_resource("spr_ms_ironclad_destroyed", [fit_on_canvas(trans_dest, max_h=100)], speed=1.0)

print("All sprites successfully generated!")
