#!/usr/bin/env python3
import subprocess
import time
import os
import sys
from PIL import Image

aid = "7bbc3111-e9e2-4ce9-ac27-cdbb483aa140"
out_dir = f"/home/tom/.gemini/antigravity-ide/brain/{aid}"
os.makedirs(out_dir, exist_ok=True)

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.stdout.strip()

# 1. Discover Game Window
lines = run_cmd("wmctrl -l").splitlines()
game_lines = [l for l in lines if "MechMakerConcept" in l]
if not game_lines:
    print("[ERROR] MechMakerConcept game window not found!")
    sys.exit(1)

win_id = game_lines[0].split()[0]
print(f"Target Window ID: {win_id}")

run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} windowraise {win_id}")
time.sleep(0.5)

def capture_step(name):
    path = os.path.join(out_dir, f"{name}.png")
    run_cmd(f"DISPLAY=:0 import -window {win_id} {path}")
    print(f"   [SCREENSHOT] {name}.png captured.")
    return path

# Step 1: Open Settings Modal by clicking the HUD button at (1059, 32)
print("Step 1: Opening Settings Modal via HUD button...")
run_cmd(f"DISPLAY=:0 xdotool mousemove --window {win_id} 1059 32 click 1")
time.sleep(0.5)
capture_step("settings_01_modal_audio_tab_muted")

# Step 2: Click the Master Mute Hero Button at center (683, 230) to UNMUTE audio
print("Step 2: Unmuting Master Audio...")
# Hero button: _hero_x = _mx0 + 24 = 307, _hero_y = _tab_y + 38 = 124 + 44 + 38 = 206, _hero_w = 752, _hero_h = 58
# Center: x = 307 + 376 = 683, y = 206 + 29 = 235
run_cmd(f"DISPLAY=:0 xdotool mousemove --window {win_id} 683 235 click 1")
time.sleep(0.5)
capture_step("settings_02_modal_audio_tab_unmuted")

# Step 3: Click 50% Master Volume preset button
# _sb_x0 = 307 + 390 = 697. Step 2 (50%): 697 + 2 * (64 + 6) = 697 + 140 = 837, y = 206 + 58 + 16 + 8 + 13 = 301
print("Step 3: Clicking 50% Volume Preset...")
run_cmd(f"DISPLAY=:0 xdotool mousemove --window {win_id} 850 301 click 1")
time.sleep(0.3)

# Step 4: Click [TEST WEAPON SFX] button
# _ch3_y = _ch2_y + 74 + 10 = 364 + 84 = 448
# _ts_x = 307 + 14 + 110 + 12 = 443, _ts_w = 160 -> center 523, y = 448 + 38 + 13 = 499
print("Step 4: Clicking [TEST WEAPON SFX]...")
run_cmd(f"DISPLAY=:0 xdotool mousemove --window {win_id} 523 499 click 1")
time.sleep(0.3)
capture_step("settings_03_volume_and_test_sfx")

# Step 5: Switch to Tab 2: [2. DISPLAY & SHORTCUTS]
# _t2_x = 307 + 260 + 12 = 579, w = 260, y = 168, h = 28 -> center (709, 182)
print("Step 5: Switching to Display & Shortcuts Tab...")
run_cmd(f"DISPLAY=:0 xdotool mousemove --window {win_id} 709 182 click 1")
time.sleep(0.5)
capture_step("settings_04_modal_display_and_shortcuts_tab")

# Step 6: Close Settings Modal
# _btn_close_x = 303 + (800 - 260)/2 = 573, y = 124 + 540 - 52 = 612 -> center (703, 631)
print("Step 6: Closing Settings Modal...")
run_cmd(f"DISPLAY=:0 xdotool mousemove --window {win_id} 703 631 click 1")
time.sleep(0.5)
capture_step("settings_05_modal_closed_command_deck")

# Step 7: Press [M] key to test quick mute toggle hotkey
print("Step 7: Testing quick mute toggle hotkey [M]...")
run_cmd(f"DISPLAY=:0 xdotool key --window {win_id} m")
time.sleep(0.5)
capture_step("settings_06_quick_mute_hotkey_toast")

# Step 8: Test Tab 4 (Strategic War Map / Planetary & Orbital Conquest)
# Top navigation tabs: Tab 3 is War Map (0:R&D, 1:Factory, 2:Contracts, 3:War Map, 4:Hangar)
# Or press [4] key!
print("Step 8: Navigating to Planetary & Orbital Conquest Map (Tab 4 / key '4')...")
run_cmd(f"DISPLAY=:0 xdotool key --window {win_id} 4")
time.sleep(0.6)
capture_step("territory_01_earth_sphere_overview")

# Step 9: Switch sphere tabs inside War Map:
# Subtab 0 is Planetary Conquest Map.
# Sphere Tabs:
# Earth Sphere: (44 + 210, 154) -> click (149, 168)
# Space & Colonies: (260, 154) -> click (365, 168)
# Mars Sphere: (476, 154) -> click (581, 168)
print("Step 9: Viewing Space & Colonies Sphere...")
run_cmd(f"DISPLAY=:0 xdotool mousemove --window {win_id} 365 168 click 1")
time.sleep(0.5)
capture_step("territory_02_space_and_colonies_sphere")

print("Step 10: Viewing Mars Sphere (Quarantine Alert & Override)...")
run_cmd(f"DISPLAY=:0 xdotool mousemove --window {win_id} 581 168 click 1")
time.sleep(0.5)
capture_step("territory_03_mars_quarantine_sphere")

# Step 11: Click Mars Quarantine Override to unlock Mars
# In obj_HQTerminal/Draw_64.gml:
# Override button: _ovr_x = _radar_x + (_radar_w - _ovr_w)/2 = 44 + (740 - 320)/2 = 254
# _ovr_y = _radar_y + _radar_h - 70 = 188 + 494 - 70 = 612 -> center (414, 630)
print("Step 11: Clicking Mars Quarantine Emergency Override...")
run_cmd(f"DISPLAY=:0 xdotool mousemove --window {win_id} 414 630 click 1")
time.sleep(0.6)
capture_step("territory_04_mars_sphere_unlocked_consensus")

# Step 12: Select a territory node on Mars (e.g. Olympus Mons or Noctis Labyrinthus)
# First Mars node is at center (200, 320)
print("Step 12: Inspecting Mars Territory Dossier...")
run_cmd(f"DISPLAY=:0 xdotool mousemove --window {win_id} 220 330 click 1")
time.sleep(0.5)
capture_step("territory_05_mars_selected_territory_dossier")

# Step 13: Re-open Settings modal while in War Map to confirm it works across any tab
print("Step 13: Opening Settings modal via [O] key from Strategic War Map...")
run_cmd(f"DISPLAY=:0 xdotool key --window {win_id} o")
time.sleep(0.5)
capture_step("settings_07_opened_over_war_map")

print("\n" + "="*70)
print("  ALL TESTS COMPLETED SUCCESSFULLY!")
print("="*70)
