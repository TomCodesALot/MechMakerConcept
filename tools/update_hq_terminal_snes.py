import re

FILE_PATH = "objects/obj_HQTerminal/Draw_64.gml"

with open(FILE_PATH, "r") as f:
    code = f.read()

# 1. Update Top HUD Bar (lines 29-134), Navigation Tabs, Alert Ticker, and Main Workspace Panel
old_hud = """// 2. PERSISTENT TOP HUD BAR (Top 10% - docs/09_ui_ux_flow.md)
// =========================================================================
var _hud_h = 64;
draw_set_color(make_color_rgb(14, 20, 28));
draw_rectangle(_sx, _sy, _gw + _sx, _hud_h + _sy, false);
draw_set_color(make_color_rgb(35, 60, 90));
draw_rectangle(_sx, _hud_h - 2 + _sy, _gw + _sx, _hud_h + _sy, false);

// Retrieve Manager Info
var _funds_val = 750000;
var _year_val = 214;
var _day_val = 45;
var _turn_val = 45;
if (instance_exists(obj_GameManager)) {
    _funds_val = obj_GameManager.funds;
    _year_val = obj_GameManager.current_cycle_year;
    _day_val = obj_GameManager.current_cycle_day;
    _turn_val = obj_GameManager.current_turn;
}

// Left Badge
draw_set_color(make_color_rgb(100, 200, 255));
draw_text(24 + _sx, 12 + _sy, "IRON RIDGE PMC // COMMAND DECK");
draw_set_color(make_color_rgb(130, 160, 190));
draw_text(24 + _sx, 32 + _sy, "LICENSED MERCENARY GUILD // TIER-2");

// Treasury Readout
draw_set_color(make_color_rgb(70, 230, 120));
draw_text(340 + _sx, 20 + _sy, "TREASURY: " + string(_funds_val) + " Cr");

// Strategic Turn & Calendar Readout
draw_set_color(make_color_rgb(240, 215, 110));
draw_text(520 + _sx, 20 + _sy, "TURN " + string(_turn_val) + " // Y" + string(_year_val) + " D" + string(_day_val));

// Big Tactile End Turn Button
var _et_x = 730;
var _et_y = 14;
var _et_w = 230;
var _et_h = 36;
var _et_hov = (_mx >= _et_x && _mx <= _et_x + _et_w && _my >= _et_y && _my <= _et_y + _et_h);
if (_et_hov && _click && instance_exists(obj_GameManager)) {
    obj_GameManager.end_turn();
}
draw_set_color(_et_hov ? make_color_rgb(30, 95, 60) : make_color_rgb(18, 52, 32));
draw_rectangle(_et_x + _sx, _et_y + _sy, _et_x + _et_w + _sx, _et_y + _et_h + _sy, false);
draw_set_color(make_color_rgb(60, 240, 120));
draw_rectangle(_et_x + _sx, _et_y + _sy, _et_x + _et_w + _sx, _et_y + _et_h + _sy, true);
draw_set_color(c_white);
draw_text(_et_x + 16 + _sx, _et_y + 9 + _sy, ">> ADVANCE TURN (SPACE) <<");

// Turn Log Button
var _log_btn_x = 974;
var _log_btn_w = 110;
var _log_btn_h = 36;
var _log_hov = (_mx >= _log_btn_x && _mx <= _log_btn_x + _log_btn_w && _my >= _et_y && _my <= _et_y + _log_btn_h);
if (_log_hov && _click) {
    show_turn_briefing_modal = !show_turn_briefing_modal;
}
draw_set_color(_log_hov ? make_color_rgb(35, 60, 90) : make_color_rgb(18, 30, 48));
draw_rectangle(_log_btn_x + _sx, _et_y + _sy, _log_btn_x + _log_btn_w + _sx, _et_y + _log_btn_h + _sy, false);
draw_set_color(make_color_rgb(80, 180, 255));
draw_rectangle(_log_btn_x + _sx, _et_y + _sy, _log_btn_x + _log_btn_w + _sx, _et_y + _log_btn_h + _sy, true);
draw_set_color(c_white);
draw_text(_log_btn_x + 14 + _sx, _et_y + 9 + _sy, "[TURN LOG]");

// Global PMC Manual / Tutorial Button
var _man_btn_x = 1098;
var _man_btn_w = 130;
var _man_btn_h = 36;
var _man_hov = (_mx >= _man_btn_x && _mx <= _man_btn_x + _man_btn_w && _my >= _et_y && _my <= _et_y + _man_btn_h);
if (_man_hov && _click) {
    active_tutorial_modal = (active_tutorial_modal == "PMC_MANUAL") ? "" : "PMC_MANUAL";
}
draw_set_color(_man_hov ? make_color_rgb(70, 50, 20) : make_color_rgb(36, 26, 12));
draw_rectangle(_man_btn_x + _sx, _et_y + _sy, _man_btn_x + _man_btn_w + _sx, _et_y + _man_btn_h + _sy, false);
draw_set_color(make_color_rgb(255, 180, 60));
draw_rectangle(_man_btn_x + _sx, _et_y + _sy, _man_btn_x + _man_btn_w + _sx, _et_y + _man_btn_h + _sy, true);
draw_set_color(c_white);
draw_text(_man_btn_x + 12 + _sx, _et_y + 9 + _sy, "[?] PMC MANUAL");

// Quick Save Button (F5)
var _btn_save_x = 1242;
var _q_btn_w = 86;
var _q_btn_h = 36;
var _s_hov = (_mx >= _btn_save_x && _mx <= _btn_save_x + _q_btn_w && _my >= _et_y && _my <= _et_y + _q_btn_h);
if (_s_hov && _click) scr_save_game();
draw_set_color(_s_hov ? make_color_rgb(20, 60, 40) : make_color_rgb(14, 32, 22));
draw_rectangle(_btn_save_x + _sx, _et_y + _sy, _btn_save_x + _q_btn_w + _sx, _et_y + _q_btn_h + _sy, false);
draw_set_color(make_color_rgb(40, 160, 80));
draw_rectangle(_btn_save_x + _sx, _et_y + _sy, _btn_save_x + _q_btn_w + _sx, _et_y + _q_btn_h + _sy, true);
draw_set_color(make_color_rgb(100, 240, 140));
draw_text(_btn_save_x + 12 + _sx, _et_y + 9 + _sy, "[F5 SAVE]");

// Career Retirement & Legacy Assessment Button (Sid Meier's Pirates Style - docs/12)
var _ret_btn_x = 1342;
var _ret_btn_w = 230;
var _ret_btn_h = 36;
var _ret_hov = (_mx >= _ret_btn_x && _mx <= _ret_btn_x + _ret_btn_w && _my >= _et_y && _my <= _et_y + _ret_btn_h);
if (_ret_hov && _click && instance_exists(obj_GameManager)) {
    obj_GameManager.retire_career();
}
draw_set_color(_ret_hov ? make_color_rgb(70, 50, 10) : make_color_rgb(34, 24, 6));
draw_rectangle(_ret_btn_x + _sx, _et_y + _sy, _ret_btn_x + _ret_btn_w + _sx, _et_y + _ret_btn_h + _sy, false);
draw_set_color(make_color_rgb(255, 205, 70));
draw_rectangle(_ret_btn_x + _sx, _et_y + _sy, _ret_btn_x + _ret_btn_w + _sx, _et_y + _ret_btn_h + _sy, true);
draw_set_color(make_color_rgb(255, 225, 120));
draw_text(_ret_btn_x + 14 + _sx, _et_y + 9 + _sy, "[★ RETIRE CAREER (SCORE)]");
// =========================================================================
// 3. PRIMARY NAVIGATION TABS (y: 68 to 106)
// =========================================================================
var _tabs = [
    "1. R&D LAB // ALLOY & PROTOTYPING",
    "2. FACTORY FLOOR & PERSONNEL",
    "3. CONTRACT BOARD & COMMERCE",
    "4. STRATEGIC WAR MAP",
    "5. DREADNOUGHT // WARSHIP & RIVALS"
];

var _tab_w = (_gw - 48) / 5;
var _tab_y = 68;
var _tab_h = 36;

for (var tb = 0; tb < 5; tb++) {
    var _tbx = 24 + tb * _tab_w;
    var _tb_active = (active_tab == tb);
    var _tb_hov = (_mx >= _tbx && _mx <= _tbx + _tab_w - 6 && _my >= _tab_y && _my <= _tab_y + _tab_h);

    if (_tb_hov && _click) active_tab = tb;

    draw_set_color(_tb_active ? make_color_rgb(24, 48, 76) : (_tb_hov ? make_color_rgb(18, 32, 50) : make_color_rgb(12, 18, 26)));
    draw_rectangle(_tbx + _sx, _tab_y + _sy, _tbx + _tab_w - 6 + _sx, _tab_y + _tab_h + _sy, false);
    draw_set_color(_tb_active ? make_color_rgb(80, 180, 255) : make_color_rgb(40, 70, 105));
    draw_rectangle(_tbx + _sx, _tab_y + _sy, _tbx + _tab_w - 6 + _sx, _tab_y + _tab_h + _sy, true);

    if (_tb_active) {
        draw_set_color(make_color_rgb(100, 220, 255));
        draw_rectangle(_tbx + _sx, _tab_y + _tab_h - 3 + _sy, _tbx + _tab_w - 6 + _sx, _tab_y + _tab_h + _sy, false);
    }

    draw_set_color(_tb_active ? c_white : make_color_rgb(170, 195, 220));
    draw_text(_tbx + 16 + _sx, _tab_y + 9 + _sy, _tabs[tb]);
}

// Alert Ticker Banner (y: 108 to 126)
draw_set_color(make_color_rgb(8, 12, 18));
draw_rectangle(24 + _sx, 108 + _sy, _gw - 24 + _sx, 126 + _sy, false);
draw_set_color(make_color_rgb(180, 210, 120));
draw_text(32 + _sx, 110 + _sy, ">> INTEL FEED: " + alerts_feed[alert_index]);

// =========================================================================
// 4. MAIN WORKSPACE PANELS (y: 132 to _gh - 30)
// =========================================================================
var _pan_x = 24;
var _pan_y = 132;
var _pan_w = _gw - 48;
var _pan_h = _gh - _pan_y - 36;

draw_set_color(make_color_rgb(12, 18, 26));
draw_rectangle(_pan_x + _sx, _pan_y + _sy, _pan_x + _pan_w + _sx, _pan_y + _pan_h + _sy, false);
draw_set_color(make_color_rgb(30, 50, 75));
draw_rectangle(_pan_x + _sx, _pan_y + _sy, _pan_x + _pan_w + _sx, _pan_y + _pan_h + _sy, true);"""

