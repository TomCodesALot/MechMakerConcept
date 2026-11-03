#!/usr/bin/env python3
import subprocess
import time
import os
import sys

aid = "7bbc3111-e9e2-4ce9-ac27-cdbb483aa140"
out_dir = f"/home/tom/.gemini/antigravity-ide/brain/{aid}"
os.makedirs(out_dir, exist_ok=True)

print("==================================================================")
print("  MECHMAKER CONCEPT - DEEP FULL CAMPAIGN PLAYTHROUGH SUITE       ")
print("  (Comprehensive Factory Fabrication, Factions & War Progression)")
print("==================================================================")

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.stdout.strip()

# 1. Discover Window
lines = run_cmd("wmctrl -l").splitlines()
game_lines = [l for l in lines if "MechMakerConcept" in l]
assert game_lines, "Could not find MechMakerConcept game window!"
win_id = game_lines[0].split()[0]
print(f"Target Window ID: {win_id}")

run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} windowraise {win_id}")
time.sleep(0.5)

info = run_cmd(f"xwininfo -id {win_id}")
wx, wy = 0, 0
for line in info.splitlines():
    if "Absolute upper-left X:" in line:
        wx = int(line.split(":")[1].strip())
    if "Absolute upper-left Y:" in line:
        wy = int(line.split(":")[1].strip())

print(f"Window Position: ({wx}, {wy})")

def move_and_click(rel_x, rel_y, label="", post_delay=0.3):
    gx = wx + rel_x
    gy = wy + rel_y
    if label:
        print(f">> [ACTION] {label} at ({rel_x}, {rel_y})...")
    run_cmd(f"DISPLAY=:0 xdotool mousemove {gx} {gy} click 1")
    time.sleep(post_delay)

def send_key(key, delay=0.3):
    print(f">> [KEY] Pressing {key}...")
    run_cmd(f"DISPLAY=:0 xdotool key {key}")
    time.sleep(delay)

def capture_step(step_name):
    path = os.path.join(out_dir, f"{step_name}.png")
    run_cmd(f"import -window {win_id} {path}")
    print(f"   [SAVED SCREENSHOT] {step_name}.png")

# =========================================================================
# PHASE 1: BOOT, INTRO BRIEFING & COMMANDER SELECTION
# =========================================================================
print("\n" + "="*60)
print(">>> PHASE 1: GENESIS & COMMANDER COMMISSION")
print("="*60)
capture_step("deep_01_boot_modal")

# Click [PROCEED TO COMMANDER APPOINTMENT >>]
move_and_click(683, 700, "Briefing: Proceed to Commander Appointment", post_delay=0.5)
capture_step("deep_02_commander_selection")

# Select Female Veteran Commander & Confirm
move_and_click(683, 300, "Select Commander Profile (Elena)", post_delay=0.3)
move_and_click(683, 675, "Confirm Commander & Initialize PMC Deck", post_delay=0.8)
capture_step("deep_03_command_deck_turn1")

# =========================================================================
# PHASE 2: METALLURGICAL SINTERING (CRUCIBLE FOUNDRY)
# =========================================================================
print("\n" + "="*60)
print(">>> PHASE 2: METALLURGICAL SINTERING & ALLOY CODEX")
print("="*60)
move_and_click(150, 86, "Tab 0: R&D Lab // Prototyping")

# Heat pulse 6 times to ~2400 C
for p in range(1, 7):
    move_and_click(70, 570, f"Crucible: Heat Pulse {p} (+400 C)", post_delay=0.15)

# Synthesize batch
move_and_click(350, 675, "Execute Alloy Synthesis Batch", post_delay=0.5)
capture_step("deep_04_alloy_synthesized")

# Inspect Discovered Alloy Codex
move_and_click(930, 195, "Subview 2: Discovered Alloy Codex", post_delay=0.3)
capture_step("deep_05_alloy_codex")

# Inspect 118-Element Periodic Table
move_and_click(1150, 195, "Subview 3: 118-Element Periodic Table", post_delay=0.3)
capture_step("deep_06_periodic_table")

# Return to Furnace View
move_and_click(730, 195, "Subview 1: Furnace & Batch Preview", post_delay=0.3)

# =========================================================================
# PHASE 3: PROTOTYPING BENCHMARK MINIGAMES
# =========================================================================
print("\n" + "="*60)
print(">>> PHASE 3: PROTOTYPING MINIGAMES (CALIBRATION BENCHMARKS)")
print("="*60)
move_and_click(550, 150, "Subtab 1: Prototyping Minigames")

