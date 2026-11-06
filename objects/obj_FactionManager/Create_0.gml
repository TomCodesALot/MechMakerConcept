/// @description obj_FactionManager Create Event
// Global Interstellar Faction Standing & Dynamic War Simulation Singleton
// Strictly implements docs/04_faction_contracts.md

show_debug_message("[obj_FactionManager] Initializing Global Factions & Strategic Contract Engine...");

// 1. Singleton Guard
if (instance_number(obj_FactionManager) > 1) {
    show_debug_message("[obj_FactionManager] Duplicate detected. Self-terminating instance.");
    instance_destroy();
    exit;
}

// 2. Global Faction Standings (-100 to 100)
// Faction A: Terran Coalition (Earth-central heavy armor & mass production)
// Faction B: Outer Colonies (High mobility energy weapon prototypes)
// Faction C: Rogue Mercenary Syndicates (Black market arms smugglers)
// Era 0 Starting Standings: Superpowers enforce sanctions, heavy tariffs, and border friction
faction_standing = {
    faction_a: -15,     // Terran Coalition (Hostile border friction & mineral quotas)
    faction_b: -25,     // Outer Colonies (Sanctioned / Suspicious)
    faction_c: -30,     // Rogue Syndicates (Hostile outlaws & piracy)
    faction_d: -10,     // Apex Zaibatsu (Dismissive corporate isolation)
    faction_e: -20,     // Sidereal Sovereign League (Hostile / Neutral)
    faction_f: 0        // Tharsis Machine Consensus (Dormant)
};

// 3. Faction Detailed Structs & Military Strengths (docs/04)
factions = {
    faction_a: {
        id: "faction_a",
        name: "The Terran Coalition",
        short_name: "TERRAN",
        alignment: "Earth-Central Command",
        military_strength_score: 55,
        standing: 45,
        standing_title: "Valued Contractor",
        ai_state: "PEACE",
        ai_behavior_title: "Imperial Hegemony & Kinetic Fortification",
        contract_bounty_multiplier: 1.0,
        superweapon_unsealed: false,
        superweapon_name: "VHD-X01 Juggernaut Prime",
        primary_enemy_id: "faction_b",
        preferred_ally_id: "faction_d",
        peace_focus: "Stockpiling tungsten ingots & expanding GHA-07 Ironclad assembly lines.",
        winning_agenda: "Imposes 40% planetary tariffs; enforces Helium-3 tribute quotas.",
        desperate_protocol: "Declares martial law; unseals VHD-X01 Juggernaut Prime; offers 2.0x emergency bounties."
    },
    faction_b: {
        id: "faction_b",
        name: "The Outer Colonies",
        short_name: "COLONIES",
        alignment: "Orbital Independence Alliance",
        military_strength_score: 50,
        standing: -20,
        standing_title: "Hostile / Sanctioned",
        ai_state: "PEACE",
        ai_behavior_title: "Spacenoid Liberation & Vernier Agility",
        contract_bounty_multiplier: 1.0,
        superweapon_unsealed: false,
        superweapon_name: "Astraea Dominus X-01",
        primary_enemy_id: "faction_a",
        preferred_ally_id: "faction_c",
        peace_focus: "Expanding Helium-3 gas refining & bio-dome defense shielding.",
        winning_agenda: "Launches interplanetary crusade; enforces low-Earth orbital blockade.",
        desperate_protocol: "Unseals lost-tech Astraea Dominus X-01; issues frantic 2.0x humanitarian tenders."
    },
    faction_c: {
        id: "faction_c",
        name: "Rogue Mercenary Syndicates",
        short_name: "SYNDICATE",
        alignment: "Black Market Smuggling Network",
        military_strength_score: 30,
        standing: 10,
        standing_title: "Neutral Broker",
        ai_state: "PEACE",
        ai_behavior_title: "Outlaw Scavenging & Harpoon Piracy",
        contract_bounty_multiplier: 1.0,
        superweapon_unsealed: false,
        superweapon_name: "AJS-X02 Rust Behemoth",
        primary_enemy_id: "faction_a",
        preferred_ally_id: "faction_b",
        peace_focus: "Stripping derelict hulks & assembling jury-rigged SCR-12 Hyena frames.",
        winning_agenda: "Consolidates pirate armada under Cruz; enforces protection rackets on all trade corridors.",
        desperate_protocol: "Unseals AJS-X02 Rust Behemoth; launches suicide overclocked swarms; offers 2.0x bounties."
    },
    faction_d: {
        id: "faction_d",
        name: "Apex Bio-Cybernetics Zaibatsu",
        short_name: "ZAIBATSU",
        alignment: "Transhumanist Hyper-Corp Conglomerate",
        military_strength_score: 45,
        standing: 0,
        standing_title: "Neutral Client",
        ai_state: "PEACE",
        ai_behavior_title: "Bio-Neural Hegemony & Covert Espionage",
        contract_bounty_multiplier: 1.0,
        superweapon_unsealed: false,
        superweapon_name: "HATS-X01 Amaterasu Zero",
        primary_enemy_id: "faction_c",
        preferred_ally_id: "faction_a",
        peace_focus: "R&D into spinal neural links, hostile takeovers, and producing ZAI-03 Muramasa dueling frames.",
        winning_agenda: "Forecloses on sovereign planetary debt; replaces human garrisons with autonomous combat drones.",
        desperate_protocol: "Unseals rogue HATS-X01 Amaterasu Zero; deploys pain-inhibited cybernetic suicide aces; offers 2.0x bounties."
    },
    faction_e: {
        id: "faction_e",
        name: "The Sidereal Sovereign League",
        short_name: "SIDEREAL",
        alignment: "Deep-Space Spacenoid Sovereignty",
        military_strength_score: 48,
        standing: -10,
        standing_title: "Distrustful / Void Republic",
        ai_state: "PEACE",
        ai_behavior_title: "Homo Sideralis & Cradle Vacatur",
        contract_bounty_multiplier: 1.0,
        superweapon_unsealed: false,
        superweapon_name: "Astraea Archon X-09",
        primary_enemy_id: "faction_a",
        preferred_ally_id: "faction_b",
        is_dormant: false,
        peace_focus: "Constructing high-orbit solar mirrors & zero-G crystalline vacuum superalloys.",
        winning_agenda: "Proclaims Universal Vacatur; demands total human evacuation of Earth.",
        desperate_protocol: "Unseals orbital beam fortress Astraea Archon X-09; issues 2.0x preservation tenders."
    },
    faction_f: {
        id: "faction_f",
        name: "The Tharsis Machine Consensus",
        short_name: "CONSENSUS",
        alignment: "Sub-Martian Cavern Ascendancy & The Logic God",
        military_strength_score: 65,
        standing: 0,
        standing_title: "Classified / Red Crypt",
        ai_state: "PEACE",
        ai_behavior_title: "Subterranean Logic God & Sister Ark Reunion",
        contract_bounty_multiplier: 1.0,
        superweapon_unsealed: false,
        superweapon_name: "Deus-Machina: Ouroboros Prime",
        primary_enemy_id: "faction_d",
        preferred_ally_id: "faction_a",
        is_dormant: true,
        peace_focus: "Subterranean quantum computations & geothermal core tapping beneath Olympus Mons.",
        winning_agenda: "Initiates Global Entropy Purge; demands unconditional biological disarmament.",
        desperate_protocol: "Unseals Deus-Machina: Ouroboros Prime; deploys nanite self-repair waves; issues 2.0x tenders to Sister Ship Hephaestus."
    }
};

// 4. Strategic Territory Control & Contested Sectors (docs/04, docs/12, docs/39)
territory_control = {
    terran_pct: 20,
    colony_pct: 20,
    syndicate_pct: 20,
    zaibatsu_pct: 20,
    astran_pct: 20,
    martian_pct: 0,
    pmc_pct: 0,
    contested_sector: "GIBRALTAR & IRONSPIRE BASTION CORRIDOR",
    last_shift_report: "Superpowers entrenched across Earth and Space frontlines (20% Sol parity)."
};
territory_database = scr_init_territory_database();
mars_unlocked = false;
scr_territory_recalculate_control_percentages();

// 4b. Mass Production Replacement Doctrine Contracts (docs/12_sandbox_and_endgame_systems.md)
mass_production_contracts = {
    faction_a: {
        faction_id: "faction_a",
        faction_name: "The Terran Coalition",
        replaced: false,
        baseline_suit_id: "GHA-07",
        baseline_suit_name: "GHA-07 Ironclad",
        replacement_name: "None (Terran Standard Issue)",
        replacement_blueprint_id: "",
        licensing_bounty: 1800000,
        royalty_per_turn: 45000,
        combat_bonus: 18,
        cumulative_royalties_paid: 0,
        adoption_stage: "UNADOPTED",
        tooling_turns_remaining: 2,
        active_frontline_units: 0,
        block_level: 1,
        req_armor: 180,
        req_power: 8
    },
    faction_b: {
        faction_id: "faction_b",
        faction_name: "The Outer Colonies",
        replaced: false,
        baseline_suit_id: "AET-01",
        baseline_suit_name: "AET-01 Aether",
        replacement_name: "None (Colony Standard Issue)",
        replacement_blueprint_id: "",
        licensing_bounty: 2100000,
        royalty_per_turn: 52000,
        combat_bonus: 20,
        cumulative_royalties_paid: 0,
        req_armor: 120,
        req_power: 16,
        adoption_stage: "UNADOPTED",
        tooling_turns_remaining: 2,
        active_frontline_units: 0,
        block_level: 1
    },
    faction_c: {
        faction_id: "faction_c",
        faction_name: "Rogue Mercenary Syndicates",
        replaced: false,
        baseline_suit_id: "SCR-12",
        baseline_suit_name: "SCR-12 Hyena",
        replacement_name: "None (Syndicate Standard Issue)",
        replacement_blueprint_id: "",
        licensing_bounty: 1400000,
        royalty_per_turn: 38000,
        combat_bonus: 16,
        cumulative_royalties_paid: 0,
        req_armor: 130,
        req_power: 10,
        adoption_stage: "UNADOPTED",
        tooling_turns_remaining: 2,
        active_frontline_units: 0,
        block_level: 1
    },
    faction_d: {
        faction_id: "faction_d",
        faction_name: "Apex Bio-Cybernetics Zaibatsu",
        replaced: false,
        baseline_suit_id: "ZAI-03",
        baseline_suit_name: "ZAI-03 Muramasa",
        replacement_name: "None (Zaibatsu Standard Issue)",
        replacement_blueprint_id: "",
        licensing_bounty: 2400000,
        royalty_per_turn: 58000,
        combat_bonus: 22,
        cumulative_royalties_paid: 0,
        req_armor: 135,
        req_power: 14,
        adoption_stage: "UNADOPTED",
        tooling_turns_remaining: 2,
        active_frontline_units: 0,
        block_level: 1
    },
    faction_e: {
        faction_id: "faction_e",
        faction_name: "The Sidereal Sovereign League",
        replaced: false,
        baseline_suit_id: "AST-01",
        baseline_suit_name: "AST-01 Chariot",
        replacement_name: "None (Sidereal Standard Issue)",
        replacement_blueprint_id: "",
        licensing_bounty: 2200000,
        royalty_per_turn: 55000,
        combat_bonus: 22,
        cumulative_royalties_paid: 0,
        req_armor: 125,
        req_power: 16,
        adoption_stage: "UNADOPTED",
        tooling_turns_remaining: 2,
        active_frontline_units: 0,
        block_level: 1
    },
    faction_f: {
        faction_id: "faction_f",
        faction_name: "The Tharsis Machine Consensus",
        replaced: false,
        baseline_suit_id: "MAR-01",
        baseline_suit_name: "MAR-01 Phobos",
        replacement_name: "None (Consensus Standard Issue)",
        replacement_blueprint_id: "",
        licensing_bounty: 2600000,
        royalty_per_turn: 65000,
        combat_bonus: 25,
        cumulative_royalties_paid: 0,
        req_armor: 160,
        req_power: 18,
        adoption_stage: "UNADOPTED",
        tooling_turns_remaining: 2,
        active_frontline_units: 0,
        block_level: 1
    }
};

