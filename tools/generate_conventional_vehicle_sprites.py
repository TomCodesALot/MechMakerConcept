import os
import json
import uuid
from PIL import Image, ImageDraw

SPRITES_DIR = "sprites"
YYP_PATH = "MechMakerConcept.yyp"

def build_vehicle_sprite(sprite_name, veh_type, is_back=False):
    spr_path = os.path.join(SPRITES_DIR, sprite_name)
    layers_path = os.path.join(spr_path, "layers")
    os.makedirs(spr_path, exist_ok=True)
    os.makedirs(layers_path, exist_ok=True)

    layer_id = str(uuid.uuid4())
    frame_uuids = [str(uuid.uuid4()) for _ in range(4)]

    for i, f_uuid in enumerate(frame_uuids):
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)

        # Ground shadow
        draw.ellipse([24, 140, 136, 154], fill=(0, 0, 0, 100))

        # Animation vibration / tread roll / hover bob
        y_bob = -1 if (i % 2 == 1) else 0
        t_off = (i * 3) % 12

        if veh_type == "terran_mammoth":
            # T-720 Mammoth Heavy Tank
            # Base Colors: Military Olive & Steel
            hull_col = (54, 62, 50, 255)
            tread_col = (32, 35, 30, 255)
            accent_col = (85, 98, 78, 255)
            dark_iron = (22, 25, 20, 255)
            metal_high = (120, 135, 110, 255)

            if not is_back:
                # FRONT ISOMETRIC PERSPECTIVE
                # Heavy Dual Caterpillar Treads
                draw.polygon([(26, 148 + y_bob), (62, 148 + y_bob), (58, 122 + y_bob), (22, 122 + y_bob)], fill=tread_col, outline=dark_iron, width=2)
                draw.polygon([(98, 148 + y_bob), (134, 148 + y_bob), (138, 122 + y_bob), (102, 122 + y_bob)], fill=tread_col, outline=dark_iron, width=2)
                # Tread Wheel details
                for wx in [32, 44, 54]:
                    draw.ellipse([wx, 128 + y_bob, wx + 8, 142 + y_bob], fill=(48, 52, 45, 255), outline=dark_iron)
                for wx in [104, 114, 126]:
                    draw.ellipse([wx, 128 + y_bob, wx + 8, 142 + y_bob], fill=(48, 52, 45, 255), outline=dark_iron)
                # Sloped Front Glacis Plate
                draw.polygon([(36, 124 + y_bob), (124, 124 + y_bob), (116, 95 + y_bob), (44, 95 + y_bob)], fill=hull_col, outline=accent_col, width=2)
                draw.line([(48, 110 + y_bob), (112, 110 + y_bob)], fill=metal_high, width=1)
                # Armor skirt plates
                draw.rectangle([28, 116 + y_bob, 60, 126 + y_bob], fill=accent_col, outline=dark_iron)
                draw.rectangle([100, 116 + y_bob, 132, 126 + y_bob], fill=accent_col, outline=dark_iron)
                # Turret Ring & Dual 120mm Turret
                draw.polygon([(50, 96 + y_bob), (110, 96 + y_bob), (104, 68 + y_bob), (56, 68 + y_bob)], fill=(45, 52, 42, 255), outline=dark_iron, width=2)
                draw.rectangle([68, 62 + y_bob, 92, 70 + y_bob], fill=accent_col)
                # Commander Cupola & Vision Slits
                draw.ellipse([64, 66 + y_bob, 76, 76 + y_bob], fill=(30, 35, 28, 255), outline=metal_high)
                draw.rectangle([67, 70 + y_bob, 73, 72 + y_bob], fill=(255, 180, 50, 255))
                # Dual Heavy Rifled Barrels
                draw.rectangle([62, 28 + y_bob, 70, 70 + y_bob], fill=(60, 68, 58, 255), outline=dark_iron)
                draw.rectangle([76, 28 + y_bob, 84, 70 + y_bob], fill=(60, 68, 58, 255), outline=dark_iron)
                # Muzzle Brakes
                draw.rectangle([60, 24 + y_bob, 72, 29 + y_bob], fill=dark_iron)
                draw.rectangle([74, 24 + y_bob, 86, 29 + y_bob], fill=dark_iron)
                if i == 3:
                    # Muzzle flash spark
                    draw.polygon([(58, 22), (66, 8), (74, 22)], fill=(255, 220, 80, 240))
                    draw.polygon([(72, 22), (80, 8), (88, 22)], fill=(255, 220, 80, 240))
            else:
                # BACK ISOMETRIC PERSPECTIVE
                # Rear Treads
                draw.polygon([(26, 148 + y_bob), (62, 148 + y_bob), (58, 122 + y_bob), (22, 122 + y_bob)], fill=tread_col, outline=dark_iron, width=2)
                draw.polygon([(98, 148 + y_bob), (134, 148 + y_bob), (138, 122 + y_bob), (102, 122 + y_bob)], fill=tread_col, outline=dark_iron, width=2)
                # Rear Engine Deck & Radiator Louvers
                draw.polygon([(36, 126 + y_bob), (124, 126 + y_bob), (118, 92 + y_bob), (42, 92 + y_bob)], fill=hull_col, outline=dark_iron, width=2)
                # Cooling Grilles
                for gy in [100, 106, 112, 118]:
                    draw.line([(52, gy + y_bob), (108, gy + y_bob)], fill=(25, 28, 22, 255), width=2)
                # Dual External Auxiliary Fuel Drums
                draw.rectangle([44, 126 + y_bob, 62, 138 + y_bob], fill=(70, 80, 65, 255), outline=dark_iron)
                draw.rectangle([98, 126 + y_bob, 116, 138 + y_bob], fill=(70, 80, 65, 255), outline=dark_iron)
                # Rear Turret Bustle & Antennae
                draw.polygon([(52, 94 + y_bob), (108, 94 + y_bob), (102, 66 + y_bob), (58, 66 + y_bob)], fill=(45, 52, 42, 255), outline=accent_col, width=2)
                draw.line([(60, 66 + y_bob), (55, 38 + y_bob)], fill=(160, 175, 150, 255), width=2)
                # Exhaust vents with heat glow
                draw.ellipse([46, 94 + y_bob, 54, 100 + y_bob], fill=(220, 110, 30, 220))
                draw.ellipse([106, 94 + y_bob, 114, 100 + y_bob], fill=(220, 110, 30, 220))

        elif veh_type == "terran_skyhammer":
            # A-14 Skyhammer Strike Jet
            jet_grey = (65, 72, 80, 255)
            jet_dark = (35, 40, 48, 255)
            canopy_gold = (240, 190, 50, 230)
            camo_green = (50, 65, 55, 255)

            # High Hovering Flight Altitude
            f_bob = y_bob * 2

            if not is_back:
                # Nose & Cockpit
                draw.polygon([(74, 122 + f_bob), (86, 122 + f_bob), (82, 142 + f_bob), (78, 142 + f_bob)], fill=jet_dark)
                # Swept Wings
                draw.polygon([(18, 95 + f_bob), (74, 80 + f_bob), (76, 115 + f_bob), (22, 115 + f_bob)], fill=jet_grey, outline=camo_green, width=2)
                draw.polygon([(142, 95 + f_bob), (86, 80 + f_bob), (84, 115 + f_bob), (138, 115 + f_bob)], fill=jet_grey, outline=camo_green, width=2)
                # Fuselage
                draw.polygon([(68, 60 + f_bob), (92, 60 + f_bob), (88, 128 + f_bob), (72, 128 + f_bob)], fill=jet_grey, outline=jet_dark, width=2)
                # Armored Canopy
                draw.polygon([(74, 82 + f_bob), (86, 82 + f_bob), (84, 106 + f_bob), (76, 106 + f_bob)], fill=canopy_gold)
                # Twin Turbofan Intakes on top
                draw.rectangle([58, 62 + f_bob, 68, 85 + f_bob], fill=jet_dark, outline=jet_grey)
                draw.rectangle([92, 62 + f_bob, 102, 85 + f_bob], fill=jet_dark, outline=jet_grey)
                # Underwing Rocket Pods
                draw.rectangle([28, 105 + f_bob, 42, 120 + f_bob], fill=(80, 85, 90, 255), outline=jet_dark)
                draw.rectangle([118, 105 + f_bob, 132, 120 + f_bob], fill=(80, 85, 90, 255), outline=jet_dark)
                # GAU-30mm Rotary under nose
                draw.line([(80, 132 + f_bob), (80, 148 + f_bob)], fill=(20, 22, 25, 255), width=3)
                if i == 3:
                    draw.polygon([(78, 148 + f_bob), (80, 158 + f_bob), (82, 148 + f_bob)], fill=(255, 220, 80, 255))
            else:
                # BACK ISOMETRIC PERSPECTIVE
                # Swept Wings from rear
                draw.polygon([(18, 98 + f_bob), (74, 85 + f_bob), (76, 118 + f_bob), (22, 118 + f_bob)], fill=jet_grey, outline=jet_dark, width=2)
                draw.polygon([(142, 98 + f_bob), (86, 85 + f_bob), (84, 118 + f_bob), (138, 118 + f_bob)], fill=jet_grey, outline=jet_dark, width=2)
                # Fuselage
                draw.polygon([(68, 55 + f_bob), (92, 55 + f_bob), (86, 120 + f_bob), (74, 120 + f_bob)], fill=jet_grey, outline=jet_dark, width=2)
                # Twin Vertical Stabilizers
                draw.polygon([(66, 42 + f_bob), (72, 42 + f_bob), (72, 75 + f_bob), (64, 75 + f_bob)], fill=camo_green, outline=jet_dark)
                draw.polygon([(88, 42 + f_bob), (94, 42 + f_bob), (96, 75 + f_bob), (88, 75 + f_bob)], fill=camo_green, outline=jet_dark)
                # Twin Screaming Exhaust Nozzles with Afterburner
                draw.ellipse([58, 112 + f_bob, 70, 124 + f_bob], fill=(20, 25, 30, 255), outline=(100, 110, 120, 255), width=2)
                draw.ellipse([90, 112 + f_bob, 102, 124 + f_bob], fill=(20, 25, 30, 255), outline=(100, 110, 120, 255), width=2)
                # Afterburner Flames
                draw.polygon([(60, 122 + f_bob), (64, 142 + f_bob), (68, 122 + f_bob)], fill=(80, 180, 255, 240))
                draw.polygon([(92, 122 + f_bob), (96, 142 + f_bob), (100, 122 + f_bob)], fill=(80, 180, 255, 240))
                draw.polygon([(62, 122 + f_bob), (64, 132 + f_bob), (66, 122 + f_bob)], fill=(255, 255, 255, 255))
                draw.polygon([(94, 122 + f_bob), (96, 132 + f_bob), (98, 122 + f_bob)], fill=(255, 255, 255, 255))

        elif veh_type == "colony_stiletto":
            # K-4 Stiletto Hover Skiff
            hull_blue = (40, 75, 125, 255)
            cyan_glow = (0, 235, 255, 255)
            dark_navy = (20, 32, 55, 255)

            # Floating Hover cushion
            h_bob = -2 if (i % 2 == 1) else 1

            # Glowing Cyan Repulsor Field beneath skirt
            draw.ellipse([34, 136 + h_bob, 126, 148 + h_bob], fill=(0, 210, 255, 110), outline=cyan_glow)

            if not is_back:
                # Wedge Front Glacis
                draw.polygon([(40, 132 + h_bob), (120, 132 + h_bob), (95, 85 + h_bob), (65, 85 + h_bob)], fill=hull_blue, outline=dark_navy, width=2)
                draw.line([(80, 85 + h_bob), (80, 132 + h_bob)], fill=cyan_glow, width=2)
                # Pilot Bubble Cockpit
                draw.ellipse([70, 92 + h_bob, 90, 112 + h_bob], fill=(20, 40, 70, 255), outline=cyan_glow)
                # Outrigger Linear Railguns
                draw.rectangle([22, 90 + h_bob, 36, 128 + h_bob], fill=dark_navy, outline=hull_blue)
                draw.line([(28, 65 + h_bob), (28, 128 + h_bob)], fill=(200, 230, 255, 255), width=2)
                draw.rectangle([124, 90 + h_bob, 138, 128 + h_bob], fill=dark_navy, outline=hull_blue)
                draw.line([(132, 65 + h_bob), (132, 128 + h_bob)], fill=(200, 230, 255, 255), width=2)
                # Hover Venturi Skirts
                draw.rectangle([36, 126 + h_bob, 124, 136 + h_bob], fill=dark_navy, outline=cyan_glow)
            else:
                # BACK PERSPECTIVE
                draw.polygon([(40, 132 + h_bob), (120, 132 + h_bob), (105, 88 + h_bob), (55, 88 + h_bob)], fill=hull_blue, outline=dark_navy, width=2)
                # High-Velocity Venturi Thrusters
                draw.ellipse([52, 114 + h_bob, 68, 130 + h_bob], fill=dark_navy, outline=cyan_glow, width=2)
                draw.ellipse([92, 114 + h_bob, 108, 130 + h_bob], fill=dark_navy, outline=cyan_glow, width=2)
                # Ion Plasma Stream
                draw.ellipse([56, 118 + h_bob, 64, 126 + h_bob], fill=cyan_glow)
                draw.ellipse([96, 118 + h_bob, 104, 126 + h_bob], fill=cyan_glow)
                # Radiator Fin array
                draw.polygon([(74, 70 + h_bob), (86, 70 + h_bob), (84, 96 + h_bob), (76, 96 + h_bob)], fill=dark_navy, outline=cyan_glow)

        elif veh_type == "colony_dart":
            # S-10 Dart Hypersonic Interceptor
            dart_white = (210, 225, 245, 255)
            dart_blue = (25, 60, 120, 255)
            cyan_glow = (0, 240, 255, 255)

            if not is_back:
                # Needle Nose
                draw.polygon([(78, 148 + y_bob), (82, 148 + y_bob), (84, 105 + y_bob), (76, 105 + y_bob)], fill=dart_blue)
                # Razor Delta Wings
                draw.polygon([(16, 105 + y_bob), (76, 85 + y_bob), (78, 118 + y_bob), (20, 122 + y_bob)], fill=dart_white, outline=dart_blue, width=2)
                draw.polygon([(144, 105 + y_bob), (84, 85 + y_bob), (82, 118 + y_bob), (140, 122 + y_bob)], fill=dart_white, outline=dart_blue, width=2)
                # Fuselage & Gold Canopy
                draw.polygon([(72, 60 + y_bob), (88, 60 + y_bob), (84, 125 + y_bob), (76, 125 + y_bob)], fill=dart_white, outline=dart_blue, width=2)
                draw.polygon([(75, 82 + y_bob), (85, 82 + y_bob), (83, 108 + y_bob), (77, 108 + y_bob)], fill=(240, 180, 40, 240))
                # Pulse Laser Pylons
                draw.line([(32, 108 + y_bob), (32, 128 + y_bob)], fill=cyan_glow, width=2)
                draw.line([(128, 108 + y_bob), (128, 128 + y_bob)], fill=cyan_glow, width=2)
            else:
                # BACK DELTA & DUAL SCRAMJETS
                draw.polygon([(16, 105 + y_bob), (76, 85 + y_bob), (78, 118 + y_bob), (20, 122 + y_bob)], fill=dart_white, outline=dart_blue, width=2)
                draw.polygon([(144, 105 + y_bob), (84, 85 + y_bob), (82, 118 + y_bob), (140, 122 + y_bob)], fill=dart_white, outline=dart_blue, width=2)
                draw.polygon([(70, 50 + y_bob), (90, 50 + y_bob), (86, 115 + y_bob), (74, 115 + y_bob)], fill=dart_white, outline=dart_blue, width=2)
                # Vertical Delta Fin
                draw.polygon([(77, 36 + y_bob), (83, 36 + y_bob), (83, 75 + y_bob), (77, 75 + y_bob)], fill=dart_blue)
                # Triangular Scramjet Nozzles
                draw.polygon([(64, 115 + y_bob), (72, 115 + y_bob), (68, 128 + y_bob)], fill=(15, 20, 30, 255), outline=cyan_glow)
                draw.polygon([(88, 115 + y_bob), (96, 115 + y_bob), (92, 128 + y_bob)], fill=(15, 20, 30, 255), outline=cyan_glow)
                # Ion trail
                draw.polygon([(66, 128 + y_bob), (68, 146 + y_bob), (70, 128 + y_bob)], fill=cyan_glow)
                draw.polygon([(90, 128 + y_bob), (92, 146 + y_bob), (94, 128 + y_bob)], fill=cyan_glow)

        elif veh_type == "syndicate_technical":
            # SCR-T01 Rustfang Technical (Scrap Gun Truck)
            rust_brown = (115, 55, 38, 255)
            scrap_iron = (50, 42, 38, 255)
            bright_orange = (235, 110, 30, 255)

            if not is_back:
                # Heavy All-Terrain Tires
                for tx in [28, 116]:
                    draw.ellipse([tx, 130 + y_bob, tx + 16, 150 + y_bob], fill=(25, 22, 20, 255), outline=scrap_iron, width=2)
                for tx in [44, 100]:
                    draw.ellipse([tx, 122 + y_bob, tx + 16, 142 + y_bob], fill=(25, 22, 20, 255), outline=scrap_iron, width=2)
                # Armored Truck Cab & Welded Mesh
                draw.polygon([(46, 128 + y_bob), (114, 128 + y_bob), (106, 92 + y_bob), (54, 92 + y_bob)], fill=rust_brown, outline=scrap_iron, width=2)
                draw.rectangle([58, 96 + y_bob, 102, 108 + y_bob], fill=(30, 24, 20, 255), outline=bright_orange)
                # Welded armor spikes / bumper
                draw.rectangle([42, 124 + y_bob, 118, 132 + y_bob], fill=scrap_iron)
                # Flatbed Mounted 50mm Flak Gunner
                draw.rectangle([68, 65 + y_bob, 92, 85 + y_bob], fill=scrap_iron, outline=bright_orange)
                draw.line([(80, 35 + y_bob), (80, 75 + y_bob)], fill=(180, 160, 150, 255), width=3)
                # Rocket Rack on side
                draw.rectangle([98, 68 + y_bob, 115, 88 + y_bob], fill=(70, 50, 40, 255), outline=bright_orange)
            else:
                # BACK PERSPECTIVE
                for tx in [28, 116]:
                    draw.ellipse([tx, 130 + y_bob, tx + 16, 150 + y_bob], fill=(25, 22, 20, 255), outline=scrap_iron, width=2)
                # Open Flatbed Tailgate
                draw.polygon([(42, 130 + y_bob), (118, 130 + y_bob), (112, 98 + y_bob), (48, 98 + y_bob)], fill=rust_brown, outline=scrap_iron, width=2)
                draw.line([(48, 114 + y_bob), (112, 114 + y_bob)], fill=bright_orange, width=2)
                # Dual Vertical Exhaust Smokestacks
                draw.rectangle([48, 62 + y_bob, 54, 100 + y_bob], fill=scrap_iron)
                draw.rectangle([106, 62 + y_bob, 112, 100 + y_bob], fill=scrap_iron)
                # Diesel black exhaust puff
                if i % 2 == 1:
                    draw.ellipse([45, 48 + y_bob, 57, 60 + y_bob], fill=(40, 35, 30, 180))
                    draw.ellipse([103, 48 + y_bob, 115, 60 + y_bob], fill=(40, 35, 30, 180))
                # Rear Turret Ring
                draw.polygon([(68, 72 + y_bob), (92, 72 + y_bob), (90, 96 + y_bob), (70, 96 + y_bob)], fill=scrap_iron, outline=bright_orange)

        elif veh_type == "zaibatsu_kurogane":
            # Type-94 Kurogane Stealth Drone Tank
            stealth_dark = (28, 24, 38, 255)
            carbon_grey = (52, 45, 68, 255)
            lens_green = (0, 255, 180, 255)

            if not is_back:
                # Silent Rubber Treads
                draw.polygon([(30, 146 + y_bob), (62, 146 + y_bob), (58, 124 + y_bob), (26, 124 + y_bob)], fill=(18, 15, 24, 255), outline=(65, 55, 80, 255))
                draw.polygon([(98, 146 + y_bob), (130, 146 + y_bob), (134, 124 + y_bob), (102, 124 + y_bob)], fill=(18, 15, 24, 255), outline=(65, 55, 80, 255))
                # Faceted Stealth Glacis
                draw.polygon([(40, 126 + y_bob), (120, 126 + y_bob), (112, 90 + y_bob), (48, 90 + y_bob)], fill=stealth_dark, outline=carbon_grey, width=2)
                draw.line([(80, 90 + y_bob), (80, 126 + y_bob)], fill=lens_green, width=1)
                # AI Optical Sensor Dome (Glowing Green Lens)
                draw.ellipse([70, 78 + y_bob, 90, 98 + y_bob], fill=(15, 12, 22, 255), outline=lens_green, width=2)
                draw.ellipse([76, 84 + y_bob, 84, 92 + y_bob], fill=lens_green)
                # Hypersonic Railgun Barrel
                draw.rectangle([76, 32 + y_bob, 84, 80 + y_bob], fill=(70, 65, 85, 255), outline=(15, 12, 22, 255))
                draw.line([(80, 32 + y_bob), (80, 80 + y_bob)], fill=lens_green, width=1)
            else:
                # BACK PERSPECTIVE
                draw.polygon([(30, 146 + y_bob), (62, 146 + y_bob), (58, 124 + y_bob), (26, 124 + y_bob)], fill=(18, 15, 24, 255), outline=(65, 55, 80, 255))
                draw.polygon([(98, 146 + y_bob), (130, 146 + y_bob), (134, 124 + y_bob), (102, 124 + y_bob)], fill=(18, 15, 24, 255), outline=(65, 55, 80, 255))
                draw.polygon([(40, 128 + y_bob), (120, 128 + y_bob), (114, 88 + y_bob), (46, 88 + y_bob)], fill=stealth_dark, outline=carbon_grey, width=2)
                # Heat Dissipation Louvers
                for hy in [96, 102, 108, 114]:
                    draw.line([(55, hy + y_bob), (105, hy + y_bob)], fill=(12, 10, 16, 255), width=2)
                # Comms & AI Telemetry Node
                draw.polygon([(72, 70 + y_bob), (88, 70 + y_bob), (84, 88 + y_bob), (76, 88 + y_bob)], fill=carbon_grey, outline=lens_green)

        # Save main frame and layer png
        main_png = os.path.join(spr_path, f"{f_uuid}.png")
        im.save(main_png, "PNG")
        layer_dir = os.path.join(layers_path, f_uuid)
        os.makedirs(layer_dir, exist_ok=True)
        layer_png = os.path.join(layer_dir, f"{layer_id}.png")
        im.save(layer_png, "PNG")

    # Generate .yy file
    yy_data = {
        "$GMSprite": "v2",
        "%Name": sprite_name,
        "bboxMode": 0,
        "bbox_bottom": 154,
        "bbox_left": 16,
        "bbox_right": 144,
        "bbox_top": 20,
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
            } for f_uuid in frame_uuids
        ],
        "gridX": 0,
        "gridY": 0,
        "height": 160,
        "HTile": False,
        "layers": [
            {
                "$GMImageLayer": "v1",
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
        "origin": 9,
        "parent": {
            "name": "sprites",
            "path": "folders/Sprites.yy"
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
                                "Key": float(idx),
                                "Length": 1.0,
                                "resourceType": "Keyframe<SpriteFrameKeyframe>",
                                "resourceVersion": "2.0",
                                "Stretch": False
                            } for idx, f_uuid in enumerate(frame_uuids)
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

    print(f"Created vehicle sprite: {sprite_name}")

vehicles_to_build = [
    ("spr_veh_terran_mammoth_idle", "terran_mammoth", False),
    ("spr_veh_terran_mammoth_back_idle", "terran_mammoth", True),
    ("spr_veh_terran_skyhammer_idle", "terran_skyhammer", False),
    ("spr_veh_terran_skyhammer_back_idle", "terran_skyhammer", True),
    ("spr_veh_colony_stiletto_idle", "colony_stiletto", False),
    ("spr_veh_colony_stiletto_back_idle", "colony_stiletto", True),
    ("spr_veh_colony_dart_idle", "colony_dart", False),
    ("spr_veh_colony_dart_back_idle", "colony_dart", True),
    ("spr_veh_syndicate_technical_idle", "syndicate_technical", False),
    ("spr_veh_syndicate_technical_back_idle", "syndicate_technical", True),
    ("spr_veh_zaibatsu_kurogane_idle", "zaibatsu_kurogane", False),
    ("spr_veh_zaibatsu_kurogane_back_idle", "zaibatsu_kurogane", True)
]

for spr_name, v_type, is_bk in vehicles_to_build:
    build_vehicle_sprite(spr_name, v_type, is_bk)

with open(YYP_PATH, "r") as f:
    yyp_content = f.read()

registered = 0
for spr_name, _, _ in vehicles_to_build:
    spr_path = f"sprites/{spr_name}/{spr_name}.yy"
    res_entry = f"{{\"id\":{{\"name\":\"{spr_name}\",\"path\":\"{spr_path}\",}},}},"
    if spr_name not in yyp_content:
        marker = '"resources": ['
        idx = yyp_content.find(marker)
        if idx != -1:
            insert_pos = idx + len(marker)
            yyp_content = yyp_content[:insert_pos] + f"\n    {res_entry}" + yyp_content[insert_pos:]
            registered += 1

with open(YYP_PATH, "w") as f:
    f.write(yyp_content)

print(f"Registered {registered} new vehicle sprites in {YYP_PATH}.")
