with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
    text = f.read()

# 1. Add battle report toast trigger right near the beginning of Draw_64
report_check = """
// Check Return from rm_combat Tactical Sortie
if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "last_battle_report") && !is_undefined(obj_GameManager.last_battle_report)) {
    var _lbr = obj_GameManager.last_battle_report;
    if (_lbr.is_win) {
        show_toast("★ TACTICAL VICTORY! " + string_upper(_lbr.sector_name) + " CONQUERED VIA MANUAL SORTIE! ★", make_color_rgb(255, 215, 60));
        scr_audio_play_ui("confirm");
    } else {
        show_toast("SORTIE WITHDRAWAL: Forces withdrew from " + string_upper(_lbr.sector_name) + ".", make_color_rgb(255, 90, 80));
        scr_audio_play_ui("cancel");
    }
    obj_GameManager.last_battle_report = undefined;
}
"""

marker_top = "var _sx = random_range(-crucible_shake, crucible_shake);"
if marker_top in text and "last_battle_report" not in text:
    text = text.replace(marker_top, marker_top + "\n" + report_check, 1)
    print("Added last_battle_report check.")

# 2. Update Dossier Sortie button to set active_combat_context
old_sortie_sec = """    var _sort_sec_y = _act_y + 40;
    var _sort_sec_hov = (_mx >= _dos_x + 16 && _mx <= _dos_x + 16 + _act_w && _my >= _sort_sec_y && _my <= _sort_sec_y + 34);
    if (_sort_sec_hov && _click && room_exists(rm_combat)) {
        scr_audio_play_ui("confirm");
        room_goto(rm_combat);
    }
    scr_draw_snes_button(_dos_x + 16, _sort_sec_y, _act_w, 34, "⚔️ SORTIE COMBAT SQUAD HERE", _sort_sec_hov, false, make_color_rgb(255, 100, 100));"""

new_sortie_sec = """    var _sort_sec_y = _act_y + 40;
    var _sort_sec_hov = (_mx >= _dos_x + 16 && _mx <= _dos_x + 16 + _act_w && _my >= _sort_sec_y && _my <= _sort_sec_y + 34);
    if (_sort_sec_hov && _click && room_exists(rm_combat)) {
        if (instance_exists(obj_GameManager)) {
            obj_GameManager.active_combat_context = {
                sector_id: _cur_t.id,
                sector_name: _cur_t.name,
                region: _cur_t.region,
                subregion: _cur_t.subregion,
                controlling_faction: _cur_t.controlling_faction,
                defense_rating: _cur_t.defense_rating,
                garrison_unit: _cur_t.garrison_unit,
                is_invasion: (_cur_t.controlling_faction != "pmc"),
                origin_base_id: (order_dispatch_mode && order_origin_id != "") ? order_origin_id : scr_territory_get_adjacent_pmc_base(_cur_t.id)
            };
        }
        scr_audio_play_ui("confirm");
        room_goto(rm_combat);
    }
    scr_draw_snes_button(_dos_x + 16, _sort_sec_y, _act_w, 34, "⚔️ SORTIE COMBAT SQUAD HERE", _sort_sec_hov, false, make_color_rgb(255, 100, 100));"""

if old_sortie_sec in text:
    text = text.replace(old_sortie_sec, new_sortie_sec, 1)
    print("Updated dossier sortie button with active_combat_context.")
else:
    print("Dossier sortie button snippet not found exactly.")

