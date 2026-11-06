#!/usr/bin/env python3
"""
Implement Material-Driven Chassis, Dynamic Alloy Palette Tinting,
and Forge Quality Tiers (S/A/B/C) into obj_DebugManager.
"""
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
create_path = os.path.join(PROJECT_ROOT, "objects", "obj_DebugManager", "Create_0.gml")
draw_path = os.path.join(PROJECT_ROOT, "objects", "obj_DebugManager", "Draw_64.gml")
step_path = os.path.join(PROJECT_ROOT, "objects", "obj_DebugManager", "Step_0.gml")

# --- 1. Update Create_0.gml ---
with open(create_path, "r") as f:
    create_src = f.read()

# Add builder_quality_idx, builder_quality_names, builder_quality_mults
old_subtab_decl = "builder_chassis_line = 0; // 0=Player PMC Proprietary Chassis, 1=Reverse-Engineered Foreign Factions"
new_subtab_decl = """builder_chassis_line = 0; // 0=Player PMC Proprietary Chassis, 1=Reverse-Engineered Foreign Factions
builder_quality_idx = 1; // 0=C-Standard, 1=B-MilSpec, 2=A-AceCustom, 3=S-SingularityMasterwork
builder_quality_names = [
    "C-TIER: INDUSTRIAL STANDARD (Baseline Yield)",
    "B-TIER: REFINED MIL-SPEC (+10% Stats, Combat Hardened)",
    "A-TIER: ACE CUSTOM PROTOTYPE (+20% Stats, Vernier Tuning)",
    "S-TIER: SINGULARITY MASTERWORK (+35% Stats, Radiant Sheen)"
];
builder_quality_badges = ["[C: INDUSTRIAL]", "[B: MIL-SPEC]", "[A: ACE PROTOTYPE]", "[S: MASTERWORK]"];
builder_quality_mults = [1.0, 1.10, 1.20, 1.35];"""

assert old_subtab_decl in create_src, "Could not find old_subtab_decl"
create_src = create_src.replace(old_subtab_decl, new_subtab_decl)

# Enhance builder_alloy_deltas with visual_finish, tint_color, and glow_color
old_alloys = """builder_alloy_deltas = [
    { armor_mult: 1.0, mass_mult: 1.0, speed_bonus: 0, desc: "Standard military baseline plating." },
    { armor_mult: 0.9, mass_mult: 0.85, speed_bonus: 15, desc: "Plasma-stabilized superconducting matrix." },
    { armor_mult: 0.8, mass_mult: 0.75, speed_bonus: 30, desc: "Ultralight vacuum-sintered vernier alloy." },
    { armor_mult: 1.45, mass_mult: 1.35, speed_bonus: -15, desc: "Super-dense impact-resistant adamantine slab." },
    { armor_mult: 1.2, mass_mult: 1.1, speed_bonus: -5, desc: "Composite tiles defeating kinetic shaped-charges." },
    { armor_mult: 1.35, mass_mult: 0.85, speed_bonus: 25, desc: "Self-healing pre-war molecular 3D lattice." }
];"""

new_alloys = """builder_alloy_deltas = [
    { armor_mult: 1.0, mass_mult: 1.0, speed_bonus: 0, desc: "Matte gunmetal olive-drab with carbon ballistic trim.", tint_color: make_color_rgb(230, 240, 230), glow_color: make_color_rgb(255, 255, 255) },
    { armor_mult: 0.9, mass_mult: 0.85, speed_bonus: 15, desc: "Deep cobalt navy with pulsing cyan superconducting lines.", tint_color: make_color_rgb(180, 220, 255), glow_color: make_color_rgb(0, 240, 255) },
    { armor_mult: 0.8, mass_mult: 0.75, speed_bonus: 30, desc: "Polished aerospace satin-white with gold vernier cowlings.", tint_color: make_color_rgb(255, 250, 240), glow_color: make_color_rgb(255, 220, 80) },
    { armor_mult: 1.45, mass_mult: 1.35, speed_bonus: -15, desc: "Blackened charred tungsten slab with industrial bronze joints.", tint_color: make_color_rgb(165, 165, 175), glow_color: make_color_rgb(255, 140, 40) },
    { armor_mult: 1.2, mass_mult: 1.1, speed_bonus: -5, desc: "Desert sand composite tiles absorbing shaped charges.", tint_color: make_color_rgb(240, 225, 195), glow_color: make_color_rgb(255, 200, 100) },
    { armor_mult: 1.35, mass_mult: 0.85, speed_bonus: 25, desc: "Midnight violet lattice with pulsating Cherenkov radiation.", tint_color: make_color_rgb(225, 195, 255), glow_color: make_color_rgb(200, 100, 255) }
];"""

