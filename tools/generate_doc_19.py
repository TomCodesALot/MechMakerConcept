#!/usr/bin/env python3
"""
tools/generate_doc_19.py
Assembles and writes the complete Document 19:
Pilot Nemesis System & Dynamic Character Relationship Web
with Front Mission SNES Visual Design Bible, Romances, Friendships,
Procedural Playthrough Allegiance Variance, and Complete 204-Character Database.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROSTER_PATH = os.path.join(BASE_DIR, "datafiles", "characters_roster.json")
DOC_PATH = os.path.join(BASE_DIR, "docs", "19_pilot_nemesis_system_and_character_relationships.md")

with open(ROSTER_PATH, "r", encoding="utf-8") as f:
    roster_data = json.load(f)

characters = roster_data["characters"]
char_map = {c["id"]: c for c in characters}

def get_kinship_str(c):
    kin = c.get("kinship") or []
    if not kin:
        return "None"
    items = []
    for k in kin:
        target = k.get("target_id", "").replace("char_", "").replace("pilot_", "")
        rel = k.get("relation", "").replace("_", " ")
        items.append(f"{rel.capitalize()}: `{target}`")
    return "; ".join(items)

def get_connections_str(c):
    parts = []
    if c.get("wingman_id"):
        w = c["wingman_id"].replace("char_", "").replace("pilot_", "")
        parts.append(f"Wingman: `{w}`")
    if c.get("mentor_id"):
        m = c["mentor_id"].replace("char_", "").replace("pilot_", "")
        parts.append(f"Mentor: `{m}`")
    if c.get("rival_id"):
        r = c["rival_id"].replace("char_", "").replace("pilot_", "")
        parts.append(f"Rival: `{r}`")
    kin = get_kinship_str(c)
    if kin != "None":
        parts.append(kin)
    return "<br>".join(parts) if parts else "Independent"

def get_romance_str(c):
    rom = c.get("love_interest")
    if not rom:
        return "*Single / Unattached*"
    status_label = rom["relationship_type"].replace("_", " ").capitalize()
    return f"**{rom['target_name']}**<br>*{status_label}* (Intensity {rom['intensity']}%)<br>`{rom['trauma_reaction']}`"

def get_friendship_str(c):
    fr = c.get("friendships")
    if not fr or not fr.get("friend_names"):
        return "*Solo Operator*"
    names = ", ".join(fr["friend_names"][:2])
    bond = fr["bond_type"].replace("_", " ").capitalize()
    return f"**{bond}**:<br>{names}<br>*{fr['sortie_synergy']}*"

def get_variance_str(c):
    var = c.get("allegiance_variance")
    if not var:
        return "*Fixed Loyalty*"
    loyalty = var["ideological_loyalty"].replace("_", " ").capitalize()
    flex = var["flexibility_score"]
    can_w = var["playthrough_weights"].get(var["canonical_faction"], 1.0)
    indep_w = var["playthrough_weights"].get("independent", 0.0)
    return f"**{loyalty}** (Flex {flex})<br>Canonical: {can_w*100:.0f}%<br>Indep: {indep_w*100:.0f}%"

def build_pilot_table(faction_id):
    f_chars = [c for c in characters if c["faction_id"] == faction_id and c["is_recruitable"]]
    lines = [
        "| ID & Callsign | Full Name & Tier | Preferred MS & Traits | Potential Love Interest | Friendship Circle & Synergy | Playthrough Faction Variance | Cost & Salary |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :---: |"
    ]
    for c in f_chars:
        cid = f"`{c['id']}`<br>**\"{c['callsign']}\"**"
        name_tier = f"**{c['name']}**<br>Tier **T{c['tier']}**"
        traits = ", ".join([f"`{t}`" for t in c.get("traits", [])])
        ms_traits = f"`{c['preferred_chassis']}`<br>{traits}"
        romance = get_romance_str(c)
        friends = get_friendship_str(c)
        variance = get_variance_str(c)
        cost = f"**{c['hiring_cost_cr']:,} Cr**<br>({c['salary_per_cycle_cr']:,}/cyc)"
        lines.append(f"| {cid} | {name_tier} | {ms_traits} | {romance} | {friends} | {variance} | {cost} |")
    return "\n".join(lines)

def build_vip_table(faction_id):
    f_chars = [c for c in characters if c["faction_id"] == faction_id and not c["is_recruitable"]]
    lines = [
        "| ID & Name | Title & Planetary Role | Dynasty & Kinship | Love Interest & Secret Ties | Ideological Stance & Consequence |",
        "| :--- | :--- | :---: | :--- | :--- |"
    ]
    for c in f_chars:
        cid = f"`{c['id']}`<br>**{c['name']}**"
        role = c["role"]
        dynasty = f"**{c.get('family_dynasty')}**" if c.get('family_dynasty') else "*Non-Dynastic*"
        conn = get_connections_str(c)
        dyn_conn = f"{dynasty}<br>{conn}"
        romance = get_romance_str(c)
        bio = c.get("bio", "").replace("\n", " ")
        var = c.get("allegiance_variance", {})
        loyalty = var.get("ideological_loyalty", "diehard_purist").replace("_", " ").capitalize()
        stance = f"**{loyalty}**<br>{bio}"
        lines.append(f"| {cid} | {role} | {dyn_conn} | {romance} | {stance} |")
    return "\n".join(lines)

with open(DOC_PATH, "w", encoding="utf-8") as out:
    out.write(r"""# Document 19: Pilot Nemesis System, Relational Character Web & Dynamic Allegiance Engine
