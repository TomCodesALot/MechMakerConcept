/// @description obj_BattleManager Draw Event
// Renders 2:1 Front Mission Axonometric Battlefield, 3D Elevation Cliffs, Depth-Sorted Mobile Suits & Physical Projectiles
// Strictly implements docs/17_grand_scale_isometric_combat_system.md

var _sx = random_range(-screen_shake, screen_shake);
var _sy = random_range(-screen_shake, screen_shake);

// 0. Active Map Theater Backdrop Fill
var _cur_map = map_definitions[current_map_id];
draw_clear(_cur_map.bg_col);

// =========================================================================
// 1. RENDER ISOMETRIC 2:1 GROUND TILES & ELEVATION CLIFFS
// =========================================================================
for (var c = 0; c < grid_cols; c++) {
    for (var r = 0; r < grid_rows; r++) {
        var _elev = grid_elev[c][r];

        // 4 Corner coordinates of axonometric diamond
        var _p0_x = iso_to_screen_x(c, r, _elev, cam_x + _sx, cam_y + _sy, zoom);
        var _p0_y = iso_to_screen_y(c, r, _elev, cam_x + _sx, cam_y + _sy, zoom);

        var _p1_x = iso_to_screen_x(c + 1, r, _elev, cam_x + _sx, cam_y + _sy, zoom);
        var _p1_y = iso_to_screen_y(c + 1, r, _elev, cam_x + _sx, cam_y + _sy, zoom);

        var _p2_x = iso_to_screen_x(c + 1, r + 1, _elev, cam_x + _sx, cam_y + _sy, zoom);
        var _p2_y = iso_to_screen_y(c + 1, r + 1, _elev, cam_x + _sx, cam_y + _sy, zoom);

        var _p3_x = iso_to_screen_x(c, r + 1, _elev, cam_x + _sx, cam_y + _sy, zoom);
        var _p3_y = iso_to_screen_y(c, r + 1, _elev, cam_x + _sx, cam_y + _sy, zoom);

        // Ground terrain color based on theater palette, terrain type and elevation tier
        var _map_def = map_definitions[current_map_id];
        var _terr = grid_terrain[c][r];
        var _tile_col = _map_def.grid_col_base;
        if (_elev == 1) _tile_col = _map_def.grid_col_elev1;
        else if (_elev == 2) _tile_col = _map_def.grid_col_elev2;
        else if (_elev >= 3) _tile_col = merge_color(_map_def.grid_col_elev2, c_white, 0.28);

        if (_terr == 1) {
            // Road / Runway (Smooth concrete asphalt)
            _tile_col = make_color_rgb(46, 54, 64);
        } else if (_terr == 2) {
            // Rubble / Masonry Debris
            _tile_col = make_color_rgb(58, 48, 42);
        } else if (_terr == 3) {
            // Seawater / Coolant Canal
            var _wave = 0.5 + 0.5 * sin((current_time * 0.003) + (c * 0.5) + (r * 0.7));
            _tile_col = merge_color(make_color_rgb(14, 52, 88), make_color_rgb(28, 88, 135), _wave);
        } else if (_terr == 4) {
            // Vacuum Deep Space Chasm
            _tile_col = make_color_rgb(4, 6, 12);
        } else if (_terr == 5) {
            // Molten Slag Drainage Runoff
            var _heat = 0.5 + 0.5 * sin((current_time * 0.005) + (c * 0.8) + (r * 0.4));
            _tile_col = merge_color(make_color_rgb(180, 52, 16), make_color_rgb(240, 110, 24), _heat);
        }

        // Draw Filled Isometric Diamond Face
        draw_primitive_begin(pr_trianglefan);
        draw_vertex_color(_p0_x, _p0_y, _tile_col, 1.0);
        draw_vertex_color(_p1_x, _p1_y, _tile_col, 1.0);
        draw_vertex_color(_p2_x, _p2_y, _tile_col, 1.0);
        draw_vertex_color(_p3_x, _p3_y, _tile_col, 1.0);
        draw_primitive_end();

        // 3D Elevation Cliff Faces
        if (_elev > 0) {
            // South-East Edge Cliff Wall (Drop to lower neighbor or base)
            var _drop_se = false;
            var _drop_se_diff = _elev;
            if (r + 1 < grid_rows) {
                if (grid_elev[c][r + 1] < _elev) {
                    _drop_se = true;
                    _drop_se_diff = _elev - grid_elev[c][r + 1];
                }
            } else {
                _drop_se = true;
            }

            if (_drop_se) {
                var _wall_h = _drop_se_diff * elev_h * zoom;
                draw_primitive_begin(pr_trianglefan);
                draw_vertex_color(_p3_x, _p3_y, _map_def.cliff_col_se, 1.0);
                draw_vertex_color(_p2_x, _p2_y, _map_def.cliff_col_se, 1.0);
                draw_vertex_color(_p2_x, _p2_y + _wall_h, _map_def.cliff_col_sw, 1.0);
                draw_vertex_color(_p3_x, _p3_y + _wall_h, _map_def.cliff_col_sw, 1.0);
                draw_primitive_end();
            }

            // South-West Edge Cliff Wall
            var _drop_sw = false;
            var _drop_sw_diff = _elev;
            if (c + 1 < grid_cols) {
                if (grid_elev[c + 1][r] < _elev) {
                    _drop_sw = true;
                    _drop_sw_diff = _elev - grid_elev[c + 1][r];
                }
            } else {
                _drop_sw = true;
            }

            if (_drop_sw) {
                var _wall_h = _drop_sw_diff * elev_h * zoom;
                draw_primitive_begin(pr_trianglefan);
                draw_vertex_color(_p1_x, _p1_y, _map_def.cliff_col_se, 1.0);
                draw_vertex_color(_p2_x, _p2_y, _map_def.cliff_col_se, 1.0);
                draw_vertex_color(_p2_x, _p2_y + _wall_h, _map_def.cliff_col_sw, 1.0);
                draw_vertex_color(_p1_x, _p1_y + _wall_h, _map_def.cliff_col_sw, 1.0);
                draw_primitive_end();
            }
        }

        // Tactical Grid Lines
        draw_set_color(make_color_rgb(32, 46, 64));
        draw_line(_p0_x, _p0_y, _p1_x, _p1_y);
        draw_line(_p1_x, _p1_y, _p2_x, _p2_y);
        draw_line(_p2_x, _p2_y, _p3_x, _p3_y);
        draw_line(_p3_x, _p3_y, _p0_x, _p0_y);

        // Highlight Valid Movement Range (Cyan)
        if (state == COMBAT_STATE.MOVE_MODE) {
            for (var m = 0; m < array_length(valid_move_tiles); m++) {
                var _vt = valid_move_tiles[m];
                if (_vt.col == c && _vt.row == r) {
                    draw_primitive_begin(pr_trianglefan);
                    draw_vertex_color(_p0_x, _p0_y, make_color_rgb(50, 180, 255), 0.35);
                    draw_vertex_color(_p1_x, _p1_y, make_color_rgb(50, 180, 255), 0.35);
                    draw_vertex_color(_p2_x, _p2_y, make_color_rgb(50, 180, 255), 0.35);
                    draw_vertex_color(_p3_x, _p3_y, make_color_rgb(50, 180, 255), 0.35);
                    draw_primitive_end();

                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_line(_p0_x, _p0_y, _p1_x, _p1_y);
                    draw_line(_p1_x, _p1_y, _p2_x, _p2_y);
                    draw_line(_p2_x, _p2_y, _p3_x, _p3_y);
                    draw_line(_p3_x, _p3_y, _p0_x, _p0_y);
                }
            }
        }

        // Highlight Weapon Attack Range (Amber / Orange)
        if (state == COMBAT_STATE.TARGET_MODE && selected_unit_idx >= 0 && selected_unit_idx < array_length(units)) {
            var _cur_u = units[selected_unit_idx];
            if (selected_weapon < array_length(_cur_u.weapons)) {
                var _w = _cur_u.weapons[selected_weapon];
                var _d = calculate_distance(_cur_u.grid_c, _cur_u.grid_r, c, r);
                if (_d >= _w.range_min && _d <= _w.range_max) {
                    draw_primitive_begin(pr_trianglefan);
                    draw_vertex_color(_p0_x, _p0_y, make_color_rgb(255, 140, 40), 0.20);
                    draw_vertex_color(_p1_x, _p1_y, make_color_rgb(255, 140, 40), 0.20);
                    draw_vertex_color(_p2_x, _p2_y, make_color_rgb(255, 140, 40), 0.20);
                    draw_vertex_color(_p3_x, _p3_y, make_color_rgb(255, 140, 40), 0.20);
                    draw_primitive_end();
                }
            }
        }

        // Hover Reticle
        if (hover_c == c && hover_r == r) {
            draw_set_color(c_white);
            draw_line(_p0_x, _p0_y, _p1_x, _p1_y);
            draw_line(_p1_x, _p1_y, _p2_x, _p2_y);
            draw_line(_p2_x, _p2_y, _p3_x, _p3_y);
            draw_line(_p3_x, _p3_y, _p0_x, _p0_y);
        }
    }
}

