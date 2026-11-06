/// @description Central Mobile Suit Database & Authoritative Animation Registry
// Single Source of Truth for all Mobile Suits, Custom Sockets, Conventional Vehicles & Infantry.
// Provides deterministic catalog ordering, unified sprite resolution, and combat weapon choreography.

/// @function scr_ms_db_get_roster()
/// @description Returns the canonical, deterministic master roster array of all 44 units.
function scr_ms_db_get_roster() {
    static _master_roster = undefined;
    if (!is_undefined(_master_roster)) return _master_roster;

    var _list = [];

    var _add = method({ roster: _list }, function(_id, _name, _fac, _cat, _chassis, _alloy, _spr_idle, _spr_back, _weapon, _w_class, _hp, _armor, _era = 2, _doc = "", _wpn_prim = "", _wpn_sec = "", _spr_boost = -1, _spr_melee = -1, _spr_fire = -1, _spr_dest = -1, _spr_dmg = -1) {
        var _spr_map = {
            idle: _spr_idle,
            back_idle: (_spr_back != -1) ? _spr_back : _spr_idle,
            boost: (_spr_boost != -1) ? _spr_boost : _spr_idle,
            melee: (_spr_melee != -1) ? _spr_melee : _spr_idle,
            fire: (_spr_fire != -1) ? _spr_fire : _spr_idle,
            destroyed: (_spr_dest != -1) ? _spr_dest : -1,
            damaged: (_spr_dmg != -1) ? _spr_dmg : -1
        };

        array_push(roster, {
            id: _id,
            name: _name,
            faction_id: _fac,
            category: _cat,
            chassis: _chassis,
            alloy: _alloy,
            sprite_asset: _spr_idle,
            sprite_back_asset: (_spr_back != -1) ? _spr_back : _spr_idle,
            sprites: _spr_map,
            weapon_name: _weapon,
            weapon_class: _w_class,
            hp: _hp,
            armor: _armor,
            era: _era,
            doctrine: _doc,
            weapon_overlay_primary: _wpn_prim,
            weapon_overlay_secondary: _wpn_sec
        });
    });

    // =========================================================================
    // 1. TERRAN CONFEDERATION (faction_a) - 6 CANONICAL MOBILE SUITS
    // =========================================================================
    _add("ms_terran_ironclad_07", "GHA-07 Ironclad", "faction_a", "MOBILE_SUIT", "biped", "alloy_vanguard_comp",
         spr_ms_ironclad_idle, spr_ms_ironclad_back_idle, "Type-77 120mm Solid Kinetic Cannon", "BALLISTIC", 680, 32, 2, "Earth Defense Heavy Battleline", "", "Cybernetic Demolition Mace & Scutum Shield", spr_ms_ironclad_boost, spr_ms_ironclad_attack_melee, spr_ms_ironclad_fire_rifle, spr_ms_ironclad_destroyed, spr_ms_ironclad_idle_damaged);

    _add("ms_terran_centurion_02", "TH-C02 Centurion", "faction_a", "MOBILE_SUIT", "biped", "alloy_adamantine_carbide",
         spr_ms_centurion_idle, spr_ms_centurion_back_idle, "Twin-Linked 35mm Heavy Chain Vulcan", "ROTARY_VULCAN", 650, 30, 2, "Shock Assault & Frontal Breach", "", "High-Frequency Thermal Gladius & Tower Shield", spr_ms_centurion_boost, spr_ms_centurion_attack_melee, spr_ms_centurion_fire_chaingun, spr_ms_centurion_destroyed, spr_ms_centurion_idle_damaged);

    _add("ms_terran_ballista_04", "TH-M04 Ballista", "faction_a", "MOBILE_SUIT", "tread", "alloy_vanguard_comp",
         spr_ms_ballista_idle, spr_ms_ballista_back_idle, "Dual 180mm Long-Range Recoil Howitzers", "BALLISTIC", 620, 28, 2, "Saturated Over-the-Horizon Bombardment", "", "Twin 40mm Bofors & Ground Anchor Spades");

    _add("ms_terran_trenchcoat_09", "TH-T09 Trenchcoat", "faction_a", "MOBILE_SUIT", "biped", "alloy_vanguard_comp",
         spr_ms_trenchcoat_idle, spr_ms_trenchcoat_back_idle, "Type-9 12-Gauge Solid Combat Shotgun", "BALLISTIC", 600, 26, 2, "Close-Quarters Domed City Brawler", "", "Pneumatic Breaching Mattock & Mantlet");

    _add("ms_terran_siegebreaker_01", "TH-S01 Siegebreaker", "faction_a", "MOBILE_SUIT", "tread", "alloy_adamantine_carbide",
         spr_ms_siegebreaker_anchor, spr_ms_siegebreaker_anchor, "Twin 280mm Heavy Siege Cannons", "BALLISTIC", 1150, 65, 3, "Planetary Bombardment & Anti-Warship", "", "Coaxial 30mm Vulcan & Hydraulic Bulldozer Prow", -1, -1, spr_ms_siegebreaker_fire);

    _add("ms_terran_titan_04", "TH-X04 Titan Prime", "faction_a", "MOBILE_SUIT", "biped", "alloy_adamantine_carbide",
         spr_ms_titan_proto, spr_ms_titan_proto_back_idle, "320mm Hyper-Kinetic Shoulder Railcannon", "BALLISTIC", 980, 55, 3, "Super-Heavy Pre-War Dreadnought Prototype", "", "Thermal Breaker Maul & Fortress Barrier");

    // =========================================================================
    // 3. OUTER COLONY LEAGUE (faction_b) - 6 CANONICAL MOBILE SUITS
    // =========================================================================
    _add("ms_colony_aether_01", "OC-A01 Aether Striker", "faction_b", "MOBILE_SUIT", "aero", "alloy_aerosteel_flux",
         spr_ms_aether_idle, spr_ms_aether_back_idle, "Type-6A High-Output Thermal Beam Rifle", "BEAM_PULSE", 580, 22, 2, "High-Mobility Space Vernier Skirmisher", "", "High-Energy Thermal Plasma Saber & Deflector", spr_ms_aether_boost, spr_ms_aether_attack_saber, spr_ms_aether_fire_beam);

    _add("ms_colony_kepler_02", "OC-K02 Kepler", "faction_b", "MOBILE_SUIT", "hover", "alloy_hyperion_matrix",
         spr_ms_kepler_idle, spr_ms_kepler_back_idle, "Linear Coherent Particle Sniper Rifle", "BEAM_PULSE", 520, 18, 2, "Extreme Range Precision Rail-Sniper", "", "Rapid Beam Pistol & Monofilament Bayonet");

    _add("ms_colony_sylph_01", "AOD-01 Sylph Interceptor", "faction_b", "MOBILE_SUIT", "aero", "alloy_aerosteel_flux",
         spr_ms_zephyr_idle, spr_ms_zephyr_back_idle, "Focused Pulse Beam Spray Gun", "BEAM_PULSE", 490, 16, 2, "Fleet Interceptor & Sensor Escort", "", "Thermal Beam Dagger & Chaff Disperser");

    _add("ms_colony_oberon_08", "OC-O08 Oberon", "faction_b", "MOBILE_SUIT", "biped", "alloy_aerosteel_flux",
         spr_ms_oberon_idle, spr_ms_oberon_back_idle, "Heavy Dual-Phase Beam Lance", "BEAM_LANCE", 640, 26, 2, "Convoy Escort & Beam Defense", "", "High-Yield Thermal Estoc & Deflector Tower Shield");

    _add("ms_colony_chronos_01", "OC-X04 Chronos Sovereign", "faction_b", "MOBILE_SUIT", "aero", "alloy_tachyon_superalloy",
         spr_ms_chronos_idle, spr_ms_chronos_back_idle, "Heavy Tachyon Beam Burst Cannon", "BEAM_LANCE", 820, 36, 4, "Flagship Vanguard Sovereign", "", "Twin Heavy Tachyon Beam Claymores & Halos");

    _add("ms_colony_cassian_custom", "Aether Commander (Cassian Custom)", "faction_b", "MOBILE_SUIT", "aero", "alloy_aerosteel_flux",
         spr_ms_cassian_custom_idle, spr_ms_cassian_custom_back_idle, "Custom Accelerated Long-Beam Carbine", "BEAM_PULSE", 740, 28, 3, "Colony Ace Custom Interceptor", "", "Twin Overclocked Thermal Plasma Sabers");

    // =========================================================================
    // 4. RUST SYNDICATE (faction_c) - 6 CANONICAL MOBILE SUITS
    // =========================================================================
    _add("ms_syndicate_hyena_12", "RS-H12 Hyena", "faction_c", "MOBILE_SUIT", "biped", "alloy_adamantine_carbide",
         spr_ms_hyena_idle, spr_ms_hyena_back_idle, "Salvaged 90mm Assault Machine Gun", "BALLISTIC", 590, 24, 2, "Guerilla Ambush & Scrap Salvo", "", "Serrated Manganese Heat Chopper & Flak Autocannon");

    _add("ms_syndicate_gorgon_04", "RS-G04 Gorgon", "faction_c", "MOBILE_SUIT", "biped", "alloy_adamantine_carbide",
         spr_ms_gorgon_idle, spr_ms_gorgon_back_idle, "Forearm Armor-Piercing Spike Launcher", "BALLISTIC", 720, 38, 2, "Armor-Crushing Point Blank Breacher", "", "Heavy Hydraulic Crush Vices & Steam Nozzles");

    _add("ms_syndicate_bloodhound_06", "RS-B06 Bloodhound", "faction_c", "MOBILE_SUIT", "tread", "alloy_adamantine_carbide",
         spr_ms_bloodhound_idle, spr_ms_bloodhound_back_idle, "Magnetic Harpoon Winch Cannon", "MICRO_MISSILE", 540, 20, 2, "Low-Profile Ambush Hound", "", "Manganese Heavy Breaching Claw & Slag Mortar");

    _add("ms_syndicate_scrapper_01", "RS-V03 Vandal Scrapper", "faction_c", "MOBILE_SUIT", "biped", "alloy_adamantine_carbide",
         spr_ms_vandal_idle, spr_ms_vandal_back_idle, "105mm Drum-Fed Scrap Flechette Gun", "ROTARY_VULCAN", 560, 22, 2, "Perimeter Raider & Boarding Shock", "", "Pneumatic High-Torque Rock-Breaker Saw & Mantlet");

    _add("ms_syndicate_marauder_02", "RS-M02 Marauder Brawler", "faction_c", "MOBILE_SUIT", "biped", "alloy_adamantine_carbide",
         spr_ms_marauder_idle, spr_ms_marauder_back_idle, "Torso Molten Slag Lobber Mortar", "BALLISTIC", 710, 36, 3, "Close-In Heavy Scrap Grappler", "", "Twin Hydraulic Demolition Pincers & Rocket Rack");

    _add("ms_syndicate_iron_reaver_09", "RS-R09 Iron Reaver", "faction_c", "MOBILE_SUIT", "tread", "alloy_adamantine_carbide",
         spr_ms_iron_reaver_idle, spr_ms_iron_reaver_back_idle, "Salvaged 210mm Warship Broadside Cannon", "BALLISTIC", 850, 48, 3, "Frontline Fortress Buster", "", "Spiked Battering Ram Shield & Heavy Manganese Cleaver");

    // =========================================================================
    // 5. APEX ZAIBATSU (faction_d) - 6 CANONICAL MOBILE SUITS
    // =========================================================================
    _add("ms_zaibatsu_kamaitachi_03", "ZX-K03 Kamaitachi", "faction_d", "MOBILE_SUIT", "biped", "alloy_tachyon_superalloy",
         spr_ms_kamaitachi_idle, spr_ms_kamaitachi_back_idle, "Dual Forearm High-Frequency Plasma Lances", "BEAM_LANCE", 860, 38, 3, "Aerodynamic High-Speed Plasma Skirmisher", "", "Dual Curved Scythe Vernier Blades & Micro-Missiles", spr_ms_kamaitachi_boost, spr_ms_kamaitachi_attack_blade, spr_ms_kamaitachi_fire_plasma);

    _add("ms_zaibatsu_ronin_04", "ZX-R04 Ronin Master", "faction_d", "MOBILE_SUIT", "biped", "alloy_tachyon_superalloy",
         spr_ms_ronin_idle, spr_ms_ronin_back_idle, "Shoulder-Mounted High-Output Plasma Cannons", "BALLISTIC", 820, 36, 4, "Apex Master Assassin & Electronic Warfare", "", "Dual Monomolecular Executioner Nodachi");

    _add("ms_zaibatsu_kage_07", "ZX-K07 Kage", "faction_d", "MOBILE_SUIT", "biped", "alloy_tachyon_superalloy",
         spr_ms_kage_idle, spr_ms_kage_back_idle, "Silenced 40mm Pneumatic Needle Dart Pistol", "BALLISTIC", 510, 18, 2, "Carbon-Weave Electronic Infiltrator", "", "Monomolecular High-Frequency Vibro-Tanto & Decoys");

    _add("ms_zaibatsu_tessen_09", "ZX-T09 Tessen", "faction_d", "MOBILE_SUIT", "biped", "alloy_tachyon_superalloy",
         spr_ms_tessen_idle, spr_ms_tessen_back_idle, "Arm-Mounted EMP Disruptor Emitter", "BEAM_PULSE", 620, 24, 2, "Disruptive Close-Range Counter-Unit", "", "Razor-Edged Monofilament War-Fan [Tessen]");

    _add("ms_zaibatsu_muramasa_03", "ZX-M03 Muramasa", "faction_d", "MOBILE_SUIT", "biped", "alloy_tachyon_superalloy",
         spr_ms_muramasa_idle, spr_ms_muramasa_back_idle, "Wrist-Mounted High-Cycle Plasma Needle Gun", "BEAM_PULSE", 670, 28, 3, "Precision Cybernetic Duelist", "", "Masterwork Monomolecular Tachyon Katana");

    _add("ms_zaibatsu_takahashi_custom", "Muramasa Shadow (Takahashi Custom)", "faction_d", "MOBILE_SUIT", "biped", "alloy_tachyon_superalloy",
         spr_ms_takahashi_custom_idle, spr_ms_takahashi_custom_back_idle, "High-Output Magnetic Needle Rifle", "BEAM_PULSE", 880, 40, 4, "Executive Assassin Custom", "", "Twin Monomolecular Tachyon Daisho & Sashimono");

    // =========================================================================
    // 5. PMC VANGUARD - 4 MODULAR CUSTOM SOCKET CHASSIS (Suits 25-28)
    // =========================================================================
    _add("custom_biped", "PMC Vanguard Heavy (Modular Socket)", "pmc_player", "CUSTOM_MECH", "biped", "alloy_vanguard_comp",
         spr_ms_custom_biped_heavy_idle, spr_ms_custom_biped_heavy_back_idle, "GAU-88 Rotary Heavy Vulcan", "ROTARY_VULCAN", 680, 32, 2, "Modular Heavy Biped", "spr_wpn_tc_cannon_150mm", "spr_wpn_tc_tower_shield");

    _add("custom_hover", "PMC Ghost Hover Sniper (Modular Socket)", "pmc_player", "CUSTOM_MECH", "hover", "alloy_hyperion_matrix",
         spr_ms_custom_hover_sniper_idle, spr_ms_custom_hover_sniper_back_idle, "Coherent Beam Pulse Rifle", "BEAM_PULSE", 480, 20, 2, "High-Mobility Hover Sniper", "spr_wpn_ocl_beam_spray", "spr_wpn_ocl_deflector_wing");

    _add("custom_tread", "PMC Scrapper Tread Artillery (Modular Socket)", "pmc_player", "CUSTOM_MECH", "tread", "alloy_adamantine_carbide",
         spr_ms_custom_tread_artillery_idle, spr_ms_custom_tread_artillery_back_idle, "Type-77 120mm Heavy Cannon", "BALLISTIC", 750, 40, 2, "Siege Tread Fortress", "spr_wpn_rsc_rock_saw", "spr_wpn_rsc_harpoon_winch");

    _add("custom_aero", "PMC Stratos Aero Striker (Modular Socket)", "pmc_player", "CUSTOM_MECH", "aero", "alloy_aerosteel_flux",
         spr_ms_custom_aero_striker_idle, spr_ms_custom_aero_striker_back_idle, "Ares Swarm-16 Missiles", "MICRO_MISSILE", 450, 22, 2, "High-Speed Atmospheric Striker", "spr_wpn_ocl_beam_lance", "spr_wpn_tc_tower_shield");

    // =========================================================================
    // 6. CONVENTIONAL VEHICLES (12 Units: 4 Factions x 3 Archetypes)
    // =========================================================================
    _add("veh_terran_mammoth", "T-720 Mammoth Heavy Battle Tank", "faction_a", "VEHICLE", "tread", "alloy_vanguard_comp",
         spr_veh_terran_mammoth_idle, spr_veh_terran_mammoth_back_idle, "Dual 150mm Siege Cannons", "BALLISTIC", 520, 35, 1, "Heavy Armored Linebreaker", "", "", -1, -1, spr_veh_terran_mammoth_fire);

    _add("veh_terran_skyhammer", "UH-44 Skyhammer Heavy Gunship", "faction_a", "VEHICLE", "aero", "alloy_vanguard_comp",
         spr_veh_terran_skyhammer_idle, spr_veh_terran_skyhammer_back_idle, "GAU-88 30mm Rotary Vulcan", "ROTARY_VULCAN", 380, 18, 1, "Close Air Support Gunship", "", "", -1, -1, spr_veh_terran_skyhammer_fire);

    _add("veh_terran_sabre", "A-14 Sabre Heavy Strike Jet", "faction_a", "VEHICLE", "aero", "alloy_vanguard_comp",
         spr_veh_terran_sabre_idle, spr_veh_terran_sabre_back_idle, "AGM-88 Swarm Strike Missiles", "MICRO_MISSILE", 340, 16, 1, "Air Superiority Fighter", "", "", -1, -1, spr_veh_terran_sabre_fire);

    _add("veh_colony_stiletto", "K-4 Stiletto Rapid Attack Skimmer", "faction_b", "VEHICLE", "hover", "alloy_aerosteel_flux",
         spr_veh_colony_stiletto_idle, spr_veh_colony_stiletto_back_idle, "Coherent Beam Carbine", "BEAM_PULSE", 310, 15, 1, "Energy Skirmisher", "", "", -1, -1, spr_veh_colony_stiletto_fire);

    _add("veh_colony_gunship", "V-88 Valkyrie Heavy Tilt-Rotor", "faction_b", "VEHICLE", "aero", "alloy_aerosteel_flux",
         spr_veh_colony_gunship_idle, spr_veh_colony_gunship_back_idle, "Thermal Beam Cannon", "BEAM_PULSE", 380, 20, 1, "Aerospace Attack Gunship", "", "", -1, -1, spr_veh_colony_gunship_fire);

    _add("veh_colony_dart", "S-10 Dart Hypersonic Interceptor", "faction_b", "VEHICLE", "aero", "alloy_aerosteel_flux",
         spr_veh_colony_dart_idle, spr_veh_colony_dart_back_idle, "Micro-Missile Salvo", "MICRO_MISSILE", 290, 14, 1, "Hypersonic Interceptor", "", "", -1, -1, spr_veh_colony_dart_fire);

    _add("veh_syndicate_technical", "SCR-T01 Rustfang Flak Technical", "faction_c", "VEHICLE", "wheeled", "alloy_adamantine_carbide",
         spr_veh_syndicate_technical_idle, spr_veh_syndicate_technical_back_idle, "Heavy Twin Flak Cannon", "ROTARY_VULCAN", 300, 14, 1, "Flak Support Technical", "", "", -1, -1, spr_veh_syndicate_technical_fire);

    _add("veh_syndicate_chopper", "H-09 Buzzsaw Scrap Chopper", "faction_c", "VEHICLE", "aero", "alloy_adamantine_carbide",
         spr_veh_syndicate_chopper_idle, spr_veh_syndicate_chopper_back_idle, "Twin 23mm Rotary Autocannon", "ROTARY_VULCAN", 320, 14, 1, "Raid Scrap Chopper", "", "", -1, -1, spr_veh_syndicate_chopper_fire);

    _add("veh_syndicate_bomber", "SCR-B03 Buzzard Light Bomber", "faction_c", "VEHICLE", "aero", "alloy_adamantine_carbide",
         spr_veh_syndicate_bomber_idle, spr_veh_syndicate_bomber_back_idle, "Incendiary Slag Cluster", "BALLISTIC", 300, 16, 1, "Tactical Slag Bomber", "", "", -1, -1, spr_veh_syndicate_bomber_fire);

    _add("veh_zaibatsu_kurogane", "Type-94 Kurogane Drone Tank", "faction_d", "VEHICLE", "hover", "alloy_tachyon_superalloy",
         spr_veh_zaibatsu_kurogane_idle, spr_veh_zaibatsu_kurogane_back_idle, "Railgun Point Defense", "BEAM_PULSE", 580, 28, 1, "Automated Point Defense Tank", "", "", -1, -1, spr_veh_zaibatsu_kurogane_fire);

    _add("veh_zaibatsu_rotor", "Type-07 Shinobi Ducted VTOL", "faction_d", "VEHICLE", "aero", "alloy_tachyon_superalloy",
         spr_veh_zaibatsu_rotor_idle, spr_veh_zaibatsu_rotor_back_idle, "Twin Pulse Laser Emitters", "BEAM_PULSE", 350, 18, 1, "Stealth Infiltration VTOL", "", "", -1, -1, spr_veh_zaibatsu_rotor_fire);

    _add("veh_zaibatsu_drone_jet", "Type-02 Kamaitachi Stealth Drone", "faction_d", "VEHICLE", "aero", "alloy_tachyon_superalloy",
         spr_veh_zaibatsu_drone_jet_idle, spr_veh_zaibatsu_drone_jet_back_idle, "Plasma Beam Emitter", "BEAM_PULSE", 270, 14, 1, "Stealth Strike Drone", "", "", -1, -1, spr_veh_zaibatsu_drone_jet_fire);

    // =========================================================================
    // 7. CONVENTIONAL INFANTRY SQUADS (4 Units: 4 Factions x 1 Squad)
    // =========================================================================
    _add("inf_terran_squad", "Terran 88th Grenadier Platoon", "faction_a", "INFANTRY", "infantry", "alloy_vanguard_comp",
         spr_inf_terran_squad_idle, spr_inf_terran_squad_back_idle, "Anti-Armor Rocket Volley", "MICRO_MISSILE", 180, 8, 1, "Urban Grenadiers", "", "", -1, -1, spr_inf_terran_squad_fire);

    _add("inf_colony_squad", "Colony Void Jump Skirmishers", "faction_b", "INFANTRY", "infantry", "alloy_aerosteel_flux",
         spr_inf_colony_squad_idle, spr_inf_colony_squad_back_idle, "Plasma Rifle Saturation", "BEAM_PULSE", 150, 6, 1, "Void Skirmishers", "", "", -1, -1, spr_inf_colony_squad_fire);

    _add("inf_syndicate_squad", "Rust Syndicate Marauder Squad", "faction_c", "INFANTRY", "infantry", "alloy_adamantine_carbide",
         spr_inf_syndicate_squad_idle, spr_inf_syndicate_squad_back_idle, "Magnetic Harpoon & Charges", "MELEE", 160, 7, 1, "Scrap Marauders", "", "", -1, -1, spr_inf_syndicate_squad_fire);

    _add("inf_zaibatsu_squad", "Zaibatsu Spec-Ops Androids", "faction_d", "INFANTRY", "infantry", "alloy_tachyon_superalloy",
         spr_inf_zaibatsu_squad_idle, spr_inf_zaibatsu_squad_back_idle, "Monoblades & Flechettes", "MELEE", 170, 10, 1, "Cybernetic Spec-Ops", "", "", -1, -1, spr_inf_zaibatsu_squad_fire);

    _master_roster = _list;
    return _master_roster;
}

