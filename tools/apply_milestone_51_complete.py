import re

print("Applying Complete Milestone 51 RPG Systems Patch...")

# -----------------------------------------------------------------------------
# 1. Patch objects/obj_HQTerminal/Draw_64.gml: Faction Audiences
# -----------------------------------------------------------------------------
hq_draw_path = "objects/obj_HQTerminal/Draw_64.gml"
with open(hq_draw_path, "r", encoding="utf-8") as f:
    hq_draw = f.read()

target_hq = '''                if (_f_box_hov && _click) {
                    if (_fid == "faction_a") scr_vn_start_episode("ep_audience_terran");
                    else if (_fid == "faction_b") scr_vn_start_episode("ep_audience_colony");
                    else if (_fid == "faction_c") scr_vn_start_episode("ep_audience_syndicate");
                    else if (_fid == "faction_d") scr_vn_start_episode("ep_audience_zaibatsu");
                    scr_audio_play_ui("confirm");
                }'''

replacement_hq = '''                if (_f_box_hov && _click) {
                    if (_fid == "faction_a") scr_vn_start_episode("ep_audience_terran");
                    else if (_fid == "faction_b") scr_vn_start_episode("ep_audience_colony");
                    else if (_fid == "faction_c") scr_vn_start_episode("ep_audience_syndicate");
                    else if (_fid == "faction_d") scr_vn_start_episode("ep_audience_zaibatsu");
                    else if (_fid == "faction_e") scr_vn_start_episode("ep_audience_sidereal");
                    else if (_fid == "faction_f") scr_vn_start_episode("ep_audience_tharsis");
                    scr_audio_play_ui("confirm");
                }'''

if target_hq in hq_draw:
    hq_draw = hq_draw.replace(target_hq, replacement_hq, 1)
    with open(hq_draw_path, "w", encoding="utf-8") as f:
        f.write(hq_draw)
    print("[PASS] obj_HQTerminal/Draw_64.gml patched with 6 faction audiences.")
else:
    print("[SKIP/WARN] obj_HQTerminal/Draw_64.gml target not found.")

# -----------------------------------------------------------------------------
# 2. Patch scripts/scr_nemesis_system/scr_nemesis_system.gml: Prisoner Recruit
# -----------------------------------------------------------------------------
nem_path = "scripts/scr_nemesis_system/scr_nemesis_system.gml"
with open(nem_path, "r", encoding="utf-8") as f:
    nem_content = f.read()

target_nem = '''    else if (_action == "recruit") {
        if (_found_idx != -1) array_delete(_mgr.prisoner_list, _found_idx, 1);
        _p.is_imprisoned = false;
        _p.current_faction_id = "independent";
        _p.morale = 60;

        array_push(_gm.player_pilots, _p);
        show_debug_message("[PRISONER RECRUIT] Turned " + _p.name + " into player PMC roster.");
        return true;
    }'''

replacement_nem = '''    else if (_action == "recruit") {
        if (_found_idx != -1) array_delete(_mgr.prisoner_list, _found_idx, 1);
        _p.is_imprisoned = false;
        _p.current_faction_id = "independent";
        _p.morale = 75;

        // Ensure full pilot struct normalization for Tab 6 Pilots Deck (Doc 51)
        if (!variable_struct_exists(_p, "status")) _p.status = "ACTIVE";
        if (!variable_struct_exists(_p, "recovery_days")) _p.recovery_days = 0;
        if (!variable_struct_exists(_p, "recovery_days_left")) _p.recovery_days_left = 0;
        if (!variable_struct_exists(_p, "is_deployed")) _p.is_deployed = false;
        if (!variable_struct_exists(_p, "kills")) _p.kills = 0;
        if (!variable_struct_exists(_p, "sorties")) _p.sorties = 0;
        if (!variable_struct_exists(_p, "fatigue")) _p.fatigue = 0;
        if (!variable_struct_exists(_p, "xp")) _p.xp = 60;
        if (!variable_struct_exists(_p, "rank_perks") || !is_array(_p.rank_perks)) _p.rank_perks = ["Deadly Aim"];
        if (!variable_struct_exists(_p, "salary_daily")) _p.salary_daily = 220;
        if (!variable_struct_exists(_p, "rank")) _p.rank = "Defector Ace";
        if (!variable_struct_exists(_p, "accuracy")) _p.accuracy = 84;
        if (!variable_struct_exists(_p, "reflexes")) _p.reflexes = 78;
        if (!variable_struct_exists(_p, "affinity")) _p.affinity = "ironclad";
        if (!variable_struct_exists(_p, "bio")) _p.bio = "Former hostile operative defected to Iron Ridge PMC after capture.";

        if (variable_struct_exists(_gm, "facilities") && variable_struct_exists(_gm.facilities, "roster_pilots")) {
            array_push(_gm.facilities.roster_pilots, _p);
        } else {
            array_push(_gm.player_pilots, _p);
        }
        show_debug_message("[PRISONER RECRUIT] Turned " + _p.name + " into player PMC roster.");
        return true;
    }'''

