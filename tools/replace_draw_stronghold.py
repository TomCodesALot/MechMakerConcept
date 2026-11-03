with open("objects/obj_HQTerminal/Draw_64.gml", "r") as f:
    content = f.read()

start_marker = '    if (_region_str == "EARTH" && earth_view_mode == "STRONGHOLD") {'
end_marker = '    } else {\n        // =========================================================================\n        // TIER 1: GLOBAL WORLD OVERVIEW (OR SPACE / MARS THEATERS)'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

print("start_idx:", start_idx, "end_idx:", end_idx)
assert start_idx != -1, "start_marker not found"
assert end_idx != -1, "end_marker not found"

new_code = '''    if (_region_str == "EARTH" && earth_view_mode == "STRONGHOLD") {
        // =========================================================================
        // SHIN GIHREN'S GREED 16x10 HEX TACTICAL OVERLAY & MOVEMENT ENGINE
        // Dedicated Stronghold Base Map with Terrain Costs, MP, and Turn Cycles
        // =========================================================================
        var _sh_layout = scr_stronghold_get_layout(active_stronghold_id);
        var _bg_spr = asset_get_index(_sh_layout.map_sprite_name);
        if (_bg_spr == -1 || !sprite_exists(_bg_spr)) _bg_spr = spr_map_earth_theater;

        if (sprite_exists(_bg_spr)) {
            draw_sprite_stretched_ext(_bg_spr, 0, _rad_x + 12, _rad_y + 26, _rad_w - 24, _rad_h - 38, c_white, 0.76);
        }

        // Radar Scan Coordinates Grid Lines
        draw_set_color(make_color_rgb(18, 30, 46));
        draw_set_alpha(0.5);
        for (var gx = _rad_x + 40; gx < _rad_x + _rad_w - 20; gx += 64) {
            draw_line(gx, _rad_y + 26, gx, _rad_y + _rad_h - 12);
        }
        for (var gy = _rad_y + 40; gy < _rad_y + _rad_h - 12; gy += 48) {
            draw_line(_rad_x + 12, gy, _rad_x + _rad_w - 12, gy);
        }
        draw_set_alpha(1.0);

        // Ensure Hex Grid Terrain & Units Initialized for Stronghold
        if (is_undefined(stronghold_terrain_grid) || array_length(stronghold_hex_units) == 0) {
            stronghold_terrain_grid = scr_hex_get_stronghold_terrain(active_stronghold_id);
            stronghold_hex_units = scr_hex_get_stronghold_units(active_stronghold_id);
            selected_hex_unit_id = "";
            reachable_hexes = {};
        }

        // Top Navigation Bar
        var _ret_x = _rad_x + 18;
        var _ret_y = _rad_y + 32;
        var _ret_w = 175;
        var _ret_h = 26;
        var _ret_hov = (_mx >= _ret_x && _mx <= _ret_x + _ret_w && _my >= _ret_y && _my <= _ret_y + _ret_h);
        if (_ret_hov && _click) {
            earth_view_mode = "GLOBAL";
            scr_audio_play_ui("cancel");
        }
        scr_draw_snes_button(_ret_x, _ret_y, _ret_w, _ret_h, "<< WORLD MAP [ESC]", _ret_hov, false, make_color_rgb(0, 240, 255));

        // Stronghold Title Banner
        var _sb_x = _ret_x + _ret_w + 8;
        var _sb_w = 270;
        draw_set_color(make_color_rgb(10, 16, 26));
        draw_rectangle(_sb_x, _ret_y, _sb_x + _sb_w, _ret_y + _ret_h, false);
        draw_set_color(make_color_rgb(255, 215, 60));
        draw_rectangle(_sb_x, _ret_y, _sb_x + _sb_w, _ret_y + _ret_h, true);
        draw_set_color(make_color_rgb(255, 230, 100));
        draw_text(_sb_x + 8, _ret_y + 5, "★ " + string_upper(_sh_layout.stronghold_name));

        // Hex Grid Toggle Button [G]
        var _grid_btn_x = _sb_x + _sb_w + 8;
        var _grid_btn_w = 125;
        var _gb_hov = (_mx >= _grid_btn_x && _mx <= _grid_btn_x + _grid_btn_w && _my >= _ret_y && _my <= _ret_y + _ret_h);
        if (_gb_hov && _click) {
            hex_grid_enabled = !hex_grid_enabled;
            scr_audio_play_ui("click");
        }
        var _grid_label = hex_grid_enabled ? "HEX GRID: [ON]" : "HEX GRID: [OFF]";
        scr_draw_snes_button(_grid_btn_x, _ret_y, _grid_btn_w, _ret_h, _grid_label, _gb_hov, hex_grid_enabled, make_color_rgb(80, 220, 180));

        // Cycle & Tactical Phase Indicator Badge
        var _ph_x = _grid_btn_x + _grid_btn_w + 8;
        var _ph_w = 130;
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

        // --- MOUSE CLICK INTERACTIONS ---
        if (_click && hovered_hex_c >= 0 && hovered_hex_r >= 0) {
            // Case 1: Clicked a friendly PMC unit -> Select it & compute reachable hexes
            if (!is_undefined(_hov_unit) && _hov_unit.faction == "pmc") {
                selected_hex_unit_id = _hov_unit.id;
                _sel_unit = _hov_unit;
                reachable_hexes = scr_hex_get_reachable(_hov_unit, stronghold_hex_units, stronghold_terrain_grid);
                scr_audio_play_ui("click");
            }
            // Case 2: Clicked an enemy unit while a friendly unit is selected and ready -> Skirmish attack
            else if (!is_undefined(_hov_unit) && _hov_unit.faction != "pmc" && !is_undefined(_sel_unit) && _sel_unit.status != "ENGAGED" && _sel_unit.current_mp >= 1) {
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
        // PASS 1: DRAW 16x10 HEX GRID CELLS & TERRAIN (Shin Gihren's Greed)
        // =====================================================================
        if (hex_grid_enabled) {
            for (var c = 0; c < 16; c++) {
                for (var r = 0; r < 10; r++) {
                    var _pos = scr_hex_get_screen_pos(c, r, _rad_x, _rad_y);
                    var _hx = _pos.x;
                    var _hy = _pos.y;
                    var _cell = stronghold_terrain_grid[c][r];

                    // Terrain Fill and Border Styling
                    var _fill_col = make_color_rgb(18, 30, 48);
                    var _fill_alpha = 0.22;
                    var _border_col = make_color_rgb(32, 60, 90);

                    if (_cell.terrain_type == "WATER") {
                        _fill_col = make_color_rgb(12, 42, 85);
                        _fill_alpha = 0.45;
                        _border_col = make_color_rgb(25, 80, 150);
                    } else if (_cell.terrain_type == "FOREST") {
                        _fill_col = make_color_rgb(16, 55, 30);
                        _fill_alpha = 0.40;
                        _border_col = make_color_rgb(35, 110, 60);
                    } else if (_cell.terrain_type == "MOUNTAIN") {
                        _fill_col = make_color_rgb(52, 48, 62);
                        _fill_alpha = 0.48;
                        _border_col = make_color_rgb(90, 85, 110);
                    } else if (_cell.terrain_type == "CRATER" || _cell.terrain_type == "ROUGH") {
                        _fill_col = make_color_rgb(70, 32, 28);
                        _fill_alpha = 0.42;
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

                // Attack Target Brackets around in-range Enemies
                for (var ui = 0; ui < array_length(stronghold_hex_units); ui++) {
                    var _eu = stronghold_hex_units[ui];
                    if (_eu.hp > 0 && _eu.faction != "pmc") {
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
        // PASS 3: DRAW TACTICAL UNITS (Shin Gihren's Greed Counters)
        // =====================================================================
        for (var ui = 0; ui < array_length(stronghold_hex_units); ui++) {
            var _u = stronghold_hex_units[ui];
            if (_u.hp <= 0) continue;

            var _upos = scr_hex_get_screen_pos(_u.col, _u.row, _rad_x, _rad_y);
            var _is_u_sel = (selected_hex_unit_id == _u.id);
            var _is_u_hov = (hovered_hex_c == _u.col && hovered_hex_r == _u.row);

            // Draw Counter Plinth + Miniature Sprite + Stack Count
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
        }

        // =====================================================================
        // PASS 4: RIGHT-SIDE TACTICAL HUD & SATELLITE RADAR
        // =====================================================================
        var _hud_w = 216;
        var _hud_x = _rad_x + _rad_w - _hud_w - 16;

        // Top-Right Satellite Minimap Box
        var _mm_h = 112;
        var _mm_y = _rad_y + 32;
        draw_set_color(make_color_rgb(8, 14, 22));
        draw_rectangle(_hud_x, _mm_y, _hud_x + _hud_w, _mm_y + _mm_h, false);
        draw_set_color(make_color_rgb(45, 80, 125));
        draw_rectangle(_hud_x, _mm_y, _hud_x + _hud_w, _mm_y + _mm_h, true);

        if (_sh_layout.region == "MARS" && sprite_exists(spr_map_mars_theater)) {
            draw_sprite_stretched_ext(spr_map_mars_theater, 0, _hud_x + 2, _mm_y + 2, _hud_w - 4, _mm_h - 4, c_white, 0.85);
            draw_set_color(make_color_rgb(255, 90, 80));
            draw_text(_hud_x + 8, _mm_y + 6, "THARSIS ORBIT TELEMETRY");
        } else if (sprite_exists(spr_radar_earth_amber)) {
            draw_sprite_stretched_ext(spr_radar_earth_amber, 0, _hud_x + 2, _mm_y + 2, _hud_w - 4, _mm_h - 4, c_white, 0.85);
            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_hud_x + 8, _mm_y + 6, "TERRESTRIAL SATELLITE");
        }

        var _mb = _sh_layout.minimap_box;
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_rectangle(_hud_x + _mb.x, _mm_y + _mb.y, _hud_x + _mb.x + _mb.w, _mm_y + _mb.y + _mb.h, true);
        draw_rectangle(_hud_x + _mb.x - 1, _mm_y + _mb.y - 1, _hud_x + _mb.x + _mb.w + 1, _mm_y + _mb.y + _mb.h + 1, true);

        // Middle: Tactical Unit & Hex Inspector Panel
        var _insp_y = _mm_y + _mm_h + 8;
        var _insp_h = 230;
        draw_set_color(make_color_rgb(12, 18, 28));
        draw_rectangle(_hud_x, _insp_y, _hud_x + _hud_w, _insp_y + _insp_h, false);
        draw_set_color(make_color_rgb(45, 85, 130));
        draw_rectangle(_hud_x, _insp_y, _hud_x + _hud_w, _insp_y + _insp_h, true);

        draw_set_color(make_color_rgb(20, 32, 50));
        draw_rectangle(_hud_x + 2, _insp_y + 2, _hud_x + _hud_w - 2, _insp_y + 22, false);
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_hud_x + 8, _insp_y + 5, "TACTICAL SQUADRON INSPECTOR");

        if (!is_undefined(_sel_unit)) {
            // Selected Unit Profile
            draw_set_color(c_white);
            draw_text(_hud_x + 8, _insp_y + 28, string_copy(_sel_unit.name, 1, 20));
            draw_set_color(make_color_rgb(255, 215, 60));
            draw_text(_hud_x + 8, _insp_y + 44, _sel_unit.unit_label);

            // Faction Banner
            var _fac_title = (_sel_unit.faction == "pmc") ? "PMC VANGUARD [ALLIED]" : "OPFOR GARRISON";
            draw_set_color((_sel_unit.faction == "pmc") ? make_color_rgb(0, 220, 255) : make_color_rgb(255, 90, 80));
            draw_text(_hud_x + 8, _insp_y + 60, _fac_title);

            // HP Bar
            draw_set_color(make_color_rgb(180, 210, 240));
            draw_text(_hud_x + 8, _insp_y + 78, "HULL INTEGRITY:");
            draw_set_color(make_color_rgb(60, 220, 100));
            draw_text(_hud_x + _hud_w - 60, _insp_y + 78, string(_sel_unit.hp) + "/" + string(_sel_unit.max_hp));

            var _ibar_w = _hud_w - 16;
            draw_set_color(make_color_rgb(20, 30, 42));
            draw_rectangle(_hud_x + 8, _insp_y + 94, _hud_x + 8 + _ibar_w, _insp_y + 101, false);
            draw_set_color(make_color_rgb(60, 220, 100));
            draw_rectangle(_hud_x + 8, _insp_y + 94, _hud_x + 8 + floor(_ibar_w * (_sel_unit.hp / _sel_unit.max_hp)), _insp_y + 101, false);

            // MP Bar
            draw_set_color(make_color_rgb(180, 210, 240));
            draw_text(_hud_x + 8, _insp_y + 106, "MOBILITY POINTS:");
            draw_set_color(make_color_rgb(0, 220, 255));
            draw_text(_hud_x + _hud_w - 60, _insp_y + 106, string(_sel_unit.current_mp) + "/" + string(_sel_unit.max_mp) + " MP");

            draw_set_color(make_color_rgb(20, 30, 42));
            draw_rectangle(_hud_x + 8, _insp_y + 122, _hud_x + 8 + _ibar_w, _insp_y + 129, false);
            draw_set_color(make_color_rgb(0, 220, 255));
            draw_rectangle(_hud_x + 8, _insp_y + 122, _hud_x + 8 + floor(_ibar_w * (_sel_unit.current_mp / _sel_unit.max_mp)), _insp_y + 129, false);

            // Combat Power Stats
            draw_set_color(make_color_rgb(220, 230, 245));
            draw_text(_hud_x + 8, _insp_y + 138, "ATK: " + string(_sel_unit.attack) + "  DEF: " + string(_sel_unit.defense) + "  RNG: " + string(_sel_unit.range) + " HEX");

            // Status Badge
            var _st_col = (_sel_unit.status == "READY") ? make_color_rgb(80, 255, 140) : make_color_rgb(180, 190, 205);
            draw_set_color(_st_col);
            draw_text(_hud_x + 8, _insp_y + 154, "STATUS: [" + _sel_unit.status + "]");

            // Hex Sector & Terrain Coordinates
            var _cur_terr = stronghold_terrain_grid[_sel_unit.col][_sel_unit.row];
            draw_set_color(make_color_rgb(160, 190, 220));
            draw_text(_hud_x + 8, _insp_y + 174, "SECTOR [" + string(_sel_unit.col) + "," + string(_sel_unit.row) + "]: " + _cur_terr.name);
            draw_set_color(make_color_rgb(255, 215, 60));
            draw_text(_hud_x + 8, _insp_y + 192, "TERRAIN DEFENSE BONUS: +" + string(_cur_terr.defense_bonus) + " %");
            draw_set_color(make_color_rgb(140, 180, 220));
            draw_text(_hud_x + 8, _insp_y + 210, "CLICK GREEN HEX TO MOVE / ENEMY TO FIRE");
        } else if (hovered_hex_c >= 0 && hovered_hex_r >= 0) {
            // Hovered Sector Telemetry
            var _ht = stronghold_terrain_grid[hovered_hex_c][hovered_hex_r];
            draw_set_color(c_white);
            draw_text(_hud_x + 8, _insp_y + 28, "GRID SECTOR [" + string(hovered_hex_c) + "," + string(hovered_hex_r) + "]");
            draw_set_color(make_color_rgb(255, 215, 60));
            draw_text(_hud_x + 8, _insp_y + 46, "TERRAIN: " + string_upper(_ht.name));

            draw_set_color(make_color_rgb(180, 210, 240));
            draw_text(_hud_x + 8, _insp_y + 70, "DEFENSE COVER:");
            draw_set_color(make_color_rgb(80, 240, 120));
            draw_text(_hud_x + _hud_w - 55, _insp_y + 70, "+" + string(_ht.defense_bonus) + " %");

            draw_set_color(make_color_rgb(180, 210, 240));
            draw_text(_hud_x + 8, _insp_y + 90, "MOVEMENT COST:");
            draw_set_color(make_color_rgb(0, 220, 255));
            draw_text(_hud_x + _hud_w - 55, _insp_y + 90, string(_ht.mp_cost) + " MP");

            if (_ht.terrain_type == "BASE_FACILITY") {
                draw_set_color(make_color_rgb(255, 220, 80));
                draw_text(_hud_x + 8, _insp_y + 115, "★ FORTIFIED FACILITY REDOUBT");
                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text(_hud_x + 8, _insp_y + 133, "FACILITY: " + string_copy(_ht.name, 1, 18));
            } else {
                draw_set_color(make_color_rgb(140, 175, 210));
                draw_text(_hud_x + 8, _insp_y + 115, "Standard tactical movement sector.");
            }

            draw_set_color(make_color_rgb(200, 220, 240));
            draw_text(_hud_x + 8, _insp_y + 160, "SELECT ALLIED SQUADRON");
            draw_text(_hud_x + 8, _insp_y + 178, "TO REVEAL MOVEMENT RANGE");
        } else {
            draw_set_color(make_color_rgb(200, 220, 240));
            draw_text(_hud_x + 8, _insp_y + 35, "★ SHIN GIHREN'S GREED ENGINE");
            draw_set_color(make_color_rgb(140, 175, 210));
            draw_text_ext(_hud_x + 8, _insp_y + 58, "16x10 Hex Tactical Grid active. Select an allied Mobile Suit or Armor unit to deploy movement range and engage hostile defense positions.", 15, _hud_w - 16);
        }

        // Bottom Area: Skirmish Combat Log Box
        var _log_y = _insp_y + _insp_h + 8;
        var _log_h = 70;
        draw_set_color(make_color_rgb(8, 12, 18));
        draw_rectangle(_hud_x, _log_y, _hud_x + _hud_w, _log_y + _log_h, false);
        draw_set_color(make_color_rgb(35, 60, 95));
        draw_rectangle(_hud_x, _log_y, _hud_x + _hud_w, _log_y + _log_h, true);

        draw_set_color(make_color_rgb(255, 215, 60));
        draw_text(_hud_x + 6, _log_y + 4, "COMBAT TELEMETRY LOG:");

        var _log_start = max(0, array_length(stronghold_combat_log) - 3);
        var _ly = _log_y + 20;
        for (var li = _log_start; li < array_length(stronghold_combat_log); li++) {
            draw_set_color(make_color_rgb(170, 205, 240));
            draw_text(_hud_x + 6, _ly, string_copy(stronghold_combat_log[li], 1, 28));
            _ly += 15;
        }

        // Action Buttons: [⏩ END TURN / CYCLE]
        var _et_y = _log_y + _log_h + 8;
        var _et_h = 32;
        var _et_hov = (_mx >= _hud_x && _mx <= _hud_x + _hud_w && _my >= _et_y && _my <= _et_y + _et_h);
        if (_et_hov && _click) {
            var _new_log = scr_stronghold_advance_turn(active_stronghold_id, stronghold_hex_units, stronghold_terrain_grid, hex_tactical_turn);
            for (var li = 0; li < array_length(_new_log); li++) {
                array_push(stronghold_combat_log, _new_log[li]);
            }
            while (array_length(stronghold_combat_log) > 10) array_delete(stronghold_combat_log, 0, 1);
            hex_tactical_turn++;
            selected_hex_unit_id = "";
            reachable_hexes = {};
            scr_audio_play_ui("confirm");
        }
        scr_draw_snes_button(_hud_x, _et_y, _hud_w, _et_h, "⏩ ADVANCE CYCLE [SPACE]", _et_hov, false, make_color_rgb(255, 215, 60));

        // Direct Combat Simulation Sortie Button
        var _sort_y = _et_y + _et_h + 6;
        var _sort_h = 28;
        var _sort_hov = (_mx >= _hud_x && _mx <= _hud_x + _hud_w && _my >= _sort_y && _my <= _sort_y + _sort_h);
        if (_sort_hov && _click && room_exists(rm_combat)) {
            if (instance_exists(obj_GameManager)) {
                obj_GameManager.active_combat_context = {
                    sector_id: active_stronghold_id,
                    sector_name: _sh_layout.stronghold_name,
                    region: _sh_layout.region,
                    subregion: "Stronghold Hex Theater",
                    controlling_faction: "faction_b",
                    defense_rating: 85,
                    garrison_unit: "OPFOR Defense Garrison",
                    is_invasion: true,
                    origin_base_id: active_stronghold_id
                };
            }
            scr_audio_play_ui("confirm");
            room_goto(rm_combat);
        }
        scr_draw_snes_button(_hud_x, _sort_y, _hud_w, _sort_h, "⚡ ENTER COMBAT SIM", _sort_hov, false, make_color_rgb(255, 80, 80));
    }'''

updated_content = content[:start_idx] + new_code + "\n" + content[end_idx:]
with open("objects/obj_HQTerminal/Draw_64.gml", "w") as f:
    f.write(updated_content)

print("Successfully replaced stronghold drawing code in Draw_64.gml!")
