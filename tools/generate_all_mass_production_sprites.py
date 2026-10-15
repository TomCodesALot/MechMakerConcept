import os
import json
import uuid
from PIL import Image, ImageDraw

SPRITES_DIR = "sprites"
YYP_PATH = "MechMakerConcept.yyp"

def create_advanced_mech_sprite(sprite_name, base_color, accent_color, glow_color, mech_type):
    spr_path = os.path.join(SPRITES_DIR, sprite_name)
    layers_path = os.path.join(spr_path, "layers")
    os.makedirs(spr_path, exist_ok=True)
    os.makedirs(layers_path, exist_ok=True)

    layer_id = str(uuid.uuid4())
    frame_uuids = [str(uuid.uuid4()) for _ in range(4)]
    
    # Generate 4 distinct animation frames (160x160)
    for i, f_uuid in enumerate(frame_uuids):
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        
        # Ground shadow
        draw.ellipse([30, 142, 130, 154], fill=(0, 0, 0, 95))
        
        # Idle / walk bob offsets
        y_bob = -2 if (i == 1 or i == 3) else 0
        x_shift = 1 if i == 2 else (-1 if i == 3 else 0)
        
        if mech_type == "centurion":
            # TH-C02 Centurion: Heavy Linebreaker with Tower Riot Shield & Rotary Vulcan
            draw.polygon([(46 + x_shift, 146 + y_bob), (42, 110 + y_bob), (62, 110 + y_bob), (66 + x_shift, 146 + y_bob)], fill=(50, 58, 48, 255))
            draw.polygon([(94 - x_shift, 146 + y_bob), (98, 110 + y_bob), (118, 110 + y_bob), (114 - x_shift, 146 + y_bob)], fill=(50, 58, 48, 255))
            draw.rectangle([44, 116 + y_bob, 64, 126 + y_bob], fill=accent_color)
            draw.rectangle([96, 116 + y_bob, 116, 126 + y_bob], fill=accent_color)
            draw.polygon([(56, 68 + y_bob), (104, 68 + y_bob), (100, 112 + y_bob), (60, 112 + y_bob)], fill=base_color, outline=accent_color, width=2)
            draw.rectangle([70, 50 + y_bob, 90, 68 + y_bob], fill=(38, 45, 36, 255), outline=accent_color)
            draw.polygon([(78, 40 + y_bob), (82, 40 + y_bob), (84, 50 + y_bob), (76, 50 + y_bob)], fill=accent_color)
            draw.line([73, 58 + y_bob, 87, 58 + y_bob], fill=glow_color, width=2)
            # Tower Shield on Left Arm
            draw.polygon([(20, 58 + y_bob), (44, 52 + y_bob), (48, 134 + y_bob), (24, 140 + y_bob)], fill=(65, 75, 62, 255), outline=(30, 36, 28, 255), width=2)
            draw.line([32, 60 + y_bob, 36, 132 + y_bob], fill=accent_color, width=3)
            draw.rectangle([28, 88 + y_bob, 40, 96 + y_bob], fill=glow_color)
            # GAU-88 Rotary Vulcan on Right Arm
            rot_off = 2 if i % 2 == 1 else 0
            draw.rectangle([106, 75 + y_bob, 126, 92 + y_bob], fill=(40, 48, 38, 255))
            draw.rectangle([112, 92 + y_bob, 120, 128 + y_bob], fill=(60, 68, 58, 255), outline=(20, 25, 20, 255))
            draw.line([115 + rot_off, 92 + y_bob, 115 + rot_off, 128 + y_bob], fill=(120, 130, 115, 255), width=1)
            draw.line([118 - rot_off, 92 + y_bob, 118 - rot_off, 128 + y_bob], fill=(120, 130, 115, 255), width=1)
            if i == 3:
                draw.polygon([(110, 128 + y_bob), (116, 148 + y_bob), (122, 128 + y_bob)], fill=(255, 220, 80, 240))
                draw.ellipse([112, 130 + y_bob, 120, 140 + y_bob], fill=(255, 255, 255, 255))

        elif mech_type == "trenchcoat":
            # TH-T09 Trenchcoat: Ballistic Skirts & Heavy Slugger
            draw.polygon([(44 + x_shift, 146 + y_bob), (40, 115 + y_bob), (60, 115 + y_bob), (64 + x_shift, 146 + y_bob)], fill=(40, 44, 48, 255))
            draw.polygon([(96 - x_shift, 146 + y_bob), (100, 115 + y_bob), (120, 115 + y_bob), (116 - x_shift, 146 + y_bob)], fill=(40, 44, 48, 255))
            draw.polygon([(36, 92 + y_bob), (54, 88 + y_bob), (50, 130 + y_bob), (32, 126 + y_bob)], fill=(55, 62, 68, 255), outline=(25, 30, 35, 255))
            draw.polygon([(106, 88 + y_bob), (124, 92 + y_bob), (128, 126 + y_bob), (110, 130 + y_bob)], fill=(55, 62, 68, 255), outline=(25, 30, 35, 255))
            draw.polygon([(52, 94 + y_bob), (108, 94 + y_bob), (104, 128 + y_bob), (56, 128 + y_bob)], fill=(48, 54, 60, 255), outline=(25, 30, 35, 255))
            draw.rectangle([54, 68 + y_bob, 106, 98 + y_bob], fill=base_color, outline=accent_color, width=2)
            draw.rectangle([70, 52 + y_bob, 90, 68 + y_bob], fill=(30, 34, 38, 255), outline=accent_color)
            draw.ellipse([73, 56 + y_bob, 79, 62 + y_bob], fill=glow_color)
            draw.ellipse([81, 56 + y_bob, 87, 62 + y_bob], fill=glow_color)
            draw.rectangle([76, 62 + y_bob, 84, 67 + y_bob], fill=(20, 22, 25, 255))
            draw.rectangle([48, 45 + y_bob, 54, 65 + y_bob], fill=(35, 38, 42, 255))
            draw.rectangle([106, 45 + y_bob, 112, 65 + y_bob], fill=(35, 38, 42, 255))
            if i == 1:
                draw.ellipse([45, 35, 57, 45], fill=(160, 160, 160, 120))
                draw.ellipse([103, 35, 115, 45], fill=(160, 160, 160, 120))
            draw.polygon([(64, 85 + y_bob), (126, 80 + y_bob), (124, 94 + y_bob), (62, 99 + y_bob)], fill=(50, 55, 60, 255))
            draw.rectangle([122, 78 + y_bob, 136, 88 + y_bob], fill=(70, 75, 80, 255))
            draw.ellipse([88, 92 + y_bob, 102, 104 + y_bob], fill=(85, 45, 30, 255))
            if i == 3:
                draw.polygon([(136, 83 + y_bob), (155, 72 + y_bob), (155, 94 + y_bob)], fill=(255, 160, 40, 230))
                draw.polygon([(136, 83 + y_bob), (148, 77 + y_bob), (148, 89 + y_bob)], fill=(255, 240, 180, 255))

        elif mech_type == "kepler":
            # JCC-K02 Kepler: Linear Rail-Sniper
            draw.polygon([(54 + x_shift, 142 + y_bob), (48, 108 + y_bob), (64, 108 + y_bob), (68 + x_shift, 142 + y_bob)], fill=(32, 45, 68, 255))
            draw.polygon([(92 - x_shift, 142 + y_bob), (96, 108 + y_bob), (112, 108 + y_bob), (106 - x_shift, 142 + y_bob)], fill=(32, 45, 68, 255))
            draw.polygon([(18, 50 + y_bob), (50, 65 + y_bob), (46, 85 + y_bob), (16, 75 + y_bob)], fill=accent_color, outline=(20, 30, 50, 255))
            draw.polygon([(142, 50 + y_bob), (110, 65 + y_bob), (114, 85 + y_bob), (144, 75 + y_bob)], fill=accent_color, outline=(20, 30, 50, 255))
            draw.polygon([(80, 48 + y_bob), (104, 72 + y_bob), (96, 110 + y_bob), (64, 110 + y_bob), (56, 72 + y_bob)], fill=base_color, outline=accent_color, width=2)
            draw.polygon([(72, 46 + y_bob), (88, 46 + y_bob), (86, 60 + y_bob), (74, 60 + y_bob)], fill=(24, 34, 52, 255))
            draw.rectangle([75, 50 + y_bob, 85, 55 + y_bob], fill=glow_color)
            draw.rectangle([112, 24 + y_bob, 122, 138 + y_bob], fill=(45, 60, 85, 255), outline=(15, 22, 35, 255), width=2)
            for by in range(35, 125, 18):
                draw.rectangle([110, by + y_bob, 124, by + 6 + y_bob], fill=glow_color)
            if i == 3:
                draw.line([117, 138 + y_bob, 117, 158 + y_bob], fill=(120, 240, 255, 255), width=4)
                draw.ellipse([110, 134 + y_bob, 124, 144 + y_bob], fill=(255, 255, 255, 255))

        elif mech_type == "oberon":
            # JCC-O08 Oberon: Fleet Escort Guardian
            draw.polygon([(52 + x_shift, 144 + y_bob), (46, 110 + y_bob), (64, 110 + y_bob), (68 + x_shift, 144 + y_bob)], fill=(30, 48, 72, 255))
            draw.polygon([(92 - x_shift, 144 + y_bob), (96, 110 + y_bob), (114, 110 + y_bob), (108 - x_shift, 144 + y_bob)], fill=(30, 48, 72, 255))
            draw.rounded_rectangle([32, 60 + y_bob, 52, 85 + y_bob], radius=4, fill=(40, 62, 95, 255), outline=accent_color)
            draw.ellipse([38, 68 + y_bob, 46, 76 + y_bob], fill=glow_color)
            draw.rounded_rectangle([108, 60 + y_bob, 128, 85 + y_bob], radius=4, fill=(40, 62, 95, 255), outline=accent_color)
            draw.ellipse([114, 68 + y_bob, 122, 76 + y_bob], fill=glow_color)
            draw.polygon([(60, 65 + y_bob), (100, 65 + y_bob), (94, 112 + y_bob), (66, 112 + y_bob)], fill=base_color, outline=accent_color, width=2)
            draw.polygon([(74, 78 + y_bob), (86, 78 + y_bob), (80, 94 + y_bob)], fill=(240, 210, 80, 255))
            draw.rectangle([72, 48 + y_bob, 88, 64 + y_bob], fill=(22, 35, 55, 255), outline=accent_color)
            draw.line([80, 36 + y_bob, 80, 48 + y_bob], fill=(240, 210, 80, 255), width=2)
            draw.line([74, 55 + y_bob, 86, 55 + y_bob], fill=glow_color, width=2)
            draw.line([120, 22 + y_bob, 120, 138 + y_bob], fill=(200, 220, 240, 255), width=3)
            draw.polygon([(115, 22 + y_bob), (120, 8 + y_bob), (125, 22 + y_bob)], fill=glow_color)
            draw.polygon([(24, 72 + y_bob), (36, 66 + y_bob), (42, 114 + y_bob), (30, 118 + y_bob)], fill=(60, 95, 140, 200), outline=glow_color)

        elif mech_type == "bloodhound":
            # ARC-B06 Bloodhound: Wheeled Pack Hunter
            draw.polygon([(50 + x_shift, 140 + y_bob), (44, 112 + y_bob), (60, 112 + y_bob), (64 + x_shift, 140 + y_bob)], fill=(60, 42, 35, 255))
            draw.polygon([(96 - x_shift, 140 + y_bob), (100, 112 + y_bob), (116, 112 + y_bob), (110 - x_shift, 140 + y_bob)], fill=(60, 42, 35, 255))
            draw.ellipse([46 + x_shift, 134 + y_bob, 66 + x_shift, 150 + y_bob], fill=(25, 22, 20, 255), outline=(80, 60, 50, 255), width=2)
            draw.ellipse([94 - x_shift, 134 + y_bob, 114 - x_shift, 150 + y_bob], fill=(25, 22, 20, 255), outline=(80, 60, 50, 255), width=2)
            draw.polygon([(54, 72 + y_bob), (106, 72 + y_bob), (98, 114 + y_bob), (62, 114 + y_bob)], fill=base_color, outline=accent_color, width=2)
            draw.polygon([(68, 60 + y_bob), (92, 60 + y_bob), (88, 74 + y_bob), (72, 74 + y_bob)], fill=(45, 30, 25, 255))
            draw.rectangle([72, 64 + y_bob, 77, 69 + y_bob], fill=glow_color)
            draw.rectangle([83, 64 + y_bob, 88, 69 + y_bob], fill=glow_color)
            draw.rectangle([62, 40 + y_bob, 98, 60 + y_bob], fill=(70, 45, 38, 255), outline=(35, 22, 18, 255), width=2)
            draw.ellipse([65, 43 + y_bob, 72, 50 + y_bob], fill=(240, 140, 40, 255))
            draw.ellipse([75, 43 + y_bob, 82, 50 + y_bob], fill=(240, 140, 40, 255))
            draw.ellipse([65, 51 + y_bob, 72, 58 + y_bob], fill=(240, 140, 40, 255))
            draw.ellipse([75, 51 + y_bob, 82, 58 + y_bob], fill=(240, 140, 40, 255))
            if i == 3:
                draw.polygon([(78, 38 + y_bob), (74, 18 + y_bob), (82, 18 + y_bob)], fill=(255, 180, 60, 240))
                draw.ellipse([70, 26 + y_bob, 86, 40 + y_bob], fill=(180, 150, 120, 180))
            draw.rectangle([108, 85 + y_bob, 128, 100 + y_bob], fill=(50, 38, 32, 255))
            draw.line([128, 92 + y_bob, 138, 92 + y_bob], fill=(90, 75, 65, 255), width=2)

        elif mech_type == "vandal":
            # ARC-V03 Vandal: Street Ambush Mecha
            draw.polygon([(46 + x_shift, 146 + y_bob), (42, 112 + y_bob), (62, 112 + y_bob), (66 + x_shift, 146 + y_bob)], fill=(50, 38, 32, 255))
            draw.polygon([(94 - x_shift, 146 + y_bob), (98, 112 + y_bob), (118, 112 + y_bob), (114 - x_shift, 146 + y_bob)], fill=(50, 38, 32, 255))
            draw.polygon([(22, 60 + y_bob), (44, 52 + y_bob), (48, 136 + y_bob), (18, 130 + y_bob)], fill=(120, 50, 40, 255), outline=(40, 20, 15, 255), width=2)
            draw.line([22, 85 + y_bob, 46, 85 + y_bob], fill=(220, 180, 40, 255), width=3)
            draw.line([22, 105 + y_bob, 46, 105 + y_bob], fill=(220, 180, 40, 255), width=3)
            draw.polygon([(56, 68 + y_bob), (104, 68 + y_bob), (98, 114 + y_bob), (62, 114 + y_bob)], fill=base_color, outline=accent_color, width=2)
            draw.rectangle([72, 54 + y_bob, 88, 68 + y_bob], fill=(38, 28, 24, 255), outline=accent_color)
            draw.line([74, 60 + y_bob, 86, 60 + y_bob], fill=glow_color, width=2)
            draw.rectangle([106, 80 + y_bob, 132, 96 + y_bob], fill=(55, 42, 35, 255))
            draw.polygon([(132, 82 + y_bob), (142, 76 + y_bob), (142, 102 + y_bob), (132, 94 + y_bob)], fill=(75, 60, 50, 255))
            if i == 3:
                for fy in [-6, 0, 6]:
                    draw.line([142, 89 + y_bob + fy, 156, int(89 + y_bob + fy * 1.5)], fill=(255, 200, 80, 240), width=1)
            draw.rectangle([98, 52 + y_bob, 106, 68 + y_bob], fill=(80, 40, 30, 255))

        elif mech_type == "ronin":
            # ZBT-R04 Ronin: Sub-Drone Carrier
            draw.polygon([(52 + x_shift, 144 + y_bob), (46, 112 + y_bob), (62, 112 + y_bob), (66 + x_shift, 144 + y_bob)], fill=(32, 24, 42, 255))
            draw.polygon([(94 - x_shift, 144 + y_bob), (98, 112 + y_bob), (114, 112 + y_bob), (108 - x_shift, 144 + y_bob)], fill=(32, 24, 42, 255))
            draw.polygon([(58, 66 + y_bob), (102, 66 + y_bob), (96, 112 + y_bob), (64, 112 + y_bob)], fill=base_color, outline=accent_color, width=2)
            draw.rectangle([70, 50 + y_bob, 90, 66 + y_bob], fill=(25, 18, 35, 255), outline=accent_color)
            draw.polygon([(66, 40 + y_bob), (74, 50 + y_bob), (80, 44 + y_bob)], fill=(240, 200, 60, 255))
            draw.polygon([(94, 40 + y_bob), (86, 50 + y_bob), (80, 44 + y_bob)], fill=(240, 200, 60, 255))
            draw.line([74, 57 + y_bob, 86, 57 + y_bob], fill=glow_color, width=2)
            d_bob = 3 if i % 2 == 1 else -3
            draw.polygon([(24, 52 + d_bob), (36, 42 + d_bob), (44, 56 + d_bob), (32, 66 + d_bob)], fill=(45, 30, 60, 255), outline=glow_color)
            draw.ellipse([30, 50 + d_bob, 38, 58 + d_bob], fill=glow_color)
            draw.polygon([(136, 52 - d_bob), (124, 42 - d_bob), (116, 56 - d_bob), (128, 66 - d_bob)], fill=(45, 30, 60, 255), outline=glow_color)
            draw.ellipse([122, 50 - d_bob, 130, 58 - d_bob], fill=glow_color)
            draw.line([50, 140 + y_bob, 120, 20 + y_bob], fill=(180, 160, 200, 255), width=2)
            draw.polygon([(120, 20 + y_bob), (132, 10 + y_bob), (126, 32 + y_bob)], fill=glow_color)

        elif mech_type == "tessen":
            # ZBT-T09 Tessen: EMP Bladed War-Fans
            draw.polygon([(52 + x_shift, 142 + y_bob), (46, 110 + y_bob), (62, 110 + y_bob), (66 + x_shift, 142 + y_bob)], fill=(35, 25, 48, 255))
            draw.polygon([(94 - x_shift, 142 + y_bob), (98, 110 + y_bob), (114, 110 + y_bob), (108 - x_shift, 142 + y_bob)], fill=(35, 25, 48, 255))
            fan_spread = 4 if (i == 1 or i == 3) else 0
            draw.polygon([(20 - fan_spread, 48 + y_bob), (54, 75 + y_bob), (30 - fan_spread, 85 + y_bob)], fill=accent_color, outline=glow_color)
            draw.polygon([(16 - fan_spread, 68 + y_bob), (54, 75 + y_bob), (24 - fan_spread, 102 + y_bob)], fill=(50, 35, 70, 255), outline=glow_color)
            draw.polygon([(140 + fan_spread, 48 + y_bob), (106, 75 + y_bob), (130 + fan_spread, 85 + y_bob)], fill=accent_color, outline=glow_color)
            draw.polygon([(144 + fan_spread, 68 + y_bob), (106, 75 + y_bob), (136 + fan_spread, 102 + y_bob)], fill=(50, 35, 70, 255), outline=glow_color)
            draw.polygon([(62, 65 + y_bob), (98, 65 + y_bob), (92, 110 + y_bob), (68, 110 + y_bob)], fill=base_color, outline=accent_color, width=2)
            draw.rectangle([72, 48 + y_bob, 88, 64 + y_bob], fill=(28, 20, 40, 255), outline=accent_color)
            draw.line([74, 38 + y_bob, 74, 48 + y_bob], fill=glow_color, width=2)
            draw.line([86, 38 + y_bob, 86, 48 + y_bob], fill=glow_color, width=2)
            draw.ellipse([76, 52 + y_bob, 84, 60 + y_bob], fill=glow_color)
            draw.ellipse([44, 94 + y_bob, 56, 106 + y_bob], fill=(80, 50, 110, 255), outline=glow_color)
            draw.ellipse([104, 94 + y_bob, 116, 106 + y_bob], fill=(80, 50, 110, 255), outline=glow_color)
            if i == 3:
                draw.ellipse([36, 86 + y_bob, 64, 114 + y_bob], outline=glow_color, width=1)
                draw.ellipse([96, 86 + y_bob, 124, 114 + y_bob], outline=glow_color, width=1)

        elif mech_type == "hephaestus_avatar":
            # Pre-War Flagship Autonomous Avatar
            draw.polygon([(48 + x_shift, 146 + y_bob), (42, 108 + y_bob), (64, 108 + y_bob), (68 + x_shift, 146 + y_bob)], fill=(28, 38, 55, 255))
            draw.polygon([(92 - x_shift, 146 + y_bob), (96, 108 + y_bob), (118, 108 + y_bob), (112 - x_shift, 146 + y_bob)], fill=(28, 38, 55, 255))
            draw.line([46, 124 + y_bob, 64, 124 + y_bob], fill=(240, 215, 80, 255), width=2)
            draw.line([96, 124 + y_bob, 114, 124 + y_bob], fill=(240, 215, 80, 255), width=2)
            draw.polygon([(54, 64 + y_bob), (106, 64 + y_bob), (98, 110 + y_bob), (62, 110 + y_bob)], fill=base_color, outline=(240, 215, 80, 255), width=2)
            c_rad = 12 if (i == 1 or i == 3) else 9
            draw.circle((80, 86 + y_bob), c_rad, fill=(0, 240, 255, 230), outline=(255, 255, 255, 255))
            draw.polygon([(70, 46 + y_bob), (90, 46 + y_bob), (86, 64 + y_bob), (74, 64 + y_bob)], fill=(20, 28, 42, 255), outline=(240, 215, 80, 255))
            draw.polygon([(77, 34 + y_bob), (83, 34 + y_bob), (85, 46 + y_bob), (75, 46 + y_bob)], fill=(240, 215, 80, 255))
            draw.line([74, 54 + y_bob, 86, 54 + y_bob], fill=(0, 240, 255, 255), width=2)
            draw.rectangle([112, 40 + y_bob, 122, 120 + y_bob], fill=(220, 230, 245, 255), outline=(0, 240, 255, 255), width=2)
            draw.polygon([(112, 40 + y_bob), (117, 20 + y_bob), (122, 40 + y_bob)], fill=(0, 240, 255, 255))
            draw.polygon([(20, 58 + y_bob), (44, 52 + y_bob), (48, 126 + y_bob), (24, 132 + y_bob)], fill=(40, 58, 85, 255), outline=(240, 215, 80, 255), width=2)
            draw.circle((34, 90 + y_bob), 6, fill=(0, 240, 255, 255))

        elif mech_type == "titan":
            # Valkyrie Heavy Dynamics Apex Titan
            draw.rectangle([38 + x_shift, 105 + y_bob, 66 + x_shift, 148 + y_bob], fill=(42, 46, 40, 255), outline=(20, 24, 20, 255), width=2)
            draw.rectangle([94 - x_shift, 105 + y_bob, 122 - x_shift, 148 + y_bob], fill=(42, 46, 40, 255), outline=(20, 24, 20, 255), width=2)
            draw.rectangle([44, 60 + y_bob, 116, 110 + y_bob], fill=base_color, outline=accent_color, width=3)
            draw.line([50, 70 + y_bob, 65, 85 + y_bob], fill=(230, 180, 20, 255), width=3)
            draw.line([68, 70 + y_bob, 83, 85 + y_bob], fill=(230, 180, 20, 255), width=3)
            draw.line([86, 70 + y_bob, 101, 85 + y_bob], fill=(230, 180, 20, 255), width=3)
            draw.rectangle([68, 48 + y_bob, 92, 60 + y_bob], fill=(25, 28, 24, 255), outline=accent_color)
            draw.line([72, 54 + y_bob, 88, 54 + y_bob], fill=glow_color, width=2)
            draw.rectangle([18, 55 + y_bob, 26, 115 + y_bob], fill=(60, 65, 58, 255), outline=(20, 25, 20, 255), width=2)
            draw.rectangle([28, 55 + y_bob, 36, 115 + y_bob], fill=(60, 65, 58, 255), outline=(20, 25, 20, 255), width=2)
            draw.rectangle([124, 55 + y_bob, 132, 115 + y_bob], fill=(60, 65, 58, 255), outline=(20, 25, 20, 255), width=2)
            draw.rectangle([134, 55 + y_bob, 142, 115 + y_bob], fill=(60, 65, 58, 255), outline=(20, 25, 20, 255), width=2)
            if i == 3:
                draw.polygon([(16, 115 + y_bob), (22, 135 + y_bob), (28, 115 + y_bob)], fill=(255, 200, 50, 240))
                draw.polygon([(26, 115 + y_bob), (32, 135 + y_bob), (38, 115 + y_bob)], fill=(255, 200, 50, 240))
                draw.polygon([(122, 115 + y_bob), (128, 135 + y_bob), (134, 115 + y_bob)], fill=(255, 200, 50, 240))
                draw.polygon([(132, 115 + y_bob), (138, 135 + y_bob), (144, 115 + y_bob)], fill=(255, 200, 50, 240))

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
            "xorigin": 0,
            "yorigin": 0
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

    print(f"Created sprite: {sprite_name}")

