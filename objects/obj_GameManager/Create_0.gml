/// @description obj_GameManager Create Event
// Core Global Game State Singleton: Funds, Temporal Calendar, Facilities, Mining Operations & Narrative Engine
// Strictly adheres to docs/01, 04, 06, 07, 08

// 1. Enforce Persistent Singleton Pattern
if (instance_number(obj_GameManager) > 1) {
    show_debug_message("[obj_GameManager] Duplicate singleton detected. Destroying instance (ID: " + string(id) + ")");
    instance_destroy();
    exit;
}

persistent = true;
show_debug_message("[obj_GameManager] Initializing Persistent Game Manager Singleton...");

// 2. Economy & Treasury State
funds = 100000;         // Current Credits (Cr) - Balanced PMC Seed Capital (100k Cr)
escrow_funds = 0;       // Escrow withheld for pending operations

// --- GOAL A: STRATEGIC LOGISTICS & FLEET UPKEEP ---
supply_starvation = false;        // True when funds < 0 or Tritium depleted
mech_upkeep_cr_per_unit = 350;    // Credits per strategic turn per deployable mech
mech_upkeep_tritium_ratio = 2;    // 1 Tritium consumed per 2 deployable mechs (min 1 if mechs > 0)
total_fleet_upkeep_cr = 0;        // Cached total credit upkeep
total_fleet_tritium_burn = 0;     // Cached total tritium fuel burn

// --- GOAL B & C: PILOT HELPER & FLAGSHIP THEATER MAPPING ---
pilot_add_xp = function(_pilot_id, _xp_gain) {
    if (!variable_struct_exists(facilities, "roster_pilots")) return;
    for (var p = 0; p < array_length(facilities.roster_pilots); p++) {
        var _plt = facilities.roster_pilots[p];
        if (_plt.id == _pilot_id || _plt.character_id == _pilot_id) {
            _plt.xp = (variable_struct_exists(_plt, "xp") ? _plt.xp : 0) + _xp_gain;

            // Milestone 56: Automatic Level-Up & Unspent Stat Point Issuance
            var _cur_lvl = variable_struct_exists(_plt, "level") ? _plt.level : 1;
            var _calc_lvl = 1 + floor(_plt.xp / 150);
            if (_calc_lvl > _cur_lvl) {
                var _lvl_delta = _calc_lvl - _cur_lvl;
                _plt.level = _calc_lvl;
                if (!variable_struct_exists(_plt, "unspent_stat_points")) _plt.unspent_stat_points = 0;
                _plt.unspent_stat_points += _lvl_delta * 2;
                array_push(last_turn_events, "* PROMOTION: " + _plt.name + " (" + _plt.callsign + ") reached Level " + string(_calc_lvl) + "! Earned +" + string(_lvl_delta * 2) + " Stat Points!");
                if (instance_exists(obj_HQTerminal)) {
                    obj_HQTerminal.show_toast("PROMOTION: " + _plt.callsign + " Level " + string(_calc_lvl) + " (+" + string(_lvl_delta * 2) + " Stat Points)!", c_yellow);
                }
            }

            if (!variable_struct_exists(_plt, "rank_perks") || !is_array(_plt.rank_perks)) {
                _plt.rank_perks = [];
            }
            // Check Ace Perk thresholds
            if (_plt.xp >= 100 && !array_contains(_plt.rank_perks, "Quick Draw")) {
                array_push(_plt.rank_perks, "Quick Draw");
                array_push(last_turn_events, "* ACE PERK UNLOCKED: " + _plt.name + " (" + _plt.callsign + ") earned 'Quick Draw' (+1 AP on Turn 1)!");
                if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("★ ACE PERK: " + _plt.callsign + " unlocked Quick Draw!", c_yellow);
            }
            if (_plt.xp >= 250 && !array_contains(_plt.rank_perks, "Deadeye")) {
                array_push(_plt.rank_perks, "Deadeye");
                array_push(last_turn_events, "* ACE PERK UNLOCKED: " + _plt.name + " (" + _plt.callsign + ") earned 'Deadeye' (+15% Critical Chance)!");
                if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("★ ACE PERK: " + _plt.callsign + " unlocked Deadeye!", c_yellow);
            }
            if (_plt.xp >= 500 && !array_contains(_plt.rank_perks, "Overdrive")) {
                array_push(_plt.rank_perks, "Overdrive");
                array_push(last_turn_events, "* ACE PERK UNLOCKED: " + _plt.name + " (" + _plt.callsign + ") earned 'Overdrive' (+20% DMG when wounded)!");
                if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("★ ACE PERK: " + _plt.callsign + " unlocked Overdrive!", c_yellow);
            }
            return;
        }
    }
};

flagship_is_in_theater = function(_theater_name) {
    if (!variable_struct_exists(flagship, "current_sphere")) return false;
    if (flagship.transit_turns_left > 0) return false; // En route, not stationed

    var _cs = string_lower(flagship.current_sphere);
    var _tn = string_upper(_theater_name);

    if (_tn == "EARTH" && (string_pos("earth", _cs) > 0 || string_pos("lagrange", _cs) > 0)) return true;
    if (_tn == "SPACE" && (string_pos("space", _cs) > 0 || string_pos("colon", _cs) > 0 || string_pos("asteroid", _cs) > 0 || string_pos("jovian", _cs) > 0 || string_pos("saturn", _cs) > 0)) return true;
    if (_tn == "MARS" && (string_pos("mars", _cs) > 0 || string_pos("martian", _cs) > 0)) return true;

    return false;
};       // Escrow withheld for pending operations       // Escrow withheld for pending operations

// 3. Turn-Based Strategic Simulation State
current_turn = 1;           // Strategic Turn Counter
current_cycle_year = 214;    // Standard Galactic Calendar Year
current_cycle_day = 1;      // Day within current operational cycle
last_turn_events = [];

    // Advance Strategic R&D Tech Tree Research Slots (HoI4 Engine)
    scr_research_advance_turn();       // Historical log of transactions and developments from the latest turn
show_turn_report = false;    // Modal toggle for turn transition summary
time_speed = 0;              // Preserved as 0 (turn-based architecture)

// 3b. Career Legacy & Sandbox Endgame State (docs/12)
career_summary = undefined;  // Sid Meier's Pirates style retirement dossier struct
total_sorties_won = 0;       // Total successful PMC sorties and sector conquests

// 3b-ii. Grand Campaign Victory Paths State (Goal D)
campaign_won = false;
campaign_victory_claimed = false;
campaign_victory_path = "";  // "MONOPOLIST", "WARLORD", "ARCHEOTECH", "CRISIS_SAVIOR"
campaign_victory_data = undefined;
crisis_defeated = false;

// 3b-iii. Corporate Espionage & Pilot Poaching State (Goal E)
pending_poaching_offer = undefined;

// 3c. Timeline Tech Eras & Progression (docs/27 & doc 38 Prometheus Catalyst)
timeline_era = 0; // 0 = Conventional Steel & Jet Fuel, 1 = First Mover Catalyst, 2 = Industrial Escalation, 3 = Total War, 4 = Apex Crisis
timeline_era_name = "ERA 0: CONVENTIONAL STEEL & JET FUEL";
first_mobile_suit_created = true; // Player foundry created the world's first working bipedal humanoid frame
first_mobile_suit_deployed = false; // Maiden combat deployment triggers global revolution
reverse_engineering_progress = {
    corp_vhi: 0.0,   // Vanguard Heavy Industries (Terran)
    corp_aod: 0.0,   // Astraea Orbital Dynamics (Colonies)
    corp_rust: 0.0,  // Rustworks Scrap Forge (Syndicates)
    corp_hats: 0.0   // Hyperion Advanced Tech (Zaibatsu)
};
reverse_engineering_unlocked = false;
timeline_era_year_start = 214;

// 3d. Player Commander Executive Dossier & Origins (Doc 51 RPG Framework)
has_completed_dossier = false;
has_completed_prologue = false;
prologue_active = false;
has_completed_intro = false;

commander_backgrounds = {
    bg_terran_officer: {
        id: "bg_terran_officer",
        title: "Ex-Terran Coalition Officer",
        default_name: "Cmdr. Alexei Kane",
        default_callsign: "VANGUARD",
        portrait_asset: spr_portrait_commander_male,
        faction_standings: { faction_a: 15, faction_b: -10, faction_c: -5 },
        starting_credits: 100000,
        starting_materials: { "mat_titanium": 40, "mat_tungsten": 25, "mat_tritium": 10 },
        starting_trait: "Artillery Spotter",
        trait_desc: "+10% Kinetic Cannon DMG, Tactical Orbital Shelling Call-in.",
        starting_mech_id: "bp_ms_ironclad_07",
        starter_mech_name: "GHA-07 Ironclad",
        starter_mech_type: "ironclad",
        starter_mech_sprite: spr_ms_custom_biped_heavy_idle,
        bio: "Decorated veteran of the Jovian border wars who resigned in protest against unprovoked mineral levies. Brings disciplined federal doctrine, kinetic mastery, and strong initial standing with Terran Command."
    },
    bg_colony_guerrilla: {
        id: "bg_colony_guerrilla",
        title: "Spacenoid Guerrilla Fighter",
        default_name: "Cmdr. Morgan Vance",
        default_callsign: "VALKYRIE",
        portrait_asset: spr_portrait_commander_female,
        faction_standings: { faction_b: 15, faction_a: -15, faction_c: 5 },
        starting_credits: 90000,
        starting_materials: { "mat_titanium": 30, "mat_tungsten": 15, "mat_tritium": 35 },
        starting_trait: "Vernier Ace",
        trait_desc: "+15% Evasion, +10% Beam Weapon DMG, Overboost agility surge.",
        starting_mech_id: "bp_ms_aerostriker",
        starter_mech_name: "Aero-Striker Mk-II",
        starter_mech_type: "aether",
        starter_mech_sprite: spr_ms_custom_aero_striker_idle,
        bio: "Former colonial orbital defense pilot who fought during the Lunar Blockade. Dedicated to spacenoid self-determination; master of zero-G vernier maneuvering and high-frequency beam weaponry."
    },
    bg_zaibatsu_defector: {
        id: "bg_zaibatsu_defector",
        title: "Zaibatsu Cybernetics Defector",
        default_name: "Cmdr. Renjiro Sato",
        default_callsign: "NULL-ZERO",
        portrait_asset: spr_portrait_null07,
        faction_standings: { faction_d: 10, faction_c: -10, faction_a: 0 },
        starting_credits: 150000,
        starting_materials: { "mat_titanium": 25, "mat_tungsten": 20, "mat_tritium": 20 },
        starting_trait: "Neural Synchronizer",
        trait_desc: "+15% Critical Hit Chance, ECM Jammer Pulse, +50,000 Bonus Credits.",
        starting_mech_id: "bp_ms_hoversniper",
        starter_mech_name: "HS-04 Hover-Sniper",
        starter_mech_type: "muramasa",
        starter_mech_sprite: spr_ms_custom_hover_sniper_idle,
        bio: "Former chief prototype test pilot for Apex Bio-Cybernetics who fled with classified neural interface telemetry. Possesses lethal precision targeting, vast credit reserves, and advanced electronic warfare tools."
    },
    bg_scavenger_veteran: {
        id: "bg_scavenger_veteran",
        title: "Scavenger Asteroid Veteran",
        default_name: "Cmdr. 'Rusty' Briggs",
        default_callsign: "RUST-HOUND",
        portrait_asset: spr_portrait_cruz,
        faction_standings: { faction_c: 15, faction_a: -10, faction_b: 0 },
        starting_credits: 80000,
        starting_materials: { "mat_titanium": 60, "mat_tungsten": 45, "mat_tritium": 10 },
        starting_trait: "Scrap Harvester",
        trait_desc: "+25% Battlefield Alloy Salvage Yield, +15% Mech Armor Durability.",
        starting_mech_id: "bp_ms_artillery",
        starter_mech_name: "Tread-Artillery Brawler",
        starter_mech_type: "hyena",
        starter_mech_sprite: spr_ms_custom_tread_artillery_idle,
        bio: "Survived a decade in the lawless asteroid belt scrapyards assembling deadly franken-mechs from military battle wreckage. Boasts unmatched salvage recycling efficiency and indestructible armor hulls."
    }
};

player_commander = {
    id: "player_commander_01",
    background_id: "bg_terran_officer",
    background_title: "Ex-Terran Coalition Officer",
    callsign: "VANGUARD",
    name: "Cmdr. Alexei Kane",
    portrait_asset: spr_portrait_commander_male,
    rank: "Commander",
    pmc_name: "Iron Ridge Dynamics",
    flagship_name: "Pre-War Dreadnought Hephaestus",
    trait: "Artillery Spotter",
    trait_desc: "+10% Kinetic Cannon DMG, Tactical Orbital Shelling Call-in.",
    starter_mech_name: "GHA-07 Ironclad",
    starter_mech_type: "ironclad",
    starter_mech_sprite: spr_ms_custom_biped_heavy_idle,
    background: "Decorated veteran of the Jovian border wars who resigned in protest against unprovoked mineral levies.",
    leadership: 9,
    tactics: 9,
    morale: 100
};

apply_commander_background = function(_bg_id, _custom_name, _custom_callsign, _custom_portrait) {
    if (!variable_struct_exists(commander_backgrounds, _bg_id)) _bg_id = "bg_terran_officer";
    var _bg = variable_struct_get(commander_backgrounds, _bg_id);
    
    player_commander.background_id = _bg_id;
    player_commander.background_title = _bg.title;
    player_commander.name = (_custom_name != "") ? _custom_name : _bg.default_name;
    player_commander.callsign = (_custom_callsign != "") ? _custom_callsign : _bg.default_callsign;
    player_commander.portrait_asset = (_custom_portrait != -1 && sprite_exists(_custom_portrait)) ? _custom_portrait : _bg.portrait_asset;
    player_commander.trait = _bg.starting_trait;
    player_commander.trait_desc = _bg.trait_desc;
    player_commander.background = _bg.bio;
    player_commander.starter_mech_name = _bg.starter_mech_name;
    player_commander.starter_mech_type = _bg.starter_mech_type;
    player_commander.starter_mech_sprite = _bg.starter_mech_sprite;
    
    // Set funds & starting raw materials
    funds = _bg.starting_credits;
    if (variable_struct_exists(_bg, "starting_materials") && variable_instance_exists(id, "inventory") && variable_struct_exists(inventory, "raw_materials")) {
        var _mkeys = variable_struct_get_names(_bg.starting_materials);
        for (var m = 0; m < array_length(_mkeys); m++) {
            var _mk = _mkeys[m];
            var _amt = variable_struct_get(_bg.starting_materials, _mk);
            variable_struct_set(inventory.raw_materials, _mk, _amt);
        }
    }
    
    // Apply initial Faction Standing Modifiers
    if (instance_exists(obj_FactionManager) && variable_struct_exists(_bg, "faction_standings")) {
        var _fkeys = variable_struct_get_names(_bg.faction_standings);
        for (var f = 0; f < array_length(_fkeys); f++) {
            var _fid = _fkeys[f];
            var _mod = variable_struct_get(_bg.faction_standings, _fid);
            obj_FactionManager.modify_standing(_fid, _mod);
        }
    }
    
    has_completed_dossier = true;
    has_completed_intro = false;
    prologue_active = true;
    advance_tutorial_step();
    
    // Configure Prologue Combat Context
    active_combat_context = {
        is_prologue: true,
        sector_id: "prologue_ambush",
        sector_name: "Cascadia Outpost SEC-00",
        region: "EARTH",
        subregion: "Emergency Relay Bunker",
        controlling_faction: "faction_c",
        defense_rating: 25,
        garrison_unit: "Unmarked Syndicate Raiders",
        is_invasion: false,
        origin_base_id: "earth_cascadia_driver",
        commander_mech_type: _bg.starter_mech_type,
        commander_mech_name: _bg.starter_mech_name,
        commander_mech_sprite: _bg.starter_mech_sprite
    };
};

apply_salvager_origin = function(_past_idx, _rig_idx, _code_idx, _beacon_idx, _portrait_asset, _callsign) {
    var _past_titles = [
        "Void Scrapper // Ex-Terran Mutineer",
        "Void Scrapper // Escaped Jovian Miner",
        "Void Scrapper // Cybernetics Fugitive",
        "Void Scrapper // Born to the Rust"
    ];
    
    // Core Pilot Attributes calculation
    var _gun = 40;
    var _eva = 40;
    var _mel = 40;
    var _eng = 40;
    
    // Past modifier
    if (_past_idx == 0) { _gun += 15; _eva -= 5; }
    else if (_past_idx == 1) { _eva += 15; _eng += 5; }
    else if (_past_idx == 2) { _gun += 10; _eng += 10; }
    else { _mel += 10; _eng += 15; }
    
    // Rig Specialization modifier
    if (_rig_idx == 0) { _gun += 10; _mel += 10; }
    else if (_rig_idx == 1) { _eva += 15; _gun += 5; }
    else if (_rig_idx == 2) { _gun += 20; _mel -= 5; }
    else { _mel += 15; _eng += 10; }
    
    // Signature Perks from Combat Instinct
    var _perk_ids = ["perk_point_blank", "perk_chaff_decoy", "perk_smuggler", "perk_scrappers_eye"];
    var _perk_names = ["Point-Blank Specialist", "Chaff Decoy", "Smuggler Contacts", "Scrapper's Eye"];
    var _perk_descs = [
        "+20% Close-Range Kinetic DMG and instant Melee Counter-Attack opportunity.",
        "+25% Evasion vs guided missiles and +1 free thruster dash AP per round.",
        "+15% Sell Value on salvaged components, Black Market trade unlocked, +15,000 Cr upfront.",
        "+25% Battlefield Salvage and raw ore recovery from wrecks, -20% Repair costs."
    ];
    
    player_commander.background_id = "salvager_custom";
    player_commander.background_title = _past_titles[_past_idx];
    player_commander.name = (_callsign != "") ? ("Scrapper " + _callsign) : "Scrapper Vance";
    player_commander.callsign = (_callsign != "") ? _callsign : "RUST-1";
    player_commander.portrait_asset = (_portrait_asset != -1 && sprite_exists(_portrait_asset)) ? _portrait_asset : spr_portrait_commander_male;
    
    // Assign stats & signature perk
    player_commander.stats = {
        gunnery: _gun,
        evasion: _eva,
        melee: _mel,
        engineering: _eng
    };
    player_commander.perk_id = _perk_ids[_code_idx];
    player_commander.perk_name = _perk_names[_code_idx];
    player_commander.perk_desc = _perk_descs[_code_idx];
    player_commander.trait = _perk_names[_code_idx];
    player_commander.trait_desc = _perk_descs[_code_idx];
    
    // The Historic Genesis Prototype (Fixed Frame)
    player_commander.starter_mech_name = "GHA-00 Genesis Prototype";
    player_commander.starter_mech_type = "ironclad";
    player_commander.starter_mech_sprite = spr_ms_custom_biped_heavy_idle;
    player_commander.background = "Operating from a battered salvage tug on the fringes of the Cascadia asteroid graveyard. Survived on stripped hulls and rusted components before intercepting the dying distress beacon of the USN-X Hephaestus.";
    
    // Starting funds & raw materials
    funds = (_code_idx == 2) ? 65000 : 50000;
    if (_beacon_idx == 2) funds += 15000;
    
    if (variable_instance_exists(id, "inventory") && variable_struct_exists(inventory, "raw_materials")) {
        inventory.raw_materials.mat_tungsten = (_past_idx == 0 || _beacon_idx == 0) ? 25 : 15;
        inventory.raw_materials.mat_titanium = (_past_idx == 3 || _beacon_idx == 1) ? 30 : 15;
        inventory.raw_materials.mat_syn_flux = (_past_idx == 2) ? 12 : 5;
    }
    
    // Faction Standing biases
    if (instance_exists(obj_FactionManager)) {
        if (_past_idx == 0) { obj_FactionManager.modify_standing("faction_a", -10); obj_FactionManager.modify_standing("faction_b", 10); }
        else if (_past_idx == 1) { obj_FactionManager.modify_standing("faction_b", 15); obj_FactionManager.modify_standing("faction_a", -10); }
        else if (_past_idx == 2) { obj_FactionManager.modify_standing("faction_d", -15); obj_FactionManager.modify_standing("faction_c", 10); }
        else { obj_FactionManager.modify_standing("faction_c", 15); }
    }
    
    has_completed_dossier = true;
    has_completed_intro = false;
    prologue_active = true;
    advance_tutorial_step();
    
    active_combat_context = {
        is_prologue: true,
        sector_id: "prologue_ambush",
        sector_name: "Derelict Dreadnought Hangar Threshold",
        region: "EARTH",
        subregion: "Lagrange Point 5 Graveyard",
        controlling_faction: "faction_c",
        defense_rating: 25,
        garrison_unit: "Corsair Raider Squadron",
        is_invasion: false,
        origin_base_id: "earth_cascadia_driver",
        commander_mech_type: "ironclad",
        commander_mech_name: "GHA-00 Genesis Prototype",
        commander_mech_sprite: spr_ms_custom_biped_heavy_idle
    };
};

