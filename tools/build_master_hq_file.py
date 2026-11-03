import os

with open('objects/obj_HQTerminal/Draw_64_legacy_backup.gml', 'r') as f:
    legacy_lines = f.readlines()

dock_code = "".join(legacy_lines[239:418])
tab0_code = "".join(legacy_lines[418:2266])   # R&D
tab1_code = "".join(legacy_lines[2266:3181])  # Factory
tab2_code = "".join(legacy_lines[3181:4187])  # Contracts
tab4_code = "".join(legacy_lines[6365:7071])  # Fleet
modals_code = "".join(legacy_lines[7071:])    # Modals & Overlays

# Let's read current map code
with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
    map_text = f.read()

# Let's find the war map section starting from CELESTIAL THEATER NAVIGATION TABS
cel_idx = map_text.find('// 3. CELESTIAL THEATER NAVIGATION TABS')
# And where the war map ends (before SETTINGS MODAL DIALOG)
set_idx = map_text.find('// 7. SETTINGS MODAL DIALOG')

warmap_section = map_text[cel_idx:set_idx]

print("Warmap section length:", len(warmap_section))