// =========================================================================
// =========================================================================
// 1B. GROUND-LEVEL TACTICAL VECTOR MARCH PATH (Dashed March Route)
// =========================================================================
if (state == COMBAT_STATE.MOVE_MODE && selected_unit_idx >= 0 && selected_unit_idx < array_length(units)) {
    var _cur_sel = units[selected_unit_idx];
    if (hover_c >= 0 && hover_r >= 0 && (hover_c != _cur_sel.grid_c || hover_r != _cur_sel.grid_r)) {
        var _hover_vt = undefined;
        for (var m = 0; m < array_length(valid_move_tiles); m++) {
            if (valid_move_tiles[m].col == hover_c && valid_move_tiles[m].row == hover_r) {
                _hover_vt = valid_move_tiles[m];
                break;
            }
        }

        if (!is_undefined(_hover_vt)) {
            var _src_x = iso_to_screen_x(_cur_sel.grid_c, _cur_sel.grid_r, _cur_sel.elev, cam_x, cam_y, zoom);
            var _src_y = iso_to_screen_y(_cur_sel.grid_c, _cur_sel.grid_r, _cur_sel.elev, cam_x, cam_y, zoom);
            var _dx = iso_to_screen_x(hover_c, hover_r, grid_elev[hover_c][hover_r], cam_x, cam_y, zoom);
            var _dy = iso_to_screen_y(hover_c, hover_r, grid_elev[hover_c][hover_r], cam_x, cam_y, zoom);

            var _dist_px = point_distance(_src_x, _src_y, _dx, _dy);
            var _dir_deg = point_direction(_src_x, _src_y, _dx, _dy);

            // Pulsing Ground Target Diamond
            var _ring_pulse = 0.5 + 0.5 * sin(current_time * 0.012);
            var _rx = (18 + _ring_pulse * 4) * zoom;
            var _ry = (9 + _ring_pulse * 2) * zoom;
            draw_set_color(make_color_rgb(64, 224, 255));
            draw_set_alpha(0.75);
            draw_ellipse(_dx - _rx, _dy - _ry, _dx + _rx, _dy + _ry, true);
            draw_set_alpha(0.35);
            draw_ellipse(_dx - _rx * 0.6, _dy - _ry * 0.6, _dx + _rx * 0.6, _dy + _ry * 0.6, true);
            draw_set_alpha(1.0);

            // Animated Marching Dashed Line Vector
            var _dash_len = 10 * zoom;
            var _gap_len = 6 * zoom;
            var _seg_len = _dash_len + _gap_len;
            var _march_anim = (current_time * 0.035) % _seg_len;

            var _p = _march_anim;
            while (_p < _dist_px) {
                var _x1 = _sx + lengthdir_x(_p, _dir_deg);
                var _y1 = _sy + lengthdir_y(_p, _dir_deg);
                var _x2 = _sx + lengthdir_x(min(_dist_px, _p + _dash_len), _dir_deg);
                var _y2 = _sy + lengthdir_y(min(_dist_px, _p + _dash_len), _dir_deg);

                // Contrast Shadow
                draw_set_color(make_color_rgb(10, 24, 40));
                draw_line_width(_x1, _y1 + 1, _x2, _y2 + 1, 3.5 * zoom);
                // Tactical Cyan Marching Vector
                draw_set_color(make_color_rgb(64, 224, 255));
                draw_line_width(_x1, _y1, _x2, _y2, 2.0 * zoom);

                _p += _seg_len;
            }
        }
    }
}

// 2. ISOMETRIC PAINTERS ALGORITHM DEPTH-SORTED ENTITY RENDERING
// =========================================================================
var _draw_list = [];

// A. Cover Props / Barricades
for (var c = 0; c < grid_cols; c++) {
    for (var r = 0; r < grid_rows; r++) {
        if (grid_cover[c][r] > 0) {
            array_push(_draw_list, {
                type: "COVER",
                col: c,
                row: r,
                elev: grid_elev[c][r],
                cover_val: grid_cover[c][r],
                sort_y: (c + r) * 1000 + grid_elev[c][r] * 100 + 20
            });
        }
    }
}

// B. Mobile Suits
for (var u = 0; u < array_length(units); u++) {
    var _u = units[u];
    array_push(_draw_list, {
        type: "UNIT",
        unit: _u,
        sort_y: (_u.grid_c + _u.grid_r) * 1000 + _u.elev * 100 + 50
    });
}

