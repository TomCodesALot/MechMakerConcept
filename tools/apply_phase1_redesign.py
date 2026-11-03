#!/usr/bin/env python3
import os
import re

print("[PHASE 1] Applying Strategic War Room Centerpiece & Front Mission Command Dock...")

# 1. Update obj_HQTerminal/Create_0.gml: default to War Map (active_tab = 3)
path_create = "objects/obj_HQTerminal/Create_0.gml"
with open(path_create, "r", encoding="utf-8") as f:
    create_code = f.read()

create_code = re.sub(r"active_tab\s*=\s*\d+;", "active_tab = 3; // Default to Strategic War Room Centerpiece (Gihren's Greed Style)", create_code, count=1)

with open(path_create, "w", encoding="utf-8") as f:
    f.write(create_code)
print("✓ obj_HQTerminal/Create_0.gml set to default active_tab = 3 (War Map).")

# 2. Update obj_HQTerminal/Step_0.gml: Update hotkeys 1-5, [S], [SPACE]
path_step = "objects/obj_HQTerminal/Step_0.gml"
with open(path_step, "r", encoding="utf-8") as f:
    step_code = f.read()

old_keys = '''// Direct Number Keys 1-5 for Command Deck Tab Navigation
if (!intro_active && !show_commander_modal && active_tutorial_modal == "" && !show_turn_briefing_modal && !showing_retire_modal && !show_settings_modal) {
    if (keyboard_check_pressed(ord("1"))) { active_tab = 0; scr_audio_play_ui("tab"); }
    if (keyboard_check_pressed(ord("2"))) { active_tab = 1; scr_audio_play_ui("tab"); }
    if (keyboard_check_pressed(ord("3"))) { active_tab = 2; scr_audio_play_ui("tab"); }
    if (keyboard_check_pressed(ord("4"))) { active_tab = 3; scr_audio_play_ui("tab"); }
    if (keyboard_check_pressed(ord("5"))) { active_tab = 4; scr_audio_play_ui("tab"); }
}'''

new_keys = '''// Direct Number Keys 1-5 for Command Deck Tab Navigation (Front Mission Style Dock)
if (!intro_active && !show_commander_modal && active_tutorial_modal == "" && !show_turn_briefing_modal && !showing_retire_modal && !show_settings_modal) {
    if (keyboard_check_pressed(ord("1"))) { active_tab = 3; scr_audio_play_ui("tab"); } // 1: War Room (Centerpiece)
    if (keyboard_check_pressed(ord("2"))) { active_tab = 1; scr_audio_play_ui("tab"); } // 2: Mech Hangar
    if (keyboard_check_pressed(ord("3"))) { active_tab = 0; scr_audio_play_ui("tab"); } // 3: R&D Forge
    if (keyboard_check_pressed(ord("4"))) { active_tab = 2; scr_audio_play_ui("tab"); } // 4: Contracts
    if (keyboard_check_pressed(ord("5"))) { active_tab = 4; scr_audio_play_ui("tab"); } // 5: Fleet & Rivals
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

if old_keys in step_code:
    step_code = step_code.replace(old_keys, new_keys, 1)
    with open(path_step, "w", encoding="utf-8") as f:
        f.write(step_code)
    print("✓ obj_HQTerminal/Step_0.gml updated with War Room navigation hotkeys.")
else:
    print("WARNING: old_keys not found in Step_0.gml")

# 3. Update obj_HQTerminal/Draw_64.gml: Replace horizontal tabs with Front Mission Command Dock
path_draw = "objects/obj_HQTerminal/Draw_64.gml"
with open(path_draw, "r", encoding="utf-8") as f:
    draw_code = f.read()

target_section = '''// =========================================================================
// 3. PRIMARY NAVIGATION TABS (y: 68 to 106)
// =========================================================================
var _tabs = [
    "1. R&D LAB // PROTOTYPING",
    "2. FACTORY & PERSONNEL",
    "3. CONTRACTS & COMMERCE",
    "4. STRATEGIC WAR MAP",
    "5. DREADNOUGHT & RIVALS"
];

var _tab_w = (_gw - 48) / 5;
var _tab_y = 68;
var _tab_h = 36;

