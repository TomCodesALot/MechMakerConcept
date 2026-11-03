import re

print("Starting Milestone 52 Full Engine Implementation...")

# =============================================================================
# 1. Update scripts/scr_vn_engine/scr_vn_engine.gml
# =============================================================================
vn_path = "scripts/scr_vn_engine/scr_vn_engine.gml"
with open(vn_path, "r", encoding="utf-8") as f:
    vn = f.read()

# 1a. Add helper functions at the end of scr_vn_engine.gml
helpers_code = '''

// =============================================================================
// REACTIVE GEOPOLITICAL VN NOVEL SYSTEM (DOC 52)
// =============================================================================

/// @function scr_vn_interpolate_text(_raw_text)
/// @description Parses and replaces dynamic world state tokens ({PLAYER_CALLSIGN}, {RECENT_SECTOR}, {ROSTER_PILOT}, etc.)
function scr_vn_interpolate_text(_raw_text) {
    if (!is_string(_raw_text)) return "";
    var _txt = _raw_text;

    // Player Commander Callouts
    var _cmdr_callsign = "VANGUARD";
    var _cmdr_name = "Commander";
    if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "player_commander") && is_struct(obj_GameManager.player_commander)) {
        if (variable_struct_exists(obj_GameManager.player_commander, "callsign")) _cmdr_callsign = obj_GameManager.player_commander.callsign;
        if (variable_struct_exists(obj_GameManager.player_commander, "name")) _cmdr_name = obj_GameManager.player_commander.name;
    }
    _txt = string_replace_all(_txt, "{PLAYER_CALLSIGN}", _cmdr_callsign);
    _txt = string_replace_all(_txt, "{PLAYER_NAME}", _cmdr_name);

    // Recent Contested Sector Callout
    var _recent_sector = "Olympus Mons";
    if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "last_battle_report") && !is_undefined(obj_GameManager.last_battle_report)) {
        if (variable_struct_exists(obj_GameManager.last_battle_report, "sector_name")) {
            _recent_sector = obj_GameManager.last_battle_report.sector_name;
        }
    }
    _txt = string_replace_all(_txt, "{RECENT_SECTOR}", _recent_sector);

    // Lead Roster Pilot Callout
    var _roster_pilot = "Lt. Sonya Cruz";
    if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "facilities") && is_struct(obj_GameManager.facilities)) {
        if (variable_struct_exists(obj_GameManager.facilities, "roster_pilots") && is_array(obj_GameManager.facilities.roster_pilots)) {
            var _rp = obj_GameManager.facilities.roster_pilots;
            if (array_length(_rp) > 0) {
                _roster_pilot = _rp[0].name + " ('" + _rp[0].callsign + "')";
            }
        }
    }
    _txt = string_replace_all(_txt, "{ROSTER_PILOT}", _roster_pilot);

    // Brig Incarcerated Prisoner Callout
    var _brig_prisoner = "Captured Hyena Ace";
    if (instance_exists(obj_NemesisManager) && variable_instance_exists(obj_NemesisManager, "prisoner_list") && is_array(obj_NemesisManager.prisoner_list)) {
        var _pl = obj_NemesisManager.prisoner_list;
        if (array_length(_pl) > 0) {
            _brig_prisoner = _pl[0].name;
        }
    }
    _txt = string_replace_all(_txt, "{BRIG_PRISONER}", _brig_prisoner);

    // Flagship Callout
    _txt = string_replace_all(_txt, "{FLAGSHIP}", "USN-X Hephaestus");

    return _txt;
}

/// @function scr_vn_start_dynamic_audience(_faction_id)
/// @description Assembles and starts a reactive 3-node VN audience with the leader based on standing, AI mood, and deeds.
function scr_vn_start_dynamic_audience(_faction_id) {
    if (!variable_global_exists("vn_state") || !is_struct(global.vn_state)) {
        scr_vn_init();
    }

    var _fm = instance_exists(obj_FactionManager) ? obj_FactionManager : undefined;
    var _standing = 0;
    var _ai_state = "PEACE";
    var _f_name = "Faction Command";
    var _speaker = "Diplomatic Attaché";
    var _title = "Liaison Officer";
    var _portrait = spr_portrait_commander_male;
    var _badge = "[DIPLOMACY]";
    var _primary_enemy = "faction_b";

    if (!is_undefined(_fm) && variable_struct_exists(_fm.factions, _faction_id)) {
        var _finfo = _fm.factions[$ _faction_id];
        _standing = _fm.get_standing(_faction_id);
        _ai_state = variable_struct_get(_finfo, "ai_state") ?? "PEACE";
        _f_name = _finfo.name;
        _primary_enemy = variable_struct_get(_finfo, "primary_enemy_id") ?? "faction_b";
    }

    if (_faction_id == "faction_a") {
        _speaker = "General Arthur Bradley";
        _title = "Supreme Commander // Earth Defense Front";
        _portrait = spr_portrait_commander_male;
        _badge = "[TERRAN COALITION]";
    } else if (_faction_id == "faction_b") {
        _speaker = "Commander Joshua Reed";
        _title = "Supreme Marshal // Outer Colony League";
        _portrait = spr_portrait_commander_female;
        _badge = "[COLONY LEAGUE]";
    } else if (_faction_id == "faction_c") {
        _speaker = "Captain Sonya Cruz";
        _title = "High Commodore // Corsair Syndicate";
        _portrait = spr_portrait_cruz;
        _badge = "[ROGUE SYNDICATE]";
    } else if (_faction_id == "faction_d") {
        _speaker = "Director Kenjiro Sato";
        _title = "Chief Executive Officer // Sato Heavy Industries";
        _portrait = spr_portrait_commander_silhouette;
        _badge = "[APEX ZAIBATSU]";
    } else if (_faction_id == "faction_e") {
        _speaker = "Archon Orin Sideris";
        _title = "First Sovereign // Republic Cylinder Astraea-01";
        _portrait = (sprite_exists(spr_portrait_sorren) ? spr_portrait_sorren : spr_portrait_commander_silhouette);
        _badge = "[SIDEREAL LEAGUE]";
    } else if (_faction_id == "faction_f") {
        _speaker = "Consensus Node 0-Prime";
        _title = "Deus Logica // Subterranean Red Crypt of Mars";
        _portrait = (sprite_exists(spr_portrait_null07) ? spr_portrait_null07 : spr_portrait_commander_silhouette);
        _badge = "[THARSIS CONSENSUS]";
    }

    // Node 0: Dynamic Mood Salutation
    var _mood_text = "";
    if (_standing <= -25) {
        _mood_text = "You dare establish an encrypted quantum uplink after declaring war on our sovereignty, {PLAYER_CALLSIGN}? Your mercenary syndicate is classified as a hostile belligerent. Speak your terms quickly before our orbital fire batteries lock your transmission source.";
    } else if (_ai_state == "DESPERATE") {
        _mood_text = "Commander {PLAYER_CALLSIGN}! Thank the stars you answered this frequency. Our frontline perimeter in {RECENT_SECTOR} is collapsing under saturation bombardment! If your Mobile Suits do not deploy immediately, our forces will be overrun. We will pay double standard contract rates!";
    } else if (_ai_state == "WINNING" || _standing >= 40) {
        _mood_text = "Greetings, Commander. The strategic war map is bending decisively toward our doctrine. The " + _f_name + " values our alliance with Iron Ridge. We are prepared to grant priority access to our military supply foundries.";
    } else if (_ai_state == "STANDARD_WAR") {
        _mood_text = "Uplink confirmed. Our battlegroups are actively engaged across all three operational theaters. We have no leisure for diplomatic pleasantries, Commander—we require immediate armored firepower on the frontlines.";
    } else {
        _mood_text = "Quantum link established with the " + _f_name + ". The commercial ledger between our commands remains open, Commander. State your operational availability and terms.";
    }

    // Node 1: Contextual Incident Bark
    var _incident_text = "";
    if (_standing < -10) {
        _incident_text = "Our strategic reconnaissance confirms that {ROSTER_PILOT} spearheaded the assault against our supply grid. Every kinetic slug fired by Iron Ridge is logged in our retaliation matrices. If you seek to de-escalate tensions, it will require immense commercial restitution.";
    } else if (_standing >= 20) {
        _incident_text = "Battlefield telemetry from {RECENT_SECTOR} confirms your squad's absolute tactical dominance. The " + _f_name + " recognizes discipline and lethal precision. We want your Mobile Suits under exclusive retainer.";
    } else {
        _incident_text = "Our logistical offices note that your flagship {FLAGSHIP} has unsealed pre-war manufacturing crucibles. We are prepared to trade high-density metallurgy for your combat escort sorties.";
    }

    // Node 2: Consequential Strategic Choice
    var _nodes = [
        {
            speaker: _speaker,
            title: _title,
            faction: _f_name,
            faction_badge: _badge,
            portrait: _portrait,
            text: _mood_text
        },
        {
            speaker: _speaker,
            title: _title,
            faction: _f_name,
            faction_badge: _badge,
            portrait: _portrait,
            text: _incident_text
        },
        {
            speaker: _speaker,
            title: _title,
            faction: _f_name,
            faction_badge: _badge,
            portrait: _portrait,
            text: "Here is our active diplomatic proposal. What is your response, Commander?",
            choices: [
                {
                    text: "Accept Frontline Contract: Deploy Mobile Suits in direct support.",
                    pillar: "ALLIANCE // STRATEGIC PACT",
                    impact_label: "+15 Standing | -10 Rival | +50,000 Cr Operational Retainer",
                    action: method({ fid: _faction_id, pen: _primary_enemy }, function() {
                        if (instance_exists(obj_FactionManager)) {
                            obj_FactionManager.modify_standing(fid, 15);
                            obj_FactionManager.modify_standing(pen, -10);
                        }
                        if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(50000);
                    })
                },
                {
                    text: "Metallurgical Exchange: Trade tactical telemetry for rare elements.",
                    pillar: "COMMERCE // RAW LOGISTICS",
                    impact_label: "+10 Standing | +20x Titanium | +15x Tungsten Ores",
                    action: method({ fid: _faction_id }, function() {
                        if (instance_exists(obj_FactionManager)) obj_FactionManager.modify_standing(fid, 10);
                        if (instance_exists(obj_GameManager)) {
                            obj_GameManager.add_raw_material("mat_titanium", 20);
                            obj_GameManager.add_raw_material("mat_tungsten", 15);
                        }
                    })
                },
                {
                    text: "Defiant Rejection: Extort ransom or sever diplomatic ties.",
                    pillar: "EXTORTION // MERCENARY DEFIANCE",
                    impact_label: "-15 Standing | +10 Rival Standing | +65,000 Cr Black Market",
                    action: method({ fid: _faction_id, pen: _primary_enemy }, function() {
                        if (instance_exists(obj_FactionManager)) {
                            obj_FactionManager.modify_standing(fid, -15);
                            obj_FactionManager.modify_standing(pen, 10);
                        }
                        if (instance_exists(obj_GameManager)) obj_GameManager.add_funds(65000);
                    })
                }
            ]
        }
    ];

    global.vn_state.episodes[$ "ep_dynamic_audience"] = {
        title: "DIPLOMATIC AUDIENCE // " + string_upper(_f_name),
        bg_scene: spr_loc_war_room,
        nodes: _nodes
    };

    return scr_vn_start_episode("ep_dynamic_audience");
}

/// @function scr_vn_trigger_combat_intercom(_speaker, _portrait, _text, _duration, _color)
/// @description Displays an in-combat Front Mission tactical radio squelch comms banner in rm_combat.
function scr_vn_trigger_combat_intercom(_speaker, _portrait, _text, _duration = 180, _color = c_lime) {
    if (!variable_global_exists("combat_intercom") || !is_struct(global.combat_intercom)) {
        global.combat_intercom = {
            active: false,
            speaker: "",
            portrait: -1,
            text: "",
            timer: 0,
            max_timer: 180,
            color: c_white
        };
    }
    global.combat_intercom.active = true;
    global.combat_intercom.speaker = _speaker;
    global.combat_intercom.portrait = _portrait;
    global.combat_intercom.text = _text;
    global.combat_intercom.timer = _duration;
    global.combat_intercom.max_timer = _duration;
    global.combat_intercom.color = _color;
    scr_audio_play_ui("boot");
}

/// @function scr_vn_draw_combat_intercom()
/// @description Draws the tactical military radio intercom banner on screen during combat.
function scr_vn_draw_combat_intercom() {
    if (!variable_global_exists("combat_intercom") || !is_struct(global.combat_intercom) || !global.combat_intercom.active) return;
    
    var _ci = global.combat_intercom;
    _ci.timer--;
    if (_ci.timer <= 0) {
        _ci.active = false;
        return;
    }
    
    var _gw = display_get_gui_width();
    var _w = min(680, _gw - 80);
    var _h = 76;
    var _x = (_gw - _w) / 2;
    var _y = 54;
    
    var _alpha = (_ci.timer < 20) ? (_ci.timer / 20.0) : min(1.0, (_ci.max_timer - _ci.timer) / 10.0);
    draw_set_alpha(_alpha * 0.92);
    
    // Panel Background
    draw_set_color(make_color_rgb(10, 16, 24));
    draw_rectangle(_x, _y, _x + _w, _y + _h, false);
    
    // Border with blinking LED pulse
    var _blink = (current_time mod 300 < 150);
    draw_set_color(_ci.color);
    draw_rectangle(_x, _y, _x + _w, _y + _h, true);
    draw_set_color(make_color_rgb(25, 45, 65));
    draw_rectangle(_x + 2, _y + 2, _x + _w - 2, _y + _h - 2, true);
    
    // Portrait
    var _p_size = 56;
    var _px = _x + 10;
    var _py = _y + 10;
    draw_set_color(c_black);
    draw_rectangle(_px, _py, _px + _p_size, _py + _p_size, false);
    if (sprite_exists(_ci.portrait)) {
        draw_sprite_ext(_ci.portrait, 0, _px, _py, _p_size / 200.0, _p_size / 200.0, 0, c_white, _alpha);
    }
    draw_set_color(_ci.color);
    draw_rectangle(_px, _py, _px + _p_size, _py + _p_size, true);
    
    // Top Radio Frequency Banner
    draw_set_color(_blink ? make_color_rgb(80, 255, 120) : make_color_rgb(40, 180, 80));
    draw_text_transformed(_px + _p_size + 14, _y + 8, "[LIVE COMMS // CH-08 ENCRYPTED]", 0.68, 0.68, 0);
    
    // Speaker Name
    draw_set_color(make_color_rgb(255, 220, 90));
    draw_text_transformed(_px + _p_size + 14, _y + 22, _ci.speaker, 0.85, 0.85, 0);
    
    // Text
    draw_set_color(c_white);
    draw_text_ext_transformed(_px + _p_size + 14, _y + 38, _ci.text, 18, floor((_w - _p_size - 30) / 0.78), 0.78, 0.78, 0);
    
    draw_set_alpha(1.0);
}
'''

