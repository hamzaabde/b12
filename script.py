import json
import hmac
import hashlib
import urllib.request
import os
from datetime import datetime, timezone

URL = "http://localhost:8000/"
SECRET = b"hello-there-from-b12"
REPO_LINK = os.environ.get('REPO_URL')
RUN_ID = os.environ.get('RUN_URL')

if not REPO_LINK and not RUN_ID:
    raise Exception("Script didn't run in GH actions environment")

timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

payload = {
    "timestamp": timestamp,
    "name": "Hamsa Abdirashid",
    "email": "hamzsaabdi@gmail.com",
    "resume_link": "https://www.linkedin.com/in/hamsaabdi/",
    "repository_link": REPO_LINK,
    "action_run_link": RUN_ID
}

# Create minified JSON and generate HMAC-SHA256 signature
body = json.dumps(payload, separators=(',', ':')).encode('utf-8')
signature = hmac.new(SECRET, body, hashlib.sha256).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}"
}

req = urllib.request.Request(URL, data=body, headers=headers, method="POST")

try:
    with urllib.request.urlopen(req) as response:
        res_text = response.read().decode('utf-8')
        if "localhost" not in URL:
            res_data = json.loads(res_text)
            print(res_data)
            print(f"Success! {res_data.get('receipt')}")
        else:
            print("Script not running in actions environment!")
            print(res_text)
            
except urllib.error.HTTPError as e:
    print(f"Error {e.code}: {e.read().decode()}")
