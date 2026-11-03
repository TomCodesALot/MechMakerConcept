import re

with open('scripts/scr_territory_war_system/scr_territory_war_system.gml', 'r') as f:
    text = f.read()

earth_coords = {
    "earth_granite_redoubt": (420, 470),
    "earth_cascadia_driver": (210, 240),
    "earth_sahara_array": (700, 340),
    "earth_andes_battery": (360, 430),
    "earth_gibraltar_redoubt": (650, 265),
    "earth_outback_proving": (1130, 520),
    "earth_shanghai_arcology": (1040, 300),
    "earth_nordic_vault": (680, 185),
    "earth_ural_arsenal": (870, 190),
    "earth_antarctic_facility": (700, 680)
}

if 'global_map_x' not in text:
    for tid, (gx, gy) in earth_coords.items():
        pattern = r'(_db\.' + tid + r'\s*=\s*\{[^}]+map_y:\s*\d+)'
        replacement = r'\1, global_map_x: ' + str(gx) + ', global_map_y: ' + str(gy)
        text = re.sub(pattern, replacement, text)
    print("Updated global_map_x and global_map_y for Earth territories.")
else:
    print("global_map_x already present.")

stronghold_code = '''
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
        minimap_box: { x: 47, y: 53, w: 42, h: 40 },
        subnodes: []
    };
    
    if (_stronghold_id == "earth_granite_redoubt") {
        _layout.stronghold_name = "Granite Deep Command (South America Stronghold)";
        _layout.map_sprite_name = "spr_map_earth_theater";
        _layout.minimap_box = { x: 47, y: 53, w: 42, h: 40 };
        
        _layout.subnodes = [
            {
                id: "granite_core",
                name: "Subterranean Command Redoubt",
                desc: "Excavated three thousand meters beneath ancient granite. Central HQ and reactor core.",
                sub_type: "CORE_BUNKER",
                map_x: 390, map_y: 280,
                controlling_faction: "faction_a",
                defense_rating: 95,
                unit_sprite_name: "spr_mini_ms_commander",
                stack_count: 4,
                unit_label: "Command Division",
                connected_ids: ["granite_north_gate", "granite_andes_battery", "granite_missile_silos"],
                is_core: true
            },
            {
                id: "granite_north_gate",
                name: "Amazon River Delta Flank Sentry",
                desc: "River crossing bridgehead and armored checkpoint interdicting river gunboats.",
                sub_type: "RIVER_GATE",
                map_x: 320, map_y: 180,
                controlling_faction: "faction_a",
                defense_rating: 75,
                unit_sprite_name: "spr_mini_veh_heavy_tank",
                stack_count: 6,
                unit_label: "Amazon Armor Cohort",
                connected_ids: ["granite_core", "granite_caribbean_dock"],
                is_core: false
            },
            {
                id: "granite_andes_battery",
                name: "Chimborazo Andean Rail Redoubt",
                desc: "High-altitude kinetic gun battery perched along the equatorial mountain spine.",
                sub_type: "MOUNTAIN_BATTERY",
                map_x: 210, map_y: 220,
                controlling_faction: "faction_b",
                defense_rating: 82,
                unit_sprite_name: "spr_mini_ms_artillery",
                stack_count: 4,
                unit_label: "Andes Artillery MS",
                connected_ids: ["granite_core", "granite_pacific_coast"],
                is_core: false
            },
            {
                id: "granite_caribbean_dock",
                name: "Caribbean Sea-Gate Anchorage",
                desc: "Deep-water gantry slips and coastal anti-air missile bunkers.",
                sub_type: "AIR_NAVAL_GATE",
                map_x: 170, map_y: 90,
                controlling_faction: "faction_b",
                defense_rating: 70,
                unit_sprite_name: "spr_mini_veh_gunship",
                stack_count: 6,
                unit_label: "Caribbean Drop Wing",
                connected_ids: ["granite_north_gate"],
                is_core: false
            },
            {
                id: "granite_missile_silos",
                name: "Mato Grosso Anti-Orbital Silos",
                desc: "Concealed surface-to-orbit missile batteries disguised beneath rainforest canopy.",
                sub_type: "MISSILE_SILO",
                map_x: 480, map_y: 350,
                controlling_faction: "faction_a",
                defense_rating: 78,
                unit_sprite_name: "spr_mini_inf_exo_squad",
                stack_count: 8,
                unit_label: "Rainforest Exo-Troopers",
                connected_ids: ["granite_core"],
                is_core: false
            },
            {
                id: "granite_pacific_coast",
                name: "Pacific Shoreline Forward Depot",
                desc: "Logistical staging depot and coastal hovercraft slipways.",
                sub_type: "PERIMETER_DEPOT",
                map_x: 150, map_y: 340,
                controlling_faction: "faction_c",
                defense_rating: 68,
                unit_sprite_name: "spr_mini_veh_technical",
                stack_count: 6,
                unit_label: "Pacific Shore Techs",
                connected_ids: ["granite_andes_battery"],
                is_core: false
            }
        ];
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
'''

if 'scr_stronghold_get_layout' not in text:
    text += stronghold_code
    print("Appended scr_stronghold_get_layout and scr_stronghold_get_subnode.")

with open('scripts/scr_territory_war_system/scr_territory_war_system.gml', 'w') as f:
    f.write(text)

print("Saved updated scr_territory_war_system.gml successfully.")
