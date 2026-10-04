import subprocess, time, json, urllib.request, asyncio, websockets, sys

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
port = 9336

pages = [
    'index.html', 'products.html', 'our-science.html', 'reports.html',
    'about.html', 'contact.html', 'faq.html', 'login.html',
    'shipping-policy.html', 'privacy-policy.html', 'refund-policy.html', 'terms.html'
]

async def check_errors():
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
            await ws.send(json.dumps({'id': 2, 'method': 'Runtime.enable'}))
            await ws.recv()

            print("=======================================================", flush=True)
            print("AUTOMATED CONSOLE & RUNTIME EXCEPTION AUDIT", flush=True)
            print("=======================================================", flush=True)

            for idx, p in enumerate(pages):
                errors = []
                req_id = 100 + idx
                await ws.send(json.dumps({
                    'id': req_id,
                    'method': 'Page.navigate',
                    'params': {'url': f'http://localhost:8089/{p}'}
                }))

                st = time.time()
                while time.time() - st < 1.0:
                    try:
                        msg = await asyncio.wait_for(ws.recv(), timeout=0.15)
                        data = json.loads(msg)
                        method = data.get('method', '')
                        if method == 'Runtime.exceptionThrown':
                            exc = data.get('params', {}).get('exceptionDetails', {})
                            desc = exc.get('text', '') + ' ' + exc.get('exception', {}).get('description', '')
                            errors.append(desc)
                        elif method == 'Runtime.consoleAPICalled':
                            if data.get('params', {}).get('type') == 'error':
                                args = [str(a.get('value', '')) for a in data.get('params', {}).get('args', [])]
                                errors.append('Console error: ' + ' '.join(args))
                    except asyncio.TimeoutError:
                        pass

                status = "PASS (0 errors)" if not errors else f"FAIL ({len(errors)} errors: {errors})"
                print(f"{p:22}: {status}", flush=True)
    finally:
        proc.terminate()

asyncio.run(check_errors())
