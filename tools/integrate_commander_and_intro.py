#!/usr/bin/env python3
"""
tools/integrate_commander_and_intro.py
Integrates:
1. Player Commander Dossier in obj_GameManager (Male / Female / Silhouette)
2. Interactive Situation Intro & Commander Selection in obj_HQTerminal
3. Atmospheric Location Backdrop Art (Hangar Bay for Tabs 0-1, War Room for Tabs 2-4)
4. Persistent Top HUD Commander Profile Badge
5. Audio synchronization for the intro sequence, commander selection, and room transitions
"""

import os
import re

# =============================================================================
# 1. UPDATE obj_GameManager/Create_0.gml
# =============================================================================
print("=== 1. UPDATING obj_GameManager/Create_0.gml ===")
with open("objects/obj_GameManager/Create_0.gml", "r") as f:
    gm_text = f.read()

commander_state_code = """// 3d. Player Commander Executive Dossier & New Game Intro State (Male / Female / Silhouette)
has_completed_intro = false;
player_commander = {
    id: "player_commander_01",
    callsign: "SHADOW",
    name: "Commander [CLASSIFIED]",
    gender: "silhouette", // "silhouette", "male", "female"
    portrait_asset: spr_portrait_commander_silhouette,
    rank: "Commander",
    pmc_name: "Iron Ridge Dynamics",
    flagship_name: "Pre-War Dreadnought Hephaestus",
    background: "Encrypted black-budget mercenary profile operating under an anonymous registry.",
    doctrine: "Black Ops Logistics (+10% Scrap Salvage, Volatility Dampening)",
    leadership: 9,
    tactics: 9,
    morale: 100
};

select_commander = function(_gender_type) {
    switch (_gender_type) {
        case "male":
            player_commander.gender = "male";
            player_commander.name = "Commander Alexei Kane";
            player_commander.callsign = "RAVEN";
            player_commander.portrait_asset = spr_portrait_commander_male;
            player_commander.background = "Former Terran Naval Strike Commander. Refused orbital saturation orders; founded an independent tactical design bureau.";
            player_commander.doctrine = "Heavy Vanguard (+12% Kinetic Armor, +10% Contract Bounty)";
            break;
        case "female":
            player_commander.gender = "female";
            player_commander.name = "Commander Morgan Vance";
            player_commander.callsign = "VALKYRIE";
            player_commander.portrait_asset = spr_portrait_commander_female;
            player_commander.background = "Former Colony Fleet Tactical Prodigy. Escaped Jovian corporate conscription to pioneer modular mobile suit metallurgy.";
            player_commander.doctrine = "Vernier Synthesis (+15% Prototyping Stability, +10% Thruster Evasion)";
            break;
        case "silhouette":
        default:
            player_commander.gender = "silhouette";
            player_commander.name = "Commander [CLASSIFIED]";
            player_commander.callsign = "SHADOW";
            player_commander.portrait_asset = spr_portrait_commander_silhouette;
            player_commander.background = "Encrypted black-budget mercenary profile operating under an anonymous registry.";
            player_commander.doctrine = "Black Ops Logistics (+10% Scrap Salvage, Volatility Dampening)";
            break;
    }
};
"""

target_era = 'timeline_era_year_start = 214;'
if "player_commander" not in gm_text:
    gm_text = gm_text.replace(target_era, target_era + "\n\n" + commander_state_code)
    with open("objects/obj_GameManager/Create_0.gml", "w") as f:
        f.write(gm_text)
    print("✓ Added player_commander state and select_commander() to obj_GameManager/Create_0.gml")

# =============================================================================
# 2. UPDATE obj_HQTerminal/Create_0.gml
# =============================================================================
print("=== 2. UPDATING obj_HQTerminal/Create_0.gml ===")
with open("objects/obj_HQTerminal/Create_0.gml", "r") as f:
    hq_c_text = f.read()

hq_intro_vars = """// Intro Briefing & Commander Selection State
intro_active = (instance_exists(obj_GameManager) && !obj_GameManager.has_completed_intro);
intro_page = 0; // 0 = Situation Briefing, 1 = Commander Selection Dossier
selected_commander_choice = "silhouette"; // "silhouette", "male", "female"
show_commander_modal = false;
"""

