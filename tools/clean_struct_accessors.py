import os
import re

def clean_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    orig = text
    
    # 1. Replace setter: <obj>[$ <key>] = <val>;
    # e.g. faction_standing[$ _faction_id] = _clamped;
    # -> variable_struct_set(faction_standing, _faction_id, _clamped);
    def repl_set(m):
        obj = m.group(1).strip()
        key = m.group(2).strip()
        val = m.group(3).strip()
        return f"variable_struct_set({obj}, {key}, {val});"

    # Match lines where an assignment happens to struct[$ key]
    # We do line by line for safety
    lines = text.splitlines(keepends=True)
    out_lines = []
    
    set_pat = re.compile(r'^(\s*)([a-zA-Z0-9_\.]+)\s*\[\s*\$\s*([^\]]+)\]\s*=\s*(.+);(\s*)$')
    # Accessor pattern: ([a-zA-Z0-9_\.]+)\s*\[\s*\$\s*([^\]]+)\]
    get_pat = re.compile(r'([a-zA-Z0-9_\.]+)\s*\[\s*\$\s*([^\]]+)\]')

    for line in lines:
        m_set = set_pat.match(line)
        if m_set:
            indent = m_set.group(1)
            obj = m_set.group(2).strip()
            key = m_set.group(3).strip()
            val = m_set.group(4).strip()
            trail = m_set.group(5)
            # If val also contains [$ ...], replace get in val
            val = get_pat.sub(r'variable_struct_get(\1, \2)', val)
            line = f"{indent}variable_struct_set({obj}, {key}, {val});{trail}"
        else:
            # Replace getters
            # Note: handle cases like _arr[i][$ "id"] -> variable_struct_get(_arr[i], "id")
            line = re.sub(r'([a-zA-Z0-9_\.]+(?:\[[^\]\$]+\])?)\s*\[\s*\$\s*([^\]]+)\]', r'variable_struct_get(\1, \2)', line)

        out_lines.append(line)

    new_text = "".join(out_lines)
    if new_text != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f"Cleaned {path}: {orig.count('[$')} -> {new_text.count('[$')} remaining")
    else:
        print(f"No changes in {path}")

# Target key manager files
targets = [
    "objects/obj_FactionManager/Create_0.gml",
    "objects/obj_BlueprintManager/Create_0.gml",
    "objects/obj_NemesisManager/Create_0.gml",
    "objects/obj_BattleManager/Create_0.gml",
    "scripts/scr_nemesis_system/scr_nemesis_system.gml"
]

for t in targets:
    if os.path.exists(t):
        clean_file(t)

