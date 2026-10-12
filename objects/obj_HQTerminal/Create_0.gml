/// @description obj_HQTerminal Create Event
// Unified Command Deck Terminal UI State Machine & Simulation Hub
// Strictly implements docs/09_ui_ux_flow.md, docs/02_alloy_chemistry.md & docs/03_prototyping_minigames.md

show_debug_message("[obj_HQTerminal] Initializing Command Deck Terminal Controller...");

// Bootstrap persistent system managers if not present
if (!instance_exists(obj_GameManager)) instance_create_depth(0, 0, 0, obj_GameManager);
if (!instance_exists(obj_FactionManager)) instance_create_depth(0, 0, 0, obj_FactionManager);
if (!instance_exists(obj_BlueprintManager)) instance_create_depth(0, 0, 0, obj_BlueprintManager);

// 1. Navigation State
active_tab = 0;              // 0 = R&D Lab, 1 = Factory Floor, 2 = Contracts, 3 = War Map
rd_subtab = 0;               // 0 = Crucible Synthesis (Doc 02), 1 = Prototyping Minigames (Doc 03), 2 = Blueprint Specs
war_subtab = 0;              // 0 = Sector War Map & Mining, 1 = Faction Dossiers & Liaisons, 2 = Decade Mecha Timeline (Y205-Y215)
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
    // Thermal expansion increases pressure
    crucible_pressure_psi = clamp(crucible_pressure_psi + (_delta * 1.8), 14.7, 10000.0);
    chamber_glow_alpha = clamp(crucible_temp_c / 4500.0, 0.0, 1.0);
    if (crucible_batch.mat_tritium > 0 && crucible_batch.mat_syn_flux > 0) {
        volatility_meter = clamp(volatility_meter + (_delta * 0.03), 0, 100);
    }
};

crucible_cool = function(_delta) {
    crucible_temp_c = clamp(crucible_temp_c - _delta, 25.0, 5000.0);
    crucible_pressure_psi = clamp(crucible_pressure_psi - (_delta * 1.2), 14.7, 10000.0);
    chamber_glow_alpha = clamp(crucible_temp_c / 4500.0, 0.0, 1.0);
};

crucible_compress = function(_delta) {
    crucible_pressure_psi = clamp(crucible_pressure_psi + _delta, 14.7, 10000.0);
    if (crucible_batch.mat_tritium > 0 && crucible_batch.mat_syn_flux > 0) {
        volatility_meter = clamp(volatility_meter + (_delta * 0.02), 0, 100);
    }
};

