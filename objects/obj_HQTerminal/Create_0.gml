/// @description obj_HQTerminal Create Event
// Unified Command Deck Terminal UI State Machine & Simulation Hub
// Strictly implements docs/09_ui_ux_flow.md, docs/02_alloy_chemistry.md & docs/03_prototyping_minigames.md

show_debug_message("[obj_HQTerminal] Initializing Command Deck Terminal Controller...");

// Bootstrap persistent system managers if not present
if (!instance_exists(obj_GameManager)) instance_create_depth(0, 0, 0, obj_GameManager);
if (!instance_exists(obj_FactionManager)) instance_create_depth(0, 0, 0, obj_FactionManager);
if (!instance_exists(obj_BlueprintManager)) instance_create_depth(0, 0, 0, obj_BlueprintManager);
if (!instance_exists(obj_AudioManager)) instance_create_depth(0, 0, 0, obj_AudioManager);

// Start Terminal Background Audio Atmosphere
scr_audio_play_ui("boot");
scr_audio_play_location_bgm((active_tab == 0) ? "prototyping" : "hq");

// 1. Navigation State
// Intro Briefing & Commander Selection State
intro_active = (instance_exists(obj_GameManager) && !obj_GameManager.has_completed_intro);
intro_page = 0; // 0 = Situation Briefing, 1 = Commander Selection Dossier
selected_commander_choice = "silhouette"; // "silhouette", "male", "female"
show_commander_modal = false;

active_tab = 0;              // 0 = R&D Lab, 1 = Factory Floor, 2 = Contracts, 3 = War Map
rd_subtab = 0;               // 0 = Crucible Synthesis (Doc 02), 1 = Prototyping Minigames (Doc 03), 2 = Blueprint Specs
war_subtab = 0;              // 0 = Sector War Map & Mining, 1 = Faction Dossiers, 2 = Faction Diplomacy Matrix (Doc 21), 3 = Decade Mecha Timeline, 4 = PMC Expedition (Doc 12)
selected_diplo_pair = "terran_colony"; // Selected pair in Diplomacy Matrix (Doc 21)
flagship_subtab = 0;                   // 0 = Warship & Upgrades, 1 = Celestial Navigation, 2 = Rival Corporate Competitors (Doc 23)
selected_rival_corp = "corp_vhi";      // Selected rival corporate manufacturer
flagship_division_category = 0;        // 0 = Production & Harvest, 1 = Defense & Weapons, 2 = Drives & Pilots, 3 = SIGINT & Command (Doc 24)
diplo_cables_scroll_offset = 0;        // Paging offset for diplomatic cables log
selected_faction_dossier = "faction_terran"; // "faction_terran", "faction_colony", "faction_syndicate", "faction_zaibatsu"
selected_timeline_era = 0;   // 0 = All Eras, 1 = Y205 Prototype, 2 = Y208 Early Mass, 3 = Y211 Mainstay, 4 = Y213 Variant, 5 = Y215 Next-Gen
selected_timeline_mech_idx = 0; // Selected mobile suit index in timeline array
timeline_page = 0;           // Current page index in mobile suit registry
timeline_filter_faction = 0; // 0 = All Factions, 1 = Terran, 2 = Colony, 3 = Syndicate, 4 = Zaibatsu
contracts_subtab = 0;        // 0 = Procurement Orders (Doc 04), 1 = Mass-Production Replacement Doctrine (Doc 12)
selected_pitch_faction = "faction_a";
selected_pitch_bp = "bp_player_vanguard_aegis";
selected_strike_faction = "faction_c";
selected_strike_mech = 0;
selected_strike_pilot = 0;
showing_retire_modal = false;
factory_subtab = 0;          // 0 = Facilities & Assembly (Doc 07), 1 = Modular Part Forge, 2 = Custom Combinations Assembly Bay (Doc 13)
forge_selected_slot = 0;     // 0=Heads, 1=Torsos, 2=Arms, 3=Legs, 4=Backpacks, 5=Weapons
assembly_head_idx = 0;
assembly_torso_idx = 0;
assembly_arms_idx = 0;
assembly_legs_idx = 0;
assembly_bp_idx = 0;
assembly_wp_idx = 0;
assembly_custom_name = "Vanguard Chimera Spec-X";
assembly_selected_slot = 0;      // 0=Heads, 1=Torsos, 2=Arms, 3=Legs, 4=Backpacks, 5=Weapons

save_custom_blueprint = function() {
    if (!instance_exists(obj_GameManager) || !instance_exists(obj_BlueprintManager)) return false;
    var _gm = obj_GameManager;
    var _pts = _gm.inventory.parts;
    if (assembly_head_idx < 0 || assembly_head_idx >= array_length(_pts.heads)) return false;
    if (assembly_torso_idx < 0 || assembly_torso_idx >= array_length(_pts.torsos)) return false;
    if (assembly_arms_idx < 0 || assembly_arms_idx >= array_length(_pts.arms)) return false;
    if (assembly_legs_idx < 0 || assembly_legs_idx >= array_length(_pts.legs)) return false;
    if (assembly_bp_idx < 0 || assembly_bp_idx >= array_length(_pts.backpacks)) return false;
    if (assembly_wp_idx < 0 || assembly_wp_idx >= array_length(_pts.weapons)) return false;

    var _hd = _pts.heads[assembly_head_idx];
    var _tr = _pts.torsos[assembly_torso_idx];
    var _am = _pts.arms[assembly_arms_idx];
    var _lg = _pts.legs[assembly_legs_idx];
    var _bp = _pts.backpacks[assembly_bp_idx];
    var _wp = _pts.weapons[assembly_wp_idx];

    var _draw = _hd.power_draw + _am.power_draw + _lg.power_draw + _bp.power_draw + _wp.power_draw;
    var _net = _tr.power_output - _draw;
    if (_net < 0) {
        show_toast("CANNOT ARCHIVE: Reactor Overload! Fix power draw first.", c_red);
        return false;
    }

    var _tot_armor = _hd.armor + _tr.armor + _am.armor + _lg.armor + _bp.armor + _wp.armor;
    var _tot_mass = _hd.mass + _tr.mass + _am.mass + _lg.mass + _bp.mass + _wp.mass;
    var _walk = max(20, floor(_lg.base_speed * (1.0 - (_tot_mass / 220.0))));
    var _boost = _walk + _bp.boost_bonus;
    var _code = "PMC-" + string_upper(string_copy(assembly_custom_name, 1, 6)) + "-" + string(irandom_range(10, 99));

    var _weight_class = "MEDIUM MAINSTAY";
    if (_tot_mass < 55) _weight_class = "LIGHT SKIRMISHER";
    else if (_tot_mass >= 55 && _tot_mass < 85) _weight_class = "MEDIUM MAINSTAY";
    else if (_tot_mass >= 85 && _tot_mass < 110) _weight_class = "HEAVY ASSAULT";
    else _weight_class = "SUPERHEAVY SIEGEBREAKER";

    var _bp_id = "bp_custom_" + string_lower(string_replace_all(assembly_custom_name, " ", "_")) + "_" + string(irandom(9999));
    var _new_bp = {
        id: _bp_id,
        blueprint_id: _bp_id,
        model_code: _code,
        name: assembly_custom_name,
        faction_id: "player",
        class: _weight_class,
        role: "Modular PMC Canonical Design (" + _wp.bonus + ")",
        tier: (_tot_armor > 1400 || _wp.damage > 350) ? 3 : 2,
        armor_rating: _tot_armor,
        structure_hp: floor(_tot_armor * 2.2),
        power_output_mw: _tr.power_output * 50,
        heat_dispersion_rate: 35.0,
        walk_speed_kph: _walk,
        boost_speed_kph: _boost,
        height_meters: 18.0,
        empty_weight_tonnes: floor(_tot_mass * 0.7),
        combat_weight_tonnes: _tot_mass,
        reactor_type: _tr.name,
        metal_type: _tr.req_alloy ?? "Custom Sintered Alloy Matrix",
        alloy_cost: { tungsten: 25, silica: 15, flux: 10, tritium: 5 },
        armament: [_wp.name, _hd.bonus, _bp.bonus],
        variants: [assembly_custom_name + " Mk.I Standard", assembly_custom_name + " Commander Custom"],
        associated_sprite: spr_ms_ironclad_idle,
        schematic_sprite: spr_mech_schematic,
        fabrication_cost_cr: floor((_tot_armor * 180) + (_wp.damage * 400)),
        manufacturing_lore: "Custom modular chassis engineered in the PMC Assembly Bay combining " + _hd.name + ", " + _tr.name + ", and " + _wp.name + ".",
        battlefield_reputation: "Bespoke PMC combat frame with high synergy tuning."
    };

    obj_BlueprintManager.register_custom_blueprint(_new_bp);
    show_toast("ARCHIVED TO CANONICAL BLUEPRINTS: " + assembly_custom_name + " (" + _code + ")!", c_lime);
    return true;
};

