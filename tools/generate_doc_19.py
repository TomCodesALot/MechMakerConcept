#!/usr/bin/env python3
"""
tools/generate_doc_19.py
Assembles and writes the complete Document 19:
Pilot Nemesis System & Dynamic Character Relationship Web
with Front Mission SNES Visual Design Bible & Complete 204-Character Database.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROSTER_PATH = os.path.join(BASE_DIR, "datafiles", "characters_roster.json")
DOC_PATH = os.path.join(BASE_DIR, "docs", "19_pilot_nemesis_system_and_character_relationships.md")

with open(ROSTER_PATH, "r") as f:
    roster_data = json.load(f)

characters = roster_data["characters"]

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

def build_pilot_table(faction_id):
    f_chars = [c for c in characters if c["faction_id"] == faction_id and c["is_recruitable"]]
    lines = [
        "| ID & Callsign | Full Name | Tier | Preferred MS | Combat & Personality Traits | Hiring / Salary | Kinship & Relational Ties |",
        "| :--- | :--- | :---: | :---: | :--- | :---: | :--- |"
    ]
    for c in f_chars:
        cid = f"`{c['id']}`<br>**\"{c['callsign']}\"**"
        name = c["name"]
        tier = f"**T{c['tier']}**"
        ms = f"`{c['preferred_chassis']}`"
        traits = ", ".join([f"`{t}`" for t in c.get("traits", [])])
        cost = f"**{c['hiring_cost_cr']:,} Cr**<br>({c['salary_per_cycle_cr']:,}/cyc)"
        conn = get_connections_str(c)
        lines.append(f"| {cid} | {name} | {tier} | {ms} | {traits} | {cost} | {conn} |")
    return "\n".join(lines)

def build_vip_table(faction_id):
    f_chars = [c for c in characters if c["faction_id"] == faction_id and not c["is_recruitable"]]
    lines = [
        "| ID & Name | Title & Planetary Role | Dynasty | Relational Ties | Narrative Dossier & Elimination Consequence |",
        "| :--- | :--- | :---: | :--- | :--- |"
    ]
    for c in f_chars:
        cid = f"`{c['id']}`<br>**{c['name']}**"
        role = c["role"]
        dynasty = f"**{c.get('family_dynasty')}**" if c.get('family_dynasty') else "*Non-Dynastic*"
        conn = get_connections_str(c)
        bio = c.get("bio", "").replace("\n", " ")
        lines.append(f"| {cid} | {role} | {dynasty} | {conn} | {bio} |")
    return "\n".join(lines)

with open(DOC_PATH, "w") as out:
    out.write(r"""# Document 19: Pilot Nemesis System & Dynamic Character Relationship Web
**Document Version:** 1.1.0  
**Target Systems:** GameMaker Studio 2 (Modern GML), Datafiles JSON Pipeline (`datafiles/characters_roster.json`)  
**Inspirational Benchmarks:** *Middle-earth: Shadow of Mordor / War* (Monolith Nemesis System), *Front Mission 1/3/5* (Square / SNES 1995), *BattleTech*, *Crusader Kings III*  
**Authors & Contributors:** Lead Systems Architect (Lead Dev), Lead Game Designer (Director GDD), Lead Narrative Designer, Lead QA Engineer, Technical Art Director

---

## 1. Executive Summary & Core Philosophical Pillars

In *MechMakerConcept*, mobile suits are mechanical manifestations of geopolitical mass destruction, but human agency pulls the triggers. The **Pilot Nemesis & Relational Character Web System** elevates tactical isometric battles and base management into a high-stakes, consequences-driven human drama.

Characters—ranging from supreme planetary directors and fleet commodores to mercenary aces, trench grunts, and recruited PMC rookies—are not disposable stat-blocks. They belong to a **living directed relationship multi-graph** anchored by bloodlines, mentorship bonds, ideological loyalties, and bitter grudges.

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
                    /                   |                  \
                   v                    v                   v
           [Blood Vendettas]   [Hostage Ransoms]   [Faction Embargoes]
           (Kin / Wingmen)    (Faction Bargains)  (Market Penalties)
                   |                    |                   |
                   v                    v                   v
           [Dynamic Ambushes]  [Pilot Defections]  [Contract Lockouts]
           (In-Battle Drops)   (Recruitment Ops)   (Geopolitical Shift)
