"""
Import Task 1 Art Assets: 3 Unarmed Base Chassis & 3 Starter Weapon Overlays.
Extracts pure transparent backgrounds via corner-seeded BFS, standardizes to
160x160 GameMaker Studio 2 v2 sprites, generates 4-frame hydraulic idle cycles
for the 3 chassis, writes .yy metadata, and registers all 6 sprites in MechMakerConcept.yyp.
"""

import os
import json
import uuid
from collections import deque
from PIL import Image

CANVAS_W = 160
CANVAS_H = 160

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BRAIN_DIR = r"C:\Users\thoma\.gemini\antigravity\brain\f369c652-2a1f-4a4b-b96b-2d843940c98d"

CHASSIS_ASSETS = [
    {
        "name": "spr_ms_pmc_aegis_visor",
        "src": os.path.join(BRAIN_DIR, "aegis_visor_base_wanzer_1794579404981.jpg"),
        "flip_x": False,
    },
    {
        "name": "spr_ms_pmc_colossus_forge",
        "src": os.path.join(BRAIN_DIR, "colossus_heavy_dreadnought_sprite_1794579403087.jpg"),
        "flip_x": True,  # Standardize to 3/4 front-right facing (xscale = 1)
    },
    {
        "name": "spr_ms_pmc_stratos_vector",
        "src": os.path.join(BRAIN_DIR, "stratos_vector_recon_chassis_1794579406414.jpg"),
        "flip_x": False,
    },
    {
        "name": "spr_ms_pmc_aegis_visor_back_idle",
        "src": os.path.join(BRAIN_DIR, "aegis_visor_rear_view_1794581909847.jpg"),
        "flip_x": False,
    },
    {
        "name": "spr_ms_pmc_colossus_forge_back_idle",
        "src": os.path.join(BRAIN_DIR, "colossus_dreadnought_rear_34_1794581908334.jpg"),
        "flip_x": False,
    },
    {
        "name": "spr_ms_pmc_stratos_vector_back_idle",
        "src": os.path.join(BRAIN_DIR, "stratos_vector_rear_1794581905631.jpg"),
        "flip_x": False,
    },
]

WEAPON_ASSETS = [
    {
        "name": "spr_wpn_starter_mg_90",
        "src": os.path.join(BRAIN_DIR, "type90_machine_gun_sprite_1794579410286.jpg"),
        "flip_x": False,
    },
    {
        "name": "spr_wpn_heat_hawk",
        "src": os.path.join(BRAIN_DIR, "heat_axe_sprite_1794579409729.jpg"),
        "flip_x": False,
    },
    {
        "name": "spr_wpn_ballistic_buckler",
        "src": os.path.join(BRAIN_DIR, "type1_ballistic_deflector_buckler_1794579412327.jpg"),
        "flip_x": False,
    },
]


def extract_transparent_bg(im: Image.Image, tolerance: int = 32) -> Image.Image:
    """Corner-seeded BFS flood-fill to remove flat light/white background cleanly."""
    im = im.convert("RGBA")
    w, h = im.size
    pixels = im.load()

    bg_r, bg_g, bg_b, _ = pixels[0, 0]
    tol_sq = tolerance * tolerance

    visited = set()
    queue = deque()

    def is_bg(r, g, b):
        return (r - bg_r) ** 2 + (g - bg_g) ** 2 + (b - bg_b) ** 2 <= tol_sq

    for x in range(w):
        for y in (0, h - 1):
            r, g, b, _ = pixels[x, y]
            if is_bg(r, g, b):
                visited.add((x, y))
                queue.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if (x, y) not in visited:
                r, g, b, _ = pixels[x, y]
                if is_bg(r, g, b):
                    visited.add((x, y))
                    queue.append((x, y))

    while queue:
        cx, cy = queue.popleft()
        pixels[cx, cy] = (0, 0, 0, 0)
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                r, g, b, _ = pixels[nx, ny]
                if is_bg(r, g, b):
                    visited.add((nx, ny))
                    queue.append((nx, ny))

    return im


