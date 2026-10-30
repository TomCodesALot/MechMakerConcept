# DOCS 43: S-GRADE MASTERWORK QUALITY TUNING & 4 GRAND CAMPAIGN VICTORY PATHS

## 1. Overview & System Objectives
This document establishes the architecture, mathematical formulations, and UI/UX flows implemented for **Goal D**:
1. **S-Grade Masterwork Quality Tuning**: Seamless integration of prototyping laboratory minigames, assembly bay heuristics, and an interactive Auto-Tune toggle directly into custom mobile suit commission, awarding permanent chassis buffs (`+10% Power Output`, `-15% Mass`, `+1 Max AP`, `+25% OSS Pitch Score`).
2. **4 Grand Campaign Victory Paths Evaluator & Climax Modal**: Strategic turn evaluation of four distinct endgame victory conditions (**The Corporate Monopolist**, **The Supreme Warlord Hegemon**, **The Archeotech Transcendent**, **The Apex Crisis Savior**), presenting a lavish 16-bit SNES victory celebration modal accompanied by continuous, seamless endless sandbox support and career legacy integration.

---

## 2. Pillar I: S-Grade Masterwork Quality Tuning

### 2.1 The Four Masterwork Benchmarks & Auto-Tune
When assembling custom mobile suits in the Assembly Bay (`obj_HQTerminal.factory_subtab == 2`), the PMC engineering team calibrates the three core sub-assemblies:
- **Reactor Conduit Harmonics**: Frequency, amplitude, and phase alignment.
- **Limb Hydraulic Stress**: High-pressure bypass balancing and pilot response limit (*Genkai* %).
- **Thruster Plasma Resonance**: Multi-stage deuterium-tritium stoichiometric vector burn.

An airframe attains **S-Grade Masterwork** qualification if **any** of the following conditions are met:
1. **Manual Perfection**: All three bench minigames achieve S-Grade (`_r.grade == "S" && _h.grade == "S" && _t.grade == "S"`).
2. **Harmonic Synergy**: Average score across all three benches reaches $\ge 88.0\%$.
3. **Auto-Tune Calibration**: The player engages the **[AUTO-TUNE: ON]** toggle or executes **[CALIBRATE BENCH]**, rolling a success chance scaled by foundry infrastructure:
   $$\text{Chance}_{\text{Masterwork}} = 35\% + (\text{Fabrication Tier} \times 10\%) + (\text{Assembly Lines} \times 5\%)$$

### 2.2 Permanent Stat Multipliers
Upon commission, an S-Grade Masterwork chassis receives permanent intrinsic modifications:
| Specification Parameter | Standard Airframe | S-Grade Masterwork Specification | In-Game Effect |
| :--- | :--- | :--- | :--- |
| **Power Output** | Base MW | **$+10\%$ Permanent Net Surplus** | Prevents reactor throttling on heavy beam weaponry. |
| **Airframe Mass** | Base Tonnes | **$-15\%$ Permanent Weight Reduction** | Increases walking speed, boost acceleration, and agility. |
| **Action Points (AP)** | Base AP | **$+1$ Max AP & $+1$ Current AP** | Extra tactical maneuver or attack per round in combat. |
| **OSS Pitch Score** | Base Score | **$+25\%$ Composite Fly-Off Score** | Massive advantage during military procurement tender trials. |
| **Tactical Rating** | Standard Rating | **$+25\%$ Combat Score** | Escalates PMC deterrence index and contract bounties. |
| **Title & Callsign** | Standard | `[★ S-GRADE MASTERWORK ★]` | Logged in Masterwork Prototype Hall of Fame archive. |

---

## 3. Pillar II: 4 Grand Campaign Victory Paths

Campaign victory evaluates automatically at the conclusion of every strategic turn (`obj_GameManager.end_turn()`) via `evaluate_campaign_victory()`.

```mermaid
graph TD
    A[End Turn Advanced] --> B[Evaluate Campaign Victory]
    B --> C{Path 1: Monopolist?}
    C -- >= 3 MP Contracts or >= 3 Majority Corps -- --> V1[Corporate Monopolist]
    C -- No -- --> D{Path 2: Warlord?}
    D -- >= 60% Territory or 3 Theater Capitals -- --> V2[Warlord Hegemon]
    D -- No -- --> E{Path 3: Archeotech?}
    E -- 8 Divisions T5 or 30 Techs Unlocked -- --> V3[Archeotech Transcendent]
    E -- No -- --> F{Path 4: Crisis Savior?}
    F -- Era IV & Crisis Vanquished -- --> V4[Apex Crisis Savior]
    F -- No -- --> G[Standard Turn Progression]

    V1 --> H[Open Grand Victory Modal]
    V2 --> H
    V3 --> H
    V4 --> H
    H --> I[Endless Sandbox Mode]
    H --> J[Retire & View Career Dossier]
```

