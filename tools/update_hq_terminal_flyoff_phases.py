import re

with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
    lines = f.readlines()

# Locate line 2975 where right box starts
start_idx = -1
end_idx = -1
for i, l in enumerate(lines):
    if "Right Box: Fly-Off Diagnostic & Benchmark Arena" in l:
        start_idx = i
        break

for i in range(start_idx, len(lines)):
    if "// SUBTAB 2: INTERSTELLAR COMMODITY TRADE EXCHANGE" in lines[i]:
        end_idx = i - 3
        break

print(f"Target slice: lines {start_idx+1} to {end_idx+1}")

new_arena_code = '''            // Right Box: 4-Phase Fly-Off Tournament Arena & Fleet Adoption Lifecycle (docs/26)
            var _cur_mp = _mpc[$ trial_selected_faction];
            var _is_adopted = (!is_undefined(_cur_mp) && _cur_mp.replaced);
            var _inc = _fm.get_incumbent_specs(trial_selected_faction);
            var _cur_cand = (trial_selected_mech_idx >= 0 && trial_selected_mech_idx < array_length(_mechs)) ? _mechs[trial_selected_mech_idx] : undefined;

            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_col2_x, _arena_y, _col2_x + _col2_w, _arena_y + _arena_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_col2_x, _arena_y, _col2_x + _col2_w, _arena_y + _arena_h, true);

            // Top Header: Title + Adoption Toggle Tab
            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_col2_x + 14, _arena_y + 10, "PROCUREMENT BUREAU: " + _inc.faction_name);
            draw_set_color(make_color_rgb(160, 190, 220));
            draw_text(_col2_x + 14, _arena_y + 28, "Evaluator: " + _inc.evaluator + " | Doctrine Focus: " + _inc.doctrine_focus);

            if (_is_adopted) {
                var _tgl_w = 200;
                var _tgl_x = _col2_x + _col2_w - _tgl_w - 14;
                var _tgl_y = _arena_y + 8;
                var _tgl_hov = (_mx >= _tgl_x && _mx <= _tgl_x + _tgl_w && _my >= _tgl_y && _my <= _tgl_y + 28);
                if (_tgl_hov && _click) {
                    trial_view_adoption_panel = !trial_view_adoption_panel;
                }
                scr_draw_snes_button(_tgl_x, _tgl_y, _tgl_w, 28, trial_view_adoption_panel ? "[ENTER FLY-OFF ARENA]" : "[FLEET ADOPTION MGMT]", _tgl_hov, trial_view_adoption_panel, make_color_rgb(80, 220, 140));
            }

            // =========================================================================
            // VIEW A: FLEET ADOPTION & MODERNIZATION DASHBOARD (docs/26 Pillar II & III)
            // =========================================================================
            if (_is_adopted && trial_view_adoption_panel) {
                var _dash_y = _arena_y + 48;
                draw_set_color(make_color_rgb(14, 22, 32));
                draw_rectangle(_col2_x + 12, _dash_y, _col2_x + _col2_w - 12, _arena_y + _arena_h - 12, false);
                draw_set_color(make_color_rgb(45, 75, 110));
                draw_rectangle(_col2_x + 12, _dash_y, _col2_x + _col2_w - 12, _arena_y + _arena_h - 12, true);

                var _stg = _cur_mp[$ "adoption_stage"] ?? "MATURE";
                var _blk = _cur_mp[$ "block_level"] ?? 1;
                var _units = _cur_mp[$ "active_frontline_units"] ?? 50;

                // Stamp & Header
                var _stamp_idx = (_stg == "TOOLING") ? 5 : ((_blk >= 3) ? 0 : ((_blk == 2) ? 4 : 1));
                scr_draw_snes_trial_stamp(_col2_x + 24, _dash_y + 14, _stamp_idx);

                draw_set_color(make_color_rgb(255, 220, 100));
                draw_text(_col2_x + 120, _dash_y + 12, "ADOPTED DOCTRINE: " + _cur_mp.replacement_name + " (BLOCK " + string(_blk) + ")");
                draw_set_color(make_color_rgb(160, 200, 230));
                draw_text(_col2_x + 120, _dash_y + 30, "Lifecycle Status: " + _stg + " | Base Doctrine Bonus: +" + string(_cur_mp.combat_bonus));

                // Status Cards & Progress
                if (_stg == "TOOLING") {
                    var _tool_rem = _cur_mp[$ "tooling_turns_remaining"] ?? 2;
                    draw_set_color(make_color_rgb(255, 200, 60));
                    draw_text(_col2_x + 24, _dash_y + 56, "SHIPYARD TOOLING IN PROGRESS: " + string(_tool_rem) + " Turn(s) until first flight wing deployment.");
                    scr_draw_snes_hazard_bar(_col2_x + 24, _dash_y + 76, _col2_w - 48, 12, true);

                    // Expedite Button
                    var _exp_btn_y = _dash_y + 105;
                    var _exp_btn_w = _col2_w - 48;
                    var _exp_btn_h = 44;
                    var _exp_hov = (_mx >= _col2_x + 24 && _mx <= _col2_x + 24 + _exp_btn_w && _my >= _exp_btn_y && _my <= _exp_btn_y + _exp_btn_h);
                    if (_exp_hov && _click) {
                        _fm.expedite_adoption_tooling(trial_selected_faction);
                    }
                    scr_draw_snes_button(_col2_x + 24, _exp_btn_y, _exp_btn_w, _exp_btn_h, ">> EXPEDITE TOOLING (-40,000 Cr) // ADVANCE TIMELINE BY 1 TURN <<", _exp_hov, false, make_color_rgb(255, 200, 60));
                } else {
                    // Fleet Rollout Metrics
                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_col2_x + 24, _dash_y + 56, "Active Frontline Fleet: " + string(_units) + " / 250 Units in Combat Service");
                    scr_draw_snes_gauge(_col2_x + 24, _dash_y + 76, _col2_w - 48, 14, _units, 250, c_lime);

                    draw_set_color(make_color_rgb(180, 210, 240));
                    draw_text(_col2_x + 24, _dash_y + 100, "Turn Royalty Revenue: +" + string(_cur_mp.royalty_per_turn) + " Cr/turn   |   Cumulative Paid: +" + string(_cur_mp.cumulative_royalties_paid) + " Cr");
                    draw_text(_col2_x + 24, _dash_y + 120, "Arms Dealer Paradox: Player squad gains +15% Crit / +20% AP against this chassis.");

                    // Modernization Upgrade Cards (Block II / Block III)
                    var _upg_btn_y = _dash_y + 155;
                    var _upg_btn_w = _col2_w - 48;
                    var _upg_btn_h = 46;

                    if (_blk == 1) {
                        var _can_b2 = (_units >= 50);
                        var _b2_hov = (_can_b2 && _mx >= _col2_x + 24 && _mx <= _col2_x + 24 + _upg_btn_w && _my >= _upg_btn_y && _my <= _upg_btn_y + _upg_btn_h);
                        if (_b2_hov && _click) {
                            _fm.upgrade_adoption_block_ii(trial_selected_faction);
                        }
                        scr_draw_snes_button(_col2_x + 24, _upg_btn_y, _upg_btn_w, _upg_btn_h, ">> RATIFY BLOCK II MODERNIZATION // CLAIM +450,000 Cr BOUNTY & +25% ROYALTIES <<", _b2_hov, false, _can_b2 ? make_color_rgb(255, 215, 80) : c_dkgray);
                    } else if (_blk == 2) {
                        var _b3_hov = (_mx >= _col2_x + 24 && _mx <= _col2_x + 24 + _upg_btn_w && _my >= _upg_btn_y && _my <= _upg_btn_y + _upg_btn_h);
                        if (_b3_hov && _click) {
                            _fm.upgrade_adoption_block_iii(trial_selected_faction);
                        }
                        scr_draw_snes_button(_col2_x + 24, _upg_btn_y, _upg_btn_w, _upg_btn_h, ">> UPGRADE TO BLOCK III ACE CUSTOM // CLAIM +750,000 Cr & FREE ACE HANGAR MECH <<", _b3_hov, false, make_color_rgb(80, 240, 180));
                    } else {
                        draw_set_color(make_color_rgb(80, 255, 140));
                        draw_text(_col2_x + 24, _upg_btn_y + 14, "*** APEX PROTOCOL: BLOCK III VANGUARD STANDARD ACHIEVED // MAXIMUM REFINEMENT ***");
                    }
                }

                // Switch back button
                var _sw_btn_y = _arena_y + _arena_h - 48;
                var _sw_hov = (_mx >= _col2_x + 24 && _mx <= _col2_x + 280 && _my >= _sw_btn_y && _my <= _sw_btn_y + 32);
                if (_sw_hov && _click) {
                    trial_view_adoption_panel = false;
                }
                scr_draw_snes_button(_col2_x + 24, _sw_btn_y, 256, 32, ">> CHALLENGE WITH NEW MECH >>", _sw_hov, false, make_color_rgb(100, 200, 255));
            }
            // =========================================================================
            // VIEW B: 4-PHASE FLY-OFF TOURNAMENT ARENA (docs/26 Pillar I)
            // =========================================================================
            else {
                // 4-Phase Breadcrumb Bar Header
                var _bc_y = _arena_y + 46;
                var _bc_w = floor((_col2_w - 24) / 4);
                var _phase_names = ["[1. STATIC AUDIT]", "[2. STRESS GAUNTLET]", "[3. COMBAT FLY-OFF]", "[4. RATIFICATION]"];
                for (var ph = 0; ph < 4; ph++) {
                    var _bx = _col2_x + 12 + ph * _bc_w;
                    var _is_cur_ph = (trial_phase == (ph + 1) || (trial_phase == 0 && ph == 0));
                    var _is_past_ph = (trial_phase > (ph + 1));
                    draw_set_color(_is_cur_ph ? make_color_rgb(18, 54, 76) : (_is_past_ph ? make_color_rgb(12, 34, 20) : make_color_rgb(12, 16, 22)));
                    draw_rectangle(_bx, _bc_y, _bx + _bc_w - 4, _bc_y + 24, false);
                    draw_set_color(_is_cur_ph ? make_color_rgb(100, 240, 255) : (_is_past_ph ? c_lime : make_color_rgb(60, 80, 100)));
                    draw_rectangle(_bx, _bc_y, _bx + _bc_w - 4, _bc_y + 24, true);
                    draw_text(_bx + 6, _bc_y + 5, _phase_names[ph]);
                }

                // --- PHASE 0 & 1: STATIC VIABILITY AUDIT & MID-TRIAL REFINEMENTS ---
                if (trial_phase <= 1) {
                    var _cmp_y = _bc_y + 32;
                    draw_set_color(make_color_rgb(14, 24, 36));
                    draw_rectangle(_col2_x + 12, _cmp_y, _col2_x + _col2_w - 12, _cmp_y + 115, false);
                    draw_set_color(make_color_rgb(45, 75, 110));
                    draw_rectangle(_col2_x + 12, _cmp_y, _col2_x + _col2_w - 12, _cmp_y + 115, true);

                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_col2_x + 24, _cmp_y + 6, "METRIC");
                    draw_text(_col2_x + 240, _cmp_y + 6, "CANDIDATE: " + (!is_undefined(_cur_cand) ? _cur_cand.name : "None"));
                    draw_text(_col2_x + 500, _cmp_y + 6, "INCUMBENT: " + _inc.name);

                    var _cand_arm = !is_undefined(_cur_cand) ? _cur_cand.armor_rating : 0;
                    var _cand_pwr = !is_undefined(_cur_cand) ? _cur_cand.power_output : 0;
                    var _cand_spd = !is_undefined(_cur_cand) ? _cur_cand.speed : 0;
                    var _cand_cr = !is_undefined(_cur_cand) ? _cur_cand.combat_rating : 0;

                    var _rows = [
                        { label: "1. Armor Plating", c_val: string(_cand_arm) + " HP", i_val: string(_inc.armor) + " HP", pass: (_cand_arm >= _inc.armor) },
                        { label: "2. Reactor Surplus", c_val: "+" + string(_cand_pwr) + " MW", i_val: "+" + string(_inc.power) + " MW", pass: (_cand_pwr >= _inc.power) },
                        { label: "3. Maximum Speed", c_val: string(_cand_spd) + " kph", i_val: string(_inc.speed) + " kph", pass: (_cand_spd >= _inc.speed) },
                        { label: "4. Combat Rating", c_val: string(_cand_cr) + " PTS", i_val: string(_inc.combat_rating) + " PTS", pass: (_cand_cr >= _inc.combat_rating) }
                    ];

                    for (var r = 0; r < 4; r++) {
                        var _ry = _cmp_y + 24 + r * 22;
                        var _rw = _rows[r];
                        draw_set_color(make_color_rgb(180, 200, 220));
                        draw_text(_col2_x + 24, _ry, _rw.label);
                        draw_set_color(_rw.pass ? c_lime : make_color_rgb(240, 160, 60));
                        draw_text(_col2_x + 240, _ry, _rw.c_val);
                        draw_set_color(make_color_rgb(200, 200, 200));
                        draw_text(_col2_x + 500, _ry, _rw.i_val);
                    }

                    // Emergency Field Refinements Section (docs/26)
                    var _ref_y = _cmp_y + 125;
                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_col2_x + 14, _ref_y, "EMERGENCY FIELD REFINEMENTS (APPLY BEFORE STRESS GAUNTLET):");

                    var _ref_opts = [
                        { id: "OVERCLOCK_REACTOR", label: "+15% Core (25k)", cost: 25000 },
                        { id: "WELD_ARMOR", label: "+12% Armor (20k)", cost: 20000 },
                        { id: "TUNE_VERNIERS", label: "+15% Vernier (25k)", cost: 25000 },
                        { id: "RECALIBRATE_SENSORS", label: "+10% Sensors (30k)", cost: 30000 }
                    ];
                    var _rw_btn = floor((_col2_w - 28) / 4);
                    for (var ro = 0; ro < 4; ro++) {
                        var _opt = _ref_opts[ro];
                        var _rx = _col2_x + 14 + ro * _rw_btn;
                        var _is_on = (array_get_index(trial_refinements, _opt.id) != -1);
                        var _rhov = (_mx >= _rx && _mx <= _rx + _rw_btn - 6 && _my >= _ref_y + 20 && _my <= _ref_y + 52);
                        if (_rhov && _click) {
                            if (_is_on) {
                                var _idx_rem = array_get_index(trial_refinements, _opt.id);
                                array_delete(trial_refinements, _idx_rem, 1);
                                _gm.funds += _opt.cost;
                            } else {
                                if (_gm.funds >= _opt.cost) {
                                    _gm.funds -= _opt.cost;
                                    array_push(trial_refinements, _opt.id);
                                    show_toast("APPLIED REFINEMENT: " + _opt.id + "!", c_lime);
                                } else {
                                    show_toast("INSUFFICIENT FUNDS FOR REFINEMENT!", c_red);
                                }
                            }
                        }
                        scr_draw_snes_button(_rx, _ref_y + 20, _rw_btn - 6, 32, _opt.label, _rhov, _is_on, _is_on ? make_color_rgb(80, 240, 140) : make_color_rgb(100, 150, 190));
                    }

                    // Advance to Phase 2 Button
                    var _p2_btn_y = _ref_y + 62;
                    var _can_run = (!is_undefined(_cur_cand));
                    var _p2_hov = (_can_run && _mx >= _col2_x + 14 && _mx <= _col2_x + _col2_w - 14 && _my >= _p2_btn_y && _my <= _p2_btn_y + 40);
                    if (_p2_hov && _click) {
                        trial_phase_results = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 2, trial_refinements);
                        trial_phase = 2;
                        show_toast("PHASE 2 INITIATED: PROVING GROUNDS STRESS RIGS ACTIVATED!", c_aqua);
                    }
                    scr_draw_snes_button(_col2_x + 14, _p2_btn_y, _col2_w - 28, 40, ">> ADVANCE TO PHASE 2: PROVING GROUNDS STRESS GAUNTLET >>", _p2_hov, false, make_color_rgb(100, 220, 255));

                    // Quick Evaluate Button (Runs all 4 phases immediately)
                    var _qk_btn_y = _p2_btn_y + 46;
                    var _qk_hov = (_can_run && _mx >= _col2_x + 14 && _mx <= _col2_x + _col2_w - 14 && _my >= _qk_btn_y && _my <= _qk_btn_y + 30);
                    if (_qk_hov && _click) {
                        trial_last_result = _fm.run_procurement_trial_phase(trial_selected_faction, _cur_cand, 4, trial_refinements);
                        trial_phase_results = trial_last_result;
                        trial_phase = 4;
                    }
                    scr_draw_snes_button(_col2_x + 14, _qk_btn_y, _col2_w - 28, 30, "[QUICK SIMULATE: RESOLVE ALL 4 PHASES INSTANTLY]", _qk_hov, false, c_gray);
                }
                // --- PHASE 2: DYNAMIC STRESS GAUNTLET ---
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
                    draw_text(_col2_x + 24, _p3_box_y + 40, "MATCHUP: " + _cur_cand.name + " (Vanguard PMC)  vs  " + _rc + " Champion");

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
                }
            }'''

new_lines = lines[:start_idx] + [new_arena_code + '\n'] + lines[end_idx:]
with open('objects/obj_HQTerminal/Draw_64.gml', 'w') as f:
    f.writelines(new_lines)

print("Updated objects/obj_HQTerminal/Draw_64.gml successfully")
