with open("objects/obj_HQTerminal/Draw_64.gml") as f:
    text = f.read()

# -----------------------------------------------------------------------------
# 1. Update contracts_subtab == 1 Header to include Candidate Pool Toggle
# -----------------------------------------------------------------------------
old_header = """            // Top Header: Title + Adoption Toggle Tab
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
            }"""

new_header = """            // Top Header: Title + Adoption & Candidate Pool Toggles
            draw_set_color(make_color_rgb(255, 215, 80));
            draw_text(_col2_x + 14, _arena_y + 10, "PROCUREMENT BUREAU: " + _inc.faction_name);
            draw_set_color(make_color_rgb(160, 190, 220));
            draw_text(_col2_x + 14, _arena_y + 28, "Evaluator: " + _inc.evaluator + " | Doctrine Focus: " + _inc.doctrine_focus);

            var _cand_btn_w = 210;
            var _cand_btn_x = _col2_x + _col2_w - _cand_btn_w - 14;
            var _cand_btn_y = _arena_y + 8;
            var _cand_btn_hov = (_mx >= _cand_btn_x && _mx <= _cand_btn_x + _cand_btn_w && _my >= _cand_btn_y && _my <= _cand_btn_y + 28);
            if (_cand_btn_hov && _click) {
                trial_view_candidates_mode = !trial_view_candidates_mode;
            }
            scr_draw_snes_button(_cand_btn_x, _cand_btn_y, _cand_btn_w, 28, trial_view_candidates_mode ? "[<< FLY-OFF ARENA]" : "[INSPECT 4 MP CANDIDATES >>]", _cand_btn_hov, trial_view_candidates_mode, make_color_rgb(255, 215, 80));

            if (_is_adopted && !trial_view_candidates_mode) {
                var _tgl_w = 170;
                var _tgl_x = _cand_btn_x - _tgl_w - 8;
                var _tgl_y = _arena_y + 8;
                var _tgl_hov = (_mx >= _tgl_x && _mx <= _tgl_x + _tgl_w && _my >= _tgl_y && _my <= _tgl_y + 28);
                if (_tgl_hov && _click) {
                    trial_view_adoption_panel = !trial_view_adoption_panel;
                }
                scr_draw_snes_button(_tgl_x, _tgl_y, _tgl_w, 28, trial_view_adoption_panel ? "[FLY-OFF ARENA]" : "[FLEET ADOPTION]", _tgl_hov, trial_view_adoption_panel, make_color_rgb(80, 220, 140));
            }"""

assert old_header in text, "Could not find old_header"
text = text.replace(old_header, new_header)

# -----------------------------------------------------------------------------
# 2. Insert Candidate Pool Inspection Panel in contracts_subtab == 1
# -----------------------------------------------------------------------------
old_view_a_marker = """            // =========================================================================
            // VIEW A: FLEET ADOPTION & MODERNIZATION DASHBOARD (docs/26 Pillar II & III)
            // ========================================================================="""

