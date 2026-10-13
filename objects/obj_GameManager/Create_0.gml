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
funds = 750000;              // Current Credits (Cr)
escrow_funds = 120000;       // Escrow withheld for pending operations

// 3. Turn-Based Strategic Simulation State
current_turn = 45;           // Strategic Turn Counter
current_cycle_year = 214;    // Standard Galactic Calendar Year
current_cycle_day = 45;      // Day within current operational cycle
last_turn_events = [];       // Historical log of transactions and developments from the latest turn
show_turn_report = false;    // Modal toggle for turn transition summary
time_speed = 0;              // Preserved as 0 (turn-based architecture)

// 3b. Career Legacy & Sandbox Endgame State (docs/12)
career_summary = undefined;  // Sid Meier's Pirates style retirement dossier struct
total_sorties_won = 0;       // Total successful PMC sorties and sector conquests

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
    current_sphere: "Asteroid Belt",
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

// 4c. Rival Corporate Mobile Suit Manufacturers (Doc 23)
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
        hq_location: "Geneva Orbital Ring (Earth)"
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
        hq_location: "Galileo Aerospace Hub (Ganymede)"
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
        hq_location: "Asteroid 433 Eros / Rust-Pike"
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
        hq_location: "Neo-Tokyo Orbital Silo (Mars)"
    }
};
pmc_market_share_pct = 5;

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
            combat_rating: 480
        },
        {
            id: "unit_ironclad_02",
            blueprint_id: "bp_ms_ironclad_07",
            callsign: "IRON-02 'JUGGERNAUT'",
            name: "GHA-07 Ironclad",
            class: "Heavy Assault",
            assigned_pilot: "Unassigned",
            status: "READY", // Available for sorties
            current_condition_pct: 1.0,
            armor_rating: 850,
            power_output: 12,
            speed: 45,
            combat_rating: 480
        }
    ]
};

