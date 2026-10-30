/// @function scr_show_toast(_msg, _col)
function scr_show_toast(_msg, _col = c_white) {
    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.toast_message = _msg;
        obj_HQTerminal.toast_color = _col;
        obj_HQTerminal.toast_timer = 200;
    }
}

/// @description scr_territory_war_system
// Comprehensive Planetary & Orbital Territory Conquest Engine (Doc 39)
// 100% Original Military Sci-Fi Universe: Space Colonies, Earth Sphere & Mars Sphere

function scr_init_territory_database() {
    var _db = {};

    // =========================================================================
    // 1. SPACE & COLONIES THEATER (15 Strategic Orbital Hubs, Cylinders & Citadels)
    // Starting Distribution: 3 Terran (A), 3 Colony (B), 3 Syndicate (C), 3 Zaibatsu (D), 3 Sidereal (E)
    // =========================================================================
    _db.space_kepler_haven = {
        id: "space_kepler_haven",
        name: "Kepler Orbital Haven (L5)",
        region: "SPACE",
        subregion: "Earth-Moon L5 Trojan Cluster",
        loc_sprite_name: "spr_loc_colony_cylinder",
        controlling_faction: "pmc", // Player starting headquarters & charter port!
        starting_faction: "pmc",
        is_unlocked: true,
        daily_credits: 48000,
        material_type: "composite",
        daily_materials: 22,
        defense_rating: 80,
        garrison_unit: "Iron Ridge Veteran Garrison Wing",
        connected_ids: ["space_aethelgard_prime", "space_hyperion_dock", "space_selene_zenith"],
        map_x: 280, map_y: 220,
        lore_brief: "A massive multi-torus orbital sanctuary anchoring the L5 cluster. Kepler Haven serves as the independent charter station where mercenary contractors and mobile suit manufacturers broker private military defense treaties outside territorial hegemony.",
        strategic_value: "Central free-trade drydocks and primary staging port for Iron Ridge PMC operations."
    };

    _db.space_aethelgard_prime = {
        id: "space_aethelgard_prime",
        name: "Aethelgard Prime Cluster (L4)",
        region: "SPACE",
        subregion: "Free Colonies High Orbit Hub",
        loc_sprite_name: "spr_loc_colony_cylinder",
        controlling_faction: "faction_b",
        starting_faction: "faction_b",
        is_unlocked: true,
        daily_credits: 44000,
        material_type: "composite",
        daily_materials: 20,
        defense_rating: 82,
        garrison_unit: "Aethelgard 1st Aerospace Platoon",
        connected_ids: ["space_kepler_haven", "space_halcyon_ring", "space_valkyrie_array"],
        map_x: 140, map_y: 120,
        lore_brief: "Triple-linked O'Neill cylinders spanning thirty kilometers. Inside, terraced green arcologies and artificial lakes thrive beneath solar reflector sails, representing the cultural pinnacle of the independent orbital colonies.",
        strategic_value: "Capital administrative hub and ideological heart of the Free Colonies League."
    };

    _db.space_halcyon_ring = {
        id: "space_halcyon_ring",
        name: "Halcyon Agricultural Torus (L1)",
        region: "SPACE",
        subregion: "Sun-Earth Orbital Meridian",
        loc_sprite_name: "spr_loc_colony_cylinder",
        controlling_faction: "faction_b",
        starting_faction: "faction_b",
        is_unlocked: true,
        daily_credits: 38000,
        material_type: "biomass",
        daily_materials: 18,
        defense_rating: 74,
        garrison_unit: "Colonial Ag-Defense Cohort",
        connected_ids: ["space_aethelgard_prime", "space_valkyrie_array", "space_archon_spire"],
        map_x: 200, map_y: 60,
        lore_brief: "The breadbasket of the inner sphere. Hydroponic centrifuges and climate-controlled biomes produce synthetic grain, cultured proteins, and fresh oxygen canisters for tens of millions of spaceborne civilians.",
        strategic_value: "Controls 35% of all orbital food production and life-support catalyst distribution."
    };

    _db.space_charybdis_gate = {
        id: "space_charybdis_gate",
        name: "Charybdis Vector Relay",
        region: "SPACE",
        subregion: "Outer Orbital Acceleration Ring",
        loc_sprite_name: "spr_loc_colony_cylinder",
        controlling_faction: "faction_b",
        starting_faction: "faction_b",
        is_unlocked: true,
        daily_credits: 36000,
        material_type: "syn_flux",
        daily_materials: 15,
        defense_rating: 78,
        garrison_unit: "Relay Patrol Interceptor Unit",
        connected_ids: ["space_valkyrie_array", "space_vesta_anchorage", "space_tartarus_citadel"],
        map_x: 380, map_y: 60,
        lore_brief: "A series of superconducting magnetic accelerator rings that fling cargo freighters and strike squads across interplanetary transfer vectors toward Mars and the asteroid belt.",
        strategic_value: "High-speed transit gateway connecting cislunar space to outer solar routes."
    };

    _db.space_tartarus_citadel = {
        id: "space_tartarus_citadel",
        name: "Tartarus Orbital Redoubt (L3)",
        region: "SPACE",
        subregion: "Earth-Sun Counter-Orbit Bastion",
        loc_sprite_name: "spr_loc_space_citadel",
        controlling_faction: "faction_a",
        starting_faction: "faction_a",
        is_unlocked: true,
        daily_credits: 46000,
        material_type: "titanium",
        daily_materials: 20,
        defense_rating: 92,
        garrison_unit: "Terran 7th Heavy Orbital Fleet",
        connected_ids: ["space_charybdis_gate", "space_ironspire_bastion", "space_archon_spire"],
        map_x: 520, map_y: 110,
        lore_brief: "Armored in meter-thick carbon-steel and bristling with dual spinal rail batteries. Tartarus watches over the counter-orbit Lagrange point, preventing surprise colonial fleet maneuvers around the sun's blind spot.",
        strategic_value: "Impregnable Terran naval bastion locking down the L3 counter-orbital approach."
    };

    _db.space_archon_spire = {
        id: "space_archon_spire",
        name: "Archon Geostationary Anchor",
        region: "SPACE",
        subregion: "Atlantic Orbital Tether Apex",
        loc_sprite_name: "spr_loc_colony_cylinder",
        controlling_faction: "faction_a",
        starting_faction: "faction_a",
        is_unlocked: true,
        daily_credits: 52000,
        material_type: "tungsten",
        daily_materials: 24,
        defense_rating: 88,
        garrison_unit: "Terran Tether Guard Division",
        connected_ids: ["space_halcyon_ring", "space_tartarus_citadel", "space_selene_zenith"],
        map_x: 360, map_y: 150,
        lore_brief: "The orbital counterweight crown of the Atlantic Space Elevator. Maglev cargo climbers ascend the 36,000-kilometer carbon nanotube ribbon day and night, ferrying terrestrial troops and munitions into high orbit.",
        strategic_value: "Primary strategic logistical link between Earth surface factories and orbital fleets."
    };

    _db.space_vesta_anchorage = {
        id: "space_vesta_anchorage",
        name: "Vesta Perimeter Outpost",
        region: "SPACE",
        subregion: "Cislunar Deep Early Warning Line",
        loc_sprite_name: "spr_loc_space_citadel",
        controlling_faction: "faction_a",
        starting_faction: "faction_a",
        is_unlocked: true,
        daily_credits: 32000,
        material_type: "titanium",
        daily_materials: 14,
        defense_rating: 76,
        garrison_unit: "Perimeter Radar Sentry Flight",
        connected_ids: ["space_charybdis_gate", "space_nadir_scrapyard", "space_ironspire_bastion"],
        map_x: 480, map_y: 50,
        lore_brief: "Long-range radar antennas and passive infrared telescope arrays sweep the vacuum, detecting unauthorized warp signatures or cold-drifting stealth strike mecha thousands of kilometers out.",
        strategic_value: "Early warning telemetry and outer orbital sensor dominance."
    };

    _db.space_pelican_refinery = {
        id: "space_pelican_refinery",
        name: "Pelican Deep Slagfield",
        region: "SPACE",
        subregion: "Wreckage Belt & Smelting Hub",
        loc_sprite_name: "spr_loc_space_citadel",
        controlling_faction: "faction_c",
        starting_faction: "faction_c",
        is_unlocked: true,
        daily_credits: 40000,
        material_type: "tungsten",
        daily_materials: 22,
        defense_rating: 75,
        garrison_unit: "Syndicate Enforcer Reclaimers",
        connected_ids: ["space_ironspire_bastion", "space_nadir_scrapyard", "space_hyperion_dock"],
        map_x: 580, map_y: 220,
        lore_brief: "Thousands of twisted starship hulls and shattered colony bulkheads drift through this industrial graveyard. Prometheus smelting barges melt wreckage down into raw unrefined ingot plates away from corporate regulators.",
        strategic_value: "Black-market metallurgical reclamation hub and clandestine refit yard."
    };

    _db.space_nadir_scrapyard = {
        id: "space_nadir_scrapyard",
        name: "Nadir Salvage Expanse",
        region: "SPACE",
        subregion: "Southern Orbital Debris Field",
        loc_sprite_name: "spr_loc_space_citadel",
        controlling_faction: "faction_c",
        starting_faction: "faction_c",
        is_unlocked: true,
        daily_credits: 35000,
        material_type: "scrap_alloy",
        daily_materials: 20,
        defense_rating: 70,
        garrison_unit: "Scavenger Swarm Corsairs",
        connected_ids: ["space_pelican_refinery", "space_vesta_anchorage", "space_ironspire_bastion"],
        map_x: 620, map_y: 140,
        lore_brief: "A lawless zone where freelance scavengers, deserters, and privateers strip forgotten warships for rare catalyst cores, intact reactor valves, and forgotten mobile suit frames.",
        strategic_value: "Abundant salvage reserves and covert contraband transit routes."
    };

    _db.space_valkyrie_array = {
        id: "space_valkyrie_array",
        name: "Valkyrie Solar Array",
        region: "SPACE",
        subregion: "High-Energy Microwave Transmitter",
        loc_sprite_name: "spr_loc_colony_cylinder",
        controlling_faction: "faction_c",
        starting_faction: "faction_c",
        is_unlocked: true,
        daily_credits: 42000,
        material_type: "syn_flux",
        daily_materials: 16,
        defense_rating: 76,
        garrison_unit: "Syndicate Grid Defense Squad",
        connected_ids: ["space_aethelgard_prime", "space_halcyon_ring", "space_charybdis_gate"],
        map_x: 290, map_y: 70,
        lore_brief: "Spanning forty square kilometers of photovoltaic film, the Valkyrie Array beams terawatts of microwave power across cislunar space to power factories and recharge mobile suit batteries.",
        strategic_value: "Controls wireless microwave power beaming throughout the orbital theater."
    };

    _db.space_selene_zenith = {
        id: "space_selene_zenith",
        name: "Port Selene Crater Metropolis",
        region: "SPACE",
        subregion: "Lunar North Polar Geodesic Rim",
        loc_sprite_name: "spr_loc_luna_city",
        controlling_faction: "faction_d",
        starting_faction: "faction_d",
        is_unlocked: true,
        daily_credits: 55000,
        material_type: "titanium",
        daily_materials: 26,
        defense_rating: 86,
        garrison_unit: "Kurogane Lunar Special Security",
        connected_ids: ["space_kepler_haven", "space_archon_spire", "space_daedalus_foundry"],
        map_x: 230, map_y: 280,
        lore_brief: "Tucked inside the permanently shadowed rim of crater Peary, Port Selene gleams beneath pressurized transparent domes. Automated Kurogane extractors harvest trillions of tons of pure water-ice and titanium ores.",
        strategic_value: "Premier lunar financial exchange and heavy metals extraction metropolis."
    };

    _db.space_daedalus_foundry = {
        id: "space_daedalus_foundry",
        name: "Daedalus Lunar Farside Works",
        region: "SPACE",
        subregion: "Deep Lunar Bedrock Foundries",
        loc_sprite_name: "spr_loc_luna_city",
        controlling_faction: "faction_d",
        starting_faction: "faction_d",
        is_unlocked: true,
        daily_credits: 48000,
        material_type: "composite",
        daily_materials: 24,
        defense_rating: 84,
        garrison_unit: "Zaibatsu Prototype Defense Unit",
        connected_ids: ["space_selene_zenith", "space_borealis_port", "space_hyperion_dock"],
        map_x: 350, map_y: 310,
        lore_brief: "Shielded by hundreds of kilometers of solid moon rock from Earth radar monitoring, Kurogane heavy fabrication plants forge experimental next-generation mobile suit armatures and high-density armor plates.",
        strategic_value: "Classified prototyping proving grounds for advanced robotic weaponry."
    };

    _db.space_borealis_port = {
        id: "space_borealis_port",
        name: "Port Borealis Cryo-Depot",
        region: "SPACE",
        subregion: "Lunar South Polar Ice Basins",
        loc_sprite_name: "spr_loc_luna_city",
        controlling_faction: "faction_d",
        starting_faction: "faction_d",
        is_unlocked: true,
        daily_credits: 42000,
        material_type: "syn_flux",
        daily_materials: 18,
        defense_rating: 80,
        garrison_unit: "Cryo-Depot Automaton Cadre",
        connected_ids: ["space_daedalus_foundry", "space_hyperion_dock", "space_selene_zenith"],
        map_x: 180, map_y: 320,
        lore_brief: "Cold-storage propellant tanks hold liquid hydrogen and liquid oxygen drilled from lunar permafrost. Fleets dock here to top off fusion reaction mass before launching combat burns.",
        strategic_value: "Monopolizes cryogenic rocket propellant and reaction mass supplies."
    };

    _db.space_ironspire_bastion = {
        id: "space_ironspire_bastion",
        name: "Ironspire Asteroid Bastion (L2)",
        region: "SPACE",
        subregion: "Earth-Moon L2 Hollowed Rock",
        loc_sprite_name: "spr_loc_space_citadel",
        controlling_faction: "faction_e",
        starting_faction: "faction_e",
        is_unlocked: true,
        daily_credits: 50000,
        material_type: "tungsten",
        daily_materials: 24,
        defense_rating: 94,
        garrison_unit: "Sidereal Ascendant Vanguard",
        connected_ids: ["space_tartarus_citadel", "space_pelican_refinery", "space_hyperion_dock"],
        map_x: 480, map_y: 280,
        lore_brief: "A massive metallic celestial asteroid hollowed out over four decades. Its interior houses sprawling cathedral hangars, while its outer crags mount colossal spinal railguns and automated anti-ship missile batteries.",
        strategic_value: "The supreme military Gibraltar of high cislunar orbit, guarding the L2 approaches."
    };

    _db.space_hyperion_dock = {
        id: "space_hyperion_dock",
        name: "Hyperion Orbital Shipyards",
        region: "SPACE",
        subregion: "Deep Space Zero-G Drydock Web",
        loc_sprite_name: "spr_loc_space_citadel",
        controlling_faction: "faction_e",
        starting_faction: "faction_e",
        is_unlocked: true,
        daily_credits: 46000,
        material_type: "composite",
        daily_materials: 22,
        defense_rating: 85,
        garrison_unit: "Sidereal Shipyard Defense Wing",
        connected_ids: ["space_kepler_haven", "space_ironspire_bastion", "space_pelican_refinery"],
        map_x: 420, map_y: 240,
        lore_brief: "Gantry lattices stretching twelve kilometers across open space. Capital battleships and carrier dreadnoughts are assembled from prefabricated structural ribs under zero gravity.",
        strategic_value: "Primary heavy warship slipways and mass fleet construction facility."
    };

    // =========================================================================
    // 2. EARTH SPHERE THEATER (10 Continental Citadels & Bastions)
    // Starting Distribution: 2 Terran (A), 2 Colony (B), 2 Syndicate (C), 2 Zaibatsu (D), 2 Sidereal (E)
    // =========================================================================
    _db.earth_granite_redoubt = {
        id: "earth_granite_redoubt",
        name: "Granite Deep Command",
        region: "EARTH",
        subregion: "Amazonian Continental Bedrock Citadel",
        loc_sprite_name: "spr_loc_earth_granite",
        controlling_faction: "faction_a",
        starting_faction: "faction_a",
        is_unlocked: true,
        daily_credits: 46000,
        material_type: "titanium",
        daily_materials: 20,
        defense_rating: 92,
        garrison_unit: "Terran 1st Heavy Armored Division",
        connected_ids: ["earth_cascadia_driver", "earth_andes_battery", "earth_gibraltar_redoubt"],
        map_x: 210, map_y: 260, global_map_x: 540, global_map_y: 480, is_major_stronghold: true,
        lore_brief: "A colossal fortress excavated three thousand meters into ancient South American granite. Deep subterranean aquifers cool gigawatt fusion plants, while disguised missile silos and blast gates launch squadrons directly into the clouds.",
        strategic_value: "Supreme subterranean headquarters of the Terran Coalition military staff."
    };

    _db.earth_cascadia_driver = {
        id: "earth_cascadia_driver",
        name: "Cascadia Mass-Driver Complex",
        region: "EARTH",
        subregion: "Pacific Mountain Launch Corridor",
        loc_sprite_name: "spr_loc_earth_granite",
        controlling_faction: "faction_a",
        starting_faction: "faction_a",
        is_unlocked: true,
        daily_credits: 44000,
        material_type: "tungsten",
        daily_materials: 22,
        defense_rating: 86,
        garrison_unit: "Cascadia Coastal Battery Regiment",
        connected_ids: ["earth_granite_redoubt", "earth_shanghai_arcology", "earth_nordic_vault"],
        map_x: 120, map_y: 130, global_map_x: 270, global_map_y: 240, is_major_stronghold: true,
        lore_brief: "A forty-kilometer electromagnetic catapult rail scaling the coastal mountain peaks. Launch sleds accelerate armored drop pods, heavy cargo shells, and strike craft into orbit every ninety seconds.",
        strategic_value: "Primary Pacific launch corridor supplying terrestrial forces to orbit."
    };

    _db.earth_sahara_array = {
        id: "earth_sahara_array",
        name: "Al-Kufra Solar Citadel",
        region: "EARTH",
        subregion: "North African Photovoltaic Basin",
        loc_sprite_name: "spr_loc_earth_granite",
        controlling_faction: "faction_b",
        starting_faction: "faction_b",
        is_unlocked: true,
        daily_credits: 38000,
        material_type: "syn_flux",
        daily_materials: 18,
        defense_rating: 78,
        garrison_unit: "Colonial Expeditionary Legion",
        connected_ids: ["earth_gibraltar_redoubt", "earth_ural_arsenal", "earth_andes_battery"],
        map_x: 340, map_y: 190, global_map_x: 740, global_map_y: 375, is_major_stronghold: true,
        lore_brief: "Tens of thousands of polished mirror heliostats focus blinding sunlight into central thermal towers. The facility generates immense synthetic fuel stores and powers long-range surface-to-air energy batteries.",
        strategic_value: "Energy nexus commanding the North African and Mediterranean skies."
    };

    _db.earth_andes_battery = {
        id: "earth_andes_battery",
        name: "Chimborazo Orbital Bastion",
        region: "EARTH",
        subregion: "High-Altitude Equatorial Ridge",
        loc_sprite_name: "spr_loc_earth_granite",
        controlling_faction: "faction_b",
        starting_faction: "faction_b",
        is_unlocked: true,
        daily_credits: 36000,
        material_type: "composite",
        daily_materials: 16,
        defense_rating: 82,
        garrison_unit: "Andes Mountain Mobile Skirmishers",
        connected_ids: ["earth_granite_redoubt", "earth_sahara_array", "earth_cascadia_driver"],
        map_x: 170, map_y: 220, global_map_x: 320, global_map_y: 420, is_major_stronghold: true,
        lore_brief: "Perched six thousand meters above sea level along the volcanic spine of the Andes. Its thin atmosphere allows heavy kinetic cannons to fire directly into low Earth orbit without thermal blooming.",
        strategic_value: "High-altitude anti-orbital gun platform interdicting equatorial passes."
    };

    _db.earth_gibraltar_redoubt = {
        id: "earth_gibraltar_redoubt",
        name: "Gibraltar Sea Gate Bastion",
        region: "EARTH",
        subregion: "Strait of Gibraltar Coastal Bunkers",
        loc_sprite_name: "spr_loc_earth_granite",
        controlling_faction: "faction_c",
        starting_faction: "faction_c",
        is_unlocked: true,
        daily_credits: 42000,
        material_type: "titanium",
        daily_materials: 18,
        defense_rating: 88,
        garrison_unit: "Syndicate Black-Water Enforcers",
        connected_ids: ["earth_granite_redoubt", "earth_sahara_array", "earth_nordic_vault"],
        map_x: 290, map_y: 160, global_map_x: 630, global_map_y: 295, is_major_stronghold: true,
        lore_brief: "Heavily fortified coastal artillery emplacements burrowed into limestone cliffs. Railgun batteries control maritime transit between the Atlantic and Mediterranean, taxing commercial freight.",
        strategic_value: "Commands vital maritime trade chokepoints and undersea communication lines."
    };

    _db.earth_outback_proving = {
        id: "earth_outback_proving",
        name: "Woomera Proving Grounds",
        region: "EARTH",
        subregion: "Central Australian Desert Weapons Basin",
        loc_sprite_name: "spr_loc_earth_granite",
        controlling_faction: "faction_c",
        starting_faction: "faction_c",
        is_unlocked: true,
        daily_credits: 39000,
        material_type: "tungsten",
        daily_materials: 20,
        defense_rating: 79,
        garrison_unit: "Outback Arms Test Cohort",
        connected_ids: ["earth_shanghai_arcology", "earth_antarctic_facility", "earth_andes_battery"],
        map_x: 520, map_y: 270, global_map_x: 1180, global_map_y: 520, is_major_stronghold: true,
        lore_brief: "Vast red desert flats scorched by decades of kinetic ordnance testing and experimental orbital drops. Autonomous target drones and salvaged enemy mechs are destroyed here in live-fire trials.",
        strategic_value: "Primary ordnance development and live-fire proving facility."
    };

    _db.earth_shanghai_arcology = {
        id: "earth_shanghai_arcology",
        name: "Neo-Shanghai Arcology Spire",
        region: "EARTH",
        subregion: "Yangtze Delta Industrial Megalopolis",
        loc_sprite_name: "spr_loc_earth_granite",
        controlling_faction: "faction_d",
        starting_faction: "faction_d",
        is_unlocked: true,
        daily_credits: 54000,
        material_type: "composite",
        daily_materials: 25,
        defense_rating: 85,
        garrison_unit: "Kurogane Cybernetic Security Force",
        connected_ids: ["earth_cascadia_driver", "earth_outback_proving", "earth_ural_arsenal"],
        map_x: 480, map_y: 170, global_map_x: 1060, global_map_y: 310, is_major_stronghold: true,
        lore_brief: "Soaring carbon-lattice towers dominating the coastal skyline. Kurogane automated micro-fabrication lines produce millions of avionics chipsets, optical sensors, and targeting processors per day.",
        strategic_value: "Industrial electronic manufacturing center and high-tech corporate asset."
    };

    _db.earth_nordic_vault = {
        id: "earth_nordic_vault",
        name: "Skagerrak Sub-Sea Hangar",
        region: "EARTH",
        subregion: "North Sea Submersible Cavern",
        loc_sprite_name: "spr_loc_earth_granite",
        controlling_faction: "faction_d",
        starting_faction: "faction_d",
        is_unlocked: true,
        daily_credits: 41000,
        material_type: "titanium",
        daily_materials: 19,
        defense_rating: 83,
        garrison_unit: "Kurogane Amphibious Mech Unit",
        connected_ids: ["earth_cascadia_driver", "earth_gibraltar_redoubt", "earth_ural_arsenal"],
        map_x: 320, map_y: 110, global_map_x: 680, global_map_y: 175, is_major_stronghold: true,
        lore_brief: "Subterranean naval drydocks hidden underneath fjord waters. Specialized amphibious combat mechs and stealth transport submarines stage missions under the cover of arctic storms.",
        strategic_value: "Covert amphibious staging ground and submarine repair slipway."
    };

    _db.earth_ural_arsenal = {
        id: "earth_ural_arsenal",
        name: "Ural Mountain Munitions Vault",
        region: "EARTH",
        subregion: "Continental Bedrock Foundry Complex",
        loc_sprite_name: "spr_loc_earth_granite",
        controlling_faction: "faction_e",
        starting_faction: "faction_e",
        is_unlocked: true,
        daily_credits: 47000,
        material_type: "tungsten",
        daily_materials: 23,
        defense_rating: 90,
        garrison_unit: "Sidereal Heavy Grenadier Corps",
        connected_ids: ["earth_sahara_array", "earth_nordic_vault", "earth_shanghai_arcology"],
        map_x: 410, map_y: 130, global_map_x: 870, global_map_y: 210, is_major_stronghold: true,
        lore_brief: "Deep mountain caverns holding millions of artillery shells, solid-propellant rockets, and tungsten penetrators. Geothermal drills power continuous casting foundries that never sleep.",
        strategic_value: "Continental munitions manufacturing forge and strategic alloy store."
    };

    _db.earth_antarctic_facility = {
        id: "earth_antarctic_facility",
        name: "Vostok Sub-Glacial Vault",
        region: "EARTH",
        subregion: "South Pole Deep Ice Research Lab",
        loc_sprite_name: "spr_loc_earth_granite",
        controlling_faction: "faction_e",
        starting_faction: "faction_e",
        is_unlocked: true,
        daily_credits: 43000,
        material_type: "syn_flux",
        daily_materials: 20,
        defense_rating: 87,
        garrison_unit: "Sidereal Polar Cryo-Guard",
        connected_ids: ["earth_granite_redoubt", "earth_outback_proving", "earth_andes_battery"],
        map_x: 340, map_y: 310, global_map_x: 750, global_map_y: 680, is_major_stronghold: true,
        lore_brief: "Buried beneath four kilometers of Antarctic ice sheet, isolated from all electromagnetic contamination. Scientists here conduct black-budget research into prototype alien catalyst materials.",
        strategic_value: "Houses classified catalyst particle research and dark-budget prototypes."
    };

    // =========================================================================
    // 3. MARS & ASTEROID THEATER (8 Martian Volcanic & Trench Redoubts)
    // Starting Distribution: 8 Faction F (Red Mars Vanguard / Tharsis Consensus)
    // Locked until Cycle 10 or override awakening!
    // =========================================================================
    _db.mars_olympus_caldera = {
        id: "mars_olympus_caldera",
        name: "Mount Olympus Zenith Redoubt",
        region: "MARS",
        subregion: "Summit Caldera Geothermal Vault",
        loc_sprite_name: "spr_loc_mars_redoubt",
        controlling_faction: "faction_f",
        starting_faction: "faction_f",
        is_unlocked: false,
        daily_credits: 52000,
        material_type: "titanium",
        daily_materials: 26,
        defense_rating: 94,
        garrison_unit: "Tharsis Red Guard Shock Legion",
        connected_ids: ["mars_marineris_rift", "mars_tharsis_foundry", "mars_phobos_citadel"],
        map_x: 290, map_y: 130, is_major_stronghold: true,
        lore_brief: "The crown fortress of Mars, situated twenty-two kilometers above the datum inside the vast volcanic crater. Geothermal conduits tap magma chambers to power heavy armor plate foundries.",
        strategic_value: "Supreme political citadel and high-altitude fortress of Red Mars."
    };

    _db.mars_marineris_rift = {
        id: "mars_marineris_rift",
        name: "Valles Marineris Chasm Base",
        region: "MARS",
        subregion: "Canyon Wall Subterranean Complex",
        loc_sprite_name: "spr_loc_mars_redoubt",
        controlling_faction: "faction_f",
        starting_faction: "faction_f",
        is_unlocked: false,
        daily_credits: 46000,
        material_type: "tungsten",
        daily_materials: 24,
        defense_rating: 89,
        garrison_unit: "Chasm Skirmisher Guerrillas",
        connected_ids: ["mars_olympus_caldera", "mars_tharsis_foundry", "mars_hellas_basin"],
        map_x: 340, map_y: 220,
        lore_brief: "Carved into vertical sandstone and basalt cliffs seven kilometers deep. Giant cantilevered cranes hoist mobile suits and mining machinery into subterranean caverns safe from surface dust storms.",
        strategic_value: "Sheltered underground industrial depot and guerrilla staging base."
    };

    _db.mars_tharsis_foundry = {
        id: "mars_tharsis_foundry",
        name: "Tharsis Volcanic Crucible",
        region: "MARS",
        subregion: "Volcanic Bulge Smelting Complex",
        loc_sprite_name: "spr_loc_mars_redoubt",
        controlling_faction: "faction_f",
        starting_faction: "faction_f",
        is_unlocked: false,
        daily_credits: 44000,
        material_type: "composite",
        daily_materials: 22,
        defense_rating: 86,
        garrison_unit: "Tharsis Magma Foundry Militia",
        connected_ids: ["mars_olympus_caldera", "mars_marineris_rift", "mars_elysium_spire"],
        map_x: 220, map_y: 210,
        lore_brief: "Tapping direct hydrothermal vents and high-pressure mineral geysers, this sprawling refinery forges reinforced tungsten-carbide alloys for Martian revolutionary armor.",
        strategic_value: "Major metallurgical refinery and heavy ordnance foundry."
    };

    _db.mars_elysium_spire = {
        id: "mars_elysium_spire",
        name: "Elysium Space Tether",
        region: "MARS",
        subregion: "Planitia Space Elevator Terminal",
        loc_sprite_name: "spr_loc_mars_redoubt",
        controlling_faction: "faction_f",
        starting_faction: "faction_f",
        is_unlocked: false,
        daily_credits: 48000,
        material_type: "syn_flux",
        daily_materials: 20,
        defense_rating: 85,
        garrison_unit: "Tether Defense Artillery Unit",
        connected_ids: ["mars_tharsis_foundry", "mars_hellas_basin", "mars_ceres_gateway"],
        map_x: 430, map_y: 160,
        lore_brief: "A carbon-nanotube space tether hoisting heavy containers of Martian iron directly into synchronous orbit, bypassing atmospheric escape fuel costs.",
        strategic_value: "Surface-to-orbit logistics terminal connecting Mars to outer belts."
    };

    _db.mars_hellas_basin = {
        id: "mars_hellas_basin",
        name: "Hellas Impact Sink",
        region: "MARS",
        subregion: "Low-Elevation Hydroponic Dome City",
        loc_sprite_name: "spr_loc_mars_redoubt",
        controlling_faction: "faction_f",
        starting_faction: "faction_f",
        is_unlocked: false,
        daily_credits: 41000,
        material_type: "biomass",
        daily_materials: 19,
        defense_rating: 82,
        garrison_unit: "Hellas Hydroponic Defense Force",
        connected_ids: ["mars_marineris_rift", "mars_elysium_spire", "mars_deimos_sensor"],
        map_x: 390, map_y: 280,
        lore_brief: "At seven kilometers below datum, atmospheric pressure is high enough that pressurized dome cities can grow extensive algae crops and support subterranean civilian populations.",
        strategic_value: "Main population sanctuary and agricultural breadbasket on Mars."
    };

    _db.mars_phobos_citadel = {
        id: "mars_phobos_citadel",
        name: "Phobos Orbital Battery",
        region: "MARS",
        subregion: "Inner Moon Kinetic Bombardment Base",
        loc_sprite_name: "spr_loc_space_citadel",
        controlling_faction: "faction_f",
        starting_faction: "faction_f",
        is_unlocked: false,
        daily_credits: 45000,
        material_type: "tungsten",
        daily_materials: 21,
        defense_rating: 90,
        garrison_unit: "Phobos Heavy Orbital Battery",
        connected_ids: ["mars_olympus_caldera", "mars_deimos_sensor", "mars_ceres_gateway"],
        map_x: 480, map_y: 80,
        lore_brief: "The inner moon has been hollowed into an immense orbital fortress. Heavy kinetic mass drivers on its surface can rain hypersonic projectiles down upon any surface landing zone.",
        strategic_value: "Kinetic orbital bombardment platform dominating low Martian orbit."
    };

    _db.mars_deimos_sensor = {
        id: "mars_deimos_sensor",
        name: "Deimos Stealth Listening Post",
        region: "MARS",
        subregion: "Outer Moon SIGINT Array",
        loc_sprite_name: "spr_loc_space_citadel",
        controlling_faction: "faction_f",
        starting_faction: "faction_f",
        is_unlocked: false,
        daily_credits: 38000,
        material_type: "syn_flux",
        daily_materials: 16,
        defense_rating: 81,
        garrison_unit: "Deimos Electronic Warfare Unit",
        connected_ids: ["mars_phobos_citadel", "mars_hellas_basin", "mars_ceres_gateway"],
        map_x: 530, map_y: 140,
        lore_brief: "Covered in radar-absorbent materials, this small moon silently intercepts communications across the entire inner solar system, feeding strategic data to Tharsis commanders.",
        strategic_value: "Solar-wide electronic intelligence and stealth surveillance node."
    };

    _db.mars_ceres_gateway = {
        id: "mars_ceres_gateway",
        name: "Ceres Belt Terminal",
        region: "MARS",
        subregion: "Main Asteroid Belt Trade Port",
        loc_sprite_name: "spr_loc_space_citadel",
        controlling_faction: "faction_f",
        starting_faction: "faction_f",
        is_unlocked: false,
        daily_credits: 50000,
        material_type: "titanium",
        daily_materials: 25,
        defense_rating: 88,
        garrison_unit: "Belt Vanguard Patrol Wing",
        connected_ids: ["mars_phobos_citadel", "mars_deimos_sensor", "mars_elysium_spire"],
        map_x: 580, map_y: 200,
        lore_brief: "A hollowed dwarf planet with an icy mantle and spinning habitat cylinders inside. It anchors hundreds of autonomous mining platforms extracting rare platinum-group metals.",
        strategic_value: "Dwarf planet trade hub linking Martian territory with outer asteroid wealth."
    };

    return _db;
}

