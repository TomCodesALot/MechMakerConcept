import re

with open('objects/obj_HQTerminal/Draw_64_legacy_backup.gml', 'r') as f:
    legacy_lines = f.readlines()

# Extract legacy sections
dock_code = "".join(legacy_lines[239:418])
tab0_code = "".join(legacy_lines[418:2266])   # R&D
tab1_code = "".join(legacy_lines[2266:3181])  # Factory
tab2_code = "".join(legacy_lines[3181:4187])  # Contracts
tab4_code = "".join(legacy_lines[6365:7071])  # Fleet
modals_code = "".join(legacy_lines[7071:])    # Modals & Overlays

with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
    current_map_text = f.read()

# 1. TOP HEADER & HQ DECK SWITCHER
header_code = '''/// @description obj_HQTerminal Draw GUI Event - UNIFIED COMMAND DECK & SHIN GIHREN'S GREED WAR MAP
// High-clarity, retro-tactical Galactic Theater Map & Multi-Deck PMC Management Sim

var _gw = display_get_gui_width();
var _gh = display_get_gui_height();
var _mx = device_mouse_x_to_gui(0);
var _my = device_mouse_y_to_gui(0);
var _click = mouse_check_button_pressed(mb_left);
var _down = mouse_check_button(mb_left);

var _sx = random_range(-crucible_shake, crucible_shake);
var _sy = random_range(-crucible_shake, crucible_shake);

// =========================================================================
// 1. BACKDROP & COORDINATE GRID
// =========================================================================
draw_set_color(make_color_rgb(8, 12, 18));
draw_rectangle(0, 0, _gw, _gh, false);

if (active_tab != 3) {
    var _loc_bg = (active_tab == 0 || active_tab == 1) ? spr_loc_hangar_bay : spr_loc_war_room;
    if (sprite_exists(_loc_bg)) {
        draw_sprite_ext(_loc_bg, 0, 0, 0, _gw / 1024.0, _gh / 576.0, 0, c_white, 0.24);
    }
}

// Tactical Coordinate Grid
draw_set_color(make_color_rgb(16, 24, 36));
for (var gx = 0; gx < _gw; gx += 48) draw_line(gx, 0, gx, _gh);
for (var gy = 0; gy < _gh; gy += 48) draw_line(0, gy, _gw, gy);

// =========================================================================
// 2. PERSISTENT TOP COMMAND BAR & HQ DECK SWITCHER (y: 6 to 54)
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

// PMC Title
draw_set_color(make_color_rgb(0, 240, 255));
draw_text(26 + _sx, _top_y + 8 + _sy, "IRON RIDGE PMC");
draw_set_color(make_color_rgb(140, 175, 215));
draw_text(26 + _sx, _top_y + 26 + _sy, "COMMAND DECK // T-2");

// Economic & Cycle Ticker
var _gm = instance_exists(obj_GameManager) ? obj_GameManager : undefined;
var _funds_val = !is_undefined(_gm) ? _gm.funds : 100000;
var _turn_val = !is_undefined(_gm) ? _gm.current_turn : 1;
var _year_val = !is_undefined(_gm) ? _gm.current_cycle_year : 214;
var _day_val = !is_undefined(_gm) ? _gm.current_cycle_day : 1;

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
draw_set_color(make_color_rgb(14, 28, 20));
draw_rectangle(180 + _sx, _top_y + 6 + _sy, 316 + _sx, _top_y + _top_h - 6 + _sy, false);
draw_set_color(make_color_rgb(30, 90, 50));
draw_rectangle(180 + _sx, _top_y + 6 + _sy, 316 + _sx, _top_y + _top_h - 6 + _sy, true);
draw_set_color(make_color_rgb(80, 240, 140));
draw_text(188 + _sx, _top_y + 14 + _sy, _funds_formatted);

// Calendar Readout
draw_set_color(make_color_rgb(20, 26, 38));
draw_rectangle(322 + _sx, _top_y + 6 + _sy, 452 + _sx, _top_y + _top_h - 6 + _sy, false);
draw_set_color(make_color_rgb(45, 70, 105));
draw_rectangle(322 + _sx, _top_y + 6 + _sy, 452 + _sx, _top_y + _top_h - 6 + _sy, true);
draw_set_color(make_color_rgb(255, 215, 80));
draw_text(330 + _sx, _top_y + 14 + _sy, "Y" + string(_year_val) + " · D" + string(_day_val) + " [T-" + string(_turn_val) + "]");

// --- HQ DECK NAVIGATION SWITCHER TABS (Front Mission / Gihren's Greed Multi-Deck) ---
var _decks = [
    { id: 3, name: "🗺️ WAR MAP" },
    { id: 0, name: "🔬 R&D BAY" },
    { id: 1, name: "🏭 FACTORY" },
    { id: 2, name: "📜 CONTRACTS" },
    { id: 4, name: "🚀 FLEET" }
];
var _d_x0 = 460;
var _d_w = 98;
var _d_h = 36;
var _d_y = _top_y + 6;

for (var di = 0; di < array_length(_decks); di++) {
    var _deck = _decks[di];
    var _bx = _d_x0 + di * (_d_w + 4);
    var _is_cur = (active_tab == _deck.id);
    var _dhov = (_mx >= _bx && _mx <= _bx + _d_w && _my >= _d_y && _my <= _d_y + _d_h);
    
    if (_dhov && _click) {
        if (active_tab != _deck.id) {
            active_tab = _deck.id;
            scr_audio_play_ui("tab");
            if (active_tab == 0) scr_audio_play_location_bgm("prototyping");
            else scr_audio_play_location_bgm("hq");
        }
    }
    
    draw_set_color(_is_cur ? make_color_rgb(24, 60, 96) : (_dhov ? make_color_rgb(18, 38, 62) : make_color_rgb(10, 16, 26)));
    draw_rectangle(_bx + _sx, _d_y + _sy, _bx + _d_w + _sx, _d_y + _d_h + _sy, false);
    draw_set_color(_is_cur ? make_color_rgb(0, 240, 255) : (_dhov ? make_color_rgb(100, 200, 255) : make_color_rgb(35, 65, 95)));
    draw_rectangle(_bx + _sx, _d_y + _sy, _bx + _d_w + _sx, _d_y + _d_h + _sy, true);
    
    if (_is_cur) {
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_rectangle(_bx + _sx, _d_y + _sy, _bx + _d_w + _sx, _d_y + 3 + _sy, false);
    }
    
    draw_set_color(_is_cur ? c_white : (_dhov ? make_color_rgb(200, 230, 255) : make_color_rgb(150, 180, 210)));
    draw_text(_bx + 8 + _sx, _d_y + 10 + _sy, _deck.name);
}

// --- TOP RIGHT ACTION BUTTONS ---
// 1. Advance Day Button
var _adv_x = 976;
var _adv_w = 144;
var _adv_hov = (_mx >= _adv_x && _mx <= _adv_x + _adv_w && _my >= _d_y && _my <= _d_y + _d_h);
if (_adv_hov && _click && !is_undefined(_gm)) {
    _gm.end_turn();
}
draw_set_color(_adv_hov ? make_color_rgb(20, 70, 40) : make_color_rgb(12, 38, 22));
draw_rectangle(_adv_x + _sx, _d_y + _sy, _adv_x + _adv_w + _sx, _d_y + _d_h + _sy, false);
draw_set_color(_adv_hov ? make_color_rgb(80, 255, 150) : make_color_rgb(45, 190, 100));
draw_rectangle(_adv_x + _sx, _d_y + _sy, _adv_x + _adv_w + _sx, _d_y + _d_h + _sy, true);
draw_set_color(c_white);
draw_text(_adv_x + 8 + _sx, _d_y + 10 + _sy, ">> ADVANCE [SPACE]");

// 2. Sortie Combat Button
var _sort_x = 1126;
var _sort_w = 90;
var _sort_hov = (_mx >= _sort_x && _mx <= _sort_x + _sort_w && _my >= _d_y && _my <= _d_y + _d_h);
if (_sort_hov && _click && room_exists(rm_combat)) {
    scr_audio_play_ui("confirm");
    room_goto(rm_combat);
}
draw_set_color(_sort_hov ? make_color_rgb(80, 50, 10) : make_color_rgb(38, 24, 8));
draw_rectangle(_sort_x + _sx, _d_y + _sy, _sort_x + _sort_w + _sx, _d_y + _d_h + _sy, false);
draw_set_color(_sort_hov ? make_color_rgb(255, 210, 60) : make_color_rgb(210, 150, 40));
draw_rectangle(_sort_x + _sx, _d_y + _sy, _sort_x + _sort_w + _sx, _d_y + _d_h + _sy, true);
draw_set_color(make_color_rgb(255, 225, 100));
draw_text(_sort_x + 8 + _sx, _d_y + 10 + _sy, "⚔️ SORTIE");

// 3. Audio Mute Toggle Button
var _mute_x = 1222;
var _mute_w = 54;
var _is_aud_muted = scr_audio_is_muted();
var _mute_hov = (_mx >= _mute_x && _mx <= _mute_x + _mute_w && _my >= _d_y && _my <= _d_y + _d_h);
if (_mute_hov && _click) {
    var _nm = scr_audio_toggle_mute();
    show_toast(_nm ? "[AUDIO MUTED]" : "[AUDIO UNMUTED]", _nm ? c_orange : c_lime);
}
draw_set_color(_mute_hov ? (_is_aud_muted ? make_color_rgb(70, 22, 22) : make_color_rgb(20, 60, 40)) : (_is_aud_muted ? make_color_rgb(40, 14, 14) : make_color_rgb(12, 32, 22)));
draw_rectangle(_mute_x + _sx, _d_y + _sy, _mute_x + _mute_w + _sx, _d_y + _d_h + _sy, false);
draw_set_color(_mute_hov ? (_is_aud_muted ? make_color_rgb(255, 100, 100) : make_color_rgb(100, 255, 160)) : (_is_aud_muted ? make_color_rgb(220, 60, 60) : make_color_rgb(50, 190, 100)));
draw_rectangle(_mute_x + _sx, _d_y + _sy, _mute_x + _mute_w + _sx, _d_y + _d_h + _sy, true);
draw_set_color(_is_aud_muted ? make_color_rgb(255, 130, 130) : make_color_rgb(130, 255, 170));
draw_text(_mute_x + 6 + _sx, _d_y + 10 + _sy, _is_aud_muted ? "[🔇]" : "[🔊]");

// 4. Settings Config Button
var _cfg_x = 1282;
var _cfg_w = 68;
var _cfg_hov = (_mx >= _cfg_x && _mx <= _cfg_x + _cfg_w && _my >= _d_y && _my <= _d_y + _d_h);
if (_cfg_hov && _click) {
    show_settings_modal = !show_settings_modal;
    scr_audio_play_ui("click");
}
draw_set_color(_cfg_hov ? make_color_rgb(20, 48, 70) : make_color_rgb(12, 22, 34));
draw_rectangle(_cfg_x + _sx, _d_y + _sy, _cfg_x + _cfg_w + _sx, _d_y + _d_h + _sy, false);
draw_set_color(_cfg_hov ? make_color_rgb(100, 220, 255) : make_color_rgb(55, 130, 190));
draw_rectangle(_cfg_x + _sx, _d_y + _sy, _cfg_x + _cfg_w + _sx, _d_y + _d_h + _sy, true);
draw_set_color(make_color_rgb(120, 220, 255));
draw_text(_cfg_x + 8 + _sx, _d_y + 10 + _sy, "[⚙ CFG]");
'''

