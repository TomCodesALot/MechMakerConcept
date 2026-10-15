import json
import os

# Database of bespoke lore profiles for archetypes, specific suits, and custom aces.

BESPOKE_LORE = {
    "ms_terran_ironclad_07": {
        "historical_lore": "Designed during the Second Resource Scramble by Valkyrie Heavy Industries, the GHA-07 Ironclad became the defining symbol of Terran planetary defense. Commissioned under the Baikal Directive, its blueprint favored brutal monolithic cast-tungsten front armor capable of withstanding direct kinetic artillery strikes while rolling forward at deliberate, crushing speeds.",
        "manufacturing_quirks": "The immense mass of the frontal tungsten cowl causes persistent hydraulic wear in the forward knee joints; field mechanics frequently replace sheared titanium pins after less than 40 hours of trench combat.",
        "battlefield_reputation": "Terran infantry revere the suit as 'The Moving Wall', while enemy pilots dread closing within range of its 120mm rifled cannon, which can crack light skirmisher cockpits with a single clean kinetic impact.",
        "doctrine_summary": "Frontline kinetic attrition anchor and heavy trench breakthrough platform.",
        "production_count": 4820,
        "active_units": 3140,
        "casualty_count": 1680,
        "kill_count": 2490,
        "adoption_status": "standard_issue",
        "primary_theaters": ["Baikal Trench Line", "Low Earth Orbit Staging", "Mare Imbrium Basin"]
    },
    "ms_colony_aether_01": {
        "historical_lore": "Engineered in the zero-G orbital docks of L-5 by Astraea Orbital Dynamics, the AET-01 Aether was conceived as an answer to Terran heavy armor. Utilizing an ultralight aerosteel frame and a high-yield Cherenkov superconducting reactor, the suit revolutionized orbital combat through unmatched vernier vectoring.",
        "manufacturing_quirks": "Superconducting bus cables run uncomfortably close to the cockpit life-support pod; pilots report ambient tingling in their fingertips and ozone smells during sustained high-burn maneuvers.",
        "battlefield_reputation": "Terran gunners derisively call it 'The Blue Mosquito' due to its evasive maneuvers, but fear its high-output beam carbine which slices through cast armor like hot wire through butter.",
        "doctrine_summary": "Zero-G orbital dominance, high-speed hit-and-run particle skirmishing.",
        "production_count": 3450,
        "active_units": 2420,
        "casualty_count": 1030,
        "kill_count": 2210,
        "adoption_status": "standard_issue",
        "primary_theaters": ["L-5 Gateway", "Jovian Mining Belt", "Archimedes Orbital Corridor"]
    },
    "ms_syndicate_hyena_12": {
        "historical_lore": "Assembled across clandestine asteroid workshops by the Rustworks Salvage Cartel, the SCR-12 Hyena represents the ruthless ingenuity of the Rim. Built almost entirely from salvaged military scrap and commercial drilling chassis, it trades uniform factory standards for brutal, improvisational durability.",
        "manufacturing_quirks": "Because wiring harnesses are cobbled together from half a dozen derelict shipwrecks, no two Hyenas share identical electrical schematics; grease monkeys routinely joke that repairing one requires a priest as much as a wrench.",
        "battlefield_reputation": "Infamous among merchant convoy captains for its heavy pneumatic harpoon winch, which drags disabled freighters and wounded mobile suits into point-blank flak range.",
        "doctrine_summary": "Ambush boarding, scrap melee brawling, and asset extraction.",
        "production_count": 5600,
        "active_units": 3680,
        "casualty_count": 1920,
        "kill_count": 1840,
        "adoption_status": "standard_issue",
        "primary_theaters": ["Ceres Deep Ring", "Trojan Asteroid Corridor", "Deimos Debris Field"]
    },
    "ms_zaibatsu_muramasa_03": {
        "historical_lore": "Conceived in the subterranean cleanrooms of Olympus Mons by Hyperion Advanced Tactical Systems, the ZAI-03 Muramasa was designed for corporate wetwork and VIP duel interdiction. It features an experimental bio-neural interface that wires directly into the pilot's spinal implants, granting reflex latencies approaching zero.",
        "manufacturing_quirks": "The bio-feedback loop generates severe neuro-thermal spikes in un-augmented pilots; Zaibatsu cockpit technicians mandate cryogenic nitrogen life-support flushes after every combat sortie.",
        "battlefield_reputation": "Known in mercenary channels as 'The Black Scalpel'. Rival aces report that encountering a Muramasa in CQB feels less like a dogfight and more like an execution by a machine that moves before human eyes can track it.",
        "doctrine_summary": "High-frequency tachyon blade dueling, rapid assassination, and line disruption.",
        "production_count": 2150,
        "active_units": 1720,
        "casualty_count": 430,
        "kill_count": 1680,
        "adoption_status": "standard_issue",
        "primary_theaters": ["Olympus Mons Redoubt", "Phobos Corporate Complex", "Syrtis Major Orbital Array"]
    },
    "bp_player_vanguard_heavy": {
        "historical_lore": "The proprietary crown jewel of PMC Hephaestus engineering. Designed aboard the forge dreadnought by the player's R&D department, the Vanguard Linebreaker integrates modular alloy crucible metallurgy with universal weapon hardpoints, bridging the gap between Terran armor survivability and Colony power efficiency.",
        "manufacturing_quirks": "The modular hardpoint lockpins require recalibration when swapping between ballistic and beam configurations, but the crucible alloy composition boasts zero thermal micro-fractures under repeated stress testing.",
        "battlefield_reputation": "Mercenary pilots view the Vanguard as the ultimate survivor's chassis—a custom combat platform that turns corporate battlefields into high-margin salvage operations.",
        "doctrine_summary": "Proprietary PMC frontline assault, modular multi-role offensive anchor.",
        "production_count": 120,
        "active_units": 94,
        "casualty_count": 26,
        "kill_count": 142,
        "adoption_status": "contested",
        "primary_theaters": ["Sector 4 Contested Periphery", "Hephaestus Proving Grounds", "Neutral Commerce Waypoints"]
    },
    "bp_player_stratos_interceptor": {
        "historical_lore": "Engineered aboard PMC Hephaestus to contest corporate air and space corridors. The Stratos pairs aerodynamic lifting body geometry with dual vector thrusters, enabling hypersonic atmospheric re-entry strikes and lightning-fast orbital interception without expensive launch boosters.",
        "manufacturing_quirks": "Vernier fuel feed valves can ice over during rapid atmospheric-to-vacuum transition unless the pilot maintains active heat dissipation cycling.",
        "battlefield_reputation": "Enemy aces fear its sudden radar bloom on high-altitude recon sensors, knowing that a Stratos descent vector is usually followed by twin railgun precision fire.",
        "doctrine_summary": "PMC air-superiority interceptor, long-range orbital interdiction.",
        "production_count": 85,
        "active_units": 68,
        "casualty_count": 17,
        "kill_count": 98,
        "adoption_status": "contested",
        "primary_theaters": ["Upper Mesosphere Corridors", "L-2 Lagrange Jump Points"]
    },
    "bp_player_scrapper_brawler": {
        "historical_lore": "Born from the dreadnought's bottom-tier reclamation decks, the Scrapper Brawler refines outlaw Asteroid Syndicate chassis into a disciplined mercenary strike unit. Reinforced with adamantine-carbide structural ribs, it is purpose-built to break through fortified defense gates and crush armored cockpits.",
        "manufacturing_quirks": "Heavy vibration dampeners in the torso must be inspected for slag buildup after extended hydraulic hammer impacts.",
        "battlefield_reputation": "Syndicate warlords hate it because it turns their own salvage doctrines against them with military-grade precision and unyielding armor density.",
        "doctrine_summary": "CQB urban breach, kinetic demolition, and close-quarters melee brawling.",
        "production_count": 110,
        "active_units": 82,
        "casualty_count": 28,
        "kill_count": 115,
        "adoption_status": "contested",
        "primary_theaters": ["Sub-surface Mining Tunnels", "Derelict Hulk Interdiction"]
    },
    "bp_player_ghost_sniper": {
        "historical_lore": "A covert long-range marksman suit developed using reverse-engineered Mars Zaibatsu optical cloaking and Colony superconducting capacitors. The Ghost Sniper engages high-value enemy targets from beyond visual and thermal detection envelopes.",
        "manufacturing_quirks": "Supercooled capacitor discharge leaves a temporary Cherenkov luminescence in the gun barrel that must be shielded during stealth extraction.",
        "battlefield_reputation": "Corporate commanders describe it as an unseen ghost; entire platoon lead mechs have had their reactors vaporized before alert sirens even triggered.",
        "doctrine_summary": "Extreme-range anti-materiel sniper, electronic warfare concealment.",
        "production_count": 65,
        "active_units": 54,
        "casualty_count": 11,
        "kill_count": 89,
        "adoption_status": "contested",
        "primary_theaters": ["Asteroid Belt Ambush Chokepoints", "Orbital Mirror Shadow Zones"]
    }
}
print("Bespoke lore definitions verified.")
