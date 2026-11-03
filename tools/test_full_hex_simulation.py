import math

# Simulate scr_hex_get_stronghold_terrain
def get_terrain(stronghold_id):
    grid = [[None for _ in range(10)] for _ in range(16)]
    for c in range(16):
        for r in range(10):
            t_type = "CRATON"
            name = "Basalt Craton"
            mp_cost = 1
            def_bonus = 10
            # Amazon tributary
            if (c == 7 and 1 <= r <= 8) or (c == 6 and 3 <= r <= 5) or (c == 8 and 6 <= r <= 9):
                t_type = "WATER"
                name = "Amazon Tributary"
                mp_cost = 3
                def_bonus = 0
            elif (3 <= c <= 5 and r <= 3) or (11 <= c <= 13 and r >= 7):
                t_type = "FOREST"
                name = "Amazon Canopy"
                mp_cost = 2
                def_bonus = 20
            elif (c <= 2 and r <= 3) or (c >= 13 and r <= 3):
                t_type = "MOUNTAIN"
                name = "Granite Ridge"
                mp_cost = 3
                def_bonus = 35
            grid[c][r] = {
                "terrain_type": t_type,
                "name": name,
                "mp_cost": mp_cost,
                "defense_bonus": def_bonus,
                "facility_id": "",
                "controlling_faction": "neutral"
            }
    # Base facilities
    for fc, fr, fid in [(10, 4, "core"), (6, 2, "north"), (12, 6, "south")]:
        grid[fc][fr]["terrain_type"] = "BASE_FACILITY"
        grid[fc][fr]["name"] = f"Granite {fid.title()}"
        grid[fc][fr]["mp_cost"] = 1
        grid[fc][fr]["defense_bonus"] = 40
        grid[fc][fr]["facility_id"] = fid
    return grid

terrain_grid = get_terrain("earth_granite_redoubt")

def hex_dist(c1, r1, c2, r2):
    x1, z1 = c1, r1 - ((c1 - (c1 & 1)) // 2)
    y1 = -x1 - z1
    x2, z2 = c2, r2 - ((c2 - (c2 & 1)) // 2)
    y2 = -x2 - z2
    return (abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)) // 2

def get_nbrs(c, r):
    if c % 2 == 0:
        raw = [(c, r-1), (c+1, r-1), (c+1, r), (c, r+1), (c-1, r), (c-1, r-1)]
    else:
        raw = [(c, r-1), (c+1, r), (c+1, r+1), (c, r+1), (c-1, r+1), (c-1, r)]
    return [(nc, nr) for nc, nr in raw if 0 <= nc < 16 and 0 <= nr < 10]

import heapq
def get_reachable(unit, units_list, grid):
    reachable = {}
    if unit["current_mp"] <= 0: return reachable
    occ = {(u["col"], u["row"]): u for u in units_list if u["id"] != unit["id"] and u["hp"] > 0}
    dist = {(unit["col"], unit["row"]): 0}
    pq = [(0, unit["col"], unit["row"])]
    while pq:
        d, c, r = heapq.heappop(pq)
        if d > dist[(c, r)]: continue
        for nc, nr in get_nbrs(c, r):
            if (nc, nr) in occ: continue
            step_cost = grid[nc][nr]["mp_cost"]
            new_cost = d + step_cost
            if new_cost <= unit["current_mp"]:
                if (nc, nr) not in dist or new_cost < dist[(nc, nr)]:
                    dist[(nc, nr)] = new_cost
                    reachable[f"{nc}_{nr}"] = new_cost
                    heapq.heappush(pq, (new_cost, nc, nr))
    return reachable

# Create test units
units = [
    {"id": "pmc_ironclad", "name": "Ironclad Vanguard Alpha", "unit_label": "GHA-07 Ironclad", "faction": "pmc", "col": 2, "row": 4, "max_mp": 4, "current_mp": 4, "hp": 100, "max_hp": 100, "attack": 45, "defense": 30, "range": 1, "status": "READY"},
    {"id": "pmc_striker", "name": "Aero-Striker Ace Flight", "unit_label": "F-102 Aero-Striker", "faction": "pmc", "col": 2, "row": 6, "max_mp": 5, "current_mp": 5, "hp": 80, "max_hp": 80, "attack": 40, "defense": 20, "range": 2, "status": "READY"},
    {"id": "opfor_grunt", "name": "Line Mobile Suit", "unit_label": "Standard Grunt MS", "faction": "faction_b", "col": 9, "row": 3, "max_mp": 4, "current_mp": 4, "hp": 90, "max_hp": 90, "attack": 42, "defense": 25, "range": 1, "status": "READY"},
    {"id": "opfor_rover", "name": "Perimeter Technicals", "unit_label": "Armed Scout", "faction": "faction_b", "col": 5, "row": 4, "max_mp": 4, "current_mp": 4, "hp": 70, "max_hp": 70, "attack": 35, "defense": 18, "range": 1, "status": "READY"}
]

print("1. Initial state:")
reach = get_reachable(units[0], units, terrain_grid)
print(f"Ironclad at (2, 4) with 4 MP has {len(reach)} reachable hexes.")
assert "3_4" in reach, "Hex (3, 4) should be reachable"
print("Cost to reach (3, 4):", reach["3_4"], "MP")

print("2. Simulating move to (3, 4):")
cost = reach["3_4"]
units[0]["col"] = 3
units[0]["row"] = 4
units[0]["current_mp"] -= cost
print("New Ironclad MP:", units[0]["current_mp"])
assert units[0]["current_mp"] == 3

print("3. Check attack distance to OPFOR Rover at (5, 4):")
d = hex_dist(units[0]["col"], units[0]["row"], units[3]["col"], units[3]["row"])
print("Hex distance between Ironclad and Rover:", d)

print("All hex calculations passed successfully!")
