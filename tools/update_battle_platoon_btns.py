FILE_PATH = "objects/obj_BattleManager/Draw_64.gml"
with open(FILE_PATH, "r") as f:
    code = f.read()

target = """    var _is_sel = (selected_unit_idx == u);
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
    }"""

replacement = """    var _is_sel = (selected_unit_idx == u);
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
    }"""

assert target in code, "Failed to match target in BattleManager Draw_64"
code = code.replace(target, replacement)
with open(FILE_PATH, "w") as f:
    f.write(code)

print("✓ Updated BattleManager platoon roster buttons to SNES tactile push buttons!")
