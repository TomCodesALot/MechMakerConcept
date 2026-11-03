import re

bm_path = "objects/obj_BattleManager/Create_0.gml"
with open(bm_path, "r") as f:
    bm_code = f.read()

era0_block = '''// =============================================================================
// ERA 0: THE PROMETHEUS PROTOCOL - CONVENTIONAL BATTLEFIELD SETUP (doc 38)
// =============================================================================
if (_is_era_0) {
    show_debug_message("[obj_BattleManager] Deploying Era 0 Conventional Forces! Unit 0 is sole Mobile Suit prototype.");

    // Player Commander Unit is the sole operational Mobile Suit in the solar system
    units[0].callsign = "Alpha-01 'WARHAMMER' [PROTOTYPE]";
    units[0].is_vehicle = false;

    // Convert Allied Wingmen into Conventional Military Escorts
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
        units[2].move_type = "aero";
        units[2].components = _create_veh_comp(320, 140, 260, 20);
        units[2].weapons = [
            { name: "GAU-30mm Rotary", short_name: "GAU-30MM", proj_type: "ROTARY_VULCAN", ap_cost: 3, heat_cost: 0, range_min: 1, range_max: 5, damage: 115, anim_state: "fire_chaingun", desc: "Armor-piercing strafe." },
            { name: "Heavy Rocket Salvo", short_name: "ROCKETS", proj_type: "MICRO_MISSILE", ap_cost: 3, heat_cost: 0, range_min: 2, range_max: 6, damage: 160, anim_state: "fire_missiles", desc: "Ground strike cluster." }
        ];
    }
    if (array_length(units) > 3) {
        units[3].callsign = "Recon Skiff 'STILETTO-3'";
        units[3].pilot_name = "Ens. Novak";
        units[3].mech_type = "veh_colony_stiletto";
        units[3].sprite_asset = spr_veh_colony_stiletto_idle;
        units[3].is_vehicle = true;
        units[3].move_type = "hover";
        units[3].components = _create_veh_comp(310, 120, 340, 16);
        units[3].weapons = [
            { name: "Twin Linear Railguns", short_name: "TWIN RAIL", proj_type: "RAILGUN_SLUG", ap_cost: 3, heat_cost: 0, range_min: 2, range_max: 7, damage: 130, anim_state: "fire_rifle", desc: "Linear rail needles." }
        ];
    }

    // Convert All Hostile Units into Conventional Enemy Formations
    for (var u = 0; u < array_length(units); u++) {
        var _un = units[u];
        if (_un.team == "HOSTILE") {
            _un.is_vehicle = true;
            var _veh_mod = u % 5;
            if (_veh_mod == 0) {
                _un.callsign = "Hostile MBT 'MAMMOTH-" + string(u) + "'";
                _un.mech_type = "veh_terran_mammoth";
                _un.sprite_asset = spr_veh_terran_mammoth_idle;
                _un.move_type = "treads";
                _un.components = _create_veh_comp(520, 240, 480, 36);
                _un.weapons = [
                    { name: "Twin 120mm Cannons", short_name: "TWIN 120MM", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 0, range_min: 2, range_max: 6, damage: 135, anim_state: "fire_rifle", desc: "Heavy rifled shot." },
                    { name: "Coaxial Autocannon", short_name: "COAXIAL AC", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 0, range_min: 1, range_max: 4, damage: 70, anim_state: "fire_chaingun", desc: "Suppression stream." }
                ];
            } else if (_veh_mod == 1) {
                _un.callsign = "Hostile Skiff 'STILETTO-" + string(u) + "'";
                _un.mech_type = "veh_colony_stiletto";
                _un.sprite_asset = spr_veh_colony_stiletto_idle;
                _un.move_type = "hover";
                _un.components = _create_veh_comp(310, 120, 340, 16);
                _un.weapons = [
                    { name: "Twin Linear Railguns", short_name: "TWIN RAIL", proj_type: "RAILGUN_SLUG", ap_cost: 3, heat_cost: 0, range_min: 2, range_max: 7, damage: 125, anim_state: "fire_rifle", desc: "Rail needles." }
                ];
            } else if (_veh_mod == 2) {
                _un.callsign = "Hostile Jet 'DART-" + string(u) + "'";
                _un.mech_type = "veh_colony_dart";
                _un.sprite_asset = spr_veh_colony_dart_idle;
                _un.move_type = "aero";
                _un.components = _create_veh_comp(280, 110, 240, 14);
                _un.weapons = [
                    { name: "Pulse Laser Pylons", short_name: "PULSE LASER", proj_type: "BEAM_PULSE", ap_cost: 3, heat_cost: 0, range_min: 1, range_max: 6, damage: 140, anim_state: "fire_beam", desc: "Laser strafe." }
                ];
            } else if (_veh_mod == 3) {
                _un.callsign = "Drone Tank 'KUROGANE-" + string(u) + "'";
                _un.mech_type = "veh_zaibatsu_kurogane";
                _un.sprite_asset = spr_veh_zaibatsu_kurogane_idle;
                _un.move_type = "treads";
                _un.components = _create_veh_comp(360, 140, 380, 26);
                _un.weapons = [
                    { name: "75mm Railgun", short_name: "75MM RAILGUN", proj_type: "RAILGUN_SLUG", ap_cost: 3, heat_cost: 0, range_min: 2, range_max: 8, damage: 165, anim_state: "fire_rifle", desc: "Hypersonic sabot." }
                ];
            } else {
                _un.callsign = "Scrap Gun Truck 'RUSTFANG-" + string(u) + "'";
                _un.mech_type = "veh_syndicate_technical";
                _un.sprite_asset = spr_veh_syndicate_technical_idle;
                _un.move_type = "wheels";
                _un.components = _create_veh_comp(290, 110, 280, 18);
                _un.weapons = [
                    { name: "50mm Flak Cannon", short_name: "50MM FLAK", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 0, range_min: 1, range_max: 4, damage: 90, anim_state: "fire_chaingun", desc: "Scrap flak." },
                    { name: "Improvised Rockets", short_name: "ROCKETS", proj_type: "MICRO_MISSILE", ap_cost: 3, heat_cost: 0, range_min: 2, range_max: 5, damage: 130, anim_state: "fire_missiles", desc: "Rocket salvo." }
                ];
            }
        }
    }
}
'''

marker = "// 6. In-Flight Physical Projectiles & Combat FX Queues"
if "ERA 0: THE PROMETHEUS PROTOCOL" not in bm_code:
    idx = bm_code.find(marker)
    if idx != -1:
        bm_code = bm_code[:idx] + era0_block + "\n" + bm_code[idx:]
        with open(bm_path, "w") as f:
            f.write(bm_code)
        print("Successfully injected Era 0 conventional battlefield setup into obj_BattleManager.")
    else:
        print("Error: marker not found in obj_BattleManager.")
else:
    print("Era 0 conventional battlefield setup already present.")
