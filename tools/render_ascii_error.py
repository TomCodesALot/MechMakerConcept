from PIL import Image

im = Image.open('/home/tom/.gemini/antigravity-ide/brain/a9197ef4-c206-4eb1-b4b4-83dfffe898d6/error_text_box.png')
w, h = im.size

# Threshold to binary (1 for text, 0 for background)
# Background is ~245
binary = []
for y in range(h):
    row = []
    for x in range(w):
        p = im.getpixel((x, y))
        is_dark = (sum(p[:3]) < 500)
        row.append(1 if is_dark else 0)
    binary.append(row)

# Find non-empty rows
rows_with_text = [y for y in range(h) if any(binary[y])]
if not rows_with_text:
    print("No text rows found!")
    exit(0)

# Render horizontal slices as ASCII
# Gap between lines is usually empty rows
blocks = []
cur = [rows_with_text[0]]
for y in rows_with_text[1:]:
    if y - cur[-1] > 2:
        blocks.append(cur)
        cur = [y]
    else:
        cur.append(y)
blocks.append(cur)

print(f"Found {len(blocks)} text blocks.")
for idx, b in enumerate(blocks):
    print(f"\n--- Block {idx+1} (y={b[0]}..{b[-1]}) ---")
    # find min_x, max_x for this block
    min_x = min(x for y in b for x in range(w) if binary[y][x])
    max_x = max(x for y in b for x in range(w) if binary[y][x])
    # print up to 120 chars wide
    for y in b:
        line_str = "".join("#" if binary[y][x] else " " for x in range(min_x, min(min_x+120, max_x+1)))
        if line_str.strip():
            print(line_str)
