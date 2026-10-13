#!/usr/bin/env python3
import os
import json

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datafiles', 'blueprints')
os.makedirs(OUT_DIR, exist_ok=True)

def make_suit_data(
    bp_id, name, model_code, faction_id, s_class, role, tier, mfr, desc,
    frame_type, empty_mass, max_cap, base_armor, base_struct, walk_spd, boost_spd, dissip_rate,
    head, torso, arm_l, arm_r, legs, backpack,
    prod_cost, prod_days, sortie_cost, alloys, affinities, lore_hist
):
    h_id, h_name, h_hp, h_range, h_lock, h_drain, h_wt = head
    t_id, t_name, t_hp, t_struct, t_rtype, t_out, t_drain, t_cool, t_wt = torso
    al_id, al_name, al_hp, al_cap, wl_id, wl_name, wl_type, wl_dmg, wl_rpm, wl_range, wl_ammo_type, wl_ammo, wl_heat, wl_drain, wl_wt = arm_l
    ar_id, ar_name, ar_hp, ar_cap, wr_id, wr_name, wr_type, wr_dmg, wr_rpm, wr_range, wr_ammo_type, wr_ammo, wr_heat, wr_drain, wr_wt = arm_r
    lg_id, lg_name, lg_hp, lg_struct, lg_wt, lg_cap, lg_turn, lg_drain, lg_recoil = legs
    bp_id_c, bp_name, bp_hp, bp_wt, bp_drain, bp_thrust, aux_id, aux_name, aux_type, aux_salvo, aux_total, aux_dmg, aux_range, aux_heat = backpack

    tot_wt = h_wt + t_wt + lg_wt + bp_wt + wl_wt + wr_wt
    tot_drain = h_drain + t_drain + lg_drain + bp_drain + wl_drain + wr_drain
    net_surplus = t_out - tot_drain
    tot_armor = h_hp + t_hp + al_hp + ar_hp + lg_hp + bp_hp
    tot_struct = base_struct + t_struct + lg_struct

    assert net_surplus >= 0, f'{bp_id} reactor overload: {net_surplus} MW'
    assert tot_wt <= lg_cap, f'{bp_id} overweight: {tot_wt} > {lg_cap}'

    suit = {
        'blueprint_id': bp_id,
        'name': name,
        'model_code': model_code,
        'faction_id': faction_id,
        'class': s_class,
        'role': role,
        'tier': tier,
        'manufacturer': mfr,
        'description': desc,
        'chassis': {
            'frame_type': frame_type,
            'empty_mass_tonnes': empty_mass,
            'max_weight_capacity_tonnes': max_cap,
            'base_armor_rating': base_armor,
            'base_structure_hp': base_struct,
            'base_walk_speed_kph': walk_spd,
            'base_boost_speed_kph': boost_spd,
            'heat_dissipation_rate': dissip_rate
        },
        'components': {
            'head': {
                'id': h_id, 'name': h_name, 'armor_hp': h_hp,
                'sensor_range_m': h_range, 'lock_on_speed_sec': h_lock,
                'power_drain_mw': h_drain, 'weight_tonnes': h_wt
            },
            'torso': {
                'id': t_id, 'name': t_name, 'armor_hp': t_hp, 'structure_hp': t_struct,
                'reactor_type': t_rtype, 'reactor_output_mw': t_out,
                'power_drain_mw': t_drain, 'internal_cooling_units': t_cool,
                'weight_tonnes': t_wt
            },
            'arm_left': {
                'id': al_id, 'name': al_name, 'armor_hp': al_hp, 'load_capacity_tonnes': al_cap,
                'equipped_weapon': {
                    'id': wl_id, 'name': wl_name, 'type': wl_type, 'damage_per_shot': wl_dmg,
                    'rate_of_fire_rpm': wl_rpm, 'effective_range_m': wl_range,
                    'ammo_type': wl_ammo_type, 'ammo_loaded': wl_ammo, 'ammo_max': wl_ammo,
                    'heat_per_shot': wl_heat, 'power_drain_mw': wl_drain, 'weight_tonnes': wl_wt
                }
            },
            'arm_right': {
                'id': ar_id, 'name': ar_name, 'armor_hp': ar_hp, 'load_capacity_tonnes': ar_cap,
                'equipped_weapon': {
                    'id': wr_id, 'name': wr_name, 'type': wr_type, 'damage_per_shot': wr_dmg,
                    'rate_of_fire_rpm': wr_rpm, 'effective_range_m': wr_range,
                    'ammo_type': wr_ammo_type, 'ammo_loaded': wr_ammo, 'ammo_max': wr_ammo,
                    'heat_per_shot': wr_heat, 'power_drain_mw': wr_drain, 'weight_tonnes': wr_wt
                }
            },
            'legs': {
                'id': lg_id, 'name': lg_name, 'armor_hp': lg_hp, 'structure_hp': lg_struct,
                'weight_tonnes': lg_wt, 'load_capacity_tonnes': lg_cap,
                'turn_rate_deg_per_sec': lg_turn, 'power_drain_mw': lg_drain,
                'recoil_absorption_pct': lg_recoil
            },
            'backpack': {
                'id': bp_id_c, 'name': bp_name, 'armor_hp': bp_hp, 'weight_tonnes': bp_wt,
                'power_drain_mw': bp_drain, 'booster_thrust_kn': bp_thrust,
                'equipped_auxiliary': {
                    'id': aux_id, 'name': aux_name, 'type': aux_type,
                    'salvo_size': aux_salvo, 'total_salvos': aux_total,
                    'damage_per_missile': aux_dmg, 'lock_range_m': aux_range,
                    'heat_per_salvo': aux_heat
                }
            }
        },
        'totals_and_specs': {
            'total_weight_tonnes': round(tot_wt, 2),
            'max_weight_tonnes': round(lg_cap, 2),
            'total_power_drain_mw': round(tot_drain, 2),
            'total_power_output_mw': round(t_out, 2),
            'net_power_surplus_mw': round(net_surplus, 2),
            'total_armor_hp': tot_armor,
            'total_structure_hp': tot_struct,
            'recoil_absorption_pct': lg_recoil
        },
        'production': {
            'base_fabrication_cost': prod_cost,
            'fabrication_time_days': prod_days,
            'maintenance_cost_per_sortie': sortie_cost,
            'required_tech_tier': tier,
            'required_materials': alloys
        },
        'damage_affinities': affinities,
        'lore_dossier': {
            'designation': f'{model_code} {name}',
            'manufacturer': mfr,
            'historical_origin': lore_hist
        }
    }
    return suit

SUITS = []

