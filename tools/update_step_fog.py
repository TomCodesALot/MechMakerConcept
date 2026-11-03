with open("objects/obj_HQTerminal/Step_0.gml", "r") as f:
    code = f.read()

old_block = '''    // Press G to toggle Hex Grid mesh
    if (keyboard_check_pressed(ord("G"))) {
        hex_grid_enabled = !hex_grid_enabled;
        scr_audio_play_ui("click");
    }
}'''

new_block = '''    // Press G to toggle Hex Grid mesh
    if (keyboard_check_pressed(ord("G"))) {
        hex_grid_enabled = !hex_grid_enabled;
        scr_audio_play_ui("click");
    }

    // Press F to toggle Prometheus Flux Fog of War
    if (keyboard_check_pressed(ord("F"))) {
        fog_of_war_enabled = !fog_of_war_enabled;
        scr_audio_play_ui("click");
    }
}'''

assert old_block in code, "old_block not found in Step_0.gml"
code = code.replace(old_block, new_block)

with open("objects/obj_HQTerminal/Step_0.gml", "w") as f:
    f.write(code)

print("Updated Step_0.gml successfully!")
