with open("objects/obj_HQTerminal/Draw_64.gml", "r") as f:
    code = f.read()

start_marker = '        // Ensure Hex Grid Terrain & Units Initialized for Stronghold'
end_marker = '        // =====================================================================\n        // PASS 4: RIGHT-SIDE TACTICAL HUD & SATELLITE RADAR'

start_idx = code.find(start_marker)
end_idx = code.find(end_marker)

assert start_idx != -1, "start_marker not found in Draw_64.gml"
assert end_idx != -1, "end_marker not found in Draw_64.gml"

new_stronghold_draw = '''        // Ensure Hex Grid Terrain, Units, and Fog of War Initialized for Stronghold
        if (is_undefined(stronghold_terrain_grid) || array_length(stronghold_hex_units) == 0 || is_undefined(stronghold_fog_grid)) {
            stronghold_terrain_grid = scr_hex_get_stronghold_terrain(active_stronghold_id);
            stronghold_hex_units = scr_hex_get_stronghold_units(active_stronghold_id);
            stronghold_fog_grid = scr_hex_init_fog_of_war();
            scr_hex_update_fog_of_war(stronghold_fog_grid, stronghold_hex_units, stronghold_terrain_grid);
            selected_hex_unit_id = "";
            reachable_hexes = {};
        }

        // Top Navigation Bar
        var _ret_x = _rad_x + 18;
        var _ret_y = _rad_y + 32;
        var _ret_w = 160;
        var _ret_h = 26;
        var _ret_hov = (_mx >= _ret_x && _mx <= _ret_x + _ret_w && _my >= _ret_y && _my <= _ret_y + _ret_h);
        if (_ret_hov && _click) {
            earth_view_mode = "GLOBAL";
            scr_audio_play_ui("cancel");
        }
        scr_draw_snes_button(_ret_x, _ret_y, _ret_w, _ret_h, "<< WORLD MAP [ESC]", _ret_hov, false, make_color_rgb(0, 240, 255));

        // Stronghold Title Banner
        var _sb_x = _ret_x + _ret_w + 6;
        var _sb_w = 230;
        draw_set_color(make_color_rgb(10, 16, 26));
        draw_rectangle(_sb_x, _ret_y, _sb_x + _sb_w, _ret_y + _ret_h, false);
        draw_set_color(make_color_rgb(255, 215, 60));
        draw_rectangle(_sb_x, _ret_y, _sb_x + _sb_w, _ret_y + _ret_h, true);
        draw_set_color(make_color_rgb(255, 230, 100));
        draw_text(_sb_x + 8, _ret_y + 5, "★ " + string_upper(_sh_layout.stronghold_name));

        // Hex Grid Toggle Button [G]
        var _grid_btn_x = _sb_x + _sb_w + 6;
        var _grid_btn_w = 105;
        var _gb_hov = (_mx >= _grid_btn_x && _mx <= _grid_btn_x + _grid_btn_w && _my >= _ret_y && _my <= _ret_y + _ret_h);
        if (_gb_hov && _click) {
            hex_grid_enabled = !hex_grid_enabled;
            scr_audio_play_ui("click");
        }
        var _grid_label = hex_grid_enabled ? "GRID: [ON]" : "GRID: [OFF]";
        scr_draw_snes_button(_grid_btn_x, _ret_y, _grid_btn_w, _ret_h, _grid_label, _gb_hov, hex_grid_enabled, make_color_rgb(80, 220, 180));

        // Fog of War Toggle Button [F]
        var _fog_btn_x = _grid_btn_x + _grid_btn_w + 6;
        var _fog_btn_w = 115;
        var _fb_hov = (_mx >= _fog_btn_x && _mx <= _fog_btn_x + _fog_btn_w && _my >= _ret_y && _my <= _ret_y + _ret_h);
        if (_fb_hov && _click) {
            fog_of_war_enabled = !fog_of_war_enabled;
            scr_audio_play_ui("click");
        }
        var _fog_label = fog_of_war_enabled ? "FOG: [ON]" : "FOG: [OFF]";
        scr_draw_snes_button(_fog_btn_x, _ret_y, _fog_btn_w, _ret_h, _fog_label, _fb_hov, fog_of_war_enabled, make_color_rgb(180, 80, 220));

        // Cycle & Tactical Phase Indicator Badge
        var _ph_x = _fog_btn_x + _fog_btn_w + 6;
        var _ph_w = 120;
        draw_set_color(make_color_rgb(14, 22, 34));
        draw_rectangle(_ph_x, _ret_y, _ph_x + _ph_w, _ret_y + _ret_h, false);
        draw_set_color(make_color_rgb(0, 220, 255));
        draw_rectangle(_ph_x, _ret_y, _ph_x + _ph_w, _ret_y + _ret_h, true);
        draw_set_color(c_white);
        draw_text(_ph_x + 8, _ret_y + 5, "CYCLE " + string(hex_tactical_turn) + " // ALLIES");

        // Hover Detection for Hex Grid
        var _hex_pick = scr_screen_to_hex(_mx, _my, _rad_x, _rad_y);
        hovered_hex_c = _hex_pick.col;
        hovered_hex_r = _hex_pick.row;

        // Find Selected Unit
        var _sel_unit = undefined;
        var _sel_unit_idx = -1;
        for (var ui = 0; ui < array_length(stronghold_hex_units); ui++) {
            if (stronghold_hex_units[ui].id == selected_hex_unit_id && stronghold_hex_units[ui].hp > 0) {
                _sel_unit = stronghold_hex_units[ui];
                _sel_unit_idx = ui;
                break;
            }
        }
        if (is_undefined(_sel_unit)) {
            selected_hex_unit_id = "";
            reachable_hexes = {};
        }

        // Unit at Hovered Hex (if any)
        var _hov_unit = undefined;
        if (hovered_hex_c >= 0 && hovered_hex_r >= 0) {
            for (var ui = 0; ui < array_length(stronghold_hex_units); ui++) {
                var _u = stronghold_hex_units[ui];
                if (_u.hp > 0 && _u.col == hovered_hex_c && _u.row == hovered_hex_r) {
                    _hov_unit = _u;
                    break;
                }
            }
        }

        // Visibility of Hovered Hex
        var _hov_vis = 2;
        if (fog_of_war_enabled && !is_undefined(stronghold_fog_grid) && hovered_hex_c >= 0 && hovered_hex_r >= 0) {
            _hov_vis = stronghold_fog_grid[hovered_hex_c][hovered_hex_r];
        }

        // --- MOUSE CLICK INTERACTIONS ---
        if (_click && hovered_hex_c >= 0 && hovered_hex_r >= 0) {
            // Case 1: Clicked a friendly PMC unit -> Select it & compute reachable hexes
            if (!is_undefined(_hov_unit) && _hov_unit.faction == "pmc") {
                selected_hex_unit_id = _hov_unit.id;
                _sel_unit = _hov_unit;
                reachable_hexes = scr_hex_get_reachable(_hov_unit, stronghold_hex_units, stronghold_terrain_grid);
                scr_audio_play_ui("click");
            }
            // Case 2: Clicked an enemy unit while a friendly unit is selected and ready -> Skirmish attack (only if target is visible!)
            else if (!is_undefined(_hov_unit) && _hov_unit.faction != "pmc" && _hov_vis == 2 && !is_undefined(_sel_unit) && _sel_unit.status != "ENGAGED" && _sel_unit.current_mp >= 1) {
                var _dist_to_enemy = scr_hex_distance(_sel_unit.col, _sel_unit.row, hovered_hex_c, hovered_hex_r);
                if (_dist_to_enemy <= _sel_unit.range) {
                    var _terr_def = 10;
                    if (!is_undefined(stronghold_terrain_grid)) {
                        _terr_def = stronghold_terrain_grid[hovered_hex_c][hovered_hex_r].defense_bonus;
                    }
                    var _sk = scr_hex_resolve_skirmish(_sel_unit, _hov_unit, _terr_def);
                    _sel_unit.status = "ENGAGED";
                    _sel_unit.current_mp = 0;
                    reachable_hexes = {};
                    
                    var _sk_msg = "SQUADRON ENGAGE: " + _sel_unit.unit_label + " DEALT " + string(_sk.damage_dealt) + " DMG TO " + _hov_unit.unit_label;
                    if (_sk.defender_destroyed) _sk_msg += " [TARGET ELIMINATED!]";
                    array_push(stronghold_combat_log, _sk_msg);
                    while (array_length(stronghold_combat_log) > 10) array_delete(stronghold_combat_log, 0, 1);
                    scr_audio_play_ui("select");
                }
            }
            // Case 3: Clicked an empty reachable hex -> Move unit and consume MP
            else if (is_undefined(_hov_unit) && !is_undefined(_sel_unit) && _sel_unit.current_mp > 0) {
                var _hkey = string(hovered_hex_c) + "_" + string(hovered_hex_r);
                if (variable_struct_exists(reachable_hexes, _hkey)) {
                    var _move_cost = variable_struct_get(reachable_hexes, _hkey);
                    _sel_unit.col = hovered_hex_c;
                    _sel_unit.row = hovered_hex_r;
                    _sel_unit.current_mp = max(0, _sel_unit.current_mp - _move_cost);
                    if (_sel_unit.current_mp <= 0) _sel_unit.status = "MOVED";
                    reachable_hexes = scr_hex_get_reachable(_sel_unit, stronghold_hex_units, stronghold_terrain_grid);
                    
                    // Update Prometheus Flux Fog of War dynamically on movement!
                    var _spotted = scr_hex_update_fog_of_war(stronghold_fog_grid, stronghold_hex_units, stronghold_terrain_grid);
                    if (array_length(_spotted) > 0) {
                        for (var spi = 0; spi < array_length(_spotted); spi++) {
                            array_push(stronghold_combat_log, "⚡ RADAR LOCK: REVEALED HOSTILE " + _spotted[spi] + "!");
                        }
                    }

                    array_push(stronghold_combat_log, _sel_unit.unit_label + " ADVANCED TO SECTOR [" + string(hovered_hex_c) + "," + string(hovered_hex_r) + "] (MP: " + string(_sel_unit.current_mp) + ")");
                    while (array_length(stronghold_combat_log) > 10) array_delete(stronghold_combat_log, 0, 1);
                    scr_audio_play_ui("select");
                } else {
                    // Clicked out of range -> deselect
                    selected_hex_unit_id = "";
                    reachable_hexes = {};
                }
            }
        }

        // Right-Click deselects
        if (mouse_check_button_pressed(mb_right)) {
            selected_hex_unit_id = "";
            reachable_hexes = {};
        }

        // =====================================================================
        // PASS 1: DRAW 16x10 HEX GRID CELLS, TERRAIN & PROMETHEUS_FLUX FOG OF WAR
        // =====================================================================
        if (hex_grid_enabled) {
            for (var c = 0; c < 16; c++) {
                for (var r = 0; r < 10; r++) {
                    var _pos = scr_hex_get_screen_pos(c, r, _rad_x, _rad_y);
                    var _hx = _pos.x;
                    var _hy = _pos.y;
                    var _cell = stronghold_terrain_grid[c][r];
                    var _vis = 2;
                    if (fog_of_war_enabled && !is_undefined(stronghold_fog_grid)) {
                        _vis = stronghold_fog_grid[c][r];
                    }

                    if (_vis == 0) {
                        // UNEXPLORED PROMETHEUS_FLUX BLACKOUT
                        draw_set_color(make_color_rgb(6, 10, 16));
                        draw_set_alpha(0.88);
                        scr_draw_hex_cell(_hx, _hy, 26, true);
                        draw_set_color(make_color_rgb(20, 32, 48));
                        draw_set_alpha(0.35);
                        scr_draw_hex_cell(_hx, _hy, 26, false);
                        // Subtle Radar Static Dot
                        draw_set_color(make_color_rgb(30, 50, 75));
                        draw_set_alpha(0.4);
                        draw_point(_hx, _hy);
                        draw_set_alpha(1.0);
                    } else {
                        // Terrain Fill and Border Styling (Visible or Explored Fog)
                        var _fill_col = make_color_rgb(18, 30, 48);
                        var _fill_alpha = (_vis == 1) ? 0.18 : 0.26;
                        var _border_col = (_vis == 1) ? make_color_rgb(24, 45, 68) : make_color_rgb(32, 60, 90);

                        if (_cell.terrain_type == "WATER") {
                            _fill_col = make_color_rgb(12, 42, 85);
                            _fill_alpha = (_vis == 1) ? 0.32 : 0.48;
                            _border_col = make_color_rgb(25, 80, 150);
                        } else if (_cell.terrain_type == "FOREST") {
                            _fill_col = make_color_rgb(16, 55, 30);
                            _fill_alpha = (_vis == 1) ? 0.28 : 0.42;
                            _border_col = make_color_rgb(35, 110, 60);
                        } else if (_cell.terrain_type == "MOUNTAIN") {
                            _fill_col = make_color_rgb(52, 48, 62);
                            _fill_alpha = (_vis == 1) ? 0.35 : 0.50;
                            _border_col = make_color_rgb(90, 85, 110);
                        } else if (_cell.terrain_type == "CRATER" || _cell.terrain_type == "ROUGH") {
                            _fill_col = make_color_rgb(70, 32, 28);
                            _fill_alpha = (_vis == 1) ? 0.30 : 0.45;
                            _border_col = make_color_rgb(140, 65, 55);
                        } else if (_cell.terrain_type == "BASE_FACILITY") {
                            _fill_col = make_color_rgb(110, 85, 20);
                            _fill_alpha = 0.45;
                            _border_col = make_color_rgb(255, 215, 60);
                        }

                        // Draw Hex Cell
                        draw_set_color(_fill_col);
                        draw_set_alpha(_fill_alpha);
                        scr_draw_hex_cell(_hx, _hy, 26, true);
                        draw_set_color(_border_col);
                        draw_set_alpha(0.35);
                        scr_draw_hex_cell(_hx, _hy, 26, false);

                        // If in FOG_OF_WAR (1), draw dimming shroud overlay
                        if (_vis == 1) {
                            draw_set_color(make_color_rgb(8, 14, 22));
                            draw_set_alpha(0.55);
                            scr_draw_hex_cell(_hx, _hy, 26, true);
                        }

                        draw_set_alpha(1.0);

                        // Base Facility Icon
                        if (_cell.terrain_type == "BASE_FACILITY") {
                            draw_set_color(make_color_rgb(255, 220, 80));
                            draw_circle(_hx, _hy - 14, 4, false);
                            draw_set_color(make_color_rgb(255, 235, 140));
                            draw_text(_hx - 14, _hy - 24, "BASE");
                        }
                    }
                }
            }

            // Sensor Radar Sweep Rings around Friendly PMC Units
            if (fog_of_war_enabled) {
                for (var ui = 0; ui < array_length(stronghold_hex_units); ui++) {
                    var _fu = stronghold_hex_units[ui];
                    if (_fu.faction == "pmc" && _fu.hp > 0) {
                        var _fpos = scr_hex_get_screen_pos(_fu.col, _fu.row, _rad_x, _rad_y);
                        var _fsr = variable_struct_exists(_fu, "sensor_range") ? _fu.sensor_range : 2;
                        var _s_rad = _fsr * 44;
                        draw_set_color(make_color_rgb(0, 240, 255));
                        draw_set_alpha(0.04 + 0.02 * sin(current_time * 0.005 + ui));
                        draw_circle(_fpos.x, _fpos.y, _s_rad, false);
                        draw_set_alpha(0.32);
                        draw_circle(_fpos.x, _fpos.y, _s_rad, true);
                        draw_set_alpha(1.0);
                    }
                }
            }

            // --- PASS 2: REACHABLE HEXES HIGHLIGHT (DIJKSTRA OVERLAY) ---
            if (!is_undefined(_sel_unit) && _sel_unit.current_mp > 0) {
                var _pulse_a = 0.22 + 0.10 * sin(current_time * 0.008);
                var _r_names = variable_struct_get_names(reachable_hexes);
                for (var ri = 0; ri < array_length(_r_names); ri++) {
                    var _rkey = _r_names[ri];
                    var _under_pos = string_pos("_", _rkey);
                    var _rc = real(string_copy(_rkey, 1, _under_pos - 1));
                    var _rr = real(string_delete(_rkey, 1, _under_pos));

                    var _rpos = scr_hex_get_screen_pos(_rc, _rr, _rad_x, _rad_y);
                    draw_set_color(make_color_rgb(0, 240, 200));
                    draw_set_alpha(_pulse_a);
                    scr_draw_hex_cell(_rpos.x, _rpos.y, 25, true);
                    draw_set_color(make_color_rgb(0, 255, 220));
                    draw_set_alpha(0.75);
                    scr_draw_hex_cell(_rpos.x, _rpos.y, 25, false);
                    draw_set_alpha(1.0);
                }

                // Route Trajectory Line & MP Badge to Hovered Reachable Hex
                if (hovered_hex_c >= 0 && hovered_hex_r >= 0) {
                    var _chk_key = string(hovered_hex_c) + "_" + string(hovered_hex_r);
                    if (variable_struct_exists(reachable_hexes, _chk_key)) {
                        var _cost_val = variable_struct_get(reachable_hexes, _chk_key);
                        var _src_pos = scr_hex_get_screen_pos(_sel_unit.col, _sel_unit.row, _rad_x, _rad_y);
                        var _dst_pos = scr_hex_get_screen_pos(hovered_hex_c, hovered_hex_r, _rad_x, _rad_y);

                        draw_set_color(make_color_rgb(0, 240, 255));
                        draw_line_width(_src_pos.x, _src_pos.y, _dst_pos.x, _dst_pos.y, 2);
                        draw_circle(_dst_pos.x, _dst_pos.y, 5, false);

                        // MP Badge
                        var _badge_w = 46;
                        var _badge_h = 16;
                        draw_set_color(make_color_rgb(10, 16, 26));
                        draw_rectangle(_dst_pos.x - _badge_w/2, _dst_pos.y - 28, _dst_pos.x + _badge_w/2, _dst_pos.y - 28 + _badge_h, false);
                        draw_set_color(make_color_rgb(0, 240, 255));
                        draw_rectangle(_dst_pos.x - _badge_w/2, _dst_pos.y - 28, _dst_pos.x + _badge_w/2, _dst_pos.y - 28 + _badge_h, true);
                        draw_set_color(c_white);
                        draw_text(_dst_pos.x - _badge_w/2 + 4, _dst_pos.y - 27, "-" + string(_cost_val) + " MP");
                    }
                }

                // Attack Target Brackets around in-range Enemies (ONLY IF VISIBLE IN SENSORS!)
                for (var ui = 0; ui < array_length(stronghold_hex_units); ui++) {
                    var _eu = stronghold_hex_units[ui];
                    if (_eu.hp > 0 && _eu.faction != "pmc") {
                        var _eu_vis = (fog_of_war_enabled && !is_undefined(stronghold_fog_grid)) ? stronghold_fog_grid[_eu.col][_eu.row] : 2;
                        if (_eu_vis == 2) {
                            var _edist = scr_hex_distance(_sel_unit.col, _sel_unit.row, _eu.col, _eu.row);
                            if (_edist <= _sel_unit.range) {
                                var _epos = scr_hex_get_screen_pos(_eu.col, _eu.row, _rad_x, _rad_y);
                                var _t_pulse = 22 + 4 * sin(current_time * 0.012);
                                draw_set_color(make_color_rgb(255, 60, 70));
                                draw_circle(_epos.x, _epos.y, _t_pulse, true);
                                draw_text(_epos.x - 22, _epos.y - 28, "[TARGET]");
                            }
                        }
                    }
                }
            }

            // Hover Bracket on Mouse Hex
            if (hovered_hex_c >= 0 && hovered_hex_r >= 0) {
                var _hpos = scr_hex_get_screen_pos(hovered_hex_c, hovered_hex_r, _rad_x, _rad_y);
                draw_set_color(c_white);
                draw_set_alpha(0.65);
                scr_draw_hex_cell(_hpos.x, _hpos.y, 27, false);
                draw_set_alpha(1.0);
            }
        }

        // =====================================================================
        // PASS 3: DRAW TACTICAL UNITS (WITH PROMETHEUS_FLUX SENSOR VISIBILITY)
        // =====================================================================
        for (var ui = 0; ui < array_length(stronghold_hex_units); ui++) {
            var _u = stronghold_hex_units[ui];
            if (_u.hp <= 0) continue;

            var _u_vis = 2;
            if (fog_of_war_enabled && !is_undefined(stronghold_fog_grid) && _u.faction != "pmc") {
                _u_vis = stronghold_fog_grid[_u.col][_u.row];
            }

            // Case A: Enemy is shrouded in deep Prometheus Flux Blackout (0) -> completely invisible!
            if (_u_vis == 0) continue;

            var _upos = scr_hex_get_screen_pos(_u.col, _u.row, _rad_x, _rad_y);
            var _is_u_sel = (selected_hex_unit_id == _u.id);
            var _is_u_hov = (hovered_hex_c == _u.col && hovered_hex_r == _u.row);

            // Case B: Enemy in Explored Fog of War (1) -> draw as Sensor Contact Ghost!
            if (_u_vis == 1) {
                draw_set_color(make_color_rgb(255, 60, 70));
                draw_set_alpha(0.65 + 0.25 * sin(current_time * 0.015 + ui));
                draw_circle(_upos.x, _upos.y, 18, true);
                draw_set_color(make_color_rgb(180, 20, 30));
                draw_circle(_upos.x, _upos.y, 14, false);
                draw_set_color(c_white);
                draw_set_alpha(1.0);
                draw_text(_upos.x - 4, _upos.y - 7, "?");
                draw_set_color(make_color_rgb(255, 140, 140));
                draw_text(_upos.x - 22, _upos.y + 16, "CONTACT");
                continue;
            }

            // Case C: Fully Visible (2) -> Full Shin Gihren's Greed Counter Plinth
            scr_draw_tactical_counter(_upos.x, _upos.y, _u.faction, _u.sprite_name, _u.stack_count, _is_u_sel, _is_u_hov, 0.95);

            // Selection Glowing Plinth Ring
            if (_is_u_sel) {
                draw_set_color(make_color_rgb(0, 240, 255));
                draw_circle(_upos.x, _upos.y + 4, 22 + 2 * sin(current_time * 0.01), true);
            }

            // HP Gauge Bar Underneath Counter
            var _hp_w = 32;
            var _hp_h = 4;
            var _hp_x = _upos.x - _hp_w / 2;
            var _hp_y = _upos.y + 16;
            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_hp_x, _hp_y, _hp_x + _hp_w, _hp_y + _hp_h, false);
            var _hp_pct = clamp(_u.hp / _u.max_hp, 0, 1.0);
            var _hp_col = make_color_rgb(60, 220, 100);
            if (_hp_pct < 0.35) _hp_col = make_color_rgb(255, 60, 60);
            else if (_hp_pct < 0.65) _hp_col = make_color_rgb(255, 200, 40);
            draw_set_color(_hp_col);
            draw_rectangle(_hp_x, _hp_y, _hp_x + floor(_hp_w * _hp_pct), _hp_y + _hp_h, false);
            draw_set_color(make_color_rgb(40, 60, 80));
            draw_rectangle(_hp_x, _hp_y, _hp_x + _hp_w, _hp_y + _hp_h, true);

            // MP Pips Above Counter (for Friendly PMC Units)
            if (_u.faction == "pmc") {
                var _pip_start_x = _upos.x - floor((_u.max_mp * 6) / 2);
                var _pip_y = _upos.y - 18;
                for (var pi = 0; pi < _u.max_mp; pi++) {
                    var _is_pip_ready = (pi < _u.current_mp);
                    draw_set_color(_is_pip_ready ? make_color_rgb(0, 240, 255) : make_color_rgb(40, 60, 80));
                    draw_rectangle(_pip_start_x + pi * 6, _pip_y, _pip_start_x + pi * 6 + 4, _pip_y + 3, false);
                }
            }
        }'''

code = code[:start_idx] + new_stronghold_draw + "\n" + code[end_idx:]

with open("objects/obj_HQTerminal/Draw_64.gml", "w") as f:
    f.write(code)

print("Updated Draw_64.gml with Fog of War successfully!")
