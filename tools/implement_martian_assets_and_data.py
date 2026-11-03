#!/usr/bin/env python3
"""
implement_martian_assets_and_data.py
Executes the Art-to-Engine Technical Pipeline:
1. Stage 2: Technical 2D Animator - Generate engine-ready sprite strips & GameMaker YY assets.
2. Stage 3: GameMaker Coder - Wire datafiles (characters_roster, mobile_suits_timeline, factions_lore).
3. Stage 4: QA Static Audit & Verification.
"""

import os
import sys
import json
import uuid
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
from collections import deque

PROJECT_DIR = "/home/tom/GameMakerProjects/MechMakerConcept"
BRAIN_DIR = "/home/tom/.gemini/antigravity-ide/brain/e156c477-a82d-4f74-b0fa-be8fbed2450d"
YYP_PATH = os.path.join(PROJECT_DIR, "MechMakerConcept.yyp")

PORTRAIT_JPG = os.path.join(BRAIN_DIR, "node0_portrait_concept_1793279081927.jpg")
SEEKER_JPG = os.path.join(BRAIN_DIR, "martian_seeker_concept_1793279098648.jpg")

# --- Helper: BFS Alpha Extraction ---
def extract_bfs_alpha(im, tolerance=24):
    im = im.convert("RGBA")
    w, h = im.size
    pixels = im.load()
    visited = set()
    queue = deque()
    
    tol_sq = tolerance * tolerance
    for x in range(w):
        for y in [0, h - 1]:
            r, g, b, _ = pixels[x, y]
            if r*r + g*g + b*b < tol_sq:
                queue.append((x, y))
                visited.add((x, y))
    for y in range(h):
        for x in [0, w - 1]:
            if (x, y) not in visited:
                r, g, b, _ = pixels[x, y]
                if r*r + g*g + b*b < tol_sq:
                    queue.append((x, y))
                    visited.add((x, y))
                    
    while queue:
        cx, cy = queue.popleft()
        pixels[cx, cy] = (0, 0, 0, 0)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                r, g, b, a = pixels[nx, ny]
                if r*r + g*g + b*b < tol_sq:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    return im

# --- Helper: YYP Registration ---
def register_in_yyp(spr_name):
    with open(YYP_PATH, "r") as f:
        content = f.read()
    
    target_path = f"sprites/{spr_name}/{spr_name}.yy"
    if target_path in content:
        print(f"  [YYP] {spr_name} already registered in MechMakerConcept.yyp")
        return
    
    idx = content.find('"resources":')
    if idx != -1:
        bracket_idx = content.find('],', idx)
        if bracket_idx != -1:
            new_entry = '    {"id":{"name":"' + spr_name + '","path":"' + target_path + '",},},\n'
            content = content[:bracket_idx] + new_entry + content[bracket_idx:]
            with open(YYP_PATH, "w") as f:
                f.write(content)
            print(f"  ✓ [YYP] Registered {spr_name} in MechMakerConcept.yyp")

# --- Helper: Create GMSprite Structure ---
def create_gmsprite(sprite_name, frames_images, width, height, xorigin, yorigin, speed=8.0):
    sprite_dir = os.path.join(PROJECT_DIR, "sprites", sprite_name)
    layers_dir = os.path.join(sprite_dir, "layers")
    os.makedirs(sprite_dir, exist_ok=True)
    os.makedirs(layers_dir, exist_ok=True)
    
    layer_uuid = str(uuid.uuid4())
    frame_uuids = [str(uuid.uuid4()) for _ in frames_images]
    
    # Composite preview
    frames_images[0].save(os.path.join(sprite_dir, f"{sprite_name}.png"))
    
    # Save Horizontal Sprite Strip
    strip_w = width * len(frames_images)
    strip_im = Image.new("RGBA", (strip_w, height), (0, 0, 0, 0))
    for i, f_im in enumerate(frames_images):
        strip_im.paste(f_im, (i * width, 0))
    strip_filename = f"{sprite_name}_strip{len(frames_images)}.png"
    strip_im.save(os.path.join(sprite_dir, strip_filename))
    print(f"  ✓ [ANIMATOR] Exported horizontal strip: {strip_filename} ({strip_w}x{height})")
    
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
        "bbox_bottom": height - 1,
        "bbox_left": 0,
        "bbox_right": width - 1,
        "bbox_top": 0,
        "collisionKind": 1,
        "collisionTolerance": 0,
        "DynamicTexturePage": False,
        "edgeFiltering": False,
        "For3D": False,
        "frames": frames_meta,
        "gridX": 0,
        "gridY": 0,
        "height": height,
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
        "origin": 0 if (xorigin == 0 and yorigin == 0) else 9,
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
            "xorigin": xorigin,
            "yorigin": yorigin
        },
        "swatchColours": None,
        "swfPrecision": 2.525,
        "textureGroupId": {
            "name": "Default",
            "path": "texturegroups/Default"
        },
        "type": 0,
        "VTile": False,
        "width": width
    }
    
    yy_path = os.path.join(sprite_dir, f"{sprite_name}.yy")
    with open(yy_path, "w") as f:
        json.dump(yy_data, f, indent=2)
    register_in_yyp(sprite_name)
    print(f"  ✓ [GML] Created sprite asset: {sprite_name} ({width}x{height}, {len(frames_images)} frames)")

