/// @description obj_BlueprintManager Create Event
// Core Global Blueprint Registry Singleton: Loads & stores JSON data for mechs and components
// Includes alloy synthesis formulas (doc 02) and prototyped masterworks (doc 03)

// 1. Enforce Persistent Singleton Pattern
if (instance_number(obj_BlueprintManager) > 1) {
    show_debug_message("[obj_BlueprintManager] Duplicate singleton detected. Destroying instance (ID: " + string(id) + ")");
    instance_destroy();
    exit;
}

persistent = true;
show_debug_message("[obj_BlueprintManager] Initializing Persistent Blueprint Manager Singleton...");

// 2. Blueprint & Component Registries
unlocked_blueprints = {};  // Keyed by blueprint_id or model_code -> blueprint struct
unlocked_components = {};  // Keyed by component_id -> component struct
all_blueprint_list = [];   // Linear array containing all canonical & player blueprints for UI iteration

// 3. Alloy Chemistry Recipe Formulas (docs/02_alloy_chemistry.md)
unlocked_recipes = {
    alloy_vanguard_comp: {
        id: "alloy_vanguard_comp",
        name: "Vanguard Composite Armor Plating",
        tier: 1,
        inputs: { mat_tungsten: 2, mat_silica_carb: 1 },
        temp_min_c: 2200,
        temp_max_c: 2500,
        pressure_max_psi: 1000,
        cook_time_sec: 5.0,
        unlocked: true,
        description: "Basic military composite offering balanced kinetic and ballistic protection."
    },
    alloy_hyperion_matrix: {
        id: "alloy_hyperion_matrix",
        name: "Hyperion Core Superconductor Matrix",
        tier: 2,
        inputs: { mat_tungsten: 1, mat_tritium: 2, mat_syn_flux: 1 },
        temp_target_c: 4500,
        temp_tolerance_c: 150,
        pressure_min_psi: 8000,
        volatility_rate: 0.15,
        cook_time_sec: 5.0,
        unlocked: false,
        description: "Plasma-stabilized superconducting grid required for heavy fusion cores. High volatility."
    }
};

// 4. Prototyped Masterwork Inventory (docs/03_prototyping_minigames.md)
masterwork_inventory = [];

add_masterwork = function(_mw_struct) {
    array_push(masterwork_inventory, _mw_struct);
    show_debug_message("[obj_BlueprintManager] Added Masterwork: " + string(_mw_struct[$ "name"] ?? "Component"));
};

// 5. Methods for Registry and File Loading
load_blueprint = function(_file_name) {
    var _bp = scr_load_blueprint(_file_name);
    if (!is_undefined(_bp) && is_struct(_bp)) {
        var _id = _bp[$ "blueprint_id"];
        if (is_string(_id) && _id != "") {
            unlocked_blueprints[$ _id] = _bp;
            show_debug_message("[obj_BlueprintManager] Registered blueprint: " + _id + " (" + string(_bp[$ "name"] ?? "") + ")");
            return _bp;
        } else {
            show_debug_message("[obj_BlueprintManager] WARNING: Blueprint in " + string(_file_name) + " missing 'blueprint_id'");
        }
    } else {
        show_debug_message("[obj_BlueprintManager] Failed to parse blueprint file: " + string(_file_name));
    }
    return undefined;
};

get_blueprint = function(_blueprint_id) {
    if (variable_struct_exists(unlocked_blueprints, _blueprint_id)) {
        return unlocked_blueprints[$ _blueprint_id];
    }
    return undefined;
};

is_blueprint_unlocked = function(_blueprint_id) {
    return variable_struct_exists(unlocked_blueprints, _blueprint_id);
};

get_all_blueprints = function() {
    return all_blueprint_list;
};

