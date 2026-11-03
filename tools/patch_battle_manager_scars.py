# -*- coding: utf-8 -*-
import re

draw_path = "objects/obj_BattleManager/Draw_0.gml"
with open(draw_path, "r", encoding="utf-8") as f:
    text = f.read()

target = "        // Floating Unit Overhead Status (Callsign, Formation Tag & HP Bar)"

replacement = """        // --- GOAL FINAL: PERSISTENT TACTICAL BATTLE SCARS & CRIPPLED LIMB FX ---
        if (!_u.is_destroyed && variable_struct_exists(_u, "damaged_parts") && is_struct(_u.damaged_parts)) {
            var _cur_draw_y = (_u.squad_type == "PLATOON_3") ? _lead_y : _ace_y;
            var _cur_scale = (_u.squad_type == "PLATOON_3") ? 1.0 : 1.15;

            // Severed Left Arm Socket Overlay & Arc Sparks
            if (variable_struct_exists(_u.damaged_parts, "arm_left") && _u.damaged_parts.arm_left && sprite_exists(spr_ms_ironclad_hit_left_arm_off)) {
                draw_sprite_ext(spr_ms_ironclad_hit_left_arm_off, 0, _vx, _cur_draw_y, _xscale * _cur_scale, _yscale * _cur_scale, 0, c_white, 0.85);
                if ((current_time + _u_c * 110) % 360 < 120) {
                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_circle(_vx - (8 * zoom * _facing_sign), _cur_draw_y - (22 * zoom), 1.8 * zoom, false);
                }
            }

            // Severed Right Arm Socket Overlay & Fiery Sparks
            if (variable_struct_exists(_u.damaged_parts, "arm_right") && _u.damaged_parts.arm_right && sprite_exists(spr_ms_ironclad_hit_right_arm_off)) {
                draw_sprite_ext(spr_ms_ironclad_hit_right_arm_off, 0, _vx, _cur_draw_y, _xscale * _cur_scale, _yscale * _cur_scale, 0, c_white, 0.85);
                if ((current_time + _u_r * 130) % 400 < 130) {
                    draw_set_color(make_color_rgb(255, 180, 50));
                    draw_circle(_vx + (8 * zoom * _facing_sign), _cur_draw_y - (20 * zoom), 2.0 * zoom, false);
                }
            }

            // Crippled Hydraulic Legs Trailing Smoke
            if (variable_struct_exists(_u.damaged_parts, "legs") && _u.damaged_parts.legs) {
                if ((current_time + _u_c * 70) % 320 < 160) {
                    draw_set_color(make_color_rgb(190, 200, 215));
                    draw_set_alpha(0.45);
                    draw_circle(_vx, _cur_draw_y - (5 * zoom), 3.5 * zoom, false);
                    draw_set_alpha(1.0);
                }
            }
        }

        // Floating Unit Overhead Status (Callsign, Formation Tag & HP Bar)"""

if target in text:
    text = text.replace(target, replacement, 1)
    with open(draw_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("[PASS] objects/obj_BattleManager/Draw_0.gml updated with persistent battle scars.")
else:
    print("[ERROR] Target string not found in Draw_0.gml")
    exit(1)

