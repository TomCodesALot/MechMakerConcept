artifact_path = "/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_unit_sprites_review.md"
with open(artifact_path, "r", encoding="utf-8") as f:
    text = f.read()

old_carousel = """````carousel
![Shin Gihren's Greed In-Situ Map Benchmark — Live Hyperlanes, Defending Stacks & Strike Wings](/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_map_shin_gihren_style.png)
<!-- slide -->
![Complete Tactical Counter Showcase — Mobile Suits, Conventional Vehicles, Infantry & Faction Plinths](/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_counters_showcase.png)"""

new_carousel = """````carousel
![Live GameMaker In-Engine War Map (1366x768) — Shin Gihren's Greed Counters, Hyperlanes, Minimap & Tac-Card](/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/live_gamemaker_map_verified.png)
<!-- slide -->
![Shin Gihren's Greed In-Situ Map Benchmark — Live Hyperlanes, Defending Stacks & Strike Wings](/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_map_shin_gihren_style.png)
<!-- slide -->
![Complete Tactical Counter Showcase — Mobile Suits, Conventional Vehicles, Infantry & Faction Plinths](/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_counters_showcase.png)"""

text = text.replace(old_carousel, new_carousel)
with open(artifact_path, "w", encoding="utf-8") as f:
    f.write(text)

print("✓ Updated review artifact with live GameMaker in-engine map slide!")