# 2. Extract current warmap code and enhance it with the new Order Dispatch & Transit logic
cel_idx = current_map_text.find('// 3. CELESTIAL THEATER NAVIGATION TABS')
set_idx = current_map_text.find('// 7. SETTINGS MODAL DIALOG')

warmap_raw = current_map_text[cel_idx:set_idx]

# In warmap_raw:
# A. Add Order Dispatch Banner right after celestial tabs
order_banner_insertion = '''
// --- ORDER DISPATCH STATUS RIBBON ---
if (order_dispatch_mode) {
    var _ob_y = _th_y + _th_h + 4;
    draw_set_color(make_color_rgb(160, 120, 10));
    draw_rectangle(_rad_x, _ob_y, _rad_x + _rad_w, _ob_y + 24, false);
    draw_set_color(make_color_rgb(255, 220, 60));
    draw_rectangle(_rad_x, _ob_y, _rad_x + _rad_w, _ob_y + 24, true);
    draw_set_color(c_white);
    draw_text(_rad_x + 12, _ob_y + 4, "⚡ TACTICAL DISPATCH MODE ACTIVE: SELECT AN ADJACENT CONNECTED NODE ALONG HYPERLANE TO ISSUE SQUADRON DIRECTIVE   [ESC TO CANCEL]");
}
'''

