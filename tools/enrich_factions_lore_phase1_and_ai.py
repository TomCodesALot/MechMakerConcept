#!/usr/bin/env python3
"""
enrich_factions_lore_phase1_and_ai.py
Author: Lore Master & Lead Game Designer
Enriches datafiles/factions_lore.json with:
1. Phase 1 Geopolitical Setting ("The Baikal Shock & The L-5 Secession", Y205-Y208).
2. Deep Phase 1 context for each faction (founding ethos, internal divide, strategic choices).
3. The AI Brain behavioral state machine (Peace State, Alignment & Diplomatic Matrix,
   Winning State behaviors, Desperate State behaviors & Superweapon unsealing).
"""

import json
import os

FP = "datafiles/factions_lore.json"
with open(FP, "r", encoding="utf-8") as f:
    data = json.load(f)

# Global Phase 1 World Setting
data["phase_1_world_setting"] = {
    "era_title": "Phase 1: The Baikal Shock & The L-5 Secession (Y205 - Y208)",
    "historical_summary": (
        "The Sol System stands on a razor's edge following the collapse of the Old Earth Central Hegemony. "
        "Depleted of critical fusion isotopes—principally Helium-3 and Tritium catalysts—Earth's industrial machine "
        "faces an existential energy deficit. In response, the newly declared Outer Colony League enacted the L-5 Covenant, "
        "abruptly cutting off uncompensated mineral shipments to Earth. High Command in Baikal responded with the Baikal Directive, "
        "deploying the first generation of monolithic cast-tungsten mobile suits to enforce orbital quotas through brute force. "
        "Meanwhile, the lawless Asteroid Belt erupted into opportunistic piracy under the Rim-Syndicate Cartel, while the Martian "
        "Apex Zaibatsu weaponized corporate finance, bio-neural wetwork, and patent espionage to harvest the spoils of war. "
        "At the crossroads of this multi-polar catastrophe drifts the forge dreadnought Hephaestus—a neutral sovereign PMC hub "
        "with the crucible metallurgical capacity to dictate the future of mechanized warfare."
    ),
    "core_conflict": "Mineral Quotas vs Spacenoid Liberty vs Corporate Profit vs Outlaw Survival",
    "factions_active": 4,
    "player_role": "Commander of the Sovereign Forge Dreadnought Hephaestus (Neutral Arms Dealer & Mercenary Kingmaker)"
}

factions = data["factions"]

# 1. THE TERRAN COALITION
factions["faction_terran"]["phase_1_context"] = {
    "founding_ethos": "Planetary Integrity & Centralized Imperial Destiny",
    "starting_territory_pct": 38,
    "starting_military_score": 55,
    "economic_reality": (
        "Possesses immense heavy metallurgical casting foundries (Lake Baikal, Ural Defense Works), "
        "deep demographic reserves, and planetary bedrock redoubts. However, its economy is suffocating "
        "under acute shortages of refined helium-3, tritium superconducting matrices, and rare-earth catalysts."
    ),
    "internal_divide": "Hawk Defense Ministry (Gen. Deborah Vance) vs Senate Trade Oligarchs (Arthur Sterling)",
    "phase_1_strategic_choice": (
        "Terran High Command must decide whether to negotiate commercial tariffs with the Colonies or launch a preemptive "
        "orbital drop campaign to seize the L-5 Lagrange transfer hubs and force colonial factories back under Earth administration."
    )
}

