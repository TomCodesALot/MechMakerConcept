#!/usr/bin/env python3
"""
tools/generate_200_characters_roster.py
Generates the comprehensive 200+ character database for MechMakerConcept in datafiles/characters_roster.json.
Features:
- Exactly 30 Recruitable Pilots per major faction (Terran, Colony, Syndicate, Zaibatsu) = 120 pilots
- Command figures, military directors, senators, and cartel bosses = 24 figures
- Family members, civilian liaisons, engineers, and dynastic kin = 48 figures
- Independent legendary mercenaries and drifters = 12 figures
- Interconnected kinship graphs (Vance, Rostova, Vane, Thorne, Cruz, Ortiz, Takahashi, Chen dynasties)
- Front Mission SNES visual aesthetic descriptors (palette, headgear, scars, bionics, expression)
"""

import os
import json

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "datafiles")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, "characters_roster.json")

# =============================================================================
# Helper Builder Function
# =============================================================================
def make_char(
    cid, name, callsign, faction, tier, role, is_recruitable,
    family_dynasty, kinship, mentor, wingman, rival,
    traits, pref_chassis, hiring_cr, salary_cr,
    snes_portrait, bio
):
    return {
        "id": cid,
        "name": name,
        "callsign": callsign,
        "faction_id": faction,
        "tier": tier,
        "role": role,
        "is_recruitable": is_recruitable,
        "family_dynasty": family_dynasty,
        "kinship": kinship,       # list of {"target_id": str, "relation": str}
        "mentor_id": mentor,
        "wingman_id": wingman,
        "rival_id": rival,
        "traits": traits,         # list of str
        "preferred_chassis": pref_chassis,
        "hiring_cost_cr": hiring_cr,
        "salary_per_cycle_cr": salary_cr,
        "morale": 80,
        "is_alive": True,
        "is_imprisoned": False,
        "snes_portrait_spec": snes_portrait, # visual spec
        "bio": bio
    }

ROSTER = []

# =============================================================================
# 1. TERRAN COALITION (48 FIGURES: 6 Command, 30 Recruitable Pilots, 12 Dynastic/Support)
# =============================================================================
# --- Terran Command & Leadership (6) ---
ROSTER.append(make_char(
    "char_terran_vance", "General Deborah Vance", "Iron Matron", "faction_terran", 4,
    "Supreme Director of Planetary Ordnance", False, "Vance",
    [{"target_id": "char_terran_julian_vance", "relation": "brother"},
     {"target_id": "char_terran_claire_vance", "relation": "daughter"},
     {"target_id": "pilot_terran_tyler_vance", "relation": "son"},
     {"target_id": "pilot_syndicate_jackal", "relation": "estranged_nephew"}],
    None, "pilot_terran_cole", "char_colony_cassian",
    ["iron_will", "artillery_doctrine", "unyielding_grit"], "GHA-07", 0, 0,
    {"palette": "terran_military_olive", "headgear": "officer_peaked_cap", "scars": "jaw_shrapnel", "eyes": "steel_grey", "expression": "severe_stoic"},
    "Supreme commander of Earth defense forces. Sacrificed family ties for imperial survival."
))

ROSTER.append(make_char(
    "char_terran_sterling", "High Commissioner Arthur Sterling", "The Auditor", "faction_terran", 4,
    "Senate Defense Liaison & Procurement Hawk", False, "Sterling",
    [{"target_id": "pilot_terran_lucas_sterling", "relation": "son"}],
    None, None, "char_terran_vance",
    ["corrupt_financier", "bureaucratic_shield", "procurement_hawk"], "None", 0, 0,
    {"palette": "terran_senate_grey", "headgear": "wire_monocle", "scars": "none", "eyes": "calculating_hazel", "expression": "condescending_smirk"},
    "Controls the military budget with an iron spreadsheet. Secretly trades with Zaibatsu brokers."
))

ROSTER.append(make_char(
    "char_terran_julian_vance", "Col. Julian Vance (Ret.)", "Old Tungsten", "faction_terran", 3,
    "Foundry Logistics Overseer", False, "Vance",
    [{"target_id": "char_terran_vance", "relation": "sister"},
     {"target_id": "pilot_syndicate_jackal", "relation": "son"}],
    None, None, None,
    ["veteran_quartermaster", "grief_stricken", "heavy_alloy_master"], "TCM-03", 0, 0,
    {"palette": "terran_foundry_slate", "headgear": "welding_goggles_up", "scars": "burn_neck", "eyes": "tired_brown", "expression": "mournful_frown"},
    "Deborah's older brother whose son Jax stole a prototype and joined the pirate fringe."
))

ROSTER.append(make_char(
    "char_terran_claire_vance", "Major Claire Vance", "Aegis Two", "faction_terran", 3,
    "Planetary Defense Battalion Commander", False, "Vance",
    [{"target_id": "char_terran_vance", "relation": "mother"},
     {"target_id": "pilot_terran_tyler_vance", "relation": "brother"},
     {"target_id": "pilot_syndicate_jackal", "relation": "cousin"}],
    "char_terran_vance", "pilot_terran_cole", "pilot_colony_sorren",
    ["defensive_bulwark", "duty_bound", "linebreaker"], "GHA-07B", 0, 0,
    {"palette": "terran_military_olive", "headgear": "comm_headset_single", "scars": "brow_cut", "eyes": "steely_green", "expression": "disciplined_focus"},
    "Deborah's disciplined daughter, determined to prove herself on merit rather than bloodline."
))

ROSTER.append(make_char(
    "char_terran_briggs", "General Gregory Briggs", "Trenchwall", "faction_terran", 4,
    "High Command Fortification Marshal", False, "Briggs",
    [{"target_id": "pilot_terran_tara_briggs", "relation": "daughter"}],
    None, None, "char_colony_cassian",
    ["trench_specialist", "cautious_tactician"], "TCM-03", 0, 0,
    {"palette": "terran_khaki_mud", "headgear": "steel_helmet_chinstrap", "scars": "chin_scar", "eyes": "cold_blue", "expression": "grim_scowl"},
    "Architect of the Callisto bunker networks."
))

ROSTER.append(make_char(
    "char_terran_oconnor", "Commodore Sean O'Connor", "Broadside", "faction_terran", 3,
    "Orbital Defense Station Overseer", False, "OConnor",
    [{"target_id": "pilot_terran_liam_oconnor", "relation": "son"}],
    None, None, "char_colony_lyra",
    ["railgun_supremacy", "orbital_anchor"], "TCX-11", 0, 0,
    {"palette": "terran_navy_blue", "headgear": "service_cap", "scars": "none", "eyes": "grey", "expression": "rigid_command"},
    "Commands orbital weapon platforms overlooking lunar staging yards."
))