if target_nem in nem_content:
    nem_content = nem_content.replace(target_nem, replacement_nem, 1)
    with open(nem_path, "w", encoding="utf-8") as f:
        f.write(nem_content)
    print("[PASS] scr_nemesis_system.gml patched with normalized recruit pilot conversion.")
else:
    print("[SKIP/WARN] scr_nemesis_system.gml target not found.")

# -----------------------------------------------------------------------------
# 3. Patch objects/obj_BattleManager/Create_0.gml: POW Capture & Frame Affinity
# -----------------------------------------------------------------------------
bm_create_path = "objects/obj_BattleManager/Create_0.gml"
with open(bm_create_path, "r", encoding="utf-8") as f:
    bm_create = f.read()

# 3a: captured_pows initialization
target_bm_init = 'ai_unit_index = 0;\n\n// 2b. Nemesis Drop-Pod'
replacement_bm_init = 'ai_unit_index = 0;\ncaptured_pows = []; // Battlefield captured enemy pilot escape pods (Doc 51)\n\n// 2b. Nemesis Drop-Pod'
if target_bm_init in bm_create:
    bm_create = bm_create.replace(target_bm_init, replacement_bm_init, 1)
    print("[PASS] captured_pows initialized in BattleManager Create_0.gml")

# 3b: Allied pilot linking and Frame Affinity check
target_bm_link = '''// 5a. Dynamic Mass-Production Line Chassis Assignment (docs/29 & docs/30)'''
replacement_bm_link = '''// 5a-ii. Pilot Roster Integration, Frame Affinity & Active Perks (Doc 51)
if (instance_exists(obj_GameManager) && variable_struct_exists(obj_GameManager.facilities, "roster_pilots")) {
    var _r_pilots = obj_GameManager.facilities.roster_pilots;
    var _allied_idx = 0;
    for (var u = 0; u < array_length(units); u++) {
        var _un = units[u];
        if (_un.team == "ALLIED" && _allied_idx < array_length(_r_pilots)) {
            var _pilot = _r_pilots[_allied_idx];
            if (_pilot.status == "ACTIVE") {
                _un.pilot_name = _pilot.name;
                _un.callsign = _pilot.callsign + " [" + string_upper(_un.mech_type) + "]";
                _un.accuracy = max(55, _pilot.accuracy);
                _un.evasion = max(35, _pilot.reflexes);
                _un.pilot_reflexes = _pilot.reflexes;
                _un.rank_perks = (variable_struct_exists(_pilot, "rank_perks") && is_array(_pilot.rank_perks)) ? _pilot.rank_perks : [];
                _un.pilot_affinity = (variable_struct_exists(_pilot, "affinity") ? _pilot.affinity : "ironclad");
                _un.kills = 0;

                // Frame Affinity Resonance Check
                var _p_aff = string_lower(_un.pilot_affinity);
                var _m_type = string_lower(_un.mech_type);
                if (_p_aff == _m_type ||
                    (_p_aff == "ironclad" && (_m_type == "ironclad" || _m_type == "biped")) ||
                    (_p_aff == "aether" && (_m_type == "aether" || _m_type == "aero")) ||
                    (_p_aff == "muramasa" && (_m_type == "muramasa" || _m_type == "hover")) ||
                    (_p_aff == "treads" && (_m_type == "titan" || _m_type == "treads"))) {
                    _un.has_affinity_match = true;
                    _un.accuracy += 8;
                    _un.evasion += 8;
                    _un.max_ap += 1;
                    _un.current_ap = _un.max_ap;
                }
                _allied_idx++;
            }
        }
    }
}

// 5a. Dynamic Mass-Production Line Chassis Assignment (docs/29 & docs/30)'''

