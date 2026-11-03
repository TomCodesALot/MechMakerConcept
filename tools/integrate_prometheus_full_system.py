import os
import re

print("=== Starting Prometheus Catalyst System Integration ===")

# -----------------------------------------------------------------------------
# 1. Update obj_GameManager/Create_0.gml
# -----------------------------------------------------------------------------
gm_path = "objects/obj_GameManager/Create_0.gml"
with open(gm_path, "r") as f:
    gm_code = f.read()

# 1a. Update timeline_era initialization
old_era_init = '''// 3c. Timeline Tech Eras & Progression (docs/27)
timeline_era = 2; // 1 = Early War (Y214), 2 = Industrial Escalation (Y215-216), 3 = Total War (Y217-219), 4 = Apex Crisis (Y220+)
timeline_era_name = "ERA II: INDUSTRIAL ESCALATION";'''

new_era_init = '''// 3c. Timeline Tech Eras & Progression (docs/27 & doc 38 Prometheus Catalyst)
timeline_era = 0; // 0 = Conventional Steel & Jet Fuel, 1 = First Mover Catalyst, 2 = Industrial Escalation, 3 = Total War, 4 = Apex Crisis
timeline_era_name = "ERA 0: CONVENTIONAL STEEL & JET FUEL";
first_mobile_suit_created = true; // Player foundry created the world's first working bipedal humanoid frame
first_mobile_suit_deployed = false; // Maiden combat deployment triggers global revolution
reverse_engineering_progress = {
    corp_vhi: 0.0,   // Vanguard Heavy Industries (Terran)
    corp_aod: 0.0,   // Astraea Orbital Dynamics (Colonies)
    corp_rust: 0.0,  // Rustworks Scrap Forge (Syndicates)
    corp_hats: 0.0   // Hyperion Advanced Tech (Zaibatsu)
};
reverse_engineering_unlocked = false;'''

if old_era_init in gm_code:
    gm_code = gm_code.replace(old_era_init, new_era_init)
    print("Updated timeline_era initialization in obj_GameManager.")
else:
    print("Notice: old_era_init pattern not exact match, searching regex...")
    gm_code = re.sub(
        r'// 3c\. Timeline Tech Eras & Progression.*?timeline_era_name = "ERA II: INDUSTRIAL ESCALATION";',
        new_era_init,
        gm_code,
        flags=re.DOTALL
    )

# 1b. Add conventional vehicles loading and trigger_mobile_suit_revolution
conv_veh_code = '''
// =============================================================================
// CONVENTIONAL VEHICLES REGISTRY & THE PROMETHEUS PROTOCOL (doc 38)
// =============================================================================
conventional_vehicles = [];
load_conventional_vehicles = function() {
    var _paths = ["datafiles/conventional_vehicles.json", "conventional_vehicles.json"];
    for (var p = 0; p < array_length(_paths); p++) {
        if (file_exists(_paths[p])) {
            try {
                var _buf = buffer_load(_paths[p]);
                var _str = buffer_read(_buf, buffer_string);
                buffer_delete(_buf);
                var _data = json_parse(_str);
                if (is_struct(_data) && variable_struct_exists(_data, "vehicles")) {
                    conventional_vehicles = _data.vehicles;
                    show_debug_message("[obj_GameManager] Loaded " + string(array_length(conventional_vehicles)) + " conventional vehicles from " + _paths[p]);
                    return;
                }
            } catch (_ex) {
                show_debug_message("[obj_GameManager] Error loading conventional vehicles: " + string(_ex));
            }
        }
    }
};
load_conventional_vehicles();

get_conventional_vehicle = function(_id) {
    for (var v = 0; v < array_length(conventional_vehicles); v++) {
        if (conventional_vehicles[v].id == _id) return conventional_vehicles[v];
    }
    return undefined;
};

trigger_mobile_suit_revolution = function(_mech_struct) {
    if (first_mobile_suit_deployed) return;
    first_mobile_suit_deployed = true;
    timeline_era = 1;
    timeline_era_name = "ERA I: THE FIRST MOVER CATALYST";
    reverse_engineering_unlocked = true;

    var _m_call = (is_struct(_mech_struct) && variable_struct_exists(_mech_struct, "callsign")) ? _mech_struct.callsign : "Alpha-01 'WARHAMMER'";

    array_push(last_turn_events, "! THE PROMETHEUS CATALYST: Mobile Suit (" + _m_call + ") publicly deployed in combat!");
    array_push(last_turn_events, "! DIPLOMATIC EMBARGO LIFTED: All Superpowers halt hostility to bid for player arms contracts!");
    array_push(last_turn_events, "! 365-DAY ARMS RACE TRIGGERED: Rival defense contractors scramble to reverse-engineer our frame!");

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("THE REVOLUTION: First Mobile Suit Deployed!", c_lime);
    }

    if (instance_exists(obj_FactionManager) && variable_instance_exists(obj_FactionManager, "on_mobile_suit_revolution")) {
        obj_FactionManager.on_mobile_suit_revolution();
    }
};
'''

