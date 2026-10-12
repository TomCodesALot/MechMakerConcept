# 04_faction_contracts.md
## Faction Economy & Contract System (The Strategic Loop)

### Core Philosophy
The player is a PMC/Arms Manufacturer, not just a frontline soldier. The strategic tension comes from balancing the checkbook against global politics. Selling top-tier Mobile Suits to one faction makes you rich, but tips the balance of the war. The player must navigate reputation, fulfill strict contract requirements, and occasionally field their own units in tactical combat to maintain corporate dominance.

---

### 1. The Factions (The Buyers & Employers)
The game tracks global standing with distinct geopolitical entities. 
*   **Faction A: The Terran Coalition (Earth-based)** - High budget, prefers heavy armor, kinetic weapons, and mass production. 
*   **Faction B: The Outer Colonies (Space-based)** - Lower budget, relies on high mobility, energy weapons, and high-tech prototypes.
*   **Faction C: Rogue Mercenary Syndicates** - Black market buyers. Pay incredibly well in rare raw materials, but interacting with them massively damages standing with Factions A and B.

*Variable to track:* `faction_standing` (Ranges from -100 to 100). Determines contract availability and market prices.

---

### 2. Contract Types
Contracts are generated dynamically by the `obj_FactionManager` based on the current state of the war map.

#### A. Mass Production Orders (The Bread and Butter)
*   **The Ask:** "We need 24 Heavy Assault suits within 30 days."
*   **The Catch:** The suits must meet a *minimum* stat threshold. The player uses saved Blueprints to fulfill this.
*   **Payout:** Large influx of standard Credits (Cr).
*   **Failure:** Missing the deadline incurs a massive financial penalty and loss of `faction_standing`.

#### B. Prototype Bounties (R&D Focused)
*   **The Ask:** "Our aces need a custom unit capable of outmaneuvering the enemy's new line."
*   **The Catch:** Extremely specific, high-tier stat requirements. Requires playing Prototyping Minigames to forge a Masterwork suit. Quantity: 1.
*   **Payout:** Rare materials (Tritium, Synthetic Flux) and high `faction_standing`.

#### C. Black Ops / Under-the-Table Sales
*   **The Ask:** Selling stripped-down or surplus mechs on the black market to Syndicates.
*   **The Catch:** Instant payout, no deadlines. Triggers a hidden `tech_leak_risk` roll. If failed, major factions discover the leak, resulting in a drastic drop in standing.

#### D. Combat Operations (Tactical Deployment)
*   **The Ask:** A faction directly hires your PMC pilots to defend a base, clear a pirate outpost, or hold a frontline trench.
*   **The Catch:** The player must transition to the Turn-Based Tactical Grid (`rm_combat`) and deploy their own inventory of mechs and hired pilots. 
*   **Payout:** Massive Credit injections and salvage rights (enemy mech parts).
*   **Failure/Risk:** Any mechs destroyed in combat are permanently lost from your inventory. Pilots killed are permanently dead (permadeath).

---

### 3. War Map Influence (The Macro Game)
The mobile suits the player sells and the battles they fight actually change the simulation.
*   Every week/turn, factions simulate battles on a background war map. 
*   Arming or fighting for a faction increases their `military_strength_score`, allowing them to capture territory.
*   **The Danger of Monopoly:** If one faction completely wins the war, demand for weapons plummets. The player must secretly arm both sides to prolong the conflict indefinitely.

---

### 4. Implementation Directives for the Coder
*   Build `obj_FactionManager` to hold an array of structs for active contracts.
*   Contract generation should be procedurally weighted based on the faction's current war status (e.g., losing factions offer more Combat Operations and Prototype Bounties).
*   Create a UI screen (`rm_contract_board`) to view active contracts, assign factory lines, or launch Combat Operations.
*   Use a global background timer (e.g., `global.current_day`) to track deadlines.
