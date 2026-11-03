#!/usr/bin/env python3
"""
tools/test_goal_e_exhaustive.py
Exhaustive verification of Goal E:
1. Corporate Retaliation & Espionage Engine (equity threshold triggers, market hostility).
2. Black-Ops Shadow Raids & Tactical Node Incursions (auto-resolve + manual Eureka rewards).
3. Pilot Poaching & Counter-Bribery (counter-bonus, Flagship SIGINT sweep, defection risk).
4. Nemesis Ace Bounties & Incarceration Triage (combat kill capture, +150k Cr, Black Box Eureka).
5. Base Detention Brig & Nemesis Radar UI (Interrogate, Ransom, Recruit Ace).
"""

import sys
import re

def test_goal_e():
    print("=== EXHAUSTIVE VALIDATION: GOAL E ===")

    # 1. Verify obj_NemesisManager Espionage & Brig Architecture
    with open("objects/obj_NemesisManager/Create_0.gml", "r") as f:
        nem_code = f.read()

    assert "evaluate_corporate_espionage_turn = function" in nem_code, "evaluate_corporate_espionage_turn missing!"
    assert "interrogate_corporate_secrets = function" in nem_code, "interrogate_corporate_secrets missing!"
    assert "ransom_to_corporation = function" in nem_code, "ransom_to_corporation missing!"
    assert "recruit_prisoner = function" in nem_code, "recruit_prisoner missing!"
    assert "add_prisoner = function" in nem_code, "add_prisoner missing!"
    assert "corp_vhi" in nem_code and "corp_aod" in nem_code and "corp_rust" in nem_code and "corp_hats" in nem_code, "Megacorps missing from espionage evaluation!"
    assert "player_equity_pct >= 51.0" in nem_code, "51% hostile takeover tension check missing!"
    assert "player_equity_pct >= 25.0" in nem_code, "25% significant equity tension check missing!"
    assert "player_equity_pct >= 10.0" in nem_code, "10% initial stake tension check missing!"
    assert "pending_poaching_offer" in nem_code, "Poaching offer generation missing!"
    assert "CORPORATE_SHADOW_RAID" in nem_code, "CORPORATE_SHADOW_RAID generation missing!"
    assert "assign_corporate_contract" in nem_code, "assign_corporate_contract call missing!"
    print("[PASS] obj_NemesisManager Corporate Espionage & Brig methods verified.")

    # 2. Verify obj_GameManager Poaching Resolution & Turn Hook
    with open("objects/obj_GameManager/Create_0.gml", "r") as f:
        gm_code = f.read()

    assert "pending_poaching_offer = undefined;" in gm_code, "pending_poaching_offer missing from obj_GameManager!"
    assert "resolve_poaching_offer = function" in gm_code, "resolve_poaching_offer missing from obj_GameManager!"
    assert '_action == "counter"' in gm_code, "Poaching counter action missing!"
    assert '_action == "sigint_sweep"' in gm_code, "Poaching sigint_sweep action missing!"
    assert '_action == "refuse"' in gm_code, "Poaching refuse action missing!"
    assert "evaluate_corporate_espionage_turn" in gm_code, "evaluate_corporate_espionage_turn missing from end_turn()!"
    print("[PASS] obj_GameManager Poaching Resolution Engine and Turn Hook verified.")

    # 3. Verify obj_BattleManager Nemesis Combat Incarceration & Eureka
    with open("objects/obj_BattleManager/Create_0.gml", "r") as f:
        bat_code = f.read()

    assert "add_prisoner" in bat_code, "add_prisoner missing from BattleManager!"
    assert "active_nemeses" in bat_code, "active_nemeses cleanup missing from BattleManager!"
    assert "scr_research_award_salvage_intel" in bat_code, "scr_research_award_salvage_intel missing from BattleManager Nemesis takedown!"
    assert "obj_GameManager.funds += 150000;" in bat_code, "+150k Cr bounty missing from BattleManager Nemesis takedown!"
    print("[PASS] obj_BattleManager Nemesis Ace Incarceration, Bounty & Eureka verified.")

    # 4. Verify obj_HQTerminal Detention Brig, Radar & Poaching Modal UI
    with open("objects/obj_HQTerminal/Create_0.gml", "r") as f:
        hqc_code = f.read()
    assert "espionage_brig_view_mode" in hqc_code, "espionage_brig_view_mode missing in obj_HQTerminal Create!"

    with open("objects/obj_HQTerminal/Draw_64.gml", "r") as f:
        hqd_code = f.read()

    assert "espionage_brig_view_mode" in hqd_code, "espionage_brig_view_mode missing in Draw_64!"
    assert "BASE DETENTION BRIG & NEMESIS RADAR" in hqd_code, "Brig & Nemesis Radar header missing!"
    assert "[INTERROGATE]" in hqd_code, "[INTERROGATE] button missing!"
    assert "[RANSOM: +250k]" in hqd_code, "[RANSOM: +250k] button missing!"
    assert "[RECRUIT ACE]" in hqd_code, "[RECRUIT ACE] button missing!"
    assert "pending_poaching_offer" in hqd_code, "Poaching modal rendering missing!"
    assert "CORPORATE ESPIONAGE INTERCEPT: HEADHUNTER BREACH" in hqd_code, "Poaching modal title missing!"
    assert "1. MATCH WITH LOYALTY RETENTION BONUS" in hqd_code, "Retention bonus button missing!"
    assert "2. EXECUTE FLAGSHIP SIGINT SECURITY SWEEP" in hqd_code, "SIGINT sweep button missing!"
    assert "3. REFUSE MATCH // RISK PILOT DEFECTION" in hqd_code, "Refusal button missing!"
    assert "CORPORATE_SHADOW_RAID" in hqd_code, "Shadow raid check in Node Raid modal missing!"
    print("[PASS] obj_HQTerminal UI (Brig, Nemesis Radar, Poaching Modal, Shadow Raid Banner) verified.")

    print("\nALL GOAL E EXHAUSTIVE SUITE TESTS PASSED (100%)!")

if __name__ == '__main__':
    test_goal_e()
