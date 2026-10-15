import re
import sys

# 1. Update obj_GameManager/Create_0.gml
with open('objects/obj_GameManager/Create_0.gml', 'r') as f:
    gm_content = f.read()

# Add timeline era and competitor catalog initialization
target_hook = '// 4. PMC Company Profile'

new_era_and_catalog = '''// 3c. Timeline Tech Eras & Progression (docs/27)
timeline_era = 2; // 1 = Early War (Y214), 2 = Industrial Escalation (Y215-216), 3 = Total War (Y217-219), 4 = Apex Crisis (Y220+)
timeline_era_name = "ERA II: INDUSTRIAL ESCALATION";
timeline_era_year_start = 214;

// 4c. Procedural Competitor R&D Catalog & Lineages (docs/27)
competitor_catalog = {};

init_competitor_catalog = function() {
    competitor_catalog = {
        corp_vhi: {
            id: "corp_vhi",
            name: "Valkyrie Heavy Industries",
            ticker: "VHI",
            branch: choose("BRANCH_A", "BRANCH_B"),
            branch_name: "",
            doctrine: "",
            suits_by_era: {},
            active_line_chassis: undefined,
            has_rare_x_spec: (random(100) < 35.0),
            rare_x_chassis: undefined
        },
        corp_aod: {
            id: "corp_aod",
            name: "Astraea Orbital Dynamics",
            ticker: "AOD",
            branch: choose("BRANCH_A", "BRANCH_B"),
            branch_name: "",
            doctrine: "",
            suits_by_era: {},
            active_line_chassis: undefined,
            has_rare_x_spec: (random(100) < 35.0),
            rare_x_chassis: undefined
        },
        corp_rust: {
            id: "corp_rust",
            name: "Rustworks Salvage Cartel",
            ticker: "RUST",
            branch: choose("BRANCH_A", "BRANCH_B"),
            branch_name: "",
            doctrine: "",
            suits_by_era: {},
            active_line_chassis: undefined,
            has_rare_x_spec: (random(100) < 35.0),
            rare_x_chassis: undefined
        },
        corp_hats: {
            id: "corp_hats",
            name: "Hyperion Advanced Tactical Systems",
            ticker: "HATS",
            branch: choose("BRANCH_A", "BRANCH_B"),
            branch_name: "",
            doctrine: "",
            suits_by_era: {},
            active_line_chassis: undefined,
            has_rare_x_spec: (random(100) < 35.0),
            rare_x_chassis: undefined
        }
    };

    // Populate Valkyrie R&D Branch
    var _vhi = competitor_catalog.corp_vhi;
    if (_vhi.branch == "BRANCH_A") {
        _vhi.branch_name = "Tungsten Citadel Doctrine";
        _vhi.doctrine = "Impenetrable frontal kinetic armor & stationary siege artillery";
        _vhi.suits_by_era = {
            era_1: { id: "TCM-03", name: "TCM-03 Bulwark", armor: 1620, power: 8, speed: 38, combat: 380, class: "Line Defense", primary_weapon: "90mm Rifled Cannon" },
            era_2: { id: "GHA-07", name: "GHA-07 Ironclad", armor: 2480, power: 12, speed: 45, combat: 480, class: "Assault Wall", primary_weapon: "Type-77 120mm Autocannon" },
            era_3: { id: "GHA-08", name: "GHA-08 Ironclad Bastion", armor: 3200, power: 15, speed: 40, combat: 590, class: "Heavy Bastion", primary_weapon: "Twin 150mm Siege Howitzer" },
            era_4: { id: "TCX-11", name: "TCX-11 Behemoth Mk.IV", armor: 4800, power: 22, speed: 35, combat: 720, class: "Heavy Dreadnought", primary_weapon: "Dual 400mm Hyper-Rail Batteries" }
        };
        _vhi.rare_x_chassis = { id: "VHI-X01", name: "VHI-X01 'Goliath Prime'", armor: 5400, power: 24, speed: 32, combat: 810, class: "Prototype Juggernaut", primary_weapon: "Supercritical Kinetic Ram" };
    } else {
        _vhi.branch_name = "Mobile Blitzkrieg Doctrine";
        _vhi.doctrine = "Tracked trench stormers & continuous feed rotary cannons";
        _vhi.suits_by_era = {
            era_1: { id: "VHI-01", name: "VHI Centurion Scout", armor: 1450, power: 9, speed: 55, combat: 390, class: "Light Blitz", primary_weapon: "40mm Twin Autocannon" },
            era_2: { id: "VHI-02", name: "VHI Centurion Assault", armor: 2200, power: 14, speed: 62, combat: 510, class: "Medium Striker", primary_weapon: "GAU-88 Rotary Heavy Vulcan" },
            era_3: { id: "VHI-03", name: "VHI Warhammer Breaker", armor: 2950, power: 18, speed: 58, combat: 620, class: "Heavy Stormer", primary_weapon: "Quad Rotary Shredder Cannon" },
            era_4: { id: "VHI-04", name: "VHI Titan Dreadnought", armor: 4300, power: 26, speed: 52, combat: 760, class: "Assault Dreadnought", primary_weapon: "Cyclic 200mm Autocannon Battery" }
        };
        _vhi.rare_x_chassis = { id: "VHI-X02", name: "VHI-X02 'Colossus Blitz'", armor: 4700, power: 28, speed: 60, combat: 830, class: "Prototype Breaker", primary_weapon: "Twin 50mm Continuous Chaingun" };
    }

    // Populate Astraea R&D Branch
    var _aod = competitor_catalog.corp_aod;
    if (_aod.branch == "BRANCH_A") {
        _aod.branch_name = "Coherent Energy Monopoly";
        _aod.doctrine = "Spinal particle beam accelerators & prism energy screen barriers";
        _aod.suits_by_era = {
            era_1: { id: "OCM-04", name: "OCM-04 Sylph", armor: 1180, power: 14, speed: 110, combat: 410, class: "Light Interceptor", primary_weapon: "Particle Carbine" },
            era_2: { id: "AET-01", name: "AET-01 Aether", armor: 1580, power: 16, speed: 120, combat: 510, class: "Energy Striker", primary_weapon: "Coherent Beam Pulse Rifle" },
            era_3: { id: "OCA-07", name: "OCA-07 Helios Arbalest", armor: 1850, power: 22, speed: 115, combat: 620, class: "Spinal Beam Sniper", primary_weapon: "Heavy Spinal Beam Accelerator" },
            era_4: { id: "OCX-15", name: "OCX-15 Seraphim Trans-Am", armor: 2900, power: 30, speed: 135, combat: 780, class: "Supercritical Dominator", primary_weapon: "Dual Hyper-Beam Cannons" }
        };
        _aod.rare_x_chassis = { id: "AOD-X01", name: "AOD-X01 'Solarion Phoenix'", armor: 3200, power: 34, speed: 140, combat: 850, class: "Prototype Dominator", primary_weapon: "Linear Vector Plasma Lance" };
    } else {
        _aod.branch_name = "Micro-G Vector Acrobatics";
        _aod.doctrine = "3D omni-directional vernier matrix & high-frequency plasma blades";
        _aod.suits_by_era = {
            era_1: { id: "AOD-01", name: "AOD Vector Dart", armor: 1050, power: 15, speed: 125, combat: 420, class: "Light Skirmisher", primary_weapon: "Twin Thermal Needles" },
            era_2: { id: "AOD-02", name: "AOD Mirage Skirmisher", armor: 1420, power: 18, speed: 135, combat: 530, class: "Vector Striker", primary_weapon: "High-Frequency Plasma Saber" },
            era_3: { id: "AOD-03", name: "AOD Valkyrie Wing", armor: 1750, power: 24, speed: 145, combat: 640, class: "Acrobatic Duelist", primary_weapon: "Twin Beam Naginata" },
            era_4: { id: "AOD-04", name: "AOD Chronos Interceptor", armor: 2600, power: 32, speed: 160, combat: 800, class: "Omni-Vector Ace", primary_weapon: "Relativistic Phase Blades" }
        };
        _aod.rare_x_chassis = { id: "AOD-X02", name: "AOD-X02 'Astraea Seraph'", armor: 2800, power: 36, speed: 175, combat: 880, class: "Prototype Interceptor", primary_weapon: "Chrono-Phase Beam Claws" };
    }

    // Populate Rustworks R&D Branch
    var _rust = competitor_catalog.corp_rust;
    if (_rust.branch == "BRANCH_A") {
        _rust.branch_name = "Molten Scrap Demolition";
        _rust.doctrine = "Converted ore refinery slag mortars & incendiary cluster bombs";
        _rust.suits_by_era = {
            era_1: { id: "SCR-05", name: "SCR-05 Marauder", armor: 1350, power: 8, speed: 65, combat: 360, class: "Pirate Raider", primary_weapon: "90mm Shrapnel Gun" },
            era_2: { id: "SCR-12", name: "SCR-12 Hyena", armor: 1720, power: 10, speed: 75, combat: 440, class: "Scav Raider", primary_weapon: "Flak Scattergun" },
            era_3: { id: "SCA-14", name: "SCA-14 Slag-Lobber", armor: 2250, power: 14, speed: 70, combat: 540, class: "Scrap Mortar", primary_weapon: "Molten Slag Catapult" },
            era_4: { id: "SCX-19", name: "SCX-19 Chimera Apex", armor: 3800, power: 20, speed: 78, combat: 710, class: "Hybrid Behemoth", primary_weapon: "Stolen Siege Railcannon" }
        };
        _rust.rare_x_chassis = { id: "RST-X01", name: "RST-X01 'Slag Titan'", armor: 4400, power: 22, speed: 65, combat: 790, class: "Prototype Demolisher", primary_weapon: "Thermal Slag Geyser" };
    } else {
        _rust.branch_name = "Overclocked Pirate Brawlers";
        _rust.doctrine = "Overpowered diesel-fusion cores & hydraulic wrecking cleavers";
        _rust.suits_by_era = {
            era_1: { id: "RST-01", name: "SCR Junk Ripper", armor: 1200, power: 10, speed: 80, combat: 370, class: "Light Brawler", primary_weapon: "Serrated Scrap Saw" },
            era_2: { id: "RST-02", name: "SCR Reaver Raider", armor: 1650, power: 13, speed: 90, combat: 470, class: "Medium Charger", primary_weapon: "Hydraulic Breaching Ram" },
            era_3: { id: "RST-03", name: "RST Blood Hound", armor: 2100, power: 18, speed: 95, combat: 580, class: "Heavy Berserker", primary_weapon: "Dual Crushing Shears" },
            era_4: { id: "RST-04", name: "RST Hellion Warlord", armor: 3400, power: 26, speed: 100, combat: 740, class: "Warlord Juggernaut", primary_weapon: "Spinal Kinetic Cleaver" }
        };
        _rust.rare_x_chassis = { id: "RST-X02", name: "RST-X02 'Junk Leviathan'", armor: 4100, power: 30, speed: 88, combat: 820, class: "Prototype Leviathan", primary_weapon: "Quad Wrecking Piles" };
    }

    // Populate Hyperion R&D Branch
    var _hats = competitor_catalog.corp_hats;
    if (_hats.branch == "BRANCH_A") {
        _hats.branch_name = "Cybernetic Neural-Drive";
        _hats.doctrine = "Transhuman brain-machine sync & predictive quantum combat AI";
        _hats.suits_by_era = {
            era_1: { id: "ZM-06", name: "ZM-06 Ronin", armor: 1250, power: 12, speed: 85, combat: 420, class: "Corporate Security", primary_weapon: "High-Frequency Vibro-Blade" },
            era_2: { id: "ZAI-03", name: "ZAI-03 Muramasa", armor: 1610, power: 18, speed: 95, combat: 560, class: "Cyber-Striker", primary_weapon: "Muramasa Plasma Katana" },
            era_3: { id: "ZMA-15", name: "ZMA-15 Raiden", armor: 1780, power: 24, speed: 100, combat: 670, class: "Precision Sniper", primary_weapon: "Hyper-Velocity Railgun" },
            era_4: { id: "ZX-22", name: "ZX-22 Susanoo Cyber-Drive", armor: 2750, power: 34, speed: 125, combat: 820, class: "Transhuman Godframe", primary_weapon: "Relativistic Tachyon Sabers" }
        };
        _hats.rare_x_chassis = { id: "HATS-X01", name: "HATS-X01 'Zero Muramasa'", armor: 3100, power: 38, speed: 135, combat: 910, class: "Prototype Cyber-Frame", primary_weapon: "Quantum Singularity Blade" };
    } else {
        _hats.branch_name = "Thermo-Optic Infiltration";
        _hats.doctrine = "Active light-bending camouflage & silent magnetic accelerators";
        _hats.suits_by_era = {
            era_1: { id: "HATS-01", name: "HATS Shadow Scout", armor: 1100, power: 13, speed: 95, combat: 430, class: "Stealth Scout", primary_weapon: "Suppressed Gauss Needle" },
            era_2: { id: "HATS-02", name: "HATS Specter Infiltrator", armor: 1520, power: 20, speed: 105, combat: 580, class: "Ghost Striker", primary_weapon: "Silent Mag-Sniper" },
            era_3: { id: "HATS-03", name: "HATS Phantom Recon", armor: 1720, power: 26, speed: 112, combat: 690, class: "EW Infiltrator", primary_weapon: "Disruptor Beam Pistol" },
            era_4: { id: "HATS-04", name: "HATS Shadow Raven", armor: 2550, power: 35, speed: 130, combat: 830, class: "Stealth Assassin", primary_weapon: "Phase-Cloaked Thermal Lance" }
        };
        _hats.rare_x_chassis = { id: "HATS-X02", name: "HATS-X02 'Eclipse Ghost'", armor: 2900, power: 40, speed: 145, combat: 920, class: "Prototype Infiltrator", primary_weapon: "Null-Trace Plasma Sniper" };
    }

    update_competitors_for_new_era();
};

update_competitors_for_new_era = function() {
    var _era_key = "era_" + string(timeline_era);
    var _corps = ["corp_vhi", "corp_aod", "corp_rust", "corp_hats"];
    for (var c = 0; c < 4; c++) {
        var _cp = competitor_catalog[$ _corps[c]];
        if (variable_struct_exists(_cp.suits_by_era, _era_key)) {
            _cp.active_line_chassis = _cp.suits_by_era[$ _era_key];
            if (variable_struct_exists(rival_corporations, _corps[c])) {
                rival_corporations[$ _corps[c]].flagship_chassis = _cp.active_line_chassis.name;
            }
        }
    }
};

evaluate_timeline_progression = function() {
    var _old_era = timeline_era;
    if (current_turn >= 200 || current_cycle_year >= 220) {
        timeline_era = 4;
        timeline_era_name = "ERA IV: APEX CRISIS & ARCHEOTECH";
    } else if (current_turn >= 120 || current_cycle_year >= 217) {
        timeline_era = 3;
        timeline_era_name = "ERA III: TOTAL STRATEGIC WAR";
    } else if (current_turn >= 60 || current_cycle_year >= 215) {
        timeline_era = 2;
        timeline_era_name = "ERA II: INDUSTRIAL ESCALATION";
    } else {
        timeline_era = 1;
        timeline_era_name = "ERA I: EARLY WAR SHAKEDOWN";
    }

    if (timeline_era != _old_era) {
        array_push(last_turn_events, "! TIMELINE TECH ADVANCEMENT: Sol System enters " + timeline_era_name + "!");
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("TECH ADVANCEMENT: " + timeline_era_name + "!", c_yellow);
        }
        update_competitors_for_new_era();
    }
};

evaluate_corporate_random_events = function() {
    if (!is_undefined(active_event_popup)) return false;
    if (array_length(narrative_events_list) == 0) return false;

    // 14% chance per turn to trigger an event
    if (random(100) < 14.0) {
        var _rand_idx = irandom(array_length(narrative_events_list) - 1);
        trigger_event_by_id(narrative_events_list[_rand_idx].id);
        return true;
    }
    return false;
};
'''

