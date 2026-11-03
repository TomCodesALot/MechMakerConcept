import re

with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
    text = f.read()

# Let's inspect the current Draw_64 to see what needs to be replaced or enhanced
print("Current length of Draw_64:", len(text))
