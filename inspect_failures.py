import os, re
from bs4 import BeautifulSoup

pages_to_test = [
    'index.html', 'products.html', 'our-science.html', 'reports.html',
    'about.html', 'contact.html', 'faq.html', 'login.html',
    'shipping-policy.html', 'privacy-policy.html', 'refund-policy.html', 'terms.html'
]

# Check HTML structure
print("HTML Structure check:")
for p in pages_to_test:
    soup = BeautifulSoup(open(p, encoding='utf-8').read(), 'html.parser')
    desc = soup.find('meta', attrs={'name': 'description'})
    if not desc or len(desc.get('content', '').strip()) <= 20:
        print(f"  Missing or short meta desc in {p}: {desc}")
    charset = soup.find('meta', attrs={'charset': True})
    if not charset:
        print(f"  Missing meta charset in {p}")

print("\nComponents check:")
for p in pages_to_test:
    soup = BeautifulSoup(open(p, encoding='utf-8').read(), 'html.parser')
    sb = soup.find(id='mobileSidebar')
    if sb:
        shop_cta = sb.find(class_='mobile-shop-cta-btn')
        if not shop_cta:
            print(f"  Missing mobile-shop-cta-btn in {p}")
    cart_btn = soup.find('button', attrs={'onclick': re.compile(r'openCartDrawer')})
    if not cart_btn:
        print(f"  Missing openCartDrawer button in {p}")

print("\nCSS tokens/rules check:")
css = open('style.css', encoding='utf-8').read()
for tok in ['--color-bg', '--color-text', '--color-accent', 'Anton', 'Caveat', 'Inter']:
    if tok not in css:
        print(f"  Missing CSS token: {tok}")

for sel in ['.top-ticker-bar', '.ticker-scroll-track', '.ticker-scroll-content', '.master-header', '.brand-logo', '.shop-pill-nav', '.icon-btn', '.cart-badge-count', '.mobile-menu-btn', '.mobile-sidebar', '.sidebar-overlay', '.mobile-shop-cta-btn', '.mobile-nav-links', '.cart-drawer', '.cart-overlay', '.cart-policy-strip', '.cart-items-container', '.cart-drawer-footer', '.cart-checkout-btn', '.milld-hs', '.mh-badge', '.mh-h1', '.mh-sub', '.mh-btn-shop', '.mh-stats', '.pg-section', '.pg-calc', '.pg-roti-slider', '.pg-whey-card', '.rr-section', '.bc-section', '.lab-showcase-section', '.tm-section', '.faq-section', '.site-footer', '.ft-col', '.ft-copyright', '.auth-container', '.auth-tab', '.prod-gallery', '.pack-selector-pill', '.science-step']:
    if sel not in css:
        print(f"  Missing selector in style.css: {sel}")

print("\nJS Architecture check:")
js = open('script.js', encoding='utf-8').read()
for fn in ['openCartDrawer', 'closeCartDrawer', 'openMobileSidebar', 'closeMobileSidebar', 'updateWheyCostCalc', 'applyCartCoupon', 'removeCartCoupon', 'selectPack', 'addConfiguredPackToCart', 'triggerRazorpayCheckout', 'switchAuthMethod']:
    if fn not in js:
        print(f"  Missing JS function in script.js: {fn}")