# 1. TERRAN COALITION
SUITS.append(make_suit_data(
    'bp_ms_ironclad_07', 'GHA-07 Ironclad [Line Type]', 'GHA-07', 'faction_terran', 'Heavy Assault',
    'Sustained Linebreaker & Heavy Fire Support', 2, 'Vanguard Defense Systems',
    'Standard mainline heavy siege suit of the Terran Coalition.',
    'Heavy Bipedal Reinforced', 58.0, 115.0, 850, 1200, 42.0, 78.0, 35.0,
    ('hd_vanguard_sentry', 'Vanguard Target-Lock Sensor Array', 160, 2400, 0.8, 12.0, 2.5),
    ('cr_hyperion_heavy', 'Hyperion Class-IV Heavy Core', 650, 500, 'Compact Fusion Core', 280.0, 35.0, 4, 24.0),
    ('am_ironclad_left', 'Ironclad Reinforced Left Arm', 400, 18.0, 'wpn_cannon_120mm', 'Type-77 120mm Solid-Slug Autocannon', 'Kinetic Autocannon', 145.0, 180, 950, '120mm APFSDS', 240, 4.2, 8.0, 14.5),
    ('am_ironclad_right', 'Ironclad Reinforced Right Arm', 400, 20.0, 'wpn_rotary_heavy', 'GAU-88 Heavy Vulcan Rotary', 'Rotary Ballistic', 38.0, 1200, 650, '30mm Tungsten Sabot', 1800, 0.9, 15.0, 16.0),
    ('lg_ironclad_colossus', 'Colossus Heavy Bipedal Hydraulic Legs', 650, 450, 26.0, 115.0, 42.0, 22.0, 0.65),
    ('bp_ares_siege', 'Ares Heavy Ordnance Pack', 220, 11.5, 28.0, 420.0, 'wpn_pod_swarm_16', 'Swarm-16 Heavy Micro-Missile Pod', 'Guided Missile Pod', 16, 6, 65.0, 1500, 35.0),
    380000, 12, 16500, {'tungsten': 60, 'silica': 30, 'tritium': 5, 'flux': 10, 'slag': 0},
    {'kinetic': {'damage_reduction_pct': 0.40}, 'energy': {'damage_reduction_pct': 0.20}, 'rocket': {'damage_reduction_pct': 0.35}, 'melee': {'damage_reduction_pct': 0.15}},
    'Engineered during the Jovian Outer Sphere Wars to resolve the Orbital Beachhead Crisis.'
))

SUITS.append(make_suit_data(
    'bp_ms_bulwark_03', 'TCM-03 Bulwark', 'TCM-03', 'faction_terran', 'Entrenched Defender',
    'Entrenched Heavy Defense Grunt', 1, 'Vanguard Defense Systems',
    'Standard mass-produced trench defense suit.',
    'Standard Trench Bipedal', 48.0, 95.0, 680, 980, 34.0, 52.0, 24.0,
    ('hd_bulwark_periscope', 'TCM Trench Periscope & Rangefinder', 140, 1800, 1.1, 8.0, 2.0),
    ('cr_hyperion_type1', 'Hyperion Type-1 Standard Fusion Tokamak', 520, 400, 'Standard Industrial Fusion', 210.0, 25.0, 2, 20.0),
    ('am_bulwark_shield', 'Bulwark Shield Arm & Mantlet', 480, 16.0, 'wpn_shield_mantlet', 'Heavy Cast-Iron Spiked Mantlet Shield', 'Defensive Kinetic Bulwark', 60.0, 60, 100, 'Solid Bash', 999, 1.0, 2.0, 12.0),
    ('am_bulwark_gun', 'Bulwark Reinforced Right Arm', 320, 14.0, 'wpn_cannon_90mm', 'Type-62 90mm Rifled Trench Cannon', 'Kinetic Cannon', 110.0, 120, 800, '90mm Solid AP', 180, 3.0, 6.0, 10.0),
    ('lg_bulwark_strut', 'TCM Trench Reinforced Strut Legs', 520, 380, 22.0, 95.0, 30.0, 16.0, 0.55),
    ('bp_bulwark_logistics', 'TCM Logistics Trench Generator', 180, 8.0, 14.0, 280.0, 'wpn_smoke_discharger', 'Hexa-Smoke Screen Mortar', 'Tactical Screen', 6, 4, 0.0, 400, 8.0),
    220000, 8, 9500, {'tungsten': 50, 'silica': 20, 'tritium': 0, 'flux': 5, 'slag': 5},
    {'kinetic': {'damage_reduction_pct': 0.38}, 'energy': {'damage_reduction_pct': 0.15}, 'rocket': {'damage_reduction_pct': 0.30}, 'melee': {'damage_reduction_pct': 0.20}},
    'First standardized mass-production trench defense workhorse.'
))

SUITS.append(make_suit_data(
    'bp_ms_siegebreaker_07b', 'GHA-07B Ironclad [Siegebreaker]', 'GHA-07B', 'faction_terran', 'Super-Heavy Artillery',
    'Bunker Penetration & Heavy Artillery Support', 3, 'Vanguard Defense Systems',
    'Devastating artillery refit of the Ironclad mounting a 300mm Titan Siege Railgun.',
    'Ultra-Heavy Bipedal Anchored', 68.0, 145.0, 1050, 1550, 32.0, 60.0, 40.0,
    ('hd_siege_telemetry', 'Titan Long-Range Orbital Telemetry Mast', 210, 4200, 1.2, 18.0, 3.5),
    ('cr_hyperion_siege_v', 'Hyperion Class-V High-Output Reactor', 850, 650, 'Supercharged Fusion Tokamak', 350.0, 45.0, 6, 29.0),
    ('am_siege_brace', 'Ironclad Pneumatic Shock Absorber Left Arm', 520, 22.0, 'wpn_shield_anchor', 'Pneumatic Ground Anchor Shield', 'Recoil Countermeasure', 90.0, 30, 150, 'Ground Stake', 999, 2.0, 10.0, 16.0),
    ('am_siege_rail', 'Titan Heavy Linear Cradle Right Arm', 520, 28.0, 'wpn_titan_rail_300mm', '300mm Titan Siege Railgun', 'Heavy Magnetic Accelerator', 420.0, 24, 2200, '300mm DU Sabot', 48, 28.0, 65.0, 24.5),
    ('lg_titan_anchor_legs', 'Titan Hydraulic Anchor Tread-Pads', 800, 580, 32.0, 145.0, 28.0, 28.0, 0.88),
    ('bp_hyper_capacitor_pack', 'Titan Magnetic Capacitor Bank', 280, 14.0, 32.0, 340.0, 'wpn_he_mortar_cluster', 'Spinal 160mm Heavy Mortar', 'Indirect Bombardment', 4, 8, 130.0, 1800, 22.0),
    540000, 18, 26000, {'tungsten': 80, 'silica': 35, 'tritium': 8, 'flux': 15, 'slag': 0},
    {'kinetic': {'damage_reduction_pct': 0.45}, 'energy': {'damage_reduction_pct': 0.22}, 'rocket': {'damage_reduction_pct': 0.38}, 'melee': {'damage_reduction_pct': 0.10}},
    'Pulverizes subterranean redoubts with 300mm kinetic rail penetrators.'
))