get_blueprints_by_faction = function(_fid) {
    if (_fid == "all" || _fid == "") return all_blueprint_list;
    var _filtered = [];
    for (var i = 0; i < array_length(all_blueprint_list); i++) {
        var _bp = all_blueprint_list[i];
        if (variable_struct_exists(_bp, "faction_id") && _bp.faction_id == _fid) {
            array_push(_filtered, _bp);
        } else if (_fid == "player" && (string_pos("player", _bp.blueprint_id) > 0 || string_pos("Player", _bp[$ "class"] ?? "") > 0)) {
            array_push(_filtered, _bp);
        }
    }
    return _filtered;
};

get_blueprint_count = function() {
    return array_length(all_blueprint_list);
};

register_custom_blueprint = function(_blueprint_struct) {
    if (!is_struct(_blueprint_struct)) return false;
    var _id = _blueprint_struct.id;
    unlocked_blueprints[$ _id] = _blueprint_struct;
    if (variable_struct_exists(_blueprint_struct, "model_code")) {
        unlocked_blueprints[$ _blueprint_struct.model_code] = _blueprint_struct;
    }
    var _found = false;
    for (var i = 0; i < array_length(all_blueprint_list); i++) {
        if (all_blueprint_list[i].id == _id) {
            all_blueprint_list[i] = _blueprint_struct;
            _found = true;
            break;
        }
    }
    if (!_found) {
        array_push(all_blueprint_list, _blueprint_struct);
    }
    show_debug_message("[obj_BlueprintManager] Registered custom blueprint: " + _id);
    return true;
};

register_component = function(_comp_id, _comp_struct) {
    if (is_string(_comp_id) && _comp_id != "" && is_struct(_comp_struct)) {
        unlocked_components[$ _comp_id] = _comp_struct;
        return true;
    }
    return false;
};

get_component = function(_comp_id) {
    if (variable_struct_exists(unlocked_components, _comp_id)) {
        return unlocked_components[$ _comp_id];
    }
    return undefined;
};

// 6. Preload Starter Blueprint (GHA-07 Ironclad)
var _ironclad = load_blueprint("bp_ms_ironclad_07.json");
if (!is_undefined(_ironclad)) {
    _ironclad.id = "bp_ms_ironclad_07";
    _ironclad.model_code = "GHA-07";
    _ironclad.faction_id = "faction_terran";
    _ironclad.associated_sprite = spr_ms_ironclad_idle;
    _ironclad.schematic_sprite = spr_mech_schematic;
    _ironclad.tier = 2;
    _ironclad.armor_rating = 850;
    _ironclad.structure_hp = 2480;
    _ironclad.power_output_mw = 280;
    _ironclad.heat_dispersion_rate = 35.0;
    _ironclad.walk_speed_kph = 42.0;
    _ironclad.boost_speed_kph = 78.0;
    _ironclad.height_meters = 18.2;
    _ironclad.empty_weight_tonnes = 58.0;
    _ironclad.combat_weight_tonnes = 94.5;
    _ironclad.reactor_type = "Hyperion Class-IV Magnetic Tokamak";
    _ironclad.metal_type = "High-Density Tungsten-Carbide Ceramite Composite";
    _ironclad.alloy_cost = { tungsten: 50, silica: 20, slag: 10, flux: 10, tritium: 5 };
    _ironclad.armament = ["Type-77 120mm Solid-Slug Autocannon", "GAU-88 Heavy Vulcan Rotary", "Swarm-16 Heavy Micro-Missile Pod"];
    _ironclad.variants = ["GHA-07 Block I Prototype", "GHA-07 Block II Standard Linebreaker", "GHA-07E Heavy Trench Refit", "GHA-07S Jovian Siege Pack"];
    _ironclad.manufacturing_lore = "Engineered by Vanguard Defense Systems to resolve the Orbital Beachhead Crisis. Sacrifices flight agility for impenetrable composite plating and heavy kinetic saturation.";
    _ironclad.battlefield_reputation = "Nicknamed 'The Walking Vault' - shrugs off solid slug fire and pulverizes enemy trench lines.";

    unlocked_blueprints[$ "bp_ms_ironclad_07"] = _ironclad;
    unlocked_blueprints[$ "GHA-07"] = _ironclad;
    array_push(all_blueprint_list, _ironclad);
    show_debug_message("[obj_BlueprintManager] GHA-07 Ironclad preloaded into registry & list.");
}