// 6. Fly-Off Procurement Trials & Interstellar Commodity Trade State (docs/15)
trial_selected_faction = "faction_a";
trial_selected_mech_idx = 0;
trial_last_result = undefined;
trial_phase = 0;              // 0 = Hangar Selection, 1 = Static Audit, 2 = Stress Gauntlet, 3 = Combat Fly-Off, 4 = Final Board Ratification
trial_refinements = [];       // Array of emergency field refinements applied during active trial
trial_phase_results = undefined; // Phase result struct
trial_view_adoption_panel = false; // Toggle to view adopted fleet management vs new trial
trade_selected_faction = "faction_a";
trade_selected_cat = 0;
trade_scroll_offset = 0;

// 2. UI Toast Notifications
toast_message = "WELCOME COMMANDER // ALL SYSTEMS NOMINAL";
toast_color = make_color_rgb(100, 220, 255);
toast_timer = 180;           // 3.0 seconds

show_toast = function(_msg, _col = c_white) {
    toast_message = _msg;
    toast_color = _col;
    toast_timer = 200;
};

// 3. Alert Ticker Feed (docs/09_ui_ux_flow.md)
alerts_feed = [
    "TERRAN HIGH COMMAND: Fortification contract awarded for Sector 4 defense line.",
    "OUTER COLONIES INTEL: High-spec fusion core prototypes sought by ace vanguard pilots.",
    "SYNDICATE COMMS: Black market smugglers offering synthetic flux for unlogged munitions.",
    "TACTICAL ALERT: Pirate reconnaissance sighted near Asteroid Belt mining claims."
];
alert_index = 0;
alert_timer = 0;

// 4. Modal Dialogs & In-Engine Tutorial Manual State
active_tutorial_modal = "";        // "" = None, "PMC_MANUAL", "CRUCIBLE", "REACTOR", "HYDRAULIC", "THRUSTER"
show_turn_briefing_modal = false; // Modal displaying last strategic turn's transaction ledger

// 5. Turn-Based Alloy Crucible Synthesis (docs/02_alloy_chemistry.md)
crucible_temp_c = 25.0;            // Ambient room temperature
crucible_pressure_psi = 14.7;      // Standard atmospheric pressure
volatility_meter = 0.0;            // 0.0 to 100.0%
crucible_shake = 0.0;              // Camera / UI shake
chamber_glow_alpha = 0.0;
crucible_batch = {
    mat_tungsten: 0,
    mat_silica_carb: 0,
    mat_syn_flux: 0,
    mat_tritium: 0
};

// Discrete Thermal & Pressure Methods (Turn-Based / Step-Based)
crucible_heat = function(_delta) {
    crucible_temp_c = clamp(crucible_temp_c + _delta, 25.0, 5000.0);
    scr_audio_play_sfx(snd_plasma_weld, 0.6, 0.08);
    // Thermal expansion increases pressure
    crucible_pressure_psi = clamp(crucible_pressure_psi + (_delta * 1.8), 14.7, 10000.0);
    chamber_glow_alpha = clamp(crucible_temp_c / 4500.0, 0.0, 1.0);
    if (crucible_batch.mat_tritium > 0 && crucible_batch.mat_syn_flux > 0) {
        volatility_meter = clamp(volatility_meter + (_delta * 0.03), 0, 100);
    }
};

crucible_cool = function(_delta) {
    crucible_temp_c = clamp(crucible_temp_c - _delta, 25.0, 5000.0);
    scr_audio_play_sfx(snd_mech_boost, 0.5, 0.08);
    crucible_pressure_psi = clamp(crucible_pressure_psi - (_delta * 1.2), 14.7, 10000.0);
    chamber_glow_alpha = clamp(crucible_temp_c / 4500.0, 0.0, 1.0);
};

crucible_compress = function(_delta) {
    crucible_pressure_psi = clamp(crucible_pressure_psi + _delta, 14.7, 10000.0);
    scr_audio_play_sfx(snd_hydraulic_press, 0.7, 0.05);
    if (crucible_batch.mat_tritium > 0 && crucible_batch.mat_syn_flux > 0) {
        volatility_meter = clamp(volatility_meter + (_delta * 0.02), 0, 100);
    }
};

crucible_vent = function() {
    crucible_pressure_psi = max(14.7, crucible_pressure_psi - 800.0);
    crucible_temp_c = max(25.0, crucible_temp_c - 150.0);
    volatility_meter = max(0.0, volatility_meter - 35.0);
    scr_audio_play_sfx(snd_mech_boost, 0.75, 0.12);
    crucible_shake = 6.0;
    chamber_glow_alpha = clamp(crucible_temp_c / 4500.0, 0.0, 1.0);
    show_toast("VENT VALVES OPENED: -800 PSI / -35% VOLATILITY", c_aqua);
};

crucible_load_mat = function(_mat_id) {
    if (!instance_exists(obj_GameManager)) return;
    var _available = obj_GameManager.inventory.raw_materials[$ _mat_id] ?? 0;
    if (_available > 0) {
        obj_GameManager.inventory.raw_materials[$ _mat_id] = _available - 1;
        crucible_batch[$ _mat_id] = (crucible_batch[$ _mat_id] ?? 0) + 1;
        scr_audio_play_ui("click");
        if (crucible_batch.mat_tritium > 0 && crucible_batch.mat_syn_flux > 0) {
            volatility_meter = min(100, volatility_meter + 25.0);
        }
        show_toast("HOPPER LOADED: +1 " + _mat_id, c_lime);
    } else {
        show_toast("INVENTORY DEPLETED: No " + _mat_id + " in warehouse!", c_red);
    }
};

crucible_purge_hopper = function() {
    if (!instance_exists(obj_GameManager)) return;
    var _keys = variable_struct_get_names(crucible_batch);
    for (var i = 0; i < array_length(_keys); i++) {
        var _k = _keys[i];
        var _amt = crucible_batch[$ _k];
        if (_amt > 0) {
            obj_GameManager.add_raw_material(_k, _amt);
            crucible_batch[$ _k] = 0;
        }
    }
    volatility_meter = 0.0;
    show_toast("HOPPER PURGED: Materials returned to storage.", c_yellow);
};