select_commander = function(_gender_type) {
    if (_gender_type == "female") apply_commander_background("bg_colony_guerrilla", "", "", spr_portrait_commander_female);
    else if (_gender_type == "silhouette") apply_commander_background("bg_zaibatsu_defector", "", "", spr_portrait_commander_silhouette);
    else apply_commander_background("bg_terran_officer", "", "", spr_portrait_commander_male);
};

has_completed_intro = false;

// 3e. Operation Groundwork: 5-Step PMC Onboarding Tutorial Cadre (Doc 50)
has_completed_tutorial = false;
tutorial_step = 0; // 0: Briefing/Dossier, 1: Crucible Sintering, 2: Assembly Bay, 3: War Room Logistics, 4: Tactical Combat Sortie, 5: Commission Confirmed
tutorial_active = true;

advance_tutorial_step = function() {
    tutorial_step += 1;
    if (tutorial_step >= 5) {
        has_completed_tutorial = true;
        tutorial_active = false;
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("★ CADRE COMMISSION CONFIRMED! ALL COMMAND DECKS UNLOCKED ★", make_color_rgb(60, 240, 140));
        }
        scr_audio_play_ui("confirm");
    } else {
        scr_audio_play_ui("confirm");
    }
};

skip_tutorial = function() {
    tutorial_step = 5;
    has_completed_intro = true;
    has_completed_tutorial = true;
    tutorial_active = false;
    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("TUTORIAL CADRE BYPASSED // FULL SANDBOX ACTIVE", c_orange);
    }
    scr_audio_play_ui("cancel");
};

// 4c. Procedural Competitor R&D Catalog & Lineages (docs/27)
competitor_catalog = {};

init_competitor_catalog = function() {
    competitor_catalog = {
        corp_vhi: {
            id: "corp_vhi",
            name: "Valkyrie Heavy Industries",
            ticker: "VHI",
            branch: choose("BRANCH_A", "BRANCH_B"),
            branch_name: "",
            doctrine: "",
            suits_by_era: {},
            active_line_chassis: undefined,
            has_rare_x_spec: (random(100) < 35.0),
            rare_x_chassis: undefined
        },
        corp_aod: {
            id: "corp_aod",
            name: "Astraea Orbital Dynamics",
            ticker: "AOD",
            branch: choose("BRANCH_A", "BRANCH_B"),
            branch_name: "",
            doctrine: "",
            suits_by_era: {},
            active_line_chassis: undefined,
            has_rare_x_spec: (random(100) < 35.0),
            rare_x_chassis: undefined
        },
        corp_rust: {
            id: "corp_rust",
            name: "Rustworks Salvage Cartel",
            ticker: "RUST",
            branch: choose("BRANCH_A", "BRANCH_B"),
            branch_name: "",
            doctrine: "",
            suits_by_era: {},
            active_line_chassis: undefined,
            has_rare_x_spec: (random(100) < 35.0),
            rare_x_chassis: undefined
        },
        corp_hats: {
            id: "corp_hats",
            name: "Hyperion Advanced Tactical Systems",
            ticker: "HATS",
            branch: choose("BRANCH_A", "BRANCH_B"),
            branch_name: "",
            doctrine: "",
            suits_by_era: {},
            active_line_chassis: undefined,
            has_rare_x_spec: (random(100) < 35.0),
            rare_x_chassis: undefined
        }
    };

    // Populate Valkyrie R&D Branch
    var _vhi = competitor_catalog.corp_vhi;
    if (_vhi.branch == "BRANCH_A") {
        _vhi.branch_name = "Tungsten Citadel Doctrine";
        _vhi.doctrine = "Impenetrable frontal kinetic armor & stationary siege artillery";
        _vhi.suits_by_era = {
            era_1: { id: "TCM-03", name: "TCM-03 Bulwark", armor: 1620, power: 8, speed: 38, combat: 380, class: "Line Defense", primary_weapon: "90mm Rifled Cannon" },
            era_2: { id: "GHA-07", name: "GHA-07 Ironclad", armor: 2480, power: 12, speed: 45, combat: 480, class: "Assault Wall", primary_weapon: "Type-77 120mm Autocannon" },
            era_3: { id: "GHA-08", name: "GHA-08 Ironclad Bastion", armor: 3200, power: 15, speed: 40, combat: 590, class: "Heavy Bastion", primary_weapon: "Twin 150mm Siege Howitzer" },
            era_4: { id: "TCX-11", name: "TCX-11 Behemoth Mk.IV", armor: 4800, power: 22, speed: 35, combat: 720, class: "Heavy Dreadnought", primary_weapon: "Dual 400mm Hyper-Rail Batteries" }
        };
        _vhi.rare_x_chassis = { id: "VHI-X01", name: "VHI-X01 'Goliath Prime'", armor: 5400, power: 24, speed: 32, combat: 810, class: "Prototype Juggernaut", primary_weapon: "Supercritical Kinetic Ram" };
    } else {
        _vhi.branch_name = "Mobile Blitzkrieg Doctrine";
        _vhi.doctrine = "Tracked trench stormers & continuous feed rotary cannons";
        _vhi.suits_by_era = {
            era_1: { id: "VHI-01", name: "VHI Centurion Scout", armor: 1450, power: 9, speed: 55, combat: 390, class: "Light Blitz", primary_weapon: "40mm Twin Autocannon" },
            era_2: { id: "VHI-02", name: "VHI Centurion Assault", armor: 2200, power: 14, speed: 62, combat: 510, class: "Medium Striker", primary_weapon: "GAU-88 Rotary Heavy Vulcan" },
            era_3: { id: "VHI-03", name: "VHI Warhammer Breaker", armor: 2950, power: 18, speed: 58, combat: 620, class: "Heavy Stormer", primary_weapon: "Quad Rotary Shredder Cannon" },
            era_4: { id: "VHI-04", name: "VHI Titan Dreadnought", armor: 4300, power: 26, speed: 52, combat: 760, class: "Assault Dreadnought", primary_weapon: "Cyclic 200mm Autocannon Battery" }
        };
        _vhi.rare_x_chassis = { id: "VHI-X02", name: "VHI-X02 'Colossus Blitz'", armor: 4700, power: 28, speed: 60, combat: 830, class: "Prototype Breaker", primary_weapon: "Twin 50mm Continuous Chaingun" };
    }

    // Populate Astraea R&D Branch
    var _aod = competitor_catalog.corp_aod;
    if (_aod.branch == "BRANCH_A") {
        _aod.branch_name = "Coherent Energy Monopoly";
        _aod.doctrine = "Spinal particle beam accelerators & prism energy screen barriers";
        _aod.suits_by_era = {
            era_1: { id: "OCM-04", name: "OCM-04 Sylph", armor: 1180, power: 14, speed: 110, combat: 410, class: "Light Interceptor", primary_weapon: "Particle Carbine" },
            era_2: { id: "AET-01", name: "AET-01 Aether", armor: 1580, power: 16, speed: 120, combat: 510, class: "Energy Striker", primary_weapon: "Coherent Beam Pulse Rifle" },
            era_3: { id: "OCA-07", name: "OCA-07 Helios Arbalest", armor: 1850, power: 22, speed: 115, combat: 620, class: "Spinal Beam Sniper", primary_weapon: "Heavy Spinal Beam Accelerator" },
            era_4: { id: "OCX-15", name: "OCX-15 Seraphim Trans-Am", armor: 2900, power: 30, speed: 135, combat: 780, class: "Supercritical Dominator", primary_weapon: "Dual Hyper-Beam Cannons" }
        };
        _aod.rare_x_chassis = { id: "AOD-X01", name: "AOD-X01 'Solarion Phoenix'", armor: 3200, power: 34, speed: 140, combat: 850, class: "Prototype Dominator", primary_weapon: "Linear Vector Plasma Lance" };
    } else {
        _aod.branch_name = "Micro-G Vector Acrobatics";
        _aod.doctrine = "3D omni-directional vernier matrix & high-frequency plasma blades";
        _aod.suits_by_era = {
            era_1: { id: "AOD-01", name: "AOD Vector Dart", armor: 1050, power: 15, speed: 125, combat: 420, class: "Light Skirmisher", primary_weapon: "Twin Thermal Needles" },
            era_2: { id: "AOD-02", name: "AOD Mirage Skirmisher", armor: 1420, power: 18, speed: 135, combat: 530, class: "Vector Striker", primary_weapon: "High-Frequency Plasma Saber" },
            era_3: { id: "AOD-03", name: "AOD Valkyrie Wing", armor: 1750, power: 24, speed: 145, combat: 640, class: "Acrobatic Duelist", primary_weapon: "Twin Beam Naginata" },
            era_4: { id: "AOD-04", name: "AOD Chronos Interceptor", armor: 2600, power: 32, speed: 160, combat: 800, class: "Omni-Vector Ace", primary_weapon: "Relativistic Phase Blades" }
        };
        _aod.rare_x_chassis = { id: "AOD-X02", name: "AOD-X02 'Astraea Seraph'", armor: 2800, power: 36, speed: 175, combat: 880, class: "Prototype Interceptor", primary_weapon: "Chrono-Phase Beam Claws" };
    }

    // Populate Rustworks R&D Branch
    var _rust = competitor_catalog.corp_rust;
    if (_rust.branch == "BRANCH_A") {
        _rust.branch_name = "Molten Scrap Demolition";
        _rust.doctrine = "Converted ore refinery slag mortars & incendiary cluster bombs";
        _rust.suits_by_era = {
            era_1: { id: "SCR-05", name: "SCR-05 Marauder", armor: 1350, power: 8, speed: 65, combat: 360, class: "Pirate Raider", primary_weapon: "90mm Shrapnel Gun" },
            era_2: { id: "SCR-12", name: "SCR-12 Hyena", armor: 1720, power: 10, speed: 75, combat: 440, class: "Scav Raider", primary_weapon: "Flak Scattergun" },
            era_3: { id: "SCA-14", name: "SCA-14 Slag-Lobber", armor: 2250, power: 14, speed: 70, combat: 540, class: "Scrap Mortar", primary_weapon: "Molten Slag Catapult" },
            era_4: { id: "SCX-19", name: "SCX-19 Chimera Apex", armor: 3800, power: 20, speed: 78, combat: 710, class: "Hybrid Behemoth", primary_weapon: "Stolen Siege Railcannon" }
        };
        _rust.rare_x_chassis = { id: "RST-X01", name: "RST-X01 'Slag Titan'", armor: 4400, power: 22, speed: 65, combat: 790, class: "Prototype Demolisher", primary_weapon: "Thermal Slag Geyser" };
    } else {
        _rust.branch_name = "Overclocked Pirate Brawlers";
        _rust.doctrine = "Overpowered diesel-fusion cores & hydraulic wrecking cleavers";
        _rust.suits_by_era = {
            era_1: { id: "RST-01", name: "SCR Junk Ripper", armor: 1200, power: 10, speed: 80, combat: 370, class: "Light Brawler", primary_weapon: "Serrated Scrap Saw" },
            era_2: { id: "RST-02", name: "SCR Reaver Raider", armor: 1650, power: 13, speed: 90, combat: 470, class: "Medium Charger", primary_weapon: "Hydraulic Breaching Ram" },
            era_3: { id: "RST-03", name: "RST Blood Hound", armor: 2100, power: 18, speed: 95, combat: 580, class: "Heavy Berserker", primary_weapon: "Dual Crushing Shears" },
            era_4: { id: "RST-04", name: "RST Hellion Warlord", armor: 3400, power: 26, speed: 100, combat: 740, class: "Warlord Juggernaut", primary_weapon: "Spinal Kinetic Cleaver" }
        };
        _rust.rare_x_chassis = { id: "RST-X02", name: "RST-X02 'Junk Leviathan'", armor: 4100, power: 30, speed: 88, combat: 820, class: "Prototype Leviathan", primary_weapon: "Quad Wrecking Piles" };
    }

    // Populate Hyperion R&D Branch
    var _hats = competitor_catalog.corp_hats;
    if (_hats.branch == "BRANCH_A") {
        _hats.branch_name = "Cybernetic Neural-Drive";
        _hats.doctrine = "Transhuman brain-machine sync & predictive quantum combat AI";
        _hats.suits_by_era = {
            era_1: { id: "ZM-06", name: "ZM-06 Ronin", armor: 1250, power: 12, speed: 85, combat: 420, class: "Corporate Security", primary_weapon: "High-Frequency Vibro-Blade" },
            era_2: { id: "ZAI-03", name: "ZAI-03 Muramasa", armor: 1610, power: 18, speed: 95, combat: 560, class: "Cyber-Striker", primary_weapon: "Muramasa Plasma Katana" },
            era_3: { id: "ZMA-15", name: "ZMA-15 Raiden", armor: 1780, power: 24, speed: 100, combat: 670, class: "Precision Sniper", primary_weapon: "Hyper-Velocity Railgun" },
            era_4: { id: "ZX-22", name: "ZX-22 Susanoo Cyber-Drive", armor: 2750, power: 34, speed: 125, combat: 820, class: "Transhuman Godframe", primary_weapon: "Relativistic Tachyon Sabers" }
        };
        _hats.rare_x_chassis = { id: "HATS-X01", name: "HATS-X01 'Zero Muramasa'", armor: 3100, power: 38, speed: 135, combat: 910, class: "Prototype Cyber-Frame", primary_weapon: "Quantum Singularity Blade" };
    } else {
        _hats.branch_name = "Thermo-Optic Infiltration";
        _hats.doctrine = "Active light-bending camouflage & silent magnetic accelerators";
        _hats.suits_by_era = {
            era_1: { id: "HATS-01", name: "HATS Shadow Scout", armor: 1100, power: 13, speed: 95, combat: 430, class: "Stealth Scout", primary_weapon: "Suppressed Gauss Needle" },
            era_2: { id: "HATS-02", name: "HATS Specter Infiltrator", armor: 1520, power: 20, speed: 105, combat: 580, class: "Ghost Striker", primary_weapon: "Silent Mag-Sniper" },
            era_3: { id: "HATS-03", name: "HATS Phantom Recon", armor: 1720, power: 26, speed: 112, combat: 690, class: "EW Infiltrator", primary_weapon: "Disruptor Beam Pistol" },
            era_4: { id: "HATS-04", name: "HATS Shadow Raven", armor: 2550, power: 35, speed: 130, combat: 830, class: "Stealth Assassin", primary_weapon: "Phase-Cloaked Thermal Lance" }
        };
        _hats.rare_x_chassis = { id: "HATS-X02", name: "HATS-X02 'Eclipse Ghost'", armor: 2900, power: 40, speed: 145, combat: 920, class: "Prototype Infiltrator", primary_weapon: "Null-Trace Plasma Sniper" };
    }

    update_competitors_for_new_era();
};


// =============================================================================
// CONVENTIONAL VEHICLES REGISTRY & THE PROMETHEUS PROTOCOL (doc 38)
// =============================================================================
conventional_vehicles = [];
load_conventional_vehicles = function() {
    var _paths = ["datafiles/conventional_vehicles.json", "conventional_vehicles.json"];
    for (var p = 0; p < array_length(_paths); p++) {
        if (file_exists(_paths[p])) {
            try {
                var _buf = buffer_load(_paths[p]);
                var _str = buffer_read(_buf, buffer_string);
                buffer_delete(_buf);
                var _data = json_parse(_str);
                if (is_struct(_data) && variable_struct_exists(_data, "vehicles")) {
                    conventional_vehicles = _data.vehicles;
                    show_debug_message("[obj_GameManager] Loaded " + string(array_length(conventional_vehicles)) + " conventional vehicles from " + _paths[p]);
                    return;
                }
            } catch (_ex) {
                show_debug_message("[obj_GameManager] Error loading conventional vehicles: " + string(_ex));
            }
        }
    }
};
load_conventional_vehicles();

get_conventional_vehicle = function(_id) {
    for (var v = 0; v < array_length(conventional_vehicles); v++) {
        if (conventional_vehicles[v].id == _id) return conventional_vehicles[v];
    }
    return undefined;
};

trigger_mobile_suit_revolution = function(_mech_struct) {
    if (first_mobile_suit_deployed) return;
    first_mobile_suit_deployed = true;
    timeline_era = 1;
    timeline_era_name = "ERA I: THE FIRST MOVER CATALYST";
    reverse_engineering_unlocked = true;

    var _m_call = (is_struct(_mech_struct) && variable_struct_exists(_mech_struct, "callsign")) ? _mech_struct.callsign : "Alpha-01 'WARHAMMER'";

    array_push(last_turn_events, "! THE PROMETHEUS CATALYST: Mobile Suit (" + _m_call + ") publicly deployed in combat!");
    array_push(last_turn_events, "! DIPLOMATIC EMBARGO LIFTED: All Superpowers halt hostility to bid for player arms contracts!");
    array_push(last_turn_events, "! 365-DAY ARMS RACE TRIGGERED: Rival defense contractors scramble to reverse-engineer our frame!");

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("THE REVOLUTION: First Mobile Suit Deployed!", c_lime);
    }

    if (instance_exists(obj_FactionManager) && variable_instance_exists(obj_FactionManager, "on_mobile_suit_revolution")) {
        obj_FactionManager.on_mobile_suit_revolution();
    }
};

update_competitors_for_new_era = function() {
    var _era_key = "era_" + string(timeline_era);
    var _corps = ["corp_vhi", "corp_aod", "corp_rust", "corp_hats"];
    for (var c = 0; c < 4; c++) {
        var _cp = variable_struct_get(competitor_catalog, _corps[c]);
        if (variable_struct_exists(_cp.suits_by_era, _era_key)) {
            _cp.active_line_chassis = variable_struct_get(_cp.suits_by_era, _era_key);
            if (variable_struct_exists(rival_corporations, _corps[c])) {
                variable_struct_get(rival_corporations, _corps[c]).flagship_chassis = _cp.active_line_chassis.name;
            }
        } else {
            _cp.active_line_chassis = undefined;
            if (variable_struct_exists(rival_corporations, _corps[c])) {
                variable_struct_get(rival_corporations, _corps[c]).flagship_chassis = "None (Reverse-Engineering...)";
            }
        }
    }
};

evaluate_timeline_progression = function() {
    var _old_era = timeline_era;

    // In Era 0, timeline stays conventional until player deploys their Mobile Suit
    if (!first_mobile_suit_deployed) {
        timeline_era = 0;
        timeline_era_name = "ERA 0: CONVENTIONAL STEEL & JET FUEL";
        return;
    }

    // 365-Day Reverse-Engineering Tick across 4 Rival Megacorporations (~0.28% per turn)
    if (reverse_engineering_unlocked) {
        var _corps = ["corp_vhi", "corp_aod", "corp_rust", "corp_hats"];
        for (var c = 0; c < 4; c++) {
            var _cid = _corps[c];
            var _cur_prog = variable_struct_get(reverse_engineering_progress, _cid);
            if (_cur_prog < 100.0) {
                var _delta = 0.28 + random_range(-0.05, 0.08);
                _cur_prog = min(100.0, _cur_prog + _delta);
                variable_struct_set(reverse_engineering_progress, _cid, _cur_prog);
                if (_cur_prog >= 100.0 && variable_struct_exists(rival_corporations, _cid)) {
                    var _rc = variable_struct_get(rival_corporations, _cid);
                    array_push(last_turn_events, "! ARMS REPLICATION: " + _rc.name + " rolled out their first reverse-engineered Mobile Suit!");
                    if (instance_exists(obj_HQTerminal)) {
                        obj_HQTerminal.show_toast("COMPETITOR MS ROLLOUT: " + _rc.name + "!", c_red);
                    }
                }
            }
        }
    }

    if (current_turn >= 200 || current_cycle_year >= 220) {
        timeline_era = 4;
        timeline_era_name = "ERA IV: APEX CRISIS & ARCHEOTECH";
    } else if (current_turn >= 120 || current_cycle_year >= 217) {
        timeline_era = 3;
        timeline_era_name = "ERA III: TOTAL STRATEGIC WAR";
    } else if (current_turn >= 60 || current_cycle_year >= 215) {
        timeline_era = 2;
        timeline_era_name = "ERA II: INDUSTRIAL ESCALATION";
    } else {
        timeline_era = 1;
        timeline_era_name = "ERA I: THE FIRST MOVER CATALYST";
    }

    if (timeline_era != _old_era) {
        array_push(last_turn_events, "! TIMELINE TECH ADVANCEMENT: Sol System enters " + timeline_era_name + "!");
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("TECH ADVANCEMENT: " + timeline_era_name + "!", c_yellow);
        }
        update_competitors_for_new_era();
    }
};

