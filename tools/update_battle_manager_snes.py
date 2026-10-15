FILE_PATH = "objects/obj_BattleManager/Draw_64.gml"

with open(FILE_PATH, "r") as f:
    code = f.read()

# 1. Top HUD bar
old_top = """draw_set_color(make_color_rgb(12, 17, 24));
draw_rectangle(0, 0, _gw, 86, false);
draw_set_color(make_color_rgb(32, 54, 82));
draw_rectangle(0, 84, _gw, 86, false);"""

new_top = """scr_draw_snes_panel(0, 0, _gw, 86, "", -1, false, 0.04);"""

assert old_top in code, "Failed to match old_top"
code = code.replace(old_top, new_top)

# 2. Retreat button
old_ret = """draw_set_color(_ab_hov ? make_color_rgb(70, 30, 20) : make_color_rgb(32, 16, 12));
draw_rectangle(_ab_x, _ab_y, _ab_x + _ab_w, _ab_y + _ab_h, false);
draw_set_color(make_color_rgb(220, 90, 50));
draw_rectangle(_ab_x, _ab_y, _ab_x + _ab_w, _ab_y + _ab_h, true);
draw_set_color(c_white);
draw_text(_ab_x + 12, _ab_y + 10, "[ESC: RETREAT HQ]");"""

new_ret = """scr_draw_snes_button(_ab_x, _ab_y, _ab_w, _ab_h, "[ESC: RETREAT HQ]", _ab_hov, false, make_color_rgb(220, 90, 50));"""

assert old_ret in code, "Failed to match old_ret"
code = code.replace(old_ret, new_ret)

# 3. Active Unit Status bar
old_status = """    draw_set_color(make_color_rgb(10, 16, 24));
    draw_rectangle(16, 92, 915, 135, false);
    draw_set_color(make_color_rgb(28, 48, 72));
    draw_rectangle(16, 92, 915, 135, true);"""

new_status = """    scr_draw_snes_panel(16, 92, 899, 43, "", -1, false, 0.03);"""

assert old_status in code, "Failed to match old_status"
code = code.replace(old_status, new_status)

# 4. Heat gauge
old_heat = """    draw_set_color(make_color_rgb(18, 28, 38));
    draw_rectangle(_heat_x, _heat_y + 18, _heat_x + 250, _heat_y + 32, false);
    draw_set_color(_h_col);
    draw_rectangle(_heat_x, _heat_y + 18, _heat_x + (250 * _h_norm), _heat_y + 32, false);
    draw_set_color(make_color_rgb(40, 70, 100));
    draw_rectangle(_heat_x, _heat_y + 18, _heat_x + 250, _heat_y + 32, true);"""

new_heat = """    scr_draw_snes_gauge(_heat_x, _heat_y + 18, 250, 14, _cur_u.current_heat, _cur_u.max_heat, _h_col);"""

assert old_heat in code, "Failed to match old_heat"
code = code.replace(old_heat, new_heat)

# 5. Right Diagnostics Panel
old_diag = """draw_set_color(make_color_rgb(10, 16, 24));
draw_rectangle(_diag_x, _diag_y, _diag_x + _diag_w, _diag_y + _diag_h, false);
draw_set_color(make_color_rgb(38, 64, 96));
draw_rectangle(_diag_x, _diag_y, _diag_x + _diag_w, _diag_y + _diag_h, true);"""

new_diag = """var _is_target = false;
if (_view_u != undefined) _is_target = (_view_u.team == "HOSTILE");
scr_draw_snes_panel(_diag_x, _diag_y, _diag_w, _diag_h, _is_target ? "TARGET DIAGNOSTICS: HOSTILE" : "UNIT STATUS: ALLIED", _is_target ? make_color_rgb(255, 120, 120) : make_color_rgb(100, 220, 255), true, 0.04);"""

assert old_diag in code, "Failed to match old_diag"
code = code.replace(old_diag, new_diag)

# 6. Component Body Part Gauges
old_comp = """        draw_set_color(make_color_rgb(20, 28, 38));
        draw_rectangle(_bx + 235, _by + 2, _bx + 355, _by + 14, false);
        if (_intact) {
            draw_set_color(_col);
            draw_rectangle(_bx + 235, _by + 2, _bx + 235 + (120 * clamp(_cur / _max, 0, 1)), _by + 14, false);
        }"""

new_comp = """        if (_intact) {
            scr_draw_snes_gauge(_bx + 235, _by + 2, 120, 12, _cur, _max, _col);
        } else {
            draw_set_color(make_color_rgb(32, 12, 16));
            draw_rectangle(_bx + 235, _by + 2, _bx + 355, _by + 14, false);
            draw_set_color(c_red);
            draw_text(_bx + 250, _by, "[DESTROYED]");
        }"""

assert old_comp in code, "Failed to match old_comp"
code = code.replace(old_comp, new_comp)

# 7. Command Action Bar
old_cmd_bar = """draw_set_color(make_color_rgb(10, 16, 24));
draw_rectangle(_act_x, _act_y, _act_x + _act_w, _act_y + _act_h, false);
draw_set_color(make_color_rgb(32, 54, 82));
draw_rectangle(_act_x, _act_y, _act_x + _act_w, _act_y + _act_h, true);"""

new_cmd_bar = """scr_draw_snes_panel(_act_x, _act_y, _act_w, _act_h, "TACTICAL COMMAND BUS // MANEUVER & ORDNANCE", make_color_rgb(100, 220, 255), false, 0.04);"""

assert old_cmd_bar in code, "Failed to match old_cmd_bar"
code = code.replace(old_cmd_bar, new_cmd_bar)

# 8. Command Action Buttons
old_cmd_btn = """    draw_set_color(_b_hov ? make_color_rgb(32, 64, 96) : make_color_rgb(16, 26, 38));
    draw_rectangle(_cur_bx, _cur_by, _cur_bx + _b_w, _cur_by + _b_h, false);
    draw_set_color(make_color_rgb(50, 95, 145));
    draw_rectangle(_cur_bx, _cur_by, _cur_bx + _b_w, _cur_by + _b_h, true);

    draw_set_color(c_white);
    draw_text_transformed(_cur_bx + 6, _cur_by + 8, _bd.label, 0.78, 0.78, 0);"""

new_cmd_btn = """    scr_draw_snes_button(_cur_bx, _cur_by, _b_w, _b_h, _bd.label, _b_hov, false, make_color_rgb(100, 220, 255));"""

assert old_cmd_btn in code, "Failed to match old_cmd_btn"
code = code.replace(old_cmd_btn, new_cmd_btn)

with open(FILE_PATH, "w") as f:
    f.write(code)

print("✓ ALL BATTLE MANAGER DRAW_64 SNES UI UPGRADES APPLIED SUCCESSFULLY!")
