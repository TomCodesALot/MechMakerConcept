/// @description Mobile Suit State Machine & Component Integrity System (Front Mission Style)

enum MS_STATE {
    IDLE,
    MOVING,
    FIRE_RIFLE,
    FIRE_CHAINGUN,
    FIRE_MISSILES,
    ATTACK_MELEE,
    HIT_KINETIC,
    HIT_ENERGY,
    HIT_ROCKET,
    HIT_MELEE,
    HIT_ARMLESS,
    HIT_CRIPPLED,
    HIT_LEFT_ARM_OFF,
    HIT_RIGHT_ARM_OFF,
    CRIPPLED,
    DESTROYED
}

enum MS_PART {
    HEAD,
    TORSO,
    ARM_LEFT,
    ARM_RIGHT,
    LEGS,
    BACKPACK
}

enum DAMAGE_TYPE {
    KINETIC,
    ENERGY,
    ROCKET,
    MELEE
}

/// @function scr_struct_clone(_val)
/// @description Performs a deep clone of structs and arrays to prevent prototype mutation.
/// @param {Any} _val Value to clone
/// @returns {Any} Deep-cloned copy
function scr_struct_clone(_val) {
    if (is_struct(_val)) {
        var _copy = {};
        var _keys = variable_struct_get_names(_val);
        var _len = array_length(_keys);
        for (var i = 0; i < _len; i++) {
            var _k = _keys[i];
            _copy[$ _k] = scr_struct_clone(_val[$ _k]);
        }
        return _copy;
    }
    if (is_array(_val)) {
        var _len = array_length(_val);
        var _arr = array_create(_len);
        for (var i = 0; i < _len; i++) {
            _arr[i] = scr_struct_clone(_val[i]);
        }
        return _arr;
    }
    return _val;
}

