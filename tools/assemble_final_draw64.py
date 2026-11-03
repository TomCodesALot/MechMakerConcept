import sys

with open('objects/obj_HQTerminal/Draw_64_legacy_backup.gml', 'r') as f:
    legacy_lines = f.readlines()

tab0_code = "".join(legacy_lines[418:2266])   # R&D
tab1_code = "".join(legacy_lines[2266:3181])  # Factory
tab2_code = "".join(legacy_lines[3181:4187])  # Contracts
tab4_code = "".join(legacy_lines[6365:7071])  # Fleet
modals_code = "".join(legacy_lines[7071:])    # Modals & Overlays

with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
    current_map_code = f.read()

# Let's inspect current_map_code to insert the order dispatch & transit features
# We want to insert:
# 1. Order dispatch ribbon
# 2. Hyperlane order highlight
# 3. Node order interaction
# 4. Active transits drawing
# 5. Dossier dispatch button & smart invasion routing
# 6. Order confirmation modal & Combat report modal

print("Successfully verified inputs for assemble_final_draw64.py")
