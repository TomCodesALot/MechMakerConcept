import sys

# 1. Update Step_0.gml
with open('objects/obj_BattleManager/Step_0.gml', 'r') as f:
    text_step = f.read()

# Add drawer animation at the start of Step_0
old_step_start = '''// 1. Zoom and Camera Bounds
if (mouse_wheel_up()) zoom_target = min(zoom_max, zoom_target + 0.10);
if (mouse_wheel_down()) zoom_target = max(zoom_min, zoom_target - 0.10);'''

new_step_start = '''// 0. Gihren's Greed Battlegroup Stack Drawer Animation
var _gw = display_get_gui_width();
stack_drawer_target_x = stack_drawer_open ? (_gw - stack_drawer_w) : (_gw - 28);
stack_drawer_x = lerp(stack_drawer_x, stack_drawer_target_x, 0.22);

// 1. Zoom and Camera Bounds
if (mouse_wheel_up()) zoom_target = min(zoom_max, zoom_target + 0.10);
if (mouse_wheel_down()) zoom_target = max(zoom_min, zoom_target - 0.10);'''

if old_step_start in text_step:
    text_step = text_step.replace(old_step_start, new_step_start)

# Add hotkeys for Drawer [D], Reorg [R], Split [S]
old_hotkeys = '''        if (keyboard_check_pressed(ord("F"))) cycle_unit_facing(units[selected_unit_idx]);
        if (keyboard_check_pressed(ord("M"))) { recalculate_moves(); state = COMBAT_STATE.MOVE_MODE; }'''

new_hotkeys = '''        if (keyboard_check_pressed(ord("F"))) cycle_unit_facing(units[selected_unit_idx]);
        if (keyboard_check_pressed(ord("D"))) { stack_drawer_open = !stack_drawer_open; scr_audio_play_ui("click"); }
        if (keyboard_check_pressed(ord("S"))) { split_mode_active = !split_mode_active; scr_audio_play_ui("click"); add_log("[SPLIT MODE] " + (split_mode_active ? "Select units in drawer to peel off." : "Disengaged.")); }
        if (keyboard_check_pressed(ord("R"))) { var _u_sel = units[selected_unit_idx]; if (_u_sel != undefined) reorganize_stack(_u_sel.grid_c, _u_sel.grid_r, _u_sel.team); }
        if (keyboard_check_pressed(ord("M"))) { recalculate_moves(); state = COMBAT_STATE.MOVE_MODE; }'''

if old_hotkeys in text_step:
    text_step = text_step.replace(old_hotkeys, new_hotkeys)

# Update MOVE_MODE to move full stack or split squad
old_move_code = '''        if (_click && !_hud_blocked && hover_c >= 0 && hover_c < grid_cols && hover_r >= 0 && hover_r < grid_rows) {
            var _cur_u = units[selected_unit_idx];
            for (var m = 0; m < array_length(valid_move_tiles); m++) {
                var _tile = valid_move_tiles[m];
                if (_tile.col == hover_c && _tile.row == hover_r) {
                    _cur_u.facing = iso_get_facing(_cur_u.grid_c, _cur_u.grid_r, hover_c, hover_r);
                    _cur_u.grid_c = hover_c;
                    _cur_u.grid_r = hover_r;
                    _cur_u.elev = grid_elev[hover_c][hover_r];
                    _cur_u.current_ap -= _tile.cost;
                    _cur_u.anim_state = (_cur_u.mech_type == "hyena") ? "walk" : ((_cur_u.mech_type == "aether") ? "boost" : "idle");
                    _cur_u.anim_timer = 20;
                    scr_audio_play_sfx((_cur_u.mech_type == "aether") ? snd_mech_boost : snd_mech_step, 0.85, 0.08);

                    add_log("[TACTICAL MOVE] " + _cur_u.callsign + " relocated to (" + string(hover_c) + ", " + string(hover_r) + ") [- " + string(_tile.cost) + " AP]");
                    state = COMBAT_STATE.PLAYER_PHASE;
                    exit;
                }
            }
        }'''

