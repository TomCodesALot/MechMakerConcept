# Document 28: Nemesis Corporate Hit Contracts, Faction Diplomatic Warfare & Railroad Tycoon Hostile Takeovers

## 1. Executive Summary
This document establishes the macro-corporate endgame and geopolitical battlefield dynamics of the Sol System PMC simulation. It links character nemeses, faction standing, and corporate economic dominance into a cohesive tactical sandbox:
1. **Rival Corporate Hit Contracts**: Rival conglomerates (**VHI, AOD, RUST, HATS**) hire ace nemeses to spearhead corporate raids, deploying active era line mechs and rare Black-Ops Prototype X-Chassis.
2. **Faction Diplomatic Assistance & Hindrance Matrix**: Active standing ($\ge +25$ Allied vs $\le -20$ Hostile) transforms tactical encounters into proxy wars, unlocking orbital MAC strikes, ECM blinding drones, field repairs, or hostile airspace interdictions.
3. **Railroad Tycoon Stock Exchange & Hostile Takeovers**: The player can trade equity shares of rival mega-corporations on the Sol Corporate Stock Exchange. Acquiring a majority (51%+) unlocks boardroom veto power and royalty extraction, while a full buyout (100%) permanently eliminates the rival company from the board, absorbs their R&D blueprints and assembly lines, and paves the path to the **Sol Industrial Monopoly** endgame.
4. **Front Mission 16-Bit SNES Character Portrait Standard**: Complete visual overhaul of character busts to authentic 16-bit dithered pixel art adhering to *Front Mission* (SNES, 1995) aesthetic conventions.

---

## 2. Sol Corporate Stock Exchange & Railroad Tycoon Takeover Engine

### 2.1 Dynamic Share Pricing Model
Each of the 4 rival mega-corporations maintains **100,000 Total Equity Shares**:
- **VHI (Valkyrie Heavy Industries)**: Ticker `VHI` (Base: 120 Cr/sh)
- **AOD (Astraea Orbital Dynamics)**: Ticker `AOD` (Base: 135 Cr/sh)
- **RUST (Rustworks Salvage Cartel)**: Ticker `RUST` (Base: 45 Cr/sh)
- **HATS (Hyperion Advanced Tactical Systems)**: Ticker `HATS` (Base: 95 Cr/sh)

The active share price updates each strategic cycle according to:
$$ \text{SharePrice} = \text{clamp}\left(\text{round}\left(\text{BasePrice} \times \frac{\text{MarketShare}}{25.0} \times (1.0 + (\text{Era} - 1) \times 0.35) \times \text{EventMultiplier}\right), 15, 600\right) $$

- **Market Shifts**:
  - Winning a Procurement Fly-Off Trial: $+15\%$ Share Price surge.
  - Losing a Procurement Fly-Off Trial: $-10\%$ Share Price decline.
  - Reactor Meltdown / Field Failure Scandal: $-30\%$ Share Price crash (creating buyout windows).

### 2.2 Ownership Stakes & Corporate Influence Tiers
| Equity Tier | Shares Required | Strategic & Financial Perks |
|---|---|---|
| **Retail Investor (5%)** | 5,000 shares | Receives quarterly dividend income ($0.2\%$ of share value per turn). |
| **Significant Stake (10%)** | 10,000 shares | Continuous dividend cashflow + insider procurement insight ($+3$ PTS in Fly-Off Trials vs that rival). |
| **Board Seat (25%)** | 25,000 shares | Unlocks full R&D tree transparency; $+8$ PTS in Fly-Off Procurement Trials vs that rival. |
| **Controlling Majority (51%)** | 51,000 shares | **Boardroom Veto Control**: Can force $-15$ PTS trial penalty on rival suits, veto black-ops raids, or extract a **10% Gross Profit Royalty** paid to player treasury each turn. |
| **Full Hostile Takeover (100%)** | 100,000 shares | **COMPLETE RIVAL ELIMINATION**: Rival is removed from the board, market share absorbed into player PMC, active line & X-chassis blueprints transferred to player, $+1$ orbital assembly line unlocked, card permanently stamped `[ ACQUIRED // PMC SUBSIDIARY ]`. |

### 2.3 Endgame Condition: Sol Industrial Monopoly
Acquiring all 4 rival mega-corporations (100% equity across VHI, AOD, RUST, and HATS) completes the **Sol Industrial Monopoly**, establishing the player's company as the supreme, unchallenged arms manufacturer in the Solar System.

---

## 3. Faction Diplomatic Battlefield Intervention Matrix

When tactical combat or incursion sorties commence, `obj_FactionManager` cross-references standing with the 4 sovereign factions:

```
+-------------------+--------------------------------------+------------------------------------+
| FACTION           | ALLIED INTERVENTION (Standing >= +25)| HOSTILE HINDRANCE (Standing <= -20)|
+-------------------+--------------------------------------+------------------------------------+
| Terran Coalition  | Orbital MAC Battery Strike           | Airspace Lock-Out Interdiction     |
|                   | (-350 to -450 Armor to Boss)         | (-2 AP to Player on Turn 1)        |
| Outer Colonies    | ECM Sensor Jamming Drones            | Solar Thermal Flare Satellite      |
|                   | (-20% Enemy Hit, -2 Enemy AP)        | (+25% Player Weapon Heat Gen)      |
| Rogue Syndicate   | Emergency Field Repair Capsule       | Flanking Mercenary Raiders         |
|                   | (+250 Armor Repaired to Allies)      | (2 Auxiliary Raider Hyenas)        |
| Apex Zaibatsu     | Cyber-Neural Overload Virus          | Sensor Scrambler Worm              |
|                   | (+40 Boss Heat, Weapons Disabled)    | (-15% Player Accuracy)             |
+-------------------+--------------------------------------+------------------------------------+
```

---

## 4. Nemesis Corporate Hit Contracts & Interrogation Loop

1. **Contract Issuance**: Rival corporations with hostility $>20\%$ or during corporate events post private assassination bounties with nemeses from `obj_NemesisManager`.
2. **Tactical Incursion**: Nemesis arrives piloting the rival's active Era line chassis or rare Black-Ops Prototype X-chassis, accompanied by custom employer dialogue barks.
3. **Capture & Interrogation**:
   - Defeating the contractor nemesis adds them to the Dreadnought brig (`prisoner_list`).
   - **Interrogate for Insider Telemetry**: Grants $+2,000$ shares of the hiring rival or $+10$ Fly-Off insight.
   - **Ransom to Corporation**: Extorts $150,000$–$300,000$ Credits directly from the rival conglomerate's treasury.

---

## 5. Front Mission 16-Bit Character Portraits Art Specification
- **Native Resolution**: 100x100 pixel canvas integer-scaled 2x to 200x200 RGBA.
- **Aesthetic Benchmark**: *Front Mission* (SNES, 1995) character portraits designed by Yoshitaka Amano.
- **Visual Vocabulary**: 16-to-25 indexed colors, high-contrast outlines, shaded cheekbones, tactical headsets with curved boom microphones, cybernetic optical visors/monocles, high officer collars, rank pins, battle scars, and CRT scanlines.