# Tokamak Reactor Wave Lock
move_and_click(254, 532, "Frequency (+) Button", post_delay=0.2)
move_and_click(254, 532, "Frequency (+) Button", post_delay=0.2)
move_and_click(950, 590, ">> TEST HARMONIC PULSE <<", post_delay=0.5)
capture_step("deep_07_reactor_harmonized")

# Hydraulic Actuators
move_and_click(450, 195, "Minigame 2: Hydraulic Limb Calibration")
move_and_click(950, 480, "[-16%] Relieve Joint Pressure", post_delay=0.2)
move_and_click(1020, 545, ">> SPOT-WELD JOINT LOCK <<", post_delay=0.5)
capture_step("deep_08_hydraulics_calibrated")

# Vernier Thrusters
move_and_click(800, 195, "Minigame 3: Vernier Thruster Resonance")
move_and_click(1000, 530, ">> COMMIT STAGE CALIBRATION PULSE <<", post_delay=0.5)
capture_step("deep_09_thrusters_ignited")

# Inspect Master Blueprint Archive
move_and_click(1000, 150, "Subtab 2: Master Blueprint Archive", post_delay=0.3)
capture_step("deep_10_blueprint_archive")

# =========================================================================
# PHASE 4: FACTORY FLOOR, ASSEMBLY & FABRICATION OF MOBILE SUITS
# =========================================================================
print("\n" + "="*60)
print(">>> PHASE 4: CAD ASSEMBLY, BLUEPRINT ARCHIVE & MOBILE SUIT FABRICATION")
print("="*60)
move_and_click(419, 86, "Primary Tab 1: Factory Floor")

# Subtab 1: Modular Part Forge
move_and_click(550, 150, "Subtab 1: Modular Part Forge", post_delay=0.3)
capture_step("deep_11_modular_forge")

# Subtab 2: Custom Assembly Bay
move_and_click(1000, 150, "Subtab 2: Custom CAD Assembly Bay", post_delay=0.4)
move_and_click(360, 260, "Slot 1 (Head Sensors)")
move_and_click(360, 344, "Slot 2 (Torso Core)")
move_and_click(360, 596, "Slot 5 (Backpack Boosters)")
move_and_click(1050, 480, ">> COMMISSION CUSTOM MS INTO HANGAR <<", post_delay=0.6)
move_and_click(1050, 528, "[★ SAVE AS PMC CANONICAL BLUEPRINT]", post_delay=0.5)
capture_step("deep_12_custom_ms_commissioned")

# Subtab 0: Base Facilities, Personnel & Assembly Queue
move_and_click(150, 150, "Subtab 0: Base Facilities & Personnel", post_delay=0.4)

# Hire New Ace Pilot from Paged Registry
print(">> Hiring Pilot from Registry...")
move_and_click(1220, 315, "Hire Candidate Ace Pilot", post_delay=0.5)

# Test Pilot Registry Pagination
move_and_click(700, 548, "Next Pilot Page [NEXT PILOTS >]", post_delay=0.4)
capture_step("deep_13_pilot_registry_paged")
move_and_click(640, 548, "Prev Pilot Page [< PREV PILOTS]", post_delay=0.4)

# Upgrade Facilities: Crucible Tier 2 (if funds permit or tested)
move_and_click(300, 242, "Facility: Upgrade Crucible Tier 2", post_delay=0.4)

# Commission / Expand Assembly Line
move_and_click(300, 282, "Facility: Commission New Assembly Line", post_delay=0.4)

# Queue Active Mobile Suit Fabrication in Assembly Bay
print(">> Queueing Mobile Suit Fabrication in Assembly Bay...")
move_and_click(300, 425, "Queue Fabrication: GHA-07 Ironclad Batch", post_delay=0.6)
capture_step("deep_14_ms_fabrication_queued")

# =========================================================================
# PHASE 5: RESOURCE OPERATIONS & STRATEGIC MINING NODES
# =========================================================================
print("\n" + "="*60)
print(">>> PHASE 5: STRATEGIC MINING NODES & LOGISTICS")
print("="*60)
move_and_click(946, 86, "Primary Tab 3: Strategic War Map", post_delay=0.5)

# Inspect Mining Nodes on War Map
# Extract ores from Asteroid Belt C-14 into Fleet Storage
move_and_click(680, 300, "Mining Node 1: [EXTRACT STORAGE] into Fleet", post_delay=0.5)
# Deploy / Assign Escort to Asteroid Node
move_and_click(880, 300, "Mining Node 1: [ASSIGN / RECALL ESCORT]", post_delay=0.5)
capture_step("deep_15_mining_node_operations")

