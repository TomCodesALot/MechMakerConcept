#!/usr/bin/env python3
"""
tools/create_audio_architecture.py
Implements the Lead Audio Engineer and Lead Composer directives:
- Creates obj_AudioManager (Create, Step, CleanUp)
- Creates scripts/scr_audio_manager/scr_audio_manager.gml
- Registers obj_AudioManager and scr_audio_manager in MechMakerConcept.yyp
- Updates rm_init/RoomCreationCode.gml to spawn obj_AudioManager
"""

import os
import json

YYP_PATH = "MechMakerConcept.yyp"

# =============================================================================
# 1. CREATE obj_AudioManager RESOURCE & EVENTS
# =============================================================================

OBJ_DIR = "objects/obj_AudioManager"
os.makedirs(OBJ_DIR, exist_ok=True)

obj_yy = {
  "$GMObject":"",
  "%Name":"obj_AudioManager",
  "eventList":[
    {"$GMEvent":"v1","%Name":"","collisionObjectId":None,"eventNum":0,"eventType":0,"isDnD":False,"name":"","resourceType":"GMEvent","resourceVersion":"2.0"},
    {"$GMEvent":"v1","%Name":"","collisionObjectId":None,"eventNum":0,"eventType":3,"isDnD":False,"name":"","resourceType":"GMEvent","resourceVersion":"2.0"},
    {"$GMEvent":"v1","%Name":"","collisionObjectId":None,"eventNum":0,"eventType":12,"isDnD":False,"name":"","resourceType":"GMEvent","resourceVersion":"2.0"}
  ],
  "managed":True,
  "name":"obj_AudioManager",
  "overriddenProperties":[],
  "parent":{
    "name":"MechMakerConcept",
    "path":"MechMakerConcept.yyp"
  },
  "parentObjectId":None,
  "persistent":True,
  "physicsAngularDamping":0.1,
  "physicsDensity":0.5,
  "physicsFriction":0.2,
  "physicsGroup":1,
  "physicsKinematic":False,
  "physicsLinearDamping":0.1,
  "physicsObject":False,
  "physicsRestitution":0.1,
  "physicsSensor":False,
  "physicsShape":1,
  "physicsShapePoints":[],
  "physicsStartAwake":True,
  "properties":[],
  "resourceType":"GMObject",
  "resourceVersion":"2.0",
  "solid":False,
  "spriteId":None,
  "spriteMaskId":None,
  "visible":False
}

with open(os.path.join(OBJ_DIR, "obj_AudioManager.yy"), "w") as f:
    json.dump(obj_yy, f, indent=2)

create_gml = """/// @description obj_AudioManager Create Event
// Central audio director managing BGM streaming, crossfading, pitch variation, and SFX volume channels

// Audio State
master_volume = 1.0;
bgm_volume = 0.85;
sfx_volume = 0.90;

// BGM State Machine
current_bgm_asset = noone;
current_bgm_inst = noone;
target_bgm_asset = noone;
target_bgm_loop = true;
target_bgm_fade_ms = 800;

fade_state = 0; // 0: IDLE, 1: FADING_OUT, 2: FADING_IN
fade_timer = 0;
fade_duration_steps = 45; // ~0.75s at 60 FPS
fade_start_vol = 0.0;
fade_target_vol = 0.0;

// Sound cooldown / pitch history to prevent audio fatigue (Lead Audio Engineer rule)
last_played_times = {};

/// @function play_bgm(_asset, _fade_ms, _loop)
play_bgm = function(_asset, _fade_ms = 800, _loop = true) {
    if (!audio_exists(_asset)) return;
    if (current_bgm_asset == _asset && current_bgm_inst != noone && audio_is_playing(current_bgm_inst)) {
        return; // Already playing this track
    }
    target_bgm_asset = _asset;
    target_bgm_loop = _loop;
    target_bgm_fade_ms = max(100, _fade_ms);
    fade_duration_steps = max(6, floor((_fade_ms / 1000.0) * game_get_speed(gamespeed_fps)));
    
    if (current_bgm_inst != noone && audio_is_playing(current_bgm_inst)) {
        fade_state = 1; // Fade out old track first
        fade_timer = 0;
        fade_start_vol = audio_sound_get_gain(current_bgm_inst);
        fade_target_vol = 0.0;
    } else {
        // Start track immediately with fade in
        fade_state = 2;
        fade_timer = 0;
        current_bgm_asset = target_bgm_asset;
        current_bgm_inst = audio_play_sound(current_bgm_asset, 10, target_bgm_loop);
        if (current_bgm_inst != noone) {
            audio_sound_gain(current_bgm_inst, 0.0, 0);
        }
        fade_start_vol = 0.0;
        fade_target_vol = bgm_volume * master_volume;
    }
};

/// @function stop_bgm(_fade_ms)
stop_bgm = function(_fade_ms = 600) {
    if (current_bgm_inst == noone || !audio_is_playing(current_bgm_inst)) return;
    target_bgm_asset = noone;
    target_bgm_fade_ms = _fade_ms;
    fade_duration_steps = max(6, floor((_fade_ms / 1000.0) * game_get_speed(gamespeed_fps)));
    fade_state = 1;
    fade_timer = 0;
    fade_start_vol = audio_sound_get_gain(current_bgm_inst);
    fade_target_vol = 0.0;
};

/// @function play_sfx(_asset, _vol_scale, _pitch_var)
play_sfx = function(_asset, _vol_scale = 1.0, _pitch_var = 0.0) {
    if (!audio_exists(_asset)) return noone;
    
    var _key = audio_get_name(_asset);
    var _now = current_time;
    // Debounce identical sound triggers within 25ms to avoid ear clipping
    if (variable_struct_exists(last_played_times, _key)) {
        if (_now - last_played_times[$ _key] < 25) {
            return noone;
        }
    }
    last_played_times[$ _key] = _now;
    
    // Pitch randomization (+/- _pitch_var)
    var _pitch = 1.0;
    if (_pitch_var > 0.0) {
        _pitch = 1.0 + random_range(-_pitch_var, _pitch_var);
    }
    
    var _gain = clamp(_vol_scale * sfx_volume * master_volume, 0.0, 1.0);
    var _inst = audio_play_sound(_asset, 5, false);
    if (_inst != noone) {
        audio_sound_pitch(_inst, _pitch);
        audio_sound_gain(_inst, _gain, 0);
    }
    return _inst;
};
"""

