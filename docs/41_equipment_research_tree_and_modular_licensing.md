# 41. Equipment Research Tech Tree, Doctrinal Divergence & Modular Blueprint Licensing
**Document Version:** 1.0.0  
**Roles:** Lead Game Designer (Director GDD), GameMaker Coder, Lead QA Engineer  
**Target Engine:** GameMaker Studio 2 (Modern GML)  
**Aesthetic & Mechanics Baseline:** *Hearts of Iron IV* (Concurrent Project Slots, Strategic Turns), *Front Mission* (Wanzer Modular Assembly), *Gihren's Greed* (Doctrinal Divergence & Arms Race)

---

## 1. Executive Summary: The Industrial-Military Equipment Loop

In *MechMakerConcept*, technology is not an abstract linear ladder of "+5% damage" spreadsheet upgrades. It directly links the PMC's **tactical battlefield salvage**, **crucible metallurgical chemistry**, **strategic calendar turn R&D**, and **custom 6-slot modular mobile suit assembly**:

$$\text{Tactical Wreckage / Intel} \longrightarrow \text{Crucible Alloys} \longrightarrow \text{Strategic R&D Tree (HOI4)} \longrightarrow \text{Licensed Modular Forge} \longrightarrow \text{Custom Hangar Assembly}$$

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │                  THE INDUSTRIAL R&D EQUIPMENT PIPELINE                 │
   └───────────────────────────────────┬────────────────────────────────────┘
                                       │
     [1. MINING & SALVAGE]             │  Contested orbital nodes / 45% Black Box Salvage drop
     [2. CRUCIBLE METALLURGY]          │  Sinter base elements into proprietary alloys
                                       ▼
 ┌──────────────────────────────────────────────────────────────────────────┐
 │ 4 DOCTRINAL SPHERES (3-5 Concurrent Research Slots // Calendar Turns)   │
 │ • 1. KINETIC & BALLISTICS  : Autocannons, Smoothbore Rifles, Railguns    │
 │ • 2. ENERGY & REACTORS     : Fission, He-3 Fusion, Tokamaks, Beam Rifles │
 │ • 3. CHASSIS & DEFENSE     : Bucklers, Reactive Armor, I-Fields, Forcefield│
 │ • 4. MOBILITY & VERNIERS   : Hydraulics, RCS Verniers, Skater Struts, Radome│
 └─────────────────────────────────────┬────────────────────────────────────┘
                                       │
         ┌─────────────────────────────┴─────────────────────────────┐
         ▼                                                           ▼
 ┌───────────────────────────────┐           ┌───────────────────────────────┐
 │   ABSTRACTED FLEET UPGRADES   │           │  MODULAR BLUEPRINT LICENSING  │
 │ • All active field suits gain │           │ • 30 Modular parts (6 slots)  │
 │   immediate passive combat    │           │   unlocked in Part Forge      │
 │   stat bonuses (no refit pain)│           │ • Blocked by [R&D REQUIRED]   │
 └───────────────────────────────┘           └───────────────────────────────┘
                                       │
                                       ▼
 ┌──────────────────────────────────────────────────────────────────────────┐
 │ MUTUALLY EXCLUSIVE DOCTRINE FORKS (Permanent Playthrough Commitment)     │
 │ • Railgun Line-Pierce vs Tachyon Mega-Beam Lance                         │
 │ • Antimatter Infinite AP Core vs Tachyon Cyclotron Fortress Core         │
 │ • Explosive Reactive Plating vs I-Field Energy Deflection Field          │
 │ • Magnetic Phase Barrier vs Damascus Adamantine Bulwark                  │
 │ • Nanite Coolant Loop vs High-G Vector Overboost Rig                     │
 └──────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Mechanics

### 2.1 Unified Blueprint Licensing
Researching an R&D node accomplishes two distinct outcomes:
1. **Fleet Combat Effect:** Applies global passive stat multipliers (`kinetic_dmg`, `beam_dmg`, `ap_max`, `evasion`, `hit_accuracy`, `move_range`, `barrier_absorb`) across all fielded units in tactical isometric combat (`obj_BattleManager`).
2. **Modular Forge License:** Unlocks corresponding modular component blueprints in the Modular Part Forge (`obj_HQTerminal`), allowing physical production from raw synthesized alloys and credits.

### 2.2 Doctrinal Divergence & Mutually Exclusive Forks
At mid-to-high tiers, engineers must choose between mutually exclusive design philosophies. Once a divergent doctrine is commenced or researched, opposing nodes are marked as **`DOCTRINE ABANDONED`** permanently for that campaign playthrough:

| Doctrinal Branch | Fork A (Aggressive / Kinetic / Agile) | Fork B (Technological / Energy / Heavy) | Tactical Trade-Off |
| :--- | :--- | :--- | :--- |
| **Tier 2 Weapons** | `tech_wpn_beam_carbine` (AP Beam Carbine) | `tech_wpn_anti_ship_torpedo` (Torpedo Salvo) | Single-target armor melt vs Area-of-effect warship cracking |
| **Tier 3 Weapons** | `tech_wpn_electromagnetic_railgun` (Railgun) | `tech_wpn_tachyon_lance` (Tachyon Lance) | Kinetic multi-unit line pierce vs Extreme continuous thermal melt |
| **Tier 3 Reactors**| `tech_rea_antimatter_pinch` (Singularity) | `tech_rea_tachyon_cyclotron` (Fortress Core) | Zero-heat movement & +4 Max AP vs +30% Forcefield absorption & heavy output |
| **Tier 2 Defense** | `tech_sld_composite_reactive` (Explosive Reactive)| `tech_sld_i_field_emitter` (I-Field Emitter) | Missile & kinetic deflection vs Particle beam deflection |
| **Tier 3 Defense** | `tech_sld_magnetic_barrier` (Phase Barrier) | `tech_sld_damascus_citadel` (Damascus Bulwark) | Active 40% pre-armor damage shield vs Raw +60 shield armor & -35% damage taken |
| **Tier 3 Mobility** | `tech_upg_nanite_cooling` (Thermal Loop) | `tech_upg_overboost_rig` (Vector Overboost) | -30% Heat per shot & auto-vent vs +25% Evasion & high-G hover dash |

### 2.3 Battlefield Salvage Intel & Black Box Eurekas
When enemy mobile suits suffer a catastrophic reactor breach on the tactical grid:
- A 45% roll triggers **Battlefield Salvage Intel**.
- If an active research slot matches the target category, **50% of remaining turn duration is instantly completed** (`BLACK BOX EUREKA`).
- If no active project matches, the Eureka is archived in `eureka_boosts`, cutting the next started project in that field by 50%.

---

## 3. Technology & Modular Component Cross-Reference (All 30 Parts)

| Slot | Part ID | Part Name | Required Alloy | Required Tech ID | Tech Name |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Heads** | `hd_vanguard_01` | Vanguard Target-Lock | Vanguard Composite | `tech_upg_analog_hydraulics` | Reinforced Hydraulic Actuators (Starter) |
| | `hd_aether_02` | Aether EW-Dome | Aerosteel Flux | `tech_upg_vernier_gimbals` | Omni-Directional Vernier Thrusters |
| | `hd_cyclops_03` | Cyclops Siege Optic | Adamantine Carbide | `tech_wpn_hyper_velocity_rifle`| 120mm Smoothbore Rifle |
| | `hd_damascus_04` | Damascus Reactive Visor | Reactive Damascus | `tech_sld_composite_reactive` | Explosive Reactive Shield |
| | `hd_tachyon_05` | Tachyon Spectral Dome | Tachyon Superalloy | `tech_sld_i_field_emitter` | Miniaturized I-Field Emitter |
| **Torsos**| `tr_colossus_01` | Colossus Heavy Torso | Vanguard Composite | `tech_rea_gas_cooled_fission` | Gas-Cooled Fission Generator (Starter) |
| | `tr_hyperion_02` | Hyperion Tokamak Torso | Hyperion Matrix | `tech_rea_compact_fusion` | Ultracompact He-3 Fusion Core |
| | `tr_phantom_03` | Phantom Striker Torso | Aerosteel Flux | `tech_upg_vernier_gimbals` | Omni-Directional Vernier Thrusters |
| | `tr_damascus_04` | Damascus Reactive Citadel| Reactive Damascus | `tech_rea_catalytic_prometheus`| Minovsky-Prometheus Catalytic Generator|
| | `tr_sol_05` | Sol Ferrite Super-Tokamak| Sol Ferrite | `tech_rea_antimatter_pinch` OR `tech_rea_tachyon_cyclotron` | Antimatter Singularity OR Tachyon Cyclotron |
| **Arms** | `am_colossus_01` | Colossus Dual Arms | Vanguard Composite | `tech_upg_analog_hydraulics` | Reinforced Hydraulic Actuators (Starter) |
| | `am_vernier_02` | Vernier Fast-Actuators | Aerosteel Flux | `tech_upg_vernier_gimbals` | Omni-Directional Vernier Thrusters |
| | `am_adamant_03` | Adamantine Heavy Brackets| Adamantine Carbide | `tech_wpn_hyper_velocity_rifle`| 120mm Smoothbore Rifle |
| | `am_aerogel_04` | Lunar Aerogel Manipulators| Lunar Aerogel | `tech_upg_nanite_cooling` OR `tech_upg_overboost_rig` | Nanite Thermal Coolant OR Vector Overboost |
| | `am_tachyon_05` | Tachyon Conduit Arms | Tachyon Superalloy | `tech_wpn_beam_carbine` | Particle Beam Rifle |
| **Legs** | `lg_vanguard_01` | Vanguard Heavy Walkers | Vanguard Composite | `tech_upg_analog_hydraulics` | Reinforced Hydraulic Actuators (Starter) |
| | `lg_stratos_02` | Stratos Vernier Skaters | Aerosteel Flux | `tech_upg_vernier_gimbals` | Omni-Directional Vernier Thrusters |
| | `lg_titan_03` | Titan Quad-Leg Platform | Adamantine Carbide | `tech_sld_composite_reactive` | Explosive Reactive Shield |
| | `lg_aerogel_04` | Lunar Aerogel Hover Struts| Lunar Aerogel | `tech_upg_nanite_cooling` OR `tech_upg_overboost_rig` | Nanite Thermal Coolant OR Vector Overboost |
| | `lg_damascus_05` | Damascus Armored Treads | Reactive Damascus | `tech_sld_magnetic_barrier` OR `tech_sld_damascus_citadel` | Magnetic Barrier OR Damascus Bulwark |
| **Backpacks**| `bp_heavy_01` | Heavy Booster Pack | Vanguard Composite | `tech_upg_analog_hydraulics` | Reinforced Hydraulic Actuators (Starter) |
| | `bp_vernier_02` | Dual-Vector Vernier Rig | Aerosteel Flux | `tech_upg_vernier_gimbals` | Omni-Directional Vernier Thrusters |
| | `bp_plasma_03` | Plasma Overcharge Booster| Hyperion Matrix | `tech_rea_catalytic_prometheus`| Minovsky-Prometheus Catalytic Generator|
| | `bp_aerogel_04` | Lunar Aerogel Siphon Rig | Lunar Aerogel | `tech_upg_nanite_cooling` OR `tech_upg_overboost_rig` | Nanite Thermal Coolant OR Vector Overboost |
| | `bp_tachyon_05` | Tachyon Fold Warp Booster| Tachyon Superalloy | `tech_rea_antimatter_pinch` OR `tech_rea_tachyon_cyclotron` | Antimatter Singularity OR Tachyon Cyclotron |
| **Weapons**| `wp_vulcan_01` | Rotary Vulcan (120mm) | Adamantine Carbide | `tech_wpn_heavy_autocannon` | Heavy Kinetic Autocannons (Starter) |
| | `wp_beam_02` | Particle Beam Rifle | Hyperion Matrix | `tech_wpn_beam_carbine` | Particle Beam Rifle |
| | `wp_rail_03` | Heavy Siege Rail Cannon | Adamantine Carbide | `tech_wpn_electromagnetic_railgun`| Hyper-Velocity Railgun |
| | `wp_sol_04` | Sol Ferrite Hyper-Railgun| Sol Ferrite | `tech_wpn_electromagnetic_railgun`| Hyper-Velocity Railgun |
| | `wp_tachyon_05` | Tachyon Beam Lance | Tachyon Superalloy | `tech_wpn_tachyon_lance` | Tachyon Beam Lance |

---

## 4. Verification Suite

The entire Equipment Research Tree system is covered by automated regression and integration suites:
- `tools/test_research_tree_system.py`: Validates all 11 core functions, UI strings, GameManager turn hooks, and save/load serialization (100% PASS).
- `tools/simulate_full_research_progression.py`: Simulates multi-turn project progression, slot expansions (3 -> 4 -> 5 slots), and breakthrough audio/log alerts (100% PASS).
- `tools/test_equipment_tech_tree_exhaustive.py`: Exhaustive validation of all 30 modular parts, 30 technology nodes, 6 symmetrical doctrine forks, Turn 1 starter coverage across all 6 slots, and battlefield salvage Eureka mechanics (100% PASS).
- `tools/validate_project.py`: Project-wide syntax and lint analyzer (0 errors).