new_hud = """// 2. PERSISTENT TOP HUD BAR (Top 10% - docs/09_ui_ux_flow.md)
// =========================================================================
var _hud_h = 64;
// Authentic 16-bit Front Mission military command deck casing with scanlines
scr_draw_snes_panel(_sx, _sy, _gw, _hud_h, "", -1, false, 0.04);

// Retrieve Manager Info
var _funds_val = 750000;
var _year_val = 214;
var _day_val = 45;
var _turn_val = 45;
if (instance_exists(obj_GameManager)) {
    _funds_val = obj_GameManager.funds;
    _year_val = obj_GameManager.current_cycle_year;
    _day_val = obj_GameManager.current_cycle_day;
    _turn_val = obj_GameManager.current_turn;
}

// Left Badge with 16-bit status LED
if (sprite_exists(spr_snes_led_indicators)) {
    draw_sprite(spr_snes_led_indicators, 0, 16 + _sx, 16 + _sy);
}
draw_set_color(make_color_rgb(120, 220, 255));
draw_text(38 + _sx, 12 + _sy, "IRON RIDGE PMC // COMMAND DECK");
draw_set_color(make_color_rgb(140, 175, 205));
draw_text(38 + _sx, 32 + _sy, "[ TAC-COM MERCENARY GUILD // TIER-2 ]");

// Treasury Readout - 16-bit Recessed Backlit Digital Meter
var _tr_x = 246 + _sx;
var _tr_y = 14 + _sy;
var _tr_w = 146;
var _tr_h = 36;
draw_set_color(make_color_rgb(8, 14, 10));
draw_rectangle(_tr_x, _tr_y, _tr_x + _tr_w, _tr_y + _tr_h, false);
draw_set_color(make_color_rgb(25, 60, 40));
draw_rectangle(_tr_x, _tr_y, _tr_x + _tr_w, _tr_y + _tr_h, true);
draw_set_color(make_color_rgb(60, 240, 120));
draw_text(_tr_x + 8, _tr_y + 4, "TREASURY:");
draw_set_color(make_color_rgb(140, 255, 170));
draw_text(_tr_x + 8, _tr_y + 18, string(_funds_val) + " Cr");

// Strategic Turn & Calendar Readout - 16-bit Recessed Backlit Digital Meter
var _cal_x = 402 + _sx;
var _cal_y = 14 + _sy;
var _cal_w = 160;
var _cal_h = 36;
draw_set_color(make_color_rgb(14, 12, 6));
draw_rectangle(_cal_x, _cal_y, _cal_x + _cal_w, _cal_y + _cal_h, false);
draw_set_color(make_color_rgb(70, 55, 20));
draw_rectangle(_cal_x, _cal_y, _cal_x + _cal_w, _cal_y + _cal_h, true);
draw_set_color(make_color_rgb(255, 210, 80));
draw_text(_cal_x + 8, _cal_y + 4, "CYCLE: Y" + string(_year_val) + " D" + string(_day_val));
draw_set_color(make_color_rgb(255, 235, 140));
draw_text(_cal_x + 8, _cal_y + 18, "STRAT-TURN: " + string(_turn_val));

// Big Tactile End Turn Button (Green Phosphor Raised Bevels)
var _et_x = 572 + _sx;
var _et_y = 14 + _sy;
var _et_w = 202;
var _et_h = 36;
var _et_hov = (_mx >= _et_x && _mx <= _et_x + _et_w && _my >= _et_y && _my <= _et_y + _et_h);
if (_et_hov && _click && instance_exists(obj_GameManager)) {
    obj_GameManager.end_turn();
}
scr_draw_snes_button(_et_x, _et_y, _et_w, _et_h, ">> ADVANCE (SPACE) <<", _et_hov, false, make_color_rgb(60, 240, 120));

// Turn Log Button
var _log_btn_x = 782 + _sx;
var _log_btn_w = 96;
var _log_btn_h = 36;
var _log_hov = (_mx >= _log_btn_x && _mx <= _log_btn_x + _log_btn_w && _my >= _et_y && _my <= _et_y + _log_btn_h);
if (_log_hov && _click) {
    show_turn_briefing_modal = !show_turn_briefing_modal;
}
scr_draw_snes_button(_log_btn_x, _et_y, _log_btn_w, _log_btn_h, "[LOG]", _log_hov, show_turn_briefing_modal, make_color_rgb(80, 180, 255));

// Global PMC Manual / Tutorial Button
var _man_btn_x = 886 + _sx;
var _man_btn_w = 112;
var _man_btn_h = 36;
var _man_hov = (_mx >= _man_btn_x && _mx <= _man_btn_x + _man_btn_w && _my >= _et_y && _my <= _et_y + _man_btn_h);
if (_man_hov && _click) {
    active_tutorial_modal = (active_tutorial_modal == "PMC_MANUAL") ? "" : "PMC_MANUAL";
}
scr_draw_snes_button(_man_btn_x, _et_y, _man_btn_w, _man_btn_h, "[?] MANUAL", _man_hov, (active_tutorial_modal == "PMC_MANUAL"), make_color_rgb(255, 180, 60));

// Quick Save Button (F5)
var _btn_save_x = 1006 + _sx;
var _q_btn_w = 90;
var _q_btn_h = 36;
var _s_hov = (_mx >= _btn_save_x && _mx <= _btn_save_x + _q_btn_w && _my >= _et_y && _my <= _et_y + _q_btn_h);
if (_s_hov && _click) scr_save_game();
scr_draw_snes_button(_btn_save_x, _et_y, _q_btn_w, _q_btn_h, "[F5 SAVE]", _s_hov, false, make_color_rgb(100, 240, 140));

// Career Retirement & Legacy Assessment Button (Sid Meier's Pirates Style - docs/12)
var _ret_btn_x = 1104 + _sx;
var _ret_btn_w = 180;
var _ret_btn_h = 36;
var _ret_hov = (_mx >= _ret_btn_x && _mx <= _ret_btn_x + _ret_btn_w && _my >= _et_y && _my <= _et_y + _ret_btn_h);
if (_ret_hov && _click && instance_exists(obj_GameManager)) {
    obj_GameManager.retire_career();
}
scr_draw_snes_button(_ret_btn_x, _et_y, _ret_btn_w, _ret_btn_h, "[★ RETIRE (SCORE)]", _ret_hov, false, make_color_rgb(255, 205, 70));

// =========================================================================
// 3. PRIMARY NAVIGATION TABS (y: 68 to 106)
// =========================================================================
var _tabs = [
    "1. R&D LAB // ALLOY & PROTOTYPING",
    "2. FACTORY FLOOR & PERSONNEL",
    "3. CONTRACT BOARD & COMMERCE",
    "4. STRATEGIC WAR MAP",
    "5. DREADNOUGHT // WARSHIP & RIVALS"
];

var _tab_w = (_gw - 48) / 5;
var _tab_y = 68;
var _tab_h = 36;

for (var tb = 0; tb < 5; tb++) {
    var _tbx = 24 + tb * _tab_w;
    var _tb_active = (active_tab == tb);
    var _tb_hov = (_mx >= _tbx && _mx <= _tbx + _tab_w - 6 && _my >= _tab_y && _my <= _tab_y + _tab_h);

    if (_tb_hov && _click) active_tab = tb;

    scr_draw_snes_header_tab(_tbx + _sx, _tab_y + _sy, _tab_w - 6, _tab_h, _tabs[tb], _tb_active, _tb_hov);
}

// Alert Ticker Banner (y: 108 to 126) - 16-bit CRT Comms Ribbon
var _tick_x = 24 + _sx;
var _tick_y = 108 + _sy;
var _tick_w = _gw - 48;
var _tick_h = 20;

draw_set_color(make_color_rgb(8, 12, 16));
draw_rectangle(_tick_x, _tick_y, _tick_x + _tick_w, _tick_y + _tick_h, false);
draw_set_color(make_color_rgb(30, 44, 60));
draw_rectangle(_tick_x, _tick_y, _tick_x + _tick_w, _tick_y + _tick_h, true);

if (sprite_exists(spr_snes_led_indicators)) {
    var _comms_fr = ((current_time div 400) % 2 == 0) ? 0 : 4;
    draw_sprite(spr_snes_led_indicators, _comms_fr, _tick_x + 6, _tick_y + 2);
    draw_set_color(make_color_rgb(180, 240, 140));
    draw_text(_tick_x + 28, _tick_y + 2, ">> TAC-NET INTEL: " + alerts_feed[alert_index]);
} else {
    draw_set_color(make_color_rgb(180, 240, 140));
    draw_text(_tick_x + 8, _tick_y + 2, ">> TAC-NET INTEL: " + alerts_feed[alert_index]);
}
scr_draw_snes_crt_overlay(_tick_x, _tick_y, _tick_w, _tick_h, 0.08);

// =========================================================================
// 4. MAIN WORKSPACE PANELS (y: 132 to _gh - 30)
// =========================================================================
var _pan_x = 24;
var _pan_y = 132;
var _pan_w = _gw - 48;
var _pan_h = _gh - _pan_y - 36;

// Heavy 16-bit industrial console housing with corner rivets and scanlines
scr_draw_snes_panel(_pan_x + _sx, _pan_y + _sy, _pan_w, _pan_h, "", -1, true, 0.04);"""

