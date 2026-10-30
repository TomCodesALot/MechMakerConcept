// Prometheus Catalyst: Check maiden mobile suit sortie
if (instance_exists(obj_GameManager) && !obj_GameManager.first_mobile_suit_deployed) {
    if (array_length(units) > 0 && units[0].team == "ALLIED" && (!variable_struct_exists(units[0], "is_vehicle") || !units[0].is_vehicle)) {
        obj_GameManager.trigger_mobile_suit_revolution(units[0]);
    }
}

/// @description obj_BattleManager Step Event
// Drives Turn-Based Isometric Tactical Combat State Machine, Physical Projectile Simulation & Platoon AI
// Strictly implements docs/17_grand_scale_isometric_combat_system.md & docs/05_tactical_combat.md


// Modal Freeze: If Debug Menu is open, halt combat map inputs
if (instance_exists(obj_DebugManager) && obj_DebugManager.is_open) {
    exit;
}

// 1. Screen Shake & Dampening
screen_shake = max(0.0, screen_shake - 0.65);

// 2. Update Floating Combat Texts
for (var i = array_length(floating_texts) - 1; i >= 0; i--) {
    var _ft = floating_texts[i];
    _ft.y += _ft.vy;
    _ft.timer--;
    _ft.alpha = _ft.timer / 60.0;
    if (_ft.timer <= 0) {
        array_delete(floating_texts, i, 1);
    }
}

// 3. Update Combat Particle Explosions & Sparks
for (var i = array_length(combat_fx) - 1; i >= 0; i--) {
    var _fx = combat_fx[i];
    _fx.frame += _fx.speed;
    var _max_f = sprite_get_number(_fx.sprite);
    if (_fx.frame >= _max_f) {
        array_delete(combat_fx, i, 1);
    }
}

// 4. Update Physical Projectiles Trajectory Simulation
for (var i = array_length(projectiles) - 1; i >= 0; i--) {
    var _p = projectiles[i];
    _p.t += _p.step_rate;

    // Linear world interpolation
    _p.cur_x = lerp(_p.x1, _p.x2, _p.t);
    var _arc_y = (_p.z_peak * sin(pi * _p.t)) * zoom;
    _p.cur_y = lerp(_p.y1, _p.y2, _p.t) - _arc_y;

    // Update angle to match flight vector
    var _dx = _p.x2 - _p.x1;
    var _dy = (_p.y2 - _p.y1) - ((_p.z_peak * cos(pi * _p.t) * pi) * zoom);
    _p.angle = point_direction(0, 0, _dx, _dy);

    // Emit smoke / sparks along flight path
    if (_p.trail_type == "smoke" || _p.trail_type == "missile_plume") {
        if (irandom(2) == 0) {
            array_push(combat_fx, {
                sprite: spr_fx_spark,
                x: _p.cur_x + irandom_range(-3, 3),
                y: _p.cur_y + irandom_range(-3, 3),
                frame: 0.0,
                speed: 0.45,
                scale: 0.5 * zoom
            });
        }
    }

    // Impact Trigger
    if (_p.t >= 1.0) {
        _p.is_finished = true;
        if (is_callable(_p.on_hit)) {
            _p.on_hit();
        }
        array_delete(projectiles, i, 1);
    }
}

// 4b. Pre-Battle Deployment Deck Modal State Intercept
if (deployment_deck_active) {
    if (keyboard_check_pressed(vk_escape) || keyboard_check_pressed(ord("H"))) {
        deployment_deck_active = false;
        if (room_exists(rm_hq_terminal)) {
            room_goto(rm_hq_terminal);
            exit;
        }
    }
    // Update idle animations for units while paused
    for (var i = 0; i < array_length(units); i++) {
        var _u = units[i];
        _u.anim_frame += _u.anim_speed;
        if (_u.anim_frame >= 4.0) _u.anim_frame = 0.0;
    }
    exit;
}

// 4c. Global Retreat Shortcut to HQ Terminal (ESC / H or click on top-right button)
var _gui_mx = device_mouse_x_to_gui(0);
var _gui_my = device_mouse_y_to_gui(0);
var _retreat_clicked = (mouse_check_button_pressed(mb_left) && _gui_mx >= 1180 && _gui_mx <= 1350 && _gui_my >= 12 && _gui_my <= 48);
if (keyboard_check_pressed(vk_escape) || keyboard_check_pressed(ord("H")) || _retreat_clicked) {
    if (room_exists(rm_hq_terminal)) {
        room_goto(rm_hq_terminal);
        exit;
    }
}

// 5. Camera Navigation (WASD / Drag / Wheel Zoom)
var _pan_spd = 14.0 / max(0.5, zoom);
if (keyboard_check(ord("W")) || keyboard_check(vk_up)) cam_target_y += _pan_spd;
if (keyboard_check(ord("S")) || keyboard_check(vk_down)) cam_target_y -= _pan_spd;
if (keyboard_check(ord("A")) || keyboard_check(vk_left)) cam_target_x += _pan_spd;
if (keyboard_check(ord("D")) || keyboard_check(vk_right)) cam_target_x -= _pan_spd;

