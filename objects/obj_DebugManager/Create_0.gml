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

// =========================================================================
// 8. MODULAR MECH BUILDER & FORGE STATE (TAB 1)
// Front Mission / Gundam Hangar Deck with Weapons from R&D Tech Tree
builder_subtab = 0; // 0=Chassis & Role, 1=Alloy Plating, 2=Researched Weapons, 3=Telemetry & Rollout
builder_chassis_line = 0; // 0=Player PMC Proprietary Chassis, 1=Reverse-Engineered Foreign Factions
builder_lineage_idx = (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "foundry_lineage")) ? obj_GameManager.foundry_lineage : 0; // 0=Aegis Visor (Wanzer Mil-Spec), 1=Colossus Forge (Industrial Dreadnought), 2=Stratos Vector (Agile Recon Skirmisher)
builder_lineage_names = [
    "AEGIS VISOR DOCTRINE (Mil-Spec Wanzer / Panoramic Tactical Visor)",
    "COLOSSUS FORGE DOCTRINE (Industrial Dreadnought / Dual Exhaust Blast-Hood)",
    "STRATOS VECTOR DOCTRINE (Agile Recon Skirmisher / Swept Cowlings & Twin Optics)"
];
builder_lineage_badges = ["[LINEAGE: AEGIS VISOR]", "[LINEAGE: COLOSSUS FORGE]", "[LINEAGE: STRATOS VECTOR]"];
builder_lineage_sprites = [spr_ms_pmc_aegis_visor, spr_ms_pmc_colossus_forge, spr_ms_pmc_stratos_vector];
builder_lineage_back_sprites = [spr_ms_pmc_aegis_visor_back_idle, spr_ms_pmc_colossus_forge_back_idle, spr_ms_pmc_stratos_vector_back_idle];
builder_quality_idx = 1; // 0=C-Standard, 1=B-MilSpec, 2=A-AceCustom, 3=S-SingularityMasterwork
builder_quality_names = [
    "C-TIER: INDUSTRIAL STANDARD (Baseline Yield)",
    "B-TIER: REFINED MIL-SPEC (+10% Stats, Combat Hardened)",
    "A-TIER: ACE CUSTOM PROTOTYPE (+20% Stats, Vernier Tuning)",
    "S-TIER: SINGULARITY MASTERWORK (+35% Stats, Radiant Sheen)"
];
builder_quality_badges = ["[C: INDUSTRIAL]", "[B: MIL-SPEC]", "[A: ACE PROTOTYPE]", "[S: MASTERWORK]"];
builder_quality_mults = [1.0, 1.10, 1.20, 1.35];
builder_chassis_idx = 0;
builder_alloy_idx = 0;
builder_propulsion_kits = ["Standard Bipedal", "Vernier Thrusters", "Hydro-Jet Pack", "Hover Skirt"];
builder_propulsion_idx = 0;
builder_primary_wpn_idx = 0;
builder_secondary_wpn_idx = 0;
builder_melee_wpn_idx = 0;
builder_shield_idx = 0;
builder_hardpoint_nav_idx = 0;
builder_custom_name = "HEPHAESTUS-X1";
builder_editing_callsign = false;
builder_callsign_pool = [
    "HEPHAESTUS-X1", "AEGIS VANGUARD", "IRON BASTION", "STRATOS LANCE",
    "VALKYRIE-07", "SOLARIS PRIME", "TITAN FORGE", "APEX DRAGOON"
];
builder_anim_state = "idle";
builder_subimg = 0.0;
builder_preview_scale = 2.0;
builder_perspective = "front"; // "front" or "rear"
builder_qa_bbox = false;
builder_socket_mode = 0; // 0=OFF, 1=PRIMARY WPN, 2=SHIELD
builder_overlay_primary_off = { x: -22, y: -48 };
builder_overlay_shield_off = { x: 28, y: -54 };
builder_baseline_telemetry = undefined;

builder_alloys = [
    "alloy_vanguard_comp",
    "alloy_hyperion_matrix",
    "alloy_aerosteel_flux",
    "alloy_adamantine_carbide",
    "alloy_chobham_reactive",
    "alloy_scrapper_slag",
    "alloy_carbon_nanoweave",
    "alloy_solar_crimson",
    "alloy_depleted_actinide",
    "alloy_tachyon_superalloy"
];
builder_alloy_names = [
    "Vanguard Tungsten Composite (Standard Mil-Spec)",
    "Hyperion Superconducting Matrix (+25% Energy Gen)",
    "Aerosteel Vector Flux (+35% Speed, -25% Mass)",
    "Adamantine Sintered Carbide (+45% Armor HP)",
    "Chobham-X Reactive Tiles (+50% Explosive Res)",
    "Crude Asteroid Slag (Scavenger Salvage Plating)",
    "Carbon Nanoweave Lattice (Stealth Radar-Absorbent)",
    "Solar-Forged Crimson Crucible (Extreme Thermal Disp)",
    "Depleted Actinide Heavy Slab (Superheavy Siege & EMP)",
    "Tachyon Singularity Superalloy (+35% All Stats)"
];
builder_alloy_deltas = [
    { armor_mult: 1.0,  mass_mult: 1.0,  speed_bonus: 0,   desc: "Matte gunmetal olive-drab with carbon ballistic trim.", tint_color: make_color_rgb(220, 235, 220), glow_color: make_color_rgb(255, 255, 255) },
    { armor_mult: 0.90, mass_mult: 0.85, speed_bonus: 15,  desc: "Deep cobalt navy with pulsing cyan superconducting traces.", tint_color: make_color_rgb(175, 215, 255), glow_color: make_color_rgb(0, 240, 255) },
    { armor_mult: 0.80, mass_mult: 0.75, speed_bonus: 30,  desc: "Satin aerospace chrome-white with gold vernier cowlings.", tint_color: make_color_rgb(255, 250, 240), glow_color: make_color_rgb(255, 220, 80) },
    { armor_mult: 1.45, mass_mult: 1.35, speed_bonus: -15, desc: "Blackened charred tungsten slab with industrial bronze joints.", tint_color: make_color_rgb(155, 155, 165), glow_color: make_color_rgb(255, 140, 40) },
    { armor_mult: 1.20, mass_mult: 1.10, speed_bonus: -5,  desc: "Desert sand composite tiles absorbing shaped charges.", tint_color: make_color_rgb(240, 225, 190), glow_color: make_color_rgb(255, 200, 100) },
    { armor_mult: 1.10, mass_mult: 1.25, speed_bonus: -10, desc: "Pitted oxidized iron, raw welding burns, and rust orange trim.", tint_color: make_color_rgb(215, 180, 160), glow_color: make_color_rgb(255, 120, 40) },
    { armor_mult: 0.85, mass_mult: 0.70, speed_bonus: 20,  desc: "Charcoal matte graphite with carbon-fiber weave sheen.", tint_color: make_color_rgb(170, 175, 185), glow_color: make_color_rgb(120, 220, 255) },
    { armor_mult: 1.15, mass_mult: 1.05, speed_bonus: 5,   desc: "Burnt anodized copper and deep crimson red with heat fins.", tint_color: make_color_rgb(255, 175, 170), glow_color: make_color_rgb(255, 60, 60) },
    { armor_mult: 1.55, mass_mult: 1.45, speed_bonus: -20, desc: "Toxic lead-slate gray with hazardous radioactive amber trim.", tint_color: make_color_rgb(180, 205, 180), glow_color: make_color_rgb(200, 255, 80) },
    { armor_mult: 1.35, mass_mult: 0.85, speed_bonus: 25,  desc: "Midnight iridescent violet with pulsating Cherenkov radiation.", tint_color: make_color_rgb(225, 195, 255), glow_color: make_color_rgb(200, 100, 255) }
];