evaluate_corporate_random_events = function() {
    if (!is_undefined(active_event_popup)) return false;
    if (array_length(narrative_events_list) == 0) return false;

    // 14% chance per turn to trigger an event
    if (random(100) < 14.0) {
        var _rand_idx = irandom(array_length(narrative_events_list) - 1);
        trigger_event_by_id(narrative_events_list[_rand_idx].id);
        return true;
    }
    return false;
};

// 4. PMC Company Profile
pmc_profile = {
    name: "Iron Ridge Tactical Operations",
    callsign: "IRON_RIDGE",
    license_tier: 2,
    tier_label: "Tier-2 Mercenary Guild Standard"
};

// 4b. Pre-War Experimental Flagship: USN-X Hephaestus (Doc 23)
// Scavenger origin: Discovered in Asteroid Belt debris; equipped with archeotech molecular fabrication bay.
flagship = {
    name: "USN-X Hephaestus",
    class: "Pre-War Foundry Dreadnought",
    origin_lore: "Unearthed from Scrapline debris; equipped with an ancient molecular nanite fabrication core.",
    current_sphere: "Earth Sphere",
    destination_sphere: "",
    transit_turns_left: 0,
    hull_hp: 8500,
    hull_max_hp: 8500,
    upgrades: {
        fabrication_tier: 1, // 1 to 5: 1-5 bays, print speed, +25% masterwork, +15% base armor/power
        mining_tier: 1,      // 1 to 5: local node yield (+25% to +250%), passive +15kg elements/turn at T5
        defense_tier: 1,     // 1 to 5: hull HP (8,500 to 40,000), pirate raid immunity at T4/T5
        weapons_tier: 1,     // 1 to 5: 600mm mass driver -> particle lance -> kinetic rods -> doomsday cleaver
        propulsion_tier: 1,  // 1 to 5: transit 3T -> 2T -> 1T -> 1T -> 0T Instant Tachyon Fold Warp
        pilot_suite_tier: 1, // 1 to 5: cryo-regen, +2 passive pilot combat stat/turn, Genkai +20%, trauma stabilization
        sigint_tier: 1,      // 1 to 5: raid alerts, 15% trade discount, sabotage immunity, passive market siphon
        command_tier: 1      // 1 to 5: +15% payouts, +1 combat deployment, +2 AP / +20% acc & armor in combat
    },
    specialization_protocol: "", // "", "forge_titan", "siege_fortress", "shadow_panopticon"
    orbital_strike_available: false,
    orbital_strike_cooldown: 0
};

// 4c. Rival Corporate Mobile Suit Manufacturers & Stock Exchange (docs/23, docs/28)
rival_corporations = {
    corp_vhi: {
        id: "corp_vhi",
        name: "Valkyrie Heavy Industries",
        ticker: "VHI",
        alignment: "The Terran Coalition",
        market_share_pct: 34,
        hostility_pct: 15,
        specialty: "Super-Heavy Armor & Ballistic Artillery",
        flagship_chassis: "GHA-07 Ironclad",
        ceo: "Baroness Victoria Sterling",
        hq_location: "Geneva Orbital Ring (Earth)",
        base_share_price: 120,
        share_price_cr: 120,
        total_shares: 100000,
        player_shares: 0,
        player_equity_pct: 0.0,
        dividend_per_turn: 0,
        is_acquired: false,
        controlling_interest: false
    },
    corp_aod: {
        id: "corp_aod",
        name: "Astraea Orbital Dynamics",
        ticker: "AOD",
        alignment: "The Outer Colonies",
        market_share_pct: 28,
        hostility_pct: 20,
        specialty: "Micro-Gravity Verniers & Beam Weaponry",
        flagship_chassis: "AET-01 Aether",
        ceo: "Dr. Sorel Vance",
        hq_location: "Galileo Aerospace Hub (Ganymede)",
        base_share_price: 135,
        share_price_cr: 135,
        total_shares: 100000,
        player_shares: 0,
        player_equity_pct: 0.0,
        dividend_per_turn: 0,
        is_acquired: false,
        controlling_interest: false
    },
    corp_rust: {
        id: "corp_rust",
        name: "Rustworks Salvage Cartel",
        ticker: "RUST",
        alignment: "Rogue Mercenary Syndicates",
        market_share_pct: 18,
        hostility_pct: 35,
        specialty: "Scavenged Junk Frames & Rotary Vulcans",
        flagship_chassis: "SCR-12 Hyena",
        ceo: "'Grease' Garvin",
        hq_location: "Asteroid 433 Eros / Rust-Pike",
        base_share_price: 45,
        share_price_cr: 45,
        total_shares: 100000,
        player_shares: 0,
        player_equity_pct: 0.0,
        dividend_per_turn: 0,
        is_acquired: false,
        controlling_interest: false
    },
    corp_hats: {
        id: "corp_hats",
        name: "Hyperion Advanced Tactical Systems",
        ticker: "HATS",
        alignment: "Apex Bio-Cybernetics Zaibatsu",
        market_share_pct: 20,
        hostility_pct: 25,
        specialty: "Neural Synapse Links & Predictive Combat AI",
        flagship_chassis: "ZAI-03 Muramasa",
        ceo: "Director Renzo Takahashi",
        hq_location: "Neo-Tokyo Orbital Silo (Mars)",
        base_share_price: 95,
        share_price_cr: 95,
        total_shares: 100000,
        player_shares: 0,
        player_equity_pct: 0.0,
        dividend_per_turn: 0,
        is_acquired: false,
        controlling_interest: false
    }
};
pmc_market_share_pct = 5;
sol_monopoly_achieved = false;

// Corporate Stock Exchange Trading Methods (docs/28)
calculate_rival_share_price = function(_corp_id) {
    if (!variable_struct_exists(rival_corporations, _corp_id)) return 0;
    var _rc = variable_struct_get(rival_corporations, _corp_id);
    if (_rc.is_acquired) {
        _rc.share_price_cr = 0;
        _rc.dividend_per_turn = 0;
        return 0;
    }
    var _era_mult = 1.0 + max(0, timeline_era - 1) * 0.35;
    var _share_mult = _rc.market_share_pct / 25.0;
    var _scandal_mult = (_rc.hostility_pct > 60) ? 0.75 : 1.0;
    _rc.share_price_cr = clamp(round(_rc.base_share_price * _share_mult * _era_mult * _scandal_mult), 15, 650);
    _rc.dividend_per_turn = floor(_rc.player_shares * (_rc.share_price_cr * 0.002));
    return _rc.share_price_cr;
};

buy_rival_shares = function(_corp_id, _shares_count) {
    if (!variable_struct_exists(rival_corporations, _corp_id)) return false;
    var _rc = variable_struct_get(rival_corporations, _corp_id);
    if (_rc.is_acquired) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("COMPANY ACQUIRED: Fully owned subsidiary!", c_yellow);
        return false;
    }
    calculate_rival_share_price(_corp_id);
    var _cost = floor(_shares_count * _rc.share_price_cr);
    if (funds < _cost) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT FUNDS! (Requires " + string(_cost) + " Cr)", c_red);
        return false;
    }
    if (_rc.player_shares + _shares_count > 100000) {
        _shares_count = 100000 - _rc.player_shares;
        _cost = floor(_shares_count * _rc.share_price_cr);
    }
    if (_shares_count <= 0) return false;

    funds -= _cost;
    _rc.player_shares += _shares_count;
    _rc.player_equity_pct = (_rc.player_shares / 100000.0) * 100.0;
    if (_rc.player_equity_pct >= 51.0) _rc.controlling_interest = true;
    _rc.dividend_per_turn = floor(_rc.player_shares * (_rc.share_price_cr * 0.002));

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("ACQUIRED " + string(_shares_count) + " SHARES OF " + _rc.ticker + " (" + string(_rc.player_equity_pct) + "% STAKE)!", c_lime);
    }
    if (_rc.player_shares >= 100000) {
        execute_hostile_takeover(_corp_id);
    }
    return true;
};

sell_rival_shares = function(_corp_id, _shares_count) {
    if (!variable_struct_exists(rival_corporations, _corp_id)) return false;
    var _rc = variable_struct_get(rival_corporations, _corp_id);
    if (_rc.is_acquired || _rc.player_shares <= 0) return false;
    var _to_sell = min(_shares_count, _rc.player_shares);
    calculate_rival_share_price(_corp_id);
    var _payout = floor(_to_sell * _rc.share_price_cr * 0.95); // 5% broker fee
    funds += _payout;
    _rc.player_shares -= _to_sell;
    _rc.player_equity_pct = (_rc.player_shares / 100000.0) * 100.0;
    if (_rc.player_equity_pct < 51.0) _rc.controlling_interest = false;
    _rc.dividend_per_turn = floor(_rc.player_shares * (_rc.share_price_cr * 0.002));

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("SOLD " + string(_to_sell) + " SHARES OF " + _rc.ticker + " (+" + string(_payout) + " Cr)!", c_yellow);
    }
    return true;
};

execute_hostile_takeover = function(_corp_id) {
    if (!variable_struct_exists(rival_corporations, _corp_id)) return false;
    var _rc = variable_struct_get(rival_corporations, _corp_id);
    if (_rc.is_acquired) return false;

    // Check if player has >= 51% stake or pays buyout tender offer
    calculate_rival_share_price(_corp_id);
    if (_rc.player_shares < 100000) {
        var _rem_shares = 100000 - _rc.player_shares;
        var _tender_cost = floor(_rem_shares * _rc.share_price_cr * 1.15); // 15% buyout premium
        if (_rc.player_equity_pct < 51.0 && funds < _tender_cost) {
            if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("BUYOUT DENIED: Need 51% controlling stake or " + string(_tender_cost) + " Cr!", c_red);
            return false;
        }
        if (funds >= _tender_cost) {
            funds -= _tender_cost;
            _rc.player_shares = 100000;
        } else {
            return false;
        }
    }

    _rc.player_shares = 100000;
    _rc.player_equity_pct = 100.0;
    _rc.is_acquired = true;
    _rc.controlling_interest = true;

    // 1. Absorb Sol Market Share
    pmc_market_share_pct = min(100, pmc_market_share_pct + _rc.market_share_pct);
    _rc.market_share_pct = 0;

    // 2. Absorb Manufacturing Assembly Line (+1 Bay)
    facilities.assembly_lines = min(4, facilities.assembly_lines + 1);

    // 3. Absorb Proprietary R&D Lineage & Prototype Blueprints
    if (variable_struct_exists(competitor_catalog, _corp_id)) {
        var _cat = variable_struct_get(competitor_catalog, _corp_id);
        _cat.is_eliminated = true;

        if (!is_undefined(_cat.active_line_chassis)) {
            var _suit = _cat.active_line_chassis;
            array_push(inventory.deployable_mechs, {
                id: "acquired_line_" + _suit.id + "_" + string(irandom(9999)),
                blueprint_id: _suit.id,
                callsign: _suit.name + " [ACQUIRED LINE]",
                name: _suit.name,
                class: _suit.class,
                assigned_pilot: "Unassigned",
                status: "READY",
                current_condition_pct: 1.0,
                armor_rating: _suit.armor,
                power_output: _suit.power,
                speed: _suit.speed,
                combat_rating: _suit.combat,
                spec_type: "CORPORATE_ACQUISITION",
                combat_pedigree: { sorties_deployed: 0, sorties_survived: 0, confirmed_kills: 0, ace_kills: 0, damage_mitigated: 0, pedigree_rating: "FACTORY_SPEC", telemetry_bonus: 5.0 }
            });
        }
        if (_cat.has_rare_x_spec && !is_undefined(_cat.rare_x_chassis)) {
            var _x_suit = _cat.rare_x_chassis;
            array_push(inventory.deployable_mechs, {
                id: "acquired_x_" + _x_suit.id + "_" + string(irandom(9999)),
                blueprint_id: _x_suit.id,
                callsign: _x_suit.name + " [PROTOTYPE ACQUIRED]",
                name: _x_suit.name,
                class: _x_suit.class,
                assigned_pilot: "Unassigned",
                status: "READY",
                current_condition_pct: 1.0,
                armor_rating: _x_suit.armor,
                power_output: _x_suit.power,
                speed: _x_suit.speed,
                combat_rating: _x_suit.combat,
                spec_type: "BLACK_OPS_PROTOTYPE",
                combat_pedigree: { sorties_deployed: 0, sorties_survived: 0, confirmed_kills: 0, ace_kills: 0, damage_mitigated: 0, pedigree_rating: "PROTOTYPE_MASTER", telemetry_bonus: 10.0 }
            });
        }
    }

    // Check Sol Industrial Monopoly Condition
    var _all_acquired = true;
    var _keys = ["corp_vhi", "corp_aod", "corp_rust", "corp_hats"];
    for (var k = 0; k < 4; k++) {
        if (!variable_struct_get(rival_corporations, _keys[k]).is_acquired) {
            _all_acquired = false;
            break;
        }
    }
    if (_all_acquired) {
        sol_monopoly_achieved = true;
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("TRIUMPH: SOL INDUSTRIAL MONOPOLY ACHIEVED!", c_yellow);
    }

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("HOSTILE TAKEOVER COMPLETE: " + _rc.name + " ACQUIRED!", c_lime);
    }
    return true;
};

// 5. Active Inventory Struct (docs/02, 06, 07)
inventory = {
    raw_materials: {
        mat_tungsten: 25,       // Raw Tungsten (400 Cr/u)
        mat_silica_carb: 40,    // Silica-Carbon (150 Cr/u)
        mat_syn_flux: 12,       // Synthetic Flux (800 Cr/u)
        mat_tritium: 8,         // Plasma-Charged Tritium (1,200 Cr/u)
        item_slag: 0            // Synthesis byproduct / scrap
    },
    alloys: {
        alloy_vanguard_comp: 12,      // Vanguard Composite Armor Plating
        alloy_hyperion_matrix: 6,     // Hyperion Superconductor Matrix
        alloy_aerosteel_flux: 8,      // Aerosteel Vernier Alloy
        alloy_adamantine_carbide: 6,  // Adamantine Heavy Carbide
        alloy_reactive_damascus: 4,   // Reactive Damascus Composite (Tier 5 Masterwork)
        alloy_tachyon_superalloy: 2,  // Tachyon Superalloy Superconductor (Tier 5 Masterwork)
        alloy_lunar_aerogel: 4,       // Lunar Aerogel Ultralight Composite (Tier 4 Advanced)
        alloy_sol_ferrite: 4,         // Sol Ferrite High-Permeability Alloy (Tier 5 Masterwork)
        alloy_chobham_reactive: 4,    // Chobham-X Reactive Composite (Tier 5 Masterwork)
        structural_alloys: 850,
        avionics_components: 240,
        rare_composites: 95
    },
    parts: {
        heads: [
            { id: "hd_vanguard_01", name: "HD-01 Vanguard Target-Lock", slot: "heads", armor: 120, mass: 4, power_draw: 2, bonus: "+15% Accuracy" },
            { id: "hd_aether_02", name: "HD-02 Aether EW-Dome", slot: "heads", armor: 90, mass: 2, power_draw: 4, bonus: "+18% Evasion" }
        ],
        torsos: [
            { id: "tr_colossus_01", name: "TR-01 Colossus Heavy Torso", slot: "torsos", armor: 480, mass: 26, power_output: 28, bonus: "Heavy Reactor Core" },
            { id: "tr_hyperion_02", name: "TR-02 Hyperion Tokamak Torso", slot: "torsos", armor: 360, mass: 20, power_output: 42, bonus: "High-Spec Fusion Core" }
        ],
        arms: [
            { id: "am_colossus_01", name: "AM-01 Colossus Dual Arms", slot: "arms", armor: 260, mass: 16, power_draw: 4, bonus: "+25% Recoil Control" },
            { id: "am_vernier_02", name: "AM-02 Vernier Fast-Actuators", slot: "arms", armor: 190, mass: 10, power_draw: 5, bonus: "+20% Handling" }
        ],
        legs: [
            { id: "lg_vanguard_01", name: "LG-01 Vanguard Heavy Walkers", slot: "legs", armor: 340, mass: 24, power_draw: 5, base_speed: 44, bonus: "+30% Stability" },
            { id: "lg_stratos_02", name: "LG-02 Stratos Vernier Skaters", slot: "legs", armor: 220, mass: 15, power_draw: 7, base_speed: 86, bonus: "+25% Agility" }
        ],
        backpacks: [
            { id: "bp_heavy_01", name: "BP-01 Heavy Booster Pack", slot: "backpacks", armor: 140, mass: 12, power_draw: 3, boost_bonus: 35, bonus: "High Thrust" },
            { id: "bp_vernier_02", name: "BP-02 Dual-Vector Vernier Rig", slot: "backpacks", armor: 100, mass: 8, power_draw: 6, boost_bonus: 65, bonus: "+15% Evade" }
        ],
        weapons: [
            { id: "wp_vulcan_01", name: "WP-01 Rotary Vulcan (120mm)", slot: "weapons", armor: 100, mass: 12, power_draw: 3, damage: 180, bonus: "Sustained Fire" },
            { id: "wp_beam_02", name: "WP-02 Particle Beam Pulse Rifle", slot: "weapons", armor: 80, mass: 8, power_draw: 10, damage: 240, bonus: "Armor Piercing" }
        ]
    },
    components: [],        // Spare weapons & masterworks
    deployable_mechs: [
        {
            id: "unit_ironclad_01",
            blueprint_id: "bp_ms_ironclad_07",
            callsign: "IRON-01 'WARHAMMER'",
            name: "GHA-07 Ironclad",
            class: "Heavy Assault",
            assigned_pilot: "Lt. Marcus Vance",
            status: "DEPLOYED_MINING", // Locked at Asteroid Belt
            current_condition_pct: 1.0,
            armor_rating: 850,
            power_output: 12,
            speed: 45,
            combat_rating: 480,
            spec_type: "COMMANDER_CUSTOM",
            combat_pedigree: {
                sorties_deployed: 2,
                sorties_survived: 2,
                confirmed_kills: 4,
                ace_kills: 1,
                damage_mitigated: 980,
                pedigree_rating: "COMBAT_PROVEN",
                telemetry_bonus: 8.0
            }
        },
    ]
};

