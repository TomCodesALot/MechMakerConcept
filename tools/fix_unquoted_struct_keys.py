with open('objects/obj_GameManager/Create_0.gml', 'r') as f:
    code = f.read()

target = '''    var _hb = variable_struct_exists(facilities, hangar_bays) ? facilities.hangar_bays : (variable_struct_exists(facilities, assembly_lines) ? facilities.assembly_lines : 1);
    var _lt = variable_struct_exists(facilities, lab_tier) ? facilities.lab_tier : ((variable_struct_exists(facilities, containment_shielding) && facilities.containment_shielding) ? 2 : 1);
    var _fc = variable_struct_exists(facilities, foundry_crucibles) ? facilities.foundry_crucibles : (variable_struct_exists(facilities, crucible_tier) ? facilities.crucible_tier : 1);'''

replacement = '''    var _hb = variable_struct_exists(facilities, "hangar_bays") ? facilities.hangar_bays : (variable_struct_exists(facilities, "assembly_lines") ? facilities.assembly_lines : 1);
    var _lt = variable_struct_exists(facilities, "lab_tier") ? facilities.lab_tier : ((variable_struct_exists(facilities, "containment_shielding") && facilities.containment_shielding) ? 2 : 1);
    var _fc = variable_struct_exists(facilities, "foundry_crucibles") ? facilities.foundry_crucibles : (variable_struct_exists(facilities, "crucible_tier") ? facilities.crucible_tier : 1);'''

assert target in code, "Target block not found in objects/obj_GameManager/Create_0.gml"
code = code.replace(target, replacement)

with open('objects/obj_GameManager/Create_0.gml', 'w') as f:
    f.write(code)

print("Successfully replaced unquoted struct keys with properly quoted strings!")