// Master Weapons & Equipment R&D Tech Tree Catalog
builder_weapons_db = {
    primary: [
        { id: "wp_starter_mg_90", name: "Type-90 90mm Kinetic Machine Gun", tech_id: "tech_wpn_heavy_autocannon", damage: 180, class: "BALLISTIC", sprite: spr_ms_ironclad_fire_rifle, overlay_sprite: spr_wpn_starter_mg_90, power_draw: 2, mass: 8, lore: "Standard issue gas-operated kinetic machine gun firing AP sabots." },
        { id: "wp_smoothbore_120", name: "120mm Smoothbore Heavy Rifle", tech_id: "tech_wpn_hyper_velocity_rifle", damage: 230, class: "BALLISTIC", sprite: spr_ms_ironclad_fire_rifle, power_draw: 4, mass: 12, lore: "High-pressure smoothbore firing depleted uranium darts." },
        { id: "wp_spartan_chaingun", name: "GAU-88 35mm Spartan Rotary Vulcan", tech_id: "tech_wpn_heavy_autocannon", damage: 215, class: "ROTARY_VULCAN", sprite: spr_ms_centurion_fire_chaingun, power_draw: 4, mass: 10, lore: "Rotating multi-barrel vulcan with cooling dissipation." },
        { id: "wp_beam_rifle_type6a", name: "Type-6A High-Output Beam Rifle", tech_id: "tech_wpn_beam_carbine", damage: 260, class: "BEAM_PULSE", sprite: spr_ms_aether_fire_beam, power_draw: 8, mass: 8, lore: "Coherent Cherenkov cyan beam lance accelerator." },
        { id: "wp_railgun_90", name: "Hyper-Velocity 90mm Railgun", tech_id: "tech_wpn_electromagnetic_railgun", damage: 340, class: "BALLISTIC", sprite: spr_ms_ironclad_fire_rifle, power_draw: 12, mass: 16, lore: "Electromagnetic mass driver accelerating tungsten to Mach 8." },
        { id: "wp_tachyon_lance", name: "Coherent Tachyon Beam Lance", tech_id: "tech_wpn_tachyon_lance", damage: 390, class: "BEAM_PULSE", sprite: spr_ms_aether_fire_beam, power_draw: 14, mass: 10, lore: "Mega-particle thermal beam slicing through capital warship hulls." }
    ],
    secondary: [
        { id: "wp_hydra_rockets", name: "Unguided 70mm Hydra Rocket Pod", tech_id: "tech_wpn_hydra_rockets", damage: 140, class: "MICRO_MISSILE", sprite: spr_ms_ironclad_fire_missiles, power_draw: 2, mass: 6, lore: "Ripple-fire rocket canisters for carpet bombardment." },
        { id: "wp_micro_missile_swarm", name: "16-Cell Micro-Missile Swarm Pod", tech_id: "tech_wpn_guided_swarm_missiles", damage: 220, class: "MICRO_MISSILE", sprite: spr_ms_ironclad_fire_missiles, power_draw: 4, mass: 10, lore: "Lidar-guided swirling micro-munitions." },
        { id: "wp_antiship_torpedo", name: "Heavy Anti-Ship Torpedo Battery", tech_id: "tech_wpn_anti_ship_torpedo", damage: 380, class: "MICRO_MISSILE", sprite: spr_ms_ironclad_fire_missiles, power_draw: 6, mass: 18, lore: "Thermonuclear torpedo cracking warship keels." },
        { id: "wp_chaff_flare", name: "Thermal Chaff & ECM Flare Dispenser", tech_id: "tech_wpn_hydra_rockets", damage: 0, class: "COUNTERMEASURE", sprite: -1, power_draw: 1, mass: 3, lore: "Radar-scattering chaff providing +20% Evasion." }
    ],
    melee: [
        { id: "wp_heat_hawk", name: "Type-1 Tactical Combat Heat Axe", tech_id: "tech_wpn_plasma_heat_blade", damage: 235, class: "MELEE", sprite: spr_ms_ironclad_attack_melee, overlay_sprite: spr_wpn_heat_hawk, power_draw: 3, mass: 8, lore: "Standard issue 3000°C thermal edge combat axe cleaving armor." },
        { id: "wp_vibro_blade", name: "Titanium Vibro-Blade", tech_id: "tech_wpn_vibro_blade", damage: 160, class: "MELEE", sprite: spr_ms_aether_attack_saber, power_draw: 1, mass: 3, lore: "Solid titanium blade with ultrasonic oscillation." },
        { id: "wp_thermal_gladius", name: "Spartan High-Frequency Gladius", tech_id: "tech_wpn_vibro_blade", damage: 250, class: "MELEE", sprite: spr_ms_centurion_attack_melee, power_draw: 4, mass: 6, lore: "Bespoke shock assault thermal blade." },
        { id: "wp_beam_saber_cherenkov", name: "High-Energy Thermal Plasma Saber", tech_id: "tech_wpn_beam_saber", damage: 285, class: "MELEE", sprite: spr_ms_aether_attack_saber, power_draw: 6, mass: 4, lore: "Cherenkov cyan plasma blade with pure white core." }
    ],
    shield: [
        { id: "sld_ballistic_buckler", name: "Type-1 Ballistic Deflector Buckler", tech_id: "tech_sld_ballistic_buckler", armor_hp: 90, mass: 4, power_draw: 0, overlay_sprite: spr_wpn_ballistic_buckler, lore: "Standard issue lightweight composite deflector buckler." },
        { id: "sld_composite_tower", name: "Aegis Composite Tower Scutum", tech_id: "tech_sld_ballistic_buckler", armor_hp: 210, mass: 9, power_draw: 0, lore: "Heavy frontline blast barrier." },
        { id: "sld_em_deflector", name: "Aerosteel Deflector Shield", tech_id: "tech_sld_ballistic_buckler", armor_hp: 150, mass: 5, power_draw: 3, lore: "Angled aerosteel with electromagnetic dispersion." },
        { id: "sld_fortress_barrier", name: "Fortress Reactive Energy Barrier", tech_id: "tech_sld_ballistic_buckler", armor_hp: 300, mass: 14, power_draw: 6, lore: "Superheavy fortress barrier absorbing kinetic/beam salvos." }
    ]
};