**Document Version:** 1.2.0  
**Target Systems:** GameMaker Studio 2 (Modern GML), Datafiles JSON Pipeline (`datafiles/characters_roster.json`)  
**Inspirational Benchmarks:** *Middle-earth: Shadow of Mordor / War* (Monolith Nemesis System), *Front Mission 1/3/5* (Square / SNES 1995), *BattleTech*, *Crusader Kings III*, *Fire Emblem: Genealogy of the Holy War*  
**Authors & Contributors:** Lead Systems Architect (Lead Dev), Lead Game Designer (Director GDD), Lead Narrative Designer, Lead QA Engineer, Technical Art Director

---

## 1. Executive Summary & Core Philosophical Pillars

In *MechMakerConcept*, mobile suits are mechanical manifestations of geopolitical mass destruction, but human agency pulls the triggers. The **Pilot Nemesis & Relational Character Web System** elevates tactical isometric battles and base management into a high-stakes, consequences-driven human drama.

Characters—ranging from supreme planetary directors and fleet commodores to mercenary aces, trench grunts, and recruited PMC rookies—are not disposable stat-blocks. They belong to a **living directed relationship multi-graph** anchored by bloodlines, mentorship bonds, ideological loyalties, close comradeship circles, romantic devotion, and bitter grudges.

```
                                [THE PLAYER PMC]
                               /        |       \
                     (Actions)          |         (Decisions)
                       /                |                \
                      v                 v                 v
            [Assassination / Kill]  [Imprisonment]  [Faction Contracts]
                      |                 |                 |
                      v                 v                 v
             +--------------------------------------------------+
             |             RELATIONAL GRAPH DISPATCHER          |
             +--------------------------------------------------+
              /            |                  |               \
             v             v                  v                v
     [Blood Vendettas] [Romance Trauma] [Friend Cascades] [Faction Shifts]
      (Kin / Wingmen)   (Heartbreak)     (Referral/Morale) (Seed Variance)
             |             |                  |                |
             v             v                  v                v
     [Drop-Pod Ambush] [Suicidal Charge] [Mutiny Threat]  [Dynamic Roster]
```

### 1.1 Core Design Directives
1. **Consequences Have Faces**: If the player obliterates an enemy ace in combat or orders the execution of an imprisoned general, their kin, lovers, wingmen, and pupils actively retaliate.
2. **The Romantic Web & Heartbreak Calculus**: Pilots form deep emotional bonds (spouses, courting, star-crossed cross-faction lovers, unrequited devotion, and bitter ex-flames). Harming a pilot's love interest unleashes catastrophic emotional trauma ($K_{\text{romance}} = 3.0\times$ grudge multiplier, triggering `berserker_rage` or `suicidal_charge`).
3. **Friendship Networks & Comradeship Synergies**: Pilots maintain circles of 2–4 close friends (academy classmates, trench survivors, cantina comrades). Hiring one friend unlocks recruitment discounts and morale boosts; losing a friend triggers grieving and mutiny risk.
4. **Procedural Playthrough Allegiance Variation**: To deliver infinite campaign replayability, pilots are not permanently bound to a single hiring hall. Each playthrough seeds dynamic faction allegiances—disillusioned veterans can defect, corporate contractors switch sponsors, and roaming ronin drift across solar borders.
5. **Front Mission (SNES, 1995) Visual Authenticity**: All character portraits adhere strictly to the 16-bit Super Nintendo *Front Mission 1 (1995)* aesthetic backdrop: 64x64 pixel busts, high-contrast dithered shading, aviator comm headsets with boom mics, high-collar flak jackets, and dynamic palette swapping upon faction defection.

---

## 2. Mathematical Relationship Graph & Grudge Calculus

The game universe models all 204 figures as nodes within a directed multi-graph:
$$\mathcal{G} = (\mathcal{V}, \mathcal{E})$$

Where each node $v_i \in \mathcal{V}$ represents a character, and each directed edge $e_{ij} = (v_i, v_j, \tau, \omega) \in \mathcal{E}$ represents a relationship of type $\tau$ with weight $\omega$.

