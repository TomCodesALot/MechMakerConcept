#!/usr/bin/env python3
import os
import re

print("Applying Settings Window & Default Audio Mute System...")

# 1. Update obj_HQTerminal/Draw_64.gml - Top Bar Buttons
path = "objects/obj_HQTerminal/Draw_64.gml"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# Replace top bar buttons with tightened layout that includes Settings & Mute button
old_top_bar = '''// 4. Command Actions (x: 588 to 1106, h: 44, y: 10)
var _et_y = 10;
var _hud_btn_h = 44;

// Advance Turn Button (x: 588, w: 164)
var _et_x = 588;
var _et_w = 164;
var _et_hov = (_mx >= _et_x && _mx <= _et_x + _et_w && _my >= _et_y && _my <= _et_y + _hud_btn_h);
if (_et_hov && _click && instance_exists(obj_GameManager)) {
    obj_GameManager.end_turn();
}
draw_set_color(_et_hov ? make_color_rgb(28, 95, 55) : make_color_rgb(16, 48, 28));
draw_rectangle(_et_x + _sx, _et_y + _sy, _et_x + _et_w + _sx, _et_y + _hud_btn_h + _sy, false);
draw_set_color(_et_hov ? make_color_rgb(80, 255, 140) : make_color_rgb(50, 200, 100));
draw_rectangle(_et_x + _sx, _et_y + _sy, _et_x + _et_w + _sx, _et_y + _hud_btn_h + _sy, true);
draw_set_color(c_white);
draw_text(_et_x + 12 + _sx, _et_y + 14 + _sy, ">> ADVANCE TURN <<");

// Turn Log Button (x: 760, w: 68)
var _log_btn_x = 760;
var _log_btn_w = 68;
var _log_hov = (_mx >= _log_btn_x && _mx <= _log_btn_x + _log_btn_w && _my >= _et_y && _my <= _et_y + _hud_btn_h);
if (_log_hov && _click) {
    show_turn_briefing_modal = !show_turn_briefing_modal;
}
draw_set_color(_log_hov ? make_color_rgb(32, 60, 95) : make_color_rgb(16, 28, 46));
draw_rectangle(_log_btn_x + _sx, _et_y + _sy, _log_btn_x + _log_btn_w + _sx, _et_y + _hud_btn_h + _sy, false);
draw_set_color(_log_hov ? make_color_rgb(100, 210, 255) : make_color_rgb(55, 140, 220));
draw_rectangle(_log_btn_x + _sx, _et_y + _sy, _log_btn_x + _log_btn_w + _sx, _et_y + _hud_btn_h + _sy, true);
draw_set_color(c_white);
draw_text(_log_btn_x + 14 + _sx, _et_y + 14 + _sy, "[LOG]");

// Global PMC Manual Button (x: 836, w: 88)
var _man_btn_x = 836;
var _man_btn_w = 88;
var _man_hov = (_mx >= _man_btn_x && _mx <= _man_btn_x + _man_btn_w && _my >= _et_y && _my <= _et_y + _hud_btn_h);
if (_man_hov && _click) {
    active_tutorial_modal = (active_tutorial_modal == "PMC_MANUAL") ? "" : "PMC_MANUAL";
}
draw_set_color(_man_hov ? make_color_rgb(68, 50, 18) : make_color_rgb(34, 24, 10));
draw_rectangle(_man_btn_x + _sx, _et_y + _sy, _man_btn_x + _man_btn_w + _sx, _et_y + _hud_btn_h + _sy, false);
draw_set_color(_man_hov ? make_color_rgb(255, 200, 70) : make_color_rgb(220, 160, 50));
draw_rectangle(_man_btn_x + _sx, _et_y + _sy, _man_btn_x + _man_btn_w + _sx, _et_y + _hud_btn_h + _sy, true);
draw_set_color(c_white);
draw_text(_man_btn_x + 10 + _sx, _et_y + 14 + _sy, "[?] MANUAL");

// Quick Save Button (x: 932, w: 82)
var _btn_save_x = 932;
var _q_btn_w = 82;
var _s_hov = (_mx >= _btn_save_x && _mx <= _btn_save_x + _q_btn_w && _my >= _et_y && _my <= _et_y + _hud_btn_h);
if (_s_hov && _click) scr_save_game();
draw_set_color(_s_hov ? make_color_rgb(20, 62, 40) : make_color_rgb(12, 32, 20));
draw_rectangle(_btn_save_x + _sx, _et_y + _sy, _btn_save_x + _q_btn_w + _sx, _et_y + _hud_btn_h + _sy, false);
draw_set_color(_s_hov ? make_color_rgb(60, 220, 120) : make_color_rgb(35, 150, 75));
draw_rectangle(_btn_save_x + _sx, _et_y + _sy, _btn_save_x + _q_btn_w + _sx, _et_y + _hud_btn_h + _sy, true);
draw_set_color(make_color_rgb(110, 245, 150));
draw_text(_btn_save_x + 8 + _sx, _et_y + 14 + _sy, "[F5 SAVE]");

// Career Retirement Button (x: 1022, w: 84)
var _ret_btn_x = 1022;
var _ret_btn_w = 84;
var _ret_hov = (_mx >= _ret_btn_x && _mx <= _ret_btn_x + _ret_btn_w && _my >= _et_y && _my <= _et_y + _hud_btn_h);
if (_ret_hov && _click && instance_exists(obj_GameManager)) {
    obj_GameManager.retire_career();
    showing_retire_modal = true;
    scr_audio_play_ui("confirm");
}
draw_set_color(_ret_hov ? make_color_rgb(68, 48, 12) : make_color_rgb(32, 22, 6));
draw_rectangle(_ret_btn_x + _sx, _et_y + _sy, _ret_btn_x + _ret_btn_w + _sx, _et_y + _hud_btn_h + _sy, false);
draw_set_color(_ret_hov ? make_color_rgb(255, 220, 80) : make_color_rgb(220, 180, 60));
draw_rectangle(_ret_btn_x + _sx, _et_y + _sy, _ret_btn_x + _ret_btn_w + _sx, _et_y + _hud_btn_h + _sy, true);
draw_set_color(make_color_rgb(255, 225, 120));
draw_text(_ret_btn_x + 8 + _sx, _et_y + 14 + _sy, "[RETIRE]");'''

