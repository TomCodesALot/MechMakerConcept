with open("objects/obj_BattleManager/Create_0.gml", "r") as f:
    code = f.read()

old_calc = """calculate_hit_chance = function(_atk, _def, _dist) {
    var _base = _atk.accuracy;
    var _eva = _def.evasion;"""

new_calc = """calculate_hit_chance = function(_atk, _def, _dist, _wpn = undefined) {
    var _base = _atk.accuracy;
    var _eva = _def.evasion;

    // Suppression aim penalty (Goal F)
    if (variable_struct_exists(_atk, "is_suppressed") && _atk.is_suppressed) {
        _base -= 20;
    }

    // Directional facing hit modifiers (Goal F)
    var _inc_dir = iso_get_facing(_def.grid_c, _def.grid_r, _atk.grid_c, _atk.grid_r);
    var _is_rear = (_inc_dir == (_def.facing + 2) % 4);
    var _is_flank = (_inc_dir == (_def.facing + 1) % 4 || _inc_dir == (_def.facing + 3) % 4);
    if (_is_rear) {
        _base += 30;
    } else if (_is_flank) {
        _base += 15;
    }"""

assert old_calc in code, "old_calc not found"
code = code.replace(old_calc, new_calc, 1)

old_cov = """    var _cov = (grid_cover[_def.grid_c][_def.grid_r] == 1) ? 25 : ((grid_cover[_def.grid_c][_def.grid_r] == 2) ? 40 : 0);"""

new_cov = """    var _cov = (grid_cover[_def.grid_c][_def.grid_r] == 1) ? 25 : ((grid_cover[_def.grid_c][_def.grid_r] == 2) ? 40 : 0);
    if (!is_undefined(_wpn) && variable_struct_exists(_wpn, "proj_type")) {
        if (_wpn.proj_type == "KINETIC_CANNON" || _wpn.proj_type == "MISSILE" || _wpn.proj_type == "TACHYON_BEAM") {
            _cov = floor(_cov * 0.50);
        }
    }"""

assert old_cov in code, "old_cov not found"
code = code.replace(old_cov, new_cov, 1)

with open("objects/obj_BattleManager/Create_0.gml", "w") as f:
    f.write(code)

print("Updated calculate_hit_chance with Goal F suppression, directional facing, and cover penetration.")
