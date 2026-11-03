# Patch Draw_0.gml with map overlays: dashed march path, stack badges, and targeting brackets
with open('objects/obj_BattleManager/Draw_0.gml', 'r') as f_in:
    content = f_in.read()

# 1. Add Ground-Level Tactical Vector March Path after tile loop (before section 2)
p_sec2 = content.find('// 2. ISOMETRIC PAINTERS ALGORITHM DEPTH-SORTED ENTITY RENDERING')
assert p_sec2 != -1, 'Section 2 not found'

march_path_code = """// =========================================================================
// 1B. GROUND-LEVEL TACTICAL VECTOR MARCH PATH (Dashed March Route)
// =========================================================================
if (state == COMBAT_STATE.MOVE_MODE && selected_unit_idx >= 0 && selected_unit_idx < array_length(units)) {
    var _cur_sel = units[selected_unit_idx];
    if (hover_c >= 0 && hover_r >= 0 && (hover_c != _cur_sel.grid_c || hover_r != _cur_sel.grid_r)) {
        var _hover_vt = undefined;
        for (var m = 0; m < array_length(valid_move_tiles); m++) {
            if (valid_move_tiles[m].col == hover_c && valid_move_tiles[m].row == hover_r) {
                _hover_vt = valid_move_tiles[m];
                break;
            }
        }

        if (!is_undefined(_hover_vt)) {
            var _sx = iso_to_screen_x(_cur_sel.grid_c, _cur_sel.grid_r, _cur_sel.elev, cam_x, cam_y, zoom);
            var _sy = iso_to_screen_y(_cur_sel.grid_c, _cur_sel.grid_r, _cur_sel.elev, cam_x, cam_y, zoom);
            var _dx = iso_to_screen_x(hover_c, hover_r, grid_elev[hover_c][hover_r], cam_x, cam_y, zoom);
            var _dy = iso_to_screen_y(hover_c, hover_r, grid_elev[hover_c][hover_r], cam_x, cam_y, zoom);

            var _dist_px = point_distance(_sx, _sy, _dx, _dy);
            var _dir_deg = point_direction(_sx, _sy, _dx, _dy);

            // Pulsing Ground Target Diamond
            var _ring_pulse = 0.5 + 0.5 * sin(current_time * 0.012);
            var _rx = (18 + _ring_pulse * 4) * zoom;
            var _ry = (9 + _ring_pulse * 2) * zoom;
            draw_set_color(make_color_rgb(64, 224, 255));
            draw_set_alpha(0.75);
            draw_ellipse(_dx - _rx, _dy - _ry, _dx + _rx, _dy + _ry, true);
            draw_set_alpha(0.35);
            draw_ellipse(_dx - _rx * 0.6, _dy - _ry * 0.6, _dx + _rx * 0.6, _dy + _ry * 0.6, true);
            draw_set_alpha(1.0);

            // Animated Marching Dashed Line Vector
            var _dash_len = 10 * zoom;
            var _gap_len = 6 * zoom;
            var _seg_len = _dash_len + _gap_len;
            var _march_anim = (current_time * 0.035) % _seg_len;

            var _p = _march_anim;
            while (_p < _dist_px) {
                var _x1 = _sx + lengthdir_x(_p, _dir_deg);
                var _y1 = _sy + lengthdir_y(_p, _dir_deg);
                var _x2 = _sx + lengthdir_x(min(_dist_px, _p + _dash_len), _dir_deg);
                var _y2 = _sy + lengthdir_y(min(_dist_px, _p + _dash_len), _dir_deg);

                // Contrast Shadow
                draw_set_color(make_color_rgb(10, 24, 40));
                draw_line_width(_x1, _y1 + 1, _x2, _y2 + 1, 3.5 * zoom);
                // Tactical Cyan Marching Vector
                draw_set_color(make_color_rgb(64, 224, 255));
                draw_line_width(_x1, _y1, _x2, _y2, 2.0 * zoom);

                _p += _seg_len;
            }
        }
    }
}

"""

content = content[:p_sec2] + march_path_code + content[p_sec2:]

# 2. Add Overhead Stack Badges
p_tag = content.find('draw_text_transformed(_vx - 22 * zoom, _by - 12 * zoom, _header_tag, 0.65 * zoom, 0.65 * zoom, 0);')
assert p_tag != -1, 'Header tag not found'
p_tag_end = p_tag + len('draw_text_transformed(_vx - 22 * zoom, _by - 12 * zoom, _header_tag, 0.65 * zoom, 0.65 * zoom, 0);')