// Mouse Drag Navigation
var _raw_mx = mouse_x;
var _raw_my = mouse_y;
if (mouse_check_button_pressed(mb_middle) || (mouse_check_button_pressed(mb_right) && state == COMBAT_STATE.PLAYER_PHASE)) {
    is_dragging = true;
    drag_start_mx = _raw_mx;
    drag_start_my = _raw_my;
    drag_start_cam_x = cam_target_x;
    drag_start_cam_y = cam_target_y;
}
if (is_dragging) {
    cam_target_x = drag_start_cam_x + (_raw_mx - drag_start_mx);
    cam_target_y = drag_start_cam_y + (_raw_my - drag_start_my);
    if (!mouse_check_button(mb_middle) && !mouse_check_button(mb_right)) {
        is_dragging = false;
    }
}

// Mouse Wheel Zoom (Clamped 0.60x to 1.35x)
if (mouse_wheel_up()) zoom_target = clamp(zoom_target + 0.08, 0.60, 1.35);
if (mouse_wheel_down()) zoom_target = clamp(zoom_target - 0.08, 0.60, 1.35);

// Reset Camera Key [R]
if (keyboard_check_pressed(ord("R"))) {
    select_unit(selected_unit_idx);
}

// Camera Lerp
cam_x = lerp(cam_x, cam_target_x, 0.18);
cam_y = lerp(cam_y, cam_target_y, 0.18);
zoom = lerp(zoom, zoom_target, 0.18);

// 6. Unit Visual Position Lerp & Springs
for (var i = 0; i < array_length(units); i++) {
    var _u = units[i];
    var _target_sx = iso_to_screen_x(_u.grid_c, _u.grid_r, _u.elev, cam_x, cam_y, zoom);
    var _target_sy = iso_to_screen_y(_u.grid_c, _u.grid_r, _u.elev, cam_x, cam_y, zoom);

    // Gihren's Greed 6-Unit Tile Stacking Echelon Offset
    var _slot = 0;
    var _tile_stack = 0;
    for (var su = 0; su < array_length(units); su++) {
        var _tu = units[su];
        if (!_tu.is_destroyed && _tu.grid_c == _u.grid_c && _tu.grid_r == _u.grid_r) {
            if (su < i) _slot++;
            _tile_stack++;
        }
    }
    if (_tile_stack > 1) {
        var _offsets_x = [0, -14, 14, -20, 0, 20];
        var _offsets_y = [0, -8, -8, 6, 12, 6];
        var _s_idx = min(_slot, 5);
        _target_sx += _offsets_x[_s_idx] * zoom;
        _target_sy += _offsets_y[_s_idx] * zoom;
    }

    _u.visual_x = lerp(_u.visual_x, _target_sx, 0.20);
    _u.visual_y = lerp(_u.visual_y, _target_sy, 0.20);

    // Spring Recoil Dampening
    _u.recoil_x = lerp(_u.recoil_x, 0, 0.15);
    _u.recoil_y = lerp(_u.recoil_y, 0, 0.15);
    _u.recoil_shake = max(0, _u.recoil_shake - 0.5);

    // Animation Frame Progress
    _u.anim_frame += _u.anim_speed;

    // Action State Timer Countdown
    if (_u.anim_timer > 0) {
        _u.anim_timer--;
        if (_u.anim_timer <= 0) {
            if (!_u.is_destroyed) {
                _u.anim_state = "idle";
            }
        }
    }
}

// 7. Mouse Coordinates & Grid Unprojection
_gui_mx = device_mouse_x_to_gui(0);
_gui_my = device_mouse_y_to_gui(0);
var _click = mouse_check_button_pressed(mb_left);
var _rclick = mouse_check_button_pressed(mb_right);

hover_c = screen_to_iso_col(_raw_mx, _raw_my, cam_x, cam_y, zoom);
hover_r = screen_to_iso_row(_raw_mx, _raw_my, cam_x, cam_y, zoom);

// Check if mouse is hovering over interactive HUD regions
var _hud_blocked = (_gui_my > 570) || (_gui_mx > 930) || (_gui_my < 95);

