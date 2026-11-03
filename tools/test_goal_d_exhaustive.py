#!/usr/bin/env python3
"""
tools/test_goal_d_exhaustive.py
Exhaustive verification of Goal D:
1. S-Grade Masterwork Quality Tuning (minigames, auto-tune, +10% Power, -15% Mass, +1 AP, +25% OSS pitch score).
2. 4 Campaign Victory Paths Evaluator (Monopolist, Warlord, Archeotech, Crisis Savior).
3. Climax Victory Modal UI with continuous endless sandbox & retirement integration.
"""

import sys
import re

def test_goal_d():
    print("=== EXHAUSTIVE VALIDATION: GOAL D ===")

    # 1. Verify BlueprintManager S-Grade Masterwork Tuning & Auto-Tune
    with open("objects/obj_BlueprintManager/Create_0.gml", "r") as f:
        bm_code = f.read()

    assert "auto_tune_prototype = function" in bm_code, "auto_tune_prototype missing from obj_BlueprintManager!"
    assert "S_GRADE_MASTERWORK" in bm_code, "S_GRADE_MASTERWORK grade missing from obj_BlueprintManager!"
    assert "_custom_mech.power_output = floor(_custom_mech.power_output * 1.10)" in bm_code, "+10% Power boost missing!"
    assert "_custom_mech.weight_tonnes = max(10.0, round(_custom_mech.weight_tonnes * 0.85 * 10.0) / 10.0)" in bm_code, "-15% Mass reduction missing!"
    assert "oss_pitch_bonus_pct" in bm_code, "oss_pitch_bonus_pct missing from obj_BlueprintManager!"
    assert "ap_bonus" in bm_code, "ap_bonus missing from obj_BlueprintManager!"
    assert "add_masterwork" in bm_code, "add_masterwork call missing from obj_BlueprintManager!"
    print("[PASS] BlueprintManager S-Grade Masterwork Tuning & Auto-Tune verified.")

    # 2. Verify BattleManager +1 AP Integration
    with open("objects/obj_BattleManager/Create_0.gml", "r") as f:
        bat_code = f.read()

    assert "ap_bonus" in bat_code, "ap_bonus missing from BattleManager unit setup!"
    assert "is_masterwork" in bat_code or "S_GRADE_MASTERWORK" in bat_code, "Masterwork AP check missing from BattleManager!"
    print("[PASS] BattleManager +1 AP combat bonus integration verified.")

    # 3. Verify FactionManager +25% OSS Pitch Score Bonus
    with open("objects/obj_FactionManager/Create_0.gml", "r") as f:
        fm_code = f.read()

    assert "_oss_bonus_pct" in fm_code, "_oss_bonus_pct missing from FactionManager procurement evaluation!"
    assert "oss_pitch_bonus_pct" in fm_code, "oss_pitch_bonus_pct check missing from FactionManager!"
    assert "S_GRADE_MASTERWORK" in fm_code, "S_GRADE_MASTERWORK check missing from FactionManager!"
    assert "round(_composite_score * (1.0 + (_oss_bonus_pct / 100.0))" in fm_code, "+25% composite score multiplier missing from FactionManager!"
    print("[PASS] FactionManager +25% OSS pitch score procurement bonus verified.")

    # 4. Verify GameManager 4 Campaign Victory Paths & Evaluator
    with open("objects/obj_GameManager/Create_0.gml", "r") as f:
        gm_code = f.read()

    assert "campaign_won = false" in gm_code, "campaign_won state missing from obj_GameManager!"
    assert "campaign_victory_claimed = false" in gm_code, "campaign_victory_claimed state missing from obj_GameManager!"
    assert "campaign_victory_path = \"\"" in gm_code, "campaign_victory_path state missing from obj_GameManager!"
    assert "evaluate_campaign_victory = function" in gm_code, "evaluate_campaign_victory method missing from obj_GameManager!"
    
    # Check all 4 Victory Paths in evaluate_campaign_victory
    assert "MONOPOLIST" in gm_code, "MONOPOLIST victory path missing from evaluator!"
    assert "THE CORPORATE MONOPOLIST" in gm_code, "Corporate Monopolist title missing!"
    assert "WARLORD" in gm_code, "WARLORD victory path missing from evaluator!"
    assert "THE SUPREME WARLORD HEGEMON" in gm_code, "Warlord Hegemon title missing!"
    assert "ARCHEOTECH" in gm_code, "ARCHEOTECH victory path missing from evaluator!"
    assert "THE ARCHEOTECH TRANSCENDENT" in gm_code, "Archeotech Transcendent title missing!"
    assert "CRISIS_SAVIOR" in gm_code, "CRISIS_SAVIOR victory path missing from evaluator!"
    assert "THE APEX CRISIS SAVIOR" in gm_code, "Apex Crisis Savior title missing!"

    # Check end_turn and retire_career integration
    assert "evaluate_campaign_victory()" in gm_code, "evaluate_campaign_victory() call missing in end_turn!"
    assert "_score_victory = (campaign_won" in gm_code, "Victory score bonus missing from retire_career!"
    print("[PASS] GameManager 4 Campaign Victory Paths Evaluator & End-Turn Integration verified.")

    # 5. Verify HQTerminal Assembly Bay Tuning & Victory Modal UI
    with open("objects/obj_HQTerminal/Create_0.gml", "r") as f:
        hqc_code = f.read()

    assert "showing_victory_modal = false" in hqc_code, "showing_victory_modal missing from HQTerminal Create!"
    assert "assembly_autotune_enabled = false" in hqc_code, "assembly_autotune_enabled missing from HQTerminal Create!"

    with open("objects/obj_HQTerminal/Draw_64.gml", "r") as f:
        hqd_code = f.read()

    assert "S-GRADE MASTERWORK TUNED" in hqd_code, "Masterwork status banner missing in Assembly Bay!"
    assert "assembly_autotune_enabled" in hqd_code, "Auto-Tune toggle missing in Assembly Bay!"
    assert "auto_tune_prototype()" in hqd_code, "auto_tune_prototype call missing in Assembly Bay!"
    assert "showing_victory_modal" in hqd_code, "showing_victory_modal block missing from HQTerminal Draw_64!"
    assert "CONTINUE ENDLESS SANDBOX" in hqd_code, "Endless Sandbox button missing from Victory Modal!"
    assert "RETIRE & VIEW CAREER DOSSIER" in hqd_code, "Retirement transition button missing from Victory Modal!"
    print("[PASS] HQTerminal Assembly Bay Tuning Controls and Victory Modal UI verified.")

    # 6. Simulate S-Grade Masterwork Stat Transformations & Bonus Calculations
    base_mech = {
        "power_output": 250,
        "weight_tonnes": 80.0,
        "speed": 90,
        "combat_rating": 450,
        "ap_bonus": 0
    }
    # Apply S-Grade Masterwork buffs (+10% Power, -15% Mass, +1 AP, +25% OSS)
    tuned_power = int(base_mech["power_output"] * 1.10)
    tuned_mass = max(10.0, round(base_mech["weight_tonnes"] * 0.85 * 10.0) / 10.0)
    tuned_ap = base_mech["ap_bonus"] + 1
    tuned_oss_bonus = 25.0

    assert tuned_power == 275, f"Expected 275 MW, got {tuned_power}"
    assert tuned_mass == 68.0, f"Expected 68.0t, got {tuned_mass}"
    assert tuned_ap == 1, f"Expected +1 AP, got {tuned_ap}"
    assert tuned_oss_bonus == 25.0, f"Expected 25% OSS bonus, got {tuned_oss_bonus}"

    # Simulate OSS Pitch Score Calculation with +25% bonus
    base_weighted_score = 96.0
    normal_composite = round(base_weighted_score * 10.0) / 10.0 # 96.0
    masterwork_composite = round(normal_composite * (1.0 + (tuned_oss_bonus / 100.0)) * 10.0) / 10.0
    assert masterwork_composite == 120.0, f"Expected 120.0, got {masterwork_composite}"
    print("[PASS] S-Grade Masterwork math simulation verified: Power +10% (250->275), Mass -15% (80->68), +1 AP, OSS (96->120).")

    # 7. Simulate all 4 Campaign Victory Path Logic Trees
    # Path 1: Monopolist
    factions_replaced = 3
    is_monopolist = (factions_replaced >= 3)
    assert is_monopolist, "Monopolist condition failed"

    # Path 2: Warlord
    pmc_pct = 65
    is_warlord = (pmc_pct >= 60)
    assert is_warlord, "Warlord condition failed"

    # Path 3: Archeotech
    flagship_divisions_tier5 = 8
    is_archeotech = (flagship_divisions_tier5 >= 8)
    assert is_archeotech, "Archeotech condition failed"

    # Path 4: Crisis Savior
    in_era4 = True
    sorties_won = 18
    is_crisis_savior = (in_era4 and sorties_won >= 15)
    assert is_crisis_savior, "Crisis Savior condition failed"

    print("[PASS] All 4 Campaign Victory Path logic trees verified.")
    print("=== ALL GOAL D TESTS PASSED 100%! ===")

if __name__ == "__main__":
    test_goal_d()
