/// @description scr_research_tree_system
// Hearts of Iron IV Style R&D Tech Tree Engine: Weapons, Reactors, Shields, and Upgrades
// Independent of the mech chassis fabrication system. Provides strategic research slots,
// branch prerequisites, turn progression, and fleet-wide passive combat stat multipliers.

// =========================================================================
// 1. INITIALIZE GLOBAL RESEARCH SYSTEM
// =========================================================================
function scr_research_init() {
    if (!instance_exists(obj_GameManager)) return;
    
    if (variable_instance_exists(obj_GameManager, "research_system") && !is_undefined(obj_GameManager.research_system)) {
        return; // Already initialized
    }

    var _sys = {
        max_slots: 3, // Default 3 slots (expandable to 4 and 5 via tech)
        slots: [
            { id: 0, status: "EMPTY", tech_id: "", progress_turns: 0, total_turns: 0, alloy_id: "", alloy_cost: 0 },
            { id: 1, status: "EMPTY", tech_id: "", progress_turns: 0, total_turns: 0, alloy_id: "", alloy_cost: 0 },
            { id: 2, status: "EMPTY", tech_id: "", progress_turns: 0, total_turns: 0, alloy_id: "", alloy_cost: 0 }
        ],
        unlocked_techs: {},
        abandoned_techs: {}, // Mutually exclusive locked/abandoned doctrines
        eureka_boosts: {},   // Battlefield salvage intel discounts (e.g. 0.50 reduction)
        active_category: "WEAPONS", // "WEAPONS", "REACTORS", "SHIELDS", "UPGRADES"
        selected_tech_id: "tech_wpn_heavy_autocannon",
        total_techs_researched: 0,
        scroll_x: 0,
        scroll_y: 0
    };

    // Pre-unlock fundamental Era 0 conventional starter technologies
    _sys.unlocked_techs[$ "tech_wpn_heavy_autocannon"] = true;
    _sys.unlocked_techs[$ "tech_wpn_hydra_rockets"] = true;
    _sys.unlocked_techs[$ "tech_wpn_vibro_blade"] = true;
    _sys.unlocked_techs[$ "tech_rea_gas_cooled_fission"] = true;
    _sys.unlocked_techs[$ "tech_sld_ballistic_buckler"] = true;
    _sys.unlocked_techs[$ "tech_upg_analog_hydraulics"] = true;
    _sys.total_techs_researched = 6;

    obj_GameManager.research_system = _sys;
    show_debug_message("[R&D SYSTEM] Hearts of Iron IV style tech tree initialized with 3 research slots.");
}

// Helper: Get active research system struct safely
function scr_research_get_system() {
    if (!instance_exists(obj_GameManager)) return undefined;
    if (!variable_instance_exists(obj_GameManager, "research_system") || is_undefined(obj_GameManager.research_system)) {
        scr_research_init();
    }
    return obj_GameManager.research_system;
}

