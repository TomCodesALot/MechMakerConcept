import os
import glob
import re

def fix_custom_mech_sprites():
    custom_sprites = glob.glob('sprites/spr_ms_custom_*/*.yy')
    print(f"Fixing {len(custom_sprites)} custom mech sprites...")
    for s in custom_sprites:
        with open(s, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix missing tags
        content = re.sub(r'{\s*"":"v2"', '{\n  "$GMSprite":"v2"', content)
        content = content.replace('{"":"v1",', '{"$GMSpriteFrame":"v1",')
        content = content.replace('{"":"",', '{"$GMImageLayer":"",')
        content = content.replace('"":"v1",', '"$GMSequence":"v1",')
        content = content.replace('"<MessageEventKeyframe>":""', '"$KeyframeStore<MessageEventKeyframe>":""')
        content = content.replace('"<MomentsEventKeyframe>":""', '"$KeyframeStore<MomentsEventKeyframe>":""')
        content = content.replace('{"":"","builtinName":0', '{"$GMSpriteFramesTrack":"","builtinName":0')
        content = content.replace('"<SpriteFrameKeyframe>":""', '"$KeyframeStore<SpriteFrameKeyframe>":""')
        content = content.replace('{"<SpriteFrameKeyframe>":""', '{"$Keyframe<SpriteFrameKeyframe>":""')
        content = content.replace('{"0":{"":"",', '{"0":{"$SpriteFrameKeyframe":"",')

        with open(s, 'w', encoding='utf-8') as f:
            f.write(content)

def fix_sprite_layers():
    sprites = glob.glob('sprites/*/*.yy')
    count = 0
    for s in sprites:
        with open(s, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content.replace('"$GMImageLayer":"v1"', '"$GMImageLayer":""')
        new_content = new_content.replace('"$GMImageLayer": "v1"', '"$GMImageLayer": ""')
        
        if new_content != content:
            count += 1
            with open(s, 'w', encoding='utf-8') as f:
                f.write(new_content)
    print(f"Fixed $GMImageLayer in {count} sprites.")

def fix_sprite_sequences():
    sprites = glob.glob('sprites/*/*.yy')
    count = 0
    for s in sprites:
        with open(s, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if sequence is missing resourceType
        seq_idx = content.find('"sequence"')
        if seq_idx == -1:
            continue
        
        seq_part = content[seq_idx:seq_idx+1200]
        if '"resourceType":"GMSequence"' not in seq_part and '"resourceType": "GMSequence"' not in seq_part:
            # Insert after playbackSpeedType
            pattern = r'("playbackSpeedType"\s*:\s*[0-9]+,)'
            replacement = r'\1\n    "resourceType": "GMSequence",\n    "resourceVersion": "2.0",'
            new_content = re.sub(pattern, replacement, content, count=1)
            if new_content != content:
                count += 1
                with open(s, 'w', encoding='utf-8') as f:
                    f.write(new_content)
    print(f"Fixed missing sequence resourceType in {count} sprites.")

def fix_sounds():
    sounds = glob.glob('sounds/*/*.yy')
    count = 0
    for snd in sounds:
        with open(snd, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '"exportDir"' not in content:
            # Insert exportDir after duration
            pattern = r'("duration"\s*:\s*[0-9\.]+,)'
            replacement = r'\1\n  "exportDir":"", '
            new_content = re.sub(pattern, replacement, content, count=1)
            if new_content != content:
                count += 1
                with open(snd, 'w', encoding='utf-8') as f:
                    f.write(new_content)
    print(f"Fixed exportDir in {count} sounds.")


def fix_sprite_tracks():
    sprites = glob.glob('sprites/*/*.yy')
    count = 0
    for s in sprites:
        with open(s, 'r', encoding='utf-8') as f:
            content = f.read()
        if '"resourceType":"GMSpriteFramesTrack"' in content or '"resourceType": "GMSpriteFramesTrack"' in content:
            if '"spriteId"' not in content:
                content = content.replace('"resourceType":"GMSpriteFramesTrack","resourceVersion":"2.0",', '"resourceType":"GMSpriteFramesTrack","resourceVersion":"2.0","spriteId":null,')
                content = content.replace('"resourceType": "GMSpriteFramesTrack",
                    "resourceVersion": "2.0",', '"resourceType": "GMSpriteFramesTrack",
                    "resourceVersion": "2.0",
                    "spriteId": null,')
                count += 1
                with open(s, 'w', encoding='utf-8') as f:
                    f.write(content)
    print(f"Fixed missing spriteId in {count} sprite tracks.")

if __name__ == '__main__':
    fix_sprite_tracks()
    fix_custom_mech_sprites()
    fix_sprite_layers()
    fix_sprite_sequences()
    fix_sounds()
