# GDD Document 51: RPG Systems, Faction Dialogue & Prologue Architecture

## 1. Executive Summary & Vision
This document specifies the end-to-end RPG systems for **MechMakerConcept**, transforming the mercenary management simulation into an immersive 16-bit retro mecha tactical RPG inspired by *Front Mission*, *Armored Core*, *Gundam: Gihren's Greed*, and *Battletech*.

All choices have been aligned via the /grill-me interview between the User and Lead Designer.

---

## 2. Pillar I: Reconfigured Campaign Opening & Prologue Flow

1. **Space Salvager Origin Questionnaire (4-Step Origin Calibration)**:
   - Grounded setting: The player begins as a bottom-of-the-barrel Space Salvager in the Cascadia debris belt before discovering the derelict warship USN-X Hephaestus.
   - **Question I (Past Exile)**: Ex-Terran Mutineer (+10% Kinetic DMG, +10% Accuracy), Escaped Jovian Miner (+15% Evasion, +10% Heat Venting), Cybernetics Fugitive (+15% Crit Chance, ECM Jammer), or Born to the Rust (+25% Salvage, +15% Frame Durability).
   - **Question II (Junk Rig Assembled)**: Jury-Rigged Ironclad (Biped), Jury-Rigged Aero-Striker (High-Mobility), Converted Hover-Sniper (Optic Recon), or Tread-Brawler Demolisher (Heavy Tractor).
   - **Question III (Tactical Instinct)**: Point-Blank Breach (+10% Weapon Damage), Evasive Plasma Decoy (+10% Evasion, +1 AP turn 1), Slick Hustle (+20k Credits, +10 Syndicate Standing), or Unbreakable Bulwark (+15% Torso/Arm Armor).
   - **Question IV (Beacon Discovery)**: Encrypted Military SOS SEC-00, Uncontained Reactor Radiation Flare, or Pirate Comm Intercept Free Salvage.
   - **Step 5 (Dossier Confirmation)**: Custom callsign cycler (RUST-1, VANGUARD, GHOST, ANVIL, VALKYRIE, etc.), portrait switcher (Male, Female, Cybernetic, Shadow), and Rig confirmation before staking salvage claim.

2. **Interactive Prologue Ambush Mission**:
   - Drops into a high-tension intro battle in rm_combat fighting off unmarked pirate/corporate assaulters.
   - Teaches combat fundamentals: movement, part aiming, heat venting, and cockpit status.

3. **Flagship Retrieval & Inaugural VN War Room Episode**:
   - The USN-X Hephaestus retrieves the player, triggering Episode 01 (IRON RIDGE COMMENCEMENT) where Lt. Vance and the Operations Officer officially hand over command of the PMC, unlocking the full Command Deck.

---

## 3. Pillar II: Visual Novel War Room Episodes & Major Faction Figures

1. **Full-Screen 16-Bit Retro VN Overlay**:
   - Scanlines, 128x128 retro portraits with emotional states (NORMAL, ANGRY, SMUG, ALARMED), retro typewriter dialogue ticks.
   - Triggers between strategic turns and after key story battles.

2. **6 Major Faction Contacts**:
   - The Terran Coalition: General Arthur Bradley
   - The Outer Colonies: Commander Joshua Reed
   - Rogue Mercenary Syndicates: Captain Cruz
   - Apex Bio-Cybernetics Zaibatsu: Director Kenjiro Sato
   - The Sidereal Sovereign League: Archon Orin Sideris
   - The Tharsis Machine Consensus: Consensus Node 0-Prime

3. **Tri-Pillar Consequential Agency**:
   - Choices directly shift Faction Standing (-100 to +100), unlock exclusive faction prototypes/contracts, affect Pilot Morale/Loyalty, and present mercenary moral dilemmas.

---

## 4. Pillar III: Pilot Barracks, Cantina Recruitment & RPG Growth

1. **Dedicated [PILOTS/BARRACKS] Deck (Tab 6)**:
   - Top navigation bar: [1] WAR MAP | [2] HANGAR | [3] R&D FORGE | [4] CONTRACTS | [5] FLEET | [6] PILOTS | [Advance] | [Sortie]

2. **Mercenary Cantina Registry**:
   - Generates candidates across 3 Tiers (Greenhorns, Combat Veterans, Legendary Aces) with daily credit salaries and signing bonuses.

3. **Story Defectors & Battlefield POWs**:
   - Unlock unique legendary aces through VN War Room episodes and combat victories.

4. **RPG Progression & XP Perk Trees**:
   - Skill trees with Gunnery (Snipe, Heavy Impact), Piloting (Evasive Burst, Counter-Strike), and Tactics (Squad Rally, Iron Will).
   - Frame Affinity specialization when piloting preferred chassis.

5. **Emergency Ejection & Medical Bay**:
   - Mech destruction triggers cockpit ejection (90% survival, injury recovery timer in Medical Bay, low permadeath risk).

---

## 5. Implementation Roadmap
- **Phase 1 (Immediate Execution)**: Commander Dossier Creation screen & Interactive Prologue Flow.
- **Phase 2**: Visual Novel War Room Episode Engine with Faction Contacts.
- **Phase 3**: Pilot Barracks & Cantina Deck with XP Perk Trees & Ejection Survival.

---

## 6. Verification & Implementation Sign-Off

All phases have been fully executed and verified:
- **Phase 1 (Commander Dossier & Interactive Prologue Flow)**: Fully integrated in `obj_HQTerminal`, `obj_BattleManager`, and `obj_GameManager`.
- **Phase 2 (Visual Novel War Room Episode Engine & 6 Faction Audiences)**: Implemented in `scr_vn_engine` with all 6 faction leaders (Bradley, Reed, Cruz, Sato, Sideris, Node 0-Prime) and campaign milestone episodes (`ep_02_shadows_over_mars`).
- **Phase 3 (Pilot Deck, Frame Affinity, Combat XP & POW Recruitment)**: Fully integrated with Tab 6 Pilots Deck, Cantina registry, medical convalescence, active Frame Affinity resonance (+8% ACC/EVA, +1 AP), and normalized POW defector conversions.
- **Automated Validation**: `python3 tools/validate_project.py` -> 0 errors. `python3 tools/test_milestone_51_rpg_and_prologue.py` -> 100% PASS.