// =========================================================================
// 2. MASTER TECHNOLOGY DATABASE (Doctrinal Branches & Modular Blueprints)
// =========================================================================
function scr_research_get_tech_db() {
    static _db = undefined;
    if (!is_undefined(_db)) return _db;

    _db = {};

    // ---------------------------------------------------------------------
    // A. WEAPONS BRANCH (Kinetic & Ballistics / Energy Ordnance)
    // ---------------------------------------------------------------------
    _db[$ "tech_wpn_heavy_autocannon"] = {
        id: "tech_wpn_heavy_autocannon",
        name: "Heavy Kinetic Autocannons",
        category: "WEAPONS",
        tier: 0, tier_name: "ERA 0 // CONVENTIONAL",
        col: 0, row: 0,
        turns: 2, cost_cr: 2500, alloy_id: "", alloy_amt: 0,
        prereqs: [],
        mutually_exclusive_with: [],
        unlocked_parts: ["wp_vulcan_01"],
        bonus_stat: "kinetic_dmg", bonus_val: 0.15,
        summary: "+15% Kinetic damage across autocannons and rotary vulcans.",
        lore: "Gas-operated cyclic cannons firing 105mm armor-piercing sabots, standard on legacy Terran armored fighting vehicles."
    };

    _db[$ "tech_wpn_hyper_velocity_rifle"] = {
        id: "tech_wpn_hyper_velocity_rifle",
        name: "120mm Smoothbore Rifle",
        category: "WEAPONS",
        tier: 1, tier_name: "ERA 1 // EARLY MOBILE SUIT",
        col: 1, row: 0,
        turns: 3, cost_cr: 6000, alloy_id: "", alloy_amt: 0,
        prereqs: ["tech_wpn_heavy_autocannon"],
        mutually_exclusive_with: [],
        unlocked_parts: ["am_adamant_03", "hd_cyclops_03"],
        bonus_stat: "kinetic_pen", bonus_val: 0.25,
        summary: "+25% Armor penetration and +1 weapon effective range.",
        lore: "High-pressure smoothbore cannon firing depleted uranium darts at 1,750 m/s to defeat early composite armor plates."
    };

    _db[$ "tech_wpn_beam_carbine"] = {
        id: "tech_wpn_beam_carbine",
        name: "Particle Beam Rifle",
        category: "WEAPONS",
        tier: 2, tier_name: "ERA 2 // SPACE SUPREMACY",
        col: 2, row: 0,
        turns: 4, cost_cr: 12000, alloy_id: "alloy_titanium_carbide", alloy_amt: 2,
        prereqs: ["tech_wpn_hyper_velocity_rifle", "tech_rea_compact_fusion"],
        mutually_exclusive_with: ["tech_wpn_anti_ship_torpedo"],
        unlocked_parts: ["wp_beam_02", "am_tachyon_05"],
        bonus_stat: "beam_dmg", bonus_val: 0.40,
        summary: "+40% Energy beam damage; burns target armor for 2 turns.",
        lore: "Miniaturized mega-particle accelerator powered by E-Cap cartridges, capable of vaporizing conventional armor hulls on contact."
    };

    _db[$ "tech_wpn_electromagnetic_railgun"] = {
        id: "tech_wpn_electromagnetic_railgun",
        name: "Hyper-Velocity Railgun",
        category: "WEAPONS",
        tier: 3, tier_name: "ERA 3 // APEX PROTOTYPE",
        col: 3, row: 0,
        turns: 5, cost_cr: 24000, alloy_id: "alloy_tungsten_carbide", alloy_amt: 4,
        prereqs: ["tech_wpn_hyper_velocity_rifle"],
        mutually_exclusive_with: ["tech_wpn_tachyon_lance"],
        unlocked_parts: ["wp_rail_03", "wp_sol_04"],
        bonus_stat: "railgun_pierce", bonus_val: 0.65,
        summary: "+65% Railgun damage; penetrates up to 2 stacked units in a formation.",
        lore: "Linear electromagnetic mass driver accelerating solid tungsten darts to Mach 8, delivering kinetic devastation beyond horizon."
    };

    _db[$ "tech_wpn_tachyon_lance"] = {
        id: "tech_wpn_tachyon_lance",
        name: "Tachyon Beam Lance",
        category: "WEAPONS",
        tier: 3, tier_name: "ERA 3 // APEX PROTOTYPE",
        col: 3, row: 2,
        turns: 6, cost_cr: 28000, alloy_id: "alloy_tachyon_superalloy", alloy_amt: 3,
        prereqs: ["tech_wpn_beam_carbine", "tech_wpn_beam_saber"],
        mutually_exclusive_with: ["tech_wpn_electromagnetic_railgun"],
        unlocked_parts: ["wp_tachyon_05"],
        bonus_stat: "beam_dmg", bonus_val: 0.60,
        summary: "+60% Energy Beam damage; superheated plasma stream melts enemy armor.",
        lore: "Continuous mega-particle thermal beam emitter capable of slicing through capital ship hulls and super-heavy bunkers."
    };

    _db[$ "tech_wpn_hydra_rockets"] = {
        id: "tech_wpn_hydra_rockets",
        name: "Unguided Hydra Rockets",
        category: "WEAPONS",
        tier: 0, tier_name: "ERA 0 // CONVENTIONAL",
        col: 0, row: 1,
        turns: 2, cost_cr: 2000, alloy_id: "", alloy_amt: 0,
        prereqs: [],
        mutually_exclusive_with: [],
        unlocked_parts: [],
        bonus_stat: "missile_blast", bonus_val: 0.20,
        summary: "+20% Splash blast damage against infantry squads and light armor.",
        lore: "Ripple-fire rocket canisters mounted on dropships and tactical chassis for carpet bombardment."
    };

    _db[$ "tech_wpn_guided_swarm_missiles"] = {
        id: "tech_wpn_guided_swarm_missiles",
        name: "Micro-Missile Swarm Pods",
        category: "WEAPONS",
        tier: 1, tier_name: "ERA 1 // EARLY MOBILE SUIT",
        col: 1, row: 1,
        turns: 3, cost_cr: 5500, alloy_id: "", alloy_amt: 0,
        prereqs: ["tech_wpn_hydra_rockets"],
        mutually_exclusive_with: [],
        unlocked_parts: [],
        bonus_stat: "missile_dmg", bonus_val: 0.35,
        summary: "+35% Missile damage; enables indirect fire over cliffs without LOS penalty.",
        lore: "Lidar-guided micro-munitions that disperse in a swirling pattern to bypass point-defense interceptors."
    };

    _db[$ "tech_wpn_anti_ship_torpedo"] = {
        id: "tech_wpn_anti_ship_torpedo",
        name: "Heavy Anti-Ship Torpedo Battery",
        category: "WEAPONS",
        tier: 2, tier_name: "ERA 2 // SPACE SUPREMACY",
        col: 2, row: 1,
        turns: 4, cost_cr: 14000, alloy_id: "alloy_titanium_carbide", alloy_amt: 2,
        prereqs: ["tech_wpn_guided_swarm_missiles"],
        mutually_exclusive_with: ["tech_wpn_beam_carbine"],
        unlocked_parts: [],
        bonus_stat: "anti_ship_dmg", bonus_val: 0.50,
        summary: "+50% Salvo damage against warships, orbital cruisers, and fortified redoubts.",
        lore: "Two-stage thermonuclear torpedoes engineered to crack warship keels and deep underground citadel bunkers."
    };

    _db[$ "tech_wpn_vibro_blade"] = {
        id: "tech_wpn_vibro_blade",
        name: "Titanium Vibro-Blade",
        category: "WEAPONS",
        tier: 0, tier_name: "ERA 0 // CONVENTIONAL",
        col: 0, row: 2,
        turns: 2, cost_cr: 1800, alloy_id: "", alloy_amt: 0,
        prereqs: [],
        mutually_exclusive_with: [],
        unlocked_parts: [],
        bonus_stat: "melee_base", bonus_val: 0.15,
        summary: "+15% Base melee damage in close-quarters skirmishes.",
        lore: "Solid titanium machete utilizing ultrasonic oscillation to shear through armor joint seals."
    };

    _db[$ "tech_wpn_plasma_heat_blade"] = {
        id: "tech_wpn_plasma_heat_blade",
        name: "High-Frequency Heat Hawk",
        category: "WEAPONS",
        tier: 1, tier_name: "ERA 1 // EARLY MOBILE SUIT",
        col: 1, row: 2,
        turns: 3, cost_cr: 4500, alloy_id: "", alloy_amt: 0,
        prereqs: ["tech_wpn_vibro_blade"],
        mutually_exclusive_with: [],
        unlocked_parts: [],
        bonus_stat: "melee_pen", bonus_val: 0.30,
        summary: "+30% Melee strike damage; ignores 50% of the target's physical armor.",
        lore: "Superheated thermal edge reaching 3,000°C, melting through enemy armor plate like warm butter."
    };

    _db[$ "tech_wpn_beam_saber"] = {
        id: "tech_wpn_beam_saber",
        name: "Mega-Particle Beam Saber",
        category: "WEAPONS",
        tier: 2, tier_name: "ERA 2 // SPACE SUPREMACY",
        col: 2, row: 2,
        turns: 4, cost_cr: 13500, alloy_id: "alloy_vanguard_comp", alloy_amt: 2,
        prereqs: ["tech_wpn_plasma_heat_blade", "tech_rea_compact_fusion"],
        mutually_exclusive_with: [],
        unlocked_parts: [],
        bonus_stat: "beam_melee", bonus_val: 0.50,
        summary: "+50% Close-combat damage; guaranteed limb severance on torso critical strike.",
        lore: "I-field magnetically constrained plasma blade that slices through titanium composite alloy without resistance."
    };

    // ---------------------------------------------------------------------
    // B. REACTORS BRANCH (Energy & Tokamak Cores)
    // ---------------------------------------------------------------------
    _db[$ "tech_rea_gas_cooled_fission"] = {
        id: "tech_rea_gas_cooled_fission",
        name: "Gas-Cooled Fission Generator",
        category: "REACTORS",
        tier: 0, tier_name: "ERA 0 // CONVENTIONAL",
        col: 0, row: 0,
        turns: 2, cost_cr: 3000, alloy_id: "", alloy_amt: 0,
        prereqs: [],
        mutually_exclusive_with: [],
        unlocked_parts: ["tr_colossus_01"],
        bonus_stat: "ap_max", bonus_val: 1,
        summary: "Base +1 Max AP for all fielded mobile suits and heavy combat chassis.",
        lore: "Enriched uranium-235 gas-cooled core encased in lead-boron shielding. Bulky, heavy, but provides steady baseline output."
    };

    _db[$ "tech_rea_compact_fusion"] = {
        id: "tech_rea_compact_fusion",
        name: "Ultracompact He-3 Fusion Core",
        category: "REACTORS",
        tier: 1, tier_name: "ERA 1 // EARLY MOBILE SUIT",
        col: 1, row: 0,
        turns: 3, cost_cr: 8000, alloy_id: "", alloy_amt: 0,
        prereqs: ["tech_rea_gas_cooled_fission"],
        mutually_exclusive_with: [],
        unlocked_parts: ["tr_hyperion_02"],
        bonus_stat: "heat_venting", bonus_val: 0.20,
        summary: "+2 Max AP and +20% Heat Dissipation rate per combat turn.",
        lore: "Aneutronic Helium-3/Deuterium magnetic confinement bottle harvested from Lunar regolith, eliminating radiation hazards."
    };

    _db[$ "tech_rea_catalytic_prometheus"] = {
        id: "tech_rea_catalytic_prometheus",
        name: "Minovsky-Prometheus Catalytic Generator",
        category: "REACTORS",
        tier: 2, tier_name: "ERA 2 // SPACE SUPREMACY",
        col: 2, row: 0,
        turns: 4, cost_cr: 16000, alloy_id: "alloy_vanguard_comp", alloy_amt: 2,
        prereqs: ["tech_rea_compact_fusion"],
        mutually_exclusive_with: [],
        unlocked_parts: ["tr_damascus_04", "bp_plasma_03"],
        bonus_stat: "catalytic_boost", bonus_val: 0.35,
        summary: "+3 Max AP, +35% Heat Dissipation; enables Overboost thruster actions.",
        lore: "Breakthrough catalyst lattice achieving 400% reactor power density, capable of sustaining particle beam arrays indefinitely."
    };

    _db[$ "tech_rea_antimatter_pinch"] = {
        id: "tech_rea_antimatter_pinch",
        name: "Antimatter-Pinch Singularity Drive",
        category: "REACTORS",
        tier: 3, tier_name: "ERA 3 // APEX PROTOTYPE",
        col: 3, row: 0,
        turns: 6, cost_cr: 32000, alloy_id: "alloy_chronos_aegis", alloy_amt: 3,
        prereqs: ["tech_rea_catalytic_prometheus"],
        mutually_exclusive_with: ["tech_rea_tachyon_cyclotron"],
        unlocked_parts: ["tr_sol_05", "bp_tachyon_05"],
        bonus_stat: "zero_point", bonus_val: 0.50,
        summary: "+4 Max AP, +50% Heat Dissipation; mechs generate zero heat on normal movement.",
        lore: "Positronium magnetic pinch drive harnessing microscopic antimatter annihilation pulses for near-infinite kinetic energy."
    };

    _db[$ "tech_rea_tachyon_cyclotron"] = {
        id: "tech_rea_tachyon_cyclotron",
        name: "Tachyon Cyclotron Fortress Core",
        category: "REACTORS",
        tier: 3, tier_name: "ERA 3 // APEX PROTOTYPE",
        col: 3, row: 1,
        turns: 6, cost_cr: 32000, alloy_id: "alloy_chronos_aegis", alloy_amt: 3,
        prereqs: ["tech_rea_catalytic_prometheus"],
        mutually_exclusive_with: ["tech_rea_antimatter_pinch"],
        unlocked_parts: ["tr_sol_05", "bp_tachyon_05"],
        bonus_stat: "barrier_absorb", bonus_val: 0.30,
        summary: "+30% Forcefield Barrier absorption and +45 MW continuous reactor surplus.",
        lore: "Heavy magnetic cyclotron reactor that routes excess particle resonance directly into protective energy bulkheads."
    };

    _db[$ "tech_rea_superconducting_caps"] = {
        id: "tech_rea_superconducting_caps",
        name: "Superconducting Magnetic Capacitors",
        category: "REACTORS",
        tier: 1, tier_name: "ERA 1 // EARLY MOBILE SUIT",
        col: 1, row: 1,
        turns: 3, cost_cr: 7000, alloy_id: "", alloy_amt: 0,
        prereqs: ["tech_rea_compact_fusion"],
        mutually_exclusive_with: [],
        unlocked_parts: [],
        bonus_stat: "energy_cap", bonus_val: 25,
        summary: "+25 Maximum Energy Buffer; prevents weapon lockout during continuous firing.",
        lore: "Cryogenic niobium-titanium magnetic coils that store immense electrical charge for instantaneous surge discharge."
    };

    // ---------------------------------------------------------------------
    // C. SHIELDS BRANCH (Chassis & Defense)
    // ---------------------------------------------------------------------
    _db[$ "tech_sld_ballistic_buckler"] = {
        id: "tech_sld_ballistic_buckler",
        name: "Reinforced Titanium Buckler",
        category: "SHIELDS",
        tier: 0, tier_name: "ERA 0 // CONVENTIONAL",
        col: 0, row: 0,
        turns: 2, cost_cr: 2500, alloy_id: "", alloy_amt: 0,
        prereqs: [],
        mutually_exclusive_with: [],
        unlocked_parts: [],
        bonus_stat: "shield_armor", bonus_val: 25,
        summary: "+25 Armor to Shield Arm; -15% kinetic projectile damage taken.",
        lore: "Curved laminated titanium-carbide shield designed to deflect incoming solid shot and artillery shrapnel."
    };

    _db[$ "tech_sld_anti_beam_coating"] = {
        id: "tech_sld_anti_beam_coating",
        name: "Ablative Anti-Beam Coating",
        category: "SHIELDS",
        tier: 1, tier_name: "ERA 1 // EARLY MOBILE SUIT",
        col: 1, row: 0,
        turns: 3, cost_cr: 7000, alloy_id: "", alloy_amt: 0,
        prereqs: ["tech_sld_ballistic_buckler"],
        mutually_exclusive_with: [],
        unlocked_parts: [],
        bonus_stat: "beam_resist", bonus_val: 0.30,
        summary: "+30% Energy/Beam damage resistance; initial beam hits vaporize coating instead of penetrating hull.",
        lore: "Micro-ceramic spray treatment applied over armored surfaces that diffuses and boils away incoming particle energy."
    };

    _db[$ "tech_sld_composite_reactive"] = {
        id: "tech_sld_composite_reactive",
        name: "Explosive Reactive Shield",
        category: "SHIELDS",
        tier: 2, tier_name: "ERA 2 // SPACE SUPREMACY",
        col: 2, row: 0,
        turns: 4, cost_cr: 15000, alloy_id: "alloy_titanium_carbide", alloy_amt: 2,
        prereqs: ["tech_sld_anti_beam_coating"],
        mutually_exclusive_with: ["tech_sld_i_field_emitter"],
        unlocked_parts: ["hd_damascus_04", "lg_titan_03"],
        bonus_stat: "missile_deflect", bonus_val: 0.40,
        summary: "+45 Shield Arm Armor; reactive explosive tiles outward-detonate to neutralize missile warheads.",
        lore: "Layered sandwich of tungsten-ceramic plates and explosive reactive wafers that detonate outward against shaped charges."
    };

    _db[$ "tech_sld_i_field_emitter"] = {
        id: "tech_sld_i_field_emitter",
        name: "Miniaturized I-Field Emitter",
        category: "SHIELDS",
        tier: 2, tier_name: "ERA 2 // SPACE SUPREMACY",
        col: 2, row: 1,
        turns: 4, cost_cr: 18000, alloy_id: "alloy_vanguard_comp", alloy_amt: 2,
        prereqs: ["tech_sld_anti_beam_coating", "tech_rea_compact_fusion"],
        mutually_exclusive_with: ["tech_sld_composite_reactive"],
        unlocked_parts: ["hd_tachyon_05"],
        bonus_stat: "i_field_beam", bonus_val: 0.50,
        summary: "50% Beam deflection field; curves high-energy particle beams away from torso.",
        lore: "Localized Minovsky particle field generator capable of curving particle beams harmlessly into surrounding space."
    };

    _db[$ "tech_sld_magnetic_barrier"] = {
        id: "tech_sld_magnetic_barrier",
        name: "Phase-Shift Magnetic Barrier",
        category: "SHIELDS",
        tier: 3, tier_name: "ERA 3 // APEX PROTOTYPE",
        col: 3, row: 0,
        turns: 5, cost_cr: 28000, alloy_id: "alloy_chronos_aegis", alloy_amt: 4,
        prereqs: ["tech_sld_anti_beam_coating"],
        prereqs_any: ["tech_sld_composite_reactive", "tech_sld_i_field_emitter"],
        mutually_exclusive_with: ["tech_sld_damascus_citadel"],
        unlocked_parts: ["lg_damascus_05"],
        bonus_stat: "barrier_absorb", bonus_val: 0.40,
        summary: "Active energy forcefield that absorbs 40% of all incoming damage before armor rolls.",
        lore: "Projected superconducting magnetic forcefield creating a high-density plasma curtain in front of the battlegroup."
    };

    _db[$ "tech_sld_damascus_citadel"] = {
        id: "tech_sld_damascus_citadel",
        name: "Damascus Fortress Bulwark",
        category: "SHIELDS",
        tier: 3, tier_name: "ERA 3 // APEX PROTOTYPE",
        col: 3, row: 1,
        turns: 5, cost_cr: 28000, alloy_id: "alloy_reactive_damascus", alloy_amt: 4,
        prereqs: ["tech_sld_anti_beam_coating"],
        prereqs_any: ["tech_sld_composite_reactive", "tech_sld_i_field_emitter"],
        mutually_exclusive_with: ["tech_sld_magnetic_barrier"],
        unlocked_parts: ["lg_damascus_05"],
        bonus_stat: "shield_armor", bonus_val: 60,
        summary: "+60 Shield Armor and -35% incoming kinetic & explosive damage.",
        lore: "Layered Damascus-adamantine composite shield capable of surviving direct nuclear ordnance detonating against its face."
    };

    // ---------------------------------------------------------------------
    // D. UPGRADES BRANCH (Mobility & Verniers)
    // ---------------------------------------------------------------------
    _db[$ "tech_upg_analog_hydraulics"] = {
        id: "tech_upg_analog_hydraulics",
        name: "Reinforced Hydraulic Actuators",
        category: "UPGRADES",
        tier: 0, tier_name: "ERA 0 // CONVENTIONAL",
        col: 0, row: 0,
        turns: 2, cost_cr: 2000, alloy_id: "", alloy_amt: 0,
        prereqs: [],
        mutually_exclusive_with: [],
        unlocked_parts: ["hd_vanguard_01", "am_colossus_01", "lg_vanguard_01", "bp_heavy_01"],
        bonus_stat: "move_range", bonus_val: 1,
        summary: "+1 Movement Range across all terrain; -10% mobility penalty on rough terrain.",
        lore: "High-pressure synthetic fluid lines and titanium-sealed cylinders replacing mechanical gear trains in limb joints."
    };

    _db[$ "tech_upg_vernier_gimbals"] = {
        id: "tech_upg_vernier_gimbals",
        name: "Omni-Directional Vernier Thrusters",
        category: "UPGRADES",
        tier: 1, tier_name: "ERA 1 // EARLY MOBILE SUIT",
        col: 1, row: 0,
        turns: 3, cost_cr: 6500, alloy_id: "", alloy_amt: 0,
        prereqs: ["tech_upg_analog_hydraulics"],
        mutually_exclusive_with: [],
        unlocked_parts: ["hd_aether_02", "tr_phantom_03", "am_vernier_02", "lg_stratos_02", "bp_vernier_02"],
        bonus_stat: "evasion", bonus_val: 0.15,
        summary: "+15% Unit Evasion; +20% Thruster Dodge chance in combat cutscenes.",
        lore: "Cold-gas RCS thruster nozzles distributed across shoulders and legs for instantaneous lateral vectoring."
    };

    _db[$ "tech_upg_multi_sensor_radome"] = {
        id: "tech_upg_multi_sensor_radome",
        name: "Multi-Spectrum Sensor Radome",
        category: "UPGRADES",
        tier: 2, tier_name: "ERA 2 // SPACE SUPREMACY",
        col: 2, row: 0,
        turns: 4, cost_cr: 12500, alloy_id: "", alloy_amt: 0,
        prereqs: ["tech_upg_vernier_gimbals"],
        mutually_exclusive_with: [],
        unlocked_parts: [],
        bonus_stat: "hit_accuracy", bonus_val: 0.20,
        summary: "+20% Weapon Hit Accuracy; +1 Tactical Detection range on the battlefield.",
        lore: "Phase-array microwave radar and quantum lidar housed in an aerodynamic disc radome, cutting through jamming."
    };

    _db[$ "tech_upg_nanite_cooling"] = {
        id: "tech_upg_nanite_cooling",
        name: "Nanite Thermal Coolant System",
        category: "UPGRADES",
        tier: 3, tier_name: "ERA 3 // APEX PROTOTYPE",
        col: 3, row: 0,
        turns: 5, cost_cr: 22000, alloy_id: "alloy_chronos_aegis", alloy_amt: 2,
        prereqs: ["tech_upg_multi_sensor_radome"],
        mutually_exclusive_with: ["tech_upg_overboost_rig"],
        unlocked_parts: ["am_aerogel_04", "lg_aerogel_04", "bp_aerogel_04"],
        bonus_stat: "heat_reduction", bonus_val: 0.30,
        summary: "-30% Heat generated per weapon shot; mechs automatically vent 15 heat each combat turn.",
        lore: "Micro-circulatory liquid metal cooling loop with self-repairing nanite suspensions that rapidly dissipate thermal buildup."
    };

    _db[$ "tech_upg_overboost_rig"] = {
        id: "tech_upg_overboost_rig",
        name: "High-G Vector Overboost Rig",
        category: "UPGRADES",
        tier: 3, tier_name: "ERA 3 // APEX PROTOTYPE",
        col: 3, row: 1,
        turns: 5, cost_cr: 22000, alloy_id: "alloy_chronos_aegis", alloy_amt: 2,
        prereqs: ["tech_upg_multi_sensor_radome"],
        mutually_exclusive_with: ["tech_upg_nanite_cooling"],
        unlocked_parts: ["am_aerogel_04", "lg_aerogel_04", "bp_aerogel_04"],
        bonus_stat: "evasion", bonus_val: 0.25,
        summary: "+25% Evasion and +30 kph Overboost speed for high-G tactical dashes.",
        lore: "Liquid-fueled auxiliary thruster manifolds providing explosive burst acceleration to evade sniper fire."
    };

    _db[$ "tech_upg_research_expansion_1"] = {
        id: "tech_upg_research_expansion_1",
        name: "Advanced R&D Laboratory Wing",
        category: "UPGRADES",
        tier: 1, tier_name: "ERA 1 // EARLY MOBILE SUIT",
        col: 1, row: 1,
        turns: 3, cost_cr: 10000, alloy_id: "", alloy_amt: 0,
        prereqs: ["tech_upg_analog_hydraulics"],
        mutually_exclusive_with: [],
        unlocked_parts: [],
        bonus_stat: "slot_expansion", bonus_val: 4,
        summary: "Permanently expands PMC R&D capacity to 4 Concurrent Research Slots.",
        lore: "Dedicated hangar retrofit housing precision diagnostic cleanrooms and automated CAD workstations."
    };

    _db[$ "tech_upg_research_expansion_2"] = {
        id: "tech_upg_research_expansion_2",
        name: "Quantum Supercomputing Cluster",
        category: "UPGRADES",
        tier: 2, tier_name: "ERA 2 // SPACE SUPREMACY",
        col: 2, row: 1,
        turns: 5, cost_cr: 25000, alloy_id: "alloy_hyperion_matrix", alloy_amt: 2,
        prereqs: ["tech_upg_research_expansion_1"],
        mutually_exclusive_with: [],
        unlocked_parts: [],
        bonus_stat: "slot_expansion", bonus_val: 5,
        summary: "Permanently expands PMC R&D capacity to 5 Concurrent Research Slots.",
        lore: "Cryogenically-cooled optical lattice supercomputer capable of simulating millions of alloy stress tests per second."
    };

    return _db;
}