# --- Terran 30 Recruitable Pilots ---
TERRAN_PILOTS_DATA = [
    ("pilot_terran_cole", "Lt. Marcus Cole", "Breaker", 3, "Vanguard Assault Ace", "GHA-07", 120000, 7500, ["vanguard_shield", "guardian_protector", "iron_grit"], "char_terran_vance", "pilot_terran_rostova", "pilot_syndicate_jackal", {"palette": "terran_military_olive", "headgear": "tactical_headset_wire", "scars": "cheek_gash", "eyes": "hazel", "expression": "protective_grim"}, "Frontline legend who shields rookies with his chassis."),
    ("pilot_terran_rostova", "Ensign Elena Rostova", "Sparrow", 1, "Recon Scout & Spotter", "TCM-03", 35000, 2200, ["high_agility", "eagle_optic", "family_debt"], "pilot_terran_cole", "pilot_terran_cole", "pilot_colony_kira", {"palette": "terran_khaki_light", "headgear": "flight_goggles_forehead", "scars": "none", "eyes": "bright_blue", "expression": "anxious_determined"}, "Rookie pilot determined to restore her family honor."),
    ("pilot_terran_tyler_vance", "Cadet Tyler Vance", "Bastion", 1, "Line Infantryman", "TCM-03", 40000, 2400, ["hothead", "reckless_bravery", "noble_blood"], "pilot_terran_cole", "pilot_terran_claire_vance", "pilot_syndicate_jackal", {"palette": "terran_military_olive", "headgear": "flight_cap_tilted", "scars": "none", "eyes": "green", "expression": "eager_cocky"}, "Deborah Vance's youngest son, eager to prove himself."),
    ("pilot_terran_lucas_sterling", "Sub-Lt. Lucas Sterling", "Goldfinger", 2, "Heavy Artillery Support", "GHA-07B", 75000, 4800, ["ammo_saver", "aristocratic_vanity", "railgun_aim"], None, "pilot_terran_cole", None, {"palette": "terran_senate_grey", "headgear": "gold_rimmed_glasses", "scars": "none", "eyes": "brown", "expression": "smug_pride"}, "Arthur Sterling's son, equipped with customized gilded FCS modules."),
    ("pilot_terran_tara_briggs", "Lt. Tara Briggs", "Bunker-Buster", 2, "Breaching Specialist", "GHA-07", 65000, 4200, ["fortress_ram", "explosive_expert"], "char_terran_briggs", "pilot_terran_rostova", "pilot_syndicate_nadia", {"palette": "terran_khaki_mud", "headgear": "heavy_ballistic_collar", "scars": "lip_scar", "eyes": "dark_brown", "expression": "hardened_smirk"}, "Demolition expert fond of dual kinetic breaching clubs."),
    ("pilot_terran_liam_oconnor", "Warrant Officer Liam O'Connor", "Deadeye", 2, "Long-Range Railgunner", "GHA-07B", 70000, 4500, ["sniper_stance", "cool_headed"], "char_terran_oconnor", "pilot_terran_cole", "pilot_zaibatsu_maya", {"palette": "terran_navy_blue", "headgear": "eye_magnifier_optic", "scars": "burn_ear", "eyes": "grey", "expression": "focused_aim"}, "Specializes in punching kinetic slugs through enemy cockpits."),
    ("pilot_terran_karl_vogel", "Sgt. Karl Vogel", "War-Pig", 2, "Heavy Vulcan Suppressor", "GHA-07", 55000, 3800, ["trigger_happy", "ballistic_saturation"], "pilot_terran_cole", None, "pilot_syndicate_skag", {"palette": "terran_mud_camo", "headgear": "heavy_boom_mic", "scars": "bullet_graze", "eyes": "brown", "expression": "feral_grin"}, "Can empty an entire 1800-round drum without releasing the trigger."),
    ("pilot_terran_anna_kovac", "Cpl. Anna Kovac", "Trench-Rat", 1, "Combat Trench Sentry", "TCM-03", 32000, 2000, ["trench_cover_bonus", "stubborn"], "pilot_terran_cole", "pilot_terran_rostova", None, {"palette": "terran_grey_drab", "headgear": "cloth_wrap_headband", "scars": "none", "eyes": "amber", "expression": "grimy_weary"}, "Veteran of the lunar trench siege, survivor of 18 sorties."),
    ("pilot_terran_dmitri_rostov", "Sgt. Dmitri Rostov", "Anvil", 2, "Armored Breacher", "TCM-03", 58000, 3900, ["shield_master", "brotherly_protection"], None, "pilot_terran_rostova", None, {"palette": "terran_foundry_slate", "headgear": "blast_shield_visor", "scars": "bridge_nose_scar", "eyes": "blue", "expression": "protective_scowl"}, "Elena's protective older brother, skilled with spiked tower shields."),
    ("pilot_terran_sergei_volkov", "Lt. Sergei Volkov", "Iron Wolf", 3, "Heavy Vanguard Hunter", "GHA-07", 95000, 6200, ["pack_hunter", "kinetic_penetrator"], "char_terran_vance", "pilot_terran_cole", "pilot_colony_sorren", {"palette": "terran_military_olive", "headgear": "fur_lined_flight_collar", "scars": "eye_patch_right", "eyes": "piercing_blue", "expression": "predatory_grin"}, "Ruthless assault commander with a verified count of 24 enemy mechs."),
    ("pilot_terran_mira_chen", "Flight Officer Mira Chen", "Comet-Lock", 2, "Missile Fire Controller", "GHA-07", 62000, 4100, ["swarm_missile_specialist", "calm_sensor"], None, "pilot_terran_cole", "pilot_zaibatsu_null07", {"palette": "terran_navy_blue", "headgear": "twin_sensor_headband", "scars": "none", "eyes": "dark_brown", "expression": "cool_confidence"}, "Maximizes missile lock-on speed and trajectory clustering."),
    ("pilot_terran_boris_kane", "Chief Warrant Kane", "Grave-Digger", 2, "Siege Mortar Gunner", "GHA-07B", 68000, 4400, ["indirect_fire_master", "heavy_recoil_soak"], "char_terran_briggs", None, "pilot_syndicate_slag_tony", {"palette": "terran_foundry_slate", "headgear": "smoke_filter_mask", "scars": "powder_burns", "eyes": "hazel", "expression": "grim_silence"}, "Known for shelling hostile positions until only craters remain."),
    ("pilot_terran_claudia_lang", "Cpl. Claudia Lang", "Valkyrie-Zero", 1, "Light Line Scout", "TCM-03", 38000, 2500, ["high_mobility_aspiration", "evasion_drill"], "pilot_terran_rostova", "pilot_terran_rostova", "pilot_colony_kira", {"palette": "terran_khaki_light", "headgear": "flight_goggles_down", "scars": "forehead_bandaid", "eyes": "green", "expression": "sharp_alert"}, "Eager young cadet studying agile vernier dodging tactics."),
    ("pilot_terran_hans_richter", "Master Sgt. Richter", "Old Bastion", 3, "Trench Defense Veteran", "TCM-03", 88000, 5800, ["impenetrable_guard", "veteran_instinct"], "char_terran_vance", "pilot_terran_cole", None, {"palette": "terran_mud_camo", "headgear": "dented_infantry_pot", "scars": "cross_hatch_cheeks", "eyes": "faded_grey", "expression": "leathery_resolve"}, "Has served 30 years under three Coalition administrations."),
    ("pilot_terran_veronica_frost", "Lt. Veronica Frost", "Cold Iron", 2, "Cryo-Containment Escort", "GHA-07", 72000, 4600, ["cryo_radiator_specialist", "calm_under_fire"], None, "pilot_terran_volkov", "pilot_colony_aether_kai", {"palette": "terran_navy_blue", "headgear": "high_thermal_collar", "scars": "frostbite_chin", "eyes": "ice_blue", "expression": "unflinching_cold"}, "Specializes in managing reactor heat spikes in prolonged firefights."),
    ("pilot_terran_jake_murdock", "Pvt. Jake Murdock", "Grease-Monkey", 1, "Field Repair Pilot", "TCM-03", 30000, 1900, ["emergency_patch", "jury_rig"], None, "pilot_terran_anna_kovac", None, {"palette": "terran_foundry_slate", "headgear": "mechanic_cap_backward", "scars": "oil_smudge", "eyes": "brown", "expression": "nervous_grin"}, "Can replace a blown hydraulic line in under four minutes."),
    ("pilot_terran_sonia_reyes", "Flight Lt. Sonia Reyes", "Scatter-Queen", 2, "Close-Range Autocannon", "GHA-07", 64000, 4200, ["point_blank_burst", "aggressive_charge"], "pilot_terran_cole", "pilot_terran_karl_vogel", "pilot_syndicate_nadia", {"palette": "terran_military_olive", "headgear": "throat_mic_strap", "scars": "neck_claw_scar", "eyes": "dark_brown", "expression": "fiery_challenge"}, "Loves charging heavy assault suits straight into point-blank range."),
    ("pilot_terran_arthur_pendleton", "Ensign Pendleton", "Squire", 1, "Line Support Gunner", "TCM-03", 34000, 2100, ["protocol_follower", "steady_hands"], "char_terran_sterling", "pilot_terran_lucas_sterling", None, {"palette": "terran_senate_grey", "headgear": "neat_haircut_no_cap", "scars": "none", "eyes": "blue", "expression": "eager_polite"}, "Academy graduate obsessed with standard Coalition regulations."),
    ("pilot_terran_igor_dubov", "Cpl. Igor Dubov", "Hammer-Head", 2, "Kinetic Brawler", "GHA-07", 56000, 3700, ["battering_ram", "stun_specialist"], "pilot_terran_volkov", "pilot_terran_karl_vogel", "pilot_syndicate_jackal", {"palette": "terran_mud_camo", "headgear": "reinforced_jaw_guard", "scars": "broken_nose", "eyes": "grey", "expression": "pugilist_scowl"}, "Specializes in crushing cockpits with gun-club clubbing strikes."),
    ("pilot_terran_helena_braun", "Capt. Helena Braun", "Iron-Siege", 3, "Artillery Battery Commander", "GHA-07B", 92000, 6000, ["battery_synchronizer", "morale_beacon"], "char_terran_vance", "pilot_terran_claire_vance", "pilot_colony_sorren", {"palette": "terran_military_olive", "headgear": "commander_beret", "scars": "temple_scar", "eyes": "green", "expression": "commanding_grace"}, "Orchestrates synchronized four-gun railgun salvos across kilometers."),
    ("pilot_terran_nathan_cross", "Warrant Officer Cross", "Bloodhound", 2, "Sensor Target-Lock", "TCM-03", 59000, 3900, ["radar_lock_bonus", "counter_ecm"], None, "pilot_terran_rostova", "pilot_zaibatsu_maya", {"palette": "terran_khaki_light", "headgear": "advanced_sensor_earmuff", "scars": "none", "eyes": "brown", "expression": "squinting_intent"}, "Punches through enemy ECM jammers with high-output targeting pulses."),
    ("pilot_terran_greta_hahn", "Sgt. Greta Hahn", "Iron-Sow", 2, "Heavy Kinetic Defender", "GHA-07", 66000, 4300, ["reactive_armor_expert", "damage_sponge"], "pilot_terran_hans_richter", "pilot_terran_anna_kovac", None, {"palette": "terran_mud_camo", "headgear": "heavy_flak_collar", "scars": "lip_cut", "eyes": "hazel", "expression": "unyielding_snarl"}, "Refuses to give up an inch of contested perimeter trench."),
    ("pilot_terran_tomas_zima", "Cadet Tomas Zima", "Spike", 1, "Trench Infantry Cadet", "TCM-03", 31000, 2000, ["fearless_rookie", "fast_reloader"], "pilot_terran_hans_richter", "pilot_terran_tyler_vance", None, {"palette": "terran_grey_drab", "headgear": "standard_issue_pot", "scars": "none", "eyes": "brown", "expression": "determined_stare"}, "Hardened orphan from the Callisto refugee camps."),
    ("pilot_terran_beatrice_fallon", "Lt. Beatrice Fallon", "Sky-Hammer", 2, "High-Impact Kinetic Diver", "GHA-07", 71000, 4700, ["drop_pod_assault", "kinetic_shock"], "char_terran_vance", "pilot_terran_cole", "pilot_colony_kira", {"palette": "terran_military_olive", "headgear": "jump_pack_respirator", "scars": "neck_cable_scar", "eyes": "dark_grey", "expression": "adrenaline_rush"}, "Specializes in orbital drop-pod descents straight onto enemy bastions."),
    ("pilot_terran_roland_vance", "Sub-Lt. Roland Vance", "Cast-Iron", 2, "Flak Screen Escort", "TCM-03", 63000, 4100, ["flak_screen_wall", "family_pride"], "char_terran_julian_vance", "pilot_terran_tyler_vance", "pilot_syndicate_jackal", {"palette": "terran_foundry_slate", "headgear": "service_visor_cap", "scars": "none", "eyes": "steel_grey", "expression": "proud_firm"}, "Julian Vance's second son who remained loyal to Earth High Command."),
    ("pilot_terran_yulia_morozova", "Flight Officer Morozova", "Hail-Storm", 2, "Rocket Saturation Gunner", "GHA-07", 67000, 4400, ["salvo_density", "suppressive_rain"], None, "pilot_terran_mira_chen", "pilot_syndicate_nadia", {"palette": "terran_navy_blue", "headgear": "targeting_monocle_left", "scars": "burn_hand", "eyes": "blue", "expression": "smirking_calculating"}, "Loves watching 32 micro-missiles streak across the black."),
    ("pilot_terran_felix_grimm", "Cpl. Felix Grimm", "Bulldozer", 1, "Fortification Clearer", "TCM-03", 36000, 2300, ["wall_crusher", "close_range_blast"], "pilot_terran_tara_briggs", "pilot_terran_karl_vogel", None, {"palette": "terran_khaki_mud", "headgear": "ballistic_cage_mask", "scars": "chin_split", "eyes": "dark_brown", "expression": "heavy_scowl"}, "Breaches blast doors with point-blank solid-slug detonations."),
    ("pilot_terran_nadine_ross", "Lt. Nadine Ross", "Iron-Sentry", 2, "Perimeter Overwatch", "TCM-03", 61000, 4000, ["overwatch_reflexes", "first_strike"], "char_terran_briggs", "pilot_terran_rostova", "pilot_zaibatsu_maya", {"palette": "terran_grey_drab", "headgear": "compact_sensor_mast", "scars": "ear_notch", "eyes": "amber", "expression": "vigilant_calm"}, "Maintains 360-degree sensor sweeps with hair-trigger reflexes."),
    ("pilot_terran_casper_lind", "Pvt. Casper Lind", "Ghost-Echo", 1, "Electronic Countermeasures", "TCM-03", 33000, 2100, ["jamming_chaff", "sensor_ghost"], None, "pilot_terran_nathan_cross", "pilot_zaibatsu_null07", {"palette": "terran_navy_blue", "headgear": "full_ecm_cowling", "scars": "none", "eyes": "hazel", "expression": "intense_stare"}, "Young radar tech adept at projecting deceptive phantom radar signatures."),
    ("pilot_terran_maxim_volk", "Captain Maxim Volk", "Dread-Walker", 3, "Titan Vanguard Commander", "TCX-11", 110000, 7200, ["dreadnought_presence", "capital_rail_aim"], "char_terran_vance", "pilot_terran_cole", "char_colony_cassian", {"palette": "terran_military_olive", "headgear": "titan_helm_crest", "scars": "full_cheek_burn", "eyes": "cold_steel", "expression": "monolithic_menace"}, "Legendary pilot of the TCX-11 Behemoth dreadnought platform.")
]

for p in TERRAN_PILOTS_DATA:
    pid, name, call, tier, role, pref, hire, sal, traits, mentor, wing, rival, snes, bio = p
    dynasty = "Vance" if "Vance" in name else ("Rostov" if "Rostov" in name else ("Sterling" if "Sterling" in name else ("Briggs" if "Briggs" in name else None)))
    kin = []
    if dynasty == "Vance":
        kin.append({"target_id": "char_terran_vance", "relation": "dynasty_member"})
    elif dynasty == "Rostov":
        kin.append({"target_id": "pilot_terran_rostova", "relation": "sibling"})
    ROSTER.append(make_char(pid, name, call, "faction_terran", tier, role, True, dynasty, kin, mentor, wing, rival, traits, pref, hire, sal, snes, bio))

# Add 12 Terran Dynastic/Support Figures
TERRAN_SUPPORT = [
    ("char_terran_anna_rostova", "Anna Rostova", "Matron Rostova", "civilian_liaison", "Rostov", [{"target_id": "pilot_terran_rostova", "relation": "mother"}, {"target_id": "pilot_terran_dmitri_rostov", "relation": "mother"}], "Widow of late Admiral Viktor Rostov fighting debt collection."),
    ("char_terran_dr_arnold", "Dr. Heinrich Arnold", "Chief Metallurgist", "chief_metallurgist", "None", [], "Lead foundry scientist developing Tungsten-Carbide alloys."),
    ("char_terran_quartermaster_graves", "Quartermaster Graves", "The Scythe", "logistics_director", "None", [], "Rigid inventory clerk who accounts for every depleted uranium sabot."),
    ("char_terran_senator_holloway", "Senator Evelyn Holloway", "War-Hawk Holloway", "senate_diplomat", "Holloway", [], "Earth Senate advocate for total planetary mobilization."),
    ("char_terran_engineer_burt", "Chief Mechanic Burt", "Wrench", "hangar_chief", "None", [], "Veteran grease monkey who has patched over two hundred Ironclads."),
    ("char_terran_cadet_elise", "Cadet Elise Vance", "Little Vance", "cadet_in_training", "Vance", [{"target_id": "char_terran_vance", "relation": "granddaughter"}], "Deborah's granddaughter studying ballistics at the Geneva Academy."),
    ("char_terran_liaison_trent", "Major Donald Trent", "Garrison Liaison", "military_police", "None", [], "Coalition internal affairs investigator watching for defectors."),
    ("char_terran_refit_master_otto", "Foundry Master Otto", "Sledge", "foundry_overseer", "None", [], "Supervises the casting of 400mm Behemoth rail barrels."),
    ("char_terran_nurse_clara", "Dr. Clara Rostova", "Mercy", "field_surgeon", "Rostov", [{"target_id": "pilot_terran_rostova", "relation": "aunt"}], "Battlefield surgeon treating trauma and amputations in bunker redoubts."),
    ("char_terran_test_pilot_greer", "Capt. Wade Greer", "Crash-Test", "test_pilot", "None", [], "Test-flies experimental Vanguard prototypes; survived four core breeches."),
    ("char_terran_attache_morris", "Diplomatic Attache Morris", "The Shadow", "intelligence_liaison", "None", [], "Monitors clandestine transmissions between Earth and Mars."),
    ("char_terran_supply_sergeant_brant", "Sgt. Caleb Brant", "Hauler", "convoy_commander", "None", [], "Commands the heavy tungsten supply haulers across crater routes.")
]
for sid, name, call, role, dyn, kin, bio in TERRAN_SUPPORT:
    ROSTER.append(make_char(sid, name, call, "faction_terran", 2, role, False, dyn, kin, None, None, None, ["support_specialist"], "None", 0, 0, {"palette": "terran_military_olive", "headgear": "service_cap", "scars": "none", "eyes": "brown", "expression": "neutral"}, bio))

print(f"Generated Terran Coalition: {len(ROSTER)} characters.")

# =============================================================================
# 2. OUTER COLONY LEAGUE (48 FIGURES: 6 Command, 30 Recruitable Pilots, 12 Dynastic/Support)
# =============================================================================
# --- Colony Command & Leadership (6) ---
ROSTER.append(make_char(
    "char_colony_cassian", "Fleet Commander Cassian Vane", "Silver Falcon", "faction_colony", 4,
    "Supreme Marshall of the Liberation Flotilla", False, "Vane",
    [{"target_id": "char_colony_beatrice_vane", "relation": "sister"},
     {"target_id": "pilot_colony_julian_vane", "relation": "son"}],
    None, "pilot_colony_sorren", "char_terran_vance",
    ["orbital_dogfight_master", "chivalric_honor", "beam_accuracy_ace"], "OCM-09", 0, 0,
    {"palette": "colony_aether_cyan", "headgear": "aristocratic_cravat_collar", "scars": "thin_saber_cut", "eyes": "bright_amber", "expression": "noble_calm"},
    "Supreme Marshall of the Outer Colony Flotilla. Former Academy rival of General Deborah Vance."
))

ROSTER.append(make_char(
    "char_colony_lyra", "Minister Lyra Thorne", "Voice of the Habitats", "faction_colony", 4,
    "Chief Diplomat & Solar Habitat Resource Chair", False, "Thorne",
    [{"target_id": "char_colony_paul_thorne", "relation": "husband"},
     {"target_id": "pilot_colony_erik_thorne", "relation": "nephew"}],
    None, None, "char_terran_sterling",
    ["habitat_humanitarian", "diplomatic_shield", "resource_balancer"], "None", 0, 0,
    {"palette": "colony_diplomatic_white", "headgear": "orbital_diadem_earpiece", "scars": "none", "eyes": "violet", "expression": "empathic_firm"},
    "Protector of the civilian orbital cylinders who negotiates desperately for raw water and tritium."
))