### 2.1 Character State Vector
Each character struct in GameMaker maintains dynamic emotional variables:
$$\mathbf{S}_i = \begin{bmatrix} A_{i,\text{player}} \\ V_{i,\text{player}} \\ L_{i,\text{faction}} \\ F_{i,\text{player}} \\ M_i \end{bmatrix} = \begin{bmatrix} \text{Affinity toward Player} \in [-100, 100] \\ \text{Vendetta / Grudge Level} \in [0, 100] \\ \text{Faction Loyalty} \in [0, 100] \\ \text{Fear of Player} \in [0, 100] \\ \text{Morale} \in [0, 100] \end{bmatrix}$$

### 2.2 Grudge & Heartbreak Propagation Calculus
When Character $K$ is killed, executed, or captured by the player, ripple events dispatch across all incident edges $e_{jK} \in \mathcal{E}$:

$$\Delta V_j = \min\left(100, \; \Delta V_j + (B_{\text{severity}} \times K_{\text{bond}} \times I_{\text{intensity}})\right)$$

$$\Delta A_j = \max\left(-100, \; \Delta A_j - (B_{\text{severity}} \times K_{\text{bond}} \times 1.25)\right)$$

Where:
- $B_{\text{severity}}$: Base event severity (Combat Kill: $+30$, Core Meltdown: $+45$, Formal Execution in Prison: $+75$).
- $K_{\text{bond}}$: Relationship multiplier:
  - **Love Interest / Spouse / Star-Crossed Partner**: $\mathbf{\times 3.00}$ (Absolute highest emotional priority)
  - Parent / Child / Sibling: $\times 2.50$
  - Sworn Wingman / Mentor / Protégé: $\times 1.80$
  - Close Friend / Trench Survivor: $\times 1.50$
  - Extended Family (Cousin, In-Law): $\times 1.30$
  - Faction Comrade: $\times 1.00$
- $I_{\text{intensity}}$: Emotional connection coefficient ($0.65$ to $0.95$).

### 2.3 Combat Romance Trauma States
When a character's romantic partner is disabled or incinerated in combat, the surviving lover immediately enters one of five psychological trauma states:

| Trauma State | Psychological Response | Tactical Combat Overrides |
| :--- | :--- | :--- |
| **`berserker_rage`** | Blind, destructive fury. | Gains $+25\%$ kinetic/melee damage, $+20\%$ weapon heat tolerance; ignores evasive maneuvers and charges the killer. |
| **`suicidal_charge`** | Complete loss of survival instinct. | Ejection module is disabled; locks core overclock to maximum; rushes point-blank range to trigger a manual core detonation. |
| **`protective_intercept`** | Desperate self-sacrifice. | Automatically redirects their mobile suit to take line-of-fire hits aimed at their lover's chassis if within 3 grid tiles. |
| **`grief_paralysis`** | Catatonic despair. | Suffers $-50\%$ evasion and accuracy; unit skips alternate action phases due to sensory overload. |
| **`hostage_bargain`** | Conditional compliance. | If the lover is captured alive in the player brig, this pilot refuses to engage player units and can be coerced into defection. |

---

## 3. The Front Mission (SNES, 1995) Character Design Bible

```
+-----------------------------------------------------------------------------------+
|               FRONT MISSION (SUPER NINTENDO, 1995) VISUAL BENCHMARK               |
|                                                                                   |
|  [64x64 Native Pixel Canvas] -> [Beveled Metallic Border] -> [16-Color Palette]   |
|  [High Ballistic Collar]     -> [Aviator Boom Microphone] -> [Tachyon Cybernetics]|
+-----------------------------------------------------------------------------------+
```

![Front Mission SNES Pilot Portrait Master Reference](assets/front_mission_snes_portraits_master.jpg)

### 3.1 Art Direction & Historical Backdrop
Character portraits in *MechMakerConcept* draw direct aesthetic heritage from **Front Mission (Square, 1995, Super Famicom)**, illustrated by Yoshitaka Amano with mechanical design by Kow Yokoyama and Yoshiyuki Sadamoto. 

The visual style rejects clean, glossy space-opera tropes in favor of **gritty, worn military realism**:
- **Tired, Cold Gaze**: Pilots exhibit hollow eyes, furrowed brows, and angular facial planes shaped by high-G maneuvers, neural feedback stress, and cockpit insomnia.
- **Flight Suit Functionalism**: Collars are thick ballistic neck protectors with visible seams and heavy brass zippers.
- **Retro Tactical Avionics**: Pilots wear bulky single-cup or dual-cup communications headsets with metal spring headbands, curved boom microphones positioning capsules directly at the mouth corner, and coiled black wiring running into chest avionics ports.
- **Visible Battlefield Trauma**: Shrapnel scars, chemical burns, glass lacerations, and rough field stitches demonstrate cockpit survival.
- **Cybernetic Augmentations**: Zaibatsu and rim pilots feature crude or sub-nanometer cybernetics—matte black ocular camera sockets with glowing cyan reticles, cranial brackets, and sub-dermal data jack ports behind the ear.

