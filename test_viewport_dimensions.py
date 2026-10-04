import subprocess, time, json, urllib.request, asyncio, websockets

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
port = 9339

viewports = [320, 360, 375, 390, 393, 412, 768, 1024, 1280, 1440, 1920]

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

            for w in viewports:
                h = 800
                is_mobile = w < 768
                await ws.send(json.dumps({
                    'id': 10,
                    'method': 'Emulation.setDeviceMetricsOverride',
                    'params': {
                        'width': w,
                        'height': h,
                        'deviceScaleFactor': 1,
                        'mobile': is_mobile,
                        'scale': 1
                    }
                }))
                await ws.recv()

                await ws.send(json.dumps({
                    'id': 20,
                    'method': 'Page.navigate',
                    'params': {'url': 'http://localhost:8089/index.html'}
                }))
                
                # wait load
                st = time.time()
                while time.time() - st < 1.0:
                    try:
                        m = await asyncio.wait_for(ws.recv(), timeout=0.1)
                        if json.loads(m).get('method') == 'Page.loadEventFired':
                            break
                    except asyncio.TimeoutError:
                        pass
                
                await ws.send(json.dumps({
                    'id': 30,
                    'method': 'Runtime.evaluate',
                    'params': {
                        'expression': '({ innerWidth: window.innerWidth, scrollWidth: document.documentElement.scrollWidth })',
                        'returnByValue': True
                    }
                }))
                
                while True:
                    m = await ws.recv()
                    data = json.loads(m)
                    if data.get('id') == 30:
                        val = data.get('result', {}).get('result', {}).get('value', {})
                        print(f"Target Width: {w}px -> innerWidth: {val.get('innerWidth')}px, scrollWidth: {val.get('scrollWidth')}px, Overflow: {val.get('scrollWidth', 0) > val.get('innerWidth', 0)}", flush=True)
                        break
    finally:
        proc.terminate()

asyncio.run(test())
