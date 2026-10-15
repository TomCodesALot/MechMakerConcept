# Document 33: Tactical Audio System, Mechanical Soundscapes & Visual Asset Overhaul

**Author**: Audio Team (Lead Composer, Lead Audio Engineer) & Art Team (Art Generator, Concept Artist)  
**Engineering Review**: GameMaker Coder & Lead QA  
**Version**: 1.0.0 (Production Master)  
**Status**: Implemented & Verified in Engine (100% Pass)

---

## 1. Executive Summary

This document establishes the canonical audio architecture and visual asset cleanup for *MechMakerConcept*. In accordance with executive direction:
1. **Audio Engine**: Implemented `obj_AudioManager` and `scr_audio_manager` supporting 31 native 44.1kHz 16-bit sound resources (25 SFX + 6 BGM tracks), continuous crossfading, pitch variance anti-fatigue algorithms, and room/mode routing.
2. **Visual Overhaul**: Eradicated all low-resolution 64x64/128x128 placeholder character sketches and obsolete static mecha sprites (`spr_faction_portraits`, `spr_faction_lineup`, `spr_mech_*`). Retained and explicitly linked the 8 established 200x200 animated portraits across the 204-pilot roster, and mapped all faction doctrines to the 160x160 4-to-5 frame animated isometric mobile suit sheets.

---

## 2. Background Music (BGM) Score & Dynamic Transitions

Composed in the aesthetic of 1990s and early 2000s tactical mecha RPGs (*Front Mission 1/3*, *Classic Gundam* tactical entries), the score utilizes FM-synth percussion, galloping mecha basslines, resonant filter sweeps, and industrial tension drones.

| Sound ID | Location / Trigger Context | Tempo & Key | Instrumentation & Aesthetic | Loop Mode |
| :--- | :--- | :--- | :--- | :--- |
| `bgm_hq_ambience` | Strategic War Map, Faction Dossiers, Diplomacy Matrix, War Room | 84 BPM, D minor | Sub-bass pulse, metallic percussive clicks, dark synth pads, tactical sonar radar pings | Seamless 4-bar Loop |
| `bgm_prototyping_bay` | Prototyping Bay, Thermal Crucible Sintering, CAD Assembly | 108 BPM, A minor | Industrial hydraulic stomp, 16th-note FM synth arpeggios, metallic anvil ticks | Seamless 4-bar Loop |
| `bgm_combat_engage` | Isometric Battle Arena (`rm_combat`), Skirmishes | 132 BPM, E minor | Syncopated FM drums, galloping mecha saw bass, brass chord stabs, heroic lead line | Seamless 4-bar Loop |
| `bgm_nemesis_incursion` | Drop-Pod Atmospheric Incursion, Rival Ace Ambush | 142 BPM, C minor | Distorted industrial percussion, relentless sub-bass slides, tension sirens | Seamless 4-bar Loop |
| `bgm_victory_fanfare` | Combat Victory Screen, Mission Accomplished | 125 BPM, G Major | Triumphant brass synth chords, rolling snare, victorious melodic resolution | One-Shot Stinger (~4.5s) |
| `bgm_defeat_somber` | Platoon Wipeout, Combat Defeat Screen | 72 BPM, D minor | Deep minor cello synth descent, low-frequency impact, somber retreat tail | One-Shot Stinger (~4.5s) |

### Dynamic BGM Crossfading Logic
- Managed by `obj_AudioManager` with linear gain interpolation (`audio_sound_gain`).
- Main tab navigation between Prototyping (Tab 0) and Strategic Planning (Tabs 1–4) triggers seamless 800ms crossfading between `bgm_prototyping_bay` and `bgm_hq_ambience`.
- Entering combat fades into `bgm_combat_engage` (1000ms); arrival of a Nemesis triggers rapid transition into `bgm_nemesis_incursion` (600ms) with warning sirens.

---

## 3. Tactical Sound Effects (SFX) Catalog

### A. Tactical UI Soundscape
* `snd_ui_click`: Tactile mechanical keyboard switch click (dual pulse, 1200Hz + 800Hz snap, duration 0.04s).
* `snd_ui_hover`: Subtle CRT data terminal blip (600Hz triangle wave, duration 0.04s).
* `snd_ui_tab`: Sub-frequency terminal panel shift (180Hz sine glide down to 90Hz, duration 0.08s).
* `snd_ui_confirm`: Resonant dual-tone confirmation chime (E5 659.25Hz -> B5 987.77Hz harmonic sine, duration 0.22s).
* `snd_ui_cancel`: Negative warning double-buzz (160Hz square wave with 2 bursts, duration 0.16s).
* `snd_ui_terminal_boot`: CRT high-voltage capacitor charging whine sweep (400Hz to 8400Hz) + 880Hz ready beep (duration 0.45s).
* `snd_ui_stamp`: Heavy industrial ink/metal trial stamp punch with mechanical clank (duration 0.25s).

