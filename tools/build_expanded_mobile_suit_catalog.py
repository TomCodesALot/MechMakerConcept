import os
import json

DATAFILES_DIR = "datafiles/mobile_suits"
os.makedirs(DATAFILES_DIR, exist_ok=True)

# Helper function to generate standardized mobile suit structs
def create_suit(suit_id, name, short_name, faction_id, manufacturer, era, chassis_class,
                is_mp, mp_idx, doctrine, primary_wep, secondary_wep, sig_feature,
                armor, power, speed, combat, alloy, sprite_asset, rgb_tint, lore):
    return {
        "id": suit_id,
        "name": name,
        "short_name": short_name,
        "faction_id": faction_id,
        "manufacturer": manufacturer,
        "era": era,
        "chassis_class": chassis_class,
        "mass_production_line": is_mp,
        "mass_production_candidate_index": mp_idx,
        "doctrine": doctrine,
        "primary_weapon": primary_wep,
        "secondary_weapon": secondary_wep,
        "signature_feature": sig_feature,
        "armor": armor,
        "power": power,
        "speed": speed,
        "combat": combat,
        "alloy_type": alloy,
        "sprite_asset": sprite_asset,
        "base_color_rgb": rgb_tint,
        "lore": lore
    }

catalog = {}

# ==============================================================================
# 1. TERRAN COALITION LINEAGES (18 SUITS)
# ==============================================================================
# MP Candidates:
# 0: GHA-07 Ironclad
# 1: TH-M04 Ballista
# 2: TH-C02 Centurion
# 3: TH-T09 Trenchcoat

catalog["ms_terran_ironclad_07"] = create_suit(
    "ms_terran_ironclad_07", "GHA-07 Ironclad", "Ironclad", "faction_a", "Valkyrie Heavy Industries", 2,
    "Heavy Assault Wall", True, 0, "Kinetic Trench Fortress & Attrition Anchor",
    "Type-77 120mm Autocannon", "GAU-88 Rotary Heavy Vulcan", "Reinforced Tungsten Frontal Cowl",
    2480, 12, 45, 480, "alloy_tungsten_carbide", "spr_ms_ironclad_idle", [72, 82, 68],
    "The legendary backbone of Earth defense, capable of surviving orbital bombardment."
)
catalog["ms_terran_ballista_04"] = create_suit(
    "ms_terran_ballista_04", "TH-M04 Ballista", "Ballista", "faction_a", "Valkyrie Heavy Industries", 1,
    "Siege Artillery", True, 1, "Quadruped Long-Range Counter-Battery",
    "Twin 200mm Heavy Howitzers", "Point-Defense 30mm Vulcan", "Hydraulic Recoil Spade Anchors",
    2350, 11, 38, 460, "alloy_tungsten_carbide", "spr_ms_ballista_idle", [65, 75, 60],
    "Quadruped heavy fire platform designed to saturate hostile trenches from over the horizon."
)
catalog["ms_terran_centurion_02"] = create_suit(
    "ms_terran_centurion_02", "TH-C02 Centurion", "Centurion", "faction_a", "Valkyrie Heavy Industries", 2,
    "Linebreaker Spearhead", True, 2, "Hydraulic Ram & Heavy Rotary Breaker",
    "GAU-88 Rotary Heavy Vulcan", "Heavy Kinetic Tower Shield", "Overdriven Hydraulic Knee Servos",
    2200, 14, 62, 510, "alloy_tungsten_carbide", "spr_ms_centurion_idle", [64, 76, 60],
    "Aggressive shock assault unit built to smash through perimeter gates and fortified bunkers."
)
catalog["ms_terran_trenchcoat_09"] = create_suit(
    "ms_terran_trenchcoat_09", "TH-T09 Trenchcoat", "Trenchcoat", "faction_a", "Valkyrie Heavy Industries", 1,
    "CQB Grunt Brawler", True, 3, "Close-Quarters Slugs & Reactive Smokescreen",
    "12-Gauge Heavy Slug Autoshotgun", "Pneumatic Trench Spade", "Dense Smokescreen Ejectors",
    2150, 10, 50, 430, "alloy_tungsten_carbide", "spr_ms_trenchcoat_idle", [52, 58, 64],
    "Specialized close-quarters brawler renowned for lethal room-clearing inside domed cities."
)

