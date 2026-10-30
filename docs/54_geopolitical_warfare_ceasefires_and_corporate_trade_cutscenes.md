# Document 54: Geopolitical Warfare, Ceasefires & Corporate Trade Cutscenes Engine
**Milestone 54: High-Stakes Player Dialogue Interactions, Inter-Faction War Declarations, Brokered Armistices & Rival Corporate Trade Interceptions**

---

## 1. Executive Summary & Design Scope

Milestone 54 expands the narrative and tactical roleplaying core of the Mobile Suit PMC Simulation. Building upon the 16-Bit Retro Visual Novel Engine (Doc 51), Reactive Geopolitical Dialogue Architecture (Doc 52), and Dramatis Personae Dossiers (Doc 53), Milestone 54 delivers comprehensive, high-stakes interactive dialogue cutscenes for four critical geopolitical moments:

1. **Inter-Faction War Declarations (`WAR_DECLARATION`)**:
   - Dual-Speaker confrontations between rival faction leaders when bilateral hostility reaches boiling point (Tension >= 85) or script-driven casus belli triggers.
   - The player's PMC is summoned as the operational kingmaker: commit vanguard mobile suits to one side, play both sides as a cynical war profiteer, or enforce a demilitarized buffer zone.

2. **Ceasefire & Armistice Negotiations (`CEASEFIRE_ARMISTICE`)**:
   - High-tension diplomatic summits where exhausted belligerents negotiate treaty boundaries, demilitarized zones, and weapon inspection regimes.
   - The player can act as the **Guarantor of Peace** (earning recurring peacekeeping subsidies and diplomatic trust), extract territorial mining concessions, or secretly **Sabotage the Accord** with false-flag black-ops to keep weapons manufacturing demand soaring.

3. **Direct Strategic Trade Delegations with the Player (`PLAYER_TRADE`)**:
   - Faction trade envoys and procurement liaisons boarding the player's flagship with urgent military orders for bulk alloys, masterwork components, and emergency frame deliveries.
   - Features negotiation trees: standard order fulfillment, aggressive price-gouging counter-offers, or seizing illicit contraband.

4. **Rival Megacorporation Corporate Trade Interceptions (`RIVAL_TRADE_INTERCEPT`)**:
   - Espionage alerts revealing that rival arms manufacturers (**Valkyrie Heavy Industries**, **Hyperion Tactical**, **Astraea Orbital Dynamics**, **Rustworks Cartel**) are finalizing exclusive mega-deals with superpowers.
   - The player can **Undercut the Rival** with superior mobile suit specifications and aggressive pricing, execute a **Black-Ops Cargo Ambush** to incinerate rival prototypes, or exploit **Insider Stock Buyouts** to reap massive capital gains.

---

## 2. Dramatis Personae & Faction Alignment Matrix

### Primary Belligerents & Trade Delegates:
* **General Arthur Bradley** (Terran Coalition): Unyielding militarist, defends Earth's industrial supremacy. Demands heavy armor and ballistic kinetic ordnance.
* **Commander Joshua Reed** (Outer Colony League): Desperate freedom fighter, relies on high-mobility lightweight titanium frames and swarm rocket platforms.
* **Captain Sonya Cruz** (Rogue Mercenary Syndicates): Privateer queen, controls black-market tritium shipping lanes and salvage bazaars in the Asteroid Belt.
* **Director Kenjiro Sato** (Apex Bio-Cybernetics Zaibatsu): Calculating oligarch, develops wetware cybernetic neural interfaces and high-frequency energy blades.
* **Archon Orin Sideris** (Sidereal Sovereign League): Aristocratic oligarch, dominates rare Jovian gas extraction and advanced beam weaponry.
* **Consensus Node 0-Prime** (Tharsis Machine Consensus): Subterranean Martian AI, seeks pre-war technological crypts and calculating mathematical supremacy.
* **CEO Victoria Sterling** (Valkyrie Heavy Industries): The player's foremost corporate rival; aggressive Terran military contractor known for bulky, high-armor siege suits.
* **Director Douglas Vance** (Hyperion Tactical): Ruthless cybernetic weapons manufacturer; black-market drone supplier to Martian insurgents.

