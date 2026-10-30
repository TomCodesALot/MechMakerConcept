# DOCS 45: TACTICAL COMBAT POLISH, CROSSFIRE SUPPRESSION, HIGH-GROUND BALLISTICS & PLATOON AI

## 1. Overview & System Objectives
This document establishes the architecture, mathematical formulations, and UI/UX flows implemented for **Goal F**:
1. **Crossfire Suppression & Pinning Engine**: Sustained rapid-fire barrages (vulcans, gatlings, autocannons) or concentrated salvos (2+ hits taken in a single turn) inflict the **`SUPPRESSED / PINNED`** tactical state, applying a $-20\%$ aim accuracy penalty, $-1$ movement range penalty, and $-2$ AP penalty on the next turn.
2. **High-Ground Kinetic Velocity & Ballistics**: Units perched on higher elevation relative to their targets gain $+15\%$ kinetic damage per elevation step, $+10\%$ hit chance per step, and $+1$ effective maximum weapon range. Conversely, units firing uphill suffer $-15\%$ kinetic damage mitigation and a $-15\%$ accuracy penalty per elevation tier.
3. **Destructible Cover Degradation & Heavy Ordnance Penetration**: Heavy armor-piercing ordnance (Railguns, 120mm solid shot, siege cannons) ignores $50\%$ of target cover evasion. Upon impact, heavy ordnance physically degrades the fortification: Level 2 Bastions crack into Level 1 Rubble, and Level 1 Rubble is annihilated to Level 0 cratered terrain.
4. **Directional Facing Angles & Flanking/Rear Core Strikes**: Calculating 4-way isometric orientation vectors (`iso_get_facing`). Attacking an opponent from the flank ($90^\circ$) grants $+15\%$ hit chance and $+20\%$ damage. Attacking from the rear ($180^\circ$) bypasses $20\%$ thruster evasion, grants $+30\%$ hit chance, $+40\%$ catastrophic damage, and focuses damage directly on the Torso Reactor Core and Vernier Backpack.
5. **Platoon Role AI Specialization & Tactical Forecast HUD**: Hostile and mercenary AI units dynamically evaluate their chassis roles (**Sniper**, **Flanker**, **Vanguard**), seeking high ground, executing flanking maneuvers around target front arcs, and coordinating focus-fire to suppress player aces. The in-game `TARGET_MODE` forecast HUD provides real-time vector, terrain, and defensive telemetry.

---

## 2. Pillar I: Crossfire Suppression & Pinning

### 2.1 Trigger Conditions & Stacking
A unit receives the `is_suppressed = true` status under either of two battlefield conditions:
- **Suppressive Weapon Caliber**: Hit by rotary vulcans, gatling guns, autocannons, or saturation micro-missiles (`proj_type == "ROTARY_VULCAN"` or name containing `"VULCAN"`, `"GATLING"`, `"AUTOCANNON"`, `"SUPPRESS"`).
- **Concentrated Volley / Interlocking Fire**: A unit absorbs $\ge 2$ distinct attacks in the same turn (`hits_taken_this_turn >= 2`).

### 2.2 Mechanical Debuffs & Recovery
| Phase | Metric | Penalty / Effect | In-Game Feedback |
| :--- | :--- | :--- | :--- |
| **Attack Phase** | Firing Accuracy | **$-20\%$ Hit Accuracy Penalty** | Firing under pinning fire reduces hit probability. |
| **Move Mode** | Movement Range | **$-1$ Hex / Tile Move Range** | Unit crouches behind cover / pinned to trench. |
| **Turn Refresh** | Initiative / AP | **$-2$ Max AP on Next Activation** | Pinned unit spends AP recovering operational posture. |
| **Status Tag** | Overhead Badge | **`[! PINNED !]` (Amber 0.62x)** | Rendered over unit health bar in `Draw_0.gml`. |
| **Cinematic** | Combat Popup | **`[PINNED // SUPPRESSED!]`** | Gold callout during cinematic impact. |