```

### 1.1 Core Design Directives
1. **Consequences Have Faces**: If the player obliterates an enemy ace in combat or orders the execution of an imprisoned general, their kin, wingmen, and pupils will actively retaliate.
2. **The Monolith Loop**: Defeated pilots who survive cockpit breaches do not vanish; they acquire cybernetic prosthetics, facial scars, dynamic traits (`vendetta_sworn`, `fear_of_artillery`), and track down the player's strike teams.
3. **Dynastic Feuds**: Major families span multiple factions. House Vance holds planetary power in the Terran Coalition while its disowned prodigal son Jax 'Jackal' Vance commands the Syndicate Reavers.
4. **Front Mission (SNES) Visual Authenticity**: All character portraits adhere strictly to the 16-bit Super Nintendo *Front Mission 1 (1995)* aesthetic backdrop: 64x64 pixel busts, high-contrast dithered shading, aviator comm headsets with boom mics, and high-collar flak jackets.

---

## 2. Mathematical Relationship Graph & Grudge Calculus

The game universe models all 204 figures as nodes within a directed multi-graph:
$$\mathcal{G} = (\mathcal{V}, \mathcal{E})$$

Where each node $v_i \in \mathcal{V}$ represents a character, and each directed edge $e_{ij} = (v_i, v_j, \tau, \omega) \in \mathcal{E}$ represents a relationship of type $\tau$ with weight $\omega$.

### 2.1 Character State Vector
Each character struct in GameMaker maintains dynamic emotional variables:
$$\mathbf{S}_i = \begin{bmatrix} A_{i,\text{player}} \\ V_{i,\text{player}} \\ L_{i,\text{faction}} \\ F_{i,\text{player}} \\ M_i \end{bmatrix} = \begin{bmatrix} \text{Affinity toward Player} \in [-100, 100] \\ \text{Vendetta / Grudge Level} \in [0, 100] \\ \text{Faction Loyalty} \in [0, 100] \\ \text{Fear of Player} \in [0, 100] \\ \text{Morale} \in [0, 100] \end{bmatrix}$$

### 2.2 Grudge Propagation Calculus
When Character $K$ is killed, executed, or maimed by the player, a ripple event dispatches through all incident edges $e_{jK} \in \mathcal{E}$ targeting neighbor characters $j$:

$$\Delta V_j = \min\left(100, \; \Delta V_j + (B_{\text{severity}} \times K_{\text{kinship}} \times I_{\text{closeness}})\right)$$

$$\Delta A_j = \max\left(-100, \; \Delta A_j - (B_{\text{severity}} \times K_{\text{kinship}} \times 1.25)\right)$$

Where:
- $B_{\text{severity}}$: Base severity index (Combat Kill: $+30$, Core Meltdown Incineration: $+45$, Formal Execution in Prison: $+75$).
- $K_{\text{kinship}}$: Relationship multiplier:
  - Parent / Child / Spouse: $\times 2.50$
  - Sibling / Twin: $\times 2.00$
  - Sworn Wingman / Mentor / Protégé: $\times 1.80$
  - Extended Family (Cousin, In-Law, Uncle): $\times 1.30$
  - Faction Comrade / Fellow Unit Member: $\times 1.00$
- $I_{\text{closeness}}$: Ideological alignment modifier ($1.0$ for loyalist, $0.5$ for estranged).

### 2.3 The Vendetta Threshold
When a character's grudge exceeds the critical trigger:
$$V_{j,\text{player}} \ge 70$$

Character $j$ enters the **`STATE_NEMESIS_ACTIVE`** mode:
1. They refuse all recruitment offers and break active employment contracts with the player's PMC.
2. They are flagged for **Procedural Drop-Pod Ambush Incursion** during the player's combat missions.
3. Their combat AI overrides default tactical routines to prioritize the player's flagship chassis.

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

### 3.3 Faction 16-Color Indexed Palettes
Each faction maintains an authentic 16-color retro palette:

```
[TERRAN COALITION]       : Olive Drab (#43523B), Khaki (#7C8068), Brass Eagle (#C69B3D), Cold Steel (#505860)
[OUTER COLONIES LEAGUE]  : Cobalt Navy (#1D3354), Pearl Silver (#9EADB8), Aristocratic Azure (#467599), Chrome (#E0E5E9)
[SYNDICATE RIM]          : Distressed Rust (#5C241C), Scrapper Leather (#684A36), Hazard Amber (#D4812B), Copper (#3B5B57)
[ZAIBATSU AEROSPACE]     : Matte Obsidian (#18191E), Carbon Weave (#2B2D35), Neon Cyan (#00F0FF), Magenta Monocle (#D6006E)
```

![SNES Faction Portraits Strip](assets/snes_faction_portraits_strip4_2x.png)
*Figure 3.1: Four-Faction Master Reference Strip at 2x Integer Scale (Terran Commander Vance, Colony Fleet Ace Cassian, Syndicate Reaver Jackal, Zaibatsu Cyber-Pilot Null-07).*

### 3.4 Dynamic Procedural Portrait Compositor (5-Layer Stack)
When a character survives catastrophic damage, shifts faction allegiance, or undergoes cybernetic surgery, the UI renders the bust through a 5-layer compositor:

```
+-------------------------------------------------------+
|            DYNAMIC PORTRAIT COMPOSITOR STACK          |
|                                                       |
|  Layer 5: [Faction Insignia / Kill Marks] (Top)       |
|  Layer 4: [Cybernetic Implants / Bionic Oculars]      |
|  Layer 3: [Battle Trauma, Shrapnel Scars & Burns]     |
|  Layer 2: [Facial Expression State / Emotion]         |
|  Layer 1: [Base Character Portrait Canvas] (Bottom)   |
+-------------------------------------------------------+
```

1. **Layer 1: Base Character Canvas**: Canonical 64x64 pilot face, hair, and uniform base.
2. **Layer 2: Expression Variation**: Neutral, Grim/Stoic, Enraged Snarl (activated against sworn nemesis), Defeated/Bandaged.
3. **Layer 3: Trauma Overlays**:
   - `spr_overlay_scar_shrapnel`: Ragged laceration across cheekbone and bridge of nose.
   - `spr_overlay_burn_plasma`: Dithered purple/charred tissue overlay across neck and jaw.
4. **Layer 4: Cybernetic Overlays**:
   - `spr_overlay_optic_tachyon`: Glowing cyan ocular sensor assembly replacing right or left eye.
   - `spr_overlay_cranial_bracket`: Bolted neuro-interface rim along temples and brow.
5. **Layer 5: Faction & Retaliation Badges**:
   - Terran Brass Eagle, Colony Starburst, Syndicate Reaver Skull, Zaibatsu Hex-Node.

---

## 4. Universe Census & Dynastic Lineage Graphs

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

### 4.1 The Seven Major Interstellar Dynasties

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
- **The Vance Drama**: Jax 'Jackal' Vance stole an experimental Terran heavy rail-chassis and fled to the Syndicate Rim. General Vance considers him dead; Jax harbors a burning vendetta against his aunt for executing his father during the Callisto strikes.

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

## 5. Recruitable Pilot Registries (The 30 Recruitable Pilots per Faction)

Below are the complete dossiers for the **132 Recruitable Pilots** available for contract across the four warring powers and independent space.

### 5.1 Terran Coalition Pilot Corps (30 Recruitable Pilots)
The Terran Coalition fields heavy artillery specialists, trench-line biped aces, and stoic frontline veterans trained in attrition warfare.
""")

    out.write("\n" + build_pilot_table("faction_terran") + "\n\n---\n\n")

    out.write("### 5.2 Outer Colonies League Star-Legion (30 Recruitable Pilots)\n")
    out.write("The Colony League employs high-mobility thruster aces, particle beam snipers, and aristocratic duelists who dominate orbital dogfights.\n\n")
    out.write(build_pilot_table("faction_colony") + "\n\n---\n\n")

    out.write("### 5.3 Syndicate Rim Marauders & Rust Aces (30 Recruitable Pilots)\n")
    out.write("The Syndicate Rim fields reckless scrappers, ballistic brawlers, and survivalist raiders who excel at close-quarters kinetic ambush.\n\n")
    out.write(build_pilot_table("faction_syndicate") + "\n\n---\n\n")

    out.write("### 5.4 Zaibatsu Aerospace Cyber-Pilots & Test Aces (30 Recruitable Pilots)\n")
    out.write("Zaibatsu Aerospace deploys transhuman cyber-pilots hardwired via direct neural links to high-frequency tachyon mobile armors.\n\n")
    out.write(build_pilot_table("faction_zaibatsu") + "\n\n---\n\n")

    out.write("### 5.5 Independent Ronin & Legendary Mercenaries (12 Recruitable Pilots)\n")
    out.write("Factionless veterans, dishonored corporate deserters, and roaming combat aces available to the highest bidder.\n\n")
    out.write(build_pilot_table("independent") + "\n\n---\n\n")

    out.write(r"""## 6. High-Value Targets & Command Structures (The 72 VIPs)

The game features **72 Non-Recruitable VIPs and Military Leaders** (18 per major faction) who command fleets, govern orbital sectors, and fund military R&D. Eliminating or capturing them triggers massive geopolitical and relational shocks.

### 6.1 Terran Coalition High Command & Aristocracy (18 VIPs)
""")
    out.write(build_vip_table("faction_terran") + "\n\n---\n\n")

    out.write("### 6.2 Outer Colonies League High Council & Admiralty (18 VIPs)\n")
    out.write(build_vip_table("faction_colony") + "\n\n---\n\n")

    out.write("### 6.3 Syndicate Rim Cartel Barons & Smuggling Lords (18 VIPs)\n")
    out.write(build_vip_table("faction_syndicate") + "\n\n---\n\n")

    out.write("### 6.4 Zaibatsu Aerospace Board of Directors & Lead Researchers (18 VIPs)\n")
    out.write(build_vip_table("faction_zaibatsu") + "\n\n---\n\n")

    out.write(r"""## 7. The Monolith-Style Nemesis Dynamic Loop

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

### 7.1 Dynamic Combat Memories & Trait Gains
Surviving pilots record specific combat trauma flags in their `traits` array:
- **`core_breaker`**: Earned if the pilot successfully destroyed one of the player's mobile suits in a previous battle (+15% Kinetic damage vs player mechs).
- **`scarred_survivor`**: Earned when surviving an eject under 10% core integrity (Immune to battlefield panic morale penalties).
- **`artillery_phobia`**: Earned if their chassis was shredded by long-range artillery splash (-20% accuracy when receiving incoming indirect fire).
- **`vendetta_sworn`**: Earned if the player executed their family member or wingman (Ignores retreat orders; gains +25% melee damage).

### 7.2 Battlefield Dialogue Barks
When entering combat within sensor range of the player, a Nemesis triggers dedicated comms barks matching their history:
- **Surviving Ejection**: *"You thought that fusion flare incinerated me, mercenary? You only scorched away my mercy. Look at my face!"*
- **Avenge Kin (House Vance)**: *"You put Deborah Vance in the dirt. I don't care about Earth's treaty—your squad dies in this trench!"*
- **Avenge Wingman**: *"Cole was my flight lead. You took his wings—now I'm taking your core!"*

---

## 8. Prisoner Disposition, Interrogation & Diplomatic Hostages

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
| **Execute Prisoner** | Salvage experimental pilot cybernetics and personal gear. | Dispatches `EVENT_EXECUTION` to all kin ($+75\text{ Grudge}$). Triggers blood feuds and procedural ambushes. |
| **Ransom to Faction** | $+50,000$ to $+500,000\text{ Cr}$ depending on character Tier. | Faction Grudge reduced by $-15$. Captive returns to active enemy service. |
| **Recruit / Turn** | Converts skilled Ace into player roster. | Requires breaking loyalty via interrogation. May trigger retaliation from former faction comrades. |
| **Diplomatic Hostage** | Halts enemy incursions in specific sectors. | Faction cannot launch punitive planetary strikes while their VIP is held hostage. |

---

## 9. Procedural Vendetta Incursions & Dynamic Ambush System

When the player embarks on tactical missions, the system evaluates all active nemeses ($V_i \ge 70$):

$$\mathcal{P}(\text{Ambush}) = \min\left(0.40, \; 0.05 + \sum_{k \in \text{Nemeses}} \left(\frac{V_k - 70}{100}\right) \times 0.15\right)$$

### 9.1 Ambush Mechanics
1. **Drop-Pod Atmospheric Insertion**: On Round 3 or 4 of an ongoing engagement, an emergency warning sirens the HUD: *"WARNING: UNIDENTIFIED DROP-POD TRAJECTORY DETECTED"*.
2. **The Nemesis Drops In**: The nemesis arrives in their signature mobile suit (e.g., Jax Vance in a modified `HYE-03 Hyena Reaver`).
3. **AI Threat Prioritization**: The Nemesis ignores generic objectives and concentrates 100% of weapon heat output against the player's designated command unit.

---

## 10. GameMaker Studio 2 Engine Architecture (Modern GML)

The relationship web and nemesis dispatch loop are managed by the persistent singleton `obj_NemesisManager`.

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
SCRIPT: scr_nemesis_event_dispatch(victim_id, killer_id, event_type)
================================================================================
/// @description Dispatches relationship reactions across the graph
function scr_nemesis_event_dispatch(_victim_id, _killer_id, _event_type) {
    if (!variable_struct_exists(obj_NemesisManager.characters_map, _victim_id)) exit;
    
    var _victim = variable_struct_get(obj_NemesisManager.characters_map, _victim_id);
    _victim.is_alive = false;
    
    // Evaluate Kinship and Relational Ripple
    var _kin = _victim.kinship;
    for (var k = 0; k < array_length(_kin); k++) {
        var _edge = _kin[k];
        var _relative_id = _edge.target_id;
        
        if (variable_struct_exists(obj_NemesisManager.characters_map, _relative_id)) {
            var _relative = variable_struct_get(obj_NemesisManager.characters_map, _relative_id);
            if (!_relative.is_alive) continue;
            
            // Apply Grudge Calculus
            var _multiplier = (_edge.relation == "brother" || _edge.relation == "sister" || _edge.relation == "daughter" || _edge.relation == "son") ? 2.5 : 1.5;
            var _base_sev = (_event_type == "executed") ? 75 : 35;
            
            _relative.morale = max(0, _relative.morale - 25);
            
            // Check Vendetta Trigger
            if (_relative.tier >= 2) {
                array_push(obj_NemesisManager.active_nemeses, _relative.id);
                show_debug_message("VENDETTA DECLARED: " + _relative.name + " against player for death of " + _victim.name);
            }
        }
    }
}
```

---

## 11. Lead QA Static Edge Case & Safety Verification

The Lead QA Engineer and Static Analyzer define strict architectural constraints to ensure engine stability and memory safety:

| Edge Case Risk | Technical Vulnerability | QA Rule & Defensive Implementation |
| :--- | :--- | :--- |
| **Cyclic Grudge Cascades** | Pilot A hates Pilot B, Pilot B hates Pilot A; death loops into reciprocal infinite events. | Event propagation depth is capped at $\text{depth} = 1$. Grudge updates only evaluate direct first-degree neighbors. |
| **Orphaned Struct Pointers** | Character $K$ dies, but other structs hold memory references to undefined instances. | Graph nodes are never deleted from memory; `is_alive = false` flags preserve structural graph integrity. |
| **Cascade Mutiny Lockout** | Player executes an enemy ace, causing all hired PMC pilots to mutiny simultaneously in one turn. | Mutiny checks require an internal threshold check ($\text{Morale} < 10$) and roll against a dampener curve; maximum 1 mutiny event per 4 turns. |
| **Memory Leaks in Graph Traversal** | Iterating over 204 struct keys using dynamic string arrays creates heap fragmentation. | Use static arrays `character_id_list` pre-cached in `Create_0`, eliminating runtime dynamic key allocations. |
| **Infinite Ambush Loops** | A vendetta pilot dies, another declares vendetta, ambushing on every consecutive mission. | Cooldown timer: Minimum $3\text{ missions}$ between procedural drop-pod nemesis incursions. |

---

## 12. Future Implementation Roadmap & Milestones

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
