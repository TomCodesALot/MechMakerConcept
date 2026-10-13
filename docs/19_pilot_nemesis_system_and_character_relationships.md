# Document 19: Pilot Nemesis System & Dynamic Character Relationship Web
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

| ID & Callsign | Full Name | Tier | Preferred MS | Combat & Personality Traits | Hiring / Salary | Kinship & Relational Ties |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- |
| `pilot_terran_cole`<br>**"Breaker"** | Lt. Marcus Cole | **T3** | `GHA-07` | `vanguard_shield`, `guardian_protector`, `iron_grit` | **120,000 Cr**<br>(7,500/cyc) | Wingman: `terran_rostova`<br>Mentor: `terran_vance`<br>Rival: `syndicate_jackal` |
| `pilot_terran_rostova`<br>**"Sparrow"** | Ensign Elena Rostova | **T1** | `TCM-03` | `high_agility`, `eagle_optic`, `family_debt` | **35,000 Cr**<br>(2,200/cyc) | Wingman: `terran_cole`<br>Mentor: `terran_cole`<br>Rival: `colony_kira`<br>Sibling: `terran_rostova` |
| `pilot_terran_tyler_vance`<br>**"Bastion"** | Cadet Tyler Vance | **T1** | `TCM-03` | `hothead`, `reckless_bravery`, `noble_blood` | **40,000 Cr**<br>(2,400/cyc) | Wingman: `terran_claire_vance`<br>Mentor: `terran_cole`<br>Rival: `syndicate_jackal`<br>Dynasty member: `terran_vance` |
| `pilot_terran_lucas_sterling`<br>**"Goldfinger"** | Sub-Lt. Lucas Sterling | **T2** | `GHA-07B` | `ammo_saver`, `aristocratic_vanity`, `railgun_aim` | **75,000 Cr**<br>(4,800/cyc) | Wingman: `terran_cole` |
| `pilot_terran_tara_briggs`<br>**"Bunker-Buster"** | Lt. Tara Briggs | **T2** | `GHA-07` | `fortress_ram`, `explosive_expert` | **65,000 Cr**<br>(4,200/cyc) | Wingman: `terran_rostova`<br>Mentor: `terran_briggs`<br>Rival: `syndicate_nadia` |
| `pilot_terran_liam_oconnor`<br>**"Deadeye"** | Warrant Officer Liam O'Connor | **T2** | `GHA-07B` | `sniper_stance`, `cool_headed` | **70,000 Cr**<br>(4,500/cyc) | Wingman: `terran_cole`<br>Mentor: `terran_oconnor`<br>Rival: `zaibatsu_maya` |
| `pilot_terran_karl_vogel`<br>**"War-Pig"** | Sgt. Karl Vogel | **T2** | `GHA-07` | `trigger_happy`, `ballistic_saturation` | **55,000 Cr**<br>(3,800/cyc) | Mentor: `terran_cole`<br>Rival: `syndicate_skag` |
| `pilot_terran_anna_kovac`<br>**"Trench-Rat"** | Cpl. Anna Kovac | **T1** | `TCM-03` | `trench_cover_bonus`, `stubborn` | **32,000 Cr**<br>(2,000/cyc) | Wingman: `terran_rostova`<br>Mentor: `terran_cole` |
| `pilot_terran_dmitri_rostov`<br>**"Anvil"** | Sgt. Dmitri Rostov | **T2** | `TCM-03` | `shield_master`, `brotherly_protection` | **58,000 Cr**<br>(3,900/cyc) | Wingman: `terran_rostova`<br>Sibling: `terran_rostova` |
| `pilot_terran_sergei_volkov`<br>**"Iron Wolf"** | Lt. Sergei Volkov | **T3** | `GHA-07` | `pack_hunter`, `kinetic_penetrator` | **95,000 Cr**<br>(6,200/cyc) | Wingman: `terran_cole`<br>Mentor: `terran_vance`<br>Rival: `colony_sorren` |
| `pilot_terran_mira_chen`<br>**"Comet-Lock"** | Flight Officer Mira Chen | **T2** | `GHA-07` | `swarm_missile_specialist`, `calm_sensor` | **62,000 Cr**<br>(4,100/cyc) | Wingman: `terran_cole`<br>Rival: `zaibatsu_null07` |
| `pilot_terran_boris_kane`<br>**"Grave-Digger"** | Chief Warrant Kane | **T2** | `GHA-07B` | `indirect_fire_master`, `heavy_recoil_soak` | **68,000 Cr**<br>(4,400/cyc) | Mentor: `terran_briggs`<br>Rival: `syndicate_slag_tony` |
| `pilot_terran_claudia_lang`<br>**"Valkyrie-Zero"** | Cpl. Claudia Lang | **T1** | `TCM-03` | `high_mobility_aspiration`, `evasion_drill` | **38,000 Cr**<br>(2,500/cyc) | Wingman: `terran_rostova`<br>Mentor: `terran_rostova`<br>Rival: `colony_kira` |
| `pilot_terran_hans_richter`<br>**"Old Bastion"** | Master Sgt. Richter | **T3** | `TCM-03` | `impenetrable_guard`, `veteran_instinct` | **88,000 Cr**<br>(5,800/cyc) | Wingman: `terran_cole`<br>Mentor: `terran_vance` |
| `pilot_terran_veronica_frost`<br>**"Cold Iron"** | Lt. Veronica Frost | **T2** | `GHA-07` | `cryo_radiator_specialist`, `calm_under_fire` | **72,000 Cr**<br>(4,600/cyc) | Wingman: `terran_volkov`<br>Rival: `colony_aether_kai` |
| `pilot_terran_jake_murdock`<br>**"Grease-Monkey"** | Pvt. Jake Murdock | **T1** | `TCM-03` | `emergency_patch`, `jury_rig` | **30,000 Cr**<br>(1,900/cyc) | Wingman: `terran_anna_kovac` |
| `pilot_terran_sonia_reyes`<br>**"Scatter-Queen"** | Flight Lt. Sonia Reyes | **T2** | `GHA-07` | `point_blank_burst`, `aggressive_charge` | **64,000 Cr**<br>(4,200/cyc) | Wingman: `terran_karl_vogel`<br>Mentor: `terran_cole`<br>Rival: `syndicate_nadia` |
| `pilot_terran_arthur_pendleton`<br>**"Squire"** | Ensign Pendleton | **T1** | `TCM-03` | `protocol_follower`, `steady_hands` | **34,000 Cr**<br>(2,100/cyc) | Wingman: `terran_lucas_sterling`<br>Mentor: `terran_sterling` |
| `pilot_terran_igor_dubov`<br>**"Hammer-Head"** | Cpl. Igor Dubov | **T2** | `GHA-07` | `battering_ram`, `stun_specialist` | **56,000 Cr**<br>(3,700/cyc) | Wingman: `terran_karl_vogel`<br>Mentor: `terran_volkov`<br>Rival: `syndicate_jackal` |
| `pilot_terran_helena_braun`<br>**"Iron-Siege"** | Capt. Helena Braun | **T3** | `GHA-07B` | `battery_synchronizer`, `morale_beacon` | **92,000 Cr**<br>(6,000/cyc) | Wingman: `terran_claire_vance`<br>Mentor: `terran_vance`<br>Rival: `colony_sorren` |
| `pilot_terran_nathan_cross`<br>**"Bloodhound"** | Warrant Officer Cross | **T2** | `TCM-03` | `radar_lock_bonus`, `counter_ecm` | **59,000 Cr**<br>(3,900/cyc) | Wingman: `terran_rostova`<br>Rival: `zaibatsu_maya` |
| `pilot_terran_greta_hahn`<br>**"Iron-Sow"** | Sgt. Greta Hahn | **T2** | `GHA-07` | `reactive_armor_expert`, `damage_sponge` | **66,000 Cr**<br>(4,300/cyc) | Wingman: `terran_anna_kovac`<br>Mentor: `terran_hans_richter` |
| `pilot_terran_tomas_zima`<br>**"Spike"** | Cadet Tomas Zima | **T1** | `TCM-03` | `fearless_rookie`, `fast_reloader` | **31,000 Cr**<br>(2,000/cyc) | Wingman: `terran_tyler_vance`<br>Mentor: `terran_hans_richter` |
| `pilot_terran_beatrice_fallon`<br>**"Sky-Hammer"** | Lt. Beatrice Fallon | **T2** | `GHA-07` | `drop_pod_assault`, `kinetic_shock` | **71,000 Cr**<br>(4,700/cyc) | Wingman: `terran_cole`<br>Mentor: `terran_vance`<br>Rival: `colony_kira` |
| `pilot_terran_roland_vance`<br>**"Cast-Iron"** | Sub-Lt. Roland Vance | **T2** | `TCM-03` | `flak_screen_wall`, `family_pride` | **63,000 Cr**<br>(4,100/cyc) | Wingman: `terran_tyler_vance`<br>Mentor: `terran_julian_vance`<br>Rival: `syndicate_jackal`<br>Dynasty member: `terran_vance` |
| `pilot_terran_yulia_morozova`<br>**"Hail-Storm"** | Flight Officer Morozova | **T2** | `GHA-07` | `salvo_density`, `suppressive_rain` | **67,000 Cr**<br>(4,400/cyc) | Wingman: `terran_mira_chen`<br>Rival: `syndicate_nadia` |
| `pilot_terran_felix_grimm`<br>**"Bulldozer"** | Cpl. Felix Grimm | **T1** | `TCM-03` | `wall_crusher`, `close_range_blast` | **36,000 Cr**<br>(2,300/cyc) | Wingman: `terran_karl_vogel`<br>Mentor: `terran_tara_briggs` |
| `pilot_terran_nadine_ross`<br>**"Iron-Sentry"** | Lt. Nadine Ross | **T2** | `TCM-03` | `overwatch_reflexes`, `first_strike` | **61,000 Cr**<br>(4,000/cyc) | Wingman: `terran_rostova`<br>Mentor: `terran_briggs`<br>Rival: `zaibatsu_maya` |
| `pilot_terran_casper_lind`<br>**"Ghost-Echo"** | Pvt. Casper Lind | **T1** | `TCM-03` | `jamming_chaff`, `sensor_ghost` | **33,000 Cr**<br>(2,100/cyc) | Wingman: `terran_nathan_cross`<br>Rival: `zaibatsu_null07` |
| `pilot_terran_maxim_volk`<br>**"Dread-Walker"** | Captain Maxim Volk | **T3** | `TCX-11` | `dreadnought_presence`, `capital_rail_aim` | **110,000 Cr**<br>(7,200/cyc) | Wingman: `terran_cole`<br>Mentor: `terran_vance`<br>Rival: `colony_cassian` |

