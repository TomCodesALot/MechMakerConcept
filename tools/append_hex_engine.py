import sys

hex_code = """

// =========================================================================
// SHIN GIHREN'S GREED 16x10 HEX TACTICAL GRID ENGINE
// Tile-by-tile MP movement, terrain costs (river/mountain/plains), and turn cycles
// =========================================================================

/// @function scr_hex_get_screen_pos(_c, _r, _rad_x, _rad_y)
/// @description Returns screen position struct { x, y } for hex at column _c, row _r
function scr_hex_get_screen_pos(_c, _r, _rad_x, _rad_y) {
    var _start_x = _rad_x + 36;
    var _start_y = _rad_y + 42;
    var _col_dist = 42;
    var _row_dist = 48;
    var _odd_offset = 24;
    var _hx = _start_x + _c * _col_dist;
    var _hy = _start_y + _r * _row_dist + ((_c % 2 == 1) ? _odd_offset : 0);
    return { x: _hx, y: _hy };
}

/// @function scr_screen_to_hex(_mx, _my, _rad_x, _rad_y)
/// @description Returns hex coordinates struct { col, row } at mouse screen position
function scr_screen_to_hex(_mx, _my, _rad_x, _rad_y) {
    var _start_x = _rad_x + 36;
    var _start_y = _rad_y + 42;
    var _col_dist = 42;
    var _row_dist = 48;
    var _odd_offset = 24;
    
    var _approx_c = round((_mx - _start_x) / _col_dist);
    var _best_c = -1;
    var _best_r = -1;
    var _min_d = 999999;
    
    for (var _dc = -1; _dc <= 1; _dc++) {
        var _c = _approx_c + _dc;
        if (_c < 0 || _c >= 16) continue;
        var _y_base = _start_y + ((_c % 2 == 1) ? _odd_offset : 0);
        var _approx_r = round((_my - _y_base) / _row_dist);
        for (var _dr = -1; _dr <= 1; _dr++) {
            var _r = _approx_r + _dr;
            if (_r < 0 || _r >= 10) continue;
            var _pos = scr_hex_get_screen_pos(_c, _r, _rad_x, _rad_y);
            var _d = point_distance(_mx, _my, _pos.x, _pos.y);
            if (_d < _min_d) {
                _min_d = _d;
                _best_c = _c;
                _best_r = _r;
            }
        }
    }
    
    if (_min_d <= 28) {
        return { col: _best_c, row: _best_r };
    }
    return { col: -1, row: -1 };
}

/// @function scr_hex_get_neighbors(_c, _r)
/// @description Returns array of valid adjacent neighbor coordinate structs { col, row }
function scr_hex_get_neighbors(_c, _r) {
    var _res = [];
    var _raw = [];
    if (_c % 2 == 0) {
        _raw = [
            { col: _c, row: _r - 1 },
            { col: _c + 1, row: _r - 1 },
            { col: _c + 1, row: _r },
            { col: _c, row: _r + 1 },
            { col: _c - 1, row: _r },
            { col: _c - 1, row: _r - 1 }
        ];
    } else {
        _raw = [
            { col: _c, row: _r - 1 },
            { col: _c + 1, row: _r },
            { col: _c + 1, row: _r + 1 },
            { col: _c, row: _r + 1 },
            { col: _c - 1, row: _r + 1 },
            { col: _c - 1, row: _r }
        ];
    }
    for (var i = 0; i < array_length(_raw); i++) {
        var _nc = _raw[i].col;
        var _nr = _raw[i].row;
        if (_nc >= 0 && _nc < 16 && _nr >= 0 && _nr < 10) {
            array_push(_res, _raw[i]);
        }
    }
    return _res;
}

/// @function scr_hex_distance(_c1, _r1, _c2, _r2)
/// @description Returns axial/cube distance in hex steps between two hex cells
function scr_hex_distance(_c1, _r1, _c2, _r2) {
    var _x1 = _c1;
    var _z1 = _r1 - floor((_c1 - (_c1 & 1)) / 2);
    var _y1 = -_x1 - _z1;
    
    var _x2 = _c2;
    var _z2 = _r2 - floor((_c2 - (_c2 & 1)) / 2);
    var _y2 = -_x2 - _z2;
    
    return floor((abs(_x1 - _x2) + abs(_y1 - _y2) + abs(_z1 - _z2)) / 2);
}

/// @function scr_hex_get_stronghold_terrain(_stronghold_id)
/// @description Generates a 16x10 terrain matrix for the specified stronghold
function scr_hex_get_stronghold_terrain(_stronghold_id) {
    var _grid = array_create(16);
    var _layout = scr_stronghold_get_layout(_stronghold_id);
    var _reg = _layout.region;
    
    for (var c = 0; c < 16; c++) {
        _grid[c] = array_create(10);
        for (var r = 0; r < 10; r++) {
            var _t_type = "CRATON";
            var _t_name = "Basalt Craton";
            var _mp_cost = 1;
            var _def = 10;
            
            // Geography patterns based on region and coordinates
            if (_reg == "MARS") {
                // Mars Caldera: Center caldera crater, Basalt scarp in north
                if (c >= 6 && c <= 10 && r >= 3 && r <= 6) {
                    _t_type = "CRATER";
                    _t_name = "Caldera Floor";
                    _mp_cost = 1;
                    _def = 15;
                } else if (r <= 2 && c >= 3 && c <= 12) {
                    _t_type = "MOUNTAIN";
                    _t_name = "Basalt Scarp";
                    _mp_cost = 3;
                    _def = 35;
                } else if (c >= 13 || r >= 8) {
                    _t_type = "ROUGH";
                    _t_name = "Volcanic Apron";
                    _mp_cost = 2;
                    _def = 20;
                }
            } else if (string_pos("cascadia", _stronghold_id) > 0) {
                // Cascadia: Pacific water on left, Mass driver in middle, mountains on right
                if (c <= 3) {
                    _t_type = "WATER";
                    _t_name = "Pacific Shelf";
                    _mp_cost = 3;
                    _def = 0;
                } else if (c >= 12) {
                    _t_type = "MOUNTAIN";
                    _t_name = "Cascade Range";
                    _mp_cost = 3;
                    _def = 35;
                } else if (c >= 4 && c <= 6 && (r == 4 || r == 5)) {
                    _t_type = "FOREST";
                    _t_name = "Coastal Redwoods";
                    _mp_cost = 2;
                    _def = 20;
                }
            } else if (string_pos("gibraltar", _stronghold_id) > 0) {
                // Gibraltar: Strait water crossing horizontally
                if (r >= 4 && r <= 6) {
                    _t_type = "WATER";
                    _t_name = "Gibraltar Strait";
                    _mp_cost = 3;
                    _def = 0;
                } else if (c <= 4 || c >= 12) {
                    _t_type = "MOUNTAIN";
                    _t_name = "Pillars of Hercules";
                    _mp_cost = 3;
                    _def = 35;
                }
            } else {
                // Standard Earth Stronghold (e.g. Granite Deep Amazon)
                // River winding through c=6..8
                if ((c == 7 && r >= 1 && r <= 8) || (c == 6 && r >= 3 && r <= 5) || (c == 8 && r >= 6 && r <= 9)) {
                    _t_type = "WATER";
                    _t_name = "Amazon Tributary";
                    _mp_cost = 3;
                    _def = 0;
                } else if ((c >= 3 && c <= 5 && r <= 3) || (c >= 11 && c <= 13 && r >= 7)) {
                    _t_type = "FOREST";
                    _t_name = "Amazon Canopy";
                    _mp_cost = 2;
                    _def = 20;
                } else if ((c <= 2 && r <= 3) || (c >= 13 && r <= 3)) {
                    _t_type = "MOUNTAIN";
                    _t_name = "Granite Ridge";
                    _mp_cost = 3;
                    _def = 35;
                }
            }
            
            _grid[c][r] = {
                terrain_type: _t_type,
                name: _t_name,
                mp_cost: _mp_cost,
                defense_bonus: _def,
                facility_id: "",
                controlling_faction: "neutral"
            };
        }
    }
    
    // Stamp Strategic Subnode Base Facilities onto the Hex Grid
    for (var sni = 0; sni < array_length(_layout.subnodes); sni++) {
        var _sn = _layout.subnodes[sni];
        var _fc = clamp(round((_sn.map_x / 580.0) * 12.0) + 2, 1, 14);
        var _fr = clamp(round((_sn.map_y / 360.0) * 8.0) + 1, 1, 8);
        
        _grid[_fc][_fr].terrain_type = "BASE_FACILITY";
        _grid[_fc][_fr].name = _sn.name;
        _grid[_fc][_fr].mp_cost = 1;
        _grid[_fc][_fr].defense_bonus = 40;
        _grid[_fc][_fr].facility_id = _sn.id;
        _grid[_fc][_fr].controlling_faction = _sn.controlling_faction;
    }
    
    return _grid;
}

/// @function scr_hex_get_stronghold_units(_stronghold_id)
/// @description Spawns initial tactical PMC vanguard and OPFOR defense units on the hex grid
function scr_hex_get_stronghold_units(_stronghold_id) {
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
        stack_count: 5,
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
        stack_count: 6,
        status: "READY"
    });

    return _units;
}

/// @function scr_hex_get_reachable(_unit, _units_array, _terrain_grid)
/// @description Returns struct of reachable hex keys { "c_r": move_cost } via Dijkstra algorithm
function scr_hex_get_reachable(_unit, _units_array, _terrain_grid) {
    var _reachable = {};
    if (is_undefined(_unit) || _unit.current_mp <= 0) return _reachable;
    
    // Map of occupied hexes by other units
    var _occupied = {};
    for (var i = 0; i < array_length(_units_array); i++) {
        var _u = _units_array[i];
        if (_u.id != _unit.id && _u.hp > 0) {
            _occupied[string(_u.col) + "_" + string(_u.row)] = _u;
        }
    }
    
    var _dist = {};
    var _start_key = string(_unit.col) + "_" + string(_unit.row);
    _dist[_start_key] = 0;
    
    var _queue = [{ col: _unit.col, row: _unit.row, cost: 0 }];
    
    while (array_length(_queue) > 0) {
        var _best_idx = 0;
        var _best_cost = _queue[0].cost;
        for (var q = 1; q < array_length(_queue); q++) {
            if (_queue[q].cost < _best_cost) {
                _best_cost = _queue[q].cost;
                _best_idx = q;
            }
        }
        var _curr = _queue[_best_idx];
        array_delete(_queue, _best_idx, 1);
        
        var _curr_key = string(_curr.col) + "_" + string(_curr.row);
        if (_curr.cost > _dist[_curr_key]) continue;
        
        var _nbrs = scr_hex_get_neighbors(_curr.col, _curr.row);
        for (var n = 0; n < array_length(_nbrs); n++) {
            var _nc = _nbrs[n].col;
            var _nr = _nbrs[n].row;
            var _nkey = string(_nc) + "_" + string(_nr);
            
            // Check occupied
            if (variable_struct_exists(_occupied, _nkey)) {
                continue; // Cannot enter occupied hex
            }
            
            var _step_cost = 1;
            if (!is_undefined(_terrain_grid) && _nc < array_length(_terrain_grid) && _nr < array_length(_terrain_grid[_nc])) {
                _step_cost = _terrain_grid[_nc][_nr].mp_cost;
            }
            
            var _new_cost = _curr.cost + _step_cost;
            if (_new_cost <= _unit.current_mp) {
                var _prev_d = variable_struct_exists(_dist, _nkey) ? _dist[_nkey] : 999999;
                if (_new_cost < _prev_d) {
                    _dist[_nkey] = _new_cost;
                    variable_struct_set(_reachable, _nkey, _new_cost);
                    array_push(_queue, { col: _nc, row: _nr, cost: _new_cost });
                }
            }
        }
    }
    
    return _reachable;
}

/// @function scr_hex_resolve_skirmish(_attacker, _defender, _def_terr_bonus)
/// @description Computes skirmish combat damage and retaliation between two hex units
function scr_hex_resolve_skirmish(_attacker, _defender, _def_terr_bonus) {
    if (is_undefined(_def_terr_bonus)) _def_terr_bonus = 10;
    
    var _atk_val = _attacker.attack * (1.0 + (irandom_range(-15, 15) / 100.0));
    var _eff_def = _defender.defense * (1.0 + (_def_terr_bonus / 100.0));
    var _dmg_to_def = max(8, floor(_atk_val * (100.0 / (100.0 + _eff_def))));
    
    _defender.hp = max(0, _defender.hp - _dmg_to_def);
    
    var _retaliate_dmg = 0;
    var _dist = scr_hex_distance(_attacker.col, _attacker.row, _defender.col, _defender.row);
    if (_defender.hp > 0 && _dist <= _defender.range) {
        var _def_atk = _defender.attack * (1.0 + (irandom_range(-15, 15) / 100.0)) * 0.75;
        var _att_eff_def = _attacker.defense;
        _retaliate_dmg = max(5, floor(_def_atk * (100.0 / (100.0 + _att_eff_def))));
        _attacker.hp = max(0, _attacker.hp - _retaliate_dmg);
    }
    
    return {
        attacker_id: _attacker.id,
        defender_id: _defender.id,
        damage_dealt: _dmg_to_def,
        damage_taken: _retaliate_dmg,
        defender_destroyed: (_defender.hp <= 0),
        attacker_destroyed: (_attacker.hp <= 0)
    };
}

/// @function scr_stronghold_advance_turn(_stronghold_id, _units_array, _terrain_grid, _turn_num)
/// @description Advances tactical turn: Executes OPFOR AI phase, resolves engagements, refreshes MPs
function scr_stronghold_advance_turn(_stronghold_id, _units_array, _terrain_grid, _turn_num) {
    var _log = [];
    array_push(_log, "=== CYCLE " + string(_turn_num) + " CONCLUDED. ADVANCING TO CYCLE " + string(_turn_num + 1) + " ===");
    
    // OPFOR AI Phase: Maneuver & Engage
    for (var i = 0; i < array_length(_units_array); i++) {
        var _u = _units_array[i];
        if (_u.faction != "pmc" && _u.hp > 0) {
            var _nearest_pmc = undefined;
            var _min_dist = 999;
            for (var p = 0; p < array_length(_units_array); p++) {
                var _pu = _units_array[p];
                if (_pu.faction == "pmc" && _pu.hp > 0) {
                    var _d = scr_hex_distance(_u.col, _u.row, _pu.col, _pu.row);
                    if (_d < _min_dist) {
                        _min_dist = _d;
                        _nearest_pmc = _pu;
                    }
                }
            }
            
            if (!is_undefined(_nearest_pmc)) {
                if (_min_dist <= _u.range) {
                    var _terr_def = 10;
                    if (!is_undefined(_terrain_grid) && _nearest_pmc.col < array_length(_terrain_grid) && _nearest_pmc.row < array_length(_terrain_grid[_nearest_pmc.col])) {
                        _terr_def = _terrain_grid[_nearest_pmc.col][_nearest_pmc.row].defense_bonus;
                    }
                    var _sk = scr_hex_resolve_skirmish(_u, _nearest_pmc, _terr_def);
                    var _msg = "OPFOR " + _u.unit_label + " ENGAGED " + _nearest_pmc.unit_label + ": -" + string(_sk.damage_dealt) + " HP";
                    if (_sk.defender_destroyed) _msg += " [UNIT DESTROYED!]";
                    array_push(_log, _msg);
                } else {
                    var _nbrs = scr_hex_get_neighbors(_u.col, _u.row);
                    var _best_nbr = undefined;
                    var _best_dist = _min_dist;
                    for (var n = 0; n < array_length(_nbrs); n++) {
                        var _cand = _nbrs[n];
                        var _is_occ = false;
                        for (var o = 0; o < array_length(_units_array); o++) {
                            if (_units_array[o].hp > 0 && _units_array[o].col == _cand.col && _units_array[o].row == _cand.row) {
                                _is_occ = true;
                                break;
                            }
                        }
                        if (!_is_occ) {
                            var _nd = scr_hex_distance(_cand.col, _cand.row, _nearest_pmc.col, _nearest_pmc.row);
                            if (_nd < _best_dist) {
                                _best_dist = _nd;
                                _best_nbr = _cand;
                            }
                        }
                    }
                    if (!is_undefined(_best_nbr)) {
                        _u.col = _best_nbr.col;
                        _u.row = _best_nbr.row;
                        array_push(_log, "OPFOR " + _u.unit_label + " ADVANCED TO SECTOR [" + string(_u.col) + "," + string(_u.row) + "]");
                    }
                }
            }
        }
    }
    
    // Refresh all active units MP and status
    for (var i = 0; i < array_length(_units_array); i++) {
        var _u = _units_array[i];
        if (_u.hp > 0) {
            _u.current_mp = _u.max_mp;
            _u.status = "READY";
        }
    }
    
    array_push(_log, "CYCLE " + string(_turn_num + 1) + ": ALL VANGUARD UNITS RE-ARMED & RE-FUELED.");
    return _log;
}
"""

with open("scripts/scr_territory_war_system/scr_territory_war_system.gml", "a") as f:
    f.write(hex_code)

print("Successfully appended hex engine code!")
