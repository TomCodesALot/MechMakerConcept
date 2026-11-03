with open("objects/obj_HQTerminal/Draw_64.gml", "r") as f:
    code = f.read()

old_block = '''        } else if (hovered_hex_c >= 0 && hovered_hex_r >= 0) {
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
        } else {'''

new_block = '''        } else if (hovered_hex_c >= 0 && hovered_hex_r >= 0) {
            if (_hov_vis == 0) {
                // UNEXPLORED PROMETHEUS_FLUX BLACKOUT TELEMETRY
                draw_set_color(make_color_rgb(255, 90, 80));
                draw_text(_hud_x + 8, _insp_y + 28, "SECTOR [" + string(hovered_hex_c) + "," + string(hovered_hex_r) + "]: BLACKOUT");
                draw_set_color(make_color_rgb(255, 215, 60));
                draw_text(_hud_x + 8, _insp_y + 46, "TERRAIN: ??? PROMETHEUS_FLUX HAZE ???");

                draw_set_color(make_color_rgb(180, 210, 240));
                draw_text(_hud_x + 8, _insp_y + 70, "RADAR MASKING:");
                draw_set_color(make_color_rgb(255, 60, 70));
                draw_text(_hud_x + _hud_w - 55, _insp_y + 70, "98 %");

                draw_set_color(make_color_rgb(180, 210, 240));
                draw_text(_hud_x + 8, _insp_y + 90, "SENSOR SIGNAL:");
                draw_set_color(make_color_rgb(255, 90, 80));
                draw_text(_hud_x + _hud_w - 55, _insp_y + 90, "BLIND");

                draw_set_color(make_color_rgb(200, 220, 240));
                draw_text(_hud_x + 8, _insp_y + 118, "UNEXPLORED COMBAT SECTOR");
                draw_set_color(make_color_rgb(140, 180, 220));
                draw_text_ext(_hud_x + 8, _insp_y + 138, "Dense Prometheus Flux scattering obscures hostile signatures. Dispatch a high-sensor Scout Technical (Sensor 4) or Aero-Striker to illuminate sector.", 14, _hud_w - 16);
            } else {
                // Hovered Sector Telemetry (Explored Fog or Visible)
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
                    draw_text(_hud_x + 8, _insp_y + 115, (_hov_vis == 1) ? "Explored sector under radar fog." : "Actively illuminated by sensors.");
                }

                draw_set_color(make_color_rgb(200, 220, 240));
                draw_text(_hud_x + 8, _insp_y + 160, "SELECT ALLIED SQUADRON");
                draw_text(_hud_x + 8, _insp_y + 178, "TO REVEAL MOVEMENT RANGE");
            }
        } else {'''

assert old_block in code, "old_block not found in Draw_64.gml"
code = code.replace(old_block, new_block)

# Also update the Advance Cycle button handler to call scr_hex_update_fog_of_war
old_btn = '''        if (_et_hov && _click) {
            var _new_log = scr_stronghold_advance_turn(active_stronghold_id, stronghold_hex_units, stronghold_terrain_grid, hex_tactical_turn);
            for (var li = 0; li < array_length(_new_log); li++) {
                array_push(stronghold_combat_log, _new_log[li]);
            }
            while (array_length(stronghold_combat_log) > 10) array_delete(stronghold_combat_log, 0, 1);
            hex_tactical_turn++;
            selected_hex_unit_id = "";
            reachable_hexes = {};
            scr_audio_play_ui("confirm");
        }'''

new_btn = '''        if (_et_hov && _click) {
            var _new_log = scr_stronghold_advance_turn(active_stronghold_id, stronghold_hex_units, stronghold_terrain_grid, hex_tactical_turn);
            for (var li = 0; li < array_length(_new_log); li++) {
                array_push(stronghold_combat_log, _new_log[li]);
            }
            while (array_length(stronghold_combat_log) > 10) array_delete(stronghold_combat_log, 0, 1);
            hex_tactical_turn++;
            selected_hex_unit_id = "";
            reachable_hexes = {};
            scr_hex_update_fog_of_war(stronghold_fog_grid, stronghold_hex_units, stronghold_terrain_grid);
            scr_audio_play_ui("confirm");
        }'''

assert old_btn in code, "old_btn not found in Draw_64.gml"
code = code.replace(old_btn, new_btn)

with open("objects/obj_HQTerminal/Draw_64.gml", "w") as f:
    f.write(code)

print("Updated inspector and turn advance fog logic in Draw_64.gml successfully!")
