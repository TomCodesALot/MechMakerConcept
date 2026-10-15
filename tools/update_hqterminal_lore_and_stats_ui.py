import re
import os

fp = "objects/obj_HQTerminal/Draw_64.gml"
with open(fp, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update Column 1 list item to display adoption status badge
target_c1 = """            draw_set_color(_i_sel ? c_white : make_color_rgb(220, 220, 220));
            draw_text(_col1_x + 16, _iy + 8, _code + " // " + _iname);
            draw_set_color(make_color_rgb(100, 200, 255));
            draw_text(_col1_x + 16, _iy + 28, _sub);"""

replacement_c1 = """            draw_set_color(_i_sel ? c_white : make_color_rgb(220, 220, 220));
            draw_text(_col1_x + 16, _iy + 8, _code + " // " + _iname);
            draw_set_color(make_color_rgb(100, 200, 255));
            draw_text(_col1_x + 16, _iy + 28, _sub);

            var _astat = _item[$ "adoption_status"] ?? "standard_issue";
            var _stat_tag = "[STD]";
            var _stat_col = make_color_rgb(100, 220, 255);
            if (_astat == "adopted") { _stat_tag = "[ADOPTED]"; _stat_col = make_color_rgb(255, 215, 80); }
            else if (_astat == "replaced_by_player") { _stat_tag = "[PMC-REP]"; _stat_col = make_color_rgb(80, 255, 120); }
            else if (_astat == "replaced_by_competitor") { _stat_tag = "[CORP-REP]"; _stat_col = make_color_rgb(255, 140, 60); }
            else if (_astat == "contested") { _stat_tag = "[PMC]"; _stat_col = make_color_rgb(255, 240, 100); }
            else if (_astat == "phased_out") { _stat_tag = "[PHASED]"; _stat_col = make_color_rgb(140, 140, 140); }
            else if (_astat == "ace_custom") { _stat_tag = "[ACE]"; _stat_col = make_color_rgb(220, 150, 255); }

            draw_set_color(_stat_col);
            draw_text(_col1_x + _col1_w - 96, _iy + 28, _stat_tag);"""

assert target_c1 in text, "target_c1 not found in Draw_64.gml"
text = text.replace(target_c1, replacement_c1, 1)

# 2. Update Column 3 Right Panel with 3 Subtabs: Specs, Global Stats, Lore & Chronicle
target_c3 = """            // Core Technical Specs
            draw_set_color(c_white);
            draw_text(_rx, _ry + 48, "* Armor Rating: " + string(_active_suit[$ "armor_rating"] ?? 850) + " HP");
            draw_text(_rx, _ry + 68, "* Structure HP: " + string(_active_suit[$ "structure_hp"] ?? 2000) + " HP");
            draw_text(_rx, _ry + 88, "* Reactor Output: " + string(_active_suit[$ "power_output_mw"] ?? 1200) + " MW (" + string(_active_suit[$ "reactor_type"] ?? "Fusion Core") + ")");
            draw_text(_rx, _ry + 108, "* Mobility: Walk " + string(_active_suit[$ "walk_speed_kph"] ?? 40) + " km/h | Boost " + string(_active_suit[$ "boost_speed_kph"] ?? 80) + " km/h");
            draw_text(_rx, _ry + 128, "* Dimensions: Height " + string(_active_suit[$ "height_meters"] ?? 18.0) + "m | Weight " + string(_active_suit[$ "combat_weight_tonnes"] ?? 85.0) + "t");

            // Gihren's Greed & Front Mission Hybrid Telemetry (Doc 20)
            var _c_stats = undefined;
            if (instance_exists(obj_BlueprintManager)) {
                _c_stats = obj_BlueprintManager.get_comprehensive_stats(_active_suit);
            }
            if (!is_undefined(_c_stats)) {
                draw_set_color(make_color_rgb(255, 215, 80));
                draw_text(_rx, _ry + 148, "* Pilot Limit (Genkai): " + string(_c_stats.pilot_limit_pct) + "% | Propellant: " + string(_c_stats.propellant_max) + " EN");
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_rx, _ry + 168, "* Terrains: G:" + _c_stats.terrain.ground + " S:" + _c_stats.terrain.space + " U:" + _c_stats.terrain.urban + " T:" + _c_stats.terrain.trench + " | ECM: " + string(_c_stats.ecm_dispersion_pct) + "% | Search: " + _c_stats.sensor_search_grade);
            }

            // Equipped Weapons
            var _arms_y = _ry + 195;
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_rx, _arms_y, "ARMAMENT LOADOUT:");
            var _arms = _active_suit[$ "armament"] ?? ["Autocannon", "Vulcan"];
            if (is_array(_arms)) {
                for (var w = 0; w < min(3, array_length(_arms)); w++) {
                    draw_set_color(c_white);
                    draw_text(_rx + 10, _arms_y + 20 + w * 18, "> " + string(_arms[w]));
                }
            }

            // Production Variants Directory
            var _var_y = _arms_y + 82;
            draw_set_color(make_color_rgb(240, 210, 100));
            draw_text(_rx, _var_y, "PRODUCTION VARIANTS & DOCTRINES:");
            var _vars = _active_suit[$ "variants"] ?? ["Standard Production", "Ace Refit"];
            if (is_array(_vars)) {
                for (var v = 0; v < min(4, array_length(_vars)); v++) {
                    draw_set_color(make_color_rgb(180, 210, 240));
                    draw_text(_rx + 10, _var_y + 20 + v * 18, "[+] " + string(_vars[v]));
                }
            }

            // Lore Dossier
            var _lore_y = _var_y + 100;
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_rx, _lore_y, "MANUFACTURING LORE & REPUTATION:");
            draw_set_color(make_color_rgb(190, 205, 220));
            draw_text_ext(_rx, _lore_y + 20, string(_active_suit[$ "manufacturing_lore"] ?? "Classified defense project."), 16, _col3_w - 32);"""

replacement_c3 = """            // Column 3 Dossier Subtabs (Specs vs Global Stats vs Lore/Chronicle)
            var _dsub_names = ["[1. SPECS & WEAPONS]", "[2. GLOBAL STATS & ATTRITION]", "[3. HISTORICAL & DYNAMIC LORE]"];
            var _dsub_w = (_col3_w - 32) / 3;
            var _dsub_y = _ry + 42;
            for (var ds = 0; ds < 3; ds++) {
                var _dsx = _rx + ds * _dsub_w;
                var _ds_active = (bp_archive_dossier_tab == ds);
                var _ds_hov = (_mx >= _dsx && _mx <= _dsx + _dsub_w - 4 && _my >= _dsub_y && _my <= _dsub_y + 24);
                if (_ds_hov && _click) { bp_archive_dossier_tab = ds; scr_audio_play_ui("click"); }

                draw_set_color(_ds_active ? make_color_rgb(30, 65, 105) : (_ds_hov ? make_color_rgb(18, 38, 60) : make_color_rgb(12, 18, 26)));
                draw_rectangle(_dsx, _dsub_y, _dsx + _dsub_w - 4, _dsub_y + 24, false);
                draw_set_color(_ds_active ? make_color_rgb(100, 220, 255) : make_color_rgb(40, 70, 100));
                draw_rectangle(_dsx, _dsub_y, _dsx + _dsub_w - 4, _dsub_y + 24, true);
                draw_set_color(_ds_active ? c_white : make_color_rgb(150, 180, 210));
                draw_text(_dsx + 6, _dsub_y + 4, _dsub_names[ds]);
            }

            var _content_y = _dsub_y + 32;

            // =================================================================
            // TAB 0: CORE TECHNICAL SPECS & WEAPON LOADOUT
            // =================================================================
            if (bp_archive_dossier_tab == 0) {
                draw_set_color(c_white);
                draw_text(_rx, _content_y, "* Armor Rating: " + string(_active_suit[$ "armor_rating"] ?? 850) + " HP");
                draw_text(_rx, _content_y + 20, "* Structure HP: " + string(_active_suit[$ "structure_hp"] ?? 2000) + " HP");
                draw_text(_rx, _content_y + 40, "* Reactor Output: " + string(_active_suit[$ "power_output_mw"] ?? 1200) + " MW (" + string(_active_suit[$ "reactor_type"] ?? "Fusion Core") + ")");
                draw_text(_rx, _content_y + 60, "* Mobility: Walk " + string(_active_suit[$ "walk_speed_kph"] ?? 40) + " km/h | Boost " + string(_active_suit[$ "boost_speed_kph"] ?? 80) + " km/h");
                draw_text(_rx, _content_y + 80, "* Dimensions: Height " + string(_active_suit[$ "height_meters"] ?? 18.0) + "m | Weight " + string(_active_suit[$ "combat_weight_tonnes"] ?? 85.0) + "t");

                var _c_stats = undefined;
                if (instance_exists(obj_BlueprintManager)) {
                    _c_stats = obj_BlueprintManager.get_comprehensive_stats(_active_suit);
                }
                if (!is_undefined(_c_stats)) {
                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_rx, _content_y + 104, "* Pilot Limit (Genkai): " + string(_c_stats.pilot_limit_pct) + "% | Propellant: " + string(_c_stats.propellant_max) + " EN");
                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_rx, _content_y + 124, "* Terrains: G:" + _c_stats.terrain.ground + " S:" + _c_stats.terrain.space + " U:" + _c_stats.terrain.urban + " T:" + _c_stats.terrain.trench + " | ECM: " + string(_c_stats.ecm_dispersion_pct) + "%");
                }

                var _arms_y = _content_y + 150;
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_rx, _arms_y, "ARMAMENT LOADOUT:");
                var _arms = _active_suit[$ "armament"] ?? ["Autocannon", "Vulcan"];
                if (is_array(_arms)) {
                    for (var w = 0; w < min(3, array_length(_arms)); w++) {
                        draw_set_color(c_white);
                        draw_text(_rx + 10, _arms_y + 20 + w * 18, "> " + string(_arms[w]));
                    }
                }

                var _var_y = _arms_y + 84;
                draw_set_color(make_color_rgb(240, 210, 100));
                draw_text(_rx, _var_y, "PRODUCTION VARIANTS & DOCTRINES:");
                var _vars = _active_suit[$ "variants"] ?? ["Standard Production", "Ace Refit"];
                if (is_array(_vars)) {
                    for (var v = 0; v < min(4, array_length(_vars)); v++) {
                        draw_set_color(make_color_rgb(180, 210, 240));
                        draw_text(_rx + 10, _var_y + 20 + v * 18, "[+] " + string(_vars[v]));
                    }
                }
            }
            // =================================================================
            // TAB 1: GLOBAL PRODUCTION NUMBERS & ATTRITION TELEMETRY
            // =================================================================
            else if (bp_archive_dossier_tab == 1) {
                draw_set_color(make_color_rgb(255, 215, 80));
                draw_text(_rx, _content_y, "GLOBAL PRODUCTION & COMBAT SERVICE METRICS (SOL REGISTRY):");

                var _prod_num = _active_suit[$ "production_count"] ?? 3200;
                var _act_num = _active_suit[$ "active_units"] ?? 2100;
                var _cas_num = _active_suit[$ "casualty_count"] ?? 1100;
                var _kill_num = _active_suit[$ "kill_count"] ?? 1850;
                var _ratio = _active_suit[$ "combat_loss_ratio"] ?? 0.59;
                var _surv = _active_suit[$ "survivability_rating"] ?? 63;

                draw_set_color(c_white);
                draw_text(_rx, _content_y + 24, "* Total Units Manufactured: " + string(_prod_num) + " Units System-Wide");
                draw_text(_rx, _content_y + 44, "* Active in Frontline Service: " + string(_act_num) + " Operational Hulls");
                draw_text(_rx, _content_y + 64, "* Confirmed Combat Losses: " + string(_cas_num) + " Neutralized Hulls");
                draw_text(_rx, _content_y + 84, "* Confirmed Enemy Kills: " + string(_kill_num) + " Neutralized Targets");
                draw_text(_rx, _content_y + 104, "* Combat Loss / Kill Ratio: " + string(_ratio));

                // Survivability Meter Bar
                draw_text(_rx, _content_y + 128, "* Frontline Survivability Rating: " + string(_surv) + "%");
                var _bar_x = _rx + 290;
                var _bar_y = _content_y + 130;
                var _bar_w = 260;
                var _bar_h = 12;
                draw_set_color(make_color_rgb(20, 30, 40));
                draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_w, _bar_y + _bar_h, false);
                var _fill_w = (_surv / 100.0) * _bar_w;
                var _surv_col = (_surv >= 65) ? make_color_rgb(80, 240, 120) : ((_surv >= 45) ? make_color_rgb(255, 200, 60) : make_color_rgb(255, 80, 80));
                draw_set_color(_surv_col);
                draw_rectangle(_bar_x, _bar_y, _bar_x + _fill_w, _bar_y + _bar_h, false);
                draw_set_color(make_color_rgb(80, 120, 160));
                draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_w, _bar_y + _bar_h, true);

                // Military Procurement & Adoption State Banner
                var _ban_y = _content_y + 158;
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_rx, _ban_y, "MILITARY PROCUREMENT & ADOPTION STATUS:");

                var _astat = _active_suit[$ "adoption_status"] ?? "standard_issue";
                var _rep_by = _active_suit[$ "replaced_by"] ?? "";
                var _status_box_y = _ban_y + 22;

                var _s_col = make_color_rgb(14, 28, 42);
                var _s_border = make_color_rgb(40, 90, 140);
                var _s_title = "[STANDARD ISSUE DOCTRINE]";
                var _s_desc = "Primary active frontline warframe deployed across regular standing army garrisons.";

                if (_astat == "adopted") {
                    _s_col = make_color_rgb(36, 32, 12);
                    _s_border = make_color_rgb(240, 200, 60);
                    _s_title = "[★ PROCUREMENT TENDER ADOPTED ★]";
                    _s_desc = "Selected as premier doctrinal contract winner! Priority factory lines active.";
                } else if (_astat == "replaced_by_player") {
                    _s_col = make_color_rgb(14, 38, 22);
                    _s_border = make_color_rgb(80, 240, 120);
                    _s_title = "[! REPLACED BY PMC DREADNOUGHT BLUEPRINT !]";
                    _s_desc = "Official procurement canceled. Tooling converted to Player Model: '" + (_rep_by != "" ? _rep_by : "PMC Vanguard") + "'.";
                } else if (_astat == "replaced_by_competitor") {
                    _s_col = make_color_rgb(38, 18, 14);
                    _s_border = make_color_rgb(255, 120, 60);
                    _s_title = "[! REPLACED BY COMPETITOR R&D LINE !]";
                    _s_desc = "Phased out in favor of rival corporation: '" + (_rep_by != "" ? _rep_by : "Rival Model") + "'. Relegated to scrap reserves.";
                } else if (_astat == "contested") {
                    _s_col = make_color_rgb(30, 28, 14);
                    _s_border = make_color_rgb(255, 230, 90);
                    _s_title = "[CONTESTED PROTOTYPE TENDER]";
                    _s_desc = "Proprietary mercenary blueprint actively competing in Sol procurement fly-offs.";
                } else if (_astat == "phased_out") {
                    _s_col = make_color_rgb(18, 20, 24);
                    _s_border = make_color_rgb(120, 130, 140);
                    _s_title = "[PHASED OUT TO RESERVES]";
                    _s_desc = "Decommissioned from primary line service; maintained only by planetary militias.";
                }

                draw_set_color(_s_col);
                draw_rectangle(_rx, _status_box_y, _rx + _col3_w - 32, _status_box_y + 54, false);
                draw_set_color(_s_border);
                draw_rectangle(_rx, _status_box_y, _rx + _col3_w - 32, _status_box_y + 54, true);

                draw_set_color(_s_border);
                draw_text(_rx + 12, _status_box_y + 8, _s_title);
                draw_set_color(make_color_rgb(210, 225, 240));
                draw_text(_rx + 12, _status_box_y + 28, _s_desc);

                // Primary Operational Theaters
                var _th_y = _status_box_y + 68;
                draw_set_color(make_color_rgb(240, 210, 100));
                draw_text(_rx, _th_y, "PRIMARY DEPLOYMENT THEATERS:");
                var _theaters = _active_suit[$ "primary_theaters"] ?? ["Baikal Redoubt", "Low Earth Orbit Fortress"];
                if (is_array(_theaters)) {
                    for (var th = 0; th < array_length(_theaters); th++) {
                        draw_set_color(make_color_rgb(180, 210, 240));
                        draw_text(_rx + 12, _th_y + 20 + th * 18, "> " + string(_theaters[th]));
                    }
                }
            }
            // =================================================================
            // TAB 2: HISTORICAL DOSSIER & DYNAMIC PLAYTHROUGH CHRONICLE
            // =================================================================
            else if (bp_archive_dossier_tab == 2) {
                // Historical Development Dossier
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_rx, _content_y, "HISTORICAL DEVELOPMENT & TENDER ORIGIN:");
                draw_set_color(make_color_rgb(200, 215, 230));
                var _hlore = _active_suit[$ "historical_lore"] ?? (_active_suit[$ "manufacturing_lore"] ?? "Classified defense project.");
                draw_text_ext(_rx, _content_y + 20, _hlore, 16, _col3_w - 32);

                // Manufacturing Quirks
                var _q_y = _content_y + 115;
                draw_set_color(make_color_rgb(255, 200, 80));
                draw_text(_rx, _q_y, "MANUFACTURING QUIRKS & MAINTENANCE QUOTIDIAN:");
                draw_set_color(make_color_rgb(190, 205, 220));
                var _quirks = _active_suit[$ "manufacturing_quirks"] ?? "Standard factory tolerances.";
                draw_text_ext(_rx, _q_y + 20, _quirks, 16, _col3_w - 32);

                // Battlefield Reputation
                var _rep_y = _q_y + 68;
                draw_set_color(make_color_rgb(255, 140, 60));
                draw_text(_rx, _rep_y, "PILOT COCKPIT REPUTATION & SLANG:");
                draw_set_color(make_color_rgb(190, 205, 220));
                var _rep = _active_suit[$ "battlefield_reputation"] ?? "Known as reliable military hardware.";
                draw_text_ext(_rx, _rep_y + 20, _rep, 16, _col3_w - 32);

                // Dynamic Playthrough Service Chronicle
                var _chr_y = _rep_y + 68;
                draw_set_color(make_color_rgb(80, 255, 140));
                draw_text(_rx, _chr_y, "DYNAMIC SERVICE CHRONICLE (PLAYTHROUGH LOG):");

                var _chr_box_y = _chr_y + 20;
                var _chr_box_h = 92;
                draw_set_color(make_color_rgb(10, 16, 24));
                draw_rectangle(_rx, _chr_box_y, _rx + _col3_w - 32, _chr_box_y + _chr_box_h, false);
                draw_set_color(make_color_rgb(35, 65, 95));
                draw_rectangle(_rx, _chr_box_y, _rx + _col3_w - 32, _chr_box_y + _chr_box_h, true);

                var _chron = _active_suit[$ "dynamic_lore_chronicle"] ?? ["[Cycle 1] Commissioned into active fleet service."];
                if (is_array(_chron)) {
                    var _max_chr_vis = 3;
                    var _chr_len = array_length(_chron);
                    bp_archive_chronicle_scroll = clamp(bp_archive_chronicle_scroll, 0, max(0, _chr_len - _max_chr_vis));

                    for (var ci = 0; ci < min(_max_chr_vis, _chr_len); ci++) {
                        var _c_idx = ci + bp_archive_chronicle_scroll;
                        if (_c_idx >= _chr_len) break;
                        var _centry = _chron[_c_idx];
                        draw_set_color(make_color_rgb(180, 230, 255));
                        draw_text_ext(_rx + 10, _chr_box_y + 8 + ci * 28, "[*] " + string(_centry), 14, _col3_w - 52);
                    }

                    if (_chr_len > _max_chr_vis) {
                        var _c_prev_hov = (_mx >= _rx + _col3_w - 130 && _mx <= _rx + _col3_w - 85 && _my >= _chr_y && _my <= _chr_y + 18);
                        var _c_next_hov = (_mx >= _rx + _col3_w - 80 && _mx <= _rx + _col3_w - 35 && _my >= _chr_y && _my <= _chr_y + 18);
                        if (_c_prev_hov && _click && bp_archive_chronicle_scroll > 0) bp_archive_chronicle_scroll--;
                        if (_c_next_hov && _click && bp_archive_chronicle_scroll + _max_chr_vis < _chr_len) bp_archive_chronicle_scroll++;

                        draw_set_color(_c_prev_hov ? make_color_rgb(60, 120, 180) : make_color_rgb(25, 45, 65));
                        draw_rectangle(_rx + _col3_w - 130, _chr_y, _rx + _col3_w - 85, _chr_y + 18, false);
                        draw_set_color(c_white);
                        draw_text(_rx + _col3_w - 125, _chr_y + 2, "< PREV");

                        draw_set_color(_c_next_hov ? make_color_rgb(60, 120, 180) : make_color_rgb(25, 45, 65));
                        draw_rectangle(_rx + _col3_w - 80, _chr_y, _rx + _col3_w - 35, _chr_y + 18, false);
                        draw_set_color(c_white);
                        draw_text(_rx + _col3_w - 75, _chr_y + 2, "NEXT >");
                    }
                }
            }"""

assert target_c3 in text, "target_c3 not found in Draw_64.gml"
text = text.replace(target_c3, replacement_c3, 1)

with open(fp, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully updated objects/obj_HQTerminal/Draw_64.gml with 3-tab Dossier & dynamic chronicle!")
