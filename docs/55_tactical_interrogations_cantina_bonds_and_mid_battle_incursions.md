# Document 55: Tactical Interrogations, Cantina Bonds & Mid-Battle Incursions Engine
**Milestone 55: Interactive Base Brig POW Triage, Crew Cantina Bonding Vignettes, Dynamic Mid-Combat Radio Directives & PMC Karma Alignment**

---

## 1. Executive Summary & Design Scope

Milestone 55 synthesizes the narrative roleplaying systems, visual novel cutscenes, and tactical combat gameplay into a unified, high-stakes ecosystem. Building upon the Visual Novel Engine (Docs 51-54), Milestone 55 introduces:

1. **Base Brig Interrogations & Defection Cutscenes (`ep_brig_interrogation_ace`)**:
   - When enemy pilots eject in combat and are captured into the Flagship Detention Brig, the player can initiate an interactive 1-on-1 interrogation cutscene.
   - 4-Tier Emotion Rendering (`ANGRY` ideological defiance, `DESPERATE` fear of tribunal, `SMUG` fanaticism, `NORMAL` weary resignation).
   - Branching decision paths:
     - **Ideological Conversion / Mercenary Commission**: Offer an upfront bonus and cabin to convert the POW into an active ace pilot in your roster.
     - **Coerced Blueprint Telemetry**: Extract proprietary mobile suit schematics and engineering insights (+15 Tech Insight / Rare Blueprint Specs).
     - **Diplomatic Prisoner Exchange**: Ransom the officer back to their home government (+45,000 Credits, +15 Faction Standing).

2. **Flagship Cantina Banter & Crew Bond Vignettes (`ep_cantina_bond_*`)**:
   - Interactive crew vignettes in the **Mercenary Cantina Registry** (Pilots Deck, Subtab 1) between sorties.
   - **Crew Vignettes**:
     - **Lt. Gregory Vance (`ep_cantina_bond_vance`)**: Grappling with fighting former Terran Coalition comrades. Unlocks the *"Brothers in Arms"* perk (+5% Tandem Volley Accuracy).
     - **Dr. Anika Soren (`ep_cantina_bond_soren`)**: Discussing neuro-trauma and cockpit cybernetic link decay. Unlocks *"Combat Triage Protocol"* (-25% Convalescence Recovery time).
     - **Chief Marcus Kovacs (`ep_cantina_bond_kovacs`)**: Detailing experimental crucible flux quenching. Unlocks *"Overclocked Actuators"* (+1 Unit AP on Turn 1 of combat).

3. **Mid-Battle Scripted Tactical Story Events & Radio Directives in `rm_combat`**:
   - At Turn 3 of combat, or when an enemy Ace drops below 40% HP, the battle halts for a **Mid-Battle Tactical Radio Incursion**.
   - Displays a live radio intercom hail from the enemy commander or rival mercenary reinforcement drop-pod.
   - Provides 3 real-time **Tactical Radio Command Directives**:
     - `[DIRECTIVE: ORBITAL KINETIC BARRAGE]`: Call in flagship heavy kinetic artillery (deals 35 damage to target tile + screen shake).
     - `[DIRECTIVE: SQUADRON FOCUS FIRE]`: Broadcast synchronized target telemetry (+15% Accuracy and +1 AP to all allied mechs for 1 turn).
     - `[DIRECTIVE: ELECTRONIC TAUNT & JAMMING]`: Broadcast neuro-jamming signal (target enemy suffers -20% Evasion and -2 AP).

4. **PMC Ideological Karma & Alignment Engine**:
   - Dynamic alignment tracking across 3 distinct mercenary paths:
     - **Noble Peacekeeper**: Honoring armistices, rescuing ejection pods, and defending civilian transports.
     - **Corporate Pragmatist**: Maximizing contract bids, patent licensing, stock buyouts, and technological extraction.
     - **Bloodhound War Profiteer**: Sabotaging peace treaties, double-dealing munitions, and executing black-market shakedowns.
   - Displayed diegetically on the persistent Top Command Bar in `obj_HQTerminal`.

---

## 2. Technical Architecture & GML Implementation

### 1. Visual Novel Engine Upgrades (`scr_vn_engine.gml`):
- Added episodes:
  - `ep_brig_interrogation_ace`
  - `ep_cantina_bond_vance`
  - `ep_cantina_bond_soren`
  - `ep_cantina_bond_kovacs`
- Upgraded `scr_vn_draw_combat_intercom()` to support interactive `directives` (array of clickable choice buttons with real-time combat execution callbacks).

### 2. Tactical Combat Integration (`obj_BattleManager`):
- Added `mid_battle_incursion_triggered = false` and `mid_battle_incursion_turn = 3`.
- In `Step_0.gml`: When `turn_number == 3 && state == COMBAT_STATE.PLAYER_PHASE && !mid_battle_incursion_triggered`, triggers `trigger_mid_battle_tactical_incursion()`.
- Wired real-time directive callbacks modifying combat state:
  - Flagship Orbital Strike: creates visual explosion, shakes camera, damages enemy unit.
  - Squadron Focus: buffs allied accuracy and AP.
  - Electronic Taunt: applies evasion and AP penalty to target enemy.

### 3. Pilots Command Deck Enhancements (`obj_HQTerminal/Draw_64.gml`):
- **Cantina Registry (Subtab 1)**: Added `[CREW BOND VIGNETTES]` command card with interactive talk buttons for Vance, Soren, and Kovacs.
- **Medical Bay & POW Detention Wing (Subtab 2)**: Added the `[BASE BRIG & POW DETENTION WING]` section with live dossiers and interactive `[INTERROGATE // CONVERSION CUTSCENE]` buttons.
- **Top Command Bar**: Added the `[PMC ALIGNMENT]` diegetic status badge.

---

## 3. Verification Standards
- Zero syntax errors in `python3 tools/validate_project.py`.
- 100% test pass in `tools/test_milestone_55_bonds_interrogations_and_incursions.py`.
- Full regression-free integration with Milestone 51, 52, 53, 54, Onboarding, and UI test suites.
