# 05_tactical_combat.md
## Turn-Based Tactical Combat System

### Core Philosophy
Combat is deliberate, grid-based, and highly lethal. It heavily favors the player who brought the right mechs for the terrain. Success relies on Action Point (AP) management, positioning (flanking), and targeted component destruction.

---

### 1. The Grid and Scale
*   **Environment:** Combat takes place on a 2D isometric or top-down square grid (e.g., 64x64 pixel tiles).
*   **Scale Translation:** 
    *   1 Grid Cell = 50 Meters. 
    *   Weapon ranges in the JSON (e.g., `effective_range_m: 950`) must be divided by 50 to determine cell range (950m = 19 cells).
    *   Movement speed (`base_walk_speed_kph`) determines the base movement radius.

### 2. Action Points (AP) Economy
Every mech has a pool of Action Points per turn. 
*   **AP Calculation:** AP is directly derived from the mech's `net_power_surplus_mw` (from the Reactor) divided by its `total_weight_tonnes`. A heavy mech with a weak reactor might only get 3 AP; a light mech with a massive reactor might get 8 AP.
*   **Actions Cost AP:**
    *   Move 1 Cell: 1 AP (Increases in rough terrain like swamps or mountains).
    *   Fire Weapon: AP cost is tied to the weapon's `power_drain_mw`. Firing a Heavy Vulcan might cost 2 AP, while firing a massive Particle Cannon costs 5 AP.
    *   Brace/Defend: 2 AP (Increases Recoil Absorption and Evasion until next turn).

### 3. Combat Resolution & Component Targeting
When an attack occurs, it does not just hit a generic "Health Bar." It hits specific mech parts.
*   **Hit Chance:** Calculated by the attacker's `sensor_range` and Pilot Accuracy vs. the defender's `turn_rate_deg_per_sec` (Evasion) and terrain cover.
*   **Part Damage (The Front Mission mechanic):** If a hit lands, the game rolls to see which component takes the damage based on percentages (e.g., Torso 40%, Arms 20%, Legs 30%, Head 10%).
*   **Destruction Penalties:**
    *   **Arm Destroyed:** The weapon attached to that arm drops. It cannot be fired.
    *   **Legs Destroyed:** Movement range is reduced to 1 Cell. Evasion drops to 0%.
    *   **Head Destroyed:** Sensor range drops to 2 Cells. Accuracy plummets.
    *   **Torso Destroyed:** The mech explodes. The pilot is KIA or injured, and the unit is lost.

### 4. Heat Management in Combat
*   Firing weapons generates heat (`heat_per_shot`). 
*   At the end of a mech's turn, it cools down based on the chassis `heat_dissipation_rate`.
*   If Heat exceeds the maximum threshold, the mech suffers an **Overheat Penalty**: It loses AP on the next turn, and takes structural damage directly to the Torso.

---

### Implementation Directives for the Coder
*   Use A* (A-Star) pathfinding for movement and AI targeting using `mp_grid` functions built into GameMaker.
*   Create a State Machine for `obj_BattleManager` (States: `Player_Select`, `Player_Move`, `Player_Attack`, `AI_Turn`, `Turn_Resolution`).
*   Ensure the UI layer visually displays AP pools, hit percentages, and a wireframe damage readout of the targeted enemy mech before the player commits to an attack.
