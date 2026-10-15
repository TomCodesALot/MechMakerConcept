import re

FM_PATH = "objects/obj_FactionManager/Create_0.gml"

with open(FM_PATH, "r") as f:
    content = f.read()

# 1. Add mass_production_candidates and selection function right after mass_production_contracts definition
target_mpc = """        active_frontline_units: 0,
        block_level: 1
    }
};"""

replacement_mpc = """        active_frontline_units: 0,
        block_level: 1
    }
};

// 4b. Revamped Mass Production Candidate Pools (docs/29)
mass_production_candidates = {
    faction_a: [
        { id: "ms_terran_ironclad_07", name: "GHA-07 Ironclad", doctrine: "Kinetic Trench Fortress", weapon: "Type-77 120mm Autocannon", armor: 2480, power: 12, speed: 45, combat: 480, sprite: spr_ms_ironclad_idle, req_armor: 180, req_power: 8, bounty: 1800000, royalty: 45000 },
        { id: "ms_terran_ballista_04", name: "TH-M04 Ballista", doctrine: "Quadruped Heavy Artillery", weapon: "Twin 200mm Heavy Howitzers", armor: 2350, power: 11, speed: 38, combat: 460, sprite: spr_ms_ballista_idle, req_armor: 170, req_power: 9, bounty: 1750000, royalty: 42000 },
        { id: "ms_terran_centurion_02", name: "TH-C02 Centurion", doctrine: "Hydraulic Linebreaker", weapon: "GAU-88 Rotary Heavy Vulcan", armor: 2200, power: 14, speed: 62, combat: 510, sprite: spr_ms_ironclad_idle, req_armor: 160, req_power: 10, bounty: 1900000, royalty: 48000 },
        { id: "ms_terran_trenchcoat_09", name: "TH-T09 Trenchcoat", doctrine: "CQB Slugs & Smokescreen", weapon: "12-Gauge Heavy Slug Autoshotgun", armor: 2150, power: 10, speed: 50, combat: 430, sprite: spr_ms_ironclad_idle, req_armor: 155, req_power: 8, bounty: 1600000, royalty: 40000 }
    ],
    faction_b: [
        { id: "ms_colony_aether_01", name: "AET-01 Aether", doctrine: "Zero-G Agile Superiority", weapon: "Twin High-Yield Beam Carbines", armor: 1820, power: 16, speed: 85, combat: 490, sprite: spr_ms_aether_idle, req_armor: 120, req_power: 16, bounty: 2100000, royalty: 52000 },
        { id: "ms_colony_zephyr_05", name: "JCC-Z05 Zephyr", doctrine: "EW Sensor Jammer", weapon: "Pulse Laser Array & Jammer", armor: 1680, power: 15, speed: 92, combat: 470, sprite: spr_ms_zephyr_idle, req_armor: 110, req_power: 15, bounty: 2000000, royalty: 50000 },
        { id: "ms_colony_kepler_02", name: "JCC-K02 Kepler", doctrine: "Orbital Rail-Sniper", weapon: "Magnetic Linear Rail-Rifle", armor: 1720, power: 14, speed: 78, combat: 480, sprite: spr_ms_aether_idle, req_armor: 115, req_power: 14, bounty: 2050000, royalty: 51000 },
        { id: "ms_colony_oberon_08", name: "JCC-O08 Oberon", doctrine: "Point-Defense Fleet Escort", weapon: "Thermal Beam Lance & PDS", armor: 1950, power: 17, speed: 80, combat: 510, sprite: spr_ms_aether_idle, req_armor: 130, req_power: 17, bounty: 2200000, royalty: 54000 }
    ],
    faction_c: [
        { id: "ms_syndicate_hyena_12", name: "SCR-12 Hyena", doctrine: "Scrap Harpoon Scavenger", weapon: "Magnetic Harpoon & 80mm Flak", armor: 1980, power: 10, speed: 60, combat: 460, sprite: spr_ms_hyena_idle, req_armor: 130, req_power: 10, bounty: 1400000, royalty: 38000 },
        { id: "ms_syndicate_gorgon_04", name: "ARC-G04 Gorgon", doctrine: "Boarding Cutter & Ram", weapon: "Heavy Thermal Cutter Claw", armor: 2300, power: 12, speed: 52, combat: 490, sprite: spr_ms_gorgon_idle, req_armor: 145, req_power: 11, bounty: 1600000, royalty: 42000 },
        { id: "ms_syndicate_bloodhound_06", name: "ARC-B06 Bloodhound", doctrine: "Wheeled Pack Hunter", weapon: "Quad 70mm Rocket Pods", armor: 1850, power: 9, speed: 72, combat: 440, sprite: spr_ms_hyena_idle, req_armor: 120, req_power: 9, bounty: 1350000, royalty: 36000 },
        { id: "ms_syndicate_vandal_03", name: "ARC-V03 Vandal", doctrine: "Ambush Shrapnel & Decoys", weapon: "Flechette Autogun & Flares", armor: 1750, power: 10, speed: 66, combat: 430, sprite: spr_ms_hyena_idle, req_armor: 115, req_power: 9, bounty: 1300000, royalty: 35000 }
    ],
    faction_d: [
        { id: "ms_zaibatsu_muramasa_03", name: "ZAI-03 Muramasa", doctrine: "High-Frequency Tachyon Duelist", weapon: "High-Frequency Tachyon Katana", armor: 1950, power: 14, speed: 82, combat: 500, sprite: spr_ms_muramasa_idle, req_armor: 135, req_power: 14, bounty: 2400000, royalty: 58000 },
        { id: "ms_zaibatsu_kage_07", name: "ZBT-K07 Kage", doctrine: "Optical Camo Assassin", weapon: "Hyper-Velocity Needle Railgun", armor: 1650, power: 13, speed: 88, combat: 480, sprite: spr_ms_kage_idle, req_armor: 120, req_power: 13, bounty: 2300000, royalty: 55000 },
        { id: "ms_zaibatsu_ronin_04", name: "ZBT-R04 Ronin", doctrine: "Autonomous Sub-Drone Carrier", weapon: "Sub-Drone Swarm Pod & Naginata", armor: 2100, power: 16, speed: 75, combat: 520, sprite: spr_ms_muramasa_idle, req_armor: 140, req_power: 15, bounty: 2500000, royalty: 60000 },
        { id: "ms_zaibatsu_tessen_09", name: "ZBT-T09 Tessen", doctrine: "EMP Neural Jammer & Deflector", weapon: "Broadband EMP Disruptor", armor: 1820, power: 15, speed: 78, combat: 470, sprite: spr_ms_kage_idle, req_armor: 125, req_power: 14, bounty: 2250000, royalty: 54000 }
    ]
};

roll_playthrough_mass_production_selection = function(_forced_seed = undefined) {
    var _f_keys = ["faction_a", "faction_b", "faction_c", "faction_d"];
    for (var f = 0; f < array_length(_f_keys); f++) {
        var _fk = _f_keys[f];
        var _pool = mass_production_candidates[$ _fk];
        var _idx = 0;
        if (!is_undefined(_forced_seed)) {
            _idx = (_forced_seed + f * 7) % array_length(_pool);
        } else {
            _idx = irandom(array_length(_pool) - 1);
        }
        var _chosen = _pool[_idx];

        var _contract = mass_production_contracts[$ _fk];
        if (!is_undefined(_contract)) {
            _contract.baseline_suit_id = _chosen.id;
            _contract.baseline_suit_name = _chosen.name;
            _contract.doctrine = _chosen.doctrine;
            _contract.signature_weapon = _chosen.weapon;
            _contract.sprite_asset = _chosen.sprite;
            _contract.req_armor = _chosen.req_armor;
            _contract.req_power = _chosen.req_power;
            _contract.licensing_bounty = _chosen.bounty;
            _contract.royalty_per_turn = _chosen.royalty;
            _contract.combat_bonus = round(_chosen.combat / 25);
            _contract.candidate_index = _idx;
            show_debug_message("[MASS PRODUCTION VARIANCE] " + _fk + " ratified candidate " + string(_idx + 1) + "/4: " + _chosen.name + " (" + _chosen.doctrine + ")");
        }
    }
};

roll_playthrough_mass_production_selection();"""

