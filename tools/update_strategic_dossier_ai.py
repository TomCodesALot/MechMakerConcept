import re

fp = "objects/obj_HQTerminal/Draw_64.gml"
with open(fp, "r", encoding="utf-8") as f:
    text = f.read()

target_dossier = """            // 3. Right Column: Detailed Strategic Dossier & Action Console
            var _col2_x = _col1_x + _col1_w + 14;
            var _col2_y = _col1_y;
            var _col2_w = _dw - _col1_w - 14;
            var _doss_h = 226;

            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_col2_x, _col2_y, _col2_x + _col2_w, _col2_y + _doss_h, false);
            draw_set_color(make_color_rgb(30, 50, 75));
            draw_rectangle(_col2_x, _col2_y, _col2_x + _col2_w, _col2_y + _doss_h, true);

            var _cur_rel = _fm.diplomatic_relations[$ selected_diplo_pair];
            if (!is_undefined(_cur_rel)) {
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_col2_x + 14, _col2_y + 8, "STRATEGIC DOSSIER: " + _cur_rel.name_1 + " <---> " + _cur_rel.name_2);

                // Status & Metrics Row
                var _r_badge_col = (_cur_rel.state == "WAR") ? make_color_rgb(255, 60, 60) :
                                   ((_cur_rel.state == "ALLIANCE") ? make_color_rgb(0, 240, 255) :
                                   ((_cur_rel.state == "TRUCE") ? make_color_rgb(255, 200, 50) : make_color_rgb(200, 100, 255)));

                draw_set_color(_r_badge_col);
                draw_text(_col2_x + 14, _col2_y + 28, "Current Status: [" + _cur_rel.state + "]");

                draw_set_color(c_white);
                var _treaty_txt = (_cur_rel.treaty_turns_left > 0) ? (string(_cur_rel.treaty_turns_left) + " turns remaining") : "None";
                draw_text(_col2_x + 220, _col2_y + 28, "Treaty Countdown: " + _treaty_txt);
                draw_text(_col2_x + 460, _col2_y + 28, "Total Wars Fought: " + string(_cur_rel.total_wars_fought));

                // Casus Belli & Grievance
                draw_set_color(make_color_rgb(255, 220, 120));
                draw_text(_col2_x + 14, _col2_y + 50, "Casus Belli: " + _cur_rel.casus_belli);
                draw_set_color(make_color_rgb(180, 200, 220));
                draw_text_ext(_col2_x + 14, _col2_y + 70, "Historical Grievance: " + _cur_rel.historical_grievance, 18, _col2_w - 28);

                // Alliance Paranoia Advisory Box
                var _adv_y = _col2_y + 110;"""

replacement_dossier = """            // 3. Right Column: Detailed Strategic Dossier & Action Console
            var _col2_x = _col1_x + _col1_w + 14;
            var _col2_y = _col1_y;
            var _col2_w = _dw - _col1_w - 14;
            var _doss_h = 286;

            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_col2_x, _col2_y, _col2_x + _col2_w, _col2_y + _doss_h, false);
            draw_set_color(make_color_rgb(30, 50, 75));
            draw_rectangle(_col2_x, _col2_y, _col2_x + _col2_w, _col2_y + _doss_h, true);

            var _cur_rel = _fm.diplomatic_relations[$ selected_diplo_pair];
            if (!is_undefined(_cur_rel)) {
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_col2_x + 14, _col2_y + 8, "STRATEGIC DOSSIER: " + _cur_rel.name_1 + " <---> " + _cur_rel.name_2);

                // Status & Metrics Row
                var _r_badge_col = (_cur_rel.state == "WAR") ? make_color_rgb(255, 60, 60) :
                                   ((_cur_rel.state == "ALLIANCE") ? make_color_rgb(0, 240, 255) :
                                   ((_cur_rel.state == "TRUCE") ? make_color_rgb(255, 200, 50) : make_color_rgb(200, 100, 255)));

                draw_set_color(_r_badge_col);
                draw_text(_col2_x + 14, _col2_y + 26, "Current Status: [" + _cur_rel.state + "]");

                draw_set_color(c_white);
                var _treaty_txt = (_cur_rel.treaty_turns_left > 0) ? (string(_cur_rel.treaty_turns_left) + " turns remaining") : "None";
                draw_text(_col2_x + 220, _col2_y + 26, "Treaty Countdown: " + _treaty_txt);
                draw_text(_col2_x + 460, _col2_y + 26, "Total Wars Fought: " + string(_cur_rel.total_wars_fought));

                // Casus Belli & Grievance
                draw_set_color(make_color_rgb(255, 220, 120));
                draw_text(_col2_x + 14, _col2_y + 44, "Casus Belli: " + _cur_rel.casus_belli);
                draw_set_color(make_color_rgb(180, 200, 220));
                draw_text_ext(_col2_x + 14, _col2_y + 60, "Historical Grievance: " + _cur_rel.historical_grievance, 16, _col2_w - 28);

                // Faction AI Behavioral Intelligence Box (docs/36)
                var _f1 = _fm.factions[$ _cur_rel.faction_1];
                var _f2 = _fm.factions[$ _cur_rel.faction_2];
                if (!is_undefined(_f1) && !is_undefined(_f2)) {
                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_col2_x + 14, _col2_y + 94, "FACTION AI BRAIN & BEHAVIORAL INTELLIGENCE (docs/36):");

                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_col2_x + 14, _col2_y + 112, "* " + _f1.short_name + " [" + _f1.ai_state + "]: " + _f1.ai_behavior_title);
                    draw_set_color(make_color_rgb(190, 215, 240));
                    draw_text(_col2_x + 24, _col2_y + 128, "  Arch-Rival: " + string_upper(_f1.primary_enemy_id) + "  |  Preferred Ally: " + string_upper(_f1.preferred_ally_id) + "  |  Bounty Mult: " + string(_f1.contract_bounty_multiplier) + "x");

                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_col2_x + 14, _col2_y + 146, "* " + _f2.short_name + " [" + _f2.ai_state + "]: " + _f2.ai_behavior_title);
                    draw_set_color(make_color_rgb(190, 215, 240));
                    draw_text(_col2_x + 24, _col2_y + 162, "  Arch-Rival: " + string_upper(_f2.primary_enemy_id) + "  |  Preferred Ally: " + string_upper(_f2.preferred_ally_id) + "  |  Bounty Mult: " + string(_f2.contract_bounty_multiplier) + "x");
                }

                // Alliance Paranoia Advisory Box
                var _adv_y = _col2_y + 184;"""

assert target_dossier in text, "target_dossier not found"
text = text.replace(target_dossier, replacement_dossier, 1)

target_act_y = """                // Interactive PMC Mercenary Diplomacy Actions
                var _act_y = _col2_y + 162;"""

replacement_act_y = """                // Interactive PMC Mercenary Diplomacy Actions
                var _act_y = _col2_y + 232;"""

assert target_act_y in text, "target_act_y not found"
text = text.replace(target_act_y, replacement_act_y, 1)

with open(fp, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully updated objects/obj_HQTerminal/Draw_64.gml with AI Brain Strategic Dossier intelligence!")
