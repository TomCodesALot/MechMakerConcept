import re

with open('objects/obj_HQTerminal/Draw_64.gml', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Tab 2 Subtab 0: Faction Standing Meters (Line 3014)
old_tab2_factions = """            var _f_list = ["faction_a", "faction_b", "faction_c", "faction_d"];
            var _f_box_w = 280;
            for (var f = 0; f < 4; f++) {
                var _fid = _f_list[f];
                if (!variable_struct_exists(_fm.factions, _fid)) continue;
                var _finfo = _fm.factions[$ _fid];
                var _std = _fm.get_standing(_fid);
                var _fx = _cb_x + f * (_f_box_w + 14);"""

new_tab2_factions = """            var _f_list = ["faction_a", "faction_b", "faction_c", "faction_d", "faction_e", "faction_f"];
            var _f_box_w = 180;
            for (var f = 0; f < 6; f++) {
                var _fid = _f_list[f];
                if (!variable_struct_exists(_fm.factions, _fid)) continue;
                var _finfo = _fm.factions[$ _fid];
                var _std = _fm.get_standing(_fid);
                var _fx = _cb_x + f * (_f_box_w + 14);"""

assert old_tab2_factions in text, "Could not find old_tab2_factions"
text = text.replace(old_tab2_factions, new_tab2_factions, 1)

# Also handle name / short name and dormant display in Tab 2 boxes
old_box_texts = """                draw_set_color(make_color_rgb(240, 210, 100));
                draw_text(_fx + 10, _std_y + 6, _finfo.name);

                // AI Brain Status Tag
                var _ai_tag = "[PEACE]";
                var _ai_col = make_color_rgb(100, 220, 255);
                if (_is_desp) { _ai_tag = "[CRITICAL +100%]"; _ai_col = make_color_rgb(255, 60, 60); }
                else if (_is_win) { _ai_tag = "[DOMINANT]"; _ai_col = make_color_rgb(255, 215, 80); }
                else if (_is_war) { _ai_tag = "[WAR]"; _ai_col = make_color_rgb(255, 100, 100); }

                draw_set_color(_ai_col);
                draw_text(_fx + _f_box_w - string_width(_ai_tag) - 8, _std_y + 6, _ai_tag);

                var _std_col = (_std > 20) ? c_lime : ((_std < -10) ? c_red : make_color_rgb(240, 200, 80));
                draw_set_color(_std_col);
                draw_text(_fx + 10, _std_y + 23, "Standing: " + string(_std) + " (" + _finfo.standing_title + ")");

                draw_set_color(_is_desp ? make_color_rgb(255, 180, 180) : make_color_rgb(160, 190, 220));
                var _posture_txt = _is_desp ? "EMERGENCY: Double Payout Bailout Active!" : (_is_win ? "HEGEMONY: Market Tariffs Enforced" : ("Posture: " + string(_finfo[$ "ai_behavior_title"] ?? "Consolidation")));
                draw_text(_fx + 10, _std_y + 38, _posture_txt);"""

new_box_texts = """                var _is_dorm = (_finfo[$ "is_dormant"] ?? false);
                var _f_disp_name = _is_dorm ? "[SECTOR 0]" : _finfo.short_name;
                draw_set_color(_is_dorm ? make_color_rgb(255, 80, 80) : make_color_rgb(240, 210, 100));
                draw_text(_fx + 8, _std_y + 6, _f_disp_name);

                // AI Brain Status Tag
                var _ai_tag = _is_dorm ? "[DORMANT]" : "[PEACE]";
                var _ai_col = _is_dorm ? make_color_rgb(255, 80, 80) : make_color_rgb(100, 220, 255);
                if (!_is_dorm) {
                    if (_is_desp) { _ai_tag = "[CRIT +100%]"; _ai_col = make_color_rgb(255, 60, 60); }
                    else if (_is_win) { _ai_tag = "[DOMINANT]"; _ai_col = make_color_rgb(255, 215, 80); }
                    else if (_is_war) { _ai_tag = "[WAR]"; _ai_col = make_color_rgb(255, 100, 100); }
                }

                draw_set_color(_ai_col);
                draw_text(_fx + _f_box_w - string_width(_ai_tag) - 6, _std_y + 6, _ai_tag);

                var _std_col = _is_dorm ? make_color_rgb(180, 80, 80) : ((_std > 20) ? c_lime : ((_std < -10) ? c_red : make_color_rgb(240, 200, 80)));
                draw_set_color(_std_col);
                var _std_str = _is_dorm ? "Status: CLASSIFIED" : ("Standing: " + string(_std));
                draw_text(_fx + 8, _std_y + 23, _std_str);

                draw_set_color(_is_dorm ? make_color_rgb(200, 70, 70) : (_is_desp ? make_color_rgb(255, 180, 180) : make_color_rgb(160, 190, 220)));
                var _posture_txt = _is_dorm ? "Crypt Telemetry" : (_is_desp ? "+100% Bailout Active" : (_is_win ? "Tariffs Enforced" : (_finfo.short_name + " Posture")));
                draw_text(_fx + 8, _std_y + 38, _posture_txt);"""

assert old_box_texts in text, "Could not find old_box_texts"
text = text.replace(old_box_texts, new_box_texts, 1)

# 2. Update Mass Production: 6 Factions (Line 3158)
old_mp_loop = """            var _f_list = ["faction_a", "faction_b", "faction_c", "faction_d"];
            var _f_card_w = 280;
            var _f_card_h = 135;

            // 1. The 4 Target Faction Cards
            for (var fc = 0; fc < 4; fc++) {
                var _fid = _f_list[fc];
                if (!variable_struct_exists(_mpc, _fid)) continue;
                var _mp = _mpc[$ _fid];
                var _std = _fm.get_standing(_fid);
                var _card_x = _tr_x + fc * (_f_card_w + 13);"""

new_mp_loop = """            var _f_list = ["faction_a", "faction_b", "faction_c", "faction_d", "faction_e", "faction_f"];
            var _f_card_w = 180;
            var _f_card_h = 135;

            // 1. The 6 Target Faction Cards
            for (var fc = 0; fc < 6; fc++) {
                var _fid = _f_list[fc];
                if (!variable_struct_exists(_mpc, _fid)) continue;
                var _mp = _mpc[$ _fid];
                var _std = _fm.get_standing(_fid);
                var _card_x = _tr_x + fc * (_f_card_w + 14);"""

assert old_mp_loop in text, "Could not find old_mp_loop"
text = text.replace(old_mp_loop, new_mp_loop, 1)

# Also adjust text inside Mass Production card for 180px width
old_mp_card_text = """                draw_set_color(make_color_rgb(240, 215, 100));
                draw_text(_card_x + 10, _card_y + 8, _mp.faction_name);

                var _std_col = (_std >= 20) ? c_lime : ((_std < -10) ? c_red : c_yellow);
                draw_set_color(_std_col);
                draw_text(_card_x + 10, _card_y + 26, "Standing: " + string(_std));

                if (_mp.replaced) {
                    draw_set_color(make_color_rgb(60, 240, 120));
                    draw_text(_card_x + 10, _card_y + 46, "[DOCTRINE: " + _mp.replacement_name + "]");
                    draw_set_color(make_color_rgb(100, 255, 160));
                    draw_text(_card_x + 10, _card_y + 66, "Royalty: +" + string(_mp.royalty_per_turn) + " Cr/turn");
                    draw_text(_card_x + 10, _card_y + 84, "Total Earned: " + string(_mp.cumulative_royalties_paid) + " Cr");
                } else {
                    draw_set_color(make_color_rgb(240, 160, 50));
                    draw_text(_card_x + 10, _card_y + 46, "Incumbent: " + _mp.baseline_suit_name);
                    draw_set_color(make_color_rgb(80, 220, 255));
                    draw_text(_card_x + 10, _card_y + 66, "License Bounty: +" + string(_mp.licensing_bounty) + " Cr");
                    draw_text(_card_x + 10, _card_y + 84, "Daily Royalty: +" + string(_mp.royalty_per_turn) + " Cr/turn");
                }"""

new_mp_card_text = """                var _is_dorm = (_fm.factions[$ _fid][$ "is_dormant"] ?? false);
                var _card_title = _is_dorm ? "[SECTOR 0 CRYPT]" : (_fm.factions[$ _fid].short_name);
                draw_set_color(_is_dorm ? make_color_rgb(255, 80, 80) : make_color_rgb(240, 215, 100));
                draw_text(_card_x + 8, _card_y + 8, _card_title);

                var _std_col = _is_dorm ? make_color_rgb(180, 80, 80) : ((_std >= 20) ? c_lime : ((_std < -10) ? c_red : c_yellow));
                draw_set_color(_std_col);
                draw_text(_card_x + 8, _card_y + 26, _is_dorm ? "Standing: ???" : ("Standing: " + string(_std)));

                if (_is_dorm) {
                    draw_set_color(make_color_rgb(255, 60, 60));
                    draw_text(_card_x + 8, _card_y + 46, "Tender: LOCKED");
                    draw_set_color(make_color_rgb(180, 180, 180));
                    draw_text(_card_x + 8, _card_y + 66, "Sub-Basalt Silo");
                    draw_text(_card_x + 8, _card_y + 84, "Sister Ark 07");
                } else if (_mp.replaced) {
                    draw_set_color(make_color_rgb(60, 240, 120));
                    draw_text(_card_x + 8, _card_y + 46, "[DOCTRINE SET]");
                    draw_set_color(make_color_rgb(100, 255, 160));
                    draw_text(_card_x + 8, _card_y + 66, "Royalty: +" + string(_mp.royalty_per_turn) + " Cr");
                    draw_text(_card_x + 8, _card_y + 84, "Earned: " + string(_mp.cumulative_royalties_paid) + " Cr");
                } else {
                    draw_set_color(make_color_rgb(240, 160, 50));
                    draw_text(_card_x + 8, _card_y + 46, "Inc: " + _mp.baseline_suit_name);
                    draw_set_color(make_color_rgb(80, 220, 255));
                    draw_text(_card_x + 8, _card_y + 66, "Bounty: +" + string(_mp.licensing_bounty / 1000) + "k");
                    draw_text(_card_x + 8, _card_y + 84, "Royalty: +" + string(_mp.royalty_per_turn / 1000) + "k/t");
                }"""

assert old_mp_card_text in text, "Could not find old_mp_card_text"
text = text.replace(old_mp_card_text, new_mp_card_text, 1)

# 3. Update Faction Trade Exchange: 6 Factions (Line 3747)
old_trade_loop = """            var _f_list = ["faction_a", "faction_b", "faction_c", "faction_d"];
            var _f_tab_w = 280;

            // 1. Faction Partner Tabs
            for (var ft = 0; ft < 4; ft++) {
                var _fid = _f_list[ft];
                if (!variable_struct_exists(_fm.factions, _fid)) continue;
                var _finfo = _fm.factions[$ _fid];
                var _std = _fm.get_standing(_fid);
                var _ft_x = _td_x + ft * (_f_tab_w + 13);"""

new_trade_loop = """            var _f_list = ["faction_a", "faction_b", "faction_c", "faction_d", "faction_e", "faction_f"];
            var _f_tab_w = 180;

            // 1. Faction Partner Tabs (6 Factions)
            for (var ft = 0; ft < 6; ft++) {
                var _fid = _f_list[ft];
                if (!variable_struct_exists(_fm.factions, _fid)) continue;
                var _finfo = _fm.factions[$ _fid];
                var _std = _fm.get_standing(_fid);
                var _ft_x = _td_x + ft * (_f_tab_w + 14);"""

assert old_trade_loop in text, "Could not find old_trade_loop"
text = text.replace(old_trade_loop, new_trade_loop, 1)

# Also update title in trade tab
old_trade_tab_text = """                draw_set_color(make_color_rgb(240, 215, 100));
                draw_text(_ft_x + 10, _ft_y + 6, _finfo.name);

                var _trade_status = (_std >= 30) ? "ALLY (-15% BUY / +15% SELL)" : ((_std < 0) ? "TARIFF (+25% EMBARGO)" : "STANDARD (PARITY)");
                var _ts_col = (_std >= 30) ? c_lime : ((_std < 0) ? c_red : c_yellow);
                draw_set_color(_ts_col);
                draw_text(_ft_x + 10, _ft_y + 26, "Standing " + string(_std) + ": " + _trade_status);"""

new_trade_tab_text = """                var _is_dorm = (_finfo[$ "is_dormant"] ?? false);
                draw_set_color(_is_dorm ? make_color_rgb(255, 80, 80) : make_color_rgb(240, 215, 100));
                draw_text(_ft_x + 8, _ft_y + 6, _is_dorm ? "[SECTOR 0]" : _finfo.short_name);

                var _trade_status = _is_dorm ? "DORMANT CRYPT" : ((_std >= 30) ? "ALLY (-15%)" : ((_std < 0) ? "TARIFF (+25%)" : "PARITY"));
                var _ts_col = _is_dorm ? make_color_rgb(180, 80, 80) : ((_std >= 30) ? c_lime : ((_std < 0) ? c_red : c_yellow));
                draw_set_color(_ts_col);
                draw_text(_ft_x + 8, _ft_y + 26, _is_dorm ? "Classified Hub" : ("Std " + string(_std) + ": " + _trade_status));"""

assert old_trade_tab_text in text, "Could not find old_trade_tab_text"
text = text.replace(old_trade_tab_text, new_trade_tab_text, 1)

# 4. Update Tab 3 Subtab 2: Bilateral Relations (Line 4874)
old_pairs_block = """            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_col1_x + 12, _col1_y + 8, "BILATERAL RELATIONS MATRIX (6 PAIRS):");

            var _pairs = [
                "terran_colony",
                "terran_syndicate",
                "terran_zaibatsu",
                "colony_syndicate",
                "colony_zaibatsu",
                "syndicate_zaibatsu"
            ];

            var _card_y_start = _col1_y + 30;
            var _card_h = 68;

            for (var _pair_i = 0; _pair_i < 6; _pair_i++) {
                var _pid = _pairs[_pair_i];
                var _rel = _fm.diplomatic_relations[$ _pid];
                if (is_undefined(_rel)) continue;

                var _cy = _card_y_start + _pair_i * (_card_h + 6);
                var _is_sel = (selected_diplo_pair == _pid);
                var _c_hov = (_mx >= _col1_x + 8 && _mx <= _col1_x + _col1_w - 8 && _my >= _cy && _my <= _cy + _card_h);
                if (_c_hov && _click) selected_diplo_pair = _pid;

                // Card background
                draw_set_color(_is_sel ? make_color_rgb(25, 48, 76) : (_c_hov ? make_color_rgb(18, 30, 46) : make_color_rgb(13, 20, 30)));
                draw_rectangle(_col1_x + 8, _cy, _col1_x + _col1_w - 8, _cy + _card_h, false);

                // State badge color
                var _st_col = make_color_rgb(150, 180, 220); // NON_AGGRESSION
                if (_rel.state == "WAR") _st_col = make_color_rgb(255, 60, 60);
                else if (_rel.state == "COLD_WAR") _st_col = make_color_rgb(200, 100, 255);
                else if (_rel.state == "TRUCE") _st_col = make_color_rgb(255, 200, 50);
                else if (_rel.state == "ALLIANCE") _st_col = make_color_rgb(0, 240, 255);

                draw_set_color(_is_sel ? make_color_rgb(100, 220, 255) : make_color_rgb(35, 55, 80));
                draw_rectangle(_col1_x + 8, _cy, _col1_x + _col1_w - 8, _cy + _card_h, true);

                // Pair names
                draw_set_color(c_white);
                draw_text(_col1_x + 16, _cy + 5, _rel.name_1 + " vs " + _rel.name_2);

                // State badge
                var _badge_str = "[" + _rel.state + "]";
                if (_rel.treaty_turns_left > 0) _badge_str += " (" + string(_rel.treaty_turns_left) + "T)";
                draw_set_color(_st_col);
                draw_text(_col1_x + _col1_w - 16 - string_width(_badge_str), _cy + 5, _badge_str);

                // Tension bar
                var _bar_x = _col1_x + 16;
                var _bar_y = _cy + 27;
                var _bar_w = _col1_w - 32;
                var _bar_h = 10;
                draw_set_color(make_color_rgb(20, 28, 38));
                draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_w, _bar_y + _bar_h, false);

                var _ten_w = (_bar_w * (_rel.tension / 100.0));
                var _ten_col = (_rel.tension >= 75) ? make_color_rgb(255, 60, 60) :
                               ((_rel.tension >= 50) ? make_color_rgb(255, 170, 40) : make_color_rgb(80, 220, 120));
                draw_set_color(_ten_col);
                draw_rectangle(_bar_x, _bar_y, _bar_x + _ten_w, _bar_y + _bar_h, false);

                // Tension value and drift note
                var _drift_lbl = "";
                if (_rel.state == "ALLIANCE") _drift_lbl = "+2.5/T Paranoia";
                else if (_rel.state == "TRUCE") _drift_lbl = "-2.0/T Truce Decay";
                else if (_rel.state == "COLD_WAR") _drift_lbl = "+" + string(_rel.base_friction) + "/T Friction";"""

new_pairs_block = """            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_col1_x + 12, _col1_y + 8, "BILATERAL RELATIONS MATRIX (12 PAIRS):");

            var _pairs = [
                "terran_colony",
                "terran_syndicate",
                "terran_zaibatsu",
                "colony_syndicate",
                "colony_zaibatsu",
                "syndicate_zaibatsu",
                "terran_astran",
                "colony_astran",
                "syndicate_astran",
                "zaibatsu_astran",
                "terran_martian",
                "zaibatsu_martian"
            ];

            var _card_y_start = _col1_y + 26;
            var _card_h = 42;

            for (var _pair_i = 0; _pair_i < array_length(_pairs); _pair_i++) {
                var _pid = _pairs[_pair_i];
                var _rel = _fm.diplomatic_relations[$ _pid];
                if (is_undefined(_rel)) continue;

                var _cy = _card_y_start + _pair_i * (_card_h + 4);
                var _is_sel = (selected_diplo_pair == _pid);
                var _c_hov = (_mx >= _col1_x + 8 && _mx <= _col1_x + _col1_w - 8 && _my >= _cy && _my <= _cy + _card_h);
                if (_c_hov && _click) selected_diplo_pair = _pid;

                // Card background
                draw_set_color(_is_sel ? make_color_rgb(25, 48, 76) : (_c_hov ? make_color_rgb(18, 30, 46) : make_color_rgb(13, 20, 30)));
                draw_rectangle(_col1_x + 8, _cy, _col1_x + _col1_w - 8, _cy + _card_h, false);

                // State badge color
                var _st_col = make_color_rgb(150, 180, 220); // NON_AGGRESSION
                if (_rel.state == "WAR") _st_col = make_color_rgb(255, 60, 60);
                else if (_rel.state == "COLD_WAR") _st_col = make_color_rgb(200, 100, 255);
                else if (_rel.state == "TRUCE") _st_col = make_color_rgb(255, 200, 50);
                else if (_rel.state == "ALLIANCE") _st_col = make_color_rgb(0, 240, 255);

                draw_set_color(_is_sel ? make_color_rgb(100, 220, 255) : make_color_rgb(35, 55, 80));
                draw_rectangle(_col1_x + 8, _cy, _col1_x + _col1_w - 8, _cy + _card_h, true);

                // Pair names (compact)
                draw_set_color(c_white);
                var _p_name1 = (_fm.factions[$ _rel.faction_1][$ "short_name"] ?? _rel.name_1);
                var _p_name2 = (_fm.factions[$ _rel.faction_2][$ "short_name"] ?? _rel.name_2);
                draw_text(_col1_x + 14, _cy + 4, _p_name1 + " vs " + _p_name2);

                // State badge
                var _badge_str = "[" + _rel.state + "]";
                if (_rel.treaty_turns_left > 0) _badge_str += " (" + string(_rel.treaty_turns_left) + "T)";
                draw_set_color(_st_col);
                draw_text(_col1_x + _col1_w - 14 - string_width(_badge_str), _cy + 4, _badge_str);

                // Tension bar
                var _bar_x = _col1_x + 14;
                var _bar_y = _cy + 22;
                var _bar_w = _col1_w - 28;
                var _bar_h = 7;
                draw_set_color(make_color_rgb(20, 28, 38));
                draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_w, _bar_y + _bar_h, false);

                var _ten_w = (_bar_w * (_rel.tension / 100.0));
                var _ten_col = (_rel.tension >= 75) ? make_color_rgb(255, 60, 60) :
                               ((_rel.tension >= 50) ? make_color_rgb(255, 170, 40) : make_color_rgb(80, 220, 120));
                draw_set_color(_ten_col);
                draw_rectangle(_bar_x, _bar_y, _bar_x + _ten_w, _bar_y + _bar_h, false);

                // Tension value and drift note
                var _drift_lbl = "";
                if (_rel.state == "ALLIANCE") _drift_lbl = "+2.5/T Paranoia";
                else if (_rel.state == "TRUCE") _drift_lbl = "-2.0/T Truce";
                else if (_rel.state == "COLD_WAR") _drift_lbl = "+" + string(_rel.base_friction) + "/T Friction";
                else if (_rel.state == "WAR") _drift_lbl = "Active War (" + string(_rel.war_duration_turns) + "T)";"""

assert old_pairs_block in text, "Could not find old_pairs_block"
text = text.replace(old_pairs_block, new_pairs_block, 1)

with open('objects/obj_HQTerminal/Draw_64.gml', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated objects/obj_HQTerminal/Draw_64.gml!")
