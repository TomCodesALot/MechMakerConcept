import os

# 1. Fix obj_BlueprintManager/Create_0.gml
p_bm = "objects/obj_BlueprintManager/Create_0.gml"
with open(p_bm, 'r', encoding='utf-8') as f:
    text_bm = f.read()

target_bm = '''        var _f_bp = file_text_open_read("mobile_suits_timeline.json");
        var _json_bp = "";
        while (!file_text_eof(_f_bp)) {
            _json_bp += file_text_readln(_f_bp);
        }
        file_text_close(_f_bp);
        var _timeline_bp = json_parse(_json_bp);'''

repl_bm = '''        var _buf_bp = buffer_load("mobile_suits_timeline.json");
        var _json_bp = buffer_read(_buf_bp, buffer_string);
        buffer_delete(_buf_bp);
        var _timeline_bp = json_parse(_json_bp);'''

assert target_bm in text_bm, "Target BM not found"
text_bm = text_bm.replace(target_bm, repl_bm, 1)
with open(p_bm, 'w', encoding='utf-8') as f:
    f.write(text_bm)
print("Fixed BlueprintManager file reading!")

# 2. Fix obj_FactionManager/Create_0.gml
p_fm = "objects/obj_FactionManager/Create_0.gml"
with open(p_fm, 'r', encoding='utf-8') as f:
    text_fm = f.read()

target_fm1 = '''        var _f = file_text_open_read("factions_lore.json");
        var _json_str = "";
        while (!file_text_eof(_f)) {
            _json_str += file_text_readln(_f);
        }
        file_text_close(_f);
        factions_lore_data = json_parse(_json_str);'''

repl_fm1 = '''        var _buf_fl = buffer_load("factions_lore.json");
        var _json_str = buffer_read(_buf_fl, buffer_string);
        buffer_delete(_buf_fl);
        factions_lore_data = json_parse(_json_str);'''

target_fm2 = '''        var _f2 = file_text_open_read("mobile_suits_timeline.json");
        var _json_str2 = "";
        while (!file_text_eof(_f2)) {
            _json_str2 += file_text_readln(_f2);
        }
        file_text_close(_f2);
        var _t_parsed = json_parse(_json_str2);'''

repl_fm2 = '''        var _buf_tl = buffer_load("mobile_suits_timeline.json");
        var _json_str2 = buffer_read(_buf_tl, buffer_string);
        buffer_delete(_buf_tl);
        var _t_parsed = json_parse(_json_str2);'''

assert target_fm1 in text_fm, "Target FM1 not found"
assert target_fm2 in text_fm, "Target FM2 not found"
text_fm = text_fm.replace(target_fm1, repl_fm1, 1).replace(target_fm2, repl_fm2, 1)
with open(p_fm, 'w', encoding='utf-8') as f:
    f.write(text_fm)
print("Fixed FactionManager file reading!")

# 3. Fix obj_GameManager/Create_0.gml
p_gm = "objects/obj_GameManager/Create_0.gml"
with open(p_gm, 'r', encoding='utf-8') as f:
    text_gm = f.read()

target_gm1 = '''            var _file = file_text_open_read("narrative_events.json");
            var _str = "";
            while (!file_text_eof(_file)) _str += file_text_readln(_file);
            file_text_close(_file);
            var _data = json_parse(_str);'''

repl_gm1 = '''            var _buf_ne = buffer_load("narrative_events.json");
            var _str = buffer_read(_buf_ne, buffer_string);
            buffer_delete(_buf_ne);
            var _data = json_parse(_str);'''

target_gm2 = '''        var _f_pt = file_text_open_read(_res_pt);
        var _json_pt = "";
        while (!file_text_eof(_f_pt)) {
            _json_pt += file_text_readln(_f_pt);
        }
        file_text_close(_f_pt);
        var _pt_parsed = json_parse(_json_pt);'''

repl_gm2 = '''        var _buf_pt = buffer_load(_res_pt);
        var _json_pt = buffer_read(_buf_pt, buffer_string);
        buffer_delete(_buf_pt);
        var _pt_parsed = json_parse(_json_pt);'''

target_gm3 = '''        var _f_sn = file_text_open_read(_res_sn);
        var _json_sn = "";
        while (!file_text_eof(_f_sn)) {
            _json_sn += file_text_readln(_f_sn);
        }
        file_text_close(_f_sn);
        var _sn_parsed = json_parse(_json_sn);'''

repl_gm3 = '''        var _buf_sn = buffer_load(_res_sn);
        var _json_sn = buffer_read(_buf_sn, buffer_string);
        buffer_delete(_buf_sn);
        var _sn_parsed = json_parse(_json_sn);'''

assert target_gm1 in text_gm, "Target GM1 not found"
assert target_gm2 in text_gm, "Target GM2 not found"
assert target_gm3 in text_gm, "Target GM3 not found"
text_gm = text_gm.replace(target_gm1, repl_gm1, 1).replace(target_gm2, repl_gm2, 1).replace(target_gm3, repl_gm3, 1)
with open(p_gm, 'w', encoding='utf-8') as f:
    f.write(text_gm)
print("Fixed GameManager file reading!")

