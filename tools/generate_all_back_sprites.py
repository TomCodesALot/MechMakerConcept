import os
import json
import uuid
from PIL import Image, ImageDraw

SPRITES_DIR = "sprites"
YYP_PATH = "MechMakerConcept.yyp"

def create_back_mech_sprite(sprite_name, base_color, accent_color, glow_color, mech_type):
    spr_path = os.path.join(SPRITES_DIR, sprite_name)
    layers_path = os.path.join(spr_path, "layers")
    os.makedirs(spr_path, exist_ok=True)
    os.makedirs(layers_path, exist_ok=True)

    layer_id = str(uuid.uuid4())
    frame_uuids = [str(uuid.uuid4()) for _ in range(4)]
    
    # Generate 4 distinct animation frames (160x160) for BACK-FACING isometric perspective
    for i, f_uuid in enumerate(frame_uuids):
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        
        # Ground shadow
        draw.ellipse([30, 142, 130, 154], fill=(0, 0, 0, 95))
        
        # Idle / walk bob offsets
        y_bob = -2 if (i == 1 or i == 3) else 0
        x_shift = 1 if i == 2 else (-1 if i == 3 else 0)
        
        if mech_type == "ballista":
            # Rear view of Quadruped Heavy Artillery
            # Rear anchor legs (prominent in back view)
            draw.polygon([(40 + x_shift, 146 + y_bob), (32 + x_shift, 115 + y_bob), (54 + x_shift, 110 + y_bob), (62 + x_shift, 146 + y_bob)], fill=base_color, outline=accent_color)
            draw.polygon([(98 - x_shift, 146 + y_bob), (106 - x_shift, 110 + y_bob), (128 - x_shift, 115 + y_bob), (120 - x_shift, 146 + y_bob)], fill=base_color, outline=accent_color)
            # Front legs visible in background
            draw.polygon([(54 + x_shift, 138 + y_bob), (50, 115 + y_bob), (64, 112 + y_bob), (68 + x_shift, 138 + y_bob)], fill=(35, 42, 32, 255))
            draw.polygon([(92 - x_shift, 138 + y_bob), (96, 112 + y_bob), (110, 115 + y_bob), (106 - x_shift, 138 + y_bob)], fill=(35, 42, 32, 255))
            # Rear Chassis Bulkhead
            draw.rounded_rectangle([48, 75 + y_bob, 112, 115 + y_bob], radius=6, fill=base_color, outline=accent_color, width=2)
            # Twin massive radiator exhaust grilles on rear
            draw.rectangle([56, 86 + y_bob, 74, 104 + y_bob], fill=(25, 30, 24, 255), outline=accent_color)
            draw.rectangle([86, 86 + y_bob, 104, 104 + y_bob], fill=(25, 30, 24, 255), outline=accent_color)
            for gy in range(88, 103, 4):
                draw.line([58, gy + y_bob, 72, gy + y_bob], fill=glow_color if (i == 1 or i == 3) else (60, 70, 55, 255))
                draw.line([88, gy + y_bob, 102, gy + y_bob], fill=glow_color if (i == 1 or i == 3) else (60, 70, 55, 255))
            # Rear of sensor turret
            draw.rectangle([68, 60 + y_bob, 92, 74 + y_bob], fill=(30, 36, 28, 255), outline=accent_color)
            # Dual massive howitzer breeches & ammo chutes
            draw.rectangle([40, 35 + y_bob, 54, 85 + y_bob], fill=(50, 58, 45, 255), outline=(20, 25, 20, 255), width=2)
            draw.rectangle([106, 35 + y_bob, 120, 85 + y_bob], fill=(50, 58, 45, 255), outline=(20, 25, 20, 255), width=2)
            # Heavy ammo feed belts entering breeches
            draw.polygon([(54, 75 + y_bob), (68, 85 + y_bob), (68, 92 + y_bob), (54, 82 + y_bob)], fill=(120, 100, 40, 255))
            draw.polygon([(106, 75 + y_bob), (92, 85 + y_bob), (92, 92 + y_bob), (106, 82 + y_bob)], fill=(120, 100, 40, 255))

        elif mech_type == "centurion":
            # Rear view of TH-C02 Centurion
            # Heavy calf hydraulics
            draw.polygon([(46 + x_shift, 146 + y_bob), (42, 110 + y_bob), (62, 110 + y_bob), (66 + x_shift, 146 + y_bob)], fill=(45, 52, 42, 255))
            draw.polygon([(94 - x_shift, 146 + y_bob), (98, 110 + y_bob), (118, 110 + y_bob), (114 - x_shift, 146 + y_bob)], fill=(45, 52, 42, 255))
            # Rear calf stabilizer vents
            draw.rectangle([48, 124 + y_bob, 60, 134 + y_bob], fill=(28, 35, 26, 255))
            draw.rectangle([100, 124 + y_bob, 112, 134 + y_bob], fill=(28, 35, 26, 255))
            # Heavy reactor backpack with cooling fins
            draw.rectangle([54, 65 + y_bob, 106, 112 + y_bob], fill=base_color, outline=accent_color, width=2)
            draw.rectangle([64, 70 + y_bob, 96, 105 + y_bob], fill=(30, 38, 28, 255), outline=accent_color)
            for fy in range(74, 102, 5):
                draw.line([66, fy + y_bob, 94, fy + y_bob], fill=glow_color if (i == 1 or i == 3) else (70, 80, 65, 255), width=2)
            # Rear helmet plate with antenna mast
            draw.polygon([(72, 52 + y_bob), (88, 52 + y_bob), (86, 68 + y_bob), (74, 68 + y_bob)], fill=(32, 40, 30, 255))
            draw.line([80, 40 + y_bob, 80, 52 + y_bob], fill=accent_color, width=2)
            # Ammo hopper on right back feeding vulcan
            draw.rectangle([98, 68 + y_bob, 114, 88 + y_bob], fill=(55, 62, 50, 255), outline=accent_color)
            draw.polygon([(110, 88 + y_bob), (118, 98 + y_bob), (114, 104 + y_bob), (106, 94 + y_bob)], fill=(130, 110, 50, 255))
            # Back of tower shield on left arm (inner braces & operator handle)
            draw.polygon([(24, 62 + y_bob), (44, 56 + y_bob), (48, 132 + y_bob), (28, 138 + y_bob)], fill=(50, 58, 48, 255), outline=(25, 30, 22, 255), width=2)
            draw.rectangle([32, 85 + y_bob, 40, 105 + y_bob], fill=(20, 25, 18, 255)) # Handle bracket

        elif mech_type == "trenchcoat":
            # Rear view of TH-T09 Trenchcoat
            # Low wide legs
            draw.polygon([(44 + x_shift, 146 + y_bob), (40, 115 + y_bob), (60, 115 + y_bob), (64 + x_shift, 146 + y_bob)], fill=(35, 38, 42, 255))
            draw.polygon([(96 - x_shift, 146 + y_bob), (100, 115 + y_bob), (120, 115 + y_bob), (116 - x_shift, 146 + y_bob)], fill=(35, 38, 42, 255))
            # Rear Ballistic Drapery (Heavy Coat Plates wrapping behind)
            draw.polygon([(36, 92 + y_bob), (54, 88 + y_bob), (52, 132 + y_bob), (34, 128 + y_bob)], fill=(45, 50, 56, 255), outline=(20, 24, 28, 255))
            draw.polygon([(106, 88 + y_bob), (124, 92 + y_bob), (126, 128 + y_bob), (108, 132 + y_bob)], fill=(45, 50, 56, 255), outline=(20, 24, 28, 255))
            draw.polygon([(52, 92 + y_bob), (108, 92 + y_bob), (106, 130 + y_bob), (54, 130 + y_bob)], fill=(40, 45, 50, 255), outline=(20, 24, 28, 255))
            # Upper Torso Backplate with fuel tank canister
            draw.rectangle([54, 66 + y_bob, 106, 96 + y_bob], fill=base_color, outline=accent_color, width=2)
            draw.rounded_rectangle([68, 72 + y_bob, 92, 90 + y_bob], radius=4, fill=(30, 32, 36, 255), outline=(15, 18, 20, 255))
            # Smoke discharger canisters from behind
            draw.rectangle([46, 48 + y_bob, 54, 68 + y_bob], fill=(30, 32, 36, 255))
            draw.rectangle([106, 48 + y_bob, 114, 68 + y_bob], fill=(30, 32, 36, 255))
            if i == 1: # Smoke puffs
                draw.ellipse([43, 38, 57, 48], fill=(140, 140, 140, 110))
                draw.ellipse([103, 38, 117, 48], fill=(140, 140, 140, 110))
            # Rear of combat helmet
            draw.polygon([(72, 50 + y_bob), (88, 50 + y_bob), (86, 66 + y_bob), (74, 66 + y_bob)], fill=(28, 30, 34, 255))

        elif mech_type == "zephyr":
            # Rear view of JCC-Z05 Zephyr
            # Main dual rocket thruster bells with bright cyan plumes
            p_len = 18 if (i == 1 or i == 3) else 12
            draw.polygon([(64, 115 + y_bob), (70, 115 + y_bob + p_len), (76, 115 + y_bob)], fill=glow_color)
            draw.polygon([(84, 115 + y_bob), (90, 115 + y_bob + p_len), (96, 115 + y_bob)], fill=glow_color)
            # Legs tucked in zero-G flight behind
            draw.polygon([(56 + x_shift, 134 + y_bob), (50, 105 + y_bob), (64, 105 + y_bob), (70 + x_shift, 134 + y_bob)], fill=(26, 38, 55, 255))
            draw.polygon([(90 - x_shift, 134 + y_bob), (96, 105 + y_bob), (110, 105 + y_bob), (104 - x_shift, 134 + y_bob)], fill=(26, 38, 55, 255))
            # Swept delta wings viewed from rear
            draw.polygon([(20, 80 + y_bob), (52, 65 + y_bob), (52, 98 + y_bob)], fill=accent_color, outline=(15, 25, 40, 255))
            draw.polygon([(140, 80 + y_bob), (108, 65 + y_bob), (108, 98 + y_bob)], fill=accent_color, outline=(15, 25, 40, 255))
            # Streamlined fuselage back
            draw.polygon([(80, 45 + y_bob), (102, 70 + y_bob), (94, 112 + y_bob), (66, 112 + y_bob), (58, 70 + y_bob)], fill=base_color, outline=accent_color)
            # Sensor dorsal fin spine
            draw.polygon([(78, 38 + y_bob), (82, 38 + y_bob), (84, 62 + y_bob), (76, 62 + y_bob)], fill=accent_color)

        elif mech_type == "kepler":
            # Rear view of JCC-K02 Kepler
            # Zero-G thruster legs
            draw.polygon([(54 + x_shift, 142 + y_bob), (48, 108 + y_bob), (64, 108 + y_bob), (68 + x_shift, 142 + y_bob)], fill=(28, 38, 58, 255))
            draw.polygon([(92 - x_shift, 142 + y_bob), (96, 108 + y_bob), (112, 108 + y_bob), (106 - x_shift, 142 + y_bob)], fill=(28, 38, 58, 255))
            # Large solar stabilizing wing fins
            draw.polygon([(16, 52 + y_bob), (48, 66 + y_bob), (44, 86 + y_bob), (14, 76 + y_bob)], fill=accent_color, outline=(18, 26, 42, 255))
            draw.polygon([(144, 52 + y_bob), (112, 66 + y_bob), (116, 86 + y_bob), (146, 76 + y_bob)], fill=accent_color, outline=(18, 26, 42, 255))
            # Torso Back with capacitor generator pack
            draw.polygon([(80, 48 + y_bob), (102, 72 + y_bob), (94, 110 + y_bob), (66, 110 + y_bob), (58, 72 + y_bob)], fill=base_color, outline=accent_color, width=2)
            draw.rectangle([68, 68 + y_bob, 92, 98 + y_bob], fill=(22, 32, 50, 255), outline=accent_color)
            # Superconducting power cable running from pack to railgun
            draw.line([92, 80 + y_bob, 114, 80 + y_bob], fill=glow_color, width=3)
            # Railgun rear housing
            draw.rectangle([112, 24 + y_bob, 122, 138 + y_bob], fill=(38, 50, 72, 255), outline=(12, 18, 28, 255), width=2)
            draw.rectangle([110, 40 + y_bob, 124, 60 + y_bob], fill=glow_color)

        elif mech_type == "oberon":
            # Rear view of JCC-O08 Oberon
            # Fleet escort legs
            draw.polygon([(52 + x_shift, 144 + y_bob), (46, 110 + y_bob), (64, 110 + y_bob), (68 + x_shift, 144 + y_bob)], fill=(25, 40, 62, 255))
            draw.polygon([(92 - x_shift, 144 + y_bob), (96, 110 + y_bob), (114, 110 + y_bob), (108 - x_shift, 144 + y_bob)], fill=(25, 40, 62, 255))
            # Rear view of shoulder Point-Defense turrets
            draw.rounded_rectangle([32, 60 + y_bob, 52, 85 + y_bob], radius=4, fill=(35, 52, 80, 255), outline=accent_color)
            draw.rounded_rectangle([108, 60 + y_bob, 128, 85 + y_bob], radius=4, fill=(35, 52, 80, 255), outline=accent_color)
            # Heavy fleet generator backpack
            draw.polygon([(60, 64 + y_bob), (100, 64 + y_bob), (94, 112 + y_bob), (66, 112 + y_bob)], fill=base_color, outline=accent_color, width=2)
            draw.rounded_rectangle([68, 70 + y_bob, 92, 102 + y_bob], radius=4, fill=(20, 30, 48, 255), outline=(240, 210, 80, 255))
            draw.circle((80, 86 + y_bob), 6, fill=glow_color)
            # Thermal beam lance mounting bracket
            draw.line([120, 22 + y_bob, 120, 138 + y_bob], fill=(160, 180, 210, 255), width=3)

        elif mech_type == "gorgon":
            # Rear view of ARC-G04 Gorgon
            # Heavy stomping legs
            draw.polygon([(46 + x_shift, 146 + y_bob), (40, 108 + y_bob), (62, 108 + y_bob), (68 + x_shift, 146 + y_bob)], fill=(45, 30, 24, 255))
            draw.polygon([(92 - x_shift, 146 + y_bob), (98, 108 + y_bob), (120, 108 + y_bob), (114 - x_shift, 146 + y_bob)], fill=(45, 30, 24, 255))
            # Chunky scrap torso back with pneumatic accumulator tanks
            draw.rectangle([52, 65 + y_bob, 108, 112 + y_bob], fill=base_color, outline=accent_color, width=2)
            # Dual pneumatic pressure tanks for claw
            draw.rounded_rectangle([60, 72 + y_bob, 76, 104 + y_bob], radius=4, fill=(60, 40, 32, 255), outline=glow_color)
            draw.rounded_rectangle([84, 72 + y_bob, 100, 104 + y_bob], radius=4, fill=(60, 40, 32, 255), outline=glow_color)
            # Pressure hoses running to claw
            draw.line([60, 88 + y_bob, 38, 88 + y_bob], fill=(220, 160, 40, 255), width=2)
            # Rear of claw
            draw.polygon([(26, 68 + y_bob), (44, 72 + y_bob), (40, 105 + y_bob), (22, 110 + y_bob)], fill=(130, 35, 28, 255))
            # Rear of pile driver ram
            draw.rectangle([112, 70 + y_bob, 134, 115 + y_bob], fill=(55, 42, 38, 255))

        elif mech_type == "bloodhound":
            # Rear view of ARC-B06 Bloodhound
            # Rear wheels and axles (prominent)
            draw.polygon([(50 + x_shift, 140 + y_bob), (44, 112 + y_bob), (60, 112 + y_bob), (64 + x_shift, 140 + y_bob)], fill=(50, 35, 28, 255))
            draw.polygon([(96 - x_shift, 140 + y_bob), (100, 112 + y_bob), (116, 112 + y_bob), (110 - x_shift, 140 + y_bob)], fill=(50, 35, 28, 255))
            draw.ellipse([46 + x_shift, 134 + y_bob, 66 + x_shift, 150 + y_bob], fill=(20, 18, 16, 255), outline=(70, 50, 40, 255), width=2)
            draw.ellipse([94 - x_shift, 134 + y_bob, 114 - x_shift, 150 + y_bob], fill=(20, 18, 16, 255), outline=(70, 50, 40, 255), width=2)
            # Scrap chassis back with engine manifold
            draw.polygon([(54, 72 + y_bob), (106, 72 + y_bob), (98, 114 + y_bob), (62, 114 + y_bob)], fill=base_color, outline=accent_color, width=2)
            draw.rectangle([68, 76 + y_bob, 92, 102 + y_bob], fill=(35, 25, 20, 255), outline=(60, 45, 35, 255))
            # Quad rocket pod back blast hatches
            draw.rectangle([62, 40 + y_bob, 98, 60 + y_bob], fill=(55, 38, 30, 255), outline=(28, 18, 14, 255), width=2)
            draw.line([64, 50 + y_bob, 96, 50 + y_bob], fill=(20, 14, 10, 255), width=1)
            draw.line([80, 42 + y_bob, 80, 58 + y_bob], fill=(20, 14, 10, 255), width=1)

        elif mech_type == "vandal":
            # Rear view of ARC-V03 Vandal
            draw.polygon([(46 + x_shift, 146 + y_bob), (42, 112 + y_bob), (62, 112 + y_bob), (66 + x_shift, 146 + y_bob)], fill=(42, 32, 26, 255))
            draw.polygon([(94 - x_shift, 146 + y_bob), (98, 112 + y_bob), (118, 112 + y_bob), (114 - x_shift, 146 + y_bob)], fill=(42, 32, 26, 255))
            # Torso with welded rebar and hip jump-jets
            draw.polygon([(56, 68 + y_bob), (104, 68 + y_bob), (98, 114 + y_bob), (62, 114 + y_bob)], fill=base_color, outline=accent_color, width=2)
            draw.rectangle([48, 85 + y_bob, 56, 102 + y_bob], fill=(30, 22, 18, 255)) # Hip jet
            draw.rectangle([104, 85 + y_bob, 112, 102 + y_bob], fill=(30, 22, 18, 255))
            # Back of barricade shield (welded rebar handles)
            draw.polygon([(24, 62 + y_bob), (44, 56 + y_bob), (48, 134 + y_bob), (20, 128 + y_bob)], fill=(90, 40, 32, 255), outline=(30, 15, 12, 255), width=2)
            draw.line([28, 85 + y_bob, 40, 85 + y_bob], fill=(160, 140, 80, 255), width=2)
            draw.line([28, 105 + y_bob, 40, 105 + y_bob], fill=(160, 140, 80, 255), width=2)

        elif mech_type == "kage":
            # Rear view of ZBT-K07 Kage
            # Articulated stealth legs
            draw.polygon([(52 + x_shift, 144 + y_bob), (44, 112 + y_bob), (58, 112 + y_bob), (64 + x_shift, 144 + y_bob)], fill=(22, 18, 30, 255))
            draw.polygon([(96 - x_shift, 144 + y_bob), (102, 112 + y_bob), (116, 112 + y_bob), (108 - x_shift, 144 + y_bob)], fill=(22, 18, 30, 255))
            # Diamond stealth torso back with heat sink dissipation gills
            draw.polygon([(80, 50 + y_bob), (106, 75 + y_bob), (96, 112 + y_bob), (64, 112 + y_bob), (54, 75 + y_bob)], fill=base_color, outline=accent_color, width=2)
            for gy in range(68, 98, 6):
                draw.line([70, gy + y_bob, 90, gy + y_bob], fill=glow_color if (i == 1) else (40, 30, 52, 255), width=1)
            # Rear of needle rifle
            draw.rectangle([110, 42 + y_bob, 118, 115 + y_bob], fill=(35, 28, 48, 255), outline=glow_color)

        elif mech_type == "ronin":
            # Rear view of ZBT-R04 Ronin
            # Samurai legs with rear sode armor
            draw.polygon([(52 + x_shift, 144 + y_bob), (46, 112 + y_bob), (62, 112 + y_bob), (66 + x_shift, 144 + y_bob)], fill=(25, 20, 32, 255))
            draw.polygon([(94 - x_shift, 144 + y_bob), (98, 112 + y_bob), (114, 112 + y_bob), (108 - x_shift, 144 + y_bob)], fill=(25, 20, 32, 255))
            # Torso back with dual drone dock cradles
            draw.polygon([(58, 66 + y_bob), (102, 66 + y_bob), (96, 112 + y_bob), (64, 112 + y_bob)], fill=base_color, outline=accent_color, width=2)
            # Rear kabuto nape armor (shikoro)
            draw.polygon([(68, 54 + y_bob), (92, 54 + y_bob), (96, 68 + y_bob), (64, 68 + y_bob)], fill=(20, 15, 28, 255), outline=(240, 200, 60, 255))
            # 2 Drones in rear cradle/hovering
            d_bob = 3 if i % 2 == 1 else -3
            draw.polygon([(26, 54 + d_bob), (38, 44 + d_bob), (46, 58 + d_bob), (34, 68 + d_bob)], fill=(38, 24, 52, 255), outline=glow_color)
            draw.polygon([(134, 54 - d_bob), (122, 44 - d_bob), (114, 58 - d_bob), (126, 68 - d_bob)], fill=(38, 24, 52, 255), outline=glow_color)
            # Naginata scabbard across back
            draw.line([48, 135 + y_bob, 118, 25 + y_bob], fill=(140, 120, 160, 255), width=2)

        elif mech_type == "tessen":
            # Rear view of ZBT-T09 Tessen
            draw.polygon([(52 + x_shift, 142 + y_bob), (46, 110 + y_bob), (62, 110 + y_bob), (66 + x_shift, 142 + y_bob)], fill=(28, 20, 38, 255))
            draw.polygon([(94 - x_shift, 142 + y_bob), (98, 110 + y_bob), (114, 110 + y_bob), (108 - x_shift, 142 + y_bob)], fill=(28, 20, 38, 255))
            # Bladed war-fan wings spread from behind
            fan_spread = 4 if (i == 1 or i == 3) else 0
            draw.polygon([(20 - fan_spread, 48 + y_bob), (54, 75 + y_bob), (30 - fan_spread, 85 + y_bob)], fill=accent_color, outline=glow_color)
            draw.polygon([(16 - fan_spread, 68 + y_bob), (54, 75 + y_bob), (24 - fan_spread, 102 + y_bob)], fill=(40, 28, 55, 255), outline=glow_color)
            draw.polygon([(140 + fan_spread, 48 + y_bob), (106, 75 + y_bob), (130 + fan_spread, 85 + y_bob)], fill=accent_color, outline=glow_color)
            draw.polygon([(144 + fan_spread, 68 + y_bob), (106, 75 + y_bob), (136 + fan_spread, 102 + y_bob)], fill=(40, 28, 55, 255), outline=glow_color)
            # EMP transformer coil core on spine
            draw.polygon([(62, 65 + y_bob), (98, 65 + y_bob), (92, 110 + y_bob), (68, 110 + y_bob)], fill=base_color, outline=accent_color, width=2)
            draw.circle((80, 84 + y_bob), 8, fill=(60, 35, 90, 255), outline=glow_color)

        elif mech_type == "hephaestus_avatar":
            # Rear view of Pre-War Flagship Autonomous Avatar
            draw.polygon([(48 + x_shift, 146 + y_bob), (42, 108 + y_bob), (64, 108 + y_bob), (68 + x_shift, 146 + y_bob)], fill=(22, 30, 44, 255))
            draw.polygon([(92 - x_shift, 146 + y_bob), (96, 108 + y_bob), (118, 108 + y_bob), (112 - x_shift, 146 + y_bob)], fill=(22, 30, 44, 255))
            # Dreadnought heavy backplate with Cherenkov Reactor Exhaust Vanes
            draw.polygon([(54, 64 + y_bob), (106, 64 + y_bob), (98, 110 + y_bob), (62, 110 + y_bob)], fill=base_color, outline=(240, 215, 80, 255), width=2)
            c_rad = 12 if (i == 1 or i == 3) else 9
            draw.circle((80, 86 + y_bob), c_rad, fill=(0, 240, 255, 220), outline=(255, 255, 255, 255))
            # Broadsword scabbard across back
            draw.rectangle([112, 40 + y_bob, 122, 120 + y_bob], fill=(30, 42, 60, 255), outline=(0, 240, 255, 255))

        elif mech_type == "titan":
            # Rear view of Valkyrie Heavy Dynamics Apex Titan
            # Massive pillar legs
            draw.rectangle([38 + x_shift, 105 + y_bob, 66 + x_shift, 148 + y_bob], fill=(35, 38, 34, 255), outline=(15, 18, 15, 255), width=2)
            draw.rectangle([94 - x_shift, 105 + y_bob, 122 - x_shift, 148 + y_bob], fill=(35, 38, 34, 255), outline=(15, 18, 15, 255), width=2)
            # Massive bunker bulkhead back
            draw.rectangle([44, 60 + y_bob, 116, 110 + y_bob], fill=base_color, outline=accent_color, width=3)
            # Dual diesel-turbine exhaust stacks
            draw.rectangle([56, 42 + y_bob, 68, 62 + y_bob], fill=(25, 28, 24, 255), outline=accent_color)
            draw.rectangle([92, 42 + y_bob, 104, 62 + y_bob], fill=(25, 28, 24, 255), outline=accent_color)
            if i == 1 or i == 3:
                draw.ellipse([54, 30, 70, 44], fill=(100, 100, 100, 140))
                draw.ellipse([90, 30, 106, 44], fill=(100, 100, 100, 140))
            # Rear drum ammo magazines for autocannons
            draw.ellipse([18, 70 + y_bob, 36, 100 + y_bob], fill=(45, 50, 42, 255), outline=accent_color)
            draw.ellipse([124, 70 + y_bob, 142, 100 + y_bob], fill=(45, 50, 42, 255), outline=accent_color)

        main_png = os.path.join(spr_path, f"{f_uuid}.png")
        im.save(main_png, "PNG")
        layer_dir = os.path.join(layers_path, f_uuid)
        os.makedirs(layer_dir, exist_ok=True)
        layer_png = os.path.join(layer_dir, f"{layer_id}.png")
        im.save(layer_png, "PNG")

    yy_data = {
        "$GMSprite": "v2",
        "%Name": sprite_name,
        "bboxMode": 0,
        "bbox_bottom": 154,
        "bbox_left": 16,
        "bbox_right": 146,
        "bbox_top": 8,
        "collisionKind": 1,
        "collisionTolerance": 0,
        "DynamicTexturePage": False,
        "edgeFiltering": False,
        "For3D": False,
        "frames": [
            {
                "$GMSpriteFrame": "v1",
                "%Name": f_uuid,
                "name": f_uuid,
                "resourceType": "GMSpriteFrame",
                "resourceVersion": "2.0"
            }
            for f_uuid in frame_uuids
        ],
        "gridX": 0,
        "gridY": 0,
        "height": 160,
        "HTile": False,
        "layers": [
            {
                "$GMImageLayer": "",
                "%Name": layer_id,
                "blendMode": 0,
                "displayName": "default",
                "isLocked": False,
                "name": layer_id,
                "opacity": 100.0,
                "resourceType": "GMImageLayer",
                "resourceVersion": "2.0",
                "visible": True
            }
        ],
        "name": sprite_name,
        "nineSlice": None,
        "origin": 0,
        "parent": {
            "name": "MechMakerConcept",
            "path": "MechMakerConcept.yyp"
        },
        "preMultiplyAlpha": False,
        "resourceType": "GMSprite",
        "resourceVersion": "2.0",
        "sequence": {
            "$GMSequence": "v1",
            "%Name": sprite_name,
            "autoRecord": True,
            "backdropHeight": 768,
            "backdropImageOpacity": 0.5,
            "backdropImagePath": "",
            "backdropWidth": 1366,
            "backdropXOffset": 0.0,
            "backdropYOffset": 0.0,
            "events": {
                "$KeyframeStore<MessageEventKeyframe>": "",
                "Keyframes": [],
                "resourceType": "KeyframeStore<MessageEventKeyframe>",
                "resourceVersion": "2.0"
            },
            "eventStubScript": None,
            "eventToFunction": {},
            "length": 4.0,
            "lockOrigin": False,
            "moments": {
                "$KeyframeStore<MomentsEventKeyframe>": "",
                "Keyframes": [],
                "resourceType": "KeyframeStore<MomentsEventKeyframe>",
                "resourceVersion": "2.0"
            },
            "name": sprite_name,
            "playback": 1,
            "playbackSpeed": 6.0,
            "playbackSpeedType": 0,
            "resourceType": "GMSequence",
            "resourceVersion": "2.0",
            "showBackdrop": True,
            "showBackdropImage": False,
            "timeUnits": 1,
            "tracks": [
                {
                    "$GMSpriteFramesTrack": "",
                    "builtinName": 0,
                    "events": [],
                    "inheritsTrackColour": True,
                    "interpolation": 1,
                    "isCreationTrack": False,
                    "keyframes": {
                        "$KeyframeStore<SpriteFrameKeyframe>": "",
                        "Keyframes": [
                            {
                                "$Keyframe<SpriteFrameKeyframe>": "",
                                "Channels": {
                                    "0": {
                                        "$SpriteFrameKeyframe": "",
                                        "Id": {
                                            "name": f_uuid,
                                            "path": f"sprites/{sprite_name}/{sprite_name}.yy"
                                        },
                                        "resourceType": "SpriteFrameKeyframe",
                                        "resourceVersion": "2.0"
                                    }
                                },
                                "Disabled": False,
                                "id": str(uuid.uuid4()),
                                "IsCreationKey": False,
                                "Key": float(k_idx),
                                "Length": 1.0,
                                "resourceType": "Keyframe<SpriteFrameKeyframe>",
                                "resourceVersion": "2.0",
                                "Stretch": False
                            }
                            for k_idx, f_uuid in enumerate(frame_uuids)
                        ],
                        "resourceType": "KeyframeStore<SpriteFrameKeyframe>",
                        "resourceVersion": "2.0"
                    },
                    "modifiers": [],
                    "name": "frames",
                    "resourceType": "GMSpriteFramesTrack",
                    "resourceVersion": "2.0",
                    "spriteId": None,
                    "trackColour": 0,
                    "tracks": [],
                    "traits": 0
                }
            ],
            "visibleRange": None,
            "volume": 1.0,
            "xorigin": 80,
            "yorigin": 145
        },
        "swatchColours": None,
        "swfPrecision": 2.525,
        "textureGroupId": {
            "name": "Default",
            "path": "texturegroups/Default"
        },
        "type": 0,
        "VTile": False,
        "width": 160
    }

    with open(os.path.join(spr_path, f"{sprite_name}.yy"), "w") as f:
        json.dump(yy_data, f, indent=2)

    print(f"Created back sprite: {sprite_name}")