// Player PMC Bespoke Foundry Chassis Catalog (Completely Unique Player Mobile Suits)
get_player_custom_chassis_catalog = function() {
    return [
        {
            id: "bp_player_vanguard_heavy",
            model_code: "PMC-01",
            name: "PMC-01 Vanguard Breaker",
            faction_id: "pmc_player",
            category: "PLAYER_PMC_CHASSIS",
            chassis: "Heavy Bipedal Walker",
            move_type: "biped",
            alloy: "alloy_vanguard_comp",
            sprite_asset: spr_ms_custom_biped_heavy_idle,
            sprite_back_asset: spr_ms_custom_biped_heavy_back_idle,
            sprites: {
                idle: spr_ms_custom_biped_heavy_idle,
                back_idle: spr_ms_custom_biped_heavy_back_idle,
                boost: spr_ms_ironclad_boost,
                melee: spr_ms_ironclad_attack_melee,
                fire: spr_ms_ironclad_fire_rifle,
                damaged: spr_ms_ironclad_idle_damaged,
                destroyed: spr_ms_ironclad_destroyed
            },
            weapon_name: "Type-77 120mm Solid Kinetic Cannon",
            weapon_class: "BALLISTIC",
            hp: 880,
            armor: 38,
            weight_tonnes: 60,
            power_output: 42,
            speed: 55,
            era: 2,
            doctrine: "Heavy Frontline Vanguard Linebreaker",
            lore: "Proprietary heavy assault frame engineered with reinforced modular hardpoints and high-impact kinetic hydraulics."
        },
        {
            id: "bp_player_stratos_interceptor",
            model_code: "PMC-02",
            name: "PMC-02 Stratos Interceptor",
            faction_id: "pmc_player",
            category: "PLAYER_PMC_CHASSIS",
            chassis: "High-G Vector Aero Frame",
            move_type: "aero",
            alloy: "alloy_aerosteel_flux",
            sprite_asset: spr_ms_custom_aero_striker_idle,
            sprite_back_asset: spr_ms_custom_aero_striker_back_idle,
            sprites: {
                idle: spr_ms_custom_aero_striker_idle,
                back_idle: spr_ms_custom_aero_striker_back_idle,
                boost: spr_ms_aether_boost,
                melee: spr_ms_aether_attack_saber,
                fire: spr_ms_aether_fire_beam,
                damaged: -1,
                destroyed: -1
            },
            weapon_name: "Type-6A Thermal Beam Rifle",
            weapon_class: "BEAM_PULSE",
            hp: 620,
            armor: 22,
            weight_tonnes: 42,
            power_output: 48,
            speed: 95,
            era: 2,
            doctrine: "Ultra-Agile Vector Vernier Skirmisher",
            lore: "High-mobility aerospace duelist chassis forged with Cherenkov thrusters for extreme evasive space interception."
        },
        {
            id: "bp_player_scrapper_brawler",
            model_code: "PMC-03",
            name: "PMC-03 Scrapper Brawler",
            faction_id: "pmc_player",
            category: "PLAYER_PMC_CHASSIS",
            chassis: "Continuous Sintered Track Assembly",
            move_type: "tread",
            alloy: "alloy_adamantine_carbide",
            sprite_asset: spr_ms_custom_tread_artillery_idle,
            sprite_back_asset: spr_ms_custom_tread_artillery_back_idle,
            sprites: {
                idle: spr_ms_custom_tread_artillery_idle,
                back_idle: spr_ms_custom_tread_artillery_back_idle,
                boost: spr_ms_custom_tread_artillery_idle,
                melee: spr_ms_hyena_attack_claw,
                fire: spr_ms_hyena_fire_flak,
                damaged: -1,
                destroyed: -1
            },
            weapon_name: "Heavy Recoil-Dampened Flak Howitzer",
            weapon_class: "EXPLOSIVE",
            hp: 980,
            armor: 42,
            weight_tonnes: 78,
            power_output: 36,
            speed: 35,
            era: 2,
            doctrine: "Continuous-Track Heavy Demolition Artillery",
            lore: "Heavily armored tracked chassis designed to withstand point-blank kinetic impacts and anchor heavy siege howitzers."
        },
        {
            id: "bp_player_ghost_sniper",
            model_code: "PMC-04",
            name: "PMC-04 Ghost Recon Sniper",
            faction_id: "pmc_player",
            category: "PLAYER_PMC_CHASSIS",
            chassis: "Anti-Grav Hover Repulsor",
            move_type: "hover",
            alloy: "alloy_hyperion_matrix",
            sprite_asset: spr_ms_custom_hover_sniper_idle,
            sprite_back_asset: spr_ms_custom_hover_sniper_back_idle,
            sprites: {
                idle: spr_ms_custom_hover_sniper_idle,
                back_idle: spr_ms_custom_hover_sniper_back_idle,
                boost: spr_ms_custom_hover_sniper_idle,
                melee: spr_ms_muramasa_attack_blade,
                fire: spr_ms_muramasa_fire_plasma,
                damaged: -1,
                destroyed: -1
            },
            weapon_name: "Electromagnetic Interdictor Railgun",
            weapon_class: "RAILGUN",
            hp: 560,
            armor: 24,
            weight_tonnes: 38,
            power_output: 52,
            speed: 80,
            era: 2,
            doctrine: "Low-Radar Gyroscopic Hover Interdictor",
            lore: "Stealth-coated hover frame equipped with gyroscopic stabilization and optical scattering matrices for long-range interdiction."
        },
        {
            id: "bp_player_hephaestus_avatar",
            model_code: "PMC-00",
            name: "PMC-00 Hephaestus Prime",
            faction_id: "pmc_player",
            category: "PLAYER_PMC_CHASSIS",
            chassis: "Archeotech Singularity Dreadnought",
            move_type: "biped",
            alloy: "alloy_tachyon_superalloy",
            sprite_asset: spr_ms_hephaestus_avatar,
            sprite_back_asset: spr_ms_hephaestus_avatar_back_idle,
            sprites: {
                idle: spr_ms_hephaestus_avatar,
                back_idle: spr_ms_hephaestus_avatar_back_idle,
                boost: spr_ms_titan_proto,
                melee: spr_ms_muramasa_attack_blade,
                fire: spr_ms_aether_fire_beam,
                damaged: -1,
                destroyed: -1
            },
            weapon_name: "Archeotech Singularity Tachyon Lance",
            weapon_class: "BEAM_PULSE",
            hp: 1450,
            armor: 55,
            weight_tonnes: 95,
            power_output: 75,
            speed: 65,
            era: 3,
            doctrine: "Foundry Ship Sovereign War Avatar",
            lore: "The personal war avatar of the USN-X Hephaestus, harnessing the vessel's miniature Singularity crucible."
        }
    ];
};