assert old_hud in code, "Failed to match old_hud in Draw_64.gml"
code = code.replace(old_hud, new_hud)
print("✓ Updated HUD header, navigation tabs, ticker, and main workspace panel")

# 2. Update Tab 0 Subtabs (lines 198-212)
old_t0_sub = """        draw_set_color(_stb_active ? make_color_rgb(30, 70, 110) : (_stb_hov ? make_color_rgb(20, 40, 60) : make_color_rgb(14, 22, 32)));
        draw_rectangle(_stbx + _sx, _sub_y + _sy, _stbx + _sub_w + _sx, _sub_y + 28 + _sy, false);
        draw_set_color(_stb_active ? make_color_rgb(100, 200, 255) : make_color_rgb(45, 75, 110));
        draw_rectangle(_stbx + _sx, _sub_y + _sy, _stbx + _sub_w + _sx, _sub_y + 28 + _sy, true);
        draw_set_color(_stb_active ? c_white : make_color_rgb(160, 190, 220));
        draw_text(_stbx + 14 + _sx, _sub_y + 6 + _sy, _sub_tabs[stb]);"""

new_t0_sub = """        scr_draw_snes_button(_stbx + _sx, _sub_y + _sy, _sub_w, 28, _sub_tabs[stb], _stb_hov, _stb_active, make_color_rgb(80, 190, 255));"""
assert old_t0_sub in code, "Failed to match Tab 0 subtabs"
code = code.replace(old_t0_sub, new_t0_sub)
print("✓ Updated Tab 0 subtabs to 16-bit push buttons")

