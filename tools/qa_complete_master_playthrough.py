import subprocess
import time
import os
import sys

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

aid = "7bbc3111-e9e2-4ce9-ac27-cdbb483aa140"
out_dir = f"/home/tom/.gemini/antigravity-ide/brain/{aid}"
os.makedirs(out_dir, exist_ok=True)

print("==================================================================")
print("  MECHMAKER CONCEPT - FULL MASTER CAMPAIGN PLAYTHROUGH          ")
print("==================================================================")

lines = run_cmd("wmctrl -l").splitlines()
game_lines = [l for l in lines if "MechMakerConcept" in l]
assert game_lines, "Could not find MechMakerConcept game window!"
win_id = game_lines[0].split()[0]
print(f"Target Window ID: {win_id}")

run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} windowraise {win_id}")
time.sleep(0.5)

info = run_cmd(f"xwininfo -id {win_id}")
win_offset_x = 37
win_offset_y = 34
for line in info.splitlines():
    if "Absolute upper-left X:" in line:
        win_offset_x = int(line.split(":")[1].strip())
    if "Absolute upper-left Y:" in line:
        win_offset_y = int(line.split(":")[1].strip())

print(f"Window display offset: ({win_offset_x}, {win_offset_y})")

def move_and_click(target_x, target_y, label="Button", steps=7, hover_delay=0.18, post_delay=0.28):
    print(f">> [ACTION] {label} at ({target_x}, {target_y})...")
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

def send_key(key, delay=0.3):
    print(f">> [KEY] Pressing {key}...")
    run_cmd(f"DISPLAY=:0 xdotool key {key}")
    time.sleep(delay)

def capture_step(step_name):
    path = os.path.join(out_dir, f"{step_name}.png")
    run_cmd(f"import -window {win_id} {path}")
    print(f"   [SAVED SCREENSHOT] {step_name}.png")

# =========================================================================
# ACT I: PROLOGUE & GENESIS (Turn 1 Setup)
# =========================================================================
print("\n" + "="*60)
print(">>> ACT I: GENESIS & METALLURGY SINTERING (TURN 1)")
print("="*60)

capture_step("master_play_01_command_deck_turn1")

# Ensure on Tab 0: R&D Lab
move_and_click(150, 86, "Tab 0: R&D Lab // Prototyping")

# Sintering Cycle 1: Forge Vanguard Composite Plating
print(">> Sintering Vanguard Composite Plating in Crucible...")
move_and_click(70, 570, "Crucible: +400 C Heat Pulse 1")
move_and_click(70, 570, "Crucible: +400 C Heat Pulse 2")
move_and_click(70, 570, "Crucible: +400 C Heat Pulse 3")
move_and_click(70, 570, "Crucible: +400 C Heat Pulse 4")
move_and_click(70, 570, "Crucible: +400 C Heat Pulse 5")
move_and_click(70, 570, "Crucible: +400 C Heat Pulse 6 (~2400 C)")
move_and_click(350, 675, "Execute Alloy Synthesis Batch", post_delay=0.6)
capture_step("master_play_02_crucible_batch1")

# Explore Metallurgy Codex & Periodic Table
move_and_click(930, 195, "Subview 2: Discovered Alloy Codex")
time.sleep(0.4)
capture_step("master_play_03_alloy_codex")

move_and_click(1150, 195, "Subview 3: 118-Element Periodic Table")
time.sleep(0.4)
capture_step("master_play_04_periodic_table")

move_and_click(730, 195, "Subview 1: Furnace & Batch Preview")
time.sleep(0.3)

# =========================================================================
# ACT II: PROTOTYPING MINIGAMES (Calibration Benchmarks)
# =========================================================================
print("\n" + "="*60)
print(">>> ACT II: PROTOTYPING MINIGAMES (CALIBRATION BENCHMARKS)")
print("="*60)

# Switch to Subtab 1: Prototyping Minigames
move_and_click(550, 150, "Subtab 1: Prototyping Minigames")
time.sleep(0.4)

