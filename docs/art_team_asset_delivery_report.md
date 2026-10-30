# Art Team Asset Delivery Report: Replacement of Placeholder Mecha Sprites

**Status:** Completed & Engine-Ready  
**Engine:** GameMaker Studio 2 (v2026.0.0.23)  
**Standard Canvas & Origin:** 160 x 160 px | Origin: (80, 145) (Grounded Center-Foot Socket)  
**Animation Specification:** 4-Frame Hydraulic Idle Cycle (Neutral -> Compression -> Core Pulse -> Recovery)  
**Perspectives:** Front 3/4 Isometric & Rear 3/4 Isometric (`_back_idle` with active backpack vernier thruster flares)

---

## 1. Summary of Completed Assets

All crude geometric polygon placeholders (previously rendered with 6–14 flat colors) have been completely replaced with high-fidelity, shaded 2D retro mecha pixel art matching the gold-standard series (`spr_ms_ironclad_idle`, `spr_ms_aether_idle`, `spr_ms_hyena_idle`).

### Canonical Mass-Production Mobile Suits (13 Chassis)

| Faction | Chassis Model | Primary Sprite Asset | Rear Sprite Asset | Unique Colors | Animation Details |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **Terran Combine** | **TH-C02 Centurion** | `spr_ms_centurion_idle` | `spr_ms_centurion_back_idle` | 8,262 | Spartan tower shield, GAU-88 heavy vulcan, hydraulic suspension bob |
| **Terran Combine** | **TH-M04 Ballista** | `spr_ms_ballista_idle` | `spr_ms_ballista_back_idle` | 7,110 | Quadruped siege artillery walker, twin 200mm howitzers, recoil stabilization |
| **Terran Combine** | **TH-T09 Trenchcoat** | `spr_ms_trenchcoat_idle` | `spr_ms_trenchcoat_back_idle` | 7,460 | Segmented ballistic skirt armor, drum combat slugger, spiked buckler |
| **Jovian Colony** | **JCC-Z05 Zephyr** | `spr_ms_zephyr_idle` | `spr_ms_zephyr_back_idle` | 6,511 | Aerodynamic shoulder flight wings, radome halo sensor, pulse laser carbine |
| **Jovian Colony** | **JCC-K02 Kepler** | `spr_ms_kepler_idle` | `spr_ms_kepler_back_idle` | 6,128 | Shoulder telephoto optical scope, linear magnetic rail-rifle |
| **Jovian Colony** | **JCC-O08 Oberon** | `spr_ms_oberon_idle` | `spr_ms_oberon_back_idle` | 8,198 | Cylindrical point-defense escort, thermal beam lance, beam deflector shield |
| **Rust Syndicate** | **ARC-G04 Gorgon** | `spr_ms_gorgon_idle` | `spr_ms_gorgon_back_idle` | 7,315 | Slag crusher cutter, hydraulic plasma pile-driver spike, chainsaw shield |
| **Rust Syndicate** | **ARC-B06 Bloodhound** | `spr_ms_bloodhound_idle` | `spr_ms_bloodhound_back_idle` | 7,254 | Low-profile quadruped scrapper hound, dual swivel quad-rocket pods |
| **Rust Syndicate** | **ARC-V03 Vandal** | `spr_ms_vandal_idle` | `spr_ms_vandal_back_idle` | 6,708 | Gunmetal/crimson raider, spiked pauldron, drum flechette autogun |
| **Zaibatsu Neo-Tokyo**| **ZBT-K07 Kage** | `spr_ms_kage_idle` | `spr_ms_kage_back_idle` | 4,862 | Carbon-weave stealth assassin, neon cyan tracers, hyper-velocity needle rifle |
| **Zaibatsu Neo-Tokyo**| **ZBT-R04 Ronin** | `spr_ms_ronin_idle` | `spr_ms_ronin_back_idle` | 6,213 | Lacquered crimson/gold samurai kabuto, sode shields, dual sub-drone containers |
| **Zaibatsu Neo-Tokyo**| **ZBT-T09 Tessen** | `spr_ms_tessen_idle` | `spr_ms_tessen_back_idle` | 7,037 | Dual folding EMP war-fans, crackling energy arcs, amethyst cyber-armor |
| **Prototypes & Flagships**| **VHI-04 Titan** | `spr_ms_titan_proto` | `spr_ms_titan_proto_back_idle` | 8,775 | Super-heavy dreadnought fortress, quad chest autocannons, bipod siege cannon |

---

### Modular Custom Chassis & Avatar Sprites

| Category | Sprite Name | Base Model | Unique Colors |
| :--- | :--- | :--- | :---: |
| **Custom Chassis** | `spr_ms_custom_biped_heavy_idle` / `_back_idle` | TH-C02 Centurion Heavy Biped Base | 8,262 |
| **Custom Chassis** | `spr_ms_custom_hover_sniper_idle` / `_back_idle` | JCC-K02 Kepler Long-Range Hover Base | 6,128 |
| **Custom Chassis** | `spr_ms_custom_tread_artillery_idle` / `_back_idle` | TH-M04 Ballista Siege Artillery Base | 7,110 |
| **Custom Chassis** | `spr_ms_custom_aero_striker_idle` / `_back_idle` | JCC-Z05 Zephyr High-Mobility Wing Base | 6,511 |
| **Pre-War Relic** | `spr_ms_hephaestus_avatar` / `_back_idle` | VHI-04 Titan Pre-War Superstructure Base | 8,775 |

---

## 2. Animation Engineering Details

1. **Uniform Grid & Strip Formatting**:
   - Every sprite contains 4 individual frame PNGs mapped to their GameMaker frame UUIDs (`<uuid>.png`).
   - Every sprite contains layer assets (`layers/<uuid>/<layer_id>.png`).
   - Every sprite contains a 640x160 horizontal strip file (`<sprite_name>_strip4.png`) for external sprite sheet slicing.
2. **Mechanical Weight & Suspension**:
   - Lower limbs and contact points remain anchored firmly at `(80, 145)`.
   - Upper torso and heavy mounted weapon systems compress downward by 1-2 px on Frame 1, settling under gravity.
   - Core reactor radiators and visor optical sensors pulse with radiant energy on Frame 2.
   - Frame 3 delivers hydraulic extension dampening before looping back to Frame 0.
3. **Rear Perspective Vernier Flares**:
   - All `_back_idle` sprites feature dynamically animated dual backpack vernier thruster plumes (core flame + radiant plume) keyed to the faction's particle signature.