crucible_execute_synthesis = function() {
    if (!instance_exists(obj_GameManager)) return;

    // Check Volatility Failure
    if (volatility_meter >= 90.0) {
        crucible_shake = 26.0;
        crucible_batch.mat_tungsten = 0;
        crucible_batch.mat_silica_carb = 0;
        crucible_batch.mat_syn_flux = 0;
        crucible_batch.mat_tritium = 0;
        volatility_meter = 0.0;
        obj_GameManager.add_raw_material("item_slag", 2);
        show_toast("CATASTROPHIC BREACH! Volatility spiked -> Batch destroyed to Slag!", c_red);
        scr_audio_play_sfx(snd_explosion_large, 1.0, 0.05);
        return;
    }

    // Recipe 1: Vanguard Composite Plating (docs/02)
    // 2 Tungsten, 1 Silica-Carbon | Temp 2200°C - 2500°C | Pressure < 1200 PSI
    if (crucible_batch.mat_tungsten == 2 && crucible_batch.mat_silica_carb == 1 &&
        crucible_batch.mat_syn_flux == 0 && crucible_batch.mat_tritium == 0) {

        if (crucible_temp_c < 2200.0) {
            show_toast("SYNTHESIS FAILED: Underheated! Requires at least 2200°C.", c_red);
            return;
        }
        if (crucible_temp_c > 2550.0) {
            crucible_batch.mat_tungsten = 0;
            crucible_batch.mat_silica_carb = 0;
            obj_GameManager.add_raw_material("item_slag", 1);
            show_toast("OVERHEAT FAILURE: Carbon burned off -> Contaminated into Slag!", c_red);
            return;
        }
        if (crucible_pressure_psi > 1200.0) {
            show_toast("PRESSURE OVERLOAD: Exceeds 1200 PSI! Vent chamber before cooking.", c_red);
            return;
        }

        // Success!
        crucible_batch.mat_tungsten = 0;
        crucible_batch.mat_silica_carb = 0;
        obj_GameManager.add_alloy("alloy_vanguard_comp", 1);
        crucible_shake = 8.0;
        show_toast("SUCCESS: +1 Vanguard Composite Plating forged into inventory!", c_lime);
        scr_audio_play_sfx(snd_crucible_pour, 0.9, 0.04);
        scr_audio_play_sfx(snd_discovery_fanfare, 1.0, 0.0);
        return;
    }

    // Recipe 2: Hyperion Superconductor Matrix (docs/02)
    // 1 Tritium, 1 Synthetic Flux, 1 Tungsten | Temp 4000°C - 4500°C | Pressure 4000 - 8000 PSI
    if (crucible_batch.mat_tritium >= 1 && crucible_batch.mat_syn_flux >= 1 && crucible_batch.mat_tungsten >= 1) {
        if (crucible_temp_c < 4000.0 || crucible_temp_c > 4600.0) {
            show_toast("THERMAL MISALIGNMENT: Must be within 4000°C - 4500°C band!", c_red);
            return;
        }
        if (crucible_pressure_psi < 4000.0) {
            show_toast("INSUFFICIENT PRESSURE: Requires at least 4,000 PSI compression!", c_red);
            return;
        }

        crucible_batch.mat_tritium--;
        crucible_batch.mat_syn_flux--;
        crucible_batch.mat_tungsten--;
        volatility_meter = 0.0;
        obj_GameManager.add_alloy("alloy_hyperion_matrix", 1);
        crucible_shake = 16.0;
        show_toast("MASTERWORK FORGE: +1 Hyperion Superconductor Matrix synthesized!", c_lime);
        return;
    }

    // Recipe 3: Aerosteel Vernier Flux (docs/13)
    // 1 Silica-Carbon, 2 Synthetic Flux | Temp 1800°C - 2200°C | Pressure < 1200 PSI
    if (crucible_batch.mat_silica_carb >= 1 && crucible_batch.mat_syn_flux >= 2 &&
        crucible_batch.mat_tungsten == 0 && crucible_batch.mat_tritium == 0) {
        if (crucible_temp_c < 1800.0 || crucible_temp_c > 2250.0) {
            show_toast("THERMAL MISALIGNMENT: Aerosteel requires 1800°C - 2200°C!", c_red);
            return;
        }
        if (crucible_pressure_psi > 1200.0) {
            show_toast("PRESSURE OVERLOAD: Aerosteel requires low pressure (<1200 PSI)!", c_red);
            return;
        }
        crucible_batch.mat_silica_carb--;
        crucible_batch.mat_syn_flux -= 2;
        volatility_meter = 0.0;
        obj_GameManager.add_alloy("alloy_aerosteel_flux", 1);
        crucible_shake = 10.0;
        show_toast("SUCCESS: +1 Aerosteel Vernier Flux Alloy forged into inventory!", c_lime);
        return;
    }

    // Recipe 4: Adamantine Heavy Carbide (docs/13)
    // 3 Tungsten, 1 Silica-Carbon, 1 Synthetic Flux | Temp 3000°C - 3500°C | Pressure >= 3000 PSI
    if (crucible_batch.mat_tungsten >= 3 && crucible_batch.mat_silica_carb >= 1 && crucible_batch.mat_syn_flux >= 1 &&
        crucible_batch.mat_tritium == 0) {
        if (crucible_temp_c < 3000.0 || crucible_temp_c > 3550.0) {
            show_toast("THERMAL MISALIGNMENT: Adamantine requires 3000°C - 3500°C!", c_red);
            return;
        }
        if (crucible_pressure_psi < 3000.0) {
            show_toast("INSUFFICIENT PRESSURE: Adamantine requires at least 3,000 PSI!", c_red);
            return;
        }
        crucible_batch.mat_tungsten -= 3;
        crucible_batch.mat_silica_carb--;
        crucible_batch.mat_syn_flux--;
        volatility_meter = 0.0;
        obj_GameManager.add_alloy("alloy_adamantine_carbide", 1);
        crucible_shake = 14.0;
        show_toast("SUCCESS: +1 Adamantine Heavy Carbide forged into inventory!", c_lime);
        return;
    }

    // Recipe 5: Reactive Damascus Steel (Canonical Tier 5 Masterwork)
    // 3 Tungsten, 2 Synthetic Flux, 1 Tritium | Temp 3400°C - 3800°C | Pressure 4500 - 7000 PSI
    if (crucible_batch.mat_tungsten >= 3 && crucible_batch.mat_syn_flux >= 2 && crucible_batch.mat_tritium >= 1 &&
        crucible_batch.mat_silica_carb == 0) {
        if (crucible_temp_c < 3400.0 || crucible_temp_c > 3800.0) {
            show_toast("THERMAL MISALIGNMENT: Damascus requires 3400°C - 3800°C sintering!", c_red);
            return;
        }
        if (crucible_pressure_psi < 4500.0 || crucible_pressure_psi > 7000.0) {
            show_toast("PRESSURE MISALIGNMENT: Damascus requires 4,500 - 7,000 PSI!", c_red);
            return;
        }
        crucible_batch.mat_tungsten -= 3;
        crucible_batch.mat_syn_flux -= 2;
        crucible_batch.mat_tritium--;
        volatility_meter = 0.0;
        obj_GameManager.add_alloy("alloy_reactive_damascus", 1);
        crucible_shake = 16.0;
        show_toast("CANONICAL FORGE: +1 Reactive Damascus Composite synthesized! (+35% Kinetic Res)", c_lime);
        return;
    }

    // Recipe 6: Tachyon Superalloy Superconductor (Canonical Tier 5 Apex)
    // 1 Tungsten, 2 Tritium, 2 Synthetic Flux | Temp 4600°C - 4950°C | Pressure 8000 - 10000 PSI
    if (crucible_batch.mat_tungsten >= 1 && crucible_batch.mat_tritium >= 2 && crucible_batch.mat_syn_flux >= 2 &&
        crucible_batch.mat_silica_carb == 0) {
        if (crucible_temp_c < 4600.0 || crucible_temp_c > 4950.0) {
            show_toast("THERMAL MISALIGNMENT: Tachyon Superalloy requires extreme 4600°C - 4950°C!", c_red);
            return;
        }
        if (crucible_pressure_psi < 8000.0) {
            show_toast("INSUFFICIENT PRESSURE: Tachyon Superalloy requires at least 8,000 PSI!", c_red);
            return;
        }
        crucible_batch.mat_tungsten--;
        crucible_batch.mat_tritium -= 2;
        crucible_batch.mat_syn_flux -= 2;
        volatility_meter = 0.0;
        obj_GameManager.add_alloy("alloy_tachyon_superalloy", 1);
        crucible_shake = 22.0;
        show_toast("APEX DISCOVERY: +1 Tachyon Superalloy Lattice synthesized! (+40% Energy Dmg)", c_aqua);
        return;
    }

    // Recipe 7: Lunar Aerogel Ultralight Matrix (Canonical Tier 4 Advanced)
    // 3 Silica-Carbon, 2 Synthetic Flux | Temp 1700°C - 2100°C | Pressure <= 800 PSI (Low Pressure)
    if (crucible_batch.mat_silica_carb >= 3 && crucible_batch.mat_syn_flux >= 2 &&
        crucible_batch.mat_tungsten == 0 && crucible_batch.mat_tritium == 0) {
        if (crucible_temp_c < 1700.0 || crucible_temp_c > 2100.0) {
            show_toast("THERMAL MISALIGNMENT: Lunar Aerogel requires 1700°C - 2100°C!", c_red);
            return;
        }
        if (crucible_pressure_psi > 800.0) {
            show_toast("PRESSURE OVERLOAD: Aerogel requires vacuum chamber (<800 PSI)! Vent valves!", c_red);
            return;
        }
        crucible_batch.mat_silica_carb -= 3;
        crucible_batch.mat_syn_flux -= 2;
        volatility_meter = 0.0;
        obj_GameManager.add_alloy("alloy_lunar_aerogel", 1);
        crucible_shake = 8.0;
        show_toast("FEATHERWEIGHT FORGE: +1 Lunar Aerogel Matrix synthesized! (-40% Mass)", c_white);
        return;
    }

    // Recipe 8: Sol Ferrite Magnetic Matrix (Canonical Tier 5 Masterwork)
    // 3 Tungsten, 1 Silica-Carbon, 2 Tritium | Temp 4100°C - 4400°C | Pressure 5500 - 8500 PSI
    if (crucible_batch.mat_tungsten >= 3 && crucible_batch.mat_silica_carb >= 1 && crucible_batch.mat_tritium >= 2 &&
        crucible_batch.mat_syn_flux == 0) {
        if (crucible_temp_c < 4100.0 || crucible_temp_c > 4400.0) {
            show_toast("THERMAL MISALIGNMENT: Sol Ferrite requires 4100°C - 4400°C!", c_red);
            return;
        }
        if (crucible_pressure_psi < 5500.0 || crucible_pressure_psi > 8500.0) {
            show_toast("PRESSURE MISALIGNMENT: Sol Ferrite requires 5500 - 8500 PSI!", c_red);
            return;
        }
        crucible_batch.mat_tungsten -= 3;
        crucible_batch.mat_silica_carb--;
        crucible_batch.mat_tritium -= 2;
        volatility_meter = 0.0;
        obj_GameManager.add_alloy("alloy_sol_ferrite", 1);
        crucible_shake = 18.0;
        show_toast("MAGNETIC APEX: +1 Sol Ferrite High-Permeability Ingot forged! (+45% Velocity)", c_yellow);
        return;
    }

    // 5. Procedural Combinatorial Metallurgy Engine (docs/14)
    var _discovery = scr_alloy_discovery_analyze(crucible_batch, crucible_temp_c, crucible_pressure_psi);
    if (_discovery.is_failure) {
        crucible_shake = 18.0;
        crucible_purge_hopper();
        obj_GameManager.add_raw_material("item_slag", 2);
        show_toast("SYNTHESIS FAILED (" + _discovery.name + "): " + _discovery.failure_reason, c_red);
        return;
    } else {
        crucible_shake = 12.0;
        scr_alloy_codex_register_discovery(_discovery);
        obj_GameManager.add_alloy(_discovery.code, 1);
        crucible_purge_hopper();
        show_toast("DISCOVERY FORGED: " + _discovery.name + " (" + _discovery.hex + ") added to inventory!", c_lime);
        return;
    }
};