// -----------------------------------------------------------------------------
// Helper: Get territory struct safely
// -----------------------------------------------------------------------------
function scr_territory_get(_id) {
    var _fm = instance_exists(obj_FactionManager) ? instance_find(obj_FactionManager, 0) : noone;
    if (_fm == noone || !variable_instance_exists(_fm, "territory_database")) return undefined;
    if (!variable_struct_exists(_fm.territory_database, _id)) return undefined;
    return variable_struct_get(_fm.territory_database, _id);
}

// -----------------------------------------------------------------------------
// Helper: Get array of territories by region ("SPACE", "EARTH", "MARS")
// -----------------------------------------------------------------------------
function scr_territory_get_by_region(_region) {
    var _results = [];
    var _fm = instance_exists(obj_FactionManager) ? instance_find(obj_FactionManager, 0) : noone;
    if (_fm == noone) return _results;
    if (!variable_instance_exists(_fm, "territory_database")) return _results;
    
    var _keys = variable_struct_get_names(_fm.territory_database);
    for (var i = 0; i < array_length(_keys); i++) {
        var _t = variable_struct_get(_fm.territory_database, _keys[i]);
        if (_t.region == _region) {
            array_push(_results, _t);
        }
    }
    return _results;
}

// -----------------------------------------------------------------------------
// Helper: Check if territory is on the frontline
// -----------------------------------------------------------------------------
function scr_territory_is_frontline(_id) {
    var _t = scr_territory_get(_id);
    if (is_undefined(_t)) return false;
    if (!_t.is_unlocked) return false;

    var _conn = _t.connected_ids;
    for (var c = 0; c < array_length(_conn); c++) {
        var _neighbor = scr_territory_get(_conn[c]);
        if (!is_undefined(_neighbor) && _neighbor.is_unlocked) {
            if (_neighbor.controlling_faction != _t.controlling_faction) {
                return true;
            }
        }
    }
    return false;
}