# Other Terran Chassis:
terran_other = [
    ("ms_terran_bulwark_03", "TCM-03 Bulwark", "Bulwark", 1, "Line Defense", "90mm Rifled Cannon", "Twin HMG", "Ablative Skirt Plating", 1620, 8, 38, 380, "alloy_structural_steel", "spr_ms_ironclad_idle", [70, 78, 65], "Early pre-war line guard with thick cast armor."),
    ("ms_terran_vanguard_01", "TCM-01 Vanguard Scout", "Vanguard", 1, "Recon Scout", "45mm High-Velocity Carbine", "Light Mortar", "High-Gain Radio Mast", 1450, 9, 58, 390, "alloy_structural_steel", "spr_ms_ironclad_idle", [80, 88, 72], "Forward artillery spotter and fast border patrol."),
    ("ms_terran_vance_custom", "GHA-07C Ironclad Commander", "Vance Custom", 2, "Commander Custom", "Type-77B 130mm Long Cannon", "Swarm-16 Missiles", "Tactical Command Antenna Array", 2750, 15, 48, 550, "alloy_tungsten_carbide", "spr_ms_ironclad_idle", [95, 105, 85], "Personal flagship of Cmdr. Marcus Vance with enhanced comms."),
    ("ms_terran_firefly_05", "TH-F05 Firefly Flanker", "Firefly", 2, "Fast Flanker", "Twin 40mm Rotary Guns", "Incendiary Micro-Rockets", "Overheated Thruster Boosters", 1850, 13, 68, 470, "alloy_titanium_aluminide", "spr_ms_ironclad_idle", [82, 92, 70], "Fast skirmisher operating in flanking pincers."),
    ("ms_terran_ironclad_bastion_08", "GHA-08 Ironclad Bastion", "Bastion", 3, "Heavy Bastion", "Twin 150mm Siege Howitzer", "Dual Rotary Vulcans", "Triple-Layer Sintered Slag Plate", 3200, 15, 40, 590, "alloy_tungsten_carbide", "spr_ms_ironclad_idle", [68, 76, 62], "Heavier evolution of the Ironclad designed to withstand naval railguns."),
    ("ms_terran_centurion_assault_02", "VHI-02 Centurion Assault", "Centurion II", 3, "Assault Striker", "GAU-92 Rotary Vulcan", "Assault Ram Shield", "Hydraulic Kick Dampeners", 2950, 18, 58, 620, "alloy_tungsten_carbide", "spr_ms_ironclad_idle", [88, 98, 80], "Up-armored strike chassis optimized for orbital drop breaches."),
    ("ms_terran_siegebreaker_01", "TH-S01 Siegebreaker", "Siegebreaker", 3, "Superheavy Artillery", "280mm Heavy Siege Cannon", "Stabilizer Outriggers", "Blast-Shield Cockpit", 3400, 16, 32, 630, "alloy_tungsten_carbide", "spr_ms_siegebreaker_anchor", [60, 68, 55], "Massive stationary bombardment mech used to reduce Jovian fortresses."),
    ("ms_terran_demolisher_08", "TH-D08 Demolisher", "Demolisher", 3, "Combat Engineer", "Pneumatic Excavation Hammer", "Thermal Cutter", "Reinforced Roll Cage", 3100, 14, 42, 580, "alloy_tungsten_carbide", "spr_ms_ironclad_idle", [75, 82, 68], "Frontline combat engineering mech equipped to clear minefields."),
    ("ms_terran_warhammer_03", "VHI-03 Warhammer Breaker", "Warhammer", 3, "Heavy Stormer", "Quad Rotary Shredder Cannon", "Kinetic Bunker Spike", "Composite Reactive Panels", 3350, 19, 54, 660, "alloy_tungsten_carbide", "spr_ms_ironclad_idle", [72, 80, 66], "Fierce anti-armor stormer with quad-linked gatling cannons."),
    ("ms_terran_behemoth_11", "TCX-11 Behemoth Mk.IV", "Behemoth", 4, "Heavy Dreadnought", "Dual 400mm Hyper-Rail Batteries", "Heavy Point-Defense Grid", "Superheavy Tungsten Monolith Hull", 4800, 22, 35, 720, "alloy_tungsten_carbide", "spr_ms_ironclad_idle", [55, 62, 50], "Colossal planetary dreadnought deploying walking battleship armor."),
    ("ms_terran_titan_04", "VHI-04 Titan Dreadnought", "Titan", 4, "Assault Dreadnought", "Cyclic 200mm Autocannon Battery", "Heavy Shield Projectors", "Tungsten Heavy Exo-Skeleton", 4300, 26, 52, 760, "alloy_tungsten_carbide", "spr_ms_ironclad_idle", [65, 74, 60], "Mobile assault fortress leading planetary invasion armies."),
    ("ms_terran_paladin_03", "TH-P03 Paladin Heavy Escort", "Paladin", 4, "Fleet Escort", "Linear Heavy Rail-Rifle", "Kinetic Dispersal Shield", "Anti-Missile Laser PDS", 4100, 24, 46, 730, "alloy_tungsten_carbide", "spr_ms_ironclad_idle", [78, 88, 70], "Escort guardian armed with anti-missile thermal lasers."),
    ("ms_terran_promethean_02", "TH-X02 Promethean", "Promethean", 4, "Experimental Prototype", "Thermal Plasma Howitzer", "Active Armor Deflection", "Overcharged Reactor Core", 4600, 25, 42, 780, "alloy_tungsten_carbide", "spr_ms_ironclad_idle", [90, 100, 78], "Experimental reactor testbed firing supercritical thermal shells."),
    ("ms_terran_goliath_prime_x01", "VHI-X01 Goliath Prime", "Goliath Prime", 4, "Prototype Juggernaut", "Supercritical Kinetic Ram", "Twin Heavy Siege Railguns", "Indestructible Tungsten Sinter Core", 5400, 24, 32, 810, "alloy_tungsten_carbide", "spr_ms_ironclad_idle", [50, 58, 46], "Terran apex X-chassis prototype capable of trampling enemy lines.")
]

for sid, n, sn, era, c_cls, pw, sw, sf, arm, pwr, spd, cbt, all_t, spr, tint, lore in terran_other:
    catalog[sid] = create_suit(sid, n, sn, "faction_a", "Valkyrie Heavy Industries", era, c_cls, False, -1, "Terran Cohort Doctrine", pw, sw, sf, arm, pwr, spd, cbt, all_t, spr, tint, lore)

# ==============================================================================
# 2. OUTER COLONIES / JOVIAN COALITION LINEAGES (18 SUITS)
# ==============================================================================
# MP Candidates:
# 0: AET-01 Aether
# 1: JCC-Z05 Zephyr
# 2: JCC-K02 Kepler
# 3: JCC-O08 Oberon

catalog["ms_colony_aether_01"] = create_suit(
    "ms_colony_aether_01", "AET-01 Aether", "Aether", "faction_b", "Astraea Orbital Dynamics", 2,
    "High-Vernier Interceptor", True, 0, "Zero-G Agile Superiority & Particle Carbines",
    "Twin High-Yield Beam Carbines", "Beam Saber Monoblade", "Quad Directional Vernier Thruster Bells",
    1820, 16, 85, 490, "alloy_titanium_aluminide", "spr_ms_aether_idle", [40, 75, 125],
    "The graceful pride of the Jovian fleet, out-turning any kinetic war machine in vacuum."
)
catalog["ms_colony_zephyr_05"] = create_suit(
    "ms_colony_zephyr_05", "JCC-Z05 Zephyr", "Zephyr", "faction_b", "Astraea Orbital Dynamics", 1,
    "EW Skirmisher", True, 1, "Sensor Jamming & High-Frequency Pulse Harassment",
    "High-Frequency Pulse Laser Array", "Ventral Chaff Dispersers", "Active Broad-Spectrum ECM Jammer",
    1680, 15, 92, 470, "alloy_titanium_aluminide", "spr_ms_zephyr_idle", [35, 65, 110],
    "Electronic warfare interceptor that blankets battlefield radars in blinding static."
)
catalog["ms_colony_kepler_02"] = create_suit(
    "ms_colony_kepler_02", "JCC-K02 Kepler", "Kepler", "faction_b", "Astraea Orbital Dynamics", 1,
    "Orbital Rail-Sniper", True, 2, "Ultra-Long-Range Linear Kinetic Acceleration",
    "Magnetic Linear Rail-Rifle", "Attitude Thruster Pods", "Targeting Sensor Monocle",
    1720, 14, 78, 480, "alloy_titanium_aluminide", "spr_ms_kepler_idle", [36, 55, 88],
    "Precision sniper unit that destroys hostile reactors from outside visual sensor range."
)
catalog["ms_colony_oberon_08"] = create_suit(
    "ms_colony_oberon_08", "JCC-O08 Oberon", "Oberon", "faction_b", "Astraea Orbital Dynamics", 2,
    "Fleet Guard Escort", True, 3, "Thermal Beam Lances & Point-Defense Shielding",
    "Thermal Beam Lance", "Continuous Beam Point-Defense", "Armored Wing Deflector Shields",
    1950, 17, 80, 510, "alloy_titanium_aluminide", "spr_ms_oberon_idle", [42, 68, 110],
    "Heavy fleet escort unit guarding Jovian gas tankers against pirate boarding torpedoes."
)

