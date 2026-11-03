# -*- coding: utf-8 -*-
"""
tools/build_obj_debug_manager.py
Generates obj_DebugManager: Universal Debug Menu & Battle Demonstration Engine.
"""

import os
import re

print("=== DEPLOYING OBJ_DEBUGMANAGER: UNIVERSAL DEBUG & BATTLE DEMO ENGINE ===")

os.makedirs("objects/obj_DebugManager", exist_ok=True)

# -----------------------------------------------------------------------------
# 1. objects/obj_DebugManager/obj_DebugManager.yy
# -----------------------------------------------------------------------------
yy_code = """{
  "$GMObject": "",
  "%Name": "obj_DebugManager",
  "eventList": [
    {
      "$GMEvent": "v1",
      "%Name": "",
      "collisionObjectId": null,
      "eventNum": 0,
      "eventType": 0,
      "isDnD": false,
      "name": "",
      "resourceType": "GMEvent",
      "resourceVersion": "2.0"
    },
    {
      "$GMEvent": "v1",
      "%Name": "",
      "collisionObjectId": null,
      "eventNum": 0,
      "eventType": 3,
      "isDnD": false,
      "name": "",
      "resourceType": "GMEvent",
      "resourceVersion": "2.0"
    },
    {
      "$GMEvent": "v1",
      "%Name": "",
      "collisionObjectId": null,
      "eventNum": 64,
      "eventType": 8,
      "isDnD": false,
      "name": "",
      "resourceType": "GMEvent",
      "resourceVersion": "2.0"
    },
    {
      "$GMEvent": "v1",
      "%Name": "",
      "collisionObjectId": null,
      "eventNum": 0,
      "eventType": 12,
      "isDnD": false,
      "name": "",
      "resourceType": "GMEvent",
      "resourceVersion": "2.0"
    }
  ],
  "managed": true,
  "name": "obj_DebugManager",
  "overriddenProperties": [],
  "parent": {
    "name": "MechMakerConcept",
    "path": "MechMakerConcept.yyp"
  },
  "parentObjectId": null,
  "persistent": true,
  "physicsAngularDamping": 0.1,
  "physicsDensity": 0.5,
  "physicsFriction": 0.2,
  "physicsGroup": 1,
  "physicsKinematic": false,
  "physicsLinearDamping": 0.1,
  "physicsObject": false,
  "physicsRestitution": 0.1,
  "physicsSensor": false,
  "physicsShape": 1,
  "physicsShapePoints": [],
  "physicsStartAwake": true,
  "properties": [],
  "resourceType": "GMObject",
  "resourceVersion": "2.0",
  "solid": false,
  "spriteId": null,
  "spriteMaskId": null,
  "visible": true
}
"""

with open("objects/obj_DebugManager/obj_DebugManager.yy", "w", encoding="utf-8") as f:
    f.write(yy_code)
print("[PASS] 1. obj_DebugManager.yy generated.")

# -----------------------------------------------------------------------------
# 2. objects/obj_DebugManager/CleanUp_0.gml
# -----------------------------------------------------------------------------
cleanup_code = """/// @description obj_DebugManager CleanUp Event
show_debug_message("[obj_DebugManager] CleanUp Event called.");
"""

with open("objects/obj_DebugManager/CleanUp_0.gml", "w", encoding="utf-8") as f:
    f.write(cleanup_code)
print("[PASS] 2. CleanUp_0.gml generated.")

