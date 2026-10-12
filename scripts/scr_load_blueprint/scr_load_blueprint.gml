/// @function scr_load_blueprint(_file_name)
/// @description Resolves, loads, and parses a Mobile Suit blueprint JSON file into a GML struct with strict memory leak prevention.
/// @param {String} _file_name File name or relative path (e.g., "bp_ms_ironclad_07.json" or "blueprints/bp_ms_ironclad_07.json")
/// @returns {Struct|Undefined} Parsed blueprint struct, or undefined if loading or parsing fails.
function scr_load_blueprint(_file_name) {
    // 1. Resolve file path across common GameMaker bundle locations
    var _resolved_path = "";
    var _candidate_paths = [
        _file_name,
        "blueprints/" + _file_name,
        "datafiles/blueprints/" + _file_name,
        "datafiles/" + _file_name,
        working_directory + _file_name,
        working_directory + "blueprints/" + _file_name,
        working_directory + "datafiles/blueprints/" + _file_name
    ];

    var _len = array_length(_candidate_paths);
    for (var i = 0; i < _len; i++) {
        if (file_exists(_candidate_paths[i])) {
            _resolved_path = _candidate_paths[i];
            break;
        }
    }

    if (_resolved_path == "") {
        show_debug_message("[scr_load_blueprint] ERROR: File not found for target: " + string(_file_name));
        return undefined;
    }

    // 2. Load buffer and protect against memory leaks using try / catch / finally
    var _buf = -1;
    var _blueprint = undefined;

    try {
        _buf = buffer_load(_resolved_path);
        if (_buf == -1) {
            show_debug_message("[scr_load_blueprint] ERROR: Failed to allocate buffer for file: " + string(_resolved_path));
            return undefined;
        }

        var _buf_size = buffer_get_size(_buf);
        if (_buf_size <= 0) {
            show_debug_message("[scr_load_blueprint] ERROR: Blueprint file is empty (0 bytes): " + string(_resolved_path));
            return undefined;
        }

        // External JSON files are not null-terminated.
        // Use buffer_text instead of buffer_string to avoid buffer over-read defects.
        buffer_seek(_buf, buffer_seek_start, 0);
        var _json_string = buffer_read(_buf, buffer_text);

        // Parse JSON string into GML struct
        var _parsed = json_parse(_json_string);

        // Defensive validation: ensure root is a valid struct
        if (!is_struct(_parsed)) {
            show_debug_message("[scr_load_blueprint] ERROR: Parsed JSON root is not a struct in: " + string(_resolved_path));
            return undefined;
        }

        // Validate critical Mobile Suit blueprint schema fields
        if (!variable_struct_exists(_parsed, "blueprint_id")) {
            show_debug_message("[scr_load_blueprint] WARNING: Missing 'blueprint_id' property in: " + string(_resolved_path));
        }

        _blueprint = _parsed;
        show_debug_message("[scr_load_blueprint] SUCCESS: Loaded blueprint [" + string(_blueprint[$ "blueprint_id"] ?? "unknown") + "] (" + string(_blueprint[$ "name"] ?? "unnamed") + ")");
    }
    catch (_ex) {
        show_debug_message("[scr_load_blueprint] JSON PARSE ERROR: " + string(_ex.message));
        _blueprint = undefined;
    }
    finally {
        // Guarantee buffer cleanup to prevent memory leaks under all execution branches
        if (_buf != -1 && buffer_exists(_buf)) {
            buffer_delete(_buf);
            _buf = -1;
        }
    }

    return _blueprint;
}
