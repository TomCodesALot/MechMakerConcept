import re

# Fix rm_init
with open('rooms/rm_init/RoomCreationCode.gml', 'r', encoding='utf-8') as f:
    s = f.read()
s = s.replace(
    'file_text_write_string(_log_f, "[BOOT] rm_init RoomCreationCode started!\n");',
    'file_text_write_string(_log_f, "[BOOT] rm_init RoomCreationCode started!\\n");'
)
s = s.replace(
    'file_text_write_string(_log_f2, "[BOOT] rm_init finished, room_goto(rm_hq_terminal) called!\n");',
    'file_text_write_string(_log_f2, "[BOOT] rm_init finished, room_goto(rm_hq_terminal) called!\\n");'
)
# Also regex replace any unescaped newline in file_text_write_string
s = re.sub(r'file_text_write_string\(([^,]+),\s*"([^"\n]*)\n"\);', r'file_text_write_string(\1, "\2\\n");', s)
with open('rooms/rm_init/RoomCreationCode.gml', 'w', encoding='utf-8') as f:
    f.write(s)
print('Fixed rm_init/RoomCreationCode.gml')

# Fix obj_HQTerminal/Create_0.gml
with open('objects/obj_HQTerminal/Create_0.gml', 'r', encoding='utf-8') as f:
    s = f.read()
s = re.sub(r'file_text_write_string\(([^,]+),\s*"([^"\n]*)\n"\);', r'file_text_write_string(\1, "\2\\n");', s)
with open('objects/obj_HQTerminal/Create_0.gml', 'w', encoding='utf-8') as f:
    f.write(s)
print('Fixed obj_HQTerminal/Create_0.gml')

# Fix obj_NemesisManager/Create_0.gml
with open('objects/obj_NemesisManager/Create_0.gml', 'r', encoding='utf-8') as f:
    s = f.read()
s = re.sub(r'file_text_write_string\(([^,]+),\s*"([^"\n]*)\n"\);', r'file_text_write_string(\1, "\2\\n");', s)
with open('objects/obj_NemesisManager/Create_0.gml', 'w', encoding='utf-8') as f:
    f.write(s)
print('Fixed obj_NemesisManager/Create_0.gml')

# Fix obj_HQTerminal/Draw_64.gml
with open('objects/obj_HQTerminal/Draw_64.gml', 'r', encoding='utf-8') as f:
    s = f.read()
s = re.sub(r'file_text_write_string\(([^,]+),\s*"([^"\n]*)\n"\);', r'file_text_write_string(\1, "\2\\n");', s)

# Multiline desc in protocols
p1_old = '''desc: "-40% Chassis Fabrication Costs
+1 Active Manufacturing Bay
3.0x Planetary Mining Yield Multiplier"'''
p1_new = 'desc: "-40% Chassis Fabrication Costs\\n+1 Active Manufacturing Bay\\n3.0x Planetary Mining Yield Multiplier"'

p2_old = '''desc: "+50% Orbital Strike Bombardment Dmg
+25,000 Warship Hull Integrity
+35% Allied Grid Armor Defense"'''
p2_new = 'desc: "+50% Orbital Strike Bombardment Dmg\\n+25,000 Warship Hull Integrity\\n+35% Allied Grid Armor Defense"'

p3_old = '''desc: "Instant 0-Turn Planetary Tachyon Fold
Nullifies Corporate Sabotage
Siphons +2% Market Share Every 4T"'''
p3_new = 'desc: "Instant 0-Turn Planetary Tachyon Fold\\nNullifies Corporate Sabotage\\nSiphons +2% Market Share Every 4T"'

s = s.replace(p1_old, p1_new)
s = s.replace(p2_old, p2_new)
s = s.replace(p3_old, p3_new)

# In case line 5 has file_text_write_string with multiline
s = re.sub(r'file_text_write_string\(_log_f,\s*"\[BOOT\] obj_HQTerminal Draw_64 FIRST FRAME EXECUTED! [^"\n]*"\s*\+\s*string\([^)]+\)\s*\+\s*"[^"\n]*"\s*\+\s*string\([^)]+\)\s*\+\s*"\n"\);',
           r'file_text_write_string(_log_f, "[BOOT] obj_HQTerminal Draw_64 FIRST FRAME EXECUTED! gw=" + string(display_get_gui_width()) + " gh=" + string(display_get_gui_height()) + "\\n");',
           s)

with open('objects/obj_HQTerminal/Draw_64.gml', 'w', encoding='utf-8') as f:
    f.write(s)
print('Fixed obj_HQTerminal/Draw_64.gml')