// -----------------------------------------------------------------------------
// Re-calculate Sol territory control percentages accurately
// -----------------------------------------------------------------------------
function scr_territory_recalculate_control_percentages() {
    var _fm = instance_exists(obj_FactionManager) ? instance_find(obj_FactionManager, 0) : noone;
    if (_fm == noone && object_index == obj_FactionManager) _fm = id;
    if (_fm == noone || !variable_instance_exists(_fm, "territory_database")) return;

    var _keys = variable_struct_get_names(_fm.territory_database);
    var _counts = {
        faction_a: 0,
        faction_b: 0,
        faction_c: 0,
        faction_d: 0,
        faction_e: 0,
        faction_f: 0,
        pmc: 0,
        total_unlocked: 0
    };

    for (var i = 0; i < array_length(_keys); i++) {
        var _t = variable_struct_get(_fm.territory_database, _keys[i]);
        if (_t.is_unlocked) {
            _counts.total_unlocked += 1;
            var _owner = _t.controlling_faction;
            if (variable_struct_exists(_counts, _owner)) {
                variable_struct_set(_counts, _owner, variable_struct_get(_counts, _owner) + 1);
            }
        }
    }

    if (_counts.total_unlocked <= 0) return;

    var _tot = _counts.total_unlocked;
    _fm.territory_control.terran_pct    = round((_counts.faction_a / _tot) * 100);
    _fm.territory_control.colony_pct    = round((_counts.faction_b / _tot) * 100);
    _fm.territory_control.syndicate_pct = round((_counts.faction_c / _tot) * 100);
    _fm.territory_control.zaibatsu_pct  = round((_counts.faction_d / _tot) * 100);
    _fm.territory_control.astran_pct    = round((_counts.faction_e / _tot) * 100);
    _fm.territory_control.martian_pct   = round((_counts.faction_f / _tot) * 100);
    _fm.territory_control.pmc_pct       = round((_counts.pmc / _tot) * 100);

    // Minor normalization so sum equals 100%
    var _sum = _fm.territory_control.terran_pct + _fm.territory_control.colony_pct + _fm.territory_control.syndicate_pct +
               _fm.territory_control.zaibatsu_pct + _fm.territory_control.astran_pct + _fm.territory_control.martian_pct +
               _fm.territory_control.pmc_pct;
    var _diff = 100 - _sum;
    if (_diff != 0) {
        _fm.territory_control.terran_pct = max(0, _fm.territory_control.terran_pct + _diff);
    }
}

// -----------------------------------------------------------------------------
// Unlock the Mars Sphere (Called when Tharsis Consensus awakens)
// -----------------------------------------------------------------------------
function scr_territory_unlock_mars() {
    var _fm = instance_exists(obj_FactionManager) ? instance_find(obj_FactionManager, 0) : noone;
    if (_fm == noone) return;
    if (!variable_instance_exists(_fm, "territory_database")) return;

    var _mars_territories = scr_territory_get_by_region("MARS");
    for (var m = 0; m < array_length(_mars_territories); m++) {
        var _mt = _mars_territories[m];
        _mt.is_unlocked = true;
        _mt.controlling_faction = "faction_f";
    }

    _fm.mars_unlocked = true;
    if (variable_struct_exists(_fm.factions, "faction_f")) {
        _fm.factions.faction_f.is_dormant = false;
    }

    scr_territory_recalculate_control_percentages();

    if (instance_exists(obj_HQTerminal)) {
        obj_HQTerminal.show_toast("MARS SPHERE UNLOCKED! THARSIS REVOLUTIONARY FRONT HAS AWOKEN!");
    }
}

// -----------------------------------------------------------------------------
// Process Daily Logistics for PMC Controlled Territories
// -----------------------------------------------------------------------------
function scr_territory_process_daily_logistics() {
    var _fm = instance_exists(obj_FactionManager) ? instance_find(obj_FactionManager, 0) : noone;
    var _gm = instance_exists(obj_GameManager) ? instance_find(obj_GameManager, 0) : noone;
    if (_fm == noone || _gm == noone) return;
    if (!variable_instance_exists(_fm, "territory_database")) return;

    var _total_creds = 0;
    var _total_mats = 0;
    var _keys = variable_struct_get_names(_fm.territory_database);

    for (var i = 0; i < array_length(_keys); i++) {
        var _t = variable_struct_get(_fm.territory_database, _keys[i]);
        if (_t.controlling_faction == "pmc" && _t.is_unlocked) {
            _total_creds += _t.daily_credits;
            _total_mats += _t.daily_materials;

            if (_t.material_type == "titanium" && variable_instance_exists(_gm, "titanium_reserve")) {
                _gm.titanium_reserve += _t.daily_materials;
            } else if (_t.material_type == "tungsten" && variable_instance_exists(_gm, "tungsten_reserve")) {
                _gm.tungsten_reserve += _t.daily_materials;
            } else if (_t.material_type == "composite" && variable_instance_exists(_gm, "composite_reserve")) {
                _gm.composite_reserve += _t.daily_materials;
            } else if (variable_instance_exists(_gm, "flux_reserve")) {
                _gm.flux_reserve += _t.daily_materials;
            }
        }
    }

    if (_total_creds > 0 && variable_instance_exists(_gm, "funds")) {
        _gm.funds += _total_creds;
    }
}

// -----------------------------------------------------------------------------
// Fortify a PMC sector (+10 Defense, Costs $25,000)
// -----------------------------------------------------------------------------
function scr_territory_fortify(_id) {
    var _t = scr_territory_get(_id);
    var _gm = instance_exists(obj_GameManager) ? instance_find(obj_GameManager, 0) : noone;
    if (is_undefined(_t) || _gm == noone) return;

    if (_t.controlling_faction != "pmc") {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("CANNOT FORTIFY: SECTOR NOT OWNED BY PMC!");
        return;
    }

    var _cost = 25000;
    if (_gm.funds < _cost) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("INSUFFICIENT FUNDS TO FORTIFY ($25,000 REQ)");
        return;
    }

    if (_t.defense_rating >= 100) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("SECTOR DEFENSES ALREADY AT MAXIMUM CAPACITY (100)");
        return;
    }

    _gm.funds -= _cost;
    _t.defense_rating = min(100, _t.defense_rating + 10);
    scr_audio_play_ui("confirm");
    if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("FORTIFICATION UPGRADED: " + _t.name + " (DEF: " + string(_t.defense_rating) + ")");
}

// -----------------------------------------------------------------------------
// Launch PMC Assault Expedition on Enemy Sector
// -----------------------------------------------------------------------------
function scr_territory_launch_pmc_assault(_target_id, _squad_power, _pmc_investment) {
    var _target = scr_territory_get(_target_id);
    var _gm = instance_exists(obj_GameManager) ? instance_find(obj_GameManager, 0) : noone;
    var _fm = instance_exists(obj_FactionManager) ? instance_find(obj_FactionManager, 0) : noone;
    if (is_undefined(_target) || _gm == noone) return;

    if (_target.controlling_faction == "pmc") {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("ALREADY UNDER PMC CONTROL!");
        return;
    }

    var _cost = 35000;
    if (_gm.funds < _cost) {
        if (instance_exists(obj_HQTerminal)) obj_HQTerminal.show_toast("EXPEDITION LAUNCH REQUIRES $35,000 PROVISIONS");
        return;
    }

    _gm.funds -= _cost;
    scr_audio_play_ui("confirm");

    // Success probability scales inversely with defense rating
    var _roll = irandom(100);
    var _difficulty = _target.defense_rating;
    
    // PMC veteran attack roll (40-95 based on random + investment)
    if (_roll >= (_difficulty - 20)) {
        // Victory! Sector captured by PMC
        var _old_owner = _target.controlling_faction;
        _target.controlling_faction = "pmc";
        _target.defense_rating = max(35, _target.defense_rating - 25);
        scr_territory_recalculate_control_percentages();

        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("★ VICTORY! " + string_upper(_target.name) + " CAPTURED BY IRON RIDGE PMC! ★");
        }
    } else {
        // Repelled: Defenses reduced by 5
        _target.defense_rating = max(20, _target.defense_rating - 5);
        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("ASSAULT REPELLED AT " + _target.name + "! ENEMY DEFENSES WEAKENED (-5 DEF)");
        }
    }
}

// -----------------------------------------------------------------------------
// Resolve AI Faction Inter-Territory Skirmishes
// -----------------------------------------------------------------------------
function scr_territory_resolve_ai_skirmishes() {
    var _fm = instance_exists(obj_FactionManager) ? instance_find(obj_FactionManager, 0) : noone;
    if (_fm == noone || !variable_instance_exists(_fm, "territory_database")) return;

    var _keys = variable_struct_get_names(_fm.territory_database);
    var _unlocked_keys = [];
    for (var i = 0; i < array_length(_keys); i++) {
        var _t = variable_struct_get(_fm.territory_database, _keys[i]);
        if (_t.is_unlocked && _t.controlling_faction != "pmc") {
            array_push(_unlocked_keys, _keys[i]);
        }
    }

    if (array_length(_unlocked_keys) < 2) return;

    var _atk_key = _unlocked_keys[irandom(array_length(_unlocked_keys) - 1)];
    var _atk_t = variable_struct_get(_fm.territory_database, _atk_key);

    var _target_candidates = [];
    for (var c = 0; c < array_length(_atk_t.connected_ids); c++) {
        var _cand = scr_territory_get(_atk_t.connected_ids[c]);
        if (!is_undefined(_cand) && _cand.is_unlocked && _cand.controlling_faction != _atk_t.controlling_faction && _cand.controlling_faction != "pmc") {
            array_push(_target_candidates, _cand);
        }
    }

    if (array_length(_target_candidates) == 0) return;

    var _def_t = _target_candidates[irandom(array_length(_target_candidates) - 1)];

    var _roll = irandom(100);
    if (_roll > _def_t.defense_rating) {
        var _prev_owner = _def_t.controlling_faction;
        _def_t.controlling_faction = _atk_t.controlling_faction;
        _def_t.defense_rating = max(30, _def_t.defense_rating - 15);
        scr_territory_recalculate_control_percentages();

        if (instance_exists(obj_HQTerminal)) {
            obj_HQTerminal.show_toast("WAR UPDATE: " + _def_t.name + " CONQUERED BY " + string_upper(_atk_t.controlling_faction));
        }
    } else {
        _def_t.defense_rating = max(20, _def_t.defense_rating - 4);
    }
}


// =========================================================================
// SHIN GIHREN'S GREED TACTICAL COUNTER SYSTEM (Doc 39 / Art Suite)
// =========================================================================

/// @function scr_territory_get_garrison_spec(_t)
/// @description Returns unit sprite, stack count, and tactical designation for a territory
function scr_territory_get_garrison_spec(_t) {
    var _spec = {
        unit_sprite_name: "spr_mini_ms_ironclad",
        stack_count: 4,
        unit_label: "Heavy Mobile Suit"
    };
    if (is_undefined(_t)) return _spec;
    
    var _fac = _t.controlling_faction;
    var _def = variable_struct_exists(_t, "defense_rating") ? _t.defense_rating : 75;
    
    if (_fac == "faction_a") {
        if (_t.region == "EARTH") {
            _spec.unit_sprite_name = "spr_mini_veh_heavy_tank";
            _spec.stack_count = max(4, floor(_def / 11));
            _spec.unit_label = "MB-88 Goliath Tanks";
        } else {
            _spec.unit_sprite_name = "spr_mini_ms_ironclad";
            _spec.stack_count = max(3, floor(_def / 14));
            _spec.unit_label = "GHA-07 Ironclad MS";
        }
    } else if (_fac == "faction_b") {
        if (_t.region == "EARTH") {
            _spec.unit_sprite_name = "spr_mini_veh_gunship";
            _spec.stack_count = max(3, floor(_def / 13));
            _spec.unit_label = "SV-13 Wyvern Gunships";
        } else {
            _spec.unit_sprite_name = "spr_mini_ms_aerostriker";
            _spec.stack_count = max(3, floor(_def / 14));
            _spec.unit_label = "Aero-Striker Wings";
        }
    } else if (_fac == "faction_c") {
        if (_t.region == "EARTH") {
            _spec.unit_sprite_name = "spr_mini_veh_technical";
            _spec.stack_count = max(4, floor(_def / 10));
            _spec.unit_label = "ATV-4 Recon Technicals";
        } else {
            _spec.unit_sprite_name = "spr_mini_ms_artillery";
            _spec.stack_count = max(2, floor(_def / 16));
            _spec.unit_label = "Mammoth-Tread Siege MS";
        }
    } else if (_fac == "faction_d") {
        _spec.unit_sprite_name = "spr_mini_ms_hoversniper";
        _spec.stack_count = max(3, floor(_def / 15));
        _spec.unit_label = "Specter Hover Railguns";
    } else if (_fac == "faction_e") {
        if (_t.region == "EARTH") {
            _spec.unit_sprite_name = "spr_mini_inf_exo_squad";
            _spec.stack_count = max(4, floor(_def / 10));
            _spec.unit_label = "Exo-Shock Troopers";
        } else {
            _spec.unit_sprite_name = "spr_mini_veh_dropship";
            _spec.stack_count = max(2, floor(_def / 18));
            _spec.unit_label = "Skyhook Fleet Escorts";
        }
    } else if (_fac == "faction_f") {
        _spec.unit_sprite_name = "spr_mini_ms_commander";
        _spec.stack_count = max(3, floor(_def / 12));
        _spec.unit_label = "Autonomous Hegemon MS";
    } else if (_fac == "pmc") {
        _spec.unit_sprite_name = "spr_mini_ms_grunt";
        _spec.stack_count = max(4, floor(_def / 12));
        _spec.unit_label = "Iron Ridge Custom Lance";
    }
    
    return _spec;
}