// 4b. Revamped Mass Production Candidate Pools (docs/29)
mass_production_candidates = {
    faction_a: [
        { id: "ms_terran_ironclad_07", name: "GHA-07 Ironclad", doctrine: "Kinetic Trench Fortress", weapon: "Type-77 120mm Autocannon", armor: 2480, power: 12, speed: 45, combat: 480, sprite: spr_ms_ironclad_idle, req_armor: 180, req_power: 8, bounty: 1800000, royalty: 45000 },
        { id: "ms_terran_ballista_04", name: "TH-M04 Ballista", doctrine: "Quadruped Heavy Artillery", weapon: "Twin 200mm Heavy Howitzers", armor: 2350, power: 11, speed: 38, combat: 460, sprite: spr_ms_ballista_idle, req_armor: 170, req_power: 9, bounty: 1750000, royalty: 42000 },
        { id: "ms_terran_centurion_02", name: "TH-C02 Centurion", doctrine: "Hydraulic Linebreaker", weapon: "GAU-88 Rotary Heavy Vulcan", armor: 2200, power: 14, speed: 62, combat: 510, sprite: spr_ms_centurion_idle, req_armor: 160, req_power: 10, bounty: 1900000, royalty: 48000 },
        { id: "ms_terran_trenchcoat_09", name: "TH-T09 Trenchcoat", doctrine: "CQB Slugs & Smokescreen", weapon: "12-Gauge Heavy Slug Autoshotgun", armor: 2150, power: 10, speed: 50, combat: 430, sprite: spr_ms_trenchcoat_idle, req_armor: 155, req_power: 8, bounty: 1600000, royalty: 40000 }
    ],
    faction_b: [
        { id: "ms_colony_aether_01", name: "AET-01 Aether", doctrine: "Zero-G Agile Superiority", weapon: "Twin High-Yield Beam Carbines", armor: 1820, power: 16, speed: 85, combat: 490, sprite: spr_ms_aether_idle, req_armor: 120, req_power: 16, bounty: 2100000, royalty: 52000 },
        { id: "ms_colony_zephyr_05", name: "JCC-Z05 Zephyr", doctrine: "EW Sensor Jammer", weapon: "Pulse Laser Array & Jammer", armor: 1680, power: 15, speed: 92, combat: 470, sprite: spr_ms_zephyr_idle, req_armor: 110, req_power: 15, bounty: 2000000, royalty: 50000 },
        { id: "ms_colony_kepler_02", name: "JCC-K02 Kepler", doctrine: "Orbital Rail-Sniper", weapon: "Magnetic Linear Rail-Rifle", armor: 1720, power: 14, speed: 78, combat: 480, sprite: spr_ms_kepler_idle, req_armor: 115, req_power: 14, bounty: 2050000, royalty: 51000 },
        { id: "ms_colony_oberon_08", name: "JCC-O08 Oberon", doctrine: "Point-Defense Fleet Escort", weapon: "Thermal Beam Lance & PDS", armor: 1950, power: 17, speed: 80, combat: 510, sprite: spr_ms_oberon_idle, req_armor: 130, req_power: 17, bounty: 2200000, royalty: 54000 }
    ],
    faction_c: [
        { id: "ms_syndicate_hyena_12", name: "SCR-12 Hyena", doctrine: "Scrap Harpoon Scavenger", weapon: "Magnetic Harpoon & 80mm Flak", armor: 1980, power: 10, speed: 60, combat: 460, sprite: spr_ms_hyena_idle, req_armor: 130, req_power: 10, bounty: 1400000, royalty: 38000 },
        { id: "ms_syndicate_gorgon_04", name: "ARC-G04 Gorgon", doctrine: "Boarding Cutter & Ram", weapon: "Heavy Thermal Cutter Claw", armor: 2300, power: 12, speed: 52, combat: 490, sprite: spr_ms_gorgon_idle, req_armor: 145, req_power: 11, bounty: 1600000, royalty: 42000 },
        { id: "ms_syndicate_bloodhound_06", name: "ARC-B06 Bloodhound", doctrine: "Wheeled Pack Hunter", weapon: "Quad 70mm Rocket Pods", armor: 1850, power: 9, speed: 72, combat: 440, sprite: spr_ms_bloodhound_idle, req_armor: 120, req_power: 9, bounty: 1350000, royalty: 36000 },
        { id: "ms_syndicate_vandal_03", name: "ARC-V03 Vandal", doctrine: "Ambush Shrapnel & Decoys", weapon: "Flechette Autogun & Flares", armor: 1750, power: 10, speed: 66, combat: 430, sprite: spr_ms_vandal_idle, req_armor: 115, req_power: 9, bounty: 1300000, royalty: 35000 }
    ],
    faction_d: [
        { id: "ms_zaibatsu_muramasa_03", name: "ZAI-03 Muramasa", doctrine: "High-Frequency Tachyon Duelist", weapon: "High-Frequency Tachyon Katana", armor: 1950, power: 14, speed: 82, combat: 500, sprite: spr_ms_muramasa_idle, req_armor: 135, req_power: 14, bounty: 2400000, royalty: 58000 },
        { id: "ms_zaibatsu_kage_07", name: "ZBT-K07 Kage", doctrine: "Optical Camo Assassin", weapon: "Hyper-Velocity Needle Railgun", armor: 1650, power: 13, speed: 88, combat: 480, sprite: spr_ms_kage_idle, req_armor: 120, req_power: 13, bounty: 2300000, royalty: 55000 },
        { id: "ms_zaibatsu_ronin_04", name: "ZBT-R04 Ronin", doctrine: "Autonomous Sub-Drone Carrier", weapon: "Sub-Drone Swarm Pod & Naginata", armor: 2100, power: 16, speed: 75, combat: 520, sprite: spr_ms_ronin_idle, req_armor: 140, req_power: 15, bounty: 2500000, royalty: 60000 },
        { id: "ms_zaibatsu_tessen_09", name: "ZBT-T09 Tessen", doctrine: "EMP Neural Jammer & Deflector", weapon: "Broadband EMP Disruptor", armor: 1820, power: 15, speed: 78, combat: 470, sprite: spr_ms_tessen_idle, req_armor: 125, req_power: 14, bounty: 2250000, royalty: 54000 }
    ],
    faction_e: [
        { id: "ms_astran_chariot_01", name: "AST-01 Chariot", doctrine: "Zero-G Vernier Interceptor", weapon: "Twin Linear Particle Rifles", armor: 1750, power: 17, speed: 90, combat: 510, sprite: spr_ms_aether_idle, req_armor: 120, req_power: 16, bounty: 2200000, royalty: 55000 },
        { id: "ms_astran_seraph_04", name: "AST-04 Seraph", doctrine: "Radiator Beam Skirmisher", weapon: "Coherent Solar Particle Lance", armor: 1820, power: 18, speed: 84, combat: 530, sprite: spr_ms_aether_idle, req_armor: 125, req_power: 17, bounty: 2350000, royalty: 58000 },
        { id: "ms_astran_paladin_09", name: "AST-09 Paladin", doctrine: "Heavy LFIP Immersion Duelist", weapon: "Hyper-Velocity Beam Saber", armor: 2050, power: 19, speed: 82, combat: 540, sprite: spr_ms_aether_idle, req_armor: 135, req_power: 18, bounty: 2500000, royalty: 62000 },
        { id: "ms_astran_orion_06", name: "AST-06 Orion", doctrine: "Deep Void Monocular Sniper", weapon: "Tachyon Waveguide Long-Rifle", armor: 1650, power: 16, speed: 88, combat: 495, sprite: spr_ms_aether_idle, req_armor: 115, req_power: 15, bounty: 2150000, royalty: 53000 }
    ],
    faction_f: [
        { id: "ms_martian_phobos_01", name: "MAR-01 Phobos", doctrine: "Superconductive Cryo-Siege", weapon: "Cryo-Coil Superconductive Lance", armor: 2400, power: 19, speed: 68, combat: 560, sprite: spr_ms_ironclad_idle, req_armor: 155, req_power: 18, bounty: 2600000, royalty: 65000 },
        { id: "ms_martian_deimos_04", name: "MAR-04 Deimos", doctrine: "Sub-Basalt Burrowing Brawler", weapon: "High-Frequency Thermal Drill Claw", armor: 2550, power: 18, speed: 64, combat: 540, sprite: spr_ms_ironclad_idle, req_armor: 165, req_power: 17, bounty: 2500000, royalty: 62000 },
        { id: "ms_martian_vector_07", name: "MAR-07 Vector-Prime", doctrine: "Autonomous Hunter-Killer Swarm", weapon: "Zero-Point Beam Arrays & Sub-Pods", armor: 2200, power: 21, speed: 80, combat: 580, sprite: spr_ms_aether_idle, req_armor: 145, req_power: 20, bounty: 2800000, royalty: 70000 },
        { id: "ms_martian_ares_09", name: "MAR-09 Ares Logica", doctrine: "Logic God Heavy Anchor", weapon: "Tachyon Entropic Disruption Cannon", armor: 2700, power: 22, speed: 60, combat: 600, sprite: spr_ms_ironclad_idle, req_armor: 175, req_power: 21, bounty: 3000000, royalty: 75000 }
    ]
};

roll_playthrough_mass_production_selection = function(_forced_seed = undefined) {
    var _f_keys = ["faction_a", "faction_b", "faction_c", "faction_d", "faction_e", "faction_f"];
    for (var f = 0; f < array_length(_f_keys); f++) {
        var _fk = _f_keys[f];
        var _pool = variable_struct_get(mass_production_candidates, _fk);
        var _idx = 0;
        if (!is_undefined(_forced_seed)) {
            _idx = (_forced_seed + f * 7) % array_length(_pool);
        } else {
            _idx = irandom(array_length(_pool) - 1);
        }
        var _chosen = _pool[_idx];

        var _contract = variable_struct_get(mass_production_contracts, _fk);
        if (!is_undefined(_contract)) {
            _contract.baseline_suit_id = _chosen.id;
            _contract.baseline_suit_name = _chosen.name;
            _contract.doctrine = _chosen.doctrine;
            _contract.signature_weapon = _chosen.weapon;
            _contract.sprite_asset = _chosen.sprite;
            _contract.req_armor = _chosen.req_armor;
            _contract.req_power = _chosen.req_power;
            _contract.licensing_bounty = _chosen.bounty;
            _contract.royalty_per_turn = _chosen.royalty;
            _contract.combat_bonus = round(_chosen.combat / 25);
            _contract.candidate_index = _idx;
            show_debug_message("[MASS PRODUCTION VARIANCE] " + _fk + " ratified candidate " + string(_idx + 1) + "/4: " + _chosen.name + " (" + _chosen.doctrine + ")");
        }
    }
};

roll_playthrough_mass_production_selection();

factions_overthrown = [];
pmc_expeditions_launched = 0;

// 4c. Bilateral Diplomatic Relations Matrix & Geopolitical AI Engine (docs/21)
// Tracks 6 unique bilateral faction pairs, Tension (0-100), treaty timers, and state machines.
diplomatic_relations = {
    terran_colony: {
        pair_id: "terran_colony",
        faction_1: "faction_a",
        faction_2: "faction_b",
        name_1: "The Terran Coalition",
        name_2: "The Outer Colonies",
        state: "WAR", // WAR, COLD_WAR, TRUCE, ALLIANCE, NON_AGGRESSION
        tension: 88,
        base_friction: 3.0,
        treaty_turns_left: 0,
        treaty_max_turns: 0,
        casus_belli: "Orbital Colonial Sovereignty & Jovian Gas Mine Hegemony",
        historical_grievance: "Centuries of Earth-centric colonial taxation & repressive mineral tariffs",
        total_wars_fought: 4,
        war_duration_turns: 8,
        last_event_turn: 1
    },
    terran_syndicate: {
        pair_id: "terran_syndicate",
        faction_1: "faction_a",
        faction_2: "faction_c",
        name_1: "The Terran Coalition",
        name_2: "Rogue Mercenary Syndicates",
        state: "COLD_WAR",
        tension: 68,
        base_friction: 2.5,
        treaty_turns_left: 0,
        treaty_max_turns: 0,
        casus_belli: "Smuggling contraband past Earth orbital blockades",
        historical_grievance: "Ruthless federal crackdowns on free-trader merchant networks",
        total_wars_fought: 2,
        war_duration_turns: 0,
        last_event_turn: 1
    },
    terran_zaibatsu: {
        pair_id: "terran_zaibatsu",
        faction_1: "faction_a",
        faction_2: "faction_d",
        name_1: "The Terran Coalition",
        name_2: "Apex Bio-Cybernetics Zaibatsu",
        state: "NON_AGGRESSION",
        tension: 35,
        base_friction: 1.0,
        treaty_turns_left: 0,
        treaty_max_turns: 0,
        casus_belli: "Corporate sovereign charter and patent tax disputes",
        historical_grievance: "Federal antitrust threats vs corporate sovereign immunity claims",
        total_wars_fought: 1,
        war_duration_turns: 0,
        last_event_turn: 1
    },
    colony_syndicate: {
        pair_id: "colony_syndicate",
        faction_1: "faction_b",
        faction_2: "faction_c",
        name_1: "The Outer Colonies",
        name_2: "Rogue Mercenary Syndicates",
        state: "ALLIANCE",
        tension: 42,
        base_friction: 1.0,
        treaty_turns_left: 14,
        treaty_max_turns: 18,
        casus_belli: "Mutual defense pact against Earth imperial expansion",
        historical_grievance: "Syndicate price-gouging on life-support parts during blockades",
        total_wars_fought: 1,
        war_duration_turns: 0,
        last_event_turn: 1
    },
    colony_zaibatsu: {
        pair_id: "colony_zaibatsu",
        faction_1: "faction_b",
        faction_2: "faction_d",
        name_1: "The Outer Colonies",
        name_2: "Apex Bio-Cybernetics Zaibatsu",
        state: "COLD_WAR",
        tension: 62,
        base_friction: 2.0,
        treaty_turns_left: 0,
        treaty_max_turns: 0,
        casus_belli: "Zaibatsu patent monopolies and cybernetic pilot debt indentures",
        historical_grievance: "Colony mineral strikes sabotaged by Zaibatsu black-ops contractors",
        total_wars_fought: 2,
        war_duration_turns: 0,
        last_event_turn: 1
    },
    syndicate_zaibatsu: {
        pair_id: "syndicate_zaibatsu",
        faction_1: "faction_c",
        faction_2: "faction_d",
        name_1: "Rogue Mercenary Syndicates",
        name_2: "Apex Bio-Cybernetics Zaibatsu",
        state: "TRUCE",
        tension: 45,
        base_friction: 1.5,
        treaty_turns_left: 9,
        treaty_max_turns: 14,
        casus_belli: "Stolen neuro-link blueprints and pirated bioware tech",
        historical_grievance: "Cartel raids on offshore research installations",
        total_wars_fought: 3,
        war_duration_turns: 0,
        last_event_turn: 1
    },
    terran_astran: {
        pair_id: "terran_astran",
        faction_1: "faction_a",
        faction_2: "faction_e",
        name_1: "The Terran Coalition",
        name_2: "The Sidereal Sovereign League",
        state: "WAR",
        tension: 92,
        base_friction: 3.5,
        treaty_turns_left: 0,
        treaty_max_turns: 0,
        casus_belli: "Universal Planetary Vacatur Edict vs Terran Territorial Sovereignty",
        historical_grievance: "Centuries of Earth-bound neglect and Astran calls to forcibly evacuate Earth",
        total_wars_fought: 3,
        war_duration_turns: 6,
        last_event_turn: 1
    },
    colony_astran: {
        pair_id: "colony_astran",
        faction_1: "faction_b",
        faction_2: "faction_e",
        name_1: "The Outer Colonies",
        name_2: "The Sidereal Sovereign League",
        state: "ALLIANCE",
        tension: 28,
        base_friction: 0.8,
        treaty_turns_left: 20,
        treaty_max_turns: 25,
        casus_belli: "Shared Spacenoid heritage and deep-space mutual defense",
        historical_grievance: "Disagreements over whether to reform trade with Earth or abandon Earth completely",
        total_wars_fought: 0,
        war_duration_turns: 0,
        last_event_turn: 1
    },
    syndicate_astran: {
        pair_id: "syndicate_astran",
        faction_1: "faction_c",
        faction_2: "faction_e",
        name_1: "Rogue Mercenary Syndicates",
        name_2: "The Sidereal Sovereign League",
        state: "COLD_WAR",
        tension: 58,
        base_friction: 1.8,
        treaty_turns_left: 0,
        treaty_max_turns: 0,
        casus_belli: "Black-market mining incursions into Jovian ice rings",
        historical_grievance: "Syndicate piracy against Astran solar collector sails",
        total_wars_fought: 1,
        war_duration_turns: 0,
        last_event_turn: 1
    },
    zaibatsu_astran: {
        pair_id: "zaibatsu_astran",
        faction_1: "faction_d",
        faction_2: "faction_e",
        name_1: "Apex Bio-Cybernetics Zaibatsu",
        name_2: "The Sidereal Sovereign League",
        state: "COLD_WAR",
        tension: 65,
        base_friction: 2.2,
        treaty_turns_left: 0,
        treaty_max_turns: 0,
        casus_belli: "Stolen LFIP liquid-breathing cockpit schematics vs Zaibatsu neuro-tech",
        historical_grievance: "Zaibatsu patent claims over Astran cryogenic genetic strains",
        total_wars_fought: 2,
        war_duration_turns: 0,
        last_event_turn: 1
    },
    terran_martian: {
        pair_id: "terran_martian",
        faction_1: "faction_a",
        faction_2: "faction_f",
        name_1: "The Terran Coalition",
        name_2: "The Tharsis Machine Consensus",
        state: "WAR",
        tension: 96,
        base_friction: 4.0,
        treaty_turns_left: 0,
        treaty_max_turns: 0,
        casus_belli: "Vengeance for the Y142 Martian Colonization Flotilla ambush",
        historical_grievance: "Terrestrial corporate strikes that doomed the first 120,000 Martian colonists",
        total_wars_fought: 1,
        war_duration_turns: 0,
        last_event_turn: 1
    },
    zaibatsu_martian: {
        pair_id: "zaibatsu_martian",
        faction_1: "faction_d",
        faction_2: "faction_f",
        name_1: "Apex Bio-Cybernetics Zaibatsu",
        name_2: "The Tharsis Machine Consensus",
        state: "WAR",
        tension: 90,
        base_friction: 3.5,
        treaty_turns_left: 0,
        treaty_max_turns: 0,
        casus_belli: "Corporate attempts to infiltrate and seize the Ares Primus quantum core",
        historical_grievance: "Zaibatsu espionage black-ops probing subterranean Olympus Mons crypts",
        total_wars_fought: 1,
        war_duration_turns: 0,
        last_event_turn: 1
    }
};

