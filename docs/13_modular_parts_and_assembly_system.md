# Document 13: Mining, Alloy Chemistry & Modular Mobile Suit Assembly System

## 1. Executive Summary & Design Vision
The central gameplay pillar of *MechMakerConcept* is the end-to-end industrial loop:
1. **Mining Operations**: Harvesting elemental raw materials across contested orbital nodes.
2. **Alloy Crucible Chemistry**: Sintering and fusing base elements into high-grade proprietary alloys.
3. **Modular Part Fabrication**: Forging 6 discrete mobile suit components from crafted alloys.
4. **Custom Combinations Assembly**: Combining modular components into unique, combat-ready mobile suits subject to real physical constraints (Reactor Power Budget, Weight-to-Thrust Ratios, Structural Integrity).

A customized mobile suit can subsequently be:
- Assigned to escort and secure mining nodes.
- Fielded in personal PMC offensives to conquer star sectors and overthrow galactic superpowers.
- Pitched to superpower Ordnance Boards to permanently replace their mass-produced standard issue suits.

---

## 2. Resource Mining Operations & Nodes

### 2.1 The 4 Elemental Precursors
| Material ID | Elemental Resource | Primary Source | Base Value | Industrial Role |
|---|---|---|---|---|
| `mat_tungsten` | Raw Heavy Tungsten | Asteroid Belt Claims | 400 Cr | Dense kinetic plating, structural bipedal frames |
| `mat_silica_carb` | Silica-Carbon Composite | Lunar Regolith Concessions | 150 Cr | Lightweight matrices, heat baffles, mass reduction |
| `mat_tritium` | Plasma-Charged Tritium | Jovian Orbital Scoops | 1,200 Cr | Tokamak fusion fuel, plasma pulse weaponry |
| `mat_syn_flux` | Synthetic Volatile Flux | Delta Smuggler Black Markets | 800 Cr | Catalytic bonding agent, superconducting matrices |

### 2.2 Extraction Operations & Escort Security
Mining nodes generate resources per turn. Hostile corsairs and rival syndicates constantly raid undefended claims.
- **Escort Security Rating**:
  $$\\text{Raid Chance} = \\max(0, \\text{Base Threat} - \\text{Assigned Mech Combat Rating} \\times 0.5)$$
- If undefended, shipments risk catastrophic piracy losses.

---

## 3. The 4 Proprietary Alloys (The Metallurgical Matrix)

| Alloy ID | Alloy Name | Required Elemental Ingredients | Sintering Temp (°C) | Pressure (PSI) | Doctrinal Specialty |
|---|---|---|---|---|---|
| `alloy_vanguard_comp` | Vanguard Composite Armor | 2x Tungsten, 1x Silica-Carbon | 2200°C – 2500°C | < 1200 PSI | Heavy kinetic & ballistic armor plating |
| `alloy_hyperion_matrix` | Hyperion Superconductor Matrix | 1x Tritium, 1x Flux, 1x Tungsten | 4000°C – 4500°C | 4000 – 8000 PSI | Tokamak fusion reactors, plasma rifles |
| `alloy_aerosteel_flux` | Aerosteel Vernier Alloy | 1x Silica-Carbon, 2x Flux | 1800°C – 2200°C | < 1000 PSI | Lightweight vernier thrusters & agile frames |
| `alloy_adamantine_carbide`| Adamantine Heavy Carbide | 3x Tungsten, 1x Silica, 1x Flux | 3000°C – 3500°C | > 3000 PSI | Hydraulic limb frames, heavy vulcan barrels |

---

## 4. The 6 Modular Part Categories & Specifications

Every mobile suit consists of exactly 6 slots:

### 4.1 HEAD (Sensors, Fire Control & Targeting)
- **HD-01 Vanguard Target-Lock Sensor**: Forged from 1x Vanguard Composite (15k Cr). Armor: 120 HP, Mass: 4t, Power Draw: 2 MW. Tactical Bonus: +15% Accuracy.
- **HD-02 Aether EW-Dome**: Forged from 1x Aerosteel Flux (25k Cr). Armor: 90 HP, Mass: 2t, Power Draw: 4 MW. Tactical Bonus: +18% Evasion.
- **HD-03 Cyclops Siege Optic**: Forged from 1x Adamantine Carbide (35k Cr). Armor: 160 HP, Mass: 6t, Power Draw: 3 MW. Tactical Bonus: +20% Critical Hit.

### 4.2 TORSO (Chassis Frame & Fusion Reactor Core)
*The Torso houses the fusion reactor, which GENERATES the suit's total Power Output!*
- **TR-01 Colossus Reinforced Heavy Torso**: Forged from 3x Vanguard Composite (65k Cr). Armor: 480 HP, Mass: 26t, Output: +28 MW Surplus, Dissipation: 35. Heavy bipedal assault core.
- **TR-02 Hyperion Tokamak Plasma Torso**: Forged from 2x Hyperion Matrix + 1x Vanguard (95k Cr). Armor: 360 HP, Mass: 20t, Output: +42 MW Surplus, Dissipation: 50. High-spec energy powerhouse.
- **TR-03 Phantom Lightweight Striker Torso**: Forged from 2x Aerosteel Flux (75k Cr). Armor: 300 HP, Mass: 14t, Output: +32 MW Surplus, Dissipation: 45. Ultra-light skirmisher core.

