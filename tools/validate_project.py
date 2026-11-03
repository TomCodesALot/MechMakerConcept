# -*- coding: utf-8 -*-
import glob
import re
import os

errors = []

# =========================================================================
# 1. SPRITE & SOUND .YY SCHEMA CHECKS
# =========================================================================
sprites = glob.glob('sprites/*/*.yy')
for s in sprites:
    with open(s) as f:
        t = f.read()
    
    if not re.search(r'"\$GMSprite"\s*:\s*"v2"', t):
        errors.append((s, 'Missing or bad $GMSprite tag'))
    if '"$GMImageLayer":"v1"' in t or '"$GMImageLayer": "v1"' in t:
        errors.append((s, 'Layer version is v1'))
    if '"$GMImageLayer"' not in t:
        errors.append((s, 'Missing $GMImageLayer'))
    if '"$GMSequence"' not in t:
        errors.append((s, 'Missing $GMSequence'))
    if '"resourceType": "GMSequence"' not in t and '"resourceType":"GMSequence"' not in t:
        errors.append((s, 'Missing GMSequence resourceType in sequence'))
    if '"$GMSpriteFramesTrack"' not in t:
        errors.append((s, 'Missing $GMSpriteFramesTrack'))
    if '"$KeyframeStore<SpriteFrameKeyframe>"' not in t:
        errors.append((s, 'Missing $KeyframeStore<SpriteFrameKeyframe>'))
    if '"$Keyframe<SpriteFrameKeyframe>"' not in t:
        errors.append((s, 'Missing $Keyframe<SpriteFrameKeyframe>'))
    if '"$SpriteFrameKeyframe"' not in t:
        errors.append((s, 'Missing $SpriteFrameKeyframe'))
    if '"swfPrecision"' not in t:
        errors.append((s, 'Missing swfPrecision'))
        
    for i, line in enumerate(t.split('\n')):
        line_s = line.strip()
        if line_s.startswith('"":'):
            errors.append((s, f'Line {i+1} has empty key: {line_s}'))
        if line_s.startswith('"<') and not line_s.startswith('"$Keyframe'):
            errors.append((s, f'Line {i+1} has bad key without $: {line_s}'))

sounds = glob.glob('sounds/*/*.yy')
for snd in sounds:
    snd_name = os.path.basename(os.path.dirname(snd))
    with open(snd) as f:
        t = f.read()
    if '"exportDir"' not in t:
        errors.append((snd, 'Missing exportDir'))
    if f'"name":"{snd_name}"' not in t and f'"name": "{snd_name}"' not in t:
        errors.append((snd, f'Missing root name: {snd_name}'))
    if '"$GMSound"' not in t:
        errors.append((snd, 'Missing $GMSound'))

# =========================================================================
# 2. GML STATIC CODE ANALYSIS (Braces, Reserved Words, Read-Only Identifiers)
# =========================================================================
gml_files = glob.glob('objects/**/*.gml', recursive=True) + glob.glob('scripts/**/*.gml', recursive=True)

readonly_assign_pattern = re.compile(r'\b(\w+)\.id\s*=(?!=)')

def is_var_decl_reserved(line):
    m = re.search(r'\bvar\s+([^=;]+)', line)
    if m:
        decl_part = m.group(1)
        names = [n.strip() for n in decl_part.split(',')]
        if 'pi' in names:
            return True
    return False

for gml_path in gml_files:
    with open(gml_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    stack = []
    in_multiline_comment = False
    
    for i, line in enumerate(lines):
        clean_line = line.strip()
        
        # Strip comments
        if '/*' in clean_line and '*/' in clean_line:
            clean_line = re.sub(r'/\*.*?\*/', '', clean_line)
        elif '/*' in clean_line:
            in_multiline_comment = True
            clean_line = clean_line[:clean_line.find('/*')]
        elif '*/' in clean_line:
            in_multiline_comment = False
            clean_line = clean_line[clean_line.find('*/')+2:]
        elif in_multiline_comment:
            continue
            
        if '//' in clean_line:
            clean_line = clean_line[:clean_line.find('//')]
            
        # Check readonly assignment to .id
        m_id = readonly_assign_pattern.search(clean_line)
        if m_id:
            errors.append((gml_path, f'Line {i+1}: Cannot assign to readonly instance variable: {clean_line}'))
            
        # Check reserved identifiers
        if is_var_decl_reserved(clean_line):
            errors.append((gml_path, f'Line {i+1}: Cannot declare reserved identifier as var: {clean_line}'))
            
        # Check brace balance
        for ch in clean_line:
            if ch == '{':
                stack.append(i + 1)
            elif ch == '}':
                if stack:
                    stack.pop()
                else:
                    errors.append((gml_path, f'Line {i+1}: Unexpected closing brace "}}" (underflow)'))
                    
    if stack:
        errors.append((gml_path, f'Unclosed brace(s) opened at line(s): {stack}'))


# =========================================================================
# =========================================================================
# 3. LOCAL VARIABLE SCOPE & USED-BEFORE-DECLARATION CHECK
# =========================================================================
for gml_path in gml_files:
    if "legacy_backup" in gml_path:
        continue
    with open(gml_path, "r", encoding="utf-8", errors="ignore") as f:
        glines = f.readlines()
        
    declared = set()
    for idx, gline in enumerate(glines):
        clean = gline.strip()
        if clean.startswith("//") or clean.startswith("/*"):
            continue
        clean = re.sub(r"\"[^\"]*\"", "\"\"", clean)
        
        # Function arguments
        func_matches = re.findall(r"function(?:\s+[a-zA-Z0-9_]+)?\s*\(([^)]*)\)", clean)
        for fm in func_matches:
            for arg in fm.split(","):
                arg_name = arg.strip().split("=")[0].strip()
                if arg_name.startswith("_"):
                    declared.add(arg_name)
                    
        # Static definitions
        static_matches = re.findall(r"static\s+([a-zA-Z0-9_]+)", clean)
        for sm in static_matches:
            if sm.startswith("_"):
                declared.add(sm)
                
        # Catch clauses
        catch_matches = re.findall(r"catch\s*\(([^)]*)\)", clean)
        for cm in catch_matches:
            cname = cm.strip()
            if cname.startswith("_"):
                declared.add(cname)
                
        # var declarations
        decl_matches = re.findall(r"\bvar\s+([^;]+)", clean)
        for dm in decl_matches:
            for v in dm.split(","):
                v_name = v.strip().split()[0] if v.strip() else ""
                v_name = re.sub(r"[^a-zA-Z0-9_]", "", v_name)
                if v_name.startswith("_"):
                    declared.add(v_name)
                    
        usages = re.findall(r"\b(_[a-zA-Z0-9_]+)\b", clean)
        for u in usages:
            if f"var {u}" in clean or f"var  {u}" in clean or f", {u}" in clean or f",{u}" in clean:
                continue
            if u not in declared:
                errors.append((gml_path, f"Line {idx+1}: Local variable {u} used before declaration: {clean}"))

print(f"Total errors found: {len(errors)}")
for err in errors:
    print("  ", err)