---

### 5.2 Outer Colonies League Star-Legion (30 Recruitable Pilots)
The Colony League employs high-mobility thruster aces, particle beam snipers, and aristocratic duelists who dominate orbital dogfights.

| ID & Callsign | Full Name | Tier | Preferred MS | Combat & Personality Traits | Hiring / Salary | Kinship & Relational Ties |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- |
| `pilot_colony_sorren`<br>**"Ghost of Sol"** | Sorren 'Ghost' Lin | **T3** | `OCM-09` | `invisible_flight`, `sniper_focus`, `chivalric_oath` | **125,000 Cr**<br>(7,800/cyc) | Wingman: `colony_kira`<br>Mentor: `colony_cassian`<br>Rival: `terran_cole`<br>Sibling: `colony_sorren` |
| `pilot_colony_kira`<br>**"Sun-Dancer"** | Kira Dahl | **T2** | `OCM-04` | `vector_drift`, `rapid_saber_flurry` | **65,000 Cr**<br>(4,200/cyc) | Wingman: `colony_sorren`<br>Mentor: `colony_sorren`<br>Rival: `terran_rostova` |
| `pilot_colony_erik_thorne`<br>**"Solar-Flare"** | Erik Thorne | **T2** | `OCA-07` | `beam_accelerator_boost`, `family_obligation` | **72,000 Cr**<br>(4,600/cyc) | Wingman: `colony_sorren`<br>Mentor: `colony_paul_thorne`<br>Rival: `terran_lucas_sterling`<br>Dynasty member: `colony_lyra` |
| `pilot_colony_rin_lin`<br>**"Stardust"** | Rin Lin | **T1** | `OCM-04` | `sensor_boost`, `agile_evasion` | **36,000 Cr**<br>(2,300/cyc) | Wingman: `colony_sorren`<br>Mentor: `colony_sorren`<br>Sibling: `colony_sorren` |
| `pilot_colony_julian_vane`<br>**"Falconet"** | Julian Vane | **T2** | `OCM-09` | `noble_fencing`, `high_accuracy_beam` | **78,000 Cr**<br>(4,900/cyc) | Wingman: `colony_sorren`<br>Mentor: `colony_cassian`<br>Rival: `terran_tyler_vance`<br>Dynasty member: `colony_cassian` |
| `pilot_colony_kai_aether`<br>**"Solar-Pulse"** | Kai Aether | **T2** | `OCM-09` | `beam_pulse_cadence`, `evasive_jink` | **68,000 Cr**<br>(4,400/cyc) | Wingman: `colony_kira`<br>Mentor: `colony_finch`<br>Rival: `terran_veronica_frost` |
| `pilot_colony_selene_voss`<br>**"Moon-Shadow"** | Selene Voss | **T2** | `OCM-04` | `chaff_specialist`, `stealth_skirmish` | **62,000 Cr**<br>(4,000/cyc) | Wingman: `colony_rin_lin`<br>Rival: `zaibatsu_null07` |
| `pilot_colony_tariq_mansoor`<br>**"Dervish"** | Tariq Mansoor | **T2** | `OCM-09` | `dual_wield_master`, `acrobatic_strike` | **74,000 Cr**<br>(4,700/cyc) | Wingman: `colony_kira`<br>Mentor: `colony_cassian`<br>Rival: `syndicate_jackal` |
| `pilot_colony_chloe_duval`<br>**"Starlight Arbalest"** | Chloe Duval | **T3** | `OCA-07` | `tachyon_lock`, `overcharge_beam` | **98,000 Cr**<br>(6,400/cyc) | Wingman: `colony_sorren`<br>Mentor: `colony_paul_thorne`<br>Rival: `terran_liam_oconnor` |
| `pilot_colony_milo_trent`<br>**"Zephyr"** | Milo Trent | **T1** | `OCM-04` | `hot_rod_thrusters`, `reckless_speed` | **34,000 Cr**<br>(2,200/cyc) | Mentor: `colony_finch`<br>Rival: `terran_tomas_zima` |
| `pilot_colony_orion_sol`<br>**"Corona"** | Orion Sol | **T3** | `OCX-15` | `transam_compatibility`, `singularity_harmonizer` | **115,000 Cr**<br>(7,500/cyc) | Wingman: `colony_sorren`<br>Mentor: `colony_cassian`<br>Rival: `terran_vance` |
| `pilot_colony_freja_lind`<br>**"Aegis-Angel"** | Freja Lind | **T2** | `OCM-09` | `thermal_siphon_shield`, `convoy_guardian` | **69,000 Cr**<br>(4,500/cyc) | Wingman: `colony_erik_thorne`<br>Mentor: `colony_lyra`<br>Rival: `terran_greta_hahn`<br>Sibling: `colony_sorren` |
| `pilot_colony_dante_mercer`<br>**"Star-Reaper"** | Dante Mercer | **T2** | `OCM-04` | `plasma_needle_master`, `weakpoint_strike` | **64,000 Cr**<br>(4,100/cyc) | Wingman: `colony_kai_aether`<br>Rival: `syndicate_skag` |
| `pilot_colony_astraea_vane`<br>**"Silver-Wing"** | Lady Astraea Vane | **T2** | `OCM-09` | `aristocratic_fencing`, `high_speed_turn` | **76,000 Cr**<br>(4,800/cyc) | Wingman: `colony_julian_vane`<br>Mentor: `colony_cassian`<br>Rival: `terran_claire_vance`<br>Dynasty member: `colony_cassian` |
| `pilot_colony_leo_drachen`<br>**"Comet-Tail"** | Leo Drachen | **T2** | `OCM-04` | `missile_barrage_agility`, `lock_break_drift` | **61,000 Cr**<br>(3,900/cyc) | Mentor: `colony_finch`<br>Rival: `terran_yulia_morozova` |
| `pilot_colony_nyx_callisto`<br>**"Eclipse"** | Nyx Callisto | **T3** | `OCM-09` | `active_camouflage`, `cold_thrusters` | **94,000 Cr**<br>(6,100/cyc) | Wingman: `colony_selene_voss`<br>Rival: `zaibatsu_maya` |
| `pilot_colony_valentin_roux`<br>**"Solar-Fencer"** | Valentin Roux | **T2** | `OCM-09` | `saber_counter_parry`, `graceful_footwork` | **71,000 Cr**<br>(4,600/cyc) | Wingman: `colony_tariq_mansoor`<br>Mentor: `colony_cassian`<br>Rival: `terran_igor_dubov` |
| `pilot_colony_jun_takahashi`<br>**"Ronin-Aether"** | Jun Takahashi | **T2** | `OCM-09` | `hybrid_doctrine`, `kinetic_deflector` | **67,000 Cr**<br>(4,300/cyc) | Wingman: `colony_sorren`<br>Rival: `zaibatsu_renzo` |
| `pilot_colony_esper_hale`<br>**"Sol-Warden"** | Esper Hale | **T1** | `OCM-04` | `habitat_loyalty`, `steady_defense` | **35,000 Cr**<br>(2,200/cyc) | Wingman: `colony_erik_thorne`<br>Mentor: `colony_lyra` |
| `pilot_colony_cyrus_vane`<br>**"Peregrine"** | Cyrus Vane | **T2** | `OCA-07` | `sniper_endurance`, `heat_management` | **75,000 Cr**<br>(4,800/cyc) | Wingman: `colony_chloe_duval`<br>Mentor: `colony_paul_thorne`<br>Rival: `terran_helen_braun`<br>Dynasty member: `colony_cassian` |
| `pilot_colony_talon_skye`<br>**"Wind-Walker"** | Talon Skye | **T2** | `OCM-04` | `high_boost_speed`, `tight_vector_turn` | **63,000 Cr**<br>(4,000/cyc) | Wingman: `colony_kira`<br>Mentor: `colony_finch`<br>Rival: `syndicate_nadia` |
| `pilot_colony_aurora_blake`<br>**"Solar-Flare-Two"** | Aurora Blake | **T1** | `OCM-04` | `rapid_fire_cadence`, `evasive_instinct` | **37,000 Cr**<br>(2,400/cyc) | Wingman: `colony_rin_lin`<br>Mentor: `colony_sorren` |
| `pilot_colony_gideon_cross`<br>**"Crucible"** | Gideon Cross | **T3** | `OCA-07` | `siege_penetration`, `radiator_wing_overdrive` | **96,000 Cr**<br>(6,200/cyc) | Wingman: `colony_chloe_duval`<br>Mentor: `colony_cassian`<br>Rival: `terran_maxim_volk` |
| `pilot_colony_lyra_junior`<br>**"Morning-Star"** | Lyra Thorne-Vane | **T1** | `OCM-04` | `sensor_network`, `diplomatic_immunity_hope` | **39,000 Cr**<br>(2,500/cyc) | Wingman: `colony_erik_thorne`<br>Mentor: `colony_lyra`<br>Dynasty member: `colony_cassian` |
| `pilot_colony_hugo_belmont`<br>**"Saber-Knight"** | Hugo Belmont | **T2** | `OCM-09` | `interceptor_bodyguard`, `honor_duel` | **73,000 Cr**<br>(4,700/cyc) | Wingman: `colony_julian_vane`<br>Mentor: `colony_cassian`<br>Rival: `terran_cole` |
| `pilot_colony_faye_valerie`<br>**"Super-Nova"** | Faye Valerie | **T2** | `OCM-09` | `burst_beam_specialist`, `overheat_risk_taker` | **69,000 Cr**<br>(4,400/cyc) | Wingman: `colony_kai_aether`<br>Mentor: `colony_paul_thorne`<br>Rival: `syndicate_marauder_rex` |
| `pilot_colony_damien_sinclair`<br>**"Void-Hound"** | Damien Sinclair | **T2** | `OCM-04` | `relentless_pursuit`, `zero_g_grapple` | **66,000 Cr**<br>(4,200/cyc) | Wingman: `colony_dante_mercer`<br>Mentor: `colony_finch`<br>Rival: `syndicate_jackal` |
| `pilot_colony_nadia_vane`<br>**"Silver-Arrow"** | Nadia Vane | **T1** | `OCM-04` | `high_altitude_optics`, `evasion_reflex` | **38,000 Cr**<br>(2,400/cyc) | Wingman: `colony_astraea_vane`<br>Mentor: `colony_cassian`<br>Dynasty member: `colony_cassian` |
| `pilot_colony_soren_kane`<br>**"Particle-Fist"** | Soren Kane | **T2** | `OCM-09` | `beam_saber_parry`, `close_range_blast` | **70,000 Cr**<br>(4,500/cyc) | Wingman: `colony_tariq_mansoor`<br>Mentor: `colony_sorren`<br>Rival: `terran_igor_dubov` |
| `pilot_colony_elysium_zero`<br>**"Trans-Am Phantom"** | Ace-01 Elysium | **T4** | `OCX-15` | `transam_apex`, `funnel_mastery`, `singularity_strike` | **140,000 Cr**<br>(9,200/cyc) | Wingman: `colony_sorren`<br>Mentor: `colony_cassian`<br>Rival: `zaibatsu_renzo` |

