import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DATA_GOV_IN_API_KEY")

URL = (
    "https://api.data.gov.in/resource/"
    "9ef84268-d588-465a-a308-a864a43d0070"
)

if not API_KEY:
    print("ERROR: DATA_GOV_IN_API_KEY missing from .env")
    raise SystemExit(1)

print("Testing data.gov.in...", flush=True)

try:
    response = requests.get(
        URL,
        params={
            "api-key": API_KEY,
            "format": "json",
            "limit": 1,
        },
        timeout=(5, 8),
    )

    print("HTTP:", response.status_code)

    if response.ok:
        data = response.json()
        print("SUCCESS")
        print("TOTAL:", data.get("total"))
        print("RECORDS:", data.get("records"))
    else:
        print("API ERROR:", response.text[:1000])

except requests.exceptions.Timeout:
    print("API TIMEOUT: data.gov.in did not respond within 8 seconds.")

except requests.exceptions.RequestException as error:
    print("CONNECTION ERROR:", error)