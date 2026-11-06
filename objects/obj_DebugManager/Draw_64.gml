/// @description obj_DebugManager Draw GUI Event
// Renders Front Mission / Gihren's Greed 2-Tier Battle Clash Demonstration & Universal Debug Hub

var _gw = display_get_gui_width();
var _gh = display_get_gui_height();
var _mx = device_mouse_x_to_gui(0);
var _my = device_mouse_y_to_gui(0);
var _click = mouse_check_button_pressed(mb_left);

// Persistent Floating Debug Launcher Badge (Always visible & clickable in any screen/room)
var _btn_dbg_w = 110;
var _btn_dbg_h = 24;
var _btn_dbg_x = _gw - _btn_dbg_w - 12;
var _btn_dbg_y = 6;
var _dbg_btn_hov = (_mx >= _btn_dbg_x && _mx <= _btn_dbg_x + _btn_dbg_w && _my >= _btn_dbg_y && _my <= _btn_dbg_y + _btn_dbg_h);

if (!is_open && !clash_cinematic.active) {
    // Render floating trigger badge
    draw_set_color(_dbg_btn_hov ? make_color_rgb(45, 30, 75) : make_color_rgb(18, 12, 30));
    draw_rectangle(_btn_dbg_x, _btn_dbg_y, _btn_dbg_x + _btn_dbg_w, _btn_dbg_y + _btn_dbg_h, false);
    draw_set_color(_dbg_btn_hov ? make_color_rgb(220, 140, 255) : make_color_rgb(140, 80, 190));
    draw_rectangle(_btn_dbg_x, _btn_dbg_y, _btn_dbg_x + _btn_dbg_w, _btn_dbg_y + _btn_dbg_h, true);
    draw_set_color(_dbg_btn_hov ? make_color_rgb(255, 230, 255) : make_color_rgb(210, 170, 255));
    draw_text_transformed(_btn_dbg_x + 8, _btn_dbg_y + 6, "[F7: DEBUG]", 0.75, 0.75, 0);

    if (_dbg_btn_hov && _click) {
        is_open = true;
        scr_audio_play_ui("boot");
    }
    exit;
}

// =========================================================================
// 1. FULL-SCREEN CINEMATIC CLASH DUEL STAGE
// =========================================================================
if (clash_cinematic.active) {
    var _shut = clash_cinematic.shutter_y;
    var _top_y = _shut;
    var _bot_y = _gh - _shut;

    var _shake_x = (clash_cinematic.screen_shake > 0) ? random_range(-clash_cinematic.screen_shake, clash_cinematic.screen_shake) : 0;
    var _shake_y = (clash_cinematic.screen_shake > 0) ? random_range(-clash_cinematic.screen_shake, clash_cinematic.screen_shake) : 0;

    // Environmental Backdrop
    if (clash_cinematic.theater == "SPACE") {
        draw_rectangle_color(0, _top_y, _gw, _bot_y, make_color_rgb(4, 7, 16), make_color_rgb(4, 7, 16), make_color_rgb(14, 22, 42), make_color_rgb(14, 22, 42), false);
        draw_set_color(make_color_rgb(10, 36, 70));
        draw_circle(_gw * 0.72, _gh * 1.05, 420, false);
        draw_set_color(make_color_rgb(50, 160, 255));
        draw_set_alpha(0.35);
        draw_circle(_gw * 0.72, _gh * 1.05, 425, true);
        draw_set_alpha(1.0);
        for (var i = 0; i < 45; i++) {
            var _sx = (i * 197 + 53) % _gw;
            var _sy = _top_y + ((i * 131 + 29) % max(1, _bot_y - _top_y));
            draw_set_color(c_white);
            draw_point(_sx, _sy);
        }
    } else if (clash_cinematic.theater == "WATER") {
        draw_rectangle_color(0, _top_y, _gw, _bot_y, make_color_rgb(10, 28, 48), make_color_rgb(14, 38, 64), make_color_rgb(6, 18, 32), make_color_rgb(8, 22, 38), false);
        draw_set_color(make_color_rgb(18, 55, 92));
        draw_rectangle(0, 500, _gw, _bot_y, false);
    } else if (clash_cinematic.theater == "SLAG") {
        draw_rectangle_color(0, _top_y, _gw, _bot_y, make_color_rgb(38, 14, 10), make_color_rgb(48, 18, 12), make_color_rgb(22, 8, 6), make_color_rgb(28, 10, 8), false);
        draw_set_color(make_color_rgb(70, 24, 14));
        draw_rectangle(0, 480, _gw, _bot_y, false);
    } else {
        // Earth Badlands
        draw_rectangle_color(0, _top_y, _gw, _bot_y, make_color_rgb(22, 16, 26), make_color_rgb(32, 24, 38), make_color_rgb(14, 10, 18), make_color_rgb(18, 12, 22), false);
        draw_set_color(make_color_rgb(38, 28, 36));
        draw_rectangle(0, 480, _gw, _bot_y, false);
    }

    // CRT Scanlines
    if (sprite_exists(spr_snes_crt_scanline)) {
        draw_sprite_tiled_ext(spr_snes_crt_scanline, 0, 0, _top_y, 1.0, 1.0, c_white, 0.12);
    }

    var _atk = clash_cinematic.attacker;
    var _def = clash_cinematic.defender;
    var _base_ground_y = 480;

    // Attacker Unit (Facing Right)
    var _ax = 360 + clash_cinematic.atk_recoil_x + _shake_x + clash_cinematic.atk_dash_x;
    var _ay = _base_ground_y + clash_cinematic.atk_recoil_y + _shake_y;
    scr_draw_animated_mobile_suit(_atk, _ax, _ay, 1.30, 1, clash_cinematic.atk_anim_state, clash_cinematic.atk_subimg, c_white, "front");

    // Defender Unit (Facing Left)
    var _dx = 1010 + clash_cinematic.def_recoil_x + _shake_x;
    var _dy = _base_ground_y + clash_cinematic.def_recoil_y + _shake_y;
    scr_draw_animated_mobile_suit(_def, _dx, _dy, 1.30, -1, clash_cinematic.def_anim_state, clash_cinematic.def_subimg, c_white, "front");

    // Dedicated Beam Lance Visual Effects
    if (clash_cinematic.weapon_class == "BEAM_LANCE") {
        var _t_cl = clash_cinematic.timer;
        // 1. Charging Vernier Thrust Trail (during high-speed charge)
        if (_t_cl >= 40 && _t_cl < 73) {
            draw_set_color(make_color_rgb(0, 240, 255));
            draw_set_alpha(0.65);
            draw_triangle(_ax - 28, _ay - 72, _ax - 28, _ay - 54, _ax - 85 - random(25), _ay - 63, false);
            draw_set_color(c_white);
            draw_set_alpha(0.85);
            draw_triangle(_ax - 28, _ay - 68, _ax - 28, _ay - 58, _ax - 55 - random(15), _ay - 63, false);
            draw_set_alpha(1.0);
        }
        // 2. Piercing Plasma Lance Core (during impale / stab)
        if (_t_cl >= 73 && _t_cl < 103) {
            var _tip_x = _dx - 15;
            var _tip_y = _dy - 55;
            var _base_x = _ax + 45;
            var _base_y = _ay - 58;
            draw_set_color(make_color_rgb(0, 240, 255));
            draw_line_width(_base_x, _base_y, _tip_x, _tip_y, 7.0);
            draw_set_color(c_white);
            draw_line_width(_base_x + 8, _base_y, _tip_x, _tip_y, 2.5);
            draw_set_color(make_color_rgb(180, 255, 255));
            draw_circle(_tip_x, _tip_y, 10 + random(6), true);
            draw_circle(_tip_x, _tip_y, 5 + random(3), false);
        }
        // 3. Point-Blank Plasma Burst Detonation & Shockwave (during blast & knockback)
        if (_t_cl >= 103 && _t_cl < 130) {
            var _b_prog = (_t_cl - 103);
            var _b_rad = _b_prog * 6.5;
            var _b_alpha = max(0, 1.0 - (_b_prog / 27.0));
            var _bx = _dx - 15;
            var _by = _dy - 55;
            draw_set_alpha(_b_alpha * 0.7);
            draw_set_color(make_color_rgb(0, 240, 255));
            draw_circle(_bx, _by, _b_rad, false);
            draw_set_alpha(_b_alpha * 0.9);
            draw_set_color(c_white);
            draw_circle(_bx, _by, _b_rad * 0.45, false);
            draw_set_color(make_color_rgb(140, 255, 255));
            draw_circle(_bx, _by, _b_rad * 1.35, true);
            draw_line_width(_bx - _b_rad, _by, _bx + _b_rad, _by, 3.0);
            draw_set_alpha(1.0);
        }
    }

    // Spent brass casings
    for (var i = 0; i < array_length(clash_cinematic.casings); i++) {
        var _cs = clash_cinematic.casings[i];
        draw_set_color(make_color_rgb(255, 215, 60));
        draw_line_width(_cs.x, _cs.y, _cs.x + lengthdir_x(7, _cs.angle), _cs.y + lengthdir_y(7, _cs.angle), 2.5);
    }

    // Projectiles
    for (var i = 0; i < array_length(clash_cinematic.projectiles); i++) {
        var _pj = clash_cinematic.projectiles[i];
        if (_pj.type == "ROTARY_VULCAN") {
            draw_set_color(make_color_rgb(255, 240, 140));
            draw_line_width(_pj.cur_x - 18, _pj.cur_y, _pj.cur_x + 18, _pj.cur_y, 3.0);
            draw_set_color(c_white);
            draw_line_width(_pj.cur_x - 8, _pj.cur_y, _pj.cur_x + 8, _pj.cur_y, 1.5);
        } else if (_pj.type == "BEAM_PULSE") {
            draw_set_color(make_color_rgb(0, 220, 255));
            draw_line_width(_pj.cur_x - 35, _pj.cur_y, _pj.cur_x + 35, _pj.cur_y, 6.0);
            draw_set_color(c_white);
            draw_line_width(_pj.cur_x - 25, _pj.cur_y, _pj.cur_x + 25, _pj.cur_y, 2.5);
        } else {
            draw_set_color(make_color_rgb(255, 200, 80));
            draw_line_width(_pj.cur_x - 14, _pj.cur_y, _pj.cur_x + 14, _pj.cur_y, 4.0);
        }
    }

    // Particles
    for (var i = 0; i < array_length(clash_cinematic.particles); i++) {
        var _pt = clash_cinematic.particles[i];
        if (sprite_exists(_pt.sprite)) {
            draw_sprite_ext(_pt.sprite, floor(_pt.frame), _pt.x + _shake_x, _pt.y + _shake_y, _pt.scale, _pt.scale, 0, c_white, _pt.alpha);
        }
    }

    // Floating Popups
    for (var i = 0; i < array_length(clash_cinematic.popups); i++) {
        var _pp = clash_cinematic.popups[i];
        draw_set_color(_pp.col);
        draw_text_transformed(_pp.x - 40, _pp.y, _pp.text, 1.25, 1.25, 0);
    }

    // Letterbox Shutter Bars
    draw_set_color(c_black);
    draw_rectangle(0, 0, _gw, _shut, false);
    draw_rectangle(0, _gh - _shut, _gw, _gh, false);

    // Top Header
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(24, max(8, _shut - 32), "THEATER: " + string_upper(clash_cinematic.theater) + " // HOLO-SIMULATION ENGAGEMENT GRID");
    draw_set_color(make_color_rgb(255, 200, 60));
    draw_text(_gw - 360, max(8, _shut - 32), "[SPACE / CLICK: SKIP // ESC: EXIT]");

    // Bottom Cockpit Telemetry Ribbons
    if (_shut >= 60) {
        // Attacker Telemetry (Left)
        draw_set_color(make_color_rgb(12, 18, 28));
        draw_rectangle(24, _gh - _shut + 8, 380, _gh - 8, false);
        draw_set_color(make_color_rgb(35, 65, 95));
        draw_rectangle(24, _gh - _shut + 8, 380, _gh - 8, true);
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(34, _gh - _shut + 14, "ALLIED: " + _atk.name);
        draw_set_color(c_white);
        draw_text(34, _gh - _shut + 34, "HULL INTEGRITY: " + string(clash_cinematic.atk_hp) + " / " + string(clash_cinematic.atk_max_hp));
        var _ab_w = 340;
        var _a_pct = clamp(clash_cinematic.atk_hp / max(1, clash_cinematic.atk_max_hp), 0, 1);
        draw_set_color(make_color_rgb(10, 20, 30));
        draw_rectangle(34, _gh - _shut + 52, 34 + _ab_w, _gh - _shut + 59, false);
        draw_set_color(merge_color(c_red, c_lime, _a_pct));
        draw_rectangle(34, _gh - _shut + 52, 34 + (_ab_w * _a_pct), _gh - _shut + 59, false);

        // Defender Telemetry (Right)
        draw_set_color(make_color_rgb(28, 14, 12));
        draw_rectangle(_gw - 404, _gh - _shut + 8, _gw - 24, _gh - 8, false);
        draw_set_color(make_color_rgb(95, 45, 35));
        draw_rectangle(_gw - 404, _gh - _shut + 8, _gw - 24, _gh - 8, true);
        draw_set_color(make_color_rgb(255, 120, 40));
        draw_text(_gw - 394, _gh - _shut + 14, "TARGET: " + _def.name);
        draw_set_color(c_white);
        draw_text(_gw - 394, _gh - _shut + 34, "HULL INTEGRITY: " + string(clash_cinematic.def_hp) + " / " + string(clash_cinematic.def_max_hp));
        var _db_w = 340;
        var _d_pct = clamp(clash_cinematic.def_hp / max(1, clash_cinematic.def_max_hp), 0, 1);
        draw_set_color(make_color_rgb(30, 10, 10));
        draw_rectangle(_gw - 394, _gh - _shut + 52, _gw - 394 + _db_w, _gh - _shut + 59, false);
        draw_set_color(merge_color(c_red, c_lime, _d_pct));
        draw_rectangle(_gw - 394, _gh - _shut + 52, _gw - 394 + (_db_w * _d_pct), _gh - _shut + 59, false);
    }

    if (_click) {
        if (clash_cinematic.phase < 3) {
            clash_cinematic.phase = 3;
            clash_cinematic.timer = 180;
        } else {
            clash_cinematic.active = false;
        }
    }
    exit;
}

