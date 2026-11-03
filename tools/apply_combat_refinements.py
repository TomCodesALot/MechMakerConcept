# Apply the 5 agreed combat refinements to Create_0.gml and Draw_64.gml

# =========================================================================
# 1. PATCH Create_0.gml: Vanguard Screening, Brace Stance, Dynamic Pacing, Wreckage & Pilot Ejection
# =========================================================================
with open('objects/obj_BattleManager/Create_0.gml', 'r') as f_in:
    c_content = f_in.read()

# 1A. Add Vanguard Screening, Brace reduction, and Dynamic Pacing to start_battle_cinematic
p_start = c_content.find('start_battle_cinematic = function')
assert p_start != -1, "start_battle_cinematic not found"

old_mit = """    var _mitigated_dmg = max(15, _raw_dmg - _limb.armor);"""

new_mit = """    // 1. Tactical Brace Defense Stance: 40% damage reduction
    var _is_braced = variable_struct_exists(_def, "braced") && _def.braced;
    var _mitigated_dmg = max(15, _raw_dmg - _limb.armor);
    if (_is_braced) {
        _mitigated_dmg = max(10, floor(_mitigated_dmg * 0.60));
    }

    // 2. Vanguard Screening & Interception:
    // Direct fire (non-artillery/missiles) aimed at rear support line is intercepted by frontline Vanguard!
    var _is_artillery_or_missile = (_wpn.range_max >= 4 || _wpn.proj_type == "MISSILE");
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
    }"""

assert old_mit in c_content, "old_mit not found"
c_content = c_content.replace(old_mit, new_mit, 1)

# 1B. Braced units forfeit counter-attacks
old_counter_chk = """    var _survives = (!_is_hit || (_hit_part != "torso" && _limb.cur > _mitigated_dmg) || (_hit_part == "torso" && _limb.cur > _mitigated_dmg));
    if (_survives && array_length(_def.weapons) > 0) {"""

new_counter_chk = """    var _survives = (!_is_hit || (_hit_part != "torso" && _limb.cur > _mitigated_dmg) || (_hit_part == "torso" && _limb.cur > _mitigated_dmg));
    if (_survives && !_is_braced && array_length(_def.weapons) > 0) {"""

assert old_counter_chk in c_content, "old_counter_chk not found"
c_content = c_content.replace(old_counter_chk, new_counter_chk, 1)

# 1C. Dynamic Pacing flag in battle_cinematic
old_cin_init = """    battle_cinematic.theater = _theater;
    battle_cinematic.terrain = _terr;"""

new_cin_init = """    // Dynamic Cinematic Pacing: Ace & Incursions get full cutscene; grunts run fast condensed clash
    var _is_ace_clash = (_atk.squad_type == "SUPER_ACE" || _def.squad_type == "SUPER_ACE" || state == COMBAT_STATE.NEMESIS_INCURSION);
    battle_cinematic.is_condensed = !_is_ace_clash;
    battle_cinematic.theater = _theater;
    battle_cinematic.terrain = _terr;"""

assert old_cin_init in c_content, "old_cin_init not found"
c_content = c_content.replace(old_cin_init, new_cin_init, 1)

# 1D. Condensed 2x speed for grunt skirmishes in update_battle_cinematic
old_timer_inc = """    battle_cinematic.timer++;
    var _t = battle_cinematic.timer;"""

new_timer_inc = """    battle_cinematic.timer += (variable_struct_exists(battle_cinematic, "is_condensed") && battle_cinematic.is_condensed) ? 2 : 1;
    var _t = battle_cinematic.timer;"""

assert old_timer_inc in c_content, "old_timer_inc not found"
c_content = c_content.replace(old_timer_inc, new_timer_inc, 1)

# 1E. Wreckage and Pilot Ejection in update_battle_cinematic (Phase 3)
old_kill_log = """add_log("[CATASTROPHIC KILL] " + _def.callsign + " REACTOR BREACH! Unit neutralized.");"""

new_kill_log = """add_log("[CATASTROPHIC KILL] " + _def.callsign + " REACTOR BREACH! Unit neutralized.");

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
                        }"""

assert old_kill_log in c_content, "old_kill_log not found"
c_content = c_content.replace(old_kill_log, new_kill_log, 1)

# 1F. Wreckage and Pilot Ejection in skip_battle_cinematic
old_skip_kill = """add_log("[CATASTROPHIC KILL] " + _def.callsign + " REACTOR BREACH! Unit neutralized.");"""
assert old_skip_kill in c_content, "old_skip_kill not found"
c_content = c_content.replace(old_skip_kill, new_kill_log, 1)