// Retrieve Canonical Chassis Catalog (Player Bespoke Foundry Platforms by Default)
get_canonical_chassis_list = function() {
    if (builder_chassis_line == 0) {
        return get_player_custom_chassis_catalog();
    }
    // builder_chassis_line == 1: Foreign Reverse-Engineered Factions
    var _list = [];
    for (var i = 0; i < array_length(master_roster); i++) {
        var _u = master_roster[i];
        if (_u.category == "MOBILE_SUIT" && _u.faction_id != "pmc_player") {
            var _hp_val = variable_struct_exists(_u, "hp") ? _u.hp : 680;
            if (!variable_struct_exists(_u, "power_output")) _u.power_output = floor(28 + (_hp_val / 30));
            if (!variable_struct_exists(_u, "weight_tonnes")) _u.weight_tonnes = floor(38 + (_hp_val / 22));
            if (!variable_struct_exists(_u, "speed")) {
                var _ch = variable_struct_exists(_u, "chassis") ? _u.chassis : "biped";
                _u.speed = (string_pos("hover", _ch) > 0) ? 80 : ((string_pos("tread", _ch) > 0) ? 35 : 55);
            }
            array_push(_list, _u);
        }
    }
    if (array_length(_list) == 0) return get_player_custom_chassis_catalog();
    return _list;
};

// Check if a technology is researched in R&D Tech Tree
is_tech_researched = function(_tech_id) {
    if (!instance_exists(obj_GameManager)) return true; // Debug mode fallback
    var _sys = obj_GameManager.research_system;
    if (is_undefined(_sys) || !variable_struct_exists(_sys, "unlocked_techs")) return true;
    return variable_struct_exists(_sys.unlocked_techs, _tech_id) && _sys.unlocked_techs[$ _tech_id] == true;
};

// Smart Default Loadout: Auto-equips latest researched equipment matching mobile suit role
apply_smart_default_loadout = function(_chassis) {
    var _doc = string_lower(variable_struct_exists(_chassis, "doctrine") ? _chassis.doctrine : "");
    var _w_class = variable_struct_exists(_chassis, "weapon_class") ? _chassis.weapon_class : "BALLISTIC";
    var _c_name = string_lower(_chassis.name);

    // 1. Primary Ranged
    if (string_pos("beam", _doc) > 0 || _w_class == "BEAM_PULSE" || string_pos("aether", _c_name) > 0) {
        builder_primary_wpn_idx = is_tech_researched("tech_wpn_tachyon_lance") ? 5 : (is_tech_researched("tech_wpn_beam_carbine") ? 3 : 0);
    } else if (string_pos("centurion", _c_name) > 0 || _w_class == "ROTARY_VULCAN") {
        builder_primary_wpn_idx = 2; // Spartan Chaingun
    } else if (string_pos("sniper", _doc) > 0 || string_pos("railgun", _doc) > 0) {
        builder_primary_wpn_idx = is_tech_researched("tech_wpn_electromagnetic_railgun") ? 4 : 1;
    } else {
        builder_primary_wpn_idx = is_tech_researched("tech_wpn_hyper_velocity_rifle") ? 1 : 0;
    }

    // 2. Secondary
    if (string_pos("missile", _doc) > 0 || string_pos("siege", _doc) > 0) {
        builder_secondary_wpn_idx = is_tech_researched("tech_wpn_anti_ship_torpedo") ? 2 : 1;
    } else if (string_pos("aero", _doc) > 0 || string_pos("vernier", _doc) > 0) {
        builder_secondary_wpn_idx = 3; // Chaff / ECM
    } else {
        builder_secondary_wpn_idx = is_tech_researched("tech_wpn_guided_swarm_missiles") ? 1 : 0;
    }

    // 3. Melee
    if (string_pos("beam", _doc) > 0 || string_pos("plasma", _doc) > 0 || string_pos("aether", _c_name) > 0) {
        builder_melee_wpn_idx = is_tech_researched("tech_wpn_beam_saber") ? 3 : 0;
    } else if (string_pos("centurion", _c_name) > 0) {
        builder_melee_wpn_idx = 2; // Spartan Gladius
    } else {
        builder_melee_wpn_idx = is_tech_researched("tech_wpn_plasma_heat_blade") ? 1 : 0;
    }

    // 4. Shield
    if (string_pos("heavy", _doc) > 0 || string_pos("trench", _doc) > 0 || string_pos("ironclad", _c_name) > 0) {
        builder_shield_idx = 1; // Tower Scutum
    } else if (string_pos("aether", _c_name) > 0 || string_pos("colony", _doc) > 0) {
        builder_shield_idx = 2; // Aerosteel Deflector
    } else {
        builder_shield_idx = 0; // Buckler
    }

    builder_custom_name = _chassis.name + " [PMC SPEC]";
};

