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
1. **Master Animation Bible & Batch 1 (Combat Choreography & Tooling)**:
   * Established [`docs/66_master_animation_bible.md`](docs/66_master_animation_bible.md) (`160x160`, `(80, 145)` foot anchor, `#FF00FF` edge flood-fill, `0`-issue QA gate).
   * Built [`tools/audit_sprites.py`](tools/audit_sprites.py) to catch missing layer PNGs, interior pinholes, white halos, and frozen frames.
   * Regenerated `spr_ms_ironclad_fire_rifle` cleanly and implemented `scr_get_mech_barrel_socket` + modular weapon-raise fallback in `scr_draw_animated_mobile_suit.gml` and 2-phase barrel-socket retaliation in `obj_DebugManager` / `obj_BattleManager`.
2. **Batch 2 — Player PMC Foundry Combat Animations**:
   * Imported, `[APPROVED]`, and registered `fire_rifle` (10 FPS, 4 frames) and `attack_melee` (12 FPS, 4 frames) for all 3 Player PMC Lineages:
     * `spr_ms_pmc_aegis_visor_fire_rifle` & `spr_ms_pmc_aegis_visor_attack_melee`
     * `spr_ms_pmc_colossus_forge_fire_rifle` & `spr_ms_pmc_colossus_forge_attack_melee`
     * `spr_ms_pmc_stratos_vector_fire_rifle` & `spr_ms_pmc_stratos_vector_attack_melee`
   * Zero `spr_ms_pmc_*` issues in `tools/audit_sprites.py`; 100% pass on `tools/test_phase4_validation.py` and `tools/test_debug_mech_builder_and_mining.py`.
3. **Combat, Campaign & Engine Stability**:
   * Unified Single HP Bar (*Gihren's Greed* style), **5-Theater Terrain Ranks (`S/A/B/C/D`: Land, Mountain, Water, Air, Space)** + Propulsion Kits + 4-Slot Sortie Picker, Battlefield Salvage (`3/3` foreign chassis unlock), Sintered Alloy combat passives, and Post-Battle Field Repair Bay.
   * Fixed `.yy` resource linking, missing `centurion` layer PNGs, `scr_territory_process_daily_logistics` crash, and `obj_DebugManager.is_open = false` startup state.

### 🎯 Immediate Next Tasks (Where to Resume):
1. **Batch 3 — Complete Remaining Animation States & Faction Roster**:
   * Generate/import `boost`, `hit`, and `destroyed` strips for the 3 PMC Foundry Lineages (`pmc_aegis_visor`, `pmc_colossus_forge`, `pmc_stratos_vector`).
   * Clean up remaining `[PINHOLES]` / `[WHITE HALO]` issues flagged by `python tools/audit_sprites.py` across existing faction suits (`centurion`, `aether`, `ironclad`, `bloodhound`, `ballista`, `chronos`) and expand bespoke `fire_*` / `attack_melee` coverage.
2. **In-Engine Barrel Socket QA (`F7` Proving Lab -> `[U]`)**:
   * Launch in GameMaker, test `fire_rifle` / `attack_melee` + 2-phase retaliation for all 3 PMC Foundry Lineages, and fine-tune `scr_get_mech_barrel_socket` muzzle offsets if needed.
3. **Foundry Selection Prologue Cutscene**:
   * Wire the 3-lineage starting choice into the campaign onboarding event in `obj_HQTerminal`.

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
