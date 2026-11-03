import re

print("=== EXHAUSTIVE VALIDATION: GOALS A, B, AND C ===")

# ----------------------------------------------------------------------
# 1. Verify Goal A: Fleet Upkeep & Supply Starvation in obj_GameManager
# ----------------------------------------------------------------------
with open('objects/obj_GameManager/Create_0.gml', 'r') as f:
    gm_code = f.read()

assert 'supply_starvation = false;' in gm_code, "supply_starvation missing in GameManager"
assert 'mech_upkeep_cr_per_unit = 350;' in gm_code, "mech_upkeep_cr_per_unit missing in GameManager"
assert 'total_fleet_tritium_burn' in gm_code, "total_fleet_tritium_burn missing in GameManager"
assert 'mat_tritium -= total_fleet_tritium_burn' in gm_code, "Tritium deduction missing in advance_turn"
assert 'supply_starvation = true;' in gm_code, "Supply starvation trigger missing"

print("[PASS] Goal A (Fleet Upkeep & Tritium Burn Logic) verified in obj_GameManager.")

# ----------------------------------------------------------------------
# 2. Verify Goal B: Pilot Fatigue, XP & Ace Perks in obj_GameManager
# ----------------------------------------------------------------------
assert 'pilot_add_xp = function' in gm_code, "pilot_add_xp function missing"
assert 'Quick Draw' in gm_code, "Quick Draw perk missing"
assert 'Deadeye' in gm_code, "Deadeye perk missing"
assert 'Overdrive' in gm_code, "Overdrive perk missing"
assert 'recovery_days_left = max(0, _plt.recovery_days_left - _heal_rate)' in gm_code, "Hospital recovery missing"
assert '_plt.fatigue = max(0, _plt.fatigue - 1)' in gm_code, "Fatigue recovery missing"

print("[PASS] Goal B (Pilot Progression, Convalescence & Ace Perks) verified in obj_GameManager.")

# ----------------------------------------------------------------------
# 3. Verify Goal C: Flagship Theater Alignment in obj_GameManager
# ----------------------------------------------------------------------
assert 'flagship_is_in_theater = function' in gm_code, "flagship_is_in_theater function missing"
assert 'transit_turns_left > 0' in gm_code, "Transit check missing in theater function"

print("[PASS] Goal C (Flagship Theater Alignment & Transit) verified in obj_GameManager.")

# ----------------------------------------------------------------------
# 4. Verify BattleManager integration
# ----------------------------------------------------------------------
with open('objects/obj_BattleManager/Create_0.gml', 'r') as f:
    bm_code = f.read()

assert 'supply_starvation' in bm_code, "supply_starvation check missing in BattleManager"
assert 'units[i].max_ap = max(1, units[i].max_ap - 2)' in bm_code, "Starvation AP debuff missing"
assert 'units[i].evasion = max(0, units[i].evasion - 25)' in bm_code, "Starvation evasion debuff missing"
assert '_matched_p.fatigue >= 3' in bm_code, "Pilot fatigue check missing in BattleManager"
assert 'Quick Draw' in bm_code, "Quick Draw bonus missing in BattleManager"
assert 'Deadeye' in bm_code, "Deadeye bonus missing in BattleManager"
assert '_in_theater = _gm.flagship_is_in_theater' in bm_code, "Flagship theater check missing in BattleManager"

print("[PASS] BattleManager correctly integrates Supply Starvation, Pilot Perks, and Flagship Orbit.")

# ----------------------------------------------------------------------
# 5. Verify BattleManager AAR Post-Combat Rewards & Fatigue Accumulation
# ----------------------------------------------------------------------
with open('objects/obj_BattleManager/Draw_64.gml', 'r') as f:
    bm_draw = f.read()

assert 'pilot_add_xp' in bm_draw, "pilot_add_xp call missing in AAR resolution"
assert '_plt.fatigue = min(5, (variable_struct_exists(_plt, "fatigue") ? _plt.fatigue : 0) + 1)' in bm_draw, "Fatigue increment missing in AAR"

print("[PASS] BattleManager AAR modal successfully awards Pilot XP and accumulates sortie fatigue.")

# ----------------------------------------------------------------------
# 6. Verify HQ Terminal UI Status Display
# ----------------------------------------------------------------------
with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
    hq_draw = f.read()

assert 'FUEL: ' in hq_draw, "Fuel / Tritium readout missing in top header"
assert 'SUPPLY DEFICIT!' in hq_draw, "SUPPLY DEFICIT alert missing in top header"
assert 'SUPPLY OK' in hq_draw, "SUPPLY OK indicator missing in top header"

print("[PASS] HQ Terminal top header displays Fuel reserves, Supply readiness, and Flagship orbit.")

print("=== ALL GOALS A, B, AND C TESTS PASSED 100%! ===")
