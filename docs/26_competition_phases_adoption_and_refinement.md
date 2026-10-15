# 26. Mobile Suit Competitions: Multi-Phase Trials, Faction Adoption & Modernization Refinement
**Document Version:** 1.0.0  
**Roles:** Lead Game Designer (Director GDD), Lead Concept Artist, Technical Game Artist, Technical Animator, Narrative Designer, GameMaker Coder, Lead QA Engineer  
**Target Engine:** GameMaker Studio 2 (Modern GML)  
**Aesthetic Baseline:** 16-Bit Super Nintendo Military Simulation (*Front Mission SNES*, *Gihren's Greed*, *Super Robot Wars 4*)

---

## 1. Executive Vision & The Tri-Pillar Architecture

The mobile suit procurement competition system is the bridge connecting the player's **Orbital Foundry** with the **Galactic Arms Market** and their **Mercenary PMC Squad**. Rather than an instantaneous binary roll, competitions unfold as a rich, multi-tiered lifecycle across three pillars:

$$\text{Pillar I: 4-Phase Fly-Off Trials} \longrightarrow \text{Pillar II: Faction Adoption Lifecycle} \longrightarrow \text{Pillar III: Modernization Refinement Tree}$$

```
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │              TRI-PILLAR MOBILE SUIT PROCUREMENT & LIFECYCLE ARCHITECTURE               │
  └───────────────────────────────────────────┬────────────────────────────────────────────┘
                                              │
         ┌────────────────────────────────────┼────────────────────────────────────┐
         ▼                                    ▼                                    ▼
 ┌───────────────────────────────┐  ┌───────────────────────────────┐  ┌───────────────────────────────┐
 │   PILLAR I: 4-PHASE TRIALS    │  │  PILLAR II: ADOPTION PIPELINE │  │ PILLAR III: REFINEMENT BLOCKS │
 │ 1. Static Design Review       │  │ 1. Contract Ratification      │  │ • Mid-Trial Emergency Tuning  │
 │ 2. Dynamic Stress Gauntlet    │  │ 2. Orbital Shipyard Tooling   │  │ • Block I: Base Standard Issue│
 │ 3. Operational Fly-Off Duel   │  │ 3. Frontline Doctrine Rollout │  │ • Block II: Field Modernize   │
 │ 4. Final Board Ratification   │  │ 4. Royalty & Territory Yield  │  │ • Block III: Ace Custom Spec  │
 └───────────────────────────────┘  └───────────────────────────────┘  └───────────────────────────────┘
```

---

## 2. Pillar I: The 4-Phase Competition Fly-Off Tournament

Competitions do not resolve in a single split second; they are multi-stage proving tournaments where players can observe performance, react to deficits, and field-tune prototypes between phases.

### 2.1 Phase Breakdown

```
 [PHASE 1: STATIC DESIGN REVIEW] ──► [PHASE 2: DYNAMIC STRESS GAUNTLET] ──► [PHASE 3: COMBAT FLY-OFF] ──► [PHASE 4: BOARD RATIFICATION]
   • Mass vs Armor Integrity          • Kinetic Ballistics Impact Rig       • 1v1 Rival Contractor Duel      • Letter Grade (S/A/B/C/F)
   • Power Surplus / Safety           • Thermal Dissipation Burn            • PMC Combat Pedigree Bonus      • Evaluator Final Quote
   • Mid-Trial Refinement Tuning      • High-G Vacuum Vernier Shakedown     • Telemetry Demonstration        • Sign Adoption Contract
                                      • ECM / EMP Hardening Chamber
```

#### Phase 1: Static Design Review & Industrial Viability Audit
* **Evaluation Criteria:** Alloy composition, structural integrity-to-mass ratio, reactor power overhead, estimated factory fabrication cost.
* **Competitor Bids:** Rival mega-corporations (Valkyrie Heavy, Astraea Dynamics, Rustworks, Hyperion) submit bids alongside the player.
* **Evaluator Critique:** Liaison highlights identified design vulnerabilities (e.g., *"Power surplus is acceptable, but thermal dissipation in sustained fire will be marginal"*).
* **Mid-Trial Refinement Hook:** If the player identifies a weakness, they can apply an **Emergency Field Tune** before Phase 2 begins.

#### Phase 2: Dynamic Stress Gauntlet (The 4 Proving Grounds Rigs)
Simulated across four 16-bit segmented telemetry meters:
1. **Kinetic Ballistics Rig:** Fires tungsten penetrators at candidate armor plates. Tests armor value and alloy yield strength.
2. **Thermal Dissipation Chamber:** Sustains prolonged plasma burns to test heat sink conduits and coolant pump circulation.
3. **High-G Vacuum Vernier Shakedown:** Stress-tests thruster thruster mounts, inertia dampeners, and chassis g-force tolerance.
4. **ECM / EMP Hardening Chamber:** Bombards avionics with electromagnetic pulses to test sensor clarity and cyber-jamming resistance.

#### Phase 3: Operational Fly-Off & Combat Telemetry Duel
* Direct head-to-head tactical flight demonstration against the rival corporate entry (e.g., Valkyrie's *GHA-07 Ironclad-X* or Astraea's *AET-01 Helios*).
* **PMC Squad Combat Pedigree Integration:**  
  Candidate suits that have seen active combat service in the player's PMC squad unlock their **Combat-Proven Telemetry Bonus (+0 to +25 pts)**! Live flight logs from real Jovian trench battles or syndicate pirate skirmishes provide the decisive margin over sterile corporate showroom prototypes.

#### Phase 4: Procurement Board Verdict & Official Ratification
* The board renders a graded verdict:
  * **Grade S ($\ge 125$ pts):** Unanimous adoption, +30% licensing bounty bonus, +30 Faction Standing, rival contractor humiliated.
  * **Grade A ($100 - 124$ pts):** Full adoption, standard licensing bounty, +25 Faction Standing.
  * **Grade B ($85 - 99$ pts):** Conditional rejection. Faction requests Modernization Refinement before re-evaluation.
  * **Grade C/F ($< 85$ pts):** Rejection. Incumbent remains in service; rival contractor expands market share.

---

## 3. Pillar II: The Faction Adoption Lifecycle

Winning the fly-off is only the first step. The superpower military must now integrate the machine into their frontline battle order through a 4-stage lifecycle:

```
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │                         THE 4-STAGE FACTION ADOPTION LIFECYCLE                         │
  ├───────────────────────┬───────────────────────┬───────────────────┬────────────────────┤
  │ STAGE 1: RATIFICATION │ STAGE 2: TOOLING      │ STAGE 3: ROLLOUT  │ STAGE 4: MATURITY  │
  ├───────────────────────┼───────────────────────┼───────────────────┼────────────────────┤
  │ • Formal State Treaty │ • Orbital Shipyards   │ • Line Deployment │ • Perpetual Royalty│
  │ • Initial Lump Bounty │ • 2-Turn Countdown    │ • Garrison Reskin │ • Market Siphon    │
  │ • Standing Surge (+25)│ • Nanite Acceleration │ • Strength Boost  │ • Arms Paradox     │
  └───────────────────────┴───────────────────────┴───────────────────┴────────────────────┘
```

1. **Stage 1: Contract Ratification & Licensing Bounty:**  
   The player receives the upfront multi-hundred-thousand Credit bounty ($1.5M - 2.5M Cr$) and a major Faction Standing leap (+25). Geopolitical ripple effects cause competing factions to grow wary.
2. **Stage 2: Orbital Shipyard Tooling:**  
   The faction's orbital factories require 2 turns to re-tool production lines.  
   * **Foundry Acceleration Option:** The player can expend $40,000$ Cr or pre-war foundry nanites to **[EXPEDITE TOOLING]**, advancing the timeline by 1 turn.
3. **Stage 3: Frontline Doctrine Rollout:**  
   Tooling completes! The faction's military strength rating surges (+15 to +25 pts). Faction defense fleets, orbital border patrols, and tactical combat encounters now field the player's chassis.
4. **Stage 4: Fleet Maturity & Perpetual Royalties:**  
   The faction fields an expanding pool of active frontline units ($50 \rightarrow 150+$ units). Every turn, the player earns royalties ($45,000 - 85,000$ Cr/turn) based on active units in service and war intensity.
5. **The Arms Dealer Paradox:**  
   The player licenses the standard-issue production model to the faction, but retains the hand-forged **Commander Spec** for their own PMC squad. The player gains the **`Blueprint Vulnerability Exploitation`** trait (+15% Crit / +20% AP) against this chassis.

---

## 4. Pillar III: The Modernization & Refinement System

A design is never static. Refinement occurs both during competition trials and across the multi-year service life of adopted suits.

### 4.1 Mid-Trial Emergency Tuning (Tactical Refinements)
When a candidate displays a deficit during Phase 1 or Phase 2, the player can apply an **Emergency Field Tune** directly from the trial console:

| Tuning Option | Cost | Stat Modifier | Rationale |
| :--- | :--- | :--- | :--- |
| **Overclock Reactor Core** | 25,000 Cr | +15% Power, +5 Heat Risk | Increases reactor surplus for energy-heavy doctrines. |
| **Flash-Weld Armor Slabs** | 20,000 Cr | +12% Armor, -5% Speed | Bolsters kinetic stress ratings at the cost of weight. |
| **High-Flow Vernier Baffles** | 25,000 Cr | +15% Speed, -5% Armor | Enhances high-G agility for interceptor roles. |
| **Avionics Sensor Recalibration** | 30,000 Cr | +10% Combat Rating | Sharpens targeting algorithms and ECM resistance. |

### 4.2 Post-Adoption Block Modernization Tree
Once a chassis has entered frontline service, the player can develop **Block Upgrades**:

```
  [BLOCK I: BASELINE ISSUE] ──► [BLOCK II: FIELD MODERNIZATION] ──► [BLOCK III: ACE VANGUARD SPEC]
    • Initial Adopted Spec         • Unlocks after 3 Turns           • High-Tier Exotic Alloys
    • Standard Mass Production     • +15% Armor, +20% Speed          • Damascus / Tachyon Matrix
    • Standard Royalties           • +25% Royalty Yield/Turn         • Max Doctrine Combat Bonus (+30)
                                   • Modernization Bounty (+450k Cr) • Free Player PMC Commander Unit
```

* **Block I (Baseline Standard Issue):**  
  The initial model adopted during the procurement trial. Standard mass-production alloys.
* **Block II (Field Modernization):**  
  * *Requirements:* Chassis in frontline service for $\ge 3$ turns or $\ge 100$ active units deployed.  
  * *Benefits:* Fixes field maintenance reports. +15% Armor, +20% Vernier Speed, faction combat rating +4. The superpower awards a **Modernization Bounty (+450,000 Cr)** and permanent turn royalties increase by +25%!
* **Block III (Ace Vanguard Spec):**  
  * *Requirements:* Flagship Fabrication Tier $\ge 3$, Block II completed.  
  * *Benefits:* Sintered with exotic masterwork alloys (Damascus-Titanium or Tachyon Superalloy). Maxes faction doctrine combat bonus (+30), awards a **Prestige Bounty (+750,000 Cr)**, and **grants a free Legendary Commander Unit** directly into the player's PMC hangar!

---

## 5. Narrative Lore & Dialogue Scripts

```json
{
  "trial_evaluator_phases": {
    "terran_general_vance": {
      "phase_1_critique": "Your blueprint shows promise, Commander. But Valkyrie's lobbyist claims your joint actuators won't survive trench mud on Ganymede. Let's see what the stress rig says.",
      "phase_2_pass": "Hydraulic integrity held under eight thousand kilonewtons of kinetic impact. Valkyrie's Ironclad-X couldn't manage that without hairline fractures.",
      "phase_3_flyoff": "Look at that combat telemetry. Your pilot took that chassis through three live sorties and held off an entire syndicate spearhead. The data doesn't lie.",
      "phase_4_verdict_s": "Unanimous approval. The Terran Munitions Board certifies your machine as the new Coalition Standard Battle Line. Sign the treaty, Commander."
    },
    "colony_minister_takahashi": {
      "phase_1_critique": "Astraea Dynamics promises zero vernier lag on their Helios prototype. Your power output is impressive, but Colony doctrine demands unmatched agility in micro-gravity.",
      "phase_2_pass": "Thruster burn test completed with zero reactor overheating. Your heat sink configuration is undeniably superior to Astraea's offering.",
      "phase_3_flyoff": "The candidate out-accelerated Astraea's champion in the orbital slalom. Exceptional flight dynamics.",
      "phase_4_verdict_s": "The Colony Defense Council ratifies adoption immediately. Mass production begins across all Ganymede shipyards."
    }
  },
  "adoption_dialogue": {
    "tooling_started": "Orbital assembly lines have begun re-tooling. First mass-production flight wings will roll out in 2 turns.",
    "tooling_expedited": "Foundry nanite engineering teams dispatched. Shipyard re-tooling accelerated by 1 cycle!",
    "doctrine_rollout": "First production wing operational! Faction defense strength increased and frontline patrols updated.",
    "block_upgrade_unlocked": "Frontline telemetry indicates high pilot satisfaction. Military procurement board requests Block II modernization contract!"
  }
}
```

---

## 6. SNES 16-Bit Retro Art & UI Specifications

In strict adherence to 16-bit SNES tactical aesthetics (*Front Mission*, *Gihren's Greed*):

* **4-Phase Breadcrumb Tracker:**  
  4 horizontal beveled rectangular tabs at the top of the fly-off console. Current phase illuminated in bright emerald cyan (`make_color_rgb(100, 240, 255)`), past phases in muted green (`c_lime`), upcoming phases in dark gunmetal.
* **Proving Grounds Segmented LED Gauges:**  
  4 discrete 16-bit segmented meters for Kinetic Ballistics, Thermal Burn, High-G Vernier, and ECM Hardening, rendering real-time tick marks in green/amber/red.
* **Corporate Competitor Comparison Bars:**  
  4-way comparison display pitting Player Candidate against Valkyrie Heavy, Astraea Dynamics, and Hyperion Tactical.
* **Adoption Pipeline Console (Tab 2 Subtab 1):**  
  Once a doctrine is ratified, the terminal displays an authentic 16-bit **Fleet Production Dashboard**:
  * Tooling Progress countdown gauge (`2 Turns Remaining`).
  * `[EXPEDITE TOOLING]` tactile push-button.
  * Active Frontline Units counter (`120 / 120 In Service`).
  * `[UPGRADE TO BLOCK II]` & `[UPGRADE TO BLOCK III]` modernization action cards with LED indicators.
