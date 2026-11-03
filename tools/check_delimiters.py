import glob
import re

for f in sorted(glob.glob('**/*.gml', recursive=True)):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        s = fh.read()
    # strip comments
    s = re.sub(r'//.*', '', s)
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.DOTALL)
    # strip strings
    s = re.sub(r'@"[^"]*"', '', s)
    s = re.sub(r'"(?:[^"\\]|\\.)*"', '', s)
    
    p = s.count('(') - s.count(')')
    b = s.count('[') - s.count(']')
    c = s.count('{') - s.count('}')
    if p != 0 or b != 0 or c != 0:
        print(f'{f}: paren={p}, bracket={b}, brace={c}')
