/// @description obj_BattleManager Create Event
// Grand-Scale Turn-Based Isometric Tactical Combat Arena
// Strictly implements docs/17_grand_scale_isometric_combat_system.md & docs/05_tactical_combat.md

show_debug_message("[obj_BattleManager] Initializing Grand-Scale Isometric Battle System...");

// 1. Bootstrap Persistent Managers if directly testing rm_combat
if (!instance_exists(obj_GameManager)) instance_create_depth(0, 0, 0, obj_GameManager);
if (!instance_exists(obj_FactionManager)) instance_create_depth(0, 0, 0, obj_FactionManager);
if (!instance_exists(obj_BlueprintManager)) instance_create_depth(0, 0, 0, obj_BlueprintManager);
if (!instance_exists(obj_NemesisManager)) instance_create_depth(0, 0, 0, obj_NemesisManager);
if (!instance_exists(obj_AudioManager)) instance_create_depth(0, 0, 0, obj_AudioManager);
if (!instance_exists(obj_DebugManager)) instance_create_depth(0, 0, -9999, obj_DebugManager);

// Start Front Mission 90s Mecha Combat BGM
scr_audio_play_location_bgm("combat");

// 2. Combat State Machine Enums & Variables
enum COMBAT_STATE {
    PLAYER_PHASE,
    MOVE_MODE,
    TARGET_MODE,
    ATTACK_EXECUTION,
    AI_PHASE,
    AUTO_SIM,
    VICTORY_AAR,
    DEFEAT_AAR,
    NEMESIS_INCURSION,
    DEPLOYMENT_DECK
}

state = COMBAT_STATE.PLAYER_PHASE;
state_timer = 0;
turn_number = 1;
screen_shake = 0.0;
auto_combat_enabled = false;
auto_combat_timer = 0;
ai_action_timer = 0;
ai_unit_index = 0;
captured_pows = []; // Battlefield captured enemy pilot escape pods (Doc 51)

// 2b. Nemesis Drop-Pod Atmospheric Ambush Incursion (Document 19, Phase 4)
nemesis_incursion_checked = false;
nemesis_incursion_active = false;
nemesis_incursion_turn = irandom_range(3, 4);
nemesis_incursion_state = 0; // 0=Warning Siren, 1=Atmospheric Descent Streak, 2=Impact Detonation & Shockwave, 3=Comms Intercom Bark, 4=Complete
nemesis_incursion_timer = 0;

incursion_data = {
    nemesis_id: "",
    nemesis_name: "",
    callsign: "",
    faction_id: "faction_syndicate",
    preferred_chassis: "HYE-03",
    portrait_asset: spr_portrait_cruz,
    bark_dialogue: "",
    target_unit_id: "ALLIED_0",
    target_c: 10,
    target_r: 10,
    pod_altitude: 650.0,
    impact_fx_played: false
};

// Milestone 55: Mid-Battle Tactical Radio Incursion & Interactive Directives
mid_battle_incursion_triggered = false;
mid_battle_incursion_turn = 3;

trigger_mid_battle_tactical_incursion = function() {
    if (mid_battle_incursion_triggered) return;
    mid_battle_incursion_triggered = true;
    
    var _mgr = id;
    var _dirs = [
        {
            text: "1. [ORBITAL BARRAGE: 35 DMG]",
            action: method({ mgr: _mgr }, function() {
                mgr.screen_shake = 16.0;
                mgr.add_log("[TACTICAL DIRECTIVE] Flagship Orbital Kinetic Barrage struck grid! 35 AoE Damage delivered!");
                for (var u = 0; u < array_length(mgr.units); u++) {
                    if (mgr.units[u].team == "HOSTILE" && !mgr.units[u].is_destroyed) {
                        mgr.units[u].components.torso.cur = max(0, mgr.units[u].components.torso.cur - 35);
                        break;
                    }
                }
            })
        },
        {
            text: "2. [FOCUS TELEMETRY: +15% ACC]",
            action: method({ mgr: _mgr }, function() {
                mgr.add_log("[TACTICAL DIRECTIVE] Squadron Synchronized Target Lock! +15% Accuracy & +1 AP to all units!");
                for (var u = 0; u < array_length(mgr.units); u++) {
                    if (mgr.units[u].team == "ALLIED") {
                        mgr.units[u].accuracy += 15;
                        mgr.units[u].current_ap = min(mgr.units[u].max_ap, mgr.units[u].current_ap + 1);
                    }
                }
            })
        },
        {
            text: "3. [NEURO-JAM: -20% ENEMY EVA]",
            action: method({ mgr: _mgr }, function() {
                mgr.add_log("[TACTICAL DIRECTIVE] Electronic Jamming Shunt broadcast! Hostile Evasion reduced by -20%!");
                for (var u = 0; u < array_length(mgr.units); u++) {
                    if (mgr.units[u].team == "HOSTILE") {
                        mgr.units[u].evasion = max(0, mgr.units[u].evasion - 20);
                    }
                }
            })
        }
    ];
    
    scr_vn_trigger_combat_intercom(
        "Flagship Fire-Control // Combat Alert",
        spr_portrait_commander_female,
        "Commander! Enemy heavy strike wings are saturating our frequencies! Flagship fire-control is online. Select immediate combat directive!",
        9999,
        make_color_rgb(255, 180, 40),
        _dirs
    );
};

evaluate_nemesis_incursion = function() {
    var _candidate = undefined;
    var _nem_mgr = instance_exists(obj_NemesisManager) ? obj_NemesisManager : undefined;

    if (!is_undefined(_nem_mgr) && array_length(_nem_mgr.active_nemeses) > 0) {
        var _list = _nem_mgr.active_nemeses;
        var _pick_entry = _list[0];
        _candidate = _nem_mgr.get_character(_pick_entry.pilot_id);
    }

    if (is_undefined(_candidate)) {
        if (!is_undefined(_nem_mgr)) {
            _candidate = _nem_mgr.get_character("pilot_syndicate_jackal");
            if (is_undefined(_candidate)) _candidate = _nem_mgr.get_character("pilot_zaibatsu_null07");
        }
    }

    if (is_undefined(_candidate)) {
        _candidate = {
            id: "pilot_syndicate_jackal",
            name: "Jax 'Jackal' Vance",
            callsign: "JACKAL",
            faction_id: "faction_syndicate",
            preferred_chassis: "HYE-03",
            role: "Reaver Pirate Ace",
            morale: 90,
            combat_trauma_mode: "berserker_rage"
        };
    }

    // Determine target landing zone: offset 3-5 tiles from player flagship
    var _cmd_c = 10;
    var _cmd_r = 10;
    for (var u = 0; u < array_length(units); u++) {
        if (units[u].team == "ALLIED" && !units[u].is_destroyed) {
            _cmd_c = units[u].grid_c;
            _cmd_r = units[u].grid_r;
            break;
        }
    }

    var _offset_c = irandom_range(3, 5) * (choose(-1, 1));
    var _offset_r = irandom_range(3, 5) * (choose(-1, 1));
    var _land_c = clamp(_cmd_c + _offset_c, 2, grid_cols - 3);
    var _land_r = clamp(_cmd_r + _offset_r, 2, grid_rows - 3);

    incursion_data.nemesis_id = _candidate.id;
    incursion_data.nemesis_name = _candidate.name;
    incursion_data.callsign = _candidate.callsign;
    incursion_data.faction_id = _candidate[$ "current_faction_id"] ?? _candidate.faction_id;
    incursion_data.preferred_chassis = _candidate[$ "preferred_chassis"] ?? "HYE-03";
    incursion_data.target_c = _land_c;
    incursion_data.target_r = _land_r;
    incursion_data.pod_altitude = 650.0;
    incursion_data.impact_fx_played = false;

    // Resolve portrait asset
    var _port = spr_portrait_cruz;
    if (incursion_data.faction_id == "faction_terran") _port = spr_portrait_vance;
    else if (incursion_data.faction_id == "faction_colony") _port = spr_portrait_cassian;
    else if (incursion_data.faction_id == "faction_zaibatsu") _port = spr_portrait_null07;
    else if (string_pos("jackal", incursion_data.nemesis_id) > 0) _port = spr_portrait_cruz;
    incursion_data.portrait_asset = _port;

    // Contextual dialogue bark
    var _trauma = _candidate[$ "combat_trauma_mode"] ?? "";
    if (_trauma == "berserker_rage") {
        incursion_data.bark_dialogue = "You took what was mine! I don't care about Earth's treaty—your squad dies in this trench!";
    } else if (_trauma == "suicidal_charge") {
        incursion_data.bark_dialogue = "I locked my reactor override before atmospheric re-entry. We both burn together!";
    } else {
        incursion_data.bark_dialogue = "Mercenary! You thought that fusion flare took me out? I've tracked your telemetry down to this crater!";
    }

    nemesis_incursion_active = true;
    add_log("[RADAR SIREN] HIGH-VELOCITY RE-ENTRY DETECTED: Capsule impact at Grid (" + string(_land_c) + ", " + string(_land_r) + ")!");
    return true;
};

// 3. Multi-Map System: Earth & Space Theaters with Dynamic Elevation & Terrain (24 Maps)
current_map_id = 0;

map_definitions = [
    {
        id: 0,
        name: "SECTOR 4 MINING OUTPOST",
        theater: "EARTH",
        category: "EARTH",
        gravity: 1.0,
        desc: "Terraced excavation quarry with haulage roads, rock shelves, and heavy machinery.",
        bg_col: make_color_rgb(18, 14, 12),
        grid_col_base: make_color_rgb(34, 28, 22),
        grid_col_elev1: make_color_rgb(52, 44, 34),
        grid_col_elev2: make_color_rgb(72, 62, 48),
        cliff_col_se: make_color_rgb(26, 20, 16),
        cliff_col_sw: make_color_rgb(16, 12, 10),
        ambient_tag: "[ATMOSPHERE: 1.0 ATM // GRAVITY: 1.0G // EARTH QUARRY]"
    },
    {
        id: 1,
        name: "NEO-VERONA COASTAL RUINS",
        theater: "EARTH",
        category: "EARTH",
        gravity: 1.0,
        desc: "Sunken highway overpasses, deep seawater canals, and concrete seawall redoubts.",
        bg_col: make_color_rgb(8, 18, 26),
        grid_col_base: make_color_rgb(14, 38, 52),
        grid_col_elev1: make_color_rgb(28, 54, 66),
        grid_col_elev2: make_color_rgb(46, 76, 88),
        cliff_col_se: make_color_rgb(10, 26, 36),
        cliff_col_sw: make_color_rgb(6, 16, 22),
        ambient_tag: "[ATMOSPHERE: 1.0 ATM // COASTAL SEAWALL // WATER CANALS]"
    },
    {
        id: 2,
        name: "VOLCANIC CALDERA RIDGE",
        theater: "EARTH",
        category: "EARTH",
        gravity: 1.0,
        desc: "Molten slag channels, obsidian basalt plateaus, and sulfur geothermal vents.",
        bg_col: make_color_rgb(24, 10, 8),
        grid_col_base: make_color_rgb(42, 22, 18),
        grid_col_elev1: make_color_rgb(64, 32, 24),
        grid_col_elev2: make_color_rgb(88, 45, 30),
        cliff_col_se: make_color_rgb(32, 14, 10),
        cliff_col_sw: make_color_rgb(18, 8, 6),
        ambient_tag: "[ATMOSPHERE: 1.0 ATM // MOLTEN SLAG RUNOFF // BASALT RIDGE]"
    },
    {
        id: 3,
        name: "GLACIAL CREVASSE PASS",
        theater: "EARTH",
        category: "EARTH",
        gravity: 1.0,
        desc: "Frozen tundra ice, bottomless glacial chasms, and slippery pack-ice bridges.",
        bg_col: make_color_rgb(12, 20, 28),
        grid_col_base: make_color_rgb(28, 48, 65),
        grid_col_elev1: make_color_rgb(45, 72, 95),
        grid_col_elev2: make_color_rgb(70, 105, 135),
        cliff_col_se: make_color_rgb(20, 35, 48),
        cliff_col_sw: make_color_rgb(12, 22, 32),
        ambient_tag: "[ATMOSPHERE: 1.0 ATM // SUB-ZERO BLIZZARD // GLACIAL CREVASSE]"
    },
    {
        id: 4,
        name: "VERDANT JUNGLE DELTA",
        theater: "EARTH",
        category: "EARTH",
        gravity: 1.0,
        desc: "Winding tropical river basins, submerged mangrove mud, and karst limestone bluffs.",
        bg_col: make_color_rgb(10, 18, 12),
        grid_col_base: make_color_rgb(22, 42, 24),
        grid_col_elev1: make_color_rgb(36, 62, 38),
        grid_col_elev2: make_color_rgb(52, 85, 54),
        cliff_col_se: make_color_rgb(16, 30, 18),
        cliff_col_sw: make_color_rgb(10, 18, 12),
        ambient_tag: "[ATMOSPHERE: 1.0 ATM // TROPICAL CANOPY // RIVER DELTA]"
    },
    {
        id: 5,
        name: "SAHARA DUNE REFINERY",
        theater: "EARTH",
        category: "EARTH",
        gravity: 1.0,
        desc: "Crushed sandstone flats, heavy industrial oil pipelines, and elevated extraction derricks.",
        bg_col: make_color_rgb(24, 18, 10),
        grid_col_base: make_color_rgb(50, 38, 22),
        grid_col_elev1: make_color_rgb(75, 58, 35),
        grid_col_elev2: make_color_rgb(105, 82, 50),
        cliff_col_se: make_color_rgb(38, 28, 16),
        cliff_col_sw: make_color_rgb(22, 16, 10),
        ambient_tag: "[ATMOSPHERE: 1.0 ATM // SANDSTORM HAZE // PIPELINE CORRIDOR]"
    },
    {
        id: 6,
        name: "MEGA-CITY SECTOR 9 GRID",
        theater: "EARTH",
        category: "EARTH",
        gravity: 1.0,
        desc: "Urban skyscraper foundations, wide concrete avenues, and collapsed overpass debris.",
        bg_col: make_color_rgb(14, 16, 20),
        grid_col_base: make_color_rgb(30, 35, 44),
        grid_col_elev1: make_color_rgb(48, 55, 68),
        grid_col_elev2: make_color_rgb(70, 80, 98),
        cliff_col_se: make_color_rgb(22, 26, 34),
        cliff_col_sw: make_color_rgb(14, 16, 22),
        ambient_tag: "[ATMOSPHERE: 1.0 ATM // HIGH-RISE DOWNTOWN // METROPOLITAN GRID]"
    },
    {
        id: 7,
        name: "SUBTERRANEAN MAGMA VAULT",
        theater: "EARTH",
        category: "EARTH",
        gravity: 1.0,
        desc: "Underground crust geothermal facility with glowing slag rivers and titanium bridges.",
        bg_col: make_color_rgb(20, 8, 6),
        grid_col_base: make_color_rgb(38, 18, 14),
        grid_col_elev1: make_color_rgb(58, 28, 22),
        grid_col_elev2: make_color_rgb(82, 40, 30),
        cliff_col_se: make_color_rgb(28, 12, 10),
        cliff_col_sw: make_color_rgb(16, 8, 6),
        ambient_tag: "[SUB-CRUST CHAMBER // GEOTHERMAL DRILL // MAGMA TRENCH]"
    },
    {
        id: 8,
        name: "ABANDONED SPACEPORT TERMINAL",
        theater: "EARTH",
        category: "EARTH",
        gravity: 1.0,
        desc: "Blast-scored aerospace tarmac runways, ferrocrete hangars, and gantry rail systems.",
        bg_col: make_color_rgb(16, 18, 22),
        grid_col_base: make_color_rgb(32, 38, 48),
        grid_col_elev1: make_color_rgb(50, 58, 72),
        grid_col_elev2: make_color_rgb(72, 84, 102),
        cliff_col_se: make_color_rgb(24, 28, 36),
        cliff_col_sw: make_color_rgb(14, 16, 22),
        ambient_tag: "[ATMOSPHERE: 1.0 ATM // AEROSPACE TARMAC // BLAST DEFLECTORS]"
    },
    {
        id: 9,
        name: "IRRADIATED SALT FLATS",
        theater: "EARTH",
        category: "EARTH",
        gravity: 1.0,
        desc: "Corrosive white alkali salt crust, brine drainage pools, and sunken trench bunkers.",
        bg_col: make_color_rgb(22, 20, 24),
        grid_col_base: make_color_rgb(46, 44, 52),
        grid_col_elev1: make_color_rgb(68, 66, 78),
        grid_col_elev2: make_color_rgb(94, 92, 108),
        cliff_col_se: make_color_rgb(34, 32, 40),
        cliff_col_sw: make_color_rgb(20, 18, 24),
        ambient_tag: "[ATMOSPHERE: 1.0 ATM // CORROSIVE ALKALI // BRINE CANAL]"
    },
    {
        id: 10,
        name: "HELIOS-7 ORBITAL ARRAY",
        theater: "SPACE",
        category: "SPACE",
        gravity: 0.0,
        desc: "Deep space truss catwalks, vacuum chasms, and glowing solar collector spires.",
        bg_col: make_color_rgb(4, 6, 14),
        grid_col_base: make_color_rgb(6, 10, 18),
        grid_col_elev1: make_color_rgb(22, 38, 62),
        grid_col_elev2: make_color_rgb(38, 66, 105),
        cliff_col_se: make_color_rgb(14, 22, 36),
        cliff_col_sw: make_color_rgb(8, 12, 20),
        ambient_tag: "[VACUUM ZERO-G // SPACE VERNIES REQUIRED // SOLAR SPIRE]"
    },
    {
        id: 11,
        name: "ASTEROID SYNDICATE FORTRESS",
        theater: "SPACE",
        category: "SPACE",
        gravity: 0.15,
        desc: "Hollow lunar asteroid with molten slag drainage trenches and heavy mining drills.",
        bg_col: make_color_rgb(14, 8, 8),
        grid_col_base: make_color_rgb(32, 16, 14),
        grid_col_elev1: make_color_rgb(46, 28, 24),
        grid_col_elev2: make_color_rgb(68, 42, 32),
        cliff_col_se: make_color_rgb(22, 12, 10),
        cliff_col_sw: make_color_rgb(12, 8, 6),
        ambient_tag: "[VACUUM LOW-G 0.15G // MOLTEN SLAG RUNOFF // REBAR BUNKER]"
    },
    {
        id: 12,
        name: "COLONY CYLINDER SHELL",
        theater: "SPACE",
        category: "SPACE",
        gravity: 0.9,
        desc: "Centrifugal curved interior hull grid, artificial waterways, and maglev rails.",
        bg_col: make_color_rgb(10, 14, 20),
        grid_col_base: make_color_rgb(24, 34, 46),
        grid_col_elev1: make_color_rgb(40, 56, 75),
        grid_col_elev2: make_color_rgb(60, 82, 108),
        cliff_col_se: make_color_rgb(18, 26, 36),
        cliff_col_sw: make_color_rgb(10, 16, 22),
        ambient_tag: "[CENTRIFUGAL 0.90G // COLONY INTERIOR // ARTIFICIAL WATERWAY]"
    },
    {
        id: 13,
        name: "LUNAR REGOLITH CRATER",
        theater: "SPACE",
        category: "SPACE",
        gravity: 0.16,
        desc: "Low-G 0.16G fine basalt dust crater, boulder scree, and subterranean hab airlocks.",
        bg_col: make_color_rgb(8, 8, 12),
        grid_col_base: make_color_rgb(24, 24, 32),
        grid_col_elev1: make_color_rgb(42, 42, 54),
        grid_col_elev2: make_color_rgb(64, 64, 80),
        cliff_col_se: make_color_rgb(18, 18, 24),
        cliff_col_sw: make_color_rgb(10, 10, 14),
        ambient_tag: "[VACUUM LOW-G 0.16G // LUNAR DUST // REGOLITH SCREE]"
    },
    {
        id: 14,
        name: "DERELICT FLEET GRAVEYARD",
        theater: "SPACE",
        category: "SPACE",
        gravity: 0.0,
        desc: "Scattered battleship hulks, sheared armor plate bridges, and cosmic void rifts.",
        bg_col: make_color_rgb(6, 6, 12),
        grid_col_base: make_color_rgb(16, 18, 28),
        grid_col_elev1: make_color_rgb(32, 36, 52),
        grid_col_elev2: make_color_rgb(52, 58, 82),
        cliff_col_se: make_color_rgb(20, 22, 34),
        cliff_col_sw: make_color_rgb(10, 12, 20),
        ambient_tag: "[VACUUM ZERO-G // WARSHIP HULL GRAVEYARD // VOID RIFTS]"
    },
    {
        id: 15,
        name: "SPACE ELEVATOR RING TERMINAL",
        theater: "SPACE",
        category: "SPACE",
        gravity: 0.0,
        desc: "Geostationary circular platform, vertical tether vacuum shaft, and docking berths.",
        bg_col: make_color_rgb(6, 10, 16),
        grid_col_base: make_color_rgb(20, 30, 44),
        grid_col_elev1: make_color_rgb(36, 52, 74),
        grid_col_elev2: make_color_rgb(58, 80, 112),
        cliff_col_se: make_color_rgb(22, 32, 48),
        cliff_col_sw: make_color_rgb(12, 18, 28),
        ambient_tag: "[GEO-ORBITAL 0.0G // ELEVATOR RING // DOCKING GANTRY]"
    },
    {
        id: 16,
        name: "COMET CORE ICE QUARRY",
        theater: "SPACE",
        category: "SPACE",
        gravity: 0.05,
        desc: "Micro-gravity 0.05G hydrocarbon ice spires and deep sublimation gas crevasses.",
        bg_col: make_color_rgb(8, 14, 20),
        grid_col_base: make_color_rgb(22, 38, 52),
        grid_col_elev1: make_color_rgb(38, 62, 84),
        grid_col_elev2: make_color_rgb(60, 92, 122),
        cliff_col_se: make_color_rgb(20, 34, 48),
        cliff_col_sw: make_color_rgb(10, 18, 28),
        ambient_tag: "[MICRO-G 0.05G // HYDROCARBON ICE SPIRES // SUBLIMATION RIFT]"
    },
    {
        id: 17,
        name: "LAGRANGE-5 LOGISTICS HUB",
        theater: "SPACE",
        category: "SPACE",
        gravity: 0.0,
        desc: "Orbital container freight stacks, automated cargo tracks, and solar sail berths.",
        bg_col: make_color_rgb(8, 10, 16),
        grid_col_base: make_color_rgb(26, 32, 46),
        grid_col_elev1: make_color_rgb(44, 54, 76),
        grid_col_elev2: make_color_rgb(68, 82, 112),
        cliff_col_se: make_color_rgb(24, 30, 44),
        cliff_col_sw: make_color_rgb(12, 16, 26),
        ambient_tag: "[LAGRANGE L5 0.0G // FREIGHT CONTAINER STACKS // CARGO BERTH]"
    },
    {
        id: 18,
        name: "DEEP VOID COMMS RELAY",
        theater: "SPACE",
        category: "SPACE",
        gravity: 0.0,
        desc: "High-gain antenna arrays, sensor dishes, cantilevered spars, and sheer void dropoffs.",
        bg_col: make_color_rgb(4, 5, 10),
        grid_col_base: make_color_rgb(14, 16, 26),
        grid_col_elev1: make_color_rgb(28, 34, 52),
        grid_col_elev2: make_color_rgb(48, 58, 86),
        cliff_col_se: make_color_rgb(18, 22, 36),
        cliff_col_sw: make_color_rgb(8, 10, 18),
        ambient_tag: "[DEEP VOID 0.0G // SATELLITE COMMS RELAY // ANTENNA SPAR]"
    },
    {
        id: 19,
        name: "SOLAR MIRROR SWARM STATION",
        theater: "SPACE",
        category: "SPACE",
        gravity: 0.0,
        desc: "Gleaming gold collector baffles, thermal radiator fins, and vacuum chasms.",
        bg_col: make_color_rgb(14, 12, 6),
        grid_col_base: make_color_rgb(36, 32, 18),
        grid_col_elev1: make_color_rgb(58, 52, 28),
        grid_col_elev2: make_color_rgb(85, 76, 42),
        cliff_col_se: make_color_rgb(30, 26, 14),
        cliff_col_sw: make_color_rgb(16, 14, 8),
        ambient_tag: "[SOLAR ORBIT 0.0G // THERMAL RADIATOR BAFFLE // GOLD MIRRORS]"
    },
    {
        id: 20,
        name: "TEST: ELEVATION BENCHMARK RANGE",
        theater: "EARTH",
        category: "TEST",
        gravity: 1.0,
        desc: "Tiered ziggurat staircases (Tiers 0, 1, 2, 3) to test climbing AP costs & height advantage.",
        bg_col: make_color_rgb(16, 20, 28),
        grid_col_base: make_color_rgb(30, 42, 58),
        grid_col_elev1: make_color_rgb(48, 66, 90),
        grid_col_elev2: make_color_rgb(72, 96, 128),
        cliff_col_se: make_color_rgb(22, 32, 46),
        cliff_col_sw: make_color_rgb(12, 18, 28),
        ambient_tag: "[CALIBRATION // ELEVATION TIERS 0-3 // CARDINAL RAMPS]"
    },
    {
        id: 21,
        name: "TEST: TERRAIN STRESS RANGE",
        theater: "EARTH",
        category: "TEST",
        gravity: 1.0,
        desc: "6 Parallel testing lanes (Dirt, Road, Rubble, Water, Vacuum, Slag) to verify mobility formulas.",
        bg_col: make_color_rgb(18, 18, 22),
        grid_col_base: make_color_rgb(36, 36, 44),
        grid_col_elev1: make_color_rgb(56, 56, 68),
        grid_col_elev2: make_color_rgb(80, 80, 96),
        cliff_col_se: make_color_rgb(26, 26, 34),
        cliff_col_sw: make_color_rgb(14, 14, 20),
        ambient_tag: "[CALIBRATION // 6 TERRAIN LANES // PROPULSION TEST]"
    },
    {
        id: 22,
        name: "TEST: OBSTACLE & COVER GAUNTLET",
        theater: "EARTH",
        category: "TEST",
        gravity: 1.0,
        desc: "Symmetrical geometric maze of light (25%) and heavy (40%) cover barriers and chokepoints.",
        bg_col: make_color_rgb(20, 16, 24),
        grid_col_base: make_color_rgb(40, 32, 48),
        grid_col_elev1: make_color_rgb(62, 50, 74),
        grid_col_elev2: make_color_rgb(88, 72, 104),
        cliff_col_se: make_color_rgb(28, 22, 36),
        cliff_col_sw: make_color_rgb(16, 12, 22),
        ambient_tag: "[CALIBRATION // LIGHT & HEAVY COVER // CHOKEPOINT CORRIDOR]"
    },
    {
        id: 23,
        name: "TEST: DUEL ARENA PROVING GROUND",
        theater: "EARTH",
        category: "TEST",
        gravity: 1.0,
        desc: "Pristine level tournament platform with 4 corner pillars for clean 1v1 Super Ace duels.",
        bg_col: make_color_rgb(12, 22, 20),
        grid_col_base: make_color_rgb(24, 46, 42),
        grid_col_elev1: make_color_rgb(38, 70, 64),
        grid_col_elev2: make_color_rgb(56, 98, 90),
        cliff_col_se: make_color_rgb(18, 34, 30),
        cliff_col_sw: make_color_rgb(10, 20, 18),
        ambient_tag: "[CALIBRATION // LEVEL 1 TOURNAMENT ARENA // 4 PILLARS]"
    }
];

grid_cols = 20;
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

var _target_map_id = 0;
var _combat_ctx = undefined;
if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "active_combat_context") && !is_undefined(obj_GameManager.active_combat_context)) {
    _combat_ctx = obj_GameManager.active_combat_context;
    _target_map_id = scr_territory_get_battle_map_id(_combat_ctx.sector_id);
}
load_map(_target_map_id);

if (!is_undefined(_combat_ctx)) {
    map_definitions[current_map_id].name = string_upper(_combat_ctx.sector_name) + " FRONT";
    map_definitions[current_map_id].desc = "Tactical Engagement Zone // " + _combat_ctx.subregion;
    map_definitions[current_map_id].ambient_tag = "[" + string_upper(_combat_ctx.region) + " THEATER // " + (_combat_ctx.is_invasion ? "OFFENSIVE INVASION VECTOR" : "SOVEREIGN DEFENSE PERIMETER") + " // GARRISON: " + string_upper(_combat_ctx.garrison_unit) + "]";
}

