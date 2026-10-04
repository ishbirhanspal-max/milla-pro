import subprocess, time, json, urllib.request, asyncio, websockets

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
port = 9351

async def test():
    proc = subprocess.Popen([chrome_path, f'--remote-debugging-port={port}', '--headless=new', '--window-size=393,852', '--disable-gpu', '--no-sandbox', 'about:blank'])
    await asyncio.sleep(1.5)
    try:
        resp = urllib.request.urlopen(f'http://localhost:{port}/json')
        ws_url = json.loads(resp.read().decode())[0]['webSocketDebuggerUrl']
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Page.enable'}))
            await ws.recv()
            await ws.send(json.dumps({'id': 2, 'method': 'Page.navigate', 'params': {'url': 'http://localhost:8089/index.html'}}))
            
            # Wait for loadEventFired
            st = time.time()
            while time.time() - st < 3.0:
                try:
                    m = await asyncio.wait_for(ws.recv(), timeout=0.2)
                    d = json.loads(m)
                    if d.get('method') == 'Page.loadEventFired':
                        break
                except asyncio.TimeoutError:
                    pass
            
            await asyncio.sleep(0.5)

            # Test openCartDrawer
            expr = "(() => { openCartDrawer(); return document.getElementById('cartDrawer').classList.contains('active'); })()"
            await ws.send(json.dumps({'id': 10, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
            while True:
                m = await ws.recv()
                d = json.loads(m)
                if d.get('id') == 10:
                    print("EVAL RESULT FOR CART DRAWER:", d)
                    break
    finally:
        proc.terminate()

asyncio.run(test())
