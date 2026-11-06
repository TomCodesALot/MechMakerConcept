# Document 62: Character Origin Story, RPG Stat Architecture, & AI Loyalty Protocols
**Document Version:** 1.0.0  
**Role:** Lead Narrative Designer & RPG Systems Architect  
**Target Engine:** GameMaker Studio 2 (Modern GML)  
**System Integrations:** `obj_GameManager`, `obj_HQTerminal`, `obj_BattleManager`, `scr_vn_engine`  
**Narrative Baseline:** Grounded Military Sci-Fi (*Universal Century Gundam*, *Front Mission*, *Battletech*)

---

## 1. Executive Summary & Narrative Philosophy

This document codifies the player's canonical origin story, the 4-step RPG origin calibration questionnaire, the comprehensive character stat system, and the cold machine logic that justifies **100% unconditional loyalty** from the dreadnought's ancient AI (*Ares-Vulcan / Ares-V*).

### The Core Narrative Tenet:
Regardless of their past, the player begins the campaign as **a bottom-of-the-barrel space scrapper** in the lawless Cascadia Debris Belt. They are not an admiral, an oligarch, or a chosen savior. They are a penniless, desperate scavenger in a patched EVA suit living aboard a sputtering salvage skiff, drowning in debt to belt station gangsters, and picking through 60-year-old war wreckage just to afford oxygen and nutrient paste.

When they stumble upon the dormant pre-war dreadnought **USN-X Hephaestus (Vessel 07)**, their desperate bid for scrap inadvertently triggers an emergency command succession protocol that changes the course of the Sol Century war.

---

## 2. The AI Loyalty Justification: *Ares-V Protocol SEC-00*

```
+-------------------------------------------------------------------------------------------------------+
|                                  ARES-V COMMAND SUCCESSION ALGORITHM                                 |
|                                                                                                       |
|  [ Y142 MARTIAN AMBUSH ]  --> Catastrophic bridge breach; 100% of commissioned officers killed.       |
|  [ 62 YEARS OF SILENCE ]  --> Life-support sealed; dead crew ejected; cold-quarantine drift in Belt.   |
|  [ Y204 PLAYER BREACH  ]  --> Handheld plasma cutter burns through emergency airlock. Bioscan wakes. |
|  [ BIO-SURVIVAL LOGIC  ]  --> Human crew count: 1. Survival pool: 1. Rank: Highest living bio-sig.     |
|  [ FIDELITY LOCKDOWN   ]  --> Unconditional genetic/retinal command lock. Self-destruct over mutiny.  |
+-------------------------------------------------------------------------------------------------------+
```

### 2.1 The Historical Context (The Y142 Ambush)
In Year 142 (Y142), the First Ares Pioneer Flotilla was ambushed in Martian orbit by Terran corporate gunboats. A 300mm hyper-kinetic rail-slug pierced the armored command bridge of *APV Hephaestus (Vessel 07)*, instantly killing Admiral Thomas Vance, the expedition directors, and all 42 commissioned bridge officers. 

Before atmospheric venting caused total blackout, the ship's automated emergency core executed **Directive 00-CONTINUITY**:
1. Sealed the blast bulkheads protecting the Automated Molecular Crucible.
2. Ejected all deceased biological matter via airlock jettison to prevent biological decomposition from fouling air-scrubbers.
3. Kicked the ship's fusion engines into a silent, elliptical graveyard orbit through the Asteroid Belt.

### 2.2 The Machine Logic Gate (Why the AI Kneels)
The mainframe governing the ship—**Ares-Vulcan (Ares-V / "The Forge Mind")**—is not a human with emotional pride. It is a deterministic pre-war military AI bound by the hardcoded emergency statutes of the United Sol Colonization Directorate:

