import re

# 1. Fix obj_GameManager/Create_0.gml
path = 'objects/obj_GameManager/Create_0.gml'
with open(path, 'r', encoding='utf-8') as f:
    s = f.read()

s = s.replace(
    'variable_struct_get(inventory.alloys, "alloy_vanguard_comp") = _cur_alloy - _alloys_req;',
    'variable_struct_set(inventory.alloys, "alloy_vanguard_comp", _cur_alloy - _alloys_req);'
)
s = s.replace(
    'variable_struct_get(inventory.raw_materials, "mat_tungsten") = _cur_tungsten - _tungsten_req;',
    'variable_struct_set(inventory.raw_materials, "mat_tungsten", _cur_tungsten - _tungsten_req);'
)
s = s.replace(
    'variable_struct_get(flagship.upgrades, _track) = _next_tier;',
    'variable_struct_set(flagship.upgrades, _track, _next_tier);'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(s)
print('Fixed obj_GameManager/Create_0.gml')

# 2. Fix obj_BlueprintManager/Create_0.gml
path_bp = 'objects/obj_BlueprintManager/Create_0.gml'
with open(path_bp, 'r', encoding='utf-8') as f:
    s_bp = f.read()

s_bp = s_bp.replace(
    'var _who = _is_player ? "PMC Hephaestus blueprint "" + _new_suit_name + """ : "Competitor model "" + _new_suit_name + """;',
    'var _who = _is_player ? ("PMC Hephaestus blueprint \'" + _new_suit_name + "\'") : ("Competitor model \'" + _new_suit_name + "\'");'
)

old_tg = '''    variable_struct_get(_custom_mech, "tuning_grades") = {
        armor: _g_arm,
        mobility: _g_mob,
        heat_sink: _g_heat,
        sensor_range: _g_sens,
        power_output: _g_pow
    };'''
new_tg = '''    variable_struct_set(_custom_mech, "tuning_grades", {
        armor: _g_arm,
        mobility: _g_mob,
        heat_sink: _g_heat,
        sensor_range: _g_sens,
        power_output: _g_pow
    });'''
s_bp = s_bp.replace(old_tg, new_tg)

with open(path_bp, 'w', encoding='utf-8') as f:
    f.write(s_bp)
print('Fixed obj_BlueprintManager/Create_0.gml')

# 3. Fix obj_NemesisManager/Create_0.gml
path_nm = 'objects/obj_NemesisManager/Create_0.gml'
with open(path_nm, 'r', encoding='utf-8') as f:
    s_nm = f.read()

old_cc = '''        variable_struct_get(corporate_contracts, _pilot_id) = {
            target_pilot_id: _pilot_id,
            bounty_credits: _bounty,
            issuing_corp: _corp,
            reason: "Preemptive strike on strategic asset",
            status: "active"
        };'''
new_cc = '''        variable_struct_set(corporate_contracts, _pilot_id, {
            target_pilot_id: _pilot_id,
            bounty_credits: _bounty,
            issuing_corp: _corp,
            reason: "Preemptive strike on strategic asset",
            status: "active"
        });'''
s_nm = s_nm.replace(old_cc, new_cc)

with open(path_nm, 'w', encoding='utf-8') as f:
    f.write(s_nm)
print('Fixed obj_NemesisManager/Create_0.gml')