for (var tb = 0; tb < 5; tb++) {
    var _tbx = 24 + tb * _tab_w;
    var _tb_active = (active_tab == tb);
    var _tb_hov = (_mx >= _tbx && _mx <= _tbx + _tab_w - 6 && _my >= _tab_y && _my <= _tab_y + _tab_h);

    if (_tb_hov && _click) {
        if (active_tab != tb) {
            active_tab = tb;
            scr_audio_play_ui("tab");
            if (active_tab == 0) {
                scr_audio_play_location_bgm("prototyping");
            } else {
                scr_audio_play_location_bgm("hq");
            }
        }
    }

    draw_set_color(_tb_active ? make_color_rgb(24, 48, 76) : (_tb_hov ? make_color_rgb(18, 32, 50) : make_color_rgb(12, 18, 26)));
    draw_rectangle(_tbx + _sx, _tab_y + _sy, _tbx + _tab_w - 6 + _sx, _tab_y + _tab_h + _sy, false);
    draw_set_color(_tb_active ? make_color_rgb(80, 180, 255) : make_color_rgb(40, 70, 105));
    draw_rectangle(_tbx + _sx, _tab_y + _sy, _tbx + _tab_w - 6 + _sx, _tab_y + _tab_h + _sy, true);

    if (_tb_active) {
        draw_set_color(make_color_rgb(100, 220, 255));
        draw_rectangle(_tbx + _sx, _tab_y + _tab_h - 3 + _sy, _tbx + _tab_w - 6 + _sx, _tab_y + _tab_h + _sy, false);
    }

    draw_set_color(_tb_active ? c_white : make_color_rgb(170, 195, 220));
    draw_text(_tbx + 16 + _sx, _tab_y + 9 + _sy, _tabs[tb]);
}

// Alert Ticker Banner (y: 108 to 126)
draw_set_color(make_color_rgb(8, 12, 18));
draw_rectangle(24 + _sx, 108 + _sy, _gw - 24 + _sx, 126 + _sy, false);
draw_set_color(make_color_rgb(180, 210, 120));
draw_text(32 + _sx, 110 + _sy, ">> INTEL FEED: " + alerts_feed[alert_index]);

// =========================================================================
// 4. MAIN WORKSPACE PANELS (y: 132 to _gh - 30)
// =========================================================================
var _pan_x = 24;
var _pan_y = 132;
var _pan_w = _gw - 48;
var _pan_h = _gh - _pan_y - 48;

draw_set_color(make_color_rgb(12, 18, 26));
draw_rectangle(_pan_x + _sx, _pan_y + _sy, _pan_x + _pan_w + _sx, _pan_y + _pan_h + _sy, false);
draw_set_color(make_color_rgb(30, 50, 75));
draw_rectangle(_pan_x + _sx, _pan_y + _sy, _pan_x + _pan_w + _sx, _pan_y + _pan_h + _sy, true);'''

replacement_section = '''// =========================================================================
// 3. FRONT MISSION STYLE LEFT TACTICAL COMMAND DOCK (x: 16 to 212, y: 66 to 720)
// =========================================================================
var _dock_x = 16;
var _dock_y = 66;
var _dock_w = 196;
var _dock_h = _gh - _dock_y - 44; // ~658px tall

// Outer Dock Frame & Backdrop
scr_draw_snes_panel(_dock_x, _dock_y, _dock_w, _dock_h, "COMMAND DECK", 0, false, 0.06);

// Dock Header Ribbon
draw_set_color(make_color_rgb(14, 22, 34));
draw_rectangle(_dock_x + 8, _dock_y + 12, _dock_x + _dock_w - 8, _dock_y + 36, false);
draw_set_color(make_color_rgb(45, 75, 110));
draw_rectangle(_dock_x + 8, _dock_y + 12, _dock_x + _dock_w - 8, _dock_y + 36, true);
draw_set_color(make_color_rgb(0, 220, 255));
draw_text(_dock_x + 14, _dock_y + 16, "PMC DIRECTIVES");

// Command Menu Items (Front Mission / Gihren's Greed Style)
var _menu_tabs = [
    { id: 3, key: "[1]", title: "1. WAR ROOM", desc: "Planetary War Map" },
    { id: 1, key: "[2]", title: "2. MECH HANGAR", desc: "Assembly & Upgrades" },
    { id: 0, key: "[3]", title: "3. R&D FORGE", desc: "Alloys & Metallurgy" },
    { id: 2, key: "[4]", title: "4. CONTRACTS", desc: "Bounties & Flyoffs" },
    { id: 4, key: "[5]", title: "5. FLEET & RIVALS", desc: "Flagship & Corps" }
];

var _btn_y0 = _dock_y + 44;
var _btn_h = 52;
var _btn_gap = 8;
var _bw = _dock_w - 16;
var _bx = _dock_x + 8;

