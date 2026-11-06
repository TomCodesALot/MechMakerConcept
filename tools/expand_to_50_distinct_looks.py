#!/usr/bin/env python3
"""
Expand Sintered Material Alloys to 10 distinct crucible recipes,
achieving exactly 50 distinct visual mobile suit looks (5 PMC Chassis x 10 Alloys)
in obj_DebugManager.
"""
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
create_path = os.path.join(PROJECT_ROOT, "objects", "obj_DebugManager", "Create_0.gml")
draw_path = os.path.join(PROJECT_ROOT, "objects", "obj_DebugManager", "Draw_64.gml")

# --- 1. Update Create_0.gml ---
with open(create_path, "r") as f:
    create_src = f.read()

old_alloys_block = """builder_alloys = [
    "alloy_vanguard_comp",
    "alloy_hyperion_matrix",
    "alloy_aerosteel_flux",
    "alloy_adamantine_carbide",
    "alloy_chobham_reactive",
    "alloy_tachyon_superalloy"
];
builder_alloy_names = [
    "Vanguard Composite (Standard Kinetic Armor)",
    "Hyperion Matrix (+25% Energy Gen, +20% Beam Res)",
    "Aerosteel Flux (+35% Boost Speed, -20% Mass)",
    "Adamantine Heavy (+40% Armor HP, Sintered Carbide)",
    "Chobham-X Reactive (+50% Explosive/Missile Res)",
    "Tachyon Superalloy (Singularity Spec, +25% All Stats)"
];
builder_alloy_deltas = [
    { armor_mult: 1.0, mass_mult: 1.0, speed_bonus: 0, desc: "Matte gunmetal olive-drab with carbon ballistic trim.", tint_color: make_color_rgb(230, 240, 230), glow_color: make_color_rgb(255, 255, 255) },
    { armor_mult: 0.9, mass_mult: 0.85, speed_bonus: 15, desc: "Deep cobalt navy with pulsing cyan superconducting lines.", tint_color: make_color_rgb(180, 220, 255), glow_color: make_color_rgb(0, 240, 255) },
    { armor_mult: 0.8, mass_mult: 0.75, speed_bonus: 30, desc: "Polished aerospace satin-white with gold vernier cowlings.", tint_color: make_color_rgb(255, 250, 240), glow_color: make_color_rgb(255, 220, 80) },
    { armor_mult: 1.45, mass_mult: 1.35, speed_bonus: -15, desc: "Blackened charred tungsten slab with industrial bronze joints.", tint_color: make_color_rgb(165, 165, 175), glow_color: make_color_rgb(255, 140, 40) },
    { armor_mult: 1.2, mass_mult: 1.1, speed_bonus: -5, desc: "Desert sand composite tiles absorbing shaped charges.", tint_color: make_color_rgb(240, 225, 195), glow_color: make_color_rgb(255, 200, 100) },
    { armor_mult: 1.35, mass_mult: 0.85, speed_bonus: 25, desc: "Midnight violet lattice with pulsating Cherenkov radiation.", tint_color: make_color_rgb(225, 195, 255), glow_color: make_color_rgb(200, 100, 255) }
];"""

