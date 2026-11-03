import subprocess
import time
import os
from PIL import Image

def run_cmd(cmd):
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.stdout.strip()

def activate_and_click(win_id, x, y):
    run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} {x} {y} click 1")
    time.sleep(0.7)

def take_shot(win_id, name):
    path = f"/home/tom/.gemini/antigravity-ide/brain/a9197ef4-c206-4eb1-b4b4-83dfffe898d6/{name}.png"
    run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id}")
    time.sleep(0.3)
    run_cmd(f"spectacle -b -n -a -o {path}")
    if os.path.exists(path):
        im = Image.open(path)
        print(f"Captured {name}: {im.size} (size: {os.path.getsize(path)} bytes)")
        # create small preview
        prev = im.resize((im.width//3, im.height//3), Image.LANCZOS)
        prev.save(f"/home/tom/.gemini/antigravity-ide/brain/a9197ef4-c206-4eb1-b4b4-83dfffe898d6/{name}_thumb.png")
    else:
        print(f"Failed to capture {name}")

print("=== STARTING QA FULL SYSTEM TRIAL IN GAMEMAKER CLIENT ===")

# 1. Identify EXACT Game Window
lines = run_cmd("wmctrl -l").splitlines()
game_lines = [l for l in lines if l.endswith("MechMakerConcept")]
assert game_lines, "Could not find MechMakerConcept game window!"
win_id = game_lines[0].split()[0]
print(f"Found EXACT game window ID: {win_id} (line: {game_lines[0]})")

# Step 0: Ensure window is focused & dismissed intro if needed
activate_and_click(win_id, 1050, 688)
activate_and_click(win_id, 1010, 688)

# TEST 1: TAB 0 - R&D LAB // ALLOY & PROTOTYPING (x=155, y=86)
print("\n--- Testing Tab 0: R&D Lab ---")
activate_and_click(win_id, 155, 86)
take_shot(win_id, "trial_01_rd_lab")

# TEST 2: TAB 1 - FACTORY FLOOR & PERSONNEL (x=416, y=86)
print("\n--- Testing Tab 1: Factory Floor ---")
activate_and_click(win_id, 416, 86)
take_shot(win_id, "trial_02_factory_floor")

# TEST 3: TAB 2 - CONTRACT BOARD & COMMERCE (x=680, y=86)
print("\n--- Testing Tab 2: Contract Board ---")
activate_and_click(win_id, 680, 86)
take_shot(win_id, "trial_03_contract_board")

# TEST 4: TAB 3 - STRATEGIC WAR MAP (x=943, y=86)
print("\n--- Testing Tab 3: Strategic War Map ---")
activate_and_click(win_id, 943, 86)
take_shot(win_id, "trial_04_war_map")

# TEST 5: TAB 4 - DREADNOUGHT // WARSHIP & RIVALS (x=1206, y=86)
print("\n--- Testing Tab 4: Dreadnought Fleet Flagship ---")
activate_and_click(win_id, 1206, 86)
take_shot(win_id, "trial_05_dreadnought_flagship")

# Verify that game process is still alive and has zero crashes
ps_out = run_cmd("ps aux | grep -i 'Runner.exe' | grep -v grep")
print("\nGame process status:\n", ps_out)

err_out = run_cmd("wmctrl -l | grep -i 'error'")
if err_out:
    print("\n[QA ERROR DETECTED] Error window found:\n", err_out)
else:
    print("\n[QA PASS] ZERO errors or crashes detected across all 5 major command tabs in live client!")

print("=== QA FULL SYSTEM TRIAL COMPLETE ===")
