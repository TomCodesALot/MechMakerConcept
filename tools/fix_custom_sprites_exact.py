import glob
import re

for s in glob.glob('sprites/spr_ms_custom_*/*.yy'):
    with open(s, 'r', encoding='utf-8') as f:
        t = f.read()

    # If it was accidentally given Keyframe instead of KeyframeStore for keyframes:
    t = re.sub(r'"keyframes":\s*\{\s*"\$Keyframe<SpriteFrameKeyframe>":\s*""', '"keyframes": {\n          "$KeyframeStore<SpriteFrameKeyframe>": ""', t)
    
    # Ensure tracks has GMSpriteFramesTrack
    t = re.sub(r'\{\s*"\$GMImageLayer":\s*"",\s*"builtinName":', '{\n        "$GMSpriteFramesTrack": "",\n        "builtinName":', t)
    
    # In channels ensure SpriteFrameKeyframe
    t = re.sub(r'"0":\s*\{\s*"\$GMImageLayer":\s*""', '"0": {\n                  "$SpriteFrameKeyframe": ""', t)
    
    with open(s, 'w', encoding='utf-8') as f:
        f.write(t)
    print(f"Updated {s}")
