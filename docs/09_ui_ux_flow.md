# 09_ui_ux_flow.md
## Game States & UI/UX Navigation Flow

### Core Philosophy
The player is a commander sitting at a terminal. Navigation between systems must be seamless. Instead of constantly loading distinct GameMaker rooms, the game should ideally use a central Hub room with UI panels that slide in and out, maintaining a persistent top-bar HUD.

### 1. The Persistent HUD (Always Visible)
No matter what screen the player is on, the top 10% of the screen must always display:
*   Current Funds (Cr)
*   Current Date (e.g., Year 214, Day 45)
*   Background Timer Toggle (Play, Pause, Fast-Forward)
*   Alert Feed (Scrolling ticker of incoming contracts or node raids)

### 2. The Navigation Hub (rm_hq_terminal)
This is the main room. It contains a sidebar or bottom nav-bar with the following access points:
*   **The Blueprint Lab:** Opens the mech visualization, prototyping minigames, and alloy crucible.
*   **The Factory Floor:** Opens assembly line management and personnel hiring.
*   **The Contract Board:** Opens the faction contract list and standing overview.
*   **The Strategic War Map:** Opens the global map for deploying mining teams and viewing faction territory.

### 3. The Combat Transition
*   When a Node Defense or Combat Operation is triggered, the game transitions entirely out of `rm_hq_terminal` and loads `rm_combat`. 
*   Once combat resolves, the `obj_BattleManager` calculates losses and salvage, displays an After-Action Report (AAR) screen, and returns the player to `rm_hq_terminal`.

### Implementation Directives for the Coder
*   Use a State Machine within `obj_UIManager` to handle which panels are drawn.
*   Use GameMaker's GUI Layer (the `Draw GUI` event) for all menus so they scale correctly regardless of camera position on the Strategic Map or Combat Grid.