### 4.3 ARMS (Manipulators, Recoil Stabilizers & Actuators)
- **AM-01 Colossus Hydraulic Dual Arms**: Forged from 2x Vanguard Composite (40k Cr). Armor: 260 HP, Mass: 16t, Power Draw: 4 MW. Recoil Control: +25%.
- **AM-02 Vernier Fast-Actuator Arms**: Forged from 2x Aerosteel Flux (50k Cr). Armor: 190 HP, Mass: 10t, Power Draw: 5 MW. Handling/Melee: +20%.
- **AM-03 Adamantine Heavy Weapon Brackets**: Forged from 2x Adamantine Carbide (60k Cr). Armor: 320 HP, Mass: 22t, Power Draw: 6 MW. Ballistic Damage: +20%.

### 4.4 LEGS (Hydraulics, Footing & Base Ground Mobility)
- **LG-01 Vanguard Heavy Bipedal Walkers**: Forged from 3x Vanguard Composite (55k Cr). Armor: 340 HP, Mass: 24t, Power Draw: 5 MW. Base Speed: 42 kph. Kinetic absorption +30%.
- **LG-02 Stratos Aerodynamic Vernier Skaters**: Forged from 2x Aerosteel Flux + 1x Hyperion (70k Cr). Armor: 220 HP, Mass: 15t, Power Draw: 7 MW. Base Speed: 88 kph. Agility: +25%.
- **LG-03 Titan Quad-Leg Siege Platform**: Forged from 3x Adamantine Carbide (80k Cr). Armor: 440 HP, Mass: 34t, Power Draw: 8 MW. Base Speed: 34 kph. Recoil Absorb: +50%.

### 4.5 BACKPACK (Vector Thrusters & Vernier Manifolds)
- **BP-01 Heavy Solid-Fuel Booster Pack**: Forged from 1x Vanguard Composite (25k Cr). Armor: 140 HP, Mass: 12t, Power Draw: 3 MW. Boost Speed: +35 kph.
- **BP-02 Dual-Vector Vernier Acceleration Rig**: Forged from 2x Aerosteel Flux (45k Cr). Armor: 100 HP, Mass: 8t, Power Draw: 6 MW. Boost Speed: +65 kph, Evade: +15%.
- **BP-03 Plasma Overcharge Booster**: Forged from 2x Hyperion Matrix (65k Cr). Armor: 120 HP, Mass: 10t, Power Draw: 9 MW. Boost Speed: +80 kph, Dash AP: +1.

### 4.6 PRIMARY WEAPON (Mounted Armaments)
- **WP-01 Rotary Heavy Vulcan Cannon (120mm)**: Forged from 2x Adamantine Carbide (45k Cr). Armor: 100 HP, Mass: 12t, Power Draw: 3 MW. Firepower: 180 Dmg, Sustained fire.
- **WP-02 Twin Particle Beam Pulse Rifle**: Forged from 2x Hyperion Matrix (60k Cr). Armor: 80 HP, Mass: 8t, Power Draw: 10 MW. Firepower: 240 Dmg, Armor Piercing.
- **WP-03 Heavy Siege Rail Cannon (300mm)**: Forged from 2x Adamantine Carbide + 1x Hyperion (85k Cr). Armor: 130 HP, Mass: 20t, Power Draw: 8 MW. Firepower: 380 Dmg, Long Range.

---

## 5. Mobile Suit Assembly & Combinations Calculus

### 5.1 Power Balance & Reactor Overload Rule
$$\\text{Net Power Surplus (MW)} = \\text{Output}_{\\text{Torso}} - \\left(\\text{Draw}_{\\text{Head}} + \\text{Draw}_{\\text{Arms}} + \\text{Draw}_{\\text{Legs}} + \\text{Draw}_{\\text{Backpack}} + \\text{Draw}_{\\text{Weapon}}\\right)$$
**ENGINEERING RULE**: $\\text{Net Power Surplus} \\ge 0$. If negative, the suit suffers **REACTOR OVERLOAD** and cannot be commissioned into service.

### 5.2 Physical Attributes
- **Total Armor HP**: Sum of armor ratings across all 6 slots.
- **Total Mass (Tonnes)**: Sum of masses across all 6 slots.
- **Effective Walk Speed**: $\\text{Speed}_{\\text{Legs}} \\times \\left(1 - \\frac{\\text{Total Mass}}{180}\\right)$
- **Effective Boost Speed**: $\\text{Walk Speed} + \\text{Boost Bonus}_{\\text{Backpack}}$
- **Tactical Combat Rating**:
  $$\\text{Rating} = \\text{Total Armor} / 5 + \\text{Weapon Firepower} + \\text{Boost Speed} / 2 + \\text{Net Power} \\times 2$$

### 5.3 Commissioning & Custom Naming
Upon completing assembly, the player can assign a custom designation (e.g. *Ironclad Chimera Spec-X*) and commission the suit into the Hangar Bay as a functional `READY` unit.