// 6. Base Facility Upgrades & Roster (docs/07_base_management.md)
facilities = {
    crucible_tier: 1,             // Tier 1: Max 3000°C, 2000 PSI; Tier 2: Max 6000°C, 10,000 PSI
    containment_shielding: false, // Prevents catastrophic lab damage on breach
    assembly_lines: 1,            // Number of concurrent manufacturing bays (up to 4)
    hangar_bays: 1,               // Hangar capacity bays for mobile suits
    lab_tier: 1,                  // R&D metallurgy and sensor laboratory tier
    foundry_crucibles: 1,         // Sintering crucible foundry count
    active_fabrications: [
        {
            mech_blueprint: "bp_ms_ironclad_07",
            name: "GHA-07 Ironclad Batch-3",
            days_remaining: 6,
            total_days: 12
        }
    ],
    roster_pilots: [
        { id: "pilot_terran_vance_starter", character_id: "pilot_terran_vance_starter", name: "Lt. Marcus Vance", callsign: "VANGUARD-1", level: 1, unspent_stat_points: 0, combat_stat: 9, tactics_stat: 8, accuracy: 88, reflexes: 75, morale: 95, salary_daily: 220, is_deployed: true, status: "ACTIVE", recovery_days: 0, recovery_days_left: 0, kills: 3, sorties: 5, fatigue: 0, xp: 120, rank_perks: ["Quick Draw"], mutated_traits: [] },
        { id: "pilot_terran_cole", character_id: "pilot_terran_cole", name: "Sgt. Sarah Cole", callsign: "DEATHBLOW", level: 1, unspent_stat_points: 0, combat_stat: 8, tactics_stat: 7, accuracy: 82, reflexes: 79, morale: 88, salary_daily: 190, is_deployed: false, status: "ACTIVE", recovery_days: 0, recovery_days_left: 0, kills: 1, sorties: 2, fatigue: 0, xp: 45, rank_perks: [], mutated_traits: [] }
    ],
    pmc_memorial_wall: [],
    roster_engineers: [
        { name: "Dr. Elena Rostova", role: "Lead Metallurgist", metallurgy: 82, precision: 78, salary_daily: 180 },
        { name: "Master Chief Travis", role: "Hydraulics Specialist", metallurgy: 70, precision: 86, salary_daily: 160 }
    ],
    available_hire_pilots: [
        { id: "plt_terran_cole", character_id: "pilot_terran_cole", name: "Lt. Marcus 'Breaker' Cole", callsign: "BREAKER", faction: "faction_terran", portrait: spr_portrait_cole, accuracy: 78, reflexes: 42, combat_stat: 8, tactics_stat: 4, morale: 70, salary_daily: 250, bonus_hire: 45000, signing_bonus: 45000, background: "Trench warfare veteran who refused to shell civilian domes.", traits: "Heavy Ordnance (+20% Kinetic DMG)", bio: "Trench warfare veteran who refused to shell civilian domes." },
        { id: "plt_terran_02", character_id: "pilot_terran_rostova", name: "Ensign Elena Rostova", callsign: "DEAD-EYE", faction: "faction_terran", portrait: spr_portrait_vance, accuracy: 92, reflexes: 55, combat_stat: 9, tactics_stat: 6, morale: 80, salary_daily: 220, bonus_hire: 38000, signing_bonus: 38000, background: "Elite sniper with cybernetic targeting implants.", traits: "Retinal Implants (+15% Critical Chance)", bio: "Elite sniper with cybernetic targeting implants." },
        { id: "plt_colony_01", character_id: "pilot_colony_sorren", name: "Sorren 'Ghost' Lin", callsign: "GHOST", faction: "faction_colony", portrait: spr_portrait_sorren, accuracy: 85, reflexes: 92, combat_stat: 9, tactics_stat: 9, morale: 85, salary_daily: 280, bonus_hire: 52000, signing_bonus: 52000, background: "Quiet Jovian interceptor ace obsessed with zero-G speed.", traits: "Vernier Ace (+25% Evasion)", bio: "Quiet Jovian interceptor ace obsessed with zero-G speed." },
        { id: "plt_colony_02", character_id: "pilot_colony_kira", name: "Kira Dahl", callsign: "SPECTER", faction: "faction_colony", portrait: spr_portrait_sorren, accuracy: 70, reflexes: 80, combat_stat: 7, tactics_stat: 8, morale: 90, salary_daily: 190, bonus_hire: 34000, signing_bonus: 34000, background: "Electronic warfare specialist and sensor jammer prodigy.", traits: "ECM Pulse (-20% Enemy Hit)", bio: "Electronic warfare specialist and sensor jammer prodigy." },
        { id: "plt_syndicate_01", character_id: "pilot_syndicate_nadia", name: "Nadia 'Spark' Ortiz", callsign: "SPARK", faction: "faction_syndicate", portrait: spr_portrait_nadia, accuracy: 72, reflexes: 65, combat_stat: 7, tactics_stat: 7, morale: 95, salary_daily: 170, bonus_hire: 31000, signing_bonus: 31000, background: "Asteroid belt mechanic who can patch hulls under direct mortar fire.", traits: "Field Rig (+25% Scrap Salvage)", bio: "Asteroid belt mechanic who can patch hulls under direct mortar fire." },
        { id: "plt_syndicate_02", character_id: "pilot_syndicate_jackal", name: "'Jackal' Jax Vance", callsign: "JACKAL", faction: "faction_syndicate", portrait: spr_portrait_cruz, accuracy: 80, reflexes: 78, combat_stat: 8, tactics_stat: 8, morale: 65, salary_daily: 230, bonus_hire: 41000, signing_bonus: 41000, background: "Mercenary skirmisher fighting purely for cold credits.", traits: "Harpoon Tether (Pins Mechs)", bio: "Mercenary skirmisher fighting purely for cold credits." },
        { id: "plt_zaibatsu_01", character_id: "pilot_zaibatsu_null07", name: "Null-07 (Ren)", callsign: "NULL", faction: "faction_zaibatsu", portrait: spr_portrait_null07, accuracy: 96, reflexes: 88, combat_stat: 10, tactics_stat: 9, morale: 50, salary_daily: 320, bonus_hire: 65000, signing_bonus: 65000, background: "Escaped Zaibatsu test subject with spinal neural-jack implants.", traits: "Neural Link (+2 Action in 1st Turn)", bio: "Escaped Zaibatsu test subject with spinal neural-jack implants." },
        { id: "plt_zaibatsu_02", character_id: "pilot_zaibatsu_maya", name: "Maya 'Kestrel' Zhao", callsign: "KESTREL", faction: "faction_zaibatsu", portrait: spr_portrait_renzo, accuracy: 84, reflexes: 75, combat_stat: 8, tactics_stat: 8, morale: 85, salary_daily: 240, bonus_hire: 46000, signing_bonus: 46000, background: "Former corporate security ace who bought out her debt contract.", traits: "Sub-Drone Swarm Support", bio: "Former corporate security ace who bought out her debt contract." }
    ]
};

// Milestone 55: Squadron Perks & PMC Karma Alignment Engine
squadron_perks = [];
pmc_karma_noble = 50;
pmc_karma_pragmatist = 50;
pmc_karma_profiteer = 20;

get_pmc_karma_alignment = function() {
    if (pmc_karma_noble >= pmc_karma_pragmatist && pmc_karma_noble >= pmc_karma_profiteer) {
        return "NOBLE PEACEKEEPER";
    } else if (pmc_karma_pragmatist >= pmc_karma_noble && pmc_karma_pragmatist >= pmc_karma_profiteer) {
        return "CORPORATE PRAGMATIST";
    } else {
        return "BLOODHOUND WAR PROFITEER";
    }
};

// 7. Strategic Resource Nodes (docs/06_resource_operations.md)
nodes = [
    {
        id: "node_asteroid_c14",
        name: "Asteroid Belt C-14",
        primary_yield: "mat_tungsten",
        secondary_yield: "mat_silica_carb",
        yield_rate_primary: 4,
        yield_rate_secondary: 3,
        threat_level_pct: 20,
        current_storage: { mat_tungsten: 18, mat_silica_carb: 12 },
        assigned_mech_id: "unit_ironclad_01",
        assigned_pilot_name: "Lt. Marcus Vance",
        status: "ACTIVE_MINING"
    },
    {
        id: "node_moon_io4",
        name: "Volcanic Moon Io-IV",
        primary_yield: "mat_silica_carb",
        secondary_yield: "mat_tungsten",
        yield_rate_primary: 6,
        yield_rate_secondary: 2,
        threat_level_pct: 35,
        current_storage: { mat_silica_carb: 0, mat_tungsten: 0 },
        assigned_mech_id: "Unassigned",
        assigned_pilot_name: "Unassigned",
        status: "UNCLAIMED"
    },
    {
        id: "node_gas_giant",
        name: "Gas Giant Orbital Ring",
        primary_yield: "mat_tritium",
        secondary_yield: "none",
        yield_rate_primary: 3,
        yield_rate_secondary: 0,
        threat_level_pct: 50,
        current_storage: { mat_tritium: 0 },
        assigned_mech_id: "Unassigned",
        assigned_pilot_name: "Unassigned",
        status: "UNCLAIMED"
    },
    {
        id: "node_shipyard_omega",
        name: "Derelict Shipyard Omega",
        primary_yield: "mat_syn_flux",
        secondary_yield: "item_slag",
        yield_rate_primary: 3,
        yield_rate_secondary: 2,
        threat_level_pct: 65,
        current_storage: { mat_syn_flux: 0, item_slag: 0 },
        assigned_mech_id: "Unassigned",
        assigned_pilot_name: "Unassigned",
        status: "UNCLAIMED"
    }
];

// Active Raid Alert State
pending_raid = undefined;

// 8. Dynamic Narrative Events Engine (docs/08_narrative_events.md)
narrative_events_list = [];
active_event_popup = undefined;

load_narrative_events = function() {
    try {
        if (file_exists("narrative_events.json")) {
            var _buf_ne = buffer_load("narrative_events.json");
            var _str = buffer_read(_buf_ne, buffer_string);
            buffer_delete(_buf_ne);
            var _data = json_parse(_str);
            if (is_struct(_data) && is_array(variable_struct_get(_data, "events"))) {
                narrative_events_list = _data.events;
                show_debug_message("[obj_GameManager] Loaded " + string(array_length(narrative_events_list)) + " narrative events.");
            }
        }
    } catch (_ex) {
        show_debug_message("[obj_GameManager] Exception loading narrative events: " + string(_ex));
    }
};
load_narrative_events();
init_competitor_catalog();

// =============================================================================
// EXPANDED MOBILE SUIT UNIVERSE & CATALOG ENGINE (docs/29)
// =============================================================================
mobile_suit_catalog = {};

init_master_mobile_suit_catalog = function() {
    var _loaded = false;
    var _paths = ["mobile_suits/mobile_suit_catalog.json", "mobile_suit_catalog.json"];
    for (var p = 0; p < array_length(_paths); p++) {
        var _fp = _paths[p];
        if (file_exists(_fp)) {
            try {
                var _buf = buffer_load(_fp);
                var _str = buffer_read(_buf, buffer_string);
                buffer_delete(_buf);
                var _parsed = json_parse(_str);
                if (is_struct(_parsed)) {
                    mobile_suit_catalog = _parsed;
                    _loaded = true;
                    show_debug_message("[obj_GameManager] Successfully loaded " + string(variable_struct_names_count(mobile_suit_catalog)) + " mobile suits from " + _fp);
                    break;
                }
            } catch (_ex) {
                show_debug_message("[obj_GameManager] Error loading " + _fp + ": " + string(_ex));
            }
        }
    }

    if (!_loaded || variable_struct_names_count(mobile_suit_catalog) == 0) {
        show_debug_message("[obj_GameManager] Initializing catalog fallback memory.");
    }
};

get_mobile_suit = function(_id) {
    if (is_struct(mobile_suit_catalog) && variable_struct_exists(mobile_suit_catalog, _id)) {
        return variable_struct_get(mobile_suit_catalog, _id);
    }
    return undefined;
};

get_suits_by_faction = function(_faction_id) {
    var _res = [];
    if (!is_struct(mobile_suit_catalog)) return _res;
    var _names = variable_struct_get_names(mobile_suit_catalog);
    for (var i = 0; i < array_length(_names); i++) {
        var _suit = variable_struct_get(mobile_suit_catalog, _names[i]);
        if (is_struct(_suit) && variable_struct_get(_suit, "faction_id") == _faction_id) {
            array_push(_res, _suit);
        }
    }
    return _res;
};

get_mass_production_candidates = function(_faction_id) {
    var _res = [];
    if (!is_struct(mobile_suit_catalog)) return _res;
    var _names = variable_struct_get_names(mobile_suit_catalog);
    for (var i = 0; i < array_length(_names); i++) {
        var _suit = variable_struct_get(mobile_suit_catalog, _names[i]);
        if (is_struct(_suit) && variable_struct_get(_suit, "faction_id") == _faction_id && (variable_struct_get(_suit, "mass_production_line") ?? false)) {
            array_push(_res, _suit);
        }
    }
    return _res;
};

get_suits_by_era = function(_era) {
    var _res = [];
    if (!is_struct(mobile_suit_catalog)) return _res;
    var _names = variable_struct_get_names(mobile_suit_catalog);
    for (var i = 0; i < array_length(_names); i++) {
        var _suit = variable_struct_get(mobile_suit_catalog, _names[i]);
        if (is_struct(_suit) && variable_struct_get(_suit, "era") == _era) {
            array_push(_res, _suit);
        }
    }
    return _res;
};

init_master_mobile_suit_catalog();

trigger_event_by_id = function(_event_id) {
    for (var e = 0; e < array_length(narrative_events_list); e++) {
        if (variable_struct_get(narrative_events_list[e], "id") == _event_id) {
            active_event_popup = narrative_events_list[e];
            time_speed = 0; // Pause simulation for commander decision
            if (instance_exists(obj_HQTerminal)) {
                obj_HQTerminal.show_toast("INCOMING HIGH-PRIORITY TRANSMISSION!", c_yellow);
            }
            return true;
        }
    }
    return false;
};

// Narrative Story Episodes Seen State (Doc 51)
story_episodes_seen = {};

