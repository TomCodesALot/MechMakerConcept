import subprocess
import time
import os
from PIL import Image

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

aid = "7bbc3111-e9e2-4ce9-ac27-cdbb483aa140"
out_dir = f"/home/tom/.gemini/antigravity-ide/brain/{aid}"

print("==================================================================")
print("  MECHMAKER CONCEPT - 100K CREDITS & TURN 1 FULL QA PLAYTHROUGH  ")
print("==================================================================")

lines = run_cmd("wmctrl -l").splitlines()
game_lines = [l for l in lines if "MechMakerConcept" in l]
assert game_lines, "Could not find MechMakerConcept game window!"
win_id = game_lines[0].split()[0]
print(f"Target Window ID: {win_id}")

# Activate and bring window to foreground
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} windowraise {win_id}")
time.sleep(0.5)

# Game window root display coordinates
info = run_cmd(f"xwininfo -id {win_id}")
win_offset_x = 37
win_offset_y = 34
for line in info.splitlines():
    if "Absolute upper-left X:" in line:
        win_offset_x = int(line.split(":")[1].strip())
    if "Absolute upper-left Y:" in line:
        win_offset_y = int(line.split(":")[1].strip())

print(f"Window display offset: ({win_offset_x}, {win_offset_y})")

def move_and_click(target_x, target_y, label="Button", steps=8, hover_delay=0.2, post_delay=0.3):
    print(f">> [ACTION] Moving mouse to {label} at ({target_x}, {target_y})...")
    
    m_info = run_cmd("DISPLAY=:0 xdotool getmouselocation").split()
    try:
        cur_x = int(m_info[0].split(":")[1])
        cur_y = int(m_info[1].split(":")[1])
    except:
        cur_x, cur_y = win_offset_x + 683, win_offset_y + 384
        
    dest_x = win_offset_x + target_x
    dest_y = win_offset_y + target_y
    
    for i in range(1, steps + 1):
        step_x = int(cur_x + (dest_x - cur_x) * (i / steps))
        step_y = int(cur_y + (dest_y - cur_y) * (i / steps))
        run_cmd(f"DISPLAY=:0 xdotool mousemove {step_x} {step_y}")
        time.sleep(0.012)
        
    run_cmd(f"DISPLAY=:0 xdotool mousemove {dest_x} {dest_y}")
    time.sleep(hover_delay)
    
    run_cmd("DISPLAY=:0 xdotool mousedown 1")
    time.sleep(0.08)
    run_cmd("DISPLAY=:0 xdotool mouseup 1")
    time.sleep(post_delay)

def capture_step(step_name):
    path = os.path.join(out_dir, f"{step_name}.png")
    run_cmd(f"import -window {win_id} {path}")
    print(f"   [SAVED] {path}")

# =========================================================================
# PHASE 1: DISMISS INTRO BRIEFING & SELECT COMMANDER
# =========================================================================
print("\n>>> PHASE 1: HANDLING SITUATION BRIEFING & APPOINTING COMMANDER <<<")
capture_step("qa_100k_01_briefing_page0")

# Click APPOINT COMMANDER PROFILE (Page 0 -> Page 1)
move_and_click(1051, 688, ">> APPOINT COMMANDER PROFILE >>")
time.sleep(0.4)
capture_step("qa_100k_02_commander_page1")

# Select Female Commander Card (Center ~790, 300)
move_and_click(790, 300, "Commander Card: Morgan Vance (Female Executive)")
time.sleep(0.3)

# Select Male Commander Card (Center ~515, 300)
move_and_click(515, 300, "Commander Card: Alexei Kane (Male Executive)")
time.sleep(0.3)

# Click CONFIRM DOSSIER & INITIALIZE PMC
move_and_click(1011, 688, ">> CONFIRM DOSSIER & INITIALIZE PMC >>", post_delay=0.6)
time.sleep(0.5)

# Verify Command Deck Booted
capture_step("qa_100k_03_command_deck_turn1")

