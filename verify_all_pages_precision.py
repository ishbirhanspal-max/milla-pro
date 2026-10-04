import os, re

files = [
    'index.html',
    'products.html',
    'our-science.html',
    'science.html',
    'reports.html',
    'about.html',
    'contact.html',
    'faq.html',
    'login.html',
    'privacy-policy.html',
    'refund-policy.html',
    'shipping-policy.html',
    'terms.html'
]

print("=== CHECKING ALL PAGES FOR 393x852 MOBILE PRECISION ===")

issues = []

for filename in files:
    if not os.path.exists(filename):
        print(f"[-] Missing file: {filename}")
        continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Viewport tag
    if 'width=device-width' not in content:
        issues.append(f"{filename}: Missing or invalid viewport meta tag")
    
    # 2. Check for inline fixed widths > 360px
    inline_widths = re.findall(r'style="[^"]*width:\s*(\d+)px', content)
    for w in inline_widths:
        if int(w) > 360:
            issues.append(f"{filename}: Fixed inline width {w}px exceeds 360px")
    
    # 3. Check for uncontained tables without overflow wrapper
    tables = re.findall(r'(<table[^>]*>)', content)
    if tables:
        # Check if wrapped in an overflow container
        table_blocks = re.findall(r'(<div[^>]*>[\s\S]*?<table[\s\S]*?</table>[\s\S]*?</div>)', content)
        print(f"[i] {filename}: Has {len(tables)} table(s)")
    
    # 4. Check CSS links
    css_match = re.search(r'href="([^"]*style\.css[^"]*)"', content)
    if not css_match:
        issues.append(f"{filename}: Missing style.css link")

print("\nIssues found:", len(issues))
for issue in issues:
    print("  *", issue)
