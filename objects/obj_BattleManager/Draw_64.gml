/// @description obj_BattleManager Draw GUI Event
// Renders Grand-Scale Tactical HUD, Platoon Timeline, Front Mission Limb Diagnostics & Command Controls
// Strictly implements docs/17_grand_scale_isometric_combat_system.md & docs/05_tactical_combat.md

var _gw = display_get_gui_width();
var _gh = display_get_gui_height();
var _mx = device_mouse_x_to_gui(0);
var _my = device_mouse_y_to_gui(0);
var _click = mouse_check_button_pressed(mb_left);

var _cur_u = (selected_unit_idx >= 0 && selected_unit_idx < array_length(units)) ? units[selected_unit_idx] : undefined;

// -------------------------------------------------------------------------
// GIHREN'S GREED + FRONT MISSION 2-TIER CINEMATIC BATTLE CLASH OVERLAY
// -------------------------------------------------------------------------
if (battle_cinematic.active) {
    draw_battle_cinematic_stage();
    exit;
}

// =========================================================================
// 1. TOP SECTOR TELEMETRY RIBBON (y: 0 to 48) - 16-Bit Front Mission Steel
// =========================================================================
scr_draw_snes_panel(0, 0, _gw, 48, "", -1, false, 0.04);

// Left: Sector Classification & Phase Badge
draw_set_color(make_color_rgb(100, 220, 255));
draw_text(16, 6, "SECTOR 04: MINING OUTPOST // THEATER: " + string_upper(map_definitions[current_map_id].theater));

var _phase_str = "[PLAYER COMMAND PHASE]";
var _phase_col = make_color_rgb(60, 240, 100);
if (state == COMBAT_STATE.AI_PHASE) {
    _phase_str = "[HOSTILE PHASE // ENEMY ADVANCE]";
    _phase_col = make_color_rgb(255, 80, 80);
} else if (state == COMBAT_STATE.MOVE_MODE) {
    _phase_str = (split_mode_active ? "[SPLIT SQUAD MARCH // SELECT CELL]" : "[BATTLEGROUP MARCH // SELECT CELL]");
    _phase_col = make_color_rgb(100, 220, 255);
} else if (state == COMBAT_STATE.TARGET_MODE) {
    _phase_str = "[AUTOMATED MAXIMUM FIREPOWER // SELECT TARGET]";
    _phase_col = make_color_rgb(255, 200, 80);
} else if (state == COMBAT_STATE.AUTO_SIM) {
    _phase_str = "[AUTONOMOUS SIMULATION ACTIVE]";
    _phase_col = make_color_rgb(210, 140, 255);
}
draw_set_color(_phase_col);
draw_text(16, 26, "STATUS: " + _phase_str + " | TURN: " + string(turn_number));

// Center: Allied vs Hostile Battlegroup Tallies
var _allied_alive = 0;
var _hostile_alive = 0;
for (var u = 0; u < array_length(units); u++) {
    if (!units[u].is_destroyed) {
        if (units[u].team == "ALLIED") _allied_alive++;
        else _hostile_alive++;
    }
}

draw_set_color(make_color_rgb(60, 220, 255));
draw_text(_gw * 0.38, 14, "PMC BATTLEGROUP: " + string(_allied_alive) + " UNITS");
draw_set_color(make_color_rgb(140, 170, 200));
draw_text(_gw * 0.38 + 160, 14, "|");
draw_set_color(make_color_rgb(255, 90, 80));
draw_text(_gw * 0.38 + 175, 14, "OPFOR: " + string(_hostile_alive) + " UNITS");

// Right: Quick Action Controls Chips
var _btn_y = 8;
var _btn_h = 32;

// [C] Cinematic Duels Toggle Button
var _cd_x = _gw - 430;
var _cd_w = 120;
var _cd_hov = (_mx >= _cd_x && _mx <= _cd_x + _cd_w && _my >= _btn_y && _my <= _btn_y + _btn_h);
if (_cd_hov && _click) {
    cinematic_combat_enabled = !cinematic_combat_enabled;
    scr_audio_play_ui("confirm");
}
scr_draw_snes_button(_cd_x, _btn_y, _cd_w, _btn_h, "[C] DUELS: " + (cinematic_combat_enabled ? "ON" : "OFF"), _cd_hov, cinematic_combat_enabled, cinematic_combat_enabled ? make_color_rgb(60, 240, 120) : make_color_rgb(220, 120, 80));

// [⚙] Audio Settings Button
var _aud_x = _cd_x + _cd_w + 8;
var _aud_w = 110;
var _aud_hov = (_mx >= _aud_x && _mx <= _aud_x + _aud_w && _my >= _btn_y && _my <= _btn_y + _btn_h);
if (_aud_hov && _click) {
    show_settings_modal = !show_settings_modal;
    scr_audio_play_ui("click");
}
var _is_aud_muted = scr_audio_is_muted();
scr_draw_snes_button(_aud_x, _btn_y, _aud_w, _btn_h, _is_aud_muted ? "[MUTED]" : "[⚙ AUDIO]", _aud_hov, _is_aud_muted, _is_aud_muted ? make_color_rgb(255, 90, 90) : make_color_rgb(100, 220, 255));