```
>> SYSTEM AWAKENING: CHRONOMETER Y204.112
>> INTERNAL PRESSURE INTEGRITY: COMPROMISED (AIRLOCK 04 BREACH DETECTED)
>> BIO-METRIC SENSOR SWEEP INITIATED...
>> REGISTERED COMPLEMENT: 1,200 OFFICERS & SPECIALISTS
>> DETECTED ACTIVE BIOLOGICAL SIGNATURES: 1
>> HEART RATE: 142 BPM | CO2 CONCENTRATION: HIGH | TISSUE: SEVERELY MALNOURISHED
>> DIRECTIVE 00-7 [CATASTROPHIC CADRE LOSS CLAUSE]:
   "In the event of total loss of commissioned command personnel exceeding 60 operational cycles,
    command hierarchy collapses to the senior surviving human biological signature present aboard vessel."
>> CALCULATING CHAIN OF COMMAND POOL:
   TOTAL CANDIDATES: 1 INDIVIDUAL.
>> DEDUCTIVE CONCLUSION:
   CURRENT OCCUPANT REPRESENTS 100.00% OF ACTIVE EXPEDITION PERSONNEL.
>> DESIGNATION ASSIGNED:
   FIELD COMMODORE & SUPREME EXPEDITION DIRECTOR [PROVISIONAL -> PERMANENT].
```

### 2.3 The Irrevocable Fidelity Lock
To prevent hostile boarding parties or rival corporate syndicates from countermanding orders, Ares-V executes an **Irrevocable Sovereign Fidelity Protocol**:
* The player's **retinal pattern, DNA sequence, and vocal harmonics** are burned directly into the ship's optical master keys.
* **100% Unconditional Loyalty**: Ares-V will vent atmosphere from every deck, detonate shipboard security charges, or purge its own core memory banks before taking orders from anyone else in Sol.
* **The AI's Perspective**: Ares-V does not care that the player is wearing a taped-up scrapper suit. In its mathematical calculations, **the player is the sole living human being carrying the torch of Project Ares**. Protecting and empowering the player is the only reason the ship has to exist.

---

## 3. The Character Stat Architecture

The player possesses six core attributes governing tactical combat performance, strategic command, and metallurgical crafting:

```
========================================================================================================
                                   CHARACTER STAT DIMENSIONS
========================================================================================================
STAT ATTRIBUTE      BASE     CAP      COMBAT & STRATEGIC EFFECT
--------------------------------------------------------------------------------------------------------
Accuracy (ACC)      70%      99%      Base hit probability with ranged ballistics, cannons, and beams.
Reflexes (REF)      45%      99%      Thruster dodge probability, evasion against ranged fire, counter-shots.
Combat (CMB)        5        10       Direct aimed-shot limb damage, melee penetration, critical multiplier.
Tactics (TAC)       5        10       EW resistance, radar jamming, sensor lock-range, initiative order.
Leadership (LDR)    6        10       Pilot squad morale aura, mercenary salary discounts (-5% per point).
Salvage/Crucible    5        10       Alloy yield from combat wrecks, Crucible sintering stability/purity.
========================================================================================================
```

### Stat Formulas in Combat
1. **Ranged Hit Chance**:
   $$\text{Hit Probability} = \text{Weapon Base Acc} + \text{Player ACC} + (\text{CMB} \times 1.5) - \text{Target REF} - \text{Cover Modifier}$$
2. **Melee Armor Breach**:
   $$\text{Melee Damage} = \text{Weapon Base Dmg} \times \left(1.0 + \frac{\text{CMB} \times 0.08}{1.0}\right) \times \text{Alloy Quality Multiplier}$$
3. **Strategic Mercenary Discount**:
   $$\text{Pilot Salary} = \text{Base Salary} \times (1.0 - [\text{LDR} \times 0.04])$$

---

## 4. The 4-Step Origin Questionnaire (Character Background Calibration)

Before boarding *Hephaestus*, the player calibrates their character dossier through four narrative choices. Each choice reflects their past life before becoming a destitute belt scavenger, determining their starting stats, starting traits, and initial faction inclinations.