# -----------------------------------------------------------------------------
# 3. objects/obj_DebugManager/Create_0.gml
# -----------------------------------------------------------------------------
create_code = """/// @description obj_DebugManager Create Event
// Universal PMC Debug Console & Battle Animation Proving Ground

if (instance_number(obj_DebugManager) > 1) {
    show_debug_message("[obj_DebugManager] Duplicate singleton detected. Destroying instance: " + string(id));
    instance_destroy();
    exit;
}

persistent = true;
depth = -9999;
show_debug_message("[obj_DebugManager] Initializing Universal Debug & Battle Demonstration Engine...");

// 1. Activation State
is_open = false;
active_debug_tab = 0; // 0 = Battle & Animation Lab, 1 = PMC Campaign Cheats
debug_toast = "";
debug_toast_timer = 0;
debug_toast_color = c_lime;

show_toast = function(_msg, _col = c_lime) {
    debug_toast = _msg;
    debug_toast_timer = 150;
    debug_toast_color = _col;
};

// 2. Factions & Category Definitions
factions = ["ALL", "faction_a", "faction_b", "faction_c", "faction_d", "pmc_player", "faction_e", "faction_f"];
faction_names = ["ALL FACTIONS", "Terran Coalition", "Outer Colonies", "Rust Syndicate", "Apex Zaibatsu", "PMC Vanguard", "Sovereign League", "Tharsis Consensus"];

categories = ["ALL", "MOBILE_SUIT", "CUSTOM_MECH", "VEHICLE", "INFANTRY"];
category_names = ["ALL CATEGORIES", "Mobile Suits", "Custom Sockets", "Vehicles", "Infantry Squads"];

// 3. Populate Comprehensive Unit Catalog Roster
master_roster = [];

var _add_unit = function(_id, _name, _fac, _cat, _chassis, _alloy, _spr, _weapon, _hp, _armor) {
    array_push(master_roster, {
        id: _id,
        name: _name,
        faction_id: _fac,
        category: _cat,
        chassis: _chassis,
        alloy: _alloy,
        sprite_asset: _spr,
        weapon_name: _weapon,
        hp: _hp,
        armor: _armor
    });
};

// 3a. Mobile Suits from obj_GameManager / JSON catalog
var _loaded_from_catalog = false;
if (instance_exists(obj_GameManager) && is_struct(obj_GameManager.mobile_suit_catalog)) {
    var _names = variable_struct_get_names(obj_GameManager.mobile_suit_catalog);
    if (array_length(_names) > 0) {
        for (var i = 0; i < array_length(_names); i++) {
            var _s = variable_struct_get(obj_GameManager.mobile_suit_catalog, _names[i]);
            if (is_struct(_s)) {
                _add_unit(
                    _s.id,
                    _s.name,
                    variable_struct_get(_s, "faction_id") ?? "faction_a",
                    "MOBILE_SUIT",
                    variable_struct_get(_s, "chassis_class") ?? "biped",
                    variable_struct_get(_s, "alloy_type") ?? "alloy_vanguard_comp",
                    variable_struct_get(_s, "sprite_asset") ?? "spr_ms_ironclad_idle",
                    variable_struct_get(_s, "primary_weapon") ?? "120mm Solid Kinetic Cannon",
                    650,
                    30
                );
            }
        }
        _loaded_from_catalog = true;
    }
}

if (!_loaded_from_catalog) {
    var _cat_paths = ["mobile_suit_catalog.json", "datafiles/mobile_suit_catalog.json"];
    for (var p = 0; p < array_length(_cat_paths); p++) {
        var _fp = _cat_paths[p];
        if (file_exists(_fp)) {
            try {
                var _buf = buffer_load(_fp);
                var _str = buffer_read(_buf, buffer_string);
                buffer_delete(_buf);
                var _parsed = json_parse(_str);
                if (is_struct(_parsed)) {
                    var _p_names = variable_struct_get_names(_parsed);
                    for (var i = 0; i < array_length(_p_names); i++) {
                        var _s = variable_struct_get(_parsed, _p_names[i]);
                        if (is_struct(_s)) {
                            _add_unit(
                                _s.id,
                                _s.name,
                                variable_struct_get(_s, "faction_id") ?? "faction_a",
                                "MOBILE_SUIT",
                                variable_struct_get(_s, "chassis_class") ?? "biped",
                                variable_struct_get(_s, "alloy_type") ?? "alloy_vanguard_comp",
                                variable_struct_get(_s, "sprite_asset") ?? "spr_ms_ironclad_idle",
                                variable_struct_get(_s, "primary_weapon") ?? "120mm Solid Kinetic Cannon",
                                650,
                                30
                            );
                        }
                    }
                    _loaded_from_catalog = true;
                    break;
                }
            } catch (_ex) {
                show_debug_message("[obj_DebugManager] Catalog load fallback error: " + string(_ex));
            }
        }
    }
}

// 3b. Custom Modular Socket Mechs (4 Mobility Archetypes)
_add_unit("custom_biped", "PMC Vanguard Heavy (Modular Socket)", "pmc_player", "CUSTOM_MECH", "biped", "alloy_vanguard_comp", "spr_ms_custom_biped_heavy_idle", "GAU-88 Rotary Heavy Vulcan", 680, 32);
_add_unit("custom_hover", "PMC Ghost Hover Sniper (Modular Socket)", "pmc_player", "CUSTOM_MECH", "hover", "alloy_hyperion_matrix", "spr_ms_custom_hover_sniper_idle", "Coherent Beam Pulse Rifle", 480, 20);
_add_unit("custom_tread", "PMC Scrapper Tread Artillery (Modular Socket)", "pmc_player", "CUSTOM_MECH", "tread", "alloy_adamantine_carbide", "spr_ms_custom_tread_artillery_idle", "Type-77 120mm Heavy Cannon", 750, 40);
_add_unit("custom_aero", "PMC Stratos Aero Striker (Modular Socket)", "pmc_player", "CUSTOM_MECH", "aero", "alloy_aerosteel_flux", "spr_ms_custom_aero_striker_idle", "Ares Swarm-16 Missiles", 450, 22);

// 3c. Conventional Vehicles (Doc 38)
_add_unit("veh_terran_mammoth", "Mammoth Heavy Siege Tank", "faction_a", "VEHICLE", "tread", "alloy_vanguard_comp", "spr_veh_terran_mammoth_idle", "Dual 150mm Siege Cannons", 520, 35);
_add_unit("veh_terran_skyhammer", "Skyhammer Combat Gunship", "faction_a", "VEHICLE", "aero", "alloy_vanguard_comp", "spr_veh_terran_skyhammer_idle", "Rotary Vulcan Pod", 380, 18);
_add_unit("veh_colony_stiletto", "Stiletto Attack Skimmer", "faction_b", "VEHICLE", "hover", "alloy_aerosteel_flux", "spr_veh_colony_stiletto_idle", "Coherent Beam Carbine", 310, 15);
_add_unit("veh_colony_dart", "Dart Interceptor Craft", "faction_b", "VEHICLE", "aero", "alloy_aerosteel_flux", "spr_veh_colony_dart_idle", "Micro-Missile Pod", 290, 14);
_add_unit("veh_colony_gunship", "Vespine Assault Gunship", "faction_b", "VEHICLE", "aero", "alloy_aerosteel_flux", "spr_veh_colony_gunship_idle", "Thermal Beam Cannon", 360, 18);
_add_unit("veh_syndicate_technical", "Reaver Flak Technical Truck", "faction_c", "VEHICLE", "wheeled", "alloy_adamantine_carbide", "spr_veh_syndicate_technical_idle", "Heavy Twin Flak Cannon", 280, 12);
_add_unit("veh_syndicate_bomber", "Corsair Low-Altitude Bomber", "faction_c", "VEHICLE", "aero", "alloy_adamantine_carbide", "spr_veh_syndicate_bomber_idle", "Thermite Bomb Bay", 420, 20);
_add_unit("veh_zaibatsu_kurogane", "Kurogane Heavy Hover Carrier", "faction_d", "VEHICLE", "hover", "alloy_tachyon_superalloy", "spr_veh_zaibatsu_kurogane_idle", "Railgun Point Defense", 580, 28);
_add_unit("veh_zaibatsu_drone_jet", "Kamaitachi Drone Jet", "faction_d", "VEHICLE", "aero", "alloy_tachyon_superalloy", "spr_veh_zaibatsu_drone_jet_idle", "Plasma Beam Emitter", 260, 14);

// 3d. Conventional Infantry Squads (Doc 38)
_add_unit("inf_terran_squad", "Terran Grenadier Platoon", "faction_a", "INFANTRY", "infantry", "alloy_vanguard_comp", "spr_inf_terran_squad_idle", "Anti-Armor Rocket Volley", 180, 8);
_add_unit("inf_colony_squad", "Colony Guerrilla Cell", "faction_b", "INFANTRY", "infantry", "alloy_aerosteel_flux", "spr_inf_colony_squad_idle", "Plasma Rifle Saturation", 150, 6);
_add_unit("inf_syndicate_squad", "Rust Syndicate Marauder Squad", "faction_c", "INFANTRY", "infantry", "alloy_adamantine_carbide", "spr_inf_syndicate_squad_idle", "Magnetic Harpoon & Charges", 160, 7);
_add_unit("inf_zaibatsu_squad", "Zaibatsu Spec-Ops Operatives", "faction_d", "INFANTRY", "infantry", "alloy_tachyon_superalloy", "spr_inf_zaibatsu_squad_idle", "Monoblades & Flechettes", 170, 10);

show_debug_message("[obj_DebugManager] Master unit catalog indexed: " + string(array_length(master_roster)) + " total units.");

// 4. Filtering & Selection Logic
atk_faction_idx = 0;
atk_cat_idx = 0;
atk_filtered_idx = 0;

def_faction_idx = 0;
def_cat_idx = 0;
def_filtered_idx = min(1, array_length(master_roster) - 1);

get_filtered_units = function(_fac_idx, _c_idx) {
    var _fac_id = factions[_fac_idx];
    var _cat_id = categories[_c_idx];
    var _res = [];
    for (var i = 0; i < array_length(master_roster); i++) {
        var _u = master_roster[i];
        if (_fac_id != "ALL" && _u.faction_id != _fac_id) continue;
        if (_cat_id != "ALL" && _u.category != _cat_id) continue;
        array_push(_res, _u);
    }
    if (array_length(_res) == 0 && array_length(master_roster) > 0) {
        array_push(_res, master_roster[0]);
    }
    return _res;
};

// 5. Interactive Animation Stage State
anim_states = ["idle", "fire_rifle", "fire_chaingun", "fire_beam", "fire_missiles", "melee", "boost", "damaged", "destroyed"];
anim_state_idx = 0;

anim_speeds = [0.25, 0.5, 1.0, 2.0];
anim_speed_names = ["0.25x", "0.5x", "1.0x", "2.0x"];
anim_speed_idx = 2; // 1.0x normal

anim_perspective = "front"; // "front" or "back"
is_paused = false;
step_frame_req = false;
subimg_atk = 0.0;
subimg_def = 0.0;

theaters = ["EARTH", "SPACE", "WATER", "SLAG"];
theater_names = ["Terran Badlands", "Orbital Space Void", "Harbor Water Canal", "Slag Foundry Caldera"];
theater_idx = 0;

weapon_classes = ["BALLISTIC", "ROTARY_VULCAN", "BEAM_PULSE", "MICRO_MISSILE", "MELEE"];
weapon_names = ["Type-77 120mm Solid Cannon", "GAU-88 Rotary Heavy Vulcan", "Coherent Beam Pulse Rifle", "Ares Swarm-16 Micro-Missiles", "Hydraulic Gun-Club Strike"];
weapon_idx = 0;

live_stage_particles = [];
live_stage_casings = [];

// 6. Full Cinematic Clash Duel Runner Struct
clash_cinematic = {
    active: false,
    phase: 0,
    timer: 0,
    shutter_y: 0,
    screen_shake: 0.0,
    theater: "EARTH",
    attacker: undefined,
    defender: undefined,
    weapon_class: "BALLISTIC",
    weapon_name: "Type-77 120mm Solid Cannon",
    raw_damage: 165,
    mitigated_dmg: 135,
    hit_part: "torso",
    is_hit: true,
    has_counter: true,
    counter_damage: 85,
    counter_part: "arm_left",
    atk_anim_state: "idle",
    def_anim_state: "idle",
    atk_dash_x: 0,
    atk_recoil_x: 0,
    atk_recoil_y: 0,
    def_recoil_x: 0,
    def_recoil_y: 0,
    atk_hp: 680,
    atk_max_hp: 680,
    def_hp: 650,
    def_max_hp: 650,
    projectiles: [],
    casings: [],
    particles: [],
    popups: []
};

// 7. Launch Full Cinematic Clash
launch_full_cinematic_clash = function() {
    var _atk_list = get_filtered_units(atk_faction_idx, atk_cat_idx);
    var _def_list = get_filtered_units(def_faction_idx, def_cat_idx);
    var _atk_u = _atk_list[clamp(atk_filtered_idx, 0, array_length(_atk_list) - 1)];
    var _def_u = _def_list[clamp(def_filtered_idx, 0, array_length(_def_list) - 1)];

    var _w_class = weapon_classes[weapon_idx];
    var _w_name = weapon_names[weapon_idx];

    clash_cinematic.active = true;
    clash_cinematic.phase = 0;
    clash_cinematic.timer = 0;
    clash_cinematic.shutter_y = 0;
    clash_cinematic.screen_shake = 0;
    clash_cinematic.theater = theaters[theater_idx];
    clash_cinematic.attacker = _atk_u;
    clash_cinematic.defender = _def_u;
    clash_cinematic.weapon_class = _w_class;
    clash_cinematic.weapon_name = _w_name;
    clash_cinematic.raw_damage = irandom_range(150, 210);
    clash_cinematic.mitigated_dmg = max(35, clash_cinematic.raw_damage - _def_u.armor);
    clash_cinematic.is_hit = true;
    clash_cinematic.has_counter = true;
    clash_cinematic.counter_damage = irandom_range(60, 110);
    clash_cinematic.atk_anim_state = "idle";
    clash_cinematic.def_anim_state = "idle";
    clash_cinematic.atk_dash_x = 0;
    clash_cinematic.atk_recoil_x = 0;
    clash_cinematic.atk_recoil_y = 0;
    clash_cinematic.def_recoil_x = 0;
    clash_cinematic.def_recoil_y = 0;
    clash_cinematic.atk_hp = _atk_u.hp;
    clash_cinematic.atk_max_hp = _atk_u.hp;
    clash_cinematic.def_hp = _def_u.hp;
    clash_cinematic.def_max_hp = _def_u.hp;
    clash_cinematic.projectiles = [];
    clash_cinematic.casings = [];
    clash_cinematic.particles = [];
    clash_cinematic.popups = [];

    scr_audio_play_ui("tab");
    show_toast("[SIMULATION LAUNCHED] Full 2-Tier Cinematic Clash Duel Active!", c_aqua);
};
"""

with open("objects/obj_DebugManager/Create_0.gml", "w", encoding="utf-8") as f:
    f.write(create_code)
print("[PASS] 3. Create_0.gml generated.")