// [ESC] Retreat Button
var _ret_x = _aud_x + _aud_w + 8;
var _ret_w = 160;
var _ret_hov = (_mx >= _ret_x && _mx <= _ret_x + _ret_w && _my >= _btn_y && _my <= _btn_y + _btn_h);
if (_ret_hov && _click) {
    if (room_exists(rm_hq_terminal)) room_goto(rm_hq_terminal);
}
scr_draw_snes_button(_ret_x, _btn_y, _ret_w, _btn_h, "[ESC: RETREAT HQ]", _ret_hov, false, make_color_rgb(220, 80, 50));

// 1b. PROLOGUE AMBUSH DIRECTIVE (DOC 51)
var _is_prologue_combat = (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "active_combat_context") && !is_undefined(obj_GameManager.active_combat_context) && variable_struct_exists(obj_GameManager.active_combat_context, "is_prologue") && obj_GameManager.active_combat_context.is_prologue);
if (_is_prologue_combat) {
    var _pb_y = 50;
    var _pb_w = _gw - 40;
    var _pb_h = 24;
    draw_set_color(make_color_rgb(18, 28, 42));
    draw_rectangle(20, _pb_y, 20 + _pb_w, _pb_y + _pb_h, false);
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_rectangle(20, _pb_y, 20 + _pb_w, _pb_y + _pb_h, true);
    draw_set_color(make_color_rgb(100, 230, 255));
    draw_text(28, _pb_y + 4, "★ PROLOGUE SORTIE // DAWN OF THE MOBILE SUIT // PILOT GHA-00 PROTOTYPE // NEUTRALIZE 3 PIRATE RAIDER CRAFT ★");
}

// 1b. OPERATION GROUNDWORK // CADRE COMBAT GUIDANCE (DOC 50)
if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "tutorial_step") && obj_GameManager.tutorial_step == 4) {
    var _tb_y = 50;
    var _tb_w = _gw - 40;
    var _tb_h = 24;
    draw_set_color(make_color_rgb(14, 20, 32));
    draw_rectangle(20, _tb_y, 20 + _tb_w, _tb_y + _tb_h, false);
    draw_set_color(make_color_rgb(255, 180, 40));
    draw_rectangle(20, _tb_y, 20 + _tb_w, _tb_y + _tb_h, true);
    draw_set_color(make_color_rgb(255, 220, 80));
    draw_text(28, _tb_y + 4, "★ CADRE TACTICAL INSTRUCTION: 1. Click Unit -> 2. Click Cyan Tile to Move -> 3. Click [ATTACK] -> 4. Choose Aimed Limb Shot!");
}


// =========================================================================
// 2. ACTIVE UNIT STATUS & AP/HEAT HUD (Middle-Left, y: 56 to 110)
// =========================================================================
if (_cur_u != undefined) {
    var _stat_x = 20;
    var _stat_y = 56;
    var _stat_w = min(680, stack_drawer_x - 40);
    scr_draw_snes_panel(_stat_x, _stat_y, _stat_w, 50, "", -1, false, 0.03);

    draw_set_color(make_color_rgb(100, 220, 255));
    draw_text(_stat_x + 12, _stat_y + 8, string_upper(_cur_u.callsign));
    draw_set_color(make_color_rgb(160, 190, 220));
    draw_text(_stat_x + 12, _stat_y + 26, "PILOT: " + _cur_u.pilot_name + " | " + string_upper(_cur_u.mech_type));

    // AP Battery Pips
    var _ap_x = _stat_x + 280;
    var _ap_y = _stat_y + 8;
    draw_set_color(c_white);
    draw_text(_ap_x, _ap_y, "AP: " + string(_cur_u.current_ap) + "/" + string(_cur_u.max_ap));
    for (var p = 0; p < _cur_u.max_ap; p++) {
        var _px = _ap_x + p * 16;
        var _py = _ap_y + 18;
        var _has_ap = (p < _cur_u.current_ap);
        draw_set_color(_has_ap ? make_color_rgb(60, 240, 100) : make_color_rgb(26, 38, 30));
        draw_rectangle(_px, _py, _px + 12, _py + 10, false);
        draw_set_color(make_color_rgb(80, 255, 140));
        draw_rectangle(_px, _py, _px + 12, _py + 10, true);
    }

    // Heat Gauge
    var _heat_x = _ap_x + 150;
    var _heat_y = _stat_y + 8;
    var _h_norm = clamp(_cur_u.current_heat / _cur_u.max_heat, 0, 1);
    var _h_col = (_h_norm > 0.8) ? c_red : ((_h_norm > 0.5) ? c_orange : make_color_rgb(100, 200, 255));
    draw_set_color(c_white);
    draw_text(_heat_x, _heat_y, "HEAT: " + string(floor(_cur_u.current_heat)) + "%");
    scr_draw_snes_gauge(_heat_x, _heat_y + 18, 140, 12, _cur_u.current_heat, _cur_u.max_heat, _h_col);
}


