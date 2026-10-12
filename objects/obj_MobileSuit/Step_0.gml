/// @description obj_MobileSuit Step Event
// State Machine Updates, Dynamic Recoil Spring Dampening & Interactive Sandbox Testing

// 1. Process Attack & Hit State Timers
if (state == MS_STATE.FIRE_RIFLE || state == MS_STATE.FIRE_CHAINGUN || state == MS_STATE.FIRE_MISSILES || state == MS_STATE.ATTACK_MELEE ||
    state == MS_STATE.HIT_KINETIC || state == MS_STATE.HIT_ENERGY || state == MS_STATE.HIT_ROCKET || state == MS_STATE.HIT_MELEE ||
    state == MS_STATE.HIT_ARMLESS || state == MS_STATE.HIT_CRIPPLED || state == MS_STATE.HIT_LEFT_ARM_OFF || state == MS_STATE.HIT_RIGHT_ARM_OFF) {
    state_timer--;
    if (state_timer <= 0) {
        state = legs_intact ? MS_STATE.IDLE : MS_STATE.CRIPPLED;
    }
}

// 2. Physical Recoil Spring Dampening & Recovery
recoil_x = lerp(recoil_x, 0, 0.12);
recoil_y = lerp(recoil_y, 0, 0.12);
recoil_angle = lerp(recoil_angle, 0, 0.12);
recoil_shake = max(0, recoil_shake - 0.6);

// 3. Enforce Permanent Crippled / Destroyed Overrides
if (is_destroyed) {
    state = MS_STATE.DESTROYED;
    speed = 0;
} else if (!legs_intact && state == MS_STATE.IDLE) {
    state = MS_STATE.CRIPPLED;
    speed = 0;
}

// 4. Dynamic Sprite Animation Management (Health-Based Idles & Limb-Lost Damage Reactions)
var _torso_cur = suit_data.components.torso.armor_hp ?? 0;
var _hp_pct = clamp(_torso_cur / max(1, max_hp.torso), 0, 1);