# =========================================================================
# PHASE 2: TAB 0 - R&D CRUCIBLE & MINIGAMES
# =========================================================================
print("\n>>> PHASE 2: TESTING TAB 0 - R&D LAB & CRUCIBLE <<<")
move_and_click(150, 86, "Primary Tab 0: R&D Lab // Prototyping")

# Heat +400 C
move_and_click(70, 570, "Crucible: +400 C Heat")
move_and_click(70, 570, "Crucible: +400 C Heat (Second Pulse)")

# Compress +800 Bar
move_and_click(220, 570, "Crucible: +800 Bar Compress")

# Cool -400 C
move_and_click(70, 615, "Crucible: -400 C Cool")

# Execute Alloy Synthesis Batch
move_and_click(350, 675, "Execute Alloy Synthesis Batch", post_delay=0.6)

# Test Crucible Subviews
move_and_click(930, 195, "Subview 2: Discovered Alloy Codex")
time.sleep(0.3)
move_and_click(1150, 195, "Subview 3: Periodic Table (118 Elements)")
time.sleep(0.3)
move_and_click(730, 195, "Subview 1: Furnace & Batch Preview")
time.sleep(0.3)

# Switch Subtab 1: Prototyping Minigames
move_and_click(550, 150, "Subtab 1: Prototyping Minigames")
time.sleep(0.4)

# Switch Subtab 2: Blueprint Archive
move_and_click(1000, 150, "Subtab 2: Master Blueprint Archive")
time.sleep(0.4)
capture_step("qa_100k_04_tab0_prototyping")

# =========================================================================
# PHASE 3: TAB 1 - FACTORY FLOOR & MODULAR CAD ASSEMBLY
# =========================================================================
print("\n>>> PHASE 3: TESTING TAB 1 - FACTORY FLOOR & CAD MECHA ASSEMBLY <<<")
move_and_click(419, 86, "Primary Tab 1: Factory Floor & Personnel")

# Modular Part Forge
move_and_click(550, 150, "Subtab 1: Modular Part Forge")
time.sleep(0.4)

# Custom Assembly Bay
move_and_click(1000, 150, "Subtab 2: Custom Assembly Bay")
time.sleep(0.4)

# Return to Assembly Floor
move_and_click(150, 150, "Subtab 0: Assembly Floor & Personnel")
time.sleep(0.3)
capture_step("qa_100k_05_tab1_factory")

# =========================================================================
# PHASE 4: TAB 2 - CONTRACT BOARD & FLY-OFFS
# =========================================================================
print("\n>>> PHASE 4: TESTING TAB 2 - CONTRACT BOARD & PROCUREMENT TRIALS <<<")
move_and_click(683, 86, "Primary Tab 2: Contracts & Commerce")

# Accept first contract
move_and_click(1080, 240, "Contract 1: [ACCEPT] Button", post_delay=0.5)

# Subtab 1: Fly-Off Arena
move_and_click(550, 150, "Subtab 1: Procurement Trials & Fly-Off Arena")
time.sleep(0.3)
move_and_click(340, 240, "Fly-Off Faction: Outer Colonies")
time.sleep(0.3)
move_and_click(530, 240, "Fly-Off Faction: Rogue Syndicates")
time.sleep(0.3)

# Subtab 2: Commodity Exchange
move_and_click(1000, 150, "Subtab 2: Commodity Trade Exchange")
time.sleep(0.4)
capture_step("qa_100k_06_tab2_contracts")

# =========================================================================
# PHASE 5: TAB 3 - STRATEGIC WAR MAP & DIPLOMACY
# =========================================================================
print("\n>>> PHASE 5: TESTING TAB 3 - STRATEGIC WAR MAP & DIPLOMACY <<<")
move_and_click(946, 86, "Primary Tab 3: Strategic War Map")

# Sphere Filters
move_and_click(700, 200, "Sphere Filter: Mars")
time.sleep(0.3)
move_and_click(790, 200, "Sphere Filter: Asteroid Belt")
time.sleep(0.3)
move_and_click(614, 200, "Sphere Filter: All")
time.sleep(0.3)