// 6. Prototyping Minigames State (docs/03_prototyping_minigames.md)
active_minigame = 0; // 0 = Reactor Wave Tuning, 1 = Limb Stress Alignment, 2 = Thruster Calibration

// --- MINIGAME 0: Reactor Conduit Wave Tuning (Turn-Based) ---
wave_target_freq = 2.4;
wave_target_amp = 48.0;
wave_target_phase = 72.0;

slider_freq = 1.0;     // 0.5 to 4.0
slider_amp = 30.0;     // 15.0 to 75.0
slider_phase = 0.0;    // 0.0 to 360.0
dragging_slider = -1;  // 0: freq, 1: amp, 2: phase

reactor_alignment_pct = 0.0;
reactor_complete = false;
reactor_last_score = 0.0;
reactor_last_grade = "UNTESTED";

test_reactor_pulse = function() {
    reactor_alignment_pct = clamp(100.0 - (abs(slider_freq - wave_target_freq) * 32.0 + abs(slider_amp - wave_target_amp) * 1.1 + abs(slider_phase - wave_target_phase) * 0.32), 0.0, 100.0);
    reactor_last_score = reactor_alignment_pct;

    if (reactor_last_score >= 95.0) reactor_last_grade = "S";
    else if (reactor_last_score >= 85.0) reactor_last_grade = "A";
    else if (reactor_last_score >= 70.0) reactor_last_grade = "B";
    else if (reactor_last_score >= 50.0) reactor_last_grade = "C";
    else reactor_last_grade = "D";

    if (instance_exists(obj_BlueprintManager)) {
        var _r = obj_BlueprintManager.active_prototype_tuning.reactor;
        _r.score = reactor_last_score;
        _r.grade = reactor_last_grade;
        if (reactor_last_grade == "S") {
            _r.output_mult = 1.25; _r.heat_diss_mult = 1.35; _r.energy_dmg_mult = 1.20; _r.en_cap_mult = 1.30;
        } else if (reactor_last_grade == "A") {
            _r.output_mult = 1.15; _r.heat_diss_mult = 1.20; _r.energy_dmg_mult = 1.10; _r.en_cap_mult = 1.15;
        } else if (reactor_last_grade == "B") {
            _r.output_mult = 1.05; _r.heat_diss_mult = 1.10; _r.energy_dmg_mult = 1.05; _r.en_cap_mult = 1.05;
        } else if (reactor_last_grade == "C") {
            _r.output_mult = 1.00; _r.heat_diss_mult = 1.00; _r.energy_dmg_mult = 1.00; _r.en_cap_mult = 1.00;
        } else {
            _r.output_mult = 0.85; _r.heat_diss_mult = 0.75; _r.energy_dmg_mult = 0.90; _r.en_cap_mult = 0.85;
        }
    }

    if (reactor_last_grade == "S" || reactor_last_grade == "A") {
        reactor_complete = true;
        if (instance_exists(obj_BlueprintManager)) {
            obj_BlueprintManager.add_masterwork({
                id: "mw_core_hyperion_" + string(current_time),
                name: (reactor_last_grade == "S" ? "S-Rank Flawless Tokamak Core (+25% MW)" : "Masterwork Hyperion Tokamak Core (+15% MW)"),
                slot: "REACTOR",
                bonus: (reactor_last_grade == "S" ? "+25% Net Surplus & +35% Cooling" : "+15% Net Power Surplus"),
                grade: reactor_last_grade
            });
        }
        show_toast("HARMONIC LOCK [" + reactor_last_grade + "-RANK]: " + string_format(reactor_alignment_pct, 1, 1) + "%! Power Output +" + string(floor((obj_BlueprintManager.active_prototype_tuning.reactor.output_mult - 1.0) * 100)) + "%!", c_lime);
    } else if (reactor_last_grade == "B") {
        show_toast("STABLE HARMONICS [B-RANK]: " + string_format(reactor_alignment_pct, 1, 1) + "% (+5% Power, +10% Cooling). Fine-tune for S-Rank!", c_yellow);
    } else if (reactor_last_grade == "C") {
        show_toast("STANDARD LINE HARMONICS [C-RANK]: " + string_format(reactor_alignment_pct, 1, 1) + "%. Baseline specs.", c_orange);
    } else {
        show_toast("CONTAINMENT INSTABILITY [D-RANK]: " + string_format(reactor_alignment_pct, 1, 1) + "%. Power output penalized by -15%!", c_red);
    }
};

