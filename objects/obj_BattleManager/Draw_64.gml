/// @description obj_BattleManager Draw GUI Event
// Renders Turn-Based Tactical Grid, AP Economy, Front Mission Component Readout & Duel Resolution
// Strictly implements docs/05_tactical_combat.md

var _gw = display_get_gui_width();
var _gh = display_get_gui_height();
var _mx = device_mouse_x_to_gui(0);
var _my = device_mouse_y_to_gui(0);
var _click = mouse_check_button_pressed(mb_left);

// Screen Shake Offset
var _sx = random_range(-screen_shake, screen_shake);
var _sy = random_range(-screen_shake, screen_shake);

// 1. Dark Sci-Fi Combat Environment
draw_set_color(make_color_rgb(10, 14, 20));
draw_set_alpha(1.0);
draw_rectangle(0, 0, _gw, _gh, false);

// Tactical Grid Lines in Background
draw_set_color(make_color_rgb(16, 24, 34));
for (var gx = 0; gx < _gw; gx += 48) draw_line(gx, 0, gx, _gh);
for (var gy = 0; gy < _gh; gy += 48) draw_line(0, gy, _gw, gy);

// =========================================================================
// 2. TOP MISSION & AP / HEAT HUD BAR (y: 0 to 90)
// =========================================================================
draw_set_color(make_color_rgb(14, 20, 28));
draw_rectangle(_sx, _sy, _gw + _sx, 90 + _sy, false);
draw_set_color(make_color_rgb(35, 60, 90));
draw_rectangle(_sx, 88 + _sy, _gw + _sx, 90 + _sy, false);

// Title & Sector
draw_set_color(make_color_rgb(100, 200, 255));
draw_text(24 + _sx, 12 + _sy, "TACTICAL COMBAT // SECTOR 4 MINING OUTPOST");
draw_set_color(make_color_rgb(140, 170, 200));
draw_text(24 + _sx, 32 + _sy, "OBJECTIVE: Neutralize Syndicate GHA-07 Reaver Incursion");

// Current Phase Badge
var _phase_str = "[PLAYER PHASE]";
var _phase_col = make_color_rgb(80, 240, 120);
if (state == COMBAT_STATE.AI_PHASE) {
    _phase_str = "[HOSTILE PHASE // ENEMY ENGAGING]";
    _phase_col = make_color_rgb(255, 80, 80);
} else if (state == COMBAT_STATE.MOVE_MODE) {
    _phase_str = "[MANEUVER MODE // SELECT DESTINATION]";
    _phase_col = make_color_rgb(100, 220, 255);
} else if (state == COMBAT_STATE.TARGET_MODE) {
    _phase_str = "[TARGETING WEAPON // SELECT ENEMY]";
    _phase_col = make_color_rgb(255, 200, 80);
}
draw_set_color(_phase_col);
draw_text(24 + _sx, 56 + _sy, "STATUS: " + _phase_str + " | TURN: " + string(turn_number));

// Player Action Points (AP) Battery Pips
var _ap_x = 520;
var _ap_y = 16;
draw_set_color(c_white);
draw_text(_ap_x + _sx, _ap_y + _sy, "ACTION POINTS (AP): " + string(player_unit.current_ap) + " / " + string(player_unit.max_ap));
for (var p = 0; p < player_unit.max_ap; p++) {
    var _px = _ap_x + p * 32;
    var _py = _ap_y + 24;
    var _has_ap = (p < player_unit.current_ap);
    draw_set_color(_has_ap ? make_color_rgb(50, 220, 100) : make_color_rgb(30, 45, 35));
    draw_rectangle(_px + _sx, _py + _sy, _px + 26 + _sx, _py + 32 + _sy, false);
    draw_set_color(make_color_rgb(80, 255, 140));
    draw_rectangle(_px + _sx, _py + _sy, _px + 26 + _sx, _py + 32 + _sy, true);
}

