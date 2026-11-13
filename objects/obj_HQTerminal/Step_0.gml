/// @description obj_HQTerminal Step Event
// Turn-based UI controller, discrete draggable inputs, and spark particle dynamics
// Strictly adheres to docs/02_alloy_chemistry.md, docs/03_prototyping_minigames.md & docs/09_ui_ux_flow.md

// 1. Toast & Alert Timers
if (toast_timer > 0) toast_timer--;

alert_timer++;
if (alert_timer >= 320) {
    alert_timer = 0;
    alert_index = (alert_index + 1) % array_length(alerts_feed);
}

// 2. Camera / UI Screen Shake Recovery
crucible_shake = max(0.0, crucible_shake - 0.7);

// 3. Update Spark Particles
for (var i = array_length(spark_particles) - 1; i >= 0; i--) {
    var _sp = spark_particles[i];
    _sp.x += _sp.vx;
    _sp.y += _sp.vy;
    _sp.life -= 0.05;
    if (_sp.life <= 0) {
        array_delete(spark_particles, i, 1);
    }
}


// Modal Freeze: If Debug Menu is open, halt background HQ inputs
if (instance_exists(obj_DebugManager) && obj_DebugManager.is_open) {
    exit;
}

// Foundry Activation Prologue: Prompt Commander to calibrate USN-X Hephaestus lineage after prologue
if (instance_exists(obj_GameManager) && obj_GameManager.has_completed_prologue && !obj_GameManager.has_calibrated_foundry && !scr_vn_is_active() && !intro_active && !show_commander_modal) {
    scr_vn_start_episode("ep_foundry_calibration");
}

// 4. Global Hotkey Shortcuts (docs/09)
if (keyboard_check_pressed(vk_f5)) {
    scr_save_game();
}
if (keyboard_check_pressed(vk_f9)) {
    scr_load_game();
}
if (keyboard_check_pressed(vk_f1) || keyboard_check_pressed(ord("H"))) {
    active_tutorial_modal = (active_tutorial_modal == "") ? "PMC_MANUAL" : "";
}
if (keyboard_check_pressed(ord("L"))) {
    show_turn_briefing_modal = !show_turn_briefing_modal;
}
// Mute audio toggle shortcut [M]
if (keyboard_check_pressed(ord("M"))) {
    var _now_muted = scr_audio_toggle_mute();
    show_toast(_now_muted ? "[AUDIO MUTED]" : "[AUDIO UNMUTED - " + string(floor(scr_audio_get_master_volume() * 100)) + "%]", _now_muted ? c_orange : c_lime);
}

// Settings modal toggle shortcut [O]
if (keyboard_check_pressed(ord("O"))) {
    show_settings_modal = !show_settings_modal;
    scr_audio_play_ui("click");
}

if (keyboard_check_pressed(vk_escape)) {
    if (show_settings_modal) {
        show_settings_modal = false;
        scr_audio_play_ui("cancel");
    } else if (scr_research_get_system() != undefined && scr_research_get_system().dossier_tech_id != "") {
        scr_research_get_system().dossier_tech_id = "";
        scr_audio_play_ui("cancel");
    } else if (instance_exists(obj_GameManager) && obj_GameManager.show_campaign_victory_modal) {
        obj_GameManager.show_campaign_victory_modal = false;
        scr_audio_play_ui("cancel");
    } else {
        active_tutorial_modal = "";
        show_turn_briefing_modal = false;
        showing_retire_modal = false;
        if (instance_exists(obj_GameManager)) {
            obj_GameManager.career_summary = undefined;
            obj_GameManager.pending_raid = undefined;
        }
        show_commander_modal = false;
        combat_modal_active = false;
        order_modal_active = false;
        order_dispatch_mode = false;
        if (earth_view_mode == "STRONGHOLD") earth_view_mode = "GLOBAL";
        scr_audio_play_ui("cancel");
    }
}