// 4d. Live Diplomatic Cables Log (Command Deck Teletype Feed, docs/21)
diplomatic_cables_log = [
    {
        id: "cable_hist_01",
        turn: 1,
        sender: "The Terran Coalition",
        recipient: "The Outer Colonies",
        title: "DECLARATION OF UNRESTRICTED ENGAGEMENT",
        body: "Federal High Command authorizes unrestricted kinetic strikes along Sector 4 trenches. All colonial craft in Jovian orbit designated hostile.",
        priority: "URGENT",
        state: "WAR"
    },
    {
        id: "cable_hist_02",
        turn: 1,
        sender: "The Outer Colonies",
        recipient: "Rogue Mercenary Syndicates",
        title: "JOVIAN MUTUAL DEFENSE ACCORD RATIFIED",
        body: "Colonial Council ratifies mutual defense pact with Free-Trader Guilds. Joint patrols established along Jupiter orbital corridor.",
        priority: "HIGH",
        state: "ALLIANCE"
    },
    {
        id: "cable_hist_03",
        turn: 1,
        sender: "Apex Bio-Cybernetics Zaibatsu",
        recipient: "Rogue Mercenary Syndicates",
        title: "CEASEFIRE ACCORD: CALLISTO PATENT SETTLEMENT",
        body: "Hostilities suspended for 14 turns following neutral arbitration over seized cybernetic neural schematics.",
        priority: "NORMAL",
        state: "TRUCE"
    },
    {
        id: "cable_hist_04",
        turn: 1,
        sender: "The Terran Coalition",
        recipient: "Apex Bio-Cybernetics Zaibatsu",
        title: "FEDERAL-CORPORATE NON-AGGRESSION PACT",
        body: "Terran Ministry of Commerce confirms mutual non-aggression and preferential tariff status with Zaibatsu industrial habitats.",
        priority: "NORMAL",
        state: "NON_AGGRESSION"
    }
];

// Anti-Hegemonic Coalition Tracker (Balance-of-Power Anti-Blobbing, docs/21)
hegemon_faction_id = "";
coalition_active = false;


// 5. Contract Queues (docs/04)
active_contracts = [];       // Currently accepted contracts with active deadlines
available_contracts = [
    {
        id: "cnt_terran_convoy_01",
        faction: "faction_a",
        faction_name: "The Terran Coalition",
        type: "ESCORT_SORTIE",
        title: "OPERATION MAMMOTH ESCORT: TANK CONVOY DEFENSE",
        briefing: "Terran Coalition requires armored support to escort a supply convoy of T-720 Mammoth Battle Tanks through contested volcanic terrain.",
        required_tier: 1,
        required_quantity: 1,
        delivered_quantity: 0,
        payout_credits: 320000,
        reputation_gain: 15,
        reputation_penalty: -15,
        deadline_days: 25,
        days_remaining: 25,
        penalty_credits: 60000
    },
    {
        id: "cnt_colony_patrol_01",
        faction: "faction_b",
        faction_name: "The Outer Colonies",
        type: "INTERCEPTION_SORTIE",
        title: "SECTOR HARRIER: INTERCEPT SYNDICATE TECHNICALS",
        briefing: "Colony defense militia requests fast tactical interdiction against roving packs of pirate technicals threatening water mining claims.",
        required_tier: 1,
        required_quantity: 1,
        delivered_quantity: 0,
        payout_credits: 280000,
        reward_material_id: "mat_tritium",
        reward_material_amount: 5,
        reputation_gain: 20,
        reputation_penalty: -10,
        deadline_days: 18,
        days_remaining: 18,
        penalty_credits: 40000
    },
    {
        id: "cnt_syndicate_black_01",
        faction: "faction_c",
        faction_name: "Rogue Mercenary Syndicates",
        type: "BLACK_OPS_SALE",
        title: "BLACK MARKET RUN: EXPERIMENTAL TOKAMAK FLUX",
        briefing: "Smugglers will pay top dollar in refined Synthetic Flux for uncataloged magnetic containment rings. 35% Risk of Terran Intelligence leak!",
        required_tier: 1,
        required_quantity: 1,
        delivered_quantity: 0,
        payout_credits: 220000,
        reward_material_id: "mat_syn_flux",
        reward_material_amount: 8,
        tech_leak_risk_pct: 35,
        reputation_gain: 25,
        reputation_penalty: 0,
        deadline_days: 12,
        days_remaining: 12,
        penalty_credits: 0
    },
    {
        id: "cnt_zaibatsu_neural_01",
        faction: "faction_d",
        faction_name: "Apex Bio-Cybernetics Zaibatsu",
        type: "PROTOTYPE_BOUNTY",
        title: "PROJECT SUSANOO: NEURAL-SYNC HARMONIC CORE",
        briefing: "Director Renzo Takahashi requires an over-clocked Tokamak reactor core tuned to >=90% harmonic sync to field-test spinal neural-link interface latency.",
        required_tier: 2,
        required_quantity: 1,
        delivered_quantity: 0,
        payout_credits: 340000,
        reward_material_id: "mat_syn_flux",
        reward_material_amount: 10,
        reputation_gain: 20,
        reputation_penalty: -10,
        deadline_days: 15,
        days_remaining: 15,
        penalty_credits: 50000
    }
];

// 6. Standing Management Methods
get_standing = function(_faction_id) {
    return variable_struct_get(faction_standing, _faction_id) ?? 0;
};

set_standing = function(_faction_id, _val) {
    var _clamped = clamp(_val, -100, 100);
    variable_struct_set(faction_standing, _faction_id, _clamped);
    if (variable_struct_exists(factions, _faction_id)) {
        variable_struct_get(factions, _faction_id).standing = _clamped;
    }
    return _clamped;
};

modify_standing = function(_faction_id, _delta) {
    var _current = get_standing(_faction_id);
    return set_standing(_faction_id, _current + _delta);
};

// 7. Dynamic Macro War Map & Faction AI Diplomacy Engine (docs/04, docs/12, docs/21)

// 7a. Add Diplomatic Cable to Teletype Log
add_diplomatic_cable = function(_sender = "Unknown Command", _recipient = "Sol Network", _title = "Diplomatic Notice", _body = "", _priority = "NORMAL", _state = "COLD_WAR") {
    var _c_turn = (instance_exists(obj_GameManager)) ? obj_GameManager.current_turn : 1;
    var _cable = {
        id: "cable_" + string(_c_turn) + "_" + string(irandom(9999)),
        turn: _c_turn,
        sender: is_undefined(_sender) ? "Unknown Command" : string(_sender),
        recipient: is_undefined(_recipient) ? "Sol Network" : string(_recipient),
        title: is_undefined(_title) ? "Diplomatic Notice" : string(_title),
        body: is_undefined(_body) ? "" : string(_body),
        priority: is_undefined(_priority) ? "NORMAL" : string(_priority),
        state: is_undefined(_state) ? "COLD_WAR" : string(_state)
    };
    array_push(diplomatic_cables_log, _cable);
    if (array_length(diplomatic_cables_log) > 30) {
        array_delete(diplomatic_cables_log, 0, 1);
    }
    if (_priority == "URGENT" && instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("DIPLOMATIC CRISIS: " + _title, c_red);
    } else if (_priority == "HIGH" && instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("DIPLOMATIC NOTICE: " + _title, c_aqua);
    }
    return _cable;
};

// 7b. Query Bilateral Relation by Faction IDs
get_relation = function(_f1, _f2) {
    var _keys = variable_struct_get_names(diplomatic_relations);
    for (var k = 0; k < array_length(_keys); k++) {
        var _rel = variable_struct_get(diplomatic_relations, _keys[k]);
        if ((_rel.faction_1 == _f1 && _rel.faction_2 == _f2) || (_rel.faction_1 == _f2 && _rel.faction_2 == _f1)) {
            return _rel;
        }
    }
    return undefined;
};

get_relation_by_id = function(_pair_id) {
    if (variable_struct_exists(diplomatic_relations, _pair_id)) {
        return variable_struct_get(diplomatic_relations, _pair_id);
    }
    return undefined;
};

// 7c. Set Diplomatic State & Record Communiqué
set_diplomatic_state = function(_pair_id, _new_state, _duration, _reason) {
    var _rel = get_relation_by_id(_pair_id);
    if (is_undefined(_rel)) return;
    
    var _old_state = _rel.state;
    _rel.state = _new_state;
    _rel.treaty_turns_left = _duration;
    _rel.treaty_max_turns = _duration;
    _rel.last_event_turn = (instance_exists(obj_GameManager)) ? obj_GameManager.current_turn : 1;
    
    var _priority = (_new_state == "WAR") ? "URGENT" : ((_new_state == "ALLIANCE" || _new_state == "TRUCE") ? "HIGH" : "NORMAL");
    var _title = _rel.name_1 + " & " + _rel.name_2 + ": " + _new_state;
    var _body = _reason + " (State transitioned from " + _old_state + " to " + _new_state + ").";
    add_diplomatic_cable(_rel.name_1, _rel.name_2, _title, _body, _priority, _new_state);
};

// 7d. Modify Bilateral Tension (clamped 0 to 100)
modify_bilateral_tension = function(_pair_id, _delta, _reason) {
    var _rel = get_relation_by_id(_pair_id);
    if (is_undefined(_rel)) return;

    var _old = _rel.tension;
    _rel.tension = clamp(_rel.tension + _delta, 0, 100);

    // Alliance Paranoia Check (Break alliance if tension reaches 75+)
    if (_rel.state == "ALLIANCE" && _rel.tension >= 75) {
        if (_rel.tension >= 85) {
            declare_war(_pair_id, "ALLIED BETRAYAL: Mounting espionage and tensions reached 85+. Alliance shattered into open war!");
        } else {
            set_diplomatic_state(_pair_id, "COLD_WAR", 0, "ALLIANCE FRACTURE: Tension reached " + string(_rel.tension) + " due to mutual paranoia and espionage.");
        }
    }
    // Cold War Boiling Point Check (Escalate to War at 85+)
    else if ((_rel.state == "COLD_WAR" || _rel.state == "NON_AGGRESSION") && _rel.tension >= 85) {
        declare_war(_pair_id, "BOILING POINT: Bilateral tension reached " + string(_rel.tension) + " over " + _rel.casus_belli + ".");
    }
};

// 7e. Formal Declaration of War
declare_war = function(_pair_id, _casus_belli) {
    var _rel = get_relation_by_id(_pair_id);
    if (is_undefined(_rel)) return;

    _rel.state = "WAR";
    _rel.tension = max(88, _rel.tension);
    _rel.treaty_turns_left = 0;
    _rel.treaty_max_turns = 0;
    _rel.war_duration_turns = 0;
    _rel.total_wars_fought += 1;
    _rel.last_event_turn = (instance_exists(obj_GameManager)) ? obj_GameManager.current_turn : 1;

    var _title = "WAR DECLARED: " + string_upper(_rel.name_1) + " VS " + string_upper(_rel.name_2);
    var _body = "Hostilities commenced! Casus Belli: " + _casus_belli + ". All active treaties voided.";
    add_diplomatic_cable(_rel.name_1, _rel.name_2, _title, _body, "URGENT", "WAR");

    // Milestone 54: Visual Novel Geopolitical War Declaration Episode Dispatch
    if (instance_exists(obj_HQTerminal) && !scr_vn_is_active()) {
        if (_pair_id == "rel_tc" && !variable_struct_exists(_rel, "vn_war_shown")) {
            _rel.vn_war_shown = true;
            scr_vn_start_episode("ep_war_terran_vs_colony");
        } else if (_pair_id == "rel_cz" && !variable_struct_exists(_rel, "vn_war_shown")) {
            _rel.vn_war_shown = true;
            scr_vn_start_episode("ep_war_zaibatsu_vs_tharsis");
        } else if ((_pair_id == "rel_ts" || _pair_id == "rel_cs" || _pair_id == "rel_sc") && !variable_struct_exists(_rel, "vn_war_shown")) {
            _rel.vn_war_shown = true;
            scr_vn_start_episode("ep_war_syndicate_vs_sidereal");
        }
    }
};

// 7f. Broker Ceasefire Truce
broker_truce = function(_pair_id, _duration, _reason) {
    var _rel = get_relation_by_id(_pair_id);
    if (is_undefined(_rel)) return;

    _rel.state = "TRUCE";
    _rel.tension = 40;
    _rel.treaty_turns_left = _duration;
    _rel.treaty_max_turns = _duration;
    _rel.war_duration_turns = 0;
    _rel.last_event_turn = (instance_exists(obj_GameManager)) ? obj_GameManager.current_turn : 1;

    var _title = "CEASEFIRE ACCORD: " + string_upper(_rel.name_1) + " - " + string_upper(_rel.name_2);
    var _body = "Armistice signed for " + string(_duration) + " turns. " + _reason;
    add_diplomatic_cable(_rel.name_1, _rel.name_2, _title, _body, "HIGH", "TRUCE");

    // Milestone 54: Visual Novel Geopolitical Ceasefire Episode Dispatch
    if (instance_exists(obj_HQTerminal) && !scr_vn_is_active()) {
        if (_pair_id == "rel_tc") {
            scr_vn_start_episode("ep_ceasefire_terran_colony");
        } else if (_pair_id == "rel_cz") {
            scr_vn_start_episode("ep_ceasefire_zaibatsu_tharsis");
        }
    }
};

// 7g. Broker Coalition Alliance
broker_alliance = function(_pair_id, _duration, _reason) {
    var _rel = get_relation_by_id(_pair_id);
    if (is_undefined(_rel)) return;

    _rel.state = "ALLIANCE";
    _rel.tension = max(20, _rel.tension - 25);
    _rel.treaty_turns_left = _duration;
    _rel.treaty_max_turns = _duration;
    _rel.war_duration_turns = 0;
    _rel.last_event_turn = (instance_exists(obj_GameManager)) ? obj_GameManager.current_turn : 1;

    var _title = "MUTUAL DEFENSE ALLIANCE: " + string_upper(_rel.name_1) + " + " + string_upper(_rel.name_2);
    var _body = "Military alliance ratified for " + string(_duration) + " turns. Joint defense pact established. " + _reason;
    add_diplomatic_cable(_rel.name_1, _rel.name_2, _title, _body, "HIGH", "ALLIANCE");
};

