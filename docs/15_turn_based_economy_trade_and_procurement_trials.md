# 15. Turn-Based Economy, Interstellar Trade & Faction Procurement Trials
**Document Version:** 1.0.0  
**Role:** Lead Game Designer & Systems Architect  
**Target Engine:** GameMaker Studio 2 (Modern GML)

---

## 1. Executive Summary & Gameplay Loop

The strategic heart of *MechMaker* empowers the player as an independent private military and industrial contractor. Rather than merely piloting mechs, the player directs the military-industrial complex of the solar system through a four-phase closed gameplay loop:

$$\text{Mine / Trade Minerals} \longrightarrow \text{Synthesize Alloys} \longrightarrow \text{Forge Modular Parts} \longrightarrow \text{Assemble Mobile Suits} \longrightarrow \text{Procurement Trials (Fly-Offs)}$$

If the player wins the procurement fly-off against a faction's incumbent flagship suit, **that faction officially adopts the player's custom mobile suit as their new Mass-Production standard**. This permanently replaces their frontline military doctrine, alters the balance of the solar war, and generates massive recurring per-turn royalties for the player.

---

## 2. Turn-Based Economic Cashflow Engine

Every strategic turn represents one operational cycle day. The cashflow ledger is resolved at the end of each turn according to the formula:

$$\Delta \text{Funds} = \text{Base Retainer} + \text{Sovereign Tribute} + \sum \text{Faction Royalties} - \sum \text{Salaries} - \text{Facility Maintenance}$$

### 2.1 Ledger Line Items
1. **Base Mercenary Guild Retainer:** +650 Cr/turn standard operational subsidy.
2. **Sovereign Territory Tribute:** $+3,500 \text{ Cr} \times \text{PMC Sovereign Territory}\%$.
3. **Mass-Production Licensing Royalties:** Each faction whose doctrine has been replaced pays a recurring per-turn royalty:
   - **The Terran Coalition:** +45,000 Cr / turn
   - **The Outer Colonies:** +52,000 Cr / turn
   - **Rogue Mercenary Syndicates:** +38,000 Cr / turn
   - **Apex Bio-Cybernetics Zaibatsu:** +58,000 Cr / turn
   *(Supplying all 4 factions yields +193,000 Cr per turn in passive royalties!)*
4. **Payroll & Upkeep:**
   - Active pilot salaries: 170 to 320 Cr / day per pilot.
   - Lead engineer salaries: 160 to 180 Cr / day per engineer.
   - Facility maintenance: $150 + 75 \times (\text{Assembly Lines} - 1)$ Cr / day.

---

## 3. Interstellar Faction Trade Exchange

The player can engage in bidirectional trade across all four major factions. Each faction maintains dynamic market multipliers based on ideological doctrine and resource scarcity:

| Faction | Favored Commodities (High Sell Payout) | Abundant Commodities (Discounted Buy) | Tariff / Standing Modifiers |
| :--- | :--- | :--- | :--- |
| **Terran Coalition** | Tungsten (`mat_tungsten`), Vanguard Alloy, Heavy Kinetic Parts | Synthetic Flux, Industrial Steels | Standing > 30: -15% Buy / +15% Sell<br>Standing < 0: +25% Tariff |
| **Outer Colonies** | Tritium (`mat_tritium`), Hyperion Matrix, Vernier Thrusters | Silica-Carbon, Refined Propellants | Standing > 30: -15% Buy / +15% Sell<br>Standing < 0: +25% Tariff |
| **Rogue Syndicates** | Weapons, Munitions, Rare Alloys (`alloy_adamantine_carbide`) | Synthetic Flux (`mat_syn_flux`), Scrap Slag | Always charges flat 5% broker fee |
| **Apex Zaibatsu** | Aerosteel (`alloy_aerosteel_flux`), Target Heads, Advanced Cores | Superconductors, Bio-Synthetics | Standing > 30: -20% Buy / +20% Sell<br>Standing < 0: +30% Tariff |

### 3.1 Diplomatic Ripple Effect (Arms Dealing)
Trade in heavy munitions and high-grade alloys carries geopolitical consequence:
- Selling large volumes or supplying weapons to **The Terran Coalition** causes diplomatic tension with **The Outer Colonies** ($\Delta \text{Standing} = -15$) and **The Syndicates** ($\Delta \text{Standing} = -5$).
- Selling to **The Outer Colonies** alarms **The Terran Coalition** ($\Delta \text{Standing} = -20$).
- Selling to **The Rogue Syndicates** risks technology leaks and causes mild scrutiny from Terran and Zaibatsu authorities ($\Delta \text{Standing} = -10$).

