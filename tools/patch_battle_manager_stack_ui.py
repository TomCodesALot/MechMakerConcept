import sys

with open('objects/obj_BattleManager/Create_0.gml', 'r') as f:
    text_create = f.read()

# Append Battlegroup Stack & Command Bus variables to Create_0.gml
stack_ui_create = '''
// =========================================================================
// GIHREN'S GREED + FRONT MISSION BATTLEGROUP STACK & COMMAND BUS STATE
// =========================================================================
stack_drawer_open = true;
stack_drawer_x = 1046.0;
stack_drawer_target_x = 1046.0;
stack_drawer_w = 320;

split_mode_active = false;
split_selected_units = {};
reorg_mode_active = false;

// Initialize formation_slot on each unit if not defined (0-2: Vanguard, 3-5: Support)
for (var u = 0; u < array_length(units); u++) {
    if (!variable_struct_exists(units[u], "formation_slot")) {
        units[u].formation_slot = u % 6;
    }
}

// Helper: Get living units occupying tile (col, row), optionally filtered by team
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
    // Sort stack: Vanguard (formation_slot 0..2) first, Support (3..5) second
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

// Helper: Reorganize stack formation (swaps vanguard and support)
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

// Helper: Automated Maximum Firepower - Computes best weapon for each unit in stack against target
get_stack_max_firepower = function(_atk_stack, _def_target, _dist) {
    var _firing_plan = [];
    var _total_min_dmg = 0;
    var _total_max_dmg = 0;

    for (var u = 0; u < array_length(_atk_stack); u++) {
        var _au = _atk_stack[u];
        if (_au.current_ap <= 0 || _au.is_destroyed) continue;

        var _best_w = undefined;
        var _best_dmg = -1;

        for (var w = 0; w < array_length(_au.weapons); w++) {
            var _cand_w = _au.weapons[w];
            if (_dist >= _cand_w.range_min && _dist <= _cand_w.range_max && _au.current_ap >= _cand_w.ap_cost) {
                var _is_tgt_air = (variable_struct_exists(_def_target, "is_aircraft") && _def_target.is_aircraft) || (variable_struct_get(_def_target, "move_type") == "aero");
                var _is_atk_air = (variable_struct_exists(_au, "is_aircraft") && _au.is_aircraft) || (variable_struct_get(_au, "move_type") == "aero");
                if (_cand_w.proj_type == "MELEE" && _is_tgt_air && !_is_atk_air) continue;

                if (_cand_w.damage > _best_dmg) {
                    _best_dmg = _cand_w.damage;
                    _best_w = _cand_w;
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

// Helper: Execute Stack Volley (Automated Maximum Firepower)
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

    // Deduct AP & Heat for all participating units
    for (var p = 0; p < array_length(_fp.plan); p++) {
        var _item = _fp.plan[p];
        _item.unit.current_ap -= _item.weapon.ap_cost;
        _item.unit.current_heat += _item.weapon.heat_cost;
        _item.unit.facing = iso_get_facing(_item.unit.grid_c, _item.unit.grid_r, _def_target.grid_c, _def_target.grid_r);
        _item.unit.anim_state = _item.weapon.anim_state;
        _item.unit.anim_timer = 28;
    }

    add_log("[BATTLEGROUP SALVO] " + string(_fp.unit_count) + " unit(s) unleashed Automated Maximum Firepower against " + _def_target.callsign + "!");

    // Launch Gihren's Greed Battle Clash Cutscene
    start_battle_cinematic(_lead_u, _def_target, _lead_w, COMBAT_STATE.ATTACK_EXECUTION);
    state = COMBAT_STATE.ATTACK_EXECUTION;
    return true;
};
'''

if 'stack_drawer_open' not in text_create:
    text_create += stack_ui_create
    with open('objects/obj_BattleManager/Create_0.gml', 'w') as f:
        f.write(text_create)
    print("Successfully patched Create_0.gml with Battlegroup Stack & Command Bus logic!")
else:
    print("Create_0.gml already contains stack_drawer_open.")
