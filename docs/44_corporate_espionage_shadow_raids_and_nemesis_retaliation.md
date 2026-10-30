# DOCS 44: CORPORATE ESPIONAGE, SHADOW RAIDS & NEMESIS RETALIATION

## 1. Overview & System Objectives
This document establishes the architecture, mathematical formulations, and UI/UX flows implemented for **Goal E**:
1. **Corporate Retaliation & Espionage Engine**: Dynamic reactions from rival megacorps (`corp_vhi`, `corp_aod`, `corp_rust`, `corp_hats`) when the player acquires equity ($\ge 10\%, \ge 25\%, \ge 51\%$), captures strategic territory, replaces their mass-production lines, or exceeds threshold wealth ($\ge 500,000$ Cr).
2. **Black-Ops Shadow Raids**: Covert corsair/strike-team attacks targeting active player mining nodes with designated corporate sponsors and Nemesis Ace commanders; auto-resolve and manual defense with Black Box Eureka rewards and Nemesis capture.
3. **Pilot Poaching & Counter-Bribery**: Headhunters targeting fatigued/hospitalized pilots; interactive dispatch modal offering:
   - **Counter-Offer Retention Bonus** (-Cr, zeroes fatigue, +XP)
   - **Flagship SIGINT Security Sweep** (arrests handler into brig, gains $+1,500$ shares, $+45,000$ Cr)
   - **Refusal** (50% risk of pilot defection to rival megacorp)
4. **Nemesis Ace Bounties & Combat Triage**: Incursions in tactical combat where destroying a Nemesis Ace incarcerates the pilot into `obj_NemesisManager.prisoner_list`, grants $+1$ Black Box Eureka intel, removes them from active nemeses, and awards $+150,000$ Cr bounty.
5. **Base Detention Brig & Nemesis Radar UI**: In `obj_HQTerminal` (`flagship_subtab == 2`), an interactive view mode to inspect active Nemesis contracts and manage brig prisoners with **[INTERROGATE]** (+2,000 shares, +125k Cr), **[RANSOM: +250k]** (+250k Cr, -15 tension), and **[RECRUIT ACE]** actions.

---

## 2. Pillar I: Megacorp Encroachment & Tension Engine

### 2.1 Corporate Tension Calculation
At the conclusion of every turn, `obj_NemesisManager.evaluate_corporate_espionage_turn()` measures corporate threat and hostility across all four rival conglomerates:
$$\text{Tension}_{\text{Corp}} = \text{Tension}_{\text{Equity}} + \text{Tension}_{\text{Market}} + \text{Tension}_{\text{Treasury}}$$

Where:
- **Equity Stake Encroachment**:
  - Player Equity $\ge 51.0\%$ (Hostile Majority Takeover Threat): $+65\text{ Tension}$
  - Player Equity $\ge 25.0\%$ (Significant Voting Stake): $+40\text{ Tension}$
  - Player Equity $\ge 10.0\%$ (Initial Foothold): $+20\text{ Tension}$
- **Market Dominance / Line Replacement**:
  - Replaced megacorp mass-production line: $+35\text{ Tension}$
- **Liquid Treasury Threat**:
  - Player Cash Reserves $\ge 500,000\text{ Cr}$: $+15\text{ Tension}$

### 2.2 Retaliation Trigger Conditions
When $\text{Tension}_{\text{Corp}} \ge 35$, the megacorp triggers covert retaliation operations on a staggered 3-turn operational cycle (`_gm.current_turn % 3 == ci % 3`):
- **Operation 1 (Roll $< 35\%$): Pilot Poaching Breach**: Targets the highest fatigue or hospitalized pilot in the PMC roster with an illicit signing bonus and defection contract.
- **Operation 2 (Roll $35\% - 75\%$): Black-Ops Shadow Raid**: Launches an unflagged strike team targeting an active mining node, sponsored by the megacorp and led by a Nemesis Ace.
- **Operation 3 (Roll $\ge 75\%$): Nemesis Ace Hit Contract**: Issues a corporate bounty contract to an elite enemy pilot to track and eliminate Iron Ridge forces.

---

## 3. Pillar II: Corporate Black-Ops Shadow Raids

### 3.1 Raid Generation & Dispatch
When a shadow raid triggers:
- Target: A randomly selected mining node currently marked as `ACTIVE_MINING`.
- Sponsor: Megacorp ID and formal company name (`corp_vhi`, `corp_aod`, `corp_rust`, or `corp_hats`).
- Commander: An ace candidate drawn from the corporation's affiliated roster (e.g. Cole, Claire Vance, Cassian, Sorren, Jackal, Cruz, Null-07, Takahashi).
- The event generates a `pending_raid` payload:
```gml
_gm.pending_raid = {
    node_index: _target_node_idx,
    node_name: _node.name,
    assigned_mech: _node.assigned_mech_id,
    assigned_pilot: _node.assigned_pilot_name,
    raid_type: "CORPORATE_SHADOW_RAID",
    sponsor_corp: _corp.id,
    sponsor_name: _corp.name,
    nemesis_pilot_id: _nemesis_candidate
};
```

### 3.2 Defense & Resolution
In the **Node Raid Modal** (`obj_HQTerminal`):
- **Corporate Shadow Raid Banner**: Distinctive warning banner indicating foreign corporate deniable operations.
- **Auto-Resolve Defense**:
  - On Victory: Repulses the raiders, arrests the Nemesis commander into the base detention brig, removes them from active nemeses, awards $+1$ Black Box Eureka intel (`scr_research_award_salvage_intel(choose("WEAPONS", "REACTORS", "SHIELDS", "UPGRADES"), 0.50)`), and awards $+50,000$ Cr counter-bounty.
  - On Defeat: Node stockpiles looted and mining operations interrupted.