ROSTER.append(make_char(
    "char_colony_beatrice_vane", "Senator Beatrice Vane", "The Dove", "faction_colony", 3,
    "Colony High Council Representative", False, "Vane",
    [{"target_id": "char_colony_cassian", "relation": "brother"}],
    None, None, None,
    ["orator_charisma", "colonial_independence"], "None", 0, 0,
    {"palette": "colony_diplomatic_white", "headgear": "senate_stole", "scars": "none", "eyes": "amber", "expression": "eloquent_pride"},
    "Cassian's sister who champions political autonomy from Terran resource quotas."
))

ROSTER.append(make_char(
    "char_colony_paul_thorne", "Chief Engineer Paul Thorne", "Life-Support", "faction_colony", 3,
    "Orbital Environmental Mesh Overseer", False, "Thorne",
    [{"target_id": "char_colony_lyra", "relation": "wife"},
     {"target_id": "pilot_colony_erik_thorne", "relation": "son"}],
    None, None, None,
    ["aerosteel_weaver", "reactor_cooling_sage"], "OCA-07", 0, 0,
    {"palette": "colony_engineer_teal", "headgear": "magnifying_visor", "scars": "coolant_burn_cheek", "eyes": "brown", "expression": "weary_precision"},
    "Designs the radiator wings and magnetic containment fields for Aether reactors."
))

ROSTER.append(make_char(
    "char_colony_helmut_zhao", "Admiral Helmut Zhao", "Starlight Vanguard", "faction_colony", 4,
    "Deep Space Patrol Fleet Commander", False, "Zhao",
    [{"target_id": "pilot_zaibatsu_maya", "relation": "estranged_daughter"}],
    None, None, "char_terran_oconnor",
    ["zero_g_carrier_tactics", "iron_discipline"], "OCM-09", 0, 0,
    {"palette": "colony_aether_cyan", "headgear": "admiral_high_collar", "scars": "temple_burn", "eyes": "dark_slate", "expression": "stern_veteran"},
    "Hardline orbital fleet officer whose daughter defected to Zaibatsu corporate security."
))

ROSTER.append(make_char(
    "char_colony_finch", "Flight Marshal Alistair Finch", "Wind-Shear", "faction_colony", 3,
    "Interceptor Wing Flight Instructor", False, "Finch",
    None, None, "pilot_colony_sorren", None,
    ["aerobatic_drillmaster", "vernier_perfectionist"], "OCM-04", 0, 0,
    {"palette": "colony_flight_orange", "headgear": "retro_pilot_helmet_unlatched", "scars": "mustache_scar", "eyes": "green", "expression": "demanding_smirk"},
    "Trains young interceptor recruits in three-dimensional vector thruster combat."
))

# --- Colony 30 Recruitable Pilots ---
COLONY_PILOTS_DATA = [
    ("pilot_colony_sorren", "Sorren 'Ghost' Lin", "Ghost of Sol", 3, "Elite Particle Sniper", "OCM-09", 125000, 7800, ["invisible_flight", "sniper_focus", "chivalric_oath"], "char_colony_cassian", "pilot_colony_kira", "pilot_terran_cole", {"palette": "colony_aether_cyan", "headgear": "tachyon_monocle_visor", "scars": "chin_nick", "eyes": "ice_blue", "expression": "serene_lethal"}, "Supreme Colony ace who snipes enemy reactors without spilling civilian blood."),
    ("pilot_colony_kira", "Kira Dahl", "Sun-Dancer", 2, "High-G Vector Skirmisher", "OCM-04", 65000, 4200, ["vector_drift", "rapid_saber_flurry"], "pilot_colony_sorren", "pilot_colony_sorren", "pilot_terran_rostova", {"palette": "colony_flight_orange", "headgear": "twin_headset_earmuffs", "scars": "none", "eyes": "violet", "expression": "exuberant_smirk"}, "High-G dogfighter who dances circles around heavy Coalition bulwarks."),
    ("pilot_colony_erik_thorne", "Erik Thorne", "Solar-Flare", 2, "Particle Arbalest Gunner", "OCA-07", 72000, 4600, ["beam_accelerator_boost", "family_obligation"], "char_colony_paul_thorne", "pilot_colony_sorren", "pilot_terran_lucas_sterling", {"palette": "colony_diplomatic_white", "headgear": "targeting_goggles_amber", "scars": "none", "eyes": "hazel", "expression": "proud_intent"}, "Lyra's nephew dedicated to defending orbital agricultural domes."),
    ("pilot_colony_rin_lin", "Rin Lin", "Stardust", 1, "Light Interceptor Scout", "OCM-04", 36000, 2300, ["sensor_boost", "agile_evasion"], "pilot_colony_sorren", "pilot_colony_sorren", None, {"palette": "colony_aether_cyan", "headgear": "comms_hairband", "scars": "none", "eyes": "dark_amber", "expression": "curious_alert"}, "Sorren's younger sibling, an instinctive pilot with uncanny zero-G reflexes."),
    ("pilot_colony_julian_vane", "Julian Vane", "Falconet", 2, "Line Dominance Duelist", "OCM-09", 78000, 4900, ["noble_fencing", "high_accuracy_beam"], "char_colony_cassian", "pilot_colony_sorren", "pilot_terran_tyler_vance", {"palette": "colony_aether_cyan", "headgear": "silver_rimmed_monocle", "scars": "none", "eyes": "amber", "expression": "haughty_brave"}, "Cassian Vane's son, fighting with an elegant high-frequency beam rapier."),
    ("pilot_colony_kai_aether", "Kai Aether", "Solar-Pulse", 2, "Particle Carbine Gunner", "OCM-09", 68000, 4400, ["beam_pulse_cadence", "evasive_jink"], "char_colony_finch", "pilot_colony_kira", "pilot_terran_veronica_frost", {"palette": "colony_flight_orange", "headgear": "tactical_boom_mic", "scars": "cheek_scratch", "eyes": "grey", "expression": "focused_intense"}, "Synchronizes beam rifle fire with vector vernier boost hops."),
    ("pilot_colony_selene_voss", "Selene Voss", "Moon-Shadow", 2, "Electronic Warfare Scout", "OCM-04", 62000, 4000, ["chaff_specialist", "stealth_skirmish"], None, "pilot_colony_rin_lin", "pilot_zaibatsu_null07", {"palette": "colony_navy_void", "headgear": "tinted_radar_visor", "scars": "none", "eyes": "violet", "expression": "mysterious_calm"}, "Blinds enemy targeting arrays before launching hit-and-run attacks."),
    ("pilot_colony_tariq_mansoor", "Tariq Mansoor", "Dervish", 2, "Twin Beam Saber Duelist", "OCM-09", 74000, 4700, ["dual_wield_master", "acrobatic_strike"], "char_colony_cassian", "pilot_colony_kira", "pilot_syndicate_jackal", {"palette": "colony_aether_cyan", "headgear": "aerosteel_circlet", "scars": "brow_cut", "eyes": "dark_brown", "expression": "fiery_zeal"}, "Wields paired Hyperion beam sabers with blinding centrifugal strikes."),
    ("pilot_colony_chloe_duval", "Chloe Duval", "Starlight Arbalest", 3, "Spinal Siege Sniper", "OCA-07", 98000, 6400, ["tachyon_lock", "overcharge_beam"], "char_colony_paul_thorne", "pilot_colony_sorren", "pilot_terran_liam_oconnor", {"palette": "colony_diplomatic_white", "headgear": "long_range_sensor_lens", "scars": "retina_burn", "eyes": "emerald", "expression": "calculating_grace"}, "Holds the record for longest verified kill on an approaching Jovian transport."),
    ("pilot_colony_milo_trent", "Milo Trent", "Zephyr", 1, "Interceptor Rookie", "OCM-04", 34000, 2200, ["hot_rod_thrusters", "reckless_speed"], "char_colony_finch", None, "pilot_terran_tomas_zima", {"palette": "colony_flight_orange", "headgear": "open_collar_headset", "scars": "none", "eyes": "blue", "expression": "cocky_grin"}, "Pushes his Sylph frame past safe-G limits for the pure thrill of speed."),
    ("pilot_colony_orion_sol", "Orion Sol", "Corona", 3, "Trans-Am Candidate Ace", "OCX-15", 115000, 7500, ["transam_compatibility", "singularity_harmonizer"], "char_colony_cassian", "pilot_colony_sorren", "char_terran_vance", {"palette": "colony_aether_cyan", "headgear": "quantum_neural_band", "scars": "solar_burn_neck", "eyes": "gold", "expression": "radiant_intensity"}, "Elite pilot tuned to withstand the devastating G-forces of the Seraphim."),
    ("pilot_colony_freja_lind", "Freja Lind", "Aegis-Angel", 2, "Defensive Beam Escort", "OCM-09", 69000, 4500, ["thermal_siphon_shield", "convoy_guardian"], "char_colony_lyra", "pilot_colony_erik_thorne", "pilot_terran_greta_hahn", {"palette": "colony_diplomatic_white", "headgear": "guardian_winged_headset", "scars": "none", "eyes": "blue", "expression": "calm_protective"}, "Uses thermal siphon shields to absorb enemy energy bolts destined for transports."),
    ("pilot_colony_dante_mercer", "Dante Mercer", "Star-Reaper", 2, "High-Speed Plasma Harasser", "OCM-04", 64000, 4100, ["plasma_needle_master", "weakpoint_strike"], None, "pilot_colony_kai_aether", "pilot_syndicate_skag", {"palette": "colony_navy_void", "headgear": "respirator_chinstrap", "scars": "lip_scar", "eyes": "grey", "expression": "cold_professional"}, "Punctures enemy armor joints with thermal needle precision strikes."),
    ("pilot_colony_astraea_vane", "Lady Astraea Vane", "Silver-Wing", 2, "Interceptor Duelist", "OCM-09", 76000, 4800, ["aristocratic_fencing", "high_speed_turn"], "char_colony_cassian", "pilot_colony_julian_vane", "pilot_terran_claire_vance", {"palette": "colony_aether_cyan", "headgear": "silver_hairclip_mic", "scars": "none", "eyes": "amber", "expression": "regal_focus"}, "Cassian Vane's niece, bringing high-society grace into cockpit dogfights."),
    ("pilot_colony_leo_drachen", "Leo Drachen", "Comet-Tail", 2, "Micro-Missile Swarmer", "OCM-04", 61000, 3900, ["missile_barrage_agility", "lock_break_drift"], "char_colony_finch", None, "pilot_terran_yulia_morozova", {"palette": "colony_flight_orange", "headgear": "dual_boom_headset", "scars": "brow_shrapnel", "eyes": "hazel", "expression": "smirking_defiant"}, "Specializes in releasing missile clouds mid-barrel roll."),
    ("pilot_colony_nyx_callisto", "Nyx Callisto", "Eclipse", 3, "Stealth Infiltrator", "OCM-09", 94000, 6100, ["active_camouflage", "cold_thrusters"], None, "pilot_colony_selene_voss", "pilot_zaibatsu_maya", {"palette": "colony_navy_void", "headgear": "optical_baffle_visor", "scars": "throat_scar", "eyes": "dark_violet", "expression": "silent_shadow"}, "Infiltrates hostile planetary perimeters using low-thermal vector coasting."),
    ("pilot_colony_valentin_roux", "Valentin Roux", "Solar-Fencer", 2, "Precision Saber Duelist", "OCM-09", 71000, 4600, ["saber_counter_parry", "graceful_footwork"], "char_colony_cassian", "pilot_colony_tariq_mansoor", "pilot_terran_igor_dubov", {"palette": "colony_aether_cyan", "headgear": "fencing_strap_headband", "scars": "none", "eyes": "green", "expression": "gentlemanly_smirk"}, "Treats every mobile suit duel as a formal fencing exhibition."),
    ("pilot_colony_jun_takahashi", "Jun Takahashi", "Ronin-Aether", 2, "High-Mobility Gunner", "OCM-09", 67000, 4300, ["hybrid_doctrine", "kinetic_deflector"], None, "pilot_colony_sorren", "pilot_zaibatsu_renzo", {"palette": "colony_aether_cyan", "headgear": "zaibatsu_defector_patch", "scars": "temple_plug_scar", "eyes": "dark_brown", "expression": "resolute_defiant"}, "Zaibatsu corporate defector who fled to the colonies to pilot free frames."),
    ("pilot_colony_esper_hale", "Esper Hale", "Sol-Warden", 1, "Civilian Guard Sentry", "OCM-04", 35000, 2200, ["habitat_loyalty", "steady_defense"], "char_colony_lyra", "pilot_colony_erik_thorne", None, {"palette": "colony_diplomatic_white", "headgear": "guard_crest_cap", "scars": "none", "eyes": "blue", "expression": "gentle_firm"}, "Former habitat police officer dedicated to stopping pirate boarding raids."),
    ("pilot_colony_cyrus_vane", "Cyrus Vane", "Peregrine", 2, "Spinal Accelerator Gunner", "OCA-07", 75000, 4800, ["sniper_endurance", "heat_management"], "char_colony_paul_thorne", "pilot_colony_chloe_duval", "pilot_terran_helen_braun", {"palette": "colony_aether_cyan", "headgear": "cooling_tube_collar", "scars": "cheek_burn", "eyes": "amber", "expression": "austere_focus"}, "Cassian Vane's cousin, stationed along the asteroid defense perimeter."),
    ("pilot_colony_talon_skye", "Talon Skye", "Wind-Walker", 2, "Vernier Sprint Specialist", "OCM-04", 63000, 4000, ["high_boost_speed", "tight_vector_turn"], "char_colony_finch", "pilot_colony_kira", "pilot_syndicate_nadia", {"palette": "colony_flight_orange", "headgear": "open_helmet_yellow_visor", "scars": "ear_clip", "eyes": "brown", "expression": "thrill_seeker"}, "Can maintain 140 kph boost speed through tight orbital debris corridors."),
    ("pilot_colony_aurora_blake", "Aurora Blake", "Solar-Flare-Two", 1, "Particle Carbine Rookie", "OCM-04", 37000, 2400, ["rapid_fire_cadence", "evasive_instinct"], "pilot_colony_sorren", "pilot_colony_rin_lin", None, {"palette": "colony_aether_cyan", "headgear": "light_headset_single", "scars": "none", "eyes": "green", "expression": "bright_determined"}, "High-scoring academy graduate assigned to border patrol sectors."),
    ("pilot_colony_gideon_cross", "Gideon Cross", "Crucible", 3, "Heavy Beam Artillery Ace", "OCA-07", 96000, 6200, ["siege_penetration", "radiator_wing_overdrive"], "char_colony_cassian", "pilot_colony_chloe_duval", "pilot_terran_maxim_volk", {"palette": "colony_diplomatic_white", "headgear": "heavy_targeting_helmet", "scars": "burn_brow", "eyes": "grey", "expression": "monolithic_calm"}, "Veteran of thirty long-range orbital engagements against Terran gunboats."),
    ("pilot_colony_lyra_junior", "Lyra Thorne-Vane", "Morning-Star", 1, "Support Spotter", "OCM-04", 39000, 2500, ["sensor_network", "diplomatic_immunity_hope"], "char_colony_lyra", "pilot_colony_erik_thorne", None, {"palette": "colony_diplomatic_white", "headgear": "ceremonial_beret", "scars": "none", "eyes": "violet", "expression": "idealistic_smile"}, "Daughter of Paul and Lyra Thorne, learning orbital combat reconnaissance."),
    ("pilot_colony_hugo_belmont", "Hugo Belmont", "Saber-Knight", 2, "Chivalric Bodyguard", "OCM-09", 73000, 4700, ["interceptor_bodyguard", "honor_duel"], "char_colony_cassian", "pilot_colony_julian_vane", "pilot_terran_cole", {"palette": "colony_aether_cyan", "headgear": "crest_plate_collar", "scars": "chin_scar", "eyes": "blue", "expression": "solemn_loyalty"}, "Sworn personal escort to the Colony Council delegation."),
    ("pilot_colony_faye_valerie", "Faye Valerie", "Super-Nova", 2, "High-Output Pulse Gunner", "OCM-09", 69000, 4400, ["burst_beam_specialist", "overheat_risk_taker"], "char_colony_paul_thorne", "pilot_colony_kai_aether", "pilot_syndicate_marauder_rex", {"palette": "colony_flight_orange", "headgear": "protective_welding_shades", "scars": "nose_scratch", "eyes": "hazel", "expression": "reckless_smirk"}, "Overclocks her E-Cap capacitor bank to fire triple-burst beam volleys."),
    ("pilot_colony_damien_sinclair", "Damien Sinclair", "Void-Hound", 2, "Intercept Hunter", "OCM-04", 66000, 4200, ["relentless_pursuit", "zero_g_grapple"], "char_colony_finch", "pilot_colony_dante_mercer", "pilot_syndicate_jackal", {"palette": "colony_navy_void", "headgear": "full_face_respirator", "scars": "none", "eyes": "cold_grey", "expression": "predatory_focus"}, "Specializes in hunting down fleeing pirate shuttles in the asteroid belt."),
    ("pilot_colony_nadia_vane", "Nadia Vane", "Silver-Arrow", 1, "Long-Range Light Scout", "OCM-04", 38000, 2400, ["high_altitude_optics", "evasion_reflex"], "char_colony_cassian", "pilot_colony_astraea_vane", None, {"palette": "colony_aether_cyan", "headgear": "feather_crest_hairband", "scars": "none", "eyes": "amber", "expression": "youthful_pride"}, "Youngest daughter of the Vane household, piloting high-agility interceptors."),
    ("pilot_colony_soren_kane", "Soren Kane", "Particle-Fist", 2, "CQB Beam Brawler", "OCM-09", 70000, 4500, ["beam_saber_parry", "close_range_blast"], "pilot_colony_sorren", "pilot_colony_tariq_mansoor", "pilot_terran_igor_dubov", {"palette": "colony_aether_cyan", "headgear": "brawler_jaw_strap", "scars": "eyebrow_notch", "eyes": "brown", "expression": "aggressive_confidence"}, "Adapts delicate beam sabers for brutal close-quarters dismantling strikes."),
    ("pilot_colony_elysium_zero", "Ace-01 Elysium", "Trans-Am Phantom", 4, "Supercritical Dominator Ace", "OCX-15", 140000, 9200, ["transam_apex", "funnel_mastery", "singularity_strike"], "char_colony_cassian", "pilot_colony_sorren", "char_zaibatsu_renzo", {"palette": "colony_aether_cyan", "headgear": "crown_resonance_circlet", "scars": "neural_burn_temples", "eyes": "radiant_gold", "expression": "transcendent_fury"}, "Legendary supreme champion of the Colony Liberation Flotilla.")
]

