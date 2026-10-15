import json

new_events = [
    {
        "id": "event_competitor_leak",
        "title": "CLASSIFIED DISPATCH: CORPORATE PROTOTYPE LEAK",
        "sender": "Black-Market Data Broker 'Cipher'",
        "category": "Corporate Espionage",
        "body": "Commander, our moles inside Astraea Orbital Dynamics have intercepted encrypted CAD schematics of their next-generation micro-gravity frame. They plan to submit this prototype in the upcoming Colony procurement tender. The broker is asking 60,000 Credits for the decrypted telemetry.",
        "choices": [
            {
                "label": "1. Purchase CAD Schematics (-60,000 Cr)",
                "credits_delta": -60000,
                "standing_colony": 0,
                "flyoff_bonus_pts": 10,
                "consequence_desc": "Telemetry decrypted! Next procurement fly-off against Astraea gains a +10 PTS competitive insight bonus."
            },
            {
                "label": "2. Leak Encrypted Data to Terran Military Intelligence",
                "credits_delta": 45000,
                "standing_terran": 15,
                "standing_colony": -10,
                "consequence_desc": "Terran Coalition awards a 45,000 Cr finder's fee (+15 Terran Standing, -10 Colony Standing)."
            },
            {
                "label": "3. Disregard Intercept as Corporate Counter-Intel",
                "credits_delta": 0,
                "consequence_desc": "Transmission archived without action."
            }
        ]
    },
    {
        "id": "event_emergency_flash_tender",
        "title": "EMERGENCY TENDER: LUNAR DEFENSE CRISIS",
        "sender": "General Hector Vance (Terran Munitions Board)",
        "category": "Flash Procurement Order",
        "body": "Urgent alert, mercenary. Syndicate pirate wolves have breached the perimeter at Archimedes Crater. The Terran Coalition has issued an emergency 3-turn flash tender for combat-ready heavy linebreakers. Any approved prototype will bypass standard shipyard tooling delays with a 50% licensing bounty bonus!",
        "choices": [
            {
                "label": "1. Mobilize Foundry for Emergency Mass-Production",
                "credits_delta": 250000,
                "standing_terran": 20,
                "consequence_desc": "Emergency defense contract ratified! +250,000 Cr mobilization grant awarded and Terran standing surged."
            },
            {
                "label": "2. Deploy PMC Strike Squad to Hold the Crater Lines",
                "credits_delta": 120000,
                "standing_terran": 25,
                "consequence_desc": "PMC aces deployed to Lunar lines. Frontline held (+120,000 Cr combat bonus, +25 Terran Standing, +PMC Combat Pedigree)."
            },
            {
                "label": "3. Prioritize Existing Foundry Orders",
                "credits_delta": 0,
                "standing_terran": -5,
                "consequence_desc": "Declined flash tender (-5 Terran Standing)."
            }
        ]
    },
    {
        "id": "event_field_failure_scandal",
        "title": "MARKET SHOCK: VALKYRIE HEAVY HYDRAULIC COLLAPSE",
        "sender": "Sol Financial News Network (SFNN)",
        "category": "Corporate Crisis",
        "body": "Catastrophe in the Jovian trenches! Valkyrie Heavy Industries' newly deployed GHA-07 line units have suffered widespread joint seizing in deep-frost mud, stranding two mechanized divisions. Terran High Command is furious and corporate stock has plunged 22%. The Munitions Board is openly considering canceling their contract.",
        "choices": [
            {
                "label": "1. Launch Aggressive Replacement Tender Blitz (-50,000 Cr)",
                "credits_delta": -50000,
                "standing_terran": 15,
                "market_share_delta": 4,
                "consequence_desc": "PR blitz launched! Siphoned 4% Sol market share from Valkyrie Heavy and boosted Terran favor."
            },
            {
                "label": "2. Offer Foundry Nanite Repair Kits at Extortionate Rates",
                "credits_delta": 140000,
                "consequence_desc": "Terran emergency procurement purchases foundry alloy kits for +140,000 Cr profit."
            },
            {
                "label": "3. Issue Neutral Engineering Advisory",
                "credits_delta": 0,
                "standing_terran": 5,
                "consequence_desc": "Neutral technical assistance offered (+5 Terran Standing)."
            }
        ]
    },
    {
        "id": "event_defector_ace_mech",
        "title": "RADAR ANOMALY: DEFECTOR TEST PILOT INCOMING",
        "sender": "Hangar Control Bridge",
        "category": "Military Defection",
        "body": "Commander! An experimental mobile suit with transhuman neural avionics has crossed our flight deck without transponder codes. The pilot identifies as Ren 'Null-09', lead test pilot from Hyperion Advanced Tactical Systems, requesting asylum with their tuned Muramasa-X prototype!",
        "choices": [
            {
                "label": "1. Grant Asylum: Commission Pilot & Prototype into PMC Hangar",
                "credits_delta": -35000,
                "pilot": {
                    "name": "Ren 'Null-09' (Defector)",
                    "callsign": "NULL_09",
                    "salary_daily": 850,
                    "combat_stat": 9,
                    "morale": 95,
                    "status": "ACTIVE",
                    "specialty": "Neural Synapse Striker"
                },
                "consequence_desc": "Elite pilot and prototype accepted into PMC roster! Hyperion corporate hostility increases."
            },
            {
                "label": "2. Strip Prototype for Exotic Tachyon Alloys & Foundry Data",
                "credits_delta": 180000,
                "consequence_desc": "Chassis dismantled in Crucible. +180,000 Cr and exotic metallurgy unlocked."
            },
            {
                "label": "3. Extradite Pilot Back to Hyperion for Diplomatic Bounty",
                "credits_delta": 95000,
                "consequence_desc": "Extradited to Hyperion (+95,000 Cr bounty, Zaibatsu standing +20)."
            }
        ]
    },
    {
        "id": "event_arms_dealer_backlash",
        "title": "DIPLOMATIC CABLE: CLONED CHASSIS PIRATE INCIDENT",
        "sender": "Outer Colony Security Liaison",
        "category": "Geopolitical Scandal",
        "body": "Disaster on the Ganymede shipping route! A pirate battle wing was detected piloting pirated hulls identical to your exported mobile suit blueprint, pillaging an unarmed medical freighter. Planetary press outlets are broadcasting footage with your corporate insignias, demanding an official response.",
        "choices": [
            {
                "label": "1. Transmit Firmware Kill-Switch Code to Colony Defense",
                "credits_delta": -20000,
                "standing_colony": 25,
                "consequence_desc": "Kill-switch transmitted! Pirate units disabled in space (+25 Colony Standing, PR crisis averted)."
            },
            {
                "label": "2. Deploy PMC Strike Lance to Destroy the Pirates Pro Bono",
                "credits_delta": 50000,
                "standing_colony": 20,
                "consequence_desc": "Pirates eliminated under PMC guns (+50,000 Cr salvage, +20 Colony Standing, +Combat Pedigree)."
            },
            {
                "label": "3. 'Arms Dealers Don't Choose the Battle' (Sell Ammo)",
                "credits_delta": 65000,
                "standing_colony": -20,
                "consequence_desc": "+65,000 Cr unlogged arms profits (-20 Colony Standing)."
            }
        ]
    },
    {
        "id": "event_corporate_black_ops_raid",
        "title": "RED ALERT: CORPORATE WET-WORK AMBUSH",
        "sender": "Tactical Sensor Network",
        "category": "Corporate Hostility",
        "body": "Proximity sensors screaming! A heavily armed black-ops strike team displaying scrubbed corporate serial numbers has breached the outer perimeter of our resource extraction outpost. They have deployed electronic jamming and are attempting to scuttle our mining crucibles!",
        "choices": [
            {
                "label": "1. Scramble Hangar Battlegroup to Repel the Raid",
                "credits_delta": 75000,
                "consequence_desc": "PMC aces scrambled! Corporate hit-squad annihilated (+75,000 Cr bounty salvage, +Combat Pedigree)."
            },
            {
                "label": "2. Activate Overcharged Automated Defense Sentry Turrets",
                "credits_delta": -40000,
                "consequence_desc": "Sentries fired at maximum overload. Perimeter held with minor facility repair costs (-40,000 Cr)."
            },
            {
                "label": "3. Tactical Withdrawal & Secure Nanite Crucible Cores",
                "credits_delta": -25000,
                "consequence_desc": "Crucibles secured; minor ore stock lost (-25,000 Cr)."
            }
        ]
    }
]

file_paths = ['datafiles/narrative_events.json', 'narrative_events.json']
for fp in file_paths:
    with open(fp, 'r') as f:
        data = json.load(f)
    existing_ids = {ev['id'] for ev in data.get('events', [])}
    for nev in new_events:
        if nev['id'] not in existing_ids:
            data['events'].append(nev)
            print(f"Added {nev['id']} to {fp}")
    with open(fp, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Updated {fp} (Total events: {len(data['events'])})")
