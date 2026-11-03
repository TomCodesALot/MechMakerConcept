import re

target = "objects/obj_HQTerminal/Draw_64.gml"
with open(target, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update Pass 1 (Hyperlanes) to add moving strike forces along contested lines
old_pass1 = '''    // Pass 1: Hyperlane Supply Lines
    for (var ti = 0; ti < array_length(_t_list); ti++) {
        var _t1 = _t_list[ti];
        var _tx1 = _rad_x + 40 + floor(_t1.map_x * 1.34);
        var _ty1 = _rad_y + 48 + floor(_t1.map_y * 1.48);
        for (var ci = 0; ci < array_length(_t1.connected_ids); ci++) {
            var _t2 = scr_territory_get(_t1.connected_ids[ci]);
            if (!is_undefined(_t2) && _t2.region == _region_str) {
                var _tx2 = _rad_x + 40 + floor(_t2.map_x * 1.34);
                var _ty2 = _rad_y + 48 + floor(_t2.map_y * 1.48);
                var _is_contested = (_t1.controlling_faction != _t2.controlling_faction);
                draw_set_color(_is_contested ? make_color_rgb(240, 70, 70) : make_color_rgb(0, 180, 220));
                draw_set_alpha(_is_contested ? 0.9 : 0.5);
                draw_line_width(_tx1, _ty1, _tx2, _ty2, _is_contested ? 2 : 1);
                draw_set_alpha(1.0);
            }
        }
    }'''

new_pass1 = '''    // Pass 1: Hyperlane Supply Lines & Contested Frontline Vectors
    for (var ti = 0; ti < array_length(_t_list); ti++) {
        var _t1 = _t_list[ti];
        var _tx1 = _rad_x + 40 + floor(_t1.map_x * 1.34);
        var _ty1 = _rad_y + 48 + floor(_t1.map_y * 1.48);
        for (var ci = 0; ci < array_length(_t1.connected_ids); ci++) {
            var _t2 = scr_territory_get(_t1.connected_ids[ci]);
            if (!is_undefined(_t2) && _t2.region == _region_str) {
                var _tx2 = _rad_x + 40 + floor(_t2.map_x * 1.34);
                var _ty2 = _rad_y + 48 + floor(_t2.map_y * 1.48);
                var _is_contested = (_t1.controlling_faction != _t2.controlling_faction);
                
                // Outer glow & core vector line
                if (_is_contested) {
                    draw_set_color(make_color_rgb(140, 20, 30));
                    draw_line_width(_tx1, _ty1, _tx2, _ty2, 4);
                    draw_set_color(make_color_rgb(255, 60, 70));
                    draw_line_width(_tx1, _ty1, _tx2, _ty2, 2);
                    
                    // Moving Shin Gihren's Greed strike wing patrol along contested hyperlane
                    var _patrol_cycle = ((current_time / 4500.0) + (ti * 0.23)) % 1.0;
                    var _px = _tx1 + (_tx2 - _tx1) * _patrol_cycle;
                    var _py = _ty1 + (_ty2 - _ty1) * _patrol_cycle;
                    var _patrol_spec = scr_territory_get_garrison_spec(_t1);
                    scr_draw_tactical_counter(_px, _py, _t1.controlling_faction, _patrol_spec.unit_sprite_name, max(2, _patrol_spec.stack_count - 1), false, false, 0.72);
                } else {
                    draw_set_color(make_color_rgb(0, 160, 210));
                    draw_set_alpha(0.5);
                    draw_line_width(_tx1, _ty1, _tx2, _ty2, 1);
                    draw_set_alpha(1.0);
                }
            }
        }
    }'''

code = code.replace(old_pass1, new_pass1)

# 2. Update Pass 2 to render the Shin Gihren's Greed Tactical Hex Plinth & Unit Counter
old_pass2 = '''    // Pass 2: Interactive Territory Nodes
    for (var ti = 0; ti < array_length(_t_list); ti++) {
        var _t = _t_list[ti];
        var _nx = _rad_x + 40 + floor(_t.map_x * 1.34);
        var _ny = _rad_y + 48 + floor(_t.map_y * 1.48);
        var _nw = 104;
        var _nh = 38;
        var _is_sel = (selected_territory_id == _t.id);
        var _is_front = scr_territory_is_frontline(_t.id);
        var _hov = (_mx >= _nx - _nw/2 && _mx <= _nx + _nw/2 && _my >= _ny - _nh/2 && _my <= _ny + _nh/2);

        if (_hov && _click) {
            selected_territory_id = _t.id;
            scr_audio_play_ui("click");
        }

        // Controlling Faction Color
        var _f_col = make_color_rgb(60, 140, 255); // Terran Blue
        if (_t.controlling_faction == "faction_b") _f_col = make_color_rgb(40, 220, 180); // Colony Teal
        else if (_t.controlling_faction == "faction_c") _f_col = make_color_rgb(255, 160, 40); // Syndicate Gold
        else if (_t.controlling_faction == "faction_d") _f_col = make_color_rgb(180, 90, 240); // Zaibatsu Purple
        else if (_t.controlling_faction == "faction_e") _f_col = make_color_rgb(120, 130, 240); // Sidereal Ruby
        else if (_t.controlling_faction == "faction_f") _f_col = make_color_rgb(240, 60, 60); // Mars Red
        else if (_t.controlling_faction == "pmc") _f_col = make_color_rgb(255, 215, 60); // PMC Gold

        // Node Card Fill
        draw_set_color(_is_sel ? make_color_rgb(32, 58, 88) : (_hov ? make_color_rgb(24, 40, 62) : make_color_rgb(12, 18, 28)));
        draw_rectangle(_nx - _nw/2, _ny - _nh/2, _nx + _nw/2, _ny + _nh/2, false);

        // Border: Gold/Cyan if selected, frontline pulsates red
        draw_set_color(_is_sel ? make_color_rgb(0, 240, 255) : (_is_front ? make_color_rgb(255, 90, 90) : make_color_rgb(40, 70, 105)));
        draw_rectangle(_nx - _nw/2, _ny - _nh/2, _nx + _nw/2, _ny + _nh/2, true);

        // Faction Color Indicator Pill
        draw_set_color(_f_col);
        draw_rectangle(_nx - _nw/2 + 2, _ny - _nh/2 + 2, _nx - _nw/2 + 7, _ny + _nh/2 - 2, false);

        // Territory Name
        draw_set_color(_is_sel ? c_white : make_color_rgb(190, 215, 240));
        var _disp_name = string_copy(_t.name, 1, 14);
        draw_text(_nx - _nw/2 + 10, _ny - 12, _disp_name);

        // Defense & Frontline Tag
        draw_set_color(_is_front ? make_color_rgb(255, 120, 120) : make_color_rgb(110, 190, 140));
        draw_text(_nx - _nw/2 + 10, _ny + 2, "DEF " + string(_t.defense_rating) + (_is_front ? " [WAR]" : ""));
    }'''

new_pass2 = '''    // Pass 2: Interactive Territory Nodes with Shin Gihren's Greed Tactical Plinths
    for (var ti = 0; ti < array_length(_t_list); ti++) {
        var _t = _t_list[ti];
        var _nx = _rad_x + 40 + floor(_t.map_x * 1.34);
        var _ny = _rad_y + 48 + floor(_t.map_y * 1.48);
        var _is_sel = (selected_territory_id == _t.id);
        var _is_front = scr_territory_is_frontline(_t.id);
        
        var _click_r = 34;
        var _hov = (_mx >= _nx - _click_r && _mx <= _nx + _click_r && _my >= _ny - _click_r && _my <= _ny + _click_r + 18);

        if (_hov && _click) {
            selected_territory_id = _t.id;
            scr_audio_play_ui("click");
        }

        // Controlling Faction Color
        var _f_col = make_color_rgb(60, 140, 255);
        if (_t.controlling_faction == "faction_b") _f_col = make_color_rgb(40, 220, 180);
        else if (_t.controlling_faction == "faction_c") _f_col = make_color_rgb(255, 160, 40);
        else if (_t.controlling_faction == "faction_d") _f_col = make_color_rgb(180, 90, 240);
        else if (_t.controlling_faction == "faction_e") _f_col = make_color_rgb(120, 130, 240);
        else if (_t.controlling_faction == "faction_f") _f_col = make_color_rgb(240, 60, 60);
        else if (_t.controlling_faction == "pmc") _f_col = make_color_rgb(255, 215, 60);

        var _g_spec = scr_territory_get_garrison_spec(_t);

        // Draw Tactical Counter (Hex Plinth + Unit Miniature + Stack Badge + Reticle)
        scr_draw_tactical_counter(_nx, _ny - 4, _t.controlling_faction, _g_spec.unit_sprite_name, _g_spec.stack_count, _is_sel, _hov, 1.05);

        // Tactical Nameplate Banner Underneath
        var _nb_w = 98;
        var _nb_h = 18;
        var _nb_y = _ny + 16;
        
        draw_set_color(_is_sel ? make_color_rgb(20, 44, 70) : (_hov ? make_color_rgb(16, 28, 44) : make_color_rgb(10, 16, 26)));
        draw_rectangle(_nx - _nb_w/2, _nb_y, _nx + _nb_w/2, _nb_y + _nb_h, false);
        draw_set_color(_is_sel ? make_color_rgb(0, 240, 255) : (_is_front ? make_color_rgb(255, 80, 80) : make_color_rgb(45, 80, 120)));
        draw_rectangle(_nx - _nb_w/2, _nb_y, _nx + _nb_w/2, _nb_y + _nb_h, true);

        // Faction Indicator Pill
        draw_set_color(_f_col);
        draw_rectangle(_nx - _nb_w/2 + 2, _nb_y + 2, _nx - _nb_w/2 + 5, _nb_y + _nb_h - 2, false);

        // Territory Name
        draw_set_color(_is_sel ? c_white : make_color_rgb(190, 215, 240));
        var _disp_name = string_copy(_t.name, 1, 13);
        draw_text(_nx - _nb_w/2 + 8, _nb_y + 2, _disp_name);
    }
    
    // --- TOP-RIGHT CELESTIAL ORBITAL TELEMETRY MINIMAP (Shin Gihren's Greed Benchmark) ---
    var _mm_w = 210;
    var _mm_h = 118;
    var _mm_x = _rad_x + _rad_w - _mm_w - 18;
    var _mm_y = _rad_y + 36;

    draw_set_color(make_color_rgb(8, 14, 22));
    draw_set_alpha(0.85);
    draw_rectangle(_mm_x, _mm_y, _mm_x + _mm_w, _mm_y + _mm_h, false);
    draw_set_alpha(1.0);
    draw_set_color(make_color_rgb(45, 80, 125));
    draw_rectangle(_mm_x, _mm_y, _mm_x + _mm_w, _mm_y + _mm_h, true);

    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_mm_x + 10, _mm_y + 8, "SOL ORBITAL TELEMETRY");

    var _mcx = _mm_x + 105;
    var _mcy = _mm_y + 68;
    draw_set_color(make_color_rgb(25, 45, 75));
    draw_ellipse(_mcx - 78, _mcy - 38, _mcx + 78, _mcy + 38, true);
    draw_ellipse(_mcx - 50, _mcy - 24, _mcx + 50, _mcy + 24, true);
    draw_ellipse(_mcx - 26, _mcy - 12, _mcx + 26, _mcy + 12, true);

    draw_set_color(make_color_rgb(255, 215, 80));
    draw_circle(_mcx, _mcy, 4, false); // Sol
    draw_set_color(make_color_rgb(60, 150, 255));
    draw_circle(_mcx + 46, _mcy - 12, 3, false); // Earth
    draw_set_color(make_color_rgb(200, 200, 190));
    draw_circle(_mcx + 52, _mcy - 14, 1, false); // Luna
    draw_set_color(make_color_rgb(240, 80, 60));
    draw_circle(_mcx - 70, _mcy + 16, 2, false); // Mars

    // Viewport Box
    draw_set_color(make_color_rgb(0, 240, 255));
    if (_region_str == "SPACE") {
        draw_rectangle(_mcx + 30, _mcy - 24, _mcx + 68, _mcy + 2, true);
    } else if (_region_str == "EARTH") {
        draw_rectangle(_mcx + 38, _mcy - 20, _mcx + 54, _mcy - 4, true);
    } else if (_region_str == "MARS") {
        draw_rectangle(_mcx - 82, _mcy + 6, _mcx - 58, _mcy + 26, true);
    }'''

code = code.replace(old_pass2, new_pass2)

# 3. Update Selected Sector Dossier to show the Garrison Battlegroup Tac-Card
old_dossier_header = '''    // Sector Name & Subregion
    var _content_y = _thumb_y + _thumb_h + 10;
    draw_set_color(make_color_rgb(255, 220, 90));
    draw_text(_dos_x + 16, _content_y, string_upper(_cur_t.name));
    draw_set_color(make_color_rgb(140, 175, 210));
    draw_text(_dos_x + 16, _content_y + 18, _cur_t.region + " // " + _cur_t.subregion);'''

new_dossier_header = '''    // Sector Name & Subregion
    var _content_y = _thumb_y + _thumb_h + 8;
    draw_set_color(make_color_rgb(255, 220, 90));
    draw_text(_dos_x + 16, _content_y, string_upper(_cur_t.name));
    draw_set_color(make_color_rgb(140, 175, 210));
    draw_text(_dos_x + 16, _content_y + 18, _cur_t.region + " // " + _cur_t.subregion);
    
    // --- GARRISON BATTLEGROUP TAC-CARD (Shin Gihren's Greed Benchmark) ---
    var _gcard_y = _content_y + 36;
    var _gcard_h = 64;
    draw_set_color(make_color_rgb(12, 18, 28));
    draw_rectangle(_dos_x + 16, _gcard_y, _dos_x + _dos_w - 16, _gcard_y + _gcard_h, false);
    draw_set_color(make_color_rgb(40, 75, 115));
    draw_rectangle(_dos_x + 16, _gcard_y, _dos_x + _dos_w - 16, _gcard_y + _gcard_h, true);
    
    var _cur_g_spec = scr_territory_get_garrison_spec(_cur_t);
    scr_draw_tactical_counter(_dos_x + 46, _gcard_y + 42, _cur_t.controlling_faction, _cur_g_spec.unit_sprite_name, _cur_g_spec.stack_count, true, false, 1.15);
    
    draw_set_color(c_white);
    draw_text(_dos_x + 78, _gcard_y + 8, string_upper(_cur_g_spec.unit_label));
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_dos_x + 78, _gcard_y + 24, "SQUADRON STRENGTH: [" + string(_cur_g_spec.stack_count) + "] UNITS");
    draw_set_color(make_color_rgb(160, 190, 220));
    draw_text(_dos_x + 78, _gcard_y + 42, string_copy(_cur_t.garrison_unit, 1, 24));'''

code = code.replace(old_dossier_header, new_dossier_header)

# Adjust following y offsets in Dossier to account for tac-card
code = code.replace("var _box_y = _content_y + 36;", "var _box_y = _content_y + 108;")

with open(target, "w", encoding="utf-8") as f:
    f.write(code)

print("✓ Successfully patched obj_HQTerminal/Draw_64.gml with Shin Gihren's Greed tactical counters & minimap!")