for p in COLONY_PILOTS_DATA:
    pid, name, call, tier, role, pref, hire, sal, traits, mentor, wing, rival, snes, bio = p
    dynasty = "Vane" if "Vane" in name else ("Thorne" if "Thorne" in name else ("Lin" if "Lin" in name else None))
    kin = []
    if dynasty == "Vane":
        kin.append({"target_id": "char_colony_cassian", "relation": "dynasty_member"})
    elif dynasty == "Thorne":
        kin.append({"target_id": "char_colony_lyra", "relation": "dynasty_member"})
    elif dynasty == "Lin":
        kin.append({"target_id": "pilot_colony_sorren", "relation": "sibling"})
    ROSTER.append(make_char(pid, name, call, "faction_colony", tier, role, True, dynasty, kin, mentor, wing, rival, traits, pref, hire, sal, snes, bio))

# Add 12 Colony Dynastic/Support Figures
COLONY_SUPPORT = [
    ("char_colony_dr_arundel", "Dr. Althea Arundel", "Aerosteel Weaver", "chief_materials_scientist", "None", [], "Pioneered lightweight Aerosteel nanoweave for Colony frames."),
    ("char_colony_ambassador_koren", "Ambassador Varis Koren", "The Peacemaker", "un_council_liaison", "None", [], "Represents the Outer Colonies at the Geneva Peace Accords."),
    ("char_colony_habitat_gov_orlov", "Governor Orlov", "Cylinder Warden", "habitat_governor", "None", [], "Administers agricultural colony Cylinder 4 overlooking Ceres."),
    ("char_colony_dockmaster_thea", "Dockmaster Thea", "Gantry Boss", "shipyard_superintendent", "None", [], "Manages zero-G mobile suit gantry cranes and launch catapults."),
    ("char_colony_hospitaller_mara", "Sister Mara Vane", "White Dove", "medical_director", "Vane", [{"target_id": "char_colony_cassian", "relation": "sister"}], "Directs civilian hospitals for habitat decompression trauma victims."),
    ("char_colony_hydroponics_sam", "Farmer Sam Thorne", "Green Thumb", "food_syndicate_chief", "Thorne", [{"target_id": "char_colony_lyra", "relation": "cousin"}], "Controls algae protein synthesizers and water filtration grids."),
    ("char_colony_telemetry_toby", "Toby Finch", "Sensor Eye", "radar_station_chief", "Finch", [{"target_id": "char_colony_finch", "relation": "son"}], "Detects approaching Coalition rail gunboats across lunar shadow corridors."),
    ("char_colony_tritium_refiner_jov", "Jovan Sol", "Tritium Burner", "refinery_boss", "None", [], "Refines high-purity fusion fuel from Jupiter gas scoops."),
    ("char_colony_quartermaster_selim", "Selim Mansoor", "Ledger-Master", "fleet_quartermaster", "None", [], "Balances emergency munitions allocations across fifty fighter wings."),
    ("char_colony_cadet_instructor_titus", "Commander Titus", "The Drill", "academy_proctor", "None", [], "Evaluates flight simulation scores for high-G vector pilots."),
    ("char_colony_historian_valeria", "Archivist Valeria", "Keeper of Oaths", "cultural_archivist", "None", [], "Preserves the historical treaty documents of the Secession War."),
    ("char_colony_salvage_broker_kenzo", "Kenzo Lin", "Tinkerer", "habitat_recycler", "Lin", [{"target_id": "pilot_colony_sorren", "relation": "uncle"}], "Reclaims shattered solar panel glass and burned thruster nozzles.")
]
for sid, name, call, role, dyn, kin, bio in COLONY_SUPPORT:
    ROSTER.append(make_char(sid, name, call, "faction_colony", 2, role, False, dyn, kin, None, None, None, ["support_specialist"], "None", 0, 0, {"palette": "colony_diplomatic_white", "headgear": "comm_headband", "scars": "none", "eyes": "violet", "expression": "neutral"}, bio))

print(f"Generated Colony League: {len(ROSTER)} characters total so far.")

# =============================================================================
# 3. RIM-SYNDICATE CARTEL (48 FIGURES: 6 Command, 30 Recruitable Pilots, 12 Dynastic/Support)
# =============================================================================
# --- Syndicate Command & Leadership (6) ---
ROSTER.append(make_char(
    "char_syndicate_cruz", "Madame Rosalind Cruz", "Queen of Slag", "faction_syndicate", 4,
    "Matriarch of Scrap Depot 9 & Smuggling Baroness", False, "Cruz",
    [{"target_id": "char_syndicate_tito_cruz", "relation": "brother"},
     {"target_id": "pilot_syndicate_nadia", "relation": "adopted_daughter"}],
    None, "pilot_syndicate_nadia", "char_terran_sterling",
    ["black_market_monopoly", "scrap_salvage_queen", "iron_fist_matriarch"], "SCR-12", 0, 0,
    {"palette": "syndicate_rust_orange", "headgear": "jeweled_welding_goggles", "scars": "acid_burn_cheek", "eyes": "piercing_hazel", "expression": "cunning_matriarch"},
    "Ruthless ruler of asteroid Scrap Depot 9. Treats family loyalty as the only law in the black."
))

ROSTER.append(make_char(
    "char_syndicate_torval", "Commodore 'Iron-Eye' Torval", "The Reaver", "faction_syndicate", 4,
    "Cartel Reaver Fleet Commodore", False, "Torval",
    None, None, "pilot_syndicate_jackal", "char_terran_vance",
    ["bloodthirsty_corsair", "boarding_claw_master", "ruthless_plunderer"], "SCX-19", 0, 0,
    {"palette": "syndicate_oil_black", "headgear": "tricorn_corsair_helmet", "scars": "cyber_eye_patch_right", "eyes": "bloodshot_yellow", "expression": "feral_snarl"},
    "Infamous pirate commodore missing his right eye from a Coalition railgun blast."
))

ROSTER.append(make_char(
    "char_syndicate_tito_cruz", "Tito Cruz", "The Fence", "faction_syndicate", 3,
    "Depot 9 Black-Market Broker", False, "Cruz",
    [{"target_id": "char_syndicate_cruz", "relation": "sister"},
     {"target_id": "pilot_syndicate_rico_cruz", "relation": "son"}],
    None, None, "char_zaibatsu_renzo",
    ["fence_mastermind", "smuggler_contracts"], "None", 0, 0,
    {"palette": "syndicate_rust_orange", "headgear": "slanted_fedora_goggles", "scars": "knife_scar_neck", "eyes": "beady_brown", "expression": "sly_grin"},
    "Manages the fence networks that launder stolen Coalition and Zaibatsu mobile suit frames."
))

ROSTER.append(make_char(
    "char_syndicate_mateo_ortiz", "Mateo Ortiz", "Old Torch", "faction_syndicate", 3,
    "Master Foundry Melter", False, "Ortiz",
    [{"target_id": "pilot_syndicate_nadia", "relation": "biological_daughter"}],
    None, "pilot_syndicate_nadia", None,
    ["crucible_master", "slag_chemistry_expert"], "SCA-14", 0, 0,
    {"palette": "syndicate_molten_copper", "headgear": "heavy_asbestos_hood", "scars": "furnace_burn_face", "eyes": "squinting_dark", "expression": "stoic_craftsman"},
    "Old foundry master who taught Nadia how to brew molten slag incendiary loads."
))

ROSTER.append(make_char(
    "char_syndicate_boss_varek", "Boss Varek", "The Butcher", "faction_syndicate", 3,
    "Asteroid Mining Guild Enforcer", False, "Varek",
    None, None, None, "char_colony_cassian",
    ["extortion_enforcer", "hydraulic_breaker"], "SCR-12", 0, 0,
    {"palette": "syndicate_oil_black", "headgear": "mining_drill_visor", "scars": "crushed_jaw", "eyes": "small_black", "expression": "brutal_sneer"},
    "Controls illegal asteroid labor colonies through terror and debt coercion."
))

ROSTER.append(make_char(
    "char_syndicate_skag_morgan", "Skag 'The Hook' Morgan", "The Hook", "faction_syndicate", 3,
    "Corsair Breaker Boss", False, "Morgan",
    None, None, "pilot_syndicate_jackal", "char_terran_oconnor",
    ["harpoon_boarding_master", "vacuum_survivor"], "SCR-05", 0, 0,
    {"palette": "syndicate_rust_orange", "headgear": "pirate_bandana_wire", "scars": "decompression_blotches", "eyes": "one_glass_eye", "expression": "crooked_leer"},
    "Boarding specialist who punctures cargo hulls with pneumatic grappling hooks."
))

