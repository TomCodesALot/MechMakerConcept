with open("scripts/scr_territory_war_system/scr_territory_war_system.gml", "r") as f:
    code = f.read()

# 1. Update scr_hex_get_stronghold_terrain
old_stamp = '''        _grid[_fc][_fr].terrain_type = "BASE_FACILITY";
        _grid[_fc][_fr].name = _sn.name;
        _grid[_fc][_fr].mp_cost = 1;
        _grid[_fc][_fr].defense_bonus = 40;
        _grid[_fc][_fr].facility_id = _sn.id;
        _grid[_fc][_fr].controlling_faction = _sn.controlling_faction;'''

new_stamp = '''        _grid[_fc][_fr].terrain_type = "BASE_FACILITY";
        _grid[_fc][_fr].name = _sn.name;
        _grid[_fc][_fr].mp_cost = 1;
        _grid[_fc][_fr].defense_bonus = 40;
        _grid[_fc][_fr].facility_id = _sn.id;
        _grid[_fc][_fr].controlling_faction = _sn.controlling_faction;
        _grid[_fc][_fr].sub_type = variable_struct_exists(_sn, "sub_type") ? _sn.sub_type : "DEPOT";
        _grid[_fc][_fr].is_core = variable_struct_exists(_sn, "is_core") ? _sn.is_core : false;
        _grid[_fc][_fr].capture_progress = (_sn.controlling_faction == "pmc") ? 100 : 0;
        _grid[_fc][_fr].capture_turns_required = (variable_struct_exists(_sn, "is_core") && _sn.is_core) ? 3 : 2;
        _grid[_fc][_fr].is_captured = (_sn.controlling_faction == "pmc");'''

assert old_stamp in code, "old_stamp not found in script"
code = code.replace(old_stamp, new_stamp)

# 2. Update scr_stronghold_advance_turn
old_advance_end = '''    // Refresh all active units MP and status
    for (var i = 0; i < array_length(_units_array); i++) {
        var _u = _units_array[i];
        if (_u.hp > 0) {
            _u.current_mp = _u.max_mp;
            _u.status = "READY";
        }
    }'''

new_advance_end = '''    // Facility Capture, Contestation & Field Repairs
    if (!is_undefined(_terrain_grid)) {
        var _sh_layout = scr_stronghold_get_layout(_stronghold_id);
        for (var c = 0; c < 16; c++) {
            for (var r = 0; r < 10; r++) {
                var _fac = _terrain_grid[c][r];
                if (_fac.terrain_type == "BASE_FACILITY") {
                    var _occ_u = undefined;
                    for (var u = 0; u < array_length(_units_array); u++) {
                        var _cand = _units_array[u];
                        if (_cand.hp > 0 && _cand.col == c && _cand.row == r) {
                            _occ_u = _cand;
                            break;
                        }
                    }

                    if (!is_undefined(_occ_u)) {
                        if (_occ_u.faction == "pmc") {
                            if (_fac.controlling_faction != "pmc") {
                                var _rate = floor(100.0 / _fac.capture_turns_required);
                                _fac.capture_progress = min(100, _fac.capture_progress + _rate);
                                if (_fac.capture_progress >= 100) {
                                    _fac.controlling_faction = "pmc";
                                    _fac.is_captured = true;
                                    array_push(_log, "★ SECTOR CAPTURED: " + _fac.name + " SECURED BY PMC!");
                                    for (var sni = 0; sni < array_length(_sh_layout.subnodes); sni++) {
                                        if (_sh_layout.subnodes[sni].id == _fac.facility_id) {
                                            _sh_layout.subnodes[sni].controlling_faction = "pmc";
                                        }
                                    }
                                    if (_fac.is_core || _fac.sub_type == "CORE_BUNKER") {
                                        array_push(_log, "🏆 VICTORY: CORE REACTOR SECURED! CITADEL LIBERATED!");
                                    }
                                } else {
                                    array_push(_log, "OCCUPATION: " + _fac.name + " CAPTURE GAUGE AT " + string(_fac.capture_progress) + "%");
                                }
                            } else {
                                if (_occ_u.hp < _occ_u.max_hp) {
                                    _occ_u.hp = min(_occ_u.max_hp, _occ_u.hp + 20);
                                    array_push(_log, "FIELD REPAIRS: " + _occ_u.unit_label + " REPAIRED (+20 HP) AT " + _fac.name);
                                }
                            }
                        } else if (_occ_u.faction != "pmc" && _fac.controlling_faction == "pmc") {
                            _fac.capture_progress = max(0, _fac.capture_progress - 50);
                            if (_fac.capture_progress <= 0) {
                                _fac.controlling_faction = _occ_u.faction;
                                _fac.is_captured = false;
                                array_push(_log, "⚠ ALERT: " + _fac.name + " RECAPTURED BY HOSTILE GARRISON!");
                            } else {
                                array_push(_log, "⚠ WARNING: HOSTILE MECHS CONTESTING " + _fac.name + "!");
                            }
                        }
                    }
                }
            }
        }
    }

    // Refresh all active units MP and status
    for (var i = 0; i < array_length(_units_array); i++) {
        var _u = _units_array[i];
        if (_u.hp > 0) {
            _u.current_mp = _u.max_mp;
            _u.status = "READY";
        }
    }'''

assert old_advance_end in code, "old_advance_end not found in script"
code = code.replace(old_advance_end, new_advance_end)

with open("scripts/scr_territory_war_system/scr_territory_war_system.gml", "w") as f:
    f.write(code)

print("Updated scr_territory_war_system.gml for Step 2 successfully!")
