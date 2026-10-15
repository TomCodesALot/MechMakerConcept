import json

with open('datafiles/mobile_suits/mobile_suit_catalog.json') as f:
    catalog = json.load(f)

def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')

def get_move_type(c_class):
    c = c_class.lower()
    if any(k in c for k in ['interceptor', 'aero', 'zero-g', 'fighter', 'high-speed', 'courier', 'skirmisher']):
        return 'aero'
    if any(k in c for k in ['sniper', 'hover', 'recon', 'scout', 'infiltrator', 'rail-sniper']):
        return 'hover'
    if any(k in c for k in ['artillery', 'mortar', 'bastion', 'behemoth', 'siege', 'juggernaut', 'leviathan', 'tread']):
        return 'treads'
    return 'biped'

# 1. Build map_definitions GML
from test_generate_24_maps_code import maps_data

gml_map_defs = "// 3. Multi-Map System: Earth & Space Theaters with Dynamic Elevation & Terrain (24 Maps)\ncurrent_map_id = 0;\n\nmap_definitions = [\n"
for m in maps_data:
    gml_map_defs += f"""    {{
        id: {m['id']},
        name: "{m['name']}",
        theater: "{m['theater']}",
        category: "{m['category']}",
        gravity: {m['gravity']},
        desc: "{esc(m['desc'])}",
        bg_col: {m['bg_col']},
        grid_col_base: {m['base']},
        grid_col_elev1: {m['e1']},
        grid_col_elev2: {m['e2']},
        cliff_col_se: {m['se']},
        cliff_col_sw: {m['sw']},
        ambient_tag: "{m['ambient']}"
    }},\n"""
gml_map_defs = gml_map_defs.rstrip(",\n") + "\n];\n"