candidate_panel_code = """            // =========================================================================
            // VIEW C: 4-CANDIDATE MASS PRODUCTION PROCUREMENT DOSSIERS (docs/29 & docs/30)
            // =========================================================================
            if (trial_view_candidates_mode) {
                var _cp_y = _arena_y + 44;
                var _cp_h = _arena_h - 54;
                var _cand_pool = variable_struct_exists(_fm.mass_production_candidates, trial_selected_faction) ? _fm.mass_production_candidates[$ trial_selected_faction] : [];
                var _card_w = floor((_col2_w - 32) / 4);

                for (var ci = 0; ci < min(4, array_length(_cand_pool)); ci++) {
                    var _cdata = _cand_pool[ci];
                    var _cx = _col2_x + 12 + ci * (_card_w + 4);
                    var _is_incumbent = (!is_undefined(_cur_mp) && _cur_mp.baseline_suit_id == _cdata.id);
                    var _is_sel_cand = (trial_candidate_dossier_idx == ci);
                    var _chov = (_mx >= _cx && _mx <= _cx + _card_w && _my >= _cp_y && _my <= _cp_y + _cp_h);
                    if (_chov && _click) trial_candidate_dossier_idx = ci;

                    // Card Enclosure
                    draw_set_color(_is_incumbent ? make_color_rgb(24, 32, 20) : (_is_sel_cand ? make_color_rgb(18, 30, 48) : make_color_rgb(12, 18, 26)));
                    draw_rectangle(_cx, _cp_y, _cx + _card_w, _cp_y + _cp_h, false);
                    draw_set_color(_is_incumbent ? make_color_rgb(255, 215, 80) : (_is_sel_cand ? make_color_rgb(80, 200, 255) : make_color_rgb(40, 60, 85)));
                    draw_rectangle(_cx, _cp_y, _cx + _card_w, _cp_y + _cp_h, true);

                    // Candidate Badge & Title
                    if (_is_incumbent) {
                        draw_set_color(make_color_rgb(255, 215, 80));
                        draw_rectangle(_cx + 4, _cp_y + 4, _cx + _card_w - 4, _cp_y + 20, false);
                        draw_set_color(c_black);
                        draw_text(_cx + 8, _cp_y + 5, "*** RATIFIED LINE ***");
                    } else {
                        draw_set_color(make_color_rgb(45, 65, 90));
                        draw_rectangle(_cx + 4, _cp_y + 4, _cx + _card_w - 4, _cp_y + 20, false);
                        draw_set_color(make_color_rgb(180, 210, 240));
                        draw_text(_cx + 8, _cp_y + 5, "CANDIDATE " + string(ci + 1) + "/4");
                    }

                    draw_set_color(make_color_rgb(240, 240, 240));
                    draw_text(_cx + 6, _cp_y + 26, _cdata.name);
                    draw_set_color(make_color_rgb(160, 190, 220));
                    draw_text(_cx + 6, _cp_y + 42, string_copy(_cdata.doctrine, 1, 18));

                    // Animated Sprite Box (160x160 rendered at 0.52 scale)
                    var _spr_cy = _cp_y + 165;
                    scr_draw_animated_mobile_suit(_cdata.id, _cx + _card_w / 2, _spr_cy, 0.52, 1, catalog_anim_state);

                    // Animation Mode Buttons
                    var _an_btns = ["idle", "walk", "fire", "hit"];
                    var _ab_w = floor((_card_w - 16) / 4);
                    for (var bi = 0; bi < 4; bi++) {
                        var _ab_x = _cx + 6 + bi * (_ab_w + 1);
                        var _ab_y = _cp_y + 175;
                        var _ab_act = (catalog_anim_state == _an_btns[bi]);
                        var _ab_hov = (_mx >= _ab_x && _mx <= _ab_x + _ab_w && _my >= _ab_y && _my <= _ab_y + 18);
                        if (_ab_hov && _click) catalog_anim_state = _an_btns[bi];
                        draw_set_color(_ab_act ? make_color_rgb(100, 220, 255) : (_ab_hov ? make_color_rgb(45, 75, 105) : make_color_rgb(18, 28, 40)));
                        draw_rectangle(_ab_x, _ab_y, _ab_x + _ab_w, _ab_y + 18, false);
                        draw_set_color(_ab_act ? c_black : make_color_rgb(180, 200, 220));
                        draw_text(_ab_x + 2, _ab_y + 3, string_upper(string_copy(_an_btns[bi], 1, 3)));
                    }

                    // Specs Telemetry
                    var _sy = _cp_y + 200;
                    draw_set_color(make_color_rgb(120, 160, 200));
                    draw_text(_cx + 6, _sy, "Armor: " + string(_cdata.armor) + " HP");
                    draw_text(_cx + 6, _sy + 16, "Reactor: +" + string(_cdata.power) + " MW");
                    draw_text(_cx + 6, _sy + 32, "Speed: " + string(_cdata.speed) + " kph");
                    draw_text(_cx + 6, _sy + 48, "Combat: " + string(_cdata.combat) + " PTS");
                    draw_set_color(make_color_rgb(255, 180, 80));
                    draw_text(_cx + 6, _sy + 68, "Wpn: " + string_copy(_cdata.weapon, 1, 16));
                    draw_set_color(make_color_rgb(100, 240, 140));
                    draw_text(_cx + 6, _sy + 86, "Royalty: +" + string(_cdata.royalty) + "/t");

                    // Select as Fly-Off Target
                    var _sel_btn_y = _cp_y + _cp_h - 26;
                    var _sb_hov = (_mx >= _cx + 4 && _mx <= _cx + _card_w - 4 && _my >= _sel_btn_y && _my <= _sel_btn_y + 22);
                    if (_sb_hov && _click) {
                        _cur_mp.baseline_suit_id = _cdata.id;
                        _cur_mp.baseline_suit_name = _cdata.name;
                        _cur_mp.doctrine = _cdata.doctrine;
                        _cur_mp.signature_weapon = _cdata.weapon;
                        _cur_mp.sprite_asset = _cdata.sprite;
                        _cur_mp.req_armor = _cdata.req_armor;
                        _cur_mp.req_power = _cdata.req_power;
                        _cur_mp.licensing_bounty = _cdata.bounty;
                        _cur_mp.royalty_per_turn = _cdata.royalty;
                        trial_view_candidates_mode = false;
                    }
                    draw_set_color(_sb_hov ? make_color_rgb(40, 80, 120) : make_color_rgb(20, 35, 55));
                    draw_rectangle(_cx + 4, _sel_btn_y, _cx + _card_w - 4, _sel_btn_y + 22, false);
                    draw_set_color(_is_incumbent ? make_color_rgb(255, 215, 80) : make_color_rgb(80, 200, 255));
                    draw_rectangle(_cx + 4, _sel_btn_y, _cx + _card_w - 4, _sel_btn_y + 22, true);
                    draw_text(_cx + 8, _sel_btn_y + 4, _is_incumbent ? "[RATIFIED LINE]" : "[FLY-OFF TARGET]");
                }
            }
            // =========================================================================
            // VIEW A: FLEET ADOPTION & MODERNIZATION DASHBOARD (docs/26 Pillar II & III)
            // ========================================================================="""

