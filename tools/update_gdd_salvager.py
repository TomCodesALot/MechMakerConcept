with open("docs/51_rpg_mechanics_and_prologue_gdd.md", "r") as f:
    gdd = f.read()

target = """1. **Commander Dossier Creation**: Player selects Callsign, Name, Portrait, and 1 of 4 Background Origins:
   - **Ex-Terran Coalition Officer**: +15 Terran Standing, Artillery Spotter perk, +10% Kinetic Damage, starter GHA-07 Ironclad mech.
   - **Spacenoid Guerrilla**: +15 Colonies Standing, Vernier Ace perk, +15% Evasion, +10% Beam Damage, starter Aero-Striker mech.
   - **Zaibatsu Cybernetics Defector**: +10 Zaibatsu Standing, +15% Crit Chance, ECM Jammer perk, +50,000 Credits, starter Hover-Sniper mech.
   - **Scavenger Veteran**: +15 Syndicate Standing, +25% Alloy Salvage, +15% Mech Armor Durability, starter Heavy Brawler mech."""

replacement = """1. **Space Salvager Origin Questionnaire (4-Step Origin Calibration)**:
   - Grounded setting: The player begins as a bottom-of-the-barrel Space Salvager in the Cascadia debris belt before discovering the derelict warship USN-X Hephaestus.
   - **Question I (Past Exile)**: Ex-Terran Mutineer (+10% Kinetic DMG, +10% Accuracy), Escaped Jovian Miner (+15% Evasion, +10% Heat Venting), Cybernetics Fugitive (+15% Crit Chance, ECM Jammer), or Born to the Rust (+25% Salvage, +15% Frame Durability).
   - **Question II (Junk Rig Assembled)**: Jury-Rigged Ironclad (Biped), Jury-Rigged Aero-Striker (High-Mobility), Converted Hover-Sniper (Optic Recon), or Tread-Brawler Demolisher (Heavy Tractor).
   - **Question III (Tactical Instinct)**: Point-Blank Breach (+10% Weapon Damage), Evasive Plasma Decoy (+10% Evasion, +1 AP turn 1), Slick Hustle (+20k Credits, +10 Syndicate Standing), or Unbreakable Bulwark (+15% Torso/Arm Armor).
   - **Question IV (Beacon Discovery)**: Encrypted Military SOS SEC-00, Uncontained Reactor Radiation Flare, or Pirate Comm Intercept Free Salvage.
   - **Step 5 (Dossier Confirmation)**: Custom callsign cycler (RUST-1, VANGUARD, GHOST, ANVIL, VALKYRIE, etc.), portrait switcher (Male, Female, Cybernetic, Shadow), and Rig confirmation before staking salvage claim."""

assert target in gdd, "target in GDD not found"
gdd = gdd.replace(target, replacement, 1)

with open("docs/51_rpg_mechanics_and_prologue_gdd.md", "w") as f:
    f.write(gdd)

print("GDD 51 updated with Space Salvager Questionnaire specification.")