# 2. Build grid arrays & load_map GML
gml_load_map = """grid_cols = 20;
grid_rows = 20;
tile_w = 64.0;
tile_h = 32.0;
elev_h = 16.0;

grid_elev = array_create(grid_cols);
grid_terrain = array_create(grid_cols);
grid_cover = array_create(grid_cols);
for (var c = 0; c < grid_cols; c++) {
    grid_elev[c] = array_create(grid_rows, 0);
    grid_terrain[c] = array_create(grid_rows, 0);
    grid_cover[c] = array_create(grid_rows, 0);
}

load_map = function(_map_idx) {
    current_map_id = clamp(_map_idx, 0, array_length(map_definitions) - 1);
    for (var c = 0; c < grid_cols; c++) {
        for (var r = 0; r < grid_rows; r++) {
            grid_elev[c][r] = 0;
            grid_terrain[c][r] = 0;
            grid_cover[c][r] = 0;
        }
    }

    if (current_map_id == 0) {
        // MAP 0: SECTOR 4 MINING OUTPOST (EARTH)
        for (var c = 5; c <= 14; c++) {
            for (var r = 5; r <= 14; r++) {
                grid_elev[c][r] = 1;
                grid_terrain[c][r] = 2;
            }
        }
        for (var c = 8; c <= 11; c++) {
            for (var r = 8; r <= 11; r++) {
                grid_elev[c][r] = 2;
                grid_terrain[c][r] = 1;
            }
        }
        for (var r = 0; r < grid_rows; r++) {
            grid_terrain[9][r] = 1; grid_terrain[10][r] = 1;
        }
        grid_cover[8][8] = 2; grid_cover[11][11] = 2; grid_cover[5][5] = 1; grid_cover[14][14] = 1;
    } else if (current_map_id == 1) {
        // MAP 1: NEO-VERONA COASTAL RUINS (EARTH)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                var _diag = c + r;
                if (_diag >= 17 && _diag <= 21) {
                    grid_terrain[c][r] = 3; // Water canal
                    grid_elev[c][r] = 0;
                } else {
                    grid_elev[c][r] = 1;
                    grid_terrain[c][r] = (_diag < 17) ? 1 : 2;
                }
                if (c >= 8 && c <= 11 && r >= 8 && r <= 11) {
                    grid_elev[c][r] = 2;
                    grid_terrain[c][r] = 1;
                    grid_cover[c][r] = 1;
                }
            }
        }
        grid_cover[7][7] = 2; grid_cover[12][12] = 2;
    } else if (current_map_id == 2) {
        // MAP 2: VOLCANIC CALDERA RIDGE (EARTH)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 1;
                grid_terrain[c][r] = 0;
                if (c <= 2 || c >= 17 || r <= 2 || r >= 17) {
                    grid_elev[c][r] = 2;
                    grid_terrain[c][r] = 2;
                }
                if (abs(c - r) <= 1) {
                    grid_terrain[c][r] = 5; // Slag fissure
                    grid_elev[c][r] = 0;
                }
            }
        }
        grid_elev[9][9] = 1; grid_terrain[9][9] = 1;
        grid_elev[10][10] = 1; grid_terrain[10][10] = 1;
        grid_cover[6][6] = 2; grid_cover[13][13] = 2;
    } else if (current_map_id == 3) {
        // MAP 3: GLACIAL CREVASSE PASS (EARTH)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 1;
                grid_terrain[c][r] = 0;
                if (r <= 2 || r >= 17) grid_elev[c][r] = 2;
                if (c >= 8 && c <= 11) {
                    grid_terrain[c][r] = 4; // Glacial chasm
                    grid_elev[c][r] = 0;
                }
            }
        }
        for (var c = 8; c <= 11; c++) {
            grid_elev[c][5] = 1; grid_terrain[c][5] = 1;
            grid_elev[c][6] = 1; grid_terrain[c][6] = 1;
            grid_elev[c][13] = 1; grid_terrain[c][13] = 1;
            grid_elev[c][14] = 1; grid_terrain[c][14] = 1;
        }
        grid_cover[5][5] = 2; grid_cover[14][14] = 2;
    } else if (current_map_id == 4) {
        // MAP 4: VERDANT JUNGLE DELTA (EARTH)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 1;
                grid_terrain[c][r] = 0;
                var _riv_r = 8 + floor(sin(c * 0.4) * 3);
                if (abs(r - _riv_r) <= 1) {
                    grid_terrain[c][r] = 3; // River
                    grid_elev[c][r] = 0;
                }
                if ((c >= 2 && c <= 5 && r >= 2 && r <= 5) || (c >= 14 && c <= 17 && r >= 14 && r <= 17)) {
                    grid_elev[c][r] = 2;
                    grid_cover[c][r] = 2;
                }
            }
        }
        grid_elev[9][8] = 1; grid_terrain[9][8] = 1;
        grid_elev[10][8] = 1; grid_terrain[10][8] = 1;
    } else if (current_map_id == 5) {
        // MAP 5: SAHARA DUNE REFINERY (EARTH)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 0;
                grid_terrain[c][r] = 0;
                if (c == 9 || c == 10 || r == 9 || r == 10) grid_terrain[c][r] = 1; // Pipeline road
                if ((c >= 4 && c <= 6 && r >= 4 && r <= 6) || (c >= 13 && c <= 15 && r >= 13 && r <= 15)) {
                    grid_elev[c][r] = 1;
                    grid_cover[c][r] = 2;
                }
            }
        }
    } else if (current_map_id == 6) {
        // MAP 6: MEGA-CITY SECTOR 9 GRID (EARTH)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 0;
                grid_terrain[c][r] = 2; // Rubble
                if (c == 8 || c == 9 || c == 10 || r == 8 || r == 9 || r == 10) grid_terrain[c][r] = 1; // Avenues
                if ((c >= 2 && c <= 5 && r >= 2 && r <= 5) ||
                    (c >= 14 && c <= 17 && r >= 2 && r <= 5) ||
                    (c >= 2 && c <= 5 && r >= 14 && r <= 17) ||
                    (c >= 14 && c <= 17 && r >= 14 && r <= 17)) {
                    grid_elev[c][r] = 2;
                    grid_cover[c][r] = 2;
                }
            }
        }
    } else if (current_map_id == 7) {
        // MAP 7: SUBTERRANEAN MAGMA VAULT (EARTH)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 1;
                grid_terrain[c][r] = 0;
                if (r == 5 || r == 6 || r == 13 || r == 14) {
                    grid_terrain[c][r] = 5; // Slag river
                    grid_elev[c][r] = 0;
                }
                if (c >= 8 && c <= 11) {
                    grid_elev[c][r] = 1;
                    grid_terrain[c][r] = 1; // Catwalk bridge
                }
            }
        }
        grid_cover[5][9] = 2; grid_cover[14][9] = 2;
    } else if (current_map_id == 8) {
        // MAP 8: ABANDONED SPACEPORT TERMINAL (EARTH)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 0;
                grid_terrain[c][r] = 0;
                if ((r >= 4 && r <= 6) || (r >= 13 && r <= 15) || (c == 9 || c == 10)) {
                    grid_terrain[c][r] = 1; // Tarmac runways
                }
                if ((c >= 2 && c <= 4 && r >= 9 && r <= 11) || (c >= 15 && c <= 17 && r >= 9 && r <= 11)) {
                    grid_terrain[c][r] = 2; // Blast craters
                }
                if (c <= 2 && (r <= 3 || r >= 16)) {
                    grid_elev[c][r] = 2;
                    grid_cover[c][r] = 2;
                }
            }
        }
    } else if (current_map_id == 9) {
        // MAP 9: IRRADIATED SALT FLATS (EARTH)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 1;
                grid_terrain[c][r] = 0;
                if ((c >= 4 && c <= 7 && r >= 6 && r <= 13) || (c >= 12 && c <= 15 && r >= 6 && r <= 13)) {
                    grid_terrain[c][r] = 3; // Brine pool
                    grid_elev[c][r] = 0;
                }
                if (r == 9 || r == 10) {
                    grid_elev[c][r] = 0;
                    grid_terrain[c][r] = 1; // Sunken trench
                }
            }
        }
        grid_cover[9][8] = 2; grid_cover[10][8] = 2; grid_cover[9][11] = 2; grid_cover[10][11] = 2;
    } else if (current_map_id == 10) {
        // MAP 10: HELIOS-7 ORBITAL ARRAY (SPACE)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_terrain[c][r] = 4; // Vacuum void
                grid_elev[c][r] = 0;
                if (c >= 8 && c <= 11 || r >= 8 && r <= 11) {
                    grid_terrain[c][r] = 1; // Catwalk
                    grid_elev[c][r] = 1;
                }
                if (c >= 8 && c <= 11 && r >= 8 && r <= 11) {
                    grid_elev[c][r] = 2;
                    grid_cover[c][r] = 2; // Spire platform
                }
                if ((c >= 2 && c <= 4 && r >= 2 && r <= 4) ||
                    (c >= 15 && c <= 17 && r >= 2 && r <= 4) ||
                    (c >= 2 && c <= 4 && r >= 15 && r <= 17) ||
                    (c >= 15 && c <= 17 && r >= 15 && r <= 17)) {
                    grid_elev[c][r] = 1;
                    grid_terrain[c][r] = 1;
                    grid_cover[c][r] = 1;
                }
            }
        }
    } else if (current_map_id == 11) {
        // MAP 11: ASTEROID SYNDICATE FORTRESS (SPACE)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 1;
                grid_terrain[c][r] = 0;
                if (c >= 8 && c <= 11) {
                    grid_elev[c][r] = 0;
                    grid_terrain[c][r] = 5; // Slag trench
                }
                if ((c >= 3 && c <= 6 && r >= 3 && r <= 6) || (c >= 13 && c <= 16 && r >= 13 && r <= 16)) {
                    grid_elev[c][r] = 2;
                    grid_terrain[c][r] = 2;
                    grid_cover[c][r] = 2;
                }
            }
        }
        grid_terrain[9][5] = 1; grid_terrain[10][5] = 1; grid_elev[9][5] = 1; grid_elev[10][5] = 1;
        grid_terrain[9][14] = 1; grid_terrain[10][14] = 1; grid_elev[9][14] = 1; grid_elev[10][14] = 1;
    } else if (current_map_id == 12) {
        // MAP 12: COLONY CYLINDER SHELL (SPACE)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 1;
                grid_terrain[c][r] = 0;
                if (r == 9 || r == 10) {
                    grid_terrain[c][r] = 3; // Climate canal
                    grid_elev[c][r] = 0;
                }
                if (r == 7 || r == 12) grid_terrain[c][r] = 1; // Maglev rail
                if ((c >= 3 && c <= 6 && r <= 4) || (c >= 13 && c <= 16 && r >= 15)) {
                    grid_elev[c][r] = 2;
                    grid_cover[c][r] = 2;
                }
            }
        }
        grid_elev[5][9] = 1; grid_elev[5][10] = 1; grid_terrain[5][9] = 1; grid_terrain[5][10] = 1;
        grid_elev[14][9] = 1; grid_elev[14][10] = 1; grid_terrain[14][9] = 1; grid_terrain[14][10] = 1;
    } else if (current_map_id == 13) {
        // MAP 13: LUNAR REGOLITH CRATER (SPACE)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                var _dist_sq = sqr(c - 9.5) + sqr(r - 9.5);
                if (_dist_sq <= 16) {
                    grid_elev[c][r] = 0;
                    grid_terrain[c][r] = 0; // Crater bottom
                } else if (_dist_sq >= 36 && _dist_sq <= 64) {
                    grid_elev[c][r] = 2;
                    grid_terrain[c][r] = 2; // Crater rim
                } else {
                    grid_elev[c][r] = 1;
                    grid_terrain[c][r] = 0;
                }
            }
        }
        grid_cover[9][9] = 2; grid_cover[10][10] = 2;
    } else if (current_map_id == 14) {
        // MAP 14: DERELICT FLEET GRAVEYARD (SPACE)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_terrain[c][r] = 4; // Void
                grid_elev[c][r] = 0;
                if ((c >= 2 && c <= 8 && r >= 2 && r <= 8) || (c >= 11 && c <= 17 && r >= 11 && r <= 17)) {
                    grid_elev[c][r] = 1;
                    grid_terrain[c][r] = 2; // Ship hull debris
                    grid_cover[c][r] = 1;
                }
                if (c >= 8 && c <= 11 && r >= 8 && r <= 11) {
                    grid_elev[c][r] = 1;
                    grid_terrain[c][r] = 1; // Armor bridge
                }
            }
        }
        grid_cover[5][5] = 2; grid_cover[14][14] = 2;
    } else if (current_map_id == 15) {
        // MAP 15: SPACE ELEVATOR RING TERMINAL (SPACE)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                var _dist_sq = sqr(c - 9.5) + sqr(r - 9.5);
                if (_dist_sq <= 8 || _dist_sq >= 80) {
                    grid_terrain[c][r] = 4; // Void
                    grid_elev[c][r] = 0;
                } else {
                    grid_elev[c][r] = 1;
                    grid_terrain[c][r] = 1; // Ring platform
                }
            }
        }
        grid_cover[9][4] = 2; grid_cover[9][15] = 2; grid_cover[4][9] = 2; grid_cover[15][9] = 2;
    } else if (current_map_id == 16) {
        // MAP 16: COMET CORE ICE QUARRY (SPACE)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 1;
                grid_terrain[c][r] = 0;
                if ((c >= 4 && c <= 6) || (c >= 13 && c <= 15)) {
                    grid_terrain[c][r] = 4; // Gas fissure
                    grid_elev[c][r] = 0;
                }
                if (r == 9 || r == 10) {
                    grid_elev[c][r] = 1;
                    grid_terrain[c][r] = 1; // Conveyer bridge
                }
                if ((c <= 2 || c >= 17) && (r <= 2 || r >= 17)) {
                    grid_elev[c][r] = 2;
                    grid_cover[c][r] = 2;
                }
            }
        }
    } else if (current_map_id == 17) {
        // MAP 17: LAGRANGE-5 LOGISTICS HUB (SPACE)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 1;
                grid_terrain[c][r] = 1;
                if (c <= 1 || c >= 18 || r <= 1 || r >= 18) {
                    grid_terrain[c][r] = 4; // Berthing void
                    grid_elev[c][r] = 0;
                }
                if ((c % 4 == 0) && (r >= 4 && r <= 15)) {
                    grid_cover[c][r] = 2; // Container stacks
                }
            }
        }
    } else if (current_map_id == 18) {
        // MAP 18: DEEP VOID COMMS RELAY (SPACE)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_terrain[c][r] = 4; // Void
                grid_elev[c][r] = 0;
                if (c >= 7 && c <= 12 && r >= 7 && r <= 12) {
                    grid_elev[c][r] = 2;
                    grid_terrain[c][r] = 1; // Dish platform
                    grid_cover[c][r] = 1;
                }
                if (c == 9 || c == 10 || r == 9 || r == 10) {
                    grid_elev[c][r] = 1;
                    grid_terrain[c][r] = 1; // Antenna spar
                }
            }
        }
        grid_cover[9][9] = 2; grid_cover[10][10] = 2;
    } else if (current_map_id == 19) {
        // MAP 19: SOLAR MIRROR SWARM STATION (SPACE)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_terrain[c][r] = 4; // Void
                grid_elev[c][r] = 0;
                if ((c >= 2 && c <= 7 && r >= 2 && r <= 7) ||
                    (c >= 12 && c <= 17 && r >= 2 && r <= 7) ||
                    (c >= 2 && c <= 7 && r >= 12 && r <= 17) ||
                    (c >= 12 && c <= 17 && r >= 12 && r <= 17)) {
                    grid_elev[c][r] = 1;
                    grid_terrain[c][r] = 1; // Mirror array
                }
                if (c >= 8 && c <= 11 && r >= 8 && r <= 11) {
                    grid_elev[c][r] = 1;
                    grid_terrain[c][r] = 1; // Central hub
                }
                if (c == 9 || c == 10) {
                    if (r == 0 || r == 1 || r == 18 || r == 19) grid_terrain[c][r] = 5; // Radiator
                }
            }
        }
    } else if (current_map_id == 20) {
        // MAP 20: TEST: ELEVATION BENCHMARK RANGE (TEST)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 0;
                grid_terrain[c][r] = 0;
                if (c >= 3 && c <= 16 && r >= 3 && r <= 16) grid_elev[c][r] = 1;
                if (c >= 6 && c <= 13 && r >= 6 && r <= 13) grid_elev[c][r] = 2;
                if (c >= 8 && c <= 11 && r >= 8 && r <= 11) grid_elev[c][r] = 3;
                if (c == 9 || c == 10 || r == 9 || r == 10) grid_terrain[c][r] = 1; // Cardinal ramp
            }
        }
        grid_cover[8][8] = 2; grid_cover[11][11] = 2;
    } else if (current_map_id == 21) {
        // MAP 21: TEST: TERRAIN STRESS RANGE (TEST)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 0;
                if (r >= 0 && r <= 2) grid_terrain[c][r] = 0; // DIRT
                else if (r >= 3 && r <= 5) grid_terrain[c][r] = 1; // ROAD
                else if (r >= 6 && r <= 8) grid_terrain[c][r] = 2; // RUBBLE
                else if (r >= 9 && r <= 11) grid_terrain[c][r] = 3; // WATER
                else if (r >= 12 && r <= 14) grid_terrain[c][r] = 4; // VACUUM
                else grid_terrain[c][r] = 5; // SLAG
                if (c == 4 || c == 5 || c == 14 || c == 15) {
                    grid_terrain[c][r] = 1; // Test bridge
                    grid_elev[c][r] = 1;
                }
            }
        }
    } else if (current_map_id == 22) {
        // MAP 22: TEST: OBSTACLE & COVER GAUNTLET (TEST)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 0;
                grid_terrain[c][r] = 1; // Clear floor
                if ((c % 3 == 0) && (r % 3 == 0)) {
                    grid_cover[c][r] = 2; // Heavy pillar
                } else if ((c % 2 == 1) && (r % 2 == 1)) {
                    grid_cover[c][r] = 1; // Light barricade
                }
            }
        }
    } else if (current_map_id == 23) {
        // MAP 23: TEST: DUEL ARENA PROVING GROUND (TEST)
        for (var c = 0; c < grid_cols; c++) {
            for (var r = 0; r < grid_rows; r++) {
                grid_elev[c][r] = 1;
                grid_terrain[c][r] = 0;
                if (c >= 6 && c <= 13 && r >= 6 && r <= 13) grid_terrain[c][r] = 1; // Center ring
            }
        }
        grid_cover[5][5] = 2; grid_cover[14][5] = 2; grid_cover[5][14] = 2; grid_cover[14][14] = 2;
    }
};

load_map(0);
"""

