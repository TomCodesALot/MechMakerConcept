path = '/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_unit_sprites_review.md'
with open(path, 'r') as f:
    content = f.read()

# Replace section 1.5 with the expanded multi-stronghold review
start_pos = content.find('## 1.5.')
end_pos = content.find('## 2. Interactive Unit Movement & Order Mechanics')

expanded_section = """## 1.5. Comprehensive Two-Tier Stronghold Architecture (*Tokubetsu Kyoten* Multi-Base Network)

Adhering to the user's directive, the 2-tier command deck has been expanded across **all 10 Continental Citadels on Earth** as well as **Mount Olympus on Mars**. Every major base operates as a discrete tactical stronghold map with tailored defense sub-nodes, custom tactical plinths, and live orbital minimap telemetry:

````carousel
![Tier 1: Global Planetary Overview](/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/live_earth_tier1_global_overview.png)
<!-- slide -->
![Tier 2: Granite Deep Command (South America Stronghold)](/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/live_earth_tier2_stronghold_granite_deep.png)
<!-- slide -->
![Tier 2: Cascadia Mass-Driver Citadel (North America Stronghold)](/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/live_stronghold_cascadia_mass_driver.png)
<!-- slide -->
![Tier 2: Gibraltar Sea-Gate Fortress (Mediterranean Maritime Stronghold)](/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/live_stronghold_gibraltar_sea_gate.png)
<!-- slide -->
![Tier 2: Mount Olympus Zenith Redoubt (Martian Super-Volcano Stronghold)](/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/live_stronghold_olympus_caldera_mars.png)
````

### Active Stronghold Base Map Network (11 Dedicated Theaters)

| Stronghold Citadel | Theater / Region | Core Defense Structure | Archetype & Strategic Role | Minimap Bounding Tracking |
|---|---|---|---|---|
| **Granite Deep Command** | Earth (South America) | Subterranean Command Redoubt (95 DEF) | Jaburo Subterranean Fortress & Fusion Reactor | Amazonian Basin (`x:48, y:54`) |
| **Cascadia Mass-Driver** | Earth (North America) | Orbital Launch Rail Apex (92 DEF) | California Base / Pacific Aerospace Mass Launcher | Pacific Northwest (`x:28, y:24`) |
| **Gibraltar Sea-Gate** | Earth (Europe / Iberia) | Rock of Gibraltar Bastion (96 DEF) | Mediterranean Chokepoint & Acoustic Net | Strait of Gibraltar (`x:94, y:28`) |
| **Ural Munitions Megafoundry** | Earth (Eurasia / Russia) | Yamantau Central Smelter & Forge (94 DEF) | Odessa Heavy Mining & Mobile Armor Vault | Ural Mountains (`x:124, y:20`) |
| **Neo-Shanghai Arcology** | Earth (East Asia) | Arcology Spire & Datavault (93 DEF) | Zaibatsu Cybernetic Spire & Maglev Hub | Yangtze Estuary (`x:144, y:32`) |
| **Al-Kufra Solar Gantry** | Earth (North Africa) | Solar Mirror Field & Uplink Core (91 DEF) | Kilimanjaro Solar-Thermal Orbital Beam Array | Sahara Desert (`x:96, y:44`) |
| **Skagerrak Sub-Sea Hangar** | Earth (Northern Europe) | Fjord Submarine Grotto Pens (92 DEF) | Belfast Submarine Docks & Kattegat Defense | North Sea / Fjord (`x:94, y:22`) |
| **Woomera Proving Grounds** | Earth (Australasia) | Underground Warhead Vault (94 DEF) | Torrington Nuclear / Kinetic Prototype Range | Outback Salt Flats (`x:154, y:64`) |
| **Chimborazo Orbital Bastion** | Earth (Equatorial Andes) | Equatorial High-Angle Mass Launcher (95 DEF) | Equatorial Andes Rail Gantry & Cloud Silos | Equatorial Spine (`x:44, y:48`) |
| **Vostok Sub-Glacial Vault** | Earth (Antarctica) | Sub-Glacial Geothermal Core (97 DEF) | Cryogenic Research Archive & Geothermal Well | South Pole Shelf (`x:85, y:88`) |
| **Mount Olympus Zenith** | Mars (Tharsis Region) | Caldera Rim Heavy Fusion Redoubt (98 DEF) | 22km High Super-Volcano Sovereign Citadel | Olympus Caldera (`x:38, y:28`) |

---

### Key Operational Features
1. **Dynamic Regional Map Loading:** Stronghold view queries `scr_stronghold_get_layout(_stronghold_id)` and switches between `spr_map_earth_theater` and `spr_map_mars_theater`.
2. **Context-Aware Orbital Telemetry:** The top-right satellite minimap dynamically draws the active camera coordinate box matching that citadel's exact planetary footprint.
3. **Subnode Defense Fortifications:** Players can spend faction funds to fortify individual subnodes (`+10 DEF`) or sortie combat wings directly into that subnode's tactical arena.
4. **Instant Zero-Loss Zoom Out:** Clicking `[<< WORLD OVERVIEW [ESC]]` or pressing `ESC` seamlessly returns the commander to the planetary overview.
"""

content = content[:start_pos] + expanded_section + "\n\n" + content[end_pos:]

with open(path, 'w') as f:
    f.write(content)

print("Updated tactical_unit_sprites_review.md with all 11 strongholds!")