back_sprites_to_build = [
    # Terran Candidates Back
    ("spr_ms_ballista_back_idle", (68, 78, 62, 255), (105, 120, 95, 255), (255, 120, 40, 255), "ballista"),
    ("spr_ms_centurion_back_idle", (64, 76, 60, 255), (105, 125, 98, 255), (255, 140, 40, 255), "centurion"),
    ("spr_ms_trenchcoat_back_idle", (52, 58, 64, 255), (88, 98, 108, 255), (240, 160, 50, 255), "trenchcoat"),
    # Colony Candidates Back
    ("spr_ms_zephyr_back_idle", (38, 70, 115, 255), (85, 145, 220, 255), (0, 240, 255, 255), "zephyr"),
    ("spr_ms_kepler_back_idle", (36, 55, 88, 255), (70, 120, 185, 255), (0, 230, 255, 255), "kepler"),
    ("spr_ms_oberon_back_idle", (42, 68, 110, 255), (90, 145, 220, 255), (0, 240, 255, 255), "oberon"),
    # Syndicate Candidates Back
    ("spr_ms_gorgon_back_idle", (135, 55, 40, 255), (185, 80, 50, 255), (255, 160, 40, 255), "gorgon"),
    ("spr_ms_bloodhound_back_idle", (125, 50, 36, 255), (175, 75, 45, 255), (255, 90, 30, 255), "bloodhound"),
    ("spr_ms_vandal_back_idle", (110, 45, 38, 255), (160, 70, 55, 255), (240, 180, 40, 255), "vandal"),
    # Zaibatsu Candidates Back
    ("spr_ms_kage_back_idle", (24, 18, 32, 255), (65, 45, 85, 255), (0, 255, 200, 255), "kage"),
    ("spr_ms_ronin_back_idle", (26, 20, 35, 255), (65, 42, 85, 255), (0, 255, 200, 255), "ronin"),
    ("spr_ms_tessen_back_idle", (32, 22, 45, 255), (75, 50, 105, 255), (180, 80, 255, 255), "tessen"),
    # Apex & Flagship Prototypes Back
    ("spr_ms_hephaestus_avatar_back_idle", (32, 45, 70, 255), (240, 215, 80, 255), (0, 240, 255, 255), "hephaestus_avatar"),
    ("spr_ms_titan_proto_back_idle", (55, 62, 52, 255), (95, 110, 90, 255), (255, 180, 40, 255), "titan")
]

for spr_id, b_col, a_col, g_col, m_type in back_sprites_to_build:
    create_back_mech_sprite(spr_id, b_col, a_col, g_col, m_type)

with open(YYP_PATH, "r") as f:
    yyp_content = f.read()

for spr_id, _, _, _, _ in back_sprites_to_build:
    spr_path = f"sprites/{spr_id}/{spr_id}.yy"
    res_entry = f"{{\"id\":{{\"name\":\"{spr_id}\",\"path\":\"{spr_path}\",}},}},"
    if spr_id not in yyp_content:
        marker = '"resources": ['
        idx = yyp_content.find(marker)
        if idx != -1:
            insert_pos = idx + len(marker)
            yyp_content = yyp_content[:insert_pos] + f"\n    {res_entry}" + yyp_content[insert_pos:]
            print(f"Registered {spr_id} in MechMakerConcept.yyp")

with open(YYP_PATH, "w") as f:
    f.write(yyp_content)

print(f"All {len(back_sprites_to_build)} BACK-FACING isometric sprites successfully created and registered!")
