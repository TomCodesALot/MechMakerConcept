# 42. Strategic Logistics, Pilot Lifecycle & Flagship Dreadnought Operations
**Document Version:** 1.0.0  
**Roles:** Lead Game Designer (Director GDD), GameMaker Coder, Lead QA Engineer  
**Target Engine:** GameMaker Studio 2 (Modern GML)  
**Aesthetic Baseline:** *Front Mission* (Wanzer Pilot Roster & Hospitalization), *Gihren's Greed* (Theater Staging & Strategic Dispatch), *Battletech* (Upkeep & Fuel Burn)

---

## 1. Executive Summary

This specification links three foundational strategic systems in *MechMakerConcept*:
1. **Goal A: Strategic Logistics, Fleet Upkeep & Supply Starvation:** Fielded forces demand continuous capital expenditure (payroll & servicing) and Tokamak containment fuel (Tritium). Deficit spending induces crippling operational debuffs.
2. **Goal B: Full Mercenary Pilot Lifecycle & Casualties:** Pilots accumulate combat fatigue from sorties, earn XP unlocking Ace Perks (*Quick Draw*, *Deadeye*, *Overdrive*), and suffer temporary hospitalization or permanent death on reactor detonation.
3. **Goal C: Mobile Orbital Flagship Operations (USN-X Hephaestus):** The pre-war dreadnought orbits a specific strategic theater (Earth, Space, or Mars), projecting local mining yield multipliers and tactical orbital artillery strikes.

---

## 2. Strategic Logistics & Fleet Upkeep (Goal A)

### 2.1 Upkeep Calculus
Each strategic calendar turn, the finance engine resolves operational burn:
- **Chassis Maintenance:** $350$ Cr per deployable mech in hangar inventory.
- **Tritium Fuel Burn:** $1$ unit of Tritium (`mat_tritium`) consumed per $2$ deployable mechs (minimum $1$ unit if fleet size $> 0$).
- **Personnel Payroll:** Base salary per active pilot and engineer.

$$\text{Turn Burn} = \text{Payroll}_{\text{Roster}} + (\text{Mechs} \times 350\text{ Cr}) + \text{Assembly Line Fixed Costs}$$
$$\text{Tritium Burn} = \max\left(1, \left\lceil \frac{\text{Mechs}}{2} \right\rceil\right)$$

### 2.2 Supply Starvation State
If treasury drops below zero or Tritium fuel reserves are depleted:
$$\text{supply\_starvation} = \text{true}$$
- **Combat Penalties:** Allied units on the tactical battle grid suffer:
  - $-2$ Maximum Action Points ($\text{Max AP} = \max(1, \text{Max AP} - 2)$)
  - $-25\%$ Evasion penalty
  - Overboost vector thrusters disabled
- **UI Indication:** Top command header bar displays flashing `[⚠ SUPPLY DEFICIT!]` in crimson red.

---

## 3. Pilot Lifecycle, Fatigue & Ace Perks (Goal B)

### 3.1 Combat Fatigue & Resting
- **Sortie Accumulation:** Participating in a tactical battle increments a pilot's fatigue by $+1$ (capped at $5$).
- **Fatigue Debuff:** If $\text{fatigue} \ge 3$, the pilot suffers **Combat Exhaustion**:
  - $-15\%$ Hit Accuracy
  - $-15\%$ Reflexes & Evasion
- **Hangar Rest:** Leaving an active pilot unassigned for a strategic turn naturally dissipates $-1$ fatigue.

### 3.2 Combat Experience & Ace Perks
Pilots earn $+40$ XP per victory ($+15$ on defeat) plus $+25$ XP per confirmed kill:
- **Rank 1 (100 XP) — Quick Draw:** Allied chassis starts Turn 1 with $+1$ bonus Action Point.
- **Rank 2 (250 XP) — Deadeye:** $+15\%$ Critical Hit Chance on all mounted weapons.
- **Rank 3 (500 XP) — Overdrive:** When chassis Torso HP drops below $50\%$, deal $+20\%$ raw weapon damage.

### 3.3 Hospitalization & Convalescence
Torso catastrophic breach triggers pilot survival check:
- Clean ejection ($65\%$): Pilot safe.
- Hospitalization ($23\%$): Pilot status set to `"HOSPITALIZED"` with a $3$-turn recovery countdown.
- K.I.A. ($12\%$): Permanent loss; ace portrait retired to the PMC Memorial Wall.
- **Flagship Medbay Acceleration:** Upgrading the *Hephaestus* Pilot Suite (Deck 6) to Tier 2+ doubles the medical recovery rate from $1$ turn/turn to $2$ turns/turn.

---

## 4. Flagship Orbit Stationing & Transit Engine (Goal C)

### 4.1 Theater Stationing & Projection
The *USN-X Hephaestus* is stationed over one of the three strategic theaters:
1. **Earth Sphere** (Low Earth Orbit & L-5 Lagrange)
2. **Space & Colonies** (Asteroid Belt & Jovian Moon System)
3. **Mars Sphere** (Phobos & Olympus Redoubt)

### 4.2 Tactical Fire Support & Mining Boost
- **Local Mining Multiplier:** Nodes located within the flagship's orbital sphere receive the full `mining_tier` boost ($+25\%$ up to $+250\%$).
- **Tactical Combat Integration:** If a battle occurs in the flagship's current theater, command buffs (+2 AP, +20% accuracy at Command Tier 5) and orbital artillery strikes remain active. If the flagship is en route or in another planetary sphere, orbital fire support is offline.
- **Transit Speed:** Traveling between planetary spheres takes $3$ turns (Tier 1) $\rightarrow$ $2$ turns (Tier 2) $\rightarrow$ $1$ turn (Tier 3-4) $\rightarrow$ **$0$-turn Instant Tachyon Fold Warp** (Tier 5 / *Shadow Panopticon*).
