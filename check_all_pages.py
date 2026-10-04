import glob, re

css = open('style.css', encoding='utf-8').read()

excluded = ['elementor-bundle.html', 'every_roti_section.html', 'milld_home.html', 'milld_product.html', 'milld_science_extracted.html']

for f in sorted(glob.glob('*.html')):
    if f in excluded:
        continue
    html = open(f, encoding='utf-8').read()
    classes = set()
    for m in re.finditer(r'class=["\']([^"\']+)["\']', html):
        for c in m.group(1).split():
            if c.strip():
                classes.add(c.strip())
    missing = [c for c in classes if ('.' + c) not in css]
    print(f"{f:22} Total: {len(classes):3} Missing: {len(missing):2}")
    if missing:
        print(f"   Missing from {f}: {sorted(missing)[:12]}")
