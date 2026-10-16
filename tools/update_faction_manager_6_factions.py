import re

with open('objects/obj_FactionManager/Create_0.gml', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update faction_standing
old_standing = """faction_standing = {
    faction_a: 45,      // Starting status with Terran Coalition
    faction_b: -20,     // Starting status with Outer Colonies
    faction_c: 10,      // Starting status with Rogue Syndicates
    faction_d: 0        // Starting status with Apex Zaibatsu
};"""

new_standing = """faction_standing = {
    faction_a: 45,      // Starting status with Terran Coalition
    faction_b: -20,     // Starting status with Outer Colonies
    faction_c: 10,      // Starting status with Rogue Syndicates
    faction_d: 0,       // Starting status with Apex Zaibatsu
    faction_e: -10,     // Starting status with Sidereal Sovereign League
    faction_f: 0        // Starting status with Tharsis Machine Consensus (Dormant)
};"""

assert old_standing in text, "Could not find old_standing"
text = text.replace(old_standing, new_standing, 1)

# 2. Add faction_e and faction_f to factions struct
old_faction_d = """        winning_agenda: "Forecloses on sovereign planetary debt; replaces human garrisons with autonomous combat drones.",
        desperate_protocol: "Unseals rogue HATS-X01 Amaterasu Zero; deploys pain-inhibited cybernetic suicide aces; offers 2.0x bounties."
    }
};"""

new_faction_d_e_f = """        winning_agenda: "Forecloses on sovereign planetary debt; replaces human garrisons with autonomous combat drones.",
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
};"""

assert old_faction_d in text, "Could not find old_faction_d"
text = text.replace(old_faction_d, new_faction_d_e_f, 1)

# 3. Update territory_control
old_tc = """territory_control = {
    terran_pct: 38,
    colony_pct: 32,
    syndicate_pct: 16,
    zaibatsu_pct: 14,
    pmc_pct: 0,
    contested_sector: "SECTOR 4-B // FRONTLINE TRENCHES",
    last_shift_report: "Terran Coalition 1st Armored Division holds forward orbital perimeter."
};"""

new_tc = """territory_control = {
    terran_pct: 35,
    colony_pct: 28,
    syndicate_pct: 14,
    zaibatsu_pct: 11,
    astran_pct: 12,
    martian_pct: 0,
    pmc_pct: 0,
    contested_sector: "SECTOR 4-B // FRONTLINE TRENCHES",
    last_shift_report: "Terran Coalition 1st Armored Division holds forward orbital perimeter."
};"""

assert old_tc in text, "Could not find old_tc"
text = text.replace(old_tc, new_tc, 1)

# 4. Update mass_production_contracts with faction_e and faction_f
old_mpc = """        req_armor: 135,
        req_power: 14,
        adoption_stage: "UNADOPTED",
        tooling_turns_remaining: 2,
        active_frontline_units: 0,
        block_level: 1
    }
};"""

new_mpc = """        req_armor: 135,
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
};"""

assert old_mpc in text, "Could not find old_mpc"
text = text.replace(old_mpc, new_mpc, 1)

# 5. Add candidate pools for faction_e and faction_f
old_candidates_end = """        { id: "ms_zaibatsu_tessen_09", name: "ZBT-T09 Tessen", doctrine: "EMP Neural Jammer & Deflector", weapon: "Broadband EMP Disruptor", armor: 1820, power: 15, speed: 78, combat: 470, sprite: spr_ms_tessen_idle, req_armor: 125, req_power: 14, bounty: 2250000, royalty: 54000 }
    ]
};"""

new_candidates_end = """        { id: "ms_zaibatsu_tessen_09", name: "ZBT-T09 Tessen", doctrine: "EMP Neural Jammer & Deflector", weapon: "Broadband EMP Disruptor", armor: 1820, power: 15, speed: 78, combat: 470, sprite: spr_ms_tessen_idle, req_armor: 125, req_power: 14, bounty: 2250000, royalty: 54000 }
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
};"""

assert old_candidates_end in text, "Could not find old_candidates_end"
text = text.replace(old_candidates_end, new_candidates_end, 1)

# 6. Update roll_playthrough_mass_production_selection
old_roll_keys = 'var _f_keys = ["faction_a", "faction_b", "faction_c", "faction_d"];'
new_roll_keys = 'var _f_keys = ["faction_a", "faction_b", "faction_c", "faction_d", "faction_e", "faction_f"];'
assert old_roll_keys in text, "Could not find old_roll_keys"
text = text.replace(old_roll_keys, new_roll_keys, 1)

# 7. Add bilateral relations for faction_e and faction_f
old_diplo_end = """        historical_grievance: "Cartel raids on offshore research installations",
        total_wars_fought: 3,
        war_duration_turns: 0,
        last_event_turn: 1
    }
};"""

new_diplo_end = """        historical_grievance: "Cartel raids on offshore research installations",
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
};"""

assert old_diplo_end in text, "Could not find old_diplo_end"
text = text.replace(old_diplo_end, new_diplo_end, 1)

# 8. Update evaluate_faction_ai_turn to evaluate 6 factions and support Martian awakening
old_ai_eval = """    // 3. Balance-of-Power Anti-Blobbing (Rubber-Banding, docs/21)
    // Check if any single faction controls > 40% of Sol territory
    var _tc = territory_control;
    var _pcts = [
        { id: "faction_a", name: "The Terran Coalition", pct: _tc.terran_pct },
        { id: "faction_b", name: "The Outer Colonies", pct: _tc.colony_pct },
        { id: "faction_c", name: "Rogue Mercenary Syndicates", pct: _tc.syndicate_pct },
        { id: "faction_d", name: "Apex Bio-Cybernetics Zaibatsu", pct: _tc.zaibatsu_pct }
    ];"""

new_ai_eval = """    // 3. Balance-of-Power Anti-Blobbing (Rubber-Banding, docs/21)
    // Check if any single faction controls > 40% of Sol territory
    var _tc = territory_control;
    var _pcts = [
        { id: "faction_a", name: "The Terran Coalition", pct: _tc[$ "terran_pct"] ?? 35 },
        { id: "faction_b", name: "The Outer Colonies", pct: _tc[$ "colony_pct"] ?? 28 },
        { id: "faction_c", name: "Rogue Mercenary Syndicates", pct: _tc[$ "syndicate_pct"] ?? 14 },
        { id: "faction_d", name: "Apex Bio-Cybernetics Zaibatsu", pct: _tc[$ "zaibatsu_pct"] ?? 11 },
        { id: "faction_e", name: "The Sidereal Sovereign League", pct: _tc[$ "astran_pct"] ?? 12 },
        { id: "faction_f", name: "The Tharsis Machine Consensus", pct: _tc[$ "martian_pct"] ?? 0 }
    ];"""

assert old_ai_eval in text, "Could not find old_ai_eval"
text = text.replace(old_ai_eval, new_ai_eval, 1)

# 9. Update the loop in Section 4 of evaluate_faction_ai_turn
old_eval_loop = """    // 4. Individual Faction AI Brains & Dynamic Behavioral State Evaluation (docs/36)
    var _f_ids = ["faction_a", "faction_b", "faction_c", "faction_d"];
    for (var fi = 0; fi < array_length(_f_ids); fi++) {
        var _fid = _f_ids[fi];
        var _f = factions[$ _fid];
        var _fpct = 25;
        if (_fid == "faction_a") _fpct = _tc.terran_pct;
        else if (_fid == "faction_b") _fpct = _tc.colony_pct;
        else if (_fid == "faction_c") _fpct = _tc.syndicate_pct;
        else if (_fid == "faction_d") _fpct = _tc.zaibatsu_pct;"""

new_eval_loop = """    // 4. Individual Faction AI Brains & Dynamic Behavioral State Evaluation (docs/36, docs/37)
    var _f_ids = ["faction_a", "faction_b", "faction_c", "faction_d", "faction_e", "faction_f"];
    for (var fi = 0; fi < array_length(_f_ids); fi++) {
        var _fid = _f_ids[fi];
        var _f = factions[$ _fid];
        var _fpct = 20;
        if (_fid == "faction_a") _fpct = _tc[$ "terran_pct"] ?? 35;
        else if (_fid == "faction_b") _fpct = _tc[$ "colony_pct"] ?? 28;
        else if (_fid == "faction_c") _fpct = _tc[$ "syndicate_pct"] ?? 14;
        else if (_fid == "faction_d") _fpct = _tc[$ "zaibatsu_pct"] ?? 11;
        else if (_fid == "faction_e") _fpct = _tc[$ "astran_pct"] ?? 12;
        else if (_fid == "faction_f") _fpct = _tc[$ "martian_pct"] ?? 0;

        // Special handling: Tharsis Machine Consensus Awakening
        if (_fid == "faction_f" && (_f[$ "is_dormant"] ?? false)) {
            var _cur_turn = (instance_exists(obj_GameManager)) ? obj_GameManager.current_turn : 1;
            if (_cur_turn >= 15) {
                _f.is_dormant = false;
                add_diplomatic_cable("THARSIS SUB-CRYPT", "Sister Ark 07 (Player)", "ARES PRIMUS AWAKENS: Sister Vessel Hephaestus Identified", "Subterranean blast doors detonate across Mars. The Logic God unseals cryo-foundries and hails Sister Vessel 07!", "URGENT", "WAR");
            }
        }"""

assert old_eval_loop in text, "Could not find old_eval_loop"
text = text.replace(old_eval_loop, new_eval_loop, 1)

# Write updated content
with open('objects/obj_FactionManager/Create_0.gml', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated objects/obj_FactionManager/Create_0.gml!")
