# 07_base_management.md
## Base Operations & Personnel Management

### Core Philosophy
The PMC facility is the economic engine of the game. Fulfilling contracts and mining raw materials generates capital, but that capital must be aggressively reinvested into the base to scale operations. A player cannot fulfill late-game Terran Coalition mass-production orders out of a single-bay garage, nor can they safely synthesize highly volatile Tritium without a state-of-the-art crucible.

---

### 1. Personnel (The Human Capital)
The player must hire and manage staff to operate the PMC. Staff require an upfront hiring bonus and a recurring daily/weekly salary deducted from the global Credit pool.

#### A. Combat Pilots
*   **Role:** Assigned to Mobile Suits for Combat Operations and Resource Node defense.
*   **Stats:** 
    *   *Accuracy:* Directly increases hit chance in the tactical grid.
    *   *Reflexes:* Increases evasion and AP (Action Point) pools.
    *   *Morale:* Drops if they are frequently deployed to high-threat nodes or if their mechs take heavy damage. Low morale leads to desertion.
*   **Risk:** Permadeath. If a mech is destroyed (Torso HP hits 0), the pilot is KIA.

#### B. Engineering & R&D Staff
*   **Role:** Assigned to the Factory and Chemistry Lab.
*   **Stats:**
    *   *Metallurgy Skill:* Reduces the speed at which the `volatility_meter` rises during Alloy Chemistry, making Tritium synthesis safer.
    *   *Precision:* Widens the "Sweet Spot" and slows down the timers during the Prototyping Minigames, making Masterwork components easier to forge.

### 2. The Chemistry Lab (R&D Upgrades)
The lab dictates what alloys can physically be created. Attempting late-game recipes in a low-tier lab guarantees catastrophic failure.
*   **Crucible Tier 1 (Starting):** Max Heat: 3000°C. Max Pressure: 2000 PSI.
*   **Crucible Tier 2 (Upgrade):** Max Heat: 6000°C. Max Pressure: 10,000 PSI. Unlocks Tritium handling.
*   **Containment Shielding:** An upgrade path that prevents lab destruction. If a batch explodes, upgraded shielding ensures you only lose the materials, not the entire lab facility (which costs massive Credits to rebuild).

### 3. Factory Production Lines (Scaling Up)
When the player saves a Blueprint (like the GHA-07 Ironclad), they must manufacture it here.
*   **Assembly Lines:** The base starts with 1 Assembly Line, meaning only 1 Mobile Suit can be fabricated at a time. Upgrading adds concurrent lines.
*   **Fabrication Speed:** Determines how many days it takes to build a mech based on its `fabrication_time_days` stat. Upgrading robotics reduces this time by percentages (e.g., a 12-day build becomes an 8-day build).
*   **Strategic Impact:** To fulfill a "24 Suits in 30 Days" Mass Production contract, the player mathematically *must* have upgraded to at least 4 active assembly lines running simultaneously.

---

### Implementation Directives for the Coder
*   Integrate facility tracking into `obj_GameManager` (e.g., `global.base_lab_tier = 1`, `global.base_assembly_lines = 1`).
*   Create an array or `ds_list` to store hired personnel structs (e.g., `global.roster_pilots`, `global.roster_engineers`).
*   Build `rm_base_management`, a purely UI-driven room with three main tabs: Personnel (roster and hiring market), Factory (line assignments and upgrades), and R&D (lab upgrades).
*   In the daily tick event, subtract total staff salaries from `global.funds`. If funds drop below 0, trigger a bankruptcy warning state.