def fit_grounded_chassis(im: Image.Image, max_w: int = 138, max_h: int = 132, origin_y: int = 145) -> Image.Image:
    """Crop to tight bounding box and anchor feet at origin_y on 160x160 canvas."""
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    cw, ch = im.size
    scale = min(float(max_w) / max(1, cw), float(max_h) / max(1, ch))
    nw = max(1, int(round(cw * scale)))
    nh = max(1, int(round(ch * scale)))

    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    paste_x = (CANVAS_W - nw) // 2
    paste_y = max(4, origin_y - nh)
    canvas.paste(resized, (paste_x, paste_y), resized)
    return canvas


def build_hydraulic_idle_frames(base_frame: Image.Image) -> list[Image.Image]:
    """
    Create a 4-frame hydraulic idle cycle (Neutral -> Compress 1px -> Hold/Pulse -> Recover)
    while keeping lower feet anchored at y=145.
    """
    split_y = 112  # Keep boots/ankles anchored; upper torso/legs compress smoothly
    upper = base_frame.crop((0, 0, CANVAS_W, split_y))
    lower = base_frame.crop((0, split_y, CANVAS_W, CANVAS_H))

    def make_compressed(dy: int) -> Image.Image:
        frame = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        frame.paste(lower, (0, split_y), lower)
        frame.paste(upper, (0, dy), upper)
        return frame

    frame0 = base_frame.copy()
    frame1 = make_compressed(1)
    frame2 = make_compressed(2)
    frame3 = make_compressed(1)
    return [frame0, frame1, frame2, frame3]


def fit_centered_overlay(im: Image.Image, max_dim: int = 96) -> Image.Image:
    """Crop weapon/shield overlay and center at (80, 80) on 160x160 canvas."""
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    cw, ch = im.size
    scale = min(float(max_dim) / max(1, cw), float(max_dim) / max(1, ch))
    nw = max(1, int(round(cw * scale)))
    nh = max(1, int(round(ch * scale)))

    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    paste_x = (CANVAS_W - nw) // 2
    paste_y = (CANVAS_H - nh) // 2
    canvas.paste(resized, (paste_x, paste_y), resized)
    return canvas


def write_gm_sprite(sprite_name: str, frames: list[Image.Image], xorigin: int, yorigin: int, speed: float):
    """Write GameMaker v2 sprite directory, frame PNGs, layer PNGs, strip PNG, and .yy JSON."""
    sprite_dir = os.path.join(PROJECT_DIR, "sprites", sprite_name)
    layers_dir = os.path.join(sprite_dir, "layers")
    os.makedirs(sprite_dir, exist_ok=True)
    os.makedirs(layers_dir, exist_ok=True)

    layer_uuid = str(uuid.uuid4())
    frame_uuids = [str(uuid.uuid4()) for _ in frames]

    # Preview PNG
    frames[0].save(os.path.join(sprite_dir, f"{sprite_name}.png"))

    # Horizontal strip PNG if multi-frame
    if len(frames) > 1:
        strip = Image.new("RGBA", (CANVAS_W * len(frames), CANVAS_H), (0, 0, 0, 0))
        for i, fr in enumerate(frames):
            strip.paste(fr, (i * CANVAS_W, 0), fr)
        strip.save(os.path.join(sprite_dir, f"{sprite_name}_strip{len(frames)}.png"))

    frames_meta = []
    keyframes_meta = []

    for idx, (frame_im, f_uuid) in enumerate(zip(frames, frame_uuids)):
        frame_im.save(os.path.join(sprite_dir, f"{f_uuid}.png"))
        f_layer_dir = os.path.join(layers_dir, f_uuid)
        os.makedirs(f_layer_dir, exist_ok=True)
        frame_im.save(os.path.join(f_layer_dir, f"{layer_uuid}.png"))

        frames_meta.append({
            "$GMSpriteFrame": "v1",
            "%Name": f_uuid,
            "name": f_uuid,
            "resourceType": "GMSpriteFrame",
            "resourceVersion": "2.0",
        })

        keyframes_meta.append({
            "$Keyframe<SpriteFrameKeyframe>": "",
            "Channels": {
                "0": {
                    "$SpriteFrameKeyframe": "",
                    "Id": {
                        "name": f_uuid,
                        "path": f"sprites/{sprite_name}/{sprite_name}.yy",
                    },
                    "resourceType": "SpriteFrameKeyframe",
                    "resourceVersion": "2.0",
                }
            },
            "Disabled": False,
            "id": str(uuid.uuid4()),
            "IsCreationKey": False,
            "Key": float(idx),
            "Length": 1.0,
            "resourceType": "Keyframe<SpriteFrameKeyframe>",
            "resourceVersion": "2.0",
            "Stretch": False,
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
                "visible": True,
            }
        ],
        "name": sprite_name,
        "nineSlice": None,
        "origin": 9,
        "parent": {
            "name": "Sprites",
            "path": "folders/Sprites.yy",
        },
        "preMultiplyAlpha": False,
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
                "resourceVersion": "2.0",
            },
            "eventStubScript": None,
            "eventToFunction": {},
            "length": float(len(frames)),
            "lockOrigin": False,
            "moments": {
                "$KeyframeStore<MomentsEventKeyframe>": "",
                "Keyframes": [],
                "resourceType": "KeyframeStore<MomentsEventKeyframe>",
                "resourceVersion": "2.0",
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
                        "resourceVersion": "2.0",
                    },
                    "modifiers": [],
                    "name": "frames",
                    "resourceType": "GMSpriteFramesTrack",
                    "resourceVersion": "2.0",
                    "spriteId": None,
                    "trackColour": 0,
                    "tracks": [],
                    "traits": 0,
                }
            ],
            "visibleRange": None,
            "volume": 1.0,
            "xorigin": xorigin,
            "yorigin": yorigin,
        },
        "swatchColours": None,
        "swfPrecision": 2.525,
        "textureGroupId": {
            "name": "Default",
            "path": "texturegroups/Default",
        },
        "type": 0,
        "VTile": False,
        "width": CANVAS_W,
    }

    yy_path = os.path.join(sprite_dir, f"{sprite_name}.yy")
    with open(yy_path, "w", encoding="utf-8") as f:
        json.dump(yy_data, f, indent=2)