new_top_bar = '''// 4. Command Actions (x: 588 to 1108, h: 44, y: 10)
var _et_y = 10;
var _hud_btn_h = 44;

// Advance Turn Button (x: 588, w: 144)
var _et_x = 588;
var _et_w = 144;
var _et_hov = (_mx >= _et_x && _mx <= _et_x + _et_w && _my >= _et_y && _my <= _et_y + _hud_btn_h);
if (_et_hov && _click && instance_exists(obj_GameManager)) {
    obj_GameManager.end_turn();
}
draw_set_color(_et_hov ? make_color_rgb(28, 95, 55) : make_color_rgb(16, 48, 28));
draw_rectangle(_et_x + _sx, _et_y + _sy, _et_x + _et_w + _sx, _et_y + _hud_btn_h + _sy, false);
draw_set_color(_et_hov ? make_color_rgb(80, 255, 140) : make_color_rgb(50, 200, 100));
draw_rectangle(_et_x + _sx, _et_y + _sy, _et_x + _et_w + _sx, _et_y + _hud_btn_h + _sy, true);
draw_set_color(c_white);
draw_text(_et_x + 8 + _sx, _et_y + 14 + _sy, ">> ADVANCE TURN <<");

// Turn Log Button (x: 736, w: 54)
var _log_btn_x = 736;
var _log_btn_w = 54;
var _log_hov = (_mx >= _log_btn_x && _mx <= _log_btn_x + _log_btn_w && _my >= _et_y && _my <= _et_y + _hud_btn_h);
if (_log_hov && _click) {
    show_turn_briefing_modal = !show_turn_briefing_modal;
}
draw_set_color(_log_hov ? make_color_rgb(32, 60, 95) : make_color_rgb(16, 28, 46));
draw_rectangle(_log_btn_x + _sx, _et_y + _sy, _log_btn_x + _log_btn_w + _sx, _et_y + _hud_btn_h + _sy, false);
draw_set_color(_log_hov ? make_color_rgb(100, 210, 255) : make_color_rgb(55, 140, 220));
draw_rectangle(_log_btn_x + _sx, _et_y + _sy, _log_btn_x + _log_btn_w + _sx, _et_y + _hud_btn_h + _sy, true);
draw_set_color(c_white);
draw_text(_log_btn_x + 8 + _sx, _et_y + 14 + _sy, "[LOG]");

// Global PMC Manual Button (x: 794, w: 70)
var _man_btn_x = 794;
var _man_btn_w = 70;
var _man_hov = (_mx >= _man_btn_x && _mx <= _man_btn_x + _man_btn_w && _my >= _et_y && _my <= _et_y + _hud_btn_h);
if (_man_hov && _click) {
    active_tutorial_modal = (active_tutorial_modal == "PMC_MANUAL") ? "" : "PMC_MANUAL";
}
draw_set_color(_man_hov ? make_color_rgb(68, 50, 18) : make_color_rgb(34, 24, 10));
draw_rectangle(_man_btn_x + _sx, _et_y + _sy, _man_btn_x + _man_btn_w + _sx, _et_y + _hud_btn_h + _sy, false);
draw_set_color(_man_hov ? make_color_rgb(255, 200, 70) : make_color_rgb(220, 160, 50));
draw_rectangle(_man_btn_x + _sx, _et_y + _sy, _man_btn_x + _man_btn_w + _sx, _et_y + _hud_btn_h + _sy, true);
draw_set_color(c_white);
draw_text(_man_btn_x + 6 + _sx, _et_y + 14 + _sy, "[?] GUIDE");

// Quick Save Button (x: 868, w: 66)
var _btn_save_x = 868;
var _q_btn_w = 66;
var _s_hov = (_mx >= _btn_save_x && _mx <= _btn_save_x + _q_btn_w && _my >= _et_y && _my <= _et_y + _hud_btn_h);
if (_s_hov && _click) scr_save_game();
draw_set_color(_s_hov ? make_color_rgb(20, 62, 40) : make_color_rgb(12, 32, 20));
draw_rectangle(_btn_save_x + _sx, _et_y + _sy, _btn_save_x + _q_btn_w + _sx, _et_y + _hud_btn_h + _sy, false);
draw_set_color(_s_hov ? make_color_rgb(60, 220, 120) : make_color_rgb(35, 150, 75));
draw_rectangle(_btn_save_x + _sx, _et_y + _sy, _btn_save_x + _q_btn_w + _sx, _et_y + _hud_btn_h + _sy, true);
draw_set_color(make_color_rgb(110, 245, 150));
draw_text(_btn_save_x + 6 + _sx, _et_y + 14 + _sy, "[SAVE]");

// Career Retirement Button (x: 938, w: 68)
var _ret_btn_x = 938;
var _ret_btn_w = 68;
var _ret_hov = (_mx >= _ret_btn_x && _mx <= _ret_btn_x + _ret_btn_w && _my >= _et_y && _my <= _et_y + _hud_btn_h);
if (_ret_hov && _click && instance_exists(obj_GameManager)) {
    obj_GameManager.retire_career();
    showing_retire_modal = true;
    scr_audio_play_ui("confirm");
}
draw_set_color(_ret_hov ? make_color_rgb(68, 48, 12) : make_color_rgb(32, 22, 6));
draw_rectangle(_ret_btn_x + _sx, _et_y + _sy, _ret_btn_x + _ret_btn_w + _sx, _et_y + _hud_btn_h + _sy, false);
draw_set_color(_ret_hov ? make_color_rgb(255, 220, 80) : make_color_rgb(220, 180, 60));
draw_rectangle(_ret_btn_x + _sx, _et_y + _sy, _ret_btn_x + _ret_btn_w + _sx, _et_y + _hud_btn_h + _sy, true);
draw_set_color(make_color_rgb(255, 225, 120));
draw_text(_ret_btn_x + 6 + _sx, _et_y + 14 + _sy, "[RETIRE]");

// Settings & Audio Mute Button (x: 1010, w: 98, h: 44, y: 10)
var _cfg_btn_x = 1010;
var _cfg_btn_w = 98;
var _is_aud_muted = scr_audio_is_muted();
var _cfg_hov = (_mx >= _cfg_btn_x && _mx <= _cfg_btn_x + _cfg_btn_w && _my >= _et_y && _my <= _et_y + _hud_btn_h);
if (_cfg_hov && _click) {
    show_settings_modal = !show_settings_modal;
    scr_audio_play_ui("click");
}
draw_set_color(_cfg_hov ? (_is_aud_muted ? make_color_rgb(72, 22, 22) : make_color_rgb(20, 48, 70)) : (_is_aud_muted ? make_color_rgb(40, 12, 12) : make_color_rgb(12, 22, 34)));
draw_rectangle(_cfg_btn_x + _sx, _et_y + _sy, _cfg_btn_x + _cfg_btn_w + _sx, _et_y + _hud_btn_h + _sy, false);
draw_set_color(_cfg_hov ? (_is_aud_muted ? make_color_rgb(255, 100, 100) : make_color_rgb(100, 220, 255)) : (_is_aud_muted ? make_color_rgb(220, 65, 65) : make_color_rgb(55, 130, 190)));
draw_rectangle(_cfg_btn_x + _sx, _et_y + _sy, _cfg_btn_x + _cfg_btn_w + _sx, _et_y + _hud_btn_h + _sy, true);
// Left Accent Strip
draw_set_color(_is_aud_muted ? make_color_rgb(255, 50, 50) : make_color_rgb(0, 220, 255));
draw_rectangle(_cfg_btn_x + _sx, _et_y + _sy, _cfg_btn_x + _sx + 3, _et_y + _hud_btn_h + _sy, false);

draw_set_color(_is_aud_muted ? make_color_rgb(255, 120, 120) : make_color_rgb(120, 220, 255));
draw_text(_cfg_btn_x + 8 + _sx, _et_y + 8 + _sy, _is_aud_muted ? "[⚙ MUTED]" : "[⚙ CONFIG]");
draw_set_color(_is_aud_muted ? make_color_rgb(255, 180, 80) : make_color_rgb(80, 240, 140));
draw_text(_cfg_btn_x + 8 + _sx, _et_y + 24 + _sy, _is_aud_muted ? "AUDIO OFF" : "VOL " + string(floor(scr_audio_get_master_volume() * 100)) + "%");'''

