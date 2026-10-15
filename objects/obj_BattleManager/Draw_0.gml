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

        draw_set_color(make_color_rgb(45, 58, 72));
        draw_rectangle(_bx - _cw, _by - _ch, _bx + _cw, _by, false);
        draw_set_color(make_color_rgb(90, 115, 140));
        draw_rectangle(_bx - _cw, _by - _ch, _bx + _cw, _by, true);

        draw_set_color(c_white);
        draw_text_transformed(_bx - 18 * zoom, _by - 18 * zoom, "COVER", 0.65 * zoom, 0.65 * zoom, 0);
    }

    // --- Render Mobile Suits ---
    else if (_item.type == UNIT) {
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

        // Dual Platoon Structure: 3-Mech Platoon vs 1-Mech Super Ace
        if (_u.squad_type == "PLATOON_3") {
            // Render Staggered Wingman 1 (Left Wing)
            if (_u.squad_members_count >= 2 && !_u.is_destroyed && sprite_exists(_spr)) {
                var _w1_x = _vx - (18.0 * zoom * _facing_sign);
                var _w1_y = _vy - (12.0 * zoom);
                draw_set_color(c_black);
                draw_set_alpha(0.30);
                draw_ellipse(_w1_x - 18 * zoom, _w1_y - 7 * zoom, _w1_x + 18 * zoom, _w1_y + 7 * zoom, false);
                draw_set_alpha(1.0);
                draw_sprite_ext(_spr, floor(_u.anim_frame), _w1_x, _w1_y, _xscale * 0.90, _yscale * 0.90, 0, _u.image_blend, 0.90);
            }

            // Render Staggered Wingman 2 (Right Wing)
            if (_u.squad_members_count >= 3 && !_u.is_destroyed && sprite_exists(_spr)) {
                var _w2_x = _vx - (18.0 * zoom * _facing_sign);
                var _w2_y = _vy + (12.0 * zoom);
                draw_set_color(c_black);
                draw_set_alpha(0.30);
                draw_ellipse(_w2_x - 18 * zoom, _w2_y - 7 * zoom, _w2_x + 18 * zoom, _w2_y + 7 * zoom, false);
                draw_set_alpha(1.0);
                draw_sprite_ext(_spr, floor(_u.anim_frame), _w2_x, _w2_y, _xscale * 0.90, _yscale * 0.90, 0, _u.image_blend, 0.90);
            }

            // Lead Mech Drop Shadow
            draw_set_color(c_black);
            draw_set_alpha(0.40);
            draw_ellipse(_vx - 24 * zoom, _vy - 10 * zoom, _vx + 24 * zoom, _vy + 10 * zoom, false);
            draw_set_alpha(1.0);

            // Lead Mech Sprite
            if (sprite_exists(_spr)) {
                draw_sprite_ext(_spr, floor(_u.anim_frame), _vx, _vy, _xscale, _yscale, 0, _u.image_blend, _alpha);
            }
        } else {
            // Super Ace (1 Unit Prototype) with 1.15 Scale & Evasion Afterimages
            var _ace_scale = 1.15;

            // Motion Blur Evasion Afterimages
            if (!_u.is_destroyed && sprite_exists(_spr)) {
                var _after_x = _vx - (4.0 * zoom * _facing_sign);
                var _after_y = _vy - (2.0 * zoom);
                draw_sprite_ext(_spr, floor(_u.anim_frame), _after_x, _after_y, _xscale * _ace_scale, _yscale * _ace_scale, 0, make_color_rgb(100, 220, 255), 0.25);
            }

            // Drop Shadow
            draw_set_color(c_black);
            draw_set_alpha(0.45);
            draw_ellipse(_vx - 26 * zoom, _vy - 11 * zoom, _vx + 26 * zoom, _vy + 11 * zoom, false);
            draw_set_alpha(1.0);

            // Lead Ace Sprite
            if (sprite_exists(_spr)) {
                draw_sprite_ext(_spr, floor(_u.anim_frame), _vx, _vy, _xscale * _ace_scale, _yscale * _ace_scale, 0, _u.image_blend, _alpha);
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

            var _hp_col = (_u.team == "ALLIED") ? c_lime : make_color_rgb(255, 80, 80);
            draw_set_color(_hp_col);
            draw_rectangle(_vx - _bar_w * 0.5, _by, _vx - _bar_w * 0.5 + (_bar_w * _hp_norm), _by + _bar_h, false);

            draw_set_color(c_white);
            var _tag_col = (_u.team == "ALLIED") ? make_color_rgb(120, 220, 255) : make_color_rgb(255, 140, 140);
            if (_u.squad_type == "SUPER_ACE") _tag_col = make_color_rgb(255, 215, 80);
            draw_set_color(_tag_col);

            var _header_tag = (_u.squad_type == "SUPER_ACE") ? ("★ [ACE] " + string_copy(_u.callsign, 1, 8)) : ("[" + string(_u.squad_members_count) + "x] " + string_copy(_u.callsign, 1, 8));
            draw_text_transformed(_vx - 22 * zoom, _by - 12 * zoom, _header_tag, 0.65 * zoom, 0.65 * zoom, 0);
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