# 3. Build 104 chassis_swap_pool
gml_swap_pool = """// 3b. Pre-Battle Deployment Deck & Chassis Swapping Test Chamber
deployment_deck_active = false;
deployment_selected_slot = 0;
deployment_selected_team = "ALLIED";
deployment_chassis_idx = 0;
deployment_facing = 0;
deployment_perspective = "front";
deployment_anim_state = "idle";
deployment_map_page = 0;
deployment_map_filter = "ALL"; // "ALL", "EARTH", "SPACE", "TEST"

chassis_swap_pool = [
    { id: "custom_biped", name: "Custom Vanguard Brawler", type: "custom_biped", move_type: "biped", default_squad: "SUPER_ACE", armor: 2600, power: 1850, speed: 450, sprite_asset: spr_ms_custom_biped_heavy_idle, desc: "Modular heavy biped with 120mm cannon and solid ablative tower shield." },
    { id: "custom_hover", name: "Custom Ghost Sniper", type: "custom_hover", move_type: "hover", default_squad: "SUPER_ACE", armor: 1750, power: 1950, speed: 680, sprite_asset: spr_ms_custom_hover_sniper_idle, desc: "Hover skirt chassis armed with high-velocity magnetic linear railgun." },
    { id: "custom_tread", name: "Custom Scrapper Fortress", type: "custom_tread", move_type: "treads", default_squad: "PLATOON_3", armor: 3200, power: 2100, speed: 380, sprite_asset: spr_ms_custom_tread_artillery_idle, desc: "Caterpillar tank tread fortress carrying twin 200mm heavy howitzers." },
    { id: "custom_aero", name: "Custom Stratos Striker", type: "custom_aero", move_type: "aero", default_squad: "SUPER_ACE", armor: 1900, power: 2200, speed: 820, sprite_asset: spr_ms_custom_aero_striker_idle, desc: "Aerodynamic swept-wing space vernier chassis with high-yield beam carbines." },\n"""

