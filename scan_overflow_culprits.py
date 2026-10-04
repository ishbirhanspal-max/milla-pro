import re

with open('style.css', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. 100vw
vw_matches = [(m.start(), text[max(0, m.start()-50):min(len(text), m.start()+50)]) for m in re.finditer(r'100vw', text)]
print(f'100vw occurrences: {len(vw_matches)}')
for pos, snippet in vw_matches:
    line_num = text[:pos].count('\n') + 1
    clean = ' '.join(snippet.split())
    print(f'  Line {line_num}: {clean}')

# 2. negative margins
neg_matches = [(m.start(), text[max(0, m.start()-30):min(len(text), m.start()+50)]) for m in re.finditer(r'margin-(?:left|right)\s*:\s*-[0-9]', text)]
print(f'\nNegative margin-left/right: {len(neg_matches)}')
for pos, snippet in neg_matches:
    line_num = text[:pos].count('\n') + 1
    clean = ' '.join(snippet.split())
    print(f'  Line {line_num}: {clean}')

# 3. min-width > 360px
minw_matches = [(m.start(), text[max(0, m.start()-30):min(len(text), m.start()+50)]) for m in re.finditer(r'min-width\s*:\s*([0-9]+)px', text) if int(m.group(1)) > 360]
print(f'\nFixed min-width > 360px: {len(minw_matches)}')
for pos, snippet in minw_matches:
    line_num = text[:pos].count('\n') + 1
    clean = ' '.join(snippet.split())
    print(f'  Line {line_num}: {clean}')