// Player Heat Gauge
var _heat_x = 760;
var _heat_y = 16;
var _h_norm = clamp(player_unit.current_heat / player_unit.max_heat, 0, 1);
var _h_col = (_h_norm > 0.8) ? c_red : ((_h_norm > 0.5) ? c_orange : make_color_rgb(100, 200, 255));
draw_set_color(c_white);
draw_text(_heat_x + _sx, _heat_y + _sy, "CHASSIS HEAT: " + string(floor(player_unit.current_heat)) + " % / 100 %");
draw_set_color(make_color_rgb(18, 28, 38));
draw_rectangle(_heat_x + _sx, _heat_y + 24 + _sy, _heat_x + 190 + _sx, _heat_y + 44 + _sy, false);
draw_set_color(_h_col);
draw_rectangle(_heat_x + _sx, _heat_y + 24 + _sy, _heat_x + (190 * _h_norm) + _sx, _heat_y + 44 + _sy, false);
draw_set_color(make_color_rgb(40, 70, 100));
draw_rectangle(_heat_x + _sx, _heat_y + 24 + _sy, _heat_x + 190 + _sx, _heat_y + 44 + _sy, true);

// Abort / Return to HQ Button
var _ab_x = 1140;
var _ab_y = 18;
var _ab_w = 200;
var _ab_h = 36;
var _ab_hov = (_mx >= _ab_x && _mx <= _ab_x + _ab_w && _my >= _ab_y && _my <= _ab_y + _ab_h);
if (_ab_hov && _click) {
    if (room_exists(rm_hq_terminal)) room_goto(rm_hq_terminal);
}
draw_set_color(_ab_hov ? make_color_rgb(60, 30, 20) : make_color_rgb(30, 15, 10));
draw_rectangle(_ab_x + _sx, _ab_y + _sy, _ab_x + _ab_w + _sx, _ab_y + _ab_h + _sy, false);
draw_set_color(make_color_rgb(220, 100, 60));
draw_rectangle(_ab_x + _sx, _ab_y + _sy, _ab_x + _ab_w + _sx, _ab_y + _ab_h + _sy, true);
draw_set_color(c_white);
draw_text(_ab_x + 16 + _sx, _ab_y + 10 + _sy, "[ESC: RETREAT TO HQ]");

// =========================================================================
// 3. TACTICAL COMBAT GRID (x: 64 to 896, y: 110 to 558)
// =========================================================================
var _grid_w = grid_cols * cell_size;
var _grid_h = grid_rows * cell_size;

// Grid Outer Border
draw_set_color(make_color_rgb(12, 18, 26));
draw_rectangle(grid_ox + _sx, grid_oy + _sy, grid_ox + _grid_w + _sx, grid_oy + _grid_h + _sy, false);
draw_set_color(make_color_rgb(35, 60, 95));
draw_rectangle(grid_ox + _sx, grid_oy + _sy, grid_ox + _grid_w + _sx, grid_oy + _grid_h + _sy, true);

