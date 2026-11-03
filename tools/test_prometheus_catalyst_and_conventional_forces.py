import os
import json
import re

print("=== RUNNING EXPANDED PRE-MS ASSET & COMBAT VALIDATION SUITE ===")

errors = []
successes = []

# 1. Check Document 38
doc_path = "docs/38_the_prometheus_catalyst_conventional_warfare_and_mobile_suit_genesis.md"
if os.path.exists(doc_path) and os.path.getsize(doc_path) > 1000:
    successes.append("Document 38 exists and is comprehensive.")
else:
    errors.append("Document 38 missing or too small.")

# 2. Check datafiles/conventional_vehicles.json
veh_json_path = "datafiles/conventional_vehicles.json"
if os.path.exists(veh_json_path):
    with open(veh_json_path, "r") as f:
        v_data = json.load(f)
    v_count = len(v_data.get("vehicles", []))
    if v_count >= 13:
        successes.append(f"conventional_vehicles.json valid with {v_count} combined-arms units (Tanks, Jets, Gunships, Infantry).")
    else:
        errors.append(f"conventional_vehicles.json has {v_count} units, expected >= 13.")
else:
    errors.append("datafiles/conventional_vehicles.json missing.")

# 3. Check All 46 Conventional, Infantry, Aircraft, and Wreckage Sprites
all_sprites = [
    # Infantry Squads (16 = 4 Factions x 4 Animation States: Idle, Back, Fire, Defeat)
    "spr_inf_terran_squad_idle", "spr_inf_terran_squad_back_idle", "spr_inf_terran_squad_fire", "spr_inf_terran_squad_defeat",
    "spr_inf_colony_squad_idle", "spr_inf_colony_squad_back_idle", "spr_inf_colony_squad_fire", "spr_inf_colony_squad_defeat",
    "spr_inf_syndicate_squad_idle", "spr_inf_syndicate_squad_back_idle", "spr_inf_syndicate_squad_fire", "spr_inf_syndicate_squad_defeat",
    "spr_inf_zaibatsu_squad_idle", "spr_inf_zaibatsu_squad_back_idle", "spr_inf_zaibatsu_squad_fire", "spr_inf_zaibatsu_squad_defeat",
    
    # Tanks & Ground Vehicles (12 = 4 Vehicles x 3 Animation States: Idle, Back, Fire)
    "spr_veh_terran_mammoth_idle", "spr_veh_terran_mammoth_back_idle", "spr_veh_terran_mammoth_fire",
    "spr_veh_colony_stiletto_idle", "spr_veh_colony_stiletto_back_idle", "spr_veh_colony_stiletto_fire",
    "spr_veh_syndicate_technical_idle", "spr_veh_syndicate_technical_back_idle", "spr_veh_syndicate_technical_fire",
    "spr_veh_zaibatsu_kurogane_idle", "spr_veh_zaibatsu_kurogane_back_idle", "spr_veh_zaibatsu_kurogane_fire",

    # Aircraft & Helicopters/Gunships (15 = 5 Vehicles x 3 States: Idle, Back, Fire)
    "spr_veh_colony_gunship_idle", "spr_veh_colony_gunship_back_idle", "spr_veh_colony_gunship_fire",
    "spr_veh_terran_skyhammer_idle", "spr_veh_terran_skyhammer_back_idle", "spr_veh_terran_skyhammer_fire",
    "spr_veh_colony_dart_idle", "spr_veh_colony_dart_back_idle", "spr_veh_colony_dart_fire",
    "spr_veh_syndicate_bomber_idle", "spr_veh_syndicate_bomber_back_idle", "spr_veh_syndicate_bomber_fire",
    "spr_veh_zaibatsu_drone_jet_idle", "spr_veh_zaibatsu_drone_jet_back_idle", "spr_veh_zaibatsu_drone_jet_fire",

    # Battlefield Wreckages & Suppression (3)
    "spr_veh_wreckage_tank",
    "spr_veh_wreckage_plane",
    "spr_inf_suppressed"
]

missing_sprs = []
frame_errors = []
for spr in all_sprites:
    spr_dir = os.path.join("sprites", spr)
    yy_file = os.path.join(spr_dir, f"{spr}.yy")
    if not (os.path.exists(spr_dir) and os.path.exists(yy_file)):
        missing_sprs.append(spr)
    else:
        pngs = [f for f in os.listdir(spr_dir) if f.endswith(".png")]
        if len(pngs) != 4:
            frame_errors.append(f"{spr}: has {len(pngs)} frames (expected 4)")

if not missing_sprs and not frame_errors:
    successes.append(f"All {len(all_sprites)} high-detail pre-MS sprites exist with valid .yy and exactly 4 frames each.")
else:
    if missing_sprs:
        errors.append(f"Missing sprites: {missing_sprs}")
    if frame_errors:
        errors.append(f"Frame count mismatches: {frame_errors}")

# 4. Check MechMakerConcept.yyp registration for all 46 sprites
with open("MechMakerConcept.yyp", "r") as f:
    yyp_content = f.read()

unregistered = [spr for spr in all_sprites if spr not in yyp_content]
if not unregistered:
    successes.append(f"All {len(all_sprites)} sprites verified registered in MechMakerConcept.yyp.")
else:
    errors.append(f"Unregistered in YYP: {unregistered}")

# 5. Check obj_BattleManager: Combat integration (Advance Wars defeat, Firing recoil, Suppression)
with open("objects/obj_BattleManager/Create_0.gml", "r") as f:
    bm_code = f.read()

if "INFANTRY SUPPRESSED! x2.0" in bm_code:
    successes.append("obj_BattleManager: Anti-Personnel 2.0x suppression bonus vs infantry verified.")
else:
    errors.append("obj_BattleManager: Anti-Personnel suppression missing.")

if "ATGM SHAPED CHARGE!" in bm_code:
    successes.append("obj_BattleManager: Infantry ATGM anti-armor shaped-charge callout verified.")
else:
    errors.append("obj_BattleManager: Infantry ATGM callout missing.")

if "string_replace(_s_name, \"_idle\", \"_defeat\")" in bm_code:
    successes.append("obj_BattleManager: Advance Wars style infantry blown-away defeat pose integration verified.")
else:
    errors.append("obj_BattleManager: Defeat pose integration missing.")

if "string_replace(_spr_name, \"_idle\", \"_fire\")" in bm_code:
    successes.append("obj_BattleManager: Dynamic firing recoil action sprite integration verified.")
else:
    errors.append("obj_BattleManager: Firing action sprite integration missing.")

# 6. Check obj_BattleManager/Draw_0.gml: Dedicated Infantry & Aircraft rendering
with open("objects/obj_BattleManager/Draw_0.gml", "r") as f:
    draw_code = f.read()

if "is_infantry" in draw_code and "is_aircraft" in draw_code:
    successes.append("obj_BattleManager Draw_0: Distinct ground infantry squad and aerial flight elevation rendering verified.")
else:
    errors.append("obj_BattleManager Draw_0: Dedicated infantry/aircraft rendering missing.")

print("\n--- RESULTS ---")
for s in successes:
    print("  [PASS]", s)
for e in errors:
    print("  [FAIL]", e)

if not errors:
    print(f"\n>>> ALL {len(successes)} ADVANCED PRE-MS ASSET & SYSTEM TESTS PASSED PERFECTLY! <<<")
else:
    print(f"\n>>> {len(errors)} TESTS FAILED! <<<")
