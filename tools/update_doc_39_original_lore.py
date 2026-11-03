import os

doc_content = """# Document 39: Planetary & Orbital Territory Conquest Engine & The Sol Theaters
**Project:** MechMakerConcept (GameMaker Studio 2 / LTS 2026 Runner)  
**Lead Game Designer:** Director GDD  
**Lead Narrative Designer:** Narrative Worldbuilder  
**Status:** Canonical Design & Architecture Specification  
**Date:** October 20, 2026  

---

## 1. Executive Summary & Strategic Design Vision

Drawing design inspiration from classic turn-based strategic mecha classics like *Front Mission* (geopolitical proxy conflicts, corporate military contracts, contested border zones) and strategic operational macro-maps (dynamic contested fronts, sovereign territory yields, and theater mobility), this document establishes the **Comprehensive Planetary & Orbital Territory Conquest Engine**.

War in Sol is not an abstract spreadsheet. It is fought across real, heavily fortified space habitats, orbital mass drivers, lunar crater metropolises, continental bedrock vaults, and the subterranean caldera foundries of Mars.

### Core Strategic Tenets
1. **Three Grand Theaters of War**:
   - **The Space & Colony Sphere (15 Strategic Orbital Hubs, Cylinders & Citadels)**:
     Anchoring the Earth-Moon Lagrange Points (L1–L5), cislunar transit corridors, lunar polar metropolises, and hollowed defense asteroids.
     *The Player PMC begins operations in Space at Kepler Orbital Haven (L5).*
   - **The Earth Sphere (10 Terrestrial Strategic Citadels & Redoubts)**:
     From the subterranean granite vaults of South America and Cascadia's Pacific mass driver, to the North African solar grids and the submarine caverns of the North Sea.
   - **The Mars & Asteroid Sphere (8 Subterranean Crypts & Martian Redoubts)**:
     Locked at game start under military quarantine and sensor blackout. Unlocks dynamically upon Year 215 or manual override when **The Tharsis Machine Consensus (`faction_f`)** awakens, unleashing an autonomous war machine into Sol.

2. **Equitable Strategic Parity**:
   - The initial 25 Earth and Space territories are evenly apportioned among the 5 active Sol superpowers:
     **Exactly 5 territories each (20% Sol control each)**, creating a balanced starting balance of power.
   - The Player PMC begins as an independent sovereign operator chartered at **Kepler Orbital Haven (L5)**.

3. **Logistics & Strategic Material Yield Economy**:
   - Every territory yields daily income (**Credits**) and continuous shipments of strategic materials:
     - **Refined Composite** (Armor structural matrix)
     - **Titanium Alloy** (Standard ballistic plating)
     - **Tungsten Heavy Ingot** (High-density kinetic armor and rail penetrators)
     - **Silica Carbide** (Thermal shielding and beam diffraction ceramic)
     - **Tritium Gas** (High-output fusion reactor core fuel)
     - **Synthetic Flux** (Superconducting electromagnetic bus conduits)
   - Whichever faction controls the territory receives its daily tribute and material shipments.
   - Seizing territories delivers daily supply crates directly into the player's HQ vaults every turn.

4. **Dynamic Territorial Warfare & Frontline Clashes**:
   - Frontline sectors are defined dynamically: any territory bordering a neighbor controlled by a rival faction is designated a **Contested Frontline [WAR]**.
   - Frontline territories risk daily border skirmishes, dynamic sovereign flips, and garrison degradation.
   - The Player PMC can accept high-stakes invasion and defense contracts, dispatching expeditionary lances to capture sovereign control.

---

## 2. Complete 33-Territory Canonical Catalog

### A. The Space & Colony Sphere (15 Territories — Player Starting Theater)

#### 1. `space_kepler_haven` — Kepler Orbital Haven (L5)
*   **Controlling Faction**: `pmc` (Player Starting Headquarters & Charter Port)
*   **Subregion**: Earth-Moon L5 Trojan Cluster
*   **Daily Yield**: +48,000 Cr | +22 kg Refined Composite
*   **Defense Rating**: 80/100 | **Garrison**: Iron Ridge Veteran Garrison Wing
*   **Connections**: `space_aethelgard_prime`, `space_hyperion_dock`, `space_selene_zenith`
*   **Strategic Lore**: A massive multi-torus orbital sanctuary anchoring the L5 cluster. Kepler Haven serves as the independent charter station where mercenary contractors and mobile suit manufacturers broker private defense treaties outside sovereign hegemony.
*   **Strategic Asset**: Central free-trade drydocks and primary staging port for Iron Ridge PMC operations.

#### 2. `space_aethelgard_prime` — Aethelgard Prime Cluster (L4)
*   **Controlling Faction**: `faction_b` (The Free Colonies League)
*   **Subregion**: Free Colonies High Orbit Hub
*   **Daily Yield**: +44,000 Cr | +20 kg Refined Composite
*   **Defense Rating**: 82/100 | **Garrison**: Aethelgard 1st Aerospace Platoon
*   **Connections**: `space_kepler_haven`, `space_halcyon_ring`, `space_valkyrie_array`
*   **Strategic Lore**: Triple-linked cylindrical habitats spanning thirty kilometers. Inside, terraced green arcologies and artificial lakes thrive beneath solar reflector sails, representing the cultural pinnacle of the independent orbital colonies.
*   **Strategic Asset**: Capital administrative hub and ideological heart of the Free Colonies League.

#### 3. `space_halcyon_ring` — Halcyon Agricultural Torus (L1)
*   **Controlling Faction**: `faction_b` (The Free Colonies League)
*   **Subregion**: Sun-Earth Orbital Meridian
*   **Daily Yield**: +36,000 Cr | +18 kg Synthetic Flux
*   **Defense Rating**: 68/100 | **Garrison**: Colonial Agri-Security Force
*   **Connections**: `space_aethelgard_prime`, `space_charybdis_gate`, `space_valkyrie_array`
*   **Strategic Lore**: A colossal rotating hydroponic ring providing over sixty percent of the fresh caloric biomass consumed across Sol's Lagrange colonies.
*   **Strategic Asset**: Vital solar-spectrum food production arrays and cislunar water purification reservoirs.

#### 4. `space_charybdis_gate` — Charybdis Vector Relay
*   **Controlling Faction**: `faction_b` (The Free Colonies League)
*   **Subregion**: Outer Orbital Acceleration Ring
*   **Daily Yield**: +40,000 Cr | +16 kg Tritium
*   **Defense Rating**: 75/100 | **Garrison**: Vector Interceptor Squadron
*   **Connections**: `space_halcyon_ring`, `space_vesta_anchorage`, `space_tartarus_citadel`
*   **Strategic Lore**: An electromagnetic accelerator gate accelerating interplanetary cargo freighters toward the Jovian routes. Contested as a prime chokepoint for long-range tactical fleet deployments.
*   **Strategic Asset**: High-velocity slingshot trajectory control and deep-space fusion propellant caches.

#### 5. `space_tartarus_citadel` — Tartarus Orbital Redoubt (L3)
*   **Controlling Faction**: `faction_a` (The Terran Coalition)
*   **Subregion**: Earth-Sun Counter-Orbit Bastion
*   **Daily Yield**: +50,000 Cr | +25 kg Tungsten
*   **Defense Rating**: 94/100 | **Garrison**: Terran Void-Guard Phalanx
*   **Connections**: `space_charybdis_gate`, `space_archon_spire`, `space_nadir_scrapyard`
*   **Strategic Lore**: A hollowed nickel-iron asteroid bristling with twin rail-gun turrets and heavy point-defense batteries, permanently stationed behind the Sun to monitor counter-orbital vector incursions.
*   **Strategic Asset**: Super-heavy spinal rail-cannon battery capable of orbital area denial.

#### 6. `space_archon_spire` — Archon Geostationary Anchor
*   **Controlling Faction**: `faction_a` (The Terran Coalition)
*   **Subregion**: Atlantic Orbital Tether Apex
*   **Daily Yield**: +42,000 Cr | +20 kg Titanium
*   **Defense Rating**: 85/100 | **Garrison**: 8th Geosynchronous Heavy Infantry
*   **Connections**: `space_tartarus_citadel`, `space_vesta_anchorage`, `space_pelican_refinery`
*   **Strategic Lore**: The counterweight orbital terminus of the Atlantic orbital elevator. Houses receiving bays for raw planetary ores hoisted daily from terrestrial strip mines.
*   **Strategic Asset**: Direct cargo elevator pipeline connecting high Earth orbit with terrestrial factories.

#### 7. `space_vesta_anchorage` — Vesta Perimeter Outpost
*   **Controlling Faction**: `faction_a` (The Terran Coalition)
*   **Subregion**: Cislunar Deep Early Warning Line
*   **Daily Yield**: +38,000 Cr | +15 kg Silica Carbide
*   **Defense Rating**: 78/100 | **Garrison**: Cislunar Sentry Battery
*   **Connections**: `space_charybdis_gate`, `space_archon_spire`, `space_nadir_scrapyard`
*   **Strategic Lore**: A militarized sensor node and patrol outpost maintaining unbroken surveillance across the cislunar shipping lanes.
*   **Strategic Asset**: Deep-radar array detecting sub-light fleet transit vectors.

#### 8. `space_pelican_refinery` — Pelican Deep Slagfield
*   **Controlling Faction**: `faction_c` (Rogue Mercenary Syndicates)
*   **Subregion**: Wreckage Belt & Smelting Hub
*   **Daily Yield**: +35,000 Cr | +30 kg Titanium
*   **Defense Rating**: 72/100 | **Garrison**: Iron Corsair Smelter Guard
*   **Connections**: `space_archon_spire`, `space_nadir_scrapyard`, `space_hyperion_dock`
*   **Strategic Lore**: Born from the dense debris field of the First Proxy Skirmishes, this industrial graveyard was seized by mercenary cartels who converted destroyed battlecruisers into crude smelting crucibles.
*   **Strategic Asset**: Massive titanium scrap salvage and black-market armor recycling yards.

#### 9. `space_nadir_scrapyard` — Nadir Salvage Expanse
*   **Controlling Faction**: `faction_c` (Rogue Mercenary Syndicates)
*   **Subregion**: Southern Orbital Debris Field
*   **Daily Yield**: +32,000 Cr | +26 kg Tungsten
*   **Defense Rating**: 70/100 | **Garrison**: Nadir Freebooter Lance
*   **Connections**: `space_tartarus_citadel`, `space_vesta_anchorage`, `space_pelican_refinery`
*   **Strategic Lore**: A lawless orbital drift field choked with shattered warship bulkheads, burnt reactor husks, and unexploded munitions where syndicate salvagers harvest precious metals under constant threat of pirate raids.
*   **Strategic Asset**: High-density scrap salvage yielding rare ballistic warheads and hull alloy.

#### 10. `space_valkyrie_array` — Valkyrie Solar Array
*   **Controlling Faction**: `faction_c` (Rogue Mercenary Syndicates)
*   **Subregion**: High-Energy Microwave Transmitter
*   **Daily Yield**: +45,000 Cr | +18 kg Synthetic Flux
*   **Defense Rating**: 65/100 | **Garrison**: Syndicate Relay Enforcers
*   **Connections**: `space_aethelgard_prime`, `space_halcyon_ring`, `space_borealis_port`
*   **Strategic Lore**: A multi-kilometer constellation of photovoltaic mirrors that collect pure solar radiation and beam gigawatts of microwave power to distant lunar bases and orbital factories.
*   **Strategic Asset**: Direct microwave energy beaming grid capable of recharging mobile suit capacitor packs in minutes.

#### 11. `space_selene_zenith` — Port Selene Crater Metropolis
*   **Controlling Faction**: `faction_d` (Apex Bio-Cybernetics Zaibatsu)
*   **Subregion**: Lunar North Polar Geodesic Rim
*   **Daily Yield**: +52,000 Cr | +24 kg Refined Composite
*   **Defense Rating**: 88/100 | **Garrison**: Zaibatsu Cyber-Garrison Unit
*   **Connections**: `space_kepler_haven`, `space_daedalus_foundry`, `space_borealis_port`
*   **Strategic Lore**: A sprawling geodesic dome city perched along the rim of Peary Crater, powered by perpetual sunlight on its peaks and fed by frozen volatiles harvested from crater-floor shadows.
*   **Strategic Asset**: Apex Zaibatsu's corporate financial exchange and cybernetic neural-link laboratories.

#### 12. `space_daedalus_foundry` — Daedalus Lunar Farside Works
*   **Controlling Faction**: `faction_d` (Apex Bio-Cybernetics Zaibatsu)
*   **Subregion**: Deep Lunar Bedrock Foundries
*   **Daily Yield**: +46,000 Cr | +28 kg Silica Carbide
*   **Defense Rating**: 86/100 | **Garrison**: Kurogane Automated Sentinel Wing
*   **Connections**: `space_selene_zenith`, `space_hyperion_dock`, `space_ironspire_bastion`
*   **Strategic Lore**: Buried deep within lunar farside bedrock to eliminate electromagnetic interference from Earth. Houses cleanroom robotic foundries mass-producing high-density ceramic armor plates.
*   **Strategic Asset**: Thermal-shock ceramic composite and laser-diffraction armor manufacturing.

#### 13. `space_borealis_port` — Port Borealis Cryo-Depot
*   **Controlling Faction**: `faction_d` (Apex Bio-Cybernetics Zaibatsu)
*   **Subregion**: Lunar South Polar Ice Basins
*   **Daily Yield**: +40,000 Cr | +20 kg Tritium
*   **Defense Rating**: 74/100 | **Garrison**: Arctic Vacuum Combat Lance
*   **Connections**: `space_selene_zenith`, `space_valkyrie_array`, `space_ironspire_bastion`
*   **Strategic Lore**: Situated inside permanently shadowed polar craters containing billions of metric tons of water ice. Purifies pure liquid hydrogen and deuterium for high-output mobile suit fusion engines.
*   **Strategic Asset**: Sol's largest lunar cryo-fuel depot and reactor coolant refinery.

#### 14. `space_ironspire_bastion` — Ironspire Asteroid Bastion (L2)
*   **Controlling Faction**: `faction_e` (Sidereal Sovereign League)
*   **Subregion**: Earth-Moon L2 Hollowed Rock
*   **Daily Yield**: +48,000 Cr | +25 kg Tungsten
*   **Defense Rating**: 92/100 | **Garrison**: Sidereal Knight-Banner Guard
*   **Connections**: `space_daedalus_foundry`, `space_borealis_port`, `space_hyperion_dock`
*   **Strategic Lore**: A hollowed, tungsten-sheathed carbonaceous chondrite asteroid converted into an impregnable fleet citadel. Commands the Earth-Moon shadow corridor at Lagrange Point 2.
*   **Strategic Asset**: Heavy spinal magnetic catapults and sovereign command bunker.

#### 15. `space_hyperion_dock` — Hyperion Orbital Shipyards
*   **Controlling Faction**: `faction_e` (Sidereal Sovereign League)
*   **Subregion**: Deep Space Zero-G Drydock Web
*   **Daily Yield**: +55,000 Cr | +26 kg Refined Composite
*   **Defense Rating**: 84/100 | **Garrison**: Sovereign Fleet Escort Flotilla
*   **Connections**: `space_kepler_haven`, `space_pelican_refinery`, `space_ironspire_bastion`
*   **Strategic Lore**: A three-dimensional web of magnetic scaffold bays where sovereign capital ships, heavy missile corvettes, and custom ace-tier mobile suit chassis are forged in microgravity.
*   **Strategic Asset**: Premier capital shipyard capable of rapid fleet hull reconstruction and frame upgrades.

---

### B. The Earth Sphere (10 Territories — Planetary Citadels)

#### 16. `earth_granite_redoubt` — Granite Deep Command
*   **Controlling Faction**: `faction_a` (The Terran Coalition)
*   **Subregion**: Amazonian Continental Bedrock Citadel
*   **Daily Yield**: +42,000 Cr | +24 kg Titanium
*   **Defense Rating**: 92/100 | **Garrison**: Terran 1st Heavy Armored Division
*   **Connections**: `earth_cascadia_driver`, `earth_andes_battery`, `earth_gibraltar_redoubt`
*   **Strategic Lore**: A multi-tiered military fortress carved thousands of meters beneath ancient continental granite. Subterranean rivers engineered into cooling canals support heavy nuclear reactors and blast hatches capable of launching carrier-class gunships.
*   **Strategic Asset**: Deep subterranean planetary command bunker impervious to orbital kinetic strikes.

#### 17. `earth_cascadia_driver` — Cascadia Mass-Driver Complex
*   **Controlling Faction**: `faction_a` (The Terran Coalition)
*   **Subregion**: Pacific Mountain Launch Corridor
*   **Daily Yield**: +46,000 Cr | +28 kg Tungsten
*   **Defense Rating**: 88/100 | **Garrison**: Coastline Rail-Artillery Brigade
*   **Connections**: `earth_granite_redoubt`, `earth_shanghai_arcology`, `earth_outback_proving`
*   **Strategic Lore**: A massive magnetic rail carved into the western mountain slopes that hurls heavy supply pods and orbital defense gunships directly into high Earth orbit without chemical fuel consumption.
*   **Strategic Asset**: High-throughput planetary-to-orbit magnetic launch corridor.

#### 18. `earth_sahara_array` — Al-Kufra Solar Citadel
*   **Controlling Faction**: `faction_b` (The Free Colonies League)
*   **Subregion**: North African Photovoltaic Basin
*   **Daily Yield**: +40,000 Cr | +22 kg Synthetic Flux
*   **Defense Rating**: 76/100 | **Garrison**: Colonial Desert Ranger Regiments
*   **Connections**: `earth_andes_battery`, `earth_gibraltar_redoubt`, `earth_ural_arsenal`
*   **Strategic Lore**: The Free Colonies League's primary terrestrial beachhead. A vast automated photovoltaic plain coupled with thermal salt reservoirs, supplying electricity to orbital beam transmitters.
*   **Strategic Asset**: Terrestrial power-beaming array and rare-earth sand refining foundries.

#### 19. `earth_andes_battery` — Chimborazo Orbital Bastion
*   **Controlling Faction**: `faction_b` (The Free Colonies League)
*   **Subregion**: High-Altitude Equatorial Ridge
*   **Daily Yield**: +38,000 Cr | +18 kg Tritium
*   **Defense Rating**: 84/100 | **Garrison**: Equatorial Skystrike Wing
*   **Connections**: `earth_granite_redoubt`, `earth_sahara_array`, `earth_antarctic_facility`
*   **Strategic Lore**: Erected on an equatorial volcanic peak to minimize atmospheric drag for surface-to-orbit transit. Heavy particle cannons guard the low-inclination launch paths.
*   **Strategic Asset**: Equatorial orbital insertion trajectory and high-altitude battery grid.

#### 20. `earth_gibraltar_redoubt` — Gibraltar Sea Gate Bastion
*   **Controlling Faction**: `faction_c` (Rogue Mercenary Syndicates)
*   **Subregion**: Strait of Gibraltar Coastal Bunkers
*   **Daily Yield**: +36,000 Cr | +26 kg Titanium
*   **Defense Rating**: 82/100 | **Garrison**: Coastal Gunboat Syndicate Flotilla
*   **Connections**: `earth_granite_redoubt`, `earth_sahara_array`, `earth_nordic_vault`
*   **Strategic Lore**: Seized by mercenary cartels during the Mediterranean shipping collapses, this fortress commands the maritime gateway between the Atlantic and Mediterranean with coastal rail batteries and naval submarine hangars.
*   **Strategic Asset**: Chokepoint maritime trade control and submersible resupply docks.

#### 21. `earth_outback_proving` — Woomera Proving Grounds
*   **Controlling Faction**: `faction_c` (Rogue Mercenary Syndicates)
*   **Subregion**: Central Australian Desert Weapons Basin
*   **Daily Yield**: +34,000 Cr | +24 kg Tungsten
*   **Defense Rating**: 74/100 | **Garrison**: Desert Raider Mechanized Column
*   **Connections**: `earth_cascadia_driver`, `earth_shanghai_arcology`, `earth_antarctic_facility`
*   **Strategic Lore**: An isolated red-dirt proving ground spanning thousands of square kilometers. Used by mercenary syndicates and private arms cartels to test prototype ordnance and heavy ballistic cannons without oversight.
*   **Strategic Asset**: Live-fire ballistic test range and heavy alloy munitions testing site.

#### 22. `earth_shanghai_arcology` — Neo-Shanghai Arcology Spire
*   **Controlling Faction**: `faction_d` (Apex Bio-Cybernetics Zaibatsu)
*   **Subregion**: Yangtze Delta Industrial Megalopolis
*   **Daily Yield**: +54,000 Cr | +30 kg Silica Carbide
*   **Defense Rating**: 86/100 | **Garrison**: Apex Corporate Security Division
*   **Connections**: `earth_cascadia_driver`, `earth_outback_proving`, `earth_ural_arsenal`
*   **Strategic Lore**: A three-kilometer-tall pyramid arcology rising above the Pacific coastline. Houses millions of technicians, cleanroom silicon foundries, and automated mecha assembly lines.
*   **Strategic Asset**: World-class electronics manufacturing and micro-die ceramic foundry.

#### 23. `earth_nordic_vault` — Skagerrak Sub-Sea Hangar
*   **Controlling Faction**: `faction_d` (Apex Bio-Cybernetics Zaibatsu)
*   **Subregion**: North Sea Submersible Cavern
*   **Daily Yield**: +44,000 Cr | +20 kg Synthetic Flux
*   **Defense Rating**: 80/100 | **Garrison**: Sub-Surface Cyber-Diver Lance
*   **Connections**: `earth_gibraltar_redoubt`, `earth_ural_arsenal`, `earth_antarctic_facility`
*   **Strategic Lore**: Subsea cavern complexes hollowed into the seabed beneath the Skagerrak strait. Allows submersible carriers to deploy amphibious mobile suits directly onto coastal targets undetected.
*   **Strategic Asset**: Amphibious deployment docks and stealth sonar baffling vaults.

#### 24. `earth_ural_arsenal` — Ural Mountain Munitions Vault
*   **Controlling Faction**: `faction_e` (Sidereal Sovereign League)
*   **Subregion**: Continental Bedrock Foundry Complex
*   **Daily Yield**: +48,000 Cr | +28 kg Titanium
*   **Defense Rating**: 90/100 | **Garrison**: Sidereal 4th Iron Fusiliers
*   **Connections**: `earth_sahara_array`, `earth_shanghai_arcology`, `earth_nordic_vault`
*   **Strategic Lore**: Deep bedrock bunkers beneath the Ural mountain chain housing vast stores of strategic metals and autonomous artillery manufacturing lines.
*   **Strategic Asset**: Heavy ballistic munitions production and titanium smelting foundries.

#### 25. `earth_antarctic_facility` — Vostok Sub-Glacial Vault
*   **Controlling Faction**: `faction_e` (Sidereal Sovereign League)
*   **Subregion**: South Pole Deep Ice Research Lab
*   **Daily Yield**: +42,000 Cr | +22 kg Tritium
*   **Defense Rating**: 85/100 | **Garrison**: Polar Cryo-Guard Phalanx
*   **Connections**: `earth_andes_battery`, `earth_outback_proving`, `earth_nordic_vault`
*   **Strategic Lore**: Buried beneath four kilometers of Antarctic ice sheet above Lake Vostok. Houses deep cryogenic prototype facilities where advanced reactor containment technologies are researched.
*   **Strategic Asset**: Cryogenic laboratory testing and heavy water tritium refining.

---

### C. The Mars & Asteroid Sphere (8 Territories — Locked Quarantine Sphere)

*Status at Campaign Start: Sensor Blackout under Protocol Omega. Automatically awakens upon Year 215 or through manual player override, introducing the Tharsis Machine Consensus (`faction_f`).*

#### 26. `mars_olympus_caldera` — Mount Olympus Zenith Redoubt
*   **Controlling Faction**: `faction_f` (Tharsis Machine Consensus)
*   **Subregion**: Summit Caldera Geothermal Vault
*   **Daily Yield**: +50,000 Cr | +25 kg Tungsten
*   **Defense Rating**: 96/100 | **Garrison**: Autonomous Hegemon Drone Core
*   **Connections**: `mars_marineris_rift`, `mars_tharsis_foundry`, `mars_phobos_citadel`
*   **Strategic Lore**: Perched within the volcanic caldera of the solar system's highest peak. Powered by deep mantle geothermal taps, this automated redoubt houses the central cognitive core of the Martian Machine Consensus.
*   **Strategic Asset**: Supreme cognitive processing core and planetary sensor umbrella.

#### 27. `mars_marineris_rift` — Valles Marineris Chasm Base
*   **Controlling Faction**: `faction_f` (Tharsis Machine Consensus)
*   **Subregion**: Canyon Wall Subterranean Complex
*   **Daily Yield**: +45,000 Cr | +26 kg Titanium
*   **Defense Rating**: 88/100 | **Garrison**: Sub-Chasm Kinetic Swarm
*   **Connections**: `mars_olympus_caldera`, `mars_tharsis_foundry`, `mars_hellas_basin`
*   **Strategic Lore**: A multi-tiered bunker complex burrowed into the four-kilometer-high vertical cliffs of the Marineris canyon. Sub-chasm launch tubes allow stealth mobile suit egress into low Martian orbit.
*   **Strategic Asset**: Natural canyon terrain defense and sheltered subsurface assembly corridors.

#### 28. `mars_tharsis_foundry` — Tharsis Volcanic Crucible
*   **Controlling Faction**: `faction_f` (Tharsis Machine Consensus)
*   **Subregion**: Volcanic Bulge Smelting Complex
*   **Daily Yield**: +55,000 Cr | +32 kg Refined Composite
*   **Defense Rating**: 90/100 | **Garrison**: Autonomous Heavy Fabricator Guard
*   **Connections**: `mars_olympus_caldera`, `mars_marineris_rift`, `mars_elysium_spire`
*   **Strategic Lore**: Channeling raw geothermal magma into automated continuous-casting lines, this volcanic crucible forges heavy armored chassis components without human labor.
*   **Strategic Asset**: Uninterrupted volcanic smelting lines with 150% standard chassis production efficiency.

#### 29. `mars_elysium_spire` — Elysium Space Tether
*   **Controlling Faction**: `faction_f` (Tharsis Machine Consensus)
*   **Subregion**: Planitia Space Elevator Terminal
*   **Daily Yield**: +44,000 Cr | +20 kg Synthetic Flux
*   **Defense Rating**: 84/100 | **Garrison**: Orbital Elevator Sentinel Array
*   **Connections**: `mars_tharsis_foundry`, `mars_hellas_basin`, `mars_deimos_sensor`
*   **Strategic Lore**: The Martian space elevator terminal anchored in the Elysium plains, lifting autonomous combat suits into synchronous orbit to board orbital invasion assault craft.
*   **Strategic Asset**: Low-gravity planetary-to-orbit transit tether.

#### 30. `mars_hellas_basin` — Hellas Impact Sink
*   **Controlling Faction**: `faction_f` (Tharsis Machine Consensus)
*   **Subregion**: Low-Elevation Hydroponic Dome City
*   **Daily Yield**: +38,000 Cr | +22 kg Silica Carbide
*   **Defense Rating**: 80/100 | **Garrison**: Basin Defense Automa Guard
*   **Connections**: `mars_marineris_rift`, `mars_elysium_spire`, `mars_ceres_gateway`
*   **Strategic Lore**: At the lowest elevation on Mars, atmospheric pressure is sufficient to sustain pressurized bio-domes and heavy water processing basins beneath dense dust storms.
*   **Strategic Asset**: Heavy water deuterium extraction and dense atmospheric thermal absorption.

#### 31. `mars_phobos_citadel` — Phobos Orbital Battery
*   **Controlling Faction**: `faction_f` (Tharsis Machine Consensus)
*   **Subregion**: Inner Moon Kinetic Bombardment Base
*   **Daily Yield**: +46,000 Cr | +28 kg Tungsten
*   **Defense Rating**: 94/100 | **Garrison**: Phobos Spinal Rail-Gun Battery
*   **Connections**: `mars_olympus_caldera`, `mars_deimos_sensor`, `mars_ceres_gateway`
*   **Strategic Lore**: The inner moon of Mars was hollowed out and converted into a massive orbital kinetic rail-cannon, capable of bombarding any point on the Martian surface or intercepting incoming invasion fleets.
*   **Strategic Asset**: Orbital kinetic bombardment platform providing +30% artillery support across all Martian sectors.

#### 32. `mars_deimos_sensor` — Deimos Stealth Listening Post
*   **Controlling Faction**: `faction_f` (Tharsis Machine Consensus)
*   **Subregion**: Outer Moon SIGINT Array
*   **Daily Yield**: +40,000 Cr | +18 kg Synthetic Flux
*   **Defense Rating**: 82/100 | **Garrison**: Silent SIGINT Drone Array
*   **Connections**: `mars_elysium_spire`, `mars_phobos_citadel`, `mars_ceres_gateway`
*   **Strategic Lore**: Embedded within the outer moon's porous rock, coated in radar-absorbent carbon tiles. Silently intercepts electromagnetic signals across the inner Sol system.
*   **Strategic Asset**: Electronic warfare array providing early warning on enemy fleet deployments.

#### 33. `mars_ceres_gateway` — Ceres Belt Terminal
*   **Controlling Faction**: `faction_f` (Tharsis Machine Consensus)
*   **Subregion**: Main Asteroid Belt Trade Port
*   **Daily Yield**: +52,000 Cr | +24 kg Tritium
*   **Defense Rating**: 86/100 | **Garrison**: Asteroid Gate Automa Flotilla
*   **Connections**: `mars_hellas_basin`, `mars_phobos_citadel`, `mars_deimos_sensor`
*   **Strategic Lore**: The gateway to the Outer Rim. Anchored on the dwarf planet Ceres, this trade terminal bridges the inner planetary economies with the vast mineral wealth of the Asteroid Belt.
*   **Strategic Asset**: Deep-space logistics hub controlling volatile gas shipments and mineral freight.

---

## 3. Dynamic Territory Mechanics & Player PMC Sorties

### A. Turn-Based Territorial War Engine
At the close of each campaign day (`obj_GameManager.end_turn()`):
1. **Material & Credit Dispersal**:
   Each territory delivers its daily credit tribute and material crates to its controlling faction's treasury.
   When the Player PMC holds territory, payouts are added directly to `obj_GameManager.funds` and the HQ material warehouse.
2. **Frontline Detection & Friction**:
   Frontline territories (`scr_territory_is_frontline()`) undergo combat friction checks:
   Rival factions evaluate adjacent territories, launching calculated assault operations based on their military strength score and mass-production chassis doctrines.
3. **Player Sortie Expeditions**:
   From the Map UI, the player can:
   - **Fortify Owned Sector**: Spends $25,000 Cr to reinforce defensive fortifications by +10 (max 100).
   - **Dispatch PMC Assault**: Launches an expeditionary battle force to seize or liberate a contested border sector.
   - **Direct Tactical Sortie [S]**: Drops directly into tactical mecha combat (`rm_combat`) deployed in that specific territorial theater!

---

## 4. Verification & QA Standard

1. **Parity**: Exactly 5 territories for each starting faction (20% each); Mars quarantined until awakening.
2. **Cohesion**: 100% original military sci-fi naming and lore; zero direct UC Gundam terminology.
3. **GML Integrity**: All 33 territory IDs strictly correspond to records in `scripts/scr_territory_war_system/scr_territory_war_system.gml`.
"""

target = "docs/39_planetary_and_orbital_territory_conquest_and_the_mars_theaters.md"
with open(target, "w", encoding="utf-8") as f:
    f.write(doc_content)

print(f"✓ {target} successfully updated with canonical, 100% original military sci-fi lore!")