// =========================================================================
// 3. TARGETING FORECAST & COMBAT TELEMETRY (When in TARGET_MODE)
// =========================================================================
if (state == COMBAT_STATE.TARGET_MODE && _cur_u != undefined) {
    var _fc_x = 20;
    var _fc_y = 114;
    var _fc_w = min(420, stack_drawer_x - 40);
    var _fc_h = 180;

    scr_draw_snes_panel(_fc_x, _fc_y, _fc_w, _fc_h, "AUTOMATED MAXIMUM FIREPOWER // FORECAST", make_color_rgb(255, 180, 60), true, 0.04);

    var _friendly_stack = get_stack_at_tile(_cur_u.grid_c, _cur_u.grid_r, _cur_u.team);
    var _target_u = (target_unit_idx >= 0 && target_unit_idx < array_length(units) && !units[target_unit_idx].is_destroyed) ? units[target_unit_idx] : undefined;

    if (_target_u != undefined) {
        var _dist = calculate_distance(_cur_u.grid_c, _cur_u.grid_r, _target_u.grid_c, _target_u.grid_r);
        var _fp = get_stack_max_firepower(_friendly_stack, _target_u, _dist);

        draw_set_color(make_color_rgb(255, 90, 80));
        draw_text(_fc_x + 12, _fc_y + 14, "TARGET: " + string_upper(_target_u.callsign));
        draw_set_color(make_color_rgb(160, 190, 220));
        draw_text(_fc_x + 12, _fc_y + 32, "DISTANCE: " + string(_dist) + " TILES | EVASION: " + string(_target_u.evasion) + "%");

        draw_set_color(make_color_rgb(255, 215, 60));
        draw_text(_fc_x + 12, _fc_y + 54, "PARTICIPATING SALVO: [" + string(_fp.unit_count) + "/" + string(array_length(_friendly_stack)) + " UNITS FIRING]");
        draw_set_color(make_color_rgb(60, 240, 140));
        draw_text(_fc_x + 12, _fc_y + 72, "ESTIMATED DAMAGE: " + string(_fp.min_dmg) + " - " + string(_fp.max_dmg) + " HP");

        var _hit_est = calculate_hit_chance(_cur_u, _target_u, _dist);
        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(_fc_x + 12, _fc_y + 92, "LEAD ACCURACY: " + string(_hit_est) + "% | [CLICK TARGET TO FIRE]");

        // Goal F: Vector, High Ground & Cover HUD
        var _elev_delta = _cur_u.elev - _target_u.elev;
        var _inc_dir = iso_get_facing(_target_u.grid_c, _target_u.grid_r, _cur_u.grid_c, _cur_u.grid_r);
        var _is_rear = (_inc_dir == (_target_u.facing + 2) % 4);
        var _is_flank = (_inc_dir == (_target_u.facing + 1) % 4 || _inc_dir == (_target_u.facing + 3) % 4);
        var _tact_str = _is_rear ? "REAR AMBUSH (+40% CORE DMG / +30% HIT)" : (_is_flank ? "FLANKING ANGLE (+20% DMG / +15% HIT)" : "FRONTAL CONFRONTATION");
        var _tact_col = _is_rear ? make_color_rgb(255, 90, 90) : (_is_flank ? make_color_rgb(255, 200, 60) : make_color_rgb(180, 200, 220));
        draw_set_color(_tact_col);
        draw_text(_fc_x + 12, _fc_y + 112, "VECTOR: " + _tact_str);

        var _elev_str = (_elev_delta > 0) ? ("HIGH GROUND +" + string(15 * _elev_delta) + "% VELOCITY / +" + string(10 * _elev_delta) + "% HIT") : ((_elev_delta < 0) ? "UPHILL LOW-GROUND PENALTY (-15% DMG / -15% HIT)" : "LEVEL ELEVATION (ELEV " + string(_cur_u.elev) + ")");
        var _elev_col = (_elev_delta > 0) ? make_color_rgb(100, 240, 255) : ((_elev_delta < 0) ? make_color_rgb(240, 140, 100) : make_color_rgb(160, 180, 200));
        draw_set_color(_elev_col);
        draw_text(_fc_x + 12, _fc_y + 130, "TERRAIN: " + _elev_str);

        var _cov_val = grid_cover[_target_u.grid_c][_target_u.grid_r];
        var _is_supp = variable_struct_exists(_target_u, "is_suppressed") && _target_u.is_suppressed;
        var _stat_str = "";
        if (_cov_val == 2) _stat_str += "[HEAVY BASTION: 40% COV] ";
        else if (_cov_val == 1) _stat_str += "[LIGHT RUBBLE: 25% COV] ";
        if (_is_supp) _stat_str += "[TARGET PINNED/SUPPRESSED] ";
        if (_stat_str != "") {
            draw_set_color(make_color_rgb(255, 220, 100));
            draw_text(_fc_x + 12, _fc_y + 148, "DEFENSE: " + _stat_str);
        }
    } else {
        draw_set_color(make_color_rgb(200, 210, 225));
        draw_text(_fc_x + 12, _fc_y + 24, "Hover cursor over enemy tile to lock on.");
        draw_set_color(make_color_rgb(255, 215, 60));
        draw_text(_fc_x + 12, _fc_y + 48, "All units in battlegroup with range");
        draw_text(_fc_x + 12, _fc_y + 66, "will auto-fire maximum damage weapons!");
    }
}


// =========================================================================
// 4. RIGHT BATTLEGROUP STACK DRAWER (x: stack_drawer_x to _gw, y: 48 to 754)
// =========================================================================
var _dr_x = stack_drawer_x;
var _dr_y = 48;
var _dr_w = stack_drawer_w;
var _dr_h = _gh - _dr_y - 14;