### 3.2 Technical Frame & Palette Specifications
All character portraits are authored to strict SNES hardware constraints:

| Parameter | Engine Specification | GameMaker Studio 2 Asset Pipeline |
| :--- | :--- | :--- |
| **Native Resolution** | $64 \times 64\text{ pixels}$ | Stored in `spr_portrait_*` (Uniform $64 \times 64$) |
| **Upscaled UI Render** | $128 \times 128\text{ px}$ (2x) / $256 \times 256\text{ px}$ (4x) | Scaled via Point / Nearest Neighbor sampling |
| **Color Depth** | 16 Colors per sub-palette (4-bit indexed) | Strict indexed color ramps to preserve retro contrast |
| **Frame Border** | 2-pixel outer beveled metallic rim | Top/Left: Highlight `#6C757D`, Bottom/Right: `#2A2D34` |
| **Dithering Technique** | Ordered $2 \times 2$ checkerboard dithering | Applied to cheekbone transitions, neck shadow, and background |

### 3.3 Faction 16-Color Indexed Palettes & Defection Reskinning
Each faction maintains an authentic 16-color retro palette:

```
[TERRAN COALITION]       : Olive Drab (#43523B), Khaki (#7C8068), Brass Eagle (#C69B3D), Cold Steel (#505860)
[OUTER COLONIES LEAGUE]  : Cobalt Navy (#1D3354), Pearl Silver (#9EADB8), Aristocratic Azure (#467599), Chrome (#E0E5E9)
[SYNDICATE RIM]          : Distressed Rust (#5C241C), Scrapper Leather (#684A36), Hazard Amber (#D4812B), Copper (#3B5B57)
[ZAIBATSU AEROSPACE]     : Matte Obsidian (#18191E), Carbon Weave (#2B2D35), Neon Cyan (#00F0FF), Magenta Monocle (#D6006E)
```

![SNES Faction Portraits Strip](assets/snes_faction_portraits_strip4_2x.png)
*Figure 3.1: Four-Faction Master Reference Strip at 2x Integer Scale (Terran Commander Vance, Colony Fleet Ace Cassian, Syndicate Reaver Jackal, Zaibatsu Cyber-Pilot Null-07).*

When a pilot rolls an alternate faction at campaign start, the procedural compositor swaps the portrait's Layer 1 uniform palette to match the newly adopted faction's signature colors!

---

## 4. Procedural Playthrough Allegiance Variation System

To maximize campaign replayability, pilot faction alignments are **probabilistically seeded** rather than hardcoded. Across different campaigns, pilots might appear under different banners based on political purges, corporate poaching, or mercenary contracts.

```
+------------------------------------------------------------------------------------+
|                   PROCEDURAL CAMPAIGN ALLEGIANCE SEED ENGINE                       |
|                                                                                    |
|  [Campaign Seed] -> [Pilot Archetype] -> [Evaluate Weights] -> [Assign Faction]   |
|         |                     |                   |                    |           |
|         v                     v                   v                    v           |
|    random_set_seed     Diehard Purist      Terran (85%)         Dynamic Portrait   |
|     (Deterministic)   Free Contractor     Syndicate (10%)       Palette Recolor    |
|                       Roaming Ronin       Indep (5%)            Defection Hook     |
+------------------------------------------------------------------------------------+
```

### 4.1 Ideological Loyalty Archetypes
Every character belongs to one of five ideological flexibility categories:

1. **`diehard_purist` (Flexibility: 0.0)**:
   - *Target Figures*: 72 High Command VIPs, Faction Patriarchs/Matriarchs (e.g. Gen. Deborah Vance, Director Renzo Takahashi, Fleet Cmdr Cassian Vane, Madame Rosalind Cruz).
   - *Behavior*: 100% locked to their home faction. They represent the ideological core of the war and never defect.
2. **`career_officer` (Flexibility: 0.15)**:
   - *Target Figures*: Elite Tier 3 Aces, Dedicated Staff Officers.
   - *Distribution*: 85% Canonical Faction, 7% Independent Freelance, 8% Rival Factions.
   - *Defection Narrative*: Only severe military tribunals or hostage negotiations cause them to fly under foreign flags.
3. **`disillusioned_veteran` (Flexibility: 0.35)**:
   - *Target Figures*: Tier 2 Veterans, Trench Grunts.
   - *Distribution*: 65% Canonical Faction, 15% Independent, 20% Rival Factions.
   - *Defection Narrative*: High weariness of planetary war; frequently recruited by private security or rival corporate interests.
