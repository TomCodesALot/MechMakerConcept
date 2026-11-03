with open('objects/obj_BattleManager/Draw_64.gml', 'r') as f:
    text = f.read()

old_click_block = """    if (_p_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            if (_is_win) {
                obj_GameManager.add_funds(180000);
                obj_GameManager.add_alloy("alloy_vanguard_comp", 4);
                obj_GameManager.add_raw_material("mat_tungsten", 25);
                if (instance_exists(obj_FactionManager)) {
                    obj_FactionManager.modify_standing("faction_a", 15);
                }
            }
        }
        if (room_exists(rm_hq_terminal)) room_goto(rm_hq_terminal);
    }"""

new_click_block = """    if (_p_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            if (variable_instance_exists(obj_GameManager, "active_combat_context") && !is_undefined(obj_GameManager.active_combat_context)) {
                var _ctx = obj_GameManager.active_combat_context;
                var _t = scr_territory_get(_ctx.sector_id);
                if (!is_undefined(_t)) {
                    if (_is_win) {
                        var _prev_fac = _t.controlling_faction;
                        _t.controlling_faction = "pmc";
                        _t.defense_rating = max(45, _t.defense_rating - 20);
                        scr_territory_recalculate_control_percentages();
                        if (instance_exists(obj_FactionManager)) {
                            obj_FactionManager.modify_standing(_prev_fac, -15);
                        }
                    } else {
                        _t.defense_rating = max(15, _t.defense_rating - 5);
                    }
                }
                obj_GameManager.last_battle_report = {
                    is_win: _is_win,
                    sector_id: _ctx.sector_id,
                    sector_name: _ctx.sector_name,
                    controlling_faction: _ctx.controlling_faction
                };
                obj_GameManager.active_combat_context = undefined;
            }
            if (_is_win) {
                obj_GameManager.add_funds(180000);
                obj_GameManager.add_alloy("alloy_vanguard_comp", 4);
                obj_GameManager.add_raw_material("mat_tungsten", 25);
            }
        }
        if (room_exists(rm_hq_terminal)) room_goto(rm_hq_terminal);
    }"""

if old_click_block in text:
    text = text.replace(old_click_block, new_click_block, 1)
    print("Successfully replaced AAR button click block.")
else:
    print("AAR button block not found exactly as string, checking alternative...")

with open('objects/obj_BattleManager/Draw_64.gml', 'w') as f:
    f.write(text)
print("Updated objects/obj_BattleManager/Draw_64.gml successfully.")