def register_sprites_in_yyp(sprite_names: list[str]):
    """Register new sprites in MechMakerConcept.yyp cleanly without duplicates."""
    yyp_path = os.path.join(PROJECT_DIR, "MechMakerConcept.yyp")
    with open(yyp_path, "r", encoding="utf-8") as f:
        raw = f.read()

    # Strip trailing commas for Python json.loads if GameMaker trailing commas exist
    import re
    clean_json = re.sub(r",(\s*[}\]])", r"\1", raw)
    yyp_data = json.loads(clean_json)

    existing = {res["id"]["name"] for res in yyp_data.get("resources", [])}
    added = []
    for name in sprite_names:
        if name not in existing:
            yyp_data["resources"].append({
                "id": {
                    "name": name,
                    "path": f"sprites/{name}/{name}.yy",
                }
            })
            existing.add(name)
            added.append(name)

    if added:
        yyp_data["resources"].sort(key=lambda r: r["id"]["path"])
        with open(yyp_path, "w", encoding="utf-8") as f:
            json.dump(yyp_data, f, indent=2)
    return added


def main():
    imported_names = []

    print("=== Importing 3 Unarmed Base Chassis (160x160, Origin 80,145, 4-Frame Idle) ===")
    for item in CHASSIS_ASSETS:
        im = Image.open(item["src"])
        if item["flip_x"]:
            im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        im = extract_transparent_bg(im)
        base_frame = fit_grounded_chassis(im)
        frames = build_hydraulic_idle_frames(base_frame)
        write_gm_sprite(item["name"], frames, xorigin=80, yorigin=145, speed=6.0)
        imported_names.append(item["name"])
        print(f"  [OK] {item['name']} (4 frames, 160x160, origin 80,145)")

    print("\n=== Importing 3 Starter Weapon Overlays (160x160, Origin 80,80) ===")
    for item in WEAPON_ASSETS:
        im = Image.open(item["src"])
        if item["flip_x"]:
            im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        im = extract_transparent_bg(im)
        frame = fit_centered_overlay(im)
        write_gm_sprite(item["name"], [frame], xorigin=80, yorigin=80, speed=0.0)
        imported_names.append(item["name"])
        print(f"  [OK] {item['name']} (1 frame, 160x160, origin 80,80)")

    added = register_sprites_in_yyp(imported_names)
    print(f"\nRegistered {len(added)} new sprites in MechMakerConcept.yyp: {added}")


if __name__ == "__main__":
    main()

