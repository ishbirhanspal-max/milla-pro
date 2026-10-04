import re

with open('milld_home.html', 'r', encoding='utf-8') as f:
    text = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', text, re.DOTALL)
print(f"Total script tags in milld_home.html: {len(scripts)}")
for i, s in enumerate(scripts):
    for sec in ['roti-slider', 'rr-bars', 'bc-card', 'faq', 'calc']:
        if sec in s:
            print(f"Script {i+1} matches {sec} (length {len(s)})")
            for line in s.split('\n')[:15]:
                if line.strip():
                    print('  ', line.strip())
