import json
import hmac
import hashlib
import urllib.request
import os
from datetime import datetime, timezone

URL = "https://b12.io/apply/submission"
SECRET = b"hello-there-from-b12"
REPO_LINK = os.environ.get('REPO_URL')
RUN_ID = os.environ.get('RUN_URL')

if not REPO_LINK or not RUN_ID:
    REPO_LINK = REPO_LINK or "https://github.com/hamsa/test"
    RUN_ID = RUN_ID or "https://github.com/hamsa/test/actions/runs/1"

timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

payload = {
    "timestamp": timestamp,
    "name": "Hamsa Abdirashid",
    "email": "hamzsaabdi@gmail.com",
    "resume_link": "https://www.linkedin.com/in/hamsaabdi/",
    "repository_link": REPO_LINK,
    "action_run_link": RUN_ID
}


body = json.dumps(payload, separators=(',', ':'), sort_keys=True).encode('utf-8')
signature = hmac.new(SECRET, body, hashlib.sha256).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}"
}

req = urllib.request.Request(URL, data=body, headers=headers, method="POST")

try:
    with urllib.request.urlopen(req) as response:
        res_text = response.read().decode('utf-8')
        res_data = json.loads(res_text)
        print(res_data.get("receipt"))
except urllib.error.HTTPError as e:
    error_body = e.read().decode()
    print(f"Error {e.code}: {error_body}")