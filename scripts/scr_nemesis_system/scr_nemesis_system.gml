/// @description scr_nemesis_system
// Pilot Nemesis Engine, Relational Event Dispatcher, Romance Trauma & Procedural Allegiance Engine
// Strictly implements Document 19: Pilot Nemesis System & Dynamic Character Relationship Web

/// @function scr_campaign_seed_allegiance_roll(_seed)
/// @description Executes deterministic procedural campaign faction assignments and updates defection narratives.
/// @param {Real} _seed Random seed integer for this campaign run
function scr_campaign_seed_allegiance_roll(_seed) {
    if (!instance_exists(obj_NemesisManager)) {
        show_debug_message("[scr_campaign_seed_allegiance_roll] ERROR: obj_NemesisManager does not exist!");
        return false;
    }

    random_set_seed(_seed);
    obj_NemesisManager.campaign_seed = _seed;

    var _mgr = obj_NemesisManager;
    var _keys = _mgr.character_id_list;
    var _total = array_length(_keys);

    // Track faction counts to enforce QA quota balance (minimum 20 recruitable pilots per major faction)
    var _counts = {
        faction_terran: 0,
        faction_colony: 0,
        faction_syndicate: 0,
        faction_zaibatsu: 0,
        independent: 0
    };

    // First pass: Roll candidate factions based on allegiance weights
    for (var i = 0; i < _total; i++) {
        var _cid = _keys[i];
        var _c = _mgr.characters_map[$ _cid];
        if (!is_struct(_c)) continue;

        var _var_data = _c[$ "allegiance_variance"];
        if (!is_struct(_var_data)) {
            _c.current_faction_id = _c.faction_id;
            continue;
        }

        // Diehard purists never defect
        if (_var_data.ideological_loyalty == "diehard_purist") {
            _c.current_faction_id = _var_data.canonical_faction;
            if (_c.is_recruitable && variable_struct_exists(_counts, _c.current_faction_id)) {
                _counts[$ _c.current_faction_id]++;
            }
            continue;
        }

        // Roll against probability weights
        var _roll = random(1.0);
        var _weights = _var_data.playthrough_weights;
        var _cumulative = 0.0;
        var _assigned = _var_data.canonical_faction;

        var _fac_names = ["faction_terran", "faction_colony", "faction_syndicate", "faction_zaibatsu", "independent"];
        for (var f = 0; f < array_length(_fac_names); f++) {
            var _fn = _fac_names[f];
            if (variable_struct_exists(_weights, _fn)) {
                _cumulative += _weights[$ _fn];
                if (_roll <= _cumulative) {
                    _assigned = _fn;
                    break;
                }
            }
        }

        _c.current_faction_id = _assigned;
        if (_c.is_recruitable && variable_struct_exists(_counts, _assigned)) {
            _counts[$ _assigned]++;
        }
    }

    // QA Quota Balance Clamp: Ensure major factions have >= 20 recruitable pilots
    var _major_factions = ["faction_terran", "faction_colony", "faction_syndicate", "faction_zaibatsu"];
    for (var m = 0; m < array_length(_major_factions); m++) {
        var _mf = _major_factions[m];
        while (_counts[$ _mf] < 20) {
            // Find a flexible pilot whose canonical faction is this one, and revert them
            var _reverted = false;
            for (var r = 0; r < _total; r++) {
                var _rc = _mgr.characters_map[$ _keys[r]];
                if (_rc.is_recruitable && _rc.allegiance_variance.canonical_faction == _mf && _rc.current_faction_id != _mf) {
                    _counts[$ _rc.current_faction_id]--;
                    _rc.current_faction_id = _mf;
                    _counts[$ _mf]++;
                    _reverted = true;
                    break;
                }
            }
            if (!_reverted) break; // Maximum possible quota restored
        }
    }

    // Finalize defection narrative hooks and rebuild faction rosters
    _mgr.faction_rosters = {
        faction_terran: [],
        faction_colony: [],
        faction_syndicate: [],
        faction_zaibatsu: [],
        independent: []
    };

    for (var k = 0; k < _total; k++) {
        var _fin_c = _mgr.characters_map[$ _keys[k]];
        var _curr_fac = _fin_c.current_faction_id;

        // Set active defection hook
        if (_curr_fac != _fin_c.allegiance_variance.canonical_faction) {
            var _hooks = _fin_c.allegiance_variance.defection_hooks;
            _fin_c.active_defection_hook = (variable_struct_exists(_hooks, _curr_fac)) ? _hooks[$ _curr_fac] : "Serving under alternate faction contract.";
        } else {
            _fin_c.active_defection_hook = "";
        }

        // Add to active faction roster
        if (variable_struct_exists(_mgr.faction_rosters, _curr_fac)) {
            array_push(_mgr.faction_rosters[$ _curr_fac], _fin_c.id);
        }
    }

    show_debug_message("[scr_campaign_seed_allegiance_roll] SUCCESS: Seed " + string(_seed) + " applied. Roster counts: Terran=" + string(_counts.faction_terran) + ", Colony=" + string(_counts.faction_colony) + ", Syndicate=" + string(_counts.faction_syndicate) + ", Zaibatsu=" + string(_counts.faction_zaibatsu) + ", Indep=" + string(_counts.independent));
    return true;
}