/// @function scr_draw_tactical_counter(_cx, _cy, _faction_id, _unit_spr_name, _stack_count, _is_selected, _is_hover, _scale)
/// @description Draws a Shin Gihren's Greed style tactical unit counter with hex plinth, unit sprite, and stack count
function scr_draw_tactical_counter(_cx, _cy, _faction_id, _unit_spr_name, _stack_count, _is_selected, _is_hover, _scale) {
    if (is_undefined(_scale)) _scale = 1.0;
    
    // 1. Determine Hex Base Plinth
    var _base_spr = spr_hex_base_pmc;
    if (_faction_id == "faction_a") _base_spr = spr_hex_base_terran;
    else if (_faction_id == "faction_b") _base_spr = spr_hex_base_colony;
    else if (_faction_id == "faction_c") _base_spr = spr_hex_base_syndicate;
    else if (_faction_id == "faction_d") _base_spr = spr_hex_base_zaibatsu;
    else if (_faction_id == "faction_e") _base_spr = spr_hex_base_sidereal;
    else if (_faction_id == "faction_f") _base_spr = spr_hex_base_mars;
    else if (_faction_id == "pmc") _base_spr = spr_hex_base_pmc;
    
    // 2. Base Dimensions
    var _bw = floor(46 * _scale);
    var _bh = floor(34 * _scale);
    
    // Hover Glow Ring
    if (_is_hover) {
        draw_set_color(c_white);
        draw_set_alpha(0.35);
        draw_ellipse(_cx - 24 * _scale, _cy - 10 * _scale, _cx + 24 * _scale, _cy + 14 * _scale, false);
        draw_set_alpha(1.0);
    }
    
    // Draw Base Plinth
    if (sprite_exists(_base_spr)) {
        draw_sprite_stretched(_base_spr, 0, _cx - _bw/2, _cy - _bh/2 + floor(4 * _scale), _bw, _bh);
    }
    
    // 3. Unit Miniature Sprite
    var _u_spr = asset_get_index(_unit_spr_name);
    if (_u_spr == -1 || !sprite_exists(_u_spr)) {
        _u_spr = spr_mini_ms_ironclad;
    }
    
    var _uw = floor(44 * _scale);
    var _uh = floor(44 * _scale);
    if (sprite_exists(_u_spr)) {
        draw_sprite_stretched(_u_spr, 0, _cx - _uw/2, _cy - _uh + floor(8 * _scale), _uw, _uh);
    }
    
    // 4. Digital Stack Numeral Badge
    var _badge_w = floor(14 * _scale);
    var _badge_h = floor(16 * _scale);
    var _badge_x = _cx + floor(8 * _scale);
    var _badge_y = _cy + floor(2 * _scale);
    
    draw_set_color(make_color_rgb(10, 16, 26));
    draw_rectangle(_badge_x, _badge_y, _badge_x + _badge_w, _badge_y + _badge_h, false);
    draw_set_color(make_color_rgb(0, 240, 255));
    draw_rectangle(_badge_x, _badge_y, _badge_x + _badge_w, _badge_y + _badge_h, true);
    
    draw_set_color(make_color_rgb(0, 255, 230));
    draw_text(_badge_x + 3, _badge_y + 1, string(_stack_count));
    
    // 5. Tactical Reticle Brackets ( )
    if (_is_selected) {
        if (sprite_exists(spr_tactical_bracket)) {
            var _brw = floor(56 * _scale);
            var _brh = floor(42 * _scale);
            draw_sprite_stretched(spr_tactical_bracket, 0, _cx - _brw/2, _cy - _brh/2 - floor(4 * _scale), _brw, _brh);
        } else {
            draw_set_color(make_color_rgb(0, 240, 255));
            draw_circle(_cx, _cy, 24 * _scale, true);
        }
    }
}

/// @function scr_draw_hex_cell(_x, _y, _r, _filled)
/// @description Draws a tactical hex cell or influence polygon in Shin Gihren's Greed style
function scr_draw_hex_cell(_x, _y, _r, _filled) {
    if (is_undefined(_filled)) _filled = true;
    var _p0_x = _x + _r; var _p0_y = _y;
    var _p1_x = _x + _r * 0.5; var _p1_y = _y + _r * 0.866;
    var _p2_x = _x - _r * 0.5; var _p2_y = _y + _r * 0.866;
    var _p3_x = _x - _r; var _p3_y = _y;
    var _p4_x = _x - _r * 0.5; var _p4_y = _y - _r * 0.866;
    var _p5_x = _x + _r * 0.5; var _p5_y = _y - _r * 0.866;
    
    if (_filled) {
        draw_triangle(_x, _y, _p0_x, _p0_y, _p1_x, _p1_y, false);
        draw_triangle(_x, _y, _p1_x, _p1_y, _p2_x, _p2_y, false);
        draw_triangle(_x, _y, _p2_x, _p2_y, _p3_x, _p3_y, false);
        draw_triangle(_x, _y, _p3_x, _p3_y, _p4_x, _p4_y, false);
        draw_triangle(_x, _y, _p4_x, _p4_y, _p5_x, _p5_y, false);
        draw_triangle(_x, _y, _p5_x, _p5_y, _p0_x, _p0_y, false);
    }
    
    draw_line(_p0_x, _p0_y, _p1_x, _p1_y);
    draw_line(_p1_x, _p1_y, _p2_x, _p2_y);
    draw_line(_p2_x, _p2_y, _p3_x, _p3_y);
    draw_line(_p3_x, _p3_y, _p4_x, _p4_y);
    draw_line(_p4_x, _p4_y, _p5_x, _p5_y);
    draw_line(_p5_x, _p5_y, _p0_x, _p0_y);
}

// =========================================================================
// TACTICAL ORDER DISPATCH & TRANSIT LOGISTICS (Shin Gihren's Greed System)
// =========================================================================

/// @function scr_territory_get_adjacent_pmc_base(_target_id)
/// @description Returns an adjacent friendly PMC territory ID if one exists, otherwise empty string
function scr_territory_get_adjacent_pmc_base(_target_id) {
    var _target = scr_territory_get(_target_id);
    if (is_undefined(_target)) return "";
    
    for (var i = 0; i < array_length(_target.connected_ids); i++) {
        var _adj_id = _target.connected_ids[i];
        var _adj = scr_territory_get(_adj_id);
        if (!is_undefined(_adj) && _adj.controlling_faction == "pmc") {
            return _adj_id;
        }
    }
    return "";
}

/// @function scr_territory_issue_order(_origin_id, _target_id, _unit_sprite, _stack_count, _is_combat)
/// @description Dispatches a mobile suit battlegroup or transit chit along a hyperlane vector
function scr_territory_issue_order(_origin_id, _target_id, _unit_sprite, _stack_count, _is_combat) {
    var _orig = scr_territory_get(_origin_id);
    var _tgt = scr_territory_get(_target_id);
    var _gm = instance_exists(obj_GameManager) ? instance_find(obj_GameManager, 0) : noone;
    var _hq = instance_exists(obj_HQTerminal) ? instance_find(obj_HQTerminal, 0) : noone;
    
    if (is_undefined(_orig) || is_undefined(_tgt)) return false;
    
    var _cost = _is_combat ? 15000 : 5000;
    if (_gm != noone && _gm.funds < _cost) {
        if (_hq != noone) {
            _hq.show_toast("INSUFFICIENT FUNDS FOR DISPATCH LOGISTICS (REQ $" + string(_cost) + ")", make_color_rgb(255, 90, 80));
        }
        scr_audio_play_ui("cancel");
        return false;
    }
    
    if (_gm != noone) {
        _gm.funds -= _cost;
    }
    
    // Calculate Screen Map Positions for Transit
    var _rad_x = 16;
    var _rad_y = 98;
    var _ox = _rad_x + 40 + floor(_orig.map_x * 1.34);
    var _oy = _rad_y + 48 + floor(_orig.map_y * 1.48);
    var _tx = _rad_x + 40 + floor(_tgt.map_x * 1.34);
    var _ty = _rad_y + 48 + floor(_tgt.map_y * 1.48);

    if (_orig.region == "EARTH" && variable_struct_exists(_orig, "global_map_x") && variable_struct_exists(_tgt, "global_map_x") && _hq != noone && _hq.earth_view_mode == "GLOBAL") {
        var _rad_w = 954;
        var _rad_h = 596;
        var _gx_scale = (_rad_w - 24) / 1376.0;
        var _gy_scale = (_rad_h - 38) / 768.0;
        _ox = _rad_x + 12 + floor(_orig.global_map_x * _gx_scale);
        _oy = _rad_y + 26 + floor(_orig.global_map_y * _gy_scale);
        _tx = _rad_x + 12 + floor(_tgt.global_map_x * _gx_scale);
        _ty = _rad_y + 26 + floor(_tgt.global_map_y * _gy_scale);
    }
    
    var _transit = {
        id: "transit_" + string(current_time) + "_" + string(irandom(9999)),
        origin_id: _origin_id,
        target_id: _target_id,
        unit_sprite_name: _unit_sprite,
        stack_count: _stack_count,
        progress: 0.0,
        speed: 0.022,
        is_combat: _is_combat,
        origin_x: _ox,
        origin_y: _oy,
        target_x: _tx,
        target_y: _ty
    };
    
    if (_hq != noone) {
        array_push(_hq.active_transits, _transit);
        _hq.crucible_shake = 3.0;
        _hq.show_toast(_is_combat ? (">> ASSAULT SQUADRON DISPATCHED: " + string_upper(_tgt.name) + " >>") : (">> REDEPLOYMENT TRANSIT EN ROUTE >>"), make_color_rgb(0, 240, 255));
    }
    
    scr_audio_play_ui("confirm");
    return true;
}

/// @function scr_territory_resolve_transit_arrival(_tr)
/// @description Resolves when a moving squadron reaches its destination node
function scr_territory_resolve_transit_arrival(_tr) {
    var _t = scr_territory_get(_tr.target_id);
    var _orig = scr_territory_get(_tr.origin_id);
    var _gm = instance_exists(obj_GameManager) ? instance_find(obj_GameManager, 0) : noone;
    var _fm = instance_exists(obj_FactionManager) ? instance_find(obj_FactionManager, 0) : noone;
    var _hq = instance_exists(obj_HQTerminal) ? instance_find(obj_HQTerminal, 0) : noone;
    
    if (is_undefined(_t)) return;
    
    if (!_tr.is_combat) {
        // Friendly redeployment
        _t.defense_rating = min(100, _t.defense_rating + 5);
        if (_hq != noone) {
            _hq.crucible_shake = 2.0;
            _hq.show_toast("✓ REINFORCEMENTS ARRIVED AT " + string_upper(_t.name) + " (+5 DEF)", make_color_rgb(80, 240, 140));
        }
        scr_audio_play_ui("confirm");
    } else {
        // Hostile Assault / Combat Clash!
        if (_hq != noone) {
            _hq.crucible_shake = 9.0;
        }
        
        // Weapon Foley
        scr_audio_play_weapon("cannon");
        
        // Authentic Shin Gihren's Greed Combat Calculation
        var _attack_base = (_tr.stack_count * 16) + irandom_range(20, 45);
        var _defense_base = _t.defense_rating + irandom_range(10, 30);
        var _is_win = (_attack_base >= _defense_base);
        
        var _rounds = [];
        array_push(_rounds, "PHASE 1 (INGRESS): Iron Ridge strike wing engages target outer sensors.");
        array_push(_rounds, "PHASE 2 (FIRE EXCHANGE): Attack rating [" + string(_attack_base) + "] vs Garrison defense [" + string(_defense_base) + "].");
        
        if (_is_win) {
            var _old_owner = _t.controlling_faction;
            _t.controlling_faction = "pmc";
            _t.defense_rating = max(40, _defense_base - 30);
            scr_territory_recalculate_control_percentages();
            
            array_push(_rounds, "PHASE 3 (BREACH): Enemy perimeter collapsed! Fortress citadel captured.");
            
            if (_hq != noone) {
                _hq.combat_modal_active = true;
                _hq.combat_report = {
                    title: "OPERATION SUCCESS // SECTOR SECURED",
                    origin_name: (!is_undefined(_orig) ? _orig.name : "Staging Bastion"),
                    target_name: _t.name,
                    target_faction: _old_owner,
                    player_power: _attack_base,
                    enemy_power: _defense_base,
                    result_text: "Sector liberated and integrated into Iron Ridge PMC sovereign zone.",
                    is_victory: true,
                    rounds: _rounds
                };
                _hq.show_toast("★ VICTORY! " + string_upper(_t.name) + " CAPTURED! ★", make_color_rgb(255, 215, 60));
            }
            scr_audio_play_ui("confirm");
        } else {
            _t.defense_rating = max(15, _t.defense_rating - 8);
            array_push(_rounds, "PHASE 3 (WITHDRAWAL): Heavy counter-fire forced tactical regroup (-8 DEF to enemy).");
            
            if (_hq != noone) {
                _hq.combat_modal_active = true;
                _hq.combat_report = {
                    title: "OPERATION WITHDRAWAL // GARRISON HELD",
                    origin_name: (!is_undefined(_orig) ? _orig.name : "Staging Bastion"),
                    target_name: _t.name,
                    target_faction: _t.controlling_faction,
                    player_power: _attack_base,
                    enemy_power: _defense_base,
                    result_text: "Invasion repelled by entrenched garrison. Enemy defenses degraded by -8 DEF.",
                    is_victory: false,
                    rounds: _rounds
                };
                _hq.show_toast("ASSAULT REPELLED AT " + string_upper(_t.name) + "! (-8 ENEMY DEF)", make_color_rgb(255, 90, 80));
            }
            scr_audio_play_ui("cancel");
        }
    }
}

/// @function scr_territory_get_battle_map_id(_tid)
/// @description Maps each of the 33 Sol strategic territories to an authentic 20x20 isometric battle arena map ID
function scr_territory_get_battle_map_id(_tid) {
    switch (_tid) {
        // --- 1. Space & Colonies Sphere (15 Strategic Sectors) ---
        case "space_kepler_haven":      return 17; // Lagrange-5 Logistics Hub
        case "space_aethelgard_prime":  return 12; // Colony Cylinder Shell
        case "space_halcyon_ring":      return 12; // Colony Cylinder Shell
        case "space_charybdis_gate":    return 15; // Space Elevator Ring Terminal
        case "space_tartarus_citadel":  return 11; // Asteroid Fortress
        case "space_archon_spire":      return 15; // Space Elevator Ring Terminal
        case "space_vesta_anchorage":   return 18; // Deep Void Comms Relay
        case "space_pelican_refinery":  return 14; // Derelict Fleet Graveyard
        case "space_nadir_scrapyard":   return 14; // Derelict Fleet Graveyard
        case "space_valkyrie_array":    return 10; // Helios-7 Orbital Array
        case "space_selene_zenith":     return 13; // Lunar Regolith Crater
        case "space_daedalus_foundry":  return 13; // Lunar Regolith Crater
        case "space_borealis_port":     return 16; // Comet Core Ice Quarry
        case "space_ironspire_bastion": return 11; // Asteroid Fortress
        case "space_hyperion_dock":     return 14; // Derelict Fleet Graveyard
        
        // --- 2. Earth Continental Sphere (10 Citadels) ---
        case "earth_granite_redoubt":   return 4;  // Verdant Jungle Delta (Amazonian Bedrock)
        case "earth_cascadia_driver":   return 8;  // Abandoned Spaceport Terminal (Cascadia)
        case "earth_sahara_array":      return 5;  // Sahara Dune Refinery (Al-Kufra)
        case "earth_andes_battery":     return 2;  // Volcanic Caldera Ridge (Chimborazo)
        case "earth_gibraltar_redoubt": return 1;  // Neo-Verona Coastal Ruins (Gibraltar)
        case "earth_outback_proving":   return 9;  // Irradiated Salt Flats (Woomera)
        case "earth_shanghai_arcology": return 6;  // Mega-City Sector 9 Grid (Neo-Shanghai)
        case "earth_nordic_vault":      return 1;  // Coastal Ruins / Subsea Fjords
        case "earth_ural_arsenal":      return 7;  // Subterranean Magma Vault (Urals)
        case "earth_antarctic_facility": return 3; // Glacial Crevasse Pass (Vostok)
        
        // --- 3. Mars & Asteroids Sphere (8 Redoubts) ---
        case "mars_olympus_caldera":    return 2;  // Volcanic Caldera Ridge (Olympus Mons)
        case "mars_valles_marineris":   return 9;  // Irradiated Salt Flats / Grand Canyon
        case "mars_hellas_basin":       return 0;  // Sector 4 Mining Outpost (Hellas Planitia)
        case "mars_tharsis_foundry":    return 7;  // Subterranean Magma Vault (Tharsis Smelters)
        case "mars_cydonia_spire":      return 8;  // Abandoned Spaceport Terminal (Cydonia)
        case "mars_elysium_depot":      return 0;  // Mining Outpost (Elysium Planitia)
        case "mars_phobos_battery":     return 11; // Asteroid Fortress (Phobos Orbital Gun)
        case "mars_deimos_relay":       return 18; // Deep Void Comms Relay (Deimos Sensor Apex)
        
        default: return 0;
    }
}

// =========================================================================
// MAJOR STRONGHOLD SEPARATE MAPS ENGINE (Gihren's Greed Tokubetsu Kyoten)
// =========================================================================