4. **`free_contractor` (Flexibility: 0.50)**:
   - *Target Figures*: Tier 1 Rookies, Scrappers, Tech-Pilots.
   - *Distribution*: 50% Canonical Faction, 20% Independent, 30% Other Factions.
   - *Defection Narrative*: Motivated by debt payoff, signing bonuses, or personal survival.
5. **`roaming_ronin` (Flexibility: 0.80)**:
   - *Target Figures*: 12 Legendary Independent Mercenaries.
   - *Distribution*: Dispersed across all 4 major factions (20% Terran, 20% Colony, 20% Syndicate, 20% Zaibatsu, 20% Independent).
   - *Defection Narrative*: Free agents who sign exclusive campaign retainers with whoever bids highest.

### 4.2 Playthrough Seed Roll Algorithm (GML)
At campaign generation, the engine initializes deterministically:

```gml
function scr_campaign_seed_allegiance_roll(_campaign_seed) {
    random_set_seed(_campaign_seed);
    var _char_keys = variable_struct_get_names(obj_NemesisManager.characters_map);
    
    for (var i = 0; i < array_length(_char_keys); i++) {
        var _c = variable_struct_get(obj_NemesisManager.characters_map, _char_keys[i]);
        var _var_data = _c.allegiance_variance;
        
        // Skip purists
        if (_var_data.ideological_loyalty == "diehard_purist") {
            _c.current_faction_id = _var_data.canonical_faction;
            continue;
        }
        
        // Roll random float [0.0, 1.0)
        var _roll = random(1.0);
        var _weights = _var_data.playthrough_weights;
        var _cumulative = 0.0;
        var _assigned_faction = _var_data.canonical_faction;
        
        var _fac_keys = variable_struct_get_names(_weights);
        for (var f = 0; f < array_length(_fac_keys); f++) {
            var _fk = _fac_keys[f];
            _cumulative += variable_struct_get(_weights, _fk);
            if (_roll <= _cumulative) {
                _assigned_faction = _fk;
                break;
            }
        }
        
        _c.current_faction_id = _assigned_faction;
        
        // Update defection bio if changed
        if (_assigned_faction != _var_data.canonical_faction) {
            _c.active_defection_hook = variable_struct_get(_var_data.defection_hooks, _assigned_faction);
            show_debug_message("CAMPAIGN VARIANCE: " + _c.name + " defected from " + _var_data.canonical_faction + " to " + _assigned_faction);
        }
    }
}
```

---

## 5. Universe Census & Dynastic Lineage Graphs

The game universe contains **exactly 204 named figures** defined in `datafiles/characters_roster.json`.

```
+-----------------------------------------------------------------------------------------+
|                              UNIVERSE CENSUS SUMMARY MATRIX                             |
+-------------------------+--------------------+---------------------+--------------------+
| Faction                 | Total Figures      | Recruitable Pilots  | High-Value VIPs    |
+-------------------------+--------------------+---------------------+--------------------+
| Terran Coalition        | 48 Figures         | 30 Recruitable      | 18 Non-Recruitable |
| Outer Colonies League   | 48 Figures         | 30 Recruitable      | 18 Non-Recruitable |
| Syndicate Rim           | 48 Figures         | 30 Recruitable      | 18 Non-Recruitable |
| Zaibatsu Aerospace      | 48 Figures         | 30 Recruitable      | 18 Non-Recruitable |
| Independent Drifters    | 12 Figures         | 12 Recruitable      | 0 Non-Recruitable  |
+-------------------------+--------------------+---------------------+--------------------+
| TOTAL UNIVERSE ROSTER   | 204 Named Figures  | 132 Pilots          | 72 Commanders/VIPs |
+-------------------------+--------------------+---------------------+--------------------+
```

### 5.1 The Seven Major Interstellar Dynasties

#### 1. House Vance (Terran Hegemony vs. Syndicate Exile) — 11 Figures
- **Patriarch / Matriarch**: General Deborah Vance (`char_terran_vance`), Supreme Director of Planetary Ordnance.
- **Dynasty Theme**: Iron-fisted Terran military aristocracy shattered by ideological desertion.
- **Lineage Tree**:
```
                        General Deborah Vance
                         (Terran Supreme Cmd)
                                  |
         +------------------------+------------------------+
         |                                                 |
  Julian Vance (Brother)                            Claire Vance (Daughter)
  (Terran Senate Hawk)                              (Trench Battery Commander)
         |                                                 |
  +------+------+                                   Tyler Vance (Son)
  |             |                                   (Artillery Test Ace)
Jax Vance     Victor Vance (Cousin)
"Jackal"      (Logistics Liaison)
(ESTRANGED NEPHEW)
[SYNDICATE REAVER ACE]
```

