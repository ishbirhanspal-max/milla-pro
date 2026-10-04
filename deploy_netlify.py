import urllib.request, urllib.error, json, sys, os

def deploy(token):
    zip_path = 'milla-pro-store-netlify.zip'
    if not os.path.exists(zip_path):
        print(f"Error: {zip_path} not found.")
        sys.exit(1)

    with open(zip_path, 'rb') as f:
        zip_data = f.read()

    print(f"Uploading {zip_path} ({len(zip_data):,} bytes) to Netlify...")

    preferred_names = ['milla-pro-store', 'milla-pro-nutrition', 'milla-pro-atta', None]

    for name in preferred_names:
        url = 'https://api.netlify.com/api/v1/sites'
        if name:
            url += f"?name={name}"
            print(f"Attempting deploy with site name '{name}'...")
        else:
            print("Deploying with Netlify auto-assigned domain...")

        req = urllib.request.Request(
            url,
            data=zip_data,
            headers={
                'Content-Type': 'application/zip',
                'Authorization': f'Bearer {token.strip()}'
            },
            method='POST'
        )

        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                print("\n[SUCCESS] Netlify Deployment Succeeded!")
                print(f"Live URL:      {data.get('ssl_url') or data.get('url')}")
                print(f"Admin URL:     {data.get('admin_url')}")
                print(f"Site ID:       {data.get('site_id')}")
                print(f"Site Name:     {data.get('name')}.netlify.app")
                
                # Save result to a JSON file
                with open('netlify_deploy_result.json', 'w') as out_f:
                    json.dump(data, out_f, indent=2)
                return data
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode('utf-8', errors='ignore')
            if e.code == 422 and name:
                print(f"Subdomain '{name}' is already taken. Trying alternative...")
                continue
            else:
                print(f"\n[ERROR] Deployment Failed (HTTP {e.code}):\n{err_msg}")
                sys.exit(1)
        except Exception as ex:
            print(f"\n[ERROR] Unexpected Error:\n{ex}")
            sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python deploy_netlify.py <NETLIFY_AUTH_TOKEN>")
        sys.exit(1)
    deploy(sys.argv[1])
