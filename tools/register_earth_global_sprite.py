import os, shutil

spr_name = "spr_map_earth_global"
spr_dir = os.path.join("sprites", spr_name)
os.makedirs(spr_dir, exist_ok=True)

# Copy clean cropped image
src_img = "/home/tom/.gemini/antigravity-ide/brain/b6b456aa-e22a-4f4e-b05e-c83eb2c3964e/earth_global_clean.png"
dst_img = os.path.join(spr_dir, spr_name + ".png")
shutil.copyfile(src_img, dst_img)

# Copy YY metadata from spr_map_earth_theater and adjust name
yy_src = os.path.join("sprites", "spr_map_earth_theater", "spr_map_earth_theater.yy")
with open(yy_src, "r") as f:
    yy_content = f.read()

yy_content = yy_content.replace("spr_map_earth_theater", spr_name)
with open(os.path.join(spr_dir, spr_name + ".yy"), "w") as f:
    f.write(yy_content)

print(f"Created sprite directory and files for {spr_name}")

# Register in MechMakerConcept.yyp if not present
with open("MechMakerConcept.yyp", "r") as f:
    yyp_text = f.read()

if spr_name not in yyp_text:
    res_entry = f'    {{"id":{{"name":"{spr_name}","path":"sprites/{spr_name}/{spr_name}.yy",}},}},'
    idx = yyp_text.find('"resources": [')
    if idx != -1:
        insert_pos = idx + len('"resources": [') + 1
        yyp_text = yyp_text[:insert_pos] + "\n" + res_entry + yyp_text[insert_pos:]
        with open("MechMakerConcept.yyp", "w") as f:
            f.write(yyp_text)
        print(f"Registered {spr_name} in MechMakerConcept.yyp")
else:
    print(f"{spr_name} already in MechMakerConcept.yyp")