---

## 4. Faction Procurement Trials (The Competitive Fly-Off)

### 4.1 Incumbent Flagship Suits
To win a procurement contract, the player's custom mobile suit must undergo a rigorous 4-phase benchmark fly-off against the faction's active incumbent model:

1. **Terran Coalition Incumbent:** `GHA-07 Ironclad`
   - *Archetype:* Heavy Trench Assault
   - *Baseline Stats:* Armor 850, Power Output 12 MW surplus, Speed 45 km/h, Combat Rating 480
   - *Doctrine Focus:* Durability & Ballistic Firepower (Weight: Armor 40%, Combat 35%, Speed 10%, Power 15%)
2. **Outer Colonies Incumbent:** `AET-01 Aether`
   - *Archetype:* Space Interceptor & Energy Striker
   - *Baseline Stats:* Armor 640, Power Output 16 MW surplus, Speed 120 km/h, Combat Rating 510
   - *Doctrine Focus:* Agility & Energy Surplus (Weight: Speed 40%, Power 30%, Combat 20%, Armor 10%)
3. **Rogue Syndicates Incumbent:** `SCR-12 Hyena`
   - *Archetype:* Raider Skirmisher
   - *Baseline Stats:* Armor 720, Power Output 10 MW surplus, Speed 75 km/h, Combat Rating 440
   - *Doctrine Focus:* Cost Efficiency & Mass to Firepower (Weight: Combat 35%, Speed 25%, Armor 25%, Power 15%)
4. **Apex Zaibatsu Incumbent:** `ZAI-03 Muramasa`
   - *Archetype:* High-Spec Cyber-Striker
   - *Baseline Stats:* Armor 780, Power Output 18 MW surplus, Speed 95 km/h, Combat Rating 560
   - *Doctrine Focus:* Balanced Technological Superiority (Weight: Combat 30%, Power 25%, Speed 25%, Armor 20%)

### 4.2 The 4 Fly-Off Evaluation Trials
During the procurement trial, the faction evaluation board runs 4 automated diagnostic trials:

1. **Trial 1: Ballistic & Hull Stress Test:**
   $$\text{Score}_1 = \text{clamp}\left(\frac{\text{Candidate Armor}}{\text{Incumbent Armor}} \times 100, 20, 150\right)$$
2. **Trial 2: Reactor Output & Thermal Sustained Test:**
   $$\text{Score}_2 = \text{clamp}\left(\frac{\text{Candidate Power Surplus}}{\text{Incumbent Power Surplus}} \times 100, 20, 150\right)$$
3. **Trial 3: High-G Mobility & Vernier Dash Test:**
   $$\text{Score}_3 = \text{clamp}\left(\frac{\text{Candidate Speed}}{\text{Incumbent Speed}} \times 100, 20, 150\right)$$
4. **Trial 4: Live-Fire Combat Simulation & Firepower Index:**
   $$\text{Score}_4 = \text{clamp}\left(\frac{\text{Candidate Combat Rating}}{\text{Incumbent Combat Rating}} \times 100, 20, 150\right)$$

### 4.3 Composite Score & Winning Threshold
The overall score is calculated as a weighted sum based on the faction's doctrine weights, plus a reputation adjustment:
$$\text{Final Score} = \sum_{i=1}^4 (w_i \times \text{Score}_i) + \left(\frac{\text{Faction Standing}}{5}\right)$$

- **Threshold for Victory:** $\ge 100.0$ points (or exceeds the Incumbent baseline performance).
- **On Victory:**
  1. The player's mobile suit **replaces** the incumbent suit across the faction's entire military doctrine.
  2. The faction pays an immediate **Upfront Licensing Bounty** (1,400,000 to 2,400,000 Cr).
  3. The faction locks in **Recurring Per-Turn Royalties** (38,000 to 58,000 Cr/turn).
  4. Faction Military Strength increases by +16 to +22 points.
  5. Winning faction standing jumps by +25.
  6. Rival faction standings decrease by -15 to -25 due to armed military escalation!
