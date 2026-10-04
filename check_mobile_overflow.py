import glob, re, os

pages = ['index.html', 'products.html', 'our-science.html', 'reports.html', 'about.html', 'contact.html', 'faq.html', 'login.html', 'privacy-policy.html', 'refund-policy.html', 'shipping-policy.html', 'terms.html']

for page in pages:
    if not os.path.exists(page):
        continue
    with open(page, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check viewport tag
    vp = re.search(r'<meta[^>]*viewport[^>]*>', content)
    vp_str = vp.group(0) if vp else "MISSING"
    
    # Check CSS stylesheets linked
    css = re.findall(r'<link[^>]*rel=[\'"]stylesheet[\'"][^>]*>', content)
    
    # Check for inline min-width or fixed width > 350
    fixed_widths = re.findall(r'(?:width|min-width)\s*:\s*(\d+)px', content)
    big_fixed = [int(w) for w in fixed_widths if int(w) > 350]
    
    # Check for tables
    has_table = '<table' in content
    
    print(f"=== {page} ===")
    print(f"  Viewport: {vp_str}")
    print(f"  CSS: {len(css)} links")
    for c in css:
        print(f"    {c}")
    if big_fixed:
        print(f"  Fixed widths > 350px: {big_fixed}")
    if has_table:
        print(f"  Has HTML Table")