switch (state) {
    case MS_STATE.DESTROYED:
        if (sprite_index != spr_ms_ironclad_destroyed) {
            sprite_index = spr_ms_ironclad_destroyed;
            image_index = 0;
            image_speed = 0;
        }
        break;

    case MS_STATE.CRIPPLED:
        if (sprite_index != spr_ms_ironclad_crippled_idle) {
            sprite_index = spr_ms_ironclad_crippled_idle;
            image_speed = 1.0;
        }
        break;

    case MS_STATE.ATTACK_MELEE:
        if (sprite_index != spr_ms_ironclad_attack_melee) {
            sprite_index = spr_ms_ironclad_attack_melee;
            image_index = 0;
            image_speed = 1.0;
        }
        break;

    case MS_STATE.HIT_CRIPPLED:
        if (sprite_index != spr_ms_ironclad_hit_crippled) {
            sprite_index = spr_ms_ironclad_hit_crippled;
            image_index = 0;
            image_speed = 1.0;
        }
        break;

    case MS_STATE.HIT_ARMLESS:
        if (sprite_index != spr_ms_ironclad_hit_armless) {
            sprite_index = spr_ms_ironclad_hit_armless;
            image_index = 0;
            image_speed = 1.0;
        }
        break;

    case MS_STATE.HIT_LEFT_ARM_OFF:
        if (sprite_index != spr_ms_ironclad_hit_left_arm_off) {
            sprite_index = spr_ms_ironclad_hit_left_arm_off;
            image_index = 0;
            image_speed = 1.0;
        }
        break;

    case MS_STATE.HIT_RIGHT_ARM_OFF:
        if (sprite_index != spr_ms_ironclad_hit_right_arm_off) {
            sprite_index = spr_ms_ironclad_hit_right_arm_off;
            image_index = 0;
            image_speed = 1.0;
        }
        break;

    case MS_STATE.HIT_KINETIC:
        if (sprite_index != spr_ms_ironclad_hit_kinetic) {
            sprite_index = spr_ms_ironclad_hit_kinetic;
            image_index = 0;
            image_speed = 1.0;
        }
        break;

    case MS_STATE.HIT_ENERGY:
        if (sprite_index != spr_ms_ironclad_hit_energy) {
            sprite_index = spr_ms_ironclad_hit_energy;
            image_index = 0;
            image_speed = 1.0;
        }
        break;

    case MS_STATE.HIT_ROCKET:
        if (sprite_index != spr_ms_ironclad_hit_rocket) {
            sprite_index = spr_ms_ironclad_hit_rocket;
            image_index = 0;
            image_speed = 1.0;
        }
        break;

    case MS_STATE.HIT_MELEE:
        if (sprite_index != spr_ms_ironclad_hit_melee) {
            sprite_index = spr_ms_ironclad_hit_melee;
            image_index = 0;
            image_speed = 1.0;
        }
        break;

    case MS_STATE.FIRE_RIFLE:
        if (sprite_index != spr_ms_ironclad_fire_rifle) {
            sprite_index = spr_ms_ironclad_fire_rifle;
            image_index = 0;
            image_speed = 1.0;
        }
        break;

    case MS_STATE.FIRE_CHAINGUN:
        if (sprite_index != spr_ms_ironclad_fire_chaingun) {
            sprite_index = spr_ms_ironclad_fire_chaingun;
            image_index = 0;
            image_speed = 1.0;
        }
        break;

    case MS_STATE.FIRE_MISSILES:
        if (sprite_index != spr_ms_ironclad_fire_missiles) {
            sprite_index = spr_ms_ironclad_fire_missiles;
            image_index = 0;
            image_speed = 1.0;
        }
        break;

    case MS_STATE.IDLE:
    default:
        // 1. Check limb loss first
        if (!arm_left_intact && !arm_right_intact) {
            // Both arms severed: Armless animated idle with sparking shoulder wiring
            if (sprite_index != spr_ms_ironclad_damage_both_arms) {
                sprite_index = spr_ms_ironclad_damage_both_arms;
                image_speed = 1.0;
            }
        } else if (!arm_left_intact) {
            // Left arm severed: Animated idle with sparking left shoulder and active right rotary
            if (sprite_index != spr_ms_ironclad_damage_left_arm) {
                sprite_index = spr_ms_ironclad_damage_left_arm;
                image_speed = 1.0;
            }
        } else if (!arm_right_intact) {
            // Right arm severed: Animated idle with sparking right shoulder and active left 120mm cannon
            if (sprite_index != spr_ms_ironclad_damage_right_arm) {
                sprite_index = spr_ms_ironclad_damage_right_arm;
                image_speed = 1.0;
            }
        } else {
            // 2. Health-based idle body state adjustments
            if (_hp_pct < 0.35) {
                if (sprite_index != spr_ms_ironclad_idle_critical) {
                    sprite_index = spr_ms_ironclad_idle_critical;
                    image_speed = 1.0;
                }
            } else if (_hp_pct < 0.75) {
                if (sprite_index != spr_ms_ironclad_idle_damaged) {
                    sprite_index = spr_ms_ironclad_idle_damaged;
                    image_speed = 1.0;
                }
            } else {
                if (sprite_index != spr_ms_ironclad_idle) {
                    sprite_index = spr_ms_ironclad_idle;
                    image_speed = 1.0;
                }
            }
        }
        break;
}

// 5. Interactive Sandbox Testing Controls
// Key [F] or [TAB]: Toggle Directional Facing (Front Mission Style)
if (keyboard_check_pressed(ord("F")) || keyboard_check_pressed(vk_tab)) {
    facing *= -1;
    last_combat_msg = (facing == 1) ? "ORIENTATION: Facing RIGHT (Attacker Position)" : "ORIENTATION: Facing LEFT (Defender Position)";
    msg_fade = 1.0;
}

// Key [V]: Toggle Front Mission Dual Unit Duel Scene Preview
if (keyboard_check_pressed(ord("V"))) {
    duel_mode_enabled = !duel_mode_enabled;
    last_combat_msg = duel_mode_enabled ? "DUEL MODE ENABLED: Front Mission 3 Opponent Deployed!" : "DUEL MODE DISABLED: Solo unit view.";
    msg_fade = 1.0;
}