# 1. Reactor Harmonization Minigame
print(">> Tuning Tokamak Reactor Containment Wave...")
# Adjust frequency +
move_and_click(254, 532, "Frequency (+) Button")
move_and_click(254, 532, "Frequency (+) Button (Second Pulse)")
# Test Harmonic Pulse
move_and_click(950, 590, ">> TEST HARMONIC PULSE <<", post_delay=0.5)
capture_step("master_play_05_reactor_harmonized")

# 2. Hydraulic Limb Stress Alignment Minigame
move_and_click(450, 195, "Minigame 2: Hydraulic Limb Calibration")
time.sleep(0.4)
print(">> Calibrating Biped Hydraulic Actuators...")
# Relieve pressure on selected joint
move_and_click(950, 480, "[-16%] Relieve Joint Pressure")
time.sleep(0.2)
# Lock Spot-Weld
move_and_click(1020, 545, ">> SPOT-WELD JOINT LOCK <<", post_delay=0.4)
capture_step("master_play_06_hydraulics_calibrated")

# 3. Vernier Thruster Resonance Flow Minigame
move_and_click(800, 195, "Minigame 3: Vernier Thruster Resonance")
time.sleep(0.4)
print(">> Igniting Plasma Burn Stages...")
# Commit Stage 1
move_and_click(1000, 530, ">> COMMIT STAGE CALIBRATION PULSE <<", post_delay=0.4)
capture_step("master_play_07_thruster_ignited")

# Inspect Master Blueprint Archive
move_and_click(1000, 150, "Subtab 2: Master Blueprint Archive")
time.sleep(0.4)
capture_step("master_play_08_blueprint_archive")

# =========================================================================
# ACT III: FACTORY FLOOR & MODULAR CAD MECHA ASSEMBLY
# =========================================================================
print("\n" + "="*60)
print(">>> ACT III: FACTORY FLOOR & CAD MECHA ASSEMBLY")
print("="*60)

# Switch to Primary Tab 1: Factory Floor
move_and_click(419, 86, "Primary Tab 1: Factory Floor")
time.sleep(0.4)

# Subtab 1: Modular Part Forge
move_and_click(550, 150, "Subtab 1: Modular Part Forge")
time.sleep(0.4)
capture_step("master_play_09_modular_forge")

# Subtab 2: Custom Assembly Bay
move_and_click(1000, 150, "Subtab 2: Custom Assembly Bay")
time.sleep(0.5)

# Cycle Slot 1 (Head)
move_and_click(360, 260, "Slot 1 (Head Sensors)")
# Cycle Slot 2 (Torso)
move_and_click(360, 344, "Slot 2 (Torso Core)")
# Cycle Slot 5 (Backpack)
move_and_click(360, 596, "Slot 5 (Backpack Boosters)")

# Commission Custom Mobile Suit into Hangar Bay
print(">> Commissioning Custom Mobile Suit into Hangar...")
move_and_click(1050, 480, ">> COMMISSION INTO HANGAR <<", post_delay=0.6)
capture_step("master_play_10_commissioned_mecha")

# Archive to Canonical PMC Blueprints
print(">> Archiving to Canonical Blueprints...")
move_and_click(1050, 528, "[★ SAVE AS PMC CANONICAL BLUEPRINT]", post_delay=0.5)

# Return to Assembly Floor
move_and_click(150, 150, "Subtab 0: Assembly Floor & Personnel")
time.sleep(0.4)
capture_step("master_play_11_assembly_hangar_ready")

# =========================================================================
# ACT IV: CONTRACTS & INTERSTELLAR COMMODITY COMMERCE
# =========================================================================
print("\n" + "="*60)
print(">>> ACT IV: CONTRACTS & INTERSTELLAR COMMERCE")
print("="*60)

# Switch to Primary Tab 2: Contracts & Commerce
move_and_click(683, 86, "Primary Tab 2: Contracts & Commerce")
time.sleep(0.4)

# Accept Available Contract
move_and_click(1080, 240, "Contract 1: [ACCEPT] Button", post_delay=0.5)
capture_step("master_play_12_contract_accepted")