# -----------------------------------------------------------------------------
# 4. objects/obj_DebugManager/Step_0.gml
# -----------------------------------------------------------------------------
step_code = """/// @description obj_DebugManager Step Event
// Drives Debug Input State, Cinematic Duel Choreography & Animation Stepping

// Toast Timer Countdown
if (debug_toast_timer > 0) debug_toast_timer--;

// 1. Universal Hotkey Trigger (F7 or backtick ` / ~)
var _toggle = keyboard_check_pressed(vk_f7) || keyboard_check_pressed(192) || keyboard_check_pressed(ord("`"));
if (_toggle) {
    is_open = !is_open;
    scr_audio_play_ui(is_open ? "boot" : "cancel");
    if (!is_open && clash_cinematic.active) {
        clash_cinematic.active = false;
    }
}

if (!is_open && !clash_cinematic.active) exit;

// 2. Escape closes debug panel or finishes cinematic clash
if (keyboard_check_pressed(vk_escape)) {
    if (clash_cinematic.active) {
        clash_cinematic.active = false;
        scr_audio_play_ui("cancel");
    } else {
        is_open = false;
        scr_audio_play_ui("cancel");
    }
    keyboard_clear(vk_escape);
}

// -------------------------------------------------------------------------
// 3. FULL CINEMATIC CLASH DUEL STATE MACHINE UPDATE
// -------------------------------------------------------------------------
if (clash_cinematic.active) {
    clash_cinematic.timer++;
    var _t = clash_cinematic.timer;

    // Fast-forward / Skip on Space or Enter
    if (keyboard_check_pressed(vk_space) || keyboard_check_pressed(vk_enter)) {
        if (clash_cinematic.phase < 3) {
            clash_cinematic.phase = 3;
            clash_cinematic.timer = 180;
        } else {
            clash_cinematic.active = false;
            exit;
        }
    }

    // Screen Shake Dampening
    clash_cinematic.screen_shake = max(0.0, clash_cinematic.screen_shake - 0.7);

    // Smooth Recoil Dampening
    clash_cinematic.atk_recoil_x = lerp(clash_cinematic.atk_recoil_x, 0, 0.15);
    clash_cinematic.atk_recoil_y = lerp(clash_cinematic.atk_recoil_y, 0, 0.15);
    clash_cinematic.def_recoil_x = lerp(clash_cinematic.def_recoil_x, 0, 0.15);
    clash_cinematic.def_recoil_y = lerp(clash_cinematic.def_recoil_y, 0, 0.15);
    clash_cinematic.atk_dash_x = lerp(clash_cinematic.atk_dash_x, 0, 0.12);

    // Phase 0: Cinema Bars Slide Down & Target Lock (t: 0 to 40)
    if (clash_cinematic.phase == 0) {
        clash_cinematic.shutter_y = min(75, clash_cinematic.shutter_y + 4.5);
        if (_t >= 40) {
            clash_cinematic.phase = 1;
            // Initiate Attack
            var _w_class = clash_cinematic.weapon_class;
            if (_w_class == "ROTARY_VULCAN") {
                clash_cinematic.atk_anim_state = "fire_chaingun";
                clash_cinematic.atk_recoil_x = -12;
                for (var v = 0; v < 4; v++) {
                    array_push(clash_cinematic.projectiles, {
                        x1: 360, y1: 450 + (v * 4) - 6,
                        x2: 1010, y2: 450 + (v * 4) - 6,
                        cur_x: 360 + (v * 40), cur_y: 450 + (v * 4) - 6,
                        speed: 34, type: "ROTARY_VULCAN"
                    });
                }
            } else if (_w_class == "BEAM_PULSE") {
                clash_cinematic.atk_anim_state = "fire_beam";
                clash_cinematic.atk_recoil_x = -8;
                array_push(clash_cinematic.projectiles, {
                    x1: 360, y1: 450, x2: 1010, y2: 450,
                    cur_x: 360, cur_y: 450, speed: 48, type: "BEAM_PULSE"
                });
            } else if (_w_class == "MICRO_MISSILE") {
                clash_cinematic.atk_anim_state = "fire_missiles";
                clash_cinematic.atk_recoil_x = -6;
                for (var m = 0; m < 3; m++) {
                    array_push(clash_cinematic.projectiles, {
                        x1: 360, y1: 440, x2: 1010, y2: 445,
                        cur_x: 360, cur_y: 440, speed: 24, type: "MICRO_MISSILE",
                        arc_offset: (m - 1) * 35
                    });
                }
            } else if (_w_class == "MELEE") {
                clash_cinematic.atk_anim_state = "melee";
                clash_cinematic.atk_dash_x = 420;
            } else {
                clash_cinematic.atk_anim_state = "fire_rifle";
                clash_cinematic.atk_recoil_x = -18;
                array_push(clash_cinematic.projectiles, {
                    x1: 360, y1: 450, x2: 1010, y2: 450,
                    cur_x: 360, cur_y: 450, speed: 30, type: "BALLISTIC"
                });
            }

            if (_w_class == "BALLISTIC" || _w_class == "ROTARY_VULCAN") {
                for (var c = 0; c < 3; c++) {
                    array_push(clash_cinematic.casings, {
                        x: 380 + random_range(-10, 10),
                        y: 440 + random_range(-10, 10),
                        vx: random_range(-3, -1),
                        vy: random_range(-6, -3),
                        angle: random(360),
                        rot_spd: random_range(12, 28)
                    });
                }
            }

            scr_audio_play_weapon(_w_class);
        }
    }
    // Phase 1: Attack Flying / Lunging (t: 40 to 95)
    else if (clash_cinematic.phase == 1) {
        if (_t >= 95) {
            clash_cinematic.phase = 2;
            clash_cinematic.screen_shake = 14.0;
            clash_cinematic.def_anim_state = "damaged";
            clash_cinematic.def_recoil_x = 18;
            clash_cinematic.def_hp = max(0, clash_cinematic.def_hp - clash_cinematic.mitigated_dmg);

            for (var p = 0; p < 8; p++) {
                array_push(clash_cinematic.particles, {
                    x: 1010 + random_range(-35, 35),
                    y: 450 + random_range(-35, 35),
                    sprite: spr_fx_explosion_small,
                    frame: 0.0, spd: 0.25,
                    scale: random_range(1.2, 1.8),
                    alpha: 1.0
                });
            }

            array_push(clash_cinematic.popups, {
                x: 1010, y: 410,
                text: "- " + string(clash_cinematic.mitigated_dmg) + " DMG",
                col: make_color_rgb(255, 120, 40),
                timer: 70, vy: -1.2
            });

            scr_audio_play_impact(clash_cinematic.weapon_class, true);
        }
    }
    // Phase 2: Impact & Counter Preparation (t: 95 to 155)
    else if (clash_cinematic.phase == 2) {
        if (_t >= 155) {
            clash_cinematic.phase = 3;
            if (clash_cinematic.has_counter && clash_cinematic.def_hp > 0) {
                clash_cinematic.def_anim_state = "fire_rifle";
                clash_cinematic.def_recoil_x = 12;
                clash_cinematic.atk_recoil_x = -14;
                clash_cinematic.atk_anim_state = "damaged";
                clash_cinematic.atk_hp = max(0, clash_cinematic.atk_hp - clash_cinematic.counter_damage);

                array_push(clash_cinematic.popups, {
                    x: 360, y: 410,
                    text: "- " + string(clash_cinematic.counter_damage) + " COUNTER",
                    col: make_color_rgb(0, 240, 255),
                    timer: 70, vy: -1.2
                });

                scr_audio_play_weapon("BALLISTIC");
                scr_audio_play_impact("BALLISTIC", false);
            }
        }
    }
    // Phase 3: Resolution & Exit Preparation (t: 155 to 220)
    else if (clash_cinematic.phase == 3) {
        if (_t >= 220) {
            clash_cinematic.phase = 4;
        }
    }
    // Phase 4: Shutter Retreat & Return to Debug Menu
    else if (clash_cinematic.phase == 4) {
        clash_cinematic.shutter_y = max(0, clash_cinematic.shutter_y - 4.5);
        if (clash_cinematic.shutter_y <= 0) {
            clash_cinematic.active = false;
        }
    }

    // Update in-flight projectiles
    for (var i = array_length(clash_cinematic.projectiles) - 1; i >= 0; i--) {
        var _pj = clash_cinematic.projectiles[i];
        _pj.cur_x += _pj.speed;
        if (_pj.cur_x >= _pj.x2) {
            array_delete(clash_cinematic.projectiles, i, 1);
        }
    }

    // Update tumbling brass casings
    for (var i = array_length(clash_cinematic.casings) - 1; i >= 0; i--) {
        var _cs = clash_cinematic.casings[i];
        _cs.x += _cs.vx;
        _cs.y += _cs.vy;
        _cs.vy += 0.35;
        _cs.angle += _cs.rot_spd;
        if (_cs.y > 600) array_delete(clash_cinematic.casings, i, 1);
    }

    // Update particles
    for (var i = array_length(clash_cinematic.particles) - 1; i >= 0; i--) {
        var _pt = clash_cinematic.particles[i];
        _pt.frame += _pt.spd;
        if (_pt.frame >= sprite_get_number(_pt.sprite)) {
            array_delete(clash_cinematic.particles, i, 1);
        }
    }

    // Update damage popups
    for (var i = array_length(clash_cinematic.popups) - 1; i >= 0; i--) {
        var _pp = clash_cinematic.popups[i];
        _pp.y += _pp.vy;
        _pp.timer--;
        if (_pp.timer <= 0) array_delete(clash_cinematic.popups, i, 1);
    }

    exit;
}

// -------------------------------------------------------------------------
// 4. LIVE INTERACTIVE ANIMATION STAGE STEPPING
// -------------------------------------------------------------------------
var _cur_spd = anim_speeds[anim_speed_idx];
if (!is_paused || step_frame_req) {
    subimg_atk += (0.15 * _cur_spd);
    subimg_def += (0.15 * _cur_spd);
    step_frame_req = false;
}
"""

