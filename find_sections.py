import re

with open('milld_home.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find shopify-section divs
sections = re.findall(r'<div id="(shopify-section-[^"]+)" class="([^"]+)"', text)
for s_id, s_cls in sections:
    print(f"ID: {s_id} | Class: {s_cls}")