/// @function scr_nemesis_event_dispatch(_victim_id, _killer_id, _event_type)
/// @description Dispatches relationship reactions across the graph when a figure is killed, executed, or captured.
/// @param {String} _victim_id ID of victim character
/// @param {String} _killer_id ID of acting entity (e.g., "player" or pilot ID)
/// @param {String} _event_type Event: "combat_kill", "executed", "core_meltdown", "captured", "ransomed"
function scr_nemesis_event_dispatch(_victim_id, _killer_id, _event_type) {
    if (!instance_exists(obj_NemesisManager)) return undefined;

    var _mgr = obj_NemesisManager;
    if (!variable_struct_exists(_mgr.characters_map, _victim_id)) {
        show_debug_message("[scr_nemesis_event_dispatch] Unknown victim: " + string(_victim_id));
        return undefined;
    }

    var _victim = _mgr.characters_map[$ _victim_id];
    var _summary = {
        victim_name: _victim.name,
        event_type: _event_type,
        nemeses_triggered: [],
        heartbreak_triggered: false,
        trauma_mode: ""
    };

    // 1. Update physical survival status
    if (_event_type == "combat_kill" || _event_type == "executed" || _event_type == "core_meltdown") {
        _victim.is_alive = false;
        _victim.is_imprisoned = false;
    } else if (_event_type == "captured") {
        _victim.is_imprisoned = true;
    }

    var _base_sev = 30;
    if (_event_type == "core_meltdown") _base_sev = 45;
    else if (_event_type == "executed") _base_sev = 75;
    else if (_event_type == "captured") _base_sev = 15;

    // 2. Evaluate Romantic Bond (Highest Emotional Priority: K_romance = 3.0x)
    if (_event_type != "captured" && _event_type != "ransomed") {
        var _rom_result = scr_check_romance_trauma(_victim_id, _killer_id);
        if (_rom_result.triggered) {
            _summary.heartbreak_triggered = true;
            _summary.trauma_mode = _rom_result.trauma_mode;
            array_push(_summary.nemeses_triggered, _rom_result.lover_id);
        }
    }

    // 3. Evaluate Direct Kinship Edges (K_kinship = 2.5x for immediate, 1.3x for extended)
    var _kin = _victim[$ "kinship"];
    if (is_array(_kin)) {
        for (var k = 0; k < array_length(_kin); k++) {
            var _edge = _kin[k];
            var _rel_id = _edge.target_id;

            if (variable_struct_exists(_mgr.characters_map, _rel_id)) {
                var _rel = _mgr.characters_map[$ _rel_id];
                if (!_rel.is_alive) continue;

                var _rel_type = _edge.relation;
                var _k_mult = 1.3;
                if (_rel_type == "brother" || _rel_type == "sister" || _rel_type == "daughter" || _rel_type == "son" || _rel_type == "mother" || _rel_type == "father") {
                    _k_mult = 2.5;
                }

                var _grudge_delta = min(100, floor(_base_sev * _k_mult));
                _rel.morale = max(0, _rel.morale - 30);
                _rel.grudge = min(100, (_rel[$ "grudge"] ?? 0) + _grudge_delta);

                // Vendetta Threshold Check (Grudge >= 70)
                if (_rel.grudge >= 70 && !_mgr.is_nemesis_active(_rel_id)) {
                    array_push(_mgr.active_nemeses, {
                        pilot_id: _rel.id,
                        target_id: _killer_id,
                        cause: "avenge_kin_" + _victim_id,
                        declared_turn: (instance_exists(obj_GameManager) ? obj_GameManager.current_turn : 1)
                    });
                    array_push(_summary.nemeses_triggered, _rel.id);
                    show_debug_message("[VENDETTA DECLARED] " + _rel.name + " swore blood vendetta against " + string(_killer_id) + " for " + _victim.name);
                }
            }
        }
    }

    // 4. Evaluate Wingman & Mentor Connections (K = 1.8x)
    var _allies = [_victim[$ "wingman_id"], _victim[$ "mentor_id"]];
    for (var a = 0; a < array_length(_allies); a++) {
        var _ally_id = _allies[a];
        if (!is_string(_ally_id) || !variable_struct_exists(_mgr.characters_map, _ally_id)) continue;

        var _ally = _mgr.characters_map[$ _ally_id];
        if (!_ally.is_alive) continue;

        var _ally_grudge = min(100, floor(_base_sev * 1.8));
        _ally.morale = max(0, _ally.morale - 20);
        _ally.grudge = min(100, (_ally[$ "grudge"] ?? 0) + _ally_grudge);

        if (_ally.grudge >= 70 && !_mgr.is_nemesis_active(_ally_id)) {
            array_push(_mgr.active_nemeses, {
                pilot_id: _ally.id,
                target_id: _killer_id,
                cause: "avenge_wingman_" + _victim_id,
                declared_turn: (instance_exists(obj_GameManager) ? obj_GameManager.current_turn : 1)
            });
            array_push(_summary.nemeses_triggered, _ally.id);
        }
    }

    // 5. Evaluate Close Friendship Circle (-25 Morale, +30 Grudge)
    var _fr = _victim[$ "friendships"];
    if (is_struct(_fr) && is_array(_fr[$ "friend_ids"])) {
        var _f_ids = _fr.friend_ids;
        for (var f = 0; f < array_length(_f_ids); f++) {
            var _fid = _f_ids[f];
            if (variable_struct_exists(_mgr.characters_map, _fid)) {
                var _friend = _mgr.characters_map[$ _fid];
                if (_friend.is_alive) {
                    _friend.morale = max(0, _friend.morale - 25);
                    _friend.grudge = min(100, (_friend[$ "grudge"] ?? 0) + 30);
                }
            }
        }
    }

    return _summary;
}

