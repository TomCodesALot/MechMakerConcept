from PIL import Image, ImageFont, ImageDraw
import string

font_path = '/home/tom/.local/share/Steam/steamapps/compatdata/1670460/pfx/drive_c/windows/Fonts/tahoma.ttf'

# Try sizes 10, 11, 12, 13
chars = string.ascii_letters + string.digits + " _.:;=()[]{}<>-+/*#\"'\\,\n"

def build_templates(font_size):
    font = ImageFont.truetype(font_path, font_size)
    templates = {}
    for c in chars:
        im = Image.new('L', (40, 30), color=255)
        d = ImageDraw.Draw(im)
        d.text((5, 5), c, fill=0, font=font)
        # get bbox
        bbox = im.getbbox()
        if bbox:
            templates[c] = (im.crop(bbox), font.getlength(c))
        else:
            templates[c] = (Image.new('L', (4, 10), color=255), font.getlength(c))
    return templates, font

im_err = Image.open('/home/tom/.gemini/antigravity-ide/brain/a9197ef4-c206-4eb1-b4b4-83dfffe898d6/error_text_box.png').convert('L')
w, h = im_err.size

# Let's find best match font size
# Check height of lowercase 'e' or 'o' in error_text_box
# Line 3 height is 8 pixels (caps+descenders), x-height is ~6-7 pixels -> font_size ~ 11 or 12
templates, font = build_templates(11)

# Let's simple slide matching or test common phrases
phrases = [
    "FATAL ERROR in",
    "action number 1",
    "of Create Event",
    "for object",
    "Execution Error",
    "Variable Index",
    "Variable not set",
    "unable to find instance",
    "gml_Object_obj_GameManager_Create_0",
    "gml_Object_obj_FactionManager_Create_0",
    "gml_Object_obj_BlueprintManager_Create_0",
    "gml_Object_obj_NemesisManager_Create_0",
    "gml_Object_obj_HQTerminal_Create_0",
    "gml_Object_obj_BattleManager_Create_0",
    "gml_Script_scr_load_blueprint",
    "gml_Script_scr_save_system",
    "gml_Script_scr_alloy_color_synthesis",
    "gml_Script_scr_alloy_discovery_codex",
    "gml_Script_scr_draw_animated_mobile_suit",
    "gml_Script_scr_snes_ui"
]

print("Scanning phrases...")
for phrase in phrases:
    # render phrase
    test_im = Image.new('L', (int(font.getlength(phrase)) + 20, 20), color=255)
    d = ImageDraw.Draw(test_im)
    d.text((5, 2), phrase, fill=0, font=font)
    tb = test_im.getbbox()
    if not tb:
        continue
    t_crop = test_im.crop(tb)
    tw, th = t_crop.size
    
    # search in im_err
    best_score = 999999
    best_pos = None
    for y in range(0, min(150, h - th), 2):
        for x in range(0, w - tw, 4):
            sub = im_err.crop((x, y, x + tw, y + th))
            # calc diff
            diff = sum(abs(p1 - p2) for p1, p2 in zip(sub.getdata(), t_crop.getdata())) // (tw * th)
            if diff < best_score:
                best_score = diff
                best_pos = (x, y)
    if best_score < 40: # good match threshold
        print(f"MATCH: '{phrase}' at pos {best_pos} (score: {best_score})")
