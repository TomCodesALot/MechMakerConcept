import re

fp = "objects/obj_HQTerminal/Draw_64.gml"
with open(fp, "r", encoding="utf-8") as f:
    text = f.read()

target_tab2_factions = """                draw_set_color(make_color_rgb(14, 20, 28));
                draw_rectangle(_fx, _std_y, _fx + _f_box_w, _std_y + 44, false);
                draw_set_color(make_color_rgb(40, 65, 95));
                draw_rectangle(_fx, _std_y, _fx + _f_box_w, _std_y + 44, true);

                draw_set_color(make_color_rgb(240, 210, 100));
                draw_text(_fx + 10, _std_y + 6, _finfo.name);
                var _std_col = (_std > 20) ? c_lime : ((_std < -10) ? c_red : make_color_rgb(240, 200, 80));
                draw_set_color(_std_col);
                draw_text(_fx + 10, _std_y + 24, "Standing: " + string(_std) + " (" + _finfo.standing_title + ")");"""

replacement_tab2_factions = """                var _f_ai = _finfo[$ "ai_state"] ?? "PEACE";
                var _is_desp = (_f_ai == "DESPERATE");
                var _is_win = (_f_ai == "WINNING");
                var _is_war = (_f_ai == "STANDARD_WAR");

                var _box_bg = _is_desp ? make_color_rgb(38, 14, 18) : (_is_win ? make_color_rgb(34, 30, 12) : make_color_rgb(14, 20, 28));
                var _box_brd = _is_desp ? make_color_rgb(255, 60, 60) : (_is_win ? make_color_rgb(255, 215, 80) : (_is_war ? make_color_rgb(220, 80, 80) : make_color_rgb(40, 65, 95)));

                draw_set_color(_box_bg);
                draw_rectangle(_fx, _std_y, _fx + _f_box_w, _std_y + 56, false);
                draw_set_color(_box_brd);
                draw_rectangle(_fx, _std_y, _fx + _f_box_w, _std_y + 56, true);

                draw_set_color(make_color_rgb(240, 210, 100));
                draw_text(_fx + 10, _std_y + 6, _finfo.name);

                // AI Brain Status Tag
                var _ai_tag = "[PEACE]";
                var _ai_col = make_color_rgb(100, 220, 255);
                if (_is_desp) { _ai_tag = "[CRITICAL +100%]"; _ai_col = make_color_rgb(255, 60, 60); }
                else if (_is_win) { _ai_tag = "[DOMINANT]"; _ai_col = make_color_rgb(255, 215, 80); }
                else if (_is_war) { _ai_tag = "[WAR]"; _ai_col = make_color_rgb(255, 100, 100); }

                draw_set_color(_ai_col);
                draw_text(_fx + _f_box_w - string_width(_ai_tag) - 8, _std_y + 6, _ai_tag);

                var _std_col = (_std > 20) ? c_lime : ((_std < -10) ? c_red : make_color_rgb(240, 200, 80));
                draw_set_color(_std_col);
                draw_text(_fx + 10, _std_y + 23, "Standing: " + string(_std) + " (" + _finfo.standing_title + ")");

                draw_set_color(_is_desp ? make_color_rgb(255, 180, 180) : make_color_rgb(160, 190, 220));
                var _posture_txt = _is_desp ? "EMERGENCY: Double Payout Bailout Active!" : (_is_win ? "HEGEMONY: Market Tariffs Enforced" : ("Posture: " + string(_finfo[$ "ai_behavior_title"] ?? "Consolidation")));
                draw_text(_fx + 10, _std_y + 38, _posture_txt);"""

assert target_tab2_factions in text, "target_tab2_factions not found"
text = text.replace(target_tab2_factions, replacement_tab2_factions, 1)

target_c_disp_y = """            // Active vs Available Contracts
            var _c_disp_y = _std_y + 54;"""
replacement_c_disp_y = """            // Active vs Available Contracts
            var _c_disp_y = _std_y + 68;"""

assert target_c_disp_y in text, "target_c_disp_y not found"
text = text.replace(target_c_disp_y, replacement_c_disp_y, 1)

with open(fp, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully updated objects/obj_HQTerminal/Draw_64.gml with AI Brain Faction meters!")