// 7. Register Player Proprietary Replacement Doctrines (docs/12)
var _bp_player_1 = {
    id: "bp_player_vanguard_aegis",
    blueprint_id: "bp_player_vanguard_aegis",
    model_code: "PMC-AEGIS",
    name: "Vanguard Aegis-MK1",
    faction_id: "player",
    class: "Heavy Assault Mass Production",
    role: "Frontline Linebreaker & Heavy Plating",
    tier: 2,
    armor_rating: 880,
    structure_hp: 2400,
    power_output_mw: 1450,
    heat_dispersion_rate: 32.0,
    walk_speed_kph: 44.0,
    boost_speed_kph: 80.0,
    height_meters: 18.5,
    empty_weight_tonnes: 60.0,
    combat_weight_tonnes: 96.0,
    reactor_type: "Hyperion-V Shielded Tokamak Core",
    metal_type: "Tungsten-Ceramic Multi-Laminate Matrix",
    alloy_cost: { tungsten: 35, silica: 15, flux: 10, slag: 5 },
    armament: ["Twin 120mm Rotary Vulcans", "Aegis Reactive Shield", "Kevlar-Reinforced Pincer"],
    variants: ["Aegis Standard", "Aegis Trench Shield", "Aegis Commander Pack"],
    associated_sprite: spr_ms_ironclad_idle,
    schematic_sprite: spr_mech_schematic,
    fabrication_cost_cr: 395000,
    manufacturing_lore: "Proprietary player heavy assault chassis designed with reinforced composite plating and dual rotary vulcan cannons.",
    battlefield_reputation: "Directly replaces Terran Coalition Ironclad doctrine across contract theaters."
};

var _bp_player_2 = {
    id: "bp_player_valkyrie_ace",
    blueprint_id: "bp_player_valkyrie_ace",
    model_code: "PMC-VALK",
    name: "Valkyrie Void-Striker",
    faction_id: "player",
    class: "High Mobility Space Interceptor",
    role: "Orbital Superiority & Plasma Skirmisher",
    tier: 2,
    armor_rating: 640,
    structure_hp: 1750,
    power_output_mw: 1850,
    heat_dispersion_rate: 45.0,
    walk_speed_kph: 52.0,
    boost_speed_kph: 120.0,
    height_meters: 17.0,
    empty_weight_tonnes: 42.0,
    combat_weight_tonnes: 68.0,
    reactor_type: "Cryo-Tritium Superconducting Vector Core",
    metal_type: "Aerosteel-Flux Ultra-Light Alloy",
    alloy_cost: { tritium: 25, flux: 20, silica: 15, tungsten: 10 },
    armament: ["Twin Particle Pulse Rifles", "Micro-Vernier Cluster", "Hyperion Beam Saber"],
    variants: ["Void-Striker High-Mobility", "EW Electronic Jammer", "Long-Range Beam Sniper"],
    associated_sprite: spr_ms_aether_idle,
    schematic_sprite: spr_mech_schematic,
    fabrication_cost_cr: 440000,
    manufacturing_lore: "High-agility orbital fighter frame utilizing vector vernier thrusters and twin particle pulse rifles.",
    battlefield_reputation: "Directly replaces Outer Colonies Aether doctrine in contested space sectors."
};

