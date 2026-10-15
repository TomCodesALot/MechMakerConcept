# DOC-30: Master Mobile Suit Universe Encyclopedia (100-Chassis), Mass-Production Procurement Variance & Universal Animation Integration

## Executive Overview
Following the geopolitical escalation across the Sol System, warfare has evolved from localized boundary skirmishes into total industrialized conflict. **Doc-30** expands the Mobile Suit Universe to **exactly 100 canonical, lore-grounded mobile suits** across four technological eras and four major geopolitical factions, accompanied by proprietary PMC designs and pre-war derelicts.

Furthermore, Doc-30 formalizes the **Playthrough Mass-Production Procurement Variance Engine**, wherein every campaign procedural seed ratifies one of four competing candidate line chassis for each faction. Combined with the **Universal Isometric Animation Engine**, every mobile suit features 160x160 multi-frame animation states (Standby Idle, Vernier Pulse, Stride Walk, Weapon Discharge with muzzle flare, and Kinetic Hit Stagger).

---

## 1. The 100-Chassis Sol System Lineage Matrix

### 1.1 Faction Distribution Breakdown
```
+----------------------------------------------------------------------------------------------------------------+
| FACTION                        | COUNT | TECH ERAS          | PRIMARY DOCTRINE / INDUSTRIAL PHILOSOPHY        |
+--------------------------------+-------+--------------------+-------------------------------------------------+
| Terran Coalition               | 25    | Eras 1, 2, 3, 4    | Kinetic Trench Walls, Heavy Artillery, Bastions |
| Outer Colonies (Jovian)        | 23    | Eras 1, 2, 3, 4    | High-Vernier Zero-G, Particle Beams, EW Skirmish|
| Rogue Cartel Syndicates        | 25    | Eras 1, 2, 3, 4    | Slag Armor, Harpoon Boarders, Ambush Guerillas  |
| Apex Bio-Zaibatsu              | 23    | Eras 1, 2, 3, 4    | Tachyon Katanas, EMP Fans, Sub-Drone Carriers   |
| Player PMC Proprietary Hangar  | 4     | Eras 2, 3          | Modular Sintered Hardpoints, Vanguard Doctrine  |
+--------------------------------+-------+--------------------+-------------------------------------------------+
| TOTAL SOL SUIT UNIVERSE        | 100   | Eras 1 to 4        | 100% Fully Specified Canonical Chassis          |
+--------------------------------+-------+--------------------+-------------------------------------------------+
```

### 1.2 Technological Eras
- **Era 1 (Pre-War & Boundary Wars)**: Heavy kinetic ballistic chassis, single-chamber fission reactors, early hydraulic servos, and ancient lost-tech archetypes (e.g., Pre-War Hephaestus Sentinel, Chronos Vector).
- **Era 2 (Early War / Sol Schism)**: Standardized military mass-production, vernier thruster skirts, early particle beam weaponry, and improvised frontier rebel units.
- **Era 3 (Mid War / Corporate Escalation)**: Heavy composite alloy sintering, smart-munition sub-drones, high-frequency melee weaponry, and customized ace platforms (Marcus Cole, Nadia Cruz, Jax Vance, Renzo Takahashi).
- **Era 4 (Apex Crisis / Forbidden Prototypes)**: Unshackled bio-neural links, tachyon beam singularities, 100-ton walking superheavy bastions (Valkyrie Titan Juggernaut), and planetary siege leviathans.

---

## 2. Mass-Production Playthrough Procurement Variance

### 2.1 The 16 Candidate Line Chassis
Each major faction possesses four candidate chassis competing for standard service procurement:

```
+-------------------+----------------------------+-----------------------+----------------------------------+------------------------------+
| FACTION           | CANDIDATE DESIGNATION      | CHASSIS CLASS         | SIGNATURE ARMAMENT               | DEDICATED SPRITE ASSET       |
+-------------------+----------------------------+-----------------------+----------------------------------+------------------------------+
| Terran Coalition  | 1. GHA-07 Ironclad         | Heavy Assault Wall    | Type-77 120mm Autocannon         | spr_ms_ironclad_idle         |
|                   | 2. TH-M04 Ballista         | Quadruped Artillery   | Twin 200mm Heavy Howitzers       | spr_ms_ballista_idle         |
|                   | 3. TH-C02 Centurion        | Hydraulic Linebreaker | GAU-88 Rotary Heavy Vulcan       | spr_ms_centurion_idle        |
|                   | 4. TH-T09 Trenchcoat       | CQB Breacher          | 12ga Heavy Slug Autoshotgun      | spr_ms_trenchcoat_idle       |
+-------------------+----------------------------+-----------------------+----------------------------------+------------------------------+
| Outer Colonies    | 1. AET-01 Aether           | Zero-G Interceptor    | Twin Beam Carbines               | spr_ms_aether_idle           |
|                   | 2. JCC-Z05 Zephyr          | EW Sensor Jammer      | Pulse Laser Array & Jammer       | spr_ms_zephyr_idle           |
|                   | 3. JCC-K02 Kepler          | Orbital Rail-Sniper   | Magnetic Linear Rail-Rifle       | spr_ms_kepler_idle           |
|                   | 4. JCC-O08 Oberon          | Fleet Escort Guardian | Thermal Beam Lance & PD Emitters | spr_ms_oberon_idle           |
+-------------------+----------------------------+-----------------------+----------------------------------+------------------------------+
| Ares Syndicates   | 1. SCR-12 Hyena            | Harpoon Scavenger     | Magnetic Harpoon & 80mm Flak     | spr_ms_hyena_idle            |
|                   | 2. ARC-G04 Gorgon          | Boarding Cutter       | Heavy Thermal Cutter Claw        | spr_ms_gorgon_idle           |
|                   | 3. ARC-B06 Bloodhound      | Wheeled Pack Hunter   | Quad 70mm Rocket Pods            | spr_ms_bloodhound_idle       |
|                   | 4. ARC-V03 Vandal          | Ambush Shrapnel Mecha | Flechette Autogun & Decoy Flares | spr_ms_vandal_idle           |
+-------------------+----------------------------+-----------------------+----------------------------------+------------------------------+
| Cyber-Zaibatsu    | 1. ZAI-03 Muramasa         | Tachyon Duelist       | High-Frequency Tachyon Katana    | spr_ms_muramasa_idle         |
|                   | 2. ZBT-K07 Kage            | Optical Camo Assassin | Hyper-Velocity Needle Railgun    | spr_ms_kage_idle             |
|                   | 3. ZBT-R04 Ronin           | Sub-Drone Carrier     | Drone Swarm Pod & Naginata       | spr_ms_ronin_idle            |
|                   | 4. ZBT-T09 Tessen          | EMP Neural Deflector  | Broadband EMP Disruptor Emitter  | spr_ms_tessen_idle           |
+-------------------+----------------------------+-----------------------+----------------------------------+------------------------------+
```

### 2.2 Procedural Impact on Campaign Ecosystem
1. **Dynamic Tactical Battlefield Spawns**: When deploying into tactical combat, allied and hostile frontline units inherit the visual sprite, callsigns, armor profiles, and weapon loadouts of the active mass-production models.
2. **Fly-Off Arena Benchmarks**: To overturn a faction contract and secure recurring royalties, the player PMC must surpass the exact mechanical specs of that seed active incumbent.
3. **Salvage & Metallurgy Economy**: Defeating active line suits yields distinct alloy types (e.g. tungsten carbide from Ironclads, titanium aluminide from Aethers, scrap composites from Hyenas, silicon carbide from Muramasas).

---

## 3. Universal Isometric Animation Engine (`scr_draw_animated_mobile_suit`)

### 3.1 Animation Standards
- **Grid Layout**: 160x160 3/4 isometric projection.
- **Desynchronized Multi-Frame Cycling**: Idle frames cycle at 250ms intervals offset by unique chassis seeds, preventing unnatural synchronized marching.
- **Dynamic Reactor Core Glow**: Faction-tailored pulsating emissive glows (Amber for Terran, Cyan for Colony, Blaze for Syndicate, Neon Green for Zaibatsu, Gold for PMC).
- **Combat Feedback Offsets**:
  - `fire`: 4px weapon blowback recoil offset, dynamic muzzle flare flash and core bloom.
  - `hit`: High-frequency jitter shake, armor deflection flash, and directional angular stagger.
  - `walk`: Heavy bipedal/quadruped stride cycle with vertical torso stabilization bob.

---

## 4. Interactive Terminal Suite Integration
- **`obj_GameManager`**: Manages master catalog memory, procedural mass-production selection rolls, and relational querying.
- **`obj_FactionManager`**: Handles bilateral faction contracts, incumbent specifications, and modernization upgrade blocks.
- **`obj_BattleManager`**: Deploys dynamic tactical squads with animated sprites and weapon projectiles.
- **`obj_HQTerminal`**: Renders the complete 100-suit interactive encyclopedia and procurement candidate comparison suite.
