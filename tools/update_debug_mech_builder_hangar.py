#!/usr/bin/env python3
"""
Update obj_DebugManager with:
- Front Mission / Gundam Hangar Deck format (60% left gantry visualizer, 40% right accordion deck)
- 4 Sub-Tabs on Right: [1. CHASSIS], [2. ALLOY], [3. WEAPONS], [4. TELEMETRY]
- Weapons outfitting from Research Tree with smart defaults by role
- Full player freedom to swap to any researched weapon
"""
import os
import re

CREATE_PATH = "objects/obj_DebugManager/Create_0.gml"
STEP_PATH = "objects/obj_DebugManager/Step_0.gml"
DRAW_PATH = "objects/obj_DebugManager/Draw_64.gml"

# 1. Update Create_0.gml
with open(CREATE_PATH) as f:
    create_code = f.read()

# Replace the previous Section 8 in Create_0.gml
sec8_start = create_code.find("// 8. MODULAR MECH BUILDER & FORGE STATE (TAB 1)")
sec9_start = create_code.find("// =========================================================================\n// 9. ASTEROID MINING & PLANETARY RESOURCE EXTRACTION STATE (TAB 2)")

new_sec8 = '''// 8. MODULAR MECH BUILDER & FORGE STATE (TAB 1)
// Front Mission / Gundam Hangar Deck with Weapons from R&D Tech Tree
builder_subtab = 0; // 0=Chassis & Role, 1=Alloy Plating, 2=Researched Weapons, 3=Telemetry & Rollout
builder_chassis_idx = 0;
builder_alloy_idx = 0;
builder_primary_wpn_idx = 0;
builder_secondary_wpn_idx = 0;
builder_melee_wpn_idx = 0;
builder_shield_idx = 0;
builder_custom_name = "HEPHAESTUS-X1";
builder_anim_state = "idle";
builder_subimg = 0.0;
builder_preview_scale = 2.0;

builder_alloys = [
    "alloy_vanguard_comp",
    "alloy_hyperion_matrix",
    "alloy_aerosteel_flux",
    "alloy_adamantine_carbide",
    "alloy_chobham_reactive",
    "alloy_tachyon_superalloy"
];
builder_alloy_names = [
    "Vanguard Composite (Standard Kinetic Armor)",
    "Hyperion Matrix (+25% Energy Gen, +20% Beam Res)",
    "Aerosteel Flux (+35% Boost Speed, -20% Mass)",
    "Adamantine Heavy (+40% Armor HP, Sintered Carbide)",
    "Chobham-X Reactive (+50% Explosive/Missile Res)",
    "Tachyon Superalloy (Singularity Spec, +25% All Stats)"
];
builder_alloy_deltas = [
    { armor_mult: 1.0, mass_mult: 1.0, speed_bonus: 0, desc: "Standard military baseline plating." },
    { armor_mult: 0.9, mass_mult: 0.85, speed_bonus: 15, desc: "Plasma-stabilized superconducting matrix." },
    { armor_mult: 0.8, mass_mult: 0.75, speed_bonus: 30, desc: "Ultralight vacuum-sintered vernier alloy." },
    { armor_mult: 1.45, mass_mult: 1.35, speed_bonus: -15, desc: "Super-dense impact-resistant adamantine slab." },
    { armor_mult: 1.2, mass_mult: 1.1, speed_bonus: -5, desc: "Composite tiles defeating kinetic shaped-charges." },
    { armor_mult: 1.35, mass_mult: 0.85, speed_bonus: 25, desc: "Self-healing pre-war molecular 3D lattice." }
];

// Master Weapons & Equipment R&D Tech Tree Catalog
builder_weapons_db = {
    primary: [
        { id: "wp_autocannon_105", name: "Type-77 105mm Heavy Autocannon", tech_id: "tech_wpn_heavy_autocannon", damage: 180, class: "BALLISTIC", sprite: spr_ms_ironclad_fire_rifle, power_draw: 2, mass: 8, lore: "Gas-operated cyclic cannon firing AP sabots." },
        { id: "wp_smoothbore_120", name: "120mm Smoothbore Heavy Rifle", tech_id: "tech_wpn_hyper_velocity_rifle", damage: 230, class: "BALLISTIC", sprite: spr_ms_ironclad_fire_rifle, power_draw: 4, mass: 12, lore: "High-pressure smoothbore firing depleted uranium darts." },
        { id: "wp_spartan_chaingun", name: "GAU-88 35mm Spartan Rotary Vulcan", tech_id: "tech_wpn_heavy_autocannon", damage: 215, class: "ROTARY_VULCAN", sprite: spr_ms_centurion_fire_chaingun, power_draw: 4, mass: 10, lore: "Rotating multi-barrel vulcan with cooling dissipation." },
        { id: "wp_beam_rifle_type6a", name: "Type-6A High-Output Beam Rifle", tech_id: "tech_wpn_beam_carbine", damage: 260, class: "BEAM_PULSE", sprite: spr_ms_aether_fire_beam, power_draw: 8, mass: 8, lore: "Coherent Cherenkov cyan beam lance accelerator." },
        { id: "wp_railgun_90", name: "Hyper-Velocity 90mm Railgun", tech_id: "tech_wpn_electromagnetic_railgun", damage: 340, class: "BALLISTIC", sprite: spr_ms_ironclad_fire_rifle, power_draw: 12, mass: 16, lore: "Electromagnetic mass driver accelerating tungsten to Mach 8." },
        { id: "wp_tachyon_lance", name: "Coherent Tachyon Beam Lance", tech_id: "tech_wpn_tachyon_lance", damage: 390, class: "BEAM_PULSE", sprite: spr_ms_aether_fire_beam, power_draw: 14, mass: 10, lore: "Mega-particle thermal beam slicing through capital warship hulls." }
    ],
    secondary: [
        { id: "wp_hydra_rockets", name: "Unguided 70mm Hydra Rocket Pod", tech_id: "tech_wpn_hydra_rockets", damage: 140, class: "MICRO_MISSILE", sprite: spr_ms_ironclad_fire_missiles, power_draw: 2, mass: 6, lore: "Ripple-fire rocket canisters for carpet bombardment." },
        { id: "wp_micro_missile_swarm", name: "16-Cell Micro-Missile Swarm Pod", tech_id: "tech_wpn_guided_swarm_missiles", damage: 220, class: "MICRO_MISSILE", sprite: spr_ms_ironclad_fire_missiles, power_draw: 4, mass: 10, lore: "Lidar-guided swirling micro-munitions." },
        { id: "wp_antiship_torpedo", name: "Heavy Anti-Ship Torpedo Battery", tech_id: "tech_wpn_anti_ship_torpedo", damage: 380, class: "MICRO_MISSILE", sprite: spr_ms_ironclad_fire_missiles, power_draw: 6, mass: 18, lore: "Thermonuclear torpedo cracking warship keels." },
        { id: "wp_chaff_flare", name: "Thermal Chaff & ECM Flare Dispenser", tech_id: "tech_wpn_hydra_rockets", damage: 0, class: "COUNTERMEASURE", sprite: -1, power_draw: 1, mass: 3, lore: "Radar-scattering chaff providing +20% Evasion." }
    ],
    melee: [
        { id: "wp_vibro_blade", name: "Titanium Vibro-Blade", tech_id: "tech_wpn_vibro_blade", damage: 160, class: "MELEE", sprite: spr_ms_aether_attack_saber, power_draw: 1, mass: 3, lore: "Solid titanium blade with ultrasonic oscillation." },
        { id: "wp_heat_hawk", name: "High-Frequency Thermal Heat Hawk / Mace", tech_id: "tech_wpn_plasma_heat_blade", damage: 235, class: "MELEE", sprite: spr_ms_ironclad_attack_melee, power_draw: 3, mass: 8, lore: "Superheated 3000°C thermal edge melting armor plate." },
        { id: "wp_thermal_gladius", name: "Spartan High-Frequency Gladius", tech_id: "tech_wpn_vibro_blade", damage: 250, class: "MELEE", sprite: spr_ms_centurion_attack_melee, power_draw: 4, mass: 6, lore: "Bespoke shock assault thermal blade." },
        { id: "wp_beam_saber_cherenkov", name: "High-Energy Thermal Plasma Saber", tech_id: "tech_wpn_beam_saber", damage: 285, class: "MELEE", sprite: spr_ms_aether_attack_saber, power_draw: 6, mass: 4, lore: "Cherenkov cyan plasma blade with pure white core." }
    ],
    shield: [
        { id: "sld_ballistic_buckler", name: "Ballistic Titanium Buckler", tech_id: "tech_sld_ballistic_buckler", armor_hp: 90, mass: 4, power_draw: 0, lore: "Lightweight deflector plate." },
        { id: "sld_composite_tower", name: "Aegis Composite Tower Scutum", tech_id: "tech_sld_ballistic_buckler", armor_hp: 210, mass: 9, power_draw: 0, lore: "Heavy frontline blast barrier." },
        { id: "sld_em_deflector", name: "Aerosteel Deflector Shield", tech_id: "tech_sld_ballistic_buckler", armor_hp: 150, mass: 5, power_draw: 3, lore: "Angled aerosteel with electromagnetic dispersion." },
        { id: "sld_fortress_barrier", name: "Fortress Reactive Energy Barrier", tech_id: "tech_sld_ballistic_buckler", armor_hp: 300, mass: 14, power_draw: 6, lore: "Superheavy fortress barrier absorbing kinetic/beam salvos." }
    ]
};

// Retrieve Canonical Chassis Catalog
get_canonical_chassis_list = function() {
    var _list = [];
    for (var i = 0; i < array_length(master_roster); i++) {
        var _u = master_roster[i];
        if (_u.category == "MOBILE_SUIT") array_push(_list, _u);
    }
    if (array_length(_list) == 0 && array_length(master_roster) > 0) array_push(_list, master_roster[0]);
    return _list;
};

// Check if a technology is researched in R&D Tech Tree
is_tech_researched = function(_tech_id) {
    if (!instance_exists(obj_GameManager)) return true; // Debug mode fallback
    var _sys = obj_GameManager.research_system;
    if (is_undefined(_sys) || !variable_struct_exists(_sys, "unlocked_techs")) return true;
    return variable_struct_exists(_sys.unlocked_techs, _tech_id) && _sys.unlocked_techs[$ _tech_id] == true;
};

// Smart Default Loadout: Auto-equips latest researched equipment matching mobile suit role
apply_smart_default_loadout = function(_chassis) {
    var _doc = string_lower(variable_struct_exists(_chassis, "doctrine") ? _chassis.doctrine : "");
    var _w_class = variable_struct_exists(_chassis, "weapon_class") ? _chassis.weapon_class : "BALLISTIC";
    var _c_name = string_lower(_chassis.name);

    // 1. Primary Ranged
    if (string_pos("beam", _doc) > 0 || _w_class == "BEAM_PULSE" || string_pos("aether", _c_name) > 0) {
        builder_primary_wpn_idx = is_tech_researched("tech_wpn_tachyon_lance") ? 5 : (is_tech_researched("tech_wpn_beam_carbine") ? 3 : 0);
    } else if (string_pos("centurion", _c_name) > 0 || _w_class == "ROTARY_VULCAN") {
        builder_primary_wpn_idx = 2; // Spartan Chaingun
    } else if (string_pos("sniper", _doc) > 0 || string_pos("railgun", _doc) > 0) {
        builder_primary_wpn_idx = is_tech_researched("tech_wpn_electromagnetic_railgun") ? 4 : 1;
    } else {
        builder_primary_wpn_idx = is_tech_researched("tech_wpn_hyper_velocity_rifle") ? 1 : 0;
    }

    // 2. Secondary
    if (string_pos("missile", _doc) > 0 || string_pos("siege", _doc) > 0) {
        builder_secondary_wpn_idx = is_tech_researched("tech_wpn_anti_ship_torpedo") ? 2 : 1;
    } else if (string_pos("aero", _doc) > 0 || string_pos("vernier", _doc) > 0) {
        builder_secondary_wpn_idx = 3; // Chaff / ECM
    } else {
        builder_secondary_wpn_idx = is_tech_researched("tech_wpn_guided_swarm_missiles") ? 1 : 0;
    }

    // 3. Melee
    if (string_pos("beam", _doc) > 0 || string_pos("plasma", _doc) > 0 || string_pos("aether", _c_name) > 0) {
        builder_melee_wpn_idx = is_tech_researched("tech_wpn_beam_saber") ? 3 : 0;
    } else if (string_pos("centurion", _c_name) > 0) {
        builder_melee_wpn_idx = 2; // Spartan Gladius
    } else {
        builder_melee_wpn_idx = is_tech_researched("tech_wpn_plasma_heat_blade") ? 1 : 0;
    }

    // 4. Shield
    if (string_pos("heavy", _doc) > 0 || string_pos("trench", _doc) > 0 || string_pos("ironclad", _c_name) > 0) {
        builder_shield_idx = 1; // Tower Scutum
    } else if (string_pos("aether", _c_name) > 0 || string_pos("colony", _doc) > 0) {
        builder_shield_idx = 2; // Aerosteel Deflector
    } else {
        builder_shield_idx = 0; // Buckler
    }

    builder_custom_name = _chassis.name + " [PMC SPEC]";
};

// Calculate Full Telemetry based on Chassis + Sintered Alloy + Researched Loadout
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
};

deploy_builder_mech_to_combat = function() {
    var _t = calculate_builder_telemetry();
    if (_t.reactor_overloaded) {
        show_toast("DEPLOYMENT REJECTED: Net Power is Negative (Reactor Overload)!", c_red);
        scr_audio_play_ui("cancel");
        return;
    }

    var _custom_u = {
        id: "custom_test_" + string(irandom(9999)),
        name: builder_custom_name,
        faction_id: "pmc_player",
        category: "CUSTOM_MECH",
        move_type: variable_struct_exists(_t.chassis, "move_type") ? _t.chassis.move_type : "biped",
        alloy_id: builder_alloys[builder_alloy_idx],
        sprite_asset: _t.chassis.sprite_asset,
        sprite_back_asset: _t.chassis.sprite_back_asset,
        weapon_name: _t.primary_wpn.name,
        weapon_class: _t.primary_wpn.class,
        hp: _t.total_armor,
        armor: floor(_t.total_armor / 12),
        speed: _t.boost_speed,
        accuracy: 88,
        evasion: 25,
        attack_range: 2,
        role: _t.weight_class,
        doctrine: "PMC Hephaestus Custom Masterwork",
        aux_system: _t.secondary_wpn.name + " // " + _t.melee_wpn.name + " // " + _t.shield.name,
        sprites: {
            idle: _t.chassis.sprite_asset,
            walk: (variable_struct_exists(_t.sprites, "boost") && _t.sprites.boost != -1) ? _t.sprites.boost : _t.chassis.sprite_asset,
            fire: _t.primary_wpn.sprite,
            melee: _t.melee_wpn.sprite,
            boost: (variable_struct_exists(_t.sprites, "boost") && _t.sprites.boost != -1) ? _t.sprites.boost : _t.chassis.sprite_asset,
            damaged: (variable_struct_exists(_t.sprites, "damaged") && _t.sprites.damaged != -1) ? _t.sprites.damaged : _t.chassis.sprite_asset,
            destroyed: (variable_struct_exists(_t.sprites, "destroyed") && _t.sprites.destroyed != -1) ? _t.sprites.destroyed : _t.chassis.sprite_asset
        }
    };

    array_insert(master_roster, 0, _custom_u);
    atk_faction_idx = 0;
    atk_cat_idx = 0;
    atk_filtered_idx = 0;
    active_debug_tab = 0;

    scr_audio_play_ui("boot");
    show_toast("DEPLOYED TO COMBAT LAB: " + builder_custom_name + " ready for live action testing!", c_lime);
};

commission_builder_mech_to_hangar = function() {
    var _t = calculate_builder_telemetry();
    if (_t.reactor_overloaded) {
        show_toast("COMMISSION REJECTED: Net Power is Negative!", c_red);
        scr_audio_play_ui("cancel");
        return;
    }
    if (instance_exists(obj_GameManager)) {
        var _gm = obj_GameManager;
        var _new_mech = {
            id: "custom_mech_" + string(_gm.current_turn) + "_" + string(irandom(9999)),
            blueprint_id: _t.chassis.id,
            callsign: builder_custom_name,
            name: builder_custom_name,
            class: _t.weight_class,
            assigned_pilot: "Unassigned",
            status: "READY",
            current_condition_pct: 1.0,
            armor_rating: _t.total_armor,
            power_output: _t.net_power,
            speed: _t.boost_speed,
            weight_tonnes: _t.total_mass,
            combat_rating: _t.combat_rating,
            components_summary: _t.chassis.name + " // " + _t.primary_wpn.name + " // " + _t.secondary_wpn.name + " // " + _t.melee_wpn.name + " // " + _t.shield.name,
            part_composition: { chassis: _t.chassis, primary: _t.primary_wpn, secondary: _t.secondary_wpn, melee: _t.melee_wpn, shield: _t.shield },
            spec_type: "COMMANDER_CUSTOM",
            combat_pedigree: { sorties_deployed: 0, sorties_survived: 0, confirmed_kills: 0, ace_kills: 0, damage_mitigated: 0, pedigree_rating: "FACTORY_FRESH", telemetry_bonus: 0.0 }
        };
        array_push(_gm.inventory.deployable_mechs, _new_mech);
        show_toast("COMMISSIONED TO FLEET HANGAR: " + builder_custom_name + " added to Hangar!", c_lime);
        scr_audio_play_ui("boot");
    }
};

unlock_all_research_cheats = function() {
    if (instance_exists(obj_GameManager) && !is_undefined(obj_GameManager.research_system)) {
        var _sys = obj_GameManager.research_system;
        var _db = scr_research_get_tech_db();
        var _keys = variable_struct_get_names(_db);
        for (var k = 0; k < array_length(_keys); k++) {
            _sys.unlocked_techs[$ _keys[k]] = true;
        }
        show_toast("ALL WEAPONS & TECH RESEARCHED! Entire R&D Arsenal Available!", c_yellow);
        scr_audio_play_ui("boot");
    }
};
'''

assert sec8_start != -1 and sec9_start != -1, "Could not find Section 8 boundaries in Create_0.gml"
create_code = create_code[:sec8_start] + new_sec8 + "\n" + create_code[sec9_start:]
with open(CREATE_PATH, "w") as f:
    f.write(create_code)
print("Create_0.gml updated successfully!")

