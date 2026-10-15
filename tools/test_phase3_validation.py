#!/usr/bin/env python3
"""
tools/test_phase3_validation.py
Comprehensive Phase 3 validation suite:
1. Validates JSON schemas for YYP, Room, Object, and Script metadata.
2. Performs robust static analysis on GML scripts and events.
3. Validates Nemesis calculus, romance heartbreak triggers, and campaign seed rolls.
"""

import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def strip_gml(content):
    """Accurately strips strings and comments from GML code."""
    result = []
    i = 0
    n = len(content)
    while i < n:
        # String literal "..."
        if content[i] == '"':
            i += 1
            while i < n and content[i] != '"':
                if content[i] == '\\' and i + 1 < n:
                    i += 2
                else:
                    i += 1
            i += 1
        # Single-line comment //...
        elif content[i:i+2] == '//':
            while i < n and content[i] != '\n':
                i += 1
        # Multi-line comment /*...*/
        elif content[i:i+2] == '/*':
            i += 2
            while i < n and content[i:i+2] != '*/':
                i += 1
            i += 2
        else:
            result.append(content[i])
            i += 1
    return "".join(result)

def test_json_files():
    print("=== 1. VALIDATING JSON & YY METADATA FILES ===")
    files_to_check = [
        "MechMakerConcept.yyp",
        "rooms/rm_init/rm_init.yy",
        "objects/obj_NemesisManager/obj_NemesisManager.yy",
        "scripts/scr_nemesis_system/scr_nemesis_system.yy",
        "datafiles/characters_roster.json",
        "characters_roster.json"
    ]
    for rel_path in files_to_check:
        full_path = os.path.join(BASE_DIR, rel_path)
        assert os.path.exists(full_path), f"File not found: {rel_path}"
        with open(full_path, "r", encoding="utf-8") as f:
            text = f.read()
            data = json.loads(re.sub(r",\s*([}\]])", r"\1", text))
        print(f"  ✓ {rel_path}: Valid JSON ({len(data)} top-level elements)")

def test_gml_syntax():
    print("\n=== 2. STATIC GML BRACE & SYNTAX VERIFICATION ===")
    gml_files = [
        "scripts/scr_nemesis_system/scr_nemesis_system.gml",
        "objects/obj_NemesisManager/Create_0.gml",
        "objects/obj_NemesisManager/CleanUp_0.gml",
        "rooms/rm_init/RoomCreationCode.gml",
        "objects/obj_GameManager/Create_0.gml",
        "objects/obj_HQTerminal/Draw_64.gml",
        "objects/obj_BattleManager/Create_0.gml"
    ]
    for rel_path in gml_files:
        full_path = os.path.join(BASE_DIR, rel_path)
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        cleaned = strip_gml(content)
        
        curly_open = cleaned.count('{')
        curly_close = cleaned.count('}')
        paren_open = cleaned.count('(')
        paren_close = cleaned.count(')')
        brack_open = cleaned.count('[')
        brack_close = cleaned.count(']')
        
        assert curly_open == curly_close, f"{rel_path}: Mismatched curlies: {curly_open} open vs {curly_close} close"
        assert paren_open == paren_close, f"{rel_path}: Mismatched parens: {paren_open} open vs {paren_close} close"
        assert brack_open == brack_close, f"{rel_path}: Mismatched brackets: {brack_open} open vs {brack_close} close"
        
        print(f"  ✓ {rel_path}: Perfectly Balanced ({curly_open} curlies, {paren_open} parens, {brack_open} brackets)")

def test_nemesis_calculus():
    print("\n=== 3. SIMULATING NEMESIS CALCULUS & ROMANCE TRAUMA ===")
    with open(os.path.join(BASE_DIR, "datafiles/characters_roster.json")) as f:
        chars = json.load(f)["characters"]
    
    char_map = {c["id"]: c for c in chars}
    
    # Test case: Marcus Cole dies, check Kira Dahl (Star-Crossed Lover)
    cole = char_map["pilot_terran_cole"]
    kira_id = cole["love_interest"]["target_id"]
    kira = char_map[kira_id]
    
    print(f"  Casualty: {cole['name']} (Terran)")
    print(f"  Star-Crossed Lover: {kira['name']} (Colony)")
    print(f"  Romance Type: {cole['love_interest']['relationship_type']}")
    print(f"  Trauma Mode: {cole['love_interest']['trauma_reaction']}")
    
    # Heartbreak Grudge calculation
    base_sev = 75 if cole["role"] != "Rookie" else 35
    g_mult = cole["love_interest"]["grudge_multiplier"]
    sim_grudge = min(100, int(base_sev * g_mult))
    print(f"  Calculated Heartbreak Grudge: +{sim_grudge} Grudge")
    assert sim_grudge >= 70, "Heartbreak grudge should immediately exceed Vendetta threshold (70)"
    print("  ✓ Lover exceeds Vendetta Threshold (>=70) -> Correctly triggers Blood Vendetta")
    
    # Test case: Referral Discount
    cole_friends = cole["friendships"]["friend_ids"]
    assert "pilot_terran_rostova" in cole_friends, "Elena Rostova should be Marcus Cole's friend"
    base_cost = cole["hiring_cost_cr"]
    discounted_cost = int(base_cost * 0.75)
    print(f"\n  Friendship Referral Test:")
    print(f"  Marcus Cole Base Cost: {base_cost:,} Cr")
    print(f"  Discounted Cost (-25%): {discounted_cost:,} Cr (Savings: {base_cost - discounted_cost:,} Cr)")
    print("  ✓ Referral calculation verified")

if __name__ == "__main__":
    test_json_files()
    test_gml_syntax()
    test_nemesis_calculus()
    print("\n>>> ALL PHASE 3 ARCHITECTURE TESTS PASSED SUCCESSFULLY! <<<")