// 3b. Pre-Battle Deployment Deck & Chassis Swapping Test Chamber
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
    { id: "custom_aero", name: "Custom Stratos Striker", type: "custom_aero", move_type: "aero", default_squad: "SUPER_ACE", armor: 1900, power: 2200, speed: 820, sprite_asset: spr_ms_custom_aero_striker_idle, desc: "Aerodynamic swept-wing space vernier chassis with high-yield beam carbines." },
    { id: "ms_terran_ironclad_07", name: "GHA-07 Ironclad", type: "ms_terran_ironclad_07", move_type: "biped", default_squad: "PLATOON_3", armor: 2480, power: 12, speed: 45, sprite_asset: spr_ms_ironclad_idle, desc: "The legendary backbone of Earth defense, capable of surviving orbital bombardment." },
    { id: "ms_terran_ballista_04", name: "TH-M04 Ballista", type: "ms_terran_ballista_04", move_type: "treads", default_squad: "PLATOON_3", armor: 2350, power: 11, speed: 38, sprite_asset: spr_ms_ballista_idle, desc: "Quadruped heavy fire platform designed to saturate hostile trenches from over the horizon." },
    { id: "ms_terran_centurion_02", name: "TH-C02 Centurion", type: "ms_terran_centurion_02", move_type: "biped", default_squad: "PLATOON_3", armor: 2200, power: 14, speed: 62, sprite_asset: spr_ms_centurion_idle, desc: "Aggressive shock assault unit built to smash through perimeter gates and fortified bunkers." },
    { id: "ms_terran_trenchcoat_09", name: "TH-T09 Trenchcoat", type: "ms_terran_trenchcoat_09", move_type: "biped", default_squad: "PLATOON_3", armor: 2150, power: 10, speed: 50, sprite_asset: spr_ms_trenchcoat_idle, desc: "Specialized close-quarters brawler renowned for lethal room-clearing inside domed cities." },
    { id: "ms_terran_bulwark_03", name: "TCM-03 Bulwark", type: "ms_terran_bulwark_03", move_type: "biped", default_squad: "SUPER_ACE", armor: 1620, power: 8, speed: 38, sprite_asset: spr_ms_ironclad_idle, desc: "Early pre-war line guard with thick cast armor." },
    { id: "ms_terran_vanguard_01", name: "TCM-01 Vanguard Scout", type: "ms_terran_vanguard_01", move_type: "hover", default_squad: "SUPER_ACE", armor: 1450, power: 9, speed: 58, sprite_asset: spr_ms_ironclad_idle, desc: "Forward artillery spotter and fast border patrol." },
    { id: "ms_terran_vance_custom", name: "GHA-07C Ironclad Commander", type: "ms_terran_vance_custom", move_type: "biped", default_squad: "SUPER_ACE", armor: 2750, power: 15, speed: 48, sprite_asset: spr_ms_ironclad_idle, desc: "Personal flagship of Cmdr. Marcus Vance with enhanced comms." },
    { id: "ms_terran_firefly_05", name: "TH-F05 Firefly Flanker", type: "ms_terran_firefly_05", move_type: "biped", default_squad: "SUPER_ACE", armor: 1850, power: 13, speed: 68, sprite_asset: spr_ms_ironclad_idle, desc: "Fast skirmisher operating in flanking pincers." },
    { id: "ms_terran_ironclad_bastion_08", name: "GHA-08 Ironclad Bastion", type: "ms_terran_ironclad_bastion_08", move_type: "treads", default_squad: "SUPER_ACE", armor: 3200, power: 15, speed: 40, sprite_asset: spr_ms_ironclad_idle, desc: "Heavier evolution of the Ironclad designed to withstand naval railguns." },
    { id: "ms_terran_centurion_assault_02", name: "VHI-02 Centurion Assault", type: "ms_terran_centurion_assault_02", move_type: "biped", default_squad: "SUPER_ACE", armor: 2950, power: 18, speed: 58, sprite_asset: spr_ms_ironclad_idle, desc: "Up-armored strike chassis optimized for orbital drop breaches." },
    { id: "ms_terran_siegebreaker_01", name: "TH-S01 Siegebreaker", type: "ms_terran_siegebreaker_01", move_type: "treads", default_squad: "SUPER_ACE", armor: 3400, power: 16, speed: 32, sprite_asset: spr_ms_siegebreaker_anchor, desc: "Massive stationary bombardment mech used to reduce Jovian fortresses." },
    { id: "ms_terran_demolisher_08", name: "TH-D08 Demolisher", type: "ms_terran_demolisher_08", move_type: "biped", default_squad: "SUPER_ACE", armor: 3100, power: 14, speed: 42, sprite_asset: spr_ms_ironclad_idle, desc: "Frontline combat engineering mech equipped to clear minefields." },
    { id: "ms_terran_warhammer_03", name: "VHI-03 Warhammer Breaker", type: "ms_terran_warhammer_03", move_type: "biped", default_squad: "SUPER_ACE", armor: 3350, power: 19, speed: 54, sprite_asset: spr_ms_ironclad_idle, desc: "Fierce anti-armor stormer with quad-linked gatling cannons." },
    { id: "ms_terran_behemoth_11", name: "TCX-11 Behemoth Mk.IV", type: "ms_terran_behemoth_11", move_type: "biped", default_squad: "SUPER_ACE", armor: 4800, power: 22, speed: 35, sprite_asset: spr_ms_ironclad_idle, desc: "Colossal planetary dreadnought deploying walking battleship armor." },
    { id: "ms_terran_titan_04", name: "VHI-04 Titan Dreadnought", type: "ms_terran_titan_04", move_type: "biped", default_squad: "SUPER_ACE", armor: 4300, power: 26, speed: 52, sprite_asset: spr_ms_ironclad_idle, desc: "Mobile assault fortress leading planetary invasion armies." },
    { id: "ms_terran_paladin_03", name: "TH-P03 Paladin Heavy Escort", type: "ms_terran_paladin_03", move_type: "biped", default_squad: "SUPER_ACE", armor: 4100, power: 24, speed: 46, sprite_asset: spr_ms_ironclad_idle, desc: "Escort guardian armed with anti-missile thermal lasers." },
    { id: "ms_terran_promethean_02", name: "TH-X02 Promethean", type: "ms_terran_promethean_02", move_type: "biped", default_squad: "SUPER_ACE", armor: 4600, power: 25, speed: 42, sprite_asset: spr_ms_ironclad_idle, desc: "Experimental reactor testbed firing supercritical thermal shells." },
    { id: "ms_terran_goliath_prime_x01", name: "VHI-X01 Goliath Prime", type: "ms_terran_goliath_prime_x01", move_type: "treads", default_squad: "SUPER_ACE", armor: 5400, power: 24, speed: 32, sprite_asset: spr_ms_ironclad_idle, desc: "Terran apex X-chassis prototype capable of trampling enemy lines." },
    { id: "ms_colony_aether_01", name: "AET-01 Aether", type: "ms_colony_aether_01", move_type: "aero", default_squad: "PLATOON_3", armor: 1820, power: 16, speed: 85, sprite_asset: spr_ms_aether_idle, desc: "The graceful pride of the Jovian fleet, out-turning any kinetic war machine in vacuum." },
    { id: "ms_colony_zephyr_05", name: "JCC-Z05 Zephyr", type: "ms_colony_zephyr_05", move_type: "aero", default_squad: "PLATOON_3", armor: 1680, power: 15, speed: 92, sprite_asset: spr_ms_zephyr_idle, desc: "Electronic warfare interceptor that blankets battlefield radars in blinding static." },
    { id: "ms_colony_kepler_02", name: "JCC-K02 Kepler", type: "ms_colony_kepler_02", move_type: "hover", default_squad: "PLATOON_3", armor: 1720, power: 14, speed: 78, sprite_asset: spr_ms_kepler_idle, desc: "Precision sniper unit that destroys hostile reactors from outside visual sensor range." },
    { id: "ms_colony_oberon_08", name: "JCC-O08 Oberon", type: "ms_colony_oberon_08", move_type: "biped", default_squad: "PLATOON_3", armor: 1950, power: 17, speed: 80, sprite_asset: spr_ms_oberon_idle, desc: "Heavy fleet escort unit guarding Jovian gas tankers against pirate boarding torpedoes." },
    { id: "ms_colony_sylph_01", name: "AOD-01 Sylph Interceptor", type: "ms_colony_sylph_01", move_type: "aero", default_squad: "SUPER_ACE", armor: 1280, power: 11, speed: 88, sprite_asset: spr_ms_aether_idle, desc: "Light early patrol chassis guarding outer Jovian listening posts." },
    { id: "ms_colony_pegasus_09", name: "JCC-P09 Pegasus Courier", type: "ms_colony_pegasus_09", move_type: "aero", default_squad: "SUPER_ACE", armor: 1320, power: 12, speed: 95, sprite_asset: spr_ms_zephyr_idle, desc: "Extremely fast courier ship used to bypass planetary embargo lines." },
    { id: "ms_colony_cassian_custom", name: "AET-01C Aether Officer", type: "ms_colony_cassian_custom", move_type: "aero", default_squad: "SUPER_ACE", armor: 2100, power: 18, speed: 88, sprite_asset: spr_ms_aether_idle, desc: "Gold-trimmed flagship of Capt. Cassian Vane with advanced tactical battle-mapping." },
    { id: "ms_colony_vector_04", name: "JCC-V04 Vector", type: "ms_colony_vector_04", move_type: "aero", default_squad: "SUPER_ACE", armor: 1880, power: 15, speed: 86, sprite_asset: spr_ms_aether_idle, desc: "Standard carrier-based vacuum superiority fighter of the Jovian navy." },
    { id: "ms_colony_aether_striker_02", name: "AOD-02 Aether Striker", type: "ms_colony_aether_striker_02", move_type: "aero", default_squad: "SUPER_ACE", armor: 2250, power: 19, speed: 90, sprite_asset: spr_ms_aether_idle, desc: "Enhanced strike model with high-power capacitor discharges." },
    { id: "ms_colony_helios_06", name: "JCC-H06 Helios Beam", type: "ms_colony_helios_06", move_type: "aero", default_squad: "SUPER_ACE", armor: 2150, power: 18, speed: 86, sprite_asset: spr_ms_aether_idle, desc: "Specialized in sustained energy fire with enormous cooling radiator arrays." },
    { id: "ms_colony_eclipse_07", name: "JCC-E07 Eclipse Stealth", type: "ms_colony_eclipse_07", move_type: "hover", default_squad: "SUPER_ACE", armor: 1980, power: 17, speed: 92, sprite_asset: spr_ms_zephyr_idle, desc: "Deep space stealth unit running completely silent on thermal heat sinks." },
    { id: "ms_colony_nebula_03", name: "JCC-N03 Nebula Minelayer", type: "ms_colony_nebula_03", move_type: "biped", default_squad: "SUPER_ACE", armor: 2300, power: 18, speed: 76, sprite_asset: spr_ms_aether_idle, desc: "Deploys vast minefields of homing smart-mines across orbital choke-points." },
    { id: "ms_colony_seraphim_03", name: "AOD-03 Seraphim Apex", type: "ms_colony_seraphim_03", move_type: "aero", default_squad: "SUPER_ACE", armor: 2700, power: 22, speed: 94, sprite_asset: spr_ms_aether_idle, desc: "Elite ace unit equipped with shimmering hexagonal beam shield wings." },
    { id: "ms_colony_archangel_04", name: "AOD-04 Archangel Dreadnought", type: "ms_colony_archangel_04", move_type: "biped", default_squad: "SUPER_ACE", armor: 3800, power: 26, speed: 84, sprite_asset: spr_ms_aether_idle, desc: "Massive orbital dreadnought commanding colonial fleet defense." },
    { id: "ms_colony_typhon_01", name: "JCC-T01 Typhon Missile Frigate", type: "ms_colony_typhon_01", move_type: "biped", default_squad: "SUPER_ACE", armor: 3950, power: 25, speed: 78, sprite_asset: spr_ms_aether_idle, desc: "Walking missile frigate capable of launching 96 smart warheads per salvo." },
    { id: "ms_colony_chronos_03", name: "JCC-X03 Chronos Drive", type: "ms_colony_chronos_03", move_type: "biped", default_squad: "SUPER_ACE", armor: 3600, power: 27, speed: 98, sprite_asset: spr_ms_zephyr_idle, desc: "Prototype equipped with experimental tachyon verniers enabling instant micro-hops." },
    { id: "ms_colony_ghost_mirage_x08", name: "JCC-X08 Ghost Mirage", type: "ms_colony_ghost_mirage_x08", move_type: "biped", default_squad: "SUPER_ACE", armor: 3500, power: 28, speed: 100, sprite_asset: spr_ms_zephyr_idle, desc: "Masterwork custom unit piloted by Sorren Lin, producing radar holograms." },
    { id: "ms_colony_astraea_dominus_x01", name: "AOD-X01 Astraea Dominus", type: "ms_colony_astraea_dominus_x01", move_type: "aero", default_squad: "SUPER_ACE", armor: 4100, power: 28, speed: 96, sprite_asset: spr_ms_aether_idle, desc: "Colonial pinnacle unit wielding miniature fusion particle blades." },
    { id: "ms_syndicate_hyena_12", name: "SCR-12 Hyena", type: "ms_syndicate_hyena_12", move_type: "biped", default_squad: "PLATOON_3", armor: 1980, power: 10, speed: 60, sprite_asset: spr_ms_hyena_idle, desc: "Built from cannibalized military wrecks, the Hyena drags enemy suits into brutal melee." },
    { id: "ms_syndicate_gorgon_04", name: "ARC-G04 Gorgon", type: "ms_syndicate_gorgon_04", move_type: "biped", default_squad: "PLATOON_3", armor: 2300, power: 12, speed: 52, sprite_asset: spr_ms_gorgon_idle, desc: "Feared asteroid boarding mech designed to breach titanium bulkheads and crush reactors." },
    { id: "ms_syndicate_bloodhound_06", name: "ARC-B06 Bloodhound", type: "ms_syndicate_bloodhound_06", move_type: "biped", default_squad: "PLATOON_3", armor: 1850, power: 9, speed: 72, sprite_asset: spr_ms_bloodhound_idle, desc: "Fast wheeled marauder that hunts in packs to ambush isolated military convoys." },
    { id: "ms_syndicate_vandal_03", name: "ARC-V03 Vandal", type: "ms_syndicate_vandal_03", move_type: "biped", default_squad: "PLATOON_3", armor: 1750, power: 10, speed: 66, sprite_asset: spr_ms_vandal_idle, desc: "Guerilla ambush unit that blankets the area in blinding magnesium flares." },
    { id: "ms_syndicate_scrapper_01", name: "RST-01 Scrapper Grunt", type: "ms_syndicate_scrapper_01", move_type: "biped", default_squad: "SUPER_ACE", armor: 1350, power: 7, speed: 54, sprite_asset: spr_ms_hyena_idle, desc: "Rudimentary combat walker patched together from industrial loaders." },
    { id: "ms_syndicate_hellhound_02", name: "ARC-H02 Hellhound Flamer", type: "ms_syndicate_hellhound_02", move_type: "biped", default_squad: "SUPER_ACE", armor: 1650, power: 9, speed: 58, sprite_asset: spr_ms_hyena_idle, desc: "Terror weapon spraying superheated napalm over infantry bunkers." },
    { id: "ms_syndicate_cruz_custom", name: "SCR-12C Hyena Warlord", type: "ms_syndicate_cruz_custom", move_type: "biped", default_squad: "SUPER_ACE", armor: 2550, power: 14, speed: 64, sprite_asset: spr_ms_hyena_idle, desc: "Battle-scarred command rig of Sonya Cruz, clad in the armor of defeated Terran aces." },
    { id: "ms_syndicate_jackal_08", name: "ARC-J08 Jackal Skirmisher", type: "ms_syndicate_jackal_08", move_type: "aero", default_squad: "SUPER_ACE", armor: 1920, power: 11, speed: 70, sprite_asset: spr_ms_hyena_idle, desc: "Aggressive skirmisher operated by seasoned mercenary contractors." },
    { id: "ms_syndicate_marauder_02", name: "RST-02 Marauder Brawler", type: "ms_syndicate_marauder_02", move_type: "biped", default_squad: "SUPER_ACE", armor: 2650, power: 13, speed: 56, sprite_asset: spr_ms_hyena_idle, desc: "Brutal brawler capable of withstanding direct missile hits." },
    { id: "ms_syndicate_warthog_05", name: "ARC-W05 Warthog Siege", type: "ms_syndicate_warthog_05", move_type: "treads", default_squad: "SUPER_ACE", armor: 2950, power: 12, speed: 42, sprite_asset: spr_ms_gorgon_idle, desc: "Fires dense balls of molten industrial slag over fortress battlements." },
    { id: "ms_syndicate_ripper_07", name: "ARC-R07 Ripper Melee", type: "ms_syndicate_ripper_07", move_type: "biped", default_squad: "SUPER_ACE", armor: 2450, power: 15, speed: 68, sprite_asset: spr_ms_bloodhound_idle, desc: "Close-combat terror machine with twin industrial circular saws." },
    { id: "ms_syndicate_scythe_09", name: "ARC-S09 Scythe Infiltrator", type: "ms_syndicate_scythe_09", move_type: "biped", default_squad: "SUPER_ACE", armor: 2150, power: 14, speed: 76, sprite_asset: spr_ms_hyena_idle, desc: "Silent assassin utilizing monofilament wire to sever limbs in ambushes." },
    { id: "ms_syndicate_slag_lobber_03", name: "RST-03 Slag Lobber", type: "ms_syndicate_slag_lobber_03", move_type: "biped", default_squad: "SUPER_ACE", armor: 2800, power: 14, speed: 48, sprite_asset: spr_ms_gorgon_idle, desc: "Covers the battlefield in sticky, blinding slag that overheats enemy vents." },
    { id: "ms_syndicate_junker_dread_04", name: "RST-04 Junker Dreadnought", type: "ms_syndicate_junker_dread_04", move_type: "treads", default_squad: "SUPER_ACE", armor: 4200, power: 20, speed: 44, sprite_asset: spr_ms_gorgon_idle, desc: "Walking scrapyard monstrosity equipped with guns salvaged from downed warships." },
    { id: "ms_syndicate_chimera_01", name: "ARC-C01 Chimera Vanguard", type: "ms_syndicate_chimera_01", move_type: "biped", default_squad: "SUPER_ACE", armor: 3800, power: 22, speed: 65, sprite_asset: spr_ms_hyena_idle, desc: "High-end mercenary flagship combining the finest military components on the black market." },
    { id: "ms_syndicate_cerberus_04", name: "ARC-X04 Cerberus Triple-Head", type: "ms_syndicate_cerberus_04", move_type: "biped", default_squad: "SUPER_ACE", armor: 4100, power: 21, speed: 54, sprite_asset: spr_ms_gorgon_idle, desc: "Terrifying three-turret assault mech capable of engaging multiple targets." },
    { id: "ms_syndicate_iron_reaver_09", name: "ARC-X09 Iron Reaver", type: "ms_syndicate_iron_reaver_09", move_type: "biped", default_squad: "SUPER_ACE", armor: 4350, power: 23, speed: 60, sprite_asset: spr_ms_gorgon_idle, desc: "The supreme flagship of pirate armadas, devastating any suit it tackles." },
    { id: "ms_syndicate_rust_devil_x01", name: "RST-X01 Rust Devil Prime", type: "ms_syndicate_rust_devil_x01", move_type: "biped", default_squad: "SUPER_ACE", armor: 4700, power: 24, speed: 52, sprite_asset: spr_ms_gorgon_idle, desc: "Legendary prototype chassis welded together by insane pirate foundry masters." },
    { id: "ms_zaibatsu_muramasa_03", name: "ZAI-03 Muramasa", type: "ms_zaibatsu_muramasa_03", move_type: "biped", default_squad: "PLATOON_3", armor: 1950, power: 14, speed: 82, sprite_asset: spr_ms_muramasa_idle, desc: "Surgical dueling mech interfaced directly into the pilot's spinal cord via cyber-implants." },
    { id: "ms_zaibatsu_kage_07", name: "ZBT-K07 Kage", type: "ms_zaibatsu_kage_07", move_type: "biped", default_squad: "PLATOON_3", armor: 1650, power: 13, speed: 88, sprite_asset: spr_ms_kage_idle, desc: "Stealth assassin chassis that bends light around its hull to vanish in open daylight." },
    { id: "ms_zaibatsu_ronin_04", name: "ZBT-R04 Ronin", type: "ms_zaibatsu_ronin_04", move_type: "biped", default_squad: "PLATOON_3", armor: 2100, power: 16, speed: 75, sprite_asset: spr_ms_ronin_idle, desc: "Coordinates autonomous AI sub-drones that harass enemy flanks with synchronized laser fire." },
    { id: "ms_zaibatsu_tessen_09", name: "ZBT-T09 Tessen", type: "ms_zaibatsu_tessen_09", move_type: "biped", default_squad: "PLATOON_3", armor: 1820, power: 15, speed: 78, sprite_asset: spr_ms_tessen_idle, desc: "Fires concentrated EMP pulses that fry enemy targeting computers and freeze joint hydraulics." },
    { id: "ms_zaibatsu_shinobi_01", name: "HATS-01 Shinobi Recon", type: "ms_zaibatsu_shinobi_01", move_type: "hover", default_squad: "SUPER_ACE", armor: 1380, power: 10, speed: 84, sprite_asset: spr_ms_kage_idle, desc: "Corporate security scout deployed for industrial espionage raids." },
    { id: "ms_zaibatsu_shuriken_02", name: "ZBT-S02 Shuriken Skirmisher", type: "ms_zaibatsu_shuriken_02", move_type: "biped", default_squad: "SUPER_ACE", armor: 1520, power: 12, speed: 86, sprite_asset: spr_ms_muramasa_idle, desc: "Agile harasser equipped with high-speed micro-beam emitters." },
    { id: "ms_zaibatsu_takahashi_custom", name: "ZAI-03C Muramasa Executive", type: "ms_zaibatsu_takahashi_custom", move_type: "biped", default_squad: "SUPER_ACE", armor: 2350, power: 17, speed: 85, sprite_asset: spr_ms_muramasa_idle, desc: "Personal masterwork of Director Renzo Takahashi with gold-etched bio-neural circuitry." },
    { id: "ms_zaibatsu_kamaitachi_03", name: "ZBT-K03 Kamaitachi Slicer", type: "ms_zaibatsu_kamaitachi_03", move_type: "aero", default_squad: "SUPER_ACE", armor: 1950, power: 15, speed: 90, sprite_asset: spr_ms_muramasa_idle, desc: "Rapid strike mech capable of eviscerating unshielded mechs in a single pass." },
    { id: "ms_zaibatsu_ronin_guardian_02", name: "HATS-02 Ronin Guardian", type: "ms_zaibatsu_ronin_guardian_02", move_type: "biped", default_squad: "SUPER_ACE", armor: 2550, power: 18, speed: 76, sprite_asset: spr_ms_muramasa_idle, desc: "Defends Zaibatsu research laboratories with heavy energy shields and autonomous drones." },
    { id: "ms_zaibatsu_oni_05", name: "ZBT-O05 Oni Heavy Assault", type: "ms_zaibatsu_oni_05", move_type: "biped", default_squad: "SUPER_ACE", armor: 3100, power: 16, speed: 62, sprite_asset: spr_ms_muramasa_idle, desc: "Terrifying heavy assault suit wielding a plasma-charged kanabo club." },
    { id: "ms_zaibatsu_bushido_01", name: "ZBT-B01 Bushido Vanguard", type: "ms_zaibatsu_bushido_01", move_type: "biped", default_squad: "SUPER_ACE", armor: 2700, power: 19, speed: 82, sprite_asset: spr_ms_muramasa_idle, desc: "Frontline vanguard unit driven by hyper-experienced cybernetically linked pilots." },
    { id: "ms_zaibatsu_fudo_08", name: "ZBT-F08 Fudo Defensive Wall", type: "ms_zaibatsu_fudo_08", move_type: "treads", default_squad: "SUPER_ACE", armor: 3300, power: 20, speed: 52, sprite_asset: spr_ms_muramasa_idle, desc: "Anchors defense lines by projecting widespread energy barriers that deflect railgun rounds." },
    { id: "ms_zaibatsu_raiden_03", name: "HATS-03 Raiden Storm", type: "ms_zaibatsu_raiden_03", move_type: "treads", default_squad: "SUPER_ACE", armor: 2850, power: 21, speed: 78, sprite_asset: spr_ms_muramasa_idle, desc: "Discharges cascading arcs of artificial lightning across multiple enemy mechs." },
    { id: "ms_zaibatsu_susanoo_04", name: "HATS-04 Susanoo Emperor", type: "ms_zaibatsu_susanoo_04", move_type: "biped", default_squad: "SUPER_ACE", armor: 4200, power: 26, speed: 80, sprite_asset: spr_ms_muramasa_idle, desc: "Supreme cybernetic war machine firing reality-tearing tachyon energy waves." },
    { id: "ms_zaibatsu_yamato_06", name: "ZBT-Y06 Yamato Beam Siege", type: "ms_zaibatsu_yamato_06", move_type: "biped", default_squad: "SUPER_ACE", armor: 4400, power: 25, speed: 60, sprite_asset: spr_ms_muramasa_idle, desc: "Walking battleship armed with long-range spinal particle beam turrets." },
    { id: "ms_zaibatsu_kusanagi_05", name: "ZBT-X05 Kusanagi Blade", type: "ms_zaibatsu_kusanagi_05", move_type: "biped", default_squad: "SUPER_ACE", armor: 3800, power: 27, speed: 92, sprite_asset: spr_ms_muramasa_idle, desc: "Piloted through complete cerebral symbiosis, mirroring human thought instantaneously." },
    { id: "ms_zaibatsu_null07_phantom_x07", name: "ZBT-X07 Null-07 Phantom", type: "ms_zaibatsu_null07_phantom_x07", move_type: "biped", default_squad: "SUPER_ACE", armor: 3650, power: 28, speed: 96, sprite_asset: spr_ms_kage_idle, desc: "Personal black-ops chassis of Null-07, capable of hacking enemy mechs mid-combat." },
    { id: "ms_zaibatsu_amaterasu_x01", name: "HATS-X01 Amaterasu Zero", type: "ms_zaibatsu_amaterasu_x01", move_type: "biped", default_squad: "SUPER_ACE", armor: 4600, power: 28, speed: 88, sprite_asset: spr_ms_muramasa_idle, desc: "Apex cybernetic prototype wielding forbidden transhumanist quantum processors." },
    { id: "bp_player_vanguard_heavy", name: "Vanguard Linebreaker [PMC Custom]", type: "bp_player_vanguard_heavy", move_type: "biped", default_squad: "SUPER_ACE", armor: 2600, power: 15, speed: 55, sprite_asset: spr_ms_ironclad_idle, desc: "Player proprietary heavy frontline chassis with modular component hardpoints." },
    { id: "bp_player_stratos_interceptor", name: "Stratos Interceptor [PMC Custom]", type: "bp_player_stratos_interceptor", move_type: "aero", default_squad: "SUPER_ACE", armor: 1950, power: 17, speed: 88, sprite_asset: spr_ms_aether_idle, desc: "Player proprietary interceptor with lightning-fast lateral evasive thrusters." },
    { id: "bp_player_scrapper_brawler", name: "Scrapper Brawler [PMC Custom]", type: "bp_player_scrapper_brawler", move_type: "biped", default_squad: "SUPER_ACE", armor: 2200, power: 12, speed: 65, sprite_asset: spr_ms_hyena_idle, desc: "Player proprietary CQB brawler designed to grapple and crush hostile armor." },
    { id: "bp_player_ghost_sniper", name: "Ghost Recon Sniper [PMC Custom]", type: "bp_player_ghost_sniper", move_type: "hover", default_squad: "SUPER_ACE", armor: 1800, power: 16, speed: 75, sprite_asset: spr_ms_kage_idle, desc: "Player proprietary sniper platform tuned for single-shot lethal cockpit assassinations." },
    { id: "ms_terran_ironclad_custom_cole", name: "GHA-07X Iron Bastion [Cole Custom]", type: "ms_terran_ironclad_custom_cole", move_type: "biped", default_squad: "SUPER_ACE", armor: 3100, power: 16, speed: 48, sprite_asset: spr_ms_ironclad_idle, desc: "Lt. Marcus Cole custom Ironclad, reinforced with doubled tungsten plates to endure close-quarters trench combat." },
    { id: "ms_terran_centurion_praetorian", name: "TH-C02P Centurion Praetorian", type: "ms_terran_centurion_praetorian", move_type: "biped", default_squad: "SUPER_ACE", armor: 2800, power: 17, speed: 66, sprite_asset: spr_ms_centurion_idle, desc: "Elite Terran Coalition guard suit deployed to escort planetary governors and spearhead armor breaches." },
    { id: "ms_terran_goliath_siege", name: "TH-G09 Goliath Heavy Howitzer", type: "ms_terran_goliath_siege", move_type: "treads", default_squad: "SUPER_ACE", armor: 4200, power: 22, speed: 32, sprite_asset: spr_ms_ballista_idle, desc: "Colossal quadruped artillery walking fortress capable of flattening entire planetary fortifications." },
    { id: "ms_terran_valkyrie_odin", name: "VHD-X02 Odin Dread-Chassis", type: "ms_terran_valkyrie_odin", move_type: "treads", default_squad: "SUPER_ACE", armor: 4600, power: 26, speed: 40, sprite_asset: spr_ms_titan_proto, desc: "Valkyrie flagship prototype walking fortress designed to withstand capital ship orbital bombardment." },
    { id: "ms_colony_aether_custom_nadia", name: "AET-01S Starlight Valkyrie [Nadia Custom]", type: "ms_colony_aether_custom_nadia", move_type: "aero", default_squad: "SUPER_ACE", armor: 2450, power: 20, speed: 98, sprite_asset: spr_ms_aether_idle, desc: "Commander Nadia Cruz tuned Aether, fitted with high-efficiency Cherenkov beam carbines and auxiliary verniers." },
    { id: "ms_colony_zephyr_custom_dahl", name: "JCC-Z05X Ghost Zephyr [Dahl Custom]", type: "ms_colony_zephyr_custom_dahl", move_type: "hover", default_squad: "SUPER_ACE", armor: 2150, power: 18, speed: 102, sprite_asset: spr_ms_zephyr_idle, desc: "Kira Dahl personal reconnaissance machine, capable of vanishing completely from military radar grids." },
    { id: "ms_colony_helios_archon", name: "HOF-X01 Helios Archon", type: "ms_colony_helios_archon", move_type: "aero", default_squad: "SUPER_ACE", armor: 3400, power: 25, speed: 92, sprite_asset: spr_ms_oberon_idle, desc: "High-orbital skirmisher drawing power directly from concentrated solar collection arrays." },
    { id: "ms_colony_selene_interceptor", name: "HOF-X02 Selene Interceptor", type: "ms_colony_selene_interceptor", move_type: "aero", default_squad: "SUPER_ACE", armor: 3100, power: 27, speed: 110, sprite_asset: spr_ms_kepler_idle, desc: "Ultra-fast interceptor built for deep-space fleet interception at interplanetary velocity." },
    { id: "ms_syndicate_hyena_custom_vance", name: "SCR-12R Jackal King [Vance Custom]", type: "ms_syndicate_hyena_custom_vance", move_type: "biped", default_squad: "SUPER_ACE", armor: 2750, power: 15, speed: 74, sprite_asset: spr_ms_hyena_idle, desc: "Jax Vance flagship war machine, adorned with skulls and reinforced with armor ripped from federal cruisers." },
    { id: "ms_syndicate_gorgon_custom_scrapper", name: "ARC-G04X Titan Crusher [Guild Master Custom]", type: "ms_syndicate_gorgon_custom_scrapper", move_type: "biped", default_squad: "SUPER_ACE", armor: 3300, power: 16, speed: 56, sprite_asset: spr_ms_gorgon_idle, desc: "Custom masterwork of the Syndicate Scrap-Masters, capable of punching through starship airlocks in seconds." },
    { id: "ms_syndicate_scrap_chimera", name: "AJS-X01 Scrap Chimera", type: "ms_syndicate_scrap_chimera", move_type: "biped", default_squad: "SUPER_ACE", armor: 4400, power: 20, speed: 48, sprite_asset: spr_ms_bloodhound_idle, desc: "Monstrous 4-armed war machine assembled from parts of four different destroyed faction chassis." },
    { id: "ms_syndicate_rust_behemoth", name: "AJS-X02 Rust Behemoth", type: "ms_syndicate_rust_behemoth", move_type: "biped", default_squad: "SUPER_ACE", armor: 5000, power: 22, speed: 35, sprite_asset: spr_ms_vandal_idle, desc: "Massive walking scrap fortress with firepower equivalent to an armored cruiser broadside." },
    { id: "ms_zaibatsu_muramasa_custom_renzo", name: "ZAI-03X Oni-Blade [Renzo Custom]", type: "ms_zaibatsu_muramasa_custom_renzo", move_type: "biped", default_squad: "SUPER_ACE", armor: 2900, power: 22, speed: 90, sprite_asset: spr_ms_muramasa_idle, desc: "Renzo Takahashi supreme dueling mobile suit with neural nanite repair weave and dual high-frequency blades." },
    { id: "ms_zaibatsu_kage_custom_null07", name: "ZBT-K07X Void Shinobi [Null-07 Custom]", type: "ms_zaibatsu_kage_custom_null07", move_type: "biped", default_squad: "SUPER_ACE", armor: 2600, power: 24, speed: 105, sprite_asset: spr_ms_kage_idle, desc: "Master assassin chassis piloted by Null-07, capable of turning completely invisible before striking." },
    { id: "ms_zaibatsu_ronin_master", name: "ZBT-R04M Ronin Shogun", type: "ms_zaibatsu_ronin_master", move_type: "biped", default_squad: "SUPER_ACE", armor: 3600, power: 26, speed: 80, sprite_asset: spr_ms_ronin_idle, desc: "Command carrier coordinating six autonomous combat sub-drones while wielding dual plasma naginatas." },
    { id: "ms_zaibatsu_tessen_empress", name: "ZBT-T09E Tessen Empress", type: "ms_zaibatsu_tessen_empress", move_type: "biped", default_squad: "SUPER_ACE", armor: 3200, power: 27, speed: 88, sprite_asset: spr_ms_tessen_idle, desc: "Apex electronic warfare mecha capable of shutting down entire battlegroups with directed EMP pulse waves." },
    { id: "ms_prewar_hephaestus_avatar", name: "Pre-War Hephaestus Sentinel", type: "ms_prewar_hephaestus_avatar", move_type: "biped", default_squad: "SUPER_ACE", armor: 4800, power: 28, speed: 70, sprite_asset: spr_ms_hephaestus_avatar, desc: "Autonomous defense mecha discovered slumbering in the reactor depths of the dreadnought Hephaestus." },
    { id: "ms_prewar_chronos_proto", name: "Pre-War Chronos Vector", type: "ms_prewar_chronos_proto", move_type: "aero", default_squad: "SUPER_ACE", armor: 4100, power: 27, speed: 95, sprite_asset: spr_ms_hephaestus_avatar, desc: "Pre-war prototype harnessing compressed tachyon fields for near-instantaneous evasive maneuvers." },
    { id: "ms_valkyrie_titan_juggernaut", name: "VHD-X01 Juggernaut Prime", type: "ms_valkyrie_titan_juggernaut", move_type: "treads", default_squad: "SUPER_ACE", armor: 5200, power: 26, speed: 36, sprite_asset: spr_ms_titan_proto, desc: "Terrifying 100-ton superheavy walking fortress armed with quad synchronized 140mm autocannons." },
    { id: "ms_rebel_partisan_guerilla", name: "Frontier Militia Partisan", type: "ms_rebel_partisan_guerilla", move_type: "biped", default_squad: "SUPER_ACE", armor: 1650, power: 10, speed: 64, sprite_asset: spr_ms_vandal_idle, desc: "Industrial mining mobile suit modified with heavy rock-cutters to fight corporate security forces." },
    { id: "ms_rebel_partisan_striker", name: "Frontier Vanguard Striker", type: "ms_rebel_partisan_striker", move_type: "aero", default_squad: "SUPER_ACE", armor: 1720, power: 11, speed: 70, sprite_asset: spr_ms_bloodhound_idle, desc: "Frontier insurgent machine built from converted ore haulers, armed with jury-rigged mining rockets." },
    { id: "ms_pirate_corsair_marauder", name: "Outer Ring Corsair Marauder", type: "ms_pirate_corsair_marauder", move_type: "biped", default_squad: "SUPER_ACE", armor: 2300, power: 14, speed: 78, sprite_asset: spr_ms_hyena_idle, desc: "Notorious pirate boarding machine designed to pierce freighter hulls and harvest element cargo." },
    { id: "ms_ancient_derelict_sentry", name: "Precursor Derelict Sentry-00", type: "ms_ancient_derelict_sentry", move_type: "biped", default_squad: "SUPER_ACE", armor: 3200, power: 19, speed: 72, sprite_asset: spr_ms_oberon_idle, desc: "Mysterious autonomous sentry recovered from an uncharted deep-space derelict station." },
    { id: "ms_apex_apocalypse_harvester", name: "Apex Apocalypse Harvester", type: "ms_apex_apocalypse_harvester", move_type: "treads", default_squad: "SUPER_ACE", armor: 5500, power: 30, speed: 42, sprite_asset: spr_ms_titan_proto, desc: "Apocalyptic super-weapon mecha created by unshackled bio-neural research, capable of harvesting planetary crusts." }
];

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