new_alloys_block = """builder_alloys = [
    "alloy_vanguard_comp",
    "alloy_hyperion_matrix",
    "alloy_aerosteel_flux",
    "alloy_adamantine_carbide",
    "alloy_chobham_reactive",
    "alloy_scrapper_slag",
    "alloy_carbon_nanoweave",
    "alloy_solar_crimson",
    "alloy_depleted_actinide",
    "alloy_tachyon_superalloy"
];
builder_alloy_names = [
    "Vanguard Tungsten Composite (Standard Mil-Spec)",
    "Hyperion Superconducting Matrix (+25% Energy Gen)",
    "Aerosteel Vector Flux (+35% Speed, -25% Mass)",
    "Adamantine Sintered Carbide (+45% Armor HP)",
    "Chobham-X Reactive Tiles (+50% Explosive Res)",
    "Crude Asteroid Slag (Scavenger Salvage Plating)",
    "Carbon Nanoweave Lattice (Stealth Radar-Absorbent)",
    "Solar-Forged Crimson Crucible (Extreme Thermal Disp)",
    "Depleted Actinide Heavy Slab (Superheavy Siege & EMP)",
    "Tachyon Singularity Superalloy (+35% All Stats)"
];
builder_alloy_deltas = [
    { armor_mult: 1.0,  mass_mult: 1.0,  speed_bonus: 0,   desc: "Matte gunmetal olive-drab with carbon ballistic trim.", tint_color: make_color_rgb(220, 235, 220), glow_color: make_color_rgb(255, 255, 255) },
    { armor_mult: 0.90, mass_mult: 0.85, speed_bonus: 15,  desc: "Deep cobalt navy with pulsing cyan superconducting traces.", tint_color: make_color_rgb(175, 215, 255), glow_color: make_color_rgb(0, 240, 255) },
    { armor_mult: 0.80, mass_mult: 0.75, speed_bonus: 30,  desc: "Satin aerospace chrome-white with gold vernier cowlings.", tint_color: make_color_rgb(255, 250, 240), glow_color: make_color_rgb(255, 220, 80) },
    { armor_mult: 1.45, mass_mult: 1.35, speed_bonus: -15, desc: "Blackened charred tungsten slab with industrial bronze joints.", tint_color: make_color_rgb(155, 155, 165), glow_color: make_color_rgb(255, 140, 40) },
    { armor_mult: 1.20, mass_mult: 1.10, speed_bonus: -5,  desc: "Desert sand composite tiles absorbing shaped charges.", tint_color: make_color_rgb(240, 225, 190), glow_color: make_color_rgb(255, 200, 100) },
    { armor_mult: 1.10, mass_mult: 1.25, speed_bonus: -10, desc: "Pitted oxidized iron, raw welding burns, and rust orange trim.", tint_color: make_color_rgb(215, 180, 160), glow_color: make_color_rgb(255, 120, 40) },
    { armor_mult: 0.85, mass_mult: 0.70, speed_bonus: 20,  desc: "Charcoal matte graphite with carbon-fiber weave sheen.", tint_color: make_color_rgb(170, 175, 185), glow_color: make_color_rgb(120, 220, 255) },
    { armor_mult: 1.15, mass_mult: 1.05, speed_bonus: 5,   desc: "Burnt anodized copper and deep crimson red with heat fins.", tint_color: make_color_rgb(255, 175, 170), glow_color: make_color_rgb(255, 60, 60) },
    { armor_mult: 1.55, mass_mult: 1.45, speed_bonus: -20, desc: "Toxic lead-slate gray with hazardous radioactive amber trim.", tint_color: make_color_rgb(180, 205, 180), glow_color: make_color_rgb(200, 255, 80) },
    { armor_mult: 1.35, mass_mult: 0.85, speed_bonus: 25,  desc: "Midnight iridescent violet with pulsating Cherenkov radiation.", tint_color: make_color_rgb(225, 195, 255), glow_color: make_color_rgb(200, 100, 255) }
];"""

assert old_alloys_block in create_src, "Could not find old_alloys_block in Create_0.gml"
create_src = create_src.replace(old_alloys_block, new_alloys_block)

with open(create_path, "w") as f:
    f.write(create_src)
print("Create_0.gml updated with 10 Sintered Material Alloys.")

# --- 2. Update Draw_64.gml Subtab 1 into a 2x5 Grid ---
with open(draw_path, "r") as f:
    draw_src = f.read()

old_subtab1_draw = """    // =====================================================================
    // SUBTAB 1: SINTERED ALLOY METALLURGY
    // =====================================================================
    else if (builder_subtab == 1) {
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 20, _deck_y, "SINTERED ALLOY PLATING (MOLECULAR CRUCIBLE):");

        var _al_y = _deck_y + 24;
        for (var a = 0; a < array_length(builder_alloys); a++) {
            var _ay_pos = _al_y + (a * 76);
            var _is_cur_al = (builder_alloy_idx == a);
            var _al_hov = (_mx >= _eng_x + 18 && _mx <= _eng_x + _eng_w - 18 && _my >= _ay_pos && _my <= _ay_pos + 70);

            if (_al_hov && _click) {
                builder_alloy_idx = a;
                scr_audio_play_ui("click");
            }

            draw_set_color(_is_cur_al ? make_color_rgb(24, 44, 70) : (_al_hov ? make_color_rgb(18, 30, 48) : make_color_rgb(12, 18, 28)));
            draw_rectangle(_eng_x + 18, _ay_pos, _eng_x + _eng_w - 18, _ay_pos + 68, false);
            draw_set_color(_is_cur_al ? make_color_rgb(0, 240, 255) : make_color_rgb(40, 65, 95));
            draw_rectangle(_eng_x + 18, _ay_pos, _eng_x + _eng_w - 18, _ay_pos + 68, true);

            // Alloy Name
            draw_set_color(_is_cur_al ? make_color_rgb(255, 220, 80) : c_white);
            draw_text(_eng_x + 28, _ay_pos + 8, (_is_cur_al ? "> " : "") + builder_alloy_names[a]);

            // Alloy Deltas
            var _ad = builder_alloy_deltas[a];
            draw_set_color(make_color_rgb(160, 190, 220));
            draw_text(_eng_x + 28, _ay_pos + 28, "Armor: " + string(floor(_ad.armor_mult * 100)) + "% | Mass: " + string(floor(_ad.mass_mult * 100)) + "% | Speed: " + (_ad.speed_bonus >= 0 ? "+" : "") + string(_ad.speed_bonus) + " km/h");

            draw_set_color(make_color_rgb(255, 180, 80));
            draw_text(_eng_x + 28, _ay_pos + 46, _ad.desc);
        }
    }"""

