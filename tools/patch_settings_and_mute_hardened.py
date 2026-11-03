#!/usr/bin/env python3
import os
import re

print("[PATCH] Applying Hardened Audio Muting and Settings Modal System...")

# 1. Patch rooms/rm_init/RoomCreationCode.gml
path_rm_init = "rooms/rm_init/RoomCreationCode.gml"
with open(path_rm_init, "r", encoding="utf-8") as f:
    rm_code = f.read()

if "audio_master_gain(0.0);" not in rm_code:
    rm_code = "audio_master_gain(0.0);\n" + rm_code
    with open(path_rm_init, "w", encoding="utf-8") as f:
        f.write(rm_code)
    print("✓ rooms/rm_init/RoomCreationCode.gml prepended with audio_master_gain(0.0);")
else:
    print("rooms/rm_init/RoomCreationCode.gml already has audio_master_gain(0.0);")

# 2. Patch objects/obj_AudioManager/Create_0.gml
path_audio_create = "objects/obj_AudioManager/Create_0.gml"
with open(path_audio_create, "r", encoding="utf-8") as f:
    ac = f.read()

# Ensure master_muted = true, bgm_muted = true, sfx_muted = true, audio_master_gain(0.0), audio_stop_all()
ac_new = re.sub(
    r"master_muted\s*=\s*[^;]+;",
    "master_muted = true;",
    ac
)
ac_new = re.sub(
    r"bgm_muted\s*=\s*[^;]+;",
    "bgm_muted = true;",
    ac_new
)
ac_new = re.sub(
    r"sfx_muted\s*=\s*[^;]+;",
    "sfx_muted = true;",
    ac_new
)
if "audio_stop_all();" not in ac_new:
    ac_new = ac_new.replace("audio_master_gain(0.0);", "audio_master_gain(0.0);\naudio_stop_all();")

with open(path_audio_create, "w", encoding="utf-8") as f:
    f.write(ac_new)
print("✓ objects/obj_AudioManager/Create_0.gml hardened to default muted.")

# 3. Patch objects/obj_AudioManager/Step_0.gml
path_audio_step = "objects/obj_AudioManager/Step_0.gml"
with open(path_audio_step, "r", encoding="utf-8") as f:
    astep = f.read()

if "if (master_muted) audio_master_gain(0.0);" not in astep:
    astep = "if (master_muted) audio_master_gain(0.0);\n" + astep
    with open(path_audio_step, "w", encoding="utf-8") as f:
        f.write(astep)
    print("✓ objects/obj_AudioManager/Step_0.gml enforces 0.0 master gain.")

# 4. Patch scripts/scr_audio_manager/scr_audio_manager.gml
path_scr_audio = "scripts/scr_audio_manager/scr_audio_manager.gml"
with open(path_scr_audio, "r", encoding="utf-8") as f:
    sa = f.read()

# Make sure scr_audio_play_bgm checks for muted before playing
old_play_bgm = '''function scr_audio_play_bgm(_bgm_asset, _fade_ms = 800, _loop = true) {
    if (!audio_exists(_bgm_asset)) return;
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) {
        _mgr.play_bgm(_bgm_asset, _fade_ms, _loop);
    } else {
        audio_play_sound(_bgm_asset, 10, _loop);
    }
}'''

new_play_bgm = '''function scr_audio_play_bgm(_bgm_asset, _fade_ms = 800, _loop = true) {
    if (!audio_exists(_bgm_asset)) return;
    var _mgr = scr_audio_ensure_manager();
    if (_mgr != noone) {
        _mgr.play_bgm(_bgm_asset, _fade_ms, _loop);
    } else {
        if (!scr_audio_is_muted()) {
            audio_play_sound(_bgm_asset, 10, _loop);
        }
    }
}'''

if old_play_bgm in sa:
    sa = sa.replace(old_play_bgm, new_play_bgm)
    with open(path_scr_audio, "w", encoding="utf-8") as f:
        f.write(sa)
    print("✓ scr_audio_manager.gml updated play_bgm safety.")

# 5. Patch objects/obj_HQTerminal/Draw_64.gml top bar
path_hq_draw = "objects/obj_HQTerminal/Draw_64.gml"
with open(path_hq_draw, "r", encoding="utf-8") as f:
    hqd = f.read()

target_top_bar = '''// Career Retirement Button (x: 938, w: 68)
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
draw_text(_cfg_btn_x + 8 + _sx, _et_y + 24 + _sy, _is_aud_muted ? "AUDIO OFF" : "VOL " + string(floor(scr_audio_get_master_volume() * 100)) + "%");

// 5. Commander Profile Dossier Badge (x: 1114 to 1348, w: 234, h: 48, y: 8)
var _cmd_bx = 1114 + _sx;
var _cmd_by = 8 + _sy;
var _cmd_bw = 234;'''

