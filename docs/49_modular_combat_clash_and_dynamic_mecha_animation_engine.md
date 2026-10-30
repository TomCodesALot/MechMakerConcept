# 49. Modular Combat Clash & Dynamic Mecha Animation Engine

**Prepared by:** Lead Developer, Lead Concept Artist & Technical Game Animator  
**For:** Executive Studio Review & Production Deployment  
**Target Engine:** GameMaker Studio 2 (Modern GML)  
**Aesthetic Core:** 16-Bit Super Nintendo / PS1 Tactical RPG (*Front Mission*, *Shin Gihren no Yabou*, *Vanguard Bandits*)

---

## 1. Executive Summary & Design Vision

Following comprehensive architectural alignment in `/grill-me`, the **Modular Combat Clash & Dynamic Mecha Animation Engine** establishes the complete dual-layer visual and mathematical engagement pipeline for *MechMakerConcept*.

The engine bridges the strategic grand-scale isometric battlefield with a high-impact, side-view 16-bit animated mecha duel. By uniting **standardized 160x160 bone socket matrices**, **sintered metallurgy procedural color grading**, **4-class weapon choreography**, **tactical limb severing**, and a **diegetic bottom phosphor cockpit telemetry console**, every mobile suit custom-forged by the player animates with authentic retro mechanical inertia and visual identity.

---

## 2. Core Architectural Pillars

### Pillar 1: Hybrid Modular Sockets across 4 Base Chassis
Rather than maintaining thousands of disconnected sprite assets, custom mecha render through standardized bone anchor matrices anchored to 4 mobility archetypes across both $3/4$ front and rear isometric angles:

1. **Bipedal Heavy (`biped`):** High-torque hydraulic legs with grounded stability and centered chest core.
2. **Hover Sniper (`hover`):** Continuous sine-wave hover levitation ($\Delta y = \sin(t \cdot 0.004) \cdot 4	ext{px}$) with offset long-rifle shoulder mounts.
3. **Caterpillar Tread (`tread`):** Heavy dual-tread artillery carriage with wide-stance shoulder mounts and reinforced chassis plating.
4. **Aerodynamic Striker (`aero`):** Forward-swept atmospheric flight frame with high-frequency vernier hover ($\Delta y = \sin(t \cdot 0.005) \cdot 5	ext{px}$) and twin rear turbine exhaust ports.

#### 160x160 Bone Socket Coordinate Database (`scr_get_chassis_sockets`)
| Chassis | Perspective | Head Socket $(x, y)$ | L-Arm Socket $(x, y)$ | R-Arm Socket $(x, y)$ | Backpack Socket $(x, y)$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Biped** | Front | $(+2, -78)$ | $(-24, -48)$ | $(+24, -44)$ | $(-12, -62)$ |
| **Biped** | Back | $(+2, -80)$ | $(+24, -48)$ | $(-24, -44)$ | $(0, -60)$ |
| **Hover** | Front | $(+6, -76)$ | $(-20, -44)$ | $(+28, -40)$ | $(-16, -56)$ |
| **Hover** | Back | $(+6, -78)$ | $(+20, -44)$ | $(-28, -40)$ | $(-4, -56)$ |
| **Tread** | Front | $(0, -70)$ | $(-30, -42)$ | $(+30, -42)$ | $(-18, -54)$ |
| **Tread** | Back | $(0, -72)$ | $(+30, -42)$ | $(-30, -42)$ | $(-6, -54)$ |
| **Aero** | Front | $(+10, -78)$ | $(-18, -46)$ | $(+26, -42)$ | $(-14, -60)$ |
| **Aero** | Back | $(+10, -80)$ | $(+18, -46)$ | $(-26, -42)$ | $(-2, -60)$ |

---

### Pillar 2: Sintered Metallurgy Procedural Color Engine
Every forged mobile suit inherits procedural alloy pigmentation derived from the periodic table sintering crucible ([docs/02_alloy_chemistry.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/02_alloy_chemistry.md)):

* **Vanguard Composite (`alloy_vanguard_comp`):** Cold gunmetal cerulean with safety-orange core exhaust glow.
* **Hyperion Matrix (`alloy_hyperion_matrix`):** Deep cobalt titanium with electric-cyan reactor plume.
* **Aerosteel Flux (`alloy_aerosteel_flux`):** High-albedo pearl silver with viridian plasma discharge.
* **Adamantine Carbide (`alloy_adamantine_carbide`):** Dark sintered tungsten graphite with fiery amber thermite venting.
* **Tachyon Superalloy (`alloy_tachyon_superalloy`):** Prismatic violet-white alloy with high-energy quantum dispersion.

---

### Pillar 3: 4-Class Dynamic Weapon Choreography
Weapon fire in the battle clash is segregated into 4 mechanical classes, each featuring tailored timing, recoil physics, and ballistic debris:

1. **Ballistic Class (Autocannons, Vulcans, Snipers):**
   * High-frequency blowback recoil ($\Delta x = -14	ext{px}$).
   * Ejection of tumbling brass shell casings with physical velocity, gravity, and spin ($\Delta v_x, \Delta v_y, \omega$).
2. **Energy Class (Beam Rifles, Plasma Torches, Tachyon Particle Beams):**
   * Charging energy flare at weapon emitter ($t = 1..15$).
   * Dual-layer raster beam stream (outer cyan glow $	ext{radius} = 6	ext{px}$, inner pure white core $	ext{radius} = 2	ext{px}$).
3. **Ordnance Class (Micro-Missiles, Torpedoes, Howitzers):**
   * Salvo launch with smoke plume cloud burst.
   * Sinusoidal missile flight paths with persistent particulate smoke contrails.