assert target_mpc in content, "target_mpc not found in obj_FactionManager!"
content = content.replace(target_mpc, replacement_mpc, 1)

# 2. Update get_incumbent_specs to reflect active chosen candidate
old_incumbent = """get_incumbent_specs = function(_faction_id) {
    var _base = variable_struct_exists(incumbent_doctrines, _faction_id) ? incumbent_doctrines[$ _faction_id] : incumbent_doctrines.faction_a;"""

new_incumbent = """get_incumbent_specs = function(_faction_id) {
    var _base = variable_struct_exists(incumbent_doctrines, _faction_id) ? incumbent_doctrines[$ _faction_id] : incumbent_doctrines.faction_a;

    // Dynamically query mass_production_contracts for active playthrough line chassis (docs/29)
    if (variable_struct_exists(mass_production_contracts, _faction_id)) {
        var _mpc = mass_production_contracts[$ _faction_id];
        if (is_struct(_mpc) && variable_struct_exists(_mpc, "baseline_suit_name")) {
            _base.name = _mpc.baseline_suit_name;
            _base.id = _mpc.baseline_suit_id;
            _base.armor = _mpc.req_armor * 10;
            _base.power = _mpc.req_power;
            _base.doctrine_focus = _mpc[$ "doctrine"] ?? _base.doctrine_focus;
        }
    }"""

