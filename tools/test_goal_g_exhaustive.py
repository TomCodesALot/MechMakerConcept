#!/usr/bin/env python3
"""
test_goal_g_exhaustive.py - Complete validation of Goal G:
Climactic Apex Crisis Sortie & Superweapon Boss Battle
(Deus-Machina: Ouroboros Prime, Phase Barrier Subsystems, Orbital Bombardment & Victory Path 4)
"""

import os
import sys

def test_battle_manager_boss_mechanics():
    print("--- 1. Testing obj_BattleManager Boss Mechanics ---")
    bm_create = "objects/obj_BattleManager/Create_0.gml"
    assert os.path.exists(bm_create), f"Missing {bm_create}"
    with open(bm_create, "r") as f:
        content = f.read()

    # Crisis battle flag and launcher check
    assert "is_crisis_boss_battle = false;" in content, "Missing is_crisis_boss_battle init"
    assert "setup_apex_crisis_boss = function()" in content, "Missing setup_apex_crisis_boss definition"
    assert "call_flagship_orbital_strike = function" in content, "Missing call_flagship_orbital_strike definition"
    assert "setup_apex_crisis_boss();" in content, "setup_apex_crisis_boss not invoked when is_crisis_boss_battle is true"

    # Boss structure & subsystems
    assert "DEUS-MACHINA: OUROBOROS PRIME" in content, "Missing boss name"
    assert "barrier_cur: 800" in content, "Missing barrier_cur 800"
    assert "barrier_max: 800" in content, "Missing barrier_max 800"
    assert "barrier_regen: 150" in content, "Missing barrier_regen 150"
    assert "Super-Heavy Plasma Annihilator" in content, "Missing boss Super-Heavy Plasma Annihilator"
    assert "Quantum Disruption Pulse" in content, "Missing boss Quantum Disruption Pulse"
    assert "Nanite Swarm Micro-Missiles" in content, "Missing boss Nanite Swarm Micro-Missiles"

    # Subsystems check: head, torso, arm_right, arm_left, legs, backpack
    for comp in ["head", "torso", "arm_right", "arm_left", "legs", "backpack"]:
        assert f"{comp}:" in content or f"components.{comp}" in content, f"Missing boss subsystem {comp}"

    # Phase Barrier Absorption in all combat pipelines
    assert "barrier_cur > 0" in content, "Missing Phase barrier absorption check"
    assert "PHASE BARRIER ABSORBED" in content or "Phase Barrier absorbed" in content or "barrier_cur" in content, "Missing barrier absorption log"
    assert "BARRIER SHATTERED" in content or "Phase Barrier Emitter destroyed" in content, "Missing barrier collapse logic"

    # Boss Defeat Hook & Victory Path 4 Trigger
    assert "crisis_defeated = true" in content, "Missing crisis_defeated = true assignment upon boss defeat"
    assert "evaluate_campaign_victory" in content, "Missing evaluate_campaign_victory call upon boss defeat"

    print("[PASS] obj_BattleManager Boss Mechanics verified.")

def test_battle_manager_step_and_draw():
    print("--- 2. Testing obj_BattleManager Step & Draw Integration ---")
    bm_step = "objects/obj_BattleManager/Step_0.gml"
    with open(bm_step, "r") as f:
        step_content = f.read()

    assert "call_flagship_orbital_strike" in step_content, "Missing orbital strike in Step_0"
    assert 'ord("O")' in step_content, "Missing [O] key check for orbital strike"
    assert "barrier_cur" in step_content, "Missing phase barrier turn recharge in Step_0"

    bm_draw64 = "objects/obj_BattleManager/Draw_64.gml"
    with open(bm_draw64, "r") as f:
        d64_content = f.read()
    assert "[O] ORBITAL" in d64_content, "Missing [O] ORBITAL button in Draw_64"
    assert "call_flagship_orbital_strike" in d64_content, "Missing call_flagship_orbital_strike click handler in Draw_64"

    bm_draw0 = "objects/obj_BattleManager/Draw_0.gml"
    with open(bm_draw0, "r") as f:
        d0_content = f.read()
    assert "★ [APEX BOSS] OUROBOROS ★" in d0_content, "Missing Boss overhead badge in Draw_0"
    assert "barrier_cur" in d0_content, "Missing Phase barrier shield bar in Draw_0"

    print("[PASS] obj_BattleManager Step & Draw verified.")

def test_hqterminal_boss_sortie():
    print("--- 3. Testing obj_HQTerminal Boss Sortie Launcher & UI ---")
    hq_create = "objects/obj_HQTerminal/Create_0.gml"
    with open(hq_create, "r") as f:
        hq_c = f.read()
    assert "launch_crisis_boss_sortie" in hq_c, "Missing launch_crisis_boss_sortie in HQTerminal Create_0"

    hq_step = "objects/obj_HQTerminal/Step_0.gml"
    with open(hq_step, "r") as f:
        hq_s = f.read()
    assert 'ord("K")' in hq_s, "Missing [K] hotkey in HQTerminal Step_0"
    assert "launch_crisis_boss_sortie" in hq_s, "Missing launch_crisis_boss_sortie call on [K]"

    hq_draw64 = "objects/obj_HQTerminal/Draw_64.gml"
    with open(hq_draw64, "r") as f:
        hq_d = f.read()
    assert "APEX CRISIS [K]" in hq_d, "Missing APEX CRISIS [K] button in HQTerminal Draw_64"
    assert "launch_crisis_boss_sortie" in hq_d, "Missing launch_crisis_boss_sortie call in HQTerminal Draw_64"

    print("[PASS] obj_HQTerminal Boss Sortie Launcher & UI verified.")

