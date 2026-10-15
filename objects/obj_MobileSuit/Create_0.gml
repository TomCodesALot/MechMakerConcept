/// @description obj_MobileSuit Create Event
// Mobile Suit Instance Controller with Front Mission Modular Damage, Dynamic Recoil & Directional Facing

// 1. Sprite & Animation Setup (Unified 3/4 Isometric Perspective)
sprite_index = spr_ms_ironclad_idle;
image_speed = 1.0;
image_index = 0;

// 2. Directional Facing (Front Mission Duel System: 1 = Facing Right [Attacker], -1 = Facing Left [Defender])
facing = 1;
duel_mode_enabled = false;

// 3. Dynamic Physical Recoil Physics
recoil_x = 0;
recoil_y = 0;
recoil_angle = 0;
recoil_shake = 0;

// 4. State Machine Variables
state = MS_STATE.IDLE;
state_timer = 0;
attack_duration_rifle = 30;    // 0.5s at 60fps
attack_duration_chaingun = 45; // 0.75s at 60fps
attack_duration_missiles = 60; // 1.0s at 60fps
attack_duration_melee = 32;    // ~0.53s at 60fps (Gun-club swing)
hit_duration = 24;             // 0.4s at 60fps

// 5. Component Condition Flags
head_intact = true;
arm_left_intact = true;
arm_right_intact = true;
legs_intact = true;
backpack_intact = true;
is_destroyed = false;

// 6. Damage State Tracking
last_damage_type = undefined;
damage_type_overlay = undefined;

// 7. Blueprint Data Binding (Isolated Instance Clone)
suit_data = undefined;
suit_name = "GHA-07 Ironclad";

if (instance_exists(obj_GameManager)) {
    var _master_bp = obj_GameManager.get_blueprint("bp_ms_ironclad_07");
    if (!is_undefined(_master_bp) && is_struct(_master_bp)) {
        suit_data = scr_struct_clone(_master_bp);
        suit_name = suit_data[$ "name"] ?? "GHA-07 Ironclad";
        show_debug_message("[obj_MobileSuit] Instance created with cloned blueprint: " + suit_name);
    }
}

if (is_undefined(suit_data)) {
    var _loaded = scr_load_blueprint("bp_ms_ironclad_07.json");
    suit_data = !is_undefined(_loaded) ? scr_struct_clone(_loaded) : {};
}

// Bind dynamic sprite asset if present on blueprint or catalog
if (is_struct(suit_data) && variable_struct_exists(suit_data, "sprite_asset") && sprite_exists(suit_data.sprite_asset)) {
    sprite_index = suit_data.sprite_asset;
}

// Cache maximum HP values for HUD display
max_hp = {
    head: suit_data.components.head.armor_hp ?? 160,
    torso: suit_data.components.torso.armor_hp ?? 650,
    arm_left: suit_data.components.arm_left.armor_hp ?? 400,
    arm_right: suit_data.components.arm_right.armor_hp ?? 400,
    legs: suit_data.components.legs.armor_hp ?? 650,
    backpack: suit_data.components.backpack.armor_hp ?? 220
};

last_combat_msg = "Ready for deployment. Facing RIGHT (Front Mission Attacker position).";
msg_fade = 1.0;
