import re

with open('milld_home.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('India loves roti')
if pos != -1:
    start = max(0, pos - 300)
    end = min(len(text), pos + 1500)
    print("=== HERO SECTION SNIPPET ===")
    print(text[start:end])
else:
    print("Text not found")
