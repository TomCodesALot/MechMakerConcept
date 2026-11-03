import os
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATHS = [
    os.path.join(ROOT_DIR, "datafiles", "mobile_suit_catalog.json"),
    os.path.join(ROOT_DIR, "datafiles", "mobile_suits", "mobile_suit_catalog.json")
]

# Base Chassis Mapping by (Faction, Era)
BASE_CHASSIS_MAP = {
    "faction_a": {
        1: "spr_ms_trenchcoat_idle",
        2: "spr_ms_ironclad_idle",
        3: "spr_ms_ballista_idle",
        4: "spr_ms_titan_proto"
    },
    "faction_b": {
        1: "spr_ms_kepler_idle",
        2: "spr_ms_aether_idle",
        3: "spr_ms_oberon_idle",
        4: "spr_ms_zephyr_idle"
    },
    "faction_c": {
        1: "spr_ms_vandal_idle",
        2: "spr_ms_hyena_idle",
        3: "spr_ms_gorgon_idle",
        4: "spr_ms_bloodhound_idle"
    },
    "faction_d": {
        1: "spr_ms_kage_idle",
        2: "spr_ms_muramasa_idle",
        3: "spr_ms_tessen_idle",
        4: "spr_ms_ronin_idle"
    }
}

# Standardized Weapon Overlay Mapping by Faction and Doctrine Role
WEAPON_MAP = {
    "faction_a": {
        "primary_kinetic": "spr_wpn_tc_carbine_90mm",
        "support_heavy": "spr_wpn_tc_cannon_150mm",
        "shield_defense": "spr_wpn_tc_tower_shield"
    },
    "faction_b": {
        "primary_beam": "spr_wpn_ocl_beam_spray",
        "support_lance": "spr_wpn_ocl_beam_lance",
        "shield_wing": "spr_wpn_ocl_deflector_wing"
    },
    "faction_c": {
        "primary_flechette": "spr_wpn_rsc_scrap_flechette",
        "support_harpoon": "spr_wpn_rsc_harpoon_winch",
        "shield_saw": "spr_wpn_rsc_rock_saw"
    },
    "faction_d": {
        "primary_needle": "spr_wpn_abc_needle_pistol",
        "melee_katana": "spr_wpn_abc_tachyon_katana",
        "shield_tessen": "spr_wpn_abc_tessen_fan"
    }
}

