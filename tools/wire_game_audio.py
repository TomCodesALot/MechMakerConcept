#!/usr/bin/env python3
"""
tools/wire_game_audio.py
Hooks sound effects and dynamic background music into obj_HQTerminal and obj_BattleManager.
"""

import os
import re

# =============================================================================
# 1. WIRE obj_HQTerminal/Create_0.gml
# =============================================================================
print("=== 1. WIRING obj_HQTerminal/Create_0.gml ===")
with open("objects/obj_HQTerminal/Create_0.gml", "r") as f:
    text = f.read()

# Add audio initialization right after managers bootstrap
init_target = 'if (!instance_exists(obj_BlueprintManager)) instance_create_depth(0, 0, 0, obj_BlueprintManager);'
audio_init_code = """if (!instance_exists(obj_BlueprintManager)) instance_create_depth(0, 0, 0, obj_BlueprintManager);
if (!instance_exists(obj_AudioManager)) instance_create_depth(0, 0, 0, obj_AudioManager);

// Start Terminal Background Audio Atmosphere
scr_audio_play_ui("boot");
scr_audio_play_location_bgm((active_tab == 0) ? "prototyping" : "hq");"""

if "scr_audio_play_location_bgm" not in text:
    text = text.replace(init_target, audio_init_code)

# Wire crucible_heat
text = text.replace(
    'crucible_temp_c = clamp(crucible_temp_c + _delta, 25.0, 5000.0);',
    'crucible_temp_c = clamp(crucible_temp_c + _delta, 25.0, 5000.0);\n    scr_audio_play_sfx(snd_plasma_weld, 0.6, 0.08);'
)

# Wire crucible_cool
text = text.replace(
    'crucible_temp_c = clamp(crucible_temp_c - _delta, 25.0, 5000.0);',
    'crucible_temp_c = clamp(crucible_temp_c - _delta, 25.0, 5000.0);\n    scr_audio_play_sfx(snd_mech_boost, 0.5, 0.08);'
)

# Wire crucible_compress
text = text.replace(
    'crucible_pressure_psi = clamp(crucible_pressure_psi + _delta, 14.7, 10000.0);',
    'crucible_pressure_psi = clamp(crucible_pressure_psi + _delta, 14.7, 10000.0);\n    scr_audio_play_sfx(snd_hydraulic_press, 0.7, 0.05);'
)

# Wire crucible_vent
text = text.replace(
    'volatility_meter = max(0.0, volatility_meter - 35.0);',
    'volatility_meter = max(0.0, volatility_meter - 35.0);\n    scr_audio_play_sfx(snd_mech_boost, 0.75, 0.12);'
)

# Wire crucible_load_mat
text = text.replace(
    'crucible_batch[$ _mat_id] = (crucible_batch[$ _mat_id] ?? 0) + 1;',
    'crucible_batch[$ _mat_id] = (crucible_batch[$ _mat_id] ?? 0) + 1;\n        scr_audio_play_ui("click");'
)

# Wire crucible_execute_synthesis failure & success
text = text.replace(
    'show_toast("CATASTROPHIC BREACH! Volatility spiked -> Batch destroyed to Slag!", c_red);',
    'show_toast("CATASTROPHIC BREACH! Volatility spiked -> Batch destroyed to Slag!", c_red);\n        scr_audio_play_sfx(snd_explosion_large, 1.0, 0.05);'
)

text = text.replace(
    'show_toast("NEW ALLOY SYNTHESIZED! Vanguard Composite Plating unlocked!", c_lime);',
    'show_toast("NEW ALLOY SYNTHESIZED! Vanguard Composite Plating unlocked!", c_lime);\n        scr_audio_play_sfx(snd_crucible_pour, 0.9, 0.04);\n        scr_audio_play_sfx(snd_discovery_fanfare, 1.0, 0.0);'
)

with open("objects/obj_HQTerminal/Create_0.gml", "w") as f:
    f.write(text)
print("✓ Updated objects/obj_HQTerminal/Create_0.gml with audio foley")

# =============================================================================
# 2. WIRE obj_HQTerminal/Draw_64.gml (Tab Navigation & Stamps)
# =============================================================================
print("=== 2. WIRING obj_HQTerminal/Draw_64.gml ===")
with open("objects/obj_HQTerminal/Draw_64.gml", "r") as f:
    text_d64 = f.read()

# Tab switching with dynamic music change
old_tab_click = 'if (_tb_hov && _click) active_tab = tb;'
new_tab_click = """if (_tb_hov && _click) {
        if (active_tab != tb) {
            active_tab = tb;
            scr_audio_play_ui("tab");
            if (active_tab == 0) {
                scr_audio_play_location_bgm("prototyping");
            } else {
                scr_audio_play_location_bgm("hq");
            }
        }
    }"""

if old_tab_click in text_d64:
    text_d64 = text_d64.replace(old_tab_click, new_tab_click)