# Subtab 2: Interstellar Commodity Trade Exchange
move_and_click(1000, 150, "Subtab 2: Commodity Trade Exchange")
time.sleep(0.4)

# Trade Partner: Terran Coalition
move_and_click(140, 255, "Trade Hub: Terran Coalition")
time.sleep(0.3)

# Buy 1 Tungsten Mineral
print(">> Purchasing Raw Minerals from Terran Hub...")
move_and_click(876, 385, "BUY 1 Tungsten Mineral", post_delay=0.4)

# Trade Partner: Outer Colonies
move_and_click(334, 255, "Trade Hub: Outer Colonies")
time.sleep(0.3)

# Sell 1 Vanguard Alloy
print(">> Selling Manufactured Vanguard Alloy to Colonies...")
move_and_click(1068, 385, "SELL 1 Vanguard Alloy", post_delay=0.4)
capture_step("master_play_13_commodity_trading")

# =========================================================================
# ACT V: CORPORATE PROCUREMENT FLY-OFF TRIALS
# =========================================================================
print("\n" + "="*60)
print(">>> ACT V: CORPORATE PROCUREMENT FLY-OFFS & DOCTRINE REPLACEMENT")
print("="*60)

# Subtab 1: Procurement Trials & Fly-Off Arena
move_and_click(550, 150, "Subtab 1: Procurement Fly-Off Arena")
time.sleep(0.4)

# Select Target Faction: Outer Colonies
move_and_click(340, 240, "Target Faction: Outer Colonies")
time.sleep(0.3)

# Select Candidate Mecha (Left Box Hangar Suit)
move_and_click(200, 420, "Select Candidate Suit in Hangar")
time.sleep(0.3)

# Apply Emergency Field Refinement: +15% Core Overclock
print(">> Applying Emergency Field Refinement (+15% Core)...")
move_and_click(700, 520, "Refinement: Overclock Reactor")
time.sleep(0.3)

# Advance to Fly-Off Trial Phase 2 / Stress Gauntlet
print(">> Launching Competitive Fly-Off Trial...")
move_and_click(950, 570, "Advance to Fly-Off Phase 2", post_delay=0.6)
capture_step("master_play_14_flyoff_arena_trial")

# =========================================================================
# ACT VI: STRATEGIC SOLAR WAR MAP & DIPLOMACY
# =========================================================================
print("\n" + "="*60)
print(">>> ACT VI: STRATEGIC SOLAR WAR MAP & FACTION DIPLOMACY")
print("="*60)

# Switch to Primary Tab 3: Strategic War Map
move_and_click(946, 86, "Primary Tab 3: Strategic War Map")
time.sleep(0.4)

# Filter Spheres
move_and_click(700, 200, "Sphere Filter: Mars")
time.sleep(0.3)
move_and_click(790, 200, "Sphere Filter: Asteroid Belt")
time.sleep(0.3)
move_and_click(614, 200, "Sphere Filter: All")
time.sleep(0.3)

# Inspect Faction Dossiers & Citadels
move_and_click(400, 150, "Subtab 1: Faction Dossiers & Citadels")
time.sleep(0.4)
move_and_click(220, 200, "Dossier: Outer Colonies")
time.sleep(0.3)
move_and_click(340, 200, "Dossier: Rogue Syndicates")
time.sleep(0.3)
move_and_click(460, 200, "Dossier: Apex Zaibatsu")
time.sleep(0.3)
move_and_click(100, 200, "Dossier: Terran Coalition")
time.sleep(0.3)
capture_step("master_play_15_faction_dossiers")

# Bilateral Diplomacy Matrix
move_and_click(680, 150, "Subtab 2: Bilateral Diplomacy Matrix")
time.sleep(0.4)
capture_step("master_play_16_diplomacy_matrix")

# Decade Mecha Lineage
move_and_click(950, 150, "Subtab 3: Decade Mecha Lineage")
time.sleep(0.4)
capture_step("master_play_17_mecha_lineage")

# =========================================================================
# ACT VII: TACTICAL ISOMETRIC COMBAT DEPLOYMENT (rm_combat)
# =========================================================================
print("\n" + "="*60)
print(">>> ACT VII: TACTICAL ISOMETRIC COMBAT ENGAGEMENT (rm_combat)")
print("="*60)

