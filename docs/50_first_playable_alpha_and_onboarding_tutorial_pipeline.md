# 50. First Playable Alpha, Tutorial Mission & Campaign Onboarding Pipeline

**Prepared by:** Lead Developer, Lead Game Designer & Lead QA Engineer  
**For:** Executive Studio Review & Milestone 50 Deployment  
**Target Engine:** GameMaker Studio 2 (Modern GML)  
**Aesthetic Core:** 16-Bit Super Nintendo / PS1 Tactical Mecha RPG (*Front Mission*, *Shin Gihren no Yabou*, *Armored Core*)

---

## 1. Executive Summary & Design Vision

Milestone 50 transforms *MechMakerConcept* from a verified headless simulation engine into a seamless, **player-facing First Playable Alpha**.

Prior to Milestone 50, a new campaign would boot directly onto an intricate 33-territory celestial war map with five sprawling command decks, leaving new commanders without context or tactical orientation. The **First Playable Alpha & Onboarding Pipeline** resolves this by implementing a guided 5-step operational cadre (**"OPERATION GROUNDWORK"**), leading the player through the four foundational pillars of PMC command:
1. **Executive Dossier Appointment:** Selecting their commander persona with gameplay traits.
2. **Metallurgical Sintering:** Sintering their first ingot of *Vanguard Composite* in the crucible.
3. **Modular CAD Assembly:** Forging their first prototype Mobile Suit (*GHA-07 Ironclad Prototype*).
4. **Strategic Logistics & Sortie:** Reviewing territory hyperlanes and launching their first tactical combat sortie.
5. **Tactical Combat Engagement:** Commanding their platoon in a 2:1 axonometric skirmish and witnessing the modular combat clash before unlocking complete strategic sandbox freedom.

---

## 2. The 5-Step Operational Onboarding Cadre

```
                     ┌────────────────────────────────────────┐
                     │ STEP 0: COMMANDER APPOINTMENT & OATH   │
                     │ (Situation Briefing & Dossier Profile) │
                     └───────────────────┬────────────────────┘
                                         │ Confirm Dossier
                                         ▼
                     ┌────────────────────────────────────────┐
                     │ STEP 1: R&D FORGE & SINTERING CRUCIBLE │
                     │ Directive: Heat & Sinter Vanguard Alloy│
                     └───────────────────┬────────────────────┘
                                         │ Sinter Ingot
                                         ▼
                     ┌────────────────────────────────────────┐
                     │ STEP 2: CAD HANGAR & PROTOTYPE ROLLOUT │
                     │ Directive: Assemble GHA-07 Ironclad    │
                     └───────────────────┬────────────────────┘
                                         │ Rollout MS
                                         ▼
                     ┌────────────────────────────────────────┐
                     │ STEP 3: WAR ROOM & LOGISTICS SORTIE    │
                     │ Directive: Inspect Sector E-02 Redoubt │
                     └───────────────────┬────────────────────┘
                                         │ Launch Sortie [S]
                                         ▼
                     ┌────────────────────────────────────────┐
                     │ STEP 4: TACTICAL COMBAT ENGAGEMENT     │
                     │ Directive: Move, Aimed Shot & Clash    │
                     └───────────────────┬────────────────────┘
                                         │ Sector Conquered
                                         ▼
                     ┌────────────────────────────────────────┐
                     │ STEP 5: PMC COMMISSION CONFIRMED       │
                     │ Full Strategic Sandbox Freedom Unlocked│
                     └────────────────────────────────────────┘
```

---

## 3. Step-by-Step Cadre Specifications

### Step 0: Commander Appointment & Solar Prologue
* **Location:** `rm_hq_terminal` (Initial Boot modal)
* **Visuals:** High-detail 16-bit background backdrops (`spr_loc_war_room`), CRT scanlines, and 3 selectable animated portraits (`spr_portrait_commander_male`, `spr_portrait_commander_female`, `spr_portrait_commander_silhouette`).
* **Directives:**
  - Page 0: Situation Briefing detailing the 4 warring factions (Terran Coalition, Outer Colonies, Rim-Syndicate, Apex Zaibatsu).
  - Page 1: Select Commander profile with passive doctrine perks:
    - **Commander Alexei Kane (`male`):** Heavy Vanguard (+12% Kinetic Armor, +10% Contract Bounty).
    - **Commander Morgan Vance (`female`):** Vernier Synthesis (+15% Prototyping Stability, +10% Thruster Evasion).
    - **Classified Shadow (`silhouette`):** Black Ops Logistics (+10% Scrap Salvage, Volatility Dampening).
* **Completion Event:** Advances to `tutorial_step = 1`, unlocks R&D Forge deck.

---

### Step 1: Metallurgical Crucible Sintering
* **Location:** `rm_hq_terminal` $ightarrow$ Deck `[3] R&D FORGE` (`active_tab = 0`, `rd_subtab = 0`).
* **UI Highlight:** Pulsing amber bracket on Tab `[3]` and over the Crucible Thermal controls.
* **Cadre Transmission:**
  > `[CADRE COMMS] "Welcome to the R&D Crucible, Commander. Before fielding war machines, we must forge alloy plating. Press [HEAT] to bring crucible temperature above 1,500°C, then click [SINTER VANGUARD COMPOSITE]."`
