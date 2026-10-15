import os
import json
import uuid
from PIL import Image, ImageDraw

SPRITES_DIR = 'sprites'
YYP_PATH = 'MechMakerConcept.yyp'

def create_sprite(sprite_name, is_back, archetype, primary_color, secondary_color, glow_color):
    spr_path = os.path.join(SPRITES_DIR, sprite_name)
    layers_path = os.path.join(spr_path, 'layers')
    os.makedirs(spr_path, exist_ok=True)
    os.makedirs(layers_path, exist_ok=True)

    layer_id = str(uuid.uuid4())
    frame_uuids = [str(uuid.uuid4()) for _ in range(4)]

    for i, f_uuid in enumerate(frame_uuids):
        im = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)

        # Ground drop shadow
        draw.ellipse([32, 142, 128, 154], fill=(0, 0, 0, 95))

        y_bob = -2 if (i == 1 or i == 3) else 0
        x_bob = 1 if i == 2 else (-1 if i == 3 else 0)

        p = primary_color
        s = secondary_color
        g = glow_color

        if archetype == 'biped_heavy':
            # Heavy Armored Bipedal Brawler (PMC Gold & Steel)
            if not is_back:
                # Legs
                draw.rectangle([56 + x_bob, 108 + y_bob, 72 + x_bob, 144], fill=s)
                draw.rectangle([88 + x_bob, 108 + y_bob, 104 + x_bob, 144], fill=s)
                draw.polygon([(52, 144), (76, 144), (74, 148), (50, 148)], fill=(35, 42, 50, 255))
                draw.polygon([(84, 144), (108, 144), (110, 148), (86, 148)], fill=(35, 42, 50, 255))
                # Torso & Heavy Pauldrons
                draw.polygon([(54, 70 + y_bob), (106, 70 + y_bob), (100, 110 + y_bob), (60, 110 + y_bob)], fill=p)
                draw.rectangle([68, 76 + y_bob, 92, 94 + y_bob], fill=s)
                # Head Visor
                draw.rectangle([72, 54 + y_bob, 88, 70 + y_bob], fill=p)
                draw.rectangle([74, 60 + y_bob, 86, 64 + y_bob], fill=g)
                # Left Arm: Heavy Solid Shield
                draw.polygon([(36, 75 + y_bob), (54, 75 + y_bob), (50, 122 + y_bob), (32, 120 + y_bob)], fill=p)
                draw.rectangle([40, 85 + y_bob, 46, 112 + y_bob], fill=(220, 180, 50, 255))
                # Right Arm: Heavy Autocannon
                draw.rectangle([106, 78 + y_bob, 120, 110 + y_bob], fill=s)
                draw.rectangle([112, 92 + y_bob, 138, 102 + y_bob], fill=(45, 52, 60, 255))
                draw.rectangle([138, 94 + y_bob, 150, 100 + y_bob], fill=(25, 30, 36, 255))
            else:
                # Back Perspective
                # Rear Legs
                draw.rectangle([56 + x_bob, 108 + y_bob, 72 + x_bob, 144], fill=s)
                draw.rectangle([88 + x_bob, 108 + y_bob, 104 + x_bob, 144], fill=s)
                # Back Torso & Heavy Reactor Backpack
                draw.polygon([(54, 70 + y_bob), (106, 70 + y_bob), (100, 110 + y_bob), (60, 110 + y_bob)], fill=p)
                draw.rectangle([62, 72 + y_bob, 98, 102 + y_bob], fill=(30, 36, 44, 255))
                # Twin heavy exhaust stacks & radiator louvers
                draw.rectangle([66, 60 + y_bob, 76, 76 + y_bob], fill=(50, 60, 70, 255))
                draw.rectangle([84, 60 + y_bob, 94, 76 + y_bob], fill=(50, 60, 70, 255))
                # Reactor glow
                draw.rectangle([70, 86 + y_bob, 90, 96 + y_bob], fill=g)
                # Ammo feed drum
                draw.ellipse([98, 85 + y_bob, 118, 105 + y_bob], fill=(60, 70, 82, 255))

        elif archetype == 'hover_sniper':
            # High-Mobility Hover Skirt Long-Range Sniper (Teal & Obsidian)
            if not is_back:
                # Wide Hover Skirt Dome
                draw.polygon([(46 + x_bob, 108 + y_bob), (114 + x_bob, 108 + y_bob), (124 + x_bob, 142), (36 + x_bob, 142)], fill=p)
                draw.ellipse([42 + x_bob, 136, 118 + x_bob, 146], fill=(20, 28, 38, 255))
                # Vent glow under hover skirt
                draw.ellipse([50 + x_bob, 140, 110 + x_bob, 146], fill=g)
                # Sleek Angular Torso
                draw.polygon([(62, 70 + y_bob), (98, 70 + y_bob), (94, 108 + y_bob), (66, 108 + y_bob)], fill=s)
                # Long Crest Sensor Head
                draw.polygon([(74, 52 + y_bob), (86, 52 + y_bob), (88, 70 + y_bob), (72, 70 + y_bob)], fill=p)
                draw.rectangle([76, 58 + y_bob, 84, 62 + y_bob], fill=g)
                # Huge Linear Railgun across right side
                draw.rectangle([98, 76 + y_bob, 110, 105 + y_bob], fill=s)
                draw.rectangle([104, 65 + y_bob, 148, 73 + y_bob], fill=(30, 42, 54, 255))
                draw.rectangle([148, 67 + y_bob, 158, 71 + y_bob], fill=(0, 240, 255, 255))
            else:
                # Back Perspective: Hover Skirt & Supercapacitor Bay
                draw.polygon([(46 + x_bob, 108 + y_bob), (114 + x_bob, 108 + y_bob), (124 + x_bob, 142), (36 + x_bob, 142)], fill=p)
                # Rear skirt vector nozzles
                draw.ellipse([52 + x_bob, 126 + y_bob, 68 + x_bob, 138 + y_bob], fill=g)
                draw.ellipse([92 + x_bob, 126 + y_bob, 108 + x_bob, 138 + y_bob], fill=g)
                # Torso & Capacitor Backpack
                draw.polygon([(62, 70 + y_bob), (98, 70 + y_bob), (94, 108 + y_bob), (66, 108 + y_bob)], fill=s)
                draw.rectangle([66, 72 + y_bob, 94, 100 + y_bob], fill=(22, 32, 44, 255))
                draw.line([(70, 78 + y_bob), (90, 78 + y_bob)], fill=g, width=2)
                draw.line([(70, 86 + y_bob), (90, 86 + y_bob)], fill=g, width=2)

        elif archetype == 'tread_artillery':
            # Heavy Caterpillar Tank Tread Artillery (Olive & Dark Iron)
            if not is_back:
                # Dual Tread Assemblies
                draw.polygon([(36 + x_bob, 120 + y_bob), (124 + x_bob, 120 + y_bob), (132 + x_bob, 146), (28 + x_bob, 146)], fill=(38, 44, 50, 255))
                # Tread wheels
                for wx in range(40, 125, 20):
                    draw.ellipse([wx + x_bob - 6, 132, wx + x_bob + 6, 144], fill=(70, 80, 90, 255))
                # Heavy Turret Torso
                draw.rectangle([52, 78 + y_bob, 108, 120 + y_bob], fill=p)
                # Reinforced Bunker Head
                draw.rectangle([70, 62 + y_bob, 90, 78 + y_bob], fill=s)
                draw.rectangle([74, 68 + y_bob, 86, 72 + y_bob], fill=g)
                # Twin Heavy Howitzer Barrels in High Angle
                draw.rectangle([54, 38 + y_bob, 66, 80 + y_bob], fill=(45, 52, 60, 255))
                draw.rectangle([94, 38 + y_bob, 106, 80 + y_bob], fill=(45, 52, 60, 255))
                draw.rectangle([52, 32 + y_bob, 68, 38 + y_bob], fill=(25, 30, 36, 255))
                draw.rectangle([92, 32 + y_bob, 108, 38 + y_bob], fill=(25, 30, 36, 255))
            else:
                # Back Perspective: Treads & Heavy Breech Mechanism
                draw.polygon([(36 + x_bob, 120 + y_bob), (124 + x_bob, 120 + y_bob), (132 + x_bob, 146), (28 + x_bob, 146)], fill=(38, 44, 50, 255))
                draw.rectangle([52, 78 + y_bob, 108, 120 + y_bob], fill=p)
                # Massive hydraulic recoil spades on rear
                draw.polygon([(42, 130), (52, 130), (50, 150), (40, 150)], fill=(65, 75, 85, 255))
                draw.polygon([(108, 130), (118, 130), (120, 150), (110, 150)], fill=(65, 75, 85, 255))
                # Shell magazine loading hopper
                draw.rectangle([60, 82 + y_bob, 100, 114 + y_bob], fill=(28, 34, 40, 255))
                draw.rectangle([68, 90 + y_bob, 92, 104 + y_bob], fill=g)

        elif archetype == 'aero_striker':
            # Swept-Wing Atmospheric & Space Vernier Striker (Navy & Crimson)
            if not is_back:
                # Aerodynamic Sleek Legs
                draw.rectangle([60 + x_bob, 108 + y_bob, 74 + x_bob, 144], fill=s)
                draw.rectangle([86 + x_bob, 108 + y_bob, 100 + x_bob, 144], fill=s)
                # Forward Swept Wing Binders
                draw.polygon([(26, 70 + y_bob), (58, 80 + y_bob), (48, 110 + y_bob), (18, 95 + y_bob)], fill=p)
                draw.polygon([(134, 70 + y_bob), (102, 80 + y_bob), (112, 110 + y_bob), (142, 95 + y_bob)], fill=p)
                # Torso & Needle Cockpit
                draw.polygon([(64, 68 + y_bob), (96, 68 + y_bob), (92, 108 + y_bob), (68, 108 + y_bob)], fill=p)
                draw.polygon([(72, 52 + y_bob), (88, 52 + y_bob), (84, 68 + y_bob), (76, 68 + y_bob)], fill=s)
                draw.rectangle([78, 58 + y_bob, 82, 64 + y_bob], fill=g)
                # High-Yield Beam Carbines
                draw.rectangle([102, 85 + y_bob, 132, 93 + y_bob], fill=(35, 45, 60, 255))
                draw.rectangle([132, 87 + y_bob, 142, 91 + y_bob], fill=g)
            else:
                # Back Perspective: Swept Wings & Dual Main Vernier Bells
                draw.rectangle([60 + x_bob, 108 + y_bob, 74 + x_bob, 144], fill=s)
                draw.rectangle([86 + x_bob, 108 + y_bob, 100 + x_bob, 144], fill=s)
                draw.polygon([(26, 70 + y_bob), (58, 80 + y_bob), (48, 110 + y_bob), (18, 95 + y_bob)], fill=p)
                draw.polygon([(134, 70 + y_bob), (102, 80 + y_bob), (112, 110 + y_bob), (142, 95 + y_bob)], fill=p)
                draw.polygon([(64, 68 + y_bob), (96, 68 + y_bob), (92, 108 + y_bob), (68, 108 + y_bob)], fill=p)
                # Twin main vernier rocket bells
                draw.polygon([(66, 80 + y_bob), (78, 80 + y_bob), (80, 96 + y_bob), (64, 96 + y_bob)], fill=(40, 50, 65, 255))
                draw.polygon([(82, 80 + y_bob), (94, 80 + y_bob), (96, 96 + y_bob), (80, 96 + y_bob)], fill=(40, 50, 65, 255))
                # Exhaust plumes
                draw.ellipse([67, 96 + y_bob, 77, 108 + y_bob], fill=g)
                draw.ellipse([83, 96 + y_bob, 93, 108 + y_bob], fill=g)

        # Save frame PNG
        frame_png_path = os.path.join(spr_path, f'{f_uuid}.png')
        im.save(frame_png_path)
        layer_dir = os.path.join(layers_path, f_uuid)
        os.makedirs(layer_dir, exist_ok=True)
        im.save(os.path.join(layer_dir, f'{layer_id}.png'))

    # Build .yy metadata
    yy_data = {
        '': 'v2',
        '%Name': sprite_name,
        'bboxMode': 0,
        'bbox_bottom': 159,
        'bbox_left': 0,
        'bbox_right': 159,
        'bbox_top': 0,
        'collisionKind': 1,
        'collisionTolerance': 0,
        'DynamicTexturePage': False,
        'edgeFiltering': False,
        'For3D': False,
        'frames': [
            {
                '': 'v1',
                '%Name': f_uuid,
                'name': f_uuid,
                'resourceType': 'GMSpriteFrame',
                'resourceVersion': '2.0'
            } for f_uuid in frame_uuids
        ],
        'gridX': 0,
        'gridY': 0,
        'height': 160,
        'HTile': False,
        'layers': [
            {
                '': '',
                '%Name': layer_id,
                'blendMode': 0,
                'displayName': 'default',
                'isLocked': False,
                'name': layer_id,
                'opacity': 100.0,
                'resourceType': 'GMImageLayer',
                'resourceVersion': '2.0',
                'visible': True
            }
        ],
        'name': sprite_name,
        'nineSlice': None,
        'origin': 9,
        'parent': {
            'name': 'sprites',
            'path': 'folders/Sprites.yy'
        },
        'preMultiplyAlpha': False,
        'resourceType': 'GMSprite',
        'resourceVersion': '2.0',
        'sequence': {
            '': 'v1',
            '%Name': sprite_name,
            'autoRecord': True,
            'backdropHeight': 768,
            'backdropImageOpacity': 0.5,
            'backdropImagePath': '',
            'backdropWidth': 1366,
            'backdropXOffset': 0.0,
            'backdropYOffset': 0.0,
            'events': {
                '<MessageEventKeyframe>': '',
                'Keyframes': [],
                'resourceType': 'KeyframeStore<MessageEventKeyframe>',
                'resourceVersion': '2.0'
            },
            'eventStubScript': None,
            'eventToFunction': {},
            'length': 4.0,
            'lockOrigin': False,
            'moments': {
                '<MomentsEventKeyframe>': '',
                'Keyframes': [],
                'resourceType': 'KeyframeStore<MomentsEventKeyframe>',
                'resourceVersion': '2.0'
            },
            'name': sprite_name,
            'playback': 1,
            'playbackSpeed': 6.0,
            'playbackSpeedType': 0,
            'showBackdrop': True,
            'showBackdropImage': False,
            'timeUnits': 1,
            'tracks': [
                {
                    '': '',
                    'builtinName': 0,
                    'events': [],
                    'inheritsTrackColour': True,
                    'interpolation': 1,
                    'isCreationTrack': False,
                    'keyframes': {
                        '<SpriteFrameKeyframe>': '',
                        'Keyframes': [
                            {
                                '<SpriteFrameKeyframe>': '',
                                'Channels': {
                                    '0': {
                                        '': '',
                                        'Id': {
                                            'name': f_uuid,
                                            'path': f'sprites/{sprite_name}/{sprite_name}.yy'
                                        },
                                        'resourceType': 'SpriteFrameKeyframe',
                                        'resourceVersion': '2.0'
                                    }
                                },
                                'Disabled': False,
                                'id': str(uuid.uuid4()),
                                'IsCreationKey': False,
                                'Key': float(idx),
                                'Length': 1.0,
                                'resourceType': 'Keyframe<SpriteFrameKeyframe>',
                                'resourceVersion': '2.0',
                                'Stretch': False
                            } for idx, f_uuid in enumerate(frame_uuids)
                        ],
                        'resourceType': 'KeyframeStore<SpriteFrameKeyframe>',
                        'resourceVersion': '2.0'
                    },
                    'modifiers': [],
                    'name': 'frames',
                    'resourceType': 'GMSpriteFramesTrack',
                    'resourceVersion': '2.0',
                    'spriteId': None,
                    'trackColour': 0,
                    'tracks': [],
                    'traits': 0
                }
            ],
            'visibleRange': None,
            'volume': 1.0,
            'xorigin': 80,
            'yorigin': 145
        },
        'swatchColours': None,
        'swfPrecision': 2.525,
        'textureGroupId': {
            'name': 'Default',
            'path': 'texturegroups/Default'
        },
        'type': 0,
        'VTile': False,
        'width': 160
    }

    with open(os.path.join(spr_path, f'{sprite_name}.yy'), 'w') as f:
        json.dump(yy_data, f, indent=2)

    print(f'Created sprite: {sprite_name}')