for sid, s in catalog.items():
    mtype = get_move_type(s['chassis_class'])
    squad = 'PLATOON_3' if s.get('mass_production_line', False) else 'SUPER_ACE'
    s_asset = s['sprite_asset']
    name = esc(s['name'])
    lore = esc(s.get('lore', s.get('doctrine', 'Combat mobile suit.')))
    gml_swap_pool += f"""    {{ id: "{sid}", name: "{name}", type: "{sid}", move_type: "{mtype}", default_squad: "{squad}", armor: {s['armor']}, power: {s['power']}, speed: {s['speed']}, sprite_asset: {s_asset}, desc: "{lore}" }},\n"""
gml_swap_pool = gml_swap_pool.rstrip(",\n") + "\n];\n"

gml_swap_func = """
swap_unit_chassis = function(_unit_idx, _chassis_data) {
    if (_unit_idx < 0 || _unit_idx >= array_length(units)) return;
    var _u = units[_unit_idx];
    _u.mech_type = _chassis_data.type;
    _u.move_type = _chassis_data.move_type;
    _u.space_adapted = (_chassis_data.move_type == "aero" || _chassis_data.move_type == "hover");
    _u.squad_type = _chassis_data.default_squad;
    _u.squad_members_count = (_chassis_data.default_squad == "PLATOON_3") ? 3 : 1;
    _u.squad_max_count = _u.squad_members_count;
    _u.accuracy = clamp(floor(_chassis_data.speed * 0.12), 65, 92);
    _u.evasion = clamp(floor(_chassis_data.speed * 0.08), 25, 75);
    _u.components.torso.max = floor(_chassis_data.armor * 0.40);
    _u.components.torso.cur = _u.components.torso.max;
    _u.components.arm_left.max = floor(_chassis_data.armor * 0.22);
    _u.components.arm_left.cur = _u.components.arm_left.max;
    _u.components.arm_right.max = floor(_chassis_data.armor * 0.22);
    _u.components.arm_right.cur = _u.components.arm_right.max;
    _u.components.legs.max = floor(_chassis_data.armor * 0.30);
    _u.components.legs.cur = _u.components.legs.max;
    if (variable_struct_exists(_chassis_data, "sprite_asset") && sprite_exists(_chassis_data.sprite_asset)) {
        _u.sprite_asset = _chassis_data.sprite_asset;
    }
};
"""

