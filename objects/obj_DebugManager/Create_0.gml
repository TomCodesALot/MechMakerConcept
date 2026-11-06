/// @description obj_DebugManager Create Event
// Universal PMC Debug Console & Battle Animation Proving Ground

if (instance_number(obj_DebugManager) > 1) {
    show_debug_message("[obj_DebugManager] Duplicate singleton detected. Destroying instance: " + string(id));
    instance_destroy();
    exit;
}

persistent = true;
depth = -9999;
show_debug_message("[obj_DebugManager] Initializing Universal Debug & Battle Demonstration Engine...");

// 1. Activation State
is_open = true;
active_debug_tab = 0; // 0 = Battle & Animation Lab, 1 = PMC Campaign Cheats
debug_toast = "";
debug_toast_timer = 0;
debug_toast_color = c_lime;

show_toast = function(_msg, _col = c_lime) {
    debug_toast = _msg;
    debug_toast_timer = 150;
    debug_toast_color = _col;
};

// 2. Factions & Category Definitions
factions = ["ALL", "faction_a", "faction_b", "faction_c", "faction_d", "pmc_player", "faction_e", "faction_f"];
faction_names = ["ALL FACTIONS", "Terran Coalition", "Outer Colonies", "Rust Syndicate", "Apex Zaibatsu", "PMC Vanguard", "Sovereign League", "Tharsis Consensus"];

categories = ["ALL", "MOBILE_SUIT", "CUSTOM_MECH", "VEHICLE", "INFANTRY"];
category_names = ["ALL CATEGORIES", "Mobile Suits", "Custom Sockets", "Vehicles", "Infantry Squads"];

// 3. Populate Comprehensive Unit Catalog Roster from Authoritative Central Database
master_roster = scr_ms_db_get_roster();
show_debug_message("[obj_DebugManager] Master unit catalog indexed from Central Database: " + string(array_length(master_roster)) + " total units.");

// 4. Filtering & Selection Logic
atk_faction_idx = 0;
atk_cat_idx = 0;
atk_filtered_idx = 0;

def_faction_idx = 0;
def_cat_idx = 0;
def_filtered_idx = min(1, array_length(master_roster) - 1);

get_filtered_units = function(_fac_idx, _c_idx) {
    var _fac_id = factions[_fac_idx];
    var _cat_id = categories[_c_idx];
    var _res = [];
    for (var i = 0; i < array_length(master_roster); i++) {
        var _u = master_roster[i];
        if (_fac_id != "ALL" && _u.faction_id != _fac_id) continue;
        if (_cat_id != "ALL" && _u.category != _cat_id) continue;
        array_push(_res, _u);
    }
    if (array_length(_res) == 0 && array_length(master_roster) > 0) {
        array_push(_res, master_roster[0]);
    }
    return _res;
};

// 5. Interactive Animation Stage State
anim_states = ["idle", "fire_rifle", "fire_chaingun", "fire_beam", "fire_missiles", "melee", "boost", "damaged", "destroyed"];
anim_state_idx = 0;

anim_speeds = [0.25, 0.5, 1.0, 2.0];
anim_speed_names = ["0.25x", "0.5x", "1.0x", "2.0x"];
anim_speed_idx = 2; // 1.0x normal

anim_perspective = "front"; // "front" or "back"
is_paused = false;
step_frame_req = false;
subimg_atk = 0.0;
subimg_def = 0.0;

theaters = ["EARTH", "SPACE", "WATER", "SLAG"];
theater_names = ["Terran Badlands", "Orbital Space Void", "Harbor Water Canal", "Slag Foundry Caldera"];
theater_idx = 0;

weapon_classes = ["BALLISTIC", "ROTARY_VULCAN", "BEAM_PULSE", "MICRO_MISSILE", "MELEE", "BEAM_LANCE"];
weapon_names = ["Type-77 120mm Solid Cannon", "GAU-88 Rotary Heavy Vulcan", "Coherent Beam Pulse Rifle", "Ares Swarm-16 Micro-Missiles", "Hydraulic Gun-Club Strike", "Twin Forearm Plasma Lances"];
weapon_idx = 0;
atk_prev_unit_id = "";

live_stage_particles = [];
live_stage_casings = [];

