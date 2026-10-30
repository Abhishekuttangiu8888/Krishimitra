import requests
import base64

s = requests.Session()
h = {
    "Origin": "https://agmarknet.gov.in",
    "Referer": "https://agmarknet.gov.in/",
    "User-Agent": "Mozilla/5.0"
}

r = s.post(
    "https://api.agmarknet.gov.in/v1/captcha/generator",
    json={}, headers=h, timeout=30
)
r.raise_for_status()
d = r.json()

with open("agmarknet_captcha.png", "wb") as f:
    f.write(base64.b64decode(d["captcha_image"]))

print("CAPTCHA image saved.")
import os
os.startfile(os.path.abspath("agmarknet_captcha.png"))

answer = input("Enter the characters shown: ").strip()

v = s.post(
    "https://api.agmarknet.gov.in/v1/captcha/verify",
    json={"captcha": answer, "captcha_key": d["captcha_key"]},
    headers=h, timeout=30
)

print("HTTP:", v.status_code)
print("Response:", v.text)
