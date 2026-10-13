/// @description obj_BattleManager Draw GUI Event
// Renders Grand-Scale Tactical HUD, Platoon Timeline, Front Mission Limb Diagnostics & Command Controls
// Strictly implements docs/17_grand_scale_isometric_combat_system.md & docs/05_tactical_combat.md

var _gw = display_get_gui_width();
var _gh = display_get_gui_height();
var _mx = device_mouse_x_to_gui(0);
var _my = device_mouse_y_to_gui(0);
var _click = mouse_check_button_pressed(mb_left);

var _cur_u = (selected_unit_idx >= 0 && selected_unit_idx < array_length(units)) ? units[selected_unit_idx] : undefined;

// =========================================================================
// 1. TOP MISSION & PLATOON TIMELINE HUD BAR (y: 0 to 86)
// =========================================================================
draw_set_color(make_color_rgb(12, 17, 24));
draw_rectangle(0, 0, _gw, 86, false);
draw_set_color(make_color_rgb(32, 54, 82));
draw_rectangle(0, 84, _gw, 86, false);

// Sector Title & Subtitle
draw_set_color(make_color_rgb(100, 210, 255));
draw_text(16, 8, "TACTICAL ISOMETRIC ENGAGEMENT // SECTOR 4 MINING OUTPOST");
draw_set_color(make_color_rgb(150, 180, 210));
draw_text(16, 26, "OBJECTIVE: Neutralize Syndicate Battlegroup (13 Units) | Allied Forces: 8 Units");

// Current Phase Badge
var _phase_str = "[PLAYER PHASE]";
var _phase_col = make_color_rgb(80, 240, 120);
if (state == COMBAT_STATE.AI_PHASE) {
    _phase_str = "[HOSTILE PHASE // ENEMY ENGAGING]";
    _phase_col = make_color_rgb(255, 80, 80);
} else if (state == COMBAT_STATE.MOVE_MODE) {
    _phase_str = "[MANEUVER MODE // SELECT DESTINATION]";
    _phase_col = make_color_rgb(100, 220, 255);
} else if (state == COMBAT_STATE.TARGET_MODE) {
    _phase_str = "[TARGETING WEAPON // SELECT TARGET]";
    _phase_col = make_color_rgb(255, 200, 80);
} else if (state == COMBAT_STATE.AUTO_SIM) {
    _phase_str = "[AUTO-SIMULATION ACTIVE]";
    _phase_col = make_color_rgb(210, 140, 255);
}
draw_set_color(_phase_col);
draw_text(16, 46, "STATUS: " + _phase_str + " | TURN: " + string(turn_number));

// Camera Navigation Hints
draw_set_color(make_color_rgb(140, 170, 200));
draw_text(16, 64, "[WASD/Drag] Pan | [Wheel] Zoom: " + string(round(zoom * 100)) + "% | [R] Reset | [TAB] Cycle | [F] Facing");