// 6. Full Cinematic Clash Duel Runner Struct
clash_cinematic = {
    active: false,
    phase: 0,
    timer: 0,
    shutter_y: 0,
    screen_shake: 0.0,
    theater: "EARTH",
    attacker: undefined,
    defender: undefined,
    weapon_class: "BALLISTIC",
    weapon_name: "Type-77 120mm Solid Cannon",
    raw_damage: 165,
    mitigated_dmg: 135,
    hit_part: "torso",
    is_hit: true,
    has_counter: true,
    counter_damage: 85,
    counter_part: "arm_left",
    atk_anim_state: "idle",
    def_anim_state: "idle",
    atk_subimg: -1,
    def_subimg: -1,
    atk_dash_x: 0,
    atk_recoil_x: 0,
    atk_recoil_y: 0,
    def_recoil_x: 0,
    def_recoil_y: 0,
    atk_hp: 680,
    atk_max_hp: 680,
    def_hp: 650,
    def_max_hp: 650,
    projectiles: [],
    casings: [],
    particles: [],
    popups: []
};

// 7. Launch Full Cinematic Clash
launch_full_cinematic_clash = function() {
    var _atk_list = get_filtered_units(atk_faction_idx, atk_cat_idx);
    var _def_list = get_filtered_units(def_faction_idx, def_cat_idx);
    var _atk_u = _atk_list[clamp(atk_filtered_idx, 0, array_length(_atk_list) - 1)];
    var _def_u = _def_list[clamp(def_filtered_idx, 0, array_length(_def_list) - 1)];

    var _w_class = weapon_classes[weapon_idx];
    var _w_name = weapon_names[weapon_idx];
    if (_atk_u.category != "CUSTOM_MECH") {
        if (_w_class == _atk_u.weapon_class) {
            _w_name = _atk_u.weapon_name;
        } else if (_w_class == "MELEE") {
            _w_name = (variable_struct_exists(_atk_u, "weapon_overlay_secondary") && _atk_u.weapon_overlay_secondary != "") ? _atk_u.weapon_overlay_secondary : "Hydraulic Shoulder Tackle & Strike";
        }
    }

    clash_cinematic.active = true;
    clash_cinematic.phase = 0;
    clash_cinematic.timer = 0;
    clash_cinematic.shutter_y = 0;
    clash_cinematic.screen_shake = 0;
    clash_cinematic.theater = theaters[theater_idx];
    clash_cinematic.attacker = _atk_u;
    clash_cinematic.defender = _def_u;
    clash_cinematic.weapon_class = _w_class;
    clash_cinematic.weapon_name = _w_name;
    clash_cinematic.raw_damage = irandom_range(150, 210);
    clash_cinematic.mitigated_dmg = max(35, clash_cinematic.raw_damage - _def_u.armor);
    clash_cinematic.is_hit = true;
    clash_cinematic.has_counter = true;
    clash_cinematic.counter_damage = irandom_range(60, 110);
    clash_cinematic.atk_anim_state = "idle";
    clash_cinematic.def_anim_state = "idle";
    clash_cinematic.atk_subimg = -1;
    clash_cinematic.def_subimg = -1;
    clash_cinematic.atk_dash_x = 0;
    clash_cinematic.atk_recoil_x = 0;
    clash_cinematic.atk_recoil_y = 0;
    clash_cinematic.def_recoil_x = 0;
    clash_cinematic.def_recoil_y = 0;
    clash_cinematic.atk_hp = _atk_u.hp;
    clash_cinematic.atk_max_hp = _atk_u.hp;
    clash_cinematic.def_hp = _def_u.hp;
    clash_cinematic.def_max_hp = _def_u.hp;
    clash_cinematic.projectiles = [];
    clash_cinematic.casings = [];
    clash_cinematic.particles = [];
    clash_cinematic.popups = [];

    scr_audio_play_ui("tab");
    show_toast("[SIMULATION LAUNCHED] Full 2-Tier Cinematic Clash Duel Active!", c_aqua);
};

// =========================================================================
// 8. MODULAR MECH BUILDER & FORGE STATE (TAB 1)
// =========================================================================
builder_selected_slot = 0; // 0=Head, 1=Torso, 2=Arms, 3=Legs, 4=Backpack, 5=Weapon, 6=Alloy
builder_head_idx = 0;
builder_torso_idx = 0;
builder_arms_idx = 0;
builder_legs_idx = 0;
builder_bp_idx = 0;
builder_wp_idx = 0;
builder_alloy_idx = 0;
builder_custom_name = "HEPHAESTUS-X1";
builder_anim_state = "idle";
builder_subimg = 0.0;
builder_preview_scale = 1.6;

