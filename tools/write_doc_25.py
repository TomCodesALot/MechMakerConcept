import os

doc_text = """# 25. Mobile Suit Corporate Competitions & PMC Squad Doctrine
**Document Version:** 1.0.0  
**Roles:** Lead Game Designer, Narrative Designer, Lead QA Engineer, GameMaker Expert Developer  
**Target Engine:** GameMaker Studio 2 (Modern GML)  
**Aesthetic Baseline:** 16-Bit Retro SNES Tactical Simulation (*Front Mission*, *Super Robot Wars*, *Gihren's Greed*)

---

## 1. Executive Summary: The Dual-Identity Gameplay Loop

In *MechMaker Concept*, the player does not operate purely as a detached corporate design bureau, nor merely as a hired-gun mercenary commander. The core fantasy resides in the tension and synergy between two interlocking roles:

$$\\text{Orbital Defense Contractor (Weapons Foundry)} \\longleftrightarrow \\text{Frontline Mercenary Strike Commander (PMC Squad)}$$

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                   THE DUAL-IDENTITY MASTER GAMEPLAY LOOP               │
  └───────────────────────────────────┬────────────────────────────────────┘
                                      │
        ┌─────────────────────────────┴─────────────────────────────┐
        ▼                                                           ▼
 ┌───────────────────────────────┐                 ┌───────────────────────────────┐
 │   ROLE 1: DEFENSE CONTRACTOR  │                 │    ROLE 2: PMC STRIKE SQUAD   │
 │ • Pre-War Dreadnought Foundry │                 │ • Hired Ace Pilot Platoon     │
 │ • Sintering Exotic Alloys     │                 │ • 4-to-8 Unit Battlegroup     │
 │ • Modular Chassis Engineering │                 │ • Mercenary Sorties & Strikes │
 │ • Superpower Tenders & Bidding│                 │ • Tactical Isometric Combat   │
 └──────────────┬────────────────┘                 └───────────────┬───────────────┘
                │                                                  │
                │◄─────────────── COMBAT-PROVEN ───────────────────┤
                │         PEDIGREE & FIELD TELEMETRY               │
                │                                                  │
                ▼                                                  ▼
 ┌───────────────────────────────┐                 ┌───────────────────────────────┐
 │  CORPORATE PROCUREMENT FLY-OFF│                 │  THE ARMS DEALER PARADOX      │
 │ • Out-score Mega-Corp Rivals  │                 │ • Keep "Commander Custom"    │
 │ • Fly-Off Proving Benchmarks  │                 │ • Export "Standard Line"     │
 │ • Win Millions & Royalties    │                 │ • Exploit Blueprint Flaws     │
 └───────────────────────────────┘                 └───────────────────────────────┘
```

1. **The Contractor Role (Macro-Strategy & Engineering):**  
   The player uses the salvaged *USN-X Hephaestus* dreadnought foundry to synthesize proprietary alloys, forge high-spec modular components (Reactors, Limbs, Avionics, Heavy Ordnance), and submit cutting-edge chassis to superpower military procurement tenders.
2. **The PMC Squad Role (Micro-Tactics & Field Operations):**  
   The player equips their own mercenary strike platoon with newly engineered prototypes. By deploying these suits into live combat missions (bounty hunts, orbital station defense, asteroid trench assaults), the player's ace pilots generate invaluable **Field Telemetry and Combat-Proven Pedigree**.
3. **The Synergistic Payoff:**  
   Sterile laboratory dyno test numbers submitted by rival defense conglomerates (Valkyrie, Astraea, Hyperion) cannot match the hardened credibility of a machine that has survived real orbital flak and downed enemy aces. High combat pedigree unlocks decisive tender scoring bonuses, while winning contracts funds the player's private army and licenses export hulls across the solar system.

---

## 2. The 5 Superpower Procurement Tenders & 4 Corporate Competitors

Superpower defense ministries issue competitive tenders across five strategic combat roles. Four established mega-defense corporations compete against the player for these multi-billion Credit government contracts.

### 2.1 The 4 Rival Corporate Defense Contractors

| Corporation | Alignment / Faction | Chief Executive / Designer | Primary Doctrine | Flagship Chassis |
| :--- | :--- | :--- | :--- | :--- |
| **Valkyrie Heavy Industries (VHI)** | Terran Coalition | Baroness Victoria Sterling | Super-heavy tungsten composite, kinetic railcannons, trench-line endurance | *GHA-07 Ironclad*, *BHM-01 Behemoth* |
| **Astraea Orbital Dynamics (AOD)** | Outer Colonies | Dr. Sorel Vance | Micro-gravity vernier agility, coherent plasma beams, composite energy screens | *AET-01 Aether*, *HLS-08 Helios* |
| **Rustworks Cartel & Scav-Forge** | Mercenary Syndicates | Warlord 'Grease' Garvin | Over-tuned diesel-fusion cores, heavy rotary vulcans, cheap salvage metallurgy | *SCR-12 Hyena*, *SLG-04 Slag Reaver* |
| **Hyperion Advanced Tactical Systems (HATS)** | Apex Zaibatsu | Director Renzo Takahashi | Neural-sync cockpits, predictive targeting AI, active thermo-optic camouflage | *ZAI-03 Muramasa*, *SUS-00 Susanoo-X* |

### 2.2 The 5 Strategic Procurement Roles

```
  [ROLE 1: LINEBREAKER]     ◄─── Heavy Armor, Kinetic Wall, Trench Breaching
  [ROLE 2: INTERCEPTOR]     ◄─── High-G Agility, Plasma Beam, Hit-and-Run Flanking
  [ROLE 3: EW RECON]        ◄─── Sensor ECM/ECCM, Target Painting, Cloaking Infiltration
  [ROLE 4: SIEGE ARTILLERY] ◄─── Long-Range Railguns, Swarm Missiles, Area Denial
  [ROLE 5: GUERILLA BRAWLER]◄─── Close-Quarters Hydraulic Cleavers, High Resilience, Scrap Economy
```

* **Role 1: Linebreaker / Frontline Wall**  
  *Evaluated by:* Terran Munitions Board (General Hector Vance).  
  *Core Metrics:* Armor Rating (40%), Firepower Penetration (35%), Reactor Stability (15%), Speed (10%).
* **Role 2: Orbital Interceptor / High-Speed Skirmisher**  
  *Evaluated by:* Colony Defense Council (Minister Jun Takahashi).  
  *Core Metrics:* Vernier Speed (40%), Energy Output (30%), Weapon Coherence (20%), Armor (10%).
* **Role 3: Electronic Warfare & Reconnaissance (EW / Sensor Infiltrator)**  
  *Evaluated by:* Apex Procurement Bureau (Director Renzo Takahashi).  
  *Core Metrics:* Sensor Accuracy / ECM (35%), Power Surplus (25%), Stealth / Evasion (25%), Armor (15%).
* **Role 4: Long-Range Siege Artillery Platform**  
  *Evaluated by:* Terran-Colony Joint Ordnance Group.  
  *Core Metrics:* Kinetic Damage Output (40%), Thermal Dissipation (30%), Weapon Range / Targeting (20%), Speed (10%).
* **Role 5: Low-Cost Guerilla Raider / Combat Scavenger**  
  *Evaluated by:* Rogue Syndicate Brokers (Kruger 'Iron-Eye').  
  *Core Metrics:* Material Build Cost (35%), Armor-Piercing Punch (30%), Repair Speed (20%), Reactor Output (15%).

---

## 3. The "Combat-Proven Pedigree" System

In standard fly-offs, candidate mechs are judged in clean-room proving grounds. However, military procurement boards heavily distrust theoretical laboratory simulations. When the player deploys a candidate prototype in their active PMC squad, the chassis accumulates **Combat-Proven Pedigree Points (CPP)**.

### 3.1 Combat Telemetry Metrics Tracked Per Chassis

Every deployable mobile suit in the player's hangar tracks a persistent `combat_pedigree` struct:

```json
{
  "sorties_deployed": 6,
  "sorties_survived": 6,
  "confirmed_kills": 14,
  "ace_kills": 3,
  "damage_mitigated_total": 4850,
  "structural_crits_survived": 2,
  "reactor_meltdowns_avoided": 1,
  "pedigree_rating": "BATTLE_HARDENED",
  "telemetry_score_bonus": 18.5
}
```

### 3.2 Mathematical Formulation of Pedigree Bonus

The Telemetry Score Bonus ($S_{\\text{pedigree}}$) is calculated and added directly to the tender composite fly-off score:

$$S_{\\text{pedigree}} = \\min \\left(25.0, \\; (N_{\\text{sorties}} \\times 1.5) + (K_{\\text{grunts}} \\times 0.5) + (K_{\\text{aces}} \\times 3.0) + \\left(\\frac{D_{\\text{mitigated}}}{1000} \\times 1.0\\right) \\right)$$

| Pedigree Tier | Required CPP | Fly-Off Modifier | Liaison Reaction Dialogue |
| :--- | :--- | :--- | :--- |
| **UNTESTED (Lab Prototype)** | 0 | +0.0 pts | *"Valkyrie's telemetry looks great on paper, and so does yours. Let's see if it holds up under fire."* |
| **FIELD EVALUATED** | 1 - 7 | +5.0 pts | *"Your PMC recorded two live combat engagements with this unit. The board appreciates actual flight logs."* |
| **COMBAT PROVEN** | 8 - 15 | +12.0 pts | *"Six confirmed kills in the Jovian asteroid belt without joint seizure. This machine has real operational teeth."* |
| **BATTLE HARDENED** | 16 - 22 | +18.0 pts | *"Survived three artillery bombardments and downed a syndicate ace? The infantry will fight to be assigned this unit."* |
| **LEGENDARY VETERAN** | 23 - 25 | +25.0 pts | *"This exact chassis broke the siege of Ceres. Faction leadership insists on adopting it regardless of corporate objections!"* |

---

## 4. "Showcase by Fire" — Live Demonstration Sorties

When bidding on major Grade-A contracts, factions are not satisfied with mathematical benchmarks alone. They issue an operational challenge: **The Live Showcase Sortie**.

```
               ┌────────────────────────────────────────────────────────┐
               │          OPERATION "SHOWCASE BY FIRE" SORTIE           │
               └───────────────────────────┬────────────────────────────┘
                                           │
         ┌─────────────────────────────────┴─────────────────────────────────┐
         ▼                                                                   ▼
  [EMBEDDED MILITARY LIAISON]                                       [RIVAL CONTRACTOR OPPOSITION]
  • Observer transport attached to squad                            • Competitor deploys hired PMC kill-team
  • Evaluates live weapon heat, armor hits                          • Attempts to destroy player candidate
  • Records pilot cockpit telemetry                                 • Failure: -30 Faction Standing, Tender Lost
```

1. **Mandatory Candidate Deployment:**  
   The candidate mobile suit must be deployed in the player's 4-to-8 unit combat battlegroup, piloted by one of your hired roster pilots.
2. **Embedded Evaluator Conditions:**  
   A liaison observation craft or hardened communications uplink monitors the battle in real time.
3. **Dynamic Mission Objectives:**
   * *Primary:* Eliminate the hostile force (pirate outpost, insurgent battery, or rogue corporate strike team).
   * *Telemetry Objective 1 (Thermal Resilience):* Never allow candidate mech heat to exceed 85% threshold.
   * *Telemetry Objective 2 (Combat Dominance):* Candidate unit must personally secure at least 2 enemy kills.
   * *Telemetry Objective 3 (Armor Demonstration):* Absorb at least 500 kinetic or energy damage without losing an arm or torso breach.
4. **Outcome on Tender:**  
   Fulfilling all telemetry objectives during the sortie grants an automatic **INSTANT TENDER APPROVAL**, bypassing standard corporate bidding and awarding the full licensing contract immediately!

---

## 5. The Arms Dealer Paradox: "Commander Custom" vs. "Export Line"

Winning a procurement tender creates a dramatic tactical dynamic: **The Player Sells Weapons to the Universe, but Remains a Mercenary.**

```
                     ┌──────────────────────────────────────────────────┐
                     │            THE ARMS DEALER PARADOX               │
                     └─────────────────────────┬────────────────────────┘
                                               │
             ┌─────────────────────────────────┴─────────────────────────────────┐
             ▼                                                                   ▼
  [THE FACTION EXPORT LINE]                                           [THE PMC COMMANDER CUSTOM]
  • Mass-produced by the faction                                      • Retained solely in player's hangar
  • Economized stamped alloys                                         • 100% Purity Damascus/Tachyon alloys
  • Stamped commercial avionics                                       • Hand-tuned overcharged reactor (+20% AP)
  • Rewards player: +50k-150k Cr/turn                                 • Fielded by player's ace strike lance
```

### 5.1 Blueprint Vulnerability Exploitation (+Crit Trait)
Because the player engineered the mobile suit from the ground up, the player's PMC pilots understand every manufacturing shortcut, cooling conduit choke-point, and armor weld tolerance of the exported line.

When the player's PMC squad engages in combat against enemy units fielding a chassis designed by the player:
* **Passive Trait: `Blueprint Vulnerability Exploitation`** is automatically active.
* **+15% Critical Hit Chance** against all target units of that blueprint type.
* **+20% Armor Penetration** when targeting the torso core.
* **Comms Dialogue Trigger:**  
  *"Commander, that hostile squad is fielding our GHA-07 line units! Focus fire on the starboard exhaust baffle—the Coalition factory always skimps on the titanium retaining ring!"*

---

## 6. Squad Role Synergy Matrix: Building for the Tender Equips the Platoon

A player never builds a mobile suit purely to win a tender; every chassis designed directly strengthens the PMC strike squad. The 5 procurement roles map 1-to-1 onto tactical squad formations:

```
  ┌─────────────────────────────────────────────────────────────────────────────────┐
  │                        4-MECH TACTICAL SQUAD FORMATION                          │
  ├───────────────────┬───────────────────┬───────────────────┬─────────────────────┤
  │   SLOT 1: TANK    │  SLOT 2: FLANKER  │  SLOT 3: SNIPER   │  SLOT 4: EW SUPPORT │
  ├───────────────────┼───────────────────┼───────────────────┼─────────────────────┤
  │ Role 1 Candidate  │ Role 2 Candidate  │ Role 4 Candidate  │ Role 3 Candidate    │
  │ • Linebreaker     │ • Interceptor     │ • Siege Artillery │ • Recon / ECM       │
  │ • Absorbs fire    │ • High-G flank    │ • 7-Tile railgun  │ • Target painter    │
  │ • Braces frontline│ • Beam saber ace  │ • Missile volley  │ • Sensor jammer     │
  └───────────────────┴───────────────────┴───────────────────┴─────────────────────┘
```

By engineering candidate suits for the Terran Linebreaker tender, the player builds their dream squad tank. By building a high-speed interceptor for the Outer Colonies, the player acquires an elite flanker for their own aces. **R&D and mercenary combat form a single unified progression loop.**

---

## 7. Rival Corporate Retaliation & Foundry Defense Sorties

Mega-corporations do not take market share loss gracefully. As the player wins tenders, rival corporate hostility rises from 0% to 100%:

| Rival Hostility | Corporate Reaction Event | Combat Implication |
| :--- | :--- | :--- |
| **0 - 24% (Normal)** | Corporate PR smearing, minor tariff spikes | None. |
| **25 - 49% (Tense)** | Corporate espionage attempts | Saboteurs attempt to corrupt blueprint data; requires engineer alert. |
| **50 - 74% (Hostile)** | Supply line ambushes | Ore cargo convoys ambushed by corporate-funded privateers; player squad must deploy on escort sorties. |
| **75 - 100% (Blood Feud)** | Black-Ops Hit Squads & Foundry Raids | Rival company deploys elite test pilots and ace assassins in a direct assault against the Dreadnought Foundry! |

---

## 8. Narrative Lore & Dialogue Scripts

```json
{
  "evaluator_briefings": {
    "terran_general_vance": {
      "lab_spec_only": "Sterling at Valkyrie swears the Ironclad-X can take a direct nuclear torpedo. But I've seen their test data—it was conducted in a vacuum chamber in Geneva. What's your prototype's track record, Commander?",
      "combat_proven_bonus": "Now that's what I call a flight log. Eight sorties in the Jovian trench, three confirmed heavy kills, and your pilot walked away without a scratch on the cockpit seal. The Terran Munitions Board votes to replace Valkyrie's contract with yours immediately.",
      "arms_dealer_irony": "Just remember whose colors you're wearing, mercenary. You might sell us our standard battle line, but if your guns ever point toward Earth, our pilots know how to shoot back."
    },
    "colony_minister_takahashi": {
      "lab_spec_only": "Astraea Dynamics claims their Helios interceptor has zero vernier lag. Yet your telemetry suggests your frame operates at twenty percent higher heat efficiency during prolonged high-G burns. Prove it in the field.",
      "combat_proven_bonus": "Magnificent. Your ace pilot Cruz danced through an entire syndicate minefield and downed their flagship's escort wing. The Colony Defense Council adopts your blueprint as the AET-Mark II standard!"
    }
  },
  "pilot_squad_banter": {
    "fielding_prototype": "Commander, this new alloy plating smells like ozone and burnt carbon. Controls feel tight—let's see if she holds together when the flak starts flying.",
    "pedigree_accumulated": "Telemetry upload complete. Let those corporate desk-jockeys in Neo-Tokyo try to match that data in their simulators!",
    "fighting_own_exported_mech": "Hostile squad is using our export model! Aim for the port heat sink baffle—we know the factory cut corners on that exhaust weld!"
  }
}
```

---

## 9. GameMaker Implementation Architecture

### 9.1 Data Structure Updates (`obj_GameManager`)

```gml
// 1. In inventory.deployable_mechs struct, add combat_pedigree:
combat_pedigree: {
    sorties_deployed: 0,
    sorties_survived: 0,
    confirmed_kills: 0,
    ace_kills: 0,
    damage_mitigated: 0,
    pedigree_rating: "UNTESTED",
    telemetry_bonus: 0.0
},
spec_type: "COMMANDER_CUSTOM", // Distinct from "EXPORT_LINE"

// 2. Telemetry Accumulator Function in obj_GameManager:
accumulate_combat_pedigree = function(_mech_id, _kills, _aces, _dmg_taken, _survived) {
    for (var m = 0; m < array_length(inventory.deployable_mechs); m++) {
        var _mech = inventory.deployable_mechs[m];
        if (_mech.id == _mech_id) {
            if (!variable_struct_exists(_mech, "combat_pedigree")) {
                _mech.combat_pedigree = {
                    sorties_deployed: 0,
                    sorties_survived: 0,
                    confirmed_kills: 0,
                    ace_kills: 0,
                    damage_mitigated: 0,
                    pedigree_rating: "UNTESTED",
                    telemetry_bonus: 0.0
                };
            }
            var _cp = _mech.combat_pedigree;
            _cp.sorties_deployed += 1;
            if (_survived) _cp.sorties_survived += 1;
            _cp.confirmed_kills += _kills;
            _cp.ace_kills += _aces;
            _cp.damage_mitigated += _dmg_taken;
            
            // Calculate Telemetry Bonus (Max 25 pts)
            var _pts = (_cp.sorties_survived * 1.5) + (_cp.confirmed_kills * 0.5) + (_cp.ace_kills * 3.0) + floor(_cp.damage_mitigated / 1000.0);
            _cp.telemetry_bonus = min(25.0, _pts);
            
            if (_pts >= 23) _cp.pedigree_rating = "LEGENDARY_VETERAN";
            else if (_pts >= 16) _cp.pedigree_rating = "BATTLE_HARDENED";
            else if (_pts >= 8) _cp.pedigree_rating = "COMBAT_PROVEN";
            else if (_pts >= 1) _cp.pedigree_rating = "FIELD_EVALUATED";
            else _cp.pedigree_rating = "UNTESTED";
            
            show_debug_message("[CombatPedigree] Updated " + _mech.name + " -> " + _cp.pedigree_rating + " (+" + string(_cp.telemetry_bonus) + " pts)");
            break;
        }
    }
};
```

### 9.2 Integration into Procurement Trials (`obj_FactionManager`)

In `run_procurement_trial(_faction_id, _mech)`:
```gml
// Read combat pedigree bonus from candidate mech
var _pedigree_bonus = 0.0;
var _pedigree_rating = "UNTESTED";
if (variable_struct_exists(_mech, "combat_pedigree")) {
    _pedigree_bonus = _mech.combat_pedigree.telemetry_bonus;
    _pedigree_rating = _mech.combat_pedigree.pedigree_rating;
}

// Composite Fly-Off Calculation with Pedigree
var _composite_score = round((_base_weighted + _st_bonus + _pedigree_bonus) * 10.0) / 10.0;
```

---

## 10. SNES 16-Bit Retro Art & UI Design Brief

* **Fly-Off Arena Terminal (Tab 2 Subtab 1):**  
  * *Pedigree Certification Stamp:* Rectangular brass/amber bordered pixel badge reading `[COMBAT PROVEN: +12.0 PTS]` or `[BATTLE HARDENED: +18.0 PTS]`.
  * *Corporate Competitor Comparison Bars:* 4-way split horizontal graph comparing the Player Candidate, Valkyrie, Astraea, and Hyperion entries with 16-bit dithering.
  * *Evaluator Portrait Window:* 48x48 pixel military liaison portrait with typewriter dialog text and animated blink frames.
  * *Blueprint Flaw Indicator:* Crosshairs flashing amber on target mechs during tactical combat when `Blueprint Vulnerability Exploitation` triggers.
"""

with open('docs/25_mobile_suit_corporate_competitions_and_pmc_squad_doctrine.md', 'w') as f:
    f.write(doc_text)

print("Document 25 written cleanly with length:", len(doc_text))
