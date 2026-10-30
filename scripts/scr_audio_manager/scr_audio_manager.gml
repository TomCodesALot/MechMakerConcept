/// @description Global Audio Architecture & Soundscape Dispatcher (Lead Audio Engineer & Lead Composer)
/// Functions for seamless BGM crossfading, tactical mecha foley, weapon fire, and UI feedback

/// @function scr_audio_ensure_manager()
function scr_audio_ensure_manager() {
    if (!instance_exists(obj_AudioManager)) {
        instance_create_depth(0, 0, 0, obj_AudioManager);
    }
    return instance_find(obj_AudioManager, 0);
}

/// @function scr_audio_is_muted()
function scr_audio_is_muted() {
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) return _mgr.master_muted;
    return true;
}

/// @function scr_audio_set_muted(_mute)
function scr_audio_set_muted(_mute) {
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) {
        return _mgr.set_muted(_mute);
    }
    return _mute;
}

/// @function scr_audio_toggle_mute()
function scr_audio_toggle_mute() {
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) {
        return _mgr.toggle_mute();
    }
    return true;
}

/// @function scr_audio_set_master_volume(_vol)
function scr_audio_set_master_volume(_vol) {
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) _mgr.set_master_volume(_vol);
}

/// @function scr_audio_set_bgm_volume(_vol)
function scr_audio_set_bgm_volume(_vol) {
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) _mgr.set_bgm_volume(_vol);
}

/// @function scr_audio_set_sfx_volume(_vol)
function scr_audio_set_sfx_volume(_vol) {
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) _mgr.set_sfx_volume(_vol);
}

/// @function scr_audio_get_master_volume()
function scr_audio_get_master_volume() {
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) return _mgr.master_volume;
    return 1.0;
}

/// @function scr_audio_get_bgm_volume()
function scr_audio_get_bgm_volume() {
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) return _mgr.bgm_volume;
    return 0.85;
}

/// @function scr_audio_get_sfx_volume()
function scr_audio_get_sfx_volume() {
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) return _mgr.sfx_volume;
    return 0.90;
}

/// @function scr_audio_is_bgm_muted()
function scr_audio_is_bgm_muted() {
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) return _mgr.bgm_muted;
    return false;
}

/// @function scr_audio_is_sfx_muted()
function scr_audio_is_sfx_muted() {
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) return _mgr.sfx_muted;
    return false;
}

/// @function scr_audio_set_bgm_muted(_mute)
function scr_audio_set_bgm_muted(_mute) {
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) _mgr.set_bgm_muted(_mute);
}

/// @function scr_audio_set_sfx_muted(_mute)
function scr_audio_set_sfx_muted(_mute) {
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) _mgr.set_sfx_muted(_mute);
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
        if (!scr_audio_is_muted()) {
            audio_play_sound(_bgm_asset, 10, _loop);
        }
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


/// @function scr_audio_play_mech_stride(_unit_type)
/// @description Dispatches authentic mechanical walking/propulsion Foley with hydraulic whine and pitch variation.
function scr_audio_play_mech_stride(_unit_type) {
    var _type = string_upper(string(_unit_type));
    if (string_pos("IRONCLAD", _type) > 0 || string_pos("COMMANDER", _type) > 0 || string_pos("GRUNT", _type) > 0) {
        // Heavy bipedal frame: deep footfall impact + hydraulic joint whine
        scr_audio_play_sfx(snd_mech_step, 0.90, 0.10);
        scr_audio_play_sfx(snd_mech_servo, 0.55, 0.08);
    } else if (string_pos("AEROSTRIKER", _type) > 0 || string_pos("AERO", _type) > 0) {
        // Aero-Striker: vernier thruster burn
        scr_audio_play_sfx(snd_mech_boost, 0.85, 0.06);
    } else if (string_pos("TANK", _type) > 0 || string_pos("TECHNICAL", _type) > 0) {
        // Heavy armor tracked tread rumble / engine roar
        scr_audio_play_sfx(snd_hydraulic_press, 0.80, 0.12);
        scr_audio_play_sfx(snd_mech_servo, 0.40, 0.05);
    } else if (string_pos("EXO", _type) > 0 || string_pos("INF", _type) > 0) {
        // Light exoskeleton power-assisted strides
        scr_audio_play_sfx(snd_mech_step, 0.65, 0.15);
    } else {
        scr_audio_play_sfx(snd_mech_step, 0.80, 0.08);
    }
}

/// @function scr_audio_play_skirmish_combat(_attacker_unit, _defender_unit, _target_destroyed)
/// @description Dispatches mobile suit ballistic or energy weapons and impact detonations during hex skirmishes.
function scr_audio_play_skirmish_combat(_attacker_unit, _defender_unit, _target_destroyed = false) {
    var _atk_type = string_upper(string(_attacker_unit.unit_type));
    
    // Weapon fire Foley
    if (string_pos("AEROSTRIKER", _atk_type) > 0 || string_pos("AERO", _atk_type) > 0) {
        scr_audio_play_sfx(snd_weapon_missile_launch, 0.95, 0.08);
    } else if (string_pos("SNIPER", _atk_type) > 0 || string_pos("HOVER", _atk_type) > 0) {
        scr_audio_play_sfx(snd_weapon_railgun, 1.0, 0.05);
    } else if (string_pos("TANK", _atk_type) > 0 || string_pos("ARTILLERY", _atk_type) > 0) {
        scr_audio_play_sfx(snd_weapon_cannon_120mm, 1.0, 0.06);
    } else if (string_pos("IRONCLAD", _atk_type) > 0) {
        scr_audio_play_sfx(snd_weapon_vulcan, 0.95, 0.12);
        scr_audio_play_sfx(snd_weapon_cannon_120mm, 0.75, 0.05);
    } else {
        scr_audio_play_sfx(snd_weapon_vulcan, 0.90, 0.10);
    }
    
    // Impact and destruction Foley
    if (_target_destroyed) {
        scr_audio_play_sfx(snd_impact_penetrate, 1.0, 0.04);
        scr_audio_play_sfx(snd_explosion_large, 1.0, 0.08);
        scr_audio_play_sfx(snd_alarm_critical, 0.70, 0.02);
    } else {
        scr_audio_play_sfx(snd_impact_armor, 0.85, 0.08);
        scr_audio_play_sfx(snd_explosion_small, 0.70, 0.10);
    }
}

/// @function scr_audio_play_radar_ping()
/// @description Dispatches high-frequency electronic sonar sweep chirp when discovering hostiles.
function scr_audio_play_radar_ping() {
    scr_audio_play_sfx(snd_ui_tab, 1.0, 0.15);
}

/// @function scr_audio_play_facility_capture()
/// @description Dispatches triumphant military fanfare and mechanical stamp upon securing an enemy facility.
function scr_audio_play_facility_capture() {
    scr_audio_play_sfx(snd_discovery_fanfare, 0.95, 0.02);
    scr_audio_play_sfx(snd_ui_stamp, 1.0, 0.04);
}

/// @function scr_audio_play_phase_horn()
/// @description Dispatches tactical phase shift industrial cue when ending player turn or advancing cycles.
function scr_audio_play_phase_horn() {
    scr_audio_play_sfx(snd_ui_terminal_boot, 0.85, 0.04);
    scr_audio_play_sfx(snd_hydraulic_press, 0.60, 0.05);
}