# 3. Update Tab 1 Subtabs (lines 1748-1753)
old_t1_sub = """        draw_set_color(_fst_active ? make_color_rgb(25, 55, 88) : (_fst_hov ? make_color_rgb(18, 38, 60) : make_color_rgb(12, 20, 32)));
        draw_rectangle(_fsx, _fsub_y, _fsx + _fsub_w, _fsub_y + 30, false);
        draw_set_color(_fst_active ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 75, 110));
        draw_rectangle(_fsx, _fsub_y, _fsx + _fsub_w, _fsub_y + 30, true);
        draw_set_color(_fst_active ? c_white : make_color_rgb(160, 190, 220));
        draw_text(_fsx + 14, _fsub_y + 7, _fsub_names[fst]);"""

new_t1_sub = """        scr_draw_snes_button(_fsx, _fsub_y, _fsub_w, 30, _fsub_names[fst], _fst_hov, _fst_active, make_color_rgb(80, 190, 255));"""
assert old_t1_sub in code, "Failed to match Tab 1 subtabs"
code = code.replace(old_t1_sub, new_t1_sub)
print("✓ Updated Tab 1 subtabs to 16-bit push buttons")

# 4. Update Tab 2 Subtabs (lines 2504-2509)
old_t2_sub = """        draw_set_color(_cst_active ? make_color_rgb(25, 55, 88) : (_cst_hov ? make_color_rgb(18, 38, 60) : make_color_rgb(12, 20, 32)));
        draw_rectangle(_csx, _csub_y, _csx + _csub_w, _csub_y + 30, false);
        draw_set_color(_cst_active ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 75, 110));
        draw_rectangle(_csx, _csub_y, _csx + _csub_w, _csub_y + 30, true);
        draw_set_color(_cst_active ? c_white : make_color_rgb(160, 190, 220));
        draw_text(_csx + 14, _csub_y + 7, _csub_names[cst]);"""

