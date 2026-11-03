import re

with open("scripts/scr_draw_animated_mobile_suit/scr_draw_animated_mobile_suit.gml", "r") as f:
    text = f.read()

# 1. Update Fallback section
start_fb = text.find('else if (string_pos("oberon"')
end_fb = text.find('spr_ms_muramasa_idle;', start_fb) + len('spr_ms_muramasa_idle;')
assert start_fb != -1 and end_fb != -1

new_fallback = '''else if (string_pos("cassian", _lower_id) > 0) {
            _spr = spr_ms_cassian_custom_idle;
        } else if (string_pos("chronos", _lower_id) > 0) {
            _spr = spr_ms_chronos_idle;
        } else if (string_pos("marauder", _lower_id) > 0) {
            _spr = spr_ms_marauder_idle;
        } else if (string_pos("iron_reaver", _lower_id) > 0 || string_pos("reaver", _lower_id) > 0) {
            _spr = spr_ms_iron_reaver_idle;
        } else if (string_pos("takahashi", _lower_id) > 0) {
            _spr = spr_ms_takahashi_custom_idle;
        } else if (string_pos("kamaitachi", _lower_id) > 0) {
            _spr = spr_ms_kamaitachi_idle;
        } else if (string_pos("oberon", _lower_id) > 0 || string_pos("archangel", _lower_id) > 0 || string_pos("typhon", _lower_id) > 0 || string_pos("seraphim", _lower_id) > 0 || string_pos("sentry", _lower_id) > 0) {
            _spr = spr_ms_oberon_idle;
        } else if (string_pos("aether", _lower_id) > 0 || string_pos("astraea", _lower_id) > 0) {
            _spr = spr_ms_aether_idle;
        } else if (string_pos("bloodhound", _lower_id) > 0 || string_pos("ripper", _lower_id) > 0 || string_pos("jackal", _lower_id) > 0 || string_pos("scythe", _lower_id) > 0) {
            _spr = spr_ms_bloodhound_idle;
        } else if (string_pos("vandal", _lower_id) > 0 || string_pos("hellhound", _lower_id) > 0 || string_pos("chimera", _lower_id) > 0 || string_pos("partisan", _lower_id) > 0) {
            _spr = spr_ms_vandal_idle;
        } else if (string_pos("gorgon", _lower_id) > 0 || string_pos("warthog", _lower_id) > 0 || string_pos("slag", _lower_id) > 0 || string_pos("cerberus", _lower_id) > 0 || string_pos("devil", _lower_id) > 0) {
            _spr = spr_ms_gorgon_idle;
        } else if (string_pos("hyena", _lower_id) > 0 || string_pos("scrapper", _lower_id) > 0 || string_pos("cruz", _lower_id) > 0) {
            _spr = spr_ms_hyena_idle;
        } else if (string_pos("kage", _lower_id) > 0 || string_pos("shinobi", _lower_id) > 0 || string_pos("phantom", _lower_id) > 0 || string_pos("null07", _lower_id) > 0) {
            _spr = spr_ms_kage_idle;
        } else if (string_pos("ronin", _lower_id) > 0 || string_pos("oni", _lower_id) > 0 || string_pos("fudo", _lower_id) > 0 || string_pos("bushido", _lower_id) > 0) {
            _spr = spr_ms_ronin_idle;
        } else if (string_pos("tessen", _lower_id) > 0 || string_pos("shuriken", _lower_id) > 0 || string_pos("raiden", _lower_id) > 0) {
            _spr = spr_ms_tessen_idle;
        } else if (string_pos("muramasa", _lower_id) > 0 || string_pos("susanoo", _lower_id) > 0 || string_pos("yamato", _lower_id) > 0 || string_pos("kusanagi", _lower_id) > 0 || string_pos("amaterasu", _lower_id) > 0) {
            _spr = spr_ms_muramasa_idle;'''

text = text[:start_fb] + new_fallback + text[end_fb:]

# 2. Update animation engine section
start_anim = text.find("    // 7. Dynamic Frame Sub-Image Calculation")
assert start_anim != -1

