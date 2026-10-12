/// @description Procedural Alloy Discovery Codex & Combinatorial Metallurgy Engine
// Analyzes multi-element mineral recipes across the 118-element periodic table.
// Synthesizes dynamic physical stats, procedural nomenclature, failure thresholds, and chromatic signatures.
// Adheres to docs/02_alloy_chemistry.md and docs/14_procedural_materials_and_deep_metallurgy.md

/// @function scr_alloy_discovery_analyze(_input_struct, _opt_temp, _opt_pressure)
function scr_alloy_discovery_analyze(_input_struct, _opt_temp = 2500, _opt_pressure = 1000) {
    if (!is_struct(_input_struct)) {
        return {
            name: "Unrefined Slag Residue",
            code: "ERR-SLAG-00",
            tier: 1,
            armor_hp: 120,
            thermal_rate: 10.0,
            density_g_cm3: 3.5,
            superconductivity: 0.0,
            radar_absorb_pct: 0.05,
            is_failure: true,
            failure_reason: "Empty or invalid hopper inputs.",
            color: make_color_rgb(65, 55, 50),
            hex: "#413732",
            formula_summary: "No components"
        };
    }

    var _keys = variable_struct_get_names(_input_struct);
    var _tot_parts = 0;
    var _dominant_key = "";
    var _secondary_key = "";
    var _max_qty = 0;
    var _sec_qty = 0;

    // Element Totals & Dominance Scan
    for (var k = 0; k < array_length(_keys); k++) {
        var _kname = _keys[k];
        var _q = _input_struct[$ _kname];
        if (!is_numeric(_q) || _q <= 0) continue;

        _tot_parts += _q;
        if (_q > _max_qty) {
            _secondary_key = _dominant_key;
            _sec_qty = _max_qty;
            _dominant_key = _kname;
            _max_qty = _q;
        } else if (_q > _sec_qty) {
            _secondary_key = _kname;
            _sec_qty = _q;
        }
    }

    if (_tot_parts <= 0) {
        return {
            name: "Unrefined Slag Residue",
            code: "ERR-SLAG-00",
            tier: 1,
            armor_hp: 120,
            thermal_rate: 10.0,
            density_g_cm3: 3.5,
            superconductivity: 0.0,
            radar_absorb_pct: 0.05,
            is_failure: true,
            failure_reason: "Hopper contains zero usable metal mass.",
            color: make_color_rgb(65, 55, 50),
            hex: "#413732",
            formula_summary: "Empty"
        };
    }

    // Baseline Metallurgy Accumulators
    var _sum_tensile = 0.0;
    var _sum_melting = 0.0;
    var _sum_density = 0.0;
    var _sum_conduct = 0.0;
    var _carbon_ratio = 0.0;
    var _volatile_ratio = 0.0;
    var _flux_ratio = 0.0;

    for (var k = 0; k < array_length(_keys); k++) {
        var _kname = _keys[k];
        var _qty = _input_struct[$ _kname];
        if (!is_numeric(_qty) || _qty <= 0) continue;
        var _fraction = _qty / _tot_parts;

        // Attribute defaults based on material name patterns
        var _ten = 600.0;
        var _melt = 1500.0;
        var _dens = 7.8;
        var _cond = 50.0;

        if (string_pos("w", _kname) > 0 || string_pos("tungsten", _kname) > 0) {
            _ten = 1510.0; _melt = 3422.0; _dens = 19.3; _cond = 173.0;
        } else if (string_pos("ti", _kname) > 0 || string_pos("titanium", _kname) > 0) {
            _ten = 950.0; _melt = 1668.0; _dens = 4.5; _cond = 22.0;
        } else if (string_pos("c", _kname) > 0 || string_pos("carbon", _kname) > 0 || string_pos("graphene", _kname) > 0 || string_pos("silica", _kname) > 0) {
            _ten = 1800.0; _melt = 3550.0; _dens = 2.3; _cond = 140.0;
            _carbon_ratio += _fraction;
        } else if (string_pos("tritium", _kname) > 0 || string_pos("h", _kname) > 0 || string_pos("deuterium", _kname) > 0) {
            _ten = 50.0; _melt = 50.0; _dens = 0.5; _cond = 280.0;
            _volatile_ratio += _fraction;
        } else if (string_pos("flux", _kname) > 0 || string_pos("y", _kname) > 0 || string_pos("nd", _kname) > 0) {
            _ten = 450.0; _melt = 1520.0; _dens = 4.8; _cond = 120.0;
            _flux_ratio += _fraction;
        } else if (string_pos("os", _kname) > 0 || string_pos("ir", _kname) > 0) {
            _ten = 1750.0; _melt = 3033.0; _dens = 22.6; _cond = 87.0;
        }

        _sum_tensile += _ten * _fraction;
        _sum_melting += _melt * _fraction;
        _sum_density += _dens * _fraction;
        _sum_conduct += _cond * _fraction;
    }

    // Thermal & Compaction Multipliers
    var _press_factor = clamp(_opt_pressure / 8000.0, 0.0, 1.4);
    var _heat_factor = clamp((_opt_temp - 1200) / 3500.0, 0.0, 1.5);

    // Failure Boundary Checks
    var _is_failure = false;
    var _failure_reason = "";

    if (_volatile_ratio > 0.35 && _flux_ratio < 0.15 && _opt_temp > 3500) {
        _is_failure = true;
        _failure_reason = "VOLATILIZATION BURNOUT: Unstabilized plasma leaked through thermal seals.";
    } else if (_carbon_ratio > 0.40 && _opt_pressure < 1500) {
        _is_failure = true;
        _failure_reason = "BRITTLE FRACTURE: Excess carbon formed needle cementite crystals under low pressure.";
    } else if (_opt_temp > _sum_melting + 1400 && _flux_ratio < 0.10) {
        _is_failure = true;
        _failure_reason = "SLAG BURNOUT: Superheated core boiled off structural crystalline matrices.";
    }

    // Final Derived Properties
    var _armor_rating = floor((_sum_tensile * (1.0 + _press_factor * 0.35)) * (_is_failure ? 0.25 : 1.0));
    var _thermal_dissip = clamp(_sum_conduct * 0.32 * (_is_failure ? 0.3 : 1.0), 10.0, 95.0);
    var _density_mod = _sum_density;
    var _supercon = clamp((_volatile_ratio * 1.5 + _flux_ratio * 2.0) * (_opt_pressure / 6000.0), 0.0, 2.5);
    var _radar_stealth = clamp(_carbon_ratio * 0.45, 0.0, 0.50);

    // Procedural Nomenclature Engine
    var _prefix = "Vanguard";
    if (string_pos("ti", _dominant_key) > 0 || string_pos("titanium", _dominant_key) > 0) _prefix = "Aether";
    else if (string_pos("c", _dominant_key) > 0 || string_pos("carbon", _dominant_key) > 0) _prefix = "Obsidian";
    else if (string_pos("tr", _dominant_key) > 0 || string_pos("tritium", _dominant_key) > 0) _prefix = "Hyperion";
    else if (string_pos("os", _dominant_key) > 0 || string_pos("ir", _dominant_key) > 0) _prefix = "Adamantine";
    else if (string_pos("flux", _dominant_key) > 0 || string_pos("y", _dominant_key) > 0) _prefix = "Sol-Flux";
    else if (string_pos("th", _dominant_key) > 0 || string_pos("u", _dominant_key) > 0) _prefix = "Actinide";

    var _suffix = "Composite Plate";
    if (_supercon > 1.0) _suffix = "Tokamak Superconductor Matrix";
    else if (_radar_stealth > 0.25) _suffix = "Stealth Nanomesh Ceramite";
    else if (_density_mod > 14.0) _suffix = "Heavy Osmiridium Bastion Plating";
    else if (_density_mod < 4.0) _suffix = "Ultra-Light Aerosteel Vernier Laminate";

    var _alloy_name = _is_failure ? "Degraded Slag Slurry" : (_prefix + " " + _suffix);
    var _code = "AL-" + string_upper(string_copy(_dominant_key, 1, 3)) + "-" + string(floor(_tot_parts)) + "-MK" + string(ceil(_armor_rating / 300));

    // Dynamic Color Signature
    var _alloy_color = _is_failure ? make_color_rgb(70, 55, 48) : scr_get_alloy_procedural_color(_input_struct, _opt_temp, _opt_pressure);
    var _alloy_hex = _is_failure ? "#463730" : scr_alloy_get_hex(_input_struct);

    // Formula Summary String
    var _form_str = "";
    for (var sk = 0; sk < array_length(_keys); sk++) {
        var _k = _keys[sk];
        var _amt = _input_struct[$ _k];
        if (is_numeric(_amt) && _amt > 0) {
            _form_str += string(_amt) + "x " + string_upper(_k) + " ";
        }
    }

    return {
        name: _alloy_name,
        code: _code,
        tier: clamp(floor(_armor_rating / 350) + 1, 1, 5),
        armor_hp: _armor_rating,
        thermal_rate: _thermal_dissip,
        density_g_cm3: _density_mod,
        superconductivity: _supercon,
        radar_absorb_pct: _radar_stealth,
        is_failure: _is_failure,
        failure_reason: _failure_reason,
        color: _alloy_color,
        hex: _alloy_hex,
        formula_summary: _form_str,
        raw_inputs: _input_struct
    };
}

