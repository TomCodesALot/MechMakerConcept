#!/usr/bin/env python3
"""
Patch obj_DebugManager/Draw_64.gml to add:
- Tab 1: MECH BUILDER & FORGE (Modular hardpoints, CAD preview, telemetry, direct test deploy)
- Tab 2: ASTEROID MINING & EXTRACTION (Planetary nodes, pulse drill HUD, smelting crucible, pirate raid testing)
- Tab 3: CAMPAIGN CHEATS & TOOLS (The existing cheats quadrant menu)
"""
import os
import re

DRAW_PATH = "objects/obj_DebugManager/Draw_64.gml"
with open(DRAW_PATH) as f:
    content = f.read()

# 1. Update Header Tabs
old_header = """// Tab Buttons
var _t0_hov = (_mx >= _win_x + 760 && _mx <= _win_x + 970 && _my >= _win_y + 8 && _my <= _win_y + 36);
if (_t0_hov && _click) {
    active_debug_tab = 0;
    scr_audio_play_ui("tab");
}
scr_draw_snes_button(_win_x + 760, _win_y + 8, 210, 28, "1. BATTLE & ANIMATION LAB", _t0_hov || (active_debug_tab == 0), (active_debug_tab == 0), (active_debug_tab == 0) ? make_color_rgb(0, 240, 255) : c_white);

var _t1_hov = (_mx >= _win_x + 980 && _mx <= _win_x + 1190 && _my >= _win_y + 8 && _my <= _win_y + 36);
if (_t1_hov && _click) {
    active_debug_tab = 1;
    scr_audio_play_ui("tab");
}
scr_draw_snes_button(_win_x + 980, _win_y + 8, 210, 28, "2. CAMPAIGN CHEATS & TOOLS", _t1_hov || (active_debug_tab == 1), (active_debug_tab == 1), (active_debug_tab == 1) ? make_color_rgb(0, 240, 255) : c_white);"""

new_header = """// 4 Universal Testing Tabs (Combat, Mech Builder, Mining, Cheats)
var _tab_w = 230;
var _tab_h = 28;

var _t0_x = _win_x + 210;
var _t0_hov = (_mx >= _t0_x && _mx <= _t0_x + _tab_w && _my >= _win_y + 8 && _my <= _win_y + 8 + _tab_h);
if (_t0_hov && _click) { active_debug_tab = 0; scr_audio_play_ui("tab"); }
scr_draw_snes_button(_t0_x, _win_y + 8, _tab_w, _tab_h, "1. COMBAT PROVING LAB", _t0_hov || (active_debug_tab == 0), (active_debug_tab == 0), (active_debug_tab == 0) ? make_color_rgb(0, 240, 255) : c_white);

var _t1_x = _t0_x + _tab_w + 10;
var _t1_hov = (_mx >= _t1_x && _mx <= _t1_x + _tab_w && _my >= _win_y + 8 && _my <= _win_y + 8 + _tab_h);
if (_t1_hov && _click) { active_debug_tab = 1; scr_audio_play_ui("tab"); }
scr_draw_snes_button(_t1_x, _win_y + 8, _tab_w, _tab_h, "2. MECH BUILDER & FORGE", _t1_hov || (active_debug_tab == 1), (active_debug_tab == 1), (active_debug_tab == 1) ? make_color_rgb(0, 240, 255) : c_white);

var _t2_x = _t1_x + _tab_w + 10;
var _t2_hov = (_mx >= _t2_x && _mx <= _t2_x + _tab_w && _my >= _win_y + 8 && _my <= _win_y + 8 + _tab_h);
if (_t2_hov && _click) { active_debug_tab = 2; scr_audio_play_ui("tab"); }
scr_draw_snes_button(_t2_x, _win_y + 8, _tab_w, _tab_h, "3. ASTEROID MINING & DRILL", _t2_hov || (active_debug_tab == 2), (active_debug_tab == 2), (active_debug_tab == 2) ? make_color_rgb(0, 240, 255) : c_white);

var _t3_x = _t2_x + _tab_w + 10;
var _t3_hov = (_mx >= _t3_x && _mx <= _t3_x + _tab_w && _my >= _win_y + 8 && _my <= _win_y + 8 + _tab_h);
if (_t3_hov && _click) { active_debug_tab = 3; scr_audio_play_ui("tab"); }
scr_draw_snes_button(_t3_x, _win_y + 8, _tab_w, _tab_h, "4. CAMPAIGN CHEATS", _t3_hov || (active_debug_tab == 3), (active_debug_tab == 3), (active_debug_tab == 3) ? make_color_rgb(0, 240, 255) : c_white);"""

assert old_header in content, "Could not find old_header in Draw_64.gml"
content = content.replace(old_header, new_header)

# Header Title change to fit tabs
content = content.replace('"PMC DEBUG CONSOLE // COMBAT & ANIMATION ENGINE PROVING GROUND"', '"PMC DEBUG HUB // [F7]"')