var _bp_player_3 = {
    id: "bp_player_chimera_modular",
    blueprint_id: "bp_player_chimera_modular",
    model_code: "PMC-CHIM",
    name: "Chimera Modular Raider",
    faction_id: "player",
    class: "Omnipurpose Skirmish Chassis",
    role: "Scavenger Guerrilla & Black Market Linebreaker",
    tier: 2,
    armor_rating: 720,
    structure_hp: 2100,
    power_output_mw: 1350,
    heat_dispersion_rate: 28.0,
    walk_speed_kph: 48.0,
    boost_speed_kph: 92.0,
    height_meters: 17.8,
    empty_weight_tonnes: 50.0,
    combat_weight_tonnes: 78.0,
    reactor_type: "Overclocked Syndicate Fission-Turbine",
    metal_type: "Reinforced Slag-Composite Armor",
    alloy_cost: { tungsten: 25, silica: 20, slag: 20, flux: 10 },
    armament: ["Scrap-Flak Heavy Cannon", "Pneumatic Harpoon Gun", "Smokescreen Ejectors"],
    variants: ["Modular Raider Alpha", "Scavenger Salvage Arm", "Demolition Flak Rig"],
    associated_sprite: spr_ms_hyena_idle,
    schematic_sprite: spr_mech_schematic,
    fabrication_cost_cr: 325000,
    manufacturing_lore: "Cost-effective modular chassis engineered with high-impact kinetic flak arrays and fast-swap armor.",
    battlefield_reputation: "Directly replaces Obsidian Syndicate Hyena doctrine in asteroid raids."
};

var _bp_player_4 = {
    id: "bp_player_muramasa_spec_x",
    blueprint_id: "bp_player_muramasa_spec_x",
    model_code: "PMC-KUSA",
    name: "Kusanagi Cyber-Assault",
    faction_id: "player",
    class: "Neural-Linked Precision Warform",
    role: "Cybernetic Ace & High-Frequency Infiltration",
    tier: 3,
    armor_rating: 780,
    structure_hp: 1950,
    power_output_mw: 2200,
    heat_dispersion_rate: 52.0,
    walk_speed_kph: 56.0,
    boost_speed_kph: 110.0,
    height_meters: 17.5,
    empty_weight_tonnes: 45.0,
    combat_weight_tonnes: 72.0,
    reactor_type: "Sub-Nanometer Quantum Tokamak",
    metal_type: "Adamantine Carbide Superconductor Weave",
    alloy_cost: { tritium: 35, flux: 30, tungsten: 15, silica: 10 },
    armament: ["High-Frequency Nanoblade", "Linear Accelerator Rifle", "Active Optical Cloak"],
    variants: ["Kusanagi Prototype", "Cyber-Ghost Infiltration", "Dual Monomolecular Edge"],
    associated_sprite: spr_ms_muramasa_idle,
    schematic_sprite: spr_mech_schematic,
    fabrication_cost_cr: 485000,
    manufacturing_lore: "Experimental cyber-neural chassis forged with superconductor matrices and monomolecular beam blades.",
    battlefield_reputation: "Directly replaces Apex Zaibatsu Muramasa doctrine in black-ops sectors."
};

var _p_docs = [_bp_player_1, _bp_player_2, _bp_player_3, _bp_player_4];
for (var p = 0; p < array_length(_p_docs); p++) {
    var _p_doc = _p_docs[p];
    unlocked_blueprints[$ _p_doc.id] = _p_doc;
    unlocked_blueprints[$ _p_doc.model_code] = _p_doc;
    array_push(all_blueprint_list, _p_doc);
}
show_debug_message("[obj_BlueprintManager] Registered 4 Player Mass-Production Doctrines into registry & list.");

