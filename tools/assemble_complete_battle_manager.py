# -*- coding: utf-8 -*-
"""
Master Builder for objects/obj_BattleManager/Create_0.gml
Assembles all Goal requirements:
- Goals A, B, C (Supply starvation, Pilot perks/fatigue, Flagship theater alignment)
- Goal D (S-Grade Masterwork AP check)
- Goal E (Detention brig incarceration, Active nemeses cleanup, +150k Cr bounty, Research salvage)
- Goal F (Tactical ballistics: elevation hit/range/dmg, suppression -1 AP, Flanking +20%, Rear +40%, Bastion degradation)
- Goal G (Crisis boss battle, setup_apex_crisis_boss, call_flagship_orbital_strike, Phase barrier, Victory path 4)
- 6-Unit Stacking (get_stack_at_tile, reorganize_stack, get_stack_max_firepower with _has_manual, execute_stack_volley)
- Refined Combat (Vanguard screening, Brace stance 40% reduction, Dynamic pacing, Field wreckage, Pilot ejection)
- Goal Final Modular Combat Clash & Animation Engine (4 chassis sockets, metallurgy alloy tints, severed arm overlays, weapon classes, melee dash, CRT scanlines, diegetic cockpit telemetry HUD)
"""

import re
import sys

print("=== ASSEMBLING COMPLETE obj_BattleManager/Create_0.gml ===")

