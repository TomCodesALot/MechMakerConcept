path = '/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_unit_sprites_review.md'
with open(path, 'r') as f:
    content = f.read()

# Remove the broken section 1.5 if present
if '## 1.5.' in content:
    start_pos = content.find('## 1.5.')
    end_pos = content.find('## 2. Interactive Unit Movement & Order Mechanics')
    content = content[:start_pos] + content[end_pos:]

new_section = """## 1.5. Two-Tier Macro/Micro Base Map Engine (Shin Gihren's Greed *Tokubetsu Kyoten*)

Directly adhering to the user's architectural vision and *Shin Gihren's Greed* mechanics, major territorial citadels on Earth now operate across **Two Discrete Tiers of Strategic Command**:

````carousel
![Tier 1: Global Planetary Overview](/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/live_earth_tier1_global_overview.png)
<!-- slide -->
![Tier 2: Dedicated Major Stronghold Base Map - Granite Deep Command](/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/live_earth_tier2_stronghold_granite_deep.png)
````

### Tier 1: Global Planetary Overview (`earth_view_mode == "GLOBAL"`)
* **Planetary Projection (`spr_map_earth_global`):** High-resolution 1376x768 satellite cartography displaying all continental landmasses with tactical latitude and equatorial transit telemetry.
* **10 Continental Citadels:**
  1. **Granite Deep Command** (South America Craton - Major Stronghold / Jaburo Archetype)
  2. **Cascadia Mass-Driver Complex** (North America Pacific Rim)
  3. **Gibraltar Sea-Gate Bastion** (Atlantic-Mediterranean Chokepoint)
  4. **Chimborazo Orbital Bastion** (Equatorial Andes Kinetic Gantry)
  5. **Skagerrak Sub-Sea Hangar** (North Sea / Nordic Sub-Surface Docks)
  6. **Woomera Proving Grounds** (Australasia Kinetic Test Range)
  7. **Neo-Shanghai Arcology Spire** (East Asian Heavy Industrial Foundry)
  8. **Al-Kufra Solar Gantry Array** (Sahara Solar-Thermal Elevator)
  9. **Ural Mountain Munitions Vault** (Eurasian Heavy Armory)
  10. **Vostok Sub-Glacial Vault** (Antarctic Cryogenic Archive)
* **Global Intercontinental Hyperlanes:** Red contested frontline corridors with assault direction arrows, moving strike wing patrols, and blue allied supply vectors.
* **Seamless Stronghold Entry:** Selecting a citadel marked with `★ MAJOR STRONGHOLD ★` illuminates the golden command button:  
  `[🔍 ENTER BASE THEATER (SEPARATE MAP) >>]`.

---

### Tier 2: Dedicated Major Stronghold Base Map (`earth_view_mode == "STRONGHOLD"`)
* **Dedicated Regional Theater (`spr_map_earth_theater`):** Zooms into the high-detail South American / Amazon Basin topographical map.
* **6 Discrete Tactical Defense Subnodes:**
  1. `granite_core`: **Subterranean Command Redoubt** (Core Bunker, 3000m deep underground, 95 DEF, MS Commander Division)
  2. `granite_north_gate`: **Amazon River Delta Flank Sentry** (River Gate bridgehead, Goliath Heavy Tanks)
  3. `granite_andes_battery`: **Chimborazo Andean Rail Redoubt** (Mountain Battery, Artillery MS)
  4. `granite_caribbean_dock`: **Caribbean Sea-Gate Anchorage** (Air/Naval slipways, Gunships)
  5. `granite_missile_silos`: **Mato Grosso Anti-Orbital Silos** (Rainforest Exo-Troopers)
  6. `granite_pacific_coast`: **Pacific Shoreline Forward Depot** (Perimeter Depot, Armed Technicals)
* **Local Perimeter Defense Vectors:** Fortified supply conduits and contested breach vectors connecting the subnodes.
* **Amber Satellite Radar Minimap:** Live orbital telemetry tracking the South America theater camera footprint on Earth (matching user upload `media_1792505836970.png`).
* **Tactical Terrain HUD:** Displays `SUBTERRANEAN GRANITE CRATON`, `+40% DEFENSE BONUS`, and `85% RADAR MASKING`.
* **Zero-Latency Zoom Out:** `[<< WORLD OVERVIEW [ESC]]` button at top-left of the radar and keyboard `ESC` smoothly returns to Tier 1.
"""

target = '## 2. Interactive Unit Movement & Order Mechanics'
assert target in content, 'Target heading not found'
content = content.replace(target, new_section + '\n\n' + target, 1)

with open(path, 'w') as f:
    f.write(content)

print('Cleanly updated tactical_unit_sprites_review.md!')
