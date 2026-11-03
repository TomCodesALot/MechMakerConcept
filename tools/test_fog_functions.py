def hex_dist(c1, r1, c2, r2):
    x1, z1 = c1, r1 - ((c1 - (c1 & 1)) // 2)
    y1 = -x1 - z1
    x2, z2 = c2, r2 - ((c2 - (c2 & 1)) // 2)
    y2 = -x2 - z2
    return (abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)) // 2

def init_fog():
    return [[0 for _ in range(10)] for _ in range(16)]

def update_fog(fog_grid, units, terrain):
    # Demote visible to fog
    for c in range(16):
        for r in range(10):
            if fog_grid[c][r] == 2:
                fog_grid[c][r] = 1

    # Units sensor sweep
    spotted = []
    for u in units:
        if u["faction"] == "pmc" and u["hp"] > 0:
            sr = u.get("sensor_range", 2)
            for c in range(16):
                for r in range(10):
                    if hex_dist(u["col"], u["row"], c, r) <= sr:
                        fog_grid[c][r] = 2

    # Check newly revealed OPFOR
    for u in units:
        if u["faction"] != "pmc" and u["hp"] > 0:
            if fog_grid[u["col"]][u["row"]] == 2:
                spotted.append(u["unit_label"])

    return spotted

fog = init_fog()
test_units = [
    {"faction": "pmc", "hp": 100, "col": 2, "row": 4, "sensor_range": 2, "unit_label": "Ironclad"},
    {"faction": "pmc", "hp": 60, "col": 4, "row": 5, "sensor_range": 4, "unit_label": "Scout"},
    {"faction": "enemy", "hp": 70, "col": 6, "row": 5, "sensor_range": 2, "unit_label": "Enemy Rover"},
    {"faction": "enemy", "hp": 90, "col": 12, "row": 4, "sensor_range": 2, "unit_label": "Enemy Cmd"}
]

spotted = update_fog(fog, test_units, None)
print("Spotted enemies:", spotted)
assert "Enemy Rover" in spotted, "Enemy Rover at (6, 5) should be spotted by Scout at (4, 5) with sensor 4"
assert "Enemy Cmd" not in spotted, "Enemy Cmd at (12, 4) should remain hidden in deep Prometheus Flux fog"

print("Enemy Rover visibility:", fog[6][5], "(2 = VISIBLE)")
print("Enemy Cmd visibility:", fog[12][4], "(0 = UNEXPLORED)")
print("Fog of war calculations tested successfully!")