// Platoon Roster Mini Selector Strip (x: 580 to 1120)
var _strip_x = 580;
var _btn_w = 64;
var _btn_h = 36;
for (var u = 0; u < 8; u++) {
    if (u >= array_length(units)) break;
    var _allied_u = units[u];
    var _bx = _strip_x + u * (_btn_w + 4);
    var _by = 12;

    var _hov = (_mx >= _bx && _mx <= _bx + _btn_w && _my >= _by && _my <= _by + _btn_h);
    if (_hov && _click && state == COMBAT_STATE.PLAYER_PHASE && !_allied_u.is_destroyed) {
        select_unit(u);
    }

    var _is_sel = (selected_unit_idx == u);
    var _b_bg = _allied_u.is_destroyed ? make_color_rgb(25, 25, 25) : (_is_sel ? make_color_rgb(30, 80, 120) : (_hov ? make_color_rgb(24, 48, 70) : make_color_rgb(16, 28, 42)));
    draw_set_color(_b_bg);
    draw_rectangle(_bx, _by, _bx + _btn_w, _by + _btn_h, false);

    draw_set_color(_is_sel ? make_color_rgb(80, 220, 255) : make_color_rgb(45, 75, 110));
    draw_rectangle(_bx, _by, _bx + _btn_w, _by + _btn_h, true);

    draw_set_color(_allied_u.is_destroyed ? c_gray : c_white);
    draw_text(_bx + 6, _by + 4, "A-0" + string(u + 1));

    // Mini AP Pips
    if (!_allied_u.is_destroyed) {
        for (var p = 0; p < _allied_u.max_ap; p++) {
            var _px = _bx + 6 + p * 8;
            var _py = _by + 22;
            draw_set_color((p < _allied_u.current_ap) ? c_lime : make_color_rgb(30, 50, 40));
            draw_rectangle(_px, _py, _px + 6, _py + 8, false);
        }
    } else {
        draw_set_color(c_red);
        draw_text(_bx + 6, _by + 18, "KIA");
    }
}

// Retreat / Abort Button (Top Right)
var _ab_x = 1180;
var _ab_y = 12;
var _ab_w = 170;
var _ab_h = 36;
var _ab_hov = (_mx >= _ab_x && _mx <= _ab_x + _ab_w && _my >= _ab_y && _my <= _ab_y + _ab_h);
if (_ab_hov && _click) {
    if (room_exists(rm_hq_terminal)) room_goto(rm_hq_terminal);
}
draw_set_color(_ab_hov ? make_color_rgb(70, 30, 20) : make_color_rgb(32, 16, 12));
draw_rectangle(_ab_x, _ab_y, _ab_x + _ab_w, _ab_y + _ab_h, false);
draw_set_color(make_color_rgb(220, 90, 50));
draw_rectangle(_ab_x, _ab_y, _ab_x + _ab_w, _ab_y + _ab_h, true);
draw_set_color(c_white);
draw_text(_ab_x + 12, _ab_y + 10, "[ESC: RETREAT HQ]");

// =========================================================================
// 2. ACTIVE UNIT STATUS, AP & HEAT BAR (y: 92 to 135)
// =========================================================================
if (_cur_u != undefined) {
    draw_set_color(make_color_rgb(10, 16, 24));
    draw_rectangle(16, 92, 915, 135, false);
    draw_set_color(make_color_rgb(28, 48, 72));
    draw_rectangle(16, 92, 915, 135, true);

    // Callsign & Pilot
    draw_set_color(make_color_rgb(100, 220, 255));
    draw_text(26, 96, "SELECTED: " + _cur_u.callsign);
    draw_set_color(make_color_rgb(160, 190, 220));
    draw_text(26, 114, "PILOT: " + _cur_u.pilot_name + " | TYPE: " + string_upper(_cur_u.mech_type) + " | FACING: " + string(_cur_u.facing));

    // Action Points (AP) Battery Pips
    var _ap_x = 380;
    var _ap_y = 96;
    draw_set_color(c_white);
    draw_text(_ap_x, _ap_y, "AP: " + string(_cur_u.current_ap) + " / " + string(_cur_u.max_ap));
    for (var p = 0; p < _cur_u.max_ap; p++) {
        var _px = _ap_x + p * 24;
        var _py = _ap_y + 18;
        var _has_ap = (p < _cur_u.current_ap);
        draw_set_color(_has_ap ? make_color_rgb(50, 220, 100) : make_color_rgb(30, 45, 35));
        draw_rectangle(_px, _py, _px + 18, _py + 16, false);
        draw_set_color(make_color_rgb(80, 255, 140));
        draw_rectangle(_px, _py, _px + 18, _py + 16, true);
    }

    // Chassis Heat Gauge
    var _heat_x = 640;
    var _heat_y = 96;
    var _h_norm = clamp(_cur_u.current_heat / _cur_u.max_heat, 0, 1);
    var _h_col = (_h_norm > 0.8) ? c_red : ((_h_norm > 0.5) ? c_orange : make_color_rgb(100, 200, 255));
    draw_set_color(c_white);
    draw_text(_heat_x, _heat_y, "HEAT: " + string(floor(_cur_u.current_heat)) + "% / 100%");
    draw_set_color(make_color_rgb(18, 28, 38));
    draw_rectangle(_heat_x, _heat_y + 18, _heat_x + 250, _heat_y + 32, false);
    draw_set_color(_h_col);
    draw_rectangle(_heat_x, _heat_y + 18, _heat_x + (250 * _h_norm), _heat_y + 32, false);
    draw_set_color(make_color_rgb(40, 70, 100));
    draw_rectangle(_heat_x, _heat_y + 18, _heat_x + 250, _heat_y + 32, true);
}

