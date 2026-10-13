#!/usr/bin/env python3
"""
tools/enrich_characters_full.py
Enriches all 204 characters in datafiles/characters_roster.json with:
1. Deep Love Interests (Spouses, Dating, Star-Crossed, Unrequited, Former Flames)
2. Comradeship & Friendship Networks (Academy, Trench, Cantina, Neuro-Sync)
3. Procedural Playthrough Allegiance Variance (Loyalty types, weights, defection hooks)
"""

import os
import json
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROSTER_PATH = os.path.join(BASE_DIR, "datafiles", "characters_roster.json")

with open(ROSTER_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

characters = data["characters"]
char_map = {c["id"]: c for c in characters}
id_list = list(char_map.keys())

# Categorize by faction
f_groups = {
    "faction_terran": [c for c in characters if c["faction_id"] == "faction_terran"],
    "faction_colony": [c for c in characters if c["faction_id"] == "faction_colony"],
    "faction_syndicate": [c for c in characters if c["faction_id"] == "faction_syndicate"],
    "faction_zaibatsu": [c for c in characters if c["faction_id"] == "faction_zaibatsu"],
    "independent": [c for c in characters if c["faction_id"] == "independent"]
}

# =============================================================================
# 1. CANONICAL HIGH-DRAMA ROMANTIC ANCHORS
# =============================================================================
CANON_ROMANCES = {
    # Star-Crossed Frontline Legends
    "pilot_terran_cole": {
        "target_id": "pilot_colony_kira",
        "relationship_type": "star_crossed",
        "intensity": 92,
        "grudge_multiplier": 3.2,
        "trauma_reaction": "berserker_rage",
        "lore_snippet": "Met Kira during the Geneva Ceasefire talks; maintain secret encrypted comms despite flying against each other in orbit."
    },
    "pilot_colony_kira": {
        "target_id": "pilot_terran_cole",
        "relationship_type": "star_crossed",
        "intensity": 92,
        "grudge_multiplier": 3.2,
        "trauma_reaction": "berserker_rage",
        "lore_snippet": "Secretly cherishes encrypted telemetry pings from Marcus Cole across the sensor void."
    },
    # Exiled Pirate Prince & Jovian Aristocrat
    "pilot_syndicate_jackal": {
        "target_id": "char_colony_genevieve_vane",
        "relationship_type": "former_flame",
        "intensity": 88,
        "grudge_multiplier": 3.0,
        "trauma_reaction": "suicidal_charge",
        "lore_snippet": "Shared a torrid romance with Genevieve Vane in their youth before Jax stole a military walker and fled into the asteroid fringe."
    },
    "char_colony_genevieve_vane": {
        "target_id": "pilot_syndicate_jackal",
        "relationship_type": "former_flame",
        "intensity": 85,
        "grudge_multiplier": 2.8,
        "trauma_reaction": "grief_paralysis",
        "lore_snippet": "Keeps a locked datapad with Jax's old flight logs in her personal Jovian stateroom."
    },
    # Terran Academy Sweethearts
    "pilot_terran_rostova": {
        "target_id": "pilot_terran_tyler_vance",
        "relationship_type": "dating",
        "intensity": 90,
        "grudge_multiplier": 3.0,
        "trauma_reaction": "protective_intercept",
        "lore_snippet": "Flew together as academy cadets; Elena vows to keep Tyler alive despite his reckless frontline charges."
    },
    "pilot_terran_tyler_vance": {
        "target_id": "pilot_terran_rostova",
        "relationship_type": "dating",
        "intensity": 90,
        "grudge_multiplier": 3.0,
        "trauma_reaction": "berserker_rage",
        "lore_snippet": "Madly in love with Elena; would break military formation to intercept incoming ordnance targeting her frame."
    },
    # Tragic Secret Longing across Ideological Lines
    "pilot_colony_sorren": {
        "target_id": "char_terran_claire_vance",
        "relationship_type": "star_crossed",
        "intensity": 86,
        "grudge_multiplier": 3.0,
        "trauma_reaction": "protective_intercept",
        "lore_snippet": "Crossed monoblades with Claire Vance at the Ceres breach; holds a profound, honorable romantic devotion to her military spirit."
    },
    "char_terran_claire_vance": {
        "target_id": "pilot_colony_sorren",
        "relationship_type": "star_crossed",
        "intensity": 84,
        "grudge_multiplier": 2.9,
        "trauma_reaction": "protective_intercept",
        "lore_snippet": "Respects and secretly longs for the Colony phantom who spared her disabled command suit at Ceres."
    },
    # Zaibatsu Synaptic Neural Pair
    "pilot_zaibatsu_null07": {
        "target_id": "pilot_zaibatsu_kaori",
        "relationship_type": "dating",
        "intensity": 95,
        "grudge_multiplier": 3.5,
        "trauma_reaction": "berserker_rage",
        "lore_snippet": "Directly linked via synchronized tachyon neural uplinks; feel each other's physical pain and combat adrenaline in real-time."
    },
    "pilot_zaibatsu_kaori": {
        "target_id": "pilot_zaibatsu_null07",
        "relationship_type": "dating",
        "intensity": 95,
        "grudge_multiplier": 3.5,
        "trauma_reaction": "berserker_rage",
        "lore_snippet": "Her neural cortex is permanently calibrated to Ren's biosignatures. If his heart stops, her brain experiences sensory trauma."
    },
    # Supreme Leaders' Decades-Long Bitter Past
    "char_terran_vance": {
        "target_id": "char_colony_cassian",
        "relationship_type": "former_flame",
        "intensity": 78,
        "grudge_multiplier": 2.7,
        "trauma_reaction": "hostage_bargain",
        "lore_snippet": "Academy sweethearts thirty years ago before the Secession War tore the solar system apart; now bitter supreme commanders."
    },
    "char_colony_cassian": {
        "target_id": "char_terran_vance",
        "relationship_type": "former_flame",
        "intensity": 78,
        "grudge_multiplier": 2.7,
        "trauma_reaction": "hostage_bargain",
        "lore_snippet": "Keeps an antique Terran locket from Deborah Vance hidden beneath his naval uniform awards."
    },
    # Underworld & Corporate Shadow Romance
    "char_syndicate_cruz": {
        "target_id": "char_zaibatsu_takahashi",
        "relationship_type": "dating",
        "intensity": 75,
        "grudge_multiplier": 2.5,
        "trauma_reaction": "hostage_bargain",
        "lore_snippet": "Masked as cold black-market corporate contracts, their secret liaison has survived two planetary wars."
    },
    "char_zaibatsu_takahashi": {
        "target_id": "char_syndicate_cruz",
        "relationship_type": "dating",
        "intensity": 75,
        "grudge_multiplier": 2.5,
        "trauma_reaction": "hostage_bargain",
        "lore_snippet": "Channels black-budget Zaibatsu funds to Madame Cruz's smuggling cartels in exchange for secure orbital safehouses."
    }
}

# =============================================================================
# 2. ENRICH EACH CHARACTER WITH ROMANCE, FRIENDS, AND VARIANCE
# =============================================================================
# Set deterministic seed for procedural fills
rng = random.Random(42)

for c in characters:
    cid = c["id"]
    fac = c["faction_id"]
    tier = c["tier"]
    is_rec = c["is_recruitable"]

    # -------------------------------------------------------------------------
    # A. LOVE INTEREST
    # -------------------------------------------------------------------------
    if cid in CANON_ROMANCES:
        c["love_interest"] = CANON_ROMANCES[cid]
        # Ensure target_name is stored
        t_id = c["love_interest"]["target_id"]
        c["love_interest"]["target_name"] = char_map[t_id]["name"] if t_id in char_map else t_id
    else:
        # Determine romance status procedurally based on traits and faction
        # 75% of pilots have a meaningful love interest (spouse, dating, star-crossed, unrequited, ex)
        has_romance = rng.random() < 0.85
        if has_romance:
            # Pick a potential partner
            # 30% chance cross-faction / star-crossed, 70% within same or allied faction
            is_cross = rng.random() < 0.30
            pool = [p["id"] for p in characters if p["id"] != cid and p["id"] not in [c.get("mentor_id"), c.get("rival_id")]]
            
            # Filter pool if not cross-faction
            if not is_cross:
                same_fac = [p["id"] for p in characters if p["faction_id"] == fac and p["id"] != cid]
                if same_fac:
                    pool = same_fac
            
            target_id = rng.choice(pool)
            target_obj = char_map.get(target_id, {})
            t_name = target_obj.get("name", "Unknown Pilot")
            
            # Relationship status
            if target_obj.get("faction_id") != fac:
                r_type = rng.choice(["star_crossed", "former_flame", "unrequited"])
            else:
                r_type = rng.choice(["spouse", "dating", "unrequited", "former_flame"])
            
            r_int = rng.randint(65, 94)
            r_mult = round(2.4 + (r_int / 100.0) * 1.1, 2)
            trauma = rng.choice(["berserker_rage", "suicidal_charge", "protective_intercept", "grief_paralysis", "hostage_bargain"])
            
            snippets = {
                "spouse": f"Lawfully wedded partner; they maintain contact across battlefield dispatches and swear to return alive.",
                "dating": f"In an active romantic partnership; often seen tuning cockpits and reviewing flight telemetry together.",
                "star_crossed": f"Forbidden love separated by the war between {fac.replace('faction_', '').capitalize()} and {target_obj.get('faction_id', '').replace('faction_', '').capitalize()}; secretly communicate over dead-drop frequencies.",
                "unrequited": f"Harbors deep, unconfessed romantic longing for {t_name}, drawing courage in combat from their memory.",
                "former_flame": f"Former lovers whose romance dissolved under the strain of wartime duty, though deep embers of passion remain."
            }
            
            c["love_interest"] = {
                "target_id": target_id,
                "target_name": t_name,
                "relationship_type": r_type,
                "intensity": r_int,
                "grudge_multiplier": r_mult,
                "trauma_reaction": trauma,
                "lore_snippet": snippets[r_type]
            }
        else:
            c["love_interest"] = None

    # -------------------------------------------------------------------------
    # B. FRIENDSHIP NETWORKS (2 to 4 Close Friends)
    # -------------------------------------------------------------------------
    # Candidates: same faction pilots, wingmen, plus cross-faction acquaintances
    friend_pool = [p["id"] for p in characters if p["id"] != cid]
    # Prefer wingman or same faction
    preferred = [p["id"] for p in characters if p["faction_id"] == fac and p["id"] != cid]
    if c.get("wingman_id") and c["wingman_id"] in char_map:
        friends_list = [c["wingman_id"]]
    else:
        friends_list = []
    
    # Pick 2-3 additional distinct friends
    num_friends = rng.randint(2, 4)
    while len(friends_list) < num_friends:
        pick = rng.choice(preferred if preferred else friend_pool)
        if pick not in friends_list and pick != cid:
            friends_list.append(pick)
            
    bond_types = ["academy_classmates", "trench_survivors", "sworn_blood_pact", "cantina_cadre", "veteran_wingmen"]
    b_type = rng.choice(bond_types)
    synergies = {
        "academy_classmates": "+15% formation accuracy when deployed in adjacent grid tiles.",
        "trench_survivors": "+20 Morale threshold against battlefield panic when friend is alive on grid.",
        "sworn_blood_pact": "If friend drops below 25% integrity, gains +2 Movement AP and +15% damage to rush to defense.",
        "cantina_cadre": "-25% hiring cost discount if this pilot's friend is already contracted by player PMC.",
        "veteran_wingmen": "+10% evasion and synchronized counter-battery fire against attacking enemies."
    }
    
    c["friendships"] = {
        "friend_ids": friends_list,
        "friend_names": [char_map[fid]["name"] for fid in friends_list if fid in char_map],
        "bond_type": b_type,
        "sortie_synergy": synergies[b_type]
    }

    # -------------------------------------------------------------------------
    # C. PROCEDURAL PLAYTHROUGH ALLEGIANCE VARIATION
    # -------------------------------------------------------------------------
    # Categories:
    # 1. Diehard Purist: 0.0 flexibility (High Command, Dynastic Heads)
    # 2. Career Officer: 0.15 flexibility (Tier 3 Aces, Dedicated Staff)
    # 3. Disillusioned Veteran: 0.35 flexibility (Tier 2 Veterans, Frontline Grunts)
    # 4. Free Contractor: 0.55 flexibility (Tier 1 Rookies, Scrappers, Techs)
    # 5. Roaming Ronin: 0.80 flexibility (Independent figures)
    
    if not is_rec:
        # High Command / VIPs are almost universally purists
        loyalty = "diehard_purist"
        flex = 0.0
        weights = {f_key: 0.0 for f_key in ["faction_terran", "faction_colony", "faction_syndicate", "faction_zaibatsu", "independent"]}
        weights[fac] = 1.0
        hooks = {fac: "Canonical high command leader loyal to the state apparatus."}
    elif fac == "independent":
        loyalty = "roaming_ronin"
        flex = 0.80
        weights = {
            "independent": 0.30,
            "faction_terran": 0.20,
            "faction_colony": 0.20,
            "faction_syndicate": 0.15,
            "faction_zaibatsu": 0.15
        }
        hooks = {
            "independent": "Free-roaming mercenary available across cantina hiring terminals.",
            "faction_terran": "Retained on exclusive retainer by the Terran Defense Senate.",
            "faction_colony": "Contracted by the Jovian Star-Legion to augment orbital patrols.",
            "faction_syndicate": "Hired by Callisto cartel bosses to escort heavy scrap convoys.",
            "faction_zaibatsu": "Signed a private security enforcement pact with Zaibatsu brokers."
        }
    else:
        if tier >= 3:
            loyalty = "career_officer"
            flex = 0.15
            weights = {f_key: 0.02 for f_key in ["faction_terran", "faction_colony", "faction_syndicate", "faction_zaibatsu", "independent"]}
            weights[fac] = 0.85
            weights["independent"] = 0.07
        elif tier == 2:
            loyalty = "disillusioned_veteran"
            flex = 0.35
            weights = {f_key: 0.05 for f_key in ["faction_terran", "faction_colony", "faction_syndicate", "faction_zaibatsu", "independent"]}
            weights[fac] = 0.65
            weights["independent"] = 0.15
        else:
            loyalty = "free_contractor"
            flex = 0.50
            weights = {f_key: 0.10 for f_key in ["faction_terran", "faction_colony", "faction_syndicate", "faction_zaibatsu", "independent"]}
            weights[fac] = 0.50
            weights["independent"] = 0.20
        
        # Normalize weights to sum exactly to 1.0
        tot = sum(weights.values())
        weights = {k: round(v / tot, 3) for k, v in weights.items()}
        # Ensure exact 1.0 sum
        diff = round(1.0 - sum(weights.values()), 3)
        weights[fac] = round(weights[fac] + diff, 3)
        
        hooks = {
            "faction_terran": f"Serving in active Terran infantry units protecting Earth and Lunar supply lines.",
            "faction_colony": f"Accepted an amnesty charter and orbital citizenship from the Colony Star-Legion.",
            "faction_syndicate": f"Dishonorably discharged or court-martialed; now flying for the Rim Cartels.",
            "faction_zaibatsu": f"Recruited by Zaibatsu headhunters with an advance signing bonus to pay family debt.",
            "independent": f"Went freelance after habitat purges; sells services on the open mercenary market."
        }

    c["allegiance_variance"] = {
        "canonical_faction": fac,
        "ideological_loyalty": loyalty,
        "flexibility_score": flex,
        "playthrough_weights": weights,
        "defection_hooks": hooks
    }

# Save back to file
with open(ROSTER_PATH, "w", encoding="utf-8") as f:
    json.dump({"total_figures": len(characters), "characters": characters}, f, indent=4)

print(f"✓ Successfully enriched all {len(characters)} characters with:")
print(f"  - Love interests & romance trauma triggers")
print(f"  - 2-4 close friendship networks & sortie synergies")
print(f"  - Procedural playthrough allegiance weights & defection hooks")
