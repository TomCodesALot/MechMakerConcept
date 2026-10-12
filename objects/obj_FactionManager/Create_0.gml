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
faction_standing = {
    faction_a: 45,      // Starting status with Terran Coalition
    faction_b: -20,     // Starting status with Outer Colonies
    faction_c: 10,      // Starting status with Rogue Syndicates
    faction_d: 0        // Starting status with Apex Zaibatsu
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
        standing_title: "Valued Contractor"
    },
    faction_b: {
        id: "faction_b",
        name: "The Outer Colonies",
        short_name: "COLONIES",
        alignment: "Orbital Independence Alliance",
        military_strength_score: 50,
        standing: -20,
        standing_title: "Hostile / Sanctioned"
    },
    faction_c: {
        id: "faction_c",
        name: "Rogue Mercenary Syndicates",
        short_name: "SYNDICATE",
        alignment: "Black Market Smuggling Network",
        military_strength_score: 30,
        standing: 10,
        standing_title: "Neutral Broker"
    },
    faction_d: {
        id: "faction_d",
        name: "Apex Bio-Cybernetics Zaibatsu",
        short_name: "ZAIBATSU",
        alignment: "Transhumanist Hyper-Corp Conglomerate",
        military_strength_score: 45,
        standing: 0,
        standing_title: "Neutral Client"
    }
};

// 4. Strategic Territory Control & Contested Sectors (docs/04, docs/12)
territory_control = {
    terran_pct: 38,
    colony_pct: 32,
    syndicate_pct: 16,
    zaibatsu_pct: 14,
    pmc_pct: 0,
    contested_sector: "SECTOR 4-B // FRONTLINE TRENCHES",
    last_shift_report: "Terran Coalition 1st Armored Division holds forward orbital perimeter."
};

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
        req_power: 16
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
        req_power: 10
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
        req_power: 14
    }
};

factions_overthrown = [];
pmc_expeditions_launched = 0;

// 5. Contract Queues (docs/04)
active_contracts = [];       // Currently accepted contracts with active deadlines
available_contracts = [
    {
        id: "cnt_terran_mass_01",
        faction: "faction_a",
        faction_name: "The Terran Coalition",
        type: "MASS_PRODUCTION",
        title: "OPERATION IRON SHIELD: HEAVY ASSAULT SUIT ORDER",
        briefing: "Terran Frontline Command requires a ready-to-deploy GHA-07 Ironclad chassis delivered to planetary staging grounds in Sector 4.",
        required_tier: 2,
        required_quantity: 1,
        delivered_quantity: 0,
        payout_credits: 480000,
        reputation_gain: 15,
        reputation_penalty: -25,
        deadline_days: 30,
        days_remaining: 30,
        penalty_credits: 120000
    },
    {
        id: "cnt_colony_bounty_01",
        faction: "faction_b",
        faction_name: "The Outer Colonies",
        type: "PROTOTYPE_BOUNTY",
        title: "PROJECT AETHER: MASTERWORK TUNED FUSION CORE",
        briefing: "Colony ace interceptor pilots demand an over-tuned fusion core prototype (+15% Power Output) forged in your R&D Oscilloscope lab.",
        required_tier: 2,
        required_quantity: 1,
        delivered_quantity: 0,
        payout_credits: 260000,
        reward_material_id: "mat_tritium",
        reward_material_amount: 6,
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
        title: "BLACK MARKET RUN: UNCATALOGED VULCAN MUNITIONS",
        briefing: "Smugglers will pay top dollar in refined Synthetic Flux for uncataloged GAU-88 Vulcan weapon crates. 35% Risk of Terran Intelligence leak!",
        required_tier: 1,
        required_quantity: 1,
        delivered_quantity: 0,
        payout_credits: 190000,
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
    return faction_standing[$ _faction_id] ?? 0;
};

set_standing = function(_faction_id, _val) {
    var _clamped = clamp(_val, -100, 100);
    faction_standing[$ _faction_id] = _clamped;
    if (variable_struct_exists(factions, _faction_id)) {
        factions[$ _faction_id].standing = _clamped;
    }
    return _clamped;
};

modify_standing = function(_faction_id, _delta) {
    var _current = get_standing(_faction_id);
    return set_standing(_faction_id, _current + _delta);
};

// 7. Dynamic Macro War Map Simulation (docs/04, docs/12)
simulate_war_turn = function() {
    var _t_bonus = (mass_production_contracts.faction_a.replaced) ? mass_production_contracts.faction_a.combat_bonus : 0;
    var _c_bonus = (mass_production_contracts.faction_b.replaced) ? mass_production_contracts.faction_b.combat_bonus : 0;
    var _s_bonus = (mass_production_contracts.faction_c.replaced) ? mass_production_contracts.faction_c.combat_bonus : 0;
    var _z_bonus = (mass_production_contracts.faction_d.replaced) ? mass_production_contracts.faction_d.combat_bonus : 0;

    var _terran_pwr = factions.faction_a.military_strength_score + _t_bonus;
    var _colony_pwr = factions.faction_b.military_strength_score + _c_bonus;
    var _syndicate_pwr = factions.faction_c.military_strength_score + _s_bonus;

    var _clash = (_terran_pwr - _colony_pwr) + irandom_range(-6, 6);
    if (_clash > 4 && territory_control.colony_pct > 5) {
        var _shift = irandom_range(1, 3);
        territory_control.terran_pct = min(75, territory_control.terran_pct + _shift);
        territory_control.colony_pct = max(0, territory_control.colony_pct - _shift);
        territory_control.last_shift_report = (mass_production_contracts.faction_a.replaced) ? 
            ("Terran Coalition fielding player-licensed " + mass_production_contracts.faction_a.replacement_name + " crushes Colony line!") :
            "Terran Coalition 1st Armored Division captures orbital trench line in Sector 4!";
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("WAR INTEL: Terran Coalition advances in Sector 4 (+ " + string(_shift) + "% control)!", c_yellow);
        }
    } else if (_clash < -4 && territory_control.terran_pct > 5) {
        var _shift = irandom_range(1, 3);
        territory_control.colony_pct = min(75, territory_control.colony_pct + _shift);
        territory_control.terran_pct = max(0, territory_control.terran_pct - _shift);
        territory_control.last_shift_report = (mass_production_contracts.faction_b.replaced) ?
            ("Outer Colonies fielding player-designed " + mass_production_contracts.faction_b.replacement_name + " shatters Terran front!") :
            "Outer Colonies ace squadrons breach Terran orbital line in Sector 5!";
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("WAR INTEL: Outer Colonies capture orbital sector (+ " + string(_shift) + "% control)!", c_aqua);
        }
    } else {
        territory_control.last_shift_report = "Stalemate along the Asteroid Belt boundary. Heavy attritional skirmishing.";
    }

    // Syndicate opportunism if strength elevated
    if (_syndicate_pwr >= 35 && random(100) < 40 && territory_control.terran_pct > 5) {
        territory_control.syndicate_pct = min(28, territory_control.syndicate_pct + 1);
        territory_control.terran_pct = max(0, territory_control.terran_pct - 1);
        territory_control.last_shift_report = "Rogue Syndicates exploit chaos to establish pirate redoubts in Delta Sector!";
    }
};