// Goal H: Universal Number Keys 1-5 for Primary Tabs, Q/E for Subtabs, and Space for Turn Advance
if (!show_settings_modal && !intro_active && !show_commander_modal) {
    if (keyboard_check_pressed(ord("1"))) { active_tab = 3; scr_audio_play_ui("tab"); scr_audio_play_location_bgm("hq"); }
    if (keyboard_check_pressed(ord("2"))) { active_tab = 1; scr_audio_play_ui("tab"); scr_audio_play_location_bgm("hq"); }
    if (keyboard_check_pressed(ord("3"))) { active_tab = 0; scr_audio_play_ui("tab"); scr_audio_play_location_bgm("prototyping"); }
    if (keyboard_check_pressed(ord("4"))) { active_tab = 2; scr_audio_play_ui("tab"); scr_audio_play_location_bgm("hq"); }
    if (keyboard_check_pressed(ord("5"))) { active_tab = 4; scr_audio_play_ui("tab"); scr_audio_play_location_bgm("hq"); }
    if (keyboard_check_pressed(ord("6"))) { active_tab = 5; scr_audio_play_ui("tab"); scr_audio_play_location_bgm("hq"); }

    // Subtab Cycling Q and E
    if (keyboard_check_pressed(ord("Q"))) {
        if (active_tab == 3) territory_sphere_tab = (territory_sphere_tab - 1 + 3) % 3;
        else if (active_tab == 1) factory_subtab = (factory_subtab - 1 + 3) % 3;
        else if (active_tab == 0) { rd_subtab = (rd_subtab - 1 + 3) % 3; research_subtab = (research_subtab - 1 + 4) % 4; }
        else if (active_tab == 2) contracts_subtab = (contracts_subtab - 1 + 3) % 3;
        else if (active_tab == 4) flagship_subtab = (flagship_subtab - 1 + 2) % 2;
        else if (active_tab == 5) pilot_deck_subtab = (pilot_deck_subtab - 1 + 3) % 3;
        scr_audio_play_ui("tab");
    }
    if (keyboard_check_pressed(ord("E"))) {
        if (active_tab == 3) territory_sphere_tab = (territory_sphere_tab + 1) % 3;
        else if (active_tab == 1) factory_subtab = (factory_subtab + 1) % 3;
        else if (active_tab == 0) { rd_subtab = (rd_subtab + 1) % 3; research_subtab = (research_subtab + 1) % 4; }
        else if (active_tab == 2) contracts_subtab = (contracts_subtab + 1) % 3;
        else if (active_tab == 4) flagship_subtab = (flagship_subtab + 1) % 2;
        else if (active_tab == 5) pilot_deck_subtab = (pilot_deck_subtab + 1) % 3;
        scr_audio_play_ui("tab");
    }

    if (keyboard_check_pressed(ord("S")) || keyboard_check_pressed(ord("C"))) {
        if (room_exists(rm_combat)) {
            if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "tutorial_step") && obj_GameManager.tutorial_step == 3) {
                obj_GameManager.tutorial_step = 4;
            }
            scr_audio_play_ui("confirm");
            room_goto(rm_combat);
        }
    }

    // Goal G: K Hotkey to launch Apex Crisis Boss Sortie
    if (keyboard_check_pressed(ord("K"))) {
        launch_crisis_boss_sortie();
    }

    if (keyboard_check_pressed(vk_space)) {
        if (instance_exists(obj_GameManager)) {
            obj_GameManager.end_turn();
            scr_audio_play_ui("confirm");
        }
    }
}

// Interactive Intro Modal Keyboard Controls (Space / Enter to proceed)
if (intro_active || show_commander_modal) {
    if (keyboard_check_pressed(vk_space) || keyboard_check_pressed(vk_enter)) {
        if (intro_page == 0) {
            intro_page = 1;
            scr_audio_play_ui("click");
        } else if (intro_page == 1) {
            if (instance_exists(obj_GameManager)) {
                obj_GameManager.select_commander(selected_commander_choice);
                obj_GameManager.has_completed_intro = true;
            }
            intro_active = false;
            show_commander_modal = false;
            scr_audio_play_ui("confirm");
            scr_audio_play_ui("boot");
            scr_audio_play_location_bgm((active_tab == 0) ? "prototyping" : "hq");
        }
    }
    if (keyboard_check_pressed(vk_escape)) {
        if (intro_page == 1) {
            intro_page = 0;
            scr_audio_play_ui("click");
        } else if (show_commander_modal && !intro_active) {
            show_commander_modal = false;
            scr_audio_play_ui("cancel");
        }
    }
}

// 5. Minigame 0: Real-Time Slider Alignment Computation
if (active_tab == 0 && rd_subtab == 1 && active_minigame == 0) {
    reactor_alignment_pct = clamp(100.0 - (abs(slider_freq - wave_target_freq) * 32.0 + abs(slider_amp - wave_target_amp) * 1.1 + abs(slider_phase - wave_target_phase) * 0.32), 0.0, 100.0);
}

// 6. Blueprint Archive Mouse Wheel Scrolling
if (active_tab == 0 && rd_subtab == 2) {
    if (mouse_wheel_up()) bp_archive_scroll = max(0, bp_archive_scroll - 1);
    if (mouse_wheel_down()) bp_archive_scroll += 1;
}