assert old_view_a_marker in text, "Could not find old_view_a_marker"
text = text.replace(old_view_a_marker, candidate_panel_code)

# -----------------------------------------------------------------------------
# 3. Update war_subtab == 1 to include 100-Suit Encyclopedia Mode
# -----------------------------------------------------------------------------
old_faction_tabs = """        // Faction Selector Buttons (4 Factions)
        var _f_tabs = [
            { id: "faction_terran", label: "1. THE TERRAN COALITION", col: make_color_rgb(60, 130, 240) },
            { id: "faction_colony", label: "2. THE OUTER COLONIES", col: make_color_rgb(40, 210, 180) },
            { id: "faction_syndicate", label: "3. RIM-SYNDICATE CARTEL", col: make_color_rgb(240, 140, 40) },
            { id: "faction_zaibatsu", label: "4. APEX BIO-ZAIBATSU", col: make_color_rgb(180, 90, 240) }
        ];
        var _fb_w = (_fw_pan - 36) / 4;
        for (var fti = 0; fti < 4; fti++) {
            var _ft_dat = _f_tabs[fti];
            var _fbx = _fx_pan + fti * (_fb_w + 12);
            var _fb_act = (selected_faction_dossier == _ft_dat.id);
            var _fb_hov = (_mx >= _fbx && _mx <= _fbx + _fb_w && _my >= _fy_pan && _my <= _fy_pan + 32);
            if (_fb_hov && _click) selected_faction_dossier = _ft_dat.id;

            draw_set_color(_fb_act ? make_color_rgb(24, 48, 76) : (_fb_hov ? make_color_rgb(18, 32, 50) : make_color_rgb(12, 18, 26)));
            draw_rectangle(_fbx, _fy_pan, _fbx + _fb_w, _fy_pan + 32, false);
            draw_set_color(_fb_act ? _ft_dat.col : make_color_rgb(40, 60, 80));
            draw_rectangle(_fbx, _fy_pan, _fbx + _fb_w, _fy_pan + 32, true);
            draw_set_color(_fb_act ? c_white : make_color_rgb(170, 195, 220));
            draw_text(_fbx + 12, _fy_pan + 8, _ft_dat.label);
        }

        // Left Card: Faction Standing & Military Mech Representative
        var _d_y = _fy_pan + 44;
        var _col1_w = 340;"""

