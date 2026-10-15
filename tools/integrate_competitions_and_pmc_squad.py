import sys

def update_game_manager():
    with open('objects/obj_GameManager/Create_0.gml', 'r') as f:
        content = f.read()

    old_mechs = '''    deployable_mechs: [
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
    ]'''

    new_mechs = '''    deployable_mechs: [
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
            combat_rating: 480,
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
        }
    ]'''

    if old_mechs not in content:
        print("ERROR: old_mechs not found in obj_GameManager/Create_0.gml")
        return False
    content = content.replace(old_mechs, new_mechs)

    old_custom = '''        part_composition: {
            head: _hd,
            torso: _tr,
            arms: _am,
            legs: _lg,
            backpack: _bp,
            weapon: _wp
        }
    };'''

    new_custom = '''        part_composition: {
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
    };'''

    if old_custom not in content:
        print("ERROR: old_custom not found in obj_GameManager/Create_0.gml")
        return False
    content = content.replace(old_custom, new_custom)

    old_bp_hook = '''get_blueprint = function(_blueprint_id) {
    if (instance_exists(obj_BlueprintManager)) return obj_BlueprintManager.get_blueprint(_blueprint_id);
    return undefined;
};'''

    new_bp_hook = '''get_blueprint = function(_blueprint_id) {
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
    blueprint_weakness_bonuses[$ _bp_id] = {
        blueprint_id: _bp_id,
        name: _mech_name,
        crit_bonus_pct: 15,
        armor_pierce_pct: 20,
        registered_turn: current_turn
    };
    show_debug_message("[BlueprintWeakness] Arms Dealer Paradox: PMC pilots gain +15% Crit / +20% AP vs " + _mech_name + " (" + _bp_id + ")!");
};'''

    if old_bp_hook not in content:
        print("ERROR: old_bp_hook not found in obj_GameManager/Create_0.gml")
        return False
    content = content.replace(old_bp_hook, new_bp_hook)

    with open('objects/obj_GameManager/Create_0.gml', 'w') as f:
        f.write(content)
    print("Successfully updated objects/obj_GameManager/Create_0.gml")
    return True

def update_faction_manager():
    with open('objects/obj_FactionManager/Create_0.gml', 'r') as f:
        content = f.read()

    old_trial = '''    // Faction Standing Bonus (-20 to +20)
    var _st_bonus = get_standing(_faction_id) / 5.0;
    var _composite_score = round((_base_weighted + _st_bonus) * 10.0) / 10.0;

    var _passed = (_composite_score >= 100.0);

    var _report = "";
    if (_passed) {
        _report = "TENDER APPROVED: " + _mech.name + " outperformed incumbent " + _inc.name + " (" + string(_composite_score) + "/100). Faction board recommends immediate mass-production contract!";
    } else {
        var _deficit = 100.0 - _composite_score;
        _report = "TENDER REJECTED: Candidate fell short of doctrine standard by " + string(_deficit) + " pts. Improve components or boost faction standing!";
    }'''

    new_trial = '''    // Faction Standing Bonus (-20 to +20)
    var _st_bonus = get_standing(_faction_id) / 5.0;

    // Combat-Proven Pedigree Telemetry Bonus (0 to 25 pts) from active PMC squad deployments (docs/25)
    var _pedigree_bonus = 0.0;
    var _pedigree_rating = "UNTESTED";
    if (variable_struct_exists(_mech, "combat_pedigree") && is_struct(_mech.combat_pedigree)) {
        _pedigree_bonus = _mech.combat_pedigree[$ "telemetry_bonus"] ?? 0.0;
        _pedigree_rating = _mech.combat_pedigree[$ "pedigree_rating"] ?? "UNTESTED";
    }

    var _composite_score = round((_base_weighted + _st_bonus + _pedigree_bonus) * 10.0) / 10.0;

    var _passed = (_composite_score >= 100.0);

    var _report = "";
    if (_passed) {
        _report = "TENDER APPROVED: " + _mech.name + " outperformed incumbent " + _inc.name + " (" + string(_composite_score) + "/100). Faction board recommends immediate mass-production contract!";
        if (_pedigree_bonus > 0) {
            _report += " [Combat Telemetry: " + _pedigree_rating + " (+" + string(_pedigree_bonus) + " pts)]";
        }
    } else {
        var _deficit = 100.0 - _composite_score;
        _report = "TENDER REJECTED: Candidate fell short of doctrine standard by " + string(_deficit) + " pts. Improve components, boost faction standing, or deploy in PMC combat for field telemetry!";
    }'''

    if old_trial not in content:
        print("ERROR: old_trial not found in obj_FactionManager/Create_0.gml")
        return False
    content = content.replace(old_trial, new_trial)

    old_ret = '''        score_combat: round(_score_combat),
        standing_bonus: round(_st_bonus),
        composite_score: _composite_score,
        passed: _passed,
        report: _report'''

    new_ret = '''        score_combat: round(_score_combat),
        standing_bonus: round(_st_bonus),
        pedigree_bonus: _pedigree_bonus,
        pedigree_rating: _pedigree_rating,
        composite_score: _composite_score,
        passed: _passed,
        report: _report'''

    if old_ret not in content:
        print("ERROR: old_ret not found in obj_FactionManager/Create_0.gml")
        return False
    content = content.replace(old_ret, new_ret)

    old_award = '''    _mp.replaced = true;
    _mp.replacement_name = _mech.name;
    _mp.replacement_blueprint_id = _mech[$ "blueprint_id"] ?? "bp_custom";
    _mp.combat_bonus = max(_is_upgrade ? _mp.combat_bonus + 4 : 18, floor(_trial_result.composite_score / 5));'''

    new_award = '''    _mp.replaced = true;
    _mp.replacement_name = _mech.name;
    _mp.replacement_blueprint_id = _mech[$ "blueprint_id"] ?? "bp_custom";
    _mp.combat_bonus = max(_is_upgrade ? _mp.combat_bonus + 4 : 18, floor(_trial_result.composite_score / 5));

    // Register Blueprint Weakness in obj_GameManager (Arms Dealer Paradox - docs/25)
    if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "register_exported_blueprint_weakness")) {
        obj_GameManager.register_exported_blueprint_weakness(_mp.replacement_blueprint_id, _mech.name);
    }'''

    if old_award not in content:
        print("ERROR: old_award not found in obj_FactionManager/Create_0.gml")
        return False
    content = content.replace(old_award, new_award)

    with open('objects/obj_FactionManager/Create_0.gml', 'w') as f:
        f.write(content)
    print("Successfully updated objects/obj_FactionManager/Create_0.gml")
    return True

