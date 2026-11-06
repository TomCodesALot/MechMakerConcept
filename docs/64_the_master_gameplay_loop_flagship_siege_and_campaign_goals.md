# Document 64: The Master Gameplay Loop, Flagship Siege Protocol, & Grand Campaign Goals
**Document Version:** 1.0.0  
**Role:** Lead Game Developer & Technical Systems Architect  
**Target Engine:** GameMaker Studio 2 (Modern GML)  
**System Integrations:** `obj_GameManager`, `obj_HQTerminal`, `obj_BattleManager`, `obj_FactionManager`  
**Narrative & Design Baseline:** *Front Mission 3*, *Armored Core: For Answer*, *Mobile Suit Gundam: Gihren's Greed*, *Mount & Blade*

---

## 1. Executive Direction: Answering the Core Questions

### Question 1: "Are we going in the right direction?"
**Yes, but we must unify our subsystems into an unmistakable, driving compulsion loop.**

We have built exceptional, deep individual engines:
* A 2:1 axonometric isometric tactical combat engine with modular limb targeting and handcrafted 160x160 pixel art (`obj_BattleManager`).
* A tactile metallurgy and molecular sintering minigame (`obj_HQTerminal`).
* A dynamic procurement fly-off simulation that obsoletes state models (`obj_BlueprintManager`).
* A 60-year pre-war history and authentic MSV mecha progression trees (`docs/57` through `63`).

**Why it feels jumbled:**  
When systems are developed in isolation, they feel like disparate mini-games. To feel like a real game, every action in the Hangar must serve a tactical goal on the War Map, and every victory on the War Map must feed resources directly back into the Crucible. The connective tissue is the **Compulsion Loop**.

---

## 2. What is the Main Goal of the Game?

### The Core High-Concept Hook:
> *"You are an indebted asteroid scrapper who stumbled into the holy grail of mechanized warfare: a lost pre-war automated mobile suit foundry. Can you turn a rusted ghost ship into a sovereign military-industrial empire before the four superpowers tear you—and the solar system—apart?"*

### The 3-Tier Progression Horizon:

```
+-------------------------------------------------------------------------------------------------------+
|                                    THE 3 CAMPAIGN PROGRESSION PHASES                                  |
+-------------------------------------------------------------------------------------------------------+
| PHASE 1: SURVIVAL & FOUNDATION (Turns 1 - 20)                                                         |
| • Goal: Keep the life support running, clear your 30,000 credit debt, and survive pirate ambushes.   |
| • Gameplay: Scavenge Cascadia scrap, sinter your first Vanguard Composite, build Unit-01 Ironclad.   |
|                                                                                                       |
| PHASE 2: THE INDUSTRIAL ARMS RACE (Turns 21 - 80)                                                     |
| • Goal: Out-engineer superpower state corporations and dominate interplanetary military contracts.    |
| • Gameplay: Enter Faction Procurement Fly-Offs, license your mechs for royalties, upgrade the ship's  |
|   8 divisions, and recruit veteran pilots in the Cantina.                                             |
|                                                                                                       |
| PHASE 3: THE ENDGAME HEGEMONY (Turns 81+)                                                             |
| • Goal: Achieve one of the 4 Grand Victory Conditions and decide the political fate of Sol.           |
| • Gameplay: Repel full fleet assaults from alienated superpowers, crush the Apex Nemesis Crisis, and  |
|   dictate the new galactic order.                                                                     |
+-------------------------------------------------------------------------------------------------------+
```

---

## 3. The Golden Compulsion Loop (Turn-to-Turn Rhythm)

Every strategic turn in *MechMaker Concept* follows a tight, satisfying 4-step loop:

```
                      ┌────────────────────────────────────────┐
                      │ 1. SCAVENGE & SECURE (The War Map)     │
                      │ Take mercenary contracts, mine nodes,  │
                      │ or deploy to tactical skirmishes.      │
                      └───────────────────┬────────────────────┘
                                          │ Raw Alloys & Credits
                                          ▼
                      ┌────────────────────────────────────────┐
                      │ 2. SINTER & FORGE (The Crucible)       │
                      │ Melt custom alloys, optimize molecular │
                      │ purity, and engineer new prototypes.   │
                      └───────────────────┬────────────────────┘
                                          │ Assembled Mobile Suits
                                          ▼
                      ┌────────────────────────────────────────┐
                      │ 3. COMPETE & COMMERCE (Contracts)      │
                      │ Enter corporate fly-offs, win tenders, │
                      │ or deploy custom lances to sorties.    │
                      └───────────────────┬────────────────────┘
                                          │ Wealth, Standing, Power
                                          ▼
                      ┌────────────────────────────────────────┐
                      │ 4. UPGRADE & SURVIVE (The Fleet Deck)  │
                      │ Refit the Hephaestus, train ace pilots,│
                      │ and defend against hostile incursions. │
                      └───────────────────┬────────────────────┘
                                          │ Next Turn Advanced
                                          └───────► (Loop)
```

1. **Step 1: Scavenge & Secure (`obj_HQTerminal.deck == 1: WAR MAP`)**:
   * Inspect contested sectors across Earth, Space, and Mars.
   * Accept high-paying faction contracts (Escort, Sector Defense, Sapper Assault).
   * Deploy tactical platoons to 2:1 isometric combat in `rm_combat`.
