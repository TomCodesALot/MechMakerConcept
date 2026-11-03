/// @description Universal Mobile Suit Animator & Modular Custom Socket Renderer
// Renders 160x160 3/4 isometric combat mechs with multi-frame idle, thruster pulse, weapon recoil, and faction paletting across both FRONT and BACK perspectives.
// Fully implements docs/13_modular_parts_and_assembly_system.md, docs/29_expanded_mobile_suit_universe_mass_production_variance_and_animation.md,
// docs/48_combat_concept_mockups_and_visual_direction.md, and docs/49_modular_combat_clash_and_dynamic_mecha_animation_engine.md.

/// @function scr_get_chassis_sockets(_chassis_type)
/// @description Returns standardized 160x160 bone socket anchor coordinates for modular custom mechs.
function scr_get_chassis_sockets(_chassis_type) {
    static _socket_db = {
        biped: {
            front: {
                torso:    { x: 0,   y: -44, depth_layer: 5 },
                head:     { x: 2,   y: -78, depth_layer: 1 },
                l_arm:    { x: -24, y: -48, depth_layer: 15 }, // Background arm
                r_arm:    { x: 24,  y: -44, depth_layer: 0 },  // Foreground weapon arm
                backpack: { x: -12, y: -62, depth_layer: 12 }  // Thrusters
            },
            back: {
                torso:    { x: 0,   y: -44, depth_layer: 5 },
                head:     { x: 2,   y: -80, depth_layer: 8 },
                l_arm:    { x: 24,  y: -48, depth_layer: 15 },
                r_arm:    { x: -24, y: -44, depth_layer: 0 },
                backpack: { x: 0,   y: -60, depth_layer: 2 }   // Prominent twin verniers
            }
        },
        hover: {
            front: {
                torso:    { x: 2,   y: -42, depth_layer: 5 },
                head:     { x: 6,   y: -76, depth_layer: 1 },
                l_arm:    { x: -20, y: -44, depth_layer: 15 },
                r_arm:    { x: 28,  y: -40, depth_layer: 0 },
                backpack: { x: -16, y: -56, depth_layer: 12 }
            },
            back: {
                torso:    { x: 2,   y: -42, depth_layer: 5 },
                head:     { x: 6,   y: -78, depth_layer: 8 },
                l_arm:    { x: 20,  y: -44, depth_layer: 15 },
                r_arm:    { x: -28, y: -40, depth_layer: 0 },
                backpack: { x: -4,  y: -56, depth_layer: 2 }
            }
        },
        tread: {
            front: {
                torso:    { x: 0,   y: -38, depth_layer: 5 },
                head:     { x: 0,   y: -70, depth_layer: 1 },
                l_arm:    { x: -30, y: -42, depth_layer: 15 },
                r_arm:    { x: 30,  y: -42, depth_layer: 0 },
                backpack: { x: -18, y: -54, depth_layer: 12 }
            },
            back: {
                torso:    { x: 0,   y: -38, depth_layer: 5 },
                head:     { x: 0,   y: -72, depth_layer: 8 },
                l_arm:    { x: 30,  y: -42, depth_layer: 15 },
                r_arm:    { x: -30, y: -42, depth_layer: 0 },
                backpack: { x: -6,  y: -54, depth_layer: 2 }
            }
        },
        aero: {
            front: {
                torso:    { x: 4,   y: -44, depth_layer: 5 },
                head:     { x: 10,  y: -78, depth_layer: 1 },
                l_arm:    { x: -18, y: -46, depth_layer: 15 },
                r_arm:    { x: 26,  y: -42, depth_layer: 0 },
                backpack: { x: -14, y: -60, depth_layer: 12 }
            },
            back: {
                torso:    { x: 4,   y: -44, depth_layer: 5 },
                head:     { x: 10,  y: -80, depth_layer: 8 },
                l_arm:    { x: 18,  y: -46, depth_layer: 15 },
                r_arm:    { x: -26, y: -42, depth_layer: 0 },
                backpack: { x: -2,  y: -60, depth_layer: 2 }
            }
        }
    };

    var _key = "biped";
    if (string_pos("hover", _chassis_type) > 0 || string_pos("sniper", _chassis_type) > 0) _key = "hover";
    else if (string_pos("tread", _chassis_type) > 0 || string_pos("artillery", _chassis_type) > 0 || string_pos("brawler", _chassis_type) > 0) _key = "tread";
    else if (string_pos("aero", _chassis_type) > 0 || string_pos("interceptor", _chassis_type) > 0 || string_pos("striker", _chassis_type) > 0) _key = "aero";

    return variable_struct_get(_socket_db, _key) ?? _socket_db.biped;
}