/// @function scr_check_romance_trauma(_casualty_id, _killer_id)
/// @description Checks heartbreak trauma, applies extreme grudge multipliers, and activates trauma combat state.
/// @param {String} _casualty_id ID of killed/executed character
/// @param {String} _killer_id ID of killer entity
function scr_check_romance_trauma(_casualty_id, _killer_id) {
    var _res = { triggered: false, lover_id: "", trauma_mode: "" };
    if (!instance_exists(obj_NemesisManager)) return _res;

    var _mgr = obj_NemesisManager;
    var _casualty = _mgr.characters_map[$ _casualty_id];
    if (!is_struct(_casualty)) return _res;

    var _rom = _casualty[$ "love_interest"];
    if (!is_struct(_rom) || !variable_struct_exists(_rom, "target_id")) return _res;

    var _lover_id = _rom.target_id;
    if (!variable_struct_exists(_mgr.characters_map, _lover_id)) return _res;

    var _lover = _mgr.characters_map[$ _lover_id];
    if (!_lover.is_alive) return _res;

    // Apply Heartbreak Trauma
    _res.triggered = true;
    _res.lover_id = _lover_id;
    _res.trauma_mode = _rom[$ "trauma_reaction"] ?? "berserker_rage";

    var _g_mult = _rom[$ "grudge_multiplier"] ?? 3.0;
    var _rom_grudge_delta = min(100, floor(75 * (_g_mult / 3.0)));

    _lover.morale = 0;
    _lover.grudge = 100; // Immediate maximum grudge
    _lover.combat_trauma_mode = _res.trauma_mode;

    // Enforce Nemesis Enrollment
    if (!_mgr.is_nemesis_active(_lover_id)) {
        array_push(_mgr.active_nemeses, {
            pilot_id: _lover_id,
            target_id: _killer_id,
            cause: "heartbreak_revenge_" + _casualty_id,
            declared_turn: (instance_exists(obj_GameManager) ? obj_GameManager.current_turn : 1)
        });
    }

    show_debug_message("[HEARTBREAK VENDETTA] " + _lover.name + " suffered fatal emotional trauma for " + _casualty.name + "! Mode: " + _res.trauma_mode);
    return _res;
}