# Return to Tab 1 (Factory Floor)
move_and_click(419, 86, "Primary Tab 1: Factory Floor")
time.sleep(0.4)

# Click DEPLOY TO TACTICAL COMBAT
print(">> Launching Tactical Sortie into rm_combat...")
move_and_click(1200, 680, ">> DEPLOY TO TACTICAL COMBAT (rm_combat) <<", post_delay=1.0)
capture_step("master_play_18_combat_initial_phase")

# In rm_combat:
# Select Unit A-01
move_and_click(612, 30, "Select Platoon Unit A-01")
time.sleep(0.4)

# Select Unit A-02
move_and_click(680, 30, "Select Platoon Unit A-02")
time.sleep(0.4)

# Call Flagship Orbital Strike Support (Press O or click support button)
print(">> Calling Flagship Orbital Strike Support...")
move_and_click(700, 740, "Flagship Orbital Strike Support", post_delay=0.6)
capture_step("master_play_19_orbital_strike_fired")

# Toggle Autonomous Tactical Auto-Combat (Press A or click auto-combat)
print(">> Engaging Autonomous Platoon Simulation (Auto-Combat)...")
send_key("a", delay=0.5)
capture_step("master_play_20_auto_combat_engaged")

# Let auto-combat simulate tactical rounds
time.sleep(2.5)

# Return from Combat to HQ Terminal (Click Return / Retreat at Top Right)
print(">> Tactical Sortie Complete - Returning to Command Deck...")
move_and_click(1265, 30, "[RETREAT / RETURN TO HQ]", post_delay=0.8)
capture_step("master_play_21_returned_to_hq")

# =========================================================================
# ACT VIII: DREADNOUGHT WARSHIP, RIVALS & CAREER RETIREMENT
# =========================================================================
print("\n" + "="*60)
print(">>> ACT VIII: DREADNOUGHT FLAGSHIP, RIVALS & ENDGAME RETIREMENT")
print("="*60)

# Switch to Primary Tab 4: Dreadnought & Rivals
move_and_click(1210, 86, "Primary Tab 4: Dreadnought Warship")
time.sleep(0.4)
capture_step("master_play_22_dreadnought_flagship")

# Celestial Navigation
move_and_click(550, 150, "Subtab 1: Celestial Navigation")
time.sleep(0.4)

# Rival Corporate Monopolies / Stock Exchange
move_and_click(1000, 150, "Subtab 2: Rival Corporate Monopolies")
time.sleep(0.4)
capture_step("master_play_23_corporate_monopolies")

# Advance Strategic Turns to simulate economic maturation
print(">> Advancing strategic turns to mature operations...")
for t in range(1, 4):
    move_and_click(650, 32, f">> ADVANCE TURN << (Turn {t} -> Turn {t+1})", post_delay=0.8)

# Quick Save Game (F5)
move_and_click(965, 32, "Top HUD: [F5 SAVE] Quick Save")
time.sleep(0.4)

# Inspect Turn Ledger
move_and_click(780, 32, "Top HUD: [LOG] Turn Ledger Modal")
time.sleep(0.5)
capture_step("master_play_24_turn_ledger_mature")
move_and_click(1010, 130, "Turn Ledger: [X CLOSE (ESC)]")
time.sleep(0.3)

# Trigger Career Retirement Dossier ([RETIRE])
print(">> Triggering Career Retirement Dossier ([RETIRE])...")
move_and_click(1060, 32, "Top HUD: [RETIRE] Career Retirement Button", post_delay=0.8)
capture_step("master_play_25_career_retirement_dossier")

# Close Retirement Dossier (ESC or close button)
send_key("Escape", delay=0.6)
print(">> Dismissed Retirement Dossier via ESC - Resuming Command Deck...")
capture_step("master_play_26_command_deck_resumed")

print("\n==================================================================")
print("  FULL MASTER CAMPAIGN PLAYTHROUGH 100% COMPLETED!              ")
print("==================================================================")
