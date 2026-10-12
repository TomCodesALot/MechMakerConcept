# 01_core_architecture.md
## Global Systems & Save Structure

### Core Philosophy
This GameMaker project relies on persistent singleton objects to manage global state. Data is passed between rooms via these managers, not by global variables scattered across scripts. Save data is serialized strictly into JSON formats to allow easy debugging and future modding support.

### 1. Global Manager Objects
The Coder must instantiate these objects in a persistent boot room (`rm_init`) before moving to the main menu.
*   `obj_GameManager`: Holds current funds (Cr), current date/turn, and the player's active inventory (alloys, components, and deployable mechs).
*   `obj_FactionManager`: Tracks standing with Factions A, B, and C, and stores the array of currently active contracts.
*   `obj_BlueprintManager`: Loads and stores the JSON data for all unlocked mechs and components.
*   `obj_BattleManager`: Handles tactical combat state, turn queues, grid pathfinding, and AI targeting during Combat Operations.

### 2. Save/Load Serialization
*   **The Save File:** All game progress is saved as `pmc_save_slot_1.json`.
*   **Saving:** The Coder must write a script (`scr_save_game`) that packs the structs from all Manager objects into a single master struct, uses `json_stringify()`, and writes it to the local AppData/datafiles directory.
*   **Loading:** `scr_load_game` reads the JSON, uses `json_parse()`, and unpacks the data back into the respective Manager objects.