// 8. Load & Register Canonical Faction Mobile Suit Blueprints from Timeline JSON
if (file_exists("mobile_suits_timeline.json")) {
    try {
        var _f_bp = file_text_open_read("mobile_suits_timeline.json");
        var _json_bp = "";
        while (!file_text_eof(_f_bp)) {
            _json_bp += file_text_readln(_f_bp);
        }
        file_text_close(_f_bp);
        var _timeline_bp = json_parse(_json_bp);
        if (variable_struct_exists(_timeline_bp, "mobile_suits")) {
            var _ms_arr = _timeline_bp.mobile_suits;
            for (var i = 0; i < array_length(_ms_arr); i++) {
                var _suit = _ms_arr[i];
                var _bid = _suit.id;

                var _spr_asset = spr_ms_ironclad_idle;
                if (_suit.faction_id == "faction_colony") _spr_asset = spr_ms_aether_idle;
                else if (_suit.faction_id == "faction_syndicate") _spr_asset = spr_ms_hyena_idle;
                else if (_suit.faction_id == "faction_zaibatsu") _spr_asset = spr_ms_muramasa_idle;
                else if (string_pos("Siege", _suit.role) > 0 || string_pos("Artillery", _suit.role) > 0) _spr_asset = spr_ms_siegebreaker_fire;

                _suit.associated_sprite = _spr_asset;
                _suit.schematic_sprite = spr_mech_schematic;
                _suit.blueprint_id = _bid;

                unlocked_blueprints[$ _bid] = _suit;
                if (variable_struct_exists(_suit, "model_code")) {
                    unlocked_blueprints[$ _suit.model_code] = _suit;
                }
                array_push(all_blueprint_list, _suit);
            }
            show_debug_message("[obj_BlueprintManager] Loaded " + string(array_length(_ms_arr)) + " canonical mobile suit blueprints into registry.");
        }
    } catch (_ex_bp) {
        show_debug_message("[obj_BlueprintManager] Warning loading timeline blueprints: " + string(_ex_bp));
    }
}

// 8b. Load & Index All 20 Canonical Blueprint JSONs from datafiles/blueprints/
var _canonical_files = [
    "bp_ms_ironclad_07.json", "bp_ms_bulwark_03.json", "bp_ms_siegebreaker_07b.json", "bp_ms_behemoth_11.json",
    "bp_ms_aether_09.json", "bp_ms_sylph_04.json", "bp_ms_helios_07.json", "bp_ms_seraphim_15.json",
    "bp_ms_hyena_12.json", "bp_ms_marauder_05.json", "bp_ms_slag_lobber_14.json", "bp_ms_chimera_19.json",
    "bp_ms_muramasa_11.json", "bp_ms_ronin_06.json", "bp_ms_raiden_15.json", "bp_ms_susanoo_22.json",
    "bp_player_vanguard_heavy.json", "bp_player_stratos_interceptor.json", "bp_player_scrapper_brawler.json", "bp_player_ghost_sniper.json"
];
for (var b = 0; b < array_length(_canonical_files); b++) {
    var _fname = _canonical_files[b];
    var _loaded_bp = load_blueprint(_fname);
    if (!is_undefined(_loaded_bp)) {
        var _bid = _loaded_bp.blueprint_id;
        var _spr = spr_ms_ironclad_idle;
        if (string_pos("aether", _bid) > 0 || string_pos("sylph", _bid) > 0 || string_pos("helios", _bid) > 0 || string_pos("seraphim", _bid) > 0 || string_pos("stratos", _bid) > 0) _spr = spr_ms_aether_idle;
        else if (string_pos("hyena", _bid) > 0 || string_pos("marauder", _bid) > 0 || string_pos("slag", _bid) > 0 || string_pos("chimera", _bid) > 0 || string_pos("scrapper", _bid) > 0) _spr = spr_ms_hyena_idle;
        else if (string_pos("muramasa", _bid) > 0 || string_pos("ronin", _bid) > 0 || string_pos("raiden", _bid) > 0 || string_pos("susanoo", _bid) > 0 || string_pos("ghost", _bid) > 0) _spr = spr_ms_muramasa_idle;
        else if (string_pos("siege", _bid) > 0) _spr = spr_ms_siegebreaker_fire;
        
        _loaded_bp.associated_sprite = _spr;
        _loaded_bp.schematic_sprite = spr_mech_schematic;
        
        unlocked_blueprints[$ _bid] = _loaded_bp;
        if (variable_struct_exists(_loaded_bp, "model_code")) {
            unlocked_blueprints[$ _loaded_bp.model_code] = _loaded_bp;
        }
        array_push(all_blueprint_list, _loaded_bp);
    }
}
show_debug_message("[obj_BlueprintManager] Loaded all 20 canonical blueprint JSONs from datafiles/blueprints/ into registry.");