for (var mi = 0; mi < array_length(_menu_tabs); mi++) {
    var _m_item = _menu_tabs[mi];
    var _by = _btn_y0 + mi * (_btn_h + _btn_gap);
    var _is_act = (active_tab == _m_item.id);
    var _m_hov = (_mx >= _bx && _mx <= _bx + _bw && _my >= _by && _my <= _by + _btn_h);

    if (_m_hov && _click) {
        if (active_tab != _m_item.id) {
            active_tab = _m_item.id;
            scr_audio_play_ui("click");
            if (active_tab == 0) {
                scr_audio_play_location_bgm("prototyping");
            } else {
                scr_audio_play_location_bgm("hq");
            }
        }
    }

    // Button Base Fill
    draw_set_color(_is_act ? make_color_rgb(20, 54, 88) : (_m_hov ? make_color_rgb(18, 36, 56) : make_color_rgb(12, 18, 28)));
    draw_rectangle(_bx + _sx, _by + _sy, _bx + _bw + _sx, _by + _btn_h + _sy, false);

    // Border
    draw_set_color(_is_act ? make_color_rgb(0, 240, 255) : (_m_hov ? make_color_rgb(100, 200, 255) : make_color_rgb(40, 65, 95)));
    draw_rectangle(_bx + _sx, _by + _sy, _bx + _bw + _sx, _by + _btn_h + _sy, true);

    // Left Active Indicator Strip
    if (_is_act) {
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_rectangle(_bx + _sx, _by + _sy, _bx + 5 + _sx, _by + _btn_h + _sy, false);
    }

    // Text Labels
    draw_set_color(_is_act ? c_white : (_m_hov ? make_color_rgb(220, 240, 255) : make_color_rgb(160, 190, 220)));
    draw_text(_bx + 12 + _sx, _by + 8 + _sy, _m_item.title);

    draw_set_color(_is_act ? make_color_rgb(120, 220, 255) : make_color_rgb(110, 140, 170));
    draw_text(_bx + 12 + _sx, _by + 26 + _sy, _m_item.desc);

    // Keybadge on Right
    draw_set_color(_is_act ? make_color_rgb(255, 220, 80) : make_color_rgb(80, 120, 160));
    draw_text(_bx + _bw - 28 + _sx, _by + 8 + _sy, _m_item.key);
}

// Tactical Divider Line
var _div_y = _btn_y0 + 5 * (_btn_h + _btn_gap) + 8;
draw_set_color(make_color_rgb(32, 54, 82));
draw_line(_bx, _div_y, _bx + _bw, _div_y);

// --- COMBAT SORTIE BUTTON ---
var _sort_y = _div_y + 12;
var _sort_h = 50;
var _sort_hov = (_mx >= _bx && _mx <= _bx + _bw && _my >= _sort_y && _my <= _sort_y + _sort_h);
if (_sort_hov && _click && room_exists(rm_combat)) {
    scr_audio_play_ui("confirm");
    room_goto(rm_combat);
}
draw_set_color(_sort_hov ? make_color_rgb(80, 50, 10) : make_color_rgb(36, 22, 6));
draw_rectangle(_bx + _sx, _sort_y + _sy, _bx + _bw + _sx, _sort_y + _sort_h + _sy, false);
draw_set_color(_sort_hov ? make_color_rgb(255, 210, 60) : make_color_rgb(220, 160, 40));
draw_rectangle(_bx + _sx, _sort_y + _sy, _bx + _bw + _sx, _sort_y + _sort_h + _sy, true);
draw_set_color(make_color_rgb(255, 200, 40));
draw_rectangle(_bx + _sx, _sort_y + _sy, _bx + 5 + _sx, _sort_y + _sort_h + _sy, false);
draw_set_color(make_color_rgb(255, 230, 100));
draw_text(_bx + 12 + _sx, _sort_y + 8 + _sy, ">> SORTIE COMBAT <<");
draw_set_color(make_color_rgb(200, 170, 100));
draw_text(_bx + 12 + _sx, _sort_y + 26 + _sy, "Deploy Platoon [S]");