// Calculate Full Telemetry based on Chassis + Sintered Alloy + Quality Tier + Researched Loadout
calculate_builder_telemetry = function() {
    var _chassis_list = get_canonical_chassis_list();
    var _c = _chassis_list[clamp(builder_chassis_idx, 0, array_length(_chassis_list) - 1)];

    var _alloy_d = builder_alloy_deltas[clamp(builder_alloy_idx, 0, array_length(builder_alloy_deltas) - 1)];
    var _q_mult = builder_quality_mults[clamp(builder_quality_idx, 0, array_length(builder_quality_mults) - 1)];
    var _wpn_p = builder_weapons_db.primary[clamp(builder_primary_wpn_idx, 0, array_length(builder_weapons_db.primary) - 1)];
    var _wpn_s = builder_weapons_db.secondary[clamp(builder_secondary_wpn_idx, 0, array_length(builder_weapons_db.secondary) - 1)];
    var _wpn_m = builder_weapons_db.melee[clamp(builder_melee_wpn_idx, 0, array_length(builder_weapons_db.melee) - 1)];
    var _sld   = builder_weapons_db.shield[clamp(builder_shield_idx, 0, array_length(builder_weapons_db.shield) - 1)];

    var _base_hp = variable_struct_exists(_c, "hp") ? _c.hp : 680;
    var _base_mass = variable_struct_exists(_c, "weight_tonnes") ? _c.weight_tonnes : 65.0;
    var _base_spd = variable_struct_exists(_c, "speed") ? _c.speed : 55;
    var _core_mw = variable_struct_exists(_c, "power_output") ? _c.power_output : 35;

    // Apply Sintered Alloy & Quality Tier Scaling
    var _tot_armor = floor(((_base_hp * _alloy_d.armor_mult) + _sld.armor_hp) * _q_mult);
    var _tot_mass = floor((_base_mass * _alloy_d.mass_mult) + _wpn_p.mass + _wpn_s.mass + _wpn_m.mass + _sld.mass);
    var _max_capacity = floor(_base_mass * 1.55);
    var _mass_overloaded = (_tot_mass > _max_capacity);

    var _tot_draw = _wpn_p.power_draw + _wpn_s.power_draw + _wpn_m.power_draw + _sld.power_draw;
    var _scaled_core = floor(_core_mw * _q_mult);
    var _net_power = _scaled_core - _tot_draw;
    var _reactor_overloaded = (_net_power < 0);

    var _final_spd = max(20, floor(((_base_spd + _alloy_d.speed_bonus) * (1.0 - (_tot_mass / 250.0))) * (1.0 + ((_q_mult - 1.0) * 0.5))));
    var _boost_spd = _final_spd + 45;
    var _oss = floor(((_tot_armor / 5) + _wpn_p.damage + (_wpn_m.damage / 2) + (_final_spd / 2) + max(0, _net_power * 3)) * _q_mult);

    var _w_class = "MEDIUM MAINSTAY";
    if (_tot_mass < 55) _w_class = "LIGHT SKIRMISHER";
    else if (_tot_mass >= 55 && _tot_mass < 82) _w_class = "MEDIUM MAINSTAY";
    else if (_tot_mass >= 82 && _tot_mass < 105) _w_class = "HEAVY ASSAULT";
    else _w_class = "SUPERHEAVY SIEGEBREAKER";

    var _preview_spr = _c.sprite_asset;
    var _preview_back_spr = _c.sprite_back_asset;
    if (builder_chassis_line == 0 && builder_chassis_idx == 0) {
        var _lin_idx = builder_lineage_idx % array_length(builder_lineage_sprites);
        _preview_spr = builder_lineage_sprites[_lin_idx];
        _preview_back_spr = builder_lineage_back_sprites[_lin_idx];
    }

    var _ov_prim = variable_struct_exists(_wpn_p, "overlay_sprite") ? _wpn_p.overlay_sprite : -1;
    var _ov_melee = variable_struct_exists(_wpn_m, "overlay_sprite") ? _wpn_m.overlay_sprite : -1;
    var _ov_shield = variable_struct_exists(_sld, "overlay_sprite") ? _sld.overlay_sprite : -1;

    var _aid_t = builder_alloys[clamp(builder_alloy_idx, 0, array_length(builder_alloys) - 1)];
    var _cid_t = string_lower(_c.id);
    var _ter = { land: "A", mountain: "B", water: "C", air: "B", space: "B", ground: "A", urban: "A", trench: "B" };
    if (string_pos("colossus", _cid_t) > 0 || string_pos("behemoth", _cid_t) > 0 || string_pos("ironclad", _cid_t) > 0) {
        _ter = { land: "S", mountain: "A", water: "D", air: "D", space: "C", ground: "S", urban: "A", trench: "A" };
    } else if (string_pos("stratos", _cid_t) > 0 || string_pos("aether", _cid_t) > 0 || string_pos("kamaitachi", _cid_t) > 0) {
        _ter = { land: "A", mountain: "B", water: "C", air: "S", space: "S", ground: "A", urban: "B", trench: "C" };
    }
    if (_aid_t == "alloy_aerosteel_flux" || _aid_t == "alloy_tachyon_superalloy") {
        _ter.air = "S"; _ter.space = "S";
    } else if (_aid_t == "alloy_adamantine_carbide" || _aid_t == "alloy_chobham_reactive") {
        _ter.land = "S"; _ter.mountain = "S";
    } else if (_aid_t == "alloy_carbon_nanoweave") {
        _ter.water = "A"; _ter.mountain = "A";
    }
    var _pkit_idx = clamp(builder_propulsion_idx, 0, array_length(builder_propulsion_kits) - 1);
    if (_pkit_idx == 1) { _ter.air = "S"; _ter.space = "S"; }
    else if (_pkit_idx == 2) { _ter.water = "S"; _ter.land = "B"; }
    else if (_pkit_idx == 3) { _ter.land = "S"; _ter.water = "A"; }

    return {
        chassis: _c, alloy_delta: _alloy_d, quality_mult: _q_mult, quality_idx: builder_quality_idx,
        primary_wpn: _wpn_p, secondary_wpn: _wpn_s, melee_wpn: _wpn_m, shield: _sld,
        total_armor: _tot_armor, total_mass: _tot_mass, max_capacity: _max_capacity,
        mass_overloaded: _mass_overloaded, power_output: _scaled_core, total_draw: _tot_draw,
        net_power: _net_power, reactor_overloaded: _reactor_overloaded,
        walk_speed: _final_spd, boost_speed: _boost_spd, combat_rating: _oss,
        weight_class: _w_class, preview_sprite: _preview_spr, preview_back_sprite: _preview_back_spr,
        overlay_primary: _ov_prim, overlay_melee: _ov_melee, overlay_shield: _ov_shield,
        terrain: _ter, propulsion_kit: builder_propulsion_kits[_pkit_idx],
        sprites: _c.sprites,
        tint: _alloy_d.tint_color,
        glow: _alloy_d.glow_color
    };
};