### 3.1 Path 1: The Corporate Monopolist
- **Requirement**: Ratify mass-production replacement contracts with $\ge 3$ superpowers (Terran Coalition, Free Colonies League, Void Syndicate, Apex Zaibatsu), OR hold majority equity ($\ge 51\%$) in $\ge 3$ rival megacorporations.
- **Narrative Theme**: Interplanetary military-industrial monopoly. All factions fire your weapons, and their treasuries sustain your sovereign corporate empire.

### 3.2 Path 2: The Supreme Warlord Hegemon
- **Requirement**: Control $\ge 60\%$ of total planetary and orbital territory across the Sol System, OR directly hold the three primary theater capitals:
  - **Earth Sphere**: `earth_granite_redoubt`, `earth_cascadia_driver`, or `earth_gibraltar_redoubt`.
  - **Space / Lunar Sphere**: `space_selene_zenith`, `space_kepler_haven`, or `space_tartarus_citadel`.
  - **Martian Sphere**: `mars_olympus_caldera`, `mars_tharsis_foundry`, or `mars_marineris_rift`.
- **Narrative Theme**: Direct military subjugation. The grand planetary fleets have surrendered, inaugurating an ironclad era of *Mercenary Pax Hegemonia*.

### 3.3 Path 3: The Archeotech Transcendent
- **Requirement**: Upgrade all 8 divisions of the Pre-War flagship *USN-X Hephaestus* to Tier 5 (`fabrication_tier`, `mining_tier`, `defense_tier`, `weapons_tier`, `propulsion_tier`, `pilot_suite_tier`, `sigint_tier`, `command_tier`), OR unlock all 30 technologies in the Hearts of Iron IV style R&D Equipment Research Tree.
- **Narrative Theme**: Technological Singularity. Awakening zero-point vacuum flux generators and instantaneous Tachyon Fold drives, elevating your PMC beyond the constraints of conventional physics.

### 3.4 Path 4: The Apex Crisis Savior
- **Requirement**: Advance into Tech Era IV (`timeline_era >= 4`, `current_turn >= 150`, or cycle year $\ge 218$) AND defeat the Apex Crisis anomaly / rogue superweapon swarm (`crisis_defeated == true` or $\ge 15$ combat sorties won).
- **Narrative Theme**: Extinction event averted. When ancient automated defenses and rogue biomechanical war engines threatened humanity's cradle, your ace vanguard held the line and vanquished the anomaly.

---

## 4. Pillar III: Victory Climax Modal UI & Endless Sandbox

### 4.1 Visual & Audio Presentation
When triggered, `obj_HQTerminal.showing_victory_modal = true` opens a dramatic full-screen 16-bit SNES celebration modal:
- **Themed Borders & Heraldry**: Golden laurels for the Monopolist, crimson warplates for the Warlord, quantum cyan circuitry for the Archeotech, and electric-blue ion shields for the Crisis Savior.
- **Historical Chronicle**: Comprehensive lore epilogue capturing the geopolitical fate of the solar system.
- **Strategic Milestone Grid**: Key statistics logging superpower contracts, territorial percentages, flagship upgrades, sorties won, and pilot aces.
- **Triumph Fanfare**: High-fidelity UI confirmation chime celebrating the historic milestone.

### 4.2 Seamless Dual Resolution
1. **[>> CONTINUE ENDLESS SANDBOX <<]**:
   - Closes modal without resetting any state.
   - Archives the campaign victory into historical records.
   - Commander maintains full operational authority to conquer remaining territory, research rival doctrine branches, or forge additional masterwork prototypes.
2. **[>> RETIRE & VIEW CAREER DOSSIER >>]**:
   - Seamlessly transitions to the *Sid Meier's Pirates*-style career retirement assessment (`retire_career()`).
   - Awards a $+2,000$ point Grand Victory Score bonus, calculates final naval grade (`RANK S: LEGENDARY OVERLORD`), and archives the career chronicle.

---

## 5. Verification & Test Suite Summary
- **Syntax & Lint Audit**: Clean `0 errors found` across all GML codebase files via `tools/validate_project.py`.
- **Exhaustive Automated Suite**: `tools/test_goal_d_exhaustive.py` verifies all mathematical formulas, stat multipliers, GML struct linkages, and UI state switches with 100% pass rate.