// 7. Metallurgy Codex, Periodic Table & Mining Nodes Mouse Wheel Scrolling
if (active_tab == 0 && rd_subtab == 0) {
    if (crucible_subview == 1) {
        if (mouse_wheel_up()) codex_scroll_offset = max(0, codex_scroll_offset - 1);
        if (mouse_wheel_down()) codex_scroll_offset += 1;
    } else if (crucible_subview == 2) {
        if (mouse_wheel_up()) pt_scroll_offset = max(0, pt_scroll_offset - 1);
        if (mouse_wheel_down()) pt_scroll_offset += 1;
    }
} else if (active_tab == 3 && war_subtab == 0) {
    if (mouse_wheel_up()) mining_scroll_offset = max(0, mining_scroll_offset - 1);
    if (mouse_wheel_down()) mining_scroll_offset += 1;
} else if (active_tab == 3 && war_subtab == 2) {
    if (mouse_wheel_up()) diplo_cables_scroll_offset = max(0, diplo_cables_scroll_offset - 1);
    if (mouse_wheel_down()) diplo_cables_scroll_offset += 1;
} else if (active_tab == 2 && contracts_subtab == 2) {
    if (mouse_wheel_up()) trade_scroll_offset = max(0, trade_scroll_offset - 1);
    if (mouse_wheel_down()) trade_scroll_offset += 1;
}
// 8. Update Active Hyperlane Transits (Shin Gihren's Greed Strike Wings)
for (var ti = array_length(active_transits) - 1; ti >= 0; ti--) {
    var _tr = active_transits[ti];
    _tr.progress += _tr.speed;

    // Thruster wake particles
    if (random(1.0) < 0.35) {
        var _px = lerp(_tr.origin_x, _tr.target_x, _tr.progress);
        var _py = lerp(_tr.origin_y, _tr.target_y, _tr.progress);
        array_push(spark_particles, {
            x: _px + random_range(-4, 4),
            y: _py + random_range(-4, 4),
            vx: random_range(-0.5, 0.5),
            vy: random_range(-0.5, 0.5),
            life: 0.5,
            col: _tr.is_combat ? make_color_rgb(255, 90, 80) : make_color_rgb(0, 220, 255)
        });
    }

    if (_tr.progress >= 1.0) {
        scr_territory_resolve_transit_arrival(_tr);
        array_delete(active_transits, ti, 1);
    }
}

// 9. Order Dispatch / Combat Modals Keyboard Dismiss
if (keyboard_check_pressed(vk_escape)) {
    if (combat_modal_active) {
        combat_modal_active = false;
        scr_audio_play_ui("cancel");
    } else if (order_modal_active) {
        order_modal_active = false;
        scr_audio_play_ui("cancel");
    } else if (order_dispatch_mode) {
        order_dispatch_mode = false;
        scr_audio_play_ui("cancel");
    }
}

// Stronghold View Zoom-Out via ESC
if (keyboard_check_pressed(vk_escape)) {
    if (earth_view_mode == "STRONGHOLD") {
        earth_view_mode = "GLOBAL";
        scr_audio_play_ui("cancel");
        scr_audio_play_location_bgm("hq");
    }
}

// =========================================================================
// 10. Shin Gihren's Greed Hex Tactical Turn / Keyboard Shortcuts
// =========================================================================
if (earth_view_mode == "STRONGHOLD") {
    // Press Space or E to Advance Cycle / End Turn
    if (keyboard_check_pressed(vk_space) || keyboard_check_pressed(ord("E"))) {
        if (!is_undefined(stronghold_terrain_grid) && array_length(stronghold_hex_units) > 0) {
            scr_audio_play_phase_horn();
            var _new_log = scr_stronghold_advance_turn(active_stronghold_id, stronghold_hex_units, stronghold_terrain_grid, hex_tactical_turn);
            for (var li = 0; li < array_length(_new_log); li++) {
                array_push(stronghold_combat_log, _new_log[li]);
            }
            while (array_length(stronghold_combat_log) > 10) {
                array_delete(stronghold_combat_log, 0, 1);
            }
            hex_tactical_turn++;
            selected_hex_unit_id = "";
            reachable_hexes = {};
            scr_hex_update_fog_of_war(stronghold_fog_grid, stronghold_hex_units, stronghold_terrain_grid);
        }
    }
    
    // Press G to toggle Hex Grid mesh
    if (keyboard_check_pressed(ord("G"))) {
        hex_grid_enabled = !hex_grid_enabled;
        scr_audio_play_ui("click");
    }

    // Press F to toggle Prometheus Flux Fog of War
    if (keyboard_check_pressed(ord("F"))) {
        fog_of_war_enabled = !fog_of_war_enabled;
        scr_audio_play_ui("click");
    }
}
