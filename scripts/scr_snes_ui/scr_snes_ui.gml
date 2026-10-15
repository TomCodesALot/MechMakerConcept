/// @description 16-Bit Super Nintendo UI Rendering Engine (Front Mission SNES & Gihren's Greed)
/// Provides authentic 16-bit militaristic beveled panels, tactile mechanical push-buttons,
/// discrete segmented LED tick gauges, stamped folder tabs, hazard warning trims, and CRT scanlines.

/// @function scr_draw_snes_panel(_x, _y, _w, _h, _title, _accent_col, _has_rivets, _scanline_alpha)
/// @description Draws a heavy 16-bit industrial metal console panel with 3D bevels, rivets, and CRT scanlines.
function scr_draw_snes_panel(_x, _y, _w, _h, _title = "", _accent_col = -1, _has_rivets = true, _scanline_alpha = 0.05) {
    // 1. Outer deep drop-border
    draw_set_color(make_color_rgb(8, 11, 16));
    draw_rectangle(_x, _y, _x + _w, _y + _h, false);

    // 2. Specular Top & Left 3D Bevel Ridge (16-bit metallic rim)
    draw_set_color(make_color_rgb(122, 144, 168));
    draw_line(_x + 1, _y + 1, _x + _w - 1, _y + 1);
    draw_line(_x + 1, _y + 1, _x + 1, _y + _h - 1);
    draw_set_color(make_color_rgb(160, 185, 210));
    draw_point(_x + 2, _y + 2); // Specular glint

    // 3. Recessed Bottom & Right 3D Shadow
    draw_set_color(make_color_rgb(14, 20, 28));
    draw_line(_x + 1, _y + _h - 1, _x + _w - 1, _y + _h - 1);
    draw_line(_x + _w - 1, _y + 1, _x + _w - 1, _y + _h - 1);

    // 4. Panel Console Surface (Deep Front Mission slate)
    draw_set_color(make_color_rgb(20, 27, 36));
    draw_rectangle(_x + 2, _y + 2, _x + _w - 2, _y + _h - 2, false);

    // 5. Inner Secondary Bezel
    draw_set_color(make_color_rgb(32, 44, 58));
    draw_rectangle(_x + 4, _y + 4, _x + _w - 4, _y + _h - 4, true);

    // 6. CRT Phosphor Horizontal Scanlines
    if (_scanline_alpha > 0) {
        draw_set_color(make_color_rgb(4, 8, 12));
        draw_set_alpha(_scanline_alpha);
        for (var sl = _y + 4; sl < _y + _h - 4; sl += 2) {
            draw_line(_x + 4, sl, _x + _w - 4, sl);
        }
        draw_set_alpha(1.0);
    }

    // 7. Corner Brackets & Hex Rivets
    if (_has_rivets) {
        if (sprite_exists(spr_snes_panel_corner)) {
            draw_sprite(spr_snes_panel_corner, 0, _x, _y);
            draw_sprite(spr_snes_panel_corner, 1, _x + _w - 32, _y);
            draw_sprite(spr_snes_panel_corner, 2, _x, _y + _h - 32);
            draw_sprite(spr_snes_panel_corner, 3, _x + _w - 32, _y + _h - 32);
        } else {
            // Procedural 16-bit hex rivets
            var _rx = [_x + 7, _x + _w - 8, _x + 7, _x + _w - 8];
            var _ry = [_y + 7, _y + 7, _y + _h - 8, _y + _h - 8];
            for (var r = 0; r < 4; r++) {
                draw_set_color(make_color_rgb(10, 14, 20));
                draw_rectangle(_rx[r] - 2, _ry[r] - 2, _rx[r] + 2, _ry[r] + 2, false);
                draw_set_color(make_color_rgb(130, 150, 175));
                draw_rectangle(_rx[r] - 1, _ry[r] - 1, _rx[r] + 1, _ry[r] + 1, false);
                draw_set_color(make_color_rgb(220, 240, 255));
                draw_point(_rx[r] - 1, _ry[r] - 1);
            }
        }
    }

    // 8. Stamped Military Title Header Bar
    if (_title != "") {
        var _th_x = _x + 10;
        var _th_y = _y + 8;
        var _th_w = _w - 20;
        var _th_h = 24;

        // Recessed header plate
        draw_set_color(make_color_rgb(12, 17, 24));
        draw_rectangle(_th_x, _th_y, _th_x + _th_w, _th_y + _th_h, false);
        draw_set_color(make_color_rgb(45, 62, 82));
        draw_rectangle(_th_x, _th_y, _th_x + _th_w, _th_y + _th_h, true);

        // Accent indicator notch
        var _acc = (_accent_col != -1) ? _accent_col : make_color_rgb(80, 190, 255);
        draw_set_color(_acc);
        draw_rectangle(_th_x + 2, _th_y + 2, _th_x + 6, _th_y + _th_h - 2, false);

        // LED Indicator if available
        if (sprite_exists(spr_snes_led_indicators)) {
            draw_sprite(spr_snes_led_indicators, 0, _th_x + 12, _th_y + 4);
            draw_set_color(c_white);
            draw_text(_th_x + 34, _th_y + 4, "[ " + string_upper(_title) + " ]");
        } else {
            draw_set_color(c_white);
            draw_text(_th_x + 14, _th_y + 4, "[ " + string_upper(_title) + " ]");
        }

        // Right-side military terminal telemetry
        draw_set_color(make_color_rgb(120, 145, 170));
        draw_text(_th_x + _th_w - 180, _th_y + 4, "TAC-COM // 16-BIT SYS");
    }
}

