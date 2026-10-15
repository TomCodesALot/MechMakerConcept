import json
import os

print("=== Generating 24 Tactical Maps and 104 Chassis Swap Pool for obj_BattleManager ===")

# Load Mobile Suit Catalog
with open('datafiles/mobile_suits/mobile_suit_catalog.json') as f:
    catalog = json.load(f)

# Helper function to escape string for GML
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

# 1. 24 MAP DEFINITIONS
maps_data = [
    # --- EARTH THEATERS (0 - 9) ---
    {
        "id": 0, "name": "SECTOR 4 MINING OUTPOST", "theater": "EARTH", "category": "EARTH", "gravity": 1.0,
        "desc": "Terraced excavation quarry with haulage roads, rock shelves, and heavy machinery.",
        "bg_col": "make_color_rgb(18, 14, 12)", "base": "make_color_rgb(34, 28, 22)",
        "e1": "make_color_rgb(52, 44, 34)", "e2": "make_color_rgb(72, 62, 48)",
        "se": "make_color_rgb(26, 20, 16)", "sw": "make_color_rgb(16, 12, 10)",
        "ambient": "[ATMOSPHERE: 1.0 ATM // GRAVITY: 1.0G // EARTH QUARRY]"
    },
    {
        "id": 1, "name": "NEO-VERONA COASTAL RUINS", "theater": "EARTH", "category": "EARTH", "gravity": 1.0,
        "desc": "Sunken highway overpasses, deep seawater canals, and concrete seawall redoubts.",
        "bg_col": "make_color_rgb(8, 18, 26)", "base": "make_color_rgb(14, 38, 52)",
        "e1": "make_color_rgb(28, 54, 66)", "e2": "make_color_rgb(46, 76, 88)",
        "se": "make_color_rgb(10, 26, 36)", "sw": "make_color_rgb(6, 16, 22)",
        "ambient": "[ATMOSPHERE: 1.0 ATM // COASTAL SEAWALL // WATER CANALS]"
    },
    {
        "id": 2, "name": "VOLCANIC CALDERA RIDGE", "theater": "EARTH", "category": "EARTH", "gravity": 1.0,
        "desc": "Molten slag channels, obsidian basalt plateaus, and sulfur geothermal vents.",
        "bg_col": "make_color_rgb(24, 10, 8)", "base": "make_color_rgb(42, 22, 18)",
        "e1": "make_color_rgb(64, 32, 24)", "e2": "make_color_rgb(88, 45, 30)",
        "se": "make_color_rgb(32, 14, 10)", "sw": "make_color_rgb(18, 8, 6)",
        "ambient": "[ATMOSPHERE: 1.0 ATM // MOLTEN SLAG RUNOFF // BASALT RIDGE]"
    },
    {
        "id": 3, "name": "GLACIAL CREVASSE PASS", "theater": "EARTH", "category": "EARTH", "gravity": 1.0,
        "desc": "Frozen tundra ice, bottomless glacial chasms, and slippery pack-ice bridges.",
        "bg_col": "make_color_rgb(12, 20, 28)", "base": "make_color_rgb(28, 48, 65)",
        "e1": "make_color_rgb(45, 72, 95)", "e2": "make_color_rgb(70, 105, 135)",
        "se": "make_color_rgb(20, 35, 48)", "sw": "make_color_rgb(12, 22, 32)",
        "ambient": "[ATMOSPHERE: 1.0 ATM // SUB-ZERO BLIZZARD // GLACIAL CREVASSE]"
    },
    {
        "id": 4, "name": "VERDANT JUNGLE DELTA", "theater": "EARTH", "category": "EARTH", "gravity": 1.0,
        "desc": "Winding tropical river basins, submerged mangrove mud, and karst limestone bluffs.",
        "bg_col": "make_color_rgb(10, 18, 12)", "base": "make_color_rgb(22, 42, 24)",
        "e1": "make_color_rgb(36, 62, 38)", "e2": "make_color_rgb(52, 85, 54)",
        "se": "make_color_rgb(16, 30, 18)", "sw": "make_color_rgb(10, 18, 12)",
        "ambient": "[ATMOSPHERE: 1.0 ATM // TROPICAL CANOPY // RIVER DELTA]"
    },
    {
        "id": 5, "name": "SAHARA DUNE REFINERY", "theater": "EARTH", "category": "EARTH", "gravity": 1.0,
        "desc": "Crushed sandstone flats, heavy industrial oil pipelines, and elevated extraction derricks.",
        "bg_col": "make_color_rgb(24, 18, 10)", "base": "make_color_rgb(50, 38, 22)",
        "e1": "make_color_rgb(75, 58, 35)", "e2": "make_color_rgb(105, 82, 50)",
        "se": "make_color_rgb(38, 28, 16)", "sw": "make_color_rgb(22, 16, 10)",
        "ambient": "[ATMOSPHERE: 1.0 ATM // SANDSTORM HAZE // PIPELINE CORRIDOR]"
    },
    {
        "id": 6, "name": "MEGA-CITY SECTOR 9 GRID", "theater": "EARTH", "category": "EARTH", "gravity": 1.0,
        "desc": "Urban skyscraper foundations, wide concrete avenues, and collapsed overpass debris.",
        "bg_col": "make_color_rgb(14, 16, 20)", "base": "make_color_rgb(30, 35, 44)",
        "e1": "make_color_rgb(48, 55, 68)", "e2": "make_color_rgb(70, 80, 98)",
        "se": "make_color_rgb(22, 26, 34)", "sw": "make_color_rgb(14, 16, 22)",
        "ambient": "[ATMOSPHERE: 1.0 ATM // HIGH-RISE DOWNTOWN // METROPOLITAN GRID]"
    },
    {
        "id": 7, "name": "SUBTERRANEAN MAGMA VAULT", "theater": "EARTH", "category": "EARTH", "gravity": 1.0,
        "desc": "Underground crust geothermal facility with glowing slag rivers and titanium bridges.",
        "bg_col": "make_color_rgb(20, 8, 6)", "base": "make_color_rgb(38, 18, 14)",
        "e1": "make_color_rgb(58, 28, 22)", "e2": "make_color_rgb(82, 40, 30)",
        "se": "make_color_rgb(28, 12, 10)", "sw": "make_color_rgb(16, 8, 6)",
        "ambient": "[SUB-CRUST CHAMBER // GEOTHERMAL DRILL // MAGMA TRENCH]"
    },
    {
        "id": 8, "name": "ABANDONED SPACEPORT TERMINAL", "theater": "EARTH", "category": "EARTH", "gravity": 1.0,
        "desc": "Blast-scored aerospace tarmac runways, ferrocrete hangars, and gantry rail systems.",
        "bg_col": "make_color_rgb(16, 18, 22)", "base": "make_color_rgb(32, 38, 48)",
        "e1": "make_color_rgb(50, 58, 72)", "e2": "make_color_rgb(72, 84, 102)",
        "se": "make_color_rgb(24, 28, 36)", "sw": "make_color_rgb(14, 16, 22)",
        "ambient": "[ATMOSPHERE: 1.0 ATM // AEROSPACE TARMAC // BLAST DEFLECTORS]"
    },
    {
        "id": 9, "name": "IRRADIATED SALT FLATS", "theater": "EARTH", "category": "EARTH", "gravity": 1.0,
        "desc": "Corrosive white alkali salt crust, brine drainage pools, and sunken trench bunkers.",
        "bg_col": "make_color_rgb(22, 20, 24)", "base": "make_color_rgb(46, 44, 52)",
        "e1": "make_color_rgb(68, 66, 78)", "e2": "make_color_rgb(94, 92, 108)",
        "se": "make_color_rgb(34, 32, 40)", "sw": "make_color_rgb(20, 18, 24)",
        "ambient": "[ATMOSPHERE: 1.0 ATM // CORROSIVE ALKALI // BRINE CANAL]"
    },

    # --- SPACE THEATERS (10 - 19) ---
    {
        "id": 10, "name": "HELIOS-7 ORBITAL ARRAY", "theater": "SPACE", "category": "SPACE", "gravity": 0.0,
        "desc": "Deep space truss catwalks, vacuum chasms, and glowing solar collector spires.",
        "bg_col": "make_color_rgb(4, 6, 14)", "base": "make_color_rgb(6, 10, 18)",
        "e1": "make_color_rgb(22, 38, 62)", "e2": "make_color_rgb(38, 66, 105)",
        "se": "make_color_rgb(14, 22, 36)", "sw": "make_color_rgb(8, 12, 20)",
        "ambient": "[VACUUM ZERO-G // SPACE VERNIES REQUIRED // SOLAR SPIRE]"
    },
    {
        "id": 11, "name": "ASTEROID SYNDICATE FORTRESS", "theater": "SPACE", "category": "SPACE", "gravity": 0.15,
        "desc": "Hollow lunar asteroid with molten slag drainage trenches and heavy mining drills.",
        "bg_col": "make_color_rgb(14, 8, 8)", "base": "make_color_rgb(32, 16, 14)",
        "e1": "make_color_rgb(46, 28, 24)", "e2": "make_color_rgb(68, 42, 32)",
        "se": "make_color_rgb(22, 12, 10)", "sw": "make_color_rgb(12, 8, 6)",
        "ambient": "[VACUUM LOW-G 0.15G // MOLTEN SLAG RUNOFF // REBAR BUNKER]"
    },
    {
        "id": 12, "name": "COLONY CYLINDER SHELL", "theater": "SPACE", "category": "SPACE", "gravity": 0.9,
        "desc": "Centrifugal curved interior hull grid, artificial waterways, and maglev rails.",
        "bg_col": "make_color_rgb(10, 14, 20)", "base": "make_color_rgb(24, 34, 46)",
        "e1": "make_color_rgb(40, 56, 75)", "e2": "make_color_rgb(60, 82, 108)",
        "se": "make_color_rgb(18, 26, 36)", "sw": "make_color_rgb(10, 16, 22)",
        "ambient": "[CENTRIFUGAL 0.90G // COLONY INTERIOR // ARTIFICIAL WATERWAY]"
    },
    {
        "id": 13, "name": "LUNAR REGOLITH CRATER", "theater": "SPACE", "category": "SPACE", "gravity": 0.16,
        "desc": "Low-G 0.16G fine basalt dust crater, boulder scree, and subterranean hab airlocks.",
        "bg_col": "make_color_rgb(8, 8, 12)", "base": "make_color_rgb(24, 24, 32)",
        "e1": "make_color_rgb(42, 42, 54)", "e2": "make_color_rgb(64, 64, 80)",
        "se": "make_color_rgb(18, 18, 24)", "sw": "make_color_rgb(10, 10, 14)",
        "ambient": "[VACUUM LOW-G 0.16G // LUNAR DUST // REGOLITH SCREE]"
    },
    {
        "id": 14, "name": "DERELICT FLEET GRAVEYARD", "theater": "SPACE", "category": "SPACE", "gravity": 0.0,
        "desc": "Scattered battleship hulks, sheared armor plate bridges, and cosmic void rifts.",
        "bg_col": "make_color_rgb(6, 6, 12)", "base": "make_color_rgb(16, 18, 28)",
        "e1": "make_color_rgb(32, 36, 52)", "e2": "make_color_rgb(52, 58, 82)",
        "se": "make_color_rgb(20, 22, 34)", "sw": "make_color_rgb(10, 12, 20)",
        "ambient": "[VACUUM ZERO-G // WARSHIP HULL GRAVEYARD // VOID RIFTS]"
    },
    {
        "id": 15, "name": "SPACE ELEVATOR RING TERMINAL", "theater": "SPACE", "category": "SPACE", "gravity": 0.0,
        "desc": "Geostationary circular platform, vertical tether vacuum shaft, and docking berths.",
        "bg_col": "make_color_rgb(6, 10, 16)", "base": "make_color_rgb(20, 30, 44)",
        "e1": "make_color_rgb(36, 52, 74)", "e2": "make_color_rgb(58, 80, 112)",
        "se": "make_color_rgb(22, 32, 48)", "sw": "make_color_rgb(12, 18, 28)",
        "ambient": "[GEO-ORBITAL 0.0G // ELEVATOR RING // DOCKING GANTRY]"
    },
    {
        "id": 16, "name": "COMET CORE ICE QUARRY", "theater": "SPACE", "category": "SPACE", "gravity": 0.05,
        "desc": "Micro-gravity 0.05G hydrocarbon ice spires and deep sublimation gas crevasses.",
        "bg_col": "make_color_rgb(8, 14, 20)", "base": "make_color_rgb(22, 38, 52)",
        "e1": "make_color_rgb(38, 62, 84)", "e2": "make_color_rgb(60, 92, 122)",
        "se": "make_color_rgb(20, 34, 48)", "sw": "make_color_rgb(10, 18, 28)",
        "ambient": "[MICRO-G 0.05G // HYDROCARBON ICE SPIRES // SUBLIMATION RIFT]"
    },
    {
        "id": 17, "name": "LAGRANGE-5 LOGISTICS HUB", "theater": "SPACE", "category": "SPACE", "gravity": 0.0,
        "desc": "Orbital container freight stacks, automated cargo tracks, and solar sail berths.",
        "bg_col": "make_color_rgb(8, 10, 16)", "base": "make_color_rgb(26, 32, 46)",
        "e1": "make_color_rgb(44, 54, 76)", "e2": "make_color_rgb(68, 82, 112)",
        "se": "make_color_rgb(24, 30, 44)", "sw": "make_color_rgb(12, 16, 26)",
        "ambient": "[LAGRANGE L5 0.0G // FREIGHT CONTAINER STACKS // CARGO BERTH]"
    },
    {
        "id": 18, "name": "DEEP VOID COMMS RELAY", "theater": "SPACE", "category": "SPACE", "gravity": 0.0,
        "desc": "High-gain antenna arrays, sensor dishes, cantilevered spars, and sheer void dropoffs.",
        "bg_col": "make_color_rgb(4, 5, 10)", "base": "make_color_rgb(14, 16, 26)",
        "e1": "make_color_rgb(28, 34, 52)", "e2": "make_color_rgb(48, 58, 86)",
        "se": "make_color_rgb(18, 22, 36)", "sw": "make_color_rgb(8, 10, 18)",
        "ambient": "[DEEP VOID 0.0G // SATELLITE COMMS RELAY // ANTENNA SPAR]"
    },
    {
        "id": 19, "name": "SOLAR MIRROR SWARM STATION", "theater": "SPACE", "category": "SPACE", "gravity": 0.0,
        "desc": "Gleaming gold collector baffles, thermal radiator fins, and vacuum chasms.",
        "bg_col": "make_color_rgb(14, 12, 6)", "base": "make_color_rgb(36, 32, 18)",
        "e1": "make_color_rgb(58, 52, 28)", "e2": "make_color_rgb(85, 76, 42)",
        "se": "make_color_rgb(30, 26, 14)", "sw": "make_color_rgb(16, 14, 8)",
        "ambient": "[SOLAR ORBIT 0.0G // THERMAL RADIATOR BAFFLE // GOLD MIRRORS]"
    },

    # --- BENCHMARK & TEST MAPS (20 - 23) ---
    {
        "id": 20, "name": "TEST: ELEVATION BENCHMARK RANGE", "theater": "EARTH", "category": "TEST", "gravity": 1.0,
        "desc": "Tiered ziggurat staircases (Tiers 0, 1, 2, 3) to test climbing AP costs & height advantage.",
        "bg_col": "make_color_rgb(16, 20, 28)", "base": "make_color_rgb(30, 42, 58)",
        "e1": "make_color_rgb(48, 66, 90)", "e2": "make_color_rgb(72, 96, 128)",
        "se": "make_color_rgb(22, 32, 46)", "sw": "make_color_rgb(12, 18, 28)",
        "ambient": "[CALIBRATION // ELEVATION TIERS 0-3 // CARDINAL RAMPS]"
    },
    {
        "id": 21, "name": "TEST: TERRAIN STRESS RANGE", "theater": "EARTH", "category": "TEST", "gravity": 1.0,
        "desc": "6 Parallel testing lanes (Dirt, Road, Rubble, Water, Vacuum, Slag) to verify mobility formulas.",
        "bg_col": "make_color_rgb(18, 18, 22)", "base": "make_color_rgb(36, 36, 44)",
        "e1": "make_color_rgb(56, 56, 68)", "e2": "make_color_rgb(80, 80, 96)",
        "se": "make_color_rgb(26, 26, 34)", "sw": "make_color_rgb(14, 14, 20)",
        "ambient": "[CALIBRATION // 6 TERRAIN LANES // PROPULSION TEST]"
    },
    {
        "id": 22, "name": "TEST: OBSTACLE & COVER GAUNTLET", "theater": "EARTH", "category": "TEST", "gravity": 1.0,
        "desc": "Symmetrical geometric maze of light (25%) and heavy (40%) cover barriers and chokepoints.",
        "bg_col": "make_color_rgb(20, 16, 24)", "base": "make_color_rgb(40, 32, 48)",
        "e1": "make_color_rgb(62, 50, 74)", "e2": "make_color_rgb(88, 72, 104)",
        "se": "make_color_rgb(28, 22, 36)", "sw": "make_color_rgb(16, 12, 22)",
        "ambient": "[CALIBRATION // LIGHT & HEAVY COVER // CHOKEPOINT CORRIDOR]"
    },
    {
        "id": 23, "name": "TEST: DUEL ARENA PROVING GROUND", "theater": "EARTH", "category": "TEST", "gravity": 1.0,
        "desc": "Pristine level tournament platform with 4 corner pillars for clean 1v1 Super Ace duels.",
        "bg_col": "make_color_rgb(12, 22, 20)", "base": "make_color_rgb(24, 46, 42)",
        "e1": "make_color_rgb(38, 70, 64)", "e2": "make_color_rgb(56, 98, 90)",
        "se": "make_color_rgb(18, 34, 30)", "sw": "make_color_rgb(10, 20, 18)",
        "ambient": "[CALIBRATION // LEVEL 1 TOURNAMENT ARENA // 4 PILLARS]"
    }
]

print(f"Generated {len(maps_data)} map definitions.")
