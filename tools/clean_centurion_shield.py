import os
from PIL import Image

fdir = 'sprites/spr_ms_centurion_idle'
frame_ids = [
    'e283773f-bb6e-48e5-93e5-3e3803458f0b',
    'f0c4c103-85f6-48ef-9ba4-9cbf6e678910',
    'f7e30520-bf8f-45f6-b096-e65666cd1856',
    '9a42f0fa-2c6f-4cea-8605-1026b640bfa4'
]
layer_id = '7921f846-eaab-485b-bb28-ab87010ddd7c'

for fid in frame_ids:
    root_p = os.path.join(fdir, f'{fid}.png')
    layer_p = os.path.join(fdir, 'layers', fid, f'{layer_id}.png')
    
    im = Image.open(root_p).convert('RGBA')
    # Clean shield area between x: 33 to 58, y: 58 to 76
    # Sample gradient from top (y=57) and bottom (y=77)
    for y in range(58, 77):
        prog = (y - 58) / 19.0
        for x in range(33, 59):
            r, g, b, a = im.getpixel((x, y))
            if a > 100:
                # Base armor fill with subtle horizontal gradient
                base_r = int(96 + prog * 6 + (x - 33) * 0.4)
                base_g = int(92 + prog * 6 + (x - 33) * 0.4)
                base_b = int(68 + prog * 5 + (x - 33) * 0.3)
                
                # Symmetrical ballistic reinforcement ribs at y=63 and y=71
                if y in [63, 71]:
                    col = (55, 52, 40, 255) # Recessed groove shadow
                elif y in [64, 72]:
                    col = (130, 126, 98, 255) # Raised bevel highlight
                else:
                    col = (base_r, base_g, base_b, 255)
                im.putpixel((x, y), col)
                
    im.save(root_p)
    im.save(layer_p)
    print(f'Cleaned shield for {fid}')

# Update preview
Image.open(os.path.join(fdir, f'{frame_ids[0]}.png')).save(os.path.join(fdir, 'spr_ms_centurion_idle.png'))
# Update strip4
strip = Image.new('RGBA', (640, 160), (0, 0, 0, 0))
for i, fid in enumerate(frame_ids):
    strip.paste(Image.open(os.path.join(fdir, f'{fid}.png')), (i * 160, 0))
strip.save(os.path.join(fdir, 'spr_ms_centurion_idle_strip4.png'))
print('Updated spr_ms_centurion_idle strip4 and preview!')
