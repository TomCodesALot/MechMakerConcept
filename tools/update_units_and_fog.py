with open("scripts/scr_territory_war_system/scr_territory_war_system.gml", "r") as f:
    code = f.read()

# Replace scr_hex_get_stronghold_units with updated version including sensor_range and Scout unit
old_start = "function scr_hex_get_stronghold_units(_stronghold_id) {"
old_end = "    return _units;\n}\n\n/// @function scr_hex_get_reachable"

start_idx = code.find(old_start)
end_idx = code.find(old_end)

assert start_idx != -1, "scr_hex_get_stronghold_units not found"
assert end_idx != -1, "end of scr_hex_get_stronghold_units not found"

new_units_code = '''function scr_hex_get_stronghold_units(_stronghold_id) {
    var _units = [];
    var _layout = scr_stronghold_get_layout(_stronghold_id);
    var _opfor_fac = "faction_b";
    if (array_length(_layout.subnodes) > 0) {
        _opfor_fac = _layout.subnodes[0].controlling_faction;
    }
    if (_opfor_fac == "pmc") _opfor_fac = "faction_c";
    
    // --- 1. Player PMC Vanguard Strike Squadrons ---
    array_push(_units, {
        id: "pmc_vanguard_ironclad",
        name: "Ironclad Vanguard Alpha",
        unit_label: "GHA-07 Ironclad",
        faction: "pmc",
        sprite_name: "spr_mini_ms_ironclad",
        col: 2,
        row: 4,
        max_mp: 4,
        current_mp: 4,
        hp: 100,
        max_hp: 100,
        attack: 45,
        defense: 30,
        range: 1,
        sensor_range: 2,
        stack_count: 3,
        status: "READY"
    });
    
    array_push(_units, {
        id: "pmc_vanguard_striker",
        name: "Aero-Striker Ace Flight",
        unit_label: "F-102 Aero-Striker",
        faction: "pmc",
        sprite_name: "spr_mini_ms_aerostriker",
        col: 2,
        row: 6,
        max_mp: 5,
        current_mp: 5,
        hp: 80,
        max_hp: 80,
        attack: 40,
        defense: 20,
        range: 2,
        sensor_range: 3,
        stack_count: 3,
        status: "READY"
    });

    array_push(_units, {
        id: "pmc_vanguard_armor",
        name: "Heavy Armor Battalion",
        unit_label: "Mammoth Siege Tank",
        faction: "pmc",
        sprite_name: "spr_mini_veh_heavy_tank",
        col: 3,
        row: 3,
        max_mp: 3,
        current_mp: 3,
        hp: 120,
        max_hp: 120,
        attack: 50,
        defense: 35,
        range: 2,
        sensor_range: 2,
        stack_count: 5,
        status: "READY"
    });

    array_push(_units, {
        id: "pmc_vanguard_recon",
        name: "Vanguard Recon Technical",
        unit_label: "Armed Scout Technical",
        faction: "pmc",
        sprite_name: "spr_mini_veh_technical",
        col: 4,
        row: 5,
        max_mp: 5,
        current_mp: 5,
        hp: 60,
        max_hp: 60,
        attack: 30,
        defense: 16,
        range: 1,
        sensor_range: 4,
        stack_count: 6,
        status: "READY"
    });

    array_push(_units, {
        id: "pmc_vanguard_exo",
        name: "Combat Exo Engineers",
        unit_label: "Exo Squad Vanguard",
        faction: "pmc",
        sprite_name: "spr_mini_inf_exo_squad",
        col: 3,
        row: 7,
        max_mp: 2,
        current_mp: 2,
        hp: 65,
        max_hp: 65,
        attack: 32,
        defense: 18,
        range: 1,
        sensor_range: 1,
        stack_count: 8,
        status: "READY"
    });

    // --- 2. OPFOR Stronghold Defense Garrison ---
    array_push(_units, {
        id: "opfor_cmd_flagship",
        name: "OPFOR Command Flagship",
        unit_label: "Garrison Command MS",
        faction: _opfor_fac,
        sprite_name: "spr_mini_ms_commander",
        col: 12,
        row: 4,
        max_mp: 4,
        current_mp: 4,
        hp: 110,
        max_hp: 110,
        attack: 48,
        defense: 32,
        range: 2,
        sensor_range: 2,
        stack_count: 4,
        status: "READY"
    });

    array_push(_units, {
        id: "opfor_heavy_artillery",
        name: "Siege Battery MS Platoon",
        unit_label: "Long-Range Rail MS",
        faction: _opfor_fac,
        sprite_name: "spr_mini_ms_artillery",
        col: 13,
        row: 2,
        max_mp: 3,
        current_mp: 3,
        hp: 85,
        max_hp: 85,
        attack: 55,
        defense: 22,
        range: 3,
        sensor_range: 2,
        stack_count: 4,
        status: "READY"
    });

    array_push(_units, {
        id: "opfor_frontline_grunt",
        name: "Garrison Frontline MS",
        unit_label: "Standard Grunt MS",
        faction: _opfor_fac,
        sprite_name: "spr_mini_ms_grunt",
        col: 9,
        row: 3,
        max_mp: 4,
        current_mp: 4,
        hp: 90,
        max_hp: 90,
        attack: 42,
        defense: 25,
        range: 1,
        sensor_range: 2,
        stack_count: 4,
        status: "READY"
    });

    array_push(_units, {
        id: "opfor_defense_armor",
        name: "Redoubt Armor Division",
        unit_label: "Heavy Defense Armor",
        faction: _opfor_fac,
        sprite_name: "spr_mini_veh_heavy_tank",
        col: 11,
        row: 6,
        max_mp: 3,
        current_mp: 3,
        hp: 110,
        max_hp: 110,
        attack: 45,
        defense: 30,
        range: 1,
        sensor_range: 2,
        stack_count: 5,
        status: "READY"
    });

    array_push(_units, {
        id: "opfor_recon_rover",
        name: "Perimeter Recon Technicals",
        unit_label: "Armed Scout Technicals",
        faction: _opfor_fac,
        sprite_name: "spr_mini_veh_technical",
        col: 8,
        row: 7,
        max_mp: 4,
        current_mp: 4,
        hp: 70,
        max_hp: 70,
        attack: 35,
        defense: 18,
        range: 1,
        sensor_range: 3,
        stack_count: 6,
        status: "READY"
    });

    return _units;
}'''