// =========================================================================
// 3. FRONT MISSION TARGET DUEL & DIAGNOSTICS (Right Panel: x 930 to 1350)
// =========================================================================
var _diag_x = 930;
var _diag_y = 92;
var _diag_w = _gw - _diag_x - 16;
var _diag_h = 470;

draw_set_color(make_color_rgb(10, 16, 24));
draw_rectangle(_diag_x, _diag_y, _diag_x + _diag_w, _diag_y + _diag_h, false);
draw_set_color(make_color_rgb(38, 64, 96));
draw_rectangle(_diag_x, _diag_y, _diag_x + _diag_w, _diag_y + _diag_h, true);

// Check if viewing targeted enemy vs selected allied unit
var _view_u = (target_unit_idx >= 0 && target_unit_idx < array_length(units) && !units[target_unit_idx].is_destroyed) ? units[target_unit_idx] : _cur_u;

if (_view_u != undefined) {
    var _is_target = (_view_u.team == "HOSTILE");
    draw_set_color(_is_target ? make_color_rgb(255, 120, 120) : make_color_rgb(100, 220, 255));
    draw_text(_diag_x + 16, _diag_y + 12, _is_target ? "== TARGET DIAGNOSTICS: HOSTILE ==" : "== UNIT STATUS SCHEMATIC: ALLIED ==");

    draw_set_color(c_white);
    draw_text(_diag_x + 16, _diag_y + 32, _view_u.callsign);
    draw_set_color(make_color_rgb(160, 190, 220));
    draw_text(_diag_x + 16, _diag_y + 50, "PILOT: " + _view_u.pilot_name + " | ACC: " + string(_view_u.accuracy) + "% | EVA: " + string(_view_u.evasion) + "%");

    // Component Breakdown Function
    var _draw_comp_bar = function(_lbl, _cur, _max, _armor, _intact, _bx, _by) {
        var _col = _intact ? ((_cur / _max > 0.4) ? c_lime : c_yellow) : c_red;
        draw_set_color(_intact ? c_white : c_gray);
        draw_text(_bx, _by, _lbl);
        draw_set_color(_col);
        draw_text(_bx + 140, _by, _intact ? (string(_cur) + " / " + string(_max) + " HP") : "[SEVERED]");

        draw_set_color(make_color_rgb(20, 28, 38));
        draw_rectangle(_bx + 235, _by + 2, _bx + 355, _by + 14, false);
        if (_intact) {
            draw_set_color(_col);
            draw_rectangle(_bx + 235, _by + 2, _bx + 235 + (120 * clamp(_cur / _max, 0, 1)), _by + 14, false);
        }
    };

    var _cy_start = _diag_y + 75;
    var _comps = _view_u.components;
    _draw_comp_bar("TORSO CORE", _comps.torso.cur, _comps.torso.max, _comps.torso.armor, _comps.torso.intact, _diag_x + 16, _cy_start);
    _draw_comp_bar("HEAD SENSORS", _comps.head.cur, _comps.head.max, _comps.head.armor, _comps.head.intact, _diag_x + 16, _cy_start + 24);
    _draw_comp_bar("LEFT ARM", _comps.arm_left.cur, _comps.arm_left.max, _comps.arm_left.armor, _comps.arm_left.intact, _diag_x + 16, _cy_start + 48);
    _draw_comp_bar("RIGHT ARM", _comps.arm_right.cur, _comps.arm_right.max, _comps.arm_right.armor, _comps.arm_right.intact, _diag_x + 16, _cy_start + 72);
    _draw_comp_bar("HYDRAULIC LEGS", _comps.legs.cur, _comps.legs.max, _comps.legs.armor, _comps.legs.intact, _diag_x + 16, _cy_start + 96);
    _draw_comp_bar("VERNIER PACK", _comps.backpack.cur, _comps.backpack.max, _comps.backpack.armor, _comps.backpack.intact, _diag_x + 16, _cy_start + 120);

    // Selected Weapon Hit Calculation Breakdown
    if (_cur_u != undefined && selected_weapon < array_length(_cur_u.weapons)) {
        var _calc_y = _cy_start + 155;
        var _sel_w = _cur_u.weapons[selected_weapon];

        draw_set_color(make_color_rgb(240, 210, 100));
        draw_text(_diag_x + 16, _calc_y, "ACTIVE WEAPON: " + _sel_w.name);
        draw_set_color(make_color_rgb(180, 205, 230));
        draw_text(_diag_x + 16, _calc_y + 20, "* Range: " + string(_sel_w.range_min) + "-" + string(_sel_w.range_max) + " Cells | Projectile: " + _sel_w.proj_type);
        draw_text(_diag_x + 16, _calc_y + 38, "* AP Cost: " + string(_sel_w.ap_cost) + " AP | Thermal Gen: +" + string(_sel_w.heat_cost) + "% Heat");

        if (_is_target) {
            var _dist_to_t = calculate_distance(_cur_u.grid_c, _cur_u.grid_r, _view_u.grid_c, _view_u.grid_r);
            var _hit_pct = calculate_hit_chance(_cur_u, _view_u, _dist_to_t);

            draw_set_color(make_color_rgb(100, 255, 140));
            draw_text(_diag_x + 16, _calc_y + 64, "CALCULATED HIT PROBABILITY: " + string(_hit_pct) + "% (Dist: " + string(_dist_to_t) + ")");
            draw_set_color(make_color_rgb(255, 140, 80));
            draw_text(_diag_x + 16, _calc_y + 84, "ESTIMATED DIRECT IMPACT: " + string(_sel_w.damage) + " DAMAGE");
        }
    }
}