if "trigger_mobile_suit_revolution = function" not in gm_code:
    # insert before update_competitors_for_new_era
    marker = "update_competitors_for_new_era = function() {"
    idx = gm_code.find(marker)
    if idx != -1:
        gm_code = gm_code[:idx] + conv_veh_code + "\n" + gm_code[idx:]
        print("Injected conventional vehicles and trigger_mobile_suit_revolution into obj_GameManager.")

# 1c. Update evaluate_timeline_progression
old_eval = '''evaluate_timeline_progression = function() {
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
};'''

new_eval = '''evaluate_timeline_progression = function() {
    var _old_era = timeline_era;

    // In Era 0, timeline stays conventional until player deploys their Mobile Suit
    if (!first_mobile_suit_deployed) {
        timeline_era = 0;
        timeline_era_name = "ERA 0: CONVENTIONAL STEEL & JET FUEL";
        return;
    }

    // 365-Day Reverse-Engineering Tick across 4 Rival Megacorporations (~0.28% per turn)
    if (reverse_engineering_unlocked) {
        var _corps = ["corp_vhi", "corp_aod", "corp_rust", "corp_hats"];
        for (var c = 0; c < 4; c++) {
            var _cid = _corps[c];
            var _cur_prog = reverse_engineering_progress[$ _cid];
            if (_cur_prog < 100.0) {
                var _delta = 0.28 + random_range(-0.05, 0.08);
                _cur_prog = min(100.0, _cur_prog + _delta);
                reverse_engineering_progress[$ _cid] = _cur_prog;
                if (_cur_prog >= 100.0 && variable_struct_exists(rival_corporations, _cid)) {
                    var _rc = rival_corporations[$ _cid];
                    array_push(last_turn_events, "! ARMS REPLICATION: " + _rc.name + " rolled out their first reverse-engineered Mobile Suit!");
                    if (instance_exists(obj_HQTerminal)) {
                        obj_HQTerminal.show_toast("COMPETITOR MS ROLLOUT: " + _rc.name + "!", c_red);
                    }
                }
            }
        }
    }

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
        timeline_era_name = "ERA I: THE FIRST MOVER CATALYST";
    }

    if (timeline_era != _old_era) {
        array_push(last_turn_events, "! TIMELINE TECH ADVANCEMENT: Sol System enters " + timeline_era_name + "!");
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("TECH ADVANCEMENT: " + timeline_era_name + "!", c_yellow);
        }
        update_competitors_for_new_era();
    }
};'''

if old_eval in gm_code:
    gm_code = gm_code.replace(old_eval, new_eval)
    print("Updated evaluate_timeline_progression in obj_GameManager.")

# 1d. Restrict starter inventory to the single Prometheus prototype
# Replace unit_ironclad_02 from deployable_mechs
marker_iron_02 = '        {\n            id: "unit_ironclad_02",'
idx_02 = gm_code.find(marker_iron_02)
if idx_02 != -1:
    end_02 = gm_code.find("        }\n    ]", idx_02)
    if end_02 != -1:
        gm_code = gm_code[:idx_02] + gm_code[end_02 + 10:]
        print("Restricted starting inventory to single Unit-01 Prometheus Prototype in obj_GameManager.")

