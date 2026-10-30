/// @description obj_AudioManager Create Event
// Central audio director managing BGM streaming, crossfading, pitch variation, and SFX volume channels
// Follows Lead Audio Engineer & Lead Composer rules: mechanical Foley, tactical soundscapes, and memory streaming

// Audio Channels & Master State
master_volume = 1.0;
bgm_volume = 0.85;
sfx_volume = 0.90;

// User Requirement: Default the game as muted
master_muted = true;
bgm_muted = false;
sfx_muted = false;

// Apply master audio gain 0 to engine listener on boot
audio_master_gain(0.0);
audio_stop_all();

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

/// @function set_muted(_mute)
set_muted = function(_mute) {
    master_muted = _mute;
    if (master_muted) {
        audio_master_gain(0.0);
        if (current_bgm_inst != noone && audio_is_playing(current_bgm_inst)) {
            audio_sound_gain(current_bgm_inst, 0.0, 0);
        }
    } else {
        audio_master_gain(master_volume);
        if (current_bgm_inst != noone && audio_is_playing(current_bgm_inst)) {
            var _bgm_vol = bgm_muted ? 0.0 : (bgm_volume * master_volume);
            audio_sound_gain(current_bgm_inst, _bgm_vol, 200);
        }
    }
    return master_muted;
};

/// @function toggle_mute()
toggle_mute = function() {
    return set_muted(!master_muted);
};

/// @function set_master_volume(_vol)
set_master_volume = function(_vol) {
    master_volume = clamp(_vol, 0.0, 1.0);
    if (!master_muted) {
        audio_master_gain(master_volume);
    }
};

/// @function set_bgm_volume(_vol)
set_bgm_volume = function(_vol) {
    bgm_volume = clamp(_vol, 0.0, 1.0);
    if (!master_muted && !bgm_muted && current_bgm_inst != noone && audio_is_playing(current_bgm_inst)) {
        audio_sound_gain(current_bgm_inst, bgm_volume * master_volume, 100);
    }
};

/// @function set_sfx_volume(_vol)
set_sfx_volume = function(_vol) {
    sfx_volume = clamp(_vol, 0.0, 1.0);
};

/// @function set_bgm_muted(_mute)
set_bgm_muted = function(_mute) {
    bgm_muted = _mute;
    if (current_bgm_inst != noone && audio_is_playing(current_bgm_inst)) {
        var _bgm_vol = (master_muted || bgm_muted) ? 0.0 : (bgm_volume * master_volume);
        audio_sound_gain(current_bgm_inst, _bgm_vol, 150);
    }
};

/// @function set_sfx_muted(_mute)
set_sfx_muted = function(_mute) {
    sfx_muted = _mute;
};

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
        fade_target_vol = (master_muted || bgm_muted) ? 0.0 : (bgm_volume * master_volume);
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
    if (master_muted || sfx_muted) return noone;
    if (!audio_exists(_asset)) return noone;
    
    var _key = audio_get_name(_asset);
    var _now = current_time;
    // Debounce identical sound triggers within 25ms to avoid ear clipping
    if (variable_struct_exists(last_played_times, _key)) {
        if (_now - variable_struct_get(last_played_times, _key) < 25) {
            return noone;
        }
    }
    variable_struct_set(last_played_times, _key, _now);
    
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