At the conclusion of the round, `hits_taken_this_turn` resets to 0. During turn refresh, suppressed units deduct 2 AP and clear `is_suppressed = false`, recovering their normal stance for subsequent rounds.

---

## 3. Pillar II: High-Ground Kinetic Velocity & Ballistics

### 3.1 Elevation Delta ($\Delta_{\text{Elev}}$)
$$\Delta_{\text{Elev}} = \text{Attacker Elev} - \text{Defender Elev}$$

### 3.2 High-Ground Advantage ($\Delta_{\text{Elev}} > 0$)
- **Kinetic Damage Velocity**: Gravity assist and unobstructed ballistic arcs amplify kinetic shell energy:
  $$\text{Damage}_{\text{Final}} = \text{floor}\left(\text{Damage}_{\text{Raw}} \times (1.0 + 0.15 \times \Delta_{\text{Elev}})\right)$$
- **Effective Firing Range**: Plunging fire extends effective weapon range:
  $$\text{Range}_{\text{Max, Effective}} = \text{Range}_{\text{Max}} + \max(0, \Delta_{\text{Elev}})$$
- **Line-of-Sight Accuracy**: $+10\%$ hit bonus per step of high ground:
  $$\text{Hit Bonus} = \Delta_{\text{Elev}} \times 10\%$$

### 3.3 Low-Ground / Uphill Disadvantage ($\Delta_{\text{Elev}} < 0$)
- **Upward Velocity Decay**: $-15\%$ kinetic damage mitigation:
  $$\text{Damage}_{\text{Final}} = \text{floor}\left(\text{Damage}_{\text{Raw}} \times \max(0.60, 1.0 - 0.15 \times |\Delta_{\text{Elev}}|)\right)$$
- **Defilade Aim Penalty**: $-15\%$ accuracy penalty per step shooting uphill into crested terrain:
  $$\text{Hit Penalty} = |\Delta_{\text{Elev}}| \times 15\%$$

---

## 4. Pillar III: Destructible Cover Degradation & Ordnance Penetration

### 4.1 Cover Fortification Tiers
1. **Level 2 (Reinforced Bastion / Concrete Bunker)**: $+40\%$ cover evasion, rendered with dark industrial plating and `[BASTION]` overhead badge.
2. **Level 1 (Shattered Rubble / Earthwork Trench)**: $+25\%$ cover evasion, rendered with textured rubble and `[RUBBLE]` overhead badge.
3. **Level 0 (Open Ground / Crater)**: $0\%$ cover evasion.

### 4.2 Heavy Ordnance Penetration
Weapons delivering high kinetic shock (Railguns, 120mm solid cannon, siege mortars, or weapons with base damage $\ge 55$):
- **Penetration Factor**: Ignores $50\%$ of target cover evasion during hit calculation:
  $$\text{Cover}_{\text{Effective}} = \text{floor}(\text{Cover}_{\text{Base}} \times 0.50)$$
- **Destructible Terrain Degradation**: Upon ordnance impact:
  - Bastions (Level 2) are fractured into Shattered Rubble (Level 1), spawning `[BASTION CRACKED -> RUBBLE]` popups.
  - Rubble (Level 1) is completely annihilated into Level 0 cratered terrain, spawning `[COVER DESTROYED]` popups.

---

## 5. Pillar IV: Directional Facing Angles & Flanking/Rear Core Strikes

### 5.1 Directional Facing Geometry
Isometric orientation is tracked across four cardinal isometric facings:
`0 = SE (Front-Right)`, `1 = SW (Front-Left)`, `2 = NE (Back-Right)`, `3 = NW (Back-Left)`.

