import subprocess, time, json, urllib.request, asyncio, websockets

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
port = 9360

pages = ['index.html', 'products.html', 'our-science.html', 'reports.html']

async def test_live():
    proc = subprocess.Popen([
        chrome_path, f'--remote-debugging-port={port}',
        '--headless=new', '--window-size=393,852',
        '--disable-extensions', '--disable-gpu', '--no-sandbox', 'about:blank'
    ])
    await asyncio.sleep(2.0)
    try:
        resp = urllib.request.urlopen(f'http://localhost:{port}/json')
        targets = json.loads(resp.read().decode())
        page_target = next(t for t in targets if t.get('type') == 'page')
        ws_url = page_target['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Page.enable'}))
            await ws.recv()
            await ws.send(json.dumps({
                'id': 2,
                'method': 'Emulation.setDeviceMetricsOverride',
                'params': {'width': 393, 'height': 852, 'deviceScaleFactor': 3, 'mobile': True, 'fitWindow': True}
            }))
            await ws.recv()

            print("=======================================================", flush=True)
            print("LIVE NETLIFY 393x852 HORIZONTAL OVERFLOW VERIFICATION", flush=True)
            print("=======================================================", flush=True)

            for idx, p in enumerate(pages):
                await ws.send(json.dumps({'id': 10 + idx, 'method': 'Page.navigate', 'params': {'url': f'https://milla-pro-store.netlify.app/{p}'}}))
                await asyncio.sleep(2.0)
                eval_id = 20 + idx
                await ws.send(json.dumps({'id': eval_id, 'method': 'Runtime.evaluate', 'params': {'expression': '({ sw: document.documentElement.scrollWidth, dw: window.innerWidth })', 'returnByValue': True}}))
                while True:
                    m = await ws.recv()
                    d = json.loads(m)
                    if d.get('id') == eval_id:
                        v = d['result']['result']['value']
                        sw = v.get('sw')
                        dw = v.get('dw')
                        status = "PASS (0px overflow)" if sw <= dw else f"FAIL ({sw}px > {dw}px)"
                        print(f"LIVE {p:16}: {status} [scrollWidth: {sw}px, docWidth: {dw}px]", flush=True)
                        break
    finally:
        proc.terminate()

asyncio.run(test_live())