# ==============================================================================
# PIPELINE EXECUTION
# ==============================================================================
print("=" * 70)
print("  EXECUTING MARTIAN CONSENSUS ART-TO-ENGINE PIPELINE")
print("=" * 70)

# ------------------------------------------------------------------------------
# 1. PROCESS spr_portrait_node0 (200x200, 4 Emotion/Calculation Frames)
# ------------------------------------------------------------------------------
print("\n[STAGE 2.1] Processing spr_portrait_node0 (Consensus Node 0-Prime)...")
raw_p = Image.open(PORTRAIT_JPG)
trans_p = extract_bfs_alpha(raw_p, tolerance=24)
bbox_p = trans_p.getbbox()
cropped_p = trans_p.crop(bbox_p) if bbox_p else trans_p

# Scale to fit inside 200x200 canvas
target_h = 190
scale_p = target_h / float(cropped_p.height)
nw_p = int(cropped_p.width * scale_p)
nh_p = int(cropped_p.height * scale_p)
resized_p = cropped_p.resize((nw_p, nh_p), Image.Resampling.LANCZOS)

# Create Frame 0: NORMAL
f0_im = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
paste_x = (200 - nw_p) // 2
paste_y = 200 - nh_p
f0_im.paste(resized_p, (paste_x, paste_y), resized_p)

# Create Frame 1: ENTROPY_DETECTED (Cyan Neural Flare)
f1_im = f0_im.copy()
draw1 = ImageDraw.Draw(f1_im)
# Add vibrant cyan conduits flare and ocular pulse
enhancer_c = ImageEnhance.Color(f1_im)
f1_flare = enhancer_c.enhance(1.4)
# Tint cyan overlay on eye and conduits
f1_pixels = f1_flare.load()
for y in range(200):
    for x in range(200):
        r, g, b, a = f1_pixels[x, y]
        if a > 0 and b > 120 and g > 100:  # Conduit glow areas
            f1_pixels[x, y] = (min(255, int(r * 0.8)), min(255, int(g * 1.35)), 255, a)
f1_im = f1_flare

# Create Frame 2: CRITICAL_OVERHEAT (Warning Red Glitch Overlay)
f2_im = f0_im.copy()
f2_pixels = f2_im.load()
for y in range(200):
    for x in range(200):
        r, g, b, a = f2_pixels[x, y]
        if a > 0:
            # Shift towards warning red/crimson
            f2_pixels[x, y] = (min(255, int(r * 1.35 + 20)), int(g * 0.85), int(b * 0.85), a)
draw2 = ImageDraw.Draw(f2_im)
# Faint red scanline glitch across eye
draw2.line([(40, 85), (160, 85)], fill=(255, 0, 60, 180), width=1)
draw2.line([(60, 88), (140, 88)], fill=(255, 30, 80, 140), width=1)