---

### 5.3 Syndicate Rim Marauders & Rust Aces (30 Recruitable Pilots)
The Syndicate Rim fields reckless scrappers, ballistic brawlers, and survivalist raiders who excel at close-quarters kinetic ambush.

| ID & Callsign | Full Name | Tier | Preferred MS | Combat & Personality Traits | Hiring / Salary | Kinship & Relational Ties |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- |
| `pilot_syndicate_nadia`<br>**"Spark"** | Nadia 'Spark' Ortiz | **T2** | `SCA-14` | `incendiary_slag_master`, `jury_rig_expert`, `explosive_temper` | **75,000 Cr**<br>(4,800/cyc) | Wingman: `syndicate_cruz`<br>Mentor: `syndicate_mateo_ortiz`<br>Rival: `terran_tara_briggs`<br>Dynasty member: `syndicate_mateo_ortiz` |
| `pilot_syndicate_jackal`<br>**"Jackal"** | Jax 'Jackal' Vance | **T3** | `SCR-12` | `hydraulic_claw_crush`, `blood_traitor_hate`, `reckless_fury` | **110,000 Cr**<br>(7,200/cyc) | Wingman: `syndicate_torval`<br>Mentor: `terran_vance`<br>Rival: `terran_cole`<br>Dynasty member: `syndicate_jackal` |
| `pilot_syndicate_rico_cruz`<br>**"Slick"** | Rico Cruz | **T2** | `SCR-05` | `hit_and_run_plunder`, `evasive_cockpit` | **58,000 Cr**<br>(3,800/cyc) | Wingman: `syndicate_cruz`<br>Mentor: `syndicate_tito_cruz`<br>Rival: `terran_lucas_sterling`<br>Dynasty member: `syndicate_cruz` |
| `pilot_syndicate_skag_tony`<br>**"Cinder"** | Tony 'Cinder' Varek | **T2** | `SCA-14` | `area_denial_fire`, `crucible_heat_soak` | **68,000 Cr**<br>(4,400/cyc) | Wingman: `syndicate_nadia`<br>Mentor: `syndicate_boss_varek`<br>Rival: `terran_boris_kane` |
| `pilot_syndicate_marauder_rex`<br>**"Guzzler"** | Rex 'Guzzler' Thorne | **T2** | `SCR-12` | `scattergun_shredder`, `fuel_thief` | **64,000 Cr**<br>(4,200/cyc) | Wingman: `syndicate_jackal`<br>Rival: `colony_faye_valerie` |
| `pilot_syndicate_gristle_pete`<br>**"Gristle"** | Pete 'Gristle' Murphy | **T1** | `SCR-05` | `cheap_repair`, `desperate_charge` | **28,000 Cr**<br>(1,800/cyc) | Mentor: `syndicate_skag_morgan`<br>Rival: `terran_jake_murdock` |
| `pilot_syndicate_val_fang`<br>**"Fang"** | Valeria 'Fang' Drachen | **T2** | `SCR-12` | `pincer_decapitator`, `armor_shredder` | **72,000 Cr**<br>(4,700/cyc) | Wingman: `syndicate_jackal`<br>Rival: `zaibatsu_maya` |
| `pilot_syndicate_rust_maggot`<br>**"Maggot"** | Mick 'Maggot' Doyle | **T1** | `SCR-05` | `debris_stealth`, `dirty_shot` | **31,000 Cr**<br>(2,000/cyc) | Wingman: `syndicate_rico_cruz`<br>Rival: `colony_milo_trent` |
| `pilot_syndicate_slik_talia`<br>**"Viper"** | Talia 'Viper' Vasquez | **T2** | `SCR-05` | `close_shrapnel_cone`, `toxic_exhaust` | **62,000 Cr**<br>(4,000/cyc) | Wingman: `syndicate_nadia`<br>Mentor: `syndicate_cruz`<br>Rival: `colony_kira` |
| `pilot_syndicate_baron_slag`<br>**"Gag-Order"** | Baron 'Gag' Gorman | **T3** | `SCX-19` | `stolen_rail_mastery`, `four_arm_grapple` | **105,000 Cr**<br>(6,800/cyc) | Wingman: `syndicate_jackal`<br>Mentor: `syndicate_torval`<br>Rival: `terran_maxim_volk` |
| `pilot_syndicate_scrappy_lou`<br>**"Scrappy"** | Lou 'Scrappy' Finch | **T1** | `SCR-05` | `salvage_bonus`, `quick_escape` | **33,000 Cr**<br>(2,100/cyc) | Wingman: `syndicate_rico_cruz` |
| `pilot_syndicate_hammer_fist_otto`<br>**"Sledge"** | Otto 'Sledge' Krupp | **T2** | `SCR-12` | `harpoon_tether`, `kinetic_pulverizer` | **66,000 Cr**<br>(4,300/cyc) | Wingman: `syndicate_nadia`<br>Mentor: `syndicate_mateo_ortiz`<br>Rival: `terran_igor_dubov` |
| `pilot_syndicate_katja_slit`<br>**"Razor"** | Katja 'Razor' Vane | **T2** | `SCR-05` | `serrated_cleaver_bleed`, `ruthless_parry` | **69,000 Cr**<br>(4,500/cyc) | Wingman: `syndicate_jackal`<br>Rival: `colony_julian_vane` |
| `pilot_syndicate_bones_mccoy`<br>**"Bone-Saw"** | Bones 'Doc' McCoy | **T2** | `SCR-12` | `cockpit_extraction`, `stim_injector` | **59,000 Cr**<br>(3,900/cyc) | Wingman: `syndicate_nadia`<br>Rival: `terran_nurse_clara` |
| `pilot_syndicate_blaze_keller`<br>**"Torch"** | Keller 'Torch' Brandt | **T2** | `SCA-14` | `thermite_spread`, `smoke_screen_evade` | **65,000 Cr**<br>(4,200/cyc) | Wingman: `syndicate_skag_tony`<br>Mentor: `syndicate_mateo_ortiz`<br>Rival: `terran_veronica_frost` |
| `pilot_syndicate_grease_pit_dan`<br>**"Oiler"** | Dan 'Oiler' Kowalski | **T1** | `SCR-05` | `fission_overclock`, `reckless_boost` | **35,000 Cr**<br>(2,200/cyc) | Wingman: `syndicate_rico_cruz` |
| `pilot_syndicate_cinder_clara`<br>**"Sparky"** | Clara 'Sparky' Cruz | **T1** | `SCR-05` | `shrapnel_barrage_spotting`, `kin_loyalty` | **37,000 Cr**<br>(2,400/cyc) | Wingman: `syndicate_nadia`<br>Mentor: `syndicate_cruz`<br>Dynasty member: `syndicate_cruz` |
| `pilot_syndicate_diesel_dave`<br>**"Diesel"** | Dave 'Diesel' O'Malley | **T2** | `SCR-12` | `ramming_prowess`, `hydraulic_torque` | **58,000 Cr**<br>(3,800/cyc) | Mentor: `syndicate_boss_varek`<br>Rival: `terran_felix_grimm` |
| `pilot_syndicate_siren_zara`<br>**"Siren"** | Zara 'Siren' Vance | **T2** | `SCR-05` | `frequency_screamer`, `jamming_static` | **71,000 Cr**<br>(4,600/cyc) | Wingman: `syndicate_jackal`<br>Mentor: `syndicate_jackal`<br>Rival: `terran_vance`<br>Dynasty member: `syndicate_jackal` |
| `pilot_syndicate_junk_king_armin`<br>**"Junk-King"** | Armin 'Junk-King' Vogel | **T3** | `SCR-12` | `tungsten_slag_armor`, `brutal_intimidation` | **89,000 Cr**<br>(5,800/cyc) | Wingman: `syndicate_nadia`<br>Mentor: `syndicate_cruz`<br>Rival: `terran_sergei_volkov` |
| `pilot_syndicate_molten_mike`<br>**"Ladle"** | Mike 'Ladle' Thorne | **T2** | `SCA-14` | `fast_crucible_feed`, `burn_resistance` | **63,000 Cr**<br>(4,100/cyc) | Wingman: `syndicate_nadia`<br>Mentor: `syndicate_mateo_ortiz`<br>Rival: `colony_erik_thorne` |
| `pilot_syndicate_grudge_boris`<br>**"Grudge"** | Boris 'Grudge' Volkov | **T2** | `SCR-12` | `blood_feud_rage`, `heavy_recoil_endure` | **67,000 Cr**<br>(4,400/cyc) | Wingman: `syndicate_jackal`<br>Rival: `terran_sergei_volkov` |
| `pilot_syndicate_tinkerer_pip`<br>**"Sprocket"** | Pip 'Sprocket' Chen | **T1** | `SCR-05` | `hotwire_avionics`, `sensor_glitch` | **38,000 Cr**<br>(2,500/cyc) | Wingman: `syndicate_nadia`<br>Rival: `zaibatsu_null07` |
| `pilot_syndicate_gutter_rat_sam`<br>**"Gutter"** | Sam 'Gutter' Higgins | **T1** | `SCR-05` | `crawlspace_ambush`, `shrapnel_burst` | **29,000 Cr**<br>(1,900/cyc) | Mentor: `syndicate_skag_morgan` |
| `pilot_syndicate_reaver_elena`<br>**"Banshee"** | Elena 'Banshee' Cruz | **T2** | `SCR-05` | `hull_breacher`, `fearless_pirate` | **68,000 Cr**<br>(4,400/cyc) | Wingman: `syndicate_rico_cruz`<br>Mentor: `syndicate_cruz`<br>Rival: `terran_rostova`<br>Dynasty member: `syndicate_cruz` |
| `pilot_syndicate_salvage_queen_mira`<br>**"Vulture"** | Mira 'Vulture' Sterling | **T2** | `SCR-12` | `part_harvest_bonus`, `chassis_strip_expert` | **70,000 Cr**<br>(4,600/cyc) | Wingman: `syndicate_cruz`<br>Rival: `terran_sterling` |
| `pilot_syndicate_iron_tusk_kurt`<br>**"Tusk"** | Kurt 'Tusk' Bauer | **T2** | `SCR-12` | `ram_shockwave`, `heavy_frontal_plate` | **66,000 Cr**<br>(4,300/cyc) | Wingman: `syndicate_jackal`<br>Mentor: `syndicate_torval`<br>Rival: `terran_karl_vogel` |
| `pilot_syndicate_rust_hound_ned`<br>**"Hound"** | Ned 'Hound' Kelly | **T1** | `SCR-05` | `heat_signature_tracker`, `relentless_scent` | **34,000 Cr**<br>(2,200/cyc) | Wingman: `syndicate_nadia` |
| `pilot_syndicate_mad_dog_rocco`<br>**"Mad-Dog"** | Rocco 'Mad-Dog' Rossi | **T2** | `SCR-12` | `point_blank_flak`, `berserk_rage` | **65,000 Cr**<br>(4,200/cyc) | Wingman: `syndicate_jackal`<br>Mentor: `syndicate_torval`<br>Rival: `terran_sonia_reyes` |
| `pilot_syndicate_apex_chimera_dread`<br>**"Apex Corsair"** | Captain 'Wreckage' Torval | **T4** | `SCX-19` | `four_arm_annihilation`, `stolen_rail_battery`, `pirate_terror` | **135,000 Cr**<br>(8,900/cyc) | Wingman: `syndicate_jackal`<br>Mentor: `syndicate_torval`<br>Rival: `terran_vance`<br>Dynasty member: `syndicate_torval` |