# --- Syndicate 30 Recruitable Pilots ---
SYNDICATE_PILOTS_DATA = [
    ("pilot_syndicate_nadia", "Nadia 'Spark' Ortiz", "Spark", 2, "Demolition & Slag Specialist", "SCA-14", 75000, 4800, ["incendiary_slag_master", "jury_rig_expert", "explosive_temper"], "char_syndicate_mateo_ortiz", "char_syndicate_cruz", "pilot_terran_tara_briggs", {"palette": "syndicate_molten_copper", "headgear": "welding_mask_propped", "scars": "soot_burn_cheek", "eyes": "amber", "expression": "ferocious_grin"}, "Adopted daughter of Madame Cruz who loves raining boiling molten alloy on fortifications."),
    ("pilot_syndicate_jackal", "Jax 'Jackal' Vance", "Jackal", 3, "Renegade Reaver Brawler", "SCR-12", 110000, 7200, ["hydraulic_claw_crush", "blood_traitor_hate", "reckless_fury"], "char_terran_vance", "char_syndicate_torval", "pilot_terran_cole", {"palette": "syndicate_oil_black", "headgear": "spiked_jaw_respirator", "scars": "branded_vance_crest_slashed", "eyes": "wild_green", "expression": "cynical_snarl"}, "Estranged nephew of General Deborah Vance who stole a military prototype and fled Earth."),
    ("pilot_syndicate_rico_cruz", "Rico Cruz", "Slick", 2, "High-Speed Scrap Raider", "SCR-05", 58000, 3800, ["hit_and_run_plunder", "evasive_cockpit"], "char_syndicate_tito_cruz", "char_syndicate_cruz", "pilot_terran_lucas_sterling", {"palette": "syndicate_rust_orange", "headgear": "greasy_flight_cap", "scars": "chin_nick", "eyes": "dark_brown", "expression": "sly_smirk"}, "Madame Cruz's nephew, an agile pirate scout skilled at stripping derelicts under fire."),
    ("pilot_syndicate_skag_tony", "Tony 'Cinder' Varek", "Cinder", 2, "Incendiary Mortar Gunner", "SCA-14", 68000, 4400, ["area_denial_fire", "crucible_heat_soak"], "char_syndicate_boss_varek", "pilot_syndicate_nadia", "pilot_terran_boris_kane", {"palette": "syndicate_molten_copper", "headgear": "slag_shield_visor", "scars": "flame_scar_neck", "eyes": "brown", "expression": "grinning_maniac"}, "Rains white-hot slag onto extraction landing pads to trap fleeing convoys."),
    ("pilot_syndicate_marauder_rex", "Rex 'Guzzler' Thorne", "Guzzler", 2, "Heavy Flak Brawler", "SCR-12", 64000, 4200, ["scattergun_shredder", "fuel_thief"], None, "pilot_syndicate_jackal", "pilot_colony_faye_valerie", {"palette": "syndicate_rust_orange", "headgear": "heavy_ear_flaps_wire", "scars": "broken_jaw", "eyes": "grey", "expression": "brutal_grin"}, "Disowned Colony exile who siphons tritium fuel tanks in mid-combat grappling."),
    ("pilot_syndicate_gristle_pete", "Pete 'Gristle' Murphy", "Gristle", 1, "Scrap Raider Grunt", "SCR-05", 28000, 1800, ["cheap_repair", "desperate_charge"], "char_syndicate_skag_morgan", None, "pilot_terran_jake_murdock", {"palette": "syndicate_oil_black", "headgear": "ragged_bandana_knot", "scars": "lip_cleft", "eyes": "yellowish", "expression": "desperate_sneer"}, "Hungry asteroid drifter piloting a rusted junk chassis welded together with wire."),
    ("pilot_syndicate_val_fang", "Valeria 'Fang' Drachen", "Fang", 2, "Hydraulic Claw Grappler", "SCR-12", 72000, 4700, ["pincer_decapitator", "armor_shredder"], None, "pilot_syndicate_jackal", "pilot_zaibatsu_maya", {"palette": "syndicate_oil_black", "headgear": "iron_teeth_mask", "scars": "claw_tracks_face", "eyes": "dark_slate", "expression": "predatory_grin"}, "Pries open enemy cockpits with hydraulic claws to extract pilot ransom chips."),
    ("pilot_syndicate_rust_maggot", "Mick 'Maggot' Doyle", "Maggot", 1, "Asteroid Ambush Scout", "SCR-05", 31000, 2000, ["debris_stealth", "dirty_shot"], None, "pilot_syndicate_rico_cruz", "pilot_colony_milo_trent", {"palette": "syndicate_rust_orange", "headgear": "mining_visor_cracked", "scars": "pockmarked_skin", "eyes": "shifting_brown", "expression": "nervous_cunning"}, "Hides within drifting slag hollows until transport ships pass by."),
    ("pilot_syndicate_slik_talia", "Talia 'Viper' Vasquez", "Viper", 2, "Shrapnel Gun Specialist", "SCR-05", 62000, 4000, ["close_shrapnel_cone", "toxic_exhaust"], "char_syndicate_cruz", "pilot_syndicate_nadia", "pilot_colony_kira", {"palette": "syndicate_oil_black", "headgear": "snakeskin_strap_mic", "scars": "bullet_scar_temple", "eyes": "green", "expression": "venomous_smirk"}, "Madame Cruz's trusted enforcer who executes contract traitors on sight."),
    ("pilot_syndicate_baron_slag", "Baron 'Gag' Gorman", "Gag-Order", 3, "Four-Armed Dreadnought Ace", "SCX-19", 105000, 6800, ["stolen_rail_mastery", "four_arm_grapple"], "char_syndicate_torval", "pilot_syndicate_jackal", "pilot_terran_maxim_volk", {"palette": "syndicate_rust_orange", "headgear": "four_lens_optic_array", "scars": "massive_chest_burn", "eyes": "reddish_brown", "expression": "grotesque_pride"}, "Pilots an illegal hybrid dreadnought built from four different shattered warframes."),
    ("pilot_syndicate_scrappy_lou", "Lou 'Scrappy' Finch", "Scrappy", 1, "Field Scavenger", "SCR-05", 33000, 2100, ["salvage_bonus", "quick_escape"], None, "pilot_syndicate_rico_cruz", None, {"palette": "syndicate_rust_orange", "headgear": "tape_repaired_goggles", "scars": "cut_across_nose", "eyes": "blue", "expression": "hungry_eager"}, "Steals weapon hardpoints off disabled chassis before the smoke clears."),
    ("pilot_syndicate_hammer_fist_otto", "Otto 'Sledge' Krupp", "Sledge", 2, "Pneumatic Harpooner", "SCR-12", 66000, 4300, ["harpoon_tether", "kinetic_pulverizer"], "char_syndicate_mateo_ortiz", "pilot_syndicate_nadia", "pilot_terran_igor_dubov", {"palette": "syndicate_molten_copper", "headgear": "forgemaster_leather_cap", "scars": "iron_flake_scars", "eyes": "faded_blue", "expression": "grim_stonewall"}, "Impales enemy suits with steel harpoons then reels them into demolition range."),
    ("pilot_syndicate_katja_slit", "Katja 'Razor' Vane", "Razor", 2, "Cleaver Duelist", "SCR-05", 69000, 4500, ["serrated_cleaver_bleed", "ruthless_parry"], None, "pilot_syndicate_jackal", "pilot_colony_julian_vane", {"palette": "syndicate_oil_black", "headgear": "spiked_choker_collar", "scars": "cheek_stitch_lines", "eyes": "pale_grey", "expression": "derisive_mockery"}, "Disowned illegitimate child of the Vane family who joined the pirate reavers."),
    ("pilot_syndicate_bones_mccoy", "Bones 'Doc' McCoy", "Bone-Saw", 2, "Field Surgeon & Breacher", "SCR-12", 59000, 3900, ["cockpit_extraction", "stim_injector"], None, "pilot_syndicate_nadia", "char_terran_nurse_clara", {"palette": "syndicate_rust_orange", "headgear": "bloody_surgical_visor", "scars": "scalpel_nicks", "eyes": "watery_blue", "expression": "manic_grin"}, "Extracts wounded enemy pilots from crushed cockpits for prisoner bounties."),
    ("pilot_syndicate_blaze_keller", "Keller 'Torch' Brandt", "Torch", 2, "Incendiary Flak Raider", "SCA-14", 65000, 4200, ["thermite_spread", "smoke_screen_evade"], "char_syndicate_mateo_ortiz", "pilot_syndicate_skag_tony", "pilot_terran_veronica_frost", {"palette": "syndicate_molten_copper", "headgear": "soot_blackened_welder_helm", "scars": "charred_ears", "eyes": "dark_brown", "expression": "grinning_pyro"}, "Covers retreating pirate convoys with billowing clouds of burning thermite."),
    ("pilot_syndicate_grease_pit_dan", "Dan 'Oiler' Kowalski", "Oiler", 1, "Turbine Overclocker", "SCR-05", 35000, 2200, ["fission_overclock", "reckless_boost"], None, "pilot_syndicate_rico_cruz", None, {"palette": "syndicate_oil_black", "headgear": "grease_stained_knit_cap", "scars": "steam_scald_forehead", "eyes": "hazel", "expression": "nervous_sweat"}, "Pours synthetic motor oil straight into overheated fission turbines."),
    ("pilot_syndicate_cinder_clara", "Clara 'Sparky' Cruz", "Sparky", 1, "Scrap Artillery Spotter", "SCR-05", 37000, 2400, ["shrapnel_barrage_spotting", "kin_loyalty"], "char_syndicate_cruz", "pilot_syndicate_nadia", None, {"palette": "syndicate_rust_orange", "headgear": "bent_antenna_headband", "scars": "none", "eyes": "brown", "expression": "feisty_glare"}, "Tito Cruz's youngest daughter who spots targets for slag catapults."),
    ("pilot_syndicate_diesel_dave", "Dave 'Diesel' O'Malley", "Diesel", 2, "Heavy Excavator Driver", "SCR-12", 58000, 3800, ["ramming_prowess", "hydraulic_torque"], "char_syndicate_boss_varek", None, "pilot_terran_felix_grimm", {"palette": "syndicate_rust_orange", "headgear": "mining_pot_with_torch", "scars": "drill_bit_scar", "eyes": "brown", "expression": "plodding_resolve"}, "Drives 80-tonne mining excavators converted into frontline armored battering rams."),
    ("pilot_syndicate_siren_zara", "Zara 'Siren' Vance", "Siren", 2, "ECM Interceptor Outlaw", "SCR-05", 71000, 4600, ["frequency_screamer", "jamming_static"], "pilot_syndicate_jackal", "pilot_syndicate_jackal", "char_terran_vance", {"palette": "syndicate_oil_black", "headgear": "audio_feedback_headset", "scars": "ear_piercing_stretch", "eyes": "sharp_green", "expression": "spiteful_grin"}, "Jax Vance's renegade partner who broadcasts mocking pirate static over military bands."),
    ("pilot_syndicate_junk_king_armin", "Armin 'Junk-King' Vogel", "Junk-King", 3, "Cartel Foundry Enforcer", "SCR-12", 89000, 5800, ["tungsten_slag_armor", "brutal_intimidation"], "char_syndicate_cruz", "pilot_syndicate_nadia", "pilot_terran_sergei_volkov", {"palette": "syndicate_rust_orange", "headgear": "crown_welded_rebar", "scars": "cracked_skull_plate", "eyes": "steely_brown", "expression": "ferocious_swagger"}, "Controls the scrap processing plants on Pallas with an iron hydraulic grip."),
    ("pilot_syndicate_molten_mike", "Mike 'Ladle' Thorne", "Ladle", 2, "Molten Slag Loader", "SCA-14", 63000, 4100, ["fast_crucible_feed", "burn_resistance"], "char_syndicate_mateo_ortiz", "pilot_syndicate_nadia", "pilot_colony_erik_thorne", {"palette": "syndicate_molten_copper", "headgear": "molten_splash_apron_collar", "scars": "arm_burns", "eyes": "grey", "expression": "sweating_scowl"}, "Displaced Colony welder who loads white-hot crucible shells by hand."),
    ("pilot_syndicate_grudge_boris", "Boris 'Grudge' Volkov", "Grudge", 2, "Outcast Kinetic Brawler", "SCR-12", 67000, 4400, ["blood_feud_rage", "heavy_recoil_endure"], None, "pilot_syndicate_jackal", "pilot_terran_sergei_volkov", {"palette": "syndicate_oil_black", "headgear": "chained_collar_headset", "scars": "cross_face_slash", "eyes": "one_cloudy_blue", "expression": "burning_hate"}, "Sergei Volkov's disgraced brother who fled a court-martial on Earth."),
    ("pilot_syndicate_tinkerer_pip", "Pip 'Sprocket' Chen", "Sprocket", 1, "Scrap Avionics Hacker", "SCR-05", 38000, 2500, ["hotwire_avionics", "sensor_glitch"], None, "pilot_syndicate_nadia", "pilot_zaibatsu_null07", {"palette": "syndicate_rust_orange", "headgear": "magnifier_jewelers_loop", "scars": "battery_acid_dots", "eyes": "dark_brown", "expression": "hyperactive_grin"}, "Can hotwire a burnt Coalition sensor array using copper wire and chewing gum."),
    ("pilot_syndicate_gutter_rat_sam", "Sam 'Gutter' Higgins", "Gutter", 1, "Under-Deck Ambush Gunner", "SCR-05", 29000, 1900, ["crawlspace_ambush", "shrapnel_burst"], "char_syndicate_skag_morgan", None, None, {"palette": "syndicate_oil_black", "headgear": "rusty_pot_wire_chinstrap", "scars": "lip_bite", "eyes": "brown", "expression": "feral_distrust"}, "Lurks beneath cargo decks to shred boarding parties with scrap shrapnel."),
    ("pilot_syndicate_reaver_elena", "Elena 'Banshee' Cruz", "Banshee", 2, "High-Speed Boarder", "SCR-05", 68000, 4400, ["hull_breacher", "fearless_pirate"], "char_syndicate_cruz", "pilot_syndicate_rico_cruz", "pilot_terran_rostova", {"palette": "syndicate_rust_orange", "headgear": "painted_skull_visor", "scars": "temple_cut", "eyes": "amber", "expression": "fierce_howl"}, "Madame Cruz's niece who screams battle barks into ship com-channels."),
    ("pilot_syndicate_salvage_queen_mira", "Mira 'Vulture' Sterling", "Vulture", 2, "Derelict Stripper", "SCR-12", 70000, 4600, ["part_harvest_bonus", "chassis_strip_expert"], None, "char_syndicate_cruz", "char_terran_sterling", {"palette": "syndicate_rust_orange", "headgear": "cutting_torch_goggles", "scars": "none", "eyes": "hazel", "expression": "cynical_greedy"}, "Arthur Sterling's disgraced sister who left high society to fence battlefield titanium."),
    ("pilot_syndicate_iron_tusk_kurt", "Kurt 'Tusk' Bauer", "Tusk", 2, "Pneumatic Ramming Ace", "SCR-12", 66000, 4300, ["ram_shockwave", "heavy_frontal_plate"], "char_syndicate_torval", "pilot_syndicate_jackal", "pilot_terran_karl_vogel", {"palette": "syndicate_oil_black", "headgear": "welded_tusks_on_helmet", "scars": "missing_teeth", "eyes": "brown", "expression": "bellowing_scowl"}, "Welded two steel locomotive tusks onto his Hyena chest plate."),
    ("pilot_syndicate_rust_hound_ned", "Ned 'Hound' Kelly", "Hound", 1, "Outlaw Tracker", "SCR-05", 34000, 2200, ["heat_signature_tracker", "relentless_scent"], None, "pilot_syndicate_nadia", None, {"palette": "syndicate_rust_orange", "headgear": "tin_cowl_headpiece", "scars": "dog_bite_cheek", "eyes": "blue", "expression": "snarling_grin"}, "Can follow a leaking fusion coolant trail through sixty kilometers of asteroid dust."),
    ("pilot_syndicate_mad_dog_rocco", "Rocco 'Mad-Dog' Rossi", "Mad-Dog", 2, "Scatter-Flak Berserker", "SCR-12", 65000, 4200, ["point_blank_flak", "berserk_rage"], "char_syndicate_torval", "pilot_syndicate_jackal", "pilot_terran_sonia_reyes", {"palette": "syndicate_oil_black", "headgear": "chain_wrapped_headset", "scars": "shrapnel_cheeks", "eyes": "bloodshot_brown", "expression": "wild_eyed_fury"}, "Charges into 10-meter range and empties double-barreled flak scatterguns."),
    ("pilot_syndicate_apex_chimera_dread", "Captain 'Wreckage' Torval", "Apex Corsair", 4, "Illegal Hybrid Dreadnought Commander", "SCX-19", 135000, 8900, ["four_arm_annihilation", "stolen_rail_battery", "pirate_terror"], "char_syndicate_torval", "pilot_syndicate_jackal", "char_terran_vance", {"palette": "syndicate_oil_black", "headgear": "dread_corsair_iron_crown", "scars": "half_face_prosthetic", "eyes": "one_glowing_red_optic", "expression": "demonic_triumph"}, "Scourge of the Jovian trade corridors; commands the monstrous SCX-19 Chimera.")
]

