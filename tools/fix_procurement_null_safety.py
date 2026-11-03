#!/usr/bin/env python3
import sys

target = "objects/obj_HQTerminal/Draw_64.gml"
with open(target, "r") as f:
    content = f.read()

# 1. Reset trial_phase on faction selection
old_faction_click = """                if (_c_hov && _click) {
                    trial_selected_faction = _fid;
                    trial_last_result = undefined;
                }"""

new_faction_click = """                if (_c_hov && _click) {
                    trial_selected_faction = _fid;
                    trial_last_result = undefined;
                    trial_phase_results = undefined;
                    trial_phase = 0;
                }"""

assert old_faction_click in content, "Could not find old_faction_click"
content = content.replace(old_faction_click, new_faction_click)

# 2. Reset trial_phase on mech selection
old_mech_click = """                    if (_m_hov && _click) {
                        trial_selected_mech_idx = m;
                        trial_last_result = undefined;
                    }"""

new_mech_click = """                    if (_m_hov && _click) {
                        trial_selected_mech_idx = m;
                        trial_last_result = undefined;
                        trial_phase_results = undefined;
                        trial_phase = 0;
                    }"""

assert old_mech_click in content, "Could not find old_mech_click"
content = content.replace(old_mech_click, new_mech_click)

# 3. Replace Phase 2, 3, 4 blocks with null-safe implementations
old_phases_block = """                // --- PHASE 2: DYNAMIC STRESS GAUNTLET ---
                else if (trial_phase == 2) {
                    var _p2_box_y = _bc_y + 36;
                    draw_set_color(make_color_rgb(14, 24, 36));
                    draw_rectangle(_col2_x + 12, _p2_box_y, _col2_x + _col2_w - 12, _p2_box_y + 240, false);
                    draw_set_color(make_color_rgb(45, 75, 110));
                    draw_rectangle(_col2_x + 12, _p2_box_y, _col2_x + _col2_w - 12, _p2_box_y + 240, true);

                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_col2_x + 24, _p2_box_y + 12, "PHASE 2: DYNAMIC PROVING GROUNDS TELEMETRY");

                    var _bm = trial_phase_results.p2_benchmarks;
                    var _stress_items = [
                        { label: "1. Kinetic Ballistics Impact Rig", val: _bm.kinetic },
                        { label: "2. Thermal Dissipation Plasma Burn", val: _bm.thermal },
                        { label: "3. High-G Vacuum Vernier Stress", val: _bm.vernier },
                        { label: "4. ECM & Avionics Pulse Chamber", val: _bm.ecm }
                    ];

                    for (var si = 0; si < 4; si++) {
                        var _sy = _p2_box_y + 40 + si * 46;
                        var _it = _stress_items[si];
                        draw_set_color(make_color_rgb(180, 210, 240));
                        draw_text(_col2_x + 24, _sy, _it.label + " : " + string(_it.val) + " / 100 PTS");
                        scr_draw_snes_gauge(_col2_x + 24, _sy + 20, _col2_w - 48, 14, _it.val, 140, (_it.val >= 100) ? c_lime : make_color_rgb(240, 160, 40));
                    }

                    // Advance to Phase 3 Button
                    var _p3_btn_y = _p2_box_y + 252;
                    var _p3_hov = (_mx >= _col2_x + 14 && _mx <= _col2_x + _col2_w - 14 && _my >= _p3_btn_y && _my <= _p3_btn_y + 44);
                    if (_p3_hov && _click) {
                        trial_phase_results = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 3, trial_refinements);
                        trial_phase = 3;
                        show_toast("PHASE 3 INITIATED: OPERATIONAL FLY-OFF DUEL COMMENCED!", c_aqua);
                    }
                    scr_draw_snes_button(_col2_x + 14, _p3_btn_y, _col2_w - 28, 44, ">> PROCEED TO PHASE 3: OPERATIONAL FLY-OFF COMBAT DUEL >>", _p3_hov, false, make_color_rgb(100, 220, 255));
                }
                // --- PHASE 3: OPERATIONAL FLY-OFF COMBAT DUEL ---
                else if (trial_phase == 3) {
                    var _p3_box_y = _bc_y + 36;
                    draw_set_color(make_color_rgb(14, 24, 36));
                    draw_rectangle(_col2_x + 12, _p3_box_y, _col2_x + _col2_w - 12, _p3_box_y + 240, false);
                    draw_set_color(make_color_rgb(45, 75, 110));
                    draw_rectangle(_col2_x + 12, _p3_box_y, _col2_x + _col2_w - 12, _p3_box_y + 240, true);

                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_col2_x + 24, _p3_box_y + 12, "PHASE 3: OPERATIONAL COMBAT FLY-OFF DUEL");

                    // Duel Rival Matchup Banner
                    var _rc = trial_phase_results.p3_rival_corp;
                    var _rs = trial_phase_results.p3_rival_score;
                    var _cs = trial_phase_results.composite_score;
                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_col2_x + 24, _p3_box_y + 40, "MATCHUP: " + string(_cur_cand.name ?? "Candidate") + " (Vanguard PMC)  vs  " + string(_rc ?? "Rival") + " Champion");

                    draw_set_color(make_color_rgb(180, 210, 240));
                    draw_text(_col2_x + 24, _p3_box_y + 68, "Rival Contractor Standard: " + string(_rs) + " PTS   |   Candidate Score: " + string(_cs) + " PTS");

                    // Combat Pedigree Showcase
                    var _ped_pts = trial_phase_results.pedigree_bonus;
                    var _ped_tag = trial_phase_results.pedigree_rating;
                    draw_set_color((_ped_pts > 0) ? make_color_rgb(255, 215, 80) : make_color_rgb(140, 160, 180));
                    draw_text(_col2_x + 24, _p3_box_y + 96, "PMC Combat Telemetry: " + _ped_tag + " (+" + string(_ped_pts) + " pts from live combat sorties)");

                    // Telemetry Duel Outcome
                    var _duel_win = trial_phase_results.p3_duel_win;
                    draw_set_color(_duel_win ? make_color_rgb(80, 255, 140) : make_color_rgb(255, 100, 100));
                    draw_text(_col2_x + 24, _p3_box_y + 130, _duel_win ? "*** TACTICAL SUPERIORITY ACHIEVED: Candidate out-flew " + _rc + " in live trial! ***" : "!!! TACTICAL DEFICIT: Candidate was out-maneuvered by " + _rc + " entry !!!");

                    // Advance to Phase 4 Button
                    var _p4_btn_y = _p3_box_y + 252;
                    var _p4_hov = (_mx >= _col2_x + 14 && _mx <= _col2_x + _col2_w - 14 && _my >= _p4_btn_y && _my <= _p4_btn_y + 44);
                    if (_p4_hov && _click) {
                        trial_last_result = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 4, trial_refinements);
                        trial_phase_results = trial_last_result;
                        trial_phase = 4;
                        show_toast("PHASE 4 CONCLUDED: BOARD VERDICT DELIVERED!", c_lime);
                    }
                    scr_draw_snes_button(_col2_x + 14, _p4_btn_y, _col2_w - 28, 44, ">> ADVANCE TO PHASE 4: PROCUREMENT BOARD FINAL VERDICT >>", _p4_hov, false, make_color_rgb(80, 255, 140));
                }
                // --- PHASE 4: FINAL BOARD VERDICT & RATIFICATION ---
                else if (trial_phase == 4) {
                    var _res_y = _bc_y + 36;
                    var _res_w = _col2_w - 24;
                    var _res_h = 245;

                    draw_set_color(trial_last_result.passed ? make_color_rgb(12, 36, 20) : make_color_rgb(36, 16, 16));
                    draw_rectangle(_col2_x + 12, _res_y, _col2_x + 12 + _res_w, _res_y + _res_h, false);
                    draw_set_color(trial_last_result.passed ? make_color_rgb(60, 240, 120) : make_color_rgb(240, 60, 60));
                    draw_rectangle(_col2_x + 12, _res_y, _col2_x + 12 + _res_w, _res_y + _res_h, true);

                    // Official Stamp
                    var _st_idx = (trial_last_result.grade == "GRADE S") ? 0 : ((trial_last_result.grade == "GRADE A") ? 1 : ((trial_last_result.grade == "GRADE B") ? 2 : 3));
                    scr_draw_snes_trial_stamp(_col2_x + 24, _res_y + 10, _st_idx);

                    draw_set_color(trial_last_result.passed ? make_color_rgb(255, 220, 100) : make_color_rgb(255, 100, 100));
                    draw_text(_col2_x + 120, _res_y + 14, trial_last_result.passed ? "*** BOARD VERDICT: TENDER APPROVED (" + trial_last_result.grade + ") ***" : "!!! BOARD VERDICT: CANDIDACY REJECTED (" + trial_last_result.grade + ") !!!");

                    draw_set_color(c_white);
                    draw_text(_col2_x + 24, _res_y + 44, "Stress Armor: " + string(trial_last_result.score_armor) + "/100  |  Reactor: " + string(trial_last_result.score_power) + "/100  |  Mobility: " + string(trial_last_result.score_speed) + "/100  |  Combat: " + string(trial_last_result.score_combat) + "/100");
                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_col2_x + 24, _res_y + 66, "Standing Bonus: +" + string(trial_last_result.standing_bonus) + " pts  |  Combat Pedigree: +" + string(trial_last_result.pedigree_bonus) + " pts  ==>  COMPOSITE: " + string(trial_last_result.composite_score) + " / 100 PTS");

                    draw_set_color(trial_last_result.passed ? make_color_rgb(140, 255, 180) : make_color_rgb(255, 180, 180));
                    draw_text(_col2_x + 24, _res_y + 92, trial_last_result.report);

                    // Ratification Action Button
                    if (trial_last_result.passed) {
                        var _rat_btn_y = _res_y + 130;
                        var _rat_btn_w = _res_w - 24;
                        var _rat_btn_h = 46;
                        var _rat_hov = (_mx >= _col2_x + 24 && _mx <= _col2_x + 24 + _rat_btn_w && _my >= _rat_btn_y && _my <= _rat_btn_y + _rat_btn_h);
                        if (_rat_hov && _click) {
                            _fm.award_procurement_contract(trial_selected_faction, _cur_cand, trial_last_result);
                            trial_phase = 0;
                            trial_view_adoption_panel = true;
                        }
                        var _bounty_val = _cur_mp.replaced ? floor(_cur_mp.licensing_bounty * 0.6) : _cur_mp.licensing_bounty;
                        scr_draw_snes_button(_col2_x + 24, _rat_btn_y, _rat_btn_w, _rat_btn_h, ">> RATIFY TENDER TREATY // CLAIM +" + string(_bounty_val) + " Cr & ENTER SHIPYARD TOOLING <<", _rat_hov, false, make_color_rgb(80, 255, 140));
                    }

                    // Reset / Return to Phase 0 Button
                    var _rst_btn_y = _res_y + 184;
                    var _rst_hov = (_mx >= _col2_x + 24 && _mx <= _col2_x + 220 && _my >= _rst_btn_y && _my <= _rst_btn_y + 32);
                    if (_rst_hov && _click) {
                        trial_phase = 0;
                        trial_last_result = undefined;
                        trial_phase_results = undefined;
                        trial_refinements = [];
                    }
                    scr_draw_snes_button(_col2_x + 24, _rst_btn_y, 196, 32, "<< RESET TO PHASE 1 <<", _rst_hov, false, c_dkgray);
                }"""

