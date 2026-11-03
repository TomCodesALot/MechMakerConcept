# Patch Create_0.gml to support 6-unit battlegroup stacks in Battle Cinematic
with open('objects/obj_BattleManager/Create_0.gml', 'r') as f_in:
    content = f_in.read()

# 1. Update start_battle_cinematic signature and assignments
old_sig = 'start_battle_cinematic = function(_atk, _def, _wpn, _return_state = COMBAT_STATE.PLAYER_PHASE) {'
new_sig = 'start_battle_cinematic = function(_atk, _def, _wpn, _return_state = COMBAT_STATE.PLAYER_PHASE, _atk_stack_override = undefined, _def_stack_override = undefined) {'
assert old_sig in content, 'start_battle_cinematic signature not found'
content = content.replace(old_sig, new_sig, 1)

old_assign = """    battle_cinematic.attacker = _atk;
    battle_cinematic.defender = _def;"""

new_assign = """    battle_cinematic.attacker = _atk;
    battle_cinematic.defender = _def;
    battle_cinematic.attacker_stack = !is_undefined(_atk_stack_override) ? _atk_stack_override : get_stack_at_tile(_atk.grid_c, _atk.grid_r, _atk.team);
    battle_cinematic.defender_stack = !is_undefined(_def_stack_override) ? _def_stack_override : get_stack_at_tile(_def.grid_c, _def.grid_r, _def.team);"""

assert old_assign in content, 'attacker assignment not found'
content = content.replace(old_assign, new_assign, 1)

# 2. Update execute_stack_volley to pass stacks
old_volley_call = """    // Launch Gihren's Greed Battle Clash Cutscene
    start_battle_cinematic(_lead_u, _def_target, _lead_w, COMBAT_STATE.ATTACK_EXECUTION);"""

new_volley_call = """    // Launch Gihren's Greed Battle Clash Cutscene
    var _def_stk = get_stack_at_tile(_def_target.grid_c, _def_target.grid_r, _def_target.team);
    start_battle_cinematic(_lead_u, _def_target, _lead_w, COMBAT_STATE.ATTACK_EXECUTION, _atk_stack, _def_stk);"""

assert old_volley_call in content, 'volley call not found'
content = content.replace(old_volley_call, new_volley_call, 1)

# 3. Update update_battle_cinematic for multi-unit firing in Phase 1
old_wing2_fire = """        // Frame 31: Wingman 2 Synchronized Salvo
        if (_t == 31 && battle_cinematic.attacker.squad_type == "PLATOON_3" && battle_cinematic.attacker.squad_members_count >= 3) {
            battle_cinematic.atk_wing2_recoil_x = -12;
            scr_audio_play_weapon(battle_cinematic.weapon.short_name);
            array_push(battle_cinematic.casings, {
                x: 170, y: 510, vx: random_range(-5.5, -3.0), vy: random_range(-5.0, -2.5),
                angle: irandom(360), spin: random_range(-18, 18), life: 75
            });
            array_push(battle_cinematic.projectiles, {
                type: battle_cinematic.weapon.proj_type,
                x1: 205, y1: 505, x2: 1025, y2: 480,
                cur_x: 205, cur_y: 505, t: 0.0, speed: 0.038,
                trail: battle_cinematic.weapon.proj_type
            });
        }"""