2. **Step 2: Sinter & Forge (`obj_HQTerminal.deck == 3: R&D FORGE`)**:
   * Use salvaged Tungsten, Titanium, Silica, and Slag in the Crucible minigame.
   * Assemble custom mobile suits using the CAD modular socket system.
3. **Step 3: Compete & Commerce (`obj_HQTerminal.deck == 4: CONTRACTS`)**:
   * Submit prototypes to superpower military tenders (Terran Linebreaker, Colony Interceptor).
   * Win contracts to replace incumbent state models, collecting recurring royalties.
4. **Step 4: Upgrade & Survive (`obj_HQTerminal.deck == 5: FLEET`)**:
   * Upgrade the *Hephaestus* (Fabrication Tier, Propulsion, Shields, Point-Defense).
   * Manage pilot fatigue, allocate level-up stats, and prepare for superpower retaliation.

---

## 4. The Flagship Defense Protocol: Hostile Fleet Assaults

While superpowers begin with cautious commercial cooperation, **hostility has real, lethal consequences**. 

If the player alienates a superpower (`standing <= -80` or `FACTION_STATE == WAR`), the enemy high command abandons restraint. They conclude that the player's PMC is an existential threat that must be captured or destroyed at all costs, launching **"OPERATION FORGE BREACH"**.

```
+-------------------------------------------------------------------------------------------------------+
|                                    FLAGSHIP SIEGE EVENT ARCHITECTURE                                  |
|                                                                                                       |
|  [ HOSTILITY TRIGGER ]     --> Standing <= -80; enemy task force intercepts the Hephaestus.          |
|  [ PRE-BATTLE SIREN ]      --> Red alert klaxons; Ares-V reports incoming capital ship fleet.        |
|  [ HULL DEFENSE BATTLE ]   --> Tactical combat deployed directly onto the exterior hull of the ship.  |
|  [ STAKES & CONSEQUENCES ] --> Defeat = Game Over (Foundry captured). Victory = Massive naval salvage. |
+-------------------------------------------------------------------------------------------------------+
```

### Mechanics of the Flagship Siege:
1. **The Tactical Staging Ground**:
   * The battle does not occur on a standard asteroid or mud map. It deploys onto **`rm_combat_flagship_hull`**—the massive exterior armor plating of the *Hephaestus* itself.
   * Environmental hazard: Vacuum micro-debris and point-defense flak bursts.
2. **Enemy Attack Waves**:
   * **Wave 1: Breaching Torpedoes & Gunships**: Fast atmospheric gunships and missile skiffs attempting to disable ship thrusters.
   * **Wave 2: Marine Shock Mobile Suits**: Elite enemy platoons carrying thermal lances and boarding clamps trying to breach the airlocks.
   * **Wave 3: The Superpower Ace / Nemesis**: The faction's champion (e.g., General Vance's custom Titan, Cassian's Aether, Lord Takahashi's Muramasa Shadow) deploying to personal duel the player.
3. **The Stakes**:
   * **Failure**: Hull breach -> Game Over.
   * **Victory**: Complete destruction of an enemy task force; yields massive amounts of rare pre-war isotopes, high-tier naval salvage, and permanently breaks the enemy faction's offensive capacity for 20 turns.

---

## 5. The Four Grand Campaign Endings

The game concludes when the player achieves one of four distinct geopolitical milestones:

1. **Path 1: The Corporate Monopolist (Economic Victory)**:
   * *Requirement*: Win mass-production replacement tenders with $\ge 3$ superpowers OR acquire majority equity in 3 megacorporations.
   * *Outcome*: Every military in Sol fires your weapons and marches in your armor. You control the war economy without firing a shot.
2. **Path 2: The Supreme Warlord Hegemon (Military Victory)**:
   * *Requirement*: Conquer $\ge 60\%$ of total planetary and orbital nodes, or directly conquer the three planetary capitals (Baikal, Selene Zenith, Olympus Caldera).
   * *Outcome*: You crush the state armadas and establish an ironclad *Mercenary Pax Hegemonia*.
3. **Path 3: The Archeotech Transcendent (Technological Victory)**:
   * *Requirement*: Fully upgrade all 8 divisions of the *Hephaestus* to Tier 5 and awaken the pre-war zero-point singularity.
   * *Outcome*: The *Hephaestus* unlocks instantaneous spatial folding, elevating your PMC beyond the reach of conventional planetary fleets.
4. **Path 4: The Sovereign Savior (Crisis Victory)**:
   * *Requirement*: Advance to Era IV and defeat the rogue automated biomechanical superweapon swarm (*The Apex Anomaly*).
   * *Outcome*: When humanity stood on the brink of extinction, your ace vanguard held the line and saved civilization.

---

## 6. Development Action Plan: Grounding the Experience

To ensure the game feels cohesive immediately, our technical roadmap focuses on:
1. **Tightening the Onboarding Cadre**: Ensuring the transition from scrapper questionnaire -> finding the ship -> building first mech -> first combat sortie feels like an unbroken cinematic prologue.
2. **Visible Feedback Loop**: Showing how winning a contract or conquering a node immediately displays your mechs deployed in that territory on the War Map.
3. **Flagship Siege Crisis Integration**: Hooking up the `standing <= -80` threshold to trigger the high-stakes exterior hull defense battle.