// 6. Base Facility Upgrades & Roster (docs/07_base_management.md)
facilities = {
    crucible_tier: 1,             // Tier 1: Max 3000°C, 2000 PSI; Tier 2: Max 6000°C, 10,000 PSI
    containment_shielding: false, // Prevents catastrophic lab damage on breach
    assembly_lines: 1,            // Number of concurrent manufacturing bays (up to 4)
    active_fabrications: [
        {
            mech_blueprint: "bp_ms_ironclad_07",
            name: "GHA-07 Ironclad Batch-3",
            days_remaining: 6,
            total_days: 12
        }
    ],
    roster_pilots: [
        { name: "Lt. Marcus Vance", callsign: "VANGUARD-1", accuracy: 88, reflexes: 75, morale: 95, salary_daily: 220, is_deployed: true, status: "ACTIVE", recovery_days: 0, kills: 3, sorties: 5 },
        { name: "Sgt. Sarah Cole", callsign: "DEATHBLOW", accuracy: 82, reflexes: 79, morale: 88, salary_daily: 190, is_deployed: false, status: "ACTIVE", recovery_days: 0, kills: 1, sorties: 2 }
    ],
    pmc_memorial_wall: [],
    roster_engineers: [
        { name: "Dr. Elena Rostova", role: "Lead Metallurgist", metallurgy: 82, precision: 78, salary_daily: 180 },
        { name: "Master Chief Travis", role: "Hydraulics Specialist", metallurgy: 70, precision: 86, salary_daily: 160 }
    ],
    available_hire_pilots: [
        { name: "Lt. Marcus 'Breaker' Cole", callsign: "BREAKER", faction: "faction_terran", portrait: spr_portrait_cole, accuracy: 78, reflexes: 42, morale: 70, salary_daily: 250, bonus_hire: 45000, traits: "Heavy Ordnance (+20% Kinetic DMG)", bio: "Trench warfare veteran who refused to shell civilian domes." },
        { name: "Ensign Elena Rostova", callsign: "DEAD-EYE", faction: "faction_terran", portrait: spr_portrait_vance, accuracy: 92, reflexes: 55, morale: 80, salary_daily: 220, bonus_hire: 38000, traits: "Retinal Implants (+15% Critical Chance)", bio: "Elite sniper with cybernetic targeting implants." },
        { name: "Sorren 'Ghost' Lin", callsign: "GHOST", faction: "faction_colony", portrait: spr_portrait_sorren, accuracy: 85, reflexes: 92, morale: 85, salary_daily: 280, bonus_hire: 52000, traits: "Vernier Ace (+25% Evasion)", bio: "Quiet Jovian interceptor ace obsessed with zero-G speed." },
        { name: "Kira Dahl", callsign: "SPECTER", faction: "faction_colony", portrait: spr_portrait_sorren, accuracy: 70, reflexes: 80, morale: 90, salary_daily: 190, bonus_hire: 34000, traits: "ECM Pulse (-20% Enemy Hit)", bio: "Electronic warfare specialist and sensor jammer prodigy." },
        { name: "Nadia 'Spark' Ortiz", callsign: "SPARK", faction: "faction_syndicate", portrait: spr_portrait_nadia, accuracy: 72, reflexes: 65, morale: 95, salary_daily: 170, bonus_hire: 31000, traits: "Field Rig (+25% Scrap Salvage)", bio: "Asteroid belt mechanic who can patch hulls under direct mortar fire." },
        { name: "'Jackal' Jax Vance", callsign: "JACKAL", faction: "faction_syndicate", portrait: spr_portrait_cole, accuracy: 80, reflexes: 78, morale: 65, salary_daily: 230, bonus_hire: 41000, traits: "Harpoon Tether (Pins Mechs)", bio: "Mercenary skirmisher fighting purely for cold credits." },
        { name: "Null-07 (Ren)", callsign: "NULL", faction: "faction_zaibatsu", portrait: spr_portrait_null07, accuracy: 96, reflexes: 88, morale: 50, salary_daily: 320, bonus_hire: 65000, traits: "Neural Link (+2 Action in 1st Turn)", bio: "Escaped Zaibatsu test subject with spinal neural-jack implants." },
        { name: "Maya 'Kestrel' Zhao", callsign: "KESTREL", faction: "faction_zaibatsu", portrait: spr_portrait_nadia, accuracy: 84, reflexes: 75, morale: 85, salary_daily: 240, bonus_hire: 46000, traits: "Sub-Drone Swarm Support", bio: "Former corporate security ace who bought out her debt contract." }
    ]
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
            var _file = file_text_open_read("narrative_events.json");
            var _str = "";
            while (!file_text_eof(_file)) _str += file_text_readln(_file);
            file_text_close(_file);
            var _data = json_parse(_str);
            if (is_struct(_data) && is_array(_data[$ "events"])) {
                narrative_events_list = _data.events;
                show_debug_message("[obj_GameManager] Loaded " + string(array_length(narrative_events_list)) + " narrative events.");
            }
        }
    } catch (_ex) {
        show_debug_message("[obj_GameManager] Exception loading narrative events: " + string(_ex));
    }
};
load_narrative_events();