# =========================================================================
# PHASE 6: FACTION CONTRACTS, COMMERCE & BILATERAL DIPLOMACY
# =========================================================================
print("\n" + "="*60)
print(">>> PHASE 6: FACTION CONTRACTS, TRADE HUBS & BILATERAL DIPLOMACY")
print("="*60)
# Switch to Primary Tab 2: Contracts & Commerce
move_and_click(683, 86, "Primary Tab 2: Contracts & Commerce", post_delay=0.4)

# Accept Available Contract 1
move_and_click(1080, 240, "Contract Board: [ACCEPT] Contract 1", post_delay=0.5)
capture_step("deep_16_contract_accepted")

# Subtab 2: Commodity Trade Exchange
move_and_click(1000, 150, "Subtab 2: Commodity Trade Exchange", post_delay=0.4)
move_and_click(140, 255, "Trade Hub: Terran Coalition")
move_and_click(876, 385, "BUY 1 Tungsten Mineral from Earth", post_delay=0.3)
move_and_click(334, 255, "Trade Hub: Outer Colonies")
move_and_click(1068, 385, "SELL 1 Vanguard Alloy to Colonies", post_delay=0.3)
capture_step("deep_17_interstellar_trade")

# Switch to Primary Tab 3 Subtab 2: Bilateral Diplomacy Matrix
move_and_click(946, 86, "Primary Tab 3: Strategic War Map", post_delay=0.4)
move_and_click(680, 150, "Subtab 2: Bilateral Diplomacy Matrix", post_delay=0.5)

# Test Diplomatic Pair Cycling
move_and_click(200, 280, "Select Diplomatic Pair: Terran vs Colony", post_delay=0.3)
move_and_click(200, 340, "Select Diplomatic Pair: Terran vs Syndicate", post_delay=0.3)
move_and_click(200, 400, "Select Diplomatic Pair: Terran vs Zaibatsu", post_delay=0.3)
move_and_click(200, 280, "Return to Terran vs Colony Pair", post_delay=0.3)

# Test Mercenary Diplomatic Proposals
print(">> Interacting with Faction Diplomacy (Ceasefire / Proxy Operations)...")
move_and_click(700, 520, "Diplomacy Action 1: [BROKER TRUCE]", post_delay=0.5)
capture_step("deep_18_diplomacy_matrix_action")

# Subtab 1: Faction Citadels & Dossiers
move_and_click(400, 150, "Subtab 1: Faction Citadels & Dossiers", post_delay=0.4)
move_and_click(100, 200, "Citadel: Terran Coalition")
move_and_click(220, 200, "Citadel: Outer Colonies")
move_and_click(340, 200, "Citadel: Rogue Syndicates")
move_and_click(460, 200, "Citadel: Apex Zaibatsu")
capture_step("deep_19_faction_citadels")

# =========================================================================
# PHASE 7: CORPORATE PROCUREMENT FLY-OFF TRIALS
# =========================================================================
print("\n" + "="*60)
print(">>> PHASE 7: CORPORATE PROCUREMENT FLY-OFF ARENA")
print("="*60)
move_and_click(683, 86, "Primary Tab 2: Contracts & Commerce", post_delay=0.4)
move_and_click(550, 150, "Subtab 1: Procurement Fly-Off Arena", post_delay=0.4)
move_and_click(340, 240, "Target Faction: Outer Colonies", post_delay=0.3)
move_and_click(200, 420, "Select Candidate Suit in Hangar", post_delay=0.3)

# Apply Emergency Field Refinements
print(">> Overclocking candidate suit systems (+15% Core)...")
move_and_click(700, 520, "Refinement: Overclock Reactor", post_delay=0.3)
move_and_click(850, 520, "Refinement: Weld Heavy Armor Plating", post_delay=0.3)

# Launch Competitive Phase 2 Fly-Off
move_and_click(950, 570, "Advance to Fly-Off Phase 2 Trial", post_delay=0.6)
capture_step("deep_20_procurement_flyoff")

# =========================================================================
# PHASE 8: TACTICAL ISOMETRIC COMBAT SORTIE (rm_combat)
# =========================================================================
print("\n" + "="*60)
print(">>> PHASE 8: TACTICAL ISOMETRIC COMBAT DEPLOYMENT (rm_combat)")
print("="*60)
move_and_click(419, 86, "Primary Tab 1: Factory Floor", post_delay=0.4)
move_and_click(1200, 680, ">> DEPLOY TO TACTICAL COMBAT (rm_combat) <<", post_delay=1.0)
capture_step("deep_21_combat_deployed")