new_wing2_fire = """        // Frame 31: Wingman 2 Synchronized Salvo
        if (_t == 31 && battle_cinematic.attacker.squad_type == "PLATOON_3" && battle_cinematic.attacker.squad_members_count >= 3) {
            battle_cinematic.atk_wing2_recoil_x = -12;
            scr_audio_play_weapon(battle_cinematic.weapon.short_name);
            array_push(battle_cinematic.casings, {
                x: 170, y: 510, vx: random_range(-5.5, -3.0), vy: random_range(-5.0, -2.5),
                angle: irandom(360), spin: random_range(-18, 18), life: 75
            });
            array_push(battle_cinematic.projectiles, {
                type: battle_cinematic.weapon.proj_type,
                x1: 205, y1: 505, x2: 1025, y2: 480,
                cur_x: 205, cur_y: 505, t: 0.0, speed: 0.038,
                trail: battle_cinematic.weapon.proj_type
            });
        }

        // Staggered Firing for 6-Unit Battlegroup Stack
        if (variable_struct_exists(battle_cinematic, "attacker_stack") && array_length(battle_cinematic.attacker_stack) > 1) {
            var _stk_atk = battle_cinematic.attacker_stack;
            var _fire_frames = [21, 25, 29, 33, 37, 41];
            for (var sf = 1; sf < min(6, array_length(_stk_atk)); sf++) {
                if (_t == _fire_frames[sf] && !_stk_atk[sf].is_destroyed) {
                    scr_audio_play_weapon(battle_cinematic.weapon.short_name);
                    var _fx_slot = variable_struct_exists(_stk_atk[sf], "formation_slot") ? _stk_atk[sf].formation_slot : sf;
                    var _src_x = (_fx_slot < 3) ? 310 : 160;
                    var _src_y = 470 + ((_fx_slot % 3 == 1) ? -40 : ((_fx_slot % 3 == 2) ? 40 : 0));
                    array_push(battle_cinematic.casings, {
                        x: _src_x, y: _src_y, vx: random_range(-5.5, -3.0), vy: random_range(-5.0, -2.5),
                        angle: irandom(360), spin: random_range(-18, 18), life: 75
                    });
                    array_push(battle_cinematic.projectiles, {
                        type: battle_cinematic.weapon.proj_type,
                        x1: _src_x + 30, y1: _src_y, x2: 1010 + irandom_range(-25, 25), y2: 465 + irandom_range(-25, 25),
                        cur_x: _src_x + 30, cur_y: _src_y, t: 0.0, speed: 0.038,
                        trail: battle_cinematic.weapon.proj_type
                    });
                }
            }
        }"""

assert old_wing2_fire in content, 'wing2 fire not found'
content = content.replace(old_wing2_fire, new_wing2_fire, 1)

# 4. Update draw_battle_cinematic_stage formation rendering
old_formation = """    // --- 1. ATTACKER PLATOON (LEFT SIDE, FACING RIGHT [facing = 1]) ---
    var _ax = 340 + battle_cinematic.atk_recoil_x + _shake_x;
    var _ay = _base_ground_y + battle_cinematic.atk_recoil_y + _shake_y;
    if (battle_cinematic.is_air_atk) _ay -= (65 + sin(current_time * 0.004) * 6);
    if (battle_cinematic.is_water) _ay += 12;

    // Attacker Lead Mech
    scr_draw_animated_mobile_suit(_atk.mech_type, _ax, _ay, 1.30, 1, battle_cinematic.atk_anim_state, -1, _atk.image_blend, "front");

    // Attacker Platoon Wingmen
    if (_atk.squad_type == "PLATOON_3") {
        if (_atk.squad_members_count >= 2) {
            var _w1x = 210 + battle_cinematic.atk_wing1_recoil_x + _shake_x;
            var _w1y = _base_ground_y - 60 + (battle_cinematic.is_air_atk ? -60 : 0);
            scr_draw_animated_mobile_suit(_atk.mech_type, _w1x, _w1y, 1.08, 1, battle_cinematic.atk_anim_state, -1, _atk.image_blend, "front");
        }
        if (_atk.squad_members_count >= 3) {
            var _w2x = 170 + battle_cinematic.atk_wing2_recoil_x + _shake_x;
            var _w2y = _base_ground_y + 45 + (battle_cinematic.is_air_atk ? -60 : 0);
            scr_draw_animated_mobile_suit(_atk.mech_type, _w2x, _w2y, 1.08, 1, battle_cinematic.atk_anim_state, -1, _atk.image_blend, "front");
        }
    }

    // --- 2. DEFENDER PLATOON (RIGHT SIDE, FACING LEFT [facing = -1]) ---
    var _dx = 1026 + battle_cinematic.def_recoil_x + _shake_x;
    var _dy = _base_ground_y + battle_cinematic.def_recoil_y + _shake_y;
    if (battle_cinematic.is_air_def) _dy -= (65 + sin(current_time * 0.004 + 1.2) * 6);
    if (battle_cinematic.is_water) _dy += 12;

    // Defender Lead Mech
    scr_draw_animated_mobile_suit(_def.mech_type, _dx, _dy, 1.30, -1, battle_cinematic.def_anim_state, -1, _def.image_blend, "front");

    // Defender Platoon Wingmen
    if (_def.squad_type == "PLATOON_3") {
        if (_def.squad_members_count >= 2) {
            var _dw1x = 1156 + battle_cinematic.def_wing1_recoil_x + _shake_x;
            var _dw1y = _base_ground_y - 60 + (battle_cinematic.is_air_def ? -60 : 0);
            scr_draw_animated_mobile_suit(_def.mech_type, _dw1x, _dw1y, 1.08, -1, battle_cinematic.def_anim_state, -1, _def.image_blend, "front");
        }
        if (_def.squad_members_count >= 3) {
            var _dw2x = 1196 + battle_cinematic.def_wing2_recoil_x + _shake_x;
            var _dw2y = _base_ground_y + 45 + (battle_cinematic.is_air_def ? -60 : 0);
            scr_draw_animated_mobile_suit(_def.mech_type, _dw2x, _dw2y, 1.08, -1, battle_cinematic.def_anim_state, -1, _def.image_blend, "front");
        }
    }"""

