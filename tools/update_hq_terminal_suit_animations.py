HQ_PATH = "objects/obj_HQTerminal/Draw_64.gml"

with open(HQ_PATH, "r") as f:
    content = f.read()

# 1. Update Fly-off incumbent header with candidate index & animated preview
target_flyoff = """                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_col2_x + 24, _cmp_y + 6, "METRIC");
                    draw_text(_col2_x + 240, _cmp_y + 6, "CANDIDATE: " + (!is_undefined(_cur_cand) ? _cur_cand.name : "None"));
                    draw_text(_col2_x + 500, _cmp_y + 6, "INCUMBENT: " + _inc.name);"""

replacement_flyoff = """                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_col2_x + 24, _cmp_y + 6, "METRIC");
                    draw_text(_col2_x + 240, _cmp_y + 6, "CANDIDATE: " + (!is_undefined(_cur_cand) ? _cur_cand.name : "None"));
                    var _cand_tag = (!is_undefined(_cur_mp) && variable_struct_exists(_cur_mp, "candidate_index")) ? (" [CANDIDATE " + string(_cur_mp.candidate_index + 1) + "/4]") : "";
                    draw_text(_col2_x + 500, _cmp_y + 6, "INCUMBENT: " + _inc.name + _cand_tag);

                    // Render Animated Preview of Incumbent Mass Production Chassis (docs/29)
                    scr_draw_animated_mobile_suit(_inc.id, _col2_x + _col2_w - 75, _cmp_y + 98, 0.65, -1, "idle");"""

assert target_flyoff in content, "target_flyoff not found in obj_HQTerminal!"
content = content.replace(target_flyoff, replacement_flyoff, 1)

# 2. Add corporate dossier animated preview
target_dossier = """                // Line 3: R&D Doctrine & Active Line Chassis
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_cdx + 14, _cdy + 44, "R&D Doctrine: " + _b_name + "  |  Active Line Chassis: " + _line_suit);"""

replacement_dossier = """                // Line 3: R&D Doctrine & Active Line Chassis
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_cdx + 14, _cdy + 44, "R&D Doctrine: " + _b_name + "  |  Active Line Chassis: " + _line_suit);

                // Render Animated Mobile Suit Preview for Corporate Dossier (docs/29)
                scr_draw_animated_mobile_suit(_line_suit, _cdx + _cd_w - 55, _cdy + 75, 0.45, -1, "idle");"""

assert target_dossier in content, "target_dossier not found in obj_HQTerminal!"
content = content.replace(target_dossier, replacement_dossier, 1)

with open(HQ_PATH, "w") as f:
    f.write(content)

print("Updated obj_HQTerminal with animated suit previews!")