assert old_incumbent in content, "old_incumbent not found in obj_FactionManager!"
content = content.replace(old_incumbent, new_incumbent, 1)

# 3. Update get_faction_patrol_squad to attach sprite_asset from chosen mass production suit
old_patrol = """get_faction_patrol_squad = function(_faction_id) {
    var _chassis = get_faction_active_line_chassis(_faction_id);
    if (is_undefined(_chassis)) return [];
    var _squad = [];
    for (var u = 0; u < 4; u++) {
        array_push(_squad, {
            unit_id: "patrol_" + _faction_id + "_" + string(u + 1),
            callsign: _chassis.name + " Unit-" + string(u + 1),
            chassis_name: _chassis.name,
            blueprint_id: _chassis.blueprint_id,
            is_player_designed: _chassis.is_player_designed,
            armor: (_chassis.is_player_designed ? 2200 : 1800) + (_chassis.block_level * 150),
            combat_rating: 450 + (_chassis.combat_bonus * 5)
        });
    }
    return _squad;
};"""

new_patrol = """get_faction_patrol_squad = function(_faction_id) {
    var _chassis = get_faction_active_line_chassis(_faction_id);
    if (is_undefined(_chassis)) return [];
    var _spr = spr_ms_ironclad_idle;
    if (variable_struct_exists(mass_production_contracts, _faction_id)) {
        _spr = mass_production_contracts[$ _faction_id][$ "sprite_asset"] ?? _spr;
    }
    var _squad = [];
    for (var u = 0; u < 4; u++) {
        array_push(_squad, {
            unit_id: "patrol_" + _faction_id + "_" + string(u + 1),
            callsign: _chassis.name + " Unit-" + string(u + 1),
            chassis_name: _chassis.name,
            blueprint_id: _chassis.blueprint_id,
            sprite_asset: _spr,
            is_player_designed: _chassis.is_player_designed,
            armor: (_chassis.is_player_designed ? 2200 : 1800) + (_chassis.block_level * 150),
            combat_rating: 450 + (_chassis.combat_bonus * 5)
        });
    }
    return _squad;
};"""

assert old_patrol in content, "old_patrol not found in obj_FactionManager!"
content = content.replace(old_patrol, new_patrol, 1)

with open(FM_PATH, "w") as f:
    f.write(content)

print("Updated obj_FactionManager with mass_production_candidates & playthrough variance!")
