# Document 12: Open Sandbox, Mass-Production Replacement & Career Retirement Systems

## 1. Executive Summary & Design Vision
In the tradition of classic sandbox simulations such as *Sid Meier's Pirates!*, *Mount & Blade*, and *Armored Core*, the player's PMC is never constrained to a rigid linear narrative. The player exists in an open interstellar theatre torn between four major superpowers (Terran Coalition, Outer Colonies, Rogue Syndicates, Apex Zaibatsu).

The player may pursue whatever career path aligns with their strategic ambition:
1. **The Military-Industrial Monopolist**: Replace the standard mass-produced suits of the major powers with proprietary player designs, extracting massive licensing fees and weekly production royalties while the superpowers fight using your machines.
2. **The Hegemon Warlord**: Field a personal PMC army, capture contested sectors, and systematically overthrow galactic superpowers to establish an independent sovereign dominion.
3. **The Shadow Opportunist / Arms Dealer**: Sell bleeding-edge prototypes to all sides, fuel endless border wars, and accumulate immense personal fortunes while maintaining plausible deniability.
4. **The Boutique Artisan**: Maintain a tight, elite squadron of ace pilots equipped with one-of-a-kind Masterwork prototypes, accepting only legendary black-ops contracts.

At any point, the player may **Retire & Assess Career Legacy**, receiving a granular score breakdown, historical epilogue, and dynamic title—or continue expanding their empire indefinitely.

---

## 2. Mass-Production Replacement Doctrine (MP Replacement)

### 2.1 Standard Issue Mass-Production Baselines
Each galactic faction enters the war with an established mass-produced grunt suit:
- **Terran Coalition**: GHA-07 Ironclad (Armor: 180, Power Surplus: 8 MW, Mobility: 38, Fabrication: 380,000 Cr)
- **Outer Colonies**: AET-01 Aether (Armor: 120, Power Surplus: 16 MW, Mobility: 68, Fabrication: 420,000 Cr)
- **Rogue Syndicates**: SCR-12 Hyena (Armor: 140, Power Surplus: 10 MW, Mobility: 52, Fabrication: 310,000 Cr)
- **Apex Zaibatsu**: ZAI-03 Muramasa (Armor: 130, Power Surplus: 14 MW, Mobility: 62, Fabrication: 460,000 Cr)

### 2.2 Pitching a Replacement Chassis
The player can submit any unlocked blueprint or customized mobile suit to a faction's Ordnance Board.
The Board calculates an **Ordnance Superiority Score (OSS)**:
$$\\text{OSS} = \\frac{\\text{Player Effective Rating}}{\\text{Faction Baseline Rating}} \\times \\left(1 + \\frac{\\text{Standing}}{200}\\right)$$

**Requirements for Adoption**:
1. Faction standing must be at least $+15$ (Friendly Contractor).
2. The player design must exceed the faction baseline in at least two core metrics (Armor, Power, or Speed) without exceeding budget limits.
3. Player must have fabricated at least one physical field-test unit in their hangar.

### 2.3 Economic & Strategic Payouts
Upon contract ratification:
- **Upfront License Bounty**: $1,500,000 - 3,000,000$ Credits deposited immediately into treasury.
- **Turn Royalties**: A passive royalty of $35,000 - 65,000$ Credits per day/turn based on active faction divisions deployed.
- **War Shift Bonus**: The adopting faction gains $+15\\%$ to $+30\\%$ combat effectiveness in the daily war simulation (`simulate_war_turn`), pushing frontlines in their favor.
- **Faction Status**: The player becomes the faction's **Chief Technological Supplier** ($+35$ Standing).

---

## 3. PMC Imperial Conquest & Faction Overthrow

### 3.1 Field Operations & Sortie Commitment
Players can transition from passive contractors to active conquerors. The War Room enables **Strategic PMC Offensives**:
- **Requirements**: At least 1 combat-ready Mobile Suit in the hangar and 1 assigned pilot.
- **Targeting**: Select any faction's border territory or contested frontline sector.
- **Tactical Power Ratio**:
  $$\\text{PMC Strike Power} = \\sum (\\text{Suit Armor} + \\text{Weapon Rating} \\times 1.5) \\times (1 + \\text{Pilot Combat Stat} \\times 0.05)$$
  Defending strength is derived from the target faction's current Military Strength Score.

### 3.2 Sector Annexation & Hegemony
When the player PMC defeats defending garrison forces:
- $2\\%$ to $6\\%$ of galactic territory flips immediately to **PMC Hegemony** (`pmc_territory_pct`).
- Defending faction loses equivalent territory share and $-8$ Military Strength.
- **Territory Tribute**: Each territory percentage under PMC control pays $4,000$ Credits and rare mineral extraction tribute per turn into company coffers.

