# Document 56: Advanced Character Stats, Pilot Fatigue & Trait Mutation Engine
**Milestone 56: Manual Stat Point Allocation, Cockpit Sortie Fatigue & Battle Scar Trait Mutations**

---

## 1. Executive Summary & Design Scope

Milestone 56 completes the RPG Character System of the Mobile Suit PMC Simulation. Building upon the Pilot Roster (Doc 51), Master Dialogue Bible (Doc 53), and Cantina Bonds (Doc 55), Milestone 56 empowers commanders with deep, granular progression and personnel management:

1. **Manual Stat Point Allocation on Level-Up**:
   - As pilots earn Combat XP across sorties, crossing Level boundaries (150 XP per Level) awards **+2 Unallocated Stat Points**.
   - In `obj_HQTerminal` (Pilots Deck, Subtab 0), commanders can manually invest points into:
     - **Accuracy (`accuracy`)**: +2% Hit probability per point (Capped at 99%).
     - **Reflexes (`reflexes`)**: +2% Thruster dodge & counter-attack speed per point (Capped at 99%).
     - **Combat Stat (`combat_stat`)**: +1 Aimed shot & melee power per point (Capped at 10/10).
     - **Tactics Stat (`tactics_stat`)**: +1 Electronic warfare resistance & initiative per point (Capped at 10/10).

2. **Cockpit Fatigue & Sortie Rotation Stress**:
   - High-G combat and reactor heat place immense strain on pilot nervous systems.
   - Each combat sortie increases a pilot's `fatigue` by **+25** (out of 100).
   - If an allied mech suffers a critical limb breach or emergency ejection, fatigue surges by **+40**.
   - **Fatigue Tiers & Degradation**:
     - `0 – 24 (Rested)`: Peak performance. Zero penalties.
     - `25 – 49 (Winded)`: Minor muscle tremor (-5% Weapon Accuracy).
     - `50 – 74 (Fatigued)`: Cockpit disorientation (-10% Accuracy, -10% Reflexes, -1 AP on Turn 1).
     - `75 – 100 (Exhausted / Combat Shock)`: Severe neuro-fatigue (-20% Accuracy, -20% Reflexes, risk of cockpit panic suppression).
   - **Recovery & R&R Leave**:
     - Pilots resting between strategic turns passively recover **-25 Fatigue** per cycle in the crew quarters.
     - In the Cantina (Pilots Deck, Subtab 1), commanders can grant **Rest & Recuperation (R&R) Leave** (-5,000 Credits) to instantly reset fatigue to 0 and boost Morale by +10.

3. **Dynamic Trait Mutations & Battle Scars**:
   - Surviving harrowing combat situations or achieving lethal combat milestones mutates permanent character traits:
     - **"Iron Survivor"**: Mutates after surviving a catastrophic torso reactor breach via emergency ejection. Grants +15% Ejection survival chance and +5 Max Morale.
     - **"Ace Predator"**: Mutates after scoring 5+ confirmed combat kills. Grants +12% Critical Kinetic Damage, and hostile units targeting this pilot suffer -10 Morale.
     - **"Ghost of Phobos"**: Mutates after surviving high-stress space/orbital sorties with fatigue >= 50. Grants +10% Thruster Evasion in space theaters.
     - **"Cybernetic Reflex Augment"**: Mutates upon discharge from ICU convalescence. Grants +6% Aimed Shot Accuracy (with +25 Cr daily neuro-fluid upkeep).

---

## 2. Mathematical Models & Formulas

### A. Level-Up Threshold Formula
$$\text{Level} = 1 + \left\lfloor \frac{\text{XP}}{150} \right\rfloor$$
$$\text{Stat Points Earned} = \Delta \text{Level} \times 2$$

### B. Combat Accuracy Modified by Fatigue
$$\text{Net Accuracy} = \text{Base Accuracy} + (\text{Combat Stat} \times 1.5) + \text{Affinity Resonance (+8)} - \text{Fatigue Penalty}$$
$$\text{Fatigue Penalty} = \begin{cases} 0 & \text{if } \text{fatigue} < 25 \\ 5 & \text{if } 25 \le \text{fatigue} < 50 \\ 10 & \text{if } 50 \le \text{fatigue} < 75 \\ 20 & \text{if } \text{fatigue} \ge 75 \end{cases}$$

---

## 3. Technical Architecture & GML Implementation

### 1. `obj_GameManager/Create_0.gml`:
- Added `allocate_pilot_stat(_pilot_idx, _stat_name)`
- Added `send_pilot_on_rr(_pilot_idx)`
- Added `mutate_pilot_trait(_pilot_idx, _trait_name)`
- Upgraded `pilot_add_xp(_pilot_id, _xp_gain)` with automatic Level-Up calculation and unspent stat point issuance.
- In `end_turn()`: Automated passive fatigue recovery (-25 fatigue per cycle for undeployed roster pilots).

### 2. `obj_BattleManager/Create_0.gml`:
- In `calculate_hit_chance()`: Applied live pilot fatigue penalties (-5% to -20% accuracy).
- In combat resolution: Checked kill and ejection milestones for automatic trait mutations (`"Ace Predator"`, `"Iron Survivor"`).

### 3. `obj_HQTerminal/Draw_64.gml`:
- **Pilots Deck (Subtab 0 - Active Squadron)**:
  - Rendered `Unspent Stat Points` badge and interactive `[+ ACC]`, `[+ REF]`, `[+ CMB]`, `[+ TAC]` buttons.
  - Rendered real-time Pilot Fatigue Gauge with color-coded status (`RESTED`, `WINDED`, `FATIGUED`, `EXHAUSTED`).
  - Rendered active `Mutated Traits` badges.
- **Cantina Deck (Subtab 1 - Cantina Registry)**:
  - Added `[GRANT R&R LEAVE (-5,000 Cr)]` button to clear fatigue immediately.

---

## 4. Verification Standards
- Zero syntax errors in `python3 tools/validate_project.py`.
- 100% test pass in `tools/test_milestone_56_stats_fatigue_and_traits.py`.
- Full regression-free integration with Milestone 51-55 test harnesses.