builder_alloys = [
    "alloy_vanguard_comp",
    "alloy_hyperion_matrix",
    "alloy_aerosteel_flux",
    "alloy_adamantine_carbide",
    "alloy_chobham_reactive",
    "alloy_tachyon_superalloy"
];
builder_alloy_names = [
    "Vanguard Composite (+15% Kinetic Res)",
    "Hyperion Matrix (+20% Energy Gen)",
    "Aerosteel Flux (+25% Boost Speed)",
    "Adamantine Heavy (+30% Armor HP)",
    "Chobham-X Reactive (+25% Explosive Res)",
    "Tachyon Superalloy (Singularity Spec)"
];

// Rich Modular Parts Catalog for Kitbashing & Testing
builder_parts_catalog = {
    heads: [
        { id: "hd_vanguard_01", name: "HD-01 Vanguard Target-Lock", slot: "heads", armor: 140, mass: 4, power_draw: 2, bonus: "+15% Accuracy", alloy: "alloy_vanguard_comp" },
        { id: "hd_aether_02", name: "HD-02 Aether EW-Dome", slot: "heads", armor: 100, mass: 2, power_draw: 3, bonus: "+18% Evasion", alloy: "alloy_aerosteel_flux" },
        { id: "hd_titan_04", name: "HD-04 Titan Heavy Sensor Brow", slot: "heads", armor: 220, mass: 7, power_draw: 5, bonus: "+30% Armor", alloy: "alloy_adamantine_carbide" },
        { id: "hd_hyena_03", name: "HD-03 Hyena Monocular Scavenger", slot: "heads", armor: 120, mass: 3, power_draw: 2, bonus: "+20% Crit Find", alloy: "alloy_vanguard_comp" },
        { id: "hd_muramasa_01", name: "HD-01 Muramasa Cyber-Optic", slot: "heads", armor: 150, mass: 4, power_draw: 4, bonus: "+25% Tracking", alloy: "alloy_tachyon_superalloy" },
        { id: "hd_genesis_00", name: "HD-00 Genesis Archeo-Crown", slot: "heads", armor: 280, mass: 3, power_draw: 1, bonus: "+35% Singularity", alloy: "alloy_tachyon_superalloy" }
    ],
    torsos: [
        { id: "tr_colossus_01", name: "TR-01 Colossus Heavy Torso", slot: "torsos", armor: 520, mass: 26, power_output: 32, bonus: "Heavy Reactor Core", alloy: "alloy_vanguard_comp" },
        { id: "tr_hyperion_02", name: "TR-02 Hyperion Tokamak Torso", slot: "torsos", armor: 400, mass: 18, power_output: 45, bonus: "High-Spec Fusion Core", alloy: "alloy_hyperion_matrix" },
        { id: "tr_adamantine_03", name: "TR-03 Adamantine Dreadnought Core", slot: "torsos", armor: 680, mass: 36, power_output: 38, bonus: "Fortress Reactor", alloy: "alloy_adamantine_carbide" },
        { id: "tr_syndicate_04", name: "TR-04 Syndicate Overclocked Fission", slot: "torsos", armor: 420, mass: 22, power_output: 36, bonus: "Volatile Turbine", alloy: "alloy_vanguard_comp" },
        { id: "tr_aether_flux_05", name: "TR-05 Aether Vector Flux Torso", slot: "torsos", armor: 380, mass: 16, power_output: 48, bonus: "Ultra-Light Tokamak", alloy: "alloy_aerosteel_flux" },
        { id: "tr_hephaestus_00", name: "TR-00 Hephaestus Singularity Core", slot: "torsos", armor: 600, mass: 15, power_output: 70, bonus: "Archeo-Crucible Dynamo", alloy: "alloy_tachyon_superalloy" }
    ],
    arms: [
        { id: "am_colossus_01", name: "AM-01 Colossus Dual Arms", slot: "arms", armor: 280, mass: 16, power_draw: 4, bonus: "+25% Recoil Control", alloy: "alloy_vanguard_comp" },
        { id: "am_vernier_02", name: "AM-02 Vernier Fast-Actuators", slot: "arms", armor: 200, mass: 9, power_draw: 4, bonus: "+20% Handling", alloy: "alloy_aerosteel_flux" },
        { id: "am_hydraulic_03", name: "AM-03 Hydraulic Crusher Pincers", slot: "arms", armor: 360, mass: 22, power_draw: 5, bonus: "+40% Melee Impact", alloy: "alloy_adamantine_carbide" },
        { id: "am_sniper_04", name: "AM-04 Gyro-Stabilized Sniper Arms", slot: "arms", armor: 180, mass: 11, power_draw: 4, bonus: "+30% Precision", alloy: "alloy_hyperion_matrix" },
        { id: "am_monomolecular_05", name: "AM-05 Monomolecular Gauntlets", slot: "arms", armor: 220, mass: 8, power_draw: 4, bonus: "+35% Speed", alloy: "alloy_tachyon_superalloy" },
        { id: "am_archeo_00", name: "AM-00 Archeotech Lattice Manipulators", slot: "arms", armor: 310, mass: 7, power_draw: 2, bonus: "Zero-Latency Link", alloy: "alloy_tachyon_superalloy" }
    ],
    legs: [
        { id: "lg_vanguard_01", name: "LG-01 Vanguard Heavy Walkers", slot: "legs", armor: 360, mass: 24, power_draw: 5, base_speed: 46, move_type: "biped", bonus: "+30% Stability", alloy: "alloy_vanguard_comp" },
        { id: "lg_stratos_02", name: "LG-02 Stratos Vernier Skaters", slot: "legs", armor: 230, mass: 14, power_draw: 6, base_speed: 88, move_type: "hover", bonus: "+25% Agility", alloy: "alloy_aerosteel_flux" },
        { id: "lg_siege_treads_03", name: "LG-03 Bulldozer Siege Treads", slot: "legs", armor: 520, mass: 35, power_draw: 6, base_speed: 34, move_type: "tread", bonus: "Heavy Recoil Anchor", alloy: "alloy_adamantine_carbide" },
        { id: "lg_aether_aero_04", name: "LG-04 Aether Aero-Struts", slot: "legs", armor: 220, mass: 11, power_draw: 7, base_speed: 98, move_type: "aero", bonus: "High-G Evasion", alloy: "alloy_aerosteel_flux" },
        { id: "lg_centurion_05", name: "LG-05 Centurion Spartan Greaves", slot: "legs", armor: 400, mass: 20, power_draw: 5, base_speed: 54, move_type: "biped", bonus: "Breaching Thrust", alloy: "alloy_vanguard_comp" },
        { id: "lg_grav_repulsor_00", name: "LG-00 Grav-Repulsor Matrix", slot: "legs", armor: 320, mass: 9, power_draw: 3, base_speed: 115, move_type: "aero", bonus: "Inertia Dampening", alloy: "alloy_tachyon_superalloy" }
    ],
    backpacks: [
        { id: "bp_heavy_01", name: "BP-01 Heavy Booster Pack", slot: "backpacks", armor: 150, mass: 12, power_draw: 3, boost_bonus: 35, bonus: "High Thrust", alloy: "alloy_vanguard_comp" },
        { id: "bp_vernier_02", name: "BP-02 Dual-Vector Vernier Rig", slot: "backpacks", armor: 110, mass: 7, power_draw: 5, boost_bonus: 68, bonus: "+15% Evade", alloy: "alloy_aerosteel_flux" },
        { id: "bp_fortress_03", name: "BP-03 Fortress Energy Barrier", slot: "backpacks", armor: 240, mass: 16, power_draw: 8, boost_bonus: 25, bonus: "Kinetic Shield", alloy: "alloy_adamantine_carbide" },
        { id: "bp_afterburner_04", name: "BP-04 High-G Overdrive Thrusters", slot: "backpacks", armor: 95, mass: 8, power_draw: 6, boost_bonus: 82, bonus: "Sprint Burst", alloy: "alloy_aerosteel_flux" },
        { id: "bp_ecm_jammer_05", name: "BP-05 Tactical ECM Jammer Mast", slot: "backpacks", armor: 120, mass: 6, power_draw: 5, boost_bonus: 48, bonus: "Radar Stealth", alloy: "alloy_tachyon_superalloy" },
        { id: "bp_sol_singularity_00", name: "BP-00 Sol-Drive Singularity Booster", slot: "backpacks", armor: 190, mass: 5, power_draw: 2, boost_bonus: 105, bonus: "Quantum Hop", alloy: "alloy_tachyon_superalloy" }
    ],
    weapons: [
        { id: "wp_vulcan_01", name: "WP-01 Rotary Vulcan (120mm)", slot: "weapons", armor: 110, mass: 12, power_draw: 3, damage: 185, weapon_class: "ROTARY_VULCAN", sprite: spr_ms_ironclad_fire_rifle, bonus: "Sustained Flak", alloy: "alloy_vanguard_comp" },
        { id: "wp_beam_02", name: "WP-02 Type-6A Thermal Beam Rifle", slot: "weapons", armor: 85, mass: 8, power_draw: 9, damage: 255, weapon_class: "BEAM_PULSE", sprite: spr_ms_aether_fire_beam, bonus: "Armor Piercing", alloy: "alloy_aerosteel_flux" },
        { id: "wp_chaingun_03", name: "WP-03 35mm Spartan Chain Gun", slot: "weapons", armor: 100, mass: 10, power_draw: 4, damage: 215, weapon_class: "ROTARY_VULCAN", sprite: spr_ms_centurion_fire_chaingun, bonus: "Rotary Barrage", alloy: "alloy_vanguard_comp" },
        { id: "wp_plasma_saber_04", name: "WP-04 High-Energy Thermal Saber", slot: "weapons", armor: 75, mass: 4, power_draw: 5, damage: 270, weapon_class: "MELEE", sprite: spr_ms_aether_attack_saber, bonus: "Plasma Cleave", alloy: "alloy_aerosteel_flux" },
        { id: "wp_missiles_05", name: "WP-05 16-Cell Micro-Missile Pod", slot: "weapons", armor: 95, mass: 13, power_draw: 5, damage: 230, weapon_class: "MICRO_MISSILE", sprite: spr_ms_ironclad_fire_missiles, bonus: "Swarm Tracking", alloy: "alloy_vanguard_comp" },
        { id: "wp_tachyon_00", name: "WP-00 Archeotech Tachyon Lance", slot: "weapons", armor: 130, mass: 9, power_draw: 11, damage: 380, weapon_class: "BEAM_PULSE", sprite: spr_ms_aether_fire_beam, bonus: "Disintegration", alloy: "alloy_tachyon_superalloy" }
    ]
};