# Insert order_banner_insertion right before `var _rad_x = 16;`
rad_idx = warmap_raw.find('var _rad_x = 16;')
warmap_enhanced = warmap_raw[:rad_idx] + order_banner_insertion + "\n" + warmap_raw[rad_idx:]

# B. Enhance Pass 1 (Hyperlanes) with pulsing highlighted order vectors
# Find where Pass 1 finishes (right before `// Pass 2: Interactive Territory Nodes`)
pass2_idx = warmap_enhanced.find('// Pass 2: Interactive Territory Nodes')
order_vectors_code = '''
    // Pass 1.5: Tactical Order Dispatch Hyperlane Vectors (Shin Gihren's Greed Route Markers)
    if (order_dispatch_mode && order_origin_id != "") {
        var _orig_t_ord = scr_territory_get(order_origin_id);
        if (!is_undefined(_orig_t_ord)) {
            var _ox = _rad_x + 40 + floor(_orig_t_ord.map_x * 1.34);
            var _oy = _rad_y + 48 + floor(_orig_t_ord.map_y * 1.48);
            
            for (var oi = 0; oi < array_length(_orig_t_ord.connected_ids); oi++) {
                var _dest_t = scr_territory_get(_orig_t_ord.connected_ids[oi]);
                if (!is_undefined(_dest_t) && _dest_t.region == _region_str) {
                    var _dx = _rad_x + 40 + floor(_dest_t.map_x * 1.34);
                    var _dy = _rad_y + 48 + floor(_dest_t.map_y * 1.48);
                    
                    var _is_friendly = (_dest_t.controlling_faction == "pmc");
                    var _v_col = _is_friendly ? make_color_rgb(0, 240, 255) : make_color_rgb(255, 90, 80);
                    
                    // Pulsing Glow Line
                    draw_set_color(_v_col);
                    draw_set_alpha(0.75 + 0.25 * sin(current_time * 0.008));
                    draw_line_width(_ox, _oy, _dx, _dy, 3);
                    draw_set_alpha(1.0);
                    
                    // Moving Directional Chevrons
                    var _flow = (current_time * 0.001) % 1.0;
                    var _cx = lerp(_ox, _dx, _flow);
                    var _cy = lerp(_oy, _dy, _flow);
                    draw_circle(_cx, _cy, 4, false);
                }
            }
        }
    }
'''
warmap_enhanced = warmap_enhanced[:pass2_idx] + order_vectors_code + "\n" + warmap_enhanced[pass2_idx:]