if "selected_commander_choice" not in hq_c_text:
    target_nav = "active_tab = 0;"
    hq_c_text = hq_c_text.replace(target_nav, hq_intro_vars + "\n" + target_nav)
    with open("objects/obj_HQTerminal/Create_0.gml", "w") as f:
        f.write(hq_c_text)
    print("✓ Added intro and commander state variables to obj_HQTerminal/Create_0.gml")

# =============================================================================
# 3. UPDATE obj_HQTerminal/Draw_64.gml (Atmospheric Backgrounds & HUD Badge)
# =============================================================================
print("=== 3. UPDATING obj_HQTerminal/Draw_64.gml ===")
with open("objects/obj_HQTerminal/Draw_64.gml", "r") as f:
    d64 = f.read()

# Add location backdrop art right after dark backdrop
bg_target = 'draw_rectangle(0, 0, _gw, _gh, false);'
loc_backdrop_code = """draw_rectangle(0, 0, _gw, _gh, false);

// Atmospheric Location Backdrop Art (Hangar Bay for Tabs 0-1, War Room for Tabs 2-4)
var _loc_bg = (active_tab == 0 || active_tab == 1) ? spr_loc_hangar_bay : spr_loc_war_room;
if (sprite_exists(_loc_bg)) {
    draw_sprite_ext(_loc_bg, 0, 0, 0, _gw / 1024.0, _gh / 576.0, 0, c_white, 0.24);
}"""

if "spr_loc_hangar_bay" not in d64:
    d64 = d64.replace(bg_target, loc_backdrop_code, 1)

# Add Commander Dossier HUD badge to Persistent Top HUD
hud_badge_target = 'draw_text(520 + _sx, 20 + _sy, "TURN " + string(_turn_val) + " // Y" + string(_year_val) + " D" + string(_day_val));'
hud_commander_badge = """draw_text(520 + _sx, 20 + _sy, "TURN " + string(_turn_val) + " // Y" + string(_year_val) + " D" + string(_day_val));

// Commander Profile Dossier Badge (Top HUD Right)
var _cmd_bx = 980 + _sx;
var _cmd_by = 8 + _sy;
var _cmd_bw = 280;
var _cmd_bh = 48;
var _cmd_hov = (_mx >= _cmd_bx && _mx <= _cmd_bx + _cmd_bw && _my >= _cmd_by && _my <= _cmd_by + _cmd_bh);

if (_cmd_hov && _click) {
    show_commander_modal = true;
    intro_page = 1;
    scr_audio_play_ui("click");
}

draw_set_color(_cmd_hov ? make_color_rgb(26, 45, 68) : make_color_rgb(16, 24, 34));
draw_rectangle(_cmd_bx, _cmd_by, _cmd_bx + _cmd_bw, _cmd_by + _cmd_bh, false);
draw_set_color(_cmd_hov ? make_color_rgb(100, 220, 255) : make_color_rgb(45, 80, 115));
draw_rectangle(_cmd_bx, _cmd_by, _cmd_bx + _cmd_bw, _cmd_by + _cmd_bh, true);

// Miniature Commander Portrait
var _c_port = spr_portrait_commander_silhouette;
var _c_name = "Commander [CLASSIFIED]";
var _c_call = "SHADOW";
var _c_rank = "Commander";
if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "player_commander")) {
    _c_port = obj_GameManager.player_commander.portrait_asset;
    _c_name = obj_GameManager.player_commander.name;
    _c_call = obj_GameManager.player_commander.callsign;
    _c_rank = obj_GameManager.player_commander.rank;
}

if (sprite_exists(_c_port)) {
    draw_sprite_ext(_c_port, 0, _cmd_bx + 4, _cmd_by + 4, 40.0 / 200.0, 40.0 / 200.0, 0, c_white, 1.0);
    draw_set_color(make_color_rgb(80, 150, 200));
    draw_rectangle(_cmd_bx + 4, _cmd_by + 4, _cmd_bx + 44, _cmd_by + 44, true);
}

draw_set_color(_cmd_hov ? c_white : make_color_rgb(200, 230, 255));
draw_text(_cmd_bx + 52, _cmd_by + 6, _c_name);
draw_set_color(make_color_rgb(120, 170, 210));
draw_text(_cmd_bx + 52, _cmd_by + 26, "[" + _c_call + "] // DOSSIER [VIEW]");"""