// =========================================================================
// 3. RESEARCH STATE & PROGRESSION QUERIES
// =========================================================================

/// @function scr_research_is_unlocked(_tech_id)
function scr_research_is_unlocked(_tech_id) {
    var _sys = scr_research_get_system();
    if (is_undefined(_sys)) return false;
    return variable_struct_exists(_sys.unlocked_techs, _tech_id) && _sys.unlocked_techs[$ _tech_id] == true;
}

/// @function scr_research_is_abandoned(_tech_id)
function scr_research_is_abandoned(_tech_id) {
    var _sys = scr_research_get_system();
    if (is_undefined(_sys)) return false;
    if (variable_struct_exists(_sys, "abandoned_techs") && !is_undefined(_sys.abandoned_techs)) {
        return variable_struct_exists(_sys.abandoned_techs, _tech_id) && _sys.abandoned_techs[$ _tech_id] == true;
    }
    return false;
}

/// @function scr_research_is_in_progress(_tech_id)
function scr_research_is_in_progress(_tech_id) {
    var _sys = scr_research_get_system();
    if (is_undefined(_sys)) return -1;
    for (var i = 0; i < array_length(_sys.slots); i++) {
        if (_sys.slots[i].status == "RESEARCHING" && _sys.slots[i].tech_id == _tech_id) {
            return i;
        }
    }
    return -1;
}

