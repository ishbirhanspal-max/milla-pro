import re

with open('milld_home.html', 'r', encoding='utf-8') as f:
    text = f.read()

sections = [
    'announcement_bar',
    'protein_gap',
    'roti_break_down',
    'benefits_scroll',
    'science_section',
    'testimonials',
    'faq',
    'footer'
]

for s in sections:
    pos = text.find(s)
    if pos != -1:
        start = text.rfind('<div id="shopify-section', 0, pos)
        end = text.find('</div>\n</div>\n</div>', pos)
        if start != -1 and end != -1:
            snippet = text[start:end+20]
            print(f"=== SECTION: {s} (length: {len(snippet)}) ===")
            print(snippet[:400].encode('ascii', 'replace').decode('ascii'))
            print("...\n")