# 1b. Update scr_vn_draw to support Dual Portrait Layout and Token Interpolation
old_draw_portrait_block = '''    // 3. Speaker Portrait Box (Left of Dialogue Box)
    var _p_size = 148;
    var _p_x = _box_x + 18;
    var _p_y = _box_y + 20;

    draw_set_color(make_color_rgb(16, 24, 38));
    draw_rectangle(_p_x, _p_y, _p_x + _p_size, _p_y + _p_size, false);

    if (variable_struct_exists(_node, "portrait") && sprite_exists(_node.portrait)) {
        draw_sprite_ext(_node.portrait, 0, _p_x, _p_y, _p_size / 200.0, _p_size / 200.0, 0, c_white, 1.0);
    }
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_rectangle(_p_x, _p_y, _p_x + _p_size, _p_y + _p_size, true);

    // Faction Badge Ribbon under Portrait
    draw_set_color(make_color_rgb(24, 48, 80));
    draw_rectangle(_p_x, _p_y + _p_size + 6, _p_x + _p_size, _p_y + _p_size + 24, false);
    draw_set_color(make_color_rgb(120, 220, 255));
    draw_text_transformed(_p_x + 6, _p_y + _p_size + 9, _node.faction_badge, 0.72, 0.72, 0);

    // 4. Speaker Nameplate & Title Banner
    var _txt_x = _p_x + _p_size + 24;
    var _txt_w = _box_w - (_p_size + 60);

    draw_set_color(make_color_rgb(255, 220, 90));
    draw_text_transformed(_txt_x, _box_y + 16, _node.speaker, 1.1, 1.1, 0);

    draw_set_color(make_color_rgb(140, 185, 225));
    draw_text_transformed(_txt_x, _box_y + 38, _node.title + " // " + _node.faction, 0.75, 0.75, 0);

    draw_set_color(make_color_rgb(40, 75, 115));
    draw_line(_txt_x, _box_y + 54, _txt_x + _txt_w, _box_y + 54);

    // 5. Typewriter Dialogue Display
    var _full_text = _node.text;'''