with open("objects/obj_DebugManager/Step_0.gml", "w", encoding="utf-8") as f:
    f.write(step_code)
print("[PASS] 4. Step_0.gml generated.")

# -----------------------------------------------------------------------------
# 5. objects/obj_DebugManager/Draw_64.gml
# -----------------------------------------------------------------------------
draw_code = """/// @description obj_DebugManager Draw GUI Event
// Renders Front Mission / Gihren's Greed 2-Tier Battle Clash Demonstration & Universal Debug Hub

if (!is_open && !clash_cinematic.active) exit;

var _gw = display_get_gui_width();
var _gh = display_get_gui_height();
var _mx = device_mouse_x_to_gui(0);
var _my = device_mouse_y_to_gui(0);
var _click = mouse_check_button_pressed(mb_left);

// =========================================================================
// 1. FULL-SCREEN CINEMATIC CLASH DUEL STAGE
// =========================================================================
if (clash_cinematic.active) {
    var _shut = clash_cinematic.shutter_y;
    var _top_y = _shut;
    var _bot_y = _gh - _shut;

    var _shake_x = (clash_cinematic.screen_shake > 0) ? random_range(-clash_cinematic.screen_shake, clash_cinematic.screen_shake) : 0;
    var _shake_y = (clash_cinematic.screen_shake > 0) ? random_range(-clash_cinematic.screen_shake, clash_cinematic.screen_shake) : 0;

    // Environmental Backdrop
    if (clash_cinematic.theater == "SPACE") {
        draw_rectangle_color(0, _top_y, _gw, _bot_y, make_color_rgb(4, 7, 16), make_color_rgb(4, 7, 16), make_color_rgb(14, 22, 42), make_color_rgb(14, 22, 42), false);
        draw_set_color(make_color_rgb(10, 36, 70));
        draw_circle(_gw * 0.72, _gh * 1.05, 420, false);
        draw_set_color(make_color_rgb(50, 160, 255));
        draw_set_alpha(0.35);
        draw_circle(_gw * 0.72, _gh * 1.05, 425, true);
        draw_set_alpha(1.0);
        for (var i = 0; i < 45; i++) {
            var _sx = (i * 197 + 53) % _gw;
            var _sy = _top_y + ((i * 131 + 29) % max(1, _bot_y - _top_y));
            draw_set_color(c_white);
            draw_point(_sx, _sy);
        }
    } else if (clash_cinematic.theater == "WATER") {
        draw_rectangle_color(0, _top_y, _gw, _bot_y, make_color_rgb(10, 28, 48), make_color_rgb(14, 38, 64), make_color_rgb(6, 18, 32), make_color_rgb(8, 22, 38), false);
        draw_set_color(make_color_rgb(18, 55, 92));
        draw_rectangle(0, 500, _gw, _bot_y, false);
    } else if (clash_cinematic.theater == "SLAG") {
        draw_rectangle_color(0, _top_y, _gw, _bot_y, make_color_rgb(38, 14, 10), make_color_rgb(48, 18, 12), make_color_rgb(22, 8, 6), make_color_rgb(28, 10, 8), false);
        draw_set_color(make_color_rgb(70, 24, 14));
        draw_rectangle(0, 480, _gw, _bot_y, false);
    } else {
        // Earth Badlands
        draw_rectangle_color(0, _top_y, _gw, _bot_y, make_color_rgb(22, 16, 26), make_color_rgb(32, 24, 38), make_color_rgb(14, 10, 18), make_color_rgb(18, 12, 22), false);
        draw_set_color(make_color_rgb(38, 28, 36));
        draw_rectangle(0, 480, _gw, _bot_y, false);
    }

    // CRT Scanlines
    if (sprite_exists(spr_snes_crt_scanline)) {
        draw_sprite_tiled_ext(spr_snes_crt_scanline, 0, 0, _top_y, 1.0, 1.0, c_white, 0.12);
    }

    var _atk = clash_cinematic.attacker;
    var _def = clash_cinematic.defender;
    var _base_ground_y = 480;

    // Attacker Unit (Facing Right)
    var _ax = 360 + clash_cinematic.atk_recoil_x + _shake_x + clash_cinematic.atk_dash_x;
    var _ay = _base_ground_y + clash_cinematic.atk_recoil_y + _shake_y;
    scr_draw_animated_mobile_suit(_atk.id, _ax, _ay, 1.30, 1, clash_cinematic.atk_anim_state, -1, c_white, "front");

    // Defender Unit (Facing Left)
    var _dx = 1010 + clash_cinematic.def_recoil_x + _shake_x;
    var _dy = _base_ground_y + clash_cinematic.def_recoil_y + _shake_y;
    scr_draw_animated_mobile_suit(_def.id, _dx, _dy, 1.30, -1, clash_cinematic.def_anim_state, -1, c_white, "front");

    // Spent brass casings
    for (var i = 0; i < array_length(clash_cinematic.casings); i++) {
        var _cs = clash_cinematic.casings[i];
        draw_set_color(make_color_rgb(255, 215, 60));
        draw_line_width(_cs.x, _cs.y, _cs.x + lengthdir_x(7, _cs.angle), _cs.y + lengthdir_y(7, _cs.angle), 2.5);
    }

    // Projectiles
    for (var i = 0; i < array_length(clash_cinematic.projectiles); i++) {
        var _pj = clash_cinematic.projectiles[i];
        if (_pj.type == "ROTARY_VULCAN") {
            draw_set_color(make_color_rgb(255, 240, 140));
            draw_line_width(_pj.cur_x - 18, _pj.cur_y, _pj.cur_x + 18, _pj.cur_y, 3.0);
            draw_set_color(c_white);
            draw_line_width(_pj.cur_x - 8, _pj.cur_y, _pj.cur_x + 8, _pj.cur_y, 1.5);
        } else if (_pj.type == "BEAM_PULSE") {
            draw_set_color(make_color_rgb(0, 220, 255));
            draw_line_width(_pj.cur_x - 35, _pj.cur_y, _pj.cur_x + 35, _pj.cur_y, 6.0);
            draw_set_color(c_white);
            draw_line_width(_pj.cur_x - 25, _pj.cur_y, _pj.cur_x + 25, _pj.cur_y, 2.5);
        } else {
            draw_set_color(make_color_rgb(255, 200, 80));
            draw_line_width(_pj.cur_x - 14, _pj.cur_y, _pj.cur_x + 14, _pj.cur_y, 4.0);
        }
    }

    // Particles
    for (var i = 0; i < array_length(clash_cinematic.particles); i++) {
        var _pt = clash_cinematic.particles[i];
        if (sprite_exists(_pt.sprite)) {
            draw_sprite_ext(_pt.sprite, floor(_pt.frame), _pt.x + _shake_x, _pt.y + _shake_y, _pt.scale, _pt.scale, 0, c_white, _pt.alpha);
        }
    }

    // Floating Popups
    for (var i = 0; i < array_length(clash_cinematic.popups); i++) {
        var _pp = clash_cinematic.popups[i];
        draw_set_color(_pp.col);
        draw_text_transformed(_pp.x - 40, _pp.y, _pp.text, 1.25, 1.25, 0);
    }

    // Letterbox Shutter Bars
    draw_set_color(c_black);
    draw_rectangle(0, 0, _gw, _shut, false);
    draw_rectangle(0, _gh - _shut, _gw, _gh, false);

    // Top Header
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(24, max(8, _shut - 32), "THEATER: " + string_upper(clash_cinematic.theater) + " // HOLO-SIMULATION ENGAGEMENT GRID");
    draw_set_color(make_color_rgb(255, 200, 60));
    draw_text(_gw - 360, max(8, _shut - 32), "[SPACE / CLICK: SKIP // ESC: EXIT]");

    // Bottom Cockpit Telemetry Ribbons
    if (_shut >= 60) {
        // Attacker Telemetry (Left)
        draw_set_color(make_color_rgb(12, 18, 28));
        draw_rectangle(24, _gh - _shut + 8, 380, _gh - 8, false);
        draw_set_color(make_color_rgb(35, 65, 95));
        draw_rectangle(24, _gh - _shut + 8, 380, _gh - 8, true);
        draw_set_color(make_color_rgb(0, 240, 255));
        draw_text(34, _gh - _shut + 14, "ALLIED: " + _atk.name);
        draw_set_color(c_white);
        draw_text(34, _gh - _shut + 36, "HULL INTEGRITY: " + string(clash_cinematic.atk_hp) + " / " + string(clash_cinematic.atk_max_hp));

        // Defender Telemetry (Right)
        draw_set_color(make_color_rgb(28, 14, 12));
        draw_rectangle(_gw - 404, _gh - _shut + 8, _gw - 24, _gh - 8, false);
        draw_set_color(make_color_rgb(95, 45, 35));
        draw_rectangle(_gw - 404, _gh - _shut + 8, _gw - 24, _gh - 8, true);
        draw_set_color(make_color_rgb(255, 120, 40));
        draw_text(_gw - 394, _gh - _shut + 14, "TARGET: " + _def.name);
        draw_set_color(c_white);
        draw_text(_gw - 394, _gh - _shut + 36, "HULL INTEGRITY: " + string(clash_cinematic.def_hp) + " / " + string(clash_cinematic.def_max_hp));
    }

    if (_click) {
        if (clash_cinematic.phase < 3) {
            clash_cinematic.phase = 3;
            clash_cinematic.timer = 180;
        } else {
            clash_cinematic.active = false;
        }
    }
    exit;
}

// =========================================================================
// 2. MAIN DEBUG & PROVING GROUND WINDOW (SNES STEEL AESTHETICS)
// =========================================================================
draw_set_color(c_black);
draw_set_alpha(0.78);
draw_rectangle(0, 0, _gw, _gh, false);
draw_set_alpha(1.0);

var _win_x = 38;
var _win_y = 28;
var _win_w = 1290;
var _win_h = 712;
scr_draw_snes_panel(_win_x, _win_y, _win_w, _win_h, "", -1, true, 0.05);

// Header Bar
draw_set_color(make_color_rgb(0, 240, 255));
draw_text(_win_x + 20, _win_y + 14, "PMC DEBUG CONSOLE // COMBAT & ANIMATION ENGINE PROVING GROUND");
draw_set_color(make_color_rgb(140, 170, 200));
draw_text(_win_x + 580, _win_y + 14, "[TOGGLE: F7 / TILDE]");

// Tab Buttons
var _t0_hov = (_mx >= _win_x + 760 && _mx <= _win_x + 970 && _my >= _win_y + 8 && _my <= _win_y + 36);
if (_t0_hov && _click) {
    active_debug_tab = 0;
    scr_audio_play_ui("tab");
}
scr_draw_snes_button(_win_x + 760, _win_y + 8, 210, 28, "1. BATTLE & ANIMATION LAB", _t0_hov || (active_debug_tab == 0), (active_debug_tab == 0), (active_debug_tab == 0) ? make_color_rgb(0, 240, 255) : c_white);

var _t1_hov = (_mx >= _win_x + 980 && _mx <= _win_x + 1190 && _my >= _win_y + 8 && _my <= _win_y + 36);
if (_t1_hov && _click) {
    active_debug_tab = 1;
    scr_audio_play_ui("tab");
}
scr_draw_snes_button(_win_x + 980, _win_y + 8, 210, 28, "2. CAMPAIGN CHEATS & TOOLS", _t1_hov || (active_debug_tab == 1), (active_debug_tab == 1), (active_debug_tab == 1) ? make_color_rgb(0, 240, 255) : c_white);

// Close Button [X]
var _cls_hov = (_mx >= _win_x + _win_w - 56 && _mx <= _win_x + _win_w - 20 && _my >= _win_y + 8 && _my <= _win_y + 36);
if (_cls_hov && _click) {
    is_open = false;
    scr_audio_play_ui("cancel");
}
scr_draw_snes_button(_win_x + _win_w - 56, _win_y + 8, 36, 28, "X", _cls_hov, false, c_red);

// =========================================================================
// TAB 0: BATTLE & ANIMATION PROVING GROUND LAB
// =========================================================================
if (active_debug_tab == 0) {
    // ---------------------------------------------------------------------
    // A. LEFT COLUMN: ATTACKER SQUADRON SELECTION (w: 300)
    // ---------------------------------------------------------------------
    var _col1_x = _win_x + 14;
    var _col1_y = _win_y + 44;
    var _col1_w = 300;
    var _col1_h = 654;
    scr_draw_snes_panel(_col1_x, _col1_y, _col1_w, _col1_h, "ATTACKER CONFIGURATION", make_color_rgb(0, 240, 255), true, 0.03);

    var _atk_list = get_filtered_units(atk_faction_idx, atk_cat_idx);
    atk_filtered_idx = clamp(atk_filtered_idx, 0, max(0, array_length(_atk_list) - 1));
    var _cur_atk = _atk_list[atk_filtered_idx];

    // Faction Filter Selector
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col1_x + 14, _col1_y + 26, "FACTION FILTER:");
    var _af_hov = (_mx >= _col1_x + 14 && _mx <= _col1_x + _col1_w - 14 && _my >= _col1_y + 44 && _my <= _col1_y + 70);
    if (_af_hov && _click) {
        atk_faction_idx = (atk_faction_idx + 1) % array_length(factions);
        atk_filtered_idx = 0;
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col1_x + 14, _col1_y + 44, _col1_w - 28, 26, "< " + faction_names[atk_faction_idx] + " >", _af_hov, false, make_color_rgb(0, 240, 255));

    // Category Filter Selector
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col1_x + 14, _col1_y + 78, "CATEGORY FILTER:");
    var _ac_hov = (_mx >= _col1_x + 14 && _mx <= _col1_x + _col1_w - 14 && _my >= _col1_y + 96 && _my <= _col1_y + 122);
    if (_ac_hov && _click) {
        atk_cat_idx = (atk_cat_idx + 1) % array_length(categories);
        atk_filtered_idx = 0;
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col1_x + 14, _col1_y + 96, _col1_w - 28, 26, "< " + category_names[atk_cat_idx] + " >", _ac_hov, false, make_color_rgb(0, 240, 255));

    // Unit Carousel Navigation
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col1_x + 14, _col1_y + 130, "UNIT SELECTION (" + string(atk_filtered_idx + 1) + " / " + string(array_length(_atk_list)) + "):");

    var _p_hov = (_mx >= _col1_x + 14 && _mx <= _col1_x + 70 && _my >= _col1_y + 148 && _my <= _col1_y + 176);
    if (_p_hov && _click) {
        atk_filtered_idx = (atk_filtered_idx - 1 + array_length(_atk_list)) % array_length(_atk_list);
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col1_x + 14, _col1_y + 148, 56, 28, "< PREV", _p_hov, false, c_white);

    var _n_hov = (_mx >= _col1_x + _col1_w - 70 && _mx <= _col1_x + _col1_w - 14 && _my >= _col1_y + 148 && _my <= _col1_y + 176);
    if (_n_hov && _click) {
        atk_filtered_idx = (atk_filtered_idx + 1) % array_length(_atk_list);
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col1_x + _col1_w - 70, _col1_y + 148, 56, 28, "NEXT >", _n_hov, false, c_white);

    // Unit Specification Card
    draw_set_color(make_color_rgb(16, 24, 34));
    draw_rectangle(_col1_x + 14, _col1_y + 186, _col1_x + _col1_w - 14, _col1_y + 440, false);
    draw_set_color(make_color_rgb(32, 60, 90));
    draw_rectangle(_col1_x + 14, _col1_y + 186, _col1_x + _col1_w - 14, _col1_y + 440, true);

    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text_transformed(_col1_x + 22, _col1_y + 196, _cur_atk.name, 0.95, 0.95, 0);

    draw_set_color(make_color_rgb(140, 170, 200));
    draw_text(_col1_x + 22, _col1_y + 226, "ID: " + _cur_atk.id);
    draw_text(_col1_x + 22, _col1_y + 250, "FACTION: " + _cur_atk.faction_id);
    draw_text(_col1_x + 22, _col1_y + 274, "CATEGORY: " + _cur_atk.category);
    draw_text(_col1_x + 22, _col1_y + 298, "CHASSIS: " + string_upper(_cur_atk.chassis));
    draw_text(_col1_x + 22, _col1_y + 322, "ALLOY: " + _cur_atk.alloy);
    draw_text(_col1_x + 22, _col1_y + 346, "WEAPON: " + _cur_atk.weapon_name);
    draw_text(_col1_x + 22, _col1_y + 370, "HULL: " + string(_cur_atk.hp) + " HP");
    draw_text(_col1_x + 22, _col1_y + 394, "ARMOR: " + string(_cur_atk.armor) + " RATING");

    // Perspective Selector Button
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col1_x + 14, _col1_y + 456, "PERSPECTIVE ANGLE:");
    var _per_hov = (_mx >= _col1_x + 14 && _mx <= _col1_x + _col1_w - 14 && _my >= _col1_y + 474 && _my <= _col1_y + 504);
    if (_per_hov && _click) {
        anim_perspective = (anim_perspective == "front") ? "back" : "front";
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col1_x + 14, _col1_y + 474, _col1_w - 28, 30, (anim_perspective == "front") ? "[3/4 ISOMETRIC FRONT]" : "[REAR TWIN VERNIERS]", _per_hov, false, make_color_rgb(100, 220, 255));

    // Formation Stance
    draw_set_color(make_color_rgb(60, 240, 120));
    draw_text(_col1_x + 14, _col1_y + 524, "STANCE: ALLIED ATTACKER (FACING RIGHT)");

    // ---------------------------------------------------------------------
    // B. RIGHT COLUMN: DEFENDER TARGET SELECTION (w: 300)
    // ---------------------------------------------------------------------
    var _col3_x = _win_x + _win_w - 314;
    var _col3_y = _win_y + 44;
    var _col3_w = 300;
    var _col3_h = 654;
    scr_draw_snes_panel(_col3_x, _col3_y, _col3_w, _col3_h, "DEFENDER TARGET", make_color_rgb(255, 120, 40), true, 0.03);

    var _def_list = get_filtered_units(def_faction_idx, def_cat_idx);
    def_filtered_idx = clamp(def_filtered_idx, 0, max(0, array_length(_def_list) - 1));
    var _cur_def = _def_list[def_filtered_idx];

    // Faction Filter Selector
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col3_x + 14, _col3_y + 26, "FACTION FILTER:");
    var _df_hov = (_mx >= _col3_x + 14 && _mx <= _col3_x + _col3_w - 14 && _my >= _col3_y + 44 && _my <= _col3_y + 70);
    if (_df_hov && _click) {
        def_faction_idx = (def_faction_idx + 1) % array_length(factions);
        def_filtered_idx = 0;
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col3_x + 14, _col3_y + 44, _col3_w - 28, 26, "< " + faction_names[def_faction_idx] + " >", _df_hov, false, make_color_rgb(255, 120, 40));

    // Category Filter Selector
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col3_x + 14, _col3_y + 78, "CATEGORY FILTER:");
    var _dc_hov = (_mx >= _col3_x + 14 && _mx <= _col3_x + _col3_w - 14 && _my >= _col3_y + 96 && _my <= _col3_y + 122);
    if (_dc_hov && _click) {
        def_cat_idx = (def_cat_idx + 1) % array_length(categories);
        def_filtered_idx = 0;
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col3_x + 14, _col3_y + 96, _col3_w - 28, 26, "< " + category_names[def_cat_idx] + " >", _dc_hov, false, make_color_rgb(255, 120, 40));

    // Unit Carousel Navigation
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col3_x + 14, _col3_y + 130, "TARGET SELECTION (" + string(def_filtered_idx + 1) + " / " + string(array_length(_def_list)) + "):");

    var _dp_hov = (_mx >= _col3_x + 14 && _mx <= _col3_x + 70 && _my >= _col3_y + 148 && _my <= _col3_y + 176);
    if (_dp_hov && _click) {
        def_filtered_idx = (def_filtered_idx - 1 + array_length(_def_list)) % array_length(_def_list);
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col3_x + 14, _col3_y + 148, 56, 28, "< PREV", _dp_hov, false, c_white);

    var _dn_hov = (_mx >= _col3_x + _col3_w - 70 && _mx <= _col3_x + _col3_w - 14 && _my >= _col3_y + 148 && _my <= _col3_y + 176);
    if (_dn_hov && _click) {
        def_filtered_idx = (def_filtered_idx + 1) % array_length(_def_list);
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col3_x + _col3_w - 70, _col3_y + 148, 56, 28, "NEXT >", _dn_hov, false, c_white);

    // Unit Specification Card
    draw_set_color(make_color_rgb(28, 18, 16));
    draw_rectangle(_col3_x + 14, _col3_y + 186, _col3_x + _col3_w - 14, _col3_y + 440, false);
    draw_set_color(make_color_rgb(90, 45, 32));
    draw_rectangle(_col3_x + 14, _col3_y + 186, _col3_x + _col3_w - 14, _col3_y + 440, true);

    draw_set_color(make_color_rgb(255, 140, 40));
    draw_text_transformed(_col3_x + 22, _col3_y + 196, _cur_def.name, 0.95, 0.95, 0);

    draw_set_color(make_color_rgb(200, 170, 160));
    draw_text(_col3_x + 22, _col3_y + 226, "ID: " + _cur_def.id);
    draw_text(_col3_x + 22, _col3_y + 250, "FACTION: " + _cur_def.faction_id);
    draw_text(_col3_x + 22, _col3_y + 274, "CATEGORY: " + _cur_def.category);
    draw_text(_col3_x + 22, _col3_y + 298, "CHASSIS: " + string_upper(_cur_def.chassis));
    draw_text(_col3_x + 22, _col3_y + 322, "ALLOY: " + _cur_def.alloy);
    draw_text(_col3_x + 22, _col3_y + 346, "WEAPON: " + _cur_def.weapon_name);
    draw_text(_col3_x + 22, _col3_y + 370, "HULL: " + string(_cur_def.hp) + " HP");
    draw_text(_col3_x + 22, _col3_y + 394, "ARMOR: " + string(_cur_def.armor) + " RATING");

    // Defense Target Reticle Status
    draw_set_color(make_color_rgb(255, 80, 80));
    draw_text(_col3_x + 14, _col3_y + 474, "TARGET STATUS: LOCK ACQUIRED");
    draw_set_color(make_color_rgb(255, 140, 40));
    draw_text(_col3_x + 14, _col3_y + 524, "STANCE: DEFENDER TARGET (FACING LEFT)");

    // ---------------------------------------------------------------------
    // C. CENTER COLUMN: VISUAL STAGE & CLASH CONTROLS (w: 646)
    // ---------------------------------------------------------------------
    var _col2_x = _win_x + 322;
    var _col2_y = _win_y + 44;
    var _col2_w = 646;
    var _col2_h = 654;
    scr_draw_snes_panel(_col2_x, _col2_y, _col2_w, _col2_h, "BATTLE ANIMATION ENGINE PROVING GROUND", make_color_rgb(255, 200, 60), true, 0.03);

    // 1. Visual Stage Frame
    var _stg_x = _col2_x + 12;
    var _stg_y = _col2_y + 28;
    var _stg_w = _col2_w - 24;
    var _stg_h = 270;

    // Environmental Backdrop
    var _th = theaters[theater_idx];
    if (_th == "SPACE") {
        draw_rectangle_color(_stg_x, _stg_y, _stg_x + _stg_w, _stg_y + _stg_h, make_color_rgb(4, 7, 16), make_color_rgb(4, 7, 16), make_color_rgb(14, 22, 42), make_color_rgb(14, 22, 42), false);
        for (var i = 0; i < 30; i++) {
            var _sx = _stg_x + ((i * 77 + 23) % _stg_w);
            var _sy = _stg_y + ((i * 43 + 17) % _stg_h);
            draw_set_color(c_white);
            draw_point(_sx, _sy);
        }
    } else if (_th == "WATER") {
        draw_rectangle_color(_stg_x, _stg_y, _stg_x + _stg_w, _stg_y + _stg_h, make_color_rgb(8, 22, 40), make_color_rgb(12, 32, 54), make_color_rgb(5, 14, 26), make_color_rgb(6, 18, 32), false);
        draw_set_color(make_color_rgb(18, 55, 92));
        draw_rectangle(_stg_x, _stg_y + 200, _stg_x + _stg_w, _stg_y + _stg_h, false);
    } else if (_th == "SLAG") {
        draw_rectangle_color(_stg_x, _stg_y, _stg_x + _stg_w, _stg_y + _stg_h, make_color_rgb(32, 12, 8), make_color_rgb(42, 16, 10), make_color_rgb(18, 6, 4), make_color_rgb(22, 8, 6), false);
        draw_set_color(make_color_rgb(65, 22, 12));
        draw_rectangle(_stg_x, _stg_y + 190, _stg_x + _stg_w, _stg_y + _stg_h, false);
    } else {
        // Earth Badlands
        draw_rectangle_color(_stg_x, _stg_y, _stg_x + _stg_w, _stg_y + _stg_h, make_color_rgb(18, 14, 22), make_color_rgb(26, 20, 30), make_color_rgb(12, 8, 14), make_color_rgb(14, 10, 16), false);
        draw_set_color(make_color_rgb(32, 24, 30));
        draw_rectangle(_stg_x, _stg_y + 195, _stg_x + _stg_w, _stg_y + _stg_h, false);
    }

    // Border around stage
    draw_set_color(make_color_rgb(50, 75, 105));
    draw_rectangle(_stg_x, _stg_y, _stg_x + _stg_w, _stg_y + _stg_h, true);

    // CRT Scanline Overlay
    if (sprite_exists(spr_snes_crt_scanline)) {
        draw_sprite_tiled_ext(spr_snes_crt_scanline, 0, _stg_x, _stg_y, 1.0, 1.0, c_white, 0.10);
    }

    // Draw Live Attacker (Left)
    var _live_ax = _stg_x + 160;
    var _live_ay = _stg_y + 205;
    var _atk_st = anim_states[anim_state_idx];
    scr_draw_animated_mobile_suit(_cur_atk.id, _live_ax, _live_ay, 1.25, 1, _atk_st, subimg_atk, c_white, anim_perspective);

    // Draw Live Defender (Right)
    var _live_dx = _stg_x + _stg_w - 160;
    var _live_dy = _stg_y + 205;
    scr_draw_animated_mobile_suit(_cur_def.id, _live_dx, _live_dy, 1.25, -1, "idle", subimg_def, c_white, anim_perspective);

    // Reticle lock on defender
    var _rt_pulse = 0.7 + 0.3 * sin(current_time * 0.008);
    draw_set_color(make_color_rgb(255, 60, 60));
    draw_set_alpha(_rt_pulse);
    draw_circle(_live_dx, _live_dy - 55, 40, true);
    draw_line(_live_dx - 50, _live_dy - 55, _live_dx - 30, _live_dy - 55);
    draw_line(_live_dx + 30, _live_dy - 55, _live_dx + 50, _live_dy - 55);
    draw_line(_live_dx, _live_dy - 105, _live_dx, _live_dy - 85);
    draw_line(_live_dx, _live_dy - 25, _live_dx, _live_dy - 5);
    draw_set_alpha(1.0);

    // 2. Controls Section Below Stage
    var _ctrl_y = _stg_y + _stg_h + 14;

    // Theater Environment Buttons
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col2_x + 14, _ctrl_y, "THEATER ENVIRONMENT:");
    var _btn_tw = (_col2_w - 28 - 18) / 4;
    for (var th = 0; th < 4; th++) {
        var _bx = _col2_x + 14 + th * (_btn_tw + 6);
        var _th_hov = (_mx >= _bx && _mx <= _bx + _btn_tw && _my >= _ctrl_y + 18 && _my <= _ctrl_y + 44);
        var _is_cur_th = (theater_idx == th);
        if (_th_hov && _click) {
            theater_idx = th;
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_bx, _ctrl_y + 18, _btn_tw, 26, theaters[th], _th_hov || _is_cur_th, _is_cur_th, _is_cur_th ? make_color_rgb(0, 240, 255) : c_white);
    }

    // Animation State Scrubbing Controls
    var _ast_y = _ctrl_y + 54;
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col2_x + 14, _ast_y, "ANIMATION STATE SCRUBBING:");

    var _ap_hov = (_mx >= _col2_x + 14 && _mx <= _col2_x + 90 && _my >= _ast_y + 18 && _my <= _ast_y + 46);
    if (_ap_hov && _click) {
        anim_state_idx = (anim_state_idx - 1 + array_length(anim_states)) % array_length(anim_states);
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col2_x + 14, _ast_y + 18, 76, 28, "< PREV", _ap_hov, false, c_white);

    var _cur_st_name = "[ " + string_upper(anim_states[anim_state_idx]) + " ]";
    var _mid_w = _col2_w - 28 - 164;
    draw_set_color(make_color_rgb(20, 32, 48));
    draw_rectangle(_col2_x + 96, _ast_y + 18, _col2_x + 96 + _mid_w, _ast_y + 46, false);
    draw_set_color(make_color_rgb(45, 80, 120));
    draw_rectangle(_col2_x + 96, _ast_y + 18, _col2_x + 96 + _mid_w, _ast_y + 46, true);
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_col2_x + 110, _ast_y + 24, _cur_st_name);

    var _an_hov = (_mx >= _col2_x + _col2_w - 90 && _mx <= _col2_x + _col2_w - 14 && _my >= _ast_y + 18 && _my <= _ast_y + 46);
    if (_an_hov && _click) {
        anim_state_idx = (anim_state_idx + 1) % array_length(anim_states);
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col2_x + _col2_w - 90, _ast_y + 18, 76, 28, "NEXT >", _an_hov, false, c_white);

    // Playback Speed & Frame Stepping
    var _ply_y = _ast_y + 56;
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col2_x + 14, _ply_y, "PLAYBACK CONTROLS:");

    for (var sp = 0; sp < 4; sp++) {
        var _sp_x = _col2_x + 14 + sp * 65;
        var _sp_hov = (_mx >= _sp_x && _mx <= _sp_x + 60 && _my >= _ply_y + 18 && _my <= _ply_y + 44);
        var _is_cur_sp = (anim_speed_idx == sp);
        if (_sp_hov && _click) {
            anim_speed_idx = sp;
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_sp_x, _ply_y + 18, 60, 26, anim_speed_names[sp], _sp_hov || _is_cur_sp, _is_cur_sp, _is_cur_sp ? make_color_rgb(0, 240, 255) : c_white);
    }

    // Pause/Play
    var _pause_x = _col2_x + 285;
    var _pau_hov = (_mx >= _pause_x && _mx <= _pause_x + 95 && _my >= _ply_y + 18 && _my <= _ply_y + 44);
    if (_pau_hov && _click) {
        is_paused = !is_paused;
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_pause_x, _ply_y + 18, 95, 26, is_paused ? "PLAY >" : "PAUSE ||", _pau_hov, is_paused, is_paused ? c_yellow : c_white);

    // Step Frame
    var _step_x = _col2_x + 390;
    var _stp_hov = (_mx >= _step_x && _mx <= _step_x + 105 && _my >= _ply_y + 18 && _my <= _ply_y + 44);
    if (_stp_hov && _click) {
        step_frame_req = true;
        is_paused = true;
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_step_x, _ply_y + 18, 105, 26, "STEP FRAME >", _stp_hov, false, c_white);

    // Audio SFX Test
    var _sfx_x = _col2_x + 505;
    var _sfx_hov = (_mx >= _sfx_x && _mx <= _sfx_x + 127 && _my >= _ply_y + 18 && _my <= _ply_y + 44);
    if (_sfx_hov && _click) {
        scr_audio_play_weapon(weapon_classes[weapon_idx]);
    }
    scr_draw_snes_button(_sfx_x, _ply_y + 18, 127, 26, "TEST SFX", _sfx_hov, false, make_color_rgb(255, 200, 60));

    // Weapon Class Selector
    var _wpn_y = _ply_y + 54;
    draw_set_color(make_color_rgb(140, 180, 220));
    draw_text(_col2_x + 14, _wpn_y, "WEAPON CLASS CHOREOGRAPHY:");

    var _w_btn_w = _col2_w - 28;
    var _wpn_hov = (_mx >= _col2_x + 14 && _mx <= _col2_x + 14 + _w_btn_w && _my >= _wpn_y + 18 && _my <= _wpn_y + 44);
    if (_wpn_hov && _click) {
        weapon_idx = (weapon_idx + 1) % array_length(weapon_classes);
        scr_audio_play_ui("click");
    }
    scr_draw_snes_button(_col2_x + 14, _wpn_y + 18, _w_btn_w, 26, "< WEAPON: " + weapon_names[weapon_idx] + " (" + weapon_classes[weapon_idx] + ") >", _wpn_hov, false, make_color_rgb(255, 200, 60));

    // 3. Huge Tactile Cinematic Clash Launcher Button
    var _lch_y = _wpn_y + 56;
    var _lch_w = _col2_w - 28;
    var _lch_h = 52;
    var _lch_hov = (_mx >= _col2_x + 14 && _mx <= _col2_x + 14 + _lch_w && _my >= _lch_y && _my <= _lch_y + _lch_h);

    var _pulse = 0.5 + 0.5 * sin(current_time * 0.008);
    var _border_col = merge_color(make_color_rgb(0, 240, 255), make_color_rgb(255, 180, 40), _pulse);

    if (_lch_hov && _click) {
        launch_full_cinematic_clash();
    }
    scr_draw_snes_button(_col2_x + 14, _lch_y, _lch_w, _lch_h, ">>>> LAUNCH FULL CINEMATIC CLASH DUEL <<<<", _lch_hov, true, _border_col);
}
// =========================================================================
// TAB 1: PMC CAMPAIGN CHEATS & SYSTEM TOOLS
// =========================================================================
else if (active_debug_tab == 1) {
    var _sec_w = (_win_w - 42) / 2;
    var _sec_h = (_win_h - 64) / 2;

    // Quadrant 1: Treasury & Metallurgy
    var _q1_x = _win_x + 14;
    var _q1_y = _win_y + 44;
    scr_draw_snes_panel(_q1_x, _q1_y, _sec_w, _sec_h, "PMC TREASURY & SINTERED METALLURGY", make_color_rgb(0, 240, 255), true, 0.03);

    var _funds = (instance_exists(obj_GameManager)) ? obj_GameManager.funds : 0;
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_text(_q1_x + 18, _q1_y + 30, "CURRENT PMC FUNDS: " + string(_funds) + " CREDITS");

    var _c1_hov = (_mx >= _q1_x + 18 && _mx <= _q1_x + _sec_w - 18 && _my >= _q1_y + 60 && _my <= _q1_y + 92);
    if (_c1_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            obj_GameManager.funds += 100000;
            show_toast("[CHEAT ACTIVE] +100,000 Credits Added to Treasury!", c_lime);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q1_x + 18, _q1_y + 60, _sec_w - 36, 32, "[+] ADD +100,000 CREDITS", _c1_hov, false, c_lime);

    var _c2_hov = (_mx >= _q1_x + 18 && _mx <= _q1_x + _sec_w - 18 && _my >= _q1_y + 102 && _my <= _q1_y + 134);
    if (_c2_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            obj_GameManager.funds += 1000000;
            show_toast("[CHEAT ACTIVE] +1,000,000 Credits Added to Treasury!", c_lime);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q1_x + 18, _q1_y + 102, _sec_w - 36, 32, "[+] ADD +1,000,000 CREDITS", _c2_hov, false, c_lime);

    var _c3_hov = (_mx >= _q1_x + 18 && _mx <= _q1_x + _sec_w - 18 && _my >= _q1_y + 144 && _my <= _q1_y + 176);
    if (_c3_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            var _alloys = ["alloy_vanguard_comp", "alloy_hyperion_matrix", "alloy_aerosteel_flux", "alloy_adamantine_carbide", "alloy_tachyon_superalloy"];
            for (var a = 0; a < array_length(_alloys); a++) {
                obj_GameManager.add_alloy(_alloys[a], 500);
            }
            show_toast("[CHEAT ACTIVE] +500 All 5 Metallurgy Sintered Alloys Added!", c_aqua);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q1_x + 18, _q1_y + 144, _sec_w - 36, 32, "[+] ADD +500 ALL CANON ALLOYS (ALL 5 TIERS)", _c3_hov, false, make_color_rgb(0, 240, 255));

    var _c4_hov = (_mx >= _q1_x + 18 && _mx <= _q1_x + _sec_w - 18 && _my >= _q1_y + 186 && _my <= _q1_y + 218);
    if (_c4_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            var _mats = ["mat_tungsten", "mat_silica_carb", "mat_tritium", "mat_syn_flux", "mat_osmium"];
            for (var m = 0; m < array_length(_mats); m++) {
                obj_GameManager.add_alloy(_mats[m], 2000);
            }
            show_toast("[CHEAT ACTIVE] +2,000 Raw Periodic Minerals Added!", c_aqua);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q1_x + 18, _q1_y + 186, _sec_w - 36, 32, "[+] ADD +2,000 RAW MATERIALS (TUNGSTEN / TRITIUM / SILICA)", _c4_hov, false, make_color_rgb(0, 240, 255));

    // Quadrant 2: R&D, Blueprints & Tech Tree
    var _q2_x = _win_x + 14 + _sec_w + 14;
    var _q2_y = _win_y + 44;
    scr_draw_snes_panel(_q2_x, _q2_y, _sec_w, _sec_h, "R&D, BLUEPRINTS & HOI4 RESEARCH", make_color_rgb(255, 200, 60), true, 0.03);

    var _b1_hov = (_mx >= _q2_x + 18 && _mx <= _q2_x + _sec_w - 18 && _my >= _q2_y + 60 && _my <= _q2_y + 92);
    if (_b1_hov && _click) {
        if (instance_exists(obj_BlueprintManager)) {
            if (is_array(obj_BlueprintManager.all_blueprint_list)) {
                for (var b = 0; b < array_length(obj_BlueprintManager.all_blueprint_list); b++) {
                    var _bp = obj_BlueprintManager.all_blueprint_list[b];
                    if (is_struct(_bp)) variable_struct_set(obj_BlueprintManager.unlocked_blueprints, _bp.id, _bp);
                }
            }
            if (is_struct(obj_BlueprintManager.unlocked_recipes)) {
                var _r_names = variable_struct_get_names(obj_BlueprintManager.unlocked_recipes);
                for (var r = 0; r < array_length(_r_names); r++) {
                    var _rc = variable_struct_get(obj_BlueprintManager.unlocked_recipes, _r_names[r]);
                    if (is_struct(_rc)) _rc.unlocked = true;
                }
            }
            show_toast("[CHEAT ACTIVE] All 100 Blueprints & Sintering Recipes Unlocked!", c_yellow);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q2_x + 18, _q2_y + 60, _sec_w - 36, 32, "[*] UNLOCK ALL 100 CANON BLUEPRINTS & RECIPES", _b1_hov, false, make_color_rgb(255, 200, 60));

    var _b2_hov = (_mx >= _q2_x + 18 && _mx <= _q2_x + _sec_w - 18 && _my >= _q2_y + 102 && _my <= _q2_y + 134);
    if (_b2_hov && _click) {
        var _res_sys = scr_research_get_system();
        if (!is_undefined(_res_sys) && is_struct(_res_sys)) {
            var _slots = _res_sys.active_slots;
            for (var s = 0; s < array_length(_slots); s++) {
                if (_slots[s].tech_id != "") _slots[s].turns_left = 0;
            }
            scr_research_advance_turn();
            show_toast("[CHEAT ACTIVE] Active Research Progress Completed!", c_lime);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q2_x + 18, _q2_y + 102, _sec_w - 36, 32, "[*] INSTANT COMPLETE ACTIVE RESEARCH (TURN ADVANCE)", _b2_hov, false, make_color_rgb(255, 200, 60));

    var _b3_hov = (_mx >= _q2_x + 18 && _mx <= _q2_x + _sec_w - 18 && _my >= _q2_y + 144 && _my <= _q2_y + 176);
    if (_b3_hov && _click) {
        var _res_sys = scr_research_get_system();
        if (!is_undefined(_res_sys) && is_struct(_res_sys)) {
            var _tech_db = scr_research_get_tech_db();
            if (is_struct(_tech_db)) {
                var _t_keys = variable_struct_get_names(_tech_db);
                for (var k = 0; k < array_length(_t_keys); k++) {
                    var _tid = _t_keys[k];
                    if (!scr_research_is_unlocked(_tid)) array_push(_res_sys.unlocked_techs, _tid);
                }
            }
            show_toast("[CHEAT ACTIVE] Entire HOI4 R&D Tech Tree Unlocked!", c_yellow);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q2_x + 18, _q2_y + 144, _sec_w - 36, 32, "[*] UNLOCK ALL TECH NODES (ENTIRE HOI4 TREE)", _b3_hov, false, make_color_rgb(255, 200, 60));

    // Quadrant 3: Narrative & Crisis Incursions
    var _q3_x = _win_x + 14;
    var _q3_y = _win_y + 44 + _sec_h + 10;
    scr_draw_snes_panel(_q3_x, _q3_y, _sec_w, _sec_h, "NARRATIVE & CRISIS INCURSIONS", make_color_rgb(255, 120, 40), true, 0.03);

    var _n1_hov = (_mx >= _q3_x + 18 && _mx <= _q3_x + _sec_w - 18 && _my >= _q3_y + 50 && _my <= _q3_y + 82);
    if (_n1_hov && _click) {
        scr_vn_start_episode("ep_00_cabin_discovery");
        is_open = false;
        scr_audio_play_ui("confirm");
    }
    scr_draw_snes_button(_q3_x + 18, _q3_y + 50, _sec_w - 36, 32, "[>] TRIGGER EPISODE 00: CABIN DISCOVERY (VN)", _n1_hov, false, make_color_rgb(255, 120, 40));

    var _n2_hov = (_mx >= _q3_x + 18 && _mx <= _q3_x + _sec_w - 18 && _my >= _q3_y + 92 && _my <= _q3_y + 124);
    if (_n2_hov && _click) {
        scr_vn_start_episode("ep_01_inauguration");
        is_open = false;
        scr_audio_play_ui("confirm");
    }
    scr_draw_snes_button(_q3_x + 18, _q3_y + 92, _sec_w - 36, 32, "[>] TRIGGER EPISODE 01: INAUGURATION (VN)", _n2_hov, false, make_color_rgb(255, 120, 40));

    var _n3_hov = (_mx >= _q3_x + 18 && _mx <= _q3_x + _sec_w - 18 && _my >= _q3_y + 134 && _my <= _q3_y + 166);
    if (_n3_hov && _click) {
        if (instance_exists(obj_BattleManager)) {
            obj_BattleManager.nemesis_incursion_turn = obj_BattleManager.turn_number;
            obj_BattleManager.nemesis_incursion_checked = false;
            show_toast("[CHEAT ACTIVE] Nemesis Drop-Pod Ambush Forced on Current Combat Turn!", c_orange);
        } else {
            show_toast("[NOTE] Nemesis Ambush will trigger immediately upon entering combat!", c_yellow);
        }
        scr_audio_play_ui("confirm");
    }
    scr_draw_snes_button(_q3_x + 18, _q3_y + 134, _sec_w - 36, 32, "[!] FORCE NEMESIS DROP-POD AMBUSH NEXT COMBAT", _n3_hov, false, c_red);

    // Quadrant 4: Engine Diagnostics & Settings
    var _q4_x = _win_x + 14 + _sec_w + 14;
    var _q4_y = _win_y + 44 + _sec_h + 10;
    scr_draw_snes_panel(_q4_x, _q4_y, _sec_w, _sec_h, "ENGINE DIAGNOSTICS & DISPLAY", make_color_rgb(140, 200, 255), true, 0.03);

    var _d1_hov = (_mx >= _q4_x + 18 && _mx <= _q4_x + _sec_w - 18 && _my >= _q4_y + 50 && _my <= _q4_y + 82);
    if (_d1_hov && _click) {
        var _m = scr_audio_toggle_mute();
        show_toast(_m ? "[AUDIO MUTED]" : "[AUDIO UNMUTED]", _m ? c_orange : c_lime);
    }
    scr_draw_snes_button(_q4_x + 18, _q4_y + 50, _sec_w - 36, 32, "[~] TOGGLE GLOBAL AUDIO MUTE", _d1_hov, false, c_white);

    var _d2_hov = (_mx >= _q4_x + 18 && _mx <= _q4_x + _sec_w - 18 && _my >= _q4_y + 92 && _my <= _q4_y + 124);
    if (_d2_hov && _click) {
        if (instance_exists(obj_GameManager)) {
            obj_GameManager.end_turn();
            show_toast("[ADVANCED TURN] Strategic World Map Turn Processed!", c_aqua);
            scr_audio_play_ui("confirm");
        }
    }
    scr_draw_snes_button(_q4_x + 18, _q4_y + 92, _sec_w - 36, 32, "[~] ADVANCE GLOBAL STRATEGIC TURN", _d2_hov, false, c_white);

    var _d3_hov = (_mx >= _q4_x + 18 && _mx <= _q4_x + _sec_w - 18 && _my >= _q4_y + 134 && _my <= _q4_y + 166);
    if (_d3_hov && _click) {
        show_debug_message("[DEBUG] Master Roster Count: " + string(array_length(master_roster)));
        show_toast("[TELEMETRY] DUMPED 100+ UNITS TO DEBUG CONSOLE", c_lime);
        scr_audio_play_ui("confirm");
    }
    scr_draw_snes_button(_q4_x + 18, _q4_y + 134, _sec_w - 36, 32, "[?] PRINT CATALOG TELEMETRY TO DEBUG LOG", _d3_hov, false, c_white);
}

// Glowing Notification Toast
if (debug_toast_timer > 0) {
    var _t_alpha = min(1.0, debug_toast_timer / 30.0);
    draw_set_alpha(_t_alpha);
    draw_set_color(make_color_rgb(14, 22, 34));
    draw_rectangle(_win_x + 20, _win_y + _win_h - 44, _win_x + _win_w - 20, _win_y + _win_h - 10, false);
    draw_set_color(debug_toast_color);
    draw_rectangle(_win_x + 20, _win_y + _win_h - 44, _win_x + _win_w - 20, _win_y + _win_h - 10, true);
    draw_text(_win_x + 36, _win_y + _win_h - 34, debug_toast);
    draw_set_alpha(1.0);
}
"""

with open("objects/obj_DebugManager/Draw_64.gml", "w", encoding="utf-8") as f:
    f.write(draw_code)
print("[PASS] 5. Draw_64.gml generated.")

print("\n=== OBJ_DEBUGMANAGER CREATION FINISHED ===")