// Draw Grid Cells & Overlays
for (var c = 0; c < grid_cols; c++) {
    for (var r = 0; r < grid_rows; r++) {
        var _cx = grid_ox + c * cell_size;
        var _cy = grid_oy + r * cell_size;

        // Base Cell Outline
        draw_set_color(make_color_rgb(22, 34, 48));
        draw_rectangle(_cx + _sx, _cy + _sy, _cx + cell_size + _sx, _cy + cell_size + _sy, true);

        // Tactical Cover Terrain (+20% Defense)
        if (grid_terrain[c][r] == 1) {
            draw_set_color(make_color_rgb(35, 45, 55));
            draw_rectangle(_cx + 4 + _sx, _cy + 4 + _sy, _cx + cell_size - 4 + _sx, _cy + cell_size - 4 + _sy, false);
            draw_set_color(make_color_rgb(120, 150, 180));
            draw_text(_cx + 8 + _sx, _cy + 22 + _sy, "COVER");
        }

        // Highlight Valid Movement Range (Cyan)
        if (state == COMBAT_STATE.MOVE_MODE) {
            for (var m = 0; m < array_length(valid_move_tiles); m++) {
                var _vt = valid_move_tiles[m];
                if (_vt.col == c && _vt.row == r) {
                    draw_set_alpha(0.25);
                    draw_set_color(make_color_rgb(50, 180, 255));
                    draw_rectangle(_cx + 2 + _sx, _cy + 2 + _sy, _cx + cell_size - 2 + _sx, _cy + cell_size - 2 + _sy, false);
                    draw_set_alpha(1.0);
                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_rectangle(_cx + 2 + _sx, _cy + 2 + _sy, _cx + cell_size - 2 + _sx, _cy + cell_size - 2 + _sy, true);
                    draw_text(_cx + 14 + _sx, _cy + 22 + _sy, string(_vt.cost) + " AP");
                }
            }
        }

        // Highlight Weapon Attack Range (Orange)
        if (state == COMBAT_STATE.TARGET_MODE) {
            var _w = weapons[selected_weapon];
            var _dist = calculate_distance(player_unit.grid_c, player_unit.grid_r, c, r);
            if (_dist >= _w.range_min && _dist <= _w.range_max) {
                draw_set_alpha(0.18);
                draw_set_color(make_color_rgb(255, 140, 40));
                draw_rectangle(_cx + 2 + _sx, _cy + 2 + _sy, _cx + cell_size - 2 + _sx, _cy + cell_size - 2 + _sy, false);
                draw_set_alpha(1.0);
            }
        }

        // Mouse Hover Reticle
        if (hover_c == c && hover_r == r) {
            draw_set_color(c_white);
            draw_rectangle(_cx + _sx, _cy + _sy, _cx + cell_size + _sx, _cy + cell_size + _sy, true);
        }
    }
}

// -------------------------------------------------------------------------
// Draw Units on Grid (with Directional Facing & Recoil Spring Physics)
// -------------------------------------------------------------------------

// 1. Draw Player Mech
var _pvx = player_unit.visual_x + player_unit.recoil_x + _sx;
var _pvy = player_unit.visual_y + player_unit.recoil_y + _sy;

if (sprite_exists(player_unit.sprite_index)) {
    draw_sprite_ext(player_unit.sprite_index, player_unit.image_index, _pvx, _pvy, player_unit.facing, 1.0, 0, player_unit.image_blend, 1.0);
}

// Player Unit Tag & HP Bar
draw_set_color(c_lime);
draw_text(_pvx - 45, _pvy - 58, "WARHAMMER");
var _php_norm = clamp(player_unit.components.torso.cur / player_unit.components.torso.max, 0, 1);
draw_set_color(make_color_rgb(10, 20, 10));
draw_rectangle(_pvx - 45, _pvy - 42, _pvx + 45, _pvy - 34, false);
draw_set_color(c_lime);
draw_rectangle(_pvx - 45, _pvy - 42, _pvx - 45 + (90 * _php_norm), _pvy - 34, false);

// 2. Draw Enemy Mech (Syndicate Reaver)
var _evx = enemy_unit.visual_x + enemy_unit.recoil_x + _sx;
var _evy = enemy_unit.visual_y + enemy_unit.recoil_y + _sy;

if (sprite_exists(enemy_unit.sprite_index)) {
    draw_sprite_ext(enemy_unit.sprite_index, enemy_unit.image_index, _evx, _evy, enemy_unit.facing, 1.0, 0, enemy_unit.image_blend, 1.0);
}