---

### 5.4 Zaibatsu Aerospace Cyber-Pilots & Test Aces (30 Recruitable Pilots)
Zaibatsu Aerospace deploys transhuman cyber-pilots hardwired via direct neural links to high-frequency tachyon mobile armors.

| ID & Callsign | Full Name | Tier | Preferred MS | Combat & Personality Traits | Hiring / Salary | Kinship & Relational Ties |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- |
| `pilot_zaibatsu_null07`<br>**"Neural-Zero"** | Null-07 (Ren) | **T3** | `ZX-22` | `zero_latency_synapse`, `quantum_blade_mastery`, `fractured_memory` | **130,000 Cr**<br>(8,200/cyc) | Wingman: `zaibatsu_maya`<br>Mentor: `zaibatsu_vivienne`<br>Rival: `colony_sorren` |
| `pilot_zaibatsu_maya`<br>**"Kestrel"** | Maya 'Kestrel' Zhao | **T3** | `ZM-11` | `plasma_katana_crit`, `stealth_baffle_ambush`, `code_of_bushido` | **100,000 Cr**<br>(6,500/cyc) | Wingman: `zaibatsu_null07`<br>Mentor: `zaibatsu_kaito_mori`<br>Rival: `colony_helmut_zhao` |
| `pilot_zaibatsu_kenji_sato`<br>**"Razor-Edge"** | Kenji Sato | **T2** | `ZM-11` | `critical_hit_boost`, `optical_cloak_expert` | **72,000 Cr**<br>(4,600/cyc) | Wingman: `zaibatsu_maya`<br>Mentor: `zaibatsu_kaito_mori`<br>Rival: `terran_sergei_volkov` |
| `pilot_zaibatsu_hana_mori`<br>**"Vibro-Fang"** | Hana Mori | **T2** | `ZM-06` | `rapid_pdw_burst`, `parry_riposte` | **65,000 Cr**<br>(4,200/cyc) | Wingman: `zaibatsu_maya`<br>Mentor: `zaibatsu_kaito_mori`<br>Rival: `colony_valentin_roux`<br>Dynasty member: `zaibatsu_kaito_mori` |
| `pilot_zaibatsu_unit_14_echo`<br>**"Echo-Pulse"** | Unit-14 (Echo) | **T2** | `ZM-06` | `reflex_overclock`, `synthetic_pain_block` | **62,000 Cr**<br>(4,000/cyc) | Wingman: `zaibatsu_null07`<br>Mentor: `zaibatsu_vivienne`<br>Rival: `terran_claudia_lang` |
| `pilot_zaibatsu_raiden_kenta`<br>**"Volt-Sniper"** | Kenta Raiden | **T3** | `ZMA-15` | `helium_cooled_sniper`, `bipod_lock_perfection` | **105,000 Cr**<br>(6,800/cyc) | Wingman: `zaibatsu_maya`<br>Mentor: `zaibatsu_renzo`<br>Rival: `terran_liam_oconnor` |
| `pilot_zaibatsu_ayako_shimizu`<br>**"Ghost-Wire"** | Ayako Shimizu | **T2** | `ZM-11` | `radar_absorb_matrix`, `ecm_scramble` | **69,000 Cr**<br>(4,400/cyc) | Wingman: `zaibatsu_kenji_sato`<br>Rival: `colony_selene_voss` |
| `pilot_zaibatsu_ryo_kurata`<br>**"Plasma-Burn"** | Ryo Kurata | **T2** | `ZM-11` | `plasma_salvo_burst`, `high_temp_dissipation` | **68,000 Cr**<br>(4,300/cyc) | Mentor: `zaibatsu_renzo`<br>Rival: `terran_sonia_reyes` |
| `pilot_zaibatsu_subject_09_kai`<br>**"Mind-Shatter"** | Subject-09 (Kai) | **T2** | `ZM-06` | `berserk_synapse`, `suicidal_charge` | **64,000 Cr**<br>(4,100/cyc) | Wingman: `zaibatsu_null07`<br>Mentor: `zaibatsu_vivienne`<br>Rival: `syndicate_mad_dog_rocco` |
| `pilot_zaibatsu_shizuka_takahashi`<br>**"Black-Lotus"** | Shizuka Takahashi | **T2** | `ZM-11` | `viper_strike`, `executive_bodyguard` | **76,000 Cr**<br>(4,900/cyc) | Wingman: `zaibatsu_ayumi_takahashi`<br>Mentor: `zaibatsu_renzo`<br>Rival: `colony_astraea_vane`<br>Dynasty member: `zaibatsu_renzo` |
| `pilot_zaibatsu_daiki_endo`<br>**"Tachyon-Edge"** | Daiki Endo | **T3** | `ZX-22` | `tachyon_blade_dance`, `vernier_phase_shift` | **112,000 Cr**<br>(7,400/cyc) | Wingman: `zaibatsu_null07`<br>Mentor: `zaibatsu_renzo`<br>Rival: `colony_tariq_mansoor` |
| `pilot_zaibatsu_chiyo_noda`<br>**"Viper-PDW"** | Chiyo Noda | **T1** | `ZM-06` | `caseless_ammo_cadence`, `urban_sweep` | **36,000 Cr**<br>(2,300/cyc) | Wingman: `zaibatsu_hana_mori`<br>Mentor: `zaibatsu_kaito_mori`<br>Rival: `terran_arthur_pendleton` |
| `pilot_zaibatsu_kazuo_miura`<br>**"Iron-Baffle"** | Kazuo Miura | **T2** | `ZM-11` | `composite_carbon_plate`, `stun_baton_melee` | **67,000 Cr**<br>(4,300/cyc) | Wingman: `zaibatsu_kenji_sato`<br>Rival: `terran_hans_richter` |
| `pilot_zaibatsu_reiko_honda`<br>**"Shadow-Sniper"** | Reiko Honda | **T2** | `ZMA-15` | `thermal_decoy_specialist`, `camo_baffle` | **73,000 Cr**<br>(4,700/cyc) | Wingman: `zaibatsu_raiden_kenta`<br>Mentor: `zaibatsu_renzo`<br>Rival: `colony_chloe_duval` |
| `pilot_zaibatsu_shin_kuroda`<br>**"Gilded-Edge"** | Shin Kuroda | **T2** | `ZM-06` | `corporate_arrogance`, `finely_tuned_servos` | **74,000 Cr**<br>(4,800/cyc) | Mentor: `zaibatsu_shiro_kuroda`<br>Rival: `terran_lucas_sterling`<br>Dynasty member: `zaibatsu_shiro_kuroda` |
| `pilot_zaibatsu_yuki_nagata`<br>**"Cryo-Baffle"** | Yuki Nagata | **T2** | `ZMA-15` | `sub_zero_radiator`, `continuous_fire` | **66,000 Cr**<br>(4,200/cyc) | Wingman: `zaibatsu_raiden_kenta`<br>Mentor: `zaibatsu_vivienne`<br>Rival: `terran_veronica_frost` |
| `pilot_zaibatsu_tetsuo_araki`<br>**"Nanite-Fist"** | Tetsuo Araki | **T2** | `ZM-06` | `monomolecular_grip`, `hydraulic_snap` | **63,000 Cr**<br>(4,000/cyc) | Wingman: `zaibatsu_unit_14_echo`<br>Mentor: `zaibatsu_jin_chen`<br>Rival: `syndicate_hammer_fist_otto` |
| `pilot_zaibatsu_naomi_inada`<br>**"Strobe-Flash"** | Naomi Inada | **T1** | `ZM-06` | `flashbang_mortar_bonus`, `sensor_blind` | **35,000 Cr**<br>(2,200/cyc) | Wingman: `zaibatsu_chiyo_noda`<br>Rival: `colony_esper_hale` |
| `pilot_zaibatsu_genta_okada`<br>**"Black-Tide"** | Genta Okada | **T2** | `ZM-11` | `pdw_saturation`, `close_in_defense` | **64,000 Cr**<br>(4,100/cyc) | Mentor: `zaibatsu_kaito_mori`<br>Rival: `terran_karl_vogel` |
| `pilot_zaibatsu_sayaka_mori`<br>**"Razor-Silk"** | Sayaka Mori | **T2** | `ZM-11` | `monowire_trap`, `tactical_snare` | **71,000 Cr**<br>(4,500/cyc) | Wingman: `zaibatsu_maya`<br>Mentor: `zaibatsu_kaito_mori`<br>Rival: `syndicate_val_fang`<br>Dynasty member: `zaibatsu_kaito_mori` |
| `pilot_zaibatsu_toru_matsuda`<br>**"Data-Siphon"** | Toru Matsuda | **T2** | `ZM-06` | `target_telemetry_share`, `neural_uplink` | **61,000 Cr**<br>(3,900/cyc) | Wingman: `zaibatsu_ayako_shimizu`<br>Mentor: `zaibatsu_vivienne`<br>Rival: `terran_casper_lind` |
| `pilot_zaibatsu_madoka_kitano`<br>**"Tachyon-Ghost"** | Madoka Kitano | **T3** | `ZX-22` | `zero_point_shift`, `neural_drone_swarm` | **115,000 Cr**<br>(7,600/cyc) | Wingman: `zaibatsu_null07`<br>Mentor: `zaibatsu_renzo`<br>Rival: `colony_nyx_callisto` |
| `pilot_zaibatsu_isamu_toba`<br>**"Bio-Shock"** | Isamu Toba | **T2** | `ZM-06` | `emp_disruptor_specialist`, `reactor_scramble` | **65,000 Cr**<br>(4,200/cyc) | Wingman: `zaibatsu_kenji_sato`<br>Rival: `terran_veronica_frost` |
| `pilot_zaibatsu_mariko_asano`<br>**"Executive-Blade"** | Mariko Asano | **T2** | `ZM-11` | `dueling_etiquette`, `monomolecular_crit` | **70,000 Cr**<br>(4,500/cyc) | Wingman: `zaibatsu_maya`<br>Mentor: `zaibatsu_kaito_mori`<br>Rival: `colony_valentin_roux` |
| `pilot_zaibatsu_zenjiro_ohta`<br>**"Cyber-Vanguard"** | Zenjiro Ohta | **T2** | `ZM-11` | `aggressive_blade_rush`, `armor_piercing_plasma` | **67,000 Cr**<br>(4,300/cyc) | Wingman: `zaibatsu_kazuo_miura`<br>Mentor: `zaibatsu_kaito_mori`<br>Rival: `terran_cole` |
| `pilot_zaibatsu_fubuki_takahashi`<br>**"Cold-Lotus"** | Fubuki Takahashi | **T1** | `ZM-06` | `family_pride`, `disciplined_aim` | **38,000 Cr**<br>(2,400/cyc) | Wingman: `zaibatsu_shizuka_takahashi`<br>Mentor: `zaibatsu_renzo`<br>Rival: `terran_tyler_vance`<br>Dynasty member: `zaibatsu_renzo` |
| `pilot_zaibatsu_gen_kudo`<br>**"Chrome-Fang"** | Gen Kudo | **T2** | `ZM-06` | `hydraulic_kick`, `vibro_blade_rend` | **62,000 Cr**<br>(4,000/cyc) | Wingman: `zaibatsu_tetsuo_araki`<br>Mentor: `zaibatsu_jin_chen`<br>Rival: `syndicate_katja_slit` |
| `pilot_zaibatsu_erika_nomura`<br>**"Plasma-Whip"** | Erika Nomura | **T2** | `ZM-11` | `continuous_beam_whip`, `thermal_stress` | **69,000 Cr**<br>(4,400/cyc) | Wingman: `zaibatsu_ryo_kurata`<br>Rival: `syndicate_nadia` |
| `pilot_zaibatsu_satoshi_endo`<br>**"Linear-God"** | Satoshi Endo | **T3** | `ZMA-15` | `kinetic_rod_penetration`, `recoil_nullifier` | **108,000 Cr**<br>(7,100/cyc) | Wingman: `zaibatsu_raiden_kenta`<br>Mentor: `zaibatsu_renzo`<br>Rival: `terran_helen_braun` |
| `pilot_zaibatsu_omega_susanoo_prime`<br>**"Omega Prime"** | Cyber-Dominator Susanoo-X | **T4** | `ZX-22` | `singularity_core_overdrive`, `tachyon_godhood`, `mind_eater_strike` | **150,000 Cr**<br>(9,800/cyc) | Wingman: `zaibatsu_null07`<br>Mentor: `zaibatsu_renzo`<br>Rival: `terran_vance` |