sprites_to_build = [
    # 1. Custom Heavy Biped Brawler
    ('spr_ms_custom_biped_heavy_idle', False, 'biped_heavy', (185, 150, 45, 255), (75, 85, 95, 255), (255, 140, 40, 255)),
    ('spr_ms_custom_biped_heavy_back_idle', True, 'biped_heavy', (185, 150, 45, 255), (75, 85, 95, 255), (255, 140, 40, 255)),
    # 2. Custom Hover Sniper
    ('spr_ms_custom_hover_sniper_idle', False, 'hover_sniper', (30, 110, 125, 255), (45, 60, 75, 255), (0, 240, 255, 255)),
    ('spr_ms_custom_hover_sniper_back_idle', True, 'hover_sniper', (30, 110, 125, 255), (45, 60, 75, 255), (0, 240, 255, 255)),
    # 3. Custom Tread Artillery
    ('spr_ms_custom_tread_artillery_idle', False, 'tread_artillery', (65, 80, 55, 255), (95, 110, 85, 255), (255, 180, 40, 255)),
    ('spr_ms_custom_tread_artillery_back_idle', True, 'tread_artillery', (65, 80, 55, 255), (95, 110, 85, 255), (255, 180, 40, 255)),
    # 4. Custom Aero Striker
    ('spr_ms_custom_aero_striker_idle', False, 'aero_striker', (28, 48, 85, 255), (145, 45, 55, 255), (255, 80, 60, 255)),
    ('spr_ms_custom_aero_striker_back_idle', True, 'aero_striker', (28, 48, 85, 255), (145, 45, 55, 255), (255, 80, 60, 255))
]

for spr_name, is_back, arch, p_col, s_col, g_col in sprites_to_build:
    create_sprite(spr_name, is_back, arch, p_col, s_col, g_col)

# Register in MechMakerConcept.yyp
with open(YYP_PATH, "r") as f:
    yyp_content = f.read()

for spr_name, _, _, _, _, _ in sprites_to_build:
    spr_path = f"sprites/{spr_name}/{spr_name}.yy"
    res_entry = "{\"id\":{\"name\":\"" + spr_name + "\",\"path\":\"" + spr_path + "\",}},},"
    if spr_name not in yyp_content:
        marker = "\"resources\": ["
        idx = yyp_content.find(marker)
        if idx != -1:
            insert_pos = idx + len(marker)
            yyp_content = yyp_content[:insert_pos] + "\n    " + res_entry + yyp_content[insert_pos:]
            print(f"Registered {spr_name} in MechMakerConcept.yyp")

with open(YYP_PATH, "w") as f:
    f.write(yyp_content)

print("All 8 custom player mobile suit isometric sprites created and registered!")
