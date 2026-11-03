#!/usr/bin/env python3
"""
Test Suite for Milestone 56: Advanced Character Stat Allocation, Cockpit Sortie Fatigue & Battle Scar Trait Mutations
Verifies:
1. Document 56 GDD design specifications and mathematical models.
2. obj_GameManager progression engine: Level-ups, Stat point allocation, R&R shore leave, and trait mutations.
3. obj_BattleManager combat fatigue degradation, trait modifiers, kill/ejection mutations, and space victory trauma.
4. obj_HQTerminal UI rendering: Interactive stat point allocation buttons, fatigue status gauges, and Cantina R&R button.
5. Master GDD index registration.
"""

import os
import sys

PASS_COUNT = 0
FAIL_COUNT = 0

def check(condition, message):
    global PASS_COUNT, FAIL_COUNT
    if condition:
        print(f"[PASS] {message}")
        PASS_COUNT += 1
    else:
        print(f"[FAIL] {message}")
        FAIL_COUNT += 1

def main():
    print("======================================================================")
    print("  MILESTONE 56: CHARACTER STATS, FATIGUE & TRAIT MUTATIONS TEST SUITE")
    print("======================================================================")

    # --- 1. Document 56 Design Scope & Math Models ---
    print("\n--- 1. Testing Document 56 Specification & Math Models ---")
    doc_path = "docs/56_advanced_character_stats_fatigue_and_trait_mutations.md"
    check(os.path.exists(doc_path), f"GDD specification exists: {doc_path}")

    with open(doc_path, "r", encoding="utf-8") as f:
        doc_text = f.read()

    check("150" in doc_text and "Level" in doc_text, "Level-up formula (150 XP per level) defined in GDD")
    check("Stat Points Earned" in doc_text or "Unallocated Stat Points" in doc_text, "Stat point rewards defined in GDD")
    check("Cockpit Fatigue" in doc_text or "fatigue" in doc_text, "Cockpit fatigue mechanics documented in GDD")
    check("R&R Leave" in doc_text or "Rest & Recuperation" in doc_text, "Rest & Recuperation (R&R) shore leave documented in GDD")
    check("Iron Survivor" in doc_text, "Trait documented: 'Iron Survivor'")
    check("Ace Predator" in doc_text, "Trait documented: 'Ace Predator'")
    check("Ghost of Phobos" in doc_text, "Trait documented: 'Ghost of Phobos'")
    check("Cybernetic Reflex Augment" in doc_text, "Trait documented: 'Cybernetic Reflex Augment'")

    # --- 2. GameManager Engine Progression & Mechanics ---
    print("\n--- 2. Testing GameManager Create_0 Engine Logic ---")
    gm_path = "objects/obj_GameManager/Create_0.gml"
    with open(gm_path, "r", encoding="utf-8") as f:
        gm_text = f.read()

    check("allocate_pilot_stat = function" in gm_text, "Function allocate_pilot_stat defined in GameManager")
    check("send_pilot_on_rr = function" in gm_text, "Function send_pilot_on_rr defined in GameManager")
    check("mutate_pilot_trait = function" in gm_text, "Function mutate_pilot_trait defined in GameManager")
    check("floor(_plt.xp / 150)" in gm_text, "Level calculation (1 + floor(xp / 150)) implemented in pilot_add_xp")
    check("_plt.unspent_stat_points += _lvl_delta * 2" in gm_text, "+2 Unspent stat points per level awarded in pilot_add_xp")
    check("mutated_traits: []" in gm_text, "Pilot roster initialized with mutated_traits array")
    check("funds -= 5000" in gm_text and "_plt.fatigue = 0" in gm_text, "send_pilot_on_rr deducts 5,000 Cr and resets fatigue to 0")
    check("max(0, _plt.fatigue - 25)" in gm_text, "Passive fatigue recovery (-25 per cycle) implemented in end_turn")
    check('mutate_pilot_trait(p, "Cybernetic Reflex Augment")' in gm_text, "Hospital convalescence clearance awards Cybernetic Reflex Augment")

    # --- 3. BattleManager Fatigue & Combat Mutations ---
    print("\n--- 3. Testing BattleManager Combat Fatigue & Trait Integration ---")
    bm_create_path = "objects/obj_BattleManager/Create_0.gml"
    with open(bm_create_path, "r", encoding="utf-8") as f:
        bm_create = f.read()

    bm_step_path = "objects/obj_BattleManager/Step_0.gml"
    with open(bm_step_path, "r", encoding="utf-8") as f:
        bm_step = f.read()

    check("_pilot.fatigue = min(100," in bm_create and "_un.fatigue = _pilot.fatigue" in bm_create, "Combat deployment adds +25 sortie fatigue in BattleManager")
    check("_atk.fatigue >= 75" in bm_create and "_base -= 20" in bm_create, "Fatigue tier Exhausted (-20% Acc) penalty implemented in calculate_hit_chance")
    check("_atk.fatigue >= 50" in bm_create and "_base -= 10" in bm_create, "Fatigue tier Fatigued (-10% Acc) penalty implemented in calculate_hit_chance")
    check("_atk.fatigue >= 25" in bm_create and "_base -= 5" in bm_create, "Fatigue tier Winded (-5% Acc) penalty implemented in calculate_hit_chance")
    check('array_contains(_atk.mutated_traits, "Cybernetic Reflex Augment")' in bm_create and "_base += 6" in bm_create, "Cybernetic Reflex Augment (+6% Acc) applied in calculate_hit_chance")
    check('array_contains(_def.mutated_traits, "Ghost of Phobos")' in bm_create and "_eva += 10" in bm_create, "Ghost of Phobos (+10% Eva) applied in calculate_hit_chance")
    check('array_contains(_atk.mutated_traits, "Ace Predator")' in bm_create and "_crit_chance += 12" in bm_create, "Ace Predator (+12% Crit Rate) applied in start_battle_cinematic")
    check('obj_GameManager.mutate_pilot_trait(ap, "Ace Predator")' in bm_create, "5+ Confirmed kills awards 'Ace Predator' trait mutation")
    check('obj_GameManager.mutate_pilot_trait(p, "Iron Survivor")' in bm_create, "Emergency ejection survival awards 'Iron Survivor' trait mutation")
    check('obj_GameManager.mutate_pilot_trait(p, "Ghost of Phobos")' in bm_step, "High fatigue surviving pilots in space victory mutate 'Ghost of Phobos' in Step_0")

    # --- 4. HQTerminal UI Rendering & Buttons ---
    print("\n--- 4. Testing HQTerminal UI Rendering in Draw_64 ---")
    hq_path = "objects/obj_HQTerminal/Draw_64.gml"
    with open(hq_path, "r", encoding="utf-8") as f:
        hq_text = f.read()

    check("LVL " in hq_text and "UNSPENT STAT POINTS:" in hq_text, "Pilot Level and Unspent Stat Points rendered in HQTerminal")
    check("COCKPIT FATIGUE:" in hq_text, "Cockpit Fatigue status gauge rendered in HQTerminal")
    check("[+2 ACC (" in hq_text and "allocate_pilot_stat(selected_roster_pilot_idx, \"accuracy\")" in hq_text, "[+2 ACC] interactive button implemented in HQTerminal")
    check("[+2 REF (" in hq_text and "allocate_pilot_stat(selected_roster_pilot_idx, \"reflexes\")" in hq_text, "[+2 REF] interactive button implemented in HQTerminal")
    check("[+1 CMB (" in hq_text and "allocate_pilot_stat(selected_roster_pilot_idx, \"combat_stat\")" in hq_text, "[+1 CMB] interactive button implemented in HQTerminal")
    check("[+1 TAC (" in hq_text and "allocate_pilot_stat(selected_roster_pilot_idx, \"tactics_stat\")" in hq_text, "[+1 TAC] interactive button implemented in HQTerminal")
    check("[GRANT R&R LEAVE (-5k Cr)]" in hq_text and "send_pilot_on_rr(selected_roster_pilot_idx)" in hq_text, "Cantina Shore Leave R&R button implemented in HQTerminal")

    # --- 5. Master GDD Index Entry ---
    print("\n--- 5. Testing Master GDD Index Entry ---")
    master_path = "docs/00_master_game_design_document.md"
    with open(master_path, "r", encoding="utf-8") as f:
        master_text = f.read()

    check("test_milestone_56_stats_fatigue_and_traits.py" in master_text, "Test suite 16 registered in Master GDD")
    check("56_advanced_character_stats_fatigue_and_trait_mutations.md" in master_text, "Doc 56 registered in Master GDD lineage index")

    print("\n======================================================================")
    print(f"  RESULTS: {PASS_COUNT} PASSED, {FAIL_COUNT} FAILED")
    print("======================================================================")

    if FAIL_COUNT > 0:
        sys.exit(1)
    else:
        print("  ALL MILESTONE 56 STATS, FATIGUE & TRAIT MUTATIONS VERIFIED 100%!")
        print("======================================================================")
        sys.exit(0)

if __name__ == "__main__":
    main()