// Key [H]: Cycle Health Tiers (100% Pristine -> 60% Damaged -> 25% Critical -> 100%)
if (keyboard_check_pressed(ord("H"))) {
    damage_type_overlay = undefined;
    var _cur = suit_data.components.torso.armor_hp;
    if (_cur > max_hp.torso * 0.75) {
        suit_data.components.torso.armor_hp = floor(max_hp.torso * 0.55);
        last_combat_msg = "HEALTH TIER: Damaged (55% HP) - Sputtering exhaust & joint sparks.";
    } else if (_cur > max_hp.torso * 0.35) {
        suit_data.components.torso.armor_hp = floor(max_hp.torso * 0.25);
        last_combat_msg = "HEALTH TIER: Critical (25% HP) - Billowing black smoke & electrical arcing!";
    } else {
        suit_data.components.torso.armor_hp = max_hp.torso;
        last_combat_msg = "HEALTH TIER: Pristine (100% HP) - Clean exhaust plumes & steady reactor.";
    }
    msg_fade = 1.0;
}

// Keys [1 - 3, C]: Weapon Firing & Melee Tests
if (keyboard_check_pressed(ord("1"))) {
    if (scr_ms_trigger_attack(id, MS_STATE.FIRE_RIFLE)) {
        last_combat_msg = "FIRING Type-77 120mm Autocannon (Left Arm)!";
    } else {
        last_combat_msg = "ACTION FAILED: Left arm is destroyed!";
    }
    msg_fade = 1.0;
}

if (keyboard_check_pressed(ord("2"))) {
    if (scr_ms_trigger_attack(id, MS_STATE.FIRE_CHAINGUN)) {
        last_combat_msg = "FIRING GAU-88 Heavy Vulcan (Right Arm ONLY)! Left cannon resting.";
    } else {
        last_combat_msg = "ACTION FAILED: Right arm is destroyed!";
    }
    msg_fade = 1.0;
}

if (keyboard_check_pressed(ord("3"))) {
    if (scr_ms_trigger_attack(id, MS_STATE.FIRE_MISSILES)) {
        last_combat_msg = "LAUNCHING Ares Swarm-16 Micro-Missiles (Backpack Pods)!";
    } else {
        last_combat_msg = "ACTION FAILED: Ares backpack pod is destroyed!";
    }
    msg_fade = 1.0;
}

// Key [C] or [M]: Melee Gun-Club Battering Strike
if (keyboard_check_pressed(ord("C")) || keyboard_check_pressed(ord("M"))) {
    if (scr_ms_trigger_attack(id, MS_STATE.ATTACK_MELEE)) {
        last_combat_msg = "MELEE ATTACK: 120mm Cannon Gun-Club Battering Swing executed!";
    } else {
        last_combat_msg = "ACTION FAILED: Left arm 120mm cannon is destroyed!";
    }
    msg_fade = 1.0;
}

// Keys [4 - 7]: Specialized Damage Type Impact Tests (With Harsh Recoil)
if (keyboard_check_pressed(ord("4"))) {
    scr_ms_take_damage(id, MS_PART.TORSO, 75, DAMAGE_TYPE.KINETIC);
    last_combat_msg = "IMPACT: Kinetic Solid Slugs! Snappy pushback & ricochet sparks.";
    msg_fade = 1.0;
}

if (keyboard_check_pressed(ord("5"))) {
    scr_ms_take_damage(id, MS_PART.TORSO, 90, DAMAGE_TYPE.ENERGY);
    last_combat_msg = "IMPACT: Energy Plasma Beam! High-frequency shudder & molten slag.";
    msg_fade = 1.0;
}

if (keyboard_check_pressed(ord("6"))) {
    scr_ms_take_damage(id, MS_PART.TORSO, 120, DAMAGE_TYPE.ROCKET);
    last_combat_msg = "IMPACT: Rocket Blast! HARSH CONCUSSIVE BLOWBACK & smoke cloud!";
    msg_fade = 1.0;
}

