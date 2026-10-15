with open('objects/obj_FactionManager/Create_0.gml', 'r') as f:
    content = f.read()

target_inc = '''get_incumbent_specs = function(_faction_id) {
    if (variable_struct_exists(incumbent_doctrines, _faction_id)) {
        return incumbent_doctrines[$ _faction_id];
    }
    return incumbent_doctrines.faction_a;
};'''

replacement_inc = '''get_incumbent_specs = function(_faction_id) {
    var _base = variable_struct_exists(incumbent_doctrines, _faction_id) ? incumbent_doctrines[$ _faction_id] : incumbent_doctrines.faction_a;

    // Dynamically query competitor catalog for active era chassis (docs/27)
    if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "competitor_catalog")) {
        var _corp_map = { faction_a: "corp_vhi", faction_b: "corp_aod", faction_c: "corp_rust", faction_d: "corp_hats" };
        var _cid = _corp_map[$ _faction_id] ?? "corp_vhi";
        if (variable_struct_exists(obj_GameManager.competitor_catalog, _cid)) {
            var _cp = obj_GameManager.competitor_catalog[$ _cid];
            if (!is_undefined(_cp.active_line_chassis)) {
                return {
                    id: _cp.active_line_chassis.id,
                    name: _cp.active_line_chassis.name,
                    faction_name: _base.faction_name,
                    role: _cp.active_line_chassis.class + " (" + _cp.branch_name + ")",
                    armor: _cp.active_line_chassis.armor,
                    power: _cp.active_line_chassis.power,
                    speed: _cp.active_line_chassis.speed,
                    mass: _base.mass,
                    combat_rating: _cp.active_line_chassis.combat,
                    weights: _base.weights,
                    doctrine_focus: _cp.doctrine,
                    evaluator: _base.evaluator
                };
            }
        }
    }
    return _base;
};'''

if target_inc in content:
    content = content.replace(target_inc, replacement_inc)
    print("Updated get_incumbent_specs with dynamic competitor catalog lookup")
else:
    print("ERROR: target_inc not found in obj_FactionManager/Create_0.gml")

world_reflection_methods = '''
// 12. Dynamic Frontline World Reflection Methods (docs/27)
get_faction_active_line_chassis = function(_faction_id) {
    if (!variable_struct_exists(mass_production_contracts, _faction_id)) return undefined;
    var _mp = mass_production_contracts[$ _faction_id];
    if (_mp.replaced) {
        return {
            name: _mp.replacement_name,
            blueprint_id: _mp.replacement_blueprint_id,
            is_player_designed: true,
            block_level: _mp.block_level,
            adoption_stage: _mp.adoption_stage,
            combat_bonus: _mp.combat_bonus,
            active_units: _mp.active_frontline_units
        };
    } else {
        var _inc = get_incumbent_specs(_faction_id);
        return {
            name: _inc.name,
            blueprint_id: _inc.id,
            is_player_designed: false,
            block_level: 1,
            adoption_stage: "INCUMBENT_LINE",
            combat_bonus: 0,
            active_units: 150
        };
    }
};

get_faction_patrol_squad = function(_faction_id) {
    var _chassis = get_faction_active_line_chassis(_faction_id);
    if (is_undefined(_chassis)) return [];
    var _squad = [];
    for (var u = 0; u < 4; u++) {
        array_push(_squad, {
            unit_id: "patrol_" + _faction_id + "_" + string(u + 1),
            callsign: _chassis.name + " Unit-" + string(u + 1),
            chassis_name: _chassis.name,
            blueprint_id: _chassis.blueprint_id,
            is_player_designed: _chassis.is_player_designed,
            armor: (_chassis.is_player_designed ? 2200 : 1800) + (_chassis.block_level * 150),
            combat_rating: 450 + (_chassis.combat_bonus * 5)
        });
    }
    return _squad;
};
'''

content += world_reflection_methods
with open('objects/obj_FactionManager/Create_0.gml', 'w') as f:
    f.write(content)
print("Updated obj_FactionManager/Create_0.gml successfully")