SUITS.append(make_suit_data(
    'bp_ms_behemoth_11', 'TCX-11 Behemoth Mk.IV', 'TCX-11', 'faction_terran', 'Super-Dreadnought Platform',
    'Quadrupedal Super-Heavy Railgun Platform', 4, 'Vanguard Defense Systems',
    'Colossal quadruped mobile fortress with twin 400mm Hyper-Rail batteries.',
    'Quadruped Heavy Dreadnought Frame', 95.0, 240.0, 1350, 2400, 26.0, 45.0, 55.0,
    ('hd_behemoth_command_dome', 'Behemoth Armored Command Bridge', 380, 5000, 0.9, 25.0, 5.0),
    ('cr_hyperion_dreadnought_core', 'Hyperion Gigawatt Class-VI Super-Core', 1250, 950, 'Multi-Chamber Fusion Super-Core', 520.0, 75.0, 10, 42.0),
    ('am_behemoth_left_rail', 'Port Heavy Rail Turret Sponson', 720, 36.0, 'wpn_hyper_rail_400mm_l', 'Port 400mm Hyper-Rail Battery', 'Capital-Grade Railgun', 580.0, 18, 3000, '400mm Penetrators', 36, 42.0, 90.0, 32.0),
    ('am_behemoth_right_rail', 'Starboard Heavy Rail Turret Sponson', 720, 36.0, 'wpn_hyper_rail_400mm_r', 'Starboard 400mm Hyper-Rail Battery', 'Capital-Grade Railgun', 580.0, 18, 3000, '400mm Penetrators', 36, 42.0, 90.0, 32.0),
    ('lg_behemoth_quad_pillars', 'Quadruped Reinforced Titan Pillar Legs', 1150, 850, 48.0, 240.0, 22.0, 45.0, 0.95),
    ('bp_behemoth_power_vault', 'Behemoth Secondary Fusion Sponson Pack', 480, 22.0, 40.0, 480.0, 'wpn_ciws_vulcan_turret', 'Twin Point-Defense CIWS Rotary Cannons', 'Anti-Air Kinetic CIWS', 30, 20, 22.0, 900, 12.0),
    890000, 28, 42000, {'tungsten': 120, 'silica': 60, 'tritium': 25, 'flux': 30, 'slag': 0},
    {'kinetic': {'damage_reduction_pct': 0.50}, 'energy': {'damage_reduction_pct': 0.28}, 'rocket': {'damage_reduction_pct': 0.45}, 'melee': {'damage_reduction_pct': 0.20}},
    'Terran Coalitions supreme mobile fortress and theater command bastion.'
))

# 2. COLONY AETHER UNION
SUITS.append(make_suit_data(
    'bp_ms_aether_09', 'OCM-09 Aether Stryker [Standard]', 'OCM-09', 'faction_colony', 'High-Mobility Space Fighter',
    'High-Mobility Space Dominance Grunt', 2, 'Aether Aerospace Guild',
    'Mainline high-mobility interceptor frame of the Colony Union.',
    'Light Aerosteel Vector Frame', 36.0, 75.0, 580, 880, 62.0, 118.0, 48.0,
    ('hd_aether_sensor_fin', 'Aether Aerofin Sensor Array', 120, 3200, 0.5, 14.0, 1.8),
    ('cr_aether_tokamak_iii', 'Aether Sol-3 High-Compression Reactor', 480, 380, 'High-Compression Fusion Tokamak', 320.0, 32.0, 5, 16.0),
    ('am_aether_saber_left', 'Aether Agile Manipulator & Saber Hardpoint', 290, 12.0, 'wpn_beam_saber_aether', 'Hyperion Twin-Focus Beam Saber', 'Coherent Energy Melee', 210.0, 90, 80, 'Plasma Core', 999, 14.0, 26.0, 3.8),
    ('am_aether_rifle_right', 'Aether Stabilized Gun Arm', 290, 14.0, 'wpn_beam_pulse_rifle', 'Type-88 Coherent Beam Pulse Rifle', 'Particle Beam Rifle', 165.0, 140, 1200, 'E-Cap Magazine', 120, 9.5, 38.0, 8.5),
    ('lg_aether_aerosteel_legs', 'Aether Vector Vernier Bipedal Legs', 440, 340, 15.0, 75.0, 75.0, 24.0, 0.40),
    ('bp_aether_twin_thruster', 'Sol-Drive High-G Dual Vernier Pack', 160, 7.5, 35.0, 680.0, 'wpn_chaff_flare_launcher', 'Thermal Chaff & ECM Flare Dispenser', 'Countermeasure', 8, 6, 0.0, 600, 4.0),
    410000, 11, 18000, {'tungsten': 35, 'silica': 45, 'tritium': 10, 'flux': 18, 'slag': 0},
    {'kinetic': {'damage_reduction_pct': 0.15}, 'energy': {'damage_reduction_pct': 0.42}, 'rocket': {'damage_reduction_pct': 0.20}, 'melee': {'damage_reduction_pct': 0.25}},
    'Mainline high-mobility vector vernier interceptor of the Colony Union.'
))

SUITS.append(make_suit_data(
    'bp_ms_sylph_04', 'OCM-04 Sylph', 'OCM-04', 'faction_colony', 'Light Interceptor',
    'Light Orbital Interceptor Grunt', 1, 'Aether Aerospace Guild',
    'Ultra-lightweight orbital scout and interceptor with blistering evasion.',
    'Featherweight Interceptor Frame', 28.0, 58.0, 420, 650, 75.0, 135.0, 42.0,
    ('hd_sylph_monoeye', 'Sylph High-Frequency Sensor Mast', 90, 2800, 0.4, 10.0, 1.2),
    ('cr_sylph_core', 'Sol-1 Compact Reaction Engine', 340, 280, 'Miniaturized Fusion Core', 240.0, 22.0, 3, 12.0),
    ('am_sylph_left', 'Sylph Lightweight Left Arm', 210, 8.0, 'wpn_thermal_needle', 'High-Frequency Thermal Needle', 'Plasma Needle Melee', 140.0, 110, 60, 'Internal Cell', 999, 8.0, 16.0, 2.2),
    ('am_sylph_right', 'Sylph Lightweight Right Arm', 210, 10.0, 'wpn_particle_carbine', 'Light Particle Carbine', 'Beam Carbine', 95.0, 220, 900, 'E-Pack Light', 160, 5.5, 24.0, 5.5),
    ('lg_sylph_feather_legs', 'Sylph High-Agility Feather Struts', 320, 250, 11.0, 58.0, 88.0, 18.0, 0.30),
    ('bp_sylph_microrocket', 'Sylph Sprint Vernier Module', 110, 5.0, 26.0, 560.0, 'wpn_micro_missile_pod', 'Quad Micro-Missile Pod', 'Light Missile Pod', 4, 4, 42.0, 800, 12.0),
    240000, 7, 10500, {'tungsten': 30, 'silica': 30, 'tritium': 5, 'flux': 10, 'slag': 0},
    {'kinetic': {'damage_reduction_pct': 0.10}, 'energy': {'damage_reduction_pct': 0.35}, 'rocket': {'damage_reduction_pct': 0.15}, 'melee': {'damage_reduction_pct': 0.20}},
    'First combat chassis produced by the orbital shipyards, ultra-agile border interceptor.'
))