// 9. Daily Simulation Advancement Method (docs/01, 04, 06, 07)
end_turn = function() {
    // Check Campaign Story Milestone Episodes & Multi-Leader Summits (Doc 51 & Doc 52)
    if (current_turn == 5 && !variable_struct_exists(story_episodes_seen, "ep_02_shadows_over_mars")) {
        variable_struct_set(story_episodes_seen, "ep_02_shadows_over_mars", true);
        scr_vn_start_episode("ep_02_shadows_over_mars");
    } else if (current_turn == 7 && !variable_struct_exists(story_episodes_seen, "ep_summit_phobos_crisis")) {
        variable_struct_set(story_episodes_seen, "ep_summit_phobos_crisis", true);
        scr_vn_start_episode("ep_summit_phobos_crisis");
    } else if (current_turn == 12 && !variable_struct_exists(story_episodes_seen, "ep_summit_transhumanist_schism")) {
        variable_struct_set(story_episodes_seen, "ep_summit_transhumanist_schism", true);
        scr_vn_start_episode("ep_summit_transhumanist_schism");
    } else if (current_turn == 18 && !variable_struct_exists(story_episodes_seen, "ep_summit_sol_monopoly")) {
        variable_struct_set(story_episodes_seen, "ep_summit_sol_monopoly", true);
        scr_vn_start_episode("ep_summit_sol_monopoly");
    } else if (current_turn == 9 && !variable_struct_exists(story_episodes_seen, "ep_war_terran_vs_colony")) {
        variable_struct_set(story_episodes_seen, "ep_war_terran_vs_colony", true);
        scr_vn_start_episode("ep_war_terran_vs_colony");
    } else if (current_turn == 11 && !variable_struct_exists(story_episodes_seen, "ep_trade_rival_valkyrie_deal")) {
        variable_struct_set(story_episodes_seen, "ep_trade_rival_valkyrie_deal", true);
        scr_vn_start_episode("ep_trade_rival_valkyrie_deal");
    } else if (current_turn == 14 && !variable_struct_exists(story_episodes_seen, "ep_war_zaibatsu_vs_tharsis")) {
        variable_struct_set(story_episodes_seen, "ep_war_zaibatsu_vs_tharsis", true);
        scr_vn_start_episode("ep_war_zaibatsu_vs_tharsis");
    } else if (current_turn == 16 && !variable_struct_exists(story_episodes_seen, "ep_trade_rival_hyperion_arms")) {
        variable_struct_set(story_episodes_seen, "ep_trade_rival_hyperion_arms", true);
        scr_vn_start_episode("ep_trade_rival_hyperion_arms");
    } else if (current_turn == 19 && !variable_struct_exists(story_episodes_seen, "ep_war_syndicate_vs_sidereal")) {
        variable_struct_set(story_episodes_seen, "ep_war_syndicate_vs_sidereal", true);
        scr_vn_start_episode("ep_war_syndicate_vs_sidereal");
    } else if (current_turn == 22 && !variable_struct_exists(story_episodes_seen, "ep_ceasefire_terran_colony")) {
        variable_struct_set(story_episodes_seen, "ep_ceasefire_terran_colony", true);
        scr_vn_start_episode("ep_ceasefire_terran_colony");
    }
    current_turn++;
    current_cycle_day++;
    if (current_cycle_day > 365) {
        current_cycle_day = 1;
        current_cycle_year++;
    }

    last_turn_events = [];
    array_push(last_turn_events, "=== STRATEGIC TURN " + string(current_turn) + " REPORT // CYCLE Y" + string(current_cycle_year) + " D" + string(current_cycle_day) + " ===");

    // 1. Economic Flow: Retainers minus upkeep & payroll
    var _daily_retainer = 650;
    var _daily_salaries = 0;
    for (var p = 0; p < array_length(facilities.roster_pilots); p++) {
        _daily_salaries += facilities.roster_pilots[p].salary_daily;
    }
    for (var eg = 0; eg < array_length(facilities.roster_engineers); eg++) {
        _daily_salaries += facilities.roster_engineers[eg].salary_daily;
    }
    // Fleet Chassis Maintenance & Reactor Tritium Burn (Goal A)
    var _num_mechs = (variable_struct_exists(inventory, "deployable_mechs") && is_array(inventory.deployable_mechs)) ? array_length(inventory.deployable_mechs) : 0;
    total_fleet_upkeep_cr = _num_mechs * mech_upkeep_cr_per_unit;
    total_fleet_tritium_burn = (_num_mechs > 0) ? max(1, ceil(_num_mechs / mech_upkeep_tritium_ratio)) : 0;

    // Deduct Tritium fuel for Tokamak magnetic bottles
    if (variable_struct_exists(inventory.raw_materials, "mat_tritium")) {
        inventory.raw_materials.mat_tritium -= total_fleet_tritium_burn;
    }

    var _daily_maintenance = 150 + (facilities.assembly_lines - 1) * 75 + total_fleet_upkeep_cr;
    var _net_flow = _daily_retainer - _daily_salaries - _daily_maintenance;
    funds += _net_flow;
    array_push(last_turn_events, "* Fiscal Ledger: Net Cashflow " + (_net_flow >= 0 ? "+" : "") + string(_net_flow) + " Cr (Treasury: " + string(funds) + " Cr)");

    // 1b. Corporate Stock Exchange Dividends & Royalties (docs/28)
    var _total_dividends = 0;
    var _total_royalties = 0;
    var _corp_list = ["corp_vhi", "corp_aod", "corp_rust", "corp_hats"];
    for (var ci = 0; ci < 4; ci++) {
        var _c_id = _corp_list[ci];
        if (variable_struct_exists(rival_corporations, _c_id)) {
            var _rcp = variable_struct_get(rival_corporations, _c_id);
            if (!_rcp.is_acquired) {
                calculate_rival_share_price(_c_id);
                if (_rcp.player_shares > 0) {
                    var _div = floor(_rcp.player_shares * (_rcp.share_price_cr * 0.002));
                    _total_dividends += _div;
                    array_push(last_turn_events, "* Equity Dividend: " + _rcp.ticker + " (" + string(_rcp.player_equity_pct) + "%) paid +" + string(_div) + " Cr");
                }
                if (_rcp.player_equity_pct >= 51.0) {
                    var _royalty = floor(_rcp.market_share_pct * 850);
                    _total_royalties += _royalty;
                    array_push(last_turn_events, "* Majority Stake Royalty: Extracted +" + string(_royalty) + " Cr from " + _rcp.ticker + " operations");
                }
            }
        }
    }
    if (_total_dividends > 0 || _total_royalties > 0) {
        funds += (_total_dividends + _total_royalties);
    }

    // Check Supply Starvation & Fuel Reserves (Goal A)
    var _tritium_cur = variable_struct_exists(inventory.raw_materials, "mat_tritium") ? inventory.raw_materials.mat_tritium : 0;
    if (funds < 0 || _tritium_cur < 0) {
        supply_starvation = true;
        array_push(last_turn_events, "! LOGISTICS DEFICIT: Fleet is suffering from lack of maintenance/fuel! Combat readiness severely degraded (-2 AP, -25% Evasion).");
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("LOGISTICS CRISIS: SUPPLY STARVATION ACTIVE!", c_red);
        }
    } else {
        supply_starvation = false;
    }

    // Pilot Convalescence & Fatigue Recovery (Goal B)
    if (variable_struct_exists(facilities, "roster_pilots") && is_array(facilities.roster_pilots)) {
        var _heal_rate = 1;
        if (flagship.upgrades.pilot_suite_tier >= 2) _heal_rate = 2; // Accelerated hospital recovery

        for (var p = 0; p < array_length(facilities.roster_pilots); p++) {
            var _plt = facilities.roster_pilots[p];
            if (!variable_struct_exists(_plt, "fatigue")) _plt.fatigue = 0;
            if (!variable_struct_exists(_plt, "recovery_days_left")) _plt.recovery_days_left = 0;

            if (_plt.status == "HOSPITALIZED") {
                _plt.recovery_days_left = max(0, _plt.recovery_days_left - _heal_rate);
                if (_plt.recovery_days_left <= 0) {
                    _plt.status = "ACTIVE";
                    _plt.fatigue = 0;
                    array_push(last_turn_events, "* MEDICAL CLEARANCE: " + _plt.name + " (" + _plt.callsign + ") discharged from hospital and cleared for active duty!");
                    mutate_pilot_trait(p, "Cybernetic Reflex Augment");
                    if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("PILOT DISCHARGED: " + _plt.callsign + " is active!", c_lime);
                }
            } else if (_plt.status == "ACTIVE") {
                // Non-deployed resting pilots dissipate fatigue (-25 fatigue per cycle)
                _plt.fatigue = max(0, _plt.fatigue - 25);
            }
        }
    }

    // 2. Resource Mining Node Extractions (docs/06)
    for (var n = 0; n < array_length(nodes); n++) {
        var _node = nodes[n];
        if (_node.status == "ACTIVE_MINING") {
            // Flagship In-Sphere Refining Multiplier (Docs 23 & 24)
            var _sphere_mult = 1.0;
            if (variable_struct_exists(_node, "sphere") && _node.sphere == flagship.current_sphere) {
                var _m_tier = flagship.upgrades.mining_tier;
                var _tier_mults = [1.25, 1.50, 2.00, 2.50, 3.50];
                _sphere_mult = _tier_mults[clamp(_m_tier - 1, 0, 4)];
                if (flagship.specialization_protocol == "forge_titan") {
                    _sphere_mult *= 1.5;
                }
            }
            var _yield_p = max(1, floor(_node.yield_rate_primary * _sphere_mult));
            var _yield_s = max(1, floor(_node.yield_rate_secondary * _sphere_mult));

            if (_node.primary_yield != "none") {
                var _cy_p = (variable_struct_exists(_node.current_storage, _node.primary_yield) ? variable_struct_get(_node.current_storage, _node.primary_yield) : 0); variable_struct_set(_node.current_storage, _node.primary_yield, _cy_p + _yield_p);
            }
            if (_node.secondary_yield != "none") {
                var _cy_s = (variable_struct_exists(_node.current_storage, _node.secondary_yield) ? variable_struct_get(_node.current_storage, _node.secondary_yield) : 0); variable_struct_set(_node.current_storage, _node.secondary_yield, _cy_s + _yield_s);
            }
            var _b_tag = (_sphere_mult > 1.0) ? " [FLAGSHIP REFINED]" : "";
            array_push(last_turn_events, "* Mining Operation: " + _node.name + " mined +" + string(_yield_p) + " " + _node.primary_yield + _b_tag);

            // Ambient Threat Raid Roll
            var _raid_roll = random(100);
            if (_raid_roll < _node.threat_level_pct * 0.15) {
                pending_raid = {
                    node_index: n,
                    node_name: _node.name,
                    assigned_mech: _node.assigned_mech_id,
                    assigned_pilot: _node.assigned_pilot_name
                };
                array_push(last_turn_events, "! PIRATE SORTIE ALERT: " + _node.name + " is being raided!");
                if (instance_exists(obj_HQTerminal)) {
                    obj_HQTerminal.show_toast("ALERT: " + _node.name + " UNDER PIRATE ATTACK!", c_red);
                }
            }
        }
    }

    // 3. Advance Assembly Lines (docs/07)
    for (var i = array_length(facilities.active_fabrications) - 1; i >= 0; i--) {
        var _fab = facilities.active_fabrications[i];
        _fab.days_remaining--;
        if (_fab.days_remaining <= 0) {
            var _bp_data = undefined;
            if (instance_exists(obj_BlueprintManager)) {
                _bp_data = obj_BlueprintManager.get_blueprint(_fab.mech_blueprint);
            }
            var _mech_armor = (!is_undefined(_bp_data) && variable_struct_exists(_bp_data, "armor_rating")) ? _bp_data.armor_rating : 850;
            var _mech_power = (!is_undefined(_bp_data) && variable_struct_exists(_bp_data, "power_output")) ? _bp_data.power_output : 12;
            var _mech_speed = (!is_undefined(_bp_data) && variable_struct_exists(_bp_data, "speed")) ? _bp_data.speed : 45;
            var _mech_class = (!is_undefined(_bp_data) && variable_struct_exists(_bp_data, "class")) ? _bp_data.class : "Heavy Assault";

            array_push(inventory.deployable_mechs, {
                id: "unit_ironclad_" + string(array_length(inventory.deployable_mechs) + 1),
                blueprint_id: _fab.mech_blueprint,
                callsign: _fab.name,
                name: _fab.name,
                class: _mech_class,
                assigned_pilot: "Unassigned",
                status: "READY",
                current_condition_pct: 1.0,
                armor_rating: _mech_armor,
                power_output: _mech_power,
                speed: _mech_speed,
                combat_rating: floor(_mech_armor / 5 + _mech_speed / 2 + _mech_power * 3)
            });
            array_push(last_turn_events, "* FACTORY ROLLOUT: " + _fab.name + " finished assembly -> transferred to Hangar!");
            array_delete(facilities.active_fabrications, i, 1);
            if (instance_exists(obj_HQTerminal)) {
                obj_HQTerminal.show_toast("FACTORY: " + _fab.name + " READY IN HANGAR!", c_lime);
            }
        } else {
            array_push(last_turn_events, "* Assembly Bay: " + _fab.name + " (" + string(_fab.days_remaining) + " turns left)");
        }
    }

    // 4. Advance Contract Deadlines (docs/04)
    if (instance_exists(obj_FactionManager)) {
        for (var c = array_length(obj_FactionManager.active_contracts) - 1; c >= 0; c--) {
            var _cnt = obj_FactionManager.active_contracts[c];
            if (variable_struct_exists(_cnt, "days_remaining")) {
                _cnt.days_remaining--;
                if (_cnt.days_remaining <= 0) {
                    funds -= (variable_struct_get(_cnt, "penalty_credits") ?? 50000);
                    obj_FactionManager.modify_standing(_cnt.faction, variable_struct_get(_cnt, "reputation_penalty") ?? -20);
                    array_push(last_turn_events, "! CONTRACT BREACH: " + _cnt.title + " expired!");
                    array_delete(obj_FactionManager.active_contracts, c, 1);
                    if (instance_exists(obj_HQTerminal)) {
                        obj_HQTerminal.show_toast("CONTRACT BREACH: " + _cnt.title + " EXPIRED!", c_red);
                    }
                }
            }
        }
    }

    // 5. Hospitalized Pilot Recovery Cycle (docs/05, 07)
    for (var p = 0; p < array_length(facilities.roster_pilots); p++) {
        var _plt = facilities.roster_pilots[p];
        if ((variable_struct_get(_plt, "status") ?? "ACTIVE") == "HOSPITALIZED") {
            var _rec = variable_struct_get(_plt, "recovery_days") ?? (variable_struct_get(_plt, "recovery_days_left") ?? 3);
            _rec--;
            _plt.recovery_days = _rec;
            _plt.recovery_days_left = _rec;
            var _p_name = variable_struct_get(_plt, "name") ?? "Pilot";
            if (_rec <= 0) {
                _plt.status = "ACTIVE";
                _plt.is_deployed = false;
                array_push(last_turn_events, "* MEDICAL CLEARANCE: " + _p_name + " discharged from infirmary -> Ready for Sortie!");
                if (instance_exists(obj_HQTerminal)) {
                    obj_HQTerminal.show_toast("PILOT RECOVERED: " + _p_name + " cleared for active sortie!", c_lime);
                }
            } else {
                array_push(last_turn_events, "* Infirmary: " + _p_name + " in critical recovery (" + string(_rec) + " turns left)");
            }
        }
    }

    // 5b. Daily Sovereign Territory Tribute & Raw Material Logistics (docs/12, docs/39)
    if (instance_exists(obj_FactionManager)) {
        var _fm = obj_FactionManager;
        scr_territory_process_turn_economy();
        var _pmc_pct = _fm.territory_control.pmc_pct;
        if (_pmc_pct > 0 && !variable_struct_exists(_fm, "territory_database")) {
            var _tribute = _pmc_pct * 3500;
            funds += _tribute;
            array_push(last_turn_events, "* Sovereign Dominion Tribute: +" + string(_tribute) + " Cr from " + string(_pmc_pct) + "% governed territory.");
        }

        var _f_keys = ["faction_a", "faction_b", "faction_c", "faction_d"];
        for (var fk = 0; fk < 4; fk++) {
            var _fid = _f_keys[fk];
            if (variable_struct_exists(_fm.mass_production_contracts, _fid)) {
                var _mp = variable_struct_get(_fm.mass_production_contracts, _fid);
                if (_mp.replaced) {
                    var _stage = variable_struct_get(_mp, "adoption_stage") ?? "MATURE";
                    if (_stage == "TOOLING") {
                        _mp.tooling_turns_remaining = max(0, (variable_struct_get(_mp, "tooling_turns_remaining") ?? 2) - 1);
                        if (_mp.tooling_turns_remaining == 0) {
                            _mp.adoption_stage = "ROLLOUT";
                            _mp.active_frontline_units = 50;
                            array_push(last_turn_events, "! DOCTRINE ROLLOUT: " + _mp.faction_name + " finished shipyard tooling! 50 " + _mp.replacement_name + " units deployed to front lines!");
                        } else {
                            array_push(last_turn_events, "* Factory Tooling (" + _mp.faction_name + "): " + string(_mp.tooling_turns_remaining) + " turn(s) remaining for " + _mp.replacement_name + " lines.");
                        }
                    } else {
                        _mp.active_frontline_units = min(250, (variable_struct_get(_mp, "active_frontline_units") ?? 50) + irandom_range(12, 22));
                        var _unit_multiplier = max(1.0, _mp.active_frontline_units / 50.0);
                        var _royalty = round(_mp.royalty_per_turn * _unit_multiplier);
                        funds += _royalty;
                        _mp.cumulative_royalties_paid = (variable_struct_get(_mp, "cumulative_royalties_paid") ?? 0) + _royalty;
                        array_push(last_turn_events, "* Mass-Production Royalty (" + _mp.faction_name + "): +" + string(_royalty) + " Cr (" + string(_mp.active_frontline_units) + " active units in service).");
                    }
                }
            }
        }
    }

    // 6. Dynamic War Map & Faction AI Turn Evaluation (docs/04, docs/21)
    if (instance_exists(obj_FactionManager)) {
        obj_FactionManager.evaluate_faction_ai_turn();
        if (current_turn % 7 == 0) {
            obj_FactionManager.simulate_war_turn();
            array_push(last_turn_events, "* WAR SHIFT: " + obj_FactionManager.territory_control.last_shift_report);
        }
    }

    // 6b. Dreadnought Flagship & Rival Corporate Evaluation (Doc 23)
    evaluate_flagship_turn();

    // Evaluate Timeline Progression & Procedural Competitor Updates (docs/27)
    evaluate_timeline_progression();

    // 7. Random Corporate & Narrative Events Engine (docs/27)
    evaluate_corporate_random_events();

    // Goal D: 4 Campaign Victory Paths Evaluation
    evaluate_campaign_victory();

    // Goal E: Corporate Espionage, Shadow Raids & Nemesis Ace Retaliation
    if (instance_exists(obj_NemesisManager)) {
        obj_NemesisManager.evaluate_corporate_espionage_turn();
    }

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("ADVANCED TO TURN " + string(current_turn) + " (Y" + string(current_cycle_year) + " D" + string(current_cycle_day) + ")", c_aqua);
    }
};

step_day = end_turn; // backwards compatible alias

// =========================================================================
// RPG PILOT CANTINA, MEDICAL & PERK SYSTEM (DOC 51)
// =========================================================================
cantina_recruits = [];

refresh_cantina_recruits = function() {
    cantina_recruits = [
        {
            id: "pilot_recruit_greenhorn",
            name: "Rookie Jax Vance",
            callsign: "SPARK",
            rank: "Ensign",
            combat_stat: 6,
            tactics_stat: 5,
            accuracy: 74,
            reflexes: 70,
            morale: 90,
            salary_daily: 120,
            signing_bonus: 15000,
            xp: 20,
            rank_perks: [],
            affinity: "ironclad",
            bio: "Fresh graduate from the Lunar Tactical Academy eager to prove his worth in live combat."
        },
        {
            id: "pilot_recruit_veteran",
            name: "Sgt. Brandon Ruiz",
            callsign: "BARRICADE",
            rank: "Master Sergeant",
            combat_stat: 8,
            tactics_stat: 7,
            accuracy: 82,
            reflexes: 76,
            morale: 85,
            salary_daily: 220,
            signing_bonus: 35000,
            xp: 75,
            rank_perks: ["Deadly Aim"],
            affinity: "ironclad",
            bio: "Ten-year veteran of the Terran border conflicts. Reliable gunner with heavy cannon specialization."
        },
        {
            id: "pilot_recruit_sniper",
            name: "Operative Yuna Chen",
            callsign: "SILVER-EYE",
            rank: "Lieutenant",
            combat_stat: 9,
            tactics_stat: 8,
            accuracy: 91,
            reflexes: 84,
            morale: 95,
            salary_daily: 340,
            signing_bonus: 60000,
            xp: 120,
            rank_perks: ["Deadly Aim", "Spotter Array"],
            affinity: "muramasa",
            bio: "Renegade colony sniper with uncanny optic reflexes and pinpoint precision at extreme range."
        },
        {
            id: "pilot_recruit_ace",
            name: "Ace Malakor Graves",
            callsign: "HELLHOUND",
            rank: "Captain",
            combat_stat: 9,
            tactics_stat: 9,
            accuracy: 88,
            reflexes: 92,
            morale: 100,
            salary_daily: 420,
            signing_bonus: 85000,
            xp: 180,
            rank_perks: ["Vernier Drift", "Heavy Breech", "Counter-Strike"],
            affinity: "aether",
            bio: "Notorious former Syndicate ace turned gun-for-hire. Has single-handedly turned the tide of six separate orbital engagements."
        }
    ];
};
refresh_cantina_recruits();

hire_cantina_pilot = function(_idx) {
    if (_idx < 0 || _idx >= array_length(cantina_recruits)) return false;
    var _p = cantina_recruits[_idx];
    if (funds < _p.signing_bonus) return false;
    funds -= _p.signing_bonus;
    
    var _new_pilot = {
        id: _p.id + "_" + string(irandom(9999)),
        character_id: _p.id,
        name: _p.name,
        callsign: _p.callsign,
        rank: _p.rank,
        combat_stat: _p.combat_stat,
        tactics_stat: _p.tactics_stat,
        accuracy: _p.accuracy,
        reflexes: _p.reflexes,
        morale: _p.morale,
        salary_daily: _p.salary_daily,
        is_deployed: false,
        status: "ACTIVE",
        recovery_days: 0,
        recovery_days_left: 0,
        kills: 0,
        sorties: 0,
        fatigue: 0,
        level: 1,
        unspent_stat_points: 0,
        mutated_traits: [],
        xp: _p.xp,
        rank_perks: _p.rank_perks,
        affinity: _p.affinity,
        bio: _p.bio
    };
    array_push(facilities.roster_pilots, _new_pilot);
    array_delete(cantina_recruits, _idx, 1);
    return true;
};

expedite_pilot_medical = function(_pilot_idx) {
    if (_pilot_idx < 0 || _pilot_idx >= array_length(facilities.roster_pilots)) return false;
    var _p = facilities.roster_pilots[_pilot_idx];
    if (_p.status != "HOSPITALIZED") return false;
    if (funds < 20000) return false;
    funds -= 20000;
    _p.recovery_days_left = max(0, (variable_struct_exists(_p, "recovery_days_left") ? _p.recovery_days_left : 2) - 2);
    if (_p.recovery_days_left <= 0) {
        _p.status = "ACTIVE";
        _p.recovery_days = 0;
        _p.recovery_days_left = 0;
    }
    return true;
};

unlock_pilot_perk = function(_pilot_idx, _perk_name, _xp_cost) {
    if (_pilot_idx < 0 || _pilot_idx >= array_length(facilities.roster_pilots)) return false;
    var _p = facilities.roster_pilots[_pilot_idx];
    if (!variable_struct_exists(_p, "xp") || _p.xp < _xp_cost) return false;
    if (!variable_struct_exists(_p, "rank_perks") || !is_array(_p.rank_perks)) _p.rank_perks = [];
    
    for (var i = 0; i < array_length(_p.rank_perks); i++) {
        if (_p.rank_perks[i] == _perk_name) return false;
    }
    
    _p.xp -= _xp_cost;
    array_push(_p.rank_perks, _perk_name);
    return true;
};

allocate_pilot_stat = function(_pilot_idx, _stat_name) {
    if (!variable_struct_exists(facilities, "roster_pilots")) return false;
    if (_pilot_idx < 0 || _pilot_idx >= array_length(facilities.roster_pilots)) return false;
    var _plt = facilities.roster_pilots[_pilot_idx];
    if (!variable_struct_exists(_plt, "unspent_stat_points") || _plt.unspent_stat_points <= 0) return false;

    if (_stat_name == "accuracy") {
        if (_plt.accuracy >= 99) return false;
        _plt.accuracy = min(99, _plt.accuracy + 2);
        _plt.unspent_stat_points -= 1;
        array_push(last_turn_events, "* STAT ALLOCATION: " + _plt.name + " (" + _plt.callsign + ") Accuracy increased to " + string(_plt.accuracy) + "%!");
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast(_plt.callsign + " Accuracy -> " + string(_plt.accuracy) + "%", c_aqua);
        return true;
    } else if (_stat_name == "reflexes") {
        if (_plt.reflexes >= 99) return false;
        _plt.reflexes = min(99, _plt.reflexes + 2);
        _plt.unspent_stat_points -= 1;
        array_push(last_turn_events, "* STAT ALLOCATION: " + _plt.name + " (" + _plt.callsign + ") Reflexes increased to " + string(_plt.reflexes) + "%!");
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast(_plt.callsign + " Reflexes -> " + string(_plt.reflexes) + "%", c_aqua);
        return true;
    } else if (_stat_name == "combat_stat") {
        if (_plt.combat_stat >= 10) return false;
        _plt.combat_stat = min(10, _plt.combat_stat + 1);
        _plt.unspent_stat_points -= 1;
        array_push(last_turn_events, "* STAT ALLOCATION: " + _plt.name + " (" + _plt.callsign + ") Combat Stat increased to " + string(_plt.combat_stat) + "/10!");
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast(_plt.callsign + " Combat Stat -> " + string(_plt.combat_stat) + "/10", c_aqua);
        return true;
    } else if (_stat_name == "tactics_stat") {
        if (_plt.tactics_stat >= 10) return false;
        _plt.tactics_stat = min(10, _plt.tactics_stat + 1);
        _plt.unspent_stat_points -= 1;
        array_push(last_turn_events, "* STAT ALLOCATION: " + _plt.name + " (" + _plt.callsign + ") Tactics Stat increased to " + string(_plt.tactics_stat) + "/10!");
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast(_plt.callsign + " Tactics Stat -> " + string(_plt.tactics_stat) + "/10", c_aqua);
        return true;
    }
    return false;
};

send_pilot_on_rr = function(_pilot_idx) {
    if (!variable_struct_exists(facilities, "roster_pilots")) return false;
    if (_pilot_idx < 0 || _pilot_idx >= array_length(facilities.roster_pilots)) return false;
    var _plt = facilities.roster_pilots[_pilot_idx];
    if (funds < 5000) return false;
    funds -= 5000;
    _plt.fatigue = 0;
    _plt.morale = min(100, (variable_struct_exists(_plt, "morale") ? _plt.morale : 80) + 10);
    array_push(last_turn_events, "* R&R LEAVE: " + _plt.name + " (" + _plt.callsign + ") granted shore leave (-5,000 Cr). Fatigue cleared, Morale +10!");
    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("R&R LEAVE: " + _plt.callsign + " refreshed! Fatigue cleared, Morale +10.", c_aqua);
    }
    return true;
};

mutate_pilot_trait = function(_pilot_idx, _trait_name) {
    if (!variable_struct_exists(facilities, "roster_pilots")) return false;
    if (_pilot_idx < 0 || _pilot_idx >= array_length(facilities.roster_pilots)) return false;
    var _plt = facilities.roster_pilots[_pilot_idx];
    if (!variable_struct_exists(_plt, "mutated_traits") || !is_array(_plt.mutated_traits)) {
        _plt.mutated_traits = [];
    }
    if (array_contains(_plt.mutated_traits, _trait_name)) return false;
    array_push(_plt.mutated_traits, _trait_name);

    if (_trait_name == "Iron Survivor") {
        _plt.morale = min(100, (variable_struct_exists(_plt, "morale") ? _plt.morale : 80) + 5);
    } else if (_trait_name == "Cybernetic Reflex Augment") {
        _plt.accuracy = min(99, _plt.accuracy + 6);
    }

    array_push(last_turn_events, "! BATTLE SCAR TRAIT MUTATION: " + _plt.name + " (" + _plt.callsign + ") developed '" + _trait_name + "'!");
    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("TRAIT MUTATION: " + _plt.callsign + " gained " + _trait_name + "!", c_fuchsia);
    }
    return true;
};