/// @function scr_ms_take_damage(_target, _part, _damage, _dmg_type)
/// @description Applies typed damage, calculates weapon recoil impulse, and triggers limb-aware hit reactions.
/// @param {Id.Instance} _target Mobile Suit instance ID
/// @param {Real} _part MS_PART enum index
/// @param {Real} _damage Amount of damage to subtract from armor/structure
/// @param {Real} [_dmg_type] DAMAGE_TYPE enum index (default KINETIC)
function scr_ms_take_damage(_target, _part, _damage, _dmg_type) {
    if (!instance_exists(_target)) return false;
    var _type = is_undefined(_dmg_type) ? DAMAGE_TYPE.KINETIC : _dmg_type;

    with (_target) {
        if (state == MS_STATE.DESTROYED) return false;

        last_damage_type = _type;
        damage_type_overlay = _type;

        // Apply physical weapon recoil impulse based on weapon used (Harsher recoil for Rocket & Melee)
        switch (_type) {
            case DAMAGE_TYPE.KINETIC:
                recoil_x = -14 * facing;
                recoil_y = -2;
                recoil_angle = -2 * facing;
                recoil_shake = 5;
                break;

            case DAMAGE_TYPE.ENERGY:
                recoil_x = -8 * facing;
                recoil_y = 0;
                recoil_angle = -1 * facing;
                recoil_shake = 7;
                break;

            case DAMAGE_TYPE.ROCKET:
                // Heavy explosive concussive blowback
                recoil_x = -32 * facing;
                recoil_y = -8;
                recoil_angle = -6 * facing;
                recoil_shake = 16;
                break;

            case DAMAGE_TYPE.MELEE:
                // Heavy lateral torque and rotational shock
                recoil_x = -24 * facing;
                recoil_y = 4;
                recoil_angle = 5 * facing;
                recoil_shake = 12;
                break;
        }

        switch (_part) {
            case MS_PART.HEAD:
                if (variable_struct_exists(suit_data.components, "head")) {
                    suit_data.components.head.armor_hp = max(0, suit_data.components.head.armor_hp - _damage);
                    if (suit_data.components.head.armor_hp <= 0 && head_intact) {
                        head_intact = false;
                        show_debug_message("[Combat] " + suit_name + " HEAD SENSOR DESTROYED! Accuracy halved.");
                    }
                }
                break;

            case MS_PART.TORSO:
                if (variable_struct_exists(suit_data.components, "torso")) {
                    suit_data.components.torso.armor_hp = max(0, suit_data.components.torso.armor_hp - _damage);
                    if (suit_data.components.torso.armor_hp <= 0 && !is_destroyed) {
                        is_destroyed = true;
                        state = MS_STATE.DESTROYED;
                        state_timer = 0;
                        recoil_x = -40 * facing;
                        recoil_shake = 25;
                        show_debug_message("[Combat] " + suit_name + " TORSO CORE BREACHED! UNIT DESTROYED!");
                        return true;
                    }
                }
                break;

            case MS_PART.ARM_LEFT:
                if (variable_struct_exists(suit_data.components, "arm_left")) {
                    suit_data.components.arm_left.armor_hp = max(0, suit_data.components.arm_left.armor_hp - _damage);
                    if (suit_data.components.arm_left.armor_hp <= 0 && arm_left_intact) {
                        arm_left_intact = false;
                        if (state == MS_STATE.FIRE_RIFLE || state == MS_STATE.ATTACK_MELEE) state = MS_STATE.IDLE;
                        show_debug_message("[Combat] " + suit_name + " LEFT ARM SEVERED! 120mm Autocannon offline.");
                    }
                }
                break;

            case MS_PART.ARM_RIGHT:
                if (variable_struct_exists(suit_data.components, "arm_right")) {
                    suit_data.components.arm_right.armor_hp = max(0, suit_data.components.arm_right.armor_hp - _damage);
                    if (suit_data.components.arm_right.armor_hp <= 0 && arm_right_intact) {
                        arm_right_intact = false;
                        if (state == MS_STATE.FIRE_CHAINGUN) state = MS_STATE.IDLE;
                        show_debug_message("[Combat] " + suit_name + " RIGHT ARM SEVERED! GAU-88 Rotary Vulcan offline.");
                    }
                }
                break;

            case MS_PART.LEGS:
                if (variable_struct_exists(suit_data.components, "legs")) {
                    suit_data.components.legs.armor_hp = max(0, suit_data.components.legs.armor_hp - _damage);
                    if (suit_data.components.legs.armor_hp <= 0 && legs_intact) {
                        legs_intact = false;
                        speed = 0;
                        if (state != MS_STATE.DESTROYED) state = MS_STATE.HIT_CRIPPLED;
                        state_timer = hit_duration;
                        show_debug_message("[Combat] " + suit_name + " LEGS DESTROYED! Unit is immobilized/crippled.");
                        return true;
                    }
                }
                break;

            case MS_PART.BACKPACK:
                if (variable_struct_exists(suit_data.components, "backpack")) {
                    suit_data.components.backpack.armor_hp = max(0, suit_data.components.backpack.armor_hp - _damage);
                    if (suit_data.components.backpack.armor_hp <= 0 && backpack_intact) {
                        backpack_intact = false;
                        if (state == MS_STATE.FIRE_MISSILES) state = MS_STATE.IDLE;
                        show_debug_message("[Combat] " + suit_name + " ARES BACKPACK DESTROYED! Missile pod disabled.");
                    }
                }
                break;
        }

        // Trigger Limb-Lost Aware Hit Reaction Animations
        if (!is_destroyed) {
            if (!legs_intact) {
                state = MS_STATE.HIT_CRIPPLED;
                state_timer = hit_duration;
            } else if (!arm_left_intact && !arm_right_intact) {
                state = MS_STATE.HIT_ARMLESS;
                state_timer = hit_duration;
            } else if (!arm_left_intact) {
                state = MS_STATE.HIT_LEFT_ARM_OFF;
                state_timer = hit_duration;
            } else if (!arm_right_intact) {
                state = MS_STATE.HIT_RIGHT_ARM_OFF;
                state_timer = hit_duration;
            } else {
                switch (_type) {
                    case DAMAGE_TYPE.KINETIC:
                        state = MS_STATE.HIT_KINETIC;
                        state_timer = hit_duration;
                        break;
                    case DAMAGE_TYPE.ENERGY:
                        state = MS_STATE.HIT_ENERGY;
                        state_timer = hit_duration;
                        break;
                    case DAMAGE_TYPE.ROCKET:
                        state = MS_STATE.HIT_ROCKET;
                        state_timer = hit_duration;
                        break;
                    case DAMAGE_TYPE.MELEE:
                        state = MS_STATE.HIT_MELEE;
                        state_timer = hit_duration;
                        break;
                }
            }
        }
    }
    return true;
}

