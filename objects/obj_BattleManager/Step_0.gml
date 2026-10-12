/// @description obj_BattleManager Step Event
// Drives Turn-Based Tactical Combat State Machine, Pathfinding & Duel Resolution
// Strictly implements docs/05_tactical_combat.md

// 1. Shake & Timer Recovery
screen_shake = max(0.0, screen_shake - 0.7);

// Update Floating Combat Texts (docs/05)
for (var i = array_length(floating_texts) - 1; i >= 0; i--) {
    var _ft = floating_texts[i];
    _ft.y += _ft.vy;
    _ft.timer--;
    _ft.alpha = _ft.timer / 55.0;
    if (_ft.timer <= 0) {
        array_delete(floating_texts, i, 1);
    }
}

// 2. Smooth Visual Interpolation (Lerp to grid positions)
var _target_px = grid_to_world_x(player_unit.grid_c);
var _target_py = grid_to_world_y(player_unit.grid_r);
player_unit.visual_x = lerp(player_unit.visual_x, _target_px, 0.18);
player_unit.visual_y = lerp(player_unit.visual_y, _target_py, 0.18);

var _target_ex = grid_to_world_x(enemy_unit.grid_c);
var _target_ey = grid_to_world_y(enemy_unit.grid_r);
enemy_unit.visual_x = lerp(enemy_unit.visual_x, _target_ex, 0.18);
enemy_unit.visual_y = lerp(enemy_unit.visual_y, _target_ey, 0.18);

// 3. Physical Recoil Spring Dampening
player_unit.recoil_x = lerp(player_unit.recoil_x, 0, 0.12);
player_unit.recoil_y = lerp(player_unit.recoil_y, 0, 0.12);
player_unit.recoil_shake = max(0, player_unit.recoil_shake - 0.6);

enemy_unit.recoil_x = lerp(enemy_unit.recoil_x, 0, 0.12);
enemy_unit.recoil_y = lerp(enemy_unit.recoil_y, 0, 0.12);
enemy_unit.recoil_shake = max(0, enemy_unit.recoil_shake - 0.6);

// 4. Update Unit Action State Timers
if (player_unit.state_timer > 0) {
    player_unit.state_timer--;
    if (player_unit.state_timer <= 0) {
        player_unit.state = player_unit.components.legs.intact ? MS_STATE.IDLE : MS_STATE.CRIPPLED;
    }
}
if (enemy_unit.state_timer > 0) {
    enemy_unit.state_timer--;
    if (enemy_unit.state_timer <= 0) {
        enemy_unit.state = enemy_unit.components.legs.intact ? MS_STATE.IDLE : MS_STATE.CRIPPLED;
    }
}

// 5. Update Mouse Coordinates & Grid Hover
var _mx = device_mouse_x_to_gui(0);
var _my = device_mouse_y_to_gui(0);
var _click = mouse_check_button_pressed(mb_left);
var _rclick = mouse_check_button_pressed(mb_right);

hover_c = world_to_grid_c(_mx);
hover_r = world_to_grid_r(_my);