SUITS.append(make_suit_data(
    'bp_ms_helios_07', 'OCA-07 Helios Arbalest', 'OCA-07', 'faction_colony', 'Long-Range Particle Artillery',
    'Long-Range Particle Siege Artillery', 3, 'Aether Aerospace Guild',
    'Spinal beam bombardment warform mounting a heavy particle accelerator.',
    'Heavy Particle Stabilized Frame', 46.0, 92.0, 680, 1150, 50.0, 95.0, 62.0,
    ('hd_helios_long_sensor', 'Helios Tachyon Targeting Mast', 150, 4800, 0.7, 20.0, 2.2),
    ('cr_helios_sol_tokamak', 'Sol-Hyperion Fusion Accelerator Core', 580, 480, 'Particle-Surge Tokamak Core', 410.0, 48.0, 8, 22.0),
    ('am_helios_coolant_arm', 'Helios Auxiliary Radiator Arm', 340, 14.0, 'wpn_heat_radiator_shield', 'Cryo-Radiator Heat Siphon Shield', 'Defensive Thermal Siphon', 40.0, 60, 120, 'Cryo Coolant', 999, -15.0, 12.0, 8.0),
    ('am_helios_spinal_mount', 'Helios Heavy Accelerator Mount Arm', 340, 22.0, 'wpn_spinal_beam_accelerator', 'Spinal Coherent Particle Accelerator', 'Heavy Particle Beam', 380.0, 32, 2500, 'Supercharged E-Core', 36, 32.0, 85.0, 18.0),
    ('lg_helios_braced_legs', 'Helios Thermal Radiating Legs', 520, 410, 19.0, 92.0, 52.0, 28.0, 0.60),
    ('bp_helios_radiator_wings', 'Helios Fold-Out Thermal Radiator Wings', 220, 9.5, 32.0, 520.0, 'wpn_beam_turret_defensive', 'Twin Defensive Particle CIWS', 'Point Defense Beam', 12, 12, 28.0, 850, 14.0),
    580000, 19, 27500, {'tungsten': 45, 'silica': 62, 'tritium': 18, 'flux': 25, 'slag': 0},
    {'kinetic': {'damage_reduction_pct': 0.20}, 'energy': {'damage_reduction_pct': 0.48}, 'rocket': {'damage_reduction_pct': 0.22}, 'melee': {'damage_reduction_pct': 0.18}},
    'Long-range sniper and siege artillery developed to break Jovian gunboat blockades.'
))

SUITS.append(make_suit_data(
    'bp_ms_seraphim_15', 'OCX-15 Seraphim Trans-Am', 'OCX-15', 'faction_colony', 'Supercritical Dominator',
    'Supercritical Particle Surge Dominator', 4, 'Aether Aerospace Guild (Apex Sol)',
    'Apex particle combat frame with supercritical Trans-Am resonance drive.',
    'Supercritical Quantum Aerosteel Frame', 52.0, 110.0, 890, 1650, 78.0, 165.0, 75.0,
    ('hd_seraphim_crown', 'Seraphim Crown Quantum Sensor Array', 240, 5500, 0.3, 26.0, 2.5),
    ('cr_seraphim_transam_core', 'Trans-Am Supercritical Singularity Reactor', 780, 620, 'Singularity-Resonance Fusion Core', 560.0, 65.0, 10, 26.0),
    ('am_seraphim_left_blade', 'Seraphim Twin Particle Arm (Left)', 450, 20.0, 'wpn_hyper_beam_saber_pair', 'Trans-Am Dual Hyper-Beam Blades', 'Supercritical Energy Blade', 340.0, 110, 120, 'Singularity Tap', 999, 18.0, 45.0, 6.5),
    ('am_seraphim_right_cannon', 'Seraphim Heavy Beam Arm (Right)', 450, 24.0, 'wpn_twin_hyper_beam_cannon', 'Dual Hyper-Beam Buster Cannons', 'Supercritical Beam Battery', 460.0, 55, 2200, 'High-Density Energy Battery', 60, 35.0, 110.0, 16.5),
    ('lg_seraphim_wings_legs', 'Seraphim Quantum Vernier Legs', 680, 520, 22.0, 110.0, 95.0, 40.0, 0.55),
    ('bp_seraphim_eight_wings', 'Octa-Wing Trans-Am Vernier Drive', 320, 12.0, 55.0, 920.0, 'wpn_remote_funnel_pod', 'Sextuple Beam Funnel Dispenser', 'Remote Funnel Drone', 6, 6, 75.0, 2400, 28.0),
    920000, 27, 45000, {'tungsten': 70, 'silica': 85, 'tritium': 35, 'flux': 40, 'slag': 0},
    {'kinetic': {'damage_reduction_pct': 0.25}, 'energy': {'damage_reduction_pct': 0.55}, 'rocket': {'damage_reduction_pct': 0.30}, 'melee': {'damage_reduction_pct': 0.35}},
    'Undisputed crown jewel of Colony Aether fleet radiating an unmistakable solar corona.'
))

# 3. SYNDICATE RIM SCAVENGERS
SUITS.append(make_suit_data(
    'bp_ms_hyena_12', 'SCR-12 Hyena [Scavenger Line]', 'SCR-12', 'faction_syndicate', 'Asymmetric Heavy Scavenger',
    'Asymmetric Heavy Scavenger & Pirate Grunt', 2, 'Rust-Belt Free Foundry',
    'Junk-welded pirate mainstay combining flak scatterguns and pneumatic crusher claw.',
    'Reinforced Scrap Tubular Frame', 52.0, 105.0, 720, 1100, 48.0, 88.0, 30.0,
    ('hd_hyena_scrap_dome', 'Welded Mining Visor & Radio Rig', 140, 1900, 0.9, 10.0, 2.2),
    ('cr_hyena_salvage_tokamak', 'Overclocked Syndicate Fission-Turbine', 580, 480, 'Overclocked Fission-Turbine Hybrid', 265.0, 32.0, 3, 22.0),
    ('am_hyena_claw_arm', 'Heavy Hydraulic Breaching Claw Left Arm', 420, 18.0, 'wpn_hydraulic_scrap_claw', 'Pneumatic Scrap-Crusher Claw', 'Hydraulic Melee Crusher', 260.0, 70, 75, 'Pneumatic Charge', 999, 10.0, 22.0, 11.5),
    ('am_hyena_flak_arm', 'Hyena Heavy Recoil Right Arm', 360, 16.0, 'wpn_flak_scattergun', '8-Gauge Slag Flak Scattergun', 'Flak Kinetic Scattergun', 180.0, 90, 550, 'Slag Canister Shot', 140, 6.5, 12.0, 12.0),
    ('lg_hyena_scrap_legs', 'Reinforced Mining Excavator Legs', 560, 420, 23.0, 105.0, 48.0, 20.0, 0.58),
    ('bp_hyena_booster_rig', 'Slag-Vent Auxiliary Thruster Rig', 180, 9.0, 24.0, 440.0, 'wpn_scrap_rocket_rack', 'Unguided Slag Rocket Pod', 'Unguided Rocket Volley', 8, 4, 58.0, 700, 20.0),
    290000, 9, 11000, {'tungsten': 45, 'silica': 20, 'tritium': 4, 'flux': 8, 'slag': 15},
    {'kinetic': {'damage_reduction_pct': 0.35}, 'energy': {'damage_reduction_pct': 0.12}, 'rocket': {'damage_reduction_pct': 0.32}, 'melee': {'damage_reduction_pct': 0.30}},
    'Scavenger pirate workhorse feared for savage boarding actions in space hulks.'
))

