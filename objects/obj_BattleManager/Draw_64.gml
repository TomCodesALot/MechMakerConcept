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
scr_draw_snes_panel(0, 0, _gw, 86, "", -1, false, 0.04);

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
    scr_draw_snes_button(_bx, _by, _btn_w, _btn_h, "A-0" + string(u + 1), _hov, _is_sel, make_color_rgb(80, 220, 255));

    // Mini AP Pips
    if (!_allied_u.is_destroyed) {
        for (var p = 0; p < _allied_u.max_ap; p++) {
            var _px = _bx + 6 + p * 8;
            var _py = _by + 20;
            var _has_ap = (p < _allied_u.current_ap);
            draw_set_color(_has_ap ? make_color_rgb(60, 240, 100) : make_color_rgb(18, 28, 22));
            draw_rectangle(_px, _py, _px + 6, _py + 7, false);
            draw_set_color(make_color_rgb(8, 14, 10));
            draw_rectangle(_px, _py, _px + 6, _py + 7, true);
        }
    } else {
        draw_set_color(c_red);
        draw_text(_bx + 6, _by + 16, "KIA");
    }
}

// Pre-Battle Deployment Deck & Hangar Staging Button
var _dd_x = 990;
var _dd_y = 12;
var _dd_w = 175;
var _dd_h = 36;
var _dd_hov = (_mx >= _dd_x && _mx <= _dd_x + _dd_w && _my >= _dd_y && _my <= _dd_y + _dd_h);
if (_dd_hov && _click) {
    deployment_deck_active = !deployment_deck_active;
}
scr_draw_snes_button(_dd_x, _dd_y, _dd_w, _dd_h, deployment_deck_active ? "[CLOSE DECK]" : "[DEPLOYMENT DECK]", _dd_hov, deployment_deck_active, make_color_rgb(100, 220, 255));

// Retreat / Abort Button (Top Right)
var _ab_x = 1180;
var _ab_y = 12;
var _ab_w = 170;
var _ab_h = 36;
var _ab_hov = (_mx >= _ab_x && _mx <= _ab_x + _ab_w && _my >= _ab_y && _my <= _ab_y + _ab_h);
if (_ab_hov && _click) {
    if (room_exists(rm_hq_terminal)) room_goto(rm_hq_terminal);
}
scr_draw_snes_button(_ab_x, _ab_y, _ab_w, _ab_h, "[ESC: RETREAT HQ]", _ab_hov, false, make_color_rgb(220, 90, 50));

// =========================================================================
// 2. ACTIVE UNIT STATUS, AP & HEAT BAR (y: 92 to 135)
// =========================================================================
if (_cur_u != undefined) {
    scr_draw_snes_panel(16, 92, 899, 43, "", -1, false, 0.03);

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
    scr_draw_snes_gauge(_heat_x, _heat_y + 18, 250, 14, _cur_u.current_heat, _cur_u.max_heat, _h_col);
}

// =========================================================================
// 3. FRONT MISSION TARGET DUEL & DIAGNOSTICS (Right Panel: x 930 to 1350)
// =========================================================================
var _diag_x = 930;
var _diag_y = 92;
var _diag_w = _gw - _diag_x - 16;
var _diag_h = 470;

var _is_target = false;
if (_view_u != undefined) _is_target = (_view_u.team == "HOSTILE");
scr_draw_snes_panel(_diag_x, _diag_y, _diag_w, _diag_h, _is_target ? "TARGET DIAGNOSTICS: HOSTILE" : "UNIT STATUS: ALLIED", _is_target ? make_color_rgb(255, 120, 120) : make_color_rgb(100, 220, 255), true, 0.04);

// Check if viewing targeted enemy vs selected allied unit
var _view_u = (target_unit_idx >= 0 && target_unit_idx < array_length(units) && !units[target_unit_idx].is_destroyed) ? units[target_unit_idx] : _cur_u;

