#!/usr/bin/env python3
"""
Patch obj_DebugManager Create_0.gml and Draw_64.gml for:
1. Unique Player PMC Chassis Platforms (PMC-01 to PMC-00 with custom sprites).
2. Defensive safe reads for _cur_atk.alloy and _cur_def.alloy.
3. Complete alloy/chassis/era initialization on deployed custom mechs.
"""
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
create_path = os.path.join(PROJECT_ROOT, "objects", "obj_DebugManager", "Create_0.gml")
draw_path = os.path.join(PROJECT_ROOT, "objects", "obj_DebugManager", "Draw_64.gml")

# --- 1. Patch Create_0.gml ---
with open(create_path, "r") as f:
    create_src = f.read()

# Add builder_chassis_line
if "builder_chassis_line" not in create_src:
    create_src = create_src.replace(
        'builder_subtab = 0; // 0=Chassis & Role, 1=Alloy Plating, 2=Researched Weapons, 3=Telemetry & Rollout',
        'builder_subtab = 0; // 0=Chassis & Role, 1=Alloy Plating, 2=Researched Weapons, 3=Telemetry & Rollout\nbuilder_chassis_line = 0; // 0=Player PMC Proprietary Chassis, 1=Reverse-Engineered Foreign Factions'
    )

# Replace get_canonical_chassis_list with Player Custom Chassis Catalog + Toggle
old_chassis_fn = '''// Retrieve Canonical Chassis Catalog
get_canonical_chassis_list = function() {
    var _list = [];
    for (var i = 0; i < array_length(master_roster); i++) {
        var _u = master_roster[i];
        if (_u.category == "MOBILE_SUIT") {
            var _hp_val = variable_struct_exists(_u, "hp") ? _u.hp : 680;
            if (!variable_struct_exists(_u, "power_output")) {
                _u.power_output = floor(28 + (_hp_val / 30));
            }
            if (!variable_struct_exists(_u, "weight_tonnes")) {
                _u.weight_tonnes = floor(38 + (_hp_val / 22));
            }
            if (!variable_struct_exists(_u, "speed")) {
                var _ch = variable_struct_exists(_u, "chassis") ? _u.chassis : "biped";
                _u.speed = (string_pos("hover", _ch) > 0) ? 80 : ((string_pos("tread", _ch) > 0) ? 35 : 55);
            }
            array_push(_list, _u);
        }
    }
    if (array_length(_list) == 0 && array_length(master_roster) > 0) {
        var _first = master_roster[0];
        if (!variable_struct_exists(_first, "power_output")) _first.power_output = 35;
        if (!variable_struct_exists(_first, "weight_tonnes")) _first.weight_tonnes = 65;
        if (!variable_struct_exists(_first, "speed")) _first.speed = 55;
        array_push(_list, _first);
    }
    return _list;
};'''

