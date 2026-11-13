"""Automated Art Asset Analyst QA Scanner for GameMaker sprites."""
import glob
import json
import os
import re
from PIL import Image


def audit_all_sprites():
    issues = []
    yy_paths = sorted(glob.glob("sprites/*/*.yy"))
    for yy_path in yy_paths:
        sdir = os.path.dirname(yy_path)
        sname = os.path.basename(sdir)
        raw = open(yy_path, encoding="utf-8").read()
        data = json.loads(re.sub(r",(\s*[}\]])", r"\1", raw))
        frames = [f["name"] for f in data.get("frames", [])]
        layers = [l["name"] for l in data.get("layers", [])]

        frame_bytes = []
        for idx, fid in enumerate(frames):
            root_png = os.path.join(sdir, fid + ".png")
            if not os.path.exists(root_png):
                issues.append(f"[MISSING ROOT PNG] {sname} frame {idx} ({fid}.png)")
                continue
            for lid in layers:
                lp = os.path.join(sdir, "layers", fid, lid + ".png")
                if not os.path.exists(lp):
                    issues.append(f"[MISSING LAYER PNG] {sname} frame {idx} layer {lid}")

            im = Image.open(root_png).convert("RGBA")
            frame_bytes.append(im.tobytes())
            if idx == 0 and sname.startswith("spr_ms_"):
                w, h = im.size
                px = im.load()
                halo = 0
                pinholes = 0
                for y in range(1, h - 1):
                    for x in range(1, w - 1):
                        r, g, b, a = px[x, y]
                        if a == 0:
                            opaque_n = sum(
                                1 for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))
                                if px[x + dx, y + dy][3] > 0
                            )
                            if opaque_n == 4:
                                pinholes += 1
                        elif (r + g + b) / 3.0 > 205 and (max(r, g, b) - min(r, g, b)) < 30:
                            if any(px[x + dx, y + dy][3] == 0 for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))):
                                halo += 1
                if halo > 40:
                    issues.append(f"[WHITE HALO] {sname}: {halo} bright edge pixels in frame 0")
                if pinholes > 15:
                    issues.append(f"[PINHOLES] {sname}: {pinholes} 1px transparent holes inside armor")

        if len(frame_bytes) > 1 and len(set(frame_bytes)) == 1:
            issues.append(f"[FROZEN ANIM] {sname}: all {len(frame_bytes)} frames are identical")

    print(f"Audited {len(yy_paths)} sprites. Issues found: {len(issues)}")
    for it in issues[:40]:
        print(" ", it)


if __name__ == "__main__":
    audit_all_sprites()

