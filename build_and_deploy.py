import os, zipfile, urllib.request, urllib.error, json

folder = r'C:\Users\ishbi\.gemini\antigravity-ide\scratch\milla-pro-store'
zip_out = os.path.join(folder, 'milla-pro-store-netlify.zip')

# Explicit, curated list of authentic production files
production_files = [
    'index.html',
    'products.html',
    'our-science.html',
    'science.html',
    'reports.html',
    'about.html',
    'contact.html',
    'faq.html',
    'login.html',
    'privacy-policy.html',
    'refund-policy.html',
    'shipping-policy.html',
    'terms.html',
    'style.css',
    'script.js',
    'netlify.toml',
    '_redirects',
    'milla-pouch-front.jpeg',
    'milla-pouch-back.jpeg',
    'milla-pouch-cover.jpeg',
    'roti-broken-down.jpeg',
    'wheat-fraction.jpeg',
    'soya-fraction.jpeg',
    'peanut-fraction.jpeg',
    'envirocare-lab-report-p1.png',
    'envirocare-lab-report-p2.png',
    'lab report.pdf',
    'milld_components.css'
]

print("Packaging production assets:")
with zipfile.ZipFile(zip_out, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for f in production_files:
        fpath = os.path.join(folder, f)
        if os.path.exists(fpath):
            z.write(fpath, arcname=f)
            print(f"  [+] {f} ({os.path.getsize(fpath):,} bytes)")
        else:
            print(f"  [!] WARNING: {f} NOT FOUND!")

print(f"\nCreated clean production zip: {zip_out} ({os.path.getsize(zip_out):,} bytes)")

# Deploy to Netlify API
token = 'nfp_FnVPwxmFeNUXEyh1rHJ3YogBc2iu81yLf4b3'
site_id = '41751cd3-803a-4fa6-b298-07768ca46bfd'

print(f"\nUploading deployment to Netlify site {site_id}...")

with open(zip_out, 'rb') as f:
    zip_bytes = f.read()

req = urllib.request.Request(
    f'https://api.netlify.com/api/v1/sites/{site_id}/deploys',
    data=zip_bytes,
    headers={
        'Content-Type': 'application/zip',
        'Authorization': f'Bearer {token}'
    },
    method='POST'
)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print("\n[SUCCESS] Deployed to Netlify successfully!")
        print("Site URL:    ", res.get('ssl_url') or f"https://{res.get('name')}.netlify.app")
        print("Deploy URL:  ", res.get('deploy_ssl_url'))
        print("Deploy State:", res.get('state'))
        print("Site Name:   ", res.get('name'))
        
        with open(os.path.join(folder, 'netlify_deploy_result.json'), 'w') as out_f:
            json.dump(res, out_f, indent=2)
except urllib.error.HTTPError as e:
    print(f"HTTPError {e.code}: {e.read().decode('utf-8')}")
except Exception as ex:
    print(f"Error: {ex}")