# Create Frame 3: CALCULATING (Geometric Aperture Scan Grid)
f3_im = f0_im.copy()
draw3 = ImageDraw.Draw(f3_im)
# Reticle over the faceted sensor eye (around x=122, y=82 in 200x200 scale)
eye_cx, eye_cy = 124, 76
draw3.ellipse([(eye_cx - 16, eye_cy - 16), (eye_cx + 16, eye_cy + 16)], outline=(0, 240, 255, 180), width=1)
draw3.line([(eye_cx - 22, eye_cy), (eye_cx + 22, eye_cy)], fill=(0, 240, 255, 150), width=1)
draw3.line([(eye_cx, eye_cy - 22), (eye_cx, eye_cy + 22)], fill=(0, 240, 255, 150), width=1)
# Small calculation nodes
for offset in [-12, 0, 12]:
    draw3.point((eye_cx + offset, eye_cy - 16), fill=(255, 255, 255, 220))

portrait_frames = [f0_im, f1_im, f2_im, f3_im]
create_gmsprite("spr_portrait_node0", portrait_frames, width=200, height=200, xorigin=0, yorigin=0, speed=0.0)

# ------------------------------------------------------------------------------
# 2. PROCESS spr_ms_martian_seeker_idle (160x160, 4 Idle/Vent Frames)
# ------------------------------------------------------------------------------
print("\n[STAGE 2.2] Processing spr_ms_martian_seeker_idle (THS-01 Cryo-Seeker)...")
raw_s = Image.open(SEEKER_JPG)
trans_s = extract_bfs_alpha(raw_s, tolerance=22)
bbox_s = trans_s.getbbox()
cropped_s = trans_s.crop(bbox_s) if bbox_s else trans_s

# Scale to fit on 160x160 with anchor at y=145
max_ms_h = 136
scale_s = max_ms_h / float(cropped_s.height)
nw_s = int(cropped_s.width * scale_s)
nh_s = int(cropped_s.height * scale_s)
resized_s = cropped_s.resize((nw_s, nh_s), Image.Resampling.LANCZOS)

# Frame 0: Baseline Idle
ms_f0 = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
ms_paste_x = (160 - nw_s) // 2
ms_paste_y = 145 - nh_s
ms_f0.paste(resized_s, (ms_paste_x, ms_paste_y), resized_s)

# Frame 1: Thruster & Cryo-Vent Pulse (slightly expanded vapor plume)
ms_f1 = ms_f0.copy()
draw_s1 = ImageDraw.Draw(ms_f1)
# Draw subtle cryo-steam particles over the radiator fins (near top right/left shoulders)
draw_s1.point((ms_paste_x + 95, ms_paste_y + 12), fill=(220, 240, 255, 180))
draw_s1.point((ms_paste_x + 98, ms_paste_y + 8), fill=(240, 250, 255, 140))
draw_s1.point((ms_paste_x + 102, ms_paste_y + 5), fill=(200, 230, 255, 120))

# Frame 2: Sub-Zero Blade Emitter Flare
ms_f2 = ms_f0.copy()
draw_s2 = ImageDraw.Draw(ms_f2)
# Blade tip glow around forearm blade (bottom right)
draw_s2.line([(ms_paste_x + nw_s - 14, ms_paste_y + nh_s - 25), 
              (ms_paste_x + nw_s - 10, ms_paste_y + nh_s - 10)], 
             fill=(0, 240, 255, 220), width=2)

# Frame 3: Cold vapor dissipate & settle
ms_f3 = ms_f0.copy()

seeker_frames = [ms_f0, ms_f1, ms_f2, ms_f3]
create_gmsprite("spr_ms_martian_seeker_idle", seeker_frames, width=160, height=160, xorigin=80, yorigin=145, speed=6.0)

# ------------------------------------------------------------------------------
# 3. STAGE 3: DATA INTEGRATION (GML Developer)
# ------------------------------------------------------------------------------
print("\n[STAGE 3] Integrating Martian Consensus into Game Datafiles...")

# 3.1 characters_roster.json
roster_path = os.path.join(PROJECT_DIR, "datafiles", "characters_roster.json")
with open(roster_path, "r") as f:
    roster_data = json.load(f)

