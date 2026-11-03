path = 'objects/obj_HQTerminal/Draw_64.gml'
with open(path, 'r') as f:
    text = f.read()

# 1. Update panel title calculation
old_panel = '''var _panel_title = _region_str + " THEATER TACTICAL RADAR";
if (_region_str == "EARTH") {
    if (earth_view_mode == "GLOBAL") {
        _panel_title = "EARTH THEATER // GLOBAL STRATEGIC OVERVIEW (10 CONTINENTAL CITADELS)";
    } else {
        _panel_title = "STRATEGIC STRONGHOLD // GRANITE DEEP COMMAND [REGIONAL THEATER]";
    }
}
scr_draw_snes_panel(_rad_x, _rad_y, _rad_w, _rad_h, _panel_title, make_color_rgb(60, 180, 240), true);'''

new_panel = '''var _panel_title = _region_str + " THEATER TACTICAL RADAR";
if (earth_view_mode == "GLOBAL") {
    _panel_title = _region_str + " THEATER // GLOBAL STRATEGIC OVERVIEW";
} else {
    var _active_sh = scr_stronghold_get_layout(active_stronghold_id);
    _panel_title = "STRATEGIC STRONGHOLD // " + string_upper(_active_sh.stronghold_name);
}
scr_draw_snes_panel(_rad_x, _rad_y, _rad_w, _rad_h, _panel_title, make_color_rgb(60, 180, 240), true);'''

assert old_panel in text, "old_panel not found"
text = text.replace(old_panel, new_panel, 1)

# 2. Update dynamic minimap box and terrain HUD in Stronghold view
old_minimap = '''        if (sprite_exists(spr_radar_earth_amber)) {
            draw_sprite_stretched_ext(spr_radar_earth_amber, 0, _mm_x + 2, _mm_y + 2, _mm_w - 4, _mm_h - 4, c_white, 0.85);
            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_mm_x + 8, _mm_y + 6, "TERRESTRIAL SATELLITE RADAR");

            // Active Theater Camera Bounding Box (South America / Amazonian basin / Granite Redoubt)
            draw_set_color(make_color_rgb(0, 240, 255));
            draw_rectangle(_mm_x + 48, _mm_y + 54, _mm_x + 88, _mm_y + 92, true);
            draw_rectangle(_mm_x + 47, _mm_y + 53, _mm_x + 89, _mm_y + 93, true);
        }

        // Bottom-Right Terrain HUD Box
        var _thud_w = 236;
        var _thud_h = 92;
        var _thud_x = _rad_x + _rad_w - _thud_w - 18;
        var _thud_y = _rad_y + _rad_h - _thud_h - 18;
        draw_set_color(make_color_rgb(222, 226, 236));
        draw_rectangle(_thud_x, _thud_y, _thud_x + _thud_w, _thud_y + _thud_h, false);
        draw_set_color(make_color_rgb(28, 40, 56));
        draw_rectangle(_thud_x, _thud_y, _thud_x + _thud_w, _thud_y + _thud_h, true);

        draw_set_color(make_color_rgb(240, 244, 252));
        draw_rectangle(_thud_x + 3, _thud_y + 3, _thud_x + _thud_w - 3, _thud_y + 24, false);
        draw_set_color(make_color_rgb(12, 22, 36));
        draw_text(_thud_x + 10, _thud_y + 6, "SUBTERRANEAN GRANITE CRATON");'''

