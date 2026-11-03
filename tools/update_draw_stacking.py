with open("objects/obj_HQTerminal/Draw_64.gml", "r") as f:
    code = f.read()

# Replace PASS 3: DRAW TACTICAL UNITS to support multi-unit stack drawing
old_pass3_start = '        // =====================================================================\n        // PASS 3: DRAW TACTICAL UNITS (WITH PROMETHEUS_FLUX SENSOR VISIBILITY)\n        // =====================================================================\n        for (var ui = 0; ui < array_length(stronghold_hex_units); ui++) {'

old_pass3_end = '''            // MP Pips Above Counter (for Friendly PMC Units)
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

start_idx = code.find(old_pass3_start)
end_idx = code.find(old_pass3_end)

assert start_idx != -1, "old_pass3_start not found in Draw_64.gml"
assert end_idx != -1, "old_pass3_end not found in Draw_64.gml"

new_pass3 = '''        // =====================================================================
        // PASS 3: DRAW TACTICAL UNITS & STACKS (Shin Gihren's Greed Battlegroups)
        // =====================================================================
        var _drawn_stacks = {};
        for (var ui = 0; ui < array_length(stronghold_hex_units); ui++) {
            var _lead_u = stronghold_hex_units[ui];
            if (_lead_u.hp <= 0) continue;

            var _skey = string(_lead_u.col) + "_" + string(_lead_u.row);
            if (variable_struct_exists(_drawn_stacks, _skey)) continue;
            _drawn_stacks[$ _skey] = true;

            // Gather all units in this stack
            var _stack_list = [];
            for (var su = 0; su < array_length(stronghold_hex_units); su++) {
                var _cand_u = stronghold_hex_units[su];
                if (_cand_u.hp > 0 && _cand_u.col == _lead_u.col && _cand_u.row == _lead_u.row) {
                    array_push(_stack_list, _cand_u);
                }
            }
            var _stack_size = array_length(_stack_list);

            var _u_vis = 2;
            if (fog_of_war_enabled && !is_undefined(stronghold_fog_grid) && _lead_u.faction != "pmc") {
                _u_vis = stronghold_fog_grid[_lead_u.col][_lead_u.row];
            }

            // Case A: Enemy is shrouded in deep Prometheus Flux Blackout (0) -> completely invisible!
            if (_u_vis == 0) continue;

            var _upos = scr_hex_get_screen_pos(_lead_u.col, _lead_u.row, _rad_x, _rad_y);
            var _is_u_sel = (selected_hex_unit_id == _lead_u.id);
            var _is_u_hov = (hovered_hex_c == _lead_u.col && hovered_hex_r == _lead_u.row);

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

            // Case C: Fully Visible (2) -> Draw Battlegroup Counter
            // If stack > 1, draw isometric depth shadow plinths underneath
            if (_stack_size >= 2) {
                draw_set_color(make_color_rgb(12, 18, 26));
                draw_set_alpha(0.5);
                draw_ellipse(_upos.x - 24, _upos.y - 14, _upos.x + 20, _upos.y + 8, false);
                draw_set_alpha(1.0);
            }
            if (_stack_size >= 3) {
                draw_set_color(make_color_rgb(8, 12, 18));
                draw_set_alpha(0.6);
                draw_ellipse(_upos.x - 26, _upos.y - 18, _upos.x + 18, _upos.y + 4, false);
                draw_set_alpha(1.0);
            }

            // Draw Leading Counter Plinth with stack size badge
            scr_draw_tactical_counter(_upos.x, _upos.y, _lead_u.faction, _lead_u.sprite_name, _stack_size, _is_u_sel, _is_u_hov, 0.95);

            // Selection Glowing Plinth Ring
            if (_is_u_sel) {
                draw_set_color(make_color_rgb(0, 240, 255));
                draw_circle(_upos.x, _upos.y + 4, 22 + 2 * sin(current_time * 0.01), true);
            }

            // HP Gauge Bar Underneath Counter (Frontline unit HP)
            var _hp_w = 32;
            var _hp_h = 4;
            var _hp_x = _upos.x - _hp_w / 2;
            var _hp_y = _upos.y + 16;
            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_hp_x, _hp_y, _hp_x + _hp_w, _hp_y + _hp_h, false);
            var _hp_pct = clamp(_lead_u.hp / _lead_u.max_hp, 0, 1.0);
            var _hp_col = make_color_rgb(60, 220, 100);
            if (_hp_pct < 0.35) _hp_col = make_color_rgb(255, 60, 60);
            else if (_hp_pct < 0.65) _hp_col = make_color_rgb(255, 200, 40);
            draw_set_color(_hp_col);
            draw_rectangle(_hp_x, _hp_y, _hp_x + floor(_hp_w * _hp_pct), _hp_y + _hp_h, false);
            draw_set_color(make_color_rgb(40, 60, 80));
            draw_rectangle(_hp_x, _hp_y, _hp_x + _hp_w, _hp_y + _hp_h, true);

            // MP Pips Above Counter (for Friendly PMC Units)
            if (_lead_u.faction == "pmc") {
                var _pip_start_x = _upos.x - floor((_lead_u.max_mp * 6) / 2);
                var _pip_y = _upos.y - 18;
                for (var pi = 0; pi < _lead_u.max_mp; pi++) {
                    var _is_pip_ready = (pi < _lead_u.current_mp);
                    draw_set_color(_is_pip_ready ? make_color_rgb(0, 240, 255) : make_color_rgb(40, 60, 80));
                    draw_rectangle(_pip_start_x + pi * 6, _pip_y, _pip_start_x + pi * 6 + 4, _pip_y + 3, false);
                }
            }
        }'''

code = code[:start_idx] + new_pass3 + code[end_idx + len(old_pass3_end):]

with open("objects/obj_HQTerminal/Draw_64.gml", "w") as f:
    f.write(code)

print("Updated Draw_64.gml for stack drawing successfully!")
