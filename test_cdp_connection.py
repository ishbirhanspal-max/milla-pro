import subprocess, time, json, urllib.request, os

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
port = 9333

# Launch Chrome headless
cmd = [
    chrome_path,
    f"--remote-debugging-port={port}",
    "--headless=new",
    "--window-size=393,852",
    "--disable-gpu",
    "--no-sandbox",
    "about:blank"
]

proc = subprocess.Popen(cmd)
time.sleep(1.5)

try:
    # Get available pages
    resp = urllib.request.urlopen(f"http://localhost:{port}/json")
    pages = json.loads(resp.read().decode())
    ws_url = pages[0]["webSocketDebuggerUrl"]
    print("Chrome connected! Target WS:", ws_url)
    
except Exception as e:
    print("Error connecting to Chrome:", e)
finally:
    proc.terminate()
