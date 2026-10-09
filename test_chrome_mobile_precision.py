import subprocess, time, json, urllib.request, asyncio, websockets, os

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
port = 9334

async def run_tests():
    import tempfile
    user_data = tempfile.mkdtemp()
    proc = subprocess.Popen([
        chrome_path,
        f"--remote-debugging-port={port}",
        "--remote-allow-origins=*",
        f"--user-data-dir={user_data}",
        "--headless=new",
        "--window-size=393,852",
        "--disable-gpu",
        "--no-sandbox",
        "about:blank"
    ])
    await asyncio.sleep(1.5)

    try:
        resp = urllib.request.urlopen(f"http://127.0.0.1:{port}/json")
        pages = json.loads(resp.read().decode())
        ws_url = pages[0]["webSocketDebuggerUrl"].replace("localhost", "127.0.0.1")

        async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
            # Enable Page and Network
            await ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
            await ws.recv()
            await ws.send(json.dumps({"id": 2, "method": "Network.enable"}))
            await ws.recv()
            
            # Set iPhone User Agent
            await ws.send(json.dumps({
                "id": 3,
                "method": "Network.setUserAgentOverride",
                "params": {
                    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
                }
            }))
            await ws.recv()

            # Set Device Metrics Override: 393x852
            await ws.send(json.dumps({
                "id": 4,
                "method": "Emulation.setDeviceMetricsOverride",
                "params": {
                    "width": 393,
                    "height": 852,
                    "deviceScaleFactor": 3,
                    "mobile": True,
                    "fitWindow": True
                }
            }))
            await ws.recv()

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

            results = {}

            check_js = """
            (() => {
                const docWidth = window.innerWidth;
                const scrollWidth = document.documentElement.scrollWidth;
                const bodyWidth = document.body ? document.body.scrollWidth : 0;
                
                const overflowing = [];
                const all = document.querySelectorAll('*');
                for (const el of all) {
                    const rect = el.getBoundingClientRect();
                    // If element extends beyond viewport width
                    if (rect.right > docWidth + 0.5 || rect.left < -0.5) {
                        // ignore hidden or transparent elements
                        const style = window.getComputedStyle(el);
                        if (style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0') {
                            overflowing.push({
                                tag: el.tagName.toLowerCase(),
                                id: el.id || '',
                                class: (typeof el.className === 'string' ? el.className.trim() : ''),
                                left: Math.round(rect.left),
                                right: Math.round(rect.right),
                                width: Math.round(rect.width),
                                text: (el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 35)
                            });
                        }
                    }
                }
                return {
                    viewportWidth: docWidth,
                    scrollWidth: scrollWidth,
                    bodyWidth: bodyWidth,
                    hasHorizontalScroll: scrollWidth > docWidth,
                    overflowCount: overflowing.length,
                    overflowing: overflowing.slice(0, 15)
                };
            })()
            """

            for idx, page_name in enumerate(pages_to_test):
                url = f"http://localhost:8089/{page_name}"
                req_id = 100 + idx
                await ws.send(json.dumps({
                    "id": req_id,
                    "method": "Page.navigate",
                    "params": {"url": url}
                }))
                
                # Drain until loadEventFired or wait 1.5s
                start_t = time.time()
                while time.time() - start_t < 1.5:
                    try:
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.3)
                        data = json.loads(msg)
                        if data.get("method") == "Page.loadEventFired":
                            break
                    except asyncio.TimeoutError:
                        pass

                await asyncio.sleep(0.5)

                eval_id = 200 + idx
                await ws.send(json.dumps({
                    "id": eval_id,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": check_js,
                        "returnByValue": True
                    }
                }))

                # Find the eval response
                while True:
                    msg = await ws.recv()
                    data = json.loads(msg)
                    if data.get("id") == eval_id:
                        val = data.get("result", {}).get("result", {}).get("value", {})
                        results[page_name] = val
                        break

            # Print summary table
            print("\n=======================================================")
            print("AUTOMATED 393x852 MOBILE AUDIT RESULTS (ALL PAGES)")
            print("=======================================================")
            for page, res in results.items():
                vw = res.get('viewportWidth')
                sw = res.get('scrollWidth')
                has_scroll = res.get('hasHorizontalScroll')
                cnt = res.get('overflowCount', 0)
                status = "PASS (No Horizontal Scroll)" if not has_scroll else f"FAIL ({sw}px > {vw}px, {cnt} overflowing elements)"
                print(f"{page:22}: {status}")
                if has_scroll and res.get('overflowing'):
                    for item in res['overflowing'][:6]:
                        print(f"    -> <{item['tag']} class='{item['class']}' id='{item['id']}'> right={item['right']}px width={item['width']}px text='{item['text']}'")

    finally:
        proc.terminate()

asyncio.run(run_tests())
