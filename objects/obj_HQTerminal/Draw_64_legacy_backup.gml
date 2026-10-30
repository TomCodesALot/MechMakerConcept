/// @description obj_HQTerminal Draw GUI Event
// Unified Command Deck Terminal HUD, Interactive R&D Lab, Crucible, Base Management, Faction Contracts & War Map
// Strictly implements docs/01, 02, 03, 04, 06, 07, 08, 09

var _gw = display_get_gui_width();
var _gh = display_get_gui_height();
var _mx = device_mouse_x_to_gui(0);
var _my = device_mouse_y_to_gui(0);
var _click = mouse_check_button_pressed(mb_left);
var _down = mouse_check_button(mb_left);

// Screen Shake Offset
var _sx = random_range(-crucible_shake, crucible_shake);
var _sy = random_range(-crucible_shake, crucible_shake);

// 1. Dark Retro-Military Command Backdrop
draw_set_color(make_color_rgb(10, 14, 20));
draw_set_alpha(1.0);
draw_rectangle(0, 0, _gw, _gh, false);

// Atmospheric Location Backdrop Art (Hangar Bay for Tabs 0-1, War Room for Tabs 2-4)
var _loc_bg = (active_tab == 0 || active_tab == 1) ? spr_loc_hangar_bay : spr_loc_war_room;
if (sprite_exists(_loc_bg)) {
    draw_sprite_ext(_loc_bg, 0, 0, 0, _gw / 1024.0, _gh / 576.0, 0, c_white, 0.24);
}

// Subtle Background Grid
draw_set_color(make_color_rgb(18, 26, 36));
for (var gx = 0; gx < _gw; gx += 48) draw_line(gx, 0, gx, _gh);
for (var gy = 0; gy < _gh; gy += 48) draw_line(0, gy, _gw, gy);

// =========================================================================
// 2. PERSISTENT TOP HUD BAR (Top 10% - docs/09_ui_ux_flow.md)
// =========================================================================
var _hud_h = 64;
draw_set_color(make_color_rgb(14, 20, 28));
draw_rectangle(_sx, _sy, _gw + _sx, _hud_h + _sy, false);
draw_set_color(make_color_rgb(35, 60, 90));
draw_rectangle(_sx, _hud_h - 2 + _sy, _gw + _sx, _hud_h + _sy, false);

// Retrieve Manager Info
var _funds_val = 100000;
var _year_val = 214;
var _day_val = 1;
var _turn_val = 1;
if (instance_exists(obj_GameManager)) {
    _funds_val = obj_GameManager.funds;
    _year_val = obj_GameManager.current_cycle_year;
    _day_val = obj_GameManager.current_cycle_day;
    _turn_val = obj_GameManager.current_turn;
}

// Format Funds String with commas
var _f_str = string(_funds_val);
var _f_len = string_length(_f_str);
var _funds_formatted = "";
for (var _fi = 1; _fi <= _f_len; _fi++) {
    _funds_formatted += string_char_at(_f_str, _fi);
    if ((_f_len - _fi) % 3 == 0 && _fi != _f_len) {
        _funds_formatted += ",";
    }
}
_funds_formatted += " Cr";

// 1. PMC Identity Card (x: 16 to 212, w: 196, h: 48, y: 8)
var _pmc_bx = 16 + _sx;
var _pmc_by = 8 + _sy;
var _pmc_bw = 196;
var _pmc_bh = 48;
draw_set_color(make_color_rgb(14, 22, 34));
draw_rectangle(_pmc_bx, _pmc_by, _pmc_bx + _pmc_bw, _pmc_by + _pmc_bh, false);
draw_set_color(make_color_rgb(35, 65, 100));
draw_rectangle(_pmc_bx, _pmc_by, _pmc_bx + _pmc_bw, _pmc_by + _pmc_bh, true);
// Left Cyan Accent Strip
draw_set_color(make_color_rgb(80, 190, 255));
draw_rectangle(_pmc_bx, _pmc_by, _pmc_bx + 4, _pmc_by + _pmc_bh, false);
// Badge Text
draw_set_color(make_color_rgb(140, 220, 255));
draw_text(_pmc_bx + 12, _pmc_by + 8, "IRON RIDGE PMC");
draw_set_color(make_color_rgb(110, 150, 185));
draw_text(_pmc_bx + 12, _pmc_by + 26, "COMMAND DECK // T-2");

// 2. Dedicated Treasury Instrument Card (x: 220 to 396, w: 176, h: 48, y: 8)
var _tres_bx = 220 + _sx;
var _tres_by = 8 + _sy;
var _tres_bw = 176;
var _tres_bh = 48;
draw_set_color(make_color_rgb(8, 24, 16));
draw_rectangle(_tres_bx, _tres_by, _tres_bx + _tres_bw, _tres_by + _tres_bh, false);
draw_set_color(make_color_rgb(28, 90, 52));
draw_rectangle(_tres_bx, _tres_by, _tres_bx + _tres_bw, _tres_by + _tres_bh, true);
// Top Green Accent Strip
draw_set_color(make_color_rgb(50, 200, 110));
draw_rectangle(_tres_bx, _tres_by, _tres_bx + _tres_bw, _tres_by + 2, false);
// Treasury Text
draw_set_color(make_color_rgb(110, 210, 145));
draw_text(_tres_bx + 10, _tres_by + 8, "OPERATING TREASURY");
draw_set_color(make_color_rgb(70, 255, 130));
draw_text(_tres_bx + 10, _tres_by + 26, _funds_formatted);

// 3. Dedicated Strategic Calendar Card (x: 404 to 580, w: 176, h: 48, y: 8)
var _cal_bx = 404 + _sx;
var _cal_by = 8 + _sy;
var _cal_bw = 176;
var _cal_bh = 48;
draw_set_color(make_color_rgb(16, 20, 30));
draw_rectangle(_cal_bx, _cal_by, _cal_bx + _cal_bw, _cal_by + _cal_bh, false);
draw_set_color(make_color_rgb(60, 75, 105));
draw_rectangle(_cal_bx, _cal_by, _cal_bx + _cal_bw, _cal_by + _cal_bh, true);
// Top Amber Accent Strip
draw_set_color(make_color_rgb(230, 185, 70));
draw_rectangle(_cal_bx, _cal_by, _cal_bx + _cal_bw, _cal_by + 2, false);
// Calendar Text
draw_set_color(make_color_rgb(195, 180, 130));
draw_text(_cal_bx + 10, _cal_by + 8, "STRATEGIC CYCLE");
draw_set_color(make_color_rgb(255, 220, 95));
draw_text(_cal_bx + 10, _cal_by + 26, "TURN " + string(_turn_val) + " // Y" + string(_year_val) + " D" + string(_day_val));

// 4. Command Actions (x: 588 to 1108, h: 44, y: 10)
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

// Career Retirement Button (x: 936, w: 62)
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
var _cmd_bw = 184;
var _cmd_bh = 48;
var _cmd_hov = (_mx >= _cmd_bx && _mx <= _cmd_bx + _cmd_bw && _my >= _cmd_by && _my <= _cmd_by + _cmd_bh);

if (_cmd_hov && _click) {
    show_commander_modal = true;
    intro_page = 1;
    scr_audio_play_ui("click");
}

draw_set_color(_cmd_hov ? make_color_rgb(26, 46, 72) : make_color_rgb(14, 22, 34));
draw_rectangle(_cmd_bx, _cmd_by, _cmd_bx + _cmd_bw, _cmd_by + _cmd_bh, false);
draw_set_color(_cmd_hov ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 80, 120));
draw_rectangle(_cmd_bx, _cmd_by, _cmd_bx + _cmd_bw, _cmd_by + _cmd_bh, true);

// Miniature Commander Portrait
var _c_port = spr_portrait_commander_silhouette;
var _c_name = "Cmdr [CLASSIFIED]";
var _c_call = "SHADOW";
if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "player_commander")) {
    _c_port = obj_GameManager.player_commander.portrait_asset;
    _c_name = string_replace(obj_GameManager.player_commander.name, "Commander ", "Cmdr. ");
    _c_call = obj_GameManager.player_commander.callsign;
}

if (sprite_exists(_c_port)) {
    draw_sprite_ext(_c_port, 0, _cmd_bx + 4, _cmd_by + 4, 40.0 / 200.0, 40.0 / 200.0, 0, c_white, 1.0);
    draw_set_color(make_color_rgb(80, 150, 200));
    draw_rectangle(_cmd_bx + 4, _cmd_by + 4, _cmd_bx + 44, _cmd_by + 44, true);
}

draw_set_color(_cmd_hov ? c_white : make_color_rgb(200, 230, 255));
draw_text(_cmd_bx + 48, _cmd_by + 8, _c_name);
draw_set_color(make_color_rgb(120, 175, 215));
draw_text(_cmd_bx + 48, _cmd_by + 26, "[" + _c_call + "] // DOSSIER");
// =========================================================================
// 3. FRONT MISSION STYLE LEFT TACTICAL COMMAND DOCK (x: 16 to 212, y: 66 to 720)
// =========================================================================
var _dock_x = 16;
var _dock_y = 66;
var _dock_w = 196;
var _dock_h = _gh - _dock_y - 44; // ~658px tall

// Outer Dock Frame & Backdrop
scr_draw_snes_panel(_dock_x, _dock_y, _dock_w, _dock_h, "COMMAND DECK", 0, false, 0.06);

// Dock Header Ribbon
draw_set_color(make_color_rgb(14, 22, 34));
draw_rectangle(_dock_x + 8, _dock_y + 12, _dock_x + _dock_w - 8, _dock_y + 36, false);
draw_set_color(make_color_rgb(45, 75, 110));
draw_rectangle(_dock_x + 8, _dock_y + 12, _dock_x + _dock_w - 8, _dock_y + 36, true);
draw_set_color(make_color_rgb(0, 220, 255));
draw_text(_dock_x + 14, _dock_y + 16, "PMC DIRECTIVES");

// Command Menu Items (Front Mission / Gihren's Greed Style)
var _menu_tabs = [
    { id: 3, key: "[1]", title: "1. WAR ROOM", desc: "Planetary War Map" },
    { id: 1, key: "[2]", title: "2. MECH HANGAR", desc: "Assembly & Upgrades" },
    { id: 0, key: "[3]", title: "3. R&D FORGE", desc: "Alloys & Metallurgy" },
    { id: 2, key: "[4]", title: "4. CONTRACTS", desc: "Bounties & Flyoffs" },
    { id: 4, key: "[5]", title: "5. FLEET & RIVALS", desc: "Flagship & Corps" }
];

var _btn_y0 = _dock_y + 44;
var _btn_h = 52;
var _btn_gap = 8;
var _bw = _dock_w - 16;
var _bx = _dock_x + 8;

for (var mi = 0; mi < array_length(_menu_tabs); mi++) {
    var _m_item = _menu_tabs[mi];
    var _by = _btn_y0 + mi * (_btn_h + _btn_gap);
    var _is_act = (active_tab == _m_item.id);
    var _m_hov = (_mx >= _bx && _mx <= _bx + _bw && _my >= _by && _my <= _by + _btn_h);

    if (_m_hov && _click) {
        if (active_tab != _m_item.id) {
            active_tab = _m_item.id;
            scr_audio_play_ui("click");
            if (active_tab == 0) {
                scr_audio_play_location_bgm("prototyping");
            } else {
                scr_audio_play_location_bgm("hq");
            }
        }
    }

    // Button Base Fill
    draw_set_color(_is_act ? make_color_rgb(20, 54, 88) : (_m_hov ? make_color_rgb(18, 36, 56) : make_color_rgb(12, 18, 28)));
    draw_rectangle(_bx + _sx, _by + _sy, _bx + _bw + _sx, _by + _btn_h + _sy, false);

    // Border
    draw_set_color(_is_act ? make_color_rgb(0, 240, 255) : (_m_hov ? make_color_rgb(100, 200, 255) : make_color_rgb(40, 65, 95)));
    draw_rectangle(_bx + _sx, _by + _sy, _bx + _bw + _sx, _by + _btn_h + _sy, true);

    // Left Active Indicator Strip
    if (_is_act) {
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_rectangle(_bx + _sx, _by + _sy, _bx + 5 + _sx, _by + _btn_h + _sy, false);
    }

    // Text Labels
    draw_set_color(_is_act ? c_white : (_m_hov ? make_color_rgb(220, 240, 255) : make_color_rgb(160, 190, 220)));
    draw_text(_bx + 12 + _sx, _by + 8 + _sy, _m_item.title);

    draw_set_color(_is_act ? make_color_rgb(120, 220, 255) : make_color_rgb(110, 140, 170));
    draw_text(_bx + 12 + _sx, _by + 26 + _sy, _m_item.desc);

    // Keybadge on Right
    draw_set_color(_is_act ? make_color_rgb(255, 220, 80) : make_color_rgb(80, 120, 160));
    draw_text(_bx + _bw - 28 + _sx, _by + 8 + _sy, _m_item.key);
}

// Tactical Divider Line
var _div_y = _btn_y0 + 5 * (_btn_h + _btn_gap) + 8;
draw_set_color(make_color_rgb(32, 54, 82));
draw_line(_bx, _div_y, _bx + _bw, _div_y);

// --- COMBAT SORTIE BUTTON ---
var _sort_y = _div_y + 12;
var _sort_h = 50;
var _sort_hov = (_mx >= _bx && _mx <= _bx + _bw && _my >= _sort_y && _my <= _sort_y + _sort_h);
if (_sort_hov && _click && room_exists(rm_combat)) {
    scr_audio_play_ui("confirm");
    room_goto(rm_combat);
}
draw_set_color(_sort_hov ? make_color_rgb(80, 50, 10) : make_color_rgb(36, 22, 6));
draw_rectangle(_bx + _sx, _sort_y + _sy, _bx + _bw + _sx, _sort_y + _sort_h + _sy, false);
draw_set_color(_sort_hov ? make_color_rgb(255, 210, 60) : make_color_rgb(220, 160, 40));
draw_rectangle(_bx + _sx, _sort_y + _sy, _bx + _bw + _sx, _sort_y + _sort_h + _sy, true);
draw_set_color(make_color_rgb(255, 200, 40));
draw_rectangle(_bx + _sx, _sort_y + _sy, _bx + 5 + _sx, _sort_y + _sort_h + _sy, false);
draw_set_color(make_color_rgb(255, 230, 100));
draw_text(_bx + 12 + _sx, _sort_y + 8 + _sy, ">> SORTIE COMBAT <<");
draw_set_color(make_color_rgb(200, 170, 100));
draw_text(_bx + 12 + _sx, _sort_y + 26 + _sy, "Deploy Platoon [S]");

// --- ADVANCE STRATEGIC CYCLE BUTTON ---
var _adv_y = _sort_y + _sort_h + 10;
var _adv_h = 50;
var _adv_hov = (_mx >= _bx && _mx <= _bx + _bw && _my >= _adv_y && _my <= _adv_y + _adv_h);
if (_adv_hov && _click && instance_exists(obj_GameManager)) {
    obj_GameManager.end_turn();
}
draw_set_color(_adv_hov ? make_color_rgb(18, 64, 36) : make_color_rgb(10, 32, 18));
draw_rectangle(_bx + _sx, _adv_y + _sy, _bx + _bw + _sx, _adv_y + _adv_h + _sy, false);
draw_set_color(_adv_hov ? make_color_rgb(60, 240, 140) : make_color_rgb(40, 180, 95));
draw_rectangle(_bx + _sx, _adv_y + _sy, _bx + _bw + _sx, _adv_y + _adv_h + _sy, true);
draw_set_color(make_color_rgb(0, 240, 120));
draw_rectangle(_bx + _sx, _adv_y + _sy, _bx + 5 + _sx, _adv_y + _adv_h + _sy, false);
draw_set_color(make_color_rgb(120, 255, 170));
draw_text(_bx + 12 + _sx, _adv_y + 8 + _sy, ">> ADVANCE DAY <<");
draw_set_color(make_color_rgb(100, 200, 140));
draw_text(_bx + 12 + _sx, _adv_y + 26 + _sy, "Next Strategic Cycle [SPACE]");

// Dock Footer Status
var _foot_y = _dock_y + _dock_h - 40;
draw_set_color(make_color_rgb(14, 20, 30));
draw_rectangle(_bx, _foot_y, _bx + _bw, _foot_y + 32, false);
draw_set_color(make_color_rgb(30, 50, 75));
draw_rectangle(_bx, _foot_y, _bx + _bw, _foot_y + 32, true);
draw_set_color(make_color_rgb(80, 220, 140));
draw_text(_bx + 8, _foot_y + 8, "PMC STATUS: READY");

// =========================================================================
// 4. MAIN WORKSPACE PANELS (Gihren's Greed Center Stage)
// =========================================================================
var _pan_x = 220;
var _pan_y = 66;
var _pan_w = _gw - _pan_x - 16; // 1130 px
var _pan_h = _gh - _pan_y - 44; // 658 px

draw_set_color(make_color_rgb(12, 18, 26));
draw_rectangle(_pan_x + _sx, _pan_y + _sy, _pan_x + _pan_w + _sx, _pan_y + _pan_h + _sy, false);
draw_set_color(make_color_rgb(30, 50, 75));
draw_rectangle(_pan_x + _sx, _pan_y + _sy, _pan_x + _pan_w + _sx, _pan_y + _pan_h + _sy, true);

// -------------------------------------------------------------------------
// TAB 0: R&D LAB // ALLOY CHEMISTRY & PROTOTYPING MINIGAMES (Docs 02 & 03)
// -------------------------------------------------------------------------
if (active_tab == 0) {
    var _sub_tabs = [
        "[1. ALLOY CRUCIBLE SYNTHESIS]",
        "[2. PROTOTYPING MINIGAMES]",
        "[3. BLUEPRINT ARCHIVE]"
    ];
    var _sub_w = floor((_pan_w - 48) / 3);
    var _sub_y = _pan_y + 8;
    for (var stb = 0; stb < 3; stb++) {
        var _stbx = _pan_x + 16 + stb * (_sub_w + 12);
        var _stb_active = (rd_subtab == stb);
        var _stb_hov = (_mx >= _stbx && _mx <= _stbx + _sub_w && _my >= _sub_y && _my <= _sub_y + 28);
        if (_stb_hov && _click) { rd_subtab = stb; scr_audio_play_ui("click"); }

        draw_set_color(_stb_active ? make_color_rgb(30, 70, 110) : (_stb_hov ? make_color_rgb(20, 40, 60) : make_color_rgb(14, 22, 32)));
        draw_rectangle(_stbx + _sx, _sub_y + _sy, _stbx + _sub_w + _sx, _sub_y + 28 + _sy, false);
        draw_set_color(_stb_active ? make_color_rgb(100, 200, 255) : make_color_rgb(45, 75, 110));
        draw_rectangle(_stbx + _sx, _sub_y + _sy, _stbx + _sub_w + _sx, _sub_y + 28 + _sy, true);
        draw_set_color(_stb_active ? c_white : make_color_rgb(160, 190, 220));
        draw_text(_stbx + 14 + _sx, _sub_y + 6 + _sy, _sub_tabs[stb]);
    }

    // ---------------------------------------------------------------------
    // SUB-TAB 0: CRUCIBLE ALLOY SYNTHESIS (docs/02_alloy_chemistry.md)
    // ---------------------------------------------------------------------
    if (rd_subtab == 0) {
        var _c_x = _pan_x + 20;
        var _c_y = _pan_y + 44;
        var _c_w = 640;
        var _c_h = _pan_h - 56;

        draw_set_color(make_color_rgb(8, 12, 16));
        draw_rectangle(_c_x + _sx, _c_y + _sy, _c_x + _c_w + _sx, _c_y + _c_h + _sy, false);
        draw_set_color(make_color_rgb(40, 65, 95));
        draw_rectangle(_c_x + _sx, _c_y + _sy, _c_x + _c_w + _sx, _c_y + _c_h + _sy, true);

        draw_set_color(make_color_rgb(100, 210, 255));
        draw_text(_c_x + 16 + _sx, _c_y + 12 + _sy, "== R&D THERMAL CRUCIBLE // ALLOY SYNTHESIS ==");

        // Crucible Tutorial Button on Header
        var _tut_btn_x = _c_x + _c_w - 180;
        var _tut_btn_y = _c_y + 8;
        var _tut_hov = (_mx >= _tut_btn_x && _mx <= _tut_btn_x + 165 && _my >= _tut_btn_y && _my <= _tut_btn_y + 26);
        if (_tut_hov && _click) active_tutorial_modal = "CRUCIBLE";
        draw_set_color(_tut_hov ? make_color_rgb(80, 55, 20) : make_color_rgb(40, 28, 12));
        draw_rectangle(_tut_btn_x, _tut_btn_y, _tut_btn_x + 165, _tut_btn_y + 26, false);
        draw_set_color(make_color_rgb(255, 180, 60));
        draw_rectangle(_tut_btn_x, _tut_btn_y, _tut_btn_x + 165, _tut_btn_y + 26, true);
        draw_set_color(c_white);
        draw_text(_tut_btn_x + 10, _tut_btn_y + 5, "[?] CRUCIBLE TUTORIAL");

        // Chamber Visualizer (16-Bit Front Mission Animated Thermal Furnace)
        var _win_x = _c_x + 24;
        var _win_y = _c_y + 44;
        var _win_w = 260;
        var _win_h = 220;

        // 1. Heavy Industrial Beveled Frame Housing
        scr_draw_snes_panel(_win_x + _sx, _win_y + _sy, _win_w, _win_h, "THERMAL CORE", make_color_rgb(255, 120, 40), true);

        // 2. High-Temperature Quartz Observation Viewport
        var _qz_x = _win_x + 10 + _sx;
        var _qz_y = _win_y + 28 + _sy;
        var _qz_w = _win_w - 20;
        var _qz_h = _win_h - 38;

        draw_set_color(make_color_rgb(8, 12, 16));
        draw_rectangle(_qz_x, _qz_y, _qz_x + _qz_w, _qz_y + _qz_h, false);

        // Heat Incandescence Glow Dynamics
        var _temp_norm = clamp((crucible_temp_c - 25.0) / 4975.0, 0, 1);
        var _glow_r = lerp(45, 255, _temp_norm);
        var _glow_g = lerp(20, 200, clamp((_temp_norm - 0.2) * 1.25, 0, 1));
        var _glow_b = lerp(15, 255, clamp((_temp_norm - 0.7) * 3.3, 0, 1));
        var _core_glow_col = make_color_rgb(_glow_r, _glow_g, _glow_b);

        // Convection Molten Magma Bed (Undulating Wave Layer)
        var _bed_h = 32 + (_temp_norm * 40);
        var _bed_y = _qz_y + _qz_h - _bed_h;
        for (var bx = 0; bx < _qz_w; bx += 4) {
            var _wave_off = sin((current_time * 0.004) + (bx * 0.08)) * (3 + _temp_norm * 4);
            var _wave_top = clamp(_bed_y + _wave_off, _qz_y + 10, _qz_y + _qz_h - 2);
            draw_set_color(_core_glow_col);
            draw_set_alpha(0.75 + _temp_norm * 0.25);
            draw_rectangle(_qz_x + bx, _wave_top, _qz_x + bx + 3, _qz_y + _qz_h, false);
        }
        draw_set_alpha(1.0);

        // Radial Thermal Corona in Center
        draw_set_color(_core_glow_col);
        draw_set_alpha(0.20 + _temp_norm * 0.55);
        draw_circle(_qz_x + _qz_w / 2, _qz_y + _qz_h / 2, 28 + _temp_norm * 42, false);
        draw_set_alpha(1.0);

        // Dynamic Procedural Elemental Reaction Sparks
        var _spark_col = make_color_rgb(255, 140, 40);
        if (crucible_batch.mat_tritium > 0) _spark_col = make_color_rgb(0, 245, 255);
        else if (crucible_batch.mat_syn_flux > 0) _spark_col = make_color_rgb(255, 185, 50);
        else if (crucible_batch.mat_tungsten > 0) _spark_col = make_color_rgb(230, 240, 255);
        else if (crucible_batch.mat_silica_carb > 0) _spark_col = make_color_rgb(110, 140, 175);

        var _total_loaded = crucible_batch.mat_tungsten + crucible_batch.mat_silica_carb + crucible_batch.mat_tritium + crucible_batch.mat_syn_flux;
        var _spark_count = clamp(_total_loaded * 3 + floor(_temp_norm * 8), 4, 16);

        gpu_set_blendmode(bm_add);
        for (var sp = 0; sp < _spark_count; sp++) {
            var _sp_seed = sp * 73 + floor(current_time * 0.06);
            var _sp_norm_y = frac((current_time * 0.0012) + (sp / _spark_count));
            var _sp_x = _qz_x + 8 + ((_sp_seed mod (_qz_w - 16)));
            var _sp_y = _qz_y + _qz_h - (_sp_norm_y * (_qz_h - 10));

            if (sprite_exists(spr_fx_spark)) {
                draw_sprite_ext(spr_fx_spark, (current_time div 80) mod 4, _sp_x, _sp_y, 0.35, 0.35, sp * 45, _spark_col, 0.85);
            } else {
                draw_set_color(_spark_col);
                draw_set_alpha(0.85);
                draw_circle(_sp_x, _sp_y, 2, false);
                draw_set_alpha(1.0);
            }
        }
        gpu_set_blendmode(bm_normal);

        // Top Pressure Relief Steam Vents
        if (crucible_shake > 0 || crucible_pressure_psi > 6000.0) {
            draw_set_color(c_white);
            draw_set_alpha(0.40);
            for (var sv = 0; sv < 3; sv++) {
                var _svx = _qz_x + 20 + sv * 40;
                draw_line(_svx, _qz_y + 4, _svx + random_range(-4, 4), _qz_y + 24);
            }
            draw_set_alpha(1.0);
        }

        // Viewport Inner Border & Bevel
        draw_set_color(make_color_rgb(20, 28, 38));
        draw_rectangle(_qz_x, _qz_y, _qz_x + _qz_w, _qz_y + _qz_h, true);
        draw_set_color(make_color_rgb(70, 95, 125));
        draw_rectangle(_qz_x - 1, _qz_y - 1, _qz_x + _qz_w + 1, _qz_y + _qz_h + 1, true);

        // =====================================================================
        // Segmented SNES LED Gauges (Front Mission / Gihren's Greed Telemetry)
        // =====================================================================
        var _gauge_x = _win_x + _win_w + 24;
        var _gauge_y = _win_y;
        var _gw_w = 280;

        // 1. Temperature Gauge
        var _temp_col = (crucible_temp_c >= 2200 && crucible_temp_c <= 2500) ? c_lime : ((crucible_temp_c >= 4000 && crucible_temp_c <= 4950) ? c_aqua : ((crucible_temp_c > 2500 && crucible_temp_c < 4000) ? make_color_rgb(255, 180, 80) : make_color_rgb(255, 100, 60)));
        draw_set_color(c_white);
        draw_text(_gauge_x, _gauge_y, "CHAMBER TEMPERATURE:");
        draw_set_color(_temp_col);
        draw_text(_gauge_x, _gauge_y + 18, string(floor(crucible_temp_c)) + " °C  [OP RANGE: 1700 - 4950°C]");
        scr_draw_snes_gauge(_gauge_x, _gauge_y + 38, _gw_w, 16, crucible_temp_c, 5000.0, _temp_col, -1, 6);

        // 2. Pressure Gauge
        var _psi_norm = clamp(crucible_pressure_psi / 10000.0, 0, 1);
        var _psi_col = (crucible_pressure_psi > 1200 && crucible_batch.mat_silica_carb > 0 && crucible_batch.mat_tritium == 0) ? c_red : ((crucible_pressure_psi >= 4000) ? make_color_rgb(100, 240, 255) : make_color_rgb(120, 200, 255));
        draw_set_color(c_white);
        draw_text(_gauge_x, _gauge_y + 64, "PRESSURE CHAMBER:");
        draw_set_color(_psi_col);
        draw_text(_gauge_x, _gauge_y + 82, string(floor(crucible_pressure_psi)) + " PSI  [VAC <800 | COMP >4000]");
        scr_draw_snes_gauge(_gauge_x, _gauge_y + 102, _gw_w, 16, crucible_pressure_psi, 10000.0, _psi_col, -1, 6);

        // 3. Volatility Gauge
        var _vol_col = (volatility_meter > 70) ? c_red : ((volatility_meter > 35) ? c_yellow : c_lime);
        draw_set_color(c_white);
        draw_text(_gauge_x, _gauge_y + 128, "CHEMICAL VOLATILITY:");
        draw_set_color(_vol_col);
        draw_text(_gauge_x, _gauge_y + 146, string(floor(volatility_meter)) + " %  [BREACH LIMIT: 90%]");

        if (volatility_meter > 70) {
            scr_draw_snes_hazard_bar(_gauge_x, _gauge_y + 164, _gw_w, 8, true);
            scr_draw_snes_gauge(_gauge_x, _gauge_y + 174, _gw_w, 14, volatility_meter, 100.0, _vol_col, -1, 6);
        } else {
            scr_draw_snes_gauge(_gauge_x, _gauge_y + 166, _gw_w, 16, volatility_meter, 100.0, _vol_col, -1, 6);
        }

        // Discrete Step Thermal & Pressure Controls
        var _act_y = _win_y + _win_h + 18;
        var _abw = 140;
        var _abh = 36;

        // + HEAT
        var _h1_hov = (_mx >= _win_x && _mx <= _win_x + _abw && _my >= _act_y && _my <= _act_y + _abh);
        if (_h1_hov && _click) crucible_heat(400);
        draw_set_color(_h1_hov ? make_color_rgb(90, 35, 15) : make_color_rgb(45, 18, 10));
        draw_rectangle(_win_x, _act_y, _win_x + _abw, _act_y + _abh, false);
        draw_set_color(make_color_rgb(255, 110, 40));
        draw_rectangle(_win_x, _act_y, _win_x + _abw, _act_y + _abh, true);
        draw_set_color(c_white);
        draw_text(_win_x + 14, _act_y + 10, "[+ HEAT 400°C]");

        // - COOL
        var _c1_x = _win_x + _abw + 12;
        var _c1_hov = (_mx >= _c1_x && _mx <= _c1_x + _abw && _my >= _act_y && _my <= _act_y + _abh);
        if (_c1_hov && _click) crucible_cool(400);
        draw_set_color(_c1_hov ? make_color_rgb(20, 60, 90) : make_color_rgb(14, 30, 48));
        draw_rectangle(_c1_x, _act_y, _c1_x + _abw, _act_y + _abh, false);
        draw_set_color(make_color_rgb(80, 180, 255));
        draw_rectangle(_c1_x, _act_y, _c1_x + _abw, _act_y + _abh, true);
        draw_set_color(c_white);
        draw_text(_c1_x + 14, _act_y + 10, "[- COOL 400°C]");

        // + COMPRESS
        var _p1_x = _c1_x + _abw + 12;
        var _p1_hov = (_mx >= _p1_x && _mx <= _p1_x + _abw && _my >= _act_y && _my <= _act_y + _abh);
        if (_p1_hov && _click) crucible_compress(800);
        draw_set_color(_p1_hov ? make_color_rgb(60, 35, 75) : make_color_rgb(30, 18, 42));
        draw_rectangle(_p1_x, _act_y, _p1_x + _abw, _act_y + _abh, false);
        draw_set_color(make_color_rgb(180, 100, 240));
        draw_rectangle(_p1_x, _act_y, _p1_x + _abw, _act_y + _abh, true);
        draw_set_color(c_white);
        draw_text(_p1_x + 10, _act_y + 10, "[+ COMP 800 PSI]");

        // - VENT PRESSURE
        var _v1_x = _p1_x + _abw + 12;
        var _v1_hov = (_mx >= _v1_x && _mx <= _v1_x + _abw && _my >= _act_y && _my <= _act_y + _abh);
        if (_v1_hov && _click) crucible_vent();
        draw_set_color(_v1_hov ? make_color_rgb(25, 75, 70) : make_color_rgb(14, 38, 35));
        draw_rectangle(_v1_x, _act_y, _v1_x + _abw, _act_y + _abh, false);
        draw_set_color(make_color_rgb(60, 220, 200));
        draw_rectangle(_v1_x, _act_y, _v1_x + _abw, _act_y + _abh, true);
        draw_set_color(c_white);
        draw_text(_v1_x + 10, _act_y + 10, "[- VENT VALVES]");

        // Raw Material Hopper Section
        var _hop_y = _act_y + _abh + 18;
        draw_set_color(make_color_rgb(240, 210, 100));
        draw_text(_win_x, _hop_y, "BATCH INGREDIENT HOPPER & WAREHOUSE LOADING:");

        var _mats = ["mat_tungsten", "mat_silica_carb", "mat_tritium", "mat_syn_flux"];
        var _mat_names = ["Tungsten", "Silica-Carbon", "Tritium", "Synth-Flux"];
        var _mat_sprs = [spr_icon_tungsten, spr_icon_silica, spr_icon_tritium, spr_icon_flux];

        for (var mi = 0; mi < 4; mi++) {
            var _mx_box = _win_x + mi * 148;
            var _my_box = _hop_y + 24;

            draw_set_color(make_color_rgb(14, 20, 28));
            draw_rectangle(_mx_box, _my_box, _mx_box + 138, _my_box + 76, false);
            draw_set_color(make_color_rgb(35, 55, 80));
            draw_rectangle(_mx_box, _my_box, _mx_box + 138, _my_box + 76, true);

            // Material Icon
            if (sprite_exists(_mat_sprs[mi])) {
                draw_sprite_ext(_mat_sprs[mi], 0, _mx_box + 8, _my_box + 8, 0.45, 0.45, 0, c_white, 1.0);
            }

            draw_set_color(c_white);
            draw_text(_mx_box + 48, _my_box + 8, _mat_names[mi]);
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_mx_box + 48, _my_box + 26, "Loaded: " + string(variable_struct_get(crucible_batch, _mats[mi])));

            // Load Button
            var _lb_y = _my_box + 46;
            var _lb_hov = (_mx >= _mx_box + 8 && _mx <= _mx_box + 130 && _my >= _lb_y && _my <= _lb_y + 24);
            if (_lb_hov && _click) crucible_load_mat(_mats[mi]);
            scr_draw_snes_button(_mx_box + 8, _lb_y, 122, 24, "[+1 LOAD]", _lb_hov, false, make_color_rgb(60, 200, 100));
        }

        // Action: Purge & Execute Synthesis Buttons
        var _exec_y = _hop_y + 112;
        var _purg_hov = (_mx >= _win_x && _mx <= _win_x + 180 && _my >= _exec_y && _my <= _exec_y + 38);
        if (_purg_hov && _click) crucible_purge_hopper();
        scr_draw_snes_button(_win_x, _exec_y, 180, 38, "[PURGE HOPPER]", _purg_hov, false, make_color_rgb(240, 80, 80));

        var _syn_btn_x = _win_x + 196;
        var _syn_btn_w = 398;
        var _syn_hov = (_mx >= _syn_btn_x && _mx <= _syn_btn_x + _syn_btn_w && _my >= _exec_y && _my <= _exec_y + 38);
        if (_syn_hov && _click) crucible_execute_synthesis();
        scr_draw_snes_button(_syn_btn_x, _exec_y, _syn_btn_w, 38, ">> EXECUTE ALLOY SYNTHESIS BATCH <<", _syn_hov, false, make_color_rgb(60, 240, 120));

        // =========================================================================
        // RIGHT PANEL: CHROMATIC ALLOY METALLURGY CODEX & LIVE COLOR PREVIEW (DOC 14)
        // =========================================================================
        var _met_x = _c_x + _c_w + 20;
        var _met_y = _c_y;
        var _met_w = _pan_w - (_c_w + 40);
        var _met_h = _c_h;

        draw_set_color(make_color_rgb(8, 12, 16));
        draw_rectangle(_met_x + _sx, _met_y + _sy, _met_x + _met_w + _sx, _met_y + _met_h + _sy, false);
        draw_set_color(make_color_rgb(40, 65, 95));
        draw_rectangle(_met_x + _sx, _met_y + _sy, _met_x + _met_w + _sx, _met_y + _met_h + _sy, true);

        // TOP SUBVIEW SELECTOR: [1. FURNACE PREVIEW] | [2. DISCOVERED ALLOY CODEX] | [3. PERIODIC TABLE (118)]
        var _c_views = [
            "[1. FURNACE & BATCH PREVIEW]",
            "[2. DISCOVERED CODEX (" + string(array_length(scr_alloy_codex_get_all())) + ")]",
            "[3. PERIODIC TABLE (118)]"
        ];
        var _cv_w = (_met_w - 40) / 3;
        for (var cv = 0; cv < 3; cv++) {
            var _cvx = _met_x + 16 + cv * (_cv_w + 8);
            var _cv_active = (crucible_subview == cv);
            var _cv_hov = (_mx >= _cvx && _mx <= _cvx + _cv_w && _my >= _met_y + 8 && _my <= _met_y + 34);
            if (_cv_hov && _click) crucible_subview = cv;

            draw_set_color(_cv_active ? make_color_rgb(35, 75, 120) : (_cv_hov ? make_color_rgb(20, 40, 65) : make_color_rgb(12, 18, 26)));
            draw_rectangle(_cvx, _met_y + 8, _cvx + _cv_w, _met_y + 34, false);
            draw_set_color(_cv_active ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 75, 105));
            draw_rectangle(_cvx, _met_y + 8, _cvx + _cv_w, _met_y + 34, true);
            draw_set_color(_cv_active ? c_white : make_color_rgb(160, 190, 220));
            draw_text(_cvx + 10, _met_y + 13, _c_views[cv]);
        }

        // --- SUBVIEW 0: LIVE STOICHIOMETRIC REACTION PREVIEW & 8 MASTER ALLOYS ---
        if (crucible_subview == 0) {
            // 1. Detect Target Canonical Sintering Alloy from Current Batch
            var _tgt_name = "PROCEDURAL METALLURGICAL DISCOVERY";
            var _tgt_tier = "TIER ?";
            var _tgt_t_min = 1500; var _tgt_t_max = 5000;
            var _tgt_p_min = 0; var _tgt_p_max = 10000;
            var _tgt_bonus = "Combinatorial Material Exploration";
            var _tgt_purity = 95;
            var _is_known_tgt = false;

            if (crucible_batch.mat_tungsten == 2 && crucible_batch.mat_silica_carb == 1 && crucible_batch.mat_syn_flux == 0 && crucible_batch.mat_tritium == 0) {
                _tgt_name = "VANGUARD COMPOSITE ARMOR"; _tgt_tier = "TIER 1";
                _tgt_t_min = 2200; _tgt_t_max = 2500; _tgt_p_min = 0; _tgt_p_max = 1200;
                _tgt_bonus = "+30% Kinetic Defense Plating"; _tgt_purity = 99; _is_known_tgt = true;
            } else if (crucible_batch.mat_tritium >= 1 && crucible_batch.mat_syn_flux >= 1 && crucible_batch.mat_tungsten >= 1 && crucible_batch.mat_silica_carb == 0) {
                _tgt_name = "HYPERION SUPERCONDUCTOR MATRIX"; _tgt_tier = "TIER 2";
                _tgt_t_min = 4000; _tgt_t_max = 4600; _tgt_p_min = 4000; _tgt_p_max = 10000;
                _tgt_bonus = "Apex Tokamak Core Superconductor"; _tgt_purity = 98; _is_known_tgt = true;
            } else if (crucible_batch.mat_silica_carb >= 1 && crucible_batch.mat_syn_flux >= 2 && crucible_batch.mat_tungsten == 0 && crucible_batch.mat_tritium == 0) {
                _tgt_name = "AEROSTEEL VERNIER FLUX"; _tgt_tier = "TIER 2";
                _tgt_t_min = 1800; _tgt_t_max = 2250; _tgt_p_min = 0; _tgt_p_max = 1200;
                _tgt_bonus = "Lightweight High-G Thruster Shell"; _tgt_purity = 97; _is_known_tgt = true;
            } else if (crucible_batch.mat_tungsten >= 3 && crucible_batch.mat_silica_carb >= 1 && crucible_batch.mat_syn_flux >= 1 && crucible_batch.mat_tritium == 0) {
                _tgt_name = "ADAMANTINE HEAVY CARBIDE"; _tgt_tier = "TIER 3";
                _tgt_t_min = 3000; _tgt_t_max = 3550; _tgt_p_min = 3000; _tgt_p_max = 10000;
                _tgt_bonus = "Superheavy Ballistic Deflection"; _tgt_purity = 98; _is_known_tgt = true;
            } else if (crucible_batch.mat_tungsten >= 3 && crucible_batch.mat_syn_flux >= 2 && crucible_batch.mat_tritium >= 1 && crucible_batch.mat_silica_carb == 0) {
                _tgt_name = "REACTIVE DAMASCUS COMPOSITE"; _tgt_tier = "TIER 5";
                _tgt_t_min = 3400; _tgt_t_max = 3800; _tgt_p_min = 4500; _tgt_p_max = 7000;
                _tgt_bonus = "+35% Explosive Kinetic Deflection"; _tgt_purity = 99; _is_known_tgt = true;
            } else if (crucible_batch.mat_tungsten >= 1 && crucible_batch.mat_tritium >= 2 && crucible_batch.mat_syn_flux >= 2 && crucible_batch.mat_silica_carb == 0) {
                _tgt_name = "TACHYON SUPERALLOY MATRIX"; _tgt_tier = "APEX 5";
                _tgt_t_min = 4600; _tgt_t_max = 4950; _tgt_p_min = 8000; _tgt_p_max = 10000;
                _tgt_bonus = "+40% Energy Weapon Output Conduit"; _tgt_purity = 99; _is_known_tgt = true;
            } else if (crucible_batch.mat_silica_carb >= 3 && crucible_batch.mat_syn_flux >= 2 && crucible_batch.mat_tungsten == 0 && crucible_batch.mat_tritium == 0) {
                _tgt_name = "LUNAR AEROGEL MATRIX"; _tgt_tier = "TIER 4";
                _tgt_t_min = 1700; _tgt_t_max = 2100; _tgt_p_min = 0; _tgt_p_max = 800;
                _tgt_bonus = "-40% Chassis Mass / +50% Heat Venting"; _tgt_purity = 96; _is_known_tgt = true;
            } else if (crucible_batch.mat_tungsten >= 3 && crucible_batch.mat_silica_carb >= 1 && crucible_batch.mat_tritium >= 2 && crucible_batch.mat_syn_flux == 0) {
                _tgt_name = "SOL FERRITE HIGH-PERMEABILITY"; _tgt_tier = "TIER 5";
                _tgt_t_min = 4100; _tgt_t_max = 4400; _tgt_p_min = 5500; _tgt_p_max = 8500;
                _tgt_bonus = "+45% Railgun Velocity & Shield Pierce"; _tgt_purity = 98; _is_known_tgt = true;
            }

            var _temp_ok = (crucible_temp_c >= _tgt_t_min && crucible_temp_c <= _tgt_t_max);
            var _psi_ok = (crucible_pressure_psi >= _tgt_p_min && crucible_pressure_psi <= _tgt_p_max);

            // 2. Render Live Stoichiometric Reaction Plaque
            var _bw_y = _met_y + 44;
            scr_draw_snes_panel(_met_x + 16, _bw_y, _met_w - 32, 116, "LIVE STOICHIOMETRIC REACTION PLAQUE", make_color_rgb(100, 220, 255), true);

            // Ingot Swatch Preview
            scr_draw_alloy_swatch(_met_x + 28, _bw_y + 36, 110, 64, crucible_batch);

            var _cur_hex = scr_alloy_get_hex(crucible_batch);
            var _batch_tot = crucible_batch.mat_tungsten + crucible_batch.mat_silica_carb + crucible_batch.mat_tritium + crucible_batch.mat_syn_flux;

            // Target Alloy Header & Classification
            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_met_x + 150, _bw_y + 32, _tgt_name + " [" + _tgt_tier + "]");

            // Stoichiometric Status Checkmarks
            var _stat_t_str = _temp_ok ? "[TEMP: OPTIMAL " + string(floor(crucible_temp_c)) + "°C]" : ((crucible_temp_c < _tgt_t_min) ? "[TEMP LOW: NEED +" + string(floor(_tgt_t_min - crucible_temp_c)) + "°C]" : "[TEMP HIGH: -" + string(floor(crucible_temp_c - _tgt_t_max)) + "°C]");
            var _stat_p_str = _psi_ok ? "[PRESS: OPTIMAL]" : ((crucible_pressure_psi < _tgt_p_min) ? "[PRESS LOW: COMPRESS]" : "[PRESS HIGH: VENT]");

            draw_set_color(_temp_ok ? c_lime : make_color_rgb(255, 160, 60));
            draw_text(_met_x + 150, _bw_y + 52, _stat_t_str);

            draw_set_color(_psi_ok ? c_lime : make_color_rgb(255, 120, 60));
            draw_text(_met_x + 360, _bw_y + 52, _stat_p_str);

            draw_set_color(make_color_rgb(160, 205, 235));
            draw_text_ext(_met_x + 150, _bw_y + 72, "Ratio: W:" + string(crucible_batch.mat_tungsten) + " C:" + string(crucible_batch.mat_silica_carb) + " Tr:" + string(crucible_batch.mat_tritium) + " Fx:" + string(crucible_batch.mat_syn_flux) + " (Total: " + string(_batch_tot) + ") | Hex: " + _cur_hex, 16, _met_w - 165);

            draw_set_color(make_color_rgb(100, 240, 160));
            draw_text_ext(_met_x + 150, _bw_y + 92, "PROJECTED YIELD: 1x Ingot (" + string(_tgt_purity) + "% Purity) // " + _tgt_bonus, 16, _met_w - 165);

            // 3. Known Master Alloy Codex Grid (Expanded to all 8 Canonical Alloys)
            var _cdx_y = _bw_y + 128;
            draw_set_color(make_color_rgb(100, 210, 255));
            draw_text(_met_x + 16, _cdx_y, "MASTER METALLURGICAL ALLOY CODEX (CANONICAL RECIPES):");

            var _known_alloys = [
                { id: "alloy_vanguard_comp", name: "Vanguard Composite", formula: "2W + 1C | 2.4k°C | <1.2k PSI", role: "+30% Kinetic Armor" },
                { id: "alloy_hyperion_matrix", name: "Hyperion Matrix", formula: "1W + 2Tr + 1Fx | >4k PSI", role: "Tokamak Core" },
                { id: "alloy_aerosteel_flux", name: "Aerosteel Flux", formula: "1C + 2Fx | 2.0k°C | <1.2k PSI", role: "Lightweight High-G" },
                { id: "alloy_adamantine_carbide", name: "Adamantine Carbide", formula: "3W + 1C + 1Fx | >3k PSI", role: "Superheavy AP Armor" },
                { id: "alloy_reactive_damascus", name: "Reactive Damascus", formula: "3W + 2Fx + 1Tr | 3.6k°C", role: "+35% Kinetic Deflect" },
                { id: "alloy_tachyon_superalloy", name: "Tachyon Matrix", formula: "1W + 2Tr + 2Fx | 4.8k°C", role: "+40% Energy Weapon" },
                { id: "alloy_lunar_aerogel", name: "Lunar Aerogel", formula: "3C + 2Fx | 1.9k°C | <800 PSI", role: "-40% Mass / Venting" },
                { id: "alloy_sol_ferrite", name: "Sol Ferrite", formula: "3W + 1C + 2Tr | 4.2k°C", role: "+45% Railgun Pierce" }
            ];

            var _al_box_w = (_met_w - 48) / 2;
            var _al_box_h = 44;

            for (var ai = 0; ai < 8; ai++) {
                var _al = _known_alloys[ai];
                var _ax = _met_x + 16 + (ai mod 2) * (_al_box_w + 16);
                var _ay = _cdx_y + 20 + (ai div 2) * (_al_box_h + 6);

                draw_set_color(make_color_rgb(12, 18, 26));
                draw_rectangle(_ax, _ay, _ax + _al_box_w, _ay + _al_box_h, false);
                draw_set_color(make_color_rgb(35, 60, 90));
                draw_rectangle(_ax, _ay, _ax + _al_box_w, _ay + _al_box_h, true);

                scr_draw_alloy_swatch(_ax + 6, _ay + 6, 32, 32, _al.id);

                draw_set_color(make_color_rgb(240, 215, 100));
                draw_text(_ax + 42, _ay + 4, _al.name);
                draw_set_color(c_white);
                draw_text(_ax + 42, _ay + 18, _al.formula);
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_ax + 42, _ay + 30, _al.role);
            }

            // 3. Technical Notes & Art Shader Pipeline Architecture
            var _art_note_y = _cdx_y + 205;
            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_met_x + 16, _art_note_y, _met_x + _met_w - 16, _met_y + _met_h - 16, false);
            draw_set_color(make_color_rgb(30, 50, 75));
            draw_rectangle(_met_x + 16, _art_note_y, _met_x + _met_w - 16, _met_y + _met_h - 16, true);

            draw_set_color(make_color_rgb(220, 180, 80));
            draw_text(_met_x + 28, _art_note_y + 8, "CRUCIBLE THERMAL SMELTER // OPERATING PROTOCOLS:");
            draw_set_color(make_color_rgb(180, 205, 230));
            draw_text_ext(_met_x + 28, _art_note_y + 26, "• Stoichiometric Equilibrium: Induction coils must match required temperatures before batch injection.", 14, _met_w - 56);
            draw_text_ext(_met_x + 28, _art_note_y + 44, "• Pressure Containment: High-tier apex superalloys demand high-pressure inert argon atmospheres.", 14, _met_w - 56);
            draw_text_ext(_met_x + 28, _art_note_y + 62, "• Crystalline Compaction: Ballistic deflection and energy throughput scale with elemental purity.", 14, _met_w - 56);
        }
        // --- SUBVIEW 1: DISCOVERED ALLOY CODEX LOG ---
        else if (crucible_subview == 1) {
            var _codex_list = scr_alloy_codex_get_all();
            var _cdx_len = array_length(_codex_list);

            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_met_x + 16, _met_y + 44, "DISCOVERED ALLOY CODEX // CATALOGED PROCEDURAL FORMULAS (" + string(_cdx_len) + "):");

            var _cdx_card_h = 76;
            var _cdx_y_start = _met_y + 68;

            for (var ci = 0; ci < min(5, _cdx_len); ci++) {
                var _cidx = ci + codex_scroll_offset;
                if (_cidx >= _cdx_len) break;
                var _al_item = _codex_list[_cidx];
                var _cy = _cdx_y_start + ci * (_cdx_card_h + 8);

                draw_set_color(make_color_rgb(14, 20, 30));
                draw_rectangle(_met_x + 16, _cy, _met_x + _met_w - 16, _cy + _cdx_card_h, false);
                draw_set_color(make_color_rgb(35, 60, 90));
                draw_rectangle(_met_x + 16, _cy, _met_x + _met_w - 16, _cy + _cdx_card_h, true);

                scr_draw_alloy_swatch(_met_x + 26, _cy + 12, 54, 52, _al_item.hex);

                draw_set_color(make_color_rgb(240, 215, 100));
                draw_text(_met_x + 92, _cy + 8, _al_item.name + " [" + _al_item.code + "]");
                draw_set_color(c_white);
                draw_text(_met_x + 92, _cy + 26, "Armor HP: " + string(_al_item.armor_hp) + " | Dissipation: " + string(_al_item.thermal_rate) + " °C/s | Density: " + string(_al_item.density_g_cm3) + " g/cm³");
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_met_x + 92, _cy + 44, "Formula: " + _al_item.formula_summary + " (Color: " + _al_item.hex + ")");
            }

            if (_cdx_len > 5) {
                var _sc_y = _met_y + _met_h - 36;
                var _can_prev = (codex_scroll_offset > 0);
                var _can_next = (codex_scroll_offset + 5 < _cdx_len);
                if (_can_prev && _click && _mx >= _met_x + 16 && _mx <= _met_x + 140 && _my >= _sc_y && _my <= _sc_y + 24) codex_scroll_offset -= 1;
                if (_can_next && _click && _mx >= _met_x + 160 && _mx <= _met_x + 280 && _my >= _sc_y && _my <= _sc_y + 24) codex_scroll_offset += 1;

                draw_set_color(_can_prev ? make_color_rgb(30, 70, 110) : make_color_rgb(14, 20, 28));
                draw_rectangle(_met_x + 16, _sc_y, _met_x + 140, _sc_y + 24, false);
                draw_set_color(make_color_rgb(80, 180, 255));
                draw_rectangle(_met_x + 16, _sc_y, _met_x + 140, _sc_y + 24, true);
                draw_set_color(c_white);
                draw_text(_met_x + 30, _sc_y + 4, "[PREV PAGE]");

                draw_set_color(_can_next ? make_color_rgb(30, 70, 110) : make_color_rgb(14, 20, 28));
                draw_rectangle(_met_x + 160, _sc_y, _met_x + 280, _sc_y + 24, false);
                draw_set_color(make_color_rgb(80, 180, 255));
                draw_rectangle(_met_x + 160, _sc_y, _met_x + 280, _sc_y + 24, true);
                draw_set_color(c_white);
                draw_text(_met_x + 175, _sc_y + 4, "[NEXT PAGE]");
            }
        }
        // --- SUBVIEW 2: 118-ELEMENT PERIODIC TABLE DATABASE ---
        else if (crucible_subview == 2) {
            var _pt_list = [];
            if (instance_exists(obj_GameManager)) _pt_list = obj_GameManager.get_all_materials();
            var _pt_len = array_length(_pt_list);

            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_met_x + 16, _met_y + 44, "PERIODIC TABLE OF MINING MINERALS (" + string(_pt_len) + " ELEMENTS REGISTERED):");

            // Element list on left half of subview (compact width to leave 320px for detail dossier)
            var _pt_box_w = 260;
            var _pt_box_h = _met_h - 80;
            var _pt_x = _met_x + 16;
            var _pt_y = _met_y + 68;

            draw_set_color(make_color_rgb(12, 18, 26));
            draw_rectangle(_pt_x, _pt_y, _pt_x + _pt_box_w, _pt_y + _pt_box_h, false);
            draw_set_color(make_color_rgb(35, 55, 80));
            draw_rectangle(_pt_x, _pt_y, _pt_x + _pt_box_w, _pt_y + _pt_box_h, true);

            var _pt_vis = 8;
            for (var _pt_i = 0; _pt_i < min(_pt_vis, _pt_len); _pt_i++) {
                var _pidx = _pt_i + pt_scroll_offset;
                if (_pidx >= _pt_len) break;
                var _elem = _pt_list[_pidx];
                var _ey = _pt_y + 8 + _pt_i * 44;
                var _is_sel = (pt_selected_idx == _pidx);
                var _e_hov = (_mx >= _pt_x + 6 && _mx <= _pt_x + _pt_box_w - 6 && _my >= _ey && _my <= _ey + 40);
                if (_e_hov && _click) pt_selected_idx = _pidx;

                draw_set_color(_is_sel ? make_color_rgb(30, 65, 105) : (_e_hov ? make_color_rgb(20, 36, 55) : make_color_rgb(14, 20, 28)));
                draw_rectangle(_pt_x + 6, _ey, _pt_x + _pt_box_w - 6, _ey + 40, false);
                draw_set_color(_is_sel ? make_color_rgb(100, 220, 255) : make_color_rgb(35, 55, 80));
                draw_rectangle(_pt_x + 6, _ey, _pt_x + _pt_box_w - 6, _ey + 40, true);

                scr_draw_alloy_swatch(_pt_x + 12, _ey + 8, 26, 24, _elem.base_color_hex);

                draw_set_color(c_white);
                draw_text(_pt_x + 46, _ey + 6, "#" + string(_elem.atomic_number) + " " + _elem.symbol + " - " + _elem.name);
                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text(_pt_x + 46, _ey + 22, _elem.category);
            }

            // Element Detail Dossier on Right side of subview
            var _dtl_x = _pt_x + _pt_box_w + 16;
            var _dtl_w = _met_w - (_pt_box_w + 48);
            var _dtl_y = _pt_y;
            draw_set_color(make_color_rgb(12, 18, 26));
            draw_rectangle(_dtl_x, _dtl_y, _dtl_x + _dtl_w, _dtl_y + _pt_box_h, false);
            draw_set_color(make_color_rgb(35, 55, 80));
            draw_rectangle(_dtl_x, _dtl_y, _dtl_x + _dtl_w, _dtl_y + _pt_box_h, true);

            if (_pt_len > 0 && pt_selected_idx < _pt_len) {
                var _sel_elem = _pt_list[pt_selected_idx];
                draw_set_color(make_color_rgb(240, 215, 100));
                draw_text(_dtl_x + 16, _dtl_y + 12, "#" + string(_sel_elem.atomic_number) + " " + _sel_elem.name + " (" + _sel_elem.symbol + ")");
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_dtl_x + 16, _dtl_y + 32, "Category: " + _sel_elem.category + " | Tier: " + string(_sel_elem.tier));

                scr_draw_alloy_swatch(_dtl_x + 16, _dtl_y + 56, 80, 50, _sel_elem.base_color_hex);

                draw_set_color(c_white);
                draw_text(_dtl_x + 108, _dtl_y + 56, "* Density: " + string(_sel_elem.density_g_cm3) + " g/cm³");
                draw_text(_dtl_x + 108, _dtl_y + 74, "* Tensile Strength: " + string(_sel_elem.tensile_mpa) + " MPa");
                draw_text(_dtl_x + 108, _dtl_y + 92, "* Melting Point: " + string(_sel_elem.melting_point_c) + " °C");

                draw_set_color(make_color_rgb(240, 210, 100));
                draw_text(_dtl_x + 16, _dtl_y + 120, "SOLAR HARVESTING LOCATIONS:");
                draw_set_color(make_color_rgb(180, 210, 240));
                var _dist_arr = _sel_elem.solar_distribution;
                for (var d = 0; d < min(3, array_length(_dist_arr)); d++) {
                    draw_text(_dtl_x + 24, _dtl_y + 140 + d * 18, "> " + string(_dist_arr[d]));
                }

                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_dtl_x + 16, _dtl_y + 205, "INDUSTRIAL MOBILE SUIT ROLE:");
                draw_set_color(c_white);
                draw_text_ext(_dtl_x + 16, _dtl_y + 225, _sel_elem.industrial_role, 16, _dtl_w - 32);

                draw_set_color(make_color_rgb(200, 205, 215));
                draw_text_ext(_dtl_x + 16, _dtl_y + 270, _sel_elem.lore_description, 16, _dtl_w - 32);
            }
        }
    }
else if (rd_subtab == 1) {
        var _m_pan_x = _pan_x + 20;
        var _m_pan_y = _pan_y + 44;
        var _m_pan_w = _pan_w - 40;
        var _m_pan_h = _pan_h - 56;

        var _mg_btns = [
            "[1. REACTOR CONDUIT SINE WAVE TUNING]",
            "[2. LIMB HYDRAULIC STRESS ALIGNMENT]",
            "[3. THRUSTER PLASMA FLOW CALIBRATION]"
        ];
        var _mg_btn_w = 340;
        for (var mb = 0; mb < 3; mb++) {
            var _mbx = _m_pan_x + mb * (_mg_btn_w + 14);
            var _mb_active = (active_minigame == mb);
            var _mb_hov = (_mx >= _mbx && _mx <= _mbx + _mg_btn_w && _my >= _m_pan_y && _my <= _m_pan_y + 30);
            if (_mb_hov && _click) active_minigame = mb;

            draw_set_color(_mb_active ? make_color_rgb(40, 80, 130) : (_mb_hov ? make_color_rgb(25, 45, 70) : make_color_rgb(16, 26, 38)));
            draw_rectangle(_mbx + _sx, _m_pan_y + _sy, _mbx + _mg_btn_w + _sx, _m_pan_y + 30 + _sy, false);
            draw_set_color(_mb_active ? make_color_rgb(100, 220, 255) : make_color_rgb(50, 90, 135));
            draw_rectangle(_mbx + _sx, _m_pan_y + _sy, _mbx + _mg_btn_w + _sx, _m_pan_y + 30 + _sy, true);
            draw_set_color(_mb_active ? c_white : make_color_rgb(180, 210, 240));
            draw_text(_mbx + 12 + _sx, _m_pan_y + 7 + _sy, _mg_btns[mb]);
        }

        // Active R&D Prototype Tuning Status Ribbon (Doc 20)
        var _ribbon_y = _m_pan_y + 36;
        var _ribbon_w = _m_pan_w;
        draw_set_color(make_color_rgb(10, 16, 24));
        draw_rectangle(_m_pan_x, _ribbon_y, _m_pan_x + _ribbon_w, _ribbon_y + 26, false);
        draw_set_color(make_color_rgb(45, 75, 110));
        draw_rectangle(_m_pan_x, _ribbon_y, _m_pan_x + _ribbon_w, _ribbon_y + 26, true);

        var _rg = "UNTESTED";
        var _hg = "UNTESTED";
        var _tg = "UNTESTED";
        if (instance_exists(obj_BlueprintManager)) {
            var _pt = obj_BlueprintManager.active_prototype_tuning;
            _rg = _pt.reactor.grade + " (" + string(floor(_pt.reactor.score)) + "%)";
            _hg = _pt.hydraulics.grade + " (" + string(floor(_pt.hydraulics.score)) + "%)";
            _tg = _pt.thrusters.grade + " (" + string(floor(_pt.thrusters.score)) + "%)";
        }

        draw_set_color(make_color_rgb(255, 215, 80));
        draw_text(_m_pan_x + 10, _ribbon_y + 5, "ACTIVE PROTOTYPE TUNING:");
        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(_m_pan_x + 220, _ribbon_y + 5, "* REACTOR: " + _rg);
        draw_set_color(make_color_rgb(140, 255, 160));
        draw_text(_m_pan_x + 440, _ribbon_y + 5, "* HYDRAULICS: " + _hg);
        draw_set_color(make_color_rgb(255, 180, 100));
        draw_text(_m_pan_x + 680, _ribbon_y + 5, "* THRUSTERS: " + _tg);

        var _jbtn_x = _m_pan_x + _ribbon_w - 230;
        var _jbtn_hov = (_mx >= _jbtn_x && _mx <= _jbtn_x + 220 && _my >= _ribbon_y + 2 && _my <= _ribbon_y + 24);
        if (_jbtn_hov && _click) {
            active_tab = 1;
            factory_subtab = 2;
            show_toast("PROCEEDING TO ASSEMBLY BAY WITH ACTIVE TUNING SPECS!", c_lime);
        }
        draw_set_color(_jbtn_hov ? make_color_rgb(30, 80, 50) : make_color_rgb(16, 45, 28));
        draw_rectangle(_jbtn_x, _ribbon_y + 2, _jbtn_x + 220, _ribbon_y + 24, false);
        draw_set_color(make_color_rgb(60, 240, 120));
        draw_rectangle(_jbtn_x, _ribbon_y + 2, _jbtn_x + 220, _ribbon_y + 24, true);
        draw_set_color(c_white);
        draw_text(_jbtn_x + 8, _ribbon_y + 5, ">> APPLY IN ASSEMBLY BAY <<");

        // Minigame 0: Reactor Conduit Tuning (Turn-Based Oscilloscope Resonance)
        if (active_minigame == 0) {
            var _scope_x = _m_pan_x + 10;
            var _scope_y = _m_pan_y + 70;
            var _scope_w = 780;
            var _scope_h = 285;

            // Header Banner & Tutorial Button
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_scope_x, _scope_y - 8, "== TOKAMAK HARMONIC CONDUIT TUNER // TURN-BASED OSCILLATOR ==");
            
            var _rtut_x = _scope_x + _scope_w - 180;
            var _rtut_y = _scope_y - 12;
            var _rtut_hov = (_mx >= _rtut_x && _mx <= _rtut_x + 180 && _my >= _rtut_y && _my <= _rtut_y + 24);
            if (_rtut_hov && _click) active_tutorial_modal = "REACTOR";
            draw_set_color(_rtut_hov ? make_color_rgb(70, 50, 20) : make_color_rgb(35, 25, 10));
            draw_rectangle(_rtut_x, _rtut_y, _rtut_x + 180, _rtut_y + 24, false);
            draw_set_color(make_color_rgb(255, 180, 60));
            draw_rectangle(_rtut_x, _rtut_y, _rtut_x + 180, _rtut_y + 24, true);
            draw_set_color(c_white);
            draw_text(_rtut_x + 10, _rtut_y + 4, "[?] REACTOR TUTORIAL");

            // Oscilloscope Screen
            var _osc_y = _scope_y + 20;
            draw_set_color(make_color_rgb(6, 12, 18));
            draw_rectangle(_scope_x + _sx, _osc_y + _sy, _scope_x + _scope_w + _sx, _osc_y + _scope_h + _sy, false);
            draw_set_color(make_color_rgb(30, 60, 90));
            draw_rectangle(_scope_x + _sx, _osc_y + _sy, _scope_x + _scope_w + _sx, _osc_y + _scope_h + _sy, true);

            draw_set_color(make_color_rgb(14, 28, 42));
            for (var ox = _scope_x; ox <= _scope_x + _scope_w; ox += 40) draw_line(ox, _osc_y, ox, _osc_y + _scope_h);
            for (var oy = _osc_y; oy <= _osc_y + _scope_h; oy += 40) draw_line(_scope_x, oy, _scope_x + _scope_w, oy);

            var _center_y = _osc_y + _scope_h / 2;

            // Target Sine Wave (White)
            draw_set_color(c_white);
            for (var px = 0; px < _scope_w - 2; px += 2) {
                var _t1 = px * (360.0 / _scope_w);
                var _t2 = (px + 2) * (360.0 / _scope_w);
                var _y1 = _center_y + wave_target_amp * sin(degtorad(_t1 * wave_target_freq + wave_target_phase));
                var _y2 = _center_y + wave_target_amp * sin(degtorad(_t2 * wave_target_freq + wave_target_phase));
                draw_line(_scope_x + px, _y1, _scope_x + px + 2, _y2);
            }

            // Player Containment Wave (Cyan)
            draw_set_color(make_color_rgb(60, 230, 255));
            for (var px = 0; px < _scope_w - 2; px += 2) {
                var _t1 = px * (360.0 / _scope_w);
                var _t2 = (px + 2) * (360.0 / _scope_w);
                var _y1 = _center_y + slider_amp * sin(degtorad(_t1 * slider_freq + slider_phase));
                var _y2 = _center_y + slider_amp * sin(degtorad(_t2 * slider_freq + slider_phase));
                draw_line(_scope_x + px, _y1, _scope_x + px + 2, _y2);
            }

            draw_set_color(c_white);
            draw_text(_scope_x + 16, _osc_y + 12, "OSCILLOSCOPE: TARGET TOKAMAK FLUX (WHITE) vs ACTIVE CONTAINMENT FIELD (CYAN)");
            var _sync_col = (reactor_alignment_pct >= 90) ? c_lime : ((reactor_alignment_pct < 50) ? c_red : c_yellow);
            draw_set_color(_sync_col);
            draw_text(_scope_x + 16, _osc_y + 32, "HARMONIC ALIGNMENT: " + string_format(reactor_alignment_pct, 1, 1) + "% " + (reactor_alignment_pct >= 90 ? "[HARMONIC LOCK READY!]" : ""));

            // Sliders Below Scope
            var _sl_y = _osc_y + _scope_h + 16;

            // Slider 1: Frequency
            draw_set_color(c_white);
            draw_text(_scope_x, _sl_y, "FREQUENCY: " + string_format(slider_freq, 1, 2) + " Hz");
            var _s1_norm = (slider_freq - 0.5) / 3.5;
            draw_set_color(make_color_rgb(20, 32, 46));
            draw_rectangle(_scope_x, _sl_y + 22, _scope_x + 190, _sl_y + 34, false);
            draw_set_color(make_color_rgb(100, 200, 255));
            draw_circle(_scope_x + (190 * _s1_norm), _sl_y + 28, 8, false);
            if (_down && _mx >= _scope_x - 10 && _mx <= _scope_x + 200 && _my >= _sl_y + 15 && _my <= _sl_y + 40) {
                slider_freq = 0.5 + clamp((_mx - _scope_x) / 190.0, 0, 1) * 3.5;
            }
            var _f_sub_hov = (_mx >= _scope_x + 200 && _mx <= _scope_x + 225 && _my >= _sl_y + 18 && _my <= _sl_y + 38);
            if (_f_sub_hov && _click) slider_freq = max(0.5, slider_freq - 0.05);
            draw_set_color(_f_sub_hov ? make_color_rgb(40, 70, 100) : make_color_rgb(20, 35, 50));
            draw_rectangle(_scope_x + 200, _sl_y + 18, _scope_x + 225, _sl_y + 38, false);
            draw_set_color(c_white); draw_text(_scope_x + 206, _sl_y + 20, "-");
            var _f_add_hov = (_mx >= _scope_x + 230 && _mx <= _scope_x + 255 && _my >= _sl_y + 18 && _my <= _sl_y + 38);
            if (_f_add_hov && _click) slider_freq = min(4.0, slider_freq + 0.05);
            draw_set_color(_f_add_hov ? make_color_rgb(40, 70, 100) : make_color_rgb(20, 35, 50));
            draw_rectangle(_scope_x + 230, _sl_y + 18, _scope_x + 255, _sl_y + 38, false);
            draw_set_color(c_white); draw_text(_scope_x + 236, _sl_y + 20, "+");

            // Slider 2: Amplitude
            var _sl2_x = _scope_x + 270;
            draw_set_color(c_white);
            draw_text(_sl2_x, _sl_y, "AMPLITUDE: " + string_format(slider_amp, 1, 1) + " px");
            var _s2_norm = (slider_amp - 15.0) / 60.0;
            draw_set_color(make_color_rgb(20, 32, 46));
            draw_rectangle(_sl2_x, _sl_y + 22, _sl2_x + 190, _sl_y + 34, false);
            draw_set_color(make_color_rgb(100, 200, 255));
            draw_circle(_sl2_x + (190 * _s2_norm), _sl_y + 28, 8, false);
            if (_down && _mx >= _sl2_x - 10 && _mx <= _sl2_x + 200 && _my >= _sl_y + 15 && _my <= _sl_y + 40) {
                slider_amp = 15.0 + clamp((_mx - _sl2_x) / 190.0, 0, 1) * 60.0;
            }
            var _a_sub_hov = (_mx >= _sl2_x + 200 && _mx <= _sl2_x + 225 && _my >= _sl_y + 18 && _my <= _sl_y + 38);
            if (_a_sub_hov && _click) slider_amp = max(15.0, slider_amp - 2.0);
            draw_set_color(_a_sub_hov ? make_color_rgb(40, 70, 100) : make_color_rgb(20, 35, 50));
            draw_rectangle(_sl2_x + 200, _sl_y + 18, _sl2_x + 225, _sl_y + 38, false);
            draw_set_color(c_white); draw_text(_sl2_x + 206, _sl_y + 20, "-");
            var _a_add_hov = (_mx >= _sl2_x + 230 && _mx <= _sl2_x + 255 && _my >= _sl_y + 18 && _my <= _sl_y + 38);
            if (_a_add_hov && _click) slider_amp = min(75.0, slider_amp + 2.0);
            draw_set_color(_a_add_hov ? make_color_rgb(40, 70, 100) : make_color_rgb(20, 35, 50));
            draw_rectangle(_sl2_x + 230, _sl_y + 18, _sl2_x + 255, _sl_y + 38, false);
            draw_set_color(c_white); draw_text(_sl2_x + 236, _sl_y + 20, "+");

            // Slider 3: Phase Angle
            var _sl3_x = _sl2_x + 270;
            draw_set_color(c_white);
            draw_text(_sl3_x, _sl_y, "PHASE ANGLE: " + string(floor(slider_phase)) + " deg");
            var _s3_norm = slider_phase / 360.0;
            draw_set_color(make_color_rgb(20, 32, 46));
            draw_rectangle(_sl3_x, _sl_y + 22, _sl3_x + 190, _sl_y + 34, false);
            draw_set_color(make_color_rgb(100, 200, 255));
            draw_circle(_sl3_x + (190 * _s3_norm), _sl_y + 28, 8, false);
            if (_down && _mx >= _sl3_x - 10 && _mx <= _sl3_x + 200 && _my >= _sl_y + 15 && _my <= _sl_y + 40) {
                slider_phase = clamp((_mx - _sl3_x) / 190.0, 0, 1) * 360.0;
            }
            var _p_sub_hov = (_mx >= _sl3_x + 200 && _mx <= _sl3_x + 225 && _my >= _sl_y + 18 && _my <= _sl_y + 38);
            if (_p_sub_hov && _click) slider_phase = (slider_phase - 10.0 + 360.0) mod 360.0;
            draw_set_color(_p_sub_hov ? make_color_rgb(40, 70, 100) : make_color_rgb(20, 35, 50));
            draw_rectangle(_sl3_x + 200, _sl_y + 18, _sl3_x + 225, _sl_y + 38, false);
            draw_set_color(c_white); draw_text(_sl3_x + 206, _sl_y + 20, "-");
            var _p_add_hov = (_mx >= _sl3_x + 230 && _mx <= _sl3_x + 255 && _my >= _sl_y + 18 && _my <= _sl_y + 38);
            if (_p_add_hov && _click) slider_phase = (slider_phase + 10.0) mod 360.0;
            draw_set_color(_p_add_hov ? make_color_rgb(40, 70, 100) : make_color_rgb(20, 35, 50));
            draw_rectangle(_sl3_x + 230, _sl_y + 18, _sl3_x + 255, _sl_y + 38, false);
            draw_set_color(c_white); draw_text(_sl3_x + 236, _sl_y + 20, "+");

            // Right Panel: Component Card, Pulse Button, Masterwork Status
            var _stat_x = _scope_x + _scope_w + 30;
            var _stat_y = _scope_y + 10;
            var _stat_w = _m_pan_w - _scope_w - 50;

            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_stat_x, _stat_y, _stat_x + _stat_w, _stat_y + 400, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_stat_x, _stat_y, _stat_x + _stat_w, _stat_y + 400, true);

            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_stat_x + 16, _stat_y + 12, "== HYPERION TOKAMAK CORE ==");

            if (sprite_exists(spr_comp_reactor)) {
                draw_sprite_ext(spr_comp_reactor, 0, _stat_x + 16, _stat_y + 40, 0.62, 0.62, 0, c_white, 0.95);
            }

            var _diag_y = _stat_y + 195;
            draw_set_color(c_white);
            draw_text(_stat_x + 16, _diag_y, "RATED OUTPUT: 1,850 MW");

            var _r_grd = reactor_last_grade;
            var _grd_col = make_color_rgb(100, 220, 255);
            if (_r_grd == "S") _grd_col = c_lime;
            else if (_r_grd == "A") _grd_col = make_color_rgb(140, 255, 160);
            else if (_r_grd == "B") _grd_col = make_color_rgb(255, 215, 80);
            else if (_r_grd == "C") _grd_col = make_color_rgb(255, 160, 60);
            else if (_r_grd == "D") _grd_col = c_red;

            draw_set_color(_grd_col);
            draw_text(_stat_x + 16, _diag_y + 20, "CURRENT GRADE: [" + _r_grd + "-RANK] (" + string_format(reactor_last_score, 1, 1) + "%)");

            // Live alignment gauge
            draw_set_color(make_color_rgb(20, 30, 44));
            draw_rectangle(_stat_x + 16, _diag_y + 44, _stat_x + _stat_w - 16, _diag_y + 64, false);
            draw_set_color(_sync_col);
            draw_rectangle(_stat_x + 16, _diag_y + 44, _stat_x + 16 + ((_stat_w - 32) * (reactor_alignment_pct / 100.0)), _diag_y + 64, false);
            draw_set_color(c_white);
            draw_text(_stat_x + 22, _diag_y + 46, string_format(reactor_alignment_pct, 1, 1) + "% RESONANCE");

            // Test Pulse Button or Masterwork Cleared Banner
            var _btn_pulse_y = _diag_y + 76;
            if (reactor_complete) {
                draw_set_color(make_color_rgb(30, 70, 40));
                draw_rectangle(_stat_x + 16, _btn_pulse_y, _stat_x + _stat_w - 16, _btn_pulse_y + 44, false);
                draw_set_color(c_lime);
                draw_rectangle(_stat_x + 16, _btn_pulse_y, _stat_x + _stat_w - 16, _btn_pulse_y + 44, true);
                draw_set_color(c_white);
                draw_text(_stat_x + 24, _btn_pulse_y + 12, "[MASTERWORK CORE FORGED & SAVED!]");
            } else {
                var _pulse_hov = (_mx >= _stat_x + 16 && _mx <= _stat_x + _stat_w - 16 && _my >= _btn_pulse_y && _my <= _btn_pulse_y + 44);
                if (_pulse_hov && _click) {
                    test_reactor_pulse();
                }
                draw_set_color(_pulse_hov ? make_color_rgb(30, 90, 130) : make_color_rgb(18, 45, 75));
                draw_rectangle(_stat_x + 16, _btn_pulse_y, _stat_x + _stat_w - 16, _btn_pulse_y + 44, false);
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_rectangle(_stat_x + 16, _btn_pulse_y, _stat_x + _stat_w - 16, _btn_pulse_y + 44, true);
                draw_set_color(c_white);
                draw_text(_stat_x + 24, _btn_pulse_y + 12, ">> TEST HARMONIC PULSE <<");
            }

            var _rst_y = _btn_pulse_y + 54;
            var _rst_hov = (_mx >= _stat_x + 16 && _mx <= _stat_x + _stat_w - 16 && _my >= _rst_y && _my <= _rst_y + 30);
            if (_rst_hov && _click) {
                reactor_complete = false;
                slider_freq = 1.0;
                slider_amp = 30.0;
                slider_phase = 0.0;
                show_toast("HARMONIC TEST BENCH RECALIBRATED", c_yellow);
            }
            draw_set_color(_rst_hov ? make_color_rgb(50, 40, 20) : make_color_rgb(25, 20, 10));
            draw_rectangle(_stat_x + 16, _rst_y, _stat_x + _stat_w - 16, _rst_y + 30, false);
            draw_set_color(make_color_rgb(200, 160, 60));
            draw_rectangle(_stat_x + 16, _rst_y, _stat_x + _stat_w - 16, _rst_y + 30, true);
            draw_set_color(c_white);
            draw_text(_stat_x + 24, _rst_y + 6, "[RESET TEST BENCH]");
        }

        // Minigame 1: Limb Hydraulic Stress Alignment (Action-Based Budget)
        else if (active_minigame == 1) {
            var _l_x = _m_pan_x + 10;
            var _l_y = _m_pan_y + 70;

            // Header Banner
            draw_set_color(make_color_rgb(100, 200, 255));
            draw_text(_l_x, _l_y - 8, "== HYDRAULIC STRUCTURAL STRESS TEST // ACTION-BUDGET CALIBRATION ==");

            // Tutorial Button
            var _htut_x = _l_x + 800;
            var _htut_y = _l_y - 12;
            var _htut_hov = (_mx >= _htut_x && _mx <= _htut_x + 180 && _my >= _htut_y && _my <= _htut_y + 24);
            if (_htut_hov && _click) active_tutorial_modal = "HYDRAULIC";
            draw_set_color(_htut_hov ? make_color_rgb(70, 50, 20) : make_color_rgb(35, 25, 10));
            draw_rectangle(_htut_x, _htut_y, _htut_x + 180, _htut_y + 24, false);
            draw_set_color(make_color_rgb(255, 180, 60));
            draw_rectangle(_htut_x, _htut_y, _htut_x + 180, _htut_y + 24, true);
            draw_set_color(c_white);
            draw_text(_htut_x + 10, _htut_y + 4, "[?] HYDRAULIC TUTORIAL");

            // Left Panel: Mechanical Leg Node Diagram
            var _schem_x = _l_x;
            var _schem_y = _l_y + 20;
            var _schem_w = 460;
            var _schem_h = 400;

            draw_set_color(make_color_rgb(8, 14, 20));
            draw_rectangle(_schem_x, _schem_y, _schem_x + _schem_w, _schem_y + _schem_h, false);
            draw_set_color(make_color_rgb(30, 60, 90));
            draw_rectangle(_schem_x, _schem_y, _schem_x + _schem_w, _schem_y + _schem_h, true);

            draw_set_color(make_color_rgb(40, 70, 110));
            draw_line_width(_schem_x + 140, _schem_y + 90, _schem_x + 140, _schem_y + 190, 3);
            draw_line_width(_schem_x + 140, _schem_y + 190, _schem_x + 140, _schem_y + 280, 3);
            draw_line_width(_schem_x + 140, _schem_y + 280, _schem_x + 140, _schem_y + 350, 3);

            // Draw 4 joint nodes
            for (var n = 0; n < array_length(limb_joints); n++) {
                var _j = limb_joints[n];
                var _jx = _schem_x + 140;
                var _jy = _schem_y + 90 + n * 88;
                var _is_sel = (selected_limb_joint == n);
                var _hov = (point_distance(_mx, _my, _jx, _jy) <= 24);
                if (_hov && _click) selected_limb_joint = n;

                var _in_safe = (_j.stress >= 25.0 && _j.stress <= 45.0);
                var _j_col = _j.locked ? c_lime : (_in_safe ? c_aqua : ((_j.stress > 45) ? c_red : c_orange));

                // Selection box
                if (_is_sel) {
                    draw_set_color(make_color_rgb(255, 220, 80));
                    draw_rectangle(_schem_x + 20, _jy - 30, _schem_x + _schem_w - 20, _jy + 30, true);
                }

                // Node circle
                draw_set_color(_j_col);
                draw_circle(_jx, _jy, 14, false);
                draw_set_color(c_white);
                draw_circle(_jx, _jy, 15, true);

                // Label and status text
                draw_set_color(_is_sel ? c_yellow : c_white);
                draw_text(_jx + 30, _jy - 14, _j.name + " (" + string(n + 1) + ")");
                draw_set_color(_j_col);
                draw_text(_jx + 30, _jy + 4, "Stress: " + string(floor(_j.stress)) + "% " + (_j.locked ? "[WELD LOCKED]" : (_in_safe ? "[TOLERANCE SAFE]" : "[OUT OF BAND]")));
            }

            // Right Panel: Joint Inspector Deck & Action Buttons
            var _info_x = _schem_x + _schem_w + 24;
            var _info_y = _schem_y;
            var _info_w = _m_pan_w - _schem_w - 44;

            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_info_x, _info_y, _info_x + _info_w, _info_y + _schem_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_info_x, _info_y, _info_x + _info_w, _info_y + _schem_h, true);

            // Action Budget Indicator
            draw_set_color(c_white);
            draw_text(_info_x + 20, _info_y + 14, "PULSE ACTION BUDGET:");
            for (var b = 0; b < 8; b++) {
                var _pip_x = _info_x + 230 + b * 26;
                var _pip_y = _info_y + 14;
                var _pip_active = (b < limb_actions_budget);
                draw_set_color(_pip_active ? c_lime : make_color_rgb(40, 50, 60));
                draw_rectangle(_pip_x, _pip_y, _pip_x + 20, _pip_y + 16, false);
                draw_set_color(c_white);
                draw_rectangle(_pip_x, _pip_y, _pip_x + 20, _pip_y + 16, true);
            }

            // Selected Joint Details
            var _cur_j = limb_joints[selected_limb_joint];
            var _j_band_ok = (_cur_j.stress >= 25.0 && _cur_j.stress <= 45.0);
            var _lg_grd = limb_last_grade;
            var _lg_lim = 115;
            if (instance_exists(obj_BlueprintManager)) _lg_lim = obj_BlueprintManager.active_prototype_tuning.hydraulics.pilot_limit_pct;
            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_info_x + 20, _info_y + 26, "BENCH GRADE: [" + _lg_grd + "-RANK] | LIMIT (GENKAI): " + string(_lg_lim) + "%");

            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_info_x + 20, _info_y + 46, "TARGET JOINT: " + _cur_j.name);
            draw_set_color(c_white);
            draw_text(_info_x + 20, _info_y + 68, "OPTIMAL SAFE BAND: 25.0% - 45.0% (Current: " + string(floor(_cur_j.stress)) + "%)");

            // Stress Bar with Green Zone
            var _bar_x = _info_x + 20;
            var _bar_y = _info_y + 92;
            var _bar_w = _info_w - 40;
            var _bar_h = 24;
            draw_set_color(make_color_rgb(20, 30, 44));
            draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_w, _bar_y + _bar_h, false);
            // Safe zone (25% to 45%)
            draw_set_color(make_color_rgb(20, 80, 40));
            draw_rectangle(_bar_x + (_bar_w * 0.25), _bar_y, _bar_x + (_bar_w * 0.45), _bar_y + _bar_h, false);
            // Stress Fill
            var _fill_col = _cur_j.locked ? c_lime : (_j_band_ok ? c_aqua : ((_cur_j.stress > 45) ? c_red : c_orange));
            draw_set_color(_fill_col);
            draw_rectangle(_bar_x, _bar_y, _bar_x + (_bar_w * (_cur_j.stress / 100.0)), _bar_y + _bar_h, false);
            draw_set_color(c_white);
            draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_w, _bar_y + _bar_h, true);

            // Discrete Action Buttons
            var _act1_y = _bar_y + 36;
            var _act_w = (_bar_w - 16) / 2;
            var _a1_hov = (_mx >= _bar_x && _mx <= _bar_x + _act_w && _my >= _act1_y && _my <= _act1_y + 40);
            if (_a1_hov && _click) limb_relieve_joint(selected_limb_joint);
            draw_set_color(_a1_hov ? make_color_rgb(30, 70, 100) : make_color_rgb(16, 40, 60));
            draw_rectangle(_bar_x, _act1_y, _bar_x + _act_w, _act1_y + 40, false);
            draw_set_color(make_color_rgb(100, 200, 255));
            draw_rectangle(_bar_x, _act1_y, _bar_x + _act_w, _act1_y + 40, true);
            draw_set_color(c_white);
            draw_text(_bar_x + 16, _act1_y + 10, "[-16%] RELIEVE PRESSURE");

            var _a2_x = _bar_x + _act_w + 16;
            var _a2_hov = (_mx >= _a2_x && _mx <= _a2_x + _act_w && _my >= _act1_y && _my <= _act1_y + 40);
            if (_a2_hov && _click) limb_tighten_joint(selected_limb_joint);
            draw_set_color(_a2_hov ? make_color_rgb(80, 70, 30) : make_color_rgb(45, 40, 16));
            draw_rectangle(_a2_x, _act1_y, _a2_x + _act_w, _act1_y + 40, false);
            draw_set_color(make_color_rgb(255, 210, 80));
            draw_rectangle(_a2_x, _act1_y, _a2_x + _act_w, _act1_y + 40, true);
            draw_set_color(c_white);
            draw_text(_a2_x + 16, _act1_y + 10, "[+14%] TIGHTEN CYLINDER");

            // Weld Lock Button (Action 3)
            var _weld_y = _act1_y + 48;
            var _w_hov = (_mx >= _bar_x && _mx <= _bar_x + _bar_w && _my >= _weld_y && _my <= _weld_y + 44);
            if (_w_hov && _click) limb_weld_joint(selected_limb_joint);
            draw_set_color(_w_hov ? make_color_rgb(40, 90, 50) : make_color_rgb(20, 50, 30));
            draw_rectangle(_bar_x, _weld_y, _bar_x + _bar_w, _weld_y + 44, false);
            draw_set_color(make_color_rgb(100, 255, 120));
            draw_rectangle(_bar_x, _weld_y, _bar_x + _bar_w, _weld_y + 44, true);
            draw_set_color(c_white);
            draw_text(_bar_x + 24, _weld_y + 12, ">> SPOT-WELD JOINT LOCK (REQUIRES 25%-45% STRESS) <<");

            // Masterwork Cleared or Reset
            var _bot_y = _weld_y + 56;
            if (limb_complete) {
                draw_set_color(make_color_rgb(30, 70, 40));
                draw_rectangle(_bar_x, _bot_y, _bar_x + _bar_w, _bot_y + 40, false);
                draw_set_color(c_lime);
                draw_rectangle(_bar_x, _bot_y, _bar_x + _bar_w, _bot_y + 40, true);
                draw_set_color(c_white);
                draw_text(_bar_x + 20, _bot_y + 10, "[ALL 4 JOINTS BALANCED! MASTERWORK HYDRAULICS FORGED!]");
            } else {
                var _rst_hov = (_mx >= _bar_x && _mx <= _bar_x + _bar_w && _my >= _bot_y && _my <= _bot_y + 36);
                if (_rst_hov && _click) reset_limb_sim();
                draw_set_color(_rst_hov ? make_color_rgb(60, 45, 20) : make_color_rgb(30, 22, 10));
                draw_rectangle(_bar_x, _bot_y, _bar_x + _bar_w, _bot_y + 36, false);
                draw_set_color(make_color_rgb(220, 180, 80));
                draw_rectangle(_bar_x, _bot_y, _bar_x + _bar_w, _bot_y + 36, true);
                draw_set_color(c_white);
                draw_text(_bar_x + 20, _bot_y + 8, "[RESET HYDRAULIC BENCH (8 ACTIONS)]");
            }

            // Component Specs Footer
            if (sprite_exists(spr_comp_legs)) {
                draw_sprite_ext(spr_comp_legs, 0, _info_x + 24, _bot_y + 48, 0.50, 0.50, 0, c_white, 0.90);
            }
        }

        // Minigame 2: Thruster Plasma Flow Calibration (Multi-Stage Resonance)
        else if (active_minigame == 2) {
            var _t_x = _m_pan_x + 10;
            var _t_y = _m_pan_y + 70;

            // Header Banner & Tutorial Button
            draw_set_color(make_color_rgb(100, 200, 255));
            draw_text(_t_x, _t_y - 8, "== THRUSTER PLASMA INJECTION CALIBRATION // MULTI-STAGE RESONANCE ==");

            var _ttut_x = _t_x + 800;
            var _ttut_y = _t_y - 12;
            var _ttut_hov = (_mx >= _ttut_x && _mx <= _ttut_x + 180 && _my >= _ttut_y && _my <= _ttut_y + 24);
            if (_ttut_hov && _click) active_tutorial_modal = "THRUSTER";
            draw_set_color(_ttut_hov ? make_color_rgb(70, 50, 20) : make_color_rgb(35, 25, 10));
            draw_rectangle(_ttut_x, _ttut_y, _ttut_x + 180, _ttut_y + 24, false);
            draw_set_color(make_color_rgb(255, 180, 60));
            draw_rectangle(_ttut_x, _ttut_y, _ttut_x + 180, _ttut_y + 24, true);
            draw_set_color(c_white);
            draw_text(_ttut_x + 10, _ttut_y + 4, "[?] THRUSTER TUTORIAL");

            // 4-Stage Progress Header Bar
            var _sbar_y = _t_y + 20;
            var _sbar_w = (_m_pan_w - 40) / 4;
            for (var st = 0; st < 4; st++) {
                var _sbx = _t_x + st * (_sbar_w + 6);
                var _is_curr = (thruster_stage == st);
                var _is_done = (thruster_stage > st);

                draw_set_color(_is_done ? make_color_rgb(20, 60, 30) : (_is_curr ? make_color_rgb(30, 70, 110) : make_color_rgb(14, 20, 28)));
                draw_rectangle(_sbx, _sbar_y, _sbx + _sbar_w, _sbar_y + 36, false);
                draw_set_color(_is_done ? c_lime : (_is_curr ? make_color_rgb(100, 220, 255) : make_color_rgb(40, 60, 85)));
                draw_rectangle(_sbx, _sbar_y, _sbx + _sbar_w, _sbar_y + 36, true);

                draw_set_color(c_white);
                draw_text(_sbx + 10, _sbar_y + 4, "STAGE " + string(st + 1));
                draw_set_color(_is_done ? c_lime : (_is_curr ? c_yellow : make_color_rgb(140, 160, 180)));
                draw_text(_sbx + 10, _sbar_y + 18, _is_done ? "[v CLEARED]" : (_is_curr ? "[>> ACTIVE <<]" : "[PENDING]"));
            }

            // Left Panel: Plasma Chamber & Resonance Scope
            var _c_x = _t_x;
            var _c_y = _sbar_y + 48;
            var _c_w = 460;
            var _c_h = 350;

            draw_set_color(make_color_rgb(8, 14, 20));
            draw_rectangle(_c_x, _c_y, _c_x + _c_w, _c_y + _c_h, false);
            draw_set_color(make_color_rgb(30, 60, 90));
            draw_rectangle(_c_x, _c_y, _c_x + _c_w, _c_y + _c_h, true);

            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_c_x + 16, _c_y + 12, "== DUAL-VECTOR PLASMA CONFINEMENT CHAMBER ==");

            if (sprite_exists(spr_comp_thruster)) {
                draw_sprite_ext(spr_comp_thruster, 0, _c_x + 16, _c_y + 40, 0.65, 0.65, 0, c_white, 0.92);
            }

            // Current resonance calculation
            var _cur_res = 0.0;
            if (thruster_stage < 4) {
                var _st_dat = thruster_stages_info[thruster_stage];
                _cur_res = clamp(100.0 - abs(thruster_fuel - _st_dat.target_fuel) * 1.5 - abs(thruster_mag - _st_dat.target_mag) * 1.5, 0.0, 100.0);
            } else {
                _cur_res = 100.0;
            }

            // Live Resonance Spectrum Bar
            var _rbar_y = _c_y + 270;
            draw_set_color(c_white);
            draw_text(_c_x + 16, _rbar_y - 20, "STAGE HARMONIC RESONANCE (TARGET: >= 80%):");

            draw_set_color(make_color_rgb(20, 30, 44));
            draw_rectangle(_c_x + 16, _rbar_y, _c_x + _c_w - 16, _rbar_y + 24, false);
            // 80% Threshold line
            var _thr_x = _c_x + 16 + (_c_w - 32) * 0.80;
            draw_set_color(make_color_rgb(255, 200, 80));
            draw_line_width(_thr_x, _rbar_y - 4, _thr_x, _rbar_y + 28, 2);

            var _res_col = (_cur_res >= 80.0) ? c_lime : ((_cur_res < 50.0) ? c_red : c_yellow);
            draw_set_color(_res_col);
            draw_rectangle(_c_x + 16, _rbar_y, _c_x + 16 + ((_c_w - 32) * (_cur_res / 100.0)), _rbar_y + 24, false);
            draw_set_color(c_white);
            draw_rectangle(_c_x + 16, _rbar_y, _c_x + _c_w - 16, _rbar_y + 24, true);
            draw_text(_c_x + 22, _rbar_y + 4, string(floor(_cur_res)) + "% RESONANCE " + (_cur_res >= 80.0 ? "[READY TO ADVANCE]" : ""));

            // Right Panel: Fuel & Magnetic Controls Deck
            var _info_x = _c_x + _c_w + 24;
            var _info_y = _c_y;
            var _info_w = _m_pan_w - _c_w - 44;

            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_info_x, _info_y, _info_x + _info_w, _info_y + _c_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_info_x, _info_y, _info_x + _info_w, _info_y + _c_h, true);

            if (thruster_stage < 4) {
                var _st_info = thruster_stages_info[thruster_stage];
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_info_x + 20, _info_y + 14, _st_info.title);
                draw_set_color(make_color_rgb(170, 195, 220));
                draw_text_ext(_info_x + 20, _info_y + 36, _st_info.desc, 20, _info_w - 40);

                // Slider 1: Fuel Injection
                var _f_sl_y = _info_y + 90;
                draw_set_color(c_white);
                draw_text(_info_x + 20, _f_sl_y, "FUEL INJECTION FLOW: " + string(floor(thruster_fuel)) + " %");
                var _f_sl_w = _info_w - 140;
                draw_set_color(make_color_rgb(20, 32, 46));
                draw_rectangle(_info_x + 20, _f_sl_y + 22, _info_x + 20 + _f_sl_w, _f_sl_y + 34, false);
                draw_set_color(make_color_rgb(255, 140, 60));
                draw_circle(_info_x + 20 + (_f_sl_w * (thruster_fuel / 100.0)), _f_sl_y + 28, 8, false);
                if (_down && _mx >= _info_x + 10 && _mx <= _info_x + 20 + _f_sl_w + 10 && _my >= _f_sl_y + 15 && _my <= _f_sl_y + 40) {
                    thruster_fuel = clamp((_mx - (_info_x + 20)) / _f_sl_w, 0, 1) * 100.0;
                }
                // Stepper buttons
                var _f1_hov = (_mx >= _info_x + 20 + _f_sl_w + 15 && _mx <= _info_x + 20 + _f_sl_w + 40 && _my >= _f_sl_y + 18 && _my <= _f_sl_y + 38);
                if (_f1_hov && _click) thruster_fuel = max(0.0, thruster_fuel - 5.0);
                draw_set_color(_f1_hov ? make_color_rgb(80, 50, 20) : make_color_rgb(40, 25, 10));
                draw_rectangle(_info_x + 20 + _f_sl_w + 15, _f_sl_y + 18, _info_x + 20 + _f_sl_w + 40, _f_sl_y + 38, false);
                draw_set_color(c_white); draw_text(_info_x + 20 + _f_sl_w + 22, _f_sl_y + 20, "-");
                var _f2_hov = (_mx >= _info_x + 20 + _f_sl_w + 45 && _mx <= _info_x + 20 + _f_sl_w + 70 && _my >= _f_sl_y + 18 && _my <= _f_sl_y + 38);
                if (_f2_hov && _click) thruster_fuel = min(100.0, thruster_fuel + 5.0);
                draw_set_color(_f2_hov ? make_color_rgb(80, 50, 20) : make_color_rgb(40, 25, 10));
                draw_rectangle(_info_x + 20 + _f_sl_w + 45, _f_sl_y + 18, _info_x + 20 + _f_sl_w + 70, _f_sl_y + 38, false);
                draw_set_color(c_white); draw_text(_info_x + 20 + _f_sl_w + 52, _f_sl_y + 20, "+");

                // Slider 2: Magnetic Confinement Flux
                var _m_sl_y = _f_sl_y + 60;
                draw_set_color(c_white);
                draw_text(_info_x + 20, _m_sl_y, "MAGNETIC COIL CONFINEMENT: " + string(floor(thruster_mag)) + " Gauss %");
                draw_set_color(make_color_rgb(20, 32, 46));
                draw_rectangle(_info_x + 20, _m_sl_y + 22, _info_x + 20 + _f_sl_w, _m_sl_y + 34, false);
                draw_set_color(make_color_rgb(100, 200, 255));
                draw_circle(_info_x + 20 + (_f_sl_w * (thruster_mag / 100.0)), _m_sl_y + 28, 8, false);
                if (_down && _mx >= _info_x + 10 && _mx <= _info_x + 20 + _f_sl_w + 10 && _my >= _m_sl_y + 15 && _my <= _m_sl_y + 40) {
                    thruster_mag = clamp((_mx - (_info_x + 20)) / _f_sl_w, 0, 1) * 100.0;
                }
                // Stepper buttons
                var _m1_hov = (_mx >= _info_x + 20 + _f_sl_w + 15 && _mx <= _info_x + 20 + _f_sl_w + 40 && _my >= _m_sl_y + 18 && _my <= _m_sl_y + 38);
                if (_m1_hov && _click) thruster_mag = max(0.0, thruster_mag - 5.0);
                draw_set_color(_m1_hov ? make_color_rgb(40, 70, 100) : make_color_rgb(20, 35, 50));
                draw_rectangle(_info_x + 20 + _f_sl_w + 15, _m_sl_y + 18, _info_x + 20 + _f_sl_w + 40, _m_sl_y + 38, false);
                draw_set_color(c_white); draw_text(_info_x + 20 + _f_sl_w + 22, _m_sl_y + 20, "-");
                var _m2_hov = (_mx >= _info_x + 20 + _f_sl_w + 45 && _mx <= _info_x + 20 + _f_sl_w + 70 && _my >= _m_sl_y + 18 && _my <= _m_sl_y + 38);
                if (_m2_hov && _click) thruster_mag = min(100.0, thruster_mag + 5.0);
                draw_set_color(_m2_hov ? make_color_rgb(40, 70, 100) : make_color_rgb(20, 35, 50));
                draw_rectangle(_info_x + 20 + _f_sl_w + 45, _m_sl_y + 18, _info_x + 20 + _f_sl_w + 70, _m_sl_y + 38, false);
                draw_set_color(c_white); draw_text(_info_x + 20 + _f_sl_w + 52, _m_sl_y + 20, "+");

                // Commit Stage Pulse Button
                var _pulse_y = _m_sl_y + 60;
                var _p_hov = (_mx >= _info_x + 20 && _mx <= _info_x + _info_w - 20 && _my >= _pulse_y && _my <= _pulse_y + 44);
                if (_p_hov && _click) {
                    commit_thruster_pulse();
                }
                draw_set_color(_p_hov ? make_color_rgb(30, 90, 60) : make_color_rgb(18, 50, 35));
                draw_rectangle(_info_x + 20, _pulse_y, _info_x + _info_w - 20, _pulse_y + 44, false);
                draw_set_color(make_color_rgb(80, 220, 140));
                draw_rectangle(_info_x + 20, _pulse_y, _info_x + _info_w - 20, _pulse_y + 44, true);
                draw_set_color(c_white);
                draw_text(_info_x + 30, _pulse_y + 12, ">> COMMIT STAGE CALIBRATION PULSE <<");
            } else {
                draw_set_color(make_color_rgb(30, 70, 40));
                draw_rectangle(_info_x + 20, _info_y + 30, _info_x + _info_w - 20, _info_y + 160, false);
                draw_set_color(c_lime);
                draw_rectangle(_info_x + 20, _info_y + 30, _info_x + _info_w - 20, _info_y + 160, true);
                draw_set_color(c_white);
                draw_text(_info_x + 36, _info_y + 50, "ALL 4 BURN STAGES HARMONIZED!");
                draw_text(_info_x + 36, _info_y + 80, "Masterwork Dual-Vector Vernier Backpack forged!");
                draw_text(_info_x + 36, _info_y + 110, "Bonus: +25% Evasion Rating and Instant Boost Thrusters!");
            }

            // Reset Button
            var _trst_y = _info_y + _c_h - 44;
            var _trst_hov = (_mx >= _info_x + 20 && _mx <= _info_x + _info_w - 20 && _my >= _trst_y && _my <= _trst_y + 32);
            if (_trst_hov && _click) reset_thruster_sim();
            draw_set_color(_trst_hov ? make_color_rgb(60, 45, 20) : make_color_rgb(30, 22, 10));
            draw_rectangle(_info_x + 20, _trst_y, _info_x + _info_w - 20, _trst_y + 32, false);
            draw_set_color(make_color_rgb(220, 180, 80));
            draw_rectangle(_info_x + 20, _trst_y, _info_x + _info_w - 20, _trst_y + 32, true);
            draw_set_color(c_white);
            draw_text(_info_x + 30, _trst_y + 8, "[RESET THRUSTER TEST BENCH]");
        }
    }
    // ---------------------------------------------------------------------
    // SUB-TAB 2: GHA-07 IRONCLAD SPECS & SORTIES (With Technical Schematic Art!)
    // ---------------------------------------------------------------------
    // ---------------------------------------------------------------------
    // SUB-TAB 2: MOBILE SUIT BLUEPRINT ARCHIVE & INVENTORY SCHEMATICS (DOCS 01, 12, 13, 14)
    // ---------------------------------------------------------------------
    else if (rd_subtab == 2) {
        var _s_x = _pan_x + 20;
        var _s_y = _pan_y + 40;
        var _s_w = _pan_w - 40;
        var _s_h = _pan_h - 56;

        // 1. TOP SOURCE SELECTOR BAR: Fleet Inventory vs Canonical Blueprints
        var _src_names = [
            "[1. PMC FLEET INVENTORY]",
            "[2. MASTER BLUEPRINT ARCHIVE (100+)]"
        ];
        var _src_w = 260;
        for (var sc = 0; sc < 2; sc++) {
            var _scx = _s_x + sc * (_src_w + 10);
            var _sc_active = (bp_archive_source == sc);
            var _sc_hov = (_mx >= _scx && _mx <= _scx + _src_w && _my >= _s_y && _my <= _s_y + 28);
            if (_sc_hov && _click) {
                bp_archive_source = sc;
                bp_archive_selected_idx = 0;
            }

            draw_set_color(_sc_active ? make_color_rgb(35, 75, 120) : (_sc_hov ? make_color_rgb(22, 42, 65) : make_color_rgb(14, 22, 34)));
            draw_rectangle(_scx, _s_y, _scx + _src_w, _s_y + 28, false);
            draw_set_color(_sc_active ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 75, 110));
            draw_rectangle(_scx, _s_y, _scx + _src_w, _s_y + 28, true);
            draw_set_color(_sc_active ? c_white : make_color_rgb(160, 190, 220));
            draw_text(_scx + 10, _s_y + 6, _src_names[sc]);
        }

        // Faction Filter Bar (only active when bp_archive_source == 1)
        if (bp_archive_source == 1) {
            var _f_filters = [
                { id: "all", label: "ALL (100+)" },
                { id: "faction_terran", label: "TERRAN" },
                { id: "faction_colony", label: "COLONY" },
                { id: "faction_syndicate", label: "SYNDICATE" },
                { id: "faction_zaibatsu", label: "ZAIBATSU" },
                { id: "player", label: "PMC LINE" }
            ];
            var _ff_x = _s_x + 2 * (_src_w + 10) + 12;
            var _ff_w = 95;
            for (var ff = 0; ff < array_length(_f_filters); ff++) {
                var _filt = _f_filters[ff];
                var _fx = _ff_x + ff * (_ff_w + 6);
                var _f_active = (bp_archive_faction_filter == _filt.id);
                var _f_hov = (_mx >= _fx && _mx <= _fx + _ff_w && _my >= _s_y && _my <= _s_y + 28);
                if (_f_hov && _click) {
                    bp_archive_faction_filter = _filt.id;
                    bp_archive_selected_idx = 0;
                }

                draw_set_color(_f_active ? make_color_rgb(60, 45, 20) : (_f_hov ? make_color_rgb(35, 28, 14) : make_color_rgb(16, 20, 26)));
                draw_rectangle(_fx, _s_y, _fx + _ff_w, _s_y + 28, false);
                draw_set_color(_f_active ? make_color_rgb(255, 180, 60) : make_color_rgb(45, 65, 90));
                draw_rectangle(_fx, _s_y, _fx + _ff_w, _s_y + 28, true);
                draw_set_color(_f_active ? c_white : make_color_rgb(160, 180, 200));
                draw_text(_fx + 8, _s_y + 6, _filt.label);
            }
        }

        // =====================================================================
        // DATA POPULATION & UNIT RESOLUTION
        // =====================================================================
        var _active_suit = undefined;
        var _unit_list = [];

        if (bp_archive_source == 0) {
            if (instance_exists(obj_GameManager)) {
                _unit_list = obj_GameManager.inventory.deployable_mechs;
            }
        } else {
            if (instance_exists(obj_BlueprintManager)) {
                _unit_list = obj_BlueprintManager.get_blueprints_by_faction(bp_archive_faction_filter);
            }
        }

        var _list_len = array_length(_unit_list);
        if (_list_len > 0) {
            bp_archive_selected_idx = clamp(bp_archive_selected_idx, 0, _list_len - 1);
            _active_suit = _unit_list[bp_archive_selected_idx];
        }

        // =====================================================================
        // COLUMN 1: LEFT SELECTOR LIST (width: 260px)
        // =====================================================================
        var _col1_x = _s_x;
        var _col1_y = _s_y + 38;
        var _col1_w = 260;
        var _col1_h = _s_h - 44;

        draw_set_color(make_color_rgb(10, 15, 22));
        draw_rectangle(_col1_x, _col1_y, _col1_x + _col1_w, _col1_y + _col1_h, false);
        draw_set_color(make_color_rgb(35, 55, 80));
        draw_rectangle(_col1_x, _col1_y, _col1_x + _col1_w, _col1_y + _col1_h, true);

        // Header
        draw_set_color(make_color_rgb(100, 220, 255));
        var _header_lbl = (bp_archive_source == 0) ? "PMC INVENTORY FLEET (" + string(_list_len) + ")" : "BLUEPRINT REGISTRY (" + string(_list_len) + ")";
        draw_text(_col1_x + 12, _col1_y + 10, _header_lbl);

        // Items per page
        var _max_visible = 9;
        var _item_h = 56;
        var _item_y_start = _col1_y + 36;

        for (var ui = 0; ui < min(_max_visible, _list_len); ui++) {
            var _u_idx = ui + bp_archive_scroll;
            if (_u_idx >= _list_len) break;
            var _item = _unit_list[_u_idx];

            var _iy = _item_y_start + ui * (_item_h + 6);
            var _i_sel = (bp_archive_selected_idx == _u_idx);
            var _i_hov = (_mx >= _col1_x + 8 && _mx <= _col1_x + _col1_w - 8 && _my >= _iy && _my <= _iy + _item_h);

            if (_i_hov && _click) bp_archive_selected_idx = _u_idx;

            draw_set_color(_i_sel ? make_color_rgb(28, 60, 95) : (_i_hov ? make_color_rgb(18, 36, 55) : make_color_rgb(14, 20, 28)));
            draw_rectangle(_col1_x + 8, _iy, _col1_x + _col1_w - 8, _iy + _item_h, false);
            draw_set_color(_i_sel ? make_color_rgb(100, 220, 255) : make_color_rgb(35, 55, 80));
            draw_rectangle(_col1_x + 8, _iy, _col1_x + _col1_w - 8, _iy + _item_h, true);

            var _code = variable_struct_get(_item, "model_code") ?? (variable_struct_get(_item, "callsign") ?? _item.name);
            var _iname = variable_struct_get(_item, "name") ?? "Mobile Suit";
            var _sub = (bp_archive_source == 0) ? ("Status: " + string(variable_struct_get(_item, "status") ?? "READY")) : ("Role: " + string(variable_struct_get(_item, "role") ?? "Assault"));

            draw_set_color(_i_sel ? c_white : make_color_rgb(220, 220, 220));
            draw_text(_col1_x + 16, _iy + 8, string_copy(_code + " // " + _iname, 1, 24));
            draw_set_color(make_color_rgb(100, 200, 255));
            draw_text(_col1_x + 16, _iy + 28, _sub);

            var _astat = variable_struct_get(_item, "adoption_status") ?? "standard_issue";
            var _stat_tag = "[STD]";
            var _stat_col = make_color_rgb(100, 220, 255);
            if (_astat == "adopted") { _stat_tag = "[ADOPTED]"; _stat_col = make_color_rgb(255, 215, 80); }
            else if (_astat == "replaced_by_player") { _stat_tag = "[PMC-REP]"; _stat_col = make_color_rgb(80, 255, 120); }
            else if (_astat == "replaced_by_competitor") { _stat_tag = "[CORP-REP]"; _stat_col = make_color_rgb(255, 140, 60); }
            else if (_astat == "contested") { _stat_tag = "[PMC]"; _stat_col = make_color_rgb(255, 240, 100); }
            else if (_astat == "phased_out") { _stat_tag = "[PHASED]"; _stat_col = make_color_rgb(140, 140, 140); }
            else if (_astat == "ace_custom") { _stat_tag = "[ACE]"; _stat_col = make_color_rgb(220, 150, 255); }

            draw_set_color(_stat_col);
            draw_text(_col1_x + _col1_w - 96, _iy + 28, _stat_tag);
        }

        // Scroll navigation buttons if items > visible
        if (_list_len > _max_visible) {
            var _sc_btn_y = _col1_y + _col1_h - 32;
            var _can_up = (bp_archive_scroll > 0);
            var _can_dn = (bp_archive_scroll + _max_visible < _list_len);

            var _up_hov = (_mx >= _col1_x + 10 && _mx <= _col1_x + 140 && _my >= _sc_btn_y && _my <= _sc_btn_y + 24);
            var _dn_hov = (_mx >= _col1_x + 170 && _mx <= _col1_x + 300 && _my >= _sc_btn_y && _my <= _sc_btn_y + 24);

            if (_up_hov && _click && _can_up) bp_archive_scroll -= 1;
            if (_dn_hov && _click && _can_dn) bp_archive_scroll += 1;

            draw_set_color(_can_up ? (_up_hov ? make_color_rgb(40, 80, 120) : make_color_rgb(20, 40, 60)) : make_color_rgb(14, 18, 24));
            draw_rectangle(_col1_x + 10, _sc_btn_y, _col1_x + 140, _sc_btn_y + 24, false);
            draw_set_color(_can_up ? make_color_rgb(80, 180, 255) : make_color_rgb(30, 45, 60));
            draw_rectangle(_col1_x + 10, _sc_btn_y, _col1_x + 140, _sc_btn_y + 24, true);
            draw_set_color(_can_up ? c_white : make_color_rgb(100, 120, 140));
            draw_text(_col1_x + 30, _sc_btn_y + 4, "[PREV PAGE]");

            draw_set_color(_can_dn ? (_dn_hov ? make_color_rgb(40, 80, 120) : make_color_rgb(20, 40, 60)) : make_color_rgb(14, 18, 24));
            draw_rectangle(_col1_x + 170, _sc_btn_y, _col1_x + 300, _sc_btn_y + 24, false);
            draw_set_color(_can_dn ? make_color_rgb(80, 180, 255) : make_color_rgb(30, 45, 60));
            draw_rectangle(_col1_x + 170, _sc_btn_y, _col1_x + 300, _sc_btn_y + 24, true);
            draw_set_color(_can_dn ? c_white : make_color_rgb(100, 120, 140));
            draw_text(_col1_x + 190, _sc_btn_y + 4, "[NEXT PAGE]");
        }

        // =====================================================================
        // COLUMN 2: CENTER VISUAL & SCHEMATICS PRESENTATION (width: 460px)
        // =====================================================================
        var _col2_x = _col1_x + _col1_w + 14;
        var _col2_y = _col1_y;
        var _col2_w = 460;
        var _col2_h = _col1_h;

        draw_set_color(make_color_rgb(10, 15, 22));
        draw_rectangle(_col2_x, _col2_y, _col2_x + _col2_w, _col2_y + _col2_h, false);
        draw_set_color(make_color_rgb(35, 55, 80));
        draw_rectangle(_col2_x, _col2_y, _col2_x + _col2_w, _col2_y + _col2_h, true);

        // Center Sub-Mode Tabs
        var _c_submodes = [
            "[1. SPRITE]",
            "[2. SCHEMATIC]",
            "[3. ALLOY]",
            "[4. MODULES]"
        ];
        var _csm_w = (_col2_w - 32) / 4;
        for (var sm = 0; sm < 4; sm++) {
            var _smx = _col2_x + 16 + sm * _csm_w;
            var _sm_active = (bp_archive_view_mode == sm);
            var _sm_hov = (_mx >= _smx && _mx <= _smx + _csm_w - 6 && _my >= _col2_y + 10 && _my <= _col2_y + 36);
            if (_sm_hov && _click) bp_archive_view_mode = sm;

            draw_set_color(_sm_active ? make_color_rgb(30, 65, 105) : (_sm_hov ? make_color_rgb(18, 38, 60) : make_color_rgb(12, 18, 26)));
            draw_rectangle(_smx, _col2_y + 10, _smx + _csm_w - 6, _col2_y + 36, false);
            draw_set_color(_sm_active ? make_color_rgb(100, 220, 255) : make_color_rgb(40, 70, 100));
            draw_rectangle(_smx, _col2_y + 10, _smx + _csm_w - 6, _col2_y + 36, true);
            draw_set_color(_sm_active ? c_white : make_color_rgb(160, 190, 220));
            draw_text(_smx + 8, _col2_y + 16, _c_submodes[sm]);
        }

        if (!is_undefined(_active_suit)) {
            var _active_alloy_cost = variable_struct_get(_active_suit, "alloy_cost") ?? { tungsten: 40, silica: 20, flux: 10 };
            var _alloy_tint = scr_get_alloy_procedural_color(_active_alloy_cost);
            var _alloy_hex = scr_alloy_get_hex(_active_alloy_cost);

            // Sub-Mode 0: Tactical Sprite & Finish
            if (bp_archive_view_mode == 0) {
                var _spr = variable_struct_get(_active_suit, "associated_sprite") ?? spr_ms_ironclad_idle;
                if (!sprite_exists(_spr)) _spr = spr_ms_ironclad_idle;

                // Tactical Grid Pedestal
                var _ped_x = _col2_x + 24;
                var _ped_y = _col2_y + 48;
                var _ped_w = _col2_w - 48;
                var _ped_h = 360;

                draw_set_color(make_color_rgb(6, 10, 14));
                draw_rectangle(_ped_x, _ped_y, _ped_x + _ped_w, _ped_y + _ped_h, false);
                draw_set_color(make_color_rgb(25, 45, 65));
                draw_rectangle(_ped_x, _ped_y, _ped_x + _ped_w, _ped_y + _ped_h, true);

                // Grid lines
                draw_set_color(make_color_rgb(16, 28, 42));
                for (var gx = _ped_x; gx < _ped_x + _ped_w; gx += 40) draw_line(gx, _ped_y, gx, _ped_y + _ped_h);
                for (var gy = _ped_y; gy < _ped_y + _ped_h; gy += 40) draw_line(_ped_x, gy, _ped_x + _ped_w, gy);

                // Draw Sprite
                if (sprite_exists(_spr)) {
                    var _spr_w = sprite_get_width(_spr);
                    var _spr_h = sprite_get_height(_spr);
                    var _scale = clamp(260.0 / max(_spr_w, _spr_h), 0.6, 2.2);
                    var _draw_x = _ped_x + (_ped_w / 2) - (_spr_w * _scale / 2);
                    var _draw_y = _ped_y + (_ped_h / 2) - (_spr_h * _scale / 2);

                    draw_sprite_ext(_spr, 0, _draw_x, _draw_y, _scale, _scale, 0, c_white, 1.0);
                }

                // Swatch Banner underneath Pedestal
                var _sw_box_y = _ped_y + _ped_h + 16;
                draw_set_color(make_color_rgb(14, 20, 28));
                draw_rectangle(_ped_x, _sw_box_y, _ped_x + _ped_w, _sw_box_y + 70, false);
                draw_set_color(make_color_rgb(35, 60, 90));
                draw_rectangle(_ped_x, _sw_box_y, _ped_x + _ped_w, _sw_box_y + 70, true);

                scr_draw_alloy_swatch(_ped_x + 14, _sw_box_y + 12, 60, 46, _active_alloy_cost);

                draw_set_color(make_color_rgb(240, 210, 100));
                draw_text(_ped_x + 86, _sw_box_y + 12, "ARMOR ALLOY FINISH: " + string(variable_struct_get(_active_suit, "metal_type") ?? "Composite Laminate"));
                draw_set_color(c_white);
                draw_text(_ped_x + 86, _sw_box_y + 30, "Procedural Chromatic Signature: " + _alloy_hex);
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_ped_x + 86, _sw_box_y + 48, "Spectral Weights: W:" + string(variable_struct_get(_active_alloy_cost, "tungsten") ?? 0) + " | C:" + string(variable_struct_get(_active_alloy_cost, "silica") ?? 0) + " | Tr:" + string(variable_struct_get(_active_alloy_cost, "tritium") ?? 0) + " | Flux:" + string(variable_struct_get(_active_alloy_cost, "flux") ?? 0));
            }
            // Sub-Mode 1: Technical Schematics
            else if (bp_archive_view_mode == 1) {
                var _sch_x = _col2_x + 24;
                var _sch_y = _col2_y + 48;
                if (sprite_exists(spr_mech_schematic)) {
                    draw_sprite_ext(spr_mech_schematic, 0, _sch_x, _sch_y, 0.62, 0.62, 0, c_white, 0.95);
                }
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_sch_x + 12, _sch_y + 390, "TECHNICAL SCHEMATIC: Height: " + string(variable_struct_get(_active_suit, "height_meters") ?? 18.0) + "m | Combat Mass: " + string(variable_struct_get(_active_suit, "combat_weight_tonnes") ?? 85.0) + "t");
            }
            // Sub-Mode 2: Deep Alloy Swatch & Metallurgy Matrix
            else if (bp_archive_view_mode == 2) {
                var _mat_x = _col2_x + 24;
                var _mat_y = _col2_y + 48;
                draw_set_color(make_color_rgb(14, 20, 28));
                draw_rectangle(_mat_x, _mat_y, _mat_x + _col2_w - 48, _mat_y + 380, false);
                draw_set_color(make_color_rgb(40, 70, 105));
                draw_rectangle(_mat_x, _mat_y, _mat_x + _col2_w - 48, _mat_y + 380, true);

                draw_set_color(make_color_rgb(240, 215, 100));
                draw_text(_mat_x + 20, _mat_y + 16, "DEEP METALLURGICAL ALLOY ANALYSIS:");

                scr_draw_alloy_swatch(_mat_x + 20, _mat_y + 44, 180, 80, _active_alloy_cost);

                draw_set_color(c_white);
                draw_text(_mat_x + 220, _mat_y + 44, "Alloy Hex Code: " + _alloy_hex);
                draw_set_color(make_color_rgb(180, 210, 240));
                draw_text(_mat_x + 220, _mat_y + 66, "Tensile Modulus: High Impact Kinetic Deflection");
                draw_text(_mat_x + 220, _mat_y + 88, "Thermal Dissipation: " + string(variable_struct_get(_active_suit, "heat_dispersion_rate") ?? 30.0) + " °C / sec");
                draw_text(_mat_x + 220, _mat_y + 110, "Base Structure Integrity: " + string(variable_struct_get(_active_suit, "structure_hp") ?? 2000) + " HP");

                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_mat_x + 20, _mat_y + 145, "REQUISITE ELEMENTAL INGOT RATIOS (CRUCIBLE HOPPER):");
                var _cost_keys = variable_struct_get_names(_active_alloy_cost);
                for (var ck = 0; ck < array_length(_cost_keys); ck++) {
                    var _ckname = _cost_keys[ck];
                    var _cqty = variable_struct_get(_active_alloy_cost, _ckname);
                    draw_set_color(make_color_rgb(200, 220, 240));
                    draw_text(_mat_x + 20, _mat_y + 175 + ck * 24, "* " + string_upper(_ckname) + ": " + string(_cqty) + " Units");
                }
            }
            // Sub-Mode 3: Modular Components Inspector
            else if (bp_archive_view_mode == 3) {
                var _cmp_x = _col2_x + 24;
                var _cmp_y = _col2_y + 48;
                var _cnames = ["REACTOR", "LEGS", "WEAPON", "HEAD", "TORSO", "THRUSTER"];
                var _cbw = 110;
                for (var ci = 0; ci < 6; ci++) {
                    var _cbx = _cmp_x + ci * (_cbw + 8);
                    var _c_active = (selected_comp_idx == ci);
                    var _c_hov = (_mx >= _cbx && _mx <= _cbx + _cbw && _my >= _cmp_y && _my <= _cmp_y + 26);
                    if (_c_hov && _click) selected_comp_idx = ci;

                    draw_set_color(_c_active ? make_color_rgb(50, 100, 160) : (_c_hov ? make_color_rgb(30, 55, 85) : make_color_rgb(14, 22, 32)));
                    draw_rectangle(_cbx, _cmp_y, _cbx + _cbw, _cmp_y + 26, false);
                    draw_set_color(_c_active ? make_color_rgb(120, 240, 255) : make_color_rgb(40, 70, 100));
                    draw_rectangle(_cbx, _cmp_y, _cbx + _cbw, _cmp_y + 26, true);
                    draw_set_color(c_white);
                    draw_text(_cbx + 8, _cmp_y + 6, _cnames[ci]);
                }

                var _sel = comp_specs_data[selected_comp_idx];
                if (sprite_exists(_sel.sprite)) {
                    draw_sprite_ext(_sel.sprite, 0, _cmp_x, _cmp_y + 40, 0.82, 0.82, 0, c_white, 0.95);
                }
                var _cdx = _cmp_x + 280;
                var _cdy = _cmp_y + 40;
                draw_set_color(make_color_rgb(240, 210, 100));
                draw_text(_cdx, _cdy, "SLOT: " + _sel.slot + " // " + _sel.name);
                draw_set_color(make_color_rgb(180, 220, 255));
                draw_text(_cdx, _cdy + 24, "* Power: " + _sel.power_output);
                draw_text(_cdx, _cdy + 44, "* Mass / Load: " + _sel.dry_mass);
                draw_text(_cdx, _cdy + 64, "* Thermal: " + _sel.heat_dissipation);
                draw_text(_cdx, _cdy + 84, "* Alloy Cost: " + _sel.alloys);
                draw_set_color(make_color_rgb(200, 200, 210));
                draw_text_ext(_cdx, _cdy + 115, _sel.desc, 18, 420);
            }
        }

        // =====================================================================
        // COLUMN 3: RIGHT PANEL - SPECS, LORE, VARIANTS & ACTIONS (width: 530px)
        // =====================================================================
        var _col3_x = _col2_x + _col2_w + 14;
        var _col3_y = _col1_y;
        var _col3_w = _s_x + _s_w - _col3_x;
        var _col3_h = _col1_h;

        draw_set_color(make_color_rgb(10, 15, 22));
        draw_rectangle(_col3_x, _col3_y, _col3_x + _col3_w, _col3_y + _col3_h, false);
        draw_set_color(make_color_rgb(35, 55, 80));
        draw_rectangle(_col3_x, _col3_y, _col3_x + _col3_w, _col3_y + _col3_h, true);

        if (!is_undefined(_active_suit)) {
            var _rx = _col3_x + 16;
            var _ry = _col3_y + 12;

            // Unit Name & Classification
            draw_set_color(make_color_rgb(240, 215, 100));
            draw_text(_rx, _ry, string(variable_struct_get(_active_suit, "model_code") ?? "MS") + " " + string(variable_struct_get(_active_suit, "name") ?? "Mobile Suit"));
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_rx, _ry + 20, "Role: " + string(variable_struct_get(_active_suit, "role") ?? "Assault") + " | Era: " + string(variable_struct_get(_active_suit, "era") ?? "Production"));

            // Column 3 Dossier Subtabs (Specs vs Global Stats vs Lore/Chronicle)
            var _dsub_names = ["[1. SPECS & WEAPONS]", "[2. GLOBAL STATS & ATTRITION]", "[3. HISTORICAL & DYNAMIC LORE]"];
            var _dsub_w = (_col3_w - 32) / 3;
            var _dsub_y = _ry + 42;
            for (var ds = 0; ds < 3; ds++) {
                var _dsx = _rx + ds * _dsub_w;
                var _ds_active = (bp_archive_dossier_tab == ds);
                var _ds_hov = (_mx >= _dsx && _mx <= _dsx + _dsub_w - 4 && _my >= _dsub_y && _my <= _dsub_y + 24);
                if (_ds_hov && _click) { bp_archive_dossier_tab = ds; scr_audio_play_ui("click"); }

                draw_set_color(_ds_active ? make_color_rgb(30, 65, 105) : (_ds_hov ? make_color_rgb(18, 38, 60) : make_color_rgb(12, 18, 26)));
                draw_rectangle(_dsx, _dsub_y, _dsx + _dsub_w - 4, _dsub_y + 24, false);
                draw_set_color(_ds_active ? make_color_rgb(100, 220, 255) : make_color_rgb(40, 70, 100));
                draw_rectangle(_dsx, _dsub_y, _dsx + _dsub_w - 4, _dsub_y + 24, true);
                draw_set_color(_ds_active ? c_white : make_color_rgb(150, 180, 210));
                draw_text(_dsx + 6, _dsub_y + 4, _dsub_names[ds]);
            }

            var _content_y = _dsub_y + 32;

            // =================================================================
            // TAB 0: CORE TECHNICAL SPECS & WEAPON LOADOUT
            // =================================================================
            if (bp_archive_dossier_tab == 0) {
                draw_set_color(c_white);
                draw_text(_rx, _content_y, "* Armor Rating: " + string(variable_struct_get(_active_suit, "armor_rating") ?? 850) + " HP");
                draw_text(_rx, _content_y + 20, "* Structure HP: " + string(variable_struct_get(_active_suit, "structure_hp") ?? 2000) + " HP");
                draw_text(_rx, _content_y + 40, "* Reactor Output: " + string(variable_struct_get(_active_suit, "power_output_mw") ?? 1200) + " MW (" + string(variable_struct_get(_active_suit, "reactor_type") ?? "Fusion Core") + ")");
                draw_text(_rx, _content_y + 60, "* Mobility: Walk " + string(variable_struct_get(_active_suit, "walk_speed_kph") ?? 40) + " km/h | Boost " + string(variable_struct_get(_active_suit, "boost_speed_kph") ?? 80) + " km/h");
                draw_text(_rx, _content_y + 80, "* Dimensions: Height " + string(variable_struct_get(_active_suit, "height_meters") ?? 18.0) + "m | Weight " + string(variable_struct_get(_active_suit, "combat_weight_tonnes") ?? 85.0) + "t");

                var _c_stats = undefined;
                if (instance_exists(obj_BlueprintManager)) {
                    _c_stats = obj_BlueprintManager.get_comprehensive_stats(_active_suit);
                }
                if (!is_undefined(_c_stats)) {
                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_rx, _content_y + 104, "* Pilot Limit (Genkai): " + string(_c_stats.pilot_limit_pct) + "% | Propellant: " + string(_c_stats.propellant_max) + " EN");
                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_rx, _content_y + 124, "* Terrains: G:" + _c_stats.terrain.ground + " S:" + _c_stats.terrain.space + " U:" + _c_stats.terrain.urban + " T:" + _c_stats.terrain.trench + " | ECM: " + string(_c_stats.ecm_dispersion_pct) + "%");
                }

                var _arms_y = _content_y + 150;
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_rx, _arms_y, "ARMAMENT LOADOUT:");
                var _arms = variable_struct_get(_active_suit, "armament") ?? ["Autocannon", "Vulcan"];
                if (is_array(_arms)) {
                    for (var w = 0; w < min(3, array_length(_arms)); w++) {
                        draw_set_color(c_white);
                        draw_text(_rx + 10, _arms_y + 20 + w * 18, "> " + string(_arms[w]));
                    }
                }

                var _var_y = _arms_y + 84;
                draw_set_color(make_color_rgb(240, 210, 100));
                draw_text(_rx, _var_y, "PRODUCTION VARIANTS & DOCTRINES:");
                var _vars = variable_struct_get(_active_suit, "variants") ?? ["Standard Production", "Ace Refit"];
                if (is_array(_vars)) {
                    for (var v = 0; v < min(4, array_length(_vars)); v++) {
                        draw_set_color(make_color_rgb(180, 210, 240));
                        draw_text(_rx + 10, _var_y + 20 + v * 18, "[+] " + string(_vars[v]));
                    }
                }
            }
            // =================================================================
            // TAB 1: GLOBAL PRODUCTION NUMBERS & ATTRITION TELEMETRY
            // =================================================================
            else if (bp_archive_dossier_tab == 1) {
                draw_set_color(make_color_rgb(255, 215, 80));
                draw_text(_rx, _content_y, "GLOBAL PRODUCTION & COMBAT SERVICE METRICS (SOL REGISTRY):");

                var _prod_num = variable_struct_get(_active_suit, "production_count") ?? 3200;
                var _act_num = variable_struct_get(_active_suit, "active_units") ?? 2100;
                var _cas_num = variable_struct_get(_active_suit, "casualty_count") ?? 1100;
                var _kill_num = variable_struct_get(_active_suit, "kill_count") ?? 1850;
                var _ratio = variable_struct_get(_active_suit, "combat_loss_ratio") ?? 0.59;
                var _surv = variable_struct_get(_active_suit, "survivability_rating") ?? 63;

                draw_set_color(c_white);
                draw_text(_rx, _content_y + 24, "* Total Units Manufactured: " + string(_prod_num) + " Units System-Wide");
                draw_text(_rx, _content_y + 44, "* Active in Frontline Service: " + string(_act_num) + " Operational Hulls");
                draw_text(_rx, _content_y + 64, "* Confirmed Combat Losses: " + string(_cas_num) + " Neutralized Hulls");
                draw_text(_rx, _content_y + 84, "* Confirmed Enemy Kills: " + string(_kill_num) + " Neutralized Targets");
                draw_text(_rx, _content_y + 104, "* Combat Loss / Kill Ratio: " + string(_ratio));

                // Survivability Meter Bar
                draw_text(_rx, _content_y + 128, "* Frontline Survivability Rating: " + string(_surv) + "%");
                var _bar_x = _rx + 240;
                var _bar_y = _content_y + 130;
                var _bar_w = 220;
                var _bar_h = 12;
                draw_set_color(make_color_rgb(20, 30, 40));
                draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_w, _bar_y + _bar_h, false);
                var _fill_w = (_surv / 100.0) * _bar_w;
                var _surv_col = (_surv >= 65) ? make_color_rgb(80, 240, 120) : ((_surv >= 45) ? make_color_rgb(255, 200, 60) : make_color_rgb(255, 80, 80));
                draw_set_color(_surv_col);
                draw_rectangle(_bar_x, _bar_y, _bar_x + _fill_w, _bar_y + _bar_h, false);
                draw_set_color(make_color_rgb(80, 120, 160));
                draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_w, _bar_y + _bar_h, true);

                // Military Procurement & Adoption State Banner
                var _ban_y = _content_y + 158;
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_rx, _ban_y, "MILITARY PROCUREMENT & ADOPTION STATUS:");

                var _astat = variable_struct_get(_active_suit, "adoption_status") ?? "standard_issue";
                var _rep_by = variable_struct_get(_active_suit, "replaced_by") ?? "";
                var _status_box_y = _ban_y + 22;

                var _s_col = make_color_rgb(14, 28, 42);
                var _s_border = make_color_rgb(40, 90, 140);
                var _s_title = "[STANDARD ISSUE DOCTRINE]";
                var _s_desc = "Primary active frontline warframe deployed across regular standing army garrisons.";

                if (_astat == "adopted") {
                    _s_col = make_color_rgb(36, 32, 12);
                    _s_border = make_color_rgb(240, 200, 60);
                    _s_title = "[★ PROCUREMENT TENDER ADOPTED ★]";
                    _s_desc = "Selected as premier doctrinal contract winner! Priority factory lines active.";
                } else if (_astat == "replaced_by_player") {
                    _s_col = make_color_rgb(14, 38, 22);
                    _s_border = make_color_rgb(80, 240, 120);
                    _s_title = "[! REPLACED BY PMC DREADNOUGHT BLUEPRINT !]";
                    _s_desc = "Official procurement canceled. Tooling converted to Player Model: '" + (_rep_by != "" ? _rep_by : "PMC Vanguard") + "'.";
                } else if (_astat == "replaced_by_competitor") {
                    _s_col = make_color_rgb(38, 18, 14);
                    _s_border = make_color_rgb(255, 120, 60);
                    _s_title = "[! REPLACED BY COMPETITOR R&D LINE !]";
                    _s_desc = "Phased out in favor of rival corporation: '" + (_rep_by != "" ? _rep_by : "Rival Model") + "'. Relegated to scrap reserves.";
                } else if (_astat == "contested") {
                    _s_col = make_color_rgb(30, 28, 14);
                    _s_border = make_color_rgb(255, 230, 90);
                    _s_title = "[CONTESTED PROTOTYPE TENDER]";
                    _s_desc = "Proprietary mercenary blueprint actively competing in Sol procurement fly-offs.";
                } else if (_astat == "phased_out") {
                    _s_col = make_color_rgb(18, 20, 24);
                    _s_border = make_color_rgb(120, 130, 140);
                    _s_title = "[PHASED OUT TO RESERVES]";
                    _s_desc = "Decommissioned from primary line service; maintained only by planetary militias.";
                }

                draw_set_color(_s_col);
                draw_rectangle(_rx, _status_box_y, _rx + _col3_w - 32, _status_box_y + 54, false);
                draw_set_color(_s_border);
                draw_rectangle(_rx, _status_box_y, _rx + _col3_w - 32, _status_box_y + 54, true);

                draw_set_color(_s_border);
                draw_text(_rx + 12, _status_box_y + 6, _s_title);
                draw_set_color(make_color_rgb(210, 225, 240));
                draw_text_ext(_rx + 12, _status_box_y + 22, _s_desc, 13, _col3_w - 56);

                // Primary Operational Theaters
                var _th_y = _status_box_y + 68;
                draw_set_color(make_color_rgb(240, 210, 100));
                draw_text(_rx, _th_y, "PRIMARY DEPLOYMENT THEATERS:");
                var _theaters = variable_struct_get(_active_suit, "primary_theaters") ?? ["Baikal Redoubt", "Low Earth Orbit Fortress"];
                if (is_array(_theaters)) {
                    for (var th = 0; th < array_length(_theaters); th++) {
                        draw_set_color(make_color_rgb(180, 210, 240));
                        draw_text(_rx + 12, _th_y + 20 + th * 18, "> " + string(_theaters[th]));
                    }
                }
            }
            // =================================================================
            // TAB 2: HISTORICAL DOSSIER & DYNAMIC PLAYTHROUGH CHRONICLE
            // =================================================================
            else if (bp_archive_dossier_tab == 2) {
                // Historical Development Dossier
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_rx, _content_y, "HISTORICAL DEVELOPMENT & TENDER ORIGIN:");
                draw_set_color(make_color_rgb(200, 215, 230));
                var _hlore = variable_struct_get(_active_suit, "historical_lore") ?? (variable_struct_get(_active_suit, "manufacturing_lore") ?? "Classified defense project.");
                draw_text_ext(_rx, _content_y + 20, _hlore, 16, _col3_w - 32);

                // Manufacturing Quirks
                var _q_y = _content_y + 115;
                draw_set_color(make_color_rgb(255, 200, 80));
                draw_text(_rx, _q_y, "MANUFACTURING QUIRKS & MAINTENANCE QUOTIDIAN:");
                draw_set_color(make_color_rgb(190, 205, 220));
                var _quirks = variable_struct_get(_active_suit, "manufacturing_quirks") ?? "Standard factory tolerances.";
                draw_text_ext(_rx, _q_y + 20, _quirks, 16, _col3_w - 32);

                // Battlefield Reputation
                var _rep_y = _q_y + 68;
                draw_set_color(make_color_rgb(255, 140, 60));
                draw_text(_rx, _rep_y, "PILOT COCKPIT REPUTATION & SLANG:");
                draw_set_color(make_color_rgb(190, 205, 220));
                var _rep = variable_struct_get(_active_suit, "battlefield_reputation") ?? "Known as reliable military hardware.";
                draw_text_ext(_rx, _rep_y + 20, _rep, 16, _col3_w - 32);

                // Dynamic Playthrough Service Chronicle
                var _chr_y = _rep_y + 68;
                draw_set_color(make_color_rgb(80, 255, 140));
                draw_text(_rx, _chr_y, "DYNAMIC SERVICE CHRONICLE (PLAYTHROUGH LOG):");

                var _chr_box_y = _chr_y + 20;
                var _chr_box_h = 92;
                draw_set_color(make_color_rgb(10, 16, 24));
                draw_rectangle(_rx, _chr_box_y, _rx + _col3_w - 32, _chr_box_y + _chr_box_h, false);
                draw_set_color(make_color_rgb(35, 65, 95));
                draw_rectangle(_rx, _chr_box_y, _rx + _col3_w - 32, _chr_box_y + _chr_box_h, true);

                var _chron = variable_struct_get(_active_suit, "dynamic_lore_chronicle") ?? ["[Cycle 1] Commissioned into active fleet service."];
                if (is_array(_chron)) {
                    var _max_chr_vis = 3;
                    var _chr_len = array_length(_chron);
                    bp_archive_chronicle_scroll = clamp(bp_archive_chronicle_scroll, 0, max(0, _chr_len - _max_chr_vis));

                    for (var ci = 0; ci < min(_max_chr_vis, _chr_len); ci++) {
                        var _c_idx = ci + bp_archive_chronicle_scroll;
                        if (_c_idx >= _chr_len) break;
                        var _centry = _chron[_c_idx];
                        draw_set_color(make_color_rgb(180, 230, 255));
                        draw_text_ext(_rx + 10, _chr_box_y + 8 + ci * 28, "[*] " + string(_centry), 14, _col3_w - 52);
                    }

                    if (_chr_len > _max_chr_vis) {
                        var _c_prev_hov = (_mx >= _rx + _col3_w - 130 && _mx <= _rx + _col3_w - 85 && _my >= _chr_y && _my <= _chr_y + 18);
                        var _c_next_hov = (_mx >= _rx + _col3_w - 80 && _mx <= _rx + _col3_w - 35 && _my >= _chr_y && _my <= _chr_y + 18);
                        if (_c_prev_hov && _click && bp_archive_chronicle_scroll > 0) bp_archive_chronicle_scroll--;
                        if (_c_next_hov && _click && bp_archive_chronicle_scroll + _max_chr_vis < _chr_len) bp_archive_chronicle_scroll++;

                        draw_set_color(_c_prev_hov ? make_color_rgb(60, 120, 180) : make_color_rgb(25, 45, 65));
                        draw_rectangle(_rx + _col3_w - 130, _chr_y, _rx + _col3_w - 85, _chr_y + 18, false);
                        draw_set_color(c_white);
                        draw_text(_rx + _col3_w - 125, _chr_y + 2, "< PREV");

                        draw_set_color(_c_next_hov ? make_color_rgb(60, 120, 180) : make_color_rgb(25, 45, 65));
                        draw_rectangle(_rx + _col3_w - 80, _chr_y, _rx + _col3_w - 35, _chr_y + 18, false);
                        draw_set_color(c_white);
                        draw_text(_rx + _col3_w - 75, _chr_y + 2, "NEXT >");
                    }
                }
            }

            // Action Buttons at Bottom
            var _act_y = _col3_y + _col3_h - 110;
            var _btn_w = _col3_w - 32;

            // Combat Sortie Button
            var _cb_hov = (_mx >= _rx && _mx <= _rx + _btn_w && _my >= _act_y && _my <= _act_y + 44);
            if (_cb_hov && _click && room_exists(rm_combat)) room_goto(rm_combat);
            draw_set_color(_cb_hov ? make_color_rgb(30, 95, 55) : make_color_rgb(18, 55, 30));
            draw_rectangle(_rx, _act_y, _rx + _btn_w, _act_y + 44, false);
            draw_set_color(make_color_rgb(80, 240, 120));
            draw_rectangle(_rx, _act_y, _rx + _btn_w, _act_y + 44, true);
            draw_set_color(c_white);
            draw_text(_rx + 16, _act_y + 14, ">> DEPLOY TO TACTICAL COMBAT (rm_combat) <<");

            // Animation Sandbox Button
            var _sb_y = _act_y + 52;
            var _sb_hov = (_mx >= _rx && _mx <= _rx + _btn_w && _my >= _sb_y && _my <= _sb_y + 44);
            if (_sb_hov && _click && room_exists(Room1)) room_goto(Room1);
            draw_set_color(_sb_hov ? make_color_rgb(160, 65, 20) : make_color_rgb(90, 32, 10));
            draw_rectangle(_rx, _sb_y, _rx + _btn_w, _sb_y + 44, false);
            draw_set_color(make_color_rgb(255, 140, 40));
            draw_rectangle(_rx, _sb_y, _rx + _btn_w, _sb_y + 44, true);
            draw_set_color(c_white);
            draw_text(_rx + 16, _sb_y + 14, ">> LIVE ANIMATION SANDBOX (Room1) <<");
        }
    }
}

else if (active_tab == 1) {
    // Triple Subtabs: Base Facilities vs Modular Part Forge vs Custom Combinations Assembly (Doc 07, Doc 13)
    var _fsub_names = [
        "[1. BASE FACILITIES & ASSEMBLY]",
        "[2. MODULAR PART FORGE]",
        "[3. MECH ASSEMBLY BAY]"
    ];
    var _fsub_w = floor((_pan_w - 48) / 3);
    var _fsub_y = _pan_y + 8;
    for (var fst = 0; fst < 3; fst++) {
        var _fsx = _pan_x + 30 + fst * (_fsub_w + 14);
        var _fst_active = (factory_subtab == fst);
        var _fst_hov = (_mx >= _fsx && _mx <= _fsx + _fsub_w && _my >= _fsub_y && _my <= _fsub_y + 30);
        if (_fst_hov && _click) { factory_subtab = fst; scr_audio_play_ui("click"); }

        draw_set_color(_fst_active ? make_color_rgb(25, 55, 88) : (_fst_hov ? make_color_rgb(18, 38, 60) : make_color_rgb(12, 20, 32)));
        draw_rectangle(_fsx, _fsub_y, _fsx + _fsub_w, _fsub_y + 30, false);
        draw_set_color(_fst_active ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 75, 110));
        draw_rectangle(_fsx, _fsub_y, _fsx + _fsub_w, _fsub_y + 30, true);
        draw_set_color(_fst_active ? c_white : make_color_rgb(160, 190, 220));
        draw_text(_fsx + 14, _fsub_y + 7, _fsub_names[fst]);
    }

    // =========================================================================
    // SUBTAB 0: BASE FACILITIES, ASSEMBLY LINES & PERSONNEL ROSTER (docs/07)
    // =========================================================================
    if (factory_subtab == 0) {
        var _f_x = _pan_x + 30;
        var _f_y = _pan_y + 44;

        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(_f_x, _f_y, "== FACTORY OPERATIONS & PERSONNEL ROSTER ==");

        // Left Column: Facility Upgrades & Assembly Lines
        var _col1_w = 580;
        scr_draw_snes_panel(_f_x, _f_y + 24, _col1_w, 556, "FACILITY UPGRADES & ASSEMBLY LINES", make_color_rgb(80, 180, 240), false, 0.04);

        draw_set_color(make_color_rgb(240, 210, 100));
        draw_text(_f_x + 16, _f_y + 36, "FACILITY SPECIFICATIONS & MANUFACTURING UPGRADES:");

        if (instance_exists(obj_GameManager)) {
            var _gm = obj_GameManager;
            draw_set_color(c_white);
            draw_text(_f_x + 16, _f_y + 60, "* Synthesis Crucible: Tier " + string(_gm.facilities.crucible_tier) + " (Max 3000°C / 2000 PSI)");
            draw_text(_f_x + 16, _f_y + 82, "* Containment Shielding: " + (_gm.facilities.containment_shielding ? "ONLINE" : "OFFLINE"));
            draw_text(_f_x + 16, _f_y + 104, "* Active Assembly Lines: " + string(_gm.facilities.assembly_lines) + " / 4 Bays");

            // Upgrade Buttons
            // 1. Upgrade Crucible
            var _u1_y = _f_y + 130;
            var _u1_hov = (_mx >= _f_x + 16 && _mx <= _f_x + 550 && _my >= _u1_y && _my <= _u1_y + 32);
            if (_u1_hov && _click && _gm.facilities.crucible_tier == 1) {
                if (_gm.spend_funds(250000)) {
                    _gm.facilities.crucible_tier = 2;
                    _gm.facilities.foundry_crucibles = 2;
                    _gm.facilities.lab_tier = 2;
                    show_toast("CRUCIBLE UPGRADED TO TIER 2 (6000°C / 10,000 PSI)!", c_lime);
                } else {
                    show_toast("INSUFFICIENT FUNDS! (Requires 250,000 Cr)", c_red);
                }
            }
            scr_draw_snes_button(_f_x + 16, _u1_y, 534, 32, _gm.facilities.crucible_tier > 1 ? "[CRUCIBLE TIER 2 INSTALLED]" : "[UPGRADE CRUCIBLE: TIER 2 - 250,000 Cr]", _u1_hov, false, make_color_rgb(80, 220, 120));

            // 2. Expand Assembly Lines
            var _u2_y = _u1_y + 40;
            var _u2_hov = (_mx >= _f_x + 16 && _mx <= _f_x + 550 && _my >= _u2_y && _my <= _u2_y + 32);
            if (_u2_hov && _click && _gm.facilities.assembly_lines < 4) {
                if (_gm.spend_funds(300000)) {
                    _gm.facilities.assembly_lines++;
                    _gm.facilities.hangar_bays = _gm.facilities.assembly_lines;
                    show_toast("ASSEMBLY CAPACITY EXPANDED TO " + string(_gm.facilities.assembly_lines) + " BAYS!", c_lime);
                } else {
                    show_toast("INSUFFICIENT FUNDS! (Requires 300,000 Cr)", c_red);
                }
            }
            scr_draw_snes_button(_f_x + 16, _u2_y, 534, 32, "[COMMISSION NEW ASSEMBLY LINE - 300,000 Cr]", _u2_hov, false, make_color_rgb(80, 180, 240));

            // Queue Fabrication Button
            var _fab_y = _u2_y + 50;
            draw_set_color(make_color_rgb(240, 210, 100));
            draw_text(_f_x + 16, _fab_y, "ACTIVE FABRICATION QUEUE:");
            for (var fb = 0; fb < array_length(_gm.facilities.active_fabrications); fb++) {
                var _fitem = _gm.facilities.active_fabrications[fb];
                draw_set_color(c_white);
                draw_text(_f_x + 16, _fab_y + 24 + fb * 24, string(fb + 1) + ". " + _fitem.name + " (" + string(_fitem.days_remaining) + " / " + string(_fitem.total_days) + " Days Remaining)");
            }

            var _q_btn_y = _fab_y + 80;
            var _q_hov = (_mx >= _f_x + 16 && _mx <= _f_x + 550 && _my >= _q_btn_y && _my <= _q_btn_y + 36);
            if (_q_hov && _click && array_length(_gm.facilities.active_fabrications) < _gm.facilities.assembly_lines) {
                if (_gm.spend_funds(380000)) {
                    array_push(_gm.facilities.active_fabrications, {
                        mech_blueprint: "bp_ms_ironclad_07",
                        name: "GHA-07 Ironclad Batch-" + string(array_length(_gm.inventory.deployable_mechs) + 2),
                        days_remaining: 12,
                        total_days: 12
                    });
                    show_toast("NEW MOBILE SUIT COMMISSIONED IN ASSEMBLY BAY!", c_lime);
                } else {
                    show_toast("INSUFFICIENT FUNDS! (Requires 380,000 Cr)", c_red);
                }
            }
            draw_set_color(_q_hov ? make_color_rgb(60, 40, 20) : make_color_rgb(32, 22, 12));
            draw_rectangle(_f_x + 16, _q_btn_y, _f_x + 550, _q_btn_y + 36, false);
            draw_set_color(make_color_rgb(240, 160, 60));
            draw_rectangle(_f_x + 16, _q_btn_y, _f_x + 550, _q_btn_y + 36, true);
            draw_set_color(c_white);
            draw_text(_f_x + 24, _q_btn_y + 10, "[FABRICATE GHA-07 IRONCLAD - 380,000 Cr (12 DAYS)]");

            var _q2_btn_y = _q_btn_y + 40;
            var _q2_hov = (_mx >= _f_x + 16 && _mx <= _f_x + 550 && _my >= _q2_btn_y && _my <= _q2_btn_y + 34);
            if (_q2_hov && _click) {
                _gm.fabricate_mech_advanced("bp_ms_ironclad_07", "GHA-07 Ironclad (Forged)", 12, 180000, 4, 10);
            }
            draw_set_color(_q2_hov ? make_color_rgb(20, 60, 40) : make_color_rgb(12, 32, 22));
            draw_rectangle(_f_x + 16, _q2_btn_y, _f_x + 550, _q2_btn_y + 34, false);
            draw_set_color(make_color_rgb(60, 220, 120));
            draw_rectangle(_f_x + 16, _q2_btn_y, _f_x + 550, _q2_btn_y + 34, true);
            draw_set_color(c_white);
            draw_text(_f_x + 24, _q2_btn_y + 8, "[ALLOY FORGE: 180,000 Cr + 4x VANGUARD + 10x TUNGSTEN]");
        }

        // Right Column: Personnel Roster & Hiring Market
        var _col2_x = _f_x + _col1_w + 30;
        var _col2_w = _pan_w - _col1_w - 70;

        scr_draw_snes_panel(_col2_x, _f_y + 24, _col2_w, 556, "ACTIVE PERSONNEL & PILOT ROSTER", make_color_rgb(255, 195, 60), false, 0.04);

        draw_set_color(make_color_rgb(240, 210, 100));
        draw_text(_col2_x + 16, _f_y + 36, "ACTIVE PERSONNEL & PILOT ROSTER:");

        if (instance_exists(obj_GameManager)) {
            var _gm = obj_GameManager;
            var _py_start = _f_y + 64;
            for (var p = 0; p < array_length(_gm.facilities.roster_pilots); p++) {
                var _plt = _gm.facilities.roster_pilots[p];
                if (!is_struct(_plt)) continue;
                var _p_stat = variable_struct_get(_plt, "status") ?? "ACTIVE";
                var _plt_ref = variable_struct_get(_plt, "character_id") ?? (variable_struct_get(_plt, "id") ?? _plt);
                scr_draw_composite_portrait(_plt_ref, _col2_x + 16, _py_start + p * 30, 24, true, "");
                draw_set_color(_p_stat == "HOSPITALIZED" ? make_color_rgb(255, 180, 80) : c_white);
                var _rec_days = variable_struct_get(_plt, "recovery_days_left") ?? (variable_struct_get(_plt, "recovery_days") ?? 0);
                var _stat_tag = (_p_stat == "HOSPITALIZED") ? " [HOSPITALIZED - " + string(_rec_days) + "d]" : "";
                var _p_name = variable_struct_get(_plt, "name") ?? "Pilot";
                var _p_call = variable_struct_get(_plt, "callsign") ?? "ACE";
                var _p_acc = variable_struct_get(_plt, "accuracy") ?? ((variable_struct_get(_plt, "combat_stat") ?? 8) * 10);
                var _p_sal = variable_struct_get(_plt, "salary_daily") ?? 150;
                draw_text(_col2_x + 46, _py_start + p * 30 + 4, string(p + 1) + ". " + _p_name + " (" + _p_call + ")" + _stat_tag + " - Acc: " + string(_p_acc) + "% | Sal: " + string(_p_sal) + " Cr");
            }

            // Available Hire Candidates (Paged 3 per view to prevent bottom screen bleed)
            var _hire_y = _py_start + min(3, array_length(_gm.facilities.roster_pilots)) * 28 + 26;
            var _tot_cands = array_length(_gm.facilities.available_hire_pilots);
            var _max_vis_hire = 3;
            var _tot_hire_pages = max(1, ceil(_tot_cands / _max_vis_hire));
            if (hire_pilot_page >= _tot_hire_pages) hire_pilot_page = max(0, _tot_hire_pages - 1);

            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_col2_x + 16, _hire_y, "FREE AGENT PILOT REGISTRY (PAGE " + string(hire_pilot_page + 1) + "/" + string(_tot_hire_pages) + "):");

            var _hovered_cand = undefined;
            var _start_hire_idx = hire_pilot_page * _max_vis_hire;
            var _vis_count = min(_max_vis_hire, _tot_cands - _start_hire_idx);

            for (var h = 0; h < _vis_count; h++) {
                var _real_h_idx = _start_hire_idx + h;
                var _cand = _gm.facilities.available_hire_pilots[_real_h_idx];
                if (!is_struct(_cand)) continue;
                var _cy = _hire_y + 26 + h * 74;
                var _c_h = 66;

                draw_set_color(make_color_rgb(16, 24, 34));
                draw_rectangle(_col2_x + 16, _cy, _col2_x + _col2_w - 16, _cy + _c_h, false);
                draw_set_color(make_color_rgb(45, 75, 110));
                draw_rectangle(_col2_x + 16, _cy, _col2_x + _col2_w - 16, _cy + _c_h, true);

                // Layered 5-Stack Procedural Portrait Compositor (54x54 px)
                var _cand_ref = variable_struct_get(_cand, "character_id") ?? (variable_struct_get(_cand, "id") ?? _cand);
                scr_draw_composite_portrait(_cand_ref, _col2_x + 22, _cy + 6, 54, true, "");

                var _c_name = variable_struct_get(_cand, "name") ?? "Candidate";
                var _c_call = variable_struct_get(_cand, "callsign") ?? "ACE";
                var _c_bg = variable_struct_get(_cand, "background") ?? (variable_struct_get(_cand, "bio") ?? (variable_struct_get(_cand, "traits") ?? "Mercenary Pilot"));
                var _c_combat = variable_struct_get(_cand, "combat_stat") ?? floor((variable_struct_get(_cand, "accuracy") ?? 80) / 10);
                var _c_tactics = variable_struct_get(_cand, "tactics_stat") ?? floor((variable_struct_get(_cand, "reflexes") ?? 70) / 10);
                var _c_salary = variable_struct_get(_cand, "salary_daily") ?? 150;
                var _c_bonus = variable_struct_get(_cand, "signing_bonus") ?? (variable_struct_get(_cand, "bonus_hire") ?? 35000);
                var _disc = variable_struct_get(_cand, "referral_discount") ?? 0;
                var _disc_tag = (_disc > 0) ? " [FRIEND REFERRAL -25%]" : "";

                draw_set_color(make_color_rgb(240, 210, 100));
                draw_text(_col2_x + 84, _cy + 8, _c_name + " [" + _c_call + "]");
                draw_set_color(c_white);
                draw_text(_col2_x + 84, _cy + 26, "Combat Rating: " + string(_c_combat) + " | Tactics: " + string(_c_tactics) + " | Salary: " + string(_c_salary) + " Cr/day");
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_col2_x + 84, _cy + 44, "Signing Bonus: " + string(_c_bonus) + " Cr" + _disc_tag);

                // Check Card Hover for floating dossier
                if (_mx >= _col2_x + 16 && _mx <= _col2_x + _col2_w - 160 && _my >= _cy && _my <= _cy + _c_h) {
                    _hovered_cand = _cand;
                }

                // Hire Button
                var _hbtn_x = _col2_x + _col2_w - 150;
                var _hbtn_y = _cy + 16;
                var _h_hov = (_mx >= _hbtn_x && _mx <= _hbtn_x + 130 && _my >= _hbtn_y && _my <= _hbtn_y + 34);
                if (_h_hov && _click) {
                    if (_gm.spend_funds(_c_bonus)) {
                        _cand.name = _c_name;
                        _cand.callsign = _c_call;
                        _cand.combat_stat = _c_combat;
                        _cand.tactics_stat = _c_tactics;
                        _cand.accuracy = variable_struct_get(_cand, "accuracy") ?? (_c_combat * 10);
                        _cand.reflexes = variable_struct_get(_cand, "reflexes") ?? (_c_tactics * 10);
                        _cand.salary_daily = _c_salary;
                        _cand.status = variable_struct_get(_cand, "status") ?? "ACTIVE";
                        _cand.is_deployed = variable_struct_get(_cand, "is_deployed") ?? false;
                        _cand.recovery_days = variable_struct_get(_cand, "recovery_days") ?? 0;
                        _cand.recovery_days_left = variable_struct_get(_cand, "recovery_days_left") ?? 0;
                        _cand.kills = variable_struct_get(_cand, "kills") ?? 0;
                        _cand.sorties = variable_struct_get(_cand, "sorties") ?? 0;
                        array_push(_gm.facilities.roster_pilots, _cand);
                        array_delete(_gm.facilities.available_hire_pilots, _real_h_idx, 1);
                        show_toast("NEW ACE COMMISSIONED: " + _c_name + " joined squad!", c_lime);
                        break;
                    } else {
                        show_toast("INSUFFICIENT FUNDS! Need " + string(_c_bonus) + " Cr", c_red);
                    }
                }
                draw_set_color(_h_hov ? make_color_rgb(20, 80, 40) : make_color_rgb(12, 45, 22));
                draw_rectangle(_hbtn_x, _hbtn_y, _hbtn_x + 130, _hbtn_y + 34, false);
                draw_set_color(make_color_rgb(80, 220, 120));
                draw_rectangle(_hbtn_x, _hbtn_y, _hbtn_x + 130, _hbtn_y + 34, true);
                draw_set_color(c_white);
                draw_text(_hbtn_x + 12, _hbtn_y + 9, "[HIRE PILOT]");
            }

            // Hire Candidates Paging Controls
            if (_tot_cands > _max_vis_hire) {
                var _hp_y = _hire_y + 26 + _vis_count * 74 + 4;
                var _can_prev_hp = (hire_pilot_page > 0);
                var _can_next_hp = (hire_pilot_page < _tot_hire_pages - 1);

                var _pbtn_w = 140;
                var _pbtn_h = 28;
                var _hp_prev_hov = (_can_prev_hp && _mx >= _col2_x + 16 && _mx <= _col2_x + 16 + _pbtn_w && _my >= _hp_y && _my <= _hp_y + _pbtn_h);
                if (_hp_prev_hov && _click) {
                    hire_pilot_page -= 1;
                    scr_audio_play_ui("click");
                }
                scr_draw_snes_button(_col2_x + 16, _hp_y, _pbtn_w, _pbtn_h, "< PREV PILOTS", _hp_prev_hov, false, _can_prev_hp ? make_color_rgb(100, 200, 255) : make_color_rgb(60, 80, 100));

                var _hp_next_hov = (_can_next_hp && _mx >= _col2_x + 166 && _mx <= _col2_x + 166 + _pbtn_w && _my >= _hp_y && _my <= _hp_y + _pbtn_h);
                if (_hp_next_hov && _click) {
                    hire_pilot_page += 1;
                    scr_audio_play_ui("click");
                }
                scr_draw_snes_button(_col2_x + 166, _hp_y, _pbtn_w, _pbtn_h, "NEXT PILOTS >", _hp_next_hov, false, _can_next_hp ? make_color_rgb(100, 200, 255) : make_color_rgb(60, 80, 100));
            }

            // Floating Character Dossier Tooltip
            if (!is_undefined(_hovered_cand) && instance_exists(obj_NemesisManager)) {
                var _cand_lookup = variable_struct_get(_hovered_cand, "character_id") ?? (variable_struct_get(_hovered_cand, "id") ?? undefined);
                var _hov_char = (!is_undefined(_cand_lookup)) ? obj_NemesisManager.get_character(_cand_lookup) : undefined;
                if (!is_undefined(_hov_char) && is_struct(_hov_char)) {
                    var _tt_w = 420;
                    var _tt_h = 130;
                    var _tt_x = clamp(_mx + 16, 50, _gw - _tt_w - 20);
                    var _tt_y = clamp(_my - 65, 80, _gh - _tt_h - 20);

                    draw_set_color(make_color_rgb(8, 12, 18));
                    draw_rectangle(_tt_x, _tt_y, _tt_x + _tt_w, _tt_y + _tt_h, false);
                    draw_set_color(make_color_rgb(70, 130, 190));
                    draw_rectangle(_tt_x, _tt_y, _tt_x + _tt_w, _tt_y + _tt_h, true);

                    var _h_id = variable_struct_get(_hov_char, "id") ?? _cand_lookup;
                    scr_draw_composite_portrait(_h_id, _tt_x + 10, _tt_y + 10, 110, true, "stoic");

                    var _h_name = variable_struct_get(_hov_char, "name") ?? "Pilot";
                    var _h_call = variable_struct_get(_hov_char, "callsign") ?? "ACE";
                    var _h_tier = string(variable_struct_get(_hov_char, "tier") ?? 1);
                    var _h_grudge = string(variable_struct_get(_hov_char, "grudge") ?? 0);

                    draw_set_color(make_color_rgb(240, 210, 100));
                    draw_text(_tt_x + 130, _tt_y + 10, _h_name + " [" + _h_call + "]");
                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_tt_x + 130, _tt_y + 30, "Tier: " + _h_tier + " | Grudge: " + _h_grudge);

                    var _li = variable_struct_get(_hov_char, "love_interest");
                    var _li_str = "None";
                    if (!is_undefined(_li) && is_struct(_li) && (variable_struct_get(_li, "target_id") ?? "") != "") {
                        var _li_tname = variable_struct_get(_li, "target_name") ?? "Unknown";
                        var _li_rel = variable_struct_get(_li, "relationship_type") ?? (variable_struct_get(_li, "archetype") ?? "Affiliation");
                        _li_str = _li_tname + " (" + _li_rel + ")";
                    }
                    draw_set_color(make_color_rgb(255, 150, 180));
                    draw_text(_tt_x + 130, _tt_y + 50, "Romance: " + _li_str);

                    var _fr = variable_struct_get(_hov_char, "friendships");
                    var _fr_count = 0;
                    if (is_struct(_fr) && is_array(variable_struct_get(_fr, "friend_ids"))) {
                        _fr_count = array_length(_fr.friend_ids);
                    } else if (is_array(_fr)) {
                        _fr_count = array_length(_fr);
                    }
                    draw_set_color(make_color_rgb(130, 220, 150));
                    draw_text(_tt_x + 130, _tt_y + 70, "Comrades: " + string(_fr_count) + " affiliated pilots");

                    var _def_hook = variable_struct_get(_hov_char, "active_defection_hook") ?? "";
                    if (_def_hook != "") {
                        draw_set_color(make_color_rgb(255, 200, 80));
                        draw_text_ext(_tt_x + 130, _tt_y + 90, "History: " + _def_hook, 14, _tt_w - 140);
                    }
                }
            }
        }
    }

    // =========================================================================
    // SUBTAB 1: MODULAR PART FORGE // ALLOY FABRICATION (docs/13)
    // =========================================================================
    else if (factory_subtab == 1) {
        var _pf_x = _pan_x + 30;
        var _pf_y = _pan_y + 44;

        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(_pf_x, _pf_y, "== MODULAR PART FABRICATOR // ALLOY COMPONENT FORGE ==");
        draw_set_color(make_color_rgb(160, 190, 220));
        draw_text(_pf_x, _pf_y + 18, "Forge high-performance modular components from synthesized alloys for custom mobile suit combinations!");

        if (instance_exists(obj_GameManager)) {
            var _gm = obj_GameManager;

            // Alloy Stockpile Header Banner (All 8 Canonical Sintered Alloys)
            var _sb_y = _pf_y + 38;
            var _sb_w = _pan_w - 60;
            draw_set_color(make_color_rgb(12, 18, 28));
            draw_rectangle(_pf_x, _sb_y, _pf_x + _sb_w, _sb_y + 54, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_pf_x, _sb_y, _pf_x + _sb_w, _sb_y + 54, true);

            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_pf_x + 14, _sb_y + 8, "ALLOY STOCK:");

            // Row 1 of Alloys
            scr_draw_alloy_swatch(_pf_x + 120, _sb_y + 6, 18, 14, "alloy_vanguard_comp");
            draw_set_color(make_color_rgb(180, 210, 235));
            draw_text(_pf_x + 144, _sb_y + 8, "Vanguard: " + string(_gm.get_alloy("alloy_vanguard_comp")));

            scr_draw_alloy_swatch(_pf_x + 280, _sb_y + 6, 18, 14, "alloy_hyperion_matrix");
            draw_set_color(make_color_rgb(100, 240, 255));
            draw_text(_pf_x + 304, _sb_y + 8, "Hyperion: " + string(_gm.get_alloy("alloy_hyperion_matrix")));

            scr_draw_alloy_swatch(_pf_x + 440, _sb_y + 6, 18, 14, "alloy_aerosteel_flux");
            draw_set_color(make_color_rgb(215, 170, 255));
            draw_text(_pf_x + 464, _sb_y + 8, "Aerosteel: " + string(_gm.get_alloy("alloy_aerosteel_flux")));

            scr_draw_alloy_swatch(_pf_x + 600, _sb_y + 6, 18, 14, "alloy_adamantine_carbide");
            draw_set_color(make_color_rgb(255, 170, 80));
            draw_text(_pf_x + 624, _sb_y + 8, "Adamantine: " + string(_gm.get_alloy("alloy_adamantine_carbide")));

            // Row 2 of Alloys (Canonical Apex Alloys)
            scr_draw_alloy_swatch(_pf_x + 120, _sb_y + 30, 18, 14, "alloy_reactive_damascus");
            draw_set_color(make_color_rgb(240, 120, 140));
            draw_text(_pf_x + 144, _sb_y + 32, "Damascus: " + string(_gm.get_alloy("alloy_reactive_damascus")));

            scr_draw_alloy_swatch(_pf_x + 280, _sb_y + 30, 18, 14, "alloy_tachyon_superalloy");
            draw_set_color(make_color_rgb(100, 255, 255));
            draw_text(_pf_x + 304, _sb_y + 32, "Tachyon: " + string(_gm.get_alloy("alloy_tachyon_superalloy")));

            scr_draw_alloy_swatch(_pf_x + 440, _sb_y + 30, 18, 14, "alloy_lunar_aerogel");
            draw_set_color(make_color_rgb(220, 240, 255));
            draw_text(_pf_x + 464, _sb_y + 32, "Aerogel: " + string(_gm.get_alloy("alloy_lunar_aerogel")));

            scr_draw_alloy_swatch(_pf_x + 600, _sb_y + 30, 18, 14, "alloy_sol_ferrite");
            draw_set_color(make_color_rgb(255, 220, 60));
            draw_text(_pf_x + 624, _sb_y + 32, "Sol Ferrite: " + string(_gm.get_alloy("alloy_sol_ferrite")));

            // Treasury display on right side of stockpile ribbon
            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_pf_x + _sb_w - 240, _sb_y + 18, "PMC FUNDS: " + string(_gm.funds) + " Cr");

            // Slot Selector Bar (6 slots)
            var _slot_names = [
                "[1. HEADS]",
                "[2. TORSOS]",
                "[3. ARMS]",
                "[4. LEGS]",
                "[5. BOOSTERS]",
                "[6. WEAPONS]"
            ];
            var _sl_w = floor((_sb_w - 50) / 6);
            var _sl_y = _sb_y + 64;

            for (var sl = 0; sl < 6; sl++) {
                var _slx = _pf_x + sl * (_sl_w + 10);
                var _sl_active = (forge_selected_slot == sl);
                var _sl_hov = (_mx >= _slx && _mx <= _slx + _sl_w && _my >= _sl_y && _my <= _sl_y + 28);
                if (_sl_hov && _click) forge_selected_slot = sl;

                draw_set_color(_sl_active ? make_color_rgb(35, 75, 120) : (_sl_hov ? make_color_rgb(22, 45, 70) : make_color_rgb(14, 22, 34)));
                draw_rectangle(_slx, _sl_y, _slx + _sl_w, _sl_y + 28, false);
                draw_set_color(_sl_active ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 75, 110));
                draw_rectangle(_slx, _sl_y, _slx + _sl_w, _sl_y + 28, true);
                draw_set_color(_sl_active ? c_white : make_color_rgb(160, 190, 220));
                draw_text(_slx + 12, _sl_y + 6, _slot_names[sl]);
            }

            // 5 Blueprint Cards for the selected slot
            var _cat_parts = modular_crafting_catalog[forge_selected_slot];
            var _num_parts = array_length(_cat_parts);
            var _card_gap = 12;
            var _card_w = floor((_sb_w - ((_num_parts - 1) * _card_gap)) / max(1, _num_parts));
            var _card_h = 410;
            var _card_y = _sl_y + 36;

            for (var ci = 0; ci < _num_parts; ci++) {
                var _pitem = _cat_parts[ci];
                var _cx = _pf_x + ci * (_card_w + _card_gap);

                // Card panel
                scr_draw_snes_panel(_cx, _card_y, _card_w, _card_h, _pitem.id, make_color_rgb(80, 180, 240), false);

                // Part Title
                draw_set_color(make_color_rgb(240, 215, 100));
                draw_text(_cx + 12, _card_y + 28, _pitem.name);
                draw_set_color(make_color_rgb(150, 180, 210));
                draw_text(_cx + 12, _card_y + 46, "Slot: " + string_upper(_pitem.slot));

                // Stats Box
                var _st_y = _card_y + 68;
                var _st_w = _card_w - 20;
                var _st_h = 160;
                draw_set_color(make_color_rgb(10, 14, 22));
                draw_rectangle(_cx + 10, _st_y, _cx + 10 + _st_w, _st_y + _st_h, false);
                draw_set_color(make_color_rgb(30, 50, 75));
                draw_rectangle(_cx + 10, _st_y, _cx + 10 + _st_w, _st_y + _st_h, true);

                draw_set_color(c_white);
                draw_text(_cx + 18, _st_y + 10, "Armor: " + string(_pitem.armor) + " HP");
                draw_text(_cx + 18, _st_y + 28, "Mass: " + string(_pitem.mass) + " Tonnes");

                if (variable_struct_exists(_pitem, "power_output")) {
                    draw_set_color(make_color_rgb(100, 255, 140));
                    draw_text(_cx + 18, _st_y + 46, "Core: +" + string(_pitem.power_output) + " MW Surplus");
                } else {
                    draw_set_color(make_color_rgb(255, 180, 100));
                    draw_text(_cx + 18, _st_y + 46, "Power Draw: -" + string(_pitem.power_draw) + " MW");
                }

                if (variable_struct_exists(_pitem, "base_speed")) {
                    draw_set_color(make_color_rgb(200, 240, 255));
                    draw_text(_cx + 18, _st_y + 64, "Speed: " + string(_pitem.base_speed) + " kph");
                } else if (variable_struct_exists(_pitem, "boost_bonus")) {
                    draw_set_color(make_color_rgb(200, 240, 255));
                    draw_text(_cx + 18, _st_y + 64, "Boost: +" + string(_pitem.boost_bonus) + " kph");
                } else if (variable_struct_exists(_pitem, "damage")) {
                    draw_set_color(make_color_rgb(255, 120, 120));
                    draw_text(_cx + 18, _st_y + 64, "Damage: " + string(_pitem.damage) + " Dmg");
                }

                draw_set_color(make_color_rgb(255, 215, 80));
                draw_text(_cx + 18, _st_y + 86, "Tactical Bonus:");
                draw_set_color(make_color_rgb(240, 240, 180));
                draw_text_ext(_cx + 18, _st_y + 104, _pitem.bonus, 13, _st_w - 16);

                // Material & Credit Costs
                var _cost_y = _st_y + _st_h + 12;
                var _cur_alloy_stock = _gm.get_alloy(_pitem.req_alloy);
                var _has_alloy = (_cur_alloy_stock >= _pitem.req_alloy_amount);
                var _has_cr = (_gm.funds >= _pitem.cost_cr);
                var _can_forge = (_has_alloy && _has_cr);

                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text(_cx + 14, _cost_y, "REQUIRED ALLOY:");
                scr_draw_alloy_swatch(_cx + 14, _cost_y + 20, 26, 18, _pitem.req_alloy);
                draw_set_color(_has_alloy ? c_lime : c_red);
                var _req_al_clean = string_replace_all(string_replace(_pitem.req_alloy, "alloy_", ""), "_", " ");
                draw_text(_cx + 46, _cost_y + 20, string(_pitem.req_alloy_amount) + "x " + _req_al_clean);
                draw_set_color(make_color_rgb(140, 170, 200));
                draw_text(_cx + 14, _cost_y + 44, "Stock: " + string(_cur_alloy_stock) + " | Cost: " + string(_pitem.cost_cr) + " Cr");

                // Forge Button
                var _f_btn_y = _cost_y + 70;
                var _f_btn_w = _card_w - 24;
                var _f_hov = (_mx >= _cx + 12 && _mx <= _cx + 12 + _f_btn_w && _my >= _f_btn_y && _my <= _f_btn_y + 32);

                if (_f_hov && _click) {
                    if (!_has_cr) {
                        show_toast("INSUFFICIENT FUNDS! (Requires " + string(_pitem.cost_cr) + " Cr)", c_red);
                    } else if (!_has_alloy) {
                        show_toast("INSUFFICIENT ALLOYS! (Requires " + string(_pitem.req_alloy_amount) + "x " + _pitem.req_alloy + ")", c_red);
                    } else {
                        _gm.craft_modular_part(_pitem, _pitem.req_alloy, _pitem.req_alloy_amount, _pitem.cost_cr);
                    }
                }

                scr_draw_snes_button(_cx + 12, _f_btn_y, _f_btn_w, 32, _can_forge ? "[FORGE PART]" : "[INSUFFICIENT]", _f_hov, false, _can_forge ? make_color_rgb(60, 220, 120) : make_color_rgb(160, 60, 60));
            }
        }
    }

    // =========================================================================
    // SUBTAB 2: CUSTOM MECH COMBINATIONS ASSEMBLY BAY (docs/13)
    // 3-COLUMN TACTICAL MECHA ENGINEERING DECK
    // =========================================================================
    else if (factory_subtab == 2) {
        var _ab_x = _pan_x + 30;
        var _ab_y = _pan_y + 44;

        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(_ab_x, _ab_y, "== CUSTOM MOBILE SUIT COMBINATIONS & ASSEMBLY BAY ==");
        draw_set_color(make_color_rgb(160, 190, 220));
        draw_text(_ab_x, _ab_y + 18, "Assemble modular heads, torsos, arms, legs, backpacks, and weapons into a fully operational mobile suit!");

        if (instance_exists(obj_GameManager)) {
            var _gm = obj_GameManager;
            var _pts = _gm.inventory.parts;

            // Clamp Indices
            assembly_head_idx = clamp(assembly_head_idx, 0, max(0, array_length(_pts.heads) - 1));
            assembly_torso_idx = clamp(assembly_torso_idx, 0, max(0, array_length(_pts.torsos) - 1));
            assembly_arms_idx = clamp(assembly_arms_idx, 0, max(0, array_length(_pts.arms) - 1));
            assembly_legs_idx = clamp(assembly_legs_idx, 0, max(0, array_length(_pts.legs) - 1));
            assembly_bp_idx = clamp(assembly_bp_idx, 0, max(0, array_length(_pts.backpacks) - 1));
            assembly_wp_idx = clamp(assembly_wp_idx, 0, max(0, array_length(_pts.weapons) - 1));

            var _hd = (array_length(_pts.heads) > 0) ? _pts.heads[assembly_head_idx] : undefined;
            var _tr = (array_length(_pts.torsos) > 0) ? _pts.torsos[assembly_torso_idx] : undefined;
            var _am = (array_length(_pts.arms) > 0) ? _pts.arms[assembly_arms_idx] : undefined;
            var _lg = (array_length(_pts.legs) > 0) ? _pts.legs[assembly_legs_idx] : undefined;
            var _bp = (array_length(_pts.backpacks) > 0) ? _pts.backpacks[assembly_bp_idx] : undefined;
            var _wp = (array_length(_pts.weapons) > 0) ? _pts.weapons[assembly_wp_idx] : undefined;

            var _has_all_6 = (!is_undefined(_hd) && !is_undefined(_tr) && !is_undefined(_am) && !is_undefined(_lg) && !is_undefined(_bp) && !is_undefined(_wp));

            var _deck_y = _ab_y + 36;
            var _deck_h = 516;

            // -----------------------------------------------------------------
            // COLUMN 1 (LEFT): EQUIPPED MODULAR HARDPOINTS (380px)
            // -----------------------------------------------------------------
            var _col1_x = _ab_x;
            var _col1_w = 380;

            scr_draw_snes_panel(_col1_x, _deck_y, _col1_w, _deck_h, "MODULAR HARDPOINTS", make_color_rgb(100, 220, 255), true);

            var _slot_items = [
                { title: "SLOT 1: HEAD SENSORS", part: _hd, list: _pts.heads, cur_idx: assembly_head_idx, key: "head" },
                { title: "SLOT 2: TORSO REACTOR CORE", part: _tr, list: _pts.torsos, cur_idx: assembly_torso_idx, key: "torso" },
                { title: "SLOT 3: ARMS & ACTUATORS", part: _am, list: _pts.arms, cur_idx: assembly_arms_idx, key: "arms" },
                { title: "SLOT 4: LEGS & HYDRAULICS", part: _lg, list: _pts.legs, cur_idx: assembly_legs_idx, key: "legs" },
                { title: "SLOT 5: BACKPACK BOOSTERS", part: _bp, list: _pts.backpacks, cur_idx: assembly_bp_idx, key: "backpack" },
                { title: "SLOT 6: PRIMARY WEAPON", part: _wp, list: _pts.weapons, cur_idx: assembly_wp_idx, key: "weapon" }
            ];

            for (var si = 0; si < 6; si++) {
                var _sitem = _slot_items[si];
                var _sy_pos = _deck_y + 24 + si * 78;
                var _is_sel_slot = (assembly_selected_slot == si);

                // Slot Card Hitbox
                var _card_hov = (_mx >= _col1_x + 12 && _mx <= _col1_x + _col1_w - 12 && _my >= _sy_pos && _my <= _sy_pos + 72);
                if (_card_hov && _click && _mx < _col1_x + _col1_w - 100) {
                    assembly_selected_slot = si;
                }

                draw_set_color(_is_sel_slot ? make_color_rgb(24, 40, 60) : (_card_hov ? make_color_rgb(18, 30, 46) : make_color_rgb(12, 18, 28)));
                draw_rectangle(_col1_x + 12, _sy_pos, _col1_x + _col1_w - 12, _sy_pos + 78, false);
                draw_set_color(_is_sel_slot ? make_color_rgb(255, 180, 50) : make_color_rgb(45, 75, 110));
                draw_rectangle(_col1_x + 12, _sy_pos, _col1_x + _col1_w - 12, _sy_pos + 78, true);

                // Slot Title & Cursor
                draw_set_color(_is_sel_slot ? make_color_rgb(255, 215, 80) : make_color_rgb(100, 220, 255));
                draw_text(_col1_x + 20, _sy_pos + 6, (_is_sel_slot ? "> " : "") + _sitem.title);

                var _p = _sitem.part;
                if (!is_undefined(_p)) {
                    // Mini Alloy Swatch if part has alloy
                    if (variable_struct_exists(_p, "req_alloy")) {
                        scr_draw_alloy_swatch(_col1_x + 20, _sy_pos + 24, 18, 14, _p.req_alloy);
                        draw_set_color(c_white);
                        draw_text(_col1_x + 44, _sy_pos + 22, _p.name);
                    } else {
                        draw_set_color(c_white);
                        draw_text(_col1_x + 20, _sy_pos + 22, _p.name);
                    }

                    draw_set_color(make_color_rgb(160, 190, 220));
                    var _stat_str = "HP: " + string(_p.armor) + " | " + string(_p.mass) + "t";
                    if (variable_struct_exists(_p, "power_output")) _stat_str += " | +" + string(_p.power_output) + " MW";
                    else _stat_str += " | -" + string(_p.power_draw) + " MW";
                    draw_text(_col1_x + 20, _sy_pos + 40, _stat_str);

                    draw_set_color(make_color_rgb(240, 215, 100));
                    draw_text(_col1_x + 20, _sy_pos + 56, _p.bonus);
                } else {
                    draw_set_color(c_red);
                    draw_text(_col1_x + 20, _sy_pos + 32, "[NO PART IN INVENTORY - FORGE]");
                }

                // Cycle Buttons (< and >)
                var _len = array_length(_sitem.list);
                var _btn_p_hov = (_mx >= _col1_x + _col1_w - 92 && _mx <= _col1_x + _col1_w - 56 && _my >= _sy_pos + 24 && _my <= _sy_pos + 52);
                if (_btn_p_hov && _click && _len > 1) {
                    if (si == 0) assembly_head_idx = (assembly_head_idx - 1 + _len) % _len;
                    else if (si == 1) assembly_torso_idx = (assembly_torso_idx - 1 + _len) % _len;
                    else if (si == 2) assembly_arms_idx = (assembly_arms_idx - 1 + _len) % _len;
                    else if (si == 3) assembly_legs_idx = (assembly_legs_idx - 1 + _len) % _len;
                    else if (si == 4) assembly_bp_idx = (assembly_bp_idx - 1 + _len) % _len;
                    else if (si == 5) assembly_wp_idx = (assembly_wp_idx - 1 + _len) % _len;
                }
                scr_draw_snes_button(_col1_x + _col1_w - 92, _sy_pos + 24, 34, 28, "<", _btn_p_hov, false, make_color_rgb(100, 220, 255));

                var _btn_n_hov = (_mx >= _col1_x + _col1_w - 52 && _mx <= _col1_x + _col1_w - 16 && _my >= _sy_pos + 24 && _my <= _sy_pos + 52);
                if (_btn_n_hov && _click && _len > 1) {
                    if (si == 0) assembly_head_idx = (assembly_head_idx + 1) % _len;
                    else if (si == 1) assembly_torso_idx = (assembly_torso_idx + 1) % _len;
                    else if (si == 2) assembly_arms_idx = (assembly_arms_idx + 1) % _len;
                    else if (si == 3) assembly_legs_idx = (assembly_legs_idx + 1) % _len;
                    else if (si == 4) assembly_bp_idx = (assembly_bp_idx + 1) % _len;
                    else if (si == 5) assembly_wp_idx = (assembly_wp_idx + 1) % _len;
                }
                scr_draw_snes_button(_col1_x + _col1_w - 52, _sy_pos + 24, 34, 28, ">", _btn_n_hov, false, make_color_rgb(100, 220, 255));
            }

            // -----------------------------------------------------------------
            // COLUMN 2 (CENTER): WANZER CAD SCHEMATIC WIREFRAME (440px)
            // -----------------------------------------------------------------
            var _col2_x = _col1_x + _col1_w + 14;
            var _col2_w = 440;

            scr_draw_snes_panel(_col2_x, _deck_y, _col2_w, _deck_h, "TACTICAL CAD SCHEMATIC", make_color_rgb(100, 220, 255), true);

            // CAD Viewport Enclosure
            var _cad_x = _col2_x + 12;
            var _cad_y = _deck_y + 32;
            var _cad_w = _col2_w - 24;
            var _cad_h = 280;

            draw_set_color(make_color_rgb(8, 12, 18));
            draw_rectangle(_cad_x, _cad_y, _cad_x + _cad_w, _cad_y + _cad_h, false);
            draw_set_color(make_color_rgb(30, 48, 70));
            draw_rectangle(_cad_x, _cad_y, _cad_x + _cad_w, _cad_y + _cad_h, true);

            // CAD Grid Lines
            draw_set_color(make_color_rgb(18, 28, 42));
            for (var cdx = _cad_x + 20; cdx < _cad_x + _cad_w; cdx += 32) draw_line(cdx, _cad_y, cdx, _cad_y + _cad_h);
            for (var cdy = _cad_y + 20; cdy < _cad_y + _cad_h; cdy += 32) draw_line(_cad_x, cdy, _cad_x + _cad_w, cdy);

            // Technical Grid Overlay text
            draw_set_color(make_color_rgb(80, 140, 190));
            draw_text(_cad_x + 8, _cad_y + 6, "CAD REF: 07.24 // CHASSIS: COMBINATIONS-MK5");

            // Draw Schematic Sprite Centerfold
            var _schem_cx = _cad_x + _cad_w / 2;
            var _schem_cy = _cad_y + _cad_h / 2;
            var _sc_scale = 0.38;
            var _sc_w = 1024 * _sc_scale;
            var _sc_h = 576 * _sc_scale;

            if (sprite_exists(spr_mech_schematic)) {
                // Base wireframe
                draw_sprite_ext(spr_mech_schematic, 0, _schem_cx - _sc_w / 2, _schem_cy - _sc_h / 2, _sc_scale, _sc_scale, 0, c_white, 0.40);

                // Procedural alloy armor plating tint from equipped torso
                if (!is_undefined(_tr) && variable_struct_exists(_tr, "req_alloy")) {
                    var _torso_col = scr_get_alloy_procedural_color(_tr.req_alloy);
                    draw_sprite_ext(spr_mech_schematic, 0, _schem_cx - _sc_w / 2, _schem_cy - _sc_h / 2, _sc_scale, _sc_scale, 0, _torso_col, 0.48);
                }
            }

            // Hardpoint Socket Coordinates on Schematic
            var _sock_coords = [
                { x: _schem_cx, y: _schem_cy - 72, label: "HEAD" },
                { x: _schem_cx, y: _schem_cy - 12, label: "CORE" },
                { x: _schem_cx - 70, y: _schem_cy - 12, label: "ARMS" },
                { x: _schem_cx, y: _schem_cy + 68, label: "LEGS" },
                { x: _schem_cx - 48, y: _schem_cy - 48, label: "BOOST" },
                { x: _schem_cx + 86, y: _schem_cy + 16, label: "WEAPON" }
            ];

            // Render Socket Connectors & Hitboxes
            for (var si = 0; si < 6; si++) {
                var _sc = _sock_coords[si];
                var _is_sel = (assembly_selected_slot == si);

                // Socket reticle ring
                draw_set_color(_is_sel ? make_color_rgb(255, 215, 80) : make_color_rgb(80, 200, 255));
                var _ring_r = _is_sel ? (7 + sin(current_time * 0.006) * 3) : 5;
                draw_circle(_sc.x, _sc.y, _ring_r, true);
                draw_circle(_sc.x, _sc.y, 2, false);

                // Targeting brackets if selected
                if (_is_sel) {
                    draw_set_color(make_color_rgb(255, 220, 80));
                    draw_text(_sc.x - 18, _sc.y - 18, "[");
                    draw_text(_sc.x + 12, _sc.y - 18, "]");
                    draw_text(_sc.x - 16, _sc.y + 8, _sc.label);
                }

                // Click on socket
                var _sock_hov = point_distance(_mx, _my, _sc.x, _sc.y) < 16;
                if (_sock_hov && _click) {
                    assembly_selected_slot = si;
                }
            }

            // Lower Section: Active Alloy Armor Composition Plaque
            var _plaq_y = _cad_y + _cad_h + 10;
            var _plaq_w = _col2_w - 24;
            var _plaq_h = 135;

            draw_set_color(make_color_rgb(12, 18, 28));
            draw_rectangle(_cad_x, _plaq_y, _cad_x + _plaq_w, _plaq_y + _plaq_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_cad_x, _plaq_y, _cad_x + _plaq_w, _plaq_y + _plaq_h, true);

            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_cad_x + 12, _plaq_y + 8, "ACTIVE ALLOY ARMOR COMPOSITION:");

            if (!is_undefined(_tr) && variable_struct_exists(_tr, "req_alloy")) {
                scr_draw_alloy_swatch(_cad_x + 12, _plaq_y + 30, 48, 48, _tr.req_alloy);
                var _al_hex = scr_alloy_get_hex(_tr.req_alloy);
                draw_set_color(c_white);
                draw_text(_cad_x + 68, _plaq_y + 30, string(_tr.req_alloy) + " (" + string(_al_hex) + ")");
                draw_set_color(make_color_rgb(160, 205, 235));
                draw_text(_cad_x + 68, _plaq_y + 48, "Sintered Hull Matrix // " + string(_tr.name));
                draw_set_color(make_color_rgb(100, 240, 160));
                draw_text(_cad_x + 68, _plaq_y + 66, "Armor Deflection: " + string(_tr.bonus));
            } else {
                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text(_cad_x + 12, _plaq_y + 32, "Equip a forged Torso to analyze composite metallurgy.");
            }

            // Weight Class Assessment Ribbon
            var _total_mass_calc = (_has_all_6) ? (_hd.mass + _tr.mass + _am.mass + _lg.mass + _bp.mass + _wp.mass) : 0;
            var _wclass_name = "MEDIUM MAINSTAY";
            var _wclass_desc = "Balanced Multi-Role Linebreaker";
            var _wclass_col = make_color_rgb(100, 220, 255);

            if (_total_mass_calc < 55) {
                _wclass_name = "LIGHT SKIRMISHER";
                _wclass_desc = "High Agility // +20% Evasion Rating";
                _wclass_col = make_color_rgb(120, 255, 160);
            } else if (_total_mass_calc >= 55 && _total_mass_calc < 85) {
                _wclass_name = "MEDIUM MAINSTAY";
                _wclass_desc = "Standard Linebreaker // Tactical Equilibrium";
                _wclass_col = make_color_rgb(100, 220, 255);
            } else if (_total_mass_calc >= 85 && _total_mass_calc < 110) {
                _wclass_name = "HEAVY ASSAULT";
                _wclass_desc = "Fortified Armor // Heavy Kinetic Ordnance";
                _wclass_col = make_color_rgb(255, 190, 60);
            } else {
                _wclass_name = "SUPERHEAVY SIEGEBREAKER";
                _wclass_desc = "Impenetrable Trench Fortress // Siege Rail";
                _wclass_col = make_color_rgb(255, 100, 80);
            }

            draw_set_color(_wclass_col);
            draw_text(_cad_x + 12, _plaq_y + 90, "WEIGHT CLASS: [ " + _wclass_name + " ]");
            draw_set_color(make_color_rgb(180, 210, 235));
            draw_text(_cad_x + 12, _plaq_y + 110, "R&D Doctrine: " + _wclass_desc);

            // Telemetry Status Ribbon
            var _link_y = _plaq_y + _plaq_h + 10;
            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_cad_x, _link_y, _cad_x + _plaq_w, _link_y + 24, false);
            draw_set_color(_has_all_6 ? make_color_rgb(80, 220, 120) : make_color_rgb(220, 70, 70));
            draw_rectangle(_cad_x, _link_y, _cad_x + _plaq_w, _link_y + 24, true);
            draw_text(_cad_x + 12, _link_y + 5, _has_all_6 ? "LINK: 6/6 HARDPOINTS SYNCHRONIZED" : "LINK: HARDPOINTS INCOMPLETE");

            // -----------------------------------------------------------------
            // COLUMN 3 (RIGHT): REAL-TIME ENGINEERING CALCULUS & ACTIONS (410px)
            // -----------------------------------------------------------------
            var _col3_x = _col2_x + _col2_w + 14;
            var _col3_w = 410;

            scr_draw_snes_panel(_col3_x, _deck_y, _col3_w, _deck_h, "ENGINEERING DIAGNOSTICS", make_color_rgb(255, 215, 80), true);

            // Designation & Preset Buttons
            draw_set_color(c_white);
            draw_text(_col3_x + 14, _deck_y + 32, "Designation: " + assembly_custom_name);

            var _presets = ["CHIMERA-X", "AEGIS-II", "VALKYRIE-S", "COLOSSUS-M"];
            var _pw = floor((_col3_w - 48) / 4);
            for (var pr = 0; pr < 4; pr++) {
                var _px = _col3_x + 14 + pr * (_pw + 6);
                var _py = _deck_y + 54;
                var _p_hov = (_mx >= _px && _mx <= _px + _pw && _my >= _py && _my <= _py + 24);
                if (_p_hov && _click) {
                    assembly_custom_name = _presets[pr];
                }
                scr_draw_snes_button(_px, _py, _pw, 24, _presets[pr], _p_hov, false, make_color_rgb(100, 220, 255));
            }

            // Real-Time Calculus
            if (_has_all_6) {
                var _total_armor = _hd.armor + _tr.armor + _am.armor + _lg.armor + _bp.armor + _wp.armor;
                var _power_draw = _hd.power_draw + _am.power_draw + _lg.power_draw + _bp.power_draw + _wp.power_draw;
                var _net_power = _tr.power_output - _power_draw;
                var _total_mass = _hd.mass + _tr.mass + _am.mass + _lg.mass + _bp.mass + _wp.mass;
                var _walk_speed = max(20, floor(_lg.base_speed * (1.0 - (_total_mass / 220.0))));
                var _boost_speed = _walk_speed + _bp.boost_bonus;
                var _combat_rating = floor((_total_armor / 5) + _wp.damage + (_boost_speed / 2) + (_net_power * 3));
                var _is_power_stable = (_net_power >= 0);

                var _diag_y = _deck_y + 86;
                var _gw_gauge = _col3_w - 28;

                // 1. Armor Integrity
                draw_set_color(c_white);
                draw_text(_col3_x + 14, _diag_y, "1. ARMOR INTEGRITY: " + string(_total_armor) + " HP / 2,500 HP");
                scr_draw_snes_gauge(_col3_x + 14, _diag_y + 18, _gw_gauge, 14, _total_armor, 2500, make_color_rgb(60, 200, 240), -1, 6);

                // 2. Tokamak Power Balance
                var _p_diag_y = _diag_y + 38;
                draw_set_color(_is_power_stable ? make_color_rgb(100, 255, 140) : make_color_rgb(255, 90, 90));
                draw_text(_col3_x + 14, _p_diag_y, "2. POWER: Net +" + string(_net_power) + " MW (Core: +" + string(_tr.power_output) + " / -" + string(_power_draw) + ")");
                scr_draw_snes_gauge(_col3_x + 14, _p_diag_y + 18, _gw_gauge, 14, max(0, _net_power), 40, _is_power_stable ? make_color_rgb(80, 220, 120) : c_red, -1, 6);

                if (!_is_power_stable) {
                    scr_draw_snes_hazard_bar(_col3_x + 14, _p_diag_y + 34, _gw_gauge, 8, true);
                    draw_set_color(make_color_rgb(255, 70, 70));
                    draw_text(_col3_x + 14, _p_diag_y + 44, "!! REACTOR OVERLOAD: DEFICIT " + string(abs(_net_power)) + " MW !!");
                }

                // 3. Mass & Mobility
                var _m_diag_y = _p_diag_y + (_is_power_stable ? 40 : 58);
                draw_set_color(make_color_rgb(200, 220, 240));
                draw_text(_col3_x + 14, _m_diag_y, "3. MOBILITY: " + string(_total_mass) + "t | Walk: " + string(_walk_speed) + " | Boost: " + string(_boost_speed) + " km/h");

                // 4. Armament Firepower
                var _w_diag_y = _m_diag_y + 24;
                draw_set_color(make_color_rgb(255, 180, 100));
                draw_text(_col3_x + 14, _w_diag_y, "4. PRIMARY WEAPON: " + string(_wp.name ?? "None") + " (" + string(_wp.damage) + " Dmg)");

                // 5. Tactical Rating Banner
                var _t_diag_y = _w_diag_y + 26;
                draw_set_color(make_color_rgb(16, 26, 38));
                draw_rectangle(_col3_x + 14, _t_diag_y, _col3_x + _col3_w - 14, _t_diag_y + 38, false);
                draw_set_color(make_color_rgb(255, 215, 80));
                draw_rectangle(_col3_x + 14, _t_diag_y, _col3_x + _col3_w - 14, _t_diag_y + 38, true);
                draw_set_color(make_color_rgb(255, 225, 100));
                draw_text(_col3_x + 22, _t_diag_y + 10, "TACTICAL COMBAT RATING: " + string(_combat_rating) + " PTS");

                // 6. Gihren's Greed Operational Telemetry
                var _gg_y = _t_diag_y + 46;
                var _lim_disp = 125;
                var _prop_disp = 140;
                var _ecm_disp = 35;
                if (instance_exists(obj_BlueprintManager)) {
                    var _pt = obj_BlueprintManager.active_prototype_tuning;
                    if (_pt.hydraulics.grade != "UNTESTED") _lim_disp = _pt.hydraulics.pilot_limit_pct;
                    if (_pt.thrusters.grade != "UNTESTED") _prop_disp = floor(150 * _pt.thrusters.fuel_eff_mult);
                }
                draw_set_color(make_color_rgb(10, 16, 24));
                draw_rectangle(_col3_x + 14, _gg_y, _col3_x + _col3_w - 14, _gg_y + 40, false);
                draw_set_color(make_color_rgb(45, 75, 110));
                draw_rectangle(_col3_x + 14, _gg_y, _col3_x + _col3_w - 14, _gg_y + 40, true);

                draw_set_color(make_color_rgb(255, 215, 80));
                draw_text(_col3_x + 20, _gg_y + 4, "LIMIT: " + string(_lim_disp) + "% | PROPELLANT: " + string(_prop_disp) + " EN | ECM: " + string(_ecm_disp) + "%");
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_col3_x + 20, _gg_y + 22, "TERRAIN: G:A S:A U:A T:B // 16-BIT TACTICAL CORE");

                // Action 1: Commission Custom Combination into Hangar
                var _com_y = _gg_y + 50;
                var _com_w = _col3_w - 28;
                var _com_hov = (_mx >= _col3_x + 14 && _mx <= _col3_x + 14 + _com_w && _my >= _com_y && _my <= _com_y + 42);

                if (_com_hov && _click) {
                    if (!_is_power_stable) {
                        show_toast("ASSEMBLY REJECTED: Resolve Reactor Overload first!", c_red);
                    } else {
                        _gm.assemble_custom_mech(assembly_custom_name, assembly_head_idx, assembly_torso_idx, assembly_arms_idx, assembly_legs_idx, assembly_bp_idx, assembly_wp_idx);
                    }
                }
                scr_draw_snes_button(_col3_x + 14, _com_y, _com_w, 42, _is_power_stable ? ">> COMMISSION INTO HANGAR <<" : "[OVERLOAD - CANNOT COMMISSION]", _com_hov, false, _is_power_stable ? make_color_rgb(60, 240, 120) : make_color_rgb(180, 50, 50));

                // Action 2: Archive as Canonical Blueprint
                var _arc_y = _com_y + 48;
                var _arc_hov = (_mx >= _col3_x + 14 && _mx <= _col3_x + 14 + _com_w && _my >= _arc_y && _my <= _arc_y + 36);
                if (_arc_hov && _click) {
                    save_custom_blueprint();
                }
                scr_draw_snes_button(_col3_x + 14, _arc_y, _com_w, 36, "[★ SAVE AS PMC CANONICAL BLUEPRINT]", _arc_hov, false, make_color_rgb(255, 185, 50));

                // Action 3: Dual Navigation Shortcuts
                var _nav_y = _arc_y + 42;
                var _half_w = floor((_com_w - 8) / 2);

                var _t_hov = (_mx >= _col3_x + 14 && _mx <= _col3_x + 14 + _half_w && _my >= _nav_y && _my <= _nav_y + 30);
                if (_t_hov && _click) {
                    active_tab = 0;
                    rd_subtab = 1;
                    show_toast("TRANSFERRED TO R&D PROTOTYPING BENCH!", c_aqua);
                }
                scr_draw_snes_button(_col3_x + 14, _nav_y, _half_w, 30, "[TUNE IN LAB]", _t_hov, false, make_color_rgb(80, 180, 240));

                var _f_nav_hov = (_mx >= _col3_x + 14 + _half_w + 8 && _mx <= _col3_x + 14 + _com_w && _my >= _nav_y && _my <= _nav_y + 30);
                if (_f_nav_hov && _click) {
                    active_tab = 2;
                    contracts_subtab = 1;
                    show_toast("TRANSFERRED TO FLY-OFF PROCUREMENT ARENA!", c_aqua);
                }
                scr_draw_snes_button(_col3_x + 14 + _half_w + 8, _nav_y, _half_w, 30, "[FLY-OFF ARENA]", _f_nav_hov, false, make_color_rgb(255, 120, 180));

            } else {
                draw_set_color(c_red);
                draw_text(_col3_x + 18, _deck_y + 120, "PARTS MISSING: Must equip all 6 component slots to compute diagnostics!");
            }
        }
    }
}
else if (active_tab == 2) {
    // 3 Subtabs: Contracts & Bounties (Doc 04), Fly-Off Procurement Trials (Doc 15), Commodity Trade Exchange (Doc 15)
    var _csub_w = floor((_pan_w - 48) / 3);
    var _csub_y = _pan_y + 8;
    var _csub_names = [
        "[1. CONTRACTS & BOUNTIES]",
        "[2. PROCUREMENT FLY-OFF TRIALS]",
        "[3. COMMODITY TRADE EXCHANGE]"
    ];
    for (var cst = 0; cst < 3; cst++) {
        var _csx = _pan_x + 30 + cst * (_csub_w + 14);
        var _cst_active = (contracts_subtab == cst);
        var _cst_hov = (_mx >= _csx && _mx <= _csx + _csub_w && _my >= _csub_y && _my <= _csub_y + 30);
        if (_cst_hov && _click) { contracts_subtab = cst; scr_audio_play_ui("click"); }

        draw_set_color(_cst_active ? make_color_rgb(25, 55, 88) : (_cst_hov ? make_color_rgb(18, 38, 60) : make_color_rgb(12, 20, 32)));
        draw_rectangle(_csx, _csub_y, _csx + _csub_w, _csub_y + 30, false);
        draw_set_color(_cst_active ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 75, 110));
        draw_rectangle(_csx, _csub_y, _csx + _csub_w, _csub_y + 30, true);
        draw_set_color(_cst_active ? c_white : make_color_rgb(160, 190, 220));
        draw_text(_csx + 14, _csub_y + 7, _csub_names[cst]);
    }

    // =========================================================================
    // SUBTAB 0: STANDARD PROCUREMENT CONTRACTS & DELIVERIES (docs/04)
    // =========================================================================
    if (contracts_subtab == 0) {
        var _cb_x = _pan_x + 30;
        var _cb_y = _pan_y + 44;

        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(_cb_x, _cb_y, "== FACTION CONTRACT BOARD & DELIVERIES ==");

        // Faction Standing Meters
        if (instance_exists(obj_FactionManager)) {
            var _fm = obj_FactionManager;
            var _std_y = _cb_y + 24;
            var _f_list = ["faction_a", "faction_b", "faction_c", "faction_d", "faction_e", "faction_f"];
            var _f_box_w = 180;
            for (var f = 0; f < 6; f++) {
                var _fid = _f_list[f];
                if (!variable_struct_exists(_fm.factions, _fid)) continue;
                var _finfo = variable_struct_get(_fm.factions, _fid);
                var _std = _fm.get_standing(_fid);
                var _fx = _cb_x + f * (_f_box_w + 14);

                var _f_ai = variable_struct_get(_finfo, "ai_state") ?? "PEACE";
                var _is_desp = (_f_ai == "DESPERATE");
                var _is_win = (_f_ai == "WINNING");
                var _is_war = (_f_ai == "STANDARD_WAR");

                var _box_bg = _is_desp ? make_color_rgb(38, 14, 18) : (_is_win ? make_color_rgb(34, 30, 12) : make_color_rgb(14, 20, 28));
                var _box_brd = _is_desp ? make_color_rgb(255, 60, 60) : (_is_win ? make_color_rgb(255, 215, 80) : (_is_war ? make_color_rgb(220, 80, 80) : make_color_rgb(40, 65, 95)));

                draw_set_color(_box_bg);
                draw_rectangle(_fx, _std_y, _fx + _f_box_w, _std_y + 56, false);
                draw_set_color(_box_brd);
                draw_rectangle(_fx, _std_y, _fx + _f_box_w, _std_y + 56, true);

                var _is_dorm = (variable_struct_get(_finfo, "is_dormant") ?? false);
                var _f_disp_name = _is_dorm ? "[SECTOR 0]" : _finfo.short_name;
                draw_set_color(_is_dorm ? make_color_rgb(255, 80, 80) : make_color_rgb(240, 210, 100));
                draw_text(_fx + 8, _std_y + 6, _f_disp_name);

                // AI Brain Status Tag
                var _ai_tag = _is_dorm ? "[DORMANT]" : "[PEACE]";
                var _ai_col = _is_dorm ? make_color_rgb(255, 80, 80) : make_color_rgb(100, 220, 255);
                if (!_is_dorm) {
                    if (_is_desp) { _ai_tag = "[CRITICAL +100%]"; _ai_col = make_color_rgb(255, 60, 60); }
                    else if (_is_win) { _ai_tag = "[DOMINANT]"; _ai_col = make_color_rgb(255, 215, 80); }
                    else if (_is_war) { _ai_tag = "[WAR]"; _ai_col = make_color_rgb(255, 100, 100); }
                }

                draw_set_color(_ai_col);
                draw_text(_fx + _f_box_w - string_width(_ai_tag) - 6, _std_y + 6, _ai_tag);

                var _std_col = _is_dorm ? make_color_rgb(180, 80, 80) : ((_std > 20) ? c_lime : ((_std < -10) ? c_red : make_color_rgb(240, 200, 80)));
                draw_set_color(_std_col);
                var _std_str = _is_dorm ? "Status: CLASSIFIED" : ("Standing: " + string(_std));
                draw_text(_fx + 8, _std_y + 23, _std_str);

                draw_set_color(_is_dorm ? make_color_rgb(200, 70, 70) : (_is_desp ? make_color_rgb(255, 180, 180) : make_color_rgb(160, 190, 220)));
                var _posture_txt = _is_dorm ? "Crypt Telemetry" : (_is_desp ? "+100% Bailout Active" : (_is_win ? "Tariffs Enforced" : (_finfo.short_name + " Posture")));
                draw_text(_fx + 8, _std_y + 38, _posture_txt);
            }

            // Active vs Available Contracts
            var _c_disp_y = _std_y + 68;

            // 1. Available Contracts
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_cb_x, _c_disp_y, "AVAILABLE FACTION CONTRACT OFFERINGS:");
            for (var ac = 0; ac < array_length(_fm.available_contracts); ac++) {
                var _cnt = _fm.available_contracts[ac];
                var _cy = _c_disp_y + 24 + ac * 94;
                var _cw = 1160;

                draw_set_color(make_color_rgb(12, 18, 26));
                draw_rectangle(_cb_x, _cy, _cb_x + _cw, _cy + 84, false);
                draw_set_color(make_color_rgb(35, 60, 90));
                draw_rectangle(_cb_x, _cy, _cb_x + _cw, _cy + 84, true);

                draw_set_color(make_color_rgb(255, 215, 80));
                draw_text(_cb_x + 14, _cy + 8, _cnt.title);
                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text_ext(_cb_x + 14, _cy + 28, _cnt.briefing, 15, _cw - 180);

                draw_set_color(make_color_rgb(100, 255, 140));
                draw_text(_cb_x + 14, _cy + 62, "Payout: " + string(_cnt.payout_credits) + " Cr | Standing: +" + string(_cnt.reputation_gain) + " | Deadline: " + string(_cnt.deadline_days) + " Days");

                // Accept Button
                var _ab_x = _cb_x + _cw - 150;
                var _ab_y = _cy + 20;
                var _ab_w = 135;
                var _ab_h = 42;
                var _ab_hov = (_mx >= _ab_x && _mx <= _ab_x + _ab_w && _my >= _ab_y && _my <= _ab_y + _ab_h);
                if (_ab_hov && _click) {
                    _fm.accept_contract(_cnt.id);
                }
                draw_set_color(_ab_hov ? make_color_rgb(30, 80, 50) : make_color_rgb(18, 50, 32));
                draw_rectangle(_ab_x, _ab_y, _ab_x + _ab_w, _ab_y + _ab_h, false);
                draw_set_color(make_color_rgb(60, 240, 120));
                draw_rectangle(_ab_x, _ab_y, _ab_x + _ab_w, _ab_y + _ab_h, true);
                draw_set_color(c_white);
                draw_text(_ab_x + 22, _ab_y + 12, "[ACCEPT]");
            }

            // 2. Active Contracts Queue
            var _act_y = _c_disp_y + 360;
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_cb_x, _act_y, "ACTIVE CONTRACT COMMITMENTS (ACCEPTED):");
            if (array_length(_fm.active_contracts) == 0) {
                draw_set_color(make_color_rgb(140, 160, 180));
                draw_text(_cb_x, _act_y + 24, "No contracts currently accepted. Accept offerings above to deploy resources!");
            } else {
                for (var act = 0; act < array_length(_fm.active_contracts); act++) {
                    var _acnt = _fm.active_contracts[act];
                    var _acy = _act_y + 24 + act * 78;
                    var _acw = 1160;

                    draw_set_color(make_color_rgb(14, 22, 32));
                    draw_rectangle(_cb_x, _acy, _cb_x + _acw, _acy + 70, false);
                    draw_set_color(make_color_rgb(45, 75, 110));
                    draw_rectangle(_cb_x, _acy, _cb_x + _acw, _acy + 70, true);

                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_cb_x + 14, _acy + 8, string(_acnt.title ?? "Contract") + " [FACTION: " + string(_acnt.faction_name ?? "Independent") + "]");
                    draw_set_color(c_white);
                    draw_text(_cb_x + 14, _acy + 28, "Remaining: " + string(_acnt.days_remaining) + " Days | Payout: " + string(_acnt.payout_credits) + " Cr");

                    // Deliver / Fulfill Button
                    var _ful_x = _cb_x + _acw - 160;
                    var _ful_y = _acy + 14;
                    var _ful_w = 145;
                    var _ful_h = 42;
                    var _ful_hov = (_mx >= _ful_x && _mx <= _ful_x + _ful_w && _my >= _ful_y && _my <= _ful_y + _ful_h);
                    if (_ful_hov && _click) {
                        _fm.fulfill_contract(_acnt.id);
                    }
                    draw_set_color(_ful_hov ? make_color_rgb(35, 95, 60) : make_color_rgb(20, 60, 38));
                    draw_rectangle(_ful_x, _ful_y, _ful_x + _ful_w, _ful_y + _ful_h, false);
                    draw_set_color(make_color_rgb(80, 255, 140));
                    draw_rectangle(_ful_x, _ful_y, _ful_x + _ful_w, _ful_y + _ful_h, true);
                    draw_set_color(c_white);
                    draw_text(_ful_x + 20, _ful_y + 12, "[FULFILL ORDER]");
                }
            }
        }
    }

    // =========================================================================
    // SUBTAB 1: FLY-OFF PROCUREMENT TRIALS & DOCTRINE REPLACEMENT (docs/15)
    // =========================================================================
    else if (contracts_subtab == 1) {
        var _tr_x = _pan_x + 30;
        var _tr_y = _pan_y + 44;

        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(_tr_x, _tr_y, "== FACTION PROCUREMENT TRIALS & FLY-OFF ARENA ==");
        draw_set_color(make_color_rgb(160, 190, 220));
        draw_text(_tr_x, _tr_y + 18, "Submit custom mobile suits to competitive fly-offs to outperform incumbents, replace doctrines, and earn royalties.");

        if (instance_exists(obj_FactionManager) && instance_exists(obj_GameManager)) {
            var _fm = obj_FactionManager;
            var _gm = obj_GameManager;
            var _mpc = _fm.mass_production_contracts;
            var _f_list = ["faction_a", "faction_b", "faction_c", "faction_d", "faction_e", "faction_f"];
            var _f_card_w = 180;
            var _f_card_h = 135;

            // 1. The 6 Target Faction Cards
            for (var fc = 0; fc < 6; fc++) {
                var _fid = _f_list[fc];
                if (!variable_struct_exists(_mpc, _fid)) continue;
                var _mp = variable_struct_get(_mpc, _fid);
                var _std = _fm.get_standing(_fid);
                var _card_x = _tr_x + fc * (_f_card_w + 14);
                var _card_y = _tr_y + 40;
                var _is_sel = (trial_selected_faction == _fid);
                var _c_hov = (_mx >= _card_x && _mx <= _card_x + _f_card_w && _my >= _card_y && _my <= _card_y + _f_card_h);
                if (_c_hov && _click) {
                    trial_selected_faction = _fid;
                    trial_last_result = undefined;
                    trial_phase_results = undefined;
                    trial_phase = 0;
                }

                draw_set_color(make_color_rgb(14, 20, 28));
                draw_rectangle(_card_x, _card_y, _card_x + _f_card_w, _card_y + _f_card_h, false);
                draw_set_color(_is_sel ? make_color_rgb(255, 215, 80) : (_mp.replaced ? make_color_rgb(60, 220, 120) : make_color_rgb(45, 75, 110)));
                draw_rectangle(_card_x, _card_y, _card_x + _f_card_w, _card_y + _f_card_h, true);

                var _is_dorm = (variable_struct_get(variable_struct_get(_fm.factions, _fid), "is_dormant") ?? false);
                var _card_title = _is_dorm ? "[SECTOR 0 CRYPT]" : (variable_struct_get(_fm.factions, _fid).short_name);
                draw_set_color(_is_dorm ? make_color_rgb(255, 80, 80) : make_color_rgb(240, 215, 100));
                draw_text(_card_x + 8, _card_y + 8, _card_title);

                var _std_col = _is_dorm ? make_color_rgb(180, 80, 80) : ((_std >= 20) ? c_lime : ((_std < -10) ? c_red : c_yellow));
                draw_set_color(_std_col);
                draw_text(_card_x + 8, _card_y + 26, _is_dorm ? "Standing: ???" : ("Standing: " + string(_std)));

                if (_is_dorm) {
                    draw_set_color(make_color_rgb(255, 60, 60));
                    draw_text(_card_x + 8, _card_y + 46, "Tender: LOCKED");
                    draw_set_color(make_color_rgb(180, 180, 180));
                    draw_text(_card_x + 8, _card_y + 66, "Sub-Basalt Silo");
                    draw_text(_card_x + 8, _card_y + 84, "Sister Ark 07");
                } else if (_mp.replaced) {
                    draw_set_color(make_color_rgb(60, 240, 120));
                    draw_text(_card_x + 8, _card_y + 46, "[DOCTRINE SET]");
                    draw_set_color(make_color_rgb(100, 255, 160));
                    draw_text(_card_x + 8, _card_y + 66, "Royalty: +" + string(_mp.royalty_per_turn) + " Cr");
                    draw_text(_card_x + 8, _card_y + 84, "Earned: " + string(_mp.cumulative_royalties_paid) + " Cr");
                } else {
                    draw_set_color(make_color_rgb(240, 160, 50));
                    draw_text(_card_x + 8, _card_y + 46, "Inc: " + string_copy(_mp.baseline_suit_name, 1, 16));
                    draw_set_color(make_color_rgb(80, 220, 255));
                    draw_text(_card_x + 8, _card_y + 66, "Bounty: +" + string(_mp.licensing_bounty / 1000) + "k");
                    draw_text(_card_x + 8, _card_y + 84, "Royalty: +" + string(_mp.royalty_per_turn / 1000) + "k/t");
                }

                draw_set_color(_is_sel ? make_color_rgb(255, 215, 80) : make_color_rgb(140, 170, 200));
                draw_text(_card_x + 10, _card_y + 110, _is_sel ? ">> TARGET SELECTED <<" : "[CLICK TO SELECT]");
            }

            // 2. Candidate Selection (Left Column) vs Fly-Off Arena (Right Column)
            var _arena_y = _tr_y + 185;
            var _col1_w = 380;
            var _col2_x = _tr_x + _col1_w + 18;
            var _col2_w = 762;
            var _arena_h = 425;

            // Left Box: Hangar Mobile Suits
            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_tr_x, _arena_y, _tr_x + _col1_w, _arena_y + _arena_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_tr_x, _arena_y, _tr_x + _col1_w, _arena_y + _arena_h, true);

            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_tr_x + 12, _arena_y + 10, "HANGAR MECHS (CHOOSE CANDIDATE):");

            var _mechs = _gm.inventory.deployable_mechs;
            if (array_length(_mechs) == 0) {
                draw_set_color(make_color_rgb(160, 180, 200));
                draw_text(_tr_x + 12, _arena_y + 36, "No deployable suits in hangar! Assemble in Factory.");
            } else {
                for (var m = 0; m < min(5, array_length(_mechs)); m++) {
                    var _mitem = _mechs[m];
                    var _my_box = _arena_y + 34 + m * 76;
                    var _m_sel = (trial_selected_mech_idx == m);
                    var _m_hov = (_mx >= _tr_x + 8 && _mx <= _tr_x + _col1_w - 8 && _my >= _my_box && _my <= _my_box + 70);
                    if (_m_hov && _click) {
                        trial_selected_mech_idx = m;
                        trial_last_result = undefined;
                        trial_phase_results = undefined;
                        trial_phase = 0;
                    }

                    draw_set_color(_m_sel ? make_color_rgb(20, 50, 75) : (_m_hov ? make_color_rgb(16, 32, 48) : make_color_rgb(12, 18, 26)));
                    draw_rectangle(_tr_x + 8, _my_box, _tr_x + _col1_w - 8, _my_box + 70, false);
                    draw_set_color(_m_sel ? make_color_rgb(100, 220, 255) : make_color_rgb(40, 65, 95));
                    draw_rectangle(_tr_x + 8, _my_box, _tr_x + _col1_w - 8, _my_box + 70, true);

                    draw_set_color(_m_sel ? make_color_rgb(255, 220, 100) : c_white);
                    draw_text(_tr_x + 14, _my_box + 6, _mitem.name);
                    var _ped_badge = "UNTESTED";
                    var _ped_bonus = 0.0;
                    if (variable_struct_exists(_mitem, "combat_pedigree") && is_struct(_mitem.combat_pedigree)) {
                        _ped_badge = variable_struct_get(_mitem.combat_pedigree, "pedigree_rating") ?? "UNTESTED";
                        _ped_bonus = variable_struct_get(_mitem.combat_pedigree, "telemetry_bonus") ?? 0.0;
                    }
                    draw_set_color((_ped_bonus > 0) ? make_color_rgb(255, 215, 80) : make_color_rgb(140, 160, 180));
                    draw_text(_tr_x + 14, _my_box + 24, "Pedigree: " + _ped_badge + ((_ped_bonus > 0) ? " (+" + string(_ped_bonus) + " pts)" : "") + " | " + _mitem.status);
                    draw_set_color(make_color_rgb(80, 220, 140));
                    draw_text(_tr_x + 14, _my_box + 44, "Armor: " + string(_mitem.armor_rating) + " | Output: +" + string(_mitem.power_output) + " MW | Spd: " + string(_mitem.speed) + " | CR: " + string(_mitem.combat_rating));
                }
            }

            // Right Box: 4-Phase Fly-Off Tournament Arena & Fleet Adoption Lifecycle (docs/26)
            var _cur_mp = variable_struct_get(_mpc, trial_selected_faction);
            var _is_adopted = (!is_undefined(_cur_mp) && _cur_mp.replaced);
            var _inc = _fm.get_incumbent_specs(trial_selected_faction);
            var _cur_cand = (trial_selected_mech_idx >= 0 && trial_selected_mech_idx < array_length(_mechs)) ? _mechs[trial_selected_mech_idx] : undefined;

            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_col2_x, _arena_y, _col2_x + _col2_w, _arena_y + _arena_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_col2_x, _arena_y, _col2_x + _col2_w, _arena_y + _arena_h, true);

            // Top Header: Title + Adoption & Candidate Pool Toggles
            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_col2_x + 14, _arena_y + 10, "PROCUREMENT BUREAU: " + _inc.faction_name);
            draw_set_color(make_color_rgb(160, 190, 220));
            draw_text_ext(_col2_x + 14, _arena_y + 28, "Evaluator: " + string(_inc.evaluator) + " | Focus: " + string_copy(_inc.doctrine_focus, 1, 32), 16, _col2_w - 28);

            var _cand_btn_w = 210;
            var _cand_btn_x = _col2_x + _col2_w - _cand_btn_w - 14;
            var _cand_btn_y = _arena_y + 8;
            var _cand_btn_hov = (_mx >= _cand_btn_x && _mx <= _cand_btn_x + _cand_btn_w && _my >= _cand_btn_y && _my <= _cand_btn_y + 28);
            if (_cand_btn_hov && _click) {
                trial_view_candidates_mode = !trial_view_candidates_mode;
            }
            scr_draw_snes_button(_cand_btn_x, _cand_btn_y, _cand_btn_w, 28, trial_view_candidates_mode ? "[<< FLY-OFF ARENA]" : "[INSPECT 4 MP CANDIDATES >>]", _cand_btn_hov, trial_view_candidates_mode, make_color_rgb(255, 215, 80));

            if (_is_adopted && !trial_view_candidates_mode) {
                var _tgl_w = 170;
                var _tgl_x = _cand_btn_x - _tgl_w - 8;
                var _tgl_y = _arena_y + 8;
                var _tgl_hov = (_mx >= _tgl_x && _mx <= _tgl_x + _tgl_w && _my >= _tgl_y && _my <= _tgl_y + 28);
                if (_tgl_hov && _click) {
                    trial_view_adoption_panel = !trial_view_adoption_panel;
                }
                scr_draw_snes_button(_tgl_x, _tgl_y, _tgl_w, 28, trial_view_adoption_panel ? "[FLY-OFF ARENA]" : "[FLEET ADOPTION]", _tgl_hov, trial_view_adoption_panel, make_color_rgb(80, 220, 140));
            }

            // =========================================================================
            // VIEW C: 4-CANDIDATE MASS PRODUCTION PROCUREMENT DOSSIERS (docs/29 & docs/30)
            // =========================================================================
            if (trial_view_candidates_mode) {
                var _cp_y = _arena_y + 44;
                var _cp_h = _arena_h - 54;

                // Perspective Toggle Header Button for 4-Candidate Comparison
                var _p_tgl_x = _col2_x + _col2_w - 340;
                var _p_tgl_y = _arena_y + 8;
                var _p_tgl_w = 110;
                var _p_tgl_hov = (_mx >= _p_tgl_x && _mx <= _p_tgl_x + _p_tgl_w && _my >= _p_tgl_y && _my <= _p_tgl_y + 26);
                if (_p_tgl_hov && _click) {
                    catalog_perspective = (catalog_perspective == "front") ? "back" : "front";
                }
                var _p_tgl_lbl = (catalog_perspective == "back") ? "ISO: REAR" : "ISO: FRONT";
                scr_draw_snes_button(_p_tgl_x, _p_tgl_y, _p_tgl_w, 26, _p_tgl_lbl, _p_tgl_hov, catalog_perspective == "back", make_color_rgb(100, 220, 255));
                var _cand_pool = variable_struct_exists(_fm.mass_production_candidates, trial_selected_faction) ? variable_struct_get(_fm.mass_production_candidates, trial_selected_faction) : [];
                var _card_w = floor((_col2_w - 32) / 4);

                for (var ci = 0; ci < min(4, array_length(_cand_pool)); ci++) {
                    var _cdata = _cand_pool[ci];
                    var _cx = _col2_x + 12 + ci * (_card_w + 4);
                    var _is_incumbent = (!is_undefined(_cur_mp) && _cur_mp.baseline_suit_id == _cdata.id);
                    var _is_sel_cand = (trial_candidate_dossier_idx == ci);
                    var _chov = (_mx >= _cx && _mx <= _cx + _card_w && _my >= _cp_y && _my <= _cp_y + _cp_h);
                    if (_chov && _click) trial_candidate_dossier_idx = ci;

                    // Card Enclosure
                    draw_set_color(_is_incumbent ? make_color_rgb(24, 32, 20) : (_is_sel_cand ? make_color_rgb(18, 30, 48) : make_color_rgb(12, 18, 26)));
                    draw_rectangle(_cx, _cp_y, _cx + _card_w, _cp_y + _cp_h, false);
                    draw_set_color(_is_incumbent ? make_color_rgb(255, 215, 80) : (_is_sel_cand ? make_color_rgb(80, 200, 255) : make_color_rgb(40, 60, 85)));
                    draw_rectangle(_cx, _cp_y, _cx + _card_w, _cp_y + _cp_h, true);

                    // Candidate Badge & Title
                    if (_is_incumbent) {
                        draw_set_color(make_color_rgb(255, 215, 80));
                        draw_rectangle(_cx + 4, _cp_y + 4, _cx + _card_w - 4, _cp_y + 20, false);
                        draw_set_color(c_black);
                        draw_text(_cx + 8, _cp_y + 5, "*** RATIFIED LINE ***");
                    } else {
                        draw_set_color(make_color_rgb(45, 65, 90));
                        draw_rectangle(_cx + 4, _cp_y + 4, _cx + _card_w - 4, _cp_y + 20, false);
                        draw_set_color(make_color_rgb(180, 210, 240));
                        draw_text(_cx + 8, _cp_y + 5, "CANDIDATE " + string(ci + 1) + "/4");
                    }

                    draw_set_color(make_color_rgb(240, 240, 240));
                    draw_text(_cx + 6, _cp_y + 26, _cdata.name);
                    draw_set_color(make_color_rgb(160, 190, 220));
                    draw_text(_cx + 6, _cp_y + 42, string_copy(_cdata.doctrine, 1, 18));

                    // Animated Sprite Box (160x160 rendered at 0.52 scale across Front and Back Isometric Perspectives)
                    var _spr_cy = _cp_y + 165;
                    scr_draw_animated_mobile_suit(_cdata.id, _cx + _card_w / 2, _spr_cy, 0.52, 1, catalog_anim_state, -1, c_white, catalog_perspective);

                    // Animation Mode Buttons
                    var _an_btns = ["idle", "walk", "fire", "hit"];
                    var _ab_w = floor((_card_w - 16) / 4);
                    for (var bi = 0; bi < 4; bi++) {
                        var _ab_x = _cx + 6 + bi * (_ab_w + 1);
                        var _ab_y = _cp_y + 175;
                        var _ab_act = (catalog_anim_state == _an_btns[bi]);
                        var _ab_hov = (_mx >= _ab_x && _mx <= _ab_x + _ab_w && _my >= _ab_y && _my <= _ab_y + 18);
                        if (_ab_hov && _click) catalog_anim_state = _an_btns[bi];
                        draw_set_color(_ab_act ? make_color_rgb(100, 220, 255) : (_ab_hov ? make_color_rgb(45, 75, 105) : make_color_rgb(18, 28, 40)));
                        draw_rectangle(_ab_x, _ab_y, _ab_x + _ab_w, _ab_y + 18, false);
                        draw_set_color(_ab_act ? c_black : make_color_rgb(180, 200, 220));
                        draw_text(_ab_x + 2, _ab_y + 3, string_upper(string_copy(_an_btns[bi], 1, 3)));
                    }

                    // Specs Telemetry
                    var _sy = _cp_y + 200;
                    draw_set_color(make_color_rgb(120, 160, 200));
                    draw_text(_cx + 6, _sy, "Armor: " + string(_cdata.armor) + " HP");
                    draw_text(_cx + 6, _sy + 16, "Reactor: +" + string(_cdata.power) + " MW");
                    draw_text(_cx + 6, _sy + 32, "Speed: " + string(_cdata.speed) + " kph");
                    draw_text(_cx + 6, _sy + 48, "Combat: " + string(_cdata.combat) + " PTS");
                    draw_set_color(make_color_rgb(255, 180, 80));
                    draw_text(_cx + 6, _sy + 68, "Wpn: " + string_copy(_cdata.weapon, 1, 16));
                    draw_set_color(make_color_rgb(100, 240, 140));
                    draw_text(_cx + 6, _sy + 86, "Royalty: +" + string(_cdata.royalty) + "/t");

                    // Select as Fly-Off Target
                    var _sel_btn_y = _cp_y + _cp_h - 26;
                    var _sb_hov = (_mx >= _cx + 4 && _mx <= _cx + _card_w - 4 && _my >= _sel_btn_y && _my <= _sel_btn_y + 22);
                    if (_sb_hov && _click) {
                        _cur_mp.baseline_suit_id = _cdata.id;
                        _cur_mp.baseline_suit_name = _cdata.name;
                        _cur_mp.doctrine = _cdata.doctrine;
                        _cur_mp.signature_weapon = _cdata.weapon;
                        _cur_mp.sprite_asset = _cdata.sprite;
                        _cur_mp.req_armor = _cdata.req_armor;
                        _cur_mp.req_power = _cdata.req_power;
                        _cur_mp.licensing_bounty = _cdata.bounty;
                        _cur_mp.royalty_per_turn = _cdata.royalty;
                        trial_view_candidates_mode = false;
                    }
                    draw_set_color(_sb_hov ? make_color_rgb(40, 80, 120) : make_color_rgb(20, 35, 55));
                    draw_rectangle(_cx + 4, _sel_btn_y, _cx + _card_w - 4, _sel_btn_y + 22, false);
                    draw_set_color(_is_incumbent ? make_color_rgb(255, 215, 80) : make_color_rgb(80, 200, 255));
                    draw_rectangle(_cx + 4, _sel_btn_y, _cx + _card_w - 4, _sel_btn_y + 22, true);
                    draw_text(_cx + 8, _sel_btn_y + 4, _is_incumbent ? "[RATIFIED LINE]" : "[FLY-OFF TARGET]");
                }
            }
            // =========================================================================
            // VIEW A: FLEET ADOPTION & MODERNIZATION DASHBOARD (docs/26 Pillar II & III)
            // =========================================================================
            if (_is_adopted && trial_view_adoption_panel) {
                var _dash_y = _arena_y + 48;
                draw_set_color(make_color_rgb(14, 22, 32));
                draw_rectangle(_col2_x + 12, _dash_y, _col2_x + _col2_w - 12, _arena_y + _arena_h - 12, false);
                draw_set_color(make_color_rgb(45, 75, 110));
                draw_rectangle(_col2_x + 12, _dash_y, _col2_x + _col2_w - 12, _arena_y + _arena_h - 12, true);

                var _stg = variable_struct_get(_cur_mp, "adoption_stage") ?? "MATURE";
                var _blk = variable_struct_get(_cur_mp, "block_level") ?? 1;
                var _units = variable_struct_get(_cur_mp, "active_frontline_units") ?? 50;

                // Stamp & Header
                var _stamp_idx = (_stg == "TOOLING") ? 5 : ((_blk >= 3) ? 0 : ((_blk == 2) ? 4 : 1));
                scr_draw_snes_trial_stamp(_col2_x + 24, _dash_y + 14, _stamp_idx);

                draw_set_color(make_color_rgb(255, 220, 100));
                draw_text(_col2_x + 120, _dash_y + 12, "ADOPTED DOCTRINE: " + _cur_mp.replacement_name + " (BLOCK " + string(_blk) + ")");
                draw_set_color(make_color_rgb(160, 200, 230));
                draw_text(_col2_x + 120, _dash_y + 30, "Lifecycle Status: " + _stg + " | Base Doctrine Bonus: +" + string(_cur_mp.combat_bonus));

                // Status Cards & Progress
                if (_stg == "TOOLING") {
                    var _tool_rem = variable_struct_get(_cur_mp, "tooling_turns_remaining") ?? 2;
                    draw_set_color(make_color_rgb(255, 200, 60));
                    draw_text(_col2_x + 24, _dash_y + 56, "SHIPYARD TOOLING IN PROGRESS: " + string(_tool_rem) + " Turn(s) until first flight wing deployment.");
                    scr_draw_snes_hazard_bar(_col2_x + 24, _dash_y + 76, _col2_w - 48, 12, true);

                    // Expedite Button
                    var _exp_btn_y = _dash_y + 105;
                    var _exp_btn_w = _col2_w - 48;
                    var _exp_btn_h = 44;
                    var _exp_hov = (_mx >= _col2_x + 24 && _mx <= _col2_x + 24 + _exp_btn_w && _my >= _exp_btn_y && _my <= _exp_btn_y + _exp_btn_h);
                    if (_exp_hov && _click) {
                        _fm.expedite_adoption_tooling(trial_selected_faction);
                    }
                    scr_draw_snes_button(_col2_x + 24, _exp_btn_y, _exp_btn_w, _exp_btn_h, ">> EXPEDITE TOOLING (-40,000 Cr) // ADVANCE TIMELINE BY 1 TURN <<", _exp_hov, false, make_color_rgb(255, 200, 60));
                } else {
                    // Fleet Rollout Metrics
                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_col2_x + 24, _dash_y + 56, "Active Frontline Fleet: " + string(_units) + " / 250 Units in Combat Service");
                    scr_draw_snes_gauge(_col2_x + 24, _dash_y + 76, _col2_w - 48, 14, _units, 250, c_lime);

                    draw_set_color(make_color_rgb(180, 210, 240));
                    draw_text(_col2_x + 24, _dash_y + 100, "Turn Royalty Revenue: +" + string(_cur_mp.royalty_per_turn) + " Cr/turn   |   Cumulative Paid: +" + string(_cur_mp.cumulative_royalties_paid) + " Cr");
                    draw_text(_col2_x + 24, _dash_y + 120, "Arms Dealer Paradox: Player squad gains +15% Crit / +20% AP against this chassis.");

                    // Modernization Upgrade Cards (Block II / Block III)
                    var _upg_btn_y = _dash_y + 155;
                    var _upg_btn_w = _col2_w - 48;
                    var _upg_btn_h = 46;

                    if (_blk == 1) {
                        var _can_b2 = (_units >= 50);
                        var _b2_hov = (_can_b2 && _mx >= _col2_x + 24 && _mx <= _col2_x + 24 + _upg_btn_w && _my >= _upg_btn_y && _my <= _upg_btn_y + _upg_btn_h);
                        if (_b2_hov && _click) {
                            _fm.upgrade_adoption_block_ii(trial_selected_faction);
                        }
                        scr_draw_snes_button(_col2_x + 24, _upg_btn_y, _upg_btn_w, _upg_btn_h, ">> RATIFY BLOCK II MODERNIZATION // CLAIM +450,000 Cr BOUNTY & +25% ROYALTIES <<", _b2_hov, false, _can_b2 ? make_color_rgb(255, 215, 80) : c_dkgray);
                    } else if (_blk == 2) {
                        var _b3_hov = (_mx >= _col2_x + 24 && _mx <= _col2_x + 24 + _upg_btn_w && _my >= _upg_btn_y && _my <= _upg_btn_y + _upg_btn_h);
                        if (_b3_hov && _click) {
                            _fm.upgrade_adoption_block_iii(trial_selected_faction);
                        }
                        scr_draw_snes_button(_col2_x + 24, _upg_btn_y, _upg_btn_w, _upg_btn_h, ">> UPGRADE TO BLOCK III ACE CUSTOM // CLAIM +750,000 Cr & FREE ACE HANGAR MECH <<", _b3_hov, false, make_color_rgb(80, 240, 180));
                    } else {
                        draw_set_color(make_color_rgb(80, 255, 140));
                        draw_text(_col2_x + 24, _upg_btn_y + 14, "*** APEX PROTOCOL: BLOCK III VANGUARD STANDARD ACHIEVED // MAXIMUM REFINEMENT ***");
                    }
                }

                // Switch back button
                var _sw_btn_y = _arena_y + _arena_h - 48;
                var _sw_hov = (_mx >= _col2_x + 24 && _mx <= _col2_x + 280 && _my >= _sw_btn_y && _my <= _sw_btn_y + 32);
                if (_sw_hov && _click) {
                    trial_view_adoption_panel = false;
                }
                scr_draw_snes_button(_col2_x + 24, _sw_btn_y, 256, 32, ">> CHALLENGE WITH NEW MECH >>", _sw_hov, false, make_color_rgb(100, 200, 255));
            }
            // =========================================================================
            // VIEW B: 4-PHASE FLY-OFF TOURNAMENT ARENA (docs/26 Pillar I)
            // =========================================================================
            else {
                // 4-Phase Breadcrumb Bar Header
                var _bc_y = _arena_y + 46;
                var _bc_w = floor((_col2_w - 24) / 4);
                var _phase_names = ["[1. STATIC AUDIT]", "[2. STRESS GAUNTLET]", "[3. COMBAT FLY-OFF]", "[4. RATIFICATION]"];
                for (var ph = 0; ph < 4; ph++) {
                    var _bx = _col2_x + 12 + ph * _bc_w;
                    var _is_cur_ph = (trial_phase == (ph + 1) || (trial_phase == 0 && ph == 0));
                    var _is_past_ph = (trial_phase > (ph + 1));
                    draw_set_color(_is_cur_ph ? make_color_rgb(18, 54, 76) : (_is_past_ph ? make_color_rgb(12, 34, 20) : make_color_rgb(12, 16, 22)));
                    draw_rectangle(_bx, _bc_y, _bx + _bc_w - 4, _bc_y + 24, false);
                    draw_set_color(_is_cur_ph ? make_color_rgb(100, 240, 255) : (_is_past_ph ? c_lime : make_color_rgb(60, 80, 100)));
                    draw_rectangle(_bx, _bc_y, _bx + _bc_w - 4, _bc_y + 24, true);
                    draw_text(_bx + 6, _bc_y + 5, _phase_names[ph]);
                }

                // --- PHASE 0 & 1: STATIC VIABILITY AUDIT & MID-TRIAL REFINEMENTS ---
                if (trial_phase <= 1) {
                    var _cmp_y = _bc_y + 32;
                    draw_set_color(make_color_rgb(14, 24, 36));
                    draw_rectangle(_col2_x + 12, _cmp_y, _col2_x + _col2_w - 12, _cmp_y + 115, false);
                    draw_set_color(make_color_rgb(45, 75, 110));
                    draw_rectangle(_col2_x + 12, _cmp_y, _col2_x + _col2_w - 12, _cmp_y + 115, true);

                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_col2_x + 24, _cmp_y + 6, "METRIC");
                    draw_text(_col2_x + 240, _cmp_y + 6, "CANDIDATE: " + (!is_undefined(_cur_cand) ? _cur_cand.name : "None"));
                    var _cand_tag = (!is_undefined(_cur_mp) && variable_struct_exists(_cur_mp, "candidate_index")) ? (" [CANDIDATE " + string(_cur_mp.candidate_index + 1) + "/4]") : "";
                    draw_text(_col2_x + 500, _cmp_y + 6, "INCUMBENT: " + string(_inc.name ?? "Incumbent") + string(_cand_tag));

                    // Render Animated Preview of Incumbent Mass Production Chassis (docs/29)
                    scr_draw_animated_mobile_suit(_inc.id, _col2_x + _col2_w - 75, _cmp_y + 98, 0.65, -1, "idle");

                    var _cand_arm = !is_undefined(_cur_cand) ? _cur_cand.armor_rating : 0;
                    var _cand_pwr = !is_undefined(_cur_cand) ? _cur_cand.power_output : 0;
                    var _cand_spd = !is_undefined(_cur_cand) ? _cur_cand.speed : 0;
                    var _cand_cr = !is_undefined(_cur_cand) ? _cur_cand.combat_rating : 0;

                    var _rows = [
                        { label: "1. Armor Plating", c_val: string(_cand_arm) + " HP", i_val: string(_inc.armor) + " HP", pass: (_cand_arm >= _inc.armor) },
                        { label: "2. Reactor Surplus", c_val: "+" + string(_cand_pwr) + " MW", i_val: "+" + string(_inc.power) + " MW", pass: (_cand_pwr >= _inc.power) },
                        { label: "3. Maximum Speed", c_val: string(_cand_spd) + " kph", i_val: string(_inc.speed) + " kph", pass: (_cand_spd >= _inc.speed) },
                        { label: "4. Combat Rating", c_val: string(_cand_cr) + " PTS", i_val: string(_inc.combat_rating) + " PTS", pass: (_cand_cr >= _inc.combat_rating) }
                    ];

                    for (var r = 0; r < 4; r++) {
                        var _ry = _cmp_y + 24 + r * 22;
                        var _rw = _rows[r];
                        draw_set_color(make_color_rgb(180, 200, 220));
                        draw_text(_col2_x + 24, _ry, _rw.label);
                        draw_set_color(_rw.pass ? c_lime : make_color_rgb(240, 160, 60));
                        draw_text(_col2_x + 240, _ry, _rw.c_val);
                        draw_set_color(make_color_rgb(200, 200, 200));
                        draw_text(_col2_x + 500, _ry, _rw.i_val);
                    }

                    // Emergency Field Refinements Section (docs/26)
                    var _ref_y = _cmp_y + 125;
                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_col2_x + 14, _ref_y, "EMERGENCY FIELD REFINEMENTS (APPLY BEFORE STRESS GAUNTLET):");

                    var _ref_opts = [
                        { id: "OVERCLOCK_REACTOR", label: "+15% Core (25k)", cost: 25000 },
                        { id: "WELD_ARMOR", label: "+12% Armor (20k)", cost: 20000 },
                        { id: "TUNE_VERNIERS", label: "+15% Vernier (25k)", cost: 25000 },
                        { id: "RECALIBRATE_SENSORS", label: "+10% Sensors (30k)", cost: 30000 }
                    ];
                    var _rw_btn = floor((_col2_w - 28) / 4);
                    for (var ro = 0; ro < 4; ro++) {
                        var _opt = _ref_opts[ro];
                        var _rx = _col2_x + 14 + ro * _rw_btn;
                        var _is_on = (array_get_index(trial_refinements, _opt.id) != -1);
                        var _rhov = (_mx >= _rx && _mx <= _rx + _rw_btn - 6 && _my >= _ref_y + 20 && _my <= _ref_y + 52);
                        if (_rhov && _click) {
                            if (_is_on) {
                                var _idx_rem = array_get_index(trial_refinements, _opt.id);
                                array_delete(trial_refinements, _idx_rem, 1);
                                _gm.funds += _opt.cost;
                            } else {
                                if (_gm.funds >= _opt.cost) {
                                    _gm.funds -= _opt.cost;
                                    array_push(trial_refinements, _opt.id);
                                    show_toast("APPLIED REFINEMENT: " + _opt.id + "!", c_lime);
                                } else {
                                    show_toast("INSUFFICIENT FUNDS FOR REFINEMENT!", c_red);
                                }
                            }
                        }
                        scr_draw_snes_button(_rx, _ref_y + 20, _rw_btn - 6, 32, _opt.label, _rhov, _is_on, _is_on ? make_color_rgb(80, 240, 140) : make_color_rgb(100, 150, 190));
                    }

                    // Advance to Phase 2 Button
                    var _p2_btn_y = _ref_y + 62;
                    var _can_run = (!is_undefined(_cur_cand));
                    var _p2_hov = (_can_run && _mx >= _col2_x + 14 && _mx <= _col2_x + _col2_w - 14 && _my >= _p2_btn_y && _my <= _p2_btn_y + 40);
                    if (_p2_hov && _click) {
                        trial_phase_results = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 2, trial_refinements);
                        trial_phase = 2;
                        show_toast("PHASE 2 INITIATED: PROVING GROUNDS STRESS RIGS ACTIVATED!", c_aqua);
                    }
                    scr_draw_snes_button(_col2_x + 14, _p2_btn_y, _col2_w - 28, 40, ">> ADVANCE TO PHASE 2: PROVING GROUNDS STRESS GAUNTLET >>", _p2_hov, false, make_color_rgb(100, 220, 255));

                    // Quick Evaluate Button (Runs all 4 phases immediately)
                    var _qk_btn_y = _p2_btn_y + 46;
                    var _qk_hov = (_can_run && _mx >= _col2_x + 14 && _mx <= _col2_x + _col2_w - 14 && _my >= _qk_btn_y && _my <= _qk_btn_y + 30);
                    if (_qk_hov && _click) {
                        trial_last_result = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 4, trial_refinements);
                        trial_phase_results = trial_last_result;
                        trial_phase = 4;
                    }
                    scr_draw_snes_button(_col2_x + 14, _qk_btn_y, _col2_w - 28, 30, "[QUICK SIMULATE: RESOLVE ALL 4 PHASES INSTANTLY]", _qk_hov, false, c_gray);
                }
                // --- PHASE 2: DYNAMIC STRESS GAUNTLET ---
                else if (trial_phase == 2) {
                    // Safe guard: Ensure trial_phase_results exists and has p2_benchmarks
                    if (!is_struct(trial_phase_results) || !variable_struct_exists(trial_phase_results, "p2_benchmarks")) {
                        if (!is_undefined(_cur_cand)) {
                            trial_phase_results = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 2, trial_refinements);
                        }
                    }
                    if (!is_struct(trial_phase_results) || !variable_struct_exists(trial_phase_results, "p2_benchmarks")) {
                        trial_phase = 0;
                    } else {
                        var _p2_box_y = _bc_y + 36;
                        draw_set_color(make_color_rgb(14, 24, 36));
                        draw_rectangle(_col2_x + 12, _p2_box_y, _col2_x + _col2_w - 12, _p2_box_y + 240, false);
                        draw_set_color(make_color_rgb(45, 75, 110));
                        draw_rectangle(_col2_x + 12, _p2_box_y, _col2_x + _col2_w - 12, _p2_box_y + 240, true);

                        draw_set_color(make_color_rgb(255, 215, 80));
                        draw_text(_col2_x + 24, _p2_box_y + 12, "PHASE 2: DYNAMIC PROVING GROUNDS TELEMETRY");

                        var _bm = trial_phase_results.p2_benchmarks;
                        var _k_val = is_struct(_bm) ? (variable_struct_get(_bm, "kinetic") ?? 50) : 50;
                        var _t_val = is_struct(_bm) ? (variable_struct_get(_bm, "thermal") ?? 50) : 50;
                        var _v_val = is_struct(_bm) ? (variable_struct_get(_bm, "vernier") ?? 50) : 50;
                        var _e_val = is_struct(_bm) ? (variable_struct_get(_bm, "ecm") ?? 50) : 50;

                        var _stress_items = [
                            { label: "1. Kinetic Ballistics Impact Rig", val: _k_val },
                            { label: "2. Thermal Dissipation Plasma Burn", val: _t_val },
                            { label: "3. High-G Vacuum Vernier Stress", val: _v_val },
                            { label: "4. ECM & Avionics Pulse Chamber", val: _e_val }
                        ];

                        for (var si = 0; si < 4; si++) {
                            var _sy = _p2_box_y + 40 + si * 46;
                            var _it = _stress_items[si];
                            draw_set_color(make_color_rgb(180, 210, 240));
                            draw_text(_col2_x + 24, _sy, _it.label + " : " + string(_it.val) + " / 100 PTS");
                            scr_draw_snes_gauge(_col2_x + 24, _sy + 20, _col2_w - 48, 14, _it.val, 140, (_it.val >= 100) ? c_lime : make_color_rgb(240, 160, 40));
                        }

                        // Advance to Phase 3 Button
                        var _p3_btn_y = _p2_box_y + 252;
                        var _p3_hov = (_mx >= _col2_x + 14 && _mx <= _col2_x + _col2_w - 14 && _my >= _p3_btn_y && _my <= _p3_btn_y + 44);
                        if (_p3_hov && _click) {
                            if (!is_undefined(_cur_cand)) {
                                trial_phase_results = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 3, trial_refinements);
                                trial_phase = 3;
                                show_toast("PHASE 3 INITIATED: OPERATIONAL FLY-OFF DUEL COMMENCED!", c_aqua);
                            } else {
                                trial_phase = 0;
                            }
                        }
                        scr_draw_snes_button(_col2_x + 14, _p3_btn_y, _col2_w - 28, 44, ">> PROCEED TO PHASE 3: OPERATIONAL FLY-OFF COMBAT DUEL >>", _p3_hov, false, make_color_rgb(100, 220, 255));
                    }
                }
                // --- PHASE 3: OPERATIONAL FLY-OFF COMBAT DUEL ---
                else if (trial_phase == 3) {
                    if (!is_struct(trial_phase_results) || !variable_struct_exists(trial_phase_results, "p3_rival_corp")) {
                        if (!is_undefined(_cur_cand)) {
                            trial_phase_results = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 3, trial_refinements);
                        }
                    }
                    if (!is_struct(trial_phase_results) || !variable_struct_exists(trial_phase_results, "p3_rival_corp")) {
                        trial_phase = 0;
                    } else {
                        var _p3_box_y = _bc_y + 36;
                        draw_set_color(make_color_rgb(14, 24, 36));
                        draw_rectangle(_col2_x + 12, _p3_box_y, _col2_x + _col2_w - 12, _p3_box_y + 240, false);
                        draw_set_color(make_color_rgb(45, 75, 110));
                        draw_rectangle(_col2_x + 12, _p3_box_y, _col2_x + _col2_w - 12, _p3_box_y + 240, true);

                        draw_set_color(make_color_rgb(255, 215, 80));
                        draw_text(_col2_x + 24, _p3_box_y + 12, "PHASE 3: OPERATIONAL COMBAT FLY-OFF DUEL");

                        // Duel Rival Matchup Banner
                        var _rc = variable_struct_get(trial_phase_results, "p3_rival_corp") ?? "Valkyrie Heavy";
                        var _rs = variable_struct_get(trial_phase_results, "p3_rival_score") ?? 100;
                        var _cs = variable_struct_get(trial_phase_results, "composite_score") ?? 100;
                        var _cand_title = !is_undefined(_cur_cand) ? (variable_struct_get(_cur_cand, "name") ?? "Candidate") : "Candidate";
                        draw_set_color(make_color_rgb(100, 220, 255));
                        draw_text(_col2_x + 24, _p3_box_y + 40, "MATCHUP: " + string(_cand_title) + " (Vanguard PMC)  vs  " + string(_rc) + " Champion");

                        draw_set_color(make_color_rgb(180, 210, 240));
                        draw_text(_col2_x + 24, _p3_box_y + 68, "Rival Contractor Standard: " + string(_rs) + " PTS   |   Candidate Score: " + string(_cs) + " PTS");

                        // Combat Pedigree Showcase
                        var _ped_pts = variable_struct_get(trial_phase_results, "pedigree_bonus") ?? 0;
                        var _ped_tag = variable_struct_get(trial_phase_results, "pedigree_rating") ?? "UNTESTED";
                        draw_set_color((_ped_pts > 0) ? make_color_rgb(255, 215, 80) : make_color_rgb(140, 160, 180));
                        draw_text(_col2_x + 24, _p3_box_y + 96, "PMC Combat Telemetry: " + _ped_tag + " (+" + string(_ped_pts) + " pts from live combat sorties)");

                        // Telemetry Duel Outcome
                        var _duel_win = variable_struct_get(trial_phase_results, "p3_duel_win") ?? (_cs >= _rs);
                        draw_set_color(_duel_win ? make_color_rgb(80, 255, 140) : make_color_rgb(255, 100, 100));
                        draw_text(_col2_x + 24, _p3_box_y + 130, _duel_win ? "*** TACTICAL SUPERIORITY ACHIEVED: Candidate out-flew " + _rc + " in live trial! ***" : "!!! TACTICAL DEFICIT: Candidate was out-maneuvered by " + _rc + " entry !!!");

                        // Advance to Phase 4 Button
                        var _p4_btn_y = _p3_box_y + 252;
                        var _p4_hov = (_mx >= _col2_x + 14 && _mx <= _col2_x + _col2_w - 14 && _my >= _p4_btn_y && _my <= _p4_btn_y + 44);
                        if (_p4_hov && _click) {
                            if (!is_undefined(_cur_cand)) {
                                trial_last_result = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 4, trial_refinements);
                                trial_phase_results = trial_last_result;
                                trial_phase = 4;
                                show_toast("PHASE 4 CONCLUDED: BOARD VERDICT DELIVERED!", c_lime);
                            } else {
                                trial_phase = 0;
                            }
                        }
                        scr_draw_snes_button(_col2_x + 14, _p4_btn_y, _col2_w - 28, 44, ">> ADVANCE TO PHASE 4: PROCUREMENT BOARD FINAL VERDICT >>", _p4_hov, false, make_color_rgb(80, 255, 140));
                    }
                }
                // --- PHASE 4: FINAL BOARD VERDICT & RATIFICATION ---
                else if (trial_phase == 4) {
                    if (!is_struct(trial_last_result) || !variable_struct_exists(trial_last_result, "grade")) {
                        if (!is_undefined(_cur_cand)) {
                            trial_last_result = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 4, trial_refinements);
                            trial_phase_results = trial_last_result;
                        }
                    }
                    if (!is_struct(trial_last_result) || !variable_struct_exists(trial_last_result, "grade")) {
                        trial_phase = 0;
                    } else {
                        var _res_y = _bc_y + 36;
                        var _res_w = _col2_w - 24;
                        var _res_h = 245;
                        var _t_pass = variable_struct_get(trial_last_result, "passed") ?? false;
                        var _t_grade = variable_struct_get(trial_last_result, "grade") ?? "GRADE B";
                        var _t_arm = variable_struct_get(trial_last_result, "score_armor") ?? 100;
                        var _t_pwr = variable_struct_get(trial_last_result, "score_power") ?? 100;
                        var _t_spd = variable_struct_get(trial_last_result, "score_speed") ?? 100;
                        var _t_cbt = variable_struct_get(trial_last_result, "score_combat") ?? 100;
                        var _t_st = variable_struct_get(trial_last_result, "standing_bonus") ?? 0;
                        var _t_ped = variable_struct_get(trial_last_result, "pedigree_bonus") ?? 0;
                        var _t_comp = variable_struct_get(trial_last_result, "composite_score") ?? 100;
                        var _t_rep = variable_struct_get(trial_last_result, "report") ?? "Evaluation Complete.";

                        draw_set_color(_t_pass ? make_color_rgb(12, 36, 20) : make_color_rgb(36, 16, 16));
                        draw_rectangle(_col2_x + 12, _res_y, _col2_x + 12 + _res_w, _res_y + _res_h, false);
                        draw_set_color(_t_pass ? make_color_rgb(60, 240, 120) : make_color_rgb(240, 60, 60));
                        draw_rectangle(_col2_x + 12, _res_y, _col2_x + 12 + _res_w, _res_y + _res_h, true);

                        // Official Stamp
                        var _st_idx = (_t_grade == "GRADE S") ? 0 : ((_t_grade == "GRADE A") ? 1 : ((_t_grade == "GRADE B") ? 2 : 3));
                        scr_draw_snes_trial_stamp(_col2_x + 24, _res_y + 10, _st_idx);

                        draw_set_color(_t_pass ? make_color_rgb(255, 220, 100) : make_color_rgb(255, 100, 100));
                        draw_text(_col2_x + 120, _res_y + 14, _t_pass ? "*** BOARD VERDICT: TENDER APPROVED (" + _t_grade + ") ***" : "!!! BOARD VERDICT: CANDIDACY REJECTED (" + _t_grade + ") !!!");

                        draw_set_color(c_white);
                        draw_text(_col2_x + 24, _res_y + 44, "Stress Armor: " + string(_t_arm) + "/100  |  Reactor: " + string(_t_pwr) + "/100  |  Mobility: " + string(_t_spd) + "/100  |  Combat: " + string(_t_cbt) + "/100");
                        draw_set_color(make_color_rgb(100, 220, 255));
                        draw_text(_col2_x + 24, _res_y + 66, "Standing Bonus: +" + string(_t_st) + " pts  |  Combat Pedigree: +" + string(_t_ped) + " pts  ==>  COMPOSITE: " + string(_t_comp) + " / 100 PTS");

                        draw_set_color(_t_pass ? make_color_rgb(140, 255, 180) : make_color_rgb(255, 180, 180));
                        draw_text(_col2_x + 24, _res_y + 92, _t_rep);

                        // Ratification Action Button
                        if (_t_pass) {
                            var _rat_btn_y = _res_y + 130;
                            var _rat_btn_w = _res_w - 24;
                            var _rat_btn_h = 46;
                            var _rat_hov = (_mx >= _col2_x + 24 && _mx <= _col2_x + 24 + _rat_btn_w && _my >= _rat_btn_y && _my <= _rat_btn_y + _rat_btn_h);
                            if (_rat_hov && _click) {
                                _fm.award_procurement_contract(trial_selected_faction, _cur_cand, trial_last_result);
                                trial_phase = 0;
                                trial_view_adoption_panel = true;
                            }
                            var _bounty_val = _cur_mp.replaced ? floor(_cur_mp.licensing_bounty * 0.6) : _cur_mp.licensing_bounty;
                            scr_draw_snes_button(_col2_x + 24, _rat_btn_y, _rat_btn_w, _rat_btn_h, ">> RATIFY TENDER TREATY // CLAIM +" + string(_bounty_val) + " Cr & ENTER SHIPYARD TOOLING <<", _rat_hov, false, make_color_rgb(80, 255, 140));
                        }

                        // Reset / Return to Phase 0 Button
                        var _rst_btn_y = _res_y + 184;
                        var _rst_hov = (_mx >= _col2_x + 24 && _mx <= _col2_x + 220 && _my >= _rst_btn_y && _my <= _rst_btn_y + 32);
                        if (_rst_hov && _click) {
                            trial_phase = 0;
                            trial_last_result = undefined;
                            trial_phase_results = undefined;
                            trial_refinements = [];
                        }
                        scr_draw_snes_button(_col2_x + 24, _rst_btn_y, 196, 32, "<< RESET TO PHASE 1 <<", _rst_hov, false, c_dkgray);
                    }
                }
            }
        }
    }

    // =========================================================================
    // SUBTAB 2: INTERSTELLAR COMMODITY TRADE EXCHANGE (docs/15)
    // =========================================================================
    else if (contracts_subtab == 2) {
        var _td_x = _pan_x + 30;
        var _td_y = _pan_y + 44;

        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(_td_x, _td_y, "== INTERSTELLAR COMMODITY TRADE EXCHANGE ==");
        draw_set_color(make_color_rgb(160, 190, 220));
        draw_text(_td_x, _td_y + 18, "Exchange raw minerals, synthesized alloys, and components across faction trade hubs. Prices track standings.");

        if (instance_exists(obj_FactionManager) && instance_exists(obj_GameManager)) {
            var _fm = obj_FactionManager;
            var _gm = obj_GameManager;
            var _f_list = ["faction_a", "faction_b", "faction_c", "faction_d", "faction_e", "faction_f"];
            var _f_tab_w = 180;

            // 1. Faction Partner Tabs (6 Factions)
            for (var ft = 0; ft < 6; ft++) {
                var _fid = _f_list[ft];
                if (!variable_struct_exists(_fm.factions, _fid)) continue;
                var _finfo = variable_struct_get(_fm.factions, _fid);
                var _std = _fm.get_standing(_fid);
                var _ft_x = _td_x + ft * (_f_tab_w + 14);
                var _ft_y = _td_y + 40;
                var _ft_sel = (trade_selected_faction == _fid);
                var _ft_hov = (_mx >= _ft_x && _mx <= _ft_x + _f_tab_w && _my >= _ft_y && _my <= _ft_y + 52);
                if (_ft_hov && _click) trade_selected_faction = _fid;

                draw_set_color(_ft_sel ? make_color_rgb(25, 55, 88) : (_ft_hov ? make_color_rgb(18, 35, 55) : make_color_rgb(12, 20, 30)));
                draw_rectangle(_ft_x, _ft_y, _ft_x + _f_tab_w, _ft_y + 52, false);
                draw_set_color(_ft_sel ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 75, 110));
                draw_rectangle(_ft_x, _ft_y, _ft_x + _f_tab_w, _ft_y + 52, true);

                var _is_dorm = (variable_struct_get(_finfo, "is_dormant") ?? false);
                draw_set_color(_is_dorm ? make_color_rgb(255, 80, 80) : make_color_rgb(240, 215, 100));
                draw_text(_ft_x + 8, _ft_y + 6, _is_dorm ? "[SECTOR 0]" : _finfo.short_name);

                var _trade_status = _is_dorm ? "DORMANT CRYPT" : ((_std >= 30) ? "ALLY (-15%)" : ((_std < 0) ? "TARIFF (+25%)" : "PARITY"));
                var _ts_col = _is_dorm ? make_color_rgb(180, 80, 80) : ((_std >= 30) ? c_lime : ((_std < 0) ? c_red : c_yellow));
                draw_set_color(_ts_col);
                draw_text(_ft_x + 8, _ft_y + 26, _is_dorm ? "Classified Hub" : ("Std " + string(_std) + ": " + _trade_status));
            }

            // 2. Category Selector Buttons
            var _cat_y = _td_y + 100;
            var _cat_names = [
                "[1. RAW STRATEGIC MINERALS]",
                "[2. SYNTHESIZED ADVANCED ALLOYS]",
                "[3. MODULAR SUIT COMPONENTS]"
            ];
            var _cat_w = 378;
            for (var ct = 0; ct < 3; ct++) {
                var _cx = _td_x + ct * (_cat_w + 13);
                var _c_sel = (trade_selected_cat == ct);
                var _c_hov = (_mx >= _cx && _mx <= _cx + _cat_w && _my >= _cat_y && _my <= _cat_y + 30);
                if (_c_hov && _click) trade_selected_cat = ct;

                draw_set_color(_c_sel ? make_color_rgb(20, 50, 75) : (_c_hov ? make_color_rgb(16, 32, 48) : make_color_rgb(12, 18, 26)));
                draw_rectangle(_cx, _cat_y, _cx + _cat_w, _cat_y + 30, false);
                draw_set_color(_c_sel ? make_color_rgb(100, 220, 255) : make_color_rgb(40, 65, 95));
                draw_rectangle(_cx, _cat_y, _cx + _cat_w, _cat_y + 30, true);

                draw_set_color(_c_sel ? c_white : make_color_rgb(160, 190, 220));
                draw_text(_cx + 14, _cat_y + 7, _cat_names[ct]);
            }

            // 3. Commodity Cards Grid
            var _grid_y = _cat_y + 38;
            var _all_items = _fm.get_faction_trade_inventory(trade_selected_faction);
            var _cat_filter = (trade_selected_cat == 0 ? "minerals" : (trade_selected_cat == 1 ? "alloys" : "parts"));
            var _filtered_items = [];
            for (var it = 0; it < array_length(_all_items); it++) {
                if (_all_items[it].cat == _cat_filter) {
                    array_push(_filtered_items, _all_items[it]);
                }
            }

            for (var i = 0; i < array_length(_filtered_items); i++) {
                var _item = _filtered_items[i];
                var _iy = _grid_y + (i - trade_scroll_offset) * 86;
                var _iw = 1160;
                var _ih = 78;
                if (_iy < _grid_y - 10 || _iy > _pan_y + _pan_h - 90) continue;

                draw_set_color(make_color_rgb(12, 18, 26));
                draw_rectangle(_td_x, _iy, _td_x + _iw, _iy + _ih, false);
                draw_set_color(make_color_rgb(35, 60, 90));
                draw_rectangle(_td_x, _iy, _td_x + _iw, _iy + _ih, true);

                // Player Stock Count
                var _owned = 0;
                if (_item.cat == "minerals") {
                    _owned = _gm.get_raw_material(_item.id);
                } else if (_item.cat == "alloys") {
                    _owned = _gm.get_alloy(_item.id);
                } else if (_item.cat == "parts") {
                    var _slot_arr = variable_struct_get(_gm.inventory.parts, _item.slot) ?? [];
                    for (var p = 0; p < array_length(_slot_arr); p++) {
                        if (_slot_arr[p].id == _item.id) _owned++;
                    }
                }

                // Item Name, Description, Demand
                draw_set_color(make_color_rgb(255, 215, 80));
                draw_text(_td_x + 14, _iy + 8, _item.name);
                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text_ext(_td_x + 14, _iy + 28, _item.desc, 13, 540);
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_td_x + 14, _iy + 48, "In Inventory: " + string(_owned) + " Units  |  Demand: " + string(round(_item.demand_mult * 100)) + "% Parity");

                // Price Tags
                draw_set_color(make_color_rgb(80, 220, 255));
                draw_text(_td_x + 580, _iy + 16, "Buy Price: " + string(_item.buy_price) + " Cr");
                draw_set_color(make_color_rgb(255, 200, 80));
                draw_text(_td_x + 580, _iy + 42, "Sell Price: " + string(_item.sell_price) + " Cr");

                // Buy 1 Button
                var _b1_x = _td_x + 780;
                var _b1_y = _iy + 16;
                var _b1_w = 85;
                var _b1_h = 44;
                var _b1_hov = (_mx >= _b1_x && _mx <= _b1_x + _b1_w && _my >= _b1_y && _my <= _b1_y + _b1_h);
                if (_b1_hov && _click) _fm.execute_trade_buy(trade_selected_faction, _item, 1);

                draw_set_color(_b1_hov ? make_color_rgb(25, 75, 45) : make_color_rgb(16, 48, 30));
                draw_rectangle(_b1_x, _b1_y, _b1_x + _b1_w, _b1_y + _b1_h, false);
                draw_set_color(make_color_rgb(60, 220, 120));
                draw_rectangle(_b1_x, _b1_y, _b1_x + _b1_w, _b1_y + _b1_h, true);
                draw_set_color(c_white);
                draw_text(_b1_x + 14, _b1_y + 14, "BUY 1");

                // Buy 5 Button
                var _b5_x = _b1_x + _b1_w + 8;
                var _b5_w = 85;
                var _b5_h = 44;
                var _b5_hov = (_mx >= _b5_x && _mx <= _b5_x + _b5_w && _my >= _b1_y && _my <= _b1_y + _b5_h);
                if (_b5_hov && _click) _fm.execute_trade_buy(trade_selected_faction, _item, 5);

                draw_set_color(_b5_hov ? make_color_rgb(25, 75, 45) : make_color_rgb(16, 48, 30));
                draw_rectangle(_b5_x, _b1_y, _b5_x + _b5_w, _b1_y + _b5_h, false);
                draw_set_color(make_color_rgb(60, 220, 120));
                draw_rectangle(_b5_x, _b1_y, _b5_x + _b5_w, _b1_y + _b5_h, true);
                draw_set_color(c_white);
                draw_text(_b5_x + 14, _b1_y + 14, "BUY 5");

                // Sell 1 Button
                var _s1_x = _b5_x + _b5_w + 14;
                var _s1_w = 85;
                var _s1_h = 44;
                var _s1_hov = (_mx >= _s1_x && _mx <= _s1_x + _s1_w && _my >= _b1_y && _my <= _b1_y + _s1_h);
                if (_s1_hov && _click) _fm.execute_trade_sell(trade_selected_faction, _item, 1);

                draw_set_color(_s1_hov ? make_color_rgb(75, 55, 20) : make_color_rgb(48, 35, 14));
                draw_rectangle(_s1_x, _b1_y, _s1_x + _s1_w, _b1_y + _s1_h, false);
                draw_set_color(make_color_rgb(240, 180, 60));
                draw_rectangle(_s1_x, _b1_y, _s1_x + _s1_w, _b1_y + _s1_h, true);
                draw_set_color(c_white);
                draw_text(_s1_x + 14, _b1_y + 14, "SELL 1");

                // Sell All Button
                var _sa_x = _s1_x + _s1_w + 8;
                var _sa_w = 90;
                var _sa_h = 44;
                var _sa_hov = (_mx >= _sa_x && _mx <= _sa_x + _sa_w && _my >= _b1_y && _my <= _b1_y + _sa_h);
                if (_sa_hov && _click) {
                    if (_owned > 0) _fm.execute_trade_sell(trade_selected_faction, _item, _owned);
                }

                draw_set_color(_sa_hov ? make_color_rgb(75, 55, 20) : make_color_rgb(48, 35, 14));
                draw_rectangle(_sa_x, _b1_y, _sa_x + _sa_w, _b1_y + _sa_h, false);
                draw_set_color(make_color_rgb(240, 180, 60));
                draw_rectangle(_sa_x, _b1_y, _sa_x + _sa_w, _b1_y + _sa_h, true);
                draw_set_color(c_white);
                draw_text(_sa_x + 10, _b1_y + 14, "SELL ALL");
            }
        }
    }
}

else if (active_tab == 3) {
    var _sub_tabs_w = [
        "[1. PLANETARY & ORBITAL MAP]",
        "[2. FACTIONS & LIAISONS]",
        "[3. DIPLOMATIC WAR ROOM]",
        "[4. MECHA ERA LINEAGE (Y205-215)]",
        "[5. EXPEDITION & OVERTHROW]"
    ];
    var _wsub_w = floor((_pan_w - 48) / 5);
    var _wsub_y = _pan_y + 8;
    for (var wst = 0; wst < 5; wst++) {
        var _wstbx = _pan_x + 16 + wst * (_wsub_w + 8);
        var _wstb_active = (war_subtab == wst);
        var _wstb_hov = (_mx >= _wstbx && _mx <= _wstbx + _wsub_w && _my >= _wsub_y && _my <= _wsub_y + 28);
        if (_wstb_hov && _click) { war_subtab = wst; scr_audio_play_ui("click"); }

        draw_set_color(_wstb_active ? make_color_rgb(30, 70, 110) : (_wstb_hov ? make_color_rgb(20, 40, 60) : make_color_rgb(14, 22, 32)));
        draw_rectangle(_wstbx + _sx, _wsub_y + _sy, _wstbx + _wsub_w + _sx, _wsub_y + 28 + _sy, false);
        draw_set_color(_wstb_active ? make_color_rgb(100, 200, 255) : make_color_rgb(45, 75, 110));
        draw_rectangle(_wstbx + _sx, _wsub_y + _sy, _wstbx + _wsub_w + _sx, _wsub_y + 28 + _sy, true);
        draw_set_color(_wstb_active ? c_white : make_color_rgb(160, 190, 220));
        draw_text(_wstbx + 10 + _sx, _wsub_y + 6 + _sy, _sub_tabs_w[wst]);
    }

    // =====================================================================
    // SUBTAB 0: PLANETARY & ORBITAL TERRITORY WAR MAP (DOC 39)
    // =====================================================================
    if (war_subtab == 0) {
        var _m_x = _pan_x + 20;
        var _m_y = _pan_y + 40;

        // Top View Selector: [1. PLANETARY & ORBITAL TERRITORY CONQUEST] | [2. DEEP-SPACE MINING CONCESSIONS]
        var _v_modes = [
            "[1. PLANETARY & ORBITAL CONQUEST MAP]",
            "[2. DEEP-SPACE MINING CONCESSIONS (16 SITES)]"
        ];
        var _vm_w = 340;
        for (var vm = 0; vm < 2; vm++) {
            var _vm_x = _m_x + vm * (_vm_w + 12);
            var _vm_active = (war_map_mode == vm);
            var _vm_hov = (_mx >= _vm_x && _mx <= _vm_x + _vm_w && _my >= _m_y && _my <= _m_y + 26);
            if (_vm_hov && _click) {
                war_map_mode = vm;
                scr_audio_play_ui("click");
            }
            draw_set_color(_vm_active ? make_color_rgb(35, 75, 120) : (_vm_hov ? make_color_rgb(20, 40, 65) : make_color_rgb(12, 18, 26)));
            draw_rectangle(_vm_x, _m_y, _vm_x + _vm_w, _m_y + 26, false);
            draw_set_color(_vm_active ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 70, 100));
            draw_rectangle(_vm_x, _m_y, _vm_x + _vm_w, _m_y + 26, true);
            draw_set_color(_vm_active ? c_white : make_color_rgb(160, 185, 210));
            draw_text(_vm_x + 12, _m_y + 5, _v_modes[vm]);
        }

        // =================================================================
        // MODE 0: PLANETARY & ORBITAL TERRITORY CONQUEST MAP (DOC 39)
        // =================================================================
        if (war_map_mode == 0) {
            // Sphere Navigation Tabs: Earth, Space, Mars
            var _spheres_t = [
                "[EARTH SPHERE (10 CITADELS)]",
                "[SPACE & COLONIES (15 SECTORS)]",
                "[MARS SPHERE (8 VAULTS)]"
            ];
            var _sph_y = _m_y + 34;
            var _sph_w = 230;
            for (var sp = 0; sp < 3; sp++) {
                var _spx = _m_x + sp * (_sph_w + 10);
                var _sp_active = (territory_sphere_tab == sp);
                var _sp_hov = (_mx >= _spx && _mx <= _spx + _sph_w && _my >= _sph_y && _my <= _sph_y + 26);
                if (_sp_hov && _click) {
                    territory_sphere_tab = sp;
                    scr_audio_play_ui("tab");
                    if (sp == 0) selected_territory_id = "earth_jaburo";
                    else if (sp == 1) selected_territory_id = "space_luna2";
                    else if (sp == 2) selected_territory_id = "mars_olympus_mons";
                }
                draw_set_color(_sp_active ? make_color_rgb(40, 85, 135) : (_sp_hov ? make_color_rgb(22, 45, 70) : make_color_rgb(14, 20, 30)));
                draw_rectangle(_spx, _sph_y, _spx + _sph_w, _sph_y + 26, false);
                draw_set_color(_sp_active ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 75, 110));
                draw_rectangle(_spx, _sph_y, _spx + _sph_w, _sph_y + 26, true);
                draw_set_color(_sp_active ? c_white : make_color_rgb(160, 190, 220));
                draw_text(_spx + 12, _sph_y + 5, _spheres_t[sp]);
            }

            var _region_str = (territory_sphere_tab == 0) ? "EARTH" : ((territory_sphere_tab == 1) ? "SPACE" : "MARS");

            // --- LEFT PANEL: TACTICAL CRT RADAR (w: 690, h: 360) ---
            var _rad_x = _m_x;
            var _rad_y = _sph_y + 32;
            var _rad_w = 690;
            var _rad_h = 360;

            scr_draw_snes_panel(_rad_x, _rad_y, _rad_w, _rad_h, _region_str + " TACTICAL THEATER RADAR", make_color_rgb(60, 180, 240), true);

            var _fm = instance_exists(obj_FactionManager) ? obj_FactionManager : undefined;
            var _mars_locked = (_region_str == "MARS" && (!is_undefined(_fm) && !_fm.mars_unlocked));

            if (_mars_locked) {
                // Dramatic Red Crypt Classified Blackout
                draw_set_color(make_color_rgb(24, 10, 14));
                draw_rectangle(_rad_x + 10, _rad_y + 24, _rad_x + _rad_w - 10, _rad_y + _rad_h - 10, false);
                draw_set_color(make_color_rgb(180, 40, 50));
                draw_rectangle(_rad_x + 10, _rad_y + 24, _rad_x + _rad_w - 10, _rad_y + _rad_h - 10, true);

                // Scanline texture
                draw_set_color(make_color_rgb(40, 15, 20));
                for (var sl = _rad_y + 26; sl < _rad_y + _rad_h - 10; sl += 6) {
                    draw_line(_rad_x + 12, sl, _rad_x + _rad_w - 12, sl);
                }

                draw_set_color(make_color_rgb(255, 60, 60));
                draw_text(_rad_x + 30, _rad_y + 44, "⚠ THARSIS SENSOR BLACKOUT // PROTOCOL OMEGA ACTIVE ⚠");
                draw_set_color(c_white);
                draw_text(_rad_x + 30, _rad_y + 70, "Classification: LEVEL-5 ULTRA-RESTRICTED BY UNITED SOL INTELLIGENCE");
                draw_set_color(make_color_rgb(255, 180, 180));
                var _c_turn = instance_exists(obj_GameManager) ? obj_GameManager.current_turn : 1;
                draw_text(_rad_x + 30, _rad_y + 92, "Consensus Awakening Window: Turn 15 (Current Turn: " + string(_c_turn) + ")");
                draw_set_color(make_color_rgb(200, 160, 160));
                draw_text_ext(_rad_x + 30, _rad_y + 124, "All commercial and sovereign sensors traversing Martian orbital space report catastrophic signals scattering. Subterranean seismic spikes detected beneath Olympus Mons and Valles Marineris. Decades ago, humanity\'s First Mars Colonization Fleet vanished here. Deep cryo-foundries are cycling online under algorithmic direction of the Logic God.", 16, _rad_w - 60);

                // Test Override button
                var _ovr_x = _rad_x + 30;
                var _ovr_y = _rad_y + 260;
                var _ovr_w = 380;
                var _ovr_h = 36;
                var _ovr_hov = (_mx >= _ovr_x && _mx <= _ovr_x + _ovr_w && _my >= _ovr_y && _my <= _ovr_y + _ovr_h);
                if (_ovr_hov && _click) {
                    scr_territory_unlock_mars();
                }
                scr_draw_snes_button(_ovr_x, _ovr_y, _ovr_w, _ovr_h, ">> OVERRIDE QUARANTINE // AWAKEN MARS >>", _ovr_hov, false, make_color_rgb(255, 80, 80));
            } else {
                // Tactical Radar Display
                // Background grid lines
                draw_set_color(make_color_rgb(18, 30, 42));
                for (var gx = _rad_x + 40; gx < _rad_x + _rad_w - 20; gx += 50) {
                    draw_line(gx, _rad_y + 25, gx, _rad_y + _rad_h - 10);
                }
                for (var gy = _rad_y + 40; gy < _rad_y + _rad_h - 10; gy += 40) {
                    draw_line(_rad_x + 10, gy, _rad_x + _rad_w - 10, gy);
                }

                var _t_list = scr_territory_get_by_region(_region_str);

                // Pass 1: Connection hyperlanes
                for (var ti = 0; ti < array_length(_t_list); ti++) {
                    var _t1 = _t_list[ti];
                    var _tx1 = _rad_x + 30 + _t1.map_x;
                    var _ty1 = _rad_y + 35 + _t1.map_y;
                    for (var ci = 0; ci < array_length(_t1.connected_ids); ci++) {
                        var _t2 = scr_territory_get(_t1.connected_ids[ci]);
                        if (!is_undefined(_t2) && _t2.region == _region_str) {
                            var _tx2 = _rad_x + 30 + _t2.map_x;
                            var _ty2 = _rad_y + 35 + _t2.map_y;
                            var _is_contested = (_t1.controlling_faction != _t2.controlling_faction);
                            draw_set_color(_is_contested ? make_color_rgb(220, 60, 60) : make_color_rgb(35, 70, 95));
                            draw_set_alpha(_is_contested ? 0.8 : 0.4);
                            draw_line_width(_tx1, _ty1, _tx2, _ty2, _is_contested ? 2 : 1);
                            draw_set_alpha(1.0);
                        }
                    }
                }

                // Pass 2: Territory Nodes
                for (var ti = 0; ti < array_length(_t_list); ti++) {
                    var _t = _t_list[ti];
                    var _nx = _rad_x + 30 + _t.map_x;
                    var _ny = _rad_y + 35 + _t.map_y;
                    var _nw = 84;
                    var _nh = 32;
                    var _is_sel = (selected_territory_id == _t.id);
                    var _is_front = scr_territory_is_frontline(_t.id);
                    var _hov = (_mx >= _nx - _nw/2 && _mx <= _nx + _nw/2 && _my >= _ny - _nh/2 && _my <= _ny + _nh/2);
                    if (_hov && _click) {
                        selected_territory_id = _t.id;
                        scr_audio_play_ui("click");
                    }

                    // Faction Color
                    var _f_col = make_color_rgb(60, 140, 255);
                    if (_t.controlling_faction == "faction_b") _f_col = make_color_rgb(40, 220, 180);
                    else if (_t.controlling_faction == "faction_c") _f_col = make_color_rgb(255, 140, 40);
                    else if (_t.controlling_faction == "faction_d") _f_col = make_color_rgb(180, 90, 240);
                    else if (_t.controlling_faction == "faction_e") _f_col = make_color_rgb(120, 130, 240);
                    else if (_t.controlling_faction == "faction_f") _f_col = make_color_rgb(240, 60, 60);
                    else if (_t.controlling_faction == "pmc") _f_col = make_color_rgb(255, 215, 60);

                    // Frontline warning pulse
                    if (_is_front) {
                        var _pls = 0.5 + 0.5 * sin(current_time * 0.007);
                        draw_set_color(merge_color(c_red, c_yellow, _pls));
                        draw_rectangle(_nx - _nw/2 - 2, _ny - _nh/2 - 2, _nx + _nw/2 + 2, _ny + _nh/2 + 2, true);
                    }

                    // Node body
                    draw_set_color(_hov ? make_color_rgb(25, 40, 60) : make_color_rgb(12, 18, 26));
                    draw_rectangle(_nx - _nw/2, _ny - _nh/2, _nx + _nw/2, _ny + _nh/2, false);
                    draw_set_color(_is_sel ? c_white : _f_col);
                    draw_rectangle(_nx - _nw/2, _ny - _nh/2, _nx + _nw/2, _ny + _nh/2, true);

                    draw_set_halign(fa_center);
                    draw_set_color(_is_sel ? c_white : make_color_rgb(220, 240, 255));
                    draw_text(_nx, _ny - 12, string_copy(_t.name, 1, 10));
                    draw_set_color(_f_col);
                    draw_text(_nx, _ny + 2, "+" + string(_t.daily_materials) + "kg " + string_upper(string_copy(_t.material_type, 1, 4)));
                    draw_set_halign(fa_left);
                }
            }

            // --- RIGHT PANEL: STRATEGIC TERRITORY DOSSIER (w: 570, h: 360) ---
            var _dos_x = _rad_x + _rad_w + 14;
            var _dos_y = _rad_y;
            var _dos_w = _pan_w - (_dos_x - _pan_x) - 20;
            var _dos_h = _rad_h;

            var _cur_t = scr_territory_get(selected_territory_id);
            if (is_undefined(_cur_t)) {
                var _fallback_list = scr_territory_get_by_region(_region_str);
                if (array_length(_fallback_list) > 0) {
                    _cur_t = _fallback_list[0];
                    selected_territory_id = _cur_t.id;
                }
            }

            if (!is_undefined(_cur_t)) {
                scr_draw_snes_panel(_dos_x, _dos_y, _dos_w, _dos_h, "TACTICAL DOSSIER", make_color_rgb(100, 200, 255), true);

                draw_set_color(make_color_rgb(255, 220, 100));
                draw_text(_dos_x + 16, _dos_y + 26, _cur_t.name);
                draw_set_color(make_color_rgb(140, 175, 210));
                draw_text(_dos_x + 16, _dos_y + 42, _cur_t.region + " // " + _cur_t.subregion);

                // Controlling Faction Banner
                var _owner_name = "Independent";
                var _f_col = make_color_rgb(60, 140, 255);
                if (_cur_t.controlling_faction == "pmc") {
                    _owner_name = "PMC Sovereign Dominion (Player)";
                    _f_col = make_color_rgb(255, 215, 60);
                } else if (!is_undefined(_fm) && variable_struct_exists(_fm.factions, _cur_t.controlling_faction)) {
                    var _fentry = variable_struct_get(_fm.factions, _cur_t.controlling_faction);
                    if (!is_undefined(_fentry)) {
                        _owner_name = _fentry.name + " (" + _fentry.short_name + ")";
                    }
                    if (_cur_t.controlling_faction == "faction_b") _f_col = make_color_rgb(40, 220, 180);
                    else if (_cur_t.controlling_faction == "faction_c") _f_col = make_color_rgb(255, 140, 40);
                    else if (_cur_t.controlling_faction == "faction_d") _f_col = make_color_rgb(180, 90, 240);
                    else if (_cur_t.controlling_faction == "faction_e") _f_col = make_color_rgb(120, 130, 240);
                    else if (_cur_t.controlling_faction == "faction_f") _f_col = make_color_rgb(240, 60, 60);
                }

                draw_set_color(make_color_rgb(12, 18, 26));
                draw_rectangle(_dos_x + 16, _dos_y + 60, _dos_x + _dos_w - 16, _dos_y + 110, false);
                draw_set_color(_f_col);
                draw_rectangle(_dos_x + 16, _dos_y + 60, _dos_x + _dos_w - 16, _dos_y + 110, true);

                draw_set_color(_f_col);
                draw_text(_dos_x + 24, _dos_y + 66, "SOVEREIGN OCCUPANT: " + _owner_name);
                draw_set_color(make_color_rgb(100, 255, 140));
                draw_text(_dos_x + 24, _dos_y + 86, "Yield: +" + string(_cur_t.daily_credits) + " Cr/day  |  +" + string(_cur_t.daily_materials) + " kg " + string_upper(_cur_t.material_type) + "/day");

                // Garrison and Frontline Alert
                var _is_front = scr_territory_is_frontline(_cur_t.id);
                draw_set_color(_is_front ? make_color_rgb(255, 80, 80) : make_color_rgb(100, 200, 140));
                draw_text(_dos_x + 16, _dos_y + 118, _is_front ? "★ CONTESTED FRONTLINE BATTLEGROUND" : "SECURE REARGUARD TERRITORY");

                draw_set_color(c_white);
                draw_text(_dos_x + 16, _dos_y + 136, "Garrison Def: " + string(_cur_t.defense_rating) + "/100  |  " + _cur_t.garrison_unit);

                // Lore text
                draw_set_color(make_color_rgb(180, 205, 230));
                draw_text_ext(_dos_x + 16, _dos_y + 160, _cur_t.lore_brief, 14, _dos_w - 32);

                draw_set_color(make_color_rgb(140, 180, 220));
                draw_text_ext(_dos_x + 16, _dos_y + 244, "Strategic Value: " + _cur_t.strategic_value, 14, _dos_w - 32);

                // Action Buttons
                var _ab_y = _dos_y + 316;
                var _ab_w = _dos_w - 32;
                var _ab_h = 32;
                var _ab_hov = (_mx >= _dos_x + 16 && _mx <= _dos_x + 16 + _ab_w && _my >= _ab_y && _my <= _ab_y + _ab_h);

                if (_cur_t.controlling_faction == "pmc") {
                    if (_ab_hov && _click) {
                        scr_territory_fortify(_cur_t.id);
                    }
                    scr_draw_snes_button(_dos_x + 16, _ab_y, _ab_w, _ab_h, "[FORTIFY GARRISON (+10 DEF: 25,000 Cr)]", _ab_hov, false, make_color_rgb(80, 220, 120));
                } else {
                    if (_ab_hov && _click) {
                        scr_territory_launch_pmc_assault(_cur_t.id, selected_strike_mech, selected_strike_pilot);
                    }
                    scr_draw_snes_button(_dos_x + 16, _ab_y, _ab_w, _ab_h, ">> LAUNCH PMC EXPEDITIONARY ASSAULT >>", _ab_hov, false, make_color_rgb(255, 180, 60));
                }
            }

            // --- BOTTOM PANEL: SOL-WIDE BALANCE OF POWER & DAILY TRIBUTE (w: _pan_w - 40, h: 90) ---
            var _bot_x = _m_x;
            var _bot_y = _rad_y + _rad_h + 10;
            var _bot_w = _pan_w - 40;
            var _bot_h = 92;

            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_bot_x, _bot_y, _bot_x + _bot_w, _bot_y + _bot_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_bot_x, _bot_y, _bot_x + _bot_w, _bot_y + _bot_h, true);

            if (!is_undefined(_fm)) {
                var _tc = _fm.territory_control;
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_bot_x + 14, _bot_y + 8, "SOL-WIDE STRATEGIC TERRITORY BALANCE OF POWER (GUNDAM-STYLE SECTOR HEGEMONY):");

                // Multi-Segment Color Bar
                var _bar_x = _bot_x + 14;
                var _bar_y = _bot_y + 26;
                var _bar_w = _bot_w - 28;
                var _bar_h = 16;

                draw_set_color(make_color_rgb(20, 25, 35));
                draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_w, _bar_y + _bar_h, false);

                var _cur_bx = _bar_x;
                var _segs = [
                    { pct: _tc.terran_pct, col: make_color_rgb(60, 140, 255) },
                    { pct: _tc.colony_pct, col: make_color_rgb(40, 220, 180) },
                    { pct: _tc.syndicate_pct, col: make_color_rgb(255, 140, 40) },
                    { pct: _tc.zaibatsu_pct, col: make_color_rgb(180, 90, 240) },
                    { pct: _tc.astran_pct, col: make_color_rgb(120, 130, 240) },
                    { pct: _tc.martian_pct, col: make_color_rgb(240, 60, 60) },
                    { pct: _tc.pmc_pct, col: make_color_rgb(255, 215, 60) }
                ];
                for (var sg = 0; sg < array_length(_segs); sg++) {
                    var _sw = _bar_w * (_segs[sg].pct / 100.0);
                    if (_sw > 0) {
                        draw_set_color(_segs[sg].col);
                        draw_rectangle(_cur_bx, _bar_y, _cur_bx + _sw, _bar_y + _bar_h, false);
                        _cur_bx += _sw;
                    }
                }
                draw_set_color(make_color_rgb(60, 90, 130));
                draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_w, _bar_y + _bar_h, true);

                // Text breakdown
                draw_set_color(make_color_rgb(180, 210, 255));
                draw_text(_bot_x + 14, _bot_y + 48, "Terran: " + string(_tc.terran_pct) + "%  |  Colonies: " + string(_tc.colony_pct) + "%  |  Syndicates: " + string(_tc.syndicate_pct) + "%  |  Zaibatsu: " + string(_tc.zaibatsu_pct) + "%  |  Sidereal: " + string(_tc.astran_pct) + "%  |  Mars: " + string(_tc.martian_pct) + "%  |  PMC: " + string(_tc.pmc_pct) + "%");

                draw_set_color(make_color_rgb(255, 215, 60));
                var _pmc_trib = _tc.pmc_pct * 3500;
                draw_text(_bot_x + 14, _bot_y + 68, "PMC Logistics Yield: +" + string(_pmc_trib) + " Cr/day  |  Frontline Dispatch: " + string(_tc.last_shift_report));
            }
        }
        // =================================================================
        // MODE 1: ORIGINAL DEEP-SPACE MINING CONCESSIONS (16 SITES)
        // =================================================================
        else if (war_map_mode == 1) {

        var _m_x = _pan_x + 30;
        var _m_y = _pan_y + 42;

        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(_m_x, _m_y, "== STRATEGIC WAR MAP & RESOURCE EXTRACTION NODES ==");

        // Render Artwork: Space Sector Cartography Map
        if (sprite_exists(spr_space_sector_map)) {
            draw_sprite_ext(spr_space_sector_map, 0, _m_x + _sx, _m_y + 24 + _sy, 0.52, 0.52, 0, c_white, 0.88);
        }

        // Dynamic 4-Faction War Balance Panel
        var _wbox_y = _m_y + 330;
        var _wbox_w = 520;
        var _wbox_h = 205;
        draw_set_color(make_color_rgb(10, 16, 24));
        draw_rectangle(_m_x, _wbox_y, _m_x + _wbox_w, _wbox_y + _wbox_h, false);
        draw_set_color(make_color_rgb(35, 60, 90));
        draw_rectangle(_m_x, _wbox_y, _m_x + _wbox_w, _wbox_y + _wbox_h, true);

        if (instance_exists(obj_FactionManager)) {
            var _fm = obj_FactionManager;
            var _tc = _fm.territory_control;
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_m_x + 14, _wbox_y + 8, "INTERSTELLAR SECTOR INFLUENCE & 4-FACTION WAR BALANCE:");

            // 1. Terran Coalition (Blue)
            var _t_doc = _fm.mass_production_contracts.faction_a.replaced ? (" [" + string_copy(_fm.mass_production_contracts.faction_a.replacement_name, 1, 14) + "]") : " [GHA-07]";
            draw_set_color(make_color_rgb(180, 210, 255));
            draw_text(_m_x + 14, _wbox_y + 28, "Terran: " + string(_tc.terran_pct) + "% | Mil: " + string(_fm.factions.faction_a.military_strength_score) + _t_doc);
            draw_set_color(make_color_rgb(18, 30, 48));
            draw_rectangle(_m_x + 14, _wbox_y + 44, _m_x + 500, _wbox_y + 52, false);
            draw_set_color(make_color_rgb(60, 130, 240));
            draw_rectangle(_m_x + 14, _wbox_y + 44, _m_x + 14 + (486 * (_tc.terran_pct / 100.0)), _wbox_y + 52, false);

            // 2. Outer Colonies (Cyan)
            var _c_doc = _fm.mass_production_contracts.faction_b.replaced ? (" [" + string_copy(_fm.mass_production_contracts.faction_b.replacement_name, 1, 14) + "]") : " [AET-01]";
            draw_set_color(make_color_rgb(160, 255, 230));
            draw_text(_m_x + 14, _wbox_y + 58, "Colonies: " + string(_tc.colony_pct) + "% | Mil: " + string(_fm.factions.faction_b.military_strength_score) + _c_doc);
            draw_set_color(make_color_rgb(18, 30, 48));
            draw_rectangle(_m_x + 14, _wbox_y + 74, _m_x + 500, _wbox_y + 82, false);
            draw_set_color(make_color_rgb(40, 210, 180));
            draw_rectangle(_m_x + 14, _wbox_y + 74, _m_x + 14 + (486 * (_tc.colony_pct / 100.0)), _wbox_y + 82, false);

            // 3. Rogue Syndicates (Amber)
            var _s_doc = _fm.mass_production_contracts.faction_c.replaced ? (" [" + string_copy(_fm.mass_production_contracts.faction_c.replacement_name, 1, 14) + "]") : " [SCR-12]";
            draw_set_color(make_color_rgb(255, 180, 100));
            draw_text(_m_x + 14, _wbox_y + 88, "Syndicates: " + string(_tc.syndicate_pct) + "% | Pirate: " + string(_fm.factions.faction_c.military_strength_score) + _s_doc);
            draw_set_color(make_color_rgb(18, 30, 48));
            draw_rectangle(_m_x + 14, _wbox_y + 104, _m_x + 500, _wbox_y + 112, false);
            draw_set_color(make_color_rgb(240, 140, 40));
            draw_rectangle(_m_x + 14, _wbox_y + 104, _m_x + 14 + (486 * (_tc.syndicate_pct / 100.0)), _wbox_y + 112, false);

            // 4. Apex Zaibatsu (Purple)
            var _z_pct = variable_struct_exists(_tc, "zaibatsu_pct") ? _tc.zaibatsu_pct : 10;
            var _z_pwr = variable_struct_exists(_fm.factions, "faction_d") ? _fm.factions.faction_d.military_strength_score : 45;
            var _z_doc = _fm.mass_production_contracts.faction_d.replaced ? (" [" + string_copy(_fm.mass_production_contracts.faction_d.replacement_name, 1, 14) + "]") : " [ZAI-03]";
            draw_set_color(make_color_rgb(210, 160, 255));
            draw_text(_m_x + 14, _wbox_y + 118, "Zaibatsu: " + string(_z_pct) + "% | Cyber: " + string(_z_pwr) + _z_doc);
            draw_set_color(make_color_rgb(18, 30, 48));
            draw_rectangle(_m_x + 14, _wbox_y + 134, _m_x + 500, _wbox_y + 142, false);
            draw_set_color(make_color_rgb(180, 90, 240));
            draw_rectangle(_m_x + 14, _wbox_y + 134, _m_x + 14 + (486 * (_z_pct / 100.0)), _wbox_y + 142, false);

            // 5. PMC Sovereign Dominion (Gold / Lime - docs/12)
            var _pmc_pct = variable_struct_exists(_tc, "pmc_pct") ? _tc.pmc_pct : 0;
            var _pmc_tribute = _pmc_pct * 3500;
            draw_set_color(make_color_rgb(255, 215, 60));
            draw_text(_m_x + 14, _wbox_y + 148, "PMC Sovereign Dominion: " + string(_pmc_pct) + "% | Tribute: +" + string(_pmc_tribute) + " Cr/day");
            draw_set_color(make_color_rgb(18, 30, 48));
            draw_rectangle(_m_x + 14, _wbox_y + 164, _m_x + 500, _wbox_y + 172, false);
            draw_set_color(make_color_rgb(255, 215, 60));
            draw_rectangle(_m_x + 14, _wbox_y + 164, _m_x + 14 + (486 * (_pmc_pct / 100.0)), _wbox_y + 172, false);

            // Contested Sector Status
            draw_set_color(make_color_rgb(255, 220, 120));
            draw_text(_m_x + 14, _wbox_y + 182, "FRONTLINE: " + string(_tc.contested_sector ?? "Sector Contested"));
        }

        // Interactive Mining Node Cards on Right (docs/06, 14)
        var _nc_x = _m_x + 560;
        var _nc_y = _m_y + 10;
        var _nc_w = _pan_w - (_nc_x - _pan_x) - 24;

        if (instance_exists(obj_GameManager)) {
            var _gm = obj_GameManager;

            // Solar Sphere Filter Tabs
            var _spheres = [
                { id: "all", label: "ALL (16)" },
                { id: "Earth Sphere", label: "EARTH" },
                { id: "Martian Sphere", label: "MARS" },
                { id: "Asteroid Belt", label: "BELT" },
                { id: "Jovian Outer Sphere", label: "JUPITER" },
                { id: "Saturnian Outer Sphere", label: "SATURN" },
                { id: "Deep Solar Frontier", label: "VOID" }
            ];
            var _sph_w = 84;
            for (var sp = 0; sp < array_length(_spheres); sp++) {
                var _sph = _spheres[sp];
                var _spx = _nc_x + sp * (_sph_w + 6);
                var _sp_active = (mining_sphere_filter == _sph.id);
                var _sp_hov = (_mx >= _spx && _mx <= _spx + _sph_w && _my >= _nc_y && _my <= _nc_y + 24);
                if (_sp_hov && _click) {
                    mining_sphere_filter = _sph.id;
                    mining_scroll_offset = 0;
                }

                draw_set_color(_sp_active ? make_color_rgb(35, 75, 120) : (_sp_hov ? make_color_rgb(20, 40, 65) : make_color_rgb(12, 18, 26)));
                draw_rectangle(_spx, _nc_y, _spx + _sph_w, _nc_y + 24, false);
                draw_set_color(_sp_active ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 70, 100));
                draw_rectangle(_spx, _nc_y, _spx + _sph_w, _nc_y + 24, true);
                draw_set_color(_sp_active ? c_white : make_color_rgb(160, 180, 200));
                draw_text(_spx + 6, _nc_y + 4, _sph.label);
            }

            var _filtered_nodes = _gm.get_mining_nodes_by_sphere(mining_sphere_filter);
            var _num_nodes = array_length(_filtered_nodes);
            var _card_y_start = _nc_y + 32;
            var _card_h = 104;
            var _max_vis_nodes = 4;

            for (var n = 0; n < min(_max_vis_nodes, _num_nodes); n++) {
                var _n_idx = n + mining_scroll_offset;
                if (_n_idx >= _num_nodes) break;
                var _nd = _filtered_nodes[_n_idx];
                var _ny = _card_y_start + n * (_card_h + 8);
                var _is_active = (_nd.status == "ACTIVE_MINING");

                draw_set_color(make_color_rgb(14, 20, 30));
                draw_rectangle(_nc_x, _ny, _nc_x + _nc_w, _ny + _card_h, false);
                draw_set_color(_is_active ? make_color_rgb(80, 220, 120) : make_color_rgb(45, 75, 110));
                draw_rectangle(_nc_x, _ny, _nc_x + _nc_w, _ny + _card_h, true);

                draw_set_color(make_color_rgb(240, 210, 100));
                var _body_tag = variable_struct_exists(_nd, "celestial_body") ? (" (" + _nd.celestial_body + ")") : "";
                draw_text(_nc_x + 16, _ny + 8, _nd.name + _body_tag + " [" + (_is_active ? "ACTIVE HARVESTING" : "IDLE CONCESSION") + "]");

                // Mineral Yield Swatches & Counters
                var _res_keys = variable_struct_get_names(_nd.current_storage);
                var _storage_str = "";
                for (var rk = 0; rk < min(3, array_length(_res_keys)); rk++) {
                    var _rkname = _res_keys[rk];
                    var _ramt = variable_struct_get(_nd.current_storage, _rkname);
                    _storage_str += string_upper(_rkname) + ": " + string(_ramt) + "kg  ";
                }
                if (_storage_str == "") _storage_str = "Storage Bin Empty";

                draw_set_color(c_white);
                draw_text_ext(_nc_x + 16, _ny + 28, "Stored Ore: " + _storage_str, 13, _nc_w - 32);
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_nc_x + 16, _ny + 46, "Daily Extraction: +" + string(_nd.yield_rate_primary) + "kg Primary | Threat Risk: " + string(_nd.threat_level_pct) + "%");

                // Harvest / Extract to Storage Button
                var _hb_x = _nc_x + 16;
                var _hb_y = _ny + 68;
                var _h_hov = (_mx >= _hb_x && _mx <= _hb_x + 180 && _my >= _hb_y && _my <= _hb_y + 26);
                if (_h_hov && _click) {
                    for (var mi = 0; mi < array_length(_gm.nodes); mi++) {
                        if (_gm.nodes[mi].id == _nd.id) { _gm.extract_node_storage(mi); break; }
                    }
                    show_toast("ORE EXTRACTED FROM " + _nd.name + " INTO FLEET STORAGE!", c_lime);
                }
                draw_set_color(_h_hov ? make_color_rgb(30, 70, 50) : make_color_rgb(18, 40, 28));
                draw_rectangle(_hb_x, _hb_y, _hb_x + 180, _hb_y + 26, false);
                draw_set_color(make_color_rgb(80, 220, 120));
                draw_rectangle(_hb_x, _hb_y, _hb_x + 180, _hb_y + 26, true);
                draw_set_color(c_white);
                draw_text(_hb_x + 10, _hb_y + 5, "[EXTRACT TO CARGO]");

                // Deploy / Recall Escort Button
                var _db_x = _hb_x + 195;
                var _db_y = _hb_y;
                var _d_hov = (_mx >= _db_x && _mx <= _db_x + 180 && _my >= _db_y && _my <= _db_y + 26);
                if (_d_hov && _click) {
                    var _master_idx = 0;
                    for (var mi = 0; mi < array_length(_gm.nodes); mi++) {
                        if (_gm.nodes[mi].id == _nd.id) { _master_idx = mi; break; }
                    }
                    if (_is_active) {
                        _gm.recall_from_node(_master_idx);
                        show_toast("ESCORT RECALLED FROM " + _nd.name + "!", c_yellow);
                    } else {
                        var _dep_found = false;
                        for (var dm = 0; dm < array_length(_gm.inventory.deployable_mechs); dm++) {
                            if (_gm.inventory.deployable_mechs[dm].status == "READY") {
                                var _plt_name = (array_length(_gm.facilities.roster_pilots) > 0) ? _gm.facilities.roster_pilots[0].name : "Marcus Vance";
                                _gm.deploy_to_node(_master_idx, _gm.inventory.deployable_mechs[dm].id, _plt_name);
                                _dep_found = true;
                                show_toast("ESCORT DEPLOYED TO " + _nd.name + "!", c_lime);
                                break;
                            }
                        }
                        if (!_dep_found) show_toast("NO READY MECHS IN HANGAR TO DEPLOY!", c_red);
                    }
                }
                draw_set_color(_d_hov ? make_color_rgb(70, 50, 25) : make_color_rgb(38, 28, 14));
                draw_rectangle(_db_x, _db_y, _db_x + 180, _db_y + 26, false);
                draw_set_color(make_color_rgb(255, 180, 60));
                draw_rectangle(_db_x, _db_y, _db_x + 180, _db_y + 26, true);
                draw_set_color(c_white);
                draw_text(_db_x + 10, _db_y + 5, _is_active ? "[RECALL ESCORT]" : "[ASSIGN MECH ESCORT]");
            }

            // Paging Buttons for Solar Mining Nodes
            if (_num_nodes > _max_vis_nodes) {
                var _np_y = _card_y_start + _max_vis_nodes * (_card_h + 8) + 4;
                var _can_p_prev = (mining_scroll_offset > 0);
                var _can_p_next = (mining_scroll_offset + _max_vis_nodes < _num_nodes);

                if (_can_p_prev && _click && _mx >= _nc_x && _mx <= _nc_x + 140 && _my >= _np_y && _my <= _np_y + 24) mining_scroll_offset -= 1;
                if (_can_p_next && _click && _mx >= _nc_x + 160 && _mx <= _nc_x + 300 && _my >= _np_y && _my <= _np_y + 24) mining_scroll_offset += 1;

                draw_set_color(_can_p_prev ? make_color_rgb(30, 70, 110) : make_color_rgb(14, 20, 28));
                draw_rectangle(_nc_x, _np_y, _nc_x + 140, _np_y + 24, false);
                draw_set_color(make_color_rgb(80, 180, 255));
                draw_rectangle(_nc_x, _np_y, _nc_x + 140, _np_y + 24, true);
                draw_set_color(c_white);
                draw_text(_nc_x + 24, _np_y + 4, "[PREV NODES]");

                draw_set_color(_can_p_next ? make_color_rgb(30, 70, 110) : make_color_rgb(14, 20, 28));
                draw_rectangle(_nc_x + 160, _np_y, _nc_x + 300, _np_y + 24, false);
                draw_set_color(make_color_rgb(80, 180, 255));
                draw_rectangle(_nc_x + 160, _np_y, _nc_x + 300, _np_y + 24, true);
                draw_set_color(c_white);
                draw_text(_nc_x + 185, _np_y + 4, "[NEXT NODES]");
            }
        }
    
        }
    }
    // =====================================================================
    // SUBTAB 1: INTERSTELLAR FACTIONS & LIAISONS (DOC 04)
    // =====================================================================
    else if (war_subtab == 1) {
        var _fx_pan = _pan_x + 24;
        var _fy_pan = _pan_y + 44;
        var _fw_pan = _pan_w - 48;
        var _fh_pan = _pan_h - 56;

        // Faction Selector Buttons (4 Factions) + 100-Suit Encyclopedia Toggle
        var _f_tabs = [
            { id: "faction_terran", label: "1. TERRAN COALITION", col: make_color_rgb(60, 130, 240) },
            { id: "faction_colony", label: "2. OUTER COLONIES", col: make_color_rgb(40, 210, 180) },
            { id: "faction_syndicate", label: "3. RIM-SYNDICATES", col: make_color_rgb(240, 140, 40) },
            { id: "faction_zaibatsu", label: "4. APEX ZAIBATSU", col: make_color_rgb(180, 90, 240) },
            { id: "catalog_100", label: "5. [100-SUIT ENCYCLOPEDIA]", col: make_color_rgb(255, 215, 80) }
        ];
        var _fb_w = (_fw_pan - 48) / 5;
        for (var fti = 0; fti < 5; fti++) {
            var _ft_dat = _f_tabs[fti];
            var _fbx = _fx_pan + fti * (_fb_w + 12);
            var _fb_act = (fti == 4 ? (catalog_view_mode == 1) : (catalog_view_mode == 0 && selected_faction_dossier == _ft_dat.id));
            var _fb_hov = (_mx >= _fbx && _mx <= _fbx + _fb_w && _my >= _fy_pan && _my <= _fy_pan + 32);
            if (_fb_hov && _click) {
                if (fti == 4) {
                    catalog_view_mode = 1;
                } else {
                    catalog_view_mode = 0;
                    selected_faction_dossier = _ft_dat.id;
                }
            }

            draw_set_color(_fb_act ? make_color_rgb(24, 48, 76) : (_fb_hov ? make_color_rgb(18, 32, 50) : make_color_rgb(12, 18, 26)));
            draw_rectangle(_fbx, _fy_pan, _fbx + _fb_w, _fy_pan + 32, false);
            draw_set_color(_fb_act ? _ft_dat.col : make_color_rgb(40, 60, 80));
            draw_rectangle(_fbx, _fy_pan, _fbx + _fb_w, _fy_pan + 32, true);
            draw_set_color(_fb_act ? c_white : make_color_rgb(170, 195, 220));
            draw_text(_fbx + 8, _fy_pan + 8, _ft_dat.label);
        }

        var _d_y = _fy_pan + 44;

        // =========================================================================
        // BRANCH A: 100-SUIT MASTER UNIVERSE ENCYCLOPEDIA & LIVE ANIMATOR (DOC-30)
        // =========================================================================
        if (catalog_view_mode == 1) {
            var _enc_w = _fw_pan;
            var _enc_h = _fh_pan - 44;

            // Top Filter Toolbar
            var _flt_y = _d_y;
            var _flt_h = 32;
            draw_set_color(make_color_rgb(12, 18, 28));
            draw_rectangle(_fx_pan, _flt_y, _fx_pan + _enc_w, _flt_y + _flt_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_fx_pan, _flt_y, _fx_pan + _enc_w, _flt_y + _flt_h, true);

            // Faction Filter Buttons
            var _fac_flts = [
                { id: "ALL", label: "ALL (100)" },
                { id: "faction_a", label: "TERRAN (25)" },
                { id: "faction_b", label: "COLONIES (23)" },
                { id: "faction_c", label: "SYNDICATES (25)" },
                { id: "faction_d", label: "ZAIBATSU (23)" },
                { id: "pmc_player", label: "PMC (4)" }
            ];
            var _ff_w = 110;
            for (var ffi = 0; ffi < array_length(_fac_flts); ffi++) {
                var _ffx = _fx_pan + 8 + ffi * (_ff_w + 6);
                var _ff_act = (catalog_filter_faction == _fac_flts[ffi].id);
                var _ff_hov = (_mx >= _ffx && _mx <= _ffx + _ff_w && _my >= _flt_y + 4 && _my <= _flt_y + 28);
                if (_ff_hov && _click) {
                    catalog_filter_faction = _fac_flts[ffi].id;
                    catalog_scroll_offset = 0;
                }
                draw_set_color(_ff_act ? make_color_rgb(80, 200, 255) : (_ff_hov ? make_color_rgb(25, 45, 70) : make_color_rgb(16, 24, 36)));
                draw_rectangle(_ffx, _flt_y + 4, _ffx + _ff_w, _flt_y + 28, false);
                draw_set_color(_ff_act ? c_white : make_color_rgb(45, 75, 110));
                draw_rectangle(_ffx, _flt_y + 4, _ffx + _ff_w, _flt_y + 28, true);
                draw_set_color(_ff_act ? c_black : make_color_rgb(180, 210, 240));
                draw_text(_ffx + 6, _flt_y + 8, _fac_flts[ffi].label);
            }

            // Era Filter Buttons
            var _era_flts = [
                { id: 0, label: "ALL ERAS" },
                { id: 1, label: "ERA 1" },
                { id: 2, label: "ERA 2" },
                { id: 3, label: "ERA 3" },
                { id: 4, label: "ERA 4" }
            ];
            var _ef_w = 75;
            var _ef_start_x = _fx_pan + _enc_w - (array_length(_era_flts) * (_ef_w + 6)) - 8;
            for (var efi = 0; efi < array_length(_era_flts); efi++) {
                var _efx = _ef_start_x + efi * (_ef_w + 6);
                var _ef_act = (catalog_filter_era == _era_flts[efi].id);
                var _ef_hov = (_mx >= _efx && _mx <= _efx + _ef_w && _my >= _flt_y + 4 && _my <= _flt_y + 28);
                if (_ef_hov && _click) {
                    catalog_filter_era = _era_flts[efi].id;
                    catalog_scroll_offset = 0;
                }
                draw_set_color(_ef_act ? make_color_rgb(255, 215, 80) : (_ef_hov ? make_color_rgb(45, 40, 25) : make_color_rgb(20, 24, 30)));
                draw_rectangle(_efx, _flt_y + 4, _efx + _ef_w, _flt_y + 28, false);
                draw_set_color(_ef_act ? c_white : make_color_rgb(70, 60, 40));
                draw_rectangle(_efx, _flt_y + 4, _efx + _ef_w, _flt_y + 28, true);
                draw_set_color(_ef_act ? c_black : make_color_rgb(220, 200, 160));
                draw_text(_efx + 6, _flt_y + 8, _era_flts[efi].label);
            }

            // Build filtered list from GameManager catalog
            var _matching_suits = [];
            if (instance_exists(obj_GameManager) && is_struct(obj_GameManager.mobile_suit_catalog)) {
                var _c_keys = variable_struct_get_names(obj_GameManager.mobile_suit_catalog);
                for (var ki = 0; ki < array_length(_c_keys); ki++) {
                    var _s = variable_struct_get(obj_GameManager.mobile_suit_catalog, _c_keys[ki]);
                    if (!is_struct(_s)) continue;
                    if (catalog_filter_faction != "ALL" && (variable_struct_get(_s, "faction_id") ?? "") != catalog_filter_faction) continue;
                    if (catalog_filter_era != 0 && (variable_struct_get(_s, "era") ?? 0) != catalog_filter_era) continue;
                    array_push(_matching_suits, _s);
                }
            }

            var _body_y = _flt_y + 40;
            var _body_h = _enc_h - 40;
            var _col1_w = 400;

            // LEFT COLUMN: SUIT DIRECTORY LIST
            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_fx_pan, _body_y, _fx_pan + _col1_w, _body_y + _body_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_fx_pan, _body_y, _fx_pan + _col1_w, _body_y + _body_h, true);

            // Scroll Bar / Navigation Header
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_fx_pan + 12, _body_y + 10, "MOBILE SUIT DIRECTORY (" + string(array_length(_matching_suits)) + " MATCHES):");

            var _up_hov = (_mx >= _fx_pan + _col1_w - 70 && _mx <= _fx_pan + _col1_w - 40 && _my >= _body_y + 6 && _my <= _body_y + 26);
            if (_up_hov && _click) catalog_scroll_offset = max(0, catalog_scroll_offset - 1);
            scr_draw_snes_button(_fx_pan + _col1_w - 70, _body_y + 6, 26, 20, "^", _up_hov, false);

            var _dn_hov = (_mx >= _fx_pan + _col1_w - 36 && _mx <= _col1_w + _fx_pan - 6 && _my >= _body_y + 6 && _my <= _body_y + 26);
            if (_dn_hov && _click) catalog_scroll_offset = min(max(0, array_length(_matching_suits) - 8), catalog_scroll_offset + 1);
            scr_draw_snes_button(_fx_pan + _col1_w - 36, _body_y + 6, 26, 20, "v", _dn_hov, false);

            // Render visible suits (8 rows)
            var _row_h = 56;
            for (var ri = 0; ri < 8; ri++) {
                var _idx = catalog_scroll_offset + ri;
                if (_idx >= array_length(_matching_suits)) break;
                var _st = _matching_suits[_idx];
                var _ry = _body_y + 34 + ri * (_row_h + 4);
                var _is_cur_sel = (catalog_selected_suit_id == _st.id);
                var _r_hov = (_mx >= _fx_pan + 8 && _mx <= _fx_pan + _col1_w - 8 && _my >= _ry && _my <= _ry + _row_h);
                if (_r_hov && _click) catalog_selected_suit_id = _st.id;

                draw_set_color(_is_cur_sel ? make_color_rgb(24, 48, 76) : (_r_hov ? make_color_rgb(18, 30, 44) : make_color_rgb(14, 20, 28)));
                draw_rectangle(_fx_pan + 8, _ry, _fx_pan + _col1_w - 8, _ry + _row_h, false);
                draw_set_color(_is_cur_sel ? make_color_rgb(255, 215, 80) : make_color_rgb(35, 55, 80));
                draw_rectangle(_fx_pan + 8, _ry, _fx_pan + _col1_w - 8, _ry + _row_h, true);

                draw_set_color(_is_cur_sel ? c_white : make_color_rgb(220, 230, 240));
                draw_text(_fx_pan + 14, _ry + 6, _st.name);

                var _era_num = variable_struct_get(_st, "era") ?? 1;
                draw_set_color(make_color_rgb(140, 180, 220));
                draw_text(_fx_pan + 14, _ry + 24, "ERA " + string(_era_num) + " // " + string(variable_struct_get(_st, "chassis_class") ?? "Combat"));

                if (variable_struct_get(_st, "mass_production_line") ?? false) {
                    draw_set_color(make_color_rgb(255, 180, 50));
                    draw_text(_fx_pan + 14, _ry + 40, "[MASS-PRODUCTION LINE]");
                } else {
                    draw_set_color(make_color_rgb(100, 240, 160));
                    draw_text(_fx_pan + 14, _ry + 40, "Rating: " + string(variable_struct_get(_st, "combat") ?? 450) + " PTS | " + string(variable_struct_get(_st, "armor") ?? 2000) + " HP");
                }
            }

            // RIGHT COLUMN: LIVE CAD CHAMBER & TELEMETRY
            var _col2_x = _fx_pan + _col1_w + 16;
            var _col2_w = _enc_w - _col1_w - 16;
            var _active_suit = (instance_exists(obj_GameManager) ? obj_GameManager.get_mobile_suit(catalog_selected_suit_id) : undefined);

            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_col2_x, _body_y, _col2_x + _col2_w, _body_y + _body_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_col2_x, _body_y, _col2_x + _col2_w, _body_y + _body_h, true);

            if (!is_undefined(_active_suit)) {
                // CAD Viewport Enclosure (Top of Right Deck)
                var _cad_x = _col2_x + 12;
                var _cad_y = _body_y + 12;
                var _cad_w = _col2_w - 24;
                var _cad_h = 240;

                draw_set_color(make_color_rgb(6, 10, 16));
                draw_rectangle(_cad_x, _cad_y, _cad_x + _cad_w, _cad_y + _cad_h, false);
                draw_set_color(make_color_rgb(25, 45, 70));
                draw_rectangle(_cad_x, _cad_y, _cad_x + _cad_w, _cad_y + _cad_h, true);

                // Technical Grid Lines
                draw_set_color(make_color_rgb(14, 24, 38));
                for (var gx = _cad_x + 30; gx < _cad_x + _cad_w; gx += 40) draw_line(gx, _cad_y, gx, _cad_y + _cad_h);
                for (var gy = _cad_y + 30; gy < _cad_y + _cad_h; gy += 40) draw_line(_cad_x, gy, _cad_x + _cad_w, gy);

                draw_set_color(make_color_rgb(80, 180, 240));
                var _view_str = (catalog_perspective == "back") ? "REAR 3/4 ISOMETRIC" : "FRONT 3/4 ISOMETRIC";
                draw_text(_cad_x + 12, _cad_y + 8, "CAD TELEMETRY // CHASSIS: " + string_upper(_active_suit.name) + " [" + _view_str + "]");

                // Render Live Mobile Suit with Universal Animator Script (Front/Back Isometric)
                var _cad_cx = _cad_x + _cad_w / 2;
                var _cad_cy = _cad_y + _cad_h - 25;
                scr_draw_animated_mobile_suit(_active_suit.id, _cad_cx, _cad_cy, 1.1, catalog_facing, catalog_anim_state, -1, c_white, catalog_perspective);

                // Animation Mode Toolbar (Bottom of CAD Chamber)
                var _ctrl_btns = [
                    { id: "idle", label: "IDLE" },
                    { id: "walk", label: "STRIDE" },
                    { id: "fire", label: "FIRE WEAPON" },
                    { id: "hit", label: "HIT DEFLECT" }
                ];
                var _cb_w = 95;
                for (var cbi = 0; cbi < 4; cbi++) {
                    var _cbx = _cad_x + 12 + cbi * (_cb_w + 6);
                    var _cby = _cad_y + _cad_h - 32;
                    var _cb_act = (catalog_anim_state == _ctrl_btns[cbi].id);
                    var _cb_hov = (_mx >= _cbx && _mx <= _cbx + _cb_w && _my >= _cby && _my <= _cby + 24);
                    if (_cb_hov && _click) catalog_anim_state = _ctrl_btns[cbi].id;
                    scr_draw_snes_button(_cbx, _cby, _cb_w, 24, _ctrl_btns[cbi].label, _cb_hov, _cb_act);
                }

                // Isometric Perspective Toggle Button (Front vs Rear 3/4)
                var _persp_x = _cad_x + _cad_w - 235;
                var _persp_y = _cad_y + _cad_h - 32;
                var _persp_hov = (_mx >= _persp_x && _mx <= _persp_x + 115 && _my >= _persp_y && _my <= _persp_y + 24);
                if (_persp_hov && _click) {
                    catalog_perspective = (catalog_perspective == "front") ? "back" : "front";
                }
                var _persp_label = (catalog_perspective == "back") ? "ISO: REAR" : "ISO: FRONT";
                scr_draw_snes_button(_persp_x, _persp_y, 115, 24, _persp_label, _persp_hov, catalog_perspective == "back");

                // Flip Facing Button (Mirror Left/Right)
                var _flip_x = _cad_x + _cad_w - 110;
                var _flip_y = _cad_y + _cad_h - 32;
                var _flip_hov = (_mx >= _flip_x && _mx <= _flip_x + 98 && _my >= _flip_y && _my <= _flip_y + 24);
                if (_flip_hov && _click) catalog_facing = -catalog_facing;
                scr_draw_snes_button(_flip_x, _flip_y, 98, 24, catalog_facing == 1 ? "FACE >" : "< FACE", _flip_hov, false);

                // Specs Readout (Lower Half of Right Deck)
                var _spec_y = _cad_y + _cad_h + 14;
                draw_set_color(make_color_rgb(255, 215, 80));
                draw_text(_col2_x + 14, _spec_y, _active_suit.name + " [" + string(variable_struct_get(_active_suit, "short_name") ?? "") + "]");
                draw_set_color(make_color_rgb(160, 200, 230));
                draw_text(_col2_x + 14, _spec_y + 18, "Manufacturer: " + string(variable_struct_get(_active_suit, "manufacturer") ?? "Classified") + " | Doctrine: " + string(variable_struct_get(_active_suit, "doctrine") ?? "Tactical"));

                // 4 Telemetry Gauges
                var _stat_rows = [
                    { label: "Armor Integrity", val: variable_struct_get(_active_suit, "armor") ?? 2000, max_v: 5500, unit: " HP", col: c_lime },
                    { label: "Reactor Power", val: variable_struct_get(_active_suit, "power") ?? 14, max_v: 30, unit: " MW", col: make_color_rgb(80, 220, 255) },
                    { label: "Max Speed", val: variable_struct_get(_active_suit, "speed") ?? 65, max_v: 120, unit: " kph", col: make_color_rgb(255, 180, 50) },
                    { label: "Combat Rating", val: variable_struct_get(_active_suit, "combat") ?? 500, max_v: 900, unit: " PTS", col: make_color_rgb(220, 100, 255) }
                ];
                for (var si = 0; si < 4; si++) {
                    var _sr = _stat_rows[si];
                    var _sry = _spec_y + 42 + si * 22;
                    draw_set_color(make_color_rgb(180, 200, 220));
                    draw_text(_col2_x + 14, _sry, _sr.label + ":");
                    draw_set_color(_sr.col);
                    draw_text(_col2_x + 140, _sry, string(_sr.val) + string(_sr.unit ?? ""));
                    scr_draw_snes_gauge(_col2_x + 230, _sry + 2, 240, 10, _sr.val, _sr.max_v, _sr.col);
                }

                // Armament & Alloy
                var _eq_y = _spec_y + 135;
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_col2_x + 14, _eq_y, "PRIMARY WEAPON: " + string(variable_struct_get(_active_suit, "primary_weapon") ?? "None"));
                draw_text(_col2_x + 14, _eq_y + 18, "SECONDARY: " + string(variable_struct_get(_active_suit, "secondary_weapon") ?? "None"));
                draw_text(_col2_x + 14, _eq_y + 36, "FEATURE: " + string(variable_struct_get(_active_suit, "signature_feature") ?? "Standard"));
                draw_set_color(make_color_rgb(240, 210, 80));
                draw_text(_col2_x + 14, _eq_y + 54, "ALLOY MATRIX: " + string(variable_struct_get(_active_suit, "alloy_type") ?? "Standard"));

                // Historical Lore Dossier
                var _lore_y = _eq_y + 76;
                draw_set_color(make_color_rgb(12, 18, 28));
                draw_rectangle(_col2_x + 12, _lore_y, _col2_x + _col2_w - 12, _body_y + _body_h - 12, false);
                draw_set_color(make_color_rgb(35, 55, 80));
                draw_rectangle(_col2_x + 12, _lore_y, _col2_x + _col2_w - 12, _body_y + _body_h - 12, true);
                draw_set_color(make_color_rgb(200, 220, 240));
                draw_text_ext(_col2_x + 18, _lore_y + 8, string(variable_struct_get(_active_suit, "lore") ?? "No classified records available."), 16, _col2_w - 36);
            }
        }
        // =========================================================================
        // BRANCH B: FACTION DOSSIERS & STRATEGIC CITADELS (STANDARD VIEW)
        // =========================================================================
        else {
            // Left Card: Faction Standing & Military Mech Representative
            var _col1_w = 340;
        draw_set_color(make_color_rgb(10, 16, 24));
        draw_rectangle(_fx_pan, _d_y, _fx_pan + _col1_w, _d_y + _fh_pan - 44, false);
        draw_set_color(make_color_rgb(35, 60, 90));
        draw_rectangle(_fx_pan, _d_y, _fx_pan + _col1_w, _d_y + _fh_pan - 44, true);

        // Faction Standing Info
        var _fid_curr = (selected_faction_dossier == "faction_terran") ? "faction_a" : ((selected_faction_dossier == "faction_colony") ? "faction_b" : ((selected_faction_dossier == "faction_syndicate") ? "faction_c" : "faction_d"));
        var _curr_std = 0;
        var _curr_title = "Neutral";
        if (instance_exists(obj_FactionManager)) {
            _curr_std = obj_FactionManager.get_standing(_fid_curr);
            if (variable_struct_exists(obj_FactionManager.factions, _fid_curr)) {
                _curr_title = variable_struct_get(obj_FactionManager.factions, _fid_curr).standing_title;
            }
        }

        draw_set_color(make_color_rgb(240, 210, 100));
        draw_text(_fx_pan + 16, _d_y + 14, "PMC REPUTATION & STANDING:");
        draw_set_color((_curr_std > 20) ? c_lime : ((_curr_std < -10) ? c_red : make_color_rgb(240, 200, 80)));
        draw_text(_fx_pan + 16, _d_y + 34, "Standing: " + string(_curr_std) + " / 100 [" + _curr_title + "]");

        // Standing Meter Bar
        draw_set_color(make_color_rgb(20, 30, 44));
        draw_rectangle(_fx_pan + 16, _d_y + 56, _fx_pan + _col1_w - 16, _d_y + 70, false);
        var _norm_std = clamp((_curr_std + 100.0) / 200.0, 0, 1);
        draw_set_color((_curr_std > 20) ? c_lime : ((_curr_std < -10) ? c_red : make_color_rgb(240, 200, 80)));
        draw_rectangle(_fx_pan + 16, _d_y + 56, _fx_pan + 16 + ((_col1_w - 32) * _norm_std), _d_y + 70, false);
        draw_set_color(c_white);
        draw_rectangle(_fx_pan + 16, _d_y + 56, _fx_pan + _col1_w - 16, _d_y + 70, true);

        // Standing Mobile Suit Artwork & Active Playthrough Mass-Production Line (docs/29 & docs/30)
        var _active_mp_id = "ms_terran_ironclad_07";
        var _active_mp_name = "GHA-07 Ironclad";
        if (instance_exists(obj_FactionManager) && variable_struct_exists(obj_FactionManager.mass_production_contracts, _fid_curr)) {
            var _active_cnt = variable_struct_get(obj_FactionManager.mass_production_contracts, _fid_curr);
            _active_mp_id = _active_cnt.baseline_suit_id;
            _active_mp_name = _active_cnt.baseline_suit_name;
        }

        draw_set_color(make_color_rgb(255, 215, 80));
        draw_text(_fx_pan + 16, _d_y + 80, "[ACTIVE LINE: " + _active_mp_name + "]");

        // Render animated 160x160 active mass production suit with thruster pulse and idle breathing
        scr_draw_animated_mobile_suit(_active_mp_id, _fx_pan + _col1_w / 2, _d_y + 360, 0.90, 1, "idle");

        // Right Deck: Dossier, Leadership & Recruitable Aces
        var _col2_x = _fx_pan + _col1_w + 20;
        var _col2_w = _fw_pan - _col1_w - 20;
        draw_set_color(make_color_rgb(10, 16, 24));
        draw_rectangle(_col2_x, _d_y, _col2_x + _col2_w, _d_y + _fh_pan - 44, false);
        draw_set_color(make_color_rgb(35, 60, 90));
        draw_rectangle(_col2_x, _d_y, _col2_x + _col2_w, _d_y + _fh_pan - 44, true);

        // Faction Dossier Content
        if (selected_faction_dossier == "faction_terran") {
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_col2_x + 20, _d_y + 14, "THE TERRAN COALITION // UNITED EARTH DEFENSE ASSEMBLY");
            draw_set_color(make_color_rgb(180, 210, 240));
            draw_text_ext(_col2_x + 20, _d_y + 36, "Doctrine: Overwhelming kinetic artillery, heavy composite armor, and mass assembly lines. Bureaucratic state capitalism treating pilots as expendable ordnance.", 20, _col2_w - 40);

            // Major Leader Card
            var _l_y = _d_y + 86;
            scr_draw_composite_portrait("char_vance", _col2_x + 20, _l_y, 72, true, "stoic");
            draw_set_color(make_color_rgb(240, 210, 100));
            draw_text(_col2_x + 120, _l_y, "GENERAL DEBORAH VANCE // SUPREME LOGISTICS DIRECTOR");
            draw_set_color(c_white);
            draw_text_ext(_col2_x + 120, _l_y + 22, "'A mobile suit is not a weapon of glory, Commander. It is a four-million-credit piece of hydraulic machinery designed to outlast the infantryman inside it. Keep the assembly line moving.'", 18, _col2_w - 140);

            // Recruitable Ace 1: Marcus Cole
            var _a1_y = _l_y + 115;
            scr_draw_composite_portrait("plt_terran_01", _col2_x + 20, _a1_y, 72, true, "stoic");
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_col2_x + 120, _a1_y, "LT. MARCUS 'BREAKER' COLE [RECRUITABLE HEAVY ACE]");
            draw_set_color(c_white);
            draw_text(_col2_x + 120, _a1_y + 20, "Acc: 78% | Ref: 42% | Morale: 95% | Trait: Heavy (+20% Kinetic)");
            draw_text_ext(_col2_x + 120, _a1_y + 38, "Trench veteran cashiered for refusing orders to shell a civilian hydroponics dome. Stoic fortress pilot.", 18, _col2_w - 280);

            var _hb1_x = _col2_x + _col2_w - 160;
            var _hb1_y = _a1_y + 15;
            var _h1_hov = (_mx >= _hb1_x && _mx <= _hb1_x + 140 && _my >= _hb1_y && _my <= _hb1_y + 36);
            if (_h1_hov && _click && instance_exists(obj_GameManager)) {
                if (obj_GameManager.spend_funds(45000)) {
                    array_push(obj_GameManager.facilities.roster_pilots, {
                        id: "plt_terran_cole", character_id: "pilot_terran_cole", name: "Lt. Marcus Cole", callsign: "BREAKER", combat_stat: 8, tactics_stat: 4, accuracy: 78, reflexes: 42, morale: 95, salary_daily: 250, is_deployed: false, status: "ACTIVE", recovery_days: 0, recovery_days_left: 0, kills: 4, sorties: 6
                    });
                    show_toast("MARCUS 'BREAKER' COLE HIRED TO PMC ROSTER!", c_lime);
                } else show_toast("INSUFFICIENT FUNDS! (Requires 45,000 Cr)", c_red);
            }
            draw_set_color(_h1_hov ? make_color_rgb(30, 80, 50) : make_color_rgb(18, 45, 28));
            draw_rectangle(_hb1_x, _hb1_y, _hb1_x + 140, _hb1_y + 36, false);
            draw_set_color(make_color_rgb(80, 220, 120));
            draw_rectangle(_hb1_x, _hb1_y, _hb1_x + 140, _hb1_y + 36, true);
            draw_set_color(c_white);
            draw_text(_hb1_x + 14, _hb1_y + 10, "[HIRE: 45,000 Cr]");

            // Recruitable Ace 2: Elena Rostova
            var _a2_y = _a1_y + 95;
            scr_draw_composite_portrait("plt_terran_02", _col2_x + 20, _a2_y, 72, true, "neutral");
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_col2_x + 120, _a2_y, "ENSIGN ELENA ROSTOVA [RECRUITABLE SNIPER]");
            draw_set_color(c_white);
            draw_text(_col2_x + 120, _a2_y + 20, "Acc: 92% | Ref: 55% | Morale: 65% | Trait: Retinal (+15% Crit)");
            draw_text_ext(_col2_x + 120, _a2_y + 38, "Precision marksman who deserted after whistleblowing corporate sensor falsifications.", 18, _col2_w - 280);

            var _hb2_x = _col2_x + _col2_w - 160;
            var _hb2_y = _a2_y + 15;
            var _h2_hov = (_mx >= _hb2_x && _mx <= _hb2_x + 140 && _my >= _hb2_y && _my <= _hb2_y + 36);
            if (_h2_hov && _click && instance_exists(obj_GameManager)) {
                if (obj_GameManager.spend_funds(38000)) {
                    array_push(obj_GameManager.facilities.roster_pilots, {
                        id: "plt_terran_02", character_id: "pilot_terran_rostova", name: "Ensign Elena Rostova", callsign: "DEAD-EYE", combat_stat: 9, tactics_stat: 6, accuracy: 92, reflexes: 55, morale: 80, salary_daily: 220, is_deployed: false, status: "ACTIVE", recovery_days: 0, recovery_days_left: 0, kills: 2, sorties: 3
                    });
                    show_toast("ELENA ROSTOVA HIRED TO PMC ROSTER!", c_lime);
                } else show_toast("INSUFFICIENT FUNDS! (Requires 38,000 Cr)", c_red);
            }
            draw_set_color(_h2_hov ? make_color_rgb(30, 80, 50) : make_color_rgb(18, 45, 28));
            draw_rectangle(_hb2_x, _hb2_y, _hb2_x + 140, _hb2_y + 36, false);
            draw_set_color(make_color_rgb(80, 220, 120));
            draw_rectangle(_hb2_x, _hb2_y, _hb2_x + 140, _hb2_y + 36, true);
            draw_set_color(c_white);
            draw_text(_hb2_x + 14, _hb2_y + 10, "[HIRE: 38,000 Cr]");

            // Strategic Bases & Citadels Readout (docs/11)
            var _by = _d_y + 365;
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_col2_x + 20, _by, "MAJOR STRATEGIC STRONGHOLDS (EARTH & SPACE):");
            draw_set_color(make_color_rgb(180, 215, 245));
            draw_text(_col2_x + 20, _by + 18, "• [EARTH] Fortress Baikal (Siberia) - Subterranean Foundry (40% GHA-07 production, tungsten casting)");
            draw_text(_col2_x + 20, _by + 34, "• [EARTH] Mt. Kenya Sky-Anchor - Mass-driver gantry firing trans-atmospheric dropships into orbit");
            draw_text(_col2_x + 20, _by + 50, "• [SPACE] Luna Fortress Archimedes (Moon) - Primary naval bastion, drydocks, TCX-11 railgun batteries");
            draw_text(_col2_x + 20, _by + 66, "• [SPACE] Citadel Gibraltar (L1 Point) - Orbital staging station inspecting commercial ore freighters");
        }
        else if (selected_faction_dossier == "faction_colony") {
            draw_set_color(make_color_rgb(40, 210, 180));
            draw_text(_col2_x + 20, _d_y + 14, "THE OUTER COLONY LEAGUE // JOVIAN LIBERATION COMPACT");
            draw_set_color(make_color_rgb(180, 210, 240));
            draw_text_ext(_col2_x + 20, _d_y + 36, "Doctrine: High agility vernier thrust, directed-energy beam weapons, and electronic jamming. Revolutionary spacenoid communal defense bypassing heavy armor.", 20, _col2_w - 40);

            var _l_y = _d_y + 86;
            scr_draw_composite_portrait("char_vane", _col2_x + 20, _l_y, 72, true, "stoic");
            draw_set_color(make_color_rgb(240, 210, 100));
            draw_text(_col2_x + 120, _l_y, "FLEET COMMANDER CASSIAN VANE // LIBERATION FLOTILLA");
            draw_set_color(c_white);
            draw_text_ext(_col2_x + 120, _l_y + 22, "'Earth treats our people as indentured ore-miners while breathing the oxygen our solar scrubbers produce. Every beam rifle we forge is an invoice for two centuries of colonial tribute.'", 18, _col2_w - 140);

            var _a1_y = _l_y + 115;
            scr_draw_composite_portrait("plt_colony_01", _col2_x + 20, _a1_y, 72, true, "stoic");
            draw_set_color(make_color_rgb(40, 210, 180));
            draw_text(_col2_x + 120, _a1_y, "SORREN 'GHOST' LIN [RECRUITABLE INTERCEPTOR ACE]");
            draw_set_color(c_white);
            draw_text(_col2_x + 120, _a1_y + 20, "Accuracy: 85% | Reflexes: 92% | Bravery: 75% | Trait: Vernier Ace (+25% Evasion on Boost)");
            draw_text_ext(_col2_x + 120, _a1_y + 38, "Legendary vacuum skirmisher who slips through radar nets without tripping proximity alarms.", 18, _col2_w - 280);

            var _hb1_x = _col2_x + _col2_w - 160;
            var _hb1_y = _a1_y + 15;
            var _h1_hov = (_mx >= _hb1_x && _mx <= _hb1_x + 140 && _my >= _hb1_y && _my <= _hb1_y + 36);
            if (_h1_hov && _click && instance_exists(obj_GameManager)) {
                if (obj_GameManager.spend_funds(52000)) {
                    array_push(obj_GameManager.facilities.roster_pilots, {
                        id: "plt_colony_01", character_id: "pilot_colony_sorren", name: "Sorren Lin", callsign: "GHOST", combat_stat: 9, tactics_stat: 9, accuracy: 85, reflexes: 92, morale: 85, salary_daily: 280, is_deployed: false, status: "ACTIVE", recovery_days: 0, recovery_days_left: 0, kills: 5, sorties: 7
                    });
                    show_toast("SORREN 'GHOST' LIN HIRED TO PMC ROSTER!", c_lime);
                } else show_toast("INSUFFICIENT FUNDS! (Requires 52,000 Cr)", c_red);
            }
            draw_set_color(_h1_hov ? make_color_rgb(30, 80, 50) : make_color_rgb(18, 45, 28));
            draw_rectangle(_hb1_x, _hb1_y, _hb1_x + 140, _hb1_y + 36, false);
            draw_set_color(make_color_rgb(80, 220, 120));
            draw_rectangle(_hb1_x, _hb1_y, _hb1_x + 140, _hb1_y + 36, true);
            draw_set_color(c_white);
            draw_text(_hb1_x + 14, _hb1_y + 10, "[HIRE: 52,000 Cr]");

            var _a2_y = _a1_y + 95;
            scr_draw_composite_portrait("plt_colony_02", _col2_x + 20, _a2_y, 72, true, "neutral");
            draw_set_color(make_color_rgb(40, 210, 180));
            draw_text(_col2_x + 120, _a2_y, "KIRA DAHL [RECRUITABLE ELECTRONIC WARFARE]");
            draw_set_color(c_white);
            draw_text(_col2_x + 120, _a2_y + 20, "Accuracy: 70% | Reflexes: 80% | Bravery: 80% | Trait: ECM Jamming (-20% Enemy Accuracy)");
            draw_text_ext(_col2_x + 120, _a2_y + 38, "Sensor engineer who defected to test novel radar signal scrambler arrays in live combat.", 18, _col2_w - 280);

            var _hb2_x = _col2_x + _col2_w - 160;
            var _hb2_y = _a2_y + 15;
            var _h2_hov = (_mx >= _hb2_x && _mx <= _hb2_x + 140 && _my >= _hb2_y && _my <= _hb2_y + 36);
            if (_h2_hov && _click && instance_exists(obj_GameManager)) {
                if (obj_GameManager.spend_funds(34000)) {
                    array_push(obj_GameManager.facilities.roster_pilots, {
                        id: "plt_colony_02", character_id: "pilot_colony_kira", name: "Kira Dahl", callsign: "SPECTER", combat_stat: 7, tactics_stat: 8, accuracy: 70, reflexes: 80, morale: 90, salary_daily: 190, is_deployed: false, status: "ACTIVE", recovery_days: 0, recovery_days_left: 0, kills: 1, sorties: 2
                    });
                    show_toast("KIRA DAHL HIRED TO PMC ROSTER!", c_lime);
                } else show_toast("INSUFFICIENT FUNDS! (Requires 34,000 Cr)", c_red);
            }
            draw_set_color(_h2_hov ? make_color_rgb(30, 80, 50) : make_color_rgb(18, 45, 28));
            draw_rectangle(_hb2_x, _hb2_y, _hb2_x + 140, _hb2_y + 36, false);
            draw_set_color(make_color_rgb(80, 220, 120));
            draw_rectangle(_hb2_x, _hb2_y, _hb2_x + 140, _hb2_y + 36, true);
            draw_set_color(c_white);
            draw_text(_hb2_x + 14, _hb2_y + 10, "[HIRE: 34,000 Cr]");

            // Strategic Bases & Citadels Readout (docs/11)
            var _by = _d_y + 365;
            draw_set_color(make_color_rgb(40, 210, 180));
            draw_text(_col2_x + 20, _by, "MAJOR STRATEGIC STRONGHOLDS (EARTH & SPACE):");
            draw_set_color(make_color_rgb(170, 240, 225));
            draw_text(_col2_x + 20, _by + 18, "• [SPACE] Ganymede Nexus 'Olympus Commune' - Capital bio-domes & zero-G automated electron-beam shipyards");
            draw_text(_col2_x + 20, _by + 34, "• [SPACE] Fortress Valhalla (L4 Trojan Asteroid) - Cassian Vane's covert headquarters in 40km hollow asteroid");
            draw_text(_col2_x + 20, _by + 50, "• [SPACE] L5 Solar Scrubber Array 'Dawn-7' - Multi-km photovoltaic mirrors supplying life support to habitats");
            draw_text(_col2_x + 20, _by + 66, "• [EARTH] Red Sands Deep Sanctuary (Atacama) - Top-secret borehole base for OCM-09G guerrilla strikes");
        }
        else if (selected_faction_dossier == "faction_syndicate") {
            draw_set_color(make_color_rgb(240, 140, 40));
            draw_text(_col2_x + 20, _d_y + 14, "THE RIM-SYNDICATE CARTEL // SCAVENGER-INDUSTRIAL GUILD");
            draw_set_color(make_color_rgb(180, 210, 240));
            draw_text_ext(_col2_x + 20, _d_y + 36, "Doctrine: Asymmetrical ambushes, scrap-welded hybrid chimeras, thermite cutters, and magnetic harpoons. Outlaw brokers trading stolen blueprints for rare isotopes.", 20, _col2_w - 40);

            var _l_y = _d_y + 86;
            scr_draw_composite_portrait("char_cruz", _col2_x + 20, _l_y, 72, true, "stoic");
            draw_set_color(make_color_rgb(240, 210, 100));
            draw_text(_col2_x + 120, _l_y, "MADAME ROSALIND CRUZ // MATRIARCH OF SCRAP DEPOT 9");
            draw_set_color(c_white);
            draw_text_ext(_col2_x + 120, _l_y + 22, "'Earth and the Colonies have been burning each other's fleets for ten years, darling. And every time a million-dollar cockpit pops in vacuum, my boys are there with blowtorches. War is the only reliable commodity.'", 18, _col2_w - 140);

            var _a1_y = _l_y + 115;
            scr_draw_composite_portrait("plt_syndicate_01", _col2_x + 20, _a1_y, 72, true, "neutral");
            draw_set_color(make_color_rgb(240, 140, 40));
            draw_text(_col2_x + 120, _a1_y, "NADIA 'SPARK' ORTIZ [RECRUITABLE SCRAP MECHANIC]");
            draw_set_color(c_white);
            draw_text(_col2_x + 120, _a1_y + 20, "Accuracy: 72% | Reflexes: 65% | Bravery: 88% | Trait: Field Rigging (+25% Post-Battle Scrap)");
            draw_text_ext(_col2_x + 120, _a1_y + 38, "Teenage prodigy mechanic who hotwires burned-out manifolds under live fire and laughs in battle.", 18, _col2_w - 280);

            var _hb1_x = _col2_x + _col2_w - 160;
            var _hb1_y = _a1_y + 15;
            var _h1_hov = (_mx >= _hb1_x && _mx <= _hb1_x + 140 && _my >= _hb1_y && _my <= _hb1_y + 36);
            if (_h1_hov && _click && instance_exists(obj_GameManager)) {
                if (obj_GameManager.spend_funds(31000)) {
                    array_push(obj_GameManager.facilities.roster_pilots, {
                        id: "plt_syndicate_01", character_id: "pilot_syndicate_nadia", name: "Nadia Ortiz", callsign: "SPARK", combat_stat: 7, tactics_stat: 7, accuracy: 72, reflexes: 65, morale: 95, salary_daily: 170, is_deployed: false, status: "ACTIVE", recovery_days: 0, recovery_days_left: 0, kills: 2, sorties: 4
                    });
                    show_toast("NADIA 'SPARK' ORTIZ HIRED TO PMC ROSTER!", c_lime);
                } else show_toast("INSUFFICIENT FUNDS! (Requires 31,000 Cr)", c_red);
            }
            draw_set_color(_h1_hov ? make_color_rgb(30, 80, 50) : make_color_rgb(18, 45, 28));
            draw_rectangle(_hb1_x, _hb1_y, _hb1_x + 140, _hb1_y + 36, false);
            draw_set_color(make_color_rgb(80, 220, 120));
            draw_rectangle(_hb1_x, _hb1_y, _hb1_x + 140, _hb1_y + 36, true);
            draw_set_color(c_white);
            draw_text(_hb1_x + 14, _hb1_y + 10, "[HIRE: 31,000 Cr]");

            var _a2_y = _a1_y + 95;
            scr_draw_composite_portrait("plt_syndicate_02", _col2_x + 20, _a2_y, 72, true, "enraged");
            draw_set_color(make_color_rgb(240, 140, 40));
            draw_text(_col2_x + 120, _a2_y, "'JACKAL' JAX VANCE [RECRUITABLE HARPOONER]");
            draw_set_color(c_white);
            draw_text(_col2_x + 120, _a2_y + 20, "Accuracy: 80% | Reflexes: 78% | Bravery: 70% | Trait: Harpoon Tether (Pins Mechs)");
            draw_text_ext(_col2_x + 120, _a2_y + 38, "Mercenary raider specializing in pinning enemy suits with magnetic boarding cables.", 18, _col2_w - 280);

            var _hb2_x = _col2_x + _col2_w - 160;
            var _hb2_y = _a2_y + 15;
            var _h2_hov = (_mx >= _hb2_x && _mx <= _hb2_x + 140 && _my >= _hb2_y && _my <= _hb2_y + 36);
            if (_h2_hov && _click && instance_exists(obj_GameManager)) {
                if (obj_GameManager.spend_funds(41000)) {
                    array_push(obj_GameManager.facilities.roster_pilots, {
                        id: "plt_syndicate_02", character_id: "pilot_syndicate_jackal", name: "Jax Vance", callsign: "JACKAL", combat_stat: 8, tactics_stat: 8, accuracy: 80, reflexes: 78, morale: 65, salary_daily: 230, is_deployed: false, status: "ACTIVE", recovery_days: 0, recovery_days_left: 0, kills: 3, sorties: 5
                    });
                    show_toast("JAX 'JACKAL' VANCE HIRED TO PMC ROSTER!", c_lime);
                } else show_toast("INSUFFICIENT FUNDS! (Requires 41,000 Cr)", c_red);
            }
            draw_set_color(_h2_hov ? make_color_rgb(30, 80, 50) : make_color_rgb(18, 45, 28));
            draw_rectangle(_hb2_x, _hb2_y, _hb2_x + 140, _hb2_y + 36, false);
            draw_set_color(make_color_rgb(80, 220, 120));
            draw_rectangle(_hb2_x, _hb2_y, _hb2_x + 140, _hb2_y + 36, true);
            draw_set_color(c_white);
            draw_text(_hb2_x + 14, _hb2_y + 10, "[HIRE: 41,000 Cr]");

            // Strategic Bases & Citadels Readout (docs/11)
            var _by = _d_y + 365;
            draw_set_color(make_color_rgb(240, 140, 40));
            draw_text(_col2_x + 20, _by, "MAJOR STRATEGIC STRONGHOLDS (EARTH & SPACE):");
            draw_set_color(make_color_rgb(255, 210, 170));
            draw_text(_col2_x + 20, _by + 18, "• [SPACE] Scrap Depot 9 'The Slag Heap' (Ceres) - Outlaw capital hollowed in Ceres mantle, molten slag rivers");
            draw_text(_col2_x + 20, _by + 34, "• [SPACE] Dead Fleet Anchorage 'Tortuga-Void' (Eros) - Torval's reaver haven lashed from 70+ derelict ships");
            draw_text(_col2_x + 20, _by + 50, "• [SPACE] The Spindle Forge (Pallas Basin) - Nadia Ortiz's chop-shop tuning blown reactors in under 2 hours");
            draw_text(_col2_x + 20, _by + 66, "• [EARTH] Rust Coast Shipbreaking Slums (Chittagong) - Lawless shoreline smuggling rare isotopes to PMCs");
        }
        else if (selected_faction_dossier == "faction_zaibatsu") {
            draw_set_color(make_color_rgb(180, 90, 240));
            draw_text(_col2_x + 20, _d_y + 14, "APEX BIO-CYBERNETICS ZAIBATSU // TRANSHUMAN HYPER-CORP");
            draw_set_color(make_color_rgb(180, 210, 240));
            draw_text_ext(_col2_x + 20, _d_y + 36, "Doctrine: Sub-millisecond latency, carbon-nanotube musculature, monomolecular blades, and illegal direct-neural pilot man-machine interfaces.", 20, _col2_w - 40);

            var _l_y = _d_y + 86;
            scr_draw_composite_portrait("char_takahashi", _col2_x + 20, _l_y, 72, true, "stoic");
            draw_set_color(make_color_rgb(240, 210, 100));
            draw_text(_col2_x + 120, _l_y, "DIRECTOR RENZO TAKAHASHI // VP SPECIAL WEAPONS");
            draw_set_color(c_white);
            draw_text_ext(_col2_x + 120, _l_y + 22, "'Human reaction time is limited to two hundred milliseconds. Our neural-interface bypasses ocular processing entirely, cutting weapon discharge latency to twelve. Progress requires shedding biological sentiment.'", 18, _col2_w - 140);

            var _a1_y = _l_y + 115;
            scr_draw_composite_portrait("plt_zaibatsu_01", _col2_x + 20, _a1_y, 72, true, "stoic");
            draw_set_color(make_color_rgb(180, 90, 240));
            draw_text(_col2_x + 120, _a1_y, "NULL-07 (REN) [RECRUITABLE NEURAL ACE]");
            draw_set_color(c_white);
            draw_text(_col2_x + 120, _a1_y + 20, "Acc: 96% | Ref: 88% | Morale: 50% | Trait: Neural Link (+2 Actions)");
            draw_text_ext(_col2_x + 120, _a1_y + 38, "Pale escaped test subject with spinal data-ports; reacts to projectile trajectories before muzzle flashes.", 18, _col2_w - 280);

            var _hb1_x = _col2_x + _col2_w - 160;
            var _hb1_y = _a1_y + 15;
            var _h1_hov = (_mx >= _hb1_x && _mx <= _hb1_x + 140 && _my >= _hb1_y && _my <= _hb1_y + 36);
            if (_h1_hov && _click && instance_exists(obj_GameManager)) {
                if (obj_GameManager.spend_funds(65000)) {
                    array_push(obj_GameManager.facilities.roster_pilots, {
                        id: "plt_zaibatsu_01", character_id: "pilot_zaibatsu_null07", name: "Null-07 (Ren)", callsign: "NULL", combat_stat: 10, tactics_stat: 9, accuracy: 96, reflexes: 88, morale: 50, salary_daily: 320, is_deployed: false, status: "ACTIVE", recovery_days: 0, recovery_days_left: 0, kills: 6, sorties: 8
                    });
                    show_toast("NULL-07 RECRUITED TO PMC ROSTER!", c_lime);
                } else show_toast("INSUFFICIENT FUNDS! (Requires 65,000 Cr)", c_red);
            }
            draw_set_color(_h1_hov ? make_color_rgb(30, 80, 50) : make_color_rgb(18, 45, 28));
            draw_rectangle(_hb1_x, _hb1_y, _hb1_x + 140, _hb1_y + 36, false);
            draw_set_color(make_color_rgb(80, 220, 120));
            draw_rectangle(_hb1_x, _hb1_y, _hb1_x + 140, _hb1_y + 36, true);
            draw_set_color(c_white);
            draw_text(_hb1_x + 14, _hb1_y + 10, "[HIRE: 65,000 Cr]");

            var _a2_y = _a1_y + 95;
            scr_draw_composite_portrait("plt_zaibatsu_02", _col2_x + 20, _a2_y, 72, true, "neutral");
            draw_set_color(make_color_rgb(180, 90, 240));
            draw_text(_col2_x + 120, _a2_y, "MAYA 'KESTREL' ZHAO [RECRUITABLE DRONE TACTICIAN]");
            draw_set_color(c_white);
            draw_text(_col2_x + 120, _a2_y + 20, "Acc: 84% | Ref: 75% | Morale: 85% | Trait: Drones (+1 Drone)");
            draw_text_ext(_col2_x + 120, _a2_y + 38, "Former corporate security flight commander who bought out her indenture debt with stolen securities.", 18, _col2_w - 280);

            var _hb2_x = _col2_x + _col2_w - 160;
            var _hb2_y = _a2_y + 15;
            var _h2_hov = (_mx >= _hb2_x && _mx <= _hb2_x + 140 && _my >= _hb2_y && _my <= _hb2_y + 36);
            if (_h2_hov && _click && instance_exists(obj_GameManager)) {
                if (obj_GameManager.spend_funds(46000)) {
                    array_push(obj_GameManager.facilities.roster_pilots, {
                        id: "plt_zaibatsu_02", character_id: "pilot_zaibatsu_maya", name: "Maya Zhao", callsign: "KESTREL", combat_stat: 8, tactics_stat: 8, accuracy: 84, reflexes: 75, morale: 85, salary_daily: 240, is_deployed: false, status: "ACTIVE", recovery_days: 0, recovery_days_left: 0, kills: 3, sorties: 5
                    });
                    show_toast("MAYA ZHAO HIRED TO PMC ROSTER!", c_lime);
                } else show_toast("INSUFFICIENT FUNDS! (Requires 46,000 Cr)", c_red);
            }
            draw_set_color(_h2_hov ? make_color_rgb(30, 80, 50) : make_color_rgb(18, 45, 28));
            draw_rectangle(_hb2_x, _hb2_y, _hb2_x + 140, _hb2_y + 36, false);
            draw_set_color(make_color_rgb(80, 220, 120));
            draw_rectangle(_hb2_x, _hb2_y, _hb2_x + 140, _hb2_y + 36, true);
            draw_set_color(c_white);
            draw_text(_hb2_x + 14, _hb2_y + 10, "[HIRE: 46,000 Cr]");

            // Strategic Bases & Citadels Readout (docs/11)
            var _by = _d_y + 365;
            draw_set_color(make_color_rgb(180, 90, 240));
            draw_text(_col2_x + 20, _by, "MAJOR STRATEGIC STRONGHOLDS (EARTH & SPACE):");
            draw_set_color(make_color_rgb(220, 185, 255));
            draw_text(_col2_x + 20, _by + 18, "• [SPACE] Citadel Susanoo (Earth-Sun L2) - Cloaked obsidian polyhedron with vacuum automated robotic foundries");
            draw_text(_col2_x + 20, _by + 34, "• [SPACE] Lab-Complex Zero 'The Nursery' (Kuiper Belt) - Classified human neural-sync test station (Null-07 origin)");
            draw_text(_col2_x + 20, _by + 50, "• [EARTH] Neo-Kobe Megaplex & Sky-Spire (Osaka Bay) - Chrome spires on sea caissons housing police mech lines");
            draw_text(_col2_x + 20, _by + 66, "• [EARTH] Atacama Quantum Data Vault (Chile) - Subterranean computing vault training predictive combat AI");
        }
        } // End Branch B else
    }

    // =====================================================================
    // SUBTAB 2: FACTION AI DIPLOMACY, ALLIANCES & WAR ROOM MATRIX (DOC 21)
    // =====================================================================
    else if (war_subtab == 2) {
        var _dx = _pan_x + 20;
        var _dy = _pan_y + 42;
        var _dw = _pan_w - 40;
        var _dh = _pan_h - 52;

        if (instance_exists(obj_FactionManager)) {
            var _fm = obj_FactionManager;
            var _tc = _fm.territory_control;

            // 1. Top Header & Hegemonic Threat Balance Bar
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_dx, _dy, "== SOL SYSTEM DIPLOMATIC MATRIX & WAR ROOM ==");

            // Hegemony Balance & Anti-Blobbing Alert Banner
            var _ban_y = _dy + 22;
            var _ban_h = 30;
            var _is_hegemon = (_fm.hegemon_faction_id != "");
            draw_set_color(_is_hegemon ? make_color_rgb(45, 15, 18) : make_color_rgb(12, 22, 35));
            draw_rectangle(_dx, _ban_y, _dx + _dw, _ban_y + _ban_h, false);
            draw_set_color(_is_hegemon ? make_color_rgb(255, 60, 60) : make_color_rgb(40, 75, 115));
            draw_rectangle(_dx, _ban_y, _dx + _dw, _ban_y + _ban_h, true);

            if (_is_hegemon) {
                var _hege_name = (_fm.hegemon_faction_id == "faction_a") ? "THE TERRAN COALITION" :
                                 ((_fm.hegemon_faction_id == "faction_b") ? "THE OUTER COLONIES" :
                                 ((_fm.hegemon_faction_id == "faction_c") ? "ROGUE SYNDICATES" : "APEX ZAIBATSU"));
                draw_set_color(make_color_rgb(255, 90, 90));
                draw_text(_dx + 12, _ban_y + 6, "⚠ HEGEMONIC CRISIS: " + _hege_name + " controls >40% Sol territory! Anti-Hegemon Emergency Coalition Active (-15 Tension / Mutual Defense)!");
            } else {
                draw_set_color(make_color_rgb(160, 210, 255));
                draw_text(_dx + 12, _ban_y + 6, "MULTI-POLAR BALANCE: Alliances are temporary expedients (+2.5/turn Paranoia). Sol Status: Dynamic Cold War & Border Skirmishes.");
            }

            // 2. Left Column: 6-Pair Bilateral Relations Grid (width: 440)
            var _col1_x = _dx;
            var _col1_y = _ban_y + _ban_h + 8;
            var _col1_w = 440;
            var _col1_h = _dh - (_col1_y - _dy);

            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_col1_x, _col1_y, _col1_x + _col1_w, _col1_y + _col1_h, false);
            draw_set_color(make_color_rgb(30, 50, 75));
            draw_rectangle(_col1_x, _col1_y, _col1_x + _col1_w, _col1_y + _col1_h, true);

            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_col1_x + 12, _col1_y + 8, "BILATERAL RELATIONS MATRIX (12 PAIRS):");

            var _pairs = [
                "terran_colony",
                "terran_syndicate",
                "terran_zaibatsu",
                "colony_syndicate",
                "colony_zaibatsu",
                "syndicate_zaibatsu",
                "terran_astran",
                "colony_astran",
                "syndicate_astran",
                "zaibatsu_astran",
                "terran_martian",
                "zaibatsu_martian"
            ];

            var _card_y_start = _col1_y + 26;
            var _card_h = 42;
            var _num_pairs = min(8, array_length(_pairs));

            for (var _pair_i = 0; _pair_i < _num_pairs; _pair_i++) {
                var _pid = _pairs[_pair_i];
                var _rel = variable_struct_get(_fm.diplomatic_relations, _pid);
                if (is_undefined(_rel)) continue;

                var _cy = _card_y_start + _pair_i * (_card_h + 4);
                var _is_sel = (selected_diplo_pair == _pid);
                var _c_hov = (_mx >= _col1_x + 8 && _mx <= _col1_x + _col1_w - 8 && _my >= _cy && _my <= _cy + _card_h);
                if (_c_hov && _click) selected_diplo_pair = _pid;

                // Card background
                draw_set_color(_is_sel ? make_color_rgb(25, 48, 76) : (_c_hov ? make_color_rgb(18, 30, 46) : make_color_rgb(13, 20, 30)));
                draw_rectangle(_col1_x + 8, _cy, _col1_x + _col1_w - 8, _cy + _card_h, false);

                // State badge color
                var _st_col = make_color_rgb(150, 180, 220); // NON_AGGRESSION
                if (_rel.state == "WAR") _st_col = make_color_rgb(255, 60, 60);
                else if (_rel.state == "COLD_WAR") _st_col = make_color_rgb(200, 100, 255);
                else if (_rel.state == "TRUCE") _st_col = make_color_rgb(255, 200, 50);
                else if (_rel.state == "ALLIANCE") _st_col = make_color_rgb(0, 240, 255);

                draw_set_color(_is_sel ? make_color_rgb(100, 220, 255) : make_color_rgb(35, 55, 80));
                draw_rectangle(_col1_x + 8, _cy, _col1_x + _col1_w - 8, _cy + _card_h, true);

                // Pair names (compact)
                draw_set_color(c_white);
                var _p_name1 = (variable_struct_get(variable_struct_get(_fm.factions, _rel.faction_1), "short_name") ?? _rel.name_1);
                var _p_name2 = (variable_struct_get(variable_struct_get(_fm.factions, _rel.faction_2), "short_name") ?? _rel.name_2);
                draw_text(_col1_x + 14, _cy + 4, _p_name1 + " vs " + _p_name2);

                // State badge
                var _badge_str = "[" + _rel.state + "]";
                if (_rel.treaty_turns_left > 0) _badge_str += " (" + string(_rel.treaty_turns_left) + "T)";
                draw_set_color(_st_col);
                draw_text(_col1_x + _col1_w - 14 - string_width(_badge_str), _cy + 4, _badge_str);

                // Tension bar
                var _bar_x = _col1_x + 14;
                var _bar_y = _cy + 22;
                var _bar_w = _col1_w - 28;
                var _bar_h = 7;
                draw_set_color(make_color_rgb(20, 28, 38));
                draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_w, _bar_y + _bar_h, false);

                var _ten_w = (_bar_w * (_rel.tension / 100.0));
                var _ten_col = (_rel.tension >= 75) ? make_color_rgb(255, 60, 60) :
                               ((_rel.tension >= 50) ? make_color_rgb(255, 170, 40) : make_color_rgb(80, 220, 120));
                draw_set_color(_ten_col);
                draw_rectangle(_bar_x, _bar_y, _bar_x + _ten_w, _bar_y + _bar_h, false);

                // Tension value and drift note
                var _drift_lbl = "";
                if (_rel.state == "ALLIANCE") _drift_lbl = "+2.5/T Paranoia";
                else if (_rel.state == "TRUCE") _drift_lbl = "-2.0/T Truce";
                else if (_rel.state == "COLD_WAR") _drift_lbl = "+" + string(_rel.base_friction) + "/T Friction";
                else if (_rel.state == "WAR") _drift_lbl = "Active War (" + string(_rel.war_duration_turns) + "T)";
                else if (_rel.state == "WAR") _drift_lbl = "ACTIVE FRONTLINE WAR";

                draw_set_color(make_color_rgb(180, 200, 220));
                draw_text(_col1_x + 16, _cy + 30, "Tension: " + string(_rel.tension) + "/100  |  " + _drift_lbl);
            }

            // 3. Right Column: Detailed Strategic Dossier & Action Console
            var _col2_x = _col1_x + _col1_w + 14;
            var _col2_y = _col1_y;
            var _col2_w = _dw - _col1_w - 14;
            var _doss_h = 286;

            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_col2_x, _col2_y, _col2_x + _col2_w, _col2_y + _doss_h, false);
            draw_set_color(make_color_rgb(30, 50, 75));
            draw_rectangle(_col2_x, _col2_y, _col2_x + _col2_w, _col2_y + _doss_h, true);

            var _cur_rel = variable_struct_get(_fm.diplomatic_relations, selected_diplo_pair);
            if (!is_undefined(_cur_rel)) {
                var _cr_name1 = string(_cur_rel.name_1 ?? "Faction 1");
                var _cr_name2 = string(_cur_rel.name_2 ?? "Faction 2");
                var _cr_state = string(_cur_rel.state ?? "COLD_WAR");
                var _cr_cb = string(_cur_rel.casus_belli ?? "Territorial friction");
                var _cr_hg = string(_cur_rel.historical_grievance ?? "Border dispute");

                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_col2_x + 14, _col2_y + 8, "STRATEGIC DOSSIER: " + _cr_name1 + " <---> " + _cr_name2);

                // Status & Metrics Row
                var _r_badge_col = (_cr_state == "WAR") ? make_color_rgb(255, 60, 60) :
                                   ((_cr_state == "ALLIANCE") ? make_color_rgb(0, 240, 255) :
                                   ((_cr_state == "TRUCE") ? make_color_rgb(255, 200, 50) : make_color_rgb(200, 100, 255)));

                draw_set_color(_r_badge_col);
                draw_text(_col2_x + 14, _col2_y + 26, "Current Status: [" + _cr_state + "]");

                draw_set_color(c_white);
                var _ttl = variable_struct_get(_cur_rel, "treaty_turns_left") ?? 0;
                var _treaty_txt = (_ttl > 0) ? (string(_ttl) + " turns remaining") : "None";
                draw_text(_col2_x + 220, _col2_y + 26, "Treaty Countdown: " + _treaty_txt);
                var _twf = variable_struct_get(_cur_rel, "total_wars_fought") ?? 0;
                draw_text(_col2_x + 460, _col2_y + 26, "Total Wars Fought: " + string(_twf));

                // Casus Belli & Grievance
                draw_set_color(make_color_rgb(255, 220, 120));
                draw_text(_col2_x + 14, _col2_y + 44, "Casus Belli: " + _cr_cb);
                draw_set_color(make_color_rgb(180, 200, 220));
                draw_text_ext(_col2_x + 14, _col2_y + 60, "Historical Grievance: " + _cr_hg, 16, _col2_w - 28);

                // Faction AI Behavioral Intelligence Box (docs/36)
                var _f1 = variable_struct_get(_fm.factions, _cur_rel.faction_1);
                var _f2 = variable_struct_get(_fm.factions, _cur_rel.faction_2);
                if (!is_undefined(_f1) && !is_undefined(_f2)) {
                    var _f1_sn = string(_f1.short_name ?? "FACTION 1");
                    var _f1_st = string(_f1.ai_state ?? "PEACE");
                    var _f1_bt = string(_f1.ai_behavior_title ?? "Standard Doctrine");
                    var _f1_ar = string_upper(string(_f1.primary_enemy_id ?? "NONE"));
                    var _f1_pa = string_upper(string(_f1.preferred_ally_id ?? "NONE"));
                    var _f1_bm = string(_f1.contract_bounty_multiplier ?? 1.0);

                    var _f2_sn = string(_f2.short_name ?? "FACTION 2");
                    var _f2_st = string(_f2.ai_state ?? "PEACE");
                    var _f2_bt = string(_f2.ai_behavior_title ?? "Standard Doctrine");
                    var _f2_ar = string_upper(string(_f2.primary_enemy_id ?? "NONE"));
                    var _f2_pa = string_upper(string(_f2.preferred_ally_id ?? "NONE"));
                    var _f2_bm = string(_f2.contract_bounty_multiplier ?? 1.0);

                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_col2_x + 14, _col2_y + 94, "FACTION AI BRAIN & BEHAVIORAL INTELLIGENCE:");

                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_col2_x + 14, _col2_y + 112, "* " + _f1_sn + " [" + _f1_st + "]: " + _f1_bt);
                    draw_set_color(make_color_rgb(190, 215, 240));
                    draw_text(_col2_x + 24, _col2_y + 128, "  Arch-Rival: " + _f1_ar + "  |  Preferred Ally: " + _f1_pa + "  |  Bounty Mult: " + _f1_bm + "x");

                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_col2_x + 14, _col2_y + 146, "* " + _f2_sn + " [" + _f2_st + "]: " + _f2_bt);
                    draw_set_color(make_color_rgb(190, 215, 240));
                    draw_text(_col2_x + 24, _col2_y + 162, "  Arch-Rival: " + _f2_ar + "  |  Preferred Ally: " + _f2_pa + "  |  Bounty Mult: " + _f2_bm + "x");
                }

                // Alliance Paranoia Advisory Box
                var _adv_y = _col2_y + 184;
                if (_cur_rel.state == "ALLIANCE") {
                    draw_set_color(make_color_rgb(18, 38, 50));
                    draw_rectangle(_col2_x + 14, _adv_y, _col2_x + _col2_w - 14, _adv_y + 40, false);
                    draw_set_color(make_color_rgb(0, 220, 255));
                    draw_rectangle(_col2_x + 14, _adv_y, _col2_x + _col2_w - 14, _adv_y + 40, true);
                    draw_text(_col2_x + 22, _adv_y + 4, "ALLIANCE PARANOIA ACTIVE (+2.5 Tension/turn):");
                    draw_set_color(make_color_rgb(180, 230, 255));
                    draw_text(_col2_x + 22, _adv_y + 20, "Espionage festers during military pacts. If Tension hits 75+, pact dissolves into Cold War or War!");
                } else if (_cur_rel.state == "TRUCE") {
                    draw_set_color(make_color_rgb(45, 38, 14));
                    draw_rectangle(_col2_x + 14, _adv_y, _col2_x + _col2_w - 14, _adv_y + 40, false);
                    draw_set_color(make_color_rgb(255, 200, 50));
                    draw_rectangle(_col2_x + 14, _adv_y, _col2_x + _col2_w - 14, _adv_y + 40, true);
                    draw_text(_col2_x + 22, _adv_y + 4, "CEASEFIRE ACCORD ACTIVE (-2.0 Tension/turn):");
                    draw_set_color(make_color_rgb(255, 230, 160));
                    draw_text(_col2_x + 22, _adv_y + 20, "Combat sorties frozen. When timer expires, peace normalizes or reverts to Cold War depending on tension.");
                } else if (_cur_rel.state == "WAR") {
                    draw_set_color(make_color_rgb(45, 14, 18));
                    draw_rectangle(_col2_x + 14, _adv_y, _col2_x + _col2_w - 14, _adv_y + 40, false);
                    draw_set_color(make_color_rgb(255, 60, 60));
                    draw_rectangle(_col2_x + 14, _adv_y, _col2_x + _col2_w - 14, _adv_y + 40, true);
                    draw_text(_col2_x + 22, _adv_y + 4, "ACTIVE FRONTLINE COMBAT:");
                    draw_set_color(make_color_rgb(255, 180, 180));
                    draw_text(_col2_x + 22, _adv_y + 20, "Armies clashing weekly. Mass-production licenses and allied pacts sway territorial shifts.");
                } else {
                    draw_set_color(make_color_rgb(25, 20, 38));
                    draw_rectangle(_col2_x + 14, _adv_y, _col2_x + _col2_w - 14, _adv_y + 40, false);
                    draw_set_color(make_color_rgb(180, 120, 240));
                    draw_rectangle(_col2_x + 14, _adv_y, _col2_x + _col2_w - 14, _adv_y + 40, true);
                    draw_text(_col2_x + 22, _adv_y + 4, "DIPLOMATIC POSTURE: " + _cur_rel.state);
                    draw_set_color(make_color_rgb(210, 190, 240));
                    draw_text(_col2_x + 22, _adv_y + 20, "Tension drifts toward boiling point (85+ = War). Use PMC operations to influence relations.");
                }

                // Interactive PMC Mercenary Diplomacy Actions
                var _act_y = _col2_y + 232;
                var _act_btn_w = (_col2_w - 44) / 3;

                // Action 1: Broker Ceasefire
                var _b1_x = _col2_x + 14;
                var _b1_en = (_cur_rel.state == "WAR");
                var _b1_hov = (_mx >= _b1_x && _mx <= _b1_x + _act_btn_w && _my >= _act_y && _my <= _act_y + 46);
                if (_b1_en && _b1_hov && _click) {
                    _fm.player_broker_ceasefire(selected_diplo_pair);
                }
                draw_set_color(_b1_en ? (_b1_hov ? make_color_rgb(30, 60, 45) : make_color_rgb(18, 38, 28)) : make_color_rgb(16, 20, 24));
                draw_rectangle(_b1_x, _act_y, _b1_x + _act_btn_w, _act_y + 46, false);
                draw_set_color(_b1_en ? make_color_rgb(80, 220, 120) : make_color_rgb(45, 55, 65));
                draw_rectangle(_b1_x, _act_y, _b1_x + _act_btn_w, _act_y + 46, true);
                draw_set_color(_b1_en ? c_white : c_gray);
                draw_text(_b1_x + 10, _act_y + 6, "[BROKER TRUCE]");
                draw_set_color(_b1_en ? make_color_rgb(180, 255, 180) : c_gray);
                draw_text(_b1_x + 10, _act_y + 24, "-50,000 Cr | 14 Turns");

                // Action 2: Provoke Proxy Crisis
                var _b2_x = _b1_x + _act_btn_w + 8;
                var _b2_hov = (_mx >= _b2_x && _mx <= _b2_x + _act_btn_w && _my >= _act_y && _my <= _act_y + 46);
                if (_b2_hov && _click) {
                    _fm.player_provoke_crisis(selected_diplo_pair);
                }
                draw_set_color(_b2_hov ? make_color_rgb(70, 40, 20) : make_color_rgb(38, 22, 12));
                draw_rectangle(_b2_x, _act_y, _b2_x + _act_btn_w, _act_y + 46, false);
                draw_set_color(make_color_rgb(255, 140, 40));
                draw_rectangle(_b2_x, _act_y, _b2_x + _act_btn_w, _act_y + 46, true);
                draw_set_color(c_white);
                draw_text(_b2_x + 10, _act_y + 6, "[PROVOKE CRISIS]");
                draw_set_color(make_color_rgb(255, 200, 140));
                draw_text(_b2_x + 10, _act_y + 24, "-40,000 Cr | +25 Tension");

                // Action 3: Offer Coalition Alliance
                var _b3_x = _b2_x + _act_btn_w + 8;
                var _b3_en = (_cur_rel.state != "WAR");
                var _b3_hov = (_mx >= _b3_x && _mx <= _b3_x + _act_btn_w && _my >= _act_y && _my <= _act_y + 46);
                if (_b3_en && _b3_hov && _click) {
                    _fm.player_negotiate_coalition(selected_diplo_pair);
                }
                draw_set_color(_b3_en ? (_b3_hov ? make_color_rgb(20, 60, 75) : make_color_rgb(14, 38, 48)) : make_color_rgb(16, 20, 24));
                draw_rectangle(_b3_x, _act_y, _b3_x + _act_btn_w, _act_y + 46, false);
                draw_set_color(_b3_en ? make_color_rgb(0, 220, 255) : make_color_rgb(45, 55, 65));
                draw_rectangle(_b3_x, _act_y, _b3_x + _act_btn_w, _act_y + 46, true);
                draw_set_color(_b3_en ? c_white : c_gray);
                draw_text(_b3_x + 10, _act_y + 6, "[OFFER ALLIANCE]");
                draw_set_color(_b3_en ? make_color_rgb(160, 240, 255) : c_gray);
                draw_text(_b3_x + 10, _act_y + 24, "-60,000 Cr | 18 Turns");
            }

            // 4. Right Column Bottom: Live Diplomatic Cables Teletype Feed
            var _feed_y = _col2_y + _doss_h + 8;
            var _feed_h = _col1_h - _doss_h - 8;

            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_col2_x, _feed_y, _col2_x + _col2_w, _feed_y + _feed_h, false);
            draw_set_color(make_color_rgb(30, 50, 75));
            draw_rectangle(_col2_x, _feed_y, _col2_x + _col2_w, _feed_y + _feed_h, true);

            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_col2_x + 14, _feed_y + 8, "COMMAND DECK DIPLOMATIC CABLES & TELETYPE FEED:");

            // Cables List & Paging
            var _cables = _fm.diplomatic_cables_log;
            var _num_cables = array_length(_cables);
            var _max_vis_cables = 3;
            var _c_entry_h = 56;
            var _c_y_start = _feed_y + 28;

            for (var ci = 0; ci < min(_max_vis_cables, _num_cables); ci++) {
                // Reverse chronological display (newest first)
                var _c_idx = (_num_cables - 1) - (ci + diplo_cables_scroll_offset);
                if (_c_idx < 0 || _c_idx >= _num_cables) break;

                var _cable = _cables[_c_idx];
                var _cby = _c_y_start + ci * (_c_entry_h + 6);

                draw_set_color(make_color_rgb(14, 20, 28));
                draw_rectangle(_col2_x + 12, _cby, _col2_x + _col2_w - 12, _cby + _c_entry_h, false);

                var _c_prio = (variable_struct_exists(_cable, "priority") && !is_undefined(_cable.priority)) ? string(_cable.priority) : "NORMAL";
                var _c_turn_val = (variable_struct_exists(_cable, "turn") && !is_undefined(_cable.turn)) ? string(_cable.turn) : "1";
                var _c_title = (variable_struct_exists(_cable, "title") && !is_undefined(_cable.title)) ? string(_cable.title) : "Diplomatic Notice";
                var _c_sender = (variable_struct_exists(_cable, "sender") && !is_undefined(_cable.sender)) ? string(_cable.sender) : "HQ Command";
                var _c_recip = (variable_struct_exists(_cable, "recipient") && !is_undefined(_cable.recipient)) ? string(_cable.recipient) : "Sol Network";
                var _c_body = (variable_struct_exists(_cable, "body") && !is_undefined(_cable.body)) ? string(_cable.body) : "";

                var _cb_border_col = (_c_prio == "URGENT") ? make_color_rgb(255, 60, 60) :
                                     ((_c_prio == "HIGH") ? make_color_rgb(0, 220, 255) : make_color_rgb(45, 65, 90));
                draw_set_color(_cb_border_col);
                draw_rectangle(_col2_x + 12, _cby, _col2_x + _col2_w - 12, _cby + _c_entry_h, true);

                // Priority Badge & Turn Timestamp
                draw_set_color((_c_prio == "URGENT") ? make_color_rgb(255, 80, 80) :
                               ((_c_prio == "HIGH") ? make_color_rgb(80, 220, 255) : make_color_rgb(160, 190, 220)));
                draw_text(_col2_x + 20, _cby + 4, "[" + _c_prio + "]  TURN " + _c_turn_val + "  |  " + _c_title);

                // Sender to Recipient
                draw_set_color(make_color_rgb(255, 220, 120));
                var _route_txt = _c_sender + " -> " + _c_recip;
                draw_text(_col2_x + _col2_w - 20 - string_width(_route_txt), _cby + 4, _route_txt);

                // Body snippet
                draw_set_color(c_white);
                draw_text_ext(_col2_x + 20, _cby + 22, _c_body, 16, _col2_w - 44);
            }

            // Cables Paging Controls
            if (_num_cables > _max_vis_cables) {
                var _cp_y = _feed_y + _feed_h - 24;
                var _can_prev_c = (diplo_cables_scroll_offset > 0);
                var _can_next_c = (diplo_cables_scroll_offset + _max_vis_cables < _num_cables);

                if (_can_prev_c && _click && _mx >= _col2_x + 12 && _mx <= _col2_x + 120 && _my >= _cp_y && _my <= _cp_y + 20) {
                    diplo_cables_scroll_offset -= 1;
                }
                if (_can_next_c && _click && _mx >= _col2_x + 130 && _mx <= _col2_x + 240 && _my >= _cp_y && _my <= _cp_y + 20) {
                    diplo_cables_scroll_offset += 1;
                }

                draw_set_color(_can_prev_c ? make_color_rgb(25, 55, 85) : make_color_rgb(14, 20, 28));
                draw_rectangle(_col2_x + 12, _cp_y, _col2_x + 120, _cp_y + 20, false);
                draw_set_color(make_color_rgb(60, 120, 180));
                draw_rectangle(_col2_x + 12, _cp_y, _col2_x + 120, _cp_y + 20, true);
                draw_set_color(c_white);
                draw_text(_col2_x + 24, _cp_y + 2, "[NEWER CABLES]");

                draw_set_color(_can_next_c ? make_color_rgb(25, 55, 85) : make_color_rgb(14, 20, 28));
                draw_rectangle(_col2_x + 130, _cp_y, _col2_x + 240, _cp_y + 20, false);
                draw_set_color(make_color_rgb(60, 120, 180));
                draw_rectangle(_col2_x + 130, _cp_y, _col2_x + 240, _cp_y + 20, true);
                draw_set_color(c_white);
                draw_text(_col2_x + 142, _cp_y + 2, "[OLDER CABLES]");
            }
        }
    }

    // =====================================================================
    // SUBTAB 3: DECADE MECHA LINEAGE & TIMELINE (Y205-Y215)
    // =====================================================================
    else if (war_subtab == 3) {
        var _lx = _pan_x + 24;
        var _ly = _pan_y + 44;
        var _lw = _pan_w - 48;
        var _lh = _pan_h - 56;

        // Top Technical Evolution Artwork Banner
        if (sprite_exists(spr_decade_evolution)) {
            draw_sprite_ext(spr_decade_evolution, 0, _lx + _sx, _ly + _sy, 0.44, 0.44, 0, c_white, 0.92);
        }

        // 1. Dual Filter Bar: Eras and Factions
        var _fil_y = _ly + 155;
        var _eras_lbl = ["ALL ERAS", "Y205 PROTOTYPES", "Y208 EARLY MASS", "Y211 MAINSTAY", "Y213 VARIANTS", "Y215 NEXT-GEN"];
        var _ebw = 175;
        for (var ei = 0; ei < 6; ei++) {
            var _ebx = _lx + ei * (_ebw + 8);
            var _e_act = (selected_timeline_era == ei);
            var _e_hov = (_mx >= _ebx && _mx <= _ebx + _ebw && _my >= _fil_y && _my <= _fil_y + 22);
            if (_e_hov && _click) {
                selected_timeline_era = ei;
                selected_timeline_mech_idx = 0;
                timeline_page = 0;
            }

            draw_set_color(_e_act ? make_color_rgb(40, 80, 130) : (_e_hov ? make_color_rgb(25, 45, 70) : make_color_rgb(14, 20, 28)));
            draw_rectangle(_ebx, _fil_y, _ebx + _ebw, _fil_y + 22, false);
            draw_set_color(_e_act ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 70, 100));
            draw_rectangle(_ebx, _fil_y, _ebx + _ebw, _fil_y + 22, true);
            draw_set_color(_e_act ? c_white : make_color_rgb(170, 195, 220));
            draw_text(_ebx + 8, _fil_y + 4, _eras_lbl[ei]);
        }

        // Faction Filter Bar
        var _fac_fil_y = _fil_y + 26;
        var _facs_lbl = ["ALL FACTIONS (54)", "TERRAN COALITION", "OUTER COLONY LEAGUE", "RIM-SYNDICATE CARTEL", "APEX ZAIBATSU"];
        var _fbw = 210;
        for (var fi = 0; fi < 5; fi++) {
            var _fbx = _lx + fi * (_fbw + 8);
            var _f_act = (timeline_filter_faction == fi);
            var _f_hov = (_mx >= _fbx && _mx <= _fbx + _fbw && _my >= _fac_fil_y && _my <= _fac_fil_y + 22);
            if (_f_hov && _click) {
                timeline_filter_faction = fi;
                selected_timeline_mech_idx = 0;
                timeline_page = 0;
            }

            var _f_btn_col = (_f_act) ? make_color_rgb(60, 90, 120) : (_f_hov ? make_color_rgb(30, 45, 60) : make_color_rgb(12, 18, 26));
            draw_set_color(_f_btn_col);
            draw_rectangle(_fbx, _fac_fil_y, _fbx + _fbw, _fac_fil_y + 22, false);
            draw_set_color(_f_act ? make_color_rgb(255, 200, 80) : make_color_rgb(50, 75, 100));
            draw_rectangle(_fbx, _fac_fil_y, _fbx + _fbw, _fac_fil_y + 22, true);
            draw_set_color(_f_act ? c_white : make_color_rgb(160, 190, 210));
            draw_text(_fbx + 8, _fac_fil_y + 4, _facs_lbl[fi]);
        }

        // Suits Array from obj_FactionManager or database
        var _all_suits = (instance_exists(obj_FactionManager) && array_length(obj_FactionManager.timeline_suits_data) > 0) ? obj_FactionManager.timeline_suits_data : [];

        // Filter Suits by Era and Faction
        var _filtered_suits = [];
        for (var si = 0; si < array_length(_all_suits); si++) {
            var _s = _all_suits[si];
            var _match_era = true;
            if (selected_timeline_era == 1 && _s.era != "Early Prototype") _match_era = false;
            if (selected_timeline_era == 2 && _s.era != "Early Mass Production") _match_era = false;
            if (selected_timeline_era == 3 && _s.era != "Mainstay Mass Production") _match_era = false;
            if (selected_timeline_era == 4 && (_s.era != "Specialized Tactical Variant" && _s.era != "Speciality Ace Suit")) _match_era = false;
            if (selected_timeline_era == 5 && _s.era != "Next-Gen Future Prototype") _match_era = false;

            var _match_fac = true;
            if (timeline_filter_faction == 1 && _s.faction_id != "faction_terran") _match_fac = false;
            if (timeline_filter_faction == 2 && _s.faction_id != "faction_colony") _match_fac = false;
            if (timeline_filter_faction == 3 && _s.faction_id != "faction_syndicate") _match_fac = false;
            if (timeline_filter_faction == 4 && _s.faction_id != "faction_zaibatsu") _match_fac = false;

            if (_match_era && _match_fac) array_push(_filtered_suits, _s);
        }

        // Left Column: Paginated Mech Registry List
        var _list_y = _fac_fil_y + 28;
        var _list_w = 420;
        var _list_h = _lh - (_list_y - _ly);
        draw_set_color(make_color_rgb(8, 14, 20));
        draw_rectangle(_lx, _list_y, _lx + _list_w, _list_y + _list_h, false);
        draw_set_color(make_color_rgb(30, 55, 80));
        draw_rectangle(_lx, _list_y, _lx + _list_w, _list_y + _list_h, true);

        if (selected_timeline_mech_idx >= array_length(_filtered_suits)) selected_timeline_mech_idx = 0;
        var _page_size = 6;
        var _total_pages = max(1, ceil(array_length(_filtered_suits) / _page_size));
        if (timeline_page >= _total_pages) timeline_page = _total_pages - 1;
        if (timeline_page < 0) timeline_page = 0;

        var _start_idx = timeline_page * _page_size;
        var _end_idx = min(_start_idx + _page_size, array_length(_filtered_suits));

        for (var li = _start_idx; li < _end_idx; li++) {
            var _suit = _filtered_suits[li];
            var _card_row = li - _start_idx;
            var _s_card_y = _list_y + 8 + _card_row * 44;
            var _is_cur_s = (selected_timeline_mech_idx == li);
            var _sc_hov = (_mx >= _lx + 8 && _mx <= _lx + _list_w - 8 && _my >= _s_card_y && _my <= _s_card_y + 38);
            if (_sc_hov && _click) selected_timeline_mech_idx = li;

            draw_set_color(_is_cur_s ? make_color_rgb(30, 70, 110) : (_sc_hov ? make_color_rgb(18, 35, 52) : make_color_rgb(12, 20, 28)));
            draw_rectangle(_lx + 8, _s_card_y, _lx + _list_w - 8, _s_card_y + 38, false);
            draw_set_color(_is_cur_s ? make_color_rgb(100, 220, 255) : make_color_rgb(40, 65, 90));
            draw_rectangle(_lx + 8, _s_card_y, _lx + _list_w - 8, _s_card_y + 38, true);

            var _f_col = (_suit.faction_id == "faction_terran") ? make_color_rgb(80, 160, 255) : ((_suit.faction_id == "faction_colony") ? make_color_rgb(40, 220, 180) : ((_suit.faction_id == "faction_syndicate") ? make_color_rgb(255, 140, 40) : make_color_rgb(180, 90, 240)));
            draw_set_color(_f_col);
            draw_circle(_lx + 22, _s_card_y + 19, 6, false);

            draw_set_color(c_white);
            draw_text(_lx + 36, _s_card_y + 5, _suit.name + " (" + string(_suit.year_introduced) + ")");
            draw_set_color(make_color_rgb(160, 190, 220));
            draw_text(_lx + 36, _s_card_y + 20, _suit.era + " // " + _suit.role);
        }

        // Pagination Bar at Bottom of Left Column
        var _pbar_y = _list_y + _list_h - 32;
        draw_set_color(make_color_rgb(10, 16, 24));
        draw_rectangle(_lx + 4, _pbar_y, _lx + _list_w - 4, _pbar_y + 28, false);
        draw_set_color(make_color_rgb(25, 45, 65));
        draw_rectangle(_lx + 4, _pbar_y, _lx + _list_w - 4, _pbar_y + 28, true);

        // Prev Page Button
        var _prev_hov = (_mx >= _lx + 8 && _mx <= _lx + 85 && _my >= _pbar_y + 2 && _my <= _pbar_y + 26);
        if (_prev_hov && _click && timeline_page > 0) {
            timeline_page--;
            selected_timeline_mech_idx = timeline_page * _page_size;
        }
        draw_set_color(_prev_hov ? make_color_rgb(30, 60, 90) : make_color_rgb(16, 28, 42));
        draw_rectangle(_lx + 8, _pbar_y + 2, _lx + 85, _pbar_y + 26, false);
        draw_set_color(_prev_hov ? make_color_rgb(100, 220, 255) : make_color_rgb(40, 70, 100));
        draw_rectangle(_lx + 8, _pbar_y + 2, _lx + 85, _pbar_y + 26, true);
        draw_set_color(timeline_page > 0 ? c_white : c_dkgray);
        draw_text(_lx + 16, _pbar_y + 6, "< PREV");

        // Page Indicator
        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(_lx + 115, _pbar_y + 6, "PAGE " + string(timeline_page + 1) + " / " + string(_total_pages) + " (" + string(array_length(_filtered_suits)) + " SUITS)");

        // Next Page Button
        var _next_hov = (_mx >= _lx + _list_w - 85 && _mx <= _lx + _list_w - 8 && _my >= _pbar_y + 2 && _my <= _pbar_y + 26);
        if (_next_hov && _click && timeline_page < _total_pages - 1) {
            timeline_page++;
            selected_timeline_mech_idx = timeline_page * _page_size;
        }
        draw_set_color(_next_hov ? make_color_rgb(30, 60, 90) : make_color_rgb(16, 28, 42));
        draw_rectangle(_lx + _list_w - 85, _pbar_y + 2, _lx + _list_w - 8, _pbar_y + 26, false);
        draw_set_color(_next_hov ? make_color_rgb(100, 220, 255) : make_color_rgb(40, 70, 100));
        draw_rectangle(_lx + _list_w - 85, _pbar_y + 2, _lx + _list_w - 8, _pbar_y + 26, true);
        draw_set_color(timeline_page < _total_pages - 1 ? c_white : c_dkgray);
        draw_text(_lx + _list_w - 75, _pbar_y + 6, "NEXT >");

        // Mouse Wheel Scroll on List
        if (_mx >= _lx && _mx <= _lx + _list_w && _my >= _list_y && _my <= _list_y + _list_h) {
            if (mouse_wheel_down() && timeline_page < _total_pages - 1) {
                timeline_page++;
                selected_timeline_mech_idx = timeline_page * _page_size;
            }
            if (mouse_wheel_up() && timeline_page > 0) {
                timeline_page--;
                selected_timeline_mech_idx = timeline_page * _page_size;
            }
        }

        // Right Column: Technical Specification Dossier Card
        var _doss_x = _lx + _list_w + 20;
        var _doss_w = _lw - _list_w - 20;
        var _doss_h = _list_h;
        draw_set_color(make_color_rgb(10, 16, 24));
        draw_rectangle(_doss_x, _list_y, _doss_x + _doss_w, _list_y + _doss_h, false);
        draw_set_color(make_color_rgb(35, 60, 90));
        draw_rectangle(_doss_x, _list_y, _doss_x + _doss_w, _list_y + _doss_h, true);

        if (selected_timeline_mech_idx < array_length(_filtered_suits)) {
            var _cur_suit = _filtered_suits[selected_timeline_mech_idx];

            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_doss_x + 20, _list_y + 12, "== " + _cur_suit.name + " [" + _cur_suit.model_code + "] ==");
            draw_set_color(make_color_rgb(240, 210, 100));
            draw_text(_doss_x + 20, _list_y + 32, "YEAR: " + string(_cur_suit.year_introduced) + " // ERA: " + _cur_suit.era + " // ROLE: " + _cur_suit.role);

            // 1. Physical Stature, Metallurgy & Reactor Readout
            var _sy = _list_y + 54;
            draw_set_color(make_color_rgb(170, 215, 255));
            var _ht_str = variable_struct_exists(_cur_suit, "height_meters") ? string(_cur_suit.height_meters) + "m" : "17.5m";
            var _wt_str = variable_struct_exists(_cur_suit, "empty_weight_tonnes") ? (string(_cur_suit.empty_weight_tonnes) + "t Dry / " + string(_cur_suit.combat_weight_tonnes) + "t Sortie") : "45.0t";
            draw_text(_doss_x + 20, _sy, "DIMENSIONS: Height: " + _ht_str + "  //  Mass: " + _wt_str + "  //  Armor: " + string(_cur_suit.armor_rating) + "mm  //  HP: " + string(_cur_suit.structure_hp));

            var _rx_name = variable_struct_exists(_cur_suit, "reactor_type") ? _cur_suit.reactor_type : "Standard Fusion Tokamak";
            draw_set_color(make_color_rgb(255, 215, 130));
            draw_text(_doss_x + 20, _sy + 18, "POWERPLANT: " + _rx_name + " (" + string(_cur_suit.power_output_mw) + " MW)  //  Heat: " + string(_cur_suit.heat_dispersion_rate) + " W/s");

            var _mt_name = variable_struct_exists(_cur_suit, "metal_type") ? _cur_suit.metal_type : "Cast Composite Plating";
            draw_set_color(make_color_rgb(200, 220, 240));
            draw_text(_doss_x + 20, _sy + 36, "METALLURGY: " + _mt_name);

            var _gp_name = variable_struct_exists(_cur_suit, "general_purpose") ? _cur_suit.general_purpose : _cur_suit.role;
            draw_set_color(make_color_rgb(140, 230, 180));
            draw_text(_doss_x + 20, _sy + 54, "DOCTRINE: " + _gp_name + "  //  Speed: " + string(_cur_suit.walk_speed_kph) + " / " + string(_cur_suit.boost_speed_kph) + " kph");

            // 2. Armament List
            var _ay = _sy + 74;
            draw_set_color(make_color_rgb(255, 180, 80));
            draw_text(_doss_x + 20, _ay, "STANDARD WEAPON SUITE:");
            draw_set_color(c_white);
            var _arm_str = "";
            for (var w = 0; w < array_length(_cur_suit.armament); w++) {
                _arm_str += "  [" + string(w+1) + "] " + _cur_suit.armament[w];
            }
            draw_text(_doss_x + 20, _ay + 16, _arm_str);

            // 3. Known Line Variants
            var _vy = _ay + 34;
            if (variable_struct_exists(_cur_suit, "variants") && array_length(_cur_suit.variants) > 0) {
                draw_set_color(make_color_rgb(190, 170, 255));
                draw_text(_doss_x + 20, _vy, "REGISTERED VARIANTS:");
                draw_set_color(make_color_rgb(220, 210, 255));
                var _v_str = "";
                for (var vi = 0; vi < min(4, array_length(_cur_suit.variants)); vi++) {
                    _v_str += "  * " + _cur_suit.variants[vi];
                }
                draw_text(_doss_x + 20, _vy + 16, _v_str);
                _vy += 34;
            }

            // 4. Alloy Material Requirements
            var _aly_y = _vy;
            draw_set_color(make_color_rgb(180, 230, 140));
            draw_text(_doss_x + 20, _aly_y, "ALLOY FORGING REQUISITION:");
            draw_set_color(make_color_rgb(210, 230, 245));
            var _c_al = _cur_suit.alloy_cost;
            var _al_str = "Tungsten: " + string(_c_al.tungsten) + "t  |  Silica: " + string(_c_al.silica) + "t  |  Tritium: " + string(_c_al.tritium) + "t  |  Flux: " + string(_c_al.flux) + "t  |  Slag: " + string(_c_al.slag) + "t";
            draw_text(_doss_x + 20, _aly_y + 16, _al_str);

            // 5. Manufacturing History & Lore
            var _ly_text = _aly_y + 34;
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_doss_x + 20, _ly_text, "HISTORICAL ENGINEERING & MANUFACTURING LORE:");
            draw_set_color(make_color_rgb(180, 210, 240));
            draw_text_ext(_doss_x + 20, _ly_text + 16, _cur_suit.manufacturing_lore, 15, _doss_w - 40);

            // 6. Battlefield Reputation & Combat Logs
            var _rep_y = _ly_text + 58;
            draw_set_color(make_color_rgb(255, 150, 70));
            draw_text(_doss_x + 20, _rep_y, "BATTLEFIELD REPUTATION & COMBAT INTELLIGENCE:");
            draw_set_color(make_color_rgb(230, 215, 195));
            draw_text_ext(_doss_x + 20, _rep_y + 16, _cur_suit.battlefield_reputation, 15, _doss_w - 40);

            // Requisition License Button
            var _lic_y = _list_y + _doss_h - 40;
            var _lic_hov = (_mx >= _doss_x + 20 && _mx <= _doss_x + 360 && _my >= _lic_y && _my <= _lic_y + 30);
            if (_lic_hov && _click) {
                show_toast("BLUEPRINT LICENSE SECURED: " + _cur_suit.name + " available in Workshop!", c_lime);
            }
            draw_set_color(_lic_hov ? make_color_rgb(30, 80, 50) : make_color_rgb(18, 45, 28));
            draw_rectangle(_doss_x + 20, _lic_y, _doss_x + 360, _lic_y + 30, false);
            draw_set_color(make_color_rgb(80, 220, 120));
            draw_rectangle(_doss_x + 20, _lic_y, _doss_x + 360, _lic_y + 30, true);
            draw_set_color(c_white);
            draw_text(_doss_x + 30, _lic_y + 7, "[>> COMMISSION BLUEPRINT LICENSE <<]");
        }
    }

    // =====================================================================
    // SUBTAB 4: PMC EXPEDITIONARY STRIKE & FACTION OVERTHROW (docs/12)
    // =====================================================================
    else if (war_subtab == 4) {
        var _ox = _pan_x + 30;
        var _oy = _pan_y + 44;

        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(_ox, _oy, "== PMC EXPEDITIONARY STRIKE & FACTION OVERTHROW COMMAND ==");
        draw_set_color(make_color_rgb(160, 190, 220));
        draw_text(_ox, _oy + 18, "Command your private military corporation to launch planetary offensives, capture enemy territory, and overthrow rival superpowers!");

        if (instance_exists(obj_FactionManager) && instance_exists(obj_GameManager)) {
            var _fm = obj_FactionManager;
            var _gm = obj_GameManager;
            var _tc = _fm.territory_control;

            // Left Column: Strategic Hegemony & Target Faction Dossiers
            var _col1_w = 560;
            var _col1_h = 580;
            var _col1_y = _oy + 42;

            draw_set_color(make_color_rgb(12, 18, 28));
            draw_rectangle(_ox, _col1_y, _ox + _col1_w, _col1_y + _col1_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_ox, _col1_y, _ox + _col1_w, _col1_y + _col1_h, true);

            // PMC Dominion Status Banner
            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_ox + 16, _col1_y + 12, "SOVEREIGN PMC HEGEMONY STATUS:");

            draw_set_color(make_color_rgb(100, 255, 140));
            draw_text(_ox + 16, _col1_y + 34, "Territory Controlled: " + string(_tc.pmc_pct) + "%   |   Daily Tribute: +" + string(_tc.pmc_pct * 3500) + " Cr/day");
            draw_set_color(c_white);
            draw_text(_ox + 16, _col1_y + 52, "Expeditions Launched: " + string(_fm.pmc_expeditions_launched) + "   |   Sorties Won: " + string(_gm.total_sorties_won) + "   |   Regimes Overthrown: " + string(array_length(_fm.factions_overthrown)) + "/4");

            // 4 Target Faction Cards
            var _f_targets = ["faction_a", "faction_b", "faction_c", "faction_d"];
            var _t_card_y = _col1_y + 80;
            var _t_card_h = 115;

            for (var tf = 0; tf < 4; tf++) {
                var _tfid = _f_targets[tf];
                var _tinfo = variable_struct_get(_fm.factions, _tfid);
                var _is_overthrown = (array_get_index(_fm.factions_overthrown, _tfid) != -1 || _tinfo.military_strength_score <= 0);
                var _is_active_target = (selected_strike_faction == _tfid);
                var _ty_pos = _t_card_y + tf * (_t_card_h + 8);

                var _t_pct = (_tfid == "faction_a") ? _tc.terran_pct : ((_tfid == "faction_b") ? _tc.colony_pct : ((_tfid == "faction_c") ? _tc.syndicate_pct : _tc.zaibatsu_pct));

                draw_set_color(make_color_rgb(16, 24, 36));
                draw_rectangle(_ox + 14, _ty_pos, _ox + _col1_w - 14, _ty_pos + _t_card_h, false);
                draw_set_color(_is_active_target ? make_color_rgb(255, 215, 80) : (_is_overthrown ? make_color_rgb(180, 50, 50) : make_color_rgb(45, 75, 110)));
                draw_rectangle(_ox + 14, _ty_pos, _ox + _col1_w - 14, _ty_pos + _t_card_h, true);

                draw_set_color(make_color_rgb(240, 215, 100));
                draw_text(_ox + 26, _ty_pos + 10, _tinfo.name + " (" + _tinfo.short_name + ")");

                if (_is_overthrown) {
                    draw_set_color(make_color_rgb(255, 80, 80));
                    draw_text(_ox + 26, _ty_pos + 32, "★ REGIME OVERTHROWN & SECTOR ANNEXED ★");
                    draw_set_color(make_color_rgb(180, 180, 180));
                    draw_text(_ox + 26, _ty_pos + 52, "Defenses obliterated. Sovereign territory absorbed into PMC Dominion.");
                } else {
                    draw_set_color(c_white);
                    draw_text(_ox + 26, _ty_pos + 32, "Territory Share: " + string(_t_pct) + "% | Garrison Defense Rating: " + string(_tinfo.military_strength_score));
                    draw_set_color(make_color_rgb(160, 190, 220));
                    draw_text(_ox + 26, _ty_pos + 52, "Alignment: " + _tinfo.alignment);

                    // Target Select Button
                    var _btn_t_y = _ty_pos + 74;
                    var _btn_t_w = 260;
                    var _btn_t_h = 30;
                    var _t_hov = (_mx >= _ox + 26 && _mx <= _ox + 26 + _btn_t_w && _my >= _btn_t_y && _my <= _btn_t_y + _btn_t_h);
                    if (_t_hov && _click) {
                        selected_strike_faction = _tfid;
                    }
                    draw_set_color(_is_active_target ? make_color_rgb(60, 48, 12) : (_t_hov ? make_color_rgb(25, 45, 65) : make_color_rgb(18, 30, 44)));
                    draw_rectangle(_ox + 26, _btn_t_y, _ox + 26 + _btn_t_w, _btn_t_y + _btn_t_h, false);
                    draw_set_color(_is_active_target ? make_color_rgb(255, 215, 80) : make_color_rgb(60, 120, 180));
                    draw_rectangle(_ox + 26, _btn_t_y, _ox + 26 + _btn_t_w, _btn_t_y + _btn_t_h, true);
                    draw_set_color(c_white);
                    draw_text(_ox + 36, _btn_t_y + 7, _is_active_target ? "[DESIGNATED TARGET]" : "[SELECT AS INVASION TARGET]");
                }
            }

            // Right Column: Sortie Task Force Configuration & Offensive Execution
            var _col2_x = _ox + _col1_w + 20;
            var _col2_w = 600;
            var _col2_h = 580;
            draw_set_color(make_color_rgb(12, 18, 28));
            draw_rectangle(_col2_x, _col1_y, _col2_x + _col2_w, _col1_y + _col2_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_col2_x, _col1_y, _col2_x + _col2_w, _col1_y + _col2_h, true);

            var _cur_target = variable_struct_get(_fm.factions, selected_strike_faction);
            var _target_overthrown = (array_get_index(_fm.factions_overthrown, selected_strike_faction) != -1 || _cur_target.military_strength_score <= 0);

            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_col2_x + 18, _col1_y + 12, "TASK FORCE SORTIE DECK // TARGET: " + string_upper(_cur_target.name));

            // Mech Selector
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_col2_x + 18, _col1_y + 40, "1. ASSIGN COMBAT-READY MOBILE SUIT CHASSIS:");

            var _num_mechs = array_length(_gm.inventory.deployable_mechs);
            selected_strike_mech = clamp(selected_strike_mech, 0, max(0, _num_mechs - 1));
            var _assigned_mech = (_num_mechs > 0) ? _gm.inventory.deployable_mechs[selected_strike_mech] : undefined;

            draw_set_color(make_color_rgb(16, 24, 36));
            draw_rectangle(_col2_x + 18, _col1_y + 64, _col2_x + _col2_w - 18, _col1_y + 140, false);
            draw_set_color(make_color_rgb(45, 75, 110));
            draw_rectangle(_col2_x + 18, _col1_y + 64, _col2_x + _col2_w - 18, _col1_y + 140, true);

            if (!is_undefined(_assigned_mech)) {
                var _m_name = variable_struct_get(_assigned_mech, "name") ?? (variable_struct_get(_assigned_mech, "callsign") ?? "Mobile Suit");
                var _m_class = variable_struct_get(_assigned_mech, "class") ?? "Mobile Suit";
                var _m_armor = variable_struct_get(_assigned_mech, "armor_rating") ?? 850;
                var _m_power = variable_struct_get(_assigned_mech, "power_output") ?? 12;
                var _m_status = variable_struct_get(_assigned_mech, "status") ?? "READY";

                draw_set_color(c_white);
                draw_text(_col2_x + 30, _col1_y + 74, "Unit: " + _m_name + " (" + _m_class + ")");
                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text(_col2_x + 30, _col1_y + 94, "Armor Rating: " + string(_m_armor) + " | Reactor Output: " + string(_m_power) + " MW");
                var _m_status_col = (_m_status == "READY") ? c_lime : c_red;
                draw_set_color(_m_status_col);
                draw_text(_col2_x + 30, _col1_y + 114, "Operational Status: " + _m_status);
            } else {
                draw_set_color(c_red);
                draw_text(_col2_x + 30, _col1_y + 90, "NO DEPLOYABLE MOBILE SUITS IN HANGAR!");
            }

            // Mech Cycle Buttons
            var _btn_pm_hov = (_mx >= _col2_x + 420 && _mx <= _col2_x + 490 && _my >= _col1_y + 75 && _my <= _col1_y + 105);
            if (_btn_pm_hov && _click && _num_mechs > 1) {
                selected_strike_mech = (selected_strike_mech - 1 + _num_mechs) % _num_mechs;
            }
            draw_set_color(_btn_pm_hov ? make_color_rgb(30, 60, 90) : make_color_rgb(18, 30, 48));
            draw_rectangle(_col2_x + 420, _col1_y + 75, _col2_x + 490, _col1_y + 105, false);
            draw_set_color(make_color_rgb(80, 180, 255));
            draw_rectangle(_col2_x + 420, _col1_y + 75, _col2_x + 490, _col1_y + 105, true);
            draw_set_color(c_white);
            draw_text(_col2_x + 430, _col1_y + 82, "< PREV");

            var _btn_nm_hov = (_mx >= _col2_x + 505 && _mx <= _col2_x + 575 && _my >= _col1_y + 75 && _my <= _col1_y + 105);
            if (_btn_nm_hov && _click && _num_mechs > 1) {
                selected_strike_mech = (selected_strike_mech + 1) % _num_mechs;
            }
            draw_set_color(_btn_nm_hov ? make_color_rgb(30, 60, 90) : make_color_rgb(18, 30, 48));
            draw_rectangle(_col2_x + 505, _col1_y + 75, _col2_x + 575, _col1_y + 105, false);
            draw_set_color(make_color_rgb(80, 180, 255));
            draw_rectangle(_col2_x + 505, _col1_y + 75, _col2_x + 575, _col1_y + 105, true);
            draw_set_color(c_white);
            draw_text(_col2_x + 515, _col1_y + 82, "NEXT >");

            // Pilot Selector
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_col2_x + 18, _col1_y + 155, "2. ASSIGN ACE SQUADRON COMMANDER:");

            var _num_pilots = array_length(_gm.facilities.roster_pilots);
            selected_strike_pilot = clamp(selected_strike_pilot, 0, max(0, _num_pilots - 1));
            var _assigned_pilot = (_num_pilots > 0) ? _gm.facilities.roster_pilots[selected_strike_pilot] : undefined;

            draw_set_color(make_color_rgb(16, 24, 36));
            draw_rectangle(_col2_x + 18, _col1_y + 178, _col2_x + _col2_w - 18, _col1_y + 252, false);
            draw_set_color(make_color_rgb(45, 75, 110));
            draw_rectangle(_col2_x + 18, _col1_y + 178, _col2_x + _col2_w - 18, _col1_y + 252, true);

            if (!is_undefined(_assigned_pilot)) {
                var _p_ref = variable_struct_get(_assigned_pilot, "character_id") ?? (variable_struct_get(_assigned_pilot, "id") ?? _assigned_pilot);
                scr_draw_composite_portrait(_p_ref, _col2_x + 28, _col1_y + 183, 62, true, "");

                var _p_name = variable_struct_get(_assigned_pilot, "name") ?? "Pilot";
                var _p_call = variable_struct_get(_assigned_pilot, "callsign") ?? "ACE";
                var _p_cstat = variable_struct_get(_assigned_pilot, "combat_stat") ?? floor((variable_struct_get(_assigned_pilot, "accuracy") ?? 80) / 10);
                var _p_tstat = variable_struct_get(_assigned_pilot, "tactics_stat") ?? floor((variable_struct_get(_assigned_pilot, "reflexes") ?? 70) / 10);
                var _p_status = variable_struct_get(_assigned_pilot, "status") ?? "ACTIVE";

                draw_set_color(c_white);
                draw_text(_col2_x + 98, _col1_y + 188, "Pilot: " + _p_name + " (" + _p_call + ")");
                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text(_col2_x + 98, _col1_y + 208, "Combat Rating: " + string(_p_cstat) + " | Tactics Rating: " + string(_p_tstat));
                var _p_status_col = (_p_status == "ACTIVE") ? c_lime : c_red;
                draw_set_color(_p_status_col);
                draw_text(_col2_x + 98, _col1_y + 228, "Deployment Status: " + _p_status);
            } else {
                draw_set_color(c_red);
                draw_text(_col2_x + 30, _col1_y + 208, "NO MERCENARY PILOTS IN ROSTER!");
            }

            // Pilot Cycle Buttons
            var _btn_pp_hov = (_mx >= _col2_x + 420 && _mx <= _col2_x + 490 && _my >= _col1_y + 190 && _my <= _col1_y + 220);
            if (_btn_pp_hov && _click && _num_pilots > 1) {
                selected_strike_pilot = (selected_strike_pilot - 1 + _num_pilots) % _num_pilots;
            }
            draw_set_color(_btn_pp_hov ? make_color_rgb(30, 60, 90) : make_color_rgb(18, 30, 48));
            draw_rectangle(_col2_x + 420, _col1_y + 190, _col2_x + 490, _col1_y + 220, false);
            draw_set_color(make_color_rgb(80, 180, 255));
            draw_rectangle(_col2_x + 420, _col1_y + 190, _col2_x + 490, _col1_y + 220, true);
            draw_set_color(c_white);
            draw_text(_col2_x + 430, _col1_y + 197, "< PREV");

            var _btn_np_hov = (_mx >= _col2_x + 505 && _mx <= _col2_x + 575 && _my >= _col1_y + 190 && _my <= _col1_y + 220);
            if (_btn_np_hov && _click && _num_pilots > 1) {
                selected_strike_pilot = (selected_strike_pilot + 1) % _num_pilots;
            }
            draw_set_color(_btn_np_hov ? make_color_rgb(30, 60, 90) : make_color_rgb(18, 30, 48));
            draw_rectangle(_col2_x + 505, _col1_y + 190, _col2_x + 575, _col1_y + 220, false);
            draw_set_color(make_color_rgb(80, 180, 255));
            draw_rectangle(_col2_x + 505, _col1_y + 190, _col2_x + 575, _col1_y + 220, true);
            draw_set_color(c_white);
            draw_text(_col2_x + 515, _col1_y + 197, "NEXT >");

            // Tactical Calculus & Ratios
            var _calc_y = _col1_y + 270;
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_col2_x + 18, _calc_y, "3. TACTICAL COMBAT CALCULUS & PROJECTION:");

            var _strike_est = 0;
            if (!is_undefined(_assigned_mech) && !is_undefined(_assigned_pilot)) {
                var _m_armor = variable_struct_get(_assigned_mech, "armor_rating") ?? 850;
                var _m_power = variable_struct_get(_assigned_mech, "power_output") ?? 12;
                var _p_cstat = variable_struct_get(_assigned_pilot, "combat_stat") ?? floor((variable_struct_get(_assigned_pilot, "accuracy") ?? 80) / 10);
                _strike_est = _m_armor + _m_power + (_p_cstat * 12);
            }
            var _def_est = _cur_target.military_strength_score * 1.8;

            draw_set_color(c_white);
            draw_text(_col2_x + 30, _calc_y + 24, "Vanguard Strike Power: " + string(_strike_est) + " pts   vs   Enemy Garrison Defense: " + string(_def_est) + " pts");
            draw_set_color(make_color_rgb(100, 255, 140));
            draw_text(_col2_x + 30, _calc_y + 44, "Projected Conquest Yield: +3% to +6% Sovereign Territory | +180,000 to +380,000 Cr Salvage");

            // Big Launch Sortie Button
            var _launch_btn_y = _calc_y + 75;
            var _launch_btn_w = _col2_w - 36;
            var _launch_btn_h = 52;
            var _m_ready = (!is_undefined(_assigned_mech) && (variable_struct_get(_assigned_mech, "status") ?? "READY") == "READY");
            var _p_ready = (!is_undefined(_assigned_pilot) && (variable_struct_get(_assigned_pilot, "status") ?? "ACTIVE") == "ACTIVE");
            var _can_launch = (!_target_overthrown && _m_ready && _p_ready);
            var _l_hov = (_mx >= _col2_x + 18 && _mx <= _col2_x + 18 + _launch_btn_w && _my >= _launch_btn_y && _my <= _launch_btn_y + _launch_btn_h);

            if (_l_hov && _click) {
                if (_target_overthrown) {
                    show_toast("SECTOR ALREADY ANNEXED: Faction regime has already collapsed!", c_yellow);
                } else if (!_can_launch) {
                    show_toast("SORTIE ABORTED: Ensure selected Mech is READY and Pilot is ACTIVE!", c_red);
                } else {
                    _fm.launch_pmc_offensive(selected_strike_faction, selected_strike_mech, selected_strike_pilot);
                }
            }

            draw_set_color(_target_overthrown ? make_color_rgb(25, 35, 45) : (_can_launch ? (_l_hov ? make_color_rgb(110, 30, 20) : make_color_rgb(70, 18, 14)) : make_color_rgb(32, 22, 22)));
            draw_rectangle(_col2_x + 18, _launch_btn_y, _col2_x + 18 + _launch_btn_w, _launch_btn_y + _launch_btn_h, false);
            draw_set_color(_target_overthrown ? make_color_rgb(70, 95, 120) : (_can_launch ? make_color_rgb(255, 90, 70) : make_color_rgb(120, 50, 50)));
            draw_rectangle(_col2_x + 18, _launch_btn_y, _col2_x + 18 + _launch_btn_w, _launch_btn_y + _launch_btn_h, true);

            draw_set_color(c_white);
            if (_target_overthrown) {
                draw_text(_col2_x + 130, _launch_btn_y + 17, "[REGIME COLLAPSED - SECTOR FULLY ANNEXED]");
            } else if (_can_launch) {
                draw_text(_col2_x + 110, _launch_btn_y + 17, ">> COMMENCE PMC STRATEGIC INVASION SORTIE <<");
            } else {
                draw_text(_col2_x + 85, _launch_btn_y + 17, "[SORTIE CRITERIA UNMET: REQUIRE READY MECH & PILOT]");
            }

            // Intel Shift Log Box
            var _log_box_y = _launch_btn_y + 65;
            draw_set_color(make_color_rgb(10, 14, 20));
            draw_rectangle(_col2_x + 18, _log_box_y, _col2_x + _col2_w - 18, _log_box_y + 85, false);
            draw_set_color(make_color_rgb(40, 60, 85));
            draw_rectangle(_col2_x + 18, _log_box_y, _col2_x + _col2_w - 18, _log_box_y + 85, true);

            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_col2_x + 28, _log_box_y + 8, "LATEST THEATER DISPATCH:");
            draw_set_color(c_white);
            draw_text_ext(_col2_x + 28, _log_box_y + 28, _tc.last_shift_report, 20, _col2_w - 56);
        }
    }
}



// -------------------------------------------------------------------------
// TAB 4: PRE-WAR DREADNOUGHT WARSHIP & RIVAL CORPORATE ARMS CONGLOMERATES (Doc 23)
// -------------------------------------------------------------------------
else if (active_tab == 4) {
    var _sub_tabs_fs = [
        "[1. WARSHIP SCHEMATIC & FORGE]",
        "[2. CELESTIAL NAVIGATION & TRANSIT]",
        "[3. RIVAL ARMS CONGLOMERATES]"
    ];
    var _fsub_w = floor((_pan_w - 48) / 3);
    var _fsub_y = _pan_y + 8;
    for (var fst = 0; fst < 3; fst++) {
        var _fstbx = _pan_x + 16 + fst * (_fsub_w + 12);
        var _fstb_act = (flagship_subtab == fst);
        var _fstb_hov = (_mx >= _fstbx && _mx <= _fstbx + _fsub_w && _my >= _fsub_y && _my <= _fsub_y + 28);
        if (_fstb_hov && _click) flagship_subtab = fst;

        draw_set_color(_fstb_act ? make_color_rgb(30, 70, 110) : (_fstb_hov ? make_color_rgb(20, 40, 60) : make_color_rgb(14, 22, 32)));
        draw_rectangle(_fstbx + _sx, _fsub_y + _sy, _fstbx + _fsub_w + _sx, _fsub_y + 28 + _sy, false);
        draw_set_color(_fstb_act ? make_color_rgb(100, 200, 255) : make_color_rgb(45, 75, 110));
        draw_rectangle(_fstbx + _sx, _fsub_y + _sy, _fstbx + _fsub_w + _sx, _fsub_y + 28 + _sy, true);
        draw_set_color(_fstb_act ? c_white : make_color_rgb(160, 190, 220));
        draw_text(_fstbx + 14 + _sx, _fsub_y + 6 + _sy, _sub_tabs_fs[fst]);
    }

    if (instance_exists(obj_GameManager)) {
        var _gm = obj_GameManager;
        var _fs = _gm.flagship;

        // =====================================================================
        // SUBTAB 0: WARSHIP SCHEMATIC, 8-DIVISION REFITS & MASTER PROTOCOLS (Docs 23 & 24)
        // =====================================================================
        if (flagship_subtab == 0) {
            var _fx = _pan_x + 24;
            var _fy = _pan_y + 40;
            var _fw = _pan_w - 48;

            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_fx, _fy, "== PRE-WAR EXPERIMENTAL DREADNOUGHT: " + string_upper(_fs.name) + " (" + _fs.class + ") ==");

            // Origin Lore Banner
            var _lor_y = _fy + 20;
            var _lor_h = 42;
            draw_set_color(make_color_rgb(14, 20, 30));
            draw_rectangle(_fx, _lor_y, _fx + _fw, _lor_y + _lor_h, false);
            draw_set_color(make_color_rgb(40, 70, 105));
            draw_rectangle(_fx, _lor_y, _fx + _fw, _lor_y + _lor_h, true);

            draw_set_color(make_color_rgb(255, 220, 120));
            draw_text(_fx + 12, _lor_y + 4, "SCAVENGER ORIGIN: " + _fs.origin_lore);
            draw_set_color(make_color_rgb(170, 195, 220));
            var _proto_label = (_fs.specialization_protocol == "forge_titan") ? "INDUSTRIAL FORGE TITAN" :
                               ((_fs.specialization_protocol == "siege_fortress") ? "ORBITAL SIEGE FORTRESS" :
                               ((_fs.specialization_protocol == "shadow_panopticon") ? "SHADOW PANOPTICON" : "STANDARD FLEET"));
            draw_text(_fx + 12, _lor_y + 22, "Stationed Orbit: " + _fs.current_sphere + "  |  Hull: " + string(_fs.hull_hp) + " / " + string(_fs.hull_max_hp) + " HP  |  Transit: " + (_fs.transit_turns_left > 0 ? ("En route to " + _fs.destination_sphere + " (" + string(_fs.transit_turns_left) + "T)") : "Stationary") + "  |  Doctrine: " + _proto_label);

            // 4-Category Division Switcher (concise button labels to prevent overflow)
            var _cat_names = [
                "[1. PRODUCTION & HARVEST]",
                "[2. DEFENSE & WEAPONS]",
                "[3. DRIVES & PILOT SUITE]",
                "[4. SIGINT & FLEET COMMAND]"
            ];
            var _cat_w = (_fw - 36) / 4;
            var _cat_y = _lor_y + _lor_h + 8;
            var _cat_h = 28;

            for (var c = 0; c < 4; c++) {
                var _cx = _fx + c * (_cat_w + 12);
                var _is_cat_act = (flagship_division_category == c);
                var _c_hov = (_mx >= _cx && _mx <= _cx + _cat_w && _my >= _cat_y && _my <= _cat_y + _cat_h);
                if (_c_hov && _click) flagship_division_category = c;

                draw_set_color(_is_cat_act ? make_color_rgb(30, 80, 120) : (_c_hov ? make_color_rgb(22, 45, 68) : make_color_rgb(14, 22, 32)));
                draw_rectangle(_cx, _cat_y, _cx + _cat_w, _cat_y + _cat_h, false);
                draw_set_color(_is_cat_act ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 75, 110));
                draw_rectangle(_cx, _cat_y, _cx + _cat_w, _cat_y + _cat_h, true);
                draw_set_color(_is_cat_act ? c_white : make_color_rgb(170, 200, 230));
                draw_text(_cx + 12, _cat_y + 6, _cat_names[c]);
            }

            // All 8 Divisions Data Structure (Docs 23 & 24)
            var _divisions = [
                // Category 0: Production & Harvest
                {
                    id: "fabrication_tier", cat: 0,
                    title: "DIV 1: MOLECULAR FABRICATION CORE", icon: "FOUNDRY",
                    desc: "Nanite sintering crucibles printing mobile suit chassis at atomic scale.",
                    tiers: [
                        "T1: Scrapline Assembler (1 Bay, Standard Print Speed)",
                        "T2: Dual Sintering Bays (2 Bays, -25% Print Time)",
                        "T3: Tri-Core Nanite Crucible (3 Bays, -50% Time, +5% Masterwork)",
                        "T4: Pre-War Archeotech Replicator (4 Bays, -70% Time, +15% Masterwork)",
                        "T5: Omega Sovereign Synthesizer (5 Bays, +25% S-Grade, +15% Armor/Power!)"
                    ],
                    alloys: ["alloy_vanguard_comp", "alloy_aerosteel_flux", "alloy_adamantine_carbide", "alloy_reactive_damascus"],
                    costs: [250000, 600000, 1500000, 3500000]
                },
                {
                    id: "mining_tier", cat: 0,
                    title: "DIV 2: MINING SILLS & DRONE REFINERY", icon: "HARVEST",
                    desc: "Automated extraction shuttles boosting planetary ore yields and refining slag.",
                    tiers: [
                        "T1: Manual Tender Shuttles (+25% Local Planetary Yield)",
                        "T2: Magnetic Harvester Drones (+50% Local Yield, +50% Depot Storage)",
                        "T3: Deep-Core Plasma Tractor (+100% Local Yield, +10% Rare Isotopes)",
                        "T4: Nanite Centrifuge Sieve (+150% Local Yield, Auto-Purify Slag)",
                        "T5: Planetary Siphon Harvester Array (+250% Yield, Passively +15kg Ore/T!)"
                    ],
                    alloys: ["alloy_vanguard_comp", "alloy_hyperion_matrix", "alloy_adamantine_carbide", "alloy_chobham_reactive"],
                    costs: [200000, 500000, 1200000, 3000000]
                },

                // Category 1: Defense & Weapons
                {
                    id: "defense_tier", cat: 1,
                    title: "DIV 3: HULL ARMOR, DEFLECTION & CIWS", icon: "DEFENSE",
                    desc: "Composite bulkheads and point-defense systems repelling pirate outpost raids.",
                    tiers: [
                        "T1: Patchwork Titanium Plating (8,500 Hull HP)",
                        "T2: Twin Flak CIWS (12,000 HP, +25% Pirate Raid Defense Rate)",
                        "T3: Hard-Light Kinetic Deflection (18,000 HP, +50% Pirate Raid Defense)",
                        "T4: Phase Displacement Matrix (26,000 HP, Outpost Mining Raids Nullified)",
                        "T5: Aegis Sovereign Fortress Barrier (40,000 HP, Sol-Wide Raid Immunity!)"
                    ],
                    alloys: ["alloy_vanguard_comp", "alloy_hyperion_matrix", "alloy_adamantine_carbide", "alloy_chobham_reactive"],
                    costs: [180000, 450000, 1100000, 2800000]
                },
                {
                    id: "weapons_tier", cat: 1,
                    title: "DIV 4: SPINAL ARTILLERY & FIRE SUPPORT", icon: "WEAPONS",
                    desc: "Spinal kinetic cannons and particle beams delivering tactical strikes in combat.",
                    tiers: [
                        "T1: Point-Defense Autocannons (No Tactical Bombardment)",
                        "T2: Twin 600mm Mass Drivers (Orbital Strike: 600-1100 Dmg, 3T CD)",
                        "T3: Spinal Particle Lance (High Beam Strike: 1200-1800 Dmg, 2T CD)",
                        "T4: Tungsten Kinetic Rod Array (Catastrophic Rods: 2000-3000 Dmg, 2T CD)",
                        "T5: Doomsday Tachyon Cleaver (Apocalyptic Strike: 3500-5000 Dmg, 1T CD!)"
                    ],
                    alloys: ["alloy_vanguard_comp", "alloy_aerosteel_flux", "alloy_adamantine_carbide", "alloy_reactive_damascus"],
                    costs: [350000, 800000, 2000000, 4500000]
                },

                // Category 2: Drives & Pilots
                {
                    id: "propulsion_tier", cat: 2,
                    title: "DIV 5: PROPULSION & TACHYON FTL DRIVE", icon: "DRIVE",
                    desc: "High-thrust graviton manifolds enabling high-speed planetary transit across Sol.",
                    tiers: [
                        "T1: Ion Thruster Verniers (Standard Sol Transit: 2-3 Turns)",
                        "T2: Fusion-Plasma Drive Manifolds (Reduced Transit: 1-2 Turns)",
                        "T3: Graviton Compression Drive (Rapid Transit: Exactly 1 Turn Across Sol)",
                        "T4: Sub-Space Micro-Warp Drive (1 Turn Transit + Tactical Emergency Warp)",
                        "T5: Tachyon Fold Warp Core (Instantaneous 0-Turn Planetary Transit!)"
                    ],
                    alloys: ["alloy_vanguard_comp", "alloy_aerosteel_flux", "alloy_adamantine_carbide", "alloy_reactive_damascus"],
                    costs: [220000, 550000, 1300000, 3200000]
                },
                {
                    id: "pilot_suite_tier", cat: 2,
                    title: "DIV 6: NEURAL HOLODECKS & MED-BAY", icon: "PILOT",
                    desc: "Cryo-regen pods and neural simulators for pilot training and psychological therapy.",
                    tiers: [
                        "T1: Standard Crew Bunks (Baseline Fatigue Recovery)",
                        "T2: Cryo-Regen Medical Pods (Hospitalized Pilots Recover 2x Faster)",
                        "T3: Neural Link Sync Holodeck (All Roster Pilots Passively +1 Combat Stat/T)",
                        "T4: Cybernetic Neural Calibrator (Genkai Pilot Reflex Limit +20% Evasion)",
                        "T5: Tachyon Mind-Link Nexus (Trauma Therapy: Stabilizes Berserkers to Masters!)"
                    ],
                    alloys: ["alloy_vanguard_comp", "alloy_hyperion_matrix", "alloy_adamantine_carbide", "alloy_chobham_reactive"],
                    costs: [190000, 480000, 1250000, 2900000]
                },

                // Category 3: SIGINT & Fleet Command
                {
                    id: "sigint_tier", cat: 3,
                    title: "DIV 7: SIGINT & EW PANOPTICON ARRAY", icon: "INTEL",
                    desc: "Tachyon sensory globes intercepting transmissions, black-market deals, and rival corps.",
                    tiers: [
                        "T1: Standard System Radar (Basic In-Sphere Tracking)",
                        "T2: Deep-Space Tachyon Dome (Forecasts Pirate Raids 2 Turns Ahead)",
                        "T3: Black-Market Intercept Matrix (15% Market Trade Price Discount)",
                        "T4: Corporate Network Infiltration (Immune to Corporate Counter-Sabotage)",
                        "T5: Prometheus Panopticon Array (Siphons +1% Market Share Every 5 Turns!)"
                    ],
                    alloys: ["alloy_vanguard_comp", "alloy_hyperion_matrix", "alloy_adamantine_carbide", "alloy_reactive_damascus"],
                    costs: [210000, 520000, 1400000, 3400000]
                },
                {
                    id: "command_tier", cat: 3,
                    title: "DIV 8: STRATEGIC COMMAND BRIDGE & CIC", icon: "COMMAND",
                    desc: "Tactical battle coordinator issuing real-time firing coordinates and sovereign edicts.",
                    tiers: [
                        "T1: Makeshift Salvage Bridge (Standard PMC Command Operations)",
                        "T2: Fleet Tactical CIC (+15% Revenue from All PMC Contracts)",
                        "T3: Multi-Wing Sortie Command (Deploy +1 Allied Mobile Suit in Combat)",
                        "T4: Sovereign Warlord War Room (+25% Expedition Success, +50% Daily Tribute)",
                        "T5: Apex Hegemon Command Nexus (Tactical Supremacy: +2 AP & +20% Acc to Units!)"
                    ],
                    alloys: ["alloy_vanguard_comp", "alloy_aerosteel_flux", "alloy_adamantine_carbide", "alloy_reactive_damascus"],
                    costs: [260000, 650000, 1600000, 4000000]
                }
            ];

            // Filter the 2 divisions for current category
            var _cat_divs = [];
            for (var d = 0; d < array_length(_divisions); d++) {
                if (_divisions[d].cat == flagship_division_category) array_push(_cat_divs, _divisions[d]);
            }

            // Render 2 Division Cards Side-by-Side with clear vertical hierarchy
            var _card_y_start = _cat_y + _cat_h + 8;
            var _card_w = (_fw - 16) / 2;
            var _card_h = 245;

            for (var cd = 0; cd < array_length(_cat_divs); cd++) {
                var _div = _cat_divs[cd];
                var _card_x = _fx + cd * (_card_w + 16);
                var _cur_t = variable_struct_get(_fs.upgrades, _div.id) ?? 1;

                draw_set_color(make_color_rgb(10, 16, 24));
                draw_rectangle(_card_x, _card_y_start, _card_x + _card_w, _card_y_start + _card_h, false);
                draw_set_color(make_color_rgb(30, 50, 75));
                draw_rectangle(_card_x, _card_y_start, _card_x + _card_w, _card_y_start + _card_h, true);

                // Division Header & Tier Badge
                draw_set_color(make_color_rgb(255, 215, 80));
                draw_text(_card_x + 14, _card_y_start + 8, _div.title);

                draw_set_color(make_color_rgb(0, 220, 255));
                draw_text(_card_x + _card_w - 110, _card_y_start + 8, "[TIER " + string(_cur_t) + " / 5]");

                // 5 Visual Progression Pips
                var _pip_x_start = _card_x + 14;
                var _pip_y = _card_y_start + 28;
                for (var p = 1; p <= 5; p++) {
                    var _px = _pip_x_start + (p - 1) * 24;
                    var _p_unlocked = (p <= _cur_t);
                    draw_set_color(_p_unlocked ? make_color_rgb(0, 220, 120) : make_color_rgb(25, 35, 45));
                    draw_rectangle(_px, _pip_y, _px + 18, _pip_y + 8, false);
                    draw_set_color(_p_unlocked ? make_color_rgb(140, 255, 180) : make_color_rgb(45, 60, 75));
                    draw_rectangle(_px, _pip_y, _px + 18, _pip_y + 8, true);
                }

                draw_set_color(make_color_rgb(180, 205, 230));
                draw_text_ext(_card_x + 140, _card_y_start + 26, _div.desc, 14, _card_w - 154);

                // 5 Tier Breakdown List with clean vertical spacing
                var _tier_list_y = _card_y_start + 58;
                for (var t = 0; t < 5; t++) {
                    var _t_num = t + 1;
                    var _is_cur = (_t_num == _cur_t);
                    var _is_past = (_t_num < _cur_t);
                    var _prefix = _is_cur ? "▶ " : (_is_past ? "✓ " : "• ");

                    if (_is_cur) {
                        draw_set_color(make_color_rgb(255, 225, 100));
                    } else if (_is_past) {
                        draw_set_color(make_color_rgb(130, 200, 150));
                    } else {
                        draw_set_color(make_color_rgb(120, 140, 160));
                    }
                    draw_text(_card_x + 14, _tier_list_y + t * 21, _prefix + _div.tiers[t]);
                }

                // Upgrade Button & Resource Checks
                var _ub_y = _card_y_start + 192;
                var _can_upg = (_cur_t < 5);

                if (_can_upg) {
                    var _req_c = _div.costs[_cur_t - 1];
                    var _req_a = _div.alloys[_cur_t - 1];
                    var _has_f = (_gm.funds >= _req_c);
                    var _has_a = (_gm.get_alloy(_req_a) >= 5);
                    var _ub_hov = (_mx >= _card_x + 14 && _mx <= _card_x + _card_w - 14 && _my >= _ub_y && _my <= _ub_y + 44);

                    if (_ub_hov && _click && _has_f && _has_a) {
                        _gm.flagship_upgrade(_div.id);
                    }

                    draw_set_color((_has_f && _has_a) ? (_ub_hov ? make_color_rgb(30, 70, 50) : make_color_rgb(18, 40, 28)) : make_color_rgb(18, 22, 28));
                    draw_rectangle(_card_x + 14, _ub_y, _card_x + _card_w - 14, _ub_y + 44, false);
                    draw_set_color((_has_f && _has_a) ? make_color_rgb(80, 220, 120) : make_color_rgb(45, 60, 75));
                    draw_rectangle(_card_x + 14, _ub_y, _card_x + _card_w - 14, _ub_y + 44, true);

                    draw_set_color((_has_f && _has_a) ? c_white : c_gray);
                    draw_text(_card_x + 24, _ub_y + 5, "[★ UPGRADE TO TIER " + string(_cur_t + 1) + "]");
                    draw_set_color((_has_f && _has_a) ? make_color_rgb(200, 255, 200) : c_gray);
                    draw_text(_card_x + 24, _ub_y + 23, "Cost: " + string(_req_c) + " Cr  +  5x " + _req_a + " (Have: " + string(_gm.get_alloy(_req_a)) + ")");
                } else {
                    draw_set_color(make_color_rgb(20, 32, 45));
                    draw_rectangle(_card_x + 14, _ub_y, _card_x + _card_w - 14, _ub_y + 44, false);
                    draw_set_color(make_color_rgb(60, 140, 220));
                    draw_rectangle(_card_x + 14, _ub_y, _card_x + _card_w - 14, _ub_y + 44, true);
                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_card_x + 24, _ub_y + 13, "★ APEX ARCHEOTECH TIER 5 RATIFIED (MAX PROGRESSION)");
                }
            }

            // =================================================================
            // FLAGSHIP SPECIALIZATION PROTOCOLS (MASTER DOCTRINES - Doc 24)
            // =================================================================
            var _t3_count = 0;
            var _chk_tracks = ["fabrication_tier", "mining_tier", "defense_tier", "weapons_tier", "propulsion_tier", "pilot_suite_tier", "sigint_tier", "command_tier"];
            for (var tk = 0; tk < array_length(_chk_tracks); tk++) {
                if ((variable_struct_get(_fs.upgrades, _chk_tracks[tk]) ?? 1) >= 3) _t3_count++;
            }

            var _proto_y = _card_y_start + _card_h + 8;
            var _proto_w = (_fw - 20) / 3;
            var _proto_h = 145;

            draw_set_color(make_color_rgb(255, 220, 100));
            draw_text(_fx, _proto_y, "== FLAGSHIP SPECIALIZATION PROTOCOLS // MASTER ENDGAME DOCTRINES (Requires 4 Divisions at Tier 3+ | Current: " + string(_t3_count) + "/4) ==");

            var _protocols = [
                {
                    id: "forge_titan",
                    name: "PROTOCOL A: INDUSTRIAL FORGE TITAN",
                    desc: "-40% Chassis Fabrication Costs\n+1 Active Manufacturing Bay\n3.0x Planetary Mining Yield Multiplier"
                },
                {
                    id: "siege_fortress",
                    name: "PROTOCOL B: ORBITAL SIEGE FORTRESS",
                    desc: "+50% Orbital Strike Bombardment Dmg\n+25,000 Warship Hull Integrity\n+35% Allied Grid Armor Defense"
                },
                {
                    id: "shadow_panopticon",
                    name: "PROTOCOL C: SHADOW PANOPTICON",
                    desc: "Instant 0-Turn Planetary Tachyon Fold\nNullifies Corporate Sabotage\nSiphons +2% Market Share Every 4T"
                }
            ];

            for (var pr = 0; pr < 3; pr++) {
                var _pdata = _protocols[pr];
                var _px = _fx + pr * (_proto_w + 10);
                var _py = _proto_y + 20;
                var _is_active = (_fs.specialization_protocol == _pdata.id);
                var _unlocked = (_t3_count >= 4);

                var _pb_hov = (_mx >= _px && _mx <= _px + _proto_w && _my >= _py && _my <= _py + _proto_h);
                if (_pb_hov && _click && _unlocked) {
                    _gm.flagship_set_specialization(_pdata.id);
                }

                draw_set_color(_is_active ? make_color_rgb(32, 60, 40) : (_unlocked ? (_pb_hov ? make_color_rgb(24, 40, 56) : make_color_rgb(14, 20, 28)) : make_color_rgb(10, 12, 16)));
                draw_rectangle(_px, _py, _px + _proto_w, _py + _proto_h, false);
                draw_set_color(_is_active ? make_color_rgb(100, 255, 140) : (_unlocked ? make_color_rgb(60, 110, 160) : make_color_rgb(40, 45, 55)));
                draw_rectangle(_px, _py, _px + _proto_w, _py + _proto_h, true);

                draw_set_color(_is_active ? make_color_rgb(255, 220, 100) : (_unlocked ? c_white : c_gray));
                draw_text(_px + 12, _py + 8, _pdata.name);

                draw_set_color(_unlocked ? make_color_rgb(170, 200, 220) : make_color_rgb(100, 110, 120));
                draw_text_ext(_px + 12, _py + 28, _pdata.desc, 17, _proto_w - 24);

                var _btn_y = _py + _proto_h - 32;
                var _badge = _is_active ? "★ [RATIFIED ACTIVE DOCTRINE]" : (_unlocked ? "[CLICK TO RATIFY DOCTRINE]" : "[LOCKED: Requires 4 T3+ Divisions]");
                draw_set_color(_is_active ? make_color_rgb(40, 100, 60) : (_unlocked ? make_color_rgb(18, 50, 75) : make_color_rgb(16, 20, 26)));
                draw_rectangle(_px + 10, _btn_y, _px + _proto_w - 10, _btn_y + 24, false);
                draw_set_color(_is_active ? make_color_rgb(80, 240, 120) : (_unlocked ? make_color_rgb(0, 220, 255) : make_color_rgb(45, 55, 65)));
                draw_rectangle(_px + 10, _btn_y, _px + _proto_w - 10, _btn_y + 24, true);

                draw_set_color(_is_active ? c_white : (_unlocked ? make_color_rgb(180, 240, 255) : c_gray));
                draw_text(_px + 16, _btn_y + 4, _badge);
            }
        }

        // =====================================================================
        // SUBTAB 1: CELESTIAL NAVIGATION & ORBITAL TRANSIT (Doc 23)
        // =====================================================================
        else if (flagship_subtab == 1) {
            var _nx = _pan_x + 24;
            var _ny = _pan_y + 40;
            var _nw = _pan_w - 48;

            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_nx, _ny, "== SOL SYSTEM CELESTIAL NAVIGATION & ORBITAL TRANSIT ==");
            draw_set_color(make_color_rgb(160, 190, 220));
            draw_text(_nx, _ny + 18, "Stationing the USN-X Hephaestus in a planetary sphere boosts local mining yields by +25% to +100% and links fleet fire support.");

            var _spheres_data = [
                { id: "Earth Sphere", name: "Earth Sphere & L-5 Lagrange", desc: "Low Earth orbit industrial habitats and lunar staging bases. Controlled by Terran Coalition." },
                { id: "Martian Sphere", name: "Martian Orbital Sphere", desc: "Phobos garrison yards and Olympus basalt research platforms. High corporate presence." },
                { id: "Asteroid Belt", name: "The Asteroid Belt Fringe", desc: "Ceres hub and Psyche metal spires. Vast mineral veins and Scrapline debris." },
                { id: "Jovian Outer Sphere", name: "Jovian Outer Moon System", desc: "Europa hydrothermal vents and Io volcanic calderas. Stronghold of the Outer Colonies." },
                { id: "Saturnian Outer Sphere", name: "Saturnian Ring Platforms", desc: "Titan methane basins and Enceladus cryo-refineries. Contested industrial outpost." },
                { id: "Deep Solar Frontier", name: "Deep Solar Void & Kuiper Belt", desc: "Derelict shipyards and unpoliced pirate redoubts. Extreme resource hazards." }
            ];

            var _sp_y_start = _ny + 44;
            var _sp_card_h = 76;

            for (var si = 0; si < array_length(_spheres_data); si++) {
                var _spd = _spheres_data[si];
                var _spy = _sp_y_start + si * (_sp_card_h + 8);
                var _is_here = (_fs.current_sphere == _spd.id);
                var _is_target = (_fs.destination_sphere == _spd.id);

                draw_set_color(_is_here ? make_color_rgb(18, 42, 60) : (_is_target ? make_color_rgb(45, 36, 16) : make_color_rgb(10, 16, 24)));
                draw_rectangle(_nx, _spy, _nx + _nw, _spy + _sp_card_h, false);
                draw_set_color(_is_here ? make_color_rgb(0, 220, 255) : (_is_target ? make_color_rgb(255, 180, 40) : make_color_rgb(30, 50, 75)));
                draw_rectangle(_nx, _spy, _nx + _nw, _spy + _sp_card_h, true);

                draw_set_color(c_white);
                draw_text(_nx + 16, _spy + 10, _spd.name);

                var _m_pct = [25, 50, 100, 150, 250][clamp(_fs.upgrades.mining_tier - 1, 0, 4)];
                if (_fs.specialization_protocol == "forge_titan") _m_pct = floor(_m_pct * 1.5);
                var _stat_badge = _is_here ? ("[FLAGSHIP STATIONED HERE - +" + string(_m_pct) + "% ORE BOOST ACTIVE]") :
                                  (_is_target ? ("[TRANSIT IN PROGRESS: " + string(_fs.transit_turns_left) + " TURNS REMAINING]") : "[ORBITAL CONCESSION]");
                draw_set_color(_is_here ? make_color_rgb(0, 240, 255) : (_is_target ? make_color_rgb(255, 200, 50) : make_color_rgb(140, 170, 200)));
                draw_text(_nx + 380, _spy + 10, _stat_badge);

                // Constrain description width so it never touches the transit button
                draw_set_color(make_color_rgb(170, 195, 220));
                draw_text_ext(_nx + 16, _spy + 34, _spd.desc, 16, _nw - 260);

                // Transit Button
                if (!_is_here && !_is_target) {
                    var _tb_x = _nx + _nw - 225;
                    var _tb_y = _spy + 20;
                    var _tb_w = 210;
                    var _tb_h = 36;
                    var _tb_hov = (_mx >= _tb_x && _mx <= _tb_x + _tb_w && _my >= _tb_y && _my <= _tb_y + _tb_h);

                    if (_tb_hov && _click) {
                        _gm.flagship_travel_to(_spd.id);
                    }

                    draw_set_color(_tb_hov ? make_color_rgb(30, 70, 100) : make_color_rgb(18, 38, 55));
                    draw_rectangle(_tb_x, _tb_y, _tb_x + _tb_w, _tb_y + _tb_h, false);
                    var _is_instant = (_fs.upgrades.propulsion_tier >= 5 || _fs.specialization_protocol == "shadow_panopticon");
                    draw_set_color(_is_instant ? make_color_rgb(255, 120, 240) : make_color_rgb(80, 180, 255));
                    draw_rectangle(_tb_x, _tb_y, _tb_x + _tb_w, _tb_y + _tb_h, true);
                    draw_set_color(c_white);
                    draw_text(_tb_x + 14, _tb_y + 10, _is_instant ? "[0-TURN TACHYON FOLD]" : "[ENGAGE TRANSIT DRIVE]");
                }
            }
        }

        // =====================================================================
        // SUBTAB 2: RIVAL CORPORATE ARMS MANUFACTURERS (Doc 23)
        // =====================================================================
        else if (flagship_subtab == 2) {
            var _rx = _pan_x + 24;
            var _ry = _pan_y + 40;
            var _rw = _pan_w - 48;

            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_rx, _ry, "== RIVAL CORPORATE ARMS CONGLOMERATES & SOL MARKET MONOPOLIES ==");

            var _rc = _gm.rival_corporations;

            // Timeline Tech Era Progression Banner (docs/27)
            var _era_y = _ry + 20;
            draw_set_color(make_color_rgb(14, 22, 32));
            draw_rectangle(_rx, _era_y, _rx + _rw, _era_y + 26, false);
            draw_set_color(make_color_rgb(45, 75, 110));
            draw_rectangle(_rx, _era_y, _rx + _rw, _era_y + 26, true);

            if (_gm.timeline_era == 0) {
                draw_set_color(make_color_rgb(255, 200, 50));
                draw_text(_rx + 12, _era_y + 5, "ACTIVE TIMELINE ERA: " + _gm.timeline_era_name + " // THE PROMETHEUS PROTOCOL (NO OTHER MOBILE SUITS EXIST!)");
            } else {
                draw_set_color(make_color_rgb(255, 220, 100));
                draw_text(_rx + 12, _era_y + 5, "ACTIVE TIMELINE ERA: " + _gm.timeline_era_name + " (YEAR " + string(_gm.current_cycle_year) + " // DAY " + string(_gm.current_cycle_day) + ")");
            }

            // 4 Segmented Era Status Indicators
            var _era_w = 110;
            var _era_labels = ["1. EARLY WAR", "2. ESCALATION", "3. TOTAL WAR", "4. APEX CRISIS"];
            for (var er = 0; er < 4; er++) {
                var _er_x = _rx + _rw - 475 + er * (_era_w + 6);
                var _is_cur = (_gm.timeline_era == (er + 1));
                var _is_past = (_gm.timeline_era > (er + 1));
                draw_set_color(_is_cur ? make_color_rgb(20, 60, 85) : (_is_past ? make_color_rgb(12, 36, 20) : make_color_rgb(12, 16, 22)));
                draw_rectangle(_er_x, _era_y + 3, _er_x + _era_w, _era_y + 23, false);
                draw_set_color(_is_cur ? make_color_rgb(100, 240, 255) : (_is_past ? c_lime : make_color_rgb(60, 80, 100)));
                draw_rectangle(_er_x, _era_y + 3, _er_x + _era_w, _era_y + 23, true);
                draw_text(_er_x + 6, _era_y + 5, _era_labels[er]);
            }

            // Sol Market Share & Industrial Monopoly Banner (docs/28)
            var _acquired_count = 0;
            var _r_keys_all = ["corp_vhi", "corp_aod", "corp_rust", "corp_hats"];
            for (var ak = 0; ak < 4; ak++) {
                if (variable_struct_get(_rc, _r_keys_all[ak]).is_acquired) _acquired_count++;
            }
            draw_set_color((_acquired_count == 4) ? make_color_rgb(255, 220, 50) : make_color_rgb(255, 215, 80));
            var _mono_tag = (_acquired_count == 4) ? "  [★ SOL INDUSTRIAL MONOPOLY ACHIEVED ★]" : ("  [MONOPOLY PROGRESS: " + string(_acquired_count) + "/4 ACQUIRED]");
            draw_text(_rx, _era_y + 32, "SOL SYSTEM MARKET SHARE: VHI " + string(_rc.corp_vhi.market_share_pct) + "% | AOD " + string(_rc.corp_aod.market_share_pct) + "% | RUST " + string(_rc.corp_rust.market_share_pct) + "% | HATS " + string(_rc.corp_hats.market_share_pct) + "% | YOUR PMC: " + string(_gm.pmc_market_share_pct) + "%" + _mono_tag);

            // Sol Market Share Bar
            var _mbar_y = _era_y + 50;
            var _mbar_h = 16;
            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_rx, _mbar_y, _rx + _rw, _mbar_y + _mbar_h, false);

            var _vhi_w = (_rw * (_rc.corp_vhi.market_share_pct / 100.0));
            var _aod_w = (_rw * (_rc.corp_aod.market_share_pct / 100.0));
            var _rst_w = (_rw * (_rc.corp_rust.market_share_pct / 100.0));
            var _hat_w = (_rw * (_rc.corp_hats.market_share_pct / 100.0));
            var _pmc_w = (_rw * (_gm.pmc_market_share_pct / 100.0));

            var _cur_bx = _rx;
            draw_set_color(make_color_rgb(60, 130, 240)); draw_rectangle(_cur_bx, _mbar_y, _cur_bx + _vhi_w, _mbar_y + _mbar_h, false); _cur_bx += _vhi_w;
            draw_set_color(make_color_rgb(40, 210, 180)); draw_rectangle(_cur_bx, _mbar_y, _cur_bx + _aod_w, _mbar_y + _mbar_h, false); _cur_bx += _aod_w;
            draw_set_color(make_color_rgb(240, 140, 40)); draw_rectangle(_cur_bx, _mbar_y, _cur_bx + _rst_w, _mbar_y + _mbar_h, false); _cur_bx += _rst_w;
            draw_set_color(make_color_rgb(180, 90, 240)); draw_rectangle(_cur_bx, _mbar_y, _cur_bx + _hat_w, _mbar_y + _mbar_h, false); _cur_bx += _hat_w;
            draw_set_color(make_color_rgb(255, 215, 60)); draw_rectangle(_cur_bx, _mbar_y, min(_rx + _rw, _cur_bx + _pmc_w), _mbar_y + _mbar_h, false);

            draw_set_color(make_color_rgb(45, 75, 110));
            draw_rectangle(_rx, _mbar_y, _rx + _rw, _mbar_y + _mbar_h, true);

            // 4 Corporate Dossiers & Stock Exchange Trading Desks (docs/23, docs/28)
            var _corp_keys = ["corp_vhi", "corp_aod", "corp_rust", "corp_hats"];
            var _cd_y_start = _mbar_y + _mbar_h + 10;
            var _cd_w = (_rw - 16) / 2;
            var _cd_h = 248;

            for (var ci = 0; ci < 4; ci++) {
                var _cid = _corp_keys[ci];
                var _cp = variable_struct_get(_rc, _cid);
                var _col = ci % 2;
                var _row = floor(ci / 2);
                var _cdx = _rx + _col * (_cd_w + 16);
                var _cdy = _cd_y_start + _row * (_cd_h + 10);

                draw_set_color(make_color_rgb(10, 16, 24));
                draw_rectangle(_cdx, _cdy, _cdx + _cd_w, _cdy + _cd_h, false);
                draw_set_color(_cp.is_acquired ? make_color_rgb(180, 140, 40) : make_color_rgb(30, 50, 75));
                draw_rectangle(_cdx, _cdy, _cdx + _cd_w, _cdy + _cd_h, true);

                // Line 1: Header & Stock Price
                draw_set_color(make_color_rgb(255, 215, 80));
                draw_text(_cdx + 14, _cdy + 8, _cp.name + " [" + _cp.ticker + "]");

                if (_cp.is_acquired) {
                    draw_set_color(c_lime);
                    draw_text(_cdx + _cd_w - 220, _cdy + 8, "[100% OWNED SUBSIDIARY]");
                } else {
                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_cdx + _cd_w - 250, _cdy + 8, "Stock: " + string(_cp.share_price_cr) + " Cr/sh | Share: " + string(_cp.market_share_pct) + "%");
                }

                var _cp_cat = variable_struct_exists(_gm.competitor_catalog, _cid) ? variable_struct_get(_gm.competitor_catalog, _cid) : undefined;
                var _b_name = (!is_undefined(_cp_cat)) ? _cp_cat.branch_name : _cp.specialty;
                var _line_suit = (!is_undefined(_cp_cat) && !is_undefined(_cp_cat.active_line_chassis)) ? _cp_cat.active_line_chassis.name : _cp.flagship_chassis;

                // Line 2: CEO & HQ
                draw_set_color(make_color_rgb(170, 195, 220));
                draw_text(_cdx + 14, _cdy + 26, "CEO: " + _cp.ceo + "  |  HQ: " + _cp.hq_location);

                // Line 3: R&D Doctrine & Active Line Chassis
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_cdx + 14, _cdy + 44, "R&D: " + string_copy(_b_name, 1, 14) + " | Line: " + string_copy(_line_suit, 1, 14));

                // Render Animated Mobile Suit Preview for Corporate Dossier (docs/29)
                scr_draw_animated_mobile_suit(_line_suit, _cdx + _cd_w - 55, _cdy + 75, 0.45, -1, "idle");

                // Line 4: Prototype Spec & Player Equity Stake
                var _x_spec_tag = (!is_undefined(_cp_cat) && _cp_cat.has_rare_x_spec && !is_undefined(_cp_cat.rare_x_chassis)) ? ("[X-SPEC] ") : "";
                var _stake_badge = (_cp.player_equity_pct >= 100.0) ? "[ACQUIRED]" :
                                  ((_cp.player_equity_pct >= 51.0) ? "[MAJORITY 51%+]" :
                                  ((_cp.player_equity_pct >= 25.0) ? "[BOARD SEAT]" :
                                  ((_cp.player_equity_pct >= 10.0) ? "[STAKEHOLDER]" : "")));
                var _stk_col = (_cp.player_equity_pct >= 51.0) ? c_lime : ((_cp.player_equity_pct >= 25.0) ? make_color_rgb(100, 220, 255) : make_color_rgb(255, 215, 100));
                draw_set_color(_stk_col);
                draw_text(_cdx + 14, _cdy + 58, _x_spec_tag + "Stake: " + string(_cp.player_shares) + " sh (" + string(_cp.player_equity_pct) + "%) " + _stake_badge + " | +" + string(_cp.dividend_per_turn) + " Cr/T");

                // Prometheus Reverse-Engineering Progress (doc 38)
                var _re_prog = (variable_instance_exists(_gm, "reverse_engineering_progress") && variable_struct_exists(_gm.reverse_engineering_progress, _cid)) ? variable_struct_get(_gm.reverse_engineering_progress, _cid) : 0.0;
                var _re_status = (_re_prog >= 100.0) ? "DEPLOYED" : (_re_prog >= 75.0 ? "Retooling" : (_re_prog >= 50.0 ? "Hybrid" : (_re_prog >= 25.0 ? "Salvage" : "Telemetry")));
                var _re_col = (_re_prog >= 100.0) ? c_red : ((_re_prog >= 50.0) ? make_color_rgb(255, 170, 40) : make_color_rgb(100, 220, 255));
                draw_set_color(_re_col);
                draw_text(_cdx + 14, _cdy + 72, "Reverse-Eng: " + string_format(_re_prog, 1, 1) + "% [" + _re_status + "]");

                // Line 5: Corporate Hostility Gauge
                var _hbar_x = _cdx + 14;
                var _hbar_y = _cdy + 86;
                var _hbar_w = _cd_w - 28;
                var _hbar_h = 8;
                draw_set_color(make_color_rgb(20, 28, 38));
                draw_rectangle(_hbar_x, _hbar_y, _hbar_x + _hbar_w, _hbar_y + _hbar_h, false);

                var _hw = (_hbar_w * (_cp.hostility_pct / 100.0));
                var _hcol = (_cp.hostility_pct >= 75) ? make_color_rgb(255, 60, 60) :
                            ((_cp.hostility_pct >= 40) ? make_color_rgb(255, 170, 40) : make_color_rgb(80, 220, 120));
                draw_set_color(_hcol);
                draw_rectangle(_hbar_x, _hbar_y, _hbar_x + _hw, _hbar_y + _hbar_h, false);

                // Line 6+: Actions Area (Trading Desk or Acquired Subsidiary Seal)
                if (_cp.is_acquired) {
                    var _seal_y = _cdy + 102;
                    var _seal_h = _cd_h - 114;
                    draw_set_color(make_color_rgb(45, 34, 12));
                    draw_rectangle(_cdx + 14, _seal_y, _cdx + _cd_w - 14, _seal_y + _seal_h, false);
                    draw_set_color(make_color_rgb(255, 200, 50));
                    draw_rectangle(_cdx + 14, _seal_y, _cdx + _cd_w - 14, _seal_y + _seal_h, true);

                    draw_set_color(make_color_rgb(255, 225, 80));
                    draw_text(_cdx + 28, _seal_y + 16, "★ SUBSIDIARY OF " + string_upper(_gm.company_name) + " // 100% PMC EQUITY ★");
                    draw_set_color(make_color_rgb(180, 240, 190));
                    draw_text_ext(_cdx + 28, _seal_y + 36, "All Proprietary Blueprints Absorbed  |  +1 Manufacturing Line Bay Unlocked", 14, _cd_w - 56);
                    draw_text_ext(_cdx + 28, _seal_y + 54, "Rival Eliminated from Procurement Trials  |  Full Sol Monopoly Rights Consolidated", 14, _cd_w - 56);
                } else {
                    // Stock Trading Desk Buttons
                    var _btn_y1 = _cdy + 100;
                    var _btn_h = 28;
                    var _btn_w = (_cd_w - 38) / 3;

                    // Button 1: Buy 5% (5,000 sh)
                    var _b1_cost = floor(5000 * _cp.share_price_cr);
                    var _b1_hov = (_mx >= _cdx + 14 && _mx <= _cdx + 14 + _btn_w && _my >= _btn_y1 && _my <= _btn_y1 + _btn_h);
                    if (_b1_hov && _click) _gm.buy_rival_shares(_cid, 5000);
                    draw_set_color(_b1_hov ? make_color_rgb(20, 65, 40) : make_color_rgb(12, 38, 24));
                    draw_rectangle(_cdx + 14, _btn_y1, _cdx + 14 + _btn_w, _btn_y1 + _btn_h, false);
                    draw_set_color(make_color_rgb(60, 220, 120));
                    draw_rectangle(_cdx + 14, _btn_y1, _cdx + 14 + _btn_w, _btn_y1 + _btn_h, true);
                    draw_set_color(c_white);
                    draw_text(_cdx + 18, _btn_y1 + 6, "[BUY 5%] " + string(_b1_cost) + " Cr");

                    // Button 2: Buy 25% (25,000 sh)
                    var _b2_x = _cdx + 14 + _btn_w + 5;
                    var _b2_cost = floor(25000 * _cp.share_price_cr);
                    var _b2_hov = (_mx >= _b2_x && _mx <= _b2_x + _btn_w && _my >= _btn_y1 && _my <= _btn_y1 + _btn_h);
                    if (_b2_hov && _click) _gm.buy_rival_shares(_cid, 25000);
                    draw_set_color(_b2_hov ? make_color_rgb(20, 55, 80) : make_color_rgb(14, 32, 50));
                    draw_rectangle(_b2_x, _btn_y1, _b2_x + _btn_w, _btn_y1 + _btn_h, false);
                    draw_set_color(make_color_rgb(80, 200, 255));
                    draw_rectangle(_b2_x, _btn_y1, _b2_x + _btn_w, _btn_y1 + _btn_h, true);
                    draw_set_color(c_white);
                    draw_text(_b2_x + 8, _btn_y1 + 6, "[BUY 25%] " + string(_b2_cost) + " Cr");

                    // Button 3: Sell 5% (5,000 sh)
                    var _b3_x = _b2_x + _btn_w + 5;
                    var _can_sell = (_cp.player_shares >= 5000);
                    var _b3_hov = (_mx >= _b3_x && _mx <= _b3_x + _btn_w && _my >= _btn_y1 && _my <= _btn_y1 + _btn_h && _can_sell);
                    if (_b3_hov && _click) _gm.sell_rival_shares(_cid, 5000);
                    draw_set_color(_b3_hov ? make_color_rgb(60, 25, 25) : (_can_sell ? make_color_rgb(35, 16, 16) : make_color_rgb(18, 14, 14)));
                    draw_rectangle(_b3_x, _btn_y1, _b3_x + _btn_w, _btn_y1 + _btn_h, false);
                    draw_set_color(_can_sell ? make_color_rgb(255, 100, 80) : make_color_rgb(70, 50, 50));
                    draw_rectangle(_b3_x, _btn_y1, _b3_x + _btn_w, _btn_y1 + _btn_h, true);
                    draw_set_color(_can_sell ? c_white : c_gray);
                    draw_text(_b3_x + 10, _btn_y1 + 6, "[SELL 5%] Cash-Out");

                    // Row 2 Actions: Hostile Takeover / Buyout Bid & Corporate Sabotage
                    var _btn_y2 = _btn_y1 + 33;
                    var _half_act_w = (_cd_w - 33) / 2;

                    // Button 4: Full Hostile Takeover / Buyout Bid
                    var _rem_sh = 100000 - _cp.player_shares;
                    var _tender_val = floor(_rem_sh * _cp.share_price_cr * 1.15);
                    var _can_takeover = (_cp.player_equity_pct >= 51.0 || _gm.funds >= _tender_val);
                    var _to_hov = (_mx >= _cdx + 14 && _mx <= _cdx + 14 + _half_act_w && _my >= _btn_y2 && _my <= _btn_y2 + 34 && _can_takeover);
                    if (_to_hov && _click) _gm.execute_hostile_takeover(_cid);

                    draw_set_color(_to_hov ? make_color_rgb(85, 65, 15) : (_can_takeover ? make_color_rgb(45, 35, 10) : make_color_rgb(20, 18, 14)));
                    draw_rectangle(_cdx + 14, _btn_y2, _cdx + 14 + _half_act_w, _btn_y2 + 34, false);
                    draw_set_color(_can_takeover ? make_color_rgb(255, 205, 50) : make_color_rgb(75, 65, 30));
                    draw_rectangle(_cdx + 14, _btn_y2, _cdx + 14 + _half_act_w, _btn_y2 + 34, true);
                    draw_set_color(_can_takeover ? c_white : c_gray);
                    draw_text(_cdx + 20, _btn_y2 + 9, ">> HOSTILE TAKEOVER BID <<");

                    // Button 5: Launch Corporate Sabotage
                    var _sab_x = _cdx + 14 + _half_act_w + 5;
                    var _sb_hov = (_mx >= _sab_x && _mx <= _sab_x + _half_act_w && _my >= _btn_y2 && _my <= _btn_y2 + 34);
                    if (_sb_hov && _click) _gm.launch_corporate_sabotage(_cid);

                    draw_set_color(_sb_hov ? make_color_rgb(70, 35, 15) : make_color_rgb(38, 20, 10));
                    draw_rectangle(_sab_x, _btn_y2, _sab_x + _half_act_w, _btn_y2 + 34, false);
                    draw_set_color(make_color_rgb(255, 130, 40));
                    draw_rectangle(_sab_x, _btn_y2, _sab_x + _half_act_w, _btn_y2 + 34, true);
                    draw_set_color(c_white);
                    draw_text(_sab_x + 14, _btn_y2 + 9, "[SABOTAGE R&D: -50k Cr]");

                    // Line below buttons: Strategic Perks Notice
                    draw_set_color(make_color_rgb(160, 190, 220));
                    var _perk_note = (_cp.player_equity_pct >= 51.0) ? "Majority Stake active: 10% gross profit royalty extracted per turn & trial veto enabled!" :
                                     ((_cp.player_equity_pct >= 25.0) ? "Board Seat active: +8 PTS Fly-Off trial insight bonus & R&D tree unlocked!" :
                                     ((_cp.player_equity_pct >= 10.0) ? "Stakeholder active: +3 PTS Fly-Off trial insight bonus & steady per-turn dividend!" :
                                     "Acquire 51%+ controlling interest or submit 100% tender offer to initiate hostile buyout."));
                    draw_text_ext(_cdx + 14, _btn_y2 + 40, _perk_note, 14, _cd_w - 28);
                }
            }
        }
    }
}

// 5. TOAST NOTIFICATION OVERLAY
// =========================================================================
if (toast_timer > 0) {
    var _t_alpha = clamp(toast_timer / 30.0, 0, 1);
    var _tw = 580;
    var _th = 36;
    var _tx = (_gw - _tw) / 2;
    var _ty = _gh - 54;

    draw_set_alpha(_t_alpha * 0.9);
    draw_set_color(make_color_rgb(10, 16, 24));
    draw_rectangle(_tx, _ty, _tx + _tw, _ty + _th, false);
    draw_set_color(toast_color);
    draw_rectangle(_tx, _ty, _tx + _tw, _ty + _th, true);
    draw_text(_tx + 20, _ty + 10, toast_message);
    draw_set_alpha(1.0);
}

// =========================================================================
// 6. DYNAMIC NARRATIVE EVENT POPUP MODAL (docs/08_narrative_events.md)
// =========================================================================
if (instance_exists(obj_GameManager) && !is_undefined(obj_GameManager.active_event_popup)) {
    var _ev = obj_GameManager.active_event_popup;
    var _ew = 740;
    var _eh = 460;
    var _ex = (_gw - _ew) / 2;
    var _ey = (_gh - _eh) / 2;

    draw_set_alpha(0.88);
    draw_set_color(c_black);
    draw_rectangle(0, 0, _gw, _gh, false);
    draw_set_alpha(1.0);

    draw_set_color(make_color_rgb(12, 18, 26));
    draw_rectangle(_ex, _ey, _ex + _ew, _ey + _eh, false);
    draw_set_color(make_color_rgb(255, 180, 40));
    draw_rectangle(_ex, _ey, _ex + _ew, _ey + _eh, true);

    draw_set_color(make_color_rgb(255, 200, 60));
    draw_text(_ex + 24, _ey + 20, _ev.title);
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_ex + 24, _ey + 44, "Sender: " + _ev.sender + " // Category: " + _ev.category);

    // Event Description Body Text
    draw_set_color(c_white);
    draw_text_ext(_ex + 24, _ey + 80, _ev.body, 22, _ew - 48);

    // Clickable Choice Options
    var _cy_start = _ey + 210;
    for (var ch = 0; ch < array_length(_ev.choices); ch++) {
        var _choice = _ev.choices[ch];
        var _c_btn_y = _cy_start + ch * 70;
        var _chov = (_mx >= _ex + 24 && _mx <= _ex + _ew - 24 && _my >= _c_btn_y && _my <= _c_btn_y + 56);

        if (_chov && _click) {
            // Apply Mechanical Consequences
            if (variable_struct_exists(_choice, "credits_delta")) obj_GameManager.funds += _choice.credits_delta;
            if (variable_struct_exists(_choice, "standing_terran") && instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_a", _choice.standing_terran);
            if (variable_struct_exists(_choice, "standing_colony") && instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing("faction_b", _choice.standing_colony);
            if (variable_struct_exists(_choice, "pilot")) array_push(obj_GameManager.facilities.roster_pilots, _choice.pilot);
            if (variable_struct_exists(_choice, "market_share_delta")) {
                obj_GameManager.pmc_market_share_pct = min(100, obj_GameManager.pmc_market_share_pct + _choice.market_share_delta);
            }

            var _succ_lbl = variable_struct_exists(_choice, "label") ? _choice.label : "Directive Executed";
            show_toast("COMMAND DIRECTIVE LOGGED: " + _succ_lbl, c_lime);
            obj_GameManager.active_event_popup = undefined;
            break;
        }

        var _clbl = variable_struct_exists(_choice, "label") ? _choice.label : (variable_struct_exists(_choice, "text") ? _choice.text : "SELECT OPTION");
        var _cdesc = variable_struct_exists(_choice, "consequence_desc") ? _choice.consequence_desc : (variable_struct_exists(_choice, "desc") ? _choice.desc : (variable_struct_exists(_choice, "description") ? _choice.description : ""));

        draw_set_color(_chov ? make_color_rgb(30, 60, 90) : make_color_rgb(16, 26, 38));
        draw_rectangle(_ex + 24, _c_btn_y, _ex + _ew - 24, _c_btn_y + 56, false);
        draw_set_color(make_color_rgb(80, 160, 240));
        draw_rectangle(_ex + 24, _c_btn_y, _ex + _ew - 24, _c_btn_y + 56, true);

        draw_set_color(make_color_rgb(240, 210, 100));
        draw_text(_ex + 36, _c_btn_y + 8, _clbl);
        draw_set_color(make_color_rgb(180, 205, 230));
        draw_text_ext(_ex + 36, _c_btn_y + 26, _cdesc, 14, _ew - 72);
    }
}

// =========================================================================
// 7. NODE PIRATE RAID EMERGENCY MODAL (docs/06_resource_operations.md)
// =========================================================================
if (instance_exists(obj_GameManager) && !is_undefined(obj_GameManager.pending_raid)) {
    var _rd = obj_GameManager.pending_raid;
    var _rw = 740;
    var _rh = 340;
    var _rx = (_gw - _rw) / 2;
    var _ry = (_gh - _rh) / 2;

    draw_set_alpha(0.88);
    draw_set_color(c_black);
    draw_rectangle(0, 0, _gw, _gh, false);
    draw_set_alpha(1.0);

    draw_set_color(make_color_rgb(24, 12, 16));
    draw_rectangle(_rx, _ry, _rx + _rw, _ry + _rh, false);
    draw_set_color(c_red);
    draw_rectangle(_rx, _ry, _rx + _rw, _ry + _rh, true);

    draw_set_color(make_color_rgb(255, 80, 80));
    draw_text(_rx + 24, _ry + 20, "== CRITICAL ALERT: RESOURCE CLAIM UNDER ATTACK! ==");
    draw_set_color(c_white);
    draw_text(_rx + 24, _ry + 54, "Target Sector: " + _rd.node_name);
    draw_text(_rx + 24, _ry + 78, "Deployed Escort: " + _rd.assigned_mech + " (Pilot: " + _rd.assigned_pilot + ")");
    draw_text(_rx + 24, _ry + 110, "Hostile pirate skirmishers attempting to loot stored mineral payloads!");

    // Option 1: Sortie Manual Defense (rm_combat)
    var _s1_y = _ry + 160;
    var _s1_hov = (_mx >= _rx + 24 && _mx <= _rx + _rw - 24 && _my >= _s1_y && _my <= _s1_y + 50);
    if (_s1_hov && _click && room_exists(rm_combat)) {
        obj_GameManager.pending_raid = undefined;
        room_goto(rm_combat);
    }
    draw_set_color(_s1_hov ? make_color_rgb(100, 30, 20) : make_color_rgb(50, 16, 12));
    draw_rectangle(_rx + 24, _s1_y, _rx + _rw - 24, _s1_y + 50, false);
    draw_set_color(make_color_rgb(255, 100, 60));
    draw_rectangle(_rx + 24, _s1_y, _rx + _rw - 24, _s1_y + 50, true);
    draw_set_color(c_white);
    draw_text(_rx + 40, _s1_y + 16, ">> 1. SORTIE COMMANDER DEFENSE // TACTICAL GRID (rm_combat) <<");

    // Option 2: Auto-Resolve Defense Gamble
    var _s2_y = _s1_y + 65;
    var _s2_hov = (_mx >= _rx + 24 && _mx <= _rx + _rw - 24 && _my >= _s2_y && _my <= _s2_y + 50);
    if (_s2_hov && _click) {
        // Roll defense roll
        var _def_roll = random(100);
        if (_def_roll > 35) {
            show_toast("ESCORT DEFENDED NODE! RAID REPULSED SUCCESSFULLY!", c_lime);
        } else {
            show_toast("RAIDERS OVERRAN PERIMETER! STORED MATERIALS LOOTED!", c_red);
            var _nidx = _rd.node_index;
            obj_GameManager.nodes[_nidx].current_storage = {};
        }
        obj_GameManager.pending_raid = undefined;
    }
    draw_set_color(_s2_hov ? make_color_rgb(40, 50, 70) : make_color_rgb(20, 26, 38));
    draw_rectangle(_rx + 24, _s2_y, _rx + _rw - 24, _s2_y + 50, false);
    draw_set_color(make_color_rgb(100, 160, 220));
    draw_rectangle(_rx + 24, _s2_y, _rx + _rw - 24, _s2_y + 50, true);
    draw_set_color(c_white);
    draw_text(_rx + 40, _s2_y + 16, ">> 2. ORDER AUTO-RESOLVE DEFENSE (COMBAT SIMULATION GAMBLE) <<");
}


// =========================================================================
// 8. STRATEGIC TURN BRIEFING MODAL (Turn Summary Ledger)
// =========================================================================
if (show_turn_briefing_modal) {
    draw_set_alpha(0.85);
    draw_set_color(c_black);
    draw_rectangle(0, 0, _gw, _gh, false);
    draw_set_alpha(1.0);

    var _mw = 800;
    var _mh = 540;
    var _mx0 = (_gw - _mw) / 2;
    var _my0 = (_gh - _mh) / 2;

    draw_set_color(make_color_rgb(12, 18, 26));
    draw_rectangle(_mx0, _my0, _mx0 + _mw, _my0 + _mh, false);
    draw_set_color(make_color_rgb(80, 180, 255));
    draw_rectangle(_mx0, _my0, _mx0 + _mw, _my0 + _mh, true);

    // Header
    draw_set_color(make_color_rgb(100, 220, 255));
    draw_text(_mx0 + 24, _my0 + 20, "== PMC COMMAND DECK // STRATEGIC TURN BRIEFING LEDGER ==");
    
    // Close Button
    var _cl_w = 140;
    var _cl_hov = (_mx >= _mx0 + _mw - _cl_w - 20 && _mx <= _mx0 + _mw - 20 && _my >= _my0 + 16 && _my <= _my0 + 44);
    if ((_cl_hov && _click) || keyboard_check_pressed(vk_escape)) show_turn_briefing_modal = false;
    draw_set_color(_cl_hov ? make_color_rgb(120, 40, 40) : make_color_rgb(60, 20, 20));
    draw_rectangle(_mx0 + _mw - _cl_w - 20, _my0 + 16, _mx0 + _mw - 20, _my0 + 44, false);
    draw_set_color(c_red);
    draw_rectangle(_mx0 + _mw - _cl_w - 20, _my0 + 16, _mx0 + _mw - 20, _my0 + 44, true);
    draw_set_color(c_white);
    draw_text(_mx0 + _mw - _cl_w - 8, _my0 + 22, "[X CLOSE (ESC)]");

    if (instance_exists(obj_GameManager)) {
        var _gm = obj_GameManager;
        var _t_num = variable_instance_exists(_gm, "current_turn") ? _gm.current_turn : 1;
        draw_set_color(make_color_rgb(255, 210, 100));
        draw_text(_mx0 + 24, _my0 + 52, "STRATEGIC TURN " + string(_t_num) + " // FINANCIAL CYCLE Y" + string(_gm.current_cycle_year) + " D" + string(_gm.current_cycle_day));
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text(_mx0 + 24, _my0 + 74, "TREASURY RESERVES: " + string(_gm.funds) + " CREDITS");

        // Event Ledger Scroll
        draw_set_color(make_color_rgb(8, 12, 18));
        draw_rectangle(_mx0 + 24, _my0 + 104, _mx0 + _mw - 24, _my0 + _mh - 70, false);
        draw_set_color(make_color_rgb(30, 50, 75));
        draw_rectangle(_mx0 + 24, _my0 + 104, _mx0 + _mw - 24, _my0 + _mh - 70, true);

        draw_set_color(make_color_rgb(80, 180, 240));
        draw_text(_mx0 + 36, _my0 + 114, "--- STRATEGIC ACTIVITY LOG (END-OF-TURN TRANSACTIONS) ---");

        var _ev_y = _my0 + 140;
        var _events = variable_instance_exists(_gm, "last_turn_events") ? _gm.last_turn_events : [];
        if (array_length(_events) == 0) {
            draw_set_color(c_gray);
            draw_text(_mx0 + 36, _ev_y, "No events recorded on turn start. Press [SPACE] to advance turns.");
        } else {
            for (var ei = 0; ei < min(11, array_length(_events)); ei++) {
                draw_set_color(make_color_rgb(210, 230, 255));
                draw_text(_mx0 + 36, _ev_y + ei * 24, string_copy(">> " + _events[ei], 1, 88));
            }
        }

        // Advance turn shortcut prompt
        draw_set_color(make_color_rgb(100, 220, 140));
        draw_text(_mx0 + 24, _my0 + _mh - 46, "Press [SPACE] or click top HUD button to simulate next strategic turn.");
    }
}

// =========================================================================
// 9. IN-ENGINE TUTORIAL & FIELD MANUAL MODAL
// =========================================================================
if (active_tutorial_modal != "") {
    var _tw = 980;
    var _th = 600;
    var _tx0 = (_gw - _tw) / 2;
    var _ty0 = (_gh - _th) / 2;

    scr_draw_snes_window_modal(_tx0, _ty0, _tw, _th, "PMC OPERATIONAL MANUAL // TACTICAL ARCHIVE", "SYSTEM TUTORIALS & DOCTRINE SCHEMATICS");

    // Modal Close Button (Top right header)
    var _cl_w = 140;
    var _cl_hov = (_mx >= _tx0 + _tw - _cl_w - 18 && _mx <= _tx0 + _tw - 18 && _my >= _ty0 + 8 && _my <= _ty0 + 34);
    if ((_cl_hov && _click) || keyboard_check_pressed(vk_escape)) active_tutorial_modal = "";
    scr_draw_snes_button(_tx0 + _tw - _cl_w - 18, _ty0 + 8, _cl_w, 26, "[X CLOSE (ESC)]", _cl_hov, false, c_red);

    // Modal Navigation Sub-Tabs (Cleanly positioned on subtab ribbon)
    var _mod_tabs = [
        { id: "PMC_MANUAL", label: "[1. PMC MANUAL]" },
        { id: "CRUCIBLE", label: "[2. CRUCIBLE R&D]" },
        { id: "REACTOR", label: "[3. REACTOR TUNING]" },
        { id: "HYDRAULIC", label: "[4. HYDRAULIC BENCH]" },
        { id: "THRUSTER", label: "[5. PLASMA THRUST]" }
    ];
    var _mtw = floor((_tw - 60) / 5);
    for (var mti = 0; mti < 5; mti++) {
        var _mt_dat = _mod_tabs[mti];
        var _mt_x = _tx0 + 20 + mti * (_mtw + 5);
        var _mt_y = _ty0 + 58;
        var _is_mact = (active_tutorial_modal == _mt_dat.id);
        var _mthov = (_mx >= _mt_x && _mx <= _mt_x + _mtw && _my >= _mt_y && _my <= _mt_y + 26);
        if (_mthov && _click) active_tutorial_modal = _mt_dat.id;

        scr_draw_snes_button(_mt_x, _mt_y, _mtw, 26, _mt_dat.label, _mthov, _is_mact, make_color_rgb(255, 190, 60));
    }

    // Modal Content Body (Cleanly beneath subtabs)
    var _body_x = _tx0 + 20;
    var _body_y = _ty0 + 92;
    var _body_w = _tw - 40;
    var _body_h = _th - 108;

    draw_set_color(make_color_rgb(6, 10, 16));
    draw_rectangle(_body_x, _body_y, _body_x + _body_w, _body_y + _body_h, false);
    draw_set_color(make_color_rgb(30, 50, 75));
    draw_rectangle(_body_x, _body_y, _body_x + _body_w, _body_y + _body_h, true);

    // TUTORIAL CONTENT ROUTING
    if (active_tutorial_modal == "PMC_MANUAL") {
        draw_set_color(make_color_rgb(255, 200, 80));
        draw_text(_body_x + 20, _body_y + 16, "== PMC EXECUTIVE FIELD MANUAL // TURN-BASED STRATEGIC OPERATIONS ==");

        draw_set_color(c_white);
        var _lh = 20;
        var _ty = _body_y + 46;

        draw_text(_body_x + 20, _ty, "1. STRATEGIC PACING & TURN ADVANCEMENT:");
        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(_body_x + 40, _ty + _lh, "- MechMaker is strictly TURN-BASED. Time does not tick down automatically.");
        draw_text(_body_x + 40, _ty + _lh * 2, "- Press [SPACE] or click [>> ADVANCE TURN <<] on the top HUD whenever you are ready.");
        draw_text(_body_x + 40, _ty + _lh * 3, "- Each turn processes mining node extraction, contractor wages, production queues, and pirate raids.");

        draw_set_color(c_white);
        draw_text(_body_x + 20, _ty + _lh * 4.5, "2. THE FOUR PILLARS OF PMC MANAGEMENT:");
        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(_body_x + 40, _ty + _lh * 5.5, "- [TAB 0] R&D LAB: Synthesize custom alloy compounds and calibrate prototype components.");
        draw_text(_body_x + 40, _ty + _lh * 6.5, "- [TAB 1] ASSEMBLY: Deploy mass-production manufacturing runs using refined alloys and blueprints.");
        draw_text(_body_x + 40, _ty + _lh * 7.5, "- [TAB 2] MINING & LOGISTICS: Stake asteroid claims and extract Tungsten, Silica, Tritium, and Flux.");
        draw_text(_body_x + 40, _ty + _lh * 8.5, "- [TAB 3] WAR THEATER: Accept faction contracts from Terran Combine or Colony Alliance.");

        draw_set_color(c_white);
        draw_text(_body_x + 20, _ty + _lh * 10, "3. KEYBOARD SHORTCUTS:");
        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(_body_x + 40, _ty + _lh * 11, "[SPACE] Advance Turn  |  [L] Turn Log  |  [F1/H] PMC Manual  |  [F5] Quick Save  |  [F9] Load");
        draw_text(_body_x + 40, _ty + _lh * 12, "[1 - 5] Direct Tab Switch  |  [ESC] Close Active Modal / Return to Deck");
    }
    else if (active_tutorial_modal == "CRUCIBLE") {
        draw_set_color(make_color_rgb(255, 200, 80));
        draw_text(_body_x + 20, _body_y + 16, "== OPERATING MANUAL: ALLOY SYNTHESIS CRUCIBLE ==");

        draw_set_color(c_white);
        var _lh = 20;
        var _ty = _body_y + 46;

        draw_text(_body_x + 20, _ty, "OBJECTIVE: Synthesize high-grade alloy ingots for mobile suit chassis production.");
        
        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(_body_x + 40, _ty + _lh * 1.5, "1. HOPPER LOADING:");
        draw_text(_body_x + 60, _ty + _lh * 2.5, "- Load elemental precursors into the hopper: Tungsten (T), Silica (S), Tritium (Tr), Flux (F).");
        draw_text(_body_x + 60, _ty + _lh * 3.5, "- Target Recipe: Ironclad Carbide requires 5 Tungsten, 2 Silica, 1 Flux.");
        draw_text(_body_x + 60, _ty + _lh * 4.5, "- Click [PURGE HOPPER] to return elements if loading incorrect materials.");

        draw_text(_body_x + 40, _ty + _lh * 6.0, "2. THERMAL & PRESSURE TUNING:");
        draw_text(_body_x + 60, _ty + _lh * 7.0, "- Use [+400 C HEAT] and [-400 C COOL] to reach target sintering temperature (e.g., 2,800 C).");
        draw_text(_body_x + 60, _ty + _lh * 8.0, "- Use [+800 BAR COMPRESS] and [VENT PRESSURE] to reach target bar rating (e.g., 4,500 bar).");
        draw_text(_body_x + 60, _ty + _lh * 9.0, "- Sintering is discrete: thermal states remain stable until you execute or adjust.");

        draw_text(_body_x + 40, _ty + _lh * 10.5, "3. BATCH EXECUTION:");
        draw_text(_body_x + 60, _ty + _lh * 11.5, "- Click [>> EXECUTE ALLOY SYNTHESIS BATCH <<] to forge the batch into your inventory.");
        draw_text(_body_x + 60, _ty + _lh * 12.5, "- Higher precision yields Masterwork ingots with bonus ballistic and energy deflection!");
    }
    else if (active_tutorial_modal == "REACTOR") {
        draw_set_color(make_color_rgb(255, 200, 80));
        draw_text(_body_x + 20, _body_y + 16, "== OPERATING MANUAL: TOKAMAK HARMONIC CONDUIT TUNER ==");

        draw_set_color(c_white);
        var _lh = 20;
        var _ty = _body_y + 46;

        draw_text(_body_x + 20, _ty, "OBJECTIVE: Align magnetic containment oscillations to achieve Tokamak harmonic synchronization.");

        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(_body_x + 40, _ty + _lh * 1.5, "1. OSCILLOSCOPE INTERPRETATION:");
        draw_text(_body_x + 60, _ty + _lh * 2.5, "- The WHITE wave represents target plasma flux produced by the tokamak core.");
        draw_text(_body_x + 60, _ty + _lh * 3.5, "- The CYAN wave represents your active magnetic containment field.");

        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(_body_x + 40, _ty + _lh * 5.0, "2. THREE CONDUIT CONTROLS:");
        draw_text(_body_x + 60, _ty + _lh * 6.0, "- FREQUENCY (Hz): Adjusts wave compression/periodicity. Match wave peaks across grid.");
        draw_text(_body_x + 60, _ty + _lh * 7.0, "- AMPLITUDE (px): Adjusts wave height/confinement strength. Match target wave peak heights.");
        draw_text(_body_x + 60, _ty + _lh * 8.0, "- PHASE ANGLE (deg): Shifts waveform horizontally to align phase crests and troughs.");

        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(_body_x + 40, _ty + _lh * 9.5, "3. PERFORMANCE TIERS & STAT IMPACT:");
        draw_text(_body_x + 60, _ty + _lh * 10.5, "- S-RANK (>=95%): Flawless Lock! +25% Power Output, +35% Cooling, +20% Energy DMG.");
        draw_text(_body_x + 60, _ty + _lh * 11.5, "- A-RANK (85-94%): Masterwork! +15% Power Output, +20% Cooling, +10% Energy DMG.");
        draw_text(_body_x + 60, _ty + _lh * 12.5, "- B-RANK (70-84%): Fine Precision (+5% Output). C-RANK: Standard Line. D-RANK: -15% Output penalty!");
        draw_text(_body_x + 60, _ty + _lh * 13.5, "- Active tuning automatically binds into custom mobile suits commissioned in Assembly Bay!");
    }
    else if (active_tutorial_modal == "HYDRAULIC") {
        draw_set_color(make_color_rgb(255, 200, 80));
        draw_text(_body_x + 20, _body_y + 16, "== OPERATING MANUAL: HYDRAULIC STRESS BENCH ==");

        draw_set_color(c_white);
        var _lh = 20;
        var _ty = _body_y + 46;

        draw_text(_body_x + 20, _ty, "OBJECTIVE: Balance hydraulic backpressure across all 4 leg joints and weld them into safe tolerance.");

        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(_body_x + 40, _ty + _lh * 1.5, "1. ACTION BUDGET:");
        draw_text(_body_x + 60, _ty + _lh * 2.5, "- You have 8 calibration pulses. Every pressure adjustment or weld consumes 1 pulse.");
        draw_text(_body_x + 60, _ty + _lh * 3.5, "- Click on joint nodes (Hip, Knee, Ankle, Foot) to select them for adjustment.");

        draw_text(_body_x + 40, _ty + _lh * 5.0, "2. PRESSURE DYNAMICS & BACKPRESSURE:");
        draw_text(_body_x + 60, _ty + _lh * 6.0, "- [-16%] RELIEVE PRESSURE: Drops target joint stress by 16%, but adds +4% backpressure to neighbors.");
        draw_text(_body_x + 60, _ty + _lh * 7.0, "- [+14%] TIGHTEN CYLINDER: Increases target joint stress by 14%, relieving -3% from neighbors.");
        draw_text(_body_x + 60, _ty + _lh * 8.0, "- SAFE TOLERANCE BAND: 25.0% to 45.0% (indicated by green zone on the stress gauge).");

        draw_text(_body_x + 40, _ty + _lh * 9.5, "3. GIHREN'S GREED LIMIT (GENKAI) SCALING:");
        draw_text(_body_x + 60, _ty + _lh * 10.5, "- S-RANK (All 4 Locked in budget): Pilot Limit 200%, +30% Recoil, +1 AP.");
        draw_text(_body_x + 60, _ty + _lh * 11.5, "- A-RANK (All 4 Locked): Pilot Limit 175%, +20% Recoil dampening, +15% Armor.");
        draw_text(_body_x + 60, _ty + _lh * 12.5, "- B-RANK: Limit 145%. C-RANK: Limit 115%. D-RANK (<50%): Limit 90% (Bottleneck!).");
        draw_text(_body_x + 60, _ty + _lh * 13.5, "- High Limit lets Ace pilots utilize full Accuracy & Evasion in combat!");
    }
    else if (active_tutorial_modal == "THRUSTER") {
        draw_set_color(make_color_rgb(255, 200, 80));
        draw_text(_body_x + 20, _body_y + 16, "== OPERATING MANUAL: DUAL-VECTOR PLASMA CALIBRATION ==");

        draw_set_color(c_white);
        var _lh = 20;
        var _ty = _body_y + 46;

        draw_text(_body_x + 20, _ty, "OBJECTIVE: Calibrate plasma injection across 4 discrete burn stages for maximum vacuum thrust.");

        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(_body_x + 40, _ty + _lh * 1.5, "1. THE FOUR IGNITION STAGES:");
        draw_text(_body_x + 60, _ty + _lh * 2.5, "- STAGE 1: Ignition Pre-Chamber (Light fuel, gentle magnetic confinement).");
        draw_text(_body_x + 60, _ty + _lh * 3.5, "- STAGE 2: Magnetic Choke Constriction (Moderate fuel, strong magnetic pinch).");
        draw_text(_body_x + 60, _ty + _lh * 4.5, "- STAGE 3: Vernier Acceleration Ring (High fuel, optimized velocity envelope).");
        draw_text(_body_x + 60, _ty + _lh * 5.5, "- STAGE 4: Full Vector Plasma Discharge (Maximum fuel burn, peak magnetic confinement).");

        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(_body_x + 40, _ty + _lh * 7.0, "2. INJECTION & CONFINEMENT TUNING:");
        draw_text(_body_x + 60, _ty + _lh * 8.0, "- Adjust FUEL INJECTION FLOW and MAGNETIC COIL CONFINEMENT to achieve harmonic resonance.");
        draw_text(_body_x + 60, _ty + _lh * 9.0, "- Watch the Stage Resonance bar; you need at least 80% resonance to successfully pulse.");

        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(_body_x + 40, _ty + _lh * 10.5, "3. STAGE RESONANCE & TERRAIN ADAPTABILITY:");
        draw_text(_body_x + 60, _ty + _lh * 11.5, "- S-RANK (Avg >=95%): +35% Booster Thrust, +25% Evasion, Space S-Rank, +35% Fuel.");
        draw_text(_body_x + 60, _ty + _lh * 12.5, "- A-RANK (85-94%): +20% Thrust, +15% Evasion, Space A-Rank, +20% Fuel Efficiency.");
        draw_text(_body_x + 60, _ty + _lh * 13.5, "- B-RANK: +10% Thrust. C-RANK: Baseline. D-RANK: -15% Thrust & flameout penalty.");
    }
}


// =========================================================================
// 8. SID MEIER'S PIRATES-STYLE RETIREMENT & CAREER LEGACY MODAL (docs/12)
// =========================================================================
if (showing_retire_modal && instance_exists(obj_GameManager) && !is_undefined(obj_GameManager.career_summary)) {
    var _csum = (instance_exists(obj_GameManager)) ? obj_GameManager.career_summary : undefined;
    if (!is_undefined(_csum)) {
        // Dim screen backdrop
        draw_set_alpha(0.88);
        draw_set_color(make_color_rgb(6, 10, 16));
        draw_rectangle(0, 0, _gw, _gh, false);
        draw_set_alpha(1.0);

        var _mw = 1200;
        var _mh = 700;
        var _mx_pos = (_gw - _mw) / 2;
        var _my_pos = (_gh - _mh) / 2;

        // Modal Frame
        draw_set_color(make_color_rgb(12, 18, 28));
        draw_rectangle(_mx_pos, _my_pos, _mx_pos + _mw, _my_pos + _mh, false);
        draw_set_color(make_color_rgb(255, 205, 70));
        draw_rectangle(_mx_pos, _my_pos, _mx_pos + _mw, _my_pos + _mh, true);
        draw_rectangle(_mx_pos + 4, _my_pos + 4, _mx_pos + _mw - 4, _my_pos + _mh - 4, true);

        // Header
        draw_set_color(make_color_rgb(255, 215, 80));
        draw_text(_mx_pos + 30, _my_pos + 20, "== MERCENARY GUILD HISTORICAL ARCHIVE // RETIREMENT DOSSIER ==");
        draw_set_color(make_color_rgb(160, 190, 220));
        draw_text(_mx_pos + 30, _my_pos + 42, "Standard Galactic Chronology // Operational Tour Complete // Campaign Duration: " + string(_csum.campaign_days) + " Days");

        // Bestowed Title Banner
        draw_set_color(make_color_rgb(20, 32, 48));
        draw_rectangle(_mx_pos + 30, _my_pos + 66, _mx_pos + _mw - 30, _my_pos + 125, false);
        draw_set_color(make_color_rgb(255, 215, 80));
        draw_rectangle(_mx_pos + 30, _my_pos + 66, _mx_pos + _mw - 30, _my_pos + 125, true);

        draw_set_color(make_color_rgb(255, 225, 100));
        draw_text(_mx_pos + 50, _my_pos + 76, "CAREER ENDING TITLE: ★ " + string_upper(_csum.title) + " ★");
        draw_set_color(make_color_rgb(100, 240, 160));
        draw_text(_mx_pos + 50, _my_pos + 98, "FINAL RATING: " + _csum.rank_grade + "   |   TOTAL SCORE: " + string(_csum.total_score) + " / 10,000 PTS");

        // 6-Category Score Breakdown Grid (2 rows x 3 cols)
        var _sc_names = [
            "1. FINANCIAL EMPIRE",
            "2. TERRITORIAL HEGEMONY",
            "3. INDUSTRIAL MONOPOLY",
            "4. ACE MERCENARY GUILD",
            "5. TECHNOLOGICAL SUPREMACY",
            "6. SUPERPOWERS OVERTHROWN"
        ];
        var _sc_sub = [
            "Net Worth: " + string(_csum.net_worth) + " Cr",
            "Sovereign Territory: " + string(_csum.pmc_territory_pct) + "%",
            "MP Lines Replaced: " + string(_csum.factions_replaced_count) + "/4 (" + string(_csum.total_royalties_collected) + " Cr)",
            "Active Aces: " + string(_csum.pilots_commanded) + " Pilots (" + string(instance_exists(obj_GameManager) ? obj_GameManager.total_sorties_won : 0) + " Wins)",
            "Masterworks Forged: " + string(_csum.masterworks_tuned) + " Prototypes",
            "Regimes Annexed: " + string(_csum.factions_overthrown_count) + " Factions Overthrown"
        ];
        var _sc_pts = [
            _csum.score_wealth,
            _csum.score_territory,
            _csum.score_monopoly,
            _csum.score_guild,
            _csum.score_tech,
            _csum.score_conquest
        ];
        var _sc_max = [2500, 2500, 2000, 1000, 1000, 1000];

        var _col_w = 360;
        var _row_h = 90;
        for (var sc = 0; sc < 6; sc++) {
            var _c_col = sc % 3;
            var _c_row = floor(sc / 3);
            var _scx = _mx_pos + 30 + _c_col * (_col_w + 25);
            var _scy = _my_pos + 138 + _c_row * (_row_h + 10);

            draw_set_color(make_color_rgb(16, 24, 36));
            draw_rectangle(_scx, _scy, _scx + _col_w, _scy + _row_h, false);
            draw_set_color(make_color_rgb(45, 75, 110));
            draw_rectangle(_scx, _scy, _scx + _col_w, _scy + _row_h, true);

            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_scx + 12, _scy + 8, _sc_names[sc]);
            draw_set_color(make_color_rgb(200, 220, 240));
            draw_text(_scx + 12, _scy + 26, _sc_sub[sc]);

            var _pct = clamp(_sc_pts[sc] / _sc_max[sc], 0, 1);
            draw_set_color(make_color_rgb(18, 30, 48));
            draw_rectangle(_scx + 12, _scy + 46, _scx + _col_w - 12, _scy + 56, false);
            draw_set_color(make_color_rgb(80, 210, 140));
            draw_rectangle(_scx + 12, _scy + 46, _scx + 12 + ((_col_w - 24) * _pct), _scy + 56, false);

            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_scx + 12, _scy + 64, "Subtotal: " + string(_sc_pts[sc]) + " / " + string(_sc_max[sc]) + " pts");
        }

        // Historical Chronicle Epilogue Box
        var _epi_y = _my_pos + 355;
        var _epi_w = _mw - 60;
        var _epi_h = 160;
        draw_set_color(make_color_rgb(14, 20, 30));
        draw_rectangle(_mx_pos + 30, _epi_y, _mx_pos + 30 + _epi_w, _epi_y + _epi_h, false);
        draw_set_color(make_color_rgb(60, 95, 140));
        draw_rectangle(_mx_pos + 30, _epi_y, _mx_pos + 30 + _epi_w, _epi_y + _epi_h, true);

        draw_set_color(make_color_rgb(255, 215, 80));
        draw_text(_mx_pos + 46, _epi_y + 12, "HISTORICAL CHRONICLE & STRATEGIC LEGACY:");
        draw_set_color(c_white);
        draw_text_ext(_mx_pos + 46, _epi_y + 36, _csum.epilogue_chronicle, 24, _epi_w - 32);

        // Action Buttons
        var _btn_resume_x = _mx_pos + 120;
        var _btn_resume_y = _my_pos + _mh - 80;
        var _btn_resume_w = 440;
        var _btn_resume_h = 48;
        var _res_hov = (_mx >= _btn_resume_x && _mx <= _btn_resume_x + _btn_resume_w && _my >= _btn_resume_y && _my <= _btn_resume_y + _btn_resume_h);
        if (_res_hov && _click && instance_exists(obj_GameManager)) {
            obj_GameManager.resume_sandbox();
        }
        draw_set_color(_res_hov ? make_color_rgb(25, 95, 55) : make_color_rgb(16, 60, 34));
        draw_rectangle(_btn_resume_x, _btn_resume_y, _btn_resume_x + _btn_resume_w, _btn_resume_y + _btn_resume_h, false);
        draw_set_color(make_color_rgb(60, 240, 120));
        draw_rectangle(_btn_resume_x, _btn_resume_y, _btn_resume_x + _btn_resume_w, _btn_resume_y + _btn_resume_h, true);
        draw_set_color(c_white);
        draw_text(_btn_resume_x + 24, _btn_resume_y + 14, ">> RESUME SANDBOX CAMPAIGN (CONTINUE PLAYING) <<");

        var _btn_close_x = _mx_pos + 640;
        var _btn_close_w = 440;
        var _btn_close_h = 48;
        var _cls_hov = (_mx >= _btn_close_x && _mx <= _btn_close_x + _btn_close_w && _my >= _btn_resume_y && _my <= _btn_resume_y + _btn_close_h);
        if (_cls_hov && _click) {
            showing_retire_modal = false;
            if (instance_exists(obj_GameManager)) obj_GameManager.career_summary = undefined;
            scr_audio_play_ui("cancel");
        }
        draw_set_color(_cls_hov ? make_color_rgb(45, 60, 85) : make_color_rgb(22, 32, 48));
        draw_rectangle(_btn_close_x, _btn_resume_y, _btn_close_x + _btn_close_w, _btn_resume_y + _btn_close_h, false);
        draw_set_color(make_color_rgb(100, 180, 255));
        draw_rectangle(_btn_close_x, _btn_resume_y, _btn_close_x + _btn_close_w, _btn_resume_y + _btn_close_h, true);
        draw_set_color(c_white);
        draw_text(_btn_close_x + 90, _btn_resume_y + 14, "[DISMISS RETIREMENT OVERLAY (ESC)]");
    }
}


// =============================================================================
// INTERACTIVE SITUATION BRIEFING & COMMANDER PROFILE SETUP MODAL
// =============================================================================
if (intro_active || show_commander_modal) {
    // 1. Dark Translucent Overlay
    draw_set_color(c_black);
    draw_set_alpha(0.88);
    draw_rectangle(0, 0, _gw, _gh, false);
    draw_set_alpha(1.0);

    // Modal Canvas Dimensions
    var _mw = min(1140, _gw - 64);
    var _mh = min(680, _gh - 50);
    var _mx0 = (_gw - _mw) / 2;
    var _my0 = (_gh - _mh) / 2;

    // Outer Frame & Recessed Panel
    scr_draw_snes_panel(_mx0, _my0, _mw, _mh, "", -1, false, 0.08);

    // Top Header Banner
    draw_set_color(make_color_rgb(18, 30, 45));
    draw_rectangle(_mx0 + 2, _my0 + 2, _mx0 + _mw - 2, _my0 + 44, false);
    draw_set_color(make_color_rgb(60, 120, 180));
    draw_line(_mx0 + 2, _my0 + 44, _mx0 + _mw - 2, _my0 + 44);

    var _banner_title = (intro_page == 0) ? "TRANSMISSION INTERCEPT // THE SOLAR SCHISM (YEAR 215)" : "PMC EXECUTIVE COMMAND DECK // APPOINT COMMANDER DOSSIER";
    draw_set_color(make_color_rgb(100, 220, 255));
    draw_text(_mx0 + 20, _my0 + 12, _banner_title);

    // Header Subtitle / Page Indicator
    draw_set_color(make_color_rgb(255, 200, 80));
    draw_text(_mx0 + _mw - 260, _my0 + 12, (intro_page == 0) ? "[PHASE 1: SITUATION BRIEFING]" : "[PHASE 2: COMMANDER PROFILE]");

    // -------------------------------------------------------------------------
    // PAGE 0: SITUATION BRIEFING & GAME INTRO
    // -------------------------------------------------------------------------
    if (intro_page == 0) {
        var _bx = _mx0 + 32;
        var _by = _my0 + 64;
        var _bw = _mw - 64;

        // Visual Backdrop Vignette (War Room / Tactical Bridge)
        if (sprite_exists(spr_loc_war_room)) {
            draw_sprite_ext(spr_loc_war_room, 0, _bx, _by, _bw / 1024.0, 160.0 / 576.0, 0, c_white, 0.65);
            draw_set_color(make_color_rgb(80, 180, 255));
            draw_rectangle(_bx, _by, _bx + _bw, _by + 160, true);
        }

        // Overlay Text on Top of Vignette
        draw_set_color(c_black);
        draw_set_alpha(0.65);
        draw_rectangle(_bx, _by + 110, _bx + _bw, _by + 160, false);
        draw_set_alpha(1.0);
        draw_set_color(make_color_rgb(255, 220, 100));
        draw_text(_bx + 16, _by + 118, "CLASSIFIED SOLAR WAR DIRECTIVE // IRON RIDGE DYNAMICS FOUNDING CHARTER");
        draw_set_color(c_white);
        draw_text(_bx + 16, _by + 136, "LOCATION: Experimental Pre-War Dreadnought 'Hephaestus' // Lagrange Point 5");

        // Narrative Sections Grid (4 Monolithic War Factions & Core Directives)
        var _sec_y = _by + 175;
        var _col_w = (_bw - 24) / 2;

        // Left Column: The 4 Solar Factions Locked in Total War
        scr_draw_snes_panel(_bx, _sec_y, _col_w, 320, "== THE FOUR BELLIGERENT FACTIONS ==", 0, false, 0.05);
        
        draw_set_color(make_color_rgb(180, 220, 255));
        var _fy = _sec_y + 40;
        
        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(_bx + 16, _fy, "1. TERRAN COALITION (Earth & Lunar Foundries)");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text_ext(_bx + 16, _fy + 18, "Doctrine: Heavy artillery, 120mm ordnance, dense composite armor plates (Ironclad series).", 14, _col_w - 32);

        _fy += 58;
        draw_set_color(make_color_rgb(100, 255, 180));
        draw_text(_bx + 16, _fy, "2. OUTER COLONY LEAGUE (Jovian High Fleet)");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text_ext(_bx + 16, _fy + 18, "Doctrine: Vernier thrusters, beam rifles, particle beam sabers (Aether interceptors).", 14, _col_w - 32);

        _fy += 58;
        draw_set_color(make_color_rgb(255, 180, 80));
        draw_text(_bx + 16, _fy, "3. RIM-SYNDICATE CARTEL (Asteroid Belt Reavers)");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text_ext(_bx + 16, _fy + 18, "Doctrine: Slag salvagers, heavy rotary flak, grappling claws, harpoon tethers (Hyena raiders).", 14, _col_w - 32);

        _fy += 58;
        draw_set_color(make_color_rgb(220, 140, 255));
        draw_text(_bx + 16, _fy, "4. APEX ZAIBATSU (Corrupted Corporate Monopoly)");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text_ext(_bx + 16, _fy + 18, "Doctrine: Cybernetic neural pilots, plasma blasters, tachyon optics, hostile takeovers.", 14, _col_w - 32);

        // Right Column: Player PMC Operations & Strategic Directives
        scr_draw_snes_panel(_bx + _col_w + 24, _sec_y, _col_w, 320, "== YOUR STRATEGIC PMC CAPABILITIES ==", 1, false, 0.05);

        var _ry = _sec_y + 40;
        draw_set_color(make_color_rgb(255, 220, 100));
        draw_text(_bx + _col_w + 32, _ry, "* METALLURGICAL SINTERING (Crucible)");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text_ext(_bx + _col_w + 32, _ry + 18, "Combine raw ores, flux, and tritium under extreme pressure to forge Vanguard Plating.", 14, _col_w - 48);

        _ry += 58;
        draw_set_color(make_color_rgb(255, 220, 100));
        draw_text(_bx + _col_w + 32, _ry, "* MODULAR CAD MECHA ASSEMBLY (Factory)");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text_ext(_bx + _col_w + 32, _ry + 18, "Fit Heads, Torsos, Arms, Legs, and Weapons across Biped, Hover, Tread, & Aero frames.", 14, _col_w - 48);

        _ry += 58;
        draw_set_color(make_color_rgb(255, 220, 100));
        draw_text(_bx + _col_w + 32, _ry, "* CORPORATE DEFENSE CONTRACTS & FLYOFFS");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text_ext(_bx + _col_w + 32, _ry + 18, "Enter 4-phase corporate design flyoffs to secure lucrative multi-million credit production lines.", 14, _col_w - 48);

        _ry += 58;
        draw_set_color(make_color_rgb(255, 220, 100));
        draw_text(_bx + _col_w + 32, _ry, "* ISOMETRIC TACTICAL COMBAT (24 Theaters)");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text_ext(_bx + _col_w + 32, _ry + 18, "Deploy dual platoons with aimed shot precision; repel rival ace drop-pod incursions.", 14, _col_w - 48);

        // Bottom Navigation Buttons
        var _nav_y = _my0 + _mh - 56;
        var _btn_w = 340;
        var _btn_x = _mx0 + _mw - _btn_w - 32;
        var _btn_hov = (_mx >= _btn_x && _mx <= _btn_x + _btn_w && _my >= _nav_y && _my <= _nav_y + 40);

        if (_btn_hov && _click) {
            intro_page = 1;
            scr_audio_play_ui("click");
        }

        scr_draw_snes_button(_btn_x, _nav_y, _btn_w, 40, ">> APPOINT COMMANDER PROFILE >>", _btn_hov, false, make_color_rgb(100, 220, 255));

        if (show_commander_modal && !intro_active) {
            var _cl_w = 200;
            var _cl_x = _mx0 + 32;
            var _cl_hov = (_mx >= _cl_x && _mx <= _cl_x + _cl_w && _my >= _nav_y && _my <= _nav_y + 40);
            if (_cl_hov && _click) {
                show_commander_modal = false;
                scr_audio_play_ui("cancel");
            }
            scr_draw_snes_button(_cl_x, _nav_y, _cl_w, 40, "[CLOSE DOSSIER]", _cl_hov, false, make_color_rgb(150, 170, 190));
        } else if (intro_active) {
            var _skip_w = 240;
            var _skip_x = _mx0 + 32;
            var _skip_hov = (_mx >= _skip_x && _mx <= _skip_x + _skip_w && _my >= _nav_y && _my <= _nav_y + 40);
            if (_skip_hov && _click) {
                intro_active = false;
                show_commander_modal = false;
                if (instance_exists(obj_GameManager)) obj_GameManager.has_completed_intro = true;
                scr_audio_play_ui("confirm");
                scr_audio_play_location_bgm((active_tab == 0) ? "prototyping" : "hq");
            }
            scr_draw_snes_button(_skip_x, _nav_y, _skip_w, 40, "[SKIP TO COMMAND DECK]", _skip_hov, false, make_color_rgb(140, 170, 200));
        }
    }

    // -------------------------------------------------------------------------
    // PAGE 1: COMMANDER SELECTION DOSSIER (MALE / FEMALE / SILHOUETTE)
    // -------------------------------------------------------------------------
    else if (intro_page == 1) {
        var _cx = _mx0 + 32;
        var _cy = _my0 + 60;
        var _cw = _mw - 64;

        draw_set_color(make_color_rgb(170, 200, 230));
        draw_text(_cx, _cy, "SELECT COMMANDER GENDER PROFILE OR MAINTAIN ANONYMOUS BLACK-BUDGET SILHOUETTE:");

        // 3 Selectable Profile Cards Side-by-Side
        var _card_w = (_cw - 32) / 3;
        var _card_h = 360;
        var _card_y = _cy + 26;

        var _options = [
            {
                id: "silhouette",
                label: "ENCRYPTED SHADOW",
                gender_lbl: "ANONYMOUS / UNKNOWN",
                name: "Commander [CLASSIFIED]",
                callsign: "SHADOW",
                portrait: spr_portrait_commander_silhouette,
                trait: "Black Ops Logistics",
                trait_desc: "+10% Scrap Salvage, Volatility Dampening",
                bio: "Encrypted black-budget mercenary profile operating under an anonymous registry. Identity masked behind electronic warfare scramblers."
            },
            {
                id: "male",
                label: "MALE COMMANDER",
                gender_lbl: "MALE EXECUTIVE",
                name: "Commander Alexei Kane",
                callsign: "RAVEN",
                portrait: spr_portrait_commander_male,
                trait: "Heavy Vanguard",
                trait_desc: "+12% Kinetic Armor, +10% Contract Bounty",
                bio: "Former Terran Naval Strike Commander. Refused orbital saturation orders; founded an independent tactical design bureau."
            },
            {
                id: "female",
                label: "FEMALE COMMANDER",
                gender_lbl: "FEMALE EXECUTIVE",
                name: "Commander Morgan Vance",
                callsign: "VALKYRIE",
                portrait: spr_portrait_commander_female,
                trait: "Vernier Synthesis",
                trait_desc: "+15% Prototyping Stability, +10% Thruster Evasion",
                bio: "Former Colony Fleet Tactical Prodigy. Escaped Jovian corporate conscription to pioneer modular mobile suit metallurgy."
            }
        ];

        for (var ci = 0; ci < 3; ci++) {
            var _opt = _options[ci];
            var _card_x = _cx + ci * (_card_w + 16);
            var _is_sel = (selected_commander_choice == _opt.id);
            var _c_hov = (_mx >= _card_x && _mx <= _card_x + _card_w && _my >= _card_y && _my <= _card_y + _card_h);

            if (_c_hov && _click) {
                selected_commander_choice = _opt.id;
                scr_audio_play_ui("click");
            }

            // Card Panel
            scr_draw_snes_panel(_card_x, _card_y, _card_w, _card_h, _opt.label, _is_sel ? 0 : -1, _is_sel, 0.06);

            // Animated Portrait Canvas (Centered in Card)
            var _p_size = 140;
            var _px = _card_x + (_card_w - _p_size) / 2;
            var _py = _card_y + 36;

            if (sprite_exists(_opt.portrait)) {
                draw_sprite_ext(_opt.portrait, 0, _px, _py, _p_size / 200.0, _p_size / 200.0, 0, c_white, 1.0);
            }
            draw_set_color(_is_sel ? make_color_rgb(100, 220, 255) : make_color_rgb(50, 80, 110));
            draw_rectangle(_px, _py, _px + _p_size, _py + _p_size, true);

            // Name & Callsign
            draw_set_color(_is_sel ? make_color_rgb(255, 220, 100) : c_white);
            draw_text(_card_x + 16, _py + _p_size + 14, _opt.name);
            draw_set_color(make_color_rgb(120, 190, 255));
            draw_text(_card_x + 16, _py + _p_size + 32, "CALLSIGN: [" + _opt.callsign + "] | " + _opt.gender_lbl);

            // Trait
            draw_set_color(make_color_rgb(80, 240, 140));
            draw_text(_card_x + 16, _py + _p_size + 54, "TRAIT: " + _opt.trait);
            draw_set_color(make_color_rgb(160, 190, 215));
            draw_text_ext(_card_x + 16, _py + _p_size + 70, _opt.trait_desc, 14, _card_w - 32);

            // Selection Radio Button
            var _sel_btn_y = _card_y + _card_h - 40;
            var _sel_btn_w = _card_w - 32;
            var _sel_btn_x = _card_x + 16;
            var _s_hov = (_mx >= _sel_btn_x && _mx <= _sel_btn_x + _sel_btn_w && _my >= _sel_btn_y && _my <= _sel_btn_y + 30);
            if (_s_hov && _click) {
                selected_commander_choice = _opt.id;
                scr_audio_play_ui("click");
            }
            scr_draw_snes_button(_sel_btn_x, _sel_btn_y, _sel_btn_w, 30, _is_sel ? "[ ACTIVE SELECTION ]" : "SELECT PROFILE", _s_hov || _is_sel, _is_sel, _is_sel ? make_color_rgb(100, 255, 180) : c_white);
        }

        // Active Bio Description Readout Box (Bottom of Page 1)
        var _bio_y = _card_y + _card_h + 14;
        var _bio_h = 68;
        draw_set_color(make_color_rgb(14, 20, 30));
        draw_rectangle(_cx, _bio_y, _cx + _cw, _bio_y + _bio_h, false);
        draw_set_color(make_color_rgb(45, 80, 120));
        draw_rectangle(_cx, _bio_y, _cx + _cw, _bio_y + _bio_h, true);

        var _cur_choice_data = _options[0];
        if (selected_commander_choice == "male") _cur_choice_data = _options[1];
        else if (selected_commander_choice == "female") _cur_choice_data = _options[2];

        draw_set_color(make_color_rgb(100, 210, 255));
        draw_text(_cx + 16, _bio_y + 8, "EXECUTIVE DOSSIER LOG // " + _cur_choice_data.name + " [" + _cur_choice_data.callsign + "]:");
        draw_set_color(make_color_rgb(200, 220, 240));
        draw_text_ext(_cx + 16, _bio_y + 28, _cur_choice_data.bio, 16, _cw - 32);

        // Confirmation / Back Navigation
        var _nav_y2 = _my0 + _mh - 56;
        
        // Back to Briefing
        var _back_w = 200;
        var _back_hov = (_mx >= _cx && _mx <= _cx + _back_w && _my >= _nav_y2 && _my <= _nav_y2 + 40);
        if (_back_hov && _click) {
            intro_page = 0;
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_cx, _nav_y2, _back_w, 40, "< SITUATION BRIEFING", _back_hov, false, make_color_rgb(150, 180, 210));

        // Confirm & Launch Command Deck
        var _cf_w = 420;
        var _cf_x = _mx0 + _mw - _cf_w - 32;
        var _cf_hov = (_mx >= _cf_x && _mx <= _cf_x + _cf_w && _my >= _nav_y2 && _my <= _nav_y2 + 40);

        if (_cf_hov && _click) {
            if (instance_exists(obj_GameManager)) {
                obj_GameManager.select_commander(selected_commander_choice);
                obj_GameManager.has_completed_intro = true;
            }
            intro_active = false;
            show_commander_modal = false;
            scr_audio_play_ui("confirm");
            scr_audio_play_ui("boot");
            scr_audio_play_location_bgm((active_tab == 0) ? "prototyping" : "hq");
        }
        scr_draw_snes_button(_cf_x, _nav_y2, _cf_w, 40, ">> CONFIRM DOSSIER & INITIALIZE PMC >>", _cf_hov, false, make_color_rgb(60, 240, 140));
    }
}


// =========================================================================
// =========================================================================
// BOTTOM GALACTIC INTEL WIRE (TICKER)
// =========================================================================
var _tick_x = 16;
var _tick_y = _gh - 38;
var _tick_w = _gw - 32;
var _tick_h = 30;

draw_set_color(make_color_rgb(8, 12, 18));
draw_rectangle(_tick_x + _sx, _tick_y + _sy, _tick_x + _tick_w + _sx, _tick_y + _tick_h + _sy, false);
draw_set_color(make_color_rgb(30, 54, 82));
draw_rectangle(_tick_x + _sx, _tick_y + _sy, _tick_x + _tick_w + _sx, _tick_y + _tick_h + _sy, true);

// Glowing Signal Light
draw_set_color(make_color_rgb(0, 240, 255));
draw_rectangle(_tick_x + 4 + _sx, _tick_y + 6 + _sy, _tick_x + 12 + _sx, _tick_y + _tick_h - 6 + _sy, false);

draw_set_color(make_color_rgb(255, 210, 90));
draw_text(_tick_x + 18 + _sx, _tick_y + 7 + _sy, "GALACTIC INTEL WIRE //");

draw_set_color(make_color_rgb(200, 230, 255));
draw_text(_tick_x + 190 + _sx, _tick_y + 7 + _sy, alerts_feed[alert_index]);


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
