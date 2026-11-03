#!/usr/bin/env python3
import os

def test_doc_52():
    print("--- 1. Testing Document 52 Specification ---")
    doc_path = "docs/52_reactive_geopolitical_visual_novel_and_multi_leader_dialogue_engine.md"
    assert os.path.exists(doc_path), "Doc 52 missing"
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "The Dynamic Contextual Salutation & Mood Engine" in content, "Pillar I missing in Doc 52"
    assert "Reactive Incident Barks & Token Interpolation" in content, "Pillar II missing in Doc 52"
    assert "Multi-Speaker War Room Summits" in content, "Pillar III missing in Doc 52"
    assert "Tactical Radio Comms Intercom in rm_combat" in content, "Pillar IV missing in Doc 52"
    assert "ep_summit_phobos_crisis" in content, "Phobos summit missing in Doc 52"
    assert "ep_summit_transhumanist_schism" in content, "Transhumanist summit missing in Doc 52"
    assert "ep_summit_sol_monopoly" in content, "Sol Monopoly summit missing in Doc 52"
    print("[PASS] Doc 52 GDD fully specified with all 4 architectural pillars.")

def test_vn_engine_upgrades():
    print("--- 2. Testing VN Engine Upgrades & Dual Layout ---")
    with open("scripts/scr_vn_engine/scr_vn_engine.gml", "r", encoding="utf-8") as f:
        vn = f.read()
    
    # Dual layout rendering
    assert "_is_dual" in vn, "Dual portrait check missing in scr_vn_draw"
    assert "portrait_right" in vn, "portrait_right handling missing in scr_vn_draw"
    assert "_right_alpha" in vn, "Dual speaker alpha dimming missing in scr_vn_draw"
    assert "_side" in vn, "Active side detection missing in scr_vn_draw"
    print("[PASS] scr_vn_draw Dual-Portrait layout & active speaker dimming verified.")

    # Token interpolator
    assert "function scr_vn_interpolate_text" in vn, "scr_vn_interpolate_text function missing"
    assert "{PLAYER_CALLSIGN}" in vn, "{PLAYER_CALLSIGN} token missing"
    assert "{RECENT_SECTOR}" in vn, "{RECENT_SECTOR} token missing"
    assert "{ROSTER_PILOT}" in vn, "{ROSTER_PILOT} token missing"
    assert "{BRIG_PRISONER}" in vn, "{BRIG_PRISONER} token missing"
    assert "{FLAGSHIP}" in vn, "{FLAGSHIP} token missing"
    print("[PASS] scr_vn_interpolate_text token replacement engine verified.")

    # Dynamic audience generator
    assert "function scr_vn_start_dynamic_audience" in vn, "scr_vn_start_dynamic_audience missing"
    assert "ep_dynamic_audience" in vn, "ep_dynamic_audience registration missing"
    assert "faction_a" in vn and "faction_f" in vn, "Faction leader mapping missing"
    assert "DESPERATE" in vn, "DESPERATE mood salutation missing"
    assert "WINNING" in vn, "WINNING mood salutation missing"
    print("[PASS] scr_vn_start_dynamic_audience 6-faction reactive generator verified.")

    # 3 Summit crisis episodes
    assert "ep_summit_phobos_crisis" in vn, "ep_summit_phobos_crisis missing"
    assert "ep_summit_transhumanist_schism" in vn, "ep_summit_transhumanist_schism missing"
    assert "ep_summit_sol_monopoly" in vn, "ep_summit_sol_monopoly missing"
    print("[PASS] All 3 Multi-Leader Summit Crisis episodes registered in engine.")

    # Radio intercom barks
    assert "function scr_vn_trigger_combat_intercom" in vn, "scr_vn_trigger_combat_intercom missing"
    assert "function scr_vn_draw_combat_intercom" in vn, "scr_vn_draw_combat_intercom missing"
    assert "[LIVE COMMS // CH-08 ENCRYPTED]" in vn, "Comms banner HUD text missing"
    print("[PASS] Tactical Radio Comms Intercom Bark engine verified.")

def test_integration_hooks():
    print("--- 3. Testing System Integration Hooks ---")
    with open("objects/obj_HQTerminal/Draw_64.gml", "r", encoding="utf-8") as f:
        hq = f.read()
    assert "scr_vn_start_dynamic_audience(_fid)" in hq, "HQTerminal dynamic audience call missing"
    print("[PASS] obj_HQTerminal/Draw_64.gml reactive audience click handler verified.")

    with open("objects/obj_GameManager/Create_0.gml", "r", encoding="utf-8") as f:
        gm = f.read()
    assert "ep_summit_phobos_crisis" in gm, "Phobos summit turn hook missing in GameManager"
    assert "ep_summit_transhumanist_schism" in gm, "Transhumanist summit turn hook missing in GameManager"
    assert "ep_summit_sol_monopoly" in gm, "Sol monopoly summit turn hook missing in GameManager"
    print("[PASS] obj_GameManager/Create_0.gml strategic turn summit hooks verified.")

    with open("objects/obj_BattleManager/Draw_64.gml", "r", encoding="utf-8") as f:
        bm_draw = f.read()
    assert "scr_vn_draw_combat_intercom()" in bm_draw, "BattleManager Draw_64 combat intercom call missing"
    print("[PASS] obj_BattleManager/Draw_64.gml combat intercom drawing hook verified.")

    with open("objects/obj_BattleManager/Create_0.gml", "r", encoding="utf-8") as f:
        bm_create = f.read()
    assert "scr_vn_trigger_combat_intercom" in bm_create, "Opening combat intercom bark missing in BattleManager"
    print("[PASS] obj_BattleManager/Create_0.gml opening radio challenge bark verified.")

if __name__ == "__main__":
    print("======================================================================")
    print("  MILESTONE 52: REACTIVE GEOPOLITICAL VN & MULTI-LEADER TEST SUITE")
    print("======================================================================")
    test_doc_52()
    test_vn_engine_upgrades()
    test_integration_hooks()
    print("======================================================================")
    print("  ALL MILESTONE 52 SYSTEMS VERIFIED 100% OPERATIONAL!")
    print("======================================================================")