// Sync with GameManager Inventory
sync_builder_parts_to_game = function() {
    if (instance_exists(obj_GameManager)) {
        var _pts = obj_GameManager.inventory.parts;
        var _slots = ["heads", "torsos", "arms", "legs", "backpacks", "weapons"];
        for (var s = 0; s < array_length(_slots); s++) {
            var _sk = _slots[s];
            if (!variable_struct_exists(_pts, _sk) || array_length(variable_struct_get(_pts, _sk)) < 6) {
                variable_struct_set(_pts, _sk, variable_struct_get(builder_parts_catalog, _sk));
            }
        }
    }
};
sync_builder_parts_to_game();

// Calculate Real-Time Builder Telemetry
calculate_builder_telemetry = function() {
    var _hd = builder_parts_catalog.heads[clamp(builder_head_idx, 0, array_length(builder_parts_catalog.heads) - 1)];
    var _tr = builder_parts_catalog.torsos[clamp(builder_torso_idx, 0, array_length(builder_parts_catalog.torsos) - 1)];
    var _am = builder_parts_catalog.arms[clamp(builder_arms_idx, 0, array_length(builder_parts_catalog.arms) - 1)];
    var _lg = builder_parts_catalog.legs[clamp(builder_legs_idx, 0, array_length(builder_parts_catalog.legs) - 1)];
    var _bp = builder_parts_catalog.backpacks[clamp(builder_bp_idx, 0, array_length(builder_parts_catalog.backpacks) - 1)];
    var _wp = builder_parts_catalog.weapons[clamp(builder_wp_idx, 0, array_length(builder_parts_catalog.weapons) - 1)];

    var _tot_armor = _hd.armor + _tr.armor + _am.armor + _lg.armor + _bp.armor + _wp.armor;
    var _tot_mass = _hd.mass + _tr.mass + _am.mass + _lg.mass + _bp.mass + _wp.mass;
    var _max_capacity = _lg.mass * 4.5;
    var _mass_overloaded = (_tot_mass > _max_capacity);

    var _tot_draw = _hd.power_draw + _am.power_draw + _lg.power_draw + _bp.power_draw + _wp.power_draw;
    var _net_power = _tr.power_output - _tot_draw;
    var _reactor_overloaded = (_net_power < 0);

    var _walk_spd = max(18, floor(_lg.base_speed * (1.0 - (_tot_mass / 220.0))));
    var _boost_spd = _walk_spd + _bp.boost_bonus;
    var _oss = floor((_tot_armor / 5) + _wp.damage + (_boost_spd / 2) + max(0, _net_power * 3));

    var _w_class = "MEDIUM MAINSTAY";
    if (_tot_mass < 55) _w_class = "LIGHT SKIRMISHER";
    else if (_tot_mass >= 55 && _tot_mass < 82) _w_class = "MEDIUM MAINSTAY";
    else if (_tot_mass >= 82 && _tot_mass < 110) _w_class = "HEAVY ASSAULT";
    else _w_class = "SUPERHEAVY SIEGEBREAKER";

    // Resolve Representative Visual Sprite
    var _prev_spr = spr_ms_aether_idle;
    var _move_type = _lg.move_type;
    if (_move_type == "aero") _prev_spr = spr_ms_aether_idle;
    else if (_move_type == "tread" || _tot_mass > 90) _prev_spr = spr_ms_ironclad_idle;
    else if (_move_type == "hover") _prev_spr = spr_ms_hyena_idle;
    else _prev_spr = spr_ms_centurion_idle;

    return {
        head: _hd, torso: _tr, arms: _am, legs: _lg, backpack: _bp, weapon: _wp,
        total_armor: _tot_armor, total_mass: _tot_mass, max_capacity: _max_capacity,
        mass_overloaded: _mass_overloaded, total_draw: _tot_draw, power_output: _tr.power_output,
        net_power: _net_power, reactor_overloaded: _reactor_overloaded,
        walk_speed: _walk_spd, boost_speed: _boost_spd, combat_rating: _oss,
        weight_class: _w_class, preview_sprite: _prev_spr, move_type: _move_type
    };
};