// Goal E: Resolve Corporate Pilot Poaching Counter-Offer (docs/28)
resolve_poaching_offer = function(_action) {
    if (is_undefined(pending_poaching_offer)) return false;
    var _po = pending_poaching_offer;
    var _plt = undefined;
    if (_po.pilot_index >= 0 && _po.pilot_index < array_length(facilities.roster_pilots)) {
        _plt = facilities.roster_pilots[_po.pilot_index];
    }

    if (_action == "counter") {
        var _cost = _po.counter_cost;
        funds -= _cost;
        if (!is_undefined(_plt)) {
            _plt.fatigue = 0;
            pilot_add_xp(_plt.id, 150);
        }
        array_push(last_turn_events, "* ESPIONAGE RESOLVED: Paid " + string(_cost) + " Cr loyalty bonus to retain " + _po.pilot_name + " (" + _po.callsign + ")!");
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("LOYALTY SECURED: " + _po.callsign + " remains in PMC service!", c_lime);
        }
        pending_poaching_offer = undefined;
        return true;
    } else if (_action == "sigint_sweep") {
        var _sig_tier = variable_struct_exists(flagship.upgrades, "sigint_tier") ? flagship.upgrades.sigint_tier : 1;
        var _success_chance = 60 + (_sig_tier * 10);
        if (flagship.specialization_protocol == "shadow_panopticon") _success_chance = 100;
        var _roll = random(100);

        if (_roll < _success_chance) {
            // Arrest spy into brig
            if (instance_exists(obj_NemesisManager)) {
                obj_NemesisManager.add_prisoner("spy_" + _po.corp_id + "_" + string(current_turn), "Corporate Infiltrator", _po.corp_id);
            }
            // Grant corporate equity or cash
            if (variable_struct_exists(rival_corporations, _po.corp_id)) {
                var _rc = variable_struct_get(rival_corporations, _po.corp_id);
                if (!_rc.is_acquired) {
                    _rc.player_shares = min(100000, _rc.player_shares + 1500);
                    _rc.player_equity_pct = (_rc.player_shares / 100000.0) * 100.0;
                }
            }
            funds += 45000;
            if (!is_undefined(_plt)) _plt.fatigue = max(0, _plt.fatigue - 1);
            array_push(last_turn_events, "* SIGINT COUNTER-ESPIONAGE: Flagship intercepted " + _po.corp_name + " handler! Extracted +1,500 shares & +45,000 Cr!");
            if (instance_exists(obj_HQTerminal)) {
                obj_HQTerminal.show_toast("SIGINT SWEEP SUCCESS: " + _po.corp_name + " handler arrested! (+1,500 shares)", c_lime);
            }
        } else {
            array_push(last_turn_events, "* SIGINT SWEEP: Corporate headhunter slipped away, but recruitment conduit was terminated.");
            if (instance_exists(obj_HQTerminal)) {
                obj_HQTerminal.show_toast("SIGINT NOTICE: Handler escaped, but leak plugged.", c_yellow);
            }
        }
        pending_poaching_offer = undefined;
        return true;
    } else if (_action == "refuse") {
        var _defect_roll = random(100);
        if (_defect_roll < 50 && !is_undefined(_plt)) {
            array_push(last_turn_events, "! PILOT DEFECTION: " + _po.pilot_name + " (" + _po.callsign + ") accepted " + _po.corp_name + " contract and deserted the PMC!");
            if (instance_exists(obj_HQTerminal)) {
                obj_HQTerminal.show_toast("DEFECTION! " + _po.callsign + " deserted to " + _po.corp_name + "!", c_red);
            }
            array_delete(facilities.roster_pilots, _po.pilot_index, 1);
        } else {
            array_push(last_turn_events, "* PILOT REMAINED: " + _po.pilot_name + " (" + _po.callsign + ") refused rival offer out of mercenary honor.");
            if (instance_exists(obj_HQTerminal)) {
                obj_HQTerminal.show_toast("PILOT STAYED: " + _po.callsign + " rejected " + _po.corp_name + " offer!", c_yellow);
            }
        }
        pending_poaching_offer = undefined;
        return true;
    }
    return false;
};

// Goal D: 4 Grand Campaign Victory Paths Evaluator (docs/12, docs/24, docs/39)
evaluate_campaign_victory = function() {
    if (campaign_victory_claimed) return campaign_victory_data;

    var _won_path = "";
    var _v_title = "";
    var _v_subtitle = "";
    var _v_badge = "";
    var _v_quote = "";
    var _v_chronicle = "";
    var _v_highlights = [];

    var _fm = instance_exists(obj_FactionManager) ? obj_FactionManager : undefined;
    var _bm = instance_exists(obj_BlueprintManager) ? obj_BlueprintManager : undefined;

    // -------------------------------------------------------------------------
    // PATH 1: CORPORATE MONOPOLIST (Market Hegemony)
    // -------------------------------------------------------------------------
    var _factions_replaced = 0;
    var _total_royalties = 0;
    if (!is_undefined(_fm)) {
        var _f_keys = ["faction_a", "faction_b", "faction_c", "faction_d"];
        for (var fk = 0; fk < 4; fk++) {
            var _fid = _f_keys[fk];
            if (variable_struct_exists(_fm.mass_production_contracts, _fid)) {
                var _mp = variable_struct_get(_fm.mass_production_contracts, _fid);
                if (_mp.replaced) {
                    _factions_replaced++;
                    _total_royalties += variable_struct_get(_mp, "cumulative_royalties_paid") ?? 0;
                }
            }
        }
    }
    var _majority_corps = 0;
    var _corp_keys = ["corp_vhi", "corp_aod", "corp_rust", "corp_hats"];
    for (var ck = 0; ck < 4; ck++) {
        var _cid = _corp_keys[ck];
        if (variable_struct_exists(rival_corporations, _cid)) {
            var _rc = variable_struct_get(rival_corporations, _cid);
            if ((variable_struct_get(_rc, "player_equity_pct") ?? 0) >= 51.0) _majority_corps++;
        }
    }

    if (_factions_replaced >= 3 || _majority_corps >= 3) {
        _won_path = "MONOPOLIST";
        _v_title = "THE CORPORATE MONOPOLIST";
        _v_subtitle = "SUPREME MARKET HEGEMON & SHADOW SOVEREIGN";
        _v_badge = "★ SOL MONOPOLY CHARTER RATIFIED ★";
        _v_quote = "Governments declare wars; accountants and armament syndicates determine who survives them.";
        _v_chronicle = "By ratifying mass-production replacement contracts across the solar system's rival superpowers, your private enterprise has monopolized the entire interplanetary arms trade. Terran legions, Jovian aerospace squadrons, and Martian trench garrisons now rely exclusively on warframes forged in your assembly bays. As their national treasuries pour into your coffers, you pull the strings of civilization without ever having to wear a crown.";
        _v_highlights = [
            "Superpower Contracts Ratified: " + string(_factions_replaced) + " / 4 Superpowers",
            "Cumulative Royalties Collected: " + string(_total_royalties) + " Credits",
            "Majority Megacorp Stakes: " + string(_majority_corps) + " Corporations Controlled",
            "Total PMC Treasury Reserves: " + string(funds) + " Credits"
        ];
    }

    // -------------------------------------------------------------------------
    // PATH 2: WARLORD HEGEMON (Military Dominion)
    // -------------------------------------------------------------------------
    if (_won_path == "" && !is_undefined(_fm)) {
        var _pmc_pct = _fm.territory_control.pmc_pct;
        var _holds_earth_cap = false;
        var _holds_space_cap = false;
        var _holds_mars_cap = false;

        if (variable_struct_exists(_fm, "territory_database") && is_struct(_fm.territory_database)) {
            var _td = _fm.territory_database;
            if ((variable_struct_exists(_td, "earth_granite_redoubt") && _td.earth_granite_redoubt.controlling_faction == "pmc") ||
                (variable_struct_exists(_td, "earth_cascadia_driver") && _td.earth_cascadia_driver.controlling_faction == "pmc") ||
                (variable_struct_exists(_td, "earth_gibraltar_redoubt") && _td.earth_gibraltar_redoubt.controlling_faction == "pmc")) {
                _holds_earth_cap = true;
            }
            if ((variable_struct_exists(_td, "space_selene_zenith") && _td.space_selene_zenith.controlling_faction == "pmc") ||
                (variable_struct_exists(_td, "space_kepler_haven") && _td.space_kepler_haven.controlling_faction == "pmc") ||
                (variable_struct_exists(_td, "space_tartarus_citadel") && _td.space_tartarus_citadel.controlling_faction == "pmc")) {
                _holds_space_cap = true;
            }
            if ((variable_struct_exists(_td, "mars_olympus_caldera") && _td.mars_olympus_caldera.controlling_faction == "pmc") ||
                (variable_struct_exists(_td, "mars_tharsis_foundry") && _td.mars_tharsis_foundry.controlling_faction == "pmc") ||
                (variable_struct_exists(_td, "mars_marineris_rift") && _td.mars_marineris_rift.controlling_faction == "pmc")) {
                _holds_mars_cap = true;
            }
        }

        var _holds_all_capitals = (_holds_earth_cap && _holds_space_cap && _holds_mars_cap);

        if (_pmc_pct >= 60 || _holds_all_capitals) {
            _won_path = "WARLORD";
            _v_title = "THE SUPREME WARLORD HEGEMON";
            _v_subtitle = "ABSOLUTE MILITARY DOMINION ACROSS SOL";
            _v_badge = "★ PAX HEGEMONIA: SOVEREIGN EMPIRE ★";
            _v_quote = "Peace is not the absence of conflict; it is the absolute certainty of defeat for anyone who defies us.";
            _v_chronicle = "The great planetary armadas and colonial fleets have shattered against your veteran vanguard squadrons. From the orbital sky-hooks of Earth to the deep terraformed trenches of Olympus Mons, the sovereign banner of your Private Military Corporation flies unopposed. You have dismantled the old geopolitical order through steel, blood, and sheer tactical supremacy, establishing an ironclad era of Mercenary Pax Hegemonia.";
            _v_highlights = [
                "Sovereign Territory Governed: " + string(_pmc_pct) + "% of Sol System",
                "Theater Capitals Garrisoned: " + (_holds_all_capitals ? "3 / 3 (Earth, Lunar, Mars)" : "Regional Hegemon"),
                "Sorties Won in Conquest: " + string(total_sorties_won) + " Combat Victories",
                "Superpower Regimes Annexed: " + string(array_length(_fm.factions_overthrown)) + " Factions"
            ];
        }
    }

    // -------------------------------------------------------------------------
    // PATH 3: ARCHEOTECH TRANSCENDENT (Technological Singularity)
    // -------------------------------------------------------------------------
    if (_won_path == "") {
        var _t5_count = 0;
        var _tracks = ["fabrication_tier", "mining_tier", "defense_tier", "weapons_tier", "propulsion_tier", "pilot_suite_tier", "sigint_tier", "command_tier"];
        for (var t = 0; t < array_length(_tracks); t++) {
            if ((variable_struct_get(flagship.upgrades, _tracks[t]) ?? 1) >= 5) _t5_count++;
        }
        var _techs_unlocked = (variable_struct_exists(self, "research_unlocked_techs") && is_array(research_unlocked_techs)) ? array_length(research_unlocked_techs) : 0;

        if (_t5_count >= 8 || _techs_unlocked >= 30) {
            _won_path = "ARCHEOTECH";
            _v_title = "THE ARCHEOTECH TRANSCENDENT";
            _v_subtitle = "SINGULARITY AWAKENED // ZERO-POINT DOMINION";
            _v_badge = "★ TACHYON TRANSCENDENCE UNLOCKED ★";
            _v_quote = "We no longer merely adapt to physics; we rewrite the baseline equations of combat.";
            _v_chronicle = "Through relentless metallurgical synthesis, crucible breakthroughs, and ancient Pre-War archeotech unsealing, your engineers have breached the threshold of conventional science. The USN-X Hephaestus has awakened its true form as a self-sustaining stellar forge, harnessing zero-point vacuum energy and instantaneous tachyon fold transit. Humanity's warlords gaze upward in terror and awe at a power that has rendered conventional weaponry obsolete.";
            _v_highlights = [
                "Flagship Divisions at Tier 5: " + string(_t5_count) + " / 8 Maxed",
                "R&D Technologies Unlocked: " + string(_techs_unlocked) + " / 30 Technologies",
                "Masterwork Prototypes Forged: " + string(!is_undefined(_bm) ? array_length(_bm.masterwork_inventory) : 0) + " Units",
                "Flagship Specialization: " + string_upper(flagship.specialization_protocol)
            ];
        }
    }

    // -------------------------------------------------------------------------
    // PATH 4: CRISIS SAVIOR (Sol Guardian / Apex Repulsion)
    // -------------------------------------------------------------------------
    if (_won_path == "") {
        var _in_crisis_era = (timeline_era >= 4 || current_turn >= 150 || current_cycle_year >= 218);
        var _repelled = (crisis_defeated || total_sorties_won >= 15);
        if (_in_crisis_era && _repelled) {
            _won_path = "CRISIS_SAVIOR";
            _v_title = "THE APEX CRISIS SAVIOR";
            _v_subtitle = "GUARDIAN OF SOL // EXISTENTIAL SHIELD";
            _v_badge = "★ SOL CRISIS VANQUISHED ★";
            _v_quote = "When the machines turned and the sky caught fire, only the mercenaries stood between humanity and the abyss.";
            _v_chronicle = "When the automated planetary defense networks malfunctioned and unsealed rogue biomechanical superweapons in Era IV, planetary high commands abandoned their populations to chaos. Your PMC ace squadrons stood alone against the encroaching existential terror, launching daring sorties into the heart of the anomaly. Through unbreakable tactical discipline and masterwork firepower, you severed the crisis core, rescuing the Sol System from total extinction.";
            _v_highlights = [
                "Crisis Status: ANOMALY CORE DESTROYED",
                "Campaign Sorties Survived: " + string(total_sorties_won) + " Operations",
                "Timeline Era: " + timeline_era_name,
                "Veteran Aces in Active Service: " + string(array_length(facilities.roster_pilots)) + " Pilots"
            ];
        }
    }

    // If victory achieved:
    if (_won_path != "") {
        campaign_won = true;
        campaign_victory_claimed = true;
        campaign_victory_path = _won_path;
        campaign_victory_data = {
            victory_path: _won_path,
            title: _v_title,
            subtitle: _v_subtitle,
            badge: _v_badge,
            quote: _v_quote,
            chronicle: _v_chronicle,
            stat_highlights: _v_highlights,
            turn: current_turn,
            year: current_cycle_year,
            day: current_cycle_day
        };

        array_push(last_turn_events, "★★ GRAND CAMPAIGN VICTORY ACHIEVED: " + _v_title + " ★★");
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.showing_victory_modal = true;
            obj_HQTerminal.show_toast("GRAND CAMPAIGN VICTORY: " + _v_title + "!", c_yellow);
        }
        scr_audio_play_ui("confirm");
        return campaign_victory_data;
    }

    return undefined;
};

// 9c. Sid Meier's Pirates-Style Career Retirement & Legacy Assessment (docs/12)
retire_career = function() {
    var _mat_val = (inventory.raw_materials.mat_tungsten * 400) + 
                   (inventory.raw_materials.mat_silica_carb * 150) + 
                   (inventory.raw_materials.mat_tritium * 1200) + 
                   (inventory.raw_materials.mat_syn_flux * 800);
    var _hb = variable_struct_exists(facilities, "hangar_bays") ? facilities.hangar_bays : (variable_struct_exists(facilities, "assembly_lines") ? facilities.assembly_lines : 1);
    var _lt = variable_struct_exists(facilities, "lab_tier") ? facilities.lab_tier : ((variable_struct_exists(facilities, "containment_shielding") && facilities.containment_shielding) ? 2 : 1);
    var _fc = variable_struct_exists(facilities, "foundry_crucibles") ? facilities.foundry_crucibles : (variable_struct_exists(facilities, "crucible_tier") ? facilities.crucible_tier : 1);
    var _facility_val = (_hb * 250000) + (_lt * 400000) + (_fc * 300000);
    var _net_worth = funds + _facility_val + _mat_val;

    // 1. Wealth Score (Max 2,500)
    var _score_wealth = min(2500, floor(_net_worth / 4000));

    // 2. Sovereign Territory Score (Max 2,500)
    var _pmc_pct = (instance_exists(obj_FactionManager)) ? obj_FactionManager.territory_control.pmc_pct : 0;
    var _score_territory = min(2500, floor(_pmc_pct * 25));

    // 3. Mass-Production Monopoly Score (Max 2,000)
    var _factions_replaced = 0;
    var _total_royalties = 0;
    if (instance_exists(obj_FactionManager)) {
        var _f_keys = ["faction_a", "faction_b", "faction_c", "faction_d"];
        for (var fk = 0; fk < 4; fk++) {
            var _fid = _f_keys[fk];
            if (variable_struct_exists(obj_FactionManager.mass_production_contracts, _fid)) {
                var _mp = variable_struct_get(obj_FactionManager.mass_production_contracts, _fid);
                if (_mp.replaced) {
                    _factions_replaced++;
                    _total_royalties += _mp.cumulative_royalties_paid;
                }
            }
        }
    }
    var _score_monopoly = min(2000, (_factions_replaced * 400) + min(1000, floor(_total_royalties / 10000)));

    // 4. Ace Mercenary Guild Score (Max 1,000)
    var _pilot_count = array_length(facilities.roster_pilots);
    var _score_guild = min(1000, (_pilot_count * 150) + (total_sorties_won * 50));

    // 5. Technological Supremacy Score (Max 1,000)
    var _mw_count = (instance_exists(obj_BlueprintManager)) ? array_length(obj_BlueprintManager.masterwork_inventory) : 0;
    var _bp_count = (instance_exists(obj_BlueprintManager)) ? variable_struct_names_count(obj_BlueprintManager.unlocked_blueprints) : 1;
    var _score_tech = min(1000, (_mw_count * 200) + (_bp_count * 100));

    // 6. Faction Overthrow Conquest Score (Max 1,000)
    var _overthrown_count = (instance_exists(obj_FactionManager)) ? array_length(obj_FactionManager.factions_overthrown) : 0;
    var _score_conquest = min(1000, _overthrown_count * 250);

    var _score_victory = (campaign_won && !is_undefined(campaign_victory_data)) ? 2000 : 0;
    var _total_score = _score_wealth + _score_territory + _score_monopoly + _score_guild + _score_tech + _score_conquest + _score_victory;

    // Determine Dynamic Title & Historical Epilogue Chronicle (docs/12)
    var _title = (campaign_won && !is_undefined(campaign_victory_data)) ? campaign_victory_data.title : "Hardened Mercenary Commander";
    var _epilogue = (campaign_won && !is_undefined(campaign_victory_data)) ? campaign_victory_data.chronicle : "You served through the crucible of the mecha wars with distinction, forging an enduring mercenary name across the stars.";

    if (_pmc_pct >= 70) {
        _title = "Supreme Solar Hegemon & Galactic Warlord";
        _epilogue = "The warring superpowers crumbled before your personal legions. The solar system is unified under the absolute sovereign dominion of your Private Military Corporation, establishing an ironclad era of mercenary Pax Hegemonia.";
    } else if (_factions_replaced >= 4 && _net_worth >= 5000000) {
        _title = "The Shadow Sovereign & Puppetmaster";
        _epilogue = "You never openly crowned yourself emperor; instead, you licensed the warframes used by every army in existence. As Terran and Colony soldiers fired your guns, your vaults overflowed, secretly pulling the strings of interstellar civilization.";
    } else if (_net_worth >= 8000000 && _factions_replaced >= 2) {
        _title = "Titan of the Military-Industrial Complex";
        _epilogue = "Your manufacturing foundries and proprietary blueprints outproduced entire planetary governments. Prime Ministers and Colonial Councils knelt before your Board of Directors, begging for delivery allocations.";
    } else if (instance_exists(obj_FactionManager) && obj_FactionManager.get_standing("faction_a") >= 70 && obj_FactionManager.territory_control.terran_pct >= 50) {
        _title = "Grand Marshal of the Terran Coalition";
        _epilogue = "Through blood and unbreakable armor plating, your mercenary vanguard preserved the cradle of humanity, crushing colonial uprisings and securing Earth's undisputed supremacy.";
    } else if (instance_exists(obj_FactionManager) && obj_FactionManager.get_standing("faction_b") >= 70 && obj_FactionManager.territory_control.colony_pct >= 50) {
        _title = "Liberator of the Outer Colonies";
        _epilogue = "Spearheading orbital combat wings, your machines shattered Earth's colonial embargoes. Lagrange colonies celebrate your PMC as the architects of interstellar independence.";
    } else if (instance_exists(obj_FactionManager) && obj_FactionManager.get_standing("faction_c") >= 70 && obj_FactionManager.territory_control.syndicate_pct >= 30) {
        _title = "Dread Void Corsair Kingpin";
        _epilogue = "You transformed scattered black-market pirate syndicates into an untouchable corsair empire. The asteroid trade lanes answer solely to your flag, collecting endless transit tolls.";
    } else if (instance_exists(obj_FactionManager) && obj_FactionManager.get_standing("faction_d") >= 70 && _score_tech >= 700) {
        _title = "Apex Cyber-Oligarch";
        _epilogue = "Merging neural bio-matrices with hyper-advanced mobile frames, you ascended into the supreme directorate of the Zaibatsu, controlling the flow of high technology and transhuman cybernetics.";
    } else if (_mw_count >= 3 && _score_tech >= 750) {
        _title = "Master Artisan of the Void Frontier";
        _epilogue = "Rather than mass-producing cheap grunt suits, you forged the most feared one-of-a-kind Masterwork war machines in history. Mercenary aces speak of your prototypes in hushed, reverent whispers.";
    } else if (_total_score < 2500) {
        _title = "Frontier Scavenger in Default";
        _epilogue = "You retired before cementing your mark on history, surviving with a patched-up hull and fond memories of high-stakes corporate warfare.";
    }

    var _rank_str = "RANK C: FRONTIER VETERAN";
    if (_total_score >= 8000) _rank_str = "RANK S: LEGENDARY OVERLORD";
    else if (_total_score >= 6000) _rank_str = "RANK A: MASTER OF WAR";
    else if (_total_score >= 4000) _rank_str = "RANK B: DISTINGUISHED COMMANDER";

    career_summary = {
        title: _title,
        rank_grade: _rank_str,
        total_score: _total_score,
        score_wealth: _score_wealth,
        score_territory: _score_territory,
        score_monopoly: _score_monopoly,
        score_guild: _score_guild,
        score_tech: _score_tech,
        score_conquest: _score_conquest,
        net_worth: _net_worth,
        pmc_territory_pct: _pmc_pct,
        factions_replaced_count: _factions_replaced,
        total_royalties_collected: _total_royalties,
        factions_overthrown_count: _overthrown_count,
        masterworks_tuned: _mw_count,
        pilots_commanded: _pilot_count,
        campaign_days: current_turn,
        epilogue_chronicle: _epilogue
    };

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.showing_retire_modal = true;
    }
    return career_summary;
};

