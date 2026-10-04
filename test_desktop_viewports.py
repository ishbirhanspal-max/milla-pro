import subprocess, time, json, urllib.request, asyncio, websockets

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
port = 9340

pages = [
    'index.html', 'products.html', 'our-science.html', 'reports.html',
    'about.html', 'contact.html', 'faq.html', 'login.html',
    'shipping-policy.html', 'privacy-policy.html', 'refund-policy.html', 'terms.html'
]

async def test_desktop(width, height):
    proc = subprocess.Popen([
        chrome_path, f'--remote-debugging-port={port}',
        '--headless=new', f'--window-size={width},{height}',
        '--disable-gpu', '--no-sandbox', 'about:blank'
    ])
    await asyncio.sleep(1.5)
    try:
        resp = urllib.request.urlopen(f'http://localhost:{port}/json')
        ws_url = json.loads(resp.read().decode())[0]['webSocketDebuggerUrl']
        async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Page.enable'}))
            await ws.recv()

            check_js = """
            (() => {
                const docWidth = window.innerWidth;
                const scrollWidth = document.documentElement.scrollWidth;
                return {
                    docWidth: docWidth,
                    scrollWidth: scrollWidth,
                    hasScroll: scrollWidth > docWidth
                };
            })()
            """

            print(f"\n=======================================================", flush=True)
            print(f"AUDITING DESKTOP/LAPTOP VIEWPORT: {width}x{height}", flush=True)
            print(f"=======================================================", flush=True)

            for idx, p in enumerate(pages):
                req_id = 100 + idx
                await ws.send(json.dumps({
                    'id': req_id,
                    'method': 'Page.navigate',
                    'params': {'url': f'http://localhost:8089/{p}'}
                }))

                st = time.time()
                while time.time() - st < 1.0:
                    try:
                        m = await asyncio.wait_for(ws.recv(), timeout=0.15)
                        if json.loads(m).get('method') == 'Page.loadEventFired':
                            break
                    except asyncio.TimeoutError:
                        pass

                eval_id = 200 + idx
                await ws.send(json.dumps({
                    'id': eval_id,
                    'method': 'Runtime.evaluate',
                    'params': {'expression': check_js, 'returnByValue': True}
                }))

                while True:
                    m = await ws.recv()
                    data = json.loads(m)
                    if data.get('id') == eval_id:
                        val = data.get('result', {}).get('result', {}).get('value', {})
                        sw = val.get('scrollWidth')
                        dw = val.get('docWidth')
                        has_scroll = val.get('hasScroll')
                        status = f"PASS ({sw}px <= {dw}px)" if not has_scroll else f"FAIL ({sw}px > {dw}px)"
                        print(f"{p:22}: {status}", flush=True)
                        break
    finally:
        proc.terminate()

async def main():
    await test_desktop(1440, 900)
    await asyncio.sleep(1)
    await test_desktop(1920, 1080)

asyncio.run(main())