new_faction_tabs = """        // Faction Selector Buttons (4 Factions) + 100-Suit Encyclopedia Toggle
        var _f_tabs = [
            { id: "faction_terran", label: "1. TERRAN COALITION", col: make_color_rgb(60, 130, 240) },
            { id: "faction_colony", label: "2. OUTER COLONIES", col: make_color_rgb(40, 210, 180) },
            { id: "faction_syndicate", label: "3. RIM-SYNDICATES", col: make_color_rgb(240, 140, 40) },
            { id: "faction_zaibatsu", label: "4. APEX ZAIBATSU", col: make_color_rgb(180, 90, 240) },
            { id: "catalog_100", label: "5. [100-SUIT ENCYCLOPEDIA]", col: make_color_rgb(255, 215, 80) }
        ];
        var _fb_w = (_fw_pan - 48) / 5;
        for (var fti = 0; fti < 5; fti++) {
            var _ft_dat = _f_tabs[fti];
            var _fbx = _fx_pan + fti * (_fb_w + 12);
            var _fb_act = (fti == 4 ? (catalog_view_mode == 1) : (catalog_view_mode == 0 && selected_faction_dossier == _ft_dat.id));
            var _fb_hov = (_mx >= _fbx && _mx <= _fbx + _fb_w && _my >= _fy_pan && _my <= _fy_pan + 32);
            if (_fb_hov && _click) {
                if (fti == 4) {
                    catalog_view_mode = 1;
                } else {
                    catalog_view_mode = 0;
                    selected_faction_dossier = _ft_dat.id;
                }
            }

            draw_set_color(_fb_act ? make_color_rgb(24, 48, 76) : (_fb_hov ? make_color_rgb(18, 32, 50) : make_color_rgb(12, 18, 26)));
            draw_rectangle(_fbx, _fy_pan, _fbx + _fb_w, _fy_pan + 32, false);
            draw_set_color(_fb_act ? _ft_dat.col : make_color_rgb(40, 60, 80));
            draw_rectangle(_fbx, _fy_pan, _fbx + _fb_w, _fy_pan + 32, true);
            draw_set_color(_fb_act ? c_white : make_color_rgb(170, 195, 220));
            draw_text(_fbx + 8, _fy_pan + 8, _ft_dat.label);
        }

        var _d_y = _fy_pan + 44;

        // =========================================================================
        // BRANCH A: 100-SUIT MASTER UNIVERSE ENCYCLOPEDIA & LIVE ANIMATOR (DOC-30)
        // =========================================================================
        if (catalog_view_mode == 1) {
            var _enc_w = _fw_pan;
            var _enc_h = _fh_pan - 44;

            // Top Filter Toolbar
            var _flt_y = _d_y;
            var _flt_h = 32;
            draw_set_color(make_color_rgb(12, 18, 28));
            draw_rectangle(_fx_pan, _flt_y, _fx_pan + _enc_w, _flt_y + _flt_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_fx_pan, _flt_y, _fx_pan + _enc_w, _flt_y + _flt_h, true);

            // Faction Filter Buttons
            var _fac_flts = [
                { id: "ALL", label: "ALL (100)" },
                { id: "faction_a", label: "TERRAN (25)" },
                { id: "faction_b", label: "COLONIES (23)" },
                { id: "faction_c", label: "SYNDICATES (25)" },
                { id: "faction_d", label: "ZAIBATSU (23)" },
                { id: "pmc_player", label: "PMC (4)" }
            ];
            var _ff_w = 110;
            for (var ffi = 0; ffi < array_length(_fac_flts); ffi++) {
                var _ffx = _fx_pan + 8 + ffi * (_ff_w + 6);
                var _ff_act = (catalog_filter_faction == _fac_flts[ffi].id);
                var _ff_hov = (_mx >= _ffx && _mx <= _ffx + _ff_w && _my >= _flt_y + 4 && _my <= _flt_y + 28);
                if (_ff_hov && _click) {
                    catalog_filter_faction = _fac_flts[ffi].id;
                    catalog_scroll_offset = 0;
                }
                draw_set_color(_ff_act ? make_color_rgb(80, 200, 255) : (_ff_hov ? make_color_rgb(25, 45, 70) : make_color_rgb(16, 24, 36)));
                draw_rectangle(_ffx, _flt_y + 4, _ffx + _ff_w, _flt_y + 28, false);
                draw_set_color(_ff_act ? c_white : make_color_rgb(45, 75, 110));
                draw_rectangle(_ffx, _flt_y + 4, _ffx + _ff_w, _flt_y + 28, true);
                draw_set_color(_ff_act ? c_black : make_color_rgb(180, 210, 240));
                draw_text(_ffx + 6, _flt_y + 8, _fac_flts[ffi].label);
            }

            // Era Filter Buttons
            var _era_flts = [
                { id: 0, label: "ALL ERAS" },
                { id: 1, label: "ERA 1" },
                { id: 2, label: "ERA 2" },
                { id: 3, label: "ERA 3" },
                { id: 4, label: "ERA 4" }
            ];
            var _ef_w = 75;
            var _ef_start_x = _fx_pan + _enc_w - (array_length(_era_flts) * (_ef_w + 6)) - 8;
            for (var efi = 0; efi < array_length(_era_flts); efi++) {
                var _efx = _ef_start_x + efi * (_ef_w + 6);
                var _ef_act = (catalog_filter_era == _era_flts[efi].id);
                var _ef_hov = (_mx >= _efx && _mx <= _efx + _ef_w && _my >= _flt_y + 4 && _my <= _flt_y + 28);
                if (_ef_hov && _click) {
                    catalog_filter_era = _era_flts[efi].id;
                    catalog_scroll_offset = 0;
                }
                draw_set_color(_ef_act ? make_color_rgb(255, 215, 80) : (_ef_hov ? make_color_rgb(45, 40, 25) : make_color_rgb(20, 24, 30)));
                draw_rectangle(_efx, _flt_y + 4, _efx + _ef_w, _flt_y + 28, false);
                draw_set_color(_ef_act ? c_white : make_color_rgb(70, 60, 40));
                draw_rectangle(_efx, _flt_y + 4, _efx + _ef_w, _flt_y + 28, true);
                draw_set_color(_ef_act ? c_black : make_color_rgb(220, 200, 160));
                draw_text(_efx + 6, _flt_y + 8, _era_flts[efi].label);
            }

            // Build filtered list from GameManager catalog
            var _matching_suits = [];
            if (instance_exists(obj_GameManager) && is_struct(obj_GameManager.mobile_suit_catalog)) {
                var _c_keys = variable_struct_get_names(obj_GameManager.mobile_suit_catalog);
                for (var ki = 0; ki < array_length(_c_keys); ki++) {
                    var _s = obj_GameManager.mobile_suit_catalog[$ _c_keys[ki]];
                    if (!is_struct(_s)) continue;
                    if (catalog_filter_faction != "ALL" && (_s[$ "faction_id"] ?? "") != catalog_filter_faction) continue;
                    if (catalog_filter_era != 0 && (_s[$ "era"] ?? 0) != catalog_filter_era) continue;
                    array_push(_matching_suits, _s);
                }
            }

            var _body_y = _flt_y + 40;
            var _body_h = _enc_h - 40;
            var _col1_w = 400;

            // LEFT COLUMN: SUIT DIRECTORY LIST
            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_fx_pan, _body_y, _fx_pan + _col1_w, _body_y + _body_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_fx_pan, _body_y, _fx_pan + _col1_w, _body_y + _body_h, true);

            // Scroll Bar / Navigation Header
            draw_set_color(make_color_rgb(100, 220, 255));
            draw_text(_fx_pan + 12, _body_y + 10, "MOBILE SUIT DIRECTORY (" + string(array_length(_matching_suits)) + " MATCHES):");

            var _up_hov = (_mx >= _fx_pan + _col1_w - 70 && _mx <= _fx_pan + _col1_w - 40 && _my >= _body_y + 6 && _my <= _body_y + 26);
            if (_up_hov && _click) catalog_scroll_offset = max(0, catalog_scroll_offset - 1);
            scr_draw_snes_button(_fx_pan + _col1_w - 70, _body_y + 6, 26, 20, "^", _up_hov, false);

            var _dn_hov = (_mx >= _fx_pan + _col1_w - 36 && _mx <= _col1_w + _fx_pan - 6 && _my >= _body_y + 6 && _my <= _body_y + 26);
            if (_dn_hov && _click) catalog_scroll_offset = min(max(0, array_length(_matching_suits) - 8), catalog_scroll_offset + 1);
            scr_draw_snes_button(_fx_pan + _col1_w - 36, _body_y + 6, 26, 20, "v", _dn_hov, false);

            // Render visible suits (8 rows)
            var _row_h = 56;
            for (var ri = 0; ri < 8; ri++) {
                var _idx = catalog_scroll_offset + ri;
                if (_idx >= array_length(_matching_suits)) break;
                var _st = _matching_suits[_idx];
                var _ry = _body_y + 34 + ri * (_row_h + 4);
                var _is_cur_sel = (catalog_selected_suit_id == _st.id);
                var _r_hov = (_mx >= _fx_pan + 8 && _mx <= _fx_pan + _col1_w - 8 && _my >= _ry && _my <= _ry + _row_h);
                if (_r_hov && _click) catalog_selected_suit_id = _st.id;

                draw_set_color(_is_cur_sel ? make_color_rgb(24, 48, 76) : (_r_hov ? make_color_rgb(18, 30, 44) : make_color_rgb(14, 20, 28)));
                draw_rectangle(_fx_pan + 8, _ry, _fx_pan + _col1_w - 8, _ry + _row_h, false);
                draw_set_color(_is_cur_sel ? make_color_rgb(255, 215, 80) : make_color_rgb(35, 55, 80));
                draw_rectangle(_fx_pan + 8, _ry, _fx_pan + _col1_w - 8, _ry + _row_h, true);

                draw_set_color(_is_cur_sel ? c_white : make_color_rgb(220, 230, 240));
                draw_text(_fx_pan + 14, _ry + 6, _st.name);

                var _era_num = _st[$ "era"] ?? 1;
                draw_set_color(make_color_rgb(140, 180, 220));
                draw_text(_fx_pan + 14, _ry + 24, "ERA " + string(_era_num) + " // " + string(_st[$ "chassis_class"] ?? "Combat"));

                if (_st[$ "mass_production_line"] ?? false) {
                    draw_set_color(make_color_rgb(255, 180, 50));
                    draw_text(_fx_pan + 14, _ry + 40, "[MASS-PRODUCTION LINE]");
                } else {
                    draw_set_color(make_color_rgb(100, 240, 160));
                    draw_text(_fx_pan + 14, _ry + 40, "Rating: " + string(_st[$ "combat"] ?? 450) + " PTS | " + string(_st[$ "armor"] ?? 2000) + " HP");
                }
            }

            // RIGHT COLUMN: LIVE CAD CHAMBER & TELEMETRY
            var _col2_x = _fx_pan + _col1_w + 16;
            var _col2_w = _enc_w - _col1_w - 16;
            var _active_suit = (instance_exists(obj_GameManager) ? obj_GameManager.get_mobile_suit(catalog_selected_suit_id) : undefined);

            draw_set_color(make_color_rgb(10, 16, 24));
            draw_rectangle(_col2_x, _body_y, _col2_x + _col2_w, _body_y + _body_h, false);
            draw_set_color(make_color_rgb(35, 60, 90));
            draw_rectangle(_col2_x, _body_y, _col2_x + _col2_w, _body_y + _body_h, true);

            if (!is_undefined(_active_suit)) {
                // CAD Viewport Enclosure (Top of Right Deck)
                var _cad_x = _col2_x + 12;
                var _cad_y = _body_y + 12;
                var _cad_w = _col2_w - 24;
                var _cad_h = 240;

                draw_set_color(make_color_rgb(6, 10, 16));
                draw_rectangle(_cad_x, _cad_y, _cad_x + _cad_w, _cad_y + _cad_h, false);
                draw_set_color(make_color_rgb(25, 45, 70));
                draw_rectangle(_cad_x, _cad_y, _cad_x + _cad_w, _cad_y + _cad_h, true);

                // Technical Grid Lines
                draw_set_color(make_color_rgb(14, 24, 38));
                for (var gx = _cad_x + 30; gx < _cad_x + _cad_w; gx += 40) draw_line(gx, _cad_y, gx, _cad_y + _cad_h);
                for (var gy = _cad_y + 30; gy < _cad_y + _cad_h; gy += 40) draw_line(_cad_x, gy, _cad_x + _cad_w, gy);

                draw_set_color(make_color_rgb(80, 180, 240));
                draw_text(_cad_x + 12, _cad_y + 8, "CAD TELEMETRY // CHASSIS: " + string_upper(_active_suit.name));

                // Render Live Mobile Suit with Universal Animator Script
                var _cad_cx = _cad_x + _cad_w / 2;
                var _cad_cy = _cad_y + _cad_h - 25;
                scr_draw_animated_mobile_suit(_active_suit.id, _cad_cx, _cad_cy, 1.1, catalog_facing, catalog_anim_state);

                // Animation Mode Toolbar (Bottom of CAD Chamber)
                var _ctrl_btns = [
                    { id: "idle", label: "IDLE" },
                    { id: "walk", label: "STRIDE" },
                    { id: "fire", label: "FIRE WEAPON" },
                    { id: "hit", label: "HIT DEFLECT" }
                ];
                var _cb_w = 95;
                for (var cbi = 0; cbi < 4; cbi++) {
                    var _cbx = _cad_x + 12 + cbi * (_cb_w + 6);
                    var _cby = _cad_y + _cad_h - 32;
                    var _cb_act = (catalog_anim_state == _ctrl_btns[cbi].id);
                    var _cb_hov = (_mx >= _cbx && _mx <= _cbx + _cb_w && _my >= _cby && _my <= _cby + 24);
                    if (_cb_hov && _click) catalog_anim_state = _ctrl_btns[cbi].id;
                    scr_draw_snes_button(_cbx, _cby, _cb_w, 24, _ctrl_btns[cbi].label, _cb_hov, _cb_act);
                }

                // Flip Facing Button
                var _flip_x = _cad_x + _cad_w - 110;
                var _flip_y = _cad_y + _cad_h - 32;
                var _flip_hov = (_mx >= _flip_x && _mx <= _flip_x + 98 && _my >= _flip_y && _my <= _flip_y + 24);
                if (_flip_hov && _click) catalog_facing = -catalog_facing;
                scr_draw_snes_button(_flip_x, _flip_y, 98, 24, catalog_facing == 1 ? "FACE >" : "< FACE", _flip_hov, false);

                // Specs Readout (Lower Half of Right Deck)
                var _spec_y = _cad_y + _cad_h + 14;
                draw_set_color(make_color_rgb(255, 215, 80));
                draw_text(_col2_x + 14, _spec_y, _active_suit.name + " [" + string(_active_suit[$ "short_name"] ?? "") + "]");
                draw_set_color(make_color_rgb(160, 200, 230));
                draw_text(_col2_x + 14, _spec_y + 18, "Manufacturer: " + string(_active_suit[$ "manufacturer"] ?? "Classified") + " | Doctrine: " + string(_active_suit[$ "doctrine"] ?? "Tactical"));

                // 4 Telemetry Gauges
                var _stat_rows = [
                    { label: "Armor Integrity", val: _active_suit[$ "armor"] ?? 2000, max_v: 5500, unit: " HP", col: c_lime },
                    { label: "Reactor Power", val: _active_suit[$ "power"] ?? 14, max_v: 30, unit: " MW", col: make_color_rgb(80, 220, 255) },
                    { label: "Max Speed", val: _active_suit[$ "speed"] ?? 65, max_v: 120, unit: " kph", col: make_color_rgb(255, 180, 50) },
                    { label: "Combat Rating", val: _active_suit[$ "combat"] ?? 500, max_v: 900, unit: " PTS", col: make_color_rgb(220, 100, 255) }
                ];
                for (var si = 0; si < 4; si++) {
                    var _sr = _stat_rows[si];
                    var _sry = _spec_y + 42 + si * 22;
                    draw_set_color(make_color_rgb(180, 200, 220));
                    draw_text(_col2_x + 14, _sry, _sr.label + ":");
                    draw_set_color(_sr.col);
                    draw_text(_col2_x + 140, _sry, string(_sr.val) + _sr.unit);
                    scr_draw_snes_gauge(_col2_x + 230, _sry + 2, 240, 10, _sr.val, _sr.max_v, _sr.col);
                }

                // Armament & Alloy
                var _eq_y = _spec_y + 135;
                draw_set_color(make_color_rgb(100, 220, 255));
                draw_text(_col2_x + 14, _eq_y, "PRIMARY WEAPON: " + string(_active_suit[$ "primary_weapon"] ?? "None"));
                draw_text(_col2_x + 14, _eq_y + 18, "SECONDARY: " + string(_active_suit[$ "secondary_weapon"] ?? "None"));
                draw_text(_col2_x + 14, _eq_y + 36, "FEATURE: " + string(_active_suit[$ "signature_feature"] ?? "Standard"));
                draw_set_color(make_color_rgb(240, 210, 80));
                draw_text(_col2_x + 14, _eq_y + 54, "ALLOY MATRIX: " + string(_active_suit[$ "alloy_type"] ?? "Standard"));

                // Historical Lore Dossier
                var _lore_y = _eq_y + 76;
                draw_set_color(make_color_rgb(12, 18, 28));
                draw_rectangle(_col2_x + 12, _lore_y, _col2_x + _col2_w - 12, _body_y + _body_h - 12, false);
                draw_set_color(make_color_rgb(35, 55, 80));
                draw_rectangle(_col2_x + 12, _lore_y, _col2_x + _col2_w - 12, _body_y + _body_h - 12, true);
                draw_set_color(make_color_rgb(200, 220, 240));
                draw_text_ext(_col2_x + 18, _lore_y + 8, string(_active_suit[$ "lore"] ?? "No classified records available."), 16, _col2_w - 36);
            }
        }
        // =========================================================================
        // BRANCH B: FACTION DOSSIERS & STRATEGIC CITADELS (STANDARD VIEW)
        // =========================================================================
        else {
            // Left Card: Faction Standing & Military Mech Representative
            var _col1_w = 340;"""

