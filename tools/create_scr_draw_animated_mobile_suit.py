import os
import json

SCRIPT_DIR = "scripts/scr_draw_animated_mobile_suit"
os.makedirs(SCRIPT_DIR, exist_ok=True)

# 1. GML Script content
gml_code = '''/// @description Universal Mobile Suit Animator: Renders 160x160 3/4 isometric combat mechs with multi-frame idle, thruster pulse, weapon recoil, and faction paletting.
/// @param {String} _suit_id Mobile suit catalog ID (or blueprint ID)
/// @param {Real} _x Center X position on screen
/// @param {Real} _y Foot origin Y position on screen
/// @param {Real} _scale Scale factor (e.g. 1.0 for normal, 0.5-0.8 for UI cards)
/// @param {Real} _facing Directional facing (1 = Facing Right [Attacker], -1 = Facing Left [Defender])
/// @param {String} _state Animation state ("idle", "walk", "fire", "hit", "crippled", "destroyed")
/// @param {Real} _subimg_override Optional frame override (-1 for auto animation loop)
/// @param {Constant} _custom_blend Optional custom color blend (default c_white)
function scr_draw_animated_mobile_suit(_suit_id, _x, _y, _scale = 1.0, _facing = 1, _state = "idle", _subimg_override = -1, _custom_blend = c_white) {
    var _spr = spr_ms_ironclad_idle;
    var _tint = _custom_blend;
    var _sig_glow = make_color_rgb(255, 120, 40);
    var _chassis_name = "Mobile Suit";

    // 1. Resolve suit metadata from GameManager catalog if available
    if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "get_mobile_suit")) {
        var _suit = obj_GameManager.get_mobile_suit(_suit_id);
        if (!is_undefined(_suit) && is_struct(_suit)) {
            _chassis_name = _suit[$ "name"] ?? _chassis_name;
            var _spr_asset = _suit[$ "sprite_asset"];
            if (!is_undefined(_spr_asset) && sprite_exists(_spr_asset)) {
                _spr = _spr_asset;
            }
            // Resolve faction glow
            var _fac = _suit[$ "faction_id"] ?? "";
            if (_fac == "faction_b") _sig_glow = make_color_rgb(0, 240, 255);
            else if (_fac == "faction_c") _sig_glow = make_color_rgb(255, 140, 30);
            else if (_fac == "faction_d") _sig_glow = make_color_rgb(0, 255, 200);
        }
    }

    // Fallback heuristic based on ID keywords if sprite not yet assigned
    if (_spr == spr_ms_ironclad_idle) {
        if (string_pos("ballista", _suit_id) > 0) _spr = spr_ms_ballista_idle;
        else if (string_pos("zephyr", _suit_id) > 0) _spr = spr_ms_zephyr_idle;
        else if (string_pos("gorgon", _suit_id) > 0) _spr = spr_ms_gorgon_idle;
        else if (string_pos("kage", _suit_id) > 0 || string_pos("shinobi", _suit_id) > 0) _spr = spr_ms_kage_idle;
        else if (string_pos("aether", _suit_id) > 0 || string_pos("colony", _suit_id) > 0 || string_pos("sylph", _suit_id) > 0) _spr = spr_ms_aether_idle;
        else if (string_pos("hyena", _suit_id) > 0 || string_pos("syndicate", _suit_id) > 0 || string_pos("scrapper", _suit_id) > 0) _spr = spr_ms_hyena_idle;
        else if (string_pos("muramasa", _suit_id) > 0 || string_pos("zaibatsu", _suit_id) > 0 || string_pos("ronin", _suit_id) > 0) _spr = spr_ms_muramasa_idle;
        else if (string_pos("siegebreaker", _suit_id) > 0) _spr = spr_ms_siegebreaker_anchor;
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
    draw_set_alpha(_glow_pulse * 0.7);

    // Render subtle atmospheric engine core glow
    draw_circle(_draw_x + (5 * _facing * _scale), _draw_y + (80 * _scale), 12 * _scale, false);
    draw_set_alpha(1.0);

    // 7. Weapon Muzzle Flash Rendering
    if (_state == "fire") {
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
'''

with open(os.path.join(SCRIPT_DIR, "scr_draw_animated_mobile_suit.gml"), "w") as f:
    f.write(gml_code)

yy_data = {
    "$GMScript": "v1",
    "%Name": "scr_draw_animated_mobile_suit",
    "isCompatibility": False,
    "isDnD": False,
    "name": "scr_draw_animated_mobile_suit",
    "parent": {
        "name": "MechMakerConcept",
        "path": "MechMakerConcept.yyp"
    },
    "resourceType": "GMScript",
    "resourceVersion": "2.0"
}

with open(os.path.join(SCRIPT_DIR, "scr_draw_animated_mobile_suit.yy"), "w") as f:
    json.dump(yy_data, f, indent=2)

print("Created script scr_draw_animated_mobile_suit.gml and .yy")

# Register in MechMakerConcept.yyp
with open("MechMakerConcept.yyp", "r") as f:
    text = f.read()

target = '"name": "spr_ms_kage_idle",'
idx = text.find(target)
if idx != -1:
    entry = """    {
      "id": {
        "name": "scr_draw_animated_mobile_suit",
        "path": "scripts/scr_draw_animated_mobile_suit/scr_draw_animated_mobile_suit.yy"
      }
    },
"""
    # Find next closing brace of that entry
    end_entry = text.find("},", idx)
    insert_pos = text.find("    {", end_entry)
    if insert_pos == -1: # It is right before the closing bracket of resources
        bracket_pos = text.find("  ],", end_entry)
        text = text[:bracket_pos] + entry + text[bracket_pos:]
    else:
        text = text[:insert_pos] + entry + text[insert_pos:]
    with open("MechMakerConcept.yyp", "w") as f:
        f.write(text)
    print("Registered scr_draw_animated_mobile_suit in MechMakerConcept.yyp")