/// @function scr_alloy_codex_register_discovery(_analysis_struct)
function scr_alloy_codex_register_discovery(_analysis_struct) {
    if (!is_struct(_analysis_struct) || _analysis_struct.is_failure) return false;
    if (!instance_exists(obj_BlueprintManager)) return false;

    var _bm = obj_BlueprintManager;
    if (!variable_instance_exists(_bm, "discovered_alloy_codex")) {
        _bm.discovered_alloy_codex = [];
    }

    // Check if fingerprint or code is already in codex
    var _code = _analysis_struct.code;
    for (var i = 0; i < array_length(_bm.discovered_alloy_codex); i++) {
        if (_bm.discovered_alloy_codex[i].code == _code) {
            return false; // Already discovered
        }
    }

    array_push(_bm.discovered_alloy_codex, _analysis_struct);
    show_debug_message("[scr_alloy_discovery_codex] New Alloy Registered: " + _analysis_struct.name + " (" + _code + ")");

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("NEW ALLOY DISCOVERED: " + _analysis_struct.name + " (" + _analysis_struct.hex + ")!", c_yellow);
    }
    return true;
}

/// @function scr_alloy_codex_get_all()
function scr_alloy_codex_get_all() {
    if (instance_exists(obj_BlueprintManager) && variable_instance_exists(obj_BlueprintManager, "discovered_alloy_codex")) {
        return obj_BlueprintManager.discovered_alloy_codex;
    }
    return [];
}
