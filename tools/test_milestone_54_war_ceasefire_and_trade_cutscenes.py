#!/usr/bin/env python3
"""
test_milestone_54_war_ceasefire_and_trade_cutscenes.py
Verifies Milestone 54: Inter-Faction War Declarations, Brokered Armistices,
Direct Strategic Player Trade Delegations, and Rival Corporate Contract Interceptions.
"""

import os
import sys

def run_test():
    print("=" * 70)
    print("  MILESTONE 54: WAR DECLARATIONS, CEASEFIRES & TRADE CUTSCENES")
    print("=" * 70)

    # 1. Document 54 Specification
    doc54_path = "docs/54_geopolitical_warfare_ceasefires_and_corporate_trade_cutscenes.md"
    assert os.path.exists(doc54_path), f"Missing {doc54_path}"
    with open(doc54_path, "r", encoding="utf-8") as f:
        doc54 = f.read()

    print("--- 1. Testing Document 54 Specification & Episode Blueprints ---")
    episodes = [
        "ep_war_terran_vs_colony",
        "ep_war_zaibatsu_vs_tharsis",
        "ep_war_syndicate_vs_sidereal",
        "ep_ceasefire_terran_colony",
        "ep_ceasefire_zaibatsu_tharsis",
        "ep_trade_terran_delegation",
        "ep_trade_syndicate_black_market",
        "ep_trade_rival_valkyrie_deal",
        "ep_trade_rival_hyperion_arms"
    ]
    for ep in episodes:
        assert ep in doc54, f"Episode '{ep}' missing from Doc 54 GDD!"
        print(f"[PASS] Blueprint verified in GDD: {ep}")

    # 2. In-Engine Registration in scr_vn_engine.gml
    print("\n--- 2. Testing Episode Registration in scr_vn_engine.gml ---")
    vn_path = "scripts/scr_vn_engine/scr_vn_engine.gml"
    assert os.path.exists(vn_path), f"Missing {vn_path}"
    with open(vn_path, "r", encoding="utf-8") as f:
        vn_code = f.read()

    for ep in episodes:
        assert f'global.vn_state.episodes[$ "{ep}"]' in vn_code, f"Episode '{ep}' not registered in scr_vn_engine.gml!"
        print(f"[PASS] Engine registration verified: {ep}")

    # Check Choice Action Closures
    assert "obj_FactionManager.declare_war" in vn_code, "War declaration action missing from VN choices!"
    assert "obj_FactionManager.broker_truce" in vn_code, "Truce brokering action missing from VN choices!"
    assert "obj_GameManager.pmc_market_share_pct" in vn_code, "Market share manipulation missing from VN choices!"
    print("[PASS] Action closures for war, truces, and corporate market share verified.")

    # 3. Faction Diplomacy Hooks in obj_FactionManager
    print("\n--- 3. Testing Faction Diplomacy Hooks in obj_FactionManager ---")
    fm_path = "objects/obj_FactionManager/Create_0.gml"
    assert os.path.exists(fm_path), f"Missing {fm_path}"
    with open(fm_path, "r", encoding="utf-8") as f:
        fm_code = f.read()

    assert "ep_war_terran_vs_colony" in fm_code, "War cutscene hook missing from declare_war!"
    assert "ep_war_zaibatsu_vs_tharsis" in fm_code, "Zaibatsu war hook missing from declare_war!"
    assert "ep_war_syndicate_vs_sidereal" in fm_code, "Syndicate war hook missing from declare_war!"
    assert "ep_ceasefire_terran_colony" in fm_code, "Ceasefire cutscene hook missing from broker_truce!"
    assert "ep_ceasefire_zaibatsu_tharsis" in fm_code, "Tharsis ceasefire hook missing from broker_truce!"
    print("[PASS] declare_war & broker_truce dynamic VN episode dispatch verified.")

    # 4. Strategic Turn Milestone Hooks in obj_GameManager
    print("\n--- 4. Testing Strategic Turn Progression in obj_GameManager ---")
    gm_path = "objects/obj_GameManager/Create_0.gml"
    assert os.path.exists(gm_path), f"Missing {gm_path}"
    with open(gm_path, "r", encoding="utf-8") as f:
        gm_code = f.read()

    assert "current_turn == 9" in gm_code and "ep_war_terran_vs_colony" in gm_code, "Turn 9 war hook missing!"
    assert "current_turn == 11" in gm_code and "ep_trade_rival_valkyrie_deal" in gm_code, "Turn 11 corporate trade hook missing!"
    assert "current_turn == 14" in gm_code and "ep_war_zaibatsu_vs_tharsis" in gm_code, "Turn 14 war hook missing!"
    assert "current_turn == 16" in gm_code and "ep_trade_rival_hyperion_arms" in gm_code, "Turn 16 corporate contraband hook missing!"
    assert "current_turn == 19" in gm_code and "ep_war_syndicate_vs_sidereal" in gm_code, "Turn 19 war hook missing!"
    assert "current_turn == 22" in gm_code and "ep_ceasefire_terran_colony" in gm_code, "Turn 22 armistice hook missing!"
    print("[PASS] Strategic turn milestones 9, 11, 14, 16, 19, 22 verified.")

    # 5. Interactive UI Buttons in obj_HQTerminal/Draw_64.gml
    print("\n--- 5. Testing Interactive UI Buttons in obj_HQTerminal ---")
    hq_path = "objects/obj_HQTerminal/Draw_64.gml"
    assert os.path.exists(hq_path), f"Missing {hq_path}"
    with open(hq_path, "r", encoding="utf-8") as f:
        hq_code = f.read()

    assert "[HAIL COALITION TRADE ENVOY]" in hq_code, "Coalition trade envoy hail button missing!"
    assert "[HAIL BLACK-MARKET VAULT]" in hq_code, "Black-market vault hail button missing!"
    assert "ep_trade_terran_delegation" in hq_code, "Terran trade delegation trigger missing!"
    assert "ep_trade_syndicate_black_market" in hq_code, "Syndicate black market trigger missing!"
    assert "INTERCEPT RIVAL MEGA-CONTRACT // ESPIONAGE" in hq_code, "Rival corporate intercept button missing!"
    assert "ep_trade_rival_valkyrie_deal" in hq_code, "Valkyrie trade deal trigger missing!"
    assert "ep_trade_rival_hyperion_arms" in hq_code, "Hyperion contraband deal trigger missing!"
    print("[PASS] Trade Exchange envoy hail buttons and Rival Corporate intercept buttons verified.")

    # 6. Master GDD Index Entry
    print("\n--- 6. Testing Master GDD Index Entry ---")
    mgdd_path = "docs/00_master_game_design_document.md"
    with open(mgdd_path, "r", encoding="utf-8") as f:
        mgdd = f.read()

    assert "54_geopolitical_warfare_ceasefires_and_corporate_trade_cutscenes.md" in mgdd, "Doc 54 link missing from Master GDD!"
    assert "test_milestone_54_war_ceasefire_and_trade_cutscenes.py" in mgdd, "Test suite 14 missing from Master GDD!"
    print("[PASS] Master GDD index and test suite list updated with Doc 54.")

    print("=" * 70)
    print("  ALL MILESTONE 54 WAR, CEASEFIRE & TRADE SYSTEMS VERIFIED 100%!")
    print("=" * 70)

if __name__ == "__main__":
    run_test()
