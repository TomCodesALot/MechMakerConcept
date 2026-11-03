import json

with open("datafiles/conventional_vehicles.json", "r") as f:
    data = json.load(f)

new_units = [
    # Terran Mechanized Infantry Squad
    {
        "id": "inf_terran_squad",
        "name": "Terran 88th Mechanized Infantry Squad",
        "short_name": "TERRAN INFANTRY",
        "faction_id": "faction_terran",
        "type": "infantry",
        "propulsion": "FOOT_SOLDIER",
        "sprite_asset": "spr_inf_terran_squad_idle",
        "back_sprite_asset": "spr_inf_terran_squad_back_idle",
        "is_infantry": True,
        "ap": 4,
        "accuracy": 82,
        "evasion": 45,
        "armor": 12,
        "components": {
            "torso": {"name": "Squad Integrity", "hp": 220, "armor": 12},
            "head": {"name": "Squad Leader & Comms", "hp": 90, "armor": 10},
            "arm_left": {"name": "GAU-50mm Machine Gun", "hp": 110, "armor": 10},
            "arm_right": {"name": "Shoulder ATGM Launcher", "hp": 120, "armor": 10},
            "legs": {"name": "Combat Mobility", "hp": 180, "armor": 10},
            "backpack": {"name": "Munitions Rucksacks", "hp": 100, "armor": 8}
        },
        "weapons": [
            {
                "name": "Heavy Anti-Tank Missile (ATGM)",
                "short_name": "HEAVY ATGM",
                "proj_type": "MICRO_MISSILE",
                "ap_cost": 3,
                "heat_cost": 0,
                "range_min": 2,
                "range_max": 6,
                "damage": 155,
                "anim_state": "fire_missiles",
                "desc": "High explosive shaped charge guided missile designed to punch through tank armor."
            },
            {
                "name": "Squad Machine Gun Volley",
                "short_name": "SQUAD MG",
                "proj_type": "ROTARY_VULCAN",
                "ap_cost": 2,
                "heat_cost": 0,
                "range_min": 1,
                "range_max": 4,
                "damage": 70,
                "anim_state": "fire_chaingun",
                "desc": "Suppression fire from riflemen and heavy gunner."
            }
        ],
        "description": "Entrenched 4-soldier infantry fireteam behind reinforced sandbags. Vulnerable to direct HE artillery, but lethal against armored vehicles using heavy shoulder rockets."
    },

    # Colony Void Jump Infantry
    {
        "id": "inf_colony_squad",
        "name": "Colonial Void Jump Skirmishers",
        "short_name": "COLONY INFANTRY",
        "faction_id": "faction_colony",
        "type": "infantry",
        "propulsion": "JUMP_PACK",
        "sprite_asset": "spr_inf_colony_squad_idle",
        "back_sprite_asset": "spr_inf_colony_squad_back_idle",
        "is_infantry": True,
        "ap": 6,
        "accuracy": 85,
        "evasion": 62,
        "armor": 10,
        "components": {
            "torso": {"name": "Pressurized Void Suits", "hp": 200, "armor": 10},
            "head": {"name": "Targeting HUD Helmets", "hp": 85, "armor": 8},
            "arm_left": {"name": "Pulse Carbines", "hp": 100, "armor": 8},
            "arm_right": {"name": "Linear Shaped Charges", "hp": 110, "armor": 8},
            "legs": {"name": "Pneumatic Jump Struts", "hp": 160, "armor": 8},
            "backpack": {"name": "Vernier Thruster Packs", "hp": 110, "armor": 8}
        },
        "weapons": [
            {
                "name": "Linear Pulse Carbines",
                "short_name": "PULSE CARBINE",
                "proj_type": "BEAM_PULSE",
                "ap_cost": 2,
                "heat_cost": 0,
                "range_min": 1,
                "range_max": 5,
                "damage": 85,
                "anim_state": "fire_beam",
                "desc": "High velocity coherent energy pulses."
            },
            {
                "name": "Micro-Demolition Charge",
                "short_name": "DEMO CHARGE",
                "proj_type": "MELEE",
                "ap_cost": 3,
                "heat_cost": 0,
                "range_min": 1,
                "range_max": 1,
                "damage": 170,
                "anim_state": "melee",
                "desc": "Zero-G magnetic limpet mine clamped directly onto enemy chassis."
            }
        ],
        "description": "High-mobility orbital skirmishers equipped with vernier thrusters capable of bounding over obstacles and flanking entrenched positions."
    },

    # Syndicate Guerrilla Militia
    {
        "id": "inf_syndicate_squad",
        "name": "Syndicate Guerrilla Scrap Militia",
        "short_name": "SCRAP MILITIA",
        "faction_id": "faction_syndicate",
        "type": "infantry",
        "propulsion": "FOOT_SOLDIER",
        "sprite_asset": "spr_inf_syndicate_squad_idle",
        "back_sprite_asset": "spr_inf_syndicate_squad_back_idle",
        "is_infantry": True,
        "ap": 5,
        "accuracy": 74,
        "evasion": 52,
        "armor": 14,
        "components": {
            "torso": {"name": "Scrap Iron Cuirasses", "hp": 210, "armor": 14},
            "head": {"name": "Welded Gas Masks", "hp": 90, "armor": 10},
            "arm_left": {"name": "Sawn-off Autocannons", "hp": 105, "armor": 10},
            "arm_right": {"name": "Improvised RPG Tube", "hp": 115, "armor": 10},
            "legs": {"name": "Combat Boots", "hp": 170, "armor": 10},
            "backpack": {"name": "Stick Grenade Harness", "hp": 95, "armor": 8}
        },
        "weapons": [
            {
                "name": "Improvised Scrap RPG",
                "short_name": "SCRAP RPG",
                "proj_type": "MICRO_MISSILE",
                "ap_cost": 3,
                "heat_cost": 0,
                "range_min": 1,
                "range_max": 5,
                "damage": 140,
                "anim_state": "fire_missiles",
                "desc": "Heavy welded rocket with unstable shaped explosive charge."
            },
            {
                "name": "Nail-Bomb Cluster",
                "short_name": "NAIL BOMB",
                "proj_type": "ROTARY_VULCAN",
                "ap_cost": 2,
                "heat_cost": 0,
                "range_min": 1,
                "range_max": 3,
                "damage": 80,
                "anim_state": "fire_chaingun",
                "desc": "Lethal shrapnel grenade barrage."
            }
        ],
        "description": "Roving guerrilla irregulars armed with black-market munitions and jury-rigged anti-vehicle weapons."
    },

    # Zaibatsu Cybernetic Android Squad
    {
        "id": "inf_zaibatsu_squad",
        "name": "Zaibatsu Cybernetic Android Squad",
        "short_name": "CYBER SQUAD",
        "faction_id": "faction_zaibatsu",
        "type": "infantry",
        "propulsion": "FOOT_SOLDIER",
        "sprite_asset": "spr_inf_zaibatsu_squad_idle",
        "back_sprite_asset": "spr_inf_zaibatsu_squad_back_idle",
        "is_infantry": True,
        "ap": 5,
        "accuracy": 88,
        "evasion": 58,
        "armor": 18,
        "components": {
            "torso": {"name": "Carbon Monocoque Frame", "hp": 240, "armor": 18},
            "head": {"name": "Optic Neural Sensor", "hp": 100, "armor": 16},
            "arm_left": {"name": "Forearm Rail-Needle", "hp": 120, "armor": 14},
            "arm_right": {"name": "Forearm Rail-Needle", "hp": 120, "armor": 14},
            "legs": {"name": "Hydraulic Bipod Limbs", "hp": 190, "armor": 14},
            "backpack": {"name": "Capacitor Battery Pack", "hp": 120, "armor": 12}
        },
        "weapons": [
            {
                "name": "Hypersonic Rail-Needles",
                "short_name": "RAIL NEEDLE",
                "proj_type": "RAILGUN_SLUG",
                "ap_cost": 2,
                "heat_cost": 0,
                "range_min": 2,
                "range_max": 7,
                "damage": 110,
                "anim_state": "fire_rifle",
                "desc": "Surgical flechettes propelled by miniature electromagnetic coils."
            },
            {
                "name": "Monofilament Snare",
                "short_name": "MONO SNARE",
                "proj_type": "MELEE",
                "ap_cost": 2,
                "heat_cost": 0,
                "range_min": 1,
                "range_max": 1,
                "damage": 135,
                "anim_state": "melee",
                "desc": "Molecularly sharp wire snare that slices actuator joints."
            }
        ],
        "description": "Autonomous android combat units programmed with synchronized quantum hivemind algorithms."
    },

    # Colony V-88 Valkyrie Gunship
    {
        "id": "veh_colony_gunship",
        "name": "V-88 'Valkyrie' Heavy Tilt-Rotor Gunship",
        "short_name": "VALKYRIE GUNSHIP",
        "faction_id": "faction_colony",
        "type": "aircraft",
        "propulsion": "FLIGHT",
        "sprite_asset": "spr_veh_colony_gunship_idle",
        "back_sprite_asset": "spr_veh_colony_gunship_back_idle",
        "is_aircraft": True,
        "ap": 7,
        "accuracy": 84,
        "evasion": 58,
        "armor": 22,
        "components": {
            "torso": {"name": "Armored Troop Fuselage", "hp": 380, "armor": 22},
            "head": {"name": "Chin Sensor & Cockpit", "hp": 150, "armor": 18},
            "arm_left": {"name": "Port Wing Tilt-Rotor", "hp": 210, "armor": 16},
            "arm_right": {"name": "Starboard Tilt-Rotor", "hp": 210, "armor": 16},
            "legs": {"name": "Turbine Lift Engine", "hp": 280, "armor": 18},
            "backpack": {"name": "Flare Countermeasures", "hp": 160, "armor": 14}
        },
        "weapons": [
            {
                "name": "Chin 25mm Rotary Gatling",
                "short_name": "25MM GATLING",
                "proj_type": "ROTARY_VULCAN",
                "ap_cost": 2,
                "heat_cost": 0,
                "range_min": 1,
                "range_max": 5,
                "damage": 95,
                "anim_state": "fire_chaingun",
                "desc": "High rate-of-fire suppression."
            },
            {
                "name": "Heavy Homing Rocket Pod",
                "short_name": "POD MISSILES",
                "proj_type": "MICRO_MISSILE",
                "ap_cost": 4,
                "heat_cost": 0,
                "range_min": 2,
                "range_max": 7,
                "damage": 175,
                "anim_state": "fire_missiles",
                "desc": "Sustained anti-armor missile salvo."
            }
        ],
        "description": "Twin tilt-rotor heavy gunship providing close air support and rapid troop transport."
    },

    # Syndicate Buzzard Light Bomber
    {
        "id": "veh_syndicate_bomber",
        "name": "SCR-B03 'Buzzard' Scrap Light Bomber",
        "short_name": "BUZZARD BOMBER",
        "faction_id": "faction_syndicate",
        "type": "aircraft",
        "propulsion": "FLIGHT",
        "sprite_asset": "spr_veh_syndicate_bomber_idle",
        "back_sprite_asset": "spr_veh_syndicate_bomber_back_idle",
        "is_aircraft": True,
        "ap": 6,
        "accuracy": 72,
        "evasion": 50,
        "armor": 16,
        "components": {
            "torso": {"name": "Welded Twin-Boom Hull", "hp": 300, "armor": 16},
            "head": {"name": "Exposed Radial Cockpit", "hp": 120, "armor": 12},
            "arm_left": {"name": "Port Bomb Pylon", "hp": 160, "armor": 12},
            "arm_right": {"name": "Starboard Bomb Pylon", "hp": 160, "armor": 12},
            "legs": {"name": "Piston Radial Engine", "hp": 240, "armor": 14},
            "backpack": {"name": "Aux Fuel Drums", "hp": 130, "armor": 10}
        },
        "weapons": [
            {
                "name": "Incendiary Slag Cluster",
                "short_name": "SLAG BOMBS",
                "proj_type": "KINETIC_CANNON",
                "ap_cost": 3,
                "heat_cost": 0,
                "range_min": 2,
                "range_max": 6,
                "damage": 150,
                "anim_state": "fire_flak",
                "desc": "Improvised incendiary fuel drums dropped from low altitude."
            }
        ],
        "description": "Rusted twin-boom atmospheric strike aircraft rigged with demolition ordnance."
    },

    # Zaibatsu Kamaitachi Stealth Drone Jet
    {
        "id": "veh_zaibatsu_drone_jet",
        "name": "Type-02 'Kamaitachi' Stealth Drone Jet",
        "short_name": "KAMAITACHI DRONE",
        "faction_id": "faction_zaibatsu",
        "type": "aircraft",
        "propulsion": "FLIGHT",
        "sprite_asset": "spr_veh_zaibatsu_drone_jet_idle",
        "back_sprite_asset": "spr_veh_zaibatsu_drone_jet_back_idle",
        "is_aircraft": True,
        "ap": 8,
        "accuracy": 90,
        "evasion": 75,
        "armor": 14,
        "components": {
            "torso": {"name": "Diamond Carbon Wing", "hp": 270, "armor": 14},
            "head": {"name": "AI Flight Core", "hp": 110, "armor": 12},
            "arm_left": {"name": "Internal Missile Bay L", "hp": 150, "armor": 12},
            "arm_right": {"name": "Internal Missile Bay R", "hp": 150, "armor": 12},
            "legs": {"name": "Ion Vector Thruster", "hp": 230, "armor": 12},
            "backpack": {"name": "Optical Cloak Emitter", "hp": 140, "armor": 10}
        },
        "weapons": [
            {
                "name": "Stealth Micro-Torpedoes",
                "short_name": "TORPEDOES",
                "proj_type": "MICRO_MISSILE",
                "ap_cost": 3,
                "heat_cost": 0,
                "range_min": 2,
                "range_max": 7,
                "damage": 145,
                "anim_state": "fire_missiles",
                "desc": "Low radar cross-section guided kinetic torpedoes."
            }
        ],
        "description": "Unmanned swept-wing combat drone designed for precision decapitation strikes."
    }
]

existing_ids = {u["id"] for u in data["vehicles"]}
for u in new_units:
    if u["id"] not in existing_ids:
        data["vehicles"].append(u)

with open("datafiles/conventional_vehicles.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"conventional_vehicles.json expanded! Total units: {len(data['vehicles'])}.")