### B. Prototyping Minigames & Metallurgy Foley
* `snd_crucible_pour`: Sizzling molten alloy crucible pour, white/pink noise sizzle + bubbling modulation (duration 0.65s).
* `snd_hydraulic_press`: Heavy pneumatic piston stroke (low-frequency thump) + metallic forge stamp clang (duration 0.42s).
* `snd_plasma_weld`: High-voltage electric arc crackle, randomized noise pulses + 120Hz transformer hum (duration 0.50s).
* `snd_discovery_fanfare`: Resonant crystal harmonic discovery arpeggio (C6 -> E6 -> G6 -> C7, duration 0.55s).

### C. Mecha Foley & Locomotion
* `snd_mech_step`: 50-ton hydraulic footstep (sub-bass impact 48Hz + metal servo whine 540Hz, duration 0.38s).
* `snd_mech_boost`: High-output vernier thruster roar, filtered white noise flare with bass rumble (duration 0.50s).
* `snd_mech_servo`: Quick metallic joint servo torque rotation (320Hz to 480Hz glide, duration 0.18s).

### D. Ballistic, Beam & Heavy Ordnance Weapons (With Pitch Randomization)
* `snd_weapon_vulcan`: Rapid heavy rotary vulcan machine gun bark (190Hz square transient + noise burst, duration 0.08s, pitch variation $\pm 0.12$).
* `snd_weapon_cannon_120mm`: Massive concussive artillery detonation (55Hz sub-bass shockwave + 680Hz steel barrel resonance + breech eject click, duration 0.65s).
* `snd_weapon_missile_launch`: Rocket motor ignition & whoosh, rising noise with hollow tube acoustic (duration 0.45s).
* `snd_weapon_beam_rifle`: High-energy particle beam ionization crackle and discharge whine (2200Hz to 180Hz chirp, duration 0.38s).
* `snd_weapon_plasma_blade`: Searing thermal blade ignition whoosh and plasma buzz (duration 0.32s).
* `snd_weapon_railgun`: Hypersonic railgun crack (sharp 2ms impulse) followed by electromagnetic rail hum and capacitor discharge (duration 0.52s).

### E. Impacts, Destruction & Critical Alarms
* `snd_impact_armor`: Metallic armor deflection and ricochet clank (1450Hz resonant ping with fast decay, duration 0.22s).
* `snd_impact_penetrate`: Heavy kinetic armor breach crunch, metal tear + low-frequency impact (duration 0.35s).
* `snd_explosion_small`: Shell explosion and shrapnel scatter (duration 0.45s).
* `snd_explosion_large`: Catastrophic reactor rupture / mobile suit destruction explosion with deep low-end rumble (duration 1.20s).
* `snd_alarm_critical`: Emergency cockpit warning klaxon (dual alternating 820Hz / 620Hz alarm square wave, duration 0.52s).

---

## 4. Visual Asset Overhaul & Cleanup

### A. Eradicated Placeholder Assets
1. **Old Character Profiles**: Eradicated `spr_faction_portraits` (1024x576 static sheet) and all raw 64x64/128x128 test pixel sketches from `docs/assets/`.
2. **Obsolete Static Mecha Sprites**: Completely deleted obsolete single-frame 256x384 sprites (`spr_mech_terran_ironclad`, `spr_mech_colony_aether`, `spr_mech_syndicate_hyena`, `spr_mech_zaibatsu_muramasa`) and `spr_faction_lineup` from disk and `MechMakerConcept.yyp`.

### B. Canonical High-Detail Assets Retained & Linked
1. **200x200 Animated Character Portraits** (12 Frames each, blinking & lip-sync):
   * `spr_portrait_vance`: General Deborah Vance & Terran High Command.
   * `spr_portrait_cole`: Lt. Marcus Cole & frontline combat veterans.
   * `spr_portrait_cassian`: Fleet Commander Cassian Vane & Jovian leadership.
   * `spr_portrait_sorren`: Sorren Lin & deep-space interceptor aces.
   * `spr_portrait_cruz`: Jax 'Jackal' Cruz & Syndicate warlords.
   * `spr_portrait_nadia`: Nadia 'Spark' Ortiz & asteroid belt salvage mechanics.
   * `spr_portrait_renzo`: Renzo Takahashi & Zaibatsu corporate executives.
   * `spr_portrait_null07`: Null-07 (Ren) & cybernetically enhanced test pilots.
   * *Status*: All 204 characters in `characters_roster.json` and `datafiles/characters_roster.json` explicitly mapped to these 8 portraits.
2. **160x160 Animated Mobile Suit Sprites**:
   * All factions and blueprints in `datafiles/factions_lore.json` and `mobile_suit_catalog.json` upgraded to canonical animated sprites (`spr_ms_ironclad_idle`, `spr_ms_aether_idle`, `spr_ms_hyena_idle`, `spr_ms_muramasa_idle`, etc.).

---

## 5. Automated Verification & QA Sign-Off

* **Test Suite**: `tools/test_audio_architecture_and_asset_cleanup.py`
* **Coverage**:
  * 31 / 31 Audio files verified (WAV, YY metadata, YYP registration).
  * 100% GML token balance across `obj_AudioManager`, `scr_audio_manager`, `obj_HQTerminal`, `obj_BattleManager`, and `rm_init`.
  * 6 / 6 Obsolete sprite directories eradicated from filesystem and YYP.
  * 204 / 204 Characters mapped to valid high-detail animated portraits.
  * 13 / 13 Total test suites passing with 0 regressions.
