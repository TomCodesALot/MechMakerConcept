with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
    code = f.read()

replacements = [
    # 1. Strategic relations dossier & AI intelligence box (lines 5065-5115)
    (
'''            var _cur_rel = variable_struct_get(_fm.diplomatic_relations, selected_diplo_pair);
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
                var _f1 = variable_struct_get(_fm.factions, _cur_rel.faction_1);
                var _f2 = variable_struct_get(_fm.factions, _cur_rel.faction_2);
                if (!is_undefined(_f1) && !is_undefined(_f2)) {
                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_col2_x + 14, _col2_y + 94, "FACTION AI BRAIN & BEHAVIORAL INTELLIGENCE:");

                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_col2_x + 14, _col2_y + 112, "* " + _f1.short_name + " [" + _f1.ai_state + "]: " + _f1.ai_behavior_title);
                    draw_set_color(make_color_rgb(190, 215, 240));
                    draw_text(_col2_x + 24, _col2_y + 128, "  Arch-Rival: " + string_upper(_f1.primary_enemy_id) + "  |  Preferred Ally: " + string_upper(_f1.preferred_ally_id) + "  |  Bounty Mult: " + string(_f1.contract_bounty_multiplier) + "x");

                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_col2_x + 14, _col2_y + 146, "* " + _f2.short_name + " [" + _f2.ai_state + "]: " + _f2.ai_behavior_title);
                    draw_set_color(make_color_rgb(190, 215, 240));
                    draw_text(_col2_x + 24, _col2_y + 162, "  Arch-Rival: " + string_upper(_f2.primary_enemy_id) + "  |  Preferred Ally: " + string_upper(_f2.preferred_ally_id) + "  |  Bounty Mult: " + string(_f2.contract_bounty_multiplier) + "x");
                }''',
'''            var _cur_rel = variable_struct_get(_fm.diplomatic_relations, selected_diplo_pair);
            if (!is_undefined(_cur_rel)) {
                var _cr_name1 = string(_cur_rel.name_1 ?? "Faction 1");
                var _cr_name2 = string(_cur_rel.name_2 ?? "Faction 2");
                var _cr_state = string(_cur_rel.state ?? "COLD_WAR");
                var _cr_cb = string(_cur_rel.casus_belli ?? "Territorial friction");
                var _cr_hg = string(_cur_rel.historical_grievance ?? "Border dispute");

                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_col2_x + 14, _col2_y + 8, "STRATEGIC DOSSIER: " + _cr_name1 + " <---> " + _cr_name2);

                // Status & Metrics Row
                var _r_badge_col = (_cr_state == "WAR") ? make_color_rgb(255, 60, 60) :
                                   ((_cr_state == "ALLIANCE") ? make_color_rgb(0, 240, 255) :
                                   ((_cr_state == "TRUCE") ? make_color_rgb(255, 200, 50) : make_color_rgb(200, 100, 255)));

                draw_set_color(_r_badge_col);
                draw_text(_col2_x + 14, _col2_y + 26, "Current Status: [" + _cr_state + "]");

                draw_set_color(c_white);
                var _ttl = variable_struct_get(_cur_rel, "treaty_turns_left") ?? 0;
                var _treaty_txt = (_ttl > 0) ? (string(_ttl) + " turns remaining") : "None";
                draw_text(_col2_x + 220, _col2_y + 26, "Treaty Countdown: " + _treaty_txt);
                var _twf = variable_struct_get(_cur_rel, "total_wars_fought") ?? 0;
                draw_text(_col2_x + 460, _col2_y + 26, "Total Wars Fought: " + string(_twf));

                // Casus Belli & Grievance
                draw_set_color(make_color_rgb(255, 220, 120));
                draw_text(_col2_x + 14, _col2_y + 44, "Casus Belli: " + _cr_cb);
                draw_set_color(make_color_rgb(180, 200, 220));
                draw_text_ext(_col2_x + 14, _col2_y + 60, "Historical Grievance: " + _cr_hg, 16, _col2_w - 28);

                // Faction AI Behavioral Intelligence Box (docs/36)
                var _f1 = variable_struct_get(_fm.factions, _cur_rel.faction_1);
                var _f2 = variable_struct_get(_fm.factions, _cur_rel.faction_2);
                if (!is_undefined(_f1) && !is_undefined(_f2)) {
                    var _f1_sn = string(_f1.short_name ?? "FACTION 1");
                    var _f1_st = string(_f1.ai_state ?? "PEACE");
                    var _f1_bt = string(_f1.ai_behavior_title ?? "Standard Doctrine");
                    var _f1_ar = string_upper(string(_f1.primary_enemy_id ?? "NONE"));
                    var _f1_pa = string_upper(string(_f1.preferred_ally_id ?? "NONE"));
                    var _f1_bm = string(_f1.contract_bounty_multiplier ?? 1.0);

                    var _f2_sn = string(_f2.short_name ?? "FACTION 2");
                    var _f2_st = string(_f2.ai_state ?? "PEACE");
                    var _f2_bt = string(_f2.ai_behavior_title ?? "Standard Doctrine");
                    var _f2_ar = string_upper(string(_f2.primary_enemy_id ?? "NONE"));
                    var _f2_pa = string_upper(string(_f2.preferred_ally_id ?? "NONE"));
                    var _f2_bm = string(_f2.contract_bounty_multiplier ?? 1.0);

                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_text(_col2_x + 14, _col2_y + 94, "FACTION AI BRAIN & BEHAVIORAL INTELLIGENCE:");

                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_col2_x + 14, _col2_y + 112, "* " + _f1_sn + " [" + _f1_st + "]: " + _f1_bt);
                    draw_set_color(make_color_rgb(190, 215, 240));
                    draw_text(_col2_x + 24, _col2_y + 128, "  Arch-Rival: " + _f1_ar + "  |  Preferred Ally: " + _f1_pa + "  |  Bounty Mult: " + _f1_bm + "x");

                    draw_set_color(make_color_rgb(255, 215, 80));
                    draw_text(_col2_x + 14, _col2_y + 146, "* " + _f2_sn + " [" + _f2_st + "]: " + _f2_bt);
                    draw_set_color(make_color_rgb(190, 215, 240));
                    draw_text(_col2_x + 24, _col2_y + 162, "  Arch-Rival: " + _f2_ar + "  |  Preferred Ally: " + _f2_pa + "  |  Bounty Mult: " + _f2_bm + "x");
                }'''
    ),
    # 2. Torso alloy plaque
    (
'''                draw_text(_cad_x + 68, _plaq_y + 30, _tr.req_alloy + " (" + _al_hex + ")");
                draw_set_color(make_color_rgb(160, 205, 235));
                draw_text(_cad_x + 68, _plaq_y + 48, "Sintered Hull Matrix // " + _tr.name);
                draw_set_color(make_color_rgb(100, 240, 160));
                draw_text(_cad_x + 68, _plaq_y + 66, "Armor Deflection: " + _tr.bonus);''',
'''                draw_text(_cad_x + 68, _plaq_y + 30, string(_tr.req_alloy) + " (" + string(_al_hex) + ")");
                draw_set_color(make_color_rgb(160, 205, 235));
                draw_text(_cad_x + 68, _plaq_y + 48, "Sintered Hull Matrix // " + string(_tr.name));
                draw_set_color(make_color_rgb(100, 240, 160));
                draw_text(_cad_x + 68, _plaq_y + 66, "Armor Deflection: " + string(_tr.bonus));'''
    ),
    # 3. Weapon firepower in CAD assembly
    (
'''draw_text(_col3_x + 14, _w_diag_y, "4. PRIMARY WEAPON: " + _wp.name + " (" + string(_wp.damage) + " Dmg)");''',
'''draw_text(_col3_x + 14, _w_diag_y, "4. PRIMARY WEAPON: " + string(_wp.name ?? "None") + " (" + string(_wp.damage) + " Dmg)");'''
    ),
    # 4. Contract card header
    (
'''draw_text(_cb_x + 14, _acy + 8, _acnt.title + " [FACTION: " + _acnt.faction_name + "]");''',
'''draw_text(_cb_x + 14, _acy + 8, string(_acnt.title ?? "Contract") + " [FACTION: " + string(_acnt.faction_name ?? "Independent") + "]");'''
    ),
    # 5. Fly-off candidate vs incumbent comparison
    (
'''                    draw_text(_col2_x + 500, _cmp_y + 6, "INCUMBENT: " + _inc.name + _cand_tag);''',
'''                    draw_text(_col2_x + 500, _cmp_y + 6, "INCUMBENT: " + string(_inc.name ?? "Incumbent") + string(_cand_tag));'''
    ),
    # 6. Matchup headline
    (
'''draw_text(_col2_x + 24, _p3_box_y + 40, "MATCHUP: " + _cur_cand.name + " (Vanguard PMC)  vs  " + _rc + " Champion");''',
'''draw_text(_col2_x + 24, _p3_box_y + 40, "MATCHUP: " + string(_cur_cand.name ?? "Candidate") + " (Vanguard PMC)  vs  " + string(_rc ?? "Rival") + " Champion");'''
    ),
    # 7. Contested sector
    (
'''draw_text(_m_x + 14, _wbox_y + 182, "FRONTLINE: " + _tc.contested_sector);''',
'''draw_text(_m_x + 14, _wbox_y + 182, "FRONTLINE: " + string(_tc.contested_sector ?? "Sector Contested"));'''
    ),
    # 8. Stat unit in celestial nav
    (
'''draw_text(_col2_x + 140, _sry, string(_sr.val) + _sr.unit);''',
'''draw_text(_col2_x + 140, _sry, string(_sr.val) + string(_sr.unit ?? ""));'''
    )
]

applied = 0
for old, new in replacements:
    if old in code:
        code = code.replace(old, new)
        applied += 1
    else:
        print(f"Warning: pattern not found: {old[:50]}...")

with open('objects/obj_HQTerminal/Draw_64.gml', 'w') as f:
    f.write(code)

print(f"Applied {applied}/{len(replacements)} hardening patches to Draw_64.gml")
