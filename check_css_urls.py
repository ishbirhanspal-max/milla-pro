import re

with open('milld_components.css', 'r', encoding='utf-8') as f:
    css = f.read()

urls = re.findall(r'url\([^)]+\)', css)
print("Total urls in milld_components.css:", len(urls))
for u in urls:
    print(" ", u)