new_minimap = '''        if (_sh_layout.region == "MARS" && sprite_exists(spr_map_mars_theater)) {
            draw_sprite_stretched_ext(spr_map_mars_theater, 0, _mm_x + 2, _mm_y + 2, _mm_w - 4, _mm_h - 4, c_white, 0.85);
            draw_set_color(make_color_rgb(255, 90, 80));
            draw_text(_mm_x + 8, _mm_y + 6, "THARSIS SATELLITE TELEMETRY");
        } else if (sprite_exists(spr_radar_earth_amber)) {
            draw_sprite_stretched_ext(spr_radar_earth_amber, 0, _mm_x + 2, _mm_y + 2, _mm_w - 4, _mm_h - 4, c_white, 0.85);
            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_mm_x + 8, _mm_y + 6, "TERRESTRIAL SATELLITE RADAR");
        }

        var _mb = _sh_layout.minimap_box;
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_rectangle(_mm_x + _mb.x, _mm_y + _mb.y, _mm_x + _mb.x + _mb.w, _mm_y + _mb.y + _mb.h, true);
        draw_rectangle(_mm_x + _mb.x - 1, _mm_y + _mb.y - 1, _mm_x + _mb.x + _mb.w + 1, _mm_y + _mb.y + _mb.h + 1, true);

        // Bottom-Right Terrain HUD Box
        var _thud_w = 236;
        var _thud_h = 92;
        var _thud_x = _rad_x + _rad_w - _thud_w - 18;
        var _thud_y = _rad_y + _rad_h - _thud_h - 18;
        draw_set_color(make_color_rgb(222, 226, 236));
        draw_rectangle(_thud_x, _thud_y, _thud_x + _thud_w, _thud_y + _thud_h, false);
        draw_set_color(make_color_rgb(28, 40, 56));
        draw_rectangle(_thud_x, _thud_y, _thud_x + _thud_w, _thud_y + _thud_h, true);

        draw_set_color(make_color_rgb(240, 244, 252));
        draw_rectangle(_thud_x + 3, _thud_y + 3, _thud_x + _thud_w - 3, _thud_y + 24, false);
        draw_set_color(make_color_rgb(12, 22, 36));
        
        var _terr_hud_name = "TERRESTRIAL CRATON";
        if (_sh_layout.region == "MARS") _terr_hud_name = "MARTIAN VOLCANIC CALDERA";
        else if (string_pos("Cascadia", _sh_layout.stronghold_name) > 0) _terr_hud_name = "PACIFIC MASS-DRIVER CRATON";
        else if (string_pos("Gibraltar", _sh_layout.stronghold_name) > 0) _terr_hud_name = "MEDITERRANEAN SEA-GATE";
        else if (string_pos("Ural", _sh_layout.stronghold_name) > 0) _terr_hud_name = "YAMANTAU FORGE CRATON";
        else if (string_pos("Shanghai", _sh_layout.stronghold_name) > 0) _terr_hud_name = "YANGTZE ESTUARY ARCOLOGY";
        else if (string_pos("Kufra", _sh_layout.stronghold_name) > 0) _terr_hud_name = "SAHARA THERMAL GANTRY";
        else if (string_pos("Skagerrak", _sh_layout.stronghold_name) > 0) _terr_hud_name = "NORTH SEA SUB-SURFACE DOCKS";
        else if (string_pos("Woomera", _sh_layout.stronghold_name) > 0) _terr_hud_name = "OUTBACK KINETIC RANGE";
        else if (string_pos("Chimborazo", _sh_layout.stronghold_name) > 0) _terr_hud_name = "ANDES HIGH-ALTITUDE SPUR";
        else if (string_pos("Vostok", _sh_layout.stronghold_name) > 0) _terr_hud_name = "ANTARCTIC GLACIAL VAULT";
        else _terr_hud_name = "SUBTERRANEAN CRATON";
        draw_text(_thud_x + 10, _thud_y + 6, _terr_hud_name);'''

assert old_minimap in text, "old_minimap not found"
text = text.replace(old_minimap, new_minimap, 1)

# 3. Update entering stronghold from map node click
old_click_enter = '''                    if (selected_territory_id == _t.id && variable_struct_exists(_t, "is_major_stronghold") && _t.is_major_stronghold && _region_str == "EARTH") {
                        earth_view_mode = "STRONGHOLD";
                        active_stronghold_id = _t.id;
                        selected_subnode_id = "granite_core";
                        scr_audio_play_ui("confirm");
                    } else {'''

