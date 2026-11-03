import re

with open('objects/obj_HQTerminal/Draw_64_legacy_backup.gml') as f:
    legacy_lines = f.readlines()

# Extract other tabs from legacy backup
tab0_lines = legacy_lines[418:2266]   # active_tab == 0 (R&D)
tab1_lines = legacy_lines[2266:3181]  # active_tab == 1 (Factory)
tab2_lines = legacy_lines[3181:4187]  # active_tab == 2 (Contracts)
tab4_lines = legacy_lines[6365:7071]  # active_tab == 4 (Fleet)
modals_lines = legacy_lines[7071:]    # Modals from line 7072 to end

print(f"Extracted: Tab 0 ({len(tab0_lines)} lines), Tab 1 ({len(tab1_lines)} lines), Tab 2 ({len(tab2_lines)} lines), Tab 4 ({len(tab4_lines)} lines), Modals ({len(modals_lines)} lines)")
