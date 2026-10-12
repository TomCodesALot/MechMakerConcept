/// @description obj_BattleManager Create Event
// Turn-Based Tactical Combat System Singleton
// Strictly implements docs/05_tactical_combat.md

show_debug_message("[obj_BattleManager] Initializing Turn-Based Tactical Combat Arena...");

// Bootstrap persistent managers if booting directly into combat room
if (!instance_exists(obj_GameManager)) instance_create_depth(0, 0, 0, obj_GameManager);
if (!instance_exists(obj_FactionManager)) instance_create_depth(0, 0, 0, obj_FactionManager);
if (!instance_exists(obj_BlueprintManager)) instance_create_depth(0, 0, 0, obj_BlueprintManager);

// 1. Combat State Machine Enums & Variables
enum COMBAT_STATE {
    PLAYER_PHASE,
    MOVE_MODE,
    TARGET_MODE,
    ATTACK_EXECUTION,
    AI_PHASE,
    VICTORY_AAR,
    DEFEAT_AAR
}

state = COMBAT_STATE.PLAYER_PHASE;
state_timer = 0;
turn_number = 1;
screen_shake = 0.0;

// 2. Tactical Grid Dimensions (13 Cols x 7 Rows, 64px cells)
grid_cols = 13;
grid_rows = 7;
cell_size = 64;
grid_ox = 64;
grid_oy = 110;

// Grid Terrain & Cover Map (0 = Plain, 1 = Heavy Titanium Rubble [+20% Cover])
grid_terrain = array_create(grid_cols);
for (var c = 0; c < grid_cols; c++) {
    grid_terrain[c] = array_create(grid_rows, 0);
}
// Place tactical cover barricades
grid_terrain[4][2] = 1;
grid_terrain[4][4] = 1;
grid_terrain[8][2] = 1;
grid_terrain[8][4] = 1;

// Grid Coordinate Helper Functions
grid_to_world_x = function(_c) { return grid_ox + _c * cell_size + cell_size / 2; };
grid_to_world_y = function(_r) { return grid_oy + _r * cell_size + cell_size / 2; };
world_to_grid_c = function(_x) { return floor((_x - grid_ox) / cell_size); };
world_to_grid_r = function(_y) { return floor((_y - grid_oy) / cell_size); };

// 3. Selection & Hover State
hover_c = -1;
hover_r = -1;
selected_weapon = 0; // 0 = 120mm Cannon, 1 = GAU-88 Vulcan, 2 = Swarm-16, 3 = Gun-Club Strike
valid_move_tiles = [];
valid_target_tiles = [];

// 4. Weapons Database (docs/05)
weapons = [
    {
        name: "Type-77 120mm Solid-Slug Cannon",
        short_name: "120MM CANNON",
        ap_cost: 3,
        heat_cost: 15,
        range_min: 1,
        range_max: 6,
        damage: 145,
        req_part: "arm_left",
        damage_type: DAMAGE_TYPE.KINETIC,
        anim_state: MS_STATE.FIRE_RIFLE,
        desc: "High-velocity kinetic AP shell. High armor penetration at medium range."
    },
    {
        name: "GAU-88 Heavy Vulcan Rotary",
        short_name: "GAU-88 VULCAN",
        ap_cost: 2,
        heat_cost: 10,
        range_min: 1,
        range_max: 4,
        damage: 126, // 3x 42 burst
        req_part: "arm_right",
        damage_type: DAMAGE_TYPE.KINETIC,
        anim_state: MS_STATE.FIRE_CHAINGUN,
        desc: "Rotary ballistic burst. Low AP cost, effective at close-to-medium range."
    },
    {
        name: "Ares Swarm-16 Micro-Missiles",
        short_name: "ARES MISSILES",
        ap_cost: 4,
        heat_cost: 35,
        range_min: 2,
        range_max: 8,
        damage: 190, // 4x 48 salvo
        req_part: "backpack",
        damage_type: DAMAGE_TYPE.ROCKET,
        anim_state: MS_STATE.FIRE_MISSILES,
        desc: "Indirect-fire guided missile volley. High damage and range, heavy heat generation."
    },
    {
        name: "Type-77 Gun-Club Battering Strike",
        short_name: "GUN-CLUB MELEE",
        ap_cost: 3,
        heat_cost: 12,
        range_min: 1,
        range_max: 1,
        damage: 280,
        req_part: "arm_left",
        damage_type: DAMAGE_TYPE.MELEE,
        anim_state: MS_STATE.ATTACK_MELEE,
        desc: "Brutal kinetic war-club strike using reinforced 14.5t cannon breech. Devastating close-range blunt force."
    }
];

// 5. Units Initialization
// --- Player Unit (Vanguard Ace) ---
var _p_name = "Lt. Marcus Vance";
var _p_acc = 88;
var _p_ref = 75;
if (instance_exists(obj_GameManager) && array_length(obj_GameManager.facilities.roster_pilots) > 0) {
    var _pilot_obj = obj_GameManager.facilities.roster_pilots[0];
    _p_name = _pilot_obj.name;
    _p_acc = _pilot_obj.accuracy;
    _p_ref = _pilot_obj.reflexes;
}

