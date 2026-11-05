import math, os, json, uuid, shutil
from PIL import Image, ImageDraw

def clamp(v, low, high):
    return max(low, min(high, v))

# Load the cleaned idle frames as base
base_frames = [
    Image.open(f'sprites/spr_ms_centurion_idle/{fn}.png').convert('RGBA')
    for fn in ['e283773f-bb6e-48e5-93e5-3e3803458f0b', 'f0c4c103-85f6-48ef-9ba4-9cbf6e678910', 'f7e30520-bf8f-45f6-b096-e65666cd1856', '9a42f0fa-2c6f-4cea-8605-1026b640bfa4']
]
master_body = base_frames[0]

# =========================================================================
# 1. BUILD spr_ms_centurion_fire_chaingun (4 FRAMES)
# =========================================================================
chaingun_frames = []

# Muzzle flare helper
def draw_muzzle_flare(draw, mx, my, length, height):
    # Flash cone pointing right (+x)
    for x in range(mx, mx + length):
        prog = (x - mx) / float(length)
        half_h = (height * 0.5) * (1.0 - prog)
        for dy in range(-int(math.ceil(half_h)), int(math.ceil(half_h)) + 1):
            dist = abs(dy) / max(1.0, half_h)
            if dist <= 1.0:
                if prog < 0.35 and dist < 0.5:
                    col = (255, 255, 220, 255) # white-yellow core
                elif prog < 0.75:
                    col = (255, 180, 40, 240)  # bright orange
                else:
                    col = (240, 70, 20, 180)   # red tip
                draw.point((x, my + dy), fill=col)
    # Side flare spikes
    draw.line([mx, my, mx + length//2, my - height], fill=(255, 250, 160, 220), width=1)
    draw.line([mx, my, mx + length//2, my + height], fill=(255, 250, 160, 220), width=1)

# Frame 0: Spinup lock & brace (recoil 0)
f0 = master_body.copy()
d0 = ImageDraw.Draw(f0)
# Barrel heat glints
d0.point((133, 63), fill=(255, 200, 60, 255))
d0.point((133, 71), fill=(255, 200, 60, 255))
chaingun_frames.append(f0)

# Frame 1: Upper barrel 1 flash & tracer exit (recoil -2)
f1 = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
f1.paste(master_body, (-2, 0), master_body)
d1 = ImageDraw.Draw(f1)
# Upper barrel flash at (133 - 2, 63) = (131, 63)
draw_muzzle_flare(d1, 133, 63, length=24, height=8)
# Spent 35mm casing ejecting
d1.ellipse([108, 54, 112, 57], fill=(240, 210, 80, 255), outline=(140, 110, 30, 255))
chaingun_frames.append(f1)

# Frame 2: Lower barrel 2 flash & tracer exit (recoil -3)
f2 = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
f2.paste(master_body, (-3, 0), master_body)
d2 = ImageDraw.Draw(f2)
# Lower barrel flash at (133 - 3, 71) = (130, 71)
draw_muzzle_flare(d2, 132, 71, length=26, height=8)
# Spent casing ejecting
d2.ellipse([109, 52, 113, 55], fill=(240, 210, 80, 255), outline=(140, 110, 30, 255))
chaingun_frames.append(f2)

# Frame 3: Barrel spin-down & heat smoke venting (recoil -1)
f3 = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
f3.paste(master_body, (-1, 0), master_body)
d3 = ImageDraw.Draw(f3)
# Propellant smoke venting from twin muzzles
for sm_x, sm_y in [(135, 62), (138, 60), (142, 58), (135, 70), (139, 68)]:
    d3.ellipse([sm_x - 2, sm_y - 2, sm_x + 2, sm_y + 2], fill=(160, 165, 170, 140))
chaingun_frames.append(f3)

# =========================================================================
# 2. BUILD spr_ms_centurion_attack_melee (6 FRAMES)
# Spartan Tower Shield Bash into Hydraulic Spiked Ramming Prow Breach
# =========================================================================
melee_frames = []

def draw_spiked_prow(draw, px, py, length, thrust_flash=False):
    # Hydraulic cylinder body
    draw.rectangle([px - 14, py - 4, px, py + 4], fill=(60, 65, 72, 255), outline=(35, 38, 42, 255))
    # Ramming spike shaft (35mm solid tungsten)
    draw.rectangle([px, py - 2, px + length, py + 2], fill=(170, 180, 195, 255), outline=(90, 100, 115, 255))
    # Beveled chisel point
    draw.polygon([(px + length, py - 4), (px + length + 8, py), (px + length, py + 4)], fill=(230, 240, 250, 255))
    if thrust_flash:
        # High-pressure pneumatic venting & impact sparks
        for angle in range(-45, 50, 20):
            rad = math.radians(angle)
            sx = px + length + 8 + math.cos(rad) * 14
            sy = py + math.sin(rad) * 14
            draw.line([px + length + 8, py, sx, sy], fill=(255, 220, 100, 240), width=2)

# Frame 0: Linebreaker Shock Stance (shift +8px forward)
m0 = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
m0.paste(master_body, (8, 1), master_body)
d0 = ImageDraw.Draw(m0)
# Spiked prow tucked back
draw_spiked_prow(d0, px=98, py=78, length=12)
melee_frames.append(m0)

# Frame 1: Spartan Tower Shield Impact Slam (+24px forward collision)
m1 = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
m1.paste(master_body, (24, 2), master_body)
d1 = ImageDraw.Draw(m1)
# Kinetic shield collision flash on leading shield rim (x: 58 + 24 = 82)
for ang in [-30, -15, 0, 15, 30]:
    rad = math.radians(ang)
    d1.line([82, 68, 82 + math.cos(rad) * 14, 68 + math.sin(rad) * 14], fill=(255, 240, 140, 240), width=2)
draw_spiked_prow(d1, px=114, py=79, length=14)
melee_frames.append(m1)

# Frame 2: Hydraulic Prow Priming & Target Pin (+18px forward)
m2 = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
m2.paste(master_body, (18, 1), master_body)
d2 = ImageDraw.Draw(m2)
# Piston pressure building (cyan heat channel on cylinder)
draw_spiked_prow(d2, px=108, py=78, length=16)
d2.line([100, 78, 106, 78], fill=(0, 240, 255, 240), width=2)
melee_frames.append(m2)

# Frame 3: Explosive Pneumatic Thrust (+22px forward)
m3 = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
m3.paste(master_body, (22, 2), master_body)
d3 = ImageDraw.Draw(m3)
# Ramming spike drives forward to x=148
draw_spiked_prow(d3, px=112, py=78, length=28, thrust_flash=False)
# Piston motion blur
d3.line([112, 78, 140, 78], fill=(200, 235, 255, 200), width=3)
melee_frames.append(m3)

# Frame 4: Catastrophic Armor Breach Impact! (+26px forward)
m4 = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
m4.paste(master_body, (26, 3), master_body)
d4 = ImageDraw.Draw(m4)
# Full extension at x=154
draw_spiked_prow(d4, px=116, py=79, length=32, thrust_flash=True)
# Shockwave ring
imp_x = 116 + 32 + 8
imp_y = 79
d4.ellipse([imp_x - 16, imp_y - 16, imp_x + 16, imp_y + 16], outline=(255, 230, 120, 240), width=2)
d4.ellipse([imp_x - 24, imp_y - 10, imp_x + 24, imp_y + 10], outline=(255, 120, 40, 180), width=1)
melee_frames.append(m4)

# Frame 5: Hydraulic Venting & Recovery (+12px forward)
m5 = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
m5.paste(master_body, (12, 1), master_body)
d5 = ImageDraw.Draw(m5)
draw_spiked_prow(d5, px=102, py=78, length=16)
# Steam venting puff from piston chamber
for sx in range(94, 104):
    for sy in range(72, 84):
        dist = math.hypot(sx - 99, sy - 78)
        if dist <= 5:
            d5.point((sx, sy), fill=(210, 215, 220, int(150 * (1 - dist / 5.0))))
melee_frames.append(m5)

# =========================================================================
# 3. BUILD spr_ms_centurion_boost (4 FRAMES)
# Heavy Linebreaker Forward Dash with twin vernier thrusters & dust
# =========================================================================
boost_frames = []

def draw_centurion_thruster(draw, ox, oy, length, width):
    for x in range(ox - length, ox):
        dx = ox - x
        prog = dx / float(length)
        half_w = (width * 0.5) * (1.0 - prog * 0.6)
        for dy_off in range(-int(math.ceil(half_w)), int(math.ceil(half_w)) + 1):
            if abs(dy_off) <= half_w:
                if prog < 0.4 and abs(dy_off) < half_w * 0.5:
                    col = (255, 255, 220, 255)
                elif prog < 0.75:
                    col = (255, 160, 30, 240)
                else:
                    col = (220, 50, 10, 180)
                draw.point((x, oy + dy_off), fill=col)

b_configs = [
    (6, 1, 24, 6),
    (10, 2, 34, 7),
    (7, 1, 28, 6),
    (9, 2, 30, 7)
]

for idx, (sx, sy, plen, pw) in enumerate(b_configs):
    bfr = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
    bfr.paste(master_body, (sx, sy), master_body)
    bd = ImageDraw.Draw(bfr)
    
    # Twin backpack thruster nozzles on Centurion (left side of torso, x: 40+sx, y: 44+sy and 52+sy)
    noz1_x = 42 + sx
    noz1_y = 44 + sy
    noz2_x = 42 + sx
    noz2_y = 52 + sy
    
    draw_centurion_thruster(bd, noz1_x, noz1_y, plen, pw)
    draw_centurion_thruster(bd, noz2_x, noz2_y, int(plen * 0.9), pw)
    
    # Ground dust streak
    heel_x = 36 + sx
    heel_y = 134 + sy
    for d_x in range(heel_x - (16 + idx * 4), heel_x):
        d_prog = (heel_x - d_x) / float(16 + idx * 4)
        for d_y in range(heel_y - int(3 * d_prog), heel_y + 1):
            bd.point((d_x, d_y), fill=(100, 95, 80, int(180 * (1 - d_prog))))
            
    boost_frames.append(bfr)

# =========================================================================
# 4. BUILD spr_ms_centurion_idle_damaged (4 FRAMES) & spr_ms_centurion_destroyed (1 FRAME)
# =========================================================================
dmg_frames = []
for idx, fr in enumerate(base_frames):
    dfr = fr.copy()
    dd = ImageDraw.Draw(dfr)
    # Scorch marks and armor scoring
    dd.line([60, 45, 75, 55], fill=(35, 30, 25, 220), width=2)
    dd.line([65, 80, 80, 88], fill=(30, 25, 20, 200), width=2)
    dd.line([45, 60, 52, 70], fill=(40, 35, 30, 200), width=2)
    # Hydraulic fluid leak drip
    dd.line([72, 55, 72, 65], fill=(45, 30, 15, 220), width=1)
    # Flinch posture shift
    dfr_out = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
    dfr_out.paste(dfr, (-4, 1), dfr)
    dmg_frames.append(dfr_out)

# Destroyed frame: kneeling breach collapse
dest_fr = master_body.copy()
dest_d = ImageDraw.Draw(dest_fr)
# Heavy burn scorches and slag scoring
for sy in range(30, 110, 8):
    dest_d.line([45, sy, 115, sy + 4], fill=(25, 25, 28, 220), width=2)
dest_out = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
# Sunk down into knees (-10px y shift, -6px x shift)
dest_out.paste(dest_fr, (-6, 8), dest_fr)

# =========================================================================
# 5. PACKAGING AND SAVING ALL ASSETS TO SPRITES FOLDERS
# =========================================================================
def save_gmsprite_suite(sprite_name, frames_list, fps=8.0):
    sdir = os.path.join('sprites', sprite_name)
    os.makedirs(sdir, exist_ok=True)
    
    num_f = len(frames_list)
    f_ids = [str(uuid.uuid4()) for _ in range(num_f)]
    l_id = str(uuid.uuid4())
    
    # Save root frames
    for i, fid in enumerate(f_ids):
        frames_list[i].save(os.path.join(sdir, f'{fid}.png'))
        
    # Save layers
    l_root = os.path.join(sdir, 'layers')
    shutil.rmtree(l_root, ignore_errors=True)
    os.makedirs(l_root, exist_ok=True)
    for i, fid in enumerate(f_ids):
        fl_dir = os.path.join(l_root, fid)
        os.makedirs(fl_dir, exist_ok=True)
        frames_list[i].save(os.path.join(fl_dir, f'{l_id}.png'))
        
    # Preview and strip
    frames_list[0].save(os.path.join(sdir, f'{sprite_name}.png'))
    strip = Image.new('RGBA', (160 * num_f, 160), (0, 0, 0, 0))
    for i, fr in enumerate(frames_list):
        strip.paste(fr, (i * 160, 0))
    strip.save(os.path.join(sdir, f'{sprite_name}_strip{num_f}.png'))
    
    # Construct .yy JSON
    yy_data = {
      "$GMSprite": "v2",
      "%Name": sprite_name,
      "bboxMode": 0,
      "bbox_bottom": 159,
      "bbox_left": 0,
      "bbox_right": 159,
      "bbox_top": 0,
      "collisionKind": 1,
      "collisionTolerance": 0,
      "DynamicTexturePage": False,
      "edgeFiltering": False,
      "For3D": False,
      "frames": [
        {
          "$GMSpriteFrame": "v1",
          "%Name": f_ids[i],
          "name": f_ids[i],
          "resourceType": "GMSpriteFrame",
          "resourceVersion": "2.0"
        } for i in range(num_f)
      ],
      "gridX": 0,
      "gridY": 0,
      "height": 160,
      "HTile": False,
      "layers": [
        {
          "$GMImageLayer": "",
          "%Name": l_id,
          "blendMode": 0,
          "displayName": "default",
          "isLocked": False,
          "name": l_id,
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
        "length": float(num_f),
        "lockOrigin": False,
        "moments": {
          "$KeyframeStore<MomentsEventKeyframe>": "",
          "Keyframes": [],
          "resourceType": "KeyframeStore<MomentsEventKeyframe>",
          "resourceVersion": "2.0"
        },
        "name": sprite_name,
        "playback": 1,
        "playbackSpeed": fps,
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
                        "name": f_ids[i],
                        "path": f"sprites/{sprite_name}/{sprite_name}.yy"
                      },
                      "resourceType": "SpriteFrameKeyframe",
                      "resourceVersion": "2.0"
                    }
                  },
                  "Disabled": False,
                  "id": str(uuid.uuid4()),
                  "IsCreationKey": False,
                  "Key": float(i),
                  "Length": 1.0,
                  "resourceType": "Keyframe<SpriteFrameKeyframe>",
                  "resourceVersion": "2.0",
                  "Stretch": False
                } for i in range(num_f)
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
      "swfPrecision": 0.5,
      "textureGroupId": {
        "name": "Default",
        "path": "texturegroups/Default"
      },
      "type": 0,
      "VTile": False,
      "width": 160
    }
    
    with open(os.path.join(sdir, f'{sprite_name}.yy'), 'w') as f:
        json.dump(yy_data, f, indent=2)
    print(f'Successfully built and packaged {sprite_name} ({num_f} frames)')

save_gmsprite_suite('spr_ms_centurion_fire_chaingun', chaingun_frames, fps=12.0)
save_gmsprite_suite('spr_ms_centurion_attack_melee', melee_frames, fps=8.0)
save_gmsprite_suite('spr_ms_centurion_boost', boost_frames, fps=10.0)
save_gmsprite_suite('spr_ms_centurion_idle_damaged', dmg_frames, fps=6.0)
save_gmsprite_suite('spr_ms_centurion_destroyed', [dest_out], fps=1.0)
print('ALL CENTURION ASSETS PACKAGED SUCCESSFULLY!')