---

### 5.5 Independent Ronin & Legendary Mercenaries (12 Recruitable Pilots)
Factionless veterans, dishonored corporate deserters, and roaming combat aces available to the highest bidder.

| ID & Callsign | Full Name | Tier | Preferred MS | Combat & Personality Traits | Hiring / Salary | Kinship & Relational Ties |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- |
| `pilot_indep_vance_outlaw`<br>**"Gray-Ghost"** | Captain Silas Vance | **T3** | `bp_player_vanguard_heavy` | `freelance_loyalty`, `veteran_instinct`, `heavy_recoil_soak` | **115,000 Cr**<br>(7,500/cyc) | Estranged cousin: `terran_vance` |
| `pilot_indep_starlight_ronin`<br>**"Ceres-Ronin"** | Miyamoto 'Zero' Vance | **T3** | `bp_player_ghost_sniper` | `wandering_blade`, `critical_parry`, `unbound_mercenary` | **120,000 Cr**<br>(7,800/cyc) | Blood brother: `syndicate_jackal` |
| `pilot_indep_helena_valk`<br>**"Free-Flight"** | Helena 'Valkyrie' Thorne | **T3** | `bp_player_stratos_interceptor` | `unshackled_vector`, `particle_fury` | **118,000 Cr**<br>(7,600/cyc) | Estranged sister: `colony_lyra` |
| `pilot_indep_iron_jaw_boris`<br>**"Old War-Hound"** | Boris 'Iron-Jaw' Rostov | **T3** | `bp_player_scrapper_brawler` | `shrapnel_veteran`, `cockpit_crusher` | **108,000 Cr**<br>(7,000/cyc) | Disgraced uncle: `terran_rostova` |
| `pilot_indep_smuggler_queen_cruz`<br>**"Shadow-Runner"** | Carmen Cruz | **T2** | `SCR-05` | `blockade_runner`, `stealth_drift` | **78,000 Cr**<br>(5,000/cyc) | Cousin: `syndicate_cruz` |
| `pilot_indep_cyborg_kage`<br>**"Cyber-Ronin"** | Kage-00 | **T3** | `bp_player_ghost_sniper` | `hacked_neural_leash`, `monoblade_decapitator` | **125,000 Cr**<br>(8,000/cyc) | Former lab mate: `zaibatsu_null07` |
| `pilot_indep_old_miner_toby`<br>**"Drill-Master"** | Old Toby | **T2** | `bp_player_scrapper_brawler` | `mining_drill_melee`, `debris_crusher` | **62,000 Cr**<br>(4,000/cyc) | Independent |
| `pilot_indep_sol_corsair_jill`<br>**"Void-Cat"** | Jill 'Corsair' Morgan | **T2** | `SCR-12` | `harpoon_breach`, `zero_g_acrobatics` | **74,000 Cr**<br>(4,800/cyc) | Daughter: `syndicate_skag_morgan` |
| `pilot_indep_tachyon_wraith`<br>**"Tachyon-Wraith"** | Wraith-99 | **T3** | `bp_player_stratos_interceptor` | `tachyon_sniping`, `ghost_radar` | **122,000 Cr**<br>(7,900/cyc) | Independent |
| `pilot_indep_foundry_exile_ortiz`<br>**"Crucible-Exile"** | Carlos Ortiz | **T2** | `bp_player_scrapper_brawler` | `incendiary_ram`, `boiler_overclock` | **71,000 Cr**<br>(4,600/cyc) | Nephew: `syndicate_mateo_ortiz` |
| `pilot_indep_senate_deserter_fallon`<br>**"Renegade Hawk"** | Major Lucas Fallon | **T3** | `bp_player_vanguard_heavy` | `military_tactician`, `kinetic_penetration` | **112,000 Cr**<br>(7,300/cyc) | Brother: `terran_beatrice_fallon` |
| `pilot_indep_transhuman_nomad_jin`<br>**"The Hybrid"** | Jin Takahashi-Chen | **T4** | `bp_player_ghost_sniper` | `hybrid_neural_chassis`, `monoblade_singularity`, `free_agent_legend` | **145,000 Cr**<br>(9,500/cyc) | Renegade grandson: `zaibatsu_renzo` |