deploy_builder_mech_to_combat = function() {
    var _t = calculate_builder_telemetry();
    if (_t.reactor_overloaded) {
        show_toast("DEPLOYMENT REJECTED: Net Power is Negative (Reactor Overload)!", c_red);
        scr_audio_play_ui("cancel");
        return;
    }

    var _custom_u = {
        id: "custom_test_" + string(irandom(9999)),
        name: builder_custom_name,
        faction_id: "pmc_player",
        category: "CUSTOM_MECH",
        move_type: variable_struct_exists(_t.chassis, "move_type") ? _t.chassis.move_type : "biped",
        chassis: variable_struct_exists(_t.chassis, "chassis") ? _t.chassis.chassis : "biped",
        alloy_id: builder_alloys[builder_alloy_idx],
        alloy: builder_alloys[builder_alloy_idx],
        era: 2,
        sprite_asset: _t.preview_sprite,
        sprite_back_asset: _t.preview_back_sprite,
        image_blend: _t.tint,
        weapon_overlay_primary: (_t.overlay_primary != -1) ? sprite_get_name(_t.overlay_primary) : "",
        weapon_overlay_secondary: (_t.overlay_shield != -1) ? sprite_get_name(_t.overlay_shield) : "",
        overlay_primary_offset: { x: builder_overlay_primary_off.x, y: builder_overlay_primary_off.y },
        overlay_shield_offset: { x: builder_overlay_shield_off.x, y: builder_overlay_shield_off.y },
        weapon_name: _t.primary_wpn.name,
        weapon_class: _t.primary_wpn.class,
        hp: _t.total_armor,
        armor: floor(_t.total_armor / 12),
        speed: _t.boost_speed,
        accuracy: 88,
        evasion: 25,
        attack_range: 2,
        role: _t.weight_class,
        doctrine: "PMC Hephaestus Custom Masterwork",
        aux_system: _t.secondary_wpn.name + " // " + _t.melee_wpn.name + " // " + _t.shield.name,
        sprites: {
            idle: _t.preview_sprite,
            back_idle: _t.preview_back_sprite,
            walk: (variable_struct_exists(_t.sprites, "boost") && _t.sprites.boost != -1) ? _t.sprites.boost : _t.preview_sprite,
            fire: _t.primary_wpn.sprite,
            melee: _t.melee_wpn.sprite,
            boost: (variable_struct_exists(_t.sprites, "boost") && _t.sprites.boost != -1) ? _t.sprites.boost : _t.preview_sprite,
            damaged: (variable_struct_exists(_t.sprites, "damaged") && _t.sprites.damaged != -1) ? _t.sprites.damaged : _t.preview_sprite,
            destroyed: (variable_struct_exists(_t.sprites, "destroyed") && _t.sprites.destroyed != -1) ? _t.sprites.destroyed : _t.preview_sprite
        }
    };

    array_insert(master_roster, 0, _custom_u);
    atk_faction_idx = 0;
    atk_cat_idx = 0;
    atk_filtered_idx = 0;
    active_debug_tab = 0;

    // Update comparison baseline to this newly created mobile suit
    builder_baseline_telemetry = {
        label: builder_custom_name,
        total_armor: _t.total_armor,
        total_mass: _t.total_mass,
        net_power: _t.net_power,
        boost_speed: _t.boost_speed,
        combat_rating: _t.combat_rating
    };

    scr_audio_play_ui("boot");
    show_toast("DEPLOYED TO COMBAT LAB: " + builder_custom_name + " ready for live action testing!", c_lime);
};

commission_builder_mech_to_hangar = function() {
    var _t = calculate_builder_telemetry();
    if (_t.reactor_overloaded) {
        show_toast("COMMISSION REJECTED: Net Power is Negative!", c_red);
        scr_audio_play_ui("cancel");
        return;
    }
    if (instance_exists(obj_GameManager)) {
        var _gm = obj_GameManager;
        var _aid = builder_alloys[builder_alloy_idx];
        var _new_mech = {
            id: "custom_mech_" + string(_gm.current_turn) + "_" + string(irandom(9999)),
            blueprint_id: _t.chassis.id,
            alloy_id: _aid,
            propulsion_kit: _t.propulsion_kit,
            is_masterwork: (builder_quality_idx == 3),
            terrain: _t.terrain,
            callsign: builder_custom_name,
            name: builder_custom_name,
            class: _t.weight_class,
            assigned_pilot: "Unassigned",
            status: "READY",
            current_condition_pct: 1.0,
            armor_rating: _t.total_armor,
            power_output: _t.net_power,
            speed: _t.boost_speed,
            weight_tonnes: _t.total_mass,
            combat_rating: _t.combat_rating,
            components_summary: _t.chassis.name + " // " + _t.primary_wpn.name + " // " + _t.secondary_wpn.name + " // " + _t.melee_wpn.name + " // " + _t.shield.name,
            part_composition: { chassis: _t.chassis, primary: _t.primary_wpn, secondary: _t.secondary_wpn, melee: _t.melee_wpn, shield: _t.shield },
            spec_type: "COMMANDER_CUSTOM",
            combat_pedigree: { sorties_deployed: 0, sorties_survived: 0, confirmed_kills: 0, ace_kills: 0, damage_mitigated: 0, pedigree_rating: "FACTORY_FRESH", telemetry_bonus: 0.0 }
        };
        array_push(_gm.inventory.deployable_mechs, _new_mech);
        builder_baseline_telemetry = {
            label: builder_custom_name,
            total_armor: _t.total_armor,
            total_mass: _t.total_mass,
            net_power: _t.net_power,
            boost_speed: _t.boost_speed,
            combat_rating: _t.combat_rating
        };
        show_toast("COMMISSIONED TO FLEET HANGAR: " + builder_custom_name + " added to Hangar!", c_lime);
        scr_audio_play_ui("boot");
    }
};

