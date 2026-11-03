import re

with open('scripts/scr_territory_war_system/scr_territory_war_system.gml') as f:
    war_sys = f.read()

with open('objects/obj_BattleManager/Create_0.gml') as f:
    bm_create = f.read()

with open('objects/obj_BattleManager/Draw_64.gml') as f:
    bm_draw = f.read()

with open('objects/obj_HQTerminal/Draw_64.gml') as f:
    hq_draw = f.read()

# Verify all key connections exist
assert 'scr_territory_get_battle_map_id' in war_sys, "Missing scr_territory_get_battle_map_id"
assert 'active_combat_context' in hq_draw, "Missing active_combat_context in HQTerminal Draw_64"
assert 'active_combat_context' in bm_create, "Missing active_combat_context in BattleManager Create_0"
assert 'active_combat_context' in bm_draw, "Missing active_combat_context in BattleManager Draw_64"
assert 'last_battle_report' in hq_draw, "Missing last_battle_report in HQTerminal Draw_64"
assert 'last_battle_report' in bm_draw, "Missing last_battle_report in BattleManager Draw_64"

print("✓ All 6 tactical sortie pipeline assertions PASSED!")