with open(os.path.join(OBJ_DIR, "Create_0.gml"), "w") as f:
    f.write(create_gml)

step_gml = """/// @description obj_AudioManager Step Event
// Smooth crossfading logic for background music

if (fade_state == 1) {
    // Fading OUT current track
    fade_timer += 1;
    var _progress = clamp(fade_timer / fade_duration_steps, 0.0, 1.0);
    var _cur_vol = lerp(fade_start_vol, fade_target_vol, _progress);
    
    if (current_bgm_inst != noone && audio_is_playing(current_bgm_inst)) {
        audio_sound_gain(current_bgm_inst, _cur_vol, 0);
    }
    
    if (_progress >= 1.0) {
        if (current_bgm_inst != noone && audio_is_playing(current_bgm_inst)) {
            audio_stop_sound(current_bgm_inst);
        }
        current_bgm_inst = noone;
        current_bgm_asset = noone;
        
        if (target_bgm_asset != noone && audio_exists(target_bgm_asset)) {
            // Transition to fade in
            fade_state = 2;
            fade_timer = 0;
            current_bgm_asset = target_bgm_asset;
            current_bgm_inst = audio_play_sound(current_bgm_asset, 10, target_bgm_loop);
            if (current_bgm_inst != noone) {
                audio_sound_gain(current_bgm_inst, 0.0, 0);
            }
            fade_start_vol = 0.0;
            fade_target_vol = bgm_volume * master_volume;
        } else {
            fade_state = 0; // IDLE
        }
    }
} else if (fade_state == 2) {
    // Fading IN new track
    fade_timer += 1;
    var _progress = clamp(fade_timer / fade_duration_steps, 0.0, 1.0);
    var _cur_vol = lerp(fade_start_vol, fade_target_vol, _progress);
    
    if (current_bgm_inst != noone && audio_is_playing(current_bgm_inst)) {
        audio_sound_gain(current_bgm_inst, _cur_vol, 0);
    }
    
    if (_progress >= 1.0) {
        fade_state = 0; // Finished transition
    }
}
"""

with open(os.path.join(OBJ_DIR, "Step_0.gml"), "w") as f:
    f.write(step_gml)

cleanup_gml = """/// @description obj_AudioManager CleanUp Event
// Halt all playing audio channels to prevent leaks or orphan emitters

if (current_bgm_inst != noone && audio_is_playing(current_bgm_inst)) {
    audio_stop_sound(current_bgm_inst);
    current_bgm_inst = noone;
}
audio_stop_all();
"""

with open(os.path.join(OBJ_DIR, "CleanUp_0.gml"), "w") as f:
    f.write(cleanup_gml)