trigger_event_by_id = function(_event_id) {
    for (var e = 0; e < array_length(narrative_events_list); e++) {
        if (narrative_events_list[e][$ "id"] == _event_id) {
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

// 9. Daily Simulation Advancement Method (docs/01, 04, 06, 07)
end_turn = function() {
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
    var _daily_maintenance = 150 + (facilities.assembly_lines - 1) * 75;
    var _net_flow = _daily_retainer - _daily_salaries - _daily_maintenance;
    funds += _net_flow;
    array_push(last_turn_events, "* Fiscal Ledger: Net Cashflow " + (_net_flow >= 0 ? "+" : "") + string(_net_flow) + " Cr (Treasury: " + string(funds) + " Cr)");

    // Bankruptcy warning
    if (funds < 0) {
        array_push(last_turn_events, "! FISCAL CRISIS: Company operational accounts are currently overdrawn!");
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("FINANCIAL CRISIS: TREASURY DEFICIT!", c_red);
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
                _node.current_storage[$ _node.primary_yield] = (_node.current_storage[$ _node.primary_yield] ?? 0) + _yield_p;
            }
            if (_node.secondary_yield != "none") {
                _node.current_storage[$ _node.secondary_yield] = (_node.current_storage[$ _node.secondary_yield] ?? 0) + _yield_s;
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
            array_push(inventory.deployable_mechs, {
                id: "unit_ironclad_" + string(array_length(inventory.deployable_mechs) + 1),
                blueprint_id: _fab.mech_blueprint,
                callsign: _fab.name,
                assigned_pilot: "Unassigned",
                status: "READY",
                current_condition_pct: 1.0
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
                    funds -= (_cnt[$ "penalty_credits"] ?? 50000);
                    obj_FactionManager.modify_standing(_cnt.faction, _cnt[$ "reputation_penalty"] ?? -20);
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
        if ((_plt[$ "status"] ?? "ACTIVE") == "HOSPITALIZED") {
            _plt.recovery_days--;
            if (_plt.recovery_days <= 0) {
                _plt.status = "ACTIVE";
                _plt.is_deployed = false;
                array_push(last_turn_events, "* MEDICAL CLEARANCE: " + _plt.name + " discharged from infirmary -> Ready for Sortie!");
                if (instance_exists(obj_HQTerminal)) {
                    obj_HQTerminal.show_toast("PILOT RECOVERED: " + _plt.name + " cleared for active sortie!", c_lime);
                }
            } else {
                array_push(last_turn_events, "* Infirmary: " + _plt.name + " in critical recovery (" + string(_plt.recovery_days) + " turns left)");
            }
        }
    }

    // 5b. Daily Sovereign Territory Tribute & Mass-Production Royalties (docs/12)
    if (instance_exists(obj_FactionManager)) {
        var _fm = obj_FactionManager;
        var _pmc_pct = _fm.territory_control.pmc_pct;
        if (_pmc_pct > 0) {
            var _tribute = _pmc_pct * 3500;
            funds += _tribute;
            array_push(last_turn_events, "* Sovereign Dominion Tribute: +" + string(_tribute) + " Cr from " + string(_pmc_pct) + "% governed territory.");
        }

        var _f_keys = ["faction_a", "faction_b", "faction_c", "faction_d"];
        for (var fk = 0; fk < 4; fk++) {
            var _fid = _f_keys[fk];
            if (variable_struct_exists(_fm.mass_production_contracts, _fid)) {
                var _mp = _fm.mass_production_contracts[$ _fid];
                if (_mp.replaced) {
                    var _royalty = _mp.royalty_per_turn;
                    funds += _royalty;
                    _mp.cumulative_royalties_paid += _royalty;
                    array_push(last_turn_events, "* Mass-Production Royalty (" + _mp.faction_name + "): +" + string(_royalty) + " Cr for licensed " + _mp.replacement_name + " lines.");
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

    // 7. Random Narrative Event Roll (8% chance each turn if none active)
    if (is_undefined(active_event_popup) && array_length(narrative_events_list) > 0) {
        if (random(100) < 8.0) {
            var _rand_idx = irandom(array_length(narrative_events_list) - 1);
            trigger_event_by_id(narrative_events_list[_rand_idx].id);
        }
    }

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("ADVANCED TO TURN " + string(current_turn) + " (Y" + string(current_cycle_year) + " D" + string(current_cycle_day) + ")", c_aqua);
    }
};

step_day = end_turn; // backwards compatible alias

// 9c. Sid Meier's Pirates-Style Career Retirement & Legacy Assessment (docs/12)
retire_career = function() {
    var _mat_val = (inventory.raw_materials.mat_tungsten * 400) + 
                   (inventory.raw_materials.mat_silica_carb * 150) + 
                   (inventory.raw_materials.mat_tritium * 1200) + 
                   (inventory.raw_materials.mat_syn_flux * 800);
    var _facility_val = (facilities.hangar_bays * 250000) + (facilities.lab_tier * 400000) + (facilities.foundry_crucibles * 300000);
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
                var _mp = obj_FactionManager.mass_production_contracts[$ _fid];
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

    var _total_score = _score_wealth + _score_territory + _score_monopoly + _score_guild + _score_tech + _score_conquest;

    // Determine Dynamic Title & Historical Epilogue Chronicle (docs/12)
    var _title = "Hardened Mercenary Commander";
    var _epilogue = "You served through the crucible of the mecha wars with distinction, forging an enduring mercenary name across the stars.";

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
    var _cur_alloy = inventory.alloys[$ "alloy_vanguard_comp"] ?? 0;
    var _cur_tungsten = inventory.raw_materials[$ "mat_tungsten"] ?? 0;
    if (_cur_alloy < _alloys_req || _cur_tungsten < _tungsten_req) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT MATERIALS! Requires " + string(_alloys_req) + " Vanguard Alloys & " + string(_tungsten_req) + " Tungsten", c_red);
        return false;
    }
    // Deduct
    spend_funds(_cost_cr);
    inventory.alloys[$ "alloy_vanguard_comp"] = _cur_alloy - _alloys_req;
    inventory.raw_materials[$ "mat_tungsten"] = _cur_tungsten - _tungsten_req;
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
            var _amt = _node.current_storage[$ _key] ?? 0;
            if (_amt > 0) {
                add_raw_material(_key, _amt);
                _node.current_storage[$ _key] = 0;
            }
        }
        return true;
    }
    return false;
};

// Material & Treasury Management Methods
add_funds = function(_amount) { if (_amount > 0) { funds += _amount; return true; } return false; };
spend_funds = function(_amount) { if (_amount > 0 && funds >= _amount) { funds -= _amount; return true; } return false; };

get_raw_material = function(_mat_id) { return inventory.raw_materials[$ _mat_id] ?? 0; };
add_raw_material = function(_mat_id, _quantity) {
    if (!variable_struct_exists(inventory.raw_materials, _mat_id)) inventory.raw_materials[$ _mat_id] = 0;
    inventory.raw_materials[$ _mat_id] += _quantity;
    return inventory.raw_materials[$ _mat_id];
};
spend_raw_material = function(_mat_id, _quantity) {
    var _cur = get_raw_material(_mat_id);
    if (_cur >= _quantity) {
        inventory.raw_materials[$ _mat_id] -= _quantity;
        return true;
    }
    return false;
};

add_alloy = function(_alloy_key, _quantity) {
    if (!variable_struct_exists(inventory.alloys, _alloy_key)) inventory.alloys[$ _alloy_key] = 0;
    inventory.alloys[$ _alloy_key] += _quantity;
    return inventory.alloys[$ _alloy_key];
};
get_alloy = function(_alloy_key) { return inventory.alloys[$ _alloy_key] ?? 0; };
spend_alloy = function(_alloy_key, _quantity) {
    var _cur = get_alloy(_alloy_key);
    if (_cur >= _quantity) {
        inventory.alloys[$ _alloy_key] -= _quantity;
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
        inventory.parts[$ _slot_key] = [];
    }
    array_push(inventory.parts[$ _slot_key], _part_data);

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("PART FORGED: " + _part_data.name + " added to inventory!", c_lime);
    }
    return true;
};

add_part_to_inventory = function(_part_data) {
    if (!is_struct(_part_data)) return false;
    var _slot_key = _part_data[$ "slot"] ?? "heads";
    if (!variable_struct_exists(inventory.parts, _slot_key)) {
        inventory.parts[$ _slot_key] = [];
    }
    array_push(inventory.parts[$ _slot_key], _part_data);
    return true;
};

remove_part_from_inventory = function(_slot_key, _index) {
    if (variable_struct_exists(inventory.parts, _slot_key)) {
        var _arr = inventory.parts[$ _slot_key];
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

    var _new_mech = {
        id: "custom_mech_" + string(current_turn) + "_" + string(irandom(9999)),
        blueprint_id: "bp_player_custom",
        callsign: _suit_name,
        name: _suit_name,
        class: "Custom Modular Unit",
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
        var _f_pt = file_text_open_read(_res_pt);
        var _json_pt = "";
        while (!file_text_eof(_f_pt)) {
            _json_pt += file_text_readln(_f_pt);
        }
        file_text_close(_f_pt);
        var _pt_parsed = json_parse(_json_pt);
        if (variable_struct_exists(_pt_parsed, "materials")) {
            periodic_table_materials = _pt_parsed.materials;
            for (var m = 0; m < array_length(periodic_table_materials); m++) {
                var _mat = periodic_table_materials[m];
                periodic_table_dict[$ _mat.id] = _mat;
                periodic_table_dict[$ _mat.symbol] = _mat;
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
        var _f_sn = file_text_open_read(_res_sn);
        var _json_sn = "";
        while (!file_text_eof(_f_sn)) {
            _json_sn += file_text_readln(_f_sn);
        }
        file_text_close(_f_sn);
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
        return periodic_table_dict[$ _mat_id];
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
        if ((flagship.upgrades[$ _tracks[t]] ?? 1) >= 3) _t3_count++;
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
    var _cur_tier = flagship.upgrades[$ _track] ?? 1;
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

    flagship.upgrades[$ _track] = _next_tier;

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
    var _corp = rival_corporations[$ _corp_id];
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
    var _nem = obj_NemesisManager;
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

// Attempt initial population if NemesisManager is already instantiated
if (instance_exists(obj_NemesisManager)) {
    populate_market_from_nemesis();
}
