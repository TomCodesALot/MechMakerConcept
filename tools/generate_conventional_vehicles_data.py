import json
import os

vehicles_data = {
    "version": "1.0.0",
    "era": "ERA_0_CONVENTIONAL",
    "vehicles": [
        # Terran Coalition
        {
            "id": "veh_terran_mammoth",
            "name": "T-720 'Mammoth' Heavy Battle Tank",
            "short_name": "MAMMOTH MBT",
            "faction_id": "faction_terran",
            "type": "tank",
            "propulsion": "QUAD_TREAD",
            "sprite_asset": "spr_veh_terran_mammoth_idle",
            "back_sprite_asset": "spr_veh_terran_mammoth_back_idle",
            "ap": 4,
            "accuracy": 78,
            "evasion": 22,
            "armor": 38,
            "components": {
                "torso": {"name": "Sloped Heavy Glacis", "hp": 520, "armor": 38},
                "head": {"name": "Dual 120mm Turret", "hp": 240, "armor": 30},
                "arm_left": {"name": "Sponson Heavy Vulcan", "hp": 220, "armor": 25},
                "arm_right": {"name": "Coaxial Autocannon", "hp": 220, "armor": 25},
                "legs": {"name": "Quad Heavy Treads", "hp": 480, "armor": 35},
                "backpack": {"name": "Diesel-Turbine Pack", "hp": 180, "armor": 20}
            },
            "weapons": [
                {
                    "name": "Twin 120mm Rifled Cannons",
                    "short_name": "TWIN 120MM",
                    "proj_type": "KINETIC_CANNON",
                    "ap_cost": 3,
                    "heat_cost": 0,
                    "range_min": 2,
                    "range_max": 6,
                    "damage": 140,
                    "anim_state": "fire_rifle",
                    "desc": "Heavy twin solid-shot bombardment."
                },
                {
                    "name": "Coaxial Heavy Autocannon",
                    "short_name": "COAXIAL AC",
                    "proj_type": "ROTARY_VULCAN",
                    "ap_cost": 2,
                    "heat_cost": 0,
                    "range_min": 1,
                    "range_max": 4,
                    "damage": 75,
                    "anim_state": "fire_chaingun",
                    "desc": "High velocity suppression fire."
                }
            ],
            "description": "The Terran Coalition's frontline armored sledgehammer. Thick sloped armor shrugs off small arms, but turning and rough terrain traversal are ponderous."
        },
        {
            "id": "veh_terran_skyhammer",
            "name": "A-14 'Skyhammer' Strike Jet",
            "short_name": "SKYHAMMER JET",
            "faction_id": "faction_terran",
            "type": "jet",
            "propulsion": "FLIGHT",
            "sprite_asset": "spr_veh_terran_skyhammer_idle",
            "back_sprite_asset": "spr_veh_terran_skyhammer_back_idle",
            "ap": 7,
            "accuracy": 84,
            "evasion": 55,
            "armor": 20,
            "components": {
                "torso": {"name": "Titanium Armored Tub", "hp": 320, "armor": 20},
                "head": {"name": "Avionics Radar Nose", "hp": 140, "armor": 14},
                "arm_left": {"name": "Port Wing Hardpoint", "hp": 180, "armor": 16},
                "arm_right": {"name": "Starboard Wing Hardpoint", "hp": 180, "armor": 16},
                "legs": {"name": "Twin Turbofan Engines", "hp": 260, "armor": 18},
                "backpack": {"name": "Decoy Flare Dispenser", "hp": 150, "armor": 12}
            },
            "weapons": [
                {
                    "name": "GAU-30mm Heavy Rotary",
                    "short_name": "GAU-30MM",
                    "proj_type": "ROTARY_VULCAN",
                    "ap_cost": 3,
                    "heat_cost": 0,
                    "range_min": 1,
                    "range_max": 5,
                    "damage": 115,
                    "anim_state": "fire_chaingun",
                    "desc": "Tank-shredding depleted uranium burst."
                },
                {
                    "name": "Heavy Unguided Rocket Salvo",
                    "short_name": "ROCKET SALVO",
                    "proj_type": "MICRO_MISSILE",
                    "ap_cost": 3,
                    "heat_cost": 0,
                    "range_min": 2,
                    "range_max": 6,
                    "damage": 160,
                    "anim_state": "fire_missiles",
                    "desc": "Parabolic ground-strike cluster."
                }
            ],
            "description": "Armored close-air-support jet designed to break entrenched defensive positions with devastating strafing runs."
        },

        # Outer Colonies
        {
            "id": "veh_colony_stiletto",
            "name": "K-4 'Stiletto' Rapid Attack Skiff",
            "short_name": "STILETTO SKIFF",
            "faction_id": "faction_colony",
            "type": "skiff",
            "propulsion": "HOVER",
            "sprite_asset": "spr_veh_colony_stiletto_idle",
            "back_sprite_asset": "spr_veh_colony_stiletto_back_idle",
            "ap": 7,
            "accuracy": 86,
            "evasion": 65,
            "armor": 16,
            "components": {
                "torso": {"name": "Aerodynamic Skiff Hull", "hp": 310, "armor": 16},
                "head": {"name": "Sensor Mast", "hp": 120, "armor": 12},
                "arm_left": {"name": "Port Linear Railgun", "hp": 150, "armor": 14},
                "arm_right": {"name": "Starboard Linear Railgun", "hp": 150, "armor": 14},
                "legs": {"name": "Repulsor Hover Skirts", "hp": 340, "armor": 16},
                "backpack": {"name": "Liquid Booster", "hp": 160, "armor": 12}
            },
            "weapons": [
                {
                    "name": "Twin 60mm Linear Railguns",
                    "short_name": "TWIN RAIL",
                    "proj_type": "RAILGUN_SLUG",
                    "ap_cost": 3,
                    "heat_cost": 0,
                    "range_min": 2,
                    "range_max": 7,
                    "damage": 130,
                    "anim_state": "fire_rifle",
                    "desc": "High velocity sabot flechette."
                },
                {
                    "name": "Point-Defense Flak",
                    "short_name": "PD FLAK",
                    "proj_type": "ROTARY_VULCAN",
                    "ap_cost": 2,
                    "heat_cost": 0,
                    "range_min": 1,
                    "range_max": 3,
                    "damage": 65,
                    "anim_state": "fire_chaingun",
                    "desc": "Rapid defensive curtain."
                }
            ],
            "description": "High-speed ground-effect hover platform utilized by Colonial defense militia to out-maneuver heavy Terran armor across plains and waterways."
        },
        {
            "id": "veh_colony_dart",
            "name": "S-10 'Dart' Hypersonic Interceptor",
            "short_name": "DART JET",
            "faction_id": "faction_colony",
            "type": "jet",
            "propulsion": "FLIGHT",
            "sprite_asset": "spr_veh_colony_dart_idle",
            "back_sprite_asset": "spr_veh_colony_dart_back_idle",
            "ap": 8,
            "accuracy": 88,
            "evasion": 72,
            "armor": 14,
            "components": {
                "torso": {"name": "Delta-Wing Fuselage", "hp": 280, "armor": 14},
                "head": {"name": "Intercept Radar Dome", "hp": 110, "armor": 10},
                "arm_left": {"name": "Port Beam Emitter", "hp": 160, "armor": 12},
                "arm_right": {"name": "Starboard Beam Emitter", "hp": 160, "armor": 12},
                "legs": {"name": "Vectored Afterburner", "hp": 240, "armor": 14},
                "backpack": {"name": "ECM Frequency Jammer", "hp": 140, "armor": 10}
            },
            "weapons": [
                {
                    "name": "Coherent Pulse Laser Pylons",
                    "short_name": "PULSE LASER",
                    "proj_type": "BEAM_PULSE",
                    "ap_cost": 3,
                    "heat_cost": 0,
                    "range_min": 1,
                    "range_max": 6,
                    "damage": 145,
                    "anim_state": "fire_beam",
                    "desc": "High intensity energy lance."
                },
                {
                    "name": "Colony Interceptor Missiles",
                    "short_name": "INT MISSILES",
                    "proj_type": "MICRO_MISSILE",
                    "ap_cost": 3,
                    "heat_cost": 0,
                    "range_min": 2,
                    "range_max": 7,
                    "damage": 135,
                    "anim_state": "fire_missiles",
                    "desc": "Agile radar homing missiles."
                }
            ],
            "description": "Colonial aerospace fighter capable of trans-atmospheric operations, prioritizing extreme speed and early directed-energy weaponry."
        },

        # Rogue Mercenary Syndicates / Outlaws
        {
            "id": "veh_syndicate_technical",
            "name": "SCR-T01 'Rustfang' Armored Technical",
            "short_name": "RUSTFANG TRUCK",
            "faction_id": "faction_syndicate",
            "type": "technical",
            "propulsion": "WHEELED",
            "sprite_asset": "spr_veh_syndicate_technical_idle",
            "back_sprite_asset": "spr_veh_syndicate_technical_back_idle",
            "ap": 6,
            "accuracy": 72,
            "evasion": 54,
            "armor": 18,
            "components": {
                "torso": {"name": "Reinforced Flatbed Hull", "hp": 290, "armor": 18},
                "head": {"name": "Gunner Armor Shield", "hp": 110, "armor": 14},
                "arm_left": {"name": "Pintle Autocannon", "hp": 130, "armor": 12},
                "arm_right": {"name": "Scrap Rocket Rack", "hp": 130, "armor": 12},
                "legs": {"name": "All-Terrain Heavy Tires", "hp": 280, "armor": 15},
                "backpack": {"name": "Nitrous Injection Rig", "hp": 130, "armor": 10}
            },
            "weapons": [
                {
                    "name": "Scrapper 50mm Flak Cannon",
                    "short_name": "50MM FLAK",
                    "proj_type": "ROTARY_VULCAN",
                    "ap_cost": 2,
                    "heat_cost": 0,
                    "range_min": 1,
                    "range_max": 4,
                    "damage": 95,
                    "anim_state": "fire_chaingun",
                    "desc": "Scrap shrapnel spray."
                },
                {
                    "name": "Jury-Rigged Rocket Salvo",
                    "short_name": "SCRAP ROCKETS",
                    "proj_type": "MICRO_MISSILE",
                    "ap_cost": 3,
                    "heat_cost": 0,
                    "range_min": 2,
                    "range_max": 5,
                    "damage": 135,
                    "anim_state": "fire_missiles",
                    "desc": "Improvised high explosive rockets."
                }
            ],
            "description": "Mass-produced guerrilla gun truck made of welded salvage and heavy industrial suspensions, lethal in roving packs."
        },

        # Apex Zaibatsu
        {
            "id": "veh_zaibatsu_kurogane",
            "name": "Type-94 'Kurogane' Drone Tank",
            "short_name": "KUROGANE DRONE",
            "faction_id": "faction_zaibatsu",
            "type": "tank",
            "propulsion": "RUBBER_TREAD",
            "sprite_asset": "spr_veh_zaibatsu_kurogane_idle",
            "back_sprite_asset": "spr_veh_zaibatsu_kurogane_back_idle",
            "ap": 5,
            "accuracy": 88,
            "evasion": 52,
            "armor": 26,
            "components": {
                "torso": {"name": "Carbon Monocoque Chasis", "hp": 360, "armor": 26},
                "head": {"name": "AI Quantum Sensor Dome", "hp": 140, "armor": 20},
                "arm_left": {"name": "Micro-Missile Well", "hp": 190, "armor": 22},
                "arm_right": {"name": "Hypersonic Railgun Pylon", "hp": 200, "armor": 22},
                "legs": {"name": "Silent Rubber Tracks", "hp": 380, "armor": 24},
                "backpack": {"name": "Active Optical Camo Pack", "hp": 170, "armor": 16}
            },
            "weapons": [
                {
                    "name": "75mm Hypersonic Railgun",
                    "short_name": "75MM RAILGUN",
                    "proj_type": "RAILGUN_SLUG",
                    "ap_cost": 3,
                    "heat_cost": 0,
                    "range_min": 2,
                    "range_max": 8,
                    "damage": 170,
                    "anim_state": "fire_rifle",
                    "desc": "Precision kinetic slug fired via electromagnetic rails."
                },
                {
                    "name": "Zaibatsu Swarm Cluster",
                    "short_name": "DRONE SWARM",
                    "proj_type": "MICRO_MISSILE",
                    "ap_cost": 3,
                    "heat_cost": 0,
                    "range_min": 1,
                    "range_max": 5,
                    "damage": 125,
                    "anim_state": "fire_missiles",
                    "desc": "Smart-guided micro munitions."
                }
            ],
            "description": "Unmanned, automated stealth combat platform utilizing quantum AI predictive tracking and active acoustic dampening."
        }
    ]
}

os.makedirs("datafiles", exist_ok=True)
with open("datafiles/conventional_vehicles.json", "w") as f:
    json.dump(vehicles_data, f, indent=2)

print("Generated datafiles/conventional_vehicles.json with 6 canonical vehicle archetypes.")