#### 2. House Vane (Colony Aristocratic Armada) — 8 Figures
- **Patriarch**: Fleet Commander Cassian Vane (`char_colony_cassian`).
- **Dynasty Theme**: Jovian orbital shipbuilders and aristocratic naval nobility.
- **Key Members**: Lady Genevieve Vane (Chief Orbital Engineer), Lucian Vane (Star-Legion Ace), Lyra Vane (Sensor Specialist), Roland Vane (Shipyard Director).

#### 3. House Cruz (Syndicate Rim Underworld Cartel) — 7 Figures
- **Matriarch**: Madame Rosalind Cruz (`char_syndicate_cruz`), High Fence of Callisto.
- **Dynasty Theme**: Black-market smuggling, scrap processing cartels, and pirate armadas.
- **Key Members**: Hector Cruz (Enforcer Wingman), Mateo Cruz (Smuggler Pilot), Sofia Cruz (Shadow Broker), Diego Cruz (Marauder Pilot).

#### 4. House Takahashi (Zaibatsu Executive Board) — 7 Figures
- **Patriarch**: Director Renzo Takahashi (`char_zaibatsu_takahashi`), VP of Advanced Mobile Armor.
- **Dynasty Theme**: Transhumanist cybernetics, corporate espionage, and ruthless corporate climbing.
- **Key Members**: Dr. Kenji Takahashi (Lead Cyber-Neurologist), Kaori Takahashi (Test Ace), Shinji Takahashi (Internal Affairs Director).

#### 5. House Rostov (Terran Veteran Artillery Lineage) — 5 Figures
- **Patriarch**: Colonel Viktor Rostov (`char_terran_viktor_rostov`).
- **Dynasty Theme**: Multigenerational trench artillerymen and frontline heavy walkers.
- **Key Members**: Elena Rostova (`pilot_terran_rostov`, Ace Pilot), Boris Rostov, Mikhail Rostov, Daria Rostova.

#### 6. House Thorne (Syndicate Marauder Kin) — 5 Figures
- **Warlord**: 'Gargoyle' Silas Thorne (`pilot_syndicate_thorne`).
- **Dynasty Theme**: Brutal raider clans operating modified close-combat mobile suits.
- **Key Members**: Boris Thorne, Val Thorne, Maya Thorne, Corva Thorne.

#### 7. Cross-Faction Dynasties: Chen, Lin, Mori, Ortiz, Torval, Morgan
- Families torn across faction borders through migration, mercenary employment, and corporate contracts.

---

## 6. Recruitable Pilot Registries (The 30 Recruitable Pilots per Faction)

Below are the complete dossiers for the **132 Recruitable Pilots** available for contract across the four warring powers and independent space, featuring their **Love Interests**, **Friendship Circles**, and **Playthrough Allegiance Weights**.

### 6.1 Terran Coalition Pilot Corps (30 Recruitable Pilots)
""")

    out.write(build_pilot_table("faction_terran") + "\n\n---\n\n")

    out.write("### 6.2 Outer Colonies League Star-Legion (30 Recruitable Pilots)\n")
    out.write(build_pilot_table("faction_colony") + "\n\n---\n\n")

    out.write("### 6.3 Syndicate Rim Marauders & Rust Aces (30 Recruitable Pilots)\n")
    out.write(build_pilot_table("faction_syndicate") + "\n\n---\n\n")

    out.write("### 6.4 Zaibatsu Aerospace Cyber-Pilots & Test Aces (30 Recruitable Pilots)\n")
    out.write(build_pilot_table("faction_zaibatsu") + "\n\n---\n\n")

    out.write("### 6.5 Independent Ronin & Legendary Mercenaries (12 Recruitable Pilots)\n")
    out.write(build_pilot_table("independent") + "\n\n---\n\n")

    out.write(r"""## 7. High-Value Targets & Command Structures (The 72 VIPs)

The game features **72 Non-Recruitable VIPs and Military Leaders** (18 per major faction) who command fleets, govern orbital sectors, and fund military R&D. Eliminating or capturing them triggers massive geopolitical and relational shocks.

### 7.1 Terran Coalition High Command & Aristocracy (18 VIPs)
""")
    out.write(build_vip_table("faction_terran") + "\n\n---\n\n")

    out.write("### 7.2 Outer Colonies League High Council & Admiralty (18 VIPs)\n")
    out.write(build_vip_table("faction_colony") + "\n\n---\n\n")

    out.write("### 7.3 Syndicate Rim Cartel Barons & Smuggling Lords (18 VIPs)\n")
    out.write(build_vip_table("faction_syndicate") + "\n\n---\n\n")

    out.write("### 7.4 Zaibatsu Aerospace Board of Directors & Lead Researchers (18 VIPs)\n")
    out.write(build_vip_table("faction_zaibatsu") + "\n\n---\n\n")

    out.write(r"""## 8. The Monolith-Style Nemesis Dynamic Loop

