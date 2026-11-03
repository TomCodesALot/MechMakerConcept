import os
import glob
from PIL import Image

cleaned_files = 0

for p in glob.glob("sprites/spr_ms_*/*.png"):
    try:
        im = Image.open(p).convert("RGBA")
        w, h = im.size
        modified = False
        
        # 1. Scrub gray pedestal boxes in rows 90..134
        for y in range(90, h):
            for x in range(w):
                r, g, b, a = im.getpixel((x, y))
                if a > 0:
                    # Check for pedestal gray/slate (roughly 60..85, 70..92, 75..98)
                    if 58 <= r <= 88 and 68 <= g <= 96 and 72 <= b <= 102 and abs(r - g) < 18 and abs(g - b) < 16:
                        im.putpixel((x, y), (0, 0, 0, 0))
                        modified = True
                    # Clear anything strictly at or below y=134 (where baked text, watermarks, reticle bases live)
                    elif y >= 134:
                        im.putpixel((x, y), (0, 0, 0, 0))
                        modified = True

        if modified:
            im.save(p)
            cleaned_files += 1
    except Exception as e:
        print(f"Error on {p}: {e}")

print(f"Cleaned {cleaned_files} sprite PNGs of baked pedestals and text labels.")