/// @function scr_draw_snes_button(_x, _y, _w, _h, _text, _hovered, _active, _accent_col, _subtext)
/// @description Draws a physical 16-bit push button with tactile raised/depressed bevels and phosphor hover glow.
function scr_draw_snes_button(_x, _y, _w, _h, _text, _hovered, _active, _accent_col = -1, _subtext = "") {
    var _offset = _active ? 1 : 0;
    var _acc = (_accent_col != -1) ? _accent_col : make_color_rgb(255, 180, 50);

    // Outer dark housing
    draw_set_color(make_color_rgb(8, 12, 16));
    draw_rectangle(_x, _y, _x + _w, _y + _h, false);

    if (_active) {
        // Inverted depressed bevel (button physically sunk into console)
        draw_set_color(make_color_rgb(10, 14, 18));
        draw_line(_x + 1, _y + 1, _x + _w - 1, _y + 1);
        draw_line(_x + 1, _y + 1, _x + 1, _y + _h - 1);
        draw_set_color(make_color_rgb(60, 78, 98));
        draw_line(_x + 1, _y + _h - 1, _x + _w - 1, _y + _h - 1);
        draw_line(_x + _w - 1, _y + 1, _x + _w - 1, _y + _h - 1);
        // Sunken button face
        draw_set_color(make_color_rgb(20, 28, 38));
        draw_rectangle(_x + 2, _y + 2, _x + _w - 2, _y + _h - 2, false);
    } else if (_hovered) {
        // Raised 3D button with phosphor glow
        draw_set_color(_acc);
        draw_rectangle(_x + 1, _y + 1, _x + _w - 1, _y + _h - 1, true);
        // Specular highlight
        draw_set_color(make_color_rgb(190, 220, 250));
        draw_line(_x + 2, _y + 2, _x + _w - 2, _y + 2);
        draw_line(_x + 2, _y + 2, _x + 2, _y + _h - 2);
        // Drop shadow
        draw_set_color(make_color_rgb(12, 16, 22));
        draw_line(_x + 2, _y + _h - 2, _x + _w - 2, _y + _h - 2);
        draw_line(_x + _w - 2, _y + 2, _x + _w - 2, _y + _h - 2);
        // Brightened face
        draw_set_color(make_color_rgb(38, 52, 70));
        draw_rectangle(_x + 3, _y + 3, _x + _w - 3, _y + _h - 3, false);
    } else {
        // Standard raised 16-bit push button
        draw_set_color(make_color_rgb(115, 138, 162));
        draw_line(_x + 1, _y + 1, _x + _w - 1, _y + 1);
        draw_line(_x + 1, _y + 1, _x + 1, _y + _h - 1);
        draw_set_color(make_color_rgb(12, 16, 22));
        draw_line(_x + 1, _y + _h - 1, _x + _w - 1, _y + _h - 1);
        draw_line(_x + _w - 1, _y + 1, _x + _w - 1, _y + _h - 1);
        // Gunmetal face
        draw_set_color(make_color_rgb(28, 38, 50));
        draw_rectangle(_x + 2, _y + 2, _x + _w - 2, _y + _h - 2, false);
        draw_set_color(make_color_rgb(44, 60, 80));
        draw_rectangle(_x + 2, _y + 2, _x + _w - 2, _y + _h - 2, true);
    }

    // Left Cursor Arrow indicator when hovered
    if (_hovered) {
        draw_set_color(_acc);
        draw_text(_x + 6 + _offset, _y + floor((_h - 16) / 2) + _offset, ">");
    }

    // Text label (shifted +1px when active)
    var _tx = _hovered ? (_x + 18 + _offset) : (_x + 12 + _offset);
    var _ty = _y + floor((_h - 16) / 2) + _offset;

    draw_set_color(_hovered ? c_white : (_active ? make_color_rgb(220, 240, 255) : make_color_rgb(190, 215, 235)));
    draw_text(_tx, _ty, _text);

    if (_subtext != "") {
        draw_set_color(make_color_rgb(130, 160, 185));
        draw_text(_tx, _ty + 14, _subtext);
    }
}