if (_view_u != undefined) {
    var _is_target = (_view_u.team == "HOSTILE");
    draw_set_color(_is_target ? make_color_rgb(255, 120, 120) : make_color_rgb(100, 220, 255));
    draw_text(_diag_x + 16, _diag_y + 12, _is_target ? "== TARGET DIAGNOSTICS: HOSTILE ==" : "== UNIT STATUS SCHEMATIC: ALLIED ==");

    draw_set_color(c_white);
    draw_text(_diag_x + 16, _diag_y + 32, _view_u.callsign);
    draw_set_color(make_color_rgb(160, 190, 220));
    draw_text(_diag_x + 16, _diag_y + 48, "PILOT: " + _view_u.pilot_name + " | ACC: " + string(_view_u.accuracy) + "% | EVA: " + string(_view_u.evasion) + "%");

    // Gihren's Greed & Front Mission Operational Telemetry (Doc 20)
    var _lim_val = _view_u[$ "pilot_limit_pct"] ?? 120;
    var _ecm_val = _view_u[$ "ecm_dispersion_pct"] ?? 25;
    var _prop_cur = _view_u[$ "propellant_cur"] ?? 140;
    var _prop_max = _view_u[$ "propellant_max"] ?? 140;
    var _ter_obj = _view_u[$ "terrain"] ?? { ground: "A", space: "B" };
    var _ter_str = "G:" + string(_ter_obj[$ "ground"] ?? "A") + " S:" + string(_ter_obj[$ "space"] ?? "B");

    draw_set_color(make_color_rgb(255, 215, 80));
    draw_text(_diag_x + 16, _diag_y + 64, "LIMIT: " + string(_lim_val) + "% | ECM: " + string(_ecm_val) + "% | EN: " + string(_prop_cur) + "/" + string(_prop_max) + " | TER: " + _ter_str);

    // Component Breakdown Function
    var _draw_comp_bar = function(_lbl, _cur, _max, _armor, _intact, _bx, _by) {
        var _col = _intact ? ((_cur / _max > 0.4) ? c_lime : c_yellow) : c_red;
        draw_set_color(_intact ? c_white : c_gray);
        draw_text(_bx, _by, _lbl);
        draw_set_color(_col);
        draw_text(_bx + 140, _by, _intact ? (string(_cur) + " / " + string(_max) + " HP") : "[SEVERED]");

        if (_intact) {
            scr_draw_snes_gauge(_bx + 235, _by + 2, 120, 12, _cur, _max, _col);
        } else {
            draw_set_color(make_color_rgb(32, 12, 16));
            draw_rectangle(_bx + 235, _by + 2, _bx + 355, _by + 14, false);
            draw_set_color(c_red);
            draw_text(_bx + 250, _by, "[DESTROYED]");
        }
    };

    var _cy_start = _diag_y + 84;
    var _comps = _view_u.components;
    _draw_comp_bar("TORSO CORE", _comps.torso.cur, _comps.torso.max, _comps.torso.armor, _comps.torso.intact, _diag_x + 16, _cy_start);
    _draw_comp_bar("HEAD SENSORS", _comps.head.cur, _comps.head.max, _comps.head.armor, _comps.head.intact, _diag_x + 16, _cy_start + 24);
    _draw_comp_bar("LEFT ARM", _comps.arm_left.cur, _comps.arm_left.max, _comps.arm_left.armor, _comps.arm_left.intact, _diag_x + 16, _cy_start + 48);
    _draw_comp_bar("RIGHT ARM", _comps.arm_right.cur, _comps.arm_right.max, _comps.arm_right.armor, _comps.arm_right.intact, _diag_x + 16, _cy_start + 72);
    _draw_comp_bar("HYDRAULIC LEGS", _comps.legs.cur, _comps.legs.max, _comps.legs.armor, _comps.legs.intact, _diag_x + 16, _cy_start + 96);
    _draw_comp_bar("VERNIER PACK", _comps.backpack.cur, _comps.backpack.max, _comps.backpack.armor, _comps.backpack.intact, _diag_x + 16, _cy_start + 120);

    // Front Mission 4-Part Aimed Shot Targeting & Platoon Squad Status
    var _aim_y = _cy_start + 144;
    if (_is_target && _cur_u != undefined) {
        if (_view_u.squad_type == "SUPER_ACE") {
            draw_set_color(make_color_rgb(240, 210, 100));
            draw_text(_diag_x + 16, _aim_y, "FRONT MISSION AIMED SHOT [SUPER ACE]:");

            var _parts = ["torso", "arm_left", "arm_right", "legs", "head"];
            var _part_labels = ["TORSO", "L-ARM", "R-ARM", "LEGS", "HEAD"];
            for (var p = 0; p < array_length(_parts); p++) {
                var _p_name = _parts[p];
                var _px = _diag_x + 16 + p * 76;
                var _py = _aim_y + 18;
                var _pw = 70;
                var _ph = 20;
                var _phov = (_mx >= _px && _mx <= _px + _pw && _my >= _py && _my <= _py + _ph);
                var _psel = (_cur_u.targeted_limb == _p_name);
                if (_phov && _click) {
                    _cur_u.targeted_limb = _p_name;
                    _cur_u.is_aimed_shot = true;
                }
                scr_draw_snes_button(_px, _py, _pw, _ph, _part_labels[p], _phov, _psel, make_color_rgb(255, 180, 60));
            }

            var _aim_btn_x = _diag_x + 16;
            var _aim_btn_y = _aim_y + 42;
            var _aim_btn_w = 380;
            var _aim_btn_h = 22;
            var _ab_hov = (_mx >= _aim_btn_x && _mx <= _aim_btn_x + _aim_btn_w && _my >= _aim_btn_y && _my <= _aim_btn_y + _aim_btn_h);
            if (_ab_hov && _click) {
                _cur_u.is_aimed_shot = !_cur_u.is_aimed_shot;
            }
            var _aim_status_txt = _cur_u.is_aimed_shot ? ("[AIMED SHOT: ON // " + string_upper(_cur_u.targeted_limb) + " (-15% ACC)]") : "[AIMED SHOT: OFF // AUTO-SCATTER]";
            scr_draw_snes_button(_aim_btn_x, _aim_btn_y, _aim_btn_w, _aim_btn_h, _aim_status_txt, _ab_hov, _cur_u.is_aimed_shot, make_color_rgb(255, 120, 80));
        } else {
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_diag_x + 16, _aim_y, "PLATOON FORMATION [" + string(_view_u.squad_members_count) + "/3 GRUNTS OPERATIONAL]:");
            draw_set_color(c_lime);
            draw_text(_diag_x + 16, _aim_y + 20, "[LEAD MECH: READY] | [WING 1: " + (_view_u.squad_members_count >= 2 ? "OK" : "KIA") + "] | [WING 2: " + (_view_u.squad_members_count >= 3 ? "OK" : "KIA") + "]");
        }
    }

    // Selected Weapon Hit Calculation Breakdown
    if (_cur_u != undefined && selected_weapon < array_length(_cur_u.weapons)) {
        var _calc_y = _cy_start + 215;
        var _sel_w = _cur_u.weapons[selected_weapon];

        draw_set_color(make_color_rgb(240, 210, 100));
        draw_text(_diag_x + 16, _calc_y, "ACTIVE WEAPON: " + _sel_w.name);
        draw_set_color(make_color_rgb(180, 205, 230));
        draw_text(_diag_x + 16, _calc_y + 20, "* Range: " + string(_sel_w.range_min) + "-" + string(_sel_w.range_max) + " Cells | Projectile: " + _sel_w.proj_type);
        draw_text(_diag_x + 16, _calc_y + 38, "* AP Cost: " + string(_sel_w.ap_cost) + " AP | Thermal Gen: +" + string(_sel_w.heat_cost) + "% Heat");

        if (_is_target) {
            var _dist_to_t = calculate_distance(_cur_u.grid_c, _cur_u.grid_r, _view_u.grid_c, _view_u.grid_r);
            var _hit_pct = calculate_hit_chance(_cur_u, _view_u, _dist_to_t);
            if (_cur_u.is_aimed_shot) _hit_pct = max(10, _hit_pct - 15);

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

scr_draw_snes_panel(_act_x, _act_y, _act_w, _act_h, "TACTICAL COMMAND BUS // MANEUVER & ORDNANCE", make_color_rgb(100, 220, 255), false, 0.04);

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

    scr_draw_snes_button(_cur_bx, _cur_by, _b_w, _b_h, _bd.label, _b_hov, false, make_color_rgb(100, 220, 255));
}

// =========================================================================
// 4b. FLAGSHIP ORBITAL FIRE SUPPORT & TACTICAL SUPERWEAPONS (Docs 23 & 24)
// =========================================================================
if (instance_exists(obj_GameManager) && obj_GameManager.flagship.upgrades.weapons_tier >= 2) {
    var _fs = obj_GameManager.flagship;
    var _wt = _fs.upgrades.weapons_tier;
    var _orb_x = _act_x;
    var _orb_y = _act_y - 34;
    var _orb_w = 340;
    var _orb_h = 28;
    var _orb_rdy = (_fs.orbital_strike_available && state == COMBAT_STATE.PLAYER_PHASE);
    var _orb_hov = (_mx >= _orb_x && _mx <= _orb_x + _orb_w && _my >= _orb_y && _my <= _orb_y + _orb_h);

    if (_orb_rdy && _orb_hov && _click) {
        _fs.orbital_strike_available = false;
        var _cd = (_wt == 2) ? 3 : ((_wt <= 4) ? 2 : 1);
        if (_fs.specialization_protocol == "siege_fortress") _cd = max(1, _cd - 1);
        _fs.orbital_strike_cooldown = _cd;
        screen_shake = (_wt >= 5) ? 26.0 : 20.0;

        var _dmg_min = 600;
        var _dmg_max = 1100;
        var _wpn_name = "600mm Spinal Mass Drivers";
        if (_wt == 3) {
            _dmg_min = 1200; _dmg_max = 1800;
            _wpn_name = "Spinal Particle Lance";
        } else if (_wt == 4) {
            _dmg_min = 2000; _dmg_max = 3000;
            _wpn_name = "Kinetic Rod Penetrator Array";
        } else if (_wt >= 5) {
            _dmg_min = 3500; _dmg_max = 5000;
            _wpn_name = "Doomsday Tachyon Cleaver";
        }

        if (_fs.specialization_protocol == "siege_fortress") {
            _dmg_min = floor(_dmg_min * 1.5);
            _dmg_max = floor(_dmg_max * 1.5);
        }

        var _targets_hit = 0;
        for (var u = 0; u < array_length(units); u++) {
            var _un = units[u];
            if ((_un.team == "ENEMY" || _un.team == 1) && !_un.is_destroyed) {
                var _dmg = irandom_range(_dmg_min, _dmg_max);
                if (variable_struct_exists(_un, "components") && variable_struct_exists(_un.components, "torso")) {
                    _un.components.torso.cur = max(0, _un.components.torso.cur - _dmg);
                    if (_un.components.torso.cur <= 0) {
                        _un.is_destroyed = true;
                        _un.components.torso.intact = false;
                        _un.anim_state = "destroyed";
                    }
                } else if (variable_struct_exists(_un, "current_hp")) {
                    _un.current_hp = max(0, _un.current_hp - _dmg);
                    if (_un.current_hp <= 0) _un.is_destroyed = true;
                }
                _targets_hit++;
                array_push(floating_texts, {
                    x: _un.grid_c * 48,
                    y: _un.grid_r * 48 - 20,
                    text: "-" + string(_dmg) + " " + string_upper(_wpn_name) + "!",
                    col: (_wt >= 5) ? c_fuchsia : c_red,
                    alpha: 1.0,
                    life: 70
                });
                if (_un.is_destroyed) {
                    add_log("[ORBITAL KILL] " + _un.callsign + " vaporized by " + _wpn_name + "!");
                }
            }
        }
        add_log("[ORBITAL STRIKE] USN-X Hephaestus fired " + _wpn_name + "! Obliterated " + string(_targets_hit) + " hostile target(s)!");
    }

    draw_set_color(_orb_rdy ? (_orb_hov ? make_color_rgb(100, 30, 20) : make_color_rgb(60, 18, 12)) : make_color_rgb(18, 22, 28));
    draw_rectangle(_orb_x, _orb_y, _orb_x + _orb_w, _orb_y + _orb_h, false);
    draw_set_color(_orb_rdy ? make_color_rgb(255, 60, 40) : make_color_rgb(45, 60, 75));
    draw_rectangle(_orb_x, _orb_y, _orb_x + _orb_w, _orb_y + _orb_h, true);
    draw_set_color(_orb_rdy ? c_white : c_gray);
    var _strike_lbl = _orb_rdy ? ("* [O] CALL FLAGSHIP " + (_wt >= 5 ? "TACHYON CLEAVER" : "ORBITAL STRIKE") + " (READY)") : ("* FLAGSHIP ORBITAL SUPPORT (" + (_fs.orbital_strike_cooldown > 0 ? ("COOLDOWN: " + string(_fs.orbital_strike_cooldown) + "T") : "RELOADING") + ")");
    draw_text_transformed(_orb_x + 10, _orb_y + 6, _strike_lbl, 0.82, 0.82, 0);
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


// =========================================================================
// 10. PRE-BATTLE DEPLOYMENT DECK & CHASSIS SWAPPING MODAL (Full Staging)
// =========================================================================
if (deployment_deck_active) {
    // Dim background
    draw_set_alpha(0.88);
    draw_set_color(c_black);
    draw_rectangle(0, 0, _gw, _gh, false);
    draw_set_alpha(1.0);

    var _deck_x = 24;
    var _deck_y = 16;
    var _deck_w = _gw - 48;
    var _deck_h = _gh - 32;

    scr_draw_snes_panel(_deck_x, _deck_y, _deck_w, _deck_h, "PRE-BATTLE DEPLOYMENT DECK // HANGAR CHASSIS STAGING & THEATER SELECTOR", make_color_rgb(100, 220, 255), true, 0.05);

    // Close Button (Top-Right)
    var _close_x = _deck_x + _deck_w - 110;
    var _close_y = _deck_y + 8;
    var _close_w = 95;
    var _close_h = 28;
    var _close_hov = (_mx >= _close_x && _mx <= _close_x + _close_w && _my >= _close_y && _my <= _close_y + _close_h);
    if (_close_hov && _click) {
        deployment_deck_active = false;
    }
    scr_draw_snes_button(_close_x, _close_y, _close_w, _close_h, "[X CLOSE]", _close_hov, false, make_color_rgb(220, 80, 80));

    // COLUMN 1: UNIT SLOTS (x: _deck_x + 16, w: 270)
    var _col1_x = _deck_x + 16;
    var _col1_y = _deck_y + 45;
    var _col1_w = 270;

    // Team Tabs
    var _tab_allied_hov = (_mx >= _col1_x && _mx <= _col1_x + 130 && _my >= _col1_y && _my <= _col1_y + 26);
    if (_tab_allied_hov && _click) deployment_selected_team = "ALLIED";
    scr_draw_snes_button(_col1_x, _col1_y, 130, 26, "ALLIED PMC (8)", _tab_allied_hov, (deployment_selected_team == "ALLIED"), make_color_rgb(80, 220, 255));

    var _tab_hostile_hov = (_mx >= _col1_x + 135 && _mx <= _col1_x + 265 && _my >= _col1_y && _my <= _col1_y + 26);
    if (_tab_hostile_hov && _click) deployment_selected_team = "HOSTILE";
    scr_draw_snes_button(_col1_x + 135, _col1_y, 130, 26, "HOSTILE OPFOR (8)", _tab_hostile_hov, (deployment_selected_team == "HOSTILE"), make_color_rgb(255, 100, 100));

    // Slots 0 to 7
    for (var s = 0; s < 8; s++) {
        var _slot_idx = (deployment_selected_team == "ALLIED") ? s : (s + 8);
        if (_slot_idx >= array_length(units)) break;
        var _su = units[_slot_idx];
        var _sy = _col1_y + 36 + (s * 75);
        var _sh = 70;
        var _shov = (_mx >= _col1_x && _mx <= _col1_x + _col1_w && _my >= _sy && _my <= _sy + _sh);
        var _ssel = (deployment_selected_slot == _slot_idx);

        if (_shov && _click) {
            deployment_selected_slot = _slot_idx;
        }

        draw_set_color(_ssel ? make_color_rgb(20, 48, 70) : (_shov ? make_color_rgb(16, 28, 42) : make_color_rgb(10, 16, 24)));
        draw_rectangle(_col1_x, _sy, _col1_x + _col1_w, _sy + _sh, false);
        draw_set_color(_ssel ? make_color_rgb(80, 220, 255) : make_color_rgb(32, 50, 72));
        draw_rectangle(_col1_x, _sy, _col1_x + _col1_w, _sy + _sh, true);

        draw_set_color(_ssel ? make_color_rgb(100, 230, 255) : c_white);
        draw_text(_col1_x + 8, _sy + 6, _su.callsign);
        draw_set_color(make_color_rgb(160, 190, 220));
        draw_text(_col1_x + 8, _sy + 26, "TYPE: " + string_upper(_su.mech_type) + " [" + string_upper(_su.move_type) + "]");

        var _f_tag = (_su.squad_type == "SUPER_ACE") ? "★ [SUPER ACE]" : ("[" + string(_su.squad_members_count) + "x PLATOON]");
        var _f_col = (_su.squad_type == "SUPER_ACE") ? make_color_rgb(255, 215, 80) : make_color_rgb(80, 240, 140);
        draw_set_color(_f_col);
        draw_text(_col1_x + 8, _sy + 46, _f_tag + " | HP: " + string(_su.components.torso.max));
    }

    // COLUMN 2: CAD CHAMBER & CHASSIS SWAPPER (x: _deck_x + 300, w: 580)
    var _col2_x = _deck_x + 300;
    var _col2_y = _deck_y + 45;
    var _col2_w = 580;

    var _cur_slot_u = units[clamp(deployment_selected_slot, 0, array_length(units) - 1)];

    // CAD Chamber Viewport Box
    var _cad_h = 300;
    draw_set_color(make_color_rgb(8, 12, 18));
    draw_rectangle(_col2_x, _col2_y, _col2_x + _col2_w, _col2_y + _cad_h, false);
    draw_set_color(make_color_rgb(45, 75, 110));
    draw_rectangle(_col2_x, _col2_y, _col2_x + _col2_w, _col2_y + _cad_h, true);

    // Chamber Grid Lines & Concentric Rings
    var _cad_cx = _col2_x + (_col2_w * 0.5);
    var _cad_cy = _col2_y + 220;
    draw_set_color(make_color_rgb(18, 30, 46));
    draw_ellipse(_cad_cx - 140, _cad_cy - 45, _cad_cx + 140, _cad_cy + 45, true);
    draw_ellipse(_cad_cx - 90, _cad_cy - 28, _cad_cx + 90, _cad_cy + 28, true);
    draw_set_color(make_color_rgb(10, 20, 32));
    draw_ellipse(_cad_cx - 70, _cad_cy - 20, _cad_cx + 70, _cad_cy + 20, false);

    // Draw Live Animated Mobile Suit in CAD Chamber
    scr_draw_animated_mobile_suit(_cur_slot_u.mech_type, deployment_anim_state, _cad_cx, _cad_cy, deployment_facing, 1.40, _cur_slot_u.image_blend, 1.0);

    // Overhead Model Tag
    draw_set_color(make_color_rgb(100, 220, 255));
    draw_text(_col2_x + 14, _col2_y + 10, "LIVE 3D CAD PROJECTION // " + string_upper(_cur_slot_u.callsign));
    var _dir_labels = ["SOUTH-EAST ↘ (FRONT-RIGHT)", "SOUTH-WEST ↙ (FRONT-LEFT)", "NORTH-EAST ↗ (BACK-RIGHT)", "NORTH-WEST ↖ (BACK-LEFT)"];
    draw_set_color(make_color_rgb(255, 215, 100));
    draw_text(_col2_x + 14, _col2_y + 28, "HEADING: " + _dir_labels[deployment_facing]);

    // 4-Way Direction Facing Control Buttons
    var _fc_y = _col2_y + _cad_h + 10;
    var _dirs = [
        { label: "[SE ↘]", face: 0 },
        { label: "[SW ↙]", face: 1 },
        { label: "[NE ↗]", face: 2 },
        { label: "[NW ↖]", face: 3 }
    ];
    for (var d = 0; d < 4; d++) {
        var _fx = _col2_x + (d * 75);
        var _fhov = (_mx >= _fx && _mx <= _fx + 70 && _my >= _fc_y && _my <= _fc_y + 26);
        var _fsel = (deployment_facing == _dirs[d].face);
        if (_fhov && _click) {
            deployment_facing = _dirs[d].face;
            _cur_slot_u.facing = deployment_facing;
        }
        scr_draw_snes_button(_fx, _fc_y, 70, 26, _dirs[d].label, _fhov, _fsel, make_color_rgb(100, 220, 255));
    }

    // Animation Pose Selector Buttons
    var _anim_states = [
        { label: "[IDLE]", a_state: "idle" },
        { label: "[WALK]", a_state: "walk" },
        { label: "[FIRE]", a_state: "fire_rifle" },
        { label: "[HIT]", a_state: "hit" }
    ];
    for (var a = 0; a < 4; a++) {
        var _ax = _col2_x + 310 + (a * 66);
        var _ahov = (_mx >= _ax && _mx <= _ax + 62 && _my >= _fc_y && _my <= _fc_y + 26);
        var _asel = (deployment_anim_state == _anim_states[a].a_state);
        if (_ahov && _click) {
            deployment_anim_state = _anim_states[a].a_state;
        }
        scr_draw_snes_button(_ax, _fc_y, 62, 26, _anim_states[a].label, _ahov, _asel, make_color_rgb(180, 140, 255));
    }

    // Chassis Selector Controls
    var _swp_y = _fc_y + 36;
    var _prev_hov = (_mx >= _col2_x && _mx <= _col2_x + 130 && _my >= _swp_y && _my <= _swp_y + 28);
    if (_prev_hov && _click) {
        deployment_chassis_idx = (deployment_chassis_idx - 1 + array_length(chassis_swap_pool)) % array_length(chassis_swap_pool);
        swap_unit_chassis(deployment_selected_slot, chassis_swap_pool[deployment_chassis_idx]);
    }
    scr_draw_snes_button(_col2_x, _swp_y, 130, 28, "< PREV CHASSIS", _prev_hov, false, make_color_rgb(100, 220, 255));

    var _next_hov = (_mx >= _col2_x + _col2_w - 130 && _mx <= _col2_x + _col2_w && _my >= _swp_y && _my <= _swp_y + 28);
    if (_next_hov && _click) {
        deployment_chassis_idx = (deployment_chassis_idx + 1) % array_length(chassis_swap_pool);
        swap_unit_chassis(deployment_selected_slot, chassis_swap_pool[deployment_chassis_idx]);
    }
    scr_draw_snes_button(_col2_x + _col2_w - 130, _swp_y, 130, 28, "NEXT CHASSIS >", _next_hov, false, make_color_rgb(100, 220, 255));

    // Active Chassis Title in Middle
    draw_set_color(c_white);
    draw_text(_col2_x + 145, _swp_y + 6, string_upper(_cur_slot_u.mech_type) + " (" + string(deployment_chassis_idx + 1) + "/" + string(array_length(chassis_swap_pool)) + ")");

    // Quick Pick Custom Combinations Archetypes
    var _arche_y = _swp_y + 38;
    var _archetypes = [
        { label: "[BIPED HEAVY]", idx: 0 },
        { label: "[HOVER SNIPER]", idx: 1 },
        { label: "[TREAD SIEGE]", idx: 2 },
        { label: "[AERO STRIKER]", idx: 3 }
    ];
    for (var k = 0; k < 4; k++) {
        var _kx = _col2_x + (k * 142);
        var _khov = (_mx >= _kx && _mx <= _kx + 138 && _my >= _arche_y && _my <= _arche_y + 26);
        if (_khov && _click) {
            deployment_chassis_idx = _archetypes[k].idx;
            swap_unit_chassis(deployment_selected_slot, chassis_swap_pool[deployment_chassis_idx]);
        }
        scr_draw_snes_button(_kx, _arche_y, 138, 26, _archetypes[k].label, _khov, (deployment_chassis_idx == _archetypes[k].idx), make_color_rgb(255, 200, 80));
    }

    // Formation Doctrine Toggle Button
    var _form_y = _arche_y + 36;
    var _is_ace = (_cur_slot_u.squad_type == "SUPER_ACE");
    var _form_label = _is_ace ? "★ FORMATION: [1-MECH SUPER ACE] (CLICK FOR 3-MECH PLATOON)" : "FORMATION: [3-MECH MASS-PRODUCTION PLATOON] (CLICK FOR ACE)";
    var _form_hov = (_mx >= _col2_x && _mx <= _col2_x + _col2_w && _my >= _form_y && _my <= _form_y + 30);
    if (_form_hov && _click) {
        if (_is_ace) {
            _cur_slot_u.squad_type = "PLATOON_3";
            _cur_slot_u.squad_members_count = 3;
            _cur_slot_u.squad_max_count = 3;
        } else {
            _cur_slot_u.squad_type = "SUPER_ACE";
            _cur_slot_u.squad_members_count = 1;
            _cur_slot_u.squad_max_count = 1;
        }
    }
    scr_draw_snes_button(_col2_x, _form_y, _col2_w, 30, _form_label, _form_hov, _is_ace, _is_ace ? make_color_rgb(255, 215, 80) : make_color_rgb(80, 240, 140));

    // Telemetry Summary Card
    var _spec_y = _form_y + 40;
    scr_draw_snes_panel(_col2_x, _spec_y, _col2_w, 130, "CHASSIS SPECIFICATIONS // BATTLE READINESS", make_color_rgb(140, 180, 220), false, 0.03);
    draw_set_color(make_color_rgb(180, 220, 255));
    draw_text(_col2_x + 16, _spec_y + 24, "PROPULSION: " + string_upper(_cur_slot_u.move_type) + " | SPACE ADAPTED: " + (_cur_slot_u.space_adapted ? "YES (NO SPACE PENALTY)" : "NO (1 AP PENALTY)"));
    draw_text(_col2_x + 16, _spec_y + 46, "ARMOR INTEGRITY: " + string(_cur_slot_u.components.torso.max) + " HP | ACCURACY: " + string(_cur_slot_u.accuracy) + "% | EVASION: " + string(_cur_slot_u.evasion) + "%");
    draw_text(_col2_x + 16, _spec_y + 68, "AP CAPACITY: " + string(_cur_slot_u.max_ap) + " AP | MAX THERMAL LIMIT: " + string(_cur_slot_u.max_heat) + " C");
    draw_set_color(make_color_rgb(240, 210, 120));
    draw_text(_col2_x + 16, _spec_y + 92, "TERRAIN EFFICIENCY: Road (1 AP) | Rubble (" + string(get_terrain_move_cost(_cur_slot_u, 0, 0, 1, 0)) + " AP) | Water (" + string(get_terrain_move_cost(_cur_slot_u, 0, 0, 2, 0)) + " AP)");

    // COLUMN 3: THEATER MAP SELECTION & LAUNCH (x: _deck_x + 900, w: 380)
    var _col3_x = _deck_x + 900;
    var _col3_y = _deck_y + 45;
    var _col3_w = _deck_w - 920;

    draw_set_color(make_color_rgb(100, 220, 255));
    draw_text(_col3_x, _col3_y, "OPERATIONAL THEATER SELECTION (24 MAPS):");

    // Category Filter Tabs
    var _filter_tabs = [
        { label: "ALL (24)", key: "ALL", w: 86 },
        { label: "EARTH (10)", key: "EARTH", w: 90 },
        { label: "SPACE (10)", key: "SPACE", w: 90 },
        { label: "TEST (4)", key: "TEST", w: 86 }
    ];
    var _cur_tab_x = _col3_x;
    var _tab_y = _col3_y + 20;
    for (var t = 0; t < array_length(_filter_tabs); t++) {
        var _ft = _filter_tabs[t];
        var _thov = (_mx >= _cur_tab_x && _mx <= _cur_tab_x + _ft.w && _my >= _tab_y && _my <= _tab_y + 22);
        var _tsel = (deployment_map_filter == _ft.key);
        if (_thov && _click) {
            deployment_map_filter = _ft.key;
            deployment_map_page = 0;
        }
        scr_draw_snes_button(_cur_tab_x, _tab_y, _ft.w, 22, _ft.label, _thov, _tsel, make_color_rgb(100, 220, 255));
        _cur_tab_x += _ft.w + 6;
    }

    // Filter maps array
    var _filtered_maps = [];
    for (var m = 0; m < array_length(map_definitions); m++) {
        var _md = map_definitions[m];
        if (deployment_map_filter == "ALL" || _md.category == deployment_map_filter) {
            array_push(_filtered_maps, _md);
        }
    }

    var _total_maps = array_length(_filtered_maps);
    var _total_pages = max(1, ceil(_total_maps / 4));
    deployment_map_page = clamp(deployment_map_page, 0, _total_pages - 1);

    // Pagination Controls Bar
    var _pg_y = _col3_y + 46;
    var _p_prev_hov = (_mx >= _col3_x && _mx <= _col3_x + 75 && _my >= _pg_y && _my <= _pg_y + 22);
    if (_p_prev_hov && _click && deployment_map_page > 0) {
        deployment_map_page--;
    }
    scr_draw_snes_button(_col3_x, _pg_y, 75, 22, "< PREV", _p_prev_hov, false, make_color_rgb(100, 220, 255));

    var _p_next_hov = (_mx >= _col3_x + _col3_w - 75 && _mx <= _col3_x + _col3_w && _my >= _pg_y && _my <= _pg_y + 22);
    if (_p_next_hov && _click && deployment_map_page < _total_pages - 1) {
        deployment_map_page++;
    }
    scr_draw_snes_button(_col3_x + _col3_w - 75, _pg_y, 75, 22, "NEXT >", _p_next_hov, false, make_color_rgb(100, 220, 255));

    draw_set_color(make_color_rgb(255, 215, 100));
    draw_text(_col3_x + 95, _pg_y + 3, "PAGE " + string(deployment_map_page + 1) + " / " + string(_total_pages) + " (" + string(_total_maps) + " THEATERS)");

    // Render 4 Map Cards for Current Page
    var _start_idx = deployment_map_page * 4;
    for (var i = 0; i < 4; i++) {
        var _idx = _start_idx + i;
        if (_idx >= _total_maps) break;
        var _md = _filtered_maps[_idx];
        var _my_card = _col3_y + 74 + (i * 112);
        var _mh_card = 106;
        var _m_hov = (_mx >= _col3_x && _mx <= _col3_x + _col3_w && _my >= _my_card && _my <= _my_card + _mh_card);
        var _m_sel = (current_map_id == _md.id);

        if (_m_hov && _click) {
            load_map(_md.id);
        }

        draw_set_color(_m_sel ? make_color_rgb(24, 46, 68) : (_m_hov ? make_color_rgb(16, 26, 38) : make_color_rgb(10, 16, 24)));
        draw_rectangle(_col3_x, _my_card, _col3_x + _col3_w, _my_card + _mh_card, false);
        draw_set_color(_m_sel ? make_color_rgb(80, 220, 255) : make_color_rgb(40, 60, 85));
        draw_rectangle(_col3_x, _my_card, _col3_x + _col3_w, _my_card + _mh_card, true);

        draw_set_color(_m_sel ? make_color_rgb(100, 240, 255) : c_white);
        draw_text(_col3_x + 10, _my_card + 6, "MAP " + string(_md.id + 1) + ": " + _md.name);

        draw_set_color(make_color_rgb(255, 200, 80));
        draw_text(_col3_x + 10, _my_card + 24, "THEATER: " + _md.theater + " [" + _md.category + "] | GRAV: " + string(_md.gravity) + "G");

        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text_ext(_col3_x + 10, _my_card + 42, _md.desc, 16, _col3_w - 20);

        draw_set_color(make_color_rgb(80, 220, 140));
        draw_text(_col3_x + 10, _my_card + 84, _md.ambient_tag);
    }

    // Deploy / Launch Button
    var _lnch_x = _col3_x;
    var _lnch_y = _col3_y + 530;
    var _lnch_w = _col3_w;
    var _lnch_h = 60;
    var _lnch_hov = (_mx >= _lnch_x && _mx <= _lnch_x + _lnch_w && _my >= _lnch_y && _my <= _lnch_y + _lnch_h);
    if (_lnch_hov && _click) {
        deployment_deck_active = false;
        state = COMBAT_STATE.PLAYER_PHASE;
        select_unit(0);
        add_log("[DEPLOYMENT COMPLETE] Battlegroup deployed to " + map_definitions[current_map_id].name);
    }
    scr_draw_snes_button(_lnch_x, _lnch_y, _lnch_w, _lnch_h, ">> DEPLOY TO BATTLEFIELD <<", _lnch_hov, false, make_color_rgb(80, 255, 140));
}