# C. In Pass 2: Handle node selection in Order Dispatch Mode
# Find:
#         if (_hov && _click) {
#             selected_territory_id = _t.id;
#             scr_audio_play_ui("click");
#         }
old_click_logic = '''        if (_hov && _click) {
            selected_territory_id = _t.id;
            scr_audio_play_ui("click");
        }'''

new_click_logic = '''        if (_hov && _click) {
            if (order_dispatch_mode && order_origin_id != "") {
                var _orig_check = scr_territory_get(order_origin_id);
                var _is_connected = false;
                if (!is_undefined(_orig_check)) {
                    for (var ci = 0; ci < array_length(_orig_check.connected_ids); ci++) {
                        if (_orig_check.connected_ids[ci] == _t.id) { _is_connected = true; break; }
                    }
                }
                if (_is_connected) {
                    order_target_id = _t.id;
                    order_operation_type = (_t.controlling_faction == "pmc") ? "REDEPLOY" : "ASSAULT";
                    order_modal_active = true;
                    scr_audio_play_ui("click");
                } else if (_t.id == order_origin_id) {
                    order_dispatch_mode = false;
                    scr_audio_play_ui("cancel");
                } else {
                    selected_territory_id = _t.id;
                    order_dispatch_mode = false;
                    scr_audio_play_ui("click");
                }
            } else {
                selected_territory_id = _t.id;
                scr_audio_play_ui("click");
            }
        }'''

warmap_enhanced = warmap_enhanced.replace(old_click_logic, new_click_logic, 1)

# D. Add Order Origin & Target visual reticles in Pass 2
old_counter_draw = 'scr_draw_tactical_counter(_nx, _ny - 4, _t.controlling_faction, _g_spec.unit_sprite_name, _g_spec.stack_count, _is_sel, _hov, 1.05);'

new_counter_draw = '''// Order Dispatch Reticle Overlay
        if (order_dispatch_mode) {
            if (_t.id == order_origin_id) {
                draw_set_color(make_color_rgb(255, 215, 60));
                draw_circle(_nx, _ny - 4, 30, true);
                draw_set_color(make_color_rgb(255, 230, 100));
                draw_text(_nx - 36, _ny - 42, "[ORDER ORIGIN]");
            } else {
                var _orig_t_chk = scr_territory_get(order_origin_id);
                var _conn = false;
                if (!is_undefined(_orig_t_chk)) {
                    for (var cj = 0; cj < array_length(_orig_t_chk.connected_ids); cj++) {
                        if (_orig_t_chk.connected_ids[cj] == _t.id) { _conn = true; break; }
                    }
                }
                if (_conn) {
                    var _is_fr = (_t.controlling_faction == "pmc");
                    draw_set_color(_is_fr ? make_color_rgb(0, 240, 255) : make_color_rgb(255, 90, 80));
                    draw_circle(_nx, _ny - 4, 28 + 3 * sin(current_time * 0.01), true);
                    if (_hov) {
                        draw_set_color(make_color_rgb(12, 18, 28));
                        draw_rectangle(_nx - 60, _ny - 42, _nx + 60, _ny - 22, false);
                        draw_set_color(_is_fr ? make_color_rgb(80, 255, 140) : make_color_rgb(255, 100, 100));
                        draw_rectangle(_nx - 60, _ny - 42, _nx + 60, _ny - 22, true);
                        draw_text(_nx - 56, _ny - 39, _is_fr ? ">> REDEPLOY >>" : ">> ASSAULT >>");
                    }
                }
            }
        }
        scr_draw_tactical_counter(_nx, _ny - 4, _t.controlling_faction, _g_spec.unit_sprite_name, _g_spec.stack_count, _is_sel, _hov, 1.05);'''

