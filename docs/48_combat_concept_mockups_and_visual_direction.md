# 48. Tactical Combat Visual Concepts & In-Game Mockups

**Prepared by:** Lead Developer & Studio Department Leads  
**For:** Co-Dev Review & System Alignment  
**Target Engine:** GameMaker Studio 2 (Modern GML)  
**Inspirations:** *Front Mission* (SNES / PS1), *Gihren's Greed (Giren no Yabou)*, *Tactics Ogre*, *Armored Core*

---

## Executive Overview: The Dual-Layer Tactical Architecture

As defined in the core combat architecture ([docs/17_grand_scale_isometric_combat_system.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/17_grand_scale_isometric_combat_system.md) and [docs/31_snes_front_mission_multi_unit_isometric_combat_system.md](file:///home/tom/GameMakerProjects/MechMakerConcept/docs/31_snes_front_mission_multi_unit_isometric_combat_system.md)), our combat loop uses a **Dual-Layer Tactical Experience**:

1. **Layer 1: The Isometric Tactical Battlefield**: A 2:1 axonometric wargame map with vertical elevation tiers ($Z \in \{0, 1, 2, 3\}$), 3-mech platoon formations, dynamic cover, crossfire angles, and movement grid navigation.
2. **Layer 2: The Dedicated Cinematic Battle Clash**: A side-view mecha engagement screen that triggers upon attack confirmation, rendering animated weapon fire, cartridge ejections, vernier thrusters, and modular limb destruction.
3. **Layer 3: Modular Precision Targeting HUD**: A pre-engagement tactical targeting overlay allowing pilots to target individual mecha parts (`BODY`, `L-ARM`, `R-ARM`, `LEGS`) with explicit tactical trade-offs (crippling weapons vs reducing movement vs core destruction).

---

## Visual Concept Showcase

````carousel
![Layer 1: Grand-Scale Isometric Tactical Map](/home/tom/.gemini/antigravity-ide/brain/8ea0d68e-0f47-497f-9824-313a8bffafd4/tactical_isometric_combat_1792814573052.jpg)
<!-- slide -->
![Layer 2: Cinematic Battle Clash (Platoon Engagement 3v3)](/home/tom/.gemini/antigravity-ide/brain/8ea0d68e-0f47-497f-9824-313a8bffafd4/cinematic_platoon_clash_1792814588337.jpg)
<!-- slide -->
![Layer 2: High-Mobility Prototype Ace Duel](/home/tom/.gemini/antigravity-ide/brain/8ea0d68e-0f47-497f-9824-313a8bffafd4/orbital_ace_duel_1792814612161.jpg)
<!-- slide -->
![Layer 3: Modular Precision Limb Targeting HUD](/home/tom/.gemini/antigravity-ide/brain/8ea0d68e-0f47-497f-9824-313a8bffafd4/modular_targeting_hud_1792814629863.jpg)
````

---

## Detailed Mockup Breakdown & Engineering Specs

### 1. Layer 1: Grand-Scale Isometric Tactical Map
![Layer 1: Grand-Scale Isometric Tactical Map](/home/tom/.gemini/antigravity-ide/brain/8ea0d68e-0f47-497f-9824-313a8bffafd4/tactical_isometric_combat_1792814573052.jpg)

#### Visual & Design Features
* **2:1 Axonometric Grid:** Classic SNES/PS1 ratio ($W_{\text{iso}} = 64\text{px}$, $H_{\text{iso}} = 32\text{px}$) with multi-level elevation cliffs ($H_{\text{elev}} = 16\text{px}$).
* **Platoon Squad Formations:** Standard grunts field as 3-mecha squads (Leader + 2 Wingmen in echelon formation: `ALPHA-1`, `ALPHA-2`, `ALPHA-3`).
* **Tactical High Ground & Line of Sight:** Elevation tiers grant high-ground bonuses ($+15\%$ accuracy, $+1$ effective firing range).
* **Tactical Overlays:**
  * Cyan/Blue navigation grid for unit movement.
  * Red vector targeting line with direct line-of-sight check to enemy targets.
  * Reticle lock-on highlight around hostile targets (`HADES` unit in canyon below).
* **Tactical Commander HUD:**
  * **Top Bar:** Sector designation, active theater, turn counter, and phase alert.
  * **Bottom-Left:** Active pilot profile (`Sgt. R. Chen`), AP action battery, and Front Mission 4-part integrity bars (`BODY: 88%`, `L-ARM: 75%`, `R-ARM: 92%`, `LEGS: 80%`).
  * **Bottom-Right:** Tactical command buttons (`[MOVE]`, `[ATTACK]`, `[OVERWATCH]`, `[END TURN]`).

#### GML Implementation Reference
* **Render Pipeline:** [obj_BattleManager/Draw_0.gml](file:///home/tom/GameMakerProjects/MechMakerConcept/objects/obj_BattleManager/Draw_0.gml) handles isometric tile conversion (`iso_to_screen_x`, `iso_to_screen_y`), elevation cliff walls, and depth sorting (`-depth = (c + r) * 32 + elev * 16`).
* **Unit Rendering:** Universal mobile suit animator [scr_draw_animated_mobile_suit.gml](file:///home/tom/GameMakerProjects/MechMakerConcept/scripts/scr_draw_animated_mobile_suit/scr_draw_animated_mobile_suit.gml) dynamically renders front and rear $3/4$ isometric perspectives based on unit facing vector.

---

### 2. Layer 2: Dedicated Cinematic Battle Clash (Platoon 3v3)
![Layer 2: Cinematic Battle Clash](/home/tom/.gemini/antigravity-ide/brain/8ea0d68e-0f47-497f-9824-313a8bffafd4/cinematic_platoon_clash_1792814588337.jpg)

#### Visual & Design Features
* **Widescreen 2.39:1 Cutscene Framing:** Black letterbox shutter bars slide in seamlessly from top and bottom upon combat engagement.
* **Allied Formation (Left, Facing Right):**
  * 3 heavy dieselpunk military mobile suits (Leader in front, 2 wingmen behind) with vernier thrusters flaring.
  * Synchronized 120mm rotary autocannon volley with intense muzzle flashes and spent brass cartridges ejecting into the air.
  * Shoulder missile salvos arcing through the sky with realistic propellant smoke plumes.
* **Hostile Formation (Right, Facing Left):**
  * Enemy Crimson Zaibatsu / Syndicate wanzer platoon taking kinetic impact spark bursts.
  * Armor plate deformation and directional smoke clouds from compromised reactors.
* **Combat Feedback & HUD:**
  * Floating yellow pixel damage numbers (`-185`, `CRITICAL HIT!`).
  * **Bottom-Left:** Platoon attrition telemetry displaying all 3 squad members (`LEO`, `MAIA`, `ROOK`) with individual health gauges and modular wireframe diagram highlighting damaged limbs in amber/red.
  * **Bottom-Right:** Hostile Ace/Commander profile (`ACE: MALAKOV`) with structural integrity meter (`85% HP`).

#### GML Implementation Reference
* **Render Pipeline:** [obj_BattleManager/Create_0.gml:L4174](file:///home/tom/GameMakerProjects/MechMakerConcept/objects/obj_BattleManager/Create_0.gml#L4174) (`draw_battle_cinematic_stage`) and [obj_BattleManager/Draw_64.gml](file:///home/tom/GameMakerProjects/MechMakerConcept/objects/obj_BattleManager/Draw_64.gml).
* **Parallax Backdrops:** Dynamically selects based on current battle theater:
  * Mining Quarry / Desert Badlands (layered canyon mesas, excavator cranes, dust motes).
  * Urban Highway (shattered brutalist towers, sweeping searchlights, concrete barriers).
  * Water Canal (shipyard silhouettes, gas torches, 3-tier rolling sine waves).
  * Slag Crucible (glowing magma fissures, basalt rocks, rising heat embers).
  * Deep Space / Orbital (colony cylinder silhouette, twinkling stars, curving planet rim).

---

### 3. Layer 2: High-Mobility Prototype Ace Duel
![Layer 2: Ace Duel](/home/tom/.gemini/antigravity-ide/brain/8ea0d68e-0f47-497f-9824-313a8bffafd4/orbital_ace_duel_1792814612161.jpg)

#### Visual & Design Features
* **Solo Super Ace Doctrine:** Elite custom prototypes deploy as single-unit powerhouses with superior agility and evasion.
* **Acrobatic Mecha Combat:**
  * High-speed vernier boost leap with luminous cyan plasma thruster plumes and afterimage motion blur.
  * Incandescent plasma beam saber arc slicing through incoming enemy fire.
  * Opponent heavy titan mecha firing flak cannons and tracking with red laser targeters.
* **Atmospheric Sci-Fi Setting:** Orbital colony interior with transparent dome viewing Earth and starfields, glowing city grid beneath.
* **Cockpit Audio/Visual Comms:**
  * Pilot radio comms box with cathode static: `[COMMS] ACE PILOT: Systems holding. Engaging target.`
  * Combat evasion alert: `EVADED! 0 DMG`.
  * Front Mission 4-part precise HP readout (`BODY: 750/750`, `L-ARM: 520/520`, `R-ARM: 520/520`, `LEGS: 680/680`) alongside reactor energy capacitor gauge ($95\%$).

---

### 4. Layer 3: Modular Precision Targeting HUD
![Layer 3: Modular Precision Targeting HUD](/home/tom/.gemini/antigravity-ide/brain/8ea0d68e-0f47-497f-9824-313a8bffafd4/modular_targeting_hud_1792814629863.jpg)

#### Visual & Design Features
* **Tactical Wireframe Breakdown:** Front-and-center mechanical schematic of the targeted enemy suit with live hit probabilities per modular component:
  * **BODY ($55\%$ Hit, $450/450$ HP):** Core destruction drops the entire unit immediately.
  * **L-ARM / SHIELD ($25\%$ Hit, $280/280$ HP):** Destroys defensive ward and shield deflection.
  * **R-ARM / AUTOCANNON ($20\%$ Hit, $280/280$ HP):** **CRIPPLE WEAPON!** Disables primary offensive firepower.
  * **LEGS ($40\%$ Hit, $350/350$ HP):** **MOBILITY PENALTY!** Inflicts `MOVE -2` and strips evasion bonuses.
* **Weapon Selection Matrix:** Allows pilot to switch between equipped armaments before firing:
  * `120mm AP Autocannon` ($40/40$ ammo, $110$ kinetic damage).
  * `Plasma Beam Rifle` ($15/15$ ammo, $140$ energy damage, high armor penetration).
  * `Swarm Missiles` ($6/6$ ammo, $180$ explosive multi-target damage).
* **Situational Tactical Modifiers:**
  * `BONUS: +15% ACCURACY (HIGH GROUND)`
  * `BONUS: CROSSFIRE FLANK (ENEMY EXPOSED)`
  * `RANGE: 7 [OPTIMAL]`

---

## Departmental Technical Notes for Implementation

### Lead Game Designer (Director) Notes
> [!IMPORTANT]
> - Grunts are designed to be cheap, replaceable, and field in **3-unit platoons** where squad attrition reduces offensive output proportionally ($3 \rightarrow 2 \rightarrow 1$ active weapons).
> - Custom player-built mechas and Nemesis Aces field as **solo modular units** where limb damage directly disables installed weapons, thrusters, and sensors.
> - Elevation must always be respected: units on higher ground take $20\%$ less splash damage and deal $+15\%$ kinetic damage due to downward projectile velocity.

### Concept Artist & Technical Animator Notes
> [!TIP]
> - All mecha sprites are rendered on uniform grids ($160 \times 160\text{px}$) with dedicated `_idle`, `_back_idle`, `_fire`, `_hit`, `_crippled`, and `_destroyed` states.
> - Particle effects (`spr_fx_spark`, `spr_fx_explosion`, `spr_proj_*`) leverage additive blending (`gpu_set_blendmode(bm_add)`) to achieve 16-bit arcade vibrancy.
> - Recoil physics during the cinematic clash apply subtle spring-damper offsets (`atk_recoil_x`, `atk_recoil_y`) followed by screen shake decay ($0.92$ damping per frame).

### Lead Audio Engineer Notes
> [!NOTE]
> - **Autocannon Barrage:** Heavy rotary punch with randomized pitch ($\pm 0.08$) and mechanical shell casing metallic bounce Foley.
> - **Missile Swarm:** High-pressure pneumatic launch hiss followed by staggered roaring rocket burns and stereo-panned explosions.
> - **Limb Destruction:** High-tension shearing alloy impact, sudden electrical arc hiss, and pilot cockpit warning klaxon.

---

## Action Items for Co-Dev Review

1. **Visual Style Approval:** Confirm the 16-bit SNES / Front Mission gritty military aesthetic, palette balance, and CRT scanline filter.
2. **Transition Timing:** Align on the cinematic clash camera transition duration (currently $18\text{ frames}$ shutter slide in, $90-120\text{ frames}$ engagement resolution, $18\text{ frames}$ shutter slide out).
3. **HUD Ergonomics:** Verify button layout and modular limb readout legibility on standard $1920 \times 1080$ displays.
