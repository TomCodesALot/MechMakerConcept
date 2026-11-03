with open("objects/obj_HQTerminal/Draw_64.gml", "r") as f:
    code = f.read()

# 1. Replace base facility hex icon
old_icon = '''                        // Base Facility Icon
                        if (_cell.terrain_type == "BASE_FACILITY") {
                            draw_set_color(make_color_rgb(255, 220, 80));
                            draw_circle(_hx, _hy - 14, 4, false);
                            draw_set_color(make_color_rgb(255, 235, 140));
                            draw_text(_hx - 14, _hy - 24, "BASE");
                        }'''

new_icon = '''                        // Base Facility Icon & Capture Gauges
                        if (_cell.terrain_type == "BASE_FACILITY") {
                            var _is_pmc = (_cell.controlling_faction == "pmc");
                            draw_set_color(_is_pmc ? make_color_rgb(255, 220, 80) : make_color_rgb(255, 80, 70));
                            draw_circle(_hx, _hy - 14, 4, false);
                            draw_set_color(_is_pmc ? make_color_rgb(255, 235, 140) : make_color_rgb(255, 160, 160));
                            draw_text(_hx - 14, _hy - 24, _is_pmc ? "PMC" : "BASE");

                            // Dynamic Capture Progress Gauge
                            var _cprog = variable_struct_exists(_cell, "capture_progress") ? _cell.capture_progress : 0;
                            if (_cprog > 0 && _cprog < 100) {
                                var _cbar_w = 32;
                                var _cbar_h = 4;
                                var _cbar_x = _hx - _cbar_w/2;
                                var _cbar_y = _hy + 18;
                                draw_set_color(make_color_rgb(10, 16, 24));
                                draw_rectangle(_cbar_x, _cbar_y, _cbar_x + _cbar_w, _cbar_y + _cbar_h, false);
                                draw_set_color(make_color_rgb(255, 215, 60));
                                draw_rectangle(_cbar_x, _cbar_y, _cbar_x + floor(_cbar_w * (_cprog / 100.0)), _cbar_y + _cbar_h, false);
                                draw_set_color(make_color_rgb(0, 240, 255));
                                draw_rectangle(_cbar_x, _cbar_y, _cbar_x + _cbar_w, _cbar_y + _cbar_h, true);
                            }
                        }'''

assert old_icon in code, "old_icon not found in Draw_64.gml"
code = code.replace(old_icon, new_icon)

# 2. Replace inspector facility block
old_insp = '''                if (_ht.terrain_type == "BASE_FACILITY") {
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
                draw_text(_hud_x + 8, _insp_y + 178, "TO REVEAL MOVEMENT RANGE");'''

new_insp = '''                if (_ht.terrain_type == "BASE_FACILITY") {
                    var _is_pmc_fac = (_ht.controlling_faction == "pmc");
                    draw_set_color(_is_pmc_fac ? make_color_rgb(255, 220, 80) : make_color_rgb(255, 90, 80));
                    draw_text(_hud_x + 8, _insp_y + 115, _is_pmc_fac ? "★ PMC SECURED FACILITY" : "⚠ HOSTILE DEFENSE REDOUBT");
                    draw_set_color(make_color_rgb(180, 210, 240));
                    draw_text(_hud_x + 8, _insp_y + 130, "NAME: " + string_copy(_ht.name, 1, 18));

                    var _cprog = variable_struct_exists(_ht, "capture_progress") ? _ht.capture_progress : 0;
                    draw_set_color(make_color_rgb(255, 215, 60));
                    draw_text(_hud_x + 8, _insp_y + 146, "SOVEREIGNTY GAUGE: " + string(_cprog) + " %");

                    draw_set_color(make_color_rgb(80, 255, 140));
                    draw_text(_hud_x + 8, _insp_y + 162, "PERKS: +20 HP REPAIRS | +40% DEF");
                } else {
                    draw_set_color(make_color_rgb(140, 175, 210));
                    draw_text(_hud_x + 8, _insp_y + 115, (_hov_vis == 1) ? "Explored sector under radar fog." : "Actively illuminated by sensors.");
                    draw_set_color(make_color_rgb(200, 220, 240));
                    draw_text(_hud_x + 8, _insp_y + 160, "SELECT ALLIED SQUADRON");
                    draw_text(_hud_x + 8, _insp_y + 178, "TO REVEAL MOVEMENT RANGE");
                }'''

assert old_insp in code, "old_insp not found in Draw_64.gml"
code = code.replace(old_insp, new_insp)

with open("objects/obj_HQTerminal/Draw_64.gml", "w") as f:
    f.write(code)

print("Updated Draw_64.gml for facility capture successfully!")