new_draw_portrait_block = '''    // 3. Speaker Portrait Layout (Doc 52 Dual & Single Layout Support)
    var _is_dual = (variable_struct_exists(_node, "portrait_right") && sprite_exists(_node.portrait_right));
    var _side = (variable_struct_exists(_node, "active_side") ? _node.active_side : "LEFT");
    var _p_size = _is_dual ? 136 : 148;
    var _p_x = _box_x + 18;
    var _p_y = _box_y + 20;

    // Left Speaker Box
    draw_set_color(make_color_rgb(16, 24, 38));
    draw_rectangle(_p_x, _p_y, _p_x + _p_size, _p_y + _p_size, false);

    var _left_alpha = (_is_dual && _side != "LEFT") ? 0.40 : 1.0;
    var _left_border = (_is_dual && _side != "LEFT") ? make_color_rgb(45, 65, 85) : make_color_rgb(0, 240, 255);

    if (variable_struct_exists(_node, "portrait") && sprite_exists(_node.portrait)) {
        draw_sprite_ext(_node.portrait, 0, _p_x, _p_y, _p_size / 200.0, _p_size / 200.0, 0, c_white, _left_alpha);
    }
    draw_set_color(_left_border);
    draw_rectangle(_p_x, _p_y, _p_x + _p_size, _p_y + _p_size, true);

    // Left Faction Ribbon
    draw_set_color(make_color_rgb(24, 48, 80));
    draw_rectangle(_p_x, _p_y + _p_size + 6, _p_x + _p_size, _p_y + _p_size + 24, false);
    draw_set_color((_is_dual && _side != "LEFT") ? make_color_rgb(100, 140, 180) : make_color_rgb(120, 220, 255));
    draw_text_transformed(_p_x + 6, _p_y + _p_size + 9, _node.faction_badge, 0.70, 0.70, 0);

    // 3b. Optional Right Speaker Box (Dual Layout)
    if (_is_dual) {
        var _pr_x = _box_x + _box_w - _p_size - 18;
        var _pr_y = _box_y + 20;
        var _right_alpha = (_side == "RIGHT") ? 1.0 : 0.40;
        var _right_border = (_side == "RIGHT") ? make_color_rgb(255, 215, 80) : make_color_rgb(45, 65, 85);

        draw_set_color(make_color_rgb(16, 24, 38));
        draw_rectangle(_pr_x, _pr_y, _pr_x + _p_size, _pr_y + _p_size, false);

        draw_sprite_ext(_node.portrait_right, 0, _pr_x, _pr_y, _p_size / 200.0, _p_size / 200.0, 0, c_white, _right_alpha);
        draw_set_color(_right_border);
        draw_rectangle(_pr_x, _pr_y, _pr_x + _p_size, _pr_y + _p_size, true);

        // Right Faction Ribbon
        draw_set_color(make_color_rgb(24, 48, 80));
        draw_rectangle(_pr_x, _pr_y + _p_size + 6, _pr_x + _p_size, _pr_y + _p_size + 24, false);
        var _r_badge = variable_struct_exists(_node, "faction_badge_right") ? _node.faction_badge_right : "[RIVAL]";
        draw_set_color((_side == "RIGHT") ? make_color_rgb(255, 220, 120) : make_color_rgb(100, 140, 180));
        draw_text_transformed(_pr_x + 6, _pr_y + _p_size + 9, _r_badge, 0.70, 0.70, 0);
    }

    // 4. Speaker Nameplate & Title Banner
    var _txt_x = _p_x + _p_size + 22;
    var _txt_w = _is_dual ? (_box_w - (2 * _p_size + 76)) : (_box_w - (_p_size + 60));

    draw_set_color((_is_dual && _side == "RIGHT") ? make_color_rgb(255, 215, 80) : make_color_rgb(255, 220, 90));
    draw_text_transformed(_txt_x, _box_y + 16, _node.speaker, 1.05, 1.05, 0);

    draw_set_color(make_color_rgb(140, 185, 225));
    draw_text_transformed(_txt_x, _box_y + 38, _node.title + " // " + _node.faction, 0.75, 0.75, 0);

    draw_set_color(make_color_rgb(40, 75, 115));
    draw_line(_txt_x, _box_y + 54, _txt_x + _txt_w, _box_y + 54);

    // 5. Typewriter Dialogue Display with Interpolation (Doc 52)
    var _full_text = scr_vn_interpolate_text(_node.text);'''

