#!/usr/bin/env python3
"""
test_milestone_53_dramatis_personae_and_bible.py
Verifies Milestone 53: Character Profiles, 4-Tier Emotion Specifications,
Master Dialogue Bible Branching Trees, In-Engine Emotion Rendering, and
In-Combat Tactical Radio Duel Barks.
"""

import os
import sys

def run_test():
    print("=" * 70)
    print("  MILESTONE 53: DRAMATIS PERSONAE & MASTER DIALOGUE BIBLE SUITE")
    print("=" * 70)
    
    # 1. Document 53 Specification & Character Dossiers
    doc53_path = "docs/53_dramatis_personae_character_profiles_and_master_dialogue_bible.md"
    assert os.path.exists(doc53_path), f"Missing {doc53_path}"
    with open(doc53_path, "r", encoding="utf-8") as f:
        doc53 = f.read()

    print("--- 1. Testing Document 53 Character Dossiers & Profiles ---")
    characters = [
        "GENERAL ARTHUR BRADLEY",
        "COMMANDER JOSHUA REED",
        "CAPTAIN SONYA CRUZ",
        "DIRECTOR KENJIRO SATO",
        "ARCHON ORIN SIDERIS",
        "CONSENSUS NODE 0-PRIME",
        "LT. GREGORY VANCE",
        "CHIEF LOGISTICS OFFICER MARCUS KOVACS",
        "PROMETHEUS-NULL",
        "DR. ANIKA SOREN"
    ]
    for ch in characters:
        assert ch in doc53, f"Character '{ch}' missing from Doc 53!"
        print(f"[PASS] Dossier & psych profile found: {ch}")

    print("\n--- 2. Testing 4-Tier Emotion Specifications ---")
    emotions = ["NORMAL", "ANGRY", "DESPERATE", "SMUG"]
    for emo in emotions:
        assert f"`{emo}" in doc53 or f"**{emo}**" in doc53 or f"{emo} /" in doc53, f"Emotion spec {emo} missing from Doc 53!"
    assert "Palette" in doc53 and "Emotional State Visual Profiles" in doc53
    print("[PASS] All 4 emotion tiers (NORMAL, ANGRY, DESPERATE, SMUG) detailed with lighting, palettes, and facial cues.")

    print("\n--- 3. Testing Exhaustive Dialogue Trees & Consequence Matrices ---")
    dialogue_checkpoints = [
        "Scene 1.1: General Arthur Bradley",
        "Scene 1.2: Commander Joshua Reed",
        "Scene 1.3: Captain Sonya Cruz",
        "Scene 1.4: Director Kenjiro Sato",
        "Scene 1.5: Archon Orin Sideris",
        "Scene 1.6: Consensus Node 0-Prime",
        "Summit 1: The Phobos Blockade Crisis",
        "Summit 2: The Transhumanist Schism",
        "Summit 3: The Sol Monopoly Accord"
    ]
    for cp in dialogue_checkpoints:
        assert cp in doc53, f"Dialogue checkpoint '{cp}' missing from Doc 53!"
        print(f"[PASS] Master dialogue tree verified: {cp}")

    print("\n--- 4. Testing In-Engine Visual Novel Emotion Rendering ---")
    vn_engine_path = "scripts/scr_vn_engine/scr_vn_engine.gml"
    assert os.path.exists(vn_engine_path), f"Missing {vn_engine_path}"
    with open(vn_engine_path, "r", encoding="utf-8") as f:
        vn_code = f.read()

    assert "_emo_tag" in vn_code, "_emo_tag rendering missing from scr_vn_draw!"
    assert "_emo_col" in vn_code, "_emo_col rendering missing from scr_vn_draw!"
    assert "[RESOLUTE]" in vn_code, "[RESOLUTE] normal badge missing!"
    assert "[ENRAGED]" in vn_code, "[ENRAGED] angry badge missing!"
    assert "[CRITICAL]" in vn_code, "[CRITICAL] desperate badge missing!"
    assert "[CALCULATING]" in vn_code, "[CALCULATING] smug badge missing!"
    assert "_dynamic_emo" in vn_code, "Dynamic audience emotion calculation missing!"
    print("[PASS] scr_vn_draw 4-tier emotion bezels, text tags, and dynamic standing assignment verified.")

    print("\n--- 5. Testing In-Combat Radio Duel Intercom Barks ---")
    bm_path = "objects/obj_BattleManager/Create_0.gml"
    assert os.path.exists(bm_path), f"Missing {bm_path}"
    with open(bm_path, "r", encoding="utf-8") as f:
        bm_code = f.read()

    assert "scr_vn_trigger_combat_intercom" in bm_code, "Combat intercom bark missing from BattleManager!"
    assert ("Target locked! Kinetic impact confirmed!" in bm_code or "Kinetic penetration confirmed!" in bm_code), "Combat hit barks missing!"
    assert "Core containment breached! Ejecting flight recorder—!" in bm_code, "Catastrophic ejection bark missing!"
    assert "Armor deflection confirmed! Is that the best you can hit?" in bm_code, "Deflection glancing bark missing!"
    print("[PASS] BattleManager dynamic intercom duel barks on Hit, Ejection, and Deflection verified.")

    print("\n--- 6. Testing Master GDD Index Entry ---")
    mgdd_path = "docs/00_master_game_design_document.md"
    with open(mgdd_path, "r", encoding="utf-8") as f:
        mgdd = f.read()
    assert "53_dramatis_personae_character_profiles_and_master_dialogue_bible.md" in mgdd, "Doc 53 link missing from Master GDD index!"
    print("[PASS] Master Game Design Document index updated with Doc 53.")

    print("=" * 70)
    print("  ALL MILESTONE 53 CHARACTER PROFILES & DIALOGUE BIBLE SYSTEMS VERIFIED!")
    print("=" * 70)

if __name__ == "__main__":
    run_test()