new_move_code = '''        if (_click && !_hud_blocked && hover_c >= 0 && hover_c < grid_cols && hover_r >= 0 && hover_r < grid_rows) {
            var _cur_u = units[selected_unit_idx];
            for (var m = 0; m < array_length(valid_move_tiles); m++) {
                var _tile = valid_move_tiles[m];
                if (_tile.col == hover_c && _tile.row == hover_r) {
                    var _moving_units = [];
                    if (split_mode_active) {
                        for (var u = 0; u < array_length(units); u++) {
                            var _chk = units[u];
                            if (!_chk.is_destroyed && _chk.grid_c == _cur_u.grid_c && _chk.grid_r == _cur_u.grid_r) {
                                if (variable_struct_exists(split_selected_units, _chk.id) && split_selected_units[$ _chk.id] == true) {
                                    array_push(_moving_units, _chk);
                                }
                            }
                        }
                        if (array_length(_moving_units) == 0) array_push(_moving_units, _cur_u);
                        split_mode_active = false;
                        split_selected_units = {};
                    } else {
                        _moving_units = get_stack_at_tile(_cur_u.grid_c, _cur_u.grid_r, _cur_u.team);
                        if (array_length(_moving_units) == 0) array_push(_moving_units, _cur_u);
                    }

                    for (var mu = 0; mu < array_length(_moving_units); mu++) {
                        var _mu_u = _moving_units[mu];
                        _mu_u.facing = iso_get_facing(_mu_u.grid_c, _mu_u.grid_r, hover_c, hover_r);
                        _mu_u.grid_c = hover_c;
                        _mu_u.grid_r = hover_r;
                        _mu_u.elev = grid_elev[hover_c][hover_r];
                        _mu_u.current_ap -= min(_mu_u.current_ap, _tile.cost);
                        _mu_u.anim_state = (_mu_u.mech_type == "hyena") ? "walk" : ((_mu_u.mech_type == "aether") ? "boost" : "idle");
                        _mu_u.anim_timer = 20;
                    }

                    scr_audio_play_sfx(snd_mech_step, 0.85, 0.08);
                    add_log("[TACTICAL MARCH] Battlegroup (" + string(array_length(_moving_units)) + " units) moved to (" + string(hover_c) + ", " + string(hover_r) + ") [- " + string(_tile.cost) + " AP]");
                    state = COMBAT_STATE.PLAYER_PHASE;
                    exit;
                }
            }
        }'''

if old_move_code in text_step:
    text_step = text_step.replace(old_move_code, new_move_code)

# Update TARGET_MODE to support Automated Maximum Firepower stack attack
old_target_code = '''                        if (_cur_u.current_ap >= _w.ap_cost) {
                            _cur_u.facing = iso_get_facing(_cur_u.grid_c, _cur_u.grid_r, _target.grid_c, _target.grid_r);
                            _cur_u.current_ap -= _w.ap_cost;
                            _cur_u.current_heat += _w.heat_cost;
                            _cur_u.anim_state = _w.anim_state;
                            _cur_u.anim_timer = 28;

                            var _recoil_dir = (_cur_u.facing == 0 || _cur_u.facing == 2) ? -12 : 12;
                            _cur_u.recoil_x = _recoil_dir;

                            spawn_combat_projectile(_cur_u, _target, _w);
                            add_log("[FIRING SALVO] " + _cur_u.callsign + " engaged " + _target.callsign + " with " + _w.name + "!");
                            state = COMBAT_STATE.ATTACK_EXECUTION;
                            exit;
                        } else {
                            add_log("[INSUFFICIENT AP] Need " + string(_w.ap_cost) + " AP to fire " + _w.short_name + "!");
                        }'''

new_target_code = '''                        // Gihren's Greed Automated Maximum Firepower for Stack
                        var _friendly_stack = get_stack_at_tile(_cur_u.grid_c, _cur_u.grid_r, _cur_u.team);
                        if (array_length(_friendly_stack) > 1) {
                            if (execute_stack_volley(_friendly_stack, _target, _dist)) {
                                exit;
                            }
                        } else {
                            if (_cur_u.current_ap >= _w.ap_cost) {
                                _cur_u.facing = iso_get_facing(_cur_u.grid_c, _cur_u.grid_r, _target.grid_c, _target.grid_r);
                                _cur_u.current_ap -= _w.ap_cost;
                                _cur_u.current_heat += _w.heat_cost;
                                _cur_u.anim_state = _w.anim_state;
                                _cur_u.anim_timer = 28;

                                var _recoil_dir = (_cur_u.facing == 0 || _cur_u.facing == 2) ? -12 : 12;
                                _cur_u.recoil_x = _recoil_dir;

                                spawn_combat_projectile(_cur_u, _target, _w);
                                add_log("[FIRING SALVO] " + _cur_u.callsign + " engaged " + _target.callsign + " with " + _w.name + "!");
                                state = COMBAT_STATE.ATTACK_EXECUTION;
                                exit;
                            } else {
                                add_log("[INSUFFICIENT AP] Need " + string(_w.ap_cost) + " AP to fire " + _w.short_name + "!");
                            }
                        }'''

if old_target_code in text_step:
    text_step = text_step.replace(old_target_code, new_target_code)

with open('objects/obj_BattleManager/Step_0.gml', 'w') as f:
    f.write(text_step)

print("Successfully updated Step_0.gml with Battlegroup Stack Movement & Automated Maximum Firepower!")
