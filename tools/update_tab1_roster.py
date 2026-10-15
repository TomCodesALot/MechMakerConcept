FILE_PATH = 'objects/obj_HQTerminal/Draw_64.gml'
with open(FILE_PATH, 'r') as f:
    code = f.read()

target = """        var _col2_x = _f_x + _col1_w + 30;
        var _col2_w = _pan_w - _col1_w - 70;

        draw_set_color(make_color_rgb(10, 16, 24));
        draw_rectangle(_col2_x, _f_y + 24, _col2_x + _col2_w, _f_y + 580, false);
        draw_set_color(make_color_rgb(35, 60, 90));
        draw_rectangle(_col2_x, _f_y + 24, _col2_x + _col2_w, _f_y + 580, true);"""

replacement = """        var _col2_x = _f_x + _col1_w + 30;
        var _col2_w = _pan_w - _col1_w - 70;

        scr_draw_snes_panel(_col2_x, _f_y + 24, _col2_w, 556, "ACTIVE PERSONNEL & PILOT ROSTER", make_color_rgb(255, 195, 60), false, 0.04);"""

assert target in code, 'Failed to match target'
code = code.replace(target, replacement)
with open(FILE_PATH, 'w') as f:
    f.write(code)
print('✓ Successfully updated Tab 1 roster panel to 16-bit SNES panel!')