// 4. Isometric Camera & Viewport Controls
cam_x = 683.0;
cam_y = 120.0;
cam_target_x = 683.0;
cam_target_y = 120.0;
zoom = 0.85;
zoom_target = 0.85;

is_dragging = false;
drag_start_mx = 0;
drag_start_my = 0;
drag_start_cam_x = 0;
drag_start_cam_y = 0;

// Mouse Grid Cursor
hover_c = -1;
hover_r = -1;
selected_weapon = 0;
valid_move_tiles = [];
valid_target_tiles = [];

// 5. Platoon Battlegroups & Mobile Suit Rosters
units = [];
selected_unit_idx = 0;
target_unit_idx = -1;

// Helper: Create Front Mission Component Set
create_components = function(_torso_hp, _arm_hp, _leg_hp, _head_hp, _pack_hp, _armor) {
    return {
        torso:    { name: "Torso Core",       cur: _torso_hp, max: _torso_hp, armor: _armor, intact: true },
        head:     { name: "Sensor Array",     cur: _head_hp,  max: _head_hp,  armor: floor(_armor * 0.7), intact: true },
        arm_left: { name: "Left Weapon Arm",  cur: _arm_hp,   max: _arm_hp,   armor: _armor, intact: true },
        arm_right:{ name: "Right Weapon Arm", cur: _arm_hp,   max: _arm_hp,   armor: _armor, intact: true },
        legs:     { name: "Hydraulic Limbs",  cur: _leg_hp,   max: _leg_hp,   armor: _armor, intact: true },
        backpack: { name: "Vernier Pack",     cur: _pack_hp,  max: _pack_hp,  armor: floor(_armor * 0.6), intact: true }
    };
};
var _create_components = create_components;