if old_draw_portrait_block in vn:
    vn = vn.replace(old_draw_portrait_block, new_draw_portrait_block, 1)
    print("[PASS] scr_vn_draw upgraded with Dual-Speaker Layout and Token Interpolation")
else:
    print("[WARN] old_draw_portrait_block not found in scr_vn_engine.gml")

# Append helpers to file
vn = vn + helpers_code

with open(vn_path, "w", encoding="utf-8") as f:
    f.write(vn)

print("[PASS] scr_vn_engine.gml updated with all Milestone 52 architectures!")

# =============================================================================
# 2. Update objects/obj_HQTerminal/Draw_64.gml to use scr_vn_start_dynamic_audience
# =============================================================================
hq_path = "objects/obj_HQTerminal/Draw_64.gml"
with open(hq_path, "r", encoding="utf-8") as f:
    hq = f.read()

target_hq_aud = '''                // Diplomatic Audience VN Trigger (Doc 51)
                var _f_box_hov = (_mx >= _fx && _mx <= _fx + _f_box_w && _my >= _std_y && _my <= _std_y + 54);
                if (_f_box_hov && _click) {
                    if (_fid == "faction_a") scr_vn_start_episode("ep_audience_terran");
                    else if (_fid == "faction_b") scr_vn_start_episode("ep_audience_colony");
                    else if (_fid == "faction_c") scr_vn_start_episode("ep_audience_syndicate");
                    else if (_fid == "faction_d") scr_vn_start_episode("ep_audience_zaibatsu");
                    else if (_fid == "faction_e") scr_vn_start_episode("ep_audience_sidereal");
                    else if (_fid == "faction_f") scr_vn_start_episode("ep_audience_tharsis");
                    scr_audio_play_ui("confirm");
                }'''