/// @function scr_ms_db_get_unit(_unit_id)
/// @description Fast lookup of any unit in the canonical database.
function scr_ms_db_get_unit(_unit_id) {
    var _roster = scr_ms_db_get_roster();
    for (var i = 0; i < array_length(_roster); i++) {
        if (_roster[i].id == _unit_id) return _roster[i];
    }
    return undefined;
}

/// @function scr_ms_db_get_unit_sprite(_unit_or_id, _state, _perspective)
/// @description Single authoritative sprite resolver for EVERY unit, animation state, and perspective.
function scr_ms_db_get_unit_sprite(_unit_or_id, _state = "idle", _perspective = "front") {
    var _u = undefined;
    if (is_struct(_unit_or_id)) {
        if (variable_struct_exists(_unit_or_id, "sprites")) {
            _u = _unit_or_id;
        } else {
            var _uid = variable_struct_get(_unit_or_id, "id") ?? "";
            _u = scr_ms_db_get_unit(_uid);
        }
    } else if (is_string(_unit_or_id)) {
        _u = scr_ms_db_get_unit(_unit_or_id);
    }

    if (!is_undefined(_u) && is_struct(_u) && variable_struct_exists(_u, "sprites")) {
        var _is_back = (_perspective == "back" || _perspective == "rear");
        if (_is_back && _state == "idle") {
            return _u.sprites.back_idle;
        }

        // Action States
        if (_state == "boost" || _state == "sprint" || _state == "walk") {
            return _u.sprites.boost;
        }
        if (_state == "melee" || _state == "attack") {
            return _u.sprites.melee;
        }
        if (string_pos("fire", _state) > 0) {
            return _u.sprites.fire;
        }
        if (_state == "damaged" || _state == "hit") {
            if (variable_struct_exists(_u.sprites, "damaged") && _u.sprites.damaged != -1) return _u.sprites.damaged;
            return _u.sprites.idle;
        }
        if (_state == "destroyed" || _state == "defeat") {
            if (variable_struct_exists(_u.sprites, "destroyed") && _u.sprites.destroyed != -1) return _u.sprites.destroyed;
            return _u.sprites.idle;
        }

        return _is_back ? _u.sprites.back_idle : _u.sprites.idle;
    }

    return -1;
}