// =========================================================================
// 4. COMMAND ACTION BAR (Bottom Left: x 16 to 915, y: 575 to 755)
// =========================================================================
var _act_x = 16;
var _act_y = 575;
var _act_w = 900;
var _act_h = _gh - _act_y - 12;

draw_set_color(make_color_rgb(10, 16, 24));
draw_rectangle(_act_x, _act_y, _act_x + _act_w, _act_y + _act_h, false);
draw_set_color(make_color_rgb(32, 54, 82));
draw_rectangle(_act_x, _act_y, _act_x + _act_w, _act_y + _act_h, true);

// Action Button Definitions
var _btn_defs = [
    { label: "[M] MOVE (1 AP/CELL)", mode: COMBAT_STATE.MOVE_MODE },
    { label: "[1] WPN 1 (CANNON / BEAM)", mode: COMBAT_STATE.TARGET_MODE, wpn: 0 },
    { label: "[2] WPN 2 (VULCAN / FLAK)", mode: COMBAT_STATE.TARGET_MODE, wpn: 1 },
    { label: "[3] WPN 3 (MISSILE / PLASMA)", mode: COMBAT_STATE.TARGET_MODE, wpn: 2 },
    { label: "[4] WPN 4 (MELEE STRIKE)", mode: COMBAT_STATE.TARGET_MODE, wpn: 3 },
    { label: "[B] BRACE & VENT (2 AP)", brace: true },
    { label: "[TAB] NEXT ALLIED UNIT", next_unit: true },
    { label: "[F] ROTATE PERSPECTIVE", cycle_face: true },
    { label: "[A] AUTO-COMBAT", auto_sim: true },
    { label: "[SPACE] END TURN", end_turn: true }
];

