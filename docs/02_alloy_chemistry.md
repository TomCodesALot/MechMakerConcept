# 02_alloy_chemistry.md
## R&D Alloy Chemistry System (The Mixing Loop)

### Core Philosophy
The prototyping phase must replicate the addictive, trial-and-error discovery of underground chemistry loops. Players risk raw capital (base elements) to discover proprietary PMC alloy formulas. Once a recipe is discovered, it is permanently unlocked for the Assembly line. Failed experiments result in wasted capital and dangerous byproducts.

---

### 1. The Base Elements (Tier 1 Raw Materials)
These are purchased from the interstellar market or salvaged from contracts.

| Element ID | Name | Properties & Behavior | Base Cost / Unit |
|---|---|---|---|
| `mat_tungsten` | Raw Tungsten | High density, extremely high heat tolerance. | 400 Cr |
| `mat_silica_carb`| Silica-Carbon | Lightweight, brittle, reduces overall mass. | 150 Cr |
| `mat_syn_flux` | Synthetic Flux | Catalyst. Rapidly accelerates chemical reactions. | 800 Cr |
| `mat_tritium` | Plasma-Charged Tritium | Highly volatile energy source. High explosive risk. | 1,200 Cr |

---

### 2. The Process Variables (The Minigame Math)
Mixing is not instant. The player must set the environmental variables of the synthesis crucible. The Coder must track these states per tick:

*   **Crucible Heat (`crucible_temp_c`):** Ranges from 0°C to 5000°C. Elements melt and bind at specific heat thresholds.
*   **Crucible Pressure (`crucible_pressure_psi`):** Ranges from 14.7 (Atmospheric) to 10,000 PSI.
*   **Volatility (`volatility_meter`):** A background variable (0-100%). If this hits 100%, the crucible breaches, destroying the batch and damaging the lab facility.

---

### 3. The Hidden Recipes (Examples for Implementation)
To discover an alloy, the player must combine the exact ratio of elements and hold the crucible within the target environmental thresholds for a specific duration (e.g., 5 seconds).

#### Recipe 1: Vanguard Composite (Basic Armor)
*   **Input:** 2x `mat_tungsten`, 1x `mat_silica_carb`
*   **Conditions:** Heat between 2200°C - 2500°C. Pressure < 1000 PSI.
*   **Result:** `alloy_vanguard_comp` (Used to build Tier 1 limbs and chassis).
*   **Failure State:** If heat exceeds 2500°C, the carbon burns away. Yields `item_slag`.

#### Recipe 2: Hyperion Core Matrix (Reactor Component)
*   **Input:** 1x `mat_tungsten`, 2x `mat_tritium`, 1x `mat_syn_flux`
*   **Conditions:** Heat exactly at 4500°C (tight tolerance). Pressure > 8000 PSI.
*   **Volatility Warning:** Mixing Tritium and Flux increases `volatility_meter` by 15% per second. The player must vent pressure periodically to survive the synthesis phase.
*   **Result:** `alloy_hyperion_matrix` (Required for heavy fusion cores).
*   **Failure State:** If `volatility_meter` hits 100%, catastrophic explosion. 

#### The Byproduct: Slag
*   **Result ID:** `item_slag`
*   **Mechanic:** Any failed mix results in Slag. It takes up inventory space. It can be sold to scrap brokers for 10% of the original material cost, creating a minor economic safety net for failed experiments.

---

### 4. Implementation Directives for the Coder
*   Use a JSON array or a `ds_map` to store the hidden recipes. 
*   Do not hardcode recipes into the step events. Build a script (e.g., `scr_check_alloy_recipe()`) that compares the current crucible contents and environment variables against the JSON recipe list every frame.
*   If a match is sustained for the required duration, trigger the success state and clear the crucible.