assert old_alloys in create_src, "Could not find old_alloys"
create_src = create_src.replace(old_alloys, new_alloys)

# Update calculate_builder_telemetry with quality multiplier and visual tint
old_telemetry = """// Calculate Full Telemetry based on Chassis + Sintered Alloy + Researched Loadout
calculate_builder_telemetry = function() {
    var _chassis_list = get_canonical_chassis_list();
    var _c = _chassis_list[clamp(builder_chassis_idx, 0, array_length(_chassis_list) - 1)];

    var _alloy_d = builder_alloy_deltas[clamp(builder_alloy_idx, 0, array_length(builder_alloy_deltas) - 1)];
    var _wpn_p = builder_weapons_db.primary[clamp(builder_primary_wpn_idx, 0, array_length(builder_weapons_db.primary) - 1)];
    var _wpn_s = builder_weapons_db.secondary[clamp(builder_secondary_wpn_idx, 0, array_length(builder_weapons_db.secondary) - 1)];
    var _wpn_m = builder_weapons_db.melee[clamp(builder_melee_wpn_idx, 0, array_length(builder_weapons_db.melee) - 1)];
    var _sld   = builder_weapons_db.shield[clamp(builder_shield_idx, 0, array_length(builder_weapons_db.shield) - 1)];

    var _base_hp = variable_struct_exists(_c, "hp") ? _c.hp : 680;
    var _base_mass = variable_struct_exists(_c, "weight_tonnes") ? _c.weight_tonnes : 65.0;
    var _base_spd = variable_struct_exists(_c, "speed") ? _c.speed : 55;
    var _core_mw = variable_struct_exists(_c, "power_output") ? _c.power_output : 35;

    // Apply Sintered Alloy Scaling
    var _tot_armor = floor((_base_hp * _alloy_d.armor_mult) + _sld.armor_hp);
    var _tot_mass = floor((_base_mass * _alloy_d.mass_mult) + _wpn_p.mass + _wpn_s.mass + _wpn_m.mass + _sld.mass);
    var _max_capacity = floor(_base_mass * 1.55);
    var _mass_overloaded = (_tot_mass > _max_capacity);

    var _tot_draw = _wpn_p.power_draw + _wpn_s.power_draw + _wpn_m.power_draw + _sld.power_draw;
    var _net_power = _core_mw - _tot_draw;
    var _reactor_overloaded = (_net_power < 0);

    var _final_spd = max(20, floor((_base_spd + _alloy_d.speed_bonus) * (1.0 - (_tot_mass / 250.0))));
    var _boost_spd = _final_spd + 45;
    var _oss = floor((_tot_armor / 5) + _wpn_p.damage + (_wpn_m.damage / 2) + (_final_spd / 2) + max(0, _net_power * 3));

    var _w_class = "MEDIUM MAINSTAY";
    if (_tot_mass < 55) _w_class = "LIGHT SKIRMISHER";
    else if (_tot_mass >= 55 && _tot_mass < 82) _w_class = "MEDIUM MAINSTAY";
    else if (_tot_mass >= 82 && _tot_mass < 105) _w_class = "HEAVY ASSAULT";
    else _w_class = "SUPERHEAVY SIEGEBREAKER";

    return {
        chassis: _c, alloy_delta: _alloy_d,
        primary_wpn: _wpn_p, secondary_wpn: _wpn_s, melee_wpn: _wpn_m, shield: _sld,
        total_armor: _tot_armor, total_mass: _tot_mass, max_capacity: _max_capacity,
        mass_overloaded: _mass_overloaded, power_output: _core_mw, total_draw: _tot_draw,
        net_power: _net_power, reactor_overloaded: _reactor_overloaded,
        walk_speed: _final_spd, boost_speed: _boost_spd, combat_rating: _oss,
        weight_class: _w_class, preview_sprite: _c.sprite_asset,
        sprites: _c.sprites
    };
};"""