/// @function scr_research_can_research(_tech_id)
function scr_research_can_research(_tech_id) {
    if (scr_research_is_unlocked(_tech_id)) return false;
    if (scr_research_is_abandoned(_tech_id)) return false;
    if (scr_research_is_in_progress(_tech_id) != -1) return false;

    var _db = scr_research_get_tech_db();
    if (!variable_struct_exists(_db, _tech_id)) return false;
    var _tech = _db[$ _tech_id];

    // Check mutually exclusive rival techs
    if (variable_struct_exists(_tech, "mutually_exclusive_with") && is_array(_tech.mutually_exclusive_with)) {
        for (var m = 0; m < array_length(_tech.mutually_exclusive_with); m++) {
            var _rival = _tech.mutually_exclusive_with[m];
            if (scr_research_is_unlocked(_rival) || scr_research_is_in_progress(_rival) != -1) {
                return false;
            }
        }
    }

    // Check all required prerequisites (AND)
    if (variable_struct_exists(_tech, "prereqs") && is_array(_tech.prereqs)) {
        for (var p = 0; p < array_length(_tech.prereqs); p++) {
            var _pre = _tech.prereqs[p];
            if (!scr_research_is_unlocked(_pre)) return false;
        }
    }

    // Check any prerequisites if defined (OR)
    if (variable_struct_exists(_tech, "prereqs_any") && is_array(_tech.prereqs_any) && array_length(_tech.prereqs_any) > 0) {
        var _any_met = false;
        for (var pa = 0; pa < array_length(_tech.prereqs_any); pa++) {
            if (scr_research_is_unlocked(_tech.prereqs_any[pa])) {
                _any_met = true;
                break;
            }
        }
        if (!_any_met) return false;
    }

    return true;
}

/// @function scr_research_get_bonus(_bonus_stat)
function scr_research_get_bonus(_bonus_stat) {
    var _sys = scr_research_get_system();
    if (is_undefined(_sys)) return 0.0;

    var _db = scr_research_get_tech_db();
    var _tot = 0.0;
    var _names = variable_struct_get_names(_sys.unlocked_techs);
    for (var i = 0; i < array_length(_names); i++) {
        var _tid = _names[i];
        if (_sys.unlocked_techs[$ _tid] == true && variable_struct_exists(_db, _tid)) {
            var _t = _db[$ _tid];
            if (_t.bonus_stat == _bonus_stat) {
                _tot += _t.bonus_val;
            }
        }
    }
    return _tot;
}

/// @function scr_research_award_salvage_intel(_target, _discount)
function scr_research_award_salvage_intel(_target, _discount) {
    var _sys = scr_research_get_system();
    if (is_undefined(_sys)) return "";
    var _db = scr_research_get_tech_db();

    // 1. Check if an active slot is currently researching this tech or category
    for (var s = 0; s < array_length(_sys.slots); s++) {
        var _slot = _sys.slots[s];
        if (_slot.status == "RESEARCHING" && _slot.tech_id != "") {
            var _t = _db[$ _slot.tech_id];
            if (_slot.tech_id == _target || _t.category == _target) {
                var _saved = max(1, ceil(_slot.total_turns * _discount));
                _slot.progress_turns = min(_slot.total_turns - 1, _slot.progress_turns + _saved);
                return "BLACK BOX EUREKA: Advanced " + _t.name + " by " + string(_saved) + " Turns (" + string(floor(_discount * 100)) + "% Boost)!";
            }
        }
    }

    // 2. Otherwise store as pre-seeded Eureka boost for future project
    if (!variable_struct_exists(_sys, "eureka_boosts") || is_undefined(_sys.eureka_boosts)) {
        _sys.eureka_boosts = {};
    }
    _sys.eureka_boosts[$ _target] = _discount;
    return "BLACK BOX ARCHIVED: 50% Breakthrough boost secured for next " + string(_target) + " project!";
}