* **Completion Event:** When `sinter_alloy()` succeeds or `crucible_sinter()` is triggered:
  - Grants $+5$ Ingots of *Vanguard Composite*.
  - Plays `snd_discovery_fanfare`.
  - Advances to `tutorial_step = 2`.

---

### Step 2: CAD Hangar & Prototype Rollout
* **Location:** `rm_hq_terminal` $ightarrow$ Deck `[2] HANGAR` (`active_tab = 1`, `factory_subtab = 1`).
* **UI Highlight:** Pulsing amber bracket on Tab `[2]` and over the `[ASSEMBLE PROTOTYPE]` button.
* **Cadre Transmission:**
  > `[CADRE COMMS] "Alloy stock verified. Enter the Modular Assembly Bay. Configure your Biped Chassis with heavy armor plating and 120mm Autocannon, then authorize prototype rollout."`
* **Completion Event:** When `prototype_mobile_suit()` is clicked:
  - Adds player custom prototype *GHA-07 Ironclad Custom* to the active hangar lineup.
  - Grants $+1,000$ Credits commissioning bonus.
  - Plays `snd_ui_stamp` and `snd_hydraulic_press`.
  - Advances to `tutorial_step = 3`.

---

### Step 3: War Room Logistics & Contested Border Sortie
* **Location:** `rm_hq_terminal` $ightarrow$ Deck `[1] WAR MAP` (`active_tab = 3`, `war_subtab = 0`).
* **UI Highlight:** Pulsing amber bracket on Tab `[1]`, Earth Sphere Sector `E-02 (Granite Redoubt)`, and the `[⚔️ SORTIE]` button.
* **Cadre Transmission:**
  > `[CADRE COMMS] "Hostile Syndicate recon units detected at Earth Sector E-02 (Granite Redoubt). Our logistics lines are threatened. Deploy Alpha Platoon to the tactical battlefield!"`
* **Completion Event:** Clicking `[⚔️ SORTIE]` or Sector E-02 transitions room to `rm_combat`, setting `tutorial_step = 4`.

---

### Step 4: Tactical Combat Engagement & First Blood
* **Location:** `rm_combat` (`obj_BattleManager`).
* **Tactical Overlay:** Top diegetic guidance bar:
  > `★ CADRE TACTICAL INSTRUCTION: Left-Click Alpha-01 -> Left-Click Cyan Grid Tile to Move -> Click [ATTACK] -> Select Aimed Limb Shot!`
* **Combat Invariants:**
  - Player executes an attack on the hostile target.
  - Dynamic Combat Clash (Doc 49) triggers: weapon recoil, shell ejections, and modular damage.
  - Hostile unit destroyed.
* **Completion Event:** Upon tactical victory, returning to `rm_hq_terminal` sets `tutorial_step = 5`.

---

### Step 5: Commission Confirmed & Strategic Sandbox Handoff
* **Location:** `rm_hq_terminal`.
* **Ceremony Banner:**
  > `★ CADRE COMMISSION COMPLETE // PROMOTION TO FULL MERCENARY COMMANDER ★`  
  > `All 5 Command Decks, 33 celestial territories, corporate stock market, and dreadnought transit are now unrestricted.`
* **State Updates:**
  - `has_completed_tutorial = true;`
  - `tutorial_active = false;`
  - Persistent game save triggered.

---

## 4. Universal Ergonomic Deck Architecture

To align with modern ergonomic play and standard numpad navigation, the five primary command decks are arranged strictly left-to-right matching Quick-Keys `[1]` through `[5]`:

| Quick-Key | Deck Name | Internal `active_tab` | Primary Purpose |
| :---: | :--- | :---: | :--- |
| **`[1]`** | **🗺️ WAR MAP** | `3` | 33-Territory 3-Theater hex wargame, hyperlanes, sorties. |
| **`[2]`** | **🏭 HANGAR** | `1` | CAD modular assembly, masterwork tuning, Block II upgrades. |
| **`[3]`** | **🔬 R&D FORGE** | `0` | Metallurgy sintering crucible, equipment tech tree, blueprints. |
| **`[4]`** | **📜 CONTRACTS** | `2` | Faction flyoffs, corporate stock market, base detention brig. |
| **`[5]`** | **🚀 FLEET** | `4` | Flagship *USN-X Hephaestus* upgrades, transit jump, corporate dossiers. |

---

## 5. Verification & QA Matrix

* **Schema Validation:** Verified via `tools/validate_project.py`.
* **State Machine Assertions:** `tools/test_onboarding_tutorial_pipeline.py` testing:
  - Step transitions ($0 ightarrow 1 ightarrow 2 ightarrow 3 ightarrow 4 ightarrow 5$).
  - Quick-key deck routing (`[1]` through `[5]`).
  - Skip tutorial bypass (`[ESC] SKIP TUTORIAL`).
  - Save/Load serialization preserving `tutorial_step` and `has_completed_tutorial`.
