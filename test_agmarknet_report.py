import requests
import base64
import os
import tempfile

BASE = "https://api.agmarknet.gov.in/v1"

session = requests.Session()
headers = {
    "Origin": "https://agmarknet.gov.in",
    "Referer": "https://agmarknet.gov.in/",
    "User-Agent": "Mozilla/5.0"
}

# Generate CAPTCHA
r = session.post(
    f"{BASE}/captcha/generator",
    json={},
    headers=headers,
    timeout=30
)
r.raise_for_status()
data = r.json()

# Save image using a safe absolute path
image_path = os.path.join(tempfile.gettempdir(), "km_captcha.png")

with open(image_path, "wb") as f:
    f.write(base64.b64decode(data["captcha_image"]))

os.startfile(image_path)

answer = input("Enter the CAPTCHA shown: ").strip()

# Verify CAPTCHA
verify = session.post(
    f"{BASE}/captcha/verify",
    json={
        "captcha": answer,
        "captcha_key": data["captcha_key"]
    },
    headers=headers,
    timeout=30
)

print("Verification:", verify.text)

if verify.status_code != 200 or verify.json().get("status") != "success":
    raise SystemExit("CAPTCHA verification failed.")

# Test report endpoint
report = session.post(
    f"{BASE}/daily-price-arrival/report",
    data={
        "captcha": answer,
        "captcha_key": data["captcha_key"]
    },
    headers=headers,
    timeout=60
)

print("\nREPORT HTTP:", report.status_code)
print("REPORT RESPONSE:", report.text[:4000])