import re

print("Wiring Equipment Tech Tree into obj_HQTerminal and obj_BattleManager...")

# 1. Update obj_HQTerminal/Create_0.gml modular_crafting_catalog with req_tech_id
with open('objects/obj_HQTerminal/Create_0.gml', 'r') as f:
    hq_create = f.read()

# Define the 30 modular parts with their req_tech_id
part_tech_map = {
    # Heads
    "hd_vanguard_01": "tech_upg_analog_hydraulics",
    "hd_aether_02": "tech_upg_vernier_gimbals",
    "hd_cyclops_03": "tech_wpn_hyper_velocity_rifle",
    "hd_damascus_04": "tech_sld_composite_reactive",
    "hd_tachyon_05": "tech_sld_i_field_emitter",
    # Torsos
    "tr_colossus_01": "tech_rea_gas_cooled_fission",
    "tr_hyperion_02": "tech_rea_compact_fusion",
    "tr_phantom_03": "tech_upg_vernier_gimbals",
    "tr_damascus_04": "tech_rea_catalytic_prometheus",
    "tr_sol_05": ["tech_rea_antimatter_pinch", "tech_rea_tachyon_cyclotron"],
    # Arms
    "am_colossus_01": "tech_upg_analog_hydraulics",
    "am_vernier_02": "tech_upg_vernier_gimbals",
    "am_adamant_03": "tech_wpn_hyper_velocity_rifle",
    "am_aerogel_04": ["tech_upg_nanite_cooling", "tech_upg_overboost_rig"],
    "am_tachyon_05": "tech_wpn_beam_carbine",
    # Legs
    "lg_vanguard_01": "tech_upg_analog_hydraulics",
    "lg_stratos_02": "tech_upg_vernier_gimbals",
    "lg_titan_03": "tech_sld_composite_reactive",
    "lg_aerogel_04": ["tech_upg_nanite_cooling", "tech_upg_overboost_rig"],
    "lg_damascus_05": "tech_sld_magnetic_barrier",
    # Backpacks
    "bp_heavy_01": "tech_upg_analog_hydraulics",
    "bp_vernier_02": "tech_upg_vernier_gimbals",
    "bp_plasma_03": "tech_rea_catalytic_prometheus",
    "bp_aerogel_04": ["tech_upg_nanite_cooling", "tech_upg_overboost_rig"],
    "bp_tachyon_05": ["tech_rea_antimatter_pinch", "tech_rea_tachyon_cyclotron"],
    # Weapons
    "wp_vulcan_01": "tech_wpn_heavy_autocannon",
    "wp_beam_02": "tech_wpn_beam_carbine",
    "wp_rail_03": "tech_wpn_electromagnetic_railgun",
    "wp_sol_04": "tech_wpn_electromagnetic_railgun",
    "wp_tachyon_05": "tech_wpn_tachyon_lance"
}

for pid, tech_val in part_tech_map.items():
    if isinstance(tech_val, list):
        tech_str = '["' + '", "'.join(tech_val) + '"]'
    else:
        tech_str = f'"{tech_val}"'
    
    # Match pattern: { id: "pid", ... cost_cr: X }
    pattern = rf'(\{{\s*id:\s*"{pid}"[^}}]+)(cost_cr:\s*\d+)(\s*\}})'
    match = re.search(pattern, hq_create)
    if match:
        old_part = match.group(0)
        if "req_tech_id:" not in old_part:
            new_part = f'{match.group(1)}{match.group(2)}, req_tech_id: {tech_str}{match.group(3)}'
            hq_create = hq_create.replace(old_part, new_part)

with open('objects/obj_HQTerminal/Create_0.gml', 'w') as f:
    f.write(hq_create)

print("[1/3] obj_HQTerminal/Create_0.gml updated with req_tech_id on modular_crafting_catalog!")

# 2. Update obj_HQTerminal/Draw_64.gml to check tech licensing before forging
with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
    hq_draw = f.read()