if target_hook in gm_content:
    gm_content = gm_content.replace(target_hook, new_era_and_catalog + '\n' + target_hook)
    print("Added timeline & competitor catalog to obj_GameManager/Create_0.gml")
else:
    print("ERROR: target_hook not found in obj_GameManager/Create_0.gml")
    sys.exit(1)

# Initialize competitor catalog at end of init
init_hook = 'load_narrative_events();'
if init_hook in gm_content:
    gm_content = gm_content.replace(init_hook, init_hook + '\ninit_competitor_catalog();')
    print("Hooked init_competitor_catalog() into GameManager")
else:
    print("ERROR: init_hook not found")
    sys.exit(1)

# Hook into end_turn()
turn_hook = '    // 7. Random Narrative Event Roll'
turn_replacement = '''    // Evaluate Timeline Progression & Procedural Competitor Updates (docs/27)
    evaluate_timeline_progression();

    // 7. Random Corporate & Narrative Events Engine (docs/27)
    evaluate_corporate_random_events();'''

if turn_hook in gm_content:
    gm_content = re.sub(r'    // 7\. Random Narrative Event Roll[^\n]*\n(?:[^\n]*\n){1,6}', turn_replacement + '\n', gm_content)
    print("Replaced random event roll in end_turn with evaluate_timeline_progression and evaluate_corporate_random_events")
else:
    print("WARNING: turn_hook not found directly")

with open('objects/obj_GameManager/Create_0.gml', 'w') as f:
    f.write(gm_content)

print("Saved obj_GameManager/Create_0.gml")