Comparing defender facing $\theta_{\text{def}}$ against incoming vector $\theta_{\text{inc}} = \text{iso\_get\_facing}(\text{def}, \text{atk})$:
- **Frontal Confrontation**: $\theta_{\text{inc}} == \theta_{\text{def}}$ ($0^\circ$). Standard damage and defense.
- **Flanking Angle**: $\theta_{\text{inc}} == (\theta_{\text{def}} \pm 1) \pmod 4$ ($90^\circ$).
  - $+15\%$ Hit Accuracy.
  - $+20\%$ Flanking Kinetic Damage (`[FLANKING ANGLE +20%]`).
- **Rear Ambush**: $\theta_{\text{inc}} == (\theta_{\text{def}} + 2) \pmod 4$ ($180^\circ$).
  - $+30\%$ Hit Accuracy.
  - Bypasses $20\%$ Defender Thruster Evasion.
  - $+40\%$ Catastrophic Kinetic Damage (`[REAR CORE HIT +40%]`).
  - Critical Dispersion: $65\%$ chance to impact the Torso Reactor Core; $35\%$ chance to sever the Vernier Backpack.

---

## 6. Pillar V: Platoon Role AI Specialization & Tactical Forecast HUD

### 6.1 Dynamic AI Squad Roles
Hostile and mercenary units evaluate squad composition and assign tactical specializations:
1. **The Sniper / Fire Support** (`max weapon range >= 5`, e.g. Siegebreaker, Long-Range Cannon):
   - Scans adjacent tiles for higher elevation (`grid_elev > elev`).
   - Maintains maximum stand-off distance (`dist >= 4`), firing with high-ground velocity bonuses rather than rushing into close-quarters melee.
2. **The Flanker / Striker** (Melee, Shotguns, e.g. Muramasa, Reaver Brawlers):
   - Computes target facing vector $\theta_{\text{def}}$.
   - Maneuvers into rear/flank hexes before discharging weapons to secure $+40\%$ rear core strike bonuses.
3. **The Vanguard / Suppressor** (Standard Bipeds, Heavy Tanks, Platoon Grunts):
   - Coordinates fire onto allied units already targeted this turn (`hits_taken_this_turn > 0`) to trigger crossfire pinning.

### 6.2 Tactical Forecast HUD (`Draw_64.gml`)
When the player hovers over a hostile target in `TARGET_MODE`, the forecast panel expands to $180\text{ px}$ height, providing complete telemetry:
- **VECTOR**: Displays `REAR AMBUSH (+40% CORE DMG / +30% HIT)`, `FLANKING ANGLE (+20% DMG / +15% HIT)`, or `FRONTAL CONFRONTATION`.
- **TERRAIN**: Displays `HIGH GROUND +% VELOCITY / +% HIT`, `UPHILL LOW-GROUND PENALTY`, or `LEVEL ELEVATION`.
- **DEFENSE**: Displays cover tier (`[HEAVY BASTION: 40% COV]` or `[LIGHT RUBBLE: 25% COV]`) and suppression state (`[TARGET PINNED/SUPPRESSED]`).

---

## 7. Automated Test Suite Metrics
The entire Goal F subsystem is verified by `tools/test_goal_f_exhaustive.py`:
- `calculate_hit_chance` suppression, facing, elevation, and cover penetration: **PASSED (100%)**
- `recalculate_moves` suppression movement penalty: **PASSED (100%)**
- `start_battle_cinematic`, `update_battle_cinematic`, `skip_battle_cinematic`, and `resolve_combat_impact`: **PASSED (100%)**
- `Step_0.gml` AI Platoon roles (Sniper, Flanker, Vanguard) and turn refresh: **PASSED (100%)**
- `Draw_64.gml` Tactical Forecast HUD: **PASSED (100%)**
- `Draw_0.gml` Overhead badges (`[! PINNED !]`, `^Elev`, `[BASTION]`/`[RUBBLE]`): **PASSED (100%)**
- Mathematical simulation model: **PASSED (100%)**
- Full Project Lint & Syntax Validation (`tools/validate_project.py`): **0 ERRORS**
- Full Backward Regression Suite (Goals A, B, C, D, E, Tech Tree, HOI4): **PASSED (100%)**
