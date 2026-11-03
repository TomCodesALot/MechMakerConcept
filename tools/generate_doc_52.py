import os

doc_content = """# GDD Document 52: Reactive Geopolitical Visual Novel & Multi-Leader Dialogue Engine

**Prepared by:** Lead Game Designer, Lead Narrative Designer & Lead GameMaker Developer  
**Status:** Approved & Engine Integrated  
**Target Engine:** GameMaker Studio 2 (Modern GML)  
**Aesthetic Core:** 16-Bit Super Nintendo / PS1 Tactical Mecha RPG (*Front Mission 3*, *Shin Gihren no Yabou*, *Armored Core*, *Alpha Centauri*)

---

## 1. Executive Summary & Design Vision

Prior to Document 52, faction leader diplomatic audiences operated on static branching dialogues. Regardless of whether the player had just bombed a faction's lunar installation, hired their disgraced former ace into their PMC squad, or captured their star general in the Hephaestus detention brig, leaders responded with identical greetings.

**Document 52 introduces the Reactive Geopolitical Visual Novel Engine (RG-VN)**. This system transforms the visual novel layer into a dynamic, living diplomatic simulation where:
1. **Dynamic Mood Salutations:** Faction leaders evaluate the player's bilateral standing, faction AI mental state (`PEACE`, `STANDARD_WAR`, `DESPERATE`, `WINNING`), and recent combat casualty ratios.
2. **Contextual Incident Barks & Token Interpolation:** Dialogue nodes dynamically inject live telemetry regarding held territories, active pilot rosters, captured prisoners, and flagship engineering feats.
3. **Multi-Speaker War Room Summits:** High-tension 3-way conference intercepts featuring dual-portrait presentation (*Left Speaker vs Right Speaker vs Center Player Deciding Vote*).
4. **Tactical Radio Comms Intercom:** Battlefield radio clashes between pilots and former faction comrades in `rm_combat`.

---

## 2. Pillar I: The Dynamic Contextual Salutation & Mood Engine

Each faction leader possesses 5 distinct emotional states evaluated in real time:

```
[Dynamic Mood Salutation] + [Specific Incident / Grievance Bark] + [Strategic Proposal / Ultimatum]
```

### The 5 Leader Dispositions:
1. **Dominant / Imperial** (`ai_state == "WINNING"` or `standing > 40`):
   - Confident, condescending, demanding tribute or offering high-tier client-state procurement contracts.
2. **Transactional / Cold Mercenary** (`standing between -15 and +15`):
   - Strict cost-benefit balance sheet. Zero ideological pretense; focus on credits, delivery timelines, and kill quotas.
3. **Desperate / Besieged** (`ai_state == "DESPERATE"` or low territory count):
   - Panicked, breathing heavily, offering 2.5x credit bounties, emergency prototype schematics, or rare element reserves if the player launches immediate relief sorties.
4. **Betrayed / Belligerent** (`standing < -30` or player annexed their territory):
   - Boiling rage, declaring the player an outlaw pirate syndicate, threatening orbital kinetic bombardment and total commercial blockades.
5. **Awed / Uneasy** (`timeline_era == 0` or player deploying first Mobile Suits):
   - Bewildered by the technological disparity of the player's humanoid Mobile Suits compared to their conventional tank/jet forces.

---

## 3. Pillar II: Reactive Incident Barks & Token Interpolation

The engine evaluates world state predicates and dynamically replaces tokens in dialogue strings:

- `{PLAYER_NAME}`: Commander callsign / formal name.
- `{FACTION_NAME}`: Target faction display title.
- `{RECENT_SECTOR}`: Name of the latest contested territory sector.
- `{ROSTER_PILOT}`: Name of the player's top-performing squad ace.
- `{BRIG_PRISONER}`: Highest-tier enemy operative currently incarcerated in the Hephaestus Brig.
- `{FLAGSHIP}`: Pre-war dreadnought *USN-X Hephaestus*.

### Reactive Bark Matrix:
| Trigger Condition | Leader | Dynamic Narrative Bark |
|---|---|---|
| **Player holds faction's core sector** | General Arthur Bradley (Terran) | *"You sit in our fortified redoubt at {RECENT_SECTOR} like a conqueror. Every day your scrap machines remain on sovereign Coalition soil brings our orbital fleet closer to full bombardment."* |
| **Faction Ace in Player Roster** | Commander Joshua Reed (Colonies) | *"I see {ROSTER_PILOT} flying on your vanguard. A spacenoid pilot serving a mercenary flag while colonial children breathe recycled exhaust in the outer tubes. What a tragic waste."* |
| **Faction Operative in Base Brig** | Captain Sonya Cruz (Syndicates) | *"My intelligence network reports you're holding {BRIG_PRISONER} in your detention brig. Release them back to the Syndicate, Commander, before our boarding breachers crack your hull from the dark."* |
| **Player fields Cybernetic Pilot** | Consensus Node 0-Prime (Tharsis) | *"Biometric scans indicate severe synthetic neural expansion within your lead pilot {ROSTER_PILOT}. Flesh is an ephemeral transitional state. Surrender their cognitive core to the Consensus."* |
| **Player sinters Superconductor Alloy** | Archon Orin Sideris (Sidereal) | *"The harmonic frequency radiating from your flagship's crucible... you have synthesized pure Astraea-grade superconductors. You understand the music of deep vacuum."* |

---

## 4. Pillar III: Multi-Speaker War Room Summits (Dual-Portrait Presentation)

Key geopolitical milestones trigger multi-faction diplomatic crises rendered in a dual-portrait letterboxed visual novel overlay:
- **Left Portrait Box (148x148)**: Leader A (e.g. General Bradley).
- **Right Portrait Box (148x148)**: Leader B (e.g. Commander Reed).
- **Center Lower Panel**: Cinematic dialogue crawl with active speaker illumination and inactive speaker dimming (0.45 alpha).

### The 3 Canonical Galactic Summits:
1. **The Phobos Blockade Crisis (`ep_summit_phobos_crisis`)**:
   - **Trigger**: Turn 7 or player entering Mars orbit.
   - **Participants**: General Arthur Bradley (Terran) vs Commander Joshua Reed (Colonies).
   - **Conflict**: Terran heavy cruisers blockade Martian shipping lanes; Colony freighters stranded.
   - **Tri-Pillar Agency**:
     - *Terran Coalition Enforcement*: +20 Terran, -15 Colonies, +75,000 Cr, +10 Tungsten.
     - *Colony Flotilla Escort*: +20 Colonies, -15 Terran, +55,000 Cr, +15 Titanium.
     - *Mercenary Neutrality Toll*: +10 Syndicate, +100,000 Cr, +15 Pilot Morale.
2. **The Transhumanist Schism (`ep_summit_transhumanist_schism`)**:
   - **Trigger**: Turn 12 or researching Cybernetic Neural Links.
   - **Participants**: Director Kenjiro Sato (Zaibatsu) vs Consensus Node 0-Prime (Tharsis).
   - **Conflict**: Sato attempts hostile corporate takeover of Tharsis quantum logic nodes.
   - **Tri-Pillar Agency**:
     - *Back Zaibatsu Bio-Cybernetics*: +20 Zaibatsu, -15 Tharsis, +80,000 Cr, +10 Syn-Flux.
     - *Synchronize with Tharsis Hive*: +20 Tharsis, -15 Zaibatsu, +80,000 Cr, +20 Tungsten.
     - *Defend Organic Human Autonomy*: +15 Terran, -10 Zaibatsu, -10 Tharsis, +20 Pilot Morale.
3. **The Sol Monopoly Crisis (`ep_summit_sol_monopoly`)**:
   - **Trigger**: Turn 18 or acquiring >25% rival shares.
   - **Participants**: Captain Sonya Cruz (Syndicates) vs Archon Orin Sideris (Sidereal League).
   - **Conflict**: Syndicate privateers jump claim deep-space asteroid mines belonging to Astraea.
   - **Tri-Pillar Agency**:
     - *Syndicate Privateer Accord*: +20 Syndicate, -15 Sidereal, +90,000 Cr.
     - *Astran High-Orbit Treaty*: +20 Sidereal, -15 Syndicate, +60,000 Cr, +25 Tritium Fuel.
     - *Broker Demilitarized Trade Corridor*: +10 Both, +50,000 Cr, +10 All Resources.

---

## 5. Pillar IV: Tactical Radio Comms Intercom in rm_combat

During tactical combat, hostile aces and allied pilots trigger Front Mission-style radio comms barks:
- **Renderer**: `scr_vn_draw_combat_intercom()` renders a sleek brushed-titanium radio HUD with blinking comms LED, animated static scanlines, pilot portrait, and military radio squelch audio.
- **Triggers**:
  - Targeting an enemy ace whose former faction matches an allied pilot.
  - Catastrophic cockpit ejection of a high-value pilot.
  - Turn 1 hostile commander challenge bark.

---

## 6. Implementation & Data Specifications

### Core GML Scripts & Methods:
- `scr_vn_interpolate_text(_raw_text)`: String token parser replacing `{TOKEN}` with live struct variables.
- `scr_vn_start_dynamic_audience(_faction_id)`: Generates custom 3-node audience matching live world state.
- `scr_vn_trigger_combat_intercom(_speaker, _portrait, _text, _duration, _color)`: Pushes radio barks to battle HUD.
- `scr_vn_draw(_mx, _my, _click)`: Enhanced with `layout == "DUAL"` support for dual-portrait summit rendering.

---

## 7. Verification Standards
- Static project compilation: `python3 tools/validate_project.py` -> 0 errors.
- Test Suite: `python3 tools/test_milestone_52_reactive_vn_dialogue.py` -> 100% PASS.
"""

with open("docs/52_reactive_geopolitical_visual_novel_and_multi_leader_dialogue_engine.md", "w", encoding="utf-8") as f:
    f.write(doc_content)

print("[SUCCESS] Generated docs/52_reactive_geopolitical_visual_novel_and_multi_leader_dialogue_engine.md")