Adapted from Monolith's *Nemesis System*, rival pilots undergo dynamic psychological and physical evolution across repeated battlefield encounters.

```
+------------------------------------------------------------------------------------+
|                         THE BATTLEFIELD EVOLUTION CYCLE                            |
|                                                                                    |
|  [Cockpit Ejection Survives] -> [Acquires Trait: core_breaker / scarred_survivor]  |
|               |                                         |                          |
|               v                                         v                          |
|   [Gains Tachyon Cyber-Optic]               [Promoted to Strike Flight Leader]     |
|               |                                         |                          |
|               +-------------------+---------------------+                          |
|                                   v                                                |
|                   [Swears Blood Vendetta Against Player]                           |
+------------------------------------------------------------------------------------+
```

### 8.1 Dynamic Combat Memories & Trait Gains
Surviving pilots record specific combat trauma flags in their `traits` array:
- **`core_breaker`**: Earned if the pilot successfully destroyed one of the player's mobile suits in a previous battle (+15% Kinetic damage vs player mechs).
- **`scarred_survivor`**: Earned when surviving an eject under 10% core integrity (Immune to battlefield panic morale penalties).
- **`artillery_phobia`**: Earned if their chassis was shredded by long-range artillery splash (-20% accuracy when receiving incoming indirect fire).
- **`vendetta_sworn`**: Earned if the player executed their family member or wingman (Ignores retreat orders; gains +25% melee damage).

### 8.2 Battlefield Dialogue Barks
When entering combat within sensor range of the player, a Nemesis triggers dedicated comms barks matching their history:
- **Surviving Ejection**: *"You thought that fusion flare incinerated me, mercenary? You only scorched away my mercy. Look at my face!"*
- **Avenge Kin (House Vance)**: *"You put Deborah Vance in the dirt. I don't care about Earth's treaty—your squad dies in this trench!"*
- **Avenge Lover**: *"You shredded Kira's cockpit at Callisto. Every missile on this chassis has your name carved into the casing!"*

---

## 9. Prisoner Disposition, Interrogation & Diplomatic Hostages

When an enemy mobile suit is disabled without destroying the cockpit module, the pilot or VIP is captured and transferred to the player's base brig.

```
                           [CAPTURED ENEMY PILOT / VIP]
                                       |
          +----------------------------+----------------------------+
          |                            |                            |
          v                            v                            v
   [EXECUTE PILOT]              [RANSOM TO FACTION]          [CONVERT / RECRUIT]
          |                            |                            |
  - Faction Grudge +50         + Faction Rep +10            + Adds Ace to Roster
  - Kin Vendettas Declared     + Substantial Credits        - Morale Check Required
  - Embargo Triggers           - Prisoner Returns to Duty   - Requires Defection Clout
```

| Decision Path | Resource Gain | Relational & Geopolitical Impact |
| :--- | :--- | :--- |
| **Execute Prisoner** | Salvage experimental pilot cybernetics and personal gear. | Dispatches `EVENT_EXECUTION` to all kin ($+75\text{ Grudge}$) and lovers ($+90\text{ Grudge}$). Triggers blood feuds and ambushes. |
| **Ransom to Faction** | $+50,000$ to $+500,000\text{ Cr}$ depending on character Tier. | Faction Grudge reduced by $-15$. Captive returns to active enemy service. |
| **Recruit / Turn** | Converts skilled Ace into player roster. | Requires breaking loyalty via interrogation. May trigger retaliation from former faction comrades. |
| **Lover Hostage Leverage** | Forcibly recruits the captive's love interest. | If captive's lover is free, they agree to defect to player PMC to guarantee captive's safety! |

---

## 10. Procedural Vendetta Incursions & Dynamic Ambush System

When the player embarks on tactical missions, the system evaluates all active nemeses ($V_i \ge 70$):

$$\mathcal{P}(\text{Ambush}) = \min\left(0.40, \; 0.05 + \sum_{k \in \text{Nemeses}} \left(\frac{V_k - 70}{100}\right) \times 0.15\right)$$

### 10.1 Ambush Mechanics
1. **Drop-Pod Atmospheric Insertion**: On Round 3 or 4 of an ongoing engagement, an emergency warning sirens the HUD: *"WARNING: UNIDENTIFIED DROP-POD TRAJECTORY DETECTED"*.
2. **The Nemesis Drops In**: The nemesis arrives in their signature mobile suit (e.g., Jax Vance in a modified `HYE-03 Hyena Reaver`).
3. **AI Threat Prioritization**: The Nemesis ignores generic objectives and concentrates 100% of weapon heat output against the player's designated command unit.

---

