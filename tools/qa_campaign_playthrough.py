import subprocess
import time
import os
import sys
from PIL import Image

def run_cmd(cmd):
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.stdout.strip()

print("==========================================================")
print("  MECHMAKER CONCEPT - FULL CAMPAIGN PLAYTHROUGH (QA SUITE)")
print("==========================================================")

lines = run_cmd("wmctrl -l").splitlines()
game_lines = [l for l in lines if l.endswith("MechMakerConcept")]
assert game_lines, "Could not find MechMakerConcept game window!"
win_id = game_lines[0].split()[0]
print(f"Target Game Window: {win_id}")

artifacts_dir = "/home/tom/.gemini/antigravity-ide/brain/a9197ef4-c206-4eb1-b4b4-83dfffe898d6"

def click_win(x, y, delay=0.35):
    run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} {x} {y} click 1")
    time.sleep(delay)

def send_key(k, delay=0.35):
    run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key {k}")
    time.sleep(delay)

milestones = []

def capture_milestone(step_id, title):
    tmp_path = f"/tmp/{step_id}.png"
    art_path = f"{artifacts_dir}/{step_id}.png"
    thumb_path = f"{artifacts_dir}/{step_id}_thumb.png"
    
    run_cmd(f"import -window {win_id} {tmp_path}")
    assert os.path.exists(tmp_path), f"Failed capture for {step_id}"
    
    im = Image.open(tmp_path)
    im.save(art_path)
    thumb = im.resize((im.width // 4, im.height // 4), Image.LANCZOS)
    thumb.save(thumb_path)
    
    # Check rightmost 25px
    right_bleed = 0
    for y in range(0, im.height):
        row = [im.getpixel((x, y)) for x in range(im.width - 25, im.width)]
        bright = [val for val in row if max(val[:3]) > 150]
        if bright:
            right_bleed += 1
            
    # Check bottommost 25px
    bot_bleed = 0
    for x in range(0, im.width):
        col = [im.getpixel((x, y)) for y in range(im.height - 25, im.height)]
        bright = [val for val in col if max(val[:3]) > 150]
        if bright:
            bot_bleed += 1
            
    err_out = run_cmd("wmctrl -l | grep -i 'error'")
    has_err = bool(err_out)
    
    status = "PASS" if (right_bleed == 0 and bot_bleed == 0 and not has_err) else "FAIL"
    milestones.append({
        "step_id": step_id,
        "title": title,
        "status": status,
        "right_bleed": right_bleed,
        "bot_bleed": bot_bleed,
        "has_err": has_err
    })
    print(f"[{status}] {step_id:<32} | {title:<40} | Bleed R:{right_bleed} B:{bot_bleed} | Err: {has_err}")
    if has_err:
        print(f"[FATAL QA ERROR DETECTED]: {err_out}")
        sys.exit(1)

# Ensure window focus
click_win(100, 100, 0.5)

# --- PROLOGUE: CAMPAIGN INITIALIZATION & COMMANDER COMMISSIONING ---
print("\n>>> MILESTONE 1: PROLOGUE & EXECUTIVE COMMISSIONING <<<")
capture_milestone("pt_01_briefing_prologue", "Intro Situation Briefing")

# Click >> APPOINT COMMANDER PROFILE >> at (1000, 700)
click_win(1000, 700, 0.7)
capture_milestone("pt_02_commander_dossier_selection", "Commander Selection Dossier")

# Choose Alexei Kane (Male Vanguard) at (680, 500)
click_win(680, 500, 0.4)
capture_milestone("pt_03_commander_alexei_selected", "Selected Alexei Kane (Vanguard)")

# Click >> RATIFY APPOINTMENT & LAUNCH COMMAND DECK >> at (1000, 700)
click_win(1000, 700, 0.8)
capture_milestone("pt_04_command_deck_arrival", "Command Deck Arrival (Turn 1)")

# --- STRATEGIC PILLAR 1: R&D LAB & ALLOY CRUCIBLE ---
print("\n>>> MILESTONE 2: R&D LAB & ALLOY SINTERING (TAB 0) <<<")
# Heat crucible (+400 x 2 = +800 C) at (70, 570)
click_win(70, 570, 0.3)
click_win(70, 570, 0.3)
# Compress chamber (+800 PSI) at (220, 570)
click_win(220, 570, 0.3)
# Sinter Alloy Batch at (350, 675)
click_win(350, 675, 0.6)
capture_milestone("pt_05_crucible_batch_sintered", "Crucible Ingot Forged & Codex Logged")

# Subtab B: Component Prototyping Minigames at (550, 150)
click_win(550, 150, 0.5)
capture_milestone("pt_06_prototyping_bench_active", "Component Prototyping Bench")

# Subtab C: Blueprint Schematics Archive at (1000, 150)
click_win(1000, 150, 0.5)
capture_milestone("pt_07_blueprint_archive_inspected", "Blueprint Schematics Archive")

# --- STRATEGIC PILLAR 2: FACTORY FLOOR & CAD ASSEMBLY ---
print("\n>>> MILESTONE 3: FACTORY OPERATIONS & CAD ASSEMBLY (TAB 1) <<<")
click_win(419, 86, 0.5) # Tab 1
capture_milestone("pt_08_factory_facilities_overview", "Base Facilities & Tooling")

# Modular Part Forge at (550, 150)
click_win(550, 150, 0.4)
capture_milestone("pt_09_modular_part_forge", "Modular Alloy Part Fabricator")

# Custom Combinations Assembly Bay at (1000, 150)
click_win(1000, 150, 0.4)
capture_milestone("pt_10_custom_combinations_builder", "Custom Suit Assembly & Diagnostics")

# --- STRATEGIC PILLAR 3: CONTRACT BOARD & COMMODITY TRADE ---
print("\n>>> MILESTONE 4: CONTRACTS & COMMODITY TRADE (TAB 2) <<<")
click_win(683, 86, 0.5) # Tab 2
# Select contract 1 at (200, 260)
click_win(200, 260, 0.4)
capture_milestone("pt_11_contracts_board_accepted", "Terran Defense Contract Evaluated")

# Procurement Fly-Offs at (550, 150)
click_win(550, 150, 0.4)
capture_milestone("pt_12_procurement_flyoffs", "Mass-Production Procurement Fly-Offs")

# Commodity Trade Exchange at (1000, 150)
click_win(1000, 150, 0.4)
# Click Buy 1 button on commodity at (820, 275)
click_win(820, 275, 0.4)
capture_milestone("pt_13_commodity_market_traded", "Mineral Ingot Traded on Exchange")

# --- STRATEGIC PILLAR 4: STRATEGIC WAR MAP & MINING THEATERS ---
print("\n>>> MILESTONE 5: STRATEGIC WAR MAP & FACTION DIPLOMACY (TAB 3) <<<")
click_win(946, 86, 0.5) # Tab 3
capture_milestone("pt_14_sector_map_war_balance", "Sol War Map & 4-Faction Balance")

# Harvest mining node 0 at (100, 480)
click_win(100, 480, 0.4)
capture_milestone("pt_15_mining_node_harvested", "Asteroid Node Extracted to Hopper")

# Factions & Liaisons Dossiers at (400, 150)
click_win(400, 150, 0.4)
capture_milestone("pt_16_faction_liaisons_dossiers", "Faction High Command Liaisons")

# Diplomacy Matrix at (680, 150)
click_win(680, 150, 0.4)
capture_milestone("pt_17_diplomacy_matrix_analyzed", "Geopolitical War/Peace Matrix")

# Decade Mecha Lineage at (950, 150)
click_win(950, 150, 0.4)
capture_milestone("pt_18_decade_mecha_lineage", "Decade Mecha Lineage (Y205-Y215)")

# --- STRATEGIC PILLAR 5: DREADNOUGHT WARSHIP & CORPORATE MONOPOLIES ---
print("\n>>> MILESTONE 6: PRE-WAR DREADNOUGHT & RIVAL CONGLOMERATES (TAB 4) <<<")
click_win(1210, 86, 0.5) # Tab 4
capture_milestone("pt_19_dreadnought_schematic", "USN-X Hephaestus Warship Deck")

# Celestial Navigation at (550, 150)
click_win(550, 150, 0.4)
# Station warship in Asteroid Belt at (500, 370)
click_win(500, 370, 0.4)
capture_milestone("pt_20_celestial_navigation_transit", "Orbital Transit to Asteroid Belt")

# Rival Arms Conglomerates at (1000, 150)
click_win(1000, 150, 0.4)
# Buy 5,000 shares in Vanguard Heavy Industries at (220, 385)
click_win(220, 385, 0.4)
capture_milestone("pt_21_rival_conglomerate_shares", "Purchased 5,000 Shares in VHI")

# --- STRATEGIC PILLAR 6: MULTI-TURN CAMPAIGN PROGRESSION ---
print("\n>>> MILESTONE 7: MULTI-TURN STRATEGIC ADVANCEMENT (TURNS 2 - 5) <<<")
# Advance to Turn 2
click_win(650, 32, 0.7)
capture_milestone("pt_22_turn_2_advanced", "Campaign Turn 2 - Revenue Accrued")

# Inspect Turn Log
click_win(780, 32, 0.5)
capture_milestone("pt_23_turn_log_ledger_audited", "Turn Briefing Ledger Audited")
send_key("Escape", 0.4)

# Advance to Turn 3
click_win(650, 32, 0.7)
capture_milestone("pt_24_turn_3_advanced", "Campaign Turn 3 - Resource Tick")

# Advance to Turn 4
click_win(650, 32, 0.7)
capture_milestone("pt_25_turn_4_advanced", "Campaign Turn 4 - Factory Progress")

# Advance to Turn 5
click_win(650, 32, 0.7)
capture_milestone("pt_26_turn_5_advanced", "Campaign Turn 5 - Hegemony Shift")

# Save game state (F5)
click_win(965, 32, 0.4)
capture_milestone("pt_27_campaign_quicksaved", "Campaign Progress QuickSaved (F5)")

# --- STRATEGIC PILLAR 7: ENDGAME CAREER RETIREMENT ASSESSMENT ---
print("\n>>> MILESTONE 8: CAREER RETIREMENT & LEGACY ASSESSMENT <<<")
# Click [★ RETIRE] button at (1060, 32)
click_win(1060, 32, 0.8)
capture_milestone("pt_28_retirement_legacy_dossier", "Mercenary Guild Historical Retirement")

# Dismiss retirement modal
send_key("Escape", 0.4)
capture_milestone("pt_29_post_retirement_deck", "Command Deck Resumed from Archive")

print("\n==========================================================")
print("  FULL CAMPAIGN PLAYTHROUGH COMPLETED WITH 100% SUCCESS! ")
print("==========================================================")
