/// @description obj_MobileSuit Draw Event
// Renders active 3/4 isometric side battle sprite, directional facing, dynamic recoil shake, and Front Mission HUD

// 1. Determine State Description and Indicator Color
var _draw_col = c_lime;
var _state_text = "STANDBY / PRISTINE IDLE";
var _torso_cur = suit_data.components.torso.armor_hp ?? 0;
var _hp_pct = clamp(_torso_cur / max(1, max_hp.torso), 0, 1);

switch (state) {
    case MS_STATE.IDLE:
        if (!arm_left_intact && !arm_right_intact) {
            _draw_col = make_color_rgb(255, 120, 100);
            _state_text = "ARMLESS IDLE (BOTH ARMS SEVERED)";
        } else if (!arm_left_intact) {
            _draw_col = make_color_rgb(255, 180, 80);
            _state_text = "SINGLE-LIMB IDLE (LEFT ARM SEVERED)";
        } else if (!arm_right_intact) {
            _draw_col = make_color_rgb(255, 180, 80);
            _state_text = "SINGLE-LIMB IDLE (RIGHT ARM SEVERED)";

        } else if (_hp_pct < 0.35) {
            _draw_col = make_color_rgb(255, 80, 80);
            _state_text = "CRITICAL IDLE (BLACK SMOKE & ELECTRICAL ARCS)";
        } else if (_hp_pct < 0.75) {
            _draw_col = make_color_rgb(255, 190, 80);
            _state_text = "DAMAGED IDLE (SPUTTERING EXHAUST & SPARKS)";
        } else {
            _draw_col = make_color_rgb(120, 220, 100);
            _state_text = "PRISTINE IDLE (EXHAUST VENTING ACTIVE)";
        }
        break;

    case MS_STATE.ATTACK_MELEE:
        _draw_col = make_color_rgb(255, 120, 40);
        _state_text = "MELEE: 120MM CANNON GUN-CLUB STRIKE!";
        break;

    case MS_STATE.FIRE_RIFLE:
        _draw_col = c_orange;
        _state_text = "FIRING TYPE-77 120MM CANNON";
        break;

    case MS_STATE.FIRE_CHAINGUN:
        _draw_col = c_yellow;
        _state_text = "FIRING GAU-88 ROTARY VULCAN (R. ARM ONLY)";
        break;

    case MS_STATE.FIRE_MISSILES:
        _draw_col = c_white;
        _state_text = "LAUNCHING SWARM-16 MISSILES";
        break;

    case MS_STATE.HIT_KINETIC:
        _draw_col = make_color_rgb(255, 230, 100);
        _state_text = "RECOIL: KINETIC AP ARMOR IMPACT";
        break;

    case MS_STATE.HIT_ENERGY:
        _draw_col = make_color_rgb(100, 220, 255);
        _state_text = "RECOIL: ENERGY BEAM SHUDDER & ARCS";
        break;

    case MS_STATE.HIT_ROCKET:
        _draw_col = make_color_rgb(255, 80, 30);
        _state_text = "HARSH RECOIL: CONCUSSIVE BLAST BLOWBACK!";
        break;

    case MS_STATE.HIT_MELEE:
        _draw_col = make_color_rgb(255, 50, 120);
        _state_text = "HARSH RECOIL: THERMAL BLADE LATERAL TORQUE!";
        break;

    case MS_STATE.HIT_ARMLESS:
        _draw_col = make_color_rgb(255, 140, 100);
        _state_text = "RECOIL: ARMLESS CHASSIS STRUCK!";
        break;

    case MS_STATE.HIT_CRIPPLED:
        _draw_col = make_color_rgb(255, 100, 50);
        _state_text = "RECOIL: GROUNDED KNEELING BLAST IMPACT!";
        break;

    case MS_STATE.HIT_LEFT_ARM_OFF:
    case MS_STATE.HIT_RIGHT_ARM_OFF:
        _draw_col = make_color_rgb(255, 160, 60);
        _state_text = "RECOIL: SEVERED HARDPOINT STRUCK!";
        break;

    case MS_STATE.CRIPPLED:
        _draw_col = make_color_rgb(255, 140, 40);
        _state_text = "CRIPPLED IDLE (HYDRAULICS DESTROYED)";
        break;

    case MS_STATE.DESTROYED:
        _draw_col = c_red;
        _state_text = "WRECKED (FUSION CORE BREACH)";
        break;
}