apply_builder_preset = function(_preset) {
    if (_preset == "GENESIS") {
        builder_head_idx = 5; builder_torso_idx = 5; builder_arms_idx = 5;
        builder_legs_idx = 5; builder_bp_idx = 5; builder_wp_idx = 5;
        builder_alloy_idx = 5; builder_custom_name = "GHA-00 GENESIS";
    } else if (_preset == "STRIKER") {
        builder_head_idx = 1; builder_torso_idx = 4; builder_arms_idx = 1;
        builder_legs_idx = 3; builder_bp_idx = 1; builder_wp_idx = 1;
        builder_alloy_idx = 2; builder_custom_name = "AETH-02 STRIKER";
    } else if (_preset == "FORTRESS") {
        builder_head_idx = 2; builder_torso_idx = 2; builder_arms_idx = 2;
        builder_legs_idx = 2; builder_bp_idx = 2; builder_wp_idx = 0;
        builder_alloy_idx = 3; builder_custom_name = "TITAN-04 BARRICADE";
    } else if (_preset == "SCAVENGER") {
        builder_head_idx = 3; builder_torso_idx = 3; builder_arms_idx = 0;
        builder_legs_idx = 1; builder_bp_idx = 3; builder_wp_idx = 4;
        builder_alloy_idx = 0; builder_custom_name = "RUST-09 CHIMERA";
    } else if (_preset == "RANDOM") {
        builder_head_idx = irandom(5); builder_torso_idx = irandom(5);
        builder_arms_idx = irandom(5); builder_legs_idx = irandom(5);
        builder_bp_idx = irandom(5); builder_wp_idx = irandom(5);
        builder_alloy_idx = irandom(5);
        var _prefixes = ["APEX", "SOLAR", "VANGUARD", "IRON", "VOID", "KINETIC"];
        builder_custom_name = _prefixes[irandom(array_length(_prefixes)-1)] + "-X" + string(irandom_range(10, 99));
    }
    scr_audio_play_ui("click");
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
        name: builder_custom_name + " [CUSTOM BUILD]",
        faction_id: "pmc_player",
        category: "CUSTOM_MECH",
        move_type: _t.move_type,
        alloy_id: builder_alloys[builder_alloy_idx],
        sprite_asset: _t.preview_sprite,
        sprite_back_asset: _t.preview_sprite,
        weapon_name: _t.weapon.name,
        weapon_class: _t.weapon.weapon_class,
        hp: _t.total_armor,
        armor: floor(_t.total_armor / 12),
        speed: _t.boost_speed,
        accuracy: 85,
        evasion: 25,
        attack_range: 2,
        role: _t.weight_class,
        doctrine: "Modular CAD Masterwork Prototype",
        aux_system: _t.head.bonus + " // " + _t.backpack.bonus,
        sprites: {
            idle: _t.preview_sprite,
            walk: spr_ms_aether_boost,
            fire: _t.weapon.sprite,
            melee: spr_ms_aether_attack_saber,
            boost: spr_ms_aether_boost,
            damaged: spr_ms_ironclad_idle_damaged,
            destroyed: spr_ms_ironclad_idle_damaged
        }
    };

    // Prepend to master_roster
    array_insert(master_roster, 0, _custom_u);
    atk_faction_idx = 0; // ALL
    atk_cat_idx = 0;     // ALL
    atk_filtered_idx = 0;
    active_debug_tab = 0; // Switch to Combat Lab

    scr_audio_play_ui("boot");
    show_toast("DEPLOYED TO COMBAT LAB: " + builder_custom_name + " ready for live duel testing!", c_lime);
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
            blueprint_id: "bp_player_custom",
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
            components_summary: _t.head.name + " // " + _t.torso.name + " // " + _t.arms.name + " // " + _t.legs.name + " // " + _t.backpack.name + " // " + _t.weapon.name,
            part_composition: { head: _t.head, torso: _t.torso, arms: _t.arms, legs: _t.legs, backpack: _t.backpack, weapon: _t.weapon },
            spec_type: "COMMANDER_CUSTOM",
            combat_pedigree: { sorties_deployed: 0, sorties_survived: 0, confirmed_kills: 0, ace_kills: 0, damage_mitigated: 0, pedigree_rating: "FACTORY_FRESH", telemetry_bonus: 0.0 }
        };
        array_push(_gm.inventory.deployable_mechs, _new_mech);
        show_toast("COMMISSIONED TO FLEET HANGAR: " + builder_custom_name + " added to Hangar!", c_lime);
        scr_audio_play_ui("boot");
    }
};

