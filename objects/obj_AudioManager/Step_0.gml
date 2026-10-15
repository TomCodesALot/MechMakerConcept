/// @description obj_AudioManager Step Event
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