var _bx_start = _act_x + 12;
var _by_start = _act_y + 10;
var _b_w = 168;
var _b_h = 32;

for (var b = 0; b < array_length(_btn_defs); b++) {
    var _bd = _btn_defs[b];
    var _col_idx = b % 5;
    var _row_idx = floor(b / 5);
    var _cur_bx = _bx_start + _col_idx * (_b_w + 8);
    var _cur_by = _by_start + _row_idx * (_b_h + 8);

    var _b_hov = (_mx >= _cur_bx && _mx <= _cur_bx + _b_w && _my >= _cur_by && _my <= _cur_by + _b_h);

    if (_b_hov && _click && state == COMBAT_STATE.PLAYER_PHASE) {
        if (variable_struct_exists(_bd, "mode")) {
            if (variable_struct_exists(_bd, "wpn")) selected_weapon = _bd.wpn;
            if (_bd.mode == COMBAT_STATE.MOVE_MODE) recalculate_moves();
            state = _bd.mode;
        } else if (variable_struct_exists(_bd, "brace")) {
            if (_cur_u != undefined && _cur_u.current_ap >= 2) {
                _cur_u.current_ap -= 2;
                _cur_u.braced = true;
                _cur_u.current_heat = max(0, _cur_u.current_heat - 25);
                add_log("[TACTICAL DEFENSE] " + _cur_u.callsign + " braced! +35% Evasion, -25% Heat vented.");
            }
        } else if (variable_struct_exists(_bd, "next_unit")) {
            cycle_allied_unit();
        } else if (variable_struct_exists(_bd, "cycle_face")) {
            if (_cur_u != undefined) cycle_unit_facing(_cur_u);
        } else if (variable_struct_exists(_bd, "auto_sim")) {
            auto_combat_enabled = !auto_combat_enabled;
            if (auto_combat_enabled) state = COMBAT_STATE.AUTO_SIM;
            add_log("[AUTO-COMBAT] " + (auto_combat_enabled ? "Autonomous Simulation Engaged!" : "Disengaged."));
        } else if (variable_struct_exists(_bd, "end_turn")) {
            add_log("[TURN END] Initiative passed to hostile battlegroup.");
            state = COMBAT_STATE.AI_PHASE;
            ai_action_timer = 0;
            ai_unit_index = 0;
        }
    }

    draw_set_color(_b_hov ? make_color_rgb(32, 64, 96) : make_color_rgb(16, 26, 38));
    draw_rectangle(_cur_bx, _cur_by, _cur_bx + _b_w, _cur_by + _b_h, false);
    draw_set_color(make_color_rgb(50, 95, 145));
    draw_rectangle(_cur_bx, _cur_by, _cur_bx + _b_w, _cur_by + _b_h, true);

    draw_set_color(c_white);
    draw_text_transformed(_cur_bx + 6, _cur_by + 8, _bd.label, 0.78, 0.78, 0);
}

// =========================================================================
// 5. LIVE COMBAT TERMINAL FEED (Bottom Right: x 930 to 1350, y: 575 to 755)
// =========================================================================
var _log_x = _diag_x;
var _log_y = _act_y;
var _log_w = _diag_w;
var _log_h = _act_h;

draw_set_color(make_color_rgb(8, 12, 18));
draw_rectangle(_log_x, _log_y, _log_x + _log_w, _log_y + _log_h, false);
draw_set_color(make_color_rgb(30, 50, 75));
draw_rectangle(_log_x, _log_y, _log_x + _log_w, _log_y + _log_h, true);

