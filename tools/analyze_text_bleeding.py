from PIL import Image
import glob
import os

images = sorted(glob.glob('/home/tom/.gemini/antigravity-ide/brain/a9197ef4-c206-4eb1-b4b4-83dfffe898d6/qa_*.png'))
images = [img for img in images if not img.endswith('_thumb.png')]

for img_path in images:
    name = os.path.basename(img_path)
    im = Image.open(img_path).convert('L')
    w, h = im.size
    
    # Check rightmost 100 pixels (x from w - 100 to w)
    # Exclude top bar (y < 80) and bottom bar (y > h - 80)
    right_bleed = []
    for y in range(80, h - 80, 5):
        row = [im.getpixel((x, y)) for x in range(w - 60, w)]
        bright = [val for val in row if val > 160]
        if len(bright) > 5:
            right_bleed.append((y, len(bright)))
            
    # Check bottommost 40 pixels (y from h - 40 to h)
    bot_bleed = []
    for x in range(80, w - 80, 10):
        col = [im.getpixel((x, y)) for y in range(h - 30, h)]
        bright = [val for val in col if val > 160]
        if len(bright) > 3:
            bot_bleed.append((x, len(bright)))

    print(f"[{name}] (size {w}x{h}): Right bleed rows={len(right_bleed)}, Bottom bleed cols={len(bot_bleed)}")
    if right_bleed:
        print(f"   Right bleed y-ranges: min_y={min(r[0] for r in right_bleed)}, max_y={max(r[0] for r in right_bleed)}")
    if bot_bleed:
        print(f"   Bottom bleed x-ranges: min_x={min(c[0] for c in bot_bleed)}, max_x={max(c[0] for c in bot_bleed)}")
