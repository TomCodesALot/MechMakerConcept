with open('objects/obj_BattleManager/Create_0.gml', 'r') as f:
    text = f.read()

old_block = """    // Direct sprite asset override if defined on unit (docs/29)
    if (variable_struct_exists(_u, "sprite_asset") && sprite_exists(_u.sprite_asset)) {
        if (_is_back) {
            var _spr_name = sprite_get_name(_u.sprite_asset);
            var _back_spr_name = string_replace(_spr_name, "_idle", "_back_idle");
            var _back_asset = asset_get_index(_back_spr_name);
            if (_back_asset != -1 && sprite_exists(_back_asset)) {
                return _back_asset;
            }
        } else {
            return _u.sprite_asset;
        }
    }"""

new_block = """    // 1. Direct sprite asset override if defined on unit (docs/29)
    if (variable_struct_exists(_u, "sprite_asset") && sprite_exists(_u.sprite_asset)) {
        if (_is_back) {
            var _spr_name = sprite_get_name(_u.sprite_asset);
            var _back_spr_name = string_replace(_spr_name, "_idle", "_back_idle");
            var _back_asset = asset_get_index(_back_spr_name);
            if (_back_asset != -1 && sprite_exists(_back_asset)) {
                return _back_asset;
            }
        } else {
            return _u.sprite_asset;
        }
    }

    // 2. Dynamic catalog lookup from obj_GameManager (Universal 100-Suit Catalog)
    if (instance_exists(obj_GameManager) && variable_instance_exists(obj_GameManager, "get_mobile_suit")) {
        var _cat_entry = obj_GameManager.get_mobile_suit(_type);
        if (!is_undefined(_cat_entry) && is_struct(_cat_entry) && variable_struct_exists(_cat_entry, "sprite_asset")) {
            var _c_asset = _cat_entry.sprite_asset;
            var _c_idx = is_string(_c_asset) ? asset_get_index(_c_asset) : _c_asset;
            if (_c_idx != -1 && sprite_exists(_c_idx)) {
                if (_is_back) {
                    var _s_name = sprite_get_name(_c_idx);
                    var _b_name = string_replace(_s_name, "_idle", "_back_idle");
                    var _b_idx = asset_get_index(_b_name);
                    if (_b_idx != -1 && sprite_exists(_b_idx)) return _b_idx;
                }
                return _c_idx;
            }
        }
    }

    // 3. Dynamic naming convention lookup (spr_ms_<type>_idle / _back_idle)
    var _cand_idle = asset_get_index("spr_ms_" + _type + "_idle");
    if (_cand_idle != -1 && sprite_exists(_cand_idle)) {
        if (_is_back) {
            var _cand_back = asset_get_index("spr_ms_" + _type + "_back_idle");
            if (_cand_back != -1 && sprite_exists(_cand_back)) return _cand_back;
        }
        return _cand_idle;
    }"""

assert old_block in text, "old_block not found in Create_0.gml"
text = text.replace(old_block, new_block, 1)

with open('objects/obj_BattleManager/Create_0.gml', 'w') as f:
    f.write(text)

print("get_unit_sprite successfully enhanced with dynamic catalog and naming lookup!")