show_debug_message("[obj_BlueprintManager] Total Blueprints Active: " + string(array_length(all_blueprint_list)) + ". Ready for Prototyping & Assembly.");

// 9. Pre-populate Discovered Alloy Codex with Canonical Standards (docs/02 & 14)
discovered_alloy_codex = [
    {
        name: "Vanguard Composite Armor Plating",
        code: "AL-W74-C6-MK1",
        tier: 1,
        armor_hp: 850,
        thermal_rate: 35.0,
        density_g_cm3: 13.5,
        superconductivity: 0.1,
        radar_absorb_pct: 0.15,
        is_failure: false,
        failure_reason: "",
        color: make_color_rgb(115, 135, 160),
        hex: "#7387A0",
        formula_summary: "2x Tungsten + 1x Silica-Carbon",
        raw_inputs: { mat_tungsten: 2, mat_silica_carb: 1 }
    },
    {
        name: "Hyperion Core Superconductor Matrix",
        code: "AL-H1-W74-MK2",
        tier: 2,
        armor_hp: 580,
        thermal_rate: 65.0,
        density_g_cm3: 6.2,
        superconductivity: 1.8,
        radar_absorb_pct: 0.05,
        is_failure: false,
        failure_reason: "",
        color: make_color_rgb(60, 230, 255),
        hex: "#3CE6FF",
        formula_summary: "1x Tungsten + 2x Tritium + 1x Flux",
        raw_inputs: { mat_tungsten: 1, mat_tritium: 2, mat_syn_flux: 1 }
    },
    {
        name: "Aerosteel Vernier Flux",
        code: "AL-TI22-H1-MK2",
        tier: 2,
        armor_hp: 620,
        thermal_rate: 55.0,
        density_g_cm3: 3.8,
        superconductivity: 1.2,
        radar_absorb_pct: 0.20,
        is_failure: false,
        failure_reason: "",
        color: make_color_rgb(195, 150, 255),
        hex: "#C396FF",
        formula_summary: "2x Flux + 1x Tritium + 1x Silica",
        raw_inputs: { mat_syn_flux: 2, mat_tritium: 1, mat_silica_carb: 1 }
    },
    {
        name: "Adamantine Carbide Plating",
        code: "AL-W74-C6-OS76-MK3",
        tier: 3,
        armor_hp: 1150,
        thermal_rate: 42.0,
        density_g_cm3: 16.8,
        superconductivity: 0.3,
        radar_absorb_pct: 0.10,
        is_failure: false,
        failure_reason: "",
        color: make_color_rgb(255, 155, 60),
        hex: "#FF9B3C",
        formula_summary: "3x Tungsten + 2x Silica + 1x Flux",
        raw_inputs: { mat_tungsten: 3, mat_silica_carb: 2, mat_syn_flux: 1 }
    }
];

show_debug_message("[obj_BlueprintManager] Initialized Discovered Alloy Codex with " + string(array_length(discovered_alloy_codex)) + " canonical masterworks.");

// =========================================================================
// 8. R&D Prototype Tuning Profiles & Comprehensive Combat Stats (Doc 20)
// =========================================================================
active_prototype_tuning = {
    reactor: {
        score: 0.0,
        grade: "UNTESTED",
        output_mult: 1.0,
        heat_diss_mult: 1.0,
        energy_dmg_mult: 1.0,
        en_cap_mult: 1.0
    },
    hydraulics: {
        score: 0.0,
        grade: "UNTESTED",
        pilot_limit_pct: 115,
        recoil_mult: 1.0,
        ap_bonus: 0,
        leg_armor_mult: 1.0
    },
    thrusters: {
        score: 0.0,
        grade: "UNTESTED",
        thrust_mult: 1.0,
        evasion_bonus: 0,
        space_terrain: "B",
        fuel_eff_mult: 1.0
    }
};

