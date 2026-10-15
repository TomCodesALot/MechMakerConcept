with open('objects/obj_GameManager/Create_0.gml', 'r') as f:
    content = f.read()

target = '''                var _mp = _fm.mass_production_contracts[$ _fid];
                if (_mp.replaced) {
                    var _royalty = _mp.royalty_per_turn;
                    funds += _royalty;
                    _mp.cumulative_royalties_paid += _royalty;
                    array_push(last_turn_events, "* Mass-Production Royalty (" + _mp.faction_name + "): +" + string(_royalty) + " Cr for licensed " + _mp.replacement_name + " lines.");
                }'''

replacement = '''                var _mp = _fm.mass_production_contracts[$ _fid];
                if (_mp.replaced) {
                    var _stage = _mp[$ "adoption_stage"] ?? "MATURE";
                    if (_stage == "TOOLING") {
                        _mp.tooling_turns_remaining = max(0, (_mp[$ "tooling_turns_remaining"] ?? 2) - 1);
                        if (_mp.tooling_turns_remaining == 0) {
                            _mp.adoption_stage = "ROLLOUT";
                            _mp.active_frontline_units = 50;
                            array_push(last_turn_events, "! DOCTRINE ROLLOUT: " + _mp.faction_name + " finished shipyard tooling! 50 " + _mp.replacement_name + " units deployed to front lines!");
                        } else {
                            array_push(last_turn_events, "* Factory Tooling (" + _mp.faction_name + "): " + string(_mp.tooling_turns_remaining) + " turn(s) remaining for " + _mp.replacement_name + " lines.");
                        }
                    } else {
                        _mp.active_frontline_units = min(250, (_mp[$ "active_frontline_units"] ?? 50) + irandom_range(12, 22));
                        var _unit_multiplier = max(1.0, _mp.active_frontline_units / 50.0);
                        var _royalty = round(_mp.royalty_per_turn * _unit_multiplier);
                        funds += _royalty;
                        _mp.cumulative_royalties_paid = (_mp[$ "cumulative_royalties_paid"] ?? 0) + _royalty;
                        array_push(last_turn_events, "* Mass-Production Royalty (" + _mp.faction_name + "): +" + string(_royalty) + " Cr (" + string(_mp.active_frontline_units) + " active units in service).");
                    }
                }'''

if target in content:
    content = content.replace(target, replacement)
    with open('objects/obj_GameManager/Create_0.gml', 'w') as f:
        f.write(content)
    print("Updated obj_GameManager/Create_0.gml with adoption lifecycle turn handling")
else:
    print("ERROR: Target block not found in obj_GameManager/Create_0.gml")
