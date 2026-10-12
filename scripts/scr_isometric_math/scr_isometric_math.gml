/// @description scr_isometric_math
// 2:1 Isometric Coordinate Conversion, Screen Unprojection & Facing Calculation
// Strictly implements docs/17_grand_scale_isometric_combat_system.md

function iso_to_screen_x(_col, _row, _elev, _cam_x, _cam_y, _zoom) {
    var _tile_w = 64.0;
    return floor(((_col - _row) * (_tile_w * 0.5)) * _zoom + _cam_x);
}

function iso_to_screen_y(_col, _row, _elev, _cam_x, _cam_y, _zoom) {
    var _tile_h = 32.0;
    var _elev_h = 16.0;
    return floor((((_col + _row) * (_tile_h * 0.5)) - (_elev * _elev_h)) * _zoom + _cam_y);
}

function screen_to_iso_col(_sx, _sy, _cam_x, _cam_y, _zoom) {
    var _tile_w = 64.0;
    var _tile_h = 32.0;
    var _adj_x = (_sx - _cam_x) / max(0.1, _zoom);
    var _adj_y = (_sy - _cam_y) / max(0.1, _zoom);
    var _c = (_adj_x / (_tile_w * 0.5) + _adj_y / (_tile_h * 0.5)) * 0.5;
    return floor(_c);
}

function screen_to_iso_row(_sx, _sy, _cam_x, _cam_y, _zoom) {
    var _tile_w = 64.0;
    var _tile_h = 32.0;
    var _adj_x = (_sx - _cam_x) / max(0.1, _zoom);
    var _adj_y = (_sy - _cam_y) / max(0.1, _zoom);
    var _r = (_adj_y / (_tile_h * 0.5) - _adj_x / (_tile_w * 0.5)) * 0.5;
    return floor(_r);
}

function iso_get_facing(_from_c, _from_r, _to_c, _to_r) {
    var _dc = _to_c - _from_c;
    var _dr = _to_r - _from_r;
    if (abs(_dc) >= abs(_dr)) {
        return (_dc >= 0) ? 0 : 3; // 0 = SE (Front-Right), 3 = NW (Back-Left)
    } else {
        return (_dr >= 0) ? 1 : 2; // 1 = SW (Front-Left), 2 = NE (Back-Right)
    }
}

function iso_is_back_facing(_dir) {
    return (_dir == 2 || _dir == 3); // 2 = NE, 3 = NW
}

function iso_distance(_c1, _r1, _c2, _r2) {
    return abs(_c1 - _c2) + abs(_r1 - _r2);
}