// =========================================================================
// 9. ASTEROID MINING & PLANETARY RESOURCE EXTRACTION STATE (TAB 2)
// =========================================================================
mining_selected_idx = 0;
mining_sphere_idx = 0;
mining_spheres = ["ALL", "Earth Sphere", "Asteroid Belt", "Jovian System", "Outer Colonies", "Mars Sphere"];
mining_drill_active = false;
mining_drill_heat = 0.0;
mining_drill_timer = 0;
mining_particles = [];
mining_session_extracted = { mat_tungsten: 0, mat_silica_carb: 0, mat_tritium: 0, mat_syn_flux: 0, item_slag: 0 };

get_debug_mining_nodes = function() {
    if (instance_exists(obj_GameManager) && is_array(obj_GameManager.nodes) && array_length(obj_GameManager.nodes) > 0) {
        var _all_nd = obj_GameManager.nodes;
        if (mining_sphere_idx == 0) return _all_nd;
        var _cur_sph = mining_spheres[mining_sphere_idx];
        var _res = [];
        for (var i = 0; i < array_length(_all_nd); i++) {
            var _n = _all_nd[i];
            if (variable_struct_exists(_n, "sphere") && _n.sphere == _cur_sph) {
                array_push(_res, _n);
            }
        }
        if (array_length(_res) == 0) return _all_nd;
        return _res;
    }
    // Fallback default node list if GameManager not loaded
    return [
        { id: "node_asteroid_c14", name: "Asteroid Belt C-14", sphere: "Asteroid Belt", primary_yield: "mat_tungsten", secondary_yield: "mat_silica_carb", yield_rate_primary: 4, yield_rate_secondary: 3, threat_level_pct: 20, status: "ACTIVE_MINING", current_storage: { mat_tungsten: 18, mat_silica_carb: 12 }, assigned_mech_id: "unit_ironclad_01" },
        { id: "node_moon_io4", name: "Volcanic Moon Io-IV", sphere: "Jovian System", primary_yield: "mat_silica_carb", secondary_yield: "mat_tungsten", yield_rate_primary: 6, yield_rate_secondary: 2, threat_level_pct: 35, status: "UNCLAIMED", current_storage: {}, assigned_mech_id: "Unassigned" },
        { id: "node_gas_giant", name: "Gas Giant Orbital Ring", sphere: "Outer Colonies", primary_yield: "mat_tritium", secondary_yield: "none", yield_rate_primary: 3, yield_rate_secondary: 0, threat_level_pct: 50, status: "UNCLAIMED", current_storage: {}, assigned_mech_id: "Unassigned" },
        { id: "node_shipyard_omega", name: "Derelict Shipyard Omega", sphere: "Earth Sphere", primary_yield: "mat_syn_flux", secondary_yield: "item_slag", yield_rate_primary: 3, yield_rate_secondary: 2, threat_level_pct: 65, status: "UNCLAIMED", current_storage: {}, assigned_mech_id: "Unassigned" }
    ];
};