---

## 6. High-Value Targets & Command Structures (The 72 VIPs)

The game features **72 Non-Recruitable VIPs and Military Leaders** (18 per major faction) who command fleets, govern orbital sectors, and fund military R&D. Eliminating or capturing them triggers massive geopolitical and relational shocks.

### 6.1 Terran Coalition High Command & Aristocracy (18 VIPs)
| ID & Name | Title & Planetary Role | Dynasty | Relational Ties | Narrative Dossier & Elimination Consequence |
| :--- | :--- | :---: | :--- | :--- |
| `char_terran_vance`<br>**General Deborah Vance** | Supreme Director of Planetary Ordnance | **Vance** | Wingman: `terran_cole`<br>Rival: `colony_cassian`<br>Brother: `terran_julian_vance`; Daughter: `terran_claire_vance`; Son: `terran_tyler_vance`; Estranged nephew: `syndicate_jackal` | Supreme commander of Earth defense forces. Sacrificed family ties for imperial survival. |
| `char_terran_sterling`<br>**High Commissioner Arthur Sterling** | Senate Defense Liaison & Procurement Hawk | **Sterling** | Rival: `terran_vance`<br>Son: `terran_lucas_sterling` | Controls the military budget with an iron spreadsheet. Secretly trades with Zaibatsu brokers. |
| `char_terran_julian_vance`<br>**Col. Julian Vance (Ret.)** | Foundry Logistics Overseer | **Vance** | Sister: `terran_vance`; Son: `syndicate_jackal` | Deborah's older brother whose son Jax stole a prototype and joined the pirate fringe. |
| `char_terran_claire_vance`<br>**Major Claire Vance** | Planetary Defense Battalion Commander | **Vance** | Wingman: `terran_cole`<br>Mentor: `terran_vance`<br>Rival: `colony_sorren`<br>Mother: `terran_vance`; Brother: `terran_tyler_vance`; Cousin: `syndicate_jackal` | Deborah's disciplined daughter, determined to prove herself on merit rather than bloodline. |
| `char_terran_briggs`<br>**General Gregory Briggs** | High Command Fortification Marshal | **Briggs** | Rival: `colony_cassian`<br>Daughter: `terran_tara_briggs` | Architect of the Callisto bunker networks. |
| `char_terran_oconnor`<br>**Commodore Sean O'Connor** | Orbital Defense Station Overseer | **OConnor** | Rival: `colony_lyra`<br>Son: `terran_liam_oconnor` | Commands orbital weapon platforms overlooking lunar staging yards. |
| `char_terran_anna_rostova`<br>**Anna Rostova** | civilian_liaison | **Rostov** | Mother: `terran_rostova`; Mother: `terran_dmitri_rostov` | Widow of late Admiral Viktor Rostov fighting debt collection. |
| `char_terran_dr_arnold`<br>**Dr. Heinrich Arnold** | chief_metallurgist | **None** | Independent | Lead foundry scientist developing Tungsten-Carbide alloys. |
| `char_terran_quartermaster_graves`<br>**Quartermaster Graves** | logistics_director | **None** | Independent | Rigid inventory clerk who accounts for every depleted uranium sabot. |
| `char_terran_senator_holloway`<br>**Senator Evelyn Holloway** | senate_diplomat | **Holloway** | Independent | Earth Senate advocate for total planetary mobilization. |
| `char_terran_engineer_burt`<br>**Chief Mechanic Burt** | hangar_chief | **None** | Independent | Veteran grease monkey who has patched over two hundred Ironclads. |
| `char_terran_cadet_elise`<br>**Cadet Elise Vance** | cadet_in_training | **Vance** | Granddaughter: `terran_vance` | Deborah's granddaughter studying ballistics at the Geneva Academy. |
| `char_terran_liaison_trent`<br>**Major Donald Trent** | military_police | **None** | Independent | Coalition internal affairs investigator watching for defectors. |
| `char_terran_refit_master_otto`<br>**Foundry Master Otto** | foundry_overseer | **None** | Independent | Supervises the casting of 400mm Behemoth rail barrels. |
| `char_terran_nurse_clara`<br>**Dr. Clara Rostova** | field_surgeon | **Rostov** | Aunt: `terran_rostova` | Battlefield surgeon treating trauma and amputations in bunker redoubts. |
| `char_terran_test_pilot_greer`<br>**Capt. Wade Greer** | test_pilot | **None** | Independent | Test-flies experimental Vanguard prototypes; survived four core breeches. |
| `char_terran_attache_morris`<br>**Diplomatic Attache Morris** | intelligence_liaison | **None** | Independent | Monitors clandestine transmissions between Earth and Mars. |
| `char_terran_supply_sergeant_brant`<br>**Sgt. Caleb Brant** | convoy_commander | **None** | Independent | Commands the heavy tungsten supply haulers across crater routes. |

