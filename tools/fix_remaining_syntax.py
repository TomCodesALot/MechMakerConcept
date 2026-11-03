import re

# 1. objects/obj_BattleManager/Create_0.gml
with open('objects/obj_BattleManager/Create_0.gml', 'r', encoding='utf-8') as f:
    s = f.read()
s = s.replace(
    'var _rc = variable_struct_get(_gm.competitor_catalog, _rival_keys[r];',
    'var _rc = variable_struct_get(_gm.competitor_catalog, _rival_keys[r]);'
)
with open('objects/obj_BattleManager/Create_0.gml', 'w', encoding='utf-8') as f:
    f.write(s)
print('Fixed BattleManager/Create_0.gml')

# 2. objects/obj_FactionManager/Create_0.gml
with open('objects/obj_FactionManager/Create_0.gml', 'r', encoding='utf-8') as f:
    s = f.read()
s = s.replace(
    'var _rel = variable_struct_get(diplomatic_relations, _keys[k];',
    'var _rel = variable_struct_get(diplomatic_relations, _keys[k]);'
)
s = s.replace(
    'var _r2 = variable_struct_get(diplomatic_relations, _keys[k2];',
    'var _r2 = variable_struct_get(diplomatic_relations, _keys[k2]);'
)
s = s.replace(
    'var _wrel = variable_struct_get(diplomatic_relations, _keys[wk];',
    'var _wrel = variable_struct_get(diplomatic_relations, _keys[wk]);'
)
s = s.replace(
    'var _r = variable_struct_get(diplomatic_relations, _keys[k];',
    'var _r = variable_struct_get(diplomatic_relations, _keys[k]);'
)
with open('objects/obj_FactionManager/Create_0.gml', 'w', encoding='utf-8') as f:
    f.write(s)
print('Fixed FactionManager/Create_0.gml')

# 3. objects/obj_HQTerminal/Draw_64.gml
with open('objects/obj_HQTerminal/Draw_64.gml', 'r', encoding='utf-8') as f:
    s = f.read()
# fix line 5 boot log
s = re.sub(
    r'file_text_write_string\(_log_f,\s*"\[BOOT\] obj_HQTerminal Draw_64 FIRST FRAME EXECUTED! gw="\s*\+\s*string\(display_get_gui_width\(\)\)\s*\+\s*" gh="\s*\+\s*string\(display_get_gui_height\(\)\)\s*\+\s*"[^\n]*\n"\);',
    'file_text_write_string(_log_f, "[BOOT] obj_HQTerminal Draw_64 FIRST FRAME EXECUTED! gw=" + string(display_get_gui_width()) + " gh=" + string(display_get_gui_height()) + "\\n");',
    s
)
s = s.replace(
    'draw_text(_mx_box + 48, _my_box + 26, "Loaded: " + string(variable_struct_get(crucible_batch, _mats[mi]));',
    'draw_text(_mx_box + 48, _my_box + 26, "Loaded: " + string(variable_struct_get(crucible_batch, _mats[mi])));'
)
s = s.replace(
    'var _s = variable_struct_get(obj_GameManager.mobile_suit_catalog, _c_keys[ki];',
    'var _s = variable_struct_get(obj_GameManager.mobile_suit_catalog, _c_keys[ki]);'
)
s = s.replace(
    'if ((variable_struct_get(_fs.upgrades, _chk_tracks[tk] ?? 1) >= 3) _t3_count++;',
    'if ((variable_struct_get(_fs.upgrades, _chk_tracks[tk]) ?? 1) >= 3) _t3_count++;'
)
s = s.replace(
    'if (variable_struct_get(_rc, _r_keys_all[ak].is_acquired) _acquired_count++;',
    'if (variable_struct_get(_rc, _r_keys_all[ak]).is_acquired) _acquired_count++;'
)
with open('objects/obj_HQTerminal/Draw_64.gml', 'w', encoding='utf-8') as f:
    f.write(s)
print('Fixed HQTerminal/Draw_64.gml')

# 4. objects/obj_NemesisManager/Create_0.gml
with open('objects/obj_NemesisManager/Create_0.gml', 'r', encoding='utf-8') as f:
    s = f.read()
s = s.replace(
    'var _c = variable_struct_get(characters_map, _ids[i];',
    'var _c = variable_struct_get(characters_map, _ids[i]);'
)
with open('objects/obj_NemesisManager/Create_0.gml', 'w', encoding='utf-8') as f:
    f.write(s)
print('Fixed NemesisManager/Create_0.gml')

# 5. scripts/scr_nemesis_system/scr_nemesis_system.gml
with open('scripts/scr_nemesis_system/scr_nemesis_system.gml', 'r', encoding='utf-8') as f:
    s = f.read()
s = s.replace(
    'var _rc = variable_struct_get(_mgr.characters_map, _keys[r];',
    'var _rc = variable_struct_get(_mgr.characters_map, _keys[r]);'
)
s = s.replace(
    'var _fin_c = variable_struct_get(_mgr.characters_map, _keys[k];',
    'var _fin_c = variable_struct_get(_mgr.characters_map, _keys[k]);'
)
with open('scripts/scr_nemesis_system/scr_nemesis_system.gml', 'w', encoding='utf-8') as f:
    f.write(s)
print('Fixed scr_nemesis_system.gml')

# 6. objects/obj_BlueprintManager/Create_0.gml
with open('objects/obj_BlueprintManager/Create_0.gml', 'r', encoding='utf-8') as f:
    s = f.read()
old_bp = '''    variable_struct_get(_custom_mech, "tuning_grades") = {
        reactor: _r.grade,
        hydraulics: _h.grade,
        thrusters: _t.grade
    };'''
new_bp = '''    variable_struct_set(_custom_mech, "tuning_grades", {
        reactor: _r.grade,
        hydraulics: _h.grade,
        thrusters: _t.grade
    });'''
s = s.replace(old_bp, new_bp)
with open('objects/obj_BlueprintManager/Create_0.gml', 'w', encoding='utf-8') as f:
    f.write(s)
print('Fixed BlueprintManager/Create_0.gml')
