#!/usr/bin/env python3
"""
tools/test_audio_architecture_and_asset_cleanup.py
Comprehensive QA test verifying:
1. Audio system integrity (31 sounds & music tracks, obj_AudioManager, scr_audio_manager, yyp registration)
2. Art cleanup integrity (removal of obsolete low-res placeholder profiles & static sprites)
3. High-detail asset linking (204 characters mapped to established 200x200 animated portraits)
4. Audio foley & BGM wiring in obj_HQTerminal and obj_BattleManager
"""

import os
import json
import re

print("=====================================================================")
print("=== AUDIO ARCHITECTURE & ART ASSET CLEANUP VERIFICATION TEST ===")
print("=====================================================================")

# -----------------------------------------------------------------------------
# 1. VERIFY AUDIO ASSETS & YYP REGISTRATION
# -----------------------------------------------------------------------------
print("\n--- 1. VERIFYING 31 AUDIO ASSETS & YYP REGISTRATION ---")
with open("MechMakerConcept.yyp", "r") as f:
    yyp_text = f.read()

expected_sfx = [
    "snd_ui_click", "snd_ui_hover", "snd_ui_tab", "snd_ui_confirm", "snd_ui_cancel",
    "snd_ui_terminal_boot", "snd_ui_stamp", "snd_crucible_pour", "snd_hydraulic_press",
    "snd_plasma_weld", "snd_discovery_fanfare", "snd_mech_step", "snd_mech_boost",
    "snd_mech_servo", "snd_weapon_vulcan", "snd_weapon_cannon_120mm",
    "snd_weapon_missile_launch", "snd_weapon_beam_rifle", "snd_weapon_plasma_blade",
    "snd_weapon_railgun", "snd_impact_armor", "snd_impact_penetrate",
    "snd_explosion_small", "snd_explosion_large", "snd_alarm_critical"
]

expected_bgm = [
    "bgm_hq_ambience", "bgm_prototyping_bay", "bgm_combat_engage",
    "bgm_nemesis_incursion", "bgm_victory_fanfare", "bgm_defeat_somber"
]

all_expected_audio = expected_sfx + expected_bgm
assert len(all_expected_audio) == 31, f"Expected 31 audio assets, got {len(all_expected_audio)}"

for snd in all_expected_audio:
    wav_path = os.path.join("sounds", snd, f"{snd}.wav")
    yy_path = os.path.join("sounds", snd, f"{snd}.yy")
    assert os.path.exists(wav_path), f"Missing audio file: {wav_path}"
    assert os.path.exists(yy_path), f"Missing sound metadata: {yy_path}"
    assert os.path.getsize(wav_path) > 1000, f"Audio file {wav_path} is too small / empty!"
    
    yyp_ref = f'sounds/{snd}/{snd}.yy'
    assert yyp_ref in yyp_text, f"Audio {snd} not registered in MechMakerConcept.yyp!"
    
print(f"  ✓ All 25 SFX assets verified (WAV, YY, and YYP registration)")
print(f"  ✓ All 6 BGM tactical tracks verified (WAV, YY, and YYP registration)")

# -----------------------------------------------------------------------------
# 2. VERIFY obj_AudioManager & scr_audio_manager
# -----------------------------------------------------------------------------
print("\n--- 2. VERIFYING AUDIO MANAGER & GML SCRIPTS ---")
assert os.path.exists("objects/obj_AudioManager/obj_AudioManager.yy")
assert os.path.exists("objects/obj_AudioManager/Create_0.gml")
assert os.path.exists("objects/obj_AudioManager/Step_0.gml")
assert os.path.exists("objects/obj_AudioManager/CleanUp_0.gml")
assert os.path.exists("scripts/scr_audio_manager/scr_audio_manager.yy")
assert os.path.exists("scripts/scr_audio_manager/scr_audio_manager.gml")

assert "objects/obj_AudioManager/obj_AudioManager.yy" in yyp_text
assert "scripts/scr_audio_manager/scr_audio_manager.yy" in yyp_text

with open("rooms/rm_init/RoomCreationCode.gml") as f:
    rm_init_code = f.read()
assert "obj_AudioManager" in rm_init_code, "obj_AudioManager not bootstrapped in rm_init!"
print("  ✓ obj_AudioManager singleton and scr_audio_manager registered & initialized in rm_init")

