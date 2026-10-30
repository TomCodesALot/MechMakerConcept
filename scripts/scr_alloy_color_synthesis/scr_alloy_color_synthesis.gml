/// @description Procedural Metallurgical Color & Chromatic Synthesis Engine
// Generates unique, distinct programmatic colors and physical metallicity for all 118 elements and thousands of custom alloys.
// Adheres to docs/02_alloy_chemistry.md, docs/13_modular_parts_and_assembly_system.md, and docs/14_procedural_materials_and_deep_metallurgy.md

/// @function scr_get_alloy_procedural_color(_alloy_data_or_key, _opt_temp, _opt_pressure)
function scr_get_alloy_procedural_color(_alloy_data_or_key, _opt_temp = 2500, _opt_pressure = 1000) {
    // 1. Direct Known Alloy & Hex Shortcuts
    if (is_string(_alloy_data_or_key)) {
        // Direct Hex Color Support (e.g. "#7387A0" or "7387A0")
        var _hex = _alloy_data_or_key;
        if (string_starts_with(_hex, "#")) _hex = string_delete(_hex, 1, 1);
        if (string_length(_hex) == 6) {
            var _hex_chars = "0123456789ABCDEFabcdef";
            var _is_hex = true;
            for (var c = 1; c <= 6; c++) {
                if (string_pos(string_char_at(_hex, c), _hex_chars) == 0) {
                    _is_hex = false;
                    break;
                }
            }
            if (_is_hex) {
                var _h1 = string_pos(string_upper(string_char_at(_hex, 1)), "0123456789ABCDEF") - 1;
                var _h2 = string_pos(string_upper(string_char_at(_hex, 2)), "0123456789ABCDEF") - 1;
                var _h3 = string_pos(string_upper(string_char_at(_hex, 3)), "0123456789ABCDEF") - 1;
                var _h4 = string_pos(string_upper(string_char_at(_hex, 4)), "0123456789ABCDEF") - 1;
                var _h5 = string_pos(string_upper(string_char_at(_hex, 5)), "0123456789ABCDEF") - 1;
                var _h6 = string_pos(string_upper(string_char_at(_hex, 6)), "0123456789ABCDEF") - 1;
                return make_color_rgb(_h1 * 16 + _h2, _h3 * 16 + _h4, _h5 * 16 + _h6);
            }
        }

        switch (_alloy_data_or_key) {
            case "alloy_vanguard_comp":      return make_color_rgb(115, 135, 160); // Gunmetal Slate with cool steel luster
            case "alloy_hyperion_matrix":    return make_color_rgb(60, 230, 255);  // Cherenkov Neon Plasma Cyan
            case "alloy_aerosteel_flux":     return make_color_rgb(195, 150, 255); // Iridescent Vernier Violet
            case "alloy_adamantine_carbide": return make_color_rgb(255, 155, 60);  // High-Density Heavy Bronze/Amber
            case "alloy_titan_composite":    return make_color_rgb(180, 195, 210); // Silvery Titanium Champagne
            case "alloy_void_glass":         return make_color_rgb(140, 220, 240); // Opaline Crystalline Translucent
            case "alloy_reactive_damascus":  return make_color_rgb(180, 70, 90);   // Damascus Crimson Bronze (#B4465A)
            case "alloy_tachyon_superalloy": return make_color_rgb(100, 240, 255); // Supercharged Tachyon Cyan (#64F0FF)
            case "alloy_lunar_aerogel":      return make_color_rgb(220, 240, 255); // Lunar Aerogel Pale Frost (#DCF0FF)
            case "alloy_sol_ferrite":        return make_color_rgb(230, 180, 40);  // Sol Ferrite Radiant Gold (#E6B428)
            case "item_slag":                return make_color_rgb(65, 55, 50);    // Dull Carbonaceous Slag
            case "mat_tungsten":
            case "tungsten":                 return make_color_rgb(115, 135, 165);
            case "mat_silica_carb":
            case "silica":                   return make_color_rgb(35, 45, 60);
            case "mat_tritium":
            case "tritium":                  return make_color_rgb(0, 245, 255);
            case "mat_syn_flux":
            case "flux":                     return make_color_rgb(255, 175, 40);
        }
    }

    // 2. 118-Element Periodic Table Base RGB Chromatic Vectors
    static _periodic_table_rgb = [
        [0, 245, 255],
        [140, 230, 255],
        [230, 180, 200],
        [190, 210, 215],
        [170, 160, 140],
        [35, 45, 60],
        [90, 140, 220],
        [180, 220, 255],
        [180, 255, 160],
        [255, 80, 60],
        [210, 205, 170],
        [215, 225, 235],
        [210, 220, 230],
        [80, 95, 115],
        [210, 140, 70],
        [230, 210, 50],
        [160, 230, 140],
        [160, 120, 240],
        [195, 190, 210],
        [200, 205, 190],
        [190, 195, 185],
        [220, 230, 245],
        [140, 155, 175],
        [190, 205, 220],
        [150, 140, 155],
        [130, 135, 145],
        [30, 90, 225],
        [185, 190, 175],
        [215, 125, 75],
        [170, 180, 190],
        [175, 190, 210],
        [110, 125, 145],
        [140, 145, 135],
        [130, 95, 100],
        [150, 50, 40],
        [140, 180, 220],
        [210, 185, 200],
        [205, 195, 180],
        [160, 190, 170],
        [175, 185, 195],
        [150, 170, 190],
        [140, 150, 165],
        [180, 160, 190],
        [170, 180, 195],
        [210, 220, 230],
        [195, 205, 215],
        [230, 235, 240],
        [175, 180, 170],
        [185, 195, 210],
        [190, 195, 200],
        [160, 165, 175],
        [150, 155, 160],
        [110, 70, 130],
        [130, 170, 230],
        [205, 190, 140],
        [190, 195, 180],
        [180, 190, 195],
        [185, 180, 170],
        [160, 185, 160],
        [170, 190, 175],
        [185, 45, 240],
        [175, 180, 165],
        [195, 175, 190],
        [180, 185, 175],
        [170, 175, 160],
        [165, 170, 175],
        [175, 165, 170],
        [180, 170, 175],
        [170, 160, 165],
        [190, 185, 175],
        [180, 175, 185],
        [145, 155, 165],
        [135, 145, 160],
        [115, 135, 165],
        [155, 165, 175],
        [95, 115, 145],
        [180, 190, 205],
        [210, 215, 225],
        [255, 205, 50],
        [190, 195, 205],
        [165, 170, 175],
        [110, 115, 125],
        [215, 180, 195],
        [195, 150, 170],
        [140, 90, 110],
        [160, 130, 180],
        [220, 140, 160],
        [210, 220, 200],
        [180, 190, 185],
        [235, 130, 25],
        [170, 160, 155],
        [75, 115, 65],
        [140, 155, 145],
        [165, 145, 130],
        [185, 160, 175],
        [195, 170, 160],
        [180, 155, 170],
        [205, 140, 90],
        [200, 160, 180],
        [190, 150, 170],
        [175, 140, 160],
        [185, 150, 165],
        [170, 145, 155],
        [155, 135, 145],
        [145, 130, 140],
        [135, 125, 135],
        [140, 120, 130],
        [125, 110, 125],
        [130, 115, 130],
        [135, 120, 135],
        [220, 180, 60],
        [160, 175, 190],
        [170, 160, 180],
        [120, 190, 220],
        [180, 140, 165],
        [165, 135, 155],
        [150, 110, 130],
        [140, 220, 240]
    ];

    // 3. Procedural Chromatic Synthesis for Custom / Infinite Compositions
    var _tot_w = 0.0;
    var _sum_r = 0.0;
    var _sum_g = 0.0;
    var _sum_b = 0.0;

    if (is_struct(_alloy_data_or_key)) {
        var _keys = variable_struct_get_names(_alloy_data_or_key);
        for (var k = 0; k < array_length(_keys); k++) {
            var _kname = _keys[k];
            var _qty = variable_struct_get(_alloy_data_or_key, _kname);
            if (!is_numeric(_qty) || _qty <= 0) continue;

            var _er = 128;
            var _eg = 128;
            var _eb = 128;
            var _matched_periodic = false;

            // Check if key is a 118-element periodic ID (e.g. "mat_074_w")
            if (string_starts_with(_kname, "mat_") && string_length(_kname) >= 7) {
                var _num_str = string_copy(_kname, 5, 3);
                if (string_length(string_digits(_num_str)) == 3) {
                    var _atomic_num = real(_num_str);
                    if (_atomic_num >= 1 && _atomic_num <= 118) {
                        var _rgb_entry = _periodic_table_rgb[_atomic_num - 1];
                        _er = _rgb_entry[0];
                        _eg = _rgb_entry[1];
                        _eb = _rgb_entry[2];
                        _matched_periodic = true;
                    }
                }
            }

            if (!_matched_periodic) {
                // Legacy & Semantic Element Fallbacks
                switch (_kname) {
                    case "mat_tungsten":
                    case "tungsten":
                        _er = 115; _eg = 135; _eb = 165; break; // W (74) Slate Blue-Gray
                    case "mat_silica_carb":
                    case "silica":
                    case "carbon":
                        _er = 35;  _eg = 45;  _eb = 60;  break; // C (6) Deep Obsidian
                    case "mat_tritium":
                    case "tritium":
                        _er = 0;   _eg = 245; _eb = 255; break; // H (1) Cherenkov Cyan
                    case "mat_syn_flux":
                    case "flux":
                        _er = 255; _eg = 175; _eb = 40;  break; // Amber Gold Catalyst
                    case "mat_titanium":
                    case "titanium":
                        _er = 220; _eg = 230; _eb = 245; break; // Ti (22) Champagne Silver
                    case "mat_cobalt":
                    case "cobalt":
                        _er = 30;  _eg = 90;  _eb = 225; break; // Co (27) Royal Azure
                    case "mat_osmium":
                    case "osmium":
                        _er = 95;  _eg = 115; _eb = 145; break; // Os (76) Bluish Platinum
                    case "mat_graphene":
                    case "graphene":
                        _er = 25;  _eg = 30;  _eb = 38;  break; // Matte Charcoal
                    case "mat_deuterium":
                    case "deuterium":
                        _er = 40;  _eg = 160; _eb = 255; break; // Ion Electric Blue
                    case "mat_promethium":
                    case "promethium":
                        _er = 185; _eg = 45;  _eb = 240; break; // Pm (61) Ion Magenta
                    case "mat_thorium":
                    case "thorium":
                        _er = 235; _eg = 130; _eb = 25;  break; // Th (90) Toxic Amber
                    case "mat_void_glass":
                    case "void_glass":
                        _er = 160; _eg = 225; _eb = 240; break; // Opalescent Cyan
                    case "slag":
                        _er = 65;  _eg = 55;  _eb = 50;  break; // Slag Gray
                    default:
                        // Deterministic Hash Fallback
                        var _hash_val = 0;
                        for (var c = 1; c <= string_length(_kname); c++) {
                            _hash_val = (_hash_val * 31 + string_byte_at(_kname, c)) mod 256;
                        }
                        var _hsv_col = make_color_hsv(_hash_val, 160, 200);
                        _er = color_get_red(_hsv_col);
                        _eg = color_get_green(_hsv_col);
                        _eb = color_get_blue(_hsv_col);
                        break;
                }
            }

            _sum_r += _er * _qty;
            _sum_g += _eg * _qty;
            _sum_b += _eb * _qty;
            _tot_w += _qty;
        }
    }

    if (_tot_w <= 0.0) return make_color_rgb(128, 128, 128);

    var _r = _sum_r / _tot_w;
    var _g = _sum_g / _tot_w;
    var _b = _sum_b / _tot_w;

    // Thermal Incandescent Shift: Higher smelting temperatures introduce glowing orange/gold tones
    var _heat_factor = clamp((_opt_temp - 1500) / 4500.0, 0.0, 0.40);
    _r = lerp(_r, 255, _heat_factor * 0.45);
    _g = lerp(_g, 210, _heat_factor * 0.25);

    // Pressure Densification Shift: High pressure densifies crystal matrix, deepening and saturating tones
    var _press_factor = clamp(_opt_pressure / 8500.0, 0.0, 0.35);
    _r = clamp(_r * (1.0 - _press_factor * 0.20), 12, 255);
    _g = clamp(_g * (1.0 - _press_factor * 0.15), 12, 255);
    _b = clamp(_b * (1.0 - _press_factor * 0.10), 12, 255);

    return make_color_rgb(floor(_r), floor(_g), floor(_b));
}