// Left Edge Toggle Tab Button
var _tab_x = _dr_x - 24;
var _tab_y = 340;
var _tab_w = 24;
var _tab_h = 60;
var _tab_hov = (_mx >= _tab_x && _mx <= _tab_x + _tab_w && _my >= _tab_y && _my <= _tab_y + _tab_h);
if (_tab_hov && _click) {
    stack_drawer_open = !stack_drawer_open;
    scr_audio_play_ui("click");
}
draw_set_color(make_color_rgb(18, 25, 36));
draw_rectangle(_tab_x, _tab_y, _tab_x + _tab_w, _tab_y + _tab_h, false);
draw_set_color(_tab_hov ? make_color_rgb(0, 220, 255) : make_color_rgb(70, 95, 125));
draw_rectangle(_tab_x, _tab_y, _tab_x + _tab_w, _tab_y + _tab_h, true);
draw_set_color(c_white);
draw_text(_tab_x + 6, _tab_y + 22, stack_drawer_open ? "▶" : "◀");

if (_dr_x < _gw - 30) {
    // Render Expanded 16-Bit Metallic Console Drawer
    scr_draw_snes_panel(_dr_x, _dr_y, _dr_w, _dr_h, "BATTLEGROUP STACK [6 SLOTS]", make_color_rgb(100, 220, 255), true, 0.04);

    var _tile_stack = (_cur_u != undefined) ? get_stack_at_tile(_cur_u.grid_c, _cur_u.grid_r, _cur_u.team) : [];
    var _stack_cnt = array_length(_tile_stack);

    // Sub-header controls
    var _btn_reorg_w = 140;
    var _btn_reorg_h = 24;
    var _btn_reorg_x = _dr_x + 12;
    var _btn_reorg_y = _dr_y + 12;
    var _rhov = (_mx >= _btn_reorg_x && _mx <= _btn_reorg_x + _btn_reorg_w && _my >= _btn_reorg_y && _my <= _btn_reorg_y + _btn_reorg_h);
    if (_rhov && _click && _cur_u != undefined) {
        reorganize_stack(_cur_u.grid_c, _cur_u.grid_r, _cur_u.team);
    }
    scr_draw_snes_button(_btn_reorg_x, _btn_reorg_y, _btn_reorg_w, _btn_reorg_h, "[R] SWAP ROWS ⇄", _rhov, false, make_color_rgb(100, 220, 255));

    var _btn_split_w = 148;
    var _btn_split_x = _btn_reorg_x + _btn_reorg_w + 8;
    var _shov = (_mx >= _btn_split_x && _mx <= _btn_split_x + _btn_split_w && _my >= _btn_reorg_y && _my <= _btn_reorg_y + _btn_reorg_h);
    if (_shov && _click) {
        split_mode_active = !split_mode_active;
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_btn_split_x, _btn_reorg_y, _btn_split_w, _btn_reorg_h, split_mode_active ? "[✓] SPLIT ACTIVE" : "[S] SPLIT SQUAD", _shov, split_mode_active, split_mode_active ? make_color_rgb(0, 240, 140) : make_color_rgb(240, 190, 50));

    // Stack Count Summary Banner
    draw_set_color(make_color_rgb(160, 190, 220));
    draw_text(_dr_x + 14, _dr_y + 40, "CURRENT CELL OCCUPANCY: [" + string(_stack_cnt) + "/6 UNITS]");

    // Section 1: Vanguard (Frontline 1-3)
    draw_set_color(make_color_rgb(255, 215, 60));
    draw_text(_dr_x + 14, _dr_y + 60, "── VANGUARD (FRONTLINE 1–3) ──");

    // Section 2: Support (Rearguard 4-6)
    draw_set_color(make_color_rgb(100, 220, 255));
    draw_text(_dr_x + 14, _dr_y + 365, "── SUPPORT (REARGUARD 4–6) ──");

    // Render Compact Unit Cards (up to 6 units)
    for (var s = 0; s < 6; s++) {
        var _is_vanguard = (s < 3);
        var _card_y = _is_vanguard ? (_dr_y + 80 + s * 92) : (_dr_y + 385 + (s - 3) * 92);
        var _card_x = _dr_x + 12;
        var _card_w = 296;
        var _card_h = 86;

        if (s < _stack_cnt) {
            var _su = _tile_stack[s];
            var _is_sel = (_cur_u != undefined && _su == _cur_u);
            var _card_hov = (_mx >= _card_x && _mx <= _card_x + _card_w && _my >= _card_y && _my <= _card_y + _card_h);

            // Card Background
            draw_set_color(_is_sel ? make_color_rgb(24, 38, 56) : (_card_hov ? make_color_rgb(18, 28, 42) : make_color_rgb(14, 20, 30)));
            draw_rectangle(_card_x, _card_y, _card_x + _card_w, _card_y + _card_h, false);
            draw_set_color(_is_sel ? make_color_rgb(0, 240, 255) : make_color_rgb(45, 65, 90));
            draw_rectangle(_card_x, _card_y, _card_x + _card_w, _card_y + _card_h, true);

            // Unit Chassis Miniature / Icon
            var _spr_icon = get_unit_sprite(_su);
            if (sprite_exists(_spr_icon)) {
                draw_sprite_ext(_spr_icon, 0, _card_x + 28, _card_y + 70, 0.42, 0.42, 0, _su.image_blend, 1.0);
            }

            // Callsign & Pilot
            draw_set_color(_is_sel ? make_color_rgb(0, 240, 255) : c_white);
            draw_text(_card_x + 64, _card_y + 6, string_copy(_su.callsign, 1, 18));
            draw_set_color(make_color_rgb(150, 180, 210));
            draw_text(_card_x + 64, _card_y + 22, _su.pilot_name + " (" + string_upper(_su.mech_type) + ")");

            // HP Bar
            var _hp_cur = _su.components.torso.cur;
            var _hp_max = _su.components.torso.max;
            var _hp_pct = clamp(_hp_cur / max(1, _hp_max), 0.0, 1.0);
            var _hp_col = (_hp_pct > 0.6) ? make_color_rgb(60, 240, 100) : ((_hp_pct > 0.25) ? make_color_rgb(240, 200, 50) : make_color_rgb(255, 60, 60));

            draw_set_color(make_color_rgb(120, 150, 180));
            draw_text(_card_x + 64, _card_y + 40, "HP:");
            draw_set_color(make_color_rgb(16, 22, 32));
            draw_rectangle(_card_x + 90, _card_y + 42, _card_x + 200, _card_y + 50, false);
            draw_set_color(_hp_col);
            draw_rectangle(_card_x + 90, _card_y + 42, _card_x + 90 + floor(110 * _hp_pct), _card_y + 50, false);
            draw_set_color(make_color_rgb(45, 65, 90));
            draw_rectangle(_card_x + 90, _card_y + 42, _card_x + 200, _card_y + 50, true);
            draw_set_color(c_white);
            draw_text_transformed(_card_x + 204, _card_y + 40, string(_hp_cur) + "/" + string(_hp_max), 0.75, 0.75, 0);

            // AP Pips
            draw_set_color(make_color_rgb(120, 150, 180));
            draw_text(_card_x + 64, _card_y + 58, "AP:");
            for (var ap = 0; ap < _su.max_ap; ap++) {
                var _apx = _card_x + 90 + ap * 12;
                var _apy = _card_y + 60;
                var _has_ap = (ap < _su.current_ap);
                draw_set_color(_has_ap ? make_color_rgb(60, 240, 100) : make_color_rgb(24, 34, 28));
                draw_rectangle(_apx, _apy, _apx + 8, _apy + 7, false);
                draw_set_color(make_color_rgb(60, 180, 100));
                draw_rectangle(_apx, _apy, _apx + 8, _apy + 7, true);
            }

            // Detach / Split Button
            if (split_mode_active) {
                var _is_sp = (variable_struct_exists(split_selected_units, _su.id) && split_selected_units[$ _su.id] == true);
                var _sp_btn_w = 64;
                var _sp_btn_x = _card_x + _card_w - _sp_btn_w - 6;
                var _sp_btn_y = _card_y + 10;
                var _sphov = (_mx >= _sp_btn_x && _mx <= _sp_btn_x + _sp_btn_w && _my >= _sp_btn_y && _my <= _sp_btn_y + 22);
                if (_sphov && _click) {
                    if (_is_sp) variable_struct_remove(split_selected_units, _su.id);
                    else split_selected_units[$ _su.id] = true;
                    scr_audio_play_ui("click");
                }
                scr_draw_snes_button(_sp_btn_x, _sp_btn_y, _sp_btn_w, 22, _is_sp ? "[✓] PEEL" : "[+] PEEL", _sphov, _is_sp, _is_sp ? make_color_rgb(0, 240, 140) : make_color_rgb(240, 190, 50));
            } else {
                var _det_btn_w = 64;
                var _det_btn_x = _card_x + _card_w - _det_btn_w - 6;
                var _det_btn_y = _card_y + 10;
                var _dethov = (_mx >= _det_btn_x && _mx <= _det_btn_x + _det_btn_w && _my >= _det_btn_y && _my <= _det_btn_y + 22);
                if (_dethov && _click) {
                    // Solo detach: select this unit only and enter move mode
                    for (var u = 0; u < array_length(units); u++) {
                        if (units[u] == _su) {
                            select_unit(u);
                            split_mode_active = true;
                            split_selected_units = {};
                            split_selected_units[$ _su.id] = true;
                            recalculate_moves();
                            state = COMBAT_STATE.MOVE_MODE;
                            add_log("[DETACH] " + _su.callsign + " detached for solo orders.");
                            break;
                        }
                    }
                }
                scr_draw_snes_button(_det_btn_x, _det_btn_y, _det_btn_w, 22, "DETACH", _dethov, false, make_color_rgb(100, 220, 255));
            }

            // Manual Weapon Override Button
            var _wpn_btn_w = 64;
            var _wpn_btn_x = _card_x + _card_w - _wpn_btn_w - 6;
            var _wpn_btn_y = _card_y + 48;
            var _wpnhov = (_mx >= _wpn_btn_x && _mx <= _wpn_btn_x + _wpn_btn_w && _my >= _wpn_btn_y && _my <= _wpn_btn_y + 20);
            if (_wpnhov && _click && array_length(_su.weapons) > 1) {
                if (!variable_struct_exists(_su, "manual_weapon_idx")) _su.manual_weapon_idx = 0;
                _su.manual_weapon_idx = (_su.manual_weapon_idx + 1) % array_length(_su.weapons);
                scr_audio_play_ui("tab");
                add_log("[WEAPON OVERRIDE] " + _su.callsign + " selected: " + _su.weapons[_su.manual_weapon_idx].short_name);
            }
            var _w_name = (variable_struct_exists(_su, "manual_weapon_idx") && _su.manual_weapon_idx >= 0 && _su.manual_weapon_idx < array_length(_su.weapons)) ? string_copy(_su.weapons[_su.manual_weapon_idx].short_name, 1, 6) : "AUTO";
            scr_draw_snes_button(_wpn_btn_x, _wpn_btn_y, _wpn_btn_w, 20, "W:" + _w_name, _wpnhov, variable_struct_exists(_su, "manual_weapon_idx"), make_color_rgb(255, 215, 60));

            // Click card to select unit
            if (_card_hov && _click && !_is_sel && !split_mode_active) {
                for (var u = 0; u < array_length(units); u++) {
                    if (units[u] == _su) {
                        select_unit(u);
                        break;
                    }
                }
            }
        } else {
            // Empty formation slot
            draw_set_color(make_color_rgb(10, 14, 20));
            draw_rectangle(_card_x, _card_y, _card_x + _card_w, _card_y + _card_h, false);
            draw_set_color(make_color_rgb(26, 36, 48));
            draw_rectangle(_card_x, _card_y, _card_x + _card_w, _card_y + _card_h, true);
            draw_set_color(make_color_rgb(60, 80, 105));
            draw_text(_card_x + 90, _card_y + 34, "[EMPTY FORMATION SLOT " + string(s + 1) + "]");
        }
    }
}