for p in SYNDICATE_PILOTS_DATA:
    pid, name, call, tier, role, pref, hire, sal, traits, mentor, wing, rival, snes, bio = p
    dynasty = "Cruz" if "Cruz" in name else ("Ortiz" if "Ortiz" in name else ("Vance" if "Vance" in name else ("Torval" if "Torval" in name else None)))
    kin = []
    if dynasty == "Cruz":
        kin.append({"target_id": "char_syndicate_cruz", "relation": "dynasty_member"})
    elif dynasty == "Ortiz":
        kin.append({"target_id": "char_syndicate_mateo_ortiz", "relation": "dynasty_member"})
    elif dynasty == "Vance":
        kin.append({"target_id": "pilot_syndicate_jackal", "relation": "dynasty_member"})
    elif dynasty == "Torval":
        kin.append({"target_id": "char_syndicate_torval", "relation": "dynasty_member"})
    ROSTER.append(make_char(pid, name, call, "faction_syndicate", tier, role, True, dynasty, kin, mentor, wing, rival, traits, pref, hire, sal, snes, bio))

# Add 12 Syndicate Dynastic/Support Figures
SYNDICATE_SUPPORT = [
    ("char_syndicate_bartender_sal", "Sal 'Two-Fingers'", "Depot Bartender", "black_market_bartender", "None", [], "Runs the cantina on Depot 9 where contracts and bounties are traded."),
    ("char_syndicate_doc_sawbones", "Dr. 'Sawbones' Miller", "The Patcher", "unlicensed_surgeon", "None", [], "Performs back-alley cybernetic amputations and stimulant injections."),
    ("char_syndicate_smuggler_greta", "Greta Cruz", "Silent Runner", "smuggler_captain", "Cruz", [{"target_id": "char_syndicate_cruz", "relation": "niece"}], "Runs blockade-running shuttles through Terran patrol nets."),
    ("char_syndicate_scrappy_kid_toby", "Toby Ortiz", "Torch-Boy", "foundry_runner", "Ortiz", [{"target_id": "char_syndicate_mateo_ortiz", "relation": "grandson"}], "Runs hot welding torches and slag crucibles across Depot 9."),
    ("char_syndicate_hacker_null", "Glitch 'Zero'", "The Ghost", "avionics_jailbreaker", "None", [], "Strips Terran DRM encryption from captured mobile suit computers."),
    ("char_syndicate_fence_malik", "Malik Torval", "The Scalper", "black_market_quartermaster", "Torval", [{"target_id": "char_syndicate_torval", "relation": "brother"}], "Fences stolen Coalition weapons and rare mineral crates."),
    ("char_syndicate_armorer_babs", "Babs 'Hammer' Varek", "Anvil Boss", "scrap_metal_stamper", "Varek", [{"target_id": "char_syndicate_boss_varek", "relation": "sister"}], "Stamps stolen slag armor plates onto Hyena chassis frames."),
    ("char_syndicate_fuel_smuggler_vic", "Vic 'Vapor' Vance", "Fuel Rat", "tritium_bootlegger", "Vance", [{"target_id": "pilot_syndicate_jackal", "relation": "brother"}], "Jax Vance's younger brother who siphons gas from Jovian platforms."),
    ("char_syndicate_mine_foreman_grog", "Foreman Grog", "Rock-Crusher", "asteroid_labor_boss", "None", [], "Oversees deep-core slag mining operations in pirate asteroid belts."),
    ("char_syndicate_radio_pirate_rox", "Roxy 'Static'", "DJ Outlaw", "pirate_broadcaster", "None", [], "Broadcasts pirate rock and radar-warning alerts across the belt."),
    ("char_syndicate_shipbreaker_hulk", "Hulk Morgan", "Cutter", "derelict_shipbreaker", "Morgan", [{"target_id": "char_syndicate_skag_morgan", "relation": "son"}], "Cuts open abandoned capital ships with massive plasma torches."),
    ("char_syndicate_informant_whisper", "Whisper", "The Rat", "shadow_informant", "None", [], "Sells military patrol timetables to the highest bidder.")
]
for sid, name, call, role, dyn, kin, bio in SYNDICATE_SUPPORT:
    ROSTER.append(make_char(sid, name, call, "faction_syndicate", 2, role, False, dyn, kin, None, None, None, ["support_specialist"], "None", 0, 0, {"palette": "syndicate_rust_orange", "headgear": "welding_goggles", "scars": "soot_smudge", "eyes": "brown", "expression": "neutral"}, bio))

print(f"Generated Syndicate Cartel: {len(ROSTER)} characters total so far.")

# =============================================================================
# 4. APEX BIO-CYBERNETICS ZAIBATSU (48 FIGURES: 6 Command, 30 Recruitable Pilots, 12 Dynastic/Support)
# =============================================================================
# --- Zaibatsu Command & Leadership (6) ---
ROSTER.append(make_char(
    "char_zaibatsu_renzo", "Director Renzo Takahashi", "Executive Zero", "faction_zaibatsu", 4,
    "Executive VP of Special Weapons & Cybernetic R&D", False, "Takahashi",
    [{"target_id": "char_zaibatsu_ayumi_takahashi", "relation": "daughter"},
     {"target_id": "pilot_colony_jun_takahashi", "relation": "disowned_son"}],
    None, "pilot_zaibatsu_null07", "char_terran_sterling",
    ["corporate_coldness", "neural_implant_pioneer", "transhuman_visionary"], "ZX-22", 0, 0,
    {"palette": "zaibatsu_carbon_black", "headgear": "cybernetic_neural_temple_prongs", "scars": "none", "eyes": "synthetic_silver_optics", "expression": "cold_imperious"},
    "Architect of transhuman pilot interfaces. Views biological pilots as replaceable wetware."
))

ROSTER.append(make_char(
    "char_zaibatsu_vivienne", "Dr. Vivienne Chen", "The Neuro-Architect", "faction_zaibatsu", 4,
    "Chief Neural Architect & Cybernetic Surgeon", False, "Chen",
    [{"target_id": "char_zaibatsu_jin_chen", "relation": "brother"},
     {"target_id": "pilot_zaibatsu_null07", "relation": "creator_guardian"}],
    None, "pilot_zaibatsu_null07", "char_colony_lyra",
    ["neuro_surgeon_genius", "cognitive_suppression_master"], "None", 0, 0,
    {"palette": "zaibatsu_lab_white", "headgear": "surgical_holographic_specs", "scars": "none", "eyes": "cool_cyan_cybernetic", "expression": "detached_clinical"},
    "Designs synaptic leashes and brain-machine bridges that eliminate pilot fear and hesitation."
))

ROSTER.append(make_char(
    "char_zaibatsu_ayumi_takahashi", "Ayumi Takahashi", "The Heiress", "faction_zaibatsu", 3,
    "Executive VP of Acquisitions & Corporate Espionage", False, "Takahashi",
    [{"target_id": "char_zaibatsu_renzo", "relation": "father"}],
    None, "pilot_zaibatsu_maya", None,
    ["corporate_espionage", "predatory_acquisitions"], "ZM-11", 0, 0,
    {"palette": "zaibatsu_neon_violet", "headgear": "sleek_neural_earring_jack", "scars": "none", "eyes": "violet", "expression": "calculating_smirk"},
    "Renzo's daughter who orchestrates hostile corporate buyouts and pilot headhunting."
))

ROSTER.append(make_char(
    "char_zaibatsu_jin_chen", "Jin Chen", "Subject Zero", "faction_zaibatsu", 3,
    "Prototype Neural Cyber-Test Overseer", False, "Chen",
    [{"target_id": "char_zaibatsu_vivienne", "relation": "sister"}],
    None, None, None,
    ["early_cyber_prosthetic_pioneer", "phantom_latency_survivor"], "ZM-06", 0, 0,
    {"palette": "zaibatsu_chrome_grey", "headgear": "heavy_cranial_brace", "scars": "craniotomy_stitches", "eyes": "dull_grey", "expression": "stoic_enduring"},
    "Vivienne's brother who volunteered for the first generation of direct synaptic jacks."
))

ROSTER.append(make_char(
    "char_zaibatsu_kaito_mori", "Director Kaito Mori", "The Razor", "faction_zaibatsu", 3,
    "Corporate Security Disciplinary Director", False, "Mori",
    None, None, "pilot_zaibatsu_maya", "char_syndicate_cruz",
    ["monofilament_specialist", "uncompromising_enforcer"], "ZM-11", 0, 0,
    {"palette": "zaibatsu_carbon_black", "headgear": "tactical_visage_mask", "scars": "throat_line_scar", "eyes": "dark_slate", "expression": "unforgiving_blade"},
    "Enforces corporate non-disclosure agreements with high-frequency assassination squads."
))

ROSTER.append(make_char(
    "char_zaibatsu_shiro_kuroda", "Senior Board Member Kuroda", "The Shadow-Board", "faction_zaibatsu", 4,
    "Zaibatsu Executive Chairman", False, "Kuroda",
    None, None, None, "char_terran_sterling",
    ["boardroom_puppeteer", "monopoly_capitalist"], "None", 0, 0,
    {"palette": "zaibatsu_executive_gold", "headgear": "antique_sunglasses_wire", "scars": "none", "eyes": "hidden", "expression": "enigmatic_frown"},
    "Elder statesman of the Zaibatsu holding company who funds private mercenary proxy wars."
))

