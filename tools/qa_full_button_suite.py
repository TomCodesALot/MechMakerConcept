import subprocess
import time
import os
from PIL import Image

def run_cmd(cmd):
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.stdout.strip()

print("==========================================================")
print("  MECHMAKER CONCEPT - COMPREHENSIVE QA BUTTON & BLEED SUITE ")
print("==========================================================")

# 1. Identify window
lines = run_cmd("wmctrl -l").splitlines()
game_lines = [l for l in lines if l.endswith("MechMakerConcept")]
assert game_lines, "Could not find MechMakerConcept game window!"
win_id = game_lines[0].split()[0]
print(f"Target Game Window: {win_id}")

artifacts_dir = "/home/tom/.gemini/antigravity-ide/brain/a9197ef4-c206-4eb1-b4b4-83dfffe898d6"

def click_win(x, y, delay=0.3):
    run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} mousemove --window {win_id} {x} {y} click 1")
    time.sleep(delay)

def send_key(k, delay=0.3):
    run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} key {k}")
    time.sleep(delay)

def capture_and_verify(step_name):
    tmp_path = f"/tmp/{step_name}.png"
    art_path = f"{artifacts_dir}/{step_name}.png"
    thumb_path = f"{artifacts_dir}/{step_name}_thumb.png"
    
    # Direct window capture at native 1366x768
    run_cmd(f"import -window {win_id} {tmp_path}")
    assert os.path.exists(tmp_path), f"Failed to capture {step_name}"
    
    im = Image.open(tmp_path)
    im.save(art_path)
    thumb = im.resize((im.width // 4, im.height // 4), Image.LANCZOS)
    thumb.save(thumb_path)
    
    # Verify zero text bleeding on rightmost 25px and bottommost 25px
    right_bleed = 0
    for y in range(0, im.height):
        row = [im.getpixel((x, y)) for x in range(im.width - 25, im.width)]
        bright = [val for val in row if max(val[:3]) > 150]
        if bright:
            right_bleed += 1
            
    bot_bleed = 0
    for x in range(0, im.width):
        col = [im.getpixel((x, y)) for y in range(im.height - 25, im.height)]
        bright = [val for val in col if max(val[:3]) > 150]
        if bright:
            bot_bleed += 1
            
    # Check error dialogs
    err_out = run_cmd("wmctrl -l | grep -i 'error'")
    has_err = bool(err_out)
    
    status = "PASS" if (right_bleed == 0 and bot_bleed == 0 and not has_err) else "WARN"
    print(f"[{status}] {step_name:<32} | Right Bleed rows: {right_bleed:2d} | Bottom Bleed cols: {bot_bleed:2d} | Errors: {has_err}")
    return right_bleed == 0 and bot_bleed == 0 and not has_err

# --- STEP 1: SITUATION BRIEFING MODAL (PAGE 0) ---
print("\n--- [PHASE 1] Situation Briefing & Commander Appointment ---")
click_win(100, 100) # Ensure window focus
capture_and_verify("qa_btn_01_briefing_page0")

# Click ">> APPOINT COMMANDER PROFILE >>" at (1000, 700)
click_win(1000, 700, 0.6)
capture_and_verify("qa_btn_02_commander_page1")

# Click Profile 2 (Male: Alexei Kane) at (680, 500)
click_win(680, 500, 0.4)
capture_and_verify("qa_btn_03_commander_male_selected")

# Click Profile 3 (Female: Morgan Vance) at (1050, 500)
click_win(1050, 500, 0.4)
capture_and_verify("qa_btn_04_commander_female_selected")

# Click ">> RATIFY APPOINTMENT & LAUNCH COMMAND DECK >>" at (1000, 700)
click_win(1000, 700, 0.8)
capture_and_verify("qa_btn_05_deck_tab0_crucible")

# --- STEP 2: TAB 0 CRUCIBLE CONTROLS ---
print("\n--- [PHASE 2] Tab 0: Crucible R&D Lab & Minigames ---")
# Click +400 HEAT button at (70, 570)
click_win(70, 570, 0.3)
click_win(70, 570, 0.3)
# Click +800 COMPRESS button at (220, 570)
click_win(220, 570, 0.3)
# Click -400 COOL button at (70, 615)
click_win(70, 615, 0.3)
# Click EXECUTE ALLOY SYNTHESIS BATCH at (350, 675)
click_win(350, 675, 0.6)
capture_and_verify("qa_btn_06_tab0_synthesis_fired")

# Switch Subtab B: Component Prototyping Minigames at (550, 150)
click_win(550, 150, 0.5)
capture_and_verify("qa_btn_07_tab0_prototyping_subtab")

# Switch Subtab C: Blueprint Archive at (1000, 150)
click_win(1000, 150, 0.5)
capture_and_verify("qa_btn_08_tab0_blueprints_subtab")

# --- STEP 3: TAB 1 FACTORY FLOOR & CAD ASSEMBLY ---
print("\n--- [PHASE 3] Tab 1: Factory Floor & CAD Assembly ---")
# Click Tab 1 on primary nav bar: x=419, y=86
click_win(419, 86, 0.5)
capture_and_verify("qa_btn_09_tab1_assembly_floor")

# Click Subtab B: Modular Part Forge at (550, 150)
click_win(550, 150, 0.4)
capture_and_verify("qa_btn_10_tab1_modular_forge")

# Click Subtab C: Custom Combinations Assembly Bay at (1000, 150)
click_win(1000, 150, 0.4)
capture_and_verify("qa_btn_11_tab1_custom_builder")

# --- STEP 4: TAB 2 CONTRACT BOARD & COMMERCE ---
print("\n--- [PHASE 4] Tab 2: Contract Board & Commerce ---")
# Click Tab 2 on primary nav bar: x=683, y=86
click_win(683, 86, 0.5)
capture_and_verify("qa_btn_12_tab2_contracts_board")

# Click Subtab B: Procurement Fly-Offs at (550, 150)
click_win(550, 150, 0.4)
capture_and_verify("qa_btn_13_tab2_procurement_trials")

# Click Subtab C: Commodity Trade Exchange at (1000, 150)
click_win(1000, 150, 0.4)
capture_and_verify("qa_btn_14_tab2_commodity_exchange")

# --- STEP 5: TAB 3 STRATEGIC WAR MAP ---
print("\n--- [PHASE 5] Tab 3: Strategic War Map & Faction Diplomacy ---")
# Click Tab 3 on primary nav bar: x=946, y=86
click_win(946, 86, 0.5)
capture_and_verify("qa_btn_15_tab3_sector_war_map")

# Click Mining Node Extract at (100, 480)
click_win(100, 480, 0.4)
capture_and_verify("qa_btn_16_tab3_mining_harvested")

# Click Subtab B: Factions & Liaisons at (400, 150)
click_win(400, 150, 0.4)
capture_and_verify("qa_btn_17_tab3_factions_dossiers")

# Click Subtab C: Diplomacy Matrix at (680, 150)
click_win(680, 150, 0.4)
capture_and_verify("qa_btn_18_tab3_diplomacy_matrix")

# Click Subtab D: Decade Mecha Lineage at (950, 150)
click_win(950, 150, 0.4)
capture_and_verify("qa_btn_19_tab3_mecha_lineage")

# --- STEP 6: TAB 4 DREADNOUGHT WARSHIP & CORPORATE RIVALS ---
print("\n--- [PHASE 6] Tab 4: Dreadnought Warship & Corporate Monopolies ---")
# Click Tab 4 on primary nav bar: x=1210, y=86
click_win(1210, 86, 0.5)
capture_and_verify("qa_btn_20_tab4_warship_schematics")

# Click Subtab B: Celestial Navigation at (550, 150)
click_win(550, 150, 0.4)
capture_and_verify("qa_btn_21_tab4_celestial_navigation")

# Click Subtab C: Rival Corporate Arms Manufacturers at (1000, 150)
click_win(1000, 150, 0.4)
capture_and_verify("qa_btn_22_tab4_rival_corporations")

# --- STEP 7: TOP HUD ACTION BUTTONS ---
print("\n--- [PHASE 7] Top HUD Action Buttons & Modals ---")

# 1. Turn Log Modal: Click [LOG] button at (780, 32)
click_win(780, 32, 0.5)
capture_and_verify("qa_btn_23_top_hud_turn_log")
# Close modal with ESC
send_key("Escape", 0.4)

# 2. Field Manual Modal: Click [?] MANUAL button at (870, 32)
click_win(870, 32, 0.5)
capture_and_verify("qa_btn_24_top_hud_manual_modal")
# Test switching manual tab to CRUCIBLE at (330, 120)
click_win(330, 120, 0.3)
# Test switching manual tab to REACTOR at (490, 120)
click_win(490, 120, 0.3)
# Test switching manual tab to HYDRAULIC at (650, 120)
click_win(650, 120, 0.3)
capture_and_verify("qa_btn_25_manual_hydraulic_tested")
# Test switching manual tab to THRUSTER at (810, 120)
click_win(810, 120, 0.3)
capture_and_verify("qa_btn_26_manual_thruster_tested")
# Close modal with ESC
send_key("Escape", 0.4)

# 3. Advance Turn: Click >> ADVANCE TURN << at (650, 32)
click_win(650, 32, 0.6)
capture_and_verify("qa_btn_27_top_hud_advance_turn_fired")

# 4. Quick Save: Click [F5 SAVE] at (965, 32)
click_win(965, 32, 0.4)
capture_and_verify("qa_btn_28_top_hud_save_fired")

# 5. Commander Profile Badge: Click Commander Dossier at (1230, 32)
click_win(1230, 32, 0.5)
capture_and_verify("qa_btn_29_top_hud_commander_badge")
# Close modal with ESC
send_key("Escape", 0.4)

# Final clean state
capture_and_verify("qa_btn_30_final_verified_state")

print("\n==========================================================")
print("  COMPREHENSIVE QA BUTTON & BLEED SUITE COMPLETED!       ")
print("==========================================================")
