import glob
import re

for s in glob.glob('sprites/spr_ms_custom_*/*.yy'):
    with open(s, 'r', encoding='utf-8') as f:
        t = f.read()
    
    if '"resourceType": "GMSequence"' not in t and '"resourceType":"GMSequence"' not in t:
        pattern = r'("playbackSpeedType"\s*:\s*[0-9]+,)'
        replacement = r'\1\n    "resourceType": "GMSequence",\n    "resourceVersion": "2.0",'
        new_t = re.sub(pattern, replacement, t, count=1)
        with open(s, 'w', encoding='utf-8') as f:
            f.write(new_t)
        print(f"Added sequence resourceType to {s}")