new_telemetry = """// Calculate Full Telemetry based on Chassis + Sintered Alloy + Quality Tier + Researched Loadout
calculate_builder_telemetry = function() {
    var _chassis_list = get_canonical_chassis_list();
    var _c = _chassis_list[clamp(builder_chassis_idx, 0, array_length(_chassis_list) - 1)];

    var _alloy_d = builder_alloy_deltas[clamp(builder_alloy_idx, 0, array_length(builder_alloy_deltas) - 1)];
    var _q_mult = builder_quality_mults[clamp(builder_quality_idx, 0, array_length(builder_quality_mults) - 1)];
    var _wpn_p = builder_weapons_db.primary[clamp(builder_primary_wpn_idx, 0, array_length(builder_weapons_db.primary) - 1)];
    var _wpn_s = builder_weapons_db.secondary[clamp(builder_secondary_wpn_idx, 0, array_length(builder_weapons_db.secondary) - 1)];
    var _wpn_m = builder_weapons_db.melee[clamp(builder_melee_wpn_idx, 0, array_length(builder_weapons_db.melee) - 1)];
    var _sld   = builder_weapons_db.shield[clamp(builder_shield_idx, 0, array_length(builder_weapons_db.shield) - 1)];

    var _base_hp = variable_struct_exists(_c, "hp") ? _c.hp : 680;
    var _base_mass = variable_struct_exists(_c, "weight_tonnes") ? _c.weight_tonnes : 65.0;
    var _base_spd = variable_struct_exists(_c, "speed") ? _c.speed : 55;
    var _core_mw = variable_struct_exists(_c, "power_output") ? _c.power_output : 35;

    // Apply Sintered Alloy & Quality Tier Scaling
    var _tot_armor = floor(((_base_hp * _alloy_d.armor_mult) + _sld.armor_hp) * _q_mult);
    var _tot_mass = floor((_base_mass * _alloy_d.mass_mult) + _wpn_p.mass + _wpn_s.mass + _wpn_m.mass + _sld.mass);
    var _max_capacity = floor(_base_mass * 1.55);
    var _mass_overloaded = (_tot_mass > _max_capacity);

    var _tot_draw = _wpn_p.power_draw + _wpn_s.power_draw + _wpn_m.power_draw + _sld.power_draw;
    var _scaled_core = floor(_core_mw * _q_mult);
    var _net_power = _scaled_core - _tot_draw;
    var _reactor_overloaded = (_net_power < 0);

    var _final_spd = max(20, floor(((_base_spd + _alloy_d.speed_bonus) * (1.0 - (_tot_mass / 250.0))) * (1.0 + ((_q_mult - 1.0) * 0.5))));
    var _boost_spd = _final_spd + 45;
    var _oss = floor(((_tot_armor / 5) + _wpn_p.damage + (_wpn_m.damage / 2) + (_final_spd / 2) + max(0, _net_power * 3)) * _q_mult);

    var _w_class = "MEDIUM MAINSTAY";
    if (_tot_mass < 55) _w_class = "LIGHT SKIRMISHER";
    else if (_tot_mass >= 55 && _tot_mass < 82) _w_class = "MEDIUM MAINSTAY";
    else if (_tot_mass >= 82 && _tot_mass < 105) _w_class = "HEAVY ASSAULT";
    else _w_class = "SUPERHEAVY SIEGEBREAKER";

    return {
        chassis: _c, alloy_delta: _alloy_d, quality_mult: _q_mult, quality_idx: builder_quality_idx,
        primary_wpn: _wpn_p, secondary_wpn: _wpn_s, melee_wpn: _wpn_m, shield: _sld,
        total_armor: _tot_armor, total_mass: _tot_mass, max_capacity: _max_capacity,
        mass_overloaded: _mass_overloaded, power_output: _scaled_core, total_draw: _tot_draw,
        net_power: _net_power, reactor_overloaded: _reactor_overloaded,
        walk_speed: _final_spd, boost_speed: _boost_spd, combat_rating: _oss,
        weight_class: _w_class, preview_sprite: _c.sprite_asset,
        sprites: _c.sprites,
        tint: _alloy_d.tint_color,
        glow: _alloy_d.glow_color
    };
};"""