/// @function scr_stronghold_get_layout(_stronghold_id)
/// @description Returns the dedicated regional map layout and local tactical defense sub-nodes
function scr_stronghold_get_layout(_stronghold_id) {
    var _layout = {
        stronghold_id: _stronghold_id,
        stronghold_name: "Major Stronghold",
        region: "EARTH",
        map_sprite_name: "spr_map_earth_theater",
        minimap_box: { x: 48, y: 54, w: 40, h: 38 },
        subnodes: []
    };
    
    switch (_stronghold_id) {
        case "earth_granite_redoubt":
            _layout.stronghold_name = "Granite Deep Command (South America Stronghold)";
            _layout.region = "EARTH";
            _layout.map_sprite_name = "spr_map_earth_theater";
            _layout.minimap_box = { x: 48, y: 54, w: 40, h: 38 };
            _layout.subnodes = [
                { id: "granite_core", name: "Subterranean Command Redoubt", desc: "Excavated three thousand meters beneath ancient granite. Central HQ and reactor core.", sub_type: "CORE_BUNKER", map_x: 390, map_y: 280, controlling_faction: "faction_a", defense_rating: 95, unit_sprite_name: "spr_mini_ms_commander", stack_count: 4, unit_label: "Command Division", connected_ids: ["granite_north_gate", "granite_andes_battery", "granite_missile_silos"], is_core: true },
                { id: "granite_north_gate", name: "Amazon River Delta Flank Sentry", desc: "River crossing bridgehead and armored checkpoint interdicting river gunboats.", sub_type: "RIVER_GATE", map_x: 320, map_y: 180, controlling_faction: "faction_a", defense_rating: 75, unit_sprite_name: "spr_mini_veh_heavy_tank", stack_count: 6, unit_label: "Amazon Armor Cohort", connected_ids: ["granite_core", "granite_caribbean_dock"], is_core: false },
                { id: "granite_andes_battery", name: "Chimborazo Andean Rail Redoubt", desc: "High-altitude kinetic gun battery perched along the equatorial mountain spine.", sub_type: "MOUNTAIN_BATTERY", map_x: 210, map_y: 220, controlling_faction: "faction_b", defense_rating: 82, unit_sprite_name: "spr_mini_ms_artillery", stack_count: 4, unit_label: "Andes Artillery MS", connected_ids: ["granite_core", "granite_pacific_coast"], is_core: false },
                { id: "granite_caribbean_dock", name: "Caribbean Sea-Gate Anchorage", desc: "Deep-water gantry slips and coastal anti-air missile bunkers.", sub_type: "AIR_NAVAL_GATE", map_x: 170, map_y: 90, controlling_faction: "faction_b", defense_rating: 70, unit_sprite_name: "spr_mini_veh_gunship", stack_count: 6, unit_label: "Caribbean Drop Wing", connected_ids: ["granite_north_gate"], is_core: false },
                { id: "granite_missile_silos", name: "Mato Grosso Anti-Orbital Silos", desc: "Concealed surface-to-orbit missile batteries disguised beneath rainforest canopy.", sub_type: "MISSILE_SILO", map_x: 480, map_y: 350, controlling_faction: "faction_a", defense_rating: 78, unit_sprite_name: "spr_mini_inf_exo_squad", stack_count: 8, unit_label: "Rainforest Exo-Troopers", connected_ids: ["granite_core"], is_core: false },
                { id: "granite_pacific_coast", name: "Pacific Shoreline Forward Depot", desc: "Logistical staging depot and coastal hovercraft slipways.", sub_type: "PERIMETER_DEPOT", map_x: 150, map_y: 340, controlling_faction: "faction_c", defense_rating: 68, unit_sprite_name: "spr_mini_veh_technical", stack_count: 6, unit_label: "Pacific Shore Techs", connected_ids: ["granite_andes_battery"], is_core: false }
            ];
            break;

        case "earth_cascadia_driver":
            _layout.stronghold_name = "Cascadia Mass-Driver Citadel (North America Stronghold)";
            _layout.region = "EARTH";
            _layout.map_sprite_name = "spr_map_earth_theater";
            _layout.minimap_box = { x: 28, y: 24, w: 40, h: 30 };
            _layout.subnodes = [
                { id: "cascadia_apex_driver", name: "Orbital Launch Rail Apex", desc: "Gigawatt kinetic acceleration track hurling shuttlecraft and drop pods into Low Earth Orbit.", sub_type: "MASS_DRIVER", map_x: 340, map_y: 220, controlling_faction: "faction_a", defense_rating: 92, unit_sprite_name: "spr_mini_ms_commander", stack_count: 4, unit_label: "Mass-Driver Command", connected_ids: ["cascadia_san_joaquin_hangar", "cascadia_sierra_redoubt", "cascadia_pacific_dock"], is_core: true },
                { id: "cascadia_san_joaquin_hangar", name: "San Joaquin Heavy Assembly Bay", desc: "High-throughput manufacturing plants forging tank armor and bipedal chassis.", sub_type: "ASSEMBLY_BAY", map_x: 280, map_y: 310, controlling_faction: "faction_a", defense_rating: 78, unit_sprite_name: "spr_mini_veh_heavy_tank", stack_count: 6, unit_label: "Valley Heavy Armor", connected_ids: ["cascadia_apex_driver", "cascadia_mojave_silo"], is_core: false },
                { id: "cascadia_pacific_dock", name: "Puget Sound Naval Slipway", desc: "Submarine pens and coastal patrol interceptors guarding Pacific sea approaches.", sub_type: "AIR_NAVAL_GATE", map_x: 190, map_y: 140, controlling_faction: "faction_b", defense_rating: 72, unit_sprite_name: "spr_mini_veh_gunship", stack_count: 6, unit_label: "Puget Coastal Wing", connected_ids: ["cascadia_apex_driver", "cascadia_sierra_redoubt"], is_core: false },
                { id: "cascadia_sierra_redoubt", name: "High Sierra Anti-Air Fortress", desc: "Ridge-mounted dual beam cannons covering the eastern airspace approach.", sub_type: "MOUNTAIN_BATTERY", map_x: 420, map_y: 180, controlling_faction: "faction_a", defense_rating: 85, unit_sprite_name: "spr_mini_ms_artillery", stack_count: 4, unit_label: "Sierra Flak Battery", connected_ids: ["cascadia_apex_driver", "cascadia_pacific_dock"], is_core: false },
                { id: "cascadia_mojave_silo", name: "Mojave Kinetic Intercept Silos", desc: "Reinforced silos housing long-range hypersonic intercontinental interceptors.", sub_type: "MISSILE_SILO", map_x: 460, map_y: 330, controlling_faction: "faction_c", defense_rating: 76, unit_sprite_name: "spr_mini_inf_exo_squad", stack_count: 8, unit_label: "Mojave Exo-Troopers", connected_ids: ["cascadia_san_joaquin_hangar"], is_core: false },
                { id: "cascadia_perimeter_gate", name: "Great Basin Logistical Gate", desc: "Heavily fortified highway pass channeling armored columns from the continental interior.", sub_type: "PERIMETER_DEPOT", map_x: 180, map_y: 260, controlling_faction: "faction_b", defense_rating: 70, unit_sprite_name: "spr_mini_veh_technical", stack_count: 6, unit_label: "Basin Technical Vanguard", connected_ids: ["cascadia_san_joaquin_hangar"], is_core: false }
            ];
            break;

        case "earth_gibraltar_redoubt":
            _layout.stronghold_name = "Gibraltar Sea-Gate Fortress (Iberian Maritime Stronghold)";
            _layout.region = "EARTH";
            _layout.map_sprite_name = "spr_map_earth_theater";
            _layout.minimap_box = { x: 94, y: 28, w: 34, h: 28 };
            _layout.subnodes = [
                { id: "gibraltar_rock_citadel", name: "Rock of Gibraltar Bastion", desc: "Tunnels hollowed inside the limestone monolith housing command staff and torpedo batteries.", sub_type: "CORE_BUNKER", map_x: 320, map_y: 230, controlling_faction: "faction_a", defense_rating: 96, unit_sprite_name: "spr_mini_ms_commander", stack_count: 4, unit_label: "Gibraltar High Command", connected_ids: ["gibraltar_strait_lock", "gibraltar_andalusian_battery", "gibraltar_alboran_acoustic"], is_core: true },
                { id: "gibraltar_strait_lock", name: "Atlantic-Mediterranean Sea Lock", desc: "Submerged acoustic hydro-gates and magnetic mine nets sealing the maritime channel.", sub_type: "SEA_GATE", map_x: 220, map_y: 260, controlling_faction: "faction_a", defense_rating: 84, unit_sprite_name: "spr_mini_veh_heavy_tank", stack_count: 6, unit_label: "Strait Marine Armor", connected_ids: ["gibraltar_rock_citadel", "gibraltar_ceuta_bridgehead"], is_core: false },
                { id: "gibraltar_alboran_acoustic", name: "Alboran Hydrophone Array", desc: "Deep sensor net tracking hostile submarine thermoclines across the western Mediterranean.", sub_type: "SONAR_PERIMETER", map_x: 440, map_y: 280, controlling_faction: "faction_b", defense_rating: 75, unit_sprite_name: "spr_mini_veh_gunship", stack_count: 6, unit_label: "Alboran Sub-Hunter Wing", connected_ids: ["gibraltar_rock_citadel"], is_core: false },
                { id: "gibraltar_andalusian_battery", name: "Andalusian Ridge Kinetic Battery", desc: "Long-range coastal gun emplacements overlooking the northern approach.", sub_type: "MOUNTAIN_BATTERY", map_x: 340, map_y: 130, controlling_faction: "faction_a", defense_rating: 80, unit_sprite_name: "spr_mini_ms_artillery", stack_count: 4, unit_label: "Andalusian Rail Artillery", connected_ids: ["gibraltar_rock_citadel"], is_core: false },
                { id: "gibraltar_ceuta_bridgehead", name: "Ceuta African Shore Bastion", desc: "Armored redoubt on the North African coastline creating an interlocking crossfire.", sub_type: "PERIMETER_DEPOT", map_x: 180, map_y: 340, controlling_faction: "faction_c", defense_rating: 72, unit_sprite_name: "spr_mini_veh_technical", stack_count: 6, unit_label: "Ceuta Coastal Recon", connected_ids: ["gibraltar_strait_lock"], is_core: false }
            ];
            break;

        case "earth_ural_arsenal":
            _layout.stronghold_name = "Ural Munitions Megafoundry (Eurasian Heavy Stronghold)";
            _layout.region = "EARTH";
            _layout.map_sprite_name = "spr_map_earth_theater";
            _layout.minimap_box = { x: 124, y: 20, w: 34, h: 28 };
            _layout.subnodes = [
                { id: "ural_deep_crucible", name: "Yamantau Central Smelter & Forge", desc: "Colossal underground foundries processing rare earth metals for heavy mobile armors.", sub_type: "FORGE_CORE", map_x: 330, map_y: 240, controlling_faction: "faction_a", defense_rating: 94, unit_sprite_name: "spr_mini_ms_commander", stack_count: 4, unit_label: "Ural Arsenal Staff", connected_ids: ["ural_northern_pit", "ural_steppe_battery", "ural_missile_cavern"], is_core: true },
                { id: "ural_northern_pit", name: "Vorkuta Titanium Mining Trench", desc: "Vast open-cast pit supplying high-grade alloy ingots to the foundry furnaces.", sub_type: "MINING_TRENCH", map_x: 250, map_y: 140, controlling_faction: "faction_a", defense_rating: 74, unit_sprite_name: "spr_mini_veh_heavy_tank", stack_count: 6, unit_label: "Vorkuta Trench Guard", connected_ids: ["ural_deep_crucible", "ural_arctic_radar"], is_core: false },
                { id: "ural_steppe_battery", name: "Chelyabinsk Rail Howitzer Ring", desc: "Long-range kinetic artillery clusters interdicting the open Siberian steppes.", sub_type: "ARTILLERY_BATTERY", map_x: 450, map_y: 290, controlling_faction: "faction_a", defense_rating: 88, unit_sprite_name: "spr_mini_ms_artillery", stack_count: 4, unit_label: "Chelyabinsk Heavy Batteries", connected_ids: ["ural_deep_crucible"], is_core: false },
                { id: "ural_volga_depot", name: "Volga River Staging Gantry", desc: "River barge slipways and repair gantries for deployed armored divisions.", sub_type: "RIVER_DEPOT", map_x: 170, map_y: 310, controlling_faction: "faction_b", defense_rating: 70, unit_sprite_name: "spr_mini_veh_technical", stack_count: 6, unit_label: "Volga Mechanized Corps", connected_ids: ["ural_deep_crucible"], is_core: false },
                { id: "ural_arctic_radar", name: "Polar Zenith Sensor Array", desc: "Early warning phased array radar monitoring orbital drops from polar orbit.", sub_type: "RADAR_SPIRE", map_x: 390, map_y: 110, controlling_faction: "faction_b", defense_rating: 76, unit_sprite_name: "spr_mini_veh_gunship", stack_count: 6, unit_label: "Polar Air Patrol", connected_ids: ["ural_northern_pit"], is_core: false },
                { id: "ural_missile_cavern", name: "Beloretsk Hardened Silo Caverns", desc: "Subterranean launch tubes housing nuclear-tipped orbital denial rockets.", sub_type: "MISSILE_SILO", map_x: 480, map_y: 190, controlling_faction: "faction_a", defense_rating: 82, unit_sprite_name: "spr_mini_inf_exo_squad", stack_count: 8, unit_label: "Beloretsk Exo-Garrison", connected_ids: ["ural_deep_crucible"], is_core: false }
            ];
            break;

        case "earth_shanghai_arcology":
            _layout.stronghold_name = "Neo-Shanghai Arcology Spire (East Asian Megacity Stronghold)";
            _layout.region = "EARTH";
            _layout.map_sprite_name = "spr_map_earth_theater";
            _layout.minimap_box = { x: 144, y: 32, w: 34, h: 28 };
            _layout.subnodes = [
                { id: "shanghai_zenith_core", name: "Arcology Central Spire & Datavault", desc: "One-hundred-story megastructure housing Kurogane Zaibatsu trade computers and command deck.", sub_type: "CORE_BUNKER", map_x: 340, map_y: 210, controlling_faction: "faction_d", defense_rating: 93, unit_sprite_name: "spr_mini_ms_commander", stack_count: 5, unit_label: "Zaibatsu Defense Board", connected_ids: ["shanghai_yangtze_gate", "shanghai_hangzhou_battery", "shanghai_maglev_terminal"], is_core: true },
                { id: "shanghai_yangtze_gate", name: "Yangtze Estuary Surge Barrier", desc: "Heavily armored sea barrier with submersible rail turrets and hovercraft docks.", sub_type: "SEA_GATE", map_x: 230, map_y: 160, controlling_faction: "faction_d", defense_rating: 82, unit_sprite_name: "spr_mini_veh_gunship", stack_count: 6, unit_label: "Estuary Strike Wing", connected_ids: ["shanghai_zenith_core", "shanghai_sub_aquatic_grid"], is_core: false },
                { id: "shanghai_hangzhou_battery", name: "Hangzhou Bay Coastal Redoubt", desc: "Kinetic defense ramparts safeguarding the maritime industrial perimeter.", sub_type: "COASTAL_BATTERY", map_x: 440, map_y: 280, controlling_faction: "faction_d", defense_rating: 78, unit_sprite_name: "spr_mini_ms_artillery", stack_count: 4, unit_label: "Bay Kinetic Turrets", connected_ids: ["shanghai_zenith_core"], is_core: false },
                { id: "shanghai_maglev_terminal", name: "Trans-Asian Maglev Freight Hub", desc: "High-speed rail terminus moving manufactured mecha components across the continent.", sub_type: "LOGISTICS_HUB", map_x: 260, map_y: 320, controlling_faction: "faction_d", defense_rating: 74, unit_sprite_name: "spr_mini_veh_heavy_tank", stack_count: 6, unit_label: "Maglev Armored Guard", connected_ids: ["shanghai_zenith_core"], is_core: false },
                { id: "shanghai_sub_aquatic_grid", name: "Yangtze Sub-Aquatic Sensor Grid", desc: "Acoustic and thermal detection arrays deployed along the river delta seabed.", sub_type: "PERIMETER_DEPOT", map_x: 150, map_y: 240, controlling_faction: "faction_c", defense_rating: 70, unit_sprite_name: "spr_mini_veh_technical", stack_count: 6, unit_label: "Delta Scout Cohort", connected_ids: ["shanghai_yangtze_gate"], is_core: false }
            ];
            break;

        case "earth_sahara_array":
            _layout.stronghold_name = "Al-Kufra Solar Gantry Array (Sahara Orbital Lift Stronghold)";
            _layout.region = "EARTH";
            _layout.map_sprite_name = "spr_map_earth_theater";
            _layout.minimap_box = { x: 96, y: 44, w: 36, h: 32 };
            _layout.subnodes = [
                { id: "kufra_thermal_array", name: "Solar Mirror Field & Uplink Core", desc: "Thousands of heliostat mirrors focusing thermal energy into an orbital power broadcast antenna.", sub_type: "SOLAR_CORE", map_x: 320, map_y: 220, controlling_faction: "faction_c", defense_rating: 91, unit_sprite_name: "spr_mini_ms_commander", stack_count: 4, unit_label: "Solar Array Cadre", connected_ids: ["kufra_dune_perimeter", "kufra_tibesti_battery", "kufra_asphodel_silo"], is_core: true },
                { id: "kufra_dune_perimeter", name: "Erg Chech Hover Armor Patrol", desc: "High-speed hovercraft bases patrolling the shifting red sand sea.", sub_type: "DESERT_PATROL", map_x: 210, map_y: 310, controlling_faction: "faction_c", defense_rating: 75, unit_sprite_name: "spr_mini_veh_technical", stack_count: 6, unit_label: "Desert Hover Vanguard", connected_ids: ["kufra_thermal_array", "kufra_aquifer_pump"], is_core: false },
                { id: "kufra_tibesti_battery", name: "Tibesti Crag Kinetic Flak Redoubt", desc: "Perched atop volcanic sandstone peaks, firing high-explosive flak into orbital drop vectors.", sub_type: "MOUNTAIN_BATTERY", map_x: 420, map_y: 150, controlling_faction: "faction_a", defense_rating: 82, unit_sprite_name: "spr_mini_ms_artillery", stack_count: 4, unit_label: "Tibesti Rail Artillery", connected_ids: ["kufra_thermal_array"], is_core: false },
                { id: "kufra_aquifer_pump", name: "Nubian Sandstone Deep Well", desc: "Vital water and coolant reservoir pumped from two miles below the desert floor.", sub_type: "RESOURCE_NODE", map_x: 160, map_y: 180, controlling_faction: "faction_b", defense_rating: 70, unit_sprite_name: "spr_mini_veh_heavy_tank", stack_count: 6, unit_label: "Aquifer Armor Post", connected_ids: ["kufra_dune_perimeter"], is_core: false },
                { id: "kufra_asphodel_silo", name: "Asphodel Anti-Orbital Silos", desc: "Camouflaged silos hidden beneath thermal baffle cloth to mask launch signatures.", sub_type: "MISSILE_SILO", map_x: 460, map_y: 290, controlling_faction: "faction_c", defense_rating: 78, unit_sprite_name: "spr_mini_inf_exo_squad", stack_count: 8, unit_label: "Asphodel Exo-Troopers", connected_ids: ["kufra_thermal_array"], is_core: false }
            ];
            break;

        case "earth_nordic_vault":
            _layout.stronghold_name = "Skagerrak Sub-Surface Docks (North Sea Submarine Stronghold)";
            _layout.region = "EARTH";
            _layout.map_sprite_name = "spr_map_earth_theater";
            _layout.minimap_box = { x: 94, y: 22, w: 30, h: 26 };
            _layout.subnodes = [
                { id: "skagerrak_grotto_dock", name: "Fjord Submarine Grotto Pens", desc: "Excavated naval slips concealed under granite cliffs, servicing stealth missile submarines.", sub_type: "SUB_HANGAR", map_x: 310, map_y: 230, controlling_faction: "faction_b", defense_rating: 92, unit_sprite_name: "spr_mini_ms_commander", stack_count: 4, unit_label: "Nordic Naval Staff", connected_ids: ["skagerrak_kattegat_sentry", "skagerrak_jotun_bunker", "skagerrak_north_sea_acoustic"], is_core: true },
                { id: "skagerrak_kattegat_sentry", name: "Kattegat Strait Coastal Battery", desc: "Armored coastal emplacements dominating the narrow entrance to the Baltic Sea.", sub_type: "COASTAL_BATTERY", map_x: 420, map_y: 310, controlling_faction: "faction_b", defense_rating: 78, unit_sprite_name: "spr_mini_veh_heavy_tank", stack_count: 6, unit_label: "Kattegat Coastal Armor", connected_ids: ["skagerrak_grotto_dock", "skagerrak_baltic_canal"], is_core: false },
                { id: "skagerrak_north_sea_acoustic", name: "Dogger Bank Sonar Intercept Grid", desc: "Wide-area underwater sensor array detecting hostile amphibious landing vessels.", sub_type: "SONAR_PERIMETER", map_x: 190, map_y: 270, controlling_faction: "faction_b", defense_rating: 74, unit_sprite_name: "spr_mini_veh_gunship", stack_count: 6, unit_label: "North Sea Air Wing", connected_ids: ["skagerrak_grotto_dock"], is_core: false },
                { id: "skagerrak_jotun_bunker", name: "Jotunheimen Hardened Missile Silos", desc: "Mountain-top silos firing long-range anti-ship cruise missiles across the Atlantic corridor.", sub_type: "MISSILE_SILO", map_x: 340, map_y: 120, controlling_faction: "faction_a", defense_rating: 80, unit_sprite_name: "spr_mini_inf_exo_squad", stack_count: 8, unit_label: "Jotun Flak Troopers", connected_ids: ["skagerrak_grotto_dock"], is_core: false },
                { id: "skagerrak_baltic_canal", name: "Kiel Logistics Lock & Slipway", desc: "Strategic canal transit checkpoint for heavy transport barges.", sub_type: "PERIMETER_DEPOT", map_x: 480, map_y: 210, controlling_faction: "faction_c", defense_rating: 72, unit_sprite_name: "spr_mini_veh_technical", stack_count: 6, unit_label: "Kiel Escort Technicals", connected_ids: ["skagerrak_kattegat_sentry"], is_core: false }
            ];
            break;

        case "earth_outback_proving":
            _layout.stronghold_name = "Woomera Kinetic Proving Grounds (Australasia Stronghold)";
            _layout.region = "EARTH";
            _layout.map_sprite_name = "spr_map_earth_theater";
            _layout.minimap_box = { x: 154, y: 64, w: 34, h: 28 };
            _layout.subnodes = [
                { id: "woomera_red_vault", name: "Underground Warhead Vault", desc: "High-security bunker complex storing experimental beam weaponry and orbital kinetic rods.", sub_type: "CORE_BUNKER", map_x: 330, map_y: 240, controlling_faction: "faction_c", defense_rating: 94, unit_sprite_name: "spr_mini_ms_commander", stack_count: 4, unit_label: "Woomera Test Command", connected_ids: ["woomera_salt_flats", "woomera_flinders_battery", "woomera_outback_silo"], is_core: true },
                { id: "woomera_salt_flats", name: "Lake Eyre High-Speed Test Flats", desc: "Kilometers of white salt playa used to calibrate mobile suit hover thrusters and artillery.", sub_type: "DESERT_PATROL", map_x: 220, map_y: 170, controlling_faction: "faction_c", defense_rating: 76, unit_sprite_name: "spr_mini_veh_technical", stack_count: 6, unit_label: "Salt Flat Interceptors", connected_ids: ["woomera_red_vault", "woomera_spencer_anchorage"], is_core: false },
                { id: "woomera_flinders_battery", name: "Flinders Ranges Rail Battery", desc: "Kinetic rail gun turrets dug into ancient quartzite cliffs overlooking the southern sea approaches.", sub_type: "MOUNTAIN_BATTERY", map_x: 430, map_y: 190, controlling_faction: "faction_a", defense_rating: 84, unit_sprite_name: "spr_mini_ms_artillery", stack_count: 4, unit_label: "Flinders Rail Turrets", connected_ids: ["woomera_red_vault"], is_core: false },
                { id: "woomera_spencer_anchorage", name: "Spencer Gulf Hovercraft Slipway", desc: "Coastal supply gantry linking the test range to deep-water maritime logistics.", sub_type: "COASTAL_BATTERY", map_x: 160, map_y: 290, controlling_faction: "faction_b", defense_rating: 72, unit_sprite_name: "spr_mini_veh_gunship", stack_count: 6, unit_label: "Spencer Coastal Patrol", connected_ids: ["woomera_salt_flats"], is_core: false },
                { id: "woomera_outback_silo", name: "Victoria Desert Hardened Silos", desc: "Long-range ballistic missile emplacements hidden among red desert scrub.", sub_type: "MISSILE_SILO", map_x: 450, map_y: 320, controlling_faction: "faction_c", defense_rating: 80, unit_sprite_name: "spr_mini_veh_heavy_tank", stack_count: 6, unit_label: "Desert Heavy Armor", connected_ids: ["woomera_red_vault"], is_core: false }
            ];
            break;

        case "earth_andes_battery":
            _layout.stronghold_name = "Chimborazo Kinetic Bastion (Equatorial Andes Stronghold)";
            _layout.region = "EARTH";
            _layout.map_sprite_name = "spr_map_earth_theater";
            _layout.minimap_box = { x: 44, y: 48, w: 36, h: 30 };
            _layout.subnodes = [
                { id: "chimborazo_zenith_rail", name: "Equatorial High-Angle Mass Launcher", desc: "Glacial summit rail accelerator designed to launch payload containers directly to geosynchronous stations.", sub_type: "MASS_DRIVER", map_x: 320, map_y: 220, controlling_faction: "faction_b", defense_rating: 95, unit_sprite_name: "spr_mini_ms_commander", stack_count: 4, unit_label: "Andean Zenith Staff", connected_ids: ["chimborazo_crag_hangar", "chimborazo_caldera_sensor", "chimborazo_cloud_silo"], is_core: true },
                { id: "chimborazo_crag_hangar", name: "Glacial Ridge Hangar Shelters", desc: "Hardened aircraft shelters carved into volcanic rock at twenty thousand feet elevation.", sub_type: "MOUNTAIN_BATTERY", map_x: 210, map_y: 150, controlling_faction: "faction_b", defense_rating: 82, unit_sprite_name: "spr_mini_ms_artillery", stack_count: 4, unit_label: "Ridge Artillery MS", connected_ids: ["chimborazo_zenith_rail", "chimborazo_guayaquil_gate"], is_core: false },
                { id: "chimborazo_guayaquil_gate", name: "Guayaquil Valley Supply Corridor", desc: "Armored mountain switchback road connecting the high rail launcher to coastal sea lanes.", sub_type: "RIVER_GATE", map_x: 160, map_y: 280, controlling_faction: "faction_a", defense_rating: 72, unit_sprite_name: "spr_mini_veh_heavy_tank", stack_count: 6, unit_label: "Valley Armor Cohort", connected_ids: ["chimborazo_crag_hangar"], is_core: false },
                { id: "chimborazo_caldera_sensor", name: "Cotopaxi Thermal Sensor Spire", desc: "Early warning sensor arrays scanning atmospheric descent corridors.", sub_type: "RADAR_SPIRE", map_x: 420, map_y: 160, controlling_faction: "faction_c", defense_rating: 76, unit_sprite_name: "spr_mini_veh_gunship", stack_count: 6, unit_label: "Volcanic Drone Wing", connected_ids: ["chimborazo_zenith_rail"], is_core: false },
                { id: "chimborazo_cloud_silo", name: "Cloud Forest Concealed Silos", desc: "Sub-canopy launch silos veiled in permanent Andean mist and thermal chaff.", sub_type: "MISSILE_SILO", map_x: 460, map_y: 310, controlling_faction: "faction_b", defense_rating: 78, unit_sprite_name: "spr_mini_inf_exo_squad", stack_count: 8, unit_label: "Cloud Forest Troopers", connected_ids: ["chimborazo_zenith_rail"], is_core: false }
            ];
            break;

        case "earth_antarctic_facility":
            _layout.stronghold_name = "Vostok Sub-Glacial Vault (Antarctic Polar Stronghold)";
            _layout.region = "EARTH";
            _layout.map_sprite_name = "spr_map_earth_theater";
            _layout.minimap_box = { x: 85, y: 88, w: 50, h: 22 };
            _layout.subnodes = [
                { id: "vostok_sub_ice_core", name: "Sub-Glacial Geothermal Core", desc: "Buried beneath four kilometers of ice. Taps thermal vents to power deep research laboratories.", sub_type: "CORE_BUNKER", map_x: 320, map_y: 230, controlling_faction: "faction_b", defense_rating: 97, unit_sprite_name: "spr_mini_ms_commander", stack_count: 4, unit_label: "Cryo-Vault Command", connected_ids: ["vostok_ridge_sentry", "vostok_amundsen_battery", "vostok_cryo_depot"], is_core: true },
                { id: "vostok_ridge_sentry", name: "Transantarctic Ice-Cap Perimeter", desc: "Heavily insulated watchtowers scanning the whiteout for snow crawler convoys.", sub_type: "POLAR_PATROL", map_x: 210, map_y: 160, controlling_faction: "faction_b", defense_rating: 74, unit_sprite_name: "spr_mini_inf_exo_squad", stack_count: 8, unit_label: "Polar Exo-Troopers", connected_ids: ["vostok_sub_ice_core", "vostok_ross_anchorage"], is_core: false },
                { id: "vostok_ross_anchorage", name: "Ross Ice Shelf Submarine Slipway", desc: "Deep ice trench providing submarine egress beneath the southern ice shelves.", sub_type: "AIR_NAVAL_GATE", map_x: 160, map_y: 290, controlling_faction: "faction_a", defense_rating: 76, unit_sprite_name: "spr_mini_veh_gunship", stack_count: 6, unit_label: "Ice Shelf Drop Wing", connected_ids: ["vostok_ridge_sentry"], is_core: false },
                { id: "vostok_amundsen_battery", name: "Amundsen Plateau Rail Battery", desc: "Automated cryo-cooled kinetic rail cannons capable of firing over the South Pole horizon.", sub_type: "MOUNTAIN_BATTERY", map_x: 440, map_y: 170, controlling_faction: "faction_b", defense_rating: 86, unit_sprite_name: "spr_mini_ms_artillery", stack_count: 4, unit_label: "Amundsen Rail Guns", connected_ids: ["vostok_sub_ice_core"], is_core: false },
                { id: "vostok_cryo_depot", name: "Dome C Automated Cryogenic Depot", desc: "Cryo-preservation vault housing seed banks, quantum memory matrices, and strategic prototypes.", sub_type: "LOGISTICS_HUB", map_x: 450, map_y: 310, controlling_faction: "faction_c", defense_rating: 72, unit_sprite_name: "spr_mini_veh_heavy_tank", stack_count: 6, unit_label: "Cryo-Depot Heavy Armor", connected_ids: ["vostok_sub_ice_core"], is_core: false }
            ];
            break;

        case "mars_olympus_caldera":
            _layout.stronghold_name = "Mount Olympus Zenith Redoubt (Martian Super-Volcano Stronghold)";
            _layout.region = "MARS";
            _layout.map_sprite_name = "spr_map_mars_theater";
            _layout.minimap_box = { x: 38, y: 28, w: 54, h: 48 };
            _layout.subnodes = [
                { id: "olympus_caldera_core", name: "Caldera Rim Heavy Fusion Redoubt", desc: "Twenty-two kilometers above the Martian datum. Sovereign command redoubt of the Tharsis Front.", sub_type: "CORE_BUNKER", map_x: 340, map_y: 220, controlling_faction: "faction_f", defense_rating: 98, unit_sprite_name: "spr_mini_ms_commander", stack_count: 5, unit_label: "Red Guard High Command", connected_ids: ["olympus_scarp_battery", "olympus_lava_tube_dock", "olympus_zenith_silos"], is_core: true },
                { id: "olympus_scarp_battery", name: "Basalt Scarp Anti-Orbital Battery", desc: "Kinetic rail cannons mounted along the sheer six-kilometer vertical scarp face.", sub_type: "MOUNTAIN_BATTERY", map_x: 220, map_y: 150, controlling_faction: "faction_f", defense_rating: 88, unit_sprite_name: "spr_mini_ms_artillery", stack_count: 4, unit_label: "Scarp Kinetic Battery", connected_ids: ["olympus_caldera_core", "olympus_aureole_sentry"], is_core: false },
                { id: "olympus_lava_tube_dock", name: "Lava Tube Mobile Suit Hangar", desc: "Ancient volcanic lava tubes sealed and pressurized into vast subterranean hangar decks.", sub_type: "SUB_HANGAR", map_x: 450, map_y: 270, controlling_faction: "faction_f", defense_rating: 82, unit_sprite_name: "spr_mini_veh_heavy_tank", stack_count: 6, unit_label: "Caldera Heavy Armor", connected_ids: ["olympus_caldera_core"], is_core: false },
                { id: "olympus_aureole_sentry", name: "Aureole Plain Perimeter Chokepoint", desc: "Armored checkpoint interdicting ground crawler approaches across the volcanic apron.", sub_type: "PERIMETER_DEPOT", map_x: 160, map_y: 280, controlling_faction: "faction_f", defense_rating: 76, unit_sprite_name: "spr_mini_veh_technical", stack_count: 6, unit_label: "Aureole Technical Rovers", connected_ids: ["olympus_scarp_battery"], is_core: false },
                { id: "olympus_zenith_silos", name: "Zenith Surface-to-Orbit Torpedo Silos", desc: "Vertical missile tubes firing thermonuclear interceptors into low Martian orbit.", sub_type: "MISSILE_SILO", map_x: 420, map_y: 130, controlling_faction: "faction_f", defense_rating: 85, unit_sprite_name: "spr_mini_inf_exo_squad", stack_count: 8, unit_label: "Olympus Zenith Shock Troops", connected_ids: ["olympus_caldera_core"], is_core: false }
            ];
            break;

        default:
            // Graceful procedural stronghold generation for any other territory
            var _terr = scr_territory_get(_stronghold_id);
            if (!is_undefined(_terr)) {
                _layout.stronghold_name = _terr.name + " (Regional Stronghold)";
                _layout.region = _terr.region;
                _layout.map_sprite_name = (_terr.region == "MARS") ? "spr_map_mars_theater" : ((_terr.region == "SPACE") ? "spr_map_space_theater" : "spr_map_earth_theater");
                _layout.minimap_box = { x: 50, y: 50, w: 40, h: 30 };
                _layout.subnodes = [
                    { id: _stronghold_id + "_core", name: _terr.name + " Central HQ", desc: _terr.lore_brief, sub_type: "CORE_BUNKER", map_x: 330, map_y: 220, controlling_faction: _terr.controlling_faction, defense_rating: _terr.defense_rating, unit_sprite_name: "spr_mini_ms_commander", stack_count: 4, unit_label: "Garrison Command", connected_ids: [_stronghold_id + "_north", _stronghold_id + "_south"], is_core: true },
                    { id: _stronghold_id + "_north", name: "Northern Defensive Flank", desc: "Perimeter checkpoint and armored outpost.", sub_type: "PERIMETER_DEPOT", map_x: 220, map_y: 160, controlling_faction: _terr.controlling_faction, defense_rating: max(60, _terr.defense_rating - 15), unit_sprite_name: "spr_mini_veh_heavy_tank", stack_count: 6, unit_label: "Northern Armor", connected_ids: [_stronghold_id + "_core"], is_core: false },
                    { id: _stronghold_id + "_south", name: "Southern Logistics Redoubt", desc: "Munitions storage and hovercraft slipway.", sub_type: "LOGISTICS_HUB", map_x: 440, map_y: 280, controlling_faction: _terr.controlling_faction, defense_rating: max(60, _terr.defense_rating - 18), unit_sprite_name: "spr_mini_veh_technical", stack_count: 6, unit_label: "Supply Escort", connected_ids: [_stronghold_id + "_core"], is_core: false }
                ];
            }
            break;
    }
    
    return _layout;
}