player_unit = {
    callsign: "IRON-01 'WARHAMMER'",
    pilot_name: _p_name,
    is_player: true,
    grid_c: 2,
    grid_r: 3,
    visual_x: grid_to_world_x(2),
    visual_y: grid_to_world_y(3),
    facing: 1,
    max_ap: 6,
    current_ap: 6,
    current_heat: 0.0,
    max_heat: 100.0,
    heat_dissipation: 35.0,
    braced: false,
    accuracy: _p_acc,
    evasion: _p_ref,
    components: {
        torso:    { name: "Hyperion Fusion Core", cur: 650, max: 650, intact: true },
        head:     { name: "Target-Lock Sensors",  cur: 160, max: 160, intact: true },
        arm_left: { name: "120mm Cannon Mount",   cur: 400, max: 400, intact: true },
        arm_right:{ name: "GAU-88 Vulcan Mount",  cur: 400, max: 400, intact: true },
        legs:     { name: "Colossus Hydraulics",  cur: 650, max: 650, intact: true },
        backpack: { name: "Ares Ordnance Pack",   cur: 220, max: 220, intact: true }
    },
    sprite_index: spr_ms_ironclad_idle,
    image_index: 0,
    image_blend: c_white,
    recoil_x: 0,
    recoil_y: 0,
    recoil_shake: 0,
    state: MS_STATE.IDLE,
    state_timer: 0,
    is_destroyed: false
};

// --- Enemy Unit (Syndicate Outlaw Reaver) ---
enemy_unit = {
    callsign: "OUTLAW GHA-07 'REAVER'",
    pilot_name: "Rogue Ace 'Viper'",
    is_player: false,
    grid_c: 10,
    grid_r: 3,
    visual_x: grid_to_world_x(10),
    visual_y: grid_to_world_y(3),
    facing: -1,
    max_ap: 5,
    current_ap: 5,
    current_heat: 0.0,
    max_heat: 100.0,
    heat_dissipation: 30.0,
    braced: false,
    accuracy: 72,
    evasion: 55,
    components: {
        torso:    { name: "Stripped Core",        cur: 580, max: 580, intact: true },
        head:     { name: "Pirate Sensors",       cur: 140, max: 140, intact: true },
        arm_left: { name: "Captured Autocannon",  cur: 380, max: 380, intact: true },
        arm_right:{ name: "Vulcan Arm",           cur: 380, max: 380, intact: true },
        legs:     { name: "Heavy Bipedal Limbs",  cur: 580, max: 580, intact: true },
        backpack: { name: "Auxiliary Booster",    cur: 200, max: 200, intact: true }
    },
    sprite_index: spr_ms_ironclad_idle,
    image_index: 0,
    image_blend: make_color_rgb(255, 130, 130), // Crimson Syndicate Warpaint
    recoil_x: 0,
    recoil_y: 0,
    recoil_shake: 0,
    state: MS_STATE.IDLE,
    state_timer: 0,
    is_destroyed: false
};

// 6. Tactical Combat Terminal Feed Log
combat_log = [
    "TACTICAL ENGAGEMENT: SECTOR 4 MINING CLAIM PERIMETER",
    "Hostile Mobile Suit Detected: Syndicate GHA-07 Reaver",
    ">> COMMANDER: Manage Action Points (AP) and target specific enemy limbs!"
];

add_log = function(_msg) {
    array_push(combat_log, _msg);
    if (array_length(combat_log) > 6) {
        array_delete(combat_log, 0, 1);
    }
};

// 7. Tactical Math Helper Functions
calculate_distance = function(_c1, _r1, _c2, _r2) {
    return abs(_c1 - _c2) + abs(_r1 - _r2);
};

calculate_hit_chance = function(_attacker, _defender, _dist) {
    var _base_acc = _attacker.accuracy;
    var _evasion = _defender.evasion;
    if (_defender.braced) _evasion += 35;
    if (! _attacker.components.head.intact) _base_acc -= 40; // Head destroyed accuracy penalty
    if (! _defender.components.legs.intact) _evasion = 0;   // Crippled legs 0% evasion
    var _cover = (grid_terrain[_defender.grid_c][_defender.grid_r] == 1) ? 20 : 0;
    return clamp(_base_acc - _evasion * 0.45 - _cover - (_dist * 2), 20, 95);
};

// Recompute Valid Move Tiles within AP
recalculate_moves = function() {
    valid_move_tiles = [];
    if (player_unit.current_ap <= 0 || player_unit.is_destroyed) return;
    var _max_steps = player_unit.components.legs.intact ? player_unit.current_ap : 1;
    for (var c = 0; c < grid_cols; c++) {
        for (var r = 0; r < grid_rows; r++) {
            // Cannot occupy enemy tile
            if (c == enemy_unit.grid_c && r == enemy_unit.grid_r) continue;
            if (c == player_unit.grid_c && r == player_unit.grid_r) continue;
            var _d = calculate_distance(player_unit.grid_c, player_unit.grid_r, c, r);
            if (_d <= _max_steps) {
                array_push(valid_move_tiles, { col: c, row: r, cost: _d });
            }
        }
    }
};

// Attack Execution Queue
pending_attack = {
    attacker: undefined,
    defender: undefined,
    weapon_index: 0,
    hit_chance: 0,
    timer: 0
};

// Floating Combat Text System (docs/05)
floating_texts = [];
add_floating_text = function(_x, _y, _txt, _col) {
    array_push(floating_texts, {
        x: _x,
        y: _y,
        text: _txt,
        color: _col,
        alpha: 1.0,
        timer: 55,
        vy: -1.2
    });
};

// Pilot Permadeath & Casualty Status (docs/05, 07)
casualty_data = {
    pilot_ejected: false,
    pilot_survived: false,
    pilot_kia: false,
    pilot_name: _p_name,
    med_fee: 15000,
    processed: false
};

show_debug_message("[obj_BattleManager] Tactical Arena ready. Phase: PLAYER_PHASE.");