// C. In-Flight Physical Projectiles
for (var p = 0; p < array_length(projectiles); p++) {
    var _proj = projectiles[p];
    var _pc = screen_to_iso_col(_proj.cur_x, _proj.cur_y, cam_x, cam_y, zoom);
    var _pr = screen_to_iso_row(_proj.cur_x, _proj.cur_y, cam_x, cam_y, zoom);
    array_push(_draw_list, {
        type: "PROJECTILE",
        proj: _proj,
        sort_y: (_pc + _pr) * 1000 + 70
    });
}

// D. Explosions & Sparks FX
for (var f = 0; f < array_length(combat_fx); f++) {
    var _fx = combat_fx[f];
    var _fc = screen_to_iso_col(_fx.x, _fx.y, cam_x, cam_y, zoom);
    var _fr = screen_to_iso_row(_fx.x, _fx.y, cam_x, cam_y, zoom);
    array_push(_draw_list, {
        type: "FX",
        fx: _fx,
        sort_y: (_fc + _fr) * 1000 + 90
    });
}

// Simple insertion sort by sort_y ascending (back-to-front painter algorithm)
var _len = array_length(_draw_list);
for (var i = 1; i < _len; i++) {
    var _key = _draw_list[i];
    var j = i - 1;
    while (j >= 0 && _draw_list[j].sort_y > _key.sort_y) {
        _draw_list[j + 1] = _draw_list[j];
        j = j - 1;
    }
    _draw_list[j + 1] = _key;
}

