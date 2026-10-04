import os, re
from bs4 import BeautifulSoup

pages_to_update = [
    'products.html', 'our-science.html', 'reports.html', 'about.html',
    'contact.html', 'faq.html', 'login.html', 'shipping-policy.html',
    'privacy-policy.html', 'refund-policy.html', 'terms.html'
]

# 1. Update HTML files for canonical and <main> tags
for p in pages_to_update:
    filepath = os.path.join(".", p)
    html = open(filepath, 'r', encoding='utf-8').read()
    soup = BeautifulSoup(html, 'html.parser')

    changed = False

    # Check canonical
    canonical = soup.find('link', attrs={'rel': 'canonical'})
    if not canonical:
        new_link = soup.new_tag('link', rel='canonical', href=f'https://milla-pro-store.netlify.app/{p}')
        if soup.head:
            soup.head.append(new_link)
            changed = True
    elif 'milla-pro-store' not in canonical.get('href', ''):
        canonical['href'] = f'https://milla-pro-store.netlify.app/{p}'
        changed = True

    # Check meta description
    mdesc = soup.find('meta', attrs={'name': 'description'})
    if not mdesc or len(mdesc.get('content', '').strip()) < 15:
        if mdesc:
            mdesc['content'] = f"MILLA PRO™ 100% clean high-protein atta. 15g protein per roti, low GI 42, zero whey bloat. Explore {p.replace('.html','').replace('-',' ')}."
            sub_title = p.replace('.html','').replace('-',' ')
            new_desc = soup.new_tag('meta', attrs={'name': 'description', 'content': f'MILLA PRO 100% clean high-protein atta. 15g protein per roti, low GI 42, zero whey bloat. Explore {sub_title}.'})
            if soup.head:
                soup.head.append(new_desc)
        changed = True

    # Check semantic <main> tag
    has_main = soup.find('main') is not None
    if not has_main:
        # Wrap content between header/sidebar/cart and footer into <main>
        # In our templates, header/cart/sidebar are at top, footer is at bottom
        header = soup.find('header')
        footer = soup.find('footer')
        cart = soup.find(id='cartDrawer')
        sidebar = soup.find(id='mobileSidebar')
        
        # We can find all elements that come after header/cart and before footer
        # In a simpler way with regex on html string:
        # Find position after </aside> (sidebar/cart) or </header> and before <footer
        pattern = r'(</aside>\s*)(<section|<div class="container"|<div class="auth-|<div class="shop-|<div class="page-)'
        if re.search(pattern, html):
            html = re.sub(pattern, r'\1<main>\n\2', html, count=1)
            # Add </main> before <footer
            html = re.sub(r'(\s*<footer)', r'\n</main>\1', html, count=1)
            open(filepath, 'w', encoding='utf-8').write(html)
            print(f"Wrapped <main> in {p} via regex")
            continue

    if changed:
        open(filepath, 'w', encoding='utf-8').write(str(soup))
        print(f"Updated metadata in {p}")

# 2. Append selectShopPack & addShopToCart into script.js if not present
js_code = open('script.js', 'r', encoding='utf-8').read()
if 'function selectShopPack' not in js_code:
    js_append = """

// ==========================================
// Global Shop Configurator & Cart Adapters
// ==========================================
var currentSelectedPack = '1kg';
var currentPrice = 249;

function selectShopPack(pack, price, mrp, discount) {
  currentSelectedPack = pack;
  currentPrice = price;

  var c1 = document.getElementById('packCard1kg');
  var c5 = document.getElementById('packCard5kg');
  if (c1) c1.classList.toggle('active', pack === '1kg');
  if (c5) c5.classList.toggle('active', pack === '5kg');

  var pText = document.getElementById('shopPriceText');
  var mText = document.getElementById('shopMrpText');
  var dText = document.getElementById('shopDiscountText');
  if (pText) pText.textContent = '₹' + price.toLocaleString('en-IN');
  if (mText) mText.textContent = '₹' + mrp.toLocaleString('en-IN');
  if (dText) dText.textContent = 'SAVE ' + discount;

  if (typeof selectPack === 'function') {
    selectPack(pack);
  }
}

function addShopToCart() {
  var qInput = document.getElementById('shopQtyInput');
  var qty = qInput ? (parseInt(qInput.value, 10) || 1) : 1;
  if (typeof addToCart === 'function') {
    addToCart(currentSelectedPack, qty);
    openCartDrawer();
  }
}

function stepQty(delta) {
  var input = document.getElementById('shopQtyInput');
  if (!input) return;
  var val = parseInt(input.value, 10) || 1;
  val = Math.max(1, Math.min(10, val + delta));
  input.value = val;
}
"""
    open('script.js', 'a', encoding='utf-8').write(js_append)
    print("Added selectShopPack & addShopToCart to script.js")

# 3. Add explicit @media (max-width: 480px) and box-sizing helper to style.css if missing
css_code = open('style.css', 'r', encoding='utf-8').read()
if '@media (max-width: 480px)' not in css_code:
    css_append = """

/* Compact Mobile Screens (<480px) Anti-Overflow & Spacing Rules */
@media (max-width: 480px) {
  html, body {
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: hidden !important;
  }
  .container, .header-inner, .pg-container, .rr-container, .bc-container {
    padding-left: 12px !important;
    padding-right: 12px !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }
  .shop-action-row {
    grid-template-columns: 1fr !important;
    gap: 8px !important;
  }
  .qty-stepper {
    justify-content: center !important;
    width: 100% !important;
  }
  .mh-h1 {
    font-size: clamp(2.2rem, 9vw, 3.2rem) !important;
  }
}
"""
    open('style.css', 'a', encoding='utf-8').write(css_append)
    print("Added @media (max-width: 480px) to style.css")