factions["faction_terran"]["ai_brain"] = {
    "peace_state": {
        "posture": "Defensive Consolidation & Industrial Stockpiling",
        "priorities": "Stockpiling tungsten ingots, fortifying lunar staging perimeters, producing GHA-07 Ironclad mainstays.",
        "patrol_focus": "Low Earth Orbit Fortress Rings, Baikal Defense Arc, Copernicus Crater.",
        "pmc_engagement": "Hires PMCs for routine border deterrence, mineral convoy escorts, and strict standardized blueprint tenders."
    },
    "diplomatic_matrix": {
        "natural_trade_partners": ["Apex Bio-Cybernetics Zaibatsu"],
        "trade_rationale": "Purchases Martian neural coprocessors and optical targeting sensors in exchange for heavy industrial tractors and raw iron.",
        "natural_allies": ["Apex Bio-Cybernetics Zaibatsu (Pragmatic Corporate Defense Pact)"],
        "primary_enemy": "The Outer Colony League",
        "enemy_rationale": "Colonial independence threatens Earth's energy supply; High Command views Spacenoids as treasonous insurgent debtors.",
        "tension_triggers": [
            "Colonial expansion into L-5 or Lunar orbit",
            "PMC exporting beam weaponry or superconducting reactors to the Colonies",
            "Syndicate pirating Terran mineral barges in the Asteroid Belt"
        ]
    },
    "winning_state": {
        "trigger": "Territory >= 38% or Military Strength >= 70",
        "behavior": "Imperial Hegemony & Resource Extraction Mandates",
        "actions": [
            "Imposes crippling 40% planetary tariffs across all Sol shipping lanes.",
            "Issues ultimatums demanding uncompensated Helium-3 tithes from colonial habitats.",
            "Deploys aggressive two-front orbital drop-pod invasions into Jovian and Belt sectors.",
            "Squeezes PMC contracts, reducing bounty payouts by 15% due to imperial hubris."
        ],
        "vulnerability": "Overextended logistical supply lines, high domestic war weariness, leaving redoubts vulnerable to harpoon ambushes."
    },
    "desperate_state": {
        "trigger": "Territory <= 18% or Military Strength <= 25",
        "behavior": "Totalitarian Fortress Protocol & Scorched Earth",
        "actions": [
            "Declares universal martial law and civilian labor conscription across Earth.",
            "Unseals forbidden pre-war superheavy warframe: VHD-X01 Juggernaut Prime / Odin Dread-Chassis.",
            "Issues frantic emergency bailout tenders to the player's PMC offering +100% bounty bonuses (2.0x multiplier).",
            "Authorizes scorched-earth orbital kinetic saturation strikes against contested borderline sectors."
        ],
        "superweapon_asset": "ms_valkyrie_titan_juggernaut"
    }
}

# 2. THE OUTER COLONY LEAGUE
factions["faction_colony"]["phase_1_context"] = {
    "founding_ethos": "Vector Liberty & Spacenoid Sovereignty",
    "starting_territory_pct": 32,
    "starting_military_score": 50,
    "economic_reality": (
        "Controls virtually all high-yield Helium-3 extraction across the Jovian atmosphere, high-vacuum "
        "electron-beam sintering plants, and orbital solar arrays. However, its populations reside inside "
        "fragile ceramic bio-domes vulnerable to single kinetic artillery punctures, with zero domestic tungsten reserves."
    ),
    "internal_divide": "Insurgent Flotilla Vanguard (Cassian Vane) vs Civilian Trade Senate (Lyra Thorne)",
    "phase_1_strategic_choice": (
        "The League must decide whether to maintain an agile hit-and-run defensive perimeter around Jovian space or "
        "take the fight to Earth by disabling the orbital elevators, risking an all-out planetary war of annihilation."
    )
}

factions["faction_colony"]["ai_brain"] = {
    "peace_state": {
        "posture": "Technological Acceleration & Bio-Dome Shielding",
        "priorities": "Expanding Helium-3 gas refining, upgrading habitat defense shields, tuning vernier agility on AET-01 Aether suits.",
        "patrol_focus": "L-5 Orbital Gateway, Jovian Mining Corridor, Archimedes Lagrange Point.",
        "pmc_engagement": "Offers high-paying escort contracts for civilian food transports; seeks high-mobility particle beam blueprints."
    },
    "diplomatic_matrix": {
        "natural_trade_partners": ["The Rim-Syndicate Cartel"],
        "trade_rationale": "Trades raw Helium-3 fuel and hydroponic synthetic nutrients for smuggled Terran steel and Asteroid Belt raw ores.",
        "natural_allies": ["The Rim-Syndicate Cartel (Anti-Earth Liberation Compact)"],
        "primary_enemy": "The Terran Coalition",
        "enemy_rationale": "Centuries of colonial tribute and Earth's relentless threat of orbital drop subjugation.",
        "tension_triggers": [
            "Terran Coalition military posturing in Lunar orbit",
            "Syndicate raids on civilian passenger freighters",
            "Zaibatsu corporate espionage attempts targeting Helium-3 synthesis algorithms"
        ]
    },
    "winning_state": {
        "trigger": "Territory >= 38% or Military Strength >= 70",
        "behavior": "Ideological Crusade & Liberation Hegemony",
        "actions": [
            "Declares an interplanetary crusade to liberate Earth's oppressed working class.",
            "Attempts dangerous atmospheric descent incursions where light aerosteel suits suffer heavy gravity drag.",
            "Enforces a total space blockade over low Earth orbit, cutting off all imported minerals.",
            "Demands unconditional recognition of complete Spacenoid sovereignty."
        ],
        "vulnerability": "Civilian bio-domes left lightly defended while vanguard fleets overextend into Earth's gravity well."
    },
    "desperate_state": {
        "trigger": "Territory <= 18% or Military Strength <= 25",
        "behavior": "Last Stand of the Free Orbit & Mutual Extinction Threat",
        "actions": [
            "Evacuates outer habitats, concentrating all remaining forces into the fortified L-5 Citadel.",
            "Unseals lost-tech experimental particle super-weapon: Astraea Dominus X-01 / Chronos Vector Proto.",
            "Dispatches desperate humanitarian defense contracts to the player's PMC offering +100% to +150% bonuses.",
            "Threatens to de-orbit spent mining asteroids into Earth's orbital corridors as a doomsday deterrent."
        ],
        "superweapon_asset": "ms_colony_astraea_dominus_x01"
    }
}

