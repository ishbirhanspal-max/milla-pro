import subprocess, time, json, urllib.request, asyncio, websockets, sys

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
port = 9338

pages = [
    'index.html', 'products.html', 'our-science.html', 'reports.html',
    'about.html', 'contact.html', 'faq.html', 'login.html',
    'shipping-policy.html', 'privacy-policy.html', 'refund-policy.html', 'terms.html'
]

viewports = [
    (320, 568, "320px (iPhone SE Small)"),
    (360, 800, "360px (Standard Android)"),
    (375, 667, "375px (iPhone Mini/Standard)"),
    (390, 844, "390px (iPhone 14)"),
    (393, 852, "393px (iPhone 15/16 Pro Mobile)"),
    (412, 915, "412px (Samsung Galaxy S24)"),
    (428, 926, "428px (iPhone Max)"),
    (768, 1024, "768px (iPad Portrait)"),
    (1024, 768, "1024px (iPad Landscape)"),
    (1280, 800, "1280px (Standard Laptop)"),
    (1440, 900, "1440px (MacBook Desktop)"),
    (1920, 1080, "1920px (Full HD 1080p Desktop)")
]

check_overflow_js = """
(() => {
    const docWidth = window.innerWidth;
    const scrollWidth = document.documentElement.scrollWidth;
    
    let maxOverflowEl = null;
    let maxRight = docWidth;
    
    const all = document.querySelectorAll('*');
    for (const el of all) {
        const rect = el.getBoundingClientRect();
        if (rect.right > docWidth + 0.75) {
            const style = window.getComputedStyle(el);
            if (style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0') {
                if (rect.right > maxRight) {
                    maxRight = rect.right;
                    maxOverflowEl = {
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
        hasScroll: scrollWidth > docWidth,
        offender: maxOverflowEl
    };
})()
"""

async def run_audit():
    proc = subprocess.Popen([
        chrome_path, f'--remote-debugging-port={port}',
        '--headless=new', '--disable-gpu', '--no-sandbox', 'about:blank'
    ])
    await asyncio.sleep(1.5)
    try:
        resp = urllib.request.urlopen(f'http://localhost:{port}/json')
        ws_url = json.loads(resp.read().decode())[0]['webSocketDebuggerUrl']
        async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Page.enable'}))
            await ws.recv()
            await ws.send(json.dumps({'id': 2, 'method': 'Network.enable'}))
            await ws.recv()

            print("=========================================================================", flush=True)
            print("CROSS-DEVICE RESPONSIVE HORIZONTAL OVERFLOW AUDIT (144 MATRIX TESTS)", flush=True)
            print("=========================================================================", flush=True)

            total_passes = 0
            failures = []

            for width, height, name in viewports:
                is_mobile = width < 768
                ua = (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
                    if is_mobile else
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                )

                # Set UA
                await ws.send(json.dumps({
                    'id': 10,
                    'method': 'Network.setUserAgentOverride',
                    'params': {'userAgent': ua}
                }))
                await ws.recv()

                # Set Device Metrics
                await ws.send(json.dumps({
                    'id': 11,
                    'method': 'Emulation.setDeviceMetricsOverride',
                    'params': {
                        'width': width,
                        'height': height,
                        'deviceScaleFactor': 3 if is_mobile else 1,
                        'mobile': is_mobile,
                        'fitWindow': True
                    }
                }))
                await ws.recv()

                for p_idx, p in enumerate(pages):
                    nav_id = 100 + p_idx
                    await ws.send(json.dumps({
                        'id': nav_id,
                        'method': 'Page.navigate',
                        'params': {'url': f'http://localhost:8089/{p}'}
                    }))

                    st = time.time()
                    while time.time() - st < 1.0:
                        try:
                            msg = await asyncio.wait_for(ws.recv(), timeout=0.15)
                            data = json.loads(msg)
                            if data.get('method') == 'Page.loadEventFired':
                                break
                        except asyncio.TimeoutError:
                            pass

                    eval_id = 200 + p_idx
                    await ws.send(json.dumps({
                        'id': eval_id,
                        'method': 'Runtime.evaluate',
                        'params': {'expression': check_overflow_js, 'returnByValue': True}
                    }))

                    val = {}
                    while True:
                        msg = await ws.recv()
                        data = json.loads(msg)
                        if data.get('id') == eval_id:
                            val = data.get('result', {}).get('result', {}).get('value', {})
                            break

                    has_scroll = val.get('hasScroll', False)
                    sw = val.get('scrollWidth', 0)
                    dw = val.get('docWidth', width)

                    if not has_scroll:
                        total_passes += 1
                        print(f"[{name[:12]:12}] {p:20}: PASS ({sw}px <= {dw}px)", flush=True)
                    else:
                        offender = val.get('offender')
                        off_text = f"<{offender['tag']} class='{offender['cls']}'> right={offender['right']}px text='{offender['text']}'" if offender else "unknown"
                        failures.append((name, p, sw, dw, off_text))
                        print(f"[{name[:12]:12}] {p:20}: FAIL ({sw}px > {dw}px) Offender: {off_text}", flush=True)

            print("\n-------------------------------------------------------------------------", flush=True)
            print(f"Audit Complete: {total_passes}/144 tests passed.", flush=True)
            if failures:
                print(f"Failures ({len(failures)}):", flush=True)
                for f in failures:
                    print(f"  ❌ {f[0]} - {f[1]}: {f[2]}px > {f[3]}px ({f[4]})", flush=True)
            else:
                print("✨ 100% PERFECT: Zero horizontal scrolling across ALL 12 viewports on all 12 pages!", flush=True)
            print("=========================================================================", flush=True)
    finally:
        proc.terminate()

asyncio.run(run_audit())
