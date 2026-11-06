/// @description obj_DebugManager Step Event
// Drives Debug Input State, Cinematic Duel Choreography & Animation Stepping

// Toast Timer Countdown
if (debug_toast_timer > 0) debug_toast_timer--;

// 1. Universal Hotkey Trigger (F7 or backtick ` / ~)
var _toggle = keyboard_check_pressed(vk_f7)
           || keyboard_check_pressed(vk_f6)
           || keyboard_check_pressed(vk_f8)
           || keyboard_check_pressed(vk_f12)
           || keyboard_check_pressed(192)
           || keyboard_check_pressed(222)
           || keyboard_check_pressed(220)
           || (keyboard_check(vk_control) && keyboard_check_pressed(ord("D")));
if (_toggle) {
    is_open = !is_open;
    scr_audio_play_ui(is_open ? "boot" : "cancel");
    if (!is_open && clash_cinematic.active) {
        clash_cinematic.active = false;
    }
}

if (!is_open && !clash_cinematic.active) exit;

// 2. Escape closes debug panel or finishes cinematic clash
if (keyboard_check_pressed(vk_escape)) {
    if (clash_cinematic.active) {
        clash_cinematic.active = false;
        scr_audio_play_ui("cancel");
    } else {
        is_open = false;
        scr_audio_play_ui("cancel");
    }
    keyboard_clear(vk_escape);
}

// Global Tab Switching Hotkeys (1-4 & Tab)
if (!clash_cinematic.active && is_open) {
    if (keyboard_check_pressed(ord("1"))) { active_debug_tab = 0; scr_audio_play_ui("tab"); }
    else if (keyboard_check_pressed(ord("2"))) { active_debug_tab = 1; scr_audio_play_ui("tab"); }
    else if (keyboard_check_pressed(ord("3"))) { active_debug_tab = 2; scr_audio_play_ui("tab"); }
    else if (keyboard_check_pressed(ord("4"))) { active_debug_tab = 3; scr_audio_play_ui("tab"); }
    else if (keyboard_check_pressed(vk_tab)) { active_debug_tab = (active_debug_tab + 1) % 4; scr_audio_play_ui("tab"); }
}

// TAB 1: MECH BUILDER & FORGE STEP CONTROLS
if (!clash_cinematic.active && is_open && active_debug_tab == 1) {
    builder_subimg += 0.15;

    // Slot navigation
    if (keyboard_check_pressed(vk_down)) {
        builder_selected_slot = (builder_selected_slot + 1) % 7;
        scr_audio_play_ui("click");
    } else if (keyboard_check_pressed(vk_up)) {
        builder_selected_slot = (builder_selected_slot - 1 + 7) % 7;
        scr_audio_play_ui("click");
    }

    // Part cycle in selected slot
    if (keyboard_check_pressed(vk_right)) {
        if (builder_selected_slot == 0) builder_head_idx = (builder_head_idx + 1) % array_length(builder_parts_catalog.heads);
        else if (builder_selected_slot == 1) builder_torso_idx = (builder_torso_idx + 1) % array_length(builder_parts_catalog.torsos);
        else if (builder_selected_slot == 2) builder_arms_idx = (builder_arms_idx + 1) % array_length(builder_parts_catalog.arms);
        else if (builder_selected_slot == 3) builder_legs_idx = (builder_legs_idx + 1) % array_length(builder_parts_catalog.legs);
        else if (builder_selected_slot == 4) builder_bp_idx = (builder_bp_idx + 1) % array_length(builder_parts_catalog.backpacks);
        else if (builder_selected_slot == 5) builder_wp_idx = (builder_wp_idx + 1) % array_length(builder_parts_catalog.weapons);
        else if (builder_selected_slot == 6) builder_alloy_idx = (builder_alloy_idx + 1) % array_length(builder_alloys);
        scr_audio_play_ui("click");
    } else if (keyboard_check_pressed(vk_left)) {
        if (builder_selected_slot == 0) builder_head_idx = (builder_head_idx - 1 + array_length(builder_parts_catalog.heads)) % array_length(builder_parts_catalog.heads);
        else if (builder_selected_slot == 1) builder_torso_idx = (builder_torso_idx - 1 + array_length(builder_parts_catalog.torsos)) % array_length(builder_parts_catalog.torsos);
        else if (builder_selected_slot == 2) builder_arms_idx = (builder_arms_idx - 1 + array_length(builder_parts_catalog.arms)) % array_length(builder_parts_catalog.arms);
        else if (builder_selected_slot == 3) builder_legs_idx = (builder_legs_idx - 1 + array_length(builder_parts_catalog.legs)) % array_length(builder_parts_catalog.legs);
        else if (builder_selected_slot == 4) builder_bp_idx = (builder_bp_idx - 1 + array_length(builder_parts_catalog.backpacks)) % array_length(builder_parts_catalog.backpacks);
        else if (builder_selected_slot == 5) builder_wp_idx = (builder_wp_idx - 1 + array_length(builder_parts_catalog.weapons)) % array_length(builder_parts_catalog.weapons);
        else if (builder_selected_slot == 6) builder_alloy_idx = (builder_alloy_idx - 1 + array_length(builder_alloys)) % array_length(builder_alloys);
        scr_audio_play_ui("click");
    }

    // Space/Enter cycles preview pose
    if (keyboard_check_pressed(vk_space) || keyboard_check_pressed(vk_enter)) {
        var _poses = ["idle", "boost", "fire", "melee"];
        var _cur_p_idx = 0;
        for (var p = 0; p < array_length(_poses); p++) {
            if (builder_anim_state == _poses[p]) { _cur_p_idx = p; break; }
        }
        builder_anim_state = _poses[(_cur_p_idx + 1) % array_length(_poses)];
        scr_audio_play_ui("click");
    }
}