// =========================================================================
// 6. COMBAT STATE MACHINE
// =========================================================================
switch (state) {

    // ---------------------------------------------------------------------
    // A. MOVE MODE: Selecting destination cell on grid
    // ---------------------------------------------------------------------
    case COMBAT_STATE.MOVE_MODE:
        if (_rclick) {
            state = COMBAT_STATE.PLAYER_PHASE;
            exit;
        }

        if (_click && hover_c >= 0 && hover_c < grid_cols && hover_r >= 0 && hover_r < grid_rows) {
            // Check if hovered tile is in valid_move_tiles
            for (var m = 0; m < array_length(valid_move_tiles); m++) {
                var _tile = valid_move_tiles[m];
                if (_tile.col == hover_c && _tile.row == hover_r) {
                    player_unit.grid_c = _tile.col;
                    player_unit.grid_r = _tile.row;
                    player_unit.current_ap -= _tile.cost;
                    add_log("[TACTICAL MOVE] Warhammer relocated to (" + string(_tile.col) + ", " + string(_tile.row) + ") [- " + string(_tile.cost) + " AP]");
                    state = COMBAT_STATE.PLAYER_PHASE;
                    exit;
                }
            }
        }
        break;

    // ---------------------------------------------------------------------
    // B. TARGET MODE: Targeting enemy with active weapon
    // ---------------------------------------------------------------------
    case COMBAT_STATE.TARGET_MODE:
        if (_rclick) {
            state = COMBAT_STATE.PLAYER_PHASE;
            exit;
        }

        var _wpn = weapons[selected_weapon];
        var _dist = calculate_distance(player_unit.grid_c, player_unit.grid_r, enemy_unit.grid_c, enemy_unit.grid_r);
        var _in_range = (_dist >= _wpn.range_min && _dist <= _wpn.range_max);
        var _can_afford = (player_unit.current_ap >= _wpn.ap_cost);
        var _part_intact = player_unit.components[$ _wpn.req_part].intact;

        if (_click && hover_c == enemy_unit.grid_c && hover_r == enemy_unit.grid_r) {
            if (!_part_intact) {
                add_log("[ERROR] Cannot fire: Required mount (" + string(_wpn.req_part) + ") is DESTROYED!");
            } else if (!_can_afford) {
                add_log("[ERROR] Insufficient AP! (Requires " + string(_wpn.ap_cost) + " AP, Available: " + string(player_unit.current_ap) + ")");
            } else if (!_in_range) {
                add_log("[ERROR] Target out of weapon range! (Range: " + string(_wpn.range_min) + "-" + string(_wpn.range_max) + " cells)");
            } else {
                // Execute attack!
                player_unit.current_ap -= _wpn.ap_cost;
                player_unit.current_heat += _wpn.heat_cost;
                player_unit.state = _wpn.anim_state;
                player_unit.state_timer = 32;
                player_unit.recoil_x = -12 * player_unit.facing;
                screen_shake = 6.0;

                pending_attack.attacker = player_unit;
                pending_attack.defender = enemy_unit;
                pending_attack.weapon_index = selected_weapon;
                pending_attack.timer = 32;

                add_log("[ENGAGING TARGET] Firing " + _wpn.name + "!");
                state = COMBAT_STATE.ATTACK_EXECUTION;
            }
        }
        break;

    // ---------------------------------------------------------------------
    // C. ATTACK EXECUTION: Recoil, projectile impact, damage roll & part sever
    // ---------------------------------------------------------------------
    case COMBAT_STATE.ATTACK_EXECUTION:
        pending_attack.timer--;

        // Impact Frame (~halfway through animation)
        if (pending_attack.timer == 16) {
            var _atk = pending_attack.attacker;
            var _def = pending_attack.defender;
            var _w = weapons[pending_attack.weapon_index];
            var _d = calculate_distance(_atk.grid_c, _atk.grid_r, _def.grid_c, _def.grid_r);
            var _hit_pct = calculate_hit_chance(_atk, _def, _d);
            var _roll = random(100);

            if (_roll <= _hit_pct) {
                // HIT LANDS! Roll Front Mission localized component damage
                var _part_roll = random(100);
                var _hit_part = "torso";
                if (_part_roll < 40) _hit_part = "torso";
                else if (_part_roll < 60) _hit_part = "arm_left";
                else if (_part_roll < 80) _hit_part = "arm_right";
                else if (_part_roll < 95) _hit_part = "legs";
                else _hit_part = "head";

                var _comp = _def.components[$ _hit_part];
                _comp.cur = max(0, _comp.cur - _w.damage);

                // Defender Hit Reaction Physics
                _def.recoil_x = 18 * _atk.facing;
                _def.recoil_shake = 16;
                screen_shake = 12.0;

                add_log("[DIRECT IMPACT] " + string_upper(_hit_part) + " hit for " + string(_w.damage) + " damage!");

                // Floating Damage Readout
                add_floating_text(_def.visual_x, _def.visual_y - 40, "-" + string(_w.damage) + " [" + string_upper(_hit_part) + "]", c_yellow);

                // Check Component Destruction
                if (_comp.cur <= 0 && _comp.intact) {
                    _comp.intact = false;
                    add_log("[CRITICAL HIT] " + _def.callsign + " " + string_upper(_hit_part) + " SEVERED!");
                    add_floating_text(_def.visual_x, _def.visual_y - 65, "CRITICAL: " + string_upper(_hit_part) + " SEVERED!", c_red);

                    if (_hit_part == "torso") {
                        _def.is_destroyed = true;
                        _def.state = MS_STATE.DESTROYED;
                        screen_shake = 24.0;
                        add_log("[CATASTROPHIC BREACH] " + _def.callsign + " TORSO CORE BREACHED! UNIT DESTROYED!");

                        // Check Ejection Survival vs Permadeath if Player Mech (docs/05, 07)
                        if (_def.is_player && !casualty_data.pilot_ejected) {
                            casualty_data.pilot_ejected = true;
                            var _eject_roll = random(100);
                            var _eject_threshold = clamp(35 + (_def.evasion * 0.45), 25, 90);
                            if (_eject_roll < _eject_threshold) {
                                casualty_data.pilot_survived = true;
                                casualty_data.pilot_kia = false;
                                add_log("[EJECTION SYSTEM ENGAGED] Emergency escape thrusters cleared blast zone! Pilot survived.");
                                add_floating_text(_def.visual_x, _def.visual_y - 95, "COCKPIT EJECTED // PILOT SURVIVED", c_lime);
                            } else {
                                casualty_data.pilot_survived = false;
                                casualty_data.pilot_kia = true;
                                add_log("[FATAL CORE DETONATION] Escape hatch jammed! Pilot KIA confirmed.");
                                add_floating_text(_def.visual_x, _def.visual_y - 95, "FATAL DETONATION // PILOT KIA", c_red);
                            }
                        }
                    } else if (_hit_part == "legs") {
                        _def.state = MS_STATE.CRIPPLED;
                        add_log("[MOBILITY KILL] " + _def.callsign + " HYDRAULIC LEGS CRUSHED!");
                    }
                }
            } else {
                add_log("[MISS] Attack glancing deflection! No critical damage.");
            }
        }

        // Animation finishes
        if (pending_attack.timer <= 0) {
            if (enemy_unit.is_destroyed) {
                state = COMBAT_STATE.VICTORY_AAR;
                add_log("[MISSION ACCOMPLISHED] Tactical Sector Cleared! Reaver neutralized.");
            } else if (player_unit.is_destroyed) {
                state = COMBAT_STATE.DEFEAT_AAR;
                add_log("[UNIT LOST] Vanguard chassis destroyed in combat!");
            } else {
                // If player attacked, check if player has AP left
                if (pending_attack.attacker.is_player) {
                    state = COMBAT_STATE.PLAYER_PHASE;
                } else {
                    // Enemy finished turn, return to player
                    state = COMBAT_STATE.PLAYER_PHASE;
                }
            }
        }
        break;

    // ---------------------------------------------------------------------
    // D. AI PHASE: Hostile Syndicate Outlaw Turn
    // ---------------------------------------------------------------------
    case COMBAT_STATE.AI_PHASE:
        state_timer++;
        if (state_timer >= 35) {
            state_timer = 0;
            var _dist = calculate_distance(enemy_unit.grid_c, enemy_unit.grid_r, player_unit.grid_c, player_unit.grid_r);

            // 1. AI Movement: Step closer if outside favored engagement range
            if (_dist > 4 && enemy_unit.current_ap >= 2 && enemy_unit.components.legs.intact) {
                if (enemy_unit.grid_c > player_unit.grid_c + 2) {
                    enemy_unit.grid_c -= 2;
                    enemy_unit.current_ap -= 2;
                    add_log("[HOSTILE MANEUVER] Reaver closes distance along trench line!");
                }
            }

            // 2. AI Weapon Selection
            var _ai_wpn_idx = -1;
            if (enemy_unit.components.arm_left.intact && enemy_unit.current_ap >= 3 && _dist <= 6) {
                _ai_wpn_idx = 0; // Fire 120mm Autocannon
            } else if (enemy_unit.components.arm_right.intact && enemy_unit.current_ap >= 2 && _dist <= 4) {
                _ai_wpn_idx = 1; // Fire Vulcan
            }

            if (_ai_wpn_idx != -1) {
                var _ai_w = weapons[_ai_wpn_idx];
                enemy_unit.current_ap -= _ai_w.ap_cost;
                enemy_unit.current_heat += _ai_w.heat_cost;
                enemy_unit.state = _ai_w.anim_state;
                enemy_unit.state_timer = 32;
                enemy_unit.recoil_x = -12 * enemy_unit.facing;
                screen_shake = 6.0;

                pending_attack.attacker = enemy_unit;
                pending_attack.defender = player_unit;
                pending_attack.weapon_index = _ai_wpn_idx;
                pending_attack.timer = 32;

                add_log("[INCOMING FIRE] Reaver attacks with " + _ai_w.name + "!");
                state = COMBAT_STATE.ATTACK_EXECUTION;
            } else {
                // End AI Turn and start New Player Turn
                turn_number++;
                enemy_unit.current_ap = enemy_unit.max_ap;
                enemy_unit.current_heat = max(0, enemy_unit.current_heat - enemy_unit.heat_dissipation);

                // Refresh Player Turn
                player_unit.current_ap = player_unit.max_ap;
                player_unit.current_heat = max(0, player_unit.current_heat - player_unit.heat_dissipation);
                player_unit.braced = false;

                // Overheat Check for Player
                if (player_unit.current_heat > 100) {
                    player_unit.components.torso.cur = max(0, player_unit.components.torso.cur - 35);
                    player_unit.current_ap = max(2, player_unit.current_ap - 2);
                    screen_shake = 8.0;
                    add_log("[OVERHEAT WARNING] Core heat limit exceeded! -35 Torso HP, AP restricted!");
                }

                add_log("[TACTICAL TURN " + string(turn_number) + "] Player Initiative Refreshed (+6 AP)!");
                state = COMBAT_STATE.PLAYER_PHASE;
            }
        }
        break;
}

// 7. Global Keyboard Shortcuts in Battle
if (keyboard_check_pressed(vk_space) && state == COMBAT_STATE.PLAYER_PHASE) {
    // End Turn -> Pass to Enemy AI
    add_log("[TURN PASSED] Ending vanguard turn. Initiative passed to hostile forces.");
    state = COMBAT_STATE.AI_PHASE;
    state_timer = 0;
}
if (keyboard_check_pressed(ord("1"))) { selected_weapon = 0; state = COMBAT_STATE.TARGET_MODE; }
if (keyboard_check_pressed(ord("2"))) { selected_weapon = 1; state = COMBAT_STATE.TARGET_MODE; }
if (keyboard_check_pressed(ord("3"))) { selected_weapon = 2; state = COMBAT_STATE.TARGET_MODE; }
if (keyboard_check_pressed(ord("4"))) { selected_weapon = 3; state = COMBAT_STATE.TARGET_MODE; }
if (keyboard_check_pressed(ord("M"))) { recalculate_moves(); state = COMBAT_STATE.MOVE_MODE; }