replacement_top_bar = '''// Career Retirement Button (x: 936, w: 62)
var _ret_btn_x = 936;
var _ret_btn_w = 62;
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

// Dedicated Mute Toggle Button (x: 1004, w: 74, h: 44, y: 10)
var _mute_btn_x = 1004;
var _mute_btn_w = 74;
var _is_aud_muted = scr_audio_is_muted();
var _mute_hov = (_mx >= _mute_btn_x && _mx <= _mute_btn_x + _mute_btn_w && _my >= _et_y && _my <= _et_y + _hud_btn_h);
if (_mute_hov && _click) {
    var _nm = scr_audio_toggle_mute();
    show_toast(_nm ? "[AUDIO MUTED]" : "[AUDIO UNMUTED - " + string(floor(scr_audio_get_master_volume() * 100)) + "%]", _nm ? c_orange : c_lime);
}
draw_set_color(_mute_hov ? (_is_aud_muted ? make_color_rgb(82, 26, 26) : make_color_rgb(20, 64, 42)) : (_is_aud_muted ? make_color_rgb(46, 14, 14) : make_color_rgb(12, 34, 22)));
draw_rectangle(_mute_btn_x + _sx, _et_y + _sy, _mute_btn_x + _mute_btn_w + _sx, _et_y + _hud_btn_h + _sy, false);
draw_set_color(_mute_hov ? (_is_aud_muted ? make_color_rgb(255, 110, 110) : make_color_rgb(100, 255, 160)) : (_is_aud_muted ? make_color_rgb(220, 65, 65) : make_color_rgb(50, 190, 100)));
draw_rectangle(_mute_btn_x + _sx, _et_y + _sy, _mute_btn_x + _mute_btn_w + _sx, _et_y + _hud_btn_h + _sy, true);
// Left Strip Indicator
draw_set_color(_is_aud_muted ? make_color_rgb(255, 50, 50) : make_color_rgb(40, 240, 120));
draw_rectangle(_mute_btn_x + _sx, _et_y + _sy, _mute_btn_x + _sx + 3, _et_y + _hud_btn_h + _sy, false);

draw_set_color(_is_aud_muted ? make_color_rgb(255, 140, 140) : make_color_rgb(140, 255, 180));
draw_text(_mute_btn_x + 7 + _sx, _et_y + 8 + _sy, _is_aud_muted ? "[🔇 MUTE]" : "[🔊 AUDIO]");
draw_set_color(_is_aud_muted ? make_color_rgb(255, 190, 100) : make_color_rgb(100, 255, 140));
draw_text(_mute_btn_x + 7 + _sx, _et_y + 24 + _sy, _is_aud_muted ? "MUTED [M]" : "VOL " + string(floor(scr_audio_get_master_volume() * 100)) + "%");

// Dedicated Settings Modal Button (x: 1084, w: 74, h: 44, y: 10)
var _cfg_btn_x = 1084;
var _cfg_btn_w = 74;
var _cfg_hov = (_mx >= _cfg_btn_x && _mx <= _cfg_btn_x + _cfg_btn_w && _my >= _et_y && _my <= _et_y + _hud_btn_h);
if (_cfg_hov && _click) {
    show_settings_modal = !show_settings_modal;
    scr_audio_play_ui("click");
}
draw_set_color(_cfg_hov ? make_color_rgb(20, 48, 70) : make_color_rgb(12, 22, 34));
draw_rectangle(_cfg_btn_x + _sx, _et_y + _sy, _cfg_btn_x + _cfg_btn_w + _sx, _et_y + _hud_btn_h + _sy, false);
draw_set_color(_cfg_hov ? make_color_rgb(100, 220, 255) : make_color_rgb(55, 130, 190));
draw_rectangle(_cfg_btn_x + _sx, _et_y + _sy, _cfg_btn_x + _cfg_btn_w + _sx, _et_y + _hud_btn_h + _sy, true);
// Left Strip Indicator
draw_set_color(make_color_rgb(0, 220, 255));
draw_rectangle(_cfg_btn_x + _sx, _et_y + _sy, _cfg_btn_x + _sx + 3, _et_y + _hud_btn_h + _sy, false);

draw_set_color(make_color_rgb(120, 220, 255));
draw_text(_cfg_btn_x + 7 + _sx, _et_y + 8 + _sy, "[⚙ CONFIG]");
draw_set_color(make_color_rgb(180, 210, 240));
draw_text(_cfg_btn_x + 7 + _sx, _et_y + 24 + _sy, "SETTING [O]");

// 5. Commander Profile Dossier Badge (x: 1164 to 1348, w: 184, h: 48, y: 8)
var _cmd_bx = 1164 + _sx;
var _cmd_by = 8 + _sy;
var _cmd_bw = 184;'''

