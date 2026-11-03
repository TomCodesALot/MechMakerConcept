#!/usr/bin/env python3
import re

path = "objects/obj_HQTerminal/Draw_64.gml"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# Tab 0: R&D
c = re.sub(r"var _sub_w = 380;", "var _sub_w = floor((_pan_w - 48) / 3);", c, count=1)
# Tab 1: Factory
c = re.sub(r"var _fsub_w = 390;", "var _fsub_w = floor((_pan_w - 48) / 3);", c, count=1)
# Tab 2: Contracts
c = re.sub(r"var _csub_w = 370;", "var _csub_w = floor((_pan_w - 48) / 3);", c, count=1)
# Tab 3: War Map
c = re.sub(r"var _wsub_w = 232;", "var _wsub_w = floor((_pan_w - 48) / 5);", c, count=1)
# Tab 4: Flagship
c = re.sub(r"var _fsub_w = 380;", "var _fsub_w = floor((_pan_w - 48) / 3);", c, count=1)

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

print("✓ Subtab widths successfully responsive to _pan_w.")
