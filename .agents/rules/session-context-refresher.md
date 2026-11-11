# SESSION CONTEXT REFRESHER & PROJECT CONTINUITY RULE

* You are working on **MechMakerConcept: Iron Vanguard**, a retro 16-bit mecha tactical RPG and PMC management simulation in GameMaker Studio 2 (Modern GML).
* **Cross-PC Migration Handover**:
  * Because conversation history and agent brains are stored locally per machine, whenever resuming work or starting a new session on any computer, you must always inspect:
    `docs/65_session_refresher_active_work_and_migration_handover.md`
  * This document contains the full active state, recent architectural decisions, test harnesses, and next tasks.

### Core Architectural Directives to Strictly Maintain:
1. **The 3 Grounded Foundry Templates (Unarmed Base Frames)**:
   * **Template 1: Aegis Visor Doctrine**: Medium Balanced Wanzer (Wanzer/mil-spec, panoramic visor, boxy hardpoints, hex-ceramic plates).
   * **Template 2: Colossus Heavy Forge Doctrine**: Heavy Industrial Dreadnought (Cast-iron brawler, wedge blast-hood with amber lens cluster, twin rear exhaust stacks, hydraulic stomper boots). STRICT REJECTION GATE: Zero Gundam/Zaku resemblance (no green paint, no snout hoses, no round dome skull).
   * **Template 3: Stratos Vector Doctrine**: Light Agile Recon Skirmisher (Grounded aerospace skirmisher, swept titanium cowlings, twin binocular optics, low-profile crest, micro-verniers. NOT alien/advanced god-tech).
2. **Starter Weapon Loadout Trio**:
   * All base models start **completely unarmed and unshielded**. Upon template selection, the foundry outfits the mech with:
     * Primary: `wp_starter_mg_90` (Type-90 90mm Kinetic Machine Gun)
     * Melee: `wp_heat_hawk` (Type-1 Tactical Combat Heat Axe)
     * Defense: `sld_ballistic_buckler` (Type-1 Ballistic Deflector Buckler)
3. **Metallurgy & Progression**:
   * 10 Sintered Crucible Alloys $\times$ 5 Bespoke PMC Chassis = 50 Distinct Visual Looks.
   * 4 Quality Tiers: C (Industrial 1.0x), B (Mil-Spec 1.10x), A (Ace Custom 1.20x), S (Masterwork 1.35x).
4. **Sprite Standards**:
   * Engine-ready 160x160 pixel art on pure transparent background, origin at (80, 145), attackers facing 3/4 front-right (`xscale = 1`), defenders facing left (`xscale = -1`).
5. **Testing**:
   * Always verify changes using `python3 tools/test_debug_mech_builder_and_mining.py`.
