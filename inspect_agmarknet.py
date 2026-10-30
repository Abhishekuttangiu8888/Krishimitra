
import re
import requests

url = "https://agmarknet.gov.in/static/js/main.06e10be8.js"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=60
)
response.raise_for_status()

javascript = response.text

terms = [
    "captcha_key",
    "captcha",
    "report_ticket",
    "dashboard-data/",
]

for term in terms:
    print("\n" + "=" * 60)
    print("Searching:", term)
    print("=" * 60)

    positions = [
        match.start()
        for match in re.finditer(re.escape(term), javascript, re.IGNORECASE)
    ]

    print("Occurrences:", len(positions))

    for position in positions[:3]:
        start = max(0, position - 1000)
        end = min(len(javascript), position + 1500)
        print("\n", javascript[start:end])