---

## 3. The Four Dialogue & Cutscene Suites

### Suite A: Inter-Faction War Declarations

#### Scene A.1: The Fall of Phobos // Solar War Ignited (`ep_war_terran_vs_colony`)
* **Trigger Conditions**: Terran-Colony Bilateral Tension >= 85, or Turn 9 Campaign Escalation, or `declare_war("rel_tc", ...)`.
* **Visual Presentation**: `DUAL` Layout.
  - Left: General Arthur Bradley (`spr_portrait_commander_male`) [ANGRY / BELLIGERENT, Crimson Bezel]
  - Right: Commander Joshua Reed (`spr_portrait_commander_female`) [ANGRY / BELLIGERENT, Crimson Bezel]
  - Background: `spr_loc_war_room`
* **Narrative Context**: A Colony freighter was vaporized by Terran orbital batteries over Phobos; Colony rocket silos on Deimos retaliated by bombarding the Terran Cascadia orbital station.
* **Branching Decisions & Consequences**:
  1. `[COMMIT TO TERRA // PLEDGE VANGUARD]`:
     - *Dialogue*: "Iron Ridge pledges its full armored division to the Coalition flag. We will purge the Deimos missile batteries."
     - *Impact*: `+25 Terran Standing`, `-30 Colony Standing`, `+85,000 Credits`, `Unlocks Heavy Siege Cannon Tech`.
  2. `[DEFEND COLONIES // SHIELD OF SPACENOIDS]`:
     - *Dialogue*: "Terran orbital tyranny ends today. Iron Ridge mobile suits will screen the evacuation convoys."
     - *Impact*: `+25 Colony Standing`, `-30 Terran Standing`, `+75,000 Credits`, `+20 Titanium`, `Unlocks Vernier Drift Tech`.
  3. `[ARMS DEALER PARADOX // DOUBLE CONTRACT]`:
     - *Dialogue*: "War is an alloy, gentlemen. We will sell kinetic munitions to Terra and thruster packs to the Colonies at 250% market rates."
     - *Impact*: `-15 Terran Standing`, `-15 Colony Standing`, `+160,000 Credits`, `+15 Tungsten`, `+15 Titanium`.
  4. `[ENFORCE BUFFER ZONE // ARMED NEUTRALITY]`:
     - *Dialogue*: "Any warframe entering neutral shipping corridors will be fired upon by Iron Ridge railguns. Stand down."
     - *Impact*: `+10 Terran`, `+10 Colony`, `+25 Pilot Morale`, `Stabilizes Tension at 60`.

---

#### Scene A.2: The Silicon Crusade // Cybernetic Schism (`ep_war_zaibatsu_vs_tharsis`)
* **Trigger Conditions**: Zaibatsu-Tharsis Tension >= 85, or Turn 14, or researching Cybernetic Crypt Decryption.
* **Visual Presentation**: `DUAL` Layout.
  - Left: Director Kenjiro Sato (`spr_portrait_commander_male`) [SMUG / CALCULATING, Gold Bezel]
  - Right: Consensus Node 0-Prime (`spr_portrait_commander_female`) [ANGRY / COMBAT ALERT, Crimson Bezel]
* **Narrative Context**: Zaibatsu net-divers hacked the Arsia Mons server crypt, stealing pre-war automated consciousness algorithms. Node 0-Prime mobilized cyber-assault drones to exterminate corporate facilities across Mars.
* **Branching Decisions & Consequences**:
  1. `[SPONSOR SATO // BIO-SYNTHETIC PATENT]`:
     - *Impact*: `+25 Zaibatsu`, `-30 Tharsis`, `+100,000 Credits`, `+15 Syn-Flux`, `Unlocks Bio-Neural Frame Mod`.
  2. `[DEFEND THE CRYPT // ARCHIVE PURITY]`:
     - *Impact*: `+25 Tharsis`, `-30 Zaibatsu`, `+90,000 Credits`, `+25 Tungsten`, `Unlocks Quantum Fire Control (+12% ACC)`.
  3. `[BLACK-MARKET DATA HARVEST // SELL CRYPT KEYS]`:
     - *Impact*: `-15 Zaibatsu`, `-15 Tharsis`, `+180,000 Credits`, `Triggers Corporate Nemesis Incursion`.