new_t2_sub = """        scr_draw_snes_button(_csx, _csub_y, _csub_w, 30, _csub_names[cst], _cst_hov, _cst_active, make_color_rgb(80, 190, 255));"""
assert old_t2_sub in code, "Failed to match Tab 2 subtabs"
code = code.replace(old_t2_sub, new_t2_sub)
print("✓ Updated Tab 2 subtabs to 16-bit push buttons")

# 5. Update Tab 3 Subtabs (lines 3071-3076)
old_t3_sub = """        draw_set_color(_wstb_active ? make_color_rgb(30, 70, 110) : (_wstb_hov ? make_color_rgb(20, 40, 60) : make_color_rgb(14, 22, 32)));
        draw_rectangle(_wstbx + _sx, _wsub_y + _sy, _wstbx + _wsub_w + _sx, _wsub_y + 28 + _sy, false);
        draw_set_color(_wstb_active ? make_color_rgb(100, 200, 255) : make_color_rgb(45, 75, 110));
        draw_rectangle(_wstbx + _sx, _wsub_y + _sy, _wstbx + _wsub_w + _sx, _wsub_y + 28 + _sy, true);
        draw_set_color(_wstb_active ? c_white : make_color_rgb(160, 190, 220));
        draw_text(_wstbx + 10 + _sx, _wsub_y + 6 + _sy, _sub_tabs_w[wst]);"""

new_t3_sub = """        scr_draw_snes_button(_wstbx + _sx, _wsub_y + _sy, _wsub_w, 28, _sub_tabs_w[wst], _wstb_hov, _wstb_active, make_color_rgb(80, 190, 255));"""
assert old_t3_sub in code, "Failed to match Tab 3 subtabs"
code = code.replace(old_t3_sub, new_t3_sub)
print("✓ Updated Tab 3 subtabs to 16-bit push buttons")

# 6. Update Tab 4 Subtabs (lines 4593-4598)
old_t4_sub = """        draw_set_color(_fstb_act ? make_color_rgb(30, 70, 110) : (_fstb_hov ? make_color_rgb(20, 40, 60) : make_color_rgb(14, 22, 32)));
        draw_rectangle(_fstbx + _sx, _fsub_y + _sy, _fstbx + _fsub_w + _sx, _fsub_y + 28 + _sy, false);
        draw_set_color(_fstb_act ? make_color_rgb(100, 200, 255) : make_color_rgb(45, 75, 110));
        draw_rectangle(_fstbx + _sx, _fsub_y + _sy, _fstbx + _fsub_w + _sx, _fsub_y + 28 + _sy, true);
        draw_set_color(_fstb_act ? c_white : make_color_rgb(160, 190, 220));
        draw_text(_fstbx + 14 + _sx, _fsub_y + 6 + _sy, _sub_tabs_fs[fst]);"""

