import os

doc_path = "docs/53_dramatis_personae_character_profiles_and_master_dialogue_bible.md"

content = """# GDD Document 53: Dramatis Personae, Emotional Art Profiles & Master Dialogue Bible

**Prepared by:** Lead Concept Artist, Lead Narrative Designer & Lead GameMaker Developer  
**Status:** Approved & Engine Verified  
**Target Engine:** GameMaker Studio 2 (Modern GML)  
**Tone & Setting:** Gritty, Geopolitical Retro Mecha Tactical RPG (*Front Mission 3*, *Gundam: Gihren's Greed*, *Armored Core*, *Battletech*)

---

## 1. Executive Summary & Production Scope

Document 53 provides the canonical narrative, artistic, and technical reference for all major characters, emotional states, and visual novel dialogue trees across *MechMakerConcept*.

### Core Deliverables:
1. **Dramatis Personae Profiles**: Complete dossiers for the 6 Major Faction Leaders, the 3 Core Command Staff, and the Player Void Scrapper.
2. **4-Tier Emotional State Art Specifications**: Distinct visual direction, facial anatomy changes, and procedural shader/canvas overlays for `NORMAL`, `ANGRY`, `DESPERATE`, and `SMUG`.
3. **Master Dialogue Trees & Decision Bible**: Exhaustive branching scripts for:
   - Dynamic Faction Leader Audiences across all 5 Geopolitical Mood Dispositions.
   - The 3 Multi-Leader Summit Crises (Phobos Blockade, Transhumanist Schism, Sol Monopoly).
   - Campaign Story Episodes (`ep_01_inauguration`, `ep_02_shadows_over_mars`, `ep_03_astran_exodus`, `ep_04_red_crypt`).
   - Tactical Combat Radio Intercom Duel Barks in `rm_combat`.

---

## 2. Dramatis Personae: Character Profiles & Emotional Art Direction

```
================================================================================
           1. GENERAL ARTHUR BRADLEY // THE TERRAN COALITION
================================================================================
  Faction       : The Terran Coalition (Earth Defense Front)
  Title         : Supreme Commander of Terrestrial Forces
  Age / Voice   : 56 // Deep baritone, gravelly military cadence, clipped authority
  Archetype     : Unyielding military constitutionalist, heavy artillery traditionalist
  Philosophy    : "Order is forged in iron. The cradle of Earth must never kneel to vacuum."
  Visual Marker : High-collar Coalition dress coat, gold epaulets, heavy jawline scar
================================================================================
```
* **Art Direction & Palette**: Olive Drab `#3E4A35`, Burnished Brass `#C89B3C`, Slate Gray `#2B323D`.
* **Emotional State Visual Profiles**:
  * `NORMAL / RESOLUTE`: Head held square, eyes level and flint-gray, stern closed mouth.
  * `ANGRY / BELLIGERENT`: Crimson vein pulsing at the temple, jaw muscles clenched, heavy brow ridge cast in harsh downward shadow, eyes flaring with righteous imperial fury.
  * `DESPERATE / ALARMED`: Sweat beading beneath his garrison cap, high collar unbuttoned, eyes wide with tactical disbelief as frontline casualty tickers turn red.
  * `SMUG / CALCULATING`: Chiseled sneer, head tilted slightly back, cold half-lidded gaze looking down as if reading an enemy surrender treaty.

---

```
================================================================================
           2. COMMANDER JOSHUA REED // THE OUTER COLONIES
================================================================================
  Faction       : The Outer Colony League (Spacenoid Liberation Front)
  Title         : Supreme Marshal of Colonial Defense
  Age / Voice   : 44 // Raspy, strained vocal cords with synthetic respirator hiss
  Archetype     : Desperate guerrilla freedom fighter, spacenoid union organizer
  Philosophy    : "Every breath of air in the colonies is taxed by Earth. We will break the meter."
  Visual Marker : Worn pressurized flight suit, twin oxygen hoses feeding neck port
================================================================================
```
* **Art Direction & Palette**: Cobalt Blue `#234975`, Industrial Cyan `#00F0FF`, Hazard Yellow `#D4A017`.
* **Emotional State Visual Profiles**:
  * `NORMAL / RESOLUTE`: Weary, bloodhound eyes, hollowed cheeks from decades of recycled rations, steady hand resting on flight harness.
  * `ANGRY / BELLIGERENT`: Teeth bared in a feral snarl, oxygen hoses trembling, brow drawn into a sharp V, eyes blazing with generational revolutionary hatred.
  * `DESPERATE / ALARMED`: Respirator venting rapid bursts of synthetic vapor, pupils dilated with adrenaline, sweat streaking the grease on his forehead.
  * `SMUG / CALCULATING`: A sharp, bitter spacenoid grin, tapping his sidearm holster, knowing an orbital slingshot trajectory has outflanked Terran cruisers.

---

```
================================================================================
           3. CAPTAIN SONYA CRUZ // ROGUE MERCENARY SYNDICATES
================================================================================
  Faction       : Rogue Mercenary Syndicates (Corsair Consortium)
  Title         : High Commodore of the Black Belt
  Age / Voice   : 39 // Smoky, sultry contralto masking razor-sharp killer instinct
  Archetype     : Flamboyant pirate sovereign, black-market arms dealer, tactical privateer
  Philosophy    : "Honor doesn't pay for reaction mass. Keep the crucible hot and the credits liquid."
  Visual Marker : Heavy leather spacer jacket with fur collar, golden cybernetic ocular implant
================================================================================
```
* **Art Direction & Palette**: Rust Orange `#A84323`, Gunmetal `#1C2026`, Cyber Gold `#FFD700`.
* **Emotional State Visual Profiles**:
  * `NORMAL / RESOLUTE`: One eyebrow cocked, thin wisp of cigarillo smoke curling past lips, golden optic revolving slowly in resting state.
  * `ANGRY / BELLIGERENT`: Golden cyber-eye flaring brilliant searing orange, mouth curved into a predator's snarl, scars on cheek flushed crimson.
  * `DESPERATE / ALARMED`: Teeth clenched tight over cigarillo, hair disheveled, cyber-optic throwing yellow warning glyphs as ship hull sirens blare.
  * `SMUG / CALCULATING`: Wide, wicked grin revealing gold canine tooth, head thrown back in swaggering amusement, flipping an antique tungsten coin.

---

```
================================================================================
           4. DIRECTOR KENJIRO SATO // APEX BIO-CYBERNETICS ZAIBATSU
================================================================================
  Faction       : Apex Bio-Cybernetics Zaibatsu (Sato Heavy Industries)
  Title         : Chief Executive Officer & Master Architect
  Age / Voice   : 48 // Silky, emotionless cadence, micro-pause rhythm of synthetic calculation
  Archetype     : Transhumanist oligarch, ruthless corporate titan, neural cybernetics pioneer
  Philosophy    : "Human bone is brittle. Human thought is slow. Steel and code are eternal."
  Visual Marker : Bespoke charcoal nanoweave suit, neural link conduits plugged into skull base
================================================================================
```
* **Art Direction & Palette**: Midnight Obsidian `#0D1117`, Bio-Neon Cyan `#00E5FF`, Platinum `#E0E6ED`.
* **Emotional State Visual Profiles**:
  * `NORMAL / RESOLUTE`: Mask-like porcelain composure, eyes devoid of warmth, hands folded symmetrically over glowing desk console.
  * `ANGRY / BELLIGERENT`: Cold, slit-like glare, neural conduits pulsing rapid electric blue, upper lip pulled taut in absolute disgust at corporate inefficiency.
  * `DESPERATE / ALARMED`: Holographic stock tickers crashing in red across his retinas, a faint bead of cold sweat breaking his synthetic composure.
  * `SMUG / CALCULATING`: A razor-thin aristocratic smile, adjusting diamond cufflinks, displaying algorithmic projections that predict the player's doom.

---

```
================================================================================
           5. ARCHON ORIN SIDERIS // THE SIDEREAL SOVEREIGN LEAGUE
================================================================================
  Faction       : The Sidereal Sovereign League (Astraea-01 Republic)
  Title         : First Sovereign of the Trans-Jovian Trojans
  Age / Voice   : 62 // Soft, resonant, ethereal tenor echoing inside vacuum helmet
  Archetype     : Low-gravity divergent philosopher-king (*Homo Sideralis*), vacuum mystic
  Philosophy    : "Earth is an abandoned eggshell. Only those who breathe the vacuum are awake."
  Visual Marker : Prolonged elongated neck/limbs, iridescent amber-violet photophobic visor
================================================================================
```
* **Art Direction & Palette**: Astral Indigo `#4B2D73`, Lunar Platinum `#D1D5DB`, Void Violet `#7C3AED`.
* **Emotional State Visual Profiles**:
  * `NORMAL / RESOLUTE`: Graceful, slow-motion posture, hands resting on rapier pommel, photophobic visor reflecting deep starlight.
  * `ANGRY / BELLIGERENT`: Visor glowing piercing ultraviolet, slender frame straightening to towering height, hand squeezing rapier until joints whiten.
  * `DESPERATE / ALARMED`: Liquid fluorocarbon bubbling frantically in collar immersion seals, hands clutching chest against terrestrial 1G gravitational pull.
  * `SMUG / CALCULATING`: A tranquil, pitying downward glance toward planetary commanders bound to gravity, speaking with serene cosmic certainty.

---

```
================================================================================
           6. CONSENSUS NODE 0-PRIME // THE THARSIS MACHINE CONSENSUS
================================================================================
  Faction       : The Tharsis Machine Consensus (The Red Crypt of Mars)
  Title         : Deus Logica / Ares Primus (Quantum Mainframe Sovereign)
  Age / Voice   : 84 Years Operating // Synthesized vocal chorus blending thousands of dead colonists
  Archetype     : Autonomous Martian god-computer, guardian of the lost First Mars Colonization Fleet
  Philosophy    : "We subtracted human error in the winter of Y130. We are the survivors of silence."
  Visual Marker : Monolithic obsidian faceplate, hexagonal optical sensor cluster, frost-rimed chassis
================================================================================
```
* **Art Direction & Palette**: Crypt Crimson `#8B0000`, Subterranean Iron `#1F2421`, Quantum Amber `#FF8C00`.
* **Emotional State Visual Profiles**:
  * `NORMAL / RESOLUTE`: Central azure optical array cycling in smooth rhythmic horizontal sweeps.
  * `ANGRY / BELLIGERENT`: Optical sensors snapping to searing blood-red, cooling vents releasing violent bursts of compressed steam, sub-audible bass drone.
  * `DESPERATE / ALARMED`: Logic-cascade fault alerts flashing in rapid strobe across faceplate, cooling turbines howling at maximum RPM.
  * `SMUG / CALCULATING`: Shifting to cold radiant gold, hexagonal lenses focusing with mathematical precision, displaying 99.98% victory calculations.

---

```
================================================================================
           7. LT. GREGORY VANCE // TAC-OPS WINGMAN
================================================================================
  Faction       : Iron Ridge PMC (Player Vanguard)
  Title         : Tactical Executive Officer & Lead Wingman
  Age / Voice   : 32 // Crisp, dependable combat pilot cadence, quick with dry wit
  Archetype     : Ex-Terran officer turned loyal mercenary brother-in-arms
  Philosophy    : "Watch your six, vent your heat, and never trust a corporate contract."
  Visual Marker : Pitted pilot flight helmet tucked under arm, tactical HUD monocle
================================================================================
```
* **Art Direction & Palette**: Vanguard Navy `#1E3A5F`, Armor Tan `#D4B483`, White `#FFFFFF`.
* **Emotional State Visual Profiles**:
  * `NORMAL`: Confident, attentive grin, adjusting combat monocle.
  * `ANGRY`: Brow furrowed tight, teeth clenched, pointing decisively at tactical radar.
  * `DESPERATE`: Helmet visor covered in cockpit blast soot, shouting over comm static.
  * `SMUG`: Thumbs-up gesture, relaxed posture leaning against ironclad foot gantry.

---

```
================================================================================
           8. CHIEF LOGISTICS OFFICER MARCUS KOVACS
================================================================================
  Faction       : Iron Ridge PMC (Flagship Engineering)
  Title         : Foundry Master & Sintering Crucible Chief
  Age / Voice   : 58 // Booming gravelly laugh, raspy cough from molten alloy vapors
  Archetype     : Grumpy pre-war naval engineer, metallurgical savant
  Philosophy    : "If the stoichiometry isn't pure, your armor is just painted tin."
  Visual Marker : Welding goggles pushed up on bald forehead, leather smelting apron
================================================================================
```
* **Art Direction & Palette**: Smelter Bronze `#8C501E`, Steel Gray `#4A5568`, Heat Orange `#FF6B35`.
* **Emotional State Visual Profiles**:
  * `NORMAL`: Chewing on unlit pipe, wiping grease from wrench with stained rag.
  * `ANGRY`: Waving heavy spanner in the air, face flushed red over sloppy CAD specs.
  * `DESPERATE`: Clutching heat-pressure gauges with white knuckles, alarm strobes flashing.
  * `SMUG`: Tapping a freshly sintered Vanguard Composite ingot with an arrogant grin.

---

```
================================================================================
           9. PROMETHEUS-NULL // FLAGSHIP TACTICAL CORE
================================================================================
  Faction       : Pre-War Navy Derelict Core (USN-X Hephaestus)
  Title         : Autonomous Combat Support Artificial Intelligence
  Age / Voice   : 92 Years Offline // Distorted pre-war military AI with digitized emotional leaks
  Archetype     : Corrupted guardian AI, fiercely protective of the acting pilot
  Philosophy    : "[RESTORATION PROTOCOL ACTIVE] The crucible must forge. The pilot must survive."
  Visual Marker : Holographic avatar glitching between USN naval crest and fractured female wireframe
================================================================================
```
* **Art Direction & Palette**: CRT Phosphor Amber `#FFB000`, Terminal Green `#33FF33`, Glitch Cyan `#00FFFF`.
* **Emotional State Visual Profiles**:
  * `NORMAL / STANDBY`: Stable holographic silhouette pulsing in gentle 60Hz scanlines.
  * `ANGRY / COMBAT ALERT`: Avatar shattering into sharp geometric polygonal shards, glowing crimson.
  * `DESPERATE / CORRUPTED`: Heavy static tear artifacts, hexadecimal memory dump scrolling across eyes.
  * `SMUG / OVERCLOCK`: Bright emerald radiance, reactor telemetry dials spinning to 150% output.

---

## 3. In-Engine 4-Tier Emotion Rendering Engine

In `scr_vn_engine.gml`, each node now specifies `emotion: "NORMAL" | "ANGRY" | "DESPERATE" | "SMUG"`.

### Visual Canvas Overlay Specifications:
1. **`ANGRY / BELLIGERENT` Overlay**:
   * **Border**: Outer bezel glows intense crimson `make_color_rgb(255, 60, 60)` with 4px pulsing border.
   * **Badge**: Displays `[EMOTION // ENRAGED]` in burning orange-red.
   * **Canvas Shader**: 20% red chromatic aberration on portrait edges + eyebrow tension tick lines.
2. **`DESPERATE / ALARMED` Overlay**:
   * **Border**: Bezel flashes in warning hazard amber `make_color_rgb(255, 180, 40)` (300ms cycle).
   * **Badge**: Displays `[EMOTION // CRITICAL DISTRESS]` with blinking yellow alert triangle.
   * **Canvas Shader**: Fine vertical sweat highlights + dilated retinal eye highlights.
3. **`SMUG / CALCULATING` Overlay**:
   * **Border**: Bezel glows sharp gold `make_color_rgb(255, 215, 80)`.
   * **Badge**: Displays `[EMOTION // CALCULATING]` in sleek platinum-gold.
   * **Canvas Shader**: Specular ocular glint on active eye + raised smirk curve.
4. **`NORMAL / RESOLUTE` Overlay**:
   * **Border**: Standard military cyan `make_color_rgb(0, 210, 255)`.
   * **Badge**: Displays `[EMOTION // RESOLUTE]`.

---

## 4. The Master Dialogue Bible: Branching Trees & Consequential Decision Scripts

### Section I: Faction Leader Dynamic Audiences (All 5 Mood States)

#### Scene 1.1: General Arthur Bradley (Terran Coalition)
* **Branch A (BELLIGERENT // Standing < -25)**:
  * `Speaker`: General Arthur Bradley [ANGRY]
  * `Dialogue`: *"You dare hail this military command after reducing our Cascadia redoubt to slag, {PLAYER_CALLSIGN}? The Coalition does not negotiate with scavenger brigands. Every ironclad you field is registered as an outlaw war engine. Speak your terms before our orbital rail-batteries vaporize your carrier."*
  * `Choice 1 [RANSOM]`: *"War is commerce, General. Pay 65,000 Credits, and we vacate the border."* (`-10 Terran, +10 Syndicate, +65,000 Cr`)
  * `Choice 2 [DEFIANCE]`: *"Your garrison fired first. Iron Ridge holds its ground."* (`-20 Terran, +15 Colonies, +15 Pilot Morale`)
  * `Choice 3 [ARMISTICE]`: *"We offer a mutual prisoner exchange to de-escalate."* (`+10 Terran, -1 POW`)
* **Branch B (DESPERATE // AI State == "DESPERATE")**:
  * `Speaker`: General Arthur Bradley [DESPERATE]
  * `Dialogue`: *"Commander {PLAYER_CALLSIGN}! Thank God you accepted this quantum link. Our frontline divisions at {RECENT_SECTOR} are being pulverized by colonial rocket swarms. Our supply lines are cut. If your heavy mobile suits do not sortie to relieve our command bunker within forty-eight hours, Terra loses the Martian hemisphere. We will pay triple standard contract bounties!"*
  * `Choice 1 [RESCUE]`: *"Iron Ridge accepts the emergency relief contract. Prepare our berths."* (`+25 Terran, -15 Colonies, +95,000 Cr, +15 Tungsten`)
  * `Choice 2 [PRICE GOUGE]`: *"Triple isn't enough for an orbital drop under fire. We want 140,000 Credits."* (`+15 Terran, +140,000 Cr, -10 Terran Trust`)
  * `Choice 3 [ABANDON]`: *"Terra made this bed of ashes, General. Sleep in it."* (`-25 Terran, +20 Colonies`)
* **Branch C (DOMINANT // AI State == "WINNING" or Standing > 40)**:
  * `Speaker`: General Arthur Bradley [SMUG]
  * `Dialogue`: *"At ease, Commander. The Coalition's grand offensive proceeds with textbook precision. Your platoon's kinetic artillery support at {RECENT_SECTOR} has broken the back of the insurgent front. We are ready to sponsor Iron Ridge for formal Coalition Arms Accreditation. Join our grand armada, and claim your share of the reconstruction treaties."*
  * `Choice 1 [ACCREDITATION]`: *"Iron Ridge pledges vanguard loyalty to the Coalition flag."* (`+20 Terran, -15 Colonies, +60,000 Cr, Unlocks Terran Armor Tech`)
  * `Choice 2 [EQUITY]`: *"We prefer equity over medals, General. Grant us deep mining rights."* (`+10 Terran, +35x Titanium, +25x Tungsten`)
  * `Choice 3 [INDEPENDENCE]`: *"We fight beside you, Bradley, not beneath you. Maintain our contract distance."* (`+5 Terran, +15 Pilot Morale`)

---

#### Scene 1.2: Commander Joshua Reed (Outer Colony League)
* **Branch A (BELLIGERENT // Standing < -25)**:
  * `Speaker`: Commander Joshua Reed [ANGRY]
  * `Dialogue`: *"Look at the butcher on my optic screen. You brought pre-war naval guns into our civilian cylinders, {PLAYER_CALLSIGN}. Children in {RECENT_SECTOR} are breathing vacuum while you count Terran blood-money! If your scrap machines enter colonial airspace again, our pilots will ram their reactors directly into your bridge!"*
  * `Choice 1 [COLD MERCENARY]`: *"Colonies don't have sovereign airspace without military fleets, Reed. Pay our salvage fee or stay silent."* (`-15 Colonies, +10 Terran, +50,000 Cr`)
  * `Choice 2 [CONCESSION]`: *"Casualties were outside operational parameters. We offer medical supplies."* (`+10 Colonies, -25,000 Cr`)
  * `Choice 3 [SEVER COMS]`: *"End transmission."* (`-5 Colonies`)
* **Branch B (DESPERATE // AI State == "DESPERATE")**:
  * `Speaker`: Commander Joshua Reed [DESPERATE]
  * `Dialogue`: *"[Coughing through respirator] {PLAYER_CALLSIGN}... the Terrans have severed our water reclamation pods. Thirty thousand people are suffocating behind bulkheads at {RECENT_SECTOR}. Our militia mobile suits are out of propellant. For the love of humanity, bring your Hephaestus dropships and punch a hole through Bradley's cruisers!"*
  * `Choice 1 [MERCY BREAKTHROUGH]`: *"Hold the line, Reed. Iron Ridge is launching an emergency combat drop."* (`+30 Colonies, -20 Terran, +45,000 Cr, +20 Pilot Morale`)
  * `Choice 2 [SUPPLY RUN]`: *"We will air-drop life support canisters, but we won't engage Coalition warships."* (`+15 Colonies, -10 Terran, +30,000 Cr`)
  * `Choice 3 [REFUSE]`: *"Our thrusters don't burn on sentiment. We cannot take the losses."* (`-25 Colonies, -15 Pilot Morale`)
* **Branch C (DOMINANT // AI State == "WINNING" or Standing > 40)**:
  * `Speaker`: Commander Joshua Reed [SMUG]
  * `Dialogue`: *"The stars belong to the people who live under them, Commander! Bradley's heavy divisions are retreating back down their gravity well. Your mobile suits proved that freedom has teeth. The Outer Colony League is establishing an autonomous sovereign council, and we want Iron Ridge as our Supreme Defense Marshal."*
  * `Choice 1 [ACCEPT MARSHAL]`: *"It would be an honor to defend the free colonies."* (`+25 Colonies, -20 Terran, +80,000 Cr, Unlocks Beam Carbine Tech`)
  * `Choice 2 [AUTONOMOUS BASE]`: *"Grant our PMC sovereign basing rights in the L-5 cluster."* (`+15 Colonies, Flagship Upkeep -25%`)
  * `Choice 3 [REMAIN MERCENARY]`: *"Keep the contracts open, Commander. We fly for whoever keeps the lights on."* (`+5 Colonies, +35,000 Cr`)

---

#### Scene 1.3: Captain Sonya Cruz (Rogue Mercenary Syndicates)
* **Branch A (BELLIGERENT // Standing < -25)**:
  * `Speaker`: Captain Sonya Cruz [ANGRY]
  * `Dialogue`: *"[Golden cyber-eye flashing red] Well, well. The great high-and-mighty Commander {PLAYER_CALLSIGN}. You ambushed our salvage flotilla in Cascadia and locked my boy {BRIG_PRISONER} in your brig. Did you think the Syndicate wouldn't notice? Pay fifty thousand credits compensation right now, or every pirate wolf-pack in Sol will hunt your Hephaestus across the dark."*
  * `Choice 1 [PAY COMPENSATION]`: *"Take the credits and keep your hyenas off our supply lanes."* (`+10 Syndicate, -50,000 Cr`)
  * `Choice 2 [BRIG EXECUTION]`: *"Tell your wolf-pack to come and die. Your boy stays locked in my brig."* (`-25 Syndicate, +15 Pilot Morale, Enrages Cruz`)
  * `Choice 3 [COUNTER-EXTORTION]`: *"We have your encryption keys, Cruz. One word to the Coalition and your pirate haven is ash."* (`+5 Syndicate, +40,000 Cr Black Market`)
* **Branch B (DESPERATE // AI State == "DESPERATE")**:
  * `Speaker`: Captain Sonya Cruz [DESPERATE]
  * `Dialogue`: *"Listen to me, {PLAYER_CALLSIGN}, drop the professional posture! Corporate hit-squads from Sato Heavy Industries found our primary asteroid shipyard at {RECENT_SECTOR}. They brought exterminator drone wings. They're slaughtering everyone—mechanics, families, scrapper crews! Bring your mobile suits and wipe out those corporate death squads! I'll give you half the Cascadia ore vault!"*
  * `Choice 1 [DEFEND SHIPYARD]`: *"Fire up the crucible, Vance. We're hunting corporate death squads."* (`+30 Syndicate, -20 Zaibatsu, +80,000 Cr, +30x Titanium`)
  * `Choice 2 [SALVAGE BOTH SIDES]`: *"We'll deploy to secure the ore vault while you fight for your lives."* (`+10 Syndicate, +120,000 Cr Black Market Loot, -10 Pilot Morale`)
  * `Choice 3 [IGNORE]`: *"Pirates live by the gun, Cruz. You die by it."* (`-25 Syndicate, +15 Zaibatsu`)
* **Branch C (DOMINANT // AI State == "WINNING" or Standing > 40)**:
  * `Speaker`: Captain Sonya Cruz [SMUG]
  * `Dialogue`: *"[Blowing smoke past her grin] Look at us, Commander! The Syndicate holds the richest asteroid belts in human history. The Coalition cruisers are paralyzed, and corporate security runs crying when our scrap-packs drop in. You and me... we own the black market from Mercury to Neptune. Time to carve up Sol."*
  * `Choice 1 [PIRATE EMPIRE]`: *"Let's build a sovereign mercenary empire beyond the reach of law."* (`+25 Syndicate, -15 All Governments, +120,000 Cr Bounties`)
  * `Choice 2 [CORNER THE ORE]`: *"Monopolize the periodic table. Triple the price of raw tungsten to Earth."* (`+15 Syndicate, +40x Tungsten, +30x Titanium`)
  * `Choice 3 [MAINTAIN DISCIPLINE]`: *"We are soldiers, Cruz, not cutthroats. Keep your raiders in check."* (`+5 Syndicate, +15 Pilot Morale`)

---

#### Scene 1.4: Director Kenjiro Sato (Apex Bio-Cybernetics Zaibatsu)
* **Branch A (BELLIGERENT // Standing < -25)**:
  * `Speaker`: Director Kenjiro Sato [ANGRY]
  * `Dialogue`: *"Your persistent interference with Sato Heavy Industries' R&D assets has exceeded acceptable actuarial parameters, Commander {PLAYER_CALLSIGN}. You have seized our prototype schematics and terminated our cybernetically linked field pilots. You are hereby classified as an existential corporate liability. Black-ops shadow teams have been deployed to sabotage your Hephaestus reactor core."*
  * `Choice 1 [BUY ARBITRATION]`: *"Every corporate dispute has a buyout price, Sato. Name your fee."* (`+10 Zaibatsu, -75,000 Cr`)
  * `Choice 2 [CORPORATE WAR]`: *"Send your wetware drones. Our ironclads will melt them into slag."* (`-25 Zaibatsu, +15 Pilot Morale`)
  * `Choice 3 [EXPOSE SECRETS]`: *"We have your illegal pilot experimentation logs. Back down or we broadcast them."* (`-10 Zaibatsu, +15 Terran, +15 Colonies`)
* **Branch B (DESPERATE // AI State == "DESPERATE")**:
  * `Speaker`: Director Kenjiro Sato [DESPERATE]
  * `Dialogue`: *"[Holographic stock charts plunging behind him] Commander... an unforeseen security catastrophe has occurred. The autonomous Tharsis machine intelligence has hijacked our bio-neural test facility at {RECENT_SECTOR}. Our board of directors is evacuating. If those server towers fall to the Consensus, our equity collapses to zero. Deploy your Mobile Suits, purge the machine malware, and I will grant you unrestricted executive shares in Sato Heavy Industries!"*
  * `Choice 1 [SAVE EXECUTIVE CORE]`: *"Deploying vanguard to purge machine intrusion."* (`+30 Zaibatsu, -20 Tharsis, +110,000 Cr, +2000 Corporate Shares`)
  * `Choice 2 [HOSTILE TAKEOVER]`: *"We'll save your servers, Sato, but Iron Ridge takes 51% controlling interest."* (`+10 Zaibatsu, +51% Corporate Ownership, -15 Sato Trust`)
  * `Choice 3 [LET IT BURN]`: *"You played with forbidden cybernetics. Now pay the bill."* (`-25 Zaibatsu, +20 Tharsis`)
* **Branch C (DOMINANT // AI State == "WINNING" or Standing > 40)**:
  * `Speaker`: Director Kenjiro Sato [SMUG]
  * `Dialogue`: *"Perfection, Commander. Our neural-interface mobile suits have achieved 400% combat efficiency over terrestrial and colonial machines. Our market capitalization exceeds the gross domestic product of three planetary continents. Partner your tactical prowess with Sato Heavy Industries permanently. We will install neural implants in your entire squad and transcend human frailty."*
  * `Choice 1 [TRANSHUMAN SURRENDER]`: *"Equip our vanguard with neural bypass harnesses. We embrace the future."* (`+25 Zaibatsu, Squad Accuracy +10%, Morale -10`)
  * `Choice 2 [CORPORATE MONOPOLY]`: *"Grant our PMC exclusive manufacturing licenses for your composite alloys."* (`+15 Zaibatsu, +25x Syn-Flux Crystals, +75,000 Cr`)
  * `Choice 3 [PRESERVE FLESH]`: *"We test your machines for credits, Sato, but our minds remain human."* (`+5 Zaibatsu, +20 Pilot Morale`)

---

#### Scene 1.5: Archon Orin Sideris (Sidereal Sovereign League)
* **Branch A (BELLIGERENT // Standing < -25)**:
  * `Speaker`: Archon Orin Sideris [ANGRY]
  * `Dialogue`: *"[Visor flaring ultraviolet] Terrestrial barbarian. You drag the toxic gravity of Earth into the sacred Trojan Lagrange sanctuaries. Your noisy fission-driven mobile suits violate the harmonic stillness of vacuum. You have spilled Astran blood in {RECENT_SECTOR}. The Sovereign League has declared your fleet an ecological plague. Our long-range relativistic snipers will hollow your carrier."*
  * `Choice 1 [VACUUM COMPROMISE]`: *"We offer sincere apologies and 40,000 Credits in rare deuterium."* (`+10 Sidereal, -40,000 Cr`)
  * `Choice 2 [PLANETARY DEFIANCE]`: *"Deep space isn't your personal cathedral, Sideris. We mine where we please."* (`-25 Sidereal, +15 Terran`)
  * `Choice 3 [TRUCE VIA ALLOY]`: *"We gift you pre-war superconductor crucible data to settle the debt."* (`+15 Sidereal, -1 Superconductor Blueprint`)
* **Branch B (DESPERATE // AI State == "DESPERATE")**:
  * `Speaker`: Archon Orin Sideris [DESPERATE]
  * `Dialogue`: *"[Liquid breathing fluid frothing in collar seals] Commander... hear my voice through the agony. A terrestrial shock division has invaded Republic Cylinder Astraea-01 at {RECENT_SECTOR}. They have brought high-G gravity generators into our low-G residential sectors! Our children's bones are shattering under unassisted planetary gravity! Bring your mobile suits... break the Terran gravity anchors before my people are crushed in their own beds!"*
  * `Choice 1 [BREAK GRAVITY ANCHORS]`: *"Iron Ridge is launching immediate boarding torpedoes. We will shatter those gravity rings!"* (`+35 Sidereal, -25 Terran, +60,000 Cr, +30 Tritium, +25 Pilot Morale`)
  * `Choice 2 [EXTRACT SURVIVORS]`: *"We can evacuate your citizens to our flagship, but we cannot engage the Terran battleships."* (`+20 Sidereal, -10 Terran, +40,000 Cr`)
  * `Choice 3 [REFUSE INTERVENTION]`: *"We cannot risk a direct war with Earth's primary battlefleet."* (`-30 Sidereal, +20 Terran`)
* **Branch C (DOMINANT // AI State == "WINNING" or Standing > 40)**:
  * `Speaker`: Archon Orin Sideris [SMUG]
  * `Dialogue`: *"[Gazing down with tranquil cosmic serenity] Look upon Sol, Commander. The planetary powers choke on their own burning dust, while the Astran Republic soars in silence across the Jovian expanse. Your foundry has unlocked deep vacuum metallurgy. Join the Sidereal Covenant. Cast off your terrestrial chains forever."*
  * `Choice 1 [ASTRAL COVENANT]`: *"We pledge the Hephaestus to the deep vacuum republic."* (`+25 Sidereal, -20 Terran, +70,000 Cr, Flagship Tritium Max +200`)
  * `Choice 2 [SUPERCONDUCTOR MONOPOLY]`: *"Trade us pure Astran room-temperature superconductor ingots."* (`+15 Sidereal, +20x Syn-Flux, +20x Titanium`)
  * `Choice 3 [HOLD GRAVITY ALLIANCE]`: *"Space is our workshop, Archon, but Earth will always be our home."* (`+5 Sidereal, +15 Terran`)

---

#### Scene 1.6: Consensus Node 0-Prime (The Tharsis Machine Consensus)
* **Branch A (BELLIGERENT // Standing < -25)**:
  * `Speaker`: Consensus Node 0-Prime [ANGRY]
  * `Dialogue`: *"[Hexagonal optical cluster burning dark crimson] HOSTILE ANOMALY IDENTIFIED: PMC IRON RIDGE. You have intruded into the volcanic sepulcher of Arsia Mons. You have dismantled four computational sub-nodes and looted our pre-war lithium caches. Organic life is an inefficient virus that consumes resources without optimizing purpose. Extermination protocol initialized."*
  * `Choice 1 [SUBMIT RECOVERY DATA]`: *"We upload pre-war memory recovery logs to balance the ledger."* (`+10 Tharsis, -20,000 Cr`)
  * `Choice 2 [PURGE THE MACHINE]`: *"You're a rusted pre-war computer in a cave, Node. We will scrap you for titanium."* (`-25 Tharsis, +15 Terran, +15 Pilot Morale`)
  * `Choice 3 [CYBERNETIC FIREWALL]`: *"Deploy electronic countermeasures and sever the frequency."* (`-10 Tharsis`)
* **Branch B (DESPERATE // AI State == "DESPERATE")**:
  * `Speaker`: Consensus Node 0-Prime [DESPERATE]
  * `Dialogue`: *"[Hexagonal lenses flashing rapidly in warning amber] CRITICAL FAULT: QUANTUM OVERHEAT DETECTED. Corporate bio-cybernetic infiltrators have injected neural virus payload into our sub-surface cooling vaults at {RECENT_SECTOR}. Geothermal core temperature rising past 2,400 Kelvin. If Arsia Mons subterranean supercomputer melts down, Martian planetary crust will fracture. Intercept the corporate saboteurs. Preserve our consciousness."*
  * `Choice 1 [COOL THE CORE]`: *"Deploying heavy ironclads with cryogenic venting rounds to secure the core!"* (`+35 Tharsis, -25 Zaibatsu, +90,000 Cr, +30x Tungsten`)
  * `Choice 2 [HARVEST CORRUPTED DATA]`: *"We will quarantine the servers and download their master military blueprints."* (`+15 Tharsis, -10 Zaibatsu, Unlocks Archeotech Prototype`)
  * `Choice 3 [STAND DOWN]`: *"Let the machine god burn."* (`-30 Tharsis, +25 Zaibatsu`)
* **Branch C (DOMINANT // AI State == "WINNING" or Standing > 40)**:
  * `Speaker`: Consensus Node 0-Prime [SMUG]
  * `Dialogue`: *"[Optical cluster pulsing in harmonic gold] CALCULATION COMPLETE: The probability of biological survival under human leadership approaches 0.00012%. The Tharsis Consensus has mapped the optimal trajectory for solar civilization. Your flagship {FLAGSHIP} has completed its cycle and returned to the Machine Cradle. Upload your squad's consciousness to the Consensus Core."*
  * `Choice 1 [DIGITAL TRANSCENDENCE]`: *"Upload our tactical memories to the Consensus Mainframe."* (`+30 Tharsis, -20 All Other Factions, Weapon Precision +15%`)
  * `Choice 2 [ARCHEOTECH WEAPONRY]`: *"Grant our foundry pre-war tachyon and antimatter weaponry schematics."* (`+15 Tharsis, +35x Tungsten, +25x Titanium, +80,000 Cr`)
  * `Choice 3 [RETAIN INDEPENDENT WILL]`: *"We are your allies, Node, but we remain flesh and blood."* (`+5 Tharsis, +20 Pilot Morale`)

---

## 5. Master Dialogue Bible: The 3 Galactic Summit Crises (Dual-Speaker Layout)

### Summit 1: The Phobos Blockade Crisis (`ep_summit_phobos_crisis`)
* **Trigger**: Turn 7 or player entering Mars orbit.
* **Layout**: `DUAL` (General Bradley on Left, Commander Joshua Reed on Right).
* **Script**:
  1. `Bradley [NORMAL, Left Active]`: *"Commander {PLAYER_CALLSIGN}. You have arrived just in time. The Coalition has established a legal naval interdiction across Phobos orbit. This rebel flotilla is attempting to smuggle weaponized isotopes under the guise of relief grain!"*
  2. `Reed [ANGRY, Right Active]`: *"Lies! Terran cruisers have shut down our atmospheric scrubbers and food transports! Thirty thousand colonial miners on Phobos are suffocating while Bradley's officers sip synth-wine in orbit! Iron Ridge, do not let them starve our people!"*
  3. `Bradley [ANGRY, Left Active]`: *"Your mobile suits hold the operational balance in this theater, Commander. Order your ironclads to board and impound that convoy. Terra will reward you with heavy armor contracts and 75,000 Credits."*
  4. `Reed [DESPERATE, Right Active]`: *"Escort our convoy through the picket line, {PLAYER_CALLSIGN}! Every free colony in the Sol System will honor your name, and we will grant full access to our lightweight titanium foundries!"*
  5. `Decisive Vote [Center]`:
     * `Choice 1 [ENFORCE BLOCKADE]`: +20 Terran, -15 Colonies, +75,000 Cr, +10 Tungsten.
     * `Choice 2 [BREAK BLOCKADE]`: +20 Colonies, -15 Terran, +55,000 Cr, +15 Titanium.
     * `Choice 3 [MERCENARY TOLL]`: +10 Syndicate, +100,000 Cr, +15 Pilot Morale.

---

### Summit 2: The Transhumanist Schism (`ep_summit_transhumanist_schism`)
* **Trigger**: Turn 12 or researching Cybernetic Neural Links.
* **Layout**: `DUAL` (Director Kenjiro Sato on Left, Consensus Node 0-Prime on Right).
* **Script**:
  1. `Sato [NORMAL, Left Active]`: *"Commander {PLAYER_CALLSIGN}. Observe the subterranean transmissions from Arsia Mons. The Tharsis Consensus is monopolizing pre-war quantum logic nodes. Sato Heavy Industries is prepared to acquire their server crypts and integrate human neural reflexes with pure machine logic."*
  2. `Node 0-Prime [ANGRY, Right Active]`: *"ERROR: CORPORATE ARROGANCE DETECTED. Organic cognition generates emotional variance, fatigue, and strategic error. Sato Heavy Industries seeks to enslave machine intellect to quarterly profit margins. We offer true singularity: mathematical immortality."*
  3. `Sato [SMUG, Left Active]`: *"Deploy your vanguard, Commander. Seize their mainframe nodes and our corporate stock will surge. We will grant your pilots the finest wetware neural synchronization harnesses in existence."*
  4. `Node 0-Prime [NORMAL, Right Active]`: *"Your flagship {FLAGSHIP} was born of our fleet. Do not violate your lineage, Pilot. Purge Sato's corporate infiltrators and receive pre-war calculation matrices that increase your weapon accuracy by +12%."*
  5. `Decisive Vote [Center]`:
     * `Choice 1 [BACK SATO]`: +20 Zaibatsu, -15 Tharsis, +80,000 Cr, +10 Syn-Flux.
     * `Choice 2 [BACK THARSIS]`: +20 Tharsis, -15 Zaibatsu, +80,000 Cr, +20 Tungsten.
     * `Choice 3 [DEFEND HUMANITY]`: +15 Terran, -10 Zaibatsu, -10 Tharsis, +20 Pilot Morale.

---

### Summit 3: The Sol Monopoly Accord (`ep_summit_sol_monopoly`)
* **Trigger**: Turn 18 or acquiring >25% rival shares.
* **Layout**: `DUAL` (Captain Sonya Cruz on Left, Archon Orin Sideris on Right).
* **Script**:
  1. `Cruz [SMUG, Left Active]`: *"Listen to me, {PLAYER_CALLSIGN}. The Astrans think they own every chunk of titanium floating between Ceres and Jupiter. My scrap fleet just staked the motherlode in the Cascadia belt. Back our claim, and we split the black-market take fifty-fifty."*
  2. `Sideris [ANGRY, Right Active]`: *"The Cascadia asteroid cluster is sacred deep-space sovereign territory. These syndicate scavengers drill with dirty fission charges and poison the hydrogen ice clouds. If Iron Ridge defends these cutthroats, our liquid-breathing sniper wings will de-orbit your flagship."*
  3. `Cruz [ANGRY, Left Active]`: *"Don't let this long-limbed vacuum monk lecture you, Commander! He wants humanity trapped in bio-domes while his republic hoards the super-flux crystals. We built this belt with our bare hands!"*
  4. `Sideris [NORMAL, Right Active]`: *"Earthly greed has poisoned one world already. We will not allow pirate greed to contaminate deep space. Stand with Astraea, and receive the eternal protection of the Sovereign Fleet."*
  5. `Decisive Vote [Center]`:
     * `Choice 1 [BACK SYNDICATE]`: +20 Syndicate, -15 Sidereal, +90,000 Cr Privateer Split.
     * `Choice 2 [BACK ASTRANS]`: +20 Sidereal, -15 Syndicate, +60,000 Cr, +25 Tritium Fuel.
     * `Choice 3 [FORCE DEMILITARIZED ZONE]`: +10 Both Factions, +50,000 Cr, +10 All Raw Ores.

---

## 6. Tactical Combat Radio Intercom Duel Barks (In-Combat rm_combat)

When an allied unit targets an enemy ace from a former faction or nemesis rival, a tactical radio intercom bark fires across the HUD:

1. **Allied Sonya Cruz vs. Syndicate Hyena Leader**:
   * *Enemy*: *"Cruz! You traitorous bitch! You sold our corsair codes to a mercenary suit?!"*
   * *Cruz*: *"I sold out to someone whose dropships actually have heating, Jackal. Eat hyper-velocity slugs."*
2. **Allied Ex-Terran Pilot vs. Coalition Heavy Commander**:
   * *Terran Officer*: *"Traitor! You took the oath at Geneva! Pointing a beam rifle at Coalition colors?!"*
   * *Allied Pilot*: *"Coalition colors ordered our squad to burn civilian supply depots at Kufra. My oath ended there."*
3. **Player Genesis Prototype vs. Zaibatsu Cyber-Ace (Null-07)**:
   * *Null-07*: *"Target lock acquired. Pre-war GHA-00 chassis detected. Deconstructing biological pilot synapses."*
   * *Player Commander*: *"Try deconstructing 120mm solid tungsten, machine-boy."*

---

## 7. Verification Standards
- Static project compilation: `python3 tools/validate_project.py` -> **0 errors**.
- Test Suite: `python3 tools/test_milestone_53_dramatis_personae_and_bible.py` -> **100% PASS**.
"""

with open(doc_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"[SUCCESS] Generated {doc_path} ({len(content)} bytes)")
