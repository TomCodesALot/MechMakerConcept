import re

print("Applying Milestone 53: Emotional Art Engine & Master Dialogue Bible...")

vn_path = "scripts/scr_vn_engine/scr_vn_engine.gml"
with open(vn_path, "r", encoding="utf-8") as f:
    vn = f.read()

# -----------------------------------------------------------------------------
# 1. Update scr_vn_draw with 4-Tier Emotion Rendering Overlays
# -----------------------------------------------------------------------------
old_portrait_section = '''    // Left Speaker Box
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
    draw_text_transformed(_p_x + 6, _p_y + _p_size + 9, _node.faction_badge, 0.70, 0.70, 0);'''

new_portrait_section = '''    // Left Speaker Box & Emotion Shader (Doc 53)
    var _emo = variable_struct_exists(_node, "emotion") ? _node.emotion : "NORMAL";
    var _emo_col = make_color_rgb(0, 240, 255);
    var _emo_tag = "[RESOLUTE]";
    if (_emo == "ANGRY" || _emo == "BELLIGERENT") {
        _emo_col = make_color_rgb(255, 60, 60);
        _emo_tag = "[ENRAGED]";
    } else if (_emo == "DESPERATE" || _emo == "ALARMED") {
        _emo_col = (current_time mod 300 < 150) ? make_color_rgb(255, 180, 40) : make_color_rgb(220, 80, 20);
        _emo_tag = "[CRITICAL]";
    } else if (_emo == "SMUG" || _emo == "CALCULATING") {
        _emo_col = make_color_rgb(255, 215, 80);
        _emo_tag = "[CALCULATING]";
    }

    draw_set_color(make_color_rgb(16, 24, 38));
    draw_rectangle(_p_x, _p_y, _p_x + _p_size, _p_y + _p_size, false);

    var _left_alpha = (_is_dual && _side != "LEFT") ? 0.40 : 1.0;
    var _left_border = (_is_dual && _side != "LEFT") ? make_color_rgb(45, 65, 85) : _emo_col;

    if (variable_struct_exists(_node, "portrait") && sprite_exists(_node.portrait)) {
        draw_sprite_ext(_node.portrait, 0, _p_x, _p_y, _p_size / 200.0, _p_size / 200.0, 0, c_white, _left_alpha);
    }
    draw_set_color(_left_border);
    draw_rectangle(_p_x, _p_y, _p_x + _p_size, _p_y + _p_size, true);

    // Left Faction & Emotion Ribbons
    draw_set_color(make_color_rgb(24, 48, 80));
    draw_rectangle(_p_x, _p_y + _p_size + 6, _p_x + _p_size, _p_y + _p_size + 24, false);
    draw_set_color((_is_dual && _side != "LEFT") ? make_color_rgb(100, 140, 180) : make_color_rgb(120, 220, 255));
    draw_text_transformed(_p_x + 6, _p_y + _p_size + 9, _node.faction_badge, 0.70, 0.70, 0);

    // Emotion State Tag
    if (!_is_dual || _side == "LEFT") {
        draw_set_color(_emo_col);
        draw_text_transformed(_p_x + 6, _p_y + 6, _emo_tag, 0.65, 0.65, 0);
    }'''

if old_portrait_section in vn:
    vn = vn.replace(old_portrait_section, new_portrait_section, 1)
    print("[PASS] scr_vn_draw upgraded with 4-Tier Emotion Rendering Overlays")
else:
    print("[WARN] old_portrait_section not found in scr_vn_engine.gml")

# -----------------------------------------------------------------------------
# 2. Add emotion tags into scr_vn_start_dynamic_audience
# -----------------------------------------------------------------------------
target_dyn_nodes = '''    // Node 2: Consequential Strategic Choice
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
            text: "Here is our active diplomatic proposal. What is your response, Commander?",'''

repl_dyn_nodes = '''    // Determine dynamic emotion state (Doc 53)
    var _dynamic_emo = "NORMAL";
    if (_standing <= -25) _dynamic_emo = "ANGRY";
    else if (_ai_state == "DESPERATE") _dynamic_emo = "DESPERATE";
    else if (_ai_state == "WINNING" || _standing >= 40) _dynamic_emo = "SMUG";

    // Node 2: Consequential Strategic Choice
    var _nodes = [
        {
            speaker: _speaker,
            title: _title,
            faction: _f_name,
            faction_badge: _badge,
            portrait: _portrait,
            emotion: _dynamic_emo,
            text: _mood_text
        },
        {
            speaker: _speaker,
            title: _title,
            faction: _f_name,
            faction_badge: _badge,
            portrait: _portrait,
            emotion: (_dynamic_emo == "ANGRY" ? "ANGRY" : "NORMAL"),
            text: _incident_text
        },
        {
            speaker: _speaker,
            title: _title,
            faction: _f_name,
            faction_badge: _badge,
            portrait: _portrait,
            emotion: (_dynamic_emo == "DESPERATE" ? "DESPERATE" : "NORMAL"),
            text: "Here is our active diplomatic proposal. What is your response, Commander?",'''

if target_dyn_nodes in vn:
    vn = vn.replace(target_dyn_nodes, repl_dyn_nodes, 1)
    print("[PASS] scr_vn_start_dynamic_audience updated with dynamic emotion assignment")
else:
    print("[WARN] target_dyn_nodes not found in scr_vn_engine.gml")

with open(vn_path, "w", encoding="utf-8") as f:
    f.write(vn)

# -----------------------------------------------------------------------------
# 3. Add Combat Radio Duel Barks into objects/obj_BattleManager/Create_0.gml
# -----------------------------------------------------------------------------
bm_create_path = "objects/obj_BattleManager/Create_0.gml"
with open(bm_create_path, "r", encoding="utf-8") as f:
    bm_code = f.read()

target_impact_log = '''    if (_hit) {
        add_log("[DIRECT HIT] " + _atk.callsign + " hit " + _def.callsign + " with " + _wpn.name + " (" + string(_hit_chance) + "% hit roll)!");'''

repl_impact_log = '''    if (_hit) {
        add_log("[DIRECT HIT] " + _atk.callsign + " hit " + _def.callsign + " with " + _wpn.name + " (" + string(_hit_chance) + "% hit roll)!");
        
        // Front Mission Tactical Radio Duel Bark (Doc 52 & 53)
        if (irandom_range(1, 100) <= 35) {
            var _atk_barks = [
                "Direct hit on their kinetic armor! Firing follow-up volley!",
                "Target lock held! Saturated missile trajectory away!",
                "Hydraulic servos at maximum output! Engaging target!",
                "Breaching their defense envelope! Keep pressure on their reactor!"
            ];
            var _bark_txt = _atk_barks[irandom(array_length(_atk_barks) - 1)];
            var _bark_speaker = _atk.pilot_name + " [" + _atk.callsign + "]";
            scr_vn_trigger_combat_intercom(_bark_speaker, _atk.sprite_asset, _bark_txt, 140, make_color_rgb(80, 240, 120));
        }'''

if target_impact_log in bm_code and "Front Mission Tactical Radio Duel Bark" not in bm_code:
    bm_code = bm_code.replace(target_impact_log, repl_impact_log, 1)
    with open(bm_create_path, "w", encoding="utf-8") as f:
        f.write(bm_code)
    print("[PASS] obj_BattleManager/Create_0.gml updated with combat radio duel barks")
else:
    print("[WARN/SKIP] target_impact_log not found or already applied in BattleManager")

print("Milestone 53 engine upgrades successfully applied!")