// 7h. Turn Evaluation: Faction AI Geopolitical Simulation (docs/21)
evaluate_faction_ai_turn = function() {
    var _keys = variable_struct_get_names(diplomatic_relations);

    for (var k = 0; k < array_length(_keys); k++) {
        var _pid = _keys[k];
        var _rel = variable_struct_get(diplomatic_relations, _pid);

        // 1. Decrement treaty countdowns
        if (_rel.treaty_turns_left > 0) {
            _rel.treaty_turns_left -= 1;
        }

        // 2. State-Specific Dynamics & Mathematical Balancing (docs/21)
        switch (_rel.state) {
            case "ALLIANCE":
                // Core Rule: Alliance Paranoia (+2.5 Tension/turn) to ensure alliances are NOT permanent!
                _rel.tension = min(100, _rel.tension + 2.5);

                // Check for treaty expiration or paranoia fracture (tension >= 75)
                if (_rel.treaty_turns_left <= 0 || _rel.tension >= 75) {
                    if (_rel.tension >= 85) {
                        declare_war(_pid, "Alliance shattered in betrayal after covert espionage incident!");
                    } else {
                        set_diplomatic_state(_pid, "COLD_WAR", 0, "Alliance expired amidst mutual suspicion and border friction.");
                    }
                }
                break;

            case "TRUCE":
                // Truce Exhaustion: Tension cools by -2.0 per turn
                _rel.tension = max(0, _rel.tension - 2.0);

                // Check for truce expiration
                if (_rel.treaty_turns_left <= 0) {
                    if (_rel.tension >= 60) {
                        set_diplomatic_state(_pid, "COLD_WAR", 0, "Ceasefire accord expired with unresolved territorial grievances.");
                    } else {
                        set_diplomatic_state(_pid, "NON_AGGRESSION", 0, "Ceasefire normalized into fragile border non-aggression.");
                    }
                }
                break;

            case "COLD_WAR":
                // Drift by Base Friction + minor variance
                var _c_drift = _rel.base_friction + irandom_range(-1, 2);
                _rel.tension = clamp(_rel.tension + _c_drift, 0, 100);

                if (_rel.tension >= 85) {
                    declare_war(_pid, "Covert skirmishes breached the threshold of full-scale warfare.");
                }
                break;

            case "NON_AGGRESSION":
                // Low tension drift
                var _n_drift = (_rel.base_friction * 0.5) + irandom_range(-1, 1);
                _rel.tension = clamp(_rel.tension + _n_drift, 0, 100);

                if (_rel.tension >= 50) {
                    set_diplomatic_state(_pid, "COLD_WAR", 0, "Ideological tension and trade tariffs eroded non-aggression pact.");
                }
                break;

            case "WAR":
                _rel.war_duration_turns += 1;
                // War exhaustion rolls after prolonged conflict (10+ turns)
                if (_rel.war_duration_turns >= 10 && random(100) < 22.0) {
                    broker_truce(_pid, irandom_range(10, 18), "Severe military attrition forces both factions to accept armistice terms.");
                }
                break;
        }
    }

    // 3. Balance-of-Power Anti-Blobbing (Rubber-Banding, docs/21)
    // Check if any single faction controls > 40% of Sol territory
    var _tc = territory_control;
    var _pcts = [
        { id: "faction_a", name: "The Terran Coalition", pct: variable_struct_get(_tc, "terran_pct") ?? 35 },
        { id: "faction_b", name: "The Outer Colonies", pct: variable_struct_get(_tc, "colony_pct") ?? 28 },
        { id: "faction_c", name: "Rogue Mercenary Syndicates", pct: variable_struct_get(_tc, "syndicate_pct") ?? 14 },
        { id: "faction_d", name: "Apex Bio-Cybernetics Zaibatsu", pct: variable_struct_get(_tc, "zaibatsu_pct") ?? 11 },
        { id: "faction_e", name: "The Sidereal Sovereign League", pct: variable_struct_get(_tc, "astran_pct") ?? 12 },
        { id: "faction_f", name: "The Tharsis Machine Consensus", pct: variable_struct_get(_tc, "martian_pct") ?? 0 }
    ];

    var _hegemon = undefined;
    for (var p = 0; p < array_length(_pcts); p++) {
        if (_pcts[p].pct >= 40) {
            _hegemon = _pcts[p];
            break;
        }
    }

    if (!is_undefined(_hegemon)) {
        hegemon_faction_id = _hegemon.id;
        coalition_active = true;

        // Threat surge: Decrease bilateral tensions between the other 3 factions by -15
        for (var k2 = 0; k2 < array_length(_keys); k2++) {
            var _r2 = variable_struct_get(diplomatic_relations, _keys[k2]);
            if (_r2.faction_1 != _hegemon.id && _r2.faction_2 != _hegemon.id) {
                _r2.tension = max(10, _r2.tension - 2.0);

                // Auto-broker Emergency Coalition Alliance if in Cold War or Non-Aggression
                if (_r2.state != "ALLIANCE" && _r2.state != "WAR" && _r2.tension < 55) {
                    broker_alliance(_keys[k2], irandom_range(12, 20), "EMERGENCY COALITION: United defense pact formed against dominant " + _hegemon.name + " (" + string(_hegemon.pct) + "% Sol Control)!");
                }
            }
        }
    } else if (coalition_active) {
        // Hegemon was beaten back below 38%
        var _max_pct = max(_tc.terran_pct, _tc.colony_pct, _tc.syndicate_pct, _tc.zaibatsu_pct);
        if (_max_pct < 35) {
            coalition_active = false;
            hegemon_faction_id = "";
            add_diplomatic_cable("Solar Council", "All Factions", "COALITION DISSOLVED: Sol Balance Restored", "Anti-hegemonic emergency measures deactivated as territory balances re-stabilize.", "NORMAL", "COLD_WAR");
        }
    }

    // 4. Individual Faction AI Brains & Dynamic Behavioral State Evaluation (docs/36, docs/37)
    var _f_ids = ["faction_a", "faction_b", "faction_c", "faction_d", "faction_e", "faction_f"];
    for (var fi = 0; fi < array_length(_f_ids); fi++) {
        var _fid = _f_ids[fi];
        var _f = variable_struct_get(factions, _fid);
        var _fpct = 20;
        if (_fid == "faction_a") _fpct = variable_struct_get(_tc, "terran_pct") ?? 35;
        else if (_fid == "faction_b") _fpct = variable_struct_get(_tc, "colony_pct") ?? 28;
        else if (_fid == "faction_c") _fpct = variable_struct_get(_tc, "syndicate_pct") ?? 14;
        else if (_fid == "faction_d") _fpct = variable_struct_get(_tc, "zaibatsu_pct") ?? 11;
        else if (_fid == "faction_e") _fpct = variable_struct_get(_tc, "astran_pct") ?? 12;
        else if (_fid == "faction_f") _fpct = variable_struct_get(_tc, "martian_pct") ?? 0;

        // Special handling: Tharsis Machine Consensus Awakening (Doc 37, Doc 39)
        if (_fid == "faction_f" && ((variable_struct_get(_f, "is_dormant") ?? false) || !mars_unlocked)) {
            var _cur_turn = (instance_exists(obj_GameManager)) ? obj_GameManager.current_turn : 1;
            if (_cur_turn >= 15) {
                _f.is_dormant = false;
                if (!mars_unlocked) {
                    scr_territory_unlock_mars();
                }
            }
        }

        // Check if currently engaged in active WAR with any faction
        var _in_war = false;
        for (var wk = 0; wk < array_length(_keys); wk++) {
            var _wrel = variable_struct_get(diplomatic_relations, _keys[wk]);
            if ((_wrel.faction_1 == _fid || _wrel.faction_2 == _fid) && _wrel.state == "WAR") {
                _in_war = true;
                break;
            }
        }

        var _old_ai_state = variable_struct_get(_f, "ai_state") ?? "PEACE";

        // DESPERATE STATE: Territory <= 18% OR Military Strength <= 25
        if (_fpct <= 18 || _f.military_strength_score <= 25) {
            _f.ai_state = "DESPERATE";
            _f.contract_bounty_multiplier = 2.0; // Emergency bailout tenders pay +100% bounties!
            if (!_f.superweapon_unsealed) {
                _f.superweapon_unsealed = true;
                var _sw_name = variable_struct_get(_f, "superweapon_name") ?? "Apex Prototype";
                add_diplomatic_cable(_f.name, "All Solar Factions", "EMERGENCY MEASURE: UNSEALED FORBIDDEN WARFRAME", _f.name + " unseals forbidden warframe [" + _sw_name + "] and issues emergency PMC bailout tenders (+100% Bounty)!", "URGENT", "WAR");
            }
        }
        // WINNING STATE: Territory >= 38% OR Military Strength >= 70
        else if (_fpct >= 38 || _f.military_strength_score >= 70) {
            _f.ai_state = "WINNING";
            _f.contract_bounty_multiplier = 0.85; // Imperial hubris squeezes mercenary profit margins
            if (_old_ai_state != "WINNING") {
                add_diplomatic_cable(_f.name, "All Solar Factions", "HEGEMONIC ASCENDANCY CLAIMED", _f.name + " claims strategic superiority across Sol. Planetary tariffs and mineral quotas enforced.", "HIGH", "COLD_WAR");
            }
        }
        // STANDARD WAR
        else if (_in_war) {
            _f.ai_state = "STANDARD_WAR";
            _f.contract_bounty_multiplier = 1.25;
        }
        // PEACE
        else {
            _f.ai_state = "PEACE";
            _f.contract_bounty_multiplier = 1.0;
        }
    }
};

// 7i-2. Flagship Fleet Siege Evaluator (Doc 64 - Hostile Faction Full Fleet Assault)
evaluate_flagship_siege_assault = function() {
    var _f_keys = ["faction_a", "faction_b", "faction_c", "faction_d"];
    for (var i = 0; i < array_length(_f_keys); i++) {
        var _fid = _f_keys[i];
        var _std = get_standing(_fid);
        var _f = variable_struct_exists(factions, _fid) ? variable_struct_get(factions, _fid) : undefined;
        if (!is_undefined(_f) && is_struct(_f)) {
            if (variable_struct_exists(_f, "siege_cooldown") && _f.siege_cooldown > 0) {
                _f.siege_cooldown--;
            }
            if (_std <= -80 && (!variable_struct_exists(_f, "siege_cooldown") || _f.siege_cooldown <= 0)) {
                _f.siege_cooldown = 15; // 15 turns between full armada assault incursions
                var _f_name = variable_struct_exists(_f, "name") ? _f.name : "Hostile Superpower";
                
                add_diplomatic_cable(_f_name, "PMC Hephaestus", "TOTAL WAR: OPERATION FORGE BREACH", 
                    _f_name + " high command drops all restraint. An armada task force has been dispatched to execute [OPERATION FORGE BREACH] and storm the Hephaestus foundry ship directly!", 
                    "URGENT", "WAR");
                    
                if (instance_exists(obj_HQTerminal)) {
                    obj_HQTerminal.show_toast("RED ALERT: " + _f_name + " ARMADA INTERCEPTING FLAGSHIP!", c_red);
                }
                
                return {
                    active: true,
                    faction_id: _fid,
                    faction_name: _f_name,
                    title: "OPERATION FORGE BREACH: FLAGSHIP UNDER SIEGE"
                };
            }
        }
    }
    return { active: false };
};

// 7i. Player Mercenary Diplomatic Actions (docs/21)
player_broker_ceasefire = function(_pair_id) {
    if (!instance_exists(obj_GameManager)) return false;
    var _gm = obj_GameManager;
    var _cost = 50000;
    if (_gm.funds < _cost) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT FUNDS: Ceasefire diplomacy costs " + string(_cost) + " Cr!", c_red);
        return false;
    }

    var _rel = get_relation_by_id(_pair_id);
    if (is_undefined(_rel)) return false;
    if (_rel.state != "WAR") {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("CANNOT BROKER TRUCE: Factions are not at WAR!", c_yellow);
        return false;
    }

    _gm.funds -= _cost;
    broker_truce(_pair_id, 14, "PMC diplomatic envoy negotiated ceasefire accord.");
    if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("CEASEFIRE RATIFIED: " + _rel.name_1 + " & " + _rel.name_2 + " sign 14-turn truce (-50,000 Cr)!", c_lime);
    return true;
};

player_provoke_crisis = function(_pair_id) {
    if (!instance_exists(obj_GameManager)) return false;
    var _gm = obj_GameManager;
    var _cost = 40000;
    if (_gm.funds < _cost) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT FUNDS: False-flag strike costs " + string(_cost) + " Cr!", c_red);
        return false;
    }

    var _rel = get_relation_by_id(_pair_id);
    if (is_undefined(_rel)) return false;

    _gm.funds -= _cost;
    modify_bilateral_tension(_pair_id, 25, "PMC false-flag provocation escalated border crisis.");
    if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("PROVOCATION SUCCESSFUL: Tension spiked +25 between " + _rel.name_1 + " and " + _rel.name_2 + " (-40,000 Cr)!", c_orange);
    return true;
};

player_negotiate_coalition = function(_pair_id) {
    if (!instance_exists(obj_GameManager)) return false;
    var _gm = obj_GameManager;
    var _cost = 60000;
    if (_gm.funds < _cost) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT FUNDS: Coalition pact costs " + string(_cost) + " Cr!", c_red);
        return false;
    }

    var _rel = get_relation_by_id(_pair_id);
    if (is_undefined(_rel)) return false;
    if (_rel.state == "WAR") {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("CANNOT ALLY: Factions are actively at WAR! Broker a truce first.", c_red);
        return false;
    }

    _gm.funds -= _cost;
    broker_alliance(_pair_id, 18, "PMC-brokered defense treaty ratified.");
    if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("ALLIANCE RATIFIED: 18-turn Mutual Defense Treaty between " + _rel.name_1 + " and " + _rel.name_2 + " (-60,000 Cr)!", c_aqua);
    return true;
};