warmap_enhanced = warmap_enhanced.replace(old_counter_draw, new_counter_draw, 1)

# E. Pass 2.5: Active Moving Transit Counters
# Find where the territory nodes loop ends (look for `// --- TOP-RIGHT AMBER SATELLITE RADAR`)
radar_mm_idx = warmap_enhanced.find('// --- TOP-RIGHT AMBER SATELLITE RADAR')
active_transits_draw_code = '''
    // =========================================================================
    // Pass 2.5: Active Hyperlane Transit Strike Wings (Shin Gihren's Greed Live March)
    // =========================================================================
    for (var tri = 0; tri < array_length(active_transits); tri++) {
        var _tr = active_transits[tri];
        var _curr_x = lerp(_tr.origin_x, _tr.target_x, _tr.progress);
        var _curr_y = lerp(_tr.origin_y, _tr.target_y, _tr.progress);
        
        // Glowing route vector
        draw_set_color(_tr.is_combat ? make_color_rgb(255, 80, 80) : make_color_rgb(0, 240, 255));
        draw_set_alpha(0.65);
        draw_line_width(_tr.origin_x, _tr.origin_y, _tr.target_x, _tr.target_y, 2);
        draw_set_alpha(1.0);
        
        // Moving Tactical Counter
        scr_draw_tactical_counter(_curr_x, _curr_y, "pmc", _tr.unit_sprite_name, _tr.stack_count, true, false, 0.95);
        
        // Status Tag
        draw_set_color(make_color_rgb(10, 16, 26));
        draw_rectangle(_curr_x - 48, _curr_y - 34, _curr_x + 48, _curr_y - 18, false);
        draw_set_color(_tr.is_combat ? make_color_rgb(255, 100, 100) : make_color_rgb(80, 220, 255));
        draw_rectangle(_curr_x - 48, _curr_y - 34, _curr_x + 48, _curr_y - 18, true);
        draw_set_color(c_white);
        draw_text(_curr_x - 42, _curr_y - 32, _tr.is_combat ? "ASSAULT WING" : "TRANSIT SQUAD");
    }
'''
warmap_enhanced = warmap_enhanced[:radar_mm_idx] + active_transits_draw_code + "\n" + warmap_enhanced[radar_mm_idx:]

# F. In Right Dossier Panel: Add "ISSUE TACTICAL ORDER / DISPATCH" button and smart adjacent invasion routing
old_actions_code = '''    // --- SECTOR DIRECT ACTIONS ---
    var _act_y = _dos_y + _dos_h - 90;
    var _act_w = _dos_w - 32;

    if (_cur_t.controlling_faction == "pmc") {
        var _fort_hov = (_mx >= _dos_x + 16 && _mx <= _dos_x + 16 + _act_w && _my >= _act_y && _my <= _act_y + 34);
        if (_fort_hov && _click) {
            scr_territory_fortify(_cur_t.id);
        }
        scr_draw_snes_button(_dos_x + 16, _act_y, _act_w, 34, ">> FORTIFY SECTOR (+10 DEF: $25K) >>", _fort_hov, false, make_color_rgb(80, 240, 140));
    } else {
        var _raid_hov = (_mx >= _dos_x + 16 && _mx <= _dos_x + 16 + _act_w && _my >= _act_y && _my <= _act_y + 34);
        if (_raid_hov && _click) {
            scr_territory_launch_pmc_assault(_cur_t.id, 0, 0);
        }
        scr_draw_snes_button(_dos_x + 16, _act_y, _act_w, 34, ">> DISPATCH PMC ASSAULT EXPEDITION >>", _raid_hov, false, make_color_rgb(255, 180, 60));
    }'''

