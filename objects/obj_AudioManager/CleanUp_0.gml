/// @description obj_AudioManager CleanUp Event
// Halt all playing audio channels to prevent leaks or orphan emitters

if (current_bgm_inst != noone && audio_is_playing(current_bgm_inst)) {
    audio_stop_sound(current_bgm_inst);
    current_bgm_inst = noone;
}
audio_stop_all();