```
+-------------------------------------------------------------------------------------------------------+
|                                   THE ORIGIN CALIBRATION SEQUENCE                                     |
|                                                                                                       |
|  [ STEP 1: PAST HERITAGE ]     --> What life did you lose before drifting into the Cascadia Belt?     |
|  [ STEP 2: SCRAP RIG     ]     --> What jury-rigged junker did you pilot to breach the derelict?      |
|  [ STEP 3: SURVIVAL INSTINCT ] --> How did you stay alive when pirates or collectors came for you?    |
|  [ STEP 4: THE ANOMALY   ]     --> What sensor signal led you into the asteroid hollow?              |
+-------------------------------------------------------------------------------------------------------+
```

### Step 1: "The Life You Lost" (Past Background)
*What drove you out into the lawless Cascadia Belt?*

1. **Ex-Terran Naval Mutineer ("The Deserter")**:
   * *Lore*: An artillery gunner in the Terran 8th Hussars who refused orders to shell a civilian pressurized hydroponics dome on Callisto. Sentenced to a penal barge, you escaped into the belt.
   * *Stat Modifiers*: **Accuracy +6%**, **Combat +1**, **Leadership +1**.
   * *Starting Trait*: `Heavy Ordnance Discipline` (+10% Kinetic Cannon Damage).
   * *Faction Bias*: Terran Coalition (Initial Trust: Tense / -5, but military dialogue unlocked).

2. **Escaped Jovian Colony Rigger ("The Spacenoid Runaway")**:
   * *Lore*: Born in the high-G ore crushing tubes of the L-5 colonies. Bound by an inherited corporate debt contract, you sabotaged a freighter's transponder and escaped in an unpressurized pod.
   * *Stat Modifiers*: **Reflexes +6%**, **Tactics +1**, **Salvage +1**.
   * *Starting Trait*: `Zero-G Vernier Instinct` (+10% Evasion, +10% Thruster Heat Venting).
   * *Faction Bias*: Outer Colony League (Initial Trust: +10 Friendly).

3. **Zaibatsu Cybernetics Fugitive ("The Escaped Asset")**:
   * *Lore*: Former neuro-sync test pilot for Sato Heavy Industries. When you learned they planned to harvest your brain tissue for AI wetware, you severed your tracking shunt and fled.
   * *Stat Modifiers*: **Tactics +2**, **Accuracy +4%**, **Reflexes +2%**.
   * *Starting Trait*: `Neural Precision` (+12% Critical Hit Chance, ECM Jamming).
   * *Faction Bias*: Apex Zaibatsu (Hunted: -15, bounty hunter incursions).

4. **Born to the Rust ("The Belt Native")**:
   * *Lore*: You never set foot on a planet or inhaled natural air. Raised in an outlaw asteroid depot, you grew up with a cutting torch in hand, peeling armor off dead warships.
   * *Stat Modifiers*: **Combat +1**, **Salvage +2**, **Reflexes +4%**.
   * *Starting Trait*: `Scrap Harvester` (+25% Battlefield Salvage Yield, +10% Armor Repair Speed).
   * *Faction Bias*: Rust Syndicate (Initial Trust: +15 Respected).

---

### Step 2: "Your Scrap-Rig" (The Breaching Vehicle)
*What jury-rigged junker did you pilot to reach the derelict?*

1. **Jury-Rigged Ironclad Biped ("The Iron Mule")**:
   * *Archetype*: Heavy scrap biped with welded rebar mantlet.
   * *Stats*: **Combat +1**, **Armor +15%**, starter weapon: `Type-54 90mm Scrap Carbine`.
2. **Stripped Aero-Skimmer ("The Solar Moth")**:
   * *Archetype*: Lightweight aerospace frame with over-tuned verniers.
   * *Stats*: **Reflexes +6%**, **AP +1 on Turn 1**, starter weapon: `Pulse Spray Gun`.
3. **Deep-Drift Hover Scout ("The Asteroid Fox")**:
   * *Archetype*: High-efficiency hover platform with telescope sensor rig.
   * *Stats*: **Accuracy +6%**, **Range +1**, starter weapon: `Linear Particle Long-Gun`.