---

#### Scene A.3: The Jovian Privateer War // Asteroid Tithe (`ep_war_syndicate_vs_sidereal`)
* **Trigger Conditions**: Syndicate-Sidereal Tension >= 85, or Turn 19, or Jovian Convoy Raid.
* **Visual Presentation**: `DUAL` Layout.
  - Left: Captain Sonya Cruz (`spr_portrait_commander_female`) [SMUG / PREDATORY, Gold Bezel]
  - Right: Archon Orin Sideris (`spr_portrait_commander_male`) [ANGRY / ARISTOCRATIC FURY, Crimson Bezel]
* **Narrative Context**: Syndicate corsairs captured a royal Sidereal helium galleon in the Trojan asteroids, taking 200 noble hostages.
* **Branching Decisions & Consequences**:
  1. `[CORSAIR'S CUT // ESCORT HIJACKED CARGO]`:
     - *Impact*: `+25 Syndicate`, `-30 Sidereal`, `+50 Tritium`, `+70,000 Credits`.
  2. `[NOBLE RETRIBUTION // STRIKE PIRATE FLOTILLA]`:
     - *Impact*: `+25 Sidereal`, `-30 Syndicate`, `+35 Tungsten`, `+85,000 Credits`, `Unlocks Astral Beam Shield Tech`.
  3. `[IMPOUND AS EVIDENCE // MERCENARY TOLL]`:
     - *Impact*: `+10 Syndicate`, `-10 Sidereal`, `+120,000 Credits`, `+25 Tritium`.

---

### Suite B: Ceasefire & Armistice Negotiations

#### Scene B.1: The Geneva Concordat // Mars Armistice (`ep_ceasefire_terran_colony`)
* **Trigger Conditions**: Faction War Duration >= 10 Turns, or Player executes `player_broker_ceasefire("rel_tc")`.
* **Visual Presentation**: `DUAL` Layout.
  - Left: General Arthur Bradley [DESPERATE / RESOLUTE, Amber Bezel]
  - Right: Commander Joshua Reed [DESPERATE / RESOLUTE, Amber Bezel]
* **Narrative Context**: Over 40,000 casualties and depleted titanium stockpiles have brought both armies to operational paralysis.
* **Branching Decisions & Consequences**:
  1. `[GUARANTOR OF PEACE // RATIFY ARMISTICE]`:
     - *Dialogue*: "Iron Ridge countersigns the treaty as military guarantor. We will patrol the Phobos Line."
     - *Impact*: `War Halted for 18 Turns`, `+15 Terran`, `+15 Colony`, `+120,000 Credits Peacekeeping Bounty`.
  2. `[SABOTAGE ACCORD // THE MERCHANT OF DEATH]`:
     - *Dialogue*: (Secret Directive to Voss) "Detonate an unregistered micro-fusion mine near Reed's flagship. Make it look like Coalition artillery."
     - *Impact*: `War Reignites Immediately`, `+40% Munitions Market Inflation`, `+200,000 Credits Weapon Sales`, `-15 Moral Karma`.
  3. `[DEMILITARIZED EXTRACTION CONCESSION]`:
     - *Dialogue*: "We will enforce your truce on one condition: Iron Ridge receives exclusive mineral leasing for the Syrtis Major Basin."
     - *Impact*: `+40 Titanium`, `+30 Tungsten`, `+10 Terran`, `+10 Colony`.

---

#### Scene B.2: The Arsia Mons Data Partition (`ep_ceasefire_zaibatsu_tharsis`)
* **Trigger Conditions**: Zaibatsu-Tharsis War Duration >= 8 Turns, or `player_broker_ceasefire("rel_cz")`.
* **Visual Presentation**: `DUAL` Layout.
  - Left: Director Kenjiro Sato [CALCULATING / WEARY]
  - Right: Consensus Node 0-Prime [RESOLUTE / DATA LOSS]
