# Document 20: Mech Building Minigames, Comprehensive Combat Stats & Gihren's Greed / Front Mission Hybrid Specification

## 1. Executive Summary & Lead Dev Status Report

### 1.1 Status Query Response: "Has This Been Started, Lead Dev?"
**Yes, the foundational architecture was initiated, but it required this comprehensive overhaul to achieve full operational depth:**

1. **What Was Previously In Place**:
   - The primary physical concepts for three R&D prototyping minigames existed in `obj_HQTerminal`:
     * *Reactor Conduit Sine Wave Tuning* (turn-based frequency oscillator).
     * *Limb Hydraulic Stress Alignment* (pulse-budget joint stress balancing).
     * *Thruster Plasma Flow Calibration* (multi-stage magnetic resonance throttle).
   - Base masterwork struct creation existed (`obj_BlueprintManager.add_masterwork()`).
   - 21 canonical blueprints existed across 4 factions, modeling 6-part Front Mission hit locations.
   - Initial modal frames for tutorials existed in `obj_HQTerminal`.

2. **What Was Missing & Is Completed in This Update**:
   - **Continuous Performance-to-Capability Pipeline**: Previously, minigames only granted a binary "Masterwork" item if performance was $\ge 90\%$. There was no granular scaling where a 98% run produces an *S-Rank Prototype Ace* while a 60% run yields a *C-Rank Stuttering Chassis* with distinct performance drawbacks.
   - **Gihren's Greed (Gihren no Yabou) Comprehensive Tactical Stats**:
     * **Pilot Reaction Limit % (限界 - Genkai)**: The classic Gihren's Greed mechanic where a mobile suit's hydraulic and neural response speed bottlenecks an Ace pilot's reflexes.
     * **Propellant / Fuel Capacity & Operational Range (EN / 推進剤)**.
     * **Terrain Adaptability Ratings (地形適性)**: Ground, Space, Urban, Trench (S/A/B/C/D).
     * **Prometheus Flux / ECM Particle Dispersion % (散布率 / 索敵)**: Electronic counter-measures and radar scattering.
   - **Front Mission Modular Stat Depth**:
     * Power-to-Weight ratios, Surplus MW acceleration bonuses, discrete part armor/structure HP, and recoil dissipation percentages.
   - **Direct Tuning Integration**:
     * Minigame results can now be directly baked into custom mobile suits forged in the Assembly Bay, modifying their in-combat performance on the isometric battlefield.
   - **Interactive In-Engine Step-by-Step Tutorials**:
     * Comprehensive tutorials explaining mechanics, optimal calibration math, and win/loss thresholds.

---

## 2. Gihren's Greed & Front Mission Hybrid Stat Architecture

Every mobile suit in *MechMakerConcept* possesses a unified stat matrix blending **Front Mission modular part damage** with **Gihren's Greed operational parameters**.