with open(gm_path, "w") as f:
    f.write(gm_code)

print("obj_GameManager updated successfully.")

# -----------------------------------------------------------------------------
# 2. Update obj_FactionManager/Create_0.gml
# -----------------------------------------------------------------------------
fm_path = "objects/obj_FactionManager/Create_0.gml"
with open(fm_path, "r") as f:
    fm_code = f.read()

# Update initial standings for Era 0
old_standing = '''faction_standing = {
    faction_a: 45,      // Starting status with Terran Coalition
    faction_b: -20,     // Starting status with Outer Colonies
    faction_c: 10,      // Starting status with Rogue Syndicates
    faction_d: 0,       // Starting status with Apex Zaibatsu
    faction_e: -10,     // Starting status with Sidereal Sovereign League
    faction_f: 0        // Starting status with Tharsis Machine Consensus (Dormant)
};'''

new_standing = '''// Era 0 Starting Standings: Superpowers enforce sanctions, heavy tariffs, and border friction
faction_standing = {
    faction_a: -15,     // Terran Coalition (Hostile border friction & mineral quotas)
    faction_b: -25,     // Outer Colonies (Sanctioned / Suspicious)
    faction_c: -30,     // Rogue Syndicates (Hostile outlaws & piracy)
    faction_d: -10,     // Apex Zaibatsu (Dismissive corporate isolation)
    faction_e: -20,     // Sidereal Sovereign League (Hostile / Neutral)
    faction_f: 0        // Tharsis Machine Consensus (Dormant)
};'''

if old_standing in fm_code:
    fm_code = fm_code.replace(old_standing, new_standing)
    print("Updated initial standings in obj_FactionManager.")

# Add on_mobile_suit_revolution method
rev_method = '''
// =============================================================================
// THE PROMETHEUS PROTOCOL: DIPLOMATIC REVOLUTION (doc 38)
// =============================================================================
on_mobile_suit_revolution = function() {
    show_debug_message("[obj_FactionManager] The Prometheus Revolution triggered! Factions pivoting from hostility to desperate cooperation...");

    // 1. Diplomatic Truce & Standing Surge (+35 to all active factions)
    var _f_keys = ["faction_a", "faction_b", "faction_c", "faction_d", "faction_e"];
    for (var f = 0; f < array_length(_f_keys); f++) {
        var _fid = _f_keys[f];
        faction_standing[$ _fid] = clamp(faction_standing[$ _fid] + 35, 15, 80);
        if (variable_struct_exists(factions, _fid)) {
            var _fc = factions[$ _fid];
            _fc.standing = faction_standing[$ _fid];
            _fc.standing_title = "Arms Monopoly Partner";
            _fc.contract_bounty_multiplier = 3.0; // 300% bounty surge for player's mobile suit!
            _fc.ai_state = "MS_REVERSE_ENGINEERING";
            _fc.ai_behavior_title = "Desperate Reverse-Engineering & High-Bounty Procurement";
        }
    }

    if (variable_struct_exists(territory_control, "last_shift_report")) {
        territory_control.last_shift_report = "GLOBAL CEASEFIRE: Superpowers suspend operations to negotiate Mobile Suit contracts with the Iron Vanguard!";
    }
};
'''

if "on_mobile_suit_revolution = function" not in fm_code:
    fm_code += "\n" + rev_method
    print("Added on_mobile_suit_revolution to obj_FactionManager.")

with open(fm_path, "w") as f:
    f.write(fm_code)

print("obj_FactionManager updated successfully.")

# -----------------------------------------------------------------------------
# 3. Update obj_BattleManager/Create_0.gml
# -----------------------------------------------------------------------------
bm_path = "objects/obj_BattleManager/Create_0.gml"
with open(bm_path, "r") as f:
    bm_code = f.read()

