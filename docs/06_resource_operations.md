# 06_resource_operations.md
## Resource Operations & Mining System

### Core Philosophy
Purchasing base elements directly from the Interstellar Market eats into profit margins and prevents massive R&D scaling. To acquire raw materials (Tungsten, Tritium, Silica-Carbon, Synthetic Flux) at cost, the player must physically secure and hold Resource Nodes on the strategic map. This creates a severe opportunity cost: a Heavy Assault mech parked on a mining asteroid is a mech that cannot be sold or used in contract combat.

---

### 1. Resource Nodes (The Map Objectives)
The War Map contains static and shifting Resource Nodes. Each node has a specific yield rate and an ambient Threat Level.

| Node Type | Primary Yield | Secondary Yield | Threat Level | Environment Notes |
|---|---|---|---|---|
| **Asteroid Belt** | `mat_tungsten` | `mat_silica_carb` | Low to Medium | High pirate activity. |
| **Volcanic Moon** | `mat_silica_carb`| `mat_tungsten` | Medium | Passive heat damage requires high mech heat dissipation. |
| **Gas Giant Orbital** | `mat_tritium` | None | High | Contested by Factions. Constant raid risk. |
| **Derelict Shipyard**| `mat_syn_flux` | Scrap/Slag | Very High | Syndicate territory. |

---

### 2. The Deployment Mechanic (Opportunity Cost)
To extract resources, the player must deploy a Task Force (at least 1 Pilot and 1 owned Mobile Suit) to a specific node.
*   **The Lockout:** Deployed mechs are removed from the active inventory. They cannot be sold, scrapped, or used in Combat Operations while assigned to a node.
*   **Yield Calculation:** The amount of material mined per day/tick is heavily dependent on the deployed mech's stats. 
    *   A mech with a high `load_capacity_tonnes` (like the Ironclad's Colossus legs) pulls in more raw material per cycle.
    *   Specialized components (e.g., swapping a Heavy Vulcan for a "Plasma Mining Drill") exponentially increase extraction rates at the cost of combat viability.

### 3. Raids and Defense (The Risk)
Nodes are not safe. Every tick, the `obj_GameManager` rolls a background check against the node's Threat Level. If the node is raided by Pirates or a hostile Faction, an event triggers:
*   **Auto-Resolve (The Gamble):** The game calculates the deployed mech's combat stats (`total_armor_hp`, `total_power_output_mw`) against the raid strength. The mech may survive, take heavy structural damage, or be completely destroyed (costing you the pilot, the mech, and the node).
*   **Tactical Defense (Manual Intervention):** The player can choose to personally command the defense. The game transitions to `rm_combat` (using the rules from Doc 5). The player must survive the turn limit or destroy the attackers using the exact mech loadout they deployed. 

### 4. Supply Lines & Extraction
*   Mined resources do not instantly teleport to the lab. They sit in the node's local storage until the player orders an "Extraction Fleet."
*   If a node is overrun before resources are extracted, all accumulated materials are looted by the enemy.

---

### Implementation Directives for the Coder
*   Create an `obj_ResourceManager` or append to `obj_GameManager` to track an array/list of `struct_resource_node`.
*   Each node struct must track: `node_id`, `yield_type`, `yield_rate`, `current_storage`, `assigned_mech_id`, and `assigned_pilot_id`.
*   In the main Step Event timer (the daily tick), loop through all active nodes, add to their `current_storage` based on the assigned mech's load stats, and roll the raid probability check.
*   Build a UI panel (`rm_strategic_map`) where the player can drag and drop mechs from their inventory onto map nodes.
