d00_path = "docs/00_master_game_design_document.md"
with open(d00_path, "r") as f:
    text = f.read()

target = "6. **Mobile Flagship Dreadnought Progression:** A sprawling 8-division, 5-tier upgrade tree transforming a derelict command cruiser into an interstellar behemoth capable of instantaneous Tachyon Fold jumps and apocalyptic orbital artillery strikes."
addition = target + "\n7. **The Prometheus Catalyst & Dawn of the Mobile Suit:** The player's independent foundry is the singular catalyst that invents and deploys the first operational bipedal Mobile Suit in human history. The universe begins in Era 0 (Conventional Warfare: Main Battle Tanks, Strike Jets, Skiffs, Gun Trucks), where the player's maiden sortie shocks the solar system, flipping hostile superpowers into high-bounty contract partners (3.0x Prometheus Subsidies) and triggering a 365-day reverse-engineering arms race across four rival defense megacorporations."

if target in text and "7. **The Prometheus Catalyst" not in text:
    text = text.replace(target, addition)
    with open(d00_path, "w") as f:
        f.write(text)
    print("Updated docs/00_master_game_design_document.md with Pillar 7.")
else:
    print("Doc 00 already updated or target not found.")
