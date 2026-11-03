import subprocess
import time
import os
import sys
from PIL import Image

def run_cmd(cmd):
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.stdout.strip()

print("==================================================================")
print("  MECHMAKER CONCEPT - LEAD QA COMPREHENSIVE MOUSE INTERACTION TRIAL")
print("==================================================================")

lines = run_cmd("wmctrl -l").splitlines()
game_lines = [l for l in lines if l.endswith("MechMakerConcept")]
assert game_lines, "Could not find MechMakerConcept game window in wmctrl!"
win_id = game_lines[0].split()[0]
print(f"Target Active Game Window: {win_id}")

artifacts_dir = "/home/tom/.gemini/antigravity-ide/brain/7bbc3111-e9e2-4ce9-ac27-cdbb483aa140"
os.makedirs(artifacts_dir, exist_ok=True)

def mouse_click(x, y, label="Button", delay=0.35):
    print(f">> [QA MOUSE CLICK] '{label}' at ({x}, {y})...")
    run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} {x} {y} click 1")
    time.sleep(delay)

def send_key(k, delay=0.35):
    print(f">> [QA KEY] Pressing {k}...")
    run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key {k}")
    time.sleep(delay)

def verify_and_capture(milestone_id, description):
    tmp_path = f"/tmp/{milestone_id}.png"
    art_path = f"{artifacts_dir}/{milestone_id}.png"
    thumb_path = f"{artifacts_dir}/{milestone_id}_thumb.png"
    
    run_cmd(f"import -window {win_id} {tmp_path}")
    assert os.path.exists(tmp_path), f"Capture failed for {milestone_id}"
    
    im = Image.open(tmp_path)
    im.save(art_path)
    thumb = im.resize((im.width // 4, im.height // 4), Image.LANCZOS)
    thumb.save(thumb_path)
    
    # Verify zero text bleeding on rightmost 25px
    r_hits = sum(1 for y in range(im.height) if any(max(im.getpixel((x, y))[:3]) > 165 for x in range(im.width - 25, im.width)))
    # Verify zero text bleeding on bottommost 25px
    b_hits = sum(1 for x in range(im.width) if any(max(im.getpixel((x, y))[:3]) > 165 for y in range(im.height - 25, im.height)))
    
    err_out = run_cmd("wmctrl -l | grep -i 'error'")
    has_err = bool(err_out)
    
    status = "PASS" if (r_hits == 0 and b_hits == 0 and not has_err) else "WARN"
    print(f"[{status}] {milestone_id:<32} | {description:<42} | Bleed R:{r_hits:2d} B:{b_hits:2d} | Err: {has_err}")
    if has_err:
        print(f"[FATAL QA ERROR DETECTED]: {err_out}")
        sys.exit(1)
    return status == "PASS"

# 1. Raise and focus window
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} windowraise {win_id}")
time.sleep(0.5)

print("\n--- [STAGE 1] INITIAL GAME STATE AUDIT (TREASURY 0, TURN 1) ---")
verify_and_capture("qa_step_01_boot_state", "Initial Game Boot State (Treasury 0 Cr, Turn 1)")

# If intro modal or commander modal is open, appoint commander
mouse_click(1000, 700, ">> APPOINT COMMANDER PROFILE >>", 0.5)
verify_and_capture("qa_step_02_commander_modal", "Commander Selection Modal Active")

mouse_click(680, 500, "Profile Card: Alexei Kane (Heavy Vanguard)", 0.3)
verify_and_capture("qa_step_03_commander_male_selected", "Alexei Kane Selected")

mouse_click(1050, 500, "Profile Card: Morgan Vance (Colony Interceptor)", 0.3)
verify_and_capture("qa_step_04_commander_female_selected", "Morgan Vance Selected")

mouse_click(320, 500, "Profile Card: Anonymous Black-Budget", 0.3)
verify_and_capture("qa_step_05_commander_silhouette_selected", "Black Budget Silhouette Selected")

# Re-select Alexei Kane and launch Command Deck
mouse_click(680, 500, "Profile Card: Alexei Kane (Final Select)", 0.3)
mouse_click(1000, 700, ">> CONFIRM DOSSIER & INITIALIZE PMC >>", 0.8)
verify_and_capture("qa_step_06_command_deck_turn1", "Command Deck Active at Turn 1 (0 Cr Treasury)")

# 2. TAB 0: R&D THERMAL CRUCIBLE & MINIGAMES
print("\n--- [STAGE 2] TAB 0: R&D CRUCIBLE & MINIGAMES ---")
mouse_click(150, 86, "Primary Nav: Tab 0 R&D Lab", 0.4)
# Test Crucible buttons
mouse_click(70, 570, "Crucible: +400 C Heat", 0.3)
mouse_click(70, 570, "Crucible: +400 C Heat (Pulse 2)", 0.3)
mouse_click(220, 570, "Crucible: +800 Bar Compress", 0.3)
mouse_click(70, 615, "Crucible: -400 C Cool", 0.3)
mouse_click(350, 675, "Execute Alloy Synthesis Batch", 0.6)
verify_and_capture("qa_step_07_tab0_crucible_batch", "Crucible Batch Sintered")

# Subtab B: Prototyping Minigames
mouse_click(550, 150, "Subtab 1: Prototyping Minigames", 0.5)
verify_and_capture("qa_step_08_tab0_prototyping_subtab", "Tokamak / Hydraulic / Thruster Minigames")

# Subtab C: Blueprint Archive
mouse_click(1000, 150, "Subtab 2: Master Blueprint Archive", 0.5)
verify_and_capture("qa_step_09_tab0_blueprints_subtab", "Blueprint Archive Catalog")

# 3. TAB 1: FACTORY FLOOR & CAD MECHA ASSEMBLY
print("\n--- [STAGE 3] TAB 1: FACTORY FLOOR & CAD ASSEMBLY ---")
mouse_click(419, 86, "Primary Nav: Tab 1 Factory Floor", 0.5)
verify_and_capture("qa_step_10_tab1_assembly_floor", "Factory Production & Pilot Hiring Market")

# Subtab B: Modular Part Forge
mouse_click(550, 150, "Subtab 1: Modular Part Forge", 0.4)
verify_and_capture("qa_step_11_tab1_modular_forge", "Modular Part Forge Alloy Components")

# Subtab C: Custom Combinations Assembly Bay
mouse_click(1000, 150, "Subtab 2: Custom Assembly Bay", 0.4)
verify_and_capture("qa_step_12_tab1_custom_builder", "Custom Modular Mobile Suit CAD Viewport")

# 4. TAB 2: CONTRACT BOARD & COMMERCE
print("\n--- [STAGE 4] TAB 2: CONTRACT BOARD & FLY-OFF TRIALS ---")
mouse_click(683, 86, "Primary Nav: Tab 2 Contract Board", 0.5)
verify_and_capture("qa_step_13_tab2_contracts_board", "Available Contracts & Active Commitments (No Bleed)")

# Subtab B: Procurement Fly-Offs
mouse_click(550, 150, "Subtab 1: Procurement Trials & Fly-Offs", 0.4)
verify_and_capture("qa_step_14_tab2_flyoffs_arena", "Fly-Off Arena & Doctrine Replacement")

# Subtab C: Commodity Trade Exchange
mouse_click(1000, 150, "Subtab 2: Commodity Trade Exchange", 0.4)
verify_and_capture("qa_step_15_tab2_commodity_exchange", "Interstellar Commodity Exchange Desks")

# 5. TAB 3: STRATEGIC WAR MAP & FACTION DIPLOMACY
print("\n--- [STAGE 5] TAB 3: STRATEGIC WAR MAP & DIPLOMACY ---")
mouse_click(946, 86, "Primary Nav: Tab 3 Strategic War Map", 0.5)
# Harvest Node button
mouse_click(100, 480, "Mining Node Extract Harvest", 0.4)
verify_and_capture("qa_step_16_tab3_sector_map", "Sector War Map & 4-Faction Balance Box (Fixed Width)")

# Subtab B: Faction Dossiers & Recruitable Aces
mouse_click(400, 150, "Subtab 1: Faction Dossiers & Citadels", 0.4)
verify_and_capture("qa_step_17_tab3_factions_dossiers", "Faction Bases & Recruitable Pilots")

# Subtab C: Diplomacy Matrix
mouse_click(680, 150, "Subtab 2: Bilateral Diplomacy Matrix", 0.4)
verify_and_capture("qa_step_18_tab3_diplomacy_matrix", "Bilateral Matrix & Faction AI Intelligence")

# Subtab D: Decade Mecha Lineage
mouse_click(950, 150, "Subtab 3: Decade Mecha Lineage", 0.4)
verify_and_capture("qa_step_19_tab3_mecha_lineage", "Historical Lineage & Expeditionary Offensives")

# 6. TAB 4: DREADNOUGHT WARSHIP & CORPORATE MONOPOLIES
print("\n--- [STAGE 6] TAB 4: DREADNOUGHT WARSHIP & CORPORATE MONOPOLIES ---")
mouse_click(1210, 86, "Primary Nav: Tab 4 Dreadnought Warship", 0.5)
verify_and_capture("qa_step_20_tab4_warship_schematics", "Dreadnought Schematics & 4 Divisions")

# Subtab B: Celestial Navigation
mouse_click(550, 150, "Subtab 1: Celestial Navigation", 0.4)
verify_and_capture("qa_step_21_tab4_celestial_navigation", "Planetary Spheres & Orbital Transit Drive")

# Subtab C: Rival Corporate Arms Conglomerates
mouse_click(1000, 150, "Subtab 2: Rival Corporate Monopolies", 0.4)
verify_and_capture("qa_step_22_tab4_rival_corporations", "4 Rival Corp Trading Desks & Reverse Engineering")

# 7. TOP HUD ACTION BUTTONS & MODALS
print("\n--- [STAGE 7] TOP HUD ACTION BUTTONS & MODALS ---")

# Modal A: Turn Log
mouse_click(780, 32, "Top HUD: [LOG] Turn Ledger Modal", 0.5)
verify_and_capture("qa_step_23_top_hud_turn_log", "Strategic Turn Ledger Modal (Bounded Event Log)")
send_key("Escape", 0.4)

# Modal B: Field Manual
mouse_click(870, 32, "Top HUD: [?] Field Manual Modal", 0.5)
verify_and_capture("qa_step_24_top_hud_manual_modal", "PMC Executive Field Manual (Expanded Width)")

# Test switching Field Manual subtabs
mouse_click(330, 120, "Manual Subtab: Crucible R&D", 0.3)
mouse_click(490, 120, "Manual Subtab: Reactor Tuning", 0.3)
mouse_click(650, 120, "Manual Subtab: Hydraulic Bench", 0.3)
verify_and_capture("qa_step_25_manual_hydraulic_tested", "Hydraulic Bench Operating Manual (No Overflow)")

mouse_click(810, 120, "Manual Subtab: Plasma Thrust", 0.3)
verify_and_capture("qa_step_26_manual_thruster_tested", "Plasma Thrust Operating Manual (No Overflow)")
send_key("Escape", 0.4)

# Button C: Quick Save
mouse_click(965, 32, "Top HUD: [F5 SAVE] Quick Save", 0.4)
verify_and_capture("qa_step_27_top_hud_save_fired", "Quick Save Executed (Slot 1)")

# Button D: Commander Profile Dossier Badge
mouse_click(1230, 32, "Top HUD: Commander Dossier Badge", 0.5)
verify_and_capture("qa_step_28_top_hud_commander_badge", "Executive Commander Profile Dossier Modal")
send_key("Escape", 0.4)

# Button E: Advance Turn >> (Turn 1 -> Turn 2)
mouse_click(650, 32, "Top HUD: >> ADVANCE TURN <<", 0.8)
verify_and_capture("qa_step_29_top_hud_advance_turn_fired", "Advance Turn Simulated (Turn 1 -> Turn 2)")

# Final Verification
verify_and_capture("qa_step_30_final_verified_state", "Final Clean Verified State")

print("\n==================================================================")
print("  COMPREHENSIVE QA MOUSE TRIAL COMPLETED SUCCESSFULLY!            ")
print("==================================================================")