new_chassis_fn = '''// Player PMC Bespoke Foundry Chassis Catalog (Completely Unique Player Mobile Suits)
get_player_custom_chassis_catalog = function() {
    return [
        {
            id: "bp_player_vanguard_heavy",
            model_code: "PMC-01",
            name: "PMC-01 Vanguard Breaker",
            faction_id: "pmc_player",
            category: "PLAYER_PMC_CHASSIS",
            chassis: "Heavy Bipedal Walker",
            move_type: "biped",
            alloy: "alloy_vanguard_comp",
            sprite_asset: spr_ms_custom_biped_heavy_idle,
            sprite_back_asset: spr_ms_custom_biped_heavy_back_idle,
            sprites: {
                idle: spr_ms_custom_biped_heavy_idle,
                back_idle: spr_ms_custom_biped_heavy_back_idle,
                boost: spr_ms_ironclad_boost,
                melee: spr_ms_ironclad_attack_melee,
                fire: spr_ms_ironclad_fire_rifle,
                damaged: spr_ms_ironclad_idle_damaged,
                destroyed: spr_ms_ironclad_destroyed
            },
            weapon_name: "Type-77 120mm Solid Kinetic Cannon",
            weapon_class: "BALLISTIC",
            hp: 880,
            armor: 38,
            weight_tonnes: 60,
            power_output: 42,
            speed: 55,
            era: 2,
            doctrine: "Heavy Frontline Vanguard Linebreaker",
            lore: "Proprietary heavy assault frame engineered with reinforced modular hardpoints and high-impact kinetic hydraulics."
        },
        {
            id: "bp_player_stratos_interceptor",
            model_code: "PMC-02",
            name: "PMC-02 Stratos Interceptor",
            faction_id: "pmc_player",
            category: "PLAYER_PMC_CHASSIS",
            chassis: "High-G Vector Aero Frame",
            move_type: "aero",
            alloy: "alloy_aerosteel_flux",
            sprite_asset: spr_ms_custom_aero_striker_idle,
            sprite_back_asset: spr_ms_custom_aero_striker_back_idle,
            sprites: {
                idle: spr_ms_custom_aero_striker_idle,
                back_idle: spr_ms_custom_aero_striker_back_idle,
                boost: spr_ms_aether_boost,
                melee: spr_ms_aether_attack_saber,
                fire: spr_ms_aether_fire_beam,
                damaged: -1,
                destroyed: -1
            },
            weapon_name: "Type-6A Thermal Beam Rifle",
            weapon_class: "BEAM_PULSE",
            hp: 620,
            armor: 22,
            weight_tonnes: 42,
            power_output: 48,
            speed: 95,
            era: 2,
            doctrine: "Ultra-Agile Vector Vernier Skirmisher",
            lore: "High-mobility aerospace duelist chassis forged with Cherenkov thrusters for extreme evasive space interception."
        },
        {
            id: "bp_player_scrapper_brawler",
            model_code: "PMC-03",
            name: "PMC-03 Scrapper Brawler",
            faction_id: "pmc_player",
            category: "PLAYER_PMC_CHASSIS",
            chassis: "Continuous Sintered Track Assembly",
            move_type: "tread",
            alloy: "alloy_adamantine_carbide",
            sprite_asset: spr_ms_custom_tread_artillery_idle,
            sprite_back_asset: spr_ms_custom_tread_artillery_back_idle,
            sprites: {
                idle: spr_ms_custom_tread_artillery_idle,
                back_idle: spr_ms_custom_tread_artillery_back_idle,
                boost: spr_ms_custom_tread_artillery_idle,
                melee: spr_ms_hyena_attack_claw,
                fire: spr_ms_hyena_fire_flak,
                damaged: -1,
                destroyed: -1
            },
            weapon_name: "Heavy Recoil-Dampened Flak Howitzer",
            weapon_class: "EXPLOSIVE",
            hp: 980,
            armor: 42,
            weight_tonnes: 78,
            power_output: 36,
            speed: 35,
            era: 2,
            doctrine: "Continuous-Track Heavy Demolition Artillery",
            lore: "Heavily armored tracked chassis designed to withstand point-blank kinetic impacts and anchor heavy siege howitzers."
        },
        {
            id: "bp_player_ghost_sniper",
            model_code: "PMC-04",
            name: "PMC-04 Ghost Recon Sniper",
            faction_id: "pmc_player",
            category: "PLAYER_PMC_CHASSIS",
            chassis: "Anti-Grav Hover Repulsor",
            move_type: "hover",
            alloy: "alloy_hyperion_matrix",
            sprite_asset: spr_ms_custom_hover_sniper_idle,
            sprite_back_asset: spr_ms_custom_hover_sniper_back_idle,
            sprites: {
                idle: spr_ms_custom_hover_sniper_idle,
                back_idle: spr_ms_custom_hover_sniper_back_idle,
                boost: spr_ms_custom_hover_sniper_idle,
                melee: spr_ms_muramasa_attack_blade,
                fire: spr_ms_muramasa_fire_plasma,
                damaged: -1,
                destroyed: -1
            },
            weapon_name: "Electromagnetic Interdictor Railgun",
            weapon_class: "RAILGUN",
            hp: 560,
            armor: 24,
            weight_tonnes: 38,
            power_output: 52,
            speed: 80,
            era: 2,
            doctrine: "Low-Radar Gyroscopic Hover Interdictor",
            lore: "Stealth-coated hover frame equipped with gyroscopic stabilization and optical scattering matrices for long-range interdiction."
        },
        {
            id: "bp_player_hephaestus_avatar",
            model_code: "PMC-00",
            name: "PMC-00 Hephaestus Prime",
            faction_id: "pmc_player",
            category: "PLAYER_PMC_CHASSIS",
            chassis: "Archeotech Singularity Dreadnought",
            move_type: "biped",
            alloy: "alloy_tachyon_superalloy",
            sprite_asset: spr_ms_hephaestus_avatar,
            sprite_back_asset: spr_ms_hephaestus_avatar_back_idle,
            sprites: {
                idle: spr_ms_hephaestus_avatar,
                back_idle: spr_ms_hephaestus_avatar_back_idle,
                boost: spr_ms_titan_proto,
                melee: spr_ms_muramasa_attack_blade,
                fire: spr_ms_aether_fire_beam,
                damaged: -1,
                destroyed: -1
            },
            weapon_name: "Archeotech Singularity Tachyon Lance",
            weapon_class: "BEAM_PULSE",
            hp: 1450,
            armor: 55,
            weight_tonnes: 95,
            power_output: 75,
            speed: 65,
            era: 3,
            doctrine: "Foundry Ship Sovereign War Avatar",
            lore: "The personal war avatar of the USN-X Hephaestus, harnessing the vessel\'s miniature Singularity crucible."
        }
    ];
};

// Retrieve Canonical Chassis Catalog (Player Bespoke Foundry Platforms by Default)
get_canonical_chassis_list = function() {
    if (builder_chassis_line == 0) {
        return get_player_custom_chassis_catalog();
    }
    // builder_chassis_line == 1: Foreign Reverse-Engineered Factions
    var _list = [];
    for (var i = 0; i < array_length(master_roster); i++) {
        var _u = master_roster[i];
        if (_u.category == "MOBILE_SUIT" && _u.faction_id != "pmc_player") {
            var _hp_val = variable_struct_exists(_u, "hp") ? _u.hp : 680;
            if (!variable_struct_exists(_u, "power_output")) _u.power_output = floor(28 + (_hp_val / 30));
            if (!variable_struct_exists(_u, "weight_tonnes")) _u.weight_tonnes = floor(38 + (_hp_val / 22));
            if (!variable_struct_exists(_u, "speed")) {
                var _ch = variable_struct_exists(_u, "chassis") ? _u.chassis : "biped";
                _u.speed = (string_pos("hover", _ch) > 0) ? 80 : ((string_pos("tread", _ch) > 0) ? 35 : 55);
            }
            array_push(_list, _u);
        }
    }
    if (array_length(_list) == 0) return get_player_custom_chassis_catalog();
    return _list;
};'''