```
┌────────────────────────────────────────────────────────────────────────┐
│               MOBILE SUIT COMPREHENSIVE COMBAT STAT SHEET              │
├────────────────────────────────────────────────────────────────────────┤
│ 1. FRONT MISSION MODULAR INTEGRITY (Part-by-Part HP & Armor):          │
│    • Torso Core (Reactor / Power Plant)                                │
│    • Head Unit (Sensors & Target Lock)                                 │
│    • Left Weapon Arm (Direct Fire Mount)                               │
│    • Right Weapon Arm (Rapid / Heavy Mount)                            │
│    • Hydraulic Legs (Bipedal / Quad Locomotion & AP)                   │
│    • Vernier Backpack (Auxiliary Booster & Missiles)                   │
│                                                                        │
│ 2. GIHREN'S GREED OPERATIONAL PARAMETERS (Gihren no Yabou):           │
│    • Pilot Reaction Limit % (限界 - Genkai): 100% to 220%              │
│    • Propellant / Fuel Max (EN - 推進剤): 80 to 250 Units               │
│    • Terrain Adaptability Matrix (地形適性): Ground, Space, Urban, Trench │
│    • Prometheus Flux / ECM Dispersion (散布率): 10% to 75%                    │
│    • Sensor Search Grade (索敵): S, A, B, C, D                         │
│                                                                        │
│ 3. THERMODYNAMICS & POWER DYNAMICS:                                    │
│    • Reactor Output (MW) vs Total Power Drain (MW) = Net Surplus (MW)  │
│    • Heat Threshold (100 C) & Dissipation Rate (C / sec)               │
│    • Recoil Absorption % (Kinetic & Ballistic stability)               │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.1 The Pilot Reaction Limit Calculus (限界 - Genkai)
In Gihren's Greed, giving a high-performance ace pilot a standard mass-produced mobile suit wastes their potential because the actuators cannot keep pace with the pilot's neural synapses.

$$	ext{Effective Pilot Reflex Bonus} = \min\left(	ext{Pilot Reflexes}, 	ext{Mobile Suit Limit \%} - 100
ight)$$

$$	ext{Final Combat Accuracy} = 	ext{Base Weapon Acc} + \left(	ext{Effective Pilot Reflex Bonus} 	imes 0.5
ight)$$
$$	ext{Final Combat Evasion} = 	ext{Base Chassis Eva} + \left(	ext{Effective Pilot Reflex Bonus} 	imes 0.6
ight)$$

- **Example 1**: Ace Pilot *Null-07* has Reflexes $= 88$. Assigned to a standard Line *Ironclad* with $	ext{Limit} = 110\%$.
  $$	ext{Effective Bonus} = \min(88, 110 - 100) = 10\% \implies 	ext{Ace is bottlenecked by sluggish hydraulics!}$$
- **Example 2**: *Null-07* pilots a *Muramasa Spec-X* tuned with **S-Rank Hydraulic Alignment** ($	ext{Limit} = 195\%$):
  $$	ext{Effective Bonus} = \min(88, 195 - 100) = 88\% \implies 	ext{Full +44% Accuracy and +52.8% Evasion unlocked!}$$

### 2.2 Propellant & Energy (EN / 推進剤) Dynamics
Every action on the tactical grid drains fuel or energy:
- **Tile Movement**: $-3$ to $-6	ext{ EN}$ per tile (scaled by chassis weight).
- **Boost Dash / Vernier Leap**: $-15	ext{ EN}$.
- **Beam Rifle / Energy Weapon Discharge**: $-8$ to $-25	ext{ EN}$ per shot.
- **Kinetic Autocannons**: Drains physical ammunition, but $-2	ext{ EN}$ for servo cycling.
- **Zero Fuel State**: When Propellant reaches 0, the suit cannot boost, move beyond 1 tile, or fire energy weapons until resupplied by a base or auxiliary supply vehicle.

### 2.3 Terrain Adaptability Ratings (地形適性)
Each chassis and leg module has environmental ratings across **Ground**, **Space**, **Urban**, and **Trench**:
- **S-Rank**: $+20\%$ Evasion, $-1	ext{ AP}$ movement cost, zero heat penalty.
- **A-Rank**: Standard movement and combat efficiency ($100\%$).
- **B-Rank**: $+10\%$ Heat generation, $+0.5	ext{ AP}$ move cost.
- **C-Rank**: $-15\%$ Evasion, $+1	ext{ AP}$ move cost, $+20\%$ fuel consumption.
- **D-Rank**: Inoperable or $-30\%$ combat penalties (e.g. pure ground walker in zero-G vacuum).

### 2.4 Prometheus Flux / ECM Particle Dispersion (散布 / 索敵)
- **Prometheus Flux ECM Density (0% to 75%)**: High ECM creates a jamming sphere that deflects laser targeting, reduces enemy lock-on ranges, and grants adjacent allies $+15\%$ to $+35\%$ guided missile decoy chance.
- **Sensor Search Grade (S/A/B/C)**: Determines fog-of-war vision radius and critical hit probability.

---

## 3. The 3 Prototyping Minigames & Performance Scaling

When building a custom mobile suit or tuning a prototype in the R&D Lab, the player's performance in the three minigames dynamically calculates a **Performance Score (0–100%)** and **Engineering Grade (S, A, B, C, D)** that directly scale the finished mobile suit's capabilities.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      MINIGAME PERFORMANCE TIERS                       │
├─────────┬──────────────┬───────────────────────────────────────────────┤
│ Grade   │ Score Range  │ Stat Multiplier & Blueprint Designation       │
├─────────┼──────────────┼───────────────────────────────────────────────┤
│ S-RANK  │ 95% - 100%   │ Flawless Prototype Ace (+25% to +35% Stats)   │
│ A-RANK  │ 85% - 94%    │ Masterwork Specification (+15% to +20% Stats) │
│ B-RANK  │ 70% - 84%    │ Fine Precision Line Unit (+5% to +10% Stats)  │
│ C-RANK  │ 50% - 69%    │ Standard Assembly Baseline (+0% Baseline)     │
│ D-RANK  │ 0% - 49%     │ Sub-Par Tolerance Flaw (-10% to -25% Penalty) │
└─────────┴──────────────┴───────────────────────────────────────────────┘
```