* **Branching Decisions & Consequences**:
  1. `[RATIFY PARTITION]`: +15 Zaibatsu, +15 Tharsis, +95,000 Credits, 14-turn truce.
  2. `[TECH TOLL EXTRACTION]`: Demand 20 Syn-Flux and pre-war schematics to arbitrate.

---

### Suite C: Direct Strategic Trading with the Player

#### Scene C.1: Strategic Ordnance Procurement Envoy (`ep_trade_terran_delegation`)
* **Trigger Conditions**: Click `[HAIL TRADE ENVOY]` in Contracts Deck (Page 3, Subtab 2), or Terran Standing > 20.
* **Visual Presentation**: `SOLO` Layout.
  - Speaker: General Arthur Bradley / Coalition Logistics Attaché (`spr_portrait_commander_male`) [NORMAL / RESOLUTE]
* **Narrative Context**: Coalition frontline divisions require an emergency shipment of 50 Refined Tungsten or high-mass armor plates to reinforce the Valles Marineris line.
* **Branching Decisions & Consequences**:
  1. `[FULFILL EMERGENCY PROCUREMENT]`: Deliver 35x Tungsten. `+150,000 Credits`, `+15 Terran Standing`, `Unlocks Heavy Armor Plating B2`.
  2. `[AGGRESSIVE COUNTER-OFFER // PRICE GOUGE]`: Demand 225,000 Credits due to "active combat hazard in delivery theater." `+225,000 Credits`, `+5 Terran Standing`, `-5 Trust`.
  3. `[RESERVE STRATEGIC STOCKPILE]`: Politely decline to protect internal PMC manufacturing lines.

---

#### Scene C.2: The Jovian Smuggler's Vault (`ep_trade_syndicate_black_market`)
* **Trigger Conditions**: Click `[HAIL BLACK-MARKET VAULT]` in Commodity Trade Exchange, or Syndicate Standing > 10.
* **Visual Presentation**: `SOLO` Layout.
  - Speaker: Captain Sonya Cruz (`spr_portrait_commander_female`) [SMUG / PREDATORY]
* **Narrative Context**: Cruz's privateers intercepted a covert navy transport carrying rare pre-war weapons tech and military tritium.
* **Branching Decisions & Consequences**:
  1. `[PURCHASE SMUGGLER'S CACHE]`: Pay 80,000 Credits. `+40 Tritium`, `+15 Syn-Flux`, `Unlocks Prototype Plasma Blade`.
  2. `[GUNBOAT SHAKEDOWN // SEIZE CONTRABAND]`: Train flagship cannons on Cruz's blockade runner. Free `+25 Tritium`, `-20 Syndicate Standing`, `+10 Pilot Notoriety`.
  3. `[DECLINE PRIVATELY]`: Maintain discretion.

---

### Suite D: Rival Corporate Espionage & Trade Interceptions

#### Scene D.1: Valkyrie Heavy Mega-Contract Undercut (`ep_trade_rival_valkyrie_deal`)
* **Trigger Conditions**: Flagship Deck (Page 5, Subtab 2) -> Click `[INTERCEPT RIVAL CONTRACT]`, or Turn 11.
* **Visual Presentation**: `DUAL` Layout.
  - Left: Intelligence Officer Kaelen Voss (`spr_portrait_commander_male`) [ALARMED / URGENT]
  - Right: CEO Victoria Sterling / Valkyrie Rep (`spr_portrait_commander_female`) [SMUG / CORPORATE ARROGANCE]
