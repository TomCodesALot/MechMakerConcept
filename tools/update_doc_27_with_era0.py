import re

d27_path = "docs/27_competitor_rd_timeline_eras_and_random_events.md"
with open(d27_path, "r") as f:
    text = f.read()

old_table = """| Tech Era | Calendar Window | Doctrinal Theme | Baseline Line Units | Tender Bounty Scale |
| :--- | :--- | :--- | :--- | :--- |
| **Era I: Early War Shakedown** | Years 1–2 (Turns 1–50) | Conventional kinetics, light aerosteel, rudimentary beam rifles | *Bulwark*, *Sylph*, *Marauder*, *Ronin* | $800,000 - 1,200,000$ Cr |"""

new_table = """| Tech Era | Calendar Window | Doctrinal Theme | Baseline Line Units | Tender Bounty Scale |
| :--- | :--- | :--- | :--- | :--- |
| **Era 0: Conventional Warfare & MS Genesis** | Year 0 (Turns 1–40 / Until MS Sortie) | Main Battle Tanks, Atmospheric Strike Jets, Skiffs, Gun Trucks | *T-720 Mammoth*, *A-14 Skyhammer*, *K-4 Stiletto*, *SCR-T01 Technical* | $250,000 - 450,000$ Cr |
| **Era I: The First Mover Catalyst & Arms Race** | Years 1–2 (Turns 41–90 / 365-Day R&D Clock) | Player MS Monopoly; Competitors rush 365-day reverse-engineering | *Unit-01 Ironclad* (Player) vs Conventional Armor / Walking Testbeds | $1,200,000 - 2,000,000$ Cr (3.0x Prometheus Subsidy) |
| **Era I-B: Competitor Mobile Suit Rollout** | Year 2 (Turns 91–120) | First rival reverse-engineered MS hit the field | *Bulwark*, *Sylph*, *Marauder*, *Ronin* | $1,500,000 - 2,200,000$ Cr |"""

if old_table in text:
    text = text.replace(old_table, new_table)
    print("Updated Tech Eras table in doc 27.")

with open(d27_path, "w") as f:
    f.write(text)

print("docs/27 updated successfully.")