new_formation = """    // --- 1. ATTACKER FORMATION (LEFT SIDE, FACING RIGHT [facing = 1]) ---
    var _ax = 340 + battle_cinematic.atk_recoil_x + _shake_x;
    var _ay = _base_ground_y + battle_cinematic.atk_recoil_y + _shake_y;
    if (battle_cinematic.is_air_atk) _ay -= (65 + sin(current_time * 0.004) * 6);
    if (battle_cinematic.is_water) _ay += 12;

    if (variable_struct_exists(battle_cinematic, "attacker_stack") && array_length(battle_cinematic.attacker_stack) > 1) {
        var _atk_stk = battle_cinematic.attacker_stack;
        var _vg_offsets_x = [360, 305, 315];
        var _vg_offsets_y = [0, -65, 60];
        var _sp_offsets_x = [200, 145, 155];
        var _sp_offsets_y = [0, -70, 65];

        for (var k = 0; k < min(6, array_length(_atk_stk)); k++) {
            var _uk = _atk_stk[k];
            if (_uk.is_destroyed) continue;

            var _slot_k = variable_struct_exists(_uk, "formation_slot") ? _uk.formation_slot : k;
            var _ux = 0;
            var _uy = 0;
            var _uscale = 1.0;

            if (_slot_k < 3) {
                _ux = _vg_offsets_x[_slot_k] + battle_cinematic.atk_recoil_x + _shake_x;
                _uy = _base_ground_y + _vg_offsets_y[_slot_k] + battle_cinematic.atk_recoil_y + _shake_y;
                _uscale = (_slot_k == 0) ? 1.25 : 1.12;
            } else {
                var _sp_idx = min(2, _slot_k - 3);
                _ux = _sp_offsets_x[_sp_idx] + battle_cinematic.atk_recoil_x * 0.7 + _shake_x;
                _uy = _base_ground_y + _sp_offsets_y[_sp_idx] + battle_cinematic.atk_recoil_y * 0.7 + _shake_y;
                _uscale = 0.98;
            }

            var _is_k_air = (variable_struct_exists(_uk, "is_aircraft") && _uk.is_aircraft) || (variable_struct_get(_uk, "move_type") == "aero");
            if (_is_k_air) _uy -= (65 + sin(current_time * 0.004 + k) * 6);
            if (battle_cinematic.is_water) _uy += 12;

            if (variable_struct_exists(_uk, "sprite_index") && sprite_exists(_uk.sprite_index) && ((variable_struct_exists(_uk, "is_vehicle") && _uk.is_vehicle) || (variable_struct_exists(_uk, "is_infantry") && _uk.is_infantry))) {
                draw_sprite_ext(_uk.sprite_index, 0, _ux, _uy, _uscale, _uscale, 0, _uk.image_blend, 1.0);
            } else {
                scr_draw_animated_mobile_suit(_uk.mech_type, _ux, _uy, _uscale, 1, battle_cinematic.atk_anim_state, -1, _uk.image_blend, "front");
            }
        }
    } else {
        scr_draw_animated_mobile_suit(_atk.mech_type, _ax, _ay, 1.30, 1, battle_cinematic.atk_anim_state, -1, _atk.image_blend, "front");
        if (_atk.squad_type == "PLATOON_3") {
            if (_atk.squad_members_count >= 2) {
                var _w1x = 210 + battle_cinematic.atk_wing1_recoil_x + _shake_x;
                var _w1y = _base_ground_y - 60 + (battle_cinematic.is_air_atk ? -60 : 0);
                scr_draw_animated_mobile_suit(_atk.mech_type, _w1x, _w1y, 1.08, 1, battle_cinematic.atk_anim_state, -1, _atk.image_blend, "front");
            }
            if (_atk.squad_members_count >= 3) {
                var _w2x = 170 + battle_cinematic.atk_wing2_recoil_x + _shake_x;
                var _w2y = _base_ground_y + 45 + (battle_cinematic.is_air_atk ? -60 : 0);
                scr_draw_animated_mobile_suit(_atk.mech_type, _w2x, _w2y, 1.08, 1, battle_cinematic.atk_anim_state, -1, _atk.image_blend, "front");
            }
        }
    }

    // --- 2. DEFENDER FORMATION (RIGHT SIDE, FACING LEFT [facing = -1]) ---
    var _dx = 1026 + battle_cinematic.def_recoil_x + _shake_x;
    var _dy = _base_ground_y + battle_cinematic.def_recoil_y + _shake_y;
    if (battle_cinematic.is_air_def) _dy -= (65 + sin(current_time * 0.004 + 1.2) * 6);
    if (battle_cinematic.is_water) _dy += 12;

    if (variable_struct_exists(battle_cinematic, "defender_stack") && array_length(battle_cinematic.defender_stack) > 1) {
        var _def_stk = battle_cinematic.defender_stack;
        var _dvg_offsets_x = [1006, 1061, 1051];
        var _dvg_offsets_y = [0, -65, 60];
        var _dsp_offsets_x = [1166, 1221, 1211];
        var _dsp_offsets_y = [0, -70, 65];

        for (var k = 0; k < min(6, array_length(_def_stk)); k++) {
            var _uk = _def_stk[k];
            if (_uk.is_destroyed) continue;

            var _slot_k = variable_struct_exists(_uk, "formation_slot") ? _uk.formation_slot : k;
            var _ux = 0;
            var _uy = 0;
            var _uscale = 1.0;

            if (_slot_k < 3) {
                _ux = _dvg_offsets_x[_slot_k] + battle_cinematic.def_recoil_x + _shake_x;
                _uy = _base_ground_y + _dvg_offsets_y[_slot_k] + battle_cinematic.def_recoil_y + _shake_y;
                _uscale = (_slot_k == 0) ? 1.25 : 1.12;
            } else {
                var _sp_idx = min(2, _slot_k - 3);
                _ux = _dsp_offsets_x[_sp_idx] + battle_cinematic.def_recoil_x * 0.7 + _shake_x;
                _uy = _base_ground_y + _dsp_offsets_y[_sp_idx] + battle_cinematic.def_recoil_y * 0.7 + _shake_y;
                _uscale = 0.98;
            }

            var _is_k_air = (variable_struct_exists(_uk, "is_aircraft") && _uk.is_aircraft) || (variable_struct_get(_uk, "move_type") == "aero");
            if (_is_k_air) _uy -= (65 + sin(current_time * 0.004 + k + 1.2) * 6);
            if (battle_cinematic.is_water) _uy += 12;

            if (variable_struct_exists(_uk, "sprite_index") && sprite_exists(_uk.sprite_index) && ((variable_struct_exists(_uk, "is_vehicle") && _uk.is_vehicle) || (variable_struct_exists(_uk, "is_infantry") && _uk.is_infantry))) {
                draw_sprite_ext(_uk.sprite_index, 0, _ux, _uy, -_uscale, _uscale, 0, _uk.image_blend, 1.0);
            } else {
                scr_draw_animated_mobile_suit(_uk.mech_type, _ux, _uy, _uscale, -1, battle_cinematic.def_anim_state, -1, _uk.image_blend, "front");
            }
        }
    } else {
        scr_draw_animated_mobile_suit(_def.mech_type, _dx, _dy, 1.30, -1, battle_cinematic.def_anim_state, -1, _def.image_blend, "front");
        if (_def.squad_type == "PLATOON_3") {
            if (_def.squad_members_count >= 2) {
                var _dw1x = 1156 + battle_cinematic.def_wing1_recoil_x + _shake_x;
                var _dw1y = _base_ground_y - 60 + (battle_cinematic.is_air_def ? -60 : 0);
                scr_draw_animated_mobile_suit(_def.mech_type, _dw1x, _dw1y, 1.08, -1, battle_cinematic.def_anim_state, -1, _def.image_blend, "front");
            }
            if (_def.squad_members_count >= 3) {
                var _dw2x = 1196 + battle_cinematic.def_wing2_recoil_x + _shake_x;
                var _dw2y = _base_ground_y + 45 + (battle_cinematic.is_air_def ? -60 : 0);
                scr_draw_animated_mobile_suit(_def.mech_type, _dw2x, _dw2y, 1.08, -1, battle_cinematic.def_anim_state, -1, _def.image_blend, "front");
            }
        }
    }"""

assert old_formation in content, 'formation rendering not found'
content = content.replace(old_formation, new_formation, 1)

with open('objects/obj_BattleManager/Create_0.gml', 'w') as f_out:
    f_out.write(content)

print('Successfully patched Create_0.gml with cinematic multi-unit formations')