resume_sandbox = function() {
    career_summary = undefined;
    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.showing_retire_modal = false;
        obj_HQTerminal.show_toast("SANDBOX RESUMED: Commander returned to active strategic operations!", c_lime);
    }
};

// 9b. Advanced Assembly Fabrication Method (docs/07)
fabricate_mech_advanced = function(_blueprint_id, _name, _days, _cost_cr, _alloys_req, _tungsten_req) {
    if (array_length(facilities.active_fabrications) >= facilities.assembly_lines) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("ASSEMBLY CAPACITY FULL! Upgrade bays in Factory.", c_red);
        return false;
    }
    if (funds < _cost_cr) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT FUNDS! Requires " + string(_cost_cr) + " Cr", c_red);
        return false;
    }
    var _cur_alloy = variable_struct_get(inventory.alloys, "alloy_vanguard_comp") ?? 0;
    var _cur_tungsten = variable_struct_get(inventory.raw_materials, "mat_tungsten") ?? 0;
    if (_cur_alloy < _alloys_req || _cur_tungsten < _tungsten_req) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT MATERIALS! Requires " + string(_alloys_req) + " Vanguard Alloys & " + string(_tungsten_req) + " Tungsten", c_red);
        return false;
    }
    // Deduct
    spend_funds(_cost_cr);
    variable_struct_set(inventory.alloys, "alloy_vanguard_comp", _cur_alloy - _alloys_req);
    variable_struct_set(inventory.raw_materials, "mat_tungsten", _cur_tungsten - _tungsten_req);
    array_push(facilities.active_fabrications, {
        mech_blueprint: _blueprint_id,
        name: _name,
        days_remaining: _days,
        total_days: _days
    });
    if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("COMMENCED FABRICATION: " + _name + " (" + string(_days) + " Days)!", c_lime);
    return true;
};

// 10. Facility Management & Deployment Methods (docs/06, 07)
deploy_to_node = function(_node_idx, _mech_id, _pilot_name) {
    if (_node_idx >= 0 && _node_idx < array_length(nodes)) {
        var _node = nodes[_node_idx];
        _node.assigned_mech_id = _mech_id;
        _node.assigned_pilot_name = _pilot_name;
        _node.status = "ACTIVE_MINING";

        // Mark mech as deployed
        for (var m = 0; m < array_length(inventory.deployable_mechs); m++) {
            if (inventory.deployable_mechs[m].id == _mech_id) {
                inventory.deployable_mechs[m].status = "DEPLOYED_MINING";
            }
        }
        return true;
    }
    return false;
};

recall_from_node = function(_node_idx) {
    if (_node_idx >= 0 && _node_idx < array_length(nodes)) {
        var _node = nodes[_node_idx];
        var _mid = _node.assigned_mech_id;
        _node.status = "UNCLAIMED";
        _node.assigned_mech_id = "Unassigned";
        _node.assigned_pilot_name = "Unassigned";

        // Restore mech in hangar
        for (var m = 0; m < array_length(inventory.deployable_mechs); m++) {
            if (inventory.deployable_mechs[m].id == _mid) {
                inventory.deployable_mechs[m].status = "READY";
            }
        }
        return true;
    }
    return false;
};

extract_node_storage = function(_node_idx) {
    if (_node_idx >= 0 && _node_idx < array_length(nodes)) {
        var _node = nodes[_node_idx];
        var _keys = variable_struct_get_names(_node.current_storage);
        for (var k = 0; k < array_length(_keys); k++) {
            var _key = _keys[k];
            var _amt = (variable_struct_exists(_node.current_storage, _key) ? variable_struct_get(_node.current_storage, _key) : 0);
            if (_amt > 0) {
                add_raw_material(_key, _amt);
                variable_struct_set(_node.current_storage, _key, 0);
            }
        }
        return true;
    }
    return false;
};

// Material & Treasury Management Methods
add_funds = function(_amount) { if (_amount > 0) { funds += _amount; return true; } return false; };
spend_funds = function(_amount) { if (_amount > 0 && funds >= _amount) { funds -= _amount; return true; } return false; };

get_raw_material = function(_mat_id) { return (variable_struct_exists(inventory.raw_materials, _mat_id) ? variable_struct_get(inventory.raw_materials, _mat_id) : 0); };
add_raw_material = function(_mat_id, _quantity) {
    if (!variable_struct_exists(inventory.raw_materials, _mat_id)) variable_struct_set(inventory.raw_materials, _mat_id, 0);
    variable_struct_set(inventory.raw_materials, _mat_id, variable_struct_get(inventory.raw_materials, _mat_id) + _quantity);
    return variable_struct_get(inventory.raw_materials, _mat_id);
};
spend_raw_material = function(_mat_id, _quantity) {
    var _cur = get_raw_material(_mat_id);
    if (_cur >= _quantity) {
        variable_struct_set(inventory.raw_materials, _mat_id, variable_struct_get(inventory.raw_materials, _mat_id) - _quantity);
        return true;
    }
    return false;
};

add_alloy = function(_alloy_key, _quantity) {
    if (!variable_struct_exists(inventory.alloys, _alloy_key)) variable_struct_set(inventory.alloys, _alloy_key, 0);
    variable_struct_set(inventory.alloys, _alloy_key, variable_struct_get(inventory.alloys, _alloy_key) + _quantity);
    return variable_struct_get(inventory.alloys, _alloy_key);
};
get_alloy = function(_alloy_key) { return (variable_struct_exists(inventory.alloys, _alloy_key) ? variable_struct_get(inventory.alloys, _alloy_key) : 0); };
spend_alloy = function(_alloy_key, _quantity) {
    var _cur = get_alloy(_alloy_key);
    if (_cur >= _quantity) {
        variable_struct_set(inventory.alloys, _alloy_key, variable_struct_get(inventory.alloys, _alloy_key) - _quantity);
        return true;
    }
    return false;
};

// Modular Part Fabrication Method (docs/13)
craft_modular_part = function(_part_data, _alloy_key, _alloy_cost, _cr_cost) {
    if (funds < _cr_cost) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT FUNDS! (Requires " + string(_cr_cost) + " Cr)", c_red);
        return false;
    }
    if (get_alloy(_alloy_key) < _alloy_cost) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT ALLOYS! (Requires " + string(_alloy_cost) + "x " + _alloy_key + ")", c_red);
        return false;
    }
    spend_funds(_cr_cost);
    spend_alloy(_alloy_key, _alloy_cost);

    var _slot_key = _part_data.slot;
    if (!variable_struct_exists(inventory.parts, _slot_key)) {
        variable_struct_set(inventory.parts, _slot_key, []);
    }
    array_push(variable_struct_get(inventory.parts, _slot_key), _part_data);

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("PART FORGED: " + _part_data.name + " added to inventory!", c_lime);
    }
    return true;
};

add_part_to_inventory = function(_part_data) {
    if (!is_struct(_part_data)) return false;
    var _slot_key = variable_struct_get(_part_data, "slot") ?? "heads";
    if (!variable_struct_exists(inventory.parts, _slot_key)) {
        variable_struct_set(inventory.parts, _slot_key, []);
    }
    array_push(variable_struct_get(inventory.parts, _slot_key), _part_data);
    return true;
};

remove_part_from_inventory = function(_slot_key, _index) {
    if (variable_struct_exists(inventory.parts, _slot_key)) {
        var _arr = variable_struct_get(inventory.parts, _slot_key);
        if (_index >= 0 && _index < array_length(_arr)) {
            array_delete(_arr, _index, 1);
            return true;
        }
    }
    return false;
};

// Modular Mobile Suit Assembly & Combinations Bay Method (docs/13)
assemble_custom_mech = function(_name, _head_idx, _torso_idx, _arms_idx, _legs_idx, _bp_idx, _wp_idx) {
    var _pts = inventory.parts;
    if (_head_idx < 0 || _head_idx >= array_length(_pts.heads)) return false;
    if (_torso_idx < 0 || _torso_idx >= array_length(_pts.torsos)) return false;
    if (_arms_idx < 0 || _arms_idx >= array_length(_pts.arms)) return false;
    if (_legs_idx < 0 || _legs_idx >= array_length(_pts.legs)) return false;
    if (_bp_idx < 0 || _bp_idx >= array_length(_pts.backpacks)) return false;
    if (_wp_idx < 0 || _wp_idx >= array_length(_pts.weapons)) return false;

    var _hd = _pts.heads[_head_idx];
    var _tr = _pts.torsos[_torso_idx];
    var _am = _pts.arms[_arms_idx];
    var _lg = _pts.legs[_legs_idx];
    var _bp = _pts.backpacks[_bp_idx];
    var _wp = _pts.weapons[_wp_idx];

    // Compute Net Power Surplus
    var _power_draw = _hd.power_draw + _am.power_draw + _lg.power_draw + _bp.power_draw + _wp.power_draw;
    var _net_power = _tr.power_output - _power_draw;

    if (_net_power < 0) {
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("REACTOR OVERLOAD! Power draw (" + string(_power_draw) + " MW) exceeds Core (" + string(_tr.power_output) + " MW)!", c_red);
        }
        return false;
    }

    var _total_armor = _hd.armor + _tr.armor + _am.armor + _lg.armor + _bp.armor + _wp.armor;
    var _total_mass = _hd.mass + _tr.mass + _am.mass + _lg.mass + _bp.mass + _wp.mass;
    var _walk_speed = max(20, floor(_lg.base_speed * (1.0 - (_total_mass / 220.0))));
    var _boost_speed = _walk_speed + _bp.boost_bonus;
    var _combat_rating = floor((_total_armor / 5) + _wp.damage + (_boost_speed / 2) + (_net_power * 3));

    var _suit_name = (_name != "") ? _name : "Custom Vanguard Unit-" + string(array_length(inventory.deployable_mechs) + 1);

    var _weight_class = "MEDIUM MAINSTAY";
    if (_total_mass < 55) _weight_class = "LIGHT SKIRMISHER";
    else if (_total_mass >= 55 && _total_mass < 85) _weight_class = "MEDIUM MAINSTAY";
    else if (_total_mass >= 85 && _total_mass < 110) _weight_class = "HEAVY ASSAULT";
    else _weight_class = "SUPERHEAVY SIEGEBREAKER";

    var _new_mech = {
        id: "custom_mech_" + string(current_turn) + "_" + string(irandom(9999)),
        blueprint_id: "bp_player_custom",
        callsign: _suit_name,
        name: _suit_name,
        class: _weight_class,
        weight_class: _weight_class,
        assigned_pilot: "Unassigned",
        status: "READY",
        current_condition_pct: 1.0,
        armor_rating: _total_armor,
        power_output: _net_power,
        speed: _boost_speed,
        weight_tonnes: _total_mass,
        combat_rating: _combat_rating,
        components_summary: _hd.name + " // " + _tr.name + " // " + _am.name + " // " + _lg.name + " // " + _bp.name + " // " + _wp.name,
        part_composition: {
            head: _hd,
            torso: _tr,
            arms: _am,
            legs: _lg,
            backpack: _bp,
            weapon: _wp
        },
        spec_type: "COMMANDER_CUSTOM",
        combat_pedigree: {
            sorties_deployed: 0,
            sorties_survived: 0,
            confirmed_kills: 0,
            ace_kills: 0,
            damage_mitigated: 0,
            pedigree_rating: "UNTESTED",
            telemetry_bonus: 0.0
        }
    };

    if (instance_exists(obj_BlueprintManager)) {
        _new_mech = obj_BlueprintManager.apply_tuning_to_custom_mech(_new_mech);
    }
    array_push(inventory.deployable_mechs, _new_mech);

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("COMMISSIONED INTO HANGAR: " + _suit_name + " (Rating: " + string(_combat_rating) + ")!", c_lime);
    }
    return true;
};

get_blueprint = function(_blueprint_id) {
    if (instance_exists(obj_BlueprintManager)) return obj_BlueprintManager.get_blueprint(_blueprint_id);
    return undefined;
};

// 10b. Combat-Proven Pedigree & Arms Dealer Paradox (docs/25)
accumulate_combat_pedigree = function(_mech_id, _kills, _aces, _dmg_taken, _survived) {
    for (var m = 0; m < array_length(inventory.deployable_mechs); m++) {
        var _mech = inventory.deployable_mechs[m];
        if (_mech.id == _mech_id) {
            if (!variable_struct_exists(_mech, "combat_pedigree") || !is_struct(_mech.combat_pedigree)) {
                _mech.combat_pedigree = {
                    sorties_deployed: 0,
                    sorties_survived: 0,
                    confirmed_kills: 0,
                    ace_kills: 0,
                    damage_mitigated: 0,
                    pedigree_rating: "UNTESTED",
                    telemetry_bonus: 0.0
                };
            }
            var _cp = _mech.combat_pedigree;
            _cp.sorties_deployed += 1;
            if (_survived) _cp.sorties_survived += 1;
            _cp.confirmed_kills += _kills;
            _cp.ace_kills += _aces;
            _cp.damage_mitigated += _dmg_taken;

            var _pts = (_cp.sorties_survived * 1.5) + (_cp.confirmed_kills * 0.5) + (_cp.ace_kills * 3.0) + floor(_cp.damage_mitigated / 1000.0);
            _cp.telemetry_bonus = min(25.0, _pts);

            if (_pts >= 23) _cp.pedigree_rating = "LEGENDARY_VETERAN";
            else if (_pts >= 16) _cp.pedigree_rating = "BATTLE_HARDENED";
            else if (_pts >= 8) _cp.pedigree_rating = "COMBAT_PROVEN";
            else if (_pts >= 1) _cp.pedigree_rating = "FIELD_EVALUATED";
            else _cp.pedigree_rating = "UNTESTED";

            show_debug_message("[CombatPedigree] Updated " + _mech.name + " (" + _mech_id + ") -> " + _cp.pedigree_rating + " (+" + string(_cp.telemetry_bonus) + " pts)");
            return _cp;
        }
    }
    return undefined;
};

blueprint_weakness_bonuses = {};
register_exported_blueprint_weakness = function(_bp_id, _mech_name) {
    variable_struct_set(blueprint_weakness_bonuses, _bp_id, {
        blueprint_id: _bp_id,
        name: _mech_name,
        crit_bonus_pct: 15,
        armor_pierce_pct: 20,
        registered_turn: current_turn
    });
    show_debug_message("[BlueprintWeakness] Arms Dealer Paradox: PMC pilots gain +15% Crit / +20% AP vs " + _mech_name + " (" + _bp_id + ")!");
};

show_debug_message("[obj_GameManager] Initialized with calendar day " + string(current_cycle_day) + ", funds: " + string(funds) + " Cr.");

// 11. Periodic Table of Materials & Solar Mining Network Integration (docs/06, 14)
periodic_table_materials = [];
periodic_table_dict = {};

var _cand_pt = [
    "materials_periodic_table.json",
    "datafiles/materials_periodic_table.json",
    working_directory + "materials_periodic_table.json",
    working_directory + "datafiles/materials_periodic_table.json"
];
var _res_pt = "";
for (var p1 = 0; p1 < array_length(_cand_pt); p1++) {
    if (file_exists(_cand_pt[p1])) { _res_pt = _cand_pt[p1]; break; }
}
if (_res_pt != "") {
    try {
        var _buf_pt = buffer_load(_res_pt);
        var _json_pt = buffer_read(_buf_pt, buffer_string);
        buffer_delete(_buf_pt);
        var _pt_parsed = json_parse(_json_pt);
        if (variable_struct_exists(_pt_parsed, "materials")) {
            periodic_table_materials = _pt_parsed.materials;
            for (var m = 0; m < array_length(periodic_table_materials); m++) {
                var _mat = periodic_table_materials[m];
                variable_struct_set(periodic_table_dict, _mat.id, _mat);
                variable_struct_set(periodic_table_dict, _mat.symbol, _mat);
            }
            show_debug_message("[obj_GameManager] Loaded " + string(array_length(periodic_table_materials)) + " elements into Periodic Table Database.");
        }
    } catch (_ex_pt) {
        show_debug_message("[obj_GameManager] Warning loading periodic table: " + string(_ex_pt));
    }
}

var _cand_sn = [
    "solar_mining_nodes.json",
    "datafiles/solar_mining_nodes.json",
    working_directory + "solar_mining_nodes.json",
    working_directory + "datafiles/solar_mining_nodes.json"
];
var _res_sn = "";
for (var p2 = 0; p2 < array_length(_cand_sn); p2++) {
    if (file_exists(_cand_sn[p2])) { _res_sn = _cand_sn[p2]; break; }
}
if (_res_sn != "") {
    try {
        var _buf_sn = buffer_load(_res_sn);
        var _json_sn = buffer_read(_buf_sn, buffer_string);
        buffer_delete(_buf_sn);
        var _sn_parsed = json_parse(_json_sn);
        if (variable_struct_exists(_sn_parsed, "mining_nodes")) {
            var _sn_arr = _sn_parsed.mining_nodes;
            for (var sn = 0; sn < array_length(_sn_arr); sn++) {
                var _snode = _sn_arr[sn];
                _snode.current_storage = {};
                _snode.assigned_mech_id = "Unassigned";
                _snode.assigned_pilot_name = "Unassigned";
                _snode.status = "UNCLAIMED";
                _snode.threat_level_pct = 25;

                var _res_keys = variable_struct_get_names(_snode.primary_resources);
                _snode.primary_yield = (array_length(_res_keys) > 0) ? _res_keys[0] : "mat_tungsten";
                _snode.secondary_yield = (array_length(_res_keys) > 1) ? _res_keys[1] : "none";
                _snode.yield_rate_primary = max(2, floor(_snode.base_daily_yield_kg / 1000.0));
                _snode.yield_rate_secondary = max(1, floor(_snode.base_daily_yield_kg / 2000.0));

                array_push(nodes, _snode);
            }
            show_debug_message("[obj_GameManager] Integrated " + string(array_length(_sn_arr)) + " Solar System mining nodes across 5 planetary spheres.");
        }
    } catch (_ex_sn) {
        show_debug_message("[obj_GameManager] Warning loading solar mining nodes: " + string(_ex_sn));
    }
}