new_actions_code = '''    // --- SECTOR DIRECT ACTIONS ---
    var _act_y = _dos_y + _dos_h - 100;
    var _act_w = _dos_w - 32;

    if (_cur_t.controlling_faction == "pmc") {
        // Dispatch Squadron Order Button
        var _disp_y = _act_y - 38;
        var _disp_hov = (_mx >= _dos_x + 16 && _mx <= _dos_x + 16 + _act_w && _my >= _disp_y && _my <= _disp_y + 32);
        if (_disp_hov && _click) {
            order_dispatch_mode = !order_dispatch_mode;
            order_origin_id = _cur_t.id;
            scr_audio_play_ui(order_dispatch_mode ? "confirm" : "cancel");
        }
        scr_draw_snes_button(_dos_x + 16, _disp_y, _act_w, 32, order_dispatch_mode ? "✖ CANCEL DISPATCH MODE" : "⚡ ISSUE TACTICAL ORDER / DISPATCH", _disp_hov, order_dispatch_mode, make_color_rgb(0, 240, 255));

        // Fortify Sector Button
        var _fort_hov = (_mx >= _dos_x + 16 && _mx <= _dos_x + 16 + _act_w && _my >= _act_y && _my <= _act_y + 32);
        if (_fort_hov && _click) {
            scr_territory_fortify(_cur_t.id);
        }
        scr_draw_snes_button(_dos_x + 16, _act_y, _act_w, 32, ">> FORTIFY SECTOR (+10 DEF: $25K) >>", _fort_hov, false, make_color_rgb(80, 240, 140));
    } else {
        // Hostile Sector Invasion Assault Button with Smart Adjacent Base Routing
        var _raid_hov = (_mx >= _dos_x + 16 && _mx <= _dos_x + 16 + _act_w && _my >= _act_y && _my <= _act_y + 34);
        if (_raid_hov && _click) {
            var _adj_pmc = scr_territory_get_adjacent_pmc_base(_cur_t.id);
            if (_adj_pmc != "") {
                order_origin_id = _adj_pmc;
                order_target_id = _cur_t.id;
                order_operation_type = "ASSAULT";
                order_modal_active = true;
                scr_audio_play_ui("confirm");
            } else {
                show_toast("CANNOT INVADE: NO CONNECTED PMC STAGING BASE! ADVANCE STEP-BY-STEP.", make_color_rgb(255, 140, 40));
                scr_audio_play_ui("cancel");
            }
        }
        scr_draw_snes_button(_dos_x + 16, _act_y, _act_w, 34, "⚔️ LAUNCH INVASION ASSAULT ($15K)", _raid_hov, false, make_color_rgb(255, 180, 60));
    }'''

warmap_enhanced = warmap_enhanced.replace(old_actions_code, new_actions_code, 1)