new_click_enter = '''                    if (selected_territory_id == _t.id && variable_struct_exists(_t, "is_major_stronghold") && _t.is_major_stronghold) {
                        earth_view_mode = "STRONGHOLD";
                        active_stronghold_id = _t.id;
                        var _target_sh = scr_stronghold_get_layout(_t.id);
                        selected_subnode_id = (array_length(_target_sh.subnodes) > 0) ? _target_sh.subnodes[0].id : "";
                        scr_audio_play_ui("confirm");
                    } else {'''

assert old_click_enter in text, "old_click_enter not found"
text = text.replace(old_click_enter, new_click_enter, 1)

# 4. Update dossier stronghold thumbnail and subtitle
old_dos_thumb = '''        var _loc_spr = spr_loc_earth_granite;
        if (sprite_exists(_loc_spr)) {
            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_thumb_x, _thumb_y, _thumb_x + _thumb_w, _thumb_y + _thumb_h, false);
            draw_sprite_stretched(_loc_spr, 0, _thumb_x, _thumb_y, _thumb_w, _thumb_h);

            // Frame and Corner Brackets
            draw_set_color(make_color_rgb(255, 215, 60));
            draw_rectangle(_thumb_x, _thumb_y, _thumb_x + _thumb_w, _thumb_y + _thumb_h, true);
            draw_rectangle(_thumb_x, _thumb_y, _thumb_x + 16, _thumb_y + 4, false);
            draw_rectangle(_thumb_x, _thumb_y, _thumb_x + 4, _thumb_y + 16, false);
            draw_rectangle(_thumb_x + _thumb_w - 16, _thumb_y, _thumb_x + _thumb_w, _thumb_y + 4, false);
            draw_rectangle(_thumb_x + _thumb_w - 4, _thumb_y, _thumb_x + _thumb_w, _thumb_y + 16, false);

            // Surveillance Badge Overlay
            draw_set_color(make_color_rgb(12, 18, 28));
            draw_rectangle(_thumb_x + 8, _thumb_y + _thumb_h - 22, _thumb_x + 195, _thumb_y + _thumb_h - 4, false);
            draw_set_color(make_color_rgb(255, 215, 60));
            draw_rectangle(_thumb_x + 8, _thumb_y + _thumb_h - 22, _thumb_x + 195, _thumb_y + _thumb_h - 4, true);
            draw_text(_thumb_x + 12, _thumb_y + _thumb_h - 19, "SUBNODE TELEMETRY // SEC-01");
        }

        // Subnode Name & Archetype
        var _content_y = _thumb_y + _thumb_h + 8;
        draw_set_color(make_color_rgb(255, 220, 90));
        draw_text(_dos_x + 16, _content_y, string_upper(_cur_sn.name));
        draw_set_color(make_color_rgb(140, 175, 210));
        draw_text(_dos_x + 16, _content_y + 18, "GRANITE COMMAND // " + _cur_sn.sub_type);'''