SUITS.append(make_suit_data(
    'bp_ms_marauder_05', 'SCR-05 Marauder', 'SCR-05', 'faction_syndicate', 'Scrap Raider',
    'Close-Quarters Pirate Raider Grunt', 1, 'Rust-Belt Free Foundry',
    'Fast-moving ambush raider with serrated cleaver and short-range blunderbuss.',
    'Light Tubular Scavenger Frame', 40.0, 80.0, 540, 820, 58.0, 96.0, 26.0,
    ('hd_marauder_skulllight', 'Welded Shrapnel Mask & Searchlight', 110, 1500, 1.0, 8.0, 1.8),
    ('cr_marauder_fission_block', 'Salvaged Fission Heat Engine', 420, 340, 'Salvaged Fission Reactor', 205.0, 24.0, 2, 17.0),
    ('am_marauder_cleaver_arm', 'Marauder Welded Cleaver Arm', 280, 11.0, 'wpn_serrated_cleaver', 'Heavy Serrated Shipbreaker Cleaver', 'Crude Melee Cleaver', 175.0, 85, 60, 'Hardened Slag', 999, 4.0, 14.0, 6.5),
    ('am_marauder_gun_arm', 'Marauder Shrapnel Arm', 280, 12.0, 'wpn_shrapnel_gun_90mm', '90mm Scrap Shrapnel Gun', 'Short-Range Scatter Kinetic', 120.0, 110, 420, 'Scrap Pellets', 100, 4.5, 8.0, 7.5),
    ('lg_marauder_spring_legs', 'Hydraulic Rebound Struts', 410, 310, 16.0, 80.0, 58.0, 18.0, 0.42),
    ('bp_marauder_torch_booster', 'Chemical Thruster Tank Rig', 130, 6.5, 20.0, 410.0, 'wpn_smokescreen_torch', 'Chemical Heavy Smokescreen Pod', 'Tactical Smokescreen', 4, 3, 0.0, 350, 6.0),
    185000, 6, 7800, {'tungsten': 35, 'silica': 15, 'tritium': 0, 'flux': 4, 'slag': 15},
    {'kinetic': {'damage_reduction_pct': 0.28}, 'energy': {'damage_reduction_pct': 0.10}, 'rocket': {'damage_reduction_pct': 0.25}, 'melee': {'damage_reduction_pct': 0.22}},
    'Standard pirate ambush suit built in clandestine salvage bays across asteroid belts.'
))

SUITS.append(make_suit_data(
    'bp_ms_slag_lobber_14', 'SCA-14 Slag-Lobber', 'SCA-14', 'faction_syndicate', 'Incendiary Siege Mortar',
    'Converted Incendiary Slag Mortar', 3, 'Rust-Belt Free Foundry',
    'Converted smelting chassis equipped with an incendiary molten slag catapult.',
    'Heavy Foundry Bipedal Frame', 64.0, 135.0, 820, 1380, 38.0, 65.0, 38.0,
    ('hd_slag_smelt_visor', 'Smelting Visor & Ballistic Angle Gauge', 160, 2800, 1.1, 12.0, 2.8),
    ('cr_slag_furnace_core', 'Twin Industrial Induction Furnace Core', 680, 550, 'Overclocked Induction Crucible Core', 310.0, 42.0, 4, 26.0),
    ('am_slag_crane_arm', 'Excavator Crane & Anchor Arm', 450, 20.0, 'wpn_spiked_stabilizer_crane', 'Spiked Excavator Stabilizer Stake', 'Ground Anchor Melee', 140.0, 45, 90, 'Steel Stake', 999, 3.0, 10.0, 12.0),
    ('am_slag_mortar_arm', 'Slag Mortar Sponson Right Arm', 450, 24.0, 'wpn_slag_catapult_220mm', '220mm Molten Slag Catapult', 'Incendiary Siege Mortar', 310.0, 28, 1800, 'Liquid Slag Shells', 40, 24.0, 35.0, 19.5),
    ('lg_slag_heavy_treads', 'Hydraulic Smelting Track Legs', 680, 490, 28.0, 135.0, 32.0, 26.0, 0.75),
    ('bp_slag_crucible_hopper', 'Crucible Slag Pre-Heater Hopper', 240, 13.0, 28.0, 360.0, 'wpn_incendiary_mine_layer', 'Thermite Mine Ejector Rack', 'Area Denial Mine', 4, 6, 85.0, 500, 16.0),
    460000, 15, 21000, {'tungsten': 60, 'silica': 25, 'tritium': 5, 'flux': 10, 'slag': 30},
    {'kinetic': {'damage_reduction_pct': 0.38}, 'energy': {'damage_reduction_pct': 0.25}, 'rocket': {'damage_reduction_pct': 0.35}, 'melee': {'damage_reduction_pct': 0.20}},
    'Rains molten industrial slag to breach hardened hangar blast doors and perimeter bunkers.'
))

SUITS.append(make_suit_data(
    'bp_ms_chimera_19', 'SCX-19 Chimera Apex', 'SCX-19', 'faction_syndicate', 'Illegal Hybrid Dreadnought',
    'Illegal Hybrid Dreadnought Brawler', 4, 'Rust-Belt Free Foundry (Bay 9)',
    'Four-armed hybrid dreadnought with stolen siege rails and dual demolition claws.',
    'Four-Armed Asymmetric Heavy Frame', 82.0, 185.0, 1150, 2100, 42.0, 82.0, 48.0,
    ('hd_chimera_spider_optic', 'Octa-Lens Stolen Sensor Array', 310, 4200, 0.7, 22.0, 3.8),
    ('cr_chimera_stolen_tokamak', 'Twin Terran-Aether Hybrid Core', 1050, 820, 'Hot-Wired Hybrid Dual Tokamak', 480.0, 65.0, 8, 38.0),
    ('am_chimera_dual_claws', 'Tandem Hydraulic Crushing Arm (Left)', 620, 30.0, 'wpn_twin_demolition_claws', 'Dual Breaching Demolition Claws', 'Tandem Kinetic Melee', 480.0, 60, 90, 'Pneumatic Fluid', 999, 16.0, 35.0, 18.0),
    ('am_chimera_stolen_rail', 'Scavenged Rail Cannon Mount (Right)', 620, 32.0, 'wpn_stolen_siege_rail_250mm', '250mm Stolen Siege Railgun', 'Stolen Magnetic Accelerator', 490.0, 22, 2400, '250mm Penetrator', 32, 34.0, 80.0, 26.0),
    ('lg_chimera_reinforced_legs', 'Quad-Pneumatic Brawler Legs', 920, 740, 36.0, 185.0, 38.0, 38.0, 0.82),
    ('bp_chimera_salvage_engines', 'Overloaded Cruiser Thruster Pod', 380, 16.0, 48.0, 640.0, 'wpn_cluster_bomb_rack', 'Slag Canister Carpet Dispenser', 'Cluster Bomb Rack', 12, 6, 48.0, 900, 22.0),
    820000, 26, 38000, {'tungsten': 95, 'silica': 45, 'tritium': 20, 'flux': 25, 'slag': 35},
    {'kinetic': {'damage_reduction_pct': 0.44}, 'energy': {'damage_reduction_pct': 0.28}, 'rocket': {'damage_reduction_pct': 0.40}, 'melee': {'damage_reduction_pct': 0.35}},
    'Scavenged apex dreadnought cobbled from destroyed capital ships and derelict planetary wrecks.'
))