/// @function scr_draw_custom_mobile_suit(_suit_data, _x, _y, _scale, _facing, _state, _subimg_override, _custom_blend, _perspective)
/// @description Multi-pass depth-sorted composite renderer for player-forged custom mobile suits with metallurgy alloy finishes.
function scr_draw_custom_mobile_suit(_suit_data, _x, _y, _scale = 1.0, _facing = 1, _state = "idle", _subimg_override = -1, _custom_blend = c_white, _perspective = "front") {
    var _is_back = (_perspective == "back" || _perspective == "rear");
    if (is_string(_x)) _x = real(_x) ?? 0;
    if (is_string(_y)) _y = real(_y) ?? 0;
    if (!is_numeric(_scale)) _scale = 1.0;

    // 1. Resolve Chassis Type and Metadata
    var _chassis_type = "biped";
    var _suit_id_str = "";
    var _components = undefined;
    var _torso_alloy = "alloy_vanguard_comp";
    var _weapon_type = "KINETIC_CANNON";

    if (is_struct(_suit_data)) {
        _suit_id_str = variable_struct_get(_suit_data, "id") ?? (variable_struct_get(_suit_data, "mech_type") ?? "custom_biped");
        _chassis_type = variable_struct_get(_suit_data, "move_type") ?? (variable_struct_get(_suit_data, "chassis_type") ?? "biped");
        _components = variable_struct_get(_suit_data, "components");
        _torso_alloy = variable_struct_get(_suit_data, "alloy_id") ?? _torso_alloy;
        if (variable_struct_exists(_suit_data, "weapons") && is_array(_suit_data.weapons) && array_length(_suit_data.weapons) > 0) {
            _weapon_type = variable_struct_get(_suit_data.weapons[0], "proj_type") ?? _weapon_type;
        }
    } else if (is_string(_suit_data)) {
        _suit_id_str = _suit_data;
        if (string_pos("hover", _suit_data) > 0 || string_pos("sniper", _suit_data) > 0) _chassis_type = "hover";
        else if (string_pos("tread", _suit_data) > 0 || string_pos("artillery", _suit_data) > 0 || string_pos("brawler", _suit_data) > 0) _chassis_type = "tread";
        else if (string_pos("aero", _suit_data) > 0 || string_pos("interceptor", _suit_data) > 0 || string_pos("striker", _suit_data) > 0) _chassis_type = "aero";
        else _chassis_type = "biped";
    }

    // Heuristics for player prototype blueprints
    if (string_pos("vanguard", _suit_id_str) > 0) {
        _chassis_type = "biped";
        _torso_alloy = "alloy_vanguard_comp";
        _weapon_type = "ROTARY_VULCAN";
    } else if (string_pos("ghost", _suit_id_str) > 0 || string_pos("sniper", _suit_id_str) > 0) {
        _chassis_type = "hover";
        _torso_alloy = "alloy_hyperion_matrix";
        _weapon_type = "BEAM_PULSE";
    } else if (string_pos("scrapper", _suit_id_str) > 0 || string_pos("brawler", _suit_id_str) > 0) {
        _chassis_type = "tread";
        _torso_alloy = "alloy_adamantine_carbide";
        _weapon_type = "KINETIC_CANNON";
    } else if (string_pos("stratos", _suit_id_str) > 0 || string_pos("interceptor", _suit_id_str) > 0) {
        _chassis_type = "aero";
        _torso_alloy = "alloy_aerosteel_flux";
        _weapon_type = "BEAM_PULSE";
    }

    // 2. Resolve Sintered Metallurgy Alloy Colors
    var _primary_color = c_white;
    var _sig_glow = make_color_rgb(255, 140, 40);
    if (is_string(_torso_alloy)) {
        _primary_color = scr_get_alloy_procedural_color(_torso_alloy);
        if (_torso_alloy == "alloy_hyperion_matrix") _sig_glow = make_color_rgb(0, 240, 255);
        else if (_torso_alloy == "alloy_aerosteel_flux") _sig_glow = make_color_rgb(180, 255, 100);
        else if (_torso_alloy == "alloy_adamantine_carbide") _sig_glow = make_color_rgb(255, 60, 40);
        else if (_torso_alloy == "alloy_tachyon_superalloy") _sig_glow = make_color_rgb(120, 255, 255);
    }
    if (_custom_blend != c_white) _primary_color = merge_color(_primary_color, _custom_blend, 0.45);

    // 3. Resolve Sockets and Base Sprite
    var _sockets_pkg = scr_get_chassis_sockets(_chassis_type);
    var _sockets = _is_back ? _sockets_pkg.back : _sockets_pkg.front;

    var _base_spr = spr_ms_custom_biped_heavy_idle;
    if (_chassis_type == "hover") _base_spr = _is_back ? spr_ms_custom_hover_sniper_back_idle : spr_ms_custom_hover_sniper_idle;
    else if (_chassis_type == "tread") _base_spr = _is_back ? spr_ms_custom_tread_artillery_back_idle : spr_ms_custom_tread_artillery_idle;
    else if (_chassis_type == "aero") _base_spr = _is_back ? spr_ms_custom_aero_striker_back_idle : spr_ms_custom_aero_striker_idle;
    else _base_spr = _is_back ? spr_ms_custom_biped_heavy_back_idle : spr_ms_custom_biped_heavy_idle;

    // 4. Ground Ellipse Contact Shadow
    var _shadow_w = (_chassis_type == "hover" ? 62 : (_chassis_type == "tread" ? 68 : 55)) * _scale;
    var _shadow_h = 10 * _scale;
    var _hover_float = (_chassis_type == "hover") ? sin(current_time * 0.004) * 4 * _scale : 0;
    var _aero_float = (_chassis_type == "aero") ? sin(current_time * 0.005) * 5 * _scale : 0;
    var _total_float = _hover_float + _aero_float;

    draw_set_color(c_black);
    draw_set_alpha(0.40);
    draw_ellipse(_x - _shadow_w, _y - (_shadow_h * 0.8), _x + _shadow_w, _y + (_shadow_h * 1.2), false);
    draw_set_alpha(1.0);

    // 5. Kinematic Displacements (Recoil, Hit Stagger, Melee Dash)
    var _draw_x = _x;
    var _draw_y = _y - _total_float;
    var _draw_angle = 0;
    var _recoil_kick = 0;

    if (_state == "hit") {
        _draw_x += random_range(-3, 3) * _scale;
        _draw_y += random_range(-2, 2) * _scale;
        _draw_angle = -5 * _facing;
        _primary_color = merge_color(_primary_color, c_red, 0.45);
    } else if (_state == "fire") {
        _recoil_kick = 5 * _scale;
        _draw_x -= (4 * _facing) * _scale;
        _draw_angle = 2 * _facing;
    } else if (_state == "walk") {
        _draw_y += sin(current_time * 0.012) * 2 * _scale;
    }

    // 6. Frame Animation Sub-Image
    var _num_frames = sprite_exists(_base_spr) ? sprite_get_number(_base_spr) : 1;
    var _sub = 0;
    if (_subimg_override >= 0) {
        _sub = _subimg_override % _num_frames;
    } else {
        var _seed = abs(string_byte_at(_suit_id_str, 1) * 31 + string_byte_at(_suit_id_str, max(1, string_length(_suit_id_str))) * 19);
        if (_state == "fire") _sub = 3 % _num_frames;
        else if (_state == "walk") _sub = (floor((current_time + _seed) / 120) % 2) + 2;
        else if (_state == "hit") _sub = 1 % _num_frames;
        else _sub = floor((current_time + _seed) / 120) % _num_frames;
    }

    // 7. Pass 1: Render Base Chassis Frame with Metallurgy Alloy Tint
    if (sprite_exists(_base_spr)) {
        draw_sprite_ext(_base_spr, _sub, _draw_x, _draw_y, _scale * _facing, _scale, _draw_angle, _primary_color, 1.0);
    }

    // 8. Pass 2: Modular Sockets & Component Destruction Overlays
    var _top_y = _draw_y - (145 * _scale);
    var _l_arm_intact = true;
    var _r_arm_intact = true;
    var _legs_intact = true;

    if (!is_undefined(_components) && is_struct(_components)) {
        if (variable_struct_exists(_components, "arm_left")) _l_arm_intact = _components.arm_left.intact && (_components.arm_left.cur > 0);
        if (variable_struct_exists(_components, "arm_right")) _r_arm_intact = _components.arm_right.intact && (_components.arm_right.cur > 0);
        if (variable_struct_exists(_components, "legs")) _legs_intact = _components.legs.intact && (_components.legs.cur > 0);
    }

    // Severed Left Arm Socket Overlay & Sparks
    if (!_l_arm_intact && sprite_exists(spr_ms_ironclad_hit_left_arm_off)) {
        var _so_x = _draw_x + (_sockets.l_arm.x * _facing * _scale);
        var _so_y = _top_y + (_sockets.l_arm.y * _scale);
        draw_sprite_ext(spr_ms_ironclad_hit_left_arm_off, 0, _draw_x, _draw_y, _scale * _facing, _scale, _draw_angle, c_white, 0.95);
// Intentionally clean: no messy random spark circles
    }

    // Severed Right Arm Socket Overlay (Weapon stripped!)
    if (!_r_arm_intact && sprite_exists(spr_ms_ironclad_hit_right_arm_off)) {
        var _ro_x = _draw_x + (_sockets.r_arm.x * _facing * _scale);
        var _ro_y = _top_y + (_sockets.r_arm.y * _scale);
        draw_sprite_ext(spr_ms_ironclad_hit_right_arm_off, 0, _draw_x, _draw_y, _scale * _facing, _scale, _draw_angle, c_white, 0.95);
// Intentionally clean: no messy random spark circles
    }

    // 9. Pass 3: Backpack Thruster Vernier Plumes
    var _glow_pulse = 0.45 + 0.35 * sin((current_time + string_byte_at(_suit_id_str, 1) * 10) / 180.0);
    var _bp_x = _draw_x + (_sockets.backpack.x * _facing * _scale);
    var _bp_y = _top_y + (_sockets.backpack.y * _scale);

    draw_set_color(_sig_glow);
    if (_is_back) {
        // Twin verniers
        draw_set_alpha(_glow_pulse * 0.9);
        draw_circle(_bp_x - (8 * _facing * _scale), _bp_y, 7 * _scale, false);
        draw_circle(_bp_x + (8 * _facing * _scale), _bp_y, 7 * _scale, false);
        draw_set_color(c_white);
        draw_set_alpha(_glow_pulse * 0.5);
        draw_circle(_bp_x - (8 * _facing * _scale), _bp_y, 3 * _scale, false);
        draw_circle(_bp_x + (8 * _facing * _scale), _bp_y, 3 * _scale, false);
        draw_set_alpha(1.0);
    } else {
        // Intentionally clean: front perspective displays crisp pixel-art without dust/glow blobs
    }

    // 10. Pass 4: Weapon Firing Recoil & Muzzle Flare (Pixel Art Geometry)
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

/// @function scr_draw_animated_mobile_suit(_suit_id, _x, _y, _scale, _facing, _state, _subimg_override, _custom_blend, _perspective)
function scr_draw_animated_mobile_suit(_suit_id, _x, _y, _scale = 1.0, _facing = 1, _state = "idle", _subimg_override = -1, _custom_blend = c_white, _perspective = "front") {
    var _is_back = (_perspective == "back" || _perspective == "rear");
    if (is_string(_x)) _x = real(_x) ?? 0;
    if (is_string(_y)) _y = real(_y) ?? 0;
    if (!is_numeric(_scale)) _scale = 1.0;

    var _suit_id_str = "";
    var _spr = -1;
    var _tint = _custom_blend;
    var _sig_glow = make_color_rgb(255, 120, 40);
    var _is_custom = false;

    // 1. Resolve struct input or string ID
    if (is_struct(_suit_id)) {
        _suit_id_str = variable_struct_get(_suit_id, "id") ?? "";
        var _cand_spr = variable_struct_get(_suit_id, "sprite_asset");
        if (!is_undefined(_cand_spr)) {
            if (is_string(_cand_spr)) {
                var _a_idx = asset_get_index(_cand_spr);
                if (_a_idx != -1 && sprite_exists(_a_idx)) _spr = _a_idx;
            } else if (sprite_exists(_cand_spr)) {
                _spr = _cand_spr;
            }
        }
        var _cat = variable_struct_get(_suit_id, "category") ?? "";
        if (_cat == "CUSTOM_MECH" && _spr == -1) {
            _is_custom = true;
        }
        // Faction glow tint
        var _fac = variable_struct_get(_suit_id, "faction_id") ?? "";
        if (_fac == "faction_b") _sig_glow = make_color_rgb(0, 240, 255);
        else if (_fac == "faction_c") _sig_glow = make_color_rgb(255, 140, 30);
        else if (_fac == "faction_d") _sig_glow = make_color_rgb(0, 255, 200);
        else if (_fac == "pmc_player") _sig_glow = make_color_rgb(255, 215, 80);
    } else if (is_numeric(_suit_id) && sprite_exists(_suit_id)) {
        _spr = _suit_id;
        _suit_id_str = sprite_get_name(_suit_id);
    } else if (is_string(_suit_id)) {
        _suit_id_str = _suit_id;
        // Check if string is directly a sprite asset name
        var _direct_spr = asset_get_index(_suit_id);
        if (_direct_spr != -1 && sprite_exists(_direct_spr)) {
            _spr = _direct_spr;
        }
    }

    // Modular Custom Mechs routing if designated without a static sprite asset
    if (_is_custom) {
        scr_draw_custom_mobile_suit(_suit_id, _x, _y, _scale, _facing, _state, _subimg_override, _custom_blend, _perspective);
        return;
    }

    // 2. Resolve sprite from Game Manager or Catalog if not already resolved
    if (_spr == -1) {
        if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "get_mobile_suit")) {
            var _cat_entry = obj_GameManager.get_mobile_suit(_suit_id_str);
            if (!is_undefined(_cat_entry) && is_struct(_cat_entry)) {
                var _c_spr = variable_struct_get(_cat_entry, "sprite_asset");
                if (!is_undefined(_c_spr)) {
                    if (is_string(_c_spr)) {
                        var _idx = asset_get_index(_c_spr);
                        if (_idx != -1 && sprite_exists(_idx)) _spr = _idx;
                    } else if (sprite_exists(_c_spr)) {
                        _spr = _c_spr;
                    }
                }
            }
        }
    }

    // 3. Fallback resolution via ID inspection
    if (_spr == -1) {
        var _lower_id = string_lower(_suit_id_str);

        // Vehicles & Infantry squads (check FIRST to avoid faction name collisions)
        if (string_copy(_lower_id, 1, 4) == "veh_" || string_copy(_lower_id, 1, 4) == "inf_") {
            var _base_spr_name = "spr_" + _lower_id;
            var _cand_idle = asset_get_index(_base_spr_name + "_idle");
            if (_cand_idle != -1 && sprite_exists(_cand_idle)) {
                _spr = _cand_idle;
            }
        }
        // Custom modular chassis
        else if (string_pos("custom_biped", _lower_id) > 0 || string_pos("vanguard_heavy", _lower_id) > 0) {
            _spr = spr_ms_custom_biped_heavy_idle;
        } else if (string_pos("custom_hover", _lower_id) > 0 || string_pos("ghost_sniper", _lower_id) > 0) {
            _spr = spr_ms_custom_hover_sniper_idle;
        } else if (string_pos("custom_tread", _lower_id) > 0 || string_pos("scrapper_brawler", _lower_id) > 0) {
            _spr = spr_ms_custom_tread_artillery_idle;
        } else if (string_pos("custom_aero", _lower_id) > 0 || string_pos("stratos_interceptor", _lower_id) > 0) {
            _spr = spr_ms_custom_aero_striker_idle;
        }
        // Mobile Suits - Specific chassis matches
        else if (string_pos("ballista", _lower_id) > 0 || string_pos("howitzer", _lower_id) > 0 || string_pos("demolisher", _lower_id) > 0 || string_pos("bulwark", _lower_id) > 0) {
            _spr = spr_ms_ballista_idle;
        } else if (string_pos("centurion", _lower_id) > 0 || string_pos("warhammer", _lower_id) > 0 || string_pos("paladin", _lower_id) > 0) {
            _spr = spr_ms_centurion_idle;
        } else if (string_pos("trenchcoat", _lower_id) > 0 || string_pos("firefly", _lower_id) > 0 || string_pos("vanguard", _lower_id) > 0 || string_pos("promethean", _lower_id) > 0) {
            _spr = spr_ms_trenchcoat_idle;
        } else if (string_pos("titan", _lower_id) > 0 || string_pos("behemoth", _lower_id) > 0 || string_pos("juggernaut", _lower_id) > 0 || string_pos("goliath", _lower_id) > 0 || string_pos("harvester", _lower_id) > 0) {
            _spr = spr_ms_titan_proto;
        } else if (string_pos("siegebreaker", _lower_id) > 0) {
            _spr = spr_ms_siegebreaker_anchor;
        } else if (string_pos("zephyr", _lower_id) > 0 || string_pos("pegasus", _lower_id) > 0 || string_pos("vector", _lower_id) > 0 || string_pos("eclipse", _lower_id) > 0 || string_pos("sylph", _lower_id) > 0) {
            _spr = spr_ms_zephyr_idle;
        } else if (string_pos("kepler", _lower_id) > 0 || string_pos("helios", _lower_id) > 0 || string_pos("nebula", _lower_id) > 0 || string_pos("selene", _lower_id) > 0) {
            _spr = spr_ms_kepler_idle;
        } else if (string_pos("cassian", _lower_id) > 0) {
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
            _spr = spr_ms_muramasa_idle;
        } else if (string_pos("hephaestus", _lower_id) > 0 || string_pos("prewar", _lower_id) > 0) {
            _spr = spr_ms_hephaestus_avatar;
        } else if (string_pos("seeker", _lower_id) > 0 || string_pos("martian", _lower_id) > 0) {
            _spr = spr_ms_martian_seeker_idle;
        } else {
            _spr = -1;
        }
    }

    // Explicit Diagnostic Wireframe Fallback (NEVER silently masquerade as Ironclad)
    if (!sprite_exists(_spr)) {
        draw_set_color(c_fuchsia);
        draw_rectangle(_x - 32 * _scale, _y - 96 * _scale, _x + 32 * _scale, _y, true);
        draw_line(_x - 32 * _scale, _y - 96 * _scale, _x + 32 * _scale, _y);
        draw_line(_x + 32 * _scale, _y - 96 * _scale, _x - 32 * _scale, _y);
        draw_set_color(c_yellow);
        draw_set_halign(fa_center);
        draw_set_valign(fa_bottom);
        draw_text_transformed(_x, _y - 100 * _scale, "[MISSING SPRITE]: " + string(_suit_id_str), 0.75, 0.75, 0);
        draw_set_halign(fa_left);
        draw_set_valign(fa_top);
        draw_set_color(c_white);
        return;
    }

    // 4. Perspective Resolution (Back View)
    var _spr_name = sprite_get_name(_spr);
    if (_is_back) {
        var _back_name = "";
        if (string_pos("_idle", _spr_name) > 0) {
            _back_name = string_replace(_spr_name, "_idle", "_back_idle");
        } else {
            _back_name = _spr_name + "_back_idle";
        }
        var _b_cand = asset_get_index(_back_name);
        if (_b_cand != -1 && sprite_exists(_b_cand)) {
            _spr = _b_cand;
            _spr_name = _back_name;
        }
    }

    // 5. Action State Resolution (fire, melee, boost, damaged, destroyed)
    if (_state != "idle") {
        var _action_spr = -1;
        var _prefix = string_replace(string_replace(_spr_name, "_back_idle", ""), "_idle", "");

        // Firing actions
        if (string_pos("fire", _state) > 0) {
            if (_state == "fire_chaingun") {
                var _fc = asset_get_index(_prefix + "_fire_chaingun");
                if (_fc != -1 && sprite_exists(_fc)) _action_spr = _fc;
            } else if (_state == "fire_beam") {
                var _fb = asset_get_index(_prefix + "_fire_beam");
                if (_fb == -1 || !sprite_exists(_fb)) _fb = asset_get_index(_prefix + "_fire_plasma");
                if (_fb != -1 && sprite_exists(_fb)) _action_spr = _fb;
            } else if (_state == "fire_missiles") {
                var _fm = asset_get_index(_prefix + "_fire_missiles");
                if (_fm != -1 && sprite_exists(_fm)) _action_spr = _fm;
            } else if (_state == "fire_rifle") {
                var _fr = asset_get_index(_prefix + "_fire_rifle");
                if (_fr != -1 && sprite_exists(_fr)) _action_spr = _fr;
            }

            // Universal _fire suffix fallback (e.g. spr_ms_siegebreaker_fire, vehicles, infantry)
            if (_action_spr == -1) {
                var _gen_fire = asset_get_index(_prefix + "_fire");
                if (_gen_fire != -1 && sprite_exists(_gen_fire)) _action_spr = _gen_fire;
            }
            if (_action_spr == -1) {
                var _gen_rifle = asset_get_index(_prefix + "_fire_rifle");
                if (_gen_rifle != -1 && sprite_exists(_gen_rifle)) _action_spr = _gen_rifle;
            }
        }
        // Melee actions
        else if (_state == "melee") {
            var _m_cand = asset_get_index(_prefix + "_attack_melee");
            if (_m_cand == -1 || !sprite_exists(_m_cand)) _m_cand = asset_get_index(_prefix + "_attack_blade");
            if (_m_cand == -1 || !sprite_exists(_m_cand)) _m_cand = asset_get_index(_prefix + "_attack_saber");
            if (_m_cand == -1 || !sprite_exists(_m_cand)) _m_cand = asset_get_index(_prefix + "_attack_claw");
            if (_m_cand != -1 && sprite_exists(_m_cand)) _action_spr = _m_cand;
        }
        // Boost / Walk / Sprint
        else if (_state == "boost" || _state == "walk") {
            var _b_cand = asset_get_index(_prefix + "_boost");
            if (_b_cand == -1 || !sprite_exists(_b_cand)) _b_cand = asset_get_index(_prefix + "_sprint");
            if (_b_cand == -1 || !sprite_exists(_b_cand)) _b_cand = asset_get_index(_prefix + "_walk");
            if (_b_cand != -1 && sprite_exists(_b_cand)) _action_spr = _b_cand;
        }
        // Damaged / Hit
        else if (_state == "damaged" || _state == "hit") {
            var _d_cand = asset_get_index(_prefix + "_idle_damaged");
            if (_d_cand == -1 || !sprite_exists(_d_cand)) _d_cand = asset_get_index(_prefix + "_crippled_idle");
            if (_d_cand == -1 || !sprite_exists(_d_cand)) _d_cand = asset_get_index(_prefix + "_hit_kinetic");
            if (_d_cand == -1 || !sprite_exists(_d_cand)) _d_cand = asset_get_index(_prefix + "_damage_kinetic");
            if (_d_cand == -1 || !sprite_exists(_d_cand)) _d_cand = asset_get_index(_prefix + "_defeat");
            if (_d_cand != -1 && sprite_exists(_d_cand)) _action_spr = _d_cand;
        }
        // Destroyed
        else if (_state == "destroyed" || _state == "defeat") {
            var _dest_cand = asset_get_index(_prefix + "_destroyed");
            if (_dest_cand == -1 || !sprite_exists(_dest_cand)) _dest_cand = asset_get_index(_prefix + "_defeat");
            if (_dest_cand == -1 || !sprite_exists(_dest_cand)) _dest_cand = asset_get_index(_prefix + "_crippled");
            // If conventional vehicle without bespoke defeat sprite, fall back to authentic vehicle wreckage
            if (_dest_cand == -1 || !sprite_exists(_dest_cand)) {
                if (string_pos("veh_", _lower_id) > 0) {
                    if (string_pos("skyhammer", _lower_id) > 0 || string_pos("sabre", _lower_id) > 0 || string_pos("dart", _lower_id) > 0 || string_pos("gunship", _lower_id) > 0 || string_pos("chopper", _lower_id) > 0 || string_pos("bomber", _lower_id) > 0 || string_pos("rotor", _lower_id) > 0 || string_pos("drone_jet", _lower_id) > 0) {
                        _dest_cand = spr_veh_wreckage_plane;
                    } else {
                        _dest_cand = spr_veh_wreckage_tank;
                    }
                }
            }
            if (_dest_cand != -1 && sprite_exists(_dest_cand)) _action_spr = _dest_cand;
        }

        if (_action_spr != -1 && sprite_exists(_action_spr)) {
            _spr = _action_spr;
        }
    }

    // 6. Ground Ellipse Contact Shadow
    var _shadow_w = 55 * _scale;
    var _shadow_h = 10 * _scale;
    draw_set_color(c_black);
    draw_set_alpha(0.40);
    draw_ellipse(_x - _shadow_w, _y - (_shadow_h * 0.8), _x + _shadow_w, _y + (_shadow_h * 1.2), false);
    draw_set_alpha(1.0);

    // 7. Dynamic Frame Sub-Image Calculation (Smooth Multi-Frame Playback!)
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
    } else if (_state == "destroyed" || _state == "defeat") {
        if (_action_spr == -1) {
            // Procedural charred collapse posture for suits without dedicated destroyed frame
            _draw_angle = -20 * _facing;
            _draw_y += 12 * _scale;
            _draw_x -= (8 * _facing) * _scale;
            _tint = merge_color(_tint, make_color_rgb(45, 45, 48), 0.75);
        }
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

    // 11. UNIFIED PROCEDURAL COMBAT ACTION VFX (State Visual Effects: Damage Smoke & Destruction)
    if (!_is_back) {
        if (_state == "destroyed" || _state == "defeat") {
            // Catastrophic destruction VFX: Rising black smoke & burning reactor flame core
            var _wreck_t = current_time * 0.003;
            for (var k = 0; k < 4; k++) {
                var _smk_off = (k * 20);
                var _smk_prog = fmod(_wreck_t * 50 + _smk_off, 55);
                var _smk_y = _top_y + (55 * _scale) - (_smk_prog * _scale);
                var _smk_x = _draw_x + (sin(_wreck_t * 1.5 + k) * 10 * _scale);
                var _smk_r = (6 + k * 3.5) * _scale;
                draw_set_color(make_color_rgb(25, 25, 30));
                draw_set_alpha(0.65 - (_smk_prog / 65));
                draw_circle(_smk_x, _smk_y, _smk_r, false);
            }
            // Burning reactor flame core
            var _flame_pulse = 0.6 + 0.4 * sin(current_time * 0.02);
            draw_set_color(make_color_rgb(255, 120, 20));
            draw_set_alpha(_flame_pulse * 0.85);
            draw_circle(_draw_x, _top_y + (75 * _scale), 9 * _scale, false);
            draw_set_color(make_color_rgb(255, 230, 80));
            draw_set_alpha(_flame_pulse * 0.65);
            draw_circle(_draw_x, _top_y + (75 * _scale), 4 * _scale, false);
            draw_set_alpha(1.0);
        } else if (_state == "damaged" || _state == "hit") {
            // Shorting electrical blue sparks
            if (fmod(current_time, 200) < 100) {
                draw_set_color(make_color_rgb(120, 220, 255));
                var _spk_x = _draw_x + random_range(-14, 14) * _scale;
                var _spk_y = _top_y + (60 + random_range(-18, 18)) * _scale;
                draw_line_width(_spk_x, _spk_y, _spk_x + random_range(-5, 5) * _scale, _spk_y + random_range(-5, 5) * _scale, 1.5 * _scale);
            }
        }
    }
}