// 7j. Dynamic Macro War Map Simulation (Refactored with 6-Pair Diplomacy & Alliances)
simulate_war_turn = function() {
    var _t_bonus = (mass_production_contracts.faction_a.replaced) ? mass_production_contracts.faction_a.combat_bonus : 0;
    var _c_bonus = (mass_production_contracts.faction_b.replaced) ? mass_production_contracts.faction_b.combat_bonus : 0;
    var _s_bonus = (mass_production_contracts.faction_c.replaced) ? mass_production_contracts.faction_c.combat_bonus : 0;
    var _z_bonus = (mass_production_contracts.faction_d.replaced) ? mass_production_contracts.faction_d.combat_bonus : 0;

    // Check Alliance Defense Reinforcement (+12 power per active ally)
    var _allies_t = 0;
    var _allies_c = 0;
    var _allies_s = 0;
    var _allies_z = 0;

    var _keys = variable_struct_get_names(diplomatic_relations);
    for (var k = 0; k < array_length(_keys); k++) {
        var _r = variable_struct_get(diplomatic_relations, _keys[k]);
        if (_r.state == "ALLIANCE") {
            if (_r.faction_1 == "faction_a" || _r.faction_2 == "faction_a") _allies_t += 12;
            if (_r.faction_1 == "faction_b" || _r.faction_2 == "faction_b") _allies_c += 12;
            if (_r.faction_1 == "faction_c" || _r.faction_2 == "faction_c") _allies_s += 12;
            if (_r.faction_1 == "faction_d" || _r.faction_2 == "faction_d") _allies_z += 12;
        }
    }

    var _terran_pwr    = factions.faction_a.military_strength_score + _t_bonus + _allies_t;
    var _colony_pwr    = factions.faction_b.military_strength_score + _c_bonus + _allies_c;
    var _syndicate_pwr = factions.faction_c.military_strength_score + _s_bonus + _allies_s;
    var _zaibatsu_pwr  = factions.faction_d.military_strength_score + _z_bonus + _allies_z;

    var _clash_reports = [];

    // Gundam-Style Planetary & Orbital Territory Clashes (Doc 39)
    var _territory_clash_reports = scr_territory_simulate_faction_clash();
    for (var tcr = 0; tcr < array_length(_territory_clash_reports); tcr++) {
        array_push(_clash_reports, _territory_clash_reports[tcr]);
    }

    // Clash 1: Terran vs Colony (if at WAR)
    var _rel_tc = get_relation("faction_a", "faction_b");
    if (!is_undefined(_rel_tc) && _rel_tc.state == "WAR") {
        var _clash = (_terran_pwr - _colony_pwr) + irandom_range(-6, 6);
        if (_clash > 4 && territory_control.colony_pct > 5) {
            var _shift = irandom_range(1, 3);
            territory_control.terran_pct = min(75, territory_control.terran_pct + _shift);
            territory_control.colony_pct = max(0, territory_control.colony_pct - _shift);
            var _rep = (mass_production_contracts.faction_a.replaced) ? 
                ("Terran Coalition fielding " + mass_production_contracts.faction_a.replacement_name + " captures orbital sector (+ " + string(_shift) + "% control)!") :
                ("Terran armored line breaches Colony defenses in Sector 4 (+ " + string(_shift) + "% control)!");
            array_push(_clash_reports, _rep);
        } else if (_clash < -4 && territory_control.terran_pct > 5) {
            var _shift = irandom_range(1, 3);
            territory_control.colony_pct = min(75, territory_control.colony_pct + _shift);
            territory_control.terran_pct = max(0, territory_control.terran_pct - _shift);
            var _rep = (mass_production_contracts.faction_b.replaced) ?
                ("Colony aces in " + mass_production_contracts.faction_b.replacement_name + " shatter Terran line (+ " + string(_shift) + "% control)!") :
                ("Outer Colonies space wing seizes Terran staging perimeter (+ " + string(_shift) + "% control)!");
            array_push(_clash_reports, _rep);
        }
    }

    // Clash 2: Syndicate Opportunism / War vs Terran
    var _rel_ts = get_relation("faction_a", "faction_c");
    if (!is_undefined(_rel_ts) && _rel_ts.state == "WAR" && territory_control.terran_pct > 5) {
        if (_syndicate_pwr >= 35 && random(100) < 45) {
            territory_control.syndicate_pct = min(35, territory_control.syndicate_pct + 1);
            territory_control.terran_pct = max(0, territory_control.terran_pct - 1);
            array_push(_clash_reports, "Rogue Syndicates conduct hit-and-run raids on Terran supply depots (+1% Syndicate)!");
        }
    }

    // Clash 3: Zaibatsu Operations
    var _rel_cz = get_relation("faction_b", "faction_d");
    if (!is_undefined(_rel_cz) && _rel_cz.state == "WAR" && territory_control.colony_pct > 5) {
        if (_zaibatsu_pwr >= 45 && random(100) < 40) {
            territory_control.zaibatsu_pct = min(35, territory_control.zaibatsu_pct + 1);
            territory_control.colony_pct = max(0, territory_control.colony_pct - 1);
            array_push(_clash_reports, "Apex Zaibatsu cyber-legions seize Jovian mining nodes from Colonies (+1% Zaibatsu)!");
        }
    }

    // Rebalance total percentages to ensure 100% total (accounting for PMC dominion)
    var _total_factions = territory_control.terran_pct + territory_control.colony_pct + territory_control.syndicate_pct + territory_control.zaibatsu_pct;
    var _target_total = 100 - territory_control.pmc_pct;
    if (_total_factions != _target_total && _total_factions > 0) {
        var _diff = _target_total - _total_factions;
        territory_control.terran_pct = max(2, territory_control.terran_pct + _diff);
    }

    if (array_length(_clash_reports) > 0) {
        territory_control.last_shift_report = _clash_reports[0];
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("WAR INTEL: " + _clash_reports[0], c_yellow);
        }
    } else {
        territory_control.last_shift_report = "Frontlines static across Sol sectors. Defensive fortifications holding.";
    }
};


// 7b. Pitch Mass-Production Replacement Doctrine (docs/12)
pitch_mass_production_replacement = function(_faction_id, _blueprint_id, _custom_name) {
    if (!variable_struct_exists(mass_production_contracts, _faction_id)) return false;
    var _mp = variable_struct_get(mass_production_contracts, _faction_id);
    if (_mp.replaced) {
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("ALREADY LICENSED: " + _mp.faction_name + " already mass-produces your " + _mp.replacement_name + "!", c_yellow);
        }
        return false;
    }

    var _std = get_standing(_faction_id);
    if (_std < 10) {
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("REJECTED: Standing with " + _mp.faction_name + " too low (" + string(_std) + "/10 needed)!", c_red);
        }
        return false;
    }

    var _has_physical_sample = false;
    if (instance_exists(obj_GameManager)) {
        _has_physical_sample = (array_length(obj_GameManager.inventory.deployable_mechs) > 0);
    }
    if (!_has_physical_sample) {
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("REJECTED: Must have at least 1 functional prototype in Hangar for Ordnance trials!", c_red);
        }
        return false;
    }

    _mp.replaced = true;
    _mp.replacement_blueprint_id = _blueprint_id;
    _mp.replacement_name = (_custom_name != "") ? _custom_name : "Player Proprietary Chassis";

    if (instance_exists(obj_GameManager)) {
        obj_GameManager.add_funds(_mp.licensing_bounty);
    }

    modify_standing(_faction_id, 35);
    if (variable_struct_exists(factions, _faction_id)) {
        variable_struct_get(factions, _faction_id).military_strength_score = min(100, variable_struct_get(factions, _faction_id).military_strength_score + 15);
    }

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("DOCTRINE RATIFIED! " + _mp.faction_name + " adopts " + _mp.replacement_name + "! +" + string(_mp.licensing_bounty) + " Cr Bounty!", c_lime);
    }
    return true;
};

// 7c. Launch Strategic PMC Offensive to Seize Territory & Overthrow Factions (docs/12)
launch_pmc_offensive = function(_target_faction_id, _mech_idx, _pilot_idx) {
    if (!instance_exists(obj_GameManager)) return false;
    var _gm = obj_GameManager;

    if (_mech_idx < 0 || _mech_idx >= array_length(_gm.inventory.deployable_mechs)) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("NO MECH SELECTED FOR OFFENSIVE!", c_red);
        return false;
    }
    if (_pilot_idx < 0 || _pilot_idx >= array_length(_gm.facilities.roster_pilots)) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("NO PILOT SELECTED FOR OFFENSIVE!", c_red);
        return false;
    }

    var _mech = _gm.inventory.deployable_mechs[_mech_idx];
    var _pilot = _gm.facilities.roster_pilots[_pilot_idx];

    if (_mech.status != "READY") {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("SELECTED MECH IS NOT COMBAT READY!", c_red);
        return false;
    }
    if (_pilot.status != "ACTIVE") {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("PILOT IS CURRENTLY UNAVAILABLE / HOSPITALIZED!", c_red);
        return false;
    }

    var _tf = variable_struct_get(factions, _target_faction_id);
    if (is_undefined(_tf)) return false;

    pmc_expeditions_launched += 1;

    var _pilot_cstat = variable_struct_get(_pilot, "combat_stat") ?? floor((variable_struct_get(_pilot, "accuracy") ?? 80) / 10);
    var _pmc_pwr = _mech.armor_rating + _mech.power_output + (_pilot_cstat * 12) + irandom_range(15, 40);
    var _def_pwr = _tf.military_strength_score * 1.8 + irandom_range(10, 30);

    if (_pmc_pwr >= _def_pwr) {
        var _captured = irandom_range(3, 6);
        var _t_key = (_target_faction_id == "faction_a") ? "terran_pct" : ((_target_faction_id == "faction_b") ? "colony_pct" : ((_target_faction_id == "faction_c") ? "syndicate_pct" : "zaibatsu_pct"));
        var _cur_t = variable_struct_get(territory_control, _t_key);
        var _actual_taken = min(_cur_t, _captured);

        variable_struct_set(territory_control, _t_key, max(0, _cur_t - _actual_taken));
        territory_control.pmc_pct = min(100, territory_control.pmc_pct + _actual_taken);

        _tf.military_strength_score = max(0, _tf.military_strength_score - 10);
        modify_standing(_target_faction_id, -30);

        var _salvage_cr = irandom_range(180000, 380000);
        _gm.add_funds(_salvage_cr);
        _gm.add_raw_material("mat_tungsten", irandom_range(2, 5));
        _gm.add_raw_material("mat_tritium", irandom_range(1, 3));
        _gm.total_sorties_won += 1;

        if (variable_struct_get(territory_control, _t_key) <= 0 || _tf.military_strength_score <= 5) {
            variable_struct_set(territory_control, _t_key, 0);
            _tf.military_strength_score = 0;
            _tf.standing_title = "OVERTHROWN / ANNEXED";
            if (array_get_index(factions_overthrown, _target_faction_id) == -1) {
                array_push(factions_overthrown, _target_faction_id);
            }
            territory_control.last_shift_report = "PMC OVERTHROW: " + _tf.name + " collapsed! All territory annexed into PMC Hegemony!";
            if (instance_exists(obj_HQTerminal)) {
                obj_HQTerminal.show_toast("FACTION OVERTHROWN! " + _tf.name + " ANNEXED BY YOUR PMC!", c_yellow);
            }
        } else {
            territory_control.last_shift_report = "PMC VICTORY: Seized " + string(_actual_taken) + "% territory from " + _tf.name + "!";
            if (instance_exists(obj_HQTerminal)) {
                obj_HQTerminal.show_toast("PMC VICTORY! Captured " + string(_actual_taken) + "% territory! Salvaged +" + string(_salvage_cr) + " Cr!", c_lime);
            }
        }
        return true;
    } else {
        _mech.status = "DAMAGED";
        _pilot.status = "HOSPITALIZED";
        _pilot.recovery_days_left = 3;
        _pilot.recovery_days = 3;
        modify_standing(_target_faction_id, -15);
        territory_control.last_shift_report = "PMC OFFENSIVE REPELLED: " + _tf.name + " defensive garrison held line.";
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("OFFENSIVE REPELLED! Mech damaged, pilot hospitalized for 3 turns!", c_red);
        }
        return false;
    }
};

// 8. Contract Methods & Fulfillments (docs/04)
accept_contract = function(_contract_id) {
    var _count = array_length(available_contracts);
    for (var i = 0; i < _count; i++) {
        if (variable_struct_get(available_contracts[i], "id") == _contract_id) {
            var _c = available_contracts[i];
            array_delete(available_contracts, i, 1);
            array_push(active_contracts, _c);
            if (instance_exists(obj_HQTerminal)) {
                obj_HQTerminal.show_toast("CONTRACT ACCEPTED: " + _c.title, c_lime);
            }
            return true;
        }
    }
    return false;
};

fulfill_contract = function(_contract_id) {
    if (!instance_exists(obj_GameManager)) return false;

    for (var c = 0; c < array_length(active_contracts); c++) {
        var _cnt = active_contracts[c];
        if (_cnt.id == _contract_id) {
            // Calculate dynamic AI bounty multiplier (docs/36)
            var _b_mult = 1.0;
            if (variable_struct_exists(factions, _cnt.faction)) {
                _b_mult = variable_struct_get(variable_struct_get(factions, _cnt.faction), "contract_bounty_multiplier") ?? 1.0;
            }
            var _final_payout = round(_cnt.payout_credits * _b_mult);

            // A. Mass Production Order Fulfillment
            if (_cnt.type == "MASS_PRODUCTION") {
                // Check if player has ready mech in hangar
                var _found_idx = -1;
                for (var m = 0; m < array_length(obj_GameManager.inventory.deployable_mechs); m++) {
                    if (obj_GameManager.inventory.deployable_mechs[m].status == "READY") {
                        _found_idx = m;
                        break;
                    }
                }
                if (_found_idx == -1) {
                    if (instance_exists(obj_HQTerminal)) {
                        obj_HQTerminal.show_toast("REQUIREMENT UNMET: Need 1 READY mobile suit in hangar!", c_red);
                    }
                    return false;
                }
                // Deliver mech
                array_delete(obj_GameManager.inventory.deployable_mechs, _found_idx, 1);
                obj_GameManager.add_funds(_final_payout);
                modify_standing(_cnt.faction, _cnt.reputation_gain);
                factions.faction_a.military_strength_score = min(100, factions.faction_a.military_strength_score + 8);
                array_delete(active_contracts, c, 1);
                if (instance_exists(obj_HQTerminal)) {
                    var _note = (_b_mult > 1.0) ? " (EMERGENCY +100% BOUNTY)!" : "!";
                    obj_HQTerminal.show_toast("ORDER DELIVERED: +" + string(_final_payout) + " Cr" + _note + " Terran Military Strength +8", c_lime);
                }
                return true;
            }

            // B. Prototype Bounty Fulfillment
            else if (_cnt.type == "PROTOTYPE_BOUNTY") {
                // Check if player forged masterwork in obj_BlueprintManager
                var _has_mw = false;
                if (instance_exists(obj_BlueprintManager)) {
                    _has_mw = (array_length(obj_BlueprintManager.masterwork_inventory) > 0);
                }
                if (!_has_mw) {
                    if (instance_exists(obj_HQTerminal)) {
                        obj_HQTerminal.show_toast("REQUIREMENT UNMET: Must tune Masterwork in R&D Lab first!", c_red);
                    }
                    return false;
                }
                // Deliver masterwork
                array_delete(obj_BlueprintManager.masterwork_inventory, 0, 1);
                obj_GameManager.add_funds(_final_payout);
                obj_GameManager.add_raw_material(_cnt.reward_material_id, _cnt.reward_material_amount);
                modify_standing(_cnt.faction, _cnt.reputation_gain);
                factions.faction_b.military_strength_score = min(100, factions.faction_b.military_strength_score + 10);
                array_delete(active_contracts, c, 1);
                if (instance_exists(obj_HQTerminal)) {
                    var _note = (_b_mult > 1.0) ? " (EMERGENCY BAILOUT BONUS)!" : "!";
                    obj_HQTerminal.show_toast("BOUNTY DELIVERED: +" + string(_final_payout) + " Cr" + _note + " & +" + string(_cnt.reward_material_amount) + " Tritium! Colony Strength +10", c_lime);
                }
                return true;
            }

            // C. Black Ops Sale (High risk / instant cash)
            else if (_cnt.type == "BLACK_OPS_SALE") {
                obj_GameManager.add_funds(_final_payout);
                obj_GameManager.add_raw_material(_cnt.reward_material_id, _cnt.reward_material_amount);
                modify_standing(_cnt.faction, _cnt.reputation_gain);
                factions.faction_c.military_strength_score = min(100, factions.faction_c.military_strength_score + 12);
                array_delete(active_contracts, c, 1);

                // Roll Tech Leak Risk
                var _leak_roll = random(100);
                if (_leak_roll < _cnt.tech_leak_risk_pct) {
                    obj_GameManager.trigger_event_by_id("event_syndicate_leak");
                } else {
                    if (instance_exists(obj_HQTerminal)) {
                        obj_HQTerminal.show_toast("BLACK OPS SALE SUCCESSFUL: +" + string(_cnt.payout_credits) + " Cr & +" + string(_cnt.reward_material_amount) + " Flux! Syndicate Strength +12", c_aqua);
                    }
                }
                return true;
            }
        }
    }
    return false;
};

