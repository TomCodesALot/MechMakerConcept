import re

fp = "objects/obj_FactionManager/Create_0.gml"
with open(fp, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update factions struct with AI Brain properties
target_factions = """factions = {
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
};"""

replacement_factions = """factions = {
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
    }
};"""

assert target_factions in text, "target_factions not found"
text = text.replace(target_factions, replacement_factions, 1)

# 2. Add Section 4 to evaluate_faction_ai_turn
target_eval_end = """        // Hegemon was beaten back below 38%
        var _max_pct = max(_tc.terran_pct, _tc.colony_pct, _tc.syndicate_pct, _tc.zaibatsu_pct);
        if (_max_pct < 35) {
            coalition_active = false;
            hegemon_faction_id = "";
            add_diplomatic_cable("Solar Council", "All Factions", "COALITION DISSOLVED: Sol Balance Restored", "Anti-hegemonic emergency measures deactivated as territory balances re-stabilize.", "NORMAL", "COLD_WAR");
        }
    }
};"""

replacement_eval_end = """        // Hegemon was beaten back below 38%
        var _max_pct = max(_tc.terran_pct, _tc.colony_pct, _tc.syndicate_pct, _tc.zaibatsu_pct);
        if (_max_pct < 35) {
            coalition_active = false;
            hegemon_faction_id = "";
            add_diplomatic_cable("Solar Council", "All Factions", "COALITION DISSOLVED: Sol Balance Restored", "Anti-hegemonic emergency measures deactivated as territory balances re-stabilize.", "NORMAL", "COLD_WAR");
        }
    }

    // 4. Individual Faction AI Brains & Dynamic Behavioral State Evaluation (docs/36)
    var _f_ids = ["faction_a", "faction_b", "faction_c", "faction_d"];
    for (var fi = 0; fi < array_length(_f_ids); fi++) {
        var _fid = _f_ids[fi];
        var _f = factions[$ _fid];
        var _fpct = 25;
        if (_fid == "faction_a") _fpct = _tc.terran_pct;
        else if (_fid == "faction_b") _fpct = _tc.colony_pct;
        else if (_fid == "faction_c") _fpct = _tc.syndicate_pct;
        else if (_fid == "faction_d") _fpct = _tc.zaibatsu_pct;

        // Check if currently engaged in active WAR with any faction
        var _in_war = false;
        for (var wk = 0; wk < array_length(_keys); wk++) {
            var _wrel = diplomatic_relations[$ _keys[wk]];
            if ((_wrel.faction_1 == _fid || _wrel.faction_2 == _fid) && _wrel.state == "WAR") {
                _in_war = true;
                break;
            }
        }

        var _old_ai_state = _f[$ "ai_state"] ?? "PEACE";

        // DESPERATE STATE: Territory <= 18% OR Military Strength <= 25
        if (_fpct <= 18 || _f.military_strength_score <= 25) {
            _f.ai_state = "DESPERATE";
            _f.contract_bounty_multiplier = 2.0; // Emergency bailout tenders pay +100% bounties!
            if (!_f.superweapon_unsealed) {
                _f.superweapon_unsealed = true;
                var _sw_name = _f[$ "superweapon_name"] ?? "Apex Prototype";
                add_diplomatic_cable(_fid, "EMERGENCY MEASURE: " + _f.name + " unseals forbidden warframe [" + _sw_name + "] and issues emergency PMC bailout tenders (+100% Bounty)!");
            }
        }
        // WINNING STATE: Territory >= 38% OR Military Strength >= 70
        else if (_fpct >= 38 || _f.military_strength_score >= 70) {
            _f.ai_state = "WINNING";
            _f.contract_bounty_multiplier = 0.85; // Imperial hubris squeezes mercenary profit margins
            if (_old_ai_state != "WINNING") {
                add_diplomatic_cable(_fid, "HEGEMONIC ASCENDANCY: " + _f.name + " claims strategic superiority across Sol. Planetary tariffs and mineral quotas enforced.");
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
};"""

assert target_eval_end in text, "target_eval_end not found"
text = text.replace(target_eval_end, replacement_eval_end, 1)

with open(fp, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully updated objects/obj_FactionManager/Create_0.gml with AI Brain State Machine!")
