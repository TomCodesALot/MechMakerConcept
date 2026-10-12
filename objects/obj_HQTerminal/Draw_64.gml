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
    "3. CONTRACT BOARD",
    "4. STRATEGIC WAR MAP"
];

var _tab_w = (_gw - 48) / 4;
var _tab_y = 68;
var _tab_h = 36;

for (var tb = 0; tb < 4; tb++) {
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
draw_rectangle(_pan_x + _sx, _pan_y + _sy, _pan_x + _pan_w + _sx, _pan_y + _pan_h + _sy, true);

// -------------------------------------------------------------------------
// TAB 0: R&D LAB // ALLOY CHEMISTRY & PROTOTYPING MINIGAMES (Docs 02 & 03)
// -------------------------------------------------------------------------
if (active_tab == 0) {
    var _sub_tabs = [
        "[A. ALLOY CRUCIBLE SYNTHESIS (DOC 02)]",
        "[B. COMPONENT PROTOTYPING MINIGAMES (DOC 03)]",
        "[C. BLUEPRINT ARCHIVE & INVENTORY SCHEMATICS]"
    ];
    var _sub_w = 380;
    var _sub_y = _pan_y + 8;
    for (var stb = 0; stb < 3; stb++) {
        var _stbx = _pan_x + 16 + stb * (_sub_w + 12);
        var _stb_active = (rd_subtab == stb);
        var _stb_hov = (_mx >= _stbx && _mx <= _stbx + _sub_w && _my >= _sub_y && _my <= _sub_y + 28);
        if (_stb_hov && _click) rd_subtab = stb;

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

        // Chamber Visualizer
        var _win_x = _c_x + 24;
        var _win_y = _c_y + 44;
        var _win_w = 260;
        var _win_h = 220;

        draw_set_color(c_black);
        draw_rectangle(_win_x + _sx, _win_y + _sy, _win_x + _win_w + _sx, _win_y + _win_h + _sy, false);

        var _temp_norm = clamp((crucible_temp_c - 25.0) / 4975.0, 0, 1);
        var _glow_r = lerp(40, 255, _temp_norm);
        var _glow_g = lerp(60, 180, _temp_norm);
        var _glow_b = lerp(120, 255, max(0, (_temp_norm - 0.7) * 3.3));
        draw_set_color(make_color_rgb(_glow_r, _glow_g, _glow_b));
        draw_set_alpha(0.3 + _temp_norm * 0.7);
        draw_circle(_win_x + _win_w / 2 + _sx, _win_y + _win_h / 2 + _sy, 50 + _temp_norm * 45, false);
        draw_set_alpha(1.0);

        draw_set_color(make_color_rgb(60, 100, 140));
        draw_rectangle(_win_x + _sx, _win_y + _sy, _win_x + _win_w + _sx, _win_y + _win_h + _sy, true);

        // Gauges
        var _gauge_x = _win_x + _win_w + 24;
        var _gauge_y = _win_y;

        // Temperature Gauge
        draw_set_color(c_white);
        draw_text(_gauge_x, _gauge_y, "CHAMBER TEMPERATURE:");
        var _temp_col = (crucible_temp_c >= 2200 && crucible_temp_c <= 2500) ? c_lime : ((crucible_temp_c >= 4000 && crucible_temp_c <= 4500) ? c_aqua : make_color_rgb(255, 180, 80));
        draw_set_color(_temp_col);
        draw_text(_gauge_x, _gauge_y + 20, string(floor(crucible_temp_c)) + " °C (Target: 2200-2500°C)");
        draw_set_color(make_color_rgb(20, 30, 40));
        draw_rectangle(_gauge_x, _gauge_y + 44, _gauge_x + 280, _gauge_y + 58, false);
        draw_set_color(_temp_col);
        draw_rectangle(_gauge_x, _gauge_y + 44, _gauge_x + (280 * _temp_norm), _gauge_y + 58, false);

        // Pressure Gauge
        var _psi_norm = clamp(crucible_pressure_psi / 10000.0, 0, 1);
        draw_set_color(c_white);
        draw_text(_gauge_x, _gauge_y + 70, "PRESSURE CHAMBER:");
        var _psi_col = (crucible_pressure_psi > 1200 && crucible_batch.mat_silica_carb > 0) ? c_red : make_color_rgb(100, 200, 255);
        draw_set_color(_psi_col);
        draw_text(_gauge_x, _gauge_y + 90, string(floor(crucible_pressure_psi)) + " PSI (Safe: <1200 PSI)");
        draw_set_color(make_color_rgb(20, 30, 40));
        draw_rectangle(_gauge_x, _gauge_y + 114, _gauge_x + 280, _gauge_y + 128, false);
        draw_set_color(_psi_col);
        draw_rectangle(_gauge_x, _gauge_y + 114, _gauge_x + (280 * _psi_norm), _gauge_y + 128, false);

        // Volatility Gauge
        draw_set_color(c_white);
        draw_text(_gauge_x, _gauge_y + 140, "CHEMICAL VOLATILITY:");
        var _vol_col = (volatility_meter > 70) ? c_red : ((volatility_meter > 35) ? c_yellow : c_lime);
        draw_set_color(_vol_col);
        draw_text(_gauge_x, _gauge_y + 160, string(floor(volatility_meter)) + " % (Breach at 90%)");
        draw_set_color(make_color_rgb(20, 30, 40));
        draw_rectangle(_gauge_x, _gauge_y + 184, _gauge_x + 280, _gauge_y + 198, false);
        draw_set_color(_vol_col);
        draw_rectangle(_gauge_x, _gauge_y + 184, _gauge_x + (280 * (volatility_meter / 100.0)), _gauge_y + 198, false);

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
            draw_text(_mx_box + 48, _my_box + 26, "Loaded: " + string(crucible_batch[$ _mats[mi]]));

            // Load Button
            var _lb_y = _my_box + 46;
            var _lb_hov = (_mx >= _mx_box + 8 && _mx <= _mx_box + 130 && _my >= _lb_y && _my <= _lb_y + 24);
            if (_lb_hov && _click) crucible_load_mat(_mats[mi]);
            draw_set_color(_lb_hov ? make_color_rgb(30, 70, 45) : make_color_rgb(16, 36, 24));
            draw_rectangle(_mx_box + 8, _lb_y, _mx_box + 130, _lb_y + 24, false);
            draw_set_color(make_color_rgb(60, 200, 100));
            draw_rectangle(_mx_box + 8, _lb_y, _mx_box + 130, _lb_y + 24, true);
            draw_set_color(c_white);
            draw_text(_mx_box + 24, _lb_y + 4, "[+1 LOAD]");
        }

        // Action: Purge & Execute Synthesis Buttons
        var _exec_y = _hop_y + 112;
        var _purg_hov = (_mx >= _win_x && _mx <= _win_x + 180 && _my >= _exec_y && _my <= _exec_y + 38);
        if (_purg_hov && _click) crucible_purge_hopper();
        draw_set_color(_purg_hov ? make_color_rgb(80, 30, 30) : make_color_rgb(40, 16, 16));
        draw_rectangle(_win_x, _exec_y, _win_x + 180, _exec_y + 38, false);
        draw_set_color(make_color_rgb(240, 80, 80));
        draw_rectangle(_win_x, _exec_y, _win_x + 180, _exec_y + 38, true);
        draw_set_color(c_white);
        draw_text(_win_x + 22, _exec_y + 11, "[PURGE HOPPER]");

        var _syn_btn_x = _win_x + 196;
        var _syn_btn_w = 398;
        var _syn_hov = (_mx >= _syn_btn_x && _mx <= _syn_btn_x + _syn_btn_w && _my >= _exec_y && _my <= _exec_y + 38);
        if (_syn_hov && _click) crucible_execute_synthesis();
        draw_set_color(_syn_hov ? make_color_rgb(30, 95, 60) : make_color_rgb(18, 52, 32));
        draw_rectangle(_syn_btn_x, _exec_y, _syn_btn_x + _syn_btn_w, _exec_y + 38, false);
        draw_set_color(make_color_rgb(60, 240, 120));
        draw_rectangle(_syn_btn_x, _exec_y, _syn_btn_x + _syn_btn_w, _exec_y + 38, true);
        draw_set_color(c_white);
        draw_text(_syn_btn_x + 40, _exec_y + 11, ">> EXECUTE ALLOY SYNTHESIS BATCH <<");

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
            "[3. PERIODIC TABLE (118 ELEMENTS)]"
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

        // --- SUBVIEW 0: FURNACE LIVE PREVIEW & MASTER CODEX ---
        if (crucible_subview == 0) {
            // 1. Current Batch Ingot Real-Time Color Preview
            var _bw_y = _met_y + 44;
            draw_set_color(make_color_rgb(14, 20, 28));
            draw_rectangle(_met_x + 16, _bw_y, _met_x + _met_w - 16, _bw_y + 110, false);
            draw_set_color(make_color_rgb(35, 55, 80));
            draw_rectangle(_met_x + 16, _bw_y, _met_x + _met_w - 16, _bw_y + 110, true);

            draw_set_color(make_color_rgb(240, 210, 100));
            draw_text(_met_x + 28, _bw_y + 10, "LIVE HOPPER ALLOY CHROMATIC SYNTHESIS:");

            scr_draw_alloy_swatch(_met_x + 28, _bw_y + 36, 120, 56, crucible_batch);

            var _cur_hex = scr_alloy_get_hex(crucible_batch);
            draw_set_color(c_white);
            draw_text(_met_x + 164, _bw_y + 36, "Synthesized Color: " + _cur_hex);
            var _batch_tot = crucible_batch.mat_tungsten + crucible_batch.mat_silica_carb + crucible_batch.mat_tritium + crucible_batch.mat_syn_flux;
            draw_set_color(make_color_rgb(160, 200, 230));
            draw_text(_met_x + 164, _bw_y + 56, "Composition Ratio: W:" + string(crucible_batch.mat_tungsten) + " | C:" + string(crucible_batch.mat_silica_carb) + " | Tr:" + string(crucible_batch.mat_tritium) + " | Fx:" + string(crucible_batch.mat_syn_flux) + " (Total: " + string(_batch_tot) + ")");
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_met_x + 164, _bw_y + 76, "Thermal Glow Shift: " + string(floor(crucible_temp_c)) + "°C | Crystal Densification: " + string(floor(crucible_pressure_psi)) + " PSI");

            // 2. Known Master Alloy Codex Grid
            var _cdx_y = _bw_y + 125;
            draw_set_color(make_color_rgb(100, 210, 255));
            draw_text(_met_x + 16, _cdx_y, "MASTER METALLURGICAL ALLOY CODEX (ENGINEERING STANDARDS):");

            var _known_alloys = [
                { id: "alloy_vanguard_comp", name: "Vanguard Composite Plating", formula: "2x Tungsten + 1x Silica-Carbon", role: "Heavy Ballistic Plating" },
                { id: "alloy_hyperion_matrix", name: "Hyperion Superconductor Matrix", formula: "1x Tungsten + 2x Tritium + 1x Flux", role: "Tokamak Core Superconductor" },
                { id: "alloy_aerosteel_flux", name: "Aerosteel Vernier Flux", formula: "2x Flux + 1x Tritium + 1x Silica", role: "High-G Orbital Thrusters" },
                { id: "alloy_adamantine_carbide", name: "Adamantine Carbide", formula: "3x Tungsten + 2x Silica + 1x Flux", role: "AP Kinetic Shells & Pincer Blades" }
            ];

            var _al_box_w = (_met_w - 48) / 2;
            var _al_box_h = 80;

            for (var ai = 0; ai < 4; ai++) {
                var _al = _known_alloys[ai];
                var _ax = _met_x + 16 + (ai mod 2) * (_al_box_w + 16);
                var _ay = _cdx_y + 24 + (ai div 2) * (_al_box_h + 12);

                draw_set_color(make_color_rgb(12, 18, 26));
                draw_rectangle(_ax, _ay, _ax + _al_box_w, _ay + _al_box_h, false);
                draw_set_color(make_color_rgb(35, 60, 90));
                draw_rectangle(_ax, _ay, _ax + _al_box_w, _ay + _al_box_h, true);

                scr_draw_alloy_swatch(_ax + 12, _ay + 14, 48, 52, _al.id);

                draw_set_color(make_color_rgb(240, 215, 100));
                draw_text(_ax + 70, _ay + 10, _al.name);
                draw_set_color(c_white);
                draw_text(_ax + 70, _ay + 30, "Recipe: " + _al.formula);
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_ax + 70, _ay + 50, "Class: " + _al.role + " (" + scr_alloy_get_hex(_al.id) + ")");
            }

            // 3. Technical Notes & Art Shader Pipeline Architecture
            var _art_note_y = _cdx_y + 205;
            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_met_x + 16, _art_note_y, _met_x + _met_w - 16, _met_y + _met_h - 16, false);
            draw_set_color(make_color_rgb(30, 50, 75));
            draw_rectangle(_met_x + 16, _art_note_y, _met_x + _met_w - 16, _met_y + _met_h - 16, true);

            draw_set_color(make_color_rgb(220, 180, 80));
            draw_text(_met_x + 28, _art_note_y + 10, "TECHNICAL ARCHITECTURE // PROGRAMMATIC ALLOY SHADER PIPELINE:");
            draw_set_color(make_color_rgb(180, 205, 230));
            draw_text(_met_x + 28, _art_note_y + 32, "* Art Pipeline: Mobile Suits use grayscale master specular masks (Neutral Albedo, Specular Gloss, Emission).");
            draw_text(_met_x + 28, _art_note_y + 52, "* Procedural Engine: scr_get_alloy_procedural_color() performs weighted spectral synthesis across elemental vectors.");
            draw_text(_met_x + 28, _art_note_y + 72, "* Thermal & Pressure Shift: Real-time incandescence (1500-6000°C) and crystal compaction (0-10,000 PSI) tinting.");
            draw_text(_met_x + 28, _art_note_y + 92, "* Scaling: Generates infinite distinct visual metallic finishes for 100+ raw ores & 1,000+ custom alloys with 0 artist crunch.");
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

            // Element list on left half of subview
            var _pt_box_w = 420;
            var _pt_box_h = _met_h - 80;
            var _pt_x = _met_x + 16;
            var _pt_y = _met_y + 68;

            draw_set_color(make_color_rgb(12, 18, 26));
            draw_rectangle(_pt_x, _pt_y, _pt_x + _pt_box_w, _pt_y + _pt_box_h, false);
            draw_set_color(make_color_rgb(35, 55, 80));
            draw_rectangle(_pt_x, _pt_y, _pt_x + _pt_box_w, _pt_y + _pt_box_h, true);

            var _pt_vis = 8;
            for (var pi = 0; pi < min(_pt_vis, _pt_len); pi++) {
                var _pidx = pi + pt_scroll_offset;
                if (_pidx >= _pt_len) break;
                var _elem = _pt_list[_pidx];
                var _ey = _pt_y + 8 + pi * 44;
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

        // Minigame 0: Reactor Conduit Tuning (Turn-Based Oscilloscope Resonance)
        if (active_minigame == 0) {
            var _scope_x = _m_pan_x + 10;
            var _scope_y = _m_pan_y + 44;
            var _scope_w = 780;
            var _scope_h = 310;

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
            draw_set_color(make_color_rgb(170, 200, 230));
            draw_text(_stat_x + 16, _diag_y + 20, "TARGET SYNC: >= 90.0% REQUIRED");

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
            var _l_y = _m_pan_y + 44;

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
            var _t_y = _m_pan_y + 44;

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
            "[1. PMC ACTIVE FLEET INVENTORY]",
            "[2. CANONICAL BLUEPRINT ARCHIVE (58 CHASSIS)]"
        ];
        var _src_w = 340;
        for (var sc = 0; sc < 2; sc++) {
            var _scx = _s_x + sc * (_src_w + 14);
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
            draw_text(_scx + 12, _s_y + 6, _src_names[sc]);
        }

        // Faction Filter Bar (only active when bp_archive_source == 1)
        if (bp_archive_source == 1) {
            var _f_filters = [
                { id: "all", label: "ALL (58)" },
                { id: "faction_terran", label: "TERRAN" },
                { id: "faction_colony", label: "COLONY" },
                { id: "faction_syndicate", label: "SYNDICATE" },
                { id: "faction_zaibatsu", label: "ZAIBATSU" },
                { id: "player", label: "PMC DOCTRINE" }
            ];
            var _ff_x = _s_x + 2 * (_src_w + 14) + 10;
            var _ff_w = 110;
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
        // COLUMN 1: LEFT SELECTOR LIST (width: 320px)
        // =====================================================================
        var _col1_x = _s_x;
        var _col1_y = _s_y + 38;
        var _col1_w = 320;
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

            var _code = _item[$ "model_code"] ?? (_item[$ "callsign"] ?? _item.name);
            var _iname = _item[$ "name"] ?? "Mobile Suit";
            var _sub = (bp_archive_source == 0) ? ("Status: " + string(_item[$ "status"] ?? "READY")) : ("Role: " + string(_item[$ "role"] ?? "Assault"));

            draw_set_color(_i_sel ? c_white : make_color_rgb(220, 220, 220));
            draw_text(_col1_x + 16, _iy + 8, _code + " // " + _iname);
            draw_set_color(make_color_rgb(100, 200, 255));
            draw_text(_col1_x + 16, _iy + 28, _sub);
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
        // COLUMN 2: CENTER VISUAL & SCHEMATICS PRESENTATION (width: 760px)
        // =====================================================================
        var _col2_x = _col1_x + _col1_w + 16;
        var _col2_y = _col1_y;
        var _col2_w = 760;
        var _col2_h = _col1_h;

        draw_set_color(make_color_rgb(10, 15, 22));
        draw_rectangle(_col2_x, _col2_y, _col2_x + _col2_w, _col2_y + _col2_h, false);
        draw_set_color(make_color_rgb(35, 55, 80));
        draw_rectangle(_col2_x, _col2_y, _col2_x + _col2_w, _col2_y + _col2_h, true);

        // Center Sub-Mode Tabs
        var _c_submodes = [
            "[1. TACTICAL SPRITE & FINISH]",
            "[2. TECHNICAL SCHEMATIC]",
            "[3. ALLOY SWATCH & MATRIX]",
            "[4. MODULAR COMPONENTS]"
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
            var _active_alloy_cost = _active_suit[$ "alloy_cost"] ?? { tungsten: 40, silica: 20, flux: 10 };
            var _alloy_tint = scr_get_alloy_procedural_color(_active_alloy_cost);
            var _alloy_hex = scr_alloy_get_hex(_active_alloy_cost);

            // Sub-Mode 0: Tactical Sprite & Finish
            if (bp_archive_view_mode == 0) {
                var _spr = _active_suit[$ "associated_sprite"] ?? spr_ms_ironclad_mp;
                if (!sprite_exists(_spr)) _spr = spr_ms_ironclad_mp;

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
                draw_text(_ped_x + 86, _sw_box_y + 12, "ARMOR ALLOY FINISH: " + string(_active_suit[$ "metal_type"] ?? "Composite Laminate"));
                draw_set_color(c_white);
                draw_text(_ped_x + 86, _sw_box_y + 30, "Procedural Chromatic Signature: " + _alloy_hex);
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_ped_x + 86, _sw_box_y + 48, "Spectral Weights: W:" + string(_active_alloy_cost[$ "tungsten"] ?? 0) + " | C:" + string(_active_alloy_cost[$ "silica"] ?? 0) + " | Tr:" + string(_active_alloy_cost[$ "tritium"] ?? 0) + " | Flux:" + string(_active_alloy_cost[$ "flux"] ?? 0));
            }
            // Sub-Mode 1: Technical Schematics
            else if (bp_archive_view_mode == 1) {
                var _sch_x = _col2_x + 24;
                var _sch_y = _col2_y + 48;
                if (sprite_exists(spr_mech_schematic)) {
                    draw_sprite_ext(spr_mech_schematic, 0, _sch_x, _sch_y, 0.62, 0.62, 0, c_white, 0.95);
                }
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_sch_x + 12, _sch_y + 390, "TECHNICAL SCHEMATIC: Height: " + string(_active_suit[$ "height_meters"] ?? 18.0) + "m | Combat Mass: " + string(_active_suit[$ "combat_weight_tonnes"] ?? 85.0) + "t");
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
                draw_text(_mat_x + 20, _mat_y + 16, "DEEP METALLURGICAL ALLOY ANALYSIS (DOC 02 & 14):");

                scr_draw_alloy_swatch(_mat_x + 20, _mat_y + 44, 180, 80, _active_alloy_cost);

                draw_set_color(c_white);
                draw_text(_mat_x + 220, _mat_y + 44, "Alloy Hex Code: " + _alloy_hex);
                draw_set_color(make_color_rgb(180, 210, 240));
                draw_text(_mat_x + 220, _mat_y + 66, "Tensile Modulus: High Impact Kinetic Deflection");
                draw_text(_mat_x + 220, _mat_y + 88, "Thermal Dissipation: " + string(_active_suit[$ "heat_dispersion_rate"] ?? 30.0) + " °C / sec");
                draw_text(_mat_x + 220, _mat_y + 110, "Base Structure Integrity: " + string(_active_suit[$ "structure_hp"] ?? 2000) + " HP");

                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_mat_x + 20, _mat_y + 145, "REQUISITE ELEMENTAL INGOT RATIOS (CRUCIBLE HOPPER):");
                var _cost_keys = variable_struct_get_names(_active_alloy_cost);
                for (var ck = 0; ck < array_length(_cost_keys); ck++) {
                    var _ckname = _cost_keys[ck];
                    var _cqty = _active_alloy_cost[$ _ckname];
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
        // COLUMN 3: RIGHT PANEL - SPECS, LORE, VARIANTS & ACTIONS (width: ~680px)
        // =====================================================================
        var _col3_x = _col2_x + _col2_w + 16;
        var _col3_y = _col1_y;
        var _col3_w = _pan_w - (_col3_x - _pan_x) - 16;
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
            draw_text(_rx, _ry, string(_active_suit[$ "model_code"] ?? "MS") + " " + string(_active_suit[$ "name"] ?? "Mobile Suit"));
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_rx, _ry + 20, "Role: " + string(_active_suit[$ "role"] ?? "Assault") + " | Era: " + string(_active_suit[$ "era"] ?? "Production"));

            // Core Technical Specs
            draw_set_color(c_white);
            draw_text(_rx, _ry + 48, "* Armor Rating: " + string(_active_suit[$ "armor_rating"] ?? 850) + " HP");
            draw_text(_rx, _ry + 68, "* Structure HP: " + string(_active_suit[$ "structure_hp"] ?? 2000) + " HP");
            draw_text(_rx, _ry + 88, "* Reactor Output: " + string(_active_suit[$ "power_output_mw"] ?? 1200) + " MW (" + string(_active_suit[$ "reactor_type"] ?? "Fusion Core") + ")");
            draw_text(_rx, _ry + 108, "* Mobility: Walk " + string(_active_suit[$ "walk_speed_kph"] ?? 40) + " km/h | Boost " + string(_active_suit[$ "boost_speed_kph"] ?? 80) + " km/h");
            draw_text(_rx, _ry + 128, "* Dimensions: Height " + string(_active_suit[$ "height_meters"] ?? 18.0) + "m | Weight " + string(_active_suit[$ "combat_weight_tonnes"] ?? 85.0) + "t");

            // Equipped Weapons
            var _arms_y = _ry + 158;
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_rx, _arms_y, "ARMAMENT LOADOUT:");
            var _arms = _active_suit[$ "armament"] ?? ["Autocannon", "Vulcan"];
            if (is_array(_arms)) {
                for (var w = 0; w < min(3, array_length(_arms)); w++) {
                    draw_set_color(c_white);
                    draw_text(_rx + 10, _arms_y + 20 + w * 18, "> " + string(_arms[w]));
                }
            }

            // Production Variants Directory
            var _var_y = _arms_y + 82;
            draw_set_color(make_color_rgb(240, 210, 100));
            draw_text(_rx, _var_y, "PRODUCTION VARIANTS & DOCTRINES:");
            var _vars = _active_suit[$ "variants"] ?? ["Standard Production", "Ace Refit"];
            if (is_array(_vars)) {
                for (var v = 0; v < min(4, array_length(_vars)); v++) {
                    draw_set_color(make_color_rgb(180, 210, 240));
                    draw_text(_rx + 10, _var_y + 20 + v * 18, "[+] " + string(_vars[v]));
                }
            }

            // Lore Dossier
            var _lore_y = _var_y + 100;
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_rx, _lore_y, "MANUFACTURING LORE & REPUTATION:");
            draw_set_color(make_color_rgb(190, 205, 220));
            draw_text_ext(_rx, _lore_y + 20, string(_active_suit[$ "manufacturing_lore"] ?? "Classified defense project."), 16, _col3_w - 32);

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
        "[A. BASE FACILITIES & ASSEMBLY BAYS (DOC 07)]",
        "[B. MODULAR PART FORGE (ALLOYS)]",
        "[C. CUSTOM COMBINATIONS ASSEMBLY BAY (BUILDER)]"
    ];
    var _fsub_w = 390;
    var _fsub_y = _pan_y + 8;
    for (var fst = 0; fst < 3; fst++) {
        var _fsx = _pan_x + 30 + fst * (_fsub_w + 14);
        var _fst_active = (factory_subtab == fst);
        var _fst_hov = (_mx >= _fsx && _mx <= _fsx + _fsub_w && _my >= _fsub_y && _my <= _fsub_y + 30);
        if (_fst_hov && _click) factory_subtab = fst;

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
        draw_text(_f_x, _f_y, "== FACTORY OPERATIONS & PERSONNEL ROSTER (docs/07) ==");

        // Left Column: Facility Upgrades & Assembly Lines
        var _col1_w = 580;
        draw_set_color(make_color_rgb(10, 16, 24));
        draw_rectangle(_f_x, _f_y + 24, _f_x + _col1_w, _f_y + 580, false);
        draw_set_color(make_color_rgb(35, 60, 90));
        draw_rectangle(_f_x, _f_y + 24, _f_x + _col1_w, _f_y + 580, true);

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
                    show_toast("CRUCIBLE UPGRADED TO TIER 2 (6000°C / 10,000 PSI)!", c_lime);
                } else {
                    show_toast("INSUFFICIENT FUNDS! (Requires 250,000 Cr)", c_red);
                }
            }
            draw_set_color(_u1_hov ? make_color_rgb(30, 70, 50) : make_color_rgb(18, 40, 28));
            draw_rectangle(_f_x + 16, _u1_y, _f_x + 550, _u1_y + 32, false);
            draw_set_color(make_color_rgb(80, 220, 120));
            draw_rectangle(_f_x + 16, _u1_y, _f_x + 550, _u1_y + 32, true);
            draw_set_color(c_white);
            draw_text(_f_x + 24, _u1_y + 8, _gm.facilities.crucible_tier > 1 ? "[CRUCIBLE TIER 2 INSTALLED]" : "[UPGRADE CRUCIBLE: TIER 2 - 250,000 Cr]");

            // 2. Expand Assembly Lines
            var _u2_y = _u1_y + 40;
            var _u2_hov = (_mx >= _f_x + 16 && _mx <= _f_x + 550 && _my >= _u2_y && _my <= _u2_y + 32);
            if (_u2_hov && _click && _gm.facilities.assembly_lines < 4) {
                if (_gm.spend_funds(300000)) {
                    _gm.facilities.assembly_lines++;
                    show_toast("ASSEMBLY CAPACITY EXPANDED TO " + string(_gm.facilities.assembly_lines) + " BAYS!", c_lime);
                } else {
                    show_toast("INSUFFICIENT FUNDS! (Requires 300,000 Cr)", c_red);
                }
            }
            draw_set_color(_u2_hov ? make_color_rgb(30, 60, 80) : make_color_rgb(18, 35, 48));
            draw_rectangle(_f_x + 16, _u2_y, _f_x + 550, _u2_y + 32, false);
            draw_set_color(make_color_rgb(80, 180, 240));
            draw_rectangle(_f_x + 16, _u2_y, _f_x + 550, _u2_y + 32, true);
            draw_set_color(c_white);
            draw_text(_f_x + 24, _u2_y + 8, "[COMMISSION NEW ASSEMBLY LINE - 300,000 Cr]");

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

        draw_set_color(make_color_rgb(10, 16, 24));
        draw_rectangle(_col2_x, _f_y + 24, _col2_x + _col2_w, _f_y + 580, false);
        draw_set_color(make_color_rgb(35, 60, 90));
        draw_rectangle(_col2_x, _f_y + 24, _col2_x + _col2_w, _f_y + 580, true);

        draw_set_color(make_color_rgb(240, 210, 100));
        draw_text(_col2_x + 16, _f_y + 36, "ACTIVE PERSONNEL & PILOT ROSTER:");

        if (instance_exists(obj_GameManager)) {
            var _gm = obj_GameManager;
            var _py_start = _f_y + 64;
            for (var p = 0; p < array_length(_gm.facilities.roster_pilots); p++) {
                var _plt = _gm.facilities.roster_pilots[p];
                var _p_stat = _plt[$ "status"] ?? "ACTIVE";
                draw_set_color(_p_stat == "HOSPITALIZED" ? make_color_rgb(255, 180, 80) : c_white);
                var _stat_tag = (_p_stat == "HOSPITALIZED") ? " [HOSPITALIZED - " + string(_plt.recovery_days_left) + "d]" : "";
                draw_text(_col2_x + 16, _py_start + p * 30, string(p + 1) + ". " + _plt.name + " (" + _plt.callsign + ")" + _stat_tag + " - Acc: " + string(_plt.combat_stat * 10) + "% | Sal: " + string(_plt.salary_daily) + " Cr");
            }

            // Available Hire Candidates
            var _hire_y = _py_start + array_length(_gm.facilities.roster_pilots) * 30 + 30;
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_col2_x + 16, _hire_y, "FREE AGENT PILOT REGISTRY (HIRE MARKET):");

            for (var h = 0; h < array_length(_gm.facilities.available_hire_pilots); h++) {
                var _cand = _gm.facilities.available_hire_pilots[h];
                var _cy = _hire_y + 26 + h * 68;

                draw_set_color(make_color_rgb(16, 24, 34));
                draw_rectangle(_col2_x + 16, _cy, _col2_x + _col2_w - 16, _cy + 60, false);
                draw_set_color(make_color_rgb(45, 75, 110));
                draw_rectangle(_col2_x + 16, _cy, _col2_x + _col2_w - 16, _cy + 60, true);

                draw_set_color(make_color_rgb(240, 210, 100));
                draw_text(_col2_x + 24, _cy + 8, _cand.name + " [" + _cand.callsign + "] - " + _cand.background);
                draw_set_color(c_white);
                draw_text(_col2_x + 24, _cy + 24, "Combat Rating: " + string(_cand.combat_stat) + " | Tactics Rating: " + string(_cand.tactics_stat) + " | Salary: " + string(_cand.salary_daily) + " Cr/day");
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_col2_x + 24, _cy + 40, "Signing Bonus: " + string(_cand.signing_bonus) + " Cr");

                // Hire Button
                var _hbtn_x = _col2_x + _col2_w - 150;
                var _hbtn_y = _cy + 14;
                var _h_hov = (_mx >= _hbtn_x && _mx <= _hbtn_x + 130 && _my >= _hbtn_y && _my <= _hbtn_y + 32);
                if (_h_hov && _click) {
                    if (_gm.spend_funds(_cand.signing_bonus)) {
                        array_push(_gm.facilities.roster_pilots, _cand);
                        array_delete(_gm.facilities.available_hire_pilots, h, 1);
                        show_toast("NEW ACE COMMISSIONED: " + _cand.name + " joined squad!", c_lime);
                        break;
                    } else {
                        show_toast("INSUFFICIENT FUNDS! Need " + string(_cand.signing_bonus) + " Cr", c_red);
                    }
                }
                draw_set_color(_h_hov ? make_color_rgb(20, 80, 40) : make_color_rgb(12, 45, 22));
                draw_rectangle(_hbtn_x, _hbtn_y, _hbtn_x + 130, _hbtn_y + 32, false);
                draw_set_color(make_color_rgb(80, 220, 120));
                draw_rectangle(_hbtn_x, _hbtn_y, _hbtn_x + 130, _hbtn_y + 32, true);
                draw_set_color(c_white);
                draw_text(_hbtn_x + 12, _hbtn_y + 8, "[HIRE PILOT]");
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
        draw_text(_pf_x, _pf_y, "== MODULAR PART FABRICATOR // ALLOY COMPONENT FORGE (docs/13) ==");
        draw_set_color(make_color_rgb(160, 190, 220));
        draw_text(_pf_x, _pf_y + 18, "Forge high-performance modular components from synthesized alloys for custom mobile suit combinations!");

        if (instance_exists(obj_GameManager)) {
            var _gm = obj_GameManager;

            // Alloy Stockpile Header Banner
            var _sb_y = _pf_y + 40;
            var _sb_w = _pan_w - 60;
            draw_set_color(make_color_rgb(12, 18, 28));
            draw_rectangle(_pf_x, _sb_y, _pf_x + _sb_w, _sb_y + 36, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_pf_x, _sb_y, _pf_x + _sb_w, _sb_y + 36, true);

            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_pf_x + 14, _sb_y + 10, "AVAILABLE ALLOY STOCKPILE:");
            scr_draw_alloy_swatch(_pf_x + 230, _sb_y + 8, 20, 14, "alloy_vanguard_comp");
            draw_set_color(make_color_rgb(100, 240, 140));
            draw_text(_pf_x + 256, _sb_y + 10, "Vanguard: " + string(_gm.get_alloy("alloy_vanguard_comp")));
            scr_draw_alloy_swatch(_pf_x + 400, _sb_y + 8, 20, 14, "alloy_hyperion_matrix");
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_pf_x + 426, _sb_y + 10, "Hyperion: " + string(_gm.get_alloy("alloy_hyperion_matrix")));
            scr_draw_alloy_swatch(_pf_x + 570, _sb_y + 8, 20, 14, "alloy_aerosteel_flux");
            draw_set_color(make_color_rgb(220, 140, 255));
            draw_text(_pf_x + 596, _sb_y + 10, "Aerosteel: " + string(_gm.get_alloy("alloy_aerosteel_flux")));
            scr_draw_alloy_swatch(_pf_x + 740, _sb_y + 8, 20, 14, "alloy_adamantine_carbide");
            draw_set_color(make_color_rgb(255, 160, 90));
            draw_text(_pf_x + 766, _sb_y + 10, "Adamantine: " + string(_gm.get_alloy("alloy_adamantine_carbide")));

            // Slot Selector Bar (6 slots)
            var _slot_names = [
                "[1. HEAD SENSORS]",
                "[2. TORSO CORES]",
                "[3. ARMS ACTUATORS]",
                "[4. LEGS HYDRAULICS]",
                "[5. BACKPACK BOOSTERS]",
                "[6. PRIMARY WEAPONS]"
            ];
            var _sl_w = 188;
            var _sl_y = _sb_y + 46;

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
                draw_text(_slx + 10, _sl_y + 6, _slot_names[sl]);
            }

            // 3 Blueprint Cards for the selected slot
            var _cat_parts = modular_crafting_catalog[forge_selected_slot];
            var _card_w = 380;
            var _card_h = 360;
            var _card_y = _sl_y + 40;

            for (var ci = 0; ci < array_length(_cat_parts); ci++) {
                var _pitem = _cat_parts[ci];
                var _cx = _pf_x + ci * (_card_w + 20);

                draw_set_color(make_color_rgb(14, 20, 30));
                draw_rectangle(_cx, _card_y, _cx + _card_w, _card_y + _card_h, false);
                draw_set_color(make_color_rgb(45, 75, 110));
                draw_rectangle(_cx, _card_y, _cx + _card_w, _card_y + _card_h, true);

                // Part Title
                draw_set_color(make_color_rgb(240, 215, 100));
                draw_text(_cx + 16, _card_y + 14, _pitem.name);
                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text(_cx + 16, _card_y + 36, "Classification: " + string_upper(_pitem.slot));

                // Stats Box
                var _st_y = _card_y + 64;
                draw_set_color(make_color_rgb(10, 14, 22));
                draw_rectangle(_cx + 14, _st_y, _cx + _card_w - 14, _st_y + 130, false);
                draw_set_color(make_color_rgb(30, 50, 75));
                draw_rectangle(_cx + 14, _st_y, _cx + _card_w - 14, _st_y + 130, true);

                draw_set_color(c_white);
                draw_text(_cx + 24, _st_y + 10, "Armor Integrity: " + string(_pitem.armor) + " HP");
                draw_text(_cx + 24, _st_y + 30, "Component Mass: " + string(_pitem.mass) + " Tonnes");

                if (variable_struct_exists(_pitem, "power_output")) {
                    draw_set_color(make_color_rgb(100, 255, 140));
                    draw_text(_cx + 24, _st_y + 50, "Reactor Output: +" + string(_pitem.power_output) + " MW Surplus");
                } else {
                    draw_set_color(make_color_rgb(255, 180, 100));
                    draw_text(_cx + 24, _st_y + 50, "Reactor Power Draw: -" + string(_pitem.power_draw) + " MW");
                }

                if (variable_struct_exists(_pitem, "base_speed")) {
                    draw_set_color(c_white);
                    draw_text(_cx + 24, _st_y + 70, "Base Walk Speed: " + string(_pitem.base_speed) + " kph");
                } else if (variable_struct_exists(_pitem, "boost_bonus")) {
                    draw_set_color(c_white);
                    draw_text(_cx + 24, _st_y + 70, "Vernier Boost: +" + string(_pitem.boost_bonus) + " kph");
                } else if (variable_struct_exists(_pitem, "damage")) {
                    draw_set_color(make_color_rgb(255, 120, 120));
                    draw_text(_cx + 24, _st_y + 70, "Weapon Firepower: " + string(_pitem.damage) + " Dmg Rating");
                }

                draw_set_color(make_color_rgb(255, 215, 80));
                draw_text(_cx + 24, _st_y + 95, "Bonus: " + _pitem.bonus);

                // Material & Credit Costs
                var _cost_y = _st_y + 145;
                var _cur_alloy_stock = _gm.get_alloy(_pitem.req_alloy);
                var _has_alloy = (_cur_alloy_stock >= _pitem.req_alloy_amount);
                var _has_cr = (_gm.funds >= _pitem.cost_cr);
                var _can_forge = (_has_alloy && _has_cr);

                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text(_cx + 16, _cost_y, "REQUIRED ALLOY:");
                scr_draw_alloy_swatch(_cx + 16, _cost_y + 20, 22, 16, _pitem.req_alloy);
                draw_set_color(_has_alloy ? c_lime : c_red);
                draw_text(_cx + 44, _cost_y + 20, string(_pitem.req_alloy_amount) + "x " + _pitem.req_alloy + " (Stock: " + string(_cur_alloy_stock) + ")");

                draw_set_color(_has_cr ? c_white : c_red);
                draw_text(_cx + 16, _cost_y + 40, "Fabrication Cost: " + string(_pitem.cost_cr) + " Cr");

                // Forge Button
                var _fb_y = _cost_y + 68;
                var _fb_w = _card_w - 32;
                var _fb_h = 36;
                var _fb_hov = (_mx >= _cx + 16 && _mx <= _cx + 16 + _fb_w && _my >= _fb_y && _my <= _fb_y + _fb_h);
                if (_fb_hov && _click && _can_forge) {
                    _gm.craft_modular_part(_pitem, _pitem.req_alloy, _pitem.req_alloy_amount, _pitem.cost_cr);
                }
                draw_set_color(_can_forge ? (_fb_hov ? make_color_rgb(25, 95, 55) : make_color_rgb(16, 60, 34)) : make_color_rgb(40, 20, 20));
                draw_rectangle(_cx + 16, _fb_y, _cx + 16 + _fb_w, _fb_y + _fb_h, false);
                draw_set_color(_can_forge ? make_color_rgb(60, 240, 120) : make_color_rgb(160, 50, 50));
                draw_rectangle(_cx + 16, _fb_y, _cx + 16 + _fb_w, _fb_y + _fb_h, true);
                draw_set_color(c_white);
                draw_text(_cx + 60, _fb_y + 10, _can_forge ? ">> FORGE THIS COMPONENT <<" : "[INSUFFICIENT RESOURCES]");
            }
        }
    }

    // =========================================================================
    // SUBTAB 2: CUSTOM MECH COMBINATIONS ASSEMBLY BAY (docs/13)
    // =========================================================================
    else if (factory_subtab == 2) {
        var _ab_x = _pan_x + 30;
        var _ab_y = _pan_y + 44;

        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(_ab_x, _ab_y, "== CUSTOM MOBILE SUIT COMBINATIONS & ASSEMBLY BAY (docs/13) ==");
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

            // Left Column: The 6 Equipped Modular Component Slots
            var _col1_w = 580;
            var _col1_h = 580;
            var _col1_y = _ab_y + 40;

            draw_set_color(make_color_rgb(12, 18, 28));
            draw_rectangle(_ab_x, _col1_y, _ab_x + _col1_w, _col1_y + _col1_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_ab_x, _col1_y, _ab_x + _col1_w, _col1_y + _col1_h, true);

            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_ab_x + 16, _col1_y + 12, "CHASSIS MODULAR HARDPOINTS & LOADOUT:");

            // Slot Cards (6 slots)
            var _slot_items = [
                { title: "SLOT 1: HEAD SENSORS", part: _hd, list: _pts.heads, cur_idx: assembly_head_idx, key: "head" },
                { title: "SLOT 2: TORSO REACTOR CORE", part: _tr, list: _pts.torsos, cur_idx: assembly_torso_idx, key: "torso" },
                { title: "SLOT 3: ARMS & ACTUATORS", part: _am, list: _pts.arms, cur_idx: assembly_arms_idx, key: "arms" },
                { title: "SLOT 4: LEGS & HYDRAULICS", part: _lg, list: _pts.legs, cur_idx: assembly_legs_idx, key: "legs" },
                { title: "SLOT 5: BACKPACK THRUSTERS", part: _bp, list: _pts.backpacks, cur_idx: assembly_bp_idx, key: "backpack" },
                { title: "SLOT 6: PRIMARY WEAPON", part: _wp, list: _pts.weapons, cur_idx: assembly_wp_idx, key: "weapon" }
            ];

            for (var si = 0; si < 6; si++) {
                var _sitem = _slot_items[si];
                var _sy_pos = _col1_y + 38 + si * 88;

                draw_set_color(make_color_rgb(16, 24, 36));
                draw_rectangle(_ab_x + 14, _sy_pos, _ab_x + _col1_w - 14, _sy_pos + 80, false);
                draw_set_color(make_color_rgb(45, 75, 110));
                draw_rectangle(_ab_x + 14, _sy_pos, _ab_x + _col1_w - 14, _sy_pos + 80, true);

                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_ab_x + 22, _sy_pos + 8, _sitem.title);

                var _p = _sitem.part;
                if (!is_undefined(_p)) {
                    draw_set_color(c_white);
                    draw_text(_ab_x + 22, _sy_pos + 26, _p.name);
                    draw_set_color(make_color_rgb(160, 190, 220));
                    var _stat_str = "Armor: " + string(_p.armor) + " | Mass: " + string(_p.mass) + "t";
                    if (variable_struct_exists(_p, "power_output")) _stat_str += " | Output: +" + string(_p.power_output) + " MW";
                    else _stat_str += " | Draw: -" + string(_p.power_draw) + " MW";
                    draw_text(_ab_x + 22, _sy_pos + 44, _stat_str);
                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_ab_x + 22, _sy_pos + 60, "Effect: " + _p.bonus);
                } else {
                    draw_set_color(c_red);
                    draw_text(_ab_x + 22, _sy_pos + 36, "[NO PART IN INVENTORY - FORGE IN PART FORGE]");
                }

                // Cycle Buttons
                var _len = array_length(_sitem.list);
                var _btn_p_hov = (_mx >= _ab_x + 420 && _mx <= _ab_x + 480 && _my >= _sy_pos + 24 && _my <= _sy_pos + 52);
                if (_btn_p_hov && _click && _len > 1) {
                    if (si == 0) assembly_head_idx = (assembly_head_idx - 1 + _len) % _len;
                    else if (si == 1) assembly_torso_idx = (assembly_torso_idx - 1 + _len) % _len;
                    else if (si == 2) assembly_arms_idx = (assembly_arms_idx - 1 + _len) % _len;
                    else if (si == 3) assembly_legs_idx = (assembly_legs_idx - 1 + _len) % _len;
                    else if (si == 4) assembly_bp_idx = (assembly_bp_idx - 1 + _len) % _len;
                    else if (si == 5) assembly_wp_idx = (assembly_wp_idx - 1 + _len) % _len;
                }
                draw_set_color(_btn_p_hov ? make_color_rgb(30, 60, 90) : make_color_rgb(18, 30, 48));
                draw_rectangle(_ab_x + 420, _sy_pos + 24, _ab_x + 480, _sy_pos + 52, false);
                draw_set_color(make_color_rgb(80, 180, 255));
                draw_rectangle(_ab_x + 420, _sy_pos + 24, _ab_x + 480, _sy_pos + 52, true);
                draw_set_color(c_white);
                draw_text(_ab_x + 430, _sy_pos + 30, "< PREV");

                var _btn_n_hov = (_mx >= _ab_x + 495 && _mx <= _ab_x + 555 && _my >= _sy_pos + 24 && _my <= _sy_pos + 52);
                if (_btn_n_hov && _click && _len > 1) {
                    if (si == 0) assembly_head_idx = (assembly_head_idx + 1) % _len;
                    else if (si == 1) assembly_torso_idx = (assembly_torso_idx + 1) % _len;
                    else if (si == 2) assembly_arms_idx = (assembly_arms_idx + 1) % _len;
                    else if (si == 3) assembly_legs_idx = (assembly_legs_idx + 1) % _len;
                    else if (si == 4) assembly_bp_idx = (assembly_bp_idx + 1) % _len;
                    else if (si == 5) assembly_wp_idx = (assembly_wp_idx + 1) % _len;
                }
                draw_set_color(_btn_n_hov ? make_color_rgb(30, 60, 90) : make_color_rgb(18, 30, 48));
                draw_rectangle(_ab_x + 495, _sy_pos + 24, _ab_x + 555, _sy_pos + 52, false);
                draw_set_color(make_color_rgb(80, 180, 255));
                draw_rectangle(_ab_x + 495, _sy_pos + 24, _ab_x + 555, _sy_pos + 52, true);
                draw_set_color(c_white);
                draw_text(_ab_x + 505, _sy_pos + 30, "NEXT >");
            }

            // Right Column: Engineering Calculus & Commissioning Bay
            var _col2_x = _ab_x + _col1_w + 20;
            var _col2_w = 600;
            draw_set_color(make_color_rgb(12, 18, 28));
            draw_rectangle(_col2_x, _col1_y, _col2_x + _col2_w, _col1_y + _col1_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_col2_x, _col1_y, _col2_x + _col2_w, _col1_y + _col1_h, true);

            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_col2_x + 18, _col1_y + 12, "REAL-TIME DIAGNOSTICS & SYSTEM COMBINATIONS CALCULUS:");

            // Suit Call Designation & Preset Buttons
            draw_set_color(c_white);
            draw_text(_col2_x + 18, _col1_y + 36, "Designation: " + assembly_custom_name);

            var _presets = ["CHIMERA-X", "AEGIS-II", "VALKYRIE-S", "COLOSSUS-M"];
            var _pw = 120;
            for (var pr = 0; pr < 4; pr++) {
                var _px = _col2_x + 18 + pr * (_pw + 10);
                var _py = _col1_y + 58;
                var _p_hov = (_mx >= _px && _mx <= _px + _pw && _my >= _py && _my <= _py + 26);
                if (_p_hov && _click) {
                    assembly_custom_name = _presets[pr];
                }
                draw_set_color(_p_hov ? make_color_rgb(30, 55, 80) : make_color_rgb(16, 26, 38));
                draw_rectangle(_px, _py, _px + _pw, _py + 26, false);
                draw_set_color(make_color_rgb(60, 120, 180));
                draw_rectangle(_px, _py, _px + _pw, _py + 26, true);
                draw_set_color(c_white);
                draw_text(_px + 12, _py + 5, "[" + _presets[pr] + "]");
            }

            // Real-Time Engineering Calculations
            if (_has_all_6) {
                var _total_armor = _hd.armor + _tr.armor + _am.armor + _lg.armor + _bp.armor + _wp.armor;
                var _power_draw = _hd.power_draw + _am.power_draw + _lg.power_draw + _bp.power_draw + _wp.power_draw;
                var _net_power = _tr.power_output - _power_draw;
                var _total_mass = _hd.mass + _tr.mass + _am.mass + _lg.mass + _bp.mass + _wp.mass;
                var _walk_speed = max(20, floor(_lg.base_speed * (1.0 - (_total_mass / 220.0))));
                var _boost_speed = _walk_speed + _bp.boost_bonus;
                var _combat_rating = floor((_total_armor / 5) + _wp.damage + (_boost_speed / 2) + (_net_power * 3));

                var _diag_y = _col1_y + 100;

                // 1. Armor Meter
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_col2_x + 18, _diag_y, "1. COMBINED ARMOR INTEGRITY:");
                draw_set_color(c_white);
                draw_text(_col2_x + 360, _diag_y, string(_total_armor) + " HP / 2,000 HP");
                draw_set_color(make_color_rgb(18, 30, 48));
                draw_rectangle(_col2_x + 18, _diag_y + 20, _col2_x + _col2_w - 18, _diag_y + 30, false);
                draw_set_color(make_color_rgb(60, 180, 240));
                draw_rectangle(_col2_x + 18, _diag_y + 20, _col2_x + 18 + ((_col2_w - 36) * clamp(_total_armor / 2000.0, 0, 1)), _diag_y + 30, false);

                // 2. Power Balance Meter (The core physics rule!)
                var _p_diag_y = _diag_y + 44;
                var _is_power_stable = (_net_power >= 0);
                draw_set_color(_is_power_stable ? make_color_rgb(100, 255, 140) : make_color_rgb(255, 90, 90));
                draw_text(_col2_x + 18, _p_diag_y, "2. TOKAMAK FUSION POWER BALANCE:");
                draw_text(_col2_x + 340, _p_diag_y, "Surplus: " + string(_net_power) + " MW (Core: " + string(_tr.power_output) + " MW, Draw: " + string(_power_draw) + " MW)");

                draw_set_color(make_color_rgb(18, 30, 48));
                draw_rectangle(_col2_x + 18, _p_diag_y + 20, _col2_x + _col2_w - 18, _p_diag_y + 30, false);
                draw_set_color(_is_power_stable ? make_color_rgb(80, 220, 120) : make_color_rgb(240, 60, 60));
                var _pw_norm = _is_power_stable ? clamp(_net_power / 30.0, 0.05, 1.0) : 1.0;
                draw_rectangle(_col2_x + 18, _p_diag_y + 20, _col2_x + 18 + ((_col2_w - 36) * _pw_norm), _p_diag_y + 30, false);

                if (!_is_power_stable) {
                    draw_set_color(make_color_rgb(255, 70, 70));
                    draw_text(_col2_x + 18, _p_diag_y + 34, "!! REACTOR OVERLOAD WARNING: POWER DRAW EXCEEDS CORE OUTPUT !!");
                }

                // 3. Mass & Mobility
                var _m_diag_y = _p_diag_y + 55;
                draw_set_color(make_color_rgb(200, 220, 240));
                draw_text(_col2_x + 18, _m_diag_y, "3. MASS & SPEED DYNAMICS:");
                draw_set_color(c_white);
                draw_text(_col2_x + 18, _m_diag_y + 20, "Total Mass: " + string(_total_mass) + " Tonnes   |   Walk: " + string(_walk_speed) + " kph   |   Boost: " + string(_boost_speed) + " kph");

                // 4. Armament Firepower
                var _w_diag_y = _m_diag_y + 48;
                draw_set_color(make_color_rgb(255, 180, 100));
                draw_text(_col2_x + 18, _w_diag_y, "4. PRIMARY WEAPON ARSENAL:");
                draw_set_color(c_white);
                draw_text(_col2_x + 18, _w_diag_y + 20, _wp.name + " (" + string(_wp.damage) + " Dmg Rating) - " + _wp.bonus);

                // 5. Tactical Rating Banner
                var _t_diag_y = _w_diag_y + 50;
                draw_set_color(make_color_rgb(16, 26, 38));
                draw_rectangle(_col2_x + 18, _t_diag_y, _col2_x + _col2_w - 18, _t_diag_y + 60, false);
                draw_set_color(make_color_rgb(255, 215, 80));
                draw_rectangle(_col2_x + 18, _t_diag_y, _col2_x + _col2_w - 18, _t_diag_y + 60, true);

                draw_set_color(make_color_rgb(255, 225, 100));
                draw_text(_col2_x + 30, _t_diag_y + 12, "PROJECTED TACTICAL COMBAT RATING: " + string(_combat_rating) + " PTS");
                draw_set_color(make_color_rgb(100, 240, 160));
                draw_text(_col2_x + 30, _t_diag_y + 34, "Ready for Strategic Sorties, Sector Offensives & Mass-Production Licensure!");

                // Commission Button
                var _com_y = _t_diag_y + 80;
                var _com_w = _col2_w - 36;
                var _com_h = 52;
                var _can_com = _is_power_stable;
                var _com_hov = (_mx >= _col2_x + 18 && _mx <= _col2_x + 18 + _com_w && _my >= _com_y && _my <= _com_y + _com_h);

                if (_com_hov && _click) {
                    if (!_can_com) {
                        show_toast("ASSEMBLY REJECTED: Resolve Reactor Overload first!", c_red);
                    } else {
                        _gm.assemble_custom_mech(assembly_custom_name, assembly_head_idx, assembly_torso_idx, assembly_arms_idx, assembly_legs_idx, assembly_bp_idx, assembly_wp_idx);
                    }
                }

                draw_set_color(_can_com ? (_com_hov ? make_color_rgb(25, 95, 55) : make_color_rgb(16, 60, 34)) : make_color_rgb(40, 20, 20));
                draw_rectangle(_col2_x + 18, _com_y, _col2_x + 18 + _com_w, _com_y + _com_h, false);
                draw_set_color(_can_com ? make_color_rgb(60, 240, 120) : make_color_rgb(160, 50, 50));
                draw_rectangle(_col2_x + 18, _com_y, _col2_x + 18 + _com_w, _com_y + _com_h, true);

                draw_set_color(c_white);
                if (_can_com) {
                    draw_text(_col2_x + 80, _com_y + 16, ">> COMMISSION CUSTOM COMBINATION INTO HANGAR <<");
                } else {
                    draw_text(_col2_x + 65, _com_y + 16, "[CANNOT COMMISSION: RESOLVE REACTOR OVERLOAD]");
                }

                // Quick Shortcut to Fly-Off Trials (docs/15)
                var _fly_nav_y = _com_y + _com_h + 10;
                var _fly_nav_h = 36;
                var _fly_nav_hov = (_mx >= _col2_x + 18 && _mx <= _col2_x + 18 + _com_w && _my >= _fly_nav_y && _my <= _fly_nav_y + _fly_nav_h);
                if (_fly_nav_hov && _click) {
                    active_tab = 2;
                    contracts_subtab = 1;
                    show_toast("TRANSFERRED TO FLY-OFF PROCUREMENT ARENA!", c_aqua);
                }
                draw_set_color(_fly_nav_hov ? make_color_rgb(25, 55, 88) : make_color_rgb(16, 32, 52));
                draw_rectangle(_col2_x + 18, _fly_nav_y, _col2_x + 18 + _com_w, _fly_nav_y + _fly_nav_h, false);
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_rectangle(_col2_x + 18, _fly_nav_y, _col2_x + 18 + _com_w, _fly_nav_y + _fly_nav_h, true);
                draw_set_color(c_white);
                draw_text(_col2_x + 60, _fly_nav_y + 10, ">> ENTER SUITS INTO FACTION PROCUREMENT FLY-OFF TRIALS (TAB 2) <<");
            } else {
                draw_set_color(c_red);
                draw_text(_col2_x + 18, _col1_y + 120, "PARTS MISSING: Must equip all 6 component slots to compute diagnostics!");
            }
        }
    }
}
else if (active_tab == 2) {
    // 3 Subtabs: Contracts & Bounties (Doc 04), Fly-Off Procurement Trials (Doc 15), Commodity Trade Exchange (Doc 15)
    var _csub_w = 370;
    var _csub_y = _pan_y + 8;
    var _csub_names = [
        "[A. CONTRACTS & BOUNTIES]",
        "[B. FLY-OFF PROCUREMENT TRIALS]",
        "[C. INTERSTELLAR TRADE EXCHANGE]"
    ];
    for (var cst = 0; cst < 3; cst++) {
        var _csx = _pan_x + 30 + cst * (_csub_w + 14);
        var _cst_active = (contracts_subtab == cst);
        var _cst_hov = (_mx >= _csx && _mx <= _csx + _csub_w && _my >= _csub_y && _my <= _csub_y + 30);
        if (_cst_hov && _click) contracts_subtab = cst;

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
        draw_text(_cb_x, _cb_y, "== FACTION CONTRACT BOARD & DELIVERIES (docs/04) ==");

        // Faction Standing Meters
        if (instance_exists(obj_FactionManager)) {
            var _fm = obj_FactionManager;
            var _std_y = _cb_y + 24;
            var _f_list = ["faction_a", "faction_b", "faction_c", "faction_d"];
            var _f_box_w = 280;
            for (var f = 0; f < 4; f++) {
                var _fid = _f_list[f];
                if (!variable_struct_exists(_fm.factions, _fid)) continue;
                var _finfo = _fm.factions[$ _fid];
                var _std = _fm.get_standing(_fid);
                var _fx = _cb_x + f * (_f_box_w + 14);

                draw_set_color(make_color_rgb(14, 20, 28));
                draw_rectangle(_fx, _std_y, _fx + _f_box_w, _std_y + 44, false);
                draw_set_color(make_color_rgb(40, 65, 95));
                draw_rectangle(_fx, _std_y, _fx + _f_box_w, _std_y + 44, true);

                draw_set_color(make_color_rgb(240, 210, 100));
                draw_text(_fx + 10, _std_y + 6, _finfo.name);
                var _std_col = (_std > 20) ? c_lime : ((_std < -10) ? c_red : make_color_rgb(240, 200, 80));
                draw_set_color(_std_col);
                draw_text(_fx + 10, _std_y + 24, "Standing: " + string(_std) + " (" + _finfo.standing_title + ")");
            }

            // Active vs Available Contracts
            var _c_disp_y = _std_y + 54;

            // 1. Available Contracts
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_cb_x, _c_disp_y, "AVAILABLE FACTION CONTRACT OFFERINGS:");
            for (var ac = 0; ac < array_length(_fm.available_contracts); ac++) {
                var _cnt = _fm.available_contracts[ac];
                var _cy = _c_disp_y + 24 + ac * 82;
                var _cw = 1160;

                draw_set_color(make_color_rgb(12, 18, 26));
                draw_rectangle(_cb_x, _cy, _cb_x + _cw, _cy + 74, false);
                draw_set_color(make_color_rgb(35, 60, 90));
                draw_rectangle(_cb_x, _cy, _cb_x + _cw, _cy + 74, true);

                draw_set_color(make_color_rgb(255, 215, 80));
                draw_text(_cb_x + 14, _cy + 8, _cnt.title);
                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text(_cb_x + 14, _cy + 28, _cnt.briefing);

                draw_set_color(make_color_rgb(100, 255, 140));
                draw_text(_cb_x + 14, _cy + 48, "Payout: " + string(_cnt.payout_credits) + " Cr | Standing: +" + string(_cnt.reputation_gain) + " | Deadline: " + string(_cnt.deadline_days) + " Days");

                // Accept Button
                var _ab_x = _cb_x + _cw - 150;
                var _ab_y = _cy + 16;
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
                    draw_text(_cb_x + 14, _acy + 8, _acnt.title + " [FACTION: " + _acnt.faction_name + "]");
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
        draw_text(_tr_x, _tr_y, "== FACTION PROCUREMENT TRIALS & COMPETITIVE FLY-OFF ARENA (docs/15) ==");
        draw_set_color(make_color_rgb(160, 190, 220));
        draw_text(_tr_x, _tr_y + 18, "Submit custom mobile suits to competitive fly-offs against faction flagship models. Outperform the incumbent to REPLACE their doctrine, earning upfront bounties & daily royalties!");

        if (instance_exists(obj_FactionManager) && instance_exists(obj_GameManager)) {
            var _fm = obj_FactionManager;
            var _gm = obj_GameManager;
            var _mpc = _fm.mass_production_contracts;
            var _f_list = ["faction_a", "faction_b", "faction_c", "faction_d"];
            var _f_card_w = 280;
            var _f_card_h = 135;

            // 1. The 4 Target Faction Cards
            for (var fc = 0; fc < 4; fc++) {
                var _fid = _f_list[fc];
                if (!variable_struct_exists(_mpc, _fid)) continue;
                var _mp = _mpc[$ _fid];
                var _std = _fm.get_standing(_fid);
                var _card_x = _tr_x + fc * (_f_card_w + 13);
                var _card_y = _tr_y + 40;
                var _is_sel = (trial_selected_faction == _fid);
                var _c_hov = (_mx >= _card_x && _mx <= _card_x + _f_card_w && _my >= _card_y && _my <= _card_y + _f_card_h);
                if (_c_hov && _click) {
                    trial_selected_faction = _fid;
                    trial_last_result = undefined;
                }

                draw_set_color(make_color_rgb(14, 20, 28));
                draw_rectangle(_card_x, _card_y, _card_x + _f_card_w, _card_y + _f_card_h, false);
                draw_set_color(_is_sel ? make_color_rgb(255, 215, 80) : (_mp.replaced ? make_color_rgb(60, 220, 120) : make_color_rgb(45, 75, 110)));
                draw_rectangle(_card_x, _card_y, _card_x + _f_card_w, _card_y + _f_card_h, true);

                draw_set_color(make_color_rgb(240, 215, 100));
                draw_text(_card_x + 10, _card_y + 8, _mp.faction_name);

                var _std_col = (_std >= 20) ? c_lime : ((_std < -10) ? c_red : c_yellow);
                draw_set_color(_std_col);
                draw_text(_card_x + 10, _card_y + 26, "Standing: " + string(_std));

                if (_mp.replaced) {
                    draw_set_color(make_color_rgb(60, 240, 120));
                    draw_text(_card_x + 10, _card_y + 46, "[DOCTRINE: " + _mp.replacement_name + "]");
                    draw_set_color(make_color_rgb(100, 255, 160));
                    draw_text(_card_x + 10, _card_y + 66, "Royalty: +" + string(_mp.royalty_per_turn) + " Cr/turn");
                    draw_text(_card_x + 10, _card_y + 84, "Total Earned: " + string(_mp.cumulative_royalties_paid) + " Cr");
                } else {
                    draw_set_color(make_color_rgb(240, 160, 50));
                    draw_text(_card_x + 10, _card_y + 46, "Incumbent: " + _mp.baseline_suit_name);
                    draw_set_color(make_color_rgb(80, 220, 255));
                    draw_text(_card_x + 10, _card_y + 66, "License Bounty: +" + string(_mp.licensing_bounty) + " Cr");
                    draw_text(_card_x + 10, _card_y + 84, "Daily Royalty: +" + string(_mp.royalty_per_turn) + " Cr/turn");
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
                    }

                    draw_set_color(_m_sel ? make_color_rgb(20, 50, 75) : (_m_hov ? make_color_rgb(16, 32, 48) : make_color_rgb(12, 18, 26)));
                    draw_rectangle(_tr_x + 8, _my_box, _tr_x + _col1_w - 8, _my_box + 70, false);
                    draw_set_color(_m_sel ? make_color_rgb(100, 220, 255) : make_color_rgb(40, 65, 95));
                    draw_rectangle(_tr_x + 8, _my_box, _tr_x + _col1_w - 8, _my_box + 70, true);

                    draw_set_color(_m_sel ? make_color_rgb(255, 220, 100) : c_white);
                    draw_text(_tr_x + 14, _my_box + 6, _mitem.name);
                    draw_set_color(make_color_rgb(160, 190, 220));
                    draw_text(_tr_x + 14, _my_box + 24, "Class: " + (_mitem[$ "class"] ?? "Mobile Suit") + " | Status: " + _mitem.status);
                    draw_set_color(make_color_rgb(80, 220, 140));
                    draw_text(_tr_x + 14, _my_box + 44, "Armor: " + string(_mitem.armor_rating) + " | Output: +" + string(_mitem.power_output) + " MW | Spd: " + string(_mitem.speed) + " | CR: " + string(_mitem.combat_rating));
                }
            }

            // Right Box: Fly-Off Diagnostic & Benchmark Arena
            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_col2_x, _arena_y, _col2_x + _col2_w, _arena_y + _arena_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_col2_x, _arena_y, _col2_x + _col2_w, _arena_y + _arena_h, true);

            var _inc = _fm.get_incumbent_specs(trial_selected_faction);
            var _cur_cand = (trial_selected_mech_idx >= 0 && trial_selected_mech_idx < array_length(_mechs)) ? _mechs[trial_selected_mech_idx] : undefined;

            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_col2_x + 14, _arena_y + 10, "FLY-OFF BENCHMARK ARENA: " + _inc.faction_name);
            draw_set_color(make_color_rgb(160, 190, 220));
            draw_text(_col2_x + 14, _arena_y + 28, "Evaluator: " + _inc.evaluator + " | Doctrine: " + _inc.doctrine_focus);

            // Side-by-side comparison table
            var _cmp_y = _arena_y + 52;
            draw_set_color(make_color_rgb(14, 24, 36));
            draw_rectangle(_col2_x + 12, _cmp_y, _col2_x + _col2_w - 12, _cmp_y + 130, false);
            draw_set_color(make_color_rgb(45, 75, 110));
            draw_rectangle(_col2_x + 12, _cmp_y, _col2_x + _col2_w - 12, _cmp_y + 130, true);

            // Column Headers
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_col2_x + 24, _cmp_y + 8, "METRIC");
            draw_text(_col2_x + 240, _cmp_y + 8, "CANDIDATE: " + (!is_undefined(_cur_cand) ? _cur_cand.name : "None"));
            draw_text(_col2_x + 500, _cmp_y + 8, "INCUMBENT: " + _inc.name);

            // Metrics: Armor, Power, Speed, Combat Rating
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
                var _ry = _cmp_y + 30 + r * 24;
                var _rw = _rows[r];
                draw_set_color(make_color_rgb(180, 200, 220));
                draw_text(_col2_x + 24, _ry, _rw.label);
                draw_set_color(_rw.pass ? c_lime : make_color_rgb(240, 160, 60));
                draw_text(_col2_x + 240, _ry, _rw.c_val);
                draw_set_color(make_color_rgb(200, 200, 200));
                draw_text(_col2_x + 500, _ry, _rw.i_val);
            }

            // Fly-Off Test Simulation Button
            var _fly_btn_y = _cmp_y + 140;
            var _fly_btn_w = _col2_w - 24;
            var _fly_btn_h = 44;
            var _can_fly = (!is_undefined(_cur_cand));
            var _fly_hov = (_mx >= _col2_x + 12 && _mx <= _col2_x + 12 + _fly_btn_w && _my >= _fly_btn_y && _my <= _fly_btn_y + _fly_btn_h);

            if (_fly_hov && _click) {
                if (_can_fly) {
                    trial_last_result = _fm.run_procurement_trial(trial_selected_faction, _cur_cand);
                    if (trial_last_result.passed) {
                        show_toast("TRIAL SUCCESS: " + _cur_cand.name + " OUTPERFORMED " + _inc.name + "! (" + string(trial_last_result.composite_score) + "/100)", c_lime);
                    } else {
                        show_toast("TRIAL DEFICIT: Candidate scored " + string(trial_last_result.composite_score) + "/100. Requirements unmet!", c_red);
                    }
                } else {
                    show_toast("SELECT A CANDIDATE MECH IN HANGAR FIRST!", c_red);
                }
            }

            draw_set_color(_can_fly ? (_fly_hov ? make_color_rgb(25, 75, 110) : make_color_rgb(18, 48, 72)) : make_color_rgb(30, 20, 20));
            draw_rectangle(_col2_x + 12, _fly_btn_y, _col2_x + 12 + _fly_btn_w, _fly_btn_y + _fly_btn_h, false);
            draw_set_color(_can_fly ? make_color_rgb(100, 220, 255) : make_color_rgb(140, 60, 60));
            draw_rectangle(_col2_x + 12, _fly_btn_y, _col2_x + 12 + _fly_btn_w, _fly_btn_y + _fly_btn_h, true);

            draw_set_color(c_white);
            draw_text(_col2_x + 160, _fly_btn_y + 13, ">> COMMENCE COMPETITIVE FLY-OFF TRIAL // RUN 4 DIAGNOSTIC PHASES <<");

            // Diagnostic Results Banner & Ratification
            if (!is_undefined(trial_last_result)) {
                var _res_y = _fly_btn_y + 52;
                var _res_w = _col2_w - 24;
                var _res_h = 175;

                draw_set_color(trial_last_result.passed ? make_color_rgb(12, 36, 20) : make_color_rgb(36, 16, 16));
                draw_rectangle(_col2_x + 12, _res_y, _col2_x + 12 + _res_w, _res_y + _res_h, false);
                draw_set_color(trial_last_result.passed ? make_color_rgb(60, 240, 120) : make_color_rgb(240, 60, 60));
                draw_rectangle(_col2_x + 12, _res_y, _col2_x + 12 + _res_w, _res_y + _res_h, true);

                draw_set_color(trial_last_result.passed ? make_color_rgb(255, 220, 100) : make_color_rgb(255, 100, 100));
                draw_text(_col2_x + 24, _res_y + 8, trial_last_result.passed ? "*** FLY-OFF VICTORY: DOCTRINE CANDIDACY QUALIFIED ***" : "!!! FLY-OFF DEFICIT: DOCTRINE CANDIDACY REJECTED !!!");

                draw_set_color(c_white);
                draw_text(_col2_x + 24, _res_y + 28, "Phase 1 Armor Stress: " + string(trial_last_result.score_armor) + "/100   |   Phase 2 Reactor Sustained: " + string(trial_last_result.score_power) + "/100");
                draw_text(_col2_x + 24, _res_y + 46, "Phase 3 High-G Mobility: " + string(trial_last_result.score_speed) + "/100   |   Phase 4 Live-Fire Combat: " + string(trial_last_result.score_combat) + "/100");
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_col2_x + 24, _res_y + 66, "Faction Standing Bonus: +" + string(trial_last_result.standing_bonus) + " pts   ==>   COMPOSITE SCORE: " + string(trial_last_result.composite_score) + " / 100.0 PTS");

                draw_set_color(trial_last_result.passed ? make_color_rgb(140, 255, 180) : make_color_rgb(255, 180, 180));
                draw_text(_col2_x + 24, _res_y + 88, trial_last_result.report);

                // Ratification Button if passed
                if (trial_last_result.passed) {
                    var _rat_btn_y = _res_y + 115;
                    var _rat_btn_w = _res_w - 24;
                    var _rat_btn_h = 48;
                    var _rat_hov = (_mx >= _col2_x + 24 && _mx <= _col2_x + 24 + _rat_btn_w && _my >= _rat_btn_y && _my <= _rat_btn_y + _rat_btn_h);

                    if (_rat_hov && _click) {
                        _fm.award_procurement_contract(trial_selected_faction, _cur_cand, trial_last_result);
                        trial_last_result = undefined;
                    }

                    draw_set_color(_rat_hov ? make_color_rgb(35, 115, 65) : make_color_rgb(22, 80, 44));
                    draw_rectangle(_col2_x + 24, _rat_btn_y, _col2_x + 24 + _rat_btn_w, _rat_btn_y + _rat_btn_h, false);
                    draw_set_color(make_color_rgb(80, 255, 140));
                    draw_rectangle(_col2_x + 24, _rat_btn_y, _col2_x + 24 + _rat_btn_w, _rat_btn_y + _rat_btn_h, true);

                    draw_set_color(c_white);
                    draw_text(_col2_x + 80, _rat_btn_y + 14, ">> RATIFY TENDER: REPLACE DOCTRINE // CLAIM +" + string(_fm.mass_production_contracts[$ trial_selected_faction].licensing_bounty) + " Cr & ROYALTIES <<");
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
        draw_text(_td_x, _td_y, "== INTERSTELLAR COMMODITY TRADE EXCHANGE (docs/15) ==");
        draw_set_color(make_color_rgb(160, 190, 220));
        draw_text(_td_x, _td_y + 18, "Exchange raw minerals, synthesized alloys, and modular components across faction trade hubs. Prices reflect ideological doctrines and diplomatic standings.");

        if (instance_exists(obj_FactionManager) && instance_exists(obj_GameManager)) {
            var _fm = obj_FactionManager;
            var _gm = obj_GameManager;
            var _f_list = ["faction_a", "faction_b", "faction_c", "faction_d"];
            var _f_tab_w = 280;

            // 1. Faction Partner Tabs
            for (var ft = 0; ft < 4; ft++) {
                var _fid = _f_list[ft];
                if (!variable_struct_exists(_fm.factions, _fid)) continue;
                var _finfo = _fm.factions[$ _fid];
                var _std = _fm.get_standing(_fid);
                var _ft_x = _td_x + ft * (_f_tab_w + 13);
                var _ft_y = _td_y + 40;
                var _ft_sel = (trade_selected_faction == _fid);
                var _ft_hov = (_mx >= _ft_x && _mx <= _ft_x + _f_tab_w && _my >= _ft_y && _my <= _ft_y + 52);
                if (_ft_hov && _click) trade_selected_faction = _fid;

                draw_set_color(_ft_sel ? make_color_rgb(25, 55, 88) : (_ft_hov ? make_color_rgb(18, 35, 55) : make_color_rgb(12, 20, 30)));
                draw_rectangle(_ft_x, _ft_y, _ft_x + _f_tab_w, _ft_y + 52, false);
                draw_set_color(_ft_sel ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 75, 110));
                draw_rectangle(_ft_x, _ft_y, _ft_x + _f_tab_w, _ft_y + 52, true);

                draw_set_color(make_color_rgb(240, 215, 100));
                draw_text(_ft_x + 10, _ft_y + 6, _finfo.name);

                var _trade_status = (_std >= 30) ? "ALLY (-15% BUY / +15% SELL)" : ((_std < 0) ? "TARIFF (+25% EMBARGO)" : "STANDARD (PARITY)");
                var _ts_col = (_std >= 30) ? c_lime : ((_std < 0) ? c_red : c_yellow);
                draw_set_color(_ts_col);
                draw_text(_ft_x + 10, _ft_y + 26, "Standing " + string(_std) + ": " + _trade_status);
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
                var _iy = _grid_y + i * 86;
                var _iw = 1160;
                var _ih = 78;

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
                    var _slot_arr = _gm.inventory.parts[$ _item.slot] ?? [];
                    for (var p = 0; p < array_length(_slot_arr); p++) {
                        if (_slot_arr[p].id == _item.id) _owned++;
                    }
                }

                // Item Name, Description, Demand
                draw_set_color(make_color_rgb(255, 215, 80));
                draw_text(_td_x + 14, _iy + 8, _item.name);
                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text(_td_x + 14, _iy + 28, _item.desc);
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
                var _sa_hov = (_mx >= _sa_x && _mx <= _sa_x + _sa_w && _my >= _b1_y && _my <= _sa_y + _sa_h);
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
        "[A. SECTOR MAP & MINING (DOC 06)]",
        "[B. FACTIONS & LIAISONS (DOC 04)]",
        "[C. DECADE MECHA LINEAGE (Y205-Y215)]",
        "[D. PMC EXPEDITION & OVERTHROW (DOC 12)]"
    ];
    var _wsub_w = 285;
    var _wsub_y = _pan_y + 8;
    for (var wst = 0; wst < 4; wst++) {
        var _wstbx = _pan_x + 16 + wst * (_wsub_w + 12);
        var _wstb_active = (war_subtab == wst);
        var _wstb_hov = (_mx >= _wstbx && _mx <= _wstbx + _wsub_w && _my >= _wsub_y && _my <= _wsub_y + 28);
        if (_wstb_hov && _click) war_subtab = wst;

        draw_set_color(_wstb_active ? make_color_rgb(30, 70, 110) : (_wstb_hov ? make_color_rgb(20, 40, 60) : make_color_rgb(14, 22, 32)));
        draw_rectangle(_wstbx + _sx, _wsub_y + _sy, _wstbx + _wsub_w + _sx, _wsub_y + 28 + _sy, false);
        draw_set_color(_wstb_active ? make_color_rgb(100, 200, 255) : make_color_rgb(45, 75, 110));
        draw_rectangle(_wstbx + _sx, _wsub_y + _sy, _wstbx + _wsub_w + _sx, _wsub_y + 28 + _sy, true);
        draw_set_color(_wstb_active ? c_white : make_color_rgb(160, 190, 220));
        draw_text(_wstbx + 14 + _sx, _wsub_y + 6 + _sy, _sub_tabs_w[wst]);
    }

    // =====================================================================
    // SUBTAB 0: ORBITAL WAR MAP & MINING OPERATIONS
    // =====================================================================
    if (war_subtab == 0) {
        var _m_x = _pan_x + 30;
        var _m_y = _pan_y + 42;

        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(_m_x, _m_y, "== STRATEGIC WAR MAP & RESOURCE EXTRACTION NODES (docs/06) ==");

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
            draw_text(_m_x + 14, _wbox_y + 8, "INTERSTELLAR SECTOR INFLUENCE & 4-FACTION WAR BALANCE (docs/04):");

            // 1. Terran Coalition (Blue)
            var _t_doc = _fm.mass_production_contracts.faction_a.replaced ? (" [DOCTRINE: " + _fm.mass_production_contracts.faction_a.replacement_name + "]") : " [DOCTRINE: GHA-07]";
            draw_set_color(make_color_rgb(180, 210, 255));
            draw_text(_m_x + 14, _wbox_y + 28, "Terran Coalition: " + string(_tc.terran_pct) + "% | Military: " + string(_fm.factions.faction_a.military_strength_score) + _t_doc);
            draw_set_color(make_color_rgb(18, 30, 48));
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
            draw_rectangle(_m_x + 14, _wbox_y + 164, _m_x + 14 + (486 * (_pmc_pct / 100.0)), _wbox_y + 172, false);

            // Contested Sector Status
            draw_set_color(make_color_rgb(255, 220, 120));
            draw_text(_m_x + 14, _wbox_y + 182, "FRONTLINE: " + _tc.contested_sector);
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
                    var _ramt = _nd.current_storage[$ _rkname];
                    _storage_str += string_upper(_rkname) + ": " + string(_ramt) + "kg  ";
                }
                if (_storage_str == "") _storage_str = "Storage Bin Empty";

                draw_set_color(c_white);
                draw_text(_nc_x + 16, _ny + 28, "Stored Ore: " + _storage_str);
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

    // =====================================================================
    // SUBTAB 1: INTERSTELLAR FACTIONS & LIAISONS (DOC 04)
    // =====================================================================
    else if (war_subtab == 1) {
        var _fx_pan = _pan_x + 24;
        var _fy_pan = _pan_y + 44;
        var _fw_pan = _pan_w - 48;
        var _fh_pan = _pan_h - 56;

        // Faction Selector Buttons (4 Factions)
        var _f_tabs = [
            { id: "faction_terran", label: "1. THE TERRAN COALITION", col: make_color_rgb(60, 130, 240) },
            { id: "faction_colony", label: "2. THE OUTER COLONIES", col: make_color_rgb(40, 210, 180) },
            { id: "faction_syndicate", label: "3. RIM-SYNDICATE CARTEL", col: make_color_rgb(240, 140, 40) },
            { id: "faction_zaibatsu", label: "4. APEX BIO-ZAIBATSU", col: make_color_rgb(180, 90, 240) }
        ];
        var _fb_w = (_fw_pan - 36) / 4;
        for (var fti = 0; fti < 4; fti++) {
            var _ft_dat = _f_tabs[fti];
            var _fbx = _fx_pan + fti * (_fb_w + 12);
            var _fb_act = (selected_faction_dossier == _ft_dat.id);
            var _fb_hov = (_mx >= _fbx && _mx <= _fbx + _fb_w && _my >= _fy_pan && _my <= _fy_pan + 32);
            if (_fb_hov && _click) selected_faction_dossier = _ft_dat.id;

            draw_set_color(_fb_act ? make_color_rgb(24, 48, 76) : (_fb_hov ? make_color_rgb(18, 32, 50) : make_color_rgb(12, 18, 26)));
            draw_rectangle(_fbx, _fy_pan, _fbx + _fb_w, _fy_pan + 32, false);
            draw_set_color(_fb_act ? _ft_dat.col : make_color_rgb(40, 60, 80));
            draw_rectangle(_fbx, _fy_pan, _fbx + _fb_w, _fy_pan + 32, true);
            draw_set_color(_fb_act ? c_white : make_color_rgb(170, 195, 220));
            draw_text(_fbx + 12, _fy_pan + 8, _ft_dat.label);
        }

        // Left Card: Faction Standing & Military Mech Representative
        var _d_y = _fy_pan + 44;
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
                _curr_title = obj_FactionManager.factions[$ _fid_curr].standing_title;
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

        // Standing Mobile Suit Artwork
        var _unit_spr = (selected_faction_dossier == "faction_terran") ? spr_mech_terran_ironclad : ((selected_faction_dossier == "faction_colony") ? spr_mech_colony_aether : ((selected_faction_dossier == "faction_syndicate") ? spr_mech_syndicate_hyena : spr_mech_zaibatsu_muramasa));
        if (sprite_exists(_unit_spr)) {
            draw_sprite_ext(_unit_spr, 0, _fx_pan + _col1_w / 2, _d_y + 390, 0.72, 0.72, 0, c_white, 0.95);
        }

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
            if (sprite_exists(spr_portrait_vance)) draw_sprite_ext(spr_portrait_vance, 0, _col2_x + 20, _l_y, 0.45, 0.45, 0, c_white, 1.0);
            draw_set_color(make_color_rgb(240, 210, 100));
            draw_text(_col2_x + 120, _l_y, "GENERAL DEBORAH VANCE // SUPREME LOGISTICS DIRECTOR");
            draw_set_color(c_white);
            draw_text_ext(_col2_x + 120, _l_y + 22, "'A mobile suit is not a weapon of glory, Commander. It is a four-million-credit piece of hydraulic machinery designed to outlast the infantryman inside it. Keep the assembly line moving.'", 18, _col2_w - 140);

            // Recruitable Ace 1: Marcus Cole
            var _a1_y = _l_y + 115;
            if (sprite_exists(spr_portrait_cole)) draw_sprite_ext(spr_portrait_cole, 0, _col2_x + 20, _a1_y, 0.45, 0.45, 0, c_white, 1.0);
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_col2_x + 120, _a1_y, "LT. MARCUS 'BREAKER' COLE [RECRUITABLE HEAVY ACE]");
            draw_set_color(c_white);
            draw_text(_col2_x + 120, _a1_y + 20, "Accuracy: 78% | Reflexes: 42% | Bravery: 95% | Trait: Heavy Ordnance (+20% Kinetic DMG)");
            draw_text_ext(_col2_x + 120, _a1_y + 38, "Trench veteran cashiered for refusing orders to shell a civilian hydroponics dome. Stoic fortress pilot.", 18, _col2_w - 280);

            var _hb1_x = _col2_x + _col2_w - 160;
            var _hb1_y = _a1_y + 15;
            var _h1_hov = (_mx >= _hb1_x && _mx <= _hb1_x + 140 && _my >= _hb1_y && _my <= _hb1_y + 36);
            if (_h1_hov && _click && instance_exists(obj_GameManager)) {
                if (obj_GameManager.spend_funds(45000)) {
                    array_push(obj_GameManager.facilities.roster_pilots, {
                        name: "Lt. Marcus Cole", callsign: "BREAKER", accuracy: 78, reflexes: 42, morale: 95, salary_daily: 250, is_deployed: false, status: "ACTIVE", recovery_days: 0, kills: 4, sorties: 6
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
            if (sprite_exists(spr_portrait_vance)) draw_sprite_ext(spr_portrait_vance, 0, _col2_x + 20, _a2_y, 0.45, 0.45, 0, c_white, 1.0);
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_col2_x + 120, _a2_y, "ENSIGN ELENA ROSTOVA [RECRUITABLE SNIPER]");
            draw_set_color(c_white);
            draw_text(_col2_x + 120, _a2_y + 20, "Accuracy: 92% | Reflexes: 55% | Bravery: 65% | Trait: Retinal Implants (+15% Critical Chance)");
            draw_text_ext(_col2_x + 120, _a2_y + 38, "Precision marksman who deserted after whistleblowing corporate sensor falsifications.", 18, _col2_w - 280);

            var _hb2_x = _col2_x + _col2_w - 160;
            var _hb2_y = _a2_y + 15;
            var _h2_hov = (_mx >= _hb2_x && _mx <= _hb2_x + 140 && _my >= _hb2_y && _my <= _hb2_y + 36);
            if (_h2_hov && _click && instance_exists(obj_GameManager)) {
                if (obj_GameManager.spend_funds(38000)) {
                    array_push(obj_GameManager.facilities.roster_pilots, {
                        name: "Ensign Elena Rostova", callsign: "DEAD-EYE", accuracy: 92, reflexes: 55, morale: 80, salary_daily: 220, is_deployed: false, status: "ACTIVE", recovery_days: 0, kills: 2, sorties: 3
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
            draw_text(_col2_x + 20, _by, "MAJOR STRATEGIC STRONGHOLDS (EARTH & SPACE // docs/11):");
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
            if (sprite_exists(spr_portrait_cassian)) draw_sprite_ext(spr_portrait_cassian, 0, _col2_x + 20, _l_y, 0.45, 0.45, 0, c_white, 1.0);
            draw_set_color(make_color_rgb(240, 210, 100));
            draw_text(_col2_x + 120, _l_y, "FLEET COMMANDER CASSIAN VANE // LIBERATION FLOTILLA");
            draw_set_color(c_white);
            draw_text_ext(_col2_x + 120, _l_y + 22, "'Earth treats our people as indentured ore-miners while breathing the oxygen our solar scrubbers produce. Every beam rifle we forge is an invoice for two centuries of colonial tribute.'", 18, _col2_w - 140);

            var _a1_y = _l_y + 115;
            if (sprite_exists(spr_portrait_sorren)) draw_sprite_ext(spr_portrait_sorren, 0, _col2_x + 20, _a1_y, 0.45, 0.45, 0, c_white, 1.0);
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
                        name: "Sorren Lin", callsign: "GHOST", accuracy: 85, reflexes: 92, morale: 85, salary_daily: 280, is_deployed: false, status: "ACTIVE", recovery_days: 0, kills: 5, sorties: 7
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
            if (sprite_exists(spr_portrait_sorren)) draw_sprite_ext(spr_portrait_sorren, 0, _col2_x + 20, _a2_y, 0.45, 0.45, 0, c_white, 1.0);
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
                        name: "Kira Dahl", callsign: "SPECTER", accuracy: 70, reflexes: 80, morale: 90, salary_daily: 190, is_deployed: false, status: "ACTIVE", recovery_days: 0, kills: 1, sorties: 2
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
            draw_text(_col2_x + 20, _by, "MAJOR STRATEGIC STRONGHOLDS (EARTH & SPACE // docs/11):");
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
            if (sprite_exists(spr_portrait_cruz)) draw_sprite_ext(spr_portrait_cruz, 0, _col2_x + 20, _l_y, 0.45, 0.45, 0, c_white, 1.0);
            draw_set_color(make_color_rgb(240, 210, 100));
            draw_text(_col2_x + 120, _l_y, "MADAME ROSALIND CRUZ // MATRIARCH OF SCRAP DEPOT 9");
            draw_set_color(c_white);
            draw_text_ext(_col2_x + 120, _l_y + 22, "'Earth and the Colonies have been burning each other's fleets for ten years, darling. And every time a million-dollar cockpit pops in vacuum, my boys are there with blowtorches. War is the only reliable commodity.'", 18, _col2_w - 140);

            var _a1_y = _l_y + 115;
            if (sprite_exists(spr_portrait_nadia)) draw_sprite_ext(spr_portrait_nadia, 0, _col2_x + 20, _a1_y, 0.45, 0.45, 0, c_white, 1.0);
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
                        name: "Nadia Ortiz", callsign: "SPARK", accuracy: 72, reflexes: 65, morale: 95, salary_daily: 170, is_deployed: false, status: "ACTIVE", recovery_days: 0, kills: 2, sorties: 4
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
            if (sprite_exists(spr_portrait_cole)) draw_sprite_ext(spr_portrait_cole, 0, _col2_x + 20, _a2_y, 0.45, 0.45, 0, c_white, 1.0);
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
                        name: "Jax Vance", callsign: "JACKAL", accuracy: 80, reflexes: 78, morale: 65, salary_daily: 230, is_deployed: false, status: "ACTIVE", recovery_days: 0, kills: 3, sorties: 5
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
            draw_text(_col2_x + 20, _by, "MAJOR STRATEGIC STRONGHOLDS (EARTH & SPACE // docs/11):");
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
            if (sprite_exists(spr_portrait_renzo)) draw_sprite_ext(spr_portrait_renzo, 0, _col2_x + 20, _l_y, 0.45, 0.45, 0, c_white, 1.0);
            draw_set_color(make_color_rgb(240, 210, 100));
            draw_text(_col2_x + 120, _l_y, "DIRECTOR RENZO TAKAHASHI // VP SPECIAL WEAPONS");
            draw_set_color(c_white);
            draw_text_ext(_col2_x + 120, _l_y + 22, "'Human reaction time is limited to two hundred milliseconds. Our neural-interface bypasses ocular processing entirely, cutting weapon discharge latency to twelve. Progress requires shedding biological sentiment.'", 18, _col2_w - 140);

            var _a1_y = _l_y + 115;
            if (sprite_exists(spr_portrait_null07)) draw_sprite_ext(spr_portrait_null07, 0, _col2_x + 20, _a1_y, 0.45, 0.45, 0, c_white, 1.0);
            draw_set_color(make_color_rgb(180, 90, 240));
            draw_text(_col2_x + 120, _a1_y, "NULL-07 (REN) [RECRUITABLE NEURAL ACE]");
            draw_set_color(c_white);
            draw_text(_col2_x + 120, _a1_y + 20, "Accuracy: 96% | Reflexes: 88% | Bravery: 99% | Trait: Neural Link (+2 Actions in 1st Turn)");
            draw_text_ext(_col2_x + 120, _a1_y + 38, "Pale escaped test subject with spinal data-ports; reacts to projectile trajectories before muzzle flashes.", 18, _col2_w - 280);

            var _hb1_x = _col2_x + _col2_w - 160;
            var _hb1_y = _a1_y + 15;
            var _h1_hov = (_mx >= _hb1_x && _mx <= _hb1_x + 140 && _my >= _hb1_y && _my <= _hb1_y + 36);
            if (_h1_hov && _click && instance_exists(obj_GameManager)) {
                if (obj_GameManager.spend_funds(65000)) {
                    array_push(obj_GameManager.facilities.roster_pilots, {
                        name: "Null-07 (Ren)", callsign: "NULL", accuracy: 96, reflexes: 88, morale: 50, salary_daily: 320, is_deployed: false, status: "ACTIVE", recovery_days: 0, kills: 6, sorties: 8
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
            if (sprite_exists(spr_portrait_nadia)) draw_sprite_ext(spr_portrait_nadia, 0, _col2_x + 20, _a2_y, 0.45, 0.45, 0, c_white, 1.0);
            draw_set_color(make_color_rgb(180, 90, 240));
            draw_text(_col2_x + 120, _a2_y, "MAYA 'KESTREL' ZHAO [RECRUITABLE DRONE TACTICIAN]");
            draw_set_color(c_white);
            draw_text(_col2_x + 120, _a2_y + 20, "Accuracy: 84% | Reflexes: 75% | Bravery: 80% | Trait: Drone Swarm (+1 Support Drone)");
            draw_text_ext(_col2_x + 120, _a2_y + 38, "Former corporate security flight commander who bought out her indenture debt with stolen securities.", 18, _col2_w - 280);

            var _hb2_x = _col2_x + _col2_w - 160;
            var _hb2_y = _a2_y + 15;
            var _h2_hov = (_mx >= _hb2_x && _mx <= _hb2_x + 140 && _my >= _hb2_y && _my <= _hb2_y + 36);
            if (_h2_hov && _click && instance_exists(obj_GameManager)) {
                if (obj_GameManager.spend_funds(46000)) {
                    array_push(obj_GameManager.facilities.roster_pilots, {
                        name: "Maya Zhao", callsign: "KESTREL", accuracy: 84, reflexes: 75, morale: 85, salary_daily: 240, is_deployed: false, status: "ACTIVE", recovery_days: 0, kills: 3, sorties: 5
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
            draw_text(_col2_x + 20, _by, "MAJOR STRATEGIC STRONGHOLDS (EARTH & SPACE // docs/11):");
            draw_set_color(make_color_rgb(220, 185, 255));
            draw_text(_col2_x + 20, _by + 18, "• [SPACE] Citadel Susanoo (Earth-Sun L2) - Cloaked obsidian polyhedron with vacuum automated robotic foundries");
            draw_text(_col2_x + 20, _by + 34, "• [SPACE] Lab-Complex Zero 'The Nursery' (Kuiper Belt) - Classified human neural-sync test station (Null-07 origin)");
            draw_text(_col2_x + 20, _by + 50, "• [EARTH] Neo-Kobe Megaplex & Sky-Spire (Osaka Bay) - Chrome spires on sea caissons housing police mech lines");
            draw_text(_col2_x + 20, _by + 66, "• [EARTH] Atacama Quantum Data Vault (Chile) - Subterranean computing vault training predictive combat AI");
        }
    }

    // =====================================================================
    // SUBTAB 2: DECADE MECHA LINEAGE & TIMELINE (Y205-Y215)
    // =====================================================================
    else if (war_subtab == 2) {
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
    // SUBTAB 3: PMC EXPEDITIONARY STRIKE & FACTION OVERTHROW (docs/12)
    // =====================================================================
    else if (war_subtab == 3) {
        var _ox = _pan_x + 30;
        var _oy = _pan_y + 44;

        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(_ox, _oy, "== PMC EXPEDITIONARY STRIKE & FACTION OVERTHROW COMMAND (docs/12) ==");
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
                var _tinfo = _fm.factions[$ _tfid];
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

            var _cur_target = _fm.factions[$ selected_strike_faction];
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
                draw_set_color(c_white);
                draw_text(_col2_x + 30, _col1_y + 74, "Unit: " + _assigned_mech.name + " (" + _assigned_mech.class + ")");
                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text(_col2_x + 30, _col1_y + 94, "Armor Rating: " + string(_assigned_mech.armor_rating) + " | Reactor Output: " + string(_assigned_mech.power_output) + " MW");
                var _m_status_col = (_assigned_mech.status == "READY") ? c_lime : c_red;
                draw_set_color(_m_status_col);
                draw_text(_col2_x + 30, _col1_y + 114, "Operational Status: " + _assigned_mech.status);
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
                draw_set_color(c_white);
                draw_text(_col2_x + 30, _col1_y + 188, "Pilot: " + _assigned_pilot.name + " (" + _assigned_pilot.callsign + ")");
                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text(_col2_x + 30, _col1_y + 208, "Combat Rating: " + string(_assigned_pilot.combat_stat) + " | Tactics Rating: " + string(_assigned_pilot.tactics_stat));
                var _p_status_col = (_assigned_pilot.status == "ACTIVE") ? c_lime : c_red;
                draw_set_color(_p_status_col);
                draw_text(_col2_x + 30, _col1_y + 228, "Deployment Status: " + _assigned_pilot.status);
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

            var _strike_est = (!is_undefined(_assigned_mech) && !is_undefined(_assigned_pilot)) ? (_assigned_mech.armor_rating + _assigned_mech.power_output + (_assigned_pilot.combat_stat * 12)) : 0;
            var _def_est = _cur_target.military_strength_score * 1.8;

            draw_set_color(c_white);
            draw_text(_col2_x + 30, _calc_y + 24, "Vanguard Strike Power: " + string(_strike_est) + " pts   vs   Enemy Garrison Defense: " + string(_def_est) + " pts");
            draw_set_color(make_color_rgb(100, 255, 140));
            draw_text(_col2_x + 30, _calc_y + 44, "Projected Conquest Yield: +3% to +6% Sovereign Territory | +180,000 to +380,000 Cr Salvage");

            // Big Launch Sortie Button
            var _launch_btn_y = _calc_y + 75;
            var _launch_btn_w = _col2_w - 36;
            var _launch_btn_h = 52;
            var _can_launch = (!_target_overthrown && !is_undefined(_assigned_mech) && _assigned_mech.status == "READY" && !is_undefined(_assigned_pilot) && _assigned_pilot.status == "ACTIVE");
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


// =========================================================================
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

            show_toast("COMMAND DIRECTIVE LOGGED: " + _choice.label, c_lime);
            obj_GameManager.active_event_popup = undefined;
            break;
        }

        draw_set_color(_chov ? make_color_rgb(30, 60, 90) : make_color_rgb(16, 26, 38));
        draw_rectangle(_ex + 24, _c_btn_y, _ex + _ew - 24, _c_btn_y + 56, false);
        draw_set_color(make_color_rgb(80, 160, 240));
        draw_rectangle(_ex + 24, _c_btn_y, _ex + _ew - 24, _c_btn_y + 56, true);

        draw_set_color(make_color_rgb(240, 210, 100));
        draw_text(_ex + 36, _c_btn_y + 8, _choice.label);
        draw_set_color(make_color_rgb(180, 205, 230));
        draw_text(_ex + 36, _c_btn_y + 30, _choice.desc);
    }
}

// =========================================================================
// 7. NODE PIRATE RAID EMERGENCY MODAL (docs/06_resource_operations.md)
// =========================================================================
if (instance_exists(obj_GameManager) && !is_undefined(obj_GameManager.pending_raid)) {
    var _rd = obj_GameManager.pending_raid;
    var _rw = 660;
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
                draw_text(_mx0 + 36, _ev_y + ei * 24, ">> " + _events[ei]);
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
    draw_set_alpha(0.90);
    draw_set_color(c_black);
    draw_rectangle(0, 0, _gw, _gh, false);
    draw_set_alpha(1.0);

    var _tw = 920;
    var _th = 580;
    var _tx0 = (_gw - _tw) / 2;
    var _ty0 = (_gh - _th) / 2;

    draw_set_color(make_color_rgb(10, 16, 24));
    draw_rectangle(_tx0, _ty0, _tx0 + _tw, _ty0 + _th, false);
    draw_set_color(make_color_rgb(255, 180, 60));
    draw_rectangle(_tx0, _ty0, _tx0 + _tw, _ty0 + _th, true);

    // Modal Close Button
    var _cl_w = 140;
    var _cl_hov = (_mx >= _tx0 + _tw - _cl_w - 20 && _mx <= _tx0 + _tw - 20 && _my >= _ty0 + 16 && _my <= _ty0 + 44);
    if ((_cl_hov && _click) || keyboard_check_pressed(vk_escape)) active_tutorial_modal = "";
    draw_set_color(_cl_hov ? make_color_rgb(120, 40, 40) : make_color_rgb(60, 20, 20));
    draw_rectangle(_tx0 + _tw - _cl_w - 20, _ty0 + 16, _tx0 + _tw - 20, _ty0 + 44, false);
    draw_set_color(c_red);
    draw_rectangle(_tx0 + _tw - _cl_w - 20, _ty0 + 16, _tx0 + _tw - 20, _ty0 + 44, true);
    draw_set_color(c_white);
    draw_text(_tx0 + _tw - _cl_w - 8, _ty0 + 22, "[X CLOSE (ESC)]");

    // Modal Navigation Sub-Tabs
    var _mod_tabs = [
        { id: "PMC_MANUAL", label: "[PMC MANUAL]" },
        { id: "CRUCIBLE", label: "[CRUCIBLE R&D]" },
        { id: "REACTOR", label: "[REACTOR TUNING]" },
        { id: "HYDRAULIC", label: "[HYDRAULIC BENCH]" },
        { id: "THRUSTER", label: "[PLASMA THRUST]" }
    ];
    var _mtw = 150;
    for (var mti = 0; mti < 5; mti++) {
        var _mt_dat = _mod_tabs[mti];
        var _mt_x = _tx0 + 24 + mti * (_mtw + 10);
        var _mt_y = _ty0 + 16;
        var _is_mact = (active_tutorial_modal == _mt_dat.id);
        var _mthov = (_mx >= _mt_x && _mx <= _mt_x + _mtw && _my >= _mt_y && _my <= _mt_y + 28);
        if (_mthov && _click) active_tutorial_modal = _mt_dat.id;

        draw_set_color(_is_mact ? make_color_rgb(50, 100, 160) : (_mthov ? make_color_rgb(30, 60, 90) : make_color_rgb(16, 26, 38)));
        draw_rectangle(_mt_x, _mt_y, _mt_x + _mtw, _mt_y + 28, false);
        draw_set_color(_is_mact ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 75, 110));
        draw_rectangle(_mt_x, _mt_y, _mt_x + _mtw, _mt_y + 28, true);
        draw_set_color(c_white);
        draw_text(_mt_x + 10, _mt_y + 6, _mt_dat.label);
    }

    // Modal Content Body
    var _body_x = _tx0 + 24;
    var _body_y = _ty0 + 58;
    var _body_w = _tw - 48;
    var _body_h = _th - 80;

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
        draw_text(_body_x + 20, _body_y + 16, "== OPERATING MANUAL: ALLOY SYNTHESIS CRUCIBLE (DOC 02) ==");

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
        draw_text(_body_x + 20, _body_y + 16, "== OPERATING MANUAL: TOKAMAK HARMONIC CONDUIT TUNER (DOC 03) ==");

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
        draw_text(_body_x + 40, _ty + _lh * 9.5, "3. TESTING & REWARDS:");
        draw_text(_body_x + 60, _ty + _lh * 10.5, "- Take your time adjusting sliders and +/- tactile buttons; the wave does not drift.");
        draw_text(_body_x + 60, _ty + _lh * 11.5, "- Once Harmonic Alignment reaches >= 90.0%, click [>> TEST CONDUIT HARMONIC PULSE <<].");
        draw_text(_body_x + 60, _ty + _lh * 12.5, "- Award: Masterwork Hyperion Tokamak Core (+15% Net Power Surplus) added to blueprints!");
    }
    else if (active_tutorial_modal == "HYDRAULIC") {
        draw_set_color(make_color_rgb(255, 200, 80));
        draw_text(_body_x + 20, _body_y + 16, "== OPERATING MANUAL: HYDRAULIC STRESS BENCH (DOC 03) ==");

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

        draw_text(_body_x + 40, _ty + _lh * 9.5, "3. SPOT-WELDING & REWARDS:");
        draw_text(_body_x + 60, _ty + _lh * 10.5, "- When a joint's stress is inside 25%-45%, click [SPOT-WELD JOINT LOCK] to lock it.");
        draw_text(_body_x + 60, _ty + _lh * 11.5, "- Once locked, a joint is immune to subsequent neighbor backpressure shifts.");
        draw_text(_body_x + 60, _ty + _lh * 12.5, "- Award: Lock all 4 joints to forge Masterwork Colossus Hydraulic Walkers (+20% Recoil & +1 AP)!");
    }
    else if (active_tutorial_modal == "THRUSTER") {
        draw_set_color(make_color_rgb(255, 200, 80));
        draw_text(_body_x + 20, _body_y + 16, "== OPERATING MANUAL: DUAL-VECTOR PLASMA CALIBRATION (DOC 03) ==");

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
        draw_text(_body_x + 40, _ty + _lh * 10.5, "3. ADVANCING & REWARDS:");
        draw_text(_body_x + 60, _ty + _lh * 11.5, "- When resonance is >= 80%, click [>> COMMIT STAGE CALIBRATION PULSE <<] to advance.");
        draw_text(_body_x + 60, _ty + _lh * 12.5, "- Clearing all 4 stages awards the Masterwork Dual-Vector Vernier Backpack (+25% Evasion)!");
    }
}


// =========================================================================
// 8. SID MEIER'S PIRATES-STYLE RETIREMENT & CAREER LEGACY MODAL (docs/12)
// =========================================================================
if (showing_retire_modal || (instance_exists(obj_GameManager) && !is_undefined(obj_GameManager.career_summary))) {
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
        }
        draw_set_color(_cls_hov ? make_color_rgb(45, 60, 85) : make_color_rgb(22, 32, 48));
        draw_rectangle(_btn_close_x, _btn_resume_y, _btn_close_x + _btn_close_w, _btn_resume_y + _btn_close_h, false);
        draw_set_color(make_color_rgb(100, 180, 255));
        draw_rectangle(_btn_close_x, _btn_resume_y, _btn_close_x + _btn_close_w, _btn_resume_y + _btn_close_h, true);
        draw_set_color(c_white);
        draw_text(_btn_close_x + 90, _btn_resume_y + 14, "[DISMISS RETIREMENT OVERLAY (ESC)]");
    }
}
