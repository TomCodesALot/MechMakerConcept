path = "objects/obj_HQTerminal/Draw_64.gml"
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    'var _is_dorm = (variable_struct_get(_fm.factions, _fid)[$ "is_dormant"] ?? false);',
    'var _is_dorm = (variable_struct_get(variable_struct_get(_fm.factions, _fid), "is_dormant") ?? false);'
)
text = text.replace(
    'var _p_name1 = (variable_struct_get(_fm.factions, _rel.faction_1)[$ "short_name"] ?? _rel.name_1);',
    'var _p_name1 = (variable_struct_get(variable_struct_get(_fm.factions, _rel.faction_1), "short_name") ?? _rel.name_1);'
)
text = text.replace(
    'var _p_name2 = (variable_struct_get(_fm.factions, _rel.faction_2)[$ "short_name"] ?? _rel.name_2);',
    'var _p_name2 = (variable_struct_get(variable_struct_get(_fm.factions, _rel.faction_2), "short_name") ?? _rel.name_2);'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Remaining in Draw_64:", text.count("[$"))