colony_other = [
    ("ms_colony_sylph_01", "AOD-01 Sylph Interceptor", "Sylph", 1, "Light Interceptor", "Rapid-Fire Beam Gun", "Light Vernier Pack", "Solar Radiation Shielding", 1280, 11, 88, 390, "alloy_titanium_aluminide", "spr_ms_aether_idle", [30, 60, 105], "Light early patrol chassis guarding outer Jovian listening posts."),
    ("ms_colony_pegasus_09", "JCC-P09 Pegasus Courier", "Pegasus", 1, "High-Speed Courier", "Light Laser Pistol", "Decoy Pods", "Long-Range Communication Laser", 1320, 12, 95, 400, "alloy_titanium_aluminide", "spr_ms_zephyr_idle", [42, 70, 118], "Extremely fast courier ship used to bypass planetary embargo lines."),
    ("ms_colony_cassian_custom", "AET-01C Aether Officer", "Cassian Custom", 2, "Command Interceptor", "Heavy Pulse Accelerator", "Dual Beam Sabers", "Fleet Uplink Command Antenna", 2100, 18, 88, 560, "alloy_titanium_aluminide", "spr_ms_aether_idle", [55, 95, 155], "Gold-trimmed flagship of Capt. Cassian Vane with advanced tactical battle-mapping."),
    ("ms_colony_vector_04", "JCC-V04 Vector", "Vector", 2, "Zero-G Fighter", "Twin Beam Cannons", "Vernier Kick Pods", "Gyro-Stabilized Torso", 1880, 15, 86, 500, "alloy_titanium_aluminide", "spr_ms_aether_idle", [38, 72, 122], "Standard carrier-based vacuum superiority fighter of the Jovian navy."),
    ("ms_colony_aether_striker_02", "AOD-02 Aether Striker", "Aether II", 3, "Assault Interceptor", "High-Energy Beam Cannon", "Twin Beam Sabers", "Afterburner Vernier Ring", 2250, 19, 90, 630, "alloy_titanium_aluminide", "spr_ms_aether_idle", [45, 85, 140], "Enhanced strike model with high-power capacitor discharges."),
    ("ms_colony_helios_06", "JCC-H06 Helios Beam", "Helios", 3, "Beam Skirmisher", "Particle Wave Cannon", "Beam Dagger", "Thermal Radiator Fin Arrays", 2150, 18, 86, 610, "alloy_titanium_aluminide", "spr_ms_aether_idle", [48, 88, 144], "Specialized in sustained energy fire with enormous cooling radiator arrays."),
    ("ms_colony_eclipse_07", "JCC-E07 Eclipse Stealth", "Eclipse", 3, "Optical Recon", "Silenced Particle Sniper", "Black-Body Thermal Shroud", "Passive Sensor Array", 1980, 17, 92, 600, "alloy_titanium_aluminide", "spr_ms_zephyr_idle", [25, 45, 80], "Deep space stealth unit running completely silent on thermal heat sinks."),
    ("ms_colony_nebula_03", "JCC-N03 Nebula Minelayer", "Nebula", 3, "Area Denial", "Smart Energy Minelayer", "Beam Scatter Gun", "Sensor Decoy Disperser", 2300, 18, 76, 590, "alloy_titanium_aluminide", "spr_ms_aether_idle", [36, 68, 115], "Deploys vast minefields of homing smart-mines across orbital choke-points."),
    ("ms_colony_seraphim_03", "AOD-03 Seraphim Apex", "Seraphim", 3, "Apex Interceptor", "Twin Particle Lance Batteries", "Heavy Beam Sabers", "Hexagonal Energy Wings", 2700, 22, 94, 690, "alloy_titanium_aluminide", "spr_ms_aether_idle", [60, 100, 165], "Elite ace unit equipped with shimmering hexagonal beam shield wings."),
    ("ms_colony_archangel_04", "AOD-04 Archangel Dreadnought", "Archangel", 4, "Fleet Flagship", "Dual Spinal Particle Accelerators", "Point-Defense Matrix", "Gravitational Vernier Binders", 3800, 26, 84, 760, "alloy_titanium_aluminide", "spr_ms_aether_idle", [65, 105, 170], "Massive orbital dreadnought commanding colonial fleet defense."),
    ("ms_colony_typhon_01", "JCC-T01 Typhon Missile Frigate", "Typhon", 4, "Missile Cruiser", "Spinal Torpedo Tubes", "VLS Swarm Pods", "Armored Missile Bunkers", 3950, 25, 78, 750, "alloy_titanium_aluminide", "spr_ms_aether_idle", [42, 75, 128], "Walking missile frigate capable of launching 96 smart warheads per salvo."),
    ("ms_colony_chronos_03", "JCC-X03 Chronos Drive", "Chronos", 4, "Tachyon Testbed", "Phase-Shift Beam Blaster", "Tachyon Evasion Drive", "Dimensional Sensor Pod", 3600, 27, 98, 790, "alloy_titanium_aluminide", "spr_ms_zephyr_idle", [50, 95, 160], "Prototype equipped with experimental tachyon verniers enabling instant micro-hops."),
    ("ms_colony_ghost_mirage_x08", "JCC-X08 Ghost Mirage", "Sorren Custom", 4, "Ghost Ace", "Tachyon Pulse Sniper", "Hyper-Mobility Thrusters", "Sensor Phantom Projector", 3500, 28, 100, 810, "alloy_titanium_aluminide", "spr_ms_zephyr_idle", [40, 85, 150], "Masterwork custom unit piloted by Sorren Lin, producing radar holograms."),
    ("ms_colony_astraea_dominus_x01", "AOD-X01 Astraea Dominus", "Astraea Prime", 4, "Apex Super-Fighter", "Super-Singularity Beam Core", "Dimensional Beam Wings", "Active Phase Reflector", 4100, 28, 96, 830, "alloy_titanium_aluminide", "spr_ms_aether_idle", [70, 115, 180], "Colonial pinnacle unit wielding miniature fusion particle blades.")
]

for sid, n, sn, era, c_cls, pw, sw, sf, arm, pwr, spd, cbt, all_t, spr, tint, lore in colony_other:
    catalog[sid] = create_suit(sid, n, sn, "faction_b", "Astraea Orbital Dynamics", era, c_cls, False, -1, "Jovian Fleet Doctrine", pw, sw, sf, arm, pwr, spd, cbt, all_t, spr, tint, lore)

# ==============================================================================
# 3. ARES MERCENARY SYNDICATES (18 SUITS)
# ==============================================================================
# MP Candidates:
# 0: SCR-12 Hyena
# 1: ARC-G04 Gorgon
# 2: ARC-B06 Bloodhound
# 3: ARC-V03 Vandal

catalog["ms_syndicate_hyena_12"] = create_suit(
    "ms_syndicate_hyena_12", "SCR-12 Hyena", "Hyena", "faction_c", "Rustworks Salvage Cartel", 2,
    "Harpoon Scavenger", True, 0, "Scrap Armor Plating & Kinetic Harpoon Grapples",
    "Magnetic Harpoon Tether Launcher", "Double-Barreled 80mm Flak Cannon", "Wreckage Scavenge Claw",
    1980, 10, 60, 460, "alloy_scrap_composite", "spr_ms_hyena_idle", [115, 65, 45],
    "Built from cannibalized military wrecks, the Hyena drags enemy suits into brutal melee."
)
catalog["ms_syndicate_gorgon_04"] = create_suit(
    "ms_syndicate_gorgon_04", "ARC-G04 Gorgon", "Gorgon", "faction_c", "Rustworks Salvage Cartel", 2,
    "Boarding Breaker", True, 1, "Pneumatic Cutter Claws & Thermal Pile-Drivers",
    "Heavy Thermal Cutter Claw", "Pneumatic Armor Pile-Driver", "Hazard Spiked Ramming Breastplate",
    2300, 12, 52, 490, "alloy_scrap_composite", "spr_ms_gorgon_idle", [135, 55, 40],
    "Feared asteroid boarding mech designed to breach titanium bulkheads and crush reactors."
)
catalog["ms_syndicate_bloodhound_06"] = create_suit(
    "ms_syndicate_bloodhound_06", "ARC-B06 Bloodhound", "Bloodhound", "faction_c", "Rustworks Salvage Cartel", 1,
    "Pack Hunter", True, 2, "High-Speed Wheeled Drive & Swarm Rockets",
    "Quad 70mm Swarm Rocket Pods", "Sawed-Off Autocannon", "All-Terrain Wheeled Leg Bogies",
    1850, 9, 72, 440, "alloy_scrap_composite", "spr_ms_bloodhound_idle", [125, 50, 36],
    "Fast wheeled marauder that hunts in packs to ambush isolated military convoys."
)
catalog["ms_syndicate_vandal_03"] = create_suit(
    "ms_syndicate_vandal_03", "ARC-V03 Vandal", "Vandal", "faction_c", "Rustworks Salvage Cartel", 1,
    "Ambush Raider", True, 3, "Flechette Shrapnel & Decoy Flares",
    "Heavy Flechette Autogun", "Scrap Metal Decoy Canister", "Mag-Booster Jump Jets",
    1750, 10, 66, 430, "alloy_scrap_composite", "spr_ms_vandal_idle", [110, 45, 38],
    "Guerilla ambush unit that blankets the area in blinding magnesium flares."
)

