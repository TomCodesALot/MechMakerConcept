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
is_open = true;
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

// 3. Populate Comprehensive Unit Catalog Roster from Authoritative Central Database
master_roster = scr_ms_db_get_roster();
show_debug_message("[obj_DebugManager] Master unit catalog indexed from Central Database: " + string(array_length(master_roster)) + " total units.");

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

weapon_classes = ["BALLISTIC", "ROTARY_VULCAN", "BEAM_PULSE", "MICRO_MISSILE", "MELEE", "BEAM_LANCE"];
weapon_names = ["Type-77 120mm Solid Cannon", "GAU-88 Rotary Heavy Vulcan", "Coherent Beam Pulse Rifle", "Ares Swarm-16 Micro-Missiles", "Hydraulic Gun-Club Strike", "Twin Forearm Plasma Lances"];
weapon_idx = 0;
atk_prev_unit_id = "";

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
    atk_subimg: -1,
    def_subimg: -1,
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
    if (_atk_u.category != "CUSTOM_MECH") {
        if (_w_class == _atk_u.weapon_class) {
            _w_name = _atk_u.weapon_name;
        } else if (_w_class == "MELEE") {
            _w_name = (variable_struct_exists(_atk_u, "weapon_overlay_secondary") && _atk_u.weapon_overlay_secondary != "") ? _atk_u.weapon_overlay_secondary : "Hydraulic Shoulder Tackle & Strike";
        }
    }

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
    clash_cinematic.atk_subimg = -1;
    clash_cinematic.def_subimg = -1;
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
