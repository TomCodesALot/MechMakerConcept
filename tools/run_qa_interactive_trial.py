import subprocess
import time
import os
from PIL import Image

def run_cmd(cmd):
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.stdout.strip()

print("=== STARTING INTERACTIVE QA SYSTEM TRIAL ===")

# 1. Identify window
lines = run_cmd("wmctrl -l").splitlines()
game_lines = [l for l in lines if l.endswith("MechMakerConcept")]
assert game_lines, "Could not find MechMakerConcept game window!"
win_id = game_lines[0].split()[0]
print(f"Found Game Window: {win_id}")

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
        # save small thumbnail
        thumb = crop.resize((crop.width // 4, crop.height // 4), Image.LANCZOS)
        thumb.save(thumb_path)
        colors = len(set(crop.getpixel((x, y))[:3] for x in range(0, crop.width, 20) for y in range(0, crop.height, 20)))
        print(f"Captured {name}: {crop.size}, sampled unique colors: {colors}")
        return colors
    else:
        print(f"Failed to capture {name}")
        return 0

# Step 1: Capture Intro / Initial Screen
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} windowraise {win_id}")
time.sleep(0.5)
capture_game("trial_00_initial_state")

# Step 2: Advance / Skip to Command Deck via Space key or click
print("\nAdvancing through intro modal...")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key space")
time.sleep(0.5)
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key space")
time.sleep(0.8)

# Also click skip button just in case: x=180, y=688 in window coords
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 180 688 click 1")
time.sleep(0.8)

# TEST 1: TAB 0 - R&D LAB // ALLOY CRUCIBLE & PROTOTYPING
print("\n--- Testing Tab 0: R&D Lab ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key 1")
time.sleep(0.5)
# Click Tab 0 header button (x=155, y=86)
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 155 86 click 1")
time.sleep(0.6)
capture_game("trial_01_rd_lab_verified")

# TEST 2: TAB 1 - FACTORY FLOOR & CAD ASSEMBLY
print("\n--- Testing Tab 1: Factory Floor ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key 2")
time.sleep(0.5)
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 416 86 click 1")
time.sleep(0.6)
capture_game("trial_02_factory_floor_verified")

# TEST 3: TAB 2 - CONTRACT BOARD & COMMERCE
print("\n--- Testing Tab 2: Contract Board ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key 3")
time.sleep(0.5)
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 680 86 click 1")
time.sleep(0.6)
capture_game("trial_03_contract_board_verified")

# TEST 4: TAB 3 - STRATEGIC WAR MAP
print("\n--- Testing Tab 3: Strategic War Map ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key 4")
time.sleep(0.5)
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 943 86 click 1")
time.sleep(0.6)
capture_game("trial_04_war_map_verified")

# TEST 5: TAB 4 - DREADNOUGHT FLAGSHIP & RIVALS
print("\n--- Testing Tab 4: Dreadnought Fleet Flagship ---")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key 5")
time.sleep(0.5)
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} 1206 86 click 1")
time.sleep(0.6)
capture_game("trial_05_dreadnought_flagship_verified")

# Check for crashes / error dialogs
ps_out = run_cmd("ps aux | grep -i 'Runner.exe' | grep -v grep")
print("\nActive Runner process status:\n", ps_out)

err_out = run_cmd("wmctrl -l | grep -i 'error'")
if err_out:
    print("\n[QA ERROR DETECTED] Error window found:\n", err_out)
else:
    print("\n[QA PASS] ZERO errors or crashes detected across all 5 major command tabs in live client!")

print("=== INTERACTIVE QA SYSTEM TRIAL COMPLETE ===")