draw_set_color(make_color_rgb(100, 200, 255));
draw_text(_log_x + 12, _log_y + 8, ">> LIVE TACTICAL COMBAT LOG <<");

for (var l = 0; l < array_length(combat_log); l++) {
    var _line = combat_log[l];
    var _lcol = make_color_rgb(180, 210, 240);
    if (string_pos("CRITICAL", _line) > 0 || string_pos("BREACH", _line) > 0 || string_pos("KILL", _line) > 0) _lcol = make_color_rgb(255, 90, 90);
    else if (string_pos("HIT", _line) > 0 || string_pos("IMPACT", _line) > 0) _lcol = make_color_rgb(255, 200, 80);
    else if (string_pos("ACCOMPLISHED", _line) > 0 || string_pos("SECURED", _line) > 0) _lcol = c_lime;
    else if (string_pos("PERSPECTIVE", _line) > 0) _lcol = make_color_rgb(100, 240, 255);

    draw_set_color(_lcol);
    draw_text_transformed(_log_x + 12, _log_y + 28 + l * 17, _line, 0.82, 0.82, 0);
}

// =========================================================================
// 6. FLOATING COMBAT TEXT LAYER (GUI SPACE)
// =========================================================================
for (var i = 0; i < array_length(floating_texts); i++) {
    var _ft = floating_texts[i];
    draw_set_alpha(_ft.alpha);
    draw_set_color(c_black);
    draw_text(_ft.x - string_width(_ft.text) * 0.5 + 1, _ft.y + 1, _ft.text);
    draw_set_color(_ft.color);
    draw_text(_ft.x - string_width(_ft.text) * 0.5, _ft.y, _ft.text);
    draw_set_alpha(1.0);
}

