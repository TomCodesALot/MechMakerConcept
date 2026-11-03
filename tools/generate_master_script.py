import re

with open('objects/obj_HQTerminal/Draw_64_legacy_backup.gml', 'r') as f:
    legacy_lines = f.readlines()

# Extract legacy sections
# Left dock is lines 240 to 418
dock_code = "".join(legacy_lines[239:418])
tab0_code = "".join(legacy_lines[418:2266])   # R&D
tab1_code = "".join(legacy_lines[2266:3181])  # Factory
tab2_code = "".join(legacy_lines[3181:4187])  # Contracts
tab4_code = "".join(legacy_lines[6365:7071])  # Fleet
modals_code = "".join(legacy_lines[7071:])    # Modals & Overlays

with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
    map_code = f.read()

print("Extracted legacy blocks successfully.")