syndicate_other = [
    ("ms_syndicate_scrapper_01", "RST-01 Scrapper Grunt", "Scrapper", 1, "Scrap Militia", "60mm Scrap Gun", "Machete Blade", "Welded Sheet Steel Cowl", 1350, 7, 54, 350, "alloy_scrap_composite", "spr_ms_hyena_idle", [95, 50, 35], "Rudimentary combat walker patched together from industrial loaders."),
    ("ms_syndicate_hellhound_02", "ARC-H02 Hellhound Flamer", "Hellhound", 1, "Thermal Torcher", "Pressurized Napalm Projector", "Thermal Harpoon", "External Fuel Drums", 1650, 9, 58, 410, "alloy_scrap_composite", "spr_ms_hyena_idle", [125, 45, 30], "Terror weapon spraying superheated napalm over infantry bunkers."),
    ("ms_syndicate_cruz_custom", "SCR-12C Hyena Warlord", "Cruz Custom", 2, "Warlord Flagship", "Twin Heavy Flak Rippers", "Reinforced Harpoon Tether", "Heavy Reactive Spikes", 2550, 14, 64, 540, "alloy_scrap_composite", "spr_ms_hyena_idle", [145, 60, 42], "Battle-scarred command rig of Sonya Cruz, clad in the armor of defeated Terran aces."),
    ("ms_syndicate_jackal_08", "ARC-J08 Jackal Skirmisher", "Jackal", 2, "Fast Skirmisher", "High-Velocity Slag Gun", "Vibro-Axe", "Jump-Jet Boosters", 1920, 11, 70, 470, "alloy_scrap_composite", "spr_ms_hyena_idle", [118, 62, 42], "Aggressive skirmisher operated by seasoned mercenary contractors."),
    ("ms_syndicate_marauder_02", "RST-02 Marauder Brawler", "Marauder", 3, "Heavy Brawler", "Twin 100mm Sawed-Off Cannons", "Hydraulic Claws", "Welded Tungsten Plates", 2650, 13, 56, 560, "alloy_scrap_composite", "spr_ms_hyena_idle", [128, 58, 40], "Brutal brawler capable of withstanding direct missile hits."),
    ("ms_syndicate_warthog_05", "ARC-W05 Warthog Siege", "Warthog", 3, "Siege Mortar", "300mm Heavy Slag Mortar", "Twin Flak Guns", "Heavy Outrigger Legs", 2950, 12, 42, 580, "alloy_scrap_composite", "spr_ms_gorgon_idle", [115, 55, 36], "Fires dense balls of molten industrial slag over fortress battlements."),
    ("ms_syndicate_ripper_07", "ARC-R07 Ripper Melee", "Ripper", 3, "Melee Specialist", "Dual Motorized Buzz-Saws", "Thermal Cutter", "Armored Forward Mask", 2450, 15, 68, 610, "alloy_scrap_composite", "spr_ms_bloodhound_idle", [125, 50, 36], "Close-combat terror machine with twin industrial circular saws."),
    ("ms_syndicate_scythe_09", "ARC-S09 Scythe Infiltrator", "Scythe", 3, "Stealth Assassin", "Silenced Rail-Crossbow", "Monofilament Net", "Low-Observable Dark Coating", 2150, 14, 76, 590, "alloy_scrap_composite", "spr_ms_hyena_idle", [90, 45, 35], "Silent assassin utilizing monofilament wire to sever limbs in ambushes."),
    ("ms_syndicate_slag_lobber_03", "RST-03 Slag Lobber", "Slag Lobber", 3, "Heavy Support", "Heavy Slag Cannon", "Anti-Personnel Canisters", "Heat-Resistant Cowling", 2800, 14, 48, 620, "alloy_scrap_composite", "spr_ms_gorgon_idle", [122, 54, 38], "Covers the battlefield in sticky, blinding slag that overheats enemy vents."),
    ("ms_syndicate_junker_dread_04", "RST-04 Junker Dreadnought", "Junker King", 4, "Scrap Behemoth", "Scavenged Destroyer Railgun", "Quad Harpoon Turrets", "Composite Scrap Slag Fortress", 4200, 20, 44, 720, "alloy_scrap_composite", "spr_ms_gorgon_idle", [110, 48, 32], "Walking scrapyard monstrosity equipped with guns salvaged from downed warships."),
    ("ms_syndicate_chimera_01", "ARC-C01 Chimera Vanguard", "Chimera", 4, "Elite Hybrid", "Stolen Terran 120mm / Beam Saber", "Swarm Rockets", "Hybrid Titanium-Tungsten Frame", 3800, 22, 65, 750, "alloy_scrap_composite", "spr_ms_hyena_idle", [135, 68, 48], "High-end mercenary flagship combining the finest military components on the black market."),
    ("ms_syndicate_cerberus_04", "ARC-X04 Cerberus Triple-Head", "Cerberus", 4, "Triple-Head Assault", "Triple 120mm Gun Cluster", "Thermal Harpoon Array", "Reinforced Heavy Breastplate", 4100, 21, 54, 760, "alloy_scrap_composite", "spr_ms_gorgon_idle", [140, 58, 38], "Terrifying three-turret assault mech capable of engaging multiple targets."),
    ("ms_syndicate_iron_reaver_09", "ARC-X09 Iron Reaver", "Iron Reaver", 4, "Reaver Flagship", "Dual Heavy Kinetic Rippers", "Thermal Dispersal Ram", "Heavy Reactive Spikes", 4350, 23, 60, 780, "alloy_scrap_composite", "spr_ms_gorgon_idle", [148, 62, 40], "The supreme flagship of pirate armadas, devastating any suit it tackles."),
    ("ms_syndicate_rust_devil_x01", "RST-X01 Rust Devil Prime", "Rust Devil", 4, "Scrap Apex X-Spec", "Supercharged Slag Melter", "Dual Harpoon Winches", "Scrap Kinetic Deflector", 4700, 24, 52, 800, "alloy_scrap_composite", "spr_ms_gorgon_idle", [130, 50, 34], "Legendary prototype chassis welded together by insane pirate foundry masters.")
]