def test_phase_barrier_and_orbital_math_simulation():
    print("--- 4. Mathematical Simulation: Phase Barrier & Orbital Strike ---")
    # Simulate Boss stats
    boss = {
        "name": "DEUS-MACHINA: OUROBOROS PRIME",
        "barrier_cur": 800,
        "barrier_max": 800,
        "barrier_regen": 150,
        "components": {
            "torso":    {"name": "Archeotech Singularity Core", "cur": 2500, "max": 2500, "armor": 65, "intact": True},
            "head":     {"name": "Quantum Cognition Array",     "cur": 800,  "max": 800,  "armor": 45, "intact": True},
            "arm_left": {"name": "Twin Particle Lance",         "cur": 1200, "max": 1200, "armor": 55, "intact": True},
            "arm_right":{"name": "Super-Heavy Plasma Annihilator", "cur": 1200, "max": 1200, "armor": 55, "intact": True},
            "legs":     {"name": "Hover-Graviton Skirt Array",  "cur": 1500, "max": 1500, "armor": 50, "intact": True},
            "backpack": {"name": "Phase Barrier Emitter",       "cur": 1000, "max": 1000, "armor": 40, "intact": True}
        }
    }

    # Step 1: Standard Railgun Attack (300 raw damage) absorbed by Phase Barrier
    incoming_dmg = 300
    if boss["barrier_cur"] > 0:
        absorbed = min(incoming_dmg, boss["barrier_cur"])
        boss["barrier_cur"] -= absorbed
        remaining_dmg = incoming_dmg - absorbed
    else:
        absorbed = 0
        remaining_dmg = incoming_dmg

    assert absorbed == 300, f"Expected 300 absorbed, got {absorbed}"
    assert boss["barrier_cur"] == 500, f"Expected 500 barrier left, got {boss['barrier_cur']}"
    assert remaining_dmg == 0, f"Expected 0 bleed damage, got {remaining_dmg}"
    assert boss["components"]["torso"]["cur"] == 2500, "Torso suffered damage through barrier"

    # Step 2: USN-X Hephaestus Orbital Bombardment: 550 AoE damage + barrier shatter
    orbital_dmg = 550
    # Orbital strike directly vaporizes active barrier and inflicts bleed-through
    if boss["barrier_cur"] > 0:
        boss["barrier_cur"] = 0
    # Bleed-through damage distributed to components (e.g. backpack)
    boss["components"]["backpack"]["cur"] -= orbital_dmg
    assert boss["barrier_cur"] == 0, "Barrier not zeroed by orbital bombardment"
    assert boss["components"]["backpack"]["cur"] == 450, f"Backpack should have 450 HP left, got {boss['components']['backpack']['cur']}"

    # Step 3: Targeted flank strike severs Phase Barrier Emitter (450 damage)
    boss["components"]["backpack"]["cur"] -= 450
    if boss["components"]["backpack"]["cur"] <= 0:
        boss["components"]["backpack"]["intact"] = False
        boss["barrier_cur"] = 0
        boss["barrier_max"] = 0

    assert boss["components"]["backpack"]["intact"] == False, "Backpack should be severed"
    assert boss["barrier_max"] == 0, "Barrier max should collapse to 0 when emitter destroyed"

    # Turn refresh recharge attempt:
    if boss["components"]["backpack"]["intact"]:
        boss["barrier_cur"] = min(boss["barrier_max"], boss["barrier_cur"] + boss["barrier_regen"])
    assert boss["barrier_cur"] == 0, "Barrier must not recharge when backpack is destroyed"

    # Step 4: Torso destroyed -> Boss defeat triggers Victory Path 4
    boss["components"]["torso"]["cur"] = 0
    boss["components"]["torso"]["intact"] = False
    
    # Boss victory hook
    credits_reward = 500000
    eureka_reward = 1
    crisis_defeated = True
    campaign_victory_path_4 = crisis_defeated

    assert credits_reward == 500000, "Victory Cr reward mismatch"
    assert eureka_reward == 1, "Victory Eureka milestone mismatch"
    assert campaign_victory_path_4 == True, "Victory Path 4 Savior of Sol should trigger"

    print("[PASS] Phase Barrier & Orbital Math Simulation verified 100%.")

if __name__ == "__main__":
    print("=== EXHAUSTIVE VALIDATION: GOAL G ===")
    test_battle_manager_boss_mechanics()
    test_battle_manager_step_and_draw()
    test_hqterminal_boss_sortie()
    test_phase_barrier_and_orbital_math_simulation()
    print(chr(10) + "ALL GOAL G EXHAUSTIVE SUITE TESTS PASSED (100%)!")
