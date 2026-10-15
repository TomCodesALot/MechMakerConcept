/// @description obj_AudioManager Create Event
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
