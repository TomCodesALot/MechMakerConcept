with open('objects/obj_HQTerminal/Create_0.gml', 'r') as f:
    content = f.read()

target = '''trial_last_result = undefined;
trade_selected_faction = "faction_a";'''

replacement = '''trial_last_result = undefined;
trial_phase = 0;              // 0 = Hangar Selection, 1 = Static Audit, 2 = Stress Gauntlet, 3 = Combat Fly-Off, 4 = Final Board Ratification
trial_refinements = [];       // Array of emergency field refinements applied during active trial
trial_phase_results = undefined; // Phase result struct
trial_view_adoption_panel = false; // Toggle to view adopted fleet management vs new trial
trade_selected_faction = "faction_a";'''

if target in content:
    content = content.replace(target, replacement)
    with open('objects/obj_HQTerminal/Create_0.gml', 'w') as f:
        f.write(content)
    print("Updated obj_HQTerminal/Create_0.gml successfully")
else:
    print("ERROR: Target not found in obj_HQTerminal/Create_0.gml")
