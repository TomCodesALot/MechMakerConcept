/// @description obj_HQTerminal Step Event
// Turn-based UI controller, discrete draggable inputs, and spark particle dynamics
// Strictly adheres to docs/02_alloy_chemistry.md, docs/03_prototyping_minigames.md & docs/09_ui_ux_flow.md

// 1. Toast & Alert Timers
if (toast_timer > 0) toast_timer--;

alert_timer++;
if (alert_timer >= 320) {
    alert_timer = 0;
    alert_index = (alert_index + 1) % array_length(alerts_feed);
}

// 2. Camera / UI Screen Shake Recovery
crucible_shake = max(0.0, crucible_shake - 0.7);

// 3. Update Spark Particles
for (var i = array_length(spark_particles) - 1; i >= 0; i--) {
    var _sp = spark_particles[i];
    _sp.x += _sp.vx;
    _sp.y += _sp.vy;
    _sp.life -= 0.05;
    if (_sp.life <= 0) {
        array_delete(spark_particles, i, 1);
    }
}

// 4. Global Hotkey Shortcuts (docs/09)
if (keyboard_check_pressed(vk_f5)) {
    scr_save_game();
}
if (keyboard_check_pressed(vk_f9)) {
    scr_load_game();
}
if (keyboard_check_pressed(vk_f1) || keyboard_check_pressed(ord("H"))) {
    active_tutorial_modal = (active_tutorial_modal == "") ? "PMC_MANUAL" : "";
}
if (keyboard_check_pressed(ord("L"))) {
    show_turn_briefing_modal = !show_turn_briefing_modal;
}
if (keyboard_check_pressed(vk_escape)) {
    active_tutorial_modal = "";
    show_turn_briefing_modal = false;
    showing_retire_modal = false;
}

// 5. Minigame 0: Real-Time Slider Alignment Computation
if (active_tab == 0 && rd_subtab == 1 && active_minigame == 0) {
    reactor_alignment_pct = clamp(100.0 - (abs(slider_freq - wave_target_freq) * 32.0 + abs(slider_amp - wave_target_amp) * 1.1 + abs(slider_phase - wave_target_phase) * 0.32), 0.0, 100.0);
}
