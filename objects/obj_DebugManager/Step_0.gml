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
    clash_cinematic.atk_dash_x = lerp(clash_cinematic.atk_dash_x, 0, 0.12);

    // Phase 0: Cinema Bars Slide Down & Target Lock (t: 0 to 40)
    if (clash_cinematic.phase == 0) {
        clash_cinematic.shutter_y = min(75, clash_cinematic.shutter_y + 4.5);
        if (_t >= 40) {
            clash_cinematic.phase = 1;
            // Initiate Attack
            var _w_class = clash_cinematic.weapon_class;
            if (_w_class == "ROTARY_VULCAN") {
                clash_cinematic.atk_anim_state = "fire_chaingun";
                clash_cinematic.atk_recoil_x = -12;
                for (var v = 0; v < 4; v++) {
                    array_push(clash_cinematic.projectiles, {
                        x1: 360, y1: 450 + (v * 4) - 6,
                        x2: 1010, y2: 450 + (v * 4) - 6,
                        cur_x: 360 + (v * 40), cur_y: 450 + (v * 4) - 6,
                        speed: 34, type: "ROTARY_VULCAN"
                    });
                }
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
            } else if (_w_class == "MELEE") {
                clash_cinematic.atk_anim_state = "melee";
                clash_cinematic.atk_dash_x = 420;
            } else {
                clash_cinematic.atk_anim_state = "fire_rifle";
                clash_cinematic.atk_recoil_x = -18;
                array_push(clash_cinematic.projectiles, {
                    x1: 360, y1: 450, x2: 1010, y2: 450,
                    cur_x: 360, cur_y: 450, speed: 30, type: "BALLISTIC"
                });
            }

            if (_w_class == "BALLISTIC" || _w_class == "ROTARY_VULCAN") {
                for (var c = 0; c < 3; c++) {
                    array_push(clash_cinematic.casings, {
                        x: 380 + random_range(-10, 10),
                        y: 440 + random_range(-10, 10),
                        vx: random_range(-3, -1),
                        vy: random_range(-6, -3),
                        angle: random(360),
                        rot_spd: random_range(12, 28)
                    });
                }
            }

            scr_audio_play_weapon(_w_class);
        }
    }
    // Phase 1: Attack Flying / Lunging (t: 40 to 95)
    else if (clash_cinematic.phase == 1) {
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
    // Phase 2: Impact & Counter Preparation (t: 95 to 155)
    else if (clash_cinematic.phase == 2) {
        if (_t >= 155) {
            clash_cinematic.phase = 3;
            if (clash_cinematic.has_counter && clash_cinematic.def_hp > 0) {
                clash_cinematic.def_anim_state = "fire_rifle";
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

                scr_audio_play_weapon("BALLISTIC");
                scr_audio_play_impact("BALLISTIC", false);
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
