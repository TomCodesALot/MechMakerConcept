/// @description obj_DebugManager Create Event
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

var _add_unit = function(_id, _name, _fac, _cat, _chassis, _alloy, _spr, _weapon, _hp, _armor, _wpn_prim = "", _wpn_sec = "", _era = 2, _doctrine = "") {
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
        armor: _armor,
        weapon_overlay_primary: _wpn_prim,
        weapon_overlay_secondary: _wpn_sec,
        era: _era,
        doctrine: _doctrine
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
                    30,
                    variable_struct_get(_s, "weapon_overlay_primary") ?? "",
                    variable_struct_get(_s, "weapon_overlay_secondary") ?? "",
                    variable_struct_get(_s, "era") ?? 2,
                    variable_struct_get(_s, "doctrine") ?? ""
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

// 3c. Conventional Force Vehicles - 4 Factions x 3 Vehicle Archetypes (Tank, Gunship, Fighter)
// Terran Confederation (faction_a)
_add_unit("veh_terran_mammoth", "T-720 Mammoth Heavy Battle Tank", "faction_a", "VEHICLE", "tread", "alloy_vanguard_comp", "spr_veh_terran_mammoth_idle", "Dual 150mm Siege Cannons", 520, 35, "", "", 1, "HEAVY_BALLISTIC");
_add_unit("veh_terran_skyhammer", "UH-44 Skyhammer Heavy Gunship", "faction_a", "VEHICLE", "aero", "alloy_vanguard_comp", "spr_veh_terran_skyhammer_idle", "GAU-88 30mm Rotary Vulcan", 380, 18, "", "", 1, "CLOSE_AIR_SUPPORT");
_add_unit("veh_terran_sabre", "A-14 Sabre Heavy Strike Jet", "faction_a", "VEHICLE", "aero", "alloy_vanguard_comp", "spr_veh_terran_sabre_idle", "AGM-88 Swarm Strike Missiles", 340, 16, "", "", 1, "AIR_SUPERIORITY");
// Outer Colony League (faction_b)
_add_unit("veh_colony_stiletto", "K-4 Stiletto Rapid Attack Skimmer", "faction_b", "VEHICLE", "hover", "alloy_aerosteel_flux", "spr_veh_colony_stiletto_idle", "Coherent Beam Carbine", 310, 15, "", "", 1, "ENERGY_SKIRMISHER");
_add_unit("veh_colony_gunship", "V-88 Valkyrie Heavy Tilt-Rotor", "faction_b", "VEHICLE", "aero", "alloy_aerosteel_flux", "spr_veh_colony_gunship_idle", "Thermal Beam Cannon", 380, 20, "", "", 1, "AEROSPACE_GUNSHIP");
_add_unit("veh_colony_dart", "S-10 Dart Hypersonic Interceptor", "faction_b", "VEHICLE", "aero", "alloy_aerosteel_flux", "spr_veh_colony_dart_idle", "Micro-Missile Salvo", 290, 14, "", "", 1, "INTERCEPTOR");
// Rogue Syndicate (faction_c)
_add_unit("veh_syndicate_technical", "SCR-T01 Rustfang Flak Technical", "faction_c", "VEHICLE", "wheeled", "alloy_adamantine_carbide", "spr_veh_syndicate_technical_idle", "Heavy Twin Flak Cannon", 300, 14, "", "", 1, "FLAK_SUPPORT");
_add_unit("veh_syndicate_chopper", "H-09 Buzzsaw Scrap Chopper", "faction_c", "VEHICLE", "aero", "alloy_adamantine_carbide", "spr_veh_syndicate_chopper_idle", "Twin 23mm Rotary Autocannon", 320, 14, "", "", 1, "RAID_CHOPPER");
_add_unit("veh_syndicate_bomber", "SCR-B03 Buzzard Light Bomber", "faction_c", "VEHICLE", "aero", "alloy_adamantine_carbide", "spr_veh_syndicate_bomber_idle", "Incendiary Slag Cluster", 300, 16, "", "", 1, "TACTICAL_BOMBER");
// Omni-Corp Zaibatsu (faction_d)
_add_unit("veh_zaibatsu_kurogane", "Type-94 Kurogane Drone Tank", "faction_d", "VEHICLE", "hover", "alloy_tachyon_superalloy", "spr_veh_zaibatsu_kurogane_idle", "Railgun Point Defense", 580, 28, "", "", 1, "AUTOMATED_DEFENSE");
_add_unit("veh_zaibatsu_rotor", "Type-07 Shinobi Ducted VTOL", "faction_d", "VEHICLE", "aero", "alloy_tachyon_superalloy", "spr_veh_zaibatsu_rotor_idle", "Twin Pulse Laser Emitters", 350, 18, "", "", 1, "STEALTH_INFILTRATION");
_add_unit("veh_zaibatsu_drone_jet", "Type-02 Kamaitachi Stealth Drone", "faction_d", "VEHICLE", "aero", "alloy_tachyon_superalloy", "spr_veh_zaibatsu_drone_jet_idle", "Plasma Beam Emitter", 270, 14, "", "", 1, "STEALTH_STRIKE");

// 3d. Conventional Infantry Squads - 4 Factions x 1 Bespoke Squad (Doc 38)
_add_unit("inf_terran_squad", "Terran 88th Grenadier Platoon", "faction_a", "INFANTRY", "infantry", "alloy_vanguard_comp", "spr_inf_terran_squad_idle", "Anti-Armor Rocket Volley", 180, 8, "", "", 1, "URBAN_GRENADIERS");
_add_unit("inf_colony_squad", "Colony Void Jump Skirmishers", "faction_b", "INFANTRY", "infantry", "alloy_aerosteel_flux", "spr_inf_colony_squad_idle", "Plasma Rifle Saturation", 150, 6, "", "", 1, "VOID_SKIRMISHERS");
_add_unit("inf_syndicate_squad", "Rust Syndicate Marauder Squad", "faction_c", "INFANTRY", "infantry", "alloy_adamantine_carbide", "spr_inf_syndicate_squad_idle", "Magnetic Harpoon & Charges", 160, 7, "", "", 1, "SCRAP_MARAUDERS");
_add_unit("inf_zaibatsu_squad", "Zaibatsu Spec-Ops Androids", "faction_d", "INFANTRY", "infantry", "alloy_tachyon_superalloy", "spr_inf_zaibatsu_squad_idle", "Monoblades & Flechettes", 170, 10, "", "", 1, "CYBERNETIC_SPEC_OPS");
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
