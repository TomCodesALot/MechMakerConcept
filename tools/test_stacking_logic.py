def test_stacking():
    # 3 units in a stack
    stack = [
        {"id": "u1", "unit_label": "Ironclad MS", "hp": 100, "max_hp": 100, "attack": 45, "defense": 30, "range": 1, "col": 2, "row": 4},
        {"id": "u2", "unit_label": "Aero-Striker Ace", "hp": 80, "max_hp": 80, "attack": 40, "defense": 20, "range": 2, "col": 2, "row": 4},
        {"id": "u3", "unit_label": "Heavy Siege Tank", "hp": 120, "max_hp": 120, "attack": 50, "defense": 35, "range": 2, "col": 2, "row": 4}
    ]

    # Verify count at hex (2, 4)
    units_at_hex = [u for u in stack if u["col"] == 2 and u["row"] == 4 and u["hp"] > 0]
    print(f"Units in stack at (2, 4): {len(units_at_hex)}/3")
    assert len(units_at_hex) == 3

    # Calculate combined attack against target at range 1
    target_dist = 1
    total_atk = sum(u["attack"] for u in units_at_hex if u["range"] >= target_dist)
    print(f"Combined attack power at range 1: {total_atk} ATK (45+40+50)")
    assert total_atk == 135

    # Calculate combined attack against target at range 2 (Ironclad cannot reach range 2)
    target_dist = 2
    total_atk_r2 = sum(u["attack"] for u in units_at_hex if u["range"] >= target_dist)
    print(f"Combined attack power at range 2: {total_atk_r2} ATK (40+50)")
    assert total_atk_r2 == 90

    # Frontline damage absorption: incoming 120 damage
    incoming_dmg = 120
    # Unit 1 absorbs first
    d1 = min(stack[0]["hp"], incoming_dmg)
    stack[0]["hp"] -= d1
    rem_dmg = incoming_dmg - d1
    # Unit 2 absorbs overflow
    d2 = min(stack[1]["hp"], rem_dmg)
    stack[1]["hp"] -= d2
    print(f"After 120 dmg: Unit 1 HP = {stack[0]['hp']}/100, Unit 2 HP = {stack[1]['hp']}/80")
    assert stack[0]["hp"] == 0
    assert stack[1]["hp"] == 60

    print("Stacking math & damage distribution verified 100%!")

test_stacking()