---

### 3.1 Minigame 1: Tokamak Reactor Conduit Harmonic Wave Tuning
**Target Component**: Torso / Fusion Reactor Core  
**Core Concept**: Oscilloscope frequency resonance and plasma confinement.

*   **Player Inputs**:
    1. **Frequency Slider** ($0.5$ to $4.0$ Hz)
    2. **Amplitude Slider** ($15.0$ to $75.0$ MW)
    3. **Phase Offset Slider** ($0.0$ to $360.0^\circ$)
    4. **Harmonic Pulse Commit Button**
*   **Scoring Formula**:
    $$	ext{Score} = \max\left(0.0, 100.0 - \left(|\Delta 	ext{Freq}| 	imes 32.0 + |\Delta 	ext{Amp}| 	imes 1.1 + |\Delta 	ext{Phase}| 	imes 0.32
ight)
ight)$$
*   **Stat Propagation to Mobile Suit**:
    - **S-Rank (95%+)**: $+25\%$ Reactor Output (MW), $+35\%$ Heat Dissipation Rate, $+20\%$ Energy Weapon DMG, $+30\%$ EN Capacity.
    - **A-Rank (85–94%)**: $+15\%$ Reactor Output, $+20\%$ Heat Dissipation Rate, $+10\%$ Energy DMG, $+15\%$ EN Capacity.
    - **B-Rank (70–84%)**: $+5\%$ Reactor Output, $+10\%$ Heat Dissipation Rate.
    - **C-Rank (50–69%)**: Standard factory specs ($+0\%$).
    - **D-Rank (<50%)**: $-15\%$ Reactor Output, $-25\%$ Heat Dissipation, $+20\%$ Heat build-up per shot.

---

### 3.2 Minigame 2: Limb Hydraulic Stress Alignment
**Target Component**: Legs & Arms (Locomotion Actuators)  
**Core Concept**: Finite pulse budget to balance hydraulic cylinder pressures within safe welding tolerances.

*   **Player Inputs**:
    1. **Select Joint**: Hip Actuator, Knee Hydraulic, Ankle Gyro, Foot Stabilizer.
    2. **Relieve Pressure Button**: Drops selected joint stress by $-16\%$, backpressure shifts $+4\%$ to neighbors.
    3. **Tighten Cylinder Button**: Raises selected joint stress by $+14\%$, relieves neighbors by $-3\%$.
    4. **Spot-Weld Lock Button**: Locks joint if stress is within optimal $25\% - 45\%$ band. Consumes 1 pulse.
    5. **Pulse Budget**: 8 pulses total.
*   **Scoring Formula**:
    $$	ext{Score} = \left(rac{	ext{Locked Joints Count}}{4} 	imes 70.0
ight) + \left(rac{	ext{Remaining Pulses}}{8} 	imes 30.0
ight)$$
    *(If any joint is unlocked when budget is depleted, Score is penalized by $-20\%$.)*
*   **Stat Propagation to Mobile Suit**:
    - **S-Rank (95%+)**: Sets **Pilot Limit (Genkai)** to $200\%$, $+30\%$ Recoil Absorption, $+1	ext{ Base AP}$, $+25\%$ Leg Armor HP.
    - **A-Rank (85–94%)**: Sets Pilot Limit to $175\%$, $+20\%$ Recoil Absorption, $+15\%$ Leg Armor HP.
    - **B-Rank (70–84%)**: Sets Pilot Limit to $145\%$, $+10\%$ Recoil Absorption.
    - **C-Rank (50–69%)**: Sets Pilot Limit to $115\%$ (Standard line unit).
    - **D-Rank (<50%)**: Sets Pilot Limit to $90\%$ (Severe actuator stutter; caps ace pilots!), $-15\%$ Recoil Absorption, $-1	ext{ AP}$ move penalty.

