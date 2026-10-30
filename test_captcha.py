import requests
import base64

session = requests.Session()

headers = {
    "Origin": "https://agmarknet.gov.in",
    "Referer": "https://agmarknet.gov.in/",
    "User-Agent": "Mozilla/5.0"
}

# Generate one fresh CAPTCHA
r = session.post(
    "https://api.agmarknet.gov.in/v1/captcha/generator",
    json={},
    headers=headers,
    timeout=30
)
r.raise_for_status()

data = r.json()
captcha_key = data["captcha_key"]

with open("agmarknet_captcha.png", "wb") as f:
    f.write(base64.b64decode(data["captcha_image"]))

print("Open agmarknet_captcha.png and read the characters.")
input("Press Enter after opening the image...")

answer = input("Enter CAPTCHA: ").strip()

# Verify the same challenge exactly once
v = session.post(
    "https://api.agmarknet.gov.in/v1/captcha/verify",
    json={
        "captcha": answer,
        "captcha_key": captcha_key
    },
    headers=headers,
    timeout=30
)

print("HTTP:", v.status_code)
print("Response:", v.text)