stack_badge_code = """

            // Gihren's Greed Stack Overhead Badge [x2]..[x6]
            var _stk = get_stack_at_tile(_u.grid_c, _u.grid_r, _u.team);
            if (array_length(_stk) > 1 && _stk[0] == _u) {
                var _stk_cnt = array_length(_stk);
                var _vg_c = 0;
                var _sp_c = 0;
                for (var si = 0; si < _stk_cnt; si++) {
                    if (_stk[si].formation_slot < 3) _vg_c++; else _sp_c++;
                }

                var _bdg_w = 60.0 * zoom;
                var _bdg_h = 13.0 * zoom;
                var _bdg_y = _by - 27.0 * zoom;

                draw_set_color(make_color_rgb(14, 20, 28));
                draw_rectangle(_vx - _bdg_w * 0.5, _bdg_y, _vx + _bdg_w * 0.5, _bdg_y + _bdg_h, false);

                var _bdg_border = (_u.team == "ALLIED") ? make_color_rgb(64, 224, 255) : make_color_rgb(255, 75, 75);
                draw_set_color(_bdg_border);
                draw_rectangle(_vx - _bdg_w * 0.5, _bdg_y, _vx + _bdg_w * 0.5, _bdg_y + _bdg_h, true);

                draw_set_halign(fa_center);
                var _bdg_txt = "[x" + string(_stk_cnt) + "] VG:" + string(_vg_c) + " SP:" + string(_sp_c);
                draw_set_color(_bdg_border);
                draw_text_transformed(_vx, _bdg_y + 2 * zoom, _bdg_txt, 0.55 * zoom, 0.55 * zoom, 0);
                draw_set_halign(fa_left);
            }"""

content = content[:p_tag_end] + stack_badge_code + content[p_tag_end:]

# 3. Add Floating March Chip & Targeting Brackets after Entity Loop
p_sec8 = content.find('// 8. PROCEDURAL NEMESIS DROP-POD AMBUSH WORLD RENDERING')
assert p_sec8 != -1, 'Section 8 not found'