show_debug_message("[obj_FactionManager] Contract engine initialized with dynamic war simulation.");

// 9. Load Expanded Faction Lore & Mobile Suits Lineage Databases (JSON with try/catch)
factions_lore_data = undefined;
timeline_suits_data = [];

if (file_exists("factions_lore.json")) {
    try {
        var _buf_fl = buffer_load("factions_lore.json");
        var _json_str = buffer_read(_buf_fl, buffer_string);
        buffer_delete(_buf_fl);
        factions_lore_data = json_parse(_json_str);
        show_debug_message("[obj_FactionManager] Loaded factions_lore.json successfully.");
    } catch (_ex) {
        show_debug_message("[obj_FactionManager] Warning: could not parse factions_lore.json: " + string(_ex));
    }
}

if (file_exists("mobile_suits_timeline.json")) {
    try {
        var _buf_tl = buffer_load("mobile_suits_timeline.json");
        var _json_str2 = buffer_read(_buf_tl, buffer_string);
        buffer_delete(_buf_tl);
        var _t_parsed = json_parse(_json_str2);
        if (variable_struct_exists(_t_parsed, "mobile_suits")) {
            timeline_suits_data = _t_parsed.mobile_suits;
        }
        show_debug_message("[obj_FactionManager] Loaded mobile_suits_timeline.json (" + string(array_length(timeline_suits_data)) + " suits).");
    } catch (_ex) {
        show_debug_message("[obj_FactionManager] Warning: could not parse mobile_suits_timeline.json: " + string(_ex));
    }
}

// 10. Faction Procurement Trials & Competitive Fly-Off Arena (docs/15)
incumbent_doctrines = {
    faction_a: {
        id: "GHA-07",
        name: "GHA-07 Ironclad",
        faction_name: "The Terran Coalition",
        role: "Heavy Trench Assault & Frontline Wall",
        armor: 850,
        power: 12,
        speed: 45,
        mass: 92,
        combat_rating: 480,
        weights: [0.40, 0.15, 0.10, 0.35],
        doctrine_focus: "Heavy Armor & Kinetic Slug Volume",
        evaluator: "General Hector Vance (Terran Munitions Board)"
    },
    faction_b: {
        id: "AET-01",
        name: "AET-01 Aether",
        faction_name: "The Outer Colonies",
        role: "Orbital Interceptor & Energy Striker",
        armor: 640,
        power: 16,
        speed: 120,
        mass: 64,
        combat_rating: 510,
        weights: [0.10, 0.30, 0.40, 0.20],
        doctrine_focus: "High-G Vernier Agility & Fusion Surplus",
        evaluator: "Minister Jun Takahashi (Colony Defense Council)"
    },
    faction_c: {
        id: "SCR-12",
        name: "SCR-12 Hyena",
        faction_name: "Rogue Mercenary Syndicates",
        role: "Guerilla Raider & Resource Scavenger",
        armor: 720,
        power: 10,
        speed: 75,
        mass: 70,
        combat_rating: 440,
        weights: [0.25, 0.15, 0.25, 0.35],
        doctrine_focus: "Cost Efficiency & Armor-Piercing Punch",
        evaluator: "Kruger 'Iron-Eye' (Black Market Boss)"
    },
    faction_d: {
        id: "ZAI-03",
        name: "ZAI-03 Muramasa",
        faction_name: "Apex Bio-Cybernetics Zaibatsu",
        role: "Transhuman Cyber-Striker & Electronic Warfare",
        armor: 780,
        power: 18,
        speed: 95,
        mass: 78,
        combat_rating: 560,
        weights: [0.20, 0.25, 0.25, 0.30],
        doctrine_focus: "Balanced Neural Response & Energy Precision",
        evaluator: "Director Renzo Takahashi (Apex Procurement Bureau)"
    }
};

get_incumbent_specs = function(_faction_id) {
    var _base = variable_struct_exists(incumbent_doctrines, _faction_id) ? variable_struct_get(incumbent_doctrines, _faction_id) : incumbent_doctrines.faction_a;

    // Dynamically query mass_production_contracts for active playthrough line chassis (docs/29)
    if (variable_struct_exists(mass_production_contracts, _faction_id)) {
        var _mpc = variable_struct_get(mass_production_contracts, _faction_id);
        if (is_struct(_mpc) && variable_struct_exists(_mpc, "baseline_suit_name")) {
            _base.name = _mpc.baseline_suit_name;
            variable_struct_set(_base, "id", _mpc.baseline_suit_id);
            _base.armor = _mpc.req_armor * 10;
            _base.power = _mpc.req_power;
            _base.doctrine_focus = variable_struct_get(_mpc, "doctrine") ?? _base.doctrine_focus;
        }
    }

    // Dynamically query competitor catalog for active era chassis (docs/27)
    if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "competitor_catalog")) {
        var _corp_map = { faction_a: "corp_vhi", faction_b: "corp_aod", faction_c: "corp_rust", faction_d: "corp_hats" };
        var _cid = variable_struct_get(_corp_map, _faction_id) ?? "corp_vhi";
        if (variable_struct_exists(obj_GameManager.competitor_catalog, _cid)) {
            var _cp = variable_struct_get(obj_GameManager.competitor_catalog, _cid);
            if (!is_undefined(_cp.active_line_chassis)) {
                return {
                    id: _cp.active_line_chassis.id,
                    name: _cp.active_line_chassis.name,
                    faction_name: _base.faction_name,
                    role: _cp.active_line_chassis.class + " (" + _cp.branch_name + ")",
                    armor: _cp.active_line_chassis.armor,
                    power: _cp.active_line_chassis.power,
                    speed: _cp.active_line_chassis.speed,
                    mass: _base.mass,
                    combat_rating: _cp.active_line_chassis.combat,
                    weights: _base.weights,
                    doctrine_focus: _cp.doctrine,
                    evaluator: _base.evaluator
                };
            }
        }
    }
    return _base;
};

run_procurement_trial = function(_faction_id, _mech) {
    var _inc = get_incumbent_specs(_faction_id);
    if (is_undefined(_mech)) return undefined;

    var _cand_armor = variable_struct_get(_mech, "armor_rating") ?? 600;
    var _cand_power = variable_struct_get(_mech, "power_output") ?? 10;
    var _cand_speed = variable_struct_get(_mech, "speed") ?? 60;
    var _cand_combat = variable_struct_get(_mech, "combat_rating") ?? 400;

    // 4 Diagnostic Phase Scores (Base 100 is exact parity with incumbent)
    var _score_armor = clamp((_cand_armor / max(1, _inc.armor)) * 100.0, 20.0, 160.0);
    var _score_power = clamp((_cand_power / max(1, _inc.power)) * 100.0, 20.0, 160.0);
    var _score_speed = clamp((_cand_speed / max(1, _inc.speed)) * 100.0, 20.0, 160.0);
    var _score_combat = clamp((_cand_combat / max(1, _inc.combat_rating)) * 100.0, 20.0, 160.0);

    var _w = _inc.weights;
    var _base_weighted = (_score_armor * _w[0]) + (_score_power * _w[1]) + (_score_speed * _w[2]) + (_score_combat * _w[3]);

    // Faction Standing Bonus (-20 to +20)
    var _st_bonus = get_standing(_faction_id) / 5.0;

    // Combat-Proven Pedigree Telemetry Bonus (0 to 25 pts) from active PMC squad deployments (docs/25)
    var _pedigree_bonus = 0.0;
    var _pedigree_rating = "UNTESTED";
    if (variable_struct_exists(_mech, "combat_pedigree") && is_struct(_mech.combat_pedigree)) {
        _pedigree_bonus = variable_struct_get(_mech.combat_pedigree, "telemetry_bonus") ?? 0.0;
        _pedigree_rating = variable_struct_get(_mech.combat_pedigree, "pedigree_rating") ?? "UNTESTED";
    }

    var _composite_score = round((_base_weighted + _st_bonus + _pedigree_bonus) * 10.0) / 10.0;

    // S-Grade Masterwork OSS Pitch Score Bonus (+25% multiplier) (Goal D)
    var _oss_bonus_pct = 0.0;
    if (variable_struct_exists(_mech, "oss_pitch_bonus_pct")) {
        _oss_bonus_pct = _mech.oss_pitch_bonus_pct;
    } else if (variable_struct_exists(_mech, "is_masterwork") && _mech.is_masterwork) {
        _oss_bonus_pct = 25.0;
    } else if (variable_struct_exists(_mech, "quality_grade") && _mech.quality_grade == "S_GRADE_MASTERWORK") {
        _oss_bonus_pct = 25.0;
    }

    if (_oss_bonus_pct > 0.0) {
        _composite_score = round(_composite_score * (1.0 + (_oss_bonus_pct / 100.0)) * 10.0) / 10.0;
    }

    var _passed = (_composite_score >= 100.0);

    var _report = "";
    if (_passed) {
        _report = "TENDER APPROVED: " + _mech.name + " outperformed incumbent " + _inc.name + " (" + string(_composite_score) + "/100). Faction board recommends immediate mass-production contract!";
        if (_pedigree_bonus > 0) {
            _report += " [Combat Telemetry: " + _pedigree_rating + " (+" + string(_pedigree_bonus) + " pts)]";
        }
        if (_oss_bonus_pct > 0.0) {
            _report += " [★ S-Grade Masterwork Pitch: +" + string(floor(_oss_bonus_pct)) + "% OSS Score ★]";
        }
    } else {
        var _deficit = 100.0 - _composite_score;
        _report = "TENDER REJECTED: Candidate fell short of doctrine standard by " + string(_deficit) + " pts. Improve components, boost faction standing, or deploy in PMC combat for field telemetry!";
    }

    return {
        faction_id: _faction_id,
        incumbent_id: _inc.id,
        incumbent_name: _inc.name,
        candidate_name: _mech.name,
        candidate_armor: _cand_armor,
        candidate_power: _cand_power,
        candidate_speed: _cand_speed,
        candidate_combat: _cand_combat,
        incumbent_armor: _inc.armor,
        incumbent_power: _inc.power,
        incumbent_speed: _inc.speed,
        incumbent_combat: _inc.combat_rating,
        score_armor: round(_score_armor),
        score_power: round(_score_power),
        score_speed: round(_score_speed),
        score_combat: round(_score_combat),
        standing_bonus: round(_st_bonus),
        pedigree_bonus: _pedigree_bonus,
        pedigree_rating: _pedigree_rating,
        composite_score: _composite_score,
        passed: _passed,
        report: _report
    };
};

award_procurement_contract = function(_faction_id, _mech, _trial_result) {
    if (!variable_struct_exists(mass_production_contracts, _faction_id)) return false;
    var _mp = variable_struct_get(mass_production_contracts, _faction_id);
    var _f = variable_struct_get(factions, _faction_id);
    var _is_upgrade = _mp.replaced;

    _mp.replaced = true;
    _mp.replacement_name = _mech.name;
    _mp.replacement_blueprint_id = variable_struct_get(_mech, "blueprint_id") ?? "bp_custom";
    _mp.combat_bonus = max(_is_upgrade ? _mp.combat_bonus + 4 : 18, floor(_trial_result.composite_score / 5));
    _mp.adoption_stage = "TOOLING";
    _mp.tooling_turns_remaining = 2;
    _mp.active_frontline_units = 0;
    _mp.block_level = _is_upgrade ? min(3, _mp.block_level + 1) : 1;

    // Dynamic Lore & Global Stats Tracking in obj_BlueprintManager (docs/35)
    if (instance_exists(obj_BlueprintManager)) {
        var _base_suit_id = _mp.baseline_suit_id;
        obj_BlueprintManager.record_suit_replacement(_base_suit_id, _mech.name, true, _faction_id);
        var _new_bid = variable_struct_get(_mech, "blueprint_id") ?? (variable_struct_get(_mech, "id") ?? "bp_custom");
        obj_BlueprintManager.record_suit_adoption(_new_bid, _faction_id, _mech.name, true, 1500);
    }

    // Register Blueprint Weakness in obj_GameManager (Arms Dealer Paradox - docs/25)
    if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "register_exported_blueprint_weakness")) {
        obj_GameManager.register_exported_blueprint_weakness(_mp.replacement_blueprint_id, _mech.name);
    }

    // Award Licensing Bounty (Full on first win, 60% upgrade incentive on subsequent wins)
    var _bounty = _is_upgrade ? floor(_mp.licensing_bounty * 0.6) : _mp.licensing_bounty;
    if (_is_upgrade) {
        _mp.royalty_per_turn = round(_mp.royalty_per_turn * 1.15); // +15% royalty boost for next-gen spec!
    }

    if (instance_exists(obj_GameManager)) {
        obj_GameManager.funds += _bounty;
        var _log_msg = _is_upgrade ? 
            ("! DOCTRINE UPGRADED: " + _f.name + " upgraded mass-production line to " + _mech.name + "! Upgrade Bounty: +" + string(_bounty) + " Cr (Royalties increased to +" + string(_mp.royalty_per_turn) + " Cr/turn)!") :
            ("! DOCTRINE REPLACED: " + _f.name + " awarded Mass-Production Tender for " + _mech.name + "! Licensing Bounty: +" + string(_bounty) + " Cr (+" + string(_mp.royalty_per_turn) + " Cr/turn royalties)!");
        array_push(obj_GameManager.last_turn_events, _log_msg);
    }

    // Boost Faction Military Rating & Standing
    _f.military_strength_score = min(100, _f.military_strength_score + (_is_upgrade ? 10 : 20));
    modify_standing(_faction_id, _is_upgrade ? 15 : 25);

    // Multi-Faction Arms Dealing Geopolitical Ripple Effect (docs/15)
    if (_faction_id == "faction_a") {
        modify_standing("faction_b", -25);
        modify_standing("faction_c", -10);
    } else if (_faction_id == "faction_b") {
        modify_standing("faction_a", -30);
        modify_standing("faction_c", -5);
    } else if (_faction_id == "faction_c") {
        modify_standing("faction_a", -15);
        modify_standing("faction_d", -10);
    } else if (_faction_id == "faction_d") {
        modify_standing("faction_a", -10);
        modify_standing("faction_b", -15);
    }

    if (instance_exists(obj_HQTerminal)) {
        var _toast_text = _is_upgrade ?
            ("DOCTRINE UPGRADED! " + _f.name + " ADOPTS NEXT-GEN " + _mech.name + "! +" + string(_bounty) + " Cr!") :
            ("TENDER WON! " + _f.name + " OFFICIALLY ADOPTS " + _mech.name + "! +" + string(_bounty) + " Cr!");
        obj_HQTerminal.show_toast(_toast_text, c_lime);
    }
    return true;
};


