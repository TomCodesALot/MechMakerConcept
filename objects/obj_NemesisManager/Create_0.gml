/// @description obj_NemesisManager Create Event
// Singleton Relational Graph Manager, Monolith Nemesis Engine & Dynamic Roster State
// Strictly implements Document 19: Pilot Nemesis System & Dynamic Character Relationship Web

// 1. Singleton Pattern Enforcement
if (instance_number(obj_NemesisManager) > 1) {
    show_debug_message("[obj_NemesisManager] Duplicate instance detected. Self-terminating.");
    instance_destroy();
    exit;
}

show_debug_message("[obj_NemesisManager] ========================================");
show_debug_message("[obj_NemesisManager] Initializing Relational Nemesis Graph Engine");
show_debug_message("[obj_NemesisManager] ========================================");

// 2. Core Relational State & Data Structures
characters_map     = {};
character_id_list  = [];
active_nemeses     = []; // Array of { pilot_id, target_id, cause, declared_turn }
prisoner_list      = []; // Array of captive pilot structs
executed_list      = []; // Array of permanently executed pilot IDs
campaign_seed      = 1337;

faction_rosters    = {
    faction_terran: [],
    faction_colony: [],
    faction_syndicate: [],
    faction_zaibatsu: [],
    independent: []
};

// 3. Resolve & Ingest Master Character Database (204 Figures)
var _candidate_paths = [
    "characters_roster.json",
    "datafiles/characters_roster.json",
    working_directory + "characters_roster.json",
    working_directory + "datafiles/characters_roster.json"
];

var _resolved_path = "";
for (var p = 0; p < array_length(_candidate_paths); p++) {
    if (file_exists(_candidate_paths[p])) {
        _resolved_path = _candidate_paths[p];
        break;
    }
}

if (_resolved_path == "") {
    show_debug_message("[obj_NemesisManager] CRITICAL WARNING: characters_roster.json not found in candidate paths!");
} else {
    var _buf = -1;
    try {
        _buf = buffer_load(_resolved_path);
        if (_buf != -1 && buffer_get_size(_buf) > 0) {
            buffer_seek(_buf, buffer_seek_start, 0);
            var _json_str = buffer_read(_buf, buffer_text);
            var _parsed = json_parse(_json_str);

            if (is_struct(_parsed) && variable_struct_exists(_parsed, "characters")) {
                var _chars = _parsed.characters;
                var _count = array_length(_chars);

                for (var i = 0; i < _count; i++) {
                    var _c = _chars[i];
                    // Dynamic initialization flags
                    _c.grudge = _c[$ "grudge"] ?? 0;
                    _c.combat_trauma_mode = "";
                    _c.current_faction_id = _c.faction_id;

                    characters_map[$ _c.id] = _c;
                    array_push(character_id_list, _c.id);
                }
                show_debug_message("[obj_NemesisManager] Successfully ingested " + string(_count) + " figures into Relational Graph from " + _resolved_path);
            }
        }
    } catch (_ex) {
        show_debug_message("[obj_NemesisManager] JSON PARSE ERROR: " + string(_ex.message));
    } finally {
        if (_buf != -1 && buffer_exists(_buf)) {
            buffer_delete(_buf);
        }
    }
}

// 4. Initialize Procedural Allegiance Variance for Initial Campaign Seed
scr_campaign_seed_allegiance_roll(campaign_seed);

// 5. Manager Query & Mutation Methods
get_character = function(_id) {
    if (variable_struct_exists(characters_map, _id)) {
        return characters_map[$ _id];
    }
    return undefined;
};

get_faction_pilots = function(_faction_id, _recruitable_only) {
    var _res = [];
    if (!variable_struct_exists(faction_rosters, _faction_id)) return _res;

    var _ids = faction_rosters[$ _faction_id];
    for (var i = 0; i < array_length(_ids); i++) {
        var _c = characters_map[$ _ids[i]];
        if (is_struct(_c)) {
            if (!_recruitable_only || _c.is_recruitable) {
                if (_c.is_alive && !_c.is_imprisoned) {
                    array_push(_res, _c);
                }
            }
        }
    }
    return _res;
};

get_active_nemeses = function() {
    return active_nemeses;
};

is_nemesis_active = function(_pilot_id) {
    for (var i = 0; i < array_length(active_nemeses); i++) {
        if (active_nemeses[i].pilot_id == _pilot_id) return true;
    }
    return false;
};

get_prisoners = function() {
    return prisoner_list;
};

add_prisoner = function(_pilot_id) {
    var _c = get_character(_pilot_id);
    if (!is_undefined(_c)) {
        _c.is_imprisoned = true;
        for (var i = 0; i < array_length(prisoner_list); i++) {
            if (prisoner_list[i].id == _pilot_id) return;
        }
        array_push(prisoner_list, _c);
        show_debug_message("[obj_NemesisManager] Incarcerated pilot " + _c.name + " in PMC base brig.");
    }
};

execute_prisoner = function(_pilot_id) {
    return scr_prisoner_triage(_pilot_id, "execute");
};

ransom_prisoner = function(_pilot_id) {
    return scr_prisoner_triage(_pilot_id, "ransom");
};

recruit_prisoner = function(_pilot_id) {
    return scr_prisoner_triage(_pilot_id, "recruit");
};

show_debug_message("[obj_NemesisManager] Manager online with " + string(array_length(character_id_list)) + " characters indexed.");
