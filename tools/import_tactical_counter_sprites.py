import os
import uuid
import json
import shutil
from PIL import Image

PROJECT_DIR = "/home/tom/GameMakerProjects/MechMakerConcept"
SPRITES_DIR = os.path.join(PROJECT_DIR, "sprites")
YYP_PATH = os.path.join(PROJECT_DIR, "MechMakerConcept.yyp")
SRC_DIR = "/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/tactical_units"

def register_in_yyp(spr_name):
    with open(YYP_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    target_path = f"sprites/{spr_name}/{spr_name}.yy"
    if target_path in content:
        return
    
    idx = content.find('"resources":')
    if idx != -1:
        bracket_idx = content.find('],', idx)
        if bracket_idx != -1:
            new_entry = '    {"id":{"name":"' + spr_name + '","path":"' + target_path + '",},},\n'
            content = content[:bracket_idx] + new_entry + content[bracket_idx:]
            with open(YYP_PATH, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✓ Registered {spr_name} in MechMakerConcept.yyp")

def create_sprite(spr_name, src_png_path):
    im = Image.open(src_png_path)
    w, h = im.size
    
    spr_folder = os.path.join(SPRITES_DIR, spr_name)
    os.makedirs(spr_folder, exist_ok=True)
    layers_folder = os.path.join(spr_folder, "layers")
    os.makedirs(layers_folder, exist_ok=True)
    
    frame_id = str(uuid.uuid4())
    layer_id = str(uuid.uuid4())
    
    # Save frame PNG
    frame_png_path = os.path.join(spr_folder, f"{frame_id}.png")
    im.save(frame_png_path)
    # Also save name.png for convenient preview
    im.save(os.path.join(spr_folder, f"{spr_name}.png"))
    
    # Save layer PNG
    layer_frame_folder = os.path.join(layers_folder, frame_id)
    os.makedirs(layer_frame_folder, exist_ok=True)
    im.save(os.path.join(layer_frame_folder, f"{layer_id}.png"))
    
    # Build YY
    yy_data = {
      "$GMSprite": "v2",
      "%Name": spr_name,
      "bboxMode": 0,
      "bbox_bottom": h - 1,
      "bbox_left": 0,
      "bbox_right": w - 1,
      "bbox_top": 0,
      "collisionKind": 1,
      "collisionTolerance": 0,
      "DynamicTexturePage": False,
      "edgeFiltering": False,
      "For3D": False,
      "frames": [
        {
          "$GMSpriteFrame": "v1",
          "%Name": frame_id,
          "name": frame_id,
          "resourceType": "GMSpriteFrame",
          "resourceVersion": "2.0"
        }
      ],
      "gridX": 0,
      "gridY": 0,
      "height": h,
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
      "name": spr_name,
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
        "%Name": spr_name,
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
        "length": 1.0,
        "lockOrigin": False,
        "moments": {
          "$KeyframeStore<MomentsEventKeyframe>": "",
          "Keyframes": [],
          "resourceType": "KeyframeStore<MomentsEventKeyframe>",
          "resourceVersion": "2.0"
        },
        "name": spr_name,
        "playback": 1,
        "playbackSpeed": 30.0,
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
                        "name": frame_id,
                        "path": f"sprites/{spr_name}/{spr_name}.yy"
                      },
                      "resourceType": "SpriteFrameKeyframe",
                      "resourceVersion": "2.0"
                    }
                  },
                  "Disabled": False,
                  "id": str(uuid.uuid4()),
                  "IsCreationKey": False,
                  "Key": 0.0,
                  "Length": 1.0,
                  "resourceType": "Keyframe<SpriteFrameKeyframe>",
                  "resourceVersion": "2.0",
                  "Stretch": False
                }
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
      "width": w
    }
    
    yy_path = os.path.join(spr_folder, f"{spr_name}.yy")
    with open(yy_path, "w", encoding="utf-8") as f:
        json.dump(yy_data, f, indent=2)
    
    register_in_yyp(spr_name)
    print(f"✓ Created and registered GameMaker sprite: {spr_name} ({w}x{h})")

all_pngs = sorted([f for f in os.listdir(SRC_DIR) if f.endswith(".png")])
print(f"Importing {len(all_pngs)} tactical unit counter sprites into GameMaker project...")
for png_file in all_pngs:
    spr_name = os.path.splitext(png_file)[0]
    src_path = os.path.join(SRC_DIR, png_file)
    create_sprite(spr_name, src_path)

print("All tactical sprites imported and registered successfully!")