// =========================================================================
// 7. AFTER-ACTION REPORT (AAR) MODAL (VICTORY OR DEFEAT)
// =========================================================================
if (state == COMBAT_STATE.VICTORY_AAR || state == COMBAT_STATE.DEFEAT_AAR) {
    var _is_win = (state == COMBAT_STATE.VICTORY_AAR);
    var _mw_w = 680;
    var _mw_h = 440;
    var _mw_x = (_gw - _mw_w) / 2;
    var _mw_y = (_gh - _mw_h) / 2;

    draw_set_alpha(0.85);
    draw_set_color(c_black);
    draw_rectangle(0, 0, _gw, _gh, false);
    draw_set_alpha(1.0);

    draw_set_color(make_color_rgb(12, 18, 26));
    draw_rectangle(_mw_x, _mw_y, _mw_x + _mw_w, _mw_y + _mw_h, false);
    draw_set_color(_is_win ? c_lime : c_red);
    draw_rectangle(_mw_x, _mw_y, _mw_x + _mw_w, _mw_y + _mw_h, true);

    draw_set_color(_is_win ? make_color_rgb(80, 255, 120) : make_color_rgb(255, 80, 80));
    draw_text(_mw_x + 30, _mw_y + 24, _is_win ? "== MISSION ACCOMPLISHED // SECTOR SECURED ==" : "== DEFEAT // VANGUARD BATTERY DESTROYED ==");

    draw_set_color(c_white);
    draw_text(_mw_x + 30, _mw_y + 55, "COMBAT CASUALTIES & AFTER-ACTION SUMMARY:");

    if (_is_win) {
        draw_set_color(make_color_rgb(180, 220, 255));
        draw_text(_mw_x + 30, _mw_y + 85, "* Combat Operations Payout: +180,000 Credits (Cr)");
        draw_text(_mw_x + 30, _mw_y + 110, "* Faction Standing Gain: +15 Standing (The Terran Coalition)");
        draw_set_color(make_color_rgb(100, 255, 140));
        draw_text(_mw_x + 30, _mw_y + 135, "* PLATOON COMMENDATION: Alpha Squadron awarded Campaign Cross (+3 Accuracy)");
        draw_set_color(make_color_rgb(240, 210, 100));
        draw_text(_mw_x + 30, _mw_y + 170, "BATTLEFIELD SALVAGE RECOVERED (SAVED TO INVENTORY):");
        draw_set_color(make_color_rgb(200, 230, 255));
        draw_text(_mw_x + 50, _mw_y + 195, "-> 4x Vanguard Composite Plating (alloy_vanguard_comp)");
        draw_text(_mw_x + 50, _mw_y + 220, "-> 25x Raw Tungsten Ore (mat_tungsten)");
        draw_text(_mw_x + 50, _mw_y + 245, "-> 2x Syndicate Reaver Heavy Breech Assemblies");
    } else {
        draw_set_color(make_color_rgb(255, 80, 80));
        draw_text(_mw_x + 30, _mw_y + 85, "* CATASTROPHIC DEFEAT: Platoon forces overwhelmed in Sector 4.");
        draw_text(_mw_x + 30, _mw_y + 110, "* Emergency orbital med-evac deployed. Casualties admitted to ICU.");
        draw_text(_mw_x + 30, _mw_y + 135, "* PMC Morale reduced by -20 Morale.");
    }

    var _btn_p_x = _mw_x + 190;
    var _btn_p_y = _mw_y + 360;
    var _btn_p_w = 300;
    var _btn_p_h = 44;
    var _p_hov = (_mx >= _btn_p_x && _mx <= _btn_p_x + _btn_p_w && _my >= _btn_p_y && _my <= _btn_p_y + _btn_p_h);

    if (_p_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            if (_is_win) {
                obj_GameManager.add_funds(180000);
                obj_GameManager.add_alloy("alloy_vanguard_comp", 4);
                obj_GameManager.add_raw_material("mat_tungsten", 25);
                if (instance_exists(obj_FactionManager)) {
                    obj_FactionManager.modify_standing("faction_a", 15);
                }
            }
        }
        if (room_exists(rm_hq_terminal)) room_goto(rm_hq_terminal);
    }

    draw_set_color(_p_hov ? make_color_rgb(30, 90, 50) : make_color_rgb(18, 50, 30));
    draw_rectangle(_btn_p_x, _btn_p_y, _btn_p_x + _btn_p_w, _btn_p_y + _btn_p_h, false);
    draw_set_color(make_color_rgb(80, 240, 120));
    draw_rectangle(_btn_p_x, _btn_p_y, _btn_p_x + _btn_p_w, _btn_p_y + _btn_p_h, true);
    draw_set_color(c_white);
    draw_text(_btn_p_x + 28, _btn_p_y + 12, "[PROCEED TO HQ COMMAND TERMINAL]");
}

