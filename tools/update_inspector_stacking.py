with open("objects/obj_HQTerminal/Draw_64.gml", "r") as f:
    code = f.read()

old_block = '''        if (!is_undefined(_sel_unit)) {
            // Selected Unit Profile
            draw_set_color(c_white);
            draw_text(_hud_x + 8, _insp_y + 28, string_copy(_sel_unit.name, 1, 20));
            draw_set_color(make_color_rgb(255, 215, 60));
            draw_text(_hud_x + 8, _insp_y + 44, _sel_unit.unit_label);

            // Faction Banner
            var _fac_title = (_sel_unit.faction == "pmc") ? "PMC VANGUARD [ALLIED]" : "OPFOR GARRISON";
            draw_set_color((_sel_unit.faction == "pmc") ? make_color_rgb(0, 220, 255) : make_color_rgb(255, 90, 80));
            draw_text(_hud_x + 8, _insp_y + 60, _fac_title);

            // HP Bar
            draw_set_color(make_color_rgb(180, 210, 240));
            draw_text(_hud_x + 8, _insp_y + 78, "HULL INTEGRITY:");
            draw_set_color(make_color_rgb(60, 220, 100));
            draw_text(_hud_x + _hud_w - 60, _insp_y + 78, string(_sel_unit.hp) + "/" + string(_sel_unit.max_hp));

            var _ibar_w = _hud_w - 16;
            draw_set_color(make_color_rgb(20, 30, 42));
            draw_rectangle(_hud_x + 8, _insp_y + 94, _hud_x + 8 + _ibar_w, _insp_y + 101, false);
            draw_set_color(make_color_rgb(60, 220, 100));
            draw_rectangle(_hud_x + 8, _insp_y + 94, _hud_x + 8 + floor(_ibar_w * (_sel_unit.hp / _sel_unit.max_hp)), _insp_y + 101, false);

            // MP Bar
            draw_set_color(make_color_rgb(180, 210, 240));
            draw_text(_hud_x + 8, _insp_y + 106, "MOBILITY POINTS:");
            draw_set_color(make_color_rgb(0, 220, 255));
            draw_text(_hud_x + _hud_w - 60, _insp_y + 106, string(_sel_unit.current_mp) + "/" + string(_sel_unit.max_mp) + " MP");

            draw_set_color(make_color_rgb(20, 30, 42));
            draw_rectangle(_hud_x + 8, _insp_y + 122, _hud_x + 8 + _ibar_w, _insp_y + 129, false);
            draw_set_color(make_color_rgb(0, 220, 255));
            draw_rectangle(_hud_x + 8, _insp_y + 122, _hud_x + 8 + floor(_ibar_w * (_sel_unit.current_mp / _sel_unit.max_mp)), _insp_y + 129, false);

            // Combat Power Stats
            draw_set_color(make_color_rgb(220, 230, 245));
            draw_text(_hud_x + 8, _insp_y + 138, "ATK: " + string(_sel_unit.attack) + "  DEF: " + string(_sel_unit.defense) + "  RNG: " + string(_sel_unit.range) + " HEX");'''

new_block = '''        if (!is_undefined(_sel_unit)) {
            // Check Battlegroup Stack at this hex
            var _cur_stack = [];
            var _comb_atk = 0;
            for (var su = 0; su < array_length(stronghold_hex_units); su++) {
                var _su = stronghold_hex_units[su];
                if (_su.hp > 0 && _su.col == _sel_unit.col && _su.row == _sel_unit.row && _su.faction == _sel_unit.faction) {
                    array_push(_cur_stack, _su);
                    _comb_atk += _su.attack;
                }
            }
            var _cur_stack_size = array_length(_cur_stack);

            // Selected Unit Profile
            draw_set_color(c_white);
            draw_text(_hud_x + 8, _insp_y + 28, string_copy(_sel_unit.name, 1, 20));
            draw_set_color(make_color_rgb(255, 215, 60));
            if (_cur_stack_size > 1) {
                draw_text(_hud_x + 8, _insp_y + 44, "BATTLEGROUP [" + string(_cur_stack_size) + "/3 UNITS]");
            } else {
                draw_text(_hud_x + 8, _insp_y + 44, _sel_unit.unit_label);
            }

            // Faction Banner
            var _fac_title = (_sel_unit.faction == "pmc") ? "PMC VANGUARD [ALLIED]" : "OPFOR GARRISON";
            draw_set_color((_sel_unit.faction == "pmc") ? make_color_rgb(0, 220, 255) : make_color_rgb(255, 90, 80));
            draw_text(_hud_x + 8, _insp_y + 60, _fac_title);

            // HP Bar
            draw_set_color(make_color_rgb(180, 210, 240));
            draw_text(_hud_x + 8, _insp_y + 78, "HULL INTEGRITY:");
            draw_set_color(make_color_rgb(60, 220, 100));
            draw_text(_hud_x + _hud_w - 60, _insp_y + 78, string(_sel_unit.hp) + "/" + string(_sel_unit.max_hp));

            var _ibar_w = _hud_w - 16;
            draw_set_color(make_color_rgb(20, 30, 42));
            draw_rectangle(_hud_x + 8, _insp_y + 94, _hud_x + 8 + _ibar_w, _insp_y + 101, false);
            draw_set_color(make_color_rgb(60, 220, 100));
            draw_rectangle(_hud_x + 8, _insp_y + 94, _hud_x + 8 + floor(_ibar_w * (_sel_unit.hp / _sel_unit.max_hp)), _insp_y + 101, false);

            // MP Bar
            draw_set_color(make_color_rgb(180, 210, 240));
            draw_text(_hud_x + 8, _insp_y + 106, "MOBILITY POINTS:");
            draw_set_color(make_color_rgb(0, 220, 255));
            draw_text(_hud_x + _hud_w - 60, _insp_y + 106, string(_sel_unit.current_mp) + "/" + string(_sel_unit.max_mp) + " MP");

            draw_set_color(make_color_rgb(20, 30, 42));
            draw_rectangle(_hud_x + 8, _insp_y + 122, _hud_x + 8 + _ibar_w, _insp_y + 129, false);
            draw_set_color(make_color_rgb(0, 220, 255));
            draw_rectangle(_hud_x + 8, _insp_y + 122, _hud_x + 8 + floor(_ibar_w * (_sel_unit.current_mp / _sel_unit.max_mp)), _insp_y + 129, false);

            // Combat Power Stats (Reflecting Combined Attack if Stacked)
            draw_set_color(make_color_rgb(220, 230, 245));
            if (_cur_stack_size > 1) {
                draw_text(_hud_x + 8, _insp_y + 138, "COMBINED ATK: " + string(_comb_atk) + " (STACK x" + string(_cur_stack_size) + ")");
            } else {
                draw_text(_hud_x + 8, _insp_y + 138, "ATK: " + string(_sel_unit.attack) + "  DEF: " + string(_sel_unit.defense) + "  RNG: " + string(_sel_unit.range) + " HEX");
            }'''

assert old_block in code, "old_block not found in Draw_64.gml"
code = code.replace(old_block, new_block)

with open("objects/obj_HQTerminal/Draw_64.gml", "w") as f:
    f.write(code)

print("Updated Inspector for Stacking successfully!")