---

### 6.2 Outer Colonies League High Council & Admiralty (18 VIPs)
| ID & Name | Title & Planetary Role | Dynasty | Relational Ties | Narrative Dossier & Elimination Consequence |
| :--- | :--- | :---: | :--- | :--- |
| `char_colony_cassian`<br>**Fleet Commander Cassian Vane** | Supreme Marshall of the Liberation Flotilla | **Vane** | Wingman: `colony_sorren`<br>Rival: `terran_vance`<br>Sister: `colony_beatrice_vane`; Son: `colony_julian_vane` | Supreme Marshall of the Outer Colony Flotilla. Former Academy rival of General Deborah Vance. |
| `char_colony_lyra`<br>**Minister Lyra Thorne** | Chief Diplomat & Solar Habitat Resource Chair | **Thorne** | Rival: `terran_sterling`<br>Husband: `colony_paul_thorne`; Nephew: `colony_erik_thorne` | Protector of the civilian orbital cylinders who negotiates desperately for raw water and tritium. |
| `char_colony_beatrice_vane`<br>**Senator Beatrice Vane** | Colony High Council Representative | **Vane** | Brother: `colony_cassian` | Cassian's sister who champions political autonomy from Terran resource quotas. |
| `char_colony_paul_thorne`<br>**Chief Engineer Paul Thorne** | Orbital Environmental Mesh Overseer | **Thorne** | Wife: `colony_lyra`; Son: `colony_erik_thorne` | Designs the radiator wings and magnetic containment fields for Aether reactors. |
| `char_colony_helmut_zhao`<br>**Admiral Helmut Zhao** | Deep Space Patrol Fleet Commander | **Zhao** | Rival: `terran_oconnor`<br>Estranged daughter: `zaibatsu_maya` | Hardline orbital fleet officer whose daughter defected to Zaibatsu corporate security. |
| `char_colony_finch`<br>**Flight Marshal Alistair Finch** | Interceptor Wing Flight Instructor | **Finch** | Wingman: `colony_sorren` | Trains young interceptor recruits in three-dimensional vector thruster combat. |
| `char_colony_dr_arundel`<br>**Dr. Althea Arundel** | chief_materials_scientist | **None** | Independent | Pioneered lightweight Aerosteel nanoweave for Colony frames. |
| `char_colony_ambassador_koren`<br>**Ambassador Varis Koren** | un_council_liaison | **None** | Independent | Represents the Outer Colonies at the Geneva Peace Accords. |
| `char_colony_habitat_gov_orlov`<br>**Governor Orlov** | habitat_governor | **None** | Independent | Administers agricultural colony Cylinder 4 overlooking Ceres. |
| `char_colony_dockmaster_thea`<br>**Dockmaster Thea** | shipyard_superintendent | **None** | Independent | Manages zero-G mobile suit gantry cranes and launch catapults. |
| `char_colony_hospitaller_mara`<br>**Sister Mara Vane** | medical_director | **Vane** | Sister: `colony_cassian` | Directs civilian hospitals for habitat decompression trauma victims. |
| `char_colony_hydroponics_sam`<br>**Farmer Sam Thorne** | food_syndicate_chief | **Thorne** | Cousin: `colony_lyra` | Controls algae protein synthesizers and water filtration grids. |
| `char_colony_telemetry_toby`<br>**Toby Finch** | radar_station_chief | **Finch** | Son: `colony_finch` | Detects approaching Coalition rail gunboats across lunar shadow corridors. |
| `char_colony_tritium_refiner_jov`<br>**Jovan Sol** | refinery_boss | **None** | Independent | Refines high-purity fusion fuel from Jupiter gas scoops. |
| `char_colony_quartermaster_selim`<br>**Selim Mansoor** | fleet_quartermaster | **None** | Independent | Balances emergency munitions allocations across fifty fighter wings. |
| `char_colony_cadet_instructor_titus`<br>**Commander Titus** | academy_proctor | **None** | Independent | Evaluates flight simulation scores for high-G vector pilots. |
| `char_colony_historian_valeria`<br>**Archivist Valeria** | cultural_archivist | **None** | Independent | Preserves the historical treaty documents of the Secession War. |
| `char_colony_salvage_broker_kenzo`<br>**Kenzo Lin** | habitat_recycler | **Lin** | Uncle: `colony_sorren` | Reclaims shattered solar panel glass and burned thruster nozzles. |

---