// =========================================================================
// 5. BOTTOM COMMAND RIBBON (x: 20 to min(1026, stack_drawer_x - 16), y: 704 to 754)
// =========================================================================
var _act_x = 20;
var _act_y = 704;
var _act_w = min(1010, stack_drawer_x - 36);
var _act_h = 50;

scr_draw_snes_panel(_act_x, _act_y, _act_w, _act_h, "", -1, false, 0.04);

var _cmd_buttons = [
    { label: "[M] MARCH", mode: COMBAT_STATE.MOVE_MODE },
    { label: "[A] ATTACK", mode: COMBAT_STATE.TARGET_MODE },
    { label: "[S] SPLIT", split_toggle: true },
    { label: "[R] REORG", reorg_action: true },
    { label: "[B] BRACE", brace: true },
    { label: "[O] ORBITAL", orbital_strike: true },
    { label: "[SPACE] STANDBY", end_turn: true },
    { label: "[AUTO] SIM", auto_sim: true }
];

var _num_btns = array_length(_cmd_buttons);
var _cb_w = floor((_act_w - 24 - (_num_btns - 1) * 6) / _num_btns);
var _cb_h = 34;

for (var b = 0; b < _num_btns; b++) {
    var _cmd = _cmd_buttons[b];
    var _bx = _act_x + 12 + b * (_cb_w + 6);
    var _by = _act_y + 8;
    var _bhov = (_mx >= _bx && _mx <= _bx + _cb_w && _my >= _by && _my <= _by + _cb_h);

    if (_bhov && _click && state == COMBAT_STATE.PLAYER_PHASE) {
        if (variable_struct_exists(_cmd, "mode")) {
            if (_cmd.mode == COMBAT_STATE.MOVE_MODE) recalculate_moves();
            state = _cmd.mode;
        } else if (variable_struct_exists(_cmd, "split_toggle")) {
            split_mode_active = !split_mode_active;
            scr_audio_play_ui("click");
            add_log("[SPLIT SQUAD] " + (split_mode_active ? "Select units in drawer to peel off." : "Disengaged."));
        } else if (variable_struct_exists(_cmd, "reorg_action")) {
            if (_cur_u != undefined) reorganize_stack(_cur_u.grid_c, _cur_u.grid_r, _cur_u.team);
        } else if (variable_struct_exists(_cmd, "brace")) {
            if (_cur_u != undefined && _cur_u.current_ap >= 2) {
                _cur_u.current_ap -= 2;
                _cur_u.braced = true;
                _cur_u.current_heat = max(0, _cur_u.current_heat - 25);
                add_log("[TACTICAL DEFENSE] " + _cur_u.callsign + " braced! +35% Evasion, -25% Heat vented.");
            }
        } else if (variable_struct_exists(_cmd, "end_turn")) {
            add_log("[TURN END] Initiative passed to hostile battlegroup.");
            state = COMBAT_STATE.AI_PHASE;
            ai_action_timer = 0;
            ai_unit_index = 0;
        } else if (variable_struct_exists(_cmd, "orbital_strike")) {
            var _tx = (target_unit_idx >= 0 && target_unit_idx < array_length(units)) ? units[target_unit_idx].grid_c : 11;
            var _ty = (target_unit_idx >= 0 && target_unit_idx < array_length(units)) ? units[target_unit_idx].grid_r : 11;
            call_flagship_orbital_strike(_tx, _ty);
        } else if (variable_struct_exists(_cmd, "auto_sim")) {
            auto_combat_enabled = !auto_combat_enabled;
            if (auto_combat_enabled) state = COMBAT_STATE.AUTO_SIM;
            add_log("[AUTO-COMBAT] " + (auto_combat_enabled ? "Autonomous Simulation Engaged!" : "Disengaged."));
        }
    }

    var _is_cmd_act = false;
    if (variable_struct_exists(_cmd, "mode") && state == _cmd.mode) _is_cmd_act = true;
    if (variable_struct_exists(_cmd, "split_toggle") && split_mode_active) _is_cmd_act = true;

    scr_draw_snes_button(_bx, _by, _cb_w, _cb_h, _cmd.label, _bhov, _is_cmd_act, _is_cmd_act ? make_color_rgb(0, 240, 140) : make_color_rgb(100, 220, 255));
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

    var _is_prologue_aar = (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "active_combat_context") && !is_undefined(obj_GameManager.active_combat_context) && variable_struct_exists(obj_GameManager.active_combat_context, "is_prologue") && obj_GameManager.active_combat_context.is_prologue);
    draw_set_color(_is_win ? make_color_rgb(80, 255, 120) : make_color_rgb(255, 80, 80));
    if (_is_prologue_aar) {
        draw_text(_mw_x + 30, _mw_y + 24, _is_win ? "== PROLOGUE SORTIE VICTORY // GHA-00 PROTOTYPE SECURES DOCKING BAY ==" : "== AMBUSH OVERWHELMED // PROTOTYPE CRITICAL ==");
    } else {
        draw_text(_mw_x + 30, _mw_y + 24, _is_win ? "== MISSION ACCOMPLISHED // SECTOR SECURED ==" : "== DEFEAT // VANGUARD BATTERY DESTROYED ==");
    }

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
        if (variable_instance_exists(id, "captured_pows") && array_length(captured_pows) > 0) {
            draw_set_color(make_color_rgb(120, 240, 255));
            draw_text(_mw_x + 50, _mw_y + 270, "-> " + string(array_length(captured_pows)) + "x Hostile Ace POWs Secured (Transferred to Flagship Brig)");
        }
    } else {
        draw_set_color(make_color_rgb(255, 80, 80));
        draw_text(_mw_x + 30, _mw_y + 85, "* CATASTROPHIC DEFEAT: Platoon forces overwhelmed in Sector 4.");
        draw_text(_mw_x + 30, _mw_y + 110, "* Emergency orbital med-evac deployed. Casualties admitted to ICU.");
        draw_text(_mw_x + 30, _mw_y + 135, "* PMC Morale reduced by -20 Morale.");
    }

    var _btn_p_w = _is_prologue_aar ? 420 : 300;
    var _btn_p_x = _mw_x + (_mw_w - _btn_p_w) / 2;
    var _btn_p_y = _mw_y + 360;
    var _btn_p_h = 44;
    var _p_hov = (_mx >= _btn_p_x && _mx <= _btn_p_x + _btn_p_w && _my >= _btn_p_y && _my <= _btn_p_y + _btn_p_h);

    if (_p_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            if (_is_prologue_aar) {
                obj_GameManager.has_completed_prologue = true;
                obj_GameManager.has_completed_intro = true;
                obj_GameManager.prologue_active = false;
                obj_GameManager.add_funds(200000);
                obj_GameManager.add_alloy("alloy_vanguard_comp", 4);
                obj_GameManager.add_raw_material("mat_tungsten", 25);
                obj_GameManager.active_combat_context = undefined;
            } else {
                if (variable_instance_exists(obj_GameManager, "active_combat_context") && !is_undefined(obj_GameManager.active_combat_context)) {
                    var _ctx = obj_GameManager.active_combat_context;
                    var _t = scr_territory_get(_ctx.sector_id);
                    if (!is_undefined(_t)) {
                        if (_is_win) {
                            var _prev_fac = _t.controlling_faction;
                            _t.controlling_faction = "pmc";
                            _t.defense_rating = max(45, _t.defense_rating - 20);
                            scr_territory_recalculate_control_percentages();
                            if (instance_exists(obj_FactionManager)) {
                                obj_FactionManager.modify_standing(_prev_fac, -15);
                            }
                        } else {
                            _t.defense_rating = max(15, _t.defense_rating - 5);
                        }
                    }
                    obj_GameManager.last_battle_report = {
                        is_win: _is_win,
                        sector_id: _ctx.sector_id,
                        sector_name: _ctx.sector_name,
                        controlling_faction: _ctx.controlling_faction
                    };
                    obj_GameManager.active_combat_context = undefined;
                }

                // Award Pilot Combat XP & Accumulate Sortie Fatigue (Goal B)
                if (variable_struct_exists(obj_GameManager.facilities, "roster_pilots")) {
                    var _xp_reward = _is_win ? 40 : 15;
                    for (var p = 0; p < array_length(obj_GameManager.facilities.roster_pilots); p++) {
                        var _plt = obj_GameManager.facilities.roster_pilots[p];
                        if (_plt.status == "ACTIVE") {
                            _plt.sorties = (variable_struct_exists(_plt, "sorties") ? _plt.sorties : 0) + 1;
                            _plt.fatigue = min(5, (variable_struct_exists(_plt, "fatigue") ? _plt.fatigue : 0) + 1);
                            obj_GameManager.pilot_add_xp(_plt.id, _xp_reward);
                        }
                    }
                }
                // Pillar 3: Post-Battle Hull Attrition Sync back to Hangar
                if (variable_struct_exists(obj_GameManager, "inventory") && variable_struct_exists(obj_GameManager.inventory, "deployable_mechs")) {
                    var _dmechs = obj_GameManager.inventory.deployable_mechs;
                    for (var u = 0; u < array_length(units); u++) {
                        var _bu = units[u];
                        if (_bu.team == "ALLIED" && variable_struct_exists(_bu, "linked_mech_id")) {
                            var _hp_pct = _bu.is_destroyed ? 0.15 : clamp(_bu.components.torso.cur / max(1, _bu.components.torso.max), 0.15, 1.0);
                            for (var m = 0; m < array_length(_dmechs); m++) {
                                if (is_struct(_dmechs[m]) && variable_struct_exists(_dmechs[m], "id") && _dmechs[m].id == _bu.linked_mech_id) {
                                    _dmechs[m].current_condition_pct = _hp_pct;
                                    _dmechs[m].status = (_hp_pct < 0.99) ? "DAMAGED" : "READY";
                                    break;
                                }
                            }
                        }
                    }
                }
                if (_is_win) {
                    obj_GameManager.add_funds(180000);
                    obj_GameManager.add_alloy("alloy_vanguard_comp", 4);
                    obj_GameManager.add_raw_material("mat_tungsten", 25);
                }
            }
        }
        if (instance_exists(obj_NemesisManager) && variable_instance_exists(id, "captured_pows") && is_array(captured_pows)) {
            for (var k = 0; k < array_length(captured_pows); k++) {
                var _pw = captured_pows[k];
                array_push(obj_NemesisManager.prisoner_list, _pw);
                variable_struct_set(obj_NemesisManager.characters_map, _pw.id, _pw);
            }
        }
        if (room_exists(rm_hq_terminal)) room_goto(rm_hq_terminal);
    }

    draw_set_color(_p_hov ? make_color_rgb(30, 90, 50) : make_color_rgb(18, 50, 30));
    draw_rectangle(_btn_p_x, _btn_p_y, _btn_p_x + _btn_p_w, _btn_p_y + _btn_p_h, false);
    draw_set_color(make_color_rgb(80, 240, 120));
    draw_rectangle(_btn_p_x, _btn_p_y, _btn_p_x + _btn_p_w, _btn_p_y + _btn_p_h, true);
    draw_set_color(c_white);
    var _btn_txt = _is_prologue_aar ? "[>> DOCK WITH HEPHAESTUS // REBOOT TACTICAL CORE >>]" : "[PROCEED TO HQ COMMAND TERMINAL]";
    draw_text(_btn_p_x + 16, _btn_p_y + 12, _btn_txt);
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

    // Direct RTB / Retreat Button from Deployment Deck
    var _rtb_x = _close_x - 145;
    var _rtb_y = _deck_y + 8;
    var _rtb_w = 135;
    var _rtb_h = 28;
    var _rtb_hov = (_mx >= _rtb_x && _mx <= _rtb_x + _rtb_w && _my >= _rtb_y && _my <= _rtb_y + _rtb_h);
    if (_rtb_hov && _click) {
        deployment_deck_active = false;
        if (room_exists(rm_hq_terminal)) {
            room_goto(rm_hq_terminal);
            exit;
        }
    }
    scr_draw_snes_button(_rtb_x, _rtb_y, _rtb_w, _rtb_h, "[RTB: RETREAT]", _rtb_hov, false, make_color_rgb(230, 110, 50));

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
    scr_draw_animated_mobile_suit(_cur_slot_u.mech_type, _cad_cx, _cad_cy, 1.40, (deployment_facing == 0 || deployment_facing == 2) ? 1 : -1, deployment_anim_state, -1, _cur_slot_u.image_blend);

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
    if (variable_struct_exists(_cur_slot_u, "has_affinity_match") && _cur_slot_u.has_affinity_match) {
        draw_set_color(make_color_rgb(255, 215, 80));
        draw_text(_col2_x + 16, _spec_y + 60, "[FRAME AFFINITY: RESONANCE (+8% ACC/EVA, +1 AP)]");
    }
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
    var _map_tab_y = _col3_y + 20;
    for (var t = 0; t < array_length(_filter_tabs); t++) {
        var _ft = _filter_tabs[t];
        var _thov = (_mx >= _cur_tab_x && _mx <= _cur_tab_x + _ft.w && _my >= _map_tab_y && _my <= _map_tab_y + 22);
        var _tsel = (deployment_map_filter == _ft.key);
        if (_thov && _click) {
            deployment_map_filter = _ft.key;
            deployment_map_page = 0;
        }
        scr_draw_snes_button(_cur_tab_x, _map_tab_y, _ft.w, 22, _ft.label, _thov, _tsel, make_color_rgb(100, 220, 255));
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
        draw_text(_col3_x + 10, _my_card + 24, string_copy(_md.theater, 1, 20) + " [" + _md.category + "] | " + string(_md.gravity) + "G");

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
    var _set_tab_y = _my0 + 44;
    var _t1_w = 260;
    var _t1_hov = (_mx >= _mx0 + 24 && _mx <= _mx0 + 24 + _t1_w && _my >= _set_tab_y && _my <= _set_tab_y + 28);
    if (_t1_hov && _click) { settings_active_tab = 0; scr_audio_play_ui("tab"); }
    scr_draw_snes_button(_mx0 + 24, _set_tab_y, _t1_w, 28, "1. AUDIO & MUTE CONTROL", _t1_hov || (settings_active_tab == 0), (settings_active_tab == 0), (settings_active_tab == 0) ? make_color_rgb(0, 240, 255) : c_white);

    var _t2_x = _mx0 + 24 + _t1_w + 12;
    var _t2_w = 260;
    var _t2_hov = (_mx >= _t2_x && _mx <= _t2_x + _t2_w && _my >= _set_tab_y && _my <= _set_tab_y + 28);
    if (_t2_hov && _click) { settings_active_tab = 1; scr_audio_play_ui("tab"); }
    scr_draw_snes_button(_t2_x, _set_tab_y, _t2_w, 28, "2. DISPLAY & SHORTCUTS", _t2_hov || (settings_active_tab == 1), (settings_active_tab == 1), (settings_active_tab == 1) ? make_color_rgb(0, 240, 255) : c_white);

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
            var _bb_hov = (_mx >= _bb_x && _mx <= _bb_x + _sb_w && _my >= _ch2_y + 8 && _my <= _ch2_y + 34);
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


// 10. Tactical Radio Comms Intercom Overlay (Doc 52)
scr_vn_draw_combat_intercom();
