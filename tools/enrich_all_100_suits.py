#!/usr/bin/env python3
import json
import os
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT_PATHS = [
    os.path.join(BASE_DIR, "datafiles/mobile_suits/mobile_suit_catalog.json"),
    os.path.join(BASE_DIR, "datafiles/mobile_suit_catalog.json")
]

with open(CAT_PATHS[0], "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Load bespoke dictionary from previous tool
import tools.generate_mobile_suit_lore_database as gmsld
bespoke = gmsld.BESPOKE_LORE

# Procedural Lore Templates per Faction and Role
FACTION_TEMPLATES = {
    "faction_a": { # Terran Combine / Valkyrie Heavy Industries
        "mfg_lore": [
            "Commissioned under the Terran Military Council to fortify Earth's planetary perimeter against insurgent fleets. Valkyrie Heavy Industries opted for heavy layered composite alloy armor, heavy diesel-fusion thermal turbines, and high-caliber rifled ballistics capable of holding entrenched ground redoubts under continuous orbital bombardments.",
            "Developed at the Lake Baikal metallurgical complex during the height of the Lunar border disputes. Its structural design emphasizes sheer mass and redundant hydraulic circuitry, ensuring the machine remains operational even after catastrophic armor breaches across secondary limbs.",
            "Designed by Ural Defense Dynamics as a counter to agile zero-gravity Colony incursions. The chassis integrates reinforced recoil dampeners and heavy kinetic armor plating, sacrificing top-speed maneuverability for unyielding structural integrity."
        ],
        "quirks": [
            "Heavy frontal armor plates cause chronic stress fractures on forward knee actuator bearings during high-g descent landings; maintenance crews routinely reinforce the limb pins with field-welded tungsten rods.",
            "The main diesel-fusion boiler vents dense superheated steam through dorsal baffles, creating a distinctive thermal plume that infrared scanners can track for kilometers.",
            "Recoil forces from the primary heavy cannon shake loose cabin telemetry wiring harnesses; pilots are taught to kick the lower dashboard console to reset failing sensor readouts.",
            "Coolant lines in the hip joints are prone to freezing in sub-zero lunar or Siberian conditions, requiring grease monkeys to pre-heat the limbs with plasma torches before morning sorties."
        ],
        "reputation": [
            "Known affectionately by ground grunts as 'The Iron Wall' and cursed by rookie pilots as a brutal, unforgiving machine that punishes over-eager maneuvering.",
            "Opposing Colony skirmishers mock its sluggish ground pace until its 120mm solid shot punches through their light aerosteel bulkheads at extreme ranges.",
            "Mercenaries consider it the most reliable machine in the Sol system—impossible to flip, impossible to crush, and simple enough to repair with scrap and an arc welder.",
            "Pilots nickname its cockpit 'The Iron Sarcophagus' because surviving a direct hit often leaves the hatches warped shut until extraction teams torch them open."
        ],
        "theaters": [
            ["Baikal Redoubt", "Copernicus Lunar Base", "Low Earth Orbit Fortress Rings"],
            ["Ural Trench Network", "Mare Crisium Crater", "Kamchatka Defense Arc"],
            ["Gobi Desert Proving Grounds", "Pacific Floating Hub", "Sub-Orbital Drop Corridors"]
        ]
    },
    "faction_b": { # Colony Coalition / Astraea Orbital Dynamics
        "mfg_lore": [
            "Conceived in the zero-G orbital foundries of L-5 by Astraea Orbital Dynamics. Rejecting Earth's obsolete heavy armor philosophy, Colony engineers utilized hyper-light aerosteel matrices, Cherenkov blue plasma thrusters, and superconductive particle conduits for supreme vacuum agility.",
            "Engineered by Jovian Construction Corp to safeguard deep-space mining colonies from Terran boarding operations. The suit leverages revolutionary vernier cluster arrays that allow instantaneous 360-degree vector changes without bleeding momentum.",
            "Born from Selene Vector Laboratories as a high-speed skirmishing doctrine. The design prioritizes particle beam efficiency and rapid heat dissipation, allowing it to harass enemy capital formations from beyond counter-battery range."
        ],
        "quirks": [
            "The Cherenkov superconductor core induces slight magnetic interference with the pilot's helmet comms, creating a faint, rhythmic whine dubbed the 'Jovian Chorus'.",
            "Continuous micro-vernier burns create rapid fuel cell pressure fluctuations that require pilots to manually feather the thruster valves during dogfights.",
            "The lightweight aerosteel chassis is prone to micro-fracturing under high atmospheric drag; pilots must disengage limiter clamps before attempting high-speed atmospheric dives.",
            "Optical sensor pods require recalibration after high-energy beam discharges due to residual thermal blooming across the fore-camera lenses."
        ],
        "reputation": [
            "Admired across the Jovian colonies as an elegant guardian of freedom; Terran tank crews call it 'The Flying Scalpel' for its precision beam attacks.",
            "Pilots praise its feather-light handling and breathtaking roll rates, though veteran aces caution that one solid kinetic hit will fold the frame in half.",
            "Mercenaries love its high salvage value; black market cartels pay top dollar for intact Astraea superconducting capacitor banks and vernier nozzles.",
            "Considered the gold standard for zero-G dogfighting; aces who master its high-frequency pitch controls can evade entire missile salvos without taking armor damage."
        ],
        "theaters": [
            ["L-5 Orbital Gateway", "Jovian Ring Platforms", "Archimedes Lagrange Corridor"],
            ["Callisto Deep Mining Station", "Ganymede Logistics Belt", "High Lunar Orbit"],
            ["Europa Cryo-Refinery Arc", "Lagrange Point 4", "Deep Void Patrol Sector"]
        ]
    },
    "faction_c": { # Asteroid Syndicate / Rustworks Salvage Cartel
        "mfg_lore": [
            "Jury-rigged across lawless asteroid shipyards by the Rustworks Salvage Cartel. Constructed from welded derelict transport hulls, repurposed industrial mining claws, and contraband military reactors, the chassis reflects the brutal, scavenged survival ethos of the Asteroid Belt.",
            "Assembled in clandestine asteroid hollows by the Asteroid Reclamation Guild. Designed to outlast corporate attrition, its frame features asymmetrical slag armor plates and heavy pneumatic harpoon winches designed for boarding raids and piracy.",
            "Engineered by the Ceres Iron Outlaws as an intimidating shock-assault platform. With dual rotary flak cannons and spiked kinetic ramming cowls, it excels at terrorizing civilian trade convoys and ambushing corporate supply lines."
        ],
        "quirks": [
            "Asymmetrical scrap plating creates an off-center center-of-gravity; pilots must learn to compensate for a persistent leftward yaw during boost maneuvers.",
            "Cockpit seals are often patched with industrial sealant tape and re-welded bulkhead scraps; cabin pressure alarms frequently sound false warnings in vacuum.",
            "The scavenged reactor runs hot and loud, occasionally venting caustic sulfurous exhaust directly past the cockpit intake filters.",
            "Ammunition feed chutes for the heavy flak cannons tend to jam if low-grade non-standard propellant rounds are loaded under high-g maneuvers."
        ],
        "reputation": [
            "Feared by merchant convoy captains across the Sol system; the harsh shriek of its pneumatic boarding harpoon usually signals total cargo confiscation.",
            "Pilots wear their suits' battle scars and mismatched armor plates like badges of honor, boasting that no corporate cleanroom suit has the guts to brawl at point-blank range.",
            "Terran and Colony militaries officially designate it as 'Irregular Terror Armor', advising pilots to destroy them on sight rather than negotiate.",
            "Mercenaries nickname it 'The Junkyard Dog'—ugly, loud, and vicious, with an uncanny ability to keep crawling forward after losing half its torso armor."
        ],
        "theaters": [
            ["Ceres Mining Outposts", "Vesta Debris Belt", "Trojan Asteroid Corridors"],
            ["Deimos Wreckage Graveyard", "Pallas Smuggling Hub", "Outer Kuiper Gateway"],
            ["Psyche Heavy Metal Drift", "Sector 7 Scrap Fields", "Inner Belt Ambush Corridors"]
        ]
    },
    "faction_d": { # Mars Zaibatsu / Hyperion Advanced Tactical Systems
        "mfg_lore": [
            "Engineered in the high-security orbital labs of Olympus Mons by Hyperion Advanced Tactical Systems. Created to enforce corporate dominance through ruthless surgical precision, the suit integrates bio-neural cockpit synchronization, sub-zero liquid nitrogen coolant loops, and high-frequency tachyon blade weaponry.",
            "Developed by Takahashi Cybernetics as the apex tool of corporate espionage and elite dueling. Its bio-synthetic neural link allows the pilot's subconscious reflexes to guide the machine's limbs with near-instantaneous reaction latencies.",
            "Designed by Olympus Mons Precision Armory to execute high-value asset decapitations. Featuring advanced optical refraction camo and hyper-focused electromagnetic rail weapons, it strikes from total sensory concealment before vanishing into the Martian red dust."
        ],
        "quirks": [
            "The direct neural link causes intense sensory phantom feedback in pilots; extended combat operations without cybernetic cerebellum dampers cause severe migraines.",
            "Sub-zero liquid nitrogen cooling jackets frost over the external armor seams, creating a ghostly white mist during high-output blade ignition.",
            "High-frequency blade emitters consume massive energy spikes, momentarily dimming cabin displays and HUD overlays upon activation.",
            "Optical camouflage refractor panels degrade quickly if scratched by abrasive Martian dust storms, requiring meticulous cleanroom polishing between missions."
        ],
        "reputation": [
            "Known with dread in corporate boardrooms as 'The Black Scalpel'. When a Zaibatsu duel chassis appears on the horizon, corporate rival executives quickly settle their contracts.",
            "Enemy pilots report that fighting one feels unnatural—it anticipates firing angles and missile trajectories before human reaction times would allow.",
            "Mercenaries speak of it in hushed tones, warning that duelists trained in the Olympus Mons academies fight with cold, mathematical precision and zero mercy.",
            "Corporate pilots regard piloting one as the pinnacle of military prestige, treating their chassis with the ritual reverence of an ancestral samurai blade."
        ],
        "theaters": [
            ["Olympus Mons Redoubt", "Phobos Deep Vaults", "Syrtis Major Corporate Corridor"],
            ["Valles Marineris Chasm", "Hellas Planitia Basin", "Cydonia Research Sector"],
            ["Tharsis Volcanic Plateau", "Deimos Listening Station", "Mars High Orbital Array"]
        ]
    }
}

# Update all 100 suits
for sid, suit in catalog.items():
    fac = suit.get("faction_id", "faction_a")
    if fac not in FACTION_TEMPLATES and fac != "pmc_player":
        fac = "faction_a" # fallback

    # Check if bespoke exists
    if sid in bespoke:
        b = bespoke[sid]
        suit["historical_lore"] = b["historical_lore"]
        suit["manufacturing_quirks"] = b["manufacturing_quirks"]
        suit["battlefield_reputation"] = b["battlefield_reputation"]
        suit["doctrine_summary"] = b["doctrine_summary"]
        suit["production_count"] = b["production_count"]
        suit["active_units"] = b["active_units"]
        suit["casualty_count"] = b["casualty_count"]
        suit["kill_count"] = b["kill_count"]
        suit["adoption_status"] = b["adoption_status"]
        suit["primary_theaters"] = b["primary_theaters"]
    else:
        # Generate rich contextual lore from template
        tm = FACTION_TEMPLATES[fac]
        tmpl_mfg = random.choice(tm["mfg_lore"])
        tmpl_q = random.choice(tm["quirks"])
        tmpl_rep = random.choice(tm["reputation"])
        tmpl_th = random.choice(tm["theaters"])

        sname = suit.get("name", "Mobile Suit")
        srole = suit.get("chassis_class", "Assault")
        mfg = suit.get("manufacturer", "Defense Syndicate")

        suit["historical_lore"] = f"{sname} was manufactured by {mfg} to fill the critical role of {srole}. {tmpl_mfg}"
        suit["manufacturing_quirks"] = tmpl_q
        suit["battlefield_reputation"] = tmpl_rep
        suit["doctrine_summary"] = f"{srole} doctrine tailored for {fac} strategic objectives."

        # Scale production and stats based on unit profile
        is_mp = suit.get("mass_production_line", False)
        is_custom = ("custom" in sid.lower() or "prime" in sid.lower() or "ace" in sid.lower() or "x01" in sid.lower())
        era = suit.get("era", 2)

        if is_mp:
            prod = random.randint(2800, 5200)
            active = round(prod * random.uniform(0.65, 0.85))
            cas = prod - active
            kills = round(cas * random.uniform(0.9, 1.4))
            status = "standard_issue"
        elif is_custom:
            prod = random.randint(45, 180)
            active = round(prod * random.uniform(0.70, 0.90))
            cas = prod - active
            kills = round(cas * random.uniform(2.5, 5.0))
            status = "ace_custom"
        else: # specialized / support
            prod = random.randint(450, 1600)
            active = round(prod * random.uniform(0.60, 0.80))
            cas = prod - active
            kills = round(cas * random.uniform(1.0, 1.8))
            status = "specialized_deployment"

        suit["production_count"] = prod
        suit["active_units"] = active
        suit["casualty_count"] = cas
        suit["kill_count"] = kills
        suit["adoption_status"] = status
        suit["primary_theaters"] = tmpl_th

    # Calculated metrics
    suit["combat_loss_ratio"] = round((suit["casualty_count"] / max(1, suit["kill_count"])) * 100.0) / 100.0
    suit["survivability_rating"] = round(100.0 * suit["kill_count"] / max(1, suit["kill_count"] + suit["casualty_count"]))
    suit["replaced_by"] = ""
    suit["adoption_turn"] = 0

    # Dynamic lore chronicle list
    suit["dynamic_lore_chronicle"] = [
        f"[Cycle 1 - COMMISSION] Officially logged in system military registries with {suit['production_count']:,} units manufactured ({suit['active_units']:,} active in field). Status: {suit['adoption_status'].upper()}."
    ]

# Save to both catalog locations
for p in CAT_PATHS:
    with open(p, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
    print(f"Saved enriched catalog to {p}")

print("Successfully enriched all 100 mobile suits with rich narrative lore and global statistics!")