---

### 3.3 Minigame 3: Thruster Plasma Flow Calibration
**Target Component**: Backpack & Vernier Boosters  
**Core Concept**: Multi-stage magnetic constriction resonance throttle.

*   **Player Inputs**:
    1. **Stage 1**: Ignition Pre-Chamber ($	ext{Fuel} pprox 35.0, 	ext{Coil} pprox 40.0$).
    2. **Stage 2**: Magnetic Choke Constriction ($	ext{Fuel} pprox 55.0, 	ext{Coil} pprox 65.0$).
    3. **Stage 3**: Vernier Acceleration Ring ($	ext{Fuel} pprox 75.0, 	ext{Coil} pprox 60.0$).
    4. **Stage 4**: Full Vector Plasma Discharge ($	ext{Fuel} pprox 90.0, 	ext{Coil} pprox 85.0$).
*   **Scoring Formula**:
    $$	ext{Stage Resonance} = \max\left(0.0, 100.0 - |\Delta 	ext{Fuel}| 	imes 1.5 - |\Delta 	ext{Coil}| 	imes 1.5
ight)$$
    $$	ext{Final Score} = rac{1}{4} \sum_{k=1}^4 	ext{Resonance}_k$$
*   **Stat Propagation to Mobile Suit**:
    - **S-Rank (95%+)**: $+35\%$ Booster Thrust ($kN$), $+25\%$ Evasion %, Space Terrain Adaptability promoted to **S**, $+35\%$ Fuel Efficiency.
    - **A-Rank (85–94%)**: $+20\%$ Booster Thrust, $+15\%$ Evasion %, $+20\%$ Fuel Efficiency.
    - **B-Rank (70–84%)**: $+10\%$ Booster Thrust, $+8\%$ Evasion %, $+10\%$ Fuel Efficiency.
    - **C-Rank (50–69%)**: Baseline factory thrust ($+0\%$).
    - **D-Rank (<50%)**: $-15\%$ Booster Thrust, $-12\%$ Evasion %, $-25\%$ Fuel Efficiency (Plasma flameout risk).

---

## 4. Canonical 21 Blueprints Comprehensive Stat Matrix

Below is the complete balance matrix for all 21 canonical mobile suits combining Front Mission and Gihren's Greed stats:

| Model Code | Name | Faction | Pilot Limit % | Max EN | Terrains (G/S/U/T) | Flux ECM % | Search | Total Armor | Net MW |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **GHA-07** | Ironclad | Terran | 115% | 140 | A / B / A / C | 25% | B | 2,480 | +160 |
| **GHA-07B**| Siegebreaker | Terran | 120% | 160 | A / B / S / C | 30% | B | 2,850 | +140 |
| **TC-B11**  | Behemoth | Terran | 110% | 200 | S / C / A / D | 35% | B | 3,400 | +180 |
| **TC-B03**  | Bulwark | Terran | 105% | 130 | A / B / A / C | 20% | C | 2,200 | +120 |
| **AET-01**  | Aether | Colony | 145% | 120 | B / S / B / B | 45% | A | 1,680 | +190 |
| **AET-09**  | Aether Mk-II | Colony | 165% | 140 | B / S / A / B | 50% | A | 1,890 | +220 |
| **OCM-04**  | Sylph | Colony | 150% | 110 | C / S / B / B | 55% | S | 1,420 | +180 |
| **OCM-07**  | Helios | Colony | 155% | 135 | B / S / B / B | 40% | A | 1,750 | +210 |
| **OCM-15**  | Seraphim | Colony | 180% | 170 | A / S / A / B | 60% | S | 2,100 | +260 |
| **SCR-12**  | Hyena | Syndicate | 125% | 115 | A / A / S / B | 35% | B | 1,590 | +130 |
| **SCR-05**  | Marauder | Syndicate | 130% | 130 | A / A / S / B | 40% | B | 1,840 | +150 |
| **SCR-14**  | Slag Lobber | Syndicate | 110% | 150 | A / B / A / C | 30% | C | 2,350 | +140 |
| **SCR-19**  | Chimera | Syndicate | 140% | 140 | A / A / S / B | 45% | B | 2,050 | +170 |
| **ZAI-03**  | Muramasa | Zaibatsu | 170% | 150 | A / S / S / C | 55% | S | 1,920 | +240 |
| **ZAI-06**  | Ronin | Zaibatsu | 160% | 135 | A / S / A / C | 50% | A | 1,760 | +210 |
| **ZAI-15**  | Raiden | Zaibatsu | 185% | 165 | A / S / S / B | 65% | S | 2,240 | +280 |
| **ZAI-22**  | Susanoo | Zaibatsu | 210% | 190 | S / S / S / A | 75% | S | 2,680 | +320 |
| **PMC-V01** | Vanguard Heavy | Player | 135% | 150 | A / A / A / B | 35% | B | 2,200 | +175 |
| **PMC-S02** | Stratos Intercept | Player | 155% | 130 | B / S / B / B | 45% | A | 1,650 | +205 |
| **PMC-G03** | Ghost Sniper | Player | 160% | 125 | A / S / B / B | 60% | S | 1,520 | +195 |
| **PMC-B04** | Scrapper Brawler | Player | 130% | 140 | S / B / S / A | 30% | B | 2,100 | +150 |

---

## 5. Step-by-Step In-Game Minigame Tutorials

### 5.1 Tutorial: Tokamak Harmonic Oscillator (Reactor Tuning)
1. **The Goal**: Match your Cyan containment wave to the Target White fusion wave.
2. **Phase 1: Frequency Matching**: Drag the **Frequency Slider** until your wave peaks match the horizontal spacing of the white wave.
3. **Phase 2: Amplitude Matching**: Adjust the **Amplitude Slider** until the vertical height matches the white peaks.
4. **Phase 3: Phase Shift Alignment**: Slide the **Phase Slider** to shift your wave left/right until the cyan wave directly overlaps the white wave.
5. **Phase 4: Containment Pulse**: Click **[DISCHARGE CONTAINMENT PULSE]**. 
   - Achieving $\ge 95\%$ locks in an **S-Rank Reactor (+25% Output, +35% Cooling)**.
   - Falling below $50\%$ triggers an unstable coil warning and $-15\%$ output penalty.

### 5.2 Tutorial: Hydraulic Stress Balancing (Limb Tuning)
1. **The Goal**: Balance all 4 hydraulic joint nodes (Hip, Knee, Ankle, Foot) inside the safe welding band ($25\% - 45\%$) using your 8-pulse budget.
2. **Step 1: Inspect Stresses**: Look at the current stress levels. Red/Amber joints ($>50\%$) are over-pressured; blue joints ($<20\%$) are slack.
3. **Step 2: Relieve & Tighten**:
   - Clicking **[RELIEVE PRESSURE]** drops the joint by $-16\%$, but shifts $+4\%$ backpressure to adjacent joints.
   - Clicking **[TIGHTEN CYLINDER]** raises the joint by $+14\%$, easing neighbors by $-3\%$.
4. **Step 3: Spot-Weld Locking**: Once a joint is between $25\%$ and $45\%$, click **[SPOT-WELD LOCK]**! This permanently locks the joint and protects it from subsequent neighbor backpressure.
5. **Step 4: Lock All Four Joints**: Successfully locking all four joints achieves an **S-Rank or A-Rank Limit % (Genkai)** rating for your mobile suit, unlocking the full reaction speed of your ace pilots!

### 5.3 Tutorial: Thruster Plasma Flow Calibration (Vernier Tuning)
1. **The Goal**: Achieve optimal magnetic resonance across all 4 sequential burn stages.
2. **Step 1: Balance Stage 1**: Adjust **Fuel Injection** to $pprox 35\%$ and **Magnetic Coil** to $pprox 40\%$. Click **[COMMIT STAGE PULSE]**.
3. **Step 2: Balance Stage 2**: Constrict the choke! Move Fuel to $pprox 55\%$ and Coil to $pprox 65\%$. Commit pulse.
4. **Step 3: Balance Stage 3**: High velocity ring! Move Fuel to $pprox 75\%$ and Coil to $pprox 60\%$. Commit pulse.
5. **Step 4: Balance Stage 4**: Full discharge! Move Fuel to $pprox 90\%$ and Coil to $pprox 85\%$. Commit final pulse.
6. **Result**: Averaging $\ge 95\%$ resonance grants **S-Rank Booster Thrust (+35% Thrust, +25% Evasion, S-Rank Space Adaptability)**!
