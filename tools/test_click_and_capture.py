import subprocess
import time
import os
from PIL import Image

def run_cmd(cmd):
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.stdout.strip()

lines = run_cmd("wmctrl -l").splitlines()
game_lines = [l for l in lines if l.endswith("MechMakerConcept")]
assert game_lines, "Could not find MechMakerConcept game window!"
win_id = game_lines[0].split()[0]
print(f"Targeting window: {win_id}")

# 1. Activate window
run_cmd(f"DISPLAY=:0 xdotool windowactivate --sync {win_id} windowraise {win_id}")
time.sleep(0.5)

# Click the [SKIP TO COMMAND DECK] button or [CONFIRM] button
# Try multiple Y coordinates around 680-720
for cy in [688, 700, 715, 730]:
    # Click skip button at x=265
    run_cmd(f"DISPLAY=:0 xdotool mousemove --window {win_id} 265 {cy} click 1")
    time.sleep(0.1)
    # Also click appoint button at x=1050
    run_cmd(f"DISPLAY=:0 xdotool mousemove --window {win_id} 1050 {cy} click 1")
    time.sleep(0.1)

# Send Space and Return
run_cmd(f"DISPLAY=:0 xdotool key Return")
time.sleep(0.2)
run_cmd(f"DISPLAY=:0 xdotool key space")
time.sleep(0.5)

# Capture fullscreen
shot_path = "/tmp/after_dismiss.png"
run_cmd(f"spectacle -b -n -f -o {shot_path}")
if os.path.exists(shot_path):
    im = Image.open(shot_path)
    # Crop window bounds (74, 68, 74+2732, 68+1536)
    crop = im.crop((74, 68, min(im.width, 74+2732), min(im.height, 68+1536)))
    crop.save("/home/tom/.gemini/antigravity-ide/brain/a9197ef4-c206-4eb1-b4b4-83dfffe898d6/live_command_deck_verified.png")
    # Save thumbnail
    thumb = crop.resize((crop.width // 4, crop.height // 4), Image.LANCZOS)
    thumb.save("/home/tom/.gemini/antigravity-ide/brain/a9197ef4-c206-4eb1-b4b4-83dfffe898d6/live_command_deck_verified_thumb.png")
    
    # Analyze colors in crop
    colors = set()
    for y in range(0, crop.height, 15):
        for x in range(0, crop.width, 15):
            colors.add(crop.getpixel((x, y))[:3])
    print(f"Captured live_command_deck_verified: {crop.size}, Unique sampled colors: {len(colors)}")
    
    # Check top HUD banner (y=100..250 in 2x scale = y=50..125 in 1x scale)
    top_colors = set(crop.getpixel((x, 150))[:3] for x in range(100, crop.width-100, 20))
    print(f"Top HUD row colors: {len(top_colors)}, Sample: {list(top_colors)[:5]}")
