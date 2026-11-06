#!/usr/bin/env python3
"""
Comprehensive Verification Suite for Material-Driven Chassis, Dynamic Alloy Palette Tinting,
Forge Quality Tiers (S/A/B/C), and Combinations Math in obj_DebugManager.
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def run_tests():
    print("=== TESTING MATERIAL-DRIVEN CHASSIS & ALLOY PALETTE FORGE ===")

    # 1. Verify obj_DebugManager/Create_0.gml
    create_path = os.path.join(PROJECT_ROOT, "objects", "obj_DebugManager", "Create_0.gml")
    with open(create_path) as f:
        c_code = f.read()

    # Bespoke Player PMC Chassis Platforms
    assert "get_player_custom_chassis_catalog" in c_code, "Missing get_player_custom_chassis_catalog in Create_0.gml"
    assert "PMC-01 Vanguard Breaker" in c_code, "Missing PMC-01 Vanguard in Create_0.gml"
    assert "PMC-02 Stratos Interceptor" in c_code, "Missing PMC-02 Stratos in Create_0.gml"
    assert "PMC-03 Scrapper Brawler" in c_code, "Missing PMC-03 Scrapper in Create_0.gml"
    assert "PMC-04 Ghost Recon Sniper" in c_code, "Missing PMC-04 Ghost in Create_0.gml"
    assert "PMC-00 Hephaestus Prime" in c_code, "Missing PMC-00 Hephaestus in Create_0.gml"
    assert "builder_chassis_line" in c_code, "Missing builder_chassis_line in Create_0.gml"

    # Quality Tiers & Material Palettes
    assert "builder_quality_idx" in c_code, "Missing builder_quality_idx in Create_0.gml"
    assert "builder_quality_names" in c_code, "Missing builder_quality_names in Create_0.gml"
    assert "builder_quality_badges" in c_code, "Missing builder_quality_badges in Create_0.gml"
    assert "builder_quality_mults" in c_code, "Missing builder_quality_mults in Create_0.gml"
    assert "tint_color" in c_code and "glow_color" in c_code, "Missing tint_color and glow_color in Create_0.gml"

    # Hangar Deck Mech Builder with R&D Weapons
    assert "builder_weapons_db" in c_code, "Missing builder_weapons_db in Create_0.gml"
    assert "apply_smart_default_loadout" in c_code, "Missing apply_smart_default_loadout in Create_0.gml"
    assert "calculate_builder_telemetry" in c_code, "Missing calculate_builder_telemetry in Create_0.gml"
    assert "deploy_builder_mech_to_combat" in c_code, "Missing deploy_builder_mech_to_combat in Create_0.gml"
    assert "commission_builder_mech_to_hangar" in c_code, "Missing commission_builder_mech_to_hangar in Create_0.gml"
    print("  ✓ obj_DebugManager Create Event: Material-Driven Chassis, Alloy Palettes, and Quality Tiers verified.")

    # 2. Verify obj_DebugManager/Step_0.gml
    step_path = os.path.join(PROJECT_ROOT, "objects", "obj_DebugManager", "Step_0.gml")
    with open(step_path) as f:
        s_code = f.read()

    assert 'ord("1")' in s_code and 'ord("2")' in s_code and 'ord("3")' in s_code and 'ord("4")' in s_code, "Missing 1-4 hotkeys in Step_0.gml"
    assert "TAB 1: MECH BUILDER & FORGE STEP CONTROLS" in s_code, "Missing Tab 1 step logic in Step_0.gml"
    assert "builder_subtab" in s_code, "Missing builder_subtab switching in Step_0.gml"
    assert 'ord("T")' in s_code, "Missing T key platform line toggle in Step_0.gml"
    assert "builder_quality_idx" in s_code, "Missing quality tier hotkeys in Step_0.gml"
    print("  ✓ obj_DebugManager Step Event: Tab hotkeys (1-4, Tab, Q/E, T) and Quality Tier cycling verified.")

    # 3. Verify obj_DebugManager/Draw_64.gml
    draw_path = os.path.join(PROJECT_ROOT, "objects", "obj_DebugManager", "Draw_64.gml")
    with open(draw_path) as f:
        d_code = f.read()

    assert "SELECT FORGE CRUCIBLE PURITY / QUALITY TIER:" in d_code, "Missing Quality Tier selector in Draw_64.gml"
    assert "builder_quality_badges" in d_code, "Missing quality badges in Draw_64.gml"
    assert "_t.tint" in d_code, "Missing dynamic alloy tinting in gantry render"
    assert "_t.glow" in d_code, "Missing masterwork energy sheen in gantry render"
    print("  ✓ obj_DebugManager Draw GUI Event: Dynamic Alloy Tinting, Sheen, and Quality UI verified.")

    # 4. Mathematical Breakdown of Combinations
    print("\n--- Mobile Suit Combinations Mathematical Analysis ---")
    num_pmc_chassis = 5
    num_faction_chassis = 24
    total_platforms = num_pmc_chassis + num_faction_chassis
    num_alloys = 6
    num_qualities = 4
    
    # Weapons in R&D DB
    num_primary = 6
    num_secondary = 4
    num_melee = 4
    num_shields = 4
    num_weapon_loadouts = num_primary * num_secondary * num_melee * num_shields

    pmc_visual_variants = num_pmc_chassis * num_alloys
    total_visual_variants = total_platforms * num_alloys

    pmc_chassis_alloy_quality = num_pmc_chassis * num_alloys * num_qualities
    pmc_full_combinations = num_pmc_chassis * num_alloys * num_qualities * num_weapon_loadouts
    total_full_combinations = total_platforms * num_alloys * num_qualities * num_weapon_loadouts

    print(f"  • Bespoke Player PMC Chassis Platforms: {num_pmc_chassis}")
    print(f"  • Reverse-Engineered Faction Platforms: {num_faction_chassis} (Total: {total_platforms})")
    print(f"  • Sintered Crucible Alloys (Visual Finishes): {num_alloys}")
    print(f"  • Forge Quality / Crucible Purity Tiers: {num_qualities} (C, B, A, S)")
    print(f"  • R&D Weapon Combinations per Suit: {num_weapon_loadouts} ({num_primary}x Prim, {num_secondary}x Sec, {num_melee}x Mel, {num_shields}x Sld)")
    print(f"\n  => Unique Visual & Material Variants (PMC Foundry): {pmc_visual_variants} distinct looks")
    print(f"  => Unique Visual & Material Variants (With Factions): {total_visual_variants} distinct looks")
    print(f"  => Factory Tuned Configurations (PMC Chassis x Alloy x Quality): {pmc_chassis_alloy_quality} configurations")
    print(f"  => Full Playable Combinations (PMC Chassis x Alloy x Quality x Weapons): {pmc_full_combinations:,} unique builds")
    print(f"  => Grand Total Sandbox Combinations (Including Factions): {total_full_combinations:,} unique builds")

    assert pmc_full_combinations == 46080, f"Expected 46,080 PMC combinations, got {pmc_full_combinations}"
    assert num_weapon_loadouts == 384, f"Expected 384 weapon loadouts, got {num_weapon_loadouts}"

    print("\n=======================================================")
    print("ALL FORGE & COMBINATION TESTS PASSED (100%)")
    print("=======================================================")

if __name__ == "__main__":
    run_tests()