* **Narrative Context**: **Valkyrie Heavy Industries** is hours away from locking in a 500,000 Credit exclusive mass-production contract with the Terran Defense Ministry, threatening to crush the player's market share by -12%.
* **Branching Decisions & Consequences**:
  1. `[UNDERCUT RIVAL SPECIFICATIONS]`:
     - *Dialogue*: "Present our Ironclad S-Tier trial telemetry directly to the procurement committee. Slash our delivery margin by 15%."
     - *Impact*: `Snatches Contract! +180,000 Credits`, `+10% Sol Market Share`, `Valkyrie Share Price Falls -18%`, `+15 Valkyrie Hostility`.
  2. `[BLACK-OPS CONVOY AMBUSH]`:
     - *Dialogue*: "Deploy an unmarked stealth squad to derail Valkyrie's prototype convoy in transit. Make it look like Syndicate pirates."
     - *Impact*: `Valkyrie Shipment Obliterated`, `Contract Defaults to Player (+110,000 Cr)`, `+30 Valkyrie Hostility (Triggers Ace Nemesis Duel)`.
  3. `[INSIDER STOCK TRADING BUYOUT]`:
     - *Dialogue*: "Don't stop the deal—exploit it! Buy 25,000 Valkyrie shares immediately, then sell the peak after ratification."
     - *Impact*: `+145,000 Credits Stock Dividend Profit`, `+25,000 Valkyrie Corporate Equity`.

---

#### Scene D.2: Hyperion Tactical's Martian Monopoly (`ep_trade_rival_hyperion_arms`)
* **Trigger Conditions**: Flagship Deck -> Hyperion Card -> `[INTERCEPT DEAL]`, or Turn 16.
* **Visual Presentation**: `DUAL` Layout.
  - Left: Chief Logistics Officer Marcus Kovacs (`spr_portrait_commander_male`) [ANGRY]
  - Right: Director Douglas Vance (`spr_portrait_commander_male`) [SMUG]
* **Narrative Context**: Hyperion Tactical is illegally supplying automated cybernetic combat frames to rebel factions on Mars, bypassing Solar Council embargoes.
* **Branching Decisions & Consequences**:
  1. `[EXPOSE TO SOLAR COUNCIL]`: Leak encrypted supply manifests. `Hyperion hit with 250,000 Cr regulatory fine`, `Hyperion Market Share drops -10%`, `+20 Solar Council Rep`.
  2. `[INTERCEPT & SALVAGE TRANSPORT]`: Intercept shipment in Martian orbit. `+30 Titanium`, `+20 Syn-Flux`, `+80,000 Credits Salvage Bounty`.
  3. `[BLACKMAIL FOR JOINT TENDER]`: Force Hyperion into a joint production agreement. `+60,000 Credits Royalty / Turn for 5 Turns`.

---

## 4. Technical Architecture & GML Implementation

### Engine Registration in `scr_vn_engine.gml`:
All episodes are registered within `global.vn_state.episodes[$ "..."]` using standard nodes, dual-portrait presentation, 4-tier emotions (`NORMAL`, `ANGRY`, `DESPERATE`, `SMUG`), and callable action closures modifying:
- `obj_FactionManager.modify_standing(faction_id, amount)`
- `obj_FactionManager.declare_war(pair_id, casus_belli)`
- `obj_FactionManager.broker_truce(pair_id, duration, reason)`
- `obj_GameManager.add_funds(amount)`
- `obj_GameManager.add_raw_material(material_id, amount)`
- `obj_GameManager.rival_corporations` (hostility, share price, market share)

### UI Interaction Bridges:
- `obj_HQTerminal/Draw_64.gml`:
  - **Contracts Deck (Page 3, Subtab 2)**: Added `[HAIL TRADE ENVOY]` button triggering `ep_trade_terran_delegation` or `ep_trade_syndicate_black_market`.
  - **Flagship Deck (Page 5, Subtab 2)**: Added `[INTERCEPT RIVAL DEAL]` button on rival corporate cards triggering `ep_trade_rival_valkyrie_deal` and `ep_trade_rival_hyperion_arms`.
- `obj_FactionManager/Create_0.gml`:
  - Hooked `declare_war` and `broker_truce` to automatically dispatch corresponding cutscenes when diplomatic state changes.

---

## 5. Verification & QA Standards
- All 8 new cutscenes registered in `scr_vn_engine.gml`.
- All choices contain validated executable actions and mathematical impact labels.
- Dual-speaker layout validated with contrasting emotional bezels.
- Zero memory leaks, zero unresolved variables, passing 100% in `tools/validate_project.py` and dedicated test suite `tools/test_milestone_54_war_ceasefire_and_trade_cutscenes.py`.
