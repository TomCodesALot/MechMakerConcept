import sys

with open('objects/obj_BattleManager/Draw_64.gml', 'r') as f:
    text = f.read()

start_marker = "// =========================================================================\n// 1. TOP MISSION & PLATOON TIMELINE HUD BAR"
end_marker = "// =========================================================================\n// 6. FLOATING COMBAT TEXT LAYER (GUI SPACE)"

start_pos = text.find(start_marker)
end_pos = text.find(end_marker)

if start_pos == -1 or end_pos == -1:
    print("Error: Could not locate start or end marker in Draw_64.gml")
    print("start_pos:", start_pos, "end_pos:", end_pos)
    sys.exit(1)

new_ui_gml = r'''// =========================================================================
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
    var _fc_h = 135;

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
'''

new_text = text[:start_pos] + new_ui_gml + "\n" + text[end_pos:]

with open('objects/obj_BattleManager/Draw_64.gml', 'w') as f:
    f.write(new_text)

print("Successfully updated Draw_64.gml with Gihren's Greed + Front Mission UI Suite!")
