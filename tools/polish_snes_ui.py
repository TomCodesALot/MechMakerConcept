import re

# 1. Update HQTerminal Draw_64
hq_path = "objects/obj_HQTerminal/Draw_64.gml"
with open(hq_path, "r") as f:
    code = f.read()

# Tab 0: Crucible buttons
old_c_btns = """            draw_set_color(_lb_hov ? make_color_rgb(30, 70, 45) : make_color_rgb(16, 36, 24));
            draw_rectangle(_mx_box + 8, _lb_y, _mx_box + 130, _lb_y + 24, false);
            draw_set_color(make_color_rgb(60, 200, 100));
            draw_rectangle(_mx_box + 8, _lb_y, _mx_box + 130, _lb_y + 24, true);
            draw_set_color(c_white);
            draw_text(_mx_box + 24, _lb_y + 4, "[+1 LOAD]");"""

new_c_btns = """            scr_draw_snes_button(_mx_box + 8, _lb_y, 122, 24, "[+1 LOAD]", _lb_hov, false, make_color_rgb(60, 200, 100));"""

if old_c_btns in code:
    code = code.replace(old_c_btns, new_c_btns)
    print("✓ Polished Tab 0 load button")

old_c_act = """        draw_set_color(_purg_hov ? make_color_rgb(80, 30, 30) : make_color_rgb(40, 16, 16));
        draw_rectangle(_win_x, _exec_y, _win_x + 180, _exec_y + 38, false);
        draw_set_color(make_color_rgb(240, 80, 80));
        draw_rectangle(_win_x, _exec_y, _win_x + 180, _exec_y + 38, true);
        draw_set_color(c_white);
        draw_text(_win_x + 22, _exec_y + 11, "[PURGE HOPPER]");

        var _syn_btn_x = _win_x + 196;
        var _syn_btn_w = 398;
        var _syn_hov = (_mx >= _syn_btn_x && _mx <= _syn_btn_x + _syn_btn_w && _my >= _exec_y && _my <= _exec_y + 38);
        if (_syn_hov && _click) crucible_execute_synthesis();
        draw_set_color(_syn_hov ? make_color_rgb(30, 95, 60) : make_color_rgb(18, 52, 32));
        draw_rectangle(_syn_btn_x, _exec_y, _syn_btn_x + _syn_btn_w, _exec_y + 38, false);
        draw_set_color(make_color_rgb(60, 240, 120));
        draw_rectangle(_syn_btn_x, _exec_y, _syn_btn_x + _syn_btn_w, _exec_y + 38, true);
        draw_set_color(c_white);
        draw_text(_syn_btn_x + 40, _exec_y + 11, ">> EXECUTE ALLOY SYNTHESIS BATCH <<");"""

new_c_act = """        scr_draw_snes_button(_win_x, _exec_y, 180, 38, "[PURGE HOPPER]", _purg_hov, false, make_color_rgb(240, 80, 80));

        var _syn_btn_x = _win_x + 196;
        var _syn_btn_w = 398;
        var _syn_hov = (_mx >= _syn_btn_x && _mx <= _syn_btn_x + _syn_btn_w && _my >= _exec_y && _my <= _exec_y + 38);
        if (_syn_hov && _click) crucible_execute_synthesis();
        scr_draw_snes_button(_syn_btn_x, _exec_y, _syn_btn_w, 38, ">> EXECUTE ALLOY SYNTHESIS BATCH <<", _syn_hov, false, make_color_rgb(60, 240, 120));"""

if old_c_act in code:
    code = code.replace(old_c_act, new_c_act)
    print("✓ Polished Tab 0 purge & execute synthesis buttons")

# Tab 1: Factory columns & upgrades
old_f_cols = """        // Left Column: Facility Upgrades & Assembly Lines
        var _col1_w = 580;
        draw_set_color(make_color_rgb(10, 16, 24));
        draw_rectangle(_f_x, _f_y + 24, _f_x + _col1_w, _f_y + 580, false);
        draw_set_color(make_color_rgb(35, 60, 90));
        draw_rectangle(_f_x, _f_y + 24, _f_x + _col1_w, _f_y + 580, true);"""

new_f_cols = """        // Left Column: Facility Upgrades & Assembly Lines
        var _col1_w = 580;
        scr_draw_snes_panel(_f_x, _f_y + 24, _col1_w, 556, "FACILITY UPGRADES & ASSEMBLY LINES", make_color_rgb(80, 180, 240), false, 0.04);"""

if old_f_cols in code:
    code = code.replace(old_f_cols, new_f_cols)
    print("✓ Polished Tab 1 facility column")

