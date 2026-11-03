#!/usr/bin/env python3
import os

print("[GALACTIC MAP] Building Clean, Focused Galactic Map UI for obj_HQTerminal...")

# 1. Update Create_0.gml
path_create = "objects/obj_HQTerminal/Create_0.gml"
with open(path_create, "r", encoding="utf-8") as f:
    create_gml = f.read()

# Disable intro modal blocking by default so player starts directly on Galactic Map
create_gml = create_gml.replace(
    "intro_active = (instance_exists(obj_GameManager) && !obj_GameManager.has_completed_intro);",
    "intro_active = false; // Directly start on Galactic Map\nshow_commander_modal = false;"
)
create_gml = create_gml.replace(
    "active_tab = 0;",
    "active_tab = 3; // Galactic Map"
)

with open(path_create, "w", encoding="utf-8") as f:
    f.write(create_gml)
print("✓ obj_HQTerminal/Create_0.gml updated to start directly on Galactic Map.")

# 2. Update Step_0.gml
path_step = "objects/obj_HQTerminal/Step_0.gml"
with open(path_step, "r", encoding="utf-8") as f:
    step_gml = f.read()

# Ensure hotkeys 1, 2, 3 switch theaters (Earth, Space, Mars)
hotkeys_code = '''// Direct Number Keys 1-3 for Galactic Theaters (Earth, Space, Mars)
if (!show_settings_modal) {
    if (keyboard_check_pressed(ord("1"))) {
        territory_sphere_tab = 0;
        selected_territory_id = "earth_granite_redoubt";
        scr_audio_play_ui("tab");
    }
    if (keyboard_check_pressed(ord("2"))) {
        territory_sphere_tab = 1;
        selected_territory_id = "space_kepler_haven";
        scr_audio_play_ui("tab");
    }
    if (keyboard_check_pressed(ord("3"))) {
        territory_sphere_tab = 2;
        selected_territory_id = "mars_olympus_caldera";
        scr_audio_play_ui("tab");
    }
    if (keyboard_check_pressed(ord("S")) || keyboard_check_pressed(ord("C"))) {
        if (room_exists(rm_combat)) {
            scr_audio_play_ui("confirm");
            room_goto(rm_combat);
        }
    }
    if (keyboard_check_pressed(vk_space)) {
        if (instance_exists(obj_GameManager)) {
            obj_GameManager.end_turn();
        }
    }
}'''

# Replace old number keys block if present
old_keys_marker = "// Direct Number Keys 1-5 for Command Deck Tab Navigation"
if old_keys_marker in step_gml:
    lines = step_gml.splitlines()
    new_lines = []
    skipping = False
    for line in lines:
        if old_keys_marker in line:
            skipping = True
            new_lines.append(hotkeys_code)
            continue
        if skipping:
            if line.startswith("}"):
                skipping = False
            continue
        new_lines.append(line)
    step_gml = "\n".join(new_lines)

with open(path_step, "w", encoding="utf-8") as f:
    f.write(step_gml)
print("✓ obj_HQTerminal/Step_0.gml updated with Galactic Theater hotkeys [1] Earth, [2] Space, [3] Mars.")

