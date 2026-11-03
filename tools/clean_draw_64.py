import re

path = "objects/obj_HQTerminal/Draw_64.gml"
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

orig = text
lines = text.splitlines(keepends=True)
out_lines = []

set_pat = re.compile(r'^(\s*)([a-zA-Z0-9_\.]+)\s*\[\s*\$\s*([^\]]+)\]\s*=\s*(.+);(\s*)$')
get_pat = re.compile(r'([a-zA-Z0-9_\.]+)\s*\[\s*\$\s*([^\]]+)\]')

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
with open(path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print(f"Cleaned Draw_64.gml: {orig.count('[$')} -> {new_text.count('[$')} remaining")