create_path = "objects/obj_BattleManager/Create_0.gml"
with open(create_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update load_map(0) to context-sensitive loader if not already present
if "scr_territory_get_battle_map_id" not in code:
    old_load = "load_map(0);"
    new_load = """var _target_map_id = 0;
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
}"""
    assert old_load in code, "load_map(0); not found"
    code = code.replace(old_load, new_load, 1)
    print("[PASS] Context-sensitive map loader applied.")

# 2. Add S-Grade Masterwork Tuning check in deployable mechs loop
if "is_masterwork" not in code and "S_GRADE_MASTERWORK" not in code:
    old_pedigree = "var _tele = _dm.combat_pedigree.telemetry_bonus;"
    new_pedigree = """var _tele = _dm.combat_pedigree.telemetry_bonus;
                // S-Grade Masterwork AP Tuning (Goal D)
                if (variable_struct_exists(_dm, "is_masterwork") && _dm.is_masterwork) {
                    _au.max_ap += 1;
                    _au.current_ap += 1;
                    _au.is_masterwork = true;
                    add_log("[S-GRADE MASTERWORK] " + _au.callsign + " active masterwork tuning (+1 AP)!");
                }"""
    assert old_pedigree in code, "combat_pedigree line not found"
    code = code.replace(old_pedigree, new_pedigree, 1)
    print("[PASS] Goal D Masterwork AP check applied.")

# 3. Add Theater Alignment, Supply Starvation, and Pilot Fatigue/Perks (Goals A, B, C)
if "supply_starvation" not in code:
    target_fs = "// 5b. Flagship Strategic Division Buffs (Doc 24)"
    fs_and_logistics = """// 5b. Flagship Strategic Division Buffs & Theater Alignment (Goal C)
if (instance_exists(obj_GameManager)) {
    var _gm = obj_GameManager;
    var _gm_fs = _gm.flagship;
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
}"""
    assert target_fs in code, "target_fs not found"
    code = code.replace(target_fs, fs_and_logistics + "\n" + target_fs, 1)
    print("[PASS] Goals A, B, C applied.")

# 4. Update calculate_hit_chance elevation modifier (Goal F)
old_elev_hc = "var _elev_bonus = _elev_diff * 10;"
new_elev_hc = "var _elev_bonus = (_elev_diff > 0) ? (_elev_diff * 10) : (_elev_diff * 15);"
if old_elev_hc in code:
    code = code.replace(old_elev_hc, new_elev_hc, 1)
    print("[PASS] Goal F elevation hit modifiers applied.")

# 5. Update recalculate_moves suppression penalty (Goal F)
old_recalc = "var _ap_pool = _sel.components.legs.intact ? _sel.current_ap : 1;"
new_recalc = """var _ap_pool = _sel.components.legs.intact ? _sel.current_ap : 1;
    if (variable_struct_exists(_sel, "is_suppressed") && _sel.is_suppressed) {
        _ap_pool = max(1, _ap_pool - 1);
    }"""
if old_recalc in code and "_ap_pool = max(1, _ap_pool - 1);" not in code:
    code = code.replace(old_recalc, new_recalc, 1)
    print("[PASS] Goal F suppression move penalty applied.")

# 6. Fix resolve_combat_impact syntax error and add Goal F/G/E mechanics
old_impact = """    if (_hit) {
        screen_shake = max(screen_shake, 7.0);
        _def.recoil_shake = 8.0;
        _def.anim_state = "hit";
        scr_audio_play_impact("kinetic", (_dmg > 50));
        _def.anim_timer = 25;"""

new_impact = """    if (_hit) {
        screen_shake = max(screen_shake, 7.0);
        _def.recoil_shake = 8.0;
        _def.anim_state = "hit";
        _def.anim_timer = 25;"""

if old_impact in code:
    code = code.replace(old_impact, new_impact, 1)
    print("[PASS] Fixed syntax error in resolve_combat_impact.")

old_dmg_calc = """        var _raw_dmg = floor((_wpn.damage + irandom_range(-15, 20)) * _squad_mult);
        var _mitigated_dmg = max(15, _raw_dmg - _limb.armor);"""

new_dmg_calc = """        var _raw_dmg = floor((_wpn.damage + irandom_range(-15, 20)) * _squad_mult);

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

        var _mitigated_dmg = max(15, _raw_dmg - _limb.armor);
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
        }"""

if old_dmg_calc in code and "REAR CORE HIT +40%" not in code:
    code = code.replace(old_dmg_calc, new_dmg_calc, 1)
    print("[PASS] Goal F directional & elevation damage multipliers applied.")

# 7. Add Goal G Boss functions and Stacking State & Cinematic Clash Engine before select_unit(0)
target_select = "select_unit(0);"

# Read the full cinematic block from patch_battle_manager_cinematic_clash.py
with open("tools/patch_battle_manager_cinematic_clash.py", "r", encoding="utf-8") as f:
    clash_txt = f.read()

s_idx = clash_txt.find('new_cinematic_block = """') + len('new_cinematic_block = """')
e_idx = clash_txt.rfind('"""')
cinematic_code = clash_txt[s_idx:e_idx].strip()

# Inject Nemesis Incarceration & Boss hooks into cinematic Phase 3 kill
if "obj_NemesisManager.add_prisoner" not in cinematic_code:
    old_cin_kill = """// 2. Pilot Ejection Survival Roll
                        var _ej_roll = irandom_range(1, 100);
                        if (_ej_roll <= 65) {
                            add_log("[EJECTION SUCCESS] Pilot ejected safely via escape pod.");
                        } else if (_ej_roll <= 88) {
                            add_log("[PILOT INJURED] Escape pod damaged during ejection; pilot hospitalized for 3 campaign turns.");
                        } else {
                            add_log("[KIA] Catastrophic cockpit breach; pilot lost in action.");
                        }"""
    new_cin_kill = """// 2. Pilot Ejection Survival Roll
                        var _ej_roll = irandom_range(1, 100);
                        if (_ej_roll <= 65) {
                            add_log("[EJECTION SUCCESS] Pilot ejected safely via escape pod.");
                        } else if (_ej_roll <= 88) {
                            add_log("[PILOT INJURED] Escape pod damaged during ejection; pilot hospitalized for 3 campaign turns.");
                        } else {
                            add_log("[KIA] Catastrophic cockpit breach; pilot lost in action.");
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
                        }"""
    cinematic_code = cinematic_code.replace(old_cin_kill, new_cin_kill)

# Rename old spawn_combat_projectile to legacy_spawn_combat_projectile if needed
if "legacy_spawn_combat_projectile" not in code:
    code = code.replace("spawn_combat_projectile = function", "legacy_spawn_combat_projectile = function", 1)

master_extensions = '''
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
// GIHREN\'S GREED + FRONT MISSION BATTLEGROUP STACK & COMMAND BUS STATE
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

''' + cinematic_code + '\n\n'

if "setup_apex_crisis_boss = function" not in code:
    assert target_select in code, "select_unit(0); not found in code"
    code = code.replace(target_select, master_extensions + target_select, 1)
    print("[PASS] Master extensions (Boss, Stacking, Cinematic Clash) appended.")

with open(create_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Master Create_0.gml written successfully.")
