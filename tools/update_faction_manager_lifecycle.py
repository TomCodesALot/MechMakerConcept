import re

with open('objects/obj_FactionManager/Create_0.gml', 'r') as f:
    content = f.read()

# 1. Update mass_production_contracts to include adoption fields
target_mpc = '''    faction_a: {
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
    },'''

replacement_mpc = '''    faction_a: {
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
    },'''

if target_mpc in content:
    content = content.replace(target_mpc, replacement_mpc)
    print("Updated faction_a in mass_production_contracts")
else:
    print("WARNING: target_mpc for faction_a not matched!")

for fid in ["faction_b", "faction_c", "faction_d"]:
    pat = rf'({fid}: \{{[^}}]+req_power: \d+)'
    def repl(m):
        return m.group(1) + ',\n        adoption_stage: "UNADOPTED",\n        tooling_turns_remaining: 2,\n        active_frontline_units: 0,\n        block_level: 1'
    content = re.sub(pat, repl, content)
    print(f"Updated {fid} in mass_production_contracts")

# 2. Add run_procurement_trial_phase and adoption methods
new_methods = '''
// 10b. 4-Phase Fly-Off Tournament Engine & Modernization Lifecycle (docs/26)
run_procurement_trial_phase = function(_faction_id, _mech, _phase_idx = 4, _refinements = []) {
    var _inc = get_incumbent_specs(_faction_id);
    if (is_undefined(_mech)) return undefined;

    var _cand_armor = _mech[$ "armor_rating"] ?? 600;
    var _cand_power = _mech[$ "power_output"] ?? 10;
    var _cand_speed = _mech[$ "speed"] ?? 60;
    var _cand_combat = _mech[$ "combat_rating"] ?? 400;

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
        _pedigree_bonus = _mech.combat_pedigree[$ "telemetry_bonus"] ?? 0.0;
        _pedigree_rating = _mech.combat_pedigree[$ "pedigree_rating"] ?? "UNTESTED";
    }

    var _composite_score = round((_base_weighted + _st_bonus + _pedigree_bonus) * 10.0) / 10.0;

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
    var _mp = mass_production_contracts[$ _faction_id];
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
    var _mp = mass_production_contracts[$ _faction_id];
    if (!_mp.replaced || _mp.block_level >= 2) return false;

    _mp.block_level = 2;
    _mp.royalty_per_turn = round(_mp.royalty_per_turn * 1.25);
    _mp.combat_bonus += 4;
    var _bounty = 450000;

    if (instance_exists(obj_GameManager)) {
        obj_GameManager.funds += _bounty;
        array_push(obj_GameManager.last_turn_events, "! BLOCK II MODERNIZATION: " + _mp.faction_name + " accepted Block II spec for " + _mp.replacement_name + "! Modernization Bounty: +" + string(_bounty) + " Cr!");
    }
    var _f = factions[$ _faction_id];
    _f.military_strength_score = min(100, _f.military_strength_score + 10);

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("BLOCK II MODERNIZED! +" + string(_bounty) + " Cr Bounty & +25% Royalties!", c_lime);
    }
    return true;
};

upgrade_adoption_block_iii = function(_faction_id) {
    if (!variable_struct_exists(mass_production_contracts, _faction_id)) return false;
    var _mp = mass_production_contracts[$ _faction_id];
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
    var _f = factions[$ _faction_id];
    _f.military_strength_score = min(100, _f.military_strength_score + 15);

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("BLOCK III APEX RATIFIED! +" + string(_bounty) + " Cr & Ace Unit Commissioned!", c_lime);
    }
    return true;
};
'''

# 3. Update award_procurement_contract to initialize adoption fields
target_award = '''    _mp.replaced = true;
    _mp.replacement_name = _mech.name;
    _mp.replacement_blueprint_id = _mech[$ "blueprint_id"] ?? "bp_custom";
    _mp.combat_bonus = max(_is_upgrade ? _mp.combat_bonus + 4 : 18, floor(_trial_result.composite_score / 5));'''

replacement_award = '''    _mp.replaced = true;
    _mp.replacement_name = _mech.name;
    _mp.replacement_blueprint_id = _mech[$ "blueprint_id"] ?? "bp_custom";
    _mp.combat_bonus = max(_is_upgrade ? _mp.combat_bonus + 4 : 18, floor(_trial_result.composite_score / 5));
    _mp.adoption_stage = "TOOLING";
    _mp.tooling_turns_remaining = 2;
    _mp.active_frontline_units = 0;
    _mp.block_level = _is_upgrade ? min(3, _mp.block_level + 1) : 1;'''

if target_award in content:
    content = content.replace(target_award, replacement_award)
    print("Updated award_procurement_contract adoption fields")
else:
    print("WARNING: target_award not found!")

# Insert new methods before commodity trade system
trade_hook = '// 11. Interstellar Commodity Trade System'
if trade_hook in content:
    content = content.replace(trade_hook, new_methods + '\n' + trade_hook)
    print("Inserted new trial phase and adoption methods")
else:
    content += '\n' + new_methods

with open('objects/obj_FactionManager/Create_0.gml', 'w') as f:
    f.write(content)
print("Updated obj_FactionManager/Create_0.gml successfully")