// --- MINIGAME 1: Limb Hydraulic Stress Alignment (Action-Based Budget) ---
limb_actions_budget = 8;
selected_limb_joint = 0;
limb_complete = false;
limb_last_score = 0.0;
limb_last_grade = "UNTESTED";

limb_joints = [
    { name: "Hip Actuator", rel_x: 120, rel_y: 90, stress: 62.0, locked: false },
    { name: "Knee Hydraulic", rel_x: 110, rel_y: 190, stress: 18.0, locked: false },
    { name: "Ankle Gyro", rel_x: 125, rel_y: 280, stress: 70.0, locked: false },
    { name: "Foot Stabilizer", rel_x: 100, rel_y: 340, stress: 24.0, locked: false }
];

reset_limb_sim = function() {
    limb_actions_budget = 8;
    limb_complete = false;
    limb_joints[0].stress = 62.0; limb_joints[0].locked = false;
    limb_joints[1].stress = 18.0; limb_joints[1].locked = false;
    limb_joints[2].stress = 70.0; limb_joints[2].locked = false;
    limb_joints[3].stress = 24.0; limb_joints[3].locked = false;
    show_toast("HYDRAULIC BENCH RESET: 8 Pulses Allocated.", c_white);
};

limb_relieve_joint = function(_idx) {
    if (limb_actions_budget <= 0) { show_toast("PULSE BUDGET DEPLETED! Reset bench to try again.", c_red); return; }
    if (limb_joints[_idx].locked) { show_toast("JOINT LOCKED: Already spot-welded into place!", c_orange); return; }
    limb_actions_budget--;
    limb_joints[_idx].stress = max(5.0, limb_joints[_idx].stress - 16.0);
    // Neighboring joints take slight backpressure
    if (_idx > 0 && !limb_joints[_idx - 1].locked) limb_joints[_idx - 1].stress = min(100.0, limb_joints[_idx - 1].stress + 4.0);
    if (_idx < 3 && !limb_joints[_idx + 1].locked) limb_joints[_idx + 1].stress = min(100.0, limb_joints[_idx + 1].stress + 4.0);
    show_toast("RELIEVED PRESSURE: " + limb_joints[_idx].name + " (-16% Stress)", c_aqua);
};

limb_tighten_joint = function(_idx) {
    if (limb_actions_budget <= 0) { show_toast("PULSE BUDGET DEPLETED! Reset bench to try again.", c_red); return; }
    if (limb_joints[_idx].locked) { show_toast("JOINT LOCKED: Already spot-welded into place!", c_orange); return; }
    limb_actions_budget--;
    limb_joints[_idx].stress = min(100.0, limb_joints[_idx].stress + 14.0);
    if (_idx > 0 && !limb_joints[_idx - 1].locked) limb_joints[_idx - 1].stress = max(5.0, limb_joints[_idx - 1].stress - 3.0);
    if (_idx < 3 && !limb_joints[_idx + 1].locked) limb_joints[_idx + 1].stress = max(5.0, limb_joints[_idx + 1].stress - 3.0);
    show_toast("TIGHTENED CYLINDER: " + limb_joints[_idx].name + " (+14% Stress)", c_yellow);
};

limb_weld_joint = function(_idx) {
    if (limb_actions_budget <= 0) { show_toast("PULSE BUDGET DEPLETED! Reset bench to try again.", c_red); return; }
    var _cur = limb_joints[_idx].stress;
    if (_cur >= 25.0 && _cur <= 45.0) {
        limb_actions_budget--;
        limb_joints[_idx].locked = true;
        show_toast("SPOT-WELD LOCKED: " + limb_joints[_idx].name + " balanced inside safe tolerance!", c_lime);

        // Check if all 4 locked
        var _all_locked = true;
        var _locked_cnt = 0;
        for (var j = 0; j < 4; j++) {
            if (limb_joints[j].locked) _locked_cnt++;
            else _all_locked = false;
        }

        if (_all_locked || limb_actions_budget == 0) {
            limb_complete = _all_locked;
            limb_last_score = clamp((_locked_cnt / 4.0) * 70.0 + (limb_actions_budget / 8.0) * 30.0, 0.0, 100.0);
            if (!_all_locked) limb_last_score = max(20.0, limb_last_score - 20.0);

            if (limb_last_score >= 95.0) limb_last_grade = "S";
            else if (limb_last_score >= 85.0) limb_last_grade = "A";
            else if (limb_last_score >= 70.0) limb_last_grade = "B";
            else if (limb_last_score >= 50.0) limb_last_grade = "C";
            else limb_last_grade = "D";

            if (instance_exists(obj_BlueprintManager)) {
                var _h = obj_BlueprintManager.active_prototype_tuning.hydraulics;
                _h.score = limb_last_score;
                _h.grade = limb_last_grade;
                if (limb_last_grade == "S") {
                    _h.pilot_limit_pct = 200; _h.recoil_mult = 1.30; _h.ap_bonus = 1; _h.leg_armor_mult = 1.25;
                } else if (limb_last_grade == "A") {
                    _h.pilot_limit_pct = 175; _h.recoil_mult = 1.20; _h.ap_bonus = 0; _h.leg_armor_mult = 1.15;
                } else if (limb_last_grade == "B") {
                    _h.pilot_limit_pct = 145; _h.recoil_mult = 1.10; _h.ap_bonus = 0; _h.leg_armor_mult = 1.05;
                } else if (limb_last_grade == "C") {
                    _h.pilot_limit_pct = 115; _h.recoil_mult = 1.00; _h.ap_bonus = 0; _h.leg_armor_mult = 1.00;
                } else {
                    _h.pilot_limit_pct = 90; _h.recoil_mult = 0.85; _h.ap_bonus = -1; _h.leg_armor_mult = 0.85;
                }

                if (_all_locked) {
                    obj_BlueprintManager.add_masterwork({
                        id: "mw_legs_colossus_" + string(current_time),
                        name: (limb_last_grade == "S" ? "S-Rank Prototype Colossus Walkers (Limit 200%)" : "Masterwork Colossus Walkers (Limit 175%)"),
                        slot: "LEGS",
                        bonus: (limb_last_grade == "S" ? "+30% Recoil, Limit 200%, +1 AP" : "+20% Recoil, Limit 175%"),
                        grade: limb_last_grade
                    });
                }
            }
            show_toast("HYDRAULIC BENCH [" + limb_last_grade + "-RANK]: " + string(floor(limb_last_score)) + "%! Pilot Limit (Genkai) set to " + string(obj_BlueprintManager.active_prototype_tuning.hydraulics.pilot_limit_pct) + "%!", c_lime);
        }
    } else {
        show_toast("CANNOT WELD: Stress (" + string(floor(_cur)) + "%) is outside optimal 25%-45% band!", c_red);
    }
};