new_phases_block = """                // --- PHASE 2: DYNAMIC STRESS GAUNTLET ---
                else if (trial_phase == 2) {
                    // Safe guard: Ensure trial_phase_results exists and has p2_benchmarks
                    if (!is_struct(trial_phase_results) || !variable_struct_exists(trial_phase_results, "p2_benchmarks")) {
                        if (!is_undefined(_cur_cand)) {
                            trial_phase_results = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 2, trial_refinements);
                        }
                    }
                    if (!is_struct(trial_phase_results) || !variable_struct_exists(trial_phase_results, "p2_benchmarks")) {
                        trial_phase = 0;
                    } else {
                        var _p2_box_y = _bc_y + 36;
                        draw_set_color(make_color_rgb(14, 24, 36));
                        draw_rectangle(_col2_x + 12, _p2_box_y, _col2_x + _col2_w - 12, _p2_box_y + 240, false);
                        draw_set_color(make_color_rgb(45, 75, 110));
                        draw_rectangle(_col2_x + 12, _p2_box_y, _col2_x + _col2_w - 12, _p2_box_y + 240, true);

                        draw_set_color(make_color_rgb(255, 215, 80));
                        draw_text(_col2_x + 24, _p2_box_y + 12, "PHASE 2: DYNAMIC PROVING GROUNDS TELEMETRY");

                        var _bm = trial_phase_results.p2_benchmarks;
                        var _k_val = is_struct(_bm) ? (variable_struct_get(_bm, "kinetic") ?? 50) : 50;
                        var _t_val = is_struct(_bm) ? (variable_struct_get(_bm, "thermal") ?? 50) : 50;
                        var _v_val = is_struct(_bm) ? (variable_struct_get(_bm, "vernier") ?? 50) : 50;
                        var _e_val = is_struct(_bm) ? (variable_struct_get(_bm, "ecm") ?? 50) : 50;

                        var _stress_items = [
                            { label: "1. Kinetic Ballistics Impact Rig", val: _k_val },
                            { label: "2. Thermal Dissipation Plasma Burn", val: _t_val },
                            { label: "3. High-G Vacuum Vernier Stress", val: _v_val },
                            { label: "4. ECM & Avionics Pulse Chamber", val: _e_val }
                        ];

                        for (var si = 0; si < 4; si++) {
                            var _sy = _p2_box_y + 40 + si * 46;
                            var _it = _stress_items[si];
                            draw_set_color(make_color_rgb(180, 210, 240));
                            draw_text(_col2_x + 24, _sy, _it.label + " : " + string(_it.val) + " / 100 PTS");
                            scr_draw_snes_gauge(_col2_x + 24, _sy + 20, _col2_w - 48, 14, _it.val, 140, (_it.val >= 100) ? c_lime : make_color_rgb(240, 160, 40));
                        }

                        // Advance to Phase 3 Button
                        var _p3_btn_y = _p2_box_y + 252;
                        var _p3_hov = (_mx >= _col2_x + 14 && _mx <= _col2_x + _col2_w - 14 && _my >= _p3_btn_y && _my <= _p3_btn_y + 44);
                        if (_p3_hov && _click) {
                            if (!is_undefined(_cur_cand)) {
                                trial_phase_results = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 3, trial_refinements);
                                trial_phase = 3;
                                show_toast("PHASE 3 INITIATED: OPERATIONAL FLY-OFF DUEL COMMENCED!", c_aqua);
                            } else {
                                trial_phase = 0;
                            }
                        }
                        scr_draw_snes_button(_col2_x + 14, _p3_btn_y, _col2_w - 28, 44, ">> PROCEED TO PHASE 3: OPERATIONAL FLY-OFF COMBAT DUEL >>", _p3_hov, false, make_color_rgb(100, 220, 255));
                    }
                }
                // --- PHASE 3: OPERATIONAL FLY-OFF COMBAT DUEL ---
                else if (trial_phase == 3) {
                    if (!is_struct(trial_phase_results) || !variable_struct_exists(trial_phase_results, "p3_rival_corp")) {
                        if (!is_undefined(_cur_cand)) {
                            trial_phase_results = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 3, trial_refinements);
                        }
                    }
                    if (!is_struct(trial_phase_results) || !variable_struct_exists(trial_phase_results, "p3_rival_corp")) {
                        trial_phase = 0;
                    } else {
                        var _p3_box_y = _bc_y + 36;
                        draw_set_color(make_color_rgb(14, 24, 36));
                        draw_rectangle(_col2_x + 12, _p3_box_y, _col2_x + _col2_w - 12, _p3_box_y + 240, false);
                        draw_set_color(make_color_rgb(45, 75, 110));
                        draw_rectangle(_col2_x + 12, _p3_box_y, _col2_x + _col2_w - 12, _p3_box_y + 240, true);

                        draw_set_color(make_color_rgb(255, 215, 80));
                        draw_text(_col2_x + 24, _p3_box_y + 12, "PHASE 3: OPERATIONAL COMBAT FLY-OFF DUEL");

                        // Duel Rival Matchup Banner
                        var _rc = variable_struct_get(trial_phase_results, "p3_rival_corp") ?? "Valkyrie Heavy";
                        var _rs = variable_struct_get(trial_phase_results, "p3_rival_score") ?? 100;
                        var _cs = variable_struct_get(trial_phase_results, "composite_score") ?? 100;
                        var _cand_title = !is_undefined(_cur_cand) ? (variable_struct_get(_cur_cand, "name") ?? "Candidate") : "Candidate";
                        draw_set_color(make_color_rgb(100, 220, 255));
                        draw_text(_col2_x + 24, _p3_box_y + 40, "MATCHUP: " + string(_cand_title) + " (Vanguard PMC)  vs  " + string(_rc) + " Champion");

                        draw_set_color(make_color_rgb(180, 210, 240));
                        draw_text(_col2_x + 24, _p3_box_y + 68, "Rival Contractor Standard: " + string(_rs) + " PTS   |   Candidate Score: " + string(_cs) + " PTS");

                        // Combat Pedigree Showcase
                        var _ped_pts = variable_struct_get(trial_phase_results, "pedigree_bonus") ?? 0;
                        var _ped_tag = variable_struct_get(trial_phase_results, "pedigree_rating") ?? "UNTESTED";
                        draw_set_color((_ped_pts > 0) ? make_color_rgb(255, 215, 80) : make_color_rgb(140, 160, 180));
                        draw_text(_col2_x + 24, _p3_box_y + 96, "PMC Combat Telemetry: " + _ped_tag + " (+" + string(_ped_pts) + " pts from live combat sorties)");

                        // Telemetry Duel Outcome
                        var _duel_win = variable_struct_get(trial_phase_results, "p3_duel_win") ?? (_cs >= _rs);
                        draw_set_color(_duel_win ? make_color_rgb(80, 255, 140) : make_color_rgb(255, 100, 100));
                        draw_text(_col2_x + 24, _p3_box_y + 130, _duel_win ? "*** TACTICAL SUPERIORITY ACHIEVED: Candidate out-flew " + _rc + " in live trial! ***" : "!!! TACTICAL DEFICIT: Candidate was out-maneuvered by " + _rc + " entry !!!");

                        // Advance to Phase 4 Button
                        var _p4_btn_y = _p3_box_y + 252;
                        var _p4_hov = (_mx >= _col2_x + 14 && _mx <= _col2_x + _col2_w - 14 && _my >= _p4_btn_y && _my <= _p4_btn_y + 44);
                        if (_p4_hov && _click) {
                            if (!is_undefined(_cur_cand)) {
                                trial_last_result = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 4, trial_refinements);
                                trial_phase_results = trial_last_result;
                                trial_phase = 4;
                                show_toast("PHASE 4 CONCLUDED: BOARD VERDICT DELIVERED!", c_lime);
                            } else {
                                trial_phase = 0;
                            }
                        }
                        scr_draw_snes_button(_col2_x + 14, _p4_btn_y, _col2_w - 28, 44, ">> ADVANCE TO PHASE 4: PROCUREMENT BOARD FINAL VERDICT >>", _p4_hov, false, make_color_rgb(80, 255, 140));
                    }
                }
                // --- PHASE 4: FINAL BOARD VERDICT & RATIFICATION ---
                else if (trial_phase == 4) {
                    if (!is_struct(trial_last_result) || !variable_struct_exists(trial_last_result, "grade")) {
                        if (!is_undefined(_cur_cand)) {
                            trial_last_result = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 4, trial_refinements);
                            trial_phase_results = trial_last_result;
                        }
                    }
                    if (!is_struct(trial_last_result) || !variable_struct_exists(trial_last_result, "grade")) {
                        trial_phase = 0;
                    } else {
                        var _res_y = _bc_y + 36;
                        var _res_w = _col2_w - 24;
                        var _res_h = 245;
                        var _t_pass = variable_struct_get(trial_last_result, "passed") ?? false;
                        var _t_grade = variable_struct_get(trial_last_result, "grade") ?? "GRADE B";
                        var _t_arm = variable_struct_get(trial_last_result, "score_armor") ?? 100;
                        var _t_pwr = variable_struct_get(trial_last_result, "score_power") ?? 100;
                        var _t_spd = variable_struct_get(trial_last_result, "score_speed") ?? 100;
                        var _t_cbt = variable_struct_get(trial_last_result, "score_combat") ?? 100;
                        var _t_st = variable_struct_get(trial_last_result, "standing_bonus") ?? 0;
                        var _t_ped = variable_struct_get(trial_last_result, "pedigree_bonus") ?? 0;
                        var _t_comp = variable_struct_get(trial_last_result, "composite_score") ?? 100;
                        var _t_rep = variable_struct_get(trial_last_result, "report") ?? "Evaluation Complete.";

                        draw_set_color(_t_pass ? make_color_rgb(12, 36, 20) : make_color_rgb(36, 16, 16));
                        draw_rectangle(_col2_x + 12, _res_y, _col2_x + 12 + _res_w, _res_y + _res_h, false);
                        draw_set_color(_t_pass ? make_color_rgb(60, 240, 120) : make_color_rgb(240, 60, 60));
                        draw_rectangle(_col2_x + 12, _res_y, _col2_x + 12 + _res_w, _res_y + _res_h, true);

                        // Official Stamp
                        var _st_idx = (_t_grade == "GRADE S") ? 0 : ((_t_grade == "GRADE A") ? 1 : ((_t_grade == "GRADE B") ? 2 : 3));
                        scr_draw_snes_trial_stamp(_col2_x + 24, _res_y + 10, _st_idx);

                        draw_set_color(_t_pass ? make_color_rgb(255, 220, 100) : make_color_rgb(255, 100, 100));
                        draw_text(_col2_x + 120, _res_y + 14, _t_pass ? "*** BOARD VERDICT: TENDER APPROVED (" + _t_grade + ") ***" : "!!! BOARD VERDICT: CANDIDACY REJECTED (" + _t_grade + ") !!!");

                        draw_set_color(c_white);
                        draw_text(_col2_x + 24, _res_y + 44, "Stress Armor: " + string(_t_arm) + "/100  |  Reactor: " + string(_t_pwr) + "/100  |  Mobility: " + string(_t_spd) + "/100  |  Combat: " + string(_t_cbt) + "/100");
                        draw_set_color(make_color_rgb(100, 220, 255));
                        draw_text(_col2_x + 24, _res_y + 66, "Standing Bonus: +" + string(_t_st) + " pts  |  Combat Pedigree: +" + string(_t_ped) + " pts  ==>  COMPOSITE: " + string(_t_comp) + " / 100 PTS");

                        draw_set_color(_t_pass ? make_color_rgb(140, 255, 180) : make_color_rgb(255, 180, 180));
                        draw_text(_col2_x + 24, _res_y + 92, _t_rep);

                        // Ratification Action Button
                        if (_t_pass) {
                            var _rat_btn_y = _res_y + 130;
                            var _rat_btn_w = _res_w - 24;
                            var _rat_btn_h = 46;
                            var _rat_hov = (_mx >= _col2_x + 24 && _mx <= _col2_x + 24 + _rat_btn_w && _my >= _rat_btn_y && _my <= _rat_btn_y + _rat_btn_h);
                            if (_rat_hov && _click) {
                                _fm.award_procurement_contract(trial_selected_faction, _cur_cand, trial_last_result);
                                trial_phase = 0;
                                trial_view_adoption_panel = true;
                            }
                            var _bounty_val = _cur_mp.replaced ? floor(_cur_mp.licensing_bounty * 0.6) : _cur_mp.licensing_bounty;
                            scr_draw_snes_button(_col2_x + 24, _rat_btn_y, _rat_btn_w, _rat_btn_h, ">> RATIFY TENDER TREATY // CLAIM +" + string(_bounty_val) + " Cr & ENTER SHIPYARD TOOLING <<", _rat_hov, false, make_color_rgb(80, 255, 140));
                        }

                        // Reset / Return to Phase 0 Button
                        var _rst_btn_y = _res_y + 184;
                        var _rst_hov = (_mx >= _col2_x + 24 && _mx <= _col2_x + 220 && _my >= _rst_btn_y && _my <= _rst_btn_y + 32);
                        if (_rst_hov && _click) {
                            trial_phase = 0;
                            trial_last_result = undefined;
                            trial_phase_results = undefined;
                            trial_refinements = [];
                        }
                        scr_draw_snes_button(_col2_x + 24, _rst_btn_y, 196, 32, "<< RESET TO PHASE 1 <<", _rst_hov, false, c_dkgray);
                    }
                }"""

assert old_phases_block in content, "Could not find old_phases_block"
content = content.replace(old_phases_block, new_phases_block)

with open(target, "w") as f:
    f.write(content)

print("[SUCCESS] Patched obj_HQTerminal/Draw_64.gml with full null-safety for all procurement trial phases!")