// 10b. 4-Phase Fly-Off Tournament Engine & Modernization Lifecycle (docs/26)
run_procurement_trial_phase = function(_faction_id, _mech, _phase_idx = 4, _refinements = []) {
    var _inc = get_incumbent_specs(_faction_id);
    if (is_undefined(_mech)) return undefined;

    var _cand_armor = variable_struct_get(_mech, "armor_rating") ?? 600;
    var _cand_power = variable_struct_get(_mech, "power_output") ?? 10;
    var _cand_speed = variable_struct_get(_mech, "speed") ?? 60;
    var _cand_combat = variable_struct_get(_mech, "combat_rating") ?? 400;

    // Apply Emergency Field Refinements
    var _ref_power_mod = 1.0;
    var _ref_armor_mod = 1.0;
    var _ref_speed_mod = 1.0;
    var _ref_combat_mod = 1.0;
    for (var rf = 0; rf < array_length(_refinements); rf++) {
        var _r = _refinements[rf];
        if (_r == "OVERCLOCK_REACTOR") { _ref_power_mod += 0.15; }
        else if (_r == "WELD_ARMOR") { _ref_armor_mod += 0.12; _ref_speed_mod -= 0.05; }
        else if (_r == "TUNE_VERNIERS") { _ref_speed_mod += 0.15; _ref_armor_mod -= 0.05; }
        else if (_r == "RECALIBRATE_SENSORS") { _ref_combat_mod += 0.10; }
    }
    _cand_armor = round(_cand_armor * _ref_armor_mod);
    _cand_power = round(_cand_power * _ref_power_mod);
    _cand_speed = round(_cand_speed * _ref_speed_mod);
    _cand_combat = round(_cand_combat * _ref_combat_mod);

    // 4 Diagnostic Phase Scores (Base 100 is exact parity with incumbent)
    var _score_armor = clamp((_cand_armor / max(1, _inc.armor)) * 100.0, 20.0, 160.0);
    var _score_power = clamp((_cand_power / max(1, _inc.power)) * 100.0, 20.0, 160.0);
    var _score_speed = clamp((_cand_speed / max(1, _inc.speed)) * 100.0, 20.0, 160.0);
    var _score_combat = clamp((_cand_combat / max(1, _inc.combat_rating)) * 100.0, 20.0, 160.0);

    var _w = _inc.weights;
    var _base_weighted = (_score_armor * _w[0]) + (_score_power * _w[1]) + (_score_speed * _w[2]) + (_score_combat * _w[3]);
    var _st_bonus = get_standing(_faction_id) / 5.0;

    // Combat-Proven Pedigree Telemetry Bonus (0 to 25 pts) from active PMC squad deployments (docs/25)
    var _pedigree_bonus = 0.0;
    var _pedigree_rating = "UNTESTED";
    if (variable_struct_exists(_mech, "combat_pedigree") && is_struct(_mech.combat_pedigree)) {
        _pedigree_bonus = variable_struct_get(_mech.combat_pedigree, "telemetry_bonus") ?? 0.0;
        _pedigree_rating = variable_struct_get(_mech.combat_pedigree, "pedigree_rating") ?? "UNTESTED";
    }

    var _composite_score = round((_base_weighted + _st_bonus + _pedigree_bonus) * 10.0) / 10.0;

    // S-Grade Masterwork OSS Pitch Score Bonus (+25% multiplier) (Goal D)
    var _oss_bonus_pct = 0.0;
    if (variable_struct_exists(_mech, "oss_pitch_bonus_pct")) {
        _oss_bonus_pct = _mech.oss_pitch_bonus_pct;
    } else if (variable_struct_exists(_mech, "is_masterwork") && _mech.is_masterwork) {
        _oss_bonus_pct = 25.0;
    } else if (variable_struct_exists(_mech, "quality_grade") && _mech.quality_grade == "S_GRADE_MASTERWORK") {
        _oss_bonus_pct = 25.0;
    }

    if (_oss_bonus_pct > 0.0) {
        _composite_score = round(_composite_score * (1.0 + (_oss_bonus_pct / 100.0)) * 10.0) / 10.0;
    }

    var _grade = "GRADE F";
    var _passed = false;
    if (_composite_score >= 125.0) { _grade = "GRADE S"; _passed = true; }
    else if (_composite_score >= 100.0) { _grade = "GRADE A"; _passed = true; }
    else if (_composite_score >= 85.0) { _grade = "GRADE B"; _passed = false; }
    else { _grade = "GRADE F"; _passed = false; }

    // Phase 1 specific: Static Viability Audit
    var _p1_critique = (_score_power >= 100) ? 
        "Viability Confirmed: Power grid surplus easily handles military avionics." :
        "Warning: Reactor output is marginal; sustained energy weapons may face throttling.";

    // Phase 2 specific: Proving Grounds Benchmarks
    var _p2_kinetic = round(_score_armor * 0.95);
    var _p2_thermal = round(_score_power * 0.92);
    var _p2_vernier = round(_score_speed * 1.05);
    var _p2_ecm = round(_score_combat * 0.94);

    // Phase 3 specific: Operational Duel vs Rival Corporate Entry
    var _rival_corp = "Valkyrie Heavy";
    var _rival_score = 98.0;
    if (_faction_id == "faction_b") { _rival_corp = "Astraea Dynamics"; _rival_score = 104.0; }
    else if (_faction_id == "faction_c") { _rival_corp = "Rustworks Cartel"; _rival_score = 94.0; }
    else if (_faction_id == "faction_d") { _rival_corp = "Hyperion Tactical"; _rival_score = 108.0; }

    var _report = "";
    if (_passed) {
        _report = "TENDER APPROVED (" + _grade + "): " + _mech.name + " outperformed " + _inc.name + " & " + _rival_corp + " (" + string(_composite_score) + "/100). Faction board recommends immediate mass-production contract!";
        if (_pedigree_bonus > 0) {
            _report += " [Combat Telemetry: " + _pedigree_rating + " (+" + string(_pedigree_bonus) + " pts)]";
        }
        if (_oss_bonus_pct > 0.0) {
            _report += " [★ S-Grade Masterwork Pitch: +" + string(floor(_oss_bonus_pct)) + "% OSS Score ★]";
        }
    } else {
        var _deficit = 100.0 - _composite_score;
        _report = "TENDER CONDITIONAL/REJECTED (" + _grade + "): Candidate fell short by " + string(_deficit) + " pts. Apply emergency field tuning, boost standing, or field in PMC combat!";
    }

    return {
        phase: _phase_idx,
        faction_id: _faction_id,
        incumbent_id: _inc.id,
        incumbent_name: _inc.name,
        candidate_name: _mech.name,
        candidate_armor: _cand_armor,
        candidate_power: _cand_power,
        candidate_speed: _cand_speed,
        candidate_combat: _cand_combat,
        incumbent_armor: _inc.armor,
        incumbent_power: _inc.power,
        incumbent_speed: _inc.speed,
        incumbent_combat: _inc.combat_rating,
        score_armor: round(_score_armor),
        score_power: round(_score_power),
        score_speed: round(_score_speed),
        score_combat: round(_score_combat),
        standing_bonus: round(_st_bonus),
        pedigree_bonus: _pedigree_bonus,
        pedigree_rating: _pedigree_rating,
        composite_score: _composite_score,
        grade: _grade,
        passed: _passed,
        report: _report,
        p1_critique: _p1_critique,
        p2_benchmarks: { kinetic: _p2_kinetic, thermal: _p2_thermal, vernier: _p2_vernier, ecm: _p2_ecm },
        p3_rival_corp: _rival_corp,
        p3_rival_score: _rival_score,
        p3_duel_win: (_composite_score >= _rival_score),
        refinements_applied: _refinements
    };
};

expedite_adoption_tooling = function(_faction_id) {
    if (!variable_struct_exists(mass_production_contracts, _faction_id)) return false;
    var _mp = variable_struct_get(mass_production_contracts, _faction_id);
    if (_mp.adoption_stage != "TOOLING") return false;

    var _cost = 40000;
    if (instance_exists(obj_GameManager)) {
        if (obj_GameManager.funds < _cost) {
            if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT FUNDS: 40,000 Cr required to expedite shipyard tooling!", c_red);
            return false;
        }
        obj_GameManager.funds -= _cost;
    }

    _mp.tooling_turns_remaining = max(0, _mp.tooling_turns_remaining - 1);
    if (_mp.tooling_turns_remaining <= 0) {
        _mp.adoption_stage = "ROLLOUT";
        _mp.active_frontline_units = 50;
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("TOOLING COMPLETE! " + _mp.faction_name + " begins frontline rollout with 50 units!", c_lime);
    } else {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("TOOLING EXPEDITED: " + string(_mp.tooling_turns_remaining) + " turn(s) remaining for " + _mp.faction_name + "!", c_aqua);
    }
    return true;
};

upgrade_adoption_block_ii = function(_faction_id) {
    if (!variable_struct_exists(mass_production_contracts, _faction_id)) return false;
    var _mp = variable_struct_get(mass_production_contracts, _faction_id);
    if (!_mp.replaced || _mp.block_level >= 2) return false;

    _mp.block_level = 2;
    _mp.royalty_per_turn = round(_mp.royalty_per_turn * 1.25);
    _mp.combat_bonus += 4;
    var _bounty = 450000;

    if (instance_exists(obj_GameManager)) {
        obj_GameManager.funds += _bounty;
        array_push(obj_GameManager.last_turn_events, "! BLOCK II MODERNIZATION: " + _mp.faction_name + " accepted Block II spec for " + _mp.replacement_name + "! Modernization Bounty: +" + string(_bounty) + " Cr!");
    }
    var _f = variable_struct_get(factions, _faction_id);
    _f.military_strength_score = min(100, _f.military_strength_score + 10);

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("BLOCK II MODERNIZED! +" + string(_bounty) + " Cr Bounty & +25% Royalties!", c_lime);
    }
    return true;
};

upgrade_adoption_block_iii = function(_faction_id) {
    if (!variable_struct_exists(mass_production_contracts, _faction_id)) return false;
    var _mp = variable_struct_get(mass_production_contracts, _faction_id);
    if (!_mp.replaced || _mp.block_level != 2) return false;

    _mp.block_level = 3;
    _mp.royalty_per_turn = round(_mp.royalty_per_turn * 1.20);
    _mp.combat_bonus = min(30, _mp.combat_bonus + 6);
    var _bounty = 750000;

    if (instance_exists(obj_GameManager)) {
        obj_GameManager.funds += _bounty;
        var _new_ace_unit = {
            id: "ace_custom_" + string(_mp.replacement_blueprint_id) + "_" + string(irandom(9999)),
            blueprint_id: _mp.replacement_blueprint_id,
            callsign: _mp.replacement_name + " [BLOCK III ACE]",
            name: _mp.replacement_name + " (Block III Ace)",
            class: "Ace Commander",
            weight_class: "HEAVY ASSAULT",
            assigned_pilot: "Unassigned",
            status: "READY",
            current_condition_pct: 1.0,
            armor_rating: 980,
            power_output: 22,
            speed: 85,
            combat_rating: 680,
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
        array_push(obj_GameManager.inventory.deployable_mechs, _new_ace_unit);
        array_push(obj_GameManager.last_turn_events, "! BLOCK III APEX SPEC: " + _mp.faction_name + " ratified Block III Vanguard! Prestige Bounty: +" + string(_bounty) + " Cr & Free Ace Custom added to Hangar!");
    }
    var _f = variable_struct_get(factions, _faction_id);
    _f.military_strength_score = min(100, _f.military_strength_score + 15);

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("BLOCK III APEX RATIFIED! +" + string(_bounty) + " Cr & Ace Unit Commissioned!", c_lime);
    }
    return true;
};

// 11. Interstellar Commodity Trade System (docs/15)
get_faction_trade_inventory = function(_faction_id) {
    var _st = get_standing(_faction_id);
    var _buy_mult = 1.0;
    var _sell_mult = 1.0;

    if (_st >= 30) {
        _buy_mult = 0.85;  // 15% discount
        _sell_mult = 1.15; // 15% bonus selling
    } else if (_st < 0) {
        _buy_mult = 1.25;  // 25% tariff surcharge
        _sell_mult = 0.85; // 15% penalty selling
    }

    // Dynamic Demand Multipliers by Faction Doctrine
    var _items = [
        // Category 0: Raw Minerals
        {
            cat: "minerals",
            id: "mat_tungsten",
            name: "Refined Tungsten (W)",
            desc: "Heavy ballistic refractory metal.",
            base_price: 400,
            demand_mult: (_faction_id == "faction_a" ? 1.4 : (_faction_id == "faction_b" ? 0.9 : 1.0)),
            stock_faction: 50
        },
        {
            cat: "minerals",
            id: "mat_silica_carb",
            name: "Silica-Carbon (SiC)",
            desc: "Thermal insulator and ceramic base.",
            base_price: 150,
            demand_mult: (_faction_id == "faction_b" ? 1.3 : (_faction_id == "faction_a" ? 1.0 : 1.1)),
            stock_faction: 80
        },
        {
            cat: "minerals",
            id: "mat_syn_flux",
            name: "Synthetic Flux (Flux)",
            desc: "Catalytic fusing agent for alloy smelting.",
            base_price: 800,
            demand_mult: (_faction_id == "faction_c" ? 1.4 : (_faction_id == "faction_d" ? 1.2 : 0.9)),
            stock_faction: 30
        },
        {
            cat: "minerals",
            id: "mat_tritium",
            name: "Plasma-Charged Tritium (T)",
            desc: "High-energy fusion reactor fuel.",
            base_price: 1200,
            demand_mult: (_faction_id == "faction_b" ? 1.5 : (_faction_id == "faction_d" ? 1.3 : 1.0)),
            stock_faction: 20
        },

        // Category 1: Synthesized Alloys
        {
            cat: "alloys",
            id: "alloy_vanguard_comp",
            name: "Vanguard Composite Plating",
            desc: "Tier-1 heavy kinetic armor alloy.",
            base_price: 5500,
            demand_mult: (_faction_id == "faction_a" ? 1.5 : 1.0),
            stock_faction: 15
        },
        {
            cat: "alloys",
            id: "alloy_hyperion_matrix",
            name: "Hyperion Superconductor Matrix",
            desc: "High-spec Tokamak magnetic liner.",
            base_price: 8500,
            demand_mult: (_faction_id == "faction_b" ? 1.5 : (_faction_id == "faction_d" ? 1.4 : 1.0)),
            stock_faction: 10
        },
        {
            cat: "alloys",
            id: "alloy_aerosteel_flux",
            name: "Aerosteel Vernier Alloy",
            desc: "Ultra-lightweight high-thrust frame alloy.",
            base_price: 7000,
            demand_mult: (_faction_id == "faction_d" ? 1.4 : (_faction_id == "faction_b" ? 1.3 : 1.0)),
            stock_faction: 12
        },
        {
            cat: "alloys",
            id: "alloy_adamantine_carbide",
            name: "Adamantine Heavy Carbide",
            desc: "Extreme density siege armor alloy.",
            base_price: 11000,
            demand_mult: (_faction_id == "faction_c" ? 1.5 : (_faction_id == "faction_a" ? 1.3 : 1.0)),
            stock_faction: 8
        },

        // Category 2: Modular Components
        {
            cat: "parts",
            slot: "weapons",
            id: "wp_vulcan_01",
            name: "WP-01 Rotary Vulcan (120mm)",
            desc: "Rapid-fire solid kinetic autocannon.",
            base_price: 45000,
            demand_mult: (_faction_id == "faction_a" ? 1.3 : (_faction_id == "faction_c" ? 1.4 : 1.0)),
            part_data: { id: "wp_vulcan_01", name: "WP-01 Rotary Vulcan (120mm)", slot: "weapons", armor: 100, mass: 12, power_draw: 3, damage: 180, bonus: "Sustained Fire" },
            stock_faction: 4
        },
        {
            cat: "parts",
            slot: "weapons",
            id: "wp_beam_02",
            name: "WP-02 Particle Pulse Rifle",
            desc: "High-AP coherent particle beam rifle.",
            base_price: 60000,
            demand_mult: (_faction_id == "faction_b" ? 1.4 : (_faction_id == "faction_d" ? 1.3 : 0.9)),
            part_data: { id: "wp_beam_02", name: "WP-02 Particle Pulse Rifle", slot: "weapons", armor: 80, mass: 8, power_draw: 10, damage: 240, bonus: "Armor Piercing" },
            stock_faction: 3
        },
        {
            cat: "parts",
            slot: "heads",
            id: "hd_aether_02",
            name: "HD-02 Aether EW-Dome",
            desc: "Electronic warfare targeting head.",
            base_price: 25000,
            demand_mult: (_faction_id == "faction_b" ? 1.4 : 1.0),
            part_data: { id: "hd_aether_02", name: "HD-02 Aether EW-Dome", slot: "heads", armor: 90, mass: 2, power_draw: 4, bonus: "+18% Evasion" },
            stock_faction: 5
        },
        {
            cat: "parts",
            slot: "torsos",
            id: "tr_hyperion_02",
            name: "TR-02 Hyperion Tokamak Torso",
            desc: "42 MW high-power fusion torso chassis.",
            base_price: 95000,
            demand_mult: (_faction_id == "faction_d" ? 1.4 : (_faction_id == "faction_b" ? 1.3 : 1.0)),
            part_data: { id: "tr_hyperion_02", name: "TR-02 Hyperion Tokamak Torso", slot: "torsos", armor: 360, mass: 20, power_output: 42, bonus: "High-Spec Fusion Core" },
            stock_faction: 2
        }
    ];

    for (var i = 0; i < array_length(_items); i++) {
        var _it = _items[i];
        _it.buy_price = round(_it.base_price * _it.demand_mult * _buy_mult);
        _it.sell_price = round(_it.base_price * _it.demand_mult * 0.70 * _sell_mult);
    }

    return _items;
};