// RENDER ALL DEPTH-SORTED ENTITIES
for (var i = 0; i < _len; i++) {
    var _item = _draw_list[i];

    // --- Render Cover Barricades ---
    if (_item.type == "COVER") {
        var _bx = iso_to_screen_x(_item.col, _item.row, _item.elev, cam_x + _sx, cam_y + _sy, zoom);
        var _by = iso_to_screen_y(_item.col, _item.row, _item.elev, cam_x + _sx, cam_y + _sy, zoom);
        var _cw = 24.0 * zoom;
        var _ch = 22.0 * zoom;

        var _is_bastion = (_item.cover_val == 2);
        draw_set_color(_is_bastion ? make_color_rgb(32, 44, 58) : make_color_rgb(52, 50, 44));
        draw_rectangle(_bx - _cw, _by - _ch, _bx + _cw, _by, false);
        draw_set_color(_is_bastion ? make_color_rgb(100, 160, 220) : make_color_rgb(160, 150, 120));
        draw_rectangle(_bx - _cw, _by - _ch, _bx + _cw, _by, true);

        draw_set_color(c_white);
        draw_text_transformed(_bx - 22 * zoom, _by - 18 * zoom, _is_bastion ? "BASTION" : "RUBBLE", 0.60 * zoom, 0.60 * zoom, 0);
    }

    // --- Render Mobile Suits ---
    else if (_item.type == "UNIT") {
        var _u = _item.unit;
        var _vx = _u.visual_x + (_u.recoil_x * zoom) + _sx;
        var _vy = _u.visual_y + (_u.recoil_y * zoom) + _sy;

        // Active Selection Ring
        if (selected_unit_idx >= 0 && selected_unit_idx < array_length(units) && units[selected_unit_idx] == _u) {
            draw_set_color(make_color_rgb(80, 220, 255));
            draw_ellipse(_vx - 30 * zoom, _vy - 13 * zoom, _vx + 30 * zoom, _vy + 13 * zoom, true);
        }

        // Mobile Suit Sprite Rendering with 4-Way Directional Mirroring
        var _spr = get_unit_sprite(_u);
        var _facing_sign = (iso_is_back_facing(_u.facing)) ? ((_u.facing == 2) ? 1.0 : -1.0) : ((_u.facing == 0) ? 1.0 : -1.0);
        var _xscale = _facing_sign * zoom;
        var _yscale = zoom;
        var _alpha = _u.is_destroyed ? 0.35 : 1.0;

        // Environmental Terrain Context for Unit
        var _u_c = _u.grid_c;
        var _u_r = _u.grid_r;
        var _u_terr = grid_terrain[_u_c][_u_r];
        var _is_space_env = (_cur_map.theater == "SPACE" || _u_terr == 4);
        var _u_mtype = variable_struct_get(_u, "move_type") ?? "biped";
        var _u_is_hover = (_u_mtype == "hover");
        var _u_is_air = (variable_struct_exists(_u, "is_aircraft") && _u.is_aircraft) || (_u_mtype == "aero");
        var _u_is_inf = (variable_struct_exists(_u, "is_infantry") && _u.is_infantry);

        // A. Dynamic Under-Unit Environmental Contact Shadow / Water Ripple / Slag Radiance
        var _draw_env_contact = function(_tx, _ty, _rw, _rh, _terr, _is_space, _is_hover, _is_air, _c, _r, _facing_dir) {
            if (_terr == 3) {
                // --- WATER CANAL / RIVER SURFACE ---
                if (_is_hover) {
                    // Hovercraft High-Pressure Repulsor Cushion & Spray
                    draw_set_color(make_color_rgb(210, 245, 255));
                    draw_set_alpha(0.45);
                    draw_ellipse(_tx - _rw, _ty - _rh, _tx + _rw, _ty + _rh, false);

                    // Expanding Water Ripple Ring
                    var _w_rip = (current_time * 0.0022 + _c * 0.4) % 1.0;
                    draw_set_color(make_color_rgb(150, 225, 255));
                    draw_set_alpha(0.60 * (1.0 - _w_rip));
                    draw_ellipse(_tx - (_rw + 14 * _w_rip * zoom), _ty - (_rh + 7 * _w_rip * zoom), _tx + (_rw + 14 * _w_rip * zoom), _ty + (_rh + 7 * _w_rip * zoom), true);

                    // Twin Trailing Spray Wakes behind Skirt
                    var _wake_dir = -_facing_dir;
                    draw_set_color(c_white);
                    draw_set_alpha(0.35);
                    draw_ellipse(_tx + (_wake_dir * 18 * zoom) - 9 * zoom, _ty - 4 * zoom, _tx + (_wake_dir * 18 * zoom) + 9 * zoom, _ty + 4 * zoom, false);
                } else if (_is_air) {
                    // Aircraft Downwash Shadow on Water
                    draw_set_color(make_color_rgb(10, 36, 60));
                    draw_set_alpha(0.32);
                    draw_ellipse(_tx - _rw, _ty - _rh, _tx + _rw, _ty + _rh, false);
                } else {
                    // Wading Mech / Vehicle / Infantry Concentric Water Ripples
                    var _rip1 = (current_time * 0.0016 + _c * 0.5) % 1.0;
                    var _rip2 = (current_time * 0.0016 + _c * 0.5 + 0.5) % 1.0;
                    draw_set_color(make_color_rgb(140, 215, 255));
                    draw_set_alpha(0.50 * (1.0 - _rip1));
                    draw_ellipse(_tx - (_rw * (0.8 + 0.6 * _rip1)), _ty - (_rh * (0.8 + 0.6 * _rip1)), _tx + (_rw * (0.8 + 0.6 * _rip1)), _ty + (_rh * (0.8 + 0.6 * _rip1)), true);
                    draw_set_alpha(0.50 * (1.0 - _rip2));
                    draw_ellipse(_tx - (_rw * (0.8 + 0.6 * _rip2)), _ty - (_rh * (0.8 + 0.6 * _rip2)), _tx + (_rw * (0.8 + 0.6 * _rip2)), _ty + (_rh * (0.8 + 0.6 * _rip2)), true);
                }
            } else if (_is_space) {
                // --- ZERO-G ORBITAL SPACE / VACUUM VOID ---
                // No black ground drop shadow in orbital vacuum!
                if (_terr == 1) {
                    // Magnetic Boot Clamps on Metal Catwalk / Platform
                    draw_set_color(make_color_rgb(60, 180, 255));
                    draw_set_alpha(0.40);
                    draw_circle(_tx - 8 * zoom, _ty - 2 * zoom, 3 * zoom, false);
                    draw_circle(_tx + 8 * zoom, _ty - 2 * zoom, 3 * zoom, false);
                }
            } else if (_terr == 5) {
                // --- MOLTEN SLAG RUNOFF / LAVA FISSURE ---
                var _heat_pulse = 0.5 + 0.5 * sin(current_time * 0.005 + _c);
                draw_set_color(merge_color(make_color_rgb(255, 80, 18), make_color_rgb(255, 175, 40), _heat_pulse));
                draw_set_alpha(0.52);
                draw_ellipse(_tx - _rw, _ty - _rh, _tx + _rw, _ty + _rh, false);
            } else {
                // --- SOLID GROUND (ROAD, RUBBLE, PLAINS) ---
                if (_is_air) {
                    draw_set_color(c_black);
                    draw_set_alpha(0.30);
                    draw_ellipse(_tx - _rw, _ty - _rh, _tx + _rw, _ty + _rh, false);
                } else if (_terr == 1) {
                    // Paved Road Asphalt Contact Shadow
                    draw_set_color(make_color_rgb(12, 16, 20));
                    draw_set_alpha(0.48);
                    draw_ellipse(_tx - _rw, _ty - _rh, _tx + _rw, _ty + _rh, false);
                } else if (_terr == 2) {
                    // Rubble / Basalt Rocky Contact Shadow
                    draw_set_color(make_color_rgb(26, 20, 16));
                    draw_set_alpha(0.44);
                    draw_ellipse(_tx - _rw, _ty - _rh, _tx + _rw, _ty + _rh, false);
                } else {
                    // Standard Soil / Dirt Plains Contact Shadow
                    draw_set_color(make_color_rgb(18, 14, 10));
                    draw_set_alpha(0.40);
                    draw_ellipse(_tx - _rw, _ty - _rh, _tx + _rw, _ty + _rh, false);
                }
            }
            draw_set_alpha(1.0);
        };

        // B. Vertical Visual Displacement Matching Environment
        var _get_env_y = function(_base_y, _terr, _is_space, _is_hover, _is_air, _c, _r) {
            if (_is_air) {
                return _base_y - (16.0 * zoom);
            } else if (_is_space) {
                // Zero-G Inertial Floating Drift Oscillation
                return _base_y + sin((current_time * 0.0022) + (_c * 1.5) + (_r * 2.1)) * 3.8 * zoom;
            } else if (_terr == 3) {
                if (_is_hover) {
                    // Hovercraft skimming on repulsor air cushion
                    return _base_y - (3.0 * zoom) + sin(current_time * 0.004 + _c) * 1.2 * zoom;
                } else {
                    // Wading immersion (submerged into water depth)
                    return _base_y + (3.0 * zoom);
                }
            } else if (_is_hover) {
                return _base_y - (3.0 * zoom) + sin(current_time * 0.003 + _c) * 1.0 * zoom;
            }
            return _base_y;
        };

        // C. Post-Sprite Surface Interaction Overlays (Waterline Splashes & Vernier Flares)
        var _draw_env_overlay = function(_tx, _ty, _draw_y, _terr, _is_space, _is_hover, _is_air, _c, _r, _facing_dir, _destroyed) {
            if (_destroyed) return;

            if (_terr == 3 && !_is_hover && !_is_air) {
                // Wading Mech / Squad Waterline Splashing Foam Ring & Depth Wash
                draw_set_color(make_color_rgb(225, 248, 255));
                draw_set_alpha(0.68);
                draw_ellipse(_tx - 17 * zoom, _ty - 4 * zoom, _tx + 17 * zoom, _ty + 4 * zoom, true);
                draw_set_color(make_color_rgb(150, 220, 255));
                draw_ellipse(_tx - 15 * zoom, _ty - 3 * zoom, _tx + 15 * zoom, _ty + 3 * zoom, true);

                // Water Submersion Wash over lower legs
                draw_set_color(make_color_rgb(14, 52, 88));
                draw_set_alpha(0.45);
                draw_ellipse(_tx - 15 * zoom, _ty - 2 * zoom, _tx + 15 * zoom, _ty + 5 * zoom, false);
                draw_set_alpha(1.0);
            } else if (_is_space) {
                // Active Attitude Vernier RCS Thrusters in Zero-G
                var _rcs_phase = (current_time + (_c * 420) + (_r * 290)) % 1500;
                if (_rcs_phase < 260) {
                    var _r_alpha = 0.85 * sin((_rcs_phase / 260) * pi);
                    var _jx1 = _tx - (7 * zoom * _facing_dir);
                    var _jy1 = _draw_y - (34 * zoom);
                    var _jx2 = _tx + (9 * zoom * _facing_dir);
                    var _jy2 = _draw_y - (32 * zoom);
                    draw_set_color(c_white);
                    draw_set_alpha(_r_alpha);
                    draw_circle(_jx1, _jy1, 1.8 * zoom, false);
                    draw_circle(_jx2, _jy2, 1.8 * zoom, false);
                    draw_set_color(make_color_rgb(70, 215, 255));
                    draw_line_width(_jx1, _jy1, _jx1 - (6 * zoom * _facing_dir), _jy1 - 5 * zoom, 2.0 * zoom);
                    draw_line_width(_jx2, _jy2, _jx2 + (6 * zoom * _facing_dir), _jy2 - 5 * zoom, 2.0 * zoom);
                    draw_set_alpha(1.0);
                }
            } else if (_terr == 5) {
                // Rising Thermal Sparks / Embers from Slag Fissure
                var _sp_y = _ty - ((current_time * 0.035 + _c * 18) % 36) * zoom;
                var _sp_x = _tx + sin(current_time * 0.005 + _c * 2) * 12 * zoom;
                draw_set_color(make_color_rgb(255, 195, 50));
                draw_set_alpha(0.75);
                draw_circle(_sp_x, _sp_y, 1.5 * zoom, false);
                draw_set_alpha(1.0);
            }
        };

        var _draw_unit_overlays = function(_ux, _uy, _usx, _usy, _u_struct, _u_alpha, _is_shield_pass) {
            if (_u_struct.is_destroyed) return;
            var _ov_key = _is_shield_pass ? "weapon_overlay_secondary" : "weapon_overlay_primary";
            if (!variable_struct_exists(_u_struct, _ov_key)) return;
            var _ov_name = _u_struct[$ _ov_key];
            if (!is_string(_ov_name) || _ov_name == "") return;
            var _ov_spr = asset_get_index(_ov_name);
            if (_ov_spr == -1 || !sprite_exists(_ov_spr)) return;
            var _f_sign = (_usx >= 0) ? 1 : -1;
            var _sc_abs = abs(_usy);
            if (sprite_get_yoffset(_ov_spr) == 80) {
                var _ox_base = _is_shield_pass ? 28 : -22;
                var _oy_base = _is_shield_pass ? -54 : -48;
                var _off_key = _is_shield_pass ? "overlay_shield_offset" : "overlay_primary_offset";
                if (variable_struct_exists(_u_struct, _off_key) && is_struct(_u_struct[$ _off_key])) {
                    _ox_base = _u_struct[$ _off_key].x;
                    _oy_base = _u_struct[$ _off_key].y;
                }
                var _ox = _ox_base * _f_sign * _sc_abs;
                var _oy = _oy_base * _sc_abs;
                var _osc = _is_shield_pass ? 0.50 : 0.52;
                draw_sprite_ext(_ov_spr, 0, _ux + _ox, _uy + _oy, _usx * _osc, _usy * _osc, 0, _is_shield_pass ? _u_struct.image_blend : c_white, _u_alpha);
            } else {
                draw_sprite_ext(_ov_spr, 0, _ux, _uy, _usx, _usy, 0, c_white, _u_alpha);
            }
        };

        // 1. Standard Ground Infantry Squads (Combined-Arms Squad on Tile)
        if (_u_is_inf) {
            _draw_env_contact(_vx, _vy, 22 * zoom, 8 * zoom, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r, _facing_sign);
            var _inf_y = _get_env_y(_vy, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r);
            if (sprite_exists(_spr)) {
                draw_sprite_ext(_spr, floor(_u.anim_frame), _vx, _inf_y, _xscale * 0.95, _yscale * 0.95, 0, _u.image_blend, _alpha);
            }
            _draw_env_overlay(_vx, _vy, _inf_y, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r, _facing_sign, _u.is_destroyed);
        }
        // 2. High-Altitude Atmospheric Aircraft & Gunships (Hovering Flight Shadow)
        else if (_u_is_air) {
            _draw_env_contact(_vx, _vy, 26 * zoom, 10 * zoom, _u_terr, _is_space_env, _u_is_hover, true, _u_c, _u_r, _facing_sign);
            var _fly_y = _get_env_y(_vy, _u_terr, _is_space_env, _u_is_hover, true, _u_c, _u_r);
            if (sprite_exists(_spr)) {
                draw_sprite_ext(_spr, floor(_u.anim_frame), _vx, _fly_y, _xscale, _yscale, 0, _u.image_blend, _alpha);
            }
            _draw_env_overlay(_vx, _vy, _fly_y, _u_terr, _is_space_env, _u_is_hover, true, _u_c, _u_r, _facing_sign, _u.is_destroyed);
        }
        // 3. Dual Platoon Structure: 3-Vehicle / 3-Mech Platoon vs 1-Mech Super Ace
        else if (_u.squad_type == "PLATOON_3") {
            // Render Staggered Wingman 1 (Left Wing)
            if (_u.squad_members_count >= 2 && !_u.is_destroyed && sprite_exists(_spr)) {
                var _w1_x = _vx - (18.0 * zoom * _facing_sign);
                var _w1_y = _vy - (12.0 * zoom);
                _draw_env_contact(_w1_x, _w1_y, 18 * zoom, 7 * zoom, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r, _facing_sign);
                var _w1_draw_y = _get_env_y(_w1_y, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r);
                draw_sprite_ext(_spr, floor(_u.anim_frame), _w1_x, _w1_draw_y, _xscale * 0.90, _yscale * 0.90, 0, _u.image_blend, 0.90);
                _draw_env_overlay(_w1_x, _w1_y, _w1_draw_y, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r, _facing_sign, _u.is_destroyed);
            }

            // Render Staggered Wingman 2 (Right Wing)
            if (_u.squad_members_count >= 3 && !_u.is_destroyed && sprite_exists(_spr)) {
                var _w2_x = _vx - (18.0 * zoom * _facing_sign);
                var _w2_y = _vy + (12.0 * zoom);
                _draw_env_contact(_w2_x, _w2_y, 18 * zoom, 7 * zoom, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r, _facing_sign);
                var _w2_draw_y = _get_env_y(_w2_y, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r);
                draw_sprite_ext(_spr, floor(_u.anim_frame), _w2_x, _w2_draw_y, _xscale * 0.90, _yscale * 0.90, 0, _u.image_blend, 0.90);
                _draw_env_overlay(_w2_x, _w2_y, _w2_draw_y, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r, _facing_sign, _u.is_destroyed);
            }

            // Lead Mech Surface Contact FX
            _draw_env_contact(_vx, _vy, 24 * zoom, 10 * zoom, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r, _facing_sign);
            var _lead_y = _get_env_y(_vy, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r);

            // Lead Mech Sprite
            if (sprite_exists(_spr)) {
                _draw_unit_overlays(_vx, _lead_y, _xscale, _yscale, _u, _alpha, true);
                draw_sprite_ext(_spr, floor(_u.anim_frame), _vx, _lead_y, _xscale, _yscale, 0, _u.image_blend, _alpha);
                _draw_unit_overlays(_vx, _lead_y, _xscale, _yscale, _u, _alpha, false);
            }
            _draw_env_overlay(_vx, _vy, _lead_y, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r, _facing_sign, _u.is_destroyed);
        } else {
            // Super Ace (1 Unit Prototype) with 1.15 Scale & Evasion Afterimages
            var _ace_scale = 1.15;
            _draw_env_contact(_vx, _vy, 26 * zoom, 11 * zoom, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r, _facing_sign);
            var _ace_y = _get_env_y(_vy, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r);

            // Motion Blur Evasion Afterimages
            if (!_u.is_destroyed && sprite_exists(_spr)) {
                var _after_x = _vx - (4.0 * zoom * _facing_sign);
                var _after_y = _ace_y - (2.0 * zoom);
                draw_sprite_ext(_spr, floor(_u.anim_frame), _after_x, _after_y, _xscale * _ace_scale, _yscale * _ace_scale, 0, make_color_rgb(100, 220, 255), 0.25);
            }

            // Lead Ace Sprite
            if (sprite_exists(_spr)) {
                _draw_unit_overlays(_vx, _ace_y, _xscale * _ace_scale, _yscale * _ace_scale, _u, _alpha, true);
                draw_sprite_ext(_spr, floor(_u.anim_frame), _vx, _ace_y, _xscale * _ace_scale, _yscale * _ace_scale, 0, _u.image_blend, _alpha);
                _draw_unit_overlays(_vx, _ace_y, _xscale * _ace_scale, _yscale * _ace_scale, _u, _alpha, false);
            }
            _draw_env_overlay(_vx, _vy, _ace_y, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r, _facing_sign, _u.is_destroyed);
        }

        // --- GOAL FINAL: PERSISTENT TACTICAL BATTLE SCARS & CRIPPLED LIMB FX ---
        if (!_u.is_destroyed && variable_struct_exists(_u, "damaged_parts") && is_struct(_u.damaged_parts)) {
            var _cur_draw_y = _get_env_y(_vy, _u_terr, _is_space_env, _u_is_hover, _u_is_air, _u_c, _u_r);
            var _cur_scale = (_u.squad_type == "PLATOON_3") ? 1.0 : 1.15;

            // Severed Left Arm Socket Overlay & Arc Sparks
            if (variable_struct_exists(_u.damaged_parts, "arm_left") && _u.damaged_parts.arm_left && sprite_exists(spr_ms_ironclad_hit_left_arm_off)) {
                draw_sprite_ext(spr_ms_ironclad_hit_left_arm_off, 0, _vx, _cur_draw_y, _xscale * _cur_scale, _yscale * _cur_scale, 0, c_white, 0.85);
                if ((current_time + _u_c * 110) % 360 < 120) {
                    draw_set_color(make_color_rgb(100, 220, 255));
                    draw_circle(_vx - (8 * zoom * _facing_sign), _cur_draw_y - (22 * zoom), 1.8 * zoom, false);
                }
            }

            // Severed Right Arm Socket Overlay & Fiery Sparks
            if (variable_struct_exists(_u.damaged_parts, "arm_right") && _u.damaged_parts.arm_right && sprite_exists(spr_ms_ironclad_hit_right_arm_off)) {
                draw_sprite_ext(spr_ms_ironclad_hit_right_arm_off, 0, _vx, _cur_draw_y, _xscale * _cur_scale, _yscale * _cur_scale, 0, c_white, 0.85);
                if ((current_time + _u_r * 130) % 400 < 130) {
                    draw_set_color(make_color_rgb(255, 180, 50));
                    draw_circle(_vx + (8 * zoom * _facing_sign), _cur_draw_y - (20 * zoom), 2.0 * zoom, false);
                }
            }

            // Crippled Hydraulic Legs Trailing Smoke
            if (variable_struct_exists(_u.damaged_parts, "legs") && _u.damaged_parts.legs) {
                if ((current_time + _u_c * 70) % 320 < 160) {
                    draw_set_color(make_color_rgb(190, 200, 215));
                    draw_set_alpha(0.45);
                    draw_circle(_vx, _cur_draw_y - (5 * zoom), 3.5 * zoom, false);
                    draw_set_alpha(1.0);
                }
            }
        }

        // Floating Unit Overhead Status (Callsign, Formation Tag & HP Bar)
        if (!_u.is_destroyed) {
            var _bar_w = 46.0 * zoom;
            var _bar_h = 5.0 * zoom;
            var _by = _vy - (84.0 * zoom);
            var _hp_norm = clamp(_u.components.torso.cur / _u.components.torso.max, 0, 1);

            draw_set_color(make_color_rgb(12, 18, 24));
            draw_rectangle(_vx - _bar_w * 0.5, _by, _vx + _bar_w * 0.5, _by + _bar_h, false);

            // Goal G: Boss Regenerative Phase Barrier Bar
            if (variable_struct_exists(_u, "barrier_cur") && _u.barrier_max > 0) {
                var _bar_norm = clamp(_u.barrier_cur / _u.barrier_max, 0, 1);
                draw_set_color(make_color_rgb(10, 20, 30));
                draw_rectangle(_vx - _bar_w * 0.5, _by - 6 * zoom, _vx + _bar_w * 0.5, _by - 2 * zoom, false);
                draw_set_color(make_color_rgb(80, 220, 255));
                draw_rectangle(_vx - _bar_w * 0.5, _by - 6 * zoom, _vx - _bar_w * 0.5 + (_bar_w * _bar_norm), _by - 2 * zoom, false);
                draw_set_color(c_white);
                draw_text_transformed(_vx - 22 * zoom, _by - 14 * zoom, "SHIELD " + string(_u.barrier_cur), 0.50 * zoom, 0.50 * zoom, 0);
            }

            var _hp_col = (_u.team == "ALLIED") ? c_lime : make_color_rgb(255, 80, 80);
            draw_set_color(_hp_col);
            draw_rectangle(_vx - _bar_w * 0.5, _by, _vx - _bar_w * 0.5 + (_bar_w * _hp_norm), _by + _bar_h, false);

            draw_set_color(c_white);
            var _tag_col = (_u.team == "ALLIED") ? make_color_rgb(120, 220, 255) : make_color_rgb(255, 140, 140);
            if (_u.squad_type == "SUPER_ACE") _tag_col = make_color_rgb(255, 215, 80);
            if (variable_struct_exists(_u, "is_apex_boss") && _u.is_apex_boss) _tag_col = make_color_rgb(255, 60, 60);
            draw_set_color(_tag_col);

            var _header_tag = (variable_struct_exists(_u, "is_apex_boss") && _u.is_apex_boss) ? ("★ [APEX BOSS] OUROBOROS ★") : ((_u.squad_type == "SUPER_ACE") ? ("★ [ACE] " + string_copy(_u.callsign, 1, 8)) : ("[" + string(_u.squad_members_count) + "x] " + string_copy(_u.callsign, 1, 8)));
            draw_text_transformed(_vx - 22 * zoom, _by - 12 * zoom, _header_tag, 0.65 * zoom, 0.65 * zoom, 0);

            // Goal F: Pinned / Suppressed Overhead Badge
            if (variable_struct_exists(_u, "is_suppressed") && _u.is_suppressed) {
                draw_set_color(make_color_rgb(255, 215, 0));
                draw_text_transformed(_vx - 26 * zoom, _by - 23 * zoom, "[! PINNED !]", 0.62 * zoom, 0.62 * zoom, 0);
            }
            // Goal F: Elevation & Cover Overhead Badges
            if (_u.elev > 0) {
                draw_set_color(make_color_rgb(100, 240, 255));
                draw_text_transformed(_vx + 26 * zoom, _by - 12 * zoom, "^" + string(_u.elev), 0.60 * zoom, 0.60 * zoom, 0);
            }
            var _u_cov = grid_cover[_u.grid_c][_u.grid_r];
            if (_u_cov > 0) {
                draw_set_color((_u_cov == 2) ? make_color_rgb(140, 200, 255) : make_color_rgb(220, 200, 140));
                draw_text_transformed(_vx - 24 * zoom, _by + _bar_h + 3 * zoom, (_u_cov == 2) ? "[BASTION]" : "[RUBBLE]", 0.55 * zoom, 0.55 * zoom, 0);
            }

            // Gihren's Greed Stack Overhead Badge [x2]..[x6]
            var _stk = get_stack_at_tile(_u.grid_c, _u.grid_r, _u.team);
            if (array_length(_stk) > 1 && _stk[0] == _u) {
                var _stk_cnt = array_length(_stk);
                var _vg_c = 0;
                var _sp_c = 0;
                for (var si = 0; si < _stk_cnt; si++) {
                    if (_stk[si].formation_slot < 3) _vg_c++; else _sp_c++;
                }

                var _bdg_w = 60.0 * zoom;
                var _bdg_h = 13.0 * zoom;
                var _bdg_y = _by - 27.0 * zoom;

                draw_set_color(make_color_rgb(14, 20, 28));
                draw_rectangle(_vx - _bdg_w * 0.5, _bdg_y, _vx + _bdg_w * 0.5, _bdg_y + _bdg_h, false);

                var _bdg_border = (_u.team == "ALLIED") ? make_color_rgb(64, 224, 255) : make_color_rgb(255, 75, 75);
                draw_set_color(_bdg_border);
                draw_rectangle(_vx - _bdg_w * 0.5, _bdg_y, _vx + _bdg_w * 0.5, _bdg_y + _bdg_h, true);

                draw_set_halign(fa_center);
                var _bdg_txt = "[x" + string(_stk_cnt) + "] VG:" + string(_vg_c) + " SP:" + string(_sp_c);
                draw_set_color(_bdg_border);
                draw_text_transformed(_vx, _bdg_y + 2 * zoom, _bdg_txt, 0.55 * zoom, 0.55 * zoom, 0);
                draw_set_halign(fa_left);
            }
        }
    }

    // --- Render In-Flight Projectiles ---
    else if (_item.type == "PROJECTILE") {
        var _p = _item.proj;
        if (sprite_exists(_p.sprite)) {
            draw_sprite_ext(_p.sprite, 0, _p.cur_x + _sx, _p.cur_y + _sy, zoom, zoom, _p.angle, c_white, 1.0);
        }
    }

    // --- Render Combat Explosions & Sparks ---
    else if (_item.type == "FX") {
        var _fx = _item.fx;
        if (sprite_exists(_fx.sprite)) {
            draw_sprite_ext(_fx.sprite, floor(_fx.frame), _fx.x + _sx, _fx.y + _sy, _fx.scale, _fx.scale, 0, c_white, 1.0);
        }
    }
}