if "Commander Profile Dossier Badge" not in d64:
    d64 = d64.replace(hud_badge_target, hud_commander_badge)

# Add full-screen Situation Briefing and Commander Dossier Modal at end of Draw_64
modal_code = """
// =============================================================================
// INTERACTIVE SITUATION BRIEFING & COMMANDER PROFILE SETUP MODAL
// =============================================================================
if (intro_active || show_commander_modal) {
    // 1. Dark Translucent Overlay
    draw_set_color(c_black);
    draw_set_alpha(0.88);
    draw_rectangle(0, 0, _gw, _gh, false);
    draw_set_alpha(1.0);

    // Modal Canvas Dimensions
    var _mw = min(1140, _gw - 64);
    var _mh = min(680, _gh - 50);
    var _mx0 = (_gw - _mw) / 2;
    var _my0 = (_gh - _mh) / 2;

    // Outer Frame & Recessed Panel
    scr_draw_snes_panel(_mx0, _my0, _mw, _mh, "", -1, false, 0.08);

    // Top Header Banner
    draw_set_color(make_color_rgb(18, 30, 45));
    draw_rectangle(_mx0 + 2, _my0 + 2, _mx0 + _mw - 2, _my0 + 44, false);
    draw_set_color(make_color_rgb(60, 120, 180));
    draw_line(_mx0 + 2, _my0 + 44, _mx0 + _mw - 2, _my0 + 44);

    var _banner_title = (intro_page == 0) ? "TRANSMISSION INTERCEPT // THE SOLAR SCHISM (YEAR 215)" : "PMC EXECUTIVE COMMAND DECK // APPOINT COMMANDER DOSSIER";
    draw_set_color(make_color_rgb(100, 220, 255));
    draw_text(_mx0 + 20, _my0 + 12, _banner_title);

    // Header Subtitle / Page Indicator
    draw_set_color(make_color_rgb(255, 200, 80));
    draw_text(_mx0 + _mw - 260, _my0 + 12, (intro_page == 0) ? "[PHASE 1: SITUATION BRIEFING]" : "[PHASE 2: COMMANDER PROFILE]");

    // -------------------------------------------------------------------------
    // PAGE 0: SITUATION BRIEFING & GAME INTRO
    // -------------------------------------------------------------------------
    if (intro_page == 0) {
        var _bx = _mx0 + 32;
        var _by = _my0 + 64;
        var _bw = _mw - 64;

        // Visual Backdrop Vignette (War Room / Tactical Bridge)
        if (sprite_exists(spr_loc_war_room)) {
            draw_sprite_ext(spr_loc_war_room, 0, _bx, _by, _bw / 1024.0, 160.0 / 576.0, 0, c_white, 0.65);
            draw_set_color(make_color_rgb(80, 180, 255));
            draw_rectangle(_bx, _by, _bx + _bw, _by + 160, true);
        }

        // Overlay Text on Top of Vignette
        draw_set_color(c_black);
        draw_set_alpha(0.65);
        draw_rectangle(_bx, _by + 110, _bx + _bw, _by + 160, false);
        draw_set_alpha(1.0);
        draw_set_color(make_color_rgb(255, 220, 100));
        draw_text(_bx + 16, _by + 118, "CLASSIFIED SOLAR WAR DIRECTIVE // IRON RIDGE DYNAMICS FOUNDING CHARTER");
        draw_set_color(c_white);
        draw_text(_bx + 16, _by + 136, "LOCATION: Experimental Pre-War Dreadnought 'Hephaestus' // Lagrange Point 5");

        // Narrative Sections Grid (4 Monolithic War Factions & Core Directives)
        var _sec_y = _by + 175;
        var _col_w = (_bw - 24) / 2;

        // Left Column: The 4 Solar Factions Locked in Total War
        scr_draw_snes_panel(_bx, _sec_y, _col_w, 320, "== THE FOUR BELLIGERENT FACTIONS ==", 0, false, 0.05);
        
        draw_set_color(make_color_rgb(180, 220, 255));
        var _fy = _sec_y + 40;
        
        draw_set_color(make_color_rgb(100, 220, 255));
        draw_text(_bx + 16, _fy, "1. TERRAN COALITION (Earth & Lunar Foundries)");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text(_bx + 16, _fy + 18, "Doctrine: Heavy artillery, 120mm ordnance, dense composite armor plates (Ironclad series).");

        _fy += 58;
        draw_set_color(make_color_rgb(100, 255, 180));
        draw_text(_bx + 16, _fy, "2. OUTER COLONY LEAGUE (Jovian High Fleet)");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text(_bx + 16, _fy + 18, "Doctrine: Vernier thrusters, beam rifles, particle beam sabers (Aether interceptors).");

        _fy += 58;
        draw_set_color(make_color_rgb(255, 180, 80));
        draw_text(_bx + 16, _fy, "3. RIM-SYNDICATE CARTEL (Asteroid Belt Reavers)");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text(_bx + 16, _fy + 18, "Doctrine: Slag salvagers, heavy rotary flak, grappling claws, harpoon tethers (Hyena raiders).");

        _fy += 58;
        draw_set_color(make_color_rgb(220, 140, 255));
        draw_text(_bx + 16, _fy, "4. APEX ZAIBATSU (Corrupted Corporate Monopoly)");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text(_bx + 16, _fy + 18, "Doctrine: Cybernetic neural pilots, plasma blasters, tachyon optics, hostile takeovers.");

        // Right Column: Player PMC Operations & Strategic Directives
        scr_draw_snes_panel(_bx + _col_w + 24, _sec_y, _col_w, 320, "== YOUR STRATEGIC PMC CAPABILITIES ==", 1, false, 0.05);

        var _ry = _sec_y + 40;
        draw_set_color(make_color_rgb(255, 220, 100));
        draw_text(_bx + _col_w + 40, _ry, "* METALLURGICAL SINTERING (Thermal Crucible)");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text(_bx + _col_w + 40, _ry + 18, "Combine raw ores, flux, and tritium under extreme pressure to forge Vanguard Plating.");

        _ry += 58;
        draw_set_color(make_color_rgb(255, 220, 100));
        draw_text(_bx + _col_w + 40, _ry, "* MODULAR CAD MECHA ASSEMBLY (Factory Floor)");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text(_bx + _col_w + 40, _ry + 18, "Fit Heads, Torsos, Arms, Legs, and Weapons across Biped, Hover, Tread, & Aero frames.");

        _ry += 58;
        draw_set_color(make_color_rgb(255, 220, 100));
        draw_text(_bx + _col_w + 40, _ry, "* CORPORATE DEFENSE CONTRACTS & COMPETITIONS");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text(_bx + _col_w + 40, _ry + 18, "Enter 4-phase corporate design flyoffs to secure lucrative multi-million credit production lines.");

        _ry += 58;
        draw_set_color(make_color_rgb(255, 220, 100));
        draw_text(_bx + _col_w + 40, _ry, "* ISOMETRIC TACTICAL COMBAT (24 Map Theaters)");
        draw_set_color(make_color_rgb(170, 195, 220));
        draw_text(_bx + _col_w + 40, _ry + 18, "Deploy dual platoons with aimed shot precision; repel rival ace drop-pod incursions.");

        // Bottom Navigation Buttons
        var _nav_y = _my0 + _mh - 56;
        var _btn_w = 340;
        var _btn_x = _mx0 + _mw - _btn_w - 32;
        var _btn_hov = (_mx >= _btn_x && _mx <= _btn_x + _btn_w && _my >= _nav_y && _my <= _nav_y + 40);

        if (_btn_hov && _click) {
            intro_page = 1;
            scr_audio_play_ui("click");
        }

        scr_draw_snes_button(_btn_x, _nav_y, _btn_w, 40, ">> APPOINT COMMANDER PROFILE >>", _btn_hov, false, make_color_rgb(100, 220, 255));

        if (show_commander_modal && !intro_active) {
            var _cl_w = 200;
            var _cl_x = _mx0 + 32;
            var _cl_hov = (_mx >= _cl_x && _mx <= _cl_x + _cl_w && _my >= _nav_y && _my <= _nav_y + 40);
            if (_cl_hov && _click) {
                show_commander_modal = false;
                scr_audio_play_ui("cancel");
            }
            scr_draw_snes_button(_cl_x, _nav_y, _cl_w, 40, "[CLOSE DOSSIER]", _cl_hov, false, make_color_rgb(150, 170, 190));
        }
    }

    // -------------------------------------------------------------------------
    // PAGE 1: COMMANDER SELECTION DOSSIER (MALE / FEMALE / SILHOUETTE)
    // -------------------------------------------------------------------------
    else if (intro_page == 1) {
        var _cx = _mx0 + 32;
        var _cy = _my0 + 60;
        var _cw = _mw - 64;

        draw_set_color(make_color_rgb(170, 200, 230));
        draw_text(_cx, _cy, "SELECT COMMANDER GENDER PROFILE OR MAINTAIN ANONYMOUS BLACK-BUDGET SILHOUETTE:");

        // 3 Selectable Profile Cards Side-by-Side
        var _card_w = (_cw - 32) / 3;
        var _card_h = 360;
        var _card_y = _cy + 26;

        var _options = [
            {
                id: "silhouette",
                label: "ENCRYPTED SHADOW",
                gender_lbl: "ANONYMOUS / UNKNOWN",
                name: "Commander [CLASSIFIED]",
                callsign: "SHADOW",
                portrait: spr_portrait_commander_silhouette,
                trait: "Black Ops Logistics",
                trait_desc: "+10% Scrap Salvage, Volatility Dampening",
                bio: "Encrypted black-budget mercenary profile operating under an anonymous registry. Identity masked behind electronic warfare scramblers."
            },
            {
                id: "male",
                label: "MALE COMMANDER",
                gender_lbl: "MALE EXECUTIVE",
                name: "Commander Alexei Kane",
                callsign: "RAVEN",
                portrait: spr_portrait_commander_male,
                trait: "Heavy Vanguard",
                trait_desc: "+12% Kinetic Armor, +10% Contract Bounty",
                bio: "Former Terran Naval Strike Commander. Refused orbital saturation orders; founded an independent tactical design bureau."
            },
            {
                id: "female",
                label: "FEMALE COMMANDER",
                gender_lbl: "FEMALE EXECUTIVE",
                name: "Commander Morgan Vance",
                callsign: "VALKYRIE",
                portrait: spr_portrait_commander_female,
                trait: "Vernier Synthesis",
                trait_desc: "+15% Prototyping Stability, +10% Thruster Evasion",
                bio: "Former Colony Fleet Tactical Prodigy. Escaped Jovian corporate conscription to pioneer modular mobile suit metallurgy."
            }
        ];

        for (var ci = 0; ci < 3; ci++) {
            var _opt = _options[ci];
            var _card_x = _cx + ci * (_card_w + 16);
            var _is_sel = (selected_commander_choice == _opt.id);
            var _c_hov = (_mx >= _card_x && _mx <= _card_x + _card_w && _my >= _card_y && _my <= _card_y + _card_h);

            if (_c_hov && _click) {
                selected_commander_choice = _opt.id;
                scr_audio_play_ui("click");
            }

            // Card Panel
            scr_draw_snes_panel(_card_x, _card_y, _card_w, _card_h, _opt.label, _is_sel ? 0 : -1, _is_sel, 0.06);

            // Animated Portrait Canvas (Centered in Card)
            var _p_size = 140;
            var _px = _card_x + (_card_w - _p_size) / 2;
            var _py = _card_y + 36;

            if (sprite_exists(_opt.portrait)) {
                draw_sprite_ext(_opt.portrait, 0, _px, _py, _p_size / 200.0, _p_size / 200.0, 0, c_white, 1.0);
            }
            draw_set_color(_is_sel ? make_color_rgb(100, 220, 255) : make_color_rgb(50, 80, 110));
            draw_rectangle(_px, _py, _px + _p_size, _py + _p_size, true);

            // Name & Callsign
            draw_set_color(_is_sel ? make_color_rgb(255, 220, 100) : c_white);
            draw_text(_card_x + 16, _py + _p_size + 14, _opt.name);
            draw_set_color(make_color_rgb(120, 190, 255));
            draw_text(_card_x + 16, _py + _p_size + 32, "CALLSIGN: [" + _opt.callsign + "] | " + _opt.gender_lbl);

            // Trait
            draw_set_color(make_color_rgb(80, 240, 140));
            draw_text(_card_x + 16, _py + _p_size + 54, "TRAIT: " + _opt.trait);
            draw_set_color(make_color_rgb(160, 190, 215));
            draw_text(_card_x + 16, _py + _p_size + 70, _opt.trait_desc);

            // Selection Radio Button
            var _sel_btn_y = _card_y + _card_h - 40;
            var _sel_btn_w = _card_w - 32;
            var _sel_btn_x = _card_x + 16;
            var _s_hov = (_mx >= _sel_btn_x && _mx <= _sel_btn_x + _sel_btn_w && _my >= _sel_btn_y && _my <= _sel_btn_y + 30);
            if (_s_hov && _click) {
                selected_commander_choice = _opt.id;
                scr_audio_play_ui("click");
            }
            scr_draw_snes_button(_sel_btn_x, _sel_btn_y, _sel_btn_w, 30, _is_sel ? "[ ACTIVE SELECTION ]" : "SELECT PROFILE", _s_hov || _is_sel, _is_sel, _is_sel ? make_color_rgb(100, 255, 180) : c_white);
        }

        // Active Bio Description Readout Box (Bottom of Page 1)
        var _bio_y = _card_y + _card_h + 14;
        var _bio_h = 68;
        draw_set_color(make_color_rgb(14, 20, 30));
        draw_rectangle(_cx, _bio_y, _cx + _cw, _bio_y + _bio_h, false);
        draw_set_color(make_color_rgb(45, 80, 120));
        draw_rectangle(_cx, _bio_y, _cx + _cw, _bio_y + _bio_h, true);

        var _cur_choice_data = _options[0];
        if (selected_commander_choice == "male") _cur_choice_data = _options[1];
        else if (selected_commander_choice == "female") _cur_choice_data = _options[2];

        draw_set_color(make_color_rgb(100, 210, 255));
        draw_text(_cx + 16, _bio_y + 8, "EXECUTIVE DOSSIER LOG // " + _cur_choice_data.name + " [" + _cur_choice_data.callsign + "]:");
        draw_set_color(make_color_rgb(200, 220, 240));
        draw_text(_cx + 16, _bio_y + 28, _cur_choice_data.bio);

        // Confirmation / Back Navigation
        var _nav_y2 = _my0 + _mh - 56;
        
        // Back to Briefing
        var _back_w = 200;
        var _back_hov = (_mx >= _cx && _mx <= _cx + _back_w && _my >= _nav_y2 && _my <= _nav_y2 + 40);
        if (_back_hov && _click) {
            intro_page = 0;
            scr_audio_play_ui("click");
        }
        scr_draw_snes_button(_cx, _nav_y2, _back_w, 40, "< SITUATION BRIEFING", _back_hov, false, make_color_rgb(150, 180, 210));

        // Confirm & Launch Command Deck
        var _cf_w = 420;
        var _cf_x = _mx0 + _mw - _cf_w - 32;
        var _cf_hov = (_mx >= _cf_x && _mx <= _cf_x + _cf_w && _my >= _nav_y2 && _my <= _nav_y2 + 40);

        if (_cf_hov && _click) {
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
        scr_draw_snes_button(_cf_x, _nav_y2, _cf_w, 40, ">> CONFIRM DOSSIER & INITIALIZE PMC >>", _cf_hov, false, make_color_rgb(60, 240, 140));
    }
}
"""

if "INTERACTIVE SITUATION BRIEFING" not in d64:
    d64 += "\n" + modal_code
    with open("objects/obj_HQTerminal/Draw_64.gml", "w") as f:
        f.write(d64)
    print("✓ Added full-screen Situation Briefing & Commander Dossier Modal to obj_HQTerminal/Draw_64.gml")

print(">>> Commander Profile & Situation Briefing Integration Complete <<<")
