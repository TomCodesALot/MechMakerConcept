import re

target = "objects/obj_HQTerminal/Draw_64.gml"
with open(target, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update background opacity to 0.72 so the massive topographical maps look vibrant
code = code.replace("c_white, 0.40);", "c_white, 0.72);")

# 2. Update Pass 1 to add animated tactical assault arrows pointing at the target sector
old_p1_cont = '''                    // Moving Shin Gihren's Greed strike wing patrol along contested hyperlane
                    var _patrol_cycle = ((current_time / 4500.0) + (ti * 0.23)) % 1.0;
                    var _px = _tx1 + (_tx2 - _tx1) * _patrol_cycle;
                    var _py = _ty1 + (_ty2 - _ty1) * _patrol_cycle;
                    var _patrol_spec = scr_territory_get_garrison_spec(_t1);
                    scr_draw_tactical_counter(_px, _py, _t1.controlling_faction, _patrol_spec.unit_sprite_name, max(2, _patrol_spec.stack_count - 1), false, false, 0.72);'''

new_p1_cont = '''                    // Glowing tactical assault engagement arrow (Shin Gihren's Greed benchmark)
                    var _ang = point_direction(_tx1, _ty1, _tx2, _ty2);
                    var _arr_pulse = 28 + ((current_time / 16) % 36);
                    var _ax = _tx1 + lengthdir_x(_arr_pulse, _ang);
                    var _ay = _ty1 + lengthdir_y(_arr_pulse, _ang);
                    draw_set_color(make_color_rgb(255, 130, 190));
                    draw_arrow(_ax - lengthdir_x(22, _ang), _ay - lengthdir_y(22, _ang), _ax, _ay, 8);

                    // Moving Shin Gihren's Greed strike wing patrol along contested hyperlane
                    var _patrol_cycle = ((current_time / 4500.0) + (ti * 0.23)) % 1.0;
                    var _px = _tx1 + (_tx2 - _tx1) * _patrol_cycle;
                    var _py = _ty1 + (_ty2 - _ty1) * _patrol_cycle;
                    var _patrol_spec = scr_territory_get_garrison_spec(_t1);
                    scr_draw_tactical_counter(_px, _py, _t1.controlling_faction, _patrol_spec.unit_sprite_name, max(2, _patrol_spec.stack_count - 1), false, false, 0.72);'''

code = code.replace(old_p1_cont, new_p1_cont)

# 3. Update Pass 2 to draw translucent tactical hex influence clusters around each territory node
old_p2_node = '''        var _g_spec = scr_territory_get_garrison_spec(_t);

        // Draw Tactical Counter (Hex Plinth + Unit Miniature + Stack Badge + Reticle)
        scr_draw_tactical_counter(_nx, _ny - 4, _t.controlling_faction, _g_spec.unit_sprite_name, _g_spec.stack_count, _is_sel, _hov, 1.05);'''

new_p2_node = '''        var _g_spec = scr_territory_get_garrison_spec(_t);

        // Translucent Tactical Hex Influence Cluster (Shin Gihren's Greed Territory Zone)
        draw_set_color(_f_col);
        draw_set_alpha(_is_front ? 0.24 : 0.14);
        scr_draw_hex_cell(_nx, _ny - 4, 22, true);
        scr_draw_hex_cell(_nx - 26, _ny - 18, 18, true);
        scr_draw_hex_cell(_nx + 26, _ny - 18, 18, true);
        scr_draw_hex_cell(_nx - 26, _ny + 12, 18, true);
        scr_draw_hex_cell(_nx + 26, _ny + 12, 18, true);
        draw_set_alpha(1.0);

        // Draw Tactical Counter (Hex Plinth + Unit Miniature + Stack Badge + Reticle)
        scr_draw_tactical_counter(_nx, _ny - 4, _t.controlling_faction, _g_spec.unit_sprite_name, _g_spec.stack_count, _is_sel, _hov, 1.05);'''

code = code.replace(old_p2_node, new_p2_node)

# 4. Update the Minimap to dynamically render Earth Amber Radar / Mars / Space with tracking box
old_minimap = '''    // --- TOP-RIGHT CELESTIAL ORBITAL TELEMETRY MINIMAP (Shin Gihren's Greed Benchmark) ---
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

new_minimap = '''    // --- TOP-RIGHT CELESTIAL ORBITAL TELEMETRY MINIMAP (Shin Gihren's Greed Benchmark) ---
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

    if (_region_str == "EARTH" && sprite_exists(spr_radar_earth_amber)) {
        // High-Impact Amber Satellite Global Map (Shin Gihren's Greed Benchmark)
        draw_sprite_stretched_ext(spr_radar_earth_amber, 0, _mm_x + 2, _mm_y + 2, _mm_w - 4, _mm_h - 4, c_white, 0.85);
        draw_set_color(make_color_rgb(255, 215, 80));
        draw_text(_mm_x + 8, _mm_y + 6, "TERRESTRIAL SATELLITE RADAR");
        
        // Active Theater Camera Bounding Box (South America / Amazonian basin / Granite Redoubt)
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_rectangle(_mm_x + 48, _mm_y + 54, _mm_x + 88, _mm_y + 92, true);
        draw_rectangle(_mm_x + 47, _mm_y + 53, _mm_x + 89, _mm_y + 93, true);
    } else if (_region_str == "MARS" && sprite_exists(spr_map_mars_theater)) {
        draw_sprite_stretched_ext(spr_map_mars_theater, 0, _mm_x + 2, _mm_y + 2, _mm_w - 4, _mm_h - 4, c_white, 0.75);
        draw_set_color(make_color_rgb(255, 90, 80));
        draw_text(_mm_x + 8, _mm_y + 6, "THARSIS SATELLITE TELEMETRY");
        
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_rectangle(_mm_x + 38, _mm_y + 28, _mm_x + 92, _mm_y + 76, true);
    } else {
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_mm_x + 8, _mm_y + 6, "SOL ORBITAL TELEMETRY");

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

        draw_set_color(make_color_rgb(0, 240, 255));
        draw_rectangle(_mcx + 30, _mcy - 24, _mcx + 68, _mcy + 2, true);
    }
    
    // --- SHIN GIHREN\'S GREED TACTICAL TERRAIN HUD BOX (Bottom-Right of Radar Canvas) ---
    var _thud_w = 236;
    var _thud_h = 92;
    var _thud_x = _rad_x + _rad_w - _thud_w - 18;
    var _thud_y = _rad_y + _rad_h - _thud_h - 18;

    draw_set_color(make_color_rgb(222, 226, 236));
    draw_rectangle(_thud_x, _thud_y, _thud_x + _thud_w, _thud_y + _thud_h, false);
    draw_set_color(make_color_rgb(28, 40, 56));
    draw_rectangle(_thud_x, _thud_y, _thud_x + _thud_w, _thud_y + _thud_h, true);
    draw_rectangle(_thud_x + 1, _thud_y + 1, _thud_x + _thud_w - 1, _thud_y + _thud_h - 1, true);

    draw_set_color(make_color_rgb(240, 244, 252));
    draw_rectangle(_thud_x + 3, _thud_y + 3, _thud_x + _thud_w - 3, _thud_y + 24, false);
    draw_set_color(make_color_rgb(12, 22, 36));
    var _terr_type_name = (_region_str == "EARTH") ? "TERRESTRIAL CRATON" : ((_region_str == "MARS") ? "MARTIAN BASALT" : "ORBITAL VACUUM");
    draw_text(_thud_x + 10, _thud_y + 6, _terr_type_name);

    draw_set_color(make_color_rgb(25, 35, 50));
    draw_text(_thud_x + 10, _thud_y + 30, "DEFENSE BONUS");
    draw_set_color(make_color_rgb(0, 110, 180));
    draw_text(_thud_x + _thud_w - 55, _thud_y + 30, "+20 %");

    draw_set_color(make_color_rgb(25, 35, 50));
    draw_text(_thud_x + 10, _thud_y + 48, "SENSOR DENSITY");
    draw_set_color(make_color_rgb(25, 35, 50));
    draw_text(_thud_x + _thud_w - 55, _thud_y + 48, "00 %");

    draw_set_color(make_color_rgb(25, 35, 50));
    draw_text(_thud_x + 10, _thud_y + 68, "GARRISON SQUAD");
    draw_set_color(make_color_rgb(190, 40, 25));
    var _active_cnt = !is_undefined(_cur_t) ? _cur_g_spec.stack_count : 4;
    draw_text(_thud_x + _thud_w - 55, _thud_y + 68, "0" + string(_active_cnt) + " MS");'''

code = code.replace(old_minimap, new_minimap)

with open(target, "w", encoding="utf-8") as f:
    f.write(code)

print("✓ Successfully patched obj_HQTerminal/Draw_64.gml with massive Earth/Mars/Colony maps and HUD!")
