import re

with open('objects/obj_BattleManager/Draw_64.gml', 'r') as f:
    text_draw = f.read()

# Replace lines from "= 1. TOP MISSION & PLATOON TIMELINE HUD BAR" up to "= 4. COMMAND ACTION BAR"
# with the new Gihren's Greed + Front Mission UI suite!

start_marker = "// ========================================================================="
start_idx = text_draw.find("// =========================================================================")
# Find the end of the combat text layer or settings modal
end_marker = "// ========================================================================="
# Let's inspect where the main HUD sections are
print("Searching markers...")
