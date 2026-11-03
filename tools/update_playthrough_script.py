import re

target = "tools/qa_true_exhaustive_playthrough.py"
with open(target, "r") as f:
    text = f.read()

old_flyoff = """# Subtab 1: Corporate Procurement Fly-Off Trials
move_and_click(623, 154, "Subtab 1: Procurement Fly-Off Trials", post_delay=0.8)
# Advance to Phase 2
move_and_click(600, 680, "Fly-Off: Advance to Phase 2 Stress Gauntlet", post_delay=0.8)
# Apply Field Refinements
move_and_click(300, 340, "Refinement: Reinforce Frontal Glacis Armor", post_delay=0.4)
move_and_click(300, 420, "Refinement: Vernier Thruster Overclock", post_delay=0.4)
move_and_click(300, 500, "Refinement: Fire Control Sensor Calibration", post_delay=0.4)
capture_step("play_23_procurement_flyoff_phase2")
check_for_gml_error()"""

new_flyoff = """# Subtab 1: Corporate Procurement Fly-Off Trials
move_and_click(623, 154, "Subtab 1: Procurement Fly-Off Trials", post_delay=0.8)
# Select Candidate Mobile Suit from Hangar list
move_and_click(240, 430, "Fly-Off: Select Candidate Mobile Suit from Hangar", post_delay=0.6)

# Apply Field Refinements in Phase 1 (BEFORE Stress Gauntlet)
move_and_click(557, 600, "Refinement: Overclock Reactor (+15% Core)", post_delay=0.4)
move_and_click(740, 600, "Refinement: Weld Frontal Armor (+12% Armor)", post_delay=0.4)
move_and_click(923, 600, "Refinement: Tune Verniers (+15% Speed)", post_delay=0.4)
capture_step("play_23_procurement_flyoff_phase1_refinements")
check_for_gml_error()

# Advance to Phase 2: Stress Gauntlet
move_and_click(833, 646, "Fly-Off: Advance to Phase 2 Stress Gauntlet", post_delay=1.0)
capture_step("play_23b_procurement_flyoff_phase2_telemetry")
check_for_gml_error()

# Advance to Phase 3: Operational Combat Fly-Off Duel
move_and_click(833, 715, "Fly-Off: Advance to Phase 3 Duel Matchup", post_delay=1.0)
capture_step("play_23c_procurement_flyoff_phase3_duel")
check_for_gml_error()

# Advance to Phase 4: Final Procurement Board Verdict
move_and_click(833, 715, "Fly-Off: Advance to Phase 4 Board Verdict", post_delay=1.2)
capture_step("play_23d_procurement_flyoff_phase4_verdict")
check_for_gml_error()"""

assert old_flyoff in text, "Could not find old_flyoff in script"
text = text.replace(old_flyoff, new_flyoff)

with open(target, "w") as f:
    f.write(text)

print("[SUCCESS] Updated tools/qa_true_exhaustive_playthrough.py with complete 4-phase fly-off progression!")