/// @function scr_alloy_get_hex(_alloy_data_or_key)
function scr_alloy_get_hex(_alloy_data_or_key) {
    if (is_string(_alloy_data_or_key) && string_starts_with(_alloy_data_or_key, "#") && string_length(_alloy_data_or_key) == 7) {
        return _alloy_data_or_key;
    }
    var _c = scr_get_alloy_procedural_color(_alloy_data_or_key);
    var _r = color_get_red(_c);
    var _g = color_get_green(_c);
    var _b = color_get_blue(_c);
    
    var _hex_chars = "0123456789ABCDEF";
    var _h_r = string_char_at(_hex_chars, (_r div 16) + 1) + string_char_at(_hex_chars, (_r mod 16) + 1);
    var _h_g = string_char_at(_hex_chars, (_g div 16) + 1) + string_char_at(_hex_chars, (_g mod 16) + 1);
    var _h_b = string_char_at(_hex_chars, (_b div 16) + 1) + string_char_at(_hex_chars, (_b mod 16) + 1);
    return "#" + _h_r + _h_g + _h_b;
}

/// @function scr_draw_alloy_swatch(_x, _y, _w, _h, _alloy_data_or_key, _label)
function scr_draw_alloy_swatch(_x, _y, _w, _h, _alloy_data_or_key, _label = "") {
    var _base_col = scr_get_alloy_procedural_color(_alloy_data_or_key);
    var _hex_str = scr_alloy_get_hex(_alloy_data_or_key);

    // Metallic Outer Bezel
    draw_set_color(make_color_rgb(25, 32, 42));
    draw_rectangle(_x, _y, _x + _w, _y + _h, false);

    // Ingot Core Fill with Procedural Alloy Color
    draw_set_color(_base_col);
    draw_rectangle(_x + 2, _y + 2, _x + _w - 2, _y + _h - 2, false);

    // Top Specular Highlight Line
    draw_set_color(c_white);
    draw_set_alpha(0.35);
    draw_line(_x + 3, _y + 3, _x + _w - 3, _y + 3);
    draw_line(_x + 3, _y + 4, _x + _w - 3, _y + 4);

    // Bottom Ambient Shadow Line
    draw_set_color(c_black);
    draw_set_alpha(0.40);
    draw_line(_x + 3, _y + _h - 3, _x + _w - 3, _y + _h - 3);
    draw_set_alpha(1.0);

    // Outer Crisp Border
    draw_set_color(make_color_rgb(70, 95, 125));
    draw_rectangle(_x, _y, _x + _w, _y + _h, true);

    // Optional Label Text Below or Inside
    if (_label != "") {
        draw_set_color(c_white);
        draw_text(_x + _w + 8, _y + (_h / 2) - 7, _label + " (" + _hex_str + ")");
    }
}
