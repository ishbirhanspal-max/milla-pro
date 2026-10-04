import subprocess, time, json, urllib.request, asyncio, websockets

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
port = 9347

async def test():
    proc = subprocess.Popen([chrome_path, f'--remote-debugging-port={port}', '--headless=new', '--disable-gpu', '--no-sandbox', 'about:blank'])
    await asyncio.sleep(1.5)
    try:
        resp = urllib.request.urlopen(f'http://localhost:{port}/json')
        ws_url = json.loads(resp.read().decode())[0]['webSocketDebuggerUrl']
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Page.enable'}))
            await ws.recv()
            await ws.send(json.dumps({'id': 2, 'method': 'Runtime.enable'}))
            await ws.recv()
            
            # Navigate to index.html and catch any syntax error in script.js
            await ws.send(json.dumps({'id': 3, 'method': 'Page.navigate', 'params': {'url': 'http://localhost:8089/index.html'}}))
            st = time.time()
            errors = []
            while time.time() - st < 2.0:
                try:
                    m = await asyncio.wait_for(ws.recv(), timeout=0.2)
                    d = json.loads(m)
                    if d.get('method') == 'Runtime.exceptionThrown':
                        errors.append(d['params']['exceptionDetails'])
                except asyncio.TimeoutError:
                    pass
            print("Errors on loading index.html:", errors)
    finally:
        proc.terminate()

asyncio.run(test())