print("✓ Created objects/obj_AudioManager (Create_0, Step_0, CleanUp_0)")

# =============================================================================
# 2. CREATE scripts/scr_audio_manager RESOURCE
# =============================================================================

SCR_DIR = "scripts/scr_audio_manager"
os.makedirs(SCR_DIR, exist_ok=True)

scr_yy = {
  "$GMScript": "v1",
  "%Name": "scr_audio_manager",
  "isCompatibility": False,
  "isDnD": False,
  "name": "scr_audio_manager",
  "parent": {
    "name": "MechMakerConcept",
    "path": "MechMakerConcept.yyp"
  },
  "resourceType": "GMScript",
  "resourceVersion": "2.0"
}

with open(os.path.join(SCR_DIR, "scr_audio_manager.yy"), "w") as f:
    json.dump(scr_yy, f, indent=2)

scr_gml = """/// @description Global Audio Architecture & Soundscape Dispatcher (Lead Audio Engineer & Lead Composer)
/// Functions for seamless BGM crossfading, tactical mecha foley, weapon fire, and UI feedback

/// @function scr_audio_ensure_manager()
function scr_audio_ensure_manager() {
    if (!instance_exists(obj_AudioManager)) {
        instance_create_depth(0, 0, 0, obj_AudioManager);
    }
    return instance_find(obj_AudioManager, 0);
}

/// @function scr_audio_play_sfx(_sound_asset, _vol_scale, _pitch_var)
/// @description Plays a sound effect with pitch randomization to prevent audio ear fatigue.
function scr_audio_play_sfx(_sound_asset, _vol_scale = 1.0, _pitch_var = 0.08) {
    if (!audio_exists(_sound_asset)) return noone;
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) {
        return _mgr.play_sfx(_sound_asset, _vol_scale, _pitch_var);
    }
    return audio_play_sound(_sound_asset, 5, false);
}

/// @function scr_audio_play_bgm(_bgm_asset, _fade_ms, _loop)
/// @description Smoothly crossfades or starts a background music track.
function scr_audio_play_bgm(_bgm_asset, _fade_ms = 800, _loop = true) {
    if (!audio_exists(_bgm_asset)) return;
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) {
        _mgr.play_bgm(_bgm_asset, _fade_ms, _loop);
    } else {
        audio_play_sound(_bgm_asset, 10, _loop);
    }
}

/// @function scr_audio_stop_bgm(_fade_ms)
/// @description Fades out currently playing music.
function scr_audio_stop_bgm(_fade_ms = 600) {
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) {
        _mgr.stop_bgm(_fade_ms);
    }
}

/// @function scr_audio_play_ui(_action)
/// @description Dispatcher for UI sounds.
function scr_audio_play_ui(_action) {
    switch (_action) {
        case "click":
            scr_audio_play_sfx(snd_ui_click, 0.9, 0.06);
            break;
        case "hover":
            scr_audio_play_sfx(snd_ui_hover, 0.6, 0.04);
            break;
        case "tab":
            scr_audio_play_sfx(snd_ui_tab, 0.85, 0.04);
            break;
        case "confirm":
            scr_audio_play_sfx(snd_ui_confirm, 1.0, 0.02);
            break;
        case "cancel":
            scr_audio_play_sfx(snd_ui_cancel, 0.9, 0.04);
            break;
        case "stamp":
            scr_audio_play_sfx(snd_ui_stamp, 1.0, 0.05);
            break;
        case "boot":
            scr_audio_play_sfx(snd_ui_terminal_boot, 1.0, 0.0);
            break;
    }
}

/// @function scr_audio_play_weapon(_weapon_type)
/// @description Dispatches authentic mobile suit ballistic, beam, or ordnance firing Foley.
function scr_audio_play_weapon(_weapon_type) {
    switch (string_lower(_weapon_type)) {
        case "vulcan":
        case "chaingun":
        case "mg":
            scr_audio_play_sfx(snd_weapon_vulcan, 0.9, 0.12);
            break;
        case "cannon":
        case "120mm":
        case "artillery":
            scr_audio_play_sfx(snd_weapon_cannon_120mm, 1.0, 0.06);
            break;
        case "missile":
        case "rocket":
        case "salvo":
            scr_audio_play_sfx(snd_weapon_missile_launch, 0.95, 0.08);
            break;
        case "beam":
        case "laser":
        case "particle":
            scr_audio_play_sfx(snd_weapon_beam_rifle, 0.95, 0.05);
            break;
        case "blade":
        case "saber":
        case "claw":
        case "melee":
            scr_audio_play_sfx(snd_weapon_plasma_blade, 0.9, 0.08);
            break;
        case "railgun":
        case "sniper":
        case "hypersonic":
            scr_audio_play_sfx(snd_weapon_railgun, 1.0, 0.04);
            break;
        default:
            scr_audio_play_sfx(snd_weapon_vulcan, 0.8, 0.10);
            break;
    }
}

/// @function scr_audio_play_impact(_type, _is_crit)
/// @description Dispatches kinetic or energy impact Foley and hull damage alarms.
function scr_audio_play_impact(_type, _is_crit = false) {
    if (_is_crit) {
        scr_audio_play_sfx(snd_impact_penetrate, 1.0, 0.05);
        scr_audio_play_sfx(snd_explosion_small, 0.85, 0.10);
        scr_audio_play_sfx(snd_alarm_critical, 0.75, 0.02);
    } else {
        if (_type == "armor" || _type == "ricochet") {
            scr_audio_play_sfx(snd_impact_armor, 0.9, 0.08);
        } else {
            scr_audio_play_sfx(snd_impact_penetrate, 0.85, 0.08);
            scr_audio_play_sfx(snd_explosion_small, 0.65, 0.10);
        }
    }
}

/// @function scr_audio_play_location_bgm(_context)
/// @description Automatically selects appropriate theme based on room and active tab.
function scr_audio_play_location_bgm(_context) {
    switch (_context) {
        case "hq":
        case "strategic_map":
        case "war_room":
        case "diplomacy":
            scr_audio_play_bgm(bgm_hq_ambience, 1000, true);
            break;
        case "prototyping":
        case "assembly":
        case "sintering":
        case "foundry":
            scr_audio_play_bgm(bgm_prototyping_bay, 800, true);
            break;
        case "combat":
        case "battle":
            scr_audio_play_bgm(bgm_combat_engage, 1000, true);
            break;
        case "incursion":
        case "nemesis":
        case "boss":
            scr_audio_play_bgm(bgm_nemesis_incursion, 600, true);
            break;
        case "victory":
            scr_audio_play_bgm(bgm_victory_fanfare, 300, false);
            break;
        case "defeat":
            scr_audio_play_bgm(bgm_defeat_somber, 400, false);
            break;
    }
}
"""