def migrate_catalog():
    with open(CATALOG_PATHS[0], "r") as f:
        catalog = json.load(f)

    updated_count = 0
    for suit_id, s in catalog.items():
        fac = s.get("faction_id", "faction_a")
        era = s.get("era", 2)
        chassis_class = s.get("chassis_class", "").lower()
        suit_name = s.get("name", "").lower()

        # 1. Resolve Era-Appropriate Base Chassis
        if fac in BASE_CHASSIS_MAP:
            # Special Ace overrides
            if "centurion" in suit_id or "praetorian" in suit_id:
                base_spr = "spr_ms_centurion_idle"
            elif "hephaestus" in suit_id or "prewar" in suit_id:
                base_spr = "spr_ms_hephaestus_avatar"
            elif "siegebreaker" in suit_id:
                base_spr = "spr_ms_ballista_idle"
            elif "ironclad" in suit_id and era == 2:
                base_spr = "spr_ms_ironclad_idle"
            elif "aether" in suit_id and era == 2:
                base_spr = "spr_ms_aether_idle"
            elif "muramasa" in suit_id and era == 2:
                base_spr = "spr_ms_muramasa_idle"
            elif "hyena" in suit_id and era == 2:
                base_spr = "spr_ms_hyena_idle"
            else:
                base_spr = BASE_CHASSIS_MAP[fac].get(era, BASE_CHASSIS_MAP[fac][2])
            
            s["sprite_asset"] = base_spr
            s["base_chassis_id"] = base_spr.replace("_idle", "")
            s["chassis_era"] = era

        # 2. Re-arm with strict Gundam-Style Faction Doctrine & Assign Weapon Overlays
        if fac == "faction_a":
            # Terran Coalition (Kinetic, Heavy, Shield)
            if era == 1:
                # Gen 1 Grunt: 90mm Carbine + Tower Shield OR Howitzer Only
                if "ballista" in suit_id or "mortar" in suit_id or "artillery" in suit_name:
                    s["primary_weapon"] = "Type-33 150mm Recoil Howitzer"
                    s["secondary_weapon"] = "Ground Stabilizer Spades"
                    s["weapon_overlay_primary"] = WEAPON_MAP["faction_a"]["support_heavy"]
                    s["weapon_overlay_secondary"] = ""
                    s["doctrine"] = "Fixed Field Artillery & Siege Support"
                elif "trench" in suit_id or "shotgun" in suit_id:
                    s["primary_weapon"] = "Type-45 90mm Kinetic Carbine"
                    s["secondary_weapon"] = "Cast-Steel Riot Tower Shield"
                    s["weapon_overlay_primary"] = WEAPON_MAP["faction_a"]["primary_kinetic"]
                    s["weapon_overlay_secondary"] = WEAPON_MAP["faction_a"]["shield_defense"]
                    s["doctrine"] = "Trench Breaching & CQC Defense"
                else:
                    s["primary_weapon"] = "Type-45 90mm Kinetic Carbine"
                    s["secondary_weapon"] = "Cast-Steel Riot Tower Shield"
                    s["weapon_overlay_primary"] = WEAPON_MAP["faction_a"]["primary_kinetic"]
                    s["weapon_overlay_secondary"] = WEAPON_MAP["faction_a"]["shield_defense"]
                    s["doctrine"] = "Standard Trench Line Infantry"
            elif era == 2:
                # Gen 2 Trooper: 120mm Autocannon + Shield or Rotary Vulcan
                if "centurion" in suit_id:
                    s["primary_weapon"] = "GAU-88 Rotary Heavy Vulcan"
                    s["secondary_weapon"] = "Cast-Alloy Tower Shield"
                    s["weapon_overlay_primary"] = WEAPON_MAP["faction_a"]["primary_kinetic"]
                    s["weapon_overlay_secondary"] = WEAPON_MAP["faction_a"]["shield_defense"]
                else:
                    s["primary_weapon"] = "Type-77 120mm Heavy Autocannon"
                    s["secondary_weapon"] = "Reinforced Cast Tower Shield"
                    s["weapon_overlay_primary"] = WEAPON_MAP["faction_a"]["primary_kinetic"]
                    s["weapon_overlay_secondary"] = WEAPON_MAP["faction_a"]["shield_defense"]
                s["doctrine"] = "Heavy Breakthrough & Attrition Anchor"
            else:
                # Gen 3-4 Heavy Support & Titan Fortress
                s["weapon_overlay_primary"] = WEAPON_MAP["faction_a"]["support_heavy"]
                s["weapon_overlay_secondary"] = WEAPON_MAP["faction_a"]["shield_defense"]

        elif fac == "faction_b":
            # Outer Colony League (Energy, Beam, Deflector Wing)
            if era == 1:
                # Gen 1 Scout: Beam Spray Gun + Light Deflector or Needle Sniper
                if "kepler" in suit_id or "sniper" in suit_name:
                    s["primary_weapon"] = "Long-Barrel Linear Beam Rifle"
                    s["secondary_weapon"] = "Targeting Sensor Monocle"
                    s["weapon_overlay_primary"] = WEAPON_MAP["faction_b"]["support_lance"]
                    s["weapon_overlay_secondary"] = ""
                    s["doctrine"] = "Zero-G Long-Range Reconnaissance"
                else:
                    s["primary_weapon"] = "Focused Pulse Beam Spray Gun"
                    s["secondary_weapon"] = "Ceramic Vernier Deflector Wing"
                    s["weapon_overlay_primary"] = WEAPON_MAP["faction_b"]["primary_beam"]
                    s["weapon_overlay_secondary"] = WEAPON_MAP["faction_b"]["shield_wing"]
                    s["doctrine"] = "Orbital Patrol & Light Skirmishing"
            elif era == 2:
                s["primary_weapon"] = "Continuous-Wave Beam Lance"
                s["secondary_weapon"] = "Ceramic Vernier Deflector Wing"
                s["weapon_overlay_primary"] = WEAPON_MAP["faction_b"]["support_lance"]
                s["weapon_overlay_secondary"] = WEAPON_MAP["faction_b"]["shield_wing"]
                s["doctrine"] = "High-Mobility Zero-G Interception"
            else:
                s["weapon_overlay_primary"] = WEAPON_MAP["faction_b"]["support_lance"]
                s["weapon_overlay_secondary"] = WEAPON_MAP["faction_b"]["shield_wing"]

        elif fac == "faction_c":
            # Rust Syndicate Cartel (Scrap, Flechette, Harpoon, Saw)
            if era == 1:
                # Gen 1 Scrapper: Flechette Gun + Rock Saw
                s["primary_weapon"] = "60mm Scrap Flechette Gun"
                s["secondary_weapon"] = "Thermite Rock-Saw Buckler"
                s["weapon_overlay_primary"] = WEAPON_MAP["faction_c"]["primary_flechette"]
                s["weapon_overlay_secondary"] = WEAPON_MAP["faction_c"]["shield_saw"]
                s["doctrine"] = "Asteroid Scrap Harvesting & Ambush"
            elif era == 2:
                s["primary_weapon"] = "Pneumatic Harpoon Winch"
                s["secondary_weapon"] = "Thermite Rock-Saw Buckler"
                s["weapon_overlay_primary"] = WEAPON_MAP["faction_c"]["support_harpoon"]
                s["weapon_overlay_secondary"] = WEAPON_MAP["faction_c"]["shield_saw"]
                s["doctrine"] = "Boarding Action & Hull Breaching"
            else:
                s["weapon_overlay_primary"] = WEAPON_MAP["faction_c"]["support_harpoon"]
                s["weapon_overlay_secondary"] = WEAPON_MAP["faction_c"]["shield_saw"]

        elif fac == "faction_d":
            # Apex Zaibatsu (Needle, Tachyon Blade, EMP Fan)
            if era == 1:
                # Gen 1 Infiltrator: Subsonic Needle Pistol + EMP Fan
                s["primary_weapon"] = "Subsonic Kinetic Needle Pistol"
                s["secondary_weapon"] = "Armored Tessen EMP Fan"
                s["weapon_overlay_primary"] = WEAPON_MAP["faction_d"]["primary_needle"]
                s["weapon_overlay_secondary"] = WEAPON_MAP["faction_d"]["shield_tessen"]
                s["doctrine"] = "Black-Ops Infiltration & Electronic Sabotage"
            elif era == 2:
                s["primary_weapon"] = "High-Frequency Tachyon Katana"
                s["secondary_weapon"] = "Armored Tessen EMP Fan"
                s["weapon_overlay_primary"] = WEAPON_MAP["faction_d"]["melee_katana"]
                s["weapon_overlay_secondary"] = WEAPON_MAP["faction_d"]["shield_tessen"]
                s["doctrine"] = "High-Speed Tactical Assassination"
            else:
                s["weapon_overlay_primary"] = WEAPON_MAP["faction_d"]["melee_katana"]
                s["weapon_overlay_secondary"] = WEAPON_MAP["faction_d"]["shield_tessen"]

        elif fac == "pmc_player":
            # Player custom blueprints
            s["weapon_overlay_primary"] = "spr_wpn_tc_carbine_90mm"
            s["weapon_overlay_secondary"] = "spr_wpn_tc_tower_shield"

        updated_count += 1

    for path in CATALOG_PATHS:
        with open(path, "w") as f:
            json.dump(catalog, f, indent=2)
        print(f"Successfully migrated {updated_count} suits in: {path}")

if __name__ == "__main__":
    migrate_catalog()
