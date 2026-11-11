# Document 65: Master Session Refresher, Cross-PC Migration Handover, & Active State
**Document Version:** 1.0.0  
**Role:** Lead Game Developer & Technical Systems Architect  
**Target Engine:** GameMaker Studio 2 (Modern GML)  
**System Integrations:** `obj_DebugManager`, `obj_HQTerminal`, `obj_BattleManager`, `obj_FactionManager`, `obj_GameManager`  
**Purpose:** Ensure seamless, instant context recovery when migrating between PCs or starting fresh AI agent sessions.

---

## 1. Quick-Start: How to Resume on a New PC

> [!IMPORTANT]
> **Why Chat History Doesn't Transfer Across Machines**:
> Antigravity conversation threads and scratchpad brains are stored locally on each physical machine (`~/.gemini/antigravity/brain/...`). When you clone or pull the git repository on a new PC, the local code and documents transfer via git, but the local agent's chat history does not.
>
> **The 1-Step Prompt to Resume Anywhere**:
> Whenever you start a new chat on any PC, simply give the agent this exact prompt:
> ```text
> Please read docs/65_session_refresher_active_work_and_migration_handover.md to get up to speed on our architecture, recent design decisions, and active tasks, then resume where we left off.
> ```
> The agent will instantly ingest the full architectural context, current codebase state, and active priorities.

---

## 2. Core Game Vision & Gameplay Pillars

### The High-Concept Elevator Pitch
> *"You are an indebted asteroid scrapper who stumbled into the holy grail of mechanized warfare: a lost pre-war automated mobile suit foundry (`USN-X Hephaestus`). Can you turn a rusted ghost ship into a sovereign military-industrial empire before the four superpowers tear you—and the solar system—apart?"*

### Primary Systems Architecture
1. **Turn-Based Daily HQ Loop**: `obj_HQTerminal` drives strategic research, crucible metallurgy, pilot cantina recruitment, and procurement fly-off trials.
2. **2:1 Axonometric Isometric Combat**: `obj_BattleManager` handles 160x160 retro 16-bit mecha tactical skirmishes with localized limb destruction, elevation, facings, and cover.
3. **Modular Mech Builder & Forge**: `obj_DebugManager` (Tab 1) features a full Front Mission / Gundam hangar deck with live 3D-feel isometric previewing, alloy tinting, quality tiers, and weapon outfitting.
4. **4 Factions in Systemic Cold War**: Terran Hegemony, Jovian Coalition, Colony Alliance, and Obsidian Syndicate competing for planetary nodes and purchasing player-designed mechs.

---

## 3. Major Recent Architectural Decisions (What We Pivoted & Finalized)

### A. Scrapping Micro-Modularity in Favor of Curated Chassis & Alloy Metallics
* **Previous Approach**: Arbitrary 7-limb mix-and-match paperdoll modularity produced massive asset bloat, visual clipping, floating boxes, and incoherent mecha silhouettes.
* **Finalized Direction**: Streamlined into **3 Curated Foundry Base Templates** combined with **10 Sintered Crucible Alloys** and **4 Quality Grades (C, B, A, S)**.
* **Result**: Generates **50 visually distinct looks** across player platforms, 200 factory-certified specs, and 76,800 playable builds without visual clipping or programmer art.

### B. The 3 Grounded Foundry Starting Templates
When starting a campaign, the player chooses one of 3 base chassis lines that establishes the design philosophy of their foundry:

```
+----------------------------------------------------------------------------------------------------+
|                                THE 3 FOUNDATIONAL STARTER TEMPLATES                                |
+----------------------------------------------------------------------------------------------------+
| TEMPLATE 1: AEGIS VISOR DOCTRINE (Medium Balanced Wanzer)                                          |
| • Role: Balanced All-Rounder / Mil-Spec Contractor Mainstay.                                       |
| • Visuals: Recessed horizontal panoramic amber/cyan visor bar, squared modular pauldrons with       |
|   universal weapon rail clamps, interlocking hexagonal ceramic chest plates, fusion core.          |
| • Baseline Stats: 880 HP | 38 Armor | 60 Tonnes | 42 MW Core | 55 km/h.                              |
+----------------------------------------------------------------------------------------------------+
| TEMPLATE 2: COLOSSUS HEAVY FORGE DOCTRINE (Heavy Industrial Dreadnought)                           |
| • Role: Frontline Siege Brawler / Cast-Iron Breaker.                                               |
| • Visuals: Sloped wedge-shaped armored blast-hood with asymmetric amber lens cluster, monolithic   |
|   cast-steel torso with heavy weld seams, dual vertical exhaust chimneys venting heat haze,        |
|   exposed hydraulic leg pistons, rectangular stomper boots with anti-recoil ground spades.         |
| • Anti-Infringement Gate: 100% Zaku II traits purged (no green paint, no snout hoses, no dome).    |
| • Baseline Stats: 980 HP | 44 Armor | 78 Tonnes | 38 MW Core | 40 km/h.                              |
+----------------------------------------------------------------------------------------------------+
| TEMPLATE 3: STRATOS VECTOR DOCTRINE (Light Agile Recon Skirmisher)                                 |
| • Role: High-Mobility Aerospace Scout / Evasive E/W Skirmisher.                                    |
| • Visuals: Grounded military spec (NOT alien/god-tech). Chiseled titanium cowlings, tapered       |
|   waist, twin binocular sensor optics with low-profile crest, exposed vernier micro-thrusters.     |
| • Baseline Stats: 650 HP | 24 Armor | 42 Tonnes | 48 MW Core | 90 km/h.                              |
+----------------------------------------------------------------------------------------------------+
```

