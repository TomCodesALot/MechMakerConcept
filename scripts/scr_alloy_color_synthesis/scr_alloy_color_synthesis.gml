/// @description Procedural Metallurgical Color & Chromatic Synthesis Engine
// Generates unique, distinct programmatic colors and physical metallicity for thousands of alloy formulas.
// Adheres to docs/02_alloy_chemistry.md and docs/13_modular_parts_and_assembly_system.md

/// @function scr_get_alloy_procedural_color(_alloy_data_or_key, _opt_temp, _opt_pressure)
function scr_get_alloy_procedural_color(_alloy_data_or_key, _opt_temp = 2500, _opt_pressure = 1000) {
    // 1. Direct Known Alloy Shortcuts
    if (is_string(_alloy_data_or_key)) {
        switch (_alloy_data_or_key) {
            case "alloy_vanguard_comp":     return make_color_rgb(115, 135, 160); // Gunmetal Slate with cool steel luster
            case "alloy_hyperion_matrix":   return make_color_rgb(60, 230, 255);  // Cherenkov Neon Plasma Cyan
            case "alloy_aerosteel_flux":    return make_color_rgb(195, 150, 255); // Iridescent Vernier Violet
            case "alloy_adamantine_carbide": return make_color_rgb(255, 155, 60);  // High-Density Heavy Bronze/Amber
            case "item_slag":               return make_color_rgb(65, 55, 50);    // Dull Carbonaceous Slag
        }
    }

    // 2. Procedural Chromatic Synthesis for Custom / Infinite Compositions
    // Element Spectral Chromatic Weights:
    // Tungsten (W): Slate Blue-Gray (120, 135, 160)
    // Silica-Carbon (C): Deep Obsidian (35, 45, 60)
    // Tritium (Tr): Vibrant Plasma Cyan (0, 245, 255)
    // Synthetic Flux (Fx): Radiant Amber Gold (255, 175, 40)
    // Titanium (Ti): Silvery Champagne (225, 230, 240)
    
    var _w = 0;
    var _c = 0;
    var _tr = 0;
    var _fx = 0;

    if (is_struct(_alloy_data_or_key)) {
        _w  = variable_struct_exists(_alloy_data_or_key, "mat_tungsten")    ? _alloy_data_or_key.mat_tungsten : (_alloy_data_or_key[$ "tungsten"] ?? 0);
        _c  = variable_struct_exists(_alloy_data_or_key, "mat_silica_carb") ? _alloy_data_or_key.mat_silica_carb : (_alloy_data_or_key[$ "silica"] ?? 0);
        _tr = variable_struct_exists(_alloy_data_or_key, "mat_tritium")     ? _alloy_data_or_key.mat_tritium : (_alloy_data_or_key[$ "tritium"] ?? 0);
        _fx = variable_struct_exists(_alloy_data_or_key, "mat_syn_flux")    ? _alloy_data_or_key.mat_syn_flux : (_alloy_data_or_key[$ "flux"] ?? 0);
    }

    var _total_parts = _w + _c + _tr + _fx;
    if (_total_parts <= 0) return make_color_rgb(128, 128, 128);

    // Weighted additive spectrum
    var _r = (_w * 120.0 + _c * 35.0 + _tr * 10.0 + _fx * 255.0) / _total_parts;
    var _g = (_w * 135.0 + _c * 45.0 + _tr * 240.0 + _fx * 175.0) / _total_parts;
    var _b = (_w * 165.0 + _c * 65.0 + _tr * 255.0 + _fx * 40.0) / _total_parts;

    // Thermal & Pressure Shifts:
    // High heat adds incandescent gold/orange tone
    var _heat_factor = clamp((_opt_temp - 1500) / 4000.0, 0.0, 0.4);
    _r = lerp(_r, 255, _heat_factor * 0.4);
    _g = lerp(_g, 200, _heat_factor * 0.2);

    // High pressure densifies and saturates the crystal structure
    var _press_factor = clamp(_opt_pressure / 8000.0, 0.0, 0.35);
    _r = clamp(_r * (1.0 - _press_factor * 0.2), 15, 255);
    _g = clamp(_g * (1.0 - _press_factor * 0.15), 15, 255);
    _b = clamp(_b * (1.0 - _press_factor * 0.1), 15, 255);

    return make_color_rgb(floor(_r), floor(_g), floor(_b));
}

/// @function scr_alloy_get_hex(_alloy_data_or_key)
function scr_alloy_get_hex(_alloy_data_or_key) {
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