/// @function scr_get_friendship_referral_discount(_pilot_id)
/// @description Returns 0.25 (25% discount) if any close friend of this pilot is already hired in player's PMC.
/// @param {String} _pilot_id ID of candidate pilot
function scr_get_friendship_referral_discount(_pilot_id) {
    if (!instance_exists(obj_NemesisManager) || !instance_exists(obj_GameManager)) return 0.0;

    var _mgr = obj_NemesisManager;
    var _gm = obj_GameManager;

    if (!variable_struct_exists(_mgr.characters_map, _pilot_id)) return 0.0;
    var _pilot = _mgr.characters_map[$ _pilot_id];
    var _fr = _pilot[$ "friendships"];
    if (!is_struct(_fr) || !is_array(_fr[$ "friend_ids"])) return 0.0;

    var _f_ids = _fr.friend_ids;
    var _player_pilots = _gm.player_pilots; // Array of hired pilot structs or IDs

    for (var i = 0; i < array_length(_player_pilots); i++) {
        var _hired = _player_pilots[i];
        var _hired_id = (is_struct(_hired) ? _hired.id : string(_hired));
        for (var f = 0; f < array_length(_f_ids); f++) {
            if (_hired_id == _f_ids[f]) {
                show_debug_message("[FRIENDSHIP REFERRAL] Pilot " + _pilot.name + " qualifies for -25% referral discount via friend " + _hired_id);
                return 0.25;
            }
        }
    }

    return 0.0;
}

