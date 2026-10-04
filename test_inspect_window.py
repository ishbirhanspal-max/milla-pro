import subprocess, time, json, urllib.request, asyncio, websockets

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
port = 9354

async def test():
    proc = subprocess.Popen([
        chrome_path, f'--remote-debugging-port={port}',
        '--headless=new', '--disable-extensions',
        '--disable-gpu', '--no-sandbox', 'about:blank'
    ])
    await asyncio.sleep(1.5)
    try:
        resp = urllib.request.urlopen(f'http://localhost:{port}/json')
        targets = json.loads(resp.read().decode())
        page_target = next(t for t in targets if t.get('type') == 'page')
        ws_url = page_target['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Page.enable'}))
            await ws.recv()
            await ws.send(json.dumps({'id': 2, 'method': 'Page.navigate', 'params': {'url': 'http://localhost:8089/index.html'}}))
            
            # Wait for loadEventFired
            st = time.time()
            while time.time() - st < 2.5:
                try:
                    m = await asyncio.wait_for(ws.recv(), timeout=0.2)
                    d = json.loads(m)
                    if d.get('method') == 'Page.loadEventFired':
                        break
                except asyncio.TimeoutError:
                    pass
            
            await asyncio.sleep(0.5)

            expr = "(() => { return { title: document.title, scriptCount: document.querySelectorAll('script').length, hasOpenCartDrawer: typeof window.openCartDrawer, hasSidebar: typeof window.openMobileSidebar, hasWheyCalc: typeof window.updateWheyCostCalc }; })()"
            await ws.send(json.dumps({'id': 10, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
            while True:
                m = await ws.recv()
                d = json.loads(m)
                if d.get('id') == 10:
                    print("PAGE INSPECTION WITH --disable-extensions:", d['result']['result']['value'])
                    break
    finally:
        proc.terminate()

asyncio.run(test())
