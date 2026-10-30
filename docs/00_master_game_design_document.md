# MECHMAKER CONCEPT: IRON VANGUARD
## Comprehensive Master Game Design & Feature Architecture Document
**Version:** 2.5.0 // **Lead Systems Architecture Specification**  
**Design Reference:** SNES 16-Bit Mecha Tactical RPG (*Front Mission*) & Grand Geopolitical Simulation (*Gihren's Greed*)

---

## 1. Executive Vision & Core Pillars

### 1.1 Premise
In a fragmented solar system torn between four irreconcilable ideological factions, the player operates an independent Private Military Corporation (PMC) operating from a mobile dreadnought flagship. The player's enterprise thrives not through blind allegiance, but through superior engineering, material mastery, pilot development, and strategic military contracting.

### 1.2 Core Pillars
1. **Deep Metallurgy & Sintering Chemistry:** Moving beyond generic crafting tiers into real stoichiometry, temperature/pressure phase shifts, crystal lattice densities, and programmatic alloy finishes across 118 elements.
2. **Modular Combinations Engineering:** Six discrete modular hardpoints (Heads, Torsos, Arms, Legs, Backpacks, Weapons) balanced through strict Tokamak thermonuclear physics, weight-to-thrust dynamics, and operational telemetry (*Genkai %*, *EN*, *ECM*).
3. **Pilot Nemesis & Relational Psychology:** A persistent social web of pilots featuring rivalries, friendship referral networks, star-crossed romances, battlefield casualties, psychological trauma (e.g. *Berserker Rage*), and procedural ambush drop-pod incursions.
4. **Grand Isometric Tactical Combat:** High-stakes turn-based warfare utilizing true 2:1 isometric coordinate math, 4-directional armor facings, localized limb destruction, kinetic ballistic trajectories, and dynamic environmental terrain.
5. **Geopolitical Interstellar Warfare & Procurement Trials:** A dynamic frontline sector map where four factions wage autonomous war, offering combat bounties, commodity trade arbitrage, and multi-round competitive **Fly-Off Procurement Trials** to secure canonical mass-production contracts.
6. **Mobile Flagship Dreadnought Progression:** A sprawling 8-division, 5-tier upgrade tree transforming a derelict command cruiser into an interstellar behemoth capable of instantaneous Tachyon Fold jumps and apocalyptic orbital artillery strikes.
7. **The Prometheus Catalyst & Dawn of the Mobile Suit:** The player's independent foundry is the singular catalyst that invents and deploys the first operational bipedal Mobile Suit in human history. The universe begins in Era 0 (Conventional Warfare: Main Battle Tanks, Strike Jets, Skiffs, Gun Trucks), where the player's maiden sortie shocks the solar system, flipping hostile superpowers into high-bounty contract partners (3.0x Prometheus Subsidies) and triggering a 365-day reverse-engineering arms race across four rival defense megacorporations.

---

## 2. Daily Command Loop (HQ Command Cycle)

The game progresses through a turn-based daily operational loop:

```
+-----------------------------------------------------------------------------------+
|                            PMC DAILY COMMAND CYCLE                                |
+-----------------------------------------------------------------------------------+
|  PHASE 1: STRATEGIC INTEL & LOGISTICS TICK                                       |
|  - Automated Solar Mining Node extraction ticks raw elements into storage.        |
|  - Active flagship fabrications advance (days remaining decrement).              |
|  - Faction frontline war simulation ticks sector control & commodity prices.     |
|  - Intelligence ticker updates with interstellar news, bounties, and nemeses.     |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|  PHASE 2: HQ OPERATIONS (THE 4 COMMAND TERMINAL WORKSPACES)                       |
|  - TAB 0: R&D LAB (Sintering Crucible, Prototyping Minigames, Blueprint Archive)   |
|  - TAB 1: FLEET & BASE (Fabrication Bays, Part Forge, Custom Combinations Bay)     |
|  - TAB 2: CONTRACTS & LOGISTICS (Faction Contracts, Fly-Off Trials, Commodity Ex) |
|  - TAB 3: STRATEGIC THEATER & COMBAT SORTIES (War Map, Platoon Deployment, Sortie) |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|  PHASE 3: TACTICAL COMBAT & SECTOR SORTIES                                        |
|  - Deploy customized platoon to contested planetary and orbital combat zones.     |
|  - Navigate isometric terrain, directional cover, and line-of-sight.              |
|  - Face rival ace pilots; handle unexpected procedural Drop-Pod Nemesis Ambush.   |
|  - Resolve salvage, structural damage repairs, and pilot casualties/grudges.      |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|  PHASE 4: CYCLE ADVANCEMENT & TURN TRANSITION                                     |
|  - Payroll, maintenance fees, and faction reputation deltas calculated.           |
|  - Pilot trauma states progress; relationship bond counters update.               |
+-----------------------------------------------------------------------------------+
```

---

## 3. Deep Metallurgy & Alloy Sintering Engine

### 3.1 Precursor Materials & Elemental Hopper
The foundation of all mobile suit engineering begins at atomic scale. The crucible hopper accepts inputs from warehouse reserves:
- **Raw Tungsten (`mat_tungsten`):** High tensile density (19.3 g/cm³), melting point 3,422°C. Found in heavy asteroidal cores.
- **Silica-Carbon Composite (`mat_silica_carb`):** Lightweight high-carbon graphite matrix (2.3 g/cm³), high thermal absorption.
- **Synthetic Catalytic Flux (`mat_syn_flux`):** Rare-earth sintering bonding agent (4.8 g/cm³) that lowers activation energy and bridges incompatible crystal lattices.
- **Plasma-Charged Tritium Gas (`mat_tritium`):** High-energy isotope (280 W/mK) required for superconductivity and tokamak magnetic containment.
- **Periodic Table of Materials:** Supports procedural combinatorial metallurgy across all 118 elements (`materials_periodic_table.json`), generating unique procedural alloys with calculated tensile yield, radar cross-sections, and density.

### 3.2 Sintering Furnace Visualizer & Segmented Telemetry
Implemented with authentic 16-bit Front Mission aesthetics in `obj_HQTerminal/Draw_64.gml`:
- **Industrial Quartz Aperture:** Heavy beveled viewport with rivet plates.
- **Molten Convection Magma Bed:** Real-time undulating sinusoidal magma bed responding to temperature and current turn.
- **Procedural Reaction Sparks:** Additive-blended particle sparks dynamically color-coded to precursor contents (Cyan for Tritium, Gold for Flux, Molten White for Tungsten, Dark Charcoal for Carbon).
- **Relief Steam Vents:** Automatic venting jets during pressure decompression.
- **Segmented LED Gauges:** 6px discrete LED bars for:
  - *Chamber Temperature:* 25°C to 5,000°C with target band indicators.
  - *Chamber Pressure:* 14.7 PSI to 10,000 PSI with compression status indicators.
  - *Chemical Volatility:* 0% to 100% (Breach threshold at 90%). Features hazard caution bars and emergency alarm strobe when exceeding 70%.

### 3.3 The 8 Canonical Sintering Alloys

| Alloy Key | Name | Inputs | Temperature Envelope | Pressure Envelope | Doctrine & Combat Bonus | Color & Hex |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `alloy_vanguard_comp` | Vanguard Composite Armor | 2W, 1C | 2200°C – 2500°C | < 1,200 PSI | +30% Kinetic & Ballistic Defense | `#7387A0` (Gunmetal Slate) |
| `alloy_hyperion_matrix` | Hyperion Superconductor | 1W, 2Tr, 1Fx | 4000°C – 4600°C | 4000 – 10,000 PSI | Tokamak Core Superconductivity | `#3CE6FF` (Cherenkov Cyan) |
| `alloy_aerosteel_flux` | Aerosteel Vernier Flux | 1C, 2Fx | 1800°C – 2250°C | < 1,200 PSI | -35% Component Weight / Vernier Agility | `#C396FF` (Vernier Violet) |
| `alloy_adamantine_carbide` | Adamantine Heavy Carbide | 3W, 1C, 1Fx | 3000°C – 3550°C | > 3,000 PSI | Superheavy AP Shells & Kinetic Plating | `#FF9B3C` (Heavy Bronze Amber) |
| `alloy_reactive_damascus` | Reactive Damascus Composite | 3W, 2Fx, 1Tr | 3400°C – 3800°C | 4500 – 7,000 PSI | +35% Explosive Reactive Deflection | `#B4465A` (Damascus Crimson) |
| `alloy_tachyon_superalloy` | Tachyon Superalloy Matrix | 1W, 2Tr, 2Fx | 4600°C – 4950°C | 8000 – 10,000 PSI | +40% Energy Weapon Output Conduit | `#64F0FF` (Supercharged Tachyon) |
| `alloy_lunar_aerogel` | Lunar Aerogel Matrix | 3C, 2Fx | 1700°C – 2100°C | < 800 PSI (Vacuum) | -40% Chassis Mass / +50% Heat Venting | `#DCF0FF` (Lunar Pale Frost) |
| `alloy_sol_ferrite` | Sol Ferrite High-Permeability | 3W, 1C, 2Tr | 4100°C – 4400°C | 5500 – 8,500 PSI | +45% Railgun Muzzle Velocity & Piercing | `#E6B428` (Radiant Solar Gold) |

### 3.4 Live Stoichiometric Reaction Preview Plaque
Before initiating furnace ignition, the system validates the loaded hopper in real time:
- Displays target alloy name, tier badge, and elemental ratio.
- Evaluates temperature: `[TEMP: OPTIMAL]` vs. `[TEMP LOW: NEED +X°C]` vs. `[OVERHEAT: NEED -X°C]`.
- Evaluates pressure: `[PRESS: OPTIMAL]` vs. `[PRESS LOW: COMPRESS]` vs. `[PRESS HIGH: VENT]`.
- Calculates expected ingot yield and metallurgical purity rating (96%–99%).

---

## 4. Component Fabrication & The 30-Part Matrix

Components are fabricated from synthesized alloys in the **Modular Part Forge** (Tab 1, Subtab 1). Five distinct components exist across all six hardpoint slots (30 parts total):

### 4.1 Heads (Sensors & Targeting)
- `hd_vanguard_01`: HD-01 Vanguard Target-Lock (120 HP, 4t, -2 MW) | +15% Accuracy [Vanguard Composite]
- `hd_aether_02`: HD-02 Aether EW-Dome (90 HP, 2t, -4 MW) | +18% Evasion [Aerosteel Flux]
- `hd_cyclops_03`: HD-03 Cyclops Siege Optic (160 HP, 6t, -3 MW) | +20% Critical Hit [Adamantine Carbide]
- `hd_damascus_04`: HD-04 Damascus Reactive Visor (195 HP, 5t, -3 MW) | +25% Kinetic Res & Targeting [Reactive Damascus]
- `hd_tachyon_05`: HD-05 Tachyon Spectral Dome (110 HP, 3t, -5 MW) | +30% Beam Critical & Deep Radar [Tachyon Superalloy]

### 4.2 Torsos (Cockpit & Reactor Cores)
- `tr_colossus_01`: TR-01 Colossus Heavy Torso (480 HP, 26t, +28 MW) | Reinforced Reactor Core [Vanguard Composite]
- `tr_hyperion_02`: TR-02 Hyperion Tokamak Torso (360 HP, 20t, +42 MW) | High-Spec Fusion Core [Hyperion Matrix]
- `tr_phantom_03`: TR-03 Phantom Striker Torso (300 HP, 14t, +32 MW) | Lightweight Agility Core [Aerosteel Flux]
- `tr_damascus_04`: TR-04 Damascus Reactive Citadel (560 HP, 28t, +36 MW) | Ablative Blast Deflection Core [Reactive Damascus]
- `tr_sol_05`: TR-05 Sol Ferrite Super-Tokamak (440 HP, 22t, +54 MW) | Apex Tokamak Core (+54 MW) [Sol Ferrite]

### 4.3 Arms (Actuators & Weapon Hardpoints)
- `am_colossus_01`: AM-01 Colossus Dual Arms (260 HP, 16t, -4 MW) | +25% Recoil Control [Vanguard Composite]
- `am_vernier_02`: AM-02 Vernier Fast-Actuators (190 HP, 10t, -5 MW) | +20% Weapon Handling [Aerosteel Flux]
- `am_adamant_03`: AM-03 Adamantine Heavy Brackets (320 HP, 22t, -6 MW) | +20% Ballistic Damage [Adamantine Carbide]
- `am_aerogel_04`: AM-04 Lunar Aerogel Manipulators (210 HP, 7t, -3 MW) | -55% Arm Mass, +25% Melee Speed [Lunar Aerogel]
- `am_tachyon_05`: AM-05 Tachyon Conduit Arms (240 HP, 12t, -7 MW) | +35% Energy Weapon Output [Tachyon Superalloy]

### 4.4 Legs (Hydraulics & Locomotion)
- `lg_vanguard_01`: LG-01 Vanguard Heavy Walkers (340 HP, 24t, -5 MW, 44 kph) | +30% Stability [Vanguard Composite]
- `lg_stratos_02`: LG-02 Stratos Vernier Skaters (220 HP, 15t, -7 MW, 86 kph) | +25% Agility [Aerosteel Flux]
- `lg_titan_03`: LG-03 Titan Quad-Leg Platform (440 HP, 34t, -8 MW, 34 kph) | +50% Recoil Absorb [Adamantine Carbide]
- `lg_aerogel_04`: LG-04 Lunar Aerogel Hover Struts (260 HP, 11t, -6 MW, 105 kph) | High-G Hover Dash [Lunar Aerogel]
- `lg_damascus_05`: LG-05 Damascus Armored Treads (520 HP, 32t, -7 MW, 48 kph) | Impenetrable Trench Fortress [Reactive Damascus]

### 4.5 Backpacks (Thrusters & Vernier Packs)
- `bp_heavy_01`: BP-01 Heavy Booster Pack (140 HP, 12t, -3 MW, +35 kph Boost) | High Thrust [Vanguard Composite]
- `bp_vernier_02`: BP-02 Dual-Vector Vernier Rig (100 HP, 8t, -6 MW, +65 kph Boost) | +15% Evade [Aerosteel Flux]
- `bp_plasma_03`: BP-03 Plasma Overcharge Booster (120 HP, 10t, -9 MW, +80 kph Boost) | +1 Dash AP [Hyperion Matrix]
- `bp_aerogel_04`: BP-04 Lunar Aerogel Siphon Rig (95 HP, 4t, -4 MW, +55 kph Boost) | +60% Heat Venting [Lunar Aerogel]
- `bp_tachyon_05`: BP-05 Tachyon Fold Warp Booster (130 HP, 11t, -12 MW, +115 kph Boost) | +2 Sortie AP & Micro-Warp [Tachyon Superalloy]

### 4.6 Weapons (Ordnance Hardpoints)
- `wp_vulcan_01`: WP-01 Rotary Vulcan (120mm) (100 HP, 12t, -3 MW, 180 Dmg) | Sustained Ballistic Fire [Adamantine Carbide]
- `wp_beam_02`: WP-02 Particle Beam Pulse Rifle (80 HP, 8t, -10 MW, 240 Dmg) | Armor Piercing Energy [Hyperion Matrix]
- `wp_rail_03`: WP-03 Heavy Siege Rail Cannon (130 HP, 20t, -8 MW, 380 Dmg) | Long Range Siege Kinetic [Adamantine Carbide]
- `wp_sol_04`: WP-04 Sol Ferrite Hyper-Railgun (150 HP, 22t, -11 MW, 460 Dmg) | +45% Shield Penetration [Sol Ferrite]
- `wp_tachyon_05`: WP-05 Tachyon Continuous Beam Lance (90 HP, 9t, -14 MW, 420 Dmg) | +40% Armor Melt [Tachyon Superalloy]

---

## 5. Custom Combinations Assembly Bay & Engineering Deck

The Assembly Bay (Tab 1, Subtab 2) provides an interactive 3-column tactical engineering deck:

```
+-----------------------------+------------------------------------+--------------------------------+
| 1. HARDPOINTS LOADOUT       | 2. WANZER CAD WIREFRAME            | 3. ENGINEERING CALCULUS        |
| (Width: 380px)              | (Width: 440px)                     | (Width: 410px)                 |
|                             |                                    |                                |
| [SLOT 1: HEAD SENSORS] < >  | +--- CAD REF: REF-07.24 ---------+ | Designation: CHIMERA-X         |
| [SLOT 2: TORSO REACTOR]< >  | |     [o] Head Socket            | | Presets: [AEGIS] [VALK] [TITAN]|
| [SLOT 3: ARMS ACTUATOR]< >  | |  [o]---[o]---[o] Arms / Core   | |                                |
| [SLOT 4: LEGS HYDRAULC]< >  | |        [o] Legs Socket         | | 1. ARMOR: 1,840 / 2,500 HP   |
| [SLOT 5: BACKPACK VERN]< >  | +--------------------------------+ | [||||||||||||||||||||..........] |
| [SLOT 6: PRIMARY WEAPN]< >  | Procedural Torso Alloy Tinting     | 2. TOKAMAK: Surplus +14 MW     |
|                             | Active Metallurgy Specs Plaque     | [||||||||||||||||||||||||||||] |
| Selected slot card glows    | Weight Class Assessment:           | 3. MOBILITY: 74t / 149 kph     |
| amber; clickable schematic. | [ MEDIUM MAINSTAY ]                | 4. WEAPON: Railgun 460 Dmg     |
|                             | Status: 6/6 HARDPOINTS SYNCED      |                                |
|                             |                                    | [>> COMMISSION INTO HANGAR <<] |
|                             |                                    | [★ SAVE CANONICAL BLUEPRINT]   |
+-----------------------------+------------------------------------+--------------------------------+
```

### 5.1 Real-Time Engineering Physics Calculus
1. **Tokamak Power Surplus Law:**
   `Net Power = Torso Output - sum(Part Power Draws)`
   If Net Power < 0, the system enters **Reactor Overload**. Commissioning is strictly locked out until the deficit is resolved.
2. **Mobility & Inertia Dynamics:**
   `Walk Speed = max(20, floor(Leg Base Speed * (1.0 - (Total Mass / 220.0))))`
   `Boost Speed = Walk Speed + Backpack Boost Bonus`
3. **Weight Class Classification:**
   - **`< 55 Tonnes`:** `LIGHT SKIRMISHER` (High Agility / +20% Evasion Rating)
   - **`55 – 84 Tonnes`:** `MEDIUM MAINSTAY` (Balanced Multi-Role Linebreaker)
   - **`85 – 109 Tonnes`:** `HEAVY ASSAULT` (Fortified Plating / Heavy Ordnance)
   - **`>= 110 Tonnes`:** `SUPERHEAVY SIEGEBREAKER` (Impenetrable Trench Line Fortress)
4. **Gihren's Greed Operational Telemetry:**
   - *Pilot Reaction Limit (Genkai %):* 100% to 195% scaling based on hydraulic calibration.
   - *Propellant Endurance (EN):* 100 to 240 EN pool dictating turn-based movement and boost sorties.
   - *ECM Dispersion:* Countermeasures scattering guided missile lock-ons.
   - *Terrain Ratings:* Ground (G), Space (S), Underground (U), Water (T).
5. **Canonical Blueprint Serialization:**
   - Pressing `[★ SAVE AS PMC CANONICAL BLUEPRINT]` generates a military model designation (e.g. `PMC-CHIMER-74`), registers the configuration in `obj_BlueprintManager`, and enables mass-production runs on factory assembly lines.

---

## 6. Prototyping Calibration Minigames

Located in Tab 0, Subtab 1, players can test and calibrate prototype assemblies to achieve **Masterwork Status** (Grades C through S-Tier):
1. **Magnetic Tokamak Containment:** Real-time containment ring stabilization. Players modulate magnetic containment solenoids to contain a fluctuating plasma vortex.
2. **Hydraulic Actuator Cadence:** Rhythmic pressure release timing to hone actuator response speed, boosting pilot reaction limit (*Genkai %*).
3. **Vernier Thruster Vectoring:** Aligning multi-axis exhaust verniers to maximize fuel-to-thrust efficiency and eliminate thermal dissipation hotspots.

---

## 7. Pilot Nemesis & Psychological Relationship System

The human element of mobile suit warfare is simulated through a persistent psychological network (`obj_NemesisManager`):

```
+----------------------------------------------------------------------------------+
|                          PILOT NEMESIS & EMOTIONAL WEB                           |
+----------------------------------------------------------------------------------+
|  FACTION PILOT ROSTER (Marcus Cole, Kira Dahl, Jax Vance, Sorren Hawke, etc.)    |
|  - Personality Traits (Stoic, Aggressive, Honorable, Mercenary, Idealist)       |
|  - Grudge Accumulators (0 to 100 PTS) tracking squad battle encounters           |
+----------------------------------------------------------------------------------+
          |                                                   |
          v                                                   v
+-----------------------------+             +--------------------------------------+
|  RELATIONSHIP ENGINE        |             |  PSYCHOLOGICAL BREAKDOWNS (TRAUMA)   |
|  - Friendship Referrals:    |             |  Triggered when a bonded comrade or  |
|    Hiring friends yields    |             |  star-crossed lover is killed:       |
|    25% salary discount.     |             |  - BERSERKER RAGE: +40% Atk, -50% Def|
|  - Star-Crossed Romance:    |             |  - DESPAIR COLLAPSE: -30% Evasion    |
|    Cross-faction lovers     |             |  - VENGEANCE STALKER: Priority target|
|    bonded in secret.        |             |  - CYNICAL APATHY: Refuses team AP   |
+-----------------------------+             +--------------------------------------+
                                            |
                                            v
                +---------------------------------------------------+
                |  PROCEDURAL AMBUSH INVASION ENGINE                |
                |  - Enemy nemeses with Grudge >= 70% calculate     |
                |    tactical drop-pod ambush probability during    |
                |    player sorties.                                |
                |  - Dynamic drop-pod atmospheric entry sequence.   |
                |  - Contextual ideological dialogue barks.         |
                +---------------------------------------------------+
```

---

## 8. Grand Isometric Tactical Combat Simulation

Implemented in `rm_combat` and driven by `obj_BattleManager`:
- **True Isometric 2:1 Projection:** Custom mathematical projection converting grid coordinates `(gx, gy, gz)` to screen space `(sx, sy)`.
- **Directional Armor Facings:** Every Mobile Suit tracks independent armor integrity for Front, Left Flank, Right Flank, and Rear facings. Rear strikes bypass standard kinetic deflection plates for critical damage.
- **Subsystem Limb Destruction:**
  - *Head Destroyed:* Radar loss, -40% accuracy, ECM disabled.
  - *Arm Destroyed:* Primary weapon destroyed, weapon handling halved.
  - *Legs Crippled:* Movement reduced to 1 tile, evasion drops to 0%.
  - *Torso Core Breach:* Fatal explosion dealing area-of-effect shrapnel damage.
- **Dynamic Ballistics:** Solid slugs, rotary chaingun streams, beam particle arcs, and swarm micro-missiles render with physics trajectories and collision detection.

---

## 9. Interstellar Geopolitics, Theaters & Contracts

### 9.1 The Four Warring Factions
1. **Terran Coalition:** Earth-sphere planetary government. Heavy doctrine favoring dense tungsten composite plating and massed kinetic artillery (*GHA-07 Ironclad*).
2. **Martian Syndicate:** High-speed orbital insurgent corporations. Agile skirmishers utilizing vernier thrusters and claw/pincer weapons (*SCR-12 Hyena*).
3. **Jovian Colonies League:** Radical orbital habitat alliance. Long-range beam particle optics and aerosteel flight mobility (*JCL-01 Aether*).
4. **Zaibatsu Conglomerate:** Mega-corporate arms cartel. High-frequency plasma blades and stealth cloaking technology (*ZBT-09 Muramasa*).

### 9.2 Fly-Off Procurement Trials (Tab 2, Subtab 1)
Instead of generic shops, factions host competitive defense procurement trials. Players select an ideological trial specification (e.g. *Terran Trench Defense Spec*), configure an prototype mecha combination, and compete against rival corporate prototypes across three combat rounds to win lucrative military mass-production defense contracts.

### 9.3 Interstellar Commodity Trade Exchange (Tab 2, Subtab 2)
A dynamic market simulation driven by active sector war frontlines:
- Raw minerals and synthesized alloys fluctuate based on supply, embargoes, and theater blockades.
- Buy low in Jovian mining colonies and sell high in contested Terran frontline siege sectors.

---

## 10. The Mobile Dreadnought Flagship ("The Archon")

Driven by `obj_GameManager` and detailed in `docs/24_dreadnought_vast_upgrade_tree_and_endgame_progression.md`:
- **8 Flagship Divisions:**
  1. *Fabrication Division:* Unlocks parallel manufacturing bays and fabrication speed multipliers.
  2. *Mining Siphon Array:* Passive automatic harvesting of raw elements (+15 kg/turn at Tier 5).
  3. *Defense Division:* Flagship hull expansion (up to 65,000 HP) and point-defense flak.
  4. *Weapons Division:* Tactical fire support and the apocalyptic *Doomsday Tachyon Cleaver*.
  5. *Propulsion Division:* Speed, sortie range, and the *Tachyon Fold Drive* (0-turn instantaneous warp).
  6. *Pilot Suite Division:* Holo-simulators, cybernetic medical recovery, and morale cohesion.
  7. *SigInt Recon Division:* Sector radar, ambush forewarning, and enemy blueprint espionage.
  8. *Command & Strategy Division:* Sortie command points (CP) and simultaneous contract capacity.
- **Ratified Flagship Doctrines:**
  - *Siege Fortress:* Hull HP quadrupled, heavy armor deflection.
  - *Fleet Vanguard:* +50% Sortie speed, +2 Tactical Action Points.
  - *Black Ops Syndicate:* Cloaking, diplomatic immunity, and +30% black-market trade arbitrage.

---

## 11. Technical Architecture & File Directory Map

```
MechMakerConcept/
├── objects/
│   ├── obj_GameManager/          # Persistent Master Singleton (Economy, turns, inventory, fleet)
│   ├── obj_HQTerminal/           # Unified Retro Command Deck UI & Event Controller
│   ├── obj_BlueprintManager/     # Blueprint registry, component specs, master tuning
│   ├── obj_NemesisManager/       # Relational pilot web, grudges, romance, drop-pod incursions
│   ├── obj_FactionManager/       # Faction AI diplomacy, frontline war map, reputation
│   ├── obj_BattleManager/        # Turn-based isometric combat controller, ballistics, limbs
│   └── obj_MobileSuit/           # Tactical unit instance in isometric combat room
├── scripts/
│   ├── scr_snes_ui/              # 16-bit SNES UI rendering engine (Panels, buttons, gauges)
│   ├── scr_alloy_color_synthesis/# Procedural metallurgy chromatics for 118 elements & alloys
│   ├── scr_alloy_discovery_codex/# Combinatorial metallurgy & procedural discovery engine
│   ├── scr_nemesis_system/       # Pilot trauma states, romance calculus, dialogue barks
│   ├── scr_isometric_math/       # True 2:1 isometric coordinate projection & depth sorting
│   └── scr_combat_projectiles/   # Ballistic, beam, and missile projectile physics
├── sprites/
│   ├── spr_snes_panel_corner/    # 16-bit beveled corner brackets & rivets
│   ├── spr_snes_hazard_stripe/   # Diagonal caution/warning hazard bars
│   ├── spr_snes_led_indicators/  # Segmented status LEDs
│   ├── spr_mech_schematic/       # 1024x576 CAD Wanzer chassis wireframe
│   ├── spr_comp_*/               # Heads, Torsos, Arms, Legs, Thrusters, Weapons
│   └── spr_ms_*/                 # Animated Mobile Suit combat sprites
└── docs/                         # Exhaustive technical design specifications
```

---

## 12. Verification & Automated Test Suites

The project includes strict automated Python test harnesses verifying GML token balancing, data schemas, mathematical models, and progression:
1. `tools/test_phase3_validation.py`: JSON schemas, GML token balance, Nemesis trauma calculus, friendship discounts.
2. `tools/test_phase4_validation.py`: Ambush probability curves, drop-pod incursion barks, multi-object syntax.
3. `tools/test_flagship_endgame_progression.py`: Flagship 8-division T1-T5 upgrade tree, Tachyon Cleaver scaling.
4. `tools/test_mech_building_and_alloys.py`: Sintering envelopes, 8-alloy chromatics, 30-part component catalog, custom assembly power/mass calculus, weight class classification, and blueprint serialization.

*All test suites pass with 100% verified integrity.*
5. `tools/test_corporate_competitions_and_pmc_squad.py`: PMC combat pedigree accumulation, fly-off conversion, arms dealer paradox (Doc 25).
6. `tools/test_competition_phases_adoption_and_refinement.py`: 4-phase tournament gauntlet, fleet tooling, Block II/III modernization (Doc 26).
7. `tools/test_competitor_rd_timeline_and_events.py`: 4 Tech Eras, competitor R&D branching, narrative event trees, dynamic battlefield encounters (Doc 27).
8. `tools/test_corporate_stock_and_faction_support.py`: Hostile takeovers, stock market tranches, bilateral faction tactical support/hindrance, Brig interrogation loop, Sol Monopoly victory (Doc 28).
9. `tools/test_expanded_mobile_suits_and_mass_production.py`: Mass-production candidate pools, seed randomization, procedural doctrine variance (Doc 29).
10. `tools/test_100_mobile_suits_and_universal_animation.py`: 100-chassis catalog schema validation, 16 candidate multi-frame animated sprites, universal isometric animation engine, interactive encyclopedia in HQTerminal (Doc 30).
11. `tools/test_milestone_51_rpg_and_prologue.py`: Space Salvager Origin Questionnaire, GHA-00 Genesis Prototype Interactive Ambush Sortie, Retro 16-Bit VN Episode Engine, and Dedicated [6] PILOTS Command Deck (Doc 51).
12. `tools/test_milestone_52_reactive_vn_dialogue.py`: Reactive Geopolitical Visual Novel & Multi-Leader Dialogue Engine, Dynamic Salutations, Multi-Speaker War Room Summits, Tactical Radio Intercom Barks (Doc 52).
13. `tools/test_milestone_53_dramatis_personae_and_bible.py`: 10 Major Character Dossiers, 4-Tier Emotion Specifications, Master Dialogue Bible Branching Trees, In-Engine Emotion Rendering, and In-Combat Tactical Radio Duel Barks (Doc 53).
14. `tools/test_milestone_54_war_ceasefire_and_trade_cutscenes.py`: Inter-Faction War Declarations, Brokered Armistices, Direct Strategic Player Trade, and Rival Corporate Contract Interceptions (Doc 54).
15. `tools/test_milestone_55_bonds_interrogations_and_incursions.py`: Base Brig POW Interrogations, Cantina Crew Bonds, Mid-Battle Tactical Radio Incursions, Interactive Directives & PMC Karma Alignment (Doc 55).
16. `tools/test_milestone_56_stats_fatigue_and_traits.py`: Manual Stat Point Allocation on Level-Up, Cockpit Sortie Fatigue & Sortie Rotation Stress, Rest & Recuperation (R&R) Leave, and Dynamic Battle Scar Trait Mutations (Doc 56).

---

## 13. System Lineage Documentation Index
- **Doc 01**: [01_core_architecture.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/01_core_architecture.md): Core Simulation Architecture, Singleton Patterns & Main Loop.
- **Doc 02**: [02_alloy_chemistry.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/02_alloy_chemistry.md): Alloy Chemistry, Metallurgy & Crucible Thermodynamics.
- **Doc 03**: [03_prototyping_minigames.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/03_prototyping_minigames.md): Prototyping Minigames, Quality Sintering & Calibration Tolerances.
- **Doc 04**: [04_faction_contracts.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/04_faction_contracts.md): Faction Contracts, Reputation Scales & Sovereign Procurement Demands.
- **Doc 05**: [05_tactical_combat.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/05_tactical_combat.md): Turn-Based Isometric Tactical Combat Architecture.
- **Doc 06**: [06_resource_operations.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/06_resource_operations.md): Strategic Resource Nodes, Mining Outposts & Refineries.
- **Doc 07**: [07_base_management.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/07_base_management.md): Base Facilities, Foundry Crucibles & Assembly Bays.
- **Doc 08**: [08_narrative_events.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/08_narrative_events.md): Narrative Events, Dilemmas & Geopolitical Ramifications.
- **Doc 09**: [09_ui_ux_flow.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/09_ui_ux_flow.md): 16-Bit SNES UI/UX Command Terminal & Visual Architecture.
- **Doc 10**: [10_factions_and_mecha_lineage.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/10_factions_and_mecha_lineage.md): Interstellar Factions & Canonical Mobile Suit Lineage.
- **Doc 11**: [11_faction_bases_and_strategic_theaters.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/11_faction_bases_and_strategic_theaters.md): Faction Strongholds & Strategic Orbital Theaters.
- **Doc 12**: [12_sandbox_and_endgame_systems.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/12_sandbox_and_endgame_systems.md): Sandbox Economy, Territory Conquest & End-Game Loops.
- **Doc 13**: [13_modular_parts_and_assembly_system.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/13_modular_parts_and_assembly_system.md): Modular Chassis Components & Assembly Bay Engineering.
- **Doc 14**: [14_procedural_materials_and_deep_metallurgy.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/14_procedural_materials_and_deep_metallurgy.md): Procedural Materials, Element Periodic Table & Synthesis.
- **Doc 15**: [15_turn_based_economy_trade_and_procurement_trials.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/15_turn_based_economy_trade_and_procurement_trials.md): Turn-Based Commodity Exchange & Procurement Trials.
- **Doc 16**: [16_qa_campaign_playthrough_audit_and_error_catalog.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/16_qa_campaign_playthrough_audit_and_error_catalog.md): Campaign Playthrough QA Audit, Bug Matrix & Exploit Triage.
- **Doc 17**: [17_grand_scale_isometric_combat_system.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/17_grand_scale_isometric_combat_system.md): Grand-Scale Isometric Combat & Multi-Unit Formations.
- **Doc 18**: [18_canonical_mobile_suit_blueprints_and_doctrine_balance.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/18_canonical_mobile_suit_blueprints_and_doctrine_balance.md): Canonical Blueprints & Combat Doctrine Balancing.
- **Doc 19**: [19_pilot_nemesis_system_and_character_relationships.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/19_pilot_nemesis_system_and_character_relationships.md): Pilot Nemesis Grudge System & Relational Dynamic Lore.
- **Doc 20**: [20_mech_building_minigames_and_comprehensive_combat_stats.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/20_mech_building_minigames_and_comprehensive_combat_stats.md): Fabrication Bay Minigames & Full Combat Statistics.
- **Doc 21**: [21_faction_ai_diplomacy_and_interstellar_war_system.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/21_faction_ai_diplomacy_and_interstellar_war_system.md): Faction AI Diplomacy, Bilateral Matrix & Interstellar War.
- **Doc 22**: [22_qa_systems_stress_audit_and_exploit_catalog.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/22_qa_systems_stress_audit_and_exploit_catalog.md): Systems Stress Audit, Boundary Safety & Exploit Catalog.
- **Doc 23**: [23_pre_war_experimental_warship_and_rival_manufacturers.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/23_pre_war_experimental_warship_and_rival_manufacturers.md): Pre-War Experimental Warship Hephaestus & Rival Conglomerates.
- **Doc 24**: [24_dreadnought_vast_upgrade_tree_and_endgame_progression.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/24_dreadnought_vast_upgrade_tree_and_endgame_progression.md): 40-Tier Dreadnought Refits & Specialization Protocols.
- **Doc 25**: [25_mobile_suit_corporate_competitions_and_pmc_squad_doctrine.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/25_mobile_suit_corporate_competitions_and_pmc_squad_doctrine.md): Corporate Competitions, Tournament Trials & Doctrine.
- **Doc 26**: [26_competition_phases_adoption_and_refinement.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/26_competition_phases_adoption_and_refinement.md): 4-Phase Fly-Off Trials, Faction Adoption & Royalties.
- **Doc 27**: [27_competitor_rd_timeline_eras_and_random_events.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/27_competitor_rd_timeline_eras_and_random_events.md): Competitor R&D Timelines, 4 Eras & Crisis Incursions.
- **Doc 28**: [28_nemesis_corporate_contracts_faction_support_and_hostile_takeovers.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/28_nemesis_corporate_contracts_faction_support_and_hostile_takeovers.md): Hostile Corporate Takeovers, Equity Stakes & Stock Market.
- **Doc 29**: [29_expanded_mobile_suit_universe_mass_production_variance_and_animation.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/29_expanded_mobile_suit_universe_mass_production_variance_and_animation.md): Dynamic Mass-Production Variance & Isometric Animation.
- **Doc 30**: [30_master_mobile_suit_universe_encyclopedia_and_procedural_procurement.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/30_master_mobile_suit_universe_encyclopedia_and_procedural_procurement.md): 100-Chassis Master Encyclopedia & Procedural Procurement.
- **Doc 31**: SNES Front Mission Multi-Unit Isometric Combat System
- **Doc 32**: Grand Isometric Tactical Combat, Multi-Map Theaters & Chassis Deployment (Dual Platoon Formations, 4-Directional Isometric Map Models, Dynamic Earth & Space Theaters, Pre-Battle Hangar Staging Deck) (Platoon-Scale 2:1 Axonometric Battlefield, 4-Part Modular Damage, On-Map Firing Animations, Part-Targeting Duel Forecast & 16-Bit Retro UI).
- **Doc 33**: Tactical Audio System Architecture, Mechanical Foley Soundscapes & High-Detail Pilot Portrait Assets.
- **Doc 34**: Player Commander Profile Creation, Prologue Scenario Briefing & Atmospheric Backdrops.
- **Doc 35**: Mobile Suit Military Lore, Global Production/Casualty Telemetry & Dynamic Playthrough Chronicle.
- **Doc 36**: Faction Ideologies, Geopolitical Stances, AI State Machines & Dynamic Contract Scaling.
- **Doc 37**: Deep Space Astran League & Martian Machine Consensus Lineage Integration.
- **Doc 38**: The Prometheus Catalyst: Conventional Warfare Ecosystem & Mobile Suit Genesis.
- **Doc 39**: Planetary & Orbital Territory Conquest: 3-Theater Grand Strategic Hex Wargame.
- **Doc 40**: System Settings, Audio Director, SFX/BGM Volumes & Operational Command Manual.
- **Doc 41**: Modular Equipment Tech Tree, Cross-Disciplinary Research Nodes & R&D Licensing.
- **Doc 42**: Strategic Logistics, Tritium Burn, Pilot Convalescence & Flagship Celestial Operations (Goals A, B, C).
- **Doc 43**: S-Grade Masterwork Prototyping Bay Tuning & 4 Campaign Victory Path Conditions (Goal D).
- **Doc 44**: Corporate Espionage Engine, Black-Ops Shadow Raids & Base Detention Brig (Goal E).
- **Doc 45**: Tactical Ballistics Polish: Elevation Line-of-Sight, Suppression Pinning & Dynamic Cover Annihilation (Goal F).
- **Doc 46**: Apex Crisis Boss Sortie: Deus-Machina Phase Barrier & USN-X Orbital Strike (Goal G).
- **Doc 47**: Production Polish, Hotkey Navigation, Memory Safety & 200-Turn Campaign Stability.
- **Doc 48**: Tactical Combat Visual Concepts, In-Game Mockups & Dual-Layer Staging Architecture.
- **Doc 49**: Modular Combat Clash & Dynamic Mecha Animation Engine: Hybrid Bone Sockets, Procedural Metallurgy Swatches, 4-Class Weapon Choreography, Persistent Tactical Battle Scars & Retro CRT Cockpit Telemetry HUD.
- **Doc 50**: First Playable Alpha, Tutorial Mission & Campaign Onboarding Pipeline: 5-Step Operational Cadre (Operation Groundwork), Ergonomic 1-5 Quick-Key Deck Architecture, Pulsing Highlight Brackets, Diegetic Radio Directives, Tactical Combat Guidance & State Persistence.

- **Doc 51**: RPG Systems, Faction Dialogue & Prologue Architecture: Space Salvager Origin Questionnaire, GHA-00 Genesis Prototype Interactive Ambush Sortie, Retro 16-Bit VN Episode Engine, and Dedicated [6] PILOTS Command Deck.
- **Doc 52**: Reactive Geopolitical Visual Novel & Multi-Leader Dialogue Engine: Dynamic Salutations across 5 Mental Mood States, Contextual Incident Barks & Token Interpolation, Multi-Speaker War Room Summits (Dual-Portrait Presentation: Phobos Blockade, Transhumanist Schism, Sol Monopoly), and Tactical Radio Comms Intercom in rm_combat.
- **Doc 53**: [53_dramatis_personae_character_profiles_and_master_dialogue_bible.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/53_dramatis_personae_character_profiles_and_master_dialogue_bible.md): Dramatis Personae Character Profiles, 4-Tier Emotion Specifications (NORMAL, ANGRY, DESPERATE, SMUG), Master Dialogue Bible & Branching Decision Trees: Comprehensive dossiers for 10 central actors (General Vance, Director Rostova, Chairman Sato, Archon Sideris, Consensus Node 0-Prime, Commander Delgado, Vaelen Gray, Linus Gable, Kaelen Voss, Dr. Soren), lighting/palette/facial guidelines, moral dilemmas, ideological consequence matrices, secret narrative unlocks, and in-combat radio duel protocols.
- **Doc 54**: [54_geopolitical_warfare_ceasefires_and_corporate_trade_cutscenes.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/54_geopolitical_warfare_ceasefires_and_corporate_trade_cutscenes.md): Geopolitical Warfare, Ceasefires & Corporate Trade Cutscenes Engine: Inter-faction war declarations (Terran vs Colony, Zaibatsu vs Tharsis, Syndicate vs Sidereal), high-tension brokered armistices (Geneva Concordat & Arsia Mons Data Accord), direct diplomatic player trade delegations (Coalition Ordnance Procurement & Jovian Black Market Vault), and rival megacorporation trade undercuts (Valkyrie Heavy mega-contract interception & Hyperion Tactical black-ops contraband raid).
- **Doc 55**: [55_tactical_interrogations_cantina_bonds_and_mid_battle_incursions.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/55_tactical_interrogations_cantina_bonds_and_mid_battle_incursions.md): Tactical Interrogations, Cantina Bonds & Mid-Battle Incursions Engine: Interactive Base Brig POW triage (`ep_brig_interrogation_ace`), flagship cantina crew bond conversations (`ep_cantina_bond_vance`, `ep_cantina_bond_soren`, `ep_cantina_bond_kovacs`), mid-battle tactical radio incursions with 3 interactive combat directives (Orbital Barrage, Focus Telemetry, Neuro-Jamming), and PMC Ideological Karma Alignment tracking (Noble Peacekeeper, Corporate Pragmatist, Bloodhound War Profiteer).
- **Doc 56**: [56_advanced_character_stats_fatigue_and_trait_mutations.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/56_advanced_character_stats_fatigue_and_trait_mutations.md): Advanced Character Stats, Pilot Fatigue & Trait Mutation Engine: Manual Stat Point Allocation on Level-Up (+2 points per level-up boundary crossing of 150 XP into Accuracy, Reflexes, Combat, or Tactics), Cockpit Sortie Fatigue (+25 per sortie, +40 on core breach/ejection) with tiered combat accuracy penalties (Winded -5%, Fatigued -10%, Exhausted -20%), passive fatigue dissipation (-25 per rest turn) and Cantina Rest & Recuperation (R&R) Shore Leave (-5,000 Cr to clear fatigue and boost morale), and permanent Battle Scar Trait Mutations ("Iron Survivor", "Ace Predator", "Ghost of Phobos", "Cybernetic Reflex Augment").
