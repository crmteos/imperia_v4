import urllib.request
import json

token = "8680343291:AAEl-um1UGMy4memLKQybK3MN-w8hYig21c"
url = f"https://api.telegram.org/bot{token}/getUpdates"
try:
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    print(json.dumps(data, ensure_ascii=False, indent=2))
except Exception as e:
    print(f"Error: {e}")