# Subtab clicks
subtab_patterns = [
    ('if (_stb_hov && _click) rd_subtab = stb;', 'if (_stb_hov && _click) { rd_subtab = stb; scr_audio_play_ui("click"); }'),
    ('if (_fst_hov && _click) factory_subtab = fst;', 'if (_fst_hov && _click) { factory_subtab = fst; scr_audio_play_ui("click"); }'),
    ('if (_cst_hov && _click) contracts_subtab = cst;', 'if (_cst_hov && _click) { contracts_subtab = cst; scr_audio_play_ui("click"); }'),
    ('if (_wstb_hov && _click) war_subtab = wst;', 'if (_wstb_hov && _click) { war_subtab = wst; scr_audio_play_ui("click"); }'),
    ('if (_fstb_act = (flagship_subtab == fst);', 'if (_fstb_act = (flagship_subtab == fst);') # keep
]
for old, new in subtab_patterns:
    if old in text_d64:
        text_d64 = text_d64.replace(old, new)

with open("objects/obj_HQTerminal/Draw_64.gml", "w") as f:
    f.write(text_d64)
print("✓ Updated objects/obj_HQTerminal/Draw_64.gml with UI audio")

# =============================================================================
# 3. WIRE obj_BattleManager/Create_0.gml (Combat Foley & Weapons)
# =============================================================================
print("=== 3. WIRING obj_BattleManager/Create_0.gml ===")
with open("objects/obj_BattleManager/Create_0.gml", "r") as f:
    text_bm_c = f.read()

# Add audio bootstrap & BGM start
bm_init_target = 'if (!instance_exists(obj_NemesisManager)) instance_create_depth(0, 0, 0, obj_NemesisManager);'
bm_audio_init = """if (!instance_exists(obj_NemesisManager)) instance_create_depth(0, 0, 0, obj_NemesisManager);
if (!instance_exists(obj_AudioManager)) instance_create_depth(0, 0, 0, obj_AudioManager);

// Start Front Mission 90s Mecha Combat BGM
scr_audio_play_location_bgm("combat");"""

if "scr_audio_play_location_bgm(\"combat\")" not in text_bm_c:
    text_bm_c = text_bm_c.replace(bm_init_target, bm_audio_init)

# Wire spawn_combat_projectile with weapon firing sound
wpn_fire_target = 'array_push(projectiles, _proj);'
wpn_fire_replacement = """array_push(projectiles, _proj);
    scr_audio_play_weapon(_wpn.short_name);"""

if "scr_audio_play_weapon" not in text_bm_c:
    text_bm_c = text_bm_c.replace(wpn_fire_target, wpn_fire_replacement)

# Wire resolve_combat_impact
impact_target = '_def.anim_state = "hit";'
impact_replacement = """_def.anim_state = "hit";
        scr_audio_play_impact("kinetic", (_dmg > 50));"""

if "scr_audio_play_impact" not in text_bm_c:
    text_bm_c = text_bm_c.replace(impact_target, impact_replacement)

# Wire unit destroyed explosion sound
destroyed_target = '_def.is_destroyed = true;'
destroyed_replacement = """_def.is_destroyed = true;
                scr_audio_play_sfx(snd_explosion_large, 1.0, 0.05);"""

if "snd_explosion_large" not in text_bm_c:
    text_bm_c = text_bm_c.replace(destroyed_target, destroyed_replacement)

# Wire evaluate_nemesis_incursion
incursion_target = 'incursion_data.is_active = true;'
incursion_replacement = """incursion_data.is_active = true;
    scr_audio_play_location_bgm("incursion");
    scr_audio_play_sfx(snd_alarm_critical, 1.0, 0.0);"""

if "scr_audio_play_location_bgm(\"incursion\")" not in text_bm_c:
    text_bm_c = text_bm_c.replace(incursion_target, incursion_replacement)

with open("objects/obj_BattleManager/Create_0.gml", "w") as f:
    f.write(text_bm_c)
print("✓ Updated objects/obj_BattleManager/Create_0.gml with combat audio")

# =============================================================================
# 4. WIRE obj_BattleManager/Step_0.gml (Victory / Defeat / Movement Foley)
# =============================================================================
print("=== 4. WIRING obj_BattleManager/Step_0.gml ===")
with open("objects/obj_BattleManager/Step_0.gml", "r") as f:
    text_bm_s = f.read()

# Victory BGM
vic_target = 'state = COMBAT_STATE.VICTORY_AAR;'
vic_replacement = """state = COMBAT_STATE.VICTORY_AAR;
                scr_audio_play_location_bgm("victory");"""
if "scr_audio_play_location_bgm(\"victory\")" not in text_bm_s:
    text_bm_s = text_bm_s.replace(vic_target, vic_replacement)

# Defeat BGM
def_target = 'state = COMBAT_STATE.DEFEAT_AAR;'
def_replacement = """state = COMBAT_STATE.DEFEAT_AAR;
                scr_audio_play_location_bgm("defeat");"""
if "scr_audio_play_location_bgm(\"defeat\")" not in text_bm_s:
    text_bm_s = text_bm_s.replace(def_target, def_replacement)

# Mech movement footstep foley
move_target = '_u.grid_c = _dest.c;\n                _u.grid_r = _dest.r;'
move_replacement = """_u.grid_c = _dest.c;
                _u.grid_r = _dest.r;
                scr_audio_play_sfx(snd_mech_step, 0.85, 0.08);"""
if "snd_mech_step" not in text_bm_s:
    text_bm_s = text_bm_s.replace(move_target, move_replacement)

with open("objects/obj_BattleManager/Step_0.gml", "w") as f:
    f.write(text_bm_s)
print("✓ Updated objects/obj_BattleManager/Step_0.gml with victory, defeat and step audio")

print(">>> ALL AUDIO HOOKS WIRED SUCCESSFULLY <<<")