// --- MINIGAME 2: Thruster Plasma Flow Calibration (Multi-Stage Resonance) ---
thruster_stage = 0; // 0 to 3
thruster_fuel = 50.0;
thruster_mag = 50.0;
thruster_complete = false;
thruster_last_score = 0.0;
thruster_last_grade = "UNTESTED";
thruster_stage_scores = [0.0, 0.0, 0.0, 0.0];

thruster_stages_info = [
    { title: "STAGE 1: IGNITION PRE-CHAMBER", target_fuel: 35.0, target_mag: 40.0, desc: "Ignite deuterium-tritium pilot flare under gentle magnetic confinement." },
    { title: "STAGE 2: MAGNETIC CHOKE CONSTRICTION", target_fuel: 55.0, target_mag: 65.0, desc: "Constrict plasma stream using high-gauss superconducting choke rings." },
    { title: "STAGE 3: VERNIER ACCELERATION RING", target_fuel: 75.0, target_mag: 60.0, desc: "Induce high-velocity magnetic acceleration into vector manifold." },
    { title: "STAGE 4: FULL VECTOR PLASMA DISCHARGE", target_fuel: 90.0, target_mag: 85.0, desc: "Achieve stoichiometric vector burn for maximum vacuum thrust." }
];

reset_thruster_sim = function() {
    thruster_stage = 0;
    thruster_fuel = 50.0;
    thruster_mag = 50.0;
    thruster_complete = false;
    show_toast("THRUSTER TEST BENCH RESET: Stage 1 initialized.", c_white);
};

commit_thruster_pulse = function() {
    if (thruster_stage >= 4) { show_toast("CALIBRATION COMPLETE: Vernier Thruster already finalized!", c_lime); return; }
    var _st = thruster_stages_info[thruster_stage];
    var _res = clamp(100.0 - abs(thruster_fuel - _st.target_fuel) * 1.5 - abs(thruster_mag - _st.target_mag) * 1.5, 0.0, 100.0);

    thruster_stage_scores[thruster_stage] = _res;

    if (_res >= 80.0) {
        thruster_stage++;
        if (thruster_stage >= 4) {
            thruster_complete = true;
            thruster_last_score = (thruster_stage_scores[0] + thruster_stage_scores[1] + thruster_stage_scores[2] + thruster_stage_scores[3]) / 4.0;
            if (thruster_last_score >= 95.0) thruster_last_grade = "S";
            else if (thruster_last_score >= 85.0) thruster_last_grade = "A";
            else if (thruster_last_score >= 70.0) thruster_last_grade = "B";
            else if (thruster_last_score >= 50.0) thruster_last_grade = "C";
            else thruster_last_grade = "D";

            if (instance_exists(obj_BlueprintManager)) {
                var _t = obj_BlueprintManager.active_prototype_tuning.thrusters;
                _t.score = thruster_last_score;
                _t.grade = thruster_last_grade;
                if (thruster_last_grade == "S") {
                    _t.thrust_mult = 1.35; _t.evasion_bonus = 25; _t.space_terrain = "S"; _t.fuel_eff_mult = 1.35;
                } else if (thruster_last_grade == "A") {
                    _t.thrust_mult = 1.20; _t.evasion_bonus = 15; _t.space_terrain = "A"; _t.fuel_eff_mult = 1.20;
                } else if (thruster_last_grade == "B") {
                    _t.thrust_mult = 1.10; _t.evasion_bonus = 8; _t.space_terrain = "A"; _t.fuel_eff_mult = 1.10;
                } else if (thruster_last_grade == "C") {
                    _t.thrust_mult = 1.00; _t.evasion_bonus = 0; _t.space_terrain = "B"; _t.fuel_eff_mult = 1.00;
                } else {
                    _t.thrust_mult = 0.85; _t.evasion_bonus = -10; _t.space_terrain = "C"; _t.fuel_eff_mult = 0.75;
                }

                obj_BlueprintManager.add_masterwork({
                    id: "mw_thruster_vernier_" + string(current_time),
                    name: (thruster_last_grade == "S" ? "S-Rank Dual-Vector Vernier (+35% Thrust, S-Space)" : "Masterwork Dual-Vector Vernier (+20% Thrust)"),
                    slot: "BACKPACK",
                    bonus: (thruster_last_grade == "S" ? "+35% Thrust, +25% Eva, Space: S" : "+20% Thrust, +15% Eva"),
                    grade: thruster_last_grade
                });
            }
            show_toast("THRUSTER RESONANCE [" + thruster_last_grade + "-RANK]: " + string(floor(thruster_last_score)) + "%! Thrust +" + string(floor((obj_BlueprintManager.active_prototype_tuning.thrusters.thrust_mult - 1.0) * 100)) + "%, Evasion +" + string(obj_BlueprintManager.active_prototype_tuning.thrusters.evasion_bonus) + "%!", c_lime);
        } else {
            show_toast("STAGE CLEARED (" + string(floor(_res)) + "% Resonance)! Advanced to " + thruster_stages_info[thruster_stage].title, c_lime);
        }
    } else {
        show_toast("FLAMEOUT / DESYNC (" + string(floor(_res)) + "%): Adjust Fuel Injection and Magnetic Coil flux!", c_red);
    }
};

// UI Spark Particles
spark_particles = [];

// 7. Modular Component Specifications Database (docs/01, 09)
spec_view_mode = 0;       // 0 = Full Mech Blueprint, 1 = Modular Component Inspector

// 7b. Mobile Suit Blueprint Archive & Inventory Schematics Browser (Docs 01, 12, 13)
bp_archive_source = 0;             // 0 = Active Fleet Inventory, 1 = Canonical Blueprint Database
bp_archive_faction_filter = "all"; // "all", "faction_terran", "faction_colony", "faction_syndicate", "faction_zaibatsu", "player"
bp_archive_selected_idx = 0;       // Index in currently filtered list
bp_archive_view_mode = 0;          // 0 = Tactical Sprite & Alloy Tint, 1 = Technical Schematics, 2 = Modular Components, 3 = Production Variants
bp_archive_scroll = 0;             // Scroll offset for left list
bp_archive_dossier_tab = 0;        // 0 = Specs & Armament, 1 = Global Stats & Attrition, 2 = Historical & Dynamic Lore
bp_archive_chronicle_scroll = 0;   // Scroll offset for dynamic chronicle entries