overlays_code = """// =========================================================================
// 7B. FLOATING MARCH TELEMETRY CHIP & TARGETING BRACKETS
// =========================================================================
if (state == COMBAT_STATE.MOVE_MODE && selected_unit_idx >= 0 && selected_unit_idx < array_length(units)) {
    var _cur_sel = units[selected_unit_idx];
    if (hover_c >= 0 && hover_r >= 0 && (hover_c != _cur_sel.grid_c || hover_r != _cur_sel.grid_r)) {
        var _hover_vt = undefined;
        for (var m = 0; m < array_length(valid_move_tiles); m++) {
            if (valid_move_tiles[m].col == hover_c && valid_move_tiles[m].row == hover_r) {
                _hover_vt = valid_move_tiles[m];
                break;
            }
        }

        if (!is_undefined(_hover_vt)) {
            var _moving_cnt = 0;
            if (split_mode_active) {
                var _keys = variable_struct_get_names(split_selected_units);
                for (var k = 0; k < array_length(_keys); k++) {
                    if (variable_struct_get(split_selected_units, _keys[k])) _moving_cnt++;
                }
                if (_moving_cnt == 0) _moving_cnt = 1;
            } else {
                _moving_cnt = array_length(get_stack_at_tile(_cur_sel.grid_c, _cur_sel.grid_r, _cur_sel.team));
            }

            var _dx = iso_to_screen_x(hover_c, hover_r, grid_elev[hover_c][hover_r], cam_x, cam_y, zoom);
            var _dy = iso_to_screen_y(hover_c, hover_r, grid_elev[hover_c][hover_r], cam_x, cam_y, zoom);
            var _chip_w = 114.0 * zoom;
            var _chip_h = 16.0 * zoom;
            var _chip_y = _dy - (32.0 * zoom);

            draw_set_color(make_color_rgb(14, 22, 32));
            draw_rectangle(_dx - _chip_w * 0.5, _chip_y, _dx + _chip_w * 0.5, _chip_y + _chip_h, false);
            draw_set_color(make_color_rgb(64, 224, 255));
            draw_rectangle(_dx - _chip_w * 0.5, _chip_y, _dx + _chip_w * 0.5, _chip_y + _chip_h, true);
            draw_set_halign(fa_center);
            draw_set_color(make_color_rgb(64, 224, 255));
            draw_text_transformed(_dx, _chip_y + 3 * zoom, "MARCH AP: -" + string(_hover_vt.cost) + " | " + string(_moving_cnt) + " UNIT(S)", 0.55 * zoom, 0.55 * zoom, 0);
            draw_set_halign(fa_left);
        }
    }
}

if (state == COMBAT_STATE.TARGET_MODE && selected_unit_idx >= 0 && selected_unit_idx < array_length(units)) {
    if (hover_c >= 0 && hover_r >= 0) {
        var _tgt_stack = get_stack_at_tile(hover_c, hover_r, "ENEMY");
        if (array_length(_tgt_stack) > 0) {
            var _tgt_u = _tgt_stack[0];
            var _cur_u = units[selected_unit_idx];
            var _d = calculate_distance(_cur_u.grid_c, _cur_u.grid_r, hover_c, hover_r);
            var _friendly_stack = get_stack_at_tile(_cur_u.grid_c, _cur_u.grid_r, _cur_u.team);
            var _fp = get_stack_max_firepower(_friendly_stack, _tgt_u, _d);

            var _tx = iso_to_screen_x(hover_c, hover_r, _tgt_u.elev, cam_x, cam_y, zoom);
            var _ty = iso_to_screen_y(hover_c, hover_r, _tgt_u.elev, cam_x, cam_y, zoom);
            var _cy_mid = _ty - 24 * zoom;

            // 4 Corner Targeting Brackets
            var _bw = 36 * zoom;
            var _bh = 40 * zoom;
            var _b_pulse = sin(current_time * 0.015) * 3 * zoom;
            var _arm = 10 * zoom;

            var _left = _tx - _bw - _b_pulse;
            var _right = _tx + _bw + _b_pulse;
            var _top = _cy_mid - _bh;
            var _bot = _cy_mid + _bh;

            draw_set_color(make_color_rgb(255, 60, 60));
            // Top-Left corner
            draw_line_width(_left, _top, _left + _arm, _top, 2.5 * zoom);
            draw_line_width(_left, _top, _left, _top + _arm, 2.5 * zoom);
            // Top-Right corner
            draw_line_width(_right, _top, _right - _arm, _top, 2.5 * zoom);
            draw_line_width(_right, _top, _right, _top + _arm, 2.5 * zoom);
            // Bottom-Left corner
            draw_line_width(_left, _bot, _left + _arm, _bot, 2.5 * zoom);
            draw_line_width(_left, _bot, _left, _bot - _arm, 2.5 * zoom);
            // Bottom-Right corner
            draw_line_width(_right, _bot, _right - _arm, _bot, 2.5 * zoom);
            draw_line_width(_right, _bot, _right, _bot - _arm, 2.5 * zoom);

            // Center Reticle
            draw_set_color(make_color_rgb(255, 215, 60));
            draw_circle(_tx, _cy_mid, 2.5 * zoom, false);

            // Telemetry Salvo Badge
            var _hdr_str = (_fp.unit_count > 0) ? ("▲ [LOCK] SALVO: " + string(_fp.unit_count) + "/" + string(array_length(_friendly_stack)) + " UNITS") : "▲ [OUT OF RANGE / AP]";
            var _col_hdr = (_fp.unit_count > 0) ? make_color_rgb(255, 215, 60) : make_color_rgb(180, 180, 180);
            var _tw = 110.0 * zoom;
            var _th = 15.0 * zoom;
            var _tb_y = _top - 18 * zoom;

            draw_set_color(make_color_rgb(15, 20, 28));
            draw_rectangle(_tx - _tw * 0.5, _tb_y, _tx + _tw * 0.5, _tb_y + _th, false);
            draw_set_color(_col_hdr);
            draw_rectangle(_tx - _tw * 0.5, _tb_y, _tx + _tw * 0.5, _tb_y + _th, true);
            draw_set_halign(fa_center);
            draw_text_transformed(_tx, _tb_y + 3 * zoom, _hdr_str, 0.55 * zoom, 0.55 * zoom, 0);
            draw_set_halign(fa_left);
        }
    }
}

"""

content = content[:p_sec8] + overlays_code + content[p_sec8:]

with open('objects/obj_BattleManager/Draw_0.gml', 'w') as f_out:
    f_out.write(content)

print('Successfully patched Draw_0.gml')
