import json

# Update obj_BlueprintManager/Create_0.gml
bpm_path = "objects/obj_BlueprintManager/Create_0.gml"
with open(bpm_path, "r") as f:
    code = f.read()

old_lore = '_ironclad.manufacturing_lore = "Engineered by Vanguard Defense Systems to resolve the Orbital Beachhead Crisis. Sacrifices flight agility for impenetrable composite plating and heavy kinetic saturation.";'
new_lore = '_ironclad.manufacturing_lore = "PROJECT PROMETHEUS (Unit-01 Prototype): The world\'s first operational bipedal Mobile Suit, engineered in secret inside our mobile Dreadnought Foundry. Combines compact Tokamak thermonuclear fusion with hydraulic limbs to shatter conventional armored warfare.";'

old_rep = '_ironclad.battlefield_reputation = "Nicknamed \'The Walking Vault\' - shrugs off solid slug fire and pulverizes enemy trench lines.";'
new_rep = '_ironclad.battlefield_reputation = "Nicknamed \'The Walking God of War\' - impervious to conventional tank shells, capable of leaping trenches and crushing armored columns in close combat.";'

if old_lore in code:
    code = code.replace(old_lore, new_lore)
if old_rep in code:
    code = code.replace(old_rep, new_rep)

code = code.replace('_ironclad.faction_id = "faction_terran";', '_ironclad.faction_id = "player";')

with open(bpm_path, "w") as f:
    f.write(code)

print("Updated obj_BlueprintManager ironclad lore to Project Prometheus.")

# Update JSON files
for jpath in ["datafiles/bp_ms_ironclad_07.json", "datafiles/blueprints/bp_ms_ironclad_07.json"]:
    with open(jpath, "r") as f:
        data = json.load(f)
    data["description"] = "PROJECT PROMETHEUS (Unit-01 Prototype): The world's first operational bipedal Mobile Suit, secretly engineered inside our mobile Dreadnought Foundry. Combines compact thermonuclear Tokamak power with neural-link hydraulic bipedal locomotion, rendering conventional tracked armor obsolete."
    data["manufacturer"] = "Iron Ridge Dynamics (Vanguard Foundry)"
    if "combat_stats" in data:
        data["combat_stats"]["battlefield_reputation"] = "The Walking God of War: impervious to conventional tank shells, leaps trenches and crushes armor in melee."
    with open(jpath, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Updated {jpath} with Prometheus lore.")