if target_top_bar in hqd:
    hqd = hqd.replace(target_top_bar, replacement_top_bar, 1)
    print("✓ obj_HQTerminal/Draw_64.gml top bar upgraded with dedicated MUTE & CONFIG buttons.")
else:
    print("WARNING: target_top_bar not found in Draw_64.gml!")

# Now check if Settings modal drawing code exists in obj_HQTerminal/Draw_64.gml
modal_marker = "// 8. SYSTEM CONFIGURATION & TACTICAL AUDIO MODAL"
if modal_marker not in hqd:
    settings_modal_drawing = '''

// =========================================================================
// 8. SYSTEM CONFIGURATION & TACTICAL AUDIO MODAL (LEAD AUDIO ENGINEER SPEC)
// =========================================================================
if (show_settings_modal) {
    // 1. Full Screen Backdrop Dimmer
    draw_set_alpha(0.80);
    draw_set_color(c_black);
    draw_rectangle(0, 0, 1366, 768, false);
    draw_set_alpha(1.0);

    // 2. Modal Dimensions (800x540 centered on 1366x768 -> x: 283, y: 114)
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

        draw_set_color(_hero_hov ? (_is_muted ? make_color_rgb(90, 28, 28) : make_color_rgb(20, 70, 95)) : (_is_muted ? make_color_rgb(52, 16, 16) : make_color_rgb(14, 38, 54)));
        draw_rectangle(_hero_x, _hero_y, _hero_x + _hero_w, _hero_y + _hero_h, false);
        draw_set_color(_hero_hov ? (_is_muted ? make_color_rgb(255, 120, 120) : make_color_rgb(80, 255, 180)) : (_is_muted ? make_color_rgb(220, 60, 60) : make_color_rgb(0, 220, 255)));
        draw_rectangle(_hero_x, _hero_y, _hero_x + _hero_w, _hero_y + _hero_h, true);

        // Accent indicator block
        draw_set_color(_is_muted ? make_color_rgb(255, 50, 50) : make_color_rgb(0, 255, 150));
        draw_rectangle(_hero_x + 4, _hero_y + 4, _hero_x + 12, _hero_y + _hero_h - 4, false);

        draw_set_color(_is_muted ? make_color_rgb(255, 140, 140) : make_color_rgb(0, 240, 255));
        draw_text(_hero_x + 24, _hero_y + 10, _is_muted ? "[!] MASTER AUDIO IS CURRENTLY MUTED (DEFAULT)" : "[✓] MASTER AUDIO IS ACTIVE & OPERATIONAL");
        draw_set_color(c_white);
        draw_text(_hero_x + 24, _hero_y + 30, _is_muted ? ">> CLICK HERE TO UNMUTE ALL AUDIO CHANNELS (Or press [M] on keyboard) <<" : ">> CLICK HERE TO MUTE ALL AUDIO (Silent Running Mode) <<");

        // 2. MASTER VOLUME CHANNEL
        var _ch_y = _hero_y + _hero_h + 16;
        var _ch_w = _hero_w;
        var _ch_h = 74;

        draw_set_color(make_color_rgb(12, 18, 28));
        draw_rectangle(_hero_x, _ch_y, _hero_x + _ch_w, _ch_y + _ch_h, false);
        draw_set_color(make_color_rgb(32, 54, 82));
        draw_rectangle(_hero_x, _ch_y, _hero_x + _ch_w, _ch_y + _ch_h, true);

        draw_set_color(make_color_rgb(100, 210, 255));
        draw_text(_hero_x + 14, _ch_y + 10, "MASTER VOLUME: " + string(floor(_m_vol * 100)) + "%" + (_is_muted ? " [MUTED]" : ""));

        // Level Meter Bar
        var _bar_x = _hero_x + 210;
        var _bar_w = 160;
        var _bar_h = 16;
        draw_set_color(make_color_rgb(20, 30, 45));
        draw_rectangle(_bar_x, _ch_y + 12, _bar_x + _bar_w, _ch_y + 12 + _bar_h, false);
        var _fill_w = floor(_bar_w * (_is_muted ? 0.0 : _m_vol));
        if (_fill_w > 0) {
            draw_set_color(_is_muted ? make_color_rgb(120, 50, 50) : make_color_rgb(0, 240, 255));
            draw_rectangle(_bar_x, _ch_y + 12, _bar_x + _fill_w, _ch_y + 12 + _bar_h, false);
        }
        draw_set_color(make_color_rgb(60, 90, 130));
        draw_rectangle(_bar_x, _ch_y + 12, _bar_x + _bar_w, _ch_y + 12 + _bar_h, true);

        // Volume Presets: 0%, 25%, 50%, 75%, 100%
        var _steps = [0.0, 0.25, 0.50, 0.75, 1.0];
        var _sb_w = 64;
        var _sb_x0 = _hero_x + 390;
        for (var vi = 0; vi < 5; vi++) {
            var _sv = _steps[vi];
            var _sb_x = _sb_x0 + vi * (_sb_w + 6);
            var _sb_hov = (_mx >= _sb_x && _mx <= _sb_x + _sb_w && _my >= _ch_y + 8 && _my <= _ch_y + 34);
            var _is_act = (abs(_m_vol - _sv) < 0.05 && !_is_muted);
            if (_sb_hov && _click) {
                scr_audio_set_master_volume(_sv);
                if (_sv > 0 && _is_muted) scr_audio_set_muted(false);
                scr_audio_play_ui("click");
            }
            scr_draw_snes_button(_sb_x, _ch_y + 8, _sb_w, 26, string(floor(_sv * 100)) + "%", _sb_hov || _is_act, _is_act, _is_act ? make_color_rgb(100, 255, 180) : c_white);
        }
        draw_set_color(make_color_rgb(150, 180, 210));
        draw_text(_hero_x + 14, _ch_y + 44, "Controls overall output gain for all sound channels via GameMaker audio listener.");

        // 3. BGM (MUSIC SCORE) CHANNEL
        var _ch2_y = _ch_y + _ch_h + 10;
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
            draw_set_color(_b_muted ? make_color_rgb(120, 50, 50) : make_color_rgb(255, 200, 80));
            draw_rectangle(_bar_x, _ch2_y + 12, _bar_x + _b_fill, _ch2_y + 12 + _bar_h, false);
        }
        draw_set_color(make_color_rgb(60, 90, 130));
        draw_rectangle(_bar_x, _ch2_y + 12, _bar_x + _bar_w, _ch2_y + 12 + _bar_h, true);

        for (var bi = 0; bi < 5; bi++) {
            var _bv = _steps[bi];
            var _bb_x = _sb_x0 + bi * (_sb_w + 6);
            var _bb_hov = (_mx >= _bb_x && _mx <= _bb_x + _bb_w && _my >= _ch2_y + 8 && _my <= _ch2_y + 34);
            var _is_act = (abs(_b_vol - _bv) < 0.05 && !_b_muted);
            if (_bb_hov && _click) {
                scr_audio_set_bgm_volume(_bv);
                if (_b_muted) scr_audio_set_bgm_muted(false);
                scr_audio_play_ui("click");
            }
            scr_draw_snes_button(_bb_x, _ch2_y + 8, _sb_w, 26, string(floor(_bv * 100)) + "%", _bb_hov || _is_act, _is_act, _is_act ? make_color_rgb(100, 255, 180) : c_white);
        }

        // BGM Mute Button
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
    hqd += settings_modal_drawing
    print("✓ Appended Settings Modal rendering block to obj_HQTerminal/Draw_64.gml")
else:
    print("Settings Modal rendering block already present in obj_HQTerminal/Draw_64.gml")

with open(path_hq_draw, "w", encoding="utf-8") as f:
    f.write(hqd)
print("✓ obj_HQTerminal/Draw_64.gml completely written.")

# 6. Patch objects/obj_BattleManager/Create_0.gml and Draw_64.gml
path_bm_create = "objects/obj_BattleManager/Create_0.gml"
with open(path_bm_create, "r", encoding="utf-8") as f:
    bmc = f.read()

if "settings_crt_scanlines" not in bmc:
    bmc += "\nsettings_crt_scanlines = true;\nsettings_screen_shake = true;\n"
    with open(path_bm_create, "w", encoding="utf-8") as f:
        f.write(bmc)
    print("✓ obj_BattleManager/Create_0.gml settings variables added.")

path_bm_draw = "objects/obj_BattleManager/Draw_64.gml"
with open(path_bm_draw, "r", encoding="utf-8") as f:
    bmd = f.read()

if modal_marker not in bmd:
    bmd += settings_modal_drawing
    with open(path_bm_draw, "w", encoding="utf-8") as f:
        f.write(bmd)
    print("✓ obj_BattleManager/Draw_64.gml settings modal added.")

print("[PATCH COMPLETE] All audio and settings files successfully patched.")