/// @function scr_prisoner_triage(_prisoner_id, _action)
/// @description Handles captured prisoner decisions: execute, ransom, recruit, or diplomatic hold.
/// @param {String} _prisoner_id ID of captive
/// @param {String} _action Action: "execute", "ransom", "recruit", "diplomatic_hold"
function scr_prisoner_triage(_prisoner_id, _action) {
    if (!instance_exists(obj_NemesisManager) || !instance_exists(obj_GameManager)) return false;

    var _mgr = obj_NemesisManager;
    var _gm = obj_GameManager;

    if (!variable_struct_exists(_mgr.characters_map, _prisoner_id)) return false;
    var _p = _mgr.characters_map[$ _prisoner_id];

    // Remove from brig prisoner list
    var _found_idx = -1;
    for (var i = 0; i < array_length(_mgr.prisoner_list); i++) {
        if (_mgr.prisoner_list[i].id == _prisoner_id) {
            _found_idx = i;
            break;
        }
    }

    if (_action == "execute") {
        if (_found_idx != -1) array_delete(_mgr.prisoner_list, _found_idx, 1);
        _p.is_alive = false;
        _p.is_imprisoned = false;

        // Dispatch execution reaction
        scr_nemesis_event_dispatch(_prisoner_id, "player", "executed");

        // Faction Standing Penalty
        if (instance_exists(obj_FactionManager)) {
            obj_FactionManager.modify_standing(_p.current_faction_id, -20);
        }
        show_debug_message("[PRISONER EXECUTION] " + _p.name + " was executed in base brig. Severe diplomatic fallout.");
        return true;
    }
    else if (_action == "ransom") {
        if (_found_idx != -1) array_delete(_mgr.prisoner_list, _found_idx, 1);
        _p.is_imprisoned = false;

        var _payout = 50000;
        if (_p.tier == 2) _payout = 120000;
        else if (_p.tier == 3) _payout = 250000;
        else if (_p.tier >= 4) _payout = 500000;

        _gm.funds += _payout;
        if (instance_exists(obj_FactionManager)) {
            obj_FactionManager.modify_standing(_p.current_faction_id, 10);
        }
        show_debug_message("[PRISONER RANSOM] Ransomed " + _p.name + " to " + _p.current_faction_id + " for +" + string(_payout) + " Cr.");
        return true;
    }
    else if (_action == "recruit") {
        if (_found_idx != -1) array_delete(_mgr.prisoner_list, _found_idx, 1);
        _p.is_imprisoned = false;
        _p.current_faction_id = "independent";
        _p.morale = 60;

        array_push(_gm.player_pilots, _p);
        show_debug_message("[PRISONER RECRUIT] Turned " + _p.name + " into player PMC roster.");
        return true;
    }
    else if (_action == "diplomatic_hold") {
        _p.is_imprisoned = true;
        show_debug_message("[PRISONER HOLD] Retaining " + _p.name + " as diplomatic shield.");
        return true;
    }

    return false;
}