/// @function scr_stronghold_get_subnode(_stronghold_id, _subnode_id)
/// @description Returns a specific local defense subnode from a stronghold layout
function scr_stronghold_get_subnode(_stronghold_id, _subnode_id) {
    var _layout = scr_stronghold_get_layout(_stronghold_id);
    for (var i = 0; i < array_length(_layout.subnodes); i++) {
        if (_layout.subnodes[i].id == _subnode_id) return _layout.subnodes[i];
    }
    return (array_length(_layout.subnodes) > 0) ? _layout.subnodes[0] : undefined;
}


// =========================================================================
// SHIN GIHREN'S GREED 16x10 HEX TACTICAL GRID ENGINE
// Tile-by-tile MP movement, terrain costs (river/mountain/plains), and turn cycles
// =========================================================================

/// @function scr_hex_get_screen_pos(_c, _r, _rad_x, _rad_y)
/// @description Returns screen position struct { x, y } for hex at column _c, row _r
function scr_hex_get_screen_pos(_c, _r, _rad_x, _rad_y) {
    var _start_x = _rad_x + 36;
    var _start_y = _rad_y + 42;
    var _col_dist = 42;
    var _row_dist = 48;
    var _odd_offset = 24;
    var _hx = _start_x + _c * _col_dist;
    var _hy = _start_y + _r * _row_dist + ((_c % 2 == 1) ? _odd_offset : 0);
    return { x: _hx, y: _hy };
}

