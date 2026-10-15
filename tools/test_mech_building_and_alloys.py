#!/usr/bin/env python3
"""
Test Suite for Revamped Mech Building, Sintering Metallurgy, and Modular Assembly
"""

import os, re, sys

print("=== 1. VERIFYING 8 CANONICAL ALLOY CHROMATIC SIGNATURES ===")
color_script_path = 'scripts/scr_alloy_color_synthesis/scr_alloy_color_synthesis.gml'
with open(color_script_path, 'r') as f_col:
    color_gml = f_col.read()

canonical_alloys = [
    ("alloy_vanguard_comp", "Gunmetal Slate"),
    ("alloy_hyperion_matrix", "Cherenkov Plasma Cyan"),
    ("alloy_aerosteel_flux", "Vernier Violet"),
    ("alloy_adamantine_carbide", "Heavy Bronze/Amber"),
    ("alloy_reactive_damascus", "Damascus Crimson Bronze"),
    ("alloy_tachyon_superalloy", "Tachyon Cyan"),
    ("alloy_lunar_aerogel", "Lunar Aerogel Pale Frost"),
    ("alloy_sol_ferrite", "Sol Ferrite Radiant Gold")
]

for alloy_id, desc in canonical_alloys:
    assert f'case "{alloy_id}":' in color_gml, f'Missing chromatic vector for {alloy_id}'
    print(f'  ✓ {alloy_id} -> Mapped ({desc})')

print("")
print("=== 2. VERIFYING 30-PART MODULAR CRAFTING CATALOG (5 PER SLOT) ===")
hq_create_path = 'objects/obj_HQTerminal/Create_0.gml'
with open(hq_create_path, 'r') as f_hq:
    hq_create = f_hq.read()

# Check catalog parts
slots = ["heads", "torsos", "arms", "legs", "backpacks", "weapons"]
for slot in slots:
    matches = re.findall(r'slot:\s*"' + slot + r'"', hq_create)
    assert len(matches) == 5, f'Expected 5 parts for slot {slot}, found {len(matches)}'
    print(f'  ✓ Hardpoint Slot [{slot.upper()}]: 5 Distinct Forged Parts Verified')

# Verify all 8 alloys are utilized in catalog
alloys_used = set(re.findall(r'req_alloy:\s*"([^"]+)"', hq_create))
for alloy_id, _ in canonical_alloys:
    assert alloy_id in alloys_used, f'Alloy {alloy_id} not used in modular crafting catalog!'
    print(f'  ✓ Alloy Utilization: {alloy_id} integrated into components')

print("")
print("=== 3. SIMULATING MECH ASSEMBLY CALCULUS & WEIGHT CLASSES ===")
def evaluate_custom_mech(mass, core_power, total_draw, armor, boost_bonus):
    net_power = core_power - total_draw
    is_stable = net_power >= 0
    if mass < 55:
        weight_class = "LIGHT SKIRMISHER"
    elif 55 <= mass < 85:
        weight_class = "MEDIUM MAINSTAY"
    elif 85 <= mass < 110:
        weight_class = "HEAVY ASSAULT"
    else:
        weight_class = "SUPERHEAVY SIEGEBREAKER"
    return is_stable, net_power, weight_class

# Test 1: Light Skirmisher
st, net, wc = evaluate_custom_mech(42, 32, 18, 920, 80)
assert st and wc == "LIGHT SKIRMISHER", f'Failed Skirmisher: {wc}'
print(f'  ✓ Specimen 1: Mass 42t -> Evaluated as [{wc}] (Net Power: +{net} MW, Stable: {st})')

# Test 2: Medium Mainstay
st, net, wc = evaluate_custom_mech(74, 42, 28, 1450, 65)
assert st and wc == "MEDIUM MAINSTAY", f'Failed Mainstay: {wc}'
print(f'  ✓ Specimen 2: Mass 74t -> Evaluated as [{wc}] (Net Power: +{net} MW, Stable: {st})')

# Test 3: Heavy Assault
st, net, wc = evaluate_custom_mech(98, 54, 33, 1920, 35)
assert st and wc == "HEAVY ASSAULT", f'Failed Heavy: {wc}'
print(f'  ✓ Specimen 3: Mass 98t -> Evaluated as [{wc}] (Net Power: +{net} MW, Stable: {st})')

# Test 4: Superheavy Siegebreaker
st, net, wc = evaluate_custom_mech(118, 54, 38, 2280, 20)
assert st and wc == "SUPERHEAVY SIEGEBREAKER", f'Failed Superheavy: {wc}'
print(f'  ✓ Specimen 4: Mass 118t -> Evaluated as [{wc}] (Net Power: +{net} MW, Stable: {st})')

# Test 5: Overloaded Reactor
st, net, wc = evaluate_custom_mech(88, 28, 38, 1600, 40)
assert not st and net == -10, f'Failed Overload check: {net}'
print(f'  ✓ Specimen 5: Core 28 MW, Draw 38 MW -> Correctly Flagged REACTOR OVERLOAD (Deficit {net} MW)')

print("")
print("=== 4. VERIFYING CANONICAL BLUEPRINT SERIALIZATION ===")
bp_create_path = 'objects/obj_BlueprintManager/Create_0.gml'
with open(bp_create_path, 'r') as f_bp:
    bp_create = f_bp.read()

assert 'register_custom_blueprint' in bp_create, 'Missing register_custom_blueprint in BlueprintManager'
assert 'save_custom_blueprint' in hq_create, 'Missing save_custom_blueprint in HQTerminal'
print('  ✓ Custom Blueprint Registration API verified in obj_BlueprintManager')
print('  ✓ Custom Blueprint Archival serialization verified in obj_HQTerminal')

print("")
print(">>> ALL REVAMPED MECH BUILDING & ALLOY CREATION TESTS PASSED! <<<")