/// @function scr_ms_trigger_attack(_target, _attack_state)
/// @description Validates component health before triggering an attack state.
/// @param {Id.Instance} _target Mobile Suit instance ID
/// @param {Real} _attack_state Desired MS_STATE attack state
/// @returns {Bool} True if attack initiated, false if blocked by destroyed components or status
function scr_ms_trigger_attack(_target, _attack_state) {
    if (!instance_exists(_target)) return false;
    with (_target) {
        if (state == MS_STATE.DESTROYED) {
            show_debug_message("[Command] Cannot attack: Unit is destroyed.");
            return false;
        }
        if (state == MS_STATE.CRIPPLED && _attack_state == MS_STATE.MOVING) {
            show_debug_message("[Command] Cannot move: Legs are destroyed.");
            return false;
        }

        switch (_attack_state) {
            case MS_STATE.FIRE_RIFLE:
                if (!arm_left_intact) {
                    show_debug_message("[Combat Error] Cannot fire Type-77 120mm Autocannon: Left arm is destroyed!");
                    return false;
                }
                state = MS_STATE.FIRE_RIFLE;
                state_timer = attack_duration_rifle;
                recoil_x = -6 * facing;
                show_debug_message("[Action] " + suit_name + " firing Type-77 120mm Solid-Slug Autocannon!");
                return true;

            case MS_STATE.FIRE_CHAINGUN:
                if (!arm_right_intact) {
                    show_debug_message("[Combat Error] Cannot fire GAU-88 Vulcan: Right arm is destroyed!");
                    return false;
                }
                state = MS_STATE.FIRE_CHAINGUN;
                state_timer = attack_duration_chaingun;
                recoil_x = -4 * facing;
                show_debug_message("[Action] " + suit_name + " firing GAU-88 Rotary Heavy Vulcan (Right Arm Only)!");
                return true;

            case MS_STATE.FIRE_MISSILES:
                if (!backpack_intact) {
                    show_debug_message("[Combat Error] Cannot launch missiles: Ares backpack pod is destroyed!");
                    return false;
                }
                state = MS_STATE.FIRE_MISSILES;
                state_timer = attack_duration_missiles;
                recoil_y = 5;
                show_debug_message("[Action] " + suit_name + " launching Ares Swarm-16 Micro-Missiles!");
                return true;

            case MS_STATE.ATTACK_MELEE:
                if (!arm_left_intact) {
                    show_debug_message("[Combat Error] Cannot perform Gun-Club Melee Strike: Left arm 120mm cannon is destroyed!");
                    return false;
                }
                state = MS_STATE.ATTACK_MELEE;
                state_timer = attack_duration_melee;
                // Forward lunge momentum
                recoil_x = 18 * facing;
                recoil_y = -3;
                recoil_angle = 3 * facing;
                show_debug_message("[Action] " + suit_name + " executing Reinforced 120mm Autocannon Gun-Club Battering Strike!");
                return true;
        }
    }
    return false;
}