assert old_chassis_fn in create_src, "Could not find old_chassis_fn in Create_0.gml"
create_src = create_src.replace(old_chassis_fn, new_chassis_fn)

# Patch deploy_builder_mech_to_combat to guarantee alloy, alloy_id, chassis, and era
old_deploy = '''    var _custom_u = {
        id: "custom_test_" + string(irandom(9999)),
        name: builder_custom_name,
        faction_id: "pmc_player",
        category: "CUSTOM_MECH",
        move_type: variable_struct_exists(_t.chassis, "move_type") ? _t.chassis.move_type : "biped",
        alloy_id: builder_alloys[builder_alloy_idx],
        sprite_asset: _t.chassis.sprite_asset,'''

new_deploy = '''    var _custom_u = {
        id: "custom_test_" + string(irandom(9999)),
        name: builder_custom_name,
        faction_id: "pmc_player",
        category: "CUSTOM_MECH",
        move_type: variable_struct_exists(_t.chassis, "move_type") ? _t.chassis.move_type : "biped",
        chassis: variable_struct_exists(_t.chassis, "chassis") ? _t.chassis.chassis : "biped",
        alloy_id: builder_alloys[builder_alloy_idx],
        alloy: builder_alloys[builder_alloy_idx],
        era: 2,
        sprite_asset: _t.chassis.sprite_asset,'''

