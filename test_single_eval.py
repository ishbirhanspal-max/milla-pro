import subprocess, time, json, urllib.request, asyncio, websockets

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
port = 9346

async def test():
    proc = subprocess.Popen([
        chrome_path, f'--remote-debugging-port={port}',
        '--headless=new', '--disable-gpu', '--no-sandbox', 'about:blank'
    ])
    await asyncio.sleep(1.5)
    try:
        resp = urllib.request.urlopen(f'http://localhost:{port}/json')
        ws_url = json.loads(resp.read().decode())[0]['webSocketDebuggerUrl']
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Page.enable'}))
            await ws.recv()
            await ws.send(json.dumps({'id': 2, 'method': 'Page.navigate', 'params': {'url': 'http://localhost:8089/index.html'}}))
            await asyncio.sleep(1.5)
            await ws.send(json.dumps({
                'id': 3,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': '(() => { openCartDrawer(); return document.getElementById("cartDrawer").classList.contains("active"); })()',
                    'returnByValue': True
                }
            }))
            while True:
                msg = await ws.recv()
                d = json.loads(msg)
                if d.get('id') == 3:
                    print('Cart Drawer result:', d)
                    break
    finally:
        proc.terminate()

asyncio.run(test())
