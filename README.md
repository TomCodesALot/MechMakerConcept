# MechMakerConcept: Iron Vanguard

A retro 16-bit SNES/PS1-inspired Mecha Tactical RPG and Sovereign PMC Management Simulation built in **GameMaker Studio 2** (Modern GML).

---

## ⚡ Cross-PC Migration & AI Session Resumption

When pulling or cloning this repository on a new PC, start any coding agent session with:
> **"Please read `docs/65_session_refresher_active_work_and_migration_handover.md` to get up to speed on our architecture, recent design decisions, and active tasks, then resume where we left off."**

Full context, state machine specifications, test scripts, and architectural roadmaps are maintained in:
📖 **[`docs/65_session_refresher_active_work_and_migration_handover.md`](docs/65_session_refresher_active_work_and_migration_handover.md)**

---

## 📍 Where We Left Off & Next Immediate Tasks

### ✅ Completed & Tested in Engine:
1. **Simplified Progression Architecture**:
   * Scrapped arbitrary 7-limb micro-paperdoll modularity (which caused visual clipping and asset bloat) in favor of **Curated Base Chassis Templates + Sintered Metallurgy Alloys + Quality Tiers (C/B/A/S) + Starter Weapon Outfitting**.
2. **The 3 Grounded Unarmed Foundry Templates**:
   * All base templates are **unarmed and unshielded** (empty mechanical hands/gauntlets with visible modular hardpoint rails):
     * **Template 1: Aegis Visor Doctrine** — *Medium Balanced Wanzer* (880 HP, 38 Armor, 60T, 55 km/h).
     * **Template 2: Colossus Heavy Forge Doctrine** — *Heavy Industrial Dreadnought* (980 HP, 44 Armor, 78T, 40 km/h; zero Gundam/Zaku resemblance, twin exhaust stacks, sloped blast-hood, hydraulic stompers).
     * **Template 3: Stratos Vector Doctrine** — *Light Agile Recon Skirmisher* (650 HP, 24 Armor, 42T, 90 km/h; grounded military aerospace scout replacing overly alien/advanced archeotech).
3. **Standard Issue Starter Equipment Kit**:
   * Once a template is chosen, the foundry equips:
     * **Primary**: `wp_starter_mg_90` — Type-90 90mm Kinetic Machine Gun (180 DMG, 8T, 2 MW).
     * **Melee**: `wp_heat_hawk` — Type-1 Tactical Combat Heat Axe (235 DMG, 8T, 3 MW).
     * **Defense**: `sld_ballistic_buckler` — Type-1 Ballistic Deflector Buckler (+90 HP, 4T, 0 MW).
4. **Metallurgy & Quality Tiers**:
   * 10 Sintered Alloys $\times$ 5 Chassis = **50 distinct visual looks**, 4 quality tiers (C, B, A, S), 200 certified specs, and 76,800 playable builds.
   * Fully wired into [`obj_DebugManager`](objects/obj_DebugManager/Create_0.gml) with live GUI cycling and hotkey `L`. 100% test pass on [`tools/test_debug_mech_builder_and_mining.py`](tools/test_debug_mech_builder_and_mining.py).

### 🎯 Immediate Next Tasks (Where to Resume):
1. **Art Asset Ingestion**:
   * Generate/import the 160x160 pixel art sprites for the **3 Unarmed Base Chassis** (`spr_ms_pmc_aegis_visor`, `spr_ms_pmc_colossus_forge`, `spr_ms_pmc_stratos_vector`) and the **3 Starter Weapon Overlays** (Type-90 Machine Gun, Type-1 Heat Axe, Type-1 Deflector Buckler).
2. **GameMaker Sprite & Hangar Wiring**:
   * Connect the new unarmed sprites into `obj_DebugManager`'s 2.0x isometric preview deck and `obj_BattleManager`'s combat rendering pipeline.
3. **Foundry Selection Prologue Cutscene**:
   * Wire the 3-lineage starting choice into the new campaign onboarding event in `obj_HQTerminal` where Chief Engineer Jessica Vance prompts the player to calibrate the *USN-X Hephaestus* foundry crucible.

---

## 🎮 Core Systems Overview

1. **Strategic Daily HQ Loop (`obj_HQTerminal`)**:
   * Turn-based command deck with Sintering Metallurgy Crucible, R&D Tech Tree, Pilot Cantina, and Procurement Fly-Off Trials.
2. **2:1 Isometric Tactical Combat (`obj_BattleManager`)**:
   * Axonometric grid combat with localized limb destruction (Head, Torso, Left Arm, Right Arm, Legs), dynamic facings, elevation, and cover.
3. **Modular Mech Builder & Forge (`obj_DebugManager` Tab 1)**:
   * Front Mission / Gundam hangar deck with live 3D-feel previewing, 10 sintered alloy finishes, 4 quality grades (C, B, A, S), and weapons outfitting.
4. **The 3 Foundational Foundry Lineages**:
   * **Template 1: Aegis Visor Doctrine** — Medium Balanced Wanzer (Mil-spec, panoramic visor, boxy modularity).
   * **Template 2: Colossus Heavy Forge Doctrine** — Heavy Industrial Dreadnought (Cast-iron brawler, wedge blast-hood, dual exhaust stacks, hydraulic stomper boots).
   * **Template 3: Stratos Vector Doctrine** — Light Agile Recon Skirmisher (Grounded aerospace skirmisher, swept cowlings, twin binocular optics, micro-verniers).
5. **Standard Starter Kit**:
   * All base models begin unarmed and are equipped with the starter trio:
     * **Primary**: Type-90 90mm Kinetic Machine Gun
     * **Melee**: Type-1 Tactical Combat Heat Axe
     * **Shield**: Type-1 Ballistic Deflector Buckler

---

## 🧪 Automated Testing & Verification

Run the verification test suite before committing changes:
```bash
# Verify Mech Builder, 50 Distinct Looks, 10 Alloys, and 3 Lineages:
python3 tools/test_debug_mech_builder_and_mining.py

# Verify Master Campaign & Systems Integration:
python3 tools/test_phase4_validation.py
```

---

## 📂 Project Directory Structure

```text
MechMakerConcept/
├── .agents/rules/     # Automated AI rules and context refreshers
├── docs/              # Master design documents (docs 00 through 65)
├── objects/           # GameMaker Studio 2 game objects (obj_DebugManager, obj_BattleManager, etc.)
├── scripts/           # GML scripts and utility libraries
├── sprites/           # Master 160x160 pixel art mecha and UI sprites
├── tools/             # Automated Python validation and testing harnesses
└── README.md          # Project entry point and migration guide
```