### 3.3 Overthrowing a Galactic Power
When a faction's territory drops to $0\\%$ or military score drops below $10$:
- The faction capitulates and is marked as **OVERTHROWN / ANNEXED**.
- All remaining bases, orbital docks, and manufacturing plants are seized by the player's PMC.
- An interstellar news bulletin proclaims the fall of the regime and the rise of the Mercenary Protectorate.

---

## 4. Career Retirement & High Score Matrix (Sid Meier's Pirates! Model)

### 4.1 Voluntary Retirement
The player may retire at any time via the HQ Terminal. The simulation calculates an aggregate **Mercenary Prestige Score (MPS)** across 6 distinct categories (0 to 10,000+ points).

### 4.2 Scoring Formula
$$\\text{Total Score} = \\text{Score}_{\\text{Wealth}} + \\text{Score}_{\\text{Territory}} + \\text{Score}_{\\text{Monopoly}} + \\text{Score}_{\\text{Guild}} + \\text{Score}_{\\text{Tech}} + \\text{Score}_{\\text{Overthrow}}$$

1. **Treasury & Wealth Score** (Max 2,500 pts):
   $$\\min(2500, \\lfloor \\text{Net Worth} / 4000 \\rfloor)$$
2. **Territorial Hegemony Score** (Max 2,500 pts):
   $$\\text{PMC Territory \\%} \\times 25$$
3. **Mass-Production Monopoly Score** (Max 2,000 pts):
   $$500 \\text{ pts per faction replaced} + \\lfloor \\text{Cumulative Royalties} / 10000 \\rfloor$$
4. **Mercenary Ace Guild Score** (Max 1,000 pts):
   $$150 \\text{ pts per veteran pilot} + 50 \\text{ pts per victorious sortie}$$
5. **Technological Supremacy Score** (Max 1,000 pts):
   $$200 \\text{ pts per Masterwork tuned} + 100 \\text{ pts per blueprint unlocked}$$
6. **Faction Overthrow Score** (Max 1,000 pts):
   $$250 \\text{ pts per superpower regime overthrown and annexed}$$

### 4.3 Dynamic Career Ending Titles
Based on the final score distribution and player actions, one of ten prestigious historical titles is bestowed:
1. **Solar Hegemon & Supreme Warlord** ($\\ge 70\\%$ PMC Territory): You unified the fractured solar system beneath the iron banner of your private military corporation.
2. **The Shadow Puppetmaster** (All 4 factions adopt your MP suits, Treasury $\\ge 8,000,000$ Cr, PMC Territory $< 20\\%$): You never ruled a world openly; instead, you owned every gun in existence and puppeted heads of state from orbit.
3. **Titan of the Military-Industrial Complex** (Treasury $\\ge 12,000,000$ Cr, $\\ge 2$ MP contracts): Richest entity in human history. Superpowers begged for your manufacturing capacity.
4. **Grand Marshal of the Terran Coalition** (Terran Standing $\\ge 75$, Terran Territory $\\ge 55\\%$): You preserved Earth's dominion against orbital insurrection.
5. **Liberator of the Outer Colonies** (Colony Standing $\\ge 75$, Colony Territory $\\ge 55\\%$): Champion of the Lagrange orbital colonies, shattering Earth's monopoly.
6. **Dread Corsair Void Kingpin** (Syndicate Standing $\\ge 75$, Pirate Territory $\\ge 40\\%$): The asteroid belt and shipping lanes answered solely to your black-market armada.
7. **Apex Cyber-Oligarch** (Zaibatsu Standing $\\ge 75$, Tech Score $\\ge 800$): Merged biological aces with hyper-advanced cybernetic warforms to dictate galactic commerce.
8. **Master Artisan of the Void Frontier** (Masterworks $\\ge 4$, Pilots survived $\\ge 90\\%$): Legendary boutique armorer whose custom machines were revered as sacred relics.
9. **Hardened Mercenary Commander** (Score $3,000 - 5,999$ pts): Survived the bloody decade of the mecha wars with an honorable record and a full bank account.
10. **Frontier Scavenger in Default** (Score $< 3,000$ pts): Retired before establishing dominance, eking out a modest living in the asteroid frontier.

---

## 5. Non-Linear Sandbox Loop & Ongoing Play
Retirement does not lock or wipe save files:
- The player can review the full high score breakdown and historical chronicle.
- At the end of the debriefing, the player may choose **[CONTINUE PLAYING / RESUME SANDBOX]** to return to the active game loop, conquer additional sectors, or tune new experimental prototypes.
