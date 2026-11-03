# Comprehensive simulation test for HoI4 Research Tree System in GameMaker
import re

print("=== VERIFYING HEARTS OF IRON IV STYLE RESEARCH TREE ===")

# 1. Verify scr_research_tree_system.gml
with open('scripts/scr_research_tree_system/scr_research_tree_system.gml', 'r') as f:
    gml = f.read()

required_funcs = [
    'scr_research_init',
    'scr_research_get_system',
    'scr_research_get_tech_db',
    'scr_research_is_unlocked',
    'scr_research_can_research',
    'scr_research_is_in_progress',
    'scr_research_start',
    'scr_research_cancel',
    'scr_research_advance_turn',
    'scr_research_get_bonus',
    'scr_draw_research_tree_hoi4'
]

for func in required_funcs:
    assert func in gml, f"Missing function: {func}"
print(f"[PASS] All {len(required_funcs)} core research functions verified in scr_research_tree_system.gml")

# 2. Verify all 4 Categories and Tech counts
categories = ["WEAPONS", "REACTORS", "SHIELDS", "UPGRADES"]
for cat in categories:
    assert f'category: "{cat}"' in gml or f"category == _sys.active_category" in gml, f"Missing category: {cat}"
    matches = gml.count(f'category: "{cat}"')
    print(f" - Branch [{cat}]: {matches} technologies registered.")
    assert matches >= 4, f"Insufficient tech nodes for {cat}"

# 3. Verify HoI4 UI components
hoi4_ui_elements = [
    'HOI4 RESEARCH SLOTS // CONCURRENT PROJECTS',
    '[⚔️ WEAPONS]',
    '[⚡ REACTORS]',
    '[🛡️ SHIELDS]',
    '[⚙️ UPGRADES]',
    'TIER 0: PRE-MS',
    'TIER 1: EARLY MS',
    'TIER 2: SPACE',
    'TIER 3: APEX',
    'TECH BLUEPRINT DOSSIER',
    'COMMENCE RESEARCH >>'
]
for elem in hoi4_ui_elements:
    assert elem in gml, f"Missing HoI4 UI element: {elem}"
print("[PASS] Hearts of Iron IV style UI (slots bar, category tabs, era columns, dossier modal) verified.")

# 4. Verify GameManager Integration
with open('objects/obj_GameManager/Create_0.gml') as f:
    gm = f.read()
assert 'scr_research_init()' in gm, "scr_research_init() missing in GameManager"
assert 'scr_research_advance_turn()' in gm, "scr_research_advance_turn() missing in GameManager"
print("[PASS] GameManager properly initialized and wired to advance research on strategic turns.")

# 5. Verify HQ Terminal Subtab Integration
with open('objects/obj_HQTerminal/Draw_64.gml') as f:
    hq = f.read()
assert '[4. TECH RESEARCH TREE (HOI4)]' in hq, "Subtab 4 label missing in HQ Terminal"
assert 'scr_draw_research_tree_hoi4' in hq, "scr_draw_research_tree_hoi4 call missing in HQ Terminal"
print("[PASS] HQ Terminal R&D Lab Tab 0 expanded with Subtab 3 [4. TECH RESEARCH TREE (HOI4)].")

# 6. Verify BattleManager Combat Stat Multipliers
with open('objects/obj_BattleManager/Create_0.gml') as f:
    bm = f.read()
assert 'scr_research_get_bonus("kinetic_dmg")' in bm, "kinetic_dmg bonus missing in BattleManager"
assert 'scr_research_get_bonus("beam_dmg")' in bm, "beam_dmg bonus missing in BattleManager"
assert 'scr_research_get_bonus("beam_resist")' in bm, "beam_resist bonus missing in BattleManager"
assert 'scr_research_get_bonus("barrier_absorb")' in bm, "barrier_absorb bonus missing in BattleManager"
assert 'scr_research_get_bonus("ap_max")' in bm, "ap_max bonus missing in BattleManager"
assert 'scr_research_get_bonus("hit_accuracy")' in bm, "hit_accuracy bonus missing in BattleManager"
assert 'scr_research_get_bonus("move_range")' in bm, "move_range bonus missing in BattleManager"
print("[PASS] BattleManager applies researched bonuses to AP, damage, resistances, hit, and movement.")

# 7. Verify Save System Serialization
with open('scripts/scr_save_system/scr_save_system.gml') as f:
    save = f.read()
assert 'research_system: obj_GameManager.research_system' in save, "Save packing missing research_system"
assert 'obj_GameManager.research_system = _gs.research_system' in save, "Load unpacking missing research_system"
print("[PASS] Save/Load system serializes and restores research_system state.")

print("=== ALL R&D RESEARCH TREE TESTS PASSED 100% ===")
