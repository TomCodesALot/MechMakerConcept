# 38. The Prometheus Catalyst: Conventional Warfare, Mobile Suit Genesis & The 1-Year Reverse-Engineering Arms Race
**Document Version:** 1.0.0  
**Roles:** Lead Game Designer (Director GDD), Narrative Designer, Lead GameMaker Developer, Technical Game Artist, Lead QA Engineer  
**Target Engine:** GameMaker Studio 2 (Modern GML)  
**Aesthetic Baseline:** 16-Bit Super Nintendo Military Simulation (*Front Mission SNES*, *Gihren's Greed*, *Super Robot Wars 4*)

---

## 1. Executive Summary & Foundational Narrative

In *MechMaker Concept: Iron Vanguard*, the universe does not begin with mobile suits already saturating every frontline. Instead, **the player's independent PMC is the singular technological catalyst that invents and deploys the first operational bipedal Mobile Suit in human history.**

Prior to the player's breakthrough, the Sol system is locked in a brutal, conventional war of attrition fought with **Main Battle Tanks, atmospheric and orbital Strike Jets, Hovercraft Skiffs, Heavy Artillery Crawlers, and Armored Technicals**.

When the player completes the first humanoid Tokamak-powered frame (Unit-01: *The Ironclad Prototype*) and deploys it in battle, the geopolitical landscape suffers a massive shockwave:
1. **The Conventional Era (Era 0):** All factions field tanks, jets, and crawlers. The superpowers treat the player's small PMC with hostility, dismissive cynicism, and punitive trade tariffs.
2. **The Catalyst Sortie (The Genesis Event):** The player's first mobile suit steps onto the battlefield, leaping trenches, shrugging off 90mm tank shells, and ripping armored turrets off main battle tanks.
3. **The Global Diplomatic Flip:** Overnight, every faction freezes open hostility toward the player. Military procurement boards scramble to hire the player's lone suit at astronomical bounty rates (2.5x - 4.0x payout) while begging to purchase blueprints or chassis units.
4. **The 365-Day Reverse-Engineering Arms Race:** Four rival megacorporations (Vanguard Heavy Industries, Astraea Orbital Dynamics, Rustworks Scrap Forge, Hyperion Cybernetics) launch aggressive industrial espionage programs, using telemetry, black-market combat salvage, and defector engineers to reverse-engineer the player's technology. Exactly one in-game year after the first deployment, the first rival prototype mobile suits hit the battlefield.

```
+-------------------------------------------------------------------------------------------------------+
|                                    THE PROMETHEUS PARADIGM SHIFT                                      |
+-------------------------------------------------------------------------------------------------------+
|  ERA 0: CONVENTIONAL WARFARE (Turns 1 - 40 / Until First Mobile Suit Deployment)                      |
|  - Combatants: Main Battle Tanks, Hypersonic Interceptors, Tilt-Wing Gunships, Technicals.            |
|  - Diplomacy: Factions are hostile, condescending, and enforce trade embargos.                        |
|  - Player Goal: Assemble and sinter the first Compact Tokamak Reactor and Bipedal Actuator Frame.    |
+-------------------------------------------------------------------------------------------------------+
                                                   |
                                                   v
+-------------------------------------------------------------------------------------------------------+
|  THE CATALYST EVENT: MAIDEN COMBAT SORTIE ("PROJECT PROMETHEUS")                                      |
|  - First Mobile Suit sorties into contested sector.                                                   |
|  - Dynamic camera zoom & battle chatter: enemy tank commanders panic at the 18-meter walking giant.   |
|  - The player's mobile suit dominates conventional armor through 3D elevation jumping & melee power.  |
+-------------------------------------------------------------------------------------------------------+
                                                   |
                                                   v
+-------------------------------------------------------------------------------------------------------+
|  ERA 1: THE MONOPOLY & REVERSE-ENGINEERING RACE (Turns 40 - 120 / Year 1 - 2)                         |
|  - Diplomacy Flip: Hostilities freeze; factions flood player with luxury bounties & procurement bids. |
|  - Resource Friction: Tritium fusion costs and rare sintered alloys limit the player to 1-2 mechs.   |
|  - Competitor R&D Bar: 4 Rival Megacorps advance from 0% -> 100% reverse-engineering over 365 days.   |
|  - Milestone Climax: First rival mobile suits (Terran Bulwark, Colony Sylph, etc.) deploy to battle.  |
+-------------------------------------------------------------------------------------------------------+
```

---

## 2. Conventional Forces Doctrine & Vehicle Catalog

Before the mobile suit revolution, each interstellar faction fields specialized conventional armor adhering to their core ideological doctrines:

### 2.1 The Terran Coalition (Imperial Heavy Armor & Mechanized Infantry Doctrine)
* **T-720 'Mammoth' Heavy Battle Tank**:
  * *Role:* Superheavy Frontline Linebreaker.
  * *Components:* Reinforced Sloped Hull (Torso: 520 HP, Armor: 38), Dual 120mm Rifled Turret (Head: 240 HP), Quad-Tread Assembly (Legs: 480 HP), Sponson Vulcan (Arm Left: 220 HP), Coaxial Autocannon (Arm Right: 220 HP), Diesel-Turbine Pack (Backpack: 180 HP).
  * *Weapons:* Dual 120mm Rifled Cannons (Damage: 140, Range: 2-6), Heavy Coaxial Vulcan (Damage: 70, Range: 1-4).
  * *Movement:* Ground-only, 4 AP. High move cost over ruins and rough terrain.
* **A-14 'Skyhammer' Close Air Support Strike Jet**:
  * *Role:* Heavy Atmospheric & Low-Orbit Ground Strafer.
  * *Components:* Armored Fuselage (Torso: 320 HP, Armor: 20), Avionics Radar Dome (Head: 140 HP), Port Wing Pylon (Arm Left: 180 HP), Starboard Wing Pylon (Arm Right: 180 HP), Twin Jet Turbines (Legs: 260 HP, Flight Capable), Countermeasure Pod (Backpack: 150 HP).
  * *Weapons:* GAU-30mm High-Velocity Rotary Gun (Damage: 110, Range: 1-5), Dumbfire Heavy Rocket Salvo (Damage: 160, Range: 2-6).
  * *Movement:* Flight (Ignores terrain cost, can cross chasms and water), 7 AP. Elevated aerial sprite offset.
* **Terran 88th Mechanized Infantry Squad**:
  * *Role:* Entrenched Anti-Armor Fireteam (4 Soldiers in Squad formation behind reinforced sandbags).
  * *Components:* Squad Integrity (Torso: 220 HP, Armor: 14), Squad Leader & Radio (Head: 90 HP), GAU-50mm Machine Gun (Arm Left: 110 HP), Shoulder ATGM Launcher (Arm Right: 120 HP), Combat Boots (Legs: 180 HP), Munition Packs (Backpack: 100 HP).
  * *Weapons:* Heavy ATGM (Damage: 155, Range: 2-6, Shaped-Charge Armor Penetration), Squad MG Volley (Damage: 70, Range: 1-4).
  * *Tactical Synergy:* Highly vulnerable to direct Mobile Suit trampling (2.0x anti-personnel damage), but deadly when firing ATGM volleys from fortified cover.

### 2.2 The Outer Colonies (High-Velocity Skimmer, Aero & Void Infantry Doctrine)
* **K-4 'Stiletto' Rapid Attack Hover-Skiff**:
  * *Role:* Ground-Effect Railgun Harrier.
  * *Components:* Ultralight Composite Chassis (Torso: 310 HP, Armor: 16), Targeting Sensor Mast (Head: 120 HP), Left Stabilization Fin (Arm Left: 150 HP), Right Stabilization Fin (Arm Right: 150 HP), Venturi Hover Skirts (Legs: 340 HP), Liquid Oxygen Booster (Backpack: 160 HP).
  * *Weapons:* Twin 60mm Linear Rail-Needles (Damage: 130, Range: 2-7, High Accuracy), Micro-Scatter Flak (Damage: 65, Range: 1-3).
  * *Movement:* Skimmer (Crosses water/swamp without penalty), 7 AP, Evasion: 65%.
* **S-10 'Dart' Hypersonic Interceptor**:
  * *Role:* Swept-Wing Atmospheric Interceptor.
  * *Components:* Delta Fuselage (Torso: 280 HP, Armor: 14), Fire-Control Cockpit (Head: 110 HP), Left Delta Wing (Arm Left: 160 HP), Right Delta Wing (Arm Right: 160 HP), Ramjet Afterburners (Legs: 240 HP), ECM Jammer (Backpack: 140 HP).
  * *Weapons:* Pulse Laser Array (Damage: 150, Range: 1-6), Air-to-Air Interceptor Missiles (Damage: 140, Range: 3-8).
  * *Movement:* High-Altitude Flight, 8 AP, Evasion: 72%.
* **V-88 'Valkyrie' Heavy Tilt-Rotor Gunship**:
  * *Role:* Twin Tilt-Rotor Close Air Support & Transport.
  * *Components:* Armored Fuselage (Torso: 380 HP, Armor: 22), Chin Sensor Turret (Head: 150 HP), Port Tilt-Rotor (Arm Left: 210 HP), Starboard Tilt-Rotor (Arm Right: 210 HP), Turbine Lift Engine (Legs: 280 HP), Flare Pods (Backpack: 160 HP).
  * *Weapons:* Chin 25mm Gatling (Damage: 95, Range: 1-5), Heavy Rocket Salvo (Damage: 170, Range: 2-7).
  * *Movement:* Hovering Flight, 7 AP.
* **Colonial Void Jump Skirmishers**:
  * *Role:* High-Mobility Zero-G Jetpack Infantry (4 Soldiers with Pressurized EVA suits).
  * *Components:* Pressurized Suits (Torso: 200 HP, Armor: 10), HUD Helmets (Head: 85 HP), Pulse Carbines (Arm Left: 100 HP), Linear Charges (Arm Right: 110 HP), Pneumatic Struts (Legs: 160 HP), Vernier Packs (Backpack: 110 HP).
  * *Weapons:* Pulse Carbines (Damage: 85, Range: 1-5), Magnetic Demo Charge (Damage: 170, Range: 1).
  * *Movement:* Jump Pack (Traverses elevation and rough terrain), 6 AP, Evasion: 62%.

### 2.3 The Rogue Mercenary Syndicates (Improvised Scrap Armor & Militia Doctrine)
* **SCR-T01 'Rustfang' Armored Technical**:
  * *Role:* Heavy Gun Truck & Guerrilla Flanker.
  * *Components:* Bolted Scrap Chassis (Torso: 290 HP, Armor: 18), Gunner Steel Shield (Head: 110 HP), Left Sponson Mount (Arm Left: 130 HP), Right Sponson Mount (Arm Right: 130 HP), Off-Road Wheels (Legs: 280 HP), Nitrous Supercharger (Backpack: 130 HP).
  * *Weapons:* Scrappers Flak Cannon (Damage: 95, Range: 1-4), Jury-Rigged Rocket Launcher (Damage: 135, Range: 2-5).
  * *Movement:* Wheeled (Fast on roads/plains, slow on hills), 6 AP.
* **SCR-B03 'Buzzard' Scrap Light Bomber**:
  * *Role:* Twin-Boom Atmospheric Demolition Bomber.
  * *Components:* Welded Scrap Fuselage (Torso: 300 HP, Armor: 16), Radial Cockpit (Head: 120 HP), Port Bomb Pylon (Arm Left: 160 HP), Starboard Bomb Pylon (Arm Right: 160 HP), Piston Engine (Legs: 240 HP), Fuel Drums (Backpack: 130 HP).
  * *Weapons:* Incendiary Slag Bombs (Damage: 150, Range: 2-6, Ballistic Splash).
  * *Movement:* Low-Altitude Flight, 6 AP.
* **Syndicate Guerrilla Scrap Militia Squad**:
  * *Role:* Irregular Guerilla Ambushers (4 Fighters with scrap armor, gas masks, and RPGs behind junk barriers).
  * *Components:* Scrap Cuirasses (Torso: 210 HP, Armor: 14), Welded Masks (Head: 90 HP), Autocannons (Arm Left: 105 HP), RPG Tube (Arm Right: 115 HP), Combat Boots (Legs: 170 HP), Grenade Harness (Backpack: 95 HP).
  * *Weapons:* Scrap RPG Volley (Damage: 140, Range: 1-5), Nail-Bomb Shrapnel (Damage: 80, Range: 1-3).
  * *Movement:* Foot Infantry, 5 AP.

### 2.4 The Apex Zaibatsu (Automated Drone Tanks, Jets & Android Infantry)
* **Type-94 'Kurogane' Drone Tank**:
  * *Role:* Automated Stealth Combat Drone.
  * *Components:* Monocoque Carbon Hull (Torso: 360 HP, Armor: 26), Optical AI Sensor Dome (Head: 140 HP), Left Missile Bay (Arm Left: 190 HP), Right Railgun Mount (Arm Right: 200 HP), Low-Noise Rubber Tracks (Legs: 380 HP), Optical Camouflage Generator (Backpack: 170 HP).
  * *Weapons:* 75mm Hypersonic Railgun (Damage: 175, Range: 2-8), Micro-Missile Pod (Damage: 120, Range: 2-5).
  * *Movement:* Stealth Tread, 5 AP, High Camouflage/Evasion (58%).
* **Type-02 'Kamaitachi' Stealth Drone Jet**:
  * *Role:* Diamond Flying Wing Unmanned Interceptor.
  * *Components:* Diamond Carbon Wing (Torso: 270 HP, Armor: 14), AI Flight Core (Head: 110 HP), Internal Bay L (Arm Left: 150 HP), Internal Bay R (Arm Right: 150 HP), Ion Vector Thruster (Legs: 230 HP), Optical Cloak (Backpack: 140 HP).
  * *Weapons:* Stealth Micro-Torpedoes (Damage: 145, Range: 2-7).
  * *Movement:* Stealth Flight, 8 AP, Evasion: 75%.
* **Zaibatsu Cybernetic Android Squad (Model Z-01)**:
  * *Role:* Synchronized Hivemind Android Fireteam (4 Carbon Humanoids with Optic Visors).
  * *Components:* Carbon Monocoque Frame (Torso: 240 HP, Armor: 18), Optic Neural Sensor (Head: 100 HP), Rail-Needle L (Arm Left: 120 HP), Rail-Needle R (Arm Right: 120 HP), Hydraulic Bipods (Legs: 190 HP), Capacitor Pack (Backpack: 120 HP).
  * *Weapons:* Hypersonic Rail-Needles (Damage: 110, Range: 2-7), Monofilament Wire Snare (Damage: 135, Range: 1).
  * *Movement:* Automated Biped, 5 AP, High Accuracy (88%).

## 3. The Catalyst Mechanics: The Birth of the Mobile Suit

### 3.1 Why the Mobile Suit Shatters Conventional Military Doctrine
When the player deploys their first Mobile Suit, the tactical superiority is overwhelming:
1. **Verticality & Terrain Flanking:** Tanks must navigate roads and ravines; fighter jets cannot hover or capture ground. The Mobile Suit traverses elevation 0, 1, and 2 cliffs, jumps river chasms, and takes directional cover behind structures.
2. **Kinetic Crushing Melee:** Tanks and jets possess zero close-quarters defense. In melee range, the Mobile Suit's hydraulic kick or crushing arm strike deals a 1.5x damage bonus against conventional armor hulls.
3. **Compound Weapon Loadouts:** While a tank carries only a turret and coaxial gun, a Mobile Suit wields handheld ballistic/energy rifles, shoulder-mounted micro-missiles, rotary vulcan point-defense, and high-frequency melee blades simultaneously.

### 3.2 Natural Friction & Anti-Steamroll Balances
To ensure the player cannot conquer the interstellar war map on Day 1:
* **The Fusion Fuel Scarcity:** Operating a compact Tokamak reactor consumes refined Tritium and Synthetic Flux. Deployment maintenance costs are 3x higher than conventional armor.
* **Irreplaceable Prototype Status:** Building a second mobile suit requires weeks of deep metallurgical sintering in the Crucible. For the first 60 days, the player possesses **only one mobile suit**.
* **Mass Frontlines:** Factions command hundreds of conventional divisions. The player can turn the tide of a single regional battle, but cannot defend five solar sectors at once.

---

## 4. The Global Diplomatic Pivot & Arms Monopoly Phase

The moment `global.first_mobile_suit_deployed` evaluates to `true`:
1. **Hostility Freeze:** Any faction with negative standing has combat aggression paused toward the player's mobile dreadnought for 60 calendar turns.
2. **Emergency Procurement Bids:** Factions offer **"Prometheus Subsidies"**:
   * Contract bounty rewards increase by **+200% to +300%** if the player brings their Mobile Suit to the battle.
   * Superpowers submit formal **"Tech Purchase Inquiries"** offering 250,000+ Credits for schematic licensing or chassis delivery.
3. **The Player's Moral & Strategic Dilemma:**
   * *Option A: Sell Units to Allies:* Yields massive immediate credits and faction favor, but **triples** that faction's reverse-engineering speed!
   * *Option B: Total Tech Monopoly:* Withhold all technology. Retain tactical battlefield dominance, but face escalating corporate espionage and black-ops retrieval raids.

---

## 5. The 365-Day Reverse-Engineering Engine

The reverse-engineering progression is tracked across four rival megacorporations in `obj_GameManager.reverse_engineering_progress`:

$$R&D Progress_i(t) = \text{Base Tick}(t) + \text{Combat Exposure Bonus} + \text{Salvage Penalty} + \text{Tech Trade Acceleration}$$

* **Base Tick:** +0.25% per calendar day (~90% after 360 days).
* **Combat Exposure:** +0.10% each time the player fights in that corporation's territory (their sensor satellites record telemetry).
* **Lost Component Salvage:** If the player's Mobile Suit loses an arm or leg in combat, that faction gains an immediate **+10.0% R&D leap**.
* **Direct Sales:** Delivering a prototype unit to a faction instantly awards their defense arm **+35.0% R&D**.

### Milestone Rollouts:
* **25% Progress:** Competitor releases news broadcast; starts constructing walking bipedal test rigs.
* **50% Progress:** Competitor tests "Semi-Mobile Suit" conversions (tanks with walking legs).
* **75% Progress:** Competitor announces completed blueprint and begins factory retooling.
* **100% Progress (Day 365):** Competitor deploys their canonical Era 1 Mobile Suit (*Bulwark*, *Sylph*, *Marauder*, or *Ronin*). The playing field levels, ushering in full-scale interstellar Mecha warfare!

---

## 6. GameMaker Architecture & File Modifications

1. `datafiles/conventional_vehicles.json`: Master database of all conventional tanks, jets, and gunships.
2. `sprites/spr_veh_*`: Isometric 16-bit SNES-style sprites with dedicated front and back perspectives.
3. `objects/obj_GameManager`: Added `timeline_era = 0`, `first_mobile_suit_created = false`, `reverse_engineering_progress`, and `trigger_mobile_suit_revolution()`.
4. `objects/obj_FactionManager`: Implemented Era 0 conventional doctrine states, diplomatic freeze, and reverse-engineering bid logic.
5. `objects/obj_BattleManager`: Configured Era 0 combat deployment to populate tanks/jets for hostile and allied platoons, with dynamic audio-visual reaction upon the player's Mobile Suit drop.