new_t4_sub = """        scr_draw_snes_button(_fstbx + _sx, _fsub_y + _sy, _fsub_w, 28, _sub_tabs_fs[fst], _fstb_hov, _fstb_act, make_color_rgb(80, 190, 255));"""
assert old_t4_sub in code, "Failed to match Tab 4 subtabs"
code = code.replace(old_t4_sub, new_t4_sub)
print("✓ Updated Tab 4 subtabs to 16-bit push buttons")

# 7. Update Tab 4 Category Switcher (lines 4649-4654)
old_t4_cat = """                draw_set_color(_is_cat_act ? make_color_rgb(30, 80, 120) : (_c_hov ? make_color_rgb(22, 45, 68) : make_color_rgb(14, 22, 32)));
                draw_rectangle(_cx, _cat_y, _cx + _cat_w, _cat_y + _cat_h, false);
                draw_set_color(_is_cat_act ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 75, 110));
                draw_rectangle(_cx, _cat_y, _cx + _cat_w, _cat_y + _cat_h, true);
                draw_set_color(_is_cat_act ? c_white : make_color_rgb(170, 200, 230));
                draw_text(_cx + 12, _cat_y + 6, _cat_names[c]);"""

new_t4_cat = """                scr_draw_snes_button(_cx, _cat_y, _cat_w, _cat_h, _cat_names[c], _c_hov, _is_cat_act, make_color_rgb(100, 220, 255));"""
assert old_t4_cat in code, "Failed to match Tab 4 category switcher"
code = code.replace(old_t4_cat, new_t4_cat)
print("✓ Updated Tab 4 category switcher to 16-bit push buttons")

# 8. Update Tab 2 Faction Standings with 16-bit Crests & Beveled Cards
old_t2_standings = """                draw_set_color(make_color_rgb(14, 20, 28));
                draw_rectangle(_fx, _std_y, _fx + _f_box_w, _std_y + 44, false);
                draw_set_color(make_color_rgb(40, 65, 95));
                draw_rectangle(_fx, _std_y, _fx + _f_box_w, _std_y + 44, true);

                draw_set_color(make_color_rgb(240, 210, 100));
                draw_text(_fx + 10, _std_y + 6, _finfo.name);
                var _std_col = (_std > 20) ? c_lime : ((_std < -10) ? c_red : make_color_rgb(240, 200, 80));
                draw_set_color(_std_col);
                draw_text(_fx + 10, _std_y + 24, "Standing: " + string(_std) + " (" + _finfo.standing_title + ")");"""

new_t2_standings = """                // 16-bit beveled faction card with crest
                scr_draw_snes_panel(_fx, _std_y, _f_box_w, 46, "", -1, false, 0.03);
                scr_draw_snes_faction_crest(_fx + 6, _std_y + 5, 36, _fid);

                draw_set_color(make_color_rgb(240, 210, 100));
                draw_text(_fx + 46, _std_y + 6, _finfo.name);
                var _std_col = (_std > 20) ? c_lime : ((_std < -10) ? c_red : make_color_rgb(240, 200, 80));
                draw_set_color(_std_col);
                draw_text(_fx + 46, _std_y + 24, "Standing: " + string(_std) + " (" + _finfo.standing_title + ")");"""

assert old_t2_standings in code, "Failed to match Tab 2 standings"
code = code.replace(old_t2_standings, new_t2_standings)
print("✓ Updated Tab 2 Faction Standings with 16-bit Crests & Beveled Cards")

