pages = [
    'about.html', 'contact.html', 'faq.html', 'login.html',
    'shipping-policy.html', 'privacy-policy.html', 'refund-policy.html', 'terms.html'
]
for p in pages:
    html = open(p, encoding='utf-8').read()
    if 'rel="canonical"' not in html:
        canonical_tag = f'  <link rel="canonical" href="https://milla-pro-store.netlify.app/{p}">\n'
        html = html.replace('</head>', canonical_tag + '</head>', 1)
        open(p, 'w', encoding='utf-8').write(html)
        print(f"Added canonical to {p}")
