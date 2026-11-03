import re

# 1. Update scr_territory_war_system.gml: set is_major_stronghold: true on all Earth bases + mars_olympus_caldera
path_sys = 'scripts/scr_territory_war_system/scr_territory_war_system.gml'
with open(path_sys, 'r') as f:
    text = f.read()

# Replace all is_major_stronghold: false with is_major_stronghold: true on Earth bases
earth_ids = [
    "earth_cascadia_driver",
    "earth_sahara_array",
    "earth_andes_battery",
    "earth_gibraltar_redoubt",
    "earth_outback_proving",
    "earth_shanghai_arcology",
    "earth_nordic_vault",
    "earth_ural_arsenal",
    "earth_antarctic_facility"
]

for eid in earth_ids:
    pattern = rf'(id:\s*"{eid}".*?is_major_stronghold:\s*)false'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        text = text[:match.start(1)] + match.group(1) + "true" + text[match.end():]
        print(f"Set is_major_stronghold: true on {eid}")
    else:
        print(f"Warning: pattern not matched for {eid}")

# Add is_major_stronghold: true to mars_olympus_caldera if missing
if 'id: "mars_olympus_caldera"' in text and 'is_major_stronghold' not in text[text.find('id: "mars_olympus_caldera"'):text.find('id: "mars_olympus_caldera"')+400]:
    old_oly = 'map_x: 290, map_y: 130,'
    new_oly = 'map_x: 290, map_y: 130, is_major_stronghold: true,'
    text = text.replace(old_oly, new_oly, 1)
    print("Set is_major_stronghold: true on mars_olympus_caldera")

# 2. Replace scr_stronghold_get_layout with the comprehensive 11-stronghold system
layout_func_start = '/// @function scr_stronghold_get_layout(_stronghold_id)'
layout_func_end_target = '/// @function scr_stronghold_get_subnode(_stronghold_id, _subnode_id)'

pos_start = text.find(layout_func_start)
pos_end = text.find(layout_func_end_target, pos_start)

assert pos_start != -1 and pos_end != -1, "Stronghold layout function anchors not found"

comprehensive_layout_code = '''/// @function scr_stronghold_get_layout(_stronghold_id)
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

'''

text = text[:pos_start] + comprehensive_layout_code + text[pos_end:]

with open(path_sys, 'w') as f:
    f.write(text)

print("Updated scr_territory_war_system.gml with 11 complete stronghold layouts!")