get_comprehensive_stats = function(_bp) {
    if (is_undefined(_bp) || !is_struct(_bp)) return undefined;

    var _code = string(_bp[$ "model_code"] ?? (_bp[$ "blueprint_id"] ?? "PMC-01"));
    var _tier = _bp[$ "tier"] ?? 2;
    var _fac = _bp[$ "faction_id"] ?? "player";

    // Gihren's Greed Pilot Limit % (Genkai) Baseline
    var _limit = 115;
    if (string_pos("susanoo", string_lower(_code)) > 0) _limit = 210;
    else if (string_pos("raiden", string_lower(_code)) > 0) _limit = 185;
    else if (string_pos("seraphim", string_lower(_code)) > 0) _limit = 180;
    else if (string_pos("muramasa", string_lower(_code)) > 0) _limit = 170;
    else if (string_pos("aether", string_lower(_code)) > 0) _limit = 155;
    else if (string_pos("ronin", string_lower(_code)) > 0) _limit = 160;
    else if (string_pos("ghost", string_lower(_code)) > 0) _limit = 160;
    else if (string_pos("stratos", string_lower(_code)) > 0) _limit = 155;
    else if (string_pos("sylph", string_lower(_code)) > 0) _limit = 150;
    else if (string_pos("helios", string_lower(_code)) > 0) _limit = 155;
    else if (string_pos("chimera", string_lower(_code)) > 0) _limit = 140;
    else if (string_pos("marauder", string_lower(_code)) > 0) _limit = 130;
    else if (string_pos("vanguard", string_lower(_code)) > 0) _limit = 135;
    else if (string_pos("hyena", string_lower(_code)) > 0) _limit = 125;
    else if (string_pos("scrapper", string_lower(_code)) > 0) _limit = 130;
    else if (string_pos("siegebreaker", string_lower(_code)) > 0) _limit = 120;
    else if (string_pos("ironclad", string_lower(_code)) > 0) _limit = 115;
    else if (string_pos("behemoth", string_lower(_code)) > 0) _limit = 110;
    else if (string_pos("slag", string_lower(_code)) > 0) _limit = 110;
    else if (string_pos("bulwark", string_lower(_code)) > 0) _limit = 105;

    // Propellant Max (EN)
    var _prop = 120 + (_tier * 20);
    if (string_pos("behemoth", string_lower(_code)) > 0) _prop = 200;
    else if (string_pos("susanoo", string_lower(_code)) > 0) _prop = 190;
    else if (string_pos("seraphim", string_lower(_code)) > 0) _prop = 170;

    // Terrain Adaptability (Ground, Space, Urban, Trench)
    var _ter = { ground: "A", space: "B", urban: "A", trench: "C" };
    if (_fac == "faction_colony") {
        _ter = { ground: "B", space: "S", urban: "B", trench: "B" };
    } else if (_fac == "faction_zaibatsu") {
        _ter = { ground: "A", space: "S", urban: "S", trench: "C" };
    } else if (_fac == "faction_syndicate") {
        _ter = { ground: "A", space: "A", urban: "S", trench: "B" };
    }
    if (string_pos("susanoo", string_lower(_code)) > 0) _ter = { ground: "S", space: "S", urban: "S", trench: "A" };

    // Minovsky / ECM Particle Dispersion %
    var _ecm = 25;
    if (_fac == "faction_zaibatsu") _ecm = 55 + (_tier * 5);
    else if (_fac == "faction_colony") _ecm = 45 + (_tier * 5);
    else if (_fac == "faction_syndicate") _ecm = 35 + (_tier * 3);
    else _ecm = 25 + (_tier * 3);
    _ecm = clamp(_ecm, 15, 75);

    // Sensor Search Grade
    var _search = "B";
    if (_ecm >= 55) _search = "S";
    else if (_ecm >= 40) _search = "A";
    else if (_ecm >= 25) _search = "B";
    else _search = "C";

    // Power & Weight Dynamics
    var _tot = _bp[$ "totals_and_specs"] ?? {};
    var _w = _tot[$ "total_weight_tonnes"] ?? 75.0;
    var _p_out = _tot[$ "total_power_output_mw"] ?? 250.0;
    var _p_drain = _tot[$ "total_power_drain_mw"] ?? 120.0;
    var _surplus = _p_out - _p_drain;
    var _pw_ratio = round((_p_out / max(1.0, _w)) * 10.0) / 10.0;
    var _armor = _tot[$ "total_armor_hp"] ?? 2000;
    var _recoil = _tot[$ "recoil_absorption_pct"] ?? 0.50;

    return {
        pilot_limit_pct: _limit,
        propellant_max: _prop,
        propellant_cur: _prop,
        terrain: _ter,
        ecm_dispersion_pct: _ecm,
        sensor_search_grade: _search,
        total_weight_tonnes: _w,
        total_power_output_mw: _p_out,
        total_power_drain_mw: _p_drain,
        net_power_surplus_mw: _surplus,
        power_weight_ratio: _pw_ratio,
        total_armor_hp: _armor,
        recoil_absorption_pct: _recoil
    };
};