assert old_telemetry in create_src, "Could not find old_telemetry"
create_src = create_src.replace(old_telemetry, new_telemetry)

with open(create_path, "w") as f:
    f.write(create_src)
print("Create_0.gml updated with Quality Tiers and Alloy Palettes.")

# --- 2. Update Draw_64.gml ---
with open(draw_path, "r") as f:
    draw_src = f.read()

# Update sprite drawing on gantry to use alloy tint and masterwork glow
old_gantry_draw = """    if (sprite_exists(_draw_spr)) {
        var _sub = floor(builder_subimg) % sprite_get_number(_draw_spr);
        draw_sprite_ext(_draw_spr, _sub, _gcx, _gcy + 45, builder_preview_scale, builder_preview_scale, 0, c_white, 1.0);
    }"""

new_gantry_draw = """    if (sprite_exists(_draw_spr)) {
        var _sub = floor(builder_subimg) % sprite_get_number(_draw_spr);
        // Base Sprite with Sintered Material Alloy Tint
        draw_sprite_ext(_draw_spr, _sub, _gcx, _gcy + 45, builder_preview_scale, builder_preview_scale, 0, _t.tint, 1.0);

        // Radiant Singularity Masterwork Sheen (S-Tier or Tachyon)
        if (builder_quality_idx == 3 || builder_alloy_idx == 5) {
            gpu_set_blendmode(bm_add);
            draw_sprite_ext(_draw_spr, _sub, _gcx, _gcy + 45, builder_preview_scale, builder_preview_scale, 0, _t.glow, 0.22 + 0.14 * sin(current_time * 0.005));
            gpu_set_blendmode(bm_normal);
        }
    }"""

assert old_gantry_draw in draw_src, "Could not find old_gantry_draw"
draw_src = draw_src.replace(old_gantry_draw, new_gantry_draw)

# Update Callsign Banner to show Quality Tier badge and cycle button
old_ban = """    // Callsign Banner & Auto-Tune Button
    var _ban_y = _hng_y + 550;
    draw_set_color(make_color_rgb(140, 170, 200));
    draw_text(_hng_x + 20, _ban_y, "CUSTOM CALLSIGN:");
    draw_set_color(make_color_rgb(255, 220, 80));
    draw_text(_hng_x + 165, _ban_y, builder_custom_name);

    draw_set_color(make_color_rgb(140, 170, 200));
    draw_text(_hng_x + 360, _ban_y, "DOCTRINE ROLE:");
    draw_set_color(c_white);
    draw_text(_hng_x + 480, _ban_y, string_copy(_t.chassis.doctrine, 1, 24));"""

new_ban = """    // Callsign Banner & Quality Tier Badge
    var _ban_y = _hng_y + 540;
    draw_set_color(make_color_rgb(140, 170, 200));
    draw_text(_hng_x + 20, _ban_y, "CUSTOM CALLSIGN:");
    draw_set_color(make_color_rgb(255, 220, 80));
    draw_text(_hng_x + 165, _ban_y, builder_custom_name);

    draw_set_color(make_color_rgb(140, 170, 200));
    draw_text(_hng_x + 360, _ban_y, "QUALITY TIER:");
    var _q_col = (builder_quality_idx == 3) ? make_color_rgb(255, 100, 255) : ((builder_quality_idx == 2) ? make_color_rgb(255, 220, 80) : ((builder_quality_idx == 1) ? c_aqua : c_white));
    draw_set_color(_q_col);
    draw_text(_hng_x + 470, _ban_y, builder_quality_badges[builder_quality_idx]);

    draw_set_color(make_color_rgb(140, 170, 200));
    draw_text(_hng_x + 20, _ban_y + 24, "FINISH:");
    draw_set_color(_t.glow);
    draw_text(_hng_x + 85, _ban_y + 24, string_copy(_t.alloy_delta.desc, 1, 55));"""

assert old_ban in draw_src, "Could not find old_ban"
draw_src = draw_src.replace(old_ban, new_ban)