repl_hq_aud = '''                // Diplomatic Audience VN Trigger: Reactive Dynamic Audience (Doc 52)
                var _f_box_hov = (_mx >= _fx && _mx <= _fx + _f_box_w && _my >= _std_y && _my <= _std_y + 54);
                if (_f_box_hov && _click) {
                    scr_vn_start_dynamic_audience(_fid);
                    scr_audio_play_ui("confirm");
                }'''

if target_hq_aud in hq:
    hq = hq.replace(target_hq_aud, repl_hq_aud, 1)
    with open(hq_path, "w", encoding="utf-8") as f:
        f.write(hq)
    print("[PASS] obj_HQTerminal/Draw_64.gml updated to use scr_vn_start_dynamic_audience")
else:
    print("[WARN] target_hq_aud not found in obj_HQTerminal/Draw_64.gml")

# =============================================================================
# 3. Update objects/obj_GameManager/Create_0.gml for Summit Triggers
# =============================================================================
gm_path = "objects/obj_GameManager/Create_0.gml"
with open(gm_path, "r", encoding="utf-8") as f:
    gm = f.read()

target_gm_turns = '''    // Check Campaign Story Milestone Episodes (Doc 51)
    if (current_turn == 5 && !variable_struct_exists(story_episodes_seen, "ep_02_shadows_over_mars")) {
        variable_struct_set(story_episodes_seen, "ep_02_shadows_over_mars", true);
        scr_vn_start_episode("ep_02_shadows_over_mars");
    }'''