new_anim = '''    // 7. Dynamic Frame Sub-Image Calculation (Smooth Multi-Frame Playback!)
    var _num_frames = sprite_exists(_spr) ? sprite_get_number(_spr) : 1;
    var _sub = 0;

    var _seed = abs(string_byte_at(_suit_id_str, 1) * 31 + string_byte_at(_suit_id_str, max(1, string_length(_suit_id_str))) * 19);
    if (_subimg_override >= 0) {
        _sub = floor(_subimg_override) % _num_frames;
    } else {
        var _frame_interval = (string_pos("fire", _state) > 0 || _state == "melee" || _state == "boost") ? 90 : 130;
        _sub = floor((current_time + _seed) / _frame_interval) % _num_frames;
    }

    // 8. Dynamic Kinematic Displacements (Recoil Kickback, Stagger, Melee Lunge)
    var _orig_yo = sprite_exists(_spr) ? sprite_get_yoffset(_spr) : 145;
    var _draw_x = _x;
    var _draw_y = (_orig_yo > 0) ? _y : (_y - (145 * _scale));
    var _top_y = (_orig_yo > 0) ? (_y - (_orig_yo * _scale)) : (_y - (145 * _scale));
    var _draw_angle = 0;

    // Resolve primary weapon name for authentic doctrine action VFX
    var _wpn_name_str = "";
    if (is_struct(_suit_id)) {
        _wpn_name_str = variable_struct_get(_suit_id, "primary_weapon") ?? "";
    }
    if (_wpn_name_str == "" && instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "get_mobile_suit")) {
        var _cat_entry_w = obj_GameManager.get_mobile_suit(_suit_id_str);
        if (is_struct(_cat_entry_w)) _wpn_name_str = variable_struct_get(_cat_entry_w, "primary_weapon") ?? "";
    }
    var _lower_wpn = string_lower(_wpn_name_str);

    if (_state == "damaged" || _state == "hit") {
        _draw_x -= (6 * _facing) * _scale;
        _draw_x += random_range(-3, 3) * _scale;
        _draw_y += random_range(-2, 2) * _scale;
        _draw_angle = -5 * _facing;
        _tint = merge_color(_tint, c_red, 0.45);
    } else if (string_pos("fire", _state) > 0) {
        // Dynamic procedural weapon recoil (pulsing kickback matching animation timer)
        var _kick = (sin((_subimg_override >= 0 ? _subimg_override : current_time * 0.015) * pi * 2.0) * 0.5 + 0.5) * 6.0 * _scale;
        _draw_x -= (_kick * _facing);
        _draw_angle = (1.5 * _scale) * _facing;
    } else if (_state == "melee") {
        // Forward lunge dash
        var _lunge = (sin((_subimg_override >= 0 ? _subimg_override : current_time * 0.012) * pi * 2.0) * 0.5 + 0.5) * 14.0 * _scale;
        _draw_x += (_lunge * _facing);
        _draw_angle = -4 * _facing;
    } else if (_state == "boost" || _state == "walk") {
        _draw_y += sin(current_time * 0.008) * 3 * _scale;
    }

    // 8b. Resolve Modular Weapon Overlays (Gundam Doctrine System)
    var _wpn_prim_spr = -1;
    var _wpn_sec_spr = -1;
    var _wpn_prim_str = "";
    var _wpn_sec_str = "";

    if (is_struct(_suit_id)) {
        _wpn_prim_str = variable_struct_get(_suit_id, "weapon_overlay_primary") ?? "";
        _wpn_sec_str = variable_struct_get(_suit_id, "weapon_overlay_secondary") ?? "";
    }
    if (_wpn_prim_str == "" && instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "get_mobile_suit")) {
        var _c_entry = obj_GameManager.get_mobile_suit(_suit_id_str);
        if (is_struct(_c_entry)) {
            _wpn_prim_str = variable_struct_get(_c_entry, "weapon_overlay_primary") ?? "";
            _wpn_sec_str = variable_struct_get(_c_entry, "weapon_overlay_secondary") ?? "";
        }
    }

    if (_wpn_prim_str != "") {
        var _p_idx = asset_get_index(_wpn_prim_str);
        if (_p_idx != -1 && sprite_exists(_p_idx)) _wpn_prim_spr = _p_idx;
    }
    if (_wpn_sec_str != "") {
        var _s_idx = asset_get_index(_wpn_sec_str);
        if (_s_idx != -1 && sprite_exists(_s_idx)) _wpn_sec_spr = _s_idx;
    }

    // Pass 1: Background Secondary Weapon / Shield (Only on CUSTOM_MECH to prevent double-weapons on military suits)
    if (!_is_back && _is_custom && _wpn_sec_spr != -1) {
        var _sec_sub = _sub % sprite_get_number(_wpn_sec_spr);
        draw_sprite_ext(_wpn_sec_spr, _sec_sub, _draw_x, _draw_y, _scale * _facing, _scale, _draw_angle, c_white, 1.0);
    }

    // 9. Render Main 2D Base Chassis Frame
    if (sprite_exists(_spr)) {
        draw_sprite_ext(_spr, _sub, _draw_x, _draw_y, _scale * _facing, _scale, _draw_angle, _tint, 1.0);
    }

    // Pass 3: Foreground Primary Weapon (Only on CUSTOM_MECH to prevent double-weapons on military suits)
    if (!_is_back && _is_custom && _wpn_prim_spr != -1) {
        var _prim_sub = _sub % sprite_get_number(_wpn_prim_spr);
        if (string_pos("fire", _state) > 0 || _state == "melee") {
            _prim_sub = 3 % sprite_get_number(_wpn_prim_spr);
        }
        draw_sprite_ext(_wpn_prim_spr, _prim_sub, _draw_x, _draw_y, _scale * _facing, _scale, _draw_angle, c_white, 1.0);
    }

    // 10. Backpack Thruster Vernier Plumes (ONLY on REAR perspective)
    if (_is_back) {
        var _glow_pulse = 0.4 + 0.3 * sin((current_time + string_byte_at(_suit_id_str, 1) * 10) / 180.0);
        draw_set_color(_sig_glow);
        draw_set_alpha(_glow_pulse * 0.85);
        draw_circle(_draw_x - (6 * _facing * _scale), _top_y + (76 * _scale), 7 * _scale, false);
        draw_circle(_draw_x + (14 * _facing * _scale), _top_y + (76 * _scale), 7 * _scale, false);
        draw_set_color(c_white);
        draw_set_alpha(_glow_pulse * 0.5);
        draw_circle(_draw_x - (6 * _facing * _scale), _top_y + (76 * _scale), 3 * _scale, false);
        draw_circle(_draw_x + (14 * _facing * _scale), _top_y + (76 * _scale), 3 * _scale, false);
        draw_set_alpha(1.0);
    }

    // 11. UNIFIED PROCEDURAL COMBAT ACTION VFX (Authentic Pixel Art, Zero Debug Circles!)
    if (!_is_back) {
        var _muz_x = _draw_x + (46 * _facing * _scale);
        var _muz_y = _top_y + (66 * _scale);

        if (string_pos("fire", _state) > 0) {
            var _is_beam = (string_pos("beam", _lower_wpn) > 0 || string_pos("particle", _lower_wpn) > 0 || string_pos("tachyon", _lower_wpn) > 0 || string_pos("plasma", _lower_wpn) > 0 || string_pos("pulse", _lower_wpn) > 0);
            var _is_missile = (string_pos("missile", _lower_wpn) > 0 || string_pos("rocket", _lower_wpn) > 0 || string_pos("swarm", _lower_wpn) > 0);

            if (_is_beam) {
                // Coherent particle / tachyon cross spark
                var _b_color = (string_pos("tachyon", _lower_wpn) > 0 || string_pos("plasma", _lower_wpn) > 0) ? make_color_rgb(180, 80, 255) : make_color_rgb(0, 240, 255);
                draw_set_color(_b_color);
                draw_set_alpha(0.90);
                draw_line_width(_muz_x - (10 * _scale), _muz_y, _muz_x + (22 * _facing * _scale), _muz_y, 3.5 * _scale);
                draw_line_width(_muz_x + (4 * _facing * _scale), _muz_y - (10 * _scale), _muz_x + (4 * _facing * _scale), _muz_y + (10 * _scale), 2.5 * _scale);
                draw_set_color(c_white);
                draw_line_width(_muz_x - (4 * _scale), _muz_y, _muz_x + (14 * _facing * _scale), _muz_y, 1.5 * _scale);
                draw_set_alpha(1.0);
            } else if (_is_missile) {
                // Micro-rocket dual flame plume
                draw_set_color(make_color_rgb(255, 140, 30));
                draw_triangle(_muz_x, _muz_y - (6 * _scale), _muz_x + (16 * _facing * _scale), _muz_y, _muz_x, _muz_y + (6 * _scale), false);
                draw_set_color(c_white);
                draw_triangle(_muz_x, _muz_y - (2 * _scale), _muz_x + (9 * _facing * _scale), _muz_y, _muz_x, _muz_y + (2 * _scale), false);
            } else {
                // Ballistic / Heavy Artillery Fiery Jagged Muzzle Flash & Ejected Brass Shell
                draw_set_color(make_color_rgb(255, 185, 45));
                draw_triangle(_muz_x, _muz_y - (8 * _scale), _muz_x + (22 * _facing * _scale), _muz_y, _muz_x, _muz_y + (8 * _scale), false);
                draw_set_color(make_color_rgb(255, 245, 170));
                draw_triangle(_muz_x, _muz_y - (3 * _scale), _muz_x + (12 * _facing * _scale), _muz_y, _muz_x, _muz_y + (3 * _scale), false);
                // Spent brass shell casing flying backward
                var _casing_x = _draw_x - (8 * _facing * _scale);
                var _casing_y = _muz_y + (6 * _scale) + (sin(current_time * 0.02) * 4 * _scale);
                draw_set_color(make_color_rgb(215, 175, 55));
                draw_rectangle(_casing_x - (2.5 * _scale), _casing_y - (1.2 * _scale), _casing_x + (2.5 * _scale), _casing_y + (1.2 * _scale), false);
            }
        } else if (_state == "melee") {
            // High-Frequency Energy Blade / Cleaver Slash Arc
            var _slash_x = _draw_x + (28 * _facing * _scale);
            var _slash_y = _top_y + (72 * _scale);
            var _slash_c = (string_pos("claw", _lower_wpn) > 0 || string_pos("crush", _lower_wpn) > 0) ? make_color_rgb(255, 160, 40) : make_color_rgb(0, 245, 220);
            draw_set_color(_slash_c);
            draw_set_alpha(0.85);
            draw_line_width(_slash_x, _slash_y - (24 * _scale), _slash_x + (22 * _facing * _scale), _slash_y + (16 * _scale), 3.0 * _scale);
            draw_set_color(c_white);
            draw_line_width(_slash_x + (2 * _facing * _scale), _slash_y - (18 * _scale), _slash_x + (18 * _facing * _scale), _slash_y + (12 * _scale), 1.5 * _scale);
            draw_set_alpha(1.0);
        }
    }
}
'''