pulse_mine_node = function() {
    var _nodes = get_debug_mining_nodes();
    if (array_length(_nodes) == 0) return;
    var _node = _nodes[clamp(mining_selected_idx, 0, array_length(_nodes) - 1)];

    mining_drill_active = true;
    mining_drill_timer = 25;
    mining_drill_heat = min(100.0, mining_drill_heat + 16.0);

    // Calculate yield with flagship refining multiplier
    var _mult = 1.0;
    if (instance_exists(obj_GameManager)) {
        var _gm = obj_GameManager;
        var _tier = (variable_struct_exists(_gm.flagship, "upgrades") && variable_struct_exists(_gm.flagship.upgrades, "mining_tier")) ? _gm.flagship.upgrades.mining_tier : 1;
        var _tier_mults = [1.25, 1.50, 2.00, 2.50, 3.50];
        _mult = _tier_mults[clamp(_tier - 1, 0, 4)];
    }

    var _yield_p = max(1, floor(_node.yield_rate_primary * _mult * random_range(0.9, 1.3)));
    var _res_p = _node.primary_yield;

    // Add to node storage and session
    if (_res_p != "none") {
        if (!variable_struct_exists(_node.current_storage, _res_p)) variable_struct_set(_node.current_storage, _res_p, 0);
        variable_struct_set(_node.current_storage, _res_p, variable_struct_get(_node.current_storage, _res_p) + _yield_p);

        if (!variable_struct_exists(mining_session_extracted, _res_p)) variable_struct_set(mining_session_extracted, _res_p, 0);
        variable_struct_set(mining_session_extracted, _res_p, variable_struct_get(mining_session_extracted, _res_p) + _yield_p);

        // Add to GameManager inventory directly
        if (instance_exists(obj_GameManager)) {
            var _raw = obj_GameManager.inventory.raw_materials;
            if (!variable_struct_exists(_raw, _res_p)) variable_struct_set(_raw, _res_p, 0);
            variable_struct_set(_raw, _res_p, variable_struct_get(_raw, _res_p) + _yield_p);
        }
    }

    // Spawn floating particle text
    array_push(mining_particles, {
        x: 640 + random_range(-60, 60),
        y: 350 + random_range(-20, 20),
        vy: -2.0,
        life: 60,
        text: "+" + string(_yield_p) + " " + string_upper(string_replace(_res_p, "mat_", "")) + " (" + string(floor(_mult * 100)) + "% Yield)",
        color: make_color_rgb(0, 240, 255)
    });

    scr_audio_play_ui("click");
    show_toast("MINING PULSE: Extracted +" + string(_yield_p) + " " + _res_p + " from " + _node.name + "!", c_aqua);
};

