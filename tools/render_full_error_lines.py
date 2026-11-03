from PIL import Image

im = Image.open('/home/tom/.gemini/antigravity-ide/brain/a9197ef4-c206-4eb1-b4b4-83dfffe898d6/error_text_box.png')
w, h = im.size

binary = []
for y in range(h):
    row = []
    for x in range(w):
        p = im.getpixel((x, y))
        is_dark = (sum(p[:3]) < 500)
        row.append(1 if is_dark else 0)
    binary.append(row)

rows_with_text = [y for y in range(h) if any(binary[y])]
blocks = []
cur = [rows_with_text[0]]
for y in rows_with_text[1:]:
    if y - cur[-1] > 2:
        blocks.append(cur)
        cur = [y]
    else:
        cur.append(y)
blocks.append(cur)

# Let's inspect each block across full width in chunks of 100 chars
for idx, b in enumerate(blocks):
    min_x = min(x for y in b for x in range(w) if binary[y][x])
    max_x = max(x for y in b for x in range(w) if binary[y][x])
    print(f"=== BLOCK {idx+1} (x={min_x}..{max_x}, y={b[0]}..{b[-1]}) ===")
    for chunk_start in range(min_x, max_x+1, 120):
        chunk_end = min(chunk_start+120, max_x+1)
        print(f"--- columns {chunk_start}..{chunk_end} ---")
        for y in b:
            line_str = "".join("#" if binary[y][x] else " " for x in range(chunk_start, chunk_end))
            print(line_str)