// Enemy Unit Tag & HP Bar
draw_set_color(enemy_unit.is_destroyed ? c_gray : make_color_rgb(255, 90, 90));
draw_text(_evx - 35, _evy - 58, enemy_unit.is_destroyed ? "[DESTROYED]" : "REAVER");
if (!enemy_unit.is_destroyed) {
    var _ehp_norm = clamp(enemy_unit.components.torso.cur / enemy_unit.components.torso.max, 0, 1);
    draw_set_color(make_color_rgb(25, 10, 10));
    draw_rectangle(_evx - 45, _evy - 42, _evx + 45, _evy - 34, false);
    draw_set_color(make_color_rgb(255, 70, 70));
    draw_rectangle(_evx - 45, _evy - 42, _evx - 45 + (90 * _ehp_norm), _evy - 34, false);
}

// =========================================================================
// 4. FRONT MISSION TARGET DUEL DIAGNOSTICS (Right Panel: x 915 to 1330)
// =========================================================================
var _diag_x = grid_ox + _grid_w + 20;
var _diag_y = grid_oy;
var _diag_w = _gw - _diag_x - 24;
var _diag_h = _grid_h;

draw_set_color(make_color_rgb(10, 16, 24));
draw_rectangle(_diag_x + _sx, _diag_y + _sy, _diag_x + _diag_w + _sx, _diag_y + _diag_h + _sy, false);
draw_set_color(make_color_rgb(40, 70, 105));
draw_rectangle(_diag_x + _sx, _diag_y + _sy, _diag_x + _diag_w + _sx, _diag_y + _diag_h + _sy, true);

draw_set_color(make_color_rgb(100, 220, 255));
draw_text(_diag_x + 16 + _sx, _diag_y + 12 + _sy, "== TARGET DIAGNOSTICS: OUTLAW REAVER ==");

// Component Breakdown Function
var _draw_comp_bar = function(_lbl, _cur, _max, _intact, _bx, _by) {
    var _col = _intact ? ((_cur / _max > 0.4) ? c_lime : c_yellow) : c_red;
    draw_set_color(_intact ? c_white : c_gray);
    draw_text(_bx, _by, _lbl);
    draw_set_color(_col);
    draw_text(_bx + 160, _by, _intact ? (string(_cur) + " / " + string(_max) + " HP") : "[SEVERED]");
    // Progress Bar
    draw_set_color(make_color_rgb(20, 28, 38));
    draw_rectangle(_bx + 260, _by + 2, _bx + 370, _by + 14, false);
    if (_intact) {
        draw_set_color(_col);
        draw_rectangle(_bx + 260, _by + 2, _bx + 260 + (110 * clamp(_cur / _max, 0, 1)), _by + 14, false);
    }
};

var _cy_start = _diag_y + 40;
var _e_comps = enemy_unit.components;
_draw_comp_bar("TORSO CORE", _e_comps.torso.cur, _e_comps.torso.max, _e_comps.torso.intact, _diag_x + 16 + _sx, _cy_start + _sy);
_draw_comp_bar("HEAD SENSORS", _e_comps.head.cur, _e_comps.head.max, _e_comps.head.intact, _diag_x + 16 + _sx, _cy_start + 28 + _sy);
_draw_comp_bar("LEFT ARM (CANNON)", _e_comps.arm_left.cur, _e_comps.arm_left.max, _e_comps.arm_left.intact, _diag_x + 16 + _sx, _cy_start + 56 + _sy);
_draw_comp_bar("RIGHT ARM (VULCAN)", _e_comps.arm_right.cur, _e_comps.arm_right.max, _e_comps.arm_right.intact, _diag_x + 16 + _sx, _cy_start + 84 + _sy);
_draw_comp_bar("HYDRAULIC LEGS", _e_comps.legs.cur, _e_comps.legs.max, _e_comps.legs.intact, _diag_x + 16 + _sx, _cy_start + 112 + _sy);
_draw_comp_bar("ARES ORDNANCE", _e_comps.backpack.cur, _e_comps.backpack.max, _e_comps.backpack.intact, _diag_x + 16 + _sx, _cy_start + 140 + _sy);