/// @function scr_screen_to_hex(_mx, _my, _rad_x, _rad_y)
/// @description Returns hex coordinates struct { col, row } at mouse screen position
function scr_screen_to_hex(_mx, _my, _rad_x, _rad_y) {
    var _start_x = _rad_x + 36;
    var _start_y = _rad_y + 42;
    var _col_dist = 42;
    var _row_dist = 48;
    var _odd_offset = 24;
    
    var _approx_c = round((_mx - _start_x) / _col_dist);
    var _best_c = -1;
    var _best_r = -1;
    var _min_d = 999999;
    
    for (var _dc = -1; _dc <= 1; _dc++) {
        var _c = _approx_c + _dc;
        if (_c < 0 || _c >= 16) continue;
        var _y_base = _start_y + ((_c % 2 == 1) ? _odd_offset : 0);
        var _approx_r = round((_my - _y_base) / _row_dist);
        for (var _dr = -1; _dr <= 1; _dr++) {
            var _r = _approx_r + _dr;
            if (_r < 0 || _r >= 10) continue;
            var _pos = scr_hex_get_screen_pos(_c, _r, _rad_x, _rad_y);
            var _d = point_distance(_mx, _my, _pos.x, _pos.y);
            if (_d < _min_d) {
                _min_d = _d;
                _best_c = _c;
                _best_r = _r;
            }
        }
    }
    
    if (_min_d <= 28) {
        return { col: _best_c, row: _best_r };
    }
    return { col: -1, row: -1 };
}

/// @function scr_hex_get_neighbors(_c, _r)
/// @description Returns array of valid adjacent neighbor coordinate structs { col, row }
function scr_hex_get_neighbors(_c, _r) {
    var _res = [];
    var _raw = [];
    if (_c % 2 == 0) {
        _raw = [
            { col: _c, row: _r - 1 },
            { col: _c + 1, row: _r - 1 },
            { col: _c + 1, row: _r },
            { col: _c, row: _r + 1 },
            { col: _c - 1, row: _r },
            { col: _c - 1, row: _r - 1 }
        ];
    } else {
        _raw = [
            { col: _c, row: _r - 1 },
            { col: _c + 1, row: _r },
            { col: _c + 1, row: _r + 1 },
            { col: _c, row: _r + 1 },
            { col: _c - 1, row: _r + 1 },
            { col: _c - 1, row: _r }
        ];
    }
    for (var i = 0; i < array_length(_raw); i++) {
        var _nc = _raw[i].col;
        var _nr = _raw[i].row;
        if (_nc >= 0 && _nc < 16 && _nr >= 0 && _nr < 10) {
            array_push(_res, _raw[i]);
        }
    }
    return _res;
}

/// @function scr_hex_distance(_c1, _r1, _c2, _r2)
/// @description Returns axial/cube distance in hex steps between two hex cells
function scr_hex_distance(_c1, _r1, _c2, _r2) {
    var _x1 = _c1;
    var _z1 = _r1 - floor((_c1 - (_c1 & 1)) / 2);
    var _y1 = -_x1 - _z1;
    
    var _x2 = _c2;
    var _z2 = _r2 - floor((_c2 - (_c2 & 1)) / 2);
    var _y2 = -_x2 - _z2;
    
    return floor((abs(_x1 - _x2) + abs(_y1 - _y2) + abs(_z1 - _z2)) / 2);
}

/// @function scr_hex_get_stronghold_terrain(_stronghold_id)
/// @description Generates a 16x10 terrain matrix for the specified stronghold
function scr_hex_get_stronghold_terrain(_stronghold_id) {
    var _grid = array_create(16);
    var _layout = scr_stronghold_get_layout(_stronghold_id);
    var _reg = _layout.region;
    
    for (var c = 0; c < 16; c++) {
        _grid[c] = array_create(10);
        for (var r = 0; r < 10; r++) {
            var _t_type = "CRATON";
            var _t_name = "Basalt Craton";
            var _mp_cost = 1;
            var _def = 10;
            
            // Geography patterns based on region and coordinates
            if (_reg == "MARS") {
                // Mars Caldera: Center caldera crater, Basalt scarp in north
                if (c >= 6 && c <= 10 && r >= 3 && r <= 6) {
                    _t_type = "CRATER";
                    _t_name = "Caldera Floor";
                    _mp_cost = 1;
                    _def = 15;
                } else if (r <= 2 && c >= 3 && c <= 12) {
                    _t_type = "MOUNTAIN";
                    _t_name = "Basalt Scarp";
                    _mp_cost = 3;
                    _def = 35;
                } else if (c >= 13 || r >= 8) {
                    _t_type = "ROUGH";
                    _t_name = "Volcanic Apron";
                    _mp_cost = 2;
                    _def = 20;
                }
            } else if (string_pos("cascadia", _stronghold_id) > 0) {
                // Cascadia: Pacific water on left, Mass driver in middle, mountains on right
                if (c <= 3) {
                    _t_type = "WATER";
                    _t_name = "Pacific Shelf";
                    _mp_cost = 3;
                    _def = 0;
                } else if (c >= 12) {
                    _t_type = "MOUNTAIN";
                    _t_name = "Cascade Range";
                    _mp_cost = 3;
                    _def = 35;
                } else if (c >= 4 && c <= 6 && (r == 4 || r == 5)) {
                    _t_type = "FOREST";
                    _t_name = "Coastal Redwoods";
                    _mp_cost = 2;
                    _def = 20;
                }
            } else if (string_pos("gibraltar", _stronghold_id) > 0) {
                // Gibraltar: Strait water crossing horizontally
                if (r >= 4 && r <= 6) {
                    _t_type = "WATER";
                    _t_name = "Gibraltar Strait";
                    _mp_cost = 3;
                    _def = 0;
                } else if (c <= 4 || c >= 12) {
                    _t_type = "MOUNTAIN";
                    _t_name = "Pillars of Hercules";
                    _mp_cost = 3;
                    _def = 35;
                }
            } else {
                // Standard Earth Stronghold (e.g. Granite Deep Amazon)
                // River winding through c=6..8
                if ((c == 7 && r >= 1 && r <= 8) || (c == 6 && r >= 3 && r <= 5) || (c == 8 && r >= 6 && r <= 9)) {
                    _t_type = "WATER";
                    _t_name = "Amazon Tributary";
                    _mp_cost = 3;
                    _def = 0;
                } else if ((c >= 3 && c <= 5 && r <= 3) || (c >= 11 && c <= 13 && r >= 7)) {
                    _t_type = "FOREST";
                    _t_name = "Amazon Canopy";
                    _mp_cost = 2;
                    _def = 20;
                } else if ((c <= 2 && r <= 3) || (c >= 13 && r <= 3)) {
                    _t_type = "MOUNTAIN";
                    _t_name = "Granite Ridge";
                    _mp_cost = 3;
                    _def = 35;
                }
            }
            
            _grid[c][r] = {
                terrain_type: _t_type,
                name: _t_name,
                mp_cost: _mp_cost,
                defense_bonus: _def,
                facility_id: "",
                controlling_faction: "neutral"
            };
        }
    }
    
    // Stamp Strategic Subnode Base Facilities onto the Hex Grid
    for (var sni = 0; sni < array_length(_layout.subnodes); sni++) {
        var _sn = _layout.subnodes[sni];
        var _fc = clamp(round((_sn.map_x / 580.0) * 12.0) + 2, 1, 14);
        var _fr = clamp(round((_sn.map_y / 360.0) * 8.0) + 1, 1, 8);
        
        _grid[_fc][_fr].terrain_type = "BASE_FACILITY";
        _grid[_fc][_fr].name = _sn.name;
        _grid[_fc][_fr].mp_cost = 1;
        _grid[_fc][_fr].defense_bonus = 40;
        _grid[_fc][_fr].facility_id = _sn.id;
        _grid[_fc][_fr].controlling_faction = _sn.controlling_faction;
        _grid[_fc][_fr].sub_type = variable_struct_exists(_sn, "sub_type") ? _sn.sub_type : "DEPOT";
        _grid[_fc][_fr].is_core = variable_struct_exists(_sn, "is_core") ? _sn.is_core : false;
        _grid[_fc][_fr].capture_progress = (_sn.controlling_faction == "pmc") ? 100 : 0;
        _grid[_fc][_fr].capture_turns_required = (variable_struct_exists(_sn, "is_core") && _sn.is_core) ? 3 : 2;
        _grid[_fc][_fr].is_captured = (_sn.controlling_faction == "pmc");
    }
    
    return _grid;
}

/// @function scr_hex_get_stronghold_units(_stronghold_id)
/// @description Spawns initial tactical PMC vanguard and OPFOR defense units on the hex grid
function scr_hex_get_stronghold_units(_stronghold_id) {
    var _units = [];
    var _layout = scr_stronghold_get_layout(_stronghold_id);
    var _opfor_fac = "faction_b";
    if (array_length(_layout.subnodes) > 0) {
        _opfor_fac = _layout.subnodes[0].controlling_faction;
    }
    if (_opfor_fac == "pmc") _opfor_fac = "faction_c";
    
    // --- 1. Player PMC Vanguard Strike Squadrons ---
    array_push(_units, {
        id: "pmc_vanguard_ironclad",
        name: "Ironclad Vanguard Alpha",
        unit_label: "GHA-07 Ironclad",
        faction: "pmc",
        sprite_name: "spr_mini_ms_ironclad",
        col: 2,
        row: 4,
        max_mp: 4,
        current_mp: 4,
        hp: 100,
        max_hp: 100,
        attack: 45,
        defense: 30,
        range: 1,
        sensor_range: 2,
        stack_count: 3,
        status: "READY"
    });
    
    array_push(_units, {
        id: "pmc_vanguard_striker",
        name: "Aero-Striker Ace Flight",
        unit_label: "F-102 Aero-Striker",
        faction: "pmc",
        sprite_name: "spr_mini_ms_aerostriker",
        col: 2,
        row: 6,
        max_mp: 5,
        current_mp: 5,
        hp: 80,
        max_hp: 80,
        attack: 40,
        defense: 20,
        range: 2,
        sensor_range: 3,
        stack_count: 3,
        status: "READY"
    });

    array_push(_units, {
        id: "pmc_vanguard_armor",
        name: "Heavy Armor Battalion",
        unit_label: "Mammoth Siege Tank",
        faction: "pmc",
        sprite_name: "spr_mini_veh_heavy_tank",
        col: 3,
        row: 3,
        max_mp: 3,
        current_mp: 3,
        hp: 120,
        max_hp: 120,
        attack: 50,
        defense: 35,
        range: 2,
        sensor_range: 2,
        stack_count: 5,
        status: "READY"
    });

    array_push(_units, {
        id: "pmc_vanguard_recon",
        name: "Vanguard Recon Technical",
        unit_label: "Armed Scout Technical",
        faction: "pmc",
        sprite_name: "spr_mini_veh_technical",
        col: 4,
        row: 5,
        max_mp: 5,
        current_mp: 5,
        hp: 60,
        max_hp: 60,
        attack: 30,
        defense: 16,
        range: 1,
        sensor_range: 4,
        stack_count: 6,
        status: "READY"
    });

    array_push(_units, {
        id: "pmc_vanguard_exo",
        name: "Combat Exo Engineers",
        unit_label: "Exo Squad Vanguard",
        faction: "pmc",
        sprite_name: "spr_mini_inf_exo_squad",
        col: 3,
        row: 7,
        max_mp: 2,
        current_mp: 2,
        hp: 65,
        max_hp: 65,
        attack: 32,
        defense: 18,
        range: 1,
        sensor_range: 1,
        stack_count: 8,
        status: "READY"
    });

    // --- 2. OPFOR Stronghold Defense Garrison ---
    array_push(_units, {
        id: "opfor_cmd_flagship",
        name: "OPFOR Command Flagship",
        unit_label: "Garrison Command MS",
        faction: _opfor_fac,
        sprite_name: "spr_mini_ms_commander",
        col: 12,
        row: 4,
        max_mp: 4,
        current_mp: 4,
        hp: 110,
        max_hp: 110,
        attack: 48,
        defense: 32,
        range: 2,
        sensor_range: 2,
        stack_count: 4,
        status: "READY"
    });

    array_push(_units, {
        id: "opfor_heavy_artillery",
        name: "Siege Battery MS Platoon",
        unit_label: "Long-Range Rail MS",
        faction: _opfor_fac,
        sprite_name: "spr_mini_ms_artillery",
        col: 13,
        row: 2,
        max_mp: 3,
        current_mp: 3,
        hp: 85,
        max_hp: 85,
        attack: 55,
        defense: 22,
        range: 3,
        sensor_range: 2,
        stack_count: 4,
        status: "READY"
    });

    array_push(_units, {
        id: "opfor_frontline_grunt",
        name: "Garrison Frontline MS",
        unit_label: "Standard Grunt MS",
        faction: _opfor_fac,
        sprite_name: "spr_mini_ms_grunt",
        col: 9,
        row: 3,
        max_mp: 4,
        current_mp: 4,
        hp: 90,
        max_hp: 90,
        attack: 42,
        defense: 25,
        range: 1,
        sensor_range: 2,
        stack_count: 4,
        status: "READY"
    });

    array_push(_units, {
        id: "opfor_defense_armor",
        name: "Redoubt Armor Division",
        unit_label: "Heavy Defense Armor",
        faction: _opfor_fac,
        sprite_name: "spr_mini_veh_heavy_tank",
        col: 11,
        row: 6,
        max_mp: 3,
        current_mp: 3,
        hp: 110,
        max_hp: 110,
        attack: 45,
        defense: 30,
        range: 1,
        sensor_range: 2,
        stack_count: 5,
        status: "READY"
    });

    array_push(_units, {
        id: "opfor_recon_rover",
        name: "Perimeter Recon Technicals",
        unit_label: "Armed Scout Technicals",
        faction: _opfor_fac,
        sprite_name: "spr_mini_veh_technical",
        col: 8,
        row: 7,
        max_mp: 4,
        current_mp: 4,
        hp: 70,
        max_hp: 70,
        attack: 35,
        defense: 18,
        range: 1,
        sensor_range: 3,
        stack_count: 6,
        status: "READY"
    });

    return _units;
}
/// @function scr_hex_get_reachable(_unit, _units_array, _terrain_grid)
/// @description Returns struct of reachable hex keys { "c_r": move_cost } via Dijkstra algorithm
function scr_hex_get_reachable(_unit, _units_array, _terrain_grid) {
    var _reachable = {};
    if (is_undefined(_unit) || _unit.current_mp <= 0) return _reachable;
    
    // Stacking Check: Block enemy hexes and full friendly stacks (Gihren's Greed max 6 units per hex)
    var _occupied = {};
    var _friendly_counts = {};
    for (var i = 0; i < array_length(_units_array); i++) {
        var _u = _units_array[i];
        if (_u.id != _unit.id && _u.hp > 0) {
            var _ukey = string(_u.col) + "_" + string(_u.row);
            if (_u.faction != _unit.faction) {
                _occupied[$ _ukey] = true;
            } else {
                var _cnt = variable_struct_exists(_friendly_counts, _ukey) ? _friendly_counts[$ _ukey] : 0;
                _cnt += 1;
                _friendly_counts[$ _ukey] = _cnt;
                if (_cnt >= 6) {
                    _occupied[$ _ukey] = true;
                }
            }
        }
    }
    
    var _dist = {};
    var _start_key = string(_unit.col) + "_" + string(_unit.row);
    _dist[$ _start_key] = 0;
    
    var _queue = [{ col: _unit.col, row: _unit.row, cost: 0 }];
    
    while (array_length(_queue) > 0) {
        var _best_idx = 0;
        var _best_cost = _queue[0].cost;
        for (var q = 1; q < array_length(_queue); q++) {
            if (_queue[q].cost < _best_cost) {
                _best_cost = _queue[q].cost;
                _best_idx = q;
            }
        }
        var _curr = _queue[_best_idx];
        array_delete(_queue, _best_idx, 1);
        
        var _curr_key = string(_curr.col) + "_" + string(_curr.row);
        var _curr_dist = variable_struct_exists(_dist, _curr_key) ? _dist[$ _curr_key] : 999999;
        if (_curr.cost > _curr_dist) continue;
        
        var _nbrs = scr_hex_get_neighbors(_curr.col, _curr.row);
        for (var n = 0; n < array_length(_nbrs); n++) {
            var _nc = _nbrs[n].col;
            var _nr = _nbrs[n].row;
            var _nkey = string(_nc) + "_" + string(_nr);
            
            // Check occupied
            if (variable_struct_exists(_occupied, _nkey)) {
                continue; // Cannot enter occupied hex
            }
            
            var _step_cost = 1;
            if (!is_undefined(_terrain_grid) && _nc < array_length(_terrain_grid) && _nr < array_length(_terrain_grid[_nc])) {
                _step_cost = _terrain_grid[_nc][_nr].mp_cost;
            }
            
            var _new_cost = _curr.cost + _step_cost;
            if (_new_cost <= _unit.current_mp) {
                var _prev_d = variable_struct_exists(_dist, _nkey) ? _dist[$ _nkey] : 999999;
                if (_new_cost < _prev_d) {
                    _dist[$ _nkey] = _new_cost;
                    variable_struct_set(_reachable, _nkey, _new_cost);
                    array_push(_queue, { col: _nc, row: _nr, cost: _new_cost });
                }
            }
        }
    }
    
    return _reachable;
}