assert old_faction_tabs in text, "Could not find old_faction_tabs"
text = text.replace(old_faction_tabs, new_faction_tabs)

# -----------------------------------------------------------------------------
# 4. Close Branch B at the end of war_subtab == 1
# -----------------------------------------------------------------------------
old_subtab_2_marker = """            draw_text(_col2_x + 20, _by + 66, "• [EARTH] Atacama Quantum Data Vault (Chile) - Subterranean computing vault training predictive combat AI");
        }
    }

    // =====================================================================
    // SUBTAB 2: FACTION AI DIPLOMACY, ALLIANCES & WAR ROOM MATRIX (DOC 21)
    // ====================================================================="""

new_subtab_2_marker = """            draw_text(_col2_x + 20, _by + 66, "• [EARTH] Atacama Quantum Data Vault (Chile) - Subterranean computing vault training predictive combat AI");
        }
        } // End Branch B else
    }

    // =====================================================================
    // SUBTAB 2: FACTION AI DIPLOMACY, ALLIANCES & WAR ROOM MATRIX (DOC 21)
    // ====================================================================="""

assert old_subtab_2_marker in text, "Could not find old_subtab_2_marker"
text = text.replace(old_subtab_2_marker, new_subtab_2_marker)

# -----------------------------------------------------------------------------
# 5. In Faction Dossier view, render active mass production line suit animated!
# -----------------------------------------------------------------------------
old_standing_mech = """        // Standing Mobile Suit Artwork
        var _unit_spr = (selected_faction_dossier == "faction_terran") ? spr_mech_terran_ironclad : ((selected_faction_dossier == "faction_colony") ? spr_mech_colony_aether : ((selected_faction_dossier == "faction_syndicate") ? spr_mech_syndicate_hyena : spr_mech_zaibatsu_muramasa));
        if (sprite_exists(_unit_spr)) {
            draw_sprite_ext(_unit_spr, 0, _fx_pan + _col1_w / 2, _d_y + 390, 0.72, 0.72, 0, c_white, 0.95);
        }"""

