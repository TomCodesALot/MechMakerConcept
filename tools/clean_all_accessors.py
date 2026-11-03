import os
import re

targets = [
    "objects/obj_HQTerminal/Create_0.gml",
    "objects/obj_MobileSuit/Create_0.gml",
    "objects/obj_BattleManager/Step_0.gml",
    "objects/obj_BattleManager/Draw_64.gml",
    "objects/obj_AudioManager/Create_0.gml",
    "scripts/scr_ms_state_machine/scr_ms_state_machine.gml",
    "scripts/scr_save_system/scr_save_system.gml",
    "scripts/scr_alloy_color_synthesis/scr_alloy_color_synthesis.gml",
    "scripts/scr_alloy_discovery_codex/scr_alloy_discovery_codex.gml",
    "scripts/scr_draw_animated_mobile_suit/scr_draw_animated_mobile_suit.gml"
]

set_pat = re.compile(r'^(\s*)([a-zA-Z0-9_\.]+)\s*\[\s*\$\s*([^\]]+)\]\s*=\s*(.+);(\s*)$')
get_pat = re.compile(r'([a-zA-Z0-9_\.]+)\s*\[\s*\$\s*([^\]]+)\]')

for t in targets:
    if not os.path.exists(t): continue
    with open(t, 'r', encoding='utf-8') as f:
        text = f.read()
    orig = text
    lines = text.splitlines(keepends=True)
    out_lines = []
    for line in lines:
        m_set = set_pat.match(line)
        if m_set:
            indent = m_set.group(1)
            obj = m_set.group(2).strip()
            key = m_set.group(3).strip()
            val = m_set.group(4).strip()
            trail = m_set.group(5)
            val = get_pat.sub(r'variable_struct_get(\1, \2)', val)
            line = f"{indent}variable_struct_set({obj}, {key}, {val});{trail}"
        else:
            line = re.sub(r'([a-zA-Z0-9_\.]+(?:\[[^\]\$]+\])?)\s*\[\s*\$\s*([^\]]+)\]', r'variable_struct_get(\1, \2)', line)
        out_lines.append(line)
    new_text = "".join(out_lines)
    if new_text != orig:
        with open(t, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f"Cleaned {t}: {orig.count('[$')} -> {new_text.count('[$')} remaining")