# 3. THE RIM-SYNDICATE CARTEL
factions["faction_syndicate"]["phase_1_context"] = {
    "founding_ethos": "Scrap Sovereignty & Lawless Void Freedom",
    "starting_territory_pct": 16,
    "starting_military_score": 30,
    "economic_reality": (
        "Controls vast deep-space salvage graveyards, asteroid hollow smelting operations, and black-market contraband "
        "routes through Ceres and Trojan clusters. Possesses immense reserves of recycled alloys and slag, but lacks "
        "high-tech cleanrooms, relying on jury-rigged modifications and hijacked military hardware."
    ),
    "internal_divide": "Scrap Depot Matriarchs (Madame Rosalind Cruz) vs Bloodthirsty Reaver Commodores ('Iron-Eye' Torval)",
    "phase_1_strategic_choice": (
        "The Syndicate must balance acting as arms suppliers to both warring titans for astronomical profit versus "
        "consolidating the lawless clans into an independent pirate empire capable of resisting corporate annexation."
    )
}

factions["faction_syndicate"]["ai_brain"] = {
    "peace_state": {
        "posture": "Opportunistic Scavenging & Black Market Smuggling",
        "priorities": "Stripping derelict wrecks, hotwiring scavenged reactors, mass-producing SCR-12 Hyena frames.",
        "patrol_focus": "Ceres Deep Ring, Vesta Debris Belt, Deimos Wreckage Graveyard.",
        "pmc_engagement": "Offers high-risk, lucrative wetwork contracts, black-market blueprint trades, and salvage bounties."
    },
    "diplomatic_matrix": {
        "natural_trade_partners": ["Outer Colony League", "Corrupt Terran Regional Governors"],
        "trade_rationale": "Sells black-market military hardware and stolen blueprints for hard currency, fuel cells, and luxury goods.",
        "natural_allies": ["Whoever is currently losing (to prolong the conflict for salvage profits)"],
        "primary_enemy": "Wealthy unescorted merchant convoys of ANY faction (especially Terran heavy freight)",
        "enemy_rationale": "Commercial freighters represent instant scrap wealth; corporate patent police threaten Syndicate independence.",
        "tension_triggers": [
            "Any faction constructing permanent naval bases in the Asteroid Belt",
            "Zaibatsu cybernetic hit-squads executing pirate captains",
            "Terran naval convoys escorting armed anti-pirate battlecruisers"
        ]
    },
    "winning_state": {
        "trigger": "Territory >= 38% or Military Strength >= 70",
        "behavior": "Pirate Armada Ascendancy & System-Wide Extortion",
        "actions": [
            "Warlord Cruz and Torval consolidate the clans into a massive reaver armada.",
            "Imposes violent protection rackets across all four quadrant trade routes.",
            "Launches bold boarding raids directly against lunar orbital docks and Jovian transfer hubs.",
            "Floods the market with cheap, deadly scrap-weapon variants, crashing corporate stock prices."
        ],
        "vulnerability": "Total absence of central logistics; internal clan infighting erupts as warlords feud over plunder."
    },
    "desperate_state": {
        "trigger": "Territory <= 18% or Military Strength <= 25",
        "behavior": "Scorched Void Guerrilla & Suicide Swarms",
        "actions": [
            "Booby-traps asteroid hollows with nuclear demolition charges and retreats into deep void stealth drifts.",
            "Unseals colossal jury-rigged monstrosity: AJS-X02 Rust Behemoth / ARC-X09 Iron Reaver.",
            "Launches suicidal unshielded overclocked shock squads with zero regard for pilot survival.",
            "Offers the player's PMC emergency mercenary contracts with triple bounties, promising 50% shares of captured territory."
        ],
        "superweapon_asset": "ms_syndicate_rust_behemoth"
    }
}