for sid, n, sn, era, c_cls, pw, sw, sf, arm, pwr, spd, cbt, all_t, spr, tint, lore in syndicate_other:
    catalog[sid] = create_suit(sid, n, sn, "faction_c", "Rustworks Salvage Cartel", era, c_cls, False, -1, "Syndicate Raider Doctrine", pw, sw, sf, arm, pwr, spd, cbt, all_t, spr, tint, lore)

# ==============================================================================
# 4. APEX BIO-CYBERNETICS ZAIBATSU (18 SUITS)
# ==============================================================================
# MP Candidates:
# 0: ZAI-03 Muramasa
# 1: ZBT-K07 Kage
# 2: ZBT-R04 Ronin
# 3: ZBT-T09 Tessen

catalog["ms_zaibatsu_muramasa_03"] = create_suit(
    "ms_zaibatsu_muramasa_03", "ZAI-03 Muramasa", "Muramasa", "faction_d", "Hyperion Advanced Tactical Systems", 2,
    "High-Frequency Duelist", True, 0, "Tachyon Katana Blades & Bio-Neural Reflexes",
    "High-Frequency Tachyon Katana", "Arm-Mounted Plasma Fang", "Neural-Jack Reflex Synchronizer",
    1950, 14, 82, 500, "alloy_silicon_carbide", "spr_ms_muramasa_idle", [32, 24, 45],
    "Surgical dueling mech interfaced directly into the pilot's spinal cord via cyber-implants."
)
catalog["ms_zaibatsu_kage_07"] = create_suit(
    "ms_zaibatsu_kage_07", "ZBT-K07 Kage", "Kage", "faction_d", "Hyperion Advanced Tactical Systems", 1,
    "Optical Camo Assassin", True, 1, "Active Prism Invisibility & Needle Railguns",
    "Hyper-Velocity Needle Railgun", "Vibro-Wakizashi Blade", "Active Optical Cloak Emitter Panels",
    1650, 13, 88, 480, "alloy_silicon_carbide", "spr_ms_kage_idle", [24, 18, 35],
    "Stealth assassin chassis that bends light around its hull to vanish in open daylight."
)
catalog["ms_zaibatsu_ronin_04"] = create_suit(
    "ms_zaibatsu_ronin_04", "ZBT-R04 Ronin", "Ronin", "faction_d", "Hyperion Advanced Tactical Systems", 2,
    "Autonomous Carrier", True, 2, "Sub-Drone Escorts & Point-Defense Beams",
    "Sub-Drone Swarm Pod (4x Drones)", "High-Yield Beam Naginata", "Neural Drone Control Processor",
    2100, 16, 75, 520, "alloy_silicon_carbide", "spr_ms_ronin_idle", [26, 20, 35],
    "Coordinates autonomous AI sub-drones that harass enemy flanks with synchronized laser fire."
)
catalog["ms_zaibatsu_tessen_09"] = create_suit(
    "ms_zaibatsu_tessen_09", "ZBT-T09 Tessen", "Tessen", "faction_d", "Hyperion Advanced Tactical Systems", 1,
    "Electronic Dominance", True, 3, "EMP Neural Jammers & Beam Deflector Fans",
    "Broadband EMP Disruptor Emitter", "Armored Beam Deflector Fan", "Active Cyber-Countermeasures",
    1820, 15, 78, 470, "alloy_silicon_carbide", "spr_ms_tessen_idle", [32, 22, 45],
    "Fires concentrated EMP pulses that fry enemy targeting computers and freeze joint hydraulics."
)

zaibatsu_other = [
    ("ms_zaibatsu_shinobi_01", "HATS-01 Shinobi Recon", "Shinobi", 1, "Recon Infiltrator", "Pulse Needle Gun", "Kyu-Dagger", "Chaff Decoy Shuriken", 1380, 10, 84, 380, "alloy_silicon_carbide", "spr_ms_kage_idle", [22, 16, 30], "Corporate security scout deployed for industrial espionage raids."),
    ("ms_zaibatsu_shuriken_02", "ZBT-S02 Shuriken Skirmisher", "Shuriken", 1, "Fast Harasser", "Rotary Micro-Beam Array", "Throwing Blade Dispenser", "Overclocked Servos", 1520, 12, 86, 420, "alloy_silicon_carbide", "spr_ms_muramasa_idle", [30, 22, 42], "Agile harasser equipped with high-speed micro-beam emitters."),
    ("ms_zaibatsu_takahashi_custom", "ZAI-03C Muramasa Executive", "Takahashi Custom", 2, "Executive Custom", "Dual Tachyon Katanas", "Armored Shoulder Shield", "Precognitive Tactical AI Node", 2350, 17, 85, 570, "alloy_silicon_carbide", "spr_ms_muramasa_idle", [45, 32, 60], "Personal masterwork of Director Renzo Takahashi with gold-etched bio-neural circuitry."),
    ("ms_zaibatsu_kamaitachi_03", "ZBT-K03 Kamaitachi Slicer", "Kamaitachi", 2, "High-Speed Slicer", "Twin Thermal Claws", "Beam Slicer Array", "Afterburner Thruster Pods", 1950, 15, 90, 510, "alloy_silicon_carbide", "spr_ms_muramasa_idle", [35, 26, 48], "Rapid strike mech capable of eviscerating unshielded mechs in a single pass."),
    ("ms_zaibatsu_ronin_guardian_02", "HATS-02 Ronin Guardian", "Ronin II", 3, "Heavy Guardian", "Heavy Beam Naginata", "Heavy Energy Shield", "Sub-Drone Interceptor Pod", 2550, 18, 76, 620, "alloy_silicon_carbide", "spr_ms_muramasa_idle", [40, 30, 55], "Defends Zaibatsu research laboratories with heavy energy shields and autonomous drones."),
    ("ms_zaibatsu_oni_05", "ZBT-O05 Oni Heavy Assault", "Oni", 3, "Heavy Brawler", "Crushing Plasma Kanabo", "Twin Torso Autocannons", "Heavy Composite Cyber-Armor", 3100, 16, 62, 640, "alloy_silicon_carbide", "spr_ms_muramasa_idle", [50, 25, 45], "Terrifying heavy assault suit wielding a plasma-charged kanabo club."),
    ("ms_zaibatsu_bushido_01", "ZBT-B01 Bushido Vanguard", "Bushido", 3, "Elite Vanguard", "Hyper-Frequency Blade", "Linear Particle Gun", "Reactive Electronic Shield", 2700, 19, 82, 660, "alloy_silicon_carbide", "spr_ms_muramasa_idle", [42, 34, 58], "Frontline vanguard unit driven by hyper-experienced cybernetically linked pilots."),
    ("ms_zaibatsu_fudo_08", "ZBT-F08 Fudo Defensive Wall", "Fudo", 3, "Energy Bastion", "Twin Particle Diffusers", "Energy Barrier Projector", "Reinforced Anchor Piles", 3300, 20, 52, 650, "alloy_silicon_carbide", "spr_ms_muramasa_idle", [36, 28, 50], "Anchors defense lines by projecting widespread energy barriers that deflect railgun rounds."),
    ("ms_zaibatsu_raiden_03", "HATS-03 Raiden Storm", "Raiden", 3, "Lightning Siege", "Tachyon Storm Blaster", "Arc-Lightning Claws", "Supercapacitor Batteries", 2850, 21, 78, 670, "alloy_silicon_carbide", "spr_ms_muramasa_idle", [45, 35, 65], "Discharges cascading arcs of artificial lightning across multiple enemy mechs."),
    ("ms_zaibatsu_susanoo_04", "HATS-04 Susanoo Emperor", "Susanoo", 4, "Emperor Flagship", "Spinal Tachyon Wave Cannon", "Dual Plasma Katanas", "Hyper-Spatial Barrier Cloak", 4200, 26, 80, 770, "alloy_silicon_carbide", "spr_ms_muramasa_idle", [52, 38, 72], "Supreme cybernetic war machine firing reality-tearing tachyon energy waves."),
    ("ms_zaibatsu_yamato_06", "ZBT-Y06 Yamato Beam Siege", "Yamato", 4, "Heavy Beam Cruiser", "Twin Spinal Beam Batteries", "Smart-Drone Carrier Node", "Composite Silicon Hull", 4400, 25, 60, 760, "alloy_silicon_carbide", "spr_ms_muramasa_idle", [40, 30, 56], "Walking battleship armed with long-range spinal particle beam turrets."),
    ("ms_zaibatsu_kusanagi_05", "ZBT-X05 Kusanagi Blade", "Kusanagi", 4, "Cyber Dueling Ace", "Tachyon Blade Slicer", "Precision Particle Lance", "Bio-Neural Synapse Link", 3800, 27, 92, 800, "alloy_silicon_carbide", "spr_ms_muramasa_idle", [48, 36, 68], "Piloted through complete cerebral symbiosis, mirroring human thought instantaneously."),
    ("ms_zaibatsu_null07_phantom_x07", "ZBT-X07 Null-07 Phantom", "Null-07 Custom", 4, "Cybernetic Phantom", "Silent Tachyon Needle", "Shadow Camo Generator", "Neural Override Wire", 3650, 28, 96, 820, "alloy_silicon_carbide", "spr_ms_kage_idle", [26, 20, 38], "Personal black-ops chassis of Null-07, capable of hacking enemy mechs mid-combat."),
    ("ms_zaibatsu_amaterasu_x01", "HATS-X01 Amaterasu Zero", "Amaterasu Prime", 4, "Apex Cyber Prototype", "Super-Singularity Tachyon Beam", "Hyper-Spatial Phase Blade", "Omni-Shield Matrix", 4600, 28, 88, 840, "alloy_silicon_carbide", "spr_ms_muramasa_idle", [60, 45, 80], "Apex cybernetic prototype wielding forbidden transhumanist quantum processors.")
]

