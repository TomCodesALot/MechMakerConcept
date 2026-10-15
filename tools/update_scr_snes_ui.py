with open('scripts/scr_snes_ui/scr_snes_ui.gml', 'r') as f:
    text = f.read()

stamp_func = '''
/// @function scr_draw_snes_trial_stamp(_x, _y, _stamp_idx)
/// @description Draws a stamped 16-bit evaluation badge (Grade S, A, Conditional, Rejected, Modernized, Tooling).
function scr_draw_snes_trial_stamp(_x, _y, _stamp_idx) {
    if (sprite_exists(spr_snes_trial_stamps)) {
        draw_sprite(spr_snes_trial_stamps, clamp(_stamp_idx, 0, 5), _x, _y);
    } else {
        draw_set_color(make_color_rgb(14, 24, 36));
        draw_rectangle(_x, _y, _x + 84, _y + 26, false);
        draw_set_color(make_color_rgb(100, 220, 255));
        draw_rectangle(_x, _y, _x + 84, _y + 26, true);
        draw_text(_x + 6, _y + 6, "STAMP #" + string(_stamp_idx));
    }
}
'''

if "scr_draw_snes_trial_stamp" not in text:
    text += stamp_func
    with open('scripts/scr_snes_ui/scr_snes_ui.gml', 'w') as f:
        f.write(text)
    print("Added scr_draw_snes_trial_stamp to scr_snes_ui.gml")
else:
    print("scr_draw_snes_trial_stamp already exists")
