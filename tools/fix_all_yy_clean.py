import os
import glob
import re

def fix_all_custom_sprites():
    custom_sprites = sorted(glob.glob('sprites/spr_ms_custom_*/*.yy'))
    print(f"Fixing {len(custom_sprites)} custom sprites...")
    for path in custom_sprites:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        in_sequence = False
        in_layers = False
        in_tracks = False
        in_keyframes = False
        in_channels = False
        
        for line in lines:
            stripped = line.strip()
            
            # Root type tag
            if stripped.startswith('"": "v2"') or stripped.startswith('"":"v2"'):
                line = line.replace('"": "v2"', '"$GMSprite": "v2"').replace('"":"v2"', '"$GMSprite": "v2"')
            
            # State tracking
            if '"layers":' in stripped:
                in_layers = True
            elif in_layers and '],' in stripped:
                in_layers = False
                
            if '"sequence":' in stripped:
                in_sequence = True
            elif in_sequence and stripped == '},':
                in_sequence = False
                
            if '"tracks":' in stripped:
                in_tracks = True
            elif in_tracks and stripped == '],':
                in_tracks = False
                
            if '"Keyframes":' in stripped:
                in_keyframes = True
            elif in_keyframes and stripped == '],':
                in_keyframes = False
                
            if '"Channels":' in stripped:
                in_channels = True
            elif in_channels and '},' in stripped:
                in_channels = False
            
            # Replacements
            if stripped.startswith('"": "v1"') or stripped.startswith('"":"v1"'):
                if not in_sequence:
                    line = line.replace('"": "v1"', '"$GMSpriteFrame": "v1"').replace('"":"v1"', '"$GMSpriteFrame": "v1"')
                else:
                    line = line.replace('"": "v1"', '"$GMSequence": "v1"').replace('"":"v1"', '"$GMSequence": "v1"')
                    
            if (stripped.startswith('"": ""') or stripped.startswith('"":""')) and in_layers:
                line = line.replace('"": ""', '"$GMImageLayer": ""').replace('"":""', '"$GMImageLayer": ""')
                
            if '<MessageEventKeyframe>' in stripped:
                line = line.replace('"<MessageEventKeyframe>": ""', '"$KeyframeStore<MessageEventKeyframe>": ""').replace('"<MessageEventKeyframe>":""', '"$KeyframeStore<MessageEventKeyframe>":""')
                
            if '<MomentsEventKeyframe>' in stripped:
                line = line.replace('"<MomentsEventKeyframe>": ""', '"$KeyframeStore<MomentsEventKeyframe>": ""').replace('"<MomentsEventKeyframe>":""', '"$KeyframeStore<MomentsEventKeyframe>":""')
                
            if in_tracks and (stripped.startswith('"": ""') or stripped.startswith('"":""')):
                if not in_channels:
                    line = line.replace('"": ""', '"$GMSpriteFramesTrack": ""').replace('"":""', '"$GMSpriteFramesTrack": ""')
                    
            if in_channels and (stripped.startswith('"": ""') or stripped.startswith('"":""')):
                line = line.replace('"": ""', '"$SpriteFrameKeyframe": ""').replace('"":""', '"$SpriteFrameKeyframe": ""')
                
            if '<SpriteFrameKeyframe>' in stripped:
                if not in_keyframes:
                    line = line.replace('"<SpriteFrameKeyframe>": ""', '"$KeyframeStore<SpriteFrameKeyframe>": ""').replace('"<SpriteFrameKeyframe>":""', '"$KeyframeStore<SpriteFrameKeyframe>":""')
                else:
                    line = line.replace('"<SpriteFrameKeyframe>": ""', '"$Keyframe<SpriteFrameKeyframe>": ""').replace('"<SpriteFrameKeyframe>":""', '"$Keyframe<SpriteFrameKeyframe>":""')
            
            new_lines.append(line)
            
            # Sequence resourceType injection
            if in_sequence and ('"playbackSpeedType":' in stripped or '"playbackSpeedType": ' in stripped):
                # check if next line already has resourceType
                # handled by sequence pass
                pass
                
        content = "".join(new_lines)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

fix_all_custom_sprites()
