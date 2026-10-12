/// @description scr_combat_projectiles
// Real-Time Physical Projectile Flight Engine & Visual Trajectories
// Strictly implements docs/17_grand_scale_isometric_combat_system.md

function create_projectile(_type, _x1, _y1, _z1, _x2, _y2, _z2, _hit_cb) {
    var _duration = 22;
    var _z_peak = 20.0;
    var _sprite = spr_proj_cannon_120mm;
    var _trail_type = "smoke";

    if (_type == "KINETIC_CANNON") {
        _sprite = spr_proj_cannon_120mm;
        _duration = 20;
        _z_peak = 24.0;
        _trail_type = "smoke";
    } else if (_type == "ROTARY_VULCAN") {
        _sprite = spr_proj_vulcan;
        _duration = 14;
        _z_peak = 6.0;
        _trail_type = "tracer";
    } else if (_type == "BEAM_PULSE") {
        _sprite = spr_proj_beam;
        _duration = 10;
        _z_peak = 0.0;
        _trail_type = "energy";
    } else if (_type == "MICRO_MISSILE") {
        _sprite = spr_proj_missile;
        _duration = 28;
        _z_peak = 45.0;
        _trail_type = "missile_plume";
    } else if (_type == "RAILGUN_SLUG") {
        _sprite = spr_proj_railgun;
        _duration = 8;
        _z_peak = 2.0;
        _trail_type = "plasma";
    }

    var _angle = point_direction(_x1, _y1, _x2, _y2);

    return {
        type: _type,
        sprite: _sprite,
        x1: _x1,
        y1: _y1,
        z1: _z1,
        x2: _x2,
        y2: _y2,
        z2: _z2,
        cur_x: _x1,
        cur_y: _y1,
        cur_z: _z1,
        angle: _angle,
        t: 0.0,
        step_rate: 1.0 / max(1.0, _duration),
        z_peak: _z_peak,
        trail_type: _trail_type,
        on_hit: _hit_cb,
        is_finished: false,
        particles: []
    };
}