// 7c. Metallurgy Codex, Periodic Table & Solar Mining UI State (Docs 02, 06, 14)
crucible_subview = 0;              // 0 = Furnace & Batch Preview, 1 = Discovered Alloy Codex, 2 = 118-Element Periodic Table
pt_view_category = "all";          // Category filter for 118 elements
pt_selected_idx = 0;               // Selected element index in periodic table
pt_scroll_offset = 0;              // Scroll offset for periodic table
codex_selected_idx = 0;            // Selected discovered alloy in codex
codex_scroll_offset = 0;           // Scroll offset for codex
mining_sphere_filter = "all";      // Solar sphere filter for mining nodes
mining_scroll_offset = 0;          // Scroll offset for solar mining nodes


comp_specs_data = [
    {
        name: "Hyperion Tokamak Fusion Core",
        slot: "REACTOR CORE",
        sprite: spr_comp_reactor,
        power_output: "1,200 MW (+160 MW Surplus)",
        dry_mass: "18.5 Tonnes",
        heat_dissipation: "35 °C / sec",
        alloys: "2x Vanguard Composite, 8x Refined Tungsten",
        desc: "High-density magnetic plasma containment chamber with cryogenic tritium injection. Powers high-drain solid kinetic and energy loadouts."
    },
    {
        name: "Colossus Hydraulic Bipedal Walkers",
        slot: "REVERSE-JOINT LEGS",
        sprite: spr_comp_legs,
        power_output: "Drain: 180 MW",
        dry_mass: "32.0 Tonnes (Load Limit: 110t)",
        heat_dissipation: "Shock Dampening: +45%",
        alloys: "4x Vanguard Composite, 15x Tungsten",
        desc: "Dual-chamber high-pressure hydraulic cylinders with heavy foot pads. Designed for massive recoil absorption and rough trench traversal."
    },
    {
        name: "Type-77 120mm Solid-Slug Autocannon",
        slot: "PRIMARY ARMAMENT",
        sprite: spr_comp_weapon,
        power_output: "Drain: 120 MW / AP Cost: 3",
        dry_mass: "14.2 Tonnes",
        heat_dissipation: "Heat Per Shot: 15°C",
        alloys: "2x Vanguard Composite, 12x Tungsten",
        desc: "Heavy drum-fed kinetic rotary cannon firing depleted-uranium/tungsten AP shells. Devastating kinetic punch against enemy torso plating."
    },
    {
        name: "Ares-IV Armored Mono-Eye Sensor Array",
        slot: "TARGETING HEAD",
        sprite: spr_comp_head,
        power_output: "Drain: 65 MW",
        dry_mass: "6.8 Tonnes",
        heat_dissipation: "Sensor Range: 950m (19 Grid Cells)",
        alloys: "1x Vanguard Composite, 4x Synthetic Flux",
        desc: "Visored mono-eye tracking optics with thermal and radar telemetry antennae. Provides +25% hit accuracy and battlefield target lock."
    },
    {
        name: "Heavy Armored Torso Chassis",
        slot: "CENTRAL CHASSIS",
        sprite: spr_comp_torso,
        power_output: "Structural Integrity: 650 HP",
        dry_mass: "28.0 Tonnes",
        heat_dissipation: "Twin Cowling Exhaust Heat Sinks",
        alloys: "6x Vanguard Composite, 20x Tungsten",
        desc: "Multi-layered composite ballistic chest block protecting cockpit and reactor core. Features armored louvers for thermal heat dispersion."
    },
    {
        name: "Dual-Vector Plasma Vernier Backpack",
        slot: "THRUSTER BACKPACK",
        sprite: spr_comp_thruster,
        power_output: "Thrust: 42,000 kN / AP Cost: 2",
        dry_mass: "12.5 Tonnes",
        heat_dissipation: "Thermal Dissipation Fins",
        alloys: "2x Vanguard Composite, 6x Tritium",
        desc: "Gimballed dual vector plasma nozzles with acceleration rings. Enables high-G tactical dashes and substantial evasion boost."
    }
];

show_debug_message("[obj_HQTerminal] Initialization Complete. Ready for command input.");