// =========================================================================
// =========================================================================
// 7B. FLOATING MARCH TELEMETRY CHIP & TARGETING BRACKETS
// =========================================================================
if (state == COMBAT_STATE.MOVE_MODE && selected_unit_idx >= 0 && selected_unit_idx < array_length(units)) {
    var _cur_sel = units[selected_unit_idx];
    if (hover_c >= 0 && hover_r >= 0 && (hover_c != _cur_sel.grid_c || hover_r != _cur_sel.grid_r)) {
        var _hover_vt = undefined;
        for (var m = 0; m < array_length(valid_move_tiles); m++) {
            if (valid_move_tiles[m].col == hover_c && valid_move_tiles[m].row == hover_r) {
                _hover_vt = valid_move_tiles[m];
                break;
            }
        }

        if (!is_undefined(_hover_vt)) {
            var _moving_cnt = 0;
            if (split_mode_active) {
                var _keys = variable_struct_get_names(split_selected_units);
                for (var k = 0; k < array_length(_keys); k++) {
                    if (variable_struct_get(split_selected_units, _keys[k])) _moving_cnt++;
                }
                if (_moving_cnt == 0) _moving_cnt = 1;
            } else {
                _moving_cnt = array_length(get_stack_at_tile(_cur_sel.grid_c, _cur_sel.grid_r, _cur_sel.team));
            }

            var _dx = iso_to_screen_x(hover_c, hover_r, grid_elev[hover_c][hover_r], cam_x, cam_y, zoom);
            var _dy = iso_to_screen_y(hover_c, hover_r, grid_elev[hover_c][hover_r], cam_x, cam_y, zoom);
            var _chip_w = 114.0 * zoom;
            var _chip_h = 16.0 * zoom;
            var _chip_y = _dy - (32.0 * zoom);

            draw_set_color(make_color_rgb(14, 22, 32));
            draw_rectangle(_dx - _chip_w * 0.5, _chip_y, _dx + _chip_w * 0.5, _chip_y + _chip_h, false);
            draw_set_color(make_color_rgb(64, 224, 255));
            draw_rectangle(_dx - _chip_w * 0.5, _chip_y, _dx + _chip_w * 0.5, _chip_y + _chip_h, true);
            draw_set_halign(fa_center);
            draw_set_color(make_color_rgb(64, 224, 255));
            draw_text_transformed(_dx, _chip_y + 3 * zoom, "MARCH AP: -" + string(_hover_vt.cost) + " | " + string(_moving_cnt) + " UNIT(S)", 0.55 * zoom, 0.55 * zoom, 0);
            draw_set_halign(fa_left);
        }
    }
}