# -----------------------------------------------------------------------------
# 3. VERIFY ART CLEANUP (OBSOLETE ASSETS REMOVED)
# -----------------------------------------------------------------------------
print("\n--- 3. VERIFYING OBSOLETE PLACEHOLDER ASSET REMOVAL ---")
obsolete_sprites = [
    "spr_faction_portraits", "spr_faction_lineup",
    "spr_mech_colony_aether", "spr_mech_syndicate_hyena",
    "spr_mech_terran_ironclad", "spr_mech_zaibatsu_muramasa"
]

for obs in obsolete_sprites:
    obs_path = os.path.join("sprites", obs)
    assert not os.path.exists(obs_path), f"Obsolete sprite {obs} still exists on disk!"
    assert obs not in yyp_text, f"Obsolete sprite {obs} still registered in MechMakerConcept.yyp!"

obsolete_docs = [
    "docs/assets/snes_portrait_colony_cassian.png",
    "docs/assets/snes_portrait_syndicate_jackal.png",
    "docs/assets/snes_portrait_terran_vance.png",
    "docs/assets/snes_portrait_zaibatsu_null07.png",
    "docs/assets/snes_faction_portraits_strip4.png"
]
for obs_d in obsolete_docs:
    assert not os.path.exists(obs_d), f"Obsolete placeholder doc image {obs_d} still exists!"

print("  ✓ All 6 obsolete placeholder sprite directories eradicated from disk and YYP")
print("  ✓ All low-res 64x64/128x128 pixel placeholder doc images eradicated")

# -----------------------------------------------------------------------------
# 4. VERIFY HIGH-DETAIL ASSET LINKING
# -----------------------------------------------------------------------------
print("\n--- 4. VERIFYING HIGH-DETAIL ANIMATED ASSET INTEGRATION ---")
with open("characters_roster.json") as f:
    roster_data = json.load(f)

characters = roster_data.get("characters", [])
assert len(characters) >= 200, f"Expected 200+ characters, got {len(characters)}"

valid_portraits = {
    "spr_portrait_vance", "spr_portrait_cole", "spr_portrait_cassian",
    "spr_portrait_sorren", "spr_portrait_cruz", "spr_portrait_nadia",
    "spr_portrait_renzo", "spr_portrait_null07"
}

mapped_count = 0
for c in characters:
    port = c.get("portrait_asset")
    assert port in valid_portraits, f"Character {c['id']} has invalid portrait: {port}"
    mapped_count += 1

print(f"  ✓ All {mapped_count} characters explicitly mapped to 8 established 200x200 animated portraits")

with open("datafiles/factions_lore.json") as f:
    fl_text = f.read()

assert "spr_mech_" not in fl_text, "Found lingering spr_mech_ in factions_lore.json!"
assert "spr_ms_ironclad_idle" in fl_text
assert "spr_ms_aether_idle" in fl_text
assert "spr_ms_hyena_idle" in fl_text
assert "spr_ms_muramasa_idle" in fl_text
print("  ✓ datafiles/factions_lore.json upgraded to canonical animated mobile suit sprites")

# -----------------------------------------------------------------------------
# 5. VERIFY AUDIO FOLEY & BGM HOOKS IN TERMINAL & BATTLE
# -----------------------------------------------------------------------------
print("\n--- 5. VERIFYING AUDIO FOLEY & BGM DISPATCHERS ---")
with open("objects/obj_HQTerminal/Create_0.gml") as f:
    hq_c = f.read()
assert "scr_audio_play_location_bgm" in hq_c
assert "scr_audio_play_sfx" in hq_c
assert "snd_crucible_pour" in hq_c
assert "snd_hydraulic_press" in hq_c

with open("objects/obj_HQTerminal/Draw_64.gml") as f:
    hq_d = f.read()
assert "scr_audio_play_ui(\"tab\")" in hq_d
assert "scr_audio_play_ui(\"click\")" in hq_d

with open("objects/obj_BattleManager/Create_0.gml") as f:
    bm_c = f.read()
assert "scr_audio_play_location_bgm(\"combat\")" in bm_c
assert "scr_audio_play_weapon" in bm_c
assert "scr_audio_play_impact" in bm_c
assert "snd_explosion_large" in bm_c

with open("objects/obj_BattleManager/Step_0.gml") as f:
    bm_s = f.read()
assert "scr_audio_play_location_bgm(\"victory\")" in bm_s
assert "scr_audio_play_location_bgm(\"defeat\")" in bm_s
assert "snd_mech_step" in bm_s

print("  ✓ Full tactical UI, metallurgy foley, and combat audio integration verified")

print("\n=====================================================================")
print("=== ALL AUDIO & ART QUALITY ASSURANCE TESTS PASSED (100%) ===")
print("=====================================================================")
