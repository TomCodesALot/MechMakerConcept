import json

prometheus_events = [
    {
        "id": "event_ms_genesis_debut",
        "title": "GLOBAL INTERCEPT: THE PROMETHEUS PROTOCOL SORTIE",
        "sender": "Interstellar Defense Press Agency (IDPA)",
        "category": "Technological Singularity",
        "body": "Commander, unencrypted sensor telemetry of our maiden Mobile Suit sortie has leaked across all military frequencies! Frontline footage shows our humanoid machine easily traversing a fractured volcanic ravine, deflecting standard 90mm tank munitions, and tearing the turret off a Terran heavy tank in close-quarters melee. The Sol Defense Board has declared an emergency summit. Every intelligence agency in the solar system is attempting to establish contact with our flagship.",
        "choices": [
            {
                "label": "1. Broadcast Open Procurement Availability (+3.0x Bounty Surge)",
                "credits_delta": 50000,
                "standing_terran": 15,
                "standing_colony": 15,
                "consequence_desc": "All factions acknowledge our PMC as the premier military pioneer. Emergency contract bounties surged across all sectors."
            },
            {
                "label": "2. Declare Technology Top-Secret & Enforce Comms Blackout",
                "credits_delta": 0,
                "standing_terran": -10,
                "standing_colony": -10,
                "consequence_desc": "Maintains total tactical secrecy. Megacorporation reverse-engineering efforts are slowed by 15%."
            }
        ]
    },
    {
        "id": "event_terran_urgent_procurement",
        "title": "DIPLOMATIC SUMMONS: TERRAN COALITION HIGH ADMIRALTY",
        "sender": "Grand Marshal Donald Sterling (Terran High Command)",
        "category": "State Procurement Inquiry",
        "body": "Iron Vanguard. I will dispense with diplomatic pleasantries. We watched your walking metal monstrosity crush our armored platoon in Neo-Verona. Our tank commanders are refusing to deploy unless they have comparable support. The Coalition Munitions Board is offering an immediate 150,000 Credit grant and 100 units of refined Tungsten if you agree to provide an operational chassis for evaluation.",
        "choices": [
            {
                "label": "1. Sign Exclusive Technology Evaluation Pact (+150k Cr, +100 Tungsten, Rivals +20% R&D)",
                "credits_delta": 150000,
                "standing_terran": 35,
                "standing_colony": -25,
                "consequence_desc": "Huge cash injection and rare metal reserves secured! However, Vanguard Heavy Industries accelerates its reverse-engineering clock."
            },
            {
                "label": "2. Respectfully Decline: Mercenary Sortie Contracts Only",
                "credits_delta": 25000,
                "standing_terran": 5,
                "consequence_desc": "We retain our tech monopoly while keeping Terran Coalition on retainer as paying contract clients."
            }
        ]
    },
    {
        "id": "event_colony_diplomatic_envoy",
        "title": "ENCRYPTED BURST: ORBITAL INDEPENDENCE ALLIANCE",
        "sender": "Ambassador Maya Vane (Colony Liberation Front)",
        "category": "Ideological Arms Request",
        "body": "Vanguard Command, your bipedal frame represents more than a military weapon—it is the equalizer that can prevent Earth's dreadnoughts from choking the outer colonies into submission. If Earth manages to reverse-engineer your machine first, our colonies will be bombed back into the stone age. We are pleading for your support. Provide our engineers with reactor schematics, or fight alongside our skimmer wings.",
        "choices": [
            {
                "label": "1. Partner with Colony Fleet (+200k Cr, +40 Tritium, +30 Colony Standing)",
                "credits_delta": 200000,
                "standing_colony": 40,
                "standing_terran": -30,
                "consequence_desc": "Colony freedom fighters hail our Foundry as liberators! Astraea Orbital gains telemetry to develop their agile aerial frames."
            },
            {
                "label": "2. Offer Escort Contracts Without Tech Transfer",
                "credits_delta": 30000,
                "standing_colony": 10,
                "consequence_desc": "Agreed to fly-off trials and defensive operations without relinquishing core Tokamak patents."
            }
        ]
    },
    {
        "id": "event_syndicate_black_ops_espionage",
        "title": "SECURITY BREACH: SYNDICATE WET-WORK INFILTRATION",
        "sender": "Flagship Chief of Security Miller",
        "category": "Corporate Espionage",
        "body": "Commander! Syndicate raiders breached Hangar Bay 3 under cover of an optical jamming flare! They weren't after money—they were trying to download the Tokamak magnetic bottle assembly telemetry from our terminal! Our security team has pinned their operative down in the airlock corridor.",
        "choices": [
            {
                "label": "1. Interrogate Operative & Trace Syndicate Backer",
                "credits_delta": 10000,
                "consequence_desc": "Operative cracked under interrogation. We discovered Rustworks' secret testing facility, reducing their R&D progress by -10%."
            },
            {
                "label": "2. Execute Operative & Broadcast Warning to Sol Underworld",
                "credits_delta": 0,
                "standing_syndicate": -20,
                "consequence_desc": "Demonstrated ruthless operational defense. Syndicate pirate raids against our mining nodes drop significantly."
            }
        ]
    },
    {
        "id": "event_competitor_first_testbed_spotted",
        "title": "RECON REPORT: RIVAL CORP COMMISSIONS WALKING TESTBED",
        "sender": "Tactical Recon Officer Diaz",
        "category": "Competitor Arms Evolution",
        "body": "Long-range orbital radar has picked up a high-energy seismic disturbance in the Asteroid Belt. One of our rival competitors has completed assembly of a crude bipedal hybrid—a converted heavy tank chassis mounted onto bipedal walking hydraulics. It's primitive, unstable, and prone to overheating, but it proves they are closing the gap. The countdown to full rival Mobile Suit mass production is ticking down.",
        "choices": [
            {
                "label": "1. Deploy Precision Strike on Rival Testing Grounds",
                "credits_delta": -25000,
                "consequence_desc": "Rival testbed annihilated in a precision strike! Competitor reverse-engineering delayed by 40 calendar days."
            },
            {
                "label": "2. Accelerate Our Next-Generation Sintering R&D",
                "credits_delta": 0,
                "consequence_desc": "We double down on superior alloy metallurgy, unlocking advanced Tier-3 composite recipes."
            }
        ]
    }
]

for filepath in ["datafiles/narrative_events.json", "narrative_events.json"]:
    with open(filepath, "r") as f:
        data = json.load(f)
    
    existing_ids = {e["id"] for e in data.get("events", [])}
    added = 0
    for ev in prometheus_events:
        if ev["id"] not in existing_ids:
            data["events"].append(ev)
            added += 1
            
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"Updated {filepath}: added {added} Prometheus narrative events.")