# 2. Add Tab 1 (Mech Builder) and Tab 2 (Mining) before existing Tab 1
tab1_and_tab2_code = '''
// =========================================================================
// TAB 1: MECH BUILDER & MODULAR FORGE ENGINEERING DECK
// =========================================================================
else if (active_debug_tab == 1) {
    var _col1_x = _win_x + 14;
    var _col1_y = _win_y + 44;
    var _col1_w = 410;
    var _col1_h = 654;
    scr_draw_snes_panel(_col1_x, _col1_y, _col1_w, _col1_h, "MODULAR HARDPOINTS & SOCKETS", make_color_rgb(0, 240, 255), true, 0.03);

    var _t = calculate_builder_telemetry();

    // 6 Sockets + Alloy Selector
    var _slots_info = [
        { name: "SLOT 1: HEAD SENSORS", part: _t.head, list: builder_parts_catalog.heads, idx: builder_head_idx, key: "head" },
        { name: "SLOT 2: TORSO REACTOR", part: _t.torso, list: builder_parts_catalog.torsos, idx: builder_torso_idx, key: "torso" },
        { name: "SLOT 3: ARMS & ACTUATORS", part: _t.arms, list: builder_parts_catalog.arms, idx: builder_arms_idx, key: "arms" },
        { name: "SLOT 4: LEGS & HYDRAULICS", part: _t.legs, list: builder_parts_catalog.legs, idx: builder_legs_idx, key: "legs" },
        { name: "SLOT 5: BACKPACK BOOSTERS", part: _t.backpack, list: builder_parts_catalog.backpacks, idx: builder_bp_idx, key: "backpack" },
        { name: "SLOT 6: PRIMARY WEAPON", part: _t.weapon, list: builder_parts_catalog.weapons, idx: builder_wp_idx, key: "weapon" },
        { name: "SLOT 7: SINTERED ARMOR ALLOY", part: undefined, list: builder_alloys, idx: builder_alloy_idx, key: "alloy" }
    ];

    var _slot_h = 68;
    for (var s = 0; s < 7; s++) {
        var _s_info = _slots_info[s];
        var _sy = _col1_y + 22 + (s * _slot_h);
        var _is_cur_slot = (builder_selected_slot == s);

        // Slot Background Card
        var _scard_hov = (_mx >= _col1_x + 12 && _mx <= _col1_x + _col1_w - 12 && _my >= _sy && _my <= _sy + _slot_h - 4);
        if (_scard_hov && _click) {
            builder_selected_slot = s;
        }

        draw_set_color(_is_cur_slot ? make_color_rgb(20, 36, 56) : (_scard_hov ? make_color_rgb(16, 26, 42) : make_color_rgb(10, 16, 26)));
        draw_rectangle(_col1_x + 12, _sy, _col1_x + _col1_w - 12, _sy + _slot_h - 6, false);
        draw_set_color(_is_cur_slot ? make_color_rgb(0, 240, 255) : make_color_rgb(40, 65, 95));
        draw_rectangle(_col1_x + 12, _sy, _col1_x + _col1_w - 12, _sy + _slot_h - 6, true);

        // Header Title
        draw_set_color(_is_cur_slot ? make_color_rgb(255, 220, 80) : make_color_rgb(100, 200, 255));
        draw_text(_col1_x + 20, _sy + 4, (_is_cur_slot ? "> " : "") + _s_info.name);

        // Prev & Next Buttons
        var _pbtn_hov = (_mx >= _col1_x + _col1_w - 74 && _mx <= _col1_x + _col1_w - 44 && _my >= _sy + 4 && _my <= _sy + 26);
        var _nbtn_hov = (_mx >= _col1_x + _col1_w - 40 && _mx <= _col1_x + _col1_w - 14 && _my >= _sy + 4 && _my <= _sy + 26);

        if (_pbtn_hov && _click) {
            if (s == 0) builder_head_idx = (builder_head_idx - 1 + array_length(builder_parts_catalog.heads)) % array_length(builder_parts_catalog.heads);
            else if (s == 1) builder_torso_idx = (builder_torso_idx - 1 + array_length(builder_parts_catalog.torsos)) % array_length(builder_parts_catalog.torsos);
            else if (s == 2) builder_arms_idx = (builder_arms_idx - 1 + array_length(builder_parts_catalog.arms)) % array_length(builder_parts_catalog.arms);
            else if (s == 3) builder_legs_idx = (builder_legs_idx - 1 + array_length(builder_parts_catalog.legs)) % array_length(builder_parts_catalog.legs);
            else if (s == 4) builder_bp_idx = (builder_bp_idx - 1 + array_length(builder_parts_catalog.backpacks)) % array_length(builder_parts_catalog.backpacks);
            else if (s == 5) builder_wp_idx = (builder_wp_idx - 1 + array_length(builder_parts_catalog.weapons)) % array_length(builder_parts_catalog.weapons);
            else if (s == 6) builder_alloy_idx = (builder_alloy_idx - 1 + array_length(builder_alloys)) % array_length(builder_alloys);
            scr_audio_play_ui("click");
        }
        if (_nbtn_hov && _click) {
            if (s == 0) builder_head_idx = (builder_head_idx + 1) % array_length(builder_parts_catalog.heads);
            else if (s == 1) builder_torso_idx = (builder_torso_idx + 1) % array_length(builder_parts_catalog.torsos);
            else if (s == 2) builder_arms_idx = (builder_arms_idx + 1) % array_length(builder_parts_catalog.arms);
            else if (s == 3) builder_legs_idx = (builder_legs_idx + 1) % array_length(builder_parts_catalog.legs);
            else if (s == 4) builder_bp_idx = (builder_bp_idx + 1) % array_length(builder_parts_catalog.backpacks);
            else if (s == 5) builder_wp_idx = (builder_wp_idx + 1) % array_length(builder_parts_catalog.weapons);
            else if (s == 6) builder_alloy_idx = (builder_alloy_idx + 1) % array_length(builder_alloys);
            scr_audio_play_ui("click");
        }

        scr_draw_snes_button(_col1_x + _col1_w - 74, _sy + 4, 30, 22, "<", _pbtn_hov, false, c_aqua);
        scr_draw_snes_button(_col1_x + _col1_w - 40, _sy + 4, 28, 22, ">", _nbtn_hov, false, c_aqua);

        // Part Details
        if (s < 6) {
            var _p = _s_info.part;
            draw_set_color(c_white);
            draw_text(_col1_x + 20, _sy + 22, _p.name);

            draw_set_color(make_color_rgb(160, 190, 220));
            var _stat_str = "HP: " + string(_p.armor) + " | " + string(_p.mass) + "t";
            if (variable_struct_exists(_p, "power_output")) _stat_str += " | Core: +" + string(_p.power_output) + " MW";
            else if (variable_struct_exists(_p, "power_draw")) _stat_str += " | Draw: -" + string(_p.power_draw) + " MW";
            if (variable_struct_exists(_p, "damage")) _stat_str += " | Dmg: " + string(_p.damage);
            draw_text(_col1_x + 20, _sy + 40, _stat_str);

            draw_set_color(make_color_rgb(255, 200, 80));
            draw_text(_col1_x + 230, _sy + 40, _p.bonus);
        } else {
            draw_set_color(c_white);
            draw_text(_col1_x + 20, _sy + 22, builder_alloy_names[builder_alloy_idx]);
            draw_set_color(make_color_rgb(160, 190, 220));
            draw_text(_col1_x + 20, _sy + 40, "Material Class: Molecular Sintered Crucible Matrix");
        }
    }

    // Quick Presets Row
    var _preset_y = _col1_y + _col1_h - 150;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col1_x + 14, _preset_y, "QUICK PROTOTYPE PRESETS:");

    var _p_labels = ["[GENESIS]", "[STRIKER]", "[FORTRESS]", "[SCAVENGER]", "[RANDOM]"];
    var _p_keys = ["GENESIS", "STRIKER", "FORTRESS", "SCAVENGER", "RANDOM"];
    for (var p = 0; p < array_length(_p_labels); p++) {
        var _px = _col1_x + 14 + (p * 76);
        var _phov = (_mx >= _px && _mx <= _px + 72 && _my >= _preset_y + 20 && _my <= _preset_y + 48);
        if (_phov && _click) {
            apply_builder_preset(_p_keys[p]);
        }
        scr_draw_snes_button(_px, _preset_y + 20, 72, 28, _p_labels[p], _phov, false, make_color_rgb(100, 220, 255));
    }

    // ---------------------------------------------------------------------
    // B. CENTER COLUMN: ISOMETRIC CAD PREVIEW & STANCE TESTER (w: 430)
    // ---------------------------------------------------------------------
    var _col2_x = _col1_x + _col1_w + 12;
    var _col2_y = _win_y + 44;
    var _col2_w = 430;
    var _col2_h = 654;
    scr_draw_snes_panel(_col2_x, _col2_y, _col2_w, _col2_h, "ISOMETRIC CAD VISUALIZER", make_color_rgb(0, 240, 255), true, 0.03);

    // CAD Wireframe Grid
    var _cad_cx = _col2_x + (_col2_w / 2);
    var _cad_cy = _col2_y + 210;
    draw_set_color(make_color_rgb(12, 28, 48));
    draw_rectangle(_col2_x + 16, _col2_y + 30, _col2_x + _col2_w - 16, _col2_y + 400, false);
    draw_set_color(make_color_rgb(25, 55, 90));
    draw_rectangle(_col2_x + 16, _col2_y + 30, _col2_x + _col2_w - 16, _col2_y + 400, true);

    // Crosshair & concentric rings
    draw_set_color(make_color_rgb(18, 48, 80));
    draw_line(_cad_cx - 180, _cad_cy, _cad_cx + 180, _cad_cy);
    draw_line(_cad_cx, _cad_cy - 160, _cad_cx, _cad_cy + 160);
    draw_circle(_cad_cx, _cad_cy, 120, true);
    draw_circle(_cad_cx, _cad_cy, 60, true);

    // Render Assembled Mobile Suit
    var _draw_spr = _t.preview_sprite;
    if (builder_anim_state == "fire") _draw_spr = _t.weapon.sprite;
    else if (builder_anim_state == "melee") _draw_spr = spr_ms_aether_attack_saber;
    else if (builder_anim_state == "boost") _draw_spr = spr_ms_aether_boost;

    if (sprite_exists(_draw_spr)) {
        var _sub = floor(builder_subimg) % sprite_get_number(_draw_spr);
        draw_sprite_ext(_draw_spr, _sub, _cad_cx, _cad_cy + 30, builder_preview_scale, builder_preview_scale, 0, c_white, 1.0);
    }

    // Reticle Scan Line
    var _scan_y = _col2_y + 30 + ((current_time / 18.0) % 370);
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_set_alpha(0.35);
    draw_line(_col2_x + 16, _scan_y, _col2_x + _col2_w - 16, _scan_y);
    draw_set_alpha(1.0);

    // Stance Buttons Row
    var _st_y = _col2_y + 414;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col2_x + 18, _st_y, "TEST ACTION STANCE:");

    var _stances = ["idle", "boost", "fire", "melee"];
    var _st_names = ["IDLE", "BOOST", "FIRE", "MELEE"];
    for (var st = 0; st < 4; st++) {
        var _stx = _col2_x + 18 + (st * 98);
        var _st_hov = (_mx >= _stx && _mx <= _stx + 92 && _my >= _st_y + 20 && _my <= _st_y + 50);
        var _st_act = (builder_anim_state == _stances[st]);
        if (_st_hov && _click) {
            builder_anim_state = _stances[st];
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_stx, _st_y + 20, 92, 30, _st_names[st], _st_hov || _st_act, _st_act, _st_act ? make_color_rgb(0, 240, 255) : c_white);
    }

    // Callsign Display & Auto-Tune Button
    var _tune_y = _col2_y + 490;
    draw_set_color(make_color_rgb(140, 170, 200));
    draw_text(_col2_x + 18, _tune_y, "CUSTOM CALLSIGN:");
    draw_set_color(make_color_rgb(255, 220, 80));
    draw_text(_col2_x + 160, _tune_y, builder_custom_name);

    var _at_hov = (_mx >= _col2_x + 18 && _mx <= _col2_x + _col2_w - 18 && _my >= _tune_y + 28 && _my <= _tune_y + 64);
    if (_at_hov && _click) {
        if (instance_exists(obj_BlueprintManager)) {
            obj_BlueprintManager.auto_tune_prototype();
            scr_audio_play_ui("boot");
        }
    }
    scr_draw_snes_button(_col2_x + 18, _tune_y + 28, _col2_w - 36, 36, ">> AUTO-TUNE PROTOTYPE MASTERWORK <<", _at_hov, true, make_color_rgb(255, 200, 50));

    // ---------------------------------------------------------------------
    // C. RIGHT COLUMN: ENGINEERING TELEMETRY & ROLLOUT (w: 410)
    // ---------------------------------------------------------------------
    var _col3_x = _col2_x + _col2_w + 12;
    var _col3_y = _win_y + 44;
    var _col3_w = 410;
    var _col3_h = 654;
    scr_draw_snes_panel(_col3_x, _col3_y, _col3_w, _col3_h, "ENGINEERING TELEMETRY & ROLLOUT", make_color_rgb(0, 240, 255), true, 0.03);

    var _ty = _col3_y + 26;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col3_x + 18, _ty, "ARMOR INTEGRITY:");
    draw_set_color(c_white);
    draw_text(_col3_x + 220, _ty, string(_t.total_armor) + " HP");

    _ty += 24;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col3_x + 18, _ty, "TOTAL CHASSIS MASS:");
    draw_set_color(_t.mass_overloaded ? c_red : c_white);
    draw_text(_col3_x + 220, _ty, string(_t.total_mass) + " t / " + string(floor(_t.max_capacity)) + " t");

    // Mass capacity bar
    _ty += 20;
    draw_set_color(make_color_rgb(20, 30, 45));
    draw_rectangle(_col3_x + 18, _ty, _col3_x + _col3_w - 18, _ty + 10, false);
    var _m_pct = clamp(_t.total_mass / max(1, _t.max_capacity), 0.0, 1.0);
    draw_set_color(_t.mass_overloaded ? c_red : make_color_rgb(0, 240, 255));
    draw_rectangle(_col3_x + 18, _ty, _col3_x + 18 + (_m_pct * (_col3_w - 36)), _ty + 10, false);

    _ty += 20;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col3_x + 18, _ty, "REACTOR OUTPUT BALANCE:");
    draw_set_color(_t.reactor_overloaded ? c_red : c_lime);
    draw_text(_col3_x + 220, _ty, (_t.net_power >= 0 ? "+" : "") + string(_t.net_power) + " MW (Core: " + string(_t.power_output) + ")");

    _ty += 24;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col3_x + 18, _ty, "SPEED & MOBILITY:");
    draw_set_color(c_white);
    draw_text(_col3_x + 220, _ty, string(_t.walk_speed) + " km/h (Boost: " + string(_t.boost_speed) + ")");

    _ty += 24;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col3_x + 18, _ty, "COMBAT RATING (OSS):");
    draw_set_color(make_color_rgb(255, 220, 80));
    draw_text(_col3_x + 220, _ty, string(_t.combat_rating) + " [SUPERIOR]");

    _ty += 24;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col3_x + 18, _ty, "WEIGHT CLASSIFICATION:");
    draw_set_color(c_white);
    draw_text(_col3_x + 220, _ty, _t.weight_class);

    // Overload Warning
    _ty += 34;
    if (_t.reactor_overloaded) {
        draw_set_color(c_red);
        draw_rectangle(_col3_x + 18, _ty, _col3_x + _col3_w - 18, _ty + 30, false);
        draw_set_color(c_white);
        draw_text(_col3_x + 26, _ty + 6, "! WARNING: REACTOR OVERLOAD - NEGATIVE POWER !");
        _ty += 38;
    } else {
        draw_set_color(make_color_rgb(18, 45, 30));
        draw_rectangle(_col3_x + 18, _ty, _col3_x + _col3_w - 18, _ty + 30, false);
        draw_set_color(c_lime);
        draw_text(_col3_x + 26, _ty + 6, "v POWER GRID STABLE // READY FOR COMBAT PROVING");
        _ty += 38;
    }

    // Action Buttons
    _ty += 14;
    var _btn1_hov = (_mx >= _col3_x + 18 && _mx <= _col3_x + _col3_w - 18 && _my >= _ty && _my <= _ty + 44);
    if (_btn1_hov && _click) {
        deploy_builder_mech_to_combat();
    }
    scr_draw_snes_button(_col3_x + 18, _ty, _col3_w - 36, 44, ">>>> DEPLOY TO COMBAT LAB (TAB 0) <<<<", _btn1_hov, true, make_color_rgb(0, 240, 255));

    _ty += 54;
    var _btn2_hov = (_mx >= _col3_x + 18 && _mx <= _col3_x + _col3_w - 18 && _my >= _ty && _my <= _ty + 40);
    if (_btn2_hov && _click) {
        commission_builder_mech_to_hangar();
    }
    scr_draw_snes_button(_col3_x + 18, _ty, _col3_w - 36, 40, "COMMISSION TO FLEET HANGAR", _btn2_hov, false, make_color_rgb(100, 220, 255));

    _ty += 50;
    var _btn3_hov = (_mx >= _col3_x + 18 && _mx <= _col3_x + _col3_w - 18 && _my >= _ty && _my <= _ty + 40);
    if (_btn3_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            var _pts = obj_GameManager.inventory.parts;
            var _slots = ["heads", "torsos", "arms", "legs", "backpacks", "weapons"];
            for (var s = 0; s < array_length(_slots); s++) {
                var _cat_arr = variable_struct_get(builder_parts_catalog, _slots[s]);
                for (var ci = 0; ci < array_length(_cat_arr); ci++) {
                    array_push(variable_struct_get(_pts, _slots[s]), _cat_arr[ci]);
                }
            }
            show_toast("[PARTS FORGED] +36 Modular Components Added to Stockpile!", c_lime);
            scr_audio_play_ui("boot");
        }
    }
    scr_draw_snes_button(_col3_x + 18, _ty, _col3_w - 36, 40, "FORGE SPARE PARTS STOCKPILE (+36 ALL)", _btn3_hov, false, make_color_rgb(255, 200, 80));
}

// =========================================================================
// TAB 2: ASTEROID MINING & PLANETARY EXTRACTION DECK
// =========================================================================
else if (active_debug_tab == 2) {
    var _col1_x = _win_x + 14;
    var _col1_y = _win_y + 44;
    var _col1_w = 410;
    var _col1_h = 654;
    scr_draw_snes_panel(_col1_x, _col1_y, _col1_w, _col1_h, "SOLAR MINING NODES & CLAIMS", make_color_rgb(0, 240, 255), true, 0.03);

    // Sphere Filter Buttons
    var _sph_y = _col1_y + 24;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col1_x + 14, _sph_y, "PLANETARY SPHERE FILTER:");

    _sph_y += 20;
    for (var sp = 0; sp < array_length(mining_spheres); sp++) {
        var _spx = _col1_x + 14 + ((sp % 3) * 128);
        var _spy = _sph_y + (floor(sp / 3) * 30);
        var _sphov = (_mx >= _spx && _mx <= _spx + 120 && _my >= _spy && _my <= _spy + 26);
        var _spact = (mining_sphere_idx == sp);
        if (_sphov && _click) {
            mining_sphere_idx = sp;
            mining_selected_idx = 0;
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_spx, _spy, 120, 26, mining_spheres[sp], _sphov || _spact, _spact, _spact ? make_color_rgb(0, 240, 255) : c_white);
    }

    // Node List
    var _nodes = get_debug_mining_nodes();
    var _nlist_y = _sph_y + 70;
    var _ncard_h = 76;

    for (var ni = 0; ni < min(4, array_length(_nodes)); ni++) {
        var _node = _nodes[ni];
        var _ny = _nlist_y + (ni * _ncard_h);
        var _is_cur_node = (mining_selected_idx == ni);

        var _nhov = (_mx >= _col1_x + 14 && _mx <= _col1_x + _col1_w - 14 && _my >= _ny && _my <= _ny + _ncard_h - 4);
        if (_nhov && _click) {
            mining_selected_idx = ni;
            scr_audio_play_ui("click");
        }

        draw_set_color(_is_cur_node ? make_color_rgb(20, 38, 60) : (_nhov ? make_color_rgb(16, 28, 44) : make_color_rgb(10, 16, 28)));
        draw_rectangle(_col1_x + 14, _ny, _col1_x + _col1_w - 14, _ny + _ncard_h - 6, false);
        draw_set_color(_is_cur_node ? make_color_rgb(0, 240, 255) : make_color_rgb(40, 65, 95));
        draw_rectangle(_col1_x + 14, _ny, _col1_x + _col1_w - 14, _ny + _ncard_h - 6, true);

        draw_set_color(_is_cur_node ? make_color_rgb(255, 220, 80) : make_color_rgb(100, 220, 255));
        draw_text(_col1_x + 20, _ny + 4, (_is_cur_node ? "> " : "") + _node.name);

        draw_set_color(c_white);
        draw_text(_col1_x + 20, _ny + 22, "Body: " + (variable_struct_exists(_node, "sphere") ? _node.sphere : "Asteroid Belt"));

        draw_set_color(make_color_rgb(160, 190, 220));
        draw_text(_col1_x + 20, _ny + 38, "Yield: " + string_upper(string_replace(_node.primary_yield, "mat_", "")) + " (+" + string(_node.yield_rate_primary * 100) + " kg/day)");

        draw_set_color((_node.status == "ACTIVE_MINING") ? c_lime : make_color_rgb(255, 140, 40));
        draw_text(_col1_x + 230, _ny + 38, "[" + _node.status + "]");

        draw_set_color(make_color_rgb(255, 180, 80));
        draw_text(_col1_x + 20, _ny + 54, "Threat: " + string(_node.threat_level_pct) + "% | Garrison: " + _node.assigned_mech_id);
    }

    // Node Quick Action Buttons
    var _nact_y = _col1_y + _col1_h - 100;
    var _clm_hov = (_mx >= _col1_x + 14 && _mx <= _col1_x + _col1_w - 14 && _my >= _nact_y && _my <= _nact_y + 36);
    if (_clm_hov && _click && array_length(_nodes) > 0) {
        var _sn = _nodes[clamp(mining_selected_idx, 0, array_length(_nodes) - 1)];
        _sn.status = "ACTIVE_MINING";
        _sn.assigned_mech_id = "Ironclad Mk-II Garrison";
        show_toast("NODE CLAIMED: " + _sn.name + " garrisoned by PMC!", c_lime);
        scr_audio_play_ui("boot");
    }
    scr_draw_snes_button(_col1_x + 14, _nact_y, _col1_w - 28, 36, "CLAIM SELECTED MINING NODE FOR PMC", _clm_hov, false, make_color_rgb(0, 240, 255));

    _nact_y += 44;
    var _all_clm_hov = (_mx >= _col1_x + 14 && _mx <= _col1_x + _col1_w - 14 && _my >= _nact_y && _my <= _nact_y + 36);
    if (_all_clm_hov && _click) {
        claim_all_mining_nodes();
    }
    scr_draw_snes_button(_col1_x + 14, _nact_y, _col1_w - 28, 36, "CLAIM ALL 16 SOLAR SYSTEM MINING NODES", _all_clm_hov, false, make_color_rgb(255, 200, 50));

    // ---------------------------------------------------------------------
    // B. CENTER COLUMN: PULSE LASER DRILL & EXTRACTION SIMULATOR (w: 430)
    // ---------------------------------------------------------------------
    var _col2_x = _col1_x + _col1_w + 12;
    var _col2_y = _win_y + 44;
    var _col2_w = 430;
    var _col2_h = 654;
    scr_draw_snes_panel(_col2_x, _col2_y, _col2_w, _col2_h, "PULSE DRILL EXTRACTION SIMULATOR", make_color_rgb(0, 240, 255), true, 0.03);

    // Asteroid Core & Drill Canvas
    var _ast_cx = _col2_x + (_col2_w / 2);
    var _ast_cy = _col2_y + 200;
    draw_set_color(make_color_rgb(8, 16, 28));
    draw_rectangle(_col2_x + 16, _col2_y + 30, _col2_x + _col2_w - 16, _col2_y + 380, false);
    draw_set_color(make_color_rgb(25, 55, 90));
    draw_rectangle(_col2_x + 16, _col2_y + 30, _col2_x + _col2_w - 16, _col2_y + 380, true);

    // Asteroid Graphic (Rock Outline & Mineral Veins)
    draw_set_color(make_color_rgb(45, 50, 60));
    draw_circle(_ast_cx, _ast_cy, 95, false);
    draw_set_color(make_color_rgb(70, 80, 95));
    draw_circle(_ast_cx - 20, _ast_cy - 15, 45, false);
    draw_circle(_ast_cx + 35, _ast_cy + 25, 35, false);

    // Glowing Mineral Crystals
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_circle(_ast_cx - 10, _ast_cy + 20, 12, false);
    draw_set_color(make_color_rgb(255, 180, 50));
    draw_circle(_ast_cx + 25, _ast_cy - 30, 8, false);

    // Pulse Drill Beam (when active)
    if (mining_drill_active || mining_drill_timer > 0) {
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_line_width(_ast_cx, _col2_y + 30, _ast_cx, _ast_cy, 6);
        draw_set_color(c_white);
        draw_line_width(_ast_cx, _col2_y + 30, _ast_cx, _ast_cy, 2);

        // Core Impact Sparks
        draw_circle(_ast_cx, _ast_cy, 28 + random(10), true);
        draw_set_color(make_color_rgb(255, 230, 100));
        draw_circle(_ast_cx, _ast_cy, 14, false);
    }

    // Floating Extraction Text Particles
    for (var p = 0; p < array_length(mining_particles); p++) {
        var _pt = mining_particles[p];
        draw_set_color(_pt.color);
        draw_set_alpha(clamp(_pt.life / 30.0, 0.0, 1.0));
        draw_text(_pt.x, _pt.y, _pt.text);
        draw_set_alpha(1.0);
    }

    // Heat Gauge
    var _heat_y = _col2_y + 395;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col2_x + 18, _heat_y, "DRILL CORE TEMPERATURE:");
    draw_set_color((mining_drill_heat > 80) ? c_red : ((mining_drill_heat > 50) ? make_color_rgb(255, 180, 40) : c_lime));
    draw_text(_col2_x + 280, _heat_y, string(floor(mining_drill_heat)) + " % CORE HEAT");

    _heat_y += 20;
    draw_set_color(make_color_rgb(20, 30, 45));
    draw_rectangle(_col2_x + 18, _heat_y, _col2_x + _col2_w - 18, _heat_y + 12, false);
    var _h_pct = clamp(mining_drill_heat / 100.0, 0.0, 1.0);
    draw_set_color((mining_drill_heat > 80) ? c_red : ((mining_drill_heat > 50) ? make_color_rgb(255, 180, 40) : make_color_rgb(0, 240, 255)));
    draw_rectangle(_col2_x + 18, _heat_y, _col2_x + 18 + (_h_pct * (_col2_w - 36)), _heat_y + 12, false);

    // Interactive Pulse Mining Button
    var _drill_btn_y = _col2_y + 450;
    var _drill_hov = (_mx >= _col2_x + 18 && _mx <= _col2_x + _col2_w - 18 && _my >= _drill_btn_y && _my <= _drill_btn_y + 54);
    if (_drill_hov && _click) {
        pulse_mine_node();
    }
    var _drill_col = (mining_drill_heat > 85) ? c_red : make_color_rgb(0, 240, 255);
    scr_draw_snes_button(_col2_x + 18, _drill_btn_y, _col2_w - 36, 54, ">>>> ENGAGE HIGH-OUTPUT PULSE DRILL [SPACE] <<<<", _drill_hov, true, _drill_col);

    // Flagship Mining Tier Status & Upgrade
    var _fs_y = _col2_y + 520;
    var _m_tier = 1;
    if (instance_exists(obj_GameManager) && variable_struct_exists(obj_GameManager.flagship, "upgrades")) {
        _m_tier = obj_GameManager.flagship.upgrades.mining_tier;
    }
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col2_x + 18, _fs_y, "FLAGSHIP REFINERY SILLS:");
    draw_set_color(make_color_rgb(255, 220, 80));
    draw_text(_col2_x + 230, _fs_y, "TIER " + string(_m_tier) + " (+" + string([25, 50, 100, 150, 250][clamp(_m_tier-1, 0, 4)]) + "% Yield Boost)");

    var _upg_hov = (_mx >= _col2_x + 18 && _mx <= _col2_x + _col2_w - 18 && _my >= _fs_y + 24 && _my <= _fs_y + 60);
    if (_upg_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            obj_GameManager.flagship.upgrades.mining_tier = 5;
            show_toast("[FLAGSHIP REFINERY] Upgraded to Tier 5 (+250% In-Sphere Refining)!", c_yellow);
            scr_audio_play_ui("boot");
        }
    }
    scr_draw_snes_button(_col2_x + 18, _fs_y + 24, _col2_w - 36, 36, "UPGRADE FLAGSHIP REFINERY TO TIER 5 (+250%)", _upg_hov, false, make_color_rgb(255, 200, 80));

    // ---------------------------------------------------------------------
    // C. RIGHT COLUMN: SMELTING FOUNDRY CRUCIBLE & RAIDS (w: 410)
    // ---------------------------------------------------------------------
    var _col3_x = _col2_x + _col2_w + 12;
    var _col3_y = _win_y + 44;
    var _col3_w = 410;
    var _col3_h = 654;
    scr_draw_snes_panel(_col3_x, _col3_y, _col3_w, _col3_h, "FOUNDRY CRUCIBLE & INCURSIONS", make_color_rgb(0, 240, 255), true, 0.03);

    // Current Raw Stockpile
    var _raw_y = _col3_y + 26;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col3_x + 18, _raw_y, "PMC RAW MINERAL STOCKPILE:");

    if (instance_exists(obj_GameManager)) {
        var _raw = obj_GameManager.inventory.raw_materials;
        _raw_y += 20;
        draw_set_color(c_white);
        draw_text(_col3_x + 18, _raw_y, "Tungsten: " + string(_raw.mat_tungsten) + " kg | Silica: " + string(_raw.mat_silica_carb) + " kg");
        _raw_y += 18;
        draw_text(_col3_x + 18, _raw_y, "Tritium: " + string(_raw.mat_tritium) + " kg | Synthetic Flux: " + string(_raw.mat_syn_flux) + " kg");
    }

    // Smelting Actions
    var _smelt_y = _raw_y + 34;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col3_x + 18, _smelt_y, "SYNTHESIZE CRUCIBLE ALLOYS:");

    var _sm_btn1_hov = (_mx >= _col3_x + 18 && _mx <= _col3_x + _col3_w - 18 && _my >= _smelt_y + 22 && _my <= _smelt_y + 58);
    if (_sm_btn1_hov && _click) {
        smelt_alloy_debug("alloy_vanguard_comp", 50);
    }
    scr_draw_snes_button(_col3_x + 18, _smelt_y + 22, _col3_w - 36, 36, "SMELT 50x VANGUARD COMPOSITE", _sm_btn1_hov, false, make_color_rgb(100, 220, 255));

    var _sm_btn2_hov = (_mx >= _col3_x + 18 && _mx <= _col3_x + _col3_w - 18 && _my >= _smelt_y + 66 && _my <= _smelt_y + 102);
    if (_sm_btn2_hov && _click) {
        smelt_alloy_debug("alloy_hyperion_matrix", 50);
    }
    scr_draw_snes_button(_col3_x + 18, _smelt_y + 66, _col3_w - 36, 36, "SMELT 50x HYPERION MATRIX", _sm_btn2_hov, false, make_color_rgb(100, 220, 255));

    var _sm_btn3_hov = (_mx >= _col3_x + 18 && _mx <= _col3_x + _col3_w - 18 && _my >= _smelt_y + 110 && _my <= _smelt_y + 146);
    if (_sm_btn3_hov && _click) {
        smelt_alloy_debug("alloy_aerosteel_flux", 50);
    }
    scr_draw_snes_button(_col3_x + 18, _smelt_y + 110, _col3_w - 36, 36, "SMELT 50x AEROSTEEL FLUX", _sm_btn3_hov, false, make_color_rgb(100, 220, 255));

    var _sm_btn4_hov = (_mx >= _col3_x + 18 && _mx <= _col3_x + _col3_w - 18 && _my >= _smelt_y + 154 && _my <= _smelt_y + 190);
    if (_sm_btn4_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            var _alloys = obj_GameManager.inventory.alloys;
            _alloys.alloy_vanguard_comp += 500;
            _alloys.alloy_hyperion_matrix += 500;
            _alloys.alloy_aerosteel_flux += 500;
            _alloys.alloy_adamantine_carbide += 500;
            _alloys.alloy_chobham_reactive += 500;
            _alloys.alloy_tachyon_superalloy += 500;
            show_toast("[CHEAT ACTIVE] +500 of Every Alloy Synthesized!", c_yellow);
            scr_audio_play_ui("boot");
        }
    }
    scr_draw_snes_button(_col3_x + 18, _smelt_y + 154, _col3_w - 36, 36, "FILL ALLOY INVENTORY (+500 EACH)", _sm_btn4_hov, false, make_color_rgb(255, 200, 50));

    // Incursion Raid Trigger
    var _raid_y = _smelt_y + 210;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col3_x + 18, _raid_y, "PIRATE RAID & INCURSION TESTBED:");

    var _nodes_curr = get_debug_mining_nodes();
    var _sel_node_name = (array_length(_nodes_curr) > 0) ? _nodes_curr[clamp(mining_selected_idx, 0, array_length(_nodes_curr)-1)].name : "Target Node";
    draw_set_color(make_color_rgb(255, 140, 40));
    draw_text(_col3_x + 18, _raid_y + 20, "TARGET: " + _sel_node_name);

    var _raid_btn_hov = (_mx >= _col3_x + 18 && _mx <= _col3_x + _col3_w - 18 && _my >= _raid_y + 44 && _my <= _raid_y + 88);
    if (_raid_btn_hov && _click) {
        trigger_mining_raid_debug();
    }
    scr_draw_snes_button(_col3_x + 18, _raid_y + 44, _col3_w - 36, 44, ">>>> TRIGGER PIRATE INVASION RAID <<<<", _raid_btn_hov, true, c_red);

    _raid_y += 98;
    var _sim_turn_hov = (_mx >= _col3_x + 18 && _mx <= _col3_x + _col3_w - 18 && _my >= _raid_y && _my <= _raid_y + 40);
    if (_sim_turn_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            obj_GameManager.end_turn();
            show_toast("[TURN ADVANCED] Global mining yields and raid rolls evaluated!", c_lime);
            scr_audio_play_ui("boot");
        }
    }
    scr_draw_snes_button(_col3_x + 18, _raid_y, _col3_w - 36, 40, "SIMULATE 1 TURN OF GLOBAL MINING", _sim_turn_hov, false, make_color_rgb(100, 220, 255));
}
'''

# 3. Replace "else if (active_debug_tab == 1)" with Tab 1, Tab 2, and "else if (active_debug_tab == 3)"
old_tab1_header = """// =========================================================================
// TAB 1: PMC CAMPAIGN CHEATS & SYSTEM TOOLS
// =========================================================================
else if (active_debug_tab == 1) {"""

new_tab_structure = tab1_and_tab2_code + """
// =========================================================================
// TAB 3: PMC CAMPAIGN CHEATS & SYSTEM TOOLS
// =========================================================================
else if (active_debug_tab == 3) {"""

assert old_tab1_header in content, "Could not find old_tab1_header in Draw_64.gml"
content = content.replace(old_tab1_header, new_tab_structure)

with open(DRAW_PATH, "w") as f:
    f.write(content)

print("Successfully patched Draw_64.gml with Tab 1 (Mech Builder) and Tab 2 (Mining)!")