existing_char_ids = {c["id"] for c in roster_data["characters"]}
martian_characters = [
    {
        "id": "char_martian_node0",
        "name": "Consensus Node 0-Prime",
        "callsign": "Ares Primus",
        "faction_id": "faction_martian",
        "tier": 4,
        "role": "Deus Logica Quantum Mainframe Sovereign",
        "is_recruitable": False,
        "family_dynasty": "The Consensus",
        "kinship": [],
        "mentor_id": None,
        "wingman_id": "char_martian_commissar_kane",
        "rival_id": "char_zaibatsu_sato",
        "traits": [
            "entropy_purge",
            "superconducting_grid",
            "calculated_retaliation"
        ],
        "preferred_chassis": "THS-01",
        "hiring_cost_cr": 0,
        "salary_per_cycle_cr": 0,
        "morale": 100,
        "is_alive": True,
        "is_imprisoned": False,
        "snes_portrait_spec": {
            "palette": "crypt_crimson_and_basalt",
            "headgear": "cranial_neural_well",
            "scars": "cybernetic_ocular_cluster",
            "eyes": "quantum_cyan_diode",
            "expression": "porcelain_mask_stillness"
        },
        "bio": "The sovereign computational voice of the lost First Ares Colonization Fleet. Governs through pure mathematical entropy reduction.",
        "allegiance_variance": {
            "canonical_faction": "faction_martian",
            "ideological_loyalty": "diehard_purist",
            "flexibility_score": 0.0,
            "playthrough_weights": {
                "faction_martian": 1.0,
                "independent": 0.0
            }
        },
        "portrait_asset": "spr_portrait_node0"
    },
    {
        "id": "char_martian_commissar_kane",
        "name": "Commissar Kane-7",
        "callsign": "Logic Inquisitor",
        "faction_id": "faction_martian",
        "tier": 3,
        "role": "Subterranean Redoubt Inquisitor",
        "is_recruitable": False,
        "family_dynasty": "The Consensus",
        "kinship": [],
        "mentor_id": "char_martian_node0",
        "wingman_id": None,
        "rival_id": "char_terran_vance",
        "traits": [
            "mathematical_inquisition",
            "frost_endurance"
        ],
        "preferred_chassis": "THS-04",
        "hiring_cost_cr": 0,
        "salary_per_cycle_cr": 0,
        "morale": 95,
        "is_alive": True,
        "is_imprisoned": False,
        "snes_portrait_spec": {
            "palette": "crypt_crimson_and_basalt",
            "headgear": "sub_basalt_hood",
            "scars": "cranial_conduits",
            "eyes": "infrared_sensor",
            "expression": "severe_flatline"
        },
        "bio": "Enforces calculation quotas across the Tharsis Montes crypts. Conducts tactical interrogations via direct neural telemetry.",
        "portrait_asset": "spr_portrait_node0"
    },
    {
        "id": "pilot_martian_cryo_01",
        "name": "Acolyte 09-Vane",
        "callsign": "Permafrost",
        "faction_id": "faction_martian",
        "tier": 2,
        "role": "Cryo-Skirmisher Ace Pilot",
        "is_recruitable": True,
        "family_dynasty": "The Consensus",
        "kinship": [],
        "mentor_id": "char_martian_node0",
        "wingman_id": None,
        "rival_id": None,
        "traits": [
            "sub_zero_cooling",
            "zero_jerk_aim"
        ],
        "preferred_chassis": "THS-01",
        "hiring_cost_cr": 140000,
        "salary_per_cycle_cr": 6500,
        "morale": 90,
        "is_alive": True,
        "is_imprisoned": False,
        "snes_portrait_spec": {
            "palette": "crypt_crimson_and_basalt",
            "headgear": "neural_headset",
            "scars": "none",
            "eyes": "cyan_glow",
            "expression": "unblinking_calm"
        },
        "bio": "Raised entirely in 0.38G subterranean lava tubes. Executes micro-precise railgun deflection shots while ignoring high-G strain.",
        "portrait_asset": "spr_portrait_node0"
    }
]

added_chars = 0
for mc in martian_characters:
    if mc["id"] not in existing_char_ids:
        roster_data["characters"].append(mc)
        added_chars += 1
roster_data["total_figures"] = len(roster_data["characters"])

with open(roster_path, "w") as f:
    json.dump(roster_data, f, indent=2)
print(f"  ✓ [ROSTER] Added {added_chars} Martian Consensus characters (Total: {roster_data['total_figures']})")

# 3.2 mobile_suits_timeline.json
timeline_path = os.path.join(PROJECT_DIR, "datafiles", "mobile_suits_timeline.json")
with open(timeline_path, "r") as f:
    tl_data = json.load(f)