// TAB 2: ASTEROID MINING & EXTRACTION STEP CONTROLS
if (!clash_cinematic.active && is_open && active_debug_tab == 2) {
    // Cool drill heat
    mining_drill_heat = max(0.0, mining_drill_heat - 0.35);
    if (mining_drill_timer > 0) mining_drill_timer--;
    else mining_drill_active = false;

    // Update floating particles
    for (var p = array_length(mining_particles) - 1; p >= 0; p--) {
        var _pt = mining_particles[p];
        _pt.y += _pt.vy;
        _pt.life -= 1;
        if (_pt.life <= 0) array_delete(mining_particles, p, 1);
    }

    // Up/Down changes selected node
    var _m_nodes = get_debug_mining_nodes();
    if (array_length(_m_nodes) > 0) {
        if (keyboard_check_pressed(vk_down)) {
            mining_selected_idx = (mining_selected_idx + 1) % array_length(_m_nodes);
            scr_audio_play_ui("click");
        } else if (keyboard_check_pressed(vk_up)) {
            mining_selected_idx = (mining_selected_idx - 1 + array_length(_m_nodes)) % array_length(_m_nodes);
            scr_audio_play_ui("click");
        }
    }

    // Space or Enter fires mining pulse
    if (keyboard_check_pressed(vk_space) || keyboard_check_pressed(vk_enter)) {
        pulse_mine_node();
    }
}

// Keyboard Navigation & Hotkeys for Proving Ground
if (!clash_cinematic.active && is_open && active_debug_tab == 0) {
    var _atk_list = get_filtered_units(atk_faction_idx, atk_cat_idx);
    if (array_length(_atk_list) > 0) {
        if (keyboard_check_pressed(vk_down)) {
            atk_filtered_idx = (atk_filtered_idx + 1) % array_length(_atk_list);
            scr_audio_play_ui("click");
        } else if (keyboard_check_pressed(vk_up)) {
            atk_filtered_idx = (atk_filtered_idx - 1 + array_length(_atk_list)) % array_length(_atk_list);
            scr_audio_play_ui("click");
        }

        var _cur_u = _atk_list[clamp(atk_filtered_idx, 0, array_length(_atk_list) - 1)];
        var _active_states = ["idle"];
        if (_cur_u.category != "CUSTOM_MECH") {
            if (_cur_u.weapon_class == "BALLISTIC") array_push(_active_states, "fire_rifle");
            else if (_cur_u.weapon_class == "ROTARY_VULCAN") array_push(_active_states, "fire_chaingun");
            else if (_cur_u.weapon_class == "BEAM_PULSE") array_push(_active_states, "fire_beam");
            else if (_cur_u.weapon_class == "MICRO_MISSILE") array_push(_active_states, "fire_missiles");
            else array_push(_active_states, "fire_rifle");

            if (variable_struct_exists(_cur_u, "sprites") && is_struct(_cur_u.sprites)) {
                if (variable_struct_exists(_cur_u.sprites, "melee") && _cur_u.sprites.melee != -1) array_push(_active_states, "melee");
                if (variable_struct_exists(_cur_u.sprites, "boost") && _cur_u.sprites.boost != -1) array_push(_active_states, "boost");
                if (variable_struct_exists(_cur_u.sprites, "damaged") && _cur_u.sprites.damaged != -1) array_push(_active_states, "damaged");
                if (variable_struct_exists(_cur_u.sprites, "destroyed") && _cur_u.sprites.destroyed != -1) array_push(_active_states, "destroyed");
            }
        } else {
            _active_states = ["idle", "fire_rifle", "fire_chaingun", "fire_beam", "fire_missiles", "melee", "boost", "damaged", "destroyed"];
        }

        if (keyboard_check_pressed(vk_right)) {
            anim_state_idx = (anim_state_idx + 1) % array_length(_active_states);
            scr_audio_play_ui("click");
        } else if (keyboard_check_pressed(vk_left)) {
            anim_state_idx = (anim_state_idx - 1 + array_length(_active_states)) % array_length(_active_states);
            scr_audio_play_ui("click");
        }

        if (keyboard_check_pressed(vk_enter) || keyboard_check_pressed(vk_space)) {
            launch_full_cinematic_clash();
        }
    }
}

