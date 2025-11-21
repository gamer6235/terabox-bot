import requests
import re
import urllib.parse

def get_direct_url(share_url):
    try:
        # Normalize domain
        share_url = share_url.replace("teraboxshare.com", "www.1024tera.com")
        share_url = share_url.replace("terabox.com", "www.1024tera.com")
        share_url = share_url.replace("nephobox.com", "www.1024tera.com")

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        # Step 1 — GET share page
        r = requests.get(share_url, headers=headers, timeout=10)
        html = r.text

        # Step 2 — extract js file containing real file info
        m = re.search(r'src="(/static/js/main\.[^"]+)"', html)
        if not m:
            return None

        js_url = "https://www.1024tera.com" + m.group(1)
        js = requests.get(js_url, headers=headers, timeout=10).text

        # Step 3 — find the encoded file info URL
        info_match = re.search(r'"(https://api[^"]+file[^"]+)"', js)
        if not info_match:
            return None

        info_url = info_match.group(1)

        # Step 4 — request real file metadata
        info = requests.get(info_url, headers=headers, timeout=10).json()

        # Step 5 — download URL extract
        try:
            durl = info["data"]["download_url"]
            return urllib.parse.unquote(durl)
        except:
            return None

    except:
        return None
