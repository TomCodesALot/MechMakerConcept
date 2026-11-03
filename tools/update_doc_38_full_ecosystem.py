import re

d38_path = "docs/38_the_prometheus_catalyst_conventional_warfare_and_mobile_suit_genesis.md"
with open(d38_path, "r") as f:
    text = f.read()

# Update Section 2 to include Infantry & Aircraft
sec2_marker = "### 2.1 The Terran Coalition (Imperial Heavy Armor Doctrine)"
sec2_expanded = """### 2.1 The Terran Coalition (Imperial Heavy Armor & Mechanized Infantry Doctrine)
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
  * *Movement:* Automated Biped, 5 AP, High Accuracy (88%)."""

# Replace Section 2 up to Section 3
pattern = r'### 2\.1 The Terran Coalition \(Imperial Heavy Armor Doctrine\).*?(?=## 3\. The Catalyst Mechanics)'
text = re.sub(pattern, sec2_expanded + "\n\n", text, flags=re.DOTALL)

with open(d38_path, "w") as f:
    f.write(text)

print("Updated docs/38 with comprehensive combined-arms roster.")