// 5b. Modular Part Fabrication Catalog (docs/13)
modular_crafting_catalog = [
    // Heads (Slot 0)
    [
        { id: "hd_vanguard_01", name: "HD-01 Vanguard Target-Lock", slot: "heads", armor: 120, mass: 4, power_draw: 2, bonus: "+15% Accuracy", req_alloy: "alloy_vanguard_comp", req_alloy_amount: 1, cost_cr: 15000 },
        { id: "hd_aether_02", name: "HD-02 Aether EW-Dome", slot: "heads", armor: 90, mass: 2, power_draw: 4, bonus: "+18% Evasion", req_alloy: "alloy_aerosteel_flux", req_alloy_amount: 1, cost_cr: 25000 },
        { id: "hd_cyclops_03", name: "HD-03 Cyclops Siege Optic", slot: "heads", armor: 160, mass: 6, power_draw: 3, bonus: "+20% Critical Hit", req_alloy: "alloy_adamantine_carbide", req_alloy_amount: 1, cost_cr: 35000 },
        { id: "hd_damascus_04", name: "HD-04 Damascus Reactive Visor", slot: "heads", armor: 195, mass: 5, power_draw: 3, bonus: "+25% Kinetic Res & Target Lock", req_alloy: "alloy_reactive_damascus", req_alloy_amount: 1, cost_cr: 48000 },
        { id: "hd_tachyon_05", name: "HD-05 Tachyon Spectral Dome", slot: "heads", armor: 110, mass: 3, power_draw: 5, bonus: "+30% Beam Crit & Deep Radar", req_alloy: "alloy_tachyon_superalloy", req_alloy_amount: 1, cost_cr: 62000 }
    ],
    // Torsos (Slot 1)
    [
        { id: "tr_colossus_01", name: "TR-01 Colossus Heavy Torso", slot: "torsos", armor: 480, mass: 26, power_output: 28, bonus: "Reinforced Reactor Core", req_alloy: "alloy_vanguard_comp", req_alloy_amount: 3, cost_cr: 65000 },
        { id: "tr_hyperion_02", name: "TR-02 Hyperion Tokamak Torso", slot: "torsos", armor: 360, mass: 20, power_output: 42, bonus: "High-Spec Fusion Core", req_alloy: "alloy_hyperion_matrix", req_alloy_amount: 2, cost_cr: 95000 },
        { id: "tr_phantom_03", name: "TR-03 Phantom Striker Torso", slot: "torsos", armor: 300, mass: 14, power_output: 32, bonus: "Lightweight Agility Core", req_alloy: "alloy_aerosteel_flux", req_alloy_amount: 2, cost_cr: 75000 },
        { id: "tr_damascus_04", name: "TR-04 Damascus Reactive Citadel", slot: "torsos", armor: 560, mass: 28, power_output: 36, bonus: "Ablative Blast Deflection Core", req_alloy: "alloy_reactive_damascus", req_alloy_amount: 2, cost_cr: 115000 },
        { id: "tr_sol_05", name: "TR-05 Sol Ferrite Super-Tokamak", slot: "torsos", armor: 440, mass: 22, power_output: 54, bonus: "Apex Tokamak Core (+54 MW Output)", req_alloy: "alloy_sol_ferrite", req_alloy_amount: 2, cost_cr: 135000 }
    ],
    // Arms (Slot 2)
    [
        { id: "am_colossus_01", name: "AM-01 Colossus Dual Arms", slot: "arms", armor: 260, mass: 16, power_draw: 4, bonus: "+25% Recoil Control", req_alloy: "alloy_vanguard_comp", req_alloy_amount: 2, cost_cr: 40000 },
        { id: "am_vernier_02", name: "AM-02 Vernier Fast-Actuators", slot: "arms", armor: 190, mass: 10, power_draw: 5, bonus: "+20% Weapon Handling", req_alloy: "alloy_aerosteel_flux", req_alloy_amount: 2, cost_cr: 50000 },
        { id: "am_adamant_03", name: "AM-03 Adamantine Heavy Brackets", slot: "arms", armor: 320, mass: 22, power_draw: 6, bonus: "+20% Ballistic Damage", req_alloy: "alloy_adamantine_carbide", req_alloy_amount: 2, cost_cr: 60000 },
        { id: "am_aerogel_04", name: "AM-04 Lunar Aerogel Manipulators", slot: "arms", armor: 210, mass: 7, power_draw: 3, bonus: "-55% Arm Mass & +25% Melee Speed", req_alloy: "alloy_lunar_aerogel", req_alloy_amount: 2, cost_cr: 72000 },
        { id: "am_tachyon_05", name: "AM-05 Tachyon Conduit Arms", slot: "arms", armor: 240, mass: 12, power_draw: 7, bonus: "+35% Energy Weapon Output", req_alloy: "alloy_tachyon_superalloy", req_alloy_amount: 2, cost_cr: 88000 }
    ],
    // Legs (Slot 3)
    [
        { id: "lg_vanguard_01", name: "LG-01 Vanguard Heavy Walkers", slot: "legs", armor: 340, mass: 24, power_draw: 5, base_speed: 44, bonus: "+30% Stability", req_alloy: "alloy_vanguard_comp", req_alloy_amount: 3, cost_cr: 55000 },
        { id: "lg_stratos_02", name: "LG-02 Stratos Vernier Skaters", slot: "legs", armor: 220, mass: 15, power_draw: 7, base_speed: 86, bonus: "+25% Agility", req_alloy: "alloy_aerosteel_flux", req_alloy_amount: 2, cost_cr: 70000 },
        { id: "lg_titan_03", name: "LG-03 Titan Quad-Leg Platform", slot: "legs", armor: 440, mass: 34, power_draw: 8, base_speed: 34, bonus: "+50% Recoil Absorb", req_alloy: "alloy_adamantine_carbide", req_alloy_amount: 3, cost_cr: 80000 },
        { id: "lg_aerogel_04", name: "LG-04 Lunar Aerogel Hover Struts", slot: "legs", armor: 260, mass: 11, power_draw: 6, base_speed: 105, bonus: "High-G Hover Dash & Terrain Master", req_alloy: "alloy_lunar_aerogel", req_alloy_amount: 2, cost_cr: 92000 },
        { id: "lg_damascus_05", name: "LG-05 Damascus Armored Treads", slot: "legs", armor: 520, mass: 32, power_draw: 7, base_speed: 48, bonus: "Impenetrable Trench Fortress", req_alloy: "alloy_reactive_damascus", req_alloy_amount: 3, cost_cr: 105000 }
    ],
    // Backpacks (Slot 4)
    [
        { id: "bp_heavy_01", name: "BP-01 Heavy Booster Pack", slot: "backpacks", armor: 140, mass: 12, power_draw: 3, boost_bonus: 35, bonus: "High Thrust", req_alloy: "alloy_vanguard_comp", req_alloy_amount: 1, cost_cr: 25000 },
        { id: "bp_vernier_02", name: "BP-02 Dual-Vector Vernier Rig", slot: "backpacks", armor: 100, mass: 8, power_draw: 6, boost_bonus: 65, bonus: "+15% Evade", req_alloy: "alloy_aerosteel_flux", req_alloy_amount: 2, cost_cr: 45000 },
        { id: "bp_plasma_03", name: "BP-03 Plasma Overcharge Booster", slot: "backpacks", armor: 120, mass: 10, power_draw: 9, boost_bonus: 80, bonus: "+1 Dash AP", req_alloy: "alloy_hyperion_matrix", req_alloy_amount: 2, cost_cr: 65000 },
        { id: "bp_aerogel_04", name: "BP-04 Lunar Aerogel Siphon Rig", slot: "backpacks", armor: 95, mass: 4, power_draw: 4, boost_bonus: 55, bonus: "+60% Heat Venting & Featherweight", req_alloy: "alloy_lunar_aerogel", req_alloy_amount: 2, cost_cr: 78000 },
        { id: "bp_tachyon_05", name: "BP-05 Tachyon Fold Warp Booster", slot: "backpacks", armor: 130, mass: 11, power_draw: 12, boost_bonus: 115, bonus: "+2 Sortie AP & Micro-Warp Dash", req_alloy: "alloy_tachyon_superalloy", req_alloy_amount: 2, cost_cr: 110000 }
    ],
    // Weapons (Slot 5)
    [
        { id: "wp_vulcan_01", name: "WP-01 Rotary Vulcan (120mm)", slot: "weapons", armor: 100, mass: 12, power_draw: 3, damage: 180, bonus: "Sustained Fire", req_alloy: "alloy_adamantine_carbide", req_alloy_amount: 2, cost_cr: 45000 },
        { id: "wp_beam_02", name: "WP-02 Particle Beam Pulse Rifle", slot: "weapons", armor: 80, mass: 8, power_draw: 10, damage: 240, bonus: "Armor Piercing", req_alloy: "alloy_hyperion_matrix", req_alloy_amount: 2, cost_cr: 60000 },
        { id: "wp_rail_03", name: "WP-03 Heavy Siege Rail Cannon", slot: "weapons", armor: 130, mass: 20, power_draw: 8, damage: 380, bonus: "Long Range Siege", req_alloy: "alloy_adamantine_carbide", req_alloy_amount: 2, cost_cr: 85000 },
        { id: "wp_sol_04", name: "WP-04 Sol Ferrite Hyper-Railgun", slot: "weapons", armor: 150, mass: 22, power_draw: 11, damage: 460, bonus: "+45% Shield Pierce & Line Punch", req_alloy: "alloy_sol_ferrite", req_alloy_amount: 2, cost_cr: 125000 },
        { id: "wp_tachyon_05", name: "WP-05 Tachyon Beam Lance", slot: "weapons", armor: 90, mass: 9, power_draw: 14, damage: 420, bonus: "+40% Energy Armor Melt & Overheat Arc", req_alloy: "alloy_tachyon_superalloy", req_alloy_amount: 2, cost_cr: 140000 }
    ]
];

// 27. Mobile Suit Universe Encyclopedia & Mass-Production Candidate Dossier (docs/29 & docs/30)
catalog_view_mode = 0; // 0 = Standard Dossier, 1 = 100-Suit Encyclopedia Browser
catalog_selected_suit_id = "ms_terran_ironclad_07";
catalog_selected_idx = 0;
catalog_filter_faction = "ALL"; // "ALL", "faction_a", "faction_b", "faction_c", "faction_d"
catalog_filter_era = 0; // 0 = All, 1, 2, 3, 4
catalog_anim_state = "idle"; // "idle", "walk", "fire", "hit"
catalog_facing = 1; // 1 = Right, -1 = Left
catalog_perspective = "front"; // "front", "back"
catalog_scroll_offset = 0;
trial_candidate_dossier_idx = 0; // 0..3 for inspecting the 4 mass production candidates
trial_view_candidates_mode = false; // Toggle between flyoff arena and candidate pool comparison