# 3. In order_modal_active: add Manual Sortie button alongside auto-dispatch
old_modal_btns = """        var _btn_w = 280;
        var _btn_h = 40;
        var _by = _fc_y + 122;
        
        var _exec_hov = (_mx >= _omx + 20 && _mx <= _omx + 20 + _btn_w && _my >= _by && _my <= _by + _btn_h);
        if (_exec_hov && _click) {
            var _is_comb = (order_operation_type == "ASSAULT");
            if (scr_territory_issue_order(order_origin_id, order_target_id, _g_spec.unit_sprite_name, _g_spec.stack_count, _is_comb)) {
                order_modal_active = false;
                order_dispatch_mode = false;
            }
        }
        scr_draw_snes_button(_omx + 20, _by, _btn_w, _btn_h, "⚡ EXECUTE DISPATCH [ENTER]", _exec_hov, false, make_color_rgb(0, 240, 255));
        
        var _can_hov = (_mx >= _omx + _omw - 20 - _btn_w && _mx <= _omx + _omw - 20 && _my >= _by && _my <= _by + _btn_h);
        if ((_can_hov && _click) || keyboard_check_pressed(vk_escape)) {
            order_modal_active = false;
            order_dispatch_mode = false;
            scr_audio_play_ui("cancel");
        }
        scr_draw_snes_button(_omx + _omw - 20 - _btn_w, _by, _btn_w, _btn_h, "✖ ABORT DIRECTIVE [ESC]", _can_hov, false, make_color_rgb(255, 90, 80));"""

new_modal_btns = """        var _btn_w = 188;
        var _btn_h = 40;
        var _by = _fc_y + 122;
        
        // 1. Auto-Simulate Dispatch Button
        var _exec_hov = (_mx >= _omx + 20 && _mx <= _omx + 20 + _btn_w && _my >= _by && _my <= _by + _btn_h);
        if (_exec_hov && _click) {
            var _is_comb = (order_operation_type == "ASSAULT");
            if (scr_territory_issue_order(order_origin_id, order_target_id, _g_spec.unit_sprite_name, _g_spec.stack_count, _is_comb)) {
                order_modal_active = false;
                order_dispatch_mode = false;
            }
        }
        scr_draw_snes_button(_omx + 20, _by, _btn_w, _btn_h, "⚡ AUTO-DISPATCH", _exec_hov, false, make_color_rgb(0, 240, 255));
        
        // 2. Manual Tactical Sortie Button (rm_combat)
        var _sort_bx = _omx + 20 + _btn_w + 14;
        var _sort_bw = 212;
        var _man_sort_hov = (_mx >= _sort_bx && _mx <= _sort_bx + _sort_bw && _my >= _by && _my <= _by + _btn_h);
        if (_man_sort_hov && _click && room_exists(rm_combat)) {
            if (instance_exists(obj_GameManager)) {
                obj_GameManager.active_combat_context = {
                    sector_id: order_target_id,
                    sector_name: _d_t.name,
                    region: _d_t.region,
                    subregion: _d_t.subregion,
                    controlling_faction: _d_t.controlling_faction,
                    defense_rating: _d_t.defense_rating,
                    garrison_unit: _d_t.garrison_unit,
                    is_invasion: (_d_t.controlling_faction != "pmc"),
                    origin_base_id: order_origin_id
                };
            }
            order_modal_active = false;
            order_dispatch_mode = false;
            scr_audio_play_ui("confirm");
            room_goto(rm_combat);
        }
        scr_draw_snes_button(_sort_bx, _by, _sort_bw, _btn_h, "⚔️ MANUAL SORTIE", _man_sort_hov, false, make_color_rgb(255, 215, 60));
        
        // 3. Abort Button
        var _abort_bx = _sort_bx + _sort_bw + 14;
        var _abort_bw = _omx + _omw - 20 - _abort_bx;
        var _can_hov = (_mx >= _abort_bx && _mx <= _abort_bx + _abort_bw && _my >= _by && _my <= _by + _btn_h);
        if ((_can_hov && _click) || keyboard_check_pressed(vk_escape)) {
            order_modal_active = false;
            order_dispatch_mode = false;
            scr_audio_play_ui("cancel");
        }
        scr_draw_snes_button(_abort_bx, _by, _abort_bw, _btn_h, "✖ ABORT", _can_hov, false, make_color_rgb(255, 90, 80));"""

if old_modal_btns in text:
    text = text.replace(old_modal_btns, new_modal_btns, 1)
    print("Updated directive modal with Manual Sortie choice.")
else:
    print("Directive modal buttons snippet not found exactly.")

with open('objects/obj_HQTerminal/Draw_64.gml', 'w') as f:
    f.write(text)
print("Updated objects/obj_HQTerminal/Draw_64.gml successfully.")