repl_gm_turns = '''    // Check Campaign Story Milestone Episodes & Multi-Leader Summits (Doc 51 & Doc 52)
    if (current_turn == 5 && !variable_struct_exists(story_episodes_seen, "ep_02_shadows_over_mars")) {
        variable_struct_set(story_episodes_seen, "ep_02_shadows_over_mars", true);
        scr_vn_start_episode("ep_02_shadows_over_mars");
    } else if (current_turn == 7 && !variable_struct_exists(story_episodes_seen, "ep_summit_phobos_crisis")) {
        variable_struct_set(story_episodes_seen, "ep_summit_phobos_crisis", true);
        scr_vn_start_episode("ep_summit_phobos_crisis");
    } else if (current_turn == 12 && !variable_struct_exists(story_episodes_seen, "ep_summit_transhumanist_schism")) {
        variable_struct_set(story_episodes_seen, "ep_summit_transhumanist_schism", true);
        scr_vn_start_episode("ep_summit_transhumanist_schism");
    } else if (current_turn == 18 && !variable_struct_exists(story_episodes_seen, "ep_summit_sol_monopoly")) {
        variable_struct_set(story_episodes_seen, "ep_summit_sol_monopoly", true);
        scr_vn_start_episode("ep_summit_sol_monopoly");
    }'''

