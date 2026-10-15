FILE_PATH = "objects/obj_MobileSuit/Draw_0.gml"
with open(FILE_PATH, "r") as f:
    code = f.read()

old_hud = """// 6. Front Mission Component Health Display
var _hud_x = 40;
var _hud_y = 35;

draw_set_color(c_dkgray);
draw_rectangle(_hud_x - 10, _hud_y - 10, _hud_x + 380, _hud_y + 245, false);
draw_set_color(c_white);
draw_rectangle(_hud_x - 10, _hud_y - 10, _hud_x + 380, _hud_y + 245, true);

draw_text(_hud_x, _hud_y, "=== MOBILE SUIT INTEGRITY ===");"""

new_hud = """// 6. Front Mission Component Health Display
var _hud_x = 40;
var _hud_y = 35;

scr_draw_snes_panel(_hud_x - 10, _hud_y - 10, 390, 255, "MOBILE SUIT INTEGRITY", make_color_rgb(100, 220, 255), true, 0.04);"""

assert old_hud in code, "Failed to match old_hud in obj_MobileSuit/Draw_0.gml"
code = code.replace(old_hud, new_hud)

old_part = """    draw_set_color(c_black);
    draw_rectangle(_px + 230, _py + 2, _px + 350, _py + 12, false);
    if (_intact) {
        draw_set_color(_col);
        draw_rectangle(_px + 230, _py + 2, _px + 230 + (120 * _pct), _py + 12, false);
    }"""

new_part = """    if (_intact) {
        scr_draw_snes_gauge(_px + 230, _py + 2, 120, 10, _cur, max(1, _max), _col);
    } else {
        draw_set_color(make_color_rgb(25, 10, 12));
        draw_rectangle(_px + 230, _py + 2, _px + 350, _py + 12, false);
        draw_set_color(c_red);
        draw_text(_px + 240, _py, "[SEVERED]");
    }"""

assert old_part in code, "Failed to match old_part in obj_MobileSuit/Draw_0.gml"
code = code.replace(old_part, new_part)

old_legend = """// Controls Helper Legend
var _leg_x = 40;
var _leg_y = 510;
draw_set_color(c_black);
draw_rectangle(_leg_x - 10, _leg_y - 10, _leg_x + 720, _leg_y + 160, false);
draw_set_color(c_lime);
draw_rectangle(_leg_x - 10, _leg_y - 10, _leg_x + 720, _leg_y + 160, true);

draw_set_color(c_white);
draw_text(_leg_x, _leg_y, "DEBUG RECOIL, MELEE & LIMB CONTROLS:");"""

new_legend = """// Controls Helper Legend
var _leg_x = 40;
var _leg_y = 510;
scr_draw_snes_panel(_leg_x - 10, _leg_y - 10, 730, 170, "DEBUG RECOIL, MELEE & LIMB CONTROLS", make_color_rgb(60, 240, 120), false, 0.04);"""

assert old_legend in code, "Failed to match old_legend in obj_MobileSuit/Draw_0.gml"
code = code.replace(old_legend, new_legend)

with open(FILE_PATH, "w") as f:
    f.write(code)

print("✓ Successfully updated obj_MobileSuit/Draw_0.gml to 16-bit SNES UI!")
