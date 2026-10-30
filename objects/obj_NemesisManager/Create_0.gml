var _log_f = file_text_open_append("boot_log.txt");
file_text_write_string(_log_f, "[BOOT] obj_NemesisManager Create event started!\n");
file_text_close(_log_f);
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
                    _c.grudge = variable_struct_get(_c, "grudge") ?? 0;
                    _c.combat_trauma_mode = "";
                    _c.current_faction_id = _c.faction_id;
                    if (!variable_struct_exists(_c, "allegiance_variance") || !is_struct(_c.allegiance_variance)) {
                        _c.allegiance_variance = {
                            canonical_faction: _c.faction_id,
                            ideological_loyalty: "diehard_purist",
                            flexibility_score: 0.0,
                            playthrough_weights: {},
                            defection_hooks: {}
                        };
                    }

                    variable_struct_set(characters_map, _c.id, _c);
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
        return variable_struct_get(characters_map, _id);
    }
    return undefined;
};

get_faction_pilots = function(_faction_id, _recruitable_only) {
    var _res = [];
    if (!variable_struct_exists(faction_rosters, _faction_id)) return _res;

    var _ids = variable_struct_get(faction_rosters, _faction_id);
    for (var i = 0; i < array_length(_ids); i++) {
        var _c = variable_struct_get(characters_map, _ids[i]);
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

add_prisoner = function(_pilot_id, _name = "Corporate Operative", _corp_id = "corp_vhi") {
    var _c = get_character(_pilot_id);
    if (!is_undefined(_c)) {
        _c.is_imprisoned = true;
        for (var i = 0; i < array_length(prisoner_list); i++) {
            if (prisoner_list[i].id == _pilot_id) return;
        }
        array_push(prisoner_list, _c);
        show_debug_message("[obj_NemesisManager] Incarcerated pilot " + _c.name + " in PMC base brig.");
    } else {
        var _spy = {
            id: _pilot_id,
            name: _name,
            callsign: "SHADOW",
            faction_id: "independent",
            contractor_corp_id: _corp_id,
            is_imprisoned: true,
            is_alive: true,
            morale: 40,
            role: "Corporate Infiltration Agent"
        };
        for (var i = 0; i < array_length(prisoner_list); i++) {
            if (prisoner_list[i].id == _pilot_id) return;
        }
        array_push(prisoner_list, _spy);
        variable_struct_set(characters_map, _pilot_id, _spy);
        show_debug_message("[obj_NemesisManager] Incarcerated operative " + _name + " in PMC base brig.");
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

// Corporate Hit Contracts & Interrogation Methods (docs/28)
corporate_contracts = {};

assign_corporate_contract = function(_pilot_id, _corp_id, _bounty_desc) {
    var _c = get_character(_pilot_id);
    if (!is_undefined(_c)) {
        _c.contractor_corp_id = _corp_id;
        _c.corporate_bounty_desc = _bounty_desc;
        variable_struct_set(corporate_contracts, _pilot_id, {
            pilot_id: _pilot_id,
            corp_id: _corp_id,
            bounty_desc: _bounty_desc,
            assigned_turn: (instance_exists(obj_GameManager)) ? obj_GameManager.current_turn : 1
        });
        show_debug_message("[obj_NemesisManager] Assigned Corporate Hit Contract: " + _c.name + " hired by " + _corp_id);
        return true;
    }
    return false;
};

interrogate_corporate_secrets = function(_pilot_id) {
    var _c = get_character(_pilot_id);
    if (is_undefined(_c) || !variable_struct_exists(_c, "is_imprisoned") || !_c.is_imprisoned) return false;
    var _corp = variable_struct_get(_c, "contractor_corp_id") ?? "corp_vhi";
    if (instance_exists(obj_GameManager)) {
        var _gm = obj_GameManager;
        if (variable_struct_exists(_gm.rival_corporations, _corp)) {
            var _rc = variable_struct_get(_gm.rival_corporations, _corp);
            // Grant 2,000 insider equity shares
            if (!_rc.is_acquired) {
                _rc.player_shares = min(100000, _rc.player_shares + 2000);
                _rc.player_equity_pct = (_rc.player_shares / 100000.0) * 100.0;
                if (_rc.player_equity_pct >= 51.0) _rc.controlling_interest = true;
            }
        }
        _gm.funds += 125000; // Industrial secret black market sale
    }
    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("INTERROGATION SUCCESS: Extracted " + _c.name + " industrial telemetry (+2,000 " + _corp + " shares, +125,000 Cr)!", c_lime);
    }
    return true;
};

ransom_to_corporation = function(_pilot_id) {
    var _c = get_character(_pilot_id);
    if (is_undefined(_c) || !variable_struct_exists(_c, "is_imprisoned") || !_c.is_imprisoned) return false;
    var _corp = variable_struct_get(_c, "contractor_corp_id") ?? "corp_vhi";
    var _payout = 250000;
    if (instance_exists(obj_GameManager)) {
        obj_GameManager.funds += _payout;
    }
    // Remove prisoner
    for (var i = 0; i < array_length(prisoner_list); i++) {
        if (prisoner_list[i].id == _pilot_id) {
            array_delete(prisoner_list, i, 1);
            break;
        }
    }
    _c.is_imprisoned = false;
    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("CORPORATE RANSOM EXCHANGED: " + _c.name + " released to " + _corp + " (+" + string(_payout) + " Cr)!", c_yellow);
    }
    return true;
};

// 7. Corporate Espionage, Shadow Raids & Nemesis Ace Retaliation Engine (Goal E)
evaluate_corporate_espionage_turn = function() {
    if (!instance_exists(obj_GameManager)) return false;
    var _gm = obj_GameManager;

    var _corps = [
        { id: "corp_vhi", name: "Vanguard Heavy Industries", faction: "faction_terran", candidate_ids: ["pilot_terran_cole", "char_terran_claire_vance"] },
        { id: "corp_aod", name: "Astraea Orbital Dynamics", faction: "faction_colony", candidate_ids: ["char_colony_cassian", "pilot_colony_sorren"] },
        { id: "corp_rust", name: "Rustworks Scrap Forge", faction: "faction_syndicate", candidate_ids: ["pilot_syndicate_jackal", "char_syndicate_cruz"] },
        { id: "corp_hats", name: "Hyperion Advanced Tech", faction: "faction_zaibatsu", candidate_ids: ["pilot_zaibatsu_null07", "char_zaibatsu_takahashi"] }
    ];

    for (var ci = 0; ci < array_length(_corps); ci++) {
        var _corp = _corps[ci];
        var _rc = variable_struct_exists(_gm.rival_corporations, _corp.id) ? variable_struct_get(_gm.rival_corporations, _corp.id) : undefined;
        if (is_undefined(_rc) || _rc.is_acquired) continue;

        // Calculate Corporate Threat / Encroachment Tension
        var _tension = 0;
        if (_rc.player_equity_pct >= 51.0) _tension += 65;
        else if (_rc.player_equity_pct >= 25.0) _tension += 40;
        else if (_rc.player_equity_pct >= 10.0) _tension += 20;

        if (instance_exists(obj_FactionManager)) {
            var _mp_f = variable_struct_exists(obj_FactionManager.mass_production_contracts, _corp.faction) ? variable_struct_get(obj_FactionManager.mass_production_contracts, _corp.faction) : undefined;
            if (!is_undefined(_mp_f) && _mp_f.replaced) _tension += 35;
        }

        if (_gm.funds >= 500000) _tension += 15;

        // Tension threshold check (35+ tension induces retaliation)
        if (_tension >= 35 && (_gm.current_turn % 3 == ci % 3)) {
            var _roll = random(100);

            // Operation 1: Pilot Poaching Offer (35% chance if no pending offer and pilots exist)
            if (_roll < 35 && is_undefined(_gm.pending_poaching_offer) && array_length(_gm.facilities.roster_pilots) > 0) {
                var _p_idx = 0;
                var _best_fatigue = -1;
                for (var p = 0; p < array_length(_gm.facilities.roster_pilots); p++) {
                    var _plt = _gm.facilities.roster_pilots[p];
                    var _fat = variable_struct_exists(_plt, "fatigue") ? _plt.fatigue : 0;
                    if (_plt.status == "HOSPITALIZED") _fat += 3;
                    if (_fat > _best_fatigue) {
                        _best_fatigue = _fat;
                        _p_idx = p;
                    }
                }
                var _target_pilot = _gm.facilities.roster_pilots[_p_idx];
                _gm.pending_poaching_offer = {
                    pilot_id: variable_struct_exists(_target_pilot, "id") ? _target_pilot.id : ("pilot_" + string(_p_idx)),
                    pilot_name: variable_struct_exists(_target_pilot, "name") ? _target_pilot.name : "Vanguard Ace",
                    callsign: variable_struct_exists(_target_pilot, "callsign") ? _target_pilot.callsign : "Ace",
                    pilot_index: _p_idx,
                    corp_id: _corp.id,
                    corp_name: _corp.name,
                    bonus_offered: 50000 + (irandom_range(1, 5) * 10000),
                    counter_cost: 15000 + (irandom_range(0, 3) * 5000)
                };
                array_push(_gm.last_turn_events, "! ESPIONAGE ALERT: " + _corp.name + " corporate headhunters approached " + _target_pilot.name + " (" + _target_pilot.callsign + ") with defection contract!");
                if (instance_exists(obj_HQTerminal)) {
                    obj_HQTerminal.show_toast("ESPIONAGE BREACH: " + _corp.name + " attempting to poach " + _target_pilot.callsign + "!", c_red);
                }
                return true;
            }

            // Operation 2: Corporate Black-Ops Shadow Raid on Mining Node (40% chance if nodes active and no raid pending)
            else if (_roll < 75 && is_undefined(_gm.pending_raid) && array_length(_gm.nodes) > 0) {
                var _active_nodes = [];
                for (var n = 0; n < array_length(_gm.nodes); n++) {
                    if (_gm.nodes[n].status == "ACTIVE_MINING") array_push(_active_nodes, n);
                }
                if (array_length(_active_nodes) > 0) {
                    var _target_node_idx = _active_nodes[irandom(array_length(_active_nodes) - 1)];
                    var _node = _gm.nodes[_target_node_idx];
                    var _nemesis_candidate = _corp.candidate_ids[irandom(array_length(_corp.candidate_ids) - 1)];

                    _gm.pending_raid = {
                        node_index: _target_node_idx,
                        node_name: _node.name,
                        assigned_mech: _node.assigned_mech_id,
                        assigned_pilot: _node.assigned_pilot_name,
                        raid_type: "CORPORATE_SHADOW_RAID",
                        sponsor_corp: _corp.id,
                        sponsor_name: _corp.name,
                        nemesis_pilot_id: _nemesis_candidate
                    };
                    array_push(_gm.last_turn_events, "! BLACK-OPS RAID: " + _corp.name + " deniable strike craft attacking " + _node.name + "!");
                    if (instance_exists(obj_HQTerminal)) {
                        obj_HQTerminal.show_toast("BLACK-OPS ALERT: " + _node.name + " assaulted by " + _corp.name + "!", c_red);
                    }
                    return true;
                }
            }

            // Operation 3: Nemesis Ace Hit Contract (if fewer than 3 active nemeses)
            else if (array_length(active_nemeses) < 3) {
                var _pick_id = _corp.candidate_ids[0];
                for (var ci2 = 0; ci2 < array_length(_corp.candidate_ids); ci2++) {
                    if (!is_nemesis_active(_corp.candidate_ids[ci2])) {
                        _pick_id = _corp.candidate_ids[ci2];
                        break;
                    }
                }
                var _char = get_character(_pick_id);
                var _ace_name = (!is_undefined(_char)) ? _char.name : "Elite Megacorp Ace";
                var _ace_callsign = (!is_undefined(_char)) ? _char.callsign : "Predator";

                assign_corporate_contract(_pick_id, _corp.id, "Eliminate Iron Ridge PMC vanguard and seize prototype telemetry.");

                var _exists_already = false;
                for (var nem_i = 0; nem_i < array_length(active_nemeses); nem_i++) {
                    if (active_nemeses[nem_i].pilot_id == _pick_id) { _exists_already = true; break; }
                }
                if (!_exists_already) {
                    array_push(active_nemeses, {
                        pilot_id: _pick_id,
                        name: _ace_name,
                        callsign: _ace_callsign,
                        target_id: "ALLIED_0",
                        sponsor_corp: _corp.id,
                        sponsor_name: _corp.name,
                        cause: "CORPORATE_BOUNTY",
                        declared_turn: _gm.current_turn,
                        bounty_cr: 150000,
                        mech_chassis: (_corp.faction == "faction_terran") ? "TCX-11 Behemoth Mk.IV" : ((_corp.faction == "faction_colony") ? "JCC-N03 Nebula" : "HATS-03 Raiden Storm")
                    });
                    array_push(_gm.last_turn_events, "! CORPORATE BOUNTY: " + _corp.name + " commissioned Nemesis Ace " + _ace_name + " [" + _ace_callsign + "] to hunt your forces!");
                    if (instance_exists(obj_HQTerminal)) {
                        obj_HQTerminal.show_toast("NEMESIS CONTRACT: " + _ace_name + " commissioned by " + _corp.name + "!", c_red);
                    }
                }
                return true;
            }
        }
    }
    return false;
};

show_debug_message("[obj_NemesisManager] Manager online with " + string(array_length(character_id_list)) + " characters indexed.");

// Populate pilot hiring market in obj_GameManager if already instantiated
if (instance_exists(obj_GameManager)) {
    var _gm = instance_find(obj_GameManager, 0);
    if (_gm != noone && variable_instance_exists(_gm, "populate_market_from_nemesis")) {
        _gm.populate_market_from_nemesis();
    }
}

var _log_f2 = file_text_open_append("boot_log.txt");
file_text_write_string(_log_f2, "[BOOT] obj_NemesisManager Create event finished!\n");
file_text_close(_log_f2);