assert old_deploy in create_src, "Could not find old_deploy in Create_0.gml"
create_src = create_src.replace(old_deploy, new_deploy)

with open(create_path, "w") as f:
    f.write(create_src)
print("Create_0.gml successfully patched with unique player chassis catalog and full deployment fields.")

# --- 2. Patch Draw_64.gml ---
with open(draw_path, "r") as f:
    draw_src = f.read()

# Defend against missing alloy on attacker
old_atk_alloy = 'draw_text(_col1_x + 22, _col1_y + 322, "ALLOY: " + _cur_atk.alloy);'
new_atk_alloy = 'var _atk_alloy_str = variable_struct_exists(_cur_atk, "alloy") ? _cur_atk.alloy : (variable_struct_exists(_cur_atk, "alloy_id") ? _cur_atk.alloy_id : "Vanguard Composite");\n    draw_text(_col1_x + 22, _col1_y + 322, "ALLOY: " + string(_atk_alloy_str));'
assert old_atk_alloy in draw_src, "Could not find old_atk_alloy in Draw_64.gml"
draw_src = draw_src.replace(old_atk_alloy, new_atk_alloy)

# Defend against missing alloy on defender
old_def_alloy = 'draw_text(_col3_x + 22, _col3_y + 322, "ALLOY: " + _cur_def.alloy);'
new_def_alloy = 'var _def_alloy_str = variable_struct_exists(_cur_def, "alloy") ? _cur_def.alloy : (variable_struct_exists(_cur_def, "alloy_id") ? _cur_def.alloy_id : "Vanguard Composite");\n    draw_text(_col3_x + 22, _col3_y + 322, "ALLOY: " + string(_def_alloy_str));'
assert old_def_alloy in draw_src, "Could not find old_def_alloy in Draw_64.gml"
draw_src = draw_src.replace(old_def_alloy, new_def_alloy)

# Add Platform Line toggle and dynamic presets in Subtab 0
old_subtab0 = '''    if (builder_subtab == 0) {
        var _clist = get_canonical_chassis_list();
        var _c = _t.chassis;

        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 20, _deck_y, "BASE MOBILE SUIT CHASSIS PLATFORM:");

        // Chassis Card
        var _cc_y = _deck_y + 24;'''

new_subtab0 = '''    if (builder_subtab == 0) {
        var _clist = get_canonical_chassis_list();
        var _c = _t.chassis;

        // Platform Line Selector (Player PMC Proprietary vs Reverse-Engineered Factions)
        var _line_str = (builder_chassis_line == 0) ? "[CATALOG: PMC PROPRIETARY FOUNDRY CHASSIS]" : "[CATALOG: REVERSE-ENGINEERED FACTIONS]";
        var _line_col = (builder_chassis_line == 0) ? make_color_rgb(0, 240, 255) : make_color_rgb(255, 180, 50);
        var _line_hov = (_mx >= _eng_x + 18 && _mx <= _eng_x + _eng_w - 18 && _my >= _deck_y && _my <= _deck_y + 26);
        if (_line_hov && _click) {
            builder_chassis_line = (builder_chassis_line == 0) ? 1 : 0;
            builder_chassis_idx = 0;
            var _new_list = get_canonical_chassis_list();
            apply_smart_default_loadout(_new_list[0]);
            scr_audio_play_ui("tab");
        }
        scr_draw_snes_button(_eng_x + 18, _deck_y, _eng_w - 36, 26, _line_str, _line_hov, true, _line_col);

        // Chassis Card
        var _cc_y = _deck_y + 32;'''