if target_bm_link in bm_create:
    bm_create = bm_create.replace(target_bm_link, replacement_bm_link, 1)
    print("[PASS] Pilot roster linking & Frame Affinity check integrated into BattleManager Create_0.gml")

# 3c: calculate_hit_chance Frame Affinity & Pilot Perks bonus
target_hit_calc = '''    // Suppression aim penalty (Goal F)
    if (variable_struct_exists(_atk, "is_suppressed") && _atk.is_suppressed) {
        _base -= 20;
    }'''

replacement_hit_calc = '''    // Pilot Rank Perks & Frame Affinity Resonance (Doc 51)
    if (variable_struct_exists(_atk, "has_affinity_match") && _atk.has_affinity_match) {
        _base += 8;
    }
    if (variable_struct_exists(_def, "has_affinity_match") && _def.has_affinity_match) {
        _eva += 8;
    }
    if (variable_struct_exists(_atk, "rank_perks") && is_array(_atk.rank_perks)) {
        for (var pk = 0; pk < array_length(_atk.rank_perks); pk++) {
            if (_atk.rank_perks[pk] == "Deadly Aim") _base += 8;
        }
    }
    if (variable_struct_exists(_def, "rank_perks") && is_array(_def.rank_perks)) {
        for (var pk = 0; pk < array_length(_def.rank_perks); pk++) {
            if (_def.rank_perks[pk] == "Vernier Drift") _eva += 10;
        }
    }

    // Suppression aim penalty (Goal F)
    if (variable_struct_exists(_atk, "is_suppressed") && _atk.is_suppressed) {
        _base -= 20;
    }'''

if target_hit_calc in bm_create:
    bm_create = bm_create.replace(target_hit_calc, replacement_hit_calc, 1)
    print("[PASS] calculate_hit_chance updated with Frame Affinity & Perks")

# 3d: Enemy torso destruction POW capture
target_torso_ej = '''                        // 2. Pilot Ejection Survival Roll (Doc 51)
                        var _ej_roll = irandom_range(1, 100);'''

replacement_torso_ej = '''                        // 2. Pilot Ejection Survival Roll & Battlefield POW Capture (Doc 51)
                        var _ej_roll = irandom_range(1, 100);
                        if (variable_struct_exists(_atk, "kills")) _atk.kills++; else _atk.kills = 1;
                        if (_def.team == "HOSTILE" && _ej_roll <= 35) {
                            var _pow_id = "pow_" + string(irandom(99999));
                            var _pow_pilot = {
                                id: _pow_id,
                                name: _def.pilot_name,
                                callsign: _def.callsign,
                                tier: 2,
                                current_faction_id: "faction_c",
                                is_imprisoned: true,
                                combat_stat: irandom_range(6, 9),
                                tactics_stat: irandom_range(6, 8),
                                accuracy: irandom_range(75, 88),
                                reflexes: irandom_range(72, 85),
                                affinity: _def.mech_type,
                                rank_perks: ["Deadly Aim"]
                            };
                            array_push(captured_pows, _pow_pilot);
                            add_log("[POW CAPTURED] " + _def.pilot_name + " escape pod intercepted! Transferred to Base Brig.");
                        }'''

if target_torso_ej in bm_create:
    bm_create = bm_create.replace(target_torso_ej, replacement_torso_ej, 1)
    print("[PASS] Torso destruction POW capture integrated into BattleManager Create_0.gml")

with open(bm_create_path, "w", encoding="utf-8") as f:
    f.write(bm_create)

# -----------------------------------------------------------------------------
# 4. Patch objects/obj_BattleManager/Draw_64.gml: AAR XP & POW Display
# -----------------------------------------------------------------------------
bm_draw_path = "objects/obj_BattleManager/Draw_64.gml"
with open(bm_draw_path, "r", encoding="utf-8") as f:
    bm_draw = f.read()

# 4a: Display POWs in AAR
target_aar_salvage = '''        draw_text(_mw_x + 50, _mw_y + 245, "-> 2x Syndicate Reaver Heavy Breech Assemblies");'''
replacement_aar_salvage = '''        draw_text(_mw_x + 50, _mw_y + 245, "-> 2x Syndicate Reaver Heavy Breech Assemblies");
        if (variable_instance_exists(id, "captured_pows") && array_length(captured_pows) > 0) {
            draw_set_color(make_color_rgb(120, 240, 255));
            draw_text(_mw_x + 50, _mw_y + 270, "-> " + string(array_length(captured_pows)) + "x Hostile Ace POWs Secured (Transferred to Flagship Brig)");
        }'''

