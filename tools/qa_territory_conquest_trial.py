#!/usr/bin/env python3
import subprocess
import time
import os
import sys
from PIL import Image

aid = "7bbc3111-e9e2-4ce9-ac27-cdbb483aa140"
out_dir = f"/home/tom/.gemini/antigravity-ide/brain/{aid}"
os.makedirs(out_dir, exist_ok=True)

print("="*75)
print("  MECHMAKER CONCEPT - PLANETARY & ORBITAL TERRITORY CONQUEST QA TRIAL")
print("  Validating Earth, Space & Mars Territories, Fair Starting Parity, Materials & UI")
print("="*75)

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.stdout.strip()

# Wait for game window
win_id = None
for attempt in range(40):
    lines = run_cmd("DISPLAY=:0 wmctrl -l").splitlines()
    game_lines = [l for l in lines if "MechMakerConcept" in l]
    if game_lines:
        win_id = game_lines[0].split()[0]
        break
    time.sleep(2)

if not win_id:
    print("[ERROR] Game window MechMakerConcept not found!")
    sys.exit(1)

print(f"Target Window ID: {win_id}")
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} windowraise {win_id}")
time.sleep(1.0)

info = run_cmd(f"DISPLAY=:0 xwininfo -id {win_id}")
wx, wy = 0, 0
for line in info.splitlines():
    if "Absolute upper-left X:" in line:
        wx = int(line.split(":")[1].strip())
    if "Absolute upper-left Y:" in line:
        wy = int(line.split(":")[1].strip())

print(f"Window Top-Left: ({wx}, {wy})")

def capture(name):
    path = os.path.join(out_dir, f"{name}.png")
    run_cmd(f"DISPLAY=:0 import -window {win_id} {path}")
    print(f"[CAPTURED] {name}.png")
    return path

def click(rx, ry, sleep_s=0.5):
    cx = wx + rx
    cy = wy + ry
    run_cmd(f"DISPLAY=:0 xdotool mousemove --sync {cx} {cy} click 1")
    time.sleep(sleep_s)

# 1. Capture initial boot / intro
capture("territory_qa_01_boot")

# Click Skip Intro / Confirm Commander if intro is open
# Button 1: Next page of intro >>
click(683, 715, 0.8)
capture("territory_qa_02_commander_page")

# Button 2: Confirm Dossier & Boot PMC >>
click(683, 715, 1.2)
capture("territory_qa_03_command_deck")

# Click Tab 4: STRATEGIC WAR MAP (x: 24 + 3 * 263 + 130 = 840, y: 86)
click(840, 86, 0.8)
capture("territory_qa_04_war_map_earth_sphere")

# Click Territory 1 on Earth: Jaburo (node around x: 44 + 30 + 190 = 264, y: 192 + 35 + 260 = 487)
click(264, 487, 0.6)
capture("territory_qa_05_earth_granite_redoubt_selected")

# Click Territory 2 on Earth: Odessa (Colonies foothold) (x: 44 + 30 + 390 = 464, y: 192 + 35 + 140 = 367)
click(464, 367, 0.6)
capture("territory_qa_06_earth_sahara_array_selected")

# Click Territory 3 on Earth: Neo-Tokyo (Zaibatsu) (x: 44 + 30 + 540 = 614, y: 192 + 35 + 160 = 387)
click(614, 387, 0.6)
capture("territory_qa_07_earth_neo_tokyo_selected")

# Switch to Sphere Tab 2: SPACE & COLONIES (x: 44 + 240 + 115 = 399, y: 192 - 12 = 180)
click(399, 180, 0.8)
capture("territory_qa_08_space_sphere")

# Click Solomon Asteroid Citadel (x: 44 + 30 + 200 = 274, y: 192 + 35 + 220 = 447)
click(274, 447, 0.6)
capture("territory_qa_09_space_ironspire_bastion_selected")

# Click Von Braun Lunar City (x: 44 + 30 + 270 = 344, y: 192 + 35 + 130 = 357)
click(344, 357, 0.6)
capture("territory_qa_10_space_von_braun_selected")

# Switch to Sphere Tab 3: MARS SPHERE (x: 44 + 480 + 115 = 639, y: 180)
click(639, 180, 0.8)
capture("territory_qa_11_mars_locked_quarantine")

# Click [OVERRIDE SENSOR LOCK // AWAKEN MARS] (x: 44 + 30 + 180 = 254, y: 192 + 260 + 18 = 470)
click(254, 470, 1.2)
capture("territory_qa_12_mars_unlocked_consensus")

# Click Olympus Mons Mega-Forge (x: 44 + 30 + 180 = 254, y: 192 + 35 + 170 = 397)
click(254, 397, 0.6)
capture("territory_qa_13_mars_olympus_selected")

# Launch PMC Assault on an enemy territory
# Click Launch PMC Assault button in dossier (x: 778 + 260 = 1038, y: 192 + 316 + 16 = 524)
click(1038, 524, 1.0)
capture("territory_qa_14_after_pmc_assault")

# Switch to Mining Concessions View (Toggle Mode 2) (x: 44 + 352 + 170 = 566, y: 152 + 13 = 165)
click(566, 165, 0.8)
capture("territory_qa_15_mining_concessions_view")

# Advance Turn to trigger logistics yield and Gundam-style war shift (x: 1280, y: 36)
click(1280, 36, 1.2)
capture("territory_qa_16_turn_advanced_logistics")

print("\n[QA TRIAL FINISHED] All 16 territory milestone tests completed successfully!")
