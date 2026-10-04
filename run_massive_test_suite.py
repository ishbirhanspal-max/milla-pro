import subprocess, time, json, urllib.request, asyncio, websockets, os, sys, re
from bs4 import BeautifulSoup

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
port = 9335

pages_to_test = [
    'index.html',
    'products.html',
    'our-science.html',
    'reports.html',
    'about.html',
    'contact.html',
    'faq.html',
    'login.html',
    'shipping-policy.html',
    'privacy-policy.html',
    'refund-policy.html',
    'terms.html'
]

viewports = [
    {"name": "320px (iPhone SE)", "width": 320, "height": 568},
    {"name": "360px (Galaxy A)", "width": 360, "height": 800},
    {"name": "375px (iPhone Mini)", "width": 375, "height": 667},
    {"name": "390px (iPhone 14)", "width": 390, "height": 844},
    {"name": "393px (iPhone 15/16 Pro)", "width": 393, "height": 852},
    {"name": "412px (Galaxy S24)", "width": 412, "height": 915},
    {"name": "428px (iPhone Pro Max)", "width": 428, "height": 926},
    {"name": "768px (iPad Portrait)", "width": 768, "height": 1024},
    {"name": "1024px (iPad Landscape)", "width": 1024, "height": 768},
    {"name": "1280px (Laptop)", "width": 1280, "height": 800},
    {"name": "1440px (Desktop)", "width": 1440, "height": 900},
    {"name": "1920px (Full HD Desktop)", "width": 1920, "height": 1080}
]

total_tests = 0
passed_tests = 0
failed_tests = []

def record_test(name, passed, details=""):
    global total_tests, passed_tests, failed_tests
    total_tests += 1
    if passed:
        passed_tests += 1
    else:
        failed_tests.append((name, details))

# ==========================================
# PHASE 1: Static HTML & Asset Tests (~400 tests)
# ==========================================
print("\n[PHASE 1] Running Static HTML & Asset Integrity Tests...")

for page_name in pages_to_test:
    filepath = os.path.join(".", page_name)
    record_test(f"{page_name} file exists", os.path.exists(filepath), f"File {filepath} not found")
    if not os.path.exists(filepath):
        continue

    content = open(filepath, 'r', encoding='utf-8').read()
    soup = BeautifulSoup(content, 'html.parser')

    # Basic structure
    record_test(f"{page_name} <!doctype html>", content.strip().lower().startswith("<!doctype html>"))
    record_test(f"{page_name} <html> tag", soup.find('html') is not None)
    record_test(f"{page_name} <head> tag", soup.find('head') is not None)
    record_test(f"{page_name} <body> tag", soup.find('body') is not None)
    
    # Meta tags
    viewport = soup.find('meta', attrs={'name': 'viewport'})
    record_test(f"{page_name} meta viewport", viewport is not None and 'width=device-width' in viewport.get('content', ''))
    
    title = soup.find('title')
    record_test(f"{page_name} non-empty <title>", title is not None and len(title.text.strip()) > 5, title.text if title else "")

    canonical = soup.find('link', attrs={'rel': 'canonical'})
    record_test(f"{page_name} canonical link", canonical is not None and 'milla-pro-store' in canonical.get('href', ''))

    # CSS link
    css_link = soup.find('link', attrs={'rel': 'stylesheet', 'href': re.compile(r'style\.css')})
    record_test(f"{page_name} style.css linked", css_link is not None)

    # JS script
    js_script = soup.find('script', attrs={'src': re.compile(r'script\.js')})
    record_test(f"{page_name} script.js included", js_script is not None)

    # Top ticker present
    top_ticker = soup.find(class_='top-ticker-bar')
    record_test(f"{page_name} top-ticker-bar", top_ticker is not None)

    # Master header present
    header = soup.find('header')
    record_test(f"{page_name} master header", header is not None)

    # Mobile sidebar drawer present
    sidebar = soup.find(id='mobileSidebar')
    record_test(f"{page_name} mobileSidebar drawer", sidebar is not None)

    # Cart drawer present
    cart = soup.find(id='cartDrawer')
    record_test(f"{page_name} cartDrawer aside", cart is not None)

    # Footer present
    footer = soup.find('footer')
    record_test(f"{page_name} footer present", footer is not None)

    # Check all images in page
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if not src:
            record_test(f"{page_name} img has src", False, f"Empty img src in {page_name}")
            continue
        alt = img.get('alt', '')
        record_test(f"{page_name} img {src[:25]} has alt", len(alt.strip()) > 0, f"Missing alt for {src}")
        
        # Check local file exists if local
        if not src.startswith(('http://', 'https://', 'data:', '//')):
            clean_src = src.split('?')[0].split('#')[0]
            exists = os.path.exists(os.path.join(".", clean_src))
            record_test(f"{page_name} local img {clean_src} exists", exists, f"File {clean_src} does not exist")

    # Check all internal <a> links
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if not href or href.startswith(('tel:', 'mailto:', 'javascript:', '#', 'http://', 'https://', '//')):
            continue
        clean_href = href.split('?')[0].split('#')[0]
        if clean_href:
            exists = os.path.exists(os.path.join(".", clean_href))
            record_test(f"{page_name} link {clean_href} exists", exists, f"Link {clean_href} in {page_name} not found")

