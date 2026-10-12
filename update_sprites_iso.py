import os
import json
import uuid
from PIL import Image
from collections import deque

CANVAS_W = 256
CANVAS_H = 256
ORIGIN_X = 128
ORIGIN_Y = 252

PROJECT_DIR = "/home/tom/GameMakerProjects/MechMakerConcept"
BRAIN_DIR = "/home/tom/.gemini/antigravity-ide/brain/c567b0d7-8303-46ee-b106-fe15fa1cd9a4"

COMBAT_IMG = os.path.join(BRAIN_DIR, "ironclad_combat_updated_iso_1791687829539.jpg")
DAMAGE_IMG = os.path.join(BRAIN_DIR, "ironclad_damage_types_iso_1791687847137.jpg")
DMG_ISO_IMG = os.path.join(BRAIN_DIR, "ironclad_damage_iso_1791669067465.jpg")

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
                    visited.add((x, y))
                    queue.append((x, y))
                    
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

def create_sprite_resource(sprite_name, frames_images, speed=8.0):
    sprite_dir = os.path.join(PROJECT_DIR, "sprites", sprite_name)
    layers_dir = os.path.join(sprite_dir, "layers")
    if os.path.exists(sprite_dir):
        import shutil
        shutil.rmtree(sprite_dir)
    os.makedirs(sprite_dir, exist_ok=True)
    os.makedirs(layers_dir, exist_ok=True)
    
    layer_uuid = str(uuid.uuid4())
    frame_uuids = [str(uuid.uuid4()) for _ in frames_images]
    
    # Save composite preview
    frames_images[0].save(os.path.join(sprite_dir, f"{sprite_name}.png"))
    
    frames_meta = []
    keyframes_meta = []
    
    for idx, (frame_im, f_uuid) in enumerate(zip(frames_images, frame_uuids)):
        frame_im.save(os.path.join(sprite_dir, f"{f_uuid}.png"))
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
                "$KeyframeStore<MomentsEventKeyframe>":"",
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
    print(f"Created sprite: {sprite_name} ({len(frames_images)} frames at {speed} FPS)")

if __name__ == "__main__":
    print("Processing Combat ISO Sprites...")
    combat_raw = Image.open(COMBAT_IMG)

    # 1. Idle TLC with active exhaust smoke plumes and joint flex (Row 0, 4 frames)
    idle_frames = [extract_bfs(combat_raw.crop((c*256, 0*256, (c+1)*256, 1*256)), tolerance=22) for c in range(4)]
    create_sprite_resource("spr_ms_ironclad_idle", idle_frames, speed=6.0)

    # 2. Firing GAU-88 Rotary Heavy Vulcan on RIGHT ARM ONLY (Row 1, 4 frames)
    chaingun_frames = [extract_bfs(combat_raw.crop((c*256, 1*256, (c+1)*256, 2*256)), tolerance=22) for c in range(4)]
    create_sprite_resource("spr_ms_ironclad_fire_chaingun", chaingun_frames, speed=12.0)

    # 3. Launching Ares Swarm-16 Missiles (Row 3, 4 frames)
    missile_frames = [extract_bfs(combat_raw.crop((c*256, 3*256, (c+1)*256, 4*256)), tolerance=22) for c in range(4)]
    create_sprite_resource("spr_ms_ironclad_fire_missiles", missile_frames, speed=8.0)

    print("Processing Specialized Damage Type ISO Sprites...")
    damage_raw = Image.open(DAMAGE_IMG)

    # Kinetic Ammo Hit Reaction & Sustained Damage (Row 0)
    kinetic_frames = [extract_bfs(damage_raw.crop((c*256, 0*256, (c+1)*256, 1*256)), tolerance=24) for c in range(4)]
    create_sprite_resource("spr_ms_ironclad_hit_kinetic", kinetic_frames, speed=8.0)
    create_sprite_resource("spr_ms_ironclad_damage_kinetic", [kinetic_frames[3]], speed=1.0)

    # Energy Weapon Hit Reaction & Sustained Slag (Row 1)
    energy_frames = [extract_bfs(damage_raw.crop((c*256, 1*256, (c+1)*256, 2*256)), tolerance=24) for c in range(4)]
    create_sprite_resource("spr_ms_ironclad_hit_energy", energy_frames, speed=8.0)
    create_sprite_resource("spr_ms_ironclad_damage_energy", [energy_frames[3]], speed=1.0)

    # Rocket Explosion Hit Reaction & Blast Crater (Row 2)
    rocket_frames = [extract_bfs(damage_raw.crop((c*256, 2*256, (c+1)*256, 3*256)), tolerance=24) for c in range(4)]
    create_sprite_resource("spr_ms_ironclad_hit_rocket", rocket_frames, speed=8.0)
    create_sprite_resource("spr_ms_ironclad_damage_rocket", [rocket_frames[3]], speed=1.0)

    # Melee Weapon Hit Reaction & Thermal Slash Scar (Row 3)
    melee_frames = [extract_bfs(damage_raw.crop((c*256, 3*256, (c+1)*256, 4*256)), tolerance=24) for c in range(4)]
    create_sprite_resource("spr_ms_ironclad_hit_melee", melee_frames, speed=8.0)
    create_sprite_resource("spr_ms_ironclad_damage_melee", [melee_frames[3]], speed=1.0)

    print("Processing Component Severing & Destruction Sprites...")
    dmg_iso_raw = Image.open(DMG_ISO_IMG)
    SCALE_DMG = 239.0 / 301.0

    def format_damage_frame(crop_box, anchor_offset_y=0):
        crop = dmg_iso_raw.crop(crop_box)
        trans = extract_bfs(crop, tolerance=24)
        bbox = trans.getbbox()
        if bbox:
            trans = trans.crop(bbox)
        tw, th = trans.size
        nw = max(1, int(tw * SCALE_DMG))
        nh = max(1, int(th * SCALE_DMG))
        resized = trans.resize((nw, nh), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        paste_x = (CANVAS_W - nw) // 2
        paste_y = max(0, (ORIGIN_Y - nh) + anchor_offset_y)
        canvas.paste(resized, (paste_x, paste_y), resized)
        return canvas

    spr_la = [format_damage_frame((710, 0, 990, 325))]
    create_sprite_resource("spr_ms_ironclad_damage_left_arm", spr_la, speed=1.0)

    spr_ra = [format_damage_frame((370, 0, 650, 325))]
    create_sprite_resource("spr_ms_ironclad_damage_right_arm", spr_ra, speed=1.0)

    spr_crip = [format_damage_frame((350, 420, 680, 705), anchor_offset_y=0)]
    create_sprite_resource("spr_ms_ironclad_crippled", spr_crip, speed=1.0)

    spr_dest = [format_damage_frame((690, 380, 1010, 705), anchor_offset_y=0)]
    create_sprite_resource("spr_ms_ironclad_destroyed", spr_dest, speed=1.0)

    print("All isometric sprites updated successfully!")