# --- Zaibatsu 30 Recruitable Pilots ---
ZAIBATSU_PILOTS_DATA = [
    ("pilot_zaibatsu_null07", "Null-07 (Ren)", "Neural-Zero", 3, "Transhuman Cyber-Ace", "ZX-22", 130000, 8200, ["zero_latency_synapse", "quantum_blade_mastery", "fractured_memory"], "char_zaibatsu_vivienne", "pilot_zaibatsu_maya", "pilot_colony_sorren", {"palette": "zaibatsu_carbon_black", "headgear": "neural_synapse_crown", "scars": "temple_interface_ports", "eyes": "glowing_crimson_optics", "expression": "haunted_unblinking"}, "Sub-nanometer cybernetic ace fighting through suppressed memories of their stolen past."),
    ("pilot_zaibatsu_maya", "Maya 'Kestrel' Zhao", "Kestrel", 3, "High-Frequency Monoblade Ace", "ZM-11", 100000, 6500, ["plasma_katana_crit", "stealth_baffle_ambush", "code_of_bushido"], "char_zaibatsu_kaito_mori", "pilot_zaibatsu_null07", "pilot_colony_helmut_zhao", {"palette": "zaibatsu_neon_violet", "headgear": "carbon_fiber_half_mask", "scars": "cheek_scratch", "eyes": "sharp_amber", "expression": "lethal_grace"}, "Admiral Zhao's estranged daughter, the deadliest monomolecular blade duelist in the solar system."),
    ("pilot_zaibatsu_kenji_sato", "Kenji Sato", "Razor-Edge", 2, "Monofilament Infiltrator", "ZM-11", 72000, 4600, ["critical_hit_boost", "optical_cloak_expert"], "char_zaibatsu_kaito_mori", "pilot_zaibatsu_maya", "pilot_terran_sergei_volkov", {"palette": "zaibatsu_carbon_black", "headgear": "low_profile_stealth_goggles", "scars": "none", "eyes": "dark_brown", "expression": "silent_focus"}, "Specializes in disabling enemy reactor heat vents with precision surgical slices."),
    ("pilot_zaibatsu_hana_mori", "Hana Mori", "Vibro-Fang", 2, "Security Duellist", "ZM-06", 65000, 4200, ["rapid_pdw_burst", "parry_riposte"], "char_zaibatsu_kaito_mori", "pilot_zaibatsu_maya", "pilot_colony_valentin_roux", {"palette": "zaibatsu_carbon_black", "headgear": "audio_sensor_hairband", "scars": "lip_cut", "eyes": "hazel", "expression": "arrogant_smirk"}, "Kaito Mori's niece, an executive escort pilot who neutralizes hostile hit squads."),
    ("pilot_zaibatsu_unit_14_echo", "Unit-14 (Echo)", "Echo-Pulse", 2, "Neural Reflex Test Pilot", "ZM-06", 62000, 4000, ["reflex_overclock", "synthetic_pain_block"], "char_zaibatsu_vivienne", "pilot_zaibatsu_null07", "pilot_terran_claudia_lang", {"palette": "zaibatsu_chrome_grey", "headgear": "cybernetic_mesh_bandage", "scars": "subdermal_implant_lumps", "eyes": "dilated_black", "expression": "vacant_stare"}, "Test pilot fitted with pain-inhibitor chips that allow combat past lethal thresholds."),
    ("pilot_zaibatsu_raiden_kenta", "Kenta Raiden", "Volt-Sniper", 3, "Extreme-Range Railgun Sniper", "ZMA-15", 105000, 6800, ["helium_cooled_sniper", "bipod_lock_perfection"], "char_zaibatsu_renzo", "pilot_zaibatsu_maya", "pilot_terran_liam_oconnor", {"palette": "zaibatsu_neon_violet", "headgear": "telemetry_monocle_right", "scars": "retinal_burn_scar", "eyes": "electric_blue", "expression": "ice_cold_aim"}, "Legendary sniper who shoots through cockpit blast doors from three kilometers away."),
    ("pilot_zaibatsu_ayako_shimizu", "Ayako Shimizu", "Ghost-Wire", 2, "Corporate ECM Saboteur", "ZM-11", 69000, 4400, ["radar_absorb_matrix", "ecm_scramble"], None, "pilot_zaibatsu_kenji_sato", "pilot_colony_selene_voss", {"palette": "zaibatsu_carbon_black", "headgear": "radar_baffle_hood", "scars": "none", "eyes": "dark_slate", "expression": "enigmatic_smile"}, "Employs radar-absorbing carbon baffles to slip past fortress automated turrets."),
    ("pilot_zaibatsu_ryo_kurata", "Ryo Kurata", "Plasma-Burn", 2, "Twin Plasma Carbine Gunner", "ZM-11", 68000, 4300, ["plasma_salvo_burst", "high_temp_dissipation"], "char_zaibatsu_renzo", None, "pilot_terran_sonia_reyes", {"palette": "zaibatsu_neon_violet", "headgear": "tinted_tactical_spectacles", "scars": "plasma_burn_forearm", "eyes": "brown", "expression": "haughty_confidence"}, "Melts enemy kinetic armor plates with continuous superheated plasma salvos."),
    ("pilot_zaibatsu_subject_09_kai", "Subject-09 (Kai)", "Mind-Shatter", 2, "Unstable Neural Brawler", "ZM-06", 64000, 4100, ["berserk_synapse", "suicidal_charge"], "char_zaibatsu_vivienne", "pilot_zaibatsu_null07", "pilot_syndicate_mad_dog_rocco", {"palette": "zaibatsu_chrome_grey", "headgear": "cranial_suppression_bolts", "scars": "scalp_electrode_scars", "eyes": "twitching_green", "expression": "frenzied_snarl"}, "Suffers from neural feedback loops that trigger terrifying berserk combat rushes."),
    ("pilot_zaibatsu_shizuka_takahashi", "Shizuka Takahashi", "Black-Lotus", 2, "High-Executive Escort Ace", "ZM-11", 76000, 4900, ["viper_strike", "executive_bodyguard"], "char_zaibatsu_renzo", "char_zaibatsu_ayumi_takahashi", "pilot_colony_astraea_vane", {"palette": "zaibatsu_carbon_black", "headgear": "lotus_crested_earpiece", "scars": "none", "eyes": "obsidian", "expression": "poised_deadly"}, "Renzo's niece, an elite assassin disguised as a corporate executive secretary."),
    ("pilot_zaibatsu_daiki_endo", "Daiki Endo", "Tachyon-Edge", 3, "Dual Tachyon Saber Master", "ZX-22", 112000, 7400, ["tachyon_blade_dance", "vernier_phase_shift"], "char_zaibatsu_renzo", "pilot_zaibatsu_null07", "pilot_colony_tariq_mansoor", {"palette": "zaibatsu_neon_violet", "headgear": "neural_comb_circlet", "scars": "forehead_seam", "eyes": "glowing_violet", "expression": "transhuman_scorn"}, "Replaced his motor cortex with superconductor chips for instantaneous sword parries."),
    ("pilot_zaibatsu_chiyo_noda", "Chiyo Noda", "Viper-PDW", 1, "Rapid Security Cadet", "ZM-06", 36000, 2300, ["caseless_ammo_cadence", "urban_sweep"], "char_zaibatsu_kaito_mori", "pilot_zaibatsu_hana_mori", "pilot_terran_arthur_pendleton", {"palette": "zaibatsu_carbon_black", "headgear": "lightweight_ear_comm", "scars": "none", "eyes": "dark_brown", "expression": "crisp_alert"}, "Academy graduate trained in close-quarters corporate building defense."),
    ("pilot_zaibatsu_kazuo_miura", "Kazuo Miura", "Iron-Baffle", 2, "Heavy Armor Corporate Enforcer", "ZM-11", 67000, 4300, ["composite_carbon_plate", "stun_baton_melee"], None, "pilot_zaibatsu_kenji_sato", "pilot_terran_hans_richter", {"palette": "zaibatsu_carbon_black", "headgear": "heavy_riot_visor", "scars": "jaw_fracture_scar", "eyes": "brown", "expression": "implacable_frown"}, "Suppresses factory strikes and labor riots with heavily reinforced Muramasa units."),
    ("pilot_zaibatsu_reiko_honda", "Reiko Honda", "Shadow-Sniper", 2, "Linear Rifle Recon", "ZMA-15", 73000, 4700, ["thermal_decoy_specialist", "camo_baffle"], "char_zaibatsu_renzo", "pilot_zaibatsu_raiden_kenta", "pilot_colony_chloe_duval", {"palette": "zaibatsu_carbon_black", "headgear": "sniper_veil_hood", "scars": "none", "eyes": "hazel", "expression": "serene_silence"}, "Employs thermal cloaking to eliminate high-value targets without revealing firing lines."),
    ("pilot_zaibatsu_shin_kuroda", "Shin Kuroda", "Gilded-Edge", 2, "Executive Duellist", "ZM-06", 74000, 4800, ["corporate_arrogance", "finely_tuned_servos"], "char_zaibatsu_shiro_kuroda", None, "pilot_terran_lucas_sterling", {"palette": "zaibatsu_executive_gold", "headgear": "gold_plated_headset", "scars": "none", "eyes": "amber", "expression": "condescending_smile"}, "Chairman Kuroda's nephew who pilots a gold-lacquered ZM-06 Ronin dueling frame."),
    ("pilot_zaibatsu_yuki_nagata", "Yuki Nagata", "Cryo-Baffle", 2, "Helium Coolant Technician Pilot", "ZMA-15", 66000, 4200, ["sub_zero_radiator", "continuous_fire"], "char_zaibatsu_vivienne", "pilot_zaibatsu_raiden_kenta", "pilot_terran_veronica_frost", {"palette": "zaibatsu_lab_white", "headgear": "cryo_respirator_tube", "scars": "frost_burn_cheek", "eyes": "pale_blue", "expression": "clinical_calm"}, "Monitors quantum core coolant levels during maximum standoff sniper bombardments."),
    ("pilot_zaibatsu_tetsuo_araki", "Tetsuo Araki", "Nanite-Fist", 2, "Cybernetic Grappler", "ZM-06", 63000, 4000, ["monomolecular_grip", "hydraulic_snap"], "char_zaibatsu_jin_chen", "pilot_zaibatsu_unit_14_echo", "pilot_syndicate_hammer_fist_otto", {"palette": "zaibatsu_chrome_grey", "headgear": "bionic_mandible_prosthetic", "scars": "synthetic_neck_cables", "eyes": "dark_slate", "expression": "metallic_grim"}, "Fitted with bionic grip servos capable of crushing titanium frame brackets bare-handed."),
    ("pilot_zaibatsu_naomi_inada", "Naomi Inada", "Strobe-Flash", 1, "Disruption Pilot", "ZM-06", 35000, 2200, ["flashbang_mortar_bonus", "sensor_blind"], None, "pilot_zaibatsu_chiyo_noda", "pilot_colony_esper_hale", {"palette": "zaibatsu_carbon_black", "headgear": "polarized_strobe_goggles", "scars": "none", "eyes": "brown", "expression": "sharp_smirk"}, "Blinds enemy pilots with high-intensity optical strobe flares before team strikes."),
    ("pilot_zaibatsu_genta_okada", "Genta Okada", "Black-Tide", 2, "High-Cycle Autocannon Enforcer", "ZM-11", 64000, 4100, ["pdw_saturation", "close_in_defense"], "char_zaibatsu_kaito_mori", None, "pilot_terran_karl_vogel", {"palette": "zaibatsu_carbon_black", "headgear": "tactical_ear_guards", "scars": "eyebrow_gash", "eyes": "dark_brown", "expression": "hardened_glare"}, "Specializes in laying down high-density 45mm caseless kinetic fire suppression."),
    ("pilot_zaibatsu_sayaka_mori", "Sayaka Mori", "Razor-Silk", 2, "Monofilament Net Deployer", "ZM-11", 71000, 4500, ["monowire_trap", "tactical_snare"], "char_zaibatsu_kaito_mori", "pilot_zaibatsu_maya", "pilot_syndicate_val_fang", {"palette": "zaibatsu_carbon_black", "headgear": "wire_spool_backpack_collar", "scars": "wire_cuts_fingers", "eyes": "amber", "expression": "predatory_smile"}, "Deploys razor-sharp monomolecular nets to sever limbs off charging assault suits."),
    ("pilot_zaibatsu_toru_matsuda", "Toru Matsuda", "Data-Siphon", 2, "Cyber Recon Specialist", "ZM-06", 61000, 3900, ["target_telemetry_share", "neural_uplink"], "char_zaibatsu_vivienne", "pilot_zaibatsu_ayako_shimizu", "pilot_terran_casper_lind", {"palette": "zaibatsu_neon_violet", "headgear": "cranial_data_antennae", "scars": "neck_jack_sockets", "eyes": "grey", "expression": "feverish_intellect"}, "Uploads real-time target telemetry directly to friendly squadron HUDs."),
    ("pilot_zaibatsu_madoka_kitano", "Madoka Kitano", "Tachyon-Ghost", 3, "Transhuman Stealth Ace", "ZX-22", 115000, 7600, ["zero_point_shift", "neural_drone_swarm"], "char_zaibatsu_renzo", "pilot_zaibatsu_null07", "pilot_colony_nyx_callisto", {"palette": "zaibatsu_carbon_black", "headgear": "neural_swarm_crown", "scars": "temple_burns", "eyes": "glowing_cyan", "expression": "serene_menace"}, "Controls eight autonomous neural swarm drones through direct synaptic thought."),
    ("pilot_zaibatsu_isamu_toba", "Isamu Toba", "Bio-Shock", 2, "EMP Disruptor Gunner", "ZM-06", 65000, 4200, ["emp_disruptor_specialist", "reactor_scramble"], None, "pilot_zaibatsu_kenji_sato", "pilot_terran_veronica_frost", {"palette": "zaibatsu_chrome_grey", "headgear": "insulating_rubber_collar", "scars": "electrical_burn_cheek", "eyes": "dark_brown", "expression": "calculating_gleam"}, "Shuts down enemy reactor regulators with localized electromagnetic pulses."),
    ("pilot_zaibatsu_mariko_asano", "Mariko Asano", "Executive-Blade", 2, "Corporate Honor Duelist", "ZM-11", 70000, 4500, ["dueling_etiquette", "monomolecular_crit"], "char_zaibatsu_kaito_mori", "pilot_zaibatsu_maya", "pilot_colony_valentin_roux", {"palette": "zaibatsu_executive_gold", "headgear": "gilded_hairpin_mic", "scars": "none", "eyes": "dark_slate", "expression": "scornful_elegance"}, "Settles multimillion-dollar corporate disputes via formal single combat duels."),
    ("pilot_zaibatsu_zenjiro_ohta", "Zenjiro Ohta", "Cyber-Vanguard", 2, "Line Breaching Enforcer", "ZM-11", 67000, 4300, ["aggressive_blade_rush", "armor_piercing_plasma"], "char_zaibatsu_kaito_mori", "pilot_zaibatsu_kazuo_miura", "pilot_terran_cole", {"palette": "zaibatsu_carbon_black", "headgear": "full_armored_cowl", "scars": "chin_split", "eyes": "brown", "expression": "implacable_fury"}, "Frontline corporate shock-trooper who slices through fortress gates."),
    ("pilot_zaibatsu_fubuki_takahashi", "Fubuki Takahashi", "Cold-Lotus", 1, "Security Recruit", "ZM-06", 38000, 2400, ["family_pride", "disciplined_aim"], "char_zaibatsu_renzo", "pilot_zaibatsu_shizuka_takahashi", "pilot_terran_tyler_vance", {"palette": "zaibatsu_carbon_black", "headgear": "sleek_comm_circlet", "scars": "none", "eyes": "obsidian", "expression": "proud_reserved"}, "Junior member of the Takahashi family eager to earn a corporate director seat."),
    ("pilot_zaibatsu_gen_kudo", "Gen Kudo", "Chrome-Fang", 2, "Cybernetic Melee Fighter", "ZM-06", 62000, 4000, ["hydraulic_kick", "vibro_blade_rend"], "char_zaibatsu_jin_chen", "pilot_zaibatsu_tetsuo_araki", "pilot_syndicate_katja_slit", {"palette": "zaibatsu_chrome_grey", "headgear": "chrome_plated_jaw", "scars": "neck_welds", "eyes": "one_bionic_blue", "expression": "feral_sneer"}, "Replaced both legs and lower jaw with titanium combat prosthetics."),
    ("pilot_zaibatsu_erika_nomura", "Erika Nomura", "Plasma-Whip", 2, "Mid-Range Thermal Gunner", "ZM-11", 69000, 4400, ["continuous_beam_whip", "thermal_stress"], None, "pilot_zaibatsu_ryo_kurata", "pilot_syndicate_nadia", {"palette": "zaibatsu_neon_violet", "headgear": "thermal_dissipation_collar", "scars": "burn_shoulder", "eyes": "hazel", "expression": "cruel_smirk"}, "Lashes enemy limbs with sustained high-frequency plasma beams until armor melts."),
    ("pilot_zaibatsu_satoshi_endo", "Satoshi Endo", "Linear-God", 3, "Super-Velocity Rail Specialist", "ZMA-15", 108000, 7100, ["kinetic_rod_penetration", "recoil_nullifier"], "char_zaibatsu_renzo", "pilot_zaibatsu_raiden_kenta", "pilot_terran_helen_braun", {"palette": "zaibatsu_carbon_black", "headgear": "orbital_telemetry_hud", "scars": "brow_shrapnel_dots", "eyes": "grey", "expression": "godlike_arrogance"}, "Views long-range sniping as the ultimate form of corporate capital liquidation."),
    ("pilot_zaibatsu_omega_susanoo_prime", "Cyber-Dominator Susanoo-X", "Omega Prime", 4, "Transhuman Singularity Cyberframe", "ZX-22", 150000, 9800, ["singularity_core_overdrive", "tachyon_godhood", "mind_eater_strike"], "char_zaibatsu_renzo", "pilot_zaibatsu_null07", "char_terran_vance", {"palette": "zaibatsu_carbon_black", "headgear": "quantum_singularity_mask", "scars": "full_cranial_silver_mesh", "eyes": "dual_crimson_lasers", "expression": "unfeeling_machine_god"}, "Apex culmination of transhuman cyber-warfare; moves with relativistic precision.")
]