- **Manual Tactical Sortie**: Player deploys combat lance into tactical grid combat against the raiders.

---

## 4. Pillar III: Pilot Poaching & Counter-Bribery

### 4.1 Vulnerability Targeting
Corporate headhunters scan PMC telemetry, specifically seeking pilots experiencing battle fatigue or recovering from injuries in convalescence:
- Target Score = $\text{Fatigue} + (3 \text{ if Hospitalized})$.
- Generates `pending_poaching_offer` on `obj_GameManager`.

### 4.2 Countermeasures & Choices
When approached, the Commander is presented with three distinct operational responses via the **Corporate Poaching Dispatch Modal**:
1. **[1. MATCH WITH LOYALTY RETENTION BONUS]**:
   - Cost: $-(\text{Counter Cost Cr})$
   - Result: Pilot fatigue instantly set to 0, $+150$ Pilot XP awarded, pilot loyalty permanently secured.
2. **[2. EXECUTE FLAGSHIP SIGINT SECURITY SWEEP]**:
   - Success Probability: $60\% + (\text{SIGINT Tier} \times 10\%)$, or $100\%$ with `Shadow Panopticon` flagship protocol.
   - On Success: Corporate handler arrested into the Base Detention Brig, player seizes $+1,500$ equity shares in the hiring megacorp ($+1.5\%$), awards $+45,000$ Cr extracted intelligence slush funds, and pilot fatigue reduced by 1.
   - On Failure: Handler escapes before arrest, but recruitment channel is shut down.
3. **[3. REFUSE MATCH // RISK PILOT DEFECTION]**:
   - $50\%$ chance the pilot defects: immediately removed from `facilities.roster_pilots`, lost to the PMC.
   - $50\%$ chance the pilot remains: stays out of loyalty, fatigue reduced.

---

## 5. Pillar IV: Tactical Combat Incarceration & Nemesis Triage

### 5.1 Combat Elimination Hooks
Across all three tactical unit destruction routines in `obj_BattleManager` (Head Destruct, Torso Destruct, and Legs Mobility Kill):
```gml
if (variable_struct_get(_def, "is_nemesis") == true || string_pos("NEMESIS_", _def.id) > 0) {
    obj_NemesisManager.add_prisoner(_vic_id, incursion_data.nemesis_name, incursion_data.faction_id);
    for (var nem_i = array_length(obj_NemesisManager.active_nemeses) - 1; nem_i >= 0; nem_i--) {
        if (obj_NemesisManager.active_nemeses[nem_i].pilot_id == _vic_id) {
            array_delete(obj_NemesisManager.active_nemeses, nem_i, 1);
        }
    }
    var _eureka_msg = scr_research_award_salvage_intel(choose("WEAPONS", "REACTORS", "SHIELDS", "UPGRADES"), 0.50);
    if (_eureka_msg != "") add_log("[EUREKA] " + _eureka_msg);
    add_log("[NEMESIS DOWN] " + _def.callsign + " disabled! Pilot captured and Black Box Eureka recovered!");
    if (instance_exists(obj_GameManager)) {
        obj_GameManager.funds += 150000;
    }
    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("NEMESIS ACE CAPTURED! +1 Eureka Intel & +150,000 Cr Bounty!", c_lime);
    }
}
```

---

## 6. Pillar V: Base Detention Brig & Nemesis Radar UI

### 6.1 View Mode Toggle & Dual Terminal Panes
Located in `obj_HQTerminal` (`flagship_subtab == 2`):
- Header toggle allows instantaneous switching between:
  - `[<< CORPORATE STOCK EXCHANGE]`
  - `[BASE DETENTION BRIG & NEMESIS RADAR >>]`
- **Active Nemesis Radar**:
  - Displays all active corporate contracts targeting Iron Ridge PMC.
  - Lists bounty issuer, target allied pilot, threat level, and tracking status.
- **PMC Maximum Security Detention Brig**:
  - Lists up to 4 captive prisoners simultaneously with individual dossiers (Name, Callsign, Sponsoring Megacorp, Role).

### 6.2 Prisoner Management Actions
Each prisoner cell offers three interactive operational decisions:
| Action | Mechanics & Costs | Output Rewards |
| :--- | :--- | :--- |
| **[INTERROGATE]** | Intelligence extraction through Flagship SIGINT & base inquisitors | $+2,000$ Corporate Shares ($+2\%$), $+125,000\text{ Cr}$, captive released/deported |
| **[RANSOM: +250k]** | Diplomatic exchange back to originating megacorp | $+250,000\text{ Cr}$, Corporate Tension reduced by $-15$, captive returned |
| **[RECRUIT ACE]** | Rehabilitation, re-indoctrination, and PMC commission | Transferred directly into `facilities.roster_pilots` with full stats, 0 fatigue, hospital cleared |

---

## 7. Verification & Automated Test Suite Metrics
The entire Goal E system is validated by `tools/test_goal_e_exhaustive.py`:
- `obj_NemesisManager` Corporate Espionage, Tension & Brig Methods: **PASSED (100%)**
- `obj_GameManager` Poaching Resolution Engine & Strategic Turn Hook: **PASSED (100%)**
- `obj_BattleManager` Nemesis Combat Incarceration, Bounty & Eureka: **PASSED (100%)**
- `obj_HQTerminal` Brig UI, Nemesis Radar, Poaching Modal, and Shadow Raid: **PASSED (100%)**
- Full Project Syntax and Lint Validation (`tools/validate_project.py`): **0 ERRORS**
- Full Backward Regression Suite (Goals A, B, C, D, Tech Tree, HOI4 System): **PASSED (100%)**
