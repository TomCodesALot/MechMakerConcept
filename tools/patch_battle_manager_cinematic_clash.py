# -*- coding: utf-8 -*-
"""
Patches obj_BattleManager/Create_0.gml and Draw_0.gml with the complete
Goal Final: Modular Combat Clash & Dynamic Mecha Animation Engine,
preserving all 5 combat refinements (Vanguard screen, Brace, Dynamic Pacing, Wreckage, Ejection).
"""

import re

# =========================================================================
# 1. PATCH Create_0.gml
# =========================================================================
create_path = "objects/obj_BattleManager/Create_0.gml"
with open(create_path, "r", encoding="utf-8") as f:
    text = f.read()

start_idx = text.find("start_battle_cinematic = function")
end_idx = text.find("// 5. Legacy Map Projectile Spawner (Preserved for Fallback)")

if start_idx == -1 or end_idx == -1:
    print("[ERROR] Could not find cinematic block boundaries in Create_0.gml")
    exit(1)

new_cinematic_block = """start_battle_cinematic = function(_atk, _def, _wpn, _return_state = COMBAT_STATE.PLAYER_PHASE, _atk_stack_override = undefined, _def_stack_override = undefined) {
    if (!cinematic_combat_enabled) {
        legacy_spawn_combat_projectile(_atk, _def, _wpn);
        return;
    }

    var _dist = calculate_distance(_atk.grid_c, _atk.grid_r, _def.grid_c, _def.grid_r);
    var _hit_chance = calculate_hit_chance(_atk, _def, _dist, _wpn);
    if (variable_struct_exists(_atk, "is_aimed_shot") && _atk.is_aimed_shot) _hit_chance = max(10, _hit_chance - 15);

    var _roll = irandom_range(1, 100);
    var _is_hit = (_roll <= _hit_chance);

    // Hit Part Selection (Front Mission 5-Part Mechanics)
    var _hit_part = "torso";
    if (variable_struct_exists(_atk, "is_aimed_shot") && _atk.is_aimed_shot && _atk.targeted_limb != "") {
        _hit_part = _atk.targeted_limb;
    } else {
        var _part_roll = irandom_range(1, 100);
        if (_part_roll <= 40) _hit_part = "torso";
        else if (_part_roll <= 55) _hit_part = "arm_left";
        else if (_part_roll <= 70) _hit_part = "arm_right";
        else if (_part_roll <= 90) _hit_part = "legs";
        else _hit_part = "head";
    }

    // Platoon Volley Scaling: 100% at 3/3, 75% at 2/3, 50% at 1/3
    var _squad_mult = 1.0;
    if (_atk.squad_type == "PLATOON_3") {
        _squad_mult = (_atk.squad_members_count == 3) ? 1.0 : ((_atk.squad_members_count == 2) ? 0.75 : 0.50);
    }
    var _raw_dmg = floor((_wpn.damage + irandom_range(-15, 20)) * _squad_mult);

    // Directional Facing Damage Multipliers (Goal F: Flanking & Rear Ambush)
    var _inc_dir = iso_get_facing(_def.grid_c, _def.grid_r, _atk.grid_c, _atk.grid_r);
    var _is_rear = (_inc_dir == (_def.facing + 2) % 4);
    var _is_flank = (_inc_dir == (_def.facing + 1) % 4 || _inc_dir == (_def.facing + 3) % 4);
    var _flank_tag = "";
    if (_is_rear) {
        _raw_dmg = floor(_raw_dmg * 1.40);
        _flank_tag = "[REAR CORE HIT +40%]";
        if (irandom(100) < 65) _hit_part = "torso"; else _hit_part = "backpack";
    } else if (_is_flank) {
        _raw_dmg = floor(_raw_dmg * 1.20);
        _flank_tag = "[FLANK SHOT +20%]";
        if (irandom(100) < 50) _hit_part = (_inc_dir == (_def.facing + 1) % 4) ? "arm_right" : "arm_left";
    }

    // High Ground Elevation Damage Bonus (+15% per tier above defender)
    var _elev_diff = _atk.elev - _def.elev;
    var _elev_tag = "";
    if (_elev_diff > 0) {
        _raw_dmg = floor(_raw_dmg * (1.0 + (_elev_diff * 0.15)));
        _elev_tag = "[HIGH GROUND +" + string(_elev_diff * 15) + "%]";
    }

    // Mitigation Calculation with Brace Stance & Vanguard Screening (Refined Combat System)
    var _limb = variable_struct_get(_def.components, _hit_part);
    var _is_braced = variable_struct_exists(_def, "braced") && _def.braced;
    var _mitigated_dmg = max(15, _raw_dmg - _limb.armor);
    if (_is_braced) {
        _mitigated_dmg = max(10, floor(_mitigated_dmg * 0.60));
    }

    // Vanguard Screening & Interception:
    // Direct fire (non-artillery/missiles) aimed at rear support line is intercepted by frontline Vanguard!
    var _is_artillery_or_missile = (_wpn.range_max >= 4 || _wpn.proj_type == "MICRO_MISSILE" || _wpn.proj_type == "MISSILE");
    var _def_stk_check = !is_undefined(_def_stack_override) ? _def_stack_override : get_stack_at_tile(_def.grid_c, _def.grid_r, _def.team);
    if (!_is_artillery_or_missile && variable_struct_exists(_def, "formation_slot") && _def.formation_slot >= 3) {
        for (var vi = 0; vi < array_length(_def_stk_check); vi++) {
            var _vu = _def_stk_check[vi];
            if (!_vu.is_destroyed && variable_struct_exists(_vu, "formation_slot") && _vu.formation_slot < 3) {
                _def = _vu;
                _limb = variable_struct_get(_def.components, _hit_part);
                _mitigated_dmg = max(15, _raw_dmg - _limb.armor);
                if (variable_struct_exists(_def, "braced") && _def.braced) {
                    _mitigated_dmg = max(10, floor(_mitigated_dmg * 0.60));
                }
                add_log("[VANGUARD SCREEN] " + _vu.callsign + " intercepted incoming fire aimed at rear support line!");
                break;
            }
        }
    }

    // Cover Mitigation
    var _def_cover = grid_cover[_def.grid_c][_def.grid_r];
    if (_def_cover == 2) _mitigated_dmg = floor(_mitigated_dmg * 0.70);
    else if (_def_cover == 1) _mitigated_dmg = floor(_mitigated_dmg * 0.85);

    // Critical Hit Roll (5% base + 15% if flank/rear)
    var _crit_chance = 5 + (_is_rear ? 20 : (_is_flank ? 10 : 0));
    var _is_crushing = (irandom(100) < _crit_chance);
    if (_is_crushing) {
        _mitigated_dmg = floor(_mitigated_dmg * 1.5);
    }

    // Counter-Attack Readiness Evaluation (Braced units forfeit counter)
    var _has_counter = false;
    var _counter_w = undefined;
    var _counter_hit_chance = 0;
    var _counter_is_hit = false;
    var _counter_hit_part = "torso";
    var _counter_dmg = 0;

    var _survives = (!_is_hit || (_hit_part != "torso" && _limb.cur > _mitigated_dmg) || (_hit_part == "torso" && _limb.cur > _mitigated_dmg));
    if (_survives && !_is_braced && array_length(_def.weapons) > 0 && _def.current_ap >= 2) {
        for (var w = 0; w < array_length(_def.weapons); w++) {
            var _cw = _def.weapons[w];
            if (_cw.range_min <= _dist && _cw.range_max >= _dist && _def.current_ap >= _cw.ap_cost) {
                _has_counter = true;
                _counter_w = _cw;
                break;
            }
        }
        if (_has_counter && !is_undefined(_counter_w)) {
            _counter_hit_chance = calculate_hit_chance(_def, _atk, _dist, _counter_w);
            _counter_is_hit = (irandom_range(1, 100) <= _counter_hit_chance);
            var _cpart_roll = irandom_range(1, 100);
            if (_cpart_roll <= 45) _counter_hit_part = "torso";
            else if (_cpart_roll <= 65) _counter_hit_part = "arm_right";
            else if (_cpart_roll <= 85) _counter_hit_part = "legs";
            else _counter_hit_part = "head";

            var _catk_armor = variable_struct_get(_atk.components, _counter_hit_part).armor;
            _counter_dmg = max(1, _counter_w.damage - floor(_catk_armor * 0.5));
        }
    }

    // Environmental Theater and Terrain Resolution
    var _terr = grid_terrain[_def.grid_c][_def.grid_r];
    var _theater = variable_struct_get(_cur_map, "theater") ?? "EARTH_SURFACE";
    var _is_space = (_theater == "SPACE" || _terr == 4);
    var _is_water = (_terr == 3);
    var _is_slag = (_terr == 5);
    var _is_air_atk = (variable_struct_exists(_atk, "is_aircraft") && _atk.is_aircraft) || (variable_struct_get(_atk, "move_type") == "aero");
    var _is_air_def = (variable_struct_exists(_def, "is_aircraft") && _def.is_aircraft) || (variable_struct_get(_def, "move_type") == "aero");

    // Resolve Weapon Class and Pilot Profiles (Goal Final Modular Combat Engine)
    var _wpn_type = variable_struct_exists(_wpn, "proj_type") ? _wpn.proj_type : "KINETIC_CANNON";
    var _wpn_class = "BALLISTIC";
    if (string_pos("BEAM", _wpn_type) > 0 || string_pos("PLASMA", _wpn_type) > 0 || string_pos("TACHYON", _wpn_type) > 0 || string_pos("LASER", _wpn_type) > 0) {
        _wpn_class = "ENERGY";
    } else if (string_pos("MISSILE", _wpn_type) > 0 || string_pos("ROCKET", _wpn_type) > 0 || string_pos("HOWITZER", _wpn_type) > 0) {
        _wpn_class = "ORDNANCE";
    } else if (string_pos("BLADE", _wpn_type) > 0 || string_pos("MELEE", _wpn_type) > 0 || string_pos("SABER", _wpn_type) > 0 || string_pos("CLAW", _wpn_type) > 0 || string_pos("PILE", _wpn_type) > 0) {
        _wpn_class = "MELEE";
    }

    var _resolve_pilot_portrait = function(_pname) {
        if (string_pos("Cole", _pname) > 0) return spr_portrait_cole;
        if (string_pos("Nadia", _pname) > 0) return spr_portrait_nadia;
        if (string_pos("Vance", _pname) > 0) return spr_portrait_vance;
        if (string_pos("Cruz", _pname) > 0) return spr_portrait_cruz;
        if (string_pos("Cassian", _pname) > 0) return spr_portrait_cassian;
        if (string_pos("Renzo", _pname) > 0) return spr_portrait_renzo;
        if (string_pos("Sorren", _pname) > 0) return spr_portrait_sorren;
        if (string_pos("Null-07", _pname) > 0 || string_pos("NULL", _pname) > 0) return spr_portrait_null07;
        return spr_portrait_commander_male;
    };

    if (!variable_struct_exists(_atk, "damaged_parts")) _atk.damaged_parts = { head: false, torso: false, arm_left: false, arm_right: false, legs: false, backpack: false };
    if (!variable_struct_exists(_def, "damaged_parts")) _def.damaged_parts = { head: false, torso: false, arm_left: false, arm_right: false, legs: false, backpack: false };

    // Dynamic Cinematic Pacing: Ace & Incursions get full cutscene; grunts run fast condensed clash
    var _is_ace_clash = (_atk.squad_type == "SUPER_ACE" || _def.squad_type == "SUPER_ACE" || state == COMBAT_STATE.NEMESIS_INCURSION);

    // Populate Cinematic State
    battle_cinematic.active = true;
    battle_cinematic.phase = 0;
    battle_cinematic.timer = 0;
    battle_cinematic.return_state = _return_state;
    battle_cinematic.attacker = _atk;
    battle_cinematic.defender = _def;
    battle_cinematic.attacker_stack = !is_undefined(_atk_stack_override) ? _atk_stack_override : get_stack_at_tile(_atk.grid_c, _atk.grid_r, _atk.team);
    battle_cinematic.defender_stack = !is_undefined(_def_stack_override) ? _def_stack_override : get_stack_at_tile(_def.grid_c, _def.grid_r, _def.team);
    battle_cinematic.weapon = _wpn;
    battle_cinematic.weapon_class = _wpn_class;
    battle_cinematic.atk_dash_x = 0.0;
    battle_cinematic.melee_cleave_timer = 0;
    battle_cinematic.counter_weapon = _counter_w;
    battle_cinematic.flank_tag = _flank_tag;
    battle_cinematic.elev_tag = _elev_tag;
    battle_cinematic.has_counter = _has_counter;

    battle_cinematic.atk_portrait = _resolve_pilot_portrait(_atk.pilot_name);
    battle_cinematic.def_portrait = _resolve_pilot_portrait(_def.pilot_name);
    battle_cinematic.atk_expr = "NEUTRAL";
    battle_cinematic.def_expr = "DEFENDING";
    battle_cinematic.atk_radio_bark = "Target acquired. Engaging with " + string_upper(_wpn.name) + "!";
    battle_cinematic.def_radio_bark = "Hostile vector detected! Reinforcing kinetic louvers!";

    battle_cinematic.atk_anim_state = "idle";
    battle_cinematic.def_anim_state = "idle";
    battle_cinematic.atk_recoil_x = 0;
    battle_cinematic.atk_recoil_y = 0;
    battle_cinematic.def_recoil_x = 0;
    battle_cinematic.def_recoil_y = 0;

    battle_cinematic.atk_wing1_recoil_x = 0; battle_cinematic.atk_wing1_recoil_y = 0;
    battle_cinematic.atk_wing2_recoil_x = 0; battle_cinematic.atk_wing2_recoil_y = 0;
    battle_cinematic.def_wing1_recoil_x = 0; battle_cinematic.def_wing1_recoil_y = 0;
    battle_cinematic.def_wing2_recoil_x = 0; battle_cinematic.def_wing2_recoil_y = 0;

    battle_cinematic.hit_chance = _hit_chance;
    battle_cinematic.is_hit = _is_hit;
    battle_cinematic.hit_part = _hit_part;
    battle_cinematic.raw_damage = _raw_dmg;
    battle_cinematic.mitigated_dmg = _mitigated_dmg;
    battle_cinematic.is_crushing = _is_crushing;
    battle_cinematic.is_suppression = false;
    battle_cinematic.applied_primary = false;
    battle_cinematic.limb_flash_part = "";
    battle_cinematic.limb_flash_timer = 0;

    battle_cinematic.counter_hit_chance = _counter_hit_chance;
    battle_cinematic.counter_is_hit = _counter_is_hit;
    battle_cinematic.counter_hit_part = _counter_hit_part;
    battle_cinematic.counter_damage = _counter_dmg;
    battle_cinematic.applied_counter = false;

    battle_cinematic.shutter_y = 0.0;
    battle_cinematic.screen_shake = 0.0;
    battle_cinematic.flash_alpha = 0.0;
    battle_cinematic.is_condensed = !_is_ace_clash;
    battle_cinematic.theater = _theater;
    battle_cinematic.terrain = _terr;
    battle_cinematic.is_space = _is_space;
    battle_cinematic.is_water = _is_water;
    battle_cinematic.is_slag = _is_slag;
    battle_cinematic.is_air_atk = _is_air_atk;
    battle_cinematic.is_air_def = _is_air_def;

    battle_cinematic.projectiles = [];
    battle_cinematic.particles = [];
    battle_cinematic.casings = [];
    battle_cinematic.popups = [];

    scr_audio_play_ui("confirm");
};

// 2. Update Battle Cinematic State & Choreography
update_battle_cinematic = function() {
    if (!battle_cinematic.active) return;

    // Fast-Forward / Skip Input Check (Space, Enter, or Click)
    if (keyboard_check_pressed(vk_space) || keyboard_check_pressed(vk_enter) || mouse_check_button_pressed(mb_left)) {
        skip_battle_cinematic();
        return;
    }

    battle_cinematic.timer += (variable_struct_exists(battle_cinematic, "is_condensed") && battle_cinematic.is_condensed) ? 2 : 1;
    var _t = battle_cinematic.timer;

    // Screen Shake & Flash Decay
    if (battle_cinematic.screen_shake > 0) battle_cinematic.screen_shake = max(0, battle_cinematic.screen_shake - 0.7);
    if (battle_cinematic.flash_alpha > 0) battle_cinematic.flash_alpha = max(0, battle_cinematic.flash_alpha - 0.06);
    if (battle_cinematic.limb_flash_timer > 0) battle_cinematic.limb_flash_timer--;
    if (battle_cinematic.melee_cleave_timer > 0) battle_cinematic.melee_cleave_timer--;

    // Update Casings Physics
    for (var i = array_length(battle_cinematic.casings) - 1; i >= 0; i--) {
        var _c = battle_cinematic.casings[i];
        _c.x += _c.vx;
        _c.y += _c.vy;
        _c.vy += 0.45;
        _c.angle += _c.spin;
        if (_c.y >= 520) {
            _c.y = 520;
            _c.vy = -_c.vy * 0.45;
            _c.vx *= 0.7;
            if (abs(_c.vy) < 1.0) _c.vy = 0;
        }
        _c.life--;
        if (_c.life <= 0) array_delete(battle_cinematic.casings, i, 1);
    }

    // Update Particles
    for (var i = array_length(battle_cinematic.particles) - 1; i >= 0; i--) {
        var _p = battle_cinematic.particles[i];
        if (variable_struct_exists(_p, "vx")) {
            _p.x += _p.vx;
            _p.y += _p.vy;
            _p.vy += 0.35;
        }
        _p.frame += _p.speed;
        if (sprite_exists(_p.sprite) && _p.frame >= sprite_get_number(_p.sprite)) {
            array_delete(battle_cinematic.particles, i, 1);
        }
    }

    // Update Popups
    for (var i = array_length(battle_cinematic.popups) - 1; i >= 0; i--) {
        var _pop = battle_cinematic.popups[i];
        _pop.y -= 0.6;
        _pop.timer--;
        if (_pop.timer <= 15) _pop.alpha = max(0, _pop.timer / 15.0);
        if (_pop.timer <= 0) array_delete(battle_cinematic.popups, i, 1);
    }

    // Recoil Smooth Dampening
    battle_cinematic.atk_recoil_x *= 0.88;
    battle_cinematic.atk_recoil_y *= 0.88;
    battle_cinematic.def_recoil_x *= 0.88;
    battle_cinematic.def_recoil_y *= 0.88;
    battle_cinematic.atk_wing1_recoil_x *= 0.88;
    battle_cinematic.atk_wing2_recoil_x *= 0.88;
    battle_cinematic.def_wing1_recoil_x *= 0.88;
    battle_cinematic.def_wing2_recoil_x *= 0.88;

    // --- PHASE 0: Letterbox In & Threat Acquisition (Frames 0 to 20) ---
    if (_t <= 20) {
        battle_cinematic.phase = 0;
        battle_cinematic.shutter_y = min(115.0, (_t / 20.0) * 115.0);
        return;
    }

    // --- PHASE 1: Attacker Salvo Initiation (Frames 21 to 65) ---
    if (_t > 20 && _t <= 65) {
        battle_cinematic.phase = 1;
        battle_cinematic.shutter_y = 115.0;

        // Frame 21: Lead Unit Fires
        if (_t == 21) {
            battle_cinematic.atk_anim_state = "fire";
            battle_cinematic.atk_expr = "ATTACKING";
            battle_cinematic.atk_recoil_x = -16;
            scr_audio_play_weapon(battle_cinematic.weapon.short_name);

            if (battle_cinematic.weapon_class == "MELEE") {
                battle_cinematic.atk_radio_bark = "Engaging vernier overdrive! Executing kinetic strike!";
            } else if (battle_cinematic.weapon_class == "ENERGY") {
                battle_cinematic.atk_radio_bark = "Particle beam emitter locked! Discharging main array!";
            } else if (battle_cinematic.weapon_class == "ORDNANCE") {
                battle_cinematic.atk_radio_bark = "Shoulder pod doors open! Salvo away!";
            } else {
                battle_cinematic.atk_radio_bark = "Full rotary battery hot! Suppressing target position!";
            }

            // Eject Spent Shell Casing for Ballistics
            if (battle_cinematic.weapon_class == "BALLISTIC") {
                array_push(battle_cinematic.casings, {
                    x: 340, y: 470, vx: random_range(-5.5, -3.0), vy: random_range(-5.0, -2.5),
                    angle: irandom(360), spin: random_range(-18, 18), life: 75
                });
            }

            // Spawn Projectile / Energy Beam / Missile Salvo
            if (battle_cinematic.weapon_class != "MELEE") {
                array_push(battle_cinematic.projectiles, {
                    type: battle_cinematic.weapon.proj_type,
                    x1: 375, y1: 460, x2: 1010, y2: 465,
                    cur_x: 375, cur_y: 460, t: 0.0, speed: (battle_cinematic.weapon_class == "ENERGY" ? 0.065 : 0.038),
                    trail: battle_cinematic.weapon.proj_type
                });
            }
        }

        // Melee High-Speed Dash Thrust
        if (battle_cinematic.weapon_class == "MELEE") {
            if (_t >= 21 && _t <= 38) {
                battle_cinematic.atk_dash_x = lerp(battle_cinematic.atk_dash_x, 620.0, 0.22);
            } else if (_t == 39) {
                battle_cinematic.melee_cleave_timer = 24;
                battle_cinematic.screen_shake = 22.0;
                battle_cinematic.flash_alpha = 0.50;
                scr_audio_play_impact("kinetic", true);
                array_push(battle_cinematic.particles, {
                    sprite: spr_fx_spark, x: 1026, y: 440, frame: 0.0, speed: 0.40, scale: 2.0, alpha: 1.0
                });
            } else if (_t > 45 && _t <= 65) {
                battle_cinematic.atk_dash_x = lerp(battle_cinematic.atk_dash_x, 0.0, 0.16);
            }
        }

        // Frame 26: Wingman 1 Synchronized Salvo (if present in Platoon)
        if (_t == 26 && battle_cinematic.attacker.squad_type == "PLATOON_3" && battle_cinematic.attacker.squad_members_count >= 2) {
            battle_cinematic.atk_wing1_recoil_x = -12;
            scr_audio_play_weapon(battle_cinematic.weapon.short_name);
            if (battle_cinematic.weapon_class == "BALLISTIC") {
                array_push(battle_cinematic.casings, {
                    x: 210, y: 420, vx: random_range(-5.5, -3.0), vy: random_range(-5.0, -2.5),
                    angle: irandom(360), spin: random_range(-18, 18), life: 75
                });
            }
            array_push(battle_cinematic.projectiles, {
                type: battle_cinematic.weapon.proj_type,
                x1: 245, y1: 410, x2: 990, y2: 450,
                cur_x: 245, cur_y: 410, t: 0.0, speed: 0.038,
                trail: battle_cinematic.weapon.proj_type
            });
        }

        // Frame 31: Wingman 2 Synchronized Salvo
        if (_t == 31 && battle_cinematic.attacker.squad_type == "PLATOON_3" && battle_cinematic.attacker.squad_members_count >= 3) {
            battle_cinematic.atk_wing2_recoil_x = -12;
            scr_audio_play_weapon(battle_cinematic.weapon.short_name);
            if (battle_cinematic.weapon_class == "BALLISTIC") {
                array_push(battle_cinematic.casings, {
                    x: 170, y: 510, vx: random_range(-5.5, -3.0), vy: random_range(-5.0, -2.5),
                    angle: irandom(360), spin: random_range(-18, 18), life: 75
                });
            }
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
                    if (battle_cinematic.weapon_class == "BALLISTIC") {
                        array_push(battle_cinematic.casings, {
                            x: _src_x, y: _src_y, vx: random_range(-5.5, -3.0), vy: random_range(-5.0, -2.5),
                            angle: irandom(360), spin: random_range(-18, 18), life: 75
                        });
                    }
                    array_push(battle_cinematic.projectiles, {
                        type: battle_cinematic.weapon.proj_type,
                        x1: _src_x + 30, y1: _src_y, x2: 1010 + irandom_range(-25, 25), y2: 465 + irandom_range(-25, 25),
                        cur_x: _src_x + 30, cur_y: _src_y, t: 0.0, speed: 0.038,
                        trail: battle_cinematic.weapon.proj_type
                    });
                }
            }
        }

        // Rapid Vulcan Multi-Bullet Stream
        if (battle_cinematic.weapon.proj_type == "ROTARY_VULCAN" && (_t == 25 || _t == 29 || _t == 34 || _t == 39)) {
            battle_cinematic.atk_recoil_x = -8;
            scr_audio_play_weapon(battle_cinematic.weapon.short_name);
            array_push(battle_cinematic.projectiles, {
                type: "ROTARY_VULCAN",
                x1: 375, y1: 455 + irandom_range(-6, 6), x2: 1010, y2: 460 + irandom_range(-15, 15),
                cur_x: 375, cur_y: 455, t: 0.0, speed: 0.065, trail: "tracer"
            });
        }

        // Recover to idle
        if (_t == 50) battle_cinematic.atk_anim_state = "idle";
    }

    // --- Update In-Flight Projectiles ---
    for (var i = array_length(battle_cinematic.projectiles) - 1; i >= 0; i--) {
        var _pj = battle_cinematic.projectiles[i];
        _pj.t += _pj.speed;
        _pj.cur_x = lerp(_pj.x1, _pj.x2, _pj.t);
        
        if (_pj.type == "KINETIC_CANNON" || _pj.type == "MICRO_MISSILE") {
            _pj.cur_y = lerp(_pj.y1, _pj.y2, _pj.t) - sin(_pj.t * pi) * 28.0;
        } else {
            _pj.cur_y = lerp(_pj.y1, _pj.y2, _pj.t);
        }

        if (_pj.t >= 1.0) {
            array_delete(battle_cinematic.projectiles, i, 1);
        }
    }

    // --- PHASE 2: Projectile Transit & Defender Reaction (Frames 65 to 85) ---
    if (_t > 65 && _t <= 85) {
        battle_cinematic.phase = 2;

        // Evasive Thruster Dodge if Miss
        if (!battle_cinematic.is_hit && _t == 72) {
            battle_cinematic.def_recoil_x = 26;
            battle_cinematic.def_expr = "EVADED";
            battle_cinematic.def_radio_bark = "Vernier burn successful! Impact vector cleared!";
            scr_audio_play_sfx(snd_mech_boost, 1.0, 0.05);
            array_push(battle_cinematic.popups, {
                text: "EVADED // THRUSTER BURST",
                x: 1026, y: 430, color: make_color_rgb(80, 240, 255),
                scale: 1.1, alpha: 1.0, timer: 50
            });
        }
    }

    // --- PHASE 3: Impact & Front Mission Modular Damage Resolution (Frames 85 to 145) ---
    if (_t > 85 && _t <= 145) {
        battle_cinematic.phase = 3;

        if (_t == 86 && !battle_cinematic.applied_primary) {
            battle_cinematic.applied_primary = true;
            var _def = battle_cinematic.defender;
            var _atk = battle_cinematic.attacker;
            var _part = battle_cinematic.hit_part;
            var _dmg = battle_cinematic.mitigated_dmg;

            if (battle_cinematic.is_hit) {
                battle_cinematic.screen_shake = 16.0;
                battle_cinematic.flash_alpha = 0.45;
                battle_cinematic.def_anim_state = "hit";
                battle_cinematic.def_expr = "TAKING_HIT";
                battle_cinematic.def_recoil_x = 22;
                battle_cinematic.limb_flash_part = _part;
                battle_cinematic.limb_flash_timer = 24;

                scr_audio_play_impact("kinetic", (battle_cinematic.weapon.damage > 50));

                // Goal G: Boss Regenerative Phase Barrier Absorption
                if (variable_struct_exists(_def, "barrier_cur") && _def.barrier_cur > 0) {
                    var _absorbed = min(_def.barrier_cur, _dmg);
                    _def.barrier_cur -= _absorbed;
                    _dmg -= _absorbed;
                    battle_cinematic.mitigated_dmg = _dmg;
                    array_push(battle_cinematic.popups, {
                        text: "[PHASE BARRIER -" + string(_absorbed) + "]",
                        x: 1026, y: 405, color: make_color_rgb(80, 220, 255),
                        scale: 1.15, alpha: 1.0, timer: 60
                    });
                    add_log("[BARRIER ABSORB] Ouroboros Prime Phase Barrier absorbed " + string(_absorbed) + " damage! (" + string(_def.barrier_cur) + " remaining)");
                }

                // Deduct modular limb damage
                var _limb = variable_struct_get(_def.components, _part);
                _limb.cur = max(0, _limb.cur - _dmg);

                // Goal Final: Limb Detachment & Persistent Battle Scars
                if (_limb.cur <= 0 && _limb.intact) {
                    _limb.intact = false;
                    variable_struct_set(_def.damaged_parts, _part, true);
                    battle_cinematic.def_expr = "CRIPPLED";
                    battle_cinematic.def_radio_bark = "Warning! " + string_upper(_limb.name) + " destroyed!";
                    
                    // Spawn flying severed limb debris
                    array_push(battle_cinematic.particles, {
                        sprite: (_part == "arm_right" ? spr_ms_ironclad_hit_right_arm_off : spr_ms_ironclad_hit_left_arm_off),
                        x: 1026, y: 440, vx: random_range(5.0, 8.0), vy: random_range(-8.0, -4.0),
                        frame: 0.0, speed: 0.0, scale: 1.15, alpha: 1.0
                    });

                    // Burst of socket sparks
                    for (var sk = 0; sk < 3; sk++) {
                        array_push(battle_cinematic.particles, {
                            sprite: spr_fx_spark, x: 1026 + irandom_range(-15, 15), y: 450 + irandom_range(-20, 20),
                            frame: 0.0, speed: 0.35, scale: 1.6, alpha: 1.0
                        });
                    }

                    array_push(battle_cinematic.popups, {
                        text: "[CRITICAL // " + string_upper(_part) + " SEVERED!]",
                        x: 1026, y: 380, color: make_color_rgb(255, 60, 60),
                        scale: 1.25, alpha: 1.0, timer: 70
                    });

                    // Catastrophic Kill Check
                    if (_part == "torso") {
                        _def.is_destroyed = true;
                        _def.anim_state = "destroyed";
                        _def.anim_timer = 40;
                        add_log("[CATASTROPHIC KILL] " + _def.callsign + " REACTOR BREACH! Unit neutralized.");

                        // 1. Tactical Battlefield Wreckage Cover (+20% cover on tile)
                        grid_cover[_def.grid_c][_def.grid_r] = 2;
                        add_log("[FIELD WRECKAGE] Smoldering chassis created tactical cover on tile (" + string(_def.grid_c) + ", " + string(_def.grid_r) + ")");

                        // 2. Pilot Ejection Survival Roll
                        var _ej_roll = irandom_range(1, 100);
                        if (_ej_roll <= 65) {
                            add_log("[EJECTION SUCCESS] Pilot ejected safely via escape pod.");
                        } else if (_ej_roll <= 88) {
                            add_log("[PILOT INJURED] Escape pod damaged during ejection; pilot hospitalized for 3 campaign turns.");
                        } else {
                            add_log("[KIA] Catastrophic cockpit breach; pilot lost in action.");
                        }
                    }
                } else if (_dmg > 80) {
                    battle_cinematic.atk_expr = "CRITICAL_SUCCESS";
                    battle_cinematic.atk_radio_bark = "Direct armor breach confirmed! Target integrity failing!";
                }

                // Explosions on Defender Lead
                array_push(battle_cinematic.particles, {
                    sprite: spr_fx_explosion, x: 1026 + irandom_range(-15, 15), y: 465 + irandom_range(-20, 20),
                    frame: 0.0, speed: 0.35, scale: 1.6, alpha: 1.0
                });

                // Damage Popup
                array_push(battle_cinematic.popups, {
                    text: "-" + string(_dmg) + " DMG (" + string_upper(_part) + ")",
                    x: 1026, y: 435, color: battle_cinematic.is_crushing ? make_color_rgb(255, 220, 50) : make_color_rgb(255, 120, 80),
                    scale: battle_cinematic.is_crushing ? 1.35 : 1.15, alpha: 1.0, timer: 65
                });
            }
        }
    }

    // --- PHASE 4: Counter-Attack Salvo (Frames 145 to 205) ---
    if (_t > 145 && _t <= 205) {
        battle_cinematic.phase = 4;

        if (battle_cinematic.has_counter && _t == 150 && !battle_cinematic.applied_counter) {
            battle_cinematic.applied_counter = true;
            battle_cinematic.def_anim_state = "fire";
            battle_cinematic.def_recoil_x = 16;
            scr_audio_play_weapon(battle_cinematic.counter_weapon.short_name);

            // Spawn Counter Projectile towards Attacker
            array_push(battle_cinematic.projectiles, {
                type: battle_cinematic.counter_weapon.proj_type,
                x1: 1010, y1: 460, x2: 375, y2: 465,
                cur_x: 1010, cur_y: 460, t: 0.0, speed: 0.045,
                trail: battle_cinematic.counter_weapon.proj_type
            });
        }

        // Counter Impact at frame 175
        if (battle_cinematic.has_counter && _t == 175) {
            if (battle_cinematic.counter_is_hit) {
                battle_cinematic.atk_anim_state = "hit";
                battle_cinematic.atk_expr = "TAKING_HIT";
                battle_cinematic.atk_recoil_x = -18;
                battle_cinematic.screen_shake = 12.0;
                scr_audio_play_impact("kinetic", false);

                var _atk = battle_cinematic.attacker;
                var _cpart = battle_cinematic.counter_hit_part;
                var _cdmg = battle_cinematic.counter_damage;
                var _climb = variable_struct_get(_atk.components, _cpart);
                _climb.cur = max(0, _climb.cur - _cdmg);
                if (_climb.cur <= 0 && _climb.intact) {
                    _climb.intact = false;
                    variable_struct_set(_atk.damaged_parts, _cpart, true);
                }

                array_push(battle_cinematic.particles, {
                    sprite: spr_fx_explosion, x: 340 + irandom_range(-15, 15), y: 465 + irandom_range(-20, 20),
                    frame: 0.0, speed: 0.35, scale: 1.4, alpha: 1.0
                });
                array_push(battle_cinematic.popups, {
                    text: "[COUNTER] -" + string(_cdmg) + " (" + string_upper(_cpart) + ")",
                    x: 340, y: 435, color: make_color_rgb(255, 120, 80),
                    scale: 1.1, alpha: 1.0, timer: 55
                });
            } else {
                battle_cinematic.atk_recoil_x = -20;
                scr_audio_play_sfx(snd_mech_boost, 1.0, 0.05);
            }
        }
    }

    // --- PHASE 5: Shutter Retraction & Exit to Isometric Map (Frames 205 to 230) ---
    if (_t > 205) {
        battle_cinematic.phase = 5;
        var _out_t = (_t - 205) / 25.0;
        battle_cinematic.shutter_y = max(0.0, (1.0 - _out_t) * 115.0);

        if (_t >= 230) {
            skip_battle_cinematic();
        }
    }
};

// 3. Skip Battle Cinematic (Instant Resolution)
skip_battle_cinematic = function() {
    if (!battle_cinematic.active) return;

    var _atk = battle_cinematic.attacker;
    var _def = battle_cinematic.defender;
    var _part = battle_cinematic.hit_part;
    var _dmg = battle_cinematic.mitigated_dmg;

    if (!variable_struct_exists(_atk, "damaged_parts")) _atk.damaged_parts = { head: false, torso: false, arm_left: false, arm_right: false, legs: false, backpack: false };
    if (!variable_struct_exists(_def, "damaged_parts")) _def.damaged_parts = { head: false, torso: false, arm_left: false, arm_right: false, legs: false, backpack: false };

    // Apply primary damage if not applied yet
    if (!battle_cinematic.applied_primary) {
        battle_cinematic.applied_primary = true;
        if (battle_cinematic.is_hit) {
            // Goal G: Boss Phase Barrier Absorption on Skip
            if (variable_struct_exists(_def, "barrier_cur") && _def.barrier_cur > 0) {
                var _absorbed = min(_def.barrier_cur, _dmg);
                _def.barrier_cur -= _absorbed;
                _dmg -= _absorbed;
                add_log("[BARRIER ABSORB] Ouroboros Prime Phase Barrier absorbed " + string(_absorbed) + " damage!");
            }

            var _limb = variable_struct_get(_def.components, _part);
            _limb.cur = max(0, _limb.cur - _dmg);
            add_log("[HIT] " + _atk.callsign + " struck " + _def.callsign + " " + _limb.name + " for " + string(_dmg) + " damage!");

            // Goal F: Suppression & Cover Degradation on Skip
            if (!variable_struct_exists(_def, "hits_taken_this_turn")) _def.hits_taken_this_turn = 0;
            _def.hits_taken_this_turn++;
            var _is_supp_wpn_sk = (battle_cinematic.weapon.proj_type == "ROTARY_VULCAN" || string_pos("VULCAN", string_upper(battle_cinematic.weapon.name)) > 0 || string_pos("GATLING", string_upper(battle_cinematic.weapon.name)) > 0 || string_pos("AUTOCANNON", string_upper(battle_cinematic.weapon.name)) > 0 || string_pos("SUPPRESS", string_upper(battle_cinematic.weapon.name)) > 0);
            if (_is_supp_wpn_sk || _def.hits_taken_this_turn >= 2) {
                _def.is_suppressed = true;
                add_log("[CROSSFIRE PIN] " + _def.callsign + " pinned down by sustained suppressive fire!");
            }
            var _is_heavy_ord_sk = (battle_cinematic.weapon.proj_type == "RAILGUN" || battle_cinematic.weapon.proj_type == "KINETIC_CANNON" || battle_cinematic.weapon.proj_type == "CANNON" || string_pos("CANNON", string_upper(battle_cinematic.weapon.name)) > 0 || string_pos("RAILGUN", string_upper(battle_cinematic.weapon.name)) > 0 || string_pos("120MM", string_upper(battle_cinematic.weapon.name)) > 0 || string_pos("SIEGE", string_upper(battle_cinematic.weapon.name)) > 0 || battle_cinematic.weapon.damage >= 55);
            if (_is_heavy_ord_sk && grid_cover[_def.grid_c][_def.grid_r] > 0) {
                if (grid_cover[_def.grid_c][_def.grid_r] == 2) {
                    grid_cover[_def.grid_c][_def.grid_r] = 1;
                    add_log("[COVER BREACH] Fortified bastion at [" + string(_def.grid_c) + "," + string(_def.grid_r) + "] fractured to rubble!");
                } else if (grid_cover[_def.grid_c][_def.grid_r] == 1) {
                    grid_cover[_def.grid_c][_def.grid_r] = 0;
                    add_log("[COVER DESTROYED] Rubble position at [" + string(_def.grid_c) + "," + string(_def.grid_r) + "] obliterated by heavy ordnance!");
                }
            }

            if (_def.squad_type == "PLATOON_3") {
                var _hp_r = _def.components.torso.cur / _def.components.torso.max;
                if (_hp_r < 0.33) _def.squad_members_count = 1;
                else if (_hp_r < 0.66 && _def.squad_members_count > 2) _def.squad_members_count = 2;
            }

            if (_limb.cur <= 0 && _limb.intact) {
                _limb.intact = false;
                variable_struct_set(_def.damaged_parts, _part, true);
                add_log("[CRITICAL BREACH] " + _def.callsign + " " + _limb.name + " HAS BEEN SEVERED!");
                if (_part == "backpack" && (_def.id == "BOSS_OUROBOROS" || (variable_struct_exists(_def, "is_apex_boss") && _def.is_apex_boss))) {
                    _def.barrier_cur = 0;
                    add_log("[PHASE SHIELD COLLAPSE] Phase Barrier Emitter severed! Boss shields permanently offline!");
                }
                if (_part == "torso") {
                    _def.is_destroyed = true;
                    _def.anim_state = "destroyed";
                    _def.anim_timer = 40;
                    add_log("[CATASTROPHIC KILL] " + _def.callsign + " REACTOR BREACH! Unit neutralized.");

                    // 1. Tactical Battlefield Wreckage Cover (+20% cover on tile)
                    grid_cover[_def.grid_c][_def.grid_r] = 2;
                    add_log("[FIELD WRECKAGE] Smoldering chassis created tactical cover on tile (" + string(_def.grid_c) + ", " + string(_def.grid_r) + ")");

                    // 2. Pilot Ejection Survival Roll
                    var _ej_roll = irandom_range(1, 100);
                    if (_ej_roll <= 65) {
                        add_log("[EJECTION SUCCESS] Pilot ejected safely via escape pod.");
                    } else if (_ej_roll <= 88) {
                        add_log("[PILOT INJURED] Escape pod damaged during ejection; pilot hospitalized for 3 campaign turns.");
                    } else {
                        add_log("[KIA] Catastrophic cockpit breach; pilot lost in action.");
                    }

                    // Goal G: Apex Crisis Boss Defeat & Campaign Victory Path 4
                    if (_def.id == "BOSS_OUROBOROS" || (variable_struct_exists(_def, "is_apex_boss") && _def.is_apex_boss)) {
                        if (instance_exists(obj_GameManager)) {
                            obj_GameManager.crisis_defeated = true;
                            obj_GameManager.funds += 500000;
                            obj_GameManager.evaluate_campaign_victory();
                        }
                        scr_research_award_salvage_intel(choose("WEAPONS", "REACTORS", "SHIELDS", "UPGRADES"), 1.00);
                        add_log("[APEX CRISIS DEFEATED] DEUS-MACHINA: OUROBOROS PRIME CORE DESTROYED! Sol System Saved!");
                        if (instance_exists(obj_HQTerminal)) {
                            obj_HQTerminal.show_toast("APEX CRISIS VANQUISHED! SOL SYSTEM SAVED! +500,000 Cr & Eureka Tech!", c_lime);
                        }
                    }

                    if (instance_exists(obj_BlueprintManager)) {
                        var _vic_c = variable_struct_get(_def, "chassis_id") ?? (variable_struct_get(_def, "mech_type") ?? "ironclad");
                        var _atk_c = variable_struct_get(_atk, "chassis_id") ?? (variable_struct_get(_atk, "mech_type") ?? "ironclad");
                        obj_BlueprintManager.record_suit_casualty(_vic_c, _atk_c);
                    }
                    if (instance_exists(obj_NemesisManager)) {
                        var _vic_id = variable_struct_get(_def, "character_id") ?? variable_struct_get(_def, "pilot_name") ?? _def.id;
                        var _atk_id = variable_struct_get(_atk, "character_id") ?? variable_struct_get(_atk, "pilot_name") ?? "player";
                        scr_nemesis_event_dispatch(_vic_id, _atk_id, "combat_kill");

                        if (variable_struct_get(_def, "is_nemesis") == true || string_pos("NEMESIS_", _def.id) > 0) {
                            var _bounty_cr = 150000;
                            if (instance_exists(obj_GameManager)) obj_GameManager.funds += _bounty_cr;
                            add_log("[NEMESIS TRIAGE] Rival Ace neutralized! Claimed +" + string(_bounty_cr) + " Cr contract bounty!");
                        }
                    }
                }
            }
        } else {
            add_log("[MISS] " + _atk.callsign + " volley missed " + _def.callsign + "!");
        }
    }

    // Apply counter-attack damage if not resolved
    if (battle_cinematic.has_counter && !battle_cinematic.applied_counter) {
        battle_cinematic.applied_counter = true;
        if (battle_cinematic.counter_is_hit) {
            var _cpart = battle_cinematic.counter_hit_part;
            var _cdmg = battle_cinematic.counter_damage;
            var _climb = variable_struct_get(_atk.components, _cpart);
            _climb.cur = max(0, _climb.cur - _cdmg);
            add_log("[COUNTER HIT] " + _def.callsign + " retaliated against " + _atk.callsign + " " + _climb.name + " for " + string(_cdmg) + " damage!");

            if (_climb.cur <= 0 && _climb.intact) {
                _climb.intact = false;
                variable_struct_set(_atk.damaged_parts, _cpart, true);
                add_log("[CRITICAL BREACH] " + _atk.callsign + " " + _climb.name + " HAS BEEN SEVERED!");
                if (_cpart == "torso") {
                    _atk.is_destroyed = true;
                    _atk.anim_state = "destroyed";
                    _atk.anim_timer = 40;
                    add_log("[CATASTROPHIC KILL] " + _atk.callsign + " neutralized in combat!");
                }
            }
        }
    }

    // Deduct AP
    _atk.current_ap = max(0, _atk.current_ap - battle_cinematic.weapon.ap_cost);
    if (battle_cinematic.has_counter && !is_undefined(battle_cinematic.counter_weapon)) {
        _def.current_ap = max(0, _def.current_ap - battle_cinematic.counter_weapon.ap_cost);
    }

    battle_cinematic.active = false;
    battle_cinematic.timer = 0;
    battle_cinematic.shutter_y = 0;
    state = battle_cinematic.return_state;

    // Check Turn & Victory Conditions
    check_combat_resolution();
};

// 4. Draw Battle Cinematic Stage (Widescreen 2.39:1 Cutscene)
draw_battle_cinematic_stage = function() {
    if (!battle_cinematic.active) return;

    draw_set_halign(fa_left);
    draw_set_valign(fa_top);

    var _gw = display_get_gui_width();
    var _gh = display_get_gui_height();
    var _shut = battle_cinematic.shutter_y;
    var _top_y = _shut;
    var _bot_y = _gh - _shut;

    var _shake_x = (battle_cinematic.screen_shake > 0) ? random_range(-battle_cinematic.screen_shake, battle_cinematic.screen_shake) : 0;
    var _shake_y = (battle_cinematic.screen_shake > 0) ? random_range(-battle_cinematic.screen_shake, battle_cinematic.screen_shake) : 0;

    // ---------------------------------------------------------------------
    // A. PANORAMIC ENVIRONMENTAL BACKDROP
    // ---------------------------------------------------------------------
    if (battle_cinematic.is_space) {
        // Deep Space / Vacuum Void
        draw_rectangle_color(0, _top_y, _gw, _bot_y, make_color_rgb(4, 7, 16), make_color_rgb(4, 7, 16), make_color_rgb(14, 22, 42), make_color_rgb(14, 22, 42), false);

        draw_set_color(make_color_rgb(10, 36, 70));
        draw_circle(_gw * 0.72, _gh * 1.05, 420, false);
        draw_set_color(make_color_rgb(50, 160, 255));
        draw_set_alpha(0.35);
        draw_circle(_gw * 0.72, _gh * 1.05, 425, true);
        draw_circle(_gw * 0.72, _gh * 1.05, 432, true);
        draw_set_alpha(1.0);

        draw_set_color(make_color_rgb(20, 32, 54));
        draw_rectangle(240, 210, 480, 265, false);
        draw_set_color(make_color_rgb(40, 65, 105));
        draw_rectangle(240, 210, 480, 265, true);

        for (var i = 0; i < 70; i++) {
            var _sx = (i * 197 + 53) % _gw;
            var _sy = _top_y + ((i * 131 + 29) % max(1, _bot_y - _top_y));
            var _tw = 0.35 + 0.65 * abs(sin((current_time * 0.002) + i));
            draw_set_color(c_white);
            draw_set_alpha(_tw);
            draw_point(_sx, _sy);
            if (i % 6 == 0) draw_circle(_sx, _sy, 1.2, false);
        }
        draw_set_alpha(1.0);
    } else if (battle_cinematic.is_water) {
        // Coastal Harbor / Water Canal
        draw_rectangle_color(0, _top_y, _gw, _bot_y, make_color_rgb(10, 28, 48), make_color_rgb(14, 38, 64), make_color_rgb(6, 18, 32), make_color_rgb(8, 22, 38), false);
        var _wave_y = 500;
        draw_set_color(make_color_rgb(18, 55, 92));
        draw_rectangle(0, _wave_y, _gw, _bot_y, false);
    } else {
        // Terran Badlands / Granite Redoubt
        draw_rectangle_color(0, _top_y, _gw, _bot_y, make_color_rgb(22, 16, 26), make_color_rgb(32, 24, 38), make_color_rgb(14, 10, 18), make_color_rgb(18, 12, 22), false);
        draw_set_color(make_color_rgb(38, 28, 36));
        draw_rectangle(0, 480, _gw, _bot_y, false);
    }

    // CRT Scanline Authenticity Pass
    if (sprite_exists(spr_snes_crt_scanline)) {
        draw_sprite_tiled_ext(spr_snes_crt_scanline, 0, 0, _top_y, 1.0, 1.0, c_white, 0.12);
    }

    // ---------------------------------------------------------------------
    // B. MOBILE SUIT UNITS RENDERING
    // ---------------------------------------------------------------------
    var _atk = battle_cinematic.attacker;
    var _def = battle_cinematic.defender;
    var _base_ground_y = 480;

    // 1. ATTACKER FORMATION (LEFT SIDE, FACING RIGHT)
    var _ax = 340 + battle_cinematic.atk_recoil_x + _shake_x + battle_cinematic.atk_dash_x;
    var _ay = _base_ground_y + battle_cinematic.atk_recoil_y + _shake_y;
    if (battle_cinematic.is_air_atk) _ay -= (65 + sin(current_time * 0.004) * 6);
    if (battle_cinematic.is_water) _ay += 12;

    scr_draw_animated_mobile_suit(_atk, _ax, _ay, 1.30, 1, battle_cinematic.atk_anim_state, -1, _atk.image_blend, "front");

    if (_atk.squad_type == "PLATOON_3") {
        if (_atk.squad_members_count >= 2) {
            var _w1x = 210 + battle_cinematic.atk_wing1_recoil_x + _shake_x;
            var _w1y = _base_ground_y - 60 + (battle_cinematic.is_air_atk ? -60 : 0);
            scr_draw_animated_mobile_suit(_atk, _w1x, _w1y, 1.08, 1, battle_cinematic.atk_anim_state, -1, _atk.image_blend, "front");
        }
        if (_atk.squad_members_count >= 3) {
            var _w2x = 170 + battle_cinematic.atk_wing2_recoil_x + _shake_x;
            var _w2y = _base_ground_y + 45 + (battle_cinematic.is_air_atk ? -60 : 0);
            scr_draw_animated_mobile_suit(_atk, _w2x, _w2y, 1.08, 1, battle_cinematic.atk_anim_state, -1, _atk.image_blend, "front");
        }
    }

    // 2. DEFENDER FORMATION (RIGHT SIDE, FACING LEFT)
    var _dx = 1026 + battle_cinematic.def_recoil_x + _shake_x;
    var _dy = _base_ground_y + battle_cinematic.def_recoil_y + _shake_y;
    if (battle_cinematic.is_air_def) _dy -= (65 + sin(current_time * 0.004 + 1.2) * 6);
    if (battle_cinematic.is_water) _dy += 12;

    scr_draw_animated_mobile_suit(_def, _dx, _dy, 1.30, -1, battle_cinematic.def_anim_state, -1, _def.image_blend, "front");

    if (_def.squad_type == "PLATOON_3") {
        if (_def.squad_members_count >= 2) {
            var _dw1x = 1156 + battle_cinematic.def_wing1_recoil_x + _shake_x;
            var _dw1y = _base_ground_y - 60 + (battle_cinematic.is_air_def ? -60 : 0);
            scr_draw_animated_mobile_suit(_def, _dw1x, _dw1y, 1.08, -1, battle_cinematic.def_anim_state, -1, _def.image_blend, "front");
        }
        if (_def.squad_members_count >= 3) {
            var _dw2x = 1196 + battle_cinematic.def_wing2_recoil_x + _shake_x;
            var _dw2y = _base_ground_y + 45 + (battle_cinematic.is_air_def ? -60 : 0);
            scr_draw_animated_mobile_suit(_def, _dw2x, _dw2y, 1.08, -1, battle_cinematic.def_anim_state, -1, _def.image_blend, "front");
        }
    }

    // Dynamic Melee Cleavage Arc
    if (battle_cinematic.melee_cleave_timer > 0) {
        var _cleave_a = battle_cinematic.melee_cleave_timer / 24.0;
        draw_set_alpha(_cleave_a);
        draw_set_color(c_white);
        draw_line_width(1026 - 45, 420 - 55, 1026 + 45, 420 + 55, 6.0);
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_line_width(1026 - 45, 420 - 55, 1026 + 45, 420 + 55, 2.5);
        draw_set_alpha(1.0);
    }

    // --- 3. DRAW SPENT BRASS CASINGS ---
    for (var i = 0; i < array_length(battle_cinematic.casings); i++) {
        var _cs = battle_cinematic.casings[i];
        draw_set_color(make_color_rgb(255, 215, 60));
        draw_line_width(_cs.x, _cs.y, _cs.x + lengthdir_x(7, _cs.angle), _cs.y + lengthdir_y(7, _cs.angle), 2.5);
    }

    // --- 4. DRAW IN-FLIGHT PROJECTILES & TRACERS ---
    for (var i = 0; i < array_length(battle_cinematic.projectiles); i++) {
        var _pj = battle_cinematic.projectiles[i];
        if (_pj.type == "ROTARY_VULCAN") {
            draw_set_color(make_color_rgb(255, 240, 140));
            draw_line_width(_pj.cur_x - 18, _pj.cur_y, _pj.cur_x + 18, _pj.cur_y, 3.0);
            draw_set_color(c_white);
            draw_line_width(_pj.cur_x - 8, _pj.cur_y, _pj.cur_x + 8, _pj.cur_y, 1.5);
        } else if (_pj.type == "BEAM_PULSE" || string_pos("BEAM", _pj.type) > 0) {
            draw_set_color(make_color_rgb(0, 220, 255));
            draw_line_width(_pj.cur_x - 35, _pj.cur_y, _pj.cur_x + 35, _pj.cur_y, 6.0);
            draw_set_color(c_white);
            draw_line_width(_pj.cur_x - 25, _pj.cur_y, _pj.cur_x + 25, _pj.cur_y, 2.5);
        } else if (_pj.type == "MICRO_MISSILE") {
            draw_set_color(make_color_rgb(220, 225, 235));
            draw_set_alpha(0.5);
            draw_circle(_pj.cur_x - 12, _pj.cur_y, 5.0, false);
            draw_circle(_pj.cur_x - 22, _pj.cur_y, 7.0, false);
            draw_set_alpha(1.0);
            if (sprite_exists(spr_proj_missile)) {
                draw_sprite_ext(spr_proj_missile, 0, _pj.cur_x, _pj.cur_y, 1.4, 1.4, point_direction(_pj.x1, _pj.y1, _pj.x2, _pj.y2), c_white, 1.0);
            }
        } else {
            if (sprite_exists(spr_proj_cannon_120mm)) {
                draw_sprite_ext(spr_proj_cannon_120mm, 0, _pj.cur_x, _pj.cur_y, 1.5, 1.5, point_direction(_pj.x1, _pj.y1, _pj.x2, _pj.y2), c_white, 1.0);
            }
        }
    }

    // --- 5. DRAW EXPLOSION & SPARK PARTICLES ---
    for (var i = 0; i < array_length(battle_cinematic.particles); i++) {
        var _pt = battle_cinematic.particles[i];
        if (sprite_exists(_pt.sprite)) {
            draw_sprite_ext(_pt.sprite, floor(_pt.frame), _pt.x + _shake_x, _pt.y + _shake_y, _pt.scale, _pt.scale, 0, c_white, _pt.alpha);
        }
    }

    // --- 6. TARGET ACQUISITION RETICLE (PHASE 0) ---
    if (battle_cinematic.phase == 0) {
        var _pulse = 0.8 + 0.2 * sin(current_time * 0.01);
        draw_set_color(make_color_rgb(255, 60, 60));
        draw_set_alpha(_pulse);
        draw_circle(_dx, _dy - 65, 55, true);
        draw_line_width(_dx - 70, _dy - 65, _dx - 40, _dy - 65, 2.0);
        draw_line_width(_dx + 40, _dy - 65, _dx + 70, _dy - 65, 2.0);
        draw_line_width(_dx, _dy - 135, _dx, _dy - 105, 2.0);
        draw_line_width(_dx, _dy - 25, _dx, _dy + 5, 2.0);
        draw_set_color(make_color_rgb(255, 120, 120));
        draw_text(_dx - 60, _dy - 150, "TARGET ACQUIRED // LOCK");
        draw_set_alpha(1.0);
    }

    // --- 7. FLOATING DAMAGE POPUPS ---
    draw_set_halign(fa_center);
    for (var i = 0; i < array_length(battle_cinematic.popups); i++) {
        var _pop = battle_cinematic.popups[i];
        draw_set_alpha(_pop.alpha);
        draw_set_color(c_black);
        draw_text_transformed(_pop.x + 1, _pop.y + 1, _pop.text, _pop.scale, _pop.scale, 0);
        draw_set_color(_pop.color);
        draw_text_transformed(_pop.x, _pop.y, _pop.text, _pop.scale, _pop.scale, 0);
        draw_set_alpha(1.0);
    }
    draw_set_halign(fa_left);

    // ---------------------------------------------------------------------
    // C. DIEGETIC RETRO COCKPIT TELEMETRY HUD (BOTTOM LETTERBOX SHUTTER)
    // ---------------------------------------------------------------------
    // Fullscreen Screen Flash
    if (battle_cinematic.flash_alpha > 0) {
        draw_set_color(c_white);
        draw_set_alpha(battle_cinematic.flash_alpha);
        draw_rectangle(0, 0, _gw, _gh, false);
        draw_set_alpha(1.0);
    }

    // Top Letterbox Shutter
    draw_set_color(c_black);
    draw_rectangle(0, 0, _gw, _shut, false);
    draw_set_color(make_color_rgb(0, 200, 255));
    draw_line_width(0, _shut, _gw, _shut, 2.0);

    // Top Ribbon Header Information
    if (_shut >= 40) {
        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(24, _shut - 28, "THEATER: " + string_upper(battle_cinematic.theater) + " // ENGAGEMENT GRID: CLASH DUEL");
        draw_set_color(make_color_rgb(255, 215, 80));
        draw_text(_gw / 2 - 120, _shut - 28, "TACTICAL COMBAT CLASH // PHASE: " + string(battle_cinematic.phase));
    }

    // Bottom Letterbox Shutter
    draw_set_color(c_black);
    draw_rectangle(0, _bot_y, _gw, _gh, false);
    draw_set_color(make_color_rgb(0, 200, 255));
    draw_line_width(0, _bot_y, _gw, _bot_y, 2.0);

    // Render Cockpit Telemetry Decks (Left: Attacker, Right: Defender, Center: Combat Feed)
    if (_shut >= 60) {
        var _hud_h = 100;
        var _hud_y = _bot_y + 8;

        // 1. LEFT COCKPIT (ATTACKER)
        var _atk_panel_w = 460;
        scr_draw_snes_panel(16, _hud_y, _atk_panel_w, _hud_h, "", -1, false, 0.04);

        if (sprite_exists(battle_cinematic.atk_portrait)) {
            draw_sprite_ext(battle_cinematic.atk_portrait, 0, 24, _hud_y + 10, 0.40, 0.40, 0, c_white, 1.0);
            draw_set_color(make_color_rgb(0, 200, 255));
            draw_rectangle(24, _hud_y + 10, 24 + 80, _hud_y + 10 + 80, true);
        }

        // Attacker Pilot & Expression Badge
        var _expr_col = (battle_cinematic.atk_expr == "CRITICAL_SUCCESS") ? make_color_rgb(255, 220, 60) : ((battle_cinematic.atk_expr == "TAKING_HIT") ? make_color_rgb(255, 80, 80) : make_color_rgb(60, 240, 120));
        draw_set_color(_expr_col);
        draw_text(112, _hud_y + 8, "[" + battle_cinematic.atk_expr + "] " + _atk.pilot_name);
        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(112, _hud_y + 24, _atk.callsign + " | " + string_upper(_atk.mech_type));

        // Radio Bark Ticker
        var _cursor = ((current_time / 250) % 2 >= 1) ? "_" : " ";
        draw_set_color(make_color_rgb(60, 240, 120));
        draw_text(112, _hud_y + 42, "> \\"" + battle_cinematic.atk_radio_bark + _cursor + "\\"");

        // 5 Front Mission Limb Bars (Attacker)
        var _parts = ["head", "torso", "arm_left", "arm_right", "legs"];
        var _pnames = ["HD", "TR", "LA", "RA", "LG"];
        for (var p = 0; p < 5; p++) {
            var _l = variable_struct_get(_atk.components, _parts[p]);
            var _ratio = clamp(_l.cur / max(1, _l.max), 0.0, 1.0);
            var _bx = 112 + p * 68;
            var _by = _hud_y + 64;
            var _bcol = (_ratio > 0.6) ? make_color_rgb(60, 240, 100) : ((_ratio > 0.25) ? make_color_rgb(240, 200, 50) : make_color_rgb(255, 60, 60));
            if (!_l.intact || _l.cur <= 0) _bcol = make_color_rgb(80, 80, 80);

            draw_set_color(make_color_rgb(150, 170, 200));
            draw_text(_bx, _by, _pnames[p]);
            draw_set_color(make_color_rgb(20, 28, 40));
            draw_rectangle(_bx, _by + 16, _bx + 60, _by + 24, false);
            draw_set_color(_bcol);
            draw_rectangle(_bx, _by + 16, _bx + (60 * _ratio), _by + 24, false);
            draw_set_color(make_color_rgb(60, 80, 110));
            draw_rectangle(_bx, _by + 16, _bx + 60, _by + 24, true);
        }

        // 2. RIGHT COCKPIT (DEFENDER)
        var _def_panel_w = 460;
        var _def_px = _gw - _def_panel_w - 16;
        scr_draw_snes_panel(_def_px, _hud_y, _def_panel_w, _hud_h, "", -1, false, 0.04);

        if (sprite_exists(battle_cinematic.def_portrait)) {
            draw_sprite_ext(battle_cinematic.def_portrait, 0, _gw - 104, _hud_y + 10, 0.40, 0.40, 0, c_white, 1.0);
            draw_set_color(make_color_rgb(255, 80, 80));
            draw_rectangle(_gw - 104, _hud_y + 10, _gw - 104 + 80, _hud_y + 10 + 80, true);
        }

        var _d_expr_col = (battle_cinematic.def_expr == "CRIPPLED") ? make_color_rgb(255, 50, 50) : ((battle_cinematic.def_expr == "EVADED") ? make_color_rgb(80, 240, 255) : make_color_rgb(255, 140, 80));
        draw_set_color(_d_expr_col);
        draw_text(_def_px + 14, _hud_y + 8, "[" + battle_cinematic.def_expr + "] " + _def.pilot_name);
        draw_set_color(make_color_rgb(180, 210, 240));
        draw_text(_def_px + 14, _hud_y + 24, _def.callsign + " | " + string_upper(_def.mech_type));

        draw_set_color(make_color_rgb(255, 180, 60));
        draw_text(_def_px + 14, _hud_y + 42, "> \\"" + battle_cinematic.def_radio_bark + _cursor + "\\"");

        // 5 Front Mission Limb Bars (Defender)
        for (var p = 0; p < 5; p++) {
            var _l = variable_struct_get(_def.components, _parts[p]);
            var _ratio = clamp(_l.cur / max(1, _l.max), 0.0, 1.0);
            var _bx = _def_px + 14 + p * 68;
            var _by = _hud_y + 64;
            var _bcol = (_ratio > 0.6) ? make_color_rgb(60, 240, 100) : ((_ratio > 0.25) ? make_color_rgb(240, 200, 50) : make_color_rgb(255, 60, 60));
            if (!_l.intact || _l.cur <= 0) _bcol = make_color_rgb(80, 80, 80);

            if (battle_cinematic.limb_flash_timer > 0 && battle_cinematic.limb_flash_part == _parts[p]) {
                if ((battle_cinematic.limb_flash_timer % 4) < 2) _bcol = c_white;
            }

            draw_set_color(make_color_rgb(150, 170, 200));
            draw_text(_bx, _by, _pnames[p]);
            draw_set_color(make_color_rgb(20, 28, 40));
            draw_rectangle(_bx, _by + 16, _bx + 60, _by + 24, false);
            draw_set_color(_bcol);
            draw_rectangle(_bx, _by + 16, _bx + (60 * _ratio), _by + 24, false);
            draw_set_color(make_color_rgb(60, 80, 110));
            draw_rectangle(_bx, _by + 16, _bx + 60, _by + 24, true);
        }

        // 3. CENTER COMBAT COMPUTER TERMINAL
        var _cen_x = 484;
        var _cen_w = _def_px - _cen_x - 12;
        scr_draw_snes_panel(_cen_x, _hud_y, _cen_w, _hud_h, "TACTICAL TELEMETRY", make_color_rgb(0, 200, 255), false);

        draw_set_color(make_color_rgb(255, 215, 80));
        draw_text(_cen_x + 12, _hud_y + 24, "ORDNANCE: " + battle_cinematic.weapon.name);
        draw_set_color(make_color_rgb(160, 200, 240));
        draw_text(_cen_x + 12, _hud_y + 42, "HIT: " + string(battle_cinematic.hit_chance) + "% | EVADE: " + string(_def.evasion) + "%");
        draw_set_color(make_color_rgb(80, 240, 120));
        draw_text(_cen_x + 12, _hud_y + 60, "CALC DMG: " + string(battle_cinematic.mitigated_dmg) + " " + battle_cinematic.flank_tag + " " + battle_cinematic.elev_tag);

        // Fast-Forward Key hint
        var _sk_pulse = 0.7 + 0.3 * sin(current_time * 0.008);
        draw_set_color(make_color_rgb(0, 210, 255));
        draw_set_alpha(_sk_pulse);
        draw_text(_cen_x + 12, _hud_y + 78, "[SPACE / CLICK] FAST-FORWARD >>");
        draw_set_alpha(1.0);
    }
};"""

text_new = text[:start_idx] + new_cinematic_block + "\n\n" + text[end_idx:]

with open(create_path, "w", encoding="utf-8") as f:
    f.write(text_new)

print("[PASS] objects/obj_BattleManager/Create_0.gml updated with all combat refinements preserved.")
