# MechMakerConcept: Iron Vanguard

A retro 16-bit SNES/PS1-inspired Mecha Tactical RPG and Sovereign PMC Management Simulation built in **GameMaker Studio 2** (Modern GML).

---

## ⚡ Cross-PC Migration & AI Session Resumption

When pulling or cloning this repository on a new PC, start any coding agent session with:
> **"Please read `docs/65_session_refresher_active_work_and_migration_handover.md` to get up to speed on our architecture, recent design decisions, and active tasks, then resume where we left off."**

Full context, state machine specifications, test scripts, and architectural roadmaps are maintained in:
📖 **[`docs/65_session_refresher_active_work_and_migration_handover.md`](docs/65_session_refresher_active_work_and_migration_handover.md)**

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