# G. Append Order Confirmation Modal and Combat Result Modal at the end of warmap_enhanced
modals_warmap_code = '''
// =========================================================================
// TACTICAL ORDER CONFIRMATION MODAL (Shin Gihren's Greed Operation Directive)
// =========================================================================
if (order_modal_active) {
    var _omw = 640;
    var _omh = 420;
    var _omx = floor((_gw - _omw) / 2);
    var _omy = floor((_gh - _omh) / 2);
    
    draw_set_color(c_black);
    draw_set_alpha(0.75);
    draw_rectangle(0, 0, _gw, _gh, false);
    draw_set_alpha(1.0);
    
    scr_draw_snes_panel(_omx, _omy, _omw, _omh, "TACTICAL DISPATCH DIRECTIVE // VANGUARD ORDERS", make_color_rgb(0, 240, 255), true);
    
    var _o_t = scr_territory_get(order_origin_id);
    var _d_t = scr_territory_get(order_target_id);
    
    if (!is_undefined(_o_t) && !is_undefined(_d_t)) {
        // Vector Routing Display
        draw_set_color(make_color_rgb(14, 22, 34));
        draw_rectangle(_omx + 20, _omy + 36, _omx + _omw - 20, _omy + 90, false);
        draw_set_color(make_color_rgb(45, 80, 120));
        draw_rectangle(_omx + 20, _omy + 36, _omx + _omw - 20, _omy + 90, true);
        
        draw_set_color(make_color_rgb(255, 215, 60));
        draw_text(_omx + 30, _omy + 44, "STAGING BASE: " + string_upper(_o_t.name));
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_omx + 30, _omy + 64, "===[ HYPERLANE TRANSIT VECTOR ]===> DESTINATION: " + string_upper(_d_t.name));
        
        // Squadron Tac-Card Preview
        var _g_spec = scr_territory_get_garrison_spec(_o_t);
        var _scard_y = _omy + 104;
        draw_set_color(make_color_rgb(12, 18, 28));
        draw_rectangle(_omx + 20, _scard_y, _omx + _omw - 20, _scard_y + 70, false);
        draw_set_color(make_color_rgb(35, 65, 100));
        draw_rectangle(_omx + 20, _scard_y, _omx + _omw - 20, _scard_y + 70, true);
        
        scr_draw_tactical_counter(_omx + 56, _scard_y + 44, "pmc", _g_spec.unit_sprite_name, _g_spec.stack_count, true, false, 1.2);
        draw_set_color(c_white);
        draw_text(_omx + 92, _scard_y + 14, "ASSIGNED SQUADRON: " + string_upper(_g_spec.unit_label) + " [" + string(_g_spec.stack_count) + " UNITS]");
        draw_set_color(make_color_rgb(80, 220, 140));
        draw_text(_omx + 92, _scard_y + 36, "OPERATION CLASSIFICATION: " + (order_operation_type == "ASSAULT" ? "INTERDICTION ASSAULT & SECTOR SEIZURE" : "LOGISTICAL FORCE REDEPLOYMENT"));
        
        // Combat Forecast & Logistics
        var _fc_y = _scard_y + 82;
        draw_set_color(make_color_rgb(14, 20, 30));
        draw_rectangle(_omx + 20, _fc_y, _omx + _omw - 20, _fc_y + 110, false);
        draw_set_color(make_color_rgb(45, 75, 110));
        draw_rectangle(_omx + 20, _fc_y, _omx + _omw - 20, _fc_y + 110, true);
        
        if (order_operation_type == "ASSAULT") {
            var _est_atk = (_g_spec.stack_count * 16) + 32;
            var _est_def = _d_t.defense_rating + 20;
            var _odds = clamp(floor((_est_atk / max(1, _est_atk + _est_def)) * 100), 15, 95);
            
            draw_set_color(make_color_rgb(255, 200, 80));
            draw_text(_omx + 32, _fc_y + 12, "COMBAT SIMULATION FORECAST (SHIN GIHREN'S GREED ALGORITHM):");
            draw_set_color(make_color_rgb(140, 220, 255));
            draw_text(_omx + 32, _fc_y + 34, "• Projectile & Kinetic Attack Power: ~" + string(_est_atk) + " pts");
            draw_set_color(make_color_rgb(255, 120, 120));
            draw_text(_omx + 32, _fc_y + 54, "• Target Fortification Envelope: " + string(_d_t.defense_rating) + " / 100 DEF");
            draw_set_color(make_color_rgb(80, 255, 150));
            draw_text(_omx + 32, _fc_y + 76, "• Projected Breakthrough Probability: " + string(_odds) + "%  |  Fuel & Munitions Cost: $15,000 Cr");
        } else {
            draw_set_color(make_color_rgb(80, 240, 140));
            draw_text(_omx + 32, _fc_y + 16, "REDEPLOYMENT TELEMETRY:");
            draw_set_color(make_color_rgb(180, 220, 255));
            draw_text(_omx + 32, _fc_y + 40, "• Zero casualty risk along secured sovereign hyperlane.");
            draw_text(_omx + 32, _fc_y + 64, "• Destination Fortification will be reinforced (+5 DEF).  |  Transit Cost: $5,000 Cr");
        }
        
        // Buttons
        var _btn_w = 280;
        var _btn_h = 40;
        var _by = _fc_y + 122;
        
        var _exec_hov = (_mx >= _omx + 20 && _mx <= _omx + 20 + _btn_w && _my >= _by && _my <= _by + _btn_h);
        if (_exec_hov && _click) {
            var _is_comb = (order_operation_type == "ASSAULT");
            if (scr_territory_issue_order(order_origin_id, order_target_id, _g_spec.unit_sprite_name, _g_spec.stack_count, _is_comb)) {
                order_modal_active = false;
                order_dispatch_mode = false;
            }
        }
        scr_draw_snes_button(_omx + 20, _by, _btn_w, _btn_h, "⚡ EXECUTE DISPATCH [ENTER]", _exec_hov, false, make_color_rgb(0, 240, 255));
        
        var _can_hov = (_mx >= _omx + _omw - 20 - _btn_w && _mx <= _omx + _omw - 20 && _my >= _by && _my <= _by + _btn_h);
        if ((_can_hov && _click) || keyboard_check_pressed(vk_escape)) {
            order_modal_active = false;
            order_dispatch_mode = false;
            scr_audio_play_ui("cancel");
        }
        scr_draw_snes_button(_omx + _omw - 20 - _btn_w, _by, _btn_w, _btn_h, "✖ ABORT DIRECTIVE [ESC]", _can_hov, false, make_color_rgb(255, 90, 80));
    }
}

// =========================================================================
// COMBAT ACTION REPORT MODAL (Round-by-Round Battle Resolution Ledger)
// =========================================================================
if (combat_modal_active) {
    var _cmw = 640;
    var _cmh = 390;
    var _cmx = floor((_gw - _cmw) / 2);
    var _cmy = floor((_gh - _cmh) / 2);
    
    draw_set_color(c_black);
    draw_set_alpha(0.80);
    draw_rectangle(0, 0, _gw, _gh, false);
    draw_set_alpha(1.0);
    
    var _c_col = combat_report.is_victory ? make_color_rgb(255, 215, 60) : make_color_rgb(255, 80, 80);
    scr_draw_snes_panel(_cmx, _cmy, _cmw, _cmh, combat_report.title, _c_col, true);
    
    // Status Banner
    draw_set_color(make_color_rgb(14, 20, 30));
    draw_rectangle(_cmx + 20, _cmy + 36, _cmx + _cmw - 20, _cmy + 84, false);
    draw_set_color(_c_col);
    draw_rectangle(_cmx + 20, _cmy + 36, _cmx + _cmw - 20, _cmy + 84, true);
    draw_rectangle(_cmx + 20, _cmy + 36, _cmx + 25, _cmy + 84, false);
    
    draw_set_color(_c_col);
    draw_text(_cmx + 36, _cmy + 44, combat_report.is_victory ? "★ TACTICAL VICTORY: SECTOR SECURED & SOVEREIGNTY CLAIMED ★" : "⚠️ OPERATION REPELLED: TACTICAL WITHDRAWAL INITIATED");
    draw_set_color(make_color_rgb(180, 210, 240));
    draw_text(_cmx + 36, _cmy + 62, combat_report.origin_name + " ===> " + combat_report.target_name);
    
    // Round Ledger Lines
    var _led_y = _cmy + 96;
    draw_set_color(make_color_rgb(10, 16, 24));
    draw_rectangle(_cmx + 20, _led_y, _cmx + _cmw - 20, _led_y + 190, false);
    draw_set_color(make_color_rgb(40, 65, 95));
    draw_rectangle(_cmx + 20, _led_y, _cmx + _cmw - 20, _led_y + 190, true);
    
    draw_set_color(make_color_rgb(0, 220, 255));
    draw_text(_cmx + 32, _led_y + 12, "BATTLE ACTION LOG // COMBAT RESOLUTION LEDGER:");
    
    for (var ri = 0; ri < array_length(combat_report.rounds); ri++) {
        draw_set_color(make_color_rgb(200, 225, 250));
        draw_text(_cmx + 32, _led_y + 36 + ri * 26, "• " + combat_report.rounds[ri]);
    }
    
    draw_set_color(combat_report.is_victory ? make_color_rgb(80, 240, 140) : make_color_rgb(255, 140, 80));
    draw_text(_cmx + 32, _led_y + 145, combat_report.result_text);
    
    // Dismiss Button
    var _dbtn_w = 260;
    var _dbtn_h = 38;
    var _dby = _cmy + _cmh - 52;
    var _dbx = _cmx + floor((_cmw - _dbtn_w) / 2);
    var _d_hov = (_mx >= _dbx && _mx <= _dbx + _dbtn_w && _my >= _dby && _my <= _dby + _dbtn_h);
    if ((_d_hov && _click) || keyboard_check_pressed(vk_escape) || keyboard_check_pressed(vk_enter) || keyboard_check_pressed(vk_space)) {
        combat_modal_active = false;
        scr_audio_play_ui("confirm");
    }
    scr_draw_snes_button(_dbx, _dby, _dbtn_w, _dbtn_h, ">> ACKNOWLEDGE REPORT [ESC/ENTER] >>", _d_hov, false, _c_col);
}
'''
warmap_enhanced += "\n" + modals_warmap_code

# Assemble Full Draw_64
full_draw64 = header_code + "\n\nif (active_tab == 3) {\n" + warmap_enhanced + "\n}\nelse {\n" + dock_code + "\n" + tab0_code + "\n" + tab1_code + "\n" + tab2_code + "\n" + tab4_code + "\n}\n\n" + modals_code

with open('objects/obj_HQTerminal/Draw_64.gml', 'w') as f:
    f.write(full_draw64)

print(f"Successfully assembled unified Draw_64.gml! Total lines: {len(full_draw64.splitlines())}")