// =========================================================================
// 4. RESEARCH ACTIONS (Start Project, Cancel, Advance Turn)
// =========================================================================

/// @function scr_research_start(_tech_id, _slot_idx)
function scr_research_start(_tech_id, _slot_idx) {
    var _sys = scr_research_get_system();
    if (is_undefined(_sys)) return false;
    if (!instance_exists(obj_GameManager)) return false;

    if (_slot_idx < 0 || _slot_idx >= array_length(_sys.slots)) {
        add_log("[R&D ERROR] Invalid research slot index: " + string(_slot_idx));
        return false;
    }

    if (!scr_research_can_research(_tech_id)) {
        scr_audio_play_ui("cancel");
        show_toast("CANNOT RESEARCH: Prerequisites not met or doctrine abandoned!", c_orange);
        return false;
    }

    var _db = scr_research_get_tech_db();
    var _tech = _db[$ _tech_id];

    // Check Credits
    if (obj_GameManager.funds < _tech.cost_cr) {
        scr_audio_play_ui("cancel");
        show_toast("INSUFFICIENT FUNDS: Requires " + string(_tech.cost_cr) + " Cr!", c_red);
        return false;
    }

    // Check Alloy requirements if any
    if (_tech.alloy_id != "" && _tech.alloy_amt > 0) {
        var _has_alloy = false;
        if (variable_instance_exists(obj_GameManager, "inventory") && variable_struct_exists(obj_GameManager.inventory, "alloys")) {
            var _cur_amt = variable_struct_get(obj_GameManager.inventory.alloys, _tech.alloy_id) ?? 0;
            if (_cur_amt >= _tech.alloy_amt) _has_alloy = true;
        }
        if (!_has_alloy) {
            scr_audio_play_ui("cancel");
            show_toast("MISSING MATERIAL: Requires " + string(_tech.alloy_amt) + "x " + _tech.alloy_id + "!", c_red);
            return false;
        }
        // Deduct alloy
        obj_GameManager.inventory.alloys[$ _tech.alloy_id] -= _tech.alloy_amt;
    }

    // Deduct Funds
    obj_GameManager.funds -= _tech.cost_cr;

    // Check for active Eureka Boost (50% turn reduction)
    var _boost = 0.0;
    if (variable_struct_exists(_sys, "eureka_boosts") && !is_undefined(_sys.eureka_boosts)) {
        if (variable_struct_exists(_sys.eureka_boosts, _tech_id)) {
            _boost = _sys.eureka_boosts[$ _tech_id];
            variable_struct_remove(_sys.eureka_boosts, _tech_id);
        } else if (variable_struct_exists(_sys.eureka_boosts, _tech.category)) {
            _boost = _sys.eureka_boosts[$ _tech.category];
            variable_struct_remove(_sys.eureka_boosts, _tech.category);
        }
    }
    var _final_turns = max(1, ceil(_tech.turns * (1.0 - _boost)));

    // Assign to slot
    var _slot = _sys.slots[_slot_idx];
    _slot.status = "RESEARCHING";
    _slot.tech_id = _tech_id;
    _slot.progress_turns = 0;
    _slot.total_turns = _final_turns;
    _slot.alloy_id = _tech.alloy_id;
    _slot.alloy_cost = _tech.alloy_amt;

    // Lock out mutually exclusive rivals permanently
    if (variable_struct_exists(_tech, "mutually_exclusive_with") && is_array(_tech.mutually_exclusive_with)) {
        if (!variable_struct_exists(_sys, "abandoned_techs") || is_undefined(_sys.abandoned_techs)) {
            _sys.abandoned_techs = {};
        }
        for (var m = 0; m < array_length(_tech.mutually_exclusive_with); m++) {
            var _rid = _tech.mutually_exclusive_with[m];
            _sys.abandoned_techs[$ _rid] = true;
        }
    }

    scr_audio_play_ui("confirm");
    var _msg = "[R&D COMMENCED] Slot #" + string(_slot_idx + 1) + ": " + _tech.name;
    if (_boost > 0) _msg += " (★ EUREKA -50% DURATION)";
    show_toast(_msg, c_lime);
    return true;
}

/// @function scr_research_cancel(_slot_idx)
function scr_research_cancel(_slot_idx) {
    var _sys = scr_research_get_system();
    if (is_undefined(_sys)) return false;
    if (_slot_idx < 0 || _slot_idx >= array_length(_sys.slots)) return false;

    var _slot = _sys.slots[_slot_idx];
    if (_slot.status != "RESEARCHING") return false;

    var _db = scr_research_get_tech_db();
    var _tech = _db[$ _slot.tech_id];

    // Partial refund (50% credits)
    var _refund = floor(_tech.cost_cr * 0.50);
    obj_GameManager.funds += _refund;

    _slot.status = "EMPTY";
    _slot.tech_id = "";
    _slot.progress_turns = 0;
    _slot.total_turns = 0;

    scr_audio_play_ui("click");
    show_toast("[R&D CANCELLED] Project halted. 50% funds refunded (" + string(_refund) + " Cr).", c_yellow);
    return true;
}

/// @function scr_research_advance_turn()
function scr_research_advance_turn() {
    var _sys = scr_research_get_system();
    if (is_undefined(_sys)) return;

    var _db = scr_research_get_tech_db();

    for (var s = 0; s < array_length(_sys.slots); s++) {
        var _slot = _sys.slots[s];
        if (_slot.status == "RESEARCHING" && _slot.tech_id != "") {
            _slot.progress_turns++;

            if (_slot.progress_turns >= _slot.total_turns) {
                // Completed!
                var _tid = _slot.tech_id;
                var _t = _db[$ _tid];
                _sys.unlocked_techs[$ _tid] = true;
                _sys.total_techs_researched++;

                _slot.status = "EMPTY";
                _slot.tech_id = "";
                _slot.progress_turns = 0;
                _slot.total_turns = 0;

                // Handle Research Slot expansions immediately
                if (_t.bonus_stat == "slot_expansion") {
                    var _new_max = floor(_t.bonus_val);
                    while (array_length(_sys.slots) < _new_max) {
                        array_push(_sys.slots, {
                            id: array_length(_sys.slots),
                            status: "EMPTY", tech_id: "",
                            progress_turns: 0, total_turns: 0,
                            alloy_id: "", alloy_cost: 0
                        });
                    }
                    _sys.max_slots = _new_max;
                    show_toast("★ [EXPANSION] " + string(_new_max) + "th Research Slot Activated!", c_yellow);
                }

                // Audio & Notification
                scr_audio_play_sfx(snd_discovery_fanfare, 1.0, 0.0);
                show_toast("★ [TECH RESEARCHED] " + _t.name + " (" + _t.category + ") UNLOCKED!", c_lime);
                if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "last_turn_events")) {
                    array_push(obj_GameManager.last_turn_events, "★ [R&D MILESTONE] Completed breakthrough: " + _t.name + " (" + _t.summary + ")");
                }
            }
        }
    }
}

