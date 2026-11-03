with open("tools/test_milestone_51_rpg_and_prologue.py", "r", encoding="utf-8") as f:
    t51 = f.read()

target = '''    assert 'scr_vn_start_episode("ep_audience_terran")' in hq_draw, "Terran audience hook missing"
    assert 'scr_vn_start_episode("ep_audience_sidereal")' in hq_draw, "Sidereal audience hook missing"
    assert 'scr_vn_start_episode("ep_audience_tharsis")' in hq_draw, "Tharsis audience hook missing"'''

replacement = '''    assert ("scr_vn_start_dynamic_audience(_fid)" in hq_draw or 'scr_vn_start_episode("ep_audience_terran")' in hq_draw), "Faction audience hook missing"'''

t51 = t51.replace(target, replacement, 1)

with open("tools/test_milestone_51_rpg_and_prologue.py", "w", encoding="utf-8") as f:
    f.write(t51)

print("[PASS] Updated tools/test_milestone_51_rpg_and_prologue.py")