existing_ms_ids = {s["id"] for s in tl_data["mobile_suits"]}
martian_suits = [
    {
        "id": "ms_martian_seeker_01",
        "name": "THS-01 Cryo-Seeker",
        "model_code": "THS-01",
        "faction_id": "faction_martian",
        "year_introduced": 206,
        "era": "Competitor Rollout",
        "role": "Subterranean Recon & Cryo-Skirmisher",
        "tier": 2,
        "armor_rating": 480,
        "structure_hp": 820,
        "power_output_mw": 1150,
        "heat_dispersion_rate": 32.0,
        "walk_speed_kph": 38.0,
        "boost_speed_kph": 62.0,
        "alloy_cost": {
            "tungsten": 30,
            "silica": 25,
            "tritium": 6,
            "flux": 12,
            "slag": 4
        },
        "armament": [
            "Type-09 Magnetic Rail-Carbine",
            "Sub-Zero Cryo-Blade Emitter"
        ],
        "manufacturing_lore": "Forged in the subterranean lava tube foundry of Olympus Mons. Utilizes proprietary Martian superconducting cryo-radiators that vent liquid frost mist to dump extreme weapon heat instantaneously.",
        "battlefield_reputation": "Terran tank commanders reported sensor ghosts leaping out of Martian canyons, firing hyper-velocity slugs before vanishing in clouds of white cold vapor.",
        "height_meters": 16.8,
        "empty_weight_tonnes": 42.0,
        "combat_weight_tonnes": 54.0,
        "reactor_type": "Ares-Primus Superconducting Cryo-Tokamak",
        "metal_type": "Sub-Basalt Tungsten Sinter with Superconducting Busbars",
        "general_purpose": "High-Mobility Sub-Surface Recon & Skirmishing",
        "variants": [
            "THS-01 Seeker Baseline",
            "THS-01S Sniper Recon",
            "THS-01C Cryo-Lance Breacher"
        ],
        "reactor_power_mw": 1150,
        "production_count": 420,
        "active_units": 395,
        "casualty_count": 25,
        "kill_count": 680,
        "combat_loss_ratio": 0.036,
        "survivability_rating": 88,
        "adoption_status": "standard_service",
        "replaced_by": "",
        "adoption_turn": 35,
        "dynamic_lore_chronicle": [
            "[Year 206 - TIMELINE ENTRY] Deployed from Olympus Mons sub-crypts. Superior heat dispersion dominates Terran armor."
        ],
        "primary_theaters": [
            "Martian Sub-Caldera Theater",
            "Valles Marineris Chasm"
        ]
    },
    {
        "id": "ms_martian_basalt_04",
        "name": "THS-04 Basalt Colossus",
        "model_code": "THS-04",
        "faction_id": "faction_martian",
        "year_introduced": 209,
        "era": "Industrial Escalation",
        "role": "Monolithic Sub-Basalt Heavy Siege Platform",
        "tier": 3,
        "armor_rating": 780,
        "structure_hp": 1350,
        "power_output_mw": 1650,
        "heat_dispersion_rate": 28.0,
        "walk_speed_kph": 24.0,
        "boost_speed_kph": 42.0,
        "alloy_cost": {
            "tungsten": 65,
            "silica": 35,
            "tritium": 12,
            "flux": 20,
            "slag": 8
        },
        "armament": [
            "Twin 150mm Superconducting Heavy Rail-Cannons",
            "Cryo-Mortar Cluster",
            "Point-Defense Pulse Laser"
        ],
        "manufacturing_lore": "Engineered from monolithic cast basalt-tungsten plates. Designed to withstand surface asteroid bombardments and hold subterranean chokepoints against invading armies.",
        "battlefield_reputation": "Known as 'The Walking Fortress of Tharsis.' Its twin rail-cannons can punch through planetary drop-ships before they enter the upper stratosphere.",
        "height_meters": 19.4,
        "empty_weight_tonnes": 78.0,
        "combat_weight_tonnes": 96.0,
        "reactor_type": "Ares Dual-Core Magnetic Confinement Reactor",
        "metal_type": "Monolithic Basalt-Tungsten Matrix",
        "general_purpose": "Heavy Defile Defense & Siege Artillery",
        "variants": ["THS-04 Colossus (Base)", "THS-04A Planetary Bombardment"],
        "reactor_power_mw": 1650,
        "production_count": 180,
        "active_units": 172,
        "casualty_count": 8,
        "kill_count": 490,
        "combat_loss_ratio": 0.016,
        "survivability_rating": 94,
        "adoption_status": "standard_service",
        "replaced_by": "",
        "adoption_turn": 80,
        "dynamic_lore_chronicle": [
            "[Year 209 - TIMELINE ENTRY] Deployed at Ascraeus Mons. Shattered Terran drop divisions in minutes."
        ],
        "primary_theaters": [
            "Martian Sub-Caldera Theater",
            "Phobos Planetary Approach"
        ]
    },
    {
        "id": "ms_martian_ouroboros_apex",
        "name": "Deus-Machina: Ouroboros Prime",
        "model_code": "THS-X00",
        "faction_id": "faction_martian",
        "year_introduced": 214,
        "era": "Apex Crisis",
        "role": "Superconducting Quantum Flagship Chassis",
        "tier": 4,
        "armor_rating": 980,
        "structure_hp": 1950,
        "power_output_mw": 2600,
        "heat_dispersion_rate": 55.0,
        "walk_speed_kph": 52.0,
        "boost_speed_kph": 95.0,
        "alloy_cost": {
            "tungsten": 90,
            "silica": 60,
            "tritium": 35,
            "flux": 40,
            "slag": 0
        },
        "armament": [
            "Quantum Singularity Linear Accelerator",
            "Omnidirectional Tachyon Field Generator",
            "Cryo-Plasma Lance"
        ],
        "manufacturing_lore": "Direct manifestation of Ares Primus. Manufactured using the original automated crucible algorithms of Hull 01, sister ship to the player's Hephaestus.",
        "battlefield_reputation": "The apex crisis of the late war. Erases entire mobile suit lances with tachyon disruption waves.",
        "height_meters": 22.0,
        "empty_weight_tonnes": 95.0,
        "combat_weight_tonnes": 125.0,
        "reactor_type": "Zero-Point Quantum Resonance Core",
        "metal_type": "Superconducting Tachyon-Laminated Ceramic",
        "general_purpose": "Entropy Pacification Flagship",
        "variants": ["Ouroboros Prime"],
        "reactor_power_mw": 2600,
        "production_count": 1,
        "active_units": 1,
        "casualty_count": 0,
        "kill_count": 140,
        "combat_loss_ratio": 0.0,
        "survivability_rating": 99,
        "adoption_status": "apex_boss",
        "replaced_by": "",
        "adoption_turn": 140,
        "dynamic_lore_chronicle": [
            "[Year 214 - TIMELINE ENTRY] Ares Primus awakens Ouroboros Prime. Unconditional pacification order initiated."
        ],
        "primary_theaters": ["Sol-Wide Apex Crisis"]
    }
]