// =============================================================================
// PHASE 5: PROCEDURAL 5-LAYER DYNAMIC PORTRAIT COMPOSITOR (Document 19)
// =============================================================================
/// @function scr_draw_composite_portrait(_char_ref, _x, _y, _size, _show_frame, _expr_override)
/// @description Renders a 5-layer procedural composite character bust adhering to Front Mission SNES 1995 standards.
/// @param {String|Struct} _char_ref Character ID string or character struct
/// @param {Real} _x Top-left screen X
/// @param {Real} _y Top-left screen Y
/// @param {Real} _size Desired square dimension (e.g., 64, 96, 128, 160, 200)
/// @param {Bool} _show_frame Draw 2-pixel metallic beveled retro frame
/// @param {String} _expr_override Optional expression: "neutral", "enraged", "stoic", "defeated"
function scr_draw_composite_portrait(_char_ref, _x, _y, _size, _show_frame, _expr_override) {
    var _c = undefined;
    if (is_struct(_char_ref)) {
        _c = _char_ref;
    } else if (is_string(_char_ref) && instance_exists(obj_NemesisManager)) {
        _c = obj_NemesisManager.get_character(_char_ref);
    }

    if (is_undefined(_c)) {
        _c = {
            id: "pilot_unknown",
            name: "Veteran Mercenary",
            callsign: "DRIFTER",
            faction_id: "independent",
            current_faction_id: "independent",
            tier: 2,
            morale: 80,
            grudge: 0,
            combat_trauma_mode: "",
            snes_portrait_spec: { palette: "indep_mercenary_grey", scars: "veteran_slash", eyes: "amber", expression: "stoic" }
        };
    }

    var _fac = _c[$ "current_faction_id"] ?? (_c[$ "faction_id"] ?? "independent");
    var _canon_fac = _c[$ "faction_id"] ?? "independent";
    var _spec = _c[$ "snes_portrait_spec"] ?? {};
    var _is_nem = false;
    if (instance_exists(obj_NemesisManager)) {
        _is_nem = obj_NemesisManager.is_nemesis_active(_c.id);
    }

    // -------------------------------------------------------------------------
    // LAYER 0: Background & Beveled Frame
    // -------------------------------------------------------------------------
    if (_show_frame) {
        // Dark recessed canvas
        draw_set_color(make_color_rgb(14, 18, 24));
        draw_rectangle(_x, _y, _x + _size, _y + _size, false);

        // Scanlines
        draw_set_color(make_color_rgb(8, 10, 14));
        draw_set_alpha(0.35);
        for (var sl = _y + 2; sl < _y + _size - 2; sl += 4) {
            draw_line(_x + 2, sl, _x + _size - 2, sl);
        }
        draw_set_alpha(1.0);

        // 2-pixel beveled metallic frame
        // Outer highlight (Top / Left)
        draw_set_color(make_color_rgb(110, 120, 135));
        draw_line(_x, _y, _x + _size, _y);
        draw_line(_x, _y, _x, _y + _size);

        // Outer shadow (Bottom / Right)
        draw_set_color(make_color_rgb(32, 36, 44));
        draw_line(_x, _y + _size, _x + _size, _y + _size);
        draw_line(_x + _size, _y, _x + _size, _y + _size);

        // Inner border rim
        draw_set_color(make_color_rgb(50, 56, 68));
        draw_rectangle(_x + 1, _y + 1, _x + _size - 1, _y + _size - 1, true);
    }

    // -------------------------------------------------------------------------
    // LAYER 1: Base Character Canvas
    // -------------------------------------------------------------------------
    var _base_spr = spr_portrait_cole;
    if (_fac == "faction_terran") {
        _base_spr = (string_pos("vance", _c.id) > 0) ? spr_portrait_vance : spr_portrait_cole;
    } else if (_fac == "faction_colony") {
        _base_spr = (string_pos("cassian", _c.id) > 0 || string_pos("vane", _c.id) > 0) ? spr_portrait_cassian : spr_portrait_sorren;
    } else if (_fac == "faction_syndicate") {
        _base_spr = (string_pos("nadia", _c.id) > 0 || string_pos("ortiz", _c.id) > 0) ? spr_portrait_nadia : spr_portrait_cruz;
    } else if (_fac == "faction_zaibatsu") {
        _base_spr = (string_pos("renzo", _c.id) > 0 || string_pos("takahashi", _c.id) > 0) ? spr_portrait_renzo : spr_portrait_null07;
    }

    // Faction palette tint (procedural defection reskinning)
    var _blend_col = c_white;
    if (_fac != _canon_fac) {
        if (_fac == "faction_terran") _blend_col = make_color_rgb(200, 220, 190);
        else if (_fac == "faction_colony") _blend_col = make_color_rgb(180, 210, 255);
        else if (_fac == "faction_syndicate") _blend_col = make_color_rgb(255, 190, 160);
        else if (_fac == "faction_zaibatsu") _blend_col = make_color_rgb(170, 240, 245);
        else if (_fac == "independent") _blend_col = make_color_rgb(220, 220, 225);
    }

    var _pad = _show_frame ? 2 : 0;
    var _draw_w = _size - (_pad * 2);
    var _draw_h = _size - (_pad * 2);

    if (sprite_exists(_base_spr)) {
        draw_sprite_stretched_ext(_base_spr, 0, _x + _pad, _y + _pad, _draw_w, _draw_h, _blend_col, 1.0);
    }

    // -------------------------------------------------------------------------
    // LAYER 2: Expression State (Grim / Enraged / Stoic / Defeated)
    // -------------------------------------------------------------------------
    var _expr = _expr_override;
    if (_expr == "") {
        if (_c[$ "combat_trauma_mode"] == "berserker_rage" || (_c[$ "grudge"] ?? 0) >= 70 || _is_nem) _expr = "enraged";
        else if (_c[$ "morale"] < 30) _expr = "defeated";
        else _expr = "stoic";
    }

    var _cx = _x + _size * 0.5;
    var _cy = _y + _size * 0.45;

    if (_expr == "enraged") {
        // Severe brow furrow
        draw_set_color(make_color_rgb(30, 25, 25));
        draw_line_width(_cx - _size * 0.18, _cy - _size * 0.12, _cx - _size * 0.04, _cy - _size * 0.08, max(1.0, _size / 64.0));
        draw_line_width(_cx + _size * 0.04, _cy - _size * 0.08, _cx + _size * 0.18, _cy - _size * 0.12, max(1.0, _size / 64.0));

        // Crimson combat adrenaline eye glint
        draw_set_color(make_color_rgb(255, 50, 40));
        draw_set_alpha(0.65);
        draw_circle(_cx - _size * 0.10, _cy - _size * 0.05, max(1.5, _size / 40.0), false);
        draw_circle(_cx + _size * 0.10, _cy - _size * 0.05, max(1.5, _size / 40.0), false);
        draw_set_alpha(1.0);
    } else if (_expr == "defeated") {
        // Forehead field dressing / bandage
        draw_set_color(make_color_rgb(220, 215, 195));
        draw_rectangle(_cx - _size * 0.22, _cy - _size * 0.22, _cx + _size * 0.15, _cy - _size * 0.15, false);
        draw_set_color(make_color_rgb(160, 150, 130));
        draw_line(_cx - _size * 0.22, _cy - _size * 0.18, _cx + _size * 0.15, _cy - _size * 0.18);
    }

    // -------------------------------------------------------------------------
    // LAYER 3: Battle Trauma & Shrapnel Scars
    // -------------------------------------------------------------------------
    var _scars = string(_spec[$ "scars"] ?? "");
    if (_scars != "none" && _scars != "") {
        if (string_pos("shrapnel", _scars) > 0 || string_pos("cut", _scars) > 0 || string_pos("slash", _scars) > 0 || string_pos("gash", _scars) > 0 || string_pos("scar", _scars) > 0) {
            // Jagged cheek laceration
            draw_set_color(make_color_rgb(140, 24, 24));
            var _sx1 = _cx + _size * 0.04;
            var _sy1 = _cy - _size * 0.02;
            var _sx2 = _cx + _size * 0.24;
            var _sy2 = _cy + _size * 0.18;
            draw_line_width(_sx1, _sy1, _sx2, _sy2, max(1.5, _size / 50.0));

            // Cross-stitch tick marks
            draw_set_color(make_color_rgb(215, 160, 160));
            draw_line(_sx1 + 4, _sy1 - 2, _sx1 + 2, _sy1 + 4);
            draw_line(_sx2 - 4, _sy2 - 2, _sx2 - 2, _sy2 + 4);
        }

        if (string_pos("burn", _scars) > 0 || string_pos("slag", _scars) > 0) {
            // Charred thermal plasma burn patch on collar/jaw
            draw_set_color(make_color_rgb(45, 20, 32));
            draw_set_alpha(0.70);
            draw_ellipse(_cx + _size * 0.08, _cy + _size * 0.16, _cx + _size * 0.28, _cy + _size * 0.30, false);
            draw_set_color(make_color_rgb(110, 40, 60));
            draw_ellipse(_cx + _size * 0.12, _cy + _size * 0.19, _cx + _size * 0.24, _cy + _size * 0.26, true);
            draw_set_alpha(1.0);
        }
    }

    // -------------------------------------------------------------------------
    // LAYER 4: Cybernetic Prosthetics & Tachyon Optic Implants
    // -------------------------------------------------------------------------
    var _eyes = string(_spec[$ "eyes"] ?? "");
    var _head = string(_spec[$ "headgear"] ?? "");
    var _has_bionic = (string_pos("optic", _eyes) > 0 || string_pos("cyber", _eyes) > 0 || string_pos("synthetic", _eyes) > 0 || _fac == "faction_zaibatsu" || string_pos("null07", _c.id) > 0);

    if (_has_bionic) {
        // Tachyon Glowing Cybernetic Optic Lens (Right Eye)
        var _ox = _cx + _size * 0.11;
        var _oy = _cy - _size * 0.05;
        var _orad = max(3.0, _size * 0.055);

        // Titanium socket housing
        draw_set_color(make_color_rgb(32, 38, 48));
        draw_circle(_ox, _oy, _orad + 1, false);
        draw_set_color(make_color_rgb(80, 95, 115));
        draw_circle(_ox, _oy, _orad + 1, true);

        // Glowing Tachyon Cyan Aperture
        var _pulse = 0.8 + 0.2 * sin(current_time * 0.008);
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_circle(_ox, _oy, _orad * _pulse, false);

        // Core white pupil diode
        draw_set_color(c_white);
        draw_circle(_ox, _oy, max(1.0, _orad * 0.35), false);

        // Neural interface lead wire back to temple
        draw_set_color(make_color_rgb(0, 180, 210));
        draw_line_width(_ox + _orad, _oy, _cx + _size * 0.28, _oy - 2, max(1.0, _size / 80.0));
    } else if (string_pos("eyepatch", _head) > 0 || (string_pos("jackal", _c.id) > 0 && _fac == "faction_syndicate")) {
        // Syndicate Reaver Angled Eye-patch
        var _ex = _cx + _size * 0.11;
        var _ey = _cy - _size * 0.05;
        draw_set_color(make_color_rgb(18, 18, 22));
        draw_rectangle(_ex - _size * 0.05, _ey - _size * 0.04, _ex + _size * 0.05, _ey + _size * 0.04, false);
        draw_set_color(make_color_rgb(50, 42, 36));
        draw_line_width(_cx - _size * 0.05, _ey - _size * 0.09, _cx + _size * 0.28, _ey + _size * 0.02, max(1.0, _size / 70.0));
    }

    // Cranial neuro-bracket rim
    if (string_pos("bracket", _head) > 0 || string_pos("neural", _head) > 0 || _fac == "faction_zaibatsu") {
        draw_set_color(make_color_rgb(120, 135, 155));
        draw_line_width(_cx - _size * 0.20, _cy - _size * 0.26, _cx + _size * 0.20, _cy - _size * 0.26, max(1.5, _size / 60.0));
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_circle(_cx - _size * 0.18, _cy - _size * 0.26, 1.5, false);
        draw_circle(_cx + _size * 0.18, _cy - _size * 0.26, 1.5, false);
    }

    // -------------------------------------------------------------------------
    // LAYER 5: Faction Insignia, Rank Pips & Nemesis Kill Badges
    // -------------------------------------------------------------------------
    // Top-Right: Faction Emblem Pip
    var _bx = _x + _size - 18;
    var _by = _y + 6;
    if (_is_nem) {
        // Glowing Crimson Vendetta Skull Badge
        var _f_pulse = (current_time mod 300 < 150);
        draw_set_color(_f_pulse ? make_color_rgb(220, 30, 30) : make_color_rgb(150, 15, 15));
        draw_rectangle(_bx - 2, _by - 2, _bx + 10, _by + 10, false);
        draw_set_color(c_white);
        draw_text_transformed(_bx - 1, _by - 2, "X", 0.65, 0.65, 0);
    } else {
        // Faction Emblem
        var _badge_col = make_color_rgb(180, 190, 205);
        if (_fac == "faction_terran") _badge_col = make_color_rgb(220, 180, 60); // Brass Eagle
        else if (_fac == "faction_colony") _badge_col = make_color_rgb(140, 190, 245); // Azure Star
        else if (_fac == "faction_syndicate") _badge_col = make_color_rgb(240, 140, 50); // Hazard Amber
        else if (_fac == "faction_zaibatsu") _badge_col = make_color_rgb(0, 240, 230); // Neon Cyan
        draw_set_color(_badge_col);
        draw_circle(_bx + 4, _by + 4, 5, false);
        draw_set_color(c_white);
        draw_circle(_bx + 4, _by + 4, 2, false);
    }

    // Bottom-Left: Pilot Tier Stars (1 to 4 Pips)
    var _t_rank = clamp(_c[$ "tier"] ?? 1, 1, 4);
    for (var tp = 0; tp < _t_rank; tp++) {
        draw_set_color(make_color_rgb(245, 215, 90));
        draw_rectangle(_x + 6 + (tp * 6), _y + _size - 10, _x + 9 + (tp * 6), _y + _size - 7, false);
    }

    return true;
}
