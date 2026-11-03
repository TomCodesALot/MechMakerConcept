import re

bm_path = "objects/obj_BattleManager/Create_0.gml"
with open(bm_path, "r") as f:
    code = f.read()

# 1. Update get_unit_sprite destroyed states
old_destroyed = '''    if (_u.is_destroyed) {
        return spr_ms_ironclad_destroyed;
    }'''

new_destroyed = '''    if (_u.is_destroyed) {
        if (variable_struct_exists(_u, "is_infantry") && _u.is_infantry) {
            return spr_inf_suppressed;
        }
        if (variable_struct_exists(_u, "is_aircraft") && _u.is_aircraft) {
            return spr_veh_wreckage_plane;
        }
        if (variable_struct_exists(_u, "is_vehicle") && _u.is_vehicle) {
            return spr_veh_wreckage_tank;
        }
        return spr_ms_ironclad_destroyed;
    }'''

if old_destroyed in code:
    code = code.replace(old_destroyed, new_destroyed)
    print("Updated get_unit_sprite destroyed states with infantry, aircraft, and tank wreckages.")

# 2. Update Era 0 Setup to include Infantry & Aircraft
old_era0_setup_start = 'if (_is_era_0) {\n    show_debug_message("[obj_BattleManager] Deploying Era 0 Conventional Forces! Unit 0 is sole Mobile Suit prototype.");'
new_era0_setup = '''if (_is_era_0) {
    show_debug_message("[obj_BattleManager] Deploying Era 0 Conventional Forces! Unit 0 is sole Mobile Suit prototype.");

    // Player Commander Unit is the sole operational Mobile Suit in the solar system
    units[0].callsign = "Alpha-01 'WARHAMMER' [PROTOTYPE]";
    units[0].is_vehicle = false;
    units[0].is_infantry = false;
    units[0].is_aircraft = false;

    // Convert Allied Wingmen into Combined-Arms Conventional Escorts
    if (array_length(units) > 1) {
        units[1].callsign = "Allied Armor 'MAMMOTH-1'";
        units[1].pilot_name = "Sgt. Miller";
        units[1].mech_type = "veh_terran_mammoth";
        units[1].sprite_asset = spr_veh_terran_mammoth_idle;
        units[1].is_vehicle = true;
        units[1].move_type = "treads";
        units[1].components = _create_veh_comp(520, 240, 480, 38);
        units[1].weapons = [
            { name: "Twin 120mm Cannons", short_name: "TWIN 120MM", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 0, range_min: 2, range_max: 6, damage: 140, anim_state: "fire_rifle", desc: "Dual heavy tank shells." },
            { name: "Coaxial Autocannon", short_name: "COAXIAL AC", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 0, range_min: 1, range_max: 4, damage: 75, anim_state: "fire_chaingun", desc: "Rapid suppression." }
        ];
    }
    if (array_length(units) > 2) {
        units[2].callsign = "Air Escort 'SKYHAMMER-2'";
        units[2].pilot_name = "Lt. Cross";
        units[2].mech_type = "veh_terran_skyhammer";
        units[2].sprite_asset = spr_veh_terran_skyhammer_idle;
        units[2].is_vehicle = true;
        units[2].is_aircraft = true;
        units[2].move_type = "aero";
        units[2].components = _create_veh_comp(320, 140, 260, 20);
        units[2].weapons = [
            { name: "GAU-30mm Rotary", short_name: "GAU-30MM", proj_type: "ROTARY_VULCAN", ap_cost: 3, heat_cost: 0, range_min: 1, range_max: 5, damage: 115, anim_state: "fire_chaingun", desc: "Armor-piercing strafe." },
            { name: "Heavy Rocket Salvo", short_name: "ROCKETS", proj_type: "MICRO_MISSILE", ap_cost: 3, heat_cost: 0, range_min: 2, range_max: 6, damage: 160, anim_state: "fire_missiles", desc: "Ground strike cluster." }
        ];
    }
    if (array_length(units) > 3) {
        units[3].callsign = "Terran 88th 'INFANTRY-SQUAD'";
        units[3].pilot_name = "Sgt. Barnes";
        units[3].mech_type = "inf_terran_squad";
        units[3].sprite_asset = spr_inf_terran_squad_idle;
        units[3].is_vehicle = false;
        units[3].is_infantry = true;
        units[3].squad_type = "PLATOON_3";
        units[3].squad_members_count = 4;
        units[3].move_type = "biped";
        units[3].components = _create_veh_comp(220, 90, 180, 14);
        units[3].weapons = [
            { name: "Heavy Anti-Tank Missile", short_name: "HEAVY ATGM", proj_type: "MICRO_MISSILE", ap_cost: 3, heat_cost: 0, range_min: 2, range_max: 6, damage: 155, anim_state: "fire_missiles", desc: "Anti-tank shaped charge rocket." },
            { name: "Squad Machine Gun", short_name: "SQUAD MG", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 0, range_min: 1, range_max: 4, damage: 70, anim_state: "fire_chaingun", desc: "Riflemen suppression volley." }
        ];
    }
    if (array_length(units) > 4) {
        units[4].callsign = "Recon Skiff 'STILETTO-4'";
        units[4].pilot_name = "Ens. Novak";
        units[4].mech_type = "veh_colony_stiletto";
        units[4].sprite_asset = spr_veh_colony_stiletto_idle;
        units[4].is_vehicle = true;
        units[4].move_type = "hover";
        units[4].components = _create_veh_comp(310, 120, 340, 16);
        units[4].weapons = [
            { name: "Twin Linear Railguns", short_name: "TWIN RAIL", proj_type: "RAILGUN_SLUG", ap_cost: 3, heat_cost: 0, range_min: 2, range_max: 7, damage: 130, anim_state: "fire_rifle", desc: "Linear rail needles." }
        ];
    }

    // Convert All Hostile Units into Diverse Conventional Platoons (Tanks, Jets, Infantry, Gunships)
    for (var u = 0; u < array_length(units); u++) {
        var _un = units[u];
        if (_un.team == "HOSTILE") {
            var _mod7 = u % 7;
            if (_mod7 == 0) {
                // Heavy Battle Tank
                _un.callsign = "Hostile MBT 'MAMMOTH-" + string(u) + "'";
                _un.mech_type = "veh_terran_mammoth";
                _un.sprite_asset = spr_veh_terran_mammoth_idle;
                _un.is_vehicle = true;
                _un.is_infantry = false;
                _un.is_aircraft = false;
                _un.move_type = "treads";
                _un.components = _create_veh_comp(520, 240, 480, 36);
                _un.weapons = [
                    { name: "Twin 120mm Cannons", short_name: "TWIN 120MM", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 0, range_min: 2, range_max: 6, damage: 135, anim_state: "fire_rifle", desc: "Heavy rifled shot." },
                    { name: "Coaxial Autocannon", short_name: "COAXIAL AC", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 0, range_min: 1, range_max: 4, damage: 70, anim_state: "fire_chaingun", desc: "Suppression stream." }
                ];
            } else if (_mod7 == 1) {
                // Syndicate Guerrilla Infantry Platoon
                _un.callsign = "Scrap Militia 'GUERRILLA-" + string(u) + "'";
                _un.mech_type = "inf_syndicate_squad";
                _un.sprite_asset = spr_inf_syndicate_squad_idle;
                _un.is_vehicle = false;
                _un.is_infantry = true;
                _un.is_aircraft = false;
                _un.squad_type = "PLATOON_3";
                _un.squad_members_count = 4;
                _un.move_type = "biped";
                _un.components = _create_veh_comp(210, 90, 170, 12);
                _un.weapons = [
                    { name: "Scrap RPG Volley", short_name: "SCRAP RPG", proj_type: "MICRO_MISSILE", ap_cost: 3, heat_cost: 0, range_min: 1, range_max: 5, damage: 140, anim_state: "fire_missiles", desc: "Improvised anti-armor rockets." },
                    { name: "Nail-Bomb Shrapnel", short_name: "NAIL BOMB", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 0, range_min: 1, range_max: 3, damage: 80, anim_state: "fire_chaingun", desc: "Shrapnel blast." }
                ];
            } else if (_mod7 == 2) {
                // Colony Valkyrie Tilt-Rotor Gunship
                _un.callsign = "Tilt-Rotor 'VALKYRIE-" + string(u) + "'";
                _un.mech_type = "veh_colony_gunship";
                _un.sprite_asset = spr_veh_colony_gunship_idle;
                _un.is_vehicle = true;
                _un.is_aircraft = true;
                _un.is_infantry = false;
                _un.move_type = "aero";
                _un.components = _create_veh_comp(380, 150, 280, 22);
                _un.weapons = [
                    { name: "Chin 25mm Gatling", short_name: "25MM GATLING", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 0, range_min: 1, range_max: 5, damage: 95, anim_state: "fire_chaingun", desc: "Gatling burst." },
                    { name: "Heavy Rocket Salvo", short_name: "ROCKETS", proj_type: "MICRO_MISSILE", ap_cost: 4, heat_cost: 0, range_min: 2, range_max: 7, damage: 170, anim_state: "fire_missiles", desc: "Parabolic missiles." }
                ];
            } else if (_mod7 == 3) {
                // Stealth Drone Tank
                _un.callsign = "Drone Tank 'KUROGANE-" + string(u) + "'";
                _un.mech_type = "veh_zaibatsu_kurogane";
                _un.sprite_asset = spr_veh_zaibatsu_kurogane_idle;
                _un.is_vehicle = true;
                _un.is_aircraft = false;
                _un.is_infantry = false;
                _un.move_type = "treads";
                _un.components = _create_veh_comp(360, 140, 380, 26);
                _un.weapons = [
                    { name: "75mm Hypersonic Railgun", short_name: "75MM RAILGUN", proj_type: "RAILGUN_SLUG", ap_cost: 3, heat_cost: 0, range_min: 2, range_max: 8, damage: 165, anim_state: "fire_rifle", desc: "Hypersonic sabot." }
                ];
            } else if (_mod7 == 4) {
                // Zaibatsu Cybernetic Android Squad
                _un.callsign = "Cyborg Squad 'SHINOBI-" + string(u) + "'";
                _un.mech_type = "inf_zaibatsu_squad";
                _un.sprite_asset = spr_inf_zaibatsu_squad_idle;
                _un.is_vehicle = false;
                _un.is_infantry = true;
                _un.is_aircraft = false;
                _un.squad_type = "PLATOON_3";
                _un.squad_members_count = 4;
                _un.move_type = "biped";
                _un.components = _create_veh_comp(240, 100, 190, 18);
                _un.weapons = [
                    { name: "Hypersonic Rail-Needles", short_name: "RAIL NEEDLE", proj_type: "RAILGUN_SLUG", ap_cost: 2, heat_cost: 0, range_min: 2, range_max: 7, damage: 110, anim_state: "fire_rifle", desc: "Surgical rail needles." },
                    { name: "Monofilament Wire Snare", short_name: "MONO SNARE", proj_type: "MELEE", ap_cost: 2, heat_cost: 0, range_min: 1, range_max: 1, damage: 135, anim_state: "melee", desc: "Molecular wire strike." }
                ];
            } else if (_mod7 == 5) {
                // Syndicate Buzzard Light Bomber
                _un.callsign = "Scrap Bomber 'BUZZARD-" + string(u) + "'";
                _un.mech_type = "veh_syndicate_bomber";
                _un.sprite_asset = spr_veh_syndicate_bomber_idle;
                _un.is_vehicle = true;
                _un.is_aircraft = true;
                _un.is_infantry = false;
                _un.move_type = "aero";
                _un.components = _create_veh_comp(300, 120, 240, 16);
                _un.weapons = [
                    { name: "Incendiary Slag Bombs", short_name: "SLAG BOMBS", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 0, range_min: 2, range_max: 6, damage: 150, anim_state: "fire_flak", desc: "Flaming slag drums." }
                ];
            } else {
                // Syndicate Gun Truck
                _un.callsign = "Scrap Gun Truck 'RUSTFANG-" + string(u) + "'";
                _un.mech_type = "veh_syndicate_technical";
                _un.sprite_asset = spr_veh_syndicate_technical_idle;
                _un.is_vehicle = true;
                _un.is_aircraft = false;
                _un.is_infantry = false;
                _un.move_type = "wheels";
                _un.components = _create_veh_comp(290, 110, 280, 18);
                _un.weapons = [
                    { name: "50mm Flak Cannon", short_name: "50MM FLAK", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 0, range_min: 1, range_max: 4, damage: 90, anim_state: "fire_chaingun", desc: "Scrap flak." },
                    { name: "Improvised Rockets", short_name: "ROCKETS", proj_type: "MICRO_MISSILE", ap_cost: 3, heat_cost: 0, range_min: 2, range_max: 5, damage: 130, anim_state: "fire_missiles", desc: "Rocket salvo." }
                ];
            }
        }
    }
}'''