assert old_subtab0 in draw_src, "Could not find old_subtab0 in Draw_64.gml"
draw_src = draw_src.replace(old_subtab0, new_subtab0)

# Replace Quick Presets to dynamically adapt to player line vs foreign line
old_presets = '''        // Quick Preset Hot-Select Row
        var _qp_y = _pbtn_y + 65;
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 20, _qp_y, "QUICK DOCTRINAL PRESETS:");

        var _qnames = ["IRONCLAD (TC)", "AETHER (OCL)", "CENTURION (TC)", "KEPLER (OCL)", "HYENA (RS)"];
        var _qindices = [0, 6, 1, 7, 12];
        for (var q = 0; q < min(5, array_length(_qnames)); q++) {
            var _qy_pos = _qp_y + 24 + (q * 44);
            var _qhov = (_mx >= _eng_x + 18 && _mx <= _eng_x + _eng_w - 18 && _my >= _qy_pos && _my <= _qy_pos + 36);
            if (_qhov && _click) {
                builder_chassis_idx = _qindices[q] % array_length(_clist);
                apply_smart_default_loadout(_clist[builder_chassis_idx]);
                scr_audio_play_ui("click");
            }
            scr_draw_snes_button(_eng_x + 18, _qy_pos, _eng_w - 36, 36, "[PRESET: " + _qnames[q] + "]", _qhov, false, make_color_rgb(100, 220, 255));
        }'''

new_presets = '''        // Quick Preset Hot-Select Row
        var _qp_y = _pbtn_y + 65;
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 20, _qp_y, (builder_chassis_line == 0) ? "BESPOKE PMC PLATFORMS:" : "CAPTURED FACTION SCHEMATICS:");

        var _qnames = (builder_chassis_line == 0) ?
            ["PMC-01: VANGUARD (HEAVY BIPED)", "PMC-02: STRATOS (AERO FIGHTER)", "PMC-03: SCRAPPER (TRACKED SIEGE)", "PMC-04: GHOST (HOVER RECON)", "PMC-00: HEPHAESTUS (FLAGSHIP AVATAR)"] :
            ["IRONCLAD (TERRAN GHA-07)", "AETHER (COLONY STRIKER)", "CENTURION (TERRAN TH-C02)", "KEPLER (COLONY SNIPER)", "HYENA (SYNDICATE RAIDER)"];
        var _qindices = (builder_chassis_line == 0) ? [0, 1, 2, 3, 4] : [0, 6, 1, 7, 12];

        for (var q = 0; q < min(5, array_length(_qnames)); q++) {
            var _qy_pos = _qp_y + 24 + (q * 44);
            var _qhov = (_mx >= _eng_x + 18 && _mx <= _eng_x + _eng_w - 18 && _my >= _qy_pos && _my <= _qy_pos + 36);
            if (_qhov && _click) {
                builder_chassis_idx = _qindices[q] % array_length(_clist);
                apply_smart_default_loadout(_clist[builder_chassis_idx]);
                scr_audio_play_ui("click");
            }
            scr_draw_snes_button(_eng_x + 18, _qy_pos, _eng_w - 36, 36, _qnames[q], _qhov, false, (builder_chassis_line == 0) ? make_color_rgb(0, 240, 255) : make_color_rgb(255, 180, 50));
        }'''

assert old_presets in draw_src, "Could not find old_presets in Draw_64.gml"
draw_src = draw_src.replace(old_presets, new_presets)

with open(draw_path, "w") as f:
    f.write(draw_src)
print("Draw_64.gml successfully patched with safe alloy reads, platform line toggle, and bespoke PMC presets.")

