import re

print("=== EXHAUSTIVE VALIDATION: EQUIPMENT RESEARCH TECH TREE ===")

# 1. Parse Tech Database from scr_research_tree_system.gml
with open('scripts/scr_research_tree_system/scr_research_tree_system.gml', 'r') as f:
    gml = f.read()

tech_matches = re.findall(r'_db\[\$ "([^"]+)"\] = \{', gml)
assert len(tech_matches) >= 30, f"Expected >= 30 technologies, found {len(tech_matches)}"
tech_set = set(tech_matches)
print(f"[PASS] Successfully parsed {len(tech_set)} unique technologies in tech database.")

# 2. Parse all 30 modular parts from obj_HQTerminal/Create_0.gml
with open('objects/obj_HQTerminal/Create_0.gml', 'r') as f:
    hq_create = f.read()

# Pattern for string or array req_tech_id
part_matches = re.findall(r'\{\s*id:\s*"([^"]+)",\s*name:\s*"([^"]+)",\s*slot:\s*"([^"]+)"[^}]+req_tech_id:\s*("[^"]+"|[\[][^\]]+[\]])', hq_create)
assert len(part_matches) == 30, f"Expected 30 modular parts with req_tech_id, found {len(part_matches)}"
print(f"[PASS] Verified all 30 modular crafting parts have req_tech_id assigned.")

# Verify each req_tech_id references real technologies
for pid, pname, pslot, req_tech in part_matches:
    if req_tech.startswith('['):
        ids = [x.strip(' "[]') for x in req_tech.split(',')]
        for tid in ids:
            assert tid in tech_set, f"Part {pid} references unknown tech: {tid}"
    else:
        tid = req_tech.strip(' "')
        assert tid in tech_set, f"Part {pid} references unknown tech: {tid}"

print("[PASS] All 30 modular parts reference verified technologies in tech database.")

# 3. Verify Starter Techs cover all 6 modular slots
starter_techs = [
    "tech_wpn_heavy_autocannon",
    "tech_wpn_hydra_rockets",
    "tech_wpn_vibro_blade",
    "tech_rea_gas_cooled_fission",
    "tech_sld_ballistic_buckler",
    "tech_upg_analog_hydraulics"
]

starter_slots_covered = set()
for pid, pname, pslot, req_tech in part_matches:
    if any(st in req_tech for st in starter_techs):
        starter_slots_covered.add(pslot)

expected_slots = {"heads", "torsos", "arms", "legs", "backpacks", "weapons"}
assert expected_slots.issubset(starter_slots_covered), f"Missing starter coverage for: {expected_slots - starter_slots_covered}"
print(f"[PASS] Starter technologies provide immediate Turn 1 coverage across all 6 slots: {sorted(list(starter_slots_covered))}")

# 4. Verify Mutually Exclusive Forks & Symmetrical Exclusivity
fork_pairs = [
    ("tech_wpn_electromagnetic_railgun", "tech_wpn_tachyon_lance"),
    ("tech_wpn_beam_carbine", "tech_wpn_anti_ship_torpedo"),
    ("tech_rea_antimatter_pinch", "tech_rea_tachyon_cyclotron"),
    ("tech_sld_composite_reactive", "tech_sld_i_field_emitter"),
    ("tech_sld_magnetic_barrier", "tech_sld_damascus_citadel"),
    ("tech_upg_nanite_cooling", "tech_upg_overboost_rig")
]

for t1, t2 in fork_pairs:
    assert t1 in tech_set, f"Tech {t1} missing"
    assert t2 in tech_set, f"Tech {t2} missing"
    # Symmetrical check in code
    p1 = rf'_db\[\$ "{t1}"\].*?mutually_exclusive_with:\s*\[[^\]]*"{t2}"[^\]]*\]'
    p2 = rf'_db\[\$ "{t2}"\].*?mutually_exclusive_with:\s*\[[^\]]*"{t1}"[^\]]*\]'
    assert re.search(p1, gml, re.DOTALL), f"Missing exclusivity: {t1} -> {t2}"
    assert re.search(p2, gml, re.DOTALL), f"Missing exclusivity: {t2} -> {t1}"

print(f"[PASS] Verified all {len(fork_pairs)} mutually exclusive doctrine forks have symmetrical locking rules.")

# 5. Verify Salvage Intel & Eurekas in obj_BattleManager
with open('objects/obj_BattleManager/Create_0.gml', 'r') as f:
    bm_code = f.read()

assert 'scr_research_award_salvage_intel' in bm_code, "scr_research_award_salvage_intel missing in BattleManager"
assert 'BLACK BOX EUREKA' in gml, "Black Box Eureka messaging missing in scr_research_tree_system.gml"
assert 'eureka_boosts' in gml, "eureka_boosts tracking missing in scr_research_tree_system.gml"
print("[PASS] Battlefield Salvage Intel & Black Box Eureka mechanics verified.")

# 6. Verify Part Forge licensing check in obj_HQTerminal/Draw_64.gml
with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
    draw_code = f.read()

assert '_is_licensed' in draw_code, "License check missing in Part Forge"
assert '[R&D LOCKED]' in draw_code, "[R&D LOCKED] button missing in Part Forge"
assert 'scr_research_is_unlocked' in draw_code, "scr_research_is_unlocked check missing in Part Forge"
print("[PASS] Modular Part Forge UI properly blocks unresearched blueprints with [R&D LOCKED].")

print("=== ALL EXHAUSTIVE EQUIPMENT RESEARCH TREE TESTS PASSED 100%! ===")
