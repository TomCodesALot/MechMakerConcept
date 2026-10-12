# 03_prototyping_minigames.md
## R&D Component Assembly (The Prototyping Loop)

### Core Philosophy
Once alloys are synthesized, they are expended to run Prototype Minigames. These minigames determine the final stat generation of a new component blueprint (e.g., Reactor, Limb, Backpack). High player skill results in a "Masterwork" component with boosted stats; poor execution results in wasted materials or a sub-par component with heavy penalties.

---

### 1. Minigame: Reactor Conduit Tuning
**Target Component:** Cores / Reactors
**Core Mechanic:** Frequency matching and heat management.
*   **The Setup:** The player is presented with a continuously fluctuating "Target Output Wave" (a sine wave) representing optimal fusion flow.
*   **Player Input:** The player controls three UI sliders (Frequency, Amplitude, Phase).
*   **The Goal:** Adjust the sliders to overlay the player's wave exactly onto the Target Wave. 
*   **Success/Fail States:** 
    *   Syncing the waves above 90% alignment fills the "Containment" bar. If filled, the Reactor is successfully prototyped with a +15% Power Output bonus.
    *   If alignment drops below 50%, the "Heat" bar rises. If Heat maxes out, the core melts down, destroying the alloys.

### 2. Minigame: Limb Stress Alignment
**Target Component:** Arms / Legs
**Core Mechanic:** Precision timing and structural load balancing.
*   **The Setup:** A wireframe schematic of the limb is displayed. As simulated weight is applied, microscopic stress fractures (red nodes) appear along the joints.
*   **Player Input:** The player must quickly move the mouse to the fracture nodes and click-and-hold to "weld" or align the armor plating. 
*   **The Goal:** Prevent any joint from hitting 100% stress while the simulation runs for 15 seconds.
*   **Success/Fail States:**
    *   Catching fractures instantly increases the final component's `armor_hp` and `recoil_absorption_pct`.
    *   Missing a fracture permanently reduces the limb's `load_capacity_tonnes`. If a joint breaks entirely, the prototype is scrapped.

### 3. Minigame: Thruster Plasma Flow Calibration
**Target Component:** Backpacks / Boosters
**Core Mechanic:** Throttle feathering (similar to a tension/fishing minigame).
*   **The Setup:** A vertical pressure gauge with a moving, fluctuating "Sweet Spot" zone that represents optimal plasma ignition.
*   **Player Input:** Pressing and holding the [SPACEBAR] or [Left Mouse Button] applies thrust, raising an indicator needle. Releasing drops it.
*   **The Goal:** Keep the indicator needle inside the randomly shifting Sweet Spot zone until the calibration timer finishes.
*   **Success/Fail States:**
    *   High time-in-zone grants a massive boost to `booster_thrust_kn` and reduces `power_drain_mw`.
    *   Hitting the extreme top (Overpressure) or bottom (Flameout) of the gauge damages the prototype, reducing overall efficiency.

---

### Implementation Directives for the Coder
*   Build these as discrete GameMaker rooms or as isolated UI layer overlays within the main R&D room.
*   Use `obj_minigame_manager` to handle the timers, input listening, and passing the final calculated stats back to the global `obj_GameManager`.
*   Ensure failure states correctly deduct the raw alloy inventory from the player's global resources without generating a usable blueprint.