# 9. Update Tab 3 War Balance Gauges (lines 3113-3156)
old_t3_gauges = """            draw_set_color(make_color_rgb(18, 30, 48));
            draw_rectangle(_m_x + 14, _wbox_y + 44, _m_x + 500, _wbox_y + 52, false);
            draw_set_color(make_color_rgb(60, 130, 240));
            draw_rectangle(_m_x + 14, _wbox_y + 44, _m_x + 14 + (486 * (_tc.terran_pct / 100.0)), _wbox_y + 52, false);

            // 2. Outer Colonies (Cyan)
            var _c_doc = _fm.mass_production_contracts.faction_b.replaced ? (" [DOCTRINE: " + _fm.mass_production_contracts.faction_b.replacement_name + "]") : " [DOCTRINE: AET-01]";
            draw_set_color(make_color_rgb(160, 255, 230));
            draw_text(_m_x + 14, _wbox_y + 58, "Outer Colonies: " + string(_tc.colony_pct) + "% | Military: " + string(_fm.factions.faction_b.military_strength_score) + _c_doc);
            draw_set_color(make_color_rgb(18, 30, 48));
            draw_rectangle(_m_x + 14, _wbox_y + 74, _m_x + 500, _wbox_y + 82, false);
            draw_set_color(make_color_rgb(40, 210, 180));
            draw_rectangle(_m_x + 14, _wbox_y + 74, _m_x + 14 + (486 * (_tc.colony_pct / 100.0)), _wbox_y + 82, false);

            // 3. Rogue Syndicates (Amber)
            var _s_doc = _fm.mass_production_contracts.faction_c.replaced ? (" [DOCTRINE: " + _fm.mass_production_contracts.faction_c.replacement_name + "]") : " [DOCTRINE: SCR-12]";
            draw_set_color(make_color_rgb(255, 180, 100));
            draw_text(_m_x + 14, _wbox_y + 88, "Rogue Syndicates: " + string(_tc.syndicate_pct) + "% | Pirate: " + string(_fm.factions.faction_c.military_strength_score) + _s_doc);
            draw_set_color(make_color_rgb(18, 30, 48));
            draw_rectangle(_m_x + 14, _wbox_y + 104, _m_x + 500, _wbox_y + 112, false);
            draw_set_color(make_color_rgb(240, 140, 40));
            draw_rectangle(_m_x + 14, _wbox_y + 104, _m_x + 14 + (486 * (_tc.syndicate_pct / 100.0)), _wbox_y + 112, false);

            // 4. Apex Zaibatsu (Purple)
            var _z_pct = variable_struct_exists(_tc, "zaibatsu_pct") ? _tc.zaibatsu_pct : 10;
            var _z_pwr = variable_struct_exists(_fm.factions, "faction_d") ? _fm.factions.faction_d.military_strength_score : 45;
            var _z_doc = _fm.mass_production_contracts.faction_d.replaced ? (" [DOCTRINE: " + _fm.mass_production_contracts.faction_d.replacement_name + "]") : " [DOCTRINE: ZAI-03]";
            draw_set_color(make_color_rgb(210, 160, 255));
            draw_text(_m_x + 14, _wbox_y + 118, "Apex Zaibatsu: " + string(_z_pct) + "% | Cyber-Pwr: " + string(_z_pwr) + _z_doc);
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
            draw_rectangle(_m_x + 14, _wbox_y + 164, _m_x + 14 + (486 * (_pmc_pct / 100.0)), _wbox_y + 172, false);"""

new_t3_gauges = """            scr_draw_snes_gauge(_m_x + 14, _wbox_y + 44, 486, 10, _tc.terran_pct, 100, make_color_rgb(60, 130, 240));

            // 2. Outer Colonies (Cyan)
            var _c_doc = _fm.mass_production_contracts.faction_b.replaced ? (" [DOCTRINE: " + _fm.mass_production_contracts.faction_b.replacement_name + "]") : " [DOCTRINE: AET-01]";
            draw_set_color(make_color_rgb(160, 255, 230));
            draw_text(_m_x + 14, _wbox_y + 58, "Outer Colonies: " + string(_tc.colony_pct) + "% | Military: " + string(_fm.factions.faction_b.military_strength_score) + _c_doc);
            scr_draw_snes_gauge(_m_x + 14, _wbox_y + 74, 486, 10, _tc.colony_pct, 100, make_color_rgb(40, 210, 180));

            // 3. Rogue Syndicates (Amber)
            var _s_doc = _fm.mass_production_contracts.faction_c.replaced ? (" [DOCTRINE: " + _fm.mass_production_contracts.faction_c.replacement_name + "]") : " [DOCTRINE: SCR-12]";
            draw_set_color(make_color_rgb(255, 180, 100));
            draw_text(_m_x + 14, _wbox_y + 88, "Rogue Syndicates: " + string(_tc.syndicate_pct) + "% | Pirate: " + string(_fm.factions.faction_c.military_strength_score) + _s_doc);
            scr_draw_snes_gauge(_m_x + 14, _wbox_y + 104, 486, 10, _tc.syndicate_pct, 100, make_color_rgb(240, 140, 40));

            // 4. Apex Zaibatsu (Purple)
            var _z_pct = variable_struct_exists(_tc, "zaibatsu_pct") ? _tc.zaibatsu_pct : 10;
            var _z_pwr = variable_struct_exists(_fm.factions, "faction_d") ? _fm.factions.faction_d.military_strength_score : 45;
            var _z_doc = _fm.mass_production_contracts.faction_d.replaced ? (" [DOCTRINE: " + _fm.mass_production_contracts.faction_d.replacement_name + "]") : " [DOCTRINE: ZAI-03]";
            draw_set_color(make_color_rgb(210, 160, 255));
            draw_text(_m_x + 14, _wbox_y + 118, "Apex Zaibatsu: " + string(_z_pct) + "% | Cyber-Pwr: " + string(_z_pwr) + _z_doc);
            scr_draw_snes_gauge(_m_x + 14, _wbox_y + 134, 486, 10, _z_pct, 100, make_color_rgb(180, 90, 240));

            // 5. PMC Sovereign Dominion (Gold / Lime - docs/12)
            var _pmc_pct = variable_struct_exists(_tc, "pmc_pct") ? _tc.pmc_pct : 0;
            var _pmc_tribute = _pmc_pct * 3500;
            draw_set_color(make_color_rgb(255, 215, 60));
            draw_text(_m_x + 14, _wbox_y + 148, "PMC Sovereign Dominion: " + string(_pmc_pct) + "% | Tribute: +" + string(_pmc_tribute) + " Cr/day");
            scr_draw_snes_gauge(_m_x + 14, _wbox_y + 164, 486, 10, _pmc_pct, 100, make_color_rgb(255, 215, 60));"""