new_standing_mech = """        // Standing Mobile Suit Artwork & Active Playthrough Mass-Production Line (docs/29 & docs/30)
        var _active_mp_id = "ms_terran_ironclad_07";
        var _active_mp_name = "GHA-07 Ironclad";
        if (instance_exists(obj_FactionManager) && variable_struct_exists(obj_FactionManager.mass_production_contracts, _fid_curr)) {
            var _active_cnt = obj_FactionManager.mass_production_contracts[$ _fid_curr];
            _active_mp_id = _active_cnt.baseline_suit_id;
            _active_mp_name = _active_cnt.baseline_suit_name;
        }

        draw_set_color(make_color_rgb(255, 215, 80));
        draw_text(_fx_pan + 16, _d_y + 80, "[ACTIVE LINE: " + _active_mp_name + "]");

        // Render animated 160x160 active mass production suit with thruster pulse and idle breathing
        scr_draw_animated_mobile_suit(_active_mp_id, _fx_pan + _col1_w / 2, _d_y + 360, 0.90, 1, "idle");"""

assert old_standing_mech in text, "Could not find old_standing_mech"
text = text.replace(old_standing_mech, new_standing_mech)

with open("objects/obj_HQTerminal/Draw_64.gml", "w") as f:
    f.write(text)

print("Successfully injected all features into objects/obj_HQTerminal/Draw_64.gml!")
