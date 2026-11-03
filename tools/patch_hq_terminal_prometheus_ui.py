import re

hqt_path = "objects/obj_HQTerminal/Draw_64.gml"
with open(hqt_path, "r") as f:
    code = f.read()

# 1. Update Era banner to highlight Era 0
old_banner = '''            draw_set_color(make_color_rgb(255, 220, 100));
            draw_text(_rx + 12, _era_y + 5, "ACTIVE TIMELINE ERA: " + _gm.timeline_era_name + " (YEAR " + string(_gm.current_cycle_year) + " // DAY " + string(_gm.current_cycle_day) + ")");'''

new_banner = '''            if (_gm.timeline_era == 0) {
                draw_set_color(make_color_rgb(255, 200, 50));
                draw_text(_rx + 12, _era_y + 5, "ACTIVE TIMELINE ERA: " + _gm.timeline_era_name + " // THE PROMETHEUS PROTOCOL (NO OTHER MOBILE SUITS EXIST!)");
            } else {
                draw_set_color(make_color_rgb(255, 220, 100));
                draw_text(_rx + 12, _era_y + 5, "ACTIVE TIMELINE ERA: " + _gm.timeline_era_name + " (YEAR " + string(_gm.current_cycle_year) + " // DAY " + string(_gm.current_cycle_day) + ")");
            }'''

if old_banner in code:
    code = code.replace(old_banner, new_banner)
    print("Updated Era Banner in obj_HQTerminal Draw_64.")

# 2. Add Reverse-Engineering Status in Corporate Cards
old_stake_line = 'draw_text(_cdx + 14, _cdy + 62, _x_spec_tag + "Stake: " + string(_cp.player_shares) + " sh (" + string(_cp.player_equity_pct) + "%) " + _stake_badge + " | Div: +" + string(_cp.dividend_per_turn) + " Cr/T");'

new_stake_line = '''draw_text(_cdx + 14, _cdy + 62, _x_spec_tag + "Stake: " + string(_cp.player_shares) + " sh (" + string(_cp.player_equity_pct) + "%) " + _stake_badge + " | Div: +" + string(_cp.dividend_per_turn) + " Cr/T");

                // Prometheus Reverse-Engineering Progress (doc 38)
                var _re_prog = (variable_instance_exists(_gm, "reverse_engineering_progress") && variable_struct_exists(_gm.reverse_engineering_progress, _cid)) ? _gm.reverse_engineering_progress[$ _cid] : 0.0;
                var _re_status = (_re_prog >= 100.0) ? "PROTOTYPE DEPLOYED" : (_re_prog >= 75.0 ? "Retooling" : (_re_prog >= 50.0 ? "Walking Hybrid" : (_re_prog >= 25.0 ? "Salvage" : "Telemetry")));
                var _re_col = (_re_prog >= 100.0) ? c_red : ((_re_prog >= 50.0) ? make_color_rgb(255, 170, 40) : make_color_rgb(100, 220, 255));
                draw_set_color(_re_col);
                draw_text(_cdx + 14, _cdy + 74, "MS Reverse-Eng: " + string_format(_re_prog, 1, 1) + "% [" + _re_status + "]");'''

if old_stake_line in code and "Prometheus Reverse-Engineering Progress" not in code:
    code = code.replace(old_stake_line, new_stake_line)
    print("Added Reverse-Engineering status in Corporate Cards in obj_HQTerminal Draw_64.")

with open(hqt_path, "w") as f:
    f.write(code)

print("obj_HQTerminal Draw_64 patching complete.")
