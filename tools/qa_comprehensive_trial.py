import subprocess
import time
import os
from PIL import Image

def run_cmd(cmd):
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.stdout.strip()

print("==================================================")
print("  MECHMAKER CONCEPT - FULL QA AUTOMATED TRIAL     ")
print("==================================================")

# 1. Identify window
lines = run_cmd("wmctrl -l").splitlines()
game_lines = [l for l in lines if l.endswith("MechMakerConcept")]
assert game_lines, "Could not find MechMakerConcept game window!"
win_id = game_lines[0].split()[0]
print(f"Target Game Window: {win_id}")

def capture_game(name):
    full_path = f"/tmp/screen_{name}.png"
    crop_path = f"/home/tom/.gemini/antigravity-ide/brain/a9197ef4-c206-4eb1-b4b4-83dfffe898d6/{name}.png"
    thumb_path = f"/home/tom/.gemini/antigravity-ide/brain/a9197ef4-c206-4eb1-b4b4-83dfffe898d6/{name}_thumb.png"
    
    run_cmd(f"spectacle -b -n -f -o {full_path}")
    if os.path.exists(full_path):
        im = Image.open(full_path)
        # crop game window at (148, 136, 148+2732, 136+1536)
        crop = im.crop((148, 136, min(im.width, 148 + 2732), min(im.height, 136 + 1536)))
        crop.save(crop_path)
        thumb = crop.resize((crop.width // 4, crop.height // 4), Image.LANCZOS)
        thumb.save(thumb_path)
        colors = len(set(crop.getpixel((x, y))[:3] for x in range(0, crop.width, 20) for y in range(0, crop.height, 20)))
        print(f"Captured {name}: {crop.size}, sampled colors: {colors}")
        return colors
    return 0

def check_errors():
    err_out = run_cmd("wmctrl -l | grep -i 'error'")
    if err_out:
        print(f"[QA ALERT] Error window detected: {err_out}")
        return False
    return True

# --- STEP 1: SITUATION BRIEFING (PAGE 0) ---
print("\n--- [STEP 1] Testing Situation Briefing & Text Bounds ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} windowraise {win_id}")
time.sleep(0.5)
capture_game("qa_01_briefing_page0")
assert check_errors(), "Error on Step 1"

# Click Next to Page 1: ">> APPOINT COMMANDER PROFILE >>" at window x=1000, y=700
print("\n--- [STEP 2] Navigating to Page 1: Commander Profiles ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 1000 700 click 1")
time.sleep(0.8)
capture_game("qa_02_commander_profiles_page1")
assert check_errors(), "Error on Step 2"

# Test clicking Profile 2 (Male Alexei Kane) at window x=680, y=500
print("\n--- [STEP 3] Selecting Commander Profile (Alexei Kane) ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 680 500 click 1")
time.sleep(0.5)
capture_game("qa_03_commander_selected_male")
assert check_errors(), "Error on Step 3"

# Confirm & Launch into Command Deck: Click "[CONFIRM PROFILE & ENTER COMMAND DECK]" at window x=960, y=700
print("\n--- [STEP 4] Confirming Commander & Launching Command Deck ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 960 700 click 1")
time.sleep(0.8)
capture_game("qa_04_command_deck_main")
assert check_errors(), "Error on Step 4"

# --- TAB 0: R&D LAB // ALLOY CRUCIBLE & MINIGAMES ---
print("\n--- [STEP 5] Testing Tab 0: R&D Lab & Crucible Controls ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key 1")
time.sleep(0.5)
# Test Crucible buttons:
# [+ HEAT 400C] at window x=75, y=320
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 75 320 click 1")
time.sleep(0.2)
# [+ COMP 800 PSI] at window x=370, y=320
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 370 320 click 1")
time.sleep(0.2)
# Load Tungsten hopper at window x=80, y=420
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 80 420 click 1")
time.sleep(0.3)
# Load Silica hopper at window x=220, y=420
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 220 420 click 1")
time.sleep(0.3)
capture_game("qa_05_tab0_crucible_tuned")
assert check_errors(), "Error on Step 5"

# --- TAB 1: FACTORY FLOOR & CAD ASSEMBLY ---
print("\n--- [STEP 6] Testing Tab 1: Factory Floor & CAD Assembly ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key 2")
time.sleep(0.5)
# Click Sub-tab 1: Platoon Roster at window x=250, y=130
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 250 130 click 1")
time.sleep(0.4)
capture_game("qa_06_tab1_factory_roster")
assert check_errors(), "Error on Step 6"

# --- TAB 2: CONTRACT BOARD & COMMERCE ---
print("\n--- [STEP 7] Testing Tab 2: Contract Board & Bounties ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key 3")
time.sleep(0.5)
# Select first contract card at window x=200, y=260
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 200 260 click 1")
time.sleep(0.4)
capture_game("qa_07_tab2_contracts")
assert check_errors(), "Error on Step 7"

# --- TAB 3: STRATEGIC WAR MAP ---
print("\n--- [STEP 8] Testing Tab 3: Strategic War Map & Mining Theaters ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key 4")
time.sleep(0.5)
# Click Mining Node node 0 at window x=350, y=300
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 350 300 click 1")
time.sleep(0.4)
capture_game("qa_08_tab3_war_map")
assert check_errors(), "Error on Step 8"

# --- TAB 4: DREADNOUGHT FLEET FLAGSHIP ---
print("\n--- [STEP 9] Testing Tab 4: Dreadnought Fleet Flagship ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key 5")
time.sleep(0.5)
# Click Division 0 card at window x=300, y=250
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 300 250 click 1")
time.sleep(0.4)
capture_game("qa_09_tab4_flagship")
assert check_errors(), "Error on Step 9"

# --- STEP 10: TURN ADVANCEMENT & TURN LOG ---
print("\n--- [STEP 10] Testing Turn Advancement (SPACE) & Turn Log ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key space")
time.sleep(0.8)
capture_game("qa_10_turn_advanced")
assert check_errors(), "Error on Step 10"

# Open Turn Log Ledger (key L or click)
print("\n--- [STEP 11] Opening Strategic Turn Log Ledger ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key l")
time.sleep(0.6)
capture_game("qa_11_turn_log_ledger")
assert check_errors(), "Error on Step 11"

# Close Modal (ESC)
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key Escape")
time.sleep(0.5)

# --- STEP 12: IN-ENGINE FIELD MANUAL ---
print("\n--- [STEP 12] Opening In-Engine PMC Field Manual ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key h")
time.sleep(0.6)
capture_game("qa_12_field_manual_modal")
assert check_errors(), "Error on Step 12"

# Close Manual (ESC)
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key Escape")
time.sleep(0.5)
capture_game("qa_13_final_verified_state")
assert check_errors(), "Final Check"

print("\n==================================================")
print("  QA FULL SUITE PASS: ZERO CRASHES, ALL PASS!     ")
print("==================================================")