if (state == COMBAT_STATE.TARGET_MODE && selected_unit_idx >= 0 && selected_unit_idx < array_length(units)) {
    if (hover_c >= 0 && hover_r >= 0) {
        var _tgt_stack = get_stack_at_tile(hover_c, hover_r, "ENEMY");
        if (array_length(_tgt_stack) > 0) {
            var _tgt_u = _tgt_stack[0];
            var _cur_u = units[selected_unit_idx];
            var _d = calculate_distance(_cur_u.grid_c, _cur_u.grid_r, hover_c, hover_r);
            var _friendly_stack = get_stack_at_tile(_cur_u.grid_c, _cur_u.grid_r, _cur_u.team);
            var _fp = get_stack_max_firepower(_friendly_stack, _tgt_u, _d);

            var _tx = iso_to_screen_x(hover_c, hover_r, _tgt_u.elev, cam_x, cam_y, zoom);
            var _ty = iso_to_screen_y(hover_c, hover_r, _tgt_u.elev, cam_x, cam_y, zoom);
            var _cy_mid = _ty - 24 * zoom;

            // 4 Corner Targeting Brackets
            var _bw = 36 * zoom;
            var _bh = 40 * zoom;
            var _b_pulse = sin(current_time * 0.015) * 3 * zoom;
            var _arm = 10 * zoom;

            var _left = _tx - _bw - _b_pulse;
            var _right = _tx + _bw + _b_pulse;
            var _top = _cy_mid - _bh;
            var _bot = _cy_mid + _bh;

            draw_set_color(make_color_rgb(255, 60, 60));
            // Top-Left corner
            draw_line_width(_left, _top, _left + _arm, _top, 2.5 * zoom);
            draw_line_width(_left, _top, _left, _top + _arm, 2.5 * zoom);
            // Top-Right corner
            draw_line_width(_right, _top, _right - _arm, _top, 2.5 * zoom);
            draw_line_width(_right, _top, _right, _top + _arm, 2.5 * zoom);
            // Bottom-Left corner
            draw_line_width(_left, _bot, _left + _arm, _bot, 2.5 * zoom);
            draw_line_width(_left, _bot, _left, _bot - _arm, 2.5 * zoom);
            // Bottom-Right corner
            draw_line_width(_right, _bot, _right - _arm, _bot, 2.5 * zoom);
            draw_line_width(_right, _bot, _right, _bot - _arm, 2.5 * zoom);

            // Center Reticle
            draw_set_color(make_color_rgb(255, 215, 60));
            draw_circle(_tx, _cy_mid, 2.5 * zoom, false);

            // Telemetry Salvo Badge
            var _hdr_str = (_fp.unit_count > 0) ? ("▲ [LOCK] SALVO: " + string(_fp.unit_count) + "/" + string(array_length(_friendly_stack)) + " UNITS") : "▲ [OUT OF RANGE / AP]";
            var _col_hdr = (_fp.unit_count > 0) ? make_color_rgb(255, 215, 60) : make_color_rgb(180, 180, 180);
            var _tw = 110.0 * zoom;
            var _th = 15.0 * zoom;
            var _tb_y = _top - 18 * zoom;

            draw_set_color(make_color_rgb(15, 20, 28));
            draw_rectangle(_tx - _tw * 0.5, _tb_y, _tx + _tw * 0.5, _tb_y + _th, false);
            draw_set_color(_col_hdr);
            draw_rectangle(_tx - _tw * 0.5, _tb_y, _tx + _tw * 0.5, _tb_y + _th, true);
            draw_set_halign(fa_center);
            draw_text_transformed(_tx, _tb_y + 3 * zoom, _hdr_str, 0.55 * zoom, 0.55 * zoom, 0);
            draw_set_halign(fa_left);
        }
    }
}