// -------------------------------------------------------------------------
// 3. FULL CINEMATIC CLASH DUEL STATE MACHINE UPDATE
// -------------------------------------------------------------------------
if (clash_cinematic.active) {
    clash_cinematic.timer++;
    var _t = clash_cinematic.timer;

    // Fast-forward / Skip on Space or Enter
    if (keyboard_check_pressed(vk_space) || keyboard_check_pressed(vk_enter)) {
        if (clash_cinematic.phase < 3) {
            clash_cinematic.phase = 3;
            clash_cinematic.timer = 180;
        } else {
            clash_cinematic.active = false;
            exit;
        }
    }

    // Screen Shake Dampening
    clash_cinematic.screen_shake = max(0.0, clash_cinematic.screen_shake - 0.7);

    // Smooth Recoil Dampening
    clash_cinematic.atk_recoil_x = lerp(clash_cinematic.atk_recoil_x, 0, 0.15);
    clash_cinematic.atk_recoil_y = lerp(clash_cinematic.atk_recoil_y, 0, 0.15);
    clash_cinematic.def_recoil_x = lerp(clash_cinematic.def_recoil_x, 0, 0.15);
    clash_cinematic.def_recoil_y = lerp(clash_cinematic.def_recoil_y, 0, 0.15);
    if (clash_cinematic.weapon_class != "MELEE" && clash_cinematic.weapon_class != "BEAM_LANCE") {
        clash_cinematic.atk_dash_x = lerp(clash_cinematic.atk_dash_x, 0, 0.12);
    }

    // Phase 0: Cinema Bars Slide Down & Target Lock (t: 0 to 40)
    if (clash_cinematic.phase == 0) {
        clash_cinematic.shutter_y = min(75, clash_cinematic.shutter_y + 4.5);
        if (_t >= 40) {
            clash_cinematic.phase = 1;
            // Initiate Attack
            var _w_class = clash_cinematic.weapon_class;
            if (_w_class == "BEAM_LANCE") {
                clash_cinematic.atk_anim_state = "boost";
                clash_cinematic.atk_dash_x = 0;
                scr_audio_play_sfx(snd_mech_boost, 1.05, 0.05);
            } else if (_w_class == "MELEE") {
                clash_cinematic.atk_anim_state = "melee";
                clash_cinematic.atk_dash_x = 0;
                scr_audio_play_sfx(snd_mech_boost, 0.95, 0.05);
            } else if (_w_class == "ROTARY_VULCAN") {
                // Rotary vulcan rapid-fire chatter sequence begins with spinup lock & brace (t: 40 to 47)
                clash_cinematic.atk_anim_state = "fire_chaingun";
                clash_cinematic.atk_subimg = 0; // Frame 0: Spinup & Stance Brace!
                scr_audio_play_ui("select");
            } else if (_w_class == "BEAM_PULSE") {
                clash_cinematic.atk_anim_state = "fire_beam";
                clash_cinematic.atk_recoil_x = -8;
                array_push(clash_cinematic.projectiles, {
                    x1: 360, y1: 450, x2: 1010, y2: 450,
                    cur_x: 360, cur_y: 450, speed: 48, type: "BEAM_PULSE"
                });
            } else if (_w_class == "MICRO_MISSILE") {
                clash_cinematic.atk_anim_state = "fire_missiles";
                clash_cinematic.atk_recoil_x = -6;
                for (var m = 0; m < 3; m++) {
                    array_push(clash_cinematic.projectiles, {
                        x1: 360, y1: 440, x2: 1010, y2: 445,
                        cur_x: 360, cur_y: 440, speed: 24, type: "MICRO_MISSILE",
                        arc_offset: (m - 1) * 35
                    });
                }
            } else if (_w_class == "BALLISTIC") {
                // Ballistic 3-round burst sequence begins with raising the rifle (t: 40 to 51)
                clash_cinematic.atk_anim_state = "fire_rifle";
                clash_cinematic.atk_subimg = 0; // Frame 0: Raising In-Between!
                scr_audio_play_ui("select");
            } else {
                clash_cinematic.atk_anim_state = "fire_rifle";
                clash_cinematic.atk_recoil_x = -18;
                var _muzzle_x = 360 + 70;
                var _muzzle_y = 480 - 125;
                var _def_target_y = 480 - 90;
                array_push(clash_cinematic.projectiles, {
                    x1: _muzzle_x, y1: _muzzle_y, x2: 1010, y2: _def_target_y,
                    cur_x: _muzzle_x, cur_y: _muzzle_y, speed: 32, type: "BALLISTIC"
                });
            }

            if (_w_class != "BEAM_LANCE" && _w_class != "MELEE" && _w_class != "BALLISTIC" && _w_class != "ROTARY_VULCAN") {
                scr_audio_play_weapon(_w_class);
            }
        }
    }
    // Phase 1: Attack Flying / Lunging (t: 40 to 95+)
    else if (clash_cinematic.phase == 1) {
        var _w_class = clash_cinematic.weapon_class;

        if (_w_class == "BEAM_LANCE") {
            // Stage 1: High-Speed Vernier Charge
            if (_t >= 40 && _t < 73) {
                var _chg_prog = clamp((_t - 40) / 33.0, 0, 1);
                clash_cinematic.atk_dash_x = lerp(0, 540, _chg_prog);
                clash_cinematic.atk_anim_state = "boost";
                if (_t % 3 == 0) {
                    array_push(clash_cinematic.particles, {
                        x: 360 + clash_cinematic.atk_dash_x - 30,
                        y: 450 + random_range(-12, 12),
                        sprite: spr_fx_explosion,
                        frame: 2.0, spd: 0.35,
                        scale: random_range(0.6, 0.9),
                        alpha: 0.8
                    });
                }
            }
            // Stage 2: Impale / Piercing Stab into Defender
            else if (_t == 73) {
                clash_cinematic.atk_dash_x = 540;
                clash_cinematic.atk_anim_state = "melee";
                clash_cinematic.screen_shake = 10.0;
                clash_cinematic.def_anim_state = "hit";
                clash_cinematic.def_recoil_x = 12;
                scr_audio_play_weapon("blade");
                scr_audio_play_impact("kinetic", false);
                for (var sp = 0; sp < 6; sp++) {
                    array_push(clash_cinematic.particles, {
                        x: 1010 - 20 + random_range(-15, 15),
                        y: 445 + random_range(-15, 15),
                        sprite: spr_fx_explosion,
                        frame: 1.0, spd: 0.3,
                        scale: random_range(0.8, 1.2),
                        alpha: 0.9
                    });
                }
            }
            // Stage 2b: Lance remains buried in chest, charging plasma
            else if (_t > 73 && _t < 103) {
                clash_cinematic.atk_dash_x = 540;
                clash_cinematic.atk_anim_state = "melee";
                clash_cinematic.def_anim_state = "hit";
                clash_cinematic.def_recoil_x = 12;
            }
            // Stage 3: Point-Blank Plasma Burst Detonation & Violent Knockback!
            else if (_t == 103) {
                clash_cinematic.phase = 2;
                clash_cinematic.screen_shake = 22.0;
                clash_cinematic.def_anim_state = "damaged";
                clash_cinematic.def_recoil_x = 75; // Heavy knockback shove
                clash_cinematic.def_hp = max(0, clash_cinematic.def_hp - clash_cinematic.mitigated_dmg);
                scr_audio_play_weapon("beam");
                scr_audio_play_impact("plasma", true);
                for (var p = 0; p < 12; p++) {
                    array_push(clash_cinematic.particles, {
                        x: 1010 - 15 + random_range(-30, 30),
                        y: 445 + random_range(-30, 30),
                        sprite: spr_fx_explosion,
                        frame: 0.0, spd: 0.25,
                        scale: random_range(1.6, 2.4),
                        alpha: 1.0
                    });
                }
                array_push(clash_cinematic.popups, {
                    x: 1010, y: 410,
                    text: "- " + string(clash_cinematic.mitigated_dmg) + " DMG [PLASMA BURST]",
                    col: make_color_rgb(0, 240, 255),
                    timer: 70, vy: -1.2
                });
            }
            // Stage 4: Reverse Vernier Kickback & Recovery
            else if (_t > 103) {
                clash_cinematic.atk_dash_x = lerp(clash_cinematic.atk_dash_x, 0, 0.12);
                if (_t >= 125) clash_cinematic.atk_anim_state = "idle";
            }
        } else if (_w_class == "MELEE") {
            var _is_centurion = (clash_cinematic.attacker.id == "ms_terran_centurion_02");
            if (_is_centurion) {
                // Centurion: Spartan Tower Shield Bash into Hydraulic Spiked Ramming Prow Breach (6 frames)
                // Stage 1: Linebreaker Thruster Charge Dash (t: 40 to 69)
                if (_t >= 40 && _t < 70) {
                    var _chg_prog = clamp((_t - 40) / 30.0, 0, 1);
                    clash_cinematic.atk_dash_x = lerp(0, 480, _chg_prog);
                    clash_cinematic.atk_anim_state = "boost"; // Dedicated 4-frame Linebreaker boost!
                    clash_cinematic.atk_subimg = -1;
                    if (_t == 40 && sound_exists(snd_mech_boost)) {
                        scr_audio_play_sfx(snd_mech_boost, 1.05, 0.05);
                    }
                }
                // Stage 2: Spartan Tower Shield Impact Slam (t: 70 to 74)
                else if (_t >= 70 && _t < 75) {
                    clash_cinematic.atk_dash_x = 480;
                    clash_cinematic.atk_anim_state = "melee";
                    clash_cinematic.atk_subimg = (_t < 72) ? 0 : 1; // F0: Linebreaker Brace -> F1: Tower Shield Slam!
                    if (_t == 72) {
                        clash_cinematic.screen_shake = 12.0;
                        clash_cinematic.def_anim_state = "hit";
                        clash_cinematic.def_recoil_x = 20;
                        scr_audio_play_weapon("blade");
                        scr_audio_play_impact("kinetic", false);
                        for (var sp = 0; sp < 8; sp++) {
                            array_push(clash_cinematic.particles, {
                                x: 1010 - 20 + random_range(-15, 15),
                                y: 445 + random_range(-15, 15),
                                sprite: spr_fx_explosion,
                                frame: 1.0, spd: 0.35,
                                scale: random_range(0.8, 1.2),
                                alpha: 0.85
                            });
                        }
                    }
                }
                // Stage 3: Hydraulic Prow Priming & Target Pin (t: 75 to 80)
                else if (_t >= 75 && _t < 81) {
                    clash_cinematic.atk_dash_x = 480;
                    clash_cinematic.atk_anim_state = "melee";
                    clash_cinematic.atk_subimg = 2; // F2: Hydraulic Prow Priming & Pressure Build
                }
                // Stage 4: Explosive Pneumatic Thrust (t: 81 to 84)
                else if (_t >= 81 && _t < 85) {
                    clash_cinematic.atk_dash_x = 480;
                    clash_cinematic.atk_anim_state = "melee";
                    clash_cinematic.atk_subimg = 3; // F3: Explosive Pneumatic Spike Thrust
                    if (_t == 81) scr_audio_play_weapon("blade");
                }
                // Stage 5: Catastrophic Armor Breach Impact! (t: 85)
                else if (_t == 85) {
                    clash_cinematic.atk_dash_x = 480;
                    clash_cinematic.atk_anim_state = "melee";
                    clash_cinematic.atk_subimg = 4; // F4: Catastrophic Armor Breach Impact!
                    clash_cinematic.phase = 2;
                    clash_cinematic.screen_shake = 26.0;
                    clash_cinematic.def_anim_state = "damaged";
                    clash_cinematic.def_recoil_x = 60; // Heavy knockback shove
                    clash_cinematic.def_hp = max(0, clash_cinematic.def_hp - clash_cinematic.mitigated_dmg);
                    scr_audio_play_weapon("BALLISTIC");
                    scr_audio_play_impact("kinetic", true);
                    for (var p = 0; p < 18; p++) {
                        array_push(clash_cinematic.particles, {
                            x: 1010 + random_range(-35, 35),
                            y: 450 + random_range(-35, 35),
                            sprite: spr_fx_explosion,
                            frame: 0.0, spd: 0.25,
                            scale: random_range(1.5, 2.5),
                            alpha: 1.0
                        });
                    }
                    array_push(clash_cinematic.popups, {
                        x: 1010, y: 410,
                        text: "- " + string(clash_cinematic.mitigated_dmg) + " DMG [THERMAL GLADIUS]",
                        col: make_color_rgb(255, 180, 40),
                        timer: 70, vy: -1.2
                    });
                }
                // Stage 6: Steam Venting & Recovery (t: 86 to 112)
                else if (_t >= 86 && _t < 113) {
                    clash_cinematic.atk_dash_x = 480;
                    clash_cinematic.atk_anim_state = "melee";
                    clash_cinematic.atk_subimg = 5; // F5: Hydraulic Venting & Steam Puff
                }
                // Stage 7: Reset & Return (t: 113+)
                else if (_t >= 113) {
                    clash_cinematic.atk_dash_x = lerp(clash_cinematic.atk_dash_x, 0, 0.12);
                    if (_t >= 138) {
                        clash_cinematic.atk_anim_state = "idle";
                        clash_cinematic.atk_subimg = -1;
                    }
                }
            } else {
                // Canonical GHA-07 Ironclad: Cybernetic Demolition Mace & Shield (8 frames)
                // Stage 1: High-Speed Thruster Charge Dash (t: 40 to 69)
                if (_t >= 40 && _t < 70) {
                    var _chg_prog = clamp((_t - 40) / 30.0, 0, 1);
                    clash_cinematic.atk_dash_x = lerp(0, 480, _chg_prog);
                    clash_cinematic.atk_anim_state = "boost"; // Dedicated forward charging animation!
                    clash_cinematic.atk_subimg = -1;
                    if (_t == 40 && sound_exists(snd_mech_boost)) {
                        scr_audio_play_sfx(snd_mech_boost, 1.0, 0.05);
                    }
                }
                // Stage 2: Shield Rush & Bash (t: 70 to 74)
                else if (_t >= 70 && _t < 75) {
                    clash_cinematic.atk_dash_x = 480;
                    clash_cinematic.atk_anim_state = "melee";
                    clash_cinematic.atk_subimg = (_t < 72) ? 0 : 1; // F0: Shield Guard Rush -> F1: Shield Bash Collision!
                    if (_t == 72) {
                        clash_cinematic.screen_shake = 10.0;
                        clash_cinematic.def_anim_state = "hit";
                        clash_cinematic.def_recoil_x = 18;
                        scr_audio_play_weapon("blade");
                        scr_audio_play_impact("kinetic", false);
                        for (var sp = 0; sp < 6; sp++) {
                            array_push(clash_cinematic.particles, {
                                x: 1010 - 20 + random_range(-15, 15),
                                y: 445 + random_range(-15, 15),
                                sprite: spr_fx_explosion,
                                frame: 1.0, spd: 0.35,
                                scale: random_range(0.8, 1.2),
                                alpha: 0.85
                            });
                        }
                    }
                }
                // Stage 3: Mace Draw & Deep Overhead Windup (t: 75 to 83)
                else if (_t >= 75 && _t < 84) {
                    clash_cinematic.atk_dash_x = 480;
                    clash_cinematic.atk_anim_state = "melee";
                    clash_cinematic.atk_subimg = (_t < 79) ? 2 : 3; // F2: Mace Draw -> F3: Deep Overhead Windup!
                }
                // Stage 4: High-Velocity Cybernetic Mace Power Swing (t: 84 to 86)
                else if (_t >= 84 && _t < 87) {
                    clash_cinematic.atk_dash_x = 480;
                    clash_cinematic.atk_anim_state = "melee";
                    clash_cinematic.atk_subimg = (_t == 84) ? 4 : 5; // F4: Swing Acceleration -> F5: Max Velocity Arc!
                    if (_t == 84) scr_audio_play_weapon("blade");
                }
                // Stage 5: Crushing Cybernetic Mace Impact Smash! (t: 87)
                else if (_t == 87) {
                    clash_cinematic.atk_dash_x = 480;
                    clash_cinematic.atk_anim_state = "melee";
                    clash_cinematic.atk_subimg = 6; // Frame 6: Catastrophic Cybernetic Impact Smash!
                    clash_cinematic.phase = 2;
                    clash_cinematic.screen_shake = 24.0;
                    clash_cinematic.def_anim_state = "damaged";
                    clash_cinematic.def_recoil_x = 52; // Heavy knockback shove
                    clash_cinematic.def_hp = max(0, clash_cinematic.def_hp - clash_cinematic.mitigated_dmg);
                    scr_audio_play_weapon("BALLISTIC");
                    scr_audio_play_impact("kinetic", true);
                    for (var p = 0; p < 16; p++) {
                        array_push(clash_cinematic.particles, {
                            x: 1010 + random_range(-35, 35),
                            y: 450 + random_range(-35, 35),
                            sprite: spr_fx_explosion,
                            frame: 0.0, spd: 0.25,
                            scale: random_range(1.4, 2.4),
                            alpha: 1.0
                        });
                    }
                    array_push(clash_cinematic.popups, {
                        x: 1010, y: 410,
                        text: "- " + string(clash_cinematic.mitigated_dmg) + " DMG [CYBERNETIC MACE]",
                        col: make_color_rgb(0, 240, 255),
                        timer: 70, vy: -1.2
                    });
                }
                // Stage 6: Ground Follow-Through & Coolant Venting (t: 88 to 112)
                else if (_t >= 88 && _t < 113) {
                    clash_cinematic.atk_dash_x = 480;
                    clash_cinematic.atk_anim_state = "melee";
                    clash_cinematic.atk_subimg = (_t < 98) ? 6 : 7; // Frame 6 impact follow-through -> Frame 7 coolant steam vent
                }
                // Stage 7: Reset & Return (t: 113+)
                else if (_t >= 113) {
                    clash_cinematic.atk_dash_x = lerp(clash_cinematic.atk_dash_x, 0, 0.12);
                    if (_t >= 138) {
                        clash_cinematic.atk_anim_state = "idle";
                        clash_cinematic.atk_subimg = -1;
                    }
                }
            }
        } else if (_w_class == "BALLISTIC") {
            // Stage 1: Raise Rifle into Shooting Brace (t: 40 to 51)
            if (_t >= 40 && _t < 52) {
                clash_cinematic.atk_anim_state = "fire_rifle";
                clash_cinematic.atk_subimg = 0; // Frame 0: Raising In-Between!
            }
            // Stage 2: 3-Round Kinetic Burst with timed casing ejections
            // Round 1 (t: 52 to 59)
            else if (_t == 52) {
                clash_cinematic.atk_anim_state = "fire_rifle";
                clash_cinematic.atk_subimg = 1; // Frame 1: Muzzle Blast!
                clash_cinematic.atk_recoil_x = -12;
                clash_cinematic.screen_shake = 5.0;
                var _mx = 360 + 70;
                var _my = 480 - 125;
                array_push(clash_cinematic.projectiles, {
                    x1: _mx, y1: _my, x2: 1010, y2: 480 - 95,
                    cur_x: _mx, cur_y: _my, speed: 36, type: "BALLISTIC"
                });
                array_push(clash_cinematic.casings, {
                    x: 360 + 20, y: 480 - 130,
                    vx: random_range(-3.5, -2.0), vy: random_range(-6.5, -4.5),
                    angle: random(360), rot_spd: random_range(16, 28)
                });
                scr_audio_play_weapon("BALLISTIC");
            }
            else if (_t >= 55 && _t < 60) {
                clash_cinematic.atk_subimg = 2; // Frame 2: Recoil blowback & smoke
            }
            // Round 2 (t: 60 to 67)
            else if (_t == 60) {
                clash_cinematic.atk_anim_state = "fire_rifle";
                clash_cinematic.atk_subimg = 1; // Frame 1: Muzzle Blast!
                clash_cinematic.atk_recoil_x = -14;
                clash_cinematic.screen_shake = 6.0;
                var _mx = 360 + 70;
                var _my = 480 - 125;
                array_push(clash_cinematic.projectiles, {
                    x1: _mx, y1: _my, x2: 1010, y2: 480 - 88,
                    cur_x: _mx, cur_y: _my, speed: 36, type: "BALLISTIC"
                });
                array_push(clash_cinematic.casings, {
                    x: 360 + 20, y: 480 - 130,
                    vx: random_range(-3.5, -2.0), vy: random_range(-6.5, -4.5),
                    angle: random(360), rot_spd: random_range(16, 28)
                });
                scr_audio_play_weapon("BALLISTIC");
            }
            else if (_t >= 63 && _t < 68) {
                clash_cinematic.atk_subimg = 2; // Frame 2: Recoil blowback & smoke
            }
            // Round 3 (t: 68 to 75)
            else if (_t == 68) {
                clash_cinematic.atk_anim_state = "fire_rifle";
                clash_cinematic.atk_subimg = 1; // Frame 1: Muzzle Blast!
                clash_cinematic.atk_recoil_x = -18;
                clash_cinematic.screen_shake = 8.0;
                var _mx = 360 + 70;
                var _my = 480 - 125;
                array_push(clash_cinematic.projectiles, {
                    x1: _mx, y1: _my, x2: 1010, y2: 480 - 82,
                    cur_x: _mx, cur_y: _my, speed: 36, type: "BALLISTIC"
                });
                array_push(clash_cinematic.casings, {
                    x: 360 + 20, y: 480 - 130,
                    vx: random_range(-4.0, -2.5), vy: random_range(-7.0, -5.0),
                    angle: random(360), rot_spd: random_range(18, 32)
                });
                scr_audio_play_weapon("BALLISTIC");
            }
            else if (_t >= 71 && _t < 80) {
                clash_cinematic.atk_subimg = 2; // Frame 2: Heavy recoil blowback
            }
            // Stage 3: Burst Impact on Defender (t: 80 to 95)
            else if (_t == 80) {
                clash_cinematic.phase = 2;
                clash_cinematic.screen_shake = 16.0;
                clash_cinematic.def_anim_state = "damaged";
                clash_cinematic.def_recoil_x = 24;
                clash_cinematic.def_hp = max(0, clash_cinematic.def_hp - clash_cinematic.mitigated_dmg);
                scr_audio_play_impact("kinetic", true);
                for (var p = 0; p < 10; p++) {
                    array_push(clash_cinematic.particles, {
                        x: 1010 + random_range(-25, 25),
                        y: 450 + random_range(-25, 25),
                        sprite: spr_fx_explosion,
                        frame: 0.0, spd: 0.25,
                        scale: random_range(1.2, 1.8),
                        alpha: 1.0
                    });
                }
                array_push(clash_cinematic.popups, {
                    x: 1010, y: 410,
                    text: "- " + string(clash_cinematic.mitigated_dmg) + " DMG",
                    col: make_color_rgb(255, 120, 40),
                    timer: 70, vy: -1.2
                });
            }
            // Stage 4: Lower Rifle Back to Neutral (t: 96 to 120)
            else if (_t >= 96 && _t < 118) {
                clash_cinematic.atk_subimg = 3; // Frame 3: Lowering In-Between!
            }
            else if (_t >= 118) {
                clash_cinematic.atk_anim_state = "idle";
                clash_cinematic.atk_subimg = -1;
            }
        } else if (_w_class == "ROTARY_VULCAN") {
            // Stage 1: High-Torque Spinup Lock & Stance Brace (t: 40 to 47)
            if (_t >= 40 && _t < 48) {
                clash_cinematic.atk_anim_state = "fire_chaingun";
                clash_cinematic.atk_subimg = 0; // Frame 0: Spinup & Stance Brace!
            }
            // Stage 2: Rapid-Fire 35mm Rotary Chain Vulcan Chatter (t: 48 to 78)
            else if (_t >= 48 && _t <= 78) {
                clash_cinematic.atk_anim_state = "fire_chaingun";
                // Rapidly cycle rotating firing frames (Frames 1, 2, 3, 4)
                clash_cinematic.atk_subimg = 1 + (((_t - 48) div 2) % 4);
                if ((_t - 48) % 3 == 0) {
                    clash_cinematic.atk_recoil_x = -6 + random_range(-2, 2);
                    clash_cinematic.screen_shake = max(clash_cinematic.screen_shake, 4.0);

                    var _mx = 360 + 75;
                    var _my = 480 - 100 + random_range(-4, 4);
                    var _target_y = 480 - 90 + random_range(-14, 14);

                    array_push(clash_cinematic.projectiles, {
                        x1: _mx, y1: _my, x2: 1010 + random_range(-12, 12), y2: _target_y,
                        cur_x: _mx, cur_y: _my, speed: 40, type: "ROTARY_VULCAN"
                    });

                    // Spent 35mm brass casing tumbling from breach
                    array_push(clash_cinematic.casings, {
                        x: 360 + 40 + random_range(-3, 3), y: 480 - 110 + random_range(-3, 3),
                        vx: random_range(-4.5, -2.5), vy: random_range(-7.0, -4.5),
                        angle: random(360), rot_spd: random_range(20, 36)
                    });

                    scr_audio_play_weapon("ROTARY_VULCAN");
                }
            }
            // Stage 3: Saturated Bullet Impact Storm on Defender (t: 79)
            else if (_t == 79) {
                clash_cinematic.phase = 2;
                clash_cinematic.screen_shake = 16.0;
                clash_cinematic.def_anim_state = "damaged";
                clash_cinematic.def_recoil_x = 28;
                clash_cinematic.def_hp = max(0, clash_cinematic.def_hp - clash_cinematic.mitigated_dmg);

                for (var p = 0; p < 14; p++) {
                    array_push(clash_cinematic.particles, {
                        x: 1010 + random_range(-35, 35),
                        y: 450 + random_range(-35, 35),
                        sprite: spr_fx_explosion,
                        frame: 0.0, spd: 0.28,
                        scale: random_range(1.0, 1.8),
                        alpha: 1.0
                    });
                }

                array_push(clash_cinematic.popups, {
                    x: 1010, y: 410,
                    text: "- " + string(clash_cinematic.mitigated_dmg) + " DMG [35mm VULCAN]",
                    col: make_color_rgb(255, 180, 50),
                    timer: 70, vy: -1.2
                });

                scr_audio_play_impact("ROTARY_VULCAN", true);
            }
            // Stage 4: Barrel Spin-Down & Smoke Venting (t: 80 to 115)
            else if (_t >= 80 && _t < 116) {
                // Transition through spin-down frame 5 (cherry-red heat) and frame 6 (smoke dissipation)
                clash_cinematic.atk_subimg = (_t < 98) ? 5 : 6;
            }
            // Stage 5: Reset to Neutral Idle (t >= 116)
            else if (_t >= 116) {
                clash_cinematic.atk_anim_state = "idle";
                clash_cinematic.atk_subimg = -1;
            }
        } else {
            // Ranged projectile impacts
            if (_t >= 95) {
                clash_cinematic.phase = 2;
                clash_cinematic.screen_shake = 14.0;
                clash_cinematic.def_anim_state = "damaged";
                clash_cinematic.def_recoil_x = 18;
                clash_cinematic.def_hp = max(0, clash_cinematic.def_hp - clash_cinematic.mitigated_dmg);

                for (var p = 0; p < 8; p++) {
                    array_push(clash_cinematic.particles, {
                        x: 1010 + random_range(-35, 35),
                        y: 450 + random_range(-35, 35),
                        sprite: spr_fx_explosion,
                        frame: 0.0, spd: 0.25,
                        scale: random_range(1.2, 1.8),
                        alpha: 1.0
                    });
                }

                array_push(clash_cinematic.popups, {
                    x: 1010, y: 410,
                    text: "- " + string(clash_cinematic.mitigated_dmg) + " DMG",
                    col: make_color_rgb(255, 120, 40),
                    timer: 70, vy: -1.2
                });

                scr_audio_play_impact(clash_cinematic.weapon_class, true);
            }
        }
    }
    // Phase 2: Impact & Counter Preparation (t: 95 to 155)
    else if (clash_cinematic.phase == 2) {
        if (_t >= 155) {
            clash_cinematic.phase = 3;
            if (clash_cinematic.has_counter && clash_cinematic.def_hp > 0) {
                var _def_w_class = (variable_struct_exists(clash_cinematic.defender, "weapon_class")) ? clash_cinematic.defender.weapon_class : "BALLISTIC";
                if (_def_w_class == "ROTARY_VULCAN") {
                    clash_cinematic.def_anim_state = "fire_chaingun";
                    scr_audio_play_weapon("ROTARY_VULCAN");
                } else if (_def_w_class == "BEAM_PULSE") {
                    clash_cinematic.def_anim_state = "fire_beam";
                    scr_audio_play_weapon("BEAM_PULSE");
                } else {
                    clash_cinematic.def_anim_state = "fire_rifle";
                    scr_audio_play_weapon("BALLISTIC");
                }
                clash_cinematic.def_recoil_x = 12;
                clash_cinematic.atk_recoil_x = -14;
                clash_cinematic.atk_anim_state = "damaged";
                clash_cinematic.atk_hp = max(0, clash_cinematic.atk_hp - clash_cinematic.counter_damage);

                array_push(clash_cinematic.popups, {
                    x: 360, y: 410,
                    text: "- " + string(clash_cinematic.counter_damage) + " COUNTER",
                    col: make_color_rgb(0, 240, 255),
                    timer: 70, vy: -1.2
                });

                scr_audio_play_impact(_def_w_class, false);
            }
        }
    }
    // Phase 3: Resolution & Exit Preparation (t: 155 to 220)
    else if (clash_cinematic.phase == 3) {
        if (_t >= 220) {
            clash_cinematic.phase = 4;
        }
    }
    // Phase 4: Shutter Retreat & Return to Debug Menu
    else if (clash_cinematic.phase == 4) {
        clash_cinematic.shutter_y = max(0, clash_cinematic.shutter_y - 4.5);
        if (clash_cinematic.shutter_y <= 0) {
            clash_cinematic.active = false;
        }
    }

    // Update in-flight projectiles
    for (var i = array_length(clash_cinematic.projectiles) - 1; i >= 0; i--) {
        var _pj = clash_cinematic.projectiles[i];
        _pj.cur_x += _pj.speed;
        if (_pj.cur_x >= _pj.x2) {
            array_delete(clash_cinematic.projectiles, i, 1);
        }
    }

    // Update tumbling brass casings
    for (var i = array_length(clash_cinematic.casings) - 1; i >= 0; i--) {
        var _cs = clash_cinematic.casings[i];
        _cs.x += _cs.vx;
        _cs.y += _cs.vy;
        _cs.vy += 0.35;
        _cs.angle += _cs.rot_spd;
        if (_cs.y > 600) array_delete(clash_cinematic.casings, i, 1);
    }

    // Update particles
    for (var i = array_length(clash_cinematic.particles) - 1; i >= 0; i--) {
        var _pt = clash_cinematic.particles[i];
        _pt.frame += _pt.spd;
        if (_pt.frame >= sprite_get_number(_pt.sprite)) {
            array_delete(clash_cinematic.particles, i, 1);
        }
    }

    // Update damage popups
    for (var i = array_length(clash_cinematic.popups) - 1; i >= 0; i--) {
        var _pp = clash_cinematic.popups[i];
        _pp.y += _pp.vy;
        _pp.timer--;
        if (_pp.timer <= 0) array_delete(clash_cinematic.popups, i, 1);
    }

    exit;
}

// -------------------------------------------------------------------------
// 4. LIVE INTERACTIVE ANIMATION STAGE STEPPING
// -------------------------------------------------------------------------
var _cur_spd = anim_speeds[anim_speed_idx];
if (!is_paused || step_frame_req) {
    subimg_atk += (0.15 * _cur_spd);
    subimg_def += (0.15 * _cur_spd);
    step_frame_req = false;
}