# 4. ZAIBATSU AEROSPACE CONGLOMERATE
SUITS.append(make_suit_data(
    'bp_ms_muramasa_11', 'ZM-11 Muramasa [Security Line]', 'ZM-11', 'faction_zaibatsu', 'Stealth Precision Warform',
    'Stealth Precision Corporate Grunt', 2, 'Apex Zaibatsu Aerospace',
    'High-tech corporate enforcer with active optical baffling and monomolecular plasma blade.',
    'Carbon-Titanium Monocoque Frame', 42.0, 85.0, 650, 920, 56.0, 112.0, 52.0,
    ('hd_muramasa_optic_visor', 'Apex Optical Telemetry Multi-Sensor', 130, 3600, 0.4, 16.0, 2.0),
    ('cr_muramasa_tokamak', 'Sub-Nanometer Quantum Fusion Tokamak', 520, 410, 'Quantum-Shielded Fusion Core', 340.0, 38.0, 6, 18.0),
    ('am_muramasa_katana_arm', 'Precision Servo Manipulator (Left)', 320, 14.0, 'wpn_muramasa_plasma_katana', 'Muramasa High-Frequency Plasma Katana', 'Monofilament Plasma Blade', 270.0, 120, 85, 'Plasma Core', 999, 12.0, 32.0, 4.5),
    ('am_muramasa_carbine_arm', 'Precision Gyro Stabilized Arm (Right)', 320, 15.0, 'wpn_plasma_carbine_twin', 'Type-91 Dual Plasma Burst Carbine', 'High-Velocity Plasma Rifle', 150.0, 180, 1100, 'Plasma Cartridge', 150, 8.0, 42.0, 9.0),
    ('lg_muramasa_sprint_legs', 'Apex High-Tensile Sprint Bipedal Legs', 480, 370, 17.0, 85.0, 78.0, 28.0, 0.48),
    ('bp_muramasa_stealth_pack', 'Active Optical Baffle & Sprint Pack', 180, 8.5, 40.0, 640.0, 'wpn_ecm_jamming_pod', 'Active Radar Jammer & Decoy Launcher', 'Electronic Warfare ECM', 4, 6, 0.0, 1200, 10.0),
    490000, 13, 22000, {'tungsten': 38, 'silica': 52, 'tritium': 12, 'flux': 22, 'slag': 0},
    {'kinetic': {'damage_reduction_pct': 0.22}, 'energy': {'damage_reduction_pct': 0.38}, 'rocket': {'damage_reduction_pct': 0.20}, 'melee': {'damage_reduction_pct': 0.30}},
    'Corporate assassin and high-value facility defense frame with optical stealth baffles.'
))

SUITS.append(make_suit_data(
    'bp_ms_ronin_06', 'ZM-06 Ronin', 'ZM-06', 'faction_zaibatsu', 'Security Duellist',
    'Corporate Security Duellist Grunt', 1, 'Apex Zaibatsu Aerospace',
    'Light security escort with high-frequency vibro-blade and 45mm caseless PDW.',
    'Light Agile Corporate Frame', 34.0, 70.0, 480, 740, 64.0, 115.0, 45.0,
    ('hd_ronin_sensor', 'Ronin Monocular Surveillance Sensor', 110, 2600, 0.5, 11.0, 1.5),
    ('cr_ronin_reactor', 'Apex Mini-Tokamak Mark II', 380, 320, 'Miniaturized Tokamak Core', 250.0, 26.0, 4, 14.0),
    ('am_ronin_blade_arm', 'Ronin Duellist Arm (Left)', 240, 9.0, 'wpn_vibro_blade', 'Type-4 High-Frequency Vibro-Blade', 'Vibro Melee Blade', 160.0, 130, 70, 'Internal Servo', 999, 5.0, 18.0, 3.2),
    ('am_ronin_pdw_arm', 'Ronin Rapid-Fire Arm (Right)', 240, 11.0, 'wpn_pdw_45mm', 'Apex 45mm High-Cycle PDW', 'Rapid Kinetic PDW', 80.0, 320, 750, '45mm Caseless', 240, 3.8, 14.0, 6.2),
    ('lg_ronin_agile_legs', 'Ronin High-Response Struts', 360, 280, 13.0, 70.0, 82.0, 22.0, 0.38),
    ('bp_ronin_sprint_thruster', 'Apex Compact Vector Pack', 130, 5.8, 25.0, 520.0, 'wpn_flashbang_launcher', 'Strobe Flashbang Mortar', 'Optical Disrupter', 3, 4, 0.0, 450, 4.0),
    260000, 8, 11500, {'tungsten': 28, 'silica': 38, 'tritium': 6, 'flux': 14, 'slag': 0},
    {'kinetic': {'damage_reduction_pct': 0.16}, 'energy': {'damage_reduction_pct': 0.30}, 'rocket': {'damage_reduction_pct': 0.15}, 'melee': {'damage_reduction_pct': 0.25}},
    'Corporate security escort built to defend arcology lobbies and VIP executive suites.'
))

SUITS.append(make_suit_data(
    'bp_ms_raiden_15', 'ZMA-15 Raiden', 'ZMA-15', 'faction_zaibatsu', 'Precision Railgun Sniper',
    'Precision Railgun Sniper Platform', 3, 'Apex Zaibatsu Aerospace',
    'Extreme standoff railgun sniper with helium-cooled quantum core and bipod stabilizer.',
    'Precision Monocoque Stabilized Frame', 48.0, 92.0, 640, 1100, 52.0, 98.0, 58.0,
    ('hd_raiden_sniper_array', 'Apex Extreme-Range Telemetry Optic', 150, 5200, 0.4, 24.0, 2.2),
    ('cr_raiden_quantum_core', 'Apex Mark-IV Helium-Cooled Fusion Core', 550, 450, 'Helium-Cooled Quantum Core', 395.0, 46.0, 8, 21.0),
    ('am_raiden_bipod_arm', 'Gyro-Stabilized Bipod Arm (Left)', 310, 13.0, 'wpn_bipod_target_designator', 'Laser Target Illuminator & Bipod', 'Sniper Stabilizer', 0.0, 60, 3500, 'Telemetry Lock', 999, 1.0, 12.0, 5.5),
    ('am_raiden_linear_arm', 'Hyper-Velocity Linear Mount Arm (Right)', 310, 25.0, 'wpn_hyper_velocity_railgun', 'Type-99 Hyper-Velocity Magnetic Accelerator', 'Extreme-Range Kinetic Railgun', 390.0, 26, 3200, 'Hyper-Velocity Sabot', 36, 26.0, 92.0, 19.5),
    ('lg_raiden_strut_legs', 'Recoil-Absorbing Gyro Struts', 480, 390, 18.0, 92.0, 55.0, 26.0, 0.72),
    ('bp_raiden_capacitor_pack', 'Cryo-Capacitor Linear Boost Pack', 190, 9.2, 35.0, 550.0, 'wpn_thermal_decoy_rack', 'Thermal Decoy & Counter-Battery Jammer', 'Electronic Warfare Decoy', 4, 6, 0.0, 1500, 8.0),
    590000, 18, 26500, {'tungsten': 45, 'silica': 68, 'tritium': 18, 'flux': 28, 'slag': 0},
    {'kinetic': {'damage_reduction_pct': 0.24}, 'energy': {'damage_reduction_pct': 0.36}, 'rocket': {'damage_reduction_pct': 0.20}, 'melee': {'damage_reduction_pct': 0.20}},
    'Long-distance surgical elimination weapon that punches through armored bridges.'
))