for p in ZAIBATSU_PILOTS_DATA:
    pid, name, call, tier, role, pref, hire, sal, traits, mentor, wing, rival, snes, bio = p
    dynasty = "Takahashi" if "Takahashi" in name else ("Chen" if "Chen" in name else ("Mori" if "Mori" in name else ("Kuroda" if "Kuroda" in name else None)))
    kin = []
    if dynasty == "Takahashi":
        kin.append({"target_id": "char_zaibatsu_renzo", "relation": "dynasty_member"})
    elif dynasty == "Chen":
        kin.append({"target_id": "char_zaibatsu_vivienne", "relation": "dynasty_member"})
    elif dynasty == "Mori":
        kin.append({"target_id": "char_zaibatsu_kaito_mori", "relation": "dynasty_member"})
    elif dynasty == "Kuroda":
        kin.append({"target_id": "char_zaibatsu_shiro_kuroda", "relation": "dynasty_member"})
    ROSTER.append(make_char(pid, name, call, "faction_zaibatsu", tier, role, True, dynasty, kin, mentor, wing, rival, traits, pref, hire, sal, snes, bio))

# Add 12 Zaibatsu Support Figures
ZAIBATSU_SUPPORT = [
    ("char_zaibatsu_legal_vp_tanaka", "VP Ken Tanaka", "The Contract", "chief_legal_counsel", "None", [], "Drafts binding corporate mercenary contracts with devastating non-compete clauses."),
    ("char_zaibatsu_neuro_surgeon_fujita", "Dr. Yosuke Fujita", "The Scalpel", "cybernetic_neurosurgeon", "None", [], "Performs synaptic bridge installations on candidate pilots."),
    ("char_zaibatsu_ai_arch_minerva", "Engineer Minerva Vance-Chen", "Core-Weaver", "ai_integration_chief", "Chen", [{"target_id": "char_zaibatsu_vivienne", "relation": "niece"}], "Synthesizes bio-neural network firmware for combat mobile suits."),
    ("char_zaibatsu_board_liaison_hisa", "Director Hisa Mori", "The Auditor", "boardroom_liaison", "Mori", [{"target_id": "char_zaibatsu_kaito_mori", "relation": "sister"}], "Monitors combat sortie profit-margins for the executive board."),
    ("char_zaibatsu_quartermaster_shin", "Quartermaster Shin", "Nano-Vault", "advanced_materials_broker", "None", [], "Oversees high-purity Adamantine Carbide and Tritium reserves."),
    ("char_zaibatsu_pr_director_emi", "Emi Takahashi", "Silver Tongue", "media_spin_director", "Takahashi", [{"target_id": "char_zaibatsu_renzo", "relation": "daughter"}], "Controls solar-wide news broadcasts covering up collateral damage."),
    ("char_zaibatsu_nanite_eng_yoshida", "Dr. Yoshida", "Molecular Smith", "monofilament_metallurgist", "None", [], "Forges molecular-edge plasma katana blades in zero-G vacuum labs."),
    ("char_zaibatsu_clone_overseer_unit0", "Overseer-00", "The Cradle", "clone_matrix_warden", "None", [], "Maintains synthetic clone pilot incubators in deep Martian vaults."),
    ("char_zaibatsu_security_warden_goro", "Warden Goro", "The Collar", "neural_penitentiary_chief", "None", [], "Tracks runaway cybernetic test subjects who escape corporate campuses."),
    ("char_zaibatsu_subcontractor_vogel", "Broker Vogel-Takahashi", "The Fixer", "black_budget_fixer", "Takahashi", [], "Channels untraceable corporate funds to mercenary contractors."),
    ("char_zaibatsu_quantum_crypt_aya", "Aya Chen", "Cipher", "quantum_cryptographer", "Chen", [{"target_id": "char_zaibatsu_vivienne", "relation": "daughter"}], "Cracks enemy military communication ciphers in real-time during sorties."),
    ("char_zaibatsu_recovery_chief_jin", "Commander Jinbo", "The Eraser", "asset_recovery_chief", "None", [], "Retrieves wrecked mobile suit black boxes before competitors can salvage them.")
]
for sid, name, call, role, dyn, kin, bio in ZAIBATSU_SUPPORT:
    ROSTER.append(make_char(sid, name, call, "faction_zaibatsu", 2, role, False, dyn, kin, None, None, None, ["support_specialist"], "None", 0, 0, {"palette": "zaibatsu_carbon_black", "headgear": "sleek_visor_specs", "scars": "none", "eyes": "synthetic_silver_optics", "expression": "neutral"}, bio))

# =============================================================================
# 5. INDEPENDENT MERCENARIES & ROGUE DRIFTERS (12 LEGENDARY FIGURES)
# =============================================================================
INDEPENDENT_FIGURES = [
    ("pilot_indep_vance_outlaw", "Captain Silas Vance", "Gray-Ghost", 3, "Freelance Linebreaker", "bp_player_vanguard_heavy", 115000, 7500, ["freelance_loyalty", "veteran_instinct", "heavy_recoil_soak"], "Vance", [{"target_id": "char_terran_vance", "relation": "estranged_cousin"}], "Disavowed Coalition commander who sells heavy siege armor services to the highest bidder."),
    ("pilot_indep_starlight_ronin", "Miyamoto 'Zero' Vance", "Ceres-Ronin", 3, "Wandering Plasma Swordmaster", "bp_player_ghost_sniper", 120000, 7800, ["wandering_blade", "critical_parry", "unbound_mercenary"], "Vance", [{"target_id": "pilot_syndicate_jackal", "relation": "blood_brother"}], "Drifting duelist who wanders asteroid cantinas looking for worthy champions."),
    ("pilot_indep_helena_valk", "Helena 'Valkyrie' Thorne", "Free-Flight", 3, "High-G Orbital Gun-for-Hire", "bp_player_stratos_interceptor", 118000, 7600, ["unshackled_vector", "particle_fury"], "Thorne", [{"target_id": "char_colony_lyra", "relation": "estranged_sister"}], "Former Colony flight leader who turned mercenary after habitat taxation riots."),
    ("pilot_indep_iron_jaw_boris", "Boris 'Iron-Jaw' Rostov", "Old War-Hound", 3, "Armored Breacher Mercenary", "bp_player_scrapper_brawler", 108000, 7000, ["shrapnel_veteran", "cockpit_crusher"], "Rostov", [{"target_id": "pilot_terran_rostova", "relation": "disgraced_uncle"}], "Disgraced Coalition major fighting under mercenary flags across the asteroid rim."),
    ("pilot_indep_smuggler_queen_cruz", "Carmen Cruz", "Shadow-Runner", 2, "Stealth Cargo Raider", "SCR-05", 78000, 5000, ["blockade_runner", "stealth_drift"], "Cruz", [{"target_id": "char_syndicate_cruz", "relation": "cousin"}], "Freebooter captain who smuggles forbidden high-tier alloy ingots across planetary blockades."),
    ("pilot_indep_cyborg_kage", "Kage-00", "Cyber-Ronin", 3, "Rogue Transhuman Assassin", "bp_player_ghost_sniper", 125000, 8000, ["hacked_neural_leash", "monoblade_decapitator"], "None", [{"target_id": "pilot_zaibatsu_null07", "relation": "former_lab_mate"}], "Escaped Zaibatsu test subject whose neural collar was severed by EMP blasts."),
    ("pilot_indep_old_miner_toby", "Old Toby", "Drill-Master", 2, "Heavy Excavation Brawler", "bp_player_scrapper_brawler", 62000, 4000, ["mining_drill_melee", "debris_crusher"], "None", [], "Veteran miner who turned his ore-crusher into a devastating anti-mech war-rig."),
    ("pilot_indep_sol_corsair_jill", "Jill 'Corsair' Morgan", "Void-Cat", 2, "Pneumatic Harpoon Raider", "SCR-12", 74000, 4800, ["harpoon_breach", "zero_g_acrobatics"], "Morgan", [{"target_id": "char_syndicate_skag_morgan", "relation": "daughter"}], "Independent pirate captain who raids corporate supply convoys on deep-space slingshots."),
    ("pilot_indep_tachyon_wraith", "Wraith-99", "Tachyon-Wraith", 3, "Experimental Beam Sniper", "bp_player_stratos_interceptor", 122000, 7900, ["tachyon_sniping", "ghost_radar"], "None", [], "Mysterious wandering pilot piloting an unmarked experimental particle interceptor."),
    ("pilot_indep_foundry_exile_ortiz", "Carlos Ortiz", "Crucible-Exile", 2, "Slag Demolition Gunner", "bp_player_scrapper_brawler", 71000, 4600, ["incendiary_ram", "boiler_overclock"], "Ortiz", [{"target_id": "char_syndicate_mateo_ortiz", "relation": "nephew"}], "Exiled foundry worker who welds heavy iron plating over salvaged chassis."),
    ("pilot_indep_senate_deserter_fallon", "Major Lucas Fallon", "Renegade Hawk", 3, "Heavy Railgun Linebreaker", "bp_player_vanguard_heavy", 112000, 7300, ["military_tactician", "kinetic_penetration"], "None", [{"target_id": "pilot_terran_beatrice_fallon", "relation": "brother"}], "Refused orders to fire on civilian miners and founded an independent contractor company."),
    ("pilot_indep_transhuman_nomad_jin", "Jin Takahashi-Chen", "The Hybrid", 4, "Supreme Independent Vanguard", "bp_player_ghost_sniper", 145000, 9500, ["hybrid_neural_chassis", "monoblade_singularity", "free_agent_legend"], "Takahashi", [{"target_id": "char_zaibatsu_renzo", "relation": "renegade_grandson"}], "Legendary freelance ace whose frame combines Terran tungsten plating with Zaibatsu neural drives.")
]

for p in INDEPENDENT_FIGURES:
    pid, name, call, tier, role, pref, hire, sal, traits, dyn, kin, bio = p
    snes = {"palette": "indep_mercenary_grey", "headgear": "battered_flight_helmet", "scars": "veteran_slash", "eyes": "steely_amber", "expression": "cynical_independent"}
    ROSTER.append(make_char(pid, name, call, "independent", tier, role, True, dyn, kin, None, None, None, traits, pref, hire, sal, snes, bio))

# =============================================================================
# Write Roster to JSON
# =============================================================================
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump({"total_figures": len(ROSTER), "characters": ROSTER}, f, indent=4)

print(f"\n=======================================================")
print(f"SUCCESS: Generated {len(ROSTER)} characters into {OUT_PATH}")
print(f"=======================================================")