if old_top_bar in c:
    c = c.replace(old_top_bar, new_top_bar, 1)
    print("Top bar HUD updated with Settings & Audio button.")
else:
    print("WARNING: old_top_bar not found in Draw_64.gml")

# Append Settings Modal rendering at the end of obj_HQTerminal/Draw_64.gml
settings_modal_code = '''

// =========================================================================
// 8. SYSTEM CONFIGURATION & TACTICAL AUDIO MODAL (LEAD AUDIO ENGINEER SPEC)
// =========================================================================
if (show_settings_modal) {
    // 1. Full Screen Backdrop Dimmer
    draw_set_alpha(0.75);
    draw_set_color(c_black);
    draw_rectangle(0, 0, 1366, 768, false);
    draw_set_alpha(1.0);

    // 2. Modal Dimensions (Fits completely inside 1366x768 with >250px margin)
    var _mw = 800;
    var _mh = 540;
    var _mx0 = floor((1366 - _mw) / 2);
    var _my0 = floor((768 - _mh) / 2);

    // Tactical SNES Border Panel
    scr_draw_snes_panel(_mx0, _my0, _mw, _mh, "TERMINAL CONFIGURATION // AUDIO & SYSTEM SETTINGS", 0, true, 0.08);

    // Close Button [X] Top Right of Modal
    var _close_x = _mx0 + _mw - 44;
    var _close_y = _my0 + 8;
    var _close_hov = (_mx >= _close_x && _mx <= _close_x + 32 && _my >= _close_y && _my <= _close_y + 26);
    if (_close_hov && _click) {
        show_settings_modal = false;
        scr_audio_play_ui("cancel");
    }
    draw_set_color(_close_hov ? make_color_rgb(180, 40, 40) : make_color_rgb(70, 20, 20));
    draw_rectangle(_close_x, _close_y, _close_x + 32, _close_y + 26, false);
    draw_set_color(_close_hov ? make_color_rgb(255, 100, 100) : make_color_rgb(200, 50, 50));
    draw_rectangle(_close_x, _close_y, _close_x + 32, _close_y + 26, true);
    draw_set_color(c_white);
    draw_text(_close_x + 10, _close_y + 6, "X");

    // Subtabs: [1. AUDIO CHANNELS & MUTE]  [2. DISPLAY & SHORTCUTS]
    var _tab_y = _my0 + 44;
    var _t1_w = 260;
    var _t1_hov = (_mx >= _mx0 + 24 && _mx <= _mx0 + 24 + _t1_w && _my >= _tab_y && _my <= _tab_y + 28);
    if (_t1_hov && _click) { settings_active_tab = 0; scr_audio_play_ui("tab"); }
    scr_draw_snes_button(_mx0 + 24, _tab_y, _t1_w, 28, "1. AUDIO & MUTE CONTROL", _t1_hov || (settings_active_tab == 0), (settings_active_tab == 0), (settings_active_tab == 0) ? make_color_rgb(0, 240, 255) : c_white);

    var _t2_x = _mx0 + 24 + _t1_w + 12;
    var _t2_w = 260;
    var _t2_hov = (_mx >= _t2_x && _mx <= _t2_x + _t2_w && _my >= _tab_y && _my <= _tab_y + 28);
    if (_t2_hov && _click) { settings_active_tab = 1; scr_audio_play_ui("tab"); }
    scr_draw_snes_button(_t2_x, _tab_y, _t2_w, 28, "2. DISPLAY & SHORTCUTS", _t2_hov || (settings_active_tab == 1), (settings_active_tab == 1), (settings_active_tab == 1) ? make_color_rgb(0, 240, 255) : c_white);

    // =====================================================================
    // TAB 0: AUDIO CHANNELS & MUTE (LEAD AUDIO ENGINEER SPEC)
    // =====================================================================
    if (settings_active_tab == 0) {
        var _is_muted = scr_audio_is_muted();
        var _m_vol = scr_audio_get_master_volume();
        var _b_vol = scr_audio_get_bgm_volume();
        var _s_vol = scr_audio_get_sfx_volume();
        var _b_muted = scr_audio_is_bgm_muted();
        var _s_muted = scr_audio_is_sfx_muted();

        // 1. PRIMARY MASTER MUTE HERO BUTTON
        var _hero_x = _mx0 + 24;
        var _hero_y = _tab_y + 38;
        var _hero_w = _mw - 48;
        var _hero_h = 58;
        var _hero_hov = (_mx >= _hero_x && _mx <= _hero_x + _hero_w && _my >= _hero_y && _my <= _hero_y + _hero_h);

        if (_hero_hov && _click) {
            scr_audio_toggle_mute();
            scr_audio_play_ui("confirm");
        }

        draw_set_color(_hero_hov ? (_is_muted ? make_color_rgb(60, 20, 20) : make_color_rgb(18, 55, 38)) : (_is_muted ? make_color_rgb(38, 12, 12) : make_color_rgb(10, 32, 22)));
        draw_rectangle(_hero_x, _hero_y, _hero_x + _hero_w, _hero_y + _hero_h, false);
        draw_set_color(_hero_hov ? (_is_muted ? make_color_rgb(255, 90, 90) : make_color_rgb(80, 255, 160)) : (_is_muted ? make_color_rgb(220, 60, 60) : make_color_rgb(45, 190, 110)));
        draw_rectangle(_hero_x, _hero_y, _hero_x + _hero_w, _hero_y + _hero_h, true);
        // Accent Bar
        draw_set_color(_is_muted ? make_color_rgb(255, 60, 60) : make_color_rgb(0, 240, 140));
        draw_rectangle(_hero_x, _hero_y, _hero_x + 6, _hero_y + _hero_h, false);

        draw_set_color(_is_muted ? make_color_rgb(255, 120, 120) : make_color_rgb(100, 255, 170));
        draw_text(_hero_x + 20, _hero_y + 10, _is_muted ? "[!] MASTER AUDIO IS CURRENTLY MUTED (DEFAULT)" : "[✓] MASTER AUDIO IS ACTIVE & OPERATIONAL");
        draw_set_color(_is_muted ? make_color_rgb(255, 200, 140) : make_color_rgb(180, 235, 205));
        draw_text(_hero_x + 20, _hero_y + 32, _is_muted ? ">> CLICK TO UNMUTE ALL AUDIO CHANNELS <<   [Hotkey: Press 'M' anytime]" : ">> CLICK TO MUTE ALL AUDIO CHANNELS <<   [Hotkey: Press 'M' anytime]");

        // 2. MASTER VOLUME CHANNEL
        var _ch1_y = _hero_y + _hero_h + 16;
        var _ch_w = _mw - 48;
        var _ch_h = 74;

        draw_set_color(make_color_rgb(12, 18, 28));
        draw_rectangle(_hero_x, _ch1_y, _hero_x + _ch_w, _ch1_y + _ch_h, false);
        draw_set_color(make_color_rgb(32, 54, 82));
        draw_rectangle(_hero_x, _ch1_y, _hero_x + _ch_w, _ch1_y + _ch_h, true);

        draw_set_color(make_color_rgb(100, 210, 255));
        draw_text(_hero_x + 14, _ch1_y + 10, "MASTER GAIN: " + string(floor(_m_vol * 100)) + "%");
        // Level Meter Bar
        var _bar_x = _hero_x + 180;
        var _bar_w = 190;
        var _bar_h = 16;
        draw_set_color(make_color_rgb(20, 30, 45));
        draw_rectangle(_bar_x, _ch1_y + 12, _bar_x + _bar_w, _ch1_y + 12 + _bar_h, false);
        var _fill_w = floor(_bar_w * _m_vol);
        if (_fill_w > 0) {
            draw_set_color(_is_muted ? make_color_rgb(120, 50, 50) : make_color_rgb(0, 210, 255));
            draw_rectangle(_bar_x, _ch1_y + 12, _bar_x + _fill_w, _ch1_y + 12 + _bar_h, false);
        }
        draw_set_color(make_color_rgb(60, 90, 130));
        draw_rectangle(_bar_x, _ch1_y + 12, _bar_x + _bar_w, _ch1_y + 12 + _bar_h, true);

        // Master Preset Step Buttons: [0%] [25%] [50%] [75%] [100%]
        var _steps = [0.0, 0.25, 0.50, 0.75, 1.0];
        var _sb_w = 64;
        var _sb_x0 = _hero_x + 390;
        for (var si = 0; si < 5; si++) {
            var _sv = _steps[si];
            var _sb_x = _sb_x0 + si * (_sb_w + 6);
            var _sb_hov = (_mx >= _sb_x && _mx <= _sb_x + _sb_w && _my >= _ch1_y + 8 && _my <= _ch1_y + 34);
            var _is_act = (abs(_m_vol - _sv) < 0.05);
            if (_sb_hov && _click) {
                scr_audio_set_master_volume(_sv);
                if (_sv > 0 && _is_muted) scr_audio_set_muted(false);
                scr_audio_play_ui("click");
            }
            scr_draw_snes_button(_sb_x, _ch1_y + 8, _sb_w, 26, string(floor(_sv * 100)) + "%", _sb_hov || _is_act, _is_act, _is_act ? make_color_rgb(100, 255, 180) : c_white);
        }
        draw_set_color(make_color_rgb(150, 180, 210));
        draw_text(_hero_x + 14, _ch1_y + 44, "Controls overall engine amplitude. Setting above 0% un-mutes automatically.");

        // 3. BGM (MUSIC) CHANNEL
        var _ch2_y = _ch1_y + _ch_h + 10;
        draw_set_color(make_color_rgb(12, 18, 28));
        draw_rectangle(_hero_x, _ch2_y, _hero_x + _ch_w, _ch2_y + _ch_h, false);
        draw_set_color(make_color_rgb(32, 54, 82));
        draw_rectangle(_hero_x, _ch2_y, _hero_x + _ch_w, _ch2_y + _ch_h, true);

        draw_set_color(make_color_rgb(100, 210, 255));
        draw_text(_hero_x + 14, _ch2_y + 10, "BGM SCORE: " + string(floor(_b_vol * 100)) + "%");
        // Meter Bar
        draw_set_color(make_color_rgb(20, 30, 45));
        draw_rectangle(_bar_x, _ch2_y + 12, _bar_x + _bar_w, _ch2_y + 12 + _bar_h, false);
        var _b_fill = floor(_bar_w * (_b_muted ? 0.0 : _b_vol));
        if (_b_fill > 0) {
            draw_set_color(_b_muted ? make_color_rgb(120, 50, 50) : make_color_rgb(255, 200, 60));
            draw_rectangle(_bar_x, _ch2_y + 12, _bar_x + _b_fill, _ch2_y + 12 + _bar_h, false);
        }
        draw_set_color(make_color_rgb(60, 90, 130));
        draw_rectangle(_bar_x, _ch2_y + 12, _bar_x + _bar_w, _ch2_y + 12 + _bar_h, true);

        for (var si = 0; si < 5; si++) {
            var _sv = _steps[si];
            var _sb_x = _sb_x0 + si * (_sb_w + 6);
            var _sb_hov = (_mx >= _sb_x && _mx <= _sb_x + _sb_w && _my >= _ch2_y + 8 && _my <= _ch2_y + 34);
            var _is_act = (abs(_b_vol - _sv) < 0.05 && !_b_muted);
            if (_sb_hov && _click) {
                scr_audio_set_bgm_volume(_sv);
                if (_b_muted) scr_audio_set_bgm_muted(false);
                scr_audio_play_ui("click");
            }
            scr_draw_snes_button(_sb_x, _ch2_y + 8, _sb_w, 26, string(floor(_sv * 100)) + "%", _sb_hov || _is_act, _is_act, _is_act ? make_color_rgb(255, 220, 90) : c_white);
        }

        // BGM Mute Toggle Button
        var _bm_w = 110;
        var _bm_x = _hero_x + 14;
        var _bm_y = _ch2_y + 38;
        var _bm_hov = (_mx >= _bm_x && _mx <= _bm_x + _bm_w && _my >= _bm_y && _my <= _bm_y + 26);
        if (_bm_hov && _click) {
            scr_audio_set_bgm_muted(!_b_muted);
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_bm_x, _bm_y, _bm_w, 26, _b_muted ? "[BGM MUTED]" : "[MUTE BGM]", _bm_hov, _b_muted, _b_muted ? make_color_rgb(255, 100, 100) : c_white);
        draw_set_color(make_color_rgb(150, 180, 210));
        draw_text(_hero_x + 140, _ch2_y + 44, "Tactical synth soundtrack (Front Mission / Gundam ambient & battle themes).");

        // 4. SFX (FOLEY & WEAPONS) CHANNEL
        var _ch3_y = _ch2_y + _ch_h + 10;
        draw_set_color(make_color_rgb(12, 18, 28));
        draw_rectangle(_hero_x, _ch3_y, _hero_x + _ch_w, _ch3_y + _ch_h, false);
        draw_set_color(make_color_rgb(32, 54, 82));
        draw_rectangle(_hero_x, _ch3_y, _hero_x + _ch_w, _ch3_y + _ch_h, true);

        draw_set_color(make_color_rgb(100, 210, 255));
        draw_text(_hero_x + 14, _ch3_y + 10, "SFX FOLEY: " + string(floor(_s_vol * 100)) + "%");
        // Meter Bar
        draw_set_color(make_color_rgb(20, 30, 45));
        draw_rectangle(_bar_x, _ch3_y + 12, _bar_x + _bar_w, _ch3_y + 12 + _bar_h, false);
        var _s_fill = floor(_bar_w * (_s_muted ? 0.0 : _s_vol));
        if (_s_fill > 0) {
            draw_set_color(_s_muted ? make_color_rgb(120, 50, 50) : make_color_rgb(0, 240, 140));
            draw_rectangle(_bar_x, _ch3_y + 12, _bar_x + _s_fill, _ch3_y + 12 + _bar_h, false);
        }
        draw_set_color(make_color_rgb(60, 90, 130));
        draw_rectangle(_bar_x, _ch3_y + 12, _bar_x + _bar_w, _ch3_y + 12 + _bar_h, true);

        for (var si = 0; si < 5; si++) {
            var _sv = _steps[si];
            var _sb_x = _sb_x0 + si * (_sb_w + 6);
            var _sb_hov = (_mx >= _sb_x && _mx <= _sb_x + _sb_w && _my >= _ch3_y + 8 && _my <= _ch3_y + 34);
            var _is_act = (abs(_s_vol - _sv) < 0.05 && !_s_muted);
            if (_sb_hov && _click) {
                scr_audio_set_sfx_volume(_sv);
                if (_s_muted) scr_audio_set_sfx_muted(false);
                scr_audio_play_ui("click");
            }
            scr_draw_snes_button(_sb_x, _ch3_y + 8, _sb_w, 26, string(floor(_sv * 100)) + "%", _sb_hov || _is_act, _is_act, _is_act ? make_color_rgb(100, 255, 180) : c_white);
        }

        // SFX Mute Button & Test Sound Button
        var _sm_w = 110;
        var _sm_x = _hero_x + 14;
        var _sm_y = _ch3_y + 38;
        var _sm_hov = (_mx >= _sm_x && _mx <= _sm_x + _sm_w && _my >= _sm_y && _my <= _sm_y + 26);
        if (_sm_hov && _click) {
            scr_audio_set_sfx_muted(!_s_muted);
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_sm_x, _sm_y, _sm_w, 26, _s_muted ? "[SFX MUTED]" : "[MUTE SFX]", _sm_hov, _s_muted, _s_muted ? make_color_rgb(255, 100, 100) : c_white);

        var _ts_w = 160;
        var _ts_x = _sm_x + _sm_w + 12;
        var _ts_hov = (_mx >= _ts_x && _mx <= _ts_x + _ts_w && _my >= _sm_y && _my <= _sm_y + 26);
        if (_ts_hov && _click) {
            scr_audio_play_sfx(snd_weapon_beam_rifle, 1.0, 0.05);
            scr_audio_play_ui("confirm");
        }
        scr_draw_snes_button(_ts_x, _sm_y, _ts_w, 26, "🔊 TEST WEAPON SFX", _ts_hov, false, make_color_rgb(100, 220, 255));
        draw_set_color(make_color_rgb(150, 180, 210));
        draw_text(_ts_x + _ts_w + 14, _ch3_y + 44, "Mechanical hydraulics, beam discharge, plasma venting.");
    }

    // =====================================================================
    // TAB 1: DISPLAY SETTINGS & SHORTCUTS REFERENCE
    // =====================================================================
    else if (settings_active_tab == 1) {
        var _dsp_x = _mx0 + 24;
        var _dsp_y = _tab_y + 40;
        var _dsp_w = _mw - 48;

        // Visual Options Card
        draw_set_color(make_color_rgb(12, 18, 28));
        draw_rectangle(_dsp_x, _dsp_y, _dsp_x + _dsp_w, _dsp_y + 110, false);
        draw_set_color(make_color_rgb(32, 54, 82));
        draw_rectangle(_dsp_x, _dsp_y, _dsp_x + _dsp_w, _dsp_y + 110, true);

        draw_set_color(make_color_rgb(100, 210, 255));
        draw_text(_dsp_x + 14, _dsp_y + 12, "TACTICAL DISPLAY & VISUAL FILTER CONFIGURATION:");

        // CRT Scanline Toggle
        var _crt_w = 260;
        var _crt_hov = (_mx >= _dsp_x + 14 && _mx <= _dsp_x + 14 + _crt_w && _my >= _dsp_y + 38 && _my <= _dsp_y + 68);
        if (_crt_hov && _click) {
            settings_crt_scanlines = !settings_crt_scanlines;
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_dsp_x + 14, _dsp_y + 38, _crt_w, 30, settings_crt_scanlines ? "[✓] CRT SCANLINES: ON" : "[X] CRT SCANLINES: OFF", _crt_hov, settings_crt_scanlines, settings_crt_scanlines ? make_color_rgb(0, 240, 140) : make_color_rgb(220, 100, 100));

        // Screen Shake Toggle
        var _shk_x = _dsp_x + 14 + _crt_w + 16;
        var _shk_w = 260;
        var _shk_hov = (_mx >= _shk_x && _mx <= _shk_x + _shk_w && _my >= _dsp_y + 38 && _my <= _dsp_y + 68);
        if (_shk_hov && _click) {
            settings_screen_shake = !settings_screen_shake;
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_shk_x, _dsp_y + 38, _shk_w, 30, settings_screen_shake ? "[✓] SCREEN SHAKE: ON" : "[X] SCREEN SHAKE: OFF", _shk_hov, settings_screen_shake, settings_screen_shake ? make_color_rgb(0, 240, 140) : make_color_rgb(220, 100, 100));

        draw_set_color(make_color_rgb(150, 180, 210));
        draw_text(_dsp_x + 14, _dsp_y + 78, "Authentic 1990s cathode-ray CRT phosphor scanline simulation and ballistic impact vibration.");

        // Tactical Keyboard Shortcuts Cheatsheet Card
        var _kb_y = _dsp_y + 124;
        var _kb_h = 190;
        draw_set_color(make_color_rgb(12, 18, 28));
        draw_rectangle(_dsp_x, _kb_y, _dsp_x + _dsp_w, _kb_y + _kb_h, false);
        draw_set_color(make_color_rgb(32, 54, 82));
        draw_rectangle(_dsp_x, _kb_y, _dsp_x + _dsp_w, _kb_y + _kb_h, true);

        draw_set_color(make_color_rgb(255, 220, 90));
        draw_text(_dsp_x + 14, _kb_y + 12, "TACTICAL HOTKEYS & RAPID COMMAND SHORTCUTS:");

        var _shortcuts = [
            { key: "[M]", desc: "Toggle Master Audio Mute (Instant on/off anytime)" },
            { key: "[O]", desc: "Open / Close this System Settings & Audio Window" },
            { key: "[ESC]", desc: "Dismiss active modal window or return to command deck" },
            { key: "[F5]", desc: "Quick Save game state to local persistent memory" },
            { key: "[F9]", desc: "Quick Load last saved PMC career state" },
            { key: "[1 - 5]", desc: "Direct switch: 1:R&D, 2:Factory, 3:Board, 4:War Map, 5:Hangar" },
            { key: "[L]", desc: "Open Turn Ledger & Transaction Briefing modal" },
            { key: "[?] / [F1]", desc: "Access the Field Manual & Tutorial Codex" }
        ];

        for (var ki = 0; ki < array_length(_shortcuts); ki++) {
            var _sc = _shortcuts[ki];
            var _row = ki % 4;
            var _col = floor(ki / 4);
            var _rx = _dsp_x + 18 + _col * 360;
            var _ry = _kb_y + 40 + _row * 34;

            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_rx, _ry, _sc.key);
            draw_set_color(make_color_rgb(200, 220, 240));
            draw_text(_rx + 74, _ry, _sc.desc);
        }
    }

    // =====================================================================
    // BOTTOM CLOSE / CONFIRM BUTTON
    // =====================================================================
    var _btn_close_w = 260;
    var _btn_close_h = 38;
    var _btn_close_x = _mx0 + floor((_mw - _btn_close_w) / 2);
    var _btn_close_y = _my0 + _mh - 52;
    var _bc_hov = (_mx >= _btn_close_x && _mx <= _btn_close_x + _btn_close_w && _my >= _btn_close_y && _my <= _btn_close_y + _btn_close_h);

    if (_bc_hov && _click) {
        show_settings_modal = false;
        scr_audio_play_ui("confirm");
    }
    scr_draw_snes_button(_btn_close_x, _btn_close_y, _btn_close_w, _btn_close_h, ">> CLOSE SETTINGS <<", _bc_hov, false, make_color_rgb(60, 240, 140));
}
'''

if "show_settings_modal" not in c:
    c = c + settings_modal_code
    print("Settings modal appended to Draw_64.gml.")

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

print("obj_HQTerminal/Draw_64.gml fully patched.")