if (keyboard_check_pressed(ord("7"))) {
    scr_ms_take_damage(id, MS_PART.TORSO, 140, DAMAGE_TYPE.MELEE);
    last_combat_msg = "IMPACT: Thermal Blade Slash! HARSH LATERAL TORQUE & hydraulic breach!";
    msg_fade = 1.0;
}

// Keys [8, 9, B, 0, -, =]: Component Severing & Limbless Tests
if (keyboard_check_pressed(ord("8"))) {
    scr_ms_take_damage(id, MS_PART.ARM_LEFT, 9999, DAMAGE_TYPE.KINETIC);
    last_combat_msg = "CRITICAL HIT: Left Arm Severed! Single-limb animated idle active.";
    msg_fade = 1.0;
}

if (keyboard_check_pressed(ord("9"))) {
    scr_ms_take_damage(id, MS_PART.ARM_RIGHT, 9999, DAMAGE_TYPE.KINETIC);
    last_combat_msg = "CRITICAL HIT: Right Arm Severed! Single-limb animated idle active.";
    msg_fade = 1.0;
}

if (keyboard_check_pressed(ord("B"))) {
    scr_ms_take_damage(id, MS_PART.ARM_LEFT, 9999, DAMAGE_TYPE.KINETIC);
    scr_ms_take_damage(id, MS_PART.ARM_RIGHT, 9999, DAMAGE_TYPE.KINETIC);
    last_combat_msg = "CATASTROPHIC HIT: BOTH ARMS SEVERED! Unit is now ARMLESS.";
    msg_fade = 1.0;
}

if (keyboard_check_pressed(ord("0"))) {
    scr_ms_take_damage(id, MS_PART.LEGS, 9999, DAMAGE_TYPE.ROCKET);
    last_combat_msg = "CRITICAL HIT: Hydraulic Legs Crippled! Unit forced to KNEEL.";
    msg_fade = 1.0;
}

if (keyboard_check_pressed(ord("-")) || keyboard_check_pressed(vk_subtract)) {
    scr_ms_take_damage(id, MS_PART.BACKPACK, 9999, DAMAGE_TYPE.ENERGY);
    last_combat_msg = "CRITICAL HIT: Ares Backpack Destroyed! Missile pod offline.";
    msg_fade = 1.0;
}

if (keyboard_check_pressed(ord("=")) || keyboard_check_pressed(vk_add)) {
    scr_ms_take_damage(id, MS_PART.TORSO, 9999, DAMAGE_TYPE.ROCKET);
    last_combat_msg = "CORE MELTDOWN: Torso Fusion Core Breached! Unit Destroyed.";
    msg_fade = 1.0;
}

// Key [R]: Full Repair / Reset
if (keyboard_check_pressed(ord("R"))) {
    head_intact = true;
    arm_left_intact = true;
    arm_right_intact = true;
    legs_intact = true;
    backpack_intact = true;
    is_destroyed = false;
    last_damage_type = undefined;
    damage_type_overlay = undefined;
    recoil_x = 0;
    recoil_y = 0;
    recoil_angle = 0;
    recoil_shake = 0;
    state = MS_STATE.IDLE;
    state_timer = 0;
    sprite_index = spr_ms_ironclad_idle;
    image_speed = 1.0;
    image_index = 0;

    suit_data.components.head.armor_hp = max_hp.head;
    suit_data.components.torso.armor_hp = max_hp.torso;
    suit_data.components.arm_left.armor_hp = max_hp.arm_left;
    suit_data.components.arm_right.armor_hp = max_hp.arm_right;
    suit_data.components.legs.armor_hp = max_hp.legs;
    suit_data.components.backpack.armor_hp = max_hp.backpack;

    last_combat_msg = "Unit fully repaired and re-armed. Pristine stance restored.";
    msg_fade = 1.0;
}

// Key [ESC]: Return to PMC HQ Terminal Hub
if (keyboard_check_pressed(vk_escape)) {
    if (room_exists(rm_hq_terminal)) {
        room_goto(rm_hq_terminal);
    }
}