### 6.3 Syndicate Rim Cartel Barons & Smuggling Lords (18 VIPs)
| ID & Name | Title & Planetary Role | Dynasty | Relational Ties | Narrative Dossier & Elimination Consequence |
| :--- | :--- | :---: | :--- | :--- |
| `char_syndicate_cruz`<br>**Madame Rosalind Cruz** | Matriarch of Scrap Depot 9 & Smuggling Baroness | **Cruz** | Wingman: `syndicate_nadia`<br>Rival: `terran_sterling`<br>Brother: `syndicate_tito_cruz`; Adopted daughter: `syndicate_nadia` | Ruthless ruler of asteroid Scrap Depot 9. Treats family loyalty as the only law in the black. |
| `char_syndicate_torval`<br>**Commodore 'Iron-Eye' Torval** | Cartel Reaver Fleet Commodore | **Torval** | Wingman: `syndicate_jackal`<br>Rival: `terran_vance` | Infamous pirate commodore missing his right eye from a Coalition railgun blast. |
| `char_syndicate_tito_cruz`<br>**Tito Cruz** | Depot 9 Black-Market Broker | **Cruz** | Rival: `zaibatsu_renzo`<br>Sister: `syndicate_cruz`; Son: `syndicate_rico_cruz` | Manages the fence networks that launder stolen Coalition and Zaibatsu mobile suit frames. |
| `char_syndicate_mateo_ortiz`<br>**Mateo Ortiz** | Master Foundry Melter | **Ortiz** | Wingman: `syndicate_nadia`<br>Biological daughter: `syndicate_nadia` | Old foundry master who taught Nadia how to brew molten slag incendiary loads. |
| `char_syndicate_boss_varek`<br>**Boss Varek** | Asteroid Mining Guild Enforcer | **Varek** | Rival: `colony_cassian` | Controls illegal asteroid labor colonies through terror and debt coercion. |
| `char_syndicate_skag_morgan`<br>**Skag 'The Hook' Morgan** | Corsair Breaker Boss | **Morgan** | Wingman: `syndicate_jackal`<br>Rival: `terran_oconnor` | Boarding specialist who punctures cargo hulls with pneumatic grappling hooks. |
| `char_syndicate_bartender_sal`<br>**Sal 'Two-Fingers'** | black_market_bartender | **None** | Independent | Runs the cantina on Depot 9 where contracts and bounties are traded. |
| `char_syndicate_doc_sawbones`<br>**Dr. 'Sawbones' Miller** | unlicensed_surgeon | **None** | Independent | Performs back-alley cybernetic amputations and stimulant injections. |
| `char_syndicate_smuggler_greta`<br>**Greta Cruz** | smuggler_captain | **Cruz** | Niece: `syndicate_cruz` | Runs blockade-running shuttles through Terran patrol nets. |
| `char_syndicate_scrappy_kid_toby`<br>**Toby Ortiz** | foundry_runner | **Ortiz** | Grandson: `syndicate_mateo_ortiz` | Runs hot welding torches and slag crucibles across Depot 9. |
| `char_syndicate_hacker_null`<br>**Glitch 'Zero'** | avionics_jailbreaker | **None** | Independent | Strips Terran DRM encryption from captured mobile suit computers. |
| `char_syndicate_fence_malik`<br>**Malik Torval** | black_market_quartermaster | **Torval** | Brother: `syndicate_torval` | Fences stolen Coalition weapons and rare mineral crates. |
| `char_syndicate_armorer_babs`<br>**Babs 'Hammer' Varek** | scrap_metal_stamper | **Varek** | Sister: `syndicate_boss_varek` | Stamps stolen slag armor plates onto Hyena chassis frames. |
| `char_syndicate_fuel_smuggler_vic`<br>**Vic 'Vapor' Vance** | tritium_bootlegger | **Vance** | Brother: `syndicate_jackal` | Jax Vance's younger brother who siphons gas from Jovian platforms. |
| `char_syndicate_mine_foreman_grog`<br>**Foreman Grog** | asteroid_labor_boss | **None** | Independent | Oversees deep-core slag mining operations in pirate asteroid belts. |
| `char_syndicate_radio_pirate_rox`<br>**Roxy 'Static'** | pirate_broadcaster | **None** | Independent | Broadcasts pirate rock and radar-warning alerts across the belt. |
| `char_syndicate_shipbreaker_hulk`<br>**Hulk Morgan** | derelict_shipbreaker | **Morgan** | Son: `syndicate_skag_morgan` | Cuts open abandoned capital ships with massive plasma torches. |
| `char_syndicate_informant_whisper`<br>**Whisper** | shadow_informant | **None** | Independent | Sells military patrol timetables to the highest bidder. |

---

### 6.4 Zaibatsu Aerospace Board of Directors & Lead Researchers (18 VIPs)
| ID & Name | Title & Planetary Role | Dynasty | Relational Ties | Narrative Dossier & Elimination Consequence |
| :--- | :--- | :---: | :--- | :--- |
| `char_zaibatsu_renzo`<br>**Director Renzo Takahashi** | Executive VP of Special Weapons & Cybernetic R&D | **Takahashi** | Wingman: `zaibatsu_null07`<br>Rival: `terran_sterling`<br>Daughter: `zaibatsu_ayumi_takahashi`; Disowned son: `colony_jun_takahashi` | Architect of transhuman pilot interfaces. Views biological pilots as replaceable wetware. |
| `char_zaibatsu_vivienne`<br>**Dr. Vivienne Chen** | Chief Neural Architect & Cybernetic Surgeon | **Chen** | Wingman: `zaibatsu_null07`<br>Rival: `colony_lyra`<br>Brother: `zaibatsu_jin_chen`; Creator guardian: `zaibatsu_null07` | Designs synaptic leashes and brain-machine bridges that eliminate pilot fear and hesitation. |
| `char_zaibatsu_ayumi_takahashi`<br>**Ayumi Takahashi** | Executive VP of Acquisitions & Corporate Espionage | **Takahashi** | Wingman: `zaibatsu_maya`<br>Father: `zaibatsu_renzo` | Renzo's daughter who orchestrates hostile corporate buyouts and pilot headhunting. |
| `char_zaibatsu_jin_chen`<br>**Jin Chen** | Prototype Neural Cyber-Test Overseer | **Chen** | Sister: `zaibatsu_vivienne` | Vivienne's brother who volunteered for the first generation of direct synaptic jacks. |
| `char_zaibatsu_kaito_mori`<br>**Director Kaito Mori** | Corporate Security Disciplinary Director | **Mori** | Wingman: `zaibatsu_maya`<br>Rival: `syndicate_cruz` | Enforces corporate non-disclosure agreements with high-frequency assassination squads. |
| `char_zaibatsu_shiro_kuroda`<br>**Senior Board Member Kuroda** | Zaibatsu Executive Chairman | **Kuroda** | Rival: `terran_sterling` | Elder statesman of the Zaibatsu holding company who funds private mercenary proxy wars. |
| `char_zaibatsu_legal_vp_tanaka`<br>**VP Ken Tanaka** | chief_legal_counsel | **None** | Independent | Drafts binding corporate mercenary contracts with devastating non-compete clauses. |
| `char_zaibatsu_neuro_surgeon_fujita`<br>**Dr. Yosuke Fujita** | cybernetic_neurosurgeon | **None** | Independent | Performs synaptic bridge installations on candidate pilots. |
| `char_zaibatsu_ai_arch_minerva`<br>**Engineer Minerva Vance-Chen** | ai_integration_chief | **Chen** | Niece: `zaibatsu_vivienne` | Synthesizes bio-neural network firmware for combat mobile suits. |
| `char_zaibatsu_board_liaison_hisa`<br>**Director Hisa Mori** | boardroom_liaison | **Mori** | Sister: `zaibatsu_kaito_mori` | Monitors combat sortie profit-margins for the executive board. |
| `char_zaibatsu_quartermaster_shin`<br>**Quartermaster Shin** | advanced_materials_broker | **None** | Independent | Oversees high-purity Adamantine Carbide and Tritium reserves. |
| `char_zaibatsu_pr_director_emi`<br>**Emi Takahashi** | media_spin_director | **Takahashi** | Daughter: `zaibatsu_renzo` | Controls solar-wide news broadcasts covering up collateral damage. |
| `char_zaibatsu_nanite_eng_yoshida`<br>**Dr. Yoshida** | monofilament_metallurgist | **None** | Independent | Forges molecular-edge plasma katana blades in zero-G vacuum labs. |
| `char_zaibatsu_clone_overseer_unit0`<br>**Overseer-00** | clone_matrix_warden | **None** | Independent | Maintains synthetic clone pilot incubators in deep Martian vaults. |
| `char_zaibatsu_security_warden_goro`<br>**Warden Goro** | neural_penitentiary_chief | **None** | Independent | Tracks runaway cybernetic test subjects who escape corporate campuses. |
| `char_zaibatsu_subcontractor_vogel`<br>**Broker Vogel-Takahashi** | black_budget_fixer | **Takahashi** | Independent | Channels untraceable corporate funds to mercenary contractors. |
| `char_zaibatsu_quantum_crypt_aya`<br>**Aya Chen** | quantum_cryptographer | **Chen** | Daughter: `zaibatsu_vivienne` | Cracks enemy military communication ciphers in real-time during sorties. |
| `char_zaibatsu_recovery_chief_jin`<br>**Commander Jinbo** | asset_recovery_chief | **None** | Independent | Retrieves wrecked mobile suit black boxes before competitors can salvage them. |

---

## 7. The Monolith-Style Nemesis Dynamic Loop

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