get_material_data = function(_mat_id) {
    if (variable_struct_exists(periodic_table_dict, _mat_id)) {
        return (variable_struct_exists(periodic_table_dict, _mat_id) ? variable_struct_get(periodic_table_dict, _mat_id) : undefined);
    }
    return undefined;
};

get_all_materials = function() {
    return periodic_table_materials;
};

// 12. Pre-War Flagship Navigation, 8-Division Upgrades & Master Protocols (Docs 23 & 24)
flagship_travel_to = function(_destination_sphere) {
    if (_destination_sphere == flagship.current_sphere) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("ALREADY STATIONED IN " + string_upper(_destination_sphere) + "!", c_yellow);
        return false;
    }
    if (flagship.transit_turns_left > 0) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("TRANSIT IN PROGRESS: " + string(flagship.transit_turns_left) + " turns left!", c_yellow);
        return false;
    }

    var _spheres = ["Earth Sphere", "Martian Sphere", "Asteroid Belt", "Jovian Outer Sphere", "Saturnian Outer Sphere", "Deep Solar Frontier"];
    var _i1 = 2;
    var _i2 = 2;
    for (var s = 0; s < array_length(_spheres); s++) {
        if (_spheres[s] == flagship.current_sphere) _i1 = s;
        if (_spheres[s] == _destination_sphere) _i2 = s;
    }
    var _dist = abs(_i1 - _i2);

    // Speed progression: T1=max 3 turns, T2=max 2 turns, T3=1 turn, T4=1 turn, T5 or Protocol C=0 turns (Instant Tachyon Fold Warp)
    var _prop_tier = flagship.upgrades.propulsion_tier;
    var _transit_turns = 1;
    if (_prop_tier == 1) {
        _transit_turns = max(1, min(3, _dist));
    } else if (_prop_tier == 2) {
        _transit_turns = max(1, min(2, _dist));
    } else if (_prop_tier == 3 || _prop_tier == 4) {
        _transit_turns = 1;
    } else if (_prop_tier >= 5 || flagship.specialization_protocol == "shadow_panopticon") {
        _transit_turns = 0;
    }

    if (_transit_turns == 0) {
        flagship.current_sphere = _destination_sphere;
        flagship.destination_sphere = "";
        flagship.transit_turns_left = 0;
        array_push(last_turn_events, "* TACHYON FOLD WARP: USN-X Hephaestus executed zero-turn transit to " + _destination_sphere + "!");
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("TACHYON FOLD INSTANT ARRIVAL: " + string_upper(_destination_sphere) + "!", c_fuchsia);
        }
        return true;
    }

    flagship.destination_sphere = _destination_sphere;
    flagship.transit_turns_left = _transit_turns;
    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("TRANSIT DRIVE ENGAGED: En route to " + _destination_sphere + " (" + string(flagship.transit_turns_left) + " turns)!", c_aqua);
    }
    return true;
};

flagship_set_specialization = function(_protocol) {
    var _t3_count = 0;
    var _tracks = ["fabrication_tier", "mining_tier", "defense_tier", "weapons_tier", "propulsion_tier", "pilot_suite_tier", "sigint_tier", "command_tier"];
    for (var t = 0; t < array_length(_tracks); t++) {
        if ((variable_struct_get(flagship.upgrades, _tracks[t]) ?? 1) >= 3) _t3_count++;
    }
    if (_t3_count < 4) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("LOCKED: Requires at least 4 Flagship Divisions at Tier 3+ (Current: " + string(_t3_count) + "/4)!", c_yellow);
        return false;
    }

    flagship.specialization_protocol = _protocol;
    var _proto_name = (_protocol == "forge_titan") ? "INDUSTRIAL FORGE TITAN" :
                      ((_protocol == "siege_fortress") ? "ORBITAL SIEGE FORTRESS" : "SHADOW PANOPTICON");

    if (_protocol == "siege_fortress") {
        flagship.hull_max_hp = 65000;
        flagship.hull_hp = min(flagship.hull_max_hp, flagship.hull_hp + 25000);
    }

    array_push(last_turn_events, "* FLAGSHIP DOCTRINE RATIFIED: USN-X Hephaestus initialized " + _proto_name + " protocol!");
    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("FLAGSHIP PROTOCOL RATIFIED: " + _proto_name + "!", c_lime);
    }
    return true;
};

flagship_upgrade = function(_track) {
    var _cur_tier = variable_struct_get(flagship.upgrades, _track) ?? 1;
    if (_cur_tier >= 5) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("DIVISION AT MAXIMUM APEX ARCHEOTECH TIER (TIER 5)!", c_yellow);
        return false;
    }

    var _next_tier = _cur_tier + 1;
    var _cost_cr = 0;
    var _req_alloy = "";
    var _req_qty = 5;

    if (_track == "fabrication_tier") {
        if (_next_tier == 2) { _cost_cr = 250000; _req_alloy = "alloy_vanguard_comp"; }
        else if (_next_tier == 3) { _cost_cr = 600000; _req_alloy = "alloy_aerosteel_flux"; }
        else if (_next_tier == 4) { _cost_cr = 1500000; _req_alloy = "alloy_adamantine_carbide"; }
        else if (_next_tier == 5) { _cost_cr = 3500000; _req_alloy = "alloy_reactive_damascus"; }
    } else if (_track == "mining_tier") {
        if (_next_tier == 2) { _cost_cr = 200000; _req_alloy = "alloy_vanguard_comp"; }
        else if (_next_tier == 3) { _cost_cr = 500000; _req_alloy = "alloy_hyperion_matrix"; }
        else if (_next_tier == 4) { _cost_cr = 1200000; _req_alloy = "alloy_adamantine_carbide"; }
        else if (_next_tier == 5) { _cost_cr = 3000000; _req_alloy = "alloy_chobham_reactive"; }
    } else if (_track == "defense_tier") {
        if (_next_tier == 2) { _cost_cr = 180000; _req_alloy = "alloy_vanguard_comp"; }
        else if (_next_tier == 3) { _cost_cr = 450000; _req_alloy = "alloy_hyperion_matrix"; }
        else if (_next_tier == 4) { _cost_cr = 1100000; _req_alloy = "alloy_adamantine_carbide"; }
        else if (_next_tier == 5) { _cost_cr = 2800000; _req_alloy = "alloy_chobham_reactive"; }
    } else if (_track == "weapons_tier") {
        if (_next_tier == 2) { _cost_cr = 350000; _req_alloy = "alloy_vanguard_comp"; }
        else if (_next_tier == 3) { _cost_cr = 800000; _req_alloy = "alloy_aerosteel_flux"; }
        else if (_next_tier == 4) { _cost_cr = 2000000; _req_alloy = "alloy_adamantine_carbide"; }
        else if (_next_tier == 5) { _cost_cr = 4500000; _req_alloy = "alloy_reactive_damascus"; }
    } else if (_track == "propulsion_tier") {
        if (_next_tier == 2) { _cost_cr = 220000; _req_alloy = "alloy_vanguard_comp"; }
        else if (_next_tier == 3) { _cost_cr = 550000; _req_alloy = "alloy_aerosteel_flux"; }
        else if (_next_tier == 4) { _cost_cr = 1300000; _req_alloy = "alloy_adamantine_carbide"; }
        else if (_next_tier == 5) { _cost_cr = 3200000; _req_alloy = "alloy_reactive_damascus"; }
    } else if (_track == "pilot_suite_tier") {
        if (_next_tier == 2) { _cost_cr = 190000; _req_alloy = "alloy_vanguard_comp"; }
        else if (_next_tier == 3) { _cost_cr = 480000; _req_alloy = "alloy_hyperion_matrix"; }
        else if (_next_tier == 4) { _cost_cr = 1250000; _req_alloy = "alloy_adamantine_carbide"; }
        else if (_next_tier == 5) { _cost_cr = 2900000; _req_alloy = "alloy_chobham_reactive"; }
    } else if (_track == "sigint_tier") {
        if (_next_tier == 2) { _cost_cr = 210000; _req_alloy = "alloy_vanguard_comp"; }
        else if (_next_tier == 3) { _cost_cr = 520000; _req_alloy = "alloy_hyperion_matrix"; }
        else if (_next_tier == 4) { _cost_cr = 1400000; _req_alloy = "alloy_adamantine_carbide"; }
        else if (_next_tier == 5) { _cost_cr = 3400000; _req_alloy = "alloy_reactive_damascus"; }
    } else if (_track == "command_tier") {
        if (_next_tier == 2) { _cost_cr = 260000; _req_alloy = "alloy_vanguard_comp"; }
        else if (_next_tier == 3) { _cost_cr = 650000; _req_alloy = "alloy_aerosteel_flux"; }
        else if (_next_tier == 4) { _cost_cr = 1600000; _req_alloy = "alloy_adamantine_carbide"; }
        else if (_next_tier == 5) { _cost_cr = 4000000; _req_alloy = "alloy_reactive_damascus"; }
    }

    if (funds < _cost_cr) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT FUNDS: Requires " + string(_cost_cr) + " Cr!", c_red);
        return false;
    }
    if (_req_alloy != "" && get_alloy(_req_alloy) < _req_qty) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT ALLOY: Requires " + string(_req_qty) + "x " + _req_alloy + "!", c_red);
        return false;
    }

    funds -= _cost_cr;
    if (_req_alloy != "") spend_alloy(_req_alloy, _req_qty);

    variable_struct_set(flagship.upgrades, _track, _next_tier);

    if (_track == "defense_tier") {
        var _hulls = [8500, 12000, 18000, 26000, 40000];
        flagship.hull_max_hp = _hulls[_next_tier - 1];
        flagship.hull_hp = flagship.hull_max_hp;
    }
    if (_track == "weapons_tier" && _next_tier >= 2) {
        flagship.orbital_strike_available = true;
    }

    var _track_name = (_track == "fabrication_tier") ? "Fabrication Core" :
                      ((_track == "mining_tier") ? "Mining Sills & Refinery" :
                      ((_track == "defense_tier") ? "Hull Defenses & CIWS" :
                      ((_track == "weapons_tier") ? "Spinal Artillery & Strikes" :
                      ((_track == "propulsion_tier") ? "Tachyon FTL Propulsion" :
                      ((_track == "pilot_suite_tier") ? "Neural Holodecks & Med-Bay" :
                      ((_track == "sigint_tier") ? "SIGINT & EW Panopticon" : "Strategic Bridge & CIC"))))));

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("DREADNOUGHT UPGRADE RATIFIED! " + _track_name + " upgraded to Tier " + string(_next_tier) + "!", c_lime);
    }
    return true;
};

launch_corporate_sabotage = function(_corp_id) {
    if (!variable_struct_exists(rival_corporations, _corp_id)) return false;
    var _corp = variable_struct_get(rival_corporations, _corp_id);
    var _cost = 50000;

    if (funds < _cost) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT FUNDS: Black-ops sabotage costs " + string(_cost) + " Cr!", c_red);
        return false;
    }

    funds -= _cost;
    _corp.hostility_pct = min(100, _corp.hostility_pct + 15);
    var _shift = min(_corp.market_share_pct, 4);
    _corp.market_share_pct -= _shift;
    pmc_market_share_pct = min(60, pmc_market_share_pct + _shift);

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("CORPORATE SABOTAGE SUCCESS: Siphoned " + string(_shift) + "% market share from " + _corp.ticker + " (-50,000 Cr)!", c_orange);
    }
    return true;
};

evaluate_flagship_turn = function() {
    // 1. Orbital Transit countdown
    if (flagship.transit_turns_left > 0) {
        flagship.transit_turns_left -= 1;
        if (flagship.transit_turns_left <= 0) {
            flagship.current_sphere = flagship.destination_sphere;
            flagship.destination_sphere = "";
            array_push(last_turn_events, "* DREADNOUGHT ARRIVAL: USN-X Hephaestus established high orbit over " + flagship.current_sphere + " (Mining yield & fire support online).");
            if (instance_exists(obj_HQTerminal)) {
                obj_HQTerminal.show_toast("FLAGSHIP ARRIVED IN " + string_upper(flagship.current_sphere) + "!", c_aqua);
            }
        }
    }

    // 2. Orbital Strike Weapon Cooldown
    if (flagship.upgrades.weapons_tier >= 2) {
        if (flagship.orbital_strike_cooldown > 0) {
            flagship.orbital_strike_cooldown -= 1;
            if (flagship.orbital_strike_cooldown <= 0) {
                flagship.orbital_strike_available = true;
            }
        }
    }

    // 3. Mining Tier 5: Autonomous Planetary Siphon Harvester Array (+15kg raw materials/turn)
    if (flagship.upgrades.mining_tier >= 5) {
        add_raw_material("mat_tungsten", 6);
        add_raw_material("mat_silica_carb", 5);
        add_raw_material("mat_tritium", 2);
        add_raw_material("mat_syn_flux", 2);
        array_push(last_turn_events, "* HARVEST ARRAY: USN-X Hephaestus siphon drones gathered +15kg raw minerals into fleet cargo.");
    }

    // 4. Pilot Suite Tier 3-5: Neural Holodeck Passive Training & Trauma Healing
    if (flagship.upgrades.pilot_suite_tier >= 3 && variable_struct_exists(facilities, "roster_pilots")) {
        for (var p = 0; p < array_length(facilities.roster_pilots); p++) {
            var _plt = facilities.roster_pilots[p];
            if (is_struct(_plt)) {
                if (variable_struct_exists(_plt, "stat_combat")) _plt.stat_combat = min(99, _plt.stat_combat + 1);
                if (flagship.upgrades.pilot_suite_tier >= 5) {
                    if (variable_struct_exists(_plt, "trauma_state")) _plt.trauma_state = "focused_master";
                    if (variable_struct_exists(_plt, "morale")) _plt.morale = 100;
                }
            }
        }
    }

    // 5. SIGINT Tier 5 / Shadow Panopticon: Intercept & Siphon Market Share
    var _siphon_freq = (flagship.specialization_protocol == "shadow_panopticon") ? 4 : 5;
    if ((flagship.upgrades.sigint_tier >= 5 || flagship.specialization_protocol == "shadow_panopticon") && (turn_count % _siphon_freq == 0)) {
        var _highest_corp = rival_corporations.corp_vhi;
        if (rival_corporations.corp_aod.market_share_pct > _highest_corp.market_share_pct) _highest_corp = rival_corporations.corp_aod;
        if (rival_corporations.corp_rust.market_share_pct > _highest_corp.market_share_pct) _highest_corp = rival_corporations.corp_rust;
        if (rival_corporations.corp_hats.market_share_pct > _highest_corp.market_share_pct) _highest_corp = rival_corporations.corp_hats;
        var _sip_pct = (flagship.specialization_protocol == "shadow_panopticon") ? 2 : 1;
        if (_highest_corp.market_share_pct > 5) {
            _highest_corp.market_share_pct -= _sip_pct;
            pmc_market_share_pct = min(80, pmc_market_share_pct + _sip_pct);
            array_push(last_turn_events, "* SIGINT EXPLOIT: Panopticon array siphoned +" + string(_sip_pct) + "% market share from " + _highest_corp.ticker + ".");
        }
    }

    // 6. Dynamic Rival Corporate Market Evolution
    if (instance_exists(obj_FactionManager)) {
        var _fm = obj_FactionManager;
        if (_fm.mass_production_contracts.faction_a.replaced && rival_corporations.corp_vhi.market_share_pct > 15) {
            rival_corporations.corp_vhi.market_share_pct -= 1;
            pmc_market_share_pct = min(75, pmc_market_share_pct + 1);
            rival_corporations.corp_vhi.hostility_pct = min(100, rival_corporations.corp_vhi.hostility_pct + 1);
        }
        if (_fm.mass_production_contracts.faction_b.replaced && rival_corporations.corp_aod.market_share_pct > 15) {
            rival_corporations.corp_aod.market_share_pct -= 1;
            pmc_market_share_pct = min(75, pmc_market_share_pct + 1);
            rival_corporations.corp_aod.hostility_pct = min(100, rival_corporations.corp_aod.hostility_pct + 1);
        }
        if (_fm.mass_production_contracts.faction_c.replaced && rival_corporations.corp_rust.market_share_pct > 10) {
            rival_corporations.corp_rust.market_share_pct -= 1;
            pmc_market_share_pct = min(75, pmc_market_share_pct + 1);
            rival_corporations.corp_rust.hostility_pct = min(100, rival_corporations.corp_rust.hostility_pct + 1);
        }
        if (_fm.mass_production_contracts.faction_d.replaced && rival_corporations.corp_hats.market_share_pct > 10) {
            rival_corporations.corp_hats.market_share_pct -= 1;
            pmc_market_share_pct = min(75, pmc_market_share_pct + 1);
            rival_corporations.corp_hats.hostility_pct = min(100, rival_corporations.corp_hats.hostility_pct + 1);
        }
    }
};

get_mining_nodes_by_sphere = function(_sphere) {
    if (_sphere == "all" || _sphere == "") return nodes;
    var _filtered = [];
    for (var i = 0; i < array_length(nodes); i++) {
        var _nd = nodes[i];
        if (variable_struct_exists(_nd, "sphere") && _nd.sphere == _sphere) {
            array_push(_filtered, _nd);
        }
    }
    return _filtered;
};

// =============================================================================
// 12. Nemesis System & Pilot Relational Roster Integration (Document 19)
// =============================================================================
player_pilots = facilities.roster_pilots;

populate_market_from_nemesis = function() {
    if (!instance_exists(obj_NemesisManager)) return;
    var _nem = instance_find(obj_NemesisManager, 0);
    if (_nem == noone) return;
    if (!variable_instance_exists(_nem, "get_faction_pilots") || !variable_instance_exists(_nem, "characters_map")) return;
    var _hire_candidates = [];

    var _factions = ["faction_terran", "faction_colony", "faction_syndicate", "faction_zaibatsu", "independent"];
    for (var f = 0; f < array_length(_factions); f++) {
        var _pilots = _nem.get_faction_pilots(_factions[f], true);
        var _take = min(2, array_length(_pilots));
        for (var p = 0; p < _take; p++) {
            var _c = _pilots[p];
            var _disc = scr_get_friendship_referral_discount(_c.id);
            var _cost = max(10000, floor(_c.hiring_cost_cr * (1.0 - _disc)));
            var _cand = {
                id: _c.id,
                name: _c.name,
                callsign: _c.callsign,
                character_id: _c.id,
                background: _c.role + (_c.active_defection_hook != "" ? " [" + _c.active_defection_hook + "]" : ""),
                combat_stat: _c.tier * 3,
                tactics_stat: _c.tier * 2 + 3,
                salary_daily: max(150, floor(_c.salary_per_cycle_cr / 30.0)),
                signing_bonus: _cost,
                referral_discount: _disc,
                love_interest_info: _c.love_interest,
                friendship_info: _c.friendships,
                tier: _c.tier,
                preferred_chassis: _c.preferred_chassis
            };
            array_push(_hire_candidates, _cand);
        }
    }

    if (array_length(_hire_candidates) > 0) {
        facilities.available_hire_pilots = _hire_candidates;
        show_debug_message("[obj_GameManager] Populated hiring market with " + string(array_length(_hire_candidates)) + " pilots from obj_NemesisManager.");
    }
};

// Attempt initial population if NemesisManager is already instantiated and initialized
if (instance_exists(obj_NemesisManager)) {
    var _nem_chk = instance_find(obj_NemesisManager, 0);
    if (_nem_chk != noone && variable_instance_exists(_nem_chk, "get_faction_pilots")) {
        populate_market_from_nemesis();
    }
}


// Initialize Hearts of Iron IV style Technology Research Tree
scr_research_init();

// Transition from initialization room to the main HQ Command Deck
if (room == rm_init) {
    show_debug_message("[obj_GameManager] Core initialization complete in rm_init. Transitioning to rm_hq_terminal...");
    room_goto(rm_hq_terminal);
}
