import sys

with open('objects/obj_HQTerminal/Draw_64_legacy_backup.gml', 'r') as f:
    legacy_lines = f.readlines()

tab0_code = "".join(legacy_lines[418:2266])   # R&D
tab1_code = "".join(legacy_lines[2266:3181])  # Factory
tab2_code = "".join(legacy_lines[3181:4187])  # Contracts
tab4_code = "".join(legacy_lines[6365:7071])  # Fleet
modals_code = "".join(legacy_lines[7071:])    # Modals & Overlays

with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
    warmap_lines = f.readlines()

print(f"Legacy lines: {len(legacy_lines)}, Warmap lines: {len(warmap_lines)}")