# Subtab 1: Faction Dossiers
move_and_click(400, 150, "Subtab 1: Faction Dossiers & Citadels")
time.sleep(0.3)
move_and_click(220, 200, "Dossier: Outer Colonies")
time.sleep(0.3)
move_and_click(340, 200, "Dossier: Rogue Syndicates")
time.sleep(0.3)
move_and_click(460, 200, "Dossier: Apex Zaibatsu")
time.sleep(0.3)
move_and_click(100, 200, "Dossier: Terran Coalition")
time.sleep(0.3)

# Subtab 2: Diplomacy Matrix
move_and_click(680, 150, "Subtab 2: Bilateral Diplomacy Matrix")
time.sleep(0.3)

# Subtab 3: Decade Mecha Lineage
move_and_click(950, 150, "Subtab 3: Decade Mecha Lineage")
time.sleep(0.3)
capture_step("qa_100k_07_tab3_warmap")

# =========================================================================
# PHASE 6: TAB 4 - DREADNOUGHT WARSHIP & RIVALS
# =========================================================================
print("\n>>> PHASE 6: TESTING TAB 4 - DREADNOUGHT WARSHIP & RIVALS <<<")
move_and_click(1210, 86, "Primary Tab 4: Dreadnought & Rivals")

# Subtab 1: Celestial Navigation
move_and_click(550, 150, "Subtab 1: Celestial Navigation")
time.sleep(0.3)

# Subtab 2: Rival Corporate Monopolies
move_and_click(1000, 150, "Subtab 2: Rival Corporate Monopolies")
time.sleep(0.4)
capture_step("qa_100k_08_tab4_dreadnought")

# =========================================================================
# PHASE 7: TOP HUD ACTION BUTTONS & MODALS
# =========================================================================
print("\n>>> PHASE 7: TESTING TOP HUD ACTION BUTTONS & MODALS <<<")

# Turn Log Modal
move_and_click(780, 32, "Top HUD: [LOG] Turn Ledger Modal")
time.sleep(0.4)
move_and_click(1010, 130, "Turn Ledger: [X CLOSE (ESC)]")
time.sleep(0.3)

# Field Manual Modal
move_and_click(870, 32, "Top HUD: [?] Field Manual Modal")
time.sleep(0.4)
move_and_click(450, 120, "Manual Subtab: Crucible R&D")
time.sleep(0.2)
move_and_click(620, 120, "Manual Subtab: Reactor Tuning")
time.sleep(0.2)
move_and_click(790, 120, "Manual Subtab: Hydraulic Bench")
time.sleep(0.2)
move_and_click(960, 120, "Manual Subtab: Plasma Thrust")
time.sleep(0.2)
move_and_click(280, 120, "Manual Subtab: PMC Manual")
time.sleep(0.2)
move_and_click(1100, 95, "Field Manual: [X CLOSE (ESC)]")
time.sleep(0.3)

# Quick Save
move_and_click(965, 32, "Top HUD: [F5 SAVE] Quick Save")
time.sleep(0.3)

# Commander Profile Badge
move_and_click(1230, 32, "Top HUD: Commander Dossier Badge")
time.sleep(0.4)
move_and_click(200, 700, "Commander Dossier: [CLOSE DOSSIER]")
time.sleep(0.3)
capture_step("qa_100k_09_hud_and_modals")

# =========================================================================
# PHASE 8: STRATEGIC TURN ADVANCEMENT (Turn 1 -> Turn 2 -> Turn 3)
# =========================================================================
print("\n>>> PHASE 8: ADVANCING STRATEGIC TURNS <<<")
move_and_click(650, 32, "Top HUD: >> ADVANCE TURN << (Turn 1 -> Turn 2)", post_delay=0.8)
capture_step("qa_100k_10_turn2_advanced")

move_and_click(650, 32, "Top HUD: >> ADVANCE TURN << (Turn 2 -> Turn 3)", post_delay=0.8)
capture_step("qa_100k_11_turn3_advanced")

print("\n==================================================================")
print("  ALL 100K CREDITS & TURN ADVANCEMENT QA TRIALS COMPLETED!       ")
print("==================================================================")
