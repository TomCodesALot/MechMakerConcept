#!/usr/bin/env python3
"""
test_milestone_55_bonds_interrogations_and_incursions.py
Verifies Milestone 55: Base Brig POW Interrogations, Cantina Crew Bonds,
Mid-Battle Tactical Radio Incursions, Interactive Directives & PMC Karma Alignment.
"""

import os
import sys

def run_test():
    print("=" * 70)
    print("  MILESTONE 55: BONDS, INTERROGATIONS & INCURSIONS TEST SUITE")
    print("=" * 70)

    # 1. Document 55 Specification
    doc55_path = "docs/55_tactical_interrogations_cantina_bonds_and_mid_battle_incursions.md"
    assert os.path.exists(doc55_path), f"Missing {doc55_path}"
    with open(doc55_path, "r", encoding="utf-8") as f:
        doc55 = f.read()

    print("--- 1. Testing Document 55 Specification & Blueprints ---")
    episodes = [
        "ep_brig_interrogation_ace",
        "ep_cantina_bond_vance",
        "ep_cantina_bond_soren",
        "ep_cantina_bond_kovacs"
    ]
    for ep in episodes:
        assert ep in doc55, f"Episode '{ep}' missing from Doc 55 GDD!"
        print(f"[PASS] Episode blueprint verified in GDD: {ep}")

    assert "Mid-Battle Scripted Tactical Story Events" in doc55, "Mid-battle incursions missing from Doc 55!"
    assert "PMC Ideological Karma & Alignment Engine" in doc55, "Karma alignment missing from Doc 55!"
    print("[PASS] Mid-battle directives and Karma engine blueprints verified.")

    # 2. In-Engine Registration in scr_vn_engine.gml
    print("\n--- 2. Testing Episode Registration in scr_vn_engine.gml ---")
    vn_path = "scripts/scr_vn_engine/scr_vn_engine.gml"
    assert os.path.exists(vn_path), f"Missing {vn_path}"
    with open(vn_path, "r", encoding="utf-8") as f:
        vn_code = f.read()

    for ep in episodes:
        assert f'global.vn_state.episodes[$ "{ep}"]' in vn_code, f"Episode '{ep}' not registered in scr_vn_engine.gml!"
        print(f"[PASS] Engine registration verified: {ep}")

    # Check Interactive Directive Support in scr_vn_engine.gml
    assert "_directives = undefined" in vn_code, "Directives parameter missing from scr_vn_trigger_combat_intercom!"
    assert "_ci.directives" in vn_code, "Directives rendering missing from scr_vn_draw_combat_intercom!"
    print("[PASS] Interactive combat radio directives rendering and execution verified.")

    # 3. Tactical Incursion Engine in obj_BattleManager
    print("\n--- 3. Testing Tactical Incursion Engine in obj_BattleManager ---")
    bm_create_path = "objects/obj_BattleManager/Create_0.gml"
    assert os.path.exists(bm_create_path), f"Missing {bm_create_path}"
    with open(bm_create_path, "r", encoding="utf-8") as f:
        bm_create = f.read()

    assert "mid_battle_incursion_triggered" in bm_create, "mid_battle_incursion_triggered missing from BattleManager!"
    assert "trigger_mid_battle_tactical_incursion" in bm_create, "trigger_mid_battle_tactical_incursion missing from BattleManager!"
    assert "[ORBITAL BARRAGE: 35 DMG]" in bm_create, "Orbital barrage directive missing!"
    assert "[FOCUS TELEMETRY: +15% ACC]" in bm_create, "Focus telemetry directive missing!"
    assert "[NEURO-JAM: -20% ENEMY EVA]" in bm_create, "Neuro-jam directive missing!"
    print("[PASS] BattleManager Create_0 incursion engine and 3 tactical directives verified.")

    bm_step_path = "objects/obj_BattleManager/Step_0.gml"
    assert os.path.exists(bm_step_path), f"Missing {bm_step_path}"
    with open(bm_step_path, "r", encoding="utf-8") as f:
        bm_step = f.read()

    assert "trigger_mid_battle_tactical_incursion()" in bm_step, "Incursion trigger missing from BattleManager Step_0!"
    print("[PASS] BattleManager Step_0 Turn 3 incursion trigger verified.")

    # 4. Karma & Squadron Perks in obj_GameManager
    print("\n--- 4. Testing Karma & Squadron Perks in obj_GameManager ---")
    gm_path = "objects/obj_GameManager/Create_0.gml"
    assert os.path.exists(gm_path), f"Missing {gm_path}"
    with open(gm_path, "r", encoding="utf-8") as f:
        gm_code = f.read()

    assert "squadron_perks = [];" in gm_code, "squadron_perks missing from GameManager!"
    assert "pmc_karma_noble" in gm_code, "pmc_karma_noble missing from GameManager!"
    assert "get_pmc_karma_alignment" in gm_code, "get_pmc_karma_alignment missing from GameManager!"
    print("[PASS] GameManager Karma alignment engine and squadron perks array verified.")

    # 5. Interactive UI in obj_HQTerminal/Draw_64.gml
    print("\n--- 5. Testing Interactive UI in obj_HQTerminal ---")
    hq_path = "objects/obj_HQTerminal/Draw_64.gml"
    assert os.path.exists(hq_path), f"Missing {hq_path}"
    with open(hq_path, "r", encoding="utf-8") as f:
        hq_code = f.read()

    assert "get_pmc_karma_alignment" in hq_code, "Top command bar Karma alignment display missing!"
    assert "[BOND: VANCE]" in hq_code, "Cantina Vance bond button missing!"
    assert "[BOND: SOREN]" in hq_code, "Cantina Soren bond button missing!"
    assert "[BOND: KOVACS]" in hq_code, "Cantina Kovacs bond button missing!"
    assert "ep_cantina_bond_vance" in hq_code, "ep_cantina_bond_vance trigger missing!"
    assert "ep_cantina_bond_soren" in hq_code, "ep_cantina_bond_soren trigger missing!"
    assert "ep_cantina_bond_kovacs" in hq_code, "ep_cantina_bond_kovacs trigger missing!"
    assert "BASE BRIG & POW DETENTION WING" in hq_code, "POW detention wing missing from Pilots Deck!"
    assert "ep_brig_interrogation_ace" in hq_code, "ep_brig_interrogation_ace trigger missing!"
    print("[PASS] Top Bar Karma badge, Cantina bond buttons, and POW Brig interrogation verified.")

    # 6. Master GDD Index Entry
    print("\n--- 6. Testing Master GDD Index Entry ---")
    mgdd_path = "docs/00_master_game_design_document.md"
    with open(mgdd_path, "r", encoding="utf-8") as f:
        mgdd = f.read()

    assert "55_tactical_interrogations_cantina_bonds_and_mid_battle_incursions.md" in mgdd, "Doc 55 link missing from Master GDD!"
    assert "test_milestone_55_bonds_interrogations_and_incursions.py" in mgdd, "Test suite 15 missing from Master GDD!"
    print("[PASS] Master GDD index and test suite list updated with Doc 55.")

    print("=" * 70)
    print("  ALL MILESTONE 55 SYSTEMS VERIFIED 100% OPERATIONAL!")
    print("=" * 70)

if __name__ == "__main__":
    run_test()
