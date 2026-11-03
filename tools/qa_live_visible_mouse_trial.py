import subprocess
import time
import os
import sys

def run_cmd(cmd):
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.stdout.strip()

print("==================================================================")
print("  MECHMAKER CONCEPT - VISIBLE REAL-TIME QA MOUSE TRIAL           ")
print("==================================================================")

lines = run_cmd("wmctrl -l").splitlines()
game_lines = [l for l in lines if l.endswith("MechMakerConcept")]
assert game_lines, "Could not find MechMakerConcept game window!"
win_id = game_lines[0].split()[0]
print(f"Target Window ID: {win_id}")

# Activate and bring game window to foreground
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} windowraise {win_id}")
time.sleep(0.5)

# Game window offset on screen
win_offset_x = 37
win_offset_y = 34

def move_and_click(target_x, target_y, label="Button", steps=8, hover_delay=0.25, post_delay=0.35):
    print(f">> [ACTION] Moving mouse to {label} at ({target_x}, {target_y})...")
    
    # 1. Get current mouse location
    m_info = run_cmd("DISPLAY=:0 xdotool getmouselocation").split()
    try:
        cur_x = int(m_info[0].split(":")[1])
        cur_y = int(m_info[1].split(":")[1])
    except:
        cur_x, cur_y = win_offset_x + 683, win_offset_y + 384
        
    dest_x = win_offset_x + target_x
    dest_y = win_offset_y + target_y
    
    # 2. Smooth interpolated cursor glide across screen
    for i in range(1, steps + 1):
        step_x = int(cur_x + (dest_x - cur_x) * (i / steps))
        step_y = int(cur_y + (dest_y - cur_y) * (i / steps))
        run_cmd(f"DISPLAY=:0 xdotool mousemove {step_x} {step_y}")
        time.sleep(0.015)
        
    # Ensure final absolute position
    run_cmd(f"DISPLAY=:0 xdotool mousemove {dest_x} {dest_y}")
    time.sleep(hover_delay) # Pause so hover animation/highlight visibly appears
    
    # 3. Explicit mouse down, hold, and release
    run_cmd("DISPLAY=:0 xdotool mousedown 1")
    time.sleep(0.08) # Hold click down so GameMaker step loop registers pressed state
    run_cmd("DISPLAY=:0 xdotool mouseup 1")
    time.sleep(post_delay)

print("\n>>> PHASE 1: TESTING TAB 0 - R&D CRUCIBLE & PROTOTYPING CONTROLS <<<")
# Ensure on Tab 0
move_and_click(150, 86, "Primary Tab 0: R&D Lab")

# Click +400 C Heat
move_and_click(70, 570, "Crucible: +400 C Heat")
move_and_click(70, 570, "Crucible: +400 C Heat (Second Pulse)")

# Click +800 Bar Compress
move_and_click(220, 570, "Crucible: +800 Bar Compress")

# Click -400 C Cool
move_and_click(70, 615, "Crucible: -400 C Cool")

# Click Execute Alloy Synthesis Batch
move_and_click(350, 675, "Execute Alloy Synthesis Batch", steps=10, post_delay=0.6)

# Test Subviews in Tab 0
move_and_click(930, 195, "Subview 2: Discovered Alloy Codex")
time.sleep(0.4)
move_and_click(1150, 195, "Subview 3: Periodic Table (118 Elements)")
time.sleep(0.4)
move_and_click(730, 195, "Subview 1: Furnace & Batch Preview")
time.sleep(0.4)

# Switch to Subtab 1: Prototyping Minigames
move_and_click(550, 150, "Subtab 1: Prototyping Minigames", steps=10)
time.sleep(0.5)

# Switch to Subtab 2: Master Blueprint Archive
move_and_click(1000, 150, "Subtab 2: Master Blueprint Archive", steps=10)
time.sleep(0.5)

print("\n>>> PHASE 2: TESTING TAB 1 - FACTORY FLOOR & CAD MECHA ASSEMBLY <<<")
# Click Primary Tab 1: Factory Floor
move_and_click(419, 86, "Primary Tab 1: Factory Floor", steps=10)

# Click Subtab 1: Modular Part Forge
move_and_click(550, 150, "Subtab 1: Modular Part Forge", steps=8)
time.sleep(0.5)

# Click Subtab 2: Custom Combinations Assembly Bay
move_and_click(1000, 150, "Subtab 2: Custom Assembly Bay", steps=8)
time.sleep(0.5)

# Return to Subtab 0: Assembly Floor
move_and_click(150, 150, "Subtab 0: Assembly Floor & Personnel", steps=8)
time.sleep(0.4)

print("\n>>> PHASE 3: TESTING TAB 2 - CONTRACT BOARD & FLY-OFF TRIALS <<<")
# Click Primary Tab 2: Contract Board
move_and_click(683, 86, "Primary Tab 2: Contract Board", steps=10)

# Click [ACCEPT] on First Contract Offering
move_and_click(1080, 240, "Contract 1: [ACCEPT] Button", steps=8, post_delay=0.5)

# Click Subtab 1: Procurement Trials & Fly-Offs
move_and_click(550, 150, "Subtab 1: Procurement Trials & Fly-Off Arena", steps=8)
time.sleep(0.4)
# Click Faction card: Outer Colonies
move_and_click(340, 240, "Target Faction: Outer Colonies", steps=6)
time.sleep(0.3)
# Click Faction card: Rogue Syndicates
move_and_click(530, 240, "Target Faction: Rogue Syndicates", steps=6)
time.sleep(0.3)

