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
unlocked_blueprints = {};  // Keyed by blueprint_id -> blueprint struct
unlocked_components = {};  // Keyed by component_id -> component struct

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

// 6. Preload Starter Blueprints
var _ironclad = load_blueprint("bp_ms_ironclad_07.json");
if (!is_undefined(_ironclad)) {
    show_debug_message("[obj_BlueprintManager] GHA-07 Ironclad preloaded successfully into blueprint registry.");
}

// 7. Register Player Proprietary Replacement Doctrines (docs/12)
unlocked_blueprints[$ "bp_player_vanguard_aegis"] = {
    blueprint_id: "bp_player_vanguard_aegis",
    name: "Vanguard Aegis-MK1",
    class: "Heavy Assault Mass Production",
    role: "Frontline Linebreaker & Heavy Plating",
    tier: 2,
    base_armor: 880,
    base_power: 24,
    base_speed: 46,
    fabrication_cost_cr: 395000,
    description: "Proprietary player heavy assault chassis designed with reinforced composite plating and dual rotary vulcan cannons. Directly replaces Terran Coalition Ironclad doctrine."
};

unlocked_blueprints[$ "bp_player_valkyrie_ace"] = {
    blueprint_id: "bp_player_valkyrie_ace",
    name: "Valkyrie Void-Striker",
    class: "High Mobility Space Interceptor",
    role: "Orbital Superiority & Plasma Skirmisher",
    tier: 2,
    base_armor: 640,
    base_power: 32,
    base_speed: 94,
    fabrication_cost_cr: 440000,
    description: "High-agility orbital fighter frame utilizing vector vernier thrusters and twin particle pulse rifles. Tailored to replace Outer Colonies Aether doctrine."
};

unlocked_blueprints[$ "bp_player_chimera_modular"] = {
    blueprint_id: "bp_player_chimera_modular",
    name: "Chimera Modular Raider",
    class: "Omnipurpose Skirmish Chassis",
    role: "Scavenger Guerrilla & Black Market Linebreaker",
    tier: 2,
    base_armor: 720,
    base_power: 26,
    base_speed: 70,
    fabrication_cost_cr: 325000,
    description: "Cost-effective modular chassis engineered with high-impact kinetic flak arrays and fast-swap armor. Directly replaces Syndicate Hyena doctrine."
};

unlocked_blueprints[$ "bp_player_muramasa_spec_x"] = {
    blueprint_id: "bp_player_muramasa_spec_x",
    name: "Kusanagi Cyber-Assault",
    class: "Neural-Linked Precision Warform",
    role: "Cybernetic Ace & High-Frequency Infiltration",
    tier: 3,
    base_armor: 780,
    base_power: 36,
    base_speed: 86,
    fabrication_cost_cr: 485000,
    description: "Experimental cyber-neural chassis forged with superconductor matrices and monomolecular beam blades. Directly replaces Apex Zaibatsu Muramasa doctrine."
};

show_debug_message("[obj_BlueprintManager] Registered 4 Player Mass-Production Doctrines. Initialization Complete.");