text = text[:start_anim] + new_anim

# 3. Clean draw_circle inside scr_draw_custom_mobile_suit
text = re.sub(
    r'// 10\. Pass 4: Weapon Firing Recoil & Muzzle Flare.*?(?=/// @function scr_draw_animated_mobile_suit|\Z)',
    '''// 10. Pass 4: Weapon Firing Recoil & Muzzle Flare (Pixel Art Geometry)
    if (_r_arm_intact && _state == "fire" && !_is_back) {
        var _muzzle_x = _draw_x + ((_sockets.r_arm.x + 36) * _facing * _scale) - (_recoil_kick * _facing);
        var _muzzle_y = _top_y + (_sockets.r_arm.y * _scale) + (14 * _scale);

        if (_weapon_type == "BEAM_PULSE" || _weapon_type == "TACHYON_BEAM") {
            draw_set_color(make_color_rgb(0, 240, 255));
            draw_line_width(_muzzle_x - 8 * _scale, _muzzle_y, _muzzle_x + 18 * _facing * _scale, _muzzle_y, 3 * _scale);
            draw_set_color(c_white);
            draw_line_width(_muzzle_x - 3 * _scale, _muzzle_y, _muzzle_x + 10 * _facing * _scale, _muzzle_y, 1.5 * _scale);
        } else if (_weapon_type == "MICRO_MISSILE") {
            draw_set_color(make_color_rgb(255, 140, 30));
            draw_triangle(_muzzle_x, _muzzle_y - 5 * _scale, _muzzle_x + 14 * _facing * _scale, _muzzle_y, _muzzle_x, _muzzle_y + 5 * _scale, false);
        } else {
            draw_set_color(make_color_rgb(255, 185, 45));
            draw_triangle(_muzzle_x, _muzzle_y - 7 * _scale, _muzzle_x + 18 * _facing * _scale, _muzzle_y, _muzzle_x, _muzzle_y + 7 * _scale, false);
            draw_set_color(make_color_rgb(255, 245, 170));
            draw_triangle(_muzzle_x, _muzzle_y - 3 * _scale, _muzzle_x + 10 * _facing * _scale, _muzzle_y, _muzzle_x, _muzzle_y + 3 * _scale, false);
        }
    }
}

''',
    text,
    flags=re.DOTALL
)

with open("scripts/scr_draw_animated_mobile_suit/scr_draw_animated_mobile_suit.gml", "w") as f:
    f.write(text)

print("Updated scr_draw_animated_mobile_suit.gml with unified procedural animation engine!")