old_f_u1 = """            draw_set_color(_u1_hov ? make_color_rgb(30, 70, 50) : make_color_rgb(18, 40, 28));
            draw_rectangle(_f_x + 16, _u1_y, _f_x + 550, _u1_y + 32, false);
            draw_set_color(make_color_rgb(80, 220, 120));
            draw_rectangle(_f_x + 16, _u1_y, _f_x + 550, _u1_y + 32, true);
            draw_set_color(c_white);
            draw_text(_f_x + 24, _u1_y + 8, _gm.facilities.crucible_tier > 1 ? "[CRUCIBLE TIER 2 INSTALLED]" : "[UPGRADE CRUCIBLE: TIER 2 - 250,000 Cr]");

            // 2. Expand Assembly Lines
            var _u2_y = _u1_y + 40;
            var _u2_hov = (_mx >= _f_x + 16 && _mx <= _f_x + 550 && _my >= _u2_y && _my <= _u2_y + 32);
            if (_u2_hov && _click && _gm.facilities.assembly_lines < 4) {
                if (_gm.spend_funds(300000)) {
                    _gm.facilities.assembly_lines++;
                    show_toast("ASSEMBLY CAPACITY EXPANDED TO " + string(_gm.facilities.assembly_lines) + " BAYS!", c_lime);
                } else {
                    show_toast("INSUFFICIENT FUNDS! (Requires 300,000 Cr)", c_red);
                }
            }
            draw_set_color(_u2_hov ? make_color_rgb(30, 60, 80) : make_color_rgb(18, 35, 48));
            draw_rectangle(_f_x + 16, _u2_y, _f_x + 550, _u2_y + 32, false);
            draw_set_color(make_color_rgb(80, 180, 240));
            draw_rectangle(_f_x + 16, _u2_y, _f_x + 550, _u2_y + 32, true);
            draw_set_color(c_white);
            draw_text(_f_x + 24, _u2_y + 8, "[COMMISSION NEW ASSEMBLY LINE - 300,000 Cr]");"""

new_f_u1 = """            scr_draw_snes_button(_f_x + 16, _u1_y, 534, 32, _gm.facilities.crucible_tier > 1 ? "[CRUCIBLE TIER 2 INSTALLED]" : "[UPGRADE CRUCIBLE: TIER 2 - 250,000 Cr]", _u1_hov, false, make_color_rgb(80, 220, 120));

            // 2. Expand Assembly Lines
            var _u2_y = _u1_y + 40;
            var _u2_hov = (_mx >= _f_x + 16 && _mx <= _f_x + 550 && _my >= _u2_y && _my <= _u2_y + 32);
            if (_u2_hov && _click && _gm.facilities.assembly_lines < 4) {
                if (_gm.spend_funds(300000)) {
                    _gm.facilities.assembly_lines++;
                    show_toast("ASSEMBLY CAPACITY EXPANDED TO " + string(_gm.facilities.assembly_lines) + " BAYS!", c_lime);
                } else {
                    show_toast("INSUFFICIENT FUNDS! (Requires 300,000 Cr)", c_red);
                }
            }
            scr_draw_snes_button(_f_x + 16, _u2_y, 534, 32, "[COMMISSION NEW ASSEMBLY LINE - 300,000 Cr]", _u2_hov, false, make_color_rgb(80, 180, 240));"""

if old_f_u1 in code:
    code = code.replace(old_f_u1, new_f_u1)
    print("✓ Polished Tab 1 upgrade buttons")

old_f_roster = """        // Right Column: Personnel Roster & Hiring Market
        var _col2_x = _f_x + _col1_w + 20;
        var _col2_w = _pan_w - (_col1_w + 80);
        draw_set_color(make_color_rgb(10, 16, 24));
        draw_rectangle(_col2_x, _f_y + 24, _col2_x + _col2_w, _f_y + 580, false);
        draw_set_color(make_color_rgb(35, 60, 90));
        draw_rectangle(_col2_x, _f_y + 24, _col2_x + _col2_w, _f_y + 580, true);"""

new_f_roster = """        // Right Column: Personnel Roster & Hiring Market
        var _col2_x = _f_x + _col1_w + 20;
        var _col2_w = _pan_w - (_col1_w + 80);
        scr_draw_snes_panel(_col2_x, _f_y + 24, _col2_w, 556, "ACTIVE PERSONNEL & PILOT ROSTER", make_color_rgb(255, 195, 60), false, 0.04);"""

if old_f_roster in code:
    code = code.replace(old_f_roster, new_f_roster)
    print("✓ Polished Tab 1 roster column")

with open(hq_path, "w") as f:
    f.write(code)

print("✓ All HQTerminal SNES UI enhancements written cleanly!")