// =========================================================================
// 5. HEARTS OF IRON IV STYLE RESEARCH TREE UI RENDERING
// =========================================================================
function scr_draw_research_tree_hoi4(_pan_x, _pan_y, _pan_w, _pan_h, _mx, _my, _click) {
    var _sys = scr_research_get_system();
    if (is_undefined(_sys)) return;
    var _db = scr_research_get_tech_db();

    // ---------------------------------------------------------------------
    // A. TOP HOI4 RESEARCH SLOTS HEADER (x: _pan_x + 16, y: _pan_y + 44)
    // ---------------------------------------------------------------------
    var _slot_bar_x = _pan_x + 16;
    var _slot_bar_y = _pan_y + 42;
    var _slot_bar_w = _pan_w - 32;
    var _slot_bar_h = 72;

    draw_set_color(make_color_rgb(18, 26, 38));
    draw_rectangle(_slot_bar_x, _slot_bar_y, _slot_bar_x + _slot_bar_w, _slot_bar_y + _slot_bar_h, false);
    draw_set_color(make_color_rgb(45, 65, 90));
    draw_rectangle(_slot_bar_x, _slot_bar_y, _slot_bar_x + _slot_bar_w, _slot_bar_y + _slot_bar_h, true);

    // Slots Title Tag
    draw_set_color(make_color_rgb(255, 215, 60));
    draw_text(_slot_bar_x + 12, _slot_bar_y + 6, "HOI4 RESEARCH SLOTS // CONCURRENT PROJECTS [" + string(array_length(_sys.slots)) + " ACTIVE CAPACITIES]");

    // Render Each Research Slot
    var _num_slots = array_length(_sys.slots);
    var _slot_card_w = floor((_slot_bar_w - 24 - (_num_slots - 1) * 8) / _num_slots);
    var _slot_card_h = 42;
    var _slot_card_y = _slot_bar_y + 24;

    for (var s = 0; s < _num_slots; s++) {
        var _sl = _sys.slots[s];
        var _sl_x = _slot_bar_x + 12 + s * (_slot_card_w + 8);
        var _sl_hov = (_mx >= _sl_x && _mx <= _sl_x + _slot_card_w && _my >= _slot_card_y && _my <= _slot_card_y + _slot_card_h);

        if (_sl.status == "RESEARCHING" && _sl.tech_id != "") {
            var _tech_item = _db[$ _sl.tech_id];
            var _pct = clamp(_sl.progress_turns / max(1, _sl.total_turns), 0, 1);

            // Active Card Background
            draw_set_color(make_color_rgb(24, 34, 50));
            draw_rectangle(_sl_x, _slot_card_y, _sl_x + _slot_card_w, _slot_card_y + _slot_card_h, false);
            draw_set_color(make_color_rgb(255, 180, 50));
            draw_rectangle(_sl_x, _slot_card_y, _sl_x + _slot_card_w, _slot_card_y + _slot_card_h, true);

            // Tech Name & Category
            draw_set_color(c_white);
            draw_text_transformed(_sl_x + 6, _slot_card_y + 4, "[" + string(s + 1) + "] " + string_copy(_tech_item.name, 1, 16), 0.72, 0.72, 0);

            // Progress Bar
            var _bar_x = _sl_x + 6;
            var _bar_y = _slot_card_y + 22;
            var _bar_w = _slot_card_w - 48;
            var _bar_h = 10;
            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_w, _bar_y + _bar_h, false);
            draw_set_color(make_color_rgb(60, 220, 100));
            draw_rectangle(_bar_x, _bar_y, _bar_x + floor(_bar_w * _pct), _bar_y + _bar_h, false);
            draw_set_color(make_color_rgb(45, 75, 100));
            draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_w, _bar_y + _bar_h, true);

            // ETA Text
            draw_set_color(make_color_rgb(200, 220, 240));
            var _turns_left = max(1, _sl.total_turns - _sl.progress_turns);
            draw_text_transformed(_bar_x + _bar_w + 6, _bar_y - 2, string(_turns_left) + "T", 0.65, 0.65, 0);

            // Cancel Button [X]
            var _cx = _sl_x + _slot_card_w - 20;
            var _cy = _slot_card_y + 4;
            var _chov = (_mx >= _cx && _mx <= _cx + 16 && _my >= _cy && _my <= _cy + 16);
            if (_chov && _click) {
                scr_research_cancel(s);
            }
            draw_set_color(_chov ? make_color_rgb(255, 60, 60) : make_color_rgb(180, 50, 50));
            draw_rectangle(_cx, _cy, _cx + 16, _cy + 16, false);
            draw_set_color(c_white);
            draw_text_transformed(_cx + 4, _cy + 1, "X", 0.7, 0.7, 0);

        } else {
            // Empty Slot
            var _pulse = 0.5 + 0.5 * sin(current_time * 0.008 + s);
            var _border_col = merge_color(make_color_rgb(45, 65, 90), make_color_rgb(64, 224, 255), _pulse);

            draw_set_color(make_color_rgb(14, 20, 30));
            draw_rectangle(_sl_x, _slot_card_y, _sl_x + _slot_card_w, _slot_card_y + _slot_card_h, false);
            draw_set_color(_sl_hov ? make_color_rgb(64, 224, 255) : _border_col);
            draw_rectangle(_sl_x, _slot_card_y, _sl_x + _slot_card_w, _slot_card_y + _slot_card_h, true);

            draw_set_color(_sl_hov ? c_white : make_color_rgb(100, 140, 180));
            draw_text_transformed(_sl_x + 8, _slot_card_y + 12, "[+] SLOT #" + string(s + 1) + ": ASSIGN PROJECT", 0.72, 0.72, 0);
        }
    }

    // ---------------------------------------------------------------------
    // B. HOI4 BRANCH SELECTOR TABS (x: _pan_x + 16, y: _pan_y + 118)
    // ---------------------------------------------------------------------
    var _cat_names = ["WEAPONS", "REACTORS", "SHIELDS", "UPGRADES"];
    var _cat_labels = [
        "[⚔️ WEAPONS] KINETIC & BALLISTICS",
        "[⚡ REACTORS] ENERGY & TOKAMAK",
        "[🛡️ SHIELDS] CHASSIS & DEFENSE",
        "[⚙️ UPGRADES] MOBILITY & VERNIERS"
    ];
    var _tab_w = floor((_slot_bar_w - 24) / 4);
    var _tab_y = _slot_bar_y + _slot_bar_h + 6;

    for (var c = 0; c < 4; c++) {
        var _tx = _slot_bar_x + c * (_tab_w + 8);
        var _is_cat = (_sys.active_category == _cat_names[c]);
        var _thov = (_mx >= _tx && _mx <= _tx + _tab_w && _my >= _tab_y && _my <= _tab_y + 28);

        if (_thov && _click) {
            _sys.active_category = _cat_names[c];
            scr_audio_play_ui("tab");
        }

        draw_set_color(_is_cat ? make_color_rgb(34, 48, 70) : (_thov ? make_color_rgb(22, 32, 48) : make_color_rgb(14, 20, 30)));
        draw_rectangle(_tx, _tab_y, _tx + _tab_w, _tab_y + 28, false);
        draw_set_color(_is_cat ? make_color_rgb(255, 215, 60) : make_color_rgb(45, 65, 90));
        draw_rectangle(_tx, _tab_y, _tx + _tab_w, _tab_y + 28, true);
        draw_set_color(_is_cat ? c_white : make_color_rgb(150, 180, 210));
        draw_text_transformed(_tx + 10, _tab_y + 7, _cat_labels[c], 0.78, 0.78, 0);
    }

    // ---------------------------------------------------------------------
    // C. HOI4 TECH TREE CANVAS & 4 TIER ERA COLUMNS
    // ---------------------------------------------------------------------
    var _canvas_x = _slot_bar_x;
    var _canvas_y = _tab_y + 34;
    var _canvas_w = _slot_bar_w - 330; // Reserve 330px on right for Detail Dossier
    var _canvas_h = _pan_h - (_canvas_y - _pan_y) - 16;

    draw_set_color(make_color_rgb(12, 16, 24));
    draw_rectangle(_canvas_x, _canvas_y, _canvas_x + _canvas_w, _canvas_y + _canvas_h, false);
    draw_set_color(make_color_rgb(35, 50, 70));
    draw_rectangle(_canvas_x, _canvas_y, _canvas_x + _canvas_w, _canvas_y + _canvas_h, true);

    // 4 Tier Column Headers (Eras)
    var _col_w = floor(_canvas_w / 4);
    var _tier_titles = [
        "TIER 0: PRE-MS (Y2085)",
        "TIER 1: EARLY MS (Y2092)",
        "TIER 2: SPACE (Y2098)",
        "TIER 3: APEX (Y2105)"
    ];

    for (var col = 0; col < 4; col++) {
        var _cx = _canvas_x + col * _col_w;
        // Vertical grid line
        draw_set_color(make_color_rgb(25, 36, 50));
        draw_line(_cx + _col_w, _canvas_y, _cx + _col_w, _canvas_y + _canvas_h);

        // Header Pill
        draw_set_color(make_color_rgb(20, 28, 42));
        draw_rectangle(_cx + 2, _canvas_y + 2, _cx + _col_w - 2, _canvas_y + 24, false);
        draw_set_color(make_color_rgb(100, 130, 160));
        draw_text_transformed(_cx + 8, _canvas_y + 6, _tier_titles[col], 0.65, 0.65, 0);
    }

    // Filter Techs for current category
    var _cat_techs = [];
    var _db_keys = variable_struct_get_names(_db);
    for (var k = 0; k < array_length(_db_keys); k++) {
        var _t_item = _db[$ _db_keys[k]];
        if (_t_item.category == _sys.active_category) {
            array_push(_cat_techs, _t_item);
        }
    }

    // --- Draw Prerequisite Connecting Lines (Behind Cards) ---
    for (var i = 0; i < array_length(_cat_techs); i++) {
        var _t = _cat_techs[i];
        var _t_card_x = _canvas_x + _t.col * _col_w + 10;
        var _t_card_y = _canvas_y + 36 + _t.row * 98;

        for (var p = 0; p < array_length(_t.prereqs); p++) {
            var _pre_id = _t.prereqs[p];
            if (variable_struct_exists(_db, _pre_id)) {
                var _pre_t = _db[$ _pre_id];
                if (_pre_t.category == _sys.active_category) {
                    var _pre_card_x = _canvas_x + _pre_t.col * _col_w + 10;
                    var _pre_card_y = _canvas_y + 36 + _pre_t.row * 98;
                    var _x1 = _pre_card_x + (_col_w - 20);
                    var _y1 = _pre_card_y + 38;
                    var _x2 = _t_card_x;
                    var _y2 = _t_card_y + 38;

                    var _line_col = scr_research_is_unlocked(_t.id) ? make_color_rgb(60, 220, 100) : (scr_research_is_unlocked(_pre_id) ? make_color_rgb(64, 224, 255) : make_color_rgb(45, 55, 70));
                    draw_set_color(_line_col);
                    draw_line_width(_x1, _y1, _x2, _y2, 2.0);
                    draw_circle(_x2, _y2, 3, false);
                }
            }
        }
    }

    // --- Draw Technology Cards ---
    var _card_w = _col_w - 20;
    var _card_h = 76;

    for (var i = 0; i < array_length(_cat_techs); i++) {
        var _t = _cat_techs[i];
        var _tx = _canvas_x + _t.col * _col_w + 10;
        var _ty = _canvas_y + 36 + _t.row * 98;

        var _is_unlocked = scr_research_is_unlocked(_t.id);
        var _is_abandoned = scr_research_is_abandoned(_t.id);
        var _in_prog_slot = scr_research_is_in_progress(_t.id);
        var _can_res = scr_research_can_research(_t.id);
        var _is_sel = (_sys.selected_tech_id == _t.id);
        var _card_hov = (_mx >= _tx && _mx <= _tx + _card_w && _my >= _ty && _my <= _ty + _card_h);

        if (_card_hov && _click) {
            _sys.selected_tech_id = _t.id;
            scr_audio_play_ui("click");
        }

        // Color coding for Card Borders & Fills
        var _fill = make_color_rgb(18, 24, 34);
        var _border = make_color_rgb(40, 55, 75);
        var _status_text = "LOCKED";
        var _status_col = make_color_rgb(120, 140, 160);

        if (_is_unlocked) {
            _fill = make_color_rgb(20, 36, 28);
            _border = make_color_rgb(60, 220, 100);
            _status_text = "RESEARCHED ✓";
            _status_col = make_color_rgb(60, 240, 100);
        } else if (_is_abandoned) {
            _fill = make_color_rgb(32, 14, 18);
            _border = make_color_rgb(140, 40, 50);
            _status_text = "DOCTRINE ABANDONED";
            _status_col = make_color_rgb(255, 70, 70);
        } else if (_in_prog_slot != -1) {
            var _pulse = 0.5 + 0.5 * sin(current_time * 0.01);
            _fill = make_color_rgb(34, 30, 20);
            _border = merge_color(make_color_rgb(255, 140, 40), make_color_rgb(255, 220, 60), _pulse);
            _status_text = "IN PROGRESS [" + string(_sys.slots[_in_prog_slot].progress_turns) + "/" + string(_sys.slots[_in_prog_slot].total_turns) + "T]";
            _status_col = make_color_rgb(255, 215, 60);
        } else if (_can_res) {
            _fill = _card_hov ? make_color_rgb(24, 36, 52) : make_color_rgb(18, 26, 38);
            _border = _card_hov ? make_color_rgb(64, 224, 255) : make_color_rgb(70, 130, 180);
            _status_text = "AVAILABLE (" + string(_t.turns) + "T)";
            _status_col = make_color_rgb(64, 224, 255);
        }

        if (_is_sel) {
            _border = c_white;
        }

        // Card Panel Body
        draw_set_color(_fill);
        draw_rectangle(_tx, _ty, _tx + _card_w, _ty + _card_h, false);
        draw_set_color(_border);
        draw_rectangle(_tx, _ty, _tx + _card_w, _ty + _card_h, true);

        // Tech Title
        draw_set_color(c_white);
        draw_text_transformed(_tx + 8, _ty + 6, string_copy(_t.name, 1, 20), 0.75, 0.75, 0);

        // Status Ribbon
        draw_set_color(_status_col);
        draw_text_transformed(_tx + 8, _ty + 22, _status_text, 0.65, 0.65, 0);

        // Cost & Turns Chip (with FORK badge if divergent)
        draw_set_color(make_color_rgb(180, 200, 225));
        var _cost_str = string(_t.cost_cr) + " Cr";
        if (_t.alloy_amt > 0) _cost_str += " + " + string(_t.alloy_amt) + "x Alloy";
        draw_text_transformed(_tx + 8, _ty + 38, _cost_str, 0.60, 0.60, 0);

        // Mutually exclusive FORK tag
        if (variable_struct_exists(_t, "mutually_exclusive_with") && is_array(_t.mutually_exclusive_with) && array_length(_t.mutually_exclusive_with) > 0) {
            draw_set_color(make_color_rgb(255, 140, 50));
            draw_text_transformed(_tx + _card_w - 48, _ty + 38, "[FORK]", 0.60, 0.60, 0);
        }

        // Summary Snippet
        draw_set_color(make_color_rgb(140, 165, 190));
        draw_text_transformed(_tx + 8, _ty + 54, string_copy(_t.summary, 1, 30) + "...", 0.55, 0.55, 0);
    }

    // ---------------------------------------------------------------------
    // D. HOI4 TECH DETAIL & DOSSIER PANEL (Right 320px)
    // ---------------------------------------------------------------------
    var _dos_x = _canvas_x + _canvas_w + 12;
    var _dos_y = _canvas_y;
    var _dos_w = 308;
    var _dos_h = _canvas_h;

    draw_set_color(make_color_rgb(16, 22, 32));
    draw_rectangle(_dos_x, _dos_y, _dos_x + _dos_w, _dos_y + _dos_h, false);
    draw_set_color(make_color_rgb(45, 65, 90));
    draw_rectangle(_dos_x, _dos_y, _dos_x + _dos_w, _dos_y + _dos_h, true);

    if (variable_struct_exists(_db, _sys.selected_tech_id)) {
        var _st = _db[$ _sys.selected_tech_id];

        // Header Title
        draw_set_color(make_color_rgb(255, 215, 60));
        draw_text(_dos_x + 12, _dos_y + 12, "TECH BLUEPRINT DOSSIER");
        draw_set_color(c_white);
        draw_text_transformed(_dos_x + 12, _dos_y + 32, _st.name, 0.95, 0.95, 0);

        draw_set_color(make_color_rgb(120, 160, 200));
        draw_text_transformed(_dos_x + 12, _dos_y + 54, _st.tier_name + " // " + _st.category, 0.68, 0.68, 0);

        // Mechanical Stat Bonus Box
        var _box_y = _dos_y + 70;
        draw_set_color(make_color_rgb(24, 34, 48));
        draw_rectangle(_dos_x + 10, _box_y, _dos_x + _dos_w - 10, _box_y + 48, false);
        draw_set_color(make_color_rgb(60, 220, 100));
        draw_rectangle(_dos_x + 10, _box_y, _dos_x + _dos_w - 10, _box_y + 48, true);

        draw_set_color(make_color_rgb(60, 240, 120));
        draw_text_transformed(_dos_x + 18, _box_y + 6, "FLEET COMBAT EFFECT:", 0.68, 0.68, 0);
        draw_set_color(c_white);
        draw_text_ext_transformed(_dos_x + 18, _box_y + 20, _st.summary, 14, 270, 0.65, 0.65, 0);

        // Unlocked Modular Blueprints Box
        var _bp_y = _box_y + 54;
        draw_set_color(make_color_rgb(20, 30, 44));
        draw_rectangle(_dos_x + 10, _bp_y, _dos_x + _dos_w - 10, _bp_y + 38, false);
        draw_set_color(make_color_rgb(64, 224, 255));
        draw_rectangle(_dos_x + 10, _bp_y, _dos_x + _dos_w - 10, _bp_y + 38, true);

        draw_set_color(make_color_rgb(64, 224, 255));
        draw_text_transformed(_dos_x + 18, _bp_y + 5, "LICENSED MODULAR BLUEPRINTS:", 0.65, 0.65, 0);
        draw_set_color(make_color_rgb(220, 240, 255));
        var _bp_text = "None (Fleet Doctrine Multiplier)";
        if (variable_struct_exists(_st, "unlocked_parts") && is_array(_st.unlocked_parts) && array_length(_st.unlocked_parts) > 0) {
            _bp_text = "";
            for (var u = 0; u < array_length(_st.unlocked_parts); u++) {
                if (u > 0) _bp_text += ", ";
                _bp_text += _st.unlocked_parts[u];
            }
        }
        draw_text_transformed(_dos_x + 18, _bp_y + 20, string_copy(_bp_text, 1, 38), 0.62, 0.62, 0);

        // Doctrinal Divergence Warning
        var _div_y = _bp_y + 44;
        if (variable_struct_exists(_st, "mutually_exclusive_with") && is_array(_st.mutually_exclusive_with) && array_length(_st.mutually_exclusive_with) > 0) {
            var _rival_id = _st.mutually_exclusive_with[0];
            var _rival_name = variable_struct_exists(_db, _rival_id) ? _db[$ _rival_id].name : _rival_id;
            draw_set_color(make_color_rgb(255, 140, 40));
            draw_text_ext_transformed(_dos_x + 12, _div_y, "⚠ DOCTRINE FORK: Locks out " + _rival_name + " permanently!", 14, 280, 0.62, 0.62, 0);
            _div_y += 24;
        }

        // Historical Lore
        draw_set_color(make_color_rgb(160, 185, 215));
        draw_text_transformed(_dos_x + 12, _div_y, "HISTORICAL DEVELOPMENT:", 0.65, 0.65, 0);
        draw_set_color(make_color_rgb(200, 215, 230));
        draw_text_ext_transformed(_dos_x + 12, _div_y + 16, _st.lore, 15, 280, 0.62, 0.62, 0);

        // Prerequisites Checklist
        var _prq_y = _div_y + 88;
        draw_set_color(make_color_rgb(160, 185, 215));
        draw_text_transformed(_dos_x + 12, _prq_y, "PREREQUISITES CHECKLIST:", 0.65, 0.65, 0);
        if (array_length(_st.prereqs) == 0) {
            draw_set_color(make_color_rgb(60, 220, 100));
            draw_text_transformed(_dos_x + 16, _prq_y + 18, "✓ None (Standard Starter Tech)", 0.62, 0.62, 0);
        } else {
            for (var p = 0; p < array_length(_st.prereqs); p++) {
                var _prq_id = _st.prereqs[p];
                var _is_p_done = scr_research_is_unlocked(_prq_id);
                var _p_name = variable_struct_exists(_db, _prq_id) ? _db[$ _prq_id].name : _prq_id;
                draw_set_color(_is_p_done ? make_color_rgb(60, 220, 100) : make_color_rgb(255, 80, 80));
                draw_text_transformed(_dos_x + 16, _prq_y + 18 + p * 16, (_is_p_done ? "✓ " : "✗ ") + _p_name, 0.62, 0.62, 0);
            }
        }

        // Research Cost & Time Summary
        var _cost_y = _dos_y + _dos_h - 106;
        draw_set_color(make_color_rgb(255, 215, 60));
        draw_text_transformed(_dos_x + 12, _cost_y, "REQUIRED R&D INVESTMENT:", 0.65, 0.65, 0);
        draw_set_color(c_white);
        draw_text_transformed(_dos_x + 16, _cost_y + 16, "• Time Duration: " + string(_st.turns) + " Strategic Turns", 0.62, 0.62, 0);
        draw_text_transformed(_dos_x + 16, _cost_y + 30, "• Capital Funds: " + string(_st.cost_cr) + " Credits", 0.62, 0.62, 0);
        if (_st.alloy_amt > 0) {
            draw_text_transformed(_dos_x + 16, _cost_y + 44, "• Materials: " + string(_st.alloy_amt) + "x " + _st.alloy_id, 0.62, 0.62, 0);
        }

        // Action Button: COMMENCE RESEARCH / RESEARCHED / IN PROGRESS / ABANDONED
        var _btn_x = _dos_x + 16;
        var _btn_y = _dos_y + _dos_h - 44;
        var _btn_w = _dos_w - 32;
        var _btn_h = 34;
        var _b_hov = (_mx >= _btn_x && _mx <= _btn_x + _btn_w && _my >= _btn_y && _my <= _btn_y + _btn_h);

        var _is_res_done = scr_research_is_unlocked(_st.id);
        var _is_res_aban = scr_research_is_abandoned(_st.id);
        var _slot_in_prog = scr_research_is_in_progress(_st.id);
        var _can_commence = scr_research_can_research(_st.id);

        if (_is_res_done) {
            draw_set_color(make_color_rgb(30, 60, 40));
            draw_rectangle(_btn_x, _btn_y, _btn_x + _btn_w, _btn_y + _btn_h, false);
            draw_set_color(make_color_rgb(60, 220, 100));
            draw_rectangle(_btn_x, _btn_y, _btn_x + _btn_w, _btn_y + _btn_h, true);
            draw_set_color(make_color_rgb(60, 240, 100));
            draw_text(_btn_x + 36, _btn_y + 8, "RESEARCH COMPLETED ✓");
        } else if (_is_res_aban) {
            draw_set_color(make_color_rgb(45, 18, 22));
            draw_rectangle(_btn_x, _btn_y, _btn_x + _btn_w, _btn_y + _btn_h, false);
            draw_set_color(make_color_rgb(200, 60, 60));
            draw_rectangle(_btn_x, _btn_y, _btn_x + _btn_w, _btn_y + _btn_h, true);
            draw_set_color(make_color_rgb(255, 90, 90));
            draw_text(_btn_x + 14, _btn_y + 8, "DOCTRINE ABANDONED // RIVAL PATH");
        } else if (_slot_in_prog != -1) {
            draw_set_color(make_color_rgb(60, 50, 20));
            draw_rectangle(_btn_x, _btn_y, _btn_x + _btn_w, _btn_y + _btn_h, false);
            draw_set_color(make_color_rgb(255, 180, 50));
            draw_rectangle(_btn_x, _btn_y, _btn_x + _btn_w, _btn_y + _btn_h, true);
            draw_set_color(make_color_rgb(255, 215, 60));
            draw_text(_btn_x + 28, _btn_y + 8, "RESEARCH IN PROGRESS...");
        } else if (_can_commence) {
            // Find first empty slot
            var _first_empty_slot = -1;
            for (var s = 0; s < array_length(_sys.slots); s++) {
                if (_sys.slots[s].status == "EMPTY") {
                    _first_empty_slot = s;
                    break;
                }
            }

            if (_first_empty_slot != -1) {
                if (_b_hov && _click) {
                    scr_research_start(_st.id, _first_empty_slot);
                }
                draw_set_color(_b_hov ? make_color_rgb(0, 140, 255) : make_color_rgb(0, 90, 180));
                draw_rectangle(_btn_x, _btn_y, _btn_x + _btn_w, _btn_y + _btn_h, false);
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_rectangle(_btn_x, _btn_y, _btn_x + _btn_w, _btn_y + _btn_h, true);
                draw_set_color(c_white);
                draw_text(_btn_x + 32, _btn_y + 8, "COMMENCE RESEARCH >>");
            } else {
                draw_set_color(make_color_rgb(40, 30, 30));
                draw_rectangle(_btn_x, _btn_y, _btn_x + _btn_w, _btn_y + _btn_h, false);
                draw_set_color(make_color_rgb(180, 80, 80));
                draw_rectangle(_btn_x, _btn_y, _btn_x + _btn_w, _btn_y + _btn_h, true);
                draw_set_color(make_color_rgb(255, 140, 140));
                draw_text(_btn_x + 14, _btn_y + 8, "ALL RESEARCH SLOTS FULL!");
            }
        } else {
            draw_set_color(make_color_rgb(24, 28, 36));
            draw_rectangle(_btn_x, _btn_y, _btn_x + _btn_w, _btn_y + _btn_h, false);
            draw_set_color(make_color_rgb(60, 75, 95));
            draw_rectangle(_btn_x, _btn_y, _btn_x + _btn_w, _btn_y + _btn_h, true);
            draw_set_color(make_color_rgb(120, 140, 165));
            draw_text(_btn_x + 32, _btn_y + 8, "PREREQUISITES LOCKED");
        }
    }
}