// =========================================================================
// 8. COMBAT STATE MACHINE
// =========================================================================
switch (state) {

    // ---------------------------------------------------------------------
    // A. PLAYER PHASE: Commander Orders
    // ---------------------------------------------------------------------
    case COMBAT_STATE.PLAYER_PHASE:
        // Clicking units on the isometric battlefield (with Gihren's Greed Stack Cycling)
        if (_click && !_hud_blocked) {
            var _clicked_unit = false;
            var _tile_allies = [];
            for (var u = 0; u < array_length(units); u++) {
                var _chk = units[u];
                if (!_chk.is_destroyed && _chk.grid_c == hover_c && _chk.grid_r == hover_r && _chk.team == "ALLIED") {
                    array_push(_tile_allies, u);
                }
            }
            if (array_length(_tile_allies) > 1) {
                var _found_cur = -1;
                for (var ti = 0; ti < array_length(_tile_allies); ti++) {
                    if (_tile_allies[ti] == selected_unit_idx) { _found_cur = ti; break; }
                }
                var _next_u_idx = _tile_allies[(_found_cur + 1) % array_length(_tile_allies)];
                select_unit(_next_u_idx);
                add_log("[STACK CYCLE] Selected " + units[_next_u_idx].callsign + " [" + string((_found_cur + 1) % array_length(_tile_allies) + 1) + "/" + string(array_length(_tile_allies)) + " IN STACK]");
                _clicked_unit = true;
            } else {
                for (var u = 0; u < array_length(units); u++) {
                    var _chk = units[u];
                    if (!_chk.is_destroyed && _chk.grid_c == hover_c && _chk.grid_r == hover_r) {
                        if (_chk.team == "ALLIED") {
                            select_unit(u);
                            add_log("[UNIT SELECTED] Switched focus to " + _chk.callsign);
                            _clicked_unit = true;
                            break;
                        } else {
                            target_unit_idx = u;
                            add_log("[TARGET ACQUIRED] Diagnostics locked on " + _chk.callsign);
                            _clicked_unit = true;
                            break;
                        }
                    }
                }
            }
        }

        // Hotkeys
        if (keyboard_check_pressed(ord("H"))) { deployment_deck_active = !deployment_deck_active; }
        if (keyboard_check_pressed(vk_tab)) cycle_allied_unit();
        if (keyboard_check_pressed(ord("F"))) cycle_unit_facing(units[selected_unit_idx]);
        if (keyboard_check_pressed(ord("D"))) { stack_drawer_open = !stack_drawer_open; scr_audio_play_ui("click"); }
        if (keyboard_check_pressed(ord("S"))) { split_mode_active = !split_mode_active; scr_audio_play_ui("click"); add_log("[SPLIT MODE] " + (split_mode_active ? "Select units in drawer to peel off." : "Disengaged.")); }
        if (keyboard_check_pressed(ord("R"))) { var _u_sel = units[selected_unit_idx]; if (_u_sel != undefined) reorganize_stack(_u_sel.grid_c, _u_sel.grid_r, _u_sel.team); }
        if (keyboard_check_pressed(ord("M"))) { recalculate_moves(); state = COMBAT_STATE.MOVE_MODE; }
        if (keyboard_check_pressed(ord("1"))) { selected_weapon = 0; state = COMBAT_STATE.TARGET_MODE; }
        if (keyboard_check_pressed(ord("2"))) { selected_weapon = 1; state = COMBAT_STATE.TARGET_MODE; }
        if (keyboard_check_pressed(ord("3"))) { selected_weapon = 2; state = COMBAT_STATE.TARGET_MODE; }
        if (keyboard_check_pressed(ord("4"))) { selected_weapon = 3; state = COMBAT_STATE.TARGET_MODE; }
        if (keyboard_check_pressed(ord("N")) && state == COMBAT_STATE.PLAYER_PHASE) {
            if (evaluate_nemesis_incursion()) {
                state = COMBAT_STATE.NEMESIS_INCURSION;
                nemesis_incursion_state = 0;
                nemesis_incursion_timer = 0;
                add_log("[MANUAL TRIGGER] Nemesis incursion drop-pod dispatched!");
            }
        }
        if (keyboard_check_pressed(ord("B"))) {
            var _cur_u = units[selected_unit_idx];
            if (_cur_u.current_ap >= 2) {
                _cur_u.current_ap -= 2;
                _cur_u.braced = true;
                _cur_u.current_heat = max(0, _cur_u.current_heat - 25);
                add_log("[TACTICAL DEFENSE] " + _cur_u.callsign + " braced! +35% Evasion, -25% Heat vented.");
            }
        }
        if (keyboard_check_pressed(vk_space)) {
            add_log("[TURN PASSED] Initiative passed to hostile battlegroup.");
            state = COMBAT_STATE.AI_PHASE;
            ai_action_timer = 0;
            ai_unit_index = 0;
        }
        if (keyboard_check_pressed(ord("A"))) {
            auto_combat_enabled = !auto_combat_enabled;
            if (auto_combat_enabled) state = COMBAT_STATE.AUTO_SIM;
            add_log("[AUTO-COMBAT] Autonomous Battle Simulation: " + (auto_combat_enabled ? "ENGAGED" : "DISENGAGED"));
        }
        // Goal G: Flagship Orbital Strike Hotkey [O]
        if (keyboard_check_pressed(ord("O"))) {
            var _tx = (target_unit_idx >= 0 && target_unit_idx < array_length(units)) ? units[target_unit_idx].grid_c : 11;
            var _ty = (target_unit_idx >= 0 && target_unit_idx < array_length(units)) ? units[target_unit_idx].grid_r : 11;
            call_flagship_orbital_strike(_tx, _ty);
        }
        break;

    // ---------------------------------------------------------------------
    // B. MOVE MODE: Selecting Destination Tile on Isometric Grid
    // ---------------------------------------------------------------------
    case COMBAT_STATE.MOVE_MODE:
        if (_rclick) {
            // Milestone 55: Mid-Battle Tactical Radio Incursion
                if (turn_number >= mid_battle_incursion_turn && !mid_battle_incursion_triggered) {
                    trigger_mid_battle_tactical_incursion();
                }

                state = COMBAT_STATE.PLAYER_PHASE;
            exit;
        }

        if (_click && !_hud_blocked && hover_c >= 0 && hover_c < grid_cols && hover_r >= 0 && hover_r < grid_rows) {
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
        }
        break;

    // ---------------------------------------------------------------------
    // C. TARGET MODE: Selecting Enemy Target Within Weapon Range
    // ---------------------------------------------------------------------
    case COMBAT_STATE.TARGET_MODE:
        if (_rclick || keyboard_check_pressed(vk_escape)) {
            state = COMBAT_STATE.PLAYER_PHASE;
            exit;
        }

        var _cur_u = units[selected_unit_idx];

        // Aimed Shot Hotkeys: [Z] Toggle Aimed Shot, [T] Cycle Targeted Limb
        if (keyboard_check_pressed(ord("Z"))) {
            _cur_u.is_aimed_shot = !_cur_u.is_aimed_shot;
            add_log("[AIMED SHOT] " + (_cur_u.is_aimed_shot ? ("Precision lock: " + string_upper(_cur_u.targeted_limb)) : "Auto scatter mode."));
        }
        if (keyboard_check_pressed(ord("T"))) {
            var _parts = ["torso", "arm_left", "arm_right", "legs", "head"];
            var _p_idx = 0;
            for (var p = 0; p < array_length(_parts); p++) {
                if (_parts[p] == _cur_u.targeted_limb) { _p_idx = (p + 1) % array_length(_parts); break; }
            }
            _cur_u.targeted_limb = _parts[_p_idx];
            _cur_u.is_aimed_shot = true;
            add_log("[AIMED SHOT LOCK] Designated component -> " + string_upper(_cur_u.targeted_limb));
        }

        // Auto-update target_unit_idx when hovering over enemy
        for (var u = 0; u < array_length(units); u++) {
            var _target = units[u];
            if (_target.team == "HOSTILE" && !_target.is_destroyed && _target.grid_c == hover_c && _target.grid_r == hover_r) {
                target_unit_idx = u;
                break;
            }
        }

        if (_click && !_hud_blocked) {
            _cur_u = units[selected_unit_idx];
            if (selected_weapon >= array_length(_cur_u.weapons)) exit;
            var _w = _cur_u.weapons[selected_weapon];

            for (var u = 0; u < array_length(units); u++) {
                var _target = units[u];
                if (_target.team == "HOSTILE" && !_target.is_destroyed && _target.grid_c == hover_c && _target.grid_r == hover_r) {
                    var _dist = calculate_distance(_cur_u.grid_c, _cur_u.grid_r, _target.grid_c, _target.grid_r);

                    var _eff_max_w_range = _w.range_max + max(0, _cur_u.elev - _target.elev);
                    if (_dist >= _w.range_min && _dist <= _eff_max_w_range) {
                        // Prevent ground melee units from engaging high-altitude airborne targets
                        if (_w.proj_type == "MELEE" && ((variable_struct_exists(_target, "is_aircraft") && _target.is_aircraft) || variable_struct_get(_target, "move_type") == "aero") && (!variable_struct_exists(_cur_u, "is_aircraft") || !_cur_u.is_aircraft)) {
                            add_log("[INVALID VECTOR] Airborne aircraft cannot be engaged with surface melee!");
                            scr_audio_play_ui("cancel");
                            exit;
                        }

                        // Gihren's Greed Automated Maximum Firepower for Stack
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

                                if (cinematic_combat_enabled) {
                                    start_battle_cinematic(_cur_u, _target, _w, COMBAT_STATE.PLAYER_PHASE);
                                } else {
                                    spawn_combat_projectile(_cur_u, _target, _w);
                                }
                                add_log("[FIRING SALVO] " + _cur_u.callsign + " engaged " + _target.callsign + " with " + _w.name + "!");
                                state = COMBAT_STATE.ATTACK_EXECUTION;
                                exit;
                            } else {
                                add_log("[INSUFFICIENT AP] Need " + string(_w.ap_cost) + " AP to fire " + _w.short_name + "!");
                            }
                        }
                    }
                }
            }
        }
        break;

    // ---------------------------------------------------------------------
    // D. ATTACK EXECUTION: Waiting for In-Flight Projectiles to Resolve
    // ---------------------------------------------------------------------
    case COMBAT_STATE.ATTACK_EXECUTION:
        if (battle_cinematic.active) {
            update_battle_cinematic();
            exit;
        }

        if (array_length(projectiles) == 0) {
            // Check Victory Condition (All Hostile Units Destroyed)
            var _any_hostile = false;
            for (var u = 0; u < array_length(units); u++) {
                if (units[u].team == "HOSTILE" && !units[u].is_destroyed) {
                    _any_hostile = true;
                    break;
                }
            }
            if (!_any_hostile) {
                state = COMBAT_STATE.VICTORY_AAR;
                scr_audio_play_location_bgm("victory");
                add_log("[SECTOR SECURED] ALL HOSTILE FORCES NEUTRALIZED! Mission accomplished.");

                // Milestone 56: Check surviving pilots with high fatigue (>= 50) for Ghost of Phobos
                if (instance_exists(obj_GameManager) && variable_struct_exists(obj_GameManager.facilities, "roster_pilots")) {
                    for (var u = 0; u < array_length(units); u++) {
                        var _un = units[u];
                        if (_un.team == "ALLIED" && !_un.is_destroyed) {
                            if (variable_struct_exists(_un, "fatigue") && _un.fatigue >= 50) {
                                for (var p = 0; p < array_length(obj_GameManager.facilities.roster_pilots); p++) {
                                    var _plt = obj_GameManager.facilities.roster_pilots[p];
                                    if (_plt.name == _un.pilot_name || string_pos(_un.pilot_name, _plt.name) > 0) {
                                        obj_GameManager.mutate_pilot_trait(p, "Ghost of Phobos");
                                        break;
                                    }
                                }
                            }
                        }
                    }
                }
                exit;
            }

            // Check Defeat Condition (All Allied Units Destroyed)
            var _any_allied = false;
            for (var u = 0; u < array_length(units); u++) {
                if (units[u].team == "ALLIED" && !units[u].is_destroyed) {
                    _any_allied = true;
                    break;
                }
            }
            if (!_any_allied) {
                state = COMBAT_STATE.DEFEAT_AAR;
                scr_audio_play_location_bgm("defeat");
                add_log("[CRITICAL FAILURE] ALL ALLIED MOBILE SUITS DESTROYED!");
                exit;
            }

            // Return to prior phase
            if (auto_combat_enabled) {
                state = COMBAT_STATE.AUTO_SIM;
            } else if (state_timer > 0) {
                state = COMBAT_STATE.AI_PHASE;
            } else {
                state = COMBAT_STATE.PLAYER_PHASE;
            }
        }
        break;

    // ---------------------------------------------------------------------
    // E. AI PHASE: Hostile Syndicate Battlegroup Sequencing
    // ---------------------------------------------------------------------
    case COMBAT_STATE.AI_PHASE:
        ai_action_timer++;
        if (ai_action_timer >= 28) {
            ai_action_timer = 0;

            // Find next active hostile unit with actions
            var _found_actor = false;
            while (ai_unit_index < array_length(units)) {
                var _ai_u = units[ai_unit_index];
                if (_ai_u.team == "HOSTILE" && !_ai_u.is_destroyed && _ai_u.current_ap >= 2) {
                    _found_actor = true;
                    break;
                }
                ai_unit_index++;
            }

            if (_found_actor) {
                var _ai_u = units[ai_unit_index];

                // Find closest living allied unit (or Nemesis Priority Target)
                var _best_target = undefined;
                var _best_dist = 999;

                // Nemesis Threat Priority Override (Document 19)
                if (variable_struct_get(_ai_u, "is_nemesis") == true) {
                    for (var u = 0; u < array_length(units); u++) {
                        if (units[u].id == _ai_u.nemesis_target_id && !units[u].is_destroyed) {
                            _best_target = units[u];
                            _best_dist = calculate_distance(_ai_u.grid_c, _ai_u.grid_r, units[u].grid_c, units[u].grid_r);
                            break;
                        }
                    }
                }

                // Goal F: Platoon Role AI Specialization
                var _max_w_range = 1;
                var _has_melee = false;
                for (var w = 0; w < array_length(_ai_u.weapons); w++) {
                    if (_ai_u.weapons[w].range_max > _max_w_range) _max_w_range = _ai_u.weapons[w].range_max;
                    if (_ai_u.weapons[w].proj_type == "MELEE") _has_melee = true;
                }
                var _ai_role = "VANGUARD";
                if (_max_w_range >= 5 || _ai_u.mech_type == "siegebreaker") _ai_role = "SNIPER";
                else if (_has_melee || _max_w_range <= 2 || _ai_u.mech_type == "muramasa") _ai_role = "FLANKER";

                if (_best_target == undefined) {
                    // Vanguard AI prioritizes units already under fire to crossfire suppress
                    if (_ai_role == "VANGUARD") {
                        for (var u = 0; u < array_length(units); u++) {
                            var _allied_chk = units[u];
                            if (_allied_chk.team == "ALLIED" && !_allied_chk.is_destroyed && variable_struct_exists(_allied_chk, "hits_taken_this_turn") && _allied_chk.hits_taken_this_turn > 0) {
                                var _d = calculate_distance(_ai_u.grid_c, _ai_u.grid_r, _allied_chk.grid_c, _allied_chk.grid_r);
                                if (_d < _best_dist) {
                                    _best_dist = _d;
                                    _best_target = _allied_chk;
                                }
                            }
                        }
                    }

                    if (_best_target == undefined) {
                        for (var u = 0; u < array_length(units); u++) {
                            var _allied_chk = units[u];
                            if (_allied_chk.team == "ALLIED" && !_allied_chk.is_destroyed) {
                                var _d = calculate_distance(_ai_u.grid_c, _ai_u.grid_r, _allied_chk.grid_c, _allied_chk.grid_r);
                                if (_d < _best_dist) {
                                    _best_dist = _d;
                                    _best_target = _allied_chk;
                                }
                            }
                        }
                    }
                }

                if (_best_target != undefined) {
                    // Try to fire weapon
                    var _fired = false;
                    for (var w = 0; w < array_length(_ai_u.weapons); w++) {
                        var _ai_w = _ai_u.weapons[w];
                        var _ai_eff_max_range = _ai_w.range_max + max(0, _ai_u.elev - _best_target.elev);
                        if (_best_dist >= _ai_w.range_min && _best_dist <= _ai_eff_max_range && _ai_u.current_ap >= _ai_w.ap_cost) {
                            _ai_u.facing = iso_get_facing(_ai_u.grid_c, _ai_u.grid_r, _best_target.grid_c, _best_target.grid_r);
                            _ai_u.current_ap -= _ai_w.ap_cost;
                            _ai_u.current_heat += _ai_w.heat_cost;
                            _ai_u.anim_state = _ai_w.anim_state;
                            _ai_u.anim_timer = 28;
                            _ai_u.recoil_x = (_ai_u.facing == 0 || _ai_u.facing == 2) ? -12 : 12;

                            spawn_combat_projectile(_ai_u, _best_target, _ai_w);
                            add_log("[HOSTILE ENGAGEMENT] " + _ai_u.callsign + " fires " + _ai_w.name + " at " + _best_target.callsign + "!");
                            state = COMBAT_STATE.ATTACK_EXECUTION;
                            state_timer = 1;
                            _fired = true;
                            break;
                        }
                    }

                    // If couldn't fire, advance closer
                    if (!_fired && _ai_u.current_ap >= 2 && _ai_u.components.legs.intact) {
                        var _step_c = sign(_best_target.grid_c - _ai_u.grid_c);
                        var _step_r = sign(_best_target.grid_r - _ai_u.grid_r);

                        // Candidate moves: diagonal first, then horizontal, then vertical
                        var _cand_steps = [
                            [_ai_u.grid_c + _step_c, _ai_u.grid_r + _step_r],
                            [_ai_u.grid_c + _step_c, _ai_u.grid_r],
                            [_ai_u.grid_c, _ai_u.grid_r + _step_r]
                        ];

                        for (var s = 0; s < array_length(_cand_steps); s++) {
                            var _nc = clamp(_cand_steps[s][0], 0, grid_cols - 1);
                            var _nr = clamp(_cand_steps[s][1], 0, grid_rows - 1);
                            if (_nc == _ai_u.grid_c && _nr == _ai_u.grid_r) continue;

                            // Check tile occupancy (allow friendly stack up to 6, block enemies)
                            var _is_occ = false;
                            var _ai_stack_cnt = 0;
                            for (var ou = 0; ou < array_length(units); ou++) {
                                var _ou_chk = units[ou];
                                if (!_ou_chk.is_destroyed && _ou_chk != _ai_u && _ou_chk.grid_c == _nc && _ou_chk.grid_r == _nr) {
                                    if (_ou_chk.team != _ai_u.team) {
                                        _is_occ = true;
                                        break;
                                    } else {
                                        _ai_stack_cnt++;
                                    }
                                }
                            }
                            if (_is_occ || _ai_stack_cnt >= 6) continue;

                            // Check movement cost and passability across terrain
                            var _m_cost = get_terrain_move_cost(_ai_u, _ai_u.grid_c, _ai_u.grid_r, _nc, _nr);
                            if (_m_cost < 999 && abs(grid_elev[_nc][_nr] - _ai_u.elev) <= 1) {
                                _ai_u.facing = iso_get_facing(_ai_u.grid_c, _ai_u.grid_r, _nc, _nr);
                                _ai_u.grid_c = _nc;
                                _ai_u.grid_r = _nr;
                                _ai_u.elev = grid_elev[_nc][_nr];
                                _ai_u.current_ap -= min(_ai_u.current_ap, max(1, _m_cost));
                                add_log("[HOSTILE ADVANCE] " + _ai_u.callsign + " maneuvers across terrain!");
                                scr_audio_play_sfx(snd_mech_step, 0.75, 0.10);
                                break;
                            }
                        }
                    }
                }

                ai_unit_index++;
            } else {
                // Hostile Phase Complete -> Refresh Next Turn
                turn_number++;
                for (var u = 0; u < array_length(units); u++) {
                    var _u = units[u];
                    _u.current_ap = _u.max_ap;
                    _u.current_heat = max(0, _u.current_heat - _u.heat_dissipation);
                    _u.braced = false;
                    _u.hits_taken_this_turn = 0;

                    // Goal F: Crossfire Suppression Recovery
                    if (variable_struct_exists(_u, "is_suppressed") && _u.is_suppressed) {
                        _u.current_ap = max(1, _u.current_ap - 2);
                        _u.is_suppressed = false;
                        add_log("[PINNED RECOVERY] " + _u.callsign + " pinned down (-2 AP applied)!");
                    }

                    // Goal G: Boss Regenerative Phase Barrier Recharge
                    if (variable_struct_exists(_u, "is_apex_boss") && _u.is_apex_boss && !_u.is_destroyed) {
                        if (variable_struct_exists(_u.components, "backpack") && _u.components.backpack.intact) {
                            _u.barrier_cur = min(_u.barrier_max, _u.barrier_cur + _u.barrier_regen);
                            add_log("[BARRIER RECHARGE] Ouroboros Prime regenerated +" + string(_u.barrier_regen) + " Phase Barrier!");
                        }
                    }
                }

                ai_unit_index = 0;
                state_timer = 0;
                select_unit(0);
                add_log("[INITIATIVE RESET // TURN " + string(turn_number) + "] Player Platoon Initiative Restored (+AP)!");

                // Check Procedural Nemesis Drop-Pod Ambush Incursion (Document 19)
                if (turn_number >= nemesis_incursion_turn && !nemesis_incursion_checked) {
                    nemesis_incursion_checked = true;
                    if (evaluate_nemesis_incursion()) {
                        state = COMBAT_STATE.NEMESIS_INCURSION;
                        nemesis_incursion_state = 0;
                        nemesis_incursion_timer = 0;
                        exit;
                    }
                }

                state = COMBAT_STATE.PLAYER_PHASE;
            }
        }
        break;

    // ---------------------------------------------------------------------
    // E2. NEMESIS INCURSION: Atmospheric Drop-Pod Descent & Comms Bark (Document 19)
    // ---------------------------------------------------------------------
    case COMBAT_STATE.NEMESIS_INCURSION:
        nemesis_incursion_timer++;

        // Substate 0: Warning Siren & Camera Pan (Frames 0 to 50)
        if (nemesis_incursion_state == 0) {
            if (nemesis_incursion_timer == 1) {
                scr_audio_play_sfx(snd_alarm_critical, 1.0, 0.0);
                scr_audio_play_location_bgm("nemesis");
            }
            screen_shake = max(screen_shake, 3.5);
            var _t_c = incursion_data.target_c;
            var _t_r = incursion_data.target_r;
            cam_target_x = -(iso_to_screen_x(_t_c, _t_r, 0, 0, 0, 1.0) - 1366 * 0.5);
            cam_target_y = -(iso_to_screen_y(_t_c, _t_r, 0, 0, 0, 1.0) - 768 * 0.5);

            if (nemesis_incursion_timer >= 50) {
                nemesis_incursion_state = 1;
                nemesis_incursion_timer = 0;
            }
        }
        // Substate 1: Atmospheric Descent Streak (Frames 51 to 120)
        else if (nemesis_incursion_state == 1) {
            incursion_data.pod_altitude = max(0, incursion_data.pod_altitude - 11.0);
            screen_shake = max(screen_shake, 6.0 + (1.0 - (incursion_data.pod_altitude / 650.0)) * 8.0);

            // Reentry plasma particles
            var _tc = incursion_data.target_c;
            var _tr = incursion_data.target_r;
            var _tx = iso_to_screen_x(_tc, _tr, 0, cam_x, cam_y, zoom);
            var _ty = iso_to_screen_y(_tc, _tr, 0, cam_x, cam_y, zoom) - incursion_data.pod_altitude * zoom;

            array_push(combat_fx, {
                sprite: spr_fx_spark,
                x: _tx + irandom_range(-15, 15),
                y: _ty + irandom_range(-10, 10),
                frame: 0.0,
                speed: 0.4,
                scale: 1.5 * zoom
            });

            if (incursion_data.pod_altitude <= 0) {
                nemesis_incursion_state = 2;
                nemesis_incursion_timer = 0;
            }
        }
        // Substate 2: Impact Detonation & Unit Insertion (Frames 121 to 170)
        else if (nemesis_incursion_state == 2) {
            if (!incursion_data.impact_fx_played) {
                incursion_data.impact_fx_played = true;
                screen_shake = 26.0;
                scr_audio_play_sfx(snd_explosion_large, 1.0, 0.05);
                scr_audio_play_impact("kinetic", true);

                var _tc = incursion_data.target_c;
                var _tr = incursion_data.target_r;
                var _tx = iso_to_screen_x(_tc, _tr, 0, cam_x, cam_y, zoom);
                var _ty = iso_to_screen_y(_tc, _tr, 0, cam_x, cam_y, zoom);

                // Spawn explosion blast ring
                for (var ex = 0; ex < 6; ex++) {
                    var _ang = ex * (360.0 / 6.0);
                    array_push(combat_fx, {
                        sprite: spr_fx_explosion,
                        x: _tx + lengthdir_x(25.0 * zoom, _ang),
                        y: _ty + lengthdir_y(15.0 * zoom, _ang),
                        frame: 0.0,
                        speed: 0.35,
                        scale: 1.6 * zoom
                    });
                }

                add_floating_text(_tx, _ty - 70, "ORBITAL IMPACT // NEMESIS INVASION", c_red);
                add_log("[DROP-POD IMPACT] Atmospheric breach confirmed at Grid (" + string(_tc) + ", " + string(_tr) + ")!");

                // Stagger adjacent units
                for (var u = 0; u < array_length(units); u++) {
                    var _adj_u = units[u];
                    if (!_adj_u.is_destroyed) {
                        var _dist = calculate_distance(_tc, _tr, _adj_u.grid_c, _adj_u.grid_r);
                        if (_dist <= 1) {
                            _adj_u.components.torso.cur = max(10, _adj_u.components.torso.cur - 40);
                            add_log("[SHOCKWAVE] " + _adj_u.callsign + " suffered -40 Kinetic Shock damage from drop-pod impact!");
                        }
                    }
                }

                // Spawn Nemesis Mobile Suit into units array
                var _type = "hyena";
                if (string_pos("GHA", incursion_data.preferred_chassis) > 0 || string_pos("ironclad", incursion_data.preferred_chassis) > 0) _type = "ironclad";
                else if (string_pos("AET", incursion_data.preferred_chassis) > 0 || string_pos("aether", incursion_data.preferred_chassis) > 0) _type = "aether";
                else if (string_pos("MUR", incursion_data.preferred_chassis) > 0 || string_pos("muramasa", incursion_data.preferred_chassis) > 0) _type = "muramasa";

                var _nem_u = {
                    id: "NEMESIS_" + incursion_data.nemesis_id,
                    callsign: incursion_data.callsign + " [NEMESIS]",
                    pilot_name: incursion_data.nemesis_name,
                    team: "HOSTILE",
                    is_nemesis: true,
                    nemesis_target_id: "ALLIED_0",
                    mech_type: _type,
                    grid_c: _tc,
                    grid_r: _tr,
                    elev: grid_elev[_tc][_tr],
                    visual_x: 0,
                    visual_y: 0,
                    facing: 0,
                    max_ap: 8,
                    current_ap: 8,
                    current_heat: 0.0,
                    max_heat: 120.0,
                    heat_dissipation: 45.0,
                    accuracy: 94,
                    evasion: 55,
                    braced: false,
                    components: create_components(850, 520, 680, 240, 310, 36),
                    weapons: [
                        { name: "Nemesis Overcharged Cannon", short_name: "120MM SABOT", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 16, range_min: 1, range_max: 7, damage: 220, anim_state: "fire_rifle", desc: "Overcharged sabot with explosive breach." },
                        { name: "Blood-Feud Heavy Vulcan", short_name: "HEAVY VULCAN", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 4, damage: 115, anim_state: "fire_chaingun", desc: "Sustained kinetic barrage." },
                        { name: "Vengeance Micro-Missile Pod", short_name: "SWARM MISSILES", proj_type: "MICRO_MISSILE", ap_cost: 4, heat_cost: 24, range_min: 2, range_max: 7, damage: 240, anim_state: "fire_missiles", desc: "Saturation cluster." },
                        { name: "Hydraulic Breaching Claw", short_name: "CRUSHER CLAW", proj_type: "MELEE", ap_cost: 3, heat_cost: 12, range_min: 1, range_max: 1, damage: 280, anim_state: "melee", desc: "Savage close-quarters armor peel." }
                    ],
                    anim_state: "idle",
                    anim_timer: 0,
                    anim_frame: 0.0,
                    anim_speed: 0.18,
                    recoil_x: 0,
                    recoil_y: 0,
                    recoil_shake: 0,
                    image_blend: make_color_rgb(255, 90, 80),
                    is_destroyed: false
                };

                array_push(units, _nem_u);
            }

            if (nemesis_incursion_timer >= 50) {
                nemesis_incursion_state = 3;
                nemesis_incursion_timer = 0;
            }
        }
        // Substate 3: Comms Intercom Bark Window (Interactive Dismiss)
        else if (nemesis_incursion_state == 3) {
            _click = mouse_check_button_pressed(mb_left);
            var _space = keyboard_check_pressed(vk_space);
            if (_click || _space || nemesis_incursion_timer >= 300) {
                nemesis_incursion_state = 4;
            }
        }
        // Substate 4: Insertion Complete -> Return to Combat
        else if (nemesis_incursion_state == 4) {
            add_log("[NEMESIS ENGAGED] " + incursion_data.nemesis_name + " has locked combat targeting onto player vanguard!");
            state = COMBAT_STATE.PLAYER_PHASE;
            nemesis_incursion_state = 0;
            nemesis_incursion_timer = 0;
            select_unit(0);
        }
        break;

    // ---------------------------------------------------------------------
    // F. AUTO SIMULATION: Autonomous Test Salvos Between Battlegroups
    // ---------------------------------------------------------------------
    case COMBAT_STATE.AUTO_SIM:
        auto_combat_timer++;
        if (auto_combat_timer >= 35) {
            auto_combat_timer = 0;

            // Pick random living allied unit
            var _living_allies = [];
            for (var u = 0; u < array_length(units); u++) if (units[u].team == "ALLIED" && !units[u].is_destroyed) array_push(_living_allies, units[u]);

            // Pick random living hostile unit
            var _living_hostiles = [];
            for (var u = 0; u < array_length(units); u++) if (units[u].team == "HOSTILE" && !units[u].is_destroyed) array_push(_living_hostiles, units[u]);

            if (array_length(_living_allies) > 0 && array_length(_living_hostiles) > 0) {
                var _a_unit = _living_allies[irandom(array_length(_living_allies) - 1)];
                var _h_unit = _living_hostiles[irandom(array_length(_living_hostiles) - 1)];

                // 50% chance ally attacks hostile, 50% chance hostile attacks ally
                if (irandom(1) == 0) {
                    var _w = _a_unit.weapons[irandom(array_length(_a_unit.weapons) - 1)];
                    _a_unit.facing = iso_get_facing(_a_unit.grid_c, _a_unit.grid_r, _h_unit.grid_c, _h_unit.grid_r);
                    _a_unit.anim_state = _w.anim_state;
                    _a_unit.anim_timer = 28;
                    spawn_combat_projectile(_a_unit, _h_unit, _w);
                    state = COMBAT_STATE.ATTACK_EXECUTION;
                } else {
                    var _w = _h_unit.weapons[irandom(array_length(_h_unit.weapons) - 1)];
                    _h_unit.facing = iso_get_facing(_h_unit.grid_c, _h_unit.grid_r, _a_unit.grid_c, _a_unit.grid_r);
                    _h_unit.anim_state = _w.anim_state;
                    _h_unit.anim_timer = 28;
                    spawn_combat_projectile(_h_unit, _a_unit, _w);
                    state = COMBAT_STATE.ATTACK_EXECUTION;
                }
            }
        }
        break;
}