// Selected Weapon & Hit Probability Breakdown
var _calc_y = _cy_start + 175;
var _sel_w = weapons[selected_weapon];
var _dist_to_e = calculate_distance(player_unit.grid_c, player_unit.grid_r, enemy_unit.grid_c, enemy_unit.grid_r);
var _hit_pct = calculate_hit_chance(player_unit, enemy_unit, _dist_to_e);

draw_set_color(make_color_rgb(240, 210, 100));
draw_text(_diag_x + 16 + _sx, _calc_y + _sy, "ACTIVE WEAPON: " + _sel_w.name);
draw_set_color(make_color_rgb(180, 205, 230));
draw_text(_diag_x + 16 + _sx, _calc_y + 22 + _sy, "* Range: " + string(_sel_w.range_min) + "-" + string(_sel_w.range_max) + " Cells | Current Target Distance: " + string(_dist_to_e) + " Cells");
draw_text(_diag_x + 16 + _sx, _calc_y + 42 + _sy, "* AP Cost: " + string(_sel_w.ap_cost) + " AP | Thermal Generation: +" + string(_sel_w.heat_cost) + "% Heat");

draw_set_color(make_color_rgb(100, 255, 140));
draw_text(_diag_x + 16 + _sx, _calc_y + 70 + _sy, "CALCULATED HIT PROBABILITY: " + string(_hit_pct) + "%");
draw_set_color(make_color_rgb(255, 140, 80));
draw_text(_diag_x + 16 + _sx, _calc_y + 90 + _sy, "EXPECTED DIRECT IMPACT: " + string(_sel_w.damage) + " DAMAGE");

// =========================================================================
// 5. COMMAND ACTION BAR (Bottom Left: y 566 to 750)
// =========================================================================
var _act_y = grid_oy + _grid_h + 12;
var _act_h = _gh - _act_y - 16;
var _act_w = _grid_w;

draw_set_color(make_color_rgb(10, 16, 24));
draw_rectangle(grid_ox + _sx, _act_y + _sy, grid_ox + _act_w + _sx, _act_y + _act_h + _sy, false);
draw_set_color(make_color_rgb(35, 60, 95));
draw_rectangle(grid_ox + _sx, _act_y + _sy, grid_ox + _act_w + _sx, _act_y + _act_h + _sy, true);

// Action Buttons
var _btn_defs = [
    { label: "[M] MOVE (1 AP/CELL)", mode: COMBAT_STATE.MOVE_MODE, ap: 1 },
    { label: "[1] 120MM CANNON (3 AP)", mode: COMBAT_STATE.TARGET_MODE, wpn: 0, ap: 3 },
    { label: "[2] GAU-88 VULCAN (2 AP)", mode: COMBAT_STATE.TARGET_MODE, wpn: 1, ap: 2 },
    { label: "[3] ARES MISSILES (4 AP)", mode: COMBAT_STATE.TARGET_MODE, wpn: 2, ap: 4 },
    { label: "[4] GUN-CLUB MELEE (3 AP)", mode: COMBAT_STATE.TARGET_MODE, wpn: 3, ap: 3 },
    { label: "[B] BRACE & VENT (2 AP)", brace: true, ap: 2 },
    { label: "[SPACE] END TURN", end_turn: true, ap: 0 }
];

var _bx_start = grid_ox + 12;
var _by_start = _act_y + 12;
var _b_w = 260;
var _b_h = 36;

