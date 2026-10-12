# 08_narrative_events.md
## Narrative Systems & Dynamic Events

### Core Philosophy
The world must feel alive and responsive to the player's actions as a PMC commander. Static numbers are boring; the Narrative Designer agents will write text that frames these variables as real-world consequences. Events force the player to adapt their strategy mid-month.

### 1. The Event Engine
Events are structured as JSON files containing flavor text, trigger conditions, and mechanical consequences. The `obj_EventManager` rolls for random events during the daily tick, or triggers conditional events based on player actions.

### 2. Event Categories
*   **Market Shocks:** 
    *   *Example:* "Tritium Embargo." Outer Colonies blockade gas giants. Tritium prices skyrocket by 300% for 14 days. 
    *   *Player Choice:* Sell their Tritium stockpile for massive profit, or hoard it to keep prototyping high-tier cores.
*   **Personnel Dilemmas:**
    *   *Example:* "Hazard Pay Strike." A high-threat mining node was raided. Pilots demand a 20% permanent salary increase or they walk.
    *   *Player Choice:* Pay up (lose Credits), or fire them (lose experienced high-accuracy pilots).
*   **Geopolitical Shifts:**
    *   *Example:* "Syndicate Leak." A Terran Coalition spy discovers the player sold Ironclad blueprints to the Black Market. 
    *   *Consequence:* Instant -40 standing with the Coalition; Coalition mass-production contracts are locked for 30 days.

### 3. Implementation Directives for the Coder
*   Build an `obj_EventManager` that loads a `narrative_events.json` file.
*   Create a UI popup layer (`obj_event_popup`) that pauses the background timer, displays the Narrative Designer's flavor text, and presents 1 to 3 clickable choices.
*   Write a script `scr_trigger_event(event_id)` that applies the mathematical consequences (deducting funds, altering standing, modifying market prices) based on the player's choice.
