import os

target = "scripts/scr_territory_war_system/scr_territory_war_system.gml"
with open(target, "r", encoding="utf-8") as f:
    code = f.read()

hex_code = '''
/// @function scr_draw_hex_cell(_x, _y, _r, _filled)
/// @description Draws a tactical hex cell or influence polygon in Shin Gihren's Greed style
function scr_draw_hex_cell(_x, _y, _r, _filled) {
    if (is_undefined(_filled)) _filled = true;
    var _p0_x = _x + _r; var _p0_y = _y;
    var _p1_x = _x + _r * 0.5; var _p1_y = _y + _r * 0.866;
    var _p2_x = _x - _r * 0.5; var _p2_y = _y + _r * 0.866;
    var _p3_x = _x - _r; var _p3_y = _y;
    var _p4_x = _x - _r * 0.5; var _p4_y = _y - _r * 0.866;
    var _p5_x = _x + _r * 0.5; var _p5_y = _y - _r * 0.866;
    
    if (_filled) {
        draw_triangle(_x, _y, _p0_x, _p0_y, _p1_x, _p1_y, false);
        draw_triangle(_x, _y, _p1_x, _p1_y, _p2_x, _p2_y, false);
        draw_triangle(_x, _y, _p2_x, _p2_y, _p3_x, _p3_y, false);
        draw_triangle(_x, _y, _p3_x, _p3_y, _p4_x, _p4_y, false);
        draw_triangle(_x, _y, _p4_x, _p4_y, _p5_x, _p5_y, false);
        draw_triangle(_x, _y, _p5_x, _p5_y, _p0_x, _p0_y, false);
    }
    
    draw_line(_p0_x, _p0_y, _p1_x, _p1_y);
    draw_line(_p1_x, _p1_y, _p2_x, _p2_y);
    draw_line(_p2_x, _p2_y, _p3_x, _p3_y);
    draw_line(_p3_x, _p3_y, _p4_x, _p4_y);
    draw_line(_p4_x, _p4_y, _p5_x, _p5_y);
    draw_line(_p5_x, _p5_y, _p0_x, _p0_y);
}
'''

if "scr_draw_hex_cell" not in code:
    code += hex_code
    with open(target, "w", encoding="utf-8") as f:
        f.write(code)
    print("✓ Appended scr_draw_hex_cell to scr_territory_war_system.gml")
else:
    print("✓ scr_draw_hex_cell already present")
