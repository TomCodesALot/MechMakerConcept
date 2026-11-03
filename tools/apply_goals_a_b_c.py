import re

print("Implementing Goal A, B, and C in MechMakerConcept...")

# --------------------------------------------------------------------------
# 1. Update obj_GameManager/Create_0.gml
# --------------------------------------------------------------------------
with open('objects/obj_GameManager/Create_0.gml', 'r') as f:
    gm_code = f.read()

# Add supply_starvation, mech_upkeep parameters, and pilot helper functions
target_init_anchor = 'escrow_funds = 0;'
replacement_init = '''escrow_funds = 0;       // Escrow withheld for pending operations

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
};'''

assert target_init_anchor in gm_code, "target_init_anchor not found in obj_GameManager/Create_0.gml"
gm_code = gm_code.replace(target_init_anchor, replacement_init, 1)

# Ensure starter pilots have fatigue, xp, rank_perks
old_vance = '{ id: "pilot_terran_vance_starter", character_id: "pilot_terran_vance_starter", name: "Lt. Marcus Vance", callsign: "VANGUARD-1", combat_stat: 9, tactics_stat: 8, accuracy: 88, reflexes: 75, morale: 95, salary_daily: 220, is_deployed: true, status: "ACTIVE", recovery_days: 0, recovery_days_left: 0, kills: 3, sorties: 5 }'
new_vance = '{ id: "pilot_terran_vance_starter", character_id: "pilot_terran_vance_starter", name: "Lt. Marcus Vance", callsign: "VANGUARD-1", combat_stat: 9, tactics_stat: 8, accuracy: 88, reflexes: 75, morale: 95, salary_daily: 220, is_deployed: true, status: "ACTIVE", recovery_days: 0, recovery_days_left: 0, kills: 3, sorties: 5, fatigue: 0, xp: 120, rank_perks: ["Quick Draw"] }'

old_cole = '{ id: "pilot_terran_cole", character_id: "pilot_terran_cole", name: "Sgt. Sarah Cole", callsign: "DEATHBLOW", combat_stat: 8, tactics_stat: 7, accuracy: 82, reflexes: 79, morale: 88, salary_daily: 190, is_deployed: false, status: "ACTIVE", recovery_days: 0, recovery_days_left: 0, kills: 1, sorties: 2 }'
new_cole = '{ id: "pilot_terran_cole", character_id: "pilot_terran_cole", name: "Sgt. Sarah Cole", callsign: "DEATHBLOW", combat_stat: 8, tactics_stat: 7, accuracy: 82, reflexes: 79, morale: 88, salary_daily: 190, is_deployed: false, status: "ACTIVE", recovery_days: 0, recovery_days_left: 0, kills: 1, sorties: 2, fatigue: 0, xp: 45, rank_perks: [] }'

if old_vance in gm_code: gm_code = gm_code.replace(old_vance, new_vance)
if old_cole in gm_code: gm_code = gm_code.replace(old_cole, new_cole)

# Update advance_turn() in obj_GameManager to calculate Fleet Upkeep, Tritium Burn, and Pilot Recovery
target_fiscal_start = 'var _daily_maintenance = 150 + (facilities.assembly_lines - 1) * 75;'
replacement_fiscal = '''// Fleet Chassis Maintenance & Reactor Tritium Burn (Goal A)
    var _num_mechs = (variable_struct_exists(inventory, "deployable_mechs") && is_array(inventory.deployable_mechs)) ? array_length(inventory.deployable_mechs) : 0;
    total_fleet_upkeep_cr = _num_mechs * mech_upkeep_cr_per_unit;
    total_fleet_tritium_burn = (_num_mechs > 0) ? max(1, ceil(_num_mechs / mech_upkeep_tritium_ratio)) : 0;

    // Deduct Tritium fuel for Tokamak magnetic bottles
    if (variable_struct_exists(inventory.raw_materials, "mat_tritium")) {
        inventory.raw_materials.mat_tritium -= total_fleet_tritium_burn;
    }

    var _daily_maintenance = 150 + (facilities.assembly_lines - 1) * 75 + total_fleet_upkeep_cr;'''

assert target_fiscal_start in gm_code, "target_fiscal_start not found in advance_turn"
gm_code = gm_code.replace(target_fiscal_start, replacement_fiscal, 1)

target_bankrupt = '''    // Bankruptcy warning
    if (funds < 0) {
        array_push(last_turn_events, "! FISCAL CRISIS: Company operational accounts are currently overdrawn!");
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("FINANCIAL CRISIS: TREASURY DEFICIT!", c_red);
        }
    }'''

replacement_bankrupt = '''    // Check Supply Starvation & Fuel Reserves (Goal A)
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
                    if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("PILOT DISCHARGED: " + _plt.callsign + " is active!", c_lime);
                }
            } else if (_plt.status == "ACTIVE") {
                // Non-deployed resting pilots dissipate fatigue
                _plt.fatigue = max(0, _plt.fatigue - 1);
            }
        }
    }'''

assert target_bankrupt in gm_code, "target_bankrupt not found in advance_turn"
gm_code = gm_code.replace(target_bankrupt, replacement_bankrupt, 1)

with open('objects/obj_GameManager/Create_0.gml', 'w') as f:
    f.write(gm_code)

print("[1/3] obj_GameManager/Create_0.gml updated with Logistics, Upkeep, and Pilot Engine!")