with open(os.path.join(SCR_DIR, "scr_audio_manager.gml"), "w") as f:
    f.write(scr_gml)

print("✓ Created scripts/scr_audio_manager/scr_audio_manager.gml")

# =============================================================================
# 3. REGISTER obj_AudioManager & scr_audio_manager IN MECHMAKERCONCEPT.YYP
# =============================================================================

def register_entry_in_yyp(name, path):
    with open(YYP_PATH, "r") as f:
        content = f.read()
    if path in content:
        return
    idx = content.find('"resources":')
    if idx != -1:
        bracket_idx = content.find('],', idx)
        if bracket_idx != -1:
            new_entry = '    {"id":{"name":"' + name + '","path":"' + path + '",},},\n'
            content = content[:bracket_idx] + new_entry + content[bracket_idx:]
            with open(YYP_PATH, "w") as f:
                f.write(content)
            print(f"✓ Registered {name} in {YYP_PATH}")

register_entry_in_yyp("obj_AudioManager", "objects/obj_AudioManager/obj_AudioManager.yy")
register_entry_in_yyp("scr_audio_manager", "scripts/scr_audio_manager/scr_audio_manager.yy")

# =============================================================================
# 4. SPAWN obj_AudioManager IN rm_init/RoomCreationCode.gml
# =============================================================================

rm_init_path = "rooms/rm_init/RoomCreationCode.gml"
with open(rm_init_path, "r") as f:
    rm_code = f.read()

audio_spawn_code = """// 4b. Instantiate persistent obj_AudioManager if not already created
if (!instance_exists(obj_AudioManager)) {
    instance_create_depth(0, 0, 0, obj_AudioManager);
    show_debug_message("[rm_init] Created obj_AudioManager");
}
"""

if "obj_AudioManager" not in rm_code:
    target = "// 5. Synchronize pilot hiring market"
    rm_code = rm_code.replace(target, audio_spawn_code + "\n" + target)
    with open(rm_init_path, "w") as f:
        f.write(rm_code)
    print("✓ Added obj_AudioManager bootstrap to rooms/rm_init/RoomCreationCode.gml")

print(">>> Audio Architecture Initialization Complete <<<")
