with open('objects/obj_HQTerminal/Draw_64.gml', 'r', encoding='utf-8') as f:
    s = f.read()

# 1. Situation Briefing (Page 0) doctrines
s = s.replace(
    'draw_text(_bx + 16, _fy + 18, "Doctrine: Heavy artillery, 120mm ordnance, dense composite armor plates (Ironclad series).");',
    'draw_text_ext(_bx + 16, _fy + 18, "Doctrine: Heavy artillery, 120mm ordnance, dense composite armor plates (Ironclad series).", 14, _col_w - 32);'
)
s = s.replace(
    'draw_text(_bx + 16, _fy + 18, "Doctrine: Vernier thrusters, beam rifles, particle beam sabers (Aether interceptors).");',
    'draw_text_ext(_bx + 16, _fy + 18, "Doctrine: Vernier thrusters, beam rifles, particle beam sabers (Aether interceptors).", 14, _col_w - 32);'
)
s = s.replace(
    'draw_text(_bx + 16, _fy + 18, "Doctrine: Slag salvagers, heavy rotary flak, grappling claws, harpoon tethers (Hyena raiders).");',
    'draw_text_ext(_bx + 16, _fy + 18, "Doctrine: Slag salvagers, heavy rotary flak, grappling claws, harpoon tethers (Hyena raiders).", 14, _col_w - 32);'
)
s = s.replace(
    'draw_text(_bx + 16, _fy + 18, "Doctrine: Cybernetic neural pilots, plasma blasters, tachyon optics, hostile takeovers.");',
    'draw_text_ext(_bx + 16, _fy + 18, "Doctrine: Cybernetic neural pilots, plasma blasters, tachyon optics, hostile takeovers.", 14, _col_w - 32);'
)

# Right Column capabilities
s = s.replace(
    'draw_text(_bx + _col_w + 40, _ry, "* METALLURGICAL SINTERING (Thermal Crucible)");\n        draw_set_color(make_color_rgb(170, 195, 220));\n        draw_text(_bx + _col_w + 40, _ry + 18, "Combine raw ores, flux, and tritium under extreme pressure to forge Vanguard Plating.");',
    'draw_text(_bx + _col_w + 32, _ry, "* METALLURGICAL SINTERING (Crucible)");\n        draw_set_color(make_color_rgb(170, 195, 220));\n        draw_text_ext(_bx + _col_w + 32, _ry + 18, "Combine raw ores, flux, and tritium under extreme pressure to forge Vanguard Plating.", 14, _col_w - 48);'
)
s = s.replace(
    'draw_text(_bx + _col_w + 40, _ry, "* MODULAR CAD MECHA ASSEMBLY (Factory Floor)");\n        draw_set_color(make_color_rgb(170, 195, 220));\n        draw_text(_bx + _col_w + 40, _ry + 18, "Fit Heads, Torsos, Arms, Legs, and Weapons across Biped, Hover, Tread, & Aero frames.");',
    'draw_text(_bx + _col_w + 32, _ry, "* MODULAR CAD MECHA ASSEMBLY (Factory)");\n        draw_set_color(make_color_rgb(170, 195, 220));\n        draw_text_ext(_bx + _col_w + 32, _ry + 18, "Fit Heads, Torsos, Arms, Legs, and Weapons across Biped, Hover, Tread, & Aero frames.", 14, _col_w - 48);'
)
s = s.replace(
    'draw_text(_bx + _col_w + 40, _ry, "* CORPORATE DEFENSE CONTRACTS & COMPETITIONS");\n        draw_set_color(make_color_rgb(170, 195, 220));\n        draw_text(_bx + _col_w + 40, _ry + 18, "Enter 4-phase corporate design flyoffs to secure lucrative multi-million credit production lines.");',
    'draw_text(_bx + _col_w + 32, _ry, "* CORPORATE DEFENSE CONTRACTS & FLYOFFS");\n        draw_set_color(make_color_rgb(170, 195, 220));\n        draw_text_ext(_bx + _col_w + 32, _ry + 18, "Enter 4-phase corporate design flyoffs to secure lucrative multi-million credit production lines.", 14, _col_w - 48);'
)
s = s.replace(
    'draw_text(_bx + _col_w + 40, _ry, "* ISOMETRIC TACTICAL COMBAT (24 Map Theaters)");\n        draw_set_color(make_color_rgb(170, 195, 220));\n        draw_text(_bx + _col_w + 40, _ry + 18, "Deploy dual platoons with aimed shot precision; repel rival ace drop-pod incursions.");',
    'draw_text(_bx + _col_w + 32, _ry, "* ISOMETRIC TACTICAL COMBAT (24 Theaters)");\n        draw_set_color(make_color_rgb(170, 195, 220));\n        draw_text_ext(_bx + _col_w + 32, _ry + 18, "Deploy dual platoons with aimed shot precision; repel rival ace drop-pod incursions.", 14, _col_w - 48);'
)

# Page 1 Commander trait & bio
s = s.replace(
    'draw_text(_card_x + 16, _py + _p_size + 70, _opt.trait_desc);',
    'draw_text_ext(_card_x + 16, _py + _p_size + 70, _opt.trait_desc, 14, _card_w - 32);'
)
s = s.replace(
    'draw_text(_cx + 16, _bio_y + 28, _cur_choice_data.bio);',
    'draw_text_ext(_cx + 16, _bio_y + 28, _cur_choice_data.bio, 16, _cw - 32);'
)

# Crucible preview
s = s.replace(
    'draw_text(_met_x + 150, _bw_y + 72, "Ratio: W:" + string(crucible_batch.mat_tungsten) + " C:" + string(crucible_batch.mat_silica_carb) + " Tr:" + string(crucible_batch.mat_tritium) + " Fx:" + string(crucible_batch.mat_syn_flux) + " (Total: " + string(_batch_tot) + ") | Hex: " + _cur_hex);',
    'draw_text_ext(_met_x + 150, _bw_y + 72, "Ratio: W:" + string(crucible_batch.mat_tungsten) + " C:" + string(crucible_batch.mat_silica_carb) + " Tr:" + string(crucible_batch.mat_tritium) + " Fx:" + string(crucible_batch.mat_syn_flux) + " (Total: " + string(_batch_tot) + ") | Hex: " + _cur_hex, 16, _met_w - 165);'
)
s = s.replace(
    'draw_text(_met_x + 150, _bw_y + 92, "PROJECTED YIELD: 1x Ingot (" + string(_tgt_purity) + "% Purity) // " + _tgt_bonus);',
    'draw_text_ext(_met_x + 150, _bw_y + 92, "PROJECTED YIELD: 1x Ingot (" + string(_tgt_purity) + "% Purity) // " + _tgt_bonus, 16, _met_w - 165);'
)

with open('objects/obj_HQTerminal/Draw_64.gml', 'w', encoding='utf-8') as f:
    f.write(s)
print('Applied text wrapping fixes to obj_HQTerminal/Draw_64.gml')