compute_stock_baseline_telemetry = function() {
    var _sv_a = builder_alloy_idx;
    var _sv_q = builder_quality_idx;
    var _sv_p = builder_primary_wpn_idx;
    var _sv_s = builder_secondary_wpn_idx;
    var _sv_m = builder_melee_wpn_idx;
    var _sv_sh = builder_shield_idx;

    builder_alloy_idx = 0;
    builder_quality_idx = 0;
    builder_primary_wpn_idx = 0;
    builder_secondary_wpn_idx = 0;
    builder_melee_wpn_idx = 0;
    builder_shield_idx = 0;

    var _base_t = calculate_builder_telemetry();

    builder_alloy_idx = _sv_a;
    builder_quality_idx = _sv_q;
    builder_primary_wpn_idx = _sv_p;
    builder_secondary_wpn_idx = _sv_s;
    builder_melee_wpn_idx = _sv_m;
    builder_shield_idx = _sv_sh;

    builder_baseline_telemetry = {
        label: "STOCK BASE",
        total_armor: _base_t.total_armor,
        total_mass: _base_t.total_mass,
        net_power: _base_t.net_power,
        boost_speed: _base_t.boost_speed,
        combat_rating: _base_t.combat_rating
    };
    return builder_baseline_telemetry;
};

apply_builder_preset = function(_preset_idx) {
    builder_chassis_line = 0;
    builder_chassis_idx = 0;
    var _np = array_length(builder_weapons_db.primary);
    var _ns = array_length(builder_weapons_db.secondary);
    var _nm = array_length(builder_weapons_db.melee);
    var _nsh = array_length(builder_weapons_db.shield);
    var _na = array_length(builder_alloys);

    if (_preset_idx == 0) {
        // BRAWLER: Colossus Forge + Heavy Armor + Assault/Melee
        builder_lineage_idx = 1;
        builder_alloy_idx = min(3, _na - 1); // Adamantine Carbide
        builder_quality_idx = 2;
        builder_primary_wpn_idx = min(1, _np - 1);
        builder_secondary_wpn_idx = 0;
        builder_melee_wpn_idx = min(1, _nm - 1);
        builder_shield_idx = min(1, _nsh - 1);
        builder_custom_name = "IRON BASTION";
        show_toast("PRESET LOADED: HEAVY BRAWLER", make_color_rgb(255, 180, 50));
    } else if (_preset_idx == 1) {
        // SKIRMISHER: Stratos Vector + Aerosteel + High Mobility
        builder_lineage_idx = 2;
        builder_alloy_idx = min(2, _na - 1); // Aerosteel Flux
        builder_quality_idx = 2;
        builder_primary_wpn_idx = 0;
        builder_secondary_wpn_idx = min(1, _ns - 1);
        builder_melee_wpn_idx = 0;
        builder_shield_idx = 0;
        builder_custom_name = "STRATOS LANCE";
        show_toast("PRESET LOADED: RECON SKIRMISHER", make_color_rgb(200, 120, 255));
    } else if (_preset_idx == 2) {
        // FIRE SUPPORT: Aegis Visor + Hyperion Matrix + Heavy Ordnance
        builder_lineage_idx = 0;
        builder_alloy_idx = min(1, _na - 1); // Hyperion Matrix
        builder_quality_idx = 2;
        builder_primary_wpn_idx = min(2, _np - 1);
        builder_secondary_wpn_idx = min(2, _ns - 1);
        builder_melee_wpn_idx = 0;
        builder_shield_idx = 0;
        builder_custom_name = "AEGIS VANGUARD";
        show_toast("PRESET LOADED: FIRE SUPPORT", c_aqua);
    } else {
        // RANDOMIZE
        builder_lineage_idx = irandom(2);
        builder_alloy_idx = irandom(_na - 1);
        builder_quality_idx = irandom(3);
        builder_primary_wpn_idx = irandom(_np - 1);
        builder_secondary_wpn_idx = irandom(_ns - 1);
        builder_melee_wpn_idx = irandom(_nm - 1);
        builder_shield_idx = irandom(_nsh - 1);
        builder_custom_name = builder_callsign_pool[irandom(array_length(builder_callsign_pool) - 1)];
        show_toast("RANDOMIZED BUILD: " + builder_custom_name, c_yellow);
    }
    if (instance_exists(obj_GameManager)) obj_GameManager.set_foundry_lineage(builder_lineage_idx);
    scr_audio_play_ui("boot");
};

unlock_all_research_cheats = function() {
    if (instance_exists(obj_GameManager) && !is_undefined(obj_GameManager.research_system)) {
        var _sys = obj_GameManager.research_system;
        var _db = scr_research_get_tech_db();
        var _keys = variable_struct_get_names(_db);
        for (var k = 0; k < array_length(_keys); k++) {
            _sys.unlocked_techs[$ _keys[k]] = true;
        }
        show_toast("ALL WEAPONS & TECH RESEARCHED! Entire R&D Arsenal Available!", c_yellow);
        scr_audio_play_ui("boot");
    }
};

// =========================================================================
// 9. ASTEROID MINING & PLANETARY RESOURCE EXTRACTION STATE (TAB 2)
// =========================================================================
mining_selected_idx = 0;
mining_sphere_idx = 0;
mining_spheres = ["ALL", "Earth Sphere", "Asteroid Belt", "Jovian System", "Outer Colonies", "Mars Sphere"];
mining_drill_active = false;
mining_drill_heat = 0.0;
mining_drill_timer = 0;
mining_particles = [];
mining_session_extracted = { mat_tungsten: 0, mat_silica_carb: 0, mat_tritium: 0, mat_syn_flux: 0, item_slag: 0 };