SUITS.append(make_suit_data(
    'bp_ms_susanoo_22', 'ZX-22 Susanoo Cyber-Drive', 'ZX-22', 'faction_zaibatsu', 'Transhuman Cyber Warform',
    'Hyper-Cognitive Transhuman Dominance Frame', 4, 'Apex Zaibatsu (Neural Labs)',
    'Transhuman cybernetic dominance frame directly interfaced with pilot cerebral cortex.',
    'Superconducting Neural Monocoque Frame', 48.0, 100.0, 920, 1750, 74.0, 155.0, 70.0,
    ('hd_susanoo_neural_crown', 'Apex Neural Synapse Interface Visor', 260, 5800, 0.2, 32.0, 2.4),
    ('cr_susanoo_quantum_singularity', 'Zero-Point Quantum Singularity Core', 820, 660, 'Zero-Point Quantum Singularity', 580.0, 70.0, 10, 25.0),
    ('am_susanoo_left_arm', 'Neural-Linked Servo Arm (Left)', 480, 22.0, 'wpn_tachyon_saber_twin', 'Dual Relativistic Tachyon Sabers', 'Tachyon Melee Blade', 360.0, 140, 110, 'Zero-Point Tap', 999, 16.0, 52.0, 6.8),
    ('am_susanoo_right_arm', 'Neural-Linked Accelerator Arm (Right)', 480, 25.0, 'wpn_quantum_tachyon_blaster', 'Twin Quantum Tachyon Beam Blaster', 'High-Output Quantum Beam', 420.0, 65, 2100, 'Quantum Flux Core', 80, 30.0, 98.0, 15.2),
    ('lg_susanoo_neural_legs', 'Superconducting Vernier Bipedal Legs', 710, 540, 21.0, 100.0, 98.0, 42.0, 0.60),
    ('bp_susanoo_singularity_pack', 'Zero-Point Vernier Shift Pack', 340, 11.5, 58.0, 880.0, 'wpn_neural_drone_cloud', 'Octa-Neural Swarm Interceptor Drones', 'Autonomous Neural Drone', 8, 6, 62.0, 2200, 24.0),
    950000, 28, 48000, {'tungsten': 65, 'silica': 90, 'tritium': 30, 'flux': 45, 'slag': 0},
    {'kinetic': {'damage_reduction_pct': 0.30}, 'energy': {'damage_reduction_pct': 0.52}, 'rocket': {'damage_reduction_pct': 0.32}, 'melee': {'damage_reduction_pct': 0.40}},
    'Hyper-cognitive warform moving with near-zero latency, anticipating firing vectors.'
))

# 5. PLAYER PMC MODULAR DOCTRINES
SUITS.append(make_suit_data(
    'bp_player_vanguard_heavy', 'PMC-01 Vanguard Breaker', 'PMC-01', 'player', 'Modular Heavy Assault',
    'Modular Heavy Vanguard Linebreaker', 2, 'Player PMC Foundries',
    'Player-engineered heavy linebreaker chassis with universal hardpoints.',
    'Modular Heavy Bipedal Frame', 54.0, 115.0, 820, 1150, 44.0, 82.0, 38.0,
    ('hd_pmc_target_sentry', 'PMC Multi-Spectrum Tactical Visor', 160, 2600, 0.7, 12.0, 2.3),
    ('cr_pmc_heavy_fusion', 'PMC High-Yield Modular Fusion Core', 620, 480, 'Tritium-Enriched Fusion Tokamak', 310.0, 36.0, 5, 23.0),
    ('am_pmc_heavy_left', 'PMC Reinforced Hardpoint Arm (Left)', 380, 18.0, 'wpn_pmc_autocannon_115mm', 'PMC 115mm Modular Solid-Slug Autocannon', 'Kinetic Autocannon', 150.0, 190, 920, '115mm Heavy AP', 220, 4.0, 8.0, 13.5),
    ('am_pmc_heavy_right', 'PMC Reinforced Hardpoint Arm (Right)', 380, 19.0, 'wpn_pmc_rotary_vulcan', 'PMC 35mm Gatling Shredder', 'Rotary Ballistic', 42.0, 1150, 680, '35mm Sabot', 1600, 1.1, 14.0, 15.0),
    ('lg_pmc_hydraulic_legs', 'PMC Heavy Hydraulic Stabilizer Legs', 620, 430, 25.0, 115.0, 45.0, 22.0, 0.62),
    ('bp_pmc_ares_pack', 'PMC Modular Ordnance Pod Pack', 210, 10.5, 26.0, 440.0, 'wpn_pmc_missile_swarm', 'PMC Swarm-12 Guided Micro-Missiles', 'Guided Missile Pod', 12, 6, 68.0, 1400, 28.0),
    360000, 10, 15000, {'tungsten': 55, 'silica': 28, 'tritium': 8, 'flux': 12, 'slag': 0},
    {'kinetic': {'damage_reduction_pct': 0.38}, 'energy': {'damage_reduction_pct': 0.22}, 'rocket': {'damage_reduction_pct': 0.34}, 'melee': {'damage_reduction_pct': 0.18}},
    'Player-commissioned assault linebreaker engineered with proprietary Vanguard Composite alloys.'
))