// --- ADVANCE STRATEGIC CYCLE BUTTON ---
var _adv_y = _sort_y + _sort_h + 10;
var _adv_h = 50;
var _adv_hov = (_mx >= _bx && _mx <= _bx + _bw && _my >= _adv_y && _my <= _adv_y + _adv_h);
if (_adv_hov && _click && instance_exists(obj_GameManager)) {
    obj_GameManager.end_turn();
}
draw_set_color(_adv_hov ? make_color_rgb(18, 64, 36) : make_color_rgb(10, 32, 18));
draw_rectangle(_bx + _sx, _adv_y + _sy, _bx + _bw + _sx, _adv_y + _adv_h + _sy, false);
draw_set_color(_adv_hov ? make_color_rgb(60, 240, 140) : make_color_rgb(40, 180, 95));
draw_rectangle(_bx + _sx, _adv_y + _sy, _bx + _bw + _sx, _adv_y + _adv_h + _sy, true);
draw_set_color(make_color_rgb(0, 240, 120));
draw_rectangle(_bx + _sx, _adv_y + _sy, _bx + 5 + _sx, _adv_y + _adv_h + _sy, false);
draw_set_color(make_color_rgb(120, 255, 170));
draw_text(_bx + 12 + _sx, _adv_y + 8 + _sy, ">> ADVANCE DAY <<");
draw_set_color(make_color_rgb(100, 200, 140));
draw_text(_bx + 12 + _sx, _adv_y + 26 + _sy, "Next Strategic Cycle [SPACE]");

// Dock Footer Status
var _foot_y = _dock_y + _dock_h - 40;
draw_set_color(make_color_rgb(14, 20, 30));
draw_rectangle(_bx, _foot_y, _bx + _bw, _foot_y + 32, false);
draw_set_color(make_color_rgb(30, 50, 75));
draw_rectangle(_bx, _foot_y, _bx + _bw, _foot_y + 32, true);
draw_set_color(make_color_rgb(80, 220, 140));
draw_text(_bx + 8, _foot_y + 8, "PMC STATUS: READY");

// =========================================================================
// 4. MAIN WORKSPACE PANELS (Gihren's Greed Center Stage)
// =========================================================================
var _pan_x = 220;
var _pan_y = 66;
var _pan_w = _gw - _pan_x - 16; // 1130 px
var _pan_h = _gh - _pan_y - 44; // 658 px

draw_set_color(make_color_rgb(12, 18, 26));
draw_rectangle(_pan_x + _sx, _pan_y + _sy, _pan_x + _pan_w + _sx, _pan_y + _pan_h + _sy, false);
draw_set_color(make_color_rgb(30, 50, 75));
draw_rectangle(_pan_x + _sx, _pan_y + _sy, _pan_x + _pan_w + _sx, _pan_y + _pan_h + _sy, true);'''

if target_section in draw_code:
    draw_code = draw_code.replace(target_section, replacement_section, 1)
    print("✓ Replaced horizontal tabs with Left Command Dock and expanded center stage.")
else:
    print("WARNING: target_section not found in Draw_64.gml!")

# Add the bottom Intel Wire Ticker right before modal section
modal_marker = "// 8. SYSTEM CONFIGURATION & TACTICAL AUDIO MODAL"
bottom_ticker_code = '''// =========================================================================
// BOTTOM GALACTIC INTEL WIRE (TICKER)
// =========================================================================
var _tick_x = 16;
var _tick_y = _gh - 38;
var _tick_w = _gw - 32;
var _tick_h = 30;

draw_set_color(make_color_rgb(8, 12, 18));
draw_rectangle(_tick_x + _sx, _tick_y + _sy, _tick_x + _tick_w + _sx, _tick_y + _tick_h + _sy, false);
draw_set_color(make_color_rgb(30, 54, 82));
draw_rectangle(_tick_x + _sx, _tick_y + _sy, _tick_x + _tick_w + _sx, _tick_y + _tick_h + _sy, true);

// Glowing Signal Light
draw_set_color(make_color_rgb(0, 240, 255));
draw_rectangle(_tick_x + 4 + _sx, _tick_y + 6 + _sy, _tick_x + 12 + _sx, _tick_y + _tick_h - 6 + _sy, false);

draw_set_color(make_color_rgb(255, 210, 90));
draw_text(_tick_x + 18 + _sx, _tick_y + 7 + _sy, "GALACTIC INTEL WIRE //");

draw_set_color(make_color_rgb(200, 230, 255));
draw_text(_tick_x + 190 + _sx, _tick_y + 7 + _sy, alerts_feed[alert_index]);

'''

if "BOTTOM GALACTIC INTEL WIRE" not in draw_code:
    if modal_marker in draw_code:
        draw_code = draw_code.replace(modal_marker, bottom_ticker_code + "\n" + modal_marker, 1)
        print("✓ Bottom Galactic Intel Wire added before modals.")
    else:
        draw_code += "\n" + bottom_ticker_code
        print("✓ Bottom Galactic Intel Wire appended.")

with open(path_draw, "w", encoding="utf-8") as f:
    f.write(draw_code)
print("✓ obj_HQTerminal/Draw_64.gml successfully patched with Phase 1 layout.")