target_forge_block = '''                // Material & Credit Costs
                var _cost_y = _st_y + _st_h + 12;
                var _cur_alloy_stock = _gm.get_alloy(_pitem.req_alloy);
                var _has_alloy = (_cur_alloy_stock >= _pitem.req_alloy_amount);
                var _has_cr = (_gm.funds >= _pitem.cost_cr);
                var _can_forge = (_has_alloy && _has_cr);

                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text(_cx + 14, _cost_y, "REQUIRED ALLOY:");
                scr_draw_alloy_swatch(_cx + 14, _cost_y + 20, 26, 18, _pitem.req_alloy);
                draw_set_color(_has_alloy ? c_lime : c_red);
                var _req_al_clean = string_replace_all(string_replace(_pitem.req_alloy, "alloy_", ""), "_", " ");
                draw_text(_cx + 46, _cost_y + 20, string(_pitem.req_alloy_amount) + "x " + _req_al_clean);
                draw_set_color(make_color_rgb(140, 170, 200));
                draw_text(_cx + 14, _cost_y + 44, "Stock: " + string(_cur_alloy_stock) + " | Cost: " + string(_pitem.cost_cr) + " Cr");

                // Forge Button
                var _f_btn_y = _cost_y + 70;
                var _f_btn_w = _card_w - 24;
                var _f_hov = (_mx >= _cx + 12 && _mx <= _cx + 12 + _f_btn_w && _my >= _f_btn_y && _my <= _f_btn_y + 32);

                if (_f_hov && _click) {
                    if (!_has_cr) {
                        show_toast("INSUFFICIENT FUNDS! (Requires " + string(_pitem.cost_cr) + " Cr)", c_red);
                    } else if (!_has_alloy) {
                        show_toast("INSUFFICIENT ALLOYS! (Requires " + string(_pitem.req_alloy_amount) + "x " + _pitem.req_alloy + ")", c_red);
                    } else {
                        _gm.craft_modular_part(_pitem, _pitem.req_alloy, _pitem.req_alloy_amount, _pitem.cost_cr);
                    }
                }

                scr_draw_snes_button(_cx + 12, _f_btn_y, _f_btn_w, 32, _can_forge ? "[FORGE PART]" : "[INSUFFICIENT]", _f_hov, false, _can_forge ? make_color_rgb(60, 220, 120) : make_color_rgb(160, 60, 60));'''

replacement_forge_block = '''                // Material, Credit & Tech Blueprint License Check
                var _cost_y = _st_y + _st_h + 12;
                var _cur_alloy_stock = _gm.get_alloy(_pitem.req_alloy);
                var _has_alloy = (_cur_alloy_stock >= _pitem.req_alloy_amount);
                var _has_cr = (_gm.funds >= _pitem.cost_cr);

                var _is_licensed = true;
                var _req_tname = "";
                if (variable_struct_exists(_pitem, "req_tech_id") && !is_undefined(_pitem.req_tech_id)) {
                    var _rdb = scr_research_get_tech_db();
                    if (is_array(_pitem.req_tech_id)) {
                        _is_licensed = false;
                        for (var ri = 0; ri < array_length(_pitem.req_tech_id); ri++) {
                            if (scr_research_is_unlocked(_pitem.req_tech_id[ri])) {
                                _is_licensed = true;
                                break;
                            }
                        }
                        if (!_is_licensed) {
                            var _f_id = _pitem.req_tech_id[0];
                            _req_tname = variable_struct_exists(_rdb, _f_id) ? _rdb[$ _f_id].name : _f_id;
                        }
                    } else if (string_length(_pitem.req_tech_id) > 0) {
                        _is_licensed = scr_research_is_unlocked(_pitem.req_tech_id);
                        if (!_is_licensed) {
                            _req_tname = variable_struct_exists(_rdb, _pitem.req_tech_id) ? _rdb[$ _pitem.req_tech_id].name : _pitem.req_tech_id;
                        }
                    }
                }
                var _can_forge = (_has_alloy && _has_cr && _is_licensed);

                draw_set_color(make_color_rgb(160, 190, 220));
                draw_text(_cx + 14, _cost_y, "REQUIRED ALLOY:");
                scr_draw_alloy_swatch(_cx + 14, _cost_y + 20, 26, 18, _pitem.req_alloy);
                draw_set_color(_has_alloy ? c_lime : c_red);
                var _req_al_clean = string_replace_all(string_replace(_pitem.req_alloy, "alloy_", ""), "_", " ");
                draw_text(_cx + 46, _cost_y + 20, string(_pitem.req_alloy_amount) + "x " + _req_al_clean);

                if (!_is_licensed) {
                    draw_set_color(make_color_rgb(255, 80, 80));
                    draw_text_transformed(_cx + 14, _cost_y + 44, "🔒 REQ R&D: " + string_copy(_req_tname, 1, 18), 0.60, 0.60, 0);
                } else {
                    draw_set_color(make_color_rgb(140, 170, 200));
                    draw_text(_cx + 14, _cost_y + 44, "Stock: " + string(_cur_alloy_stock) + " | Cost: " + string(_pitem.cost_cr) + " Cr");
                }

                // Forge Button
                var _f_btn_y = _cost_y + 70;
                var _f_btn_w = _card_w - 24;
                var _f_hov = (_mx >= _cx + 12 && _mx <= _cx + 12 + _f_btn_w && _my >= _f_btn_y && _my <= _f_btn_y + 32);

                if (_f_hov && _click) {
                    if (!_is_licensed) {
                        scr_audio_play_ui("cancel");
                        show_toast("BLUEPRINT LOCKED: Requires R&D: " + _req_tname + "!", c_red);
                    } else if (!_has_cr) {
                        scr_audio_play_ui("cancel");
                        show_toast("INSUFFICIENT FUNDS! (Requires " + string(_pitem.cost_cr) + " Cr)", c_red);
                    } else if (!_has_alloy) {
                        scr_audio_play_ui("cancel");
                        show_toast("INSUFFICIENT ALLOYS! (Requires " + string(_pitem.req_alloy_amount) + "x " + _pitem.req_alloy + ")", c_red);
                    } else {
                        _gm.craft_modular_part(_pitem, _pitem.req_alloy, _pitem.req_alloy_amount, _pitem.cost_cr);
                    }
                }

                var _btn_txt = _is_licensed ? (_can_forge ? "[FORGE PART]" : "[INSUFFICIENT]") : "[R&D LOCKED]";
                var _btn_col = !_is_licensed ? make_color_rgb(180, 50, 50) : (_can_forge ? make_color_rgb(60, 220, 120) : make_color_rgb(160, 60, 60));
                scr_draw_snes_button(_cx + 12, _f_btn_y, _f_btn_w, 32, _btn_txt, _f_hov, false, _btn_col);'''

