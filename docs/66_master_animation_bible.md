# Master Mobile Suit Animation Bible (v1.0)

**Status:** Canonical Production Standard  
**Scope:** All Mobile Suit sprites, modular weapon overlays, Proving Lab (`obj_DebugManager`), and Tactical Combat (`obj_BattleManager`).

---

## 1. Universal Technical Specification (GameMaker Studio 2)
- **Frame Dimensions:** Strictly `160x160` px per frame in horizontal strips (`*_stripN.png`).
- **Origin / Foot Anchor:** `(80, 145)` (`origin: 9` custom in `.yy`, centered horizontally, feet planted at `y = 145`).
- **Facing Standard:**
  - `xscale = 1`: **3/4 Front-Right** (Allied Attacker).
  - `xscale = -1`: **3/4 Front-Left** (Hostile Defender).
  - Rear views (`*_back_idle`) use `3/4 Rear-Right` (`xscale = 1`).
- **Chroma-Key & Background Removal:**
  - Generate on solid **`#FF00FF` magenta** (never `#FFFFFF` white).
  - Extract via **edge flood-fill** + 1px magenta fringe cleanup (never global color thresholding, which punches pinholes into armor).
  - Slice multi-frame strips along pure-magenta cut columns so adjacent frames never bleed.
- **Automated QA Gate:** Every sprite must pass `python tools/audit_sprites.py` with:
  - `0` missing root/layer PNGs
  - `0` interior 1px pinholes
  - `0` white background halos
  - `0` frozen/identical multi-frame animations

---

## 2. Mandatory Animation State Contract
Every Mobile Suit model must support the following states (no unit may freeze in `idle` while attacking):
1. **`idle`** (4 frames, 6 FPS): Subtle reactor breathing / weapon-ready stance.
2. **`fire_rifle` / `fire_primary`** (4 frames, 10 FPS):
   - Frame 0: Weapon raised & braced, initial trigger spark.
   - Frame 1: Peak recoil kickback, muzzle flash cone, brass/energy discharge.
   - Frame 2: Torso absorbs recoil, flash fades into smoke/plasma trail.
   - Frame 3: Barrel cooling wisp, return to ready stance.
   - **Rule:** Shield must be swung clear/sideways so the barrel and muzzle flash are 100% unobstructed.
3. **`attack_melee`** (4–6 frames, 12 FPS): Wind-up -> lunge/slash arc -> impact follow-through -> recovery.
4. **`boost`** (4 frames, 10 FPS): Forward lean + active vernier exhaust flare.
5. **`hit`** (2–4 frames, 10 FPS): Armor stagger/recoil without clipping limbs.
6. **`destroyed`** (2–4 frames, 8 FPS): Critical spark/smoke collapse into wreckage.
7. **`back_idle`** (4 frames, 6 FPS): Rear 3/4 view for tactical map & Gantry `[R]` inspection.

---

## 3. Barrel Bore, Ejection Port & Firearm Anatomy Standard
- Every Mobile Suit + weapon combination defines `{ muzzle_x, muzzle_y, eject_x, eject_y }` relative to `(80, 145)`.
- Projectiles, tracers, muzzle flashes, and spent brass casings **must** spawn at the exact barrel bore coordinates (calibrated via `SOCKET QA [U]` in the Foundry).
- Rotary/Chain guns must visibly rotate barrels across frames and end with a barrel spin-down & cooling smoke phase.
- **Firearm Anatomy & Magazine Seating:** Rifles must maintain consistent receiver, handguard, stock, and magwell geometry across all frames. Box magazines must be proportionally large, box-shaped (with 3D depth planes), seated **flush inside the receiver magwell** forward of the trigger guard, and aligned perpendicular to the barrel axis.

---

## 4. Two-Phase Combat Clash & Retaliation Choreography
1. **Phase 1 — Attacker Strike:**
   - Attacker raises weapon -> fires projectile(s) from barrel bore (or boosts into melee range).
   - Defender triggers **Hitstop (3 frames) + Hit-Flash + Camera Shake + `hit` / `guard` / `evade` reaction** + floating damage popup.
2. **Phase 2 — Defender Retaliation (`has_counter`):**
   - If the Defender survives, is within weapon range, and is neither `braced` nor `suppressed`:
   - Defender immediately retaliates using **its own equipped weapon's attack method** (ranged barrel fire from its own muzzle socket, or melee dash counter).
3. **Destruction Climax:**
   - At `0 HP`, play internal reactor sparks -> smoke plume -> `destroyed` wreckage frame before clearing the unit.

---

## 5. Production Rollout & Batch Progress
- **Batch 1 (Complete):** Animation Bible v1.0, `tools/audit_sprites.py`, `spr_ms_ironclad_fire_rifle` clean regeneration, `scr_get_mech_barrel_socket` + modular weapon-raise fallback in `scr_draw_animated_mobile_suit.gml`, and 2-phase barrel-socket retaliation in `obj_DebugManager` / `obj_BattleManager`.
- **Batch 2 (Complete):** Bespoke `fire_rifle` (4 frames @ 10 FPS) & `attack_melee` (4 frames @ 12 FPS) imported, QA-approved, and registered in `MechMakerConcept.yyp` for all 3 Player PMC Foundry Lineages (`spr_ms_pmc_aegis_visor_*`, `spr_ms_pmc_colossus_forge_*`, `spr_ms_pmc_stratos_vector_*`) with 0 audit issues.
- **Batch 3 (In Progress — Resuming after Image API Quota Reset at `2026-11-14T22:20:02Z` / 5:20 PM EST):**
  1. **GHA-07 Ironclad Master Base Reference & Core Suite:** Generate clean Master Base Reference (no white halo, FN FAL–inspired all-metal battle carbine with large 3D box magazine seated flush into magwell, curved buckler shield), get Director sign-off, and animate Ironclad's core kit (`idle`, `fire_rifle` with aim-raise anticipation frames, `attack_melee` mace, `boost`, `hit_kinetic`, `destroyed` — dropping chaingun/missiles).
  2. **GML Barrel/Recoil Sync:** Snap `obj_DebugManager/Step_0.gml` 3-round ballistic burst projectile/casing spawns to `scr_get_mech_barrel_socket` + `atk_recoil_x`.
  3. **PMC Foundry & Roster Completion:** Add `boost`, `hit`, `destroyed` for the 3 PMC Foundry Lineages and resolve remaining legacy `[PINHOLES]` / `[WHITE HALO]` audit findings.


