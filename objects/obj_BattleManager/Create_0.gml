/// @description obj_BattleManager Create Event
// Grand-Scale Turn-Based Isometric Tactical Combat Arena
// Strictly implements docs/17_grand_scale_isometric_combat_system.md & docs/05_tactical_combat.md

show_debug_message("[obj_BattleManager] Initializing Grand-Scale Isometric Battle System...");

// 1. Bootstrap Persistent Managers if directly testing rm_combat
if (!instance_exists(obj_GameManager)) instance_create_depth(0, 0, 0, obj_GameManager);
if (!instance_exists(obj_FactionManager)) instance_create_depth(0, 0, 0, obj_FactionManager);
if (!instance_exists(obj_BlueprintManager)) instance_create_depth(0, 0, 0, obj_BlueprintManager);

// 2. Combat State Machine Enums & Variables
enum COMBAT_STATE {
    PLAYER_PHASE,
    MOVE_MODE,
    TARGET_MODE,
    ATTACK_EXECUTION,
    AI_PHASE,
    AUTO_SIM,
    VICTORY_AAR,
    DEFEAT_AAR
}

state = COMBAT_STATE.PLAYER_PHASE;
state_timer = 0;
turn_number = 1;
screen_shake = 0.0;
auto_combat_enabled = false;
auto_combat_timer = 0;
ai_action_timer = 0;
ai_unit_index = 0;

// 3. Isometric Battlefield Dimensions (20 Cols x 20 Rows)
grid_cols = 20;
grid_rows = 20;
tile_w = 64.0;
tile_h = 32.0;
elev_h = 16.0;

// Elevation Grid (0 = Ground, 1 = Elevated Ridge, 2 = Command Bunker Plateau)
grid_elev = array_create(grid_cols);
for (var c = 0; c < grid_cols; c++) {
    grid_elev[c] = array_create(grid_rows, 0);
    for (var r = 0; r < grid_rows; r++) {
        // Natural ridge plateau in central region
        if (c >= 6 && c <= 13 && r >= 6 && r <= 13) {
            grid_elev[c][r] = 1;
        }
        // Fortress observation mound in center
        if (c >= 9 && c <= 10 && r >= 9 && r <= 10) {
            grid_elev[c][r] = 2;
        }
    }
}

// Cover Obstacles (0 = Open, 1 = Titanium Barricade [+25% Cover], 2 = Hardened Bunker Blast Wall [+40% Cover])
grid_cover = array_create(grid_cols);
for (var c = 0; c < grid_cols; c++) {
    grid_cover[c] = array_create(grid_rows, 0);
}
// Barricades along trenches and approach choke points
grid_cover[5][5] = 1; grid_cover[5][6] = 1; grid_cover[6][5] = 1;
grid_cover[14][14] = 1; grid_cover[14][15] = 1; grid_cover[15][14] = 1;
grid_cover[6][13] = 1; grid_cover[13][6] = 1;
grid_cover[9][8] = 2; grid_cover[10][8] = 2; grid_cover[8][9] = 2; grid_cover[8][10] = 2;

// 4. Isometric Camera & Viewport Controls
cam_x = 683.0;
cam_y = 120.0;
cam_target_x = 683.0;
cam_target_y = 120.0;
zoom = 0.85;
zoom_target = 0.85;

is_dragging = false;
drag_start_mx = 0;
drag_start_my = 0;
drag_start_cam_x = 0;
drag_start_cam_y = 0;

// Mouse Grid Cursor
hover_c = -1;
hover_r = -1;
selected_weapon = 0;
valid_move_tiles = [];
valid_target_tiles = [];

// 5. Platoon Battlegroups & Mobile Suit Rosters
units = [];
selected_unit_idx = 0;
target_unit_idx = -1;

// Helper: Create Front Mission Component Set
var _create_components = function(_torso_hp, _arm_hp, _leg_hp, _head_hp, _pack_hp, _armor) {
    return {
        torso:    { name: "Torso Core",       cur: _torso_hp, max: _torso_hp, armor: _armor, intact: true },
        head:     { name: "Sensor Array",     cur: _head_hp,  max: _head_hp,  armor: floor(_armor * 0.7), intact: true },
        arm_left: { name: "Left Weapon Arm",  cur: _arm_hp,   max: _arm_hp,   armor: _armor, intact: true },
        arm_right:{ name: "Right Weapon Arm", cur: _arm_hp,   max: _arm_hp,   armor: _armor, intact: true },
        legs:     { name: "Hydraulic Limbs",  cur: _leg_hp,   max: _leg_hp,   armor: _armor, intact: true },
        backpack: { name: "Vernier Pack",     cur: _pack_hp,  max: _pack_hp,  armor: floor(_armor * 0.6), intact: true }
    };
};