// =========================================================================
// 2. MAIN DEBUG & PROVING GROUND WINDOW (SNES STEEL AESTHETICS)
// =========================================================================
draw_set_color(c_black);
draw_set_alpha(0.78);
draw_rectangle(0, 0, _gw, _gh, false);
draw_set_alpha(1.0);

var _win_x = 38;
var _win_y = 28;
var _win_w = 1290;
var _win_h = 712;
scr_draw_snes_panel(_win_x, _win_y, _win_w, _win_h, "", -1, true, 0.05);

// Header Bar
draw_set_color(make_color_rgb(0, 240, 255));
draw_text(_win_x + 20, _win_y + 14, "PMC DEBUG HUB // [F7]");
draw_set_color(make_color_rgb(140, 170, 200));
draw_text(_win_x + 580, _win_y + 14, "[TOGGLE: F7 / TILDE]");

// 4 Universal Testing Tabs (Combat, Mech Builder, Mining, Cheats)
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
scr_draw_snes_button(_t3_x, _win_y + 8, _tab_w, _tab_h, "4. CAMPAIGN CHEATS", _t3_hov || (active_debug_tab == 3), (active_debug_tab == 3), (active_debug_tab == 3) ? make_color_rgb(0, 240, 255) : c_white);

// Close Button [X]
var _cls_hov = (_mx >= _win_x + _win_w - 56 && _mx <= _win_x + _win_w - 20 && _my >= _win_y + 8 && _my <= _win_y + 36);
if (_cls_hov && _click) {
    is_open = false;
    scr_audio_play_ui("cancel");
}
scr_draw_snes_button(_win_x + _win_w - 56, _win_y + 8, 36, 28, "X", _cls_hov, false, c_red);

