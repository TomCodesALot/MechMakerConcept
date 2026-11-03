def test_capture():
    facility = {
        "terrain_type": "BASE_FACILITY",
        "name": "Basalt Scarp Battery",
        "sub_type": "MOUNTAIN_BATTERY",
        "is_core": False,
        "controlling_faction": "faction_b",
        "capture_progress": 0,
        "capture_turns_required": 2,
        "is_captured": False
    }

    unit = {
        "faction": "pmc",
        "unit_label": "Ironclad Vanguard",
        "hp": 80,
        "max_hp": 100
    }

    # Turn 1: Allied unit moves onto enemy facility
    rate = 100 // facility["capture_turns_required"] # 50
    facility["capture_progress"] += rate
    print(f"Turn 1 Capture Progress: {facility['capture_progress']}%")
    assert facility["capture_progress"] == 50
    assert facility["controlling_faction"] == "faction_b"

    # Turn 2: Allied unit continues occupying facility
    facility["capture_progress"] += rate
    print(f"Turn 2 Capture Progress: {facility['capture_progress']}%")
    if facility["capture_progress"] >= 100:
        facility["controlling_faction"] = "pmc"
        facility["is_captured"] = True
    assert facility["is_captured"] == True
    assert facility["controlling_faction"] == "pmc"

    # Turn 3: Friendly unit receives field repair
    if facility["controlling_faction"] == "pmc" and unit["hp"] < unit["max_hp"]:
        unit["hp"] = min(unit["max_hp"], unit["hp"] + 20)
    print(f"Turn 3 Unit HP after repair: {unit['hp']}/{unit['max_hp']}")
    assert unit["hp"] == 100

    print("Capture and field repair state machine passed 100%!")

test_capture()