// 2. Render Ground Shadow at Foot Origin
draw_set_color(c_black);
draw_set_alpha(0.4);
draw_ellipse(x - 55, y - 8, x + 55, y + 10, false);
draw_set_alpha(1.0);

// 3. Render High-Fidelity 3/4 Isometric Mech Sprite with Recoil Shake and Directional Facing
var _shake_x = (recoil_shake > 0) ? random_range(-recoil_shake, recoil_shake) : 0;
var _shake_y = (recoil_shake > 0) ? random_range(-recoil_shake, recoil_shake) : 0;
var _draw_x = x + recoil_x + _shake_x;
var _draw_y = y + recoil_y + _shake_y;
var _draw_angle = recoil_angle * facing;

if (sprite_exists(sprite_index)) {
    draw_sprite_ext(sprite_index, image_index, _draw_x, _draw_y, facing, 1.0, _draw_angle, c_white, 1.0);
}

// 4. Duel Arena Mode Preview: Render Opponent Unit Facing the Player Unit (Front Mission 3 Style)
if (duel_mode_enabled) {
    var _opp_x = x + (facing * 420);
    var _opp_y = y;
    
    // Opponent shadow
    draw_set_color(c_black);
    draw_set_alpha(0.4);
    draw_ellipse(_opp_x - 55, _opp_y - 8, _opp_x + 55, _opp_y + 10, false);
    draw_set_alpha(1.0);
    
    // Opponent mech facing opposite direction
    if (sprite_exists(spr_ms_ironclad_idle)) {
        draw_sprite_ext(spr_ms_ironclad_idle, (image_index + 2) mod 4, _opp_x, _opp_y, -facing, 1.0, 0, make_color_rgb(255, 180, 180), 0.95);
    }
    
    draw_set_color(make_color_rgb(255, 120, 120));
    draw_text(_opp_x - 70, _opp_y - 265, "[HOSTILE OPFOR MECH]");
    draw_text(_opp_x - 70, _opp_y - 248, "<- TARGET LOCKED ->");
}

// 5. Overhead Unit Callout & State Badge
var _facing_badge = (facing == 1) ? "-> FACING RIGHT [ATTACKER]" : "<- FACING LEFT [DEFENDER]";
draw_set_color(c_white);
draw_text(x - 75, y - 280, suit_name + " (" + _facing_badge + ")");

draw_set_color(_draw_col);
draw_text(x - 75, y - 262, "[" + _state_text + "]");

// 6. Front Mission Component Health Display
var _hud_x = 40;
var _hud_y = 35;

draw_set_color(c_dkgray);
draw_rectangle(_hud_x - 10, _hud_y - 10, _hud_x + 380, _hud_y + 245, false);
draw_set_color(c_white);
draw_rectangle(_hud_x - 10, _hud_y - 10, _hud_x + 380, _hud_y + 245, true);

draw_text(_hud_x, _hud_y, "=== MOBILE SUIT INTEGRITY ===");

var _draw_part_hp = function(_name, _cur, _max, _intact, _px, _py) {
    var _pct = clamp(_cur / max(1, _max), 0, 1);
    var _col = _intact ? (_pct > 0.4 ? c_lime : c_yellow) : c_red;
    var _status = _intact ? (string(_cur) + " / " + string(_max)) : "DESTROYED";

    draw_set_color(c_white);
    draw_text(_px, _py, _name + ": ");
    draw_set_color(_col);
    draw_text(_px + 120, _py, _status);

    draw_set_color(c_black);
    draw_rectangle(_px + 230, _py + 2, _px + 350, _py + 12, false);
    if (_intact) {
        draw_set_color(_col);
        draw_rectangle(_px + 230, _py + 2, _px + 230 + (120 * _pct), _py + 12, false);
    }
};

_draw_part_hp("TORSO CORE", suit_data.components.torso.armor_hp, max_hp.torso, !is_destroyed, _hud_x, _hud_y + 28);
_draw_part_hp("HEAD SENSOR", suit_data.components.head.armor_hp, max_hp.head, head_intact, _hud_x, _hud_y + 50);
_draw_part_hp("LEFT ARM", suit_data.components.arm_left.armor_hp, max_hp.arm_left, arm_left_intact, _hud_x, _hud_y + 72);
_draw_part_hp("RIGHT ARM", suit_data.components.arm_right.armor_hp, max_hp.arm_right, arm_right_intact, _hud_x, _hud_y + 94);
_draw_part_hp("HYDR. LEGS", suit_data.components.legs.armor_hp, max_hp.legs, legs_intact, _hud_x, _hud_y + 116);
_draw_part_hp("ARES PACK", suit_data.components.backpack.armor_hp, max_hp.backpack, backpack_intact, _hud_x, _hud_y + 138);

