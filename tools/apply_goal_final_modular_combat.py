# -*- coding: utf-8 -*-
"""
Goal Final: Modular Combat Clash & Dynamic Mecha Animation Engine
Applies all agreed architecture from /grill-me across:
1. scripts/scr_draw_animated_mobile_suit/scr_draw_animated_mobile_suit.gml
2. objects/obj_BattleManager/Create_0.gml
3. objects/obj_BattleManager/Draw_0.gml
"""

import re
import os

print("=== APPLYING GOAL FINAL: MODULAR COMBAT CLASH & ANIMATION ENGINE ===")

# =========================================================================
# 1. UPDATE scr_draw_animated_mobile_suit.gml
# =========================================================================
animator_path = "scripts/scr_draw_animated_mobile_suit/scr_draw_animated_mobile_suit.gml"
animator_code = """/// @description Universal Mobile Suit Animator & Modular Custom Socket Renderer
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
        else _sub = floor((current_time + _seed) / 250) % min(2, _num_frames);
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
        if ((current_time % 300) < 140) {
            draw_set_color(make_color_rgb(140, 220, 255));
            draw_circle(_so_x + random_range(-3, 3) * _scale, _so_y + random_range(-3, 3) * _scale, 2 * _scale, false);
        }
    }

    // Severed Right Arm Socket Overlay (Weapon stripped!)
    if (!_r_arm_intact && sprite_exists(spr_ms_ironclad_hit_right_arm_off)) {
        var _ro_x = _draw_x + (_sockets.r_arm.x * _facing * _scale);
        var _ro_y = _top_y + (_sockets.r_arm.y * _scale);
        draw_sprite_ext(spr_ms_ironclad_hit_right_arm_off, 0, _draw_x, _draw_y, _scale * _facing, _scale, _draw_angle, c_white, 0.95);
        if ((current_time % 350) < 160) {
            draw_set_color(make_color_rgb(255, 180, 60));
            draw_circle(_ro_x + random_range(-3, 3) * _scale, _ro_y + random_range(-3, 3) * _scale, 2.5 * _scale, false);
        }
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
        // Core chest / shoulder exhaust flare
        draw_set_alpha(_glow_pulse * 0.75);
        draw_circle(_bp_x, _bp_y, 9 * _scale, false);
        draw_set_color(c_white);
        draw_set_alpha(_glow_pulse * 0.4);
        draw_circle(_bp_x, _bp_y, 4 * _scale, false);
        draw_set_alpha(1.0);
    }

    // 10. Pass 4: Weapon Firing Recoil & Muzzle Flare
    if (_r_arm_intact && _state == "fire" && !_is_back) {
        var _muzzle_x = _draw_x + ((_sockets.r_arm.x + 36) * _facing * _scale) - (_recoil_kick * _facing);
        var _muzzle_y = _top_y + (_sockets.r_arm.y * _scale) + (14 * _scale);

        if (_weapon_type == "BEAM_PULSE" || _weapon_type == "TACHYON_BEAM") {
            // Cyan energy discharge ring
            draw_set_color(make_color_rgb(0, 240, 255));
            draw_set_alpha(0.85);
            draw_circle(_muzzle_x, _muzzle_y, 18 * _scale, false);
            draw_set_color(c_white);
            draw_circle(_muzzle_x, _muzzle_y, 9 * _scale, false);
        } else if (_weapon_type == "MICRO_MISSILE") {
            // White smoke cloud burst
            draw_set_color(make_color_rgb(220, 225, 235));
            draw_set_alpha(0.70);
            draw_circle(_muzzle_x - (10 * _facing * _scale), _muzzle_y, 14 * _scale, false);
        } else {
            // Kinetic / Vulcan fiery flash
            draw_set_color(make_color_rgb(255, 220, 90));
            draw_set_alpha(0.90);
            draw_circle(_muzzle_x, _muzzle_y, 16 * _scale, false);
            draw_set_color(c_white);
            draw_circle(_muzzle_x, _muzzle_y, 8 * _scale, false);
        }
        draw_set_alpha(1.0);
    }
}

/// @function scr_draw_animated_mobile_suit(_suit_id, _x, _y, _scale, _facing, _state, _subimg_override, _custom_blend, _perspective)
function scr_draw_animated_mobile_suit(_suit_id, _x, _y, _scale = 1.0, _facing = 1, _state = "idle", _subimg_override = -1, _custom_blend = c_white, _perspective = "front") {
    // Check if _suit_id is a struct or custom player mech
    var _is_custom = false;
    var _suit_id_str = "";

    if (is_struct(_suit_id)) {
        _is_custom = true;
        _suit_id_str = variable_struct_get(_suit_id, "id") ?? (variable_struct_get(_suit_id, "mech_type") ?? "custom_biped");
    } else if (is_string(_suit_id)) {
        _suit_id_str = _suit_id;
        if (string_pos("custom_", _suit_id) > 0 || string_pos("bp_player_", _suit_id) > 0 || string_pos("vanguard_heavy", _suit_id) > 0 || string_pos("ghost_sniper", _suit_id) > 0 || string_pos("scrapper_brawler", _suit_id) > 0 || string_pos("stratos_interceptor", _suit_id) > 0) {
            _is_custom = true;
        }
    }

    // Route Custom Mechs to the Modular Socket Composite Renderer
    if (_is_custom) {
        scr_draw_custom_mobile_suit(_suit_id, _x, _y, _scale, _facing, _state, _subimg_override, _custom_blend, _perspective);
        return;
    }

    var _is_back = (_perspective == "back" || _perspective == "rear");
    var _spr = _is_back ? spr_ms_ironclad_back_idle : spr_ms_ironclad_idle;
    var _tint = _custom_blend;
    var _sig_glow = make_color_rgb(255, 120, 40);
    var _chassis_name = "Mobile Suit";

    // 1. Resolve suit metadata from GameManager catalog if available
    if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "get_mobile_suit")) {
        var _suit = obj_GameManager.get_mobile_suit(_suit_id);
        if (!is_undefined(_suit) && is_struct(_suit)) {
            _chassis_name = variable_struct_get(_suit, "name") ?? _chassis_name;
            var _spr_asset = variable_struct_get(_suit, "sprite_asset");
            if (!is_undefined(_spr_asset)) {
                var _res_idx = -1;
                if (is_string(_spr_asset)) {
                    _res_idx = asset_get_index(_spr_asset);
                } else if (sprite_exists(_spr_asset)) {
                    _res_idx = _spr_asset;
                }

                if (_res_idx != -1 && sprite_exists(_res_idx)) {
                    if (_is_back) {
                        var _s_name = sprite_get_name(_res_idx);
                        var _b_name = string_replace(_s_name, "_idle", "_back_idle");
                        var _b_idx = asset_get_index(_b_name);
                        if (_b_idx != -1 && sprite_exists(_b_idx)) {
                            _spr = _b_idx;
                        } else {
                            _spr = _res_idx;
                        }
                    } else {
                        _spr = _res_idx;
                    }
                }
            }
            // Resolve faction glow
            var _fac = variable_struct_get(_suit, "faction_id") ?? "";
            if (_fac == "faction_b") _sig_glow = make_color_rgb(0, 240, 255);
            else if (_fac == "faction_c") _sig_glow = make_color_rgb(255, 140, 30);
            else if (_fac == "faction_d") _sig_glow = make_color_rgb(0, 255, 200);
            else if (_fac == "pmc_player") _sig_glow = make_color_rgb(255, 215, 80);
        }
    }

    // Direct keyword mapping heuristics for all 16 mass-production candidates & apex prototypes
    if (_spr == spr_ms_ironclad_idle || _spr == spr_ms_ironclad_back_idle) {
        if (_is_back) {
            if (string_pos("ballista", _suit_id) > 0) _spr = spr_ms_ballista_back_idle;
            else if (string_pos("centurion", _suit_id) > 0) _spr = spr_ms_centurion_back_idle;
            else if (string_pos("trenchcoat", _suit_id) > 0) _spr = spr_ms_trenchcoat_back_idle;
            else if (string_pos("zephyr", _suit_id) > 0) _spr = spr_ms_zephyr_back_idle;
            else if (string_pos("kepler", _suit_id) > 0) _spr = spr_ms_kepler_back_idle;
            else if (string_pos("oberon", _suit_id) > 0) _spr = spr_ms_oberon_back_idle;
            else if (string_pos("gorgon", _suit_id) > 0) _spr = spr_ms_gorgon_back_idle;
            else if (string_pos("bloodhound", _suit_id) > 0) _spr = spr_ms_bloodhound_back_idle;
            else if (string_pos("vandal", _suit_id) > 0) _spr = spr_ms_vandal_back_idle;
            else if (string_pos("ronin", _suit_id) > 0) _spr = spr_ms_ronin_back_idle;
            else if (string_pos("tessen", _suit_id) > 0) _spr = spr_ms_tessen_back_idle;
            else if (string_pos("kage", _suit_id) > 0 || string_pos("shinobi", _suit_id) > 0) _spr = spr_ms_kage_back_idle;
            else if (string_pos("aether", _suit_id) > 0 || string_pos("colony", _suit_id) > 0 || string_pos("sylph", _suit_id) > 0) _spr = spr_ms_aether_back_idle;
            else if (string_pos("hyena", _suit_id) > 0 || string_pos("syndicate", _suit_id) > 0 || string_pos("scrapper", _suit_id) > 0) _spr = spr_ms_hyena_back_idle;
            else if (string_pos("muramasa", _suit_id) > 0 || string_pos("zaibatsu", _suit_id) > 0) _spr = spr_ms_muramasa_back_idle;
            else if (string_pos("hephaestus", _suit_id) > 0) _spr = spr_ms_hephaestus_avatar_back_idle;
            else if (string_pos("titan", _suit_id) > 0 || string_pos("juggernaut", _suit_id) > 0) _spr = spr_ms_titan_proto_back_idle;
            else if (string_pos("siegebreaker", _suit_id) > 0) _spr = spr_ms_ironclad_back_idle;
            else _spr = spr_ms_ironclad_back_idle;
        } else {
            if (string_pos("ballista", _suit_id) > 0) _spr = spr_ms_ballista_idle;
            else if (string_pos("centurion", _suit_id) > 0) _spr = spr_ms_centurion_idle;
            else if (string_pos("trenchcoat", _suit_id) > 0) _spr = spr_ms_trenchcoat_idle;
            else if (string_pos("zephyr", _suit_id) > 0) _spr = spr_ms_zephyr_idle;
            else if (string_pos("kepler", _suit_id) > 0) _spr = spr_ms_kepler_idle;
            else if (string_pos("oberon", _suit_id) > 0) _spr = spr_ms_oberon_idle;
            else if (string_pos("gorgon", _suit_id) > 0) _spr = spr_ms_gorgon_idle;
            else if (string_pos("bloodhound", _suit_id) > 0) _spr = spr_ms_bloodhound_idle;
            else if (string_pos("vandal", _suit_id) > 0) _spr = spr_ms_vandal_idle;
            else if (string_pos("ronin", _suit_id) > 0) _spr = spr_ms_ronin_idle;
            else if (string_pos("tessen", _suit_id) > 0) _spr = spr_ms_tessen_idle;
            else if (string_pos("kage", _suit_id) > 0 || string_pos("shinobi", _suit_id) > 0) _spr = spr_ms_kage_idle;
            else if (string_pos("aether", _suit_id) > 0 || string_pos("colony", _suit_id) > 0 || string_pos("sylph", _suit_id) > 0) _spr = spr_ms_aether_idle;
            else if (string_pos("hyena", _suit_id) > 0 || string_pos("syndicate", _suit_id) > 0 || string_pos("scrapper", _suit_id) > 0) _spr = spr_ms_hyena_idle;
            else if (string_pos("muramasa", _suit_id) > 0 || string_pos("zaibatsu", _suit_id) > 0) _spr = spr_ms_muramasa_idle;
            else if (string_pos("hephaestus", _suit_id) > 0) _spr = spr_ms_hephaestus_avatar;
            else if (string_pos("titan", _suit_id) > 0 || string_pos("juggernaut", _suit_id) > 0) _spr = spr_ms_titan_proto;
            else if (string_pos("siegebreaker", _suit_id) > 0) _spr = spr_ms_siegebreaker_anchor;
        }
    }

    // Conventional Vehicles & Infantry Squads lookup (doc 38)
    if (string_copy(_suit_id_str, 1, 4) == "veh_" || string_copy(_suit_id_str, 1, 4) == "inf_") {
        var _base_spr_name = "spr_" + _suit_id_str;
        var _action_suffix = "_idle";
        if (_state == "fire") _action_suffix = "_fire";
        else if (_state == "destroyed" || _state == "defeat") _action_suffix = "_defeat";
        else if (_is_back) _action_suffix = "_back_idle";

        var _cand = asset_get_index(_base_spr_name + _action_suffix);
        if (_cand != -1 && sprite_exists(_cand)) {
            _spr = _cand;
        } else {
            var _cand_idle = asset_get_index(_base_spr_name + "_idle");
            if (_cand_idle != -1 && sprite_exists(_cand_idle)) _spr = _cand_idle;
        }
    }

    // Action state sprite resolution for mechs (fire / destroyed)
    if (_state == "fire" && !_is_back) {
        var _cur_spr_name = sprite_get_name(_spr);
        if (string_pos("_idle", _cur_spr_name) > 0) {
            var _fire_cand_name = string_replace(_cur_spr_name, "_idle", "_fire");
            var _fire_cand = asset_get_index(_fire_cand_name);
            if (_fire_cand != -1 && sprite_exists(_fire_cand)) {
                _spr = _fire_cand;
            } else {
                var _fire_rifle = string_replace(_cur_spr_name, "_idle", "_fire_rifle");
                var _fr_asset = asset_get_index(_fire_rifle);
                if (_fr_asset != -1 && sprite_exists(_fr_asset)) _spr = _fr_asset;
            }
        }
    } else if (_state == "destroyed" && !_is_back) {
        var _cur_spr_name = sprite_get_name(_spr);
        var _dest_cand_name = string_replace(_cur_spr_name, "_idle", "_destroyed");
        var _dest_cand = asset_get_index(_dest_cand_name);
        if (_dest_cand != -1 && sprite_exists(_dest_cand)) {
            _spr = _dest_cand;
        }
    }

    // 2. Render Ground Ellipse Shadow (guarded for numeric coordinates)
    if (is_string(_x)) _x = real(_x) ?? 0;
    if (is_string(_y)) _y = real(_y) ?? 0;
    if (!is_numeric(_scale)) _scale = 1.0;
    var _shadow_w = 55 * _scale;
    var _shadow_h = 10 * _scale;
    draw_set_color(c_black);
    draw_set_alpha(0.40);
    draw_ellipse(_x - _shadow_w, _y - (_shadow_h * 0.8), _x + _shadow_w, _y + (_shadow_h * 1.2), false);
    draw_set_alpha(1.0);

    // 3. Frame Animation Index Selection
    var _num_frames = sprite_exists(_spr) ? sprite_get_number(_spr) : 1;
    var _sub = 0;

    if (_subimg_override >= 0) {
        _sub = _subimg_override % _num_frames;
    } else {
        // Desynchronized smooth multi-frame animation
        var _seed = abs(string_byte_at(_suit_id_str, 1) * 31 + string_byte_at(_suit_id_str, max(1, string_length(_suit_id_str))) * 19);
        if (_state == "fire") {
            _sub = 3 % _num_frames; // Fire/recoil frame
        } else if (_state == "walk") {
            _sub = (floor((current_time + _seed) / 120) % 2) + 2; // Stride cycle
            if (_sub >= _num_frames) _sub = 0;
        } else if (_state == "hit") {
            _sub = 1 % _num_frames;
        } else {
            // Idle breathing / vernier pulse (Frames 0 and 1)
            _sub = floor((current_time + _seed) / 250) % min(2, _num_frames);
        }
    }

    // 4. Dynamic Recoil / Hit Stagger Offsets & Origin Alignment
    var _orig_yo = sprite_exists(_spr) ? sprite_get_yoffset(_spr) : 145;
    var _draw_x = _x;
    var _draw_y = (_orig_yo > 0) ? _y : (_y - (145 * _scale));
    var _top_y = (_orig_yo > 0) ? (_y - (_orig_yo * _scale)) : (_y - (145 * _scale));
    var _draw_angle = 0;

    if (_state == "hit") {
        _draw_x += random_range(-3, 3) * _scale;
        _draw_y += random_range(-2, 2) * _scale;
        _draw_angle = -5 * _facing;
        _tint = merge_color(_tint, c_red, 0.4);
    } else if (_state == "fire") {
        _draw_x -= (4 * _facing) * _scale; // Barrel blowback
        _draw_angle = 2 * _facing;
    }

    // 5. Render Main 160x160 Mobile Suit Sprite
    if (sprite_exists(_spr)) {
        draw_sprite_ext(_spr, _sub, _draw_x, _draw_y, _scale * _facing, _scale, _draw_angle, _tint, 1.0);
    }

    // 6. Dynamic Reactor / Thruster Exhaust Emission Glow (Pulsating sine wave)
    var _glow_pulse = 0.4 + 0.3 * sin((current_time + string_byte_at(_suit_id_str, 1) * 10) / 180.0);
    draw_set_color(_sig_glow);

    if (_is_back) {
        // Twin rear backpack thruster plumes (Upper rear reactor manifold)
        draw_set_alpha(_glow_pulse * 0.85);
        draw_circle(_draw_x - (6 * _facing * _scale), _top_y + (76 * _scale), 7 * _scale, false);
        draw_circle(_draw_x + (14 * _facing * _scale), _top_y + (76 * _scale), 7 * _scale, false);
        draw_set_color(c_white);
        draw_set_alpha(_glow_pulse * 0.5);
        draw_circle(_draw_x - (6 * _facing * _scale), _top_y + (76 * _scale), 3 * _scale, false);
        draw_circle(_draw_x + (14 * _facing * _scale), _top_y + (76 * _scale), 3 * _scale, false);
        draw_set_alpha(1.0);
    } else {
        // Front atmospheric core vent glow
        draw_set_alpha(_glow_pulse * 0.7);
        draw_circle(_draw_x + (5 * _facing * _scale), _top_y + (80 * _scale), 12 * _scale, false);
        draw_set_alpha(1.0);
    }

    // 7. Weapon Muzzle Flash Rendering
    if (_state == "fire" && !_is_back) {
        draw_set_color(make_color_rgb(255, 230, 100));
        draw_set_alpha(0.85);
        var _muzzle_x = _draw_x + (45 * _facing * _scale);
        var _muzzle_y = _top_y + (65 * _scale);
        draw_circle(_muzzle_x, _muzzle_y, 16 * _scale, false);
        draw_set_color(c_white);
        draw_circle(_muzzle_x, _muzzle_y, 8 * _scale, false);
        draw_set_alpha(1.0);
    }
}
"""

with open(animator_path, "w") as f:
    f.write(animator_code)
print("[PASS] scr_draw_animated_mobile_suit.gml updated with modular custom socket renderer.")

