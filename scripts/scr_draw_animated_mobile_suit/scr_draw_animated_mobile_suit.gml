/// @description Universal Mobile Suit Animator: Renders 160x160 3/4 isometric combat mechs with multi-frame idle, thruster pulse, weapon recoil, and faction paletting across both FRONT and BACK perspectives.
/// @param {String} _suit_id Mobile suit catalog ID (or blueprint ID)
/// @param {Real} _x Center X position on screen
/// @param {Real} _y Foot origin Y position on screen
/// @param {Real} _scale Scale factor (e.g. 1.0 for normal, 0.5-0.8 for UI cards)
/// @param {Real} _facing Directional facing (1 = Facing Right [Attacker/SE/NE], -1 = Facing Left [Defender/SW/NW])
/// @param {String} _state Animation state ("idle", "walk", "fire", "hit", "crippled", "destroyed")
/// @param {Real} _subimg_override Optional frame override (-1 for auto animation loop)
/// @param {Constant} _custom_blend Optional custom color blend (default c_white)
/// @param {String} _perspective Isometric perspective ("front" or "back", default "front")
function scr_draw_animated_mobile_suit(_suit_id, _x, _y, _scale = 1.0, _facing = 1, _state = "idle", _subimg_override = -1, _custom_blend = c_white, _perspective = "front") {
    var _is_back = (_perspective == "back" || _perspective == "rear");
    var _spr = _is_back ? spr_ms_ironclad_back_idle : spr_ms_ironclad_idle;
    var _tint = _custom_blend;
    var _sig_glow = make_color_rgb(255, 120, 40);
    var _chassis_name = "Mobile Suit";

    // 1. Resolve suit metadata from GameManager catalog if available
    if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "get_mobile_suit")) {
        var _suit = obj_GameManager.get_mobile_suit(_suit_id);
        if (!is_undefined(_suit) && is_struct(_suit)) {
            _chassis_name = _suit[$ "name"] ?? _chassis_name;
            var _spr_asset = _suit[$ "sprite_asset"];
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
            var _fac = _suit[$ "faction_id"] ?? "";
            if (_fac == "faction_b") _sig_glow = make_color_rgb(0, 240, 255);
            else if (_fac == "faction_c") _sig_glow = make_color_rgb(255, 140, 30);
            else if (_fac == "faction_d") _sig_glow = make_color_rgb(0, 255, 200);
            else if (_fac == "pmc_player") _sig_glow = make_color_rgb(255, 215, 80);
        }
    }

    // Direct keyword mapping heuristics for all 16 mass-production candidates & apex prototypes
    if (_spr == spr_ms_ironclad_idle || _spr == spr_ms_ironclad_back_idle) {
        if (_is_back) {
            if (string_pos("custom_biped", _suit_id) > 0 || string_pos("vanguard_heavy", _suit_id) > 0) _spr = spr_ms_custom_biped_heavy_back_idle;
            else if (string_pos("custom_hover", _suit_id) > 0 || string_pos("ghost_sniper", _suit_id) > 0) _spr = spr_ms_custom_hover_sniper_back_idle;
            else if (string_pos("custom_tread", _suit_id) > 0 || string_pos("scrapper_brawler", _suit_id) > 0) _spr = spr_ms_custom_tread_artillery_back_idle;
            else if (string_pos("custom_aero", _suit_id) > 0 || string_pos("stratos_interceptor", _suit_id) > 0) _spr = spr_ms_custom_aero_striker_back_idle;
            else if (string_pos("ballista", _suit_id) > 0) _spr = spr_ms_ballista_back_idle;
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
            if (string_pos("custom_biped", _suit_id) > 0 || string_pos("vanguard_heavy", _suit_id) > 0) _spr = spr_ms_custom_biped_heavy_idle;
            else if (string_pos("custom_hover", _suit_id) > 0 || string_pos("ghost_sniper", _suit_id) > 0) _spr = spr_ms_custom_hover_sniper_idle;
            else if (string_pos("custom_tread", _suit_id) > 0 || string_pos("scrapper_brawler", _suit_id) > 0) _spr = spr_ms_custom_tread_artillery_idle;
            else if (string_pos("custom_aero", _suit_id) > 0 || string_pos("stratos_interceptor", _suit_id) > 0) _spr = spr_ms_custom_aero_striker_idle;
            else if (string_pos("ballista", _suit_id) > 0) _spr = spr_ms_ballista_idle;
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

    // 2. Render Ground Ellipse Shadow
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
        var _seed = abs(string_byte_at(_suit_id, 1) * 31 + string_byte_at(_suit_id, max(1, string_length(_suit_id))) * 19);
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

    // 4. Dynamic Recoil / Hit Stagger Offsets
    var _draw_x = _x;
    var _draw_y = _y - (145 * _scale); // Align foot origin at _y
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
    var _glow_pulse = 0.4 + 0.3 * sin((current_time + string_byte_at(_suit_id, 1) * 10) / 180.0);
    draw_set_color(_sig_glow);

    if (_is_back) {
        // Twin rear backpack thruster plumes (Upper rear reactor manifold)
        draw_set_alpha(_glow_pulse * 0.85);
        draw_circle(_draw_x - (6 * _facing * _scale), _draw_y + (76 * _scale), 7 * _scale, false);
        draw_circle(_draw_x + (14 * _facing * _scale), _draw_y + (76 * _scale), 7 * _scale, false);
        draw_set_color(c_white);
        draw_set_alpha(_glow_pulse * 0.5);
        draw_circle(_draw_x - (6 * _facing * _scale), _draw_y + (76 * _scale), 3 * _scale, false);
        draw_circle(_draw_x + (14 * _facing * _scale), _draw_y + (76 * _scale), 3 * _scale, false);
        draw_set_alpha(1.0);
    } else {
        // Front atmospheric core vent glow
        draw_set_alpha(_glow_pulse * 0.7);
        draw_circle(_draw_x + (5 * _facing * _scale), _draw_y + (80 * _scale), 12 * _scale, false);
        draw_set_alpha(1.0);
    }

    // 7. Weapon Muzzle Flash Rendering
    if (_state == "fire" && !_is_back) {
        draw_set_color(make_color_rgb(255, 230, 100));
        draw_set_alpha(0.85);
        var _muzzle_x = _draw_x + (45 * _facing * _scale);
        var _muzzle_y = _draw_y + (65 * _scale);
        draw_circle(_muzzle_x, _muzzle_y, 16 * _scale, false);
        draw_set_color(c_white);
        draw_circle(_muzzle_x, _muzzle_y, 8 * _scale, false);
        draw_set_alpha(1.0);
    }
}
