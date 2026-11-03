import re

with open('objects/obj_BattleManager/Create_0.gml', 'r') as f:
    text = f.read()

# 1. Update load_map(0) to load map based on active_combat_context
old_load_map = "load_map(0);"
new_load_map = """var _target_map_id = 0;
var _combat_ctx = undefined;
if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "active_combat_context") && !is_undefined(obj_GameManager.active_combat_context)) {
    _combat_ctx = obj_GameManager.active_combat_context;
    _target_map_id = scr_territory_get_battle_map_id(_combat_ctx.sector_id);
}
load_map(_target_map_id);

if (!is_undefined(_combat_ctx)) {
    map_definitions[current_map_id].name = string_upper(_combat_ctx.sector_name) + " FRONT";
    map_definitions[current_map_id].desc = "Tactical Engagement Zone // " + _combat_ctx.subregion;
    map_definitions[current_map_id].ambient_tag = "[" + string_upper(_combat_ctx.region) + " THEATER // " + (_combat_ctx.is_invasion ? "OFFENSIVE INVASION VECTOR" : "SOVEREIGN DEFENSE PERIMETER") + " // GARRISON: " + string_upper(_combat_ctx.garrison_unit) + "]";
}"""

if old_load_map in text:
    text = text.replace(old_load_map, new_load_map, 1)
    print("Replaced load_map(0) with context-sensitive loader.")
else:
    print("load_map(0) not found or already replaced.")

# 2. Add customization for HOSTILE and ALLIED units before camera setup
cam_marker = "// 4. Isometric Camera & Viewport Controls"
unit_customization = """// 3c. Context-Sensitive Unit Customization from Strategic War Map Context
if (!is_undefined(_combat_ctx)) {
    var _fac = _combat_ctx.controlling_faction;
    var _fac_col = make_color_rgb(180, 180, 180);
    var _faction_name_str = "OPFOR GARRISON";
    
    if (_fac == "faction_a") {
        _fac_col = make_color_rgb(100, 160, 255);
        _faction_name_str = "Terran Coalition";
    } else if (_fac == "faction_b") {
        _fac_col = make_color_rgb(80, 240, 200);
        _faction_name_str = "Free Colonies League";
    } else if (_fac == "faction_c") {
        _fac_col = make_color_rgb(255, 160, 60);
        _faction_name_str = "Rogue Syndicates";
    } else if (_fac == "faction_d") {
        _fac_col = make_color_rgb(200, 120, 255);
        _faction_name_str = "Kurogane Zaibatsu";
    } else if (_fac == "faction_e") {
        _fac_col = make_color_rgb(140, 150, 255);
        _faction_name_str = "Sidereal Sovereign";
    } else if (_fac == "faction_f") {
        _fac_col = make_color_rgb(255, 80, 80);
        _faction_name_str = "Red Mars Consensus";
    }
    
    for (var ui = 0; ui < array_length(units); ui++) {
        var _u = units[ui];
        if (_u.team == "HOSTILE") {
            _u.image_blend = _fac_col;
            if (ui == 8) {
                _u.callsign = string_upper(_faction_name_str) + " COMMAND BASTION";
                _u.pilot_name = _combat_ctx.garrison_unit;
            } else {
                _u.callsign = _faction_name_str + " Cohort [" + string(ui - 7) + "]";
            }
        }
    }
}

// Deploy Custom Assembled Player Mechs from Hangar if Available
if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "inventory") && variable_struct_exists(obj_GameManager.inventory, "deployable_mechs")) {
    var _p_mechs = obj_GameManager.inventory.deployable_mechs;
    if (array_length(_p_mechs) > 0) {
        var _allied_idx = 0;
        for (var ui = 0; ui < array_length(units); ui++) {
            var _u = units[ui];
            if (_u.team == "ALLIED" && _allied_idx < array_length(_p_mechs)) {
                var _pm = _p_mechs[_allied_idx];
                _u.callsign = _pm.name;
                _u.pilot_name = (_pm.assigned_pilot != "Unassigned") ? _pm.assigned_pilot : ("Pilot " + string(_allied_idx + 1));
                _u.components.torso.max = _pm.armor_rating;
                _u.components.torso.cur = _pm.armor_rating;
                _allied_idx++;
            }
        }
    }
}

"""

if cam_marker in text and "Context-Sensitive Unit Customization" not in text:
    text = text.replace(cam_marker, unit_customization + cam_marker, 1)
    print("Added context-sensitive unit customization.")
else:
    print("Camera marker not found or already added.")

with open('objects/obj_BattleManager/Create_0.gml', 'w') as f:
    f.write(text)
print("Updated objects/obj_BattleManager/Create_0.gml successfully.")