// =========================================================================
// TAB 0: BATTLE & ANIMATION PROVING GROUND LAB
// =========================================================================
if (active_debug_tab == 0) {
    // ---------------------------------------------------------------------
    // A. LEFT COLUMN: ATTACKER SQUADRON SELECTION (w: 300)
    // ---------------------------------------------------------------------
    var _col1_x = _win_x + 14;
    var _col1_y = _win_y + 44;
    var _col1_w = 300;
    var _col1_h = 654;
    scr_draw_snes_panel(_col1_x, _col1_y, _col1_w, _col1_h, "ATTACKER CONFIGURATION", make_color_rgb(0, 240, 255), true, 0.03);

    var _atk_list = get_filtered_units(atk_faction_idx, atk_cat_idx);
    atk_filtered_idx = clamp(atk_filtered_idx, 0, max(0, array_length(_atk_list) - 1));
    var _cur_atk = _atk_list[atk_filtered_idx];
    // Automatically synchronize weapon choreography when switching units
    if (!variable_instance_exists(id, "atk_prev_unit_id") || atk_prev_unit_id != _cur_atk.id) {
        atk_prev_unit_id = _cur_atk.id;
        anim_state_idx = 0;
        if (variable_struct_exists(_cur_atk, "weapon_class") && _cur_atk.weapon_class != "") {
            for (var wi = 0; wi < array_length(weapon_classes); wi++) {
                if (weapon_classes[wi] == _cur_atk.weapon_class) {
                    weapon_idx = wi;
                    break;
                }
            }
        }
    }

    // Resolve applicable animation states for the selected attacker
    var _active_anim_states = ["idle"];
    if (_cur_atk.category != "CUSTOM_MECH") {
        if (_cur_atk.weapon_class == "BALLISTIC") array_push(_active_anim_states, "fire_rifle");
        else if (_cur_atk.weapon_class == "ROTARY_VULCAN") array_push(_active_anim_states, "fire_chaingun");
        else if (_cur_atk.weapon_class == "BEAM_PULSE") array_push(_active_anim_states, "fire_beam");
        else if (_cur_atk.weapon_class == "MICRO_MISSILE") array_push(_active_anim_states, "fire_missiles");
        else array_push(_active_anim_states, "fire_rifle");

        if (variable_struct_exists(_cur_atk, "sprites") && is_struct(_cur_atk.sprites)) {
            if (variable_struct_exists(_cur_atk.sprites, "melee") && _cur_atk.sprites.melee != -1) array_push(_active_anim_states, "melee");
            if (variable_struct_exists(_cur_atk.sprites, "boost") && _cur_atk.sprites.boost != -1) array_push(_active_anim_states, "boost");
            if (variable_struct_exists(_cur_atk.sprites, "damaged") && _cur_atk.sprites.damaged != -1) array_push(_active_anim_states, "damaged");
            if (variable_struct_exists(_cur_atk.sprites, "destroyed") && _cur_atk.sprites.destroyed != -1) array_push(_active_anim_states, "destroyed");
        }
    } else {
        _active_anim_states = ["idle", "fire_rifle", "fire_chaingun", "fire_beam", "fire_missiles", "melee", "boost", "damaged", "destroyed"];
    }
    anim_state_idx = clamp(anim_state_idx, 0, array_length(_active_anim_states) - 1);

    // Faction Filter Selector
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col1_x + 14, _col1_y + 26, "FACTION FILTER:");
    var _af_hov = (_mx >= _col1_x + 14 && _mx <= _col1_x + _col1_w - 14 && _my >= _col1_y + 44 && _my <= _col1_y + 70);
    if (_af_hov && _click) {
        atk_faction_idx = (atk_faction_idx + 1) % array_length(factions);
        atk_filtered_idx = 0;
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col1_x + 14, _col1_y + 44, _col1_w - 28, 26, "< " + faction_names[atk_faction_idx] + " >", _af_hov, false, make_color_rgb(0, 240, 255));

    // Category Filter Selector
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col1_x + 14, _col1_y + 78, "CATEGORY FILTER:");
    var _ac_hov = (_mx >= _col1_x + 14 && _mx <= _col1_x + _col1_w - 14 && _my >= _col1_y + 96 && _my <= _col1_y + 122);
    if (_ac_hov && _click) {
        atk_cat_idx = (atk_cat_idx + 1) % array_length(categories);
        atk_filtered_idx = 0;
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col1_x + 14, _col1_y + 96, _col1_w - 28, 26, "< " + category_names[atk_cat_idx] + " >", _ac_hov, false, make_color_rgb(0, 240, 255));

    // Unit Carousel Navigation
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col1_x + 14, _col1_y + 130, "UNIT SELECTION (" + string(atk_filtered_idx + 1) + " / " + string(array_length(_atk_list)) + "):");

    var _p_hov = (_mx >= _col1_x + 14 && _mx <= _col1_x + 70 && _my >= _col1_y + 148 && _my <= _col1_y + 176);
    if (_p_hov && _click) {
        atk_filtered_idx = (atk_filtered_idx - 1 + array_length(_atk_list)) % array_length(_atk_list);
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col1_x + 14, _col1_y + 148, 56, 28, "< PREV", _p_hov, false, c_white);

    var _n_hov = (_mx >= _col1_x + _col1_w - 70 && _mx <= _col1_x + _col1_w - 14 && _my >= _col1_y + 148 && _my <= _col1_y + 176);
    if (_n_hov && _click) {
        atk_filtered_idx = (atk_filtered_idx + 1) % array_length(_atk_list);
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col1_x + _col1_w - 70, _col1_y + 148, 56, 28, "NEXT >", _n_hov, false, c_white);

    // Unit Specification Card
    draw_set_color(make_color_rgb(16, 24, 34));
    draw_rectangle(_col1_x + 14, _col1_y + 186, _col1_x + _col1_w - 14, _col1_y + 440, false);
    draw_set_color(make_color_rgb(32, 60, 90));
    draw_rectangle(_col1_x + 14, _col1_y + 186, _col1_x + _col1_w - 14, _col1_y + 440, true);

    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text_transformed(_col1_x + 22, _col1_y + 196, _cur_atk.name, 0.95, 0.95, 0);

    draw_set_color(make_color_rgb(140, 170, 200));
    draw_text(_col1_x + 22, _col1_y + 226, "ID: " + _cur_atk.id);
    var _atk_era_str = variable_struct_exists(_cur_atk, "era") ? (" [GEN " + string(_cur_atk.era) + "]") : "";
    draw_text(_col1_x + 22, _col1_y + 250, "FACTION: " + _cur_atk.faction_id + _atk_era_str);
    draw_text(_col1_x + 22, _col1_y + 274, "CATEGORY: " + _cur_atk.category);
    var _atk_doc_str = (variable_struct_exists(_cur_atk, "doctrine") && _cur_atk.doctrine != "") ? string_copy(_cur_atk.doctrine, 1, 24) : string_upper(_cur_atk.chassis);
    draw_text(_col1_x + 22, _col1_y + 298, "DOCTRINE: " + _atk_doc_str);
    var _atk_alloy_str = variable_struct_exists(_cur_atk, "alloy") ? _cur_atk.alloy : (variable_struct_exists(_cur_atk, "alloy_id") ? _cur_atk.alloy_id : "Vanguard Composite");
    draw_text(_col1_x + 22, _col1_y + 322, "ALLOY: " + string(_atk_alloy_str));
    draw_text(_col1_x + 22, _col1_y + 346, "WEAPON: " + _cur_atk.weapon_name);
    draw_text(_col1_x + 22, _col1_y + 370, "HULL: " + string(_cur_atk.hp) + " HP");
    draw_text(_col1_x + 22, _col1_y + 394, "ARMOR: " + string(_cur_atk.armor) + " RATING");

    // Perspective Selector Button
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col1_x + 14, _col1_y + 456, "PERSPECTIVE ANGLE:");
    var _per_hov = (_mx >= _col1_x + 14 && _mx <= _col1_x + _col1_w - 14 && _my >= _col1_y + 474 && _my <= _col1_y + 504);
    if (_per_hov && _click) {
        anim_perspective = (anim_perspective == "front") ? "back" : "front";
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col1_x + 14, _col1_y + 474, _col1_w - 28, 30, (anim_perspective == "front") ? "[3/4 ISOMETRIC FRONT]" : "[REAR TWIN VERNIERS]", _per_hov, false, make_color_rgb(100, 220, 255));

    // Formation Stance
    draw_set_color(make_color_rgb(60, 240, 120));
    draw_text(_col1_x + 14, _col1_y + 524, "STANCE: ALLIED ATTACKER (FACING RIGHT)");

    // ---------------------------------------------------------------------
    // B. RIGHT COLUMN: DEFENDER TARGET SELECTION (w: 300)
    // ---------------------------------------------------------------------
    var _col3_x = _win_x + _win_w - 314;
    var _col3_y = _win_y + 44;
    var _col3_w = 300;
    var _col3_h = 654;
    scr_draw_snes_panel(_col3_x, _col3_y, _col3_w, _col3_h, "DEFENDER TARGET", make_color_rgb(255, 120, 40), true, 0.03);

    var _def_list = get_filtered_units(def_faction_idx, def_cat_idx);
    def_filtered_idx = clamp(def_filtered_idx, 0, max(0, array_length(_def_list) - 1));
    var _cur_def = _def_list[def_filtered_idx];

    // Faction Filter Selector
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col3_x + 14, _col3_y + 26, "FACTION FILTER:");
    var _df_hov = (_mx >= _col3_x + 14 && _mx <= _col3_x + _col3_w - 14 && _my >= _col3_y + 44 && _my <= _col3_y + 70);
    if (_df_hov && _click) {
        def_faction_idx = (def_faction_idx + 1) % array_length(factions);
        def_filtered_idx = 0;
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col3_x + 14, _col3_y + 44, _col3_w - 28, 26, "< " + faction_names[def_faction_idx] + " >", _df_hov, false, make_color_rgb(255, 120, 40));

    // Category Filter Selector
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col3_x + 14, _col3_y + 78, "CATEGORY FILTER:");
    var _dc_hov = (_mx >= _col3_x + 14 && _mx <= _col3_x + _col3_w - 14 && _my >= _col3_y + 96 && _my <= _col3_y + 122);
    if (_dc_hov && _click) {
        def_cat_idx = (def_cat_idx + 1) % array_length(categories);
        def_filtered_idx = 0;
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col3_x + 14, _col3_y + 96, _col3_w - 28, 26, "< " + category_names[def_cat_idx] + " >", _dc_hov, false, make_color_rgb(255, 120, 40));

    // Unit Carousel Navigation
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col3_x + 14, _col3_y + 130, "TARGET SELECTION (" + string(def_filtered_idx + 1) + " / " + string(array_length(_def_list)) + "):");

    var _dp_hov = (_mx >= _col3_x + 14 && _mx <= _col3_x + 70 && _my >= _col3_y + 148 && _my <= _col3_y + 176);
    if (_dp_hov && _click) {
        def_filtered_idx = (def_filtered_idx - 1 + array_length(_def_list)) % array_length(_def_list);
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col3_x + 14, _col3_y + 148, 56, 28, "< PREV", _dp_hov, false, c_white);

    var _dn_hov = (_mx >= _col3_x + _col3_w - 70 && _mx <= _col3_x + _col3_w - 14 && _my >= _col3_y + 148 && _my <= _col3_y + 176);
    if (_dn_hov && _click) {
        def_filtered_idx = (def_filtered_idx + 1) % array_length(_def_list);
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col3_x + _col3_w - 70, _col3_y + 148, 56, 28, "NEXT >", _dn_hov, false, c_white);

    // Unit Specification Card
    draw_set_color(make_color_rgb(28, 18, 16));
    draw_rectangle(_col3_x + 14, _col3_y + 186, _col3_x + _col3_w - 14, _col3_y + 440, false);
    draw_set_color(make_color_rgb(90, 45, 32));
    draw_rectangle(_col3_x + 14, _col3_y + 186, _col3_x + _col3_w - 14, _col3_y + 440, true);

    draw_set_color(make_color_rgb(255, 140, 40));
    draw_text_transformed(_col3_x + 22, _col3_y + 196, _cur_def.name, 0.95, 0.95, 0);

    draw_set_color(make_color_rgb(200, 170, 160));
    draw_text(_col3_x + 22, _col3_y + 226, "ID: " + _cur_def.id);
    var _def_era_str = variable_struct_exists(_cur_def, "era") ? (" [GEN " + string(_cur_def.era) + "]") : "";
    draw_text(_col3_x + 22, _col3_y + 250, "FACTION: " + _cur_def.faction_id + _def_era_str);
    draw_text(_col3_x + 22, _col3_y + 274, "CATEGORY: " + _cur_def.category);
    var _def_doc_str = (variable_struct_exists(_cur_def, "doctrine") && _cur_def.doctrine != "") ? string_copy(_cur_def.doctrine, 1, 24) : string_upper(_cur_def.chassis);
    draw_text(_col3_x + 22, _col3_y + 298, "DOCTRINE: " + _def_doc_str);
    var _def_alloy_str = variable_struct_exists(_cur_def, "alloy") ? _cur_def.alloy : (variable_struct_exists(_cur_def, "alloy_id") ? _cur_def.alloy_id : "Vanguard Composite");
    draw_text(_col3_x + 22, _col3_y + 322, "ALLOY: " + string(_def_alloy_str));
    draw_text(_col3_x + 22, _col3_y + 346, "WEAPON: " + _cur_def.weapon_name);
    draw_text(_col3_x + 22, _col3_y + 370, "HULL: " + string(_cur_def.hp) + " HP");
    draw_text(_col3_x + 22, _col3_y + 394, "ARMOR: " + string(_cur_def.armor) + " RATING");

    // Defense Target Reticle Status
    draw_set_color(make_color_rgb(255, 80, 80));
    draw_text(_col3_x + 14, _col3_y + 474, "TARGET STATUS: LOCK ACQUIRED");
    draw_set_color(make_color_rgb(255, 140, 40));
    draw_text(_col3_x + 14, _col3_y + 524, "STANCE: DEFENDER TARGET (FACING LEFT)");

    // ---------------------------------------------------------------------
    // C. CENTER COLUMN: VISUAL STAGE & CLASH CONTROLS (w: 646)
    // ---------------------------------------------------------------------
    var _col2_x = _win_x + 322;
    var _col2_y = _win_y + 44;
    var _col2_w = 646;
    var _col2_h = 654;
    scr_draw_snes_panel(_col2_x, _col2_y, _col2_w, _col2_h, "BATTLE ANIMATION ENGINE PROVING GROUND", make_color_rgb(255, 200, 60), true, 0.03);

    // 1. Visual Stage Frame
    var _stg_x = _col2_x + 12;
    var _stg_y = _col2_y + 28;
    var _stg_w = _col2_w - 24;
    var _stg_h = 270;

    // Environmental Backdrop
    var _th = theaters[theater_idx];
    if (_th == "SPACE") {
        draw_rectangle_color(_stg_x, _stg_y, _stg_x + _stg_w, _stg_y + _stg_h, make_color_rgb(4, 7, 16), make_color_rgb(4, 7, 16), make_color_rgb(14, 22, 42), make_color_rgb(14, 22, 42), false);
        for (var i = 0; i < 30; i++) {
            var _sx = _stg_x + ((i * 77 + 23) % _stg_w);
            var _sy = _stg_y + ((i * 43 + 17) % _stg_h);
            draw_set_color(c_white);
            draw_point(_sx, _sy);
        }
    } else if (_th == "WATER") {
        draw_rectangle_color(_stg_x, _stg_y, _stg_x + _stg_w, _stg_y + _stg_h, make_color_rgb(8, 22, 40), make_color_rgb(12, 32, 54), make_color_rgb(5, 14, 26), make_color_rgb(6, 18, 32), false);
        draw_set_color(make_color_rgb(18, 55, 92));
        draw_rectangle(_stg_x, _stg_y + 200, _stg_x + _stg_w, _stg_y + _stg_h, false);
    } else if (_th == "SLAG") {
        draw_rectangle_color(_stg_x, _stg_y, _stg_x + _stg_w, _stg_y + _stg_h, make_color_rgb(32, 12, 8), make_color_rgb(42, 16, 10), make_color_rgb(18, 6, 4), make_color_rgb(22, 8, 6), false);
        draw_set_color(make_color_rgb(65, 22, 12));
        draw_rectangle(_stg_x, _stg_y + 190, _stg_x + _stg_w, _stg_y + _stg_h, false);
    } else {
        // Earth Badlands
        draw_rectangle_color(_stg_x, _stg_y, _stg_x + _stg_w, _stg_y + _stg_h, make_color_rgb(18, 14, 22), make_color_rgb(26, 20, 30), make_color_rgb(12, 8, 14), make_color_rgb(14, 10, 16), false);
        draw_set_color(make_color_rgb(32, 24, 30));
        draw_rectangle(_stg_x, _stg_y + 195, _stg_x + _stg_w, _stg_y + _stg_h, false);
    }

    // Border around stage
    draw_set_color(make_color_rgb(50, 75, 105));
    draw_rectangle(_stg_x, _stg_y, _stg_x + _stg_w, _stg_y + _stg_h, true);

    // CRT Scanline Overlay
    if (sprite_exists(spr_snes_crt_scanline)) {
        draw_sprite_tiled_ext(spr_snes_crt_scanline, 0, _stg_x, _stg_y, 1.0, 1.0, c_white, 0.10);
    }

    // Draw Live Attacker (Left)
    var _live_ax = _stg_x + 160;
    var _live_ay = _stg_y + 205;
    var _atk_st = _active_anim_states[anim_state_idx];
    scr_draw_animated_mobile_suit(_cur_atk, _live_ax, _live_ay, 1.25, 1, _atk_st, subimg_atk, c_white, anim_perspective);

    // Draw Live Defender (Right)
    var _live_dx = _stg_x + _stg_w - 160;
    var _live_dy = _stg_y + 205;
    scr_draw_animated_mobile_suit(_cur_def, _live_dx, _live_dy, 1.25, -1, "idle", subimg_def, c_white, anim_perspective);

    // Reticle lock on defender
    var _rt_pulse = 0.7 + 0.3 * sin(current_time * 0.008);
    draw_set_color(make_color_rgb(255, 60, 60));
    draw_set_alpha(_rt_pulse);
    draw_circle(_live_dx, _live_dy - 55, 40, true);
    draw_line(_live_dx - 50, _live_dy - 55, _live_dx - 30, _live_dy - 55);
    draw_line(_live_dx + 30, _live_dy - 55, _live_dx + 50, _live_dy - 55);
    draw_line(_live_dx, _live_dy - 105, _live_dx, _live_dy - 85);
    draw_line(_live_dx, _live_dy - 25, _live_dx, _live_dy - 5);
    draw_set_alpha(1.0);

    // 2. Controls Section Below Stage
    var _ctrl_y = _stg_y + _stg_h + 14;

    // Theater Environment Buttons
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col2_x + 14, _ctrl_y, "THEATER ENVIRONMENT:");
    var _btn_tw = (_col2_w - 28 - 18) / 4;
    for (var th = 0; th < 4; th++) {
        var _bx = _col2_x + 14 + th * (_btn_tw + 6);
        var _th_hov = (_mx >= _bx && _mx <= _bx + _btn_tw && _my >= _ctrl_y + 18 && _my <= _ctrl_y + 44);
        var _is_cur_th = (theater_idx == th);
        if (_th_hov && _click) {
            theater_idx = th;
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_bx, _ctrl_y + 18, _btn_tw, 26, theaters[th], _th_hov || _is_cur_th, _is_cur_th, _is_cur_th ? make_color_rgb(0, 240, 255) : c_white);
    }

    // Animation State Scrubbing Controls
    var _ast_y = _ctrl_y + 54;
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col2_x + 14, _ast_y, "ANIMATION STATE SCRUBBING:");

    var _ap_hov = (_mx >= _col2_x + 14 && _mx <= _col2_x + 90 && _my >= _ast_y + 18 && _my <= _ast_y + 46);
    if (_ap_hov && _click) {
        anim_state_idx = (anim_state_idx - 1 + array_length(_active_anim_states)) % array_length(_active_anim_states);
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col2_x + 14, _ast_y + 18, 76, 28, "< PREV", _ap_hov, false, c_white);

    var _cur_st_name = "[ " + string_upper(_active_anim_states[anim_state_idx]) + " ]";
    var _mid_w = _col2_w - 28 - 164;
    draw_set_color(make_color_rgb(20, 32, 48));
    draw_rectangle(_col2_x + 96, _ast_y + 18, _col2_x + 96 + _mid_w, _ast_y + 46, false);
    draw_set_color(make_color_rgb(45, 80, 120));
    draw_rectangle(_col2_x + 96, _ast_y + 18, _col2_x + 96 + _mid_w, _ast_y + 46, true);
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col2_x + 110, _ast_y + 24, _cur_st_name);

    var _an_hov = (_mx >= _col2_x + _col2_w - 90 && _mx <= _col2_x + _col2_w - 14 && _my >= _ast_y + 18 && _my <= _ast_y + 46);
    if (_an_hov && _click) {
        anim_state_idx = (anim_state_idx + 1) % array_length(_active_anim_states);
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col2_x + _col2_w - 90, _ast_y + 18, 76, 28, "NEXT >", _an_hov, false, c_white);

    // Playback Speed & Frame Stepping
    var _ply_y = _ast_y + 56;
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col2_x + 14, _ply_y, "PLAYBACK CONTROLS:");

    for (var sp = 0; sp < 4; sp++) {
        var _sp_x = _col2_x + 14 + sp * 65;
        var _sp_hov = (_mx >= _sp_x && _mx <= _sp_x + 60 && _my >= _ply_y + 18 && _my <= _ply_y + 44);
        var _is_cur_sp = (anim_speed_idx == sp);
        if (_sp_hov && _click) {
            anim_speed_idx = sp;
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_sp_x, _ply_y + 18, 60, 26, anim_speed_names[sp], _sp_hov || _is_cur_sp, _is_cur_sp, _is_cur_sp ? make_color_rgb(0, 240, 255) : c_white);
    }

    // Pause/Play
    var _pause_x = _col2_x + 285;
    var _pau_hov = (_mx >= _pause_x && _mx <= _pause_x + 95 && _my >= _ply_y + 18 && _my <= _ply_y + 44);
    if (_pau_hov && _click) {
        is_paused = !is_paused;
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_pause_x, _ply_y + 18, 95, 26, is_paused ? "PLAY >" : "PAUSE ||", _pau_hov, is_paused, is_paused ? c_yellow : c_white);

    // Step Frame
    var _step_x = _col2_x + 390;
    var _stp_hov = (_mx >= _step_x && _mx <= _step_x + 105 && _my >= _ply_y + 18 && _my <= _ply_y + 44);
    if (_stp_hov && _click) {
        step_frame_req = true;
        is_paused = true;
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_step_x, _ply_y + 18, 105, 26, "STEP FRAME >", _stp_hov, false, c_white);

    // Audio SFX Test
    var _sfx_x = _col2_x + 505;
    var _sfx_hov = (_mx >= _sfx_x && _mx <= _sfx_x + 127 && _my >= _ply_y + 18 && _my <= _ply_y + 44);
    if (_sfx_hov && _click) {
        scr_audio_play_weapon(weapon_classes[weapon_idx]);
    }
    scr_draw_snes_button(_sfx_x, _ply_y + 18, 127, 26, "TEST SFX", _sfx_hov, false, make_color_rgb(255, 200, 60));

    // Weapon Class Selector (Filtered strictly to options that apply for this mobile suit)
    var _wpn_y = _ply_y + 54;
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col2_x + 14, _wpn_y, "WEAPON CLASS CHOREOGRAPHY:");

    var _applicable_w_classes = [];
    if (_cur_atk.category != "CUSTOM_MECH") {
        array_push(_applicable_w_classes, _cur_atk.weapon_class);
        if (variable_struct_exists(_cur_atk, "sprites") && is_struct(_cur_atk.sprites) && variable_struct_exists(_cur_atk.sprites, "melee") && _cur_atk.sprites.melee != -1) {
            array_push(_applicable_w_classes, "MELEE");
        }
    } else {
        _applicable_w_classes = weapon_classes;
    }

    var _w_btn_w = _col2_w - 28;
    var _wpn_hov = (_mx >= _col2_x + 14 && _mx <= _col2_x + 14 + _w_btn_w && _my >= _wpn_y + 18 && _my <= _wpn_y + 44);
    if (_wpn_hov && _click) {
        var _cur_cls = weapon_classes[weapon_idx];
        var _app_idx = 0;
        for (var ai = 0; ai < array_length(_applicable_w_classes); ai++) {
            if (_applicable_w_classes[ai] == _cur_cls) { _app_idx = ai; break; }
        }
        var _next_app_idx = (_app_idx + 1) % array_length(_applicable_w_classes);
        var _target_cls = _applicable_w_classes[_next_app_idx];
        for (var wi = 0; wi < array_length(weapon_classes); wi++) {
            if (weapon_classes[wi] == _target_cls) { weapon_idx = wi; break; }
        }
        scr_audio_play_ui("click");
    }

    var _btn_label = "";
    var _btn_col = make_color_rgb(255, 200, 60);
    if (_cur_atk.category != "CUSTOM_MECH") {
        if (weapon_classes[weapon_idx] == _cur_atk.weapon_class) {
            _btn_label = "< [PRIMARY DOCTRINE]: " + _cur_atk.weapon_name + " (" + weapon_classes[weapon_idx] + ") >";
            _btn_col = make_color_rgb(100, 240, 255);
        } else if (weapon_classes[weapon_idx] == "MELEE") {
            var _m_name = (variable_struct_exists(_cur_atk, "weapon_overlay_secondary") && _cur_atk.weapon_overlay_secondary != "") ? _cur_atk.weapon_overlay_secondary : "Cybernetic Demolition Mace & Shield";
            _btn_label = "< [MELEE COMBAT]: " + _m_name + " (MELEE) >";
            _btn_col = make_color_rgb(0, 240, 255);
        }
    } else {
        _btn_label = "< WEAPON: " + weapon_names[weapon_idx] + " (" + weapon_classes[weapon_idx] + ") >";
    }
    scr_draw_snes_button(_col2_x + 14, _wpn_y + 18, _w_btn_w, 26, _btn_label, _wpn_hov, false, _btn_col);

    // 3. Huge Tactile Cinematic Clash Launcher Button
    var _lch_y = _wpn_y + 56;
    var _lch_w = _col2_w - 28;
    var _lch_h = 52;
    var _lch_hov = (_mx >= _col2_x + 14 && _mx <= _col2_x + 14 + _lch_w && _my >= _lch_y && _my <= _lch_y + _lch_h);

    var _pulse = 0.5 + 0.5 * sin(current_time * 0.008);
    var _border_col = merge_color(make_color_rgb(0, 240, 255), make_color_rgb(255, 180, 40), _pulse);

    if (_lch_hov && _click) {
        launch_full_cinematic_clash();
    }
    scr_draw_snes_button(_col2_x + 14, _lch_y, _lch_w, _lch_h, ">>>> LAUNCH FULL CINEMATIC CLASH DUEL <<<<", _lch_hov, true, _border_col);
}