### C. Unarmed Base Chassis & Starter Weapon Kit
* **Unarmed Presentation**: All 3 templates are presented in their raw, naked state—completely unequipped with empty mechanical manipulators/gauntlets and visible modular hardpoint rails.
* **Standard Military Starter Kit**: Immediately upon selecting a template, the PMC foundry outfits the mech with:
  1. **Primary Weapon**: `wp_starter_mg_90` — **Type-90 90mm Kinetic Machine Gun** (180 Ballistic DMG, 8T, 2 MW).
  2. **Melee Weapon**: `wp_heat_hawk` — **Type-1 Tactical Combat Heat Axe** (235 Thermal DMG, 8T, 3 MW).
  3. **Shield Defense**: `sld_ballistic_buckler` — **Type-1 Ballistic Deflector Buckler** (+90 Shield HP, 4T, 0 MW).

### D. The 10 Sintered Crucible Alloys & 4 Quality Tiers
* **10 Sintered Alloys**:
  1. `alloy_vanguard_comp`: Gunmetal / Navy with cyan trim (Default Mil-Spec)
  2. `alloy_hyperion_matrix`: Deep cobalt with superconducting cyan glow
  3. `alloy_aerosteel_flux`: Satin chrome-white with gold vernier cowlings
  4. `alloy_adamantine_carbide`: Blackened charred tungsten with bronze joints
  5. `alloy_chobham_reactive`: Desert sand composite absorbing shaped charges
  6. `alloy_scrapper_slag`: Oxidized pitted iron with rust-orange trim
  7. `alloy_carbon_nanoweave`: Charcoal matte graphite with carbon-fiber weave
  8. `alloy_solar_crimson`: Anodized copper and deep crimson red with heat fins
  9. `alloy_depleted_actinide`: Toxic lead-slate gray with hazardous radioactive amber
  10. `alloy_tachyon_superalloy`: Midnight iridescent violet with Cherenkov radiation
* **4 Quality Grades**:
  * **C-Grade**: Industrial Standard (1.0x baseline stats)
  * **B-Grade**: Refined Mil-Spec (1.10x stats, combat hardened)
  * **A-Grade**: Ace Custom Prototype (1.20x stats, vernier tuning)
  * **S-Grade**: Singularity Masterwork (1.35x stats, radiant metallic sheen)

---

## 4. Key Source Code Files & Directory Architecture

| Path | Purpose | Key Variables / Functions |
| :--- | :--- | :--- |
| `objects/obj_DebugManager/Create_0.gml` | Mech Builder state & databases | `builder_lineage_idx`, `builder_lineage_names`, `builder_weapons_db`, `builder_alloys`, `builder_quality_mults`, `calculate_builder_telemetry()`, `deploy_builder_mech_to_combat()` |
| `objects/obj_DebugManager/Draw_64.gml` | Builder Hangar GUI & metallurgy | Lineage toggle bar (`_lin_str`), 2x5 sintered alloy grid with live color swatches, dynamic palette tinting (`_ad.tint_color`), weapon loadouts |
| `objects/obj_DebugManager/Step_0.gml` | Interactive builder navigation | Hotkey `L` cycles Foundry Lineages, `T` toggles platform catalogs, `1`-`4` switches subtabs |
| `objects/obj_BattleManager/` | 2:1 isometric tactical combat engine | Handles turn-based grid, limb destruction, animations (`idle`, `boost`, `melee`, `fire`), combat log, damage formulas |
| `objects/obj_HQTerminal/` | Strategic HQ command hub | R&D Tech Tree, Sintering Crucible, Procurement Fly-Off Trials, Pilot Cantina |
| `tools/test_debug_mech_builder_and_mining.py` | Automated testing harness | Validates 50 visual looks, 10 alloys, 4 quality tiers, and 3 lineages |

---

## 5. How to Run Automated Verification Tests

Before committing any new code, always run the automated Python test suite:
```bash
# Verify Mech Builder, 50 Distinct Looks, 10 Alloys, and 3 Lineages:
python3 tools/test_debug_mech_builder_and_mining.py

# Verify Master Campaign & Systems Integration:
python3 tools/test_phase4_validation.py
```

---

## 6. Immediate Next Tasks & Open Work

1. **Art Asset Ingestion**:
   * Generate/import the 3 unarmed base chassis sprite sheets into GameMaker Studio 2:
     * `spr_ms_pmc_aegis_visor` (Medium Balanced Wanzer)
     * `spr_ms_pmc_colossus_forge` (Heavy Industrial Dreadnought)
     * `spr_ms_pmc_stratos_vector` (Light Agile Recon Skirmisher)
   * Generate/import the starter weapon overlay sprites (Type-90 Machine Gun, Type-1 Heat Axe, Type-1 Buckler).
2. **Prologue / Foundry Activation Flow**:
   * Integrate the 3-lineage choice into the new campaign onboarding cutscene/dialogue (`obj_PrologueManager` / `obj_HQTerminal`), where Chief Engineer Jessica Vance prompts the Commander to calibrate the ship's ancient foundry crucible.
3. **Save/Load Serialization**:
   * Ensure `builder_lineage_idx` is saved to `obj_GameManager`'s persistent campaign state struct (`global.game_state.foundry_lineage`).

---

*Authored by the Lead Developer for MechMakerConcept.*