# 3. Create the Clean Galactic Map in Draw_64.gml
clean_draw_64 = '''/// @description obj_HQTerminal Draw GUI Event - CLEAN GALACTIC MAP INTERFACE
// High-clarity, retro-tactical Galactic Theater Map inspired by Gihren's Greed & Front Mission

var _gw = display_get_gui_width();
var _gh = display_get_gui_height();
var _mx = device_mouse_x_to_gui(0);
var _my = device_mouse_y_to_gui(0);
var _click = mouse_check_button_pressed(mb_left);
var _down = mouse_check_button(mb_left);

var _sx = random_range(-crucible_shake, crucible_shake);
var _sy = random_range(-crucible_shake, crucible_shake);

// =========================================================================
// 1. DEEP SPACE BACKDROP & SECTOR MAP ARTWORK
// =========================================================================
draw_set_color(make_color_rgb(8, 12, 18));
draw_rectangle(0, 0, _gw, _gh, false);

if (sprite_exists(spr_space_sector_map)) {
    draw_sprite_ext(spr_space_sector_map, 0, 0, 0, _gw / 1024.0, _gh / 576.0, 0, c_white, 0.32);
}

// Tactical Coordinate Grid
draw_set_color(make_color_rgb(16, 24, 36));
for (var gx = 0; gx < _gw; gx += 48) draw_line(gx, 0, gx, _gh);
for (var gy = 0; gy < _gh; gy += 48) draw_line(0, gy, _gw, gy);

// =========================================================================
// 2. TOP TACTICAL COMMAND BAR (y: 6 to 56)
// =========================================================================
var _top_y = 6;
var _top_h = 48;
draw_set_color(make_color_rgb(12, 18, 28));
draw_rectangle(16 + _sx, _top_y + _sy, _gw - 16 + _sx, _top_y + _top_h + _sy, false);
draw_set_color(make_color_rgb(35, 60, 95));
draw_rectangle(16 + _sx, _top_y + _sy, _gw - 16 + _sx, _top_y + _top_h + _sy, true);

// Left Accent Line
draw_set_color(make_color_rgb(0, 220, 255));
draw_rectangle(16 + _sx, _top_y + _sy, 20 + _sx, _top_y + _top_h + _sy, false);

// PMC Title & Theater
draw_set_color(make_color_rgb(0, 240, 255));
draw_text(28 + _sx, _top_y + 8 + _sy, "IRON RIDGE PMC // GALACTIC THEATER WAR MAP");
draw_set_color(make_color_rgb(140, 175, 215));
draw_text(28 + _sx, _top_y + 26 + _sy, "TACTICAL COMMAND & FACTION CONQUEST SYSTEM");

// Economic & Cycle Ticker
var _gm = instance_exists(obj_GameManager) ? obj_GameManager : undefined;
var _funds_val = !is_undefined(_gm) ? _gm.funds : 100000;
var _turn_val = !is_undefined(_gm) ? _gm.current_turn : 1;
var _year_val = !is_undefined(_gm) ? _gm.current_cycle_year : 214;

// Format Funds String with commas
var _f_str = string(_funds_val);
var _f_len = string_length(_f_str);
var _funds_formatted = "";
for (var _fi = 1; _fi <= _f_len; _fi++) {
    _funds_formatted += string_char_at(_f_str, _fi);
    if ((_f_len - _fi) % 3 == 0 && _fi != _f_len) _funds_formatted += ",";
}
_funds_formatted += " Cr";

// Funds Readout
draw_set_color(make_color_rgb(20, 32, 48));
draw_rectangle(450 + _sx, _top_y + 6 + _sy, 640 + _sx, _top_y + _top_h - 6 + _sy, false);
draw_set_color(make_color_rgb(40, 75, 115));
draw_rectangle(450 + _sx, _top_y + 6 + _sy, 640 + _sx, _top_y + _top_h - 6 + _sy, true);
draw_set_color(make_color_rgb(80, 240, 140));
draw_text(462 + _sx, _top_y + 14 + _sy, "FUNDS: " + _funds_formatted);

// Calendar Readout
draw_set_color(make_color_rgb(20, 32, 48));
draw_rectangle(650 + _sx, _top_y + 6 + _sy, 820 + _sx, _top_y + _top_h - 6 + _sy, false);
draw_set_color(make_color_rgb(40, 75, 115));
draw_rectangle(650 + _sx, _top_y + 6 + _sy, 820 + _sx, _top_y + _top_h - 6 + _sy, true);
draw_set_color(make_color_rgb(255, 215, 80));
draw_text(662 + _sx, _top_y + 14 + _sy, "YEAR " + string(_year_val) + " · DAY " + string(_turn_val));

// --- TOP RIGHT DIRECT ACTION BUTTONS ---
var _btn_h = 36;
var _btn_y = _top_y + 6;

// 1. Advance Day Button
var _adv_x = 832;
var _adv_w = 176;
var _adv_hov = (_mx >= _adv_x && _mx <= _adv_x + _adv_w && _my >= _btn_y && _my <= _btn_y + _btn_h);
if (_adv_hov && _click && !is_undefined(_gm)) {
    _gm.end_turn();
}
draw_set_color(_adv_hov ? make_color_rgb(20, 70, 40) : make_color_rgb(12, 38, 22));
draw_rectangle(_adv_x + _sx, _btn_y + _sy, _adv_x + _adv_w + _sx, _btn_y + _btn_h + _sy, false);
draw_set_color(_adv_hov ? make_color_rgb(80, 255, 150) : make_color_rgb(45, 190, 100));
draw_rectangle(_adv_x + _sx, _btn_y + _sy, _adv_x + _adv_w + _sx, _btn_y + _btn_h + _sy, true);
draw_set_color(c_white);
draw_text(_adv_x + 12 + _sx, _btn_y + 10 + _sy, ">> ADVANCE DAY [SPACE]");

// 2. Sortie Combat Button
var _sort_x = 1016;
var _sort_w = 154;
var _sort_hov = (_mx >= _sort_x && _mx <= _sort_x + _sort_w && _my >= _btn_y && _my <= _btn_y + _btn_h);
if (_sort_hov && _click && room_exists(rm_combat)) {
    scr_audio_play_ui("confirm");
    room_goto(rm_combat);
}
draw_set_color(_sort_hov ? make_color_rgb(80, 50, 10) : make_color_rgb(38, 24, 8));
draw_rectangle(_sort_x + _sx, _btn_y + _sy, _sort_x + _sort_w + _sx, _btn_y + _btn_h + _sy, false);
draw_set_color(_sort_hov ? make_color_rgb(255, 210, 60) : make_color_rgb(210, 150, 40));
draw_rectangle(_sort_x + _sx, _btn_y + _sy, _sort_x + _sort_w + _sx, _btn_y + _btn_h + _sy, true);
draw_set_color(make_color_rgb(255, 225, 100));
draw_text(_sort_x + 10 + _sx, _btn_y + 10 + _sy, "⚔️ SORTIE [S]");

// 3. Audio Mute Toggle Button
var _mute_x = 1178;
var _mute_w = 78;
var _is_aud_muted = scr_audio_is_muted();
var _mute_hov = (_mx >= _mute_x && _mx <= _mute_x + _mute_w && _my >= _btn_y && _my <= _btn_y + _btn_h);
if (_mute_hov && _click) {
    var _nm = scr_audio_toggle_mute();
    show_toast(_nm ? "[AUDIO MUTED]" : "[AUDIO UNMUTED]", _nm ? c_orange : c_lime);
}
draw_set_color(_mute_hov ? (_is_aud_muted ? make_color_rgb(70, 22, 22) : make_color_rgb(20, 60, 40)) : (_is_aud_muted ? make_color_rgb(40, 14, 14) : make_color_rgb(12, 32, 22)));
draw_rectangle(_mute_x + _sx, _btn_y + _sy, _mute_x + _mute_w + _sx, _btn_y + _btn_h + _sy, false);
draw_set_color(_mute_hov ? (_is_aud_muted ? make_color_rgb(255, 100, 100) : make_color_rgb(100, 255, 160)) : (_is_aud_muted ? make_color_rgb(220, 60, 60) : make_color_rgb(50, 190, 100)));
draw_rectangle(_mute_x + _sx, _btn_y + _sy, _mute_x + _mute_w + _sx, _btn_y + _btn_h + _sy, true);
draw_set_color(_is_aud_muted ? make_color_rgb(255, 130, 130) : make_color_rgb(130, 255, 170));
draw_text(_mute_x + 8 + _sx, _btn_y + 10 + _sy, _is_aud_muted ? "[🔇 MUTE]" : "[🔊 100%]");

// 4. Settings Config Button
var _cfg_x = 1262;
var _cfg_w = 88;
var _cfg_hov = (_mx >= _cfg_x && _mx <= _cfg_x + _cfg_w && _my >= _btn_y && _my <= _btn_y + _btn_h);
if (_cfg_hov && _click) {
    show_settings_modal = !show_settings_modal;
    scr_audio_play_ui("click");
}
draw_set_color(_cfg_hov ? make_color_rgb(20, 48, 70) : make_color_rgb(12, 22, 34));
draw_rectangle(_cfg_x + _sx, _btn_y + _sy, _cfg_x + _cfg_w + _sx, _btn_y + _btn_h + _sy, false);
draw_set_color(_cfg_hov ? make_color_rgb(100, 220, 255) : make_color_rgb(55, 130, 190));
draw_rectangle(_cfg_x + _sx, _btn_y + _sy, _cfg_x + _cfg_w + _sx, _btn_y + _btn_h + _sy, true);
draw_set_color(make_color_rgb(120, 220, 255));
draw_text(_cfg_x + 8 + _sx, _btn_y + 10 + _sy, "[⚙ CONFIG]");

// =========================================================================
// 3. CELESTIAL THEATER NAVIGATION TABS (y: 60 to 92)
// =========================================================================
var _theaters = [
    "[1. EARTH SPHERE // 10 CITADELS]",
    "[2. SPACE & COLONIES // 15 SECTORS]",
    "[3. MARS & ASTEROIDS // 8 REDOUBTS]"
];
var _th_x = 16;
var _th_y = 60;
var _th_w = 300;
var _th_h = 32;

for (var th = 0; th < 3; th++) {
    var _bx = _th_x + th * (_th_w + 10);
    var _is_act = (territory_sphere_tab == th);
    var _th_hov = (_mx >= _bx && _mx <= _bx + _th_w && _my >= _th_y && _my <= _th_y + _th_h);

    if (_th_hov && _click) {
        territory_sphere_tab = th;
        scr_audio_play_ui("tab");
        if (th == 0) selected_territory_id = "earth_granite_redoubt";
        else if (th == 1) selected_territory_id = "space_kepler_haven";
        else if (th == 2) selected_territory_id = "mars_olympus_caldera";
    }

    draw_set_color(_is_act ? make_color_rgb(28, 62, 98) : (_th_hov ? make_color_rgb(18, 38, 62) : make_color_rgb(12, 18, 28)));
    draw_rectangle(_bx + _sx, _th_y + _sy, _bx + _th_w + _sx, _th_y + _th_h + _sy, false);
    draw_set_color(_is_act ? make_color_rgb(0, 240, 255) : (_th_hov ? make_color_rgb(100, 200, 255) : make_color_rgb(40, 70, 105)));
    draw_rectangle(_bx + _sx, _th_y + _sy, _bx + _th_w + _sx, _th_y + _th_h + _sy, true);

    if (_is_act) {
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_rectangle(_bx + _sx, _th_y + _th_h - 3 + _sy, _bx + _th_w + _sx, _th_y + _th_h + _sy, false);
    }

    draw_set_color(_is_act ? c_white : make_color_rgb(160, 190, 220));
    draw_text(_bx + 14 + _sx, _th_y + 8 + _sy, _theaters[th]);
}

// Current Region Key
var _region_str = (territory_sphere_tab == 0) ? "EARTH" : ((territory_sphere_tab == 1) ? "SPACE" : "MARS");

// =========================================================================
// 4. MAIN INTERACTIVE TACTICAL RADAR CANVAS (x: 16 to 970, y: 98 to 694)
// =========================================================================
var _rad_x = 16;
var _rad_y = 98;
var _rad_w = 954;
var _rad_h = 596;

scr_draw_snes_panel(_rad_x, _rad_y, _rad_w, _rad_h, _region_str + " THEATER TACTICAL RADAR", make_color_rgb(60, 180, 240), true);

var _fm = instance_exists(obj_FactionManager) ? obj_FactionManager : undefined;
var _mars_locked = (_region_str == "MARS" && (!is_undefined(_fm) && !_fm.mars_unlocked));

if (_mars_locked) {
    // Red Crypt Blackout
    draw_set_color(make_color_rgb(24, 10, 14));
    draw_rectangle(_rad_x + 12, _rad_y + 26, _rad_x + _rad_w - 12, _rad_y + _rad_h - 12, false);
    draw_set_color(make_color_rgb(180, 40, 50));
    draw_rectangle(_rad_x + 12, _rad_y + 26, _rad_x + _rad_w - 12, _rad_y + _rad_h - 12, true);

    draw_set_color(make_color_rgb(255, 60, 60));
    draw_text(_rad_x + 40, _rad_y + 60, "⚠ THARSIS SENSOR BLACKOUT // PROTOCOL OMEGA ACTIVE ⚠");
    draw_set_color(c_white);
    draw_text(_rad_x + 40, _rad_y + 90, "Martian orbital space is completely restricted under Sol Security Directives.");
    draw_set_color(make_color_rgb(255, 180, 180));
    draw_text(_rad_x + 40, _rad_y + 115, "Tharsis Machine Consensus awakes when global tensions reach critical mass.");

    var _ovr_x = _rad_x + 40;
    var _ovr_y = _rad_y + 240;
    var _ovr_w = 420;
    var _ovr_h = 44;
    var _ovr_hov = (_mx >= _ovr_x && _mx <= _ovr_x + _ovr_w && _my >= _ovr_y && _my <= _ovr_y + _ovr_h);
    if (_ovr_hov && _click) {
        scr_territory_unlock_mars();
        scr_audio_play_ui("confirm");
    }
    scr_draw_snes_button(_ovr_x, _ovr_y, _ovr_w, _ovr_h, ">> OVERRIDE SENSOR LOCK // REVEAL MARS >>", _ovr_hov, false, make_color_rgb(255, 80, 80));
} else {
    // Background Tactical Grid Lines
    draw_set_color(make_color_rgb(18, 30, 46));
    for (var gx = _rad_x + 40; gx < _rad_x + _rad_w - 20; gx += 64) {
        draw_line(gx, _rad_y + 26, gx, _rad_y + _rad_h - 12);
    }
    for (var gy = _rad_y + 40; gy < _rad_y + _rad_h - 12; gy += 48) {
        draw_line(_rad_x + 12, gy, _rad_x + _rad_w - 12, gy);
    }

    // Range Radar Circles
    var _rcx = _rad_x + _rad_w / 2;
    var _rcy = _rad_y + _rad_h / 2;
    draw_set_color(make_color_rgb(22, 40, 60));
    draw_circle(_rcx, _rcy, 140, true);
    draw_circle(_rcx, _rcy, 250, true);

    var _t_list = scr_territory_get_by_region(_region_str);

    // Pass 1: Hyperlane Supply Lines
    for (var ti = 0; ti < array_length(_t_list); ti++) {
        var _t1 = _t_list[ti];
        var _tx1 = _rad_x + 40 + floor(_t1.map_x * 1.34);
        var _ty1 = _rad_y + 48 + floor(_t1.map_y * 1.48);
        for (var ci = 0; ci < array_length(_t1.connected_ids); ci++) {
            var _t2 = scr_territory_get(_t1.connected_ids[ci]);
            if (!is_undefined(_t2) && _t2.region == _region_str) {
                var _tx2 = _rad_x + 40 + floor(_t2.map_x * 1.34);
                var _ty2 = _rad_y + 48 + floor(_t2.map_y * 1.48);
                var _is_contested = (_t1.controlling_faction != _t2.controlling_faction);
                draw_set_color(_is_contested ? make_color_rgb(220, 60, 60) : make_color_rgb(35, 75, 105));
                draw_set_alpha(_is_contested ? 0.85 : 0.45);
                draw_line_width(_tx1, _ty1, _tx2, _ty2, _is_contested ? 2 : 1);
                draw_set_alpha(1.0);
            }
        }
    }

    // Pass 2: Interactive Territory Nodes
    for (var ti = 0; ti < array_length(_t_list); ti++) {
        var _t = _t_list[ti];
        var _nx = _rad_x + 40 + floor(_t.map_x * 1.34);
        var _ny = _rad_y + 48 + floor(_t.map_y * 1.48);
        var _nw = 96;
        var _nh = 36;
        var _is_sel = (selected_territory_id == _t.id);
        var _is_front = scr_territory_is_frontline(_t.id);
        var _hov = (_mx >= _nx - _nw/2 && _mx <= _nx + _nw/2 && _my >= _ny - _nh/2 && _my <= _ny + _nh/2);

        if (_hov && _click) {
            selected_territory_id = _t.id;
            scr_audio_play_ui("click");
        }

        // Controlling Faction Color
        var _f_col = make_color_rgb(60, 140, 255); // Terran Blue
        if (_t.controlling_faction == "faction_b") _f_col = make_color_rgb(40, 220, 180); // Colony Teal
        else if (_t.controlling_faction == "faction_c") _f_col = make_color_rgb(255, 140, 40); // Syndicate Gold
        else if (_t.controlling_faction == "faction_d") _f_col = make_color_rgb(180, 90, 240); // Zaibatsu Purple
        else if (_t.controlling_faction == "faction_e") _f_col = make_color_rgb(120, 130, 240); // Sovereign Ruby
        else if (_t.controlling_faction == "faction_f") _f_col = make_color_rgb(240, 60, 60); // Mars Consensus Crimson
        else if (_t.controlling_faction == "pmc") _f_col = make_color_rgb(255, 215, 60); // PMC Gold

        // Frontline Alert Reticle
        if (_is_front) {
            var _pls = 0.5 + 0.5 * sin(current_time * 0.008);
            draw_set_color(merge_color(c_red, c_yellow, _pls));
            draw_rectangle(_nx - _nw/2 - 3, _ny - _nh/2 - 3, _nx + _nw/2 + 3, _ny + _nh/2 + 3, true);
        }

        // Node Box
        draw_set_color(_hov ? make_color_rgb(28, 44, 68) : make_color_rgb(14, 20, 30));
        draw_rectangle(_nx - _nw/2, _ny - _nh/2, _nx + _nw/2, _ny + _nh/2, false);
        draw_set_color(_is_sel ? c_white : _f_col);
        draw_rectangle(_nx - _nw/2, _ny - _nh/2, _nx + _nw/2, _ny + _nh/2, true);

        // Indicator Bar
        draw_set_color(_f_col);
        draw_rectangle(_nx - _nw/2, _ny - _nh/2, _nx - _nw/2 + 4, _ny + _nh/2, false);

        draw_set_halign(fa_center);
        draw_set_color(_is_sel ? c_white : make_color_rgb(220, 240, 255));
        draw_text(_nx, _ny - 14, string_copy(_t.name, 1, 12));
        draw_set_color(make_color_rgb(100, 255, 160));
        draw_text(_nx, _ny + 2, "+" + string(_t.daily_materials) + "kg " + string_upper(string_copy(_t.material_type, 1, 4)));
        draw_set_halign(fa_left);
    }
}

// =========================================================================
// 5. SELECTED SECTOR TACTICAL DOSSIER (x: 982 to 1350, y: 98 to 694)
// =========================================================================
var _dos_x = 982;
var _dos_y = 98;
var _dos_w = _gw - _dos_x - 16;
var _dos_h = _rad_h;

var _cur_t = scr_territory_get(selected_territory_id);
if (is_undefined(_cur_t)) {
    var _fallback_list = scr_territory_get_by_region(_region_str);
    if (array_length(_fallback_list) > 0) {
        _cur_t = _fallback_list[0];
        selected_territory_id = _cur_t.id;
    }
}

if (!is_undefined(_cur_t)) {
    scr_draw_snes_panel(_dos_x, _dos_y, _dos_w, _dos_h, "TACTICAL SECTOR DOSSIER", make_color_rgb(100, 200, 255), true);

    // Sector Name
    draw_set_color(make_color_rgb(255, 220, 90));
    draw_text(_dos_x + 16, _dos_y + 26, string_upper(_cur_t.name));
    draw_set_color(make_color_rgb(140, 175, 210));
    draw_text(_dos_x + 16, _dos_y + 44, _cur_t.region + " // " + _cur_t.subregion);

    // Controlling Faction Identification
    var _owner_name = "Independent";
    var _f_col = make_color_rgb(60, 140, 255);
    if (_cur_t.controlling_faction == "pmc") {
        _owner_name = "PMC Sovereign Dominion (Player)";
        _f_col = make_color_rgb(255, 215, 60);
    } else if (!is_undefined(_fm) && variable_struct_exists(_fm.factions, _cur_t.controlling_faction)) {
        var _fentry = variable_struct_get(_fm.factions, _cur_t.controlling_faction);
        if (!is_undefined(_fentry)) {
            _owner_name = _fentry.name + " (" + _fentry.short_name + ")";
        }
        if (_cur_t.controlling_faction == "faction_b") _f_col = make_color_rgb(40, 220, 180);
        else if (_cur_t.controlling_faction == "faction_c") _f_col = make_color_rgb(255, 140, 40);
        else if (_cur_t.controlling_faction == "faction_d") _f_col = make_color_rgb(180, 90, 240);
        else if (_cur_t.controlling_faction == "faction_e") _f_col = make_color_rgb(120, 130, 240);
        else if (_cur_t.controlling_faction == "faction_f") _f_col = make_color_rgb(240, 60, 60);
    }

    // Sovereign Banner Box
    draw_set_color(make_color_rgb(14, 22, 32));
    draw_rectangle(_dos_x + 16, _dos_y + 64, _dos_x + _dos_w - 16, _dos_y + 118, false);
    draw_set_color(_f_col);
    draw_rectangle(_dos_x + 16, _dos_y + 64, _dos_x + _dos_w - 16, _dos_y + 118, true);
    draw_rectangle(_dos_x + 16, _dos_y + 64, _dos_x + 20, _dos_y + 118, false);

    draw_set_color(_f_col);
    draw_text(_dos_x + 26, _dos_y + 70, "CONTROLLER: " + _owner_name);
    draw_set_color(make_color_rgb(80, 255, 140));
    draw_text(_dos_x + 26, _dos_y + 92, "DAILY YIELD: +" + string(_cur_t.daily_credits) + " Cr / +" + string(_cur_t.daily_materials) + "kg " + string_upper(_cur_t.material_type));

    // Fortification Rating Bar
    var _def_y = _dos_y + 128;
    draw_set_color(make_color_rgb(200, 220, 245));
    draw_text(_dos_x + 16, _def_y, "DEFENSE FORTIFICATION: " + string(_cur_t.defense_rating) + " / 100");

    var _dbar_w = _dos_w - 32;
    draw_set_color(make_color_rgb(20, 28, 40));
    draw_rectangle(_dos_x + 16, _def_y + 20, _dos_x + 16 + _dbar_w, _def_y + 32, false);
    var _dfill = floor(_dbar_w * (_cur_t.defense_rating / 100.0));
    draw_set_color(make_color_rgb(0, 220, 255));
    draw_rectangle(_dos_x + 16, _def_y + 20, _dos_x + 16 + _dfill, _def_y + 32, false);
    draw_set_color(make_color_rgb(50, 80, 120));
    draw_rectangle(_dos_x + 16, _def_y + 20, _dos_x + 16 + _dbar_w, _def_y + 32, true);

    // Frontline Combat Alert
    var _is_front = scr_territory_is_frontline(_cur_t.id);
    var _f_alert_y = _def_y + 44;
    draw_set_color(_is_front ? make_color_rgb(255, 80, 80) : make_color_rgb(80, 220, 140));
    draw_text(_dos_x + 16, _f_alert_y, _is_front ? "★ CONTESTED FRONTLINE BATTLEGROUND" : "✓ SECURE TERRITORIAL SECTOR");

    draw_set_color(make_color_rgb(180, 210, 240));
    draw_text(_dos_x + 16, _f_alert_y + 20, "Garrison Forces: " + _cur_t.garrison_unit);

    // Tactical Lore Brief
    draw_set_color(make_color_rgb(160, 190, 220));
    draw_text_ext(_dos_x + 16, _f_alert_y + 48, _cur_t.lore_brief, 15, _dos_w - 32);

    draw_set_color(make_color_rgb(255, 215, 80));
    draw_text_ext(_dos_x + 16, _f_alert_y + 140, "Strategic Asset: " + _cur_t.strategic_value, 15, _dos_w - 32);

    // --- SECTOR DIRECT ACTIONS ---
    var _act_y = _dos_y + _dos_h - 100;
    var _act_w = _dos_w - 32;

    if (_cur_t.controlling_faction == "pmc") {
        var _fort_hov = (_mx >= _dos_x + 16 && _mx <= _dos_x + 16 + _act_w && _my >= _act_y && _my <= _act_y + 38);
        if (_fort_hov && _click) {
            scr_territory_fortify(_cur_t.id);
        }
        scr_draw_snes_button(_dos_x + 16, _act_y, _act_w, 38, ">> FORTIFY SECTOR (+10 DEF: $25K) >>", _fort_hov, false, make_color_rgb(80, 240, 140));
    } else {
        var _raid_hov = (_mx >= _dos_x + 16 && _mx <= _dos_x + 16 + _act_w && _my >= _act_y && _my <= _act_y + 38);
        if (_raid_hov && _click) {
            scr_territory_launch_pmc_assault(_cur_t.id, 0, 0);
        }
        scr_draw_snes_button(_dos_x + 16, _act_y, _act_w, 38, ">> DISPATCH PMC ASSAULT EXPEDITION >>", _raid_hov, false, make_color_rgb(255, 180, 60));
    }

    // Direct Sortie into Combat on this sector
    var _sort_sec_y = _act_y + 46;
    var _sort_sec_hov = (_mx >= _dos_x + 16 && _mx <= _dos_x + 16 + _act_w && _my >= _sort_sec_y && _my <= _sort_sec_y + 38);
    if (_sort_sec_hov && _click && room_exists(rm_combat)) {
        scr_audio_play_ui("confirm");
        room_goto(rm_combat);
    }
    scr_draw_snes_button(_dos_x + 16, _sort_sec_y, _act_w, 38, "⚔️ SORTIE COMBAT SQUAD HERE", _sort_sec_hov, false, make_color_rgb(255, 100, 100));
}

// =========================================================================
// 6. BOTTOM GALACTIC HEGEMONY & BALANCE OF POWER STRIP (y: 704 to 756)
// =========================================================================
var _bot_x = 16;
var _bot_y = 704;
var _bot_w = _gw - 32;
var _bot_h = 52;

draw_set_color(make_color_rgb(10, 16, 24));
draw_rectangle(_bot_x + _sx, _bot_y + _sy, _bot_x + _bot_w + _sx, _bot_y + _bot_h + _sy, false);
draw_set_color(make_color_rgb(35, 60, 90));
draw_rectangle(_bot_x + _sx, _bot_y + _sy, _bot_x + _bot_w + _sx, _bot_y + _bot_h + _sy, true);

if (!is_undefined(_fm)) {
    var _tc = _fm.territory_control;

    // Multi-Segment Color Bar
    var _bar_x = _bot_x + 14;
    var _bar_y = _bot_y + 8;
    var _bar_w = _bot_w - 28;
    var _bar_h = 14;

    draw_set_color(make_color_rgb(20, 25, 35));
    draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_w, _bar_y + _bar_h, false);

    var _cur_bx = _bar_x;
    var _segs = [
        { pct: _tc.terran_pct, col: make_color_rgb(60, 140, 255) },
        { pct: _tc.colony_pct, col: make_color_rgb(40, 220, 180) },
        { pct: _tc.syndicate_pct, col: make_color_rgb(255, 140, 40) },
        { pct: _tc.zaibatsu_pct, col: make_color_rgb(180, 90, 240) },
        { pct: _tc.astran_pct, col: make_color_rgb(120, 130, 240) },
        { pct: _tc.martian_pct, col: make_color_rgb(240, 60, 60) },
        { pct: _tc.pmc_pct, col: make_color_rgb(255, 215, 60) }
    ];
    for (var sg = 0; sg < array_length(_segs); sg++) {
        var _sw = _bar_w * (_segs[sg].pct / 100.0);
        if (_sw > 0) {
            draw_set_color(_segs[sg].col);
            draw_rectangle(_cur_bx, _bar_y, _cur_bx + _sw, _bar_y + _bar_h, false);
            _cur_bx += _sw;
        }
    }
    draw_set_color(make_color_rgb(60, 90, 130));
    draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_w, _bar_y + _bar_h, true);

    // Text Breakdown
    draw_set_color(make_color_rgb(180, 210, 255));
    draw_text(_bot_x + 14, _bot_y + 28, "Terran: " + string(_tc.terran_pct) + "% · Colonies: " + string(_tc.colony_pct) + "% · Syndicates: " + string(_tc.syndicate_pct) + "% · Zaibatsu: " + string(_tc.zaibatsu_pct) + "% · Sovereign: " + string(_tc.astran_pct) + "% · Mars: " + string(_tc.martian_pct) + "% · PMC: " + string(_tc.pmc_pct) + "%");

    draw_set_color(make_color_rgb(255, 215, 60));
    var _pmc_trib = _tc.pmc_pct * 3500;
    draw_text(_bot_x + 920, _bot_y + 28, "PMC Logistics Yield: +" + string(_pmc_trib) + " Cr/day");
}

// =========================================================================
// 7. TOAST FEEDBACK NOTIFICATIONS
// =========================================================================
if (toast_timer > 0) {
    var _tw = 400;
    var _th_t = 36;
    var _tx = floor((_gw - _tw) / 2);
    var _ty = 70;
    draw_set_color(make_color_rgb(16, 24, 36));
    draw_rectangle(_tx, _ty, _tx + _tw, _ty + _th_t, false);
    draw_set_color(toast_color);
    draw_rectangle(_tx, _ty, _tx + _tw, _ty + _th_t, true);
    draw_set_halign(fa_center);
    draw_set_color(toast_color);
    draw_text(_tx + _tw / 2, _ty + 10, toast_message);
    draw_set_halign(fa_left);
}

// =========================================================================
// 8. SYSTEM CONFIGURATION & TACTICAL AUDIO MODAL (LEAD AUDIO ENGINEER SPEC)
// =========================================================================
if (show_settings_modal) {
    draw_set_alpha(0.80);
    draw_set_color(c_black);
    draw_rectangle(0, 0, 1366, 768, false);
    draw_set_alpha(1.0);

    var _mw = 800;
    var _mh = 540;
    var _mx0 = floor((1366 - _mw) / 2);
    var _my0 = floor((768 - _mh) / 2);

    scr_draw_snes_panel(_mx0, _my0, _mw, _mh, "TERMINAL CONFIGURATION // AUDIO & SYSTEM SETTINGS", 0, true, 0.08);

    // Close Button [X]
    var _close_x = _mx0 + _mw - 44;
    var _close_y = _my0 + 8;
    var _close_hov = (_mx >= _close_x && _mx <= _close_x + 32 && _my >= _close_y && _my <= _close_y + 26);
    if (_close_hov && _click) {
        show_settings_modal = false;
        scr_audio_play_ui("cancel");
    }
    draw_set_color(_close_hov ? make_color_rgb(180, 40, 40) : make_color_rgb(70, 20, 20));
    draw_rectangle(_close_x, _close_y, _close_x + 32, _close_y + 26, false);
    draw_set_color(_close_hov ? make_color_rgb(255, 100, 100) : make_color_rgb(200, 50, 50));
    draw_rectangle(_close_x, _close_y, _close_x + 32, _close_y + 26, true);
    draw_set_color(c_white);
    draw_text(_close_x + 10, _close_y + 6, "X");

    // Subtabs: [1. AUDIO CHANNELS & MUTE]  [2. DISPLAY & SHORTCUTS]
    var _tab_y = _my0 + 44;
    var _t1_w = 260;
    var _t1_hov = (_mx >= _mx0 + 24 && _mx <= _mx0 + 24 + _t1_w && _my >= _tab_y && _my <= _tab_y + 28);
    if (_t1_hov && _click) { settings_active_tab = 0; scr_audio_play_ui("tab"); }
    scr_draw_snes_button(_mx0 + 24, _tab_y, _t1_w, 28, "1. AUDIO & MUTE CONTROL", _t1_hov || (settings_active_tab == 0), (settings_active_tab == 0), (settings_active_tab == 0) ? make_color_rgb(0, 240, 255) : c_white);

    var _t2_x = _mx0 + 24 + _t1_w + 12;
    var _t2_w = 260;
    var _t2_hov = (_mx >= _t2_x && _mx <= _t2_x + _t2_w && _my >= _tab_y && _my <= _tab_y + 28);
    if (_t2_hov && _click) { settings_active_tab = 1; scr_audio_play_ui("tab"); }
    scr_draw_snes_button(_t2_x, _tab_y, _t2_w, 28, "2. DISPLAY & SHORTCUTS", _t2_hov || (settings_active_tab == 1), (settings_active_tab == 1), (settings_active_tab == 1) ? make_color_rgb(0, 240, 255) : c_white);

    if (settings_active_tab == 0) {
        var _is_muted = scr_audio_is_muted();
        var _m_vol = scr_audio_get_master_volume();
        var _b_vol = scr_audio_get_bgm_volume();
        var _s_vol = scr_audio_get_sfx_volume();
        var _b_muted = scr_audio_is_bgm_muted();
        var _s_muted = scr_audio_is_sfx_muted();

        // Hero Audio Mute Button
        var _hero_x = _mx0 + 24;
        var _hero_y = _tab_y + 38;
        var _hero_w = _mw - 48;
        var _hero_h = 58;
        var _hero_hov = (_mx >= _hero_x && _mx <= _hero_x + _hero_w && _my >= _hero_y && _my <= _hero_y + _hero_h);

        if (_hero_hov && _click) {
            scr_audio_toggle_mute();
            scr_audio_play_ui("confirm");
        }

        draw_set_color(_hero_hov ? (_is_muted ? make_color_rgb(90, 28, 28) : make_color_rgb(20, 70, 95)) : (_is_muted ? make_color_rgb(52, 16, 16) : make_color_rgb(14, 38, 54)));
        draw_rectangle(_hero_x, _hero_y, _hero_x + _hero_w, _hero_y + _hero_h, false);
        draw_set_color(_hero_hov ? (_is_muted ? make_color_rgb(255, 120, 120) : make_color_rgb(80, 255, 180)) : (_is_muted ? make_color_rgb(220, 60, 60) : make_color_rgb(0, 220, 255)));
        draw_rectangle(_hero_x, _hero_y, _hero_x + _hero_w, _hero_y + _hero_h, true);

        draw_set_color(_is_muted ? make_color_rgb(255, 50, 50) : make_color_rgb(0, 255, 150));
        draw_rectangle(_hero_x + 4, _hero_y + 4, _hero_x + 12, _hero_y + _hero_h - 4, false);

        draw_set_color(_is_muted ? make_color_rgb(255, 140, 140) : make_color_rgb(0, 240, 255));
        draw_text(_hero_x + 24, _hero_y + 10, _is_muted ? "[!] MASTER AUDIO IS CURRENTLY MUTED (DEFAULT)" : "[✓] MASTER AUDIO IS ACTIVE & OPERATIONAL");
        draw_set_color(c_white);
        draw_text(_hero_x + 24, _hero_y + 30, _is_muted ? ">> CLICK TO UNMUTE ALL AUDIO (Or press [M] on keyboard) <<" : ">> CLICK TO MUTE ALL AUDIO (Silent Running Mode) <<");

        // Master Volume Presets
        var _ch_y = _hero_y + _hero_h + 16;
        var _ch_w = _hero_w;
        var _ch_h = 74;

        draw_set_color(make_color_rgb(12, 18, 28));
        draw_rectangle(_hero_x, _ch_y, _hero_x + _ch_w, _ch_y + _ch_h, false);
        draw_set_color(make_color_rgb(32, 54, 82));
        draw_rectangle(_hero_x, _ch_y, _hero_x + _ch_w, _ch_y + _ch_h, true);

        draw_set_color(make_color_rgb(100, 210, 255));
        draw_text(_hero_x + 14, _ch_y + 10, "MASTER VOLUME: " + string(floor(_m_vol * 100)) + "%" + (_is_muted ? " [MUTED]" : ""));

        var _steps = [0.0, 0.25, 0.50, 0.75, 1.0];
        var _sb_w = 64;
        var _sb_x0 = _hero_x + 390;
        for (var vi = 0; vi < 5; vi++) {
            var _sv = _steps[vi];
            var _sb_x = _sb_x0 + vi * (_sb_w + 6);
            var _sb_hov = (_mx >= _sb_x && _mx <= _sb_x + _sb_w && _my >= _ch_y + 8 && _my <= _ch_y + 34);
            var _is_act = (abs(_m_vol - _sv) < 0.05 && !_is_muted);
            if (_sb_hov && _click) {
                scr_audio_set_master_volume(_sv);
                if (_sv > 0 && _is_muted) scr_audio_set_muted(false);
                scr_audio_play_ui("click");
            }
            scr_draw_snes_button(_sb_x, _ch_y + 8, _sb_w, 26, string(floor(_sv * 100)) + "%", _sb_hov || _is_act, _is_act, _is_act ? make_color_rgb(100, 255, 180) : c_white);
        }

        // BGM Channel
        var _ch2_y = _ch_y + _ch_h + 10;
        draw_set_color(make_color_rgb(12, 18, 28));
        draw_rectangle(_hero_x, _ch2_y, _hero_x + _ch_w, _ch2_y + _ch_h, false);
        draw_set_color(make_color_rgb(32, 54, 82));
        draw_rectangle(_hero_x, _ch2_y, _hero_x + _ch_w, _ch2_y + _ch_h, true);

        draw_set_color(make_color_rgb(100, 210, 255));
        draw_text(_hero_x + 14, _ch2_y + 10, "BGM SCORE: " + string(floor(_b_vol * 100)) + "%");
        var _bm_w = 110;
        var _bm_x = _hero_x + 14;
        var _bm_y = _ch2_y + 38;
        var _bm_hov = (_mx >= _bm_x && _mx <= _bm_x + _bm_w && _my >= _bm_y && _my <= _bm_y + 26);
        if (_bm_hov && _click) {
            scr_audio_set_bgm_muted(!_b_muted);
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_bm_x, _bm_y, _bm_w, 26, _b_muted ? "[BGM MUTED]" : "[MUTE BGM]", _bm_hov, _b_muted, _b_muted ? make_color_rgb(255, 100, 100) : c_white);

        // SFX Channel
        var _ch3_y = _ch2_y + _ch_h + 10;
        draw_set_color(make_color_rgb(12, 18, 28));
        draw_rectangle(_hero_x, _ch3_y, _hero_x + _ch_w, _ch3_y + _ch_h, false);
        draw_set_color(make_color_rgb(32, 54, 82));
        draw_rectangle(_hero_x, _ch3_y, _hero_x + _ch_w, _ch3_y + _ch_h, true);

        draw_set_color(make_color_rgb(100, 210, 255));
        draw_text(_hero_x + 14, _ch3_y + 10, "SFX FOLEY: " + string(floor(_s_vol * 100)) + "%");
        var _sm_w = 110;
        var _sm_x = _hero_x + 14;
        var _sm_y = _ch3_y + 38;
        var _sm_hov = (_mx >= _sm_x && _mx <= _sm_x + _sm_w && _my >= _sm_y && _my <= _sm_y + 26);
        if (_sm_hov && _click) {
            scr_audio_set_sfx_muted(!_s_muted);
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_sm_x, _sm_y, _sm_w, 26, _s_muted ? "[SFX MUTED]" : "[MUTE SFX]", _sm_hov, _s_muted, _s_muted ? make_color_rgb(255, 100, 100) : c_white);
    } else if (settings_active_tab == 1) {
        var _dsp_x = _mx0 + 24;
        var _dsp_y = _tab_y + 40;
        var _dsp_w = _mw - 48;

        draw_set_color(make_color_rgb(12, 18, 28));
        draw_rectangle(_dsp_x, _dsp_y, _dsp_x + _dsp_w, _dsp_y + 110, false);
        draw_set_color(make_color_rgb(32, 54, 82));
        draw_rectangle(_dsp_x, _dsp_y, _dsp_x + _dsp_w, _dsp_y + 110, true);

        draw_set_color(make_color_rgb(100, 210, 255));
        draw_text(_dsp_x + 14, _dsp_y + 12, "TACTICAL DISPLAY CONFIGURATION:");

        var _crt_w = 260;
        var _crt_hov = (_mx >= _dsp_x + 14 && _mx <= _dsp_x + 14 + _crt_w && _my >= _dsp_y + 38 && _my <= _dsp_y + 68);
        if (_crt_hov && _click) {
            settings_crt_scanlines = !settings_crt_scanlines;
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_dsp_x + 14, _dsp_y + 38, _crt_w, 30, settings_crt_scanlines ? "[✓] CRT SCANLINES: ON" : "[X] CRT SCANLINES: OFF", _crt_hov, settings_crt_scanlines, settings_crt_scanlines ? make_color_rgb(0, 240, 140) : make_color_rgb(220, 100, 100));
    }

    var _btn_close_w = 260;
    var _btn_close_h = 38;
    var _btn_close_x = _mx0 + floor((_mw - _btn_close_w) / 2);
    var _btn_close_y = _my0 + _mh - 52;
    var _bc_hov = (_mx >= _btn_close_x && _mx <= _btn_close_x + _btn_close_w && _my >= _btn_close_y && _my <= _btn_close_y + _btn_close_h);
    if (_bc_hov && _click) {
        show_settings_modal = false;
        scr_audio_play_ui("confirm");
    }
    scr_draw_snes_button(_btn_close_x, _btn_close_y, _btn_close_w, _btn_close_h, ">> CLOSE SETTINGS <<", _bc_hov, false, make_color_rgb(60, 240, 140));
}
'''

path_draw = "objects/obj_HQTerminal/Draw_64.gml"
with open(path_draw, "w", encoding="utf-8") as f:
    f.write(clean_draw_64)

print("✓ obj_HQTerminal/Draw_64.gml completely rewritten as Clean Galactic Map interface!")
