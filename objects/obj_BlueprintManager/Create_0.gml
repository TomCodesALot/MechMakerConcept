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
    _ironclad.associated_sprite = spr_ms_ironclad_mp;
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
    associated_sprite: spr_ms_ironclad_mp,
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

                var _spr_asset = spr_ms_ironclad_mp;
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

show_debug_message("[obj_BlueprintManager] Total Blueprints Active: " + string(array_length(all_blueprint_list)) + ". Ready for Prototyping & Assembly.");