/// @function scr_draw_snes_gauge(_x, _y, _w, _h, _val, _max, _fill_col, _empty_col, _segment_w)
/// @description Draws a Front Mission 16-bit discrete segmented LED tick gauge.
function scr_draw_snes_gauge(_x, _y, _w, _h, _val, _max, _fill_col = c_lime, _empty_col = -1, _segment_w = 6) {
    // 1. Recessed dark housing
    draw_set_color(make_color_rgb(8, 12, 16));
    draw_rectangle(_x, _y, _x + _w, _y + _h, false);
    draw_set_color(make_color_rgb(36, 48, 64));
    draw_rectangle(_x, _y, _x + _w, _y + _h, true);

    // Inner shadow bevel
    draw_set_color(make_color_rgb(5, 7, 10));
    draw_line(_x + 1, _y + 1, _x + _w - 1, _y + 1);
    draw_line(_x + 1, _y + 1, _x + 1, _y + _h - 1);

    // 2. Calculate Discrete LED Segments
    var _gap = 2;
    var _step = _segment_w + _gap;
    var _inner_w = _w - 4;
    var _inner_h = _h - 4;
    var _total_segs = max(1, floor(_inner_w / _step));
    var _norm = clamp(_val / max(_max, 0.001), 0, 1);
    var _lit_segs = round(_norm * _total_segs);

    var _e_col = (_empty_col != -1) ? _empty_col : make_color_rgb(20, 28, 38);

    // 3. Render Segments
    for (var s = 0; s < _total_segs; s++) {
        var _sx = _x + 2 + s * _step;
        var _sy = _y + 2;
        var _is_lit = (s < _lit_segs);

        if (_is_lit) {
            // Main illuminated LED block
            draw_set_color(_fill_col);
            draw_rectangle(_sx, _sy, _sx + _segment_w - 1, _sy + _inner_h - 1, false);

            // Specular top highlight (brightened LED rim)
            draw_set_color(c_white);
            draw_set_alpha(0.5);
            draw_line(_sx, _sy, _sx + _segment_w - 1, _sy);
            draw_set_alpha(1.0);

            // Bottom shadow line
            draw_set_color(make_color_rgb(0, 0, 0));
            draw_set_alpha(0.4);
            draw_line(_sx, _sy + _inner_h - 1, _sx + _segment_w - 1, _sy + _inner_h - 1);
            draw_set_alpha(1.0);
        } else {
            // Inactive unlit LED slot
            draw_set_color(_e_col);
            draw_rectangle(_sx, _sy, _sx + _segment_w - 1, _sy + _inner_h - 1, false);
            draw_set_color(make_color_rgb(10, 14, 20));
            draw_rectangle(_sx, _sy, _sx + _segment_w - 1, _sy + _inner_h - 1, true);
        }

        // Tick scale every 5th segment
        if (s % 5 == 0 && s > 0) {
            draw_set_color(make_color_rgb(60, 80, 105));
            draw_point(_sx - 1, _y - 1);
            draw_point(_sx - 1, _y + _h + 1);
        }
    }
}