def update_hq_terminal():
    with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
        content = f.read()

    old_card = '''                    draw_set_color(make_color_rgb(160, 190, 220));
                    draw_text(_tr_x + 14, _my_box + 24, "Class: " + (_mitem[$ "class"] ?? "Mobile Suit") + " | Status: " + _mitem.status);'''

    new_card = '''                    var _ped_badge = "UNTESTED";
                    var _ped_bonus = 0.0;
                    if (variable_struct_exists(_mitem, "combat_pedigree") && is_struct(_mitem.combat_pedigree)) {
                        _ped_badge = _mitem.combat_pedigree[$ "pedigree_rating"] ?? "UNTESTED";
                        _ped_bonus = _mitem.combat_pedigree[$ "telemetry_bonus"] ?? 0.0;
                    }
                    draw_set_color((_ped_bonus > 0) ? make_color_rgb(255, 215, 80) : make_color_rgb(140, 160, 180));
                    draw_text(_tr_x + 14, _my_box + 24, "Pedigree: " + _ped_badge + ((_ped_bonus > 0) ? " (+" + string(_ped_bonus) + " pts)" : "") + " | " + _mitem.status);'''

    if old_card not in content:
        print("ERROR: old_card not found in obj_HQTerminal/Draw_64.gml")
        return False
    content = content.replace(old_card, new_card)

    old_banner = '''                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_col2_x + 24, _res_y + 66, "Faction Standing Bonus: +" + string(trial_last_result.standing_bonus) + " pts   ==>   COMPOSITE SCORE: " + string(trial_last_result.composite_score) + " / 100.0 PTS");'''

    new_banner = '''                var _ped_str = (variable_struct_exists(trial_last_result, "pedigree_bonus") && trial_last_result.pedigree_bonus > 0) ?
                    (" | Combat Pedigree: +" + string(trial_last_result.pedigree_bonus) + " pts [" + string(trial_last_result.pedigree_rating) + "]") :
                    " | Pedigree: Untested (+0 pts)";
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_col2_x + 24, _res_y + 66, "Standing: +" + string(trial_last_result.standing_bonus) + " pts" + _ped_str + " ==> COMPOSITE: " + string(trial_last_result.composite_score) + " / 100.0 PTS");'''

    if old_banner not in content:
        print("ERROR: old_banner not found in obj_HQTerminal/Draw_64.gml")
        return False
    content = content.replace(old_banner, new_banner)

    with open('objects/obj_HQTerminal/Draw_64.gml', 'w') as f:
        f.write(content)
    print("Successfully updated objects/obj_HQTerminal/Draw_64.gml")
    return True

if __name__ == '__main__':
    if not update_game_manager(): sys.exit(1)
    if not update_faction_manager(): sys.exit(1)
    if not update_hq_terminal(): sys.exit(1)
    print("ALL 3 FILES INTEGRATED CLEANLY!")
