# Dynamic simulation of HoI4 Research Tree state machine
print("=== SIMULATING HOI4 RESEARCH PROGRESSION ===")

# Simulated Game State
funds = 100000
unlocked_techs = {
    "tech_wpn_heavy_autocannon": True,
    "tech_wpn_hydra_rockets": True,
    "tech_wpn_vibro_blade": True,
    "tech_rea_gas_cooled_fission": True,
    "tech_sld_ballistic_buckler": True,
    "tech_upg_analog_hydraulics": True
}
slots = [
    {"id": 0, "status": "EMPTY", "tech_id": "", "progress_turns": 0, "total_turns": 0},
    {"id": 1, "status": "EMPTY", "tech_id": "", "progress_turns": 0, "total_turns": 0},
    {"id": 2, "status": "EMPTY", "tech_id": "", "progress_turns": 0, "total_turns": 0}
]
max_slots = 3

techs = {
    "tech_wpn_hyper_velocity_rifle": {"turns": 3, "cost": 6000, "prereqs": ["tech_wpn_heavy_autocannon"]},
    "tech_rea_compact_fusion": {"turns": 3, "cost": 8000, "prereqs": ["tech_rea_gas_cooled_fission"]},
    "tech_wpn_beam_carbine": {"turns": 4, "cost": 12000, "prereqs": ["tech_wpn_hyper_velocity_rifle", "tech_rea_compact_fusion"]},
    "tech_upg_research_expansion_1": {"turns": 3, "cost": 10000, "prereqs": []},
    "tech_upg_research_expansion_2": {"turns": 5, "cost": 25000, "prereqs": ["tech_upg_research_expansion_1"]}
}

def can_research(tid):
    if tid in unlocked_techs: return False
    for s in slots:
        if s["tech_id"] == tid: return False
    for p in techs[tid]["prereqs"]:
        if p not in unlocked_techs: return False
    return True

def start_research(tid, slot_idx):
    global funds
    assert can_research(tid), f"Cannot research {tid}"
    cost = techs[tid]["cost"]
    assert funds >= cost, "Not enough funds"
    funds -= cost
    slots[slot_idx]["status"] = "RESEARCHING"
    slots[slot_idx]["tech_id"] = tid
    slots[slot_idx]["progress_turns"] = 0
    slots[slot_idx]["total_turns"] = techs[tid]["turns"]
    print(f" -> Assigned [{tid}] to Slot #{slot_idx + 1} (Cost: {cost} Cr, Turns: {techs[tid]['turns']})")

def advance_turn():
    global max_slots
    print(" >> Advancing strategic turn...")
    for s in slots:
        if s["status"] == "RESEARCHING":
            s["progress_turns"] += 1
            print(f"    Slot #{s['id']+1} [{s['tech_id']}]: Turn {s['progress_turns']}/{s['total_turns']}")
            if s["progress_turns"] >= s["total_turns"]:
                tid = s["tech_id"]
                unlocked_techs[tid] = True
                s["status"] = "EMPTY"
                s["tech_id"] = ""
                s["progress_turns"] = 0
                s["total_turns"] = 0
                print(f" ★ BREAKTHROUGH: [{tid}] RESEARCH COMPLETE!")
                if tid == "tech_upg_research_expansion_1":
                    max_slots = 4
                    slots.append({"id": 3, "status": "EMPTY", "tech_id": "", "progress_turns": 0, "total_turns": 0})
                    print("   *** 4TH RESEARCH SLOT ACTIVATED ***")
                elif tid == "tech_upg_research_expansion_2":
                    max_slots = 5
                    slots.append({"id": 4, "status": "EMPTY", "tech_id": "", "progress_turns": 0, "total_turns": 0})
                    print("   *** 5TH RESEARCH SLOT ACTIVATED ***")

# Step 1: Check prerequisites
assert can_research("tech_wpn_hyper_velocity_rifle") == True
assert can_research("tech_wpn_beam_carbine") == False # Lacks both rifle and fusion!

# Step 2: Queue 3 projects into the 3 slots
start_research("tech_wpn_hyper_velocity_rifle", 0)
start_research("tech_rea_compact_fusion", 1)
start_research("tech_upg_research_expansion_1", 2)

# Step 3: Advance 3 turns
advance_turn()
advance_turn()
advance_turn()

assert "tech_wpn_hyper_velocity_rifle" in unlocked_techs
assert "tech_rea_compact_fusion" in unlocked_techs
assert "tech_upg_research_expansion_1" in unlocked_techs
assert max_slots == 4
assert len(slots) == 4
print("[PASS] 3 Projects completed, 4th research slot unlocked!")

# Step 4: Now tech_wpn_beam_carbine is unlocked for research
assert can_research("tech_wpn_beam_carbine") == True
start_research("tech_wpn_beam_carbine", 0)
start_research("tech_upg_research_expansion_2", 1)

advance_turn()
advance_turn()
advance_turn()
advance_turn()
assert "tech_wpn_beam_carbine" in unlocked_techs
advance_turn()
assert "tech_upg_research_expansion_2" in unlocked_techs
assert max_slots == 5
assert len(slots) == 5
print("[PASS] Particle Beam Rifle unlocked, 5th research slot unlocked!")

print("=== ALL PROGRESSION SIMULATIONS VALIDATED 100% ===")
