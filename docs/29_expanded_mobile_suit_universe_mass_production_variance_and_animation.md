# DOC-29: Expanded Mobile Suit Universe, Mass-Production Playthrough Variance, and Universal Animation Engine

## Executive Overview
In the gritty geopolitical mecha warfare of the Sol System, military dominance hinges upon mass-production doctrine. Historically, games in the genre often relegate grunt units to static, predetermined models. **Doc-29** expands the Mobile Suit Universe to **76 distinct canonical mobile suits** across four tech eras and four geopolitical factions, and introduces the **Playthrough Mass-Production Procurement Variance Engine**.

In each playthrough, every major military faction evaluates four competing mass-production candidate suits and ratifies one as its standard-issue line chassis. This procedural doctrine selection ripples throughout the entire game: altering battlefield encounter compositions, tactical damage profiles, salvage economies, and the precise mechanical thresholds required for the player's PMC to overturn the military contract and replace the incumbent suit.

---

## 1. The Playthrough Mass-Production Variance Architecture

### 1.1 Procurement Doctrine Matrix (16 Candidate Line Chassis)
Every military faction maintains a procurement pipeline consisting of four distinct mass-production candidate designs. When a new campaign begins (or via a procedural world seed), each faction ratifies ONE candidate as its standard service chassis.

```
+-------------------------------------------------------------------------------------------------------+
|                                FACTION MASS-PRODUCTION CANDIDATE MATRIX                              |
+-------------------+---------------------------+-----------------------------------+-------------------+
| FACTION           | CANDIDATE DESIGNATION     | DOCTRINE / TACTICAL ROLE          | SIGNATURE WEAPON  |
+-------------------+---------------------------+-----------------------------------+-------------------+
| Terran Coalition  | 1. GHA-07 Ironclad        | Kinetic Trench Fortress           | Type-77 120mm     |
|                   | 2. TH-M04 Ballista        | Quadruped Long-Range Artillery    | Twin 200mm Howitzer|
|                   | 3. TH-C02 Centurion       | Hydraulic Linebreaker Spearhead   | GAU-88 Vulcan     |
|                   | 4. TH-T09 Trenchcoat      | CQB Breacher & Smokescreen        | 12ga Slug Shotgun |
+-------------------+---------------------------+-----------------------------------+-------------------+
| Outer Colonies    | 1. AET-01 Aether          | Zero-G High-Vernier Interceptor   | Twin Beam Carbine |
|                   | 2. JCC-Z05 Zephyr         | EW Sensor Skirmisher & Jammer     | Pulse Laser Array |
|                   | 3. JCC-K02 Kepler         | Deep-Space Linear Rail-Sniper     | Magnetic Rail-Rifle|
|                   | 4. JCC-O08 Oberon         | Point-Defense Fleet Escort        | Thermal Beam Lance|
+-------------------+---------------------------+-----------------------------------+-------------------+
| Ares Syndicates   | 1. SCR-12 Hyena           | Scrap-Plated Harpoon Scavenger    | Harpoon Tether Gun|
|                   | 2. ARC-G04 Gorgon         | Boarding Cutter & Thermal Ram     | Plasma Pile-Driver|
|                   | 3. ARC-B06 Bloodhound     | High-Speed Wheeled Pack Hunter    | Quad Rocket Pods  |
|                   | 4. ARC-V03 Vandal         | Ambush Rail-Shotgun & Decoy       | Flechette Autogun |
+-------------------+---------------------------+-----------------------------------+-------------------+
| Cyber-Zaibatsu    | 1. ZAI-03 Muramasa        | High-Frequency Tachyon Duelist    | Katana Monoblade  |
|                   | 2. ZBT-K07 Kage           | Optical Camo Infiltrator          | Needle Rail-Sniper|
|                   | 3. ZBT-R04 Ronin          | Autonomous Sub-Drone Carrier      | Drone Swarm Node  |
|                   | 4. ZBT-T09 Tessen         | Neural-Jammer & Beam Deflector    | EMP Pulse Emitter |
+-------------------+---------------------------+-----------------------------------+-------------------+
```

