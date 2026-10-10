import subprocess, time, json, urllib.request, asyncio, websockets, tempfile

cdp_port = 9355
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

async def main():
    user_data = tempfile.mkdtemp()
    proc = subprocess.Popen([
        chrome_path,
        f"--remote-debugging-port={cdp_port}",
        f"--user-data-dir={user_data}",
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "http://localhost:8080/index.html"
    ])
    await asyncio.sleep(2.0)

    try:
        resp = urllib.request.urlopen(f"http://localhost:{cdp_port}/json")
        pages = json.loads(resp.read().decode())
        ws_url = pages[0]["webSocketDebuggerUrl"]

        async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
            # Set mobile emulation 393 x 852
            await ws.send(json.dumps({
                "id": 1,
                "method": "Emulation.setDeviceMetricsOverride",
                "params": {
                    "width": 393,
                    "height": 852,
                    "deviceScaleFactor": 3,
                    "mobile": True,
                    "scale": 1
                }
            }))
            await ws.recv()

            results = {}

            for page in ["index.html", "products.html"]:
                url = f"http://localhost:8080/{page}"
                await ws.send(json.dumps({
                    "id": 2,
                    "method": "Page.navigate",
                    "params": {"url": url}
                }))

                # wait for load
                await asyncio.sleep(1.5)

                # 1. Check horizontal scroll
                await ws.send(json.dumps({
                    "id": 10,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": "({ scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth, hasOverflow: document.documentElement.scrollWidth > window.innerWidth })",
                        "returnByValue": True
                    }
                }))
                h_res = json.loads(await ws.recv())["result"]["result"]["value"]

                # 2. Check header layout & cart button clipping
                await ws.send(json.dumps({
                    "id": 11,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": """(() => {
                            const cart = document.querySelector('.mh-cart-btn');
                            const menu = document.querySelector('.mh-menu-btn');
                            const logo = document.querySelector('.mh-logo');
                            const cartRect = cart ? cart.getBoundingClientRect() : null;
                            const menuRect = menu ? menu.getBoundingClientRect() : null;
                            const logoRect = logo ? logo.getBoundingClientRect() : null;
                            return {
                                cartExists: !!cart,
                                menuExists: !!menu,
                                logoExists: !!logo,
                                cartRect: cartRect ? { left: cartRect.left, right: cartRect.right, width: cartRect.width } : null,
                                menuRect: menuRect ? { left: menuRect.left, right: menuRect.right, width: menuRect.width } : null,
                                cartClipped: cartRect ? cartRect.right > window.innerWidth : false,
                                menuClipped: menuRect ? menuRect.right > window.innerWidth : false
                            };
                        })()""",
                        "returnByValue": True
                    }
                }))
                header_res = json.loads(await ws.recv())["result"]["result"]["value"]

                # 3. Check right-side sidebar drawer
                await ws.send(json.dumps({
                    "id": 12,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": """(() => {
                            if (typeof openSidebar === 'function') openSidebar();
                            const sb = document.getElementById('mobileSidebar');
                            if (!sb) return { error: 'No mobileSidebar' };
                            const r = sb.getBoundingClientRect();
                            const style = window.getComputedStyle(sb);
                            const onRight = (r.right >= window.innerWidth - 5) && (r.left > 0);
                            return {
                                isOpen: sb.classList.contains('active'),
                                right: style.right,
                                left: style.left,
                                rectRight: r.right,
                                rectLeft: r.left,
                                onRight: onRight
                            };
                        })()""",
                        "returnByValue": True
                    }
                }))
                sidebar_res = json.loads(await ws.recv())["result"]["result"]["value"]

                # Close sidebar
                await ws.send(json.dumps({
                    "id": 13,
                    "method": "Runtime.evaluate",
                    "params": {"expression": "if (typeof closeSidebar === 'function') closeSidebar();"}
                }))
                await ws.recv()
                await asyncio.sleep(0.3)

                # 4. Check cart drawer & verify NO duplicate floating bar or island below it
                await ws.send(json.dumps({
                    "id": 14,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": """(() => {
                            if (typeof openCartDrawer === 'function') openCartDrawer();
                            const cd = document.getElementById('cartDrawer');
                            const fi = document.getElementById('floatingIsland');
                            const sticky = document.getElementById('mobileStickyBar');
                            const cdStyle = cd ? window.getComputedStyle(cd) : null;
                            const fiStyle = fi ? window.getComputedStyle(fi) : null;
                            const stickyStyle = sticky ? window.getComputedStyle(sticky) : null;
                            return {
                                cartDrawerOpen: cd ? cd.classList.contains('active') || cd.classList.contains('open') : false,
                                cartDrawerRight: cdStyle ? cdStyle.right : null,
                                floatingIslandVisible: fiStyle ? fiStyle.display !== 'none' && fiStyle.opacity !== '0' : false,
                                stickyBarVisible: stickyStyle ? stickyStyle.display !== 'none' && stickyStyle.visibility !== 'hidden' : false
                            };
                        })()""",
                        "returnByValue": True
                    }
                }))
                cart_res = json.loads(await ws.recv())["result"]["result"]["value"]

                # Close cart drawer
                await ws.send(json.dumps({
                    "id": 15,
                    "method": "Runtime.evaluate",
                    "params": {"expression": "if (typeof closeCartDrawer === 'function') closeCartDrawer();"}
                }))
                await ws.recv()

                results[page] = {
                    "h_scroll": h_res,
                    "header": header_res,
                    "sidebar": sidebar_res,
                    "cart": cart_res
                }

            print(json.dumps(results, indent=2))

    finally:
        proc.kill()

asyncio.run(main())
