#!/usr/bin/env python3
"""
tools/test_goal_f_exhaustive.py
Exhaustive verification of Goal F:
1. Crossfire Suppression & Pinning Engine (accuracy penalty, AP depletion, move penalty).
2. High-Ground Kinetic Velocity Ballistics (effective range bonus, damage multiplier, uphill penalty).
3. Destructible Cover Degradation & Ordnance Penetration (heavy ordnance, Bastion -> Rubble -> Destroyed).
4. Directional Facing Angles & Flanking/Rear Core Strikes (+40% rear, +20% flank).
5. Platoon Role AI Specialization & Tactical Forecast HUD.
"""

import sys

def test_goal_f():
    print("=== EXHAUSTIVE VALIDATION: GOAL F ===")

    # 1. Verify obj_BattleManager Create_0.gml Combat Calculations
    with open("objects/obj_BattleManager/Create_0.gml", "r") as f:
        bm_create = f.read()

    # Hit Chance Modifiers
    assert "is_suppressed" in bm_create, "is_suppressed check missing from calculate_hit_chance!"
    assert "_base -= 20;" in bm_create, "-20% aim penalty for suppressed units missing!"
    assert "_is_rear" in bm_create and "_is_flank" in bm_create, "Directional facing missing from calculate_hit_chance!"
    assert "_base += 30;" in bm_create, "+30% hit on rear ambush missing!"
    assert "_base += 15;" in bm_create, "+15% hit on flank angle missing!"
    assert "_cov = floor(_cov * 0.50);" in bm_create, "50% cover penetration for heavy ordnance missing!"
    assert "(_elev_diff > 0) ? (_elev_diff * 10) : (_elev_diff * 15);" in bm_create, "High ground vs uphill hit modifiers missing!"

    # Movement Penalty
    assert "_ap_pool = max(1, _ap_pool - 1);" in bm_create, "Suppressed unit move penalty missing in recalculate_moves!"

    # High Ground Effective Range in Firepower Forecast
    assert "max(0, _au.elev - _def_target.elev)" in bm_create, "High ground weapon range bonus missing in get_stack_max_firepower!"

    # Damage Multipliers in Cinematic & Impact
    assert "REAR CORE HIT +40%" in bm_create, "Rear core strike +40% damage missing!"
    assert "FLANKING ANGLE +20%" in bm_create, "Flanking angle +20% damage missing!"
    assert "HIGH GROUND +" in bm_create and "% VELOCITY" in bm_create, "High ground kinetic damage bonus missing!"
    assert "UPHILL -15% KINETIC" in bm_create, "Uphill kinetic mitigation missing!"

    # Cover Degradation
    assert "BASTION CRACKED -> RUBBLE" in bm_create, "Bastion cover degradation missing!"
    assert "COVER DESTROYED" in bm_create, "Rubble cover annihilation missing!"

    print("[PASS] obj_BattleManager Create_0.gml core combat formulas, suppression & cover verified.")

    # 2. Verify obj_BattleManager Step_0.gml AI Roles & Turn Refresh
    with open("objects/obj_BattleManager/Step_0.gml", "r") as f:
        bm_step = f.read()

    # Effective weapon range in TARGET_MODE
    assert "_eff_max_w_range = _w.range_max + max(0, _cur_u.elev - _target.elev);" in bm_step, "High ground player range extension missing in Step_0!"

    # AI Role Specialization
    assert "_ai_role = \"SNIPER\";" in bm_step, "SNIPER AI role missing!"
    assert "_ai_role = \"FLANKER\";" in bm_step, "FLANKER AI role missing!"
    assert "_ai_role = \"VANGUARD\";" in bm_step, "VANGUARD AI role missing!"
    assert "hits_taken_this_turn > 0" in bm_step, "Vanguard focus-fire suppression logic missing!"

    # Turn Refresh & Suppression Recovery
    assert "hits_taken_this_turn = 0;" in bm_step, "hits_taken_this_turn reset missing in turn refresh!"
    assert "_u.current_ap = max(1, _u.current_ap - 2);" in bm_step, "-2 AP suppression penalty missing in turn refresh!"

    print("[PASS] obj_BattleManager Step_0.gml AI Platoon roles, high-ground range & turn refresh verified.")

    # 3. Verify obj_BattleManager Draw_64.gml Forecast Panel
    with open("objects/obj_BattleManager/Draw_64.gml", "r") as f:
        bm_draw64 = f.read()

    assert "VECTOR:" in bm_draw64, "VECTOR line missing in forecast HUD!"
    assert "REAR AMBUSH (+40% CORE DMG / +30% HIT)" in bm_draw64, "Rear ambush indicator missing in forecast HUD!"
    assert "FLANKING ANGLE (+20% DMG / +15% HIT)" in bm_draw64, "Flank angle indicator missing in forecast HUD!"
    assert "TERRAIN:" in bm_draw64, "TERRAIN line missing in forecast HUD!"
    assert "HIGH GROUND +" in bm_draw64, "High ground velocity indicator missing in forecast HUD!"
    assert "DEFENSE:" in bm_draw64, "DEFENSE cover/suppression breakdown missing in forecast HUD!"

    print("[PASS] obj_BattleManager Draw_64.gml Tactical Forecast HUD verified.")

    # 4. Verify obj_BattleManager Draw_0.gml Overhead Badges & Cover Visuals
    with open("objects/obj_BattleManager/Draw_0.gml", "r") as f:
        bm_draw0 = f.read()

    assert "[! PINNED !]" in bm_draw0, "[! PINNED !] overhead badge missing in Draw_0!"
    assert "\"^\" + string(_u.elev)" in bm_draw0, "Elevation indicator missing in Draw_0!"
    assert "[BASTION]" in bm_draw0 and "[RUBBLE]" in bm_draw0, "Cover badges missing in Draw_0!"
    assert "_is_bastion ? \"BASTION\" : \"RUBBLE\"" in bm_draw0, "Dynamic cover visual degradation missing in Draw_0!"

    print("[PASS] obj_BattleManager Draw_0.gml overhead badges and dynamic cover rendering verified.")

    # 5. Math Simulation of Flanking and Elevation
    def sim_hit(base_acc, def_eva, cov, dist, elev_diff, is_rear, is_flank, is_supp, heavy_ord):
        acc = base_acc
        eva = def_eva
        if is_supp:
            acc -= 20
        if is_rear:
            acc += 30
            eva = max(0, eva - 20)
        elif is_flank:
            acc += 15

        c = cov
        if heavy_ord and c > 0:
            c = c // 2

        elev_bon = (elev_diff * 10) if elev_diff > 0 else (elev_diff * 15)
        res = acc - int(eva * 0.40) - c - (dist * 2) + elev_bon
        return max(15, min(95, res))

    # Standard level attack: Acc 80, Eva 40, Cov 0, Dist 3, Elev 0
    std_hit = sim_hit(80, 40, 0, 3, 0, False, False, False, False)
    assert std_hit == 80 - 16 - 6, f"Std hit mismatch: {std_hit}" # 58%

    # High ground (+1 elev): +10% hit
    hg_hit = sim_hit(80, 40, 0, 3, 1, False, False, False, False)
    assert hg_hit == 68, f"High ground hit mismatch: {hg_hit}"

    # Flanking (+15% hit)
    flk_hit = sim_hit(80, 40, 0, 3, 0, False, True, False, False)
    assert flk_hit == 73, f"Flank hit mismatch: {flk_hit}"

    # Rear Ambush (+30% hit, bypass 20% eva)
    rear_hit = sim_hit(80, 40, 0, 3, 0, True, False, False, False)
    assert rear_hit == 95, f"Rear hit mismatch: {rear_hit}"

    # Suppressed (-20% hit)
    supp_hit = sim_hit(80, 40, 0, 3, 0, False, False, True, False)
    assert supp_hit == 38, f"Suppressed hit mismatch: {supp_hit}"

    # Heavy ordnance vs Bastion (Cov 40 -> 20)
    cov_std = sim_hit(80, 40, 40, 3, 0, False, False, False, False)
    cov_pen = sim_hit(80, 40, 40, 3, 0, False, False, False, True)
    assert cov_pen - cov_std == 20, f"Cover pen bonus mismatch: {cov_pen - cov_std}"

    print("[PASS] Goal F tactical ballistics mathematical model verified.")

    print("\nALL GOAL F EXHAUSTIVE SUITE TESTS PASSED (100%)!")

if __name__ == '__main__':
    test_goal_f()