crucible_vent = function() {
    crucible_pressure_psi = max(14.7, crucible_pressure_psi - 800.0);
    crucible_temp_c = max(25.0, crucible_temp_c - 150.0);
    volatility_meter = max(0.0, volatility_meter - 35.0);
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

    show_toast("INVALID BATCH: Material ratio does not match any known formula!", c_orange);
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

test_reactor_pulse = function() {
    reactor_alignment_pct = clamp(100.0 - (abs(slider_freq - wave_target_freq) * 32.0 + abs(slider_amp - wave_target_amp) * 1.1 + abs(slider_phase - wave_target_phase) * 0.32), 0.0, 100.0);
    if (reactor_alignment_pct >= 90.0) {
        reactor_complete = true;
        if (instance_exists(obj_BlueprintManager)) {
            obj_BlueprintManager.add_masterwork({
                id: "mw_core_hyperion_" + string(current_time),
                name: "Masterwork Hyperion Tokamak Core (+15% MW)",
                slot: "REACTOR",
                bonus: "+15% Net Power Surplus",
                grade: "MASTERWORK"
            });
        }
        show_toast("HARMONIC LOCK ACHIEVED! Masterwork Reactor Core forged!", c_lime);
    } else if (reactor_alignment_pct >= 70.0) {
        show_toast("STABLE HARMONICS: Alignment at " + string_format(reactor_alignment_pct, 1, 1) + "%. Fine-tune to reach 90% for Masterwork!", c_yellow);
    } else {
        show_toast("CONDUIT DESYNC: Alignment only " + string_format(reactor_alignment_pct, 1, 1) + "%. Adjust frequency and phase!", c_red);
    }
};

// --- MINIGAME 1: Limb Hydraulic Stress Alignment (Action-Based Budget) ---
limb_actions_budget = 8;
selected_limb_joint = 0;
limb_complete = false;

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
        for (var j = 0; j < 4; j++) {
            if (!limb_joints[j].locked) _all_locked = false;
        }
        if (_all_locked) {
            limb_complete = true;
            if (instance_exists(obj_BlueprintManager)) {
                obj_BlueprintManager.add_masterwork({
                    id: "mw_legs_colossus_" + string(current_time),
                    name: "Masterwork Colossus Hydraulic Walkers (+20% Recoil)",
                    slot: "LEGS",
                    bonus: "+20% Recoil Absorption & +1 AP",
                    grade: "MASTERWORK"
                });
            }
            show_toast("ALL JOINTS BALANCED! Masterwork Colossus Hydraulics forged!", c_lime);
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

    if (_res >= 80.0) {
        thruster_stage++;
        if (thruster_stage >= 4) {
            thruster_complete = true;
            if (instance_exists(obj_BlueprintManager)) {
                obj_BlueprintManager.add_masterwork({
                    id: "mw_thruster_vernier_" + string(current_time),
                    name: "Masterwork Dual-Vector Vernier Backpack (+25% Evasion)",
                    slot: "BACKPACK",
                    bonus: "+25% Evasion & Instant Boost",
                    grade: "MASTERWORK"
                });
            }
            show_toast("RESONANCE 100%! Masterwork Dual-Vector Vernier Backpack forged!", c_lime);
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
selected_comp_idx = 0;    // 0 = Reactor, 1 = Legs, 2 = Cannon, 3 = Head, 4 = Torso, 5 = Thruster

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
        { id: "hd_cyclops_03", name: "HD-03 Cyclops Siege Optic", slot: "heads", armor: 160, mass: 6, power_draw: 3, bonus: "+20% Critical Hit", req_alloy: "alloy_adamantine_carbide", req_alloy_amount: 1, cost_cr: 35000 }
    ],
    // Torsos (Slot 1)
    [
        { id: "tr_colossus_01", name: "TR-01 Colossus Heavy Torso", slot: "torsos", armor: 480, mass: 26, power_output: 28, bonus: "Reinforced Reactor Core", req_alloy: "alloy_vanguard_comp", req_alloy_amount: 3, cost_cr: 65000 },
        { id: "tr_hyperion_02", name: "TR-02 Hyperion Tokamak Torso", slot: "torsos", armor: 360, mass: 20, power_output: 42, bonus: "High-Spec Fusion Core", req_alloy: "alloy_hyperion_matrix", req_alloy_amount: 2, cost_cr: 95000 },
        { id: "tr_phantom_03", name: "TR-03 Phantom Striker Torso", slot: "torsos", armor: 300, mass: 14, power_output: 32, bonus: "Lightweight Agility Core", req_alloy: "alloy_aerosteel_flux", req_alloy_amount: 2, cost_cr: 75000 }
    ],
    // Arms (Slot 2)
    [
        { id: "am_colossus_01", name: "AM-01 Colossus Dual Arms", slot: "arms", armor: 260, mass: 16, power_draw: 4, bonus: "+25% Recoil Control", req_alloy: "alloy_vanguard_comp", req_alloy_amount: 2, cost_cr: 40000 },
        { id: "am_vernier_02", name: "AM-02 Vernier Fast-Actuators", slot: "arms", armor: 190, mass: 10, power_draw: 5, bonus: "+20% Weapon Handling", req_alloy: "alloy_aerosteel_flux", req_alloy_amount: 2, cost_cr: 50000 },
        { id: "am_adamant_03", name: "AM-03 Adamantine Heavy Brackets", slot: "arms", armor: 320, mass: 22, power_draw: 6, bonus: "+20% Ballistic Damage", req_alloy: "alloy_adamantine_carbide", req_alloy_amount: 2, cost_cr: 60000 }
    ],
    // Legs (Slot 3)
    [
        { id: "lg_vanguard_01", name: "LG-01 Vanguard Heavy Walkers", slot: "legs", armor: 340, mass: 24, power_draw: 5, base_speed: 44, bonus: "+30% Stability", req_alloy: "alloy_vanguard_comp", req_alloy_amount: 3, cost_cr: 55000 },
        { id: "lg_stratos_02", name: "LG-02 Stratos Vernier Skaters", slot: "legs", armor: 220, mass: 15, power_draw: 7, base_speed: 86, bonus: "+25% Agility", req_alloy: "alloy_aerosteel_flux", req_alloy_amount: 2, cost_cr: 70000 },
        { id: "lg_titan_03", name: "LG-03 Titan Quad-Leg Platform", slot: "legs", armor: 440, mass: 34, power_draw: 8, base_speed: 34, bonus: "+50% Recoil Absorb", req_alloy: "alloy_adamantine_carbide", req_alloy_amount: 3, cost_cr: 80000 }
    ],
    // Backpacks (Slot 4)
    [
        { id: "bp_heavy_01", name: "BP-01 Heavy Booster Pack", slot: "backpacks", armor: 140, mass: 12, power_draw: 3, boost_bonus: 35, bonus: "High Thrust", req_alloy: "alloy_vanguard_comp", req_alloy_amount: 1, cost_cr: 25000 },
        { id: "bp_vernier_02", name: "BP-02 Dual-Vector Vernier Rig", slot: "backpacks", armor: 100, mass: 8, power_draw: 6, boost_bonus: 65, bonus: "+15% Evade", req_alloy: "alloy_aerosteel_flux", req_alloy_amount: 2, cost_cr: 45000 },
        { id: "bp_plasma_03", name: "BP-03 Plasma Overcharge Booster", slot: "backpacks", armor: 120, mass: 10, power_draw: 9, boost_bonus: 80, bonus: "+1 Dash AP", req_alloy: "alloy_hyperion_matrix", req_alloy_amount: 2, cost_cr: 65000 }
    ],
    // Weapons (Slot 5)
    [
        { id: "wp_vulcan_01", name: "WP-01 Rotary Vulcan (120mm)", slot: "weapons", armor: 100, mass: 12, power_draw: 3, damage: 180, bonus: "Sustained Fire", req_alloy: "alloy_adamantine_carbide", req_alloy_amount: 2, cost_cr: 45000 },
        { id: "wp_beam_02", name: "WP-02 Particle Beam Pulse Rifle", slot: "weapons", armor: 80, mass: 8, power_draw: 10, damage: 240, bonus: "Armor Piercing", req_alloy: "alloy_hyperion_matrix", req_alloy_amount: 2, cost_cr: 60000 },
        { id: "wp_rail_03", name: "WP-03 Heavy Siege Rail Cannon", slot: "weapons", armor: 130, mass: 20, power_draw: 8, damage: 380, bonus: "Long Range Siege", req_alloy: "alloy_adamantine_carbide", req_alloy_amount: 2, cost_cr: 85000 }
    ]
];