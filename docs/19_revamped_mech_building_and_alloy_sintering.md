# Mech Building & Alloy Creation System Overhaul

## Executive Summary
This overhaul elevates the Mobile Suit fabrication, metallurgical sintering crucible, and custom chassis combinations system into a deeply tactical, 16-bit military engineering suite inspired by Front Mission (SNES) and Gihren's Greed (PS1/Saturn).

---

## 1. Metallurgical Sintering Crucible Overhaul (Tab 0, Subtab 0)

### 1.1 Animated 16-Bit Thermal Sintering Chamber
- **Blast-Aperture Viewport:** Replaced flat boxes with an industrial quartz viewing viewport framed with beveled steel and hazard bevels.
- **Molten Convection Magma Bed:** Real-time undulating sinusoidal molten layer responding to temperature (wave function) shifting from deep cherry incandescence to brilliant plasma cyan.
- **Dynamic Elemental Reaction Sparks:** Procedural sparks rendered using additive blending (bm_add), dynamically tinted according to the precursor elements loaded in the hopper:
  - **Tritium Gas:** Electric Ion Cyan (#00F5FF)
  - **Synthetic Flux:** Catalytic Solar Gold (#FFAF28)
  - **Raw Tungsten:** White-Hot Molten Steel (#E0F0FF)
  - **Silica-Carbon:** Charcoal Crystalline Scintillations (#7085A0)
- **Pressure Relief Exhaust Steam:** Animated relief steam plumes during venting or extreme chamber compression (>6,000 PSI).

### 1.2 16-Bit Segmented LED Gauges
- **Temperature Gauge:** Discrete 6px LED blocks with dynamic green/cyan/orange/red bands indicating operational envelopes (1,700°C – 4,950°C).
- **Pressure Chamber Gauge:** Segmented LED bar with target compression brackets (Vacuum <800 PSI vs. Compression >4,000 PSI).
- **Volatility Gauge:** Discrete LED monitor with flashing hazard caution stripes and emergency text strobe when volatility exceeds 70%.

### 1.3 Canonical 8-Alloy Recipe Matrix
The crucible synthesis engine now supports 8 canonical military alloys with strict stoichiometric and thermomechanical envelopes:

| Alloy Code | Name | Precursors | Target Temp | Target Pressure | Role / Combat Bonus | Hex Finish |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| alloy_vanguard_comp | Vanguard Composite | 2 W, 1 C | 2200–2500°C | < 1,200 PSI | +30% Kinetic Defense Plating | #7387A0 |
| alloy_hyperion_matrix | Hyperion Superconductor | 1 W, 2 Tr, 1 Fx | 4000–4600°C | 4000–10,000 PSI | Tokamak Core Superconductor Matrix | #3CE6FF |
| alloy_aerosteel_flux | Aerosteel Vernier Flux | 1 C, 2 Fx | 1800–2250°C | < 1,200 PSI | Lightweight High-G Thruster Cowling | #C396FF |
| alloy_adamantine_carbide | Adamantine Heavy Carbide | 3 W, 1 C, 1 Fx | 3000–3550°C | > 3,000 PSI | Superheavy AP Armor Plating | #FF9B3C |
| alloy_reactive_damascus | Reactive Damascus Composite | 3 W, 2 Fx, 1 Tr | 3400–3800°C | 4500–7,000 PSI | +35% Explosive Kinetic Deflection | #B4465A |
| alloy_tachyon_superalloy | Tachyon Superalloy Matrix | 1 W, 2 Tr, 2 Fx | 4600–4950°C | 8000–10,000 PSI | +40% Energy Weapon Output Conduit | #64F0FF |
| alloy_lunar_aerogel | Lunar Aerogel Matrix | 3 C, 2 Fx | 1700–2100°C | < 800 PSI (Vacuum) | -40% Chassis Mass / +50% Heat Venting | #DCF0FF |
| alloy_sol_ferrite | Sol Ferrite Conductor | 3 W, 1 C, 2 Tr | 4100–4400°C | 5500–8,500 PSI | +45% Railgun Velocity & Line Punch | #E6B428 |

### 1.4 Live Stoichiometric Reaction Preview Plaque
- Automatically detects candidate recipes from loaded hopper inputs before firing.
- Live real-time temperature status check: [TEMP: OPTIMAL] vs. [TEMP LOW: NEED +X°C] vs. [TEMP HIGH: -X°C].
- Live real-time pressure status check: [PRESS: OPTIMAL] vs. [PRESS LOW: COMPRESS] vs. [PRESS HIGH: VENT].
- Projected Ingot Yield with purity percentage (96%–99%) and metallurgical synergy description.

---

## 2. Modular Part Fabrication Forge (Tab 1, Subtab 1)

### 2.1 30-Part Catalog Matrix (5 Parts per Hardpoint Slot)
Expanded from 18 to 30 distinct components, ensuring full utilization of all 8 alloys:
- **Heads (5 parts):** Vanguard Target-Lock, Aether EW-Dome, Cyclops Siege Optic, Damascus Reactive Visor, Tachyon Spectral Dome.
- **Torsos (5 parts):** Colossus Heavy Torso, Hyperion Tokamak, Phantom Striker, Damascus Reactive Citadel, Sol Ferrite Super-Tokamak.
- **Arms (5 parts):** Colossus Dual Arms, Vernier Fast-Actuators, Adamantine Heavy Brackets, Lunar Aerogel Manipulators, Tachyon Conduit Arms.
- **Legs (5 parts):** Vanguard Heavy Walkers, Stratos Vernier Skaters, Titan Quad-Leg, Lunar Aerogel Hover Struts, Damascus Armored Treads.
- **Backpacks (5 parts):** Heavy Booster Pack, Dual-Vector Vernier Rig, Plasma Overcharge Booster, Lunar Aerogel Siphon Rig, Tachyon Fold Warp Booster.
- **Weapons (5 parts):** Rotary Vulcan (120mm), Particle Beam Rifle, Heavy Siege Rail Cannon, Sol Ferrite Hyper-Railgun, Tachyon Beam Lance.

---

## 3. Custom Combinations Assembly Bay (Tab 1, Subtab 2)

### 3.1 3-Column Tactical Mecha Engineering Deck
1. **Left Column (Modular Hardpoints):** 6 equipped hardpoint cards with cycling controls (< and >), mini alloy swatches, stat breakdown, and interactive socket selection.
2. **Center Column (Wanzer CAD Schematic):** Interactive CAD wireframe (spr_mech_schematic) with coordinate grid, socket reticles with [ ] targeting brackets, dynamic torso alloy armor tinting, active metallurgy composition plaque, and weight class assessment.
3. **Right Column (Engineering Calculus & Commissioning):** Segmented LED gauges for Armor and Tokamak Power Balance, mobility dynamics, combat rating, Gihren's Greed telemetry, [>> COMMISSION INTO HANGAR <<], and [★ SAVE AS PMC CANONICAL BLUEPRINT].