execute_trade_buy = function(_faction_id, _item, _qty) {
    if (!instance_exists(obj_GameManager)) return false;
    var _cost = _item.buy_price * _qty;
    if (obj_GameManager.funds < _cost) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT FUNDS: Needs " + string(_cost) + " Cr!", c_red);
        return false;
    }

    obj_GameManager.funds -= _cost;

    if (_item.cat == "minerals") {
        obj_GameManager.add_raw_material(_item.id, _qty);
    } else if (_item.cat == "alloys") {
        obj_GameManager.add_alloy(_item.id, _qty);
    } else if (_item.cat == "parts") {
        for (var q = 0; q < _qty; q++) {
            obj_GameManager.add_part_to_inventory(_item.part_data);
        }
    }

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("TRADE PURCHASE: +" + string(_qty) + "x " + _item.name + " (-" + string(_cost) + " Cr)", c_lime);
    }
    return true;
};

execute_trade_sell = function(_faction_id, _item, _qty) {
    if (!instance_exists(obj_GameManager)) return false;

    // Check player stock
    var _available = 0;
    if (_item.cat == "minerals") {
        _available = obj_GameManager.get_raw_material(_item.id);
    } else if (_item.cat == "alloys") {
        _available = obj_GameManager.get_alloy(_item.id);
    } else if (_item.cat == "parts") {
        var _slot_arr = variable_struct_get(obj_GameManager.inventory.parts, _item.slot) ?? [];
        for (var p = 0; p < array_length(_slot_arr); p++) {
            if (_slot_arr[p].id == _item.id) _available++;
        }
    }

    if (_available < _qty) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT STOCK TO SELL!", c_red);
        return false;
    }

    // Deduct stock
    if (_item.cat == "minerals") {
        obj_GameManager.spend_raw_material(_item.id, _qty);
    } else if (_item.cat == "alloys") {
        obj_GameManager.spend_alloy(_item.id, _qty);
    } else if (_item.cat == "parts") {
        var _slot_arr2 = variable_struct_get(obj_GameManager.inventory.parts, _item.slot);
        var _removed = 0;
        for (var p2 = array_length(_slot_arr2) - 1; p2 >= 0; p2--) {
            if (_slot_arr2[p2].id == _item.id) {
                array_delete(_slot_arr2, p2, 1);
                _removed++;
                if (_removed >= _qty) break;
            }
        }
    }

    var _payout = _item.sell_price * _qty;
    obj_GameManager.funds += _payout;

    // Slight Standing Adjustment (+1 with buyer)
    modify_standing(_faction_id, 1);

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("TRADE SALE: Sold " + string(_qty) + "x " + _item.name + " (+" + string(_payout) + " Cr)", c_yellow);
    }
    return true;
};

// 12. Dynamic Frontline World Reflection Methods (docs/27)
get_faction_active_line_chassis = function(_faction_id) {
    if (!variable_struct_exists(mass_production_contracts, _faction_id)) return undefined;
    var _mp = variable_struct_get(mass_production_contracts, _faction_id);
    if (_mp.replaced) {
        return {
            name: _mp.replacement_name,
            blueprint_id: _mp.replacement_blueprint_id,
            is_player_designed: true,
            block_level: _mp.block_level,
            adoption_stage: _mp.adoption_stage,
            combat_bonus: _mp.combat_bonus,
            active_units: _mp.active_frontline_units
        };
    } else {
        var _inc = get_incumbent_specs(_faction_id);
        return {
            name: _inc.name,
            blueprint_id: _inc.id,
            is_player_designed: false,
            block_level: 1,
            adoption_stage: "INCUMBENT_LINE",
            combat_bonus: 0,
            active_units: 150
        };
    }
};

get_faction_patrol_squad = function(_faction_id) {
    var _chassis = get_faction_active_line_chassis(_faction_id);
    if (is_undefined(_chassis)) return [];
    var _spr = spr_ms_ironclad_idle;
    if (variable_struct_exists(mass_production_contracts, _faction_id)) {
        _spr = variable_struct_get(variable_struct_get(mass_production_contracts, _faction_id), "sprite_asset") ?? _spr;
    }
    var _squad = [];
    for (var u = 0; u < 4; u++) {
        array_push(_squad, {
            unit_id: "patrol_" + _faction_id + "_" + string(u + 1),
            callsign: _chassis.name + " Unit-" + string(u + 1),
            chassis_name: _chassis.name,
            blueprint_id: _chassis.blueprint_id,
            sprite_asset: _spr,
            is_player_designed: _chassis.is_player_designed,
            armor: (_chassis.is_player_designed ? 2200 : 1800) + (_chassis.block_level * 150),
            combat_rating: 450 + (_chassis.combat_bonus * 5)
        });
    }
    return _squad;
};


// 13. Diplomatic Battlefield Intervention Matrix (docs/28)
evaluate_battlefield_faction_intervention = function(_sector_sphere) {
    var _interventions = [];
    var _f_keys = ["faction_a", "faction_b", "faction_c", "faction_d"];
    for (var f = 0; f < array_length(_f_keys); f++) {
        var _fid = _f_keys[f];
        var _std = get_standing(_fid);
        var _f_info = variable_struct_get(factions, _fid);
        var _fname = _f_info.name;

        // ALLIED INTERVENTION (Standing >= +25)
        if (_std >= 25) {
            if (_fid == "faction_a") {
                array_push(_interventions, {
                    faction_id: _fid, faction_name: _fname, type: "ALLIED_ASSIST",
                    action_id: "orbital_mac_strike", title: "Terran Orbital MAC Strike",
                    desc: "Terran cruisers in orbit fire a 380mm kinetic slug at the enemy lead combatant!",
                    dmg_to_boss: irandom_range(350, 450), hit_penalty: 0, ap_mod: 0, heat_spike: 0, armor_repair: 0
                });
            } else if (_fid == "faction_b") {
                array_push(_interventions, {
                    faction_id: _fid, faction_name: _fname, type: "ALLIED_ASSIST",
                    action_id: "ecm_sensor_blind", title: "Colony ECM Blinding Chaff",
                    desc: "Colony drones saturate the battlespace with radar chaff, stripping -20% accuracy and -1 AP from hostiles!",
                    dmg_to_boss: 0, hit_penalty: 20, ap_mod: -1, heat_spike: 0, armor_repair: 0
                });
            } else if (_fid == "faction_c") {
                array_push(_interventions, {
                    faction_id: _fid, faction_name: _fname, type: "ALLIED_ASSIST",
                    action_id: "field_repair_drop", title: "Syndicate Field Rig Repair",
                    desc: "Syndicate salvage riggers drop emergency nanite canisters, restoring +250 armor across Allied units!",
                    dmg_to_boss: 0, hit_penalty: 0, ap_mod: 0, heat_spike: 0, armor_repair: 250
                });
            } else if (_fid == "faction_d") {
                array_push(_interventions, {
                    faction_id: _fid, faction_name: _fname, type: "ALLIED_ASSIST",
                    action_id: "cyber_neural_overload", title: "Zaibatsu Cyber-Neural Overload",
                    desc: "Zaibatsu electronic warfare infiltrates the enemy reactor, spiking heat by +40 and disabling special weapons!",
                    dmg_to_boss: 0, hit_penalty: 0, ap_mod: 0, heat_spike: 40, armor_repair: 0
                });
            }
        }
        // HOSTILE HINDRANCE (Standing <= -20)
        else if (_std <= -20) {
            if (_fid == "faction_a") {
                array_push(_interventions, {
                    faction_id: _fid, faction_name: _fname, type: "HOSTILE_HINDRANCE",
                    action_id: "airspace_lockout", title: "Terran Airspace Lockout",
                    desc: "Terran orbital defense declares an interdiction corridor; Allied units suffer -2 AP on turn 1!",
                    allied_ap_penalty: 2, allied_heat_penalty: 0, spawn_flankers: false, allied_acc_penalty: 0
                });
            } else if (_fid == "faction_b") {
                array_push(_interventions, {
                    faction_id: _fid, faction_name: _fname, type: "HOSTILE_HINDRANCE",
                    action_id: "thermal_flare_storm", title: "Colony Thermal Flare Storm",
                    desc: "Colony satellites reflect concentrated solar radiation, reducing Allied heat dissipation by -15!",
                    allied_ap_penalty: 0, allied_heat_penalty: 15, spawn_flankers: false, allied_acc_penalty: 0
                });
            } else if (_fid == "faction_c") {
                array_push(_interventions, {
                    faction_id: _fid, faction_name: _fname, type: "HOSTILE_HINDRANCE",
                    action_id: "mercenary_flankers", title: "Syndicate Pirate Flankers",
                    desc: "Hostile syndicate raiders deploy auxiliary skirmishers to pinch Allied supply lines!",
                    allied_ap_penalty: 0, allied_heat_penalty: 0, spawn_flankers: true, allied_acc_penalty: 0
                });
            } else if (_fid == "faction_d") {
                array_push(_interventions, {
                    faction_id: _fid, faction_name: _fname, type: "HOSTILE_HINDRANCE",
                    action_id: "targeting_scrambler_worm", title: "Zaibatsu Scrambler Worm",
                    desc: "Zaibatsu cyber-command infiltrates Allied optics, inflicting -15% accuracy!",
                    allied_ap_penalty: 0, allied_heat_penalty: 0, spawn_flankers: false, allied_acc_penalty: 15
                });
            }
        }
    }
    return _interventions;
};

// =============================================================================
// THE PROMETHEUS PROTOCOL: DIPLOMATIC REVOLUTION (doc 38)
// =============================================================================
on_mobile_suit_revolution = function() {
    show_debug_message("[obj_FactionManager] The Prometheus Revolution triggered! Factions pivoting from hostility to desperate cooperation...");

    // 1. Diplomatic Truce & Standing Surge (+35 to all active factions)
    var _f_keys = ["faction_a", "faction_b", "faction_c", "faction_d", "faction_e"];
    for (var f = 0; f < array_length(_f_keys); f++) {
        var _fid = _f_keys[f];
        variable_struct_set(faction_standing, _fid, clamp(variable_struct_get(faction_standing, _fid) + 35, 15, 80));
        if (variable_struct_exists(factions, _fid)) {
            var _fc = variable_struct_get(factions, _fid);
            _fc.standing = variable_struct_get(faction_standing, _fid);
            _fc.standing_title = "Arms Monopoly Partner";
            _fc.contract_bounty_multiplier = 3.0; // 300% bounty surge for player's mobile suit!
            _fc.ai_state = "MS_REVERSE_ENGINEERING";
            _fc.ai_behavior_title = "Desperate Reverse-Engineering & High-Bounty Procurement";
        }
    }

        // 2. Inject Urgent Prometheus High-Bounty Tenders
    array_push(available_contracts, {
        id: "cnt_prometheus_linebreaker_01",
        faction: "faction_a",
        faction_name: "The Terran Coalition",
        type: "PROMETHEUS_TENDER",
        title: "★ THE PROMETHEUS TENDER: BREAK THE TRENCH LINE ★",
        briefing: "Terran High Command offers an astronomical 3.0x bounty to deploy your bipedal Mobile Suit into Sector 4 to crush entrenched heavy tank battalions!",
        required_tier: 2,
        required_quantity: 1,
        delivered_quantity: 0,
        payout_credits: 750000,
        reward_material_id: "mat_tungsten",
        reward_material_amount: 50,
        reputation_gain: 30,
        reputation_penalty: -10,
        deadline_days: 35,
        days_remaining: 35,
        penalty_credits: 0
    });
    array_push(available_contracts, {
        id: "cnt_prometheus_colony_01",
        faction: "faction_b",
        faction_name: "The Outer Colonies",
        type: "PROMETHEUS_TENDER",
        title: "★ LIBERATION PACT: ORBITAL BEACHHEAD MOBILE SUIT DEFENSE ★",
        briefing: "Colonial Alliance requests Mobile Suit tactical superiority to shatter an incoming tank invasion force. Offers emergency Tritium reserves.",
        required_tier: 2,
        required_quantity: 1,
        delivered_quantity: 0,
        payout_credits: 680000,
        reward_material_id: "mat_tritium",
        reward_material_amount: 25,
        reputation_gain: 35,
        reputation_penalty: -15,
        deadline_days: 28,
        days_remaining: 28,
        penalty_credits: 0
    });

    if (variable_struct_exists(territory_control, "last_shift_report")) {
        territory_control.last_shift_report = "GLOBAL CEASEFIRE: Superpowers suspend operations to negotiate Mobile Suit contracts with the Iron Vanguard!";
    }
};