apply_tuning_to_custom_mech = function(_custom_mech) {
    if (is_undefined(_custom_mech) || !is_struct(_custom_mech)) return _custom_mech;

    var _r = active_prototype_tuning.reactor;
    var _h = active_prototype_tuning.hydraulics;
    var _t = active_prototype_tuning.thrusters;

    // Apply Reactor Tuning
    if (_r.grade != "UNTESTED") {
        _custom_mech.power_output = floor(_custom_mech.power_output * _r.output_mult);
        _custom_mech[$ "heat_dissipation"] = floor(35.0 * _r.heat_diss_mult);
    }

    // Apply Hydraulic Tuning (Pilot Limit Genkai)
    if (_h.grade != "UNTESTED") {
        _custom_mech[$ "pilot_limit_pct"] = _h.pilot_limit_pct;
        _custom_mech[$ "recoil_absorption_pct"] = clamp(0.50 * _h.recoil_mult, 0.20, 0.95);
        _custom_mech[$ "armor_rating"] = floor(_custom_mech.armor_rating * _h.leg_armor_mult);
    } else {
        _custom_mech[$ "pilot_limit_pct"] = 125;
        _custom_mech[$ "recoil_absorption_pct"] = 0.50;
    }

    // Apply Thruster Calibration
    if (_t.grade != "UNTESTED") {
        _custom_mech.speed = max(1, floor(_custom_mech.speed * _t.thrust_mult));
        _custom_mech[$ "evasion_bonus"] = _t.evasion_bonus;
        _custom_mech[$ "propellant_max"] = floor(150 * _t.fuel_eff_mult);
        _custom_mech[$ "propellant_cur"] = _custom_mech.propellant_max;
    } else {
        _custom_mech[$ "evasion_bonus"] = 0;
        _custom_mech[$ "propellant_max"] = 140;
        _custom_mech[$ "propellant_cur"] = 140;
    }

    _custom_mech[$ "terrain"] = { ground: "A", space: (_t.space_terrain != "" ? _t.space_terrain : "A"), urban: "A", trench: "B" };
    _custom_mech[$ "ecm_dispersion_pct"] = 35;
    _custom_mech[$ "sensor_search_grade"] = "A";
    _custom_mech[$ "tuning_grades"] = {
        reactor: _r.grade,
        hydraulics: _h.grade,
        thrusters: _t.grade
    };

    if (_r.grade == "S" || _h.grade == "S" || _t.grade == "S") {
        _custom_mech.name += " [Ace Prototype Spec-X]";
        _custom_mech.callsign += " [Ace Spec-X]";
    } else if (_r.grade == "A" || _h.grade == "A" || _t.grade == "A") {
        _custom_mech.name += " [Masterwork Spec]";
        _custom_mech.callsign += " [Masterwork]";
    }

    return _custom_mech;
};
