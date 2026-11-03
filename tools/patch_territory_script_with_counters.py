import os

target = "scripts/scr_territory_war_system/scr_territory_war_system.gml"
with open(target, "r", encoding="utf-8") as f:
    code = f.read()

helper_code = '''

// =========================================================================
// SHIN GIHREN\'S GREED TACTICAL COUNTER SYSTEM (Doc 39 / Art Suite)
// =========================================================================

/// @function scr_territory_get_garrison_spec(_t)
/// @description Returns unit sprite, stack count, and tactical designation for a territory
function scr_territory_get_garrison_spec(_t) {
    var _spec = {
        unit_sprite_name: "spr_mini_ms_ironclad",
        stack_count: 4,
        unit_label: "Heavy Mobile Suit"
    };
    if (is_undefined(_t)) return _spec;
    
    var _fac = _t.controlling_faction;
    var _def = variable_struct_exists(_t, "defense_rating") ? _t.defense_rating : 75;
    
    if (_fac == "faction_a") {
        if (_t.region == "EARTH") {
            _spec.unit_sprite_name = "spr_mini_veh_heavy_tank";
            _spec.stack_count = max(4, floor(_def / 11));
            _spec.unit_label = "MB-88 Goliath Tanks";
        } else {
            _spec.unit_sprite_name = "spr_mini_ms_ironclad";
            _spec.stack_count = max(3, floor(_def / 14));
            _spec.unit_label = "GHA-07 Ironclad MS";
        }
    } else if (_fac == "faction_b") {
        if (_t.region == "EARTH") {
            _spec.unit_sprite_name = "spr_mini_veh_gunship";
            _spec.stack_count = max(3, floor(_def / 13));
            _spec.unit_label = "SV-13 Wyvern Gunships";
        } else {
            _spec.unit_sprite_name = "spr_mini_ms_aerostriker";
            _spec.stack_count = max(3, floor(_def / 14));
            _spec.unit_label = "Aero-Striker Wings";
        }
    } else if (_fac == "faction_c") {
        if (_t.region == "EARTH") {
            _spec.unit_sprite_name = "spr_mini_veh_technical";
            _spec.stack_count = max(4, floor(_def / 10));
            _spec.unit_label = "ATV-4 Recon Technicals";
        } else {
            _spec.unit_sprite_name = "spr_mini_ms_artillery";
            _spec.stack_count = max(2, floor(_def / 16));
            _spec.unit_label = "Mammoth-Tread Siege MS";
        }
    } else if (_fac == "faction_d") {
        _spec.unit_sprite_name = "spr_mini_ms_hoversniper";
        _spec.stack_count = max(3, floor(_def / 15));
        _spec.unit_label = "Specter Hover Railguns";
    } else if (_fac == "faction_e") {
        if (_t.region == "EARTH") {
            _spec.unit_sprite_name = "spr_mini_inf_exo_squad";
            _spec.stack_count = max(4, floor(_def / 10));
            _spec.unit_label = "Exo-Shock Troopers";
        } else {
            _spec.unit_sprite_name = "spr_mini_veh_dropship";
            _spec.stack_count = max(2, floor(_def / 18));
            _spec.unit_label = "Skyhook Fleet Escorts";
        }
    } else if (_fac == "faction_f") {
        _spec.unit_sprite_name = "spr_mini_ms_commander";
        _spec.stack_count = max(3, floor(_def / 12));
        _spec.unit_label = "Autonomous Hegemon MS";
    } else if (_fac == "pmc") {
        _spec.unit_sprite_name = "spr_mini_ms_grunt";
        _spec.stack_count = max(4, floor(_def / 12));
        _spec.unit_label = "Iron Ridge Custom Lance";
    }
    
    return _spec;
}

/// @function scr_draw_tactical_counter(_cx, _cy, _faction_id, _unit_spr_name, _stack_count, _is_selected, _is_hover, _scale)
/// @description Draws a Shin Gihren\'s Greed style tactical unit counter with hex plinth, unit sprite, and stack count
function scr_draw_tactical_counter(_cx, _cy, _faction_id, _unit_spr_name, _stack_count, _is_selected, _is_hover, _scale) {
    if (is_undefined(_scale)) _scale = 1.0;
    
    // 1. Determine Hex Base Plinth
    var _base_spr = spr_hex_base_pmc;
    if (_faction_id == "faction_a") _base_spr = spr_hex_base_terran;
    else if (_faction_id == "faction_b") _base_spr = spr_hex_base_colony;
    else if (_faction_id == "faction_c") _base_spr = spr_hex_base_syndicate;
    else if (_faction_id == "faction_d") _base_spr = spr_hex_base_zaibatsu;
    else if (_faction_id == "faction_e") _base_spr = spr_hex_base_sidereal;
    else if (_faction_id == "faction_f") _base_spr = spr_hex_base_mars;
    else if (_faction_id == "pmc") _base_spr = spr_hex_base_pmc;
    
    // 2. Base Dimensions
    var _bw = floor(46 * _scale);
    var _bh = floor(34 * _scale);
    
    // Hover Glow Ring
    if (_is_hover) {
        draw_set_color(c_white);
        draw_set_alpha(0.35);
        draw_ellipse(_cx - 24 * _scale, _cy - 10 * _scale, _cx + 24 * _scale, _cy + 14 * _scale, false);
        draw_set_alpha(1.0);
    }
    
    // Draw Base Plinth
    if (sprite_exists(_base_spr)) {
        draw_sprite_stretched(_base_spr, 0, _cx - _bw/2, _cy - _bh/2 + floor(4 * _scale), _bw, _bh);
    }
    
    // 3. Unit Miniature Sprite
    var _u_spr = asset_get_index(_unit_spr_name);
    if (_u_spr == -1 || !sprite_exists(_u_spr)) {
        _u_spr = spr_mini_ms_ironclad;
    }
    
    var _uw = floor(44 * _scale);
    var _uh = floor(44 * _scale);
    if (sprite_exists(_u_spr)) {
        draw_sprite_stretched(_u_spr, 0, _cx - _uw/2, _cy - _uh + floor(8 * _scale), _uw, _uh);
    }
    
    // 4. Digital Stack Numeral Badge
    var _badge_w = floor(14 * _scale);
    var _badge_h = floor(16 * _scale);
    var _badge_x = _cx + floor(8 * _scale);
    var _badge_y = _cy + floor(2 * _scale);
    
    draw_set_color(make_color_rgb(10, 16, 26));
    draw_rectangle(_badge_x, _badge_y, _badge_x + _badge_w, _badge_y + _badge_h, false);
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_rectangle(_badge_x, _badge_y, _badge_x + _badge_w, _badge_y + _badge_h, true);
    
    draw_set_color(make_color_rgb(0, 255, 230));
    draw_text(_badge_x + 3, _badge_y + 1, string(_stack_count));
    
    // 5. Tactical Reticle Brackets ( )
    if (_is_selected) {
        if (sprite_exists(spr_tactical_bracket)) {
            var _brw = floor(56 * _scale);
            var _brh = floor(42 * _scale);
            draw_sprite_stretched(spr_tactical_bracket, 0, _cx - _brw/2, _cy - _brh/2 - floor(4 * _scale), _brw, _brh);
        } else {
            draw_set_color(make_color_rgb(0, 240, 255));
            draw_circle(_cx, _cy, 24 * _scale, true);
        }
    }
}
'''

if "scr_draw_tactical_counter" not in code:
    code += helper_code
    with open(target, "w", encoding="utf-8") as f:
        f.write(code)
    print("✓ Appended tactical counter functions to scr_territory_war_system.gml")
else:
    print("✓ Functions already present in scr_territory_war_system.gml")