get_debug_mining_nodes = function() {
    if (instance_exists(obj_GameManager) && is_array(obj_GameManager.nodes) && array_length(obj_GameManager.nodes) > 0) {
        var _all_nd = obj_GameManager.nodes;
        if (mining_sphere_idx == 0) return _all_nd;
        var _cur_sph = mining_spheres[mining_sphere_idx];
        var _res = [];
        for (var i = 0; i < array_length(_all_nd); i++) {
            var _n = _all_nd[i];
            if (variable_struct_exists(_n, "sphere") && _n.sphere == _cur_sph) {
                array_push(_res, _n);
            }
        }
        if (array_length(_res) == 0) return _all_nd;
        return _res;
    }
    // Fallback default node list if GameManager not loaded
    return [
        { id: "node_asteroid_c14", name: "Asteroid Belt C-14", sphere: "Asteroid Belt", primary_yield: "mat_tungsten", secondary_yield: "mat_silica_carb", yield_rate_primary: 4, yield_rate_secondary: 3, threat_level_pct: 20, status: "ACTIVE_MINING", current_storage: { mat_tungsten: 18, mat_silica_carb: 12 }, assigned_mech_id: "unit_ironclad_01" },
        { id: "node_moon_io4", name: "Volcanic Moon Io-IV", sphere: "Jovian System", primary_yield: "mat_silica_carb", secondary_yield: "mat_tungsten", yield_rate_primary: 6, yield_rate_secondary: 2, threat_level_pct: 35, status: "UNCLAIMED", current_storage: {}, assigned_mech_id: "Unassigned" },
        { id: "node_gas_giant", name: "Gas Giant Orbital Ring", sphere: "Outer Colonies", primary_yield: "mat_tritium", secondary_yield: "none", yield_rate_primary: 3, yield_rate_secondary: 0, threat_level_pct: 50, status: "UNCLAIMED", current_storage: {}, assigned_mech_id: "Unassigned" },
        { id: "node_shipyard_omega", name: "Derelict Shipyard Omega", sphere: "Earth Sphere", primary_yield: "mat_syn_flux", secondary_yield: "item_slag", yield_rate_primary: 3, yield_rate_secondary: 2, threat_level_pct: 65, status: "UNCLAIMED", current_storage: {}, assigned_mech_id: "Unassigned" }
    ];
};

pulse_mine_node = function() {
    var _nodes = get_debug_mining_nodes();
    if (array_length(_nodes) == 0) return;
    var _node = _nodes[clamp(mining_selected_idx, 0, array_length(_nodes) - 1)];

    mining_drill_active = true;
    mining_drill_timer = 25;
    mining_drill_heat = min(100.0, mining_drill_heat + 16.0);

    // Calculate yield with flagship refining multiplier
    var _mult = 1.0;
    if (instance_exists(obj_GameManager)) {
        var _gm = obj_GameManager;
        var _tier = (variable_struct_exists(_gm.flagship, "upgrades") && variable_struct_exists(_gm.flagship.upgrades, "mining_tier")) ? _gm.flagship.upgrades.mining_tier : 1;
        var _tier_mults = [1.25, 1.50, 2.00, 2.50, 3.50];
        _mult = _tier_mults[clamp(_tier - 1, 0, 4)];
    }

    var _yield_p = max(1, floor(_node.yield_rate_primary * _mult * random_range(0.9, 1.3)));
    var _res_p = _node.primary_yield;

    // Add to node storage and session
    if (_res_p != "none") {
        if (!variable_struct_exists(_node.current_storage, _res_p)) variable_struct_set(_node.current_storage, _res_p, 0);
        variable_struct_set(_node.current_storage, _res_p, variable_struct_get(_node.current_storage, _res_p) + _yield_p);

        if (!variable_struct_exists(mining_session_extracted, _res_p)) variable_struct_set(mining_session_extracted, _res_p, 0);
        variable_struct_set(mining_session_extracted, _res_p, variable_struct_get(mining_session_extracted, _res_p) + _yield_p);

        // Add to GameManager inventory directly
        if (instance_exists(obj_GameManager)) {
            var _raw = obj_GameManager.inventory.raw_materials;
            if (!variable_struct_exists(_raw, _res_p)) variable_struct_set(_raw, _res_p, 0);
            variable_struct_set(_raw, _res_p, variable_struct_get(_raw, _res_p) + _yield_p);
        }
    }

    // Spawn floating particle text
    array_push(mining_particles, {
        x: 640 + random_range(-60, 60),
        y: 350 + random_range(-20, 20),
        vy: -2.0,
        life: 60,
        text: "+" + string(_yield_p) + " " + string_upper(string_replace(_res_p, "mat_", "")) + " (" + string(floor(_mult * 100)) + "% Yield)",
        color: make_color_rgb(0, 240, 255)
    });

    scr_audio_play_ui("click");
    show_toast("MINING PULSE: Extracted +" + string(_yield_p) + " " + _res_p + " from " + _node.name + "!", c_aqua);
};

smelt_alloy_debug = function(_alloy_key, _qty) {
    if (instance_exists(obj_GameManager)) {
        var _gm = obj_GameManager;
        var _alloys = _gm.inventory.alloys;
        if (!variable_struct_exists(_alloys, _alloy_key)) variable_struct_set(_alloys, _alloy_key, 0);
        variable_struct_set(_alloys, _alloy_key, variable_struct_get(_alloys, _alloy_key) + _qty);
        scr_audio_play_ui("boot");
        show_toast("SMELTER COMPLETE: Synthesized +" + string(_qty) + " " + _alloy_key + "!", c_yellow);
    }
};

trigger_mining_raid_debug = function() {
    var _nodes = get_debug_mining_nodes();
    if (array_length(_nodes) == 0) return;
    var _node = _nodes[clamp(mining_selected_idx, 0, array_length(_nodes) - 1)];
    if (instance_exists(obj_GameManager)) {
        obj_GameManager.pending_raid = {
            node: _node,
            threat: _node.threat_level_pct,
            target_node_id: _node.id,
            attacker_faction: "faction_syndicate",
            attacker_count: irandom_range(3, 6)
        };
        scr_audio_play_ui("cancel");
        show_toast("PIRATE INVASION TRIGGERED: Alert on " + _node.name + " (Threat: " + string(_node.threat_level_pct) + "%)!", c_red);
    }
};

claim_all_mining_nodes = function() {
    if (instance_exists(obj_GameManager)) {
        var _nodes = obj_GameManager.nodes;
        for (var i = 0; i < array_length(_nodes); i++) {
            _nodes[i].status = "ACTIVE_MINING";
            _nodes[i].assigned_mech_id = "GHA-07 Ironclad Escort";
        }
        scr_audio_play_ui("boot");
        show_toast("MASTER OVERRIDE: All " + string(array_length(_nodes)) + " Solar System mining nodes claimed!", c_lime);
    }
};