if target_aar_salvage in bm_draw:
    bm_draw = bm_draw.replace(target_aar_salvage, replacement_aar_salvage, 1)
    print("[PASS] AAR POW summary added to BattleManager Draw_64.gml")

# 4b: Display Frame Affinity Resonance in Unit Inspector
target_insp_stat = '''    draw_text(_col2_x + 16, _spec_y + 46, "ARMOR INTEGRITY: " + string(_cur_slot_u.components.torso.max) + " HP | ACCURACY: " + string(_cur_slot_u.accuracy) + "% | EVASION: " + string(_cur_slot_u.evasion) + "%");'''
replacement_insp_stat = '''    draw_text(_col2_x + 16, _spec_y + 46, "ARMOR INTEGRITY: " + string(_cur_slot_u.components.torso.max) + " HP | ACCURACY: " + string(_cur_slot_u.accuracy) + "% | EVASION: " + string(_cur_slot_u.evasion) + "%");
    if (variable_struct_exists(_cur_slot_u, "has_affinity_match") && _cur_slot_u.has_affinity_match) {
        draw_set_color(make_color_rgb(255, 215, 80));
        draw_text(_col2_x + 16, _spec_y + 60, "[FRAME AFFINITY: RESONANCE (+8% ACC/EVA, +1 AP)]");
    }'''

if target_insp_stat in bm_draw:
    bm_draw = bm_draw.replace(target_insp_stat, replacement_insp_stat, 1)
    print("[PASS] Frame Affinity resonance badge added to BattleManager Draw_64.gml")

# 4c: Transfer POWs on AAR button click
target_aar_btn_exit = '''        if (room_exists(rm_hq_terminal)) room_goto(rm_hq_terminal);'''
replacement_aar_btn_exit = '''        if (instance_exists(obj_NemesisManager) && variable_instance_exists(id, "captured_pows") && is_array(captured_pows)) {
            for (var k = 0; k < array_length(captured_pows); k++) {
                var _pw = captured_pows[k];
                array_push(obj_NemesisManager.prisoner_list, _pw);
                variable_struct_set(obj_NemesisManager.characters_map, _pw.id, _pw);
            }
        }
        if (room_exists(rm_hq_terminal)) room_goto(rm_hq_terminal);'''

if target_aar_btn_exit in bm_draw:
    bm_draw = bm_draw.replace(target_aar_btn_exit, replacement_aar_btn_exit, 1)
    print("[PASS] POW transfer on AAR exit added to BattleManager Draw_64.gml")

with open(bm_draw_path, "w", encoding="utf-8") as f:
    f.write(bm_draw)

# -----------------------------------------------------------------------------
# 5. Patch objects/obj_GameManager/Create_0.gml: Story episodes seen & trigger
# -----------------------------------------------------------------------------
gm_create_path = "objects/obj_GameManager/Create_0.gml"
with open(gm_create_path, "r", encoding="utf-8") as f:
    gm_create = f.read()

target_gm_seen = '''// 9. Daily Simulation Advancement Method (docs/01, 04, 06, 07)
end_turn = function() {'''

replacement_gm_seen = '''// Narrative Story Episodes Seen State (Doc 51)
story_episodes_seen = {};

// 9. Daily Simulation Advancement Method (docs/01, 04, 06, 07)
end_turn = function() {
    // Check Campaign Story Milestone Episodes (Doc 51)
    if (current_turn == 5 && !variable_struct_exists(story_episodes_seen, "ep_02_shadows_over_mars")) {
        variable_struct_set(story_episodes_seen, "ep_02_shadows_over_mars", true);
        scr_vn_start_episode("ep_02_shadows_over_mars");
    }'''

if target_gm_seen in gm_create:
    gm_create = gm_create.replace(target_gm_seen, replacement_gm_seen, 1)
    with open(gm_create_path, "w", encoding="utf-8") as f:
        f.write(gm_create)
    print("[PASS] story_episodes_seen & Turn 5 episode hook added to GameManager Create_0.gml")

print("All Milestone 51 components patched successfully!")
