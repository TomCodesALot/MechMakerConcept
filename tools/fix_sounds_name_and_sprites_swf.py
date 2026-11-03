import os
import glob
import re

# 1. Fix sounds
sounds = glob.glob('sounds/*/*.yy')
print(f"Fixing root 'name' in {len(sounds)} sounds...")
for s in sounds:
    snd_name = os.path.basename(os.path.dirname(s))
    with open(s, 'r', encoding='utf-8') as f:
        t = f.read()
    
    if f'"name":"{snd_name}"' not in t and f'"name": "{snd_name}"' not in t:
        pattern = r'("exportDir"\s*:\s*""\s*,)'
        replacement = f'\\1\n  "name":"{snd_name}",'
        new_t = re.sub(pattern, replacement, t, count=1)
        if new_t == t:
            # try after duration if exportDir didn't match
            pattern = r'("duration"\s*:\s*[0-9\.]+\s*,)'
            replacement = f'\\1\n  "exportDir":"",\n  "name":"{snd_name}",'
            new_t = re.sub(pattern, replacement, t, count=1)
            
        with open(s, 'w', encoding='utf-8') as f:
            f.write(new_t)
        print(f"Updated sound: {snd_name}")

# 2. Fix sprites swfPrecision
sprites = glob.glob('sprites/*/*.yy')
count = 0
for sp in sprites:
    with open(sp, 'r', encoding='utf-8') as f:
        t = f.read()
    
    if '"swfPrecision"' not in t:
        pattern = r'("swatchColours"\s*:\s*null\s*,)'
        replacement = r'\1\n  "swfPrecision": 2.525,'
        new_t = re.sub(pattern, replacement, t, count=1)
        with open(sp, 'w', encoding='utf-8') as f:
            f.write(new_t)
        count += 1
        print(f"Added swfPrecision to: {sp}")

print(f"Added swfPrecision to {count} sprites.")