// Combat Audio & Settings Shortcuts
if (keyboard_check_pressed(ord("C"))) {
    cinematic_combat_enabled = !cinematic_combat_enabled;
    scr_audio_play_ui("confirm");
    if (instance_exists(obj_GameManager)) {
        obj_GameManager.show_toast(cinematic_combat_enabled ? "[GIHREN DUELS: ON]" : "[GIHREN DUELS: OFF]", cinematic_combat_enabled ? c_lime : c_orange);
    }
    add_log("[CONFIG] Cinematic Duel Cutscenes set to: " + (cinematic_combat_enabled ? "ON" : "OFF"));
}

if (keyboard_check_pressed(ord("M"))) {
    var _now_muted = scr_audio_toggle_mute();
    if (instance_exists(obj_GameManager)) {
        obj_GameManager.show_toast(_now_muted ? "[AUDIO MUTED]" : "[AUDIO UNMUTED - " + string(floor(scr_audio_get_master_volume() * 100)) + "%]", _now_muted ? c_orange : c_lime);
    }
}
if (keyboard_check_pressed(ord("O"))) {
    show_settings_modal = !show_settings_modal;
    scr_audio_play_ui("click");
}
if (keyboard_check_pressed(vk_escape)) {
    if (show_settings_modal) {
        show_settings_modal = false;
        scr_audio_play_ui("cancel");
    }
}