# Click Subtab 2: Interstellar Commodity Trade Exchange
move_and_click(1000, 150, "Subtab 2: Commodity Trade Exchange", steps=8)
time.sleep(0.4)

print("\n>>> PHASE 4: TESTING TAB 3 - STRATEGIC WAR MAP & FACTION DIPLOMACY <<<")
# Click Primary Tab 3: Strategic War Map
move_and_click(946, 86, "Primary Tab 3: Strategic War Map", steps=10)

# Click Solar Sphere filter: Mars
move_and_click(700, 200, "Sphere Filter: Mars", steps=6)
time.sleep(0.3)
# Click Solar Sphere filter: Belt
move_and_click(790, 200, "Sphere Filter: Asteroid Belt", steps=6)
time.sleep(0.3)
# Click Solar Sphere filter: All
move_and_click(614, 200, "Sphere Filter: All", steps=6)
time.sleep(0.3)

# Click Subtab 1: Faction Dossiers & Recruitable Aces
move_and_click(400, 150, "Subtab 1: Faction Dossiers & Citadels", steps=8)
time.sleep(0.4)
# Switch faction dossier tabs
move_and_click(220, 200, "Faction Tab: Outer Colonies", steps=6)
time.sleep(0.3)
move_and_click(340, 200, "Faction Tab: Rogue Syndicates", steps=6)
time.sleep(0.3)
move_and_click(460, 200, "Faction Tab: Apex Zaibatsu", steps=6)
time.sleep(0.3)
move_and_click(100, 200, "Faction Tab: Terran Coalition", steps=6)
time.sleep(0.3)

# Click Subtab 2: Bilateral Diplomacy Matrix
move_and_click(680, 150, "Subtab 2: Bilateral Diplomacy Matrix", steps=8)
time.sleep(0.4)

# Click Subtab 3: Decade Mecha Lineage
move_and_click(950, 150, "Subtab 3: Decade Mecha Lineage", steps=8)
time.sleep(0.4)

print("\n>>> PHASE 5: TESTING TAB 4 - DREADNOUGHT WARSHIP & CORPORATE MONOPOLIES <<<")
# Click Primary Tab 4: Dreadnought Warship
move_and_click(1210, 86, "Primary Tab 4: Dreadnought Warship", steps=10)

# Click Subtab 1: Celestial Navigation & Orbital Transit
move_and_click(550, 150, "Subtab 1: Celestial Navigation", steps=8)
time.sleep(0.4)

# Click Subtab 2: Rival Corporate Monopolies
move_and_click(1000, 150, "Subtab 2: Rival Corporate Monopolies", steps=8)
time.sleep(0.4)

print("\n>>> PHASE 6: TESTING TOP HUD ACTION BUTTONS & MODALS <<<")
# 1. Turn Log Modal
move_and_click(780, 32, "Top HUD: [LOG] Turn Ledger Modal", steps=8)
time.sleep(0.5)
# Close with close button
move_and_click(1010, 130, "Turn Ledger: [X CLOSE (ESC)]", steps=6)
time.sleep(0.3)

# 2. Field Manual Modal
move_and_click(870, 32, "Top HUD: [?] Field Manual Modal", steps=8)
time.sleep(0.5)
# Test manual subtabs
move_and_click(450, 120, "Manual Subtab: Crucible R&D", steps=6)
time.sleep(0.3)
move_and_click(620, 120, "Manual Subtab: Reactor Tuning", steps=6)
time.sleep(0.3)
move_and_click(790, 120, "Manual Subtab: Hydraulic Bench", steps=6)
time.sleep(0.3)
move_and_click(960, 120, "Manual Subtab: Plasma Thrust", steps=6)
time.sleep(0.3)
move_and_click(280, 120, "Manual Subtab: PMC Manual", steps=6)
time.sleep(0.3)
# Close manual
move_and_click(1100, 95, "Field Manual: [X CLOSE (ESC)]", steps=6)
time.sleep(0.3)

# 3. Quick Save Button
move_and_click(965, 32, "Top HUD: [F5 SAVE] Quick Save", steps=8)
time.sleep(0.4)

# 4. Commander Profile Badge
move_and_click(1230, 32, "Top HUD: Commander Dossier Badge", steps=8)
time.sleep(0.5)
# Close commander dossier
move_and_click(200, 700, "Commander Dossier: [CLOSE DOSSIER]", steps=6)
time.sleep(0.3)

# 5. ADVANCE TURN: Turn 1 -> Turn 2
print("\n>>> PHASE 7: ADVANCING STRATEGIC TURN <<<")
move_and_click(650, 32, "Top HUD: >> ADVANCE TURN << (Turn 1 -> Turn 2)", steps=8, post_delay=0.8)

# ADVANCE TURN AGAIN: Turn 2 -> Turn 3
move_and_click(650, 32, "Top HUD: >> ADVANCE TURN << (Turn 2 -> Turn 3)", steps=8, post_delay=0.8)

print("\n==================================================================")
print("  VISIBLE LIVE MOUSE TRIAL COMPLETED SUCCESSFULLY!                ")
print("==================================================================")