code = code[:start_idx] + new_units_code + code[end_idx + len("    return _units;\n}\n"):]

# Append Fog of War functions at the end of the script
fog_functions = '''

// =========================================================================
// PROMETHEUS_FLUX PARTICLE FOG OF WAR & RADAR RECONNAISSANCE ENGINE
// 0 = UNEXPLORED (Blackout), 1 = FOG_OF_WAR (Previously Explored), 2 = VISIBLE (Illuminated)
// =========================================================================

/// @function scr_hex_init_fog_of_war()
/// @description Initializes a 16x10 fog of war visibility matrix
function scr_hex_init_fog_of_war() {
    var _fog = array_create(16);
    for (var c = 0; c < 16; c++) {
        _fog[c] = array_create(10, 0); // 0 = UNEXPLORED
    }
    return _fog;
}

/// @function scr_hex_update_fog_of_war(_fog_grid, _units_array, _terrain_grid)
/// @description Updates hex visibility based on friendly unit sensors and base radar
function scr_hex_update_fog_of_war(_fog_grid, _units_array, _terrain_grid) {
    if (is_undefined(_fog_grid)) return [];
    
    // 1. Demote currently VISIBLE (2) cells down to EXPLORED_FOG (1)
    for (var c = 0; c < 16; c++) {
        for (var r = 0; r < 10; r++) {
            if (_fog_grid[c][r] == 2) {
                _fog_grid[c][r] = 1;
            }
        }
    }
    
    // 2. Active Sensor Sweep from all Friendly PMC Units
    for (var i = 0; i < array_length(_units_array); i++) {
        var _u = _units_array[i];
        if (_u.faction == "pmc" && _u.hp > 0) {
            var _sr = variable_struct_exists(_u, "sensor_range") ? _u.sensor_range : 2;
            for (var c = 0; c < 16; c++) {
                for (var r = 0; r < 10; r++) {
                    if (scr_hex_distance(_u.col, _u.row, c, r) <= _sr) {
                        _fog_grid[c][r] = 2; // Actively illuminated
                    }
                }
            }
        }
    }
    
    // 3. Fixed Radar Perimeter from Friendly Base Facilities
    if (!is_undefined(_terrain_grid)) {
        for (var c = 0; c < 16; c++) {
            for (var r = 0; r < 10; r++) {
                if (_terrain_grid[c][r].terrain_type == "BASE_FACILITY" && _terrain_grid[c][r].controlling_faction == "pmc") {
                    for (var nc = 0; nc < 16; nc++) {
                        for (var nr = 0; nr < 10; nr++) {
                            if (scr_hex_distance(c, r, nc, nr) <= 2) {
                                _fog_grid[nc][nr] = 2;
                            }
                        }
                    }
                }
            }
        }
    }
    
    // 4. Detect Spotted Hostiles in Sensor Perimeter
    var _spotted = [];
    for (var i = 0; i < array_length(_units_array); i++) {
        var _eu = _units_array[i];
        if (_eu.faction != "pmc" && _eu.hp > 0) {
            if (_fog_grid[_eu.col][_eu.row] == 2) {
                array_push(_spotted, _eu.unit_label);
            }
        }
    }
    
    return _spotted;
}
'''

code += fog_functions

with open("scripts/scr_territory_war_system/scr_territory_war_system.gml", "w") as f:
    f.write(code)

print("Updated scr_territory_war_system.gml with Fog of War engine successfully!")