for sid, n, sn, era, c_cls, pw, sw, sf, arm, pwr, spd, cbt, all_t, spr, tint, lore in zaibatsu_other:
    catalog[sid] = create_suit(sid, n, sn, "faction_d", "Hyperion Advanced Tactical Systems", era, c_cls, False, -1, "Zaibatsu Cyber-Dueling Doctrine", pw, sw, sf, arm, pwr, spd, cbt, all_t, spr, tint, lore)

# ==============================================================================
# 5. PLAYER PMC CUSTOM FLAGSHIP BLUEPRINTS (4 SUITS)
# ==============================================================================
catalog["bp_player_vanguard_heavy"] = create_suit(
    "bp_player_vanguard_heavy", "Vanguard Linebreaker [PMC Custom]", "Vanguard", "pmc_player", "Player PMC Hangar", 3,
    "Heavy Assault", False, -1, "Custom PMC Assault Platform",
    "Heavy 120mm Autocannon", "Twin Vulcan Pods", "Modular Sintered Hardpoints",
    2600, 15, 55, 560, "alloy_tungsten_carbide", "spr_ms_ironclad_idle", [60, 100, 140],
    "Player proprietary heavy frontline chassis with modular component hardpoints."
)
catalog["bp_player_stratos_interceptor"] = create_suit(
    "bp_player_stratos_interceptor", "Stratos Interceptor [PMC Custom]", "Stratos", "pmc_player", "Player PMC Hangar", 3,
    "High-Vernier Interceptor", False, -1, "Custom PMC Zero-G Fighter",
    "Twin Beam Carbines", "Beam Saber", "Tuned Vernier Pods",
    1950, 17, 88, 550, "alloy_titanium_aluminide", "spr_ms_aether_idle", [50, 110, 150],
    "Player proprietary interceptor with lightning-fast lateral evasive thrusters."
)
catalog["bp_player_scrapper_brawler"] = create_suit(
    "bp_player_scrapper_brawler", "Scrapper Brawler [PMC Custom]", "Scrapper", "pmc_player", "Player PMC Hangar", 2,
    "Close-Combat Brawler", False, -1, "Custom PMC Boarding Machine",
    "Harpoon Grapple", "Heavy Autoshotgun", "Spiked Ramming Plate",
    2200, 12, 65, 510, "alloy_scrap_composite", "spr_ms_hyena_idle", [130, 80, 50],
    "Player proprietary CQB brawler designed to grapple and crush hostile armor."
)
catalog["bp_player_ghost_sniper"] = create_suit(
    "bp_player_ghost_sniper", "Ghost Recon Sniper [PMC Custom]", "Ghost", "pmc_player", "Player PMC Hangar", 3,
    "Recon Sniper", False, -1, "Custom PMC Precision Platform",
    "Magnetic Railgun", "Sensor Scrambler Chaff", "Passive Sensor Visor",
    1800, 16, 75, 540, "alloy_silicon_carbide", "spr_ms_kage_idle", [40, 50, 70],
    "Player proprietary sniper platform tuned for single-shot lethal cockpit assassinations."
)