/// @function scr_draw_snes_header_tab(_x, _y, _w, _h, _text, _is_active, _is_hovered, _badge_text)
/// @description Draws a stamped 16-bit tactical military index tab.
function scr_draw_snes_header_tab(_x, _y, _w, _h, _text, _is_active, _is_hovered, _badge_text = "") {
    // Outer shadow
    draw_set_color(make_color_rgb(8, 12, 16));
    draw_rectangle(_x, _y, _x + _w, _y + _h, false);

    if (_is_active) {
        // Raised Active Tab
        draw_set_color(make_color_rgb(32, 54, 80));
        draw_rectangle(_x + 1, _y + 1, _x + _w - 1, _y + _h, false);

        // Bright top highlight
        draw_set_color(make_color_rgb(120, 190, 255));
        draw_line(_x + 2, _y + 1, _x + _w - 2, _y + 1);
        draw_line(_x + 1, _y + 2, _x + 1, _y + _h);
        draw_line(_x + _w - 1, _y + 2, _x + _w - 1, _y + _h);

        // Tactical amber indicator bar across the bottom
        draw_set_color(make_color_rgb(255, 185, 50));
        draw_rectangle(_x + 2, _y + _h - 3, _x + _w - 2, _y + _h, false);

        // LED indicator pip
        if (sprite_exists(spr_snes_led_indicators)) {
            draw_sprite(spr_snes_led_indicators, 0, _x + 8, _y + floor((_h - 16) / 2));
        }

        // Active crisp white text
        draw_set_color(c_white);
        draw_text(_x + 28, _y + floor((_h - 16) / 2), _text);
    } else if (_is_hovered) {
        // Hovered Tab
        draw_set_color(make_color_rgb(24, 38, 54));
        draw_rectangle(_x + 1, _y + 1, _x + _w - 1, _y + _h, false);

        // Tactical amber rim
        draw_set_color(make_color_rgb(240, 180, 60));
        draw_rectangle(_x + 1, _y + 1, _x + _w - 1, _y + _h, true);

        // Hover text
        draw_set_color(make_color_rgb(230, 240, 255));
        draw_text(_x + 16, _y + floor((_h - 16) / 2), _text);
    } else {
        // Inactive Tab
        draw_set_color(make_color_rgb(16, 22, 30));
        draw_rectangle(_x + 1, _y + 1, _x + _w - 1, _y + _h, false);
        draw_set_color(make_color_rgb(36, 48, 64));
        draw_rectangle(_x + 1, _y + 1, _x + _w - 1, _y + _h, true);

        // Inactive text
        draw_set_color(make_color_rgb(130, 155, 180));
        draw_text(_x + 16, _y + floor((_h - 16) / 2), _text);
    }

    // Optional Badge Count (e.g. "[3]")
    if (_badge_text != "") {
        draw_set_color(make_color_rgb(255, 210, 60));
        draw_text(_x + _w - 40, _y + floor((_h - 16) / 2), _badge_text);
    }
}