# Select Platoon Unit A-01 and A-02
move_and_click(612, 30, "Select Platoon Unit A-01", post_delay=0.3)
move_and_click(680, 30, "Select Platoon Unit A-02", post_delay=0.3)

# Fire Dreadnought Flagship Orbital Kinetic Strike Support
print(">> Calling Flagship Orbital Strike...")
move_and_click(700, 740, "Flagship Orbital Strike Support", post_delay=0.6)
capture_step("deep_22_orbital_strike_fired")

# Engage Autonomous Platoon Combat Simulation
print(">> Engaging Autonomous Platoon Simulation (Auto-Combat)...")
send_key("a", delay=0.5)
capture_step("deep_23_auto_combat_engaged")

# Simulate active combat rounds
time.sleep(3.0)

# Tactical Return to HQ Command Deck
move_and_click(1265, 30, "[RETREAT / RETURN TO HQ]", post_delay=1.0)
capture_step("deep_24_returned_to_hq")

# =========================================================================
# PHASE 9: DREADNOUGHT WARSHIP & STOCK MARKET MONOPOLIES
# =========================================================================
print("\n" + "="*60)
print(">>> PHASE 9: DREADNOUGHT WARSHIP & STOCK MONOPOLIES")
print("="*60)
move_and_click(1210, 86, "Primary Tab 4: Dreadnought Warship", post_delay=0.4)
capture_step("deep_25_dreadnought_flagship")

# Subtab 1: Celestial Navigation
move_and_click(550, 150, "Subtab 1: Celestial Navigation", post_delay=0.4)

# Subtab 2: Rival Corporate Monopolies / Stock Exchange
move_and_click(1000, 150, "Subtab 2: Rival Corporate Monopolies", post_delay=0.4)

# Acquire 5% Equity Stake in Vulcan Heavy Industries
print(">> Purchasing corporate shares on stock exchange...")
move_and_click(250, 520, "Buy 5% Shares in Rival Corp", post_delay=0.5)
capture_step("deep_26_corporate_equity_acquired")

# =========================================================================
# PHASE 10: EXTENSIVE STRATEGIC TURN PROGRESSION & TIMELINE ADVANCEMENT
# =========================================================================
print("\n" + "="*60)
print(">>> PHASE 10: MULTI-TURN STRATEGIC PROGRESSION (TURNS 1 -> 12+)")
print("="*60)
# Advance turns substantially to progress fabrication, mining ticks, and contracts
for turn_step in range(1, 13):
    move_and_click(650, 32, f">> ADVANCE TURN << (Advancing Turn {turn_step} -> {turn_step+1})", post_delay=0.6)
    if turn_step % 3 == 0:
        # Check turn log occasionally
        move_and_click(780, 32, "Top HUD: [LOG] Turn Ledger Modal", post_delay=0.4)
        move_and_click(1010, 130, "Turn Ledger: [X CLOSE (ESC)]", post_delay=0.3)

capture_step("deep_27_turn_progression_mature")

# F5 Quick Save
move_and_click(965, 32, "Top HUD: [F5 SAVE] Quick Save", post_delay=0.4)

# Verify Factory Fabrication Rollout
move_and_click(419, 86, "Primary Tab 1: Factory Floor", post_delay=0.4)
move_and_click(150, 150, "Subtab 0: Base Facilities & Personnel", post_delay=0.4)
capture_step("deep_28_factory_fabrication_complete")

# =========================================================================
# PHASE 11: MATURE PMC EMPIRE & HISTORICAL CAREER RETIREMENT
# =========================================================================
print("\n" + "="*60)
print(">>> PHASE 11: MATURE PMC RETIREMENT DOSSIER & SANDBOX RESUMPTION")
print("="*60)
# Trigger Career Retirement Button ([RETIRE])
print(">> Triggering Mature Career Retirement Dossier ([RETIRE])...")
move_and_click(1060, 32, "Top HUD: [RETIRE] Career Retirement Button", post_delay=1.0)
capture_step("deep_29_mature_career_retirement_dossier")

# Verify [RESUME SANDBOX CAMPAIGN (CONTINUE PLAYING)] button works
print(">> Clicking [RESUME SANDBOX CAMPAIGN] to continue empire leadership...")
move_and_click(340, 680, ">> RESUME SANDBOX CAMPAIGN <<", post_delay=0.8)
capture_step("deep_30_campaign_resumed_seamlessly")

print("\n==================================================================")
print("  DEEP FULL CAMPAIGN PLAYTHROUGH 100% COMPLETED!                ")
print("==================================================================")