# Add crushing melee bonus against conventional vehicles in resolve_combat_impact
target_crush = '// Platoon Squad Member Casualty Attrition'
crush_code = '''        // Prometheus Catalyst Bonus: Mobile Suit Melee Crushing vs Conventional Armor (doc 38)
        if (_wpn.proj_type == "MELEE" && (!variable_struct_exists(_atk, "is_vehicle") || !_atk.is_vehicle) && (variable_struct_exists(_def, "is_vehicle") && _def.is_vehicle)) {
            _mitigated_dmg = floor(_mitigated_dmg * 1.5);
            add_floating_text(_def_sx, _def_sy - 50, "CRUSHING BLOW! x1.5", c_orange);
        }

        // Platoon Squad Member Casualty Attrition'''

if "CRUSHING BLOW! x1.5" not in bm_code and target_crush in bm_code:
    bm_code = bm_code.replace(target_crush, crush_code)
    print("Added crushing melee bonus against vehicles in obj_BattleManager.")

# Add conventional units population in Era 0
# Check where units array is populated
old_allied_marker = '// --- ALLIED / PLAYER PMC BATTLEGROUP (8 Units) ---'
era0_units_builder = '''// Helper: Create Conventional Vehicle Component Set (doc 38)
create_vehicle_components = function(_hull_hp, _turret_hp, _prop_hp, _armor) {
    return {
        torso:    { name: "Armored Hull",        cur: _hull_hp,   max: _hull_hp,   armor: _armor, intact: true },
        head:     { name: "Turret / Optics",     cur: _turret_hp, max: _turret_hp, armor: floor(_armor * 0.8), intact: true },
        arm_left: { name: "Port Weapon Mount",   cur: floor(_hull_hp * 0.4), max: floor(_hull_hp * 0.4), armor: _armor, intact: true },
        arm_right:{ name: "Starboard Mount",     cur: floor(_hull_hp * 0.4), max: floor(_hull_hp * 0.4), armor: _armor, intact: true },
        legs:     { name: "Treads / Propulsion", cur: _prop_hp,   max: _prop_hp,   armor: _armor, intact: true },
        backpack: { name: "Engine & Fuel Cell",  cur: floor(_hull_hp * 0.35), max: floor(_hull_hp * 0.35), armor: floor(_armor * 0.6), intact: true }
    };
};
var _create_veh_comp = create_vehicle_components;

var _is_era_0 = (!instance_exists(obj_GameManager) || obj_GameManager.timeline_era == 0);

// --- ALLIED / PLAYER PMC BATTLEGROUP ---'''

if "create_vehicle_components = function" not in bm_code:
    bm_code = bm_code.replace(old_allied_marker, era0_units_builder)
    print("Injected create_vehicle_components into obj_BattleManager.")

with open(bm_path, "w") as f:
    f.write(bm_code)

print("obj_BattleManager updated successfully.")

# -----------------------------------------------------------------------------
# 4. Update obj_BattleManager Step_0.gml: Trigger Mobile Suit Revolution on Maiden Action
# -----------------------------------------------------------------------------
bms_path = "objects/obj_BattleManager/Step_0.gml"
with open(bms_path, "r") as f:
    bms_code = f.read()

catalyst_hook = '''// Prometheus Catalyst: Check maiden mobile suit sortie
if (instance_exists(obj_GameManager) && !obj_GameManager.first_mobile_suit_deployed) {
    if (array_length(units) > 0 && units[0].team == "ALLIED" && (!variable_struct_exists(units[0], "is_vehicle") || !units[0].is_vehicle)) {
        obj_GameManager.trigger_mobile_suit_revolution(units[0]);
    }
}
'''

if "Prometheus Catalyst: Check maiden mobile suit sortie" not in bms_code:
    bms_code = catalyst_hook + "\n" + bms_code
    with open(bms_path, "w") as f:
        f.write(bms_code)
    print("Injected Prometheus maiden sortie hook into obj_BattleManager Step_0.gml.")

print("=== Prometheus Catalyst System Integration Complete ===")