// 8. PROCEDURAL NEMESIS DROP-POD AMBUSH WORLD RENDERING (Document 19)
// =========================================================================
if (state == COMBAT_STATE.NEMESIS_INCURSION || incursion_data.impact_fx_played) {
    var _tc = incursion_data.target_c;
    var _tr = incursion_data.target_r;
    var _te = grid_elev[_tc][_tr];
    var _tx = iso_to_screen_x(_tc, _tr, _te, cam_x + _sx, cam_y + _sy, zoom);
    var _ty = iso_to_screen_y(_tc, _tr, _te, cam_x + _sx, cam_y + _sy, zoom);

    // 1. Landing Target Reticle & Blast Ring
    if (state == COMBAT_STATE.NEMESIS_INCURSION && incursion_data.pod_altitude > 0) {
        var _pulse = 0.5 + 0.5 * sin(current_time * 0.015);
        draw_set_color(make_color_rgb(255, 60, 40));
        draw_set_alpha(0.7 * _pulse);
        draw_ellipse(_tx - 32 * zoom, _ty - 16 * zoom, _tx + 32 * zoom, _ty + 16 * zoom, true);
        draw_ellipse(_tx - 16 * zoom, _ty - 8 * zoom, _tx + 16 * zoom, _ty + 8 * zoom, true);
        draw_line(_tx - 40 * zoom, _ty, _tx + 40 * zoom, _ty);
        draw_line(_tx, _ty - 20 * zoom, _tx, _ty + 20 * zoom);
        draw_set_alpha(1.0);

        // 2. Descending Atmospheric Drop-Pod Capsule & Plasma Streak
        var _pod_y = _ty - incursion_data.pod_altitude * zoom;

        // Plasma trail / fire streak extending upward
        draw_set_color(make_color_rgb(255, 120, 30));
        draw_line_width(_tx, _pod_y, _tx - 4 * zoom, _pod_y - 120 * zoom, 4.0 * zoom);
        draw_set_color(make_color_rgb(255, 230, 100));
        draw_line_width(_tx, _pod_y, _tx - 2 * zoom, _pod_y - 80 * zoom, 2.0 * zoom);

        // Armored Drop-Pod Cone (Titanium Capsule with Ablative Heat Shield)
        draw_set_color(make_color_rgb(45, 50, 60)); // Dark hull
        draw_triangle(_tx - 14 * zoom, _pod_y - 28 * zoom, _tx + 14 * zoom, _pod_y - 28 * zoom, _tx, _pod_y, false);
        draw_set_color(make_color_rgb(255, 90, 40)); // Glowing ablative nose
        draw_triangle(_tx - 6 * zoom, _pod_y - 10 * zoom, _tx + 6 * zoom, _pod_y - 10 * zoom, _tx, _pod_y, false);
        draw_set_color(make_color_rgb(200, 210, 225));
        draw_triangle(_tx - 14 * zoom, _pod_y - 28 * zoom, _tx + 14 * zoom, _pod_y - 28 * zoom, _tx, _pod_y, true);
    }

    // 3. Persistent Ground Scorch & Detonation Crater
    if (incursion_data.impact_fx_played) {
        draw_set_color(make_color_rgb(25, 20, 20));
        draw_set_alpha(0.65);
        draw_ellipse(_tx - 28 * zoom, _ty - 14 * zoom, _tx + 28 * zoom, _ty + 14 * zoom, false);
        draw_set_color(make_color_rgb(180, 70, 30));
        draw_ellipse(_tx - 18 * zoom, _ty - 9 * zoom, _tx + 18 * zoom, _ty + 9 * zoom, true);
        draw_set_alpha(1.0);
    }
}
