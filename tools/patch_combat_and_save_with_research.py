import re

with open("objects/obj_BattleManager/Create_0.gml", "r") as f_in:
    bm_code = f_in.read()

target_unit_init = "show_debug_message(\"[obj_BattleManager] Combat grid initialized\");"
unit_boost_code = (
    "// Apply Strategic Tech Tree Multipliers to Fielded Allied Forces\n"
    "var _ap_bonus = floor(scr_research_get_bonus(\"ap_max\"));\n"
    "var _ev_bonus = floor(scr_research_get_bonus(\"evasion\") * 100);\n"
    "for (var u = 0; u < array_length(units); u++) {\n"
    "    if (units[u].team == \"ALLIED\") {\n"
    "        units[u].max_ap += _ap_bonus;\n"
    "        units[u].current_ap = units[u].max_ap;\n"
    "        units[u].evasion += _ev_bonus;\n"
    "    }\n"
    "}\n"
)

if target_unit_init in bm_code and "scr_research_get_bonus" not in bm_code:
    bm_code = bm_code.replace(target_unit_init, unit_boost_code + "\n" + target_unit_init, 1)

old_dmg_calc = "    var _mitigated_dmg = max(15, _raw_dmg - _limb.armor);"
new_dmg_calc = (
    "    // Researched Weapon Multipliers (Allied Attacker)\n"
    "    if (_atk.team == \"ALLIED\") {\n"
    "        if (_wpn.proj_type == \"KINETIC\" || _wpn.proj_type == \"ROTARY_VULCAN\") {\n"
    "            _raw_dmg = floor(_raw_dmg * (1.0 + scr_research_get_bonus(\"kinetic_dmg\")));\n"
    "        } else if (_wpn.proj_type == \"BEAM\" || _wpn.proj_type == \"ENERGY\") {\n"
    "            _raw_dmg = floor(_raw_dmg * (1.0 + scr_research_get_bonus(\"beam_dmg\")));\n"
    "        } else if (_wpn.proj_type == \"MISSILE\") {\n"
    "            _raw_dmg = floor(_raw_dmg * (1.0 + scr_research_get_bonus(\"missile_dmg\")));\n"
    "        } else if (_wpn.proj_type == \"MELEE\") {\n"
    "            _raw_dmg = floor(_raw_dmg * (1.0 + scr_research_get_bonus(\"melee_pen\")));\n"
    "        }\n"
    "    }\n"
    "    var _mitigated_dmg = max(15, _raw_dmg - _limb.armor);\n"
    "    // Researched Shield / Barrier Multipliers (Allied Defender)\n"
    "    if (_def.team == \"ALLIED\") {\n"
    "        if (_wpn.proj_type == \"BEAM\" || _wpn.proj_type == \"ENERGY\") {\n"
    "            _mitigated_dmg = floor(_mitigated_dmg * (1.0 - scr_research_get_bonus(\"beam_resist\")));\n"
    "        }\n"
    "        _mitigated_dmg = floor(_mitigated_dmg * (1.0 - scr_research_get_bonus(\"barrier_absorb\")));\n"
    "        _mitigated_dmg = max(5, _mitigated_dmg);\n"
    "    }"
)

if old_dmg_calc in bm_code:
    bm_code = bm_code.replace(old_dmg_calc, new_dmg_calc, 1)

old_acc = "    var _base = _atk.accuracy;\n    var _eva = _def.evasion;"
new_acc = (
    "    var _base = _atk.accuracy;\n    var _eva = _def.evasion;\n"
    "    if (_atk.team == \"ALLIED\") {\n"
    "        _base += floor(scr_research_get_bonus(\"hit_accuracy\") * 100);\n"
    "    }\n"
    "    if (_def.team == \"ALLIED\") {\n"
    "        _eva += floor(scr_research_get_bonus(\"evasion\") * 100);\n"
    "    }"
)

if old_acc in bm_code:
    bm_code = bm_code.replace(old_acc, new_acc, 1)

old_move = "var _ap_pool = _sel.components.legs.intact ? _sel.current_ap : 1;"
new_move = (
    "var _ap_pool = _sel.components.legs.intact ? _sel.current_ap : 1;\n"
    "    if (_sel.team == \"ALLIED\") {\n"
    "        _ap_pool += floor(scr_research_get_bonus(\"move_range\"));\n"
    "    }"
)

if old_move in bm_code:
    bm_code = bm_code.replace(old_move, new_move, 1)

with open("objects/obj_BattleManager/Create_0.gml", "w") as f_out:
    f_out.write(bm_code)
print("BattleManager Create_0.gml patched with research bonuses.")

with open("scripts/scr_save_system/scr_save_system.gml", "r") as f_save:
    save_code = f_save.read()

old_save_pack = "                inventory: obj_GameManager.inventory,\n                facilities: obj_GameManager.facilities"
new_save_pack = "                inventory: obj_GameManager.inventory,\n                facilities: obj_GameManager.facilities,\n                research_system: obj_GameManager.research_system"

if old_save_pack in save_code:
    save_code = save_code.replace(old_save_pack, new_save_pack, 1)

old_load_unpack = "            if (variable_struct_exists(_gs, \"facilities\")) obj_GameManager.facilities = _gs.facilities;"
new_load_unpack = "            if (variable_struct_exists(_gs, \"facilities\")) obj_GameManager.facilities = _gs.facilities;\n            if (variable_struct_exists(_gs, \"research_system\") && is_struct(_gs.research_system)) {\n                obj_GameManager.research_system = _gs.research_system;\n            }"

if old_load_unpack in save_code:
    save_code = save_code.replace(old_load_unpack, new_load_unpack, 1)

with open("scripts/scr_save_system/scr_save_system.gml", "w") as f_out:
    f_out.write(save_code)
print("scr_save_system.gml patched with research serialization.")