## 11. GameMaker Studio 2 Engine Architecture (Modern GML)

The relationship web, romances, friendships, and allegiance variance loop are managed by `obj_NemesisManager`.

```
================================================================================
OBJECT: obj_NemesisManager (Persistent Singleton)
EVENT: Create_0
================================================================================
/// @description Initialize Relational Graph & Roster Database
characters_map = {};
active_nemeses = [];
prisoner_list  = [];

// Ingest master 204-character database
var _file_path = working_directory + "datafiles/characters_roster.json";
if (file_exists(_file_path)) {
    var _json_string = file_text_read_all(_file_path);
    var _data = json_parse(_json_string);
    var _chars = _data.characters;
    for (var i = 0; i < array_length(_chars); i++) {
        var _c = _chars[i];
        variable_struct_set(characters_map, _c.id, _c);
    }
}
```

```
================================================================================
SCRIPT: scr_check_romance_trauma(casualty_id, killer_id)
================================================================================
/// @description Checks and applies heartbreak trauma to surviving lovers
function scr_check_romance_trauma(_casualty_id, _killer_id) {
    if (!variable_struct_exists(obj_NemesisManager.characters_map, _casualty_id)) exit;
    var _casualty = variable_struct_get(obj_NemesisManager.characters_map, _casualty_id);
    
    var _rom = _casualty.love_interest;
    if (is_struct(_rom) && variable_struct_exists(_rom, "target_id")) {
        var _lover_id = _rom.target_id;
        if (variable_struct_exists(obj_NemesisManager.characters_map, _lover_id)) {
            var _lover = variable_struct_get(obj_NemesisManager.characters_map, _lover_id);
            if (!_lover.is_alive) exit;
            
            // Apply massive emotional spike
            _lover.morale = 0;
            _lover.grudge_toward_player = min(100, _lover.grudge_toward_player + (75 * _rom.grudge_multiplier));
            _lover.combat_trauma_mode = _rom.trauma_reaction;
            
            // Force Nemesis Declaration
            array_push(obj_NemesisManager.active_nemeses, _lover.id);
            show_debug_message("HEARTBREAK VENDETTA: " + _lover.name + " declared blood revenge for lover " + _casualty.name);
        }
    }
}
```

---

## 12. Lead QA Static Edge Case & Safety Verification

The Lead QA Engineer and Static Analyzer define strict architectural constraints to ensure engine stability and memory safety:

| Edge Case Risk | Technical Vulnerability | QA Rule & Defensive Implementation |
| :--- | :--- | :--- |
| **Faction Pool Starvation** | Procedural variance rolls could leave a faction with zero recruitable pilots. | Faction quota clamp: Every major faction is guaranteed at least 20 recruitable pilots per playthrough. |
| **Cyclic Grudge Cascades** | Pilot A hates Pilot B, Pilot B hates Pilot A; death loops into reciprocal infinite events. | Event propagation depth is capped at $\text{depth} = 1$. Grudge updates only evaluate direct first-degree neighbors. |
| **Orphaned Struct Pointers** | Character $K$ dies, but other structs hold memory references to undefined instances. | Graph nodes are never deleted from memory; `is_alive = false` flags preserve structural graph integrity. |
| **Cascade Mutiny Lockout** | Player executes an enemy ace, causing all hired PMC pilots to mutiny simultaneously in one turn. | Mutiny checks require an internal threshold check ($\text{Morale} < 10$) and roll against a dampener curve; maximum 1 mutiny event per 4 turns. |
| **Memory Leaks in Graph Traversal** | Iterating over 204 struct keys using dynamic string arrays creates heap fragmentation. | Use static arrays `character_id_list` pre-cached in `Create_0`, eliminating runtime dynamic key allocations. |
| **Infinite Ambush Loops** | A vendetta pilot dies, another declares vendetta, ambushing on every consecutive mission. | Cooldown timer: Minimum $3\text{ missions}$ between procedural drop-pod nemesis incursions. |

---

## 13. Future Implementation Roadmap & Milestones

```
Phase 1: Conceptual Brief & Character Web Specification (Current - Doc 19)
Phase 2: Master Datafiles JSON Registry (datafiles/characters_roster.json - 204 Figures)
Phase 3: GML Architecture & Manager Integration (obj_NemesisManager & scr_nemesis_dispatcher)
Phase 4: Procedural Drop-Pod Ambush Incursion in Isometric Combat (obj_BattleManager)
Phase 5: Layered Dynamic Portrait Compositor HUD & Comms Terminal
```

This specification completes the comprehensive technical, architectural, artistic, and narrative foundation for the **Pilot Nemesis & Relational Character Web System**.
""")

print(f"✓ Successfully wrote Document 19 to: {DOC_PATH}")
print(f"✓ File size: {os.path.getsize(DOC_PATH)} bytes")
