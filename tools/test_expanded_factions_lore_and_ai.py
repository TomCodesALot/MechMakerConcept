#!/usr/bin/env python3
"""
test_expanded_factions_lore_and_ai.py
Validates full 6-faction roster, biological profiles, and player mothership connection.
"""
import os
import sys
import re
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_file(fp):
    full_path = os.path.join(BASE_DIR, fp)
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    no_strings = re.sub(r'"(?:\\.|[^"\\])*"', '""', content)
    no_comments = re.sub(r"//.*", "", no_strings)
    no_block = re.sub(r"/\*.*?\*/", "", no_comments, flags=re.DOTALL)
    counts = {
        "{": no_block.count("{"),
        "}": no_block.count("}"),
        "(": no_block.count("("),
        ")": no_block.count(")"),
        "[": no_block.count("["),
        "]": no_block.count("]")
    }
    curlies = counts["{"] - counts["}"]
    parens = counts["("] - counts[")"]
    brackets = counts["["] - counts["]"]
    assert curlies == 0, f"{fp}: Unbalanced curlies ({curlies})"
    assert parens == 0, f"{fp}: Unbalanced parens ({parens})"
    assert brackets == 0, f"{fp}: Unbalanced brackets ({brackets})"
    print(f"  ✓ {fp}: 100% Balanced ({counts['{']} curlies, {counts['(']} parens, {counts['[']} brackets)")

print("=== 1. VERIFYING GML SYNTAX & TOKEN BALANCE ===")
check_file("objects/obj_FactionManager/Create_0.gml")
check_file("objects/obj_HQTerminal/Draw_64.gml")

print("=== 2. VERIFYING 6-FACTION ROSTER IN FACTIONS_LORE.JSON ===")
lore_path = os.path.join(BASE_DIR, "datafiles/factions_lore.json")
with open(lore_path, "r", encoding="utf-8") as f:
    lore_data = json.load(f)

factions = lore_data.get("factions", {})
expected_keys = [
    "faction_terran",
    "faction_colony",
    "faction_syndicate",
    "faction_zaibatsu",
    "faction_astran",
    "faction_martian"
]

for ek in expected_keys:
    assert ek in factions, f"Missing {ek} in factions_lore.json"
    fac = factions[ek]
    assert "name" in fac and "short_name" in fac and "ai_brain" in fac
    print(f"  ✓ Faction Verified: {fac['name']} [{fac['short_name']}] - Alignment: {fac['alignment']}")

print("=== 3. VALIDATING SIDEREAL SOVEREIGN LEAGUE (FACTION_ASTRAN / HOMO SIDERALIS) ===")
astran = factions["faction_astran"]
bio = astran.get("biological_profile", {})
assert "Homo Sideralis" in bio.get("species_designation", ""), "Missing Homo Sideralis designation"
assert "Osteocartilaginous elongation" in bio.get("skeletal_structure", ""), "Missing skeletal elongation"
assert "spr_brace" in bio.get("planetary_mobility", ""), "Missing exoskeleton brace reference"
assert "photophobia" in bio.get("sensory_and_ocular", "").lower(), "Missing photophobia sensory profile"
assert "translucent albinoid" in bio.get("dermatology_and_pigment", "").lower(), "Missing albinoid dermis description"

print(f"  ✓ Biological Profile Confirmed: {bio['species_designation']}")
print(f"    - Skeletal Structure: {bio['skeletal_structure'][:70]}...")
print(f"    - Mobility Gear: {bio['planetary_mobility']}")
print(f"    - Ocular Sensitivity: {bio['sensory_and_ocular'][:70]}...")
print(f"    - Dermis & Hair: {bio['dermatology_and_pigment'][:70]}...")

assert "Astraea Archon X-09" in astran["ai_brain"]["superweapon"], "Missing Astraea Archon X-09 superweapon"
print(f"  ✓ Spacenoid Superweapon Verified: {astran['ai_brain']['superweapon']}")
print(f"  ✓ Sacred Cradle Philosophy Verified: {astran['phase_1_context']['founding_ethos'][:80]}...")

print("=== 4. VALIDATING THARSIS MACHINE CONSENSUS & PLAYER FLAGSHIP ORIGIN ===")
martian = factions["faction_martian"]
mship = martian.get("mothership_origin_connection", {})
assert "APV Hephaestus" in mship.get("player_ship_identity", ""), "Missing APV Hephaestus ship identity"
assert "Sister Unit 07" in mship.get("awakening_reaction", "") or "Sister Ark" in mship.get("awakening_reaction", ""), "Missing Sister Unit awakening telemetry"
assert "Ares Primus" in martian["overview"], "Missing Ares Primus in Martian lore"
assert "Deus-Machina: Ouroboros Prime" in martian["ai_brain"]["superweapon"], "Missing Ouroboros Prime superweapon"

print(f"  ✓ Subterranean Machine Cult Confirmed: {martian['name']} (Governed by Ares Primus)")
print(f"  ✓ Player Flagship Origin Verified: {mship['player_ship_identity']}")
print(f"    - Revelation: {mship['narrative_twist'][:90]}...")
print(f"    - Awakening Telemetry: {mship['awakening_reaction'][:90]}...")
print(f"  ✓ Logic God Superweapon Verified: {martian['ai_brain']['superweapon']}")

print("=== 5. VERIFYING BILATERAL DIPLOMATIC MATRIX (12 PAIRS) IN OBJ_FACTIONMANAGER ===")
fm_file = os.path.join(BASE_DIR, "objects/obj_FactionManager/Create_0.gml")
with open(fm_file, "r", encoding="utf-8") as f:
    fm_text = f.read()

required_pairs = [
    "terran_colony",
    "terran_syndicate",
    "terran_zaibatsu",
    "colony_syndicate",
    "colony_zaibatsu",
    "syndicate_zaibatsu",
    "terran_astran",
    "colony_astran",
    "syndicate_astran",
    "zaibatsu_astran",
    "terran_martian",
    "zaibatsu_martian"
]

for rp in required_pairs:
    assert rp + ":" in fm_text, f"Missing bilateral relation {rp} in obj_FactionManager"
    print(f"  ✓ Bilateral Relation Verified: {rp}")

assert "faction_e:" in fm_text and "faction_f:" in fm_text, "Missing faction_e or faction_f structs"
assert "ms_astran_chariot_01" in fm_text, "Missing Astran candidate suit"
assert "ms_martian_phobos_01" in fm_text, "Missing Martian candidate suit"
print("  ✓ Candidate Mobile Suits & Mass Production Contracts Verified for Factions E & F.")

print("=== 6. VERIFYING HQTERMINAL DRAW_64 MULTI-FACTION PRESENTATION ===")
hq_file = os.path.join(BASE_DIR, "objects/obj_HQTerminal/Draw_64.gml")
with open(hq_file, "r", encoding="utf-8") as f:
    hq_text = f.read()

assert '["faction_a", "faction_b", "faction_c", "faction_d", "faction_e", "faction_f"]' in hq_text, "Missing 6-faction list in Draw_64"
assert "[SECTOR 0]" in hq_text, "Missing Sector 0 dormant Martian indicator in Draw_64"
assert "BILATERAL RELATIONS MATRIX (12 PAIRS):" in hq_text, "Missing 12-pair bilateral header in Draw_64"
print("  ✓ HQTerminal Draw_64 UI verification passed for 6-faction contracts, mass production fly-offs, and 12-pair diplomatic relations.")

print("=====================================================================")
print("=== ALL EXPANDED FACTIONS LORE & AI TESTS PASSED (100%) ===")
print("=====================================================================")
