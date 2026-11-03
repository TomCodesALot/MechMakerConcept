import glob
import re

files = glob.glob('**/*.yy', recursive=True)
count = 0
for f in files:
    if f.endswith('MechMakerConcept.yyp'):
        continue
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    if '"folders/' in content:
        # replace parent block with standard parent
        # pattern matching "parent": { ... }
        new_content = re.sub(
            r'"parent"\s*:\s*\{[^\}]*"folders/[^\}]*\}',
            '"parent": {\n    "name": "MechMakerConcept",\n    "path": "MechMakerConcept.yyp"\n  }',
            content
        )
        if new_content != content:
            count += 1
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(new_content)
            print(f"Fixed parent in: {f}")

print(f"Fixed parent in {count} files.")