# 4. APEX BIO-CYBERNETICS ZAIBATSU
factions["faction_zaibatsu"]["phase_1_context"] = {
    "founding_ethos": "Post-Human Optimization & Transhumanist Shareholder Hegemony",
    "starting_territory_pct": 14,
    "starting_military_score": 45,
    "economic_reality": (
        "Maintains total technological monopoly over bio-neural spinal cockpits, optical stealth refractors, and "
        "sub-zero tachyon superconductor matrices. Operates out of subterranean Martian arcologies and Phobos data vaults. "
        "Possesses massive financial capital, but suffers from low native population and severe distrust from all planetary states."
    ),
    "internal_divide": "Corporate Board of Directors (Executive Takahashi) vs Unchecked Cybernetic Labs (Chief Scientist Renzo)",
    "phase_1_strategic_choice": (
        "The Zaibatsu must choose between quietly selling advanced weapons to both Earth and the Colonies to collect sovereign debt "
        "or initiating covert decapitation strikes against rival leadership to trigger a full corporate takeover of Sol."
    )
}

factions["faction_zaibatsu"]["ai_brain"] = {
    "peace_state": {
        "posture": "Covert Espionage & Bio-Neural Telemetry Testing",
        "priorities": "R&D into spinal neural link interfaces, hostile corporate acquisitions, producing ZAI-03 Muramasa dueling frames.",
        "patrol_focus": "Olympus Mons Redoubt, Phobos Deep Vaults, Syrtis Major Corporate Corridor.",
        "pmc_engagement": "Hires PMCs for covert asset extraction, VIP wetwork, and live-fire telemetry gathering; pays in corporate equity and high-tech alloys."
    },
    "diplomatic_matrix": {
        "natural_trade_partners": ["The Terran Coalition (High-Value Defense Contracts)"],
        "trade_rationale": "Supplies neural computers, optical stealth gear, and precision components in exchange for raw mineral quotas.",
        "natural_allies": ["The second-weakest faction (as a puppet buffer state to destabilize the hegemon)"],
        "primary_enemy": "The Rim-Syndicate Cartel (Patent Thieves) & whichever power refuses debt repayment",
        "enemy_rationale": "Syndicate pirates reverse-engineer and clone Zaibatsu patents; state governments threaten corporate tax audits.",
        "tension_triggers": [
            "Discovery of Zaibatsu covert black-ops infiltration units in rival territory",
            "Syndicate black-market cloning of Takahashi neural interfaces",
            "State regulation or nationalization of Martian orbital assets"
        ]
    },
    "winning_state": {
        "trigger": "Territory >= 38% or Military Strength >= 70",
        "behavior": "Corporate Feudalism & Bio-Synthetic Monopoly",
        "actions": [
            "Forecloses on sovereign planetary debt, seizing orbital factories and shipyards as corporate collateral.",
            "Mandates that all military pilots undergo corporate neural sync procedures, creating an army of indentured cyborg aces.",
            "Deploys autonomous AI combat drones to replace human military garrisons across Sol.",
            "Slits competitor profit margins, demanding exorbitant licensing royalties for all energy weapon technologies."
        ],
        "vulnerability": "Over-centralized cybernetic telemetry networks; highly vulnerable to electromagnetic pulses and physical kinetic artillery."
    },
    "desperate_state": {
        "trigger": "Territory <= 18% or Military Strength <= 25",
        "behavior": "Cybernetic Singularity Protocol & Rogue Lab Activation",
        "actions": [
            "Seals subterranean Martian vaults and deletes corporate audit logs.",
            "Unseals forbidden autonomous cybernetic apex prototype: HATS-X01 Amaterasu Zero / Null-07 Phantom.",
            "Dispatches brain-fried cybernetic suicide aces stripped of all pain and survival inhibitors.",
            "Offers the player's PMC astronomical equity payouts (+100% bonus bounties) and proprietary patent schematics to eliminate hostile siege lines."
        ],
        "superweapon_asset": "ms_zaibatsu_amaterasu_x01"
    }
}

with open(FP, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Successfully enriched datafiles/factions_lore.json with Phase 1 World Setting and AI Brain State Machines!")