/// @function scr_draw_snes_hazard_bar(_x, _y, _w, _h, _is_warning)
/// @description Draws a repeating 16-bit diagonal caution/warning hazard strip.
function scr_draw_snes_hazard_bar(_x, _y, _w, _h, _is_warning = false) {
    var _fr = _is_warning ? 1 : 0;
    if (sprite_exists(spr_snes_hazard_stripe)) {
        var _sw = 64;
        var _steps = ceil(_w / _sw);
        for (var i = 0; i < _steps; i++) {
            var _draw_w = min(_sw, _w - (i * _sw));
            draw_sprite_part(spr_snes_hazard_stripe, _fr, 0, 0, _draw_w, min(16, _h), _x + (i * _sw), _y);
        }
    } else {
        draw_set_color(_is_warning ? c_orange : c_yellow);
        draw_rectangle(_x, _y, _x + _w, _y + _h, false);
    }
}

/// @function scr_draw_snes_faction_crest(_x, _y, _size, _faction_id)
/// @description Draws the 16-bit military crest for the respective faction with beveled badge backer.
function scr_draw_snes_faction_crest(_x, _y, _size, _faction_id) {
    var _frame = 0;
    if (_faction_id == "faction_terran" || _faction_id == "terran") _frame = 0;
    else if (_faction_id == "faction_colony" || _faction_id == "colony") _frame = 1;
    else if (_faction_id == "faction_syndicate" || _faction_id == "syndicate") _frame = 2;
    else if (_faction_id == "faction_zaibatsu" || _faction_id == "zaibatsu") _frame = 3;

    if (sprite_exists(spr_snes_faction_crests)) {
        var _spr_w = sprite_get_width(spr_snes_faction_crests);
        var _scale = _size / _spr_w;
        draw_sprite_ext(spr_snes_faction_crests, _frame, _x, _y, _scale, _scale, 0, c_white, 1.0);
    }
}

/// @function scr_draw_snes_crt_overlay(_x, _y, _w, _h, _alpha)
/// @description Draws an authentic CRT monitor scanline raster overlay.
function scr_draw_snes_crt_overlay(_x, _y, _w, _h, _alpha = 0.06) {
    draw_set_color(make_color_rgb(0, 4, 8));
    draw_set_alpha(_alpha);
    for (var sl = _y; sl < _y + _h; sl += 2) {
        draw_line(_x, sl, _x + _w, sl);
    }
    draw_set_alpha(1.0);
}

/// @function scr_draw_snes_window_modal(_x, _y, _w, _h, _title, _subtitle)
/// @description Draws a heavy 16-bit modal briefing dialog window.
function scr_draw_snes_window_modal(_x, _y, _w, _h, _title, _subtitle = "") {
    // Backdrop shadow / dimming
    draw_set_color(c_black);
    draw_set_alpha(0.65);
    draw_rectangle(0, 0, display_get_gui_width(), display_get_gui_height(), false);
    draw_set_alpha(1.0);

    // Main beveled chassis
    scr_draw_snes_panel(_x, _y, _w, _h, _title, make_color_rgb(255, 190, 50), true, 0.08);

    // Hazard warning strip below title
    scr_draw_snes_hazard_bar(_x + 10, _y + 34, _w - 20, 6, false);

    if (_subtitle != "") {
        draw_set_color(make_color_rgb(160, 195, 225));
        draw_text(_x + 16, _y + 44, _subtitle);
    }
}

/// @function scr_draw_snes_trial_stamp(_x, _y, _stamp_idx)
/// @description Draws a stamped 16-bit evaluation badge (Grade S, A, Conditional, Rejected, Modernized, Tooling).
function scr_draw_snes_trial_stamp(_x, _y, _stamp_idx) {
    if (sprite_exists(spr_snes_trial_stamps)) {
        draw_sprite(spr_snes_trial_stamps, clamp(_stamp_idx, 0, 5), _x, _y);
    } else {
        draw_set_color(make_color_rgb(14, 24, 36));
        draw_rectangle(_x, _y, _x + 84, _y + 26, false);
        draw_set_color(make_color_rgb(100, 220, 255));
        draw_rectangle(_x, _y, _x + 84, _y + 26, true);
        draw_text(_x + 6, _y + 6, "STAMP #" + string(_stamp_idx));
    }
}
