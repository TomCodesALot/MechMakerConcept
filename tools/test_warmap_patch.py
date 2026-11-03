with open('objects/obj_HQTerminal/Draw_64.gml', 'r') as f:
    text = f.read()

# Let's find Pass 1 in Draw_64
idx_pass1 = text.find('// Pass 1: Hyperlane Grid Lines')
idx_pass2 = text.find('// Pass 2: Interactive Territory Nodes')
idx_dossier = text.find('// --- SECTOR DIRECT ACTIONS ---')

print(f"Pass 1 at {idx_pass1}, Pass 2 at {idx_pass2}, Dossier Actions at {idx_dossier}")