// =========================================================================
// TAB 1: MECH BUILDER & MODULAR FORGE ENGINEERING DECK
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
        // Base Sprite with Sintered Material Alloy Tint
        draw_sprite_ext(_draw_spr, _sub, _gcx, _gcy + 45, builder_preview_scale, builder_preview_scale, 0, _t.tint, 1.0);

        // Radiant Singularity Masterwork Sheen (S-Tier or Tachyon)
        if (builder_quality_idx == 3 || builder_alloy_idx == 5) {
            gpu_set_blendmode(bm_add);
            draw_sprite_ext(_draw_spr, _sub, _gcx, _gcy + 45, builder_preview_scale, builder_preview_scale, 0, _t.glow, 0.22 + 0.14 * sin(current_time * 0.005));
            gpu_set_blendmode(bm_normal);
        }
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

    // Callsign Banner & Quality Tier Badge
    var _ban_y = _hng_y + 540;
    draw_set_color(make_color_rgb(140, 170, 200));
    draw_text(_hng_x + 20, _ban_y, "CUSTOM CALLSIGN:");
    draw_set_color(make_color_rgb(255, 220, 80));
    draw_text(_hng_x + 165, _ban_y, builder_custom_name);

    draw_set_color(make_color_rgb(140, 170, 200));
    draw_text(_hng_x + 360, _ban_y, "QUALITY TIER:");
    var _q_col = (builder_quality_idx == 3) ? make_color_rgb(255, 100, 255) : ((builder_quality_idx == 2) ? make_color_rgb(255, 220, 80) : ((builder_quality_idx == 1) ? c_aqua : c_white));
    draw_set_color(_q_col);
    draw_text(_hng_x + 470, _ban_y, builder_quality_badges[builder_quality_idx]);

    draw_set_color(make_color_rgb(140, 170, 200));
    draw_text(_hng_x + 20, _ban_y + 24, "FINISH:");
    draw_set_color(_t.glow);
    draw_text(_hng_x + 85, _ban_y + 24, string_copy(_t.alloy_delta.desc, 1, 55));

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

        // Lineage Selector (Active Foundry Lineage Doctrine)
        var _lin_cols = [make_color_rgb(0, 240, 255), make_color_rgb(255, 180, 50), make_color_rgb(200, 80, 255)];
        var _lin_titles = [
            "[FOUNDRY LINEAGE 1: AEGIS VISOR (Wanzer Mil-Spec)]",
            "[FOUNDRY LINEAGE 2: COLOSSUS FORGE (Industrial Dreadnought)]",
            "[FOUNDRY LINEAGE 3: STRATOS VECTOR (Agile Recon Skirmisher)]"
        ];
        var _lin_col = _lin_cols[builder_lineage_idx % 3];
        var _lin_str = _lin_titles[builder_lineage_idx % 3] + " [L]";
        var _lin_hov = (_mx >= _eng_x + 18 && _mx <= _eng_x + _eng_w - 18 && _my >= _deck_y && _my <= _deck_y + 24);
        if (_lin_hov && _click) {
            builder_lineage_idx = (builder_lineage_idx + 1) % 3;
            scr_audio_play_ui("click");
            show_toast("FOUNDRY LINEAGE: " + builder_lineage_badges[builder_lineage_idx], _lin_col);
        }
        scr_draw_snes_button(_eng_x + 18, _deck_y, _eng_w - 36, 24, _lin_str, _lin_hov, true, _lin_col);

        // Platform Line Selector (Player PMC Proprietary vs Reverse-Engineered Factions)
        var _pline_y = _deck_y + 28;
        var _line_str = (builder_chassis_line == 0) ? "[CATALOG: PMC PROPRIETARY FOUNDRY CHASSIS] [T]" : "[CATALOG: REVERSE-ENGINEERED FACTIONS] [T]";
        var _line_col = (builder_chassis_line == 0) ? make_color_rgb(0, 240, 255) : make_color_rgb(255, 180, 50);
        var _line_hov = (_mx >= _eng_x + 18 && _mx <= _eng_x + _eng_w - 18 && _my >= _pline_y && _my <= _pline_y + 24);
        if (_line_hov && _click) {
            builder_chassis_line = (builder_chassis_line == 0) ? 1 : 0;
            builder_chassis_idx = 0;
            var _new_list = get_canonical_chassis_list();
            apply_smart_default_loadout(_new_list[0]);
            scr_audio_play_ui("tab");
        }
        scr_draw_snes_button(_eng_x + 18, _pline_y, _eng_w - 36, 24, _line_str, _line_hov, false, _line_col);

        // Chassis Card
        var _cc_y = _pline_y + 28;
        draw_set_color(make_color_rgb(14, 26, 44));
        draw_rectangle(_eng_x + 18, _cc_y, _eng_x + _eng_w - 18, _cc_y + 160, false);
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_rectangle(_eng_x + 18, _cc_y, _eng_x + _eng_w - 18, _cc_y + 160, true);

        // Name & Model Code
        draw_set_color(make_color_rgb(255, 220, 80));
        draw_text_transformed(_eng_x + 30, _cc_y + 12, _c.name, 1.15, 1.15, 0);

        draw_set_color(make_color_rgb(140, 180, 220));
        draw_text(_eng_x + 30, _cc_y + 40, "Faction: " + _c.faction_id + " | Movement Locomotion: " + string_upper(_c.chassis));

        var _c_pwr = variable_struct_exists(_c, "power_output") ? _c.power_output : _t.power_output;
        var _c_mass = variable_struct_exists(_c, "weight_tonnes") ? _c.weight_tonnes : floor(38 + (_c.hp / 22));
        var _c_spd = variable_struct_exists(_c, "speed") ? _c.speed : 55;

        draw_set_color(c_white);
        draw_text(_eng_x + 30, _cc_y + 64, "Core Power: " + string(_c_pwr) + " MW | Mass: " + string(_c_mass) + " tonnes | Speed: " + string(_c_spd) + " km/h");

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
        draw_text(_eng_x + 20, _qp_y, (builder_chassis_line == 0) ? "BESPOKE PMC PLATFORMS:" : "CAPTURED FACTION SCHEMATICS:");

        var _qnames = (builder_chassis_line == 0) ?
            ["PMC-01: VANGUARD (HEAVY BIPED)", "PMC-02: STRATOS (AERO FIGHTER)", "PMC-03: SCRAPPER (TRACKED SIEGE)", "PMC-04: GHOST (HOVER RECON)", "PMC-00: HEPHAESTUS (FLAGSHIP AVATAR)"] :
            ["IRONCLAD (TERRAN GHA-07)", "AETHER (COLONY STRIKER)", "CENTURION (TERRAN TH-C02)", "KEPLER (COLONY SNIPER)", "HYENA (SYNDICATE RAIDER)"];
        var _qindices = (builder_chassis_line == 0) ? [0, 1, 2, 3, 4] : [0, 6, 1, 7, 12];

        for (var q = 0; q < min(5, array_length(_qnames)); q++) {
            var _qy_pos = _qp_y + 24 + (q * 44);
            var _qhov = (_mx >= _eng_x + 18 && _mx <= _eng_x + _eng_w - 18 && _my >= _qy_pos && _my <= _qy_pos + 36);
            if (_qhov && _click) {
                builder_chassis_idx = _qindices[q] % array_length(_clist);
                apply_smart_default_loadout(_clist[builder_chassis_idx]);
                scr_audio_play_ui("click");
            }
            scr_draw_snes_button(_eng_x + 18, _qy_pos, _eng_w - 36, 36, _qnames[q], _qhov, false, (builder_chassis_line == 0) ? make_color_rgb(0, 240, 255) : make_color_rgb(255, 180, 50));
        }
    }

    // =====================================================================
    // SUBTAB 1: SINTERED ALLOY METALLURGY (10 RECIPES / 50 LOOKS)
    // =====================================================================
    else if (builder_subtab == 1) {
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 20, _deck_y, "SINTERED ALLOY METALLURGY & VISUAL FINISH (10 RECIPES):");

        var _grid_w = 264;
        var _card_h = 100;
        var _start_y = _deck_y + 24;

        for (var a = 0; a < array_length(builder_alloys); a++) {
            var _col = floor(a / 5);
            var _row = a % 5;
            var _ax = _eng_x + 16 + (_col * (_grid_w + 8));
            var _ay = _start_y + (_row * (_card_h + 8));

            var _is_cur_al = (builder_alloy_idx == a);
            var _al_hov = (_mx >= _ax && _mx <= _ax + _grid_w && _my >= _ay && _my <= _ay + _card_h);

            if (_al_hov && _click) {
                builder_alloy_idx = a;
                scr_audio_play_ui("click");
            }

            var _ad = builder_alloy_deltas[a];

            // Card Background & Border
            draw_set_color(_is_cur_al ? make_color_rgb(26, 48, 76) : (_al_hov ? make_color_rgb(18, 30, 48) : make_color_rgb(12, 18, 28)));
            draw_rectangle(_ax, _ay, _ax + _grid_w, _ay + _card_h, false);
            draw_set_color(_is_cur_al ? make_color_rgb(0, 240, 255) : make_color_rgb(45, 68, 98));
            draw_rectangle(_ax, _ay, _ax + _grid_w, _ay + _card_h, true);

            // Color Swatch Indicator (14x14)
            draw_set_color(_ad.tint_color);
            draw_rectangle(_ax + _grid_w - 22, _ay + 8, _ax + _grid_w - 8, _ay + 22, false);
            draw_set_color(_ad.glow_color);
            draw_rectangle(_ax + _grid_w - 22, _ay + 8, _ax + _grid_w - 8, _ay + 22, true);

            // Alloy Name
            draw_set_color(_is_cur_al ? make_color_rgb(255, 220, 80) : c_white);
            var _short_name = string_copy(builder_alloy_names[a], 1, 26);
            draw_text(_ax + 8, _ay + 8, (_is_cur_al ? "> " : "") + _short_name);

            // Stat Multipliers
            draw_set_color(make_color_rgb(150, 190, 230));
            draw_text(_ax + 8, _ay + 28, "Arm: " + string(floor(_ad.armor_mult * 100)) + "% | Mass: " + string(floor(_ad.mass_mult * 100)) + "% | Spd: " + (_ad.speed_bonus >= 0 ? "+" : "") + string(_ad.speed_bonus));

            // Surface Finish Lore
            draw_set_color(_is_cur_al ? _ad.glow_color : make_color_rgb(220, 180, 120));
            var _desc_line1 = string_copy(_ad.desc, 1, 30);
            var _desc_line2 = string_copy(_ad.desc, 31, 32);
            draw_text(_ax + 8, _ay + 50, _desc_line1);
            if (_desc_line2 != "") draw_text(_ax + 8, _ay + 68, _desc_line2);
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

        // Quality Tier Selector
        _ty += 30;
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 28, _ty, "SELECT FORGE CRUCIBLE PURITY / QUALITY TIER:");
        _ty += 22;
        var _qw = (_eng_w - 56 - 18) / 4;
        for (var q = 0; q < 4; q++) {
            var _qx = _eng_x + 28 + (q * (_qw + 6));
            var _q_hov = (_mx >= _qx && _mx <= _qx + _qw && _my >= _ty && _my <= _ty + 30);
            var _q_act = (builder_quality_idx == q);
            if (_q_hov && _click) {
                builder_quality_idx = q;
                scr_audio_play_ui("click");
            }
            var _q_btn_col = (q == 3) ? make_color_rgb(255, 100, 255) : ((q == 2) ? make_color_rgb(255, 220, 80) : ((q == 1) ? c_aqua : c_white));
            scr_draw_snes_button(_qx, _ty, _qw, 30, builder_quality_badges[q], _q_hov || _q_act, _q_act, _q_btn_col);
        }
        _ty += 40;

        // Overload Safety Alert Box
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