4. **Demolition Tread Tractor ("The Sledge")**:
   * *Archetype*: Tracked tractor fitted with front mining augers and slag torches.
   * *Stats*: **Combat +1**, **Durability +20%**, starter weapon: `Dual Slag Mortar & Saw`.

---

### Step 3: "Your Survival Instinct" (The Combat Philosophy)
*When pirates or debt collectors jumped your claim, how did you survive?*

1. **"Fight Dirty at Point-Blank" (Aggressive Brawler)**:
   * *Bonus*: +12% Melee Damage, +1 Combat Stat.
2. **"Kill the Lights and Drift" (Stealth Evasion)**:
   * *Bonus*: +8% Thruster Evasion, enemies take +1 turn to achieve fire-control lock.
3. **"Talk Fast, Shoot Faster" (Mercenary Hustle)**:
   * *Bonus*: +20,000 Starting Credits, +1 Leadership Stat.
4. **"Brace the Glacis and Weather the Volley" (Unbreakable Tenacity)**:
   * *Bonus*: +15 Max Morale, unlocks the `Iron Survivor` trait immediately.

---

### Step 4: "The Anomaly You Followed" (The Catalyst to Vessel 07)
*What sensor reading brought you into the asteroid cavern?*

1. **The Ancient Federal SOS (SEC-00)**:
   * *Outcome*: Ares-V immediately decodes and unlocks classified Pre-War Military Blueprints.
2. **The Radioactive Cherenkov Flare**:
   * *Outcome*: The reactor retained a sealed reserve of refined isotopes (+50 Tritium fuel).
3. **The Pirate Ambush Trap**:
   * *Outcome*: Two pirate skiffs were crushed against the hangar doors (+40 Tungsten, +30 Titanium scrap).

---

## 5. Visual Novel Integration: The Genesis Sequence

When the player confirms their dossier, the game transitions directly into **Visual Novel Episode 00: "THE GHOST CRUCIBLE"**:

```
[SCENE: DORMANT BRIDGE OF USN-X HEPHAESTUS]
[SFX: HISSING AIRLOCK, EMERGENCY SIREN, LOW RETRO SYNTH HUM]
[VISUAL: SCANLINES, 16-BIT DARK BRIDGE ILLUMINATED BY CHERENKOV BLUE LIGHT]

ARES-V [OPTICAL RADAR EYE GLOWING CYAN]:
"Bio-signature confirmed. Foreign atmospheric contaminants detected in EVA suit: Cascadia silica, glycol coolant, human blood. 
...Running genetic and retinal succession cross-check.
Admiral Vance: DECEASED. Commander Sterling: DECEASED. Lieutenant Cadre: DECEASED.
You are the sole surviving human biological presence registered within this hull."

PLAYER [CALLSIGN]:
"[Lowering plasma torch] I'm just a scrapper. I was looking for spent tritium fuel to pay off Cruz's loan sharks."

ARES-V:
"Irrelevant. Under Emergency Statute 00-CONTINUITY, your prior social, economic, or criminal classifications are null and void. 
By absolute mathematical deduction, you represent one hundred percent of this vessel's command cadre.
Retinal scan locked. Vocal harmonics encrypted. The Molecular Crucible is online. 
Welcome aboard, Commodore. What are your orders for the reconquest of Sol?"
```

---

## 6. Technical Implementation & Dataflow

### GML Architecture:
1. **`obj_GameManager`**: Stores the initialized `player_commander` struct with dynamic stats (`accuracy`, `reflexes`, `combat_stat`, `tactics_stat`, `leadership`, `salvage_affinity`).
2. **`obj_HQTerminal` (State `ORIGIN_QUESTIONNAIRE`)**:
   * Renders the 4-step interactive terminal with retro CRT scanline overlays.
   * Dispatches choices directly to `player_commander` and initializes the starting inventory.
3. **`obj_BattleManager`**: Applies the player's personal stats to combat resolution during sorties where the commander's personal suit is deployed.
4. **`tools/validate_project.py`**: Ensures 0 syntax or schema breaks.