// 7b. Pitch Mass-Production Replacement Doctrine (docs/12)
pitch_mass_production_replacement = function(_faction_id, _blueprint_id, _custom_name) {
    if (!variable_struct_exists(mass_production_contracts, _faction_id)) return false;
    var _mp = mass_production_contracts[$ _faction_id];
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
        factions[$ _faction_id].military_strength_score = min(100, factions[$ _faction_id].military_strength_score + 15);
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

    var _tf = factions[$ _target_faction_id];
    if (is_undefined(_tf)) return false;

    pmc_expeditions_launched += 1;

    var _pmc_pwr = _mech.armor_rating + _mech.power_output + (_pilot.combat_stat * 12) + irandom_range(15, 40);
    var _def_pwr = _tf.military_strength_score * 1.8 + irandom_range(10, 30);

    if (_pmc_pwr >= _def_pwr) {
        var _captured = irandom_range(3, 6);
        var _t_key = (_target_faction_id == "faction_a") ? "terran_pct" : ((_target_faction_id == "faction_b") ? "colony_pct" : ((_target_faction_id == "faction_c") ? "syndicate_pct" : "zaibatsu_pct"));
        var _cur_t = territory_control[$ _t_key];
        var _actual_taken = min(_cur_t, _captured);

        territory_control[$ _t_key] = max(0, _cur_t - _actual_taken);
        territory_control.pmc_pct = min(100, territory_control.pmc_pct + _actual_taken);

        _tf.military_strength_score = max(0, _tf.military_strength_score - 10);
        modify_standing(_target_faction_id, -30);

        var _salvage_cr = irandom_range(180000, 380000);
        _gm.add_funds(_salvage_cr);
        _gm.add_raw_material("mat_tungsten", irandom_range(2, 5));
        _gm.add_raw_material("mat_tritium", irandom_range(1, 3));
        _gm.total_sorties_won += 1;

        if (territory_control[$ _t_key] <= 0 || _tf.military_strength_score <= 5) {
            territory_control[$ _t_key] = 0;
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
        if (available_contracts[i][$ "id"] == _contract_id) {
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
                obj_GameManager.add_funds(_cnt.payout_credits);
                modify_standing(_cnt.faction, _cnt.reputation_gain);
                factions.faction_a.military_strength_score = min(100, factions.faction_a.military_strength_score + 8);
                array_delete(active_contracts, c, 1);
                if (instance_exists(obj_HQTerminal)) {
                    obj_HQTerminal.show_toast("ORDER DELIVERED: +" + string(_cnt.payout_credits) + " Cr! Terran Military Strength +8", c_lime);
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
                obj_GameManager.add_funds(_cnt.payout_credits);
                obj_GameManager.add_raw_material(_cnt.reward_material_id, _cnt.reward_material_amount);
                modify_standing(_cnt.faction, _cnt.reputation_gain);
                factions.faction_b.military_strength_score = min(100, factions.faction_b.military_strength_score + 10);
                array_delete(active_contracts, c, 1);
                if (instance_exists(obj_HQTerminal)) {
                    obj_HQTerminal.show_toast("BOUNTY DELIVERED: +" + string(_cnt.payout_credits) + " Cr & +" + string(_cnt.reward_material_amount) + " Tritium! Colony Strength +10", c_lime);
                }
                return true;
            }

            // C. Black Ops Sale (High risk / instant cash)
            else if (_cnt.type == "BLACK_OPS_SALE") {
                obj_GameManager.add_funds(_cnt.payout_credits);
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
        var _f = file_text_open_read("factions_lore.json");
        var _json_str = "";
        while (!file_text_eof(_f)) {
            _json_str += file_text_readln(_f);
        }
        file_text_close(_f);
        factions_lore_data = json_parse(_json_str);
        show_debug_message("[obj_FactionManager] Loaded factions_lore.json successfully.");
    } catch (_ex) {
        show_debug_message("[obj_FactionManager] Warning: could not parse factions_lore.json: " + string(_ex));
    }
}

if (file_exists("mobile_suits_timeline.json")) {
    try {
        var _f2 = file_text_open_read("mobile_suits_timeline.json");
        var _json_str2 = "";
        while (!file_text_eof(_f2)) {
            _json_str2 += file_text_readln(_f2);
        }
        file_text_close(_f2);
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
    if (variable_struct_exists(incumbent_doctrines, _faction_id)) {
        return incumbent_doctrines[$ _faction_id];
    }
    return incumbent_doctrines.faction_a;
};

run_procurement_trial = function(_faction_id, _mech) {
    var _inc = get_incumbent_specs(_faction_id);
    if (is_undefined(_mech)) return undefined;

    var _cand_armor = _mech[$ "armor_rating"] ?? 600;
    var _cand_power = _mech[$ "power_output"] ?? 10;
    var _cand_speed = _mech[$ "speed"] ?? 60;
    var _cand_combat = _mech[$ "combat_rating"] ?? 400;

    // 4 Diagnostic Phase Scores (Base 100 is exact parity with incumbent)
    var _score_armor = clamp((_cand_armor / max(1, _inc.armor)) * 100.0, 20.0, 160.0);
    var _score_power = clamp((_cand_power / max(1, _inc.power)) * 100.0, 20.0, 160.0);
    var _score_speed = clamp((_cand_speed / max(1, _inc.speed)) * 100.0, 20.0, 160.0);
    var _score_combat = clamp((_cand_combat / max(1, _inc.combat_rating)) * 100.0, 20.0, 160.0);

    var _w = _inc.weights;
    var _base_weighted = (_score_armor * _w[0]) + (_score_power * _w[1]) + (_score_speed * _w[2]) + (_score_combat * _w[3]);

    // Faction Standing Bonus (-20 to +20)
    var _st_bonus = get_standing(_faction_id) / 5.0;
    var _composite_score = round((_base_weighted + _st_bonus) * 10.0) / 10.0;

    var _passed = (_composite_score >= 100.0);

    var _report = "";
    if (_passed) {
        _report = "TENDER APPROVED: " + _mech.name + " outperformed incumbent " + _inc.name + " (" + string(_composite_score) + "/100). Faction board recommends immediate mass-production contract!";
    } else {
        var _deficit = 100.0 - _composite_score;
        _report = "TENDER REJECTED: Candidate fell short of doctrine standard by " + string(_deficit) + " pts. Improve components or boost faction standing!";
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
        composite_score: _composite_score,
        passed: _passed,
        report: _report
    };
};

award_procurement_contract = function(_faction_id, _mech, _trial_result) {
    if (!variable_struct_exists(mass_production_contracts, _faction_id)) return false;
    var _mp = mass_production_contracts[$ _faction_id];
    var _f = factions[$ _faction_id];

    _mp.replaced = true;
    _mp.replacement_name = _mech.name;
    _mp.replacement_blueprint_id = _mech[$ "blueprint_id"] ?? "bp_custom";
    _mp.combat_bonus = max(18, floor(_trial_result.composite_score / 5));

    // Award Licensing Bounty
    var _bounty = _mp.licensing_bounty;
    if (instance_exists(obj_GameManager)) {
        obj_GameManager.funds += _bounty;
        array_push(obj_GameManager.last_turn_events, "! DOCTRINE REPLACED: " + _f.name + " awarded Mass-Production Tender for " + _mech.name + "! Licensing Bounty: +" + string(_bounty) + " Cr (+" + string(_mp.royalty_per_turn) + " Cr/turn royalties)!");
    }

    // Boost Faction Military Rating & Standing
    _f.military_strength_score = min(100, _f.military_strength_score + 20);
    modify_standing(_faction_id, 25);

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
        obj_HQTerminal.show_toast("TENDER WON! " + _f.name + " OFFICIALLY ADOPTS " + _mech.name + "! +" + string(_bounty) + " Cr!", c_lime);
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
        var _slot_arr = obj_GameManager.inventory.parts[$ _item.slot] ?? [];
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
        var _slot_arr2 = obj_GameManager.inventory.parts[$ _item.slot];
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