4. **Melee Class (Plasma Blades, Vibro-Axes, Pile Bunkers):**
   * High-speed forward dash thrust ($\Delta x = +320	ext{px}$ closing into defender point-blank range).
   * High-energy kinetic cleavage arc ($	ext{timer} = 24	ext{ frames}$, screen shake $22.0$).
   * Spark cascade and instantaneous backward dash return.

---

### Pillar 4: Modular Limb Detachment & Persistent Tactical Scars
When component HP drops to zero ($\le 0	ext{ HP}$):
1. **Clash Cutscene:** Spawns a detached limb debris projectile that spins through the air with angular momentum ($	ext{spin} = \pm 18^\circ/	ext{frame}$) and emits electrical arc sparks.
2. **Severed Arm Socket Overlays:** Direct $1:1$ sprite overlay onto the unit origin using `spr_ms_ironclad_hit_left_arm_off` (left arm severed) and `spr_ms_ironclad_hit_right_arm_off` (right arm and primary weapon severed).
3. **Persistent Map Scars:** The isometric tactical battlefield retains visual battle damage—units with severed arms show broken spark sockets, and crippled legs emit periodic trailing smoke clouds.

---

### Pillar 5: Retro CRT Scanlines & Diegetic Cockpit Telemetry HUD
The clash screen renders through a $128 	imes 128	ext{px}$ seamless scanline overlay (`spr_snes_crt_scanline`) with top and bottom hydraulic letterbox shutters. The bottom shutter houses the **Retro Cockpit Telemetry Deck**:

* **Attacker Cockpit (Left):** Pilot portrait ($0.40$ scale), expression badge (`[NEUTRAL]`, `[FIRING]`, `[CRITICAL_SUCCESS]`), callsign, metallurgy alloy type, green phosphor radio bark ticker with blinking underscore cursor, and 5 Front Mission wireframe limb bars (`HD`, `TR`, `LA`, `RA`, `LG`).
* **Defender Cockpit (Right):** Hostile pilot portrait ($0.40$ scale), defensive badge (`[DEFENDING]`, `[EVADED]`, `[CRIPPLED]`), callsign, amber radio bark ticker, and 5 Front Mission wireframe limb bars with flashing red critical limb highlights (`limb_flash_part`).
* **Tactical Computer (Center):** Real-time ballistic metrics (Calculated Damage, Mitigation, AP, Flanking tags, Elevation modifiers, Fast-forward hint `[SPACE / CLICK] FAST-FORWARD >>`).

---

## 3. Engineering Implementation Details

### File Manifest
1. `scripts/scr_draw_animated_mobile_suit/scr_draw_animated_mobile_suit.gml`:
   * `scr_get_chassis_sockets(_chassis_type)`: Returns Front & Back socket coordinates.
   * `scr_draw_custom_mobile_suit(...)`: Multi-pass composite socket renderer with metallurgy alloy colors, severed arm overlays, weapon kickback, and vernier plumes.
   * Universal routing: Routes all custom prototypes (`bp_player_*`, `custom_*`, `vanguard_heavy`, `ghost_sniper`, `scrapper_brawler`, `stratos_interceptor`) directly into socket renderer.
2. `objects/obj_BattleManager/Create_0.gml`:
   * `cinematic_combat_enabled = true;`
   * `battle_cinematic`: Complete 66-field state container.
   * `start_battle_cinematic(...)`: Initialises clash state, evaluates Vanguard screening, Brace mitigation, weapon class choreography, and pilot expressions.
   * `update_battle_cinematic()`: Phase machine driving Melee forward dash, energy charge, missile salvos, ballistic casings, limb fly-off, and wreckage creation.
   * `skip_battle_cinematic()`: Fast-forward instant combat resolution.
   * `draw_battle_cinematic_stage()`: Renders CRT scanline background, staged mechas, in-flight ordnance, and bottom cockpit telemetry HUD.
3. `objects/obj_BattleManager/Draw_0.gml`:
   * Persistent tactical map battle scars with severed arm overlays and crippled leg trailing smoke puffs.
4. `objects/obj_BattleManager/Step_0.gml` & `Draw_64.gml`:
   * Frame-by-frame update and screen-space clash rendering hooks.

---

## 4. Verification & QA Sign-Off

The entire engine has been validated across automated test suites:
* `tools/test_goal_final_modular_combat_engine.py`: **100% PASSED** (Sockets, Metallurgy, Choreography, Limb Detachment, Cockpit HUD).
* `tools/test_refined_combat_system.py`: **100% PASSED** (Vanguard screening, Brace, Dynamic Pacing, Wreckage, Ejection).
* `tools/test_complete_stack_ui_suite.py`: **100% PASSED** (6-unit stacking, echelon offsets, command bus).
* `tools/test_goals_a_b_c_exhaustive.py`: **100% PASSED** (Supply starvation, Pilot perks, Flagship orbit).
* `tools/test_goal_d_exhaustive.py`: **100% PASSED** (S-grade masterwork +1 AP, Victory paths).
* `tools/test_goal_e_exhaustive.py`: **100% PASSED** (Espionage, Brig detention, Nemesis bounty).
* `tools/test_goal_f_exhaustive.py`: **100% PASSED** (Tactical ballistics, elevation modifiers, cover degradation).
* `tools/test_goal_g_exhaustive.py`: **100% PASSED** (Apex crisis boss, phase barrier, orbital bombardment).
* `tools/validate_project.py`: **0 ERRORS** (Zero syntax or schema violations).

---

*Lead Developer & Technical Game Animator Sign-Off: Ready for Mainline Deployment.*