assert target_forge_block in hq_draw, "Target forge block not found in obj_HQTerminal/Draw_64.gml"
hq_draw = hq_draw.replace(target_forge_block, replacement_forge_block)

with open('objects/obj_HQTerminal/Draw_64.gml', 'w') as f:
    f.write(hq_draw)

print("[2/3] obj_HQTerminal/Draw_64.gml updated with tech licensing check!")

# 3. Update obj_BattleManager/Create_0.gml to award Battlefield Salvage Intel & Black Box Eurekas
with open('objects/obj_BattleManager/Create_0.gml', 'r') as f:
    bm_code = f.read()

salvage_inject = '''
                        // 1b. Battlefield Salvage Intel & Black Box Eureka
                        if (_def.team == "HOSTILE") {
                            var _e_roll = irandom_range(1, 100);
                            if (_e_roll <= 45) {
                                var _intel_cat = "WEAPONS";
                                var _cs_low = string_lower(_def.callsign);
                                if (string_pos("beam", _cs_low) > 0 || string_pos("sniper", _cs_low) > 0) _intel_cat = "REACTORS";
                                else if (string_pos("skater", _cs_low) > 0 || string_pos("hover", _cs_low) > 0) _intel_cat = "UPGRADES";
                                else if (string_pos("dread", _cs_low) > 0 || string_pos("bastion", _cs_low) > 0) _intel_cat = "SHIELDS";
                                else _intel_cat = choose("WEAPONS", "REACTORS", "SHIELDS", "UPGRADES");

                                var _e_msg = scr_research_award_salvage_intel(_intel_cat, 0.50);
                                if (_e_msg != "") {
                                    add_log("[SALVAGE INTEL] " + _e_msg);
                                    scr_audio_play_ui("alert");
                                }
                            }
                        }'''

target_bm_wreckage = 'add_log("[FIELD WRECKAGE] Smoldering chassis created tactical cover on tile (" + string(_def.grid_c) + ", " + string(_def.grid_r) + ")");'
assert target_bm_wreckage in bm_code, "Target wreckage log not found in obj_BattleManager/Create_0.gml"

# Only replace the first instance where hostile kills occur
bm_code = bm_code.replace(target_bm_wreckage, target_bm_wreckage + salvage_inject, 1)

with open('objects/obj_BattleManager/Create_0.gml', 'w') as f:
    f.write(bm_code)

print("[3/3] obj_BattleManager/Create_0.gml updated with Battlefield Salvage Intel & Eurekas!")
