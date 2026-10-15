import re

GM_PATH = "objects/obj_GameManager/Create_0.gml"

with open(GM_PATH, "r") as f:
    content = f.read()

target_marker = "init_competitor_catalog();"

insertion = """init_competitor_catalog();

// =============================================================================
// EXPANDED MOBILE SUIT UNIVERSE & CATALOG ENGINE (docs/29)
// =============================================================================
mobile_suit_catalog = {};

init_master_mobile_suit_catalog = function() {
    var _loaded = false;
    var _paths = ["mobile_suits/mobile_suit_catalog.json", "mobile_suit_catalog.json"];
    for (var p = 0; p < array_length(_paths); p++) {
        var _fp = _paths[p];
        if (file_exists(_fp)) {
            try {
                var _buf = buffer_load(_fp);
                var _str = buffer_read(_buf, buffer_string);
                buffer_delete(_buf);
                var _parsed = json_parse(_str);
                if (is_struct(_parsed)) {
                    mobile_suit_catalog = _parsed;
                    _loaded = true;
                    show_debug_message("[obj_GameManager] Successfully loaded " + string(variable_struct_names_count(mobile_suit_catalog)) + " mobile suits from " + _fp);
                    break;
                }
            } catch (_ex) {
                show_debug_message("[obj_GameManager] Error loading " + _fp + ": " + string(_ex));
            }
        }
    }

    if (!_loaded || variable_struct_names_count(mobile_suit_catalog) == 0) {
        show_debug_message("[obj_GameManager] Initializing catalog fallback memory.");
    }
};

get_mobile_suit = function(_id) {
    if (is_struct(mobile_suit_catalog) && variable_struct_exists(mobile_suit_catalog, _id)) {
        return mobile_suit_catalog[$ _id];
    }
    return undefined;
};

get_suits_by_faction = function(_faction_id) {
    var _res = [];
    if (!is_struct(mobile_suit_catalog)) return _res;
    var _names = variable_struct_get_names(mobile_suit_catalog);
    for (var i = 0; i < array_length(_names); i++) {
        var _suit = mobile_suit_catalog[$ _names[i]];
        if (is_struct(_suit) && _suit[$ "faction_id"] == _faction_id) {
            array_push(_res, _suit);
        }
    }
    return _res;
};

get_mass_production_candidates = function(_faction_id) {
    var _res = [];
    if (!is_struct(mobile_suit_catalog)) return _res;
    var _names = variable_struct_get_names(mobile_suit_catalog);
    for (var i = 0; i < array_length(_names); i++) {
        var _suit = mobile_suit_catalog[$ _names[i]];
        if (is_struct(_suit) && _suit[$ "faction_id"] == _faction_id && (_suit[$ "mass_production_line"] ?? false)) {
            array_push(_res, _suit);
        }
    }
    return _res;
};

get_suits_by_era = function(_era) {
    var _res = [];
    if (!is_struct(mobile_suit_catalog)) return _res;
    var _names = variable_struct_get_names(mobile_suit_catalog);
    for (var i = 0; i < array_length(_names); i++) {
        var _suit = mobile_suit_catalog[$ _names[i]];
        if (is_struct(_suit) && _suit[$ "era"] == _era) {
            array_push(_res, _suit);
        }
    }
    return _res;
};

init_master_mobile_suit_catalog();"""

assert target_marker in content, "target_marker not found in obj_GameManager!"
content = content.replace(target_marker, insertion, 1)

with open(GM_PATH, "w") as f:
    f.write(content)

print("Updated obj_GameManager with init_master_mobile_suit_catalog!")
