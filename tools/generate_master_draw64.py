import os

with open('objects/obj_HQTerminal/Draw_64_legacy_backup.gml', 'r') as f:
    legacy_lines = f.readlines()

tab0_code = "".join(legacy_lines[418:2266])   # R&D
tab1_code = "".join(legacy_lines[2266:3181])  # Factory
tab2_code = "".join(legacy_lines[3181:4187])  # Contracts
tab4_code = "".join(legacy_lines[6365:7071])  # Fleet
modals_code = "".join(legacy_lines[7071:])    # Modals & Overlays

with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
    current_map_code = f.read()

# Let's extract from current_map_code the theater tabs, radar, dossier, hegemony strip, etc.
# Find where the top bar ends in current_map_code (around CELESTIAL THEATER NAVIGATION TABS)
cel_idx = current_map_code.find('// 3. CELESTIAL THEATER NAVIGATION TABS')
if cel_idx == -1:
    cel_idx = current_map_code.find('CELESTIAL THEATER NAVIGATION TABS')

warmap_core_code = current_map_code[cel_idx:]
print("Warmap core code starts with:", warmap_core_code[:120])