// =========================================================================
// TAB 3: PMC CAMPAIGN CHEATS & SYSTEM TOOLS
// =========================================================================
else if (active_debug_tab == 3) {
    var _sec_w = (_win_w - 42) / 2;
    var _sec_h = (_win_h - 64) / 2;

    // Quadrant 1: Treasury & Metallurgy
    var _q1_x = _win_x + 14;
    var _q1_y = _win_y + 44;
    scr_draw_snes_panel(_q1_x, _q1_y, _sec_w, _sec_h, "PMC TREASURY & SINTERED METALLURGY", make_color_rgb(0, 240, 255), true, 0.03);

    var _funds = (instance_exists(obj_GameManager)) ? obj_GameManager.funds : 0;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_q1_x + 18, _q1_y + 30, "CURRENT PMC FUNDS: " + string(_funds) + " CREDITS");

    var _c1_hov = (_mx >= _q1_x + 18 && _mx <= _q1_x + _sec_w - 18 && _my >= _q1_y + 60 && _my <= _q1_y + 92);
    if (_c1_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            obj_GameManager.funds += 100000;
            show_toast("[CHEAT ACTIVE] +100,000 Credits Added to Treasury!", c_lime);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q1_x + 18, _q1_y + 60, _sec_w - 36, 32, "[+] ADD +100,000 CREDITS", _c1_hov, false, c_lime);

    var _c2_hov = (_mx >= _q1_x + 18 && _mx <= _q1_x + _sec_w - 18 && _my >= _q1_y + 102 && _my <= _q1_y + 134);
    if (_c2_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            obj_GameManager.funds += 1000000;
            show_toast("[CHEAT ACTIVE] +1,000,000 Credits Added to Treasury!", c_lime);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q1_x + 18, _q1_y + 102, _sec_w - 36, 32, "[+] ADD +1,000,000 CREDITS", _c2_hov, false, c_lime);

    var _c3_hov = (_mx >= _q1_x + 18 && _mx <= _q1_x + _sec_w - 18 && _my >= _q1_y + 144 && _my <= _q1_y + 176);
    if (_c3_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            var _alloys = ["alloy_vanguard_comp", "alloy_hyperion_matrix", "alloy_aerosteel_flux", "alloy_adamantine_carbide", "alloy_tachyon_superalloy"];
            for (var a = 0; a < array_length(_alloys); a++) {
                obj_GameManager.add_alloy(_alloys[a], 500);
            }
            show_toast("[CHEAT ACTIVE] +500 All 5 Metallurgy Sintered Alloys Added!", c_aqua);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q1_x + 18, _q1_y + 144, _sec_w - 36, 32, "[+] ADD +500 ALL CANON ALLOYS (ALL 5 TIERS)", _c3_hov, false, make_color_rgb(0, 240, 255));

    var _c4_hov = (_mx >= _q1_x + 18 && _mx <= _q1_x + _sec_w - 18 && _my >= _q1_y + 186 && _my <= _q1_y + 218);
    if (_c4_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            var _mats = ["mat_tungsten", "mat_silica_carb", "mat_tritium", "mat_syn_flux", "mat_osmium"];
            for (var m = 0; m < array_length(_mats); m++) {
                obj_GameManager.add_alloy(_mats[m], 2000);
            }
            show_toast("[CHEAT ACTIVE] +2,000 Raw Periodic Minerals Added!", c_aqua);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q1_x + 18, _q1_y + 186, _sec_w - 36, 32, "[+] ADD +2,000 RAW MATERIALS (TUNGSTEN / TRITIUM / SILICA)", _c4_hov, false, make_color_rgb(0, 240, 255));

    // Quadrant 2: R&D, Blueprints & Tech Tree
    var _q2_x = _win_x + 14 + _sec_w + 14;
    var _q2_y = _win_y + 44;
    scr_draw_snes_panel(_q2_x, _q2_y, _sec_w, _sec_h, "R&D, BLUEPRINTS & HOI4 RESEARCH", make_color_rgb(255, 200, 60), true, 0.03);

    var _b1_hov = (_mx >= _q2_x + 18 && _mx <= _q2_x + _sec_w - 18 && _my >= _q2_y + 60 && _my <= _q2_y + 92);
    if (_b1_hov && _click) {
        if (instance_exists(obj_BlueprintManager)) {
            if (is_array(obj_BlueprintManager.all_blueprint_list)) {
                for (var b = 0; b < array_length(obj_BlueprintManager.all_blueprint_list); b++) {
                    var _bp = obj_BlueprintManager.all_blueprint_list[b];
                    if (is_struct(_bp)) variable_struct_set(obj_BlueprintManager.unlocked_blueprints, _bp.id, _bp);
                }
            }
            if (is_struct(obj_BlueprintManager.unlocked_recipes)) {
                var _r_names = variable_struct_get_names(obj_BlueprintManager.unlocked_recipes);
                for (var r = 0; r < array_length(_r_names); r++) {
                    var _rc = variable_struct_get(obj_BlueprintManager.unlocked_recipes, _r_names[r]);
                    if (is_struct(_rc)) _rc.unlocked = true;
                }
            }
            show_toast("[CHEAT ACTIVE] All 100 Blueprints & Sintering Recipes Unlocked!", c_yellow);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q2_x + 18, _q2_y + 60, _sec_w - 36, 32, "[*] UNLOCK ALL 100 CANON BLUEPRINTS & RECIPES", _b1_hov, false, make_color_rgb(255, 200, 60));

    var _b2_hov = (_mx >= _q2_x + 18 && _mx <= _q2_x + _sec_w - 18 && _my >= _q2_y + 102 && _my <= _q2_y + 134);
    if (_b2_hov && _click) {
        var _res_sys = scr_research_get_system();
        if (!is_undefined(_res_sys) && is_struct(_res_sys)) {
            var _slots = _res_sys.active_slots;
            for (var s = 0; s < array_length(_slots); s++) {
                if (_slots[s].tech_id != "") _slots[s].turns_left = 0;
            }
            scr_research_advance_turn();
            show_toast("[CHEAT ACTIVE] Active Research Progress Completed!", c_lime);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q2_x + 18, _q2_y + 102, _sec_w - 36, 32, "[*] INSTANT COMPLETE ACTIVE RESEARCH (TURN ADVANCE)", _b2_hov, false, make_color_rgb(255, 200, 60));

    var _b3_hov = (_mx >= _q2_x + 18 && _mx <= _q2_x + _sec_w - 18 && _my >= _q2_y + 144 && _my <= _q2_y + 176);
    if (_b3_hov && _click) {
        var _res_sys = scr_research_get_system();
        if (!is_undefined(_res_sys) && is_struct(_res_sys)) {
            var _tech_db = scr_research_get_tech_db();
            if (is_struct(_tech_db)) {
                var _t_keys = variable_struct_get_names(_tech_db);
                for (var k = 0; k < array_length(_t_keys); k++) {
                    var _tid = _t_keys[k];
                    if (!scr_research_is_unlocked(_tid)) array_push(_res_sys.unlocked_techs, _tid);
                }
            }
            show_toast("[CHEAT ACTIVE] Entire HOI4 R&D Tech Tree Unlocked!", c_yellow);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q2_x + 18, _q2_y + 144, _sec_w - 36, 32, "[*] UNLOCK ALL TECH NODES (ENTIRE HOI4 TREE)", _b3_hov, false, make_color_rgb(255, 200, 60));

    // Quadrant 3: Narrative & Crisis Incursions
    var _q3_x = _win_x + 14;
    var _q3_y = _win_y + 44 + _sec_h + 10;
    scr_draw_snes_panel(_q3_x, _q3_y, _sec_w, _sec_h, "NARRATIVE & CRISIS INCURSIONS", make_color_rgb(255, 120, 40), true, 0.03);

    var _n1_hov = (_mx >= _q3_x + 18 && _mx <= _q3_x + _sec_w - 18 && _my >= _q3_y + 50 && _my <= _q3_y + 82);
    if (_n1_hov && _click) {
        scr_vn_start_episode("ep_00_cabin_discovery");
        is_open = false;
        scr_audio_play_ui("confirm");
    }
    scr_draw_snes_button(_q3_x + 18, _q3_y + 50, _sec_w - 36, 32, "[>] TRIGGER EPISODE 00: CABIN DISCOVERY (VN)", _n1_hov, false, make_color_rgb(255, 120, 40));

    var _n2_hov = (_mx >= _q3_x + 18 && _mx <= _q3_x + _sec_w - 18 && _my >= _q3_y + 92 && _my <= _q3_y + 124);
    if (_n2_hov && _click) {
        scr_vn_start_episode("ep_01_inauguration");
        is_open = false;
        scr_audio_play_ui("confirm");
    }
    scr_draw_snes_button(_q3_x + 18, _q3_y + 92, _sec_w - 36, 32, "[>] TRIGGER EPISODE 01: INAUGURATION (VN)", _n2_hov, false, make_color_rgb(255, 120, 40));

    var _n3_hov = (_mx >= _q3_x + 18 && _mx <= _q3_x + _sec_w - 18 && _my >= _q3_y + 134 && _my <= _q3_y + 166);
    if (_n3_hov && _click) {
        if (instance_exists(obj_BattleManager)) {
            obj_BattleManager.nemesis_incursion_turn = obj_BattleManager.turn_number;
            obj_BattleManager.nemesis_incursion_checked = false;
            show_toast("[CHEAT ACTIVE] Nemesis Drop-Pod Ambush Forced on Current Combat Turn!", c_orange);
        } else {
            show_toast("[NOTE] Nemesis Ambush will trigger immediately upon entering combat!", c_yellow);
        }
        scr_audio_play_ui("confirm");
    }
    scr_draw_snes_button(_q3_x + 18, _q3_y + 134, _sec_w - 36, 32, "[!] FORCE NEMESIS DROP-POD AMBUSH NEXT COMBAT", _n3_hov, false, c_red);

    // Quadrant 4: Engine Diagnostics & Settings
    var _q4_x = _win_x + 14 + _sec_w + 14;
    var _q4_y = _win_y + 44 + _sec_h + 10;
    scr_draw_snes_panel(_q4_x, _q4_y, _sec_w, _sec_h, "ENGINE DIAGNOSTICS & DISPLAY", make_color_rgb(140, 200, 255), true, 0.03);

    var _d1_hov = (_mx >= _q4_x + 18 && _mx <= _q4_x + _sec_w - 18 && _my >= _q4_y + 50 && _my <= _q4_y + 82);
    if (_d1_hov && _click) {
        var _m = scr_audio_toggle_mute();
        show_toast(_m ? "[AUDIO MUTED]" : "[AUDIO UNMUTED]", _m ? c_orange : c_lime);
    }
    scr_draw_snes_button(_q4_x + 18, _q4_y + 50, _sec_w - 36, 32, "[~] TOGGLE GLOBAL AUDIO MUTE", _d1_hov, false, c_white);

    var _d2_hov = (_mx >= _q4_x + 18 && _mx <= _q4_x + _sec_w - 18 && _my >= _q4_y + 92 && _my <= _q4_y + 124);
    if (_d2_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            obj_GameManager.end_turn();
            show_toast("[ADVANCED TURN] Strategic World Map Turn Processed!", c_aqua);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q4_x + 18, _q4_y + 92, _sec_w - 36, 32, "[~] ADVANCE GLOBAL STRATEGIC TURN", _d2_hov, false, c_white);

    var _d3_hov = (_mx >= _q4_x + 18 && _mx <= _q4_x + _sec_w - 18 && _my >= _q4_y + 134 && _my <= _q4_y + 166);
    if (_d3_hov && _click) {
        show_debug_message("[DEBUG] Master Roster Count: " + string(array_length(master_roster)));
        show_toast("[TELEMETRY] DUMPED 100+ UNITS TO DEBUG CONSOLE", c_lime);
        scr_audio_play_ui("confirm");
    }
    scr_draw_snes_button(_q4_x + 18, _q4_y + 134, _sec_w - 36, 32, "[?] PRINT CATALOG TELEMETRY TO DEBUG LOG", _d3_hov, false, c_white);
}

// Glowing Notification Toast
if (debug_toast_timer > 0) {
    var _t_alpha = min(1.0, debug_toast_timer / 30.0);
    draw_set_alpha(_t_alpha);
    draw_set_color(make_color_rgb(14, 22, 34));
    draw_rectangle(_win_x + 20, _win_y + _win_h - 44, _win_x + _win_w - 20, _win_y + _win_h - 10, false);
    draw_set_color(debug_toast_color);
    draw_rectangle(_win_x + 20, _win_y + _win_h - 44, _win_x + _win_w - 20, _win_y + _win_h - 10, true);
    draw_text(_win_x + 36, _win_y + _win_h - 34, debug_toast);
    draw_set_alpha(1.0);
}
