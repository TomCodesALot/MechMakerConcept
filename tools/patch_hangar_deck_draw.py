#!/usr/bin/env python3
"""
Patch obj_DebugManager/Draw_64.gml to implement the Gundam Hangar Deck Mech Builder:
- 60% Left: Gantry repair cradle, animated mobile suit visualizer, stance buttons, auto-tune.
- 40% Right: 4-step Sub-tabs [1. CHASSIS], [2. ALLOY], [3. WEAPONS], [4. ROLLOUT].
- Full weapons outfitting from R&D Tech Tree with Smart Default for Role.
"""
import os

DRAW_PATH = "objects/obj_DebugManager/Draw_64.gml"
with open(DRAW_PATH) as f:
    content = f.read()

start_marker = "// TAB 1: MECH BUILDER & MODULAR FORGE ENGINEERING DECK\n// =========================================================================\nelse if (active_debug_tab == 1) {"
end_marker = "// =========================================================================\n// TAB 2: ASTEROID MINING & PLANETARY EXTRACTION DECK"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

assert start_idx != -1 and end_idx != -1, f"Could not find Tab 1 boundaries in {DRAW_PATH}"

new_tab1_code = '''// TAB 1: MECH BUILDER & MODULAR FORGE ENGINEERING DECK
// =========================================================================
else if (active_debug_tab == 1) {
    var _t = calculate_builder_telemetry();

    // ---------------------------------------------------------------------
    // LEFT 60%: HEPHAESTUS MOBILE SUIT FABRICATION GANTRY (w: 680)
    // ---------------------------------------------------------------------
    var _hng_x = _win_x + 14;
    var _hng_y = _win_y + 44;
    var _hng_w = 680;
    var _hng_h = 654;
    scr_draw_snes_panel(_hng_x, _hng_y, _hng_w, _hng_h, "HEPHAESTUS MOBILE SUIT FABRICATION GANTRY", make_color_rgb(0, 240, 255), true, 0.03);

    // Industrial Gantry Backdrop Canvas
    var _gcx = _hng_x + (_hng_w / 2);
    var _gcy = _hng_y + 240;

    draw_set_color(make_color_rgb(8, 16, 28));
    draw_rectangle(_hng_x + 16, _hng_y + 32, _hng_x + _hng_w - 16, _hng_y + 470, false);
    draw_set_color(make_color_rgb(25, 50, 85));
    draw_rectangle(_hng_x + 16, _hng_y + 32, _hng_x + _hng_w - 16, _hng_y + 470, true);

    // Hazard Stripes & Floor Grid
    for (var hz = _hng_x + 16; hz < _hng_x + _hng_w - 16; hz += 24) {
        draw_set_color(make_color_rgb(50, 45, 15));
        draw_line(hz, _hng_y + 456, hz + 14, _hng_y + 470);
    }
    draw_set_color(make_color_rgb(18, 42, 70));
    draw_line(_gcx - 260, _gcy, _gcx + 260, _gcy);
    draw_line(_gcx, _gcy - 190, _gcx, _gcy + 190);
    draw_circle(_gcx, _gcy, 180, true);
    draw_circle(_gcx, _gcy, 90, true);

    // Magnetic Gantry Scaffolding Clamps
    draw_set_color(make_color_rgb(45, 55, 75));
    draw_rectangle(_hng_x + 24, _gcy - 80, _hng_x + 48, _gcy + 80, false);
    draw_rectangle(_hng_x + _hng_w - 48, _gcy - 80, _hng_x + _hng_w - 24, _gcy + 80, false);
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_rectangle(_hng_x + 24, _gcy - 80, _hng_x + 48, _gcy + 80, true);
    draw_rectangle(_hng_x + _hng_w - 48, _gcy - 80, _hng_x + _hng_w - 24, _gcy + 80, true);

    // Live Render Mobile Suit
    var _draw_spr = _t.preview_sprite;
    if (builder_anim_state == "fire") _draw_spr = _t.primary_wpn.sprite;
    else if (builder_anim_state == "melee") _draw_spr = _t.melee_wpn.sprite;
    else if (builder_anim_state == "boost") {
        if (variable_struct_exists(_t.sprites, "boost") && _t.sprites.boost != -1) _draw_spr = _t.sprites.boost;
        else _draw_spr = spr_ms_aether_boost;
    }

    if (sprite_exists(_draw_spr)) {
        var _sub = floor(builder_subimg) % sprite_get_number(_draw_spr);
        draw_sprite_ext(_draw_spr, _sub, _gcx, _gcy + 45, builder_preview_scale, builder_preview_scale, 0, c_white, 1.0);
    }

    // Reticle Scan Line
    var _scan_y = _hng_y + 32 + ((current_time / 16.0) % 438);
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_set_alpha(0.35);
    draw_line(_hng_x + 16, _scan_y, _hng_x + _hng_w - 16, _scan_y);
    draw_set_alpha(1.0);

    // Stance Action Testing Buttons Row
    var _st_y = _hng_y + 482;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_hng_x + 20, _st_y, "LIVE GANTRY STANCE PREVIEW:");

    var _stances = ["idle", "boost", "fire", "melee"];
    var _st_names = ["IDLE STANCE", "VERNIER BOOST", "PRIMARY FIRE", "MELEE STRIKE"];
    for (var st = 0; st < 4; st++) {
        var _stx = _hng_x + 20 + (st * 160);
        var _st_hov = (_mx >= _stx && _mx <= _stx + 150 && _my >= _st_y + 20 && _my <= _st_y + 52);
        var _st_act = (builder_anim_state == _stances[st]);
        if (_st_hov && _click) {
            builder_anim_state = _stances[st];
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_stx, _st_y + 20, 150, 32, _st_names[st], _st_hov || _st_act, _st_act, _st_act ? make_color_rgb(0, 240, 255) : c_white);
    }

    // Callsign Banner & Auto-Tune Button
    var _ban_y = _hng_y + 550;
    draw_set_color(make_color_rgb(140, 170, 200));
    draw_text(_hng_x + 20, _ban_y, "CUSTOM CALLSIGN:");
    draw_set_color(make_color_rgb(255, 220, 80));
    draw_text(_hng_x + 165, _ban_y, builder_custom_name);

    draw_set_color(make_color_rgb(140, 170, 200));
    draw_text(_hng_x + 360, _ban_y, "DOCTRINE ROLE:");
    draw_set_color(c_white);
    draw_text(_hng_x + 480, _ban_y, string_copy(_t.chassis.doctrine, 1, 24));

    var _tune_btn_y = _ban_y + 30;
    var _at_hov = (_mx >= _hng_x + 20 && _mx <= _hng_x + _hng_w - 20 && _my >= _tune_btn_y && _my <= _tune_btn_y + 44);
    if (_at_hov && _click) {
        if (instance_exists(obj_BlueprintManager)) {
            obj_BlueprintManager.auto_tune_prototype();
            scr_audio_play_ui("boot");
        }
    }
    scr_draw_snes_button(_hng_x + 20, _tune_btn_y, _hng_w - 40, 44, ">> AUTO-TUNE PROTOTYPE BENCHES (S-GRADE MASTERWORK) <<", _at_hov, true, make_color_rgb(255, 200, 50));

    // ---------------------------------------------------------------------
    // RIGHT 40%: ORDNANCE CONFIGURATION & TELEMETRY DECK (w: 566)
    // ---------------------------------------------------------------------
    var _eng_x = _hng_x + _hng_w + 14;
    var _eng_y = _win_y + 44;
    var _eng_w = 566;
    var _eng_h = 654;
    scr_draw_snes_panel(_eng_x, _eng_y, _eng_w, _eng_h, "ORDNANCE CONFIGURATION & TELEMETRY", make_color_rgb(0, 240, 255), true, 0.03);

    // 4 Sub-Tabs Navigation Row
    var _sub_titles = ["1. CHASSIS", "2. ALLOY", "3. WEAPONS", "4. ROLLOUT"];
    var _sub_w = 130;
    for (var sb = 0; sb < 4; sb++) {
        var _sbx = _eng_x + 18 + (sb * 134);
        var _sb_hov = (_mx >= _sbx && _mx <= _sbx + _sub_w && _my >= _eng_y + 24 && _my <= _eng_y + 54);
        var _sb_act = (builder_subtab == sb);
        if (_sb_hov && _click) {
            builder_subtab = sb;
            scr_audio_play_ui("tab");
        }
        scr_draw_snes_button(_sbx, _eng_y + 24, _sub_w, 30, _sub_titles[sb], _sb_hov || _sb_act, _sb_act, _sb_act ? make_color_rgb(0, 240, 255) : c_white);
    }

    var _deck_y = _eng_y + 68;

    // =====================================================================
    // SUBTAB 0: CHASSIS & DOCTRINAL ROLE SELECTION
    // =====================================================================
    if (builder_subtab == 0) {
        var _clist = get_canonical_chassis_list();
        var _c = _t.chassis;

        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 20, _deck_y, "BASE MOBILE SUIT CHASSIS PLATFORM:");

        // Chassis Card
        var _cc_y = _deck_y + 24;
        draw_set_color(make_color_rgb(14, 26, 44));
        draw_rectangle(_eng_x + 18, _cc_y, _eng_x + _eng_w - 18, _cc_y + 160, false);
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_rectangle(_eng_x + 18, _cc_y, _eng_x + _eng_w - 18, _cc_y + 160, true);

        // Name & Model Code
        draw_set_color(make_color_rgb(255, 220, 80));
        draw_text_transformed(_eng_x + 30, _cc_y + 12, _c.name, 1.15, 1.15, 0);

        draw_set_color(make_color_rgb(140, 180, 220));
        draw_text(_eng_x + 30, _cc_y + 40, "Faction: " + _c.faction_id + " | Movement Locomotion: " + string_upper(_c.chassis));

        draw_set_color(c_white);
        draw_text(_eng_x + 30, _cc_y + 64, "Core Power: " + string(_c.power_output) + " MW | Mass: " + string(_c.weight_tonnes) + " tonnes | Speed: " + string(_c.speed) + " km/h");

        draw_set_color(make_color_rgb(180, 220, 255));
        draw_text(_eng_x + 30, _cc_y + 90, "Standard Issue Doctrine: " + _c.doctrine);

        draw_set_color(make_color_rgb(255, 180, 60));
        draw_text(_eng_x + 30, _cc_y + 116, "Signature Armament: " + _c.weapon_name);

        // Prev & Next Chassis Buttons
        var _pbtn_y = _cc_y + 175;
        var _cp_hov = (_mx >= _eng_x + 18 && _mx <= _eng_x + 260 && _my >= _pbtn_y && _my <= _pbtn_y + 40);
        var _cn_hov = (_mx >= _eng_x + 280 && _mx <= _eng_x + _eng_w - 18 && _my >= _pbtn_y && _my <= _pbtn_y + 40);

        if (_cp_hov && _click) {
            builder_chassis_idx = (builder_chassis_idx - 1 + array_length(_clist)) % array_length(_clist);
            apply_smart_default_loadout(_clist[builder_chassis_idx]);
            scr_audio_play_ui("click");
        }
        if (_cn_hov && _click) {
            builder_chassis_idx = (builder_chassis_idx + 1) % array_length(_clist);
            apply_smart_default_loadout(_clist[builder_chassis_idx]);
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_eng_x + 18, _pbtn_y, 242, 40, "< PREVIOUS CHASSIS", _cp_hov, false, c_aqua);
        scr_draw_snes_button(_eng_x + 280, _pbtn_y, 242, 40, "NEXT CHASSIS >", _cn_hov, false, c_aqua);

        // Quick Preset Hot-Select Row
        var _qp_y = _pbtn_y + 65;
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 20, _qp_y, "QUICK DOCTRINAL PRESETS:");

        var _qnames = ["IRONCLAD (TC)", "AETHER (OCL)", "CENTURION (TC)", "KEPLER (OCL)", "HYENA (RS)"];
        var _qindices = [0, 6, 1, 7, 12];
        for (var q = 0; q < min(5, array_length(_qnames)); q++) {
            var _qy_pos = _qp_y + 24 + (q * 44);
            var _qhov = (_mx >= _eng_x + 18 && _mx <= _eng_x + _eng_w - 18 && _my >= _qy_pos && _my <= _qy_pos + 36);
            if (_qhov && _click) {
                builder_chassis_idx = _qindices[q] % array_length(_clist);
                apply_smart_default_loadout(_clist[builder_chassis_idx]);
                scr_audio_play_ui("click");
            }
            scr_draw_snes_button(_eng_x + 18, _qy_pos, _eng_w - 36, 36, "[PRESET: " + _qnames[q] + "]", _qhov, false, make_color_rgb(100, 220, 255));
        }
    }

    // =====================================================================
    // SUBTAB 1: SINTERED ALLOY METALLURGY
    // =====================================================================
    else if (builder_subtab == 1) {
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 20, _deck_y, "SINTERED ALLOY PLATING (MOLECULAR CRUCIBLE):");

        var _al_y = _deck_y + 24;
        for (var a = 0; a < array_length(builder_alloys); a++) {
            var _ay_pos = _al_y + (a * 76);
            var _is_cur_al = (builder_alloy_idx == a);
            var _al_hov = (_mx >= _eng_x + 18 && _mx <= _eng_x + _eng_w - 18 && _my >= _ay_pos && _my <= _ay_pos + 70);

            if (_al_hov && _click) {
                builder_alloy_idx = a;
                scr_audio_play_ui("click");
            }

            draw_set_color(_is_cur_al ? make_color_rgb(24, 44, 70) : (_al_hov ? make_color_rgb(18, 30, 48) : make_color_rgb(12, 18, 28)));
            draw_rectangle(_eng_x + 18, _ay_pos, _eng_x + _eng_w - 18, _ay_pos + 68, false);
            draw_set_color(_is_cur_al ? make_color_rgb(0, 240, 255) : make_color_rgb(40, 65, 95));
            draw_rectangle(_eng_x + 18, _ay_pos, _eng_x + _eng_w - 18, _ay_pos + 68, true);

            // Alloy Name
            draw_set_color(_is_cur_al ? make_color_rgb(255, 220, 80) : c_white);
            draw_text(_eng_x + 28, _ay_pos + 8, (_is_cur_al ? "> " : "") + builder_alloy_names[a]);

            // Alloy Deltas
            var _ad = builder_alloy_deltas[a];
            draw_set_color(make_color_rgb(160, 190, 220));
            draw_text(_eng_x + 28, _ay_pos + 28, "Armor: " + string(floor(_ad.armor_mult * 100)) + "% | Mass: " + string(floor(_ad.mass_mult * 100)) + "% | Speed: " + (_ad.speed_bonus >= 0 ? "+" : "") + string(_ad.speed_bonus) + " km/h");

            draw_set_color(make_color_rgb(255, 180, 80));
            draw_text(_eng_x + 28, _ay_pos + 46, _ad.desc);
        }
    }

    // =====================================================================
    // SUBTAB 2: WEAPONS & EQUIPMENT OUTFITTING (R&D TECH TREE)
    // =====================================================================
    else if (builder_subtab == 2) {
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 20, _deck_y, "R&D RESEARCHED WEAPONS & EQUIPMENT:");

        // Smart Default Auto-Equip Button
        var _sdef_hov = (_mx >= _eng_x + 18 && _mx <= _eng_x + _eng_w - 18 && _my >= _deck_y + 22 && _my <= _deck_y + 54);
        if (_sdef_hov && _click) {
            apply_smart_default_loadout(_t.chassis);
            show_toast("SMART DEFAULT EQUIPPED: Outfitted latest tech matching role!", c_lime);
            scr_audio_play_ui("boot");
        }
        scr_draw_snes_button(_eng_x + 18, _deck_y + 22, _eng_w - 36, 32, ">> AUTO-EQUIP SMART DEFAULT FOR ROLE <<", _sdef_hov, false, make_color_rgb(0, 240, 255));

        // 4 Hardpoints List
        var _hp_list = [
            { title: "HARDPOINT 1: PRIMARY RANGED WEAPON", item: _t.primary_wpn, list: builder_weapons_db.primary, idx: builder_primary_wpn_idx, slot_key: "primary" },
            { title: "HARDPOINT 2: SECONDARY / AUX MUNITION", item: _t.secondary_wpn, list: builder_weapons_db.secondary, idx: builder_secondary_wpn_idx, slot_key: "secondary" },
            { title: "HARDPOINT 3: CLOSE-COMBAT MELEE", item: _t.melee_wpn, list: builder_weapons_db.melee, idx: builder_melee_wpn_idx, slot_key: "melee" },
            { title: "HARDPOINT 4: DEFENSIVE GEAR / SHIELD", item: _t.shield, list: builder_weapons_db.shield, idx: builder_shield_idx, slot_key: "shield" }
        ];

        var _hp_y = _deck_y + 64;
        for (var h = 0; h < 4; h++) {
            var _hp_info = _hp_list[h];
            var _hpy_pos = _hp_y + (h * 105);

            draw_set_color(make_color_rgb(14, 24, 38));
            draw_rectangle(_eng_x + 18, _hpy_pos, _eng_x + _eng_w - 18, _hpy_pos + 98, false);
            draw_set_color(make_color_rgb(0, 240, 255));
            draw_rectangle(_eng_x + 18, _hpy_pos, _eng_x + _eng_w - 18, _hpy_pos + 98, true);

            draw_set_color(make_color_rgb(255, 220, 80));
            draw_text(_eng_x + 28, _hpy_pos + 6, _hp_info.title);

            // Prev & Next Buttons
            var _hp_p_hov = (_mx >= _eng_x + _eng_w - 90 && _mx <= _eng_x + _eng_w - 56 && _my >= _hpy_pos + 6 && _my <= _hpy_pos + 32);
            var _hp_n_hov = (_mx >= _eng_x + _eng_w - 50 && _mx <= _eng_x + _eng_w - 18 && _my >= _hpy_pos + 6 && _my <= _hpy_pos + 32);

            if (_hp_p_hov && _click) {
                if (h == 0) builder_primary_wpn_idx = (builder_primary_wpn_idx - 1 + array_length(builder_weapons_db.primary)) % array_length(builder_weapons_db.primary);
                else if (h == 1) builder_secondary_wpn_idx = (builder_secondary_wpn_idx - 1 + array_length(builder_weapons_db.secondary)) % array_length(builder_weapons_db.secondary);
                else if (h == 2) builder_melee_wpn_idx = (builder_melee_wpn_idx - 1 + array_length(builder_weapons_db.melee)) % array_length(builder_weapons_db.melee);
                else if (h == 3) builder_shield_idx = (builder_shield_idx - 1 + array_length(builder_weapons_db.shield)) % array_length(builder_weapons_db.shield);
                scr_audio_play_ui("click");
            }
            if (_hp_n_hov && _click) {
                if (h == 0) builder_primary_wpn_idx = (builder_primary_wpn_idx + 1) % array_length(builder_weapons_db.primary);
                else if (h == 1) builder_secondary_wpn_idx = (builder_secondary_wpn_idx + 1) % array_length(builder_weapons_db.secondary);
                else if (h == 2) builder_melee_wpn_idx = (builder_melee_wpn_idx + 1) % array_length(builder_weapons_db.melee);
                else if (h == 3) builder_shield_idx = (builder_shield_idx + 1) % array_length(builder_weapons_db.shield);
                scr_audio_play_ui("click");
            }
            scr_draw_snes_button(_eng_x + _eng_w - 90, _hpy_pos + 6, 34, 26, "<", _hp_p_hov, false, c_aqua);
            scr_draw_snes_button(_eng_x + _eng_w - 50, _hpy_pos + 6, 32, 26, ">", _hp_n_hov, false, c_aqua);

            // Item Details
            var _it = _hp_info.item;
            draw_set_color(c_white);
            draw_text(_eng_x + 28, _hpy_pos + 28, _it.name);

            // Research Status Tag
            var _is_res = is_tech_researched(_it.tech_id);
            draw_set_color(_is_res ? c_lime : make_color_rgb(255, 140, 40));
            draw_text(_eng_x + 28, _hpy_pos + 48, _is_res ? "[TECH RESEARCHED & AVAILABLE]" : "[LOCKED IN TECH TREE: " + _it.tech_id + "]");

            draw_set_color(make_color_rgb(160, 190, 220));
            var _stat_line = "";
            if (variable_struct_exists(_it, "damage") && _it.damage > 0) _stat_line += "Dmg: " + string(_it.damage) + " | ";
            if (variable_struct_exists(_it, "armor_hp")) _stat_line += "Armor Guard: +" + string(_it.armor_hp) + " HP | ";
            _stat_line += "Mass: " + string(_it.mass) + "t | Draw: -" + string(_it.power_draw) + " MW";
            draw_text(_eng_x + 28, _hpy_pos + 66, _stat_line);

            draw_set_color(make_color_rgb(255, 180, 80));
            draw_text(_eng_x + 28, _hpy_pos + 82, _it.lore);
        }

        // Cheat unlock all button
        var _res_all_y = _hp_y + 428;
        var _ra_hov = (_mx >= _eng_x + 18 && _mx <= _eng_x + _eng_w - 18 && _my >= _res_all_y && _my <= _res_all_y + 36);
        if (_ra_hov && _click) {
            unlock_all_research_cheats();
        }
        scr_draw_snes_button(_eng_x + 18, _res_all_y, _eng_w - 36, 36, "UNLOCK ALL WEAPONS & EQUIPMENT IN TECH TREE (CHEAT)", _ra_hov, false, make_color_rgb(255, 200, 50));
    }

    // =====================================================================
    // SUBTAB 3: TELEMETRY & FLEET ROLLOUT
    // =====================================================================
    else if (builder_subtab == 3) {
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 20, _deck_y, "LIVE ENGINEERING TELEMETRY & ROLLOUT:");

        var _ty = _deck_y + 30;

        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 28, _ty, "ARMOR INTEGRITY:");
        draw_set_color(c_white);
        draw_text(_eng_x + 280, _ty, string(_t.total_armor) + " HP");

        _ty += 28;
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 28, _ty, "TOTAL CHASSIS MASS:");
        draw_set_color(_t.mass_overloaded ? c_red : c_white);
        draw_text(_eng_x + 280, _ty, string(_t.total_mass) + " t / " + string(_t.max_capacity) + " t Limit");

        // Capacity Bar
        _ty += 22;
        draw_set_color(make_color_rgb(20, 30, 45));
        draw_rectangle(_eng_x + 28, _ty, _eng_x + _eng_w - 28, _ty + 12, false);
        var _m_pct = clamp(_t.total_mass / max(1, _t.max_capacity), 0.0, 1.0);
        draw_set_color(_t.mass_overloaded ? c_red : make_color_rgb(0, 240, 255));
        draw_rectangle(_eng_x + 28, _ty, _eng_x + 28 + (_m_pct * (_eng_w - 56)), _ty + 12, false);

        _ty += 26;
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 28, _ty, "REACTOR OUTPUT BALANCE:");
        draw_set_color(_t.reactor_overloaded ? c_red : c_lime);
        draw_text(_eng_x + 280, _ty, (_t.net_power >= 0 ? "+" : "") + string(_t.net_power) + " MW (Core: " + string(_t.power_output) + " MW)");

        _ty += 28;
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 28, _ty, "CALCULATED SPEED:");
        draw_set_color(c_white);
        draw_text(_eng_x + 280, _ty, string(_t.walk_speed) + " km/h (Boost: " + string(_t.boost_speed) + " km/h)");

        _ty += 28;
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 28, _ty, "COMBAT RATING (OSS):");
        draw_set_color(make_color_rgb(255, 220, 80));
        draw_text(_eng_x + 280, _ty, string(_t.combat_rating) + " [SUPERIOR]");

        _ty += 28;
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 28, _ty, "WEIGHT CLASSIFICATION:");
        draw_set_color(c_white);
        draw_text(_eng_x + 280, _ty, _t.weight_class);

        // Overload Safety Alert Box
        _ty += 38;
        if (_t.reactor_overloaded) {
            draw_set_color(c_red);
            draw_rectangle(_eng_x + 28, _ty, _eng_x + _eng_w - 28, _ty + 34, false);
            draw_set_color(c_white);
            draw_text(_eng_x + 36, _ty + 8, "! REACTOR OVERLOAD: POWER DRAW EXCEEDS CORE GENERATION !");
            _ty += 46;
        } else {
            draw_set_color(make_color_rgb(18, 48, 30));
            draw_rectangle(_eng_x + 28, _ty, _eng_x + _eng_w - 28, _ty + 34, false);
            draw_set_color(c_lime);
            draw_text(_eng_x + 36, _ty + 8, "v POWER GRID STABLE // READY FOR COMBAT PROVING");
            _ty += 46;
        }

        // Direct Action Buttons
        _ty += 12;
        var _btn1_hov = (_mx >= _eng_x + 28 && _mx <= _eng_x + _eng_w - 28 && _my >= _ty && _my <= _ty + 52);
        if (_btn1_hov && _click) {
            deploy_builder_mech_to_combat();
        }
        scr_draw_snes_button(_eng_x + 28, _ty, _eng_w - 56, 52, ">>>> DEPLOY TO COMBAT LAB (TAB 0) <<<<", _btn1_hov, true, make_color_rgb(0, 240, 255));

        _ty += 64;
        var _btn2_hov = (_mx >= _eng_x + 28 && _mx <= _eng_x + _eng_w - 28 && _my >= _ty && _my <= _ty + 44);
        if (_btn2_hov && _click) {
            commission_builder_mech_to_hangar();
        }
        scr_draw_snes_button(_eng_x + 28, _ty, _eng_w - 56, 44, "COMMISSION TO FLEET HANGAR", _btn2_hov, false, make_color_rgb(100, 220, 255));
    }
}
'''

content = content[:start_idx] + new_tab1_code + "\n" + content[end_idx:]

with open(DRAW_PATH, "w") as f:
    f.write(content)

print("Draw_64.gml patched successfully with Gundam Hangar Deck!")