/// @function scr_hex_resolve_skirmish(_attacker, _defender, _def_terr_bonus, _units_array)
/// @description Computes skirmish combat damage with combined stack firepower and distributed damage
function scr_hex_resolve_skirmish(_attacker, _defender, _def_terr_bonus = 10, _units_array = undefined) {
    if (is_undefined(_def_terr_bonus)) _def_terr_bonus = 10;
    
    var _combined_atk = _attacker.attack;
    if (!is_undefined(_units_array)) {
        _combined_atk = 0;
        for (var i = 0; i < array_length(_units_array); i++) {
            var _au = _units_array[i];
            if (_au.hp > 0 && _au.col == _attacker.col && _au.row == _attacker.row && _au.faction == _attacker.faction) {
                var _edist = scr_hex_distance(_au.col, _au.row, _defender.col, _defender.row);
                if (_edist <= _au.range) {
                    _combined_atk += _au.attack;
                }
            }
        }
        if (_combined_atk <= 0) _combined_atk = _attacker.attack;
    }
    
    var _atk_val = _combined_atk * (1.0 + (irandom_range(-15, 15) / 100.0));
    var _eff_def = _defender.defense * (1.0 + (_def_terr_bonus / 100.0));
    var _dmg_to_def = max(8, floor(_atk_val * (100.0 / (100.0 + _eff_def))));
    
    var _rem_dmg = _dmg_to_def;
    if (!is_undefined(_units_array)) {
        for (var i = 0; i < array_length(_units_array); i++) {
            var _du = _units_array[i];
            if (_du.hp > 0 && _du.col == _defender.col && _du.row == _defender.row && _du.faction == _defender.faction) {
                var _absorb = min(_du.hp, _rem_dmg);
                _du.hp = max(0, _du.hp - _absorb);
                _rem_dmg -= _absorb;
                if (_rem_dmg <= 0) break;
            }
        }
    } else {
        _defender.hp = max(0, _defender.hp - _dmg_to_def);
    }
    
    var _retaliate_dmg = 0;
    var _dist = scr_hex_distance(_attacker.col, _attacker.row, _defender.col, _defender.row);
    if (_defender.hp > 0 && _dist <= _defender.range) {
        var _def_atk = _defender.attack * (1.0 + (irandom_range(-15, 15) / 100.0)) * 0.75;
        var _att_eff_def = _attacker.defense;
        _retaliate_dmg = max(5, floor(_def_atk * (100.0 / (100.0 + _att_eff_def))));
        _attacker.hp = max(0, _attacker.hp - _retaliate_dmg);
    }
    
    return {
        attacker_id: _attacker.id,
        defender_id: _defender.id,
        damage_dealt: _dmg_to_def,
        damage_taken: _retaliate_dmg,
        defender_destroyed: (_defender.hp <= 0),
        attacker_destroyed: (_attacker.hp <= 0)
    };
}

/// @function scr_stronghold_advance_turn(_stronghold_id, _units_array, _terrain_grid, _turn_num)
/// @description Advances tactical turn: Executes OPFOR AI phase, resolves engagements, refreshes MPs
function scr_stronghold_advance_turn(_stronghold_id, _units_array, _terrain_grid, _turn_num) {
    var _log = [];
    array_push(_log, "=== CYCLE " + string(_turn_num) + " CONCLUDED. ADVANCING TO CYCLE " + string(_turn_num + 1) + " ===");
    
    // OPFOR AI Phase: Maneuver & Engage
    for (var i = 0; i < array_length(_units_array); i++) {
        var _u = _units_array[i];
        if (_u.faction != "pmc" && _u.hp > 0) {
            var _nearest_pmc = undefined;
            var _min_dist = 999;
            for (var p = 0; p < array_length(_units_array); p++) {
                var _pu = _units_array[p];
                if (_pu.faction == "pmc" && _pu.hp > 0) {
                    var _d = scr_hex_distance(_u.col, _u.row, _pu.col, _pu.row);
                    if (_d < _min_dist) {
                        _min_dist = _d;
                        _nearest_pmc = _pu;
                    }
                }
            }
            
            if (!is_undefined(_nearest_pmc)) {
                if (_min_dist <= _u.range) {
                    var _terr_def = 10;
                    if (!is_undefined(_terrain_grid) && _nearest_pmc.col < array_length(_terrain_grid) && _nearest_pmc.row < array_length(_terrain_grid[_nearest_pmc.col])) {
                        _terr_def = _terrain_grid[_nearest_pmc.col][_nearest_pmc.row].defense_bonus;
                    }
                    var _sk = scr_hex_resolve_skirmish(_u, _nearest_pmc, _terr_def, _units_array);
                    scr_audio_play_skirmish_combat(_u, _nearest_pmc, _sk.defender_destroyed);
                    var _msg = "OPFOR " + _u.unit_label + " ENGAGED " + _nearest_pmc.unit_label + ": -" + string(_sk.damage_dealt) + " HP";
                    if (_sk.defender_destroyed) _msg += " [UNIT DESTROYED!]";
                    array_push(_log, _msg);
                } else {
                    var _nbrs = scr_hex_get_neighbors(_u.col, _u.row);
                    var _best_nbr = undefined;
                    var _best_dist = _min_dist;
                    for (var n = 0; n < array_length(_nbrs); n++) {
                        var _cand = _nbrs[n];
                        var _is_occ = false;
                        for (var o = 0; o < array_length(_units_array); o++) {
                            if (_units_array[o].hp > 0 && _units_array[o].col == _cand.col && _units_array[o].row == _cand.row) {
                                _is_occ = true;
                                break;
                            }
                        }
                        if (!_is_occ) {
                            var _nd = scr_hex_distance(_cand.col, _cand.row, _nearest_pmc.col, _nearest_pmc.row);
                            if (_nd < _best_dist) {
                                _best_dist = _nd;
                                _best_nbr = _cand;
                            }
                        }
                    }
                    if (!is_undefined(_best_nbr)) {
                        _u.col = _best_nbr.col;
                        _u.row = _best_nbr.row;
                        array_push(_log, "OPFOR " + _u.unit_label + " ADVANCED TO SECTOR [" + string(_u.col) + "," + string(_u.row) + "]");
                    }
                }
            }
        }
    }
    
    // Facility Capture, Contestation & Field Repairs
    if (!is_undefined(_terrain_grid)) {
        var _sh_layout = scr_stronghold_get_layout(_stronghold_id);
        for (var c = 0; c < 16; c++) {
            for (var r = 0; r < 10; r++) {
                var _fac = _terrain_grid[c][r];
                if (_fac.terrain_type == "BASE_FACILITY") {
                    var _occ_u = undefined;
                    for (var u = 0; u < array_length(_units_array); u++) {
                        var _cand = _units_array[u];
                        if (_cand.hp > 0 && _cand.col == c && _cand.row == r) {
                            _occ_u = _cand;
                            break;
                        }
                    }

                    if (!is_undefined(_occ_u)) {
                        if (_occ_u.faction == "pmc") {
                            if (_fac.controlling_faction != "pmc") {
                                var _rate = floor(100.0 / _fac.capture_turns_required);
                                _fac.capture_progress = min(100, _fac.capture_progress + _rate);
                                if (_fac.capture_progress >= 100) {
                                    _fac.controlling_faction = "pmc";
                                    _fac.is_captured = true;
                                    scr_audio_play_facility_capture();
                                    array_push(_log, "★ SECTOR CAPTURED: " + _fac.name + " SECURED BY PMC!");
                                    for (var sni = 0; sni < array_length(_sh_layout.subnodes); sni++) {
                                        if (_sh_layout.subnodes[sni].id == _fac.facility_id) {
                                            _sh_layout.subnodes[sni].controlling_faction = "pmc";
                                        }
                                    }
                                    if (_fac.is_core || _fac.sub_type == "CORE_BUNKER") {
                                        array_push(_log, "🏆 VICTORY: CORE REACTOR SECURED! CITADEL LIBERATED!");
                                    }
                                } else {
                                    array_push(_log, "OCCUPATION: " + _fac.name + " CAPTURE GAUGE AT " + string(_fac.capture_progress) + "%");
                                }
                            } else {
                                if (_occ_u.hp < _occ_u.max_hp) {
                                    _occ_u.hp = min(_occ_u.max_hp, _occ_u.hp + 20);
                                    scr_audio_play_sfx(snd_plasma_weld, 0.75, 0.08);
                                    array_push(_log, "FIELD REPAIRS: " + _occ_u.unit_label + " REPAIRED (+20 HP) AT " + _fac.name);
                                }
                            }
                        } else if (_occ_u.faction != "pmc" && _fac.controlling_faction == "pmc") {
                            _fac.capture_progress = max(0, _fac.capture_progress - 50);
                            if (_fac.capture_progress <= 0) {
                                _fac.controlling_faction = _occ_u.faction;
                                _fac.is_captured = false;
                                array_push(_log, "⚠ ALERT: " + _fac.name + " RECAPTURED BY HOSTILE GARRISON!");
                            } else {
                                array_push(_log, "⚠ WARNING: HOSTILE MECHS CONTESTING " + _fac.name + "!");
                            }
                        }
                    }
                }
            }
        }
    }

    // Refresh all active units MP and status (revert fortified stance bonus)
    for (var i = 0; i < array_length(_units_array); i++) {
        var _u = _units_array[i];
        if (_u.hp > 0) {
            if (_u.status == "FORTIFIED") {
                _u.defense = max(10, _u.defense - 15);
            }
            _u.current_mp = _u.max_mp;
            _u.status = "READY";
        }
    }
    
    array_push(_log, "CYCLE " + string(_turn_num + 1) + ": ALL VANGUARD UNITS RE-ARMED & RE-FUELED.");
    return _log;
}


// =========================================================================
// PROMETHEUS FLUX FOG OF WAR & RADAR RECONNAISSANCE ENGINE
// 0 = UNEXPLORED (Blackout), 1 = FOG_OF_WAR (Previously Explored), 2 = VISIBLE (Illuminated)
// =========================================================================

/// @function scr_hex_init_fog_of_war()
/// @description Initializes a 16x10 fog of war visibility matrix
function scr_hex_init_fog_of_war() {
    var _fog = array_create(16);
    for (var c = 0; c < 16; c++) {
        _fog[c] = array_create(10, 0); // 0 = UNEXPLORED
    }
    return _fog;
}

/// @function scr_hex_update_fog_of_war(_fog_grid, _units_array, _terrain_grid)
/// @description Updates hex visibility based on friendly unit sensors and base radar
function scr_hex_update_fog_of_war(_fog_grid, _units_array, _terrain_grid) {
    if (is_undefined(_fog_grid)) return [];
    
    // 1. Demote currently VISIBLE (2) cells down to EXPLORED_FOG (1)
    for (var c = 0; c < 16; c++) {
        for (var r = 0; r < 10; r++) {
            if (_fog_grid[c][r] == 2) {
                _fog_grid[c][r] = 1;
            }
        }
    }
    
    // 2. Active Sensor Sweep from all Friendly PMC Units
    for (var i = 0; i < array_length(_units_array); i++) {
        var _u = _units_array[i];
        if (_u.faction == "pmc" && _u.hp > 0) {
            var _sr = variable_struct_exists(_u, "sensor_range") ? _u.sensor_range : 2;
            for (var c = 0; c < 16; c++) {
                for (var r = 0; r < 10; r++) {
                    if (scr_hex_distance(_u.col, _u.row, c, r) <= _sr) {
                        _fog_grid[c][r] = 2; // Actively illuminated
                    }
                }
            }
        }
    }
    
    // 3. Fixed Radar Perimeter from Friendly Base Facilities
    if (!is_undefined(_terrain_grid)) {
        for (var c = 0; c < 16; c++) {
            for (var r = 0; r < 10; r++) {
                if (_terrain_grid[c][r].terrain_type == "BASE_FACILITY" && _terrain_grid[c][r].controlling_faction == "pmc") {
                    for (var nc = 0; nc < 16; nc++) {
                        for (var nr = 0; nr < 10; nr++) {
                            if (scr_hex_distance(c, r, nc, nr) <= 2) {
                                _fog_grid[nc][nr] = 2;
                            }
                        }
                    }
                }
            }
        }
    }
    
    // 4. Detect Spotted Hostiles in Sensor Perimeter
    var _spotted = [];
    for (var i = 0; i < array_length(_units_array); i++) {
        var _eu = _units_array[i];
        if (_eu.faction != "pmc" && _eu.hp > 0) {
            if (_fog_grid[_eu.col][_eu.row] == 2) {
                array_push(_spotted, _eu.unit_label);
            }
        }
    }
    
    return _spotted;
}