# Replace the Era 0 setup block
era0_pattern = r'if \(_is_era_0\) \{.*?show_debug_message\("\[obj_BattleManager\] Deploying Era 0 Conventional Forces!.*?\n    \}\n\}'
code = re.sub(era0_pattern, new_era0_setup, code, flags=re.DOTALL)
print("Updated Era 0 setup block with combined-arms Infantry, Aircraft, and Armor.")

# 3. Add Mobile Suit Anti-Personnel suppression and ATGM interaction in resolve_combat_impact
ap_marker = '// Platoon Squad Member Casualty Attrition'
ap_combat_code = '''        // Prometheus Catalyst: Mobile Suit Anti-Personnel Suppression vs Infantry
        if ((!variable_struct_exists(_atk, "is_infantry") || !_atk.is_infantry) && (!variable_struct_exists(_atk, "is_vehicle") || !_atk.is_vehicle) && (variable_struct_exists(_def, "is_infantry") && _def.is_infantry)) {
            _mitigated_dmg = floor(_mitigated_dmg * 2.0);
            add_floating_text(_def_sx, _def_sy - 50, "INFANTRY SUPPRESSED! x2.0", c_red);
            add_log("[SUPPRESSION] " + _atk.callsign + " walking titan trampled and suppressed " + _def.callsign + "!");
        }

        // Conventional Infantry ATGM Rocket Callout vs Mobile Suits
        if ((variable_struct_exists(_atk, "is_infantry") && _atk.is_infantry) && _wpn.proj_type == "MICRO_MISSILE" && (!variable_struct_exists(_def, "is_infantry") || !_def.is_infantry)) {
            add_floating_text(_def_sx, _def_sy - 50, "ATGM SHAPED CHARGE!", c_yellow);
            add_log("[ATGM VOLLEY] " + _atk.callsign + " fired an anti-tank shaped charge directly into " + _def.callsign + "'s actuators!");
        }

        // Platoon Squad Member Casualty Attrition'''

if "INFANTRY SUPPRESSED! x2.0" not in code and ap_marker in code:
    code = code.replace(ap_marker, ap_combat_code)
    print("Injected Anti-Personnel suppression and ATGM combat logic in resolve_combat_impact.")

with open(bm_path, "w") as f:
    f.write(code)

print("obj_BattleManager/Create_0.gml updated successfully.")