for (var b = 0; b < array_length(_btn_defs); b++) {
    var _bd = _btn_defs[b];
    var _col_idx = b % 3;
    var _row_idx = floor(b / 3);
    var _cur_bx = _bx_start + _col_idx * (_b_w + 14);
    var _cur_by = _by_start + _row_idx * (_b_h + 10);
    var _b_hov = (_mx >= _cur_bx && _mx <= _cur_bx + _b_w && _my >= _cur_by && _my <= _cur_by + _b_h);

    if (_b_hov && _click && state == COMBAT_STATE.PLAYER_PHASE) {
        if (variable_struct_exists(_bd, "mode")) {
            if (variable_struct_exists(_bd, "wpn")) selected_weapon = _bd.wpn;
            if (_bd.mode == COMBAT_STATE.MOVE_MODE) recalculate_moves();
            state = _bd.mode;
        } else if (variable_struct_exists(_bd, "brace")) {
            if (player_unit.current_ap >= 2) {
                player_unit.current_ap -= 2;
                player_unit.braced = true;
                player_unit.current_heat = max(0, player_unit.current_heat - 25);
                add_log("[TACTICAL DEFENSE] Warhammer braced! +35% Evasion, -25% Heat vented.");
            }
        } else if (variable_struct_exists(_bd, "end_turn")) {
            add_log("[TURN END] Initiative passed to enemy forces.");
            state = COMBAT_STATE.AI_PHASE;
            state_timer = 0;
        }
    }

    draw_set_color(_b_hov ? make_color_rgb(30, 60, 90) : make_color_rgb(16, 26, 38));
    draw_rectangle(_cur_bx + _sx, _cur_by + _sy, _cur_bx + _b_w + _sx, _cur_by + _b_h + _sy, false);
    draw_set_color(make_color_rgb(60, 110, 170));
    draw_rectangle(_cur_bx + _sx, _cur_by + _sy, _cur_bx + _b_w + _sx, _cur_by + _b_h + _sy, true);
    draw_set_color(c_white);
    draw_text(_cur_bx + 12 + _sx, _cur_by + 9 + _sy, _bd.label);
}

// =========================================================================
// 6. LIVE COMBAT TERMINAL FEED (Bottom Right: y 566 to 750)
// =========================================================================
var _log_x = _diag_x;
var _log_y = _act_y;
var _log_w = _diag_w;
var _log_h = _act_h;

draw_set_color(make_color_rgb(8, 12, 18));
draw_rectangle(_log_x + _sx, _log_y + _sy, _log_x + _log_w + _sx, _log_y + _log_h + _sy, false);
draw_set_color(make_color_rgb(30, 50, 75));
draw_rectangle(_log_x + _sx, _log_y + _sy, _log_x + _log_w + _sx, _log_y + _log_h + _sy, true);

draw_set_color(make_color_rgb(100, 200, 255));
draw_text(_log_x + 12 + _sx, _log_y + 10 + _sy, ">> LIVE TACTICAL COMBAT LOG <<");

for (var l = 0; l < array_length(combat_log); l++) {
    var _line = combat_log[l];
    var _lcol = make_color_rgb(180, 210, 240);
    if (string_pos("CRITICAL", _line) > 0 || string_pos("BREACH", _line) > 0) _lcol = make_color_rgb(255, 90, 90);
    else if (string_pos("IMPACT", _line) > 0) _lcol = make_color_rgb(255, 200, 80);
    else if (string_pos("ACCOMPLISHED", _line) > 0) _lcol = c_lime;

    draw_set_color(_lcol);
    draw_text(_log_x + 12 + _sx, _log_y + 32 + l * 20 + _sy, _line);
}

// =========================================================================
// 6b. FLOATING COMBAT TEXT LAYER (docs/05)
// =========================================================================
for (var i = 0; i < array_length(floating_texts); i++) {
    var _ft = floating_texts[i];
    draw_set_alpha(_ft.alpha);
    draw_set_color(c_black);
    draw_text(_ft.x - string_width(_ft.text) / 2 + 1, _ft.y + 1, _ft.text);
    draw_set_color(_ft.color);
    draw_text(_ft.x - string_width(_ft.text) / 2, _ft.y, _ft.text);
    draw_set_alpha(1.0);
}