with open('objects/obj_BattleManager/Create_0.gml', 'w') as f_out:
    f_out.write(c_content)

print("Create_0.gml patched successfully.")

# =========================================================================
# 2. PATCH Draw_64.gml: Add Aimed Shot Toggle and Manual Weapon Selection
# =========================================================================
with open('objects/obj_BattleManager/Draw_64.gml', 'r') as f_in:
    d_content = f_in.read()

old_det_btn = """                scr_draw_snes_button(_det_btn_x, _det_btn_y, _det_btn_w, 22, "DETACH", _dethov, false, make_color_rgb(100, 220, 255));
            }"""

new_det_btn = """                scr_draw_snes_button(_det_btn_x, _det_btn_y, _det_btn_w, 22, "DETACH", _dethov, false, make_color_rgb(100, 220, 255));
            }

            // Aimed Shot Precision Limb Toggle [AIM: OFF / TORSO / ARMS / LEGS]
            var _aim_btn_w = 64;
            var _aim_btn_x = _card_x + _card_w - _aim_btn_w - 6;
            var _aim_btn_y = _card_y + 36;
            var _aimhov = (_mx >= _aim_btn_x && _mx <= _aim_btn_x + _aim_btn_w && _my >= _aim_btn_y && _my <= _aim_btn_y + 20);
            if (_aimhov && _click) {
                if (!variable_struct_exists(_su, "is_aimed_shot") || !_su.is_aimed_shot) {
                    _su.is_aimed_shot = true;
                    _su.targeted_limb = "torso";
                } else if (_su.targeted_limb == "torso") {
                    _su.targeted_limb = "arm_right";
                } else if (_su.targeted_limb == "arm_right") {
                    _su.targeted_limb = "legs";
                } else {
                    _su.is_aimed_shot = false;
                    _su.targeted_limb = "";
                }
                scr_audio_play_ui("click");
                add_log("[AIM OVERRIDE] " + _su.callsign + " target: " + (_su.is_aimed_shot ? string_upper(_su.targeted_limb) : "AUTO"));
            }
            var _aim_lbl = (!variable_struct_exists(_su, "is_aimed_shot") || !_su.is_aimed_shot) ? "AIM:OFF" : ("AIM:" + string_upper(string_copy(_su.targeted_limb, 1, 4)));
            scr_draw_snes_button(_aim_btn_x, _aim_btn_y, _aim_btn_w, 20, _aim_lbl, _aimhov, (variable_struct_exists(_su, "is_aimed_shot") && _su.is_aimed_shot), (variable_struct_exists(_su, "is_aimed_shot") && _su.is_aimed_shot) ? make_color_rgb(255, 140, 40) : make_color_rgb(120, 140, 160));

            // Manual Weapon Override Button
            var _wpn_btn_w = 64;
            var _wpn_btn_x = _card_x + _card_w - _wpn_btn_w - 6;
            var _wpn_btn_y = _card_y + 58;
            var _wpnhov = (_mx >= _wpn_btn_x && _mx <= _wpn_btn_x + _wpn_btn_w && _my >= _wpn_btn_y && _my <= _wpn_btn_y + 20);
            if (_wpnhov && _click && array_length(_su.weapons) > 1) {
                if (!variable_struct_exists(_su, "manual_weapon_idx")) _su.manual_weapon_idx = 0;
                _su.manual_weapon_idx = (_su.manual_weapon_idx + 1) % array_length(_su.weapons);
                scr_audio_play_ui("tab");
                add_log("[WEAPON OVERRIDE] " + _su.callsign + " selected: " + _su.weapons[_su.manual_weapon_idx].short_name);
            }
            var _w_name = (variable_struct_exists(_su, "manual_weapon_idx") && _su.manual_weapon_idx >= 0 && _su.manual_weapon_idx < array_length(_su.weapons)) ? string_copy(_su.weapons[_su.manual_weapon_idx].short_name, 1, 6) : "AUTO";
            scr_draw_snes_button(_wpn_btn_x, _wpn_btn_y, _wpn_btn_w, 20, "W:" + _w_name, _wpnhov, variable_struct_exists(_su, "manual_weapon_idx"), make_color_rgb(255, 215, 60));"""

assert old_det_btn in d_content, "old_det_btn not found in Draw_64"
d_content = d_content.replace(old_det_btn, new_det_btn, 1)

with open('objects/obj_BattleManager/Draw_64.gml', 'w') as f_out:
    f_out.write(d_content)

print("Draw_64.gml patched successfully.")