# --------------------------------------------------------------------------
# 2. Update obj_BattleManager/Create_0.gml
# --------------------------------------------------------------------------
with open('objects/obj_BattleManager/Create_0.gml', 'r') as f:
    bm_code = f.read()

# Replace lines 2038+ where Flagship buffs are applied to verify theater alignment
old_fs_buffs = '''// 5b. Flagship Strategic Division Buffs (Doc 24)
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
    }'''

new_fs_buffs = '''// 5b. Flagship Strategic Division Buffs & Theater Alignment (Goal C)
if (instance_exists(obj_GameManager)) {
    var _gm = obj_GameManager;
    var _gm_fs = _gm.flagship;
    var _in_theater = _gm.flagship_is_in_theater(_cur_map.theater);

    if (_in_theater) {
        add_log("[ORBITAL SUPPORT ONLINE] USN-X Hephaestus in position over " + _cur_map.theater + " theater.");
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
    } else if (_gm_fs.transit_turns_left > 0) {
        add_log("[ORBITAL SUPPORT OFFLINE] Hephaestus in transit to " + _gm_fs.destination_sphere + " (" + string(_gm_fs.transit_turns_left) + "T).");
    } else {
        add_log("[ORBITAL SUPPORT OFFLINE] Hephaestus stationed in " + _gm_fs.current_sphere + " (out of range).");
    }'''

assert old_fs_buffs in bm_code, "old_fs_buffs not found in obj_BattleManager/Create_0.gml"
bm_code = bm_code.replace(old_fs_buffs, new_fs_buffs, 1)

# Add Supply Starvation debuff and Pilot Perks/Fatigue in obj_BattleManager/Create_0.gml
target_stat_escalation = '// 5c. Ongoing Campaign Reflection: Tech Era Escalation & Competitor R&D Lineage (Doc 27)'
replacement_stat_escalation = '''// 5c-1. Strategic Logistics & Supply Starvation Check (Goal A)
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
            // Find pilot matching this unit or default to first pilot
            var _matched_p = undefined;
            for (var p = 0; p < array_length(_r_pilots); p++) {
                if (_r_pilots[p].status == "ACTIVE") {
                    _matched_p = _r_pilots[p];
                    break;
                }
            }

            if (_matched_p != undefined) {
                _un.pilot_ref_id = _matched_p.id;
                // Pilot Fatigue Check
                if (variable_struct_exists(_matched_p, "fatigue") && _matched_p.fatigue >= 3) {
                    _un.accuracy = max(20, _un.accuracy - 15);
                    _un.evasion = max(0, _un.evasion - 15);
                    add_log("[FATIGUED PILOT] " + _matched_p.name + " (" + _matched_p.callsign + ") suffering combat exhaustion (-15% Acc/Eva)!");
                }
                // Pilot Ace Perks
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

// 5c. Ongoing Campaign Reflection: Tech Era Escalation & Competitor R&D Lineage (Doc 27)'''

assert target_stat_escalation in bm_code, "target_stat_escalation not found in obj_BattleManager/Create_0.gml"
bm_code = bm_code.replace(target_stat_escalation, replacement_stat_escalation, 1)

with open('objects/obj_BattleManager/Create_0.gml', 'w') as f:
    f.write(bm_code)

print("[2/3] obj_BattleManager/Create_0.gml updated with Theater check, Starvation, and Pilot Perks!")

# --------------------------------------------------------------------------
# 3. Update obj_BattleManager/Draw_64.gml to award Pilot XP and apply Fatigue
# --------------------------------------------------------------------------
with open('objects/obj_BattleManager/Draw_64.gml', 'r') as f:
    draw_code = f.read()

target_aar_return = '''                obj_GameManager.last_battle_report = {
                    is_win: _is_win,
                    sector_id: _ctx.sector_id,
                    sector_name: _ctx.sector_name,
                    controlling_faction: _ctx.controlling_faction
                };
                obj_GameManager.active_combat_context = undefined;
            }'''

replacement_aar_return = '''                obj_GameManager.last_battle_report = {
                    is_win: _is_win,
                    sector_id: _ctx.sector_id,
                    sector_name: _ctx.sector_name,
                    controlling_faction: _ctx.controlling_faction
                };
                obj_GameManager.active_combat_context = undefined;
            }

            // Award Pilot Combat XP & Accumulate Sortie Fatigue (Goal B)
            if (variable_struct_exists(obj_GameManager.facilities, "roster_pilots")) {
                var _xp_reward = _is_win ? 40 : 15;
                for (var p = 0; p < array_length(obj_GameManager.facilities.roster_pilots); p++) {
                    var _plt = obj_GameManager.facilities.roster_pilots[p];
                    if (_plt.status == "ACTIVE") {
                        _plt.sorties = (variable_struct_exists(_plt, "sorties") ? _plt.sorties : 0) + 1;
                        _plt.fatigue = min(5, (variable_struct_exists(_plt, "fatigue") ? _plt.fatigue : 0) + 1);
                        obj_GameManager.pilot_add_xp(_plt.id, _xp_reward);
                    }
                }
            }'''

assert target_aar_return in draw_code, "target_aar_return not found in obj_BattleManager/Draw_64.gml"
draw_code = draw_code.replace(target_aar_return, replacement_aar_return, 1)

with open('objects/obj_BattleManager/Draw_64.gml', 'w') as f:
    f.write(draw_code)

print("[3/3] obj_BattleManager/Draw_64.gml updated with Pilot XP & Fatigue at AAR resolution!")