SUITS.append(make_suit_data(
    'bp_player_stratos_interceptor', 'PMC-02 Stratos Interceptor', 'PMC-02', 'player', 'Modular High-G Interceptor',
    'Player Modular Stratos High-G Interceptor', 2, 'Player PMC Foundries',
    'High-agility orbital fighter frame utilizing vector vernier thrusters.',
    'Aerosteel Hybrid Interceptor Frame', 38.0, 80.0, 610, 890, 60.0, 115.0, 46.0,
    ('hd_pmc_aerofin', 'PMC High-G Telemetry Fin', 130, 3100, 0.5, 14.0, 1.9),
    ('cr_pmc_flux_reactor', 'PMC Hyperion-Flux Core', 490, 390, 'Flux-Boosted Fusion Tokamak', 330.0, 34.0, 5, 17.0),
    ('am_pmc_saber_arm', 'PMC Rapid Servo Manipulator (Left)', 300, 13.0, 'wpn_pmc_beam_saber', 'PMC Hyperion Focus Beam Saber', 'Coherent Energy Melee', 220.0, 95, 85, 'Plasma E-Cap', 999, 13.0, 28.0, 4.0),
    ('am_pmc_beam_arm', 'PMC Beam Hardpoint Arm (Right)', 300, 15.0, 'wpn_pmc_particle_rifle', 'PMC Twin Particle Pulse Rifle', 'Particle Beam Rifle', 170.0, 145, 1180, 'E-Cap Magazine', 130, 9.0, 40.0, 8.8),
    ('lg_pmc_vernier_legs', 'PMC Vector Vernier Strut Legs', 460, 350, 16.0, 80.0, 72.0, 25.0, 0.42),
    ('bp_pmc_vector_pack', 'PMC Dual Sol-Vernier Thruster Pack', 170, 8.0, 36.0, 660.0, 'wpn_pmc_ecm_chaff', 'Chaff Dispenser & Thermal Cloak', 'Tactical Countermeasure', 6, 6, 0.0, 550, 4.0),
    440000, 11, 17500, {'tungsten': 10, 'silica': 15, 'tritium': 25, 'flux': 20, 'slag': 0},
    {'kinetic': {'damage_reduction_pct': 0.18}, 'energy': {'damage_reduction_pct': 0.40}, 'rocket': {'damage_reduction_pct': 0.22}, 'melee': {'damage_reduction_pct': 0.24}},
    'Player-commissioned orbital interceptor designed to dominate deep space sectors.'
))

SUITS.append(make_suit_data(
    'bp_player_scrapper_brawler', 'PMC-03 Chimera Scrapper', 'PMC-03', 'player', 'Modular Scrapper Bruiser',
    'Player Modular Scrapper Bruiser', 2, 'Player PMC Foundries',
    'Cost-effective modular chassis with high-impact flak arrays and fast-swap armor.',
    'Reinforced Modular Scrapper Frame', 50.0, 102.0, 720, 1100, 48.0, 92.0, 32.0,
    ('hd_pmc_scrapper_visor', 'PMC Reinforced Mining Visor', 140, 2000, 0.8, 10.0, 2.1),
    ('cr_pmc_turbine_core', 'PMC Overclocked Turbine Fission Core', 560, 470, 'Turbine Fission Core', 280.0, 32.0, 4, 21.0),
    ('am_pmc_harpoon_arm', 'PMC Pneumatic Harpoon Arm (Left)', 390, 17.0, 'wpn_pmc_pneumatic_harpoon', 'Pneumatic Harpoon & Breaching Ram', 'Hydraulic Melee Harpoon', 250.0, 75, 120, 'Pneumatic Stake', 999, 8.0, 18.0, 10.5),
    ('am_pmc_flak_arm', 'PMC Heavy Flak Hardpoint (Right)', 370, 16.0, 'wpn_pmc_flak_cannon', 'Scrap-Flak Heavy Rapid Cannon', 'Flak Kinetic Scattergun', 175.0, 95, 580, 'Flak Canister', 150, 6.0, 11.0, 11.5),
    ('lg_pmc_brawler_legs', 'PMC Reinforced Excavator Bipedal Legs', 550, 410, 22.0, 102.0, 50.0, 20.0, 0.56),
    ('bp_pmc_scrapper_booster', 'PMC Slag-Ejector Thruster Pack', 180, 8.5, 22.0, 460.0, 'wpn_pmc_smokescreen_rack', 'Heavy Smokescreen & Shrapnel Ejector', 'Area Obscuration', 6, 4, 12.0, 450, 8.0),
    325000, 9, 12000, {'tungsten': 25, 'silica': 20, 'tritium': 0, 'flux': 10, 'slag': 20},
    {'kinetic': {'damage_reduction_pct': 0.34}, 'energy': {'damage_reduction_pct': 0.14}, 'rocket': {'damage_reduction_pct': 0.30}, 'melee': {'damage_reduction_pct': 0.28}},
    'Cost-effective modular brawler built with high-velocity scrap ordnance.'
))

SUITS.append(make_suit_data(
    'bp_player_ghost_sniper', 'PMC-04 Kusanagi Ghost', 'PMC-04', 'player', 'Neural-Linked Precision Warform',
    'Player Modular Ghost Sniper', 3, 'Player PMC Foundries',
    'Experimental cyber-neural chassis forged with superconductor matrices.',
    'Superconductor Neural Monocoque Frame', 45.0, 88.0, 780, 1050, 56.0, 110.0, 54.0,
    ('hd_pmc_ghost_sensor', 'PMC Neural Infiltration Visor', 150, 4500, 0.35, 20.0, 2.0),
    ('cr_pmc_quantum_tokamak', 'PMC Sub-Nanometer Quantum Tokamak', 600, 480, 'Quantum Tokamak Core', 380.0, 44.0, 7, 20.0),
    ('am_pmc_nanoblade_arm', 'PMC Monomolecular Manipulator (Left)', 340, 14.0, 'wpn_pmc_nanoblade', 'High-Frequency Nanoblade & Thermal Saber', 'Monofilament Energy Blade', 290.0, 125, 90, 'Superconducting Edge', 999, 11.0, 34.0, 4.2),
    ('am_pmc_linear_rifle_arm', 'PMC Linear Rifle Hardpoint (Right)', 340, 18.0, 'wpn_pmc_linear_rifle', 'Linear Accelerator Sniper Rifle', 'Precision Linear Accelerator', 310.0, 45, 2100, 'Magnetic Linear Sabot', 50, 18.0, 62.0, 12.0),
    ('lg_pmc_ghost_legs', 'PMC Agile Bipedal Dampener Legs', 520, 400, 17.5, 88.0, 76.0, 26.0, 0.58),
    ('bp_pmc_optical_cloak_pack', 'Active Optical Cloak & ECM Thruster Pack', 210, 8.8, 42.0, 650.0, 'wpn_pmc_sensor_decoy', 'Holographic Decoy & Chaff Ejector', 'Optical Decoy System', 4, 6, 0.0, 1200, 8.0),
    485000, 14, 23500, {'tungsten': 15, 'silica': 10, 'tritium': 35, 'flux': 30, 'slag': 0},
    {'kinetic': {'damage_reduction_pct': 0.24}, 'energy': {'damage_reduction_pct': 0.40}, 'rocket': {'damage_reduction_pct': 0.22}, 'melee': {'damage_reduction_pct': 0.32}},
    'Player-commissioned stealth sniper warform combining optical baffles with linear rail punch.'
))

def main():
    print(f'Writing {len(SUITS)} canonical blueprint JSON files to {OUT_DIR}...')
    for s in SUITS:
        path = os.path.join(OUT_DIR, f"{s['blueprint_id']}.json")
        with open(path, 'w') as f:
            json.dump(s, f, indent=4)
        specs = s['totals_and_specs']
        print(f"✓ {s['blueprint_id']}.json | Weight: {specs['total_weight_tonnes']}/{specs['max_weight_tonnes']}t | Net Surplus: +{specs['net_power_surplus_mw']}MW | Armor: {specs['total_armor_hp']}HP")
    print('ALL 20 BLUEPRINTS SUCCESSFULLY GENERATED AND VALIDATED!')

if __name__ == '__main__':
    main()
