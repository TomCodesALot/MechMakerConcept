import re

BM_PATH = "objects/obj_BattleManager/Create_0.gml"

with open(BM_PATH, "r") as f:
    content = f.read()

target = """    if (_u.is_destroyed) {
        return spr_ms_ironclad_destroyed;
    }"""

replacement = """    if (_u.is_destroyed) {
        return spr_ms_ironclad_destroyed;
    }

    // Direct sprite asset override if defined on unit (docs/29)
    if (variable_struct_exists(_u, "sprite_asset") && sprite_exists(_u.sprite_asset)) {
        return _u.sprite_asset;
    }"""

assert target in content, "target not found in obj_BattleManager!"
content = content.replace(target, replacement, 1)

# Also add default front idles for the 4 new archetypes
target_idles = """        if (_type == "siegebreaker" || _type == "behemoth") return spr_ms_siegebreaker_anchor;
        return spr_ms_ironclad_idle;"""

replacement_idles = """        if (_type == "siegebreaker" || _type == "behemoth") return spr_ms_siegebreaker_anchor;
        if (_type == "ballista") return spr_ms_ballista_idle;
        if (_type == "zephyr") return spr_ms_zephyr_idle;
        if (_type == "gorgon") return spr_ms_gorgon_idle;
        if (_type == "kage" || _type == "shinobi") return spr_ms_kage_idle;
        return spr_ms_ironclad_idle;"""

assert target_idles in content, "target_idles not found in obj_BattleManager!"
content = content.replace(target_idles, replacement_idles, 1)

with open(BM_PATH, "w") as f:
    f.write(content)

print("Updated obj_BattleManager with expanded sprite resolution!")