sprites_to_build = [
    ("spr_ms_centurion_idle", (64, 76, 60, 255), (105, 125, 98, 255), (255, 140, 40, 255), "centurion"),
    ("spr_ms_trenchcoat_idle", (52, 58, 64, 255), (88, 98, 108, 255), (240, 160, 50, 255), "trenchcoat"),
    ("spr_ms_kepler_idle", (36, 55, 88, 255), (70, 120, 185, 255), (0, 230, 255, 255), "kepler"),
    ("spr_ms_oberon_idle", (42, 68, 110, 255), (90, 145, 220, 255), (0, 240, 255, 255), "oberon"),
    ("spr_ms_bloodhound_idle", (125, 50, 36, 255), (175, 75, 45, 255), (255, 90, 30, 255), "bloodhound"),
    ("spr_ms_vandal_idle", (110, 45, 38, 255), (160, 70, 55, 255), (240, 180, 40, 255), "vandal"),
    ("spr_ms_ronin_idle", (26, 20, 35, 255), (65, 42, 85, 255), (0, 255, 200, 255), "ronin"),
    ("spr_ms_tessen_idle", (32, 22, 45, 255), (75, 50, 105, 255), (180, 80, 255, 255), "tessen"),
    ("spr_ms_hephaestus_avatar", (32, 45, 70, 255), (240, 215, 80, 255), (0, 240, 255, 255), "hephaestus_avatar"),
    ("spr_ms_titan_proto", (55, 62, 52, 255), (95, 110, 90, 255), (255, 180, 40, 255), "titan")
]

for spr_id, b_col, a_col, g_col, m_type in sprites_to_build:
    create_advanced_mech_sprite(spr_id, b_col, a_col, g_col, m_type)

with open(YYP_PATH, "r") as f:
    yyp_content = f.read()

for spr_id, _, _, _, _ in sprites_to_build:
    spr_path = f"sprites/{spr_id}/{spr_id}.yy"
    entry = f"\"id\":{{\"name\":\"{spr_id}\",\"path\":\"{spr_path}\",}},"
    clean_entry = f"\"{entry}\""
    # standard GM resource format
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

print(f"All {len(sprites_to_build)} advanced sprites successfully created and registered!")
