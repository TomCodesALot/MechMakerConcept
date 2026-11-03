import os
import glob
from PIL import Image
from collections import deque

def clean_sprite_surface(im):
    w, h = im.size
    to_clear = set()
    
    # 1. Check for floating text with gap
    counts = [sum(1 for x in range(w) if im.getpixel((x, y))[3] > 10) for y in range(45)]
    top_rows = [y for y in range(15, 33) if counts[y] > 5]
    if top_rows:
        gap_rows = [y for y in range(max(top_rows) + 1, 38) if counts[y] == 0]
        if gap_rows:
            cutoff = min(gap_rows)
            for y in range(0, cutoff + 1):
                for x in range(w):
                    to_clear.add((x, y))

    # 2. Check for solid card box background
    edge_px_count = 0
    for y in range(25, 95):
        for x in [16, 17, 18, 142, 143, 144]:
            r, g, b, a = im.getpixel((x, y))
            if a > 60 and abs(r-g)<=16 and abs(g-b)<=16 and abs(r-b)<=22 and 18<=r<=115:
                edge_px_count += 1

    if edge_px_count > 25:
        # Clear entire top card banner (rows 0..34)
        for y in range(0, 35):
            for x in range(w):
                to_clear.add((x, y))
                
        # Flood-fill card flanks from edges
        visited = set()
        seeds = []
        for y in range(h):
            for x in [0, 1, 15, 16, 17, w-2, w-1, 143, 144]:
                seeds.append((x, y))
        for x in range(w):
            seeds.append((x, 0))
            seeds.append((x, 1))
            seeds.append((x, 34))
            
        q = deque(seeds)
        for s in seeds: visited.add(s)
        
        while q:
            cx, cy = q.popleft()
            if not (0 <= cx < w and 0 <= cy < h): continue
            r, g, b, a = im.getpixel((cx, cy))
            if a == 0 or (cx, cy) in to_clear:
                for nx, ny in [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]:
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        q.append((nx, ny))
                continue
                
            diff_rg = abs(r - g)
            diff_gb = abs(g - b)
            diff_rb = abs(r - b)
            is_card_gray = (diff_rg <= 16 and diff_gb <= 16 and diff_rb <= 22 and 18 <= r <= 115)
            is_edge_fringe = (r < 50 and g < 50 and b < 50 and a < 220)
            
            if is_card_gray or is_edge_fringe:
                to_clear.add((cx, cy))
                for nx, ny in [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]:
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        q.append((nx, ny))

    # 3. Bottom pedestal removal (y >= 134)
    for y in range(134, h):
        for x in range(w):
            if im.getpixel((x, y))[3] > 0:
                to_clear.add((x, y))

    if not to_clear:
        return 0

    for cx, cy in to_clear:
        im.putpixel((cx, cy), (0, 0, 0, 0))
        
    return len(to_clear)

def main():
    patterns = [
        'sprites/spr_ms_*/**/*.png',
        'sprites/spr_ms_*/*.png',
        'sprites/spr_veh_*/**/*.png',
        'sprites/spr_veh_*/*.png',
        'sprites/spr_inf_*/**/*.png',
        'sprites/spr_inf_*/*.png'
    ]
    
    all_files = set()
    for pat in patterns:
        for p in glob.glob(pat, recursive=True):
            all_files.add(p)
            
    print(f'Total PNG files found across mechs, vehicles, infantry: {len(all_files)}')
    
    modified_files = 0
    total_pixels_cleaned = 0
    per_sprite_stats = {}
    
    for p in sorted(all_files):
        try:
            im = Image.open(p).convert('RGBA')
            cleared = clean_sprite_surface(im)
            if cleared > 0:
                im.save(p)
                modified_files += 1
                total_pixels_cleaned += cleared
                spr_dir = p.split('/')[1]
                per_sprite_stats[spr_dir] = per_sprite_stats.get(spr_dir, 0) + cleared
        except Exception as e:
            print(f'Error processing {p}: {e}')
            
    print(f'Done! Modified {modified_files} files, cleared {total_pixels_cleaned} pixels.')
    print('Per-sprite cleanup summary:')
    for spr, px in sorted(per_sprite_stats.items()):
        print(f'  {spr:35}: {px:6d} pixels purged')

if __name__ == "__main__":
    main()