assert old_t3_gauges in code, "Failed to match Tab 3 gauges"
code = code.replace(old_t3_gauges, new_t3_gauges)
print("✓ Updated Tab 3 War Map faction influence bars to 16-bit segmented LED gauges")

# 10. Update Modals: Turn Briefing and Tutorial Modal
old_turn_modal = """if (show_turn_briefing_modal) {
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
    draw_text(_mx0 + _mw - _cl_w - 8, _my0 + 22, "[X CLOSE (ESC)]");"""

new_turn_modal = """if (show_turn_briefing_modal) {
    var _mw = 800;
    var _mh = 540;
    var _mx0 = (_gw - _mw) / 2;
    var _my0 = (_gh - _mh) / 2;

    scr_draw_snes_window_modal(_mx0, _my0, _mw, _mh, "PMC COMMAND DECK // STRATEGIC TURN BRIEFING", "HISTORICAL LOG & EVENT LEDGER");

    // Close Button
    var _cl_w = 140;
    var _cl_hov = (_mx >= _mx0 + _mw - _cl_w - 20 && _mx <= _mx0 + _mw - 20 && _my >= _my0 + 10 && _my <= _my0 + 38);
    if ((_cl_hov && _click) || keyboard_check_pressed(vk_escape)) show_turn_briefing_modal = false;
    scr_draw_snes_button(_mx0 + _mw - _cl_w - 20, _my0 + 10, _cl_w, 28, "[X CLOSE (ESC)]", _cl_hov, false, c_red);"""

assert old_turn_modal in code, "Failed to match Turn Briefing modal"
code = code.replace(old_turn_modal, new_turn_modal)
print("✓ Updated Turn Briefing modal to 16-bit SNES briefing window")

old_tut_modal = """if (active_tutorial_modal != "") {
    draw_set_alpha(0.85);
    draw_set_color(c_black);
    draw_rectangle(0, 0, _gw, _gh, false);
    draw_set_alpha(1.0);

    var _mw = 860;
    var _mh = 580;
    var _mx0 = (_gw - _mw) / 2;
    var _my0 = (_gh - _mh) / 2;

    draw_set_color(make_color_rgb(12, 18, 26));
    draw_rectangle(_mx0, _my0, _mx0 + _mw, _my0 + _mh, false);
    draw_set_color(make_color_rgb(255, 180, 60));
    draw_rectangle(_mx0, _my0, _mx0 + _mw, _my0 + _mh, true);

    // Header
    draw_set_color(make_color_rgb(255, 200, 80));
    draw_text(_mx0 + 24, _my0 + 20, "== PMC OPERATIONAL FLIGHT MANUAL & SYSTEM TUTORIALS ==");

    // Close Button
    var _cl_w = 140;
    var _cl_hov = (_mx >= _mx0 + _mw - _cl_w - 20 && _mx <= _mx0 + _mw - 20 && _my >= _my0 + 16 && _my <= _my0 + 44);
    if ((_cl_hov && _click) || keyboard_check_pressed(vk_escape)) active_tutorial_modal = "";
    draw_set_color(_cl_hov ? make_color_rgb(120, 40, 40) : make_color_rgb(60, 20, 20));
    draw_rectangle(_mx0 + _mw - _cl_w - 20, _my0 + 16, _mx0 + _mw - 20, _my0 + 44, false);
    draw_set_color(c_red);
    draw_rectangle(_mx0 + _mw - _cl_w - 20, _my0 + 16, _mx0 + _mw - 20, _my0 + 44, true);
    draw_set_color(c_white);
    draw_text(_mx0 + _mw - _cl_w - 8, _my0 + 22, "[X CLOSE (ESC)]");"""

new_tut_modal = """if (active_tutorial_modal != "") {
    var _mw = 860;
    var _mh = 580;
    var _mx0 = (_gw - _mw) / 2;
    var _my0 = (_gh - _mh) / 2;

    scr_draw_snes_window_modal(_mx0, _my0, _mw, _mh, "PMC OPERATIONAL MANUAL // TACTICAL ARCHIVE", "SYSTEM TUTORIALS & DOCTRINE SCHEMATICS");

    // Close Button
    var _cl_w = 140;
    var _cl_hov = (_mx >= _mx0 + _mw - _cl_w - 20 && _mx <= _mx0 + _mw - 20 && _my >= _my0 + 10 && _my <= _my0 + 38);
    if ((_cl_hov && _click) || keyboard_check_pressed(vk_escape)) active_tutorial_modal = "";
    scr_draw_snes_button(_mx0 + _mw - _cl_w - 20, _my0 + 10, _cl_w, 28, "[X CLOSE (ESC)]", _cl_hov, false, c_red);"""

assert old_tut_modal in code, "Failed to match Tutorial modal"
code = code.replace(old_tut_modal, new_tut_modal)
print("✓ Updated Tutorial modal to 16-bit SNES briefing window")

with open(FILE_PATH, "w") as f:
    f.write(code)

print("\n✓ ALL HQTERMINAL DRAW_64 SNES UI UPGRADES APPLIED SUCCESSFULLY!")