smelt_alloy_debug = function(_alloy_key, _qty) {
    if (instance_exists(obj_GameManager)) {
        var _gm = obj_GameManager;
        var _alloys = _gm.inventory.alloys;
        if (!variable_struct_exists(_alloys, _alloy_key)) variable_struct_set(_alloys, _alloy_key, 0);
        variable_struct_set(_alloys, _alloy_key, variable_struct_get(_alloys, _alloy_key) + _qty);
        scr_audio_play_ui("boot");
        show_toast("SMELTER COMPLETE: Synthesized +" + string(_qty) + " " + _alloy_key + "!", c_yellow);
    }
};

trigger_mining_raid_debug = function() {
    var _nodes = get_debug_mining_nodes();
    if (array_length(_nodes) == 0) return;
    var _node = _nodes[clamp(mining_selected_idx, 0, array_length(_nodes) - 1)];
    if (instance_exists(obj_GameManager)) {
        obj_GameManager.pending_raid = {
            node: _node,
            threat: _node.threat_level_pct,
            target_node_id: _node.id,
            attacker_faction: "faction_syndicate",
            attacker_count: irandom_range(3, 6)
        };
        scr_audio_play_ui("cancel");
        show_toast("PIRATE INVASION TRIGGERED: Alert on " + _node.name + " (Threat: " + string(_node.threat_level_pct) + "%)!", c_red);
    }
};

claim_all_mining_nodes = function() {
    if (instance_exists(obj_GameManager)) {
        var _nodes = obj_GameManager.nodes;
        for (var i = 0; i < array_length(_nodes); i++) {
            _nodes[i].status = "ACTIVE_MINING";
            _nodes[i].assigned_mech_id = "GHA-07 Ironclad Escort";
        }
        scr_audio_play_ui("boot");
        show_toast("MASTER OVERRIDE: All " + string(array_length(_nodes)) + " Solar System mining nodes claimed!", c_lime);
    }
};
