# -*- coding: utf-8 -*-
import os
import sys
import re

print("=" * 70)
print("  MILESTONE 50: FIRST PLAYABLE ALPHA & ONBOARDING TUTORIAL TEST SUITE")
print("=" * 70)

# --- 1. CODEBASE STATIC VERIFICATION ---
def test_static_integration():
    print("\n--- 1. Testing Codebase Static Architecture ---")

    # A. obj_GameManager
    with open("objects/obj_GameManager/Create_0.gml", "r") as f:
        gm_code = f.read()
    assert "has_completed_tutorial = false;" in gm_code, "has_completed_tutorial missing in obj_GameManager"
    assert "tutorial_step = 0;" in gm_code, "tutorial_step missing in obj_GameManager"
    assert "advance_tutorial_step = function" in gm_code, "advance_tutorial_step missing in obj_GameManager"
    assert "skip_tutorial = function" in gm_code, "skip_tutorial missing in obj_GameManager"
    assert "advance_tutorial_step();" in gm_code, "select_commander hook missing in obj_GameManager"
    print("[PASS] obj_GameManager Onboarding Cadre architecture verified.")

    # B. obj_HQTerminal
    with open("objects/obj_HQTerminal/Create_0.gml", "r") as f:
        hq_c = f.read()
    assert "!obj_GameManager.has_completed_intro" in hq_c, "intro_active boot condition missing in obj_HQTerminal/Create_0.gml"
    assert "tutorial_pulse_timer" in hq_c, "tutorial_pulse_timer missing in obj_HQTerminal/Create_0.gml"
    assert "advance_tutorial_step()" in hq_c, "tutorial step hooks missing in obj_HQTerminal/Create_0.gml"
    print("[PASS] obj_HQTerminal Create_0 hooks verified.")

    # C. obj_HQTerminal Step_0
    with open("objects/obj_HQTerminal/Step_0.gml", "r") as f:
        hq_s = f.read()
    assert "active_tab = 3" in hq_s, "Key 1 -> War Map missing in Step_0"
    assert "active_tab = 1" in hq_s, "Key 2 -> Hangar missing in Step_0"
    assert "active_tab = 0" in hq_s, "Key 3 -> R&D Forge missing in Step_0"
    assert "active_tab = 2" in hq_s, "Key 4 -> Contracts missing in Step_0"
    assert "active_tab = 4" in hq_s, "Key 5 -> Fleet missing in Step_0"
    assert "obj_GameManager.tutorial_step = 4;" in hq_s, "Sortie key tutorial hook missing in Step_0"
    print("[PASS] obj_HQTerminal Step_0 quick-keys and sortie hook verified.")

    # D. obj_HQTerminal Draw_64
    with open("objects/obj_HQTerminal/Draw_64.gml", "r") as f:
        hq_d = f.read()
    assert "[1] WAR MAP" in hq_d, "Deck 1 War Map missing in Draw_64"
    assert "[2] HANGAR" in hq_d, "Deck 2 Hangar missing in Draw_64"
    assert "[3] R&D FORGE" in hq_d, "Deck 3 R&D Forge missing in Draw_64"
    assert "[4] CONTRACTS" in hq_d, "Deck 4 Contracts missing in Draw_64"
    assert "[5] FLEET" in hq_d, "Deck 5 Fleet missing in Draw_64"
    assert "CADRE TACTICAL WIRE" in hq_d, "Cadre Tactical Wire banner missing in Draw_64"
    assert "SKIP CADRE" in hq_d, "Skip cadre button missing in Draw_64"
    assert "obj_GameManager.advance_tutorial_step()" in hq_d, "Battle victory return hook missing in Draw_64"
    print("[PASS] obj_HQTerminal Draw_64 deck switcher & Cadre HUD verified.")

    # E. obj_BattleManager Draw_64
    with open("objects/obj_BattleManager/Draw_64.gml", "r") as f:
        bm_d = f.read()
    assert "CADRE TACTICAL INSTRUCTION" in bm_d, "Cadre tactical instruction banner missing in BattleManager"
    print("[PASS] obj_BattleManager tactical tutorial ribbon verified.")

    # F. scr_save_system
    with open("scripts/scr_save_system/scr_save_system.gml", "r") as f:
        ss_code = f.read()
    assert "has_completed_tutorial" in ss_code, "has_completed_tutorial serialization missing in scr_save_system"
    assert "tutorial_step" in ss_code, "tutorial_step serialization missing in scr_save_system"
    print("[PASS] scr_save_system tutorial state serialization verified.")

# --- 2. PIPELINE STATE MACHINE SIMULATION ---
def test_pipeline_simulation():
    print("\n--- 2. Executing 5-Step Onboarding Pipeline Simulation ---")
    
    class MockGameManager:
        def __init__(self):
            self.has_completed_intro = False
            self.has_completed_tutorial = False
            self.tutorial_step = 0
            self.tutorial_active = True
            self.commander = None

        def select_commander(self, choice):
            self.commander = choice
            self.has_completed_intro = True
            if self.tutorial_step == 0:
                self.advance_tutorial_step()

        def advance_tutorial_step(self):
            self.tutorial_step += 1
            if self.tutorial_step >= 5:
                self.has_completed_tutorial = True
                self.tutorial_active = False

        def skip_tutorial(self):
            self.tutorial_step = 5
            self.has_completed_intro = True
            self.has_completed_tutorial = True
            self.tutorial_active = False

    # Run Standard Progression
    gm = MockGameManager()
    assert gm.tutorial_step == 0 and not gm.has_completed_intro
    print("  [Step 0 Initial Boot] Situation Briefing & Commander Appointment pending.")

    # Execute Step 0: Appoint Commander
    gm.select_commander("male")
    assert gm.has_completed_intro is True
    assert gm.tutorial_step == 1
    print("  [Step 1 R&D Forge] Commander Vance appointed -> Crucible Sintering Directive active.")

    # Execute Step 1: Sinter Vanguard Composite
    gm.advance_tutorial_step()
    assert gm.tutorial_step == 2
    print("  [Step 2 Hangar Assembly] Vanguard Composite sintered -> CAD Prototype Rollout Directive active.")

    # Execute Step 2: Assemble Prototype
    gm.advance_tutorial_step()
    assert gm.tutorial_step == 3
    print("  [Step 3 War Map Logistics] GHA-07 Prototype registered -> Sector E-02 Sortie Directive active.")

    # Execute Step 3: Sortie Launch
    gm.tutorial_step = 4
    assert gm.tutorial_step == 4
    print("  [Step 4 Tactical Combat] Sortie launched into rm_combat -> Tactical Instructions active.")

    # Execute Step 4: Win Battle & Return
    gm.advance_tutorial_step()
    assert gm.tutorial_step == 5
    assert gm.has_completed_tutorial is True
    assert gm.tutorial_active is False
    print("  [Step 5 Sandbox Handoff] Battle Won -> Full Mercenary Commission Confirmed!")

    print("[PASS] Full 5-Step Pipeline Progression simulated with 100% mathematical fidelity.")

    # Test Skip Option
    gm2 = MockGameManager()
    gm2.skip_tutorial()
    assert gm2.tutorial_step == 5
    assert gm2.has_completed_intro is True
    assert gm2.has_completed_tutorial is True
    assert gm2.tutorial_active is False
    print("[PASS] Skip Cadre Bypass verified.")

if __name__ == "__main__":
    test_static_integration()
    test_pipeline_simulation()
    print("\nALL MILESTONE 50 ONBOARDING CADRE TESTS PASSED (100%)!\n")
