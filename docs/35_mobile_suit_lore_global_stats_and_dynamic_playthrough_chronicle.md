# Document 35: Mobile Suit Living Lore, Global Production Metrics, & Dynamic Playthrough Chronicle

## 1. Executive Summary & Narrative Architecture
This document establishes the comprehensive **Living Lore, Global Production, & Dynamic Playthrough Chronicle System** across the entire 100-mobile suit catalog and 54-suit historical timeline in *MechMakerConcept*. 

In alignment with grounded military sci-fi worldbuilding (inspired by *Front Mission*, *Armored Core*, and *Mobile Suit Gundam*), war machines in this universe are not static stat sheets. They are industrial artifacts forged by massive military-industrial conglomerates—burdened by corporate cost-cutting, mechanical quirks, pilot legends, and political tenders. 

Crucially, every chassis in the game now tracks its own **system-wide production history, operational deployment, combat casualties, and dynamic service chronicle**. When a player prototypes a superior PMC mobile suit and wins a faction procurement tender, the superseded state model is formally declared obsolete in the historical ledger, its assembly lines are scrapped or retooled, and a dynamic chronicle entry is permanently stamped into the machine's war record.

---

## 2. Lore Schema & Mechanical Dimensions
Every mobile suit in [`datafiles/mobile_suits/mobile_suit_catalog.json`](file:///home/tom/GameMakerProjects/MechMakerConcept/datafiles/mobile_suits/mobile_suit_catalog.json) has been enriched with the following core narrative fields:

1. **`historical_lore`**: Comprehensive historical briefing detailing state procurement origin, metallurgical rationale, geopolitical tensions, and corporate contracts.
2. **`manufacturing_quirks`**: Concrete engineering idiosyncrasies, hydraulic tolerances, reactor feedback loops, electrical harness headaches, and greasemonkey complaints.
3. **`battlefield_reputation`**: Frontline pilot slang, callsigns, cockpit ergonomics, fear factors, and veteran mercenary anecdotes.
4. **`doctrine_summary`**: Operational role and engagement profile within the faction's overarching military doctrine.
5. **`primary_theaters`**: Specific planetary and orbital combat zones where the chassis saw its most intense deployments (e.g., *Baikal Redoubt*, *L-5 Orbital Gateway*, *Ceres Mining Outpost*, *Olympus Mons Redoubt*).

### Faction Archetypes & Narrative Profiles

| Faction / Manufacturer | Doctrinal Philosophy | Typical Manufacturing Quirk | Pilot Slang & Reputation |
| :--- | :--- | :--- | :--- |
| **Terran Combine**<br>*(Valkyrie Heavy Industries)* | Monolithic cast-tungsten frontal cowls, high-caliber kinetic ballistics, diesel-fusion boilers. | Nose-heavy weight balance; hydraulic wear on knee pins; dense thermal steam plumes. | *"The Moving Wall"*, *"The Iron Sarcophagus"*; praised for unyielding armor, cursed for sluggish ground speed. |
| **Colony Coalition**<br>*(Astraea Orbital Dynamics)* | Superconducting aerosteel frames, Cherenkov blue plasma thrusters, particle beam rifles. | Superconductor magnetic hum (*"Jovian Chorus"*); micro-vernier valve pressure spikes; fragile drag limits. | *"The Flying Scalpel"*, *"The Blue Mosquito"*; supreme zero-G turn rates, but folds under kinetic artillery. |
| **Asteroid Syndicate**<br>*(Rustworks Salvage Cartel)* | Welded heterogeneous slag plates, pneumatic harpoon winches, scrap-flak brawling. | Off-center center of gravity; mismatched salvaged wiring; caustic exhaust venting into cockpit air. | *"The Junkyard Dog"*, *"Scrap Reaver"*; terror of trade convoys; brutal point-blank grappling melee. |
| **Mars Zaibatsu**<br>*(Hyperion Advanced Tactical Systems)* | Bio-neural spinal interface, liquid nitrogen coolant jackets, high-frequency tachyon katanas. | Neural phantom sensory feedback; sub-zero external frosting; severe power spikes during blade ignition. | *"The Black Scalpel"*; moves before human eyes can track; feared as an emotionless, surgical executioner. |
| **PMC Hephaestus**<br>*(Player Proprietary Hangar)* | Crucible alloy metallurgy, universal modular hardpoint lattices, adaptive multi-role systems. | Modular hardpoint locks require recalibration when swapping ballistic and beam cowls. | The ultimate mercenary survivor frame; turns corporate attrition into high-margin salvage profits. |

---

## 3. Global Production Numbers & Attrition Statistics
Every chassis now maintains real-time global telemetry representing the total war economy across the Sol system:

- **`production_count`**: Total units manufactured across all planetary and orbital factories.
  - *Mainline Standard Issue Grunts*: 2,800 – 5,600 units.
  - *Specialized Fire Support / Artillery*: 450 – 1,600 units.
  - *Ace Customs / Elite Prototypes*: 45 – 180 units.
  - *Player Blueprints*: Starts at initial batch size (0 – 120 units), scaling upward as tenders are won.
- **`active_units`**: Currently operational hulls deployed in active standing divisions and fleets.
- **`casualty_count`**: Confirmed combat losses neutralized in battle.
- **`kill_count`**: Confirmed enemy targets destroyed by this chassis type.
- **`combat_loss_ratio`**: `casualty_count / max(1, kill_count)`.
- **`survivability_rating`**: `round(100.0 * kill_count / (kill_count + casualty_count))`.

---

## 4. Dynamic Playthrough Chronicle & Living Arms Race
Rather than remaining static, the mobile suit's status evolves dynamically throughout the campaign based on player achievements, corporate competitions, and tactical combat:

### Dynamic Adoption Statuses
- **`standard_issue`**: Official mainline battle doctrine for regular standing army garrisons. Displayed with `[STD]` tag.
- **`adopted`**: Winner of an active procurement tender (such as the Phase 4 Fly-Off). Displayed with `[ADOPTED]` gold tag.
- **`replaced_by_player`**: Procurement canceled in favor of a player PMC dreadnought blueprint. Displayed with `[PMC-REP]` lime-green tag.
- **`replaced_by_competitor`**: Phased out on assembly lines by a rival corporation's next-generation frame. Displayed with `[CORP-REP]` orange tag.
- **`contested`**: Proprietary mercenary prototype actively competing in trials. Displayed with `[PMC]` yellow tag.
- **`phased_out`**: Retired from active frontline service to planetary militia reserves. Displayed with `[PHASED]` grey tag.

### Event-Driven Chronicle Entries
Whenever a significant event occurs, an entry is permanently appended to `dynamic_lore_chronicle`:
1. **Commissioning**: `[Cycle 1 - COMMISSION] Officially logged in system military registries with 4,820 units manufactured (3,140 active in field). Status: STANDARD_ISSUE.`
2. **Player Procurement Victory**: `[Cycle 5 - TENDER ADOPTED] Formally adopted by TERRAN COALITION as mainline doctrine! Tender won by Vanguard Linebreaker. Authorized +1,500 active units.`
3. **Obsolescence Notice**: `[Cycle 5 - OBSOLESCENCE NOTICE] Procurement canceled by TERRAN COALITION. Replaced on frontline assembly by PMC Hephaestus blueprint 'Vanguard Linebreaker [PMC Custom]'. Retooling active.`
4. **Combat Citations**: `[Cycle 8 - BATTLE CITATION] Confirmed 150 kills. Frontline survivability: 68%.`

---

## 5. GameMaker Implementation Architecture

### Singletons & System Hooks
1. **`obj_BlueprintManager`** ([`objects/obj_BlueprintManager/Create_0.gml`](file:///home/tom/GameMakerProjects/MechMakerConcept/objects/obj_BlueprintManager/Create_0.gml)):
   - Loads and registers all 100 mobile suits from `datafiles/mobile_suits/mobile_suit_catalog.json` into `unlocked_blueprints` and `all_blueprint_list`.
   - Core API:
     - `get_suit_record(_suit_id)`
     - `append_suit_dynamic_lore(_suit_id, _log_entry)`
     - `record_suit_production(_suit_id, _quantity, _reason)`
     - `record_suit_casualty(_victim_suit_id, _killer_suit_id)`
     - `record_suit_adoption(_suit_id, _faction_id, _winner_name, _is_player, _units)`
     - `record_suit_replacement(_old_suit_id, _new_suit_name, _is_player, _faction_id)`
2. **`obj_FactionManager`** ([`objects/obj_FactionManager/Create_0.gml`](file:///home/tom/GameMakerProjects/MechMakerConcept/objects/obj_FactionManager/Create_0.gml)):
   - In `award_procurement_contract(_faction_id, _mech, _trial_result)`:
     - Automatically calls `record_suit_replacement` on the incumbent baseline chassis (`GHA-07`, `AET-01`, `SCR-12`, `MUR-03`).
     - Automatically calls `record_suit_adoption` on the winning blueprint (`+1,500 units` production expansion).
3. **`obj_BattleManager`** ([`objects/obj_BattleManager/Create_0.gml`](file:///home/tom/GameMakerProjects/MechMakerConcept/objects/obj_BattleManager/Create_0.gml)):
   - In catastrophic reactor breach (`is_destroyed = true`) and squad wingman casualties:
     - Calls `obj_BlueprintManager.record_suit_casualty(_vic_chassis, _atk_chassis)`.
     - Updates casualties, active units, and confirmed kills in real time.
4. **`obj_HQTerminal`** ([`objects/obj_HQTerminal/Draw_64.gml`](file:///home/tom/GameMakerProjects/MechMakerConcept/objects/obj_HQTerminal/Draw_64.gml)):
   - **Column 1 (Chassis Browser)**: Renders colored adoption status badges (`[STD]`, `[ADOPTED]`, `[PMC-REP]`, `[CORP-REP]`, `[PHASED]`).
   - **Column 3 (Dossier Panel)**: Provides a 3-tab sub-mode navigation system:
     - **`[1. SPECS & WEAPONS]`**: Core attributes, Front Mission/Gihren's Greed telemetry, armaments, and variants.
     - **`[2. GLOBAL STATS & ATTRITION]`**: Units produced, active count, combat losses, kills, K/D ratio, visual survivability gauge, military procurement status, and operational theaters.
     - **`[3. HISTORICAL & DYNAMIC LORE]`**: Historical development dossier, manufacturing quirks, pilot slang, and the scrollable dynamic service chronicle.

---

## 6. Verification & Automated Test Coverage
All mechanics are verified by [`tools/test_mobile_suit_lore_and_global_stats.py`](file:///home/tom/GameMakerProjects/MechMakerConcept/tools/test_mobile_suit_lore_and_global_stats.py):
- 100% token balance verified across all 5 modified GML files.
- 100/100 mobile suits in `mobile_suit_catalog.json` verified for complete lore, quirks, reputation, and non-zero global stats.
- 54/54 historical timeline suits in `mobile_suits_timeline.json` verified for matching schema.
- Full combat casualty and kill mutation verified through simulation.
- Procurement tender adoption and competitor replacement lifecycle verified through simulation.