full_replacement = gml_map_defs + "\n" + gml_load_map + "\n" + gml_swap_pool + gml_swap_func

# Check token balance of full replacement
c_open, c_close = full_replacement.count('{'), full_replacement.count('}')
p_open, p_close = full_replacement.count('('), full_replacement.count(')')
b_open, b_close = full_replacement.count('['), full_replacement.count(']')
print(f"Full replacement token balance: curlies {c_open}=={c_close}, parens {p_open}=={p_close}, brackets {b_open}=={b_close}")
assert c_open == c_close and p_open == p_close and b_open == b_close

# Read current Create_0.gml and find boundaries
with open('objects/obj_BattleManager/Create_0.gml', 'r') as f:
    text = f.read()

start_marker = "// 3. Multi-Map System: Earth & Space Theaters"
end_marker = "// 4. Isometric Camera & Viewport Controls"

idx1 = text.find(start_marker)
idx2 = text.find(end_marker)
assert idx1 != -1 and idx2 != -1, f"Markers not found: idx1={idx1}, idx2={idx2}"

new_create_0 = text[:idx1] + full_replacement + "\n" + text[idx2:]

with open('objects/obj_BattleManager/Create_0.gml', 'w') as f:
    f.write(new_create_0)

print("Create_0.gml successfully updated with 24 Maps and 104 Chassis Swap Pool!")
