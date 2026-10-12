/// @description scr_save_system
// Comprehensive JSON Save & Load Serialization for PMC Core Managers
// Adheres strictly to docs/01_core_architecture.md

/// @function scr_save_game(_slot_name)
/// @param {String} [_slot_name] Filename of save slot (default: "pmc_save_slot_1.json")
/// @returns {Bool} True if save succeeded, false otherwise
function scr_save_game(_slot_name = "pmc_save_slot_1.json") {
    try {
        var _save_data = {
            version: "1.0.0",
            timestamp: string(current_year) + "-" + string(current_month) + "-" + string(current_day),
            game_state: undefined,
            faction_state: undefined,
            blueprint_state: undefined
        };

        // 1. Pack obj_GameManager state
        if (instance_exists(obj_GameManager)) {
            _save_data.game_state = {
                funds: obj_GameManager.funds,
                escrow_funds: obj_GameManager.escrow_funds,
                current_cycle_year: obj_GameManager.current_cycle_year,
                current_cycle_day: obj_GameManager.current_cycle_day,
                time_speed: obj_GameManager.time_speed,
                pmc_profile: obj_GameManager.pmc_profile,
                inventory: obj_GameManager.inventory,
                facilities: obj_GameManager.facilities
            };
        }

        // 2. Pack obj_FactionManager state
        if (instance_exists(obj_FactionManager)) {
            _save_data.faction_state = {
                faction_standing: obj_FactionManager.faction_standing,
                factions: obj_FactionManager.factions,
                active_contracts: obj_FactionManager.active_contracts,
                available_contracts: obj_FactionManager.available_contracts
            };
        }

        // 3. Pack obj_BlueprintManager state
        if (instance_exists(obj_BlueprintManager)) {
            _save_data.blueprint_state = {
                unlocked_blueprints: obj_BlueprintManager.unlocked_blueprints,
                unlocked_components: obj_BlueprintManager.unlocked_components,
                unlocked_recipes: obj_BlueprintManager.unlocked_recipes,
                masterwork_inventory: obj_BlueprintManager.masterwork_inventory
            };
        }

        // 4. Serialize to JSON string
        var _json_string = json_stringify(_save_data);
        var _file = file_text_open_write(_slot_name);
        if (_file != -1) {
            file_text_write_string(_file, _json_string);
            file_text_close(_file);
            show_debug_message("[scr_save_system] Game successfully serialized to '" + string(_slot_name) + "'");
            if (instance_exists(obj_HQTerminal)) {
                obj_HQTerminal.show_toast("PROGRESS SAVED: '" + string(_slot_name) + "'", c_lime);
            }
            return true;
        } else {
            show_debug_message("[scr_save_system] ERROR: Could not open file '" + string(_slot_name) + "' for writing.");
            return false;
        }
    } catch (_ex) {
        show_debug_message("[scr_save_system] EXCEPTION during save: " + string(_ex));
        return false;
    }
}

/// @function scr_load_game(_slot_name)
/// @param {String} [_slot_name] Filename of save slot (default: "pmc_save_slot_1.json")
/// @returns {Bool} True if load succeeded, false otherwise
function scr_load_game(_slot_name = "pmc_save_slot_1.json") {
    try {
        if (!file_exists(_slot_name)) {
            show_debug_message("[scr_save_system] Load aborted: File '" + string(_slot_name) + "' does not exist.");
            if (instance_exists(obj_HQTerminal)) {
                obj_HQTerminal.show_toast("NO SAVE FOUND: '" + string(_slot_name) + "'", c_orange);
            }
            return false;
        }

        var _file = file_text_open_read(_slot_name);
        var _json_string = "";
        while (!file_text_eof(_file)) {
            _json_string += file_text_readln(_file);
        }
        file_text_close(_file);

        var _save_data = json_parse(_json_string);
        if (!is_struct(_save_data)) {
            show_debug_message("[scr_save_system] ERROR: Invalid JSON structure in '" + string(_slot_name) + "'");
            return false;
        }

        // 1. Unpack into obj_GameManager
        if (instance_exists(obj_GameManager) && is_struct(_save_data[$ "game_state"])) {
            var _gs = _save_data.game_state;
            if (variable_struct_exists(_gs, "funds")) obj_GameManager.funds = _gs.funds;
            if (variable_struct_exists(_gs, "escrow_funds")) obj_GameManager.escrow_funds = _gs.escrow_funds;
            if (variable_struct_exists(_gs, "current_cycle_year")) obj_GameManager.current_cycle_year = _gs.current_cycle_year;
            if (variable_struct_exists(_gs, "current_cycle_day")) obj_GameManager.current_cycle_day = _gs.current_cycle_day;
            if (variable_struct_exists(_gs, "time_speed")) obj_GameManager.time_speed = _gs.time_speed;
            if (variable_struct_exists(_gs, "pmc_profile")) obj_GameManager.pmc_profile = _gs.pmc_profile;
            if (variable_struct_exists(_gs, "inventory")) obj_GameManager.inventory = _gs.inventory;
            if (variable_struct_exists(_gs, "facilities")) obj_GameManager.facilities = _gs.facilities;
        }

        // 2. Unpack into obj_FactionManager
        if (instance_exists(obj_FactionManager) && is_struct(_save_data[$ "faction_state"])) {
            var _fs = _save_data.faction_state;
            if (variable_struct_exists(_fs, "faction_standing")) obj_FactionManager.faction_standing = _fs.faction_standing;
            if (variable_struct_exists(_fs, "factions")) obj_FactionManager.factions = _fs.factions;
            if (variable_struct_exists(_fs, "active_contracts")) obj_FactionManager.active_contracts = _fs.active_contracts;
            if (variable_struct_exists(_fs, "available_contracts")) obj_FactionManager.available_contracts = _fs.available_contracts;
        }

        // 3. Unpack into obj_BlueprintManager
        if (instance_exists(obj_BlueprintManager) && is_struct(_save_data[$ "blueprint_state"])) {
            var _bs = _save_data.blueprint_state;
            if (variable_struct_exists(_bs, "unlocked_blueprints")) obj_BlueprintManager.unlocked_blueprints = _bs.unlocked_blueprints;
            if (variable_struct_exists(_bs, "unlocked_components")) obj_BlueprintManager.unlocked_components = _bs.unlocked_components;
            if (variable_struct_exists(_bs, "unlocked_recipes")) obj_BlueprintManager.unlocked_recipes = _bs.unlocked_recipes;
            if (variable_struct_exists(_bs, "masterwork_inventory")) obj_BlueprintManager.masterwork_inventory = _bs.masterwork_inventory;
        }

        show_debug_message("[scr_save_system] Game successfully restored from '" + string(_slot_name) + "'");
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("GAME LOADED: '" + string(_slot_name) + "'", c_cyan);
        }
        return true;
    } catch (_ex) {
        show_debug_message("[scr_save_system] EXCEPTION during load: " + string(_ex));
        return false;
    }
}