# Update Subtab 3 (Rollout) to include Quality Tier Selector buttons
old_rollout_subtab = """        // Overload Safety Alert Box
        _ty += 38;
        if (_t.reactor_overloaded) {
            draw_set_color(c_red);
            draw_rectangle(_eng_x + 28, _ty, _eng_x + _eng_w - 28, _ty + 34, false);
            draw_set_color(c_white);
            draw_text(_eng_x + 36, _ty + 8, "! REACTOR OVERLOAD: POWER DRAW EXCEEDS CORE GENERATION !");
            _ty += 46;
        } else {
            draw_set_color(make_color_rgb(18, 48, 30));
            draw_rectangle(_eng_x + 28, _ty, _eng_x + _eng_w - 28, _ty + 34, false);
            draw_set_color(c_lime);
            draw_text(_eng_x + 36, _ty + 8, "v POWER GRID STABLE // READY FOR COMBAT PROVING");
            _ty += 46;
        }"""

new_rollout_subtab = """        // Quality Tier Selector
        _ty += 30;
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 28, _ty, "SELECT FORGE CRUCIBLE PURITY / QUALITY TIER:");
        _ty += 22;
        var _qw = (_eng_w - 56 - 18) / 4;
        for (var q = 0; q < 4; q++) {
            var _qx = _eng_x + 28 + (q * (_qw + 6));
            var _q_hov = (_mx >= _qx && _mx <= _qx + _qw && _my >= _ty && _my <= _ty + 30);
            var _q_act = (builder_quality_idx == q);
            if (_q_hov && _click) {
                builder_quality_idx = q;
                scr_audio_play_ui("click");
            }
            var _q_btn_col = (q == 3) ? make_color_rgb(255, 100, 255) : ((q == 2) ? make_color_rgb(255, 220, 80) : ((q == 1) ? c_aqua : c_white));
            scr_draw_snes_button(_qx, _ty, _qw, 30, builder_quality_badges[q], _q_hov || _q_act, _q_act, _q_btn_col);
        }
        _ty += 40;

        // Overload Safety Alert Box
        if (_t.reactor_overloaded) {
            draw_set_color(c_red);
            draw_rectangle(_eng_x + 28, _ty, _eng_x + _eng_w - 28, _ty + 34, false);
            draw_set_color(c_white);
            draw_text(_eng_x + 36, _ty + 8, "! REACTOR OVERLOAD: POWER DRAW EXCEEDS CORE GENERATION !");
            _ty += 46;
        } else {
            draw_set_color(make_color_rgb(18, 48, 30));
            draw_rectangle(_eng_x + 28, _ty, _eng_x + _eng_w - 28, _ty + 34, false);
            draw_set_color(c_lime);
            draw_text(_eng_x + 36, _ty + 8, "v POWER GRID STABLE // READY FOR COMBAT PROVING");
            _ty += 46;
        }"""

assert old_rollout_subtab in draw_src, "Could not find old_rollout_subtab"
draw_src = draw_src.replace(old_rollout_subtab, new_rollout_subtab)

with open(draw_path, "w") as f:
    f.write(draw_src)
print("Draw_64.gml updated with Gantry Tinting, Sheen, and Quality Tier Selector.")

# --- 3. Update Step_0.gml for Quality Hotkey ---
with open(step_path, "r") as f:
    step_src = f.read()

old_step_subtab3 = """    } else if (builder_subtab == 3) {
        // Rollout shortcuts
        if (keyboard_check_pressed(vk_enter)) {
            deploy_builder_mech_to_combat();
        }
    }"""

new_step_subtab3 = """    } else if (builder_subtab == 3) {
        // Rollout shortcuts
        if (keyboard_check_pressed(vk_left) || keyboard_check_pressed(vk_up)) {
            builder_quality_idx = (builder_quality_idx - 1 + 4) % 4;
            scr_audio_play_ui("click");
        } else if (keyboard_check_pressed(vk_right) || keyboard_check_pressed(vk_down)) {
            builder_quality_idx = (builder_quality_idx + 1) % 4;
            scr_audio_play_ui("click");
        }
        if (keyboard_check_pressed(vk_enter)) {
            deploy_builder_mech_to_combat();
        }
    }"""

assert old_step_subtab3 in step_src, "Could not find old_step_subtab3"
step_src = step_src.replace(old_step_subtab3, new_step_subtab3)

with open(step_path, "w") as f:
    f.write(step_src)
print("Step_0.gml updated with Quality Hotkeys.")