new_dos_thumb = '''        var _loc_spr = -1;
        var _parent_t = scr_territory_get(active_stronghold_id);
        if (!is_undefined(_parent_t) && variable_struct_exists(_parent_t, "loc_sprite_name")) {
            _loc_spr = asset_get_index(_parent_t.loc_sprite_name);
        }
        if (_loc_spr == -1 || !sprite_exists(_loc_spr)) {
            _loc_spr = (_sh_layout.region == "MARS") ? spr_loc_mars_redoubt : spr_loc_earth_granite;
        }

        if (sprite_exists(_loc_spr)) {
            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_thumb_x, _thumb_y, _thumb_x + _thumb_w, _thumb_y + _thumb_h, false);
            draw_sprite_stretched(_loc_spr, 0, _thumb_x, _thumb_y, _thumb_w, _thumb_h);

            // Frame and Corner Brackets
            draw_set_color(make_color_rgb(255, 215, 60));
            draw_rectangle(_thumb_x, _thumb_y, _thumb_x + _thumb_w, _thumb_y + _thumb_h, true);
            draw_rectangle(_thumb_x, _thumb_y, _thumb_x + 16, _thumb_y + 4, false);
            draw_rectangle(_thumb_x, _thumb_y, _thumb_x + 4, _thumb_y + 16, false);
            draw_rectangle(_thumb_x + _thumb_w - 16, _thumb_y, _thumb_x + _thumb_w, _thumb_y + 4, false);
            draw_rectangle(_thumb_x + _thumb_w - 4, _thumb_y, _thumb_x + _thumb_w, _thumb_y + 16, false);

            // Surveillance Badge Overlay
            draw_set_color(make_color_rgb(12, 18, 28));
            draw_rectangle(_thumb_x + 8, _thumb_y + _thumb_h - 22, _thumb_x + 195, _thumb_y + _thumb_h - 4, false);
            draw_set_color(make_color_rgb(255, 215, 60));
            draw_rectangle(_thumb_x + 8, _thumb_y + _thumb_h - 22, _thumb_x + 195, _thumb_y + _thumb_h - 4, true);
            draw_text(_thumb_x + 12, _thumb_y + _thumb_h - 19, "SUBNODE TELEMETRY // " + string_upper(_cur_sn.sub_type));
        }

        // Subnode Name & Archetype
        var _content_y = _thumb_y + _thumb_h + 8;
        draw_set_color(make_color_rgb(255, 220, 90));
        draw_text(_dos_x + 16, _content_y, string_upper(_cur_sn.name));
        draw_set_color(make_color_rgb(140, 175, 210));
        draw_text(_dos_x + 16, _content_y + 18, string_copy(_sh_layout.stronghold_name, 1, 24) + " // " + _cur_sn.sub_type);'''

assert old_dos_thumb in text, "old_dos_thumb not found"
text = text.replace(old_dos_thumb, new_dos_thumb, 1)

# 5. Update entering stronghold from dossier button
old_btn_enter = '''        var _has_stronghold = (variable_struct_exists(_cur_t, "is_major_stronghold") && _cur_t.is_major_stronghold && _cur_t.region == "EARTH");
        if (_has_stronghold) {
            var _sh_btn_y = _act_y - 74;
            var _sh_btn_hov = (_mx >= _dos_x + 16 && _mx <= _dos_x + 16 + _act_w && _my >= _sh_btn_y && _my <= _sh_btn_y + 32);
            if (_sh_btn_hov && _click) {
                earth_view_mode = "STRONGHOLD";
                active_stronghold_id = _cur_t.id;
                selected_subnode_id = "granite_core";
                scr_audio_play_ui("confirm");
            }
            scr_draw_snes_button(_dos_x + 16, _sh_btn_y, _act_w, 32, "🔍 ENTER BASE THEATER (SEPARATE MAP) >>", _sh_btn_hov, false, make_color_rgb(255, 215, 60));
        }'''

new_btn_enter = '''        var _has_stronghold = (variable_struct_exists(_cur_t, "is_major_stronghold") && _cur_t.is_major_stronghold);
        if (_has_stronghold) {
            var _sh_btn_y = _act_y - 74;
            var _sh_btn_hov = (_mx >= _dos_x + 16 && _mx <= _dos_x + 16 + _act_w && _my >= _sh_btn_y && _my <= _sh_btn_y + 32);
            if (_sh_btn_hov && _click) {
                earth_view_mode = "STRONGHOLD";
                active_stronghold_id = _cur_t.id;
                var _target_sh = scr_stronghold_get_layout(_cur_t.id);
                selected_subnode_id = (array_length(_target_sh.subnodes) > 0) ? _target_sh.subnodes[0].id : "";
                scr_audio_play_ui("confirm");
            }
            scr_draw_snes_button(_dos_x + 16, _sh_btn_y, _act_w, 32, "🔍 ENTER BASE THEATER (SEPARATE MAP) >>", _sh_btn_hov, false, make_color_rgb(255, 215, 60));
        }'''

assert old_btn_enter in text, "old_btn_enter not found"
text = text.replace(old_btn_enter, new_btn_enter, 1)

with open(path, 'w') as f:
    f.write(text)

print("Successfully patched Draw_64.gml with full dynamic stronghold support!")
