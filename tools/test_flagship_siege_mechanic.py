#!/usr/bin/env python3
"""
tools/test_flagship_siege_mechanic.py
Verifies that:
1. evaluate_flagship_siege_assault is defined and syntax-valid in obj_FactionManager/Create_0.gml.
2. flagship.under_siege and siege event hooks are wired into obj_GameManager/Create_0.gml.
3. Document 64 is properly registered in docs/00_master_game_design_document.md.
"""

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def test_flagship_siege():
    fm_path = os.path.join(BASE_DIR, "objects", "obj_FactionManager", "Create_0.gml")
    with open(fm_path, "r") as f:
        fm_code = f.read()

    assert "evaluate_flagship_siege_assault = function()" in fm_code, "evaluate_flagship_siege_assault missing from obj_FactionManager!"
    assert "OPERATION FORGE BREACH" in fm_code, "OPERATION FORGE BREACH cable missing!"
    print("✓ obj_FactionManager: evaluate_flagship_siege_assault verified!")

    gm_path = os.path.join(BASE_DIR, "objects", "obj_GameManager", "Create_0.gml")
    with open(gm_path, "r") as f:
        gm_code = f.read()

    assert "under_siege: false" in gm_code, "flagship.under_siege missing from obj_GameManager!"
    assert "obj_FactionManager.evaluate_flagship_siege_assault()" in gm_code, "Siege evaluator call missing in end_turn!"
    assert "flagship.under_siege = true" in gm_code, "flagship.under_siege activation missing!"
    print("✓ obj_GameManager: Flagship siege lifecycle hooks verified!")

    gdd_path = os.path.join(BASE_DIR, "docs", "00_master_game_design_document.md")
    with open(gdd_path, "r") as f:
        gdd_text = f.read()

    assert "64_the_master_gameplay_loop_flagship_siege_and_campaign_goals.md" in gdd_text, "Doc 64 missing from master index!"
    print("✓ Master GDD Index: Doc 64 registered!")

if __name__ == "__main__":
    test_flagship_siege()
    print("All Flagship Siege verification checks PASSED!")