new_subtab1_draw = """    // =====================================================================
    // SUBTAB 1: SINTERED ALLOY METALLURGY (10 RECIPES / 50 LOOKS)
    // =====================================================================
    else if (builder_subtab == 1) {
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(_eng_x + 20, _deck_y, "SINTERED ALLOY METALLURGY & VISUAL FINISH (10 RECIPES):");

        var _grid_w = 264;
        var _card_h = 100;
        var _start_y = _deck_y + 24;

        for (var a = 0; a < array_length(builder_alloys); a++) {
            var _col = floor(a / 5);
            var _row = a % 5;
            var _ax = _eng_x + 16 + (_col * (_grid_w + 8));
            var _ay = _start_y + (_row * (_card_h + 8));

            var _is_cur_al = (builder_alloy_idx == a);
            var _al_hov = (_mx >= _ax && _mx <= _ax + _grid_w && _my >= _ay && _my <= _ay + _card_h);

            if (_al_hov && _click) {
                builder_alloy_idx = a;
                scr_audio_play_ui("click");
            }

            var _ad = builder_alloy_deltas[a];

            // Card Background & Border
            draw_set_color(_is_cur_al ? make_color_rgb(26, 48, 76) : (_al_hov ? make_color_rgb(18, 30, 48) : make_color_rgb(12, 18, 28)));
            draw_rectangle(_ax, _ay, _ax + _grid_w, _ay + _card_h, false);
            draw_set_color(_is_cur_al ? make_color_rgb(0, 240, 255) : make_color_rgb(45, 68, 98));
            draw_rectangle(_ax, _ay, _ax + _grid_w, _ay + _card_h, true);

            // Color Swatch Indicator (14x14)
            draw_set_color(_ad.tint_color);
            draw_rectangle(_ax + _grid_w - 22, _ay + 8, _ax + _grid_w - 8, _ay + 22, false);
            draw_set_color(_ad.glow_color);
            draw_rectangle(_ax + _grid_w - 22, _ay + 8, _ax + _grid_w - 8, _ay + 22, true);

            // Alloy Name
            draw_set_color(_is_cur_al ? make_color_rgb(255, 220, 80) : c_white);
            var _short_name = string_copy(builder_alloy_names[a], 1, 26);
            draw_text(_ax + 8, _ay + 8, (_is_cur_al ? "> " : "") + _short_name);

            // Stat Multipliers
            draw_set_color(make_color_rgb(150, 190, 230));
            draw_text(_ax + 8, _ay + 28, "Arm: " + string(floor(_ad.armor_mult * 100)) + "% | Mass: " + string(floor(_ad.mass_mult * 100)) + "% | Spd: " + (_ad.speed_bonus >= 0 ? "+" : "") + string(_ad.speed_bonus));

            // Surface Finish Lore
            draw_set_color(_is_cur_al ? _ad.glow_color : make_color_rgb(220, 180, 120));
            var _desc_line1 = string_copy(_ad.desc, 1, 30);
            var _desc_line2 = string_copy(_ad.desc, 31, 32);
            draw_text(_ax + 8, _ay + 50, _desc_line1);
            if (_desc_line2 != "") draw_text(_ax + 8, _ay + 68, _desc_line2);
        }
    }"""

assert old_subtab1_draw in draw_src, "Could not find old_subtab1_draw in Draw_64.gml"
draw_src = draw_src.replace(old_subtab1_draw, new_subtab1_draw)

with open(draw_path, "w") as f:
    f.write(draw_src)
print("Draw_64.gml updated with 2x5 grid for 10 Sintered Material Alloys.")