if target_gm_turns in gm:
    gm = gm.replace(target_gm_turns, repl_gm_turns, 1)
    with open(gm_path, "w", encoding="utf-8") as f:
        f.write(gm)
    print("[PASS] obj_GameManager/Create_0.gml updated with Summit Crisis turn hooks")
else:
    print("[WARN] target_gm_turns not found in obj_GameManager/Create_0.gml")

# =============================================================================
# 4. Update objects/obj_BattleManager/Draw_64.gml and Create_0.gml
# =============================================================================
bm_draw_path = "objects/obj_BattleManager/Draw_64.gml"
with open(bm_draw_path, "r", encoding="utf-8") as f:
    bm_draw = f.read()

# Add combat intercom draw at the very end of Draw_64
intercom_draw_hook = '''

// 10. Tactical Radio Comms Intercom Overlay (Doc 52)
scr_vn_draw_combat_intercom();
'''

if "scr_vn_draw_combat_intercom()" not in bm_draw:
    bm_draw = bm_draw + intercom_draw_hook
    with open(bm_draw_path, "w", encoding="utf-8") as f:
        f.write(bm_draw)
    print("[PASS] obj_BattleManager/Draw_64.gml updated with scr_vn_draw_combat_intercom()")

bm_create_path = "objects/obj_BattleManager/Create_0.gml"
with open(bm_create_path, "r", encoding="utf-8") as f:
    bm_create = f.read()

# Add opening radio challenge bark in BattleManager Create
target_bm_end = '''    // Disable random Nemesis incursion during prologue
    nemesis_incursion_checked = true;
}'''

repl_bm_end = '''    // Disable random Nemesis incursion during prologue
    nemesis_incursion_checked = true;
}

// Tactical Radio Comms Opening Intercom Bark (Doc 52)
if ((is_undefined(_combat_ctx) || !variable_struct_exists(_combat_ctx, "is_prologue") || !_combat_ctx.is_prologue) && array_length(units) > 0) {
    var _first_enemy = undefined;
    for (var u = 0; u < array_length(units); u++) {
        if (units[u].team == "HOSTILE") {
            _first_enemy = units[u];
            break;
        }
    }
    if (!is_undefined(_first_enemy)) {
        scr_vn_trigger_combat_intercom(_first_enemy.pilot_name + " [" + _first_enemy.callsign + "]", _first_enemy.sprite_asset, "Hostile vanguard detected on tactical radar. All units, weapons free! Tear their armor apart!", 180, make_color_rgb(255, 90, 90));
    }
}'''

if target_bm_end in bm_create and "Tactical Radio Comms Opening Intercom Bark" not in bm_create:
    bm_create = bm_create.replace(target_bm_end, repl_bm_end, 1)
    with open(bm_create_path, "w", encoding="utf-8") as f:
        f.write(bm_create)
    print("[PASS] obj_BattleManager/Create_0.gml updated with opening radio challenge bark")

print("All Milestone 52 components successfully applied!")
