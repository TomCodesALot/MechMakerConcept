with open('objects/obj_BattleManager/Draw_64.gml', 'r') as f:
    text = f.read()

old_col3_start = '    // COLUMN 3: THEATER MAP SELECTION & LAUNCH (x: _deck_x + 900, w: 380)'
old_col3_end = '    scr_draw_snes_button(_lnch_x, _lnch_y, _lnch_w, _lnch_h, ">> DEPLOY TO BATTLEFIELD <<", _lnch_hov, false, make_color_rgb(80, 255, 140));\n}'

idx1 = text.find(old_col3_start)
idx2 = text.find(old_col3_end)
assert idx1 != -1 and idx2 != -1, f"Markers not found: idx1={idx1}, idx2={idx2}"

new_col3 = """    // COLUMN 3: THEATER MAP SELECTION & LAUNCH (x: _deck_x + 900, w: 380)
    var _col3_x = _deck_x + 900;
    var _col3_y = _deck_y + 45;
    var _col3_w = _deck_w - 920;

    draw_set_color(make_color_rgb(100, 220, 255));
    draw_text(_col3_x, _col3_y, "OPERATIONAL THEATER SELECTION (24 MAPS):");

    // Category Filter Tabs
    var _filter_tabs = [
        { label: "ALL (24)", key: "ALL", w: 86 },
        { label: "EARTH (10)", key: "EARTH", w: 90 },
        { label: "SPACE (10)", key: "SPACE", w: 90 },
        { label: "TEST (4)", key: "TEST", w: 86 }
    ];
    var _cur_tab_x = _col3_x;
    var _tab_y = _col3_y + 20;
    for (var t = 0; t < array_length(_filter_tabs); t++) {
        var _ft = _filter_tabs[t];
        var _thov = (_mx >= _cur_tab_x && _mx <= _cur_tab_x + _ft.w && _my >= _tab_y && _my <= _tab_y + 22);
        var _tsel = (deployment_map_filter == _ft.key);
        if (_thov && _click) {
            deployment_map_filter = _ft.key;
            deployment_map_page = 0;
        }
        scr_draw_snes_button(_cur_tab_x, _tab_y, _ft.w, 22, _ft.label, _thov, _tsel, make_color_rgb(100, 220, 255));
        _cur_tab_x += _ft.w + 6;
    }

    // Filter maps array
    var _filtered_maps = [];
    for (var m = 0; m < array_length(map_definitions); m++) {
        var _md = map_definitions[m];
        if (deployment_map_filter == "ALL" || _md.category == deployment_map_filter) {
            array_push(_filtered_maps, _md);
        }
    }

    var _total_maps = array_length(_filtered_maps);
    var _total_pages = max(1, ceil(_total_maps / 4));
    deployment_map_page = clamp(deployment_map_page, 0, _total_pages - 1);

    // Pagination Controls Bar
    var _pg_y = _col3_y + 46;
    var _p_prev_hov = (_mx >= _col3_x && _mx <= _col3_x + 75 && _my >= _pg_y && _my <= _pg_y + 22);
    if (_p_prev_hov && _click && deployment_map_page > 0) {
        deployment_map_page--;
    }
    scr_draw_snes_button(_col3_x, _pg_y, 75, 22, "< PREV", _p_prev_hov, false, make_color_rgb(100, 220, 255));

    var _p_next_hov = (_mx >= _col3_x + _col3_w - 75 && _mx <= _col3_x + _col3_w && _my >= _pg_y && _my <= _pg_y + 22);
    if (_p_next_hov && _click && deployment_map_page < _total_pages - 1) {
        deployment_map_page++;
    }
    scr_draw_snes_button(_col3_x + _col3_w - 75, _pg_y, 75, 22, "NEXT >", _p_next_hov, false, make_color_rgb(100, 220, 255));

    draw_set_color(make_color_rgb(255, 215, 100));
    draw_text(_col3_x + 95, _pg_y + 3, "PAGE " + string(deployment_map_page + 1) + " / " + string(_total_pages) + " (" + string(_total_maps) + " THEATERS)");

    // Render 4 Map Cards for Current Page
    var _start_idx = deployment_map_page * 4;
    for (var i = 0; i < 4; i++) {
        var _idx = _start_idx + i;
        if (_idx >= _total_maps) break;
        var _md = _filtered_maps[_idx];
        var _my_card = _col3_y + 74 + (i * 112);
        var _mh_card = 106;
        var _m_hov = (_mx >= _col3_x && _mx <= _col3_x + _col3_w && _my >= _my_card && _my <= _my_card + _mh_card);
        var _m_sel = (current_map_id == _md.id);

        if (_m_hov && _click) {
            load_map(_md.id);
        }

        draw_set_color(_m_sel ? make_color_rgb(24, 46, 68) : (_m_hov ? make_color_rgb(16, 26, 38) : make_color_rgb(10, 16, 24)));
        draw_rectangle(_col3_x, _my_card, _col3_x + _col3_w, _my_card + _mh_card, false);
        draw_set_color(_m_sel ? make_color_rgb(80, 220, 255) : make_color_rgb(40, 60, 85));
        draw_rectangle(_col3_x, _my_card, _col3_x + _col3_w, _my_card + _mh_card, true);

        draw_set_color(_m_sel ? make_color_rgb(100, 240, 255) : c_white);
        draw_text(_col3_x + 10, _my_card + 6, "MAP " + string(_md.id + 1) + ": " + _md.name);

        draw_set_color(make_color_rgb(255, 200, 80));
        draw_text(_col3_x + 10, _my_card + 24, "THEATER: " + _md.theater + " [" + _md.category + "] | GRAV: " + string(_md.gravity) + "G");

        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text_ext(_col3_x + 10, _my_card + 42, _md.desc, 16, _col3_w - 20);

        draw_set_color(make_color_rgb(80, 220, 140));
        draw_text(_col3_x + 10, _my_card + 84, _md.ambient_tag);
    }

    // Deploy / Launch Button
    var _lnch_x = _col3_x;
    var _lnch_y = _col3_y + 530;
    var _lnch_w = _col3_w;
    var _lnch_h = 60;
    var _lnch_hov = (_mx >= _lnch_x && _mx <= _lnch_x + _lnch_w && _my >= _lnch_y && _my <= _lnch_y + _lnch_h);
    if (_lnch_hov && _click) {
        deployment_deck_active = false;
        state = COMBAT_STATE.PLAYER_PHASE;
        select_unit(0);
        add_log("[DEPLOYMENT COMPLETE] Battlegroup deployed to " + map_definitions[current_map_id].name);
    }
    scr_draw_snes_button(_lnch_x, _lnch_y, _lnch_w, _lnch_h, ">> DEPLOY TO BATTLEFIELD <<", _lnch_hov, false, make_color_rgb(80, 255, 140));
}"""

new_text = text[:idx1] + new_col3 + text[idx2 + len(old_col3_end):]

with open('objects/obj_BattleManager/Draw_64.gml', 'w') as f:
    f.write(new_text)

print("Updated Draw_64.gml with 24-map filter & pagination controls!")