// =========================================================================
// 7. AFTER-ACTION REPORT (AAR) MODAL (VICTORY OR DEFEAT)
// =========================================================================
if (state == COMBAT_STATE.VICTORY_AAR || state == COMBAT_STATE.DEFEAT_AAR) {
    var _is_win = (state == COMBAT_STATE.VICTORY_AAR);
    var _mw_w = 660;
    var _mw_h = 420;
    var _mw_x = (_gw - _mw_w) / 2;
    var _mw_y = (_gh - _mw_h) / 2;

    draw_set_alpha(0.85);
    draw_set_color(c_black);
    draw_rectangle(0, 0, _gw, _gh, false);
    draw_set_alpha(1.0);

    draw_set_color(make_color_rgb(12, 18, 26));
    draw_rectangle(_mw_x, _mw_y, _mw_x + _mw_w, _mw_y + _mw_h, false);
    draw_set_color(_is_win ? c_lime : c_red);
    draw_rectangle(_mw_x, _mw_y, _mw_x + _mw_w, _mw_y + _mw_h, true);

    // Banner Text
    draw_set_color(_is_win ? make_color_rgb(80, 255, 120) : make_color_rgb(255, 80, 80));
    draw_text(_mw_x + 30, _mw_y + 24, _is_win ? "== MISSION ACCOMPLISHED // SECTOR DEFENDED ==" : "== DEFEAT // VANGUARD UNIT DESTROYED ==");

    draw_set_color(c_white);
    draw_text(_mw_x + 30, _mw_y + 55, "COMBAT CASUALTIES & AFTER-ACTION SUMMARY:");

    if (_is_win) {
        draw_set_color(make_color_rgb(180, 220, 255));
        draw_text(_mw_x + 30, _mw_y + 85, "* Combat Operations Payout: +120,000 Credits (Cr)");
        draw_text(_mw_x + 30, _mw_y + 110, "* Faction Standing Gain: +10 Standing (The Terran Coalition)");
        draw_set_color(make_color_rgb(100, 255, 140));
        draw_text(_mw_x + 30, _mw_y + 135, "* PILOT COMMENDATION: " + player_unit.pilot_name + " (+3 Accuracy, +2 Reflexes, +10 Morale)");
        draw_set_color(make_color_rgb(240, 210, 100));
        draw_text(_mw_x + 30, _mw_y + 170, "BATTLEFIELD SALVAGE RECOVERED (SAVED TO INVENTORY):");
        draw_set_color(make_color_rgb(200, 230, 255));
        draw_text(_mw_x + 50, _mw_y + 195, "-> 2x Vanguard Composite Plating (alloy_vanguard_comp)");
        draw_text(_mw_x + 50, _mw_y + 220, "-> 15x Raw Tungsten Ore (mat_tungsten)");
        draw_text(_mw_x + 50, _mw_y + 245, "-> 1x Stripped Autocannon Breech Assembly");
    } else {
        if (casualty_data.pilot_kia) {
            draw_set_color(make_color_rgb(255, 60, 60));
            draw_text(_mw_x + 30, _mw_y + 85, "* FATAL CATASTROPHE: Core breach detonated before cockpit ejection.");
            draw_text(_mw_x + 30, _mw_y + 110, "* PILOT KIA: " + casualty_data.pilot_name + " was KILLED IN ACTION.");
            draw_text(_mw_x + 30, _mw_y + 135, "* PERMADEATH: Pilot permanently removed. Added to PMC Memorial Wall.");
            draw_text(_mw_x + 30, _mw_y + 160, "* Base Morale has suffered a severe breakdown (-15 Morale).");
            draw_text(_mw_x + 30, _mw_y + 185, "* Chassis Asset " + player_unit.callsign + " completely destroyed.");
        } else {
            draw_set_color(make_color_rgb(255, 180, 80));
            draw_text(_mw_x + 30, _mw_y + 85, "* EJECTION SUCCESSFUL: Emergency escape thrusters cleared blast zone.");
            draw_text(_mw_x + 30, _mw_y + 110, "* PILOT WOUNDED: " + casualty_data.pilot_name + " evacuated to medical bay.");
            draw_text(_mw_x + 30, _mw_y + 135, "* Hospitalization required: 12 Days recovery | Med-Evac Fee: -15,000 Cr.");
            draw_text(_mw_x + 30, _mw_y + 160, "* Chassis Asset " + player_unit.callsign + " was completely written off.");
        }
    }

    // Proceed Button
    var _btn_p_x = _mw_x + 180;
    var _btn_p_y = _mw_y + 340;
    var _btn_p_w = 300;
    var _btn_p_h = 44;
    var _p_hov = (_mx >= _btn_p_x && _mx <= _btn_p_x + _btn_p_w && _my >= _btn_p_y && _my <= _btn_p_y + _btn_p_h);

    if (_p_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            if (_is_win) {
                obj_GameManager.add_funds(120000);
                obj_GameManager.add_alloy("alloy_vanguard_comp", 2);
                obj_GameManager.add_raw_material("mat_tungsten", 15);
                if (instance_exists(obj_FactionManager)) {
                    obj_FactionManager.modify_standing("faction_a", 10);
                }
                // Pilot Commendation XP
                for (var p = 0; p < array_length(obj_GameManager.facilities.roster_pilots); p++) {
                    var _p = obj_GameManager.facilities.roster_pilots[p];
                    if (_p.name == player_unit.pilot_name) {
                        _p.accuracy = min(100, _p.accuracy + 3);
                        _p.reflexes = min(100, _p.reflexes + 2);
                        _p.morale = min(100, _p.morale + 10);
                        _p.kills = (_p[$ "kills"] ?? 0) + 1;
                        _p.sorties = (_p[$ "sorties"] ?? 0) + 1;
                        break;
                    }
                }
            } else {
                // Defeat Consequences:
                // 1. Remove destroyed mobile suit
                if (array_length(obj_GameManager.inventory.deployable_mechs) > 0) {
                    array_delete(obj_GameManager.inventory.deployable_mechs, 0, 1);
                }
                // 2. Pilot KIA vs Hospitalization
                for (var p = array_length(obj_GameManager.facilities.roster_pilots) - 1; p >= 0; p--) {
                    var _p = obj_GameManager.facilities.roster_pilots[p];
                    if (_p.name == player_unit.pilot_name) {
                        if (casualty_data.pilot_kia) {
                            array_push(obj_GameManager.pmc_memorial_wall, {
                                name: _p.name,
                                callsign: _p.callsign,
                                date: "Cycle " + string(obj_GameManager.current_cycle_year) + " Day " + string(obj_GameManager.current_cycle_day),
                                cause: "Catastrophic Torso Breach in Tactical Combat"
                            });
                            array_delete(obj_GameManager.facilities.roster_pilots, p, 1);
                            for (var r = 0; r < array_length(obj_GameManager.facilities.roster_pilots); r++) {
                                obj_GameManager.facilities.roster_pilots[r].morale = max(10, obj_GameManager.facilities.roster_pilots[r].morale - 15);
                            }
                        } else {
                            _p.status = "HOSPITALIZED";
                            _p.recovery_days = 12;
                            _p.is_deployed = false;
                            _p.morale = max(15, _p.morale - 25);
                            obj_GameManager.spend_funds(casualty_data.med_fee);
                        }
                        break;
                    }
                }
            }
        }
        if (room_exists(rm_hq_terminal)) room_goto(rm_hq_terminal);
    }

    draw_set_color(_p_hov ? make_color_rgb(30, 90, 50) : make_color_rgb(18, 50, 30));
    draw_rectangle(_btn_p_x, _btn_p_y, _btn_p_x + _btn_p_w, _btn_p_y + _btn_p_h, false);
    draw_set_color(make_color_rgb(80, 240, 120));
    draw_rectangle(_btn_p_x, _btn_p_y, _btn_p_x + _btn_p_w, _btn_p_y + _btn_p_h, true);
    draw_set_color(c_white);
    draw_text(_btn_p_x + 28, _btn_p_y + 12, "[PROCEED TO HQ COMMAND TERMINAL]");
}