// --- ALLIED / PLAYER PMC BATTLEGROUP (8 Units) ---
// 1. Alpha-01: Commander Unit (Player Heavy Ironclad)
array_push(units, {
    id: "ALLIED_0",
    callsign: "Alpha-01 'WARHAMMER'",
    pilot_name: "Commander Vance",
    team: "ALLIED",
    mech_type: "ironclad",
    grid_c: 3, grid_r: 4, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 0,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 100.0, heat_dissipation: 35.0,
    accuracy: 82, evasion: 48, braced: false,
    components: _create_components(680, 420, 620, 180, 240, 32),
    weapons: [
        { name: "Type-77 120mm Cannon", short_name: "120MM CANNON", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 15, range_min: 1, range_max: 6, damage: 165, anim_state: "fire_rifle", desc: "Kinetic solid-slug with high penetration arc." },
        { name: "GAU-88 Heavy Vulcan", short_name: "GAU-88 VULCAN", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 4, damage: 85, anim_state: "fire_chaingun", desc: "Rapid tracer bullet stream." },
        { name: "Ares Swarm-16 Missiles", short_name: "SWARM-16", proj_type: "MICRO_MISSILE", ap_cost: 4, heat_cost: 22, range_min: 2, range_max: 7, damage: 195, anim_state: "fire_missiles", desc: "Parabolic micro-missile saturation volley." },
        { name: "Gun-Club Strike", short_name: "MELEE BASH", proj_type: "MELEE", ap_cost: 3, heat_cost: 8, range_min: 1, range_max: 1, damage: 210, anim_state: "melee", desc: "Heavy hydraulic smash in close combat." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(180, 220, 255),
    is_destroyed: false
});

// 2. Alpha-02: Colony Interceptor (AET-01 Aether)
array_push(units, {
    id: "ALLIED_1",
    callsign: "Alpha-02 'VALKYRIE'",
    pilot_name: "Lt. Sonya Cruz",
    team: "ALLIED",
    mech_type: "aether",
    grid_c: 2, grid_r: 5, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 0,
    max_ap: 7, current_ap: 7,
    current_heat: 0.0, max_heat: 90.0, heat_dissipation: 40.0,
    accuracy: 88, evasion: 68, braced: false,
    components: _create_components(490, 310, 440, 160, 220, 22),
    weapons: [
        { name: "Coherent Beam Pulse Rifle", short_name: "BEAM RIFLE", proj_type: "BEAM_PULSE", ap_cost: 3, heat_cost: 20, range_min: 1, range_max: 7, damage: 180, anim_state: "fire_beam", desc: "High-intensity focused laser pulse." },
        { name: "High-Frequency Beam Saber", short_name: "BEAM SABER", proj_type: "MELEE", ap_cost: 2, heat_cost: 12, range_min: 1, range_max: 1, damage: 190, anim_state: "melee", desc: "Thermal plasma blade slash." },
        { name: "Ares Micro-Missile Pod", short_name: "POD MISSILES", proj_type: "MICRO_MISSILE", ap_cost: 3, heat_cost: 18, range_min: 2, range_max: 6, damage: 140, anim_state: "fire_missiles", desc: "Lightweight homing cluster." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(160, 235, 255),
    is_destroyed: false
});

// 3. Alpha-03: Zaibatsu High-Mobility Striker (Muramasa Prototype)
array_push(units, {
    id: "ALLIED_2",
    callsign: "Alpha-03 'KUSANAGI'",
    pilot_name: "Operative Ren",
    team: "ALLIED",
    mech_type: "muramasa",
    grid_c: 4, grid_r: 2, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 1,
    max_ap: 8, current_ap: 8,
    current_heat: 0.0, max_heat: 85.0, heat_dissipation: 35.0,
    accuracy: 85, evasion: 75, braced: false,
    components: _create_components(440, 280, 420, 150, 200, 18),
    weapons: [
        { name: "Muramasa Plasma Katana", short_name: "PLASMA BLADE", proj_type: "MELEE", ap_cost: 3, heat_cost: 14, range_min: 1, range_max: 1, damage: 240, anim_state: "melee", desc: "Monofilament thermal blade." },
        { name: "Dual Plasma Cannons", short_name: "PLASMA CANNON", proj_type: "RAILGUN_SLUG", ap_cost: 4, heat_cost: 28, range_min: 1, range_max: 5, damage: 205, anim_state: "fire_plasma", desc: "Twin magnetic containment bursts." },
        { name: "Rotary Vulcan Harass", short_name: "VULCAN", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 8, range_min: 1, range_max: 3, damage: 75, anim_state: "fire_chaingun", desc: "Point-defense deterrent." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.20,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(200, 200, 255),
    is_destroyed: false
});

// 4. Alpha-04: Terran Heavy Artillery (Siegebreaker Tank Chassis)
array_push(units, {
    id: "ALLIED_3",
    callsign: "Alpha-04 'SIEGEBREAKER'",
    pilot_name: "Gunner Miller",
    team: "ALLIED",
    mech_type: "siegebreaker",
    grid_c: 1, grid_r: 2, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 0,
    max_ap: 5, current_ap: 5,
    current_heat: 0.0, max_heat: 120.0, heat_dissipation: 28.0,
    accuracy: 90, evasion: 25, braced: true,
    components: _create_components(850, 450, 750, 220, 300, 45),
    weapons: [
        { name: "Titan 300mm Siege Railgun", short_name: "300MM RAILGUN", proj_type: "RAILGUN_SLUG", ap_cost: 4, heat_cost: 32, range_min: 3, range_max: 10, damage: 320, anim_state: "fire_siege", desc: "Ultra-high kinetic hypersonic slug." },
        { name: "Counter-Battery 120mm Shell", short_name: "120MM SOLID", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 15, range_min: 2, range_max: 7, damage: 170, anim_state: "fire_siege", desc: "Arced ballistic bombardment." },
        { name: "Defensive Flak Cannon", short_name: "DEF FLAK", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 3, damage: 90, anim_state: "fire_chaingun", desc: "Area denial shrapnel." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.12,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(220, 210, 180),
    is_destroyed: false
});

// 5. Bravo-01: Terran Coalition Line Unit (Mass Production Ironclad)
array_push(units, {
    id: "ALLIED_4",
    callsign: "Bravo-01 'BULWARK'",
    pilot_name: "Cpl. Diaz",
    team: "ALLIED",
    mech_type: "ironclad",
    grid_c: 3, grid_r: 6, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 0,
    max_ap: 5, current_ap: 5,
    current_heat: 0.0, max_heat: 100.0, heat_dissipation: 30.0,
    accuracy: 75, evasion: 42, braced: false,
    components: _create_components(620, 380, 560, 160, 210, 30),
    weapons: [
        { name: "Type-77 120mm Cannon", short_name: "120MM CANNON", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 15, range_min: 1, range_max: 6, damage: 150, anim_state: "fire_rifle", desc: "Standard issue kinetic cannon." },
        { name: "GAU-88 Heavy Vulcan", short_name: "VULCAN", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 4, damage: 80, anim_state: "fire_chaingun", desc: "Rapid fire rotary." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(170, 200, 230),
    is_destroyed: false
});

// 6. Bravo-02: Terran Coalition Heavy Line (Ironclad MP)
array_push(units, {
    id: "ALLIED_5",
    callsign: "Bravo-02 'AEGIS'",
    pilot_name: "Sgt. Kovacs",
    team: "ALLIED",
    mech_type: "ironclad",
    grid_c: 4, grid_r: 5, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 0,
    max_ap: 5, current_ap: 5,
    current_heat: 0.0, max_heat: 100.0, heat_dissipation: 30.0,
    accuracy: 76, evasion: 40, braced: false,
    components: _create_components(640, 390, 580, 170, 220, 32),
    weapons: [
        { name: "Type-77 120mm Cannon", short_name: "120MM CANNON", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 15, range_min: 1, range_max: 6, damage: 155, anim_state: "fire_rifle", desc: "Standard cannon." },
        { name: "Ares Micro-Missile Pod", short_name: "MISSILES", proj_type: "MICRO_MISSILE", ap_cost: 4, heat_cost: 20, range_min: 2, range_max: 6, damage: 170, anim_state: "fire_missiles", desc: "Missile pod." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(170, 200, 230),
    is_destroyed: false
});

// 7. Bravo-03: Colony Escort (Aether MP)
array_push(units, {
    id: "ALLIED_6",
    callsign: "Bravo-03 'ZEPHYR'",
    pilot_name: "Ens. Novak",
    team: "ALLIED",
    mech_type: "aether",
    grid_c: 2, grid_r: 3, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 0,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 90.0, heat_dissipation: 38.0,
    accuracy: 84, evasion: 64, braced: false,
    components: _create_components(460, 290, 410, 150, 210, 20),
    weapons: [
        { name: "Coherent Beam Rifle", short_name: "BEAM RIFLE", proj_type: "BEAM_PULSE", ap_cost: 3, heat_cost: 18, range_min: 1, range_max: 6, damage: 165, anim_state: "fire_beam", desc: "Laser pulse weapon." },
        { name: "Beam Saber", short_name: "SABER", proj_type: "MELEE", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 1, damage: 175, anim_state: "melee", desc: "Thermal slash." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(150, 220, 245),
    is_destroyed: false
});

// 8. Bravo-04: Zaibatsu Escort (Muramasa MP)
array_push(units, {
    id: "ALLIED_7",
    callsign: "Bravo-04 'RONIN'",
    pilot_name: "Agent Jin",
    team: "ALLIED",
    mech_type: "muramasa",
    grid_c: 5, grid_r: 4, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 1,
    max_ap: 7, current_ap: 7,
    current_heat: 0.0, max_heat: 85.0, heat_dissipation: 32.0,
    accuracy: 82, evasion: 70, braced: false,
    components: _create_components(430, 270, 400, 140, 190, 18),
    weapons: [
        { name: "Plasma Katana", short_name: "KATANA", proj_type: "MELEE", ap_cost: 3, heat_cost: 12, range_min: 1, range_max: 1, damage: 220, anim_state: "melee", desc: "Energy blade." },
        { name: "Plasma Cannon", short_name: "PLASMA", proj_type: "RAILGUN_SLUG", ap_cost: 4, heat_cost: 24, range_min: 1, range_max: 4, damage: 185, anim_state: "fire_plasma", desc: "Plasma bolt." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.20,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(190, 190, 240),
    is_destroyed: false
});


// --- HOSTILE SYNDICATE & OUTLAW BATTLEGROUP (13 Units) ---
// 1. Viper-01: Syndicate Boss Flagship (Reaver Prime - Customized Ironclad)
array_push(units, {
    id: "HOSTILE_0",
    callsign: "Viper-01 'REAVER PRIME'",
    pilot_name: "Warlord Malakar",
    team: "HOSTILE",
    mech_type: "ironclad",
    grid_c: 16, grid_r: 16, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 7, current_ap: 7,
    current_heat: 0.0, max_heat: 130.0, heat_dissipation: 35.0,
    accuracy: 82, evasion: 45, braced: false,
    components: _create_components(880, 520, 780, 220, 320, 36),
    weapons: [
        { name: "Syndicate Siege 120mm", short_name: "120MM REAVER", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 16, range_min: 1, range_max: 7, damage: 185, anim_state: "fire_rifle", desc: "Overcharged kinetic breech." },
        { name: "Rotary Flak Cannon", short_name: "HEAVY FLAK", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 4, damage: 95, anim_state: "fire_chaingun", desc: "Serrated shrapnel stream." },
        { name: "Heavy Spiked Claw", short_name: "CRUSHER CLAW", proj_type: "MELEE", ap_cost: 3, heat_cost: 10, range_min: 1, range_max: 1, damage: 250, anim_state: "melee", desc: "Devastating melee clamp." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 110, 110),
    is_destroyed: false
});

// 2. Viper-02: Raider Skirmisher (SCR-12 Hyena)
array_push(units, {
    id: "HOSTILE_1",
    callsign: "Viper-02 'SCAVENGER'",
    pilot_name: "Rogue Gnasher",
    team: "HOSTILE",
    mech_type: "hyena",
    grid_c: 15, grid_r: 14, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 2,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 80.0, heat_dissipation: 30.0,
    accuracy: 72, evasion: 62, braced: false,
    components: _create_components(420, 290, 440, 130, 170, 18),
    weapons: [
        { name: "Scrapper Flak Scattergun", short_name: "FLAK SCATTER", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 12, range_min: 1, range_max: 4, damage: 110, anim_state: "fire_flak", desc: "Scrap metal shrapnel blast." },
        { name: "Hydraulic Scrap Claw", short_name: "SCRAP CLAW", proj_type: "MELEE", ap_cost: 2, heat_cost: 8, range_min: 1, range_max: 1, damage: 180, anim_state: "melee", desc: "Industrial cutting claw." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 170, 120),
    is_destroyed: false
});

// 3. Viper-03: Raider Skirmisher (SCR-12 Hyena)
array_push(units, {
    id: "HOSTILE_2",
    callsign: "Viper-03 'CARRION'",
    pilot_name: "Rogue Grin",
    team: "HOSTILE",
    mech_type: "hyena",
    grid_c: 17, grid_r: 15, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 80.0, heat_dissipation: 30.0,
    accuracy: 74, evasion: 60, braced: false,
    components: _create_components(430, 290, 450, 130, 170, 18),
    weapons: [
        { name: "Scrapper Flak Scattergun", short_name: "FLAK SCATTER", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 12, range_min: 1, range_max: 4, damage: 110, anim_state: "fire_flak", desc: "Flak scatter." },
        { name: "Hydraulic Scrap Claw", short_name: "SCRAP CLAW", proj_type: "MELEE", ap_cost: 2, heat_cost: 8, range_min: 1, range_max: 1, damage: 180, anim_state: "melee", desc: "Scrap claw." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 170, 120),
    is_destroyed: false
});

// 4. Viper-04: Raider Skirmisher (SCR-12 Hyena)
array_push(units, {
    id: "HOSTILE_3",
    callsign: "Viper-04 'RUSTFANG'",
    pilot_name: "Rogue Snarl",
    team: "HOSTILE",
    mech_type: "hyena",
    grid_c: 14, grid_r: 16, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 80.0, heat_dissipation: 30.0,
    accuracy: 70, evasion: 65, braced: false,
    components: _create_components(410, 280, 430, 120, 160, 16),
    weapons: [
        { name: "Scrap Rocket Salvo", short_name: "ROCKETS", proj_type: "MICRO_MISSILE", ap_cost: 3, heat_cost: 16, range_min: 2, range_max: 5, damage: 145, anim_state: "fire_flak", desc: "Improvised rockets." },
        { name: "Hydraulic Scrap Claw", short_name: "SCRAP CLAW", proj_type: "MELEE", ap_cost: 2, heat_cost: 8, range_min: 1, range_max: 1, damage: 185, anim_state: "melee", desc: "Claw tear." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 170, 120),
    is_destroyed: false
});

// 5. Viper-05: Rogue Assassin (Stolen Muramasa Blade)
array_push(units, {
    id: "HOSTILE_4",
    callsign: "Viper-05 'SHADOW'",
    pilot_name: "Ex-Agent Kuro",
    team: "HOSTILE",
    mech_type: "muramasa",
    grid_c: 13, grid_r: 14, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 2,
    max_ap: 8, current_ap: 8,
    current_heat: 0.0, max_heat: 85.0, heat_dissipation: 34.0,
    accuracy: 86, evasion: 74, braced: false,
    components: _create_components(450, 280, 420, 150, 200, 20),
    weapons: [
        { name: "Plasma Katana", short_name: "KATANA", proj_type: "MELEE", ap_cost: 3, heat_cost: 14, range_min: 1, range_max: 1, damage: 235, anim_state: "melee", desc: "Energy blade." },
        { name: "Plasma Cannon", short_name: "PLASMA", proj_type: "RAILGUN_SLUG", ap_cost: 4, heat_cost: 25, range_min: 1, range_max: 5, damage: 195, anim_state: "fire_plasma", desc: "Magnetic burst." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.20,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(230, 140, 240),
    is_destroyed: false
});

// 6. Outlaw-01: Captured Ironclad Heavy Frontline
array_push(units, {
    id: "HOSTILE_5",
    callsign: "Outlaw-01 'DREAD'",
    pilot_name: "Marauder Jax",
    team: "HOSTILE",
    mech_type: "ironclad",
    grid_c: 15, grid_r: 12, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 5, current_ap: 5,
    current_heat: 0.0, max_heat: 100.0, heat_dissipation: 30.0,
    accuracy: 74, evasion: 44, braced: false,
    components: _create_components(620, 380, 560, 160, 220, 30),
    weapons: [
        { name: "Type-77 120mm Autocannon", short_name: "120MM CANNON", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 15, range_min: 1, range_max: 6, damage: 150, anim_state: "fire_rifle", desc: "Captured 120mm." },
        { name: "GAU-88 Heavy Vulcan", short_name: "VULCAN", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 4, damage: 80, anim_state: "fire_chaingun", desc: "Vulcan stream." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 120, 120),
    is_destroyed: false
});

// 7. Outlaw-02: Stolen Aether Interceptor
array_push(units, {
    id: "HOSTILE_6",
    callsign: "Outlaw-02 'SPECTRE'",
    pilot_name: "Deserter Vane",
    team: "HOSTILE",
    mech_type: "aether",
    grid_c: 12, grid_r: 15, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 2,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 90.0, heat_dissipation: 38.0,
    accuracy: 84, evasion: 66, braced: false,
    components: _create_components(460, 290, 420, 150, 210, 20),
    weapons: [
        { name: "Coherent Beam Rifle", short_name: "BEAM RIFLE", proj_type: "BEAM_PULSE", ap_cost: 3, heat_cost: 18, range_min: 1, range_max: 6, damage: 170, anim_state: "fire_beam", desc: "Stolen laser rifle." },
        { name: "Beam Saber", short_name: "SABER", proj_type: "MELEE", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 1, damage: 180, anim_state: "melee", desc: "High heat saber." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 150, 180),
    is_destroyed: false
});

// 8. Outlaw-03: Heavy Outlaw Grunt (Ironclad)
array_push(units, {
    id: "HOSTILE_7",
    callsign: "Outlaw-03 'GARGOYLE'",
    pilot_name: "Marauder Tyke",
    team: "HOSTILE",
    mech_type: "ironclad",
    grid_c: 16, grid_r: 13, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 5, current_ap: 5,
    current_heat: 0.0, max_heat: 100.0, heat_dissipation: 30.0,
    accuracy: 72, evasion: 40, braced: false,
    components: _create_components(600, 360, 540, 150, 200, 28),
    weapons: [
        { name: "120mm Autocannon", short_name: "120MM CANNON", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 15, range_min: 1, range_max: 5, damage: 145, anim_state: "fire_rifle", desc: "Kinetic weapon." },
        { name: "Missile Pod", short_name: "MISSILES", proj_type: "MICRO_MISSILE", ap_cost: 4, heat_cost: 20, range_min: 2, range_max: 6, damage: 165, anim_state: "fire_missiles", desc: "Rocket swarm." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 120, 120),
    is_destroyed: false
});

// 9. Outlaw-04: Rogue Muramasa Skirmisher
array_push(units, {
    id: "HOSTILE_8",
    callsign: "Outlaw-04 'ONI'",
    pilot_name: "Rogue Kenji",
    team: "HOSTILE",
    mech_type: "muramasa",
    grid_c: 14, grid_r: 15, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 2,
    max_ap: 7, current_ap: 7,
    current_heat: 0.0, max_heat: 85.0, heat_dissipation: 32.0,
    accuracy: 80, evasion: 70, braced: false,
    components: _create_components(430, 270, 410, 140, 190, 18),
    weapons: [
        { name: "Plasma Katana", short_name: "KATANA", proj_type: "MELEE", ap_cost: 3, heat_cost: 12, range_min: 1, range_max: 1, damage: 215, anim_state: "melee", desc: "Blade slash." },
        { name: "Plasma Cannon", short_name: "PLASMA", proj_type: "RAILGUN_SLUG", ap_cost: 4, heat_cost: 24, range_min: 1, range_max: 4, damage: 180, anim_state: "fire_plasma", desc: "Plasma strike." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.20,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(230, 130, 220),
    is_destroyed: false
});

// 10. Outlaw-05: Hyena Salvage Raider
array_push(units, {
    id: "HOSTILE_9",
    callsign: "Outlaw-05 'SCRAPHEAP'",
    pilot_name: "Rogue Patch",
    team: "HOSTILE",
    mech_type: "hyena",
    grid_c: 13, grid_r: 12, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 80.0, heat_dissipation: 30.0,
    accuracy: 70, evasion: 60, braced: false,
    components: _create_components(400, 270, 410, 120, 150, 16),
    weapons: [
        { name: "Scrapper Flak", short_name: "FLAK", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 4, damage: 105, anim_state: "fire_flak", desc: "Flak burst." },
        { name: "Scrap Claw", short_name: "CLAW", proj_type: "MELEE", ap_cost: 2, heat_cost: 8, range_min: 1, range_max: 1, damage: 175, anim_state: "melee", desc: "Claw strike." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 170, 120),
    is_destroyed: false
});

// 11. Outlaw-06: Hyena Salvage Raider
array_push(units, {
    id: "HOSTILE_10",
    callsign: "Outlaw-06 'BONECRUSHER'",
    pilot_name: "Rogue Maul",
    team: "HOSTILE",
    mech_type: "hyena",
    grid_c: 15, grid_r: 15, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 2,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 80.0, heat_dissipation: 30.0,
    accuracy: 71, evasion: 62, braced: false,
    components: _create_components(410, 280, 420, 120, 160, 16),
    weapons: [
        { name: "Scrapper Flak", short_name: "FLAK", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 4, damage: 105, anim_state: "fire_flak", desc: "Flak." },
        { name: "Scrap Claw", short_name: "CLAW", proj_type: "MELEE", ap_cost: 2, heat_cost: 8, range_min: 1, range_max: 1, damage: 175, anim_state: "melee", desc: "Claw." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 170, 120),
    is_destroyed: false
});

// 12. Outlaw-07: Stolen Aether Sniper
array_push(units, {
    id: "HOSTILE_11",
    callsign: "Outlaw-07 'WRAITH'",
    pilot_name: "Rogue Ghost",
    team: "HOSTILE",
    mech_type: "aether",
    grid_c: 16, grid_r: 11, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 90.0, heat_dissipation: 38.0,
    accuracy: 86, evasion: 65, braced: false,
    components: _create_components(450, 280, 410, 150, 200, 20),
    weapons: [
        { name: "Coherent Beam Rifle", short_name: "BEAM RIFLE", proj_type: "BEAM_PULSE", ap_cost: 3, heat_cost: 18, range_min: 2, range_max: 7, damage: 175, anim_state: "fire_beam", desc: "Long range laser beam." },
        { name: "Beam Saber", short_name: "SABER", proj_type: "MELEE", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 1, damage: 170, anim_state: "melee", desc: "Saber." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 150, 180),
    is_destroyed: false
});

// 13. Outlaw-08: Captured Ironclad Line
array_push(units, {
    id: "HOSTILE_12",
    callsign: "Outlaw-08 'RUSTBUCKET'",
    pilot_name: "Marauder Clank",
    team: "HOSTILE",
    mech_type: "ironclad",
    grid_c: 17, grid_r: 12, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 5, current_ap: 5,
    current_heat: 0.0, max_heat: 100.0, heat_dissipation: 30.0,
    accuracy: 70, evasion: 38, braced: false,
    components: _create_components(590, 350, 530, 150, 190, 26),
    weapons: [
        { name: "120mm Autocannon", short_name: "120MM CANNON", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 15, range_min: 1, range_max: 5, damage: 140, anim_state: "fire_rifle", desc: "Standard solid cannon." },
        { name: "Vulcan Harass", short_name: "VULCAN", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 3, damage: 75, anim_state: "fire_chaingun", desc: "Vulcan." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 120, 120),
    is_destroyed: false
});

// =========================================================================
// INTERACTIVE PROLOGUE AMBUSH SORTIE OVERRIDE (DOC 51)
// =========================================================================
if (!is_undefined(_combat_ctx) && variable_struct_exists(_combat_ctx, "is_prologue") && _combat_ctx.is_prologue) {
    units = [];
    var _cmdr_callsign = (instance_exists(obj_GameManager) ? ("Genesis-01 '" + obj_GameManager.player_commander.callsign + "'") : "Genesis-01 'PILOT'");
    var _cmdr_name = (instance_exists(obj_GameManager) ? obj_GameManager.player_commander.name : "Acting Pilot");
    var _cmdr_spr = spr_ms_custom_biped_heavy_idle;
    
    // Calculate Pilot Stat influence
    var _acc_bonus = 0;
    var _eva_bonus = 0;
    if (instance_exists(obj_GameManager) && variable_struct_exists(obj_GameManager.player_commander, "stats")) {
        var _c_stats = obj_GameManager.player_commander.stats;
        _acc_bonus = floor((_c_stats.gunnery - 40) * 0.4);
        _eva_bonus = floor((_c_stats.evasion - 40) * 0.4);
    }

    // Unit 0: Player Commander in the GHA-00 Genesis Prototype
    array_push(units, {
        id: "ALLIED_0",
        callsign: _cmdr_callsign,
        pilot_name: _cmdr_name,
        team: "ALLIED",
        mech_type: "ironclad",
        sprite_asset: _cmdr_spr,
        grid_c: 4, grid_r: 4, elev: 0,
        visual_x: 0, visual_y: 0,
        facing: 0,
        max_ap: 8, current_ap: 8,
        current_heat: 0.0, max_heat: 100.0, heat_dissipation: 45.0,
        accuracy: 86 + _acc_bonus, evasion: 52 + _eva_bonus, braced: false,
        components: _create_components(750, 420, 620, 240, 280, 32),
        weapons: [
            { name: "120mm Proto-Rail Vulcan", short_name: "RAIL VULCAN", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 8, range_min: 1, range_max: 5, damage: 135, anim_state: "fire_chaingun", desc: "Experimental pre-war rapid magnetic slug accelerator." },
            { name: "Hyper-Particle Beam Rifle", short_name: "BEAM RIFLE", proj_type: "BEAM_PULSE", ap_cost: 3, heat_cost: 18, range_min: 1, range_max: 7, damage: 220, anim_state: "fire_beam", desc: "Devastating focused particle beam punch." },
            { name: "Pre-War Plasma Saber", short_name: "PLASMA SABER", proj_type: "MELEE", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 1, damage: 260, anim_state: "melee", desc: "Superheated plasma cutting blade." },
            { name: "VLS Micro-Missile Pod", short_name: "VLS MISSILES", proj_type: "MICRO_MISSILE", ap_cost: 3, heat_cost: 16, range_min: 2, range_max: 6, damage: 175, anim_state: "fire_missiles", desc: "Multi-target tracking swarm warheads." }
        ],
        anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
        recoil_x: 0, recoil_y: 0, recoil_shake: 0,
        image_blend: c_white,
        is_destroyed: false
    });

    // Unit 1: Hephaestus Point-Defense Automated Sentry Drone
    array_push(units, {
        id: "ALLIED_1",
        callsign: "DEFENSE-01 'SEC-TURRET'",
        pilot_name: "Hephaestus Defense AI",
        team: "ALLIED",
        mech_type: "veh_terran_skyhammer",
        sprite_asset: (sprite_exists(spr_veh_terran_skyhammer_idle) ? spr_veh_terran_skyhammer_idle : spr_ms_custom_hover_sniper_idle),
        grid_c: 3, grid_r: 5, elev: 0,
        visual_x: 0, visual_y: 0,
        facing: 0,
        max_ap: 6, current_ap: 6,
        current_heat: 0.0, max_heat: 90.0, heat_dissipation: 35.0,
        accuracy: 82, evasion: 40, braced: false,
        components: _create_components(450, 280, 360, 150, 180, 20),
        weapons: [
            { name: "Flak Intercept Gun", short_name: "FLAK GUN", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 5, damage: 95, anim_state: "fire_flak", desc: "Automated perimeter flak curtain." },
            { name: "EMP Shock Burst", short_name: "EMP BURST", proj_type: "BEAM_PULSE", ap_cost: 3, heat_cost: 14, range_min: 1, range_max: 4, damage: 80, anim_state: "fire_beam", desc: "Electromagnetic systems disruptor." }
        ],
        anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
        recoil_x: 0, recoil_y: 0, recoil_shake: 0,
        image_blend: make_color_rgb(180, 230, 255),
        is_destroyed: false
    });

    // Hostile 0: Light Corsair Strike Skiff A
    array_push(units, {
        id: "HOSTILE_0",
        callsign: "Raider-01 'CORSAIR SKIFF A'",
        pilot_name: "Hyena Interceptor",
        team: "HOSTILE",
        mech_type: "veh_syndicate_technical",
        sprite_asset: (sprite_exists(spr_veh_syndicate_technical_idle) ? spr_veh_syndicate_technical_idle : spr_ms_custom_aero_striker_idle),
        grid_c: 7, grid_r: 3, elev: 0,
        visual_x: 0, visual_y: 0,
        facing: 2,
        max_ap: 6, current_ap: 6,
        current_heat: 0.0, max_heat: 75.0, heat_dissipation: 30.0,
        accuracy: 68, evasion: 55, braced: false,
        components: _create_components(280, 140, 240, 90, 120, 14),
        weapons: [
            { name: "Rapid Autoguns", short_name: "AUTOGUNS", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 8, range_min: 1, range_max: 4, damage: 70, anim_state: "fire_flak", desc: "Light kinetic tracer burst." },
            { name: "Harpoon Kinetic Tether", short_name: "HARPOON", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 12, range_min: 1, range_max: 4, damage: 95, anim_state: "fire_rifle", desc: "Magnetic cable shot." }
        ],
        anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.16,
        recoil_x: 0, recoil_y: 0, recoil_shake: 0,
        image_blend: make_color_rgb(255, 140, 120),
        is_destroyed: false
    });

    // Hostile 1: Light Corsair Strike Skiff B
    array_push(units, {
        id: "HOSTILE_1",
        callsign: "Raider-02 'CORSAIR SKIFF B'",
        pilot_name: "Hyena Striker",
        team: "HOSTILE",
        mech_type: "veh_colony_stiletto",
        sprite_asset: (sprite_exists(spr_veh_colony_stiletto_idle) ? spr_veh_colony_stiletto_idle : spr_ms_custom_hover_sniper_idle),
        grid_c: 8, grid_r: 4, elev: 0,
        visual_x: 0, visual_y: 0,
        facing: 3,
        max_ap: 6, current_ap: 6,
        current_heat: 0.0, max_heat: 75.0, heat_dissipation: 30.0,
        accuracy: 70, evasion: 58, braced: false,
        components: _create_components(260, 130, 220, 90, 110, 14),
        weapons: [
            { name: "Twin Autocannons", short_name: "TWIN CANNON", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 8, range_min: 1, range_max: 4, damage: 75, anim_state: "fire_flak", desc: "Twin kinetic volley." },
            { name: "Rocket Pod", short_name: "ROCKET POD", proj_type: "MICRO_MISSILE", ap_cost: 3, heat_cost: 14, range_min: 2, range_max: 5, damage: 90, anim_state: "fire_missiles", desc: "Unguided rocket pod." }
        ],
        anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.16,
        recoil_x: 0, recoil_y: 0, recoil_shake: 0,
        image_blend: make_color_rgb(255, 170, 130),
        is_destroyed: false
    });

    // Hostile 2: Heavy Corsair Gunship
    array_push(units, {
        id: "HOSTILE_2",
        callsign: "Raider-03 'CORSAIR GUNSHIP'",
        pilot_name: "Hyena Raid Leader",
        team: "HOSTILE",
        mech_type: "veh_colony_gunship",
        sprite_asset: (sprite_exists(spr_veh_colony_gunship_idle) ? spr_veh_colony_gunship_idle : spr_ms_custom_tread_artillery_idle),
        grid_c: 7, grid_r: 6, elev: 0,
        visual_x: 0, visual_y: 0,
        facing: 2,
        max_ap: 6, current_ap: 6,
        current_heat: 0.0, max_heat: 85.0, heat_dissipation: 28.0,
        accuracy: 74, evasion: 42, braced: false,
        components: _create_components(440, 220, 380, 140, 180, 22),
        weapons: [
            { name: "Heavy Dual Autocannon", short_name: "HEAVY CANNON", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 14, range_min: 1, range_max: 6, damage: 130, anim_state: "fire_rifle", desc: "Heavy kinetic artillery slug." },
            { name: "Shrapnel Torpedo", short_name: "TORPEDO", proj_type: "MICRO_MISSILE", ap_cost: 3, heat_cost: 18, range_min: 2, range_max: 5, damage: 145, anim_state: "fire_missiles", desc: "Anti-ship shrapnel warhead." }
        ],
        anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
        recoil_x: 0, recoil_y: 0, recoil_shake: 0,
        image_blend: make_color_rgb(255, 120, 100),
        is_destroyed: false
    });
    // Disable random Nemesis incursion during prologue
    nemesis_incursion_checked = true;
}

// Ensure sprite_asset is initialized on every combat unit
for (var i = 0; i < array_length(units); i++) {
    var _u = units[i];
    if (!variable_struct_exists(_u, "sprite_asset") || !sprite_exists(_u.sprite_asset)) {
        var _cand = asset_get_index("spr_ms_" + string(_u.mech_type) + "_idle");
        if (_cand != -1 && sprite_exists(_cand)) {
            _u.sprite_asset = _cand;
        } else {
            _u.sprite_asset = spr_ms_ironclad_idle;
        }
    }
}

// Tactical Radio Comms Opening Intercom Bark (Doc 52)
if ((is_undefined(_combat_ctx) || !variable_struct_exists(_combat_ctx, "is_prologue") || !_combat_ctx.is_prologue) && array_length(units) > 0) {
    var _first_enemy = undefined;
    for (var u = 0; u < array_length(units); u++) {
        if (units[u].team == "HOSTILE") {
            _first_enemy = units[u];
            break;
        }
    }
    if (!is_undefined(_first_enemy)) {
        var _enemy_portrait = (variable_struct_exists(_first_enemy, "portrait") && sprite_exists(_first_enemy.portrait)) ? _first_enemy.portrait : ((variable_struct_exists(_first_enemy, "sprite_asset") && sprite_exists(_first_enemy.sprite_asset)) ? _first_enemy.sprite_asset : spr_portrait_commander_male);
        scr_vn_trigger_combat_intercom(_first_enemy.pilot_name + " [" + _first_enemy.callsign + "]", _enemy_portrait, "Hostile vanguard detected on tactical radar. All units, weapons free! Tear their armor apart!", 180, make_color_rgb(255, 90, 90));
    }
}

// Initialize unit visual coordinates to world screen positions
for (var i = 0; i < array_length(units); i++) {
    var _u = units[i];
    _u.elev = grid_elev[_u.grid_c][_u.grid_r];
    _u.visual_x = iso_to_screen_x(_u.grid_c, _u.grid_r, _u.elev, cam_x, cam_y, zoom);
    _u.visual_y = iso_to_screen_y(_u.grid_c, _u.grid_r, _u.elev, cam_x, cam_y, zoom);
}

// 5a-ii. Pilot Roster Integration, Frame Affinity & Active Perks (Doc 51)
if (instance_exists(obj_GameManager) && variable_struct_exists(obj_GameManager.facilities, "roster_pilots")) {
    var _r_pilots = obj_GameManager.facilities.roster_pilots;
    var _allied_idx = 0;
    for (var u = 0; u < array_length(units); u++) {
        var _un = units[u];
        if (_un.team == "ALLIED" && _allied_idx < array_length(_r_pilots)) {
            var _pilot = _r_pilots[_allied_idx];
            if (_pilot.status == "ACTIVE") {
                _un.pilot_name = _pilot.name;
                _un.callsign = _pilot.callsign + " [" + string_upper(_un.mech_type) + "]";
                _un.accuracy = max(55, _pilot.accuracy);
                _un.evasion = max(35, _pilot.reflexes);
                _un.pilot_reflexes = _pilot.reflexes;
                _un.combat_stat = variable_struct_exists(_pilot, "combat_stat") ? _pilot.combat_stat : 8;
                _un.tactics_stat = variable_struct_exists(_pilot, "tactics_stat") ? _pilot.tactics_stat : 8;
                _un.rank_perks = (variable_struct_exists(_pilot, "rank_perks") && is_array(_pilot.rank_perks)) ? _pilot.rank_perks : [];
                _un.pilot_affinity = (variable_struct_exists(_pilot, "affinity") ? _pilot.affinity : "ironclad");
                _un.mutated_traits = (variable_struct_exists(_pilot, "mutated_traits") && is_array(_pilot.mutated_traits)) ? _pilot.mutated_traits : [];
                _un.kills = 0;

                // Milestone 56: Combat Sortie increases pilot fatigue (+25)
                _pilot.fatigue = min(100, (variable_struct_exists(_pilot, "fatigue") ? _pilot.fatigue : 0) + 25);
                _un.fatigue = _pilot.fatigue;

                // Frame Affinity Resonance Check
                var _p_aff = string_lower(_un.pilot_affinity);
                var _m_type = string_lower(_un.mech_type);
                if (_p_aff == _m_type ||
                    (_p_aff == "ironclad" && (_m_type == "ironclad" || _m_type == "biped")) ||
                    (_p_aff == "aether" && (_m_type == "aether" || _m_type == "aero")) ||
                    (_p_aff == "muramasa" && (_m_type == "muramasa" || _m_type == "hover")) ||
                    (_p_aff == "treads" && (_m_type == "titan" || _m_type == "treads"))) {
                    _un.has_affinity_match = true;
                    _un.accuracy += 8;
                    _un.evasion += 8;
                    _un.max_ap += 1;
                    _un.current_ap = _un.max_ap;
                }
                _allied_idx++;
            }
        }
    }
}

// 5a. Dynamic Mass-Production Line Chassis Assignment (docs/29 & docs/30)
if (instance_exists(obj_FactionManager) && variable_instance_exists(obj_FactionManager, "mass_production_contracts")) {
    var _mp_terran = obj_FactionManager.mass_production_contracts[$ "faction_a"];
    var _mp_syndicate = obj_FactionManager.mass_production_contracts[$ "faction_c"];
    
    for (var u = 0; u < array_length(units); u++) {
        var _un = units[u];
        // Allied line units field the active Terran Mass-Production Suit
        if (_un.id == "ALLIED_4" || _un.id == "ALLIED_5") {
            if (!is_undefined(_mp_terran)) {
                _un.callsign = ((_un.id == "ALLIED_4") ? "Bravo-01 " : "Bravo-02 ") + "(" + _mp_terran.baseline_suit_name + ")";
                if (variable_struct_exists(_mp_terran, "sprite_asset") && sprite_exists(_mp_terran.sprite_asset)) {
                    _un.sprite_asset = _mp_terran.sprite_asset;
                }
            }
        }
        // Hostile Outlaw grunts field the active Syndicate Mass-Production Suit
        if (string_pos("OUTLAW_", _un.id) > 0 || _un.id == "ENEMY_5" || _un.id == "ENEMY_7") {
            if (!is_undefined(_mp_syndicate)) {
                _un.callsign = "Raider (" + _mp_syndicate.baseline_suit_name + ")";
                if (variable_struct_exists(_mp_syndicate, "sprite_asset") && sprite_exists(_mp_syndicate.sprite_asset)) {
                    _un.sprite_asset = _mp_syndicate.sprite_asset;
                }
            }
        }
    }
}

// 5b. Flagship Strategic Division Buffs & Theater Alignment (Goal C)
if (instance_exists(obj_GameManager)) {
    var _gm = obj_GameManager;
    var _gm_fs = _gm.flagship;
    var _cur_map = map_definitions[current_map_id];
    var _in_theater = _gm.flagship_is_in_theater(_cur_map.theater);

    if (_in_theater) {
        add_log("[ORBITAL SUPPORT ONLINE] USN-X Hephaestus in position over " + _cur_map.theater + " theater.");
        if (_gm_fs.upgrades.command_tier >= 5) {
            for (var i = 0; i < array_length(units); i++) {
                if (units[i].team == "ALLIED") {
                    units[i].max_ap += 2;
                    units[i].current_ap += 2;
                    units[i].accuracy = min(99, units[i].accuracy + 20);
                }
            }
        }
    } else if (_gm_fs.transit_turns_left > 0) {
        add_log("[ORBITAL SUPPORT OFFLINE] Hephaestus in transit to " + _gm_fs.destination_sphere + " (" + string(_gm_fs.transit_turns_left) + "T).");
    } else {
        add_log("[ORBITAL SUPPORT OFFLINE] Hephaestus stationed in " + _gm_fs.current_sphere + " (out of range).");
    }
}

// 5c-0. Strategic Tech Tree Multipliers to Fielded Allied Forces (Doc 41)
var _ap_bonus = floor(scr_research_get_bonus("ap_max"));
var _ev_bonus = floor(scr_research_get_bonus("evasion") * 100);
for (var u = 0; u < array_length(units); u++) {
    if (units[u].team == "ALLIED") {
        units[u].max_ap += _ap_bonus;
        units[u].current_ap = units[u].max_ap;
        units[u].evasion += _ev_bonus;
    }
}

// 5c-1. Strategic Logistics & Supply Starvation Check (Goal A)
if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "supply_starvation") && obj_GameManager.supply_starvation) {
    for (var i = 0; i < array_length(units); i++) {
        if (units[i].team == "ALLIED") {
            units[i].max_ap = max(1, units[i].max_ap - 2);
            units[i].current_ap = min(units[i].current_ap, units[i].max_ap);
            units[i].evasion = max(0, units[i].evasion - 25);
            units[i].supply_starved = true;
        }
    }
    add_log("[SUPPLY DEFICIT] Allied battlegroup suffering maintenance & fuel starvation (-2 AP, -25% Evasion)!");
}

// 5c-2. Pilot Fatigue & Ace Perks Check (Goal B)
if (instance_exists(obj_GameManager) && variable_struct_exists(obj_GameManager.facilities, "roster_pilots")) {
    var _r_pilots = obj_GameManager.facilities.roster_pilots;
    for (var u = 0; u < array_length(units); u++) {
        var _un = units[u];
        if (_un.team == "ALLIED") {
            var _matched_p = undefined;
            for (var p = 0; p < array_length(_r_pilots); p++) {
                if (_r_pilots[p].status == "ACTIVE") {
                    _matched_p = _r_pilots[p];
                    break;
                }
            }

            if (_matched_p != undefined) {
                _un.pilot_ref_id = _matched_p.id;
                if (variable_struct_exists(_matched_p, "fatigue") && _matched_p.fatigue >= 3) {
                    _un.accuracy = max(20, _un.accuracy - 15);
                    _un.evasion = max(0, _un.evasion - 15);
                    add_log("[FATIGUED PILOT] " + _matched_p.name + " (" + _matched_p.callsign + ") suffering combat exhaustion (-15% Acc/Eva)!");
                }
                if (variable_struct_exists(_matched_p, "rank_perks") && is_array(_matched_p.rank_perks)) {
                    if (array_contains(_matched_p.rank_perks, "Quick Draw")) {
                        _un.current_ap += 1;
                        add_log("[ACE PERK] " + _matched_p.callsign + " triggered 'Quick Draw' (+1 Turn 1 AP)!");
                    }
                    if (array_contains(_matched_p.rank_perks, "Deadeye")) {
                        _un.crit_chance = min(99, (variable_struct_exists(_un, "crit_chance") ? _un.crit_chance : 10) + 15);
                        add_log("[ACE PERK] " + _matched_p.callsign + " active 'Deadeye' (+15% Crit Rate)!");
                    }
                    if (array_contains(_matched_p.rank_perks, "Overdrive")) {
                        _un.has_overdrive = true;
                    }
                }
            }
        }
    }
}
// 5b. Flagship Strategic Division Buffs (Doc 24)
if (instance_exists(obj_GameManager)) {
    var _gm_fs = obj_GameManager.flagship;
    // Command Tier 5: Tactical Supremacy (+2 AP, +20% accuracy)
    if (_gm_fs.upgrades.command_tier >= 5) {
        for (var i = 0; i < array_length(units); i++) {
            if (units[i].team == "ALLIED") {
                units[i].max_ap += 2;
                units[i].current_ap += 2;
                units[i].accuracy = min(99, units[i].accuracy + 20);
            }
        }
    }
    // Pilot Suite Tier 4+: Genkai Reflex Limit (+20% evasion)
    if (_gm_fs.upgrades.pilot_suite_tier >= 4) {
        for (var i = 0; i < array_length(units); i++) {
            if (units[i].team == "ALLIED") {
                units[i].evasion = min(99, units[i].evasion + 20);
            }
        }
    }
    // Master Protocol B: Orbital Siege Fortress (+35% armor rating, +15 heat dissipation)
    if (_gm_fs.specialization_protocol == "siege_fortress") {
        for (var i = 0; i < array_length(units); i++) {
            if (units[i].team == "ALLIED") {
                units[i].heat_dissipation += 15.0;
                if (variable_struct_exists(units[i], "components") && variable_struct_exists(units[i].components, "torso")) {
                    units[i].components.torso.armor = floor(units[i].components.torso.armor * 1.35);
                }
            }
        }
    }
}

// 5c. Ongoing Campaign Reflection: Tech Era Escalation & Competitor R&D Lineage (Doc 27)
if (instance_exists(obj_GameManager)) {
    var _gm = obj_GameManager;
    var _era = _gm[$ "timeline_era"] ?? 1;
    var _era_name = _gm[$ "timeline_era_name"] ?? "Early Solar Skirmishes";
    
    // Scale hostiles with Solar Tech Era
    if (_era >= 2) {
        var _armor_mult = (_era == 2) ? 1.15 : ((_era == 3) ? 1.30 : 1.50);
        var _dmg_add = (_era == 2) ? 10 : ((_era == 3) ? 25 : 40);
        var _acc_add = (_era == 2) ? 6 : ((_era == 3) ? 12 : 20);
        
        for (var i = 0; i < array_length(units); i++) {
            if (units[i].team == "HOSTILE") {
                units[i].accuracy = min(95, units[i].accuracy + _acc_add);
                if (variable_struct_exists(units[i], "components")) {
                    if (variable_struct_exists(units[i].components, "torso")) units[i].components.torso.armor = floor(units[i].components.torso.armor * _armor_mult);
                    if (variable_struct_exists(units[i].components, "arm_left")) units[i].components.arm_left.armor = floor(units[i].components.arm_left.armor * _armor_mult);
                    if (variable_struct_exists(units[i].components, "arm_right")) units[i].components.arm_right.armor = floor(units[i].components.arm_right.armor * _armor_mult);
                    if (variable_struct_exists(units[i].components, "legs")) units[i].components.legs.armor = floor(units[i].components.legs.armor * _armor_mult);
                }
                if (variable_struct_exists(units[i], "weapons")) {
                    for (var w = 0; w < array_length(units[i].weapons); w++) {
                        units[i].weapons[w].damage += _dmg_add;
                    }
                }
            }
        }
    }
    
    // Check Faction Mass Production & Blueprint Vulnerability Exploitation
    if (instance_exists(obj_FactionManager)) {
        var _fm = obj_FactionManager;
        var _factions = ["faction_terran", "faction_colony", "faction_syndicate", "faction_zaibatsu"];
        for (var f = 0; f < array_length(_factions); f++) {
            var _fid = _factions[f];
            if (variable_struct_exists(_fm.mass_production_contracts, _fid)) {
                var _mp = _fm.mass_production_contracts[$ _fid];
                if (_mp.replaced) {
                    // Outlaw / Syndicate forces have salvaged or pirated the player's adopted chassis!
                    for (var u = 0; u < array_length(units); u++) {
                        if (units[u].team == "HOSTILE" && (u == 5 || u == 6)) {
                            units[u].callsign = "Pirated " + _mp.replacement_name + " #" + string(u);
                            units[u].blueprint_exploited = true;
                        }
                    }
                }
            }
        }
    }
    
    // Check Competitor Rare Prototype X-Chassis Incursion
    if (variable_struct_exists(_gm, "competitor_catalog") && is_struct(_gm.competitor_catalog)) {
        var _rival_keys = variable_struct_get_names(_gm.competitor_catalog);
        for (var r = 0; r < array_length(_rival_keys); r++) {
            var _rc = _gm.competitor_catalog[$ _rival_keys[r]];
            if (is_struct(_rc) && _rc.has_rare_x_spec && variable_struct_exists(_rc, "rare_x_chassis") && !is_undefined(_rc.rare_x_chassis) && _era >= 3) {
                // Elite hostile leader upgrades to competitor prototype
                for (var u = 0; u < array_length(units); u++) {
                    if (units[u].id == "HOSTILE_0") {
                        units[u].callsign = units[u].pilot_name + " [" + _rc.rare_x_chassis.name + "]";
                        units[u].max_ap += 1;
                        units[u].current_ap += 1;
                        if (variable_struct_exists(units[u], "components") && variable_struct_exists(units[u].components, "torso")) {
                            units[u].components.torso.armor += 10;
                        }
                        break;
                    }
                }
                break;
            }
        }
    }
    
    // Sync Allied Units with Player Commissioned Deployable Mechs & Pedigree
    if (variable_struct_exists(_gm, "inventory") && variable_struct_exists(_gm.inventory, "deployable_mechs")) {
        var _dmechs = _gm.inventory.deployable_mechs;
        for (var m = 0; m < min(array_length(_dmechs), 4); m++) {
            var _dm = _dmechs[m];
            var _au = units[m];
            if (is_struct(_dm) && variable_struct_exists(_dm, "name") && _dm.name != "") {
                _au.callsign = _dm.callsign;
                if (variable_struct_exists(_dm, "combat_pedigree") && is_struct(_dm.combat_pedigree)) {
                    var _tele = _dm.combat_pedigree.telemetry_bonus;
                // S-Grade Masterwork AP Tuning (Goal D)
                if (variable_struct_exists(_dm, "is_masterwork") && _dm.is_masterwork) {
                    _au.max_ap += 1;
                    _au.current_ap += 1;
                    _au.is_masterwork = true;
                    add_log("[S-GRADE MASTERWORK] " + _au.callsign + " active masterwork tuning (+1 AP)!");
                }
                    _au.accuracy = min(99, _au.accuracy + floor(_tele));
                }
            }
        }
    }

    // 5d. Faction Diplomatic Battlefield Intervention Execution (docs/28)
    if (instance_exists(obj_FactionManager)) {
        var _interventions = obj_FactionManager.evaluate_battlefield_faction_intervention("");
        for (var it = 0; it < array_length(_interventions); it++) {
            var _action = _interventions[it];
            if (_action.type == "ALLIED_ASSIST") {
                // Orbital MAC Strike
                if (_action.dmg_to_boss > 0) {
                    for (var u = 0; u < array_length(units); u++) {
                        if (units[u].id == "HOSTILE_0" && !units[u].is_destroyed) {
                            if (variable_struct_exists(units[u].components, "torso")) {
                                units[u].components.torso.cur = max(50, units[u].components.torso.cur - _action.dmg_to_boss);
                            }
                            add_log("[ALLIED INTERVENTION] " + _action.title + " strikes " + units[u].callsign + " for -" + string(_action.dmg_to_boss) + " DMG!");
                            break;
                        }
                    }
                }
                // ECM Blinding Chaff
                if (_action.hit_penalty > 0) {
                    for (var u = 0; u < array_length(units); u++) {
                        if (units[u].team == "HOSTILE") {
                            units[u].accuracy = max(20, units[u].accuracy - _action.hit_penalty);
                            units[u].max_ap = max(3, units[u].max_ap + _action.ap_mod);
                            units[u].current_ap = units[u].max_ap;
                        }
                    }
                    add_log("[ALLIED INTERVENTION] " + _action.title + ": Hostile sensors blinded (-20% Hit, -1 AP)!");
                }
                // Field Rig Repair
                if (_action.armor_repair > 0) {
                    for (var u = 0; u < array_length(units); u++) {
                        if (units[u].team == "ALLIED") {
                            if (variable_struct_exists(units[u].components, "torso")) {
                                units[u].components.torso.cur = min(units[u].components.torso.max, units[u].components.torso.cur + _action.armor_repair);
                            }
                        }
                    }
                    add_log("[ALLIED INTERVENTION] " + _action.title + ": Emergency nanites repair +" + string(_action.armor_repair) + " Armor!");
                }
                // Cyber-Neural Overload
                if (_action.heat_spike > 0) {
                    for (var u = 0; u < array_length(units); u++) {
                        if (units[u].id == "HOSTILE_0") {
                            units[u].current_heat = min(units[u].max_heat, units[u].current_heat + _action.heat_spike);
                            add_log("[ALLIED INTERVENTION] " + _action.title + ": Hostile reactor spiked +" + string(_action.heat_spike) + " Heat!");
                            break;
                        }
                    }
                }
            } else if (_action.type == "HOSTILE_HINDRANCE") {
                // Airspace Lockout
                if (variable_struct_exists(_action, "allied_ap_penalty") && _action.allied_ap_penalty > 0) {
                    for (var u = 0; u < array_length(units); u++) {
                        if (units[u].team == "ALLIED") {
                            units[u].current_ap = max(2, units[u].current_ap - _action.allied_ap_penalty);
                        }
                    }
                    add_log("[HOSTILE HINDRANCE] " + _action.title + ": Airspace interdiction active (-2 AP on Sortie)!");
                }
                // Thermal Flare Storm
                if (variable_struct_exists(_action, "allied_heat_penalty") && _action.allied_heat_penalty > 0) {
                    for (var u = 0; u < array_length(units); u++) {
                        if (units[u].team == "ALLIED") {
                            units[u].heat_dissipation = max(10, units[u].heat_dissipation - _action.allied_heat_penalty);
                        }
                    }
                    add_log("[HOSTILE HINDRANCE] " + _action.title + ": Solar flare storm (-15 Heat Dissipation)!");
                }
                // Targeting Scrambler Worm
                if (variable_struct_exists(_action, "allied_acc_penalty") && _action.allied_acc_penalty > 0) {
                    for (var u = 0; u < array_length(units); u++) {
                        if (units[u].team == "ALLIED") {
                            units[u].accuracy = max(30, units[u].accuracy - _action.allied_acc_penalty);
                        }
                    }
                    add_log("[HOSTILE HINDRANCE] " + _action.title + ": Targeting scrambler worm active (-15% Accuracy)!");
                }
                // Mercenary Flankers
                if (variable_struct_exists(_action, "spawn_flankers") && _action.spawn_flankers) {
                    for (var u = 0; u < array_length(units); u++) {
                        if (units[u].team == "HOSTILE" && units[u].mech_type == "hyena") {
                            units[u].evasion = min(90, units[u].evasion + 15);
                        }
                    }
                    add_log("[HOSTILE HINDRANCE] " + _action.title + ": Pirate raiders flanking battlefield (+15% Evasion)!");
                }
            }
        }
    }
}


// Ensure all units possess platoon vs super-ace, movement profile & targeting properties
for (var u = 0; u < array_length(units); u++) {
    var _un = units[u];
    if (!variable_struct_exists(_un, "squad_type")) {
        if (_un.id == "ALLIED_0" || _un.id == "ALLIED_2" || _un.id == "HOSTILE_0" || _un.id == "HOSTILE_4") {
            _un.squad_type = "SUPER_ACE";
        } else {
            _un.squad_type = "PLATOON_3";
        }
    }
    if (!variable_struct_exists(_un, "squad_members_count")) {
        _un.squad_members_count = (_un.squad_type == "PLATOON_3") ? 3 : 1;
    }
    if (!variable_struct_exists(_un, "squad_max_count")) {
        _un.squad_max_count = _un.squad_members_count;
    }
    if (!variable_struct_exists(_un, "move_type")) {
        if (_un.mech_type == "aether" || _un.mech_type == "zephyr" || _un.mech_type == "custom_aero") _un.move_type = "aero";
        else if (_un.mech_type == "kepler" || _un.mech_type == "oberon" || _un.mech_type == "custom_hover") _un.move_type = "hover";
        else if (_un.mech_type == "ballista" || _un.mech_type == "titan" || _un.mech_type == "custom_tread") _un.move_type = "treads";
        else _un.move_type = "biped";
    }
    if (!variable_struct_exists(_un, "space_adapted")) {
        _un.space_adapted = (_un.move_type == "aero" || _un.move_type == "hover");
    }
    if (!variable_struct_exists(_un, "targeted_limb")) _un.targeted_limb = "body";
    if (!variable_struct_exists(_un, "is_aimed_shot")) _un.is_aimed_shot = false;
}

// 6. In-Flight Physical Projectiles & Combat FX Queues
projectiles = [];
combat_fx = [];
floating_texts = [];

// 7. Tactical Combat Log
combat_log = [
    "GRAND-SCALE ISOMETRIC COMBAT INITIALIZED // SECTOR 4 MINING CLAIM",
    "Allied Battlegroup deployed: 8 Mobile Suits (Alpha & Bravo Squadrons)",
    "Hostile Syndicate Battlegroup detected: 13 Mobile Suits (Reaver Vanguard)",
    ">> THEATER ESCALATION: " + (instance_exists(obj_GameManager) ? obj_GameManager.timeline_era_name : "Early War") + " (Era " + (instance_exists(obj_GameManager) ? string(obj_GameManager.timeline_era) : "1") + ")",
    ">> TACTICAL COMMAND: WASD/Drag to Pan, Wheel to Zoom, TAB to cycle units, [F] to rotate perspective!"
];

add_log = function(_msg) {
    array_push(combat_log, _msg);
    if (array_length(combat_log) > 8) {
        array_delete(combat_log, 0, 1);
    }
};

add_floating_text = function(_x, _y, _txt, _col) {
    array_push(floating_texts, {
        x: _x,
        y: _y,
        text: _txt,
        color: _col,
        alpha: 1.0,
        timer: 60,
        vy: -1.3
    });
};

// 8. Dynamic Sprite Selector (Front vs Back Perspective & Actions)
get_unit_sprite = function(_u) {
    var _is_back = iso_is_back_facing(_u.facing);
    var _type = _u.mech_type;
    var _act = _u.anim_state;

    // Conventional Vehicles (spr_veh_*) & Infantry Squads (spr_inf_*) lookup (Doc 38)
    if (string_copy(_type, 1, 4) == "veh_" || string_copy(_type, 1, 4) == "inf_") {
        var _base_spr_name = "spr_" + _type;
        var _action_suffix = "_idle";
        if (_u.is_destroyed || _act == "destroyed" || _act == "defeat") _action_suffix = "_defeat";
        else if (_act == "fire" || _act == "fire_rifle" || _act == "fire_chaingun") _action_suffix = "_fire";
        else if (_is_back) _action_suffix = "_back_idle";

        var _cand = asset_get_index(_base_spr_name + _action_suffix);
        if (_cand != -1 && sprite_exists(_cand)) return _cand;
        var _cand_idle = asset_get_index(_base_spr_name + "_idle");
        if (_cand_idle != -1 && sprite_exists(_cand_idle)) return _cand_idle;
    }

    if (_u.is_destroyed) {
        return spr_ms_ironclad_destroyed;
    }

    // 1. Direct sprite asset override if defined on unit (docs/29)
    if (variable_struct_exists(_u, "sprite_asset") && sprite_exists(_u.sprite_asset)) {
        if (_is_back) {
            var _spr_name = sprite_get_name(_u.sprite_asset);
            var _back_spr_name = string_replace(_spr_name, "_idle", "_back_idle");
            var _back_asset = asset_get_index(_back_spr_name);
            if (_back_asset != -1 && sprite_exists(_back_asset)) {
                return _back_asset;
            }
        } else {
            return _u.sprite_asset;
        }
    }

    // 2. Dynamic catalog lookup from obj_GameManager (Universal 100-Suit Catalog)
    if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "get_mobile_suit")) {
        var _cat_entry = obj_GameManager.get_mobile_suit(_type);
        if (!is_undefined(_cat_entry) && is_struct(_cat_entry) && variable_struct_exists(_cat_entry, "sprite_asset")) {
            var _c_asset = _cat_entry.sprite_asset;
            var _c_idx = is_string(_c_asset) ? asset_get_index(_c_asset) : _c_asset;
            if (_c_idx != -1 && sprite_exists(_c_idx)) {
                if (_is_back) {
                    var _s_name = sprite_get_name(_c_idx);
                    var _b_name = string_replace(_s_name, "_idle", "_back_idle");
                    var _b_idx = asset_get_index(_b_name);
                    if (_b_idx != -1 && sprite_exists(_b_idx)) return _b_idx;
                }
                return _c_idx;
            }
        }
    }

    // 3. Dynamic naming convention lookup (spr_ms_<type>_idle / _back_idle)
    var _cand_idle = asset_get_index("spr_ms_" + _type + "_idle");
    if (_cand_idle != -1 && sprite_exists(_cand_idle)) {
        if (_is_back) {
            var _cand_back = asset_get_index("spr_ms_" + _type + "_back_idle");
            if (_cand_back != -1 && sprite_exists(_cand_back)) return _cand_back;
        }
        return _cand_idle;
    }

    if (_is_back) {
        // DEDICATED BACK-FACING ISOMETRIC SPRITES (160x160, origin 80, 145)
        // Terran Mass-Production Candidates & Lineage
        // Player Custom Combinations Back
        if (_type == "custom_biped" || _type == "vanguard_heavy" || _type == "bp_player_vanguard_heavy") return spr_ms_custom_biped_heavy_back_idle;
        if (_type == "custom_hover" || _type == "ghost_sniper" || _type == "bp_player_ghost_sniper") return spr_ms_custom_hover_sniper_back_idle;
        if (_type == "custom_tread" || _type == "scrapper_brawler" || _type == "bp_player_scrapper_brawler") return spr_ms_custom_tread_artillery_back_idle;
        if (_type == "custom_aero" || _type == "stratos_interceptor" || _type == "bp_player_stratos_interceptor") return spr_ms_custom_aero_striker_back_idle;

        if (_type == "ballista") return spr_ms_ballista_back_idle;
        if (_type == "centurion") return spr_ms_centurion_back_idle;
        if (_type == "trenchcoat") return spr_ms_trenchcoat_back_idle;

        // Colony Mass-Production Candidates & Lineage
        if (_type == "zephyr") return spr_ms_zephyr_back_idle;
        if (_type == "kepler") return spr_ms_kepler_back_idle;
        if (_type == "oberon") return spr_ms_oberon_back_idle;

        // Syndicate Mass-Production Candidates & Lineage
        if (_type == "gorgon") return spr_ms_gorgon_back_idle;
        if (_type == "bloodhound") return spr_ms_bloodhound_back_idle;
        if (_type == "vandal") return spr_ms_vandal_back_idle;

        // Zaibatsu Mass-Production Candidates & Lineage
        if (_type == "kage" || _type == "shinobi") return spr_ms_kage_back_idle;
        if (_type == "ronin") return spr_ms_ronin_back_idle;
        if (_type == "tessen") return spr_ms_tessen_back_idle;

        // Apex Prototypes & Juggernauts
        if (_type == "hephaestus") return spr_ms_hephaestus_avatar_back_idle;
        if (_type == "titan" || _type == "juggernaut") return spr_ms_titan_proto_back_idle;

        // Core Faction Archetypes
        if (_type == "aether" || _type == "sylph" || _type == "helios" || _type == "seraphim" || _type == "stratos" || _type == "pmc_02") return spr_ms_aether_back_idle;
        if (_type == "hyena" || _type == "marauder" || _type == "slag_lobber" || _type == "chimera" || _type == "scrapper" || _type == "pmc_03") return spr_ms_hyena_back_idle;
        if (_type == "muramasa" || _type == "raiden" || _type == "susanoo" || _type == "ghost" || _type == "pmc_04") return spr_ms_muramasa_back_idle;
        return spr_ms_ironclad_back_idle;
    } else {
        // FRONT PERSPECTIVE SPRITES (160x160, origin 80, 145)
        if (_act == "fire_rifle" && (_type == "ironclad" || _type == "bulwark" || _type == "behemoth" || _type == "vanguard" || _type == "pmc_01")) return spr_ms_ironclad_fire_rifle;
        if (_act == "fire_chaingun" && (_type == "ironclad" || _type == "bulwark" || _type == "behemoth" || _type == "vanguard" || _type == "pmc_01")) return spr_ms_ironclad_fire_chaingun;
        if (_act == "fire_missiles" && (_type == "ironclad" || _type == "bulwark" || _type == "behemoth" || _type == "vanguard" || _type == "pmc_01")) return spr_ms_ironclad_fire_missiles;
        if (_act == "melee" && (_type == "ironclad" || _type == "bulwark" || _type == "behemoth" || _type == "vanguard" || _type == "pmc_01")) return spr_ms_ironclad_attack_melee;
        if (_act == "hit" && (_type == "ironclad" || _type == "bulwark" || _type == "behemoth" || _type == "vanguard" || _type == "pmc_01")) return spr_ms_ironclad_hit_kinetic;

        if (_act == "fire_beam" && (_type == "aether" || _type == "sylph" || _type == "helios" || _type == "seraphim" || _type == "stratos" || _type == "pmc_02")) return spr_ms_aether_fire_beam;
        if (_act == "melee" && (_type == "aether" || _type == "sylph" || _type == "helios" || _type == "seraphim" || _type == "stratos" || _type == "pmc_02")) return spr_ms_aether_attack_saber;
        if (_act == "boost" && (_type == "aether" || _type == "sylph" || _type == "helios" || _type == "seraphim" || _type == "stratos" || _type == "pmc_02")) return spr_ms_aether_boost;

        if (_act == "fire_flak" && (_type == "hyena" || _type == "marauder" || _type == "slag_lobber" || _type == "chimera" || _type == "scrapper" || _type == "pmc_03")) return spr_ms_hyena_fire_flak;
        if (_act == "melee" && (_type == "hyena" || _type == "marauder" || _type == "slag_lobber" || _type == "chimera" || _type == "scrapper" || _type == "pmc_03")) return spr_ms_hyena_attack_claw;
        if (_act == "walk" && (_type == "hyena" || _type == "marauder" || _type == "slag_lobber" || _type == "chimera" || _type == "scrapper" || _type == "pmc_03")) return spr_ms_hyena_walk;

        if (_act == "fire_plasma" && (_type == "muramasa" || _type == "ronin" || _type == "raiden" || _type == "susanoo" || _type == "ghost" || _type == "pmc_04")) return spr_ms_muramasa_fire_plasma;
        if (_act == "melee" && (_type == "muramasa" || _type == "ronin" || _type == "raiden" || _type == "susanoo" || _type == "ghost" || _type == "pmc_04")) return spr_ms_muramasa_attack_blade;
        if (_act == "sprint" && (_type == "muramasa" || _type == "ronin" || _type == "raiden" || _type == "susanoo" || _type == "ghost" || _type == "pmc_04")) return spr_ms_muramasa_sprint;

        if (_act == "fire_siege" && (_type == "siegebreaker" || _type == "behemoth" || _type == "slag_lobber")) return spr_ms_siegebreaker_fire;
        if (_act == "anchor" && (_type == "siegebreaker" || _type == "behemoth" || _type == "slag_lobber")) return spr_ms_siegebreaker_anchor;

        // Default Front Idles (160x160, origin 80, 145)
        if (_type == "aether" || _type == "sylph" || _type == "helios" || _type == "seraphim" || _type == "stratos" || _type == "pmc_02") return spr_ms_aether_idle;
        if (_type == "hyena" || _type == "marauder" || _type == "slag_lobber" || _type == "chimera" || _type == "scrapper" || _type == "pmc_03") return spr_ms_hyena_idle;
        if (_type == "muramasa" || _type == "ronin" || _type == "raiden" || _type == "susanoo" || _type == "ghost" || _type == "pmc_04") return spr_ms_muramasa_idle;
        if (_type == "siegebreaker" || _type == "behemoth") return spr_ms_siegebreaker_anchor;
        // Player Custom Combinations Front
        if (_type == "custom_biped" || _type == "vanguard_heavy" || _type == "bp_player_vanguard_heavy") return spr_ms_custom_biped_heavy_idle;
        if (_type == "custom_hover" || _type == "ghost_sniper" || _type == "bp_player_ghost_sniper") return spr_ms_custom_hover_sniper_idle;
        if (_type == "custom_tread" || _type == "scrapper_brawler" || _type == "bp_player_scrapper_brawler") return spr_ms_custom_tread_artillery_idle;
        if (_type == "custom_aero" || _type == "stratos_interceptor" || _type == "bp_player_stratos_interceptor") return spr_ms_custom_aero_striker_idle;

        if (_type == "ballista") return spr_ms_ballista_idle;
        if (_type == "centurion") return spr_ms_centurion_idle;
        if (_type == "trenchcoat") return spr_ms_trenchcoat_idle;
        if (_type == "zephyr") return spr_ms_zephyr_idle;
        if (_type == "kepler") return spr_ms_kepler_idle;
        if (_type == "oberon") return spr_ms_oberon_idle;
        if (_type == "gorgon") return spr_ms_gorgon_idle;
        if (_type == "bloodhound") return spr_ms_bloodhound_idle;
        if (_type == "vandal") return spr_ms_vandal_idle;
        if (_type == "kage" || _type == "shinobi") return spr_ms_kage_idle;
        if (_type == "ronin") return spr_ms_ronin_idle;
        if (_type == "tessen") return spr_ms_tessen_idle;
        if (_type == "hephaestus") return spr_ms_hephaestus_avatar;
        if (_type == "titan" || _type == "juggernaut") return spr_ms_titan_proto;
        return spr_ms_ironclad_idle;
    }
};

// 9. Combat Distance & Hit Probability Functions
calculate_distance = function(_c1, _r1, _c2, _r2) {
    return abs(_c1 - _c2) + abs(_r1 - _r2);
};

calculate_hit_chance = function(_atk, _def, _dist, _wpn = undefined) {
    var _base = _atk.accuracy;
    var _eva = _def.evasion;
    if (_atk.team == "ALLIED") {
        _base += floor(scr_research_get_bonus("hit_accuracy") * 100);
    }
    if (_def.team == "ALLIED") {
        _eva += floor(scr_research_get_bonus("evasion") * 100);
    }

    // Pilot Rank Perks & Frame Affinity Resonance (Doc 51)
    if (variable_struct_exists(_atk, "has_affinity_match") && _atk.has_affinity_match) {
        _base += 8;
    }
    if (variable_struct_exists(_def, "has_affinity_match") && _def.has_affinity_match) {
        _eva += 8;
    }
    if (variable_struct_exists(_atk, "rank_perks") && is_array(_atk.rank_perks)) {
        for (var pk = 0; pk < array_length(_atk.rank_perks); pk++) {
            if (_atk.rank_perks[pk] == "Deadly Aim") _base += 8;
        }
    }
    if (variable_struct_exists(_def, "rank_perks") && is_array(_def.rank_perks)) {
        for (var pk = 0; pk < array_length(_def.rank_perks); pk++) {
            if (_def.rank_perks[pk] == "Vernier Drift") _eva += 10;
        }
    }

    // Suppression aim penalty (Goal F)
    if (variable_struct_exists(_atk, "is_suppressed") && _atk.is_suppressed) {
        _base -= 20;
    }

    // Directional facing hit modifiers (Goal F)
    var _inc_dir = iso_get_facing(_def.grid_c, _def.grid_r, _atk.grid_c, _atk.grid_r);
    var _is_rear = (_inc_dir == (_def.facing + 2) % 4);
    var _is_flank = (_inc_dir == (_def.facing + 1) % 4 || _inc_dir == (_def.facing + 3) % 4);
    if (_is_rear) {
        _base += 30;
    } else if (_is_flank) {
        _base += 15;
    }

    // Blueprint Vulnerability Exploitation (Arms Dealer Paradox / Known Specs)
    if (_def[$ "blueprint_exploited"] == true) {
        _base += 15;
    }

    // Gihren's Greed Pilot Limit % (Genkai) Cap Calculus (Doc 20)
    var _atk_lim = _atk[$ "pilot_limit_pct"] ?? 115;
    var _atk_ref = _atk[$ "pilot_reflexes"] ?? 50;
    var _atk_cap_bonus = min(_atk_ref, _atk_lim - 100) * 0.45;
    _base += _atk_cap_bonus;

    var _def_lim = _def[$ "pilot_limit_pct"] ?? 115;
    var _def_ref = _def[$ "pilot_reflexes"] ?? 50;
    var _def_cap_bonus = min(_def_ref, _def_lim - 100) * 0.50;
    _eva += _def_cap_bonus;

    // Minovsky / ECM Particle Dispersion Jamming (Doc 20)
    var _ecm_jamming = (_def[$ "ecm_dispersion_pct"] ?? 20) * 0.20;
    _base -= _ecm_jamming;

    // Terrain Adaptability Modifiers
    var _def_ter = _def[$ "terrain"] ?? { ground: "A" };
    if (_def_ter[$ "ground"] == "S") _eva += 12;
    else if (_def_ter[$ "ground"] == "C") _eva -= 10;

    if (_def.braced) _eva += 35;
    if (!_atk.components.head.intact) _base -= 40;
    if (!_def.components.legs.intact) _eva = 0;
    var _cov = (grid_cover[_def.grid_c][_def.grid_r] == 1) ? 25 : ((grid_cover[_def.grid_c][_def.grid_r] == 2) ? 40 : 0);
    if (!is_undefined(_wpn) && variable_struct_exists(_wpn, "proj_type")) {
        if (_wpn.proj_type == "KINETIC_CANNON" || _wpn.proj_type == "MISSILE" || _wpn.proj_type == "TACHYON_BEAM") {
            _cov = floor(_cov * 0.50);
        }
    }
    // Milestone 56: Pilot Cockpit Fatigue Degradation
    if (variable_struct_exists(_atk, "fatigue")) {
        if (_atk.fatigue >= 75) {
            _base -= 20; // Exhausted / Combat Shock
        } else if (_atk.fatigue >= 50) {
            _base -= 10; // Fatigued
        } else if (_atk.fatigue >= 25) {
            _base -= 5;  // Winded
        }
    }
    // Milestone 56: Mutated Traits Modifiers
    if (variable_struct_exists(_atk, "mutated_traits") && is_array(_atk.mutated_traits)) {
        if (array_contains(_atk.mutated_traits, "Cybernetic Reflex Augment")) {
            _base += 6;
        }
    }
    if (variable_struct_exists(_def, "mutated_traits") && is_array(_def.mutated_traits)) {
        if (array_contains(_def.mutated_traits, "Ghost of Phobos")) {
            _eva += 10;
        }
    }

    var _elev_diff = _atk.elev - _def.elev;
    var _elev_bonus = (_elev_diff > 0) ? (_elev_diff * 10) : (_elev_diff * 15);
    return clamp(_base - (_eva * 0.40) - _cov - (_dist * 2) + _elev_bonus, 15, 95);
};

// 10. Recompute Movement Tiles for Selected Unit with Dynamic Terrain Costs
get_terrain_move_cost = function(_u, _from_c, _from_r, _to_c, _to_r) {
    if (_to_c < 0 || _to_c >= grid_cols || _to_r < 0 || _to_r >= grid_rows) return 999;
    var _terr = grid_terrain[_to_c][_to_r];
    var _from_elev = grid_elev[_from_c][_from_r];
    var _to_elev = grid_elev[_to_c][_to_r];
    var _elev_diff = _to_elev - _from_elev;

    var _m_type = _u[$ "move_type"] ?? "biped";
    var _sp_adapt = _u[$ "space_adapted"] ?? false;

    if (abs(_elev_diff) > 1 && _m_type != "aero") return 999;

    var _base_cost = 1;

    if (_m_type == "aero") {
        _base_cost = 1;
    } else if (_m_type == "hover") {
        if (_terr == 3) _base_cost = 1;
        else if (_terr == 2) _base_cost = 1;
        else if (_terr == 4) return 999;
        else if (_terr == 5) _base_cost = 2;
        else _base_cost = 1;
        if (_elev_diff > 0) _base_cost += 1;
    } else if (_m_type == "treads") {
        if (_terr == 2) _base_cost = 1;
        else if (_terr == 3) return 999;
        else if (_terr == 4) return 999;
        else if (_terr == 5) _base_cost = 1;
        else _base_cost = 1;
        if (_elev_diff > 0) _base_cost += 1;
    } else {
        if (_terr == 1) _base_cost = 1;
        else if (_terr == 2) _base_cost = 2;
        else if (_terr == 3) _base_cost = 3;
        else if (_terr == 4) return 999;
        else if (_terr == 5) _base_cost = 2;
        else _base_cost = 1;
        if (_elev_diff > 0) _base_cost += 1;
    }

    if (map_definitions[current_map_id].theater == "SPACE" && _m_type != "aero" && !_sp_adapt) {
        _base_cost += 1;
    }

    return _base_cost;
};

recalculate_moves = function() {
    valid_move_tiles = [];
    if (selected_unit_idx < 0 || selected_unit_idx >= array_length(units)) return;
    var _sel = units[selected_unit_idx];
    if (_sel.current_ap <= 0 || _sel.is_destroyed) return;
    var _ap_pool = _sel.components.legs.intact ? _sel.current_ap : 1;
    if (_sel.team == "ALLIED") {
        _ap_pool += floor(scr_research_get_bonus("move_range"));
    }
    if (variable_struct_exists(_sel, "is_suppressed") && _sel.is_suppressed) {
        _ap_pool = max(1, _ap_pool - 1);
    }

    for (var c = 0; c < grid_cols; c++) {
        for (var r = 0; r < grid_rows; r++) {
            var _occupied = false;
            for (var u = 0; u < array_length(units); u++) {
                var _chk = units[u];
                if (!_chk.is_destroyed && _chk != _sel && _chk.grid_c == c && _chk.grid_r == r) {
                    _occupied = true;
                    break;
                }
            }
            if (_occupied) continue;

            var _cost = get_terrain_move_cost(_sel, _sel.grid_c, _sel.grid_r, c, r);
            if (_cost >= 999) continue;

            var _d = calculate_distance(_sel.grid_c, _sel.grid_r, c, r);
            var _tot = _d * _cost;
            if (_tot <= _ap_pool && _d > 0) {
                array_push(valid_move_tiles, { col: c, row: r, cost: _tot });
            }
        }
    }
};

// 11. Cycle Units & Facing Controls
select_unit = function(_idx) {
    if (_idx >= 0 && _idx < array_length(units)) {
        selected_unit_idx = _idx;
        var _u = units[_idx];
        cam_target_x = 683.0 - ((_u.grid_c - _u.grid_r) * (tile_w * 0.5) * zoom);
        cam_target_y = 384.0 - (((_u.grid_c + _u.grid_r) * (tile_h * 0.5) - (_u.elev * elev_h)) * zoom);
        recalculate_moves();
    }
};

cycle_allied_unit = function() {
    var _start = selected_unit_idx;
    for (var i = 1; i <= array_length(units); i++) {
        var _idx = (_start + i) % array_length(units);
        var _u = units[_idx];
        if (_u.team == "ALLIED" && !_u.is_destroyed && _u.current_ap > 0) {
            select_unit(_idx);
            add_log("[UNIT SELECTED] Active control: " + _u.callsign);
            return;
        }
    }
    for (var i = 1; i <= array_length(units); i++) {
        var _idx = (_start + i) % array_length(units);
        var _u = units[_idx];
        if (_u.team == "ALLIED" && !_u.is_destroyed) {
            select_unit(_idx);
            return;
        }
    }
};

cycle_unit_facing = function(_u) {
    _u.facing = (_u.facing + 1) % 4;
    var _dir_names = ["SE (Front-Right)", "SW (Front-Left)", "NE (Back-Right)", "NW (Back-Left)"];
    add_log("[PERSPECTIVE ROTATE] " + _u.callsign + " facing -> " + _dir_names[_u.facing]);
};

// 12. Spawn Physical Projectile Across Screen & Platoon Synchronized Volleys
legacy_spawn_combat_projectile = function(_atk, _def, _wpn) {
    var _sx = iso_to_screen_x(_atk.grid_c, _atk.grid_r, _atk.elev, cam_x, cam_y, zoom);
    var _sy = iso_to_screen_y(_atk.grid_c, _atk.grid_r, _atk.elev, cam_x, cam_y, zoom) - (40 * zoom);
    var _tx = iso_to_screen_x(_def.grid_c, _def.grid_r, _def.elev, cam_x, cam_y, zoom);
    var _ty = iso_to_screen_y(_def.grid_c, _def.grid_r, _def.elev, cam_x, cam_y, zoom) - (40 * zoom);

    var _dist = calculate_distance(_atk.grid_c, _atk.grid_r, _def.grid_c, _def.grid_r);
    var _hit_chance = calculate_hit_chance(_atk, _def, _dist);
    if (_atk.is_aimed_shot) _hit_chance = max(10, _hit_chance - 15);

    var _cb = method({ atk: _atk, def: _def, wpn: _wpn, hit_pct: _hit_chance, mgr: id }, function() {
        mgr.resolve_combat_impact(atk, def, wpn, hit_pct);
    });

    // Lead mech main projectile (with impact callback)
    var _proj = create_projectile(_wpn.proj_type, _sx, _sy, 0, _tx, _ty, 0, _cb);
    array_push(projectiles, _proj);
    scr_audio_play_weapon(_wpn.short_name);

    // Gihren's Greed 3-Mech Platoon Synchronized Volley
    if (_atk.squad_type == "PLATOON_3") {
        if (_atk.squad_members_count >= 2) {
            var _p2 = create_projectile(_wpn.proj_type, _sx - 18 * zoom, _sy - 10 * zoom, 0, _tx - 8 * zoom, _ty - 6 * zoom, 0, undefined);
            array_push(projectiles, _p2);
        }
        if (_atk.squad_members_count >= 3) {
            var _p3 = create_projectile(_wpn.proj_type, _sx - 18 * zoom, _sy + 10 * zoom, 0, _tx + 8 * zoom, _ty + 6 * zoom, 0, undefined);
            array_push(projectiles, _p3);
        }
    }
};

// 13. Resolve Impact, Front Mission Modular Limb Damage & Platoon Attrition
resolve_combat_impact = function(_atk, _def, _wpn, _hit_chance) {
    var _roll = irandom_range(1, 100);
    var _hit = (_roll <= _hit_chance);

    var _def_sx = iso_to_screen_x(_def.grid_c, _def.grid_r, _def.elev, cam_x, cam_y, zoom);
    var _def_sy = iso_to_screen_y(_def.grid_c, _def.grid_r, _def.elev, cam_x, cam_y, zoom) - (40 * zoom);

    if (_hit) {
        screen_shake = max(screen_shake, 7.0);
        _def.recoil_shake = 8.0;
        _def.anim_state = "hit";
        _def.anim_timer = 25;

        // Front Mission Aimed Shot Precision or Random Limb Dispersion
        var _hit_part = "torso";
        if (_atk.is_aimed_shot && _atk.targeted_limb != "") {
            _hit_part = _atk.targeted_limb;
        } else {
            var _part_roll = irandom_range(1, 100);
            if (_part_roll <= 40) _hit_part = "torso";
            else if (_part_roll <= 55) _hit_part = "arm_left";
            else if (_part_roll <= 70) _hit_part = "arm_right";
            else if (_part_roll <= 90) _hit_part = "legs";
            else _hit_part = "head";
        }

        var _limb = _def.components[$ _hit_part];

        // Platoon Volley Scaling: 100% at 3/3 grunts, 75% at 2/3, 50% at 1/3
        var _squad_mult = 1.0;
        if (_atk.squad_type == "PLATOON_3") {
            _squad_mult = (_atk.squad_members_count == 3) ? 1.0 : ((_atk.squad_members_count == 2) ? 0.75 : 0.50);
        }
        var _raw_dmg = floor((_wpn.damage + irandom_range(-15, 20)) * _squad_mult);

        // Directional Facing Damage Multipliers (Goal F: Flanking & Rear Ambush)
        var _inc_dir = iso_get_facing(_def.grid_c, _def.grid_r, _atk.grid_c, _atk.grid_r);
        var _is_rear = (_inc_dir == (_def.facing + 2) % 4);
        var _is_flank = (_inc_dir == (_def.facing + 1) % 4 || _inc_dir == (_def.facing + 3) % 4);
        if (_is_rear) {
            _raw_dmg = floor(_raw_dmg * 1.40);
            add_log("[REAR CORE HIT +40%]");
        } else if (_is_flank) {
            _raw_dmg = floor(_raw_dmg * 1.20);
            add_log("[FLANKING ANGLE +20%]");
        }

        // High Ground Elevation Velocity Bonus (Goal F)
        var _elev_diff = _atk.elev - _def.elev;
        if (_elev_diff > 0) {
            _raw_dmg = floor(_raw_dmg * (1.0 + (_elev_diff * 0.15)));
            add_log("[HIGH GROUND +" + string(_elev_diff * 15) + "% VELOCITY]");
        } else if (_elev_diff < 0) {
            _raw_dmg = floor(_raw_dmg * 0.85);
            add_log("[UPHILL -15% KINETIC]");
        }

        // Researched Weapon Multipliers (Allied Attacker)
    if (_atk.team == "ALLIED") {
        if (_wpn.proj_type == "KINETIC" || _wpn.proj_type == "ROTARY_VULCAN") {
            _raw_dmg = floor(_raw_dmg * (1.0 + scr_research_get_bonus("kinetic_dmg")));
        } else if (_wpn.proj_type == "BEAM" || _wpn.proj_type == "ENERGY") {
            _raw_dmg = floor(_raw_dmg * (1.0 + scr_research_get_bonus("beam_dmg")));
        } else if (_wpn.proj_type == "MISSILE") {
            _raw_dmg = floor(_raw_dmg * (1.0 + scr_research_get_bonus("missile_dmg")));
        } else if (_wpn.proj_type == "MELEE") {
            _raw_dmg = floor(_raw_dmg * (1.0 + scr_research_get_bonus("melee_pen")));
        }
    }
    var _mitigated_dmg = max(15, _raw_dmg - _limb.armor);
    // Researched Shield / Barrier Multipliers (Allied Defender)
    if (_def.team == "ALLIED") {
        if (_wpn.proj_type == "BEAM" || _wpn.proj_type == "ENERGY") {
            _mitigated_dmg = floor(_mitigated_dmg * (1.0 - scr_research_get_bonus("beam_resist")));
        }
        _mitigated_dmg = floor(_mitigated_dmg * (1.0 - scr_research_get_bonus("barrier_absorb")));
        _mitigated_dmg = max(5, _mitigated_dmg);
    }
        scr_audio_play_impact("kinetic", (_mitigated_dmg > 50));

        // Bastion & Cover Degradation (Goal F)
        if (grid_cover[_def.grid_c][_def.grid_r] == 2) {
            grid_cover[_def.grid_c][_def.grid_r] = 1;
            add_log("[BASTION CRACKED -> RUBBLE] Heavy ordnance reduced bastion to low rubble at (" + string(_def.grid_c) + ", " + string(_def.grid_r) + ")!");
        } else if (grid_cover[_def.grid_c][_def.grid_r] == 1) {
            grid_cover[_def.grid_c][_def.grid_r] = 0;
            add_log("[COVER DESTROYED] Rubble pulverized at (" + string(_def.grid_c) + ", " + string(_def.grid_r) + ")!");
        }

        // Phase Barrier Absorption (Goal G)
        if (variable_struct_exists(_def, "barrier_cur") && _def.barrier_cur > 0) {
            var _abs = min(_mitigated_dmg, _def.barrier_cur);
            _def.barrier_cur -= _abs;
            _mitigated_dmg -= _abs;
            add_log("[PHASE BARRIER ABSORBED] Phase Barrier absorbed " + string(_abs) + " damage! (" + string(_def.barrier_cur) + " remaining)");
            if (_def.barrier_cur <= 0) {
                add_log("[BARRIER SHATTERED] Phase Barrier Emitter overloaded!");
            }
        }

        _limb.cur = max(0, _limb.cur - _mitigated_dmg);

        array_push(combat_fx, {
            sprite: spr_fx_explosion,
            x: _def_sx,
            y: _def_sy,
            frame: 0.0,
            speed: 0.25,
            scale: 1.2 * zoom
        });

        add_floating_text(_def_sx, _def_sy - 30, "-" + string(_mitigated_dmg) + " " + string_upper(_limb.name) + "!", c_yellow);
        add_log("[HIT] " + _atk.callsign + " struck " + _def.callsign + " " + _limb.name + " for " + string(_mitigated_dmg) + " damage!");

        // Tactical Radio Duel Bark (Doc 52 / Doc 53)
        if (irandom_range(1, 100) <= 35) {
            var _atk_name = _atk.pilot_name + " [" + _atk.callsign + "]";
            var _atk_spr = (variable_struct_exists(_atk, "sprite_asset") && sprite_exists(_atk.sprite_asset)) ? _atk.sprite_asset : spr_portrait_commander_male;
            var _bark_col = (_atk.team == "ALLIED") ? make_color_rgb(100, 220, 255) : make_color_rgb(255, 100, 100);
            var _bark_txt = "Target locked! Kinetic impact confirmed!";
            if (_atk.team == "ALLIED") {
                var _ab = ["Target locked and hammered! Keep the pressure on!", "Kinetic penetration confirmed! Pushing through their line!", "Good hit! Their actuators are smoking!"];
                _bark_txt = _ab[irandom(array_length(_ab) - 1)];
            } else {
                var _eb = ["Contract target struck! Kinetic bill itemized.", "Organic telemetry fading. Clean kinetic delivery.", "That armor won't save you from our volley!"];
                _bark_txt = _eb[irandom(array_length(_eb) - 1)];
            }
            scr_vn_trigger_combat_intercom(_atk_name, _atk_spr, _bark_txt, 150, _bark_col);
        }

        // Platoon Squad Member Casualty Attrition
        if (_def.squad_type == "PLATOON_3") {
            var _hp_ratio = _def.components.torso.cur / _def.components.torso.max;
            if (_hp_ratio < 0.33 && _def.squad_members_count > 1) {
                _def.squad_members_count = 1;
                add_floating_text(_def_sx, _def_sy - 65, "WINGMAN DESTROYED! [1/3 REMAINING]", make_color_rgb(255, 120, 60));
                add_log("[SQUAD CASUALTY] " + _def.callsign + " Wingman 2 destroyed! Only squad leader operational.");
                array_push(combat_fx, { sprite: spr_fx_explosion, x: _def_sx - 22 * zoom, y: _def_sy, frame: 0.0, speed: 0.3, scale: 1.0 * zoom });
            } else if (_hp_ratio < 0.66 && _def.squad_members_count > 2) {
                _def.squad_members_count = 2;
                add_floating_text(_def_sx, _def_sy - 65, "WINGMAN CASUALTY! [2/3 REMAINING]", make_color_rgb(255, 160, 60));
                add_log("[SQUAD CASUALTY] " + _def.callsign + " Wingman 1 destroyed! 2/3 operational.");
                array_push(combat_fx, { sprite: spr_fx_explosion, x: _def_sx + 22 * zoom, y: _def_sy, frame: 0.0, speed: 0.3, scale: 1.0 * zoom });
            }
        }

        // Front Mission Component Destruction Debuffs
        if (_limb.cur <= 0 && _limb.intact) {
            _limb.intact = false;
            add_floating_text(_def_sx, _def_sy - 55, "COMPONENT DESTROYED: " + string_upper(_limb.name), c_red);
            add_log("[CRITICAL BREACH] " + _def.callsign + " " + _limb.name + " HAS BEEN SEVERED!");

            if (_hit_part == "torso") {
                _def.is_destroyed = true;
                scr_audio_play_sfx(snd_explosion_large, 1.0, 0.05);
                _def.anim_state = "destroyed";
                screen_shake = 14.0;
                add_floating_text(_def_sx, _def_sy - 80, "REACTOR DETONATION // CHASSIS DESTROYED", c_red);
                add_log("[CATASTROPHIC KILL] " + _def.callsign + " REACTOR BREACH! Unit neutralized.");

                // Intercom Ejection Bark (Doc 53)
                var _def_name = _def.pilot_name + " [" + _def.callsign + "]";
                var _def_spr = (variable_struct_exists(_def, "sprite_asset") && sprite_exists(_def.sprite_asset)) ? _def.sprite_asset : spr_portrait_commander_male;
                var _ej_bark = (_def.team == "HOSTILE") ? "Core containment breached! Ejecting flight recorder—!" : "Mayday! Reactor redline! Punching out!";
                scr_vn_trigger_combat_intercom(_def_name, _def_spr, _ej_bark, 180, make_color_rgb(255, 60, 60));

                // Mobile Suit Global Attrition & Service Record Hook (docs/35)
                if (instance_exists(obj_BlueprintManager)) {
                    var _vic_chassis = _def[$ "chassis_id"] ?? (_def[$ "mech_type"] ?? "ironclad");
                    var _atk_chassis = _atk[$ "chassis_id"] ?? (_atk[$ "mech_type"] ?? "ironclad");
                    obj_BlueprintManager.record_suit_casualty(_vic_chassis, _atk_chassis);
                }

                // Nemesis System Event Dispatch Hook (Document 19)
                if (instance_exists(obj_NemesisManager)) {
                    var _vic_id = _def[$ "character_id"] ?? _def[$ "pilot_name"] ?? _def.id;
                    var _atk_id = _atk[$ "character_id"] ?? _atk[$ "pilot_name"] ?? "player";
                    scr_nemesis_event_dispatch(_vic_id, _atk_id, "combat_kill");
                }
            } else if (_hit_part == "legs") {
                _def.current_ap = min(_def.current_ap, 1);
                _def.evasion = 0;
                add_log("[MOBILITY KILL] " + _def.callsign + " hydraulic bipedal limbs crippled! Evasion 0%, AP capped at 1.");
            } else if (_hit_part == "arm_left" || _hit_part == "arm_right") {
                _def.accuracy = max(20, _def.accuracy - 25);
                add_log("[DISARMED] " + _def.callsign + " " + _limb.name + " severed! Accuracy penalized -25%.");
            } else if (_hit_part == "head") {
                _def.accuracy = max(10, _def.accuracy - 40);
                add_log("[SENSORS BLINDED] " + _def.callsign + " head sensor array destroyed! Accuracy -40%.");
            }
        }
    } else {
        array_push(combat_fx, {
            sprite: spr_fx_spark,
            x: _def_sx + irandom_range(-20, 20),
            y: _def_sy + irandom_range(-20, 20),
            frame: 0.0,
            speed: 0.35,
            scale: 1.0 * zoom
        });
        add_floating_text(_def_sx, _def_sy - 25, "DEFLECTED // GLANCING", c_aqua);
        add_log("[DEFLECTION] Attack glanced off " + _def.callsign + " armor!");

        // Deflection / Glancing Intercom Bark (Doc 53)
        if (irandom_range(1, 100) <= 25) {
            var _def_name = _def.pilot_name + " [" + _def.callsign + "]";
            var _def_spr = (variable_struct_exists(_def, "sprite_asset") && sprite_exists(_def.sprite_asset)) ? _def.sprite_asset : spr_portrait_commander_male;
            var _db = ["Armor deflection confirmed! Is that the best you can hit?", "Kinetic dispersion held! Returning fire!", "Glancing blow! Hull integrity intact!"];
            var _def_bark = _db[irandom(array_length(_db) - 1)];
            scr_vn_trigger_combat_intercom(_def_name, _def_spr, _def_bark, 140, make_color_rgb(120, 255, 200));
        }
    }
};


// =========================================================================
// GOAL G: APEX CRISIS BOSS ENGINE & ORBITAL BOMBARDMENT
// =========================================================================
is_crisis_boss_battle = false;
crisis_defeated = false;

setup_apex_crisis_boss = function() {
    var _boss = {
        id: "apex_boss_ouroboros",
        callsign: "DEUS-MACHINA: OUROBOROS PRIME",
        pilot_name: "ARCHEOTECH SINGULARITY AI",
        squad_type: "SUPER_ACE",
        squad_members_count: 1,
        team: "HOSTILE",
        grid_c: 9,
        grid_r: 9,
        elev: 2,
        facing: 2,
        is_aircraft: false,
        move_type: "hover",
        max_ap: 8,
        current_ap: 8,
        accuracy: 95,
        evasion: 25,
        is_boss: true,
        is_destroyed: false,
        barrier_cur: 800,
        barrier_max: 800,
        barrier_regen: 150,
        components: {
            torso:    { name: "Archeotech Singularity Core", cur: 2500, max: 2500, armor: 65, intact: true },
            head:     { name: "Quantum Cognition Array",     cur: 800,  max: 800,  armor: 45, intact: true },
            arm_left: { name: "Twin Particle Lance",         cur: 1200, max: 1200, armor: 55, intact: true },
            arm_right:{ name: "Super-Heavy Plasma Annihilator", cur: 1200, max: 1200, armor: 55, intact: true },
            legs:     { name: "Hover-Graviton Skirt Array",  cur: 1500, max: 1500, armor: 50, intact: true },
            backpack: { name: "Phase Barrier Emitter",       cur: 1000, max: 1000, armor: 40, intact: true }
        },
        weapons: [
            { name: "Super-Heavy Plasma Annihilator", short_name: "PLASMA", damage: 320, ap_cost: 3, heat_cost: 20, range_min: 1, range_max: 6, proj_type: "TACHYON_BEAM", anim_state: "fire" },
            { name: "Quantum Disruption Pulse", short_name: "Q-PULSE", damage: 180, ap_cost: 2, heat_cost: 15, range_min: 1, range_max: 4, proj_type: "BEAM_PULSE", anim_state: "fire" },
            { name: "Nanite Swarm Micro-Missiles", short_name: "NANITES", damage: 220, ap_cost: 3, heat_cost: 10, range_min: 2, range_max: 7, proj_type: "MICRO_MISSILE", anim_state: "fire" }
        ],
        damaged_parts: { head: false, torso: false, arm_left: false, arm_right: false, legs: false, backpack: false }
    };
    units[8] = _boss;
    add_log("[CRISIS INVASION] ANOMALOUS DREADNOUGHT SIGNATURE: " + _boss.callsign + " deployed!");
};

call_flagship_orbital_strike = function(_target_c, _target_r) {
    add_log("[ORBITAL STRIKE] USN-X Hephaestus firing Heavy Kinetic Lance at (" + string(_target_c) + ", " + string(_target_r) + ")!");
    screen_shake = max(screen_shake, 25.0);
    scr_audio_play_weapon("RAILGUN");

    for (var u = 0; u < array_length(units); u++) {
        var _un = units[u];
        if (!_un.is_destroyed && calculate_distance(_un.grid_c, _un.grid_r, _target_c, _target_r) <= 1) {
            var _strike_dmg = 550;
            if (variable_struct_exists(_un, "barrier_cur") && _un.barrier_cur > 0) {
                _un.barrier_cur = 0;
                add_log("[BARRIER SHATTERED] Phase Barrier Emitter overloaded by orbital bombardment!");
            }
            if (variable_struct_exists(_un, "components") && variable_struct_exists(_un.components, "backpack")) {
                _un.components.backpack.cur = max(0, _un.components.backpack.cur - _strike_dmg);
                if (_un.components.backpack.cur <= 0) {
                    _un.components.backpack.intact = false;
                    _un.barrier_max = 0;
                    _un.barrier_cur = 0;
                    add_log("[BARRIER SHATTERED] Phase Barrier Emitter destroyed!");
                }
            }
        }
    }
};

// Check if crisis boss battle is active
if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "active_crisis_boss_sortie") && obj_GameManager.active_crisis_boss_sortie) {
    is_crisis_boss_battle = true;
    obj_GameManager.active_crisis_boss_sortie = false;
    setup_apex_crisis_boss();
}

// =========================================================================
// GIHREN'S GREED + FRONT MISSION BATTLEGROUP STACK & COMMAND BUS STATE
// =========================================================================
stack_drawer_open = true;
stack_drawer_x = 1046.0;
stack_drawer_target_x = 1046.0;
stack_drawer_w = 320;

split_mode_active = false;
split_selected_units = {};
reorg_mode_active = false;

// Initialize formation_slot and damaged_parts on all units
for (var u = 0; u < array_length(units); u++) {
    if (!variable_struct_exists(units[u], "formation_slot")) {
        units[u].formation_slot = u % 6;
    }
    if (!variable_struct_exists(units[u], "damaged_parts")) {
        units[u].damaged_parts = { head: false, torso: false, arm_left: false, arm_right: false, legs: false, backpack: false };
    }
}

get_stack_at_tile = function(_c, _r, _team = undefined) {
    var _stack = [];
    for (var u = 0; u < array_length(units); u++) {
        var _chk = units[u];
        if (!_chk.is_destroyed && _chk.grid_c == _c && _chk.grid_r == _r) {
            if (is_undefined(_team) || _chk.team == _team) {
                array_push(_stack, _chk);
            }
        }
    }
    // Sort stack: Vanguard (0..2) first, Support (3..5) second
    for (var i = 1; i < array_length(_stack); i++) {
        var _key = _stack[i];
        var j = i - 1;
        while (j >= 0 && _stack[j].formation_slot > _key.formation_slot) {
            _stack[j + 1] = _stack[j];
            j--;
        }
        _stack[j + 1] = _key;
    }
    return _stack;
};

reorganize_stack = function(_c, _r, _team) {
    var _stack = get_stack_at_tile(_c, _r, _team);
    if (array_length(_stack) <= 1) {
        add_log("[FORMATION] Need at least 2 units in stack to reorganize rows.");
        scr_audio_play_ui("cancel");
        return;
    }
    for (var s = 0; s < array_length(_stack); s++) {
        var _u = _stack[s];
        if (_u.formation_slot < 3) {
            _u.formation_slot += 3;
        } else {
            _u.formation_slot -= 3;
        }
    }
    scr_audio_play_ui("confirm");
    add_log("[FORMATION REORG] Battlegroup at (" + string(_c) + ", " + string(_r) + ") swapped Vanguard & Support rows!");
};

get_stack_max_firepower = function(_atk_stack, _def_target, _dist) {
    var _firing_plan = [];
    var _total_min_dmg = 0;
    var _total_max_dmg = 0;

    for (var u = 0; u < array_length(_atk_stack); u++) {
        var _au = _atk_stack[u];
        if (_au.current_ap <= 0 || _au.is_destroyed) continue;

        var _has_manual = (variable_struct_exists(_au, "manual_weapon_idx") && _au.manual_weapon_idx >= 0 && _au.manual_weapon_idx < array_length(_au.weapons));
        var _best_w = undefined;
        var _best_dmg = -1;

        if (_has_manual) {
            var _mw = _au.weapons[_au.manual_weapon_idx];
            var _eff_max_range = _mw.range_max + max(0, _au.elev - _def_target.elev);
            if (_dist >= _mw.range_min && _dist <= _eff_max_range && _au.current_ap >= _mw.ap_cost) {
                _best_w = _mw;
            }
        }

        if (is_undefined(_best_w)) {
            for (var w = 0; w < array_length(_au.weapons); w++) {
                var _cand_w = _au.weapons[w];
                var _eff_max_range = _cand_w.range_max + max(0, _au.elev - _def_target.elev);
                if (_dist >= _cand_w.range_min && _dist <= _eff_max_range && _au.current_ap >= _cand_w.ap_cost) {
                    var _is_tgt_air = (variable_struct_exists(_def_target, "is_aircraft") && _def_target.is_aircraft) || (variable_struct_get(_def_target, "move_type") == "aero");
                    var _is_atk_air = (variable_struct_exists(_au, "is_aircraft") && _au.is_aircraft) || (variable_struct_get(_au, "move_type") == "aero");
                    if (_cand_w.proj_type == "MELEE" && _is_tgt_air && !_is_atk_air) continue;

                    if (_cand_w.damage > _best_dmg) {
                        _best_dmg = _cand_w.damage;
                        _best_w = _cand_w;
                    }
                }
            }
        }

        if (!is_undefined(_best_w)) {
            array_push(_firing_plan, { unit: _au, weapon: _best_w });
            var _est_lo = max(10, floor(_best_w.damage * 0.85) - 30);
            var _est_hi = max(15, floor(_best_w.damage * 1.15) - 20);
            _total_min_dmg += _est_lo;
            _total_max_dmg += _est_hi;
        }
    }

    return {
        plan: _firing_plan,
        min_dmg: _total_min_dmg,
        max_dmg: _total_max_dmg,
        unit_count: array_length(_firing_plan)
    };
};

execute_stack_volley = function(_atk_stack, _def_target, _dist) {
    var _fp = get_stack_max_firepower(_atk_stack, _def_target, _dist);
    if (_fp.unit_count == 0) {
        add_log("[NO WEAPONS IN RANGE] No units in battlegroup can engage target at " + string(_dist) + " tiles!");
        scr_audio_play_ui("cancel");
        return false;
    }

    var _lead_plan = _fp.plan[0];
    var _lead_u = _lead_plan.unit;
    var _lead_w = _lead_plan.weapon;

    for (var p = 0; p < array_length(_fp.plan); p++) {
        var _item = _fp.plan[p];
        _item.unit.current_ap -= _item.weapon.ap_cost;
        _item.unit.current_heat += _item.weapon.heat_cost;
        _item.unit.facing = iso_get_facing(_item.unit.grid_c, _item.unit.grid_r, _def_target.grid_c, _def_target.grid_r);
        _item.unit.anim_state = _item.weapon.anim_state;
        _item.unit.anim_timer = 28;
    }

    add_log("[BATTLEGROUP SALVO] " + string(_fp.unit_count) + " unit(s) unleashed Automated Maximum Firepower against " + _def_target.callsign + "!");

    var _def_stk = get_stack_at_tile(_def_target.grid_c, _def_target.grid_r, _def_target.team);
    start_battle_cinematic(_lead_u, _def_target, _lead_w, COMBAT_STATE.ATTACK_EXECUTION, _atk_stack, _def_stk);
    state = COMBAT_STATE.ATTACK_EXECUTION;
    return true;
};

// =========================================================================
// GOAL FINAL: MODULAR COMBAT CLASH & DYNAMIC MECHA ANIMATION ENGINE
// =========================================================================
cinematic_combat_enabled = true;

battle_cinematic = {
    active: false,
    phase: 0,
    timer: 0,
    is_condensed: false,
    theater: "EARTH_SURFACE",
    terrain: 0,
    return_state: COMBAT_STATE.PLAYER_PHASE,
    attacker: undefined,
    defender: undefined,
    attacker_stack: [],
    defender_stack: [],
    weapon: undefined,
    weapon_class: "BALLISTIC",
    raw_damage: 0,
    mitigated_dmg: 0,
    hit_chance: 0,
    is_hit: false,
    is_crushing: false,
    hit_part: "torso",
    flank_tag: "",
    elev_tag: "",
    is_space: false,
    is_water: false,
    is_slag: false,
    is_air_atk: false,
    is_air_def: false,
    has_counter: false,
    counter_weapon: undefined,
    counter_hit_chance: 0,
    counter_is_hit: false,
    counter_hit_part: "torso",
    counter_damage: 0,
    applied_primary: false,
    applied_counter: false,
    atk_portrait: spr_portrait_commander_male,
    def_portrait: spr_portrait_vance,
    atk_expr: "NEUTRAL",
    def_expr: "DEFENDING",
    atk_radio_bark: "Engaging target.",
    def_radio_bark: "Incoming fire!",
    limb_flash_timer: 0,
    limb_flash_part: "",
    melee_cleave_timer: 0,
    shutter_y: 0,
    screen_shake: 0,
    flash_alpha: 0,
    atk_dash_x: 0,
    atk_recoil_x: 0,
    atk_recoil_y: 0,
    def_recoil_x: 0,
    def_recoil_y: 0,
    atk_wing1_recoil_x: 0,
    atk_wing1_recoil_y: 0,
    atk_wing2_recoil_x: 0,
    atk_wing2_recoil_y: 0,
    def_wing1_recoil_x: 0,
    def_wing1_recoil_y: 0,
    def_wing2_recoil_x: 0,
    def_wing2_recoil_y: 0,
    atk_anim_state: "idle",
    def_anim_state: "idle",
    projectiles: [],
    casings: [],
    particles: [],
    popups: []
};

start_battle_cinematic = function(_atk, _def, _wpn, _return_state = COMBAT_STATE.PLAYER_PHASE, _atk_stack_override = undefined, _def_stack_override = undefined) {
    if (!cinematic_combat_enabled) {
        legacy_spawn_combat_projectile(_atk, _def, _wpn);
        return;
    }

    var _dist = calculate_distance(_atk.grid_c, _atk.grid_r, _def.grid_c, _def.grid_r);
    var _hit_chance = calculate_hit_chance(_atk, _def, _dist, _wpn);
    if (variable_struct_exists(_atk, "is_aimed_shot") && _atk.is_aimed_shot) _hit_chance = max(10, _hit_chance - 15);

    var _roll = irandom_range(1, 100);
    var _is_hit = (_roll <= _hit_chance);

    // Hit Part Selection (Front Mission 5-Part Mechanics)
    var _hit_part = "torso";
    if (variable_struct_exists(_atk, "is_aimed_shot") && _atk.is_aimed_shot && _atk.targeted_limb != "") {
        _hit_part = _atk.targeted_limb;
    } else {
        var _part_roll = irandom_range(1, 100);
        if (_part_roll <= 40) _hit_part = "torso";
        else if (_part_roll <= 55) _hit_part = "arm_left";
        else if (_part_roll <= 70) _hit_part = "arm_right";
        else if (_part_roll <= 90) _hit_part = "legs";
        else _hit_part = "head";
    }

    // Platoon Volley Scaling: 100% at 3/3, 75% at 2/3, 50% at 1/3
    var _squad_mult = 1.0;
    if (_atk.squad_type == "PLATOON_3") {
        _squad_mult = (_atk.squad_members_count == 3) ? 1.0 : ((_atk.squad_members_count == 2) ? 0.75 : 0.50);
    }
    var _raw_dmg = floor((_wpn.damage + irandom_range(-15, 20)) * _squad_mult);

    // Directional Facing Damage Multipliers (Goal F: Flanking & Rear Ambush)
    var _inc_dir = iso_get_facing(_def.grid_c, _def.grid_r, _atk.grid_c, _atk.grid_r);
    var _is_rear = (_inc_dir == (_def.facing + 2) % 4);
    var _is_flank = (_inc_dir == (_def.facing + 1) % 4 || _inc_dir == (_def.facing + 3) % 4);
    var _flank_tag = "";
    if (_is_rear) {
        _raw_dmg = floor(_raw_dmg * 1.40);
        _flank_tag = "[REAR CORE HIT +40%]";
        if (irandom(100) < 65) _hit_part = "torso"; else _hit_part = "backpack";
    } else if (_is_flank) {
        _raw_dmg = floor(_raw_dmg * 1.20);
        _flank_tag = "[FLANK SHOT +20%]";
        if (irandom(100) < 50) _hit_part = (_inc_dir == (_def.facing + 1) % 4) ? "arm_right" : "arm_left";
    }

    // High Ground Elevation Damage Bonus (+15% per tier above defender)
    var _elev_diff = _atk.elev - _def.elev;
    var _elev_tag = "";
    if (_elev_diff > 0) {
        _raw_dmg = floor(_raw_dmg * (1.0 + (_elev_diff * 0.15)));
        _elev_tag = "[HIGH GROUND +" + string(_elev_diff * 15) + "%]";
    }

    // Mitigation Calculation with Brace Stance & Vanguard Screening (Refined Combat System)
    var _limb = variable_struct_get(_def.components, _hit_part);
    var _is_braced = variable_struct_exists(_def, "braced") && _def.braced;
    var _mitigated_dmg = max(15, _raw_dmg - _limb.armor);
    if (_is_braced) {
        _mitigated_dmg = max(10, floor(_mitigated_dmg * 0.60));
    }

    // Vanguard Screening & Interception:
    // Direct fire (non-artillery/missiles) aimed at rear support line is intercepted by frontline Vanguard!
    var _is_artillery_or_missile = (_wpn.range_max >= 4 || _wpn.proj_type == "MICRO_MISSILE" || _wpn.proj_type == "MISSILE");
    var _def_stk_check = !is_undefined(_def_stack_override) ? _def_stack_override : get_stack_at_tile(_def.grid_c, _def.grid_r, _def.team);
    if (!_is_artillery_or_missile && variable_struct_exists(_def, "formation_slot") && _def.formation_slot >= 3) {
        for (var vi = 0; vi < array_length(_def_stk_check); vi++) {
            var _vu = _def_stk_check[vi];
            if (!_vu.is_destroyed && variable_struct_exists(_vu, "formation_slot") && _vu.formation_slot < 3) {
                _def = _vu;
                _limb = variable_struct_get(_def.components, _hit_part);
                _mitigated_dmg = max(15, _raw_dmg - _limb.armor);
                if (variable_struct_exists(_def, "braced") && _def.braced) {
                    _mitigated_dmg = max(10, floor(_mitigated_dmg * 0.60));
                }
                add_log("[VANGUARD SCREEN] " + _vu.callsign + " intercepted incoming fire aimed at rear support line!");
                break;
            }
        }
    }

    // Cover Mitigation
    var _def_cover = grid_cover[_def.grid_c][_def.grid_r];
    if (_def_cover == 2) _mitigated_dmg = floor(_mitigated_dmg * 0.70);
    else if (_def_cover == 1) _mitigated_dmg = floor(_mitigated_dmg * 0.85);

    // Critical Hit Roll (5% base + 15% if flank/rear)
    var _crit_chance = 5 + (_is_rear ? 20 : (_is_flank ? 10 : 0));
    if (variable_struct_exists(_atk, "crit_chance")) _crit_chance += _atk.crit_chance;
    if (variable_struct_exists(_atk, "mutated_traits") && is_array(_atk.mutated_traits)) {
        if (array_contains(_atk.mutated_traits, "Ace Predator")) {
            _crit_chance += 12;
        }
    }
    var _is_crushing = (irandom(100) < _crit_chance);
    if (_is_crushing) {
        if (variable_struct_exists(_atk, "mutated_traits") && is_array(_atk.mutated_traits) && array_contains(_atk.mutated_traits, "Ace Predator")) {
            _mitigated_dmg = floor(_mitigated_dmg * 1.62);
        } else {
            _mitigated_dmg = floor(_mitigated_dmg * 1.5);
        }
    }

    // Counter-Attack Readiness Evaluation (Braced units forfeit counter)
    var _has_counter = false;
    var _counter_w = undefined;
    var _counter_hit_chance = 0;
    var _counter_is_hit = false;
    var _counter_hit_part = "torso";
    var _counter_dmg = 0;

    var _survives = (!_is_hit || (_hit_part != "torso" && _limb.cur > _mitigated_dmg) || (_hit_part == "torso" && _limb.cur > _mitigated_dmg));
    if (_survives && !_is_braced && array_length(_def.weapons) > 0 && _def.current_ap >= 2) {
        for (var w = 0; w < array_length(_def.weapons); w++) {
            var _cw = _def.weapons[w];
            if (_cw.range_min <= _dist && _cw.range_max >= _dist && _def.current_ap >= _cw.ap_cost) {
                _has_counter = true;
                _counter_w = _cw;
                break;
            }
        }
        if (_has_counter && !is_undefined(_counter_w)) {
            _counter_hit_chance = calculate_hit_chance(_def, _atk, _dist, _counter_w);
            _counter_is_hit = (irandom_range(1, 100) <= _counter_hit_chance);
            var _cpart_roll = irandom_range(1, 100);
            if (_cpart_roll <= 45) _counter_hit_part = "torso";
            else if (_cpart_roll <= 65) _counter_hit_part = "arm_right";
            else if (_cpart_roll <= 85) _counter_hit_part = "legs";
            else _counter_hit_part = "head";

            var _catk_armor = variable_struct_get(_atk.components, _counter_hit_part).armor;
            _counter_dmg = max(1, _counter_w.damage - floor(_catk_armor * 0.5));
        }
    }

    // Environmental Theater and Terrain Resolution
    var _terr = grid_terrain[_def.grid_c][_def.grid_r];
    var _cur_map = map_definitions[current_map_id];
    var _theater = variable_struct_get(_cur_map, "theater") ?? "EARTH_SURFACE";
    var _is_space = (_theater == "SPACE" || _terr == 4);
    var _is_water = (_terr == 3);
    var _is_slag = (_terr == 5);
    var _is_air_atk = (variable_struct_exists(_atk, "is_aircraft") && _atk.is_aircraft) || (variable_struct_get(_atk, "move_type") == "aero");
    var _is_air_def = (variable_struct_exists(_def, "is_aircraft") && _def.is_aircraft) || (variable_struct_get(_def, "move_type") == "aero");

    // Resolve Weapon Class and Pilot Profiles (Goal Final Modular Combat Engine)
    var _wpn_type = variable_struct_exists(_wpn, "proj_type") ? _wpn.proj_type : "KINETIC_CANNON";
    var _wpn_class = "BALLISTIC";
    if (string_pos("BEAM", _wpn_type) > 0 || string_pos("PLASMA", _wpn_type) > 0 || string_pos("TACHYON", _wpn_type) > 0 || string_pos("LASER", _wpn_type) > 0) {
        _wpn_class = "ENERGY";
    } else if (string_pos("MISSILE", _wpn_type) > 0 || string_pos("ROCKET", _wpn_type) > 0 || string_pos("HOWITZER", _wpn_type) > 0) {
        _wpn_class = "ORDNANCE";
    } else if (string_pos("BLADE", _wpn_type) > 0 || string_pos("MELEE", _wpn_type) > 0 || string_pos("SABER", _wpn_type) > 0 || string_pos("CLAW", _wpn_type) > 0 || string_pos("PILE", _wpn_type) > 0) {
        _wpn_class = "MELEE";
    }

    var _resolve_pilot_portrait = function(_pname) {
        if (string_pos("Cole", _pname) > 0) return spr_portrait_cole;
        if (string_pos("Nadia", _pname) > 0) return spr_portrait_nadia;
        if (string_pos("Vance", _pname) > 0) return spr_portrait_vance;
        if (string_pos("Cruz", _pname) > 0) return spr_portrait_cruz;
        if (string_pos("Cassian", _pname) > 0) return spr_portrait_cassian;
        if (string_pos("Renzo", _pname) > 0) return spr_portrait_renzo;
        if (string_pos("Sorren", _pname) > 0) return spr_portrait_sorren;
        if (string_pos("Null-07", _pname) > 0 || string_pos("NULL", _pname) > 0) return spr_portrait_null07;
        return spr_portrait_commander_male;
    };

    if (!variable_struct_exists(_atk, "damaged_parts")) _atk.damaged_parts = { head: false, torso: false, arm_left: false, arm_right: false, legs: false, backpack: false };
    if (!variable_struct_exists(_def, "damaged_parts")) _def.damaged_parts = { head: false, torso: false, arm_left: false, arm_right: false, legs: false, backpack: false };

    // Dynamic Cinematic Pacing: Ace & Incursions get full cutscene; grunts run fast condensed clash
    var _is_ace_clash = (_atk.squad_type == "SUPER_ACE" || _def.squad_type == "SUPER_ACE" || state == COMBAT_STATE.NEMESIS_INCURSION);

    // Populate Cinematic State
    battle_cinematic.active = true;
    battle_cinematic.phase = 0;
    battle_cinematic.timer = 0;
    battle_cinematic.return_state = _return_state;
    battle_cinematic.attacker = _atk;
    battle_cinematic.defender = _def;
    battle_cinematic.attacker_stack = !is_undefined(_atk_stack_override) ? _atk_stack_override : get_stack_at_tile(_atk.grid_c, _atk.grid_r, _atk.team);
    battle_cinematic.defender_stack = !is_undefined(_def_stack_override) ? _def_stack_override : get_stack_at_tile(_def.grid_c, _def.grid_r, _def.team);
    battle_cinematic.weapon = _wpn;
    battle_cinematic.weapon_class = _wpn_class;
    battle_cinematic.atk_dash_x = 0.0;
    battle_cinematic.melee_cleave_timer = 0;
    battle_cinematic.counter_weapon = _counter_w;
    battle_cinematic.flank_tag = _flank_tag;
    battle_cinematic.elev_tag = _elev_tag;
    battle_cinematic.has_counter = _has_counter;

    battle_cinematic.atk_portrait = _resolve_pilot_portrait(_atk.pilot_name);
    battle_cinematic.def_portrait = _resolve_pilot_portrait(_def.pilot_name);
    battle_cinematic.atk_expr = "NEUTRAL";
    battle_cinematic.def_expr = "DEFENDING";
    battle_cinematic.atk_radio_bark = "Target acquired. Engaging with " + string_upper(_wpn.name) + "!";
    battle_cinematic.def_radio_bark = "Hostile vector detected! Reinforcing kinetic louvers!";

    battle_cinematic.atk_anim_state = "idle";
    battle_cinematic.def_anim_state = "idle";
    battle_cinematic.atk_recoil_x = 0;
    battle_cinematic.atk_recoil_y = 0;
    battle_cinematic.def_recoil_x = 0;
    battle_cinematic.def_recoil_y = 0;

    battle_cinematic.atk_wing1_recoil_x = 0; battle_cinematic.atk_wing1_recoil_y = 0;
    battle_cinematic.atk_wing2_recoil_x = 0; battle_cinematic.atk_wing2_recoil_y = 0;
    battle_cinematic.def_wing1_recoil_x = 0; battle_cinematic.def_wing1_recoil_y = 0;
    battle_cinematic.def_wing2_recoil_x = 0; battle_cinematic.def_wing2_recoil_y = 0;

    battle_cinematic.hit_chance = _hit_chance;
    battle_cinematic.is_hit = _is_hit;
    battle_cinematic.hit_part = _hit_part;
    battle_cinematic.raw_damage = _raw_dmg;
    battle_cinematic.mitigated_dmg = _mitigated_dmg;
    battle_cinematic.is_crushing = _is_crushing;
    battle_cinematic.is_suppression = false;
    battle_cinematic.applied_primary = false;
    battle_cinematic.limb_flash_part = "";
    battle_cinematic.limb_flash_timer = 0;

    battle_cinematic.counter_hit_chance = _counter_hit_chance;
    battle_cinematic.counter_is_hit = _counter_is_hit;
    battle_cinematic.counter_hit_part = _counter_hit_part;
    battle_cinematic.counter_damage = _counter_dmg;
    battle_cinematic.applied_counter = false;

    battle_cinematic.shutter_y = 0.0;
    battle_cinematic.screen_shake = 0.0;
    battle_cinematic.flash_alpha = 0.0;
    battle_cinematic.is_condensed = !_is_ace_clash;
    battle_cinematic.theater = _theater;
    battle_cinematic.terrain = _terr;
    battle_cinematic.is_space = _is_space;
    battle_cinematic.is_water = _is_water;
    battle_cinematic.is_slag = _is_slag;
    battle_cinematic.is_air_atk = _is_air_atk;
    battle_cinematic.is_air_def = _is_air_def;

    battle_cinematic.projectiles = [];
    battle_cinematic.particles = [];
    battle_cinematic.casings = [];
    battle_cinematic.popups = [];

    scr_audio_play_ui("confirm");
};

// 2. Update Battle Cinematic State & Choreography
update_battle_cinematic = function() {
    if (!battle_cinematic.active) return;

    // Fast-Forward / Skip Input Check (Space, Enter, or Click)
    if (keyboard_check_pressed(vk_space) || keyboard_check_pressed(vk_enter) || mouse_check_button_pressed(mb_left)) {
        skip_battle_cinematic();
        return;
    }

    battle_cinematic.timer += (variable_struct_exists(battle_cinematic, "is_condensed") && battle_cinematic.is_condensed) ? 2 : 1;
    var _t = battle_cinematic.timer;

    // Screen Shake & Flash Decay
    if (battle_cinematic.screen_shake > 0) battle_cinematic.screen_shake = max(0, battle_cinematic.screen_shake - 0.7);
    if (battle_cinematic.flash_alpha > 0) battle_cinematic.flash_alpha = max(0, battle_cinematic.flash_alpha - 0.06);
    if (battle_cinematic.limb_flash_timer > 0) battle_cinematic.limb_flash_timer--;
    if (battle_cinematic.melee_cleave_timer > 0) battle_cinematic.melee_cleave_timer--;

    // Update Casings Physics
    for (var i = array_length(battle_cinematic.casings) - 1; i >= 0; i--) {
        var _c = battle_cinematic.casings[i];
        _c.x += _c.vx;
        _c.y += _c.vy;
        _c.vy += 0.45;
        _c.angle += _c.spin;
        if (_c.y >= 520) {
            _c.y = 520;
            _c.vy = -_c.vy * 0.45;
            _c.vx *= 0.7;
            if (abs(_c.vy) < 1.0) _c.vy = 0;
        }
        _c.life--;
        if (_c.life <= 0) array_delete(battle_cinematic.casings, i, 1);
    }

    // Update Particles
    for (var i = array_length(battle_cinematic.particles) - 1; i >= 0; i--) {
        var _p = battle_cinematic.particles[i];
        if (variable_struct_exists(_p, "vx")) {
            _p.x += _p.vx;
            _p.y += _p.vy;
            _p.vy += 0.35;
        }
        _p.frame += _p.speed;
        if (sprite_exists(_p.sprite) && _p.frame >= sprite_get_number(_p.sprite)) {
            array_delete(battle_cinematic.particles, i, 1);
        }
    }

    // Update Popups
    for (var i = array_length(battle_cinematic.popups) - 1; i >= 0; i--) {
        var _pop = battle_cinematic.popups[i];
        _pop.y -= 0.6;
        _pop.timer--;
        if (_pop.timer <= 15) _pop.alpha = max(0, _pop.timer / 15.0);
        if (_pop.timer <= 0) array_delete(battle_cinematic.popups, i, 1);
    }

    // Recoil Smooth Dampening
    battle_cinematic.atk_recoil_x *= 0.88;
    battle_cinematic.atk_recoil_y *= 0.88;
    battle_cinematic.def_recoil_x *= 0.88;
    battle_cinematic.def_recoil_y *= 0.88;
    battle_cinematic.atk_wing1_recoil_x *= 0.88;
    battle_cinematic.atk_wing2_recoil_x *= 0.88;
    battle_cinematic.def_wing1_recoil_x *= 0.88;
    battle_cinematic.def_wing2_recoil_x *= 0.88;

    // --- PHASE 0: Letterbox In & Threat Acquisition (Frames 0 to 20) ---
    if (_t <= 20) {
        battle_cinematic.phase = 0;
        battle_cinematic.shutter_y = min(115.0, (_t / 20.0) * 115.0);
        return;
    }

    // --- PHASE 1: Attacker Salvo Initiation (Frames 21 to 65) ---
    if (_t > 20 && _t <= 65) {
        battle_cinematic.phase = 1;
        battle_cinematic.shutter_y = 115.0;

        // Frame 21: Lead Unit Fires
        if (_t == 21) {
            battle_cinematic.atk_anim_state = "fire";
            battle_cinematic.atk_expr = "ATTACKING";
            battle_cinematic.atk_recoil_x = -16;
            scr_audio_play_weapon(battle_cinematic.weapon.short_name);

            if (battle_cinematic.weapon_class == "MELEE") {
                battle_cinematic.atk_radio_bark = "Engaging vernier overdrive! Executing kinetic strike!";
            } else if (battle_cinematic.weapon_class == "ENERGY") {
                battle_cinematic.atk_radio_bark = "Particle beam emitter locked! Discharging main array!";
            } else if (battle_cinematic.weapon_class == "ORDNANCE") {
                battle_cinematic.atk_radio_bark = "Shoulder pod doors open! Salvo away!";
            } else {
                battle_cinematic.atk_radio_bark = "Full rotary battery hot! Suppressing target position!";
            }

            // Eject Spent Shell Casing for Ballistics
            if (battle_cinematic.weapon_class == "BALLISTIC") {
                array_push(battle_cinematic.casings, {
                    x: 340, y: 470, vx: random_range(-5.5, -3.0), vy: random_range(-5.0, -2.5),
                    angle: irandom(360), spin: random_range(-18, 18), life: 75
                });
            }

            // Spawn Projectile / Energy Beam / Missile Salvo
            if (battle_cinematic.weapon_class != "MELEE") {
                array_push(battle_cinematic.projectiles, {
                    type: battle_cinematic.weapon.proj_type,
                    x1: 375, y1: 460, x2: 1010, y2: 465,
                    cur_x: 375, cur_y: 460, t: 0.0, speed: (battle_cinematic.weapon_class == "ENERGY" ? 0.065 : 0.038),
                    trail: battle_cinematic.weapon.proj_type
                });
            }
        }

        // Melee High-Speed Dash Thrust
        if (battle_cinematic.weapon_class == "MELEE") {
            if (_t >= 21 && _t <= 38) {
                battle_cinematic.atk_dash_x = lerp(battle_cinematic.atk_dash_x, 620.0, 0.22);
            } else if (_t == 39) {
                battle_cinematic.melee_cleave_timer = 24;
                battle_cinematic.screen_shake = 22.0;
                battle_cinematic.flash_alpha = 0.50;
                scr_audio_play_impact("kinetic", true);
                array_push(battle_cinematic.particles, {
                    sprite: spr_fx_spark, x: 1026, y: 440, frame: 0.0, speed: 0.40, scale: 2.0, alpha: 1.0
                });
            } else if (_t > 45 && _t <= 65) {
                battle_cinematic.atk_dash_x = lerp(battle_cinematic.atk_dash_x, 0.0, 0.16);
            }
        }

        // Frame 26: Wingman 1 Synchronized Salvo (if present in Platoon)
        if (_t == 26 && battle_cinematic.attacker.squad_type == "PLATOON_3" && battle_cinematic.attacker.squad_members_count >= 2) {
            battle_cinematic.atk_wing1_recoil_x = -12;
            scr_audio_play_weapon(battle_cinematic.weapon.short_name);
            if (battle_cinematic.weapon_class == "BALLISTIC") {
                array_push(battle_cinematic.casings, {
                    x: 210, y: 420, vx: random_range(-5.5, -3.0), vy: random_range(-5.0, -2.5),
                    angle: irandom(360), spin: random_range(-18, 18), life: 75
                });
            }
            array_push(battle_cinematic.projectiles, {
                type: battle_cinematic.weapon.proj_type,
                x1: 245, y1: 410, x2: 990, y2: 450,
                cur_x: 245, cur_y: 410, t: 0.0, speed: 0.038,
                trail: battle_cinematic.weapon.proj_type
            });
        }

        // Frame 31: Wingman 2 Synchronized Salvo
        if (_t == 31 && battle_cinematic.attacker.squad_type == "PLATOON_3" && battle_cinematic.attacker.squad_members_count >= 3) {
            battle_cinematic.atk_wing2_recoil_x = -12;
            scr_audio_play_weapon(battle_cinematic.weapon.short_name);
            if (battle_cinematic.weapon_class == "BALLISTIC") {
                array_push(battle_cinematic.casings, {
                    x: 170, y: 510, vx: random_range(-5.5, -3.0), vy: random_range(-5.0, -2.5),
                    angle: irandom(360), spin: random_range(-18, 18), life: 75
                });
            }
            array_push(battle_cinematic.projectiles, {
                type: battle_cinematic.weapon.proj_type,
                x1: 205, y1: 505, x2: 1025, y2: 480,
                cur_x: 205, cur_y: 505, t: 0.0, speed: 0.038,
                trail: battle_cinematic.weapon.proj_type
            });
        }

        // Staggered Firing for 6-Unit Battlegroup Stack
        if (variable_struct_exists(battle_cinematic, "attacker_stack") && array_length(battle_cinematic.attacker_stack) > 1) {
            var _stk_atk = battle_cinematic.attacker_stack;
            var _fire_frames = [21, 25, 29, 33, 37, 41];
            for (var sf = 1; sf < min(6, array_length(_stk_atk)); sf++) {
                if (_t == _fire_frames[sf] && !_stk_atk[sf].is_destroyed) {
                    scr_audio_play_weapon(battle_cinematic.weapon.short_name);
                    var _fx_slot = variable_struct_exists(_stk_atk[sf], "formation_slot") ? _stk_atk[sf].formation_slot : sf;
                    var _src_x = (_fx_slot < 3) ? 310 : 160;
                    var _src_y = 470 + ((_fx_slot % 3 == 1) ? -40 : ((_fx_slot % 3 == 2) ? 40 : 0));
                    if (battle_cinematic.weapon_class == "BALLISTIC") {
                        array_push(battle_cinematic.casings, {
                            x: _src_x, y: _src_y, vx: random_range(-5.5, -3.0), vy: random_range(-5.0, -2.5),
                            angle: irandom(360), spin: random_range(-18, 18), life: 75
                        });
                    }
                    array_push(battle_cinematic.projectiles, {
                        type: battle_cinematic.weapon.proj_type,
                        x1: _src_x + 30, y1: _src_y, x2: 1010 + irandom_range(-25, 25), y2: 465 + irandom_range(-25, 25),
                        cur_x: _src_x + 30, cur_y: _src_y, t: 0.0, speed: 0.038,
                        trail: battle_cinematic.weapon.proj_type
                    });
                }
            }
        }

        // Rapid Vulcan Multi-Bullet Stream
        if (battle_cinematic.weapon.proj_type == "ROTARY_VULCAN" && (_t == 25 || _t == 29 || _t == 34 || _t == 39)) {
            battle_cinematic.atk_recoil_x = -8;
            scr_audio_play_weapon(battle_cinematic.weapon.short_name);
            array_push(battle_cinematic.projectiles, {
                type: "ROTARY_VULCAN",
                x1: 375, y1: 455 + irandom_range(-6, 6), x2: 1010, y2: 460 + irandom_range(-15, 15),
                cur_x: 375, cur_y: 455, t: 0.0, speed: 0.065, trail: "tracer"
            });
        }

        // Recover to idle
        if (_t == 50) battle_cinematic.atk_anim_state = "idle";
    }

    // --- Update In-Flight Projectiles ---
    for (var i = array_length(battle_cinematic.projectiles) - 1; i >= 0; i--) {
        var _pj = battle_cinematic.projectiles[i];
        _pj.t += _pj.speed;
        _pj.cur_x = lerp(_pj.x1, _pj.x2, _pj.t);
        
        if (_pj.type == "KINETIC_CANNON" || _pj.type == "MICRO_MISSILE") {
            _pj.cur_y = lerp(_pj.y1, _pj.y2, _pj.t) - sin(_pj.t * pi) * 28.0;
        } else {
            _pj.cur_y = lerp(_pj.y1, _pj.y2, _pj.t);
        }

        if (_pj.t >= 1.0) {
            array_delete(battle_cinematic.projectiles, i, 1);
        }
    }

    // --- PHASE 2: Projectile Transit & Defender Reaction (Frames 65 to 85) ---
    if (_t > 65 && _t <= 85) {
        battle_cinematic.phase = 2;

        // Evasive Thruster Dodge if Miss
        if (!battle_cinematic.is_hit && _t == 72) {
            battle_cinematic.def_recoil_x = 26;
            battle_cinematic.def_expr = "EVADED";
            battle_cinematic.def_radio_bark = "Vernier burn successful! Impact vector cleared!";
            scr_audio_play_sfx(snd_mech_boost, 1.0, 0.05);
            array_push(battle_cinematic.popups, {
                text: "EVADED // THRUSTER BURST",
                x: 1026, y: 430, color: make_color_rgb(80, 240, 255),
                scale: 1.1, alpha: 1.0, timer: 50
            });
        }
    }

    // --- PHASE 3: Impact & Front Mission Modular Damage Resolution (Frames 85 to 145) ---
    if (_t > 85 && _t <= 145) {
        battle_cinematic.phase = 3;

        if (_t == 86 && !battle_cinematic.applied_primary) {
            battle_cinematic.applied_primary = true;
            var _def = battle_cinematic.defender;
            var _atk = battle_cinematic.attacker;
            var _part = battle_cinematic.hit_part;
            var _dmg = battle_cinematic.mitigated_dmg;

            if (battle_cinematic.is_hit) {
                battle_cinematic.screen_shake = 16.0;
                battle_cinematic.flash_alpha = 0.45;
                battle_cinematic.def_anim_state = "hit";
                battle_cinematic.def_expr = "TAKING_HIT";
                battle_cinematic.def_recoil_x = 22;
                battle_cinematic.limb_flash_part = _part;
                battle_cinematic.limb_flash_timer = 24;

                scr_audio_play_impact("kinetic", (battle_cinematic.weapon.damage > 50));

                // Goal G: Boss Regenerative Phase Barrier Absorption
                if (variable_struct_exists(_def, "barrier_cur") && _def.barrier_cur > 0) {
                    var _absorbed = min(_def.barrier_cur, _dmg);
                    _def.barrier_cur -= _absorbed;
                    _dmg -= _absorbed;
                    battle_cinematic.mitigated_dmg = _dmg;
                    array_push(battle_cinematic.popups, {
                        text: "[PHASE BARRIER -" + string(_absorbed) + "]",
                        x: 1026, y: 405, color: make_color_rgb(80, 220, 255),
                        scale: 1.15, alpha: 1.0, timer: 60
                    });
                    add_log("[BARRIER ABSORB] Ouroboros Prime Phase Barrier absorbed " + string(_absorbed) + " damage! (" + string(_def.barrier_cur) + " remaining)");
                }

                // Deduct modular limb damage
                var _limb = variable_struct_get(_def.components, _part);
                _limb.cur = max(0, _limb.cur - _dmg);

                // Goal Final: Limb Detachment & Persistent Battle Scars
                if (_limb.cur <= 0 && _limb.intact) {
                    _limb.intact = false;
                    variable_struct_set(_def.damaged_parts, _part, true);
                    battle_cinematic.def_expr = "CRIPPLED";
                    battle_cinematic.def_radio_bark = "Warning! " + string_upper(_limb.name) + " destroyed!";
                    
                    // Spawn flying severed limb debris
                    array_push(battle_cinematic.particles, {
                        sprite: (_part == "arm_right" ? spr_ms_ironclad_hit_right_arm_off : spr_ms_ironclad_hit_left_arm_off),
                        x: 1026, y: 440, vx: random_range(5.0, 8.0), vy: random_range(-8.0, -4.0),
                        frame: 0.0, speed: 0.0, scale: 1.15, alpha: 1.0
                    });

                    // Burst of socket sparks
                    for (var sk = 0; sk < 3; sk++) {
                        array_push(battle_cinematic.particles, {
                            sprite: spr_fx_spark, x: 1026 + irandom_range(-15, 15), y: 450 + irandom_range(-20, 20),
                            frame: 0.0, speed: 0.35, scale: 1.6, alpha: 1.0
                        });
                    }

                    array_push(battle_cinematic.popups, {
                        text: "[CRITICAL // " + string_upper(_part) + " SEVERED!]",
                        x: 1026, y: 380, color: make_color_rgb(255, 60, 60),
                        scale: 1.25, alpha: 1.0, timer: 70
                    });

                    // Catastrophic Kill Check
                    if (_part == "torso") {
                        _def.is_destroyed = true;
                        _def.anim_state = "destroyed";
                        _def.anim_timer = 40;
                        add_log("[CATASTROPHIC KILL] " + _def.callsign + " REACTOR BREACH! Unit neutralized.");

                        // 1. Tactical Battlefield Wreckage Cover (+20% cover on tile)
                        grid_cover[_def.grid_c][_def.grid_r] = 2;
                        add_log("[FIELD WRECKAGE] Smoldering chassis created tactical cover on tile (" + string(_def.grid_c) + ", " + string(_def.grid_r) + ")");

                        // 2. Pilot Ejection Survival Roll & Battlefield POW Capture (Doc 51)
                        var _ej_roll = irandom_range(1, 100);
                        if (variable_struct_exists(_atk, "kills")) _atk.kills++; else _atk.kills = 1;

                        // Milestone 56: Ace Predator Kill Count Milestone (5+ Kills)
                        if (_atk.team == "ALLIED" && instance_exists(obj_GameManager) && variable_struct_exists(obj_GameManager.facilities, "roster_pilots")) {
                            for (var ap = 0; ap < array_length(obj_GameManager.facilities.roster_pilots); ap++) {
                                var _aplt = obj_GameManager.facilities.roster_pilots[ap];
                                if (_aplt.name == _atk.pilot_name || string_pos(_atk.pilot_name, _aplt.name) > 0) {
                                    _aplt.kills = (variable_struct_exists(_aplt, "kills") ? _aplt.kills : 0) + 1;
                                    if (_aplt.kills >= 5) {
                                        obj_GameManager.mutate_pilot_trait(ap, "Ace Predator");
                                    }
                                    break;
                                }
                            }
                        }

                        if (_def.team == "HOSTILE" && _ej_roll <= 35) {
                            var _pow_id = "pow_" + string(irandom(99999));
                            var _pow_pilot = {
                                id: _pow_id,
                                name: _def.pilot_name,
                                callsign: _def.callsign,
                                tier: 2,
                                current_faction_id: "faction_c",
                                is_imprisoned: true,
                                combat_stat: irandom_range(6, 9),
                                tactics_stat: irandom_range(6, 8),
                                accuracy: irandom_range(75, 88),
                                reflexes: irandom_range(72, 85),
                                affinity: _def.mech_type,
                                rank_perks: ["Deadly Aim"]
                            };
                            array_push(captured_pows, _pow_pilot);
                            add_log("[POW CAPTURED] " + _def.pilot_name + " escape pod intercepted! Transferred to Base Brig.");
                        }
                        if (_def.team == "ALLIED" && instance_exists(obj_GameManager) && variable_struct_exists(obj_GameManager.facilities, "roster_pilots")) {
                            for (var p = 0; p < array_length(obj_GameManager.facilities.roster_pilots); p++) {
                                var _plt = obj_GameManager.facilities.roster_pilots[p];
                                if (_plt.name == _def.pilot_name || string_pos(_def.pilot_name, _plt.name) > 0) {
                                    _plt.fatigue = min(100, (variable_struct_exists(_plt, "fatigue") ? _plt.fatigue : 0) + 40);
                                    var _surv_threshold = 80;
                                    if (variable_struct_exists(_plt, "mutated_traits") && is_array(_plt.mutated_traits) && array_contains(_plt.mutated_traits, "Iron Survivor")) {
                                        _surv_threshold += 15;
                                    }
                                    if (_ej_roll <= _surv_threshold) {
                                        add_log("[EJECTION SUCCESS] " + _def.pilot_name + " ejected safely via rocket-assist pod.");
                                        _plt.status = "HOSPITALIZED";
                                        _plt.recovery_days_left = 2;
                                        obj_GameManager.mutate_pilot_trait(p, "Iron Survivor");
                                    } else {
                                        add_log("[PILOT INJURED] " + _def.pilot_name + " escape pod damaged; admitted to ICU for 4 turns.");
                                        _plt.status = "HOSPITALIZED";
                                        _plt.recovery_days_left = 4;
                                        obj_GameManager.mutate_pilot_trait(p, "Iron Survivor");
                                    }
                                    break;
                                }
                            }
                        } else {
                            if (_ej_roll <= 65) {
                                add_log("[EJECTION SUCCESS] Pilot ejected safely via escape pod.");
                            } else if (_ej_roll <= 88) {
                                add_log("[PILOT INJURED] Escape pod damaged during ejection; pilot hospitalized for 3 campaign turns.");
                            } else {
                                add_log("[KIA] Catastrophic cockpit breach; pilot lost in action.");
                            }
                        }

                        // 3. Nemesis Incarceration & Bounty Triage (Goal E)
                        if (variable_struct_exists(_def, "character_id") || (variable_struct_exists(_def, "is_nemesis") && _def.is_nemesis)) {
                            if (instance_exists(obj_NemesisManager)) {
                                obj_NemesisManager.add_prisoner(_def);
                                if (variable_struct_exists(obj_NemesisManager, "active_nemeses")) {
                                    // active_nemeses list cleanup
                                }
                            }
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.funds += 150000;
                                add_log("[NEMESIS BOUNTY] +150,000 Cr bounty awarded for neutralising rival ace!");
                            }
                            scr_research_award_salvage_intel("WEAPONS", 25);
                        }

                        // 4. Boss Defeat & Victory Path 4 Trigger (Goal G)
                        if (variable_struct_exists(_def, "is_boss") && _def.is_boss) {
                            crisis_defeated = true;
                            if (instance_exists(obj_GameManager)) {
                                obj_GameManager.evaluate_campaign_victory();
                            }
                        }
                    }
                } else if (_dmg > 80) {
                    battle_cinematic.atk_expr = "CRITICAL_SUCCESS";
                    battle_cinematic.atk_radio_bark = "Direct armor breach confirmed! Target integrity failing!";
                }

                // Explosions on Defender Lead
                array_push(battle_cinematic.particles, {
                    sprite: spr_fx_explosion, x: 1026 + irandom_range(-15, 15), y: 465 + irandom_range(-20, 20),
                    frame: 0.0, speed: 0.35, scale: 1.6, alpha: 1.0
                });

                // Damage Popup
                array_push(battle_cinematic.popups, {
                    text: "-" + string(_dmg) + " DMG (" + string_upper(_part) + ")",
                    x: 1026, y: 435, color: battle_cinematic.is_crushing ? make_color_rgb(255, 220, 50) : make_color_rgb(255, 120, 80),
                    scale: battle_cinematic.is_crushing ? 1.35 : 1.15, alpha: 1.0, timer: 65
                });
            }
        }
    }

    // --- PHASE 4: Counter-Attack Salvo (Frames 145 to 205) ---
    if (_t > 145 && _t <= 205) {
        battle_cinematic.phase = 4;

        if (battle_cinematic.has_counter && _t == 150 && !battle_cinematic.applied_counter) {
            battle_cinematic.applied_counter = true;
            battle_cinematic.def_anim_state = "fire";
            battle_cinematic.def_recoil_x = 16;
            scr_audio_play_weapon(battle_cinematic.counter_weapon.short_name);

            // Spawn Counter Projectile towards Attacker
            array_push(battle_cinematic.projectiles, {
                type: battle_cinematic.counter_weapon.proj_type,
                x1: 1010, y1: 460, x2: 375, y2: 465,
                cur_x: 1010, cur_y: 460, t: 0.0, speed: 0.045,
                trail: battle_cinematic.counter_weapon.proj_type
            });
        }

        // Counter Impact at frame 175
        if (battle_cinematic.has_counter && _t == 175) {
            if (battle_cinematic.counter_is_hit) {
                battle_cinematic.atk_anim_state = "hit";
                battle_cinematic.atk_expr = "TAKING_HIT";
                battle_cinematic.atk_recoil_x = -18;
                battle_cinematic.screen_shake = 12.0;
                scr_audio_play_impact("kinetic", false);

                var _atk = battle_cinematic.attacker;
                var _cpart = battle_cinematic.counter_hit_part;
                var _cdmg = battle_cinematic.counter_damage;
                var _climb = variable_struct_get(_atk.components, _cpart);
                _climb.cur = max(0, _climb.cur - _cdmg);
                if (_climb.cur <= 0 && _climb.intact) {
                    _climb.intact = false;
                    variable_struct_set(_atk.damaged_parts, _cpart, true);
                }

                array_push(battle_cinematic.particles, {
                    sprite: spr_fx_explosion, x: 340 + irandom_range(-15, 15), y: 465 + irandom_range(-20, 20),
                    frame: 0.0, speed: 0.35, scale: 1.4, alpha: 1.0
                });
                array_push(battle_cinematic.popups, {
                    text: "[COUNTER] -" + string(_cdmg) + " (" + string_upper(_cpart) + ")",
                    x: 340, y: 435, color: make_color_rgb(255, 120, 80),
                    scale: 1.1, alpha: 1.0, timer: 55
                });
            } else {
                battle_cinematic.atk_recoil_x = -20;
                scr_audio_play_sfx(snd_mech_boost, 1.0, 0.05);
            }
        }
    }

    // --- PHASE 5: Shutter Retraction & Exit to Isometric Map (Frames 205 to 230) ---
    if (_t > 205) {
        battle_cinematic.phase = 5;
        var _out_t = (_t - 205) / 25.0;
        battle_cinematic.shutter_y = max(0.0, (1.0 - _out_t) * 115.0);

        if (_t >= 230) {
            skip_battle_cinematic();
        }
    }
};

// 3. Skip Battle Cinematic (Instant Resolution)
skip_battle_cinematic = function() {
    if (!battle_cinematic.active) return;

    var _atk = battle_cinematic.attacker;
    var _def = battle_cinematic.defender;
    var _part = battle_cinematic.hit_part;
    var _dmg = battle_cinematic.mitigated_dmg;

    if (!variable_struct_exists(_atk, "damaged_parts")) _atk.damaged_parts = { head: false, torso: false, arm_left: false, arm_right: false, legs: false, backpack: false };
    if (!variable_struct_exists(_def, "damaged_parts")) _def.damaged_parts = { head: false, torso: false, arm_left: false, arm_right: false, legs: false, backpack: false };

    // Apply primary damage if not applied yet
    if (!battle_cinematic.applied_primary) {
        battle_cinematic.applied_primary = true;
        if (battle_cinematic.is_hit) {
            // Goal G: Boss Phase Barrier Absorption on Skip
            if (variable_struct_exists(_def, "barrier_cur") && _def.barrier_cur > 0) {
                var _absorbed = min(_def.barrier_cur, _dmg);
                _def.barrier_cur -= _absorbed;
                _dmg -= _absorbed;
                add_log("[BARRIER ABSORB] Ouroboros Prime Phase Barrier absorbed " + string(_absorbed) + " damage!");
            }

            var _limb = variable_struct_get(_def.components, _part);
            _limb.cur = max(0, _limb.cur - _dmg);
            add_log("[HIT] " + _atk.callsign + " struck " + _def.callsign + " " + _limb.name + " for " + string(_dmg) + " damage!");

            // Goal F: Suppression & Cover Degradation on Skip
            if (!variable_struct_exists(_def, "hits_taken_this_turn")) _def.hits_taken_this_turn = 0;
            _def.hits_taken_this_turn++;
            var _is_supp_wpn_sk = (battle_cinematic.weapon.proj_type == "ROTARY_VULCAN" || string_pos("VULCAN", string_upper(battle_cinematic.weapon.name)) > 0 || string_pos("GATLING", string_upper(battle_cinematic.weapon.name)) > 0 || string_pos("AUTOCANNON", string_upper(battle_cinematic.weapon.name)) > 0 || string_pos("SUPPRESS", string_upper(battle_cinematic.weapon.name)) > 0);
            if (_is_supp_wpn_sk || _def.hits_taken_this_turn >= 2) {
                _def.is_suppressed = true;
                add_log("[CROSSFIRE PIN] " + _def.callsign + " pinned down by sustained suppressive fire!");
            }
            var _is_heavy_ord_sk = (battle_cinematic.weapon.proj_type == "RAILGUN" || battle_cinematic.weapon.proj_type == "KINETIC_CANNON" || battle_cinematic.weapon.proj_type == "CANNON" || string_pos("CANNON", string_upper(battle_cinematic.weapon.name)) > 0 || string_pos("RAILGUN", string_upper(battle_cinematic.weapon.name)) > 0 || string_pos("120MM", string_upper(battle_cinematic.weapon.name)) > 0 || string_pos("SIEGE", string_upper(battle_cinematic.weapon.name)) > 0 || battle_cinematic.weapon.damage >= 55);
            if (_is_heavy_ord_sk && grid_cover[_def.grid_c][_def.grid_r] > 0) {
                if (grid_cover[_def.grid_c][_def.grid_r] == 2) {
                    grid_cover[_def.grid_c][_def.grid_r] = 1;
                    add_log("[COVER BREACH] Fortified bastion at [" + string(_def.grid_c) + "," + string(_def.grid_r) + "] fractured to rubble!");
                } else if (grid_cover[_def.grid_c][_def.grid_r] == 1) {
                    grid_cover[_def.grid_c][_def.grid_r] = 0;
                    add_log("[COVER DESTROYED] Rubble position at [" + string(_def.grid_c) + "," + string(_def.grid_r) + "] obliterated by heavy ordnance!");
                }
            }

            if (_def.squad_type == "PLATOON_3") {
                var _hp_r = _def.components.torso.cur / _def.components.torso.max;
                if (_hp_r < 0.33) _def.squad_members_count = 1;
                else if (_hp_r < 0.66 && _def.squad_members_count > 2) _def.squad_members_count = 2;
            }

            if (_limb.cur <= 0 && _limb.intact) {
                _limb.intact = false;
                variable_struct_set(_def.damaged_parts, _part, true);
                add_log("[CRITICAL BREACH] " + _def.callsign + " " + _limb.name + " HAS BEEN SEVERED!");
                if (_part == "backpack" && (_def.id == "BOSS_OUROBOROS" || (variable_struct_exists(_def, "is_apex_boss") && _def.is_apex_boss))) {
                    _def.barrier_cur = 0;
                    add_log("[PHASE SHIELD COLLAPSE] Phase Barrier Emitter severed! Boss shields permanently offline!");
                }
                if (_part == "torso") {
                    _def.is_destroyed = true;
                    _def.anim_state = "destroyed";
                    _def.anim_timer = 40;
                    add_log("[CATASTROPHIC KILL] " + _def.callsign + " REACTOR BREACH! Unit neutralized.");

                    // 1. Tactical Battlefield Wreckage Cover (+20% cover on tile)
                    grid_cover[_def.grid_c][_def.grid_r] = 2;
                    add_log("[FIELD WRECKAGE] Smoldering chassis created tactical cover on tile (" + string(_def.grid_c) + ", " + string(_def.grid_r) + ")");

                    // 2. Pilot Ejection Survival Roll
                    var _ej_roll = irandom_range(1, 100);
                    if (_ej_roll <= 65) {
                        add_log("[EJECTION SUCCESS] Pilot ejected safely via escape pod.");
                    } else if (_ej_roll <= 88) {
                        add_log("[PILOT INJURED] Escape pod damaged during ejection; pilot hospitalized for 3 campaign turns.");
                    } else {
                        add_log("[KIA] Catastrophic cockpit breach; pilot lost in action.");
                    }

                    // Goal G: Apex Crisis Boss Defeat & Campaign Victory Path 4
                    if (_def.id == "BOSS_OUROBOROS" || (variable_struct_exists(_def, "is_apex_boss") && _def.is_apex_boss)) {
                        if (instance_exists(obj_GameManager)) {
                            obj_GameManager.crisis_defeated = true;
                            obj_GameManager.funds += 500000;
                            obj_GameManager.evaluate_campaign_victory();
                        }
                        scr_research_award_salvage_intel(choose("WEAPONS", "REACTORS", "SHIELDS", "UPGRADES"), 1.00);
                        add_log("[APEX CRISIS DEFEATED] DEUS-MACHINA: OUROBOROS PRIME CORE DESTROYED! Sol System Saved!");
                        if (instance_exists(obj_HQTerminal)) {
                            obj_HQTerminal.show_toast("APEX CRISIS VANQUISHED! SOL SYSTEM SAVED! +500,000 Cr & Eureka Tech!", c_lime);
                        }
                    }

                    if (instance_exists(obj_BlueprintManager)) {
                        var _vic_c = variable_struct_get(_def, "chassis_id") ?? (variable_struct_get(_def, "mech_type") ?? "ironclad");
                        var _atk_c = variable_struct_get(_atk, "chassis_id") ?? (variable_struct_get(_atk, "mech_type") ?? "ironclad");
                        obj_BlueprintManager.record_suit_casualty(_vic_c, _atk_c);
                    }
                    if (instance_exists(obj_NemesisManager)) {
                        var _vic_id = variable_struct_get(_def, "character_id") ?? variable_struct_get(_def, "pilot_name") ?? _def.id;
                        var _atk_id = variable_struct_get(_atk, "character_id") ?? variable_struct_get(_atk, "pilot_name") ?? "player";
                        scr_nemesis_event_dispatch(_vic_id, _atk_id, "combat_kill");

                        if (variable_struct_get(_def, "is_nemesis") == true || string_pos("NEMESIS_", _def.id) > 0) {
                            var _bounty_cr = 150000;
                            if (instance_exists(obj_GameManager)) obj_GameManager.funds += _bounty_cr;
                            add_log("[NEMESIS TRIAGE] Rival Ace neutralized! Claimed +" + string(_bounty_cr) + " Cr contract bounty!");
                        }
                    }
                }
            }
        } else {
            add_log("[MISS] " + _atk.callsign + " volley missed " + _def.callsign + "!");
        }
    }

    // Apply counter-attack damage if not resolved
    if (battle_cinematic.has_counter && !battle_cinematic.applied_counter) {
        battle_cinematic.applied_counter = true;
        if (battle_cinematic.counter_is_hit) {
            var _cpart = battle_cinematic.counter_hit_part;
            var _cdmg = battle_cinematic.counter_damage;
            var _climb = variable_struct_get(_atk.components, _cpart);
            _climb.cur = max(0, _climb.cur - _cdmg);
            add_log("[COUNTER HIT] " + _def.callsign + " retaliated against " + _atk.callsign + " " + _climb.name + " for " + string(_cdmg) + " damage!");

            if (_climb.cur <= 0 && _climb.intact) {
                _climb.intact = false;
                variable_struct_set(_atk.damaged_parts, _cpart, true);
                add_log("[CRITICAL BREACH] " + _atk.callsign + " " + _climb.name + " HAS BEEN SEVERED!");
                if (_cpart == "torso") {
                    _atk.is_destroyed = true;
                    _atk.anim_state = "destroyed";
                    _atk.anim_timer = 40;
                    add_log("[CATASTROPHIC KILL] " + _atk.callsign + " neutralized in combat!");
                }
            }
        }
    }

    // Deduct AP
    _atk.current_ap = max(0, _atk.current_ap - battle_cinematic.weapon.ap_cost);
    if (battle_cinematic.has_counter && !is_undefined(battle_cinematic.counter_weapon)) {
        _def.current_ap = max(0, _def.current_ap - battle_cinematic.counter_weapon.ap_cost);
    }

    battle_cinematic.active = false;
    battle_cinematic.timer = 0;
    battle_cinematic.shutter_y = 0;
    state = battle_cinematic.return_state;

    // Check Turn & Victory Conditions
    check_combat_resolution();
};

// 4. Draw Battle Cinematic Stage (Widescreen 2.39:1 Cutscene)
draw_battle_cinematic_stage = function() {
    if (!battle_cinematic.active) return;

    draw_set_halign(fa_left);
    draw_set_valign(fa_top);

    var _gw = display_get_gui_width();
    var _gh = display_get_gui_height();
    var _shut = battle_cinematic.shutter_y;
    var _top_y = _shut;
    var _bot_y = _gh - _shut;

    var _shake_x = (battle_cinematic.screen_shake > 0) ? random_range(-battle_cinematic.screen_shake, battle_cinematic.screen_shake) : 0;
    var _shake_y = (battle_cinematic.screen_shake > 0) ? random_range(-battle_cinematic.screen_shake, battle_cinematic.screen_shake) : 0;

    // ---------------------------------------------------------------------
    // A. PANORAMIC ENVIRONMENTAL BACKDROP
    // ---------------------------------------------------------------------
    if (battle_cinematic.is_space) {
        // Deep Space / Vacuum Void
        draw_rectangle_color(0, _top_y, _gw, _bot_y, make_color_rgb(4, 7, 16), make_color_rgb(4, 7, 16), make_color_rgb(14, 22, 42), make_color_rgb(14, 22, 42), false);

        draw_set_color(make_color_rgb(10, 36, 70));
        draw_circle(_gw * 0.72, _gh * 1.05, 420, false);
        draw_set_color(make_color_rgb(50, 160, 255));
        draw_set_alpha(0.35);
        draw_circle(_gw * 0.72, _gh * 1.05, 425, true);
        draw_circle(_gw * 0.72, _gh * 1.05, 432, true);
        draw_set_alpha(1.0);

        draw_set_color(make_color_rgb(20, 32, 54));
        draw_rectangle(240, 210, 480, 265, false);
        draw_set_color(make_color_rgb(40, 65, 105));
        draw_rectangle(240, 210, 480, 265, true);

        for (var i = 0; i < 70; i++) {
            var _sx = (i * 197 + 53) % _gw;
            var _sy = _top_y + ((i * 131 + 29) % max(1, _bot_y - _top_y));
            var _tw = 0.35 + 0.65 * abs(sin((current_time * 0.002) + i));
            draw_set_color(c_white);
            draw_set_alpha(_tw);
            draw_point(_sx, _sy);
            if (i % 6 == 0) draw_circle(_sx, _sy, 1.2, false);
        }
        draw_set_alpha(1.0);
    } else if (battle_cinematic.is_water) {
        // Coastal Harbor / Water Canal
        draw_rectangle_color(0, _top_y, _gw, _bot_y, make_color_rgb(10, 28, 48), make_color_rgb(14, 38, 64), make_color_rgb(6, 18, 32), make_color_rgb(8, 22, 38), false);
        var _wave_y = 500;
        draw_set_color(make_color_rgb(18, 55, 92));
        draw_rectangle(0, _wave_y, _gw, _bot_y, false);
    } else {
        // Terran Badlands / Granite Redoubt
        draw_rectangle_color(0, _top_y, _gw, _bot_y, make_color_rgb(22, 16, 26), make_color_rgb(32, 24, 38), make_color_rgb(14, 10, 18), make_color_rgb(18, 12, 22), false);
        draw_set_color(make_color_rgb(38, 28, 36));
        draw_rectangle(0, 480, _gw, _bot_y, false);
    }

    // CRT Scanline Authenticity Pass
    if (sprite_exists(spr_snes_crt_scanline)) {
        draw_sprite_tiled_ext(spr_snes_crt_scanline, 0, 0, _top_y, 1.0, 1.0, c_white, 0.12);
    }

    // ---------------------------------------------------------------------
    // B. MOBILE SUIT UNITS RENDERING
    // ---------------------------------------------------------------------
    var _atk = battle_cinematic.attacker;
    var _def = battle_cinematic.defender;
    var _base_ground_y = 480;

    // 1. ATTACKER FORMATION (LEFT SIDE, FACING RIGHT)
    var _ax = 340 + battle_cinematic.atk_recoil_x + _shake_x + battle_cinematic.atk_dash_x;
    var _ay = _base_ground_y + battle_cinematic.atk_recoil_y + _shake_y;
    if (battle_cinematic.is_air_atk) _ay -= (65 + sin(current_time * 0.004) * 6);
    if (battle_cinematic.is_water) _ay += 12;

    scr_draw_animated_mobile_suit(_atk, _ax, _ay, 1.30, 1, battle_cinematic.atk_anim_state, -1, _atk.image_blend, "front");

    if (_atk.squad_type == "PLATOON_3") {
        if (_atk.squad_members_count >= 2) {
            var _w1x = 210 + battle_cinematic.atk_wing1_recoil_x + _shake_x;
            var _w1y = _base_ground_y - 60 + (battle_cinematic.is_air_atk ? -60 : 0);
            scr_draw_animated_mobile_suit(_atk, _w1x, _w1y, 1.08, 1, battle_cinematic.atk_anim_state, -1, _atk.image_blend, "front");
        }
        if (_atk.squad_members_count >= 3) {
            var _w2x = 170 + battle_cinematic.atk_wing2_recoil_x + _shake_x;
            var _w2y = _base_ground_y + 45 + (battle_cinematic.is_air_atk ? -60 : 0);
            scr_draw_animated_mobile_suit(_atk, _w2x, _w2y, 1.08, 1, battle_cinematic.atk_anim_state, -1, _atk.image_blend, "front");
        }
    }

    // 2. DEFENDER FORMATION (RIGHT SIDE, FACING LEFT)
    var _dx = 1026 + battle_cinematic.def_recoil_x + _shake_x;
    var _dy = _base_ground_y + battle_cinematic.def_recoil_y + _shake_y;
    if (battle_cinematic.is_air_def) _dy -= (65 + sin(current_time * 0.004 + 1.2) * 6);
    if (battle_cinematic.is_water) _dy += 12;

    scr_draw_animated_mobile_suit(_def, _dx, _dy, 1.30, -1, battle_cinematic.def_anim_state, -1, _def.image_blend, "front");

    if (_def.squad_type == "PLATOON_3") {
        if (_def.squad_members_count >= 2) {
            var _dw1x = 1156 + battle_cinematic.def_wing1_recoil_x + _shake_x;
            var _dw1y = _base_ground_y - 60 + (battle_cinematic.is_air_def ? -60 : 0);
            scr_draw_animated_mobile_suit(_def, _dw1x, _dw1y, 1.08, -1, battle_cinematic.def_anim_state, -1, _def.image_blend, "front");
        }
        if (_def.squad_members_count >= 3) {
            var _dw2x = 1196 + battle_cinematic.def_wing2_recoil_x + _shake_x;
            var _dw2y = _base_ground_y + 45 + (battle_cinematic.is_air_def ? -60 : 0);
            scr_draw_animated_mobile_suit(_def, _dw2x, _dw2y, 1.08, -1, battle_cinematic.def_anim_state, -1, _def.image_blend, "front");
        }
    }

    // Dynamic Melee Cleavage Arc
    if (battle_cinematic.melee_cleave_timer > 0) {
        var _cleave_a = battle_cinematic.melee_cleave_timer / 24.0;
        draw_set_alpha(_cleave_a);
        draw_set_color(c_white);
        draw_line_width(1026 - 45, 420 - 55, 1026 + 45, 420 + 55, 6.0);
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_line_width(1026 - 45, 420 - 55, 1026 + 45, 420 + 55, 2.5);
        draw_set_alpha(1.0);
    }

    // --- 3. DRAW SPENT BRASS CASINGS ---
    for (var i = 0; i < array_length(battle_cinematic.casings); i++) {
        var _cs = battle_cinematic.casings[i];
        draw_set_color(make_color_rgb(255, 215, 60));
        draw_line_width(_cs.x, _cs.y, _cs.x + lengthdir_x(7, _cs.angle), _cs.y + lengthdir_y(7, _cs.angle), 2.5);
    }

    // --- 4. DRAW IN-FLIGHT PROJECTILES & TRACERS ---
    for (var i = 0; i < array_length(battle_cinematic.projectiles); i++) {
        var _pj = battle_cinematic.projectiles[i];
        if (_pj.type == "ROTARY_VULCAN") {
            draw_set_color(make_color_rgb(255, 240, 140));
            draw_line_width(_pj.cur_x - 18, _pj.cur_y, _pj.cur_x + 18, _pj.cur_y, 3.0);
            draw_set_color(c_white);
            draw_line_width(_pj.cur_x - 8, _pj.cur_y, _pj.cur_x + 8, _pj.cur_y, 1.5);
        } else if (_pj.type == "BEAM_PULSE" || string_pos("BEAM", _pj.type) > 0) {
            draw_set_color(make_color_rgb(0, 220, 255));
            draw_line_width(_pj.cur_x - 35, _pj.cur_y, _pj.cur_x + 35, _pj.cur_y, 6.0);
            draw_set_color(c_white);
            draw_line_width(_pj.cur_x - 25, _pj.cur_y, _pj.cur_x + 25, _pj.cur_y, 2.5);
        } else if (_pj.type == "MICRO_MISSILE") {
            draw_set_color(make_color_rgb(220, 225, 235));
            draw_set_alpha(0.5);
            draw_circle(_pj.cur_x - 12, _pj.cur_y, 5.0, false);
            draw_circle(_pj.cur_x - 22, _pj.cur_y, 7.0, false);
            draw_set_alpha(1.0);
            if (sprite_exists(spr_proj_missile)) {
                draw_sprite_ext(spr_proj_missile, 0, _pj.cur_x, _pj.cur_y, 1.4, 1.4, point_direction(_pj.x1, _pj.y1, _pj.x2, _pj.y2), c_white, 1.0);
            }
        } else {
            if (sprite_exists(spr_proj_cannon_120mm)) {
                draw_sprite_ext(spr_proj_cannon_120mm, 0, _pj.cur_x, _pj.cur_y, 1.5, 1.5, point_direction(_pj.x1, _pj.y1, _pj.x2, _pj.y2), c_white, 1.0);
            }
        }
    }

    // --- 5. DRAW EXPLOSION & SPARK PARTICLES ---
    for (var i = 0; i < array_length(battle_cinematic.particles); i++) {
        var _pt = battle_cinematic.particles[i];
        if (sprite_exists(_pt.sprite)) {
            draw_sprite_ext(_pt.sprite, floor(_pt.frame), _pt.x + _shake_x, _pt.y + _shake_y, _pt.scale, _pt.scale, 0, c_white, _pt.alpha);
        }
    }

    // --- 6. TARGET ACQUISITION RETICLE (PHASE 0) ---
    if (battle_cinematic.phase == 0) {
        var _pulse = 0.8 + 0.2 * sin(current_time * 0.01);
        draw_set_color(make_color_rgb(255, 60, 60));
        draw_set_alpha(_pulse);
        draw_circle(_dx, _dy - 65, 55, true);
        draw_line_width(_dx - 70, _dy - 65, _dx - 40, _dy - 65, 2.0);
        draw_line_width(_dx + 40, _dy - 65, _dx + 70, _dy - 65, 2.0);
        draw_line_width(_dx, _dy - 135, _dx, _dy - 105, 2.0);
        draw_line_width(_dx, _dy - 25, _dx, _dy + 5, 2.0);
        draw_set_color(make_color_rgb(255, 120, 120));
        draw_text(_dx - 60, _dy - 150, "TARGET ACQUIRED // LOCK");
        draw_set_alpha(1.0);
    }

    // --- 7. FLOATING DAMAGE POPUPS ---
    draw_set_halign(fa_center);
    for (var i = 0; i < array_length(battle_cinematic.popups); i++) {
        var _pop = battle_cinematic.popups[i];
        draw_set_alpha(_pop.alpha);
        draw_set_color(c_black);
        draw_text_transformed(_pop.x + 1, _pop.y + 1, _pop.text, _pop.scale, _pop.scale, 0);
        draw_set_color(_pop.color);
        draw_text_transformed(_pop.x, _pop.y, _pop.text, _pop.scale, _pop.scale, 0);
        draw_set_alpha(1.0);
    }
    draw_set_halign(fa_left);

    // ---------------------------------------------------------------------
    // C. DIEGETIC RETRO COCKPIT TELEMETRY HUD (BOTTOM LETTERBOX SHUTTER)
    // ---------------------------------------------------------------------
    // Fullscreen Screen Flash
    if (battle_cinematic.flash_alpha > 0) {
        draw_set_color(c_white);
        draw_set_alpha(battle_cinematic.flash_alpha);
        draw_rectangle(0, 0, _gw, _gh, false);
        draw_set_alpha(1.0);
    }

    // Top Letterbox Shutter
    draw_set_color(c_black);
    draw_rectangle(0, 0, _gw, _shut, false);
    draw_set_color(make_color_rgb(0, 200, 255));
    draw_line_width(0, _shut, _gw, _shut, 2.0);

    // Top Ribbon Header Information
    if (_shut >= 40) {
        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(24, _shut - 28, "THEATER: " + string_upper(battle_cinematic.theater) + " // ENGAGEMENT GRID: CLASH DUEL");
        draw_set_color(make_color_rgb(255, 215, 80));
        draw_text(_gw / 2 - 120, _shut - 28, "TACTICAL COMBAT CLASH // PHASE: " + string(battle_cinematic.phase));
    }

    // Bottom Letterbox Shutter
    draw_set_color(c_black);
    draw_rectangle(0, _bot_y, _gw, _gh, false);
    draw_set_color(make_color_rgb(0, 200, 255));
    draw_line_width(0, _bot_y, _gw, _bot_y, 2.0);

    // Render Cockpit Telemetry Decks (Left: Attacker, Right: Defender, Center: Combat Feed)
    if (_shut >= 60) {
        var _hud_h = 100;
        var _hud_y = _bot_y + 8;

        // 1. LEFT COCKPIT (ATTACKER)
        var _atk_panel_w = 460;
        scr_draw_snes_panel(16, _hud_y, _atk_panel_w, _hud_h, "", -1, false, 0.04);

        if (sprite_exists(battle_cinematic.atk_portrait)) {
            draw_sprite_ext(battle_cinematic.atk_portrait, 0, 24, _hud_y + 10, 0.40, 0.40, 0, c_white, 1.0);
            draw_set_color(make_color_rgb(0, 200, 255));
            draw_rectangle(24, _hud_y + 10, 24 + 80, _hud_y + 10 + 80, true);
        }

        // Attacker Pilot & Expression Badge
        var _expr_col = (battle_cinematic.atk_expr == "CRITICAL_SUCCESS") ? make_color_rgb(255, 220, 60) : ((battle_cinematic.atk_expr == "TAKING_HIT") ? make_color_rgb(255, 80, 80) : make_color_rgb(60, 240, 120));
        draw_set_color(_expr_col);
        draw_text(112, _hud_y + 8, "[" + battle_cinematic.atk_expr + "] " + _atk.pilot_name);
        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(112, _hud_y + 24, _atk.callsign + " | " + string_upper(_atk.mech_type));

        // Radio Bark Ticker
        var _cursor = ((current_time / 250) % 2 >= 1) ? "_" : " ";
        draw_set_color(make_color_rgb(60, 240, 120));
        draw_text(112, _hud_y + 42, "> " + chr(34) + battle_cinematic.atk_radio_bark + _cursor + chr(34));

        // 5 Front Mission Limb Bars (Attacker)
        var _parts = ["head", "torso", "arm_left", "arm_right", "legs"];
        var _pnames = ["HD", "TR", "LA", "RA", "LG"];
        for (var p = 0; p < 5; p++) {
            var _l = variable_struct_get(_atk.components, _parts[p]);
            var _ratio = clamp(_l.cur / max(1, _l.max), 0.0, 1.0);
            var _bx = 112 + p * 68;
            var _by = _hud_y + 64;
            var _bcol = (_ratio > 0.6) ? make_color_rgb(60, 240, 100) : ((_ratio > 0.25) ? make_color_rgb(240, 200, 50) : make_color_rgb(255, 60, 60));
            if (!_l.intact || _l.cur <= 0) _bcol = make_color_rgb(80, 80, 80);

            draw_set_color(make_color_rgb(150, 170, 200));
            draw_text(_bx, _by, _pnames[p]);
            draw_set_color(make_color_rgb(20, 28, 40));
            draw_rectangle(_bx, _by + 16, _bx + 60, _by + 24, false);
            draw_set_color(_bcol);
            draw_rectangle(_bx, _by + 16, _bx + (60 * _ratio), _by + 24, false);
            draw_set_color(make_color_rgb(60, 80, 110));
            draw_rectangle(_bx, _by + 16, _bx + 60, _by + 24, true);
        }

        // 2. RIGHT COCKPIT (DEFENDER)
        var _def_panel_w = 460;
        var _def_px = _gw - _def_panel_w - 16;
        scr_draw_snes_panel(_def_px, _hud_y, _def_panel_w, _hud_h, "", -1, false, 0.04);

        if (sprite_exists(battle_cinematic.def_portrait)) {
            draw_sprite_ext(battle_cinematic.def_portrait, 0, _gw - 104, _hud_y + 10, 0.40, 0.40, 0, c_white, 1.0);
            draw_set_color(make_color_rgb(255, 80, 80));
            draw_rectangle(_gw - 104, _hud_y + 10, _gw - 104 + 80, _hud_y + 10 + 80, true);
        }

        var _d_expr_col = (battle_cinematic.def_expr == "CRIPPLED") ? make_color_rgb(255, 50, 50) : ((battle_cinematic.def_expr == "EVADED") ? make_color_rgb(80, 240, 255) : make_color_rgb(255, 140, 80));
        draw_set_color(_d_expr_col);
        draw_text(_def_px + 14, _hud_y + 8, "[" + battle_cinematic.def_expr + "] " + _def.pilot_name);
        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(_def_px + 14, _hud_y + 24, _def.callsign + " | " + string_upper(_def.mech_type));

        draw_set_color(make_color_rgb(255, 180, 60));
        draw_text(_def_px + 14, _hud_y + 42, "> " + chr(34) + battle_cinematic.def_radio_bark + _cursor + chr(34));

        // 5 Front Mission Limb Bars (Defender)
        for (var p = 0; p < 5; p++) {
            var _l = variable_struct_get(_def.components, _parts[p]);
            var _ratio = clamp(_l.cur / max(1, _l.max), 0.0, 1.0);
            var _bx = _def_px + 14 + p * 68;
            var _by = _hud_y + 64;
            var _bcol = (_ratio > 0.6) ? make_color_rgb(60, 240, 100) : ((_ratio > 0.25) ? make_color_rgb(240, 200, 50) : make_color_rgb(255, 60, 60));
            if (!_l.intact || _l.cur <= 0) _bcol = make_color_rgb(80, 80, 80);

            if (battle_cinematic.limb_flash_timer > 0 && battle_cinematic.limb_flash_part == _parts[p]) {
                if ((battle_cinematic.limb_flash_timer % 4) < 2) _bcol = c_white;
            }

            draw_set_color(make_color_rgb(150, 170, 200));
            draw_text(_bx, _by, _pnames[p]);
            draw_set_color(make_color_rgb(20, 28, 40));
            draw_rectangle(_bx, _by + 16, _bx + 60, _by + 24, false);
            draw_set_color(_bcol);
            draw_rectangle(_bx, _by + 16, _bx + (60 * _ratio), _by + 24, false);
            draw_set_color(make_color_rgb(60, 80, 110));
            draw_rectangle(_bx, _by + 16, _bx + 60, _by + 24, true);
        }

        // 3. CENTER COMBAT COMPUTER TERMINAL
        var _cen_x = 484;
        var _cen_w = _def_px - _cen_x - 12;
        scr_draw_snes_panel(_cen_x, _hud_y, _cen_w, _hud_h, "TACTICAL TELEMETRY", make_color_rgb(0, 200, 255), false);

        draw_set_color(make_color_rgb(255, 215, 80));
        draw_text(_cen_x + 12, _hud_y + 24, "ORDNANCE: " + battle_cinematic.weapon.name);
        draw_set_color(make_color_rgb(160, 200, 240));
        draw_text(_cen_x + 12, _hud_y + 42, "HIT: " + string(battle_cinematic.hit_chance) + "% | EVADE: " + string(_def.evasion) + "%");
        draw_set_color(make_color_rgb(80, 240, 120));
        draw_text(_cen_x + 12, _hud_y + 60, "CALC DMG: " + string(battle_cinematic.mitigated_dmg) + " " + battle_cinematic.flank_tag + " " + battle_cinematic.elev_tag);

        // Fast-Forward Key hint
        var _sk_pulse = 0.7 + 0.3 * sin(current_time * 0.008);
        draw_set_color(make_color_rgb(0, 210, 255));
        draw_set_alpha(_sk_pulse);
        draw_text(_cen_x + 12, _hud_y + 78, "[SPACE / CLICK] FAST-FORWARD >>");
        draw_set_alpha(1.0);
    }
};

select_unit(0);

show_debug_message("[obj_BattleManager] Grand-Scale Isometric Arena initialized successfully.");