// Health-Based Body Idle Tier Display
var _tier_name = "PRISTINE (Smooth Venting & Core Glow)";
var _tier_col = c_lime;
if (_hp_pct < 0.35) {
    _tier_name = "CRITICAL (Heavy Black Smoke & Arcing)";
    _tier_col = make_color_rgb(255, 80, 80);
} else if (_hp_pct < 0.75) {
    _tier_name = "DAMAGED (Sputtering Smoke & Sparks)";
    _tier_col = make_color_rgb(255, 190, 80);
}
draw_set_color(c_white);
draw_text(_hud_x, _hud_y + 165, "Body Idle State: ");
draw_set_color(_tier_col);
draw_text(_hud_x + 130, _hud_y + 165, _tier_name);

// Combat Event Notice
draw_set_color(c_yellow);
draw_text(_hud_x, _hud_y + 190, "Event: " + last_combat_msg);

// Recoil Impulse & Directional Orientation Bar
var _recoil_str = string(abs(round(recoil_x))) + "px | Shake: " + string(round(recoil_shake));
draw_set_color(c_aqua);
draw_text(_hud_x, _hud_y + 215, "Recoil Impulse: " + _recoil_str + " | Orientation: " + _facing_badge);

// Controls Helper Legend
var _leg_x = 40;
var _leg_y = 510;
draw_set_color(c_black);
draw_rectangle(_leg_x - 10, _leg_y - 10, _leg_x + 720, _leg_y + 160, false);
draw_set_color(c_lime);
draw_rectangle(_leg_x - 10, _leg_y - 10, _leg_x + 720, _leg_y + 160, true);

draw_set_color(c_white);
draw_text(_leg_x, _leg_y, "DEBUG RECOIL, MELEE & LIMB CONTROLS:");
draw_set_color(make_color_rgb(180, 255, 255));
draw_text(_leg_x, _leg_y + 20, "[F / TAB] Flip Facing (L/R)  |  [V] Duel Arena  |  [H] Cycle Health Tiers (100% -> 55% -> 25%)");
draw_set_color(make_color_rgb(255, 200, 100));
draw_text(_leg_x, _leg_y + 40, "[C / M] 120mm CANNON GUN-CLUB MELEE STRIKE  |  [1] 120mm Shot  |  [2] GAU-88 Vulcan  |  [3] Missiles");
draw_set_color(make_color_rgb(255, 140, 100));
draw_text(_leg_x, _leg_y + 60, "[4] Kinetic Impact (14px)  |  [5] Energy Shudder (8px)  |  [6] ROCKET BLAST (32px HARSH!)  |  [7] MELEE SLASH (24px)");
draw_set_color(make_color_rgb(255, 160, 160));
draw_text(_leg_x, _leg_y + 80, "[8] Sever Left Arm (Idle)  |  [9] Sever Right Arm (Idle)  |  [B] Sever BOTH Arms  |  [0] Crush Legs");
draw_set_color(c_yellow);
draw_text(_leg_x, _leg_y + 105, "[R] Full Repair & Reset  |  [-] Destroy Ares Pack  |  [=] Torso Core Meltdown");

// Return to HQ Terminal Button (Top Right)
var _ret_bx = room_width - 320;
var _ret_by = 20;
var _ret_bw = 300;
var _ret_bh = 38;
var _rmx = mouse_x;
var _rmy = mouse_y;
var _rhov = (_rmx >= _ret_bx && _rmx <= _ret_bx + _ret_bw && _rmy >= _ret_by && _rmy <= _ret_by + _ret_bh);

if (_rhov && mouse_check_button_pressed(mb_left)) {
    if (room_exists(rm_hq_terminal)) {
        room_goto(rm_hq_terminal);
    }
}

draw_set_color(_rhov ? make_color_rgb(140, 50, 20) : make_color_rgb(60, 20, 10));
draw_rectangle(_ret_bx, _ret_by, _ret_bx + _ret_bw, _ret_by + _ret_bh, false);
draw_set_color(make_color_rgb(255, 140, 60));
draw_rectangle(_ret_bx, _ret_by, _ret_bx + _ret_bw, _ret_by + _ret_bh, true);
draw_set_color(c_white);
draw_text(_ret_bx + 16, _ret_by + 10, "[ESC / CLICK: RETURN TO HQ TERMINAL]");