### 1.2 Gameplay Consequences of Mass-Production Selection
1. **Frontline Patrol Formations**: If the Terran Coalition ratifies the `TH-M04 Ballista`, player missions against Terran forces feature heavy quadruped artillery barrages from across the map rather than Ironclad brawlers.
2. **Salvage & Alloy Drops**: Defeating a `ZBT-K07 Kage` line drops stealth optical prism glass and sensory cyberware, whereas defeating an `Ironclad` drops dense tungsten-carbide armor plates.
3. **PMC Replacement Contract Requirements**: To win the multi-million credit Mass-Production Replacement Contract, the player's prototype must exceed the specific benchmark stats of the active incumbent. Replacing an artillery suit demands superior counter-battery range, while replacing a high-vernier interceptor demands high evasion and cooling efficiency.

---

## 2. Master Mobile Suit Universe Catalog (76 Canonical Chassis)

The catalog is divided across four factions and four technological eras:
- **Era 1 (Pre-War / Boundary Clashes)**: Heavy kinetic ballistic chassis, primitive hydraulic servos, single-chamber fission reactors.
- **Era 2 (Early War / Sol Schism)**: Standardized military mass-production, vernier thruster arrays, early particle beam prototypes.
- **Era 3 (Mid War / Corporate Escalation)**: Heavy composite armor sintering, smart-munition sub-drones, high-frequency melee blades.
- **Era 4 (Apex Crisis / Forbidden Prototypes)**: Unshackled bio-neural jacks, tachyon particle projectors, planetary siege dreadnoughts.

---

## 3. Universal Mobile Suit Animation Engine

### 3.1 Frame Standards (160x160 Isometric Perspective)
Every mobile suit utilizes a standard 160x160 isometric frame layout with six key animation sub-images:
- **Sub-Image 0: Standby Idle (Frame A)** - Neutral combat stance, reactor idling.
- **Sub-Image 1: Standby Idle (Frame B)** - Exhaust venting, reactor glow pulse, micro-vernier flickers.
- **Sub-Image 2: Stride Walk (Frame A)** - Left leg/track forward stride, torso stabilization bob.
- **Sub-Image 3: Stride Walk (Frame B)** - Right leg/track forward stride, weapon stabilization dip.
- **Sub-Image 4: Attack Fire** - Primary weapon discharge, barrel blowback recoil, muzzle flare.
- **Sub-Image 5: Impact Recoil / Stagger** - Kinetic shock wave, armor deflection sparks, torso twist.

### 3.2 Dynamic Procedural Animator (`scr_draw_animated_mobile_suit`)
For custom mechs and catalog variants, `scr_draw_animated_mobile_suit` combines:
1. Base sprite archetype (`ironclad`, `ballista`, `aether`, `zephyr`, `hyena`, `gorgon`, `muramasa`, `kage`).
2. Faction-specific palette shading.
3. Sub-image cycle driven by instance state (`MS_STATE.IDLE`, `MS_STATE.WALK`, `MS_STATE.FIRE`, `MS_STATE.HIT`).
4. Procedural thruster emission glow (`sin(current_time / 100)`).
5. Dynamic recoil shake offsets during weapon fire and incoming hits.

---

## 4. Integration Specifications for Coding & QA Teams
- **`obj_GameManager`**: Stores `mobile_suit_catalog` containing all 76 chassis structs, and initializes `roll_playthrough_mass_production_line()`.
- **`obj_FactionManager`**: Dynamically binds `mass_production_contracts` to the selected candidates.
- **`obj_BattleManager`**: Spawns OPFOR and allied patrol squads reflecting the active mass-production suits.
- **`obj_HQTerminal`**: Displays animated visual previews and tactical dossiers for all candidate suits.