// =========================================================================
// 9. PROCEDURAL NEMESIS DROP-POD AMBUSH HUD & COMMS INTERCOM (Document 19)
// =========================================================================
if (state == COMBAT_STATE.NEMESIS_INCURSION) {
    // 1. Top Flashing Atmospheric Warning Banner
    var _banner_w = 900;
    var _banner_h = 52;
    var _banner_x = (1366 - _banner_w) * 0.5;
    var _banner_y = 18;

    var _flash = (current_time mod 400 < 200);
    draw_set_color(_flash ? make_color_rgb(180, 20, 20) : make_color_rgb(100, 10, 10));
    draw_rectangle(_banner_x, _banner_y, _banner_x + _banner_w, _banner_y + _banner_h, false);
    draw_set_color(_flash ? make_color_rgb(255, 180, 60) : make_color_rgb(200, 40, 40));
    draw_rectangle(_banner_x, _banner_y, _banner_x + _banner_w, _banner_y + _banner_h, true);

    draw_set_color(c_white);
    draw_text(_banner_x + 22, _banner_y + 10, "▲ EMERGENCY WARNING: UNIDENTIFIED DROP-POD TRAJECTORY DETECTED // SECTOR BREACH ▲");
    draw_set_color(make_color_rgb(255, 220, 120));
    var _alt_str = (incursion_data.pod_altitude > 0) ? ("DESCENT ALTITUDE: " + string(floor(incursion_data.pod_altitude)) + " METERS // IMPACT IMMINENT") : "ATMOSPHERIC PENETRATION CONFIRMED // TARGET ON GRID";
    draw_text(_banner_x + 22, _banner_y + 28, _alt_str);

    // 2. Substate 3: Front Mission Retro Comms Intercom Dialog Window
    if (nemesis_incursion_state >= 3) {
        var _box_w = 780;
        var _box_h = 210;
        var _box_x = (1366 - _box_w) * 0.5;
        var _box_y = 510;

        // Outer Beveled SNES Metallic Frame
        draw_set_color(make_color_rgb(14, 18, 24));
        draw_rectangle(_box_x, _box_y, _box_x + _box_w, _box_y + _box_h, false);
        draw_set_color(make_color_rgb(110, 120, 135)); // Highlight border
        draw_rectangle(_box_x, _box_y, _box_x + _box_w, _box_y + _box_h, true);
        draw_set_color(make_color_rgb(45, 50, 60)); // Inner recessed shadow
        draw_rectangle(_box_x + 2, _box_y + 2, _box_x + _box_w - 2, _box_y + _box_h - 2, true);

        // Pilot Portrait Box (128x128 inside frame)
        var _port_x = _box_x + 20;
        var _port_y = _box_y + 24;
        draw_set_color(make_color_rgb(8, 10, 14));
        draw_rectangle(_port_x, _port_y, _port_x + 128, _port_y + 128, false);
        draw_set_color(make_color_rgb(90, 100, 115));
        draw_rectangle(_port_x, _port_y, _port_x + 128, _port_y + 128, true);

        // Layered 5-Stack Procedural Portrait Compositor (Document 19, Phase 5)
        scr_draw_composite_portrait(incursion_data.nemesis_id, _port_x, _port_y, 128, true, "enraged");

        // Header Information
        var _info_x = _box_x + 168;
        draw_set_color(make_color_rgb(255, 140, 40));
        draw_text(_info_x, _box_y + 18, "[PRIORITY COMMS OVERRIDE] " + string_upper(incursion_data.faction_id));

        draw_set_color(make_color_rgb(240, 220, 120));
        draw_text(_info_x, _box_y + 38, incursion_data.nemesis_name + " [\"" + incursion_data.callsign + "\"] - " + incursion_data.preferred_chassis);

        // Crimson Nemesis Badge
        draw_set_color(make_color_rgb(180, 20, 20));
        draw_rectangle(_info_x, _box_y + 58, _info_x + 230, _box_y + 78, false);
        draw_set_color(make_color_rgb(255, 80, 80));
        draw_rectangle(_info_x, _box_y + 58, _info_x + 230, _box_y + 78, true);
        draw_set_color(c_white);
        draw_text(_info_x + 10, _box_y + 61, "▲ VENDETTA INVASION ACE ▲");

        // Dialogue Bark Text
        draw_set_color(make_color_rgb(220, 235, 255));
        draw_text_ext(_info_x, _box_y + 92, "\"" + incursion_data.bark_dialogue + "\"", 20, _box_w - 188);

        // Dismiss Prompt
        var _prompt_flash = (current_time mod 600 < 350);
        draw_set_color(_prompt_flash ? make_color_rgb(80, 230, 140) : make_color_rgb(40, 150, 90));
        draw_text(_box_x + _box_w - 320, _box_y + _box_h - 26, "[CLICK OR SPACE TO ENGAGE TARGET]");
    }
}
