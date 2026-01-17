import json
import hmac
import hashlib
import urllib.request
from datetime import datetime, timezone

URL = "https://b12.io/apply/submission"
SECRET = b"hello-there-from-b12"

# Generates ISO 8601 timestamp: YYYY-MM-DDTHH:MM:SS.mmmZ
timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

payload = {
    "timestamp": timestamp,
    "name": "Your Name",
    "email": "you@example.com",
    "resume_link": "https://linkedin.com/in/yourprofile",
    "repository_link": "https://github.com/youruser/yourrepo",
    "action_run_link": "https://github.com/youruser/yourrepo/actions/runs/123456789"
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
        res_data = json.loads(response.read().decode('utf-8'))
        print(res_data.get("receipt"))
except urllib.error.HTTPError as e:
    print(f"Error {e.code}: {e.read().decode()}")
