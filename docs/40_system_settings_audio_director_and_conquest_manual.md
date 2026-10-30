# System Configuration, Audio Architecture & Planetary Conquest Manual

> [!IMPORTANT]
> **Key Implementations Delivered**:
> 1. **Default Audio Mute**: Game initializes with `master_muted = true` and `audio_master_gain(0.0)`.
> 2. **Tactical Settings Window**: Dedicated retro SNES CRT modal (`[⚙ CONFIG]` / `[⚙ MUTED]` on HUD, hotkey `[O]` or `[ESC]`).
> 3. **Interactive Audio Mixer**: Hero mute/unmute toggle button, preset gain steps (0%, 25%, 50%, 75%, 100%), independent BGM and SFX channels, and `[🔊 TEST SFX]` preview.
> 4. **Quick Mute Hotkey**: Pressing `[M]` toggles master audio on the fly with a floating HUD toast notification.
> 5. **Comprehensive Territory Conquest Map**: Complete 33-territory strategic map across Earth Sphere (10), Space & Colonies (15), and Mars Sphere (8) with Gundam-style inter-faction war declarations, 20% starting balance parity, daily credit/ore supply yields, and Mars quarantine unlocking.

---

## 1. Visual Verification & Interface Proofs

- **Settings Modal (Default Muted)**: `settings_01_modal_audio_tab_muted.png`
- **Settings Modal (Unmuted & Tuned)**: `settings_02_modal_audio_tab_unmuted.png`
- **Settings Tab 2 (Display & Shortcuts)**: `settings_04_modal_display_and_shortcuts_tab.png`
- **Quick Mute Hotkey Toast**: `settings_06_quick_mute_hotkey_toast.png`
- **Earth Sphere (10 Territories, 20% Parity Balanced Starting Frontline)**: `territory_01_earth_sphere_overview.png`
- **Space & Colonies (15 Orbital Sectors, Lagrange Hubs, Asteroid Belts)**: `territory_02_space_and_colonies_sphere.png`
- **Mars Sphere (Quarantined State with Automated Biohazard Security Lock)**: `territory_03_mars_quarantine_sphere.png`
- **Mars Sphere Unlocked (Tharsis Machine Consensus Theaters & Plunder Assault)**: `territory_04_mars_sphere_unlocked_consensus.png`
- **Settings Modal Opened Seamlessly Over Strategic War Map**: `settings_07_opened_over_war_map.png`

---

## 2. Audio Director Architecture & Specification

In accordance with the Lead Audio Engineer and Lead Composer directives:

### Audio State Flow
1. Game Boot (`rm_init`) -> `obj_AudioManager` instantiated.
2. `master_muted = true` -> `audio_master_gain(0.0)` applied immediately.
3. User un-mutes via Hero button in Settings or `[M]` hotkey -> `audio_master_gain(master_volume)` restored.

### Channel Mixer Controls
| Channel | Default State | Presets Available | Hotkey | Engine Hook |
| :--- | :--- | :--- | :--- | :--- |
| **Master Gain** | `Muted (0.0)` | `0%, 25%, 50%, 75%, 100%` | `[M]` / `[O]` | `audio_master_gain()` |
| **BGM (Music)** | `Active (85%)` | `0%, 25%, 50%, 75%, 100%` | Via Settings | `play_bgm()` |
| **SFX (Foley)** | `Active (90%)` | `0%, 25%, 50%, 75%, 100%` | Via Settings | `play_sfx()` |

---

## 3. Planetary & Orbital Territory Conquest System

| Theater Sphere | Territories | Primary Faction Allocation (Turn 1 Parity) | Resource Supply Yields |
| :--- | :---: | :--- | :--- |
| **Earth Sphere** | 10 | 2 Terran, 2 Syndicate, 2 Zaibatsu, 2 Sidereal, 2 Colony | Cr + Titanium, Heavy Composites, Synthetic Flux |
| **Space & Orbital Colonies** | 15 | 3 Colony, 3 Terran, 3 Syndicate, 3 Zaibatsu, 3 Sidereal | Cr + Tritium, Tungsten, Silica Carbide |
| **Mars Sphere** | 8 | Quarantined on Turn 1; Unlocks Turn 15 or via Emergency Override | Cr + Refined Composite, Solar Ferrite, Tachyon Ore |
| **Starting Balance Parity** | **25 Active** | **Exactly 5 Territories (20.0%) Each across all 5 starting factions** | Guaranteed starting parity |

---

## 4. UI Precision & Pixel Audit Summary

- **Screen Resolution**: Target 1366x768 GUI.
- **Top Bar**:
  - `[ADVANCE TURN]`: `x: 588..732`
  - `[LOG]`: `x: 736..790`
  - `[GUIDE]`: `x: 794..864`
  - `[SAVE]`: `x: 868..934`
  - `[RETIRE]`: `x: 938..1006`
  - `[⚙ CONFIG] / [⚙ MUTED]`: `x: 1010..1108` (44px height, high-contrast status and volume level readout)
  - `[COMMANDER BADGE]`: `x: 1114..1348` (ends at 1348px, leaves 18px clean right margin)
- **Settings Modal**: `800x540px` centered at `x: 283, y: 114` (margins: 283px left/right, 114px top/bottom, 0% overflow).
- **War Map CRT Radar**: `740x494px` at `x: 44, y: 188`; Dossier at `x: 800, y: 188` (ends at `x: 1290`, 76px clean right margin).
- **Fatal Error Count**: 0.