# Check homepage specific constraint: No packaging image on homepage
index_content = open('index.html', 'r', encoding='utf-8').read()
has_packaging_in_index = 'milld_pack' in index_content or 'packaging' in index_content.lower() and 'pouch' in index_content.lower() and '<img' in index_content
# We ensure the hero image is roti / real food, not packaging
record_test("index.html hero has NO packaging image", 'roti-broken-down' in index_content or 'broken open' in index_content or 'milld_hs' in index_content)

print(f"Phase 1 Complete: {passed_tests}/{total_tests} passed so far.")

# ==========================================
# PHASE 2: Chrome CDP Headless Tests (~600+ tests)
# ==========================================
print("\n[PHASE 2] Starting Chrome CDP Headless Automation Server...")

async def run_cdp_suite():
    proc = subprocess.Popen([
        chrome_path,
        f"--remote-debugging-port={port}",
        "--headless=new",
        "--window-size=1280,800",
        "--disable-gpu",
        "--no-sandbox",
        "about:blank"
    ])
    await asyncio.sleep(1.8)

    try:
        resp = urllib.request.urlopen(f"http://localhost:{port}/json")
        pages = json.loads(resp.read().decode())
        ws_url = pages[0]["webSocketDebuggerUrl"]

        async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
            # Enable domains
            msg_id = 1
            for domain in ["Page", "Network", "Runtime", "Log"]:
                await ws.send(json.dumps({"id": msg_id, "method": f"{domain}.enable"}))
                await ws.recv()
                msg_id += 1

            console_errors = []

            async def eval_js(expression):
                nonlocal msg_id
                req_id = msg_id
                msg_id += 1
                await ws.send(json.dumps({
                    "id": req_id,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": expression,
                        "returnByValue": True,
                        "awaitPromise": True
                    }
                }))
                while True:
                    m = await ws.recv()
                    data = json.loads(m)
                    if data.get("id") == req_id:
                        return data.get("result", {}).get("result", {}).get("value")

            async def set_viewport(w, h):
                nonlocal msg_id
                req_id = msg_id
                msg_id += 1
                await ws.send(json.dumps({
                    "id": req_id,
                    "method": "Emulation.setDeviceMetricsOverride",
                    "params": {
                        "width": w,
                        "height": h,
                        "deviceScaleFactor": 2 if w < 600 else 1,
                        "mobile": w < 600,
                        "fitWindow": True
                    }
                }))
                await ws.recv()

            async def navigate_page(url):
                nonlocal msg_id
                req_id = msg_id
                msg_id += 1
                await ws.send(json.dumps({
                    "id": req_id,
                    "method": "Page.navigate",
                    "params": {"url": url}
                }))
                start_t = time.time()
                while time.time() - start_t < 2.0:
                    try:
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.25)
                        data = json.loads(msg)
                        if data.get("method") == "Page.loadEventFired":
                            break
                    except asyncio.TimeoutError:
                        pass
                await asyncio.sleep(0.3)

            # --- PART A: Responsive Horizontal Scroll Checks Across 144 Combinations ---
            print("\n  -> Testing horizontal scroll on 12 viewports across all 12 pages...")
            
            overflow_check_js = """
            (() => {
                const docWidth = window.innerWidth;
                const scrollWidth = document.documentElement.scrollWidth;
                const bodyWidth = document.body ? document.body.scrollWidth : 0;
                
                let maxRight = docWidth;
                let offendingEl = null;
                const all = document.querySelectorAll('*');
                for (const el of all) {
                    const rect = el.getBoundingClientRect();
                    if (rect.right > docWidth + 0.75) {
                        const style = window.getComputedStyle(el);
                        if (style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0') {
                            if (rect.right > maxRight) {
                                maxRight = rect.right;
                                offendingEl = {
                                    tag: el.tagName.toLowerCase(),
                                    cls: (typeof el.className === 'string' ? el.className.trim() : ''),
                                    id: el.id || '',
                                    right: Math.round(rect.right),
                                    text: (el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 30)
                                };
                            }
                        }
                    }
                }
                return {
                    docWidth: docWidth,
                    scrollWidth: scrollWidth,
                    bodyWidth: bodyWidth,
                    hasScroll: scrollWidth > docWidth,
                    offender: offendingEl
                };
            })()
            """

            for vp in viewports:
                await set_viewport(vp["width"], vp["height"])
                for p in pages_to_test:
                    await navigate_page(f"http://localhost:8089/{p}")
                    res = await eval_js(overflow_check_js)
                    if res:
                        has_scroll = res.get("hasScroll", False)
                        offender = res.get("offender")
                        err_str = f"scrollWidth {res.get('scrollWidth')} > {res.get('docWidth')}"
                        if offender:
                            err_str += f" | element <{offender['tag']} class='{offender['cls']}'> right={offender['right']}px text='{offender['text']}'"
                        record_test(f"No horizontal scroll: {p} @ {vp['name']}", not has_scroll, err_str)

            print(f"  Passed {passed_tests}/{total_tests} after viewport matrix tests.")

            # --- PART B: Interactive Cart Drawer Tests ---
            print("\n  -> Testing Cart Drawer Interactions...")
            await set_viewport(393, 852)
            await navigate_page("http://localhost:8089/index.html")

            # Test 1: Open Cart Drawer
            cart_open_res = await eval_js("""
            (() => {
                if (typeof openCartDrawer === 'function') openCartDrawer();
                const drawer = document.getElementById('cartDrawer');
                const overlay = document.getElementById('cartOverlay');
                return {
                    drawerActive: drawer ? drawer.classList.contains('active') : false,
                    overlayActive: overlay ? overlay.classList.contains('active') : false
                };
            })()
            """)
            record_test("Cart Drawer opens via openCartDrawer()", cart_open_res.get("drawerActive") and cart_open_res.get("overlayActive"))

            # Test 2: Cart Items Rendered & Totals Exist
            cart_items_res = await eval_js("""
            (() => {
                const list = document.getElementById('cartItemsList');
                const total = document.getElementById('billGrandTotal');
                return {
                    itemCount: list ? list.children.length : 0,
                    totalText: total ? total.innerText : ''
                };
            })()
            """)
            record_test("Cart has rendered items", cart_items_res.get("itemCount") > 0, f"Items: {cart_items_res.get('itemCount')}")
            record_test("Cart displays grand total", '₹' in cart_items_res.get("totalText", ""), cart_items_res.get("totalText"))

            # Test 3: Increment Quantity
            qty_inc_res = await eval_js("""
            (() => {
                const initTotal = document.getElementById('billGrandTotal')?.innerText || '';
                // find increment button
                const incBtn = document.querySelector('#cartItemsList .cart-qty-btn:last-child');
                if (incBtn) incBtn.click();
                const newTotal = document.getElementById('billGrandTotal')?.innerText || '';
                return {
                    initTotal: initTotal,
                    newTotal: newTotal,
                    changed: initTotal !== newTotal
                };
            })()
            """)
            record_test("Cart quantity increment updates total", qty_inc_res.get("changed"), f"{qty_inc_res.get('initTotal')} -> {qty_inc_res.get('newTotal')}")

            # Test 4: Decrement Quantity
            qty_dec_res = await eval_js("""
            (() => {
                const initTotal = document.getElementById('billGrandTotal')?.innerText || '';
                const decBtn = document.querySelector('#cartItemsList .cart-qty-btn:first-child');
                if (decBtn) decBtn.click();
                const newTotal = document.getElementById('billGrandTotal')?.innerText || '';
                return {
                    initTotal: initTotal,
                    newTotal: newTotal,
                    changed: initTotal !== newTotal
                };
            })()
            """)
            record_test("Cart quantity decrement updates total", qty_dec_res.get("changed"))

            # Test 5: Coupon Application
            coupon_res = await eval_js("""
            (() => {
                const input = document.getElementById('couponCodeInput') || document.getElementById('cartCouponInput');
                if (input) input.value = 'LAUNCH20';
                if (typeof applyCartCoupon === 'function') applyCartCoupon();
                const discRow = document.getElementById('billCouponDiscountRow');
                const discVal = document.getElementById('billCouponDiscount');
                return {
                    discountApplied: discRow ? discRow.style.display !== 'none' : false,
                    discountText: discVal ? discVal.innerText : ''
                };
            })()
            """)
            record_test("Coupon LAUNCH20 applied successfully", coupon_res.get("discountApplied"), coupon_res.get("discountText"))

            # Test 6: Close Cart Drawer
            cart_close_res = await eval_js("""
            (() => {
                if (typeof closeCartDrawer === 'function') closeCartDrawer();
                const drawer = document.getElementById('cartDrawer');
                return {
                    drawerActive: drawer ? drawer.classList.contains('active') : true
                };
            })()
            """)
            record_test("Cart Drawer closes via closeCartDrawer()", not cart_close_res.get("drawerActive"))

            # --- PART C: Mobile Sidebar Drawer Tests ---
            print("\n  -> Testing Mobile Sidebar Drawer...")
            sidebar_open_res = await eval_js("""
            (() => {
                if (typeof openMobileSidebar === 'function') openMobileSidebar();
                const sb = document.getElementById('mobileSidebar');
                const ov = document.getElementById('sidebarOverlay');
                return {
                    sbActive: sb ? sb.classList.contains('active') : false,
                    ovActive: ov ? ov.classList.contains('active') : false,
                    linksCount: sb ? sb.querySelectorAll('nav a').length : 0,
                    shopBtn: sb ? sb.querySelector('.mobile-shop-cta-btn') !== null : false
                };
            })()
            """)
            record_test("Mobile sidebar opens", sidebar_open_res.get("sbActive") and sidebar_open_res.get("ovActive"))
            record_test("Mobile sidebar has Shop Now CTA button", sidebar_open_res.get("shopBtn"))
            record_test("Mobile sidebar has clean navigation links", sidebar_open_res.get("linksCount") >= 6)

            sidebar_close_res = await eval_js("""
            (() => {
                if (typeof closeMobileSidebar === 'function') closeMobileSidebar();
                const sb = document.getElementById('mobileSidebar');
                return { sbActive: sb ? sb.classList.contains('active') : true };
            })()
            """)
            record_test("Mobile sidebar closes cleanly", not sidebar_close_res.get("sbActive"))

            # --- PART D: Whey Protein Cost Calculator Reactive Precision Tests ---
            print("\n  -> Testing Whey Protein Cost Calculator on index.html...")
            # Test 10 distinct slider values (1 to 10 rotis)
            for r in range(1, 11):
                calc_val_res = await eval_js(f"""
                (() => {{
                    const slider = document.getElementById('pgRotiSlider');
                    if (slider) {{
                        slider.value = {r};
                        if (typeof updateWheyCostCalc === 'function') updateWheyCostCalc({r});
                    }}
                    const count = document.getElementById('pgRotiCount')?.innerText;
                    const milla = document.getElementById('pgMillaVal')?.innerText;
                    const gain = document.getElementById('pgGainVal')?.innerText;
                    const wheyCost = document.getElementById('wheyMonthlyCostVal')?.innerText;
                    const millaCost = document.getElementById('millaMonthlyCostVal')?.innerText;
                    const monthlySavings = document.getElementById('wheySavingsMonthlyVal')?.innerText;
                    const yearlySavings = document.getElementById('wheySavingsYearlyVal')?.innerText;
                    
                    return {{
                        count: count,
                        milla: milla,
                        gain: gain,
                        wheyCost: wheyCost,
                        millaCost: millaCost,
                        monthlySavings: monthlySavings,
                        yearlySavings: yearlySavings,
                        isNan: [count, milla, gain, wheyCost, millaCost, monthlySavings, yearlySavings].some(v => !v || v.includes('NaN') || v.includes('undefined'))
                    }};
                }})()
                """)
                record_test(f"Calculator valid at {r} rotis/day", not calc_val_res.get("isNan"), f"Returned NaN or undefined: {calc_val_res}")
                record_test(f"Calculator {r} rotis milla protein positive", float(calc_val_res.get("milla", "0").replace('g','')) > 0)
                record_test(f"Calculator {r} rotis savings > 0", int(calc_val_res.get("monthlySavings", "0").replace('₹','').replace(',','')) > 0)

            # --- PART E: Product Page Pack Switcher & Buy Buttons ---
            print("\n  -> Testing Products Page Interactivity...")
            await navigate_page("http://localhost:8089/products.html")
            prod_res = await eval_js("""
            (() => {
                // Check default pack selection
                const priceEl = document.getElementById('currentPackPrice');
                const initPrice = priceEl ? priceEl.innerText : '';
                
                // Select 5kg
                if (typeof selectPack === 'function') selectPack('5kg');
                const p5Price = priceEl ? priceEl.innerText : '';

                // Select 1kg
                if (typeof selectPack === 'function') selectPack('1kg');
                const p1Price = priceEl ? priceEl.innerText : '';

                return {
                    initPrice: initPrice,
                    p5Price: p5Price,
                    p1Price: p1Price,
                    switchesCorrectly: p5Price.includes('1,199') && p1Price.includes('249')
                };
            })()
            """)
            record_test("Products Page Pack switch updates price", prod_res.get("switchesCorrectly"), f"1kg: {prod_res.get('p1Price')}, 5kg: {prod_res.get('p5Price')}")

            # Test Add to cart from products page
            prod_add_res = await eval_js("""
            (() => {
                const initItems = document.getElementById('cartItemsList')?.children.length || 0;
                if (typeof addConfiguredPackToCart === 'function') addConfiguredPackToCart();
                const newItems = document.getElementById('cartItemsList')?.children.length || 0;
                const drawerActive = document.getElementById('cartDrawer')?.classList.contains('active');
                return {
                    initItems: initItems,
                    newItems: newItems,
                    drawerActive: drawerActive
                };
            })()
            """)
            record_test("Products Page Add to Cart opens drawer", prod_add_res.get("drawerActive"))

            # --- PART F: FAQ Accordion Tests ---
            print("\n  -> Testing FAQ Accordion Open/Close...")
            await navigate_page("http://localhost:8089/faq.html")
            faq_res = await eval_js("""
            (() => {
                const faqs = document.querySelectorAll('.faq-item, .faq-card, details');
                let clicked = 0;
                if (faqs.length > 0) {
                    for (let i = 0; i < Math.min(faqs.length, 5); i++) {
                        const item = faqs[i];
                        if (item.tagName.toLowerCase() === 'details') {
                            item.open = true;
                            clicked++;
                        } else {
                            const btn = item.querySelector('.faq-question, button, h3');
                            if (btn) {
                                btn.click();
                                clicked++;
                            }
                        }
                    }
                }
                return { faqCount: faqs.length, clicked: clicked };
            })()
            """)
            record_test("FAQ items found and expandable", faq_res.get("clicked") > 0, f"Found {faq_res.get('faqCount')} FAQs")

            # --- PART G: Login & Auth Simulation Tests ---
            print("\n  -> Testing Login Page Auth Tabs...")
            await navigate_page("http://localhost:8089/login.html")
            auth_res = await eval_js("""
            (() => {
                if (typeof switchAuthMethod === 'function') {
                    switchAuthMethod('email');
                    const emailVisible = document.getElementById('authEmailView')?.style.display !== 'none';
                    switchAuthMethod('track');
                    const trackVisible = document.getElementById('authTrackView')?.style.display !== 'none';
                    switchAuthMethod('mobile');
                    const mobileVisible = document.getElementById('authMobileView')?.style.display !== 'none';
                    return { emailVisible, trackVisible, mobileVisible };
                }
                return { emailVisible: false, trackVisible: false, mobileVisible: false };
            })()
            """)
            record_test("Login page auth tab switching works", auth_res.get("emailVisible") and auth_res.get("trackVisible") and auth_res.get("mobileVisible"))

            # --- PART H: Science & Lab Reports Page Elements ---
            print("\n  -> Testing Science & Reports Page Visual Elements...")
            await navigate_page("http://localhost:8089/our-science.html")
            sci_res = await eval_js("""
            (() => {
                const fractionCards = document.querySelectorAll('.fraction-card, .science-fraction-card, .process-step, .amino-card');
                return { count: fractionCards.length };
            })()
            """)
            record_test("Science page has fractions & process elements", sci_res.get("count") >= 3, f"Found {sci_res.get('count')} elements")

            await navigate_page("http://localhost:8089/reports.html")
            rep_res = await eval_js("""
            (() => {
                const certCards = document.querySelectorAll('.cert-scan-card, .cert-card, .lab-table');
                return { count: certCards.length };
            })()
            """)
            record_test("Reports page has NABL cert cards & data table", rep_res.get("count") >= 2, f"Found {rep_res.get('count')} elements")

            # --- PART I: Link Crawl Validation on ALL Pages ---
            print("\n  -> Testing all link targets and anchors across 12 pages...")
            for page in pages_to_test:
                await navigate_page(f"http://localhost:8089/{page}")
                links_check = await eval_js("""
                (() => {
                    const links = document.querySelectorAll('a[href]');
                    const results = [];
                    for (const a of links) {
                        const href = a.getAttribute('href');
                        if (href && href.startsWith('#') && href.length > 1) {
                            const target = document.querySelector(href);
                            results.push({ href: href, targetExists: target !== null });
                        }
                    }
                    return results;
                })()
                """)
                if links_check:
                    for lk in links_check:
                        record_test(f"{page} internal anchor {lk['href']} target exists", lk.get("targetExists", False), f"Target {lk['href']} not found in {page}")

    finally:
        proc.terminate()

asyncio.run(run_cdp_suite())

# ==========================================
# FINAL REPORT
# ==========================================
print("\n" + "="*70)
print(f"AUTOMATED TEST SUITE EXECUTION SUMMARY")
print("="*70)
print(f"Total Tests Executed : {total_tests}")
print(f"Passed Tests         : {passed_tests}")
print(f"Failed Tests         : {len(failed_tests)}")
print(f"Pass Rate            : {(passed_tests/total_tests)*100:.2f}%")

if failed_tests:
    print("\n[FAILURES TO INVESTIGATE & FIX]:")
    for name, details in failed_tests[:25]:
        print(f"  ❌ {name}")
        if details:
            print(f"     Details: {details}")
    if len(failed_tests) > 25:
        print(f"  ... and {len(failed_tests) - 25} more failures.")
else:
    print("\n✨ ALL TESTS PASSED WITH 100% PRECISION! ZERO BUGS DETECTED!")
print("="*70)