# ==============================================================================
# 6. EXPANDED ACES, RIVAL PROTOTYPES & ENDGAME SANDBOX SUITS (24 SUITS -> 100 TOTAL)
# ==============================================================================
expansion_suits = [
    # Terran Aces & Prototypes (+4)
    ("ms_terran_ironclad_custom_cole", "GHA-07X Iron Bastion [Cole Custom]", "Iron Bastion", "faction_a", "Valkyrie Heavy Industries", 3,
     "Heavy Fortress Vanguard", False, -1, "Trench Fortress Doctrine", "Twin 120mm Heavy Autocannons", "Reinforced Frontal Tower Shield", "Tungsten Reactive Mantlet",
     3100, 16, 48, 650, "alloy_tungsten_carbide", "spr_ms_ironclad_idle", [72, 82, 68],
     "Lt. Marcus Cole custom Ironclad, reinforced with doubled tungsten plates to endure close-quarters trench combat."),
    ("ms_terran_centurion_praetorian", "TH-C02P Centurion Praetorian", "Praetorian", "faction_a", "Valkyrie Heavy Industries", 3,
     "Linebreaker Guard", False, -1, "Terran Shock Doctrine", "GAU-99 Rotary Heavy Vulcan", "Hydraulic Kinetic Ram", "Gilded Brass Pauldrons",
     2800, 17, 66, 640, "alloy_tungsten_carbide", "spr_ms_centurion_idle", [68, 80, 62],
     "Elite Terran Coalition guard suit deployed to escort planetary governors and spearhead armor breaches."),
    ("ms_terran_goliath_siege", "TH-G09 Goliath Heavy Howitzer", "Goliath", "faction_a", "Valkyrie Heavy Industries", 4,
     "Quadruped Siege Wall", False, -1, "Planetary Siege Doctrine", "Quad 240mm Siege Howitzers", "Ground Hydraulic Anchor Piles", "Heavy Trench Armor",
     4200, 22, 32, 760, "alloy_tungsten_carbide", "spr_ms_ballista_idle", [55, 65, 52],
     "Colossal quadruped artillery walking fortress capable of flattening entire planetary fortifications."),
    ("ms_terran_valkyrie_odin", "VHD-X02 Odin Dread-Chassis", "Odin", "faction_a", "Valkyrie Heavy Industries", 4,
     "Apex Orbital Bastion", False, -1, "Apex Coalition Doctrine", "Spinal Mass Accelerator Cannon", "Broadband EMP Shield Wall", "Adamantine Composite Hull",
     4600, 26, 40, 810, "alloy_adamantine_carbide", "spr_ms_titan_proto", [58, 66, 56],
     "Valkyrie flagship prototype walking fortress designed to withstand capital ship orbital bombardment."),

    # Colony Aces & Prototypes (+4)
    ("ms_colony_aether_custom_nadia", "AET-01S Starlight Valkyrie [Nadia Custom]", "Starlight", "faction_b", "Jovian Commonwealth Consortium", 3,
     "High-Speed Ace Superiority", False, -1, "High-Vernier Superiority", "Twin Cherenkov Beam Carbines", "Vernier Aero-Skirt Array", "Overclocked Plasma Core",
     2450, 20, 98, 680, "alloy_titanium_aluminide", "spr_ms_aether_idle", [40, 65, 110],
     "Commander Nadia Cruz tuned Aether, fitted with high-efficiency Cherenkov beam carbines and auxiliary verniers."),
    ("ms_colony_zephyr_custom_dahl", "JCC-Z05X Ghost Zephyr [Dahl Custom]", "Ghost Zephyr", "faction_b", "Jovian Commonwealth Consortium", 3,
     "EW Infiltrator & Scout", False, -1, "Colony EW Skirmish", "Pulse Laser Slicer Array", "Phase Jammer Disruption Grid", "Stealth Optical Baffles",
     2150, 18, 102, 660, "alloy_titanium_aluminide", "spr_ms_zephyr_idle", [35, 60, 100],
     "Kira Dahl personal reconnaissance machine, capable of vanishing completely from military radar grids."),
    ("ms_colony_helios_archon", "HOF-X01 Helios Archon", "Helios", "faction_b", "Hyperion Orbital Foundry", 4,
     "Solar Particle Skirmisher", False, -1, "Colony Beam Superiority", "Radiant Solar-Particle Cannon", "Thermal Radiator Wing Fins", "Superheated Mirror Shields",
     3400, 25, 92, 780, "alloy_hyperion_matrix", "spr_ms_oberon_idle", [45, 75, 125],
     "High-orbital skirmisher drawing power directly from concentrated solar collection arrays."),
    ("ms_colony_selene_interceptor", "HOF-X02 Selene Interceptor", "Selene", "faction_b", "Hyperion Orbital Foundry", 4,
     "Apex Deep-Space Interceptor", False, -1, "Zero-G Interception", "Twin Tachyon Linear Rifles", "Micro-Warp Fold Thrusters", "Polar Aerogel Plating",
     3100, 27, 110, 820, "alloy_hyperion_matrix", "spr_ms_kepler_idle", [38, 62, 98],
     "Ultra-fast interceptor built for deep-space fleet interception at interplanetary velocity."),

    # Syndicate Aces & Prototypes (+4)
    ("ms_syndicate_hyena_custom_vance", "SCR-12R Jackal King [Vance Custom]", "Jackal King", "faction_c", "Ares Salvage Guild", 3,
     "Scavenger Warlord", False, -1, "Syndicate Harpoon Swarm", "Dual Magnetic Harpoon Reapers", "Twin 100mm Flak Autocannons", "Reinforced Spiked Cowl",
     2750, 15, 74, 640, "alloy_scrap_composite", "spr_ms_hyena_idle", [135, 55, 40],
     "Jax Vance flagship war machine, adorned with skulls and reinforced with armor ripped from federal cruisers."),
    ("ms_syndicate_gorgon_custom_scrapper", "ARC-G04X Titan Crusher [Guild Master Custom]", "Titan Crusher", "faction_c", "Ares Salvage Guild", 3,
     "Heavy Boarding Breaker", False, -1, "Syndicate CQB Doctrine", "Dual Pneumatic Plasma Piles", "Heavy Scrap Mantlet", "High-Torque Hydraulic Servos",
     3300, 16, 56, 660, "alloy_scrap_composite", "spr_ms_gorgon_idle", [140, 50, 35],
     "Custom masterwork of the Syndicate Scrap-Masters, capable of punching through starship airlocks in seconds."),
    ("ms_syndicate_scrap_chimera", "AJS-X01 Scrap Chimera", "Chimera", "faction_c", "Ares Junk-Works Syndicate", 4,
     "Quad-Arm Brawler", False, -1, "Rogue Ambush Doctrine", "Twin Heavy Howitzers & Dual Power Claws", "Composite Slag Mantlet", "Salvaged Battleship Core",
     4400, 20, 48, 770, "alloy_scrap_composite", "spr_ms_bloodhound_idle", [120, 48, 32],
     "Monstrous 4-armed war machine assembled from parts of four different destroyed faction chassis."),
    ("ms_syndicate_rust_behemoth", "AJS-X02 Rust Behemoth", "Rust Behemoth", "faction_c", "Ares Junk-Works Syndicate", 4,
     "Apex Salvage Dreadnought", False, -1, "Scrap Heavy Armor Doctrine", "Dreadnought Broadside Flak Array", "Hydraulic Armor Vise", "Multi-Layered Armor Slag",
     5000, 22, 35, 800, "alloy_scrap_composite", "spr_ms_vandal_idle", [115, 45, 30],
     "Massive walking scrap fortress with firepower equivalent to an armored cruiser broadside."),

    # Zaibatsu Aces & Prototypes (+4)
    ("ms_zaibatsu_muramasa_custom_renzo", "ZAI-03X Oni-Blade [Renzo Custom]", "Oni-Blade", "faction_d", "Hyperion Advanced Tactical Systems", 3,
     "Supreme Cyber Dueling", False, -1, "Zaibatsu Blade Master", "Twin Tachyon Katanas", "Nanite Self-Repair Matrix", "Gold Lacquered Cyber Armor",
     2900, 22, 90, 710, "alloy_silicon_carbide", "spr_ms_muramasa_idle", [35, 24, 45],
     "Renzo Takahashi supreme dueling mobile suit with neural nanite repair weave and dual high-frequency blades."),
    ("ms_zaibatsu_kage_custom_null07", "ZBT-K07X Void Shinobi [Null-07 Custom]", "Void Shinobi", "faction_d", "Hyperion Advanced Tactical Systems", 4,
     "Sub-Space Assassin", False, -1, "Zaibatsu Shadow Strike", "Tachyon Needle Sniper Rifle", "Active Optical Camo Cloak", "Neural Synapse Overdrive",
     2600, 24, 105, 750, "alloy_silicon_carbide", "spr_ms_kage_idle", [24, 18, 35],
     "Master assassin chassis piloted by Null-07, capable of turning completely invisible before striking."),
    ("ms_zaibatsu_ronin_master", "ZBT-R04M Ronin Shogun", "Ronin Shogun", "faction_d", "Hyperion Advanced Tactical Systems", 4,
     "Drone Carrier Master", False, -1, "Autonomous Swarm Carrier", "Hex-Drone Swarm Carrier Pods", "Dual Plasma Naginatas", "Sub-Neural Command Jack",
     3600, 26, 80, 810, "alloy_silicon_carbide", "spr_ms_ronin_idle", [30, 22, 42],
     "Command carrier coordinating six autonomous combat sub-drones while wielding dual plasma naginatas."),
    ("ms_zaibatsu_tessen_empress", "ZBT-T09E Tessen Empress", "Tessen Empress", "faction_d", "Hyperion Advanced Tactical Systems", 4,
     "Electronic Warfare Apex", False, -1, "Electronic Dominance", "Omni-Directional EMP Burst Array", "Armored Beam Deflector War-Fans", "Cybernetic Neural Baffles",
     3200, 27, 88, 830, "alloy_silicon_carbide", "spr_ms_tessen_idle", [34, 25, 48],
     "Apex electronic warfare mecha capable of shutting down entire battlegroups with directed EMP pulse waves."),

    # Pre-War, Frontier Militia & Endgame Sandbox (+8)
    ("ms_prewar_hephaestus_avatar", "Pre-War Hephaestus Sentinel", "Hephaestus Guard", "faction_a", "Pre-War Sol Arsenal", 1,
     "Autonomous Flagship Escort", False, -1, "Pre-War Lost-Tech Doctrine", "Cherenkov Plasma Broadsword", "Pre-War Aegis Barrier Shield", "Cherenkov Reactor Core",
     4800, 28, 70, 850, "alloy_tachyon_superalloy", "spr_ms_hephaestus_avatar", [32, 45, 70],
     "Autonomous defense mecha discovered slumbering in the reactor depths of the dreadnought Hephaestus."),
    ("ms_prewar_chronos_proto", "Pre-War Chronos Vector", "Chronos", "faction_b", "Pre-War Sol Arsenal", 1,
     "Lost-Tech Tachyon Skirmisher", False, -1, "Pre-War Tachyon Vector", "Tachyon Singularity Cannon", "Temporal Chaff Emitter", "Singularity Reaction Core",
     4100, 27, 95, 830, "alloy_tachyon_superalloy", "spr_ms_hephaestus_avatar", [35, 50, 75],
     "Pre-war prototype harnessing compressed tachyon fields for near-instantaneous evasive maneuvers."),
    ("ms_valkyrie_titan_juggernaut", "VHD-X01 Juggernaut Prime", "Juggernaut", "faction_a", "Valkyrie Heavy Industries", 4,
     "100t Superheavy Bastion", False, -1, "Heavy Trench Fortress", "Quad 140mm Heavy Autocannons", "Reinforced Adamantine Bunker Cowl", "Hydraulic Shock Dampeners",
     5200, 26, 36, 860, "alloy_adamantine_carbide", "spr_ms_titan_proto", [55, 62, 52],
     "Terrifying 100-ton superheavy walking fortress armed with quad synchronized 140mm autocannons."),
    ("ms_rebel_partisan_guerilla", "Frontier Militia Partisan", "Partisan", "faction_c", "Frontier Free Assembly", 2,
     "Improvised Mining Guerrilla", False, -1, "Guerilla Sabotage", "80mm Rock-Cutter Drill", "Heavy Mining Welder", "Reinforced Scrap Shovel",
     1650, 10, 64, 390, "alloy_scrap_composite", "spr_ms_vandal_idle", [100, 60, 45],
     "Industrial mining mobile suit modified with heavy rock-cutters to fight corporate security forces."),
    ("ms_rebel_partisan_striker", "Frontier Vanguard Striker", "Frontier Striker", "faction_c", "Frontier Free Assembly", 2,
     "Improvised Rocket Skirmisher", False, -1, "Guerilla Hit-and-Run", "Pod-Mounted Mining Rockets", "Hydraulic Spiked Shield", "Salvaged Diesel Thrusters",
     1720, 11, 70, 410, "alloy_scrap_composite", "spr_ms_bloodhound_idle", [110, 65, 48],
     "Frontier insurgent machine built from converted ore haulers, armed with jury-rigged mining rockets."),
    ("ms_pirate_corsair_marauder", "Outer Ring Corsair Marauder", "Corsair", "faction_c", "Outer Ring Pirate Fleets", 3,
     "Boarding Raider", False, -1, "Void Piracy Doctrine", "Magnetic Harpoon Drill", "Heavy Breaching Autocannon", "Grappling Winch Cable",
     2300, 14, 78, 520, "alloy_scrap_composite", "spr_ms_hyena_idle", [120, 52, 38],
     "Notorious pirate boarding machine designed to pierce freighter hulls and harvest element cargo."),
    ("ms_ancient_derelict_sentry", "Precursor Derelict Sentry-00", "Sentry-00", "faction_d", "Unknown Precursor", 1,
     "Autonomous Ancient Sentinel", False, -1, "Automated Guardian Routine", "Automated Particle Arc Gun", "Micro-Thruster Array", "Unknown Alloy Chassis",
     3200, 19, 72, 600, "alloy_tachyon_superalloy", "spr_ms_oberon_idle", [40, 55, 80],
     "Mysterious autonomous sentry recovered from an uncharted deep-space derelict station."),
    ("ms_apex_apocalypse_harvester", "Apex Apocalypse Harvester", "Harvester", "faction_a", "Forbidden Cyber-Foundry", 4,
     "Planetary Siege Leviathan", False, -1, "Apex Annihilation", "Singularity Disruption Beam", "Composite Carapace Hull", "Bio-Synthetic Neural Reactor",
     5500, 30, 42, 900, "alloy_adamantine_carbide", "spr_ms_titan_proto", [48, 52, 45],
     "Apocalyptic super-weapon mecha created by unshackled bio-neural research, capable of harvesting planetary crusts.")
]

for sid, n, sn, fid, mfg, era, c_cls, mpl, mpi, doc, pw, sw, sf, arm, pwr, spd, cbt, all_t, spr, tint, lore in expansion_suits:
    catalog[sid] = create_suit(sid, n, sn, fid, mfg, era, c_cls, mpl, mpi, doc, pw, sw, sf, arm, pwr, spd, cbt, all_t, spr, tint, lore)

# Save JSON file
out_path = os.path.join(DATAFILES_DIR, "mobile_suit_catalog.json")
with open(out_path, "w") as f:
    json.dump(catalog, f, indent=2)

# Also save copy in root datafiles/
with open("datafiles/mobile_suit_catalog.json", "w") as f:
    json.dump(catalog, f, indent=2)

print(f"Successfully generated expanded Mobile Suit Catalog with {len(catalog)} suits at {out_path}!")