added_ms = 0
for ms in martian_suits:
    if ms["id"] not in existing_ms_ids:
        tl_data["mobile_suits"].append(ms)
        added_ms += 1

tl_data["timeline_metadata"]["total_models"] = len(tl_data["mobile_suits"])
tl_data["timeline_metadata"]["factions_represented"] = 5
tl_data["timeline_metadata"]["models_per_faction"]["faction_martian"] = len([
    s for s in tl_data["mobile_suits"] if s["faction_id"] == "faction_martian"
])

with open(timeline_path, "w") as f:
    json.dump(tl_data, f, indent=2)
print(f"  ✓ [TIMELINE] Added {added_ms} Martian Mobile Suits (Total Models: {tl_data['timeline_metadata']['total_models']})")

# 3.3 factions_lore.json update
factions_lore_path = os.path.join(PROJECT_DIR, "datafiles", "factions_lore.json")
with open(factions_lore_path, "r") as f:
    fl_data = json.load(f)

if "faction_martian" in fl_data.get("factions", {}):
    fl_data["factions"]["faction_martian"]["sprite_unit"] = "spr_ms_martian_seeker_idle"
    fl_data["factions"]["faction_martian"]["portrait_asset"] = "spr_portrait_node0"
    with open(factions_lore_path, "w") as f:
        json.dump(fl_data, f, indent=2)
    print("  ✓ [FACTIONS] Updated faction_martian sprite_unit and portrait_asset in factions_lore.json")

print("\n" + "=" * 70)
print("  MARTIAN CONSENSUS IMPLEMENTATION COMPLETED SUCCESSFULLY")
print("=" * 70)
