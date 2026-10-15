# Document 34: Commander Executive Dossier, Cinematic Situation Briefing & Location Visual Polish

**Author**: Lead Dev, Art Team (Art Generator, Concept Artist) & Audio Team (Composer, Audio Engineer)  
**Engineering Review**: GameMaker Coder & Lead QA  
**Version**: 1.0.0 (Production Master)  
**Status**: Implemented & Verified in Engine (100% Pass)

---

## 1. Executive Summary

This document specifies the implementation of:
1. **Player Commander Executive Selection System**: Initial start with an encrypted, greyed-out tactical shadow silhouette (`spr_portrait_commander_silhouette`), with selectable high-detail 200x200 12-frame animated **Male Commander** (`spr_portrait_commander_male` - Alexei Kane) and **Female Commander** (`spr_portrait_commander_female` - Morgan Vance) profiles.
2. **Interactive Solar Schism Situation Briefing**: A two-phase prologue sequence that educates the player on the geopolitical war between the 4 major powers, the neutral PMC operations aboard the experimental dreadnought *Hephaestus*, and core mechanics (metallurgy, modular CAD assembly, defense contracts, and 24-map isometric combat).
3. **Atmospheric Location Backdrops**: Engine-ready 1024x576 high-detail environment backdrops (`spr_loc_hangar_bay` for Prototyping & Factory floors; `spr_loc_war_room` for Strategic War Map & Flagship Bridge).
4. **Complete Audio Synchronization**: Integrated auditory feedback for CRT terminal boot, transmission blips, profile selection clicks, confirmation chimes, and seamless BGM transitions.

---

## 2. Player Commander Executive Profiles

The player's executive profile is managed by [`obj_GameManager`](file:///home/tom/GameMakerProjects/MechMakerConcept/objects/obj_GameManager/obj_GameManager.yy) and rendered via [`scr_draw_composite_portrait`](file:///home/tom/GameMakerProjects/MechMakerConcept/scripts/scr_nemesis_system/scr_nemesis_system.gml) in the top HUD and dossier modals.

| Profile Option | Character Name & Callsign | Sprite Asset & Frames | Doctrine & Passive Trait | Lore & Background |
| :--- | :--- | :--- | :--- | :--- |
| **Tactical Silhouette (Default)** | Commander [CLASSIFIED]<br>`[SHADOW]` | `spr_portrait_commander_silhouette`<br>(4 Frames, 200x200, Pulsing Scanlines) | **Black Ops Logistics**<br>+10% Scrap Salvage, Sintering Volatility Dampening | Encrypted black-budget mercenary profile operating under an anonymous registry. Identity masked behind electronic warfare scramblers. |
| **Male Commander** | Commander Alexei Kane<br>`[RAVEN]` | `spr_portrait_commander_male`<br>(12 Frames, 200x200, Blinking & Speaking) | **Heavy Vanguard**<br>+12% Kinetic Armor, +10% Contract Bounty | Former Terran Naval Strike Commander. Refused orbital saturation orders; founded an independent tactical design bureau. |
| **Female Commander** | Commander Morgan Vance<br>`[VALKYRIE]` | `spr_portrait_commander_female`<br>(12 Frames, 200x200, Blinking & Speaking) | **Vernier Synthesis**<br>+15% Prototyping Stability, +10% Thruster Evasion | Former Colony Fleet Tactical Prodigy. Escaped Jovian corporate conscription to pioneer modular mobile suit metallurgy. |

---

## 3. Interactive Situation Briefing & Game Intro

The prologue sequence launches automatically when `has_completed_intro == false` and can be inspected anytime by clicking the Commander Dossier Badge in the top HUD bar.

### Phase 1: Situation Briefing (`intro_page == 0`)
1. **The Four Belligerent Powers**:
   * **Terran Coalition**: Heavy industrial might, 120mm ordnance, dense composite armor plates (*GHA-07 Ironclad*).
   * **Outer Colony League**: Jovian fleet, vernier thrusters, beam rifles, particle beam sabers (*XMS-01 Aether*).
   * **Rim-Syndicate Cartel**: Asteroid belt reavers, rotary flak, grappling claws, harpoon tethers (*SCR-12 Hyena*).
   * **Apex Zaibatsu**: Corporate monopoly, cybernetic neural pilots, plasma blasters, hostile takeovers (*NZ-99 Muramasa*).
2. **The Flagship *Hephaestus***:
   * Independent neutral base operating at Lagrange Point 5, unbound by sovereign allegiance.
3. **Core Directives**:
   * Thermal Crucible Sintering (alloys & exotic recipes).
   * Modular CAD Mecha Assembly (Heads, Torsos, Arms, Legs, Weapons across 4 locomotion classes).
   * Corporate Design Competitions & Mass-Production Trials.
   * Isometric Tactical Combat across 24 Earth, Space, and Test theaters.

### Phase 2: Commander Appointment (`intro_page == 1`)
* Interactive 3-card layout allowing the player to select the **Tactical Silhouette**, **Male Commander**, or **Female Commander**.
* Shows real-time animated bust preview, doctrine traits, and full narrative bio.
* Confirmation button locks the dossier, plays `snd_ui_confirm` + `snd_ui_terminal_boot`, sets `has_completed_intro = true`, and starts the appropriate location BGM.

---

## 4. Location Environment Visuals & Audio Synchronization

### A. Location Backdrops
* **`spr_loc_hangar_bay`** (1024x576): Rendered behind Tabs 0 (R&D Prototyping) and 1 (Factory Assembly). Features a massive bipedal mobile suit docked within maintenance scaffolding, overhead cranes, steam venting, and hazard stripes.
* **`spr_loc_war_room`** (1024x576): Rendered behind Tabs 2 (Contracts), 3 (War Map), and 4 (Flagship Bridge). Features a glowing celestial holographic table displaying solar system trajectories, telemetry stations, and deep space observation windows.

### B. Audio Synchronization Map
* **Intro Briefing**: Ambient low hum `bgm_hq_ambience`, terminal boot `snd_ui_terminal_boot`, button clicks `snd_ui_click`.
* **Commander Confirmation**: Resonant double-chime `snd_ui_confirm` + capacitor whine `snd_ui_terminal_boot`.
* **Prototyping & Sintering (Tab 0)**: `bgm_prototyping_bay`, molten pour `snd_crucible_pour`, press `snd_hydraulic_press`, weld `snd_plasma_weld`, alloy discovery `snd_discovery_fanfare`.
* **Factory Floor (Tab 1)**: `bgm_prototyping_bay`, pneumatic stamping, modular part slot clicks.
* **War Map & Flagship Bridge (Tabs 3 & 4)**: `bgm_hq_ambience`, celestial transit clicks, division upgrade chimes.
* **Tactical Combat Arena (`rm_combat`)**: `bgm_combat_engage`, drop-pod incursion `bgm_nemesis_incursion` + `snd_alarm_critical`, 6 weapon audio profiles with pitch randomization, kinetic/armor impacts, step/boost movement foley, victory fanfare, and defeat somber.

---

## 5. Automated Verification & QA Sign-Off

* **Test Suite**: `tools/test_commander_dossier_and_intro.py`
* **Coverage**:
  * 5 / 5 New visual assets verified (Dimensions, frame counts, YY metadata, YYP registration).
  * 100% GML token balance across `obj_GameManager`, `obj_HQTerminal`, and `scr_nemesis_system`.
  * Simulated Commander switching between Male, Female, and Silhouette validated.
  * 14 / 14 Total project test suites passing (100% Pass).