// --- ALLIED / PLAYER PMC BATTLEGROUP (8 Units) ---
// 1. Alpha-01: Commander Unit (Player Heavy Ironclad)
array_push(units, {
    id: "ALLIED_0",
    callsign: "Alpha-01 'WARHAMMER'",
    pilot_name: "Commander Vance",
    team: "ALLIED",
    mech_type: "ironclad",
    grid_c: 3, grid_r: 4, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 0,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 100.0, heat_dissipation: 35.0,
    accuracy: 82, evasion: 48, braced: false,
    components: _create_components(680, 420, 620, 180, 240, 32),
    weapons: [
        { name: "Type-77 120mm Cannon", short_name: "120MM CANNON", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 15, range_min: 1, range_max: 6, damage: 165, anim_state: "fire_rifle", desc: "Kinetic solid-slug with high penetration arc." },
        { name: "GAU-88 Heavy Vulcan", short_name: "GAU-88 VULCAN", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 4, damage: 85, anim_state: "fire_chaingun", desc: "Rapid tracer bullet stream." },
        { name: "Ares Swarm-16 Missiles", short_name: "SWARM-16", proj_type: "MICRO_MISSILE", ap_cost: 4, heat_cost: 22, range_min: 2, range_max: 7, damage: 195, anim_state: "fire_missiles", desc: "Parabolic micro-missile saturation volley." },
        { name: "Gun-Club Strike", short_name: "MELEE BASH", proj_type: "MELEE", ap_cost: 3, heat_cost: 8, range_min: 1, range_max: 1, damage: 210, anim_state: "melee", desc: "Heavy hydraulic smash in close combat." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(180, 220, 255),
    is_destroyed: false
});

// 2. Alpha-02: Colony Interceptor (AET-01 Aether)
array_push(units, {
    id: "ALLIED_1",
    callsign: "Alpha-02 'VALKYRIE'",
    pilot_name: "Lt. Sonya Cruz",
    team: "ALLIED",
    mech_type: "aether",
    grid_c: 2, grid_r: 5, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 0,
    max_ap: 7, current_ap: 7,
    current_heat: 0.0, max_heat: 90.0, heat_dissipation: 40.0,
    accuracy: 88, evasion: 68, braced: false,
    components: _create_components(490, 310, 440, 160, 220, 22),
    weapons: [
        { name: "Coherent Beam Pulse Rifle", short_name: "BEAM RIFLE", proj_type: "BEAM_PULSE", ap_cost: 3, heat_cost: 20, range_min: 1, range_max: 7, damage: 180, anim_state: "fire_beam", desc: "High-intensity focused laser pulse." },
        { name: "High-Frequency Beam Saber", short_name: "BEAM SABER", proj_type: "MELEE", ap_cost: 2, heat_cost: 12, range_min: 1, range_max: 1, damage: 190, anim_state: "melee", desc: "Thermal plasma blade slash." },
        { name: "Ares Micro-Missile Pod", short_name: "POD MISSILES", proj_type: "MICRO_MISSILE", ap_cost: 3, heat_cost: 18, range_min: 2, range_max: 6, damage: 140, anim_state: "fire_missiles", desc: "Lightweight homing cluster." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(160, 235, 255),
    is_destroyed: false
});

// 3. Alpha-03: Zaibatsu High-Mobility Striker (Muramasa Prototype)
array_push(units, {
    id: "ALLIED_2",
    callsign: "Alpha-03 'KUSANAGI'",
    pilot_name: "Operative Ren",
    team: "ALLIED",
    mech_type: "muramasa",
    grid_c: 4, grid_r: 2, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 1,
    max_ap: 8, current_ap: 8,
    current_heat: 0.0, max_heat: 85.0, heat_dissipation: 35.0,
    accuracy: 85, evasion: 75, braced: false,
    components: _create_components(440, 280, 420, 150, 200, 18),
    weapons: [
        { name: "Muramasa Plasma Katana", short_name: "PLASMA BLADE", proj_type: "MELEE", ap_cost: 3, heat_cost: 14, range_min: 1, range_max: 1, damage: 240, anim_state: "melee", desc: "Monofilament thermal blade." },
        { name: "Dual Plasma Cannons", short_name: "PLASMA CANNON", proj_type: "RAILGUN_SLUG", ap_cost: 4, heat_cost: 28, range_min: 1, range_max: 5, damage: 205, anim_state: "fire_plasma", desc: "Twin magnetic containment bursts." },
        { name: "Rotary Vulcan Harass", short_name: "VULCAN", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 8, range_min: 1, range_max: 3, damage: 75, anim_state: "fire_chaingun", desc: "Point-defense deterrent." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.20,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(200, 200, 255),
    is_destroyed: false
});

// 4. Alpha-04: Terran Heavy Artillery (Siegebreaker Tank Chassis)
array_push(units, {
    id: "ALLIED_3",
    callsign: "Alpha-04 'SIEGEBREAKER'",
    pilot_name: "Gunner Miller",
    team: "ALLIED",
    mech_type: "siegebreaker",
    grid_c: 1, grid_r: 2, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 0,
    max_ap: 5, current_ap: 5,
    current_heat: 0.0, max_heat: 120.0, heat_dissipation: 28.0,
    accuracy: 90, evasion: 25, braced: true,
    components: _create_components(850, 450, 750, 220, 300, 45),
    weapons: [
        { name: "Titan 300mm Siege Railgun", short_name: "300MM RAILGUN", proj_type: "RAILGUN_SLUG", ap_cost: 4, heat_cost: 32, range_min: 3, range_max: 10, damage: 320, anim_state: "fire_siege", desc: "Ultra-high kinetic hypersonic slug." },
        { name: "Counter-Battery 120mm Shell", short_name: "120MM SOLID", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 15, range_min: 2, range_max: 7, damage: 170, anim_state: "fire_siege", desc: "Arced ballistic bombardment." },
        { name: "Defensive Flak Cannon", short_name: "DEF FLAK", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 3, damage: 90, anim_state: "fire_chaingun", desc: "Area denial shrapnel." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.12,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(220, 210, 180),
    is_destroyed: false
});

// 5. Bravo-01: Terran Coalition Line Unit (Mass Production Ironclad)
array_push(units, {
    id: "ALLIED_4",
    callsign: "Bravo-01 'BULWARK'",
    pilot_name: "Cpl. Diaz",
    team: "ALLIED",
    mech_type: "ironclad",
    grid_c: 3, grid_r: 6, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 0,
    max_ap: 5, current_ap: 5,
    current_heat: 0.0, max_heat: 100.0, heat_dissipation: 30.0,
    accuracy: 75, evasion: 42, braced: false,
    components: _create_components(620, 380, 560, 160, 210, 30),
    weapons: [
        { name: "Type-77 120mm Cannon", short_name: "120MM CANNON", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 15, range_min: 1, range_max: 6, damage: 150, anim_state: "fire_rifle", desc: "Standard issue kinetic cannon." },
        { name: "GAU-88 Heavy Vulcan", short_name: "VULCAN", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 4, damage: 80, anim_state: "fire_chaingun", desc: "Rapid fire rotary." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(170, 200, 230),
    is_destroyed: false
});

// 6. Bravo-02: Terran Coalition Heavy Line (Ironclad MP)
array_push(units, {
    id: "ALLIED_5",
    callsign: "Bravo-02 'AEGIS'",
    pilot_name: "Sgt. Kovacs",
    team: "ALLIED",
    mech_type: "ironclad",
    grid_c: 4, grid_r: 5, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 0,
    max_ap: 5, current_ap: 5,
    current_heat: 0.0, max_heat: 100.0, heat_dissipation: 30.0,
    accuracy: 76, evasion: 40, braced: false,
    components: _create_components(640, 390, 580, 170, 220, 32),
    weapons: [
        { name: "Type-77 120mm Cannon", short_name: "120MM CANNON", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 15, range_min: 1, range_max: 6, damage: 155, anim_state: "fire_rifle", desc: "Standard cannon." },
        { name: "Ares Micro-Missile Pod", short_name: "MISSILES", proj_type: "MICRO_MISSILE", ap_cost: 4, heat_cost: 20, range_min: 2, range_max: 6, damage: 170, anim_state: "fire_missiles", desc: "Missile pod." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(170, 200, 230),
    is_destroyed: false
});

// 7. Bravo-03: Colony Escort (Aether MP)
array_push(units, {
    id: "ALLIED_6",
    callsign: "Bravo-03 'ZEPHYR'",
    pilot_name: "Ens. Novak",
    team: "ALLIED",
    mech_type: "aether",
    grid_c: 2, grid_r: 3, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 0,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 90.0, heat_dissipation: 38.0,
    accuracy: 84, evasion: 64, braced: false,
    components: _create_components(460, 290, 410, 150, 210, 20),
    weapons: [
        { name: "Coherent Beam Rifle", short_name: "BEAM RIFLE", proj_type: "BEAM_PULSE", ap_cost: 3, heat_cost: 18, range_min: 1, range_max: 6, damage: 165, anim_state: "fire_beam", desc: "Laser pulse weapon." },
        { name: "Beam Saber", short_name: "SABER", proj_type: "MELEE", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 1, damage: 175, anim_state: "melee", desc: "Thermal slash." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(150, 220, 245),
    is_destroyed: false
});

// 8. Bravo-04: Zaibatsu Escort (Muramasa MP)
array_push(units, {
    id: "ALLIED_7",
    callsign: "Bravo-04 'RONIN'",
    pilot_name: "Agent Jin",
    team: "ALLIED",
    mech_type: "muramasa",
    grid_c: 5, grid_r: 4, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 1,
    max_ap: 7, current_ap: 7,
    current_heat: 0.0, max_heat: 85.0, heat_dissipation: 32.0,
    accuracy: 82, evasion: 70, braced: false,
    components: _create_components(430, 270, 400, 140, 190, 18),
    weapons: [
        { name: "Plasma Katana", short_name: "KATANA", proj_type: "MELEE", ap_cost: 3, heat_cost: 12, range_min: 1, range_max: 1, damage: 220, anim_state: "melee", desc: "Energy blade." },
        { name: "Plasma Cannon", short_name: "PLASMA", proj_type: "RAILGUN_SLUG", ap_cost: 4, heat_cost: 24, range_min: 1, range_max: 4, damage: 185, anim_state: "fire_plasma", desc: "Plasma bolt." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.20,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(190, 190, 240),
    is_destroyed: false
});


// --- HOSTILE SYNDICATE & OUTLAW BATTLEGROUP (13 Units) ---
// 1. Viper-01: Syndicate Boss Flagship (Reaver Prime - Customized Ironclad)
array_push(units, {
    id: "HOSTILE_0",
    callsign: "Viper-01 'REAVER PRIME'",
    pilot_name: "Warlord Malakar",
    team: "HOSTILE",
    mech_type: "ironclad",
    grid_c: 16, grid_r: 16, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 7, current_ap: 7,
    current_heat: 0.0, max_heat: 130.0, heat_dissipation: 35.0,
    accuracy: 82, evasion: 45, braced: false,
    components: _create_components(880, 520, 780, 220, 320, 36),
    weapons: [
        { name: "Syndicate Siege 120mm", short_name: "120MM REAVER", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 16, range_min: 1, range_max: 7, damage: 185, anim_state: "fire_rifle", desc: "Overcharged kinetic breech." },
        { name: "Rotary Flak Cannon", short_name: "HEAVY FLAK", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 4, damage: 95, anim_state: "fire_chaingun", desc: "Serrated shrapnel stream." },
        { name: "Heavy Spiked Claw", short_name: "CRUSHER CLAW", proj_type: "MELEE", ap_cost: 3, heat_cost: 10, range_min: 1, range_max: 1, damage: 250, anim_state: "melee", desc: "Devastating melee clamp." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 110, 110),
    is_destroyed: false
});

// 2. Viper-02: Raider Skirmisher (SCR-12 Hyena)
array_push(units, {
    id: "HOSTILE_1",
    callsign: "Viper-02 'SCAVENGER'",
    pilot_name: "Rogue Gnasher",
    team: "HOSTILE",
    mech_type: "hyena",
    grid_c: 15, grid_r: 14, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 2,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 80.0, heat_dissipation: 30.0,
    accuracy: 72, evasion: 62, braced: false,
    components: _create_components(420, 290, 440, 130, 170, 18),
    weapons: [
        { name: "Scrapper Flak Scattergun", short_name: "FLAK SCATTER", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 12, range_min: 1, range_max: 4, damage: 110, anim_state: "fire_flak", desc: "Scrap metal shrapnel blast." },
        { name: "Hydraulic Scrap Claw", short_name: "SCRAP CLAW", proj_type: "MELEE", ap_cost: 2, heat_cost: 8, range_min: 1, range_max: 1, damage: 180, anim_state: "melee", desc: "Industrial cutting claw." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 170, 120),
    is_destroyed: false
});

// 3. Viper-03: Raider Skirmisher (SCR-12 Hyena)
array_push(units, {
    id: "HOSTILE_2",
    callsign: "Viper-03 'CARRION'",
    pilot_name: "Rogue Grin",
    team: "HOSTILE",
    mech_type: "hyena",
    grid_c: 17, grid_r: 15, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 80.0, heat_dissipation: 30.0,
    accuracy: 74, evasion: 60, braced: false,
    components: _create_components(430, 290, 450, 130, 170, 18),
    weapons: [
        { name: "Scrapper Flak Scattergun", short_name: "FLAK SCATTER", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 12, range_min: 1, range_max: 4, damage: 110, anim_state: "fire_flak", desc: "Flak scatter." },
        { name: "Hydraulic Scrap Claw", short_name: "SCRAP CLAW", proj_type: "MELEE", ap_cost: 2, heat_cost: 8, range_min: 1, range_max: 1, damage: 180, anim_state: "melee", desc: "Scrap claw." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 170, 120),
    is_destroyed: false
});

// 4. Viper-04: Raider Skirmisher (SCR-12 Hyena)
array_push(units, {
    id: "HOSTILE_3",
    callsign: "Viper-04 'RUSTFANG'",
    pilot_name: "Rogue Snarl",
    team: "HOSTILE",
    mech_type: "hyena",
    grid_c: 14, grid_r: 16, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 80.0, heat_dissipation: 30.0,
    accuracy: 70, evasion: 65, braced: false,
    components: _create_components(410, 280, 430, 120, 160, 16),
    weapons: [
        { name: "Scrap Rocket Salvo", short_name: "ROCKETS", proj_type: "MICRO_MISSILE", ap_cost: 3, heat_cost: 16, range_min: 2, range_max: 5, damage: 145, anim_state: "fire_flak", desc: "Improvised rockets." },
        { name: "Hydraulic Scrap Claw", short_name: "SCRAP CLAW", proj_type: "MELEE", ap_cost: 2, heat_cost: 8, range_min: 1, range_max: 1, damage: 185, anim_state: "melee", desc: "Claw tear." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 170, 120),
    is_destroyed: false
});

// 5. Viper-05: Rogue Assassin (Stolen Muramasa Blade)
array_push(units, {
    id: "HOSTILE_4",
    callsign: "Viper-05 'SHADOW'",
    pilot_name: "Ex-Agent Kuro",
    team: "HOSTILE",
    mech_type: "muramasa",
    grid_c: 13, grid_r: 14, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 2,
    max_ap: 8, current_ap: 8,
    current_heat: 0.0, max_heat: 85.0, heat_dissipation: 34.0,
    accuracy: 86, evasion: 74, braced: false,
    components: _create_components(450, 280, 420, 150, 200, 20),
    weapons: [
        { name: "Plasma Katana", short_name: "KATANA", proj_type: "MELEE", ap_cost: 3, heat_cost: 14, range_min: 1, range_max: 1, damage: 235, anim_state: "melee", desc: "Energy blade." },
        { name: "Plasma Cannon", short_name: "PLASMA", proj_type: "RAILGUN_SLUG", ap_cost: 4, heat_cost: 25, range_min: 1, range_max: 5, damage: 195, anim_state: "fire_plasma", desc: "Magnetic burst." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.20,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(230, 140, 240),
    is_destroyed: false
});

// 6. Outlaw-01: Captured Ironclad Heavy Frontline
array_push(units, {
    id: "HOSTILE_5",
    callsign: "Outlaw-01 'DREAD'",
    pilot_name: "Marauder Jax",
    team: "HOSTILE",
    mech_type: "ironclad",
    grid_c: 15, grid_r: 12, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 5, current_ap: 5,
    current_heat: 0.0, max_heat: 100.0, heat_dissipation: 30.0,
    accuracy: 74, evasion: 44, braced: false,
    components: _create_components(620, 380, 560, 160, 220, 30),
    weapons: [
        { name: "Type-77 120mm Autocannon", short_name: "120MM CANNON", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 15, range_min: 1, range_max: 6, damage: 150, anim_state: "fire_rifle", desc: "Captured 120mm." },
        { name: "GAU-88 Heavy Vulcan", short_name: "VULCAN", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 4, damage: 80, anim_state: "fire_chaingun", desc: "Vulcan stream." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 120, 120),
    is_destroyed: false
});

// 7. Outlaw-02: Stolen Aether Interceptor
array_push(units, {
    id: "HOSTILE_6",
    callsign: "Outlaw-02 'SPECTRE'",
    pilot_name: "Deserter Vane",
    team: "HOSTILE",
    mech_type: "aether",
    grid_c: 12, grid_r: 15, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 2,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 90.0, heat_dissipation: 38.0,
    accuracy: 84, evasion: 66, braced: false,
    components: _create_components(460, 290, 420, 150, 210, 20),
    weapons: [
        { name: "Coherent Beam Rifle", short_name: "BEAM RIFLE", proj_type: "BEAM_PULSE", ap_cost: 3, heat_cost: 18, range_min: 1, range_max: 6, damage: 170, anim_state: "fire_beam", desc: "Stolen laser rifle." },
        { name: "Beam Saber", short_name: "SABER", proj_type: "MELEE", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 1, damage: 180, anim_state: "melee", desc: "High heat saber." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 150, 180),
    is_destroyed: false
});

// 8. Outlaw-03: Heavy Outlaw Grunt (Ironclad)
array_push(units, {
    id: "HOSTILE_7",
    callsign: "Outlaw-03 'GARGOYLE'",
    pilot_name: "Marauder Tyke",
    team: "HOSTILE",
    mech_type: "ironclad",
    grid_c: 16, grid_r: 13, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 5, current_ap: 5,
    current_heat: 0.0, max_heat: 100.0, heat_dissipation: 30.0,
    accuracy: 72, evasion: 40, braced: false,
    components: _create_components(600, 360, 540, 150, 200, 28),
    weapons: [
        { name: "120mm Autocannon", short_name: "120MM CANNON", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 15, range_min: 1, range_max: 5, damage: 145, anim_state: "fire_rifle", desc: "Kinetic weapon." },
        { name: "Missile Pod", short_name: "MISSILES", proj_type: "MICRO_MISSILE", ap_cost: 4, heat_cost: 20, range_min: 2, range_max: 6, damage: 165, anim_state: "fire_missiles", desc: "Rocket swarm." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 120, 120),
    is_destroyed: false
});

// 9. Outlaw-04: Rogue Muramasa Skirmisher
array_push(units, {
    id: "HOSTILE_8",
    callsign: "Outlaw-04 'ONI'",
    pilot_name: "Rogue Kenji",
    team: "HOSTILE",
    mech_type: "muramasa",
    grid_c: 14, grid_r: 15, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 2,
    max_ap: 7, current_ap: 7,
    current_heat: 0.0, max_heat: 85.0, heat_dissipation: 32.0,
    accuracy: 80, evasion: 70, braced: false,
    components: _create_components(430, 270, 410, 140, 190, 18),
    weapons: [
        { name: "Plasma Katana", short_name: "KATANA", proj_type: "MELEE", ap_cost: 3, heat_cost: 12, range_min: 1, range_max: 1, damage: 215, anim_state: "melee", desc: "Blade slash." },
        { name: "Plasma Cannon", short_name: "PLASMA", proj_type: "RAILGUN_SLUG", ap_cost: 4, heat_cost: 24, range_min: 1, range_max: 4, damage: 180, anim_state: "fire_plasma", desc: "Plasma strike." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.20,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(230, 130, 220),
    is_destroyed: false
});

// 10. Outlaw-05: Hyena Salvage Raider
array_push(units, {
    id: "HOSTILE_9",
    callsign: "Outlaw-05 'SCRAPHEAP'",
    pilot_name: "Rogue Patch",
    team: "HOSTILE",
    mech_type: "hyena",
    grid_c: 13, grid_r: 12, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 80.0, heat_dissipation: 30.0,
    accuracy: 70, evasion: 60, braced: false,
    components: _create_components(400, 270, 410, 120, 150, 16),
    weapons: [
        { name: "Scrapper Flak", short_name: "FLAK", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 4, damage: 105, anim_state: "fire_flak", desc: "Flak burst." },
        { name: "Scrap Claw", short_name: "CLAW", proj_type: "MELEE", ap_cost: 2, heat_cost: 8, range_min: 1, range_max: 1, damage: 175, anim_state: "melee", desc: "Claw strike." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 170, 120),
    is_destroyed: false
});

// 11. Outlaw-06: Hyena Salvage Raider
array_push(units, {
    id: "HOSTILE_10",
    callsign: "Outlaw-06 'BONECRUSHER'",
    pilot_name: "Rogue Maul",
    team: "HOSTILE",
    mech_type: "hyena",
    grid_c: 15, grid_r: 15, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 2,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 80.0, heat_dissipation: 30.0,
    accuracy: 71, evasion: 62, braced: false,
    components: _create_components(410, 280, 420, 120, 160, 16),
    weapons: [
        { name: "Scrapper Flak", short_name: "FLAK", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 4, damage: 105, anim_state: "fire_flak", desc: "Flak." },
        { name: "Scrap Claw", short_name: "CLAW", proj_type: "MELEE", ap_cost: 2, heat_cost: 8, range_min: 1, range_max: 1, damage: 175, anim_state: "melee", desc: "Claw." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 170, 120),
    is_destroyed: false
});

// 12. Outlaw-07: Stolen Aether Sniper
array_push(units, {
    id: "HOSTILE_11",
    callsign: "Outlaw-07 'WRAITH'",
    pilot_name: "Rogue Ghost",
    team: "HOSTILE",
    mech_type: "aether",
    grid_c: 16, grid_r: 11, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 6, current_ap: 6,
    current_heat: 0.0, max_heat: 90.0, heat_dissipation: 38.0,
    accuracy: 86, evasion: 65, braced: false,
    components: _create_components(450, 280, 410, 150, 200, 20),
    weapons: [
        { name: "Coherent Beam Rifle", short_name: "BEAM RIFLE", proj_type: "BEAM_PULSE", ap_cost: 3, heat_cost: 18, range_min: 2, range_max: 7, damage: 175, anim_state: "fire_beam", desc: "Long range laser beam." },
        { name: "Beam Saber", short_name: "SABER", proj_type: "MELEE", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 1, damage: 170, anim_state: "melee", desc: "Saber." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.18,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 150, 180),
    is_destroyed: false
});

// 13. Outlaw-08: Captured Ironclad Line
array_push(units, {
    id: "HOSTILE_12",
    callsign: "Outlaw-08 'RUSTBUCKET'",
    pilot_name: "Marauder Clank",
    team: "HOSTILE",
    mech_type: "ironclad",
    grid_c: 17, grid_r: 12, elev: 0,
    visual_x: 0, visual_y: 0,
    facing: 3,
    max_ap: 5, current_ap: 5,
    current_heat: 0.0, max_heat: 100.0, heat_dissipation: 30.0,
    accuracy: 70, evasion: 38, braced: false,
    components: _create_components(590, 350, 530, 150, 190, 26),
    weapons: [
        { name: "120mm Autocannon", short_name: "120MM CANNON", proj_type: "KINETIC_CANNON", ap_cost: 3, heat_cost: 15, range_min: 1, range_max: 5, damage: 140, anim_state: "fire_rifle", desc: "Standard solid cannon." },
        { name: "Vulcan Harass", short_name: "VULCAN", proj_type: "ROTARY_VULCAN", ap_cost: 2, heat_cost: 10, range_min: 1, range_max: 3, damage: 75, anim_state: "fire_chaingun", desc: "Vulcan." }
    ],
    anim_state: "idle", anim_timer: 0, anim_frame: 0.0, anim_speed: 0.15,
    recoil_x: 0, recoil_y: 0, recoil_shake: 0,
    image_blend: make_color_rgb(255, 120, 120),
    is_destroyed: false
});

// Initialize unit visual coordinates to world screen positions
for (var i = 0; i < array_length(units); i++) {
    var _u = units[i];
    _u.elev = grid_elev[_u.grid_c][_u.grid_r];
    _u.visual_x = iso_to_screen_x(_u.grid_c, _u.grid_r, _u.elev, cam_x, cam_y, zoom);
    _u.visual_y = iso_to_screen_y(_u.grid_c, _u.grid_r, _u.elev, cam_x, cam_y, zoom);
}

// 6. In-Flight Physical Projectiles & Combat FX Queues
projectiles = [];
combat_fx = [];
floating_texts = [];

// 7. Tactical Combat Log
combat_log = [
    "GRAND-SCALE ISOMETRIC COMBAT INITIALIZED // SECTOR 4 MINING CLAIM",
    "Allied Battlegroup deployed: 8 Mobile Suits (Alpha & Bravo Squadrons)",
    "Hostile Syndicate Battlegroup detected: 13 Mobile Suits (Reaver Vanguard)",
    ">> TACTICAL COMMAND: WASD/Drag to Pan, Wheel to Zoom, TAB to cycle units, [F] to rotate perspective!"
];

add_log = function(_msg) {
    array_push(combat_log, _msg);
    if (array_length(combat_log) > 8) {
        array_delete(combat_log, 0, 1);
    }
};

add_floating_text = function(_x, _y, _txt, _col) {
    array_push(floating_texts, {
        x: _x,
        y: _y,
        text: _txt,
        color: _col,
        alpha: 1.0,
        timer: 60,
        vy: -1.3
    });
};

// 8. Dynamic Sprite Selector (Front vs Back Perspective & Actions)
get_unit_sprite = function(_u) {
    var _is_back = iso_is_back_facing(_u.facing);
    var _type = _u.mech_type;
    var _act = _u.anim_state;

    if (_u.is_destroyed) {
        return spr_ms_ironclad_destroyed;
    }

    if (_is_back) {
        // BACK PERSPECTIVE SPRITES (160x160, origin 80, 145)
        if (_type == "aether" || _type == "sylph" || _type == "helios" || _type == "seraphim" || _type == "stratos" || _type == "pmc_02") return spr_ms_aether_back_idle;
        if (_type == "hyena" || _type == "marauder" || _type == "slag_lobber" || _type == "chimera" || _type == "scrapper" || _type == "pmc_03") return spr_ms_hyena_back_idle;
        if (_type == "muramasa" || _type == "ronin" || _type == "raiden" || _type == "susanoo" || _type == "ghost" || _type == "pmc_04") return spr_ms_muramasa_back_idle;
        return spr_ms_ironclad_back_idle;
    } else {
        // FRONT PERSPECTIVE SPRITES (160x160, origin 80, 145)
        if (_act == "fire_rifle" && (_type == "ironclad" || _type == "bulwark" || _type == "behemoth" || _type == "vanguard" || _type == "pmc_01")) return spr_ms_ironclad_fire_rifle;
        if (_act == "fire_chaingun" && (_type == "ironclad" || _type == "bulwark" || _type == "behemoth" || _type == "vanguard" || _type == "pmc_01")) return spr_ms_ironclad_fire_chaingun;
        if (_act == "fire_missiles" && (_type == "ironclad" || _type == "bulwark" || _type == "behemoth" || _type == "vanguard" || _type == "pmc_01")) return spr_ms_ironclad_fire_missiles;
        if (_act == "melee" && (_type == "ironclad" || _type == "bulwark" || _type == "behemoth" || _type == "vanguard" || _type == "pmc_01")) return spr_ms_ironclad_attack_melee;
        if (_act == "hit" && (_type == "ironclad" || _type == "bulwark" || _type == "behemoth" || _type == "vanguard" || _type == "pmc_01")) return spr_ms_ironclad_hit_kinetic;

        if (_act == "fire_beam" && (_type == "aether" || _type == "sylph" || _type == "helios" || _type == "seraphim" || _type == "stratos" || _type == "pmc_02")) return spr_ms_aether_fire_beam;
        if (_act == "melee" && (_type == "aether" || _type == "sylph" || _type == "helios" || _type == "seraphim" || _type == "stratos" || _type == "pmc_02")) return spr_ms_aether_attack_saber;
        if (_act == "boost" && (_type == "aether" || _type == "sylph" || _type == "helios" || _type == "seraphim" || _type == "stratos" || _type == "pmc_02")) return spr_ms_aether_boost;

        if (_act == "fire_flak" && (_type == "hyena" || _type == "marauder" || _type == "slag_lobber" || _type == "chimera" || _type == "scrapper" || _type == "pmc_03")) return spr_ms_hyena_fire_flak;
        if (_act == "melee" && (_type == "hyena" || _type == "marauder" || _type == "slag_lobber" || _type == "chimera" || _type == "scrapper" || _type == "pmc_03")) return spr_ms_hyena_attack_claw;
        if (_act == "walk" && (_type == "hyena" || _type == "marauder" || _type == "slag_lobber" || _type == "chimera" || _type == "scrapper" || _type == "pmc_03")) return spr_ms_hyena_walk;

        if (_act == "fire_plasma" && (_type == "muramasa" || _type == "ronin" || _type == "raiden" || _type == "susanoo" || _type == "ghost" || _type == "pmc_04")) return spr_ms_muramasa_fire_plasma;
        if (_act == "melee" && (_type == "muramasa" || _type == "ronin" || _type == "raiden" || _type == "susanoo" || _type == "ghost" || _type == "pmc_04")) return spr_ms_muramasa_attack_blade;
        if (_act == "sprint" && (_type == "muramasa" || _type == "ronin" || _type == "raiden" || _type == "susanoo" || _type == "ghost" || _type == "pmc_04")) return spr_ms_muramasa_sprint;

        if (_act == "fire_siege" && (_type == "siegebreaker" || _type == "behemoth" || _type == "slag_lobber")) return spr_ms_siegebreaker_fire;
        if (_act == "anchor" && (_type == "siegebreaker" || _type == "behemoth" || _type == "slag_lobber")) return spr_ms_siegebreaker_anchor;

        // Default Front Idles (160x160, origin 80, 145)
        if (_type == "aether" || _type == "sylph" || _type == "helios" || _type == "seraphim" || _type == "stratos" || _type == "pmc_02") return spr_ms_aether_idle;
        if (_type == "hyena" || _type == "marauder" || _type == "slag_lobber" || _type == "chimera" || _type == "scrapper" || _type == "pmc_03") return spr_ms_hyena_idle;
        if (_type == "muramasa" || _type == "ronin" || _type == "raiden" || _type == "susanoo" || _type == "ghost" || _type == "pmc_04") return spr_ms_muramasa_idle;
        if (_type == "siegebreaker" || _type == "behemoth") return spr_ms_siegebreaker_anchor;
        return spr_ms_ironclad_idle;
    }
};

// 9. Combat Distance & Hit Probability Functions
calculate_distance = function(_c1, _r1, _c2, _r2) {
    return abs(_c1 - _c2) + abs(_r1 - _r2);
};

calculate_hit_chance = function(_atk, _def, _dist) {
    var _base = _atk.accuracy;
    var _eva = _def.evasion;
    if (_def.braced) _eva += 35;
    if (!_atk.components.head.intact) _base -= 40;
    if (!_def.components.legs.intact) _eva = 0;
    var _cov = (grid_cover[_def.grid_c][_def.grid_r] == 1) ? 25 : ((grid_cover[_def.grid_c][_def.grid_r] == 2) ? 40 : 0);
    var _elev_diff = _atk.elev - _def.elev;
    var _elev_bonus = _elev_diff * 10;
    return clamp(_base - (_eva * 0.40) - _cov - (_dist * 2) + _elev_bonus, 20, 95);
};

// 10. Recompute Movement Tiles for Selected Unit
recalculate_moves = function() {
    valid_move_tiles = [];
    if (selected_unit_idx < 0 || selected_unit_idx >= array_length(units)) return;
    var _sel = units[selected_unit_idx];
    if (_sel.current_ap <= 0 || _sel.is_destroyed) return;
    var _max_steps = _sel.components.legs.intact ? _sel.current_ap : 1;

    for (var c = 0; c < grid_cols; c++) {
        for (var r = 0; r < grid_rows; r++) {
            var _occupied = false;
            for (var u = 0; u < array_length(units); u++) {
                var _chk = units[u];
                if (!_chk.is_destroyed && _chk.grid_c == c && _chk.grid_r == r) {
                    _occupied = true;
                    break;
                }
            }
            if (_occupied) continue;

            var _cur_elev = grid_elev[_sel.grid_c][_sel.grid_r];
            var _tgt_elev = grid_elev[c][r];
            if (abs(_tgt_elev - _cur_elev) > 1) continue;

            var _d = calculate_distance(_sel.grid_c, _sel.grid_r, c, r);
            if (_d <= _max_steps) {
                array_push(valid_move_tiles, { col: c, row: r, cost: _d });
            }
        }
    }
};

// 11. Cycle Units & Facing Controls
select_unit = function(_idx) {
    if (_idx >= 0 && _idx < array_length(units)) {
        selected_unit_idx = _idx;
        var _u = units[_idx];
        cam_target_x = 683.0 - ((_u.grid_c - _u.grid_r) * (tile_w * 0.5) * zoom);
        cam_target_y = 384.0 - (((_u.grid_c + _u.grid_r) * (tile_h * 0.5) - (_u.elev * elev_h)) * zoom);
        recalculate_moves();
    }
};

cycle_allied_unit = function() {
    var _start = selected_unit_idx;
    for (var i = 1; i <= array_length(units); i++) {
        var _idx = (_start + i) % array_length(units);
        var _u = units[_idx];
        if (_u.team == "ALLIED" && !_u.is_destroyed && _u.current_ap > 0) {
            select_unit(_idx);
            add_log("[UNIT SELECTED] Active control: " + _u.callsign);
            return;
        }
    }
    for (var i = 1; i <= array_length(units); i++) {
        var _idx = (_start + i) % array_length(units);
        var _u = units[_idx];
        if (_u.team == "ALLIED" && !_u.is_destroyed) {
            select_unit(_idx);
            return;
        }
    }
};

cycle_unit_facing = function(_u) {
    _u.facing = (_u.facing + 1) % 4;
    var _dir_names = ["SE (Front-Right)", "SW (Front-Left)", "NE (Back-Right)", "NW (Back-Left)"];
    add_log("[PERSPECTIVE ROTATE] " + _u.callsign + " facing -> " + _dir_names[_u.facing]);
};

// 12. Spawn Physical Projectile Across Screen
spawn_combat_projectile = function(_atk, _def, _wpn) {
    var _sx = iso_to_screen_x(_atk.grid_c, _atk.grid_r, _atk.elev, cam_x, cam_y, zoom);
    var _sy = iso_to_screen_y(_atk.grid_c, _atk.grid_r, _atk.elev, cam_x, cam_y, zoom) - (40 * zoom);
    var _tx = iso_to_screen_x(_def.grid_c, _def.grid_r, _def.elev, cam_x, cam_y, zoom);
    var _ty = iso_to_screen_y(_def.grid_c, _def.grid_r, _def.elev, cam_x, cam_y, zoom) - (40 * zoom);

    var _dist = calculate_distance(_atk.grid_c, _atk.grid_r, _def.grid_c, _def.grid_r);
    var _hit_chance = calculate_hit_chance(_atk, _def, _dist);

    var _cb = method({ atk: _atk, def: _def, wpn: _wpn, hit_pct: _hit_chance, mgr: id }, function() {
        mgr.resolve_combat_impact(atk, def, wpn, hit_pct);
    });

    var _proj = create_projectile(_wpn.proj_type, _sx, _sy, 0, _tx, _ty, 0, _cb);
    array_push(projectiles, _proj);
};

// 13. Resolve Impact, Front Mission Limb Damage & Reactions
resolve_combat_impact = function(_atk, _def, _wpn, _hit_chance) {
    var _roll = irandom_range(1, 100);
    var _hit = (_roll <= _hit_chance);

    var _def_sx = iso_to_screen_x(_def.grid_c, _def.grid_r, _def.elev, cam_x, cam_y, zoom);
    var _def_sy = iso_to_screen_y(_def.grid_c, _def.grid_r, _def.elev, cam_x, cam_y, zoom) - (40 * zoom);

    if (_hit) {
        screen_shake = max(screen_shake, 7.0);
        _def.recoil_shake = 8.0;
        _def.anim_state = "hit";
        _def.anim_timer = 25;

        var _part_roll = irandom_range(1, 100);
        var _hit_part = "torso";
        if (_part_roll <= 40) _hit_part = "torso";
        else if (_part_roll <= 55) _hit_part = "arm_left";
        else if (_part_roll <= 70) _hit_part = "arm_right";
        else if (_part_roll <= 90) _hit_part = "legs";
        else _hit_part = "head";

        var _limb = _def.components[$ _hit_part];
        var _raw_dmg = _wpn.damage + irandom_range(-15, 20);
        var _mitigated_dmg = max(15, _raw_dmg - _limb.armor);

        _limb.cur = max(0, _limb.cur - _mitigated_dmg);

        array_push(combat_fx, {
            sprite: spr_fx_explosion,
            x: _def_sx,
            y: _def_sy,
            frame: 0.0,
            speed: 0.25,
            scale: 1.2 * zoom
        });

        add_floating_text(_def_sx, _def_sy - 30, "-" + string(_mitigated_dmg) + " " + string_upper(_limb.name) + "!", c_yellow);
        add_log("[HIT] " + _atk.callsign + " struck " + _def.callsign + " " + _limb.name + " for " + string(_mitigated_dmg) + " damage!");

        if (_limb.cur <= 0 && _limb.intact) {
            _limb.intact = false;
            add_floating_text(_def_sx, _def_sy - 55, "COMPONENT DESTROYED: " + string_upper(_limb.name), c_red);
            add_log("[CRITICAL BREACH] " + _def.callsign + " " + _limb.name + " HAS BEEN SEVERED!");

            if (_hit_part == "torso") {
                _def.is_destroyed = true;
                _def.anim_state = "destroyed";
                screen_shake = 14.0;
                add_floating_text(_def_sx, _def_sy - 80, "REACTOR DETONATION // CHASSIS DESTROYED", c_red);
                add_log("[CATASTROPHIC KILL] " + _def.callsign + " REACTOR BREACH! Unit neutralized.");
            } else if (_hit_part == "legs") {
                _def.current_ap = min(_def.current_ap, 1);
                add_log("[MOBILITY KILL] " + _def.callsign + " hydraulic bipedal limbs crippled!");
            }
        }
    } else {
        array_push(combat_fx, {
            sprite: spr_fx_spark,
            x: _def_sx + irandom_range(-20, 20),
            y: _def_sy + irandom_range(-20, 20),
            frame: 0.0,
            speed: 0.35,
            scale: 1.0 * zoom
        });
        add_floating_text(_def_sx, _def_sy - 25, "DEFLECTED // GLANCING", c_aqua);
        add_log("[DEFLECTION] Attack glanced off " + _def.callsign + " armor!");
    }
};

select_unit(0);

show_debug_message("[obj_BattleManager] Grand-Scale Isometric Arena initialized successfully.");
