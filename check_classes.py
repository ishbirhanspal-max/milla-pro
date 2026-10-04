import re

html = open('index.html', encoding='utf-8').read()
css = open('style.css', encoding='utf-8').read()

classes_in_html = set()
for match in re.finditer(r'class=["\']([^"\']+)["\']', html):
    for c in match.group(1).split():
        if c.strip():
            classes_in_html.add(c.strip())

missing = [c for c in sorted(classes_in_html) if ('.' + c) not in css]
print(f"Total unique classes in HTML: {len(classes_in_html)}")
print(f"Classes missing from style.css: {len(missing)}")
print("Missing classes:")
for c in missing:
    print(f"  - {c}